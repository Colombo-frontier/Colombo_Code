"""Bounded, resumable OpenAI Code Interpreter experiments.

The service records execution evidence, never a mathematical verdict. A failed
connection after a POST is deliberately not retried: a response whose identifier
is unknown may still be consuming compute remotely.
"""
from __future__ import annotations

import base64
from contextlib import contextmanager, ExitStack
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Callable
from copy import deepcopy
import json
import os
from pathlib import PurePosixPath
from pathlib import PureWindowsPath
from colombo.shared.file_io import Path, file_lock
from colombo.shared.file_io import atomic_write
import re
import time
from uuid import uuid4

import requests

from colombo.shared.runtime_budget import finite_min
from colombo.shared.runtime_budget import remaining_seconds as remaining
from colombo.shared.runtime_budget import expired

from colombo.shared.file_io import json_equal


@dataclass(frozen=True)
class ExperimentContext:
    """Caller-supplied task settings and record operations; no role-owned store."""
    read_settings: Callable[[], dict]
    resolve_refs: Callable[[list[dict]], list[dict]]
    write_result: Callable[[str, dict], dict]
    restore_settings: Callable[[dict], dict]
    deadline: Callable[[str], float | None]


_context = ContextVar("experiment_execution_context")


BASE_URL = "https://api.openai.com/v1"
_PENDING = {"preparing", "submitted", "running", "remote_unknown", "download_pending"}
_REMOTE_RUNNING = {"queued", "in_progress"}
_ID = re.compile(r"[A-Za-z0-9_-]+\Z")


class ExperimentError(ValueError):
    """Actionable local validation error (contains no transport credentials)."""


class _TransportError(Exception):
    def __init__(self, reason: str, *, uncertain: bool = False, details: dict | None = None):
        self.reason, self.uncertain, self.details = reason, uncertain, details or {}
        super().__init__(reason)


def _json(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       allow_nan=False, indent=2) + "\n").encode("utf-8")


def _save(path: Path, value: dict) -> None:
    atomic_write(path, _json(value))


def _read(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ExperimentError("Experiment metadata must be a JSON object")
    return value


def _safe_file(root: Path, relative: str, *, must_exist: bool = True) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ExperimentError("File paths must be task-relative POSIX paths")
    value = PurePosixPath(relative)
    if value.is_absolute() or PureWindowsPath(relative).drive or ".." in value.parts:
        raise ExperimentError("Files must remain inside the current task")
    candidate = root.joinpath(*value.parts)
    if candidate.resolve().is_relative_to(root) is False:
        raise ExperimentError("File escapes the current task")
    for parent in [candidate, *candidate.parents]:
        if parent == root:
            break
        if parent.is_symlink() or (hasattr(parent, "is_junction") and parent.is_junction()):
            raise ExperimentError("Experiment paths cannot contain symlinks or junctions")
    if must_exist and not candidate.is_file():
        raise ExperimentError("Input file does not exist in this task")
    return candidate


@contextmanager
def _operation(root: Path):
    directory = _safe_file(root, "experiments", must_exist=False)
    directory.mkdir(exist_ok=True)
    lock = _safe_file(root, "experiments/.lock", must_exist=False)
    with ExitStack() as stack:
        try:
            stack.enter_context(file_lock(lock, timeout=0))
        except TimeoutError:
            raise ExperimentError("Another experiment operation is active in this task") from None
        yield directory


class _Client:
    """Only this object holds credentials; never serialize exceptions/headers."""
    def __init__(self, key: str, settings: dict, deadline: float | None):
        self.key, self.settings, self.deadline = key, settings, deadline
        self.session = requests.Session()
        self.session.headers.update({"Authorization": "Bearer " + key})

    def close(self):
        self.session.close()

    def _request(self, method: str, path: str, **kwargs):
        remaining_seconds = remaining(self.deadline, wall=True)
        if remaining_seconds <= 0:
            raise _TransportError("operation_deadline")
        network = self.settings["network"]
        timeout = (min(network["connect_timeout_seconds"], remaining_seconds / 2),
                   min(network["read_timeout_seconds"], remaining_seconds / 2))
        try:
            response = self.session.request(method, BASE_URL + path, timeout=timeout,
                                            allow_redirects=False, stream=True, **kwargs)
        except requests.RequestException:
            raise _TransportError("connection_interrupted", uncertain=method == "POST") from None
        if not 200 <= response.status_code < 300:
            # HTTP status is sufficient to distinguish credentials/quota/model and
            # capacity problems. Server-provided messages can echo user secrets.
            status = response.status_code
            response.close()
            raise _TransportError("api_http_error", uncertain=method == "POST" and status >= 500,
                                  details={"http_status": status})
        return response

    def _bytes(self, response, maximum: int) -> bytes:
        parts, size = [], 0
        try:
            for chunk in response.iter_content(self.settings["network"]["chunk_bytes"]):
                if expired(self.deadline, wall=True):
                    raise _TransportError("operation_deadline")
                size += len(chunk)
                if size > maximum:
                    raise _TransportError("artifact_size_limit")
                parts.append(chunk)
        except requests.RequestException:
            raise _TransportError("download_interrupted") from None
        finally:
            response.close()
        result = b"".join(parts)
        if self.key.encode() in result:
            raise _TransportError("credential_in_response")
        return result

    def json(self, method: str, path: str, body: dict | None = None) -> dict:
        response = self._request(method, path, json=body)
        try:
            data = self._bytes(response, self.settings["experiment"]["artifact_max_bytes"])
            result = json.loads(data)
            if not isinstance(result, dict):
                raise ValueError()
            return result
        except (_TransportError, ValueError) as exc:
            if isinstance(exc, _TransportError):
                exc.uncertain = exc.uncertain or method == "POST"
                raise
            raise _TransportError("invalid_api_response", uncertain=method == "POST") from None

    def upload(self, container_id: str, name: str, data: bytes) -> dict:
        response = self._request("POST", f"/containers/{container_id}/files",
                                 files={"file": (name, data, "application/octet-stream")})
        try:
            result = json.loads(self._bytes(response, self.settings["experiment"]["artifact_max_bytes"]))
            if not isinstance(result, dict):
                raise ValueError()
            return result
        except (ValueError, _TransportError):
            raise _TransportError("upload_outcome_unknown", uncertain=True) from None

    def download(self, container_id: str, file_id: str, maximum: int) -> bytes:
        return self._bytes(self._request("GET", f"/containers/{container_id}/files/{file_id}/content"), maximum)


def _identifier(value, label: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise _TransportError("invalid_" + label)
    return value


def _response_path(response_id: str) -> str:
    return f"/responses/{response_id}?include%5B%5D=code_interpreter_call.outputs"


def _window(config: dict, deadline: float | None) -> float:
    seconds = float("inf") if config["timeout_seconds"] == "unlimited" else float(config["timeout_seconds"])
    return min(seconds, remaining(deadline))


def _input_path(root: Path, relative: str) -> Path:
    path = _safe_file(root, relative)
    parts = {part.lower() for part in PurePosixPath(relative).parts}
    basename = path.name.lower()
    if parts & {".ssh", ".aws", ".azure", ".codex", ".git", "credentials", "secrets"} or basename in {
        "auth.json", "credentials.json", "credentials.toml", "credentials.ini", "id_rsa", "id_ed25519",
        ".netrc", ".npmrc", ".pypirc", "secrets.json", "secrets.toml",
    } or basename == ".env" or basename.startswith(".env.") or path.suffix.lower() in {".pem", ".key", ".pfx", ".p12"}:
        raise ExperimentError("Credential/configuration files cannot be experiment inputs")
    return path


def _key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise ExperimentError("OPENAI_API_KEY is unavailable; no hosted experiment was submitted")
    return key


def _fixed_ref(ref: dict, label: str) -> dict:
    if not isinstance(ref, dict) or set(ref) != {"kind", "id", "revision"}:
        raise ExperimentError(label + " must pin kind, id, revision")
    record = _context.get().resolve_refs([ref])[0]
    return {key: record[key] for key in ("kind", "id", "revision")}


def _artifact(root: Path, state: dict, relative: str, data: bytes, config: dict) -> None:
    """Write-once files: transport/remote names never choose a local destination."""
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key and key.encode() in data:
        raise _TransportError("credential_in_artifact")
    manifest = state["artifacts"]
    old = next((item for item in manifest if item["path"] == relative), None)
    entry = {"path": relative, "size": len(data)}
    if old is not None and old != entry:
        raise _TransportError("immutable_artifact_changed")
    if len(data) > config["artifact_max_bytes"]:
        raise _TransportError("artifact_size_limit")
    if old is None and (len(manifest) >= config["max_files"] or
                        sum(item["size"] for item in manifest) + len(data) > config["max_total_artifact_bytes"]):
        raise _TransportError("artifact_budget_limit")
    destination = _safe_file(root, relative, must_exist=False)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if not destination.is_file() or destination.read_bytes() != data:
            raise _TransportError("immutable_artifact_changed")
    else:
        # A hard parent-process stop must leave either the complete file or no
        # file, not an irreparable prefix mistaken for immutable evidence.
        atomic_write(destination, data)
    if old is None:
        manifest.append(entry)


def _persist(root: Path, directory: Path, plan: dict, state: dict) -> dict:
    # Durable checkpoint precedes the Store revision. A crash between these
    # writes is repaired by the next run/resume call, without another POST.
    _save(directory / "state.json", state)
    payload = {key: plan[key] for key in ("question", "target_ref", "parameters", "input_files",
                                          "attempt_ref", "code_file")}
    payload.update(execution=state["execution"], artifacts=state["artifacts"])
    record = _context.get().write_result(plan["experiment_id"], payload)
    return {"experiment_id": plan["experiment_id"], "status": state["execution"]["status"],
            "record_ref": {key: record[key] for key in ("kind", "id", "revision")},
            "plan_file": f"experiments/{plan['experiment_id']}/plan.json",
            "state_file": f"experiments/{plan['experiment_id']}/state.json",
            "artifact_count": len(state["artifacts"]),
            "reason": state["execution"].get("reason"),
            "resume_available": state["execution"]["status"] in _PENDING}


def _wrapper(plan: dict, code: bytes, remote_inputs: dict) -> bytes:
    """Run exact supplied bytes once and emit independently checkable receipts."""
    values = {"id": plan["experiment_id"], "nonce": plan["nonce"],
              "code": base64.b64encode(code).decode(),
              "parameters": plan["parameters"], "inputs": remote_inputs}
    return ('''import base64, contextlib, importlib.metadata, json, os, pathlib, sys, traceback
V = json.loads(base64.b64decode("''' + base64.b64encode(_json(values)).decode() + '''"))
out = pathlib.Path("/mnt/data") / ("cell-" + V["id"])
out.mkdir(exist_ok=True)
receipt_path = out / "execution_receipt.json"
if receipt_path.exists():
    print("Already executed; existing receipt:", receipt_path)
else:
    code = base64.b64decode(V["code"])
    receipt = {"experiment_id": V["id"], "nonce": V["nonce"], "status": "failed"}
    environment = {"python": sys.version, "packages": {}}
    for name in ("numpy", "scipy", "sympy", "mpmath"):
        try: environment["packages"][name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: environment["packages"][name] = None
    (out / "environment.json").write_text(json.dumps(environment, indent=2), encoding="utf-8")
    with (out / "stdout.txt").open("w", encoding="utf-8") as stdout, (out / "stderr.txt").open("w", encoding="utf-8") as stderr:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                os.chdir(out)
                exec(compile(code, "requested_code.py", "exec"), {"__name__": "__main__", "PARAMETERS": V["parameters"], "INPUT_FILES": V["inputs"], "OUTPUT_DIR": str(out)})
                receipt["status"] = "completed"
            except BaseException as exc:
                receipt["error_type"] = type(exc).__name__
                traceback.print_exc()
    receipt["files"] = []
    for path in sorted(out.rglob("*")):
        if path.is_file() and not path.is_symlink() and path != receipt_path:
            data = path.read_bytes()
            receipt["files"].append({"name": path.relative_to(out).as_posix(), "size": len(data)})
    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print("Execution receipt:", receipt_path)
''').encode()


def _remote_path(value) -> str:
    if not isinstance(value, str) or not value.startswith("/mnt/data/") or ".." in PurePosixPath(value).parts or "\\" in value:
        raise _TransportError("invalid_remote_file_path")
    return value


def _cancel(root, directory, plan, state, client):
    execution = state["execution"]
    execution.update(status="remote_unknown", reason="deadline_cancellation_unconfirmed")
    _persist(root, directory, plan, state)
    if execution.get("response_id"):
        result = client.json("POST", f"/responses/{execution['response_id']}/cancel")
        execution["remote_status"] = result.get("status")
        if result.get("status") == "cancelled":
            execution.update(status="timed_out", reason="execution_deadline", completed_at=time.time())
        elif result.get("status") not in _REMOTE_RUNNING:
            return result
    return None


def _download(root, directory, plan, state, client, response, config):
    prefix = f"experiments/{plan['experiment_id']}/"
    execution = state["execution"]
    execution.update(status="download_pending", remote_status=response.get("status"))
    _persist(root, directory, plan, state)
    _artifact(root, state, prefix + "transport/response.json", _json(response), config)
    calls = [item for item in response.get("output", []) if item.get("type") == "code_interpreter_call"]
    for index, call in enumerate(calls):
        _artifact(root, state, prefix + f"outputs/executed_code_{index}.py", (call.get("code") or "").encode(), config)
    _artifact(root, state, prefix + "outputs/tool_outputs.json", _json(calls), config)
    if not any(call.get("status") == "completed" and state["wrapper_path"] in (call.get("code") or "")
               and "runpy.run_path" in (call.get("code") or "") for call in calls):
        execution.update(status="failed", reason="execution_evidence_missing", completed_at=time.time())
        return
    remote_root = "/mnt/data/cell-" + plan["experiment_id"] + "/"
    items, after = [], None
    while True:
        query = "?after=" + after if after else ""
        listing = client.json("GET", f"/containers/{execution['container_id']}/files" + query)
        batch = listing.get("data", [])
        if not isinstance(batch, list):
            raise _TransportError("invalid_file_listing")
        for item in batch:
            path = _remote_path(item.get("path", item.get("filename")))
            if path.startswith(remote_root):
                items.append({"id": _identifier(item.get("id"), "file_id"), "name": path[len(remote_root):]})
        if len(items) > config["max_files"]:
            raise _TransportError("artifact_count_limit")
        if not listing.get("has_more"):
            break
        next_after = _identifier(listing.get("last_id"), "pagination_id")
        if after == next_after or not batch:
            raise _TransportError("invalid_file_pagination")
        after = next_after
    if len({item["name"] for item in items}) != len(items):
        raise _TransportError("duplicate_remote_artifact")
    state.setdefault("downloads", {})
    for item in sorted(items, key=lambda item: item["name"]):
        remote_name = item["name"]
        # No remote path is ever joined to the local workspace.
        local = prefix + "outputs/file_" + uuid4().hex[:16] + ".bin"
        old = state["downloads"].get(remote_name)
        if old:
            data = _safe_file(root, old["path"]).read_bytes()
        else:
            remaining = config["max_total_artifact_bytes"] - sum(item["size"] for item in state["artifacts"])
            data = client.download(execution["container_id"], item["id"], min(config["artifact_max_bytes"], remaining))
            _artifact(root, state, local, data, config)
            state["downloads"][remote_name] = {"path": local, "size": len(data), "remote_file_id": item["id"]}
            _persist(root, directory, plan, state)
    downloaded = state["downloads"]
    if not {"execution_receipt.json", "environment.json", "stdout.txt", "stderr.txt"} <= downloaded.keys():
        raise _TransportError("required_artifacts_missing")
    try:
        receipt = _read(_safe_file(root, downloaded["execution_receipt.json"]["path"]))
        environment = _read(_safe_file(root, downloaded["environment.json"]["path"]))
    except (ValueError, OSError):
        raise _TransportError("invalid_execution_receipt") from None
    if any(receipt.get(key) != plan[key] for key in ("experiment_id", "nonce")):
        raise _TransportError("execution_receipt_mismatch")
    if not isinstance(environment.get("python"), str) or not isinstance(environment.get("packages"), dict):
        raise _TransportError("environment_manifest_missing")
    if not isinstance(receipt.get("files"), list):
        raise _TransportError("invalid_execution_receipt")
    for item in receipt["files"]:
        found = downloaded.get(item.get("name"))
        if not found or any(found[key] != item.get(key) for key in ("size",)):
            raise _TransportError("generated_artifact_missing_or_changed")
    expected = {item["name"] for item in receipt["files"]} | {"execution_receipt.json"}
    if set(downloaded) != expected:
        raise _TransportError("generated_artifact_manifest_mismatch")
    if receipt.get("status") not in {"completed", "failed"}:
        raise _TransportError("invalid_execution_status")
    _artifact(root, state, prefix + "outputs/download_manifest.json", _json(downloaded), config)
    execution.update(status=receipt["status"], completed_at=time.time(), environment=environment,
                     reason="script_error" if receipt["status"] == "failed" else None,
                     output_files=downloaded)
    execution["usage"] = response.get("usage")
    _persist(root, directory, plan, state)


def _execution_settings(root: Path, plan: dict) -> dict:
    snapshot = deepcopy(plan["settings_snapshot"])
    if "reasoning_effort" not in snapshot["experiment"]:
        # Older plans pinned the execution effort under the Cell model. Resolve
        # that historical value before managed_settings can merge live defaults;
        # never rewrite the plan or reinterpret an already submitted request.
        effort = snapshot.get("model", {}).get("reasoning_effort")
        if not isinstance(effort, str) or not effort.strip():
            raise ExperimentError("Historical experiment plan is missing its pinned reasoning effort")
        snapshot["experiment"]["reasoning_effort"] = effort
    return _context.get().restore_settings(snapshot)


def _continue(root: Path, directory: Path, plan: dict, state: dict, *, submit: bool = False) -> dict:
    settings = _execution_settings(root, plan)
    config = settings["experiment"]
    execution = state["execution"]
    if execution["status"] not in _PENDING:
        return _persist(root, directory, plan, state)
    seconds = _window(config, _context.get().deadline("work"))
    if seconds <= 0:
        return _persist(root, directory, plan, state)
    operation_deadline = None if seconds == float("inf") else time.time() + seconds
    from colombo.shared.runtime_budget import get_budget_context
    managed = get_budget_context(root)
    if managed is not None:
        # All research stops at the root work boundary; transport cleanup uses
        # its already reserved closing window, without taking another reserve.
        execution["deadline_at"] = operation_deadline
        cleanup = _context.get().deadline("hard")
        operation_deadline = None if cleanup is None else time.time() + remaining(cleanup)
        execution["total_deadline_at"] = operation_deadline
        execution["budget_policy_revision"] = managed["policy_revision"]
    if submit:
        operation_deadline = finite_min(operation_deadline, execution["total_deadline_at"])
    client = _Client(_key(), settings, operation_deadline)
    stage = "resume"
    try:
        if submit:
            client.deadline = finite_min(operation_deadline, execution["deadline_at"])
            stage = "create_container"
            execution.update(status="remote_unknown", reason="container_submission_started")
            _persist(root, directory, plan, state)
            container = client.json("POST", "/containers", {"name": "cell-" + plan["experiment_id"], "memory_limit": config["memory_limit"]})
            execution["container_id"] = _identifier(container.get("id"), "container_id")
            _persist(root, directory, plan, state)
            stage = "upload_inputs"
            paths = {}
            for item in plan["input_files"]:
                copied = _safe_file(root, item["saved_path"]).read_bytes()
                uploaded = client.upload(execution["container_id"], item["upload_name"], copied)
                paths[item["path"]] = _remote_path(uploaded.get("path"))
            wrapper = _wrapper(plan, (directory / "requested_code.py").read_bytes(), paths)
            _artifact(root, state, f"experiments/{plan['experiment_id']}/runner.py", wrapper, config)
            _persist(root, directory, plan, state)
            uploaded = client.upload(execution["container_id"], plan["experiment_id"] + "-runner.py", wrapper)
            state["wrapper_path"] = _remote_path(uploaded.get("path"))
            _persist(root, directory, plan, state)
            if expired(execution["deadline_at"], wall=True):
                execution.update(status="timed_out", reason="preparation_deadline")
                return _persist(root, directory, plan, state)
            invocation = "import runpy\nrunpy.run_path(" + repr(state["wrapper_path"]) + ", run_name='__main__')"
            payload = {"model": execution["model"], "background": True, "store": True,
                       "reasoning": {"effort": config["reasoning_effort"]},
                       "max_output_tokens": config["max_output_tokens"], "max_tool_calls": config["max_tool_calls"],
                       "tools": [{"type": "code_interpreter", "container": execution["container_id"]}],
                       "tool_choice": "required", "include": ["code_interpreter_call.outputs"],
                       "instructions": "Execute the supplied Python invocation exactly once using Code Interpreter. The uploaded wrapper runs the prepared experiment and saves its receipt and files. Do not alter scripts, run other research, or interpret results as a proof. Return only the receipt path.",
                       "input": invocation}
            _artifact(root, state, f"experiments/{plan['experiment_id']}/transport/request.json", _json(payload), config)
            stage = "submit_response"
            execution.update(status="remote_unknown", reason="response_submission_started")
            _persist(root, directory, plan, state)
            response = client.json("POST", "/responses", payload)
            execution.update(response_id=_identifier(response.get("id"), "response_id"), status="submitted", reason=None)
            _persist(root, directory, plan, state)
        else:
            if not execution.get("response_id"):
                execution.update(status="remote_unknown", reason="submission_id_unknown_no_resubmit")
                return _persist(root, directory, plan, state)
            response = client.json("GET", _response_path(execution["response_id"]))
        stage = "poll_response"
        while response.get("status") in _REMOTE_RUNNING:
            execution.update(status="running", remote_status=response["status"], reason=None)
            _persist(root, directory, plan, state)
            if expired(execution["deadline_at"], wall=True):
                stage = "cancel_response"
                client.deadline = operation_deadline
                response = _cancel(root, directory, plan, state, client)
                break
            time.sleep(min(config["poll_seconds"], remaining(execution["deadline_at"], wall=True)))
            if expired(execution["deadline_at"], wall=True):
                stage = "cancel_response"
                client.deadline = operation_deadline
                response = _cancel(root, directory, plan, state, client)
                break
            client.deadline = finite_min(operation_deadline, execution["deadline_at"])
            response = client.json("GET", _response_path(execution["response_id"]))
        if response is not None:
            remote_status = response.get("status")
            if remote_status in {"completed", "incomplete", "failed"}:
                stage = "download"
                client.deadline = operation_deadline
                _download(root, directory, plan, state, client, response, config)
            elif remote_status == "cancelled":
                execution.update(status="cancelled", remote_status=remote_status, completed_at=time.time())
            else:
                raise _TransportError("unknown_response_status")
        if execution["status"] not in _PENDING and execution.get("container_id"):
            stage = "cleanup"
            client.deadline = operation_deadline
            try:
                client.json("DELETE", f"/containers/{execution['container_id']}")
                execution["container_deleted"] = True
            except _TransportError:
                execution["container_deleted"] = False
    except _TransportError as exc:
        if stage == "poll_response" and expired(execution["deadline_at"], wall=True):
            client.deadline = operation_deadline
            try:
                response = _cancel(root, directory, plan, state, client)
                if response is not None and response.get("status") in {"completed", "incomplete", "failed"}:
                    _download(root, directory, plan, state, client, response, config)
                return _persist(root, directory, plan, state)
            except _TransportError:
                execution.update(status="remote_unknown", reason="deadline_cancellation_unconfirmed")
                return _persist(root, directory, plan, state)
        if exc.details.get("http_status") in {404, 410} and stage in {"download", "resume", "poll_response"}:
            execution["status"] = "expired"
        elif stage == "download":
            execution["status"] = "download_pending"
        elif execution.get("response_id") or exc.uncertain or stage in {"create_container", "submit_response"} and not exc.details.get("http_status"):
            execution["status"] = "remote_unknown"
        else:
            execution["status"] = "failed"
        execution.update(reason=exc.reason, last_stage=stage)
        if exc.details:
            execution["api_error"] = exc.details
    finally:
        client.close()
    return _persist(root, directory, plan, state)


def _run_experiment(run_dir, question, target_ref, code, request_id,
                   parameters=None, input_files=None, attempt_ref=None) -> dict:
    """Execute once, or recover the matching request; never rewrite user config."""
    root = Path(run_dir).resolve()
    settings = _context.get().read_settings()
    config = settings["experiment"]
    if not isinstance(request_id, str) or not request_id or len(request_id) > settings["limits"]["request_id_max_chars"]:
        raise ExperimentError("request_id must be a nonempty bounded string")
    if not isinstance(question, str) or not question.strip() or not isinstance(code, str) or not code.strip():
        raise ExperimentError("question and code must be nonempty strings")
    if parameters is None:
        parameters = {}
    if not isinstance(parameters, dict):
        raise ExperimentError("parameters must be a JSON object")
    if input_files is None:
        input_files = []
    if not isinstance(input_files, list) or any(not isinstance(item, str) for item in input_files) or len(set(input_files)) != len(input_files):
        raise ExperimentError("input_files must be distinct task-relative file paths")
    target_ref = _fixed_ref(target_ref, "target_ref")
    if attempt_ref is not None:
        attempt_ref = _fixed_ref(attempt_ref, "attempt_ref")
        if attempt_ref["kind"] != "attempts":
            raise ExperimentError("attempt_ref must reference an attempt")
    inputs = []
    input_data = {}
    for path in input_files:
        file = _input_path(root, path)
        with file.open("rb") as stream:
            data = stream.read(config["artifact_max_bytes"] + 1)
        if len(data) > config["artifact_max_bytes"]:
            raise ExperimentError("Input file exceeds artifact_max_bytes")
        inputs.append({"path": path, "size": len(data)})
        input_data[path] = data
    arguments = {"question": question, "target_ref": target_ref, 
                 "parameters": parameters, "input_files": inputs, "attempt_ref": attempt_ref}
    try:
        encoded = _json({**arguments, "code": code, "request_id": request_id})
    except (TypeError, ValueError):
        raise ExperimentError("Experiment inputs must be finite JSON data") from None
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key and key.encode() in encoded:
        raise ExperimentError("Experiment inputs must not contain API credentials")
    # Parent grants contain immutable plan artifacts but no task-owned state.
    # Salt new identifiers by task; find an existing owned request first so a
    # moved workspace can still recover its original identifier.
    experiment_id = "exp-" + uuid4().hex[:24]
    with _operation(root) as experiments:
        prior = [path for path in experiments.glob("exp-*/plan.json")
                 if (path.parent / "state.json").is_file()]
        matches = [path for path in prior if _read(path).get("request_id") == request_id]
        if len(matches) > 1:
            raise ExperimentError("Multiple owned experiments have this request_id")
        if matches:
            experiment_id = matches[0].parent.name
        directory = _safe_file(root, "experiments/" + experiment_id, must_exist=False)
        if directory.exists():
            if not (directory / "state.json").is_file():
                raise ExperimentError("Experiment evidence is read-only or its local initialization is incomplete")
            plan = _read(directory / "plan.json")
            if (not json_equal(plan["arguments"], arguments) or (directory / "requested_code.py").read_text(encoding="utf-8") != code
                    or any(_safe_file(root, item["saved_path"]).read_bytes() != input_data[item["path"]]
                           for item in plan["input_files"])):
                raise ExperimentError("request_id already exists with different inputs")
            return _continue(root, directory, plan, _read(directory / "state.json"))
        if not config["enabled"]:
            raise ExperimentError("Hosted experiments are disabled for new runs")
        _key()
        from colombo.cell.restart_budget import effective_limit
        if len(prior) >= effective_limit(root, "experiment_hosted", config["max_runs"]):
            raise ExperimentError("This task has reached experiment.max_runs")
        for existing in prior:
            status = _read(existing.parent / "state.json")["execution"]["status"]
            if status in {"preparing", "submitted", "running", "remote_unknown"}:
                raise ExperimentError("Resume the unfinished experiment before starting another")
        window = _window(config, _context.get().deadline("work"))
        from colombo.shared.runtime_budget import get_budget_context
        local_reserve = 0 if get_budget_context(root) is not None else config["download_reserve_seconds"]
        if window <= local_reserve:
            raise ExperimentError("Insufficient parent work budget for an experiment and result download")
        started = time.time()
        directory.mkdir()
        prefix = "experiments/" + experiment_id + "/"
        copied_inputs = [{**item, "saved_path": prefix + f"inputs/input_{index}.bin",
                          "upload_name": experiment_id + f"-input-{index}.bin"} for index, item in enumerate(inputs)]
        plan = {**arguments, "input_files": copied_inputs, "experiment_id": experiment_id,
                "request_id": request_id, "arguments": arguments, "code_file": prefix + "requested_code.py", "nonce": uuid4().hex,
                "settings_snapshot": {"experiment": deepcopy(config), "network": deepcopy(settings["network"])}}
        state = {"execution": {"status": "preparing", "backend": "openai_code_interpreter",
                                "model": config["model"], "started_at": started,
                                "deadline_at": None if window == float("inf") else started + window - local_reserve,
                                "total_deadline_at": None if window == float("inf") else started + window,
                                "artifact_limits": {key: config[key] for key in
                                                    ("artifact_max_bytes", "max_total_artifact_bytes", "max_files")}}, "artifacts": []}
        # Charging the persisted plan happens before any API operation.
        _save(directory / "plan.json", plan)
        _save(directory / "state.json", state)
        try:
            _artifact(root, state, prefix + "plan.json", _json(plan), config)
            _artifact(root, state, prefix + "requested_code.py", code.encode(), config)
            for item in copied_inputs:
                data = input_data[item["path"]]
                _artifact(root, state, item["saved_path"], data, config)
        except _TransportError as exc:
            state["execution"].update(status="failed", reason=exc.reason)
            return _persist(root, directory, plan, state)
        _persist(root, directory, plan, state)
        return _continue(root, directory, plan, state, submit=True)


def _resume_experiment(run_dir, experiment_id) -> dict:
    """Poll/download the original response; execution deadline and quota persist."""
    root = Path(run_dir).resolve()
    if not isinstance(experiment_id, str) or not re.fullmatch(r"exp-[0-9a-f]{24}", experiment_id):
        raise ExperimentError("Invalid experiment_id")
    with _operation(root):
        directory = _safe_file(root, "experiments/" + experiment_id, must_exist=False)
        if not directory.is_dir():
            raise ExperimentError("Experiment does not exist in this task")
        if not (directory / "state.json").is_file():
            raise ExperimentError("Inherited experiment evidence is read-only; resume it in its owning task")
        return _continue(root, directory, _read(directory / "plan.json"), _read(directory / "state.json"))


def run_experiment(run_dir, question, target_ref, code, request_id,
                   parameters=None, input_files=None, attempt_ref=None, *, context: ExperimentContext) -> dict:
    """Execute under caller-supplied task context without changing MCP payloads."""
    token = _context.set(context)
    try:
        return _run_experiment(run_dir, question, target_ref, code, request_id,
                               parameters=parameters, input_files=input_files, attempt_ref=attempt_ref)
    finally:
        _context.reset(token)


def resume_experiment(run_dir, experiment_id, *, context: ExperimentContext) -> dict:
    """Recover the original operation with explicit record and deadline access."""
    token = _context.set(context)
    try:
        return _resume_experiment(run_dir, experiment_id)
    finally:
        _context.reset(token)
