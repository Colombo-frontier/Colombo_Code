"""Durable, batch-level adapter for the Cell colombo.cell.runner."""
from __future__ import annotations

import math
import hashlib
import os
import re
import subprocess
import sys
import threading
import time
import uuid

from colombo.shared.file_io import Path, file_lock, freeze_json, json_equal, read_json, write_json
from colombo.shared.process_control import execution_scope, process_identity, process_matches, spawn_options, load_stop_request, complete_stop_request
from colombo.shared.runtime_budget import cell_operational, operational


_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}\Z")


class CellWaitCancelled(InterruptedError):
    """The controller stopped waiting; the durable supervisor is unaffected."""


def _check_cancelled(event) -> None:
    if event is not None and event.is_set():
        raise CellWaitCancelled("Controller cancelled its wait; reconcile this same Cell attempt to recover")


def _poll_pause(event, seconds=0.2) -> None:
    if event is None:
        time.sleep(seconds)
    elif event.wait(seconds):
        _check_cancelled(event)


def _safe_id(value: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value) or ".." in value:
        raise ValueError("Invalid attempt id")
    return value


def _tree_manifest(root: Path) -> list[dict]:
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Package must be an ordinary directory")
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError("Package symlinks are not permitted")
        if path.is_file():
            rows.append({"path": path.relative_to(root).as_posix(), "size": path.stat().st_size,
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    if not rows or not (root / "manifest.json").is_file():
        raise ValueError("Package requires a manifest")
    return rows


def _required_review_files(package: Path) -> list[str]:
    """Carry explicitly required supplied materials into the Cell review."""
    manifest = read_json(package / "manifest.json")
    names = ["README.md", "manifest.json"]
    names.extend(name for name in ("setting.json", "bracket_snapshot.json") if (package / name).is_file())
    for item in manifest.get("items", []):
        if item.get("importance") == "required":
            names.append(item["record_path"])
            names.extend(artifact["package_path"] for artifact in item.get("artifacts", []))
    result = []
    for name in names:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Required review material must have an explicit path")
        relative = Path(name.replace("\\", "/"))
        source = package / relative
        if (relative.is_absolute() or relative.drive or ".." in relative.parts or source.is_symlink()
                or not source.resolve().is_relative_to(package) or not source.is_file()):
            raise ValueError("Required review material is missing or outside its package")
        delivered = "inputs/package/" + relative.as_posix()
        if delivered not in result:
            result.append(delivered)
    return result


class CellAdapter:
    def __init__(self, project_root: Path, config: dict):
        self.project_root = Path(project_root).resolve()
        self.config = dict(config.get("cell", {}))
        self.runtime = config.get("runtime", {})
        self.prepare_timeout = operational(config, "cell_prepare_timeout_seconds", 90)
        self.lock_timeout = cell_operational(config, "task_lock_timeout_seconds", 30)
        self.lock_poll = cell_operational(config, "lock_poll_seconds", 0.05)
        self.process_poll = cell_operational(config, "process_poll_seconds", 0.2)
        self.terminate_wait = cell_operational(config, "terminate_wait_seconds", 3)
        self.startup_wait = operational(config, "cell_launch_grace_seconds", 15)
        self.python = self.config.get("python") or sys.executable
        self.worker = self.project_root / "src/colombo/cell/worker.py"
        if not (self.project_root / "src/colombo/cell/controller.py").is_file():
            raise ValueError("The Cell runtime is missing")

    def _env(self, root=None) -> dict:
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        if root is not None:
            from colombo.shared.runtime_budget import environment
            env.update(environment(root))
        if self.config.get("codex_bin"):
            env["CELL_CODEX_BIN"] = str(self.config["codex_bin"])
        if self.config.get("auth_home"):
            env["CELL_AUTH_HOME"] = str(self.config["auth_home"])
        # Static catalogs are an explicit run option, not an ambient host default.
        env.pop("CELL_MODEL_CATALOG_JSON", None)
        if self.config.get("model_catalog_json"):
            source = Path(self.config["model_catalog_json"]).expanduser()
            if not source.is_absolute():
                source = self.project_root / source
            env["CELL_MODEL_CATALOG_JSON"] = str(source.absolute())
        return env

    def _lock(self, path):
        return file_lock(path, timeout=self.lock_timeout, poll_seconds=self.lock_poll)

    def prepare(self, task_dir: Path, assignment: dict, package_dir: Path, *,
                assignment_ref: dict, package_ref: dict) -> None:
        task_dir, package_dir = Path(task_dir).resolve(), Path(package_dir).resolve()
        problem = task_dir / "input/problem.md"
        if not problem.is_file() or problem.is_symlink():
            raise ValueError("Task input/problem.md is required")
        if not package_dir.is_relative_to(task_dir):
            raise ValueError("Task package must reside in its task directory")
        from colombo.cell.instructions import validate_specialization
        research_mode = assignment.get("research_mode", "generic")
        specialization = assignment.get("spec", assignment).get("specialization", "general")
        validate_specialization(research_mode, specialization)
        base = {"storage_version": 3, "task_id": task_dir.name,
                "research_mode": research_mode, "specialization": specialization,
                "assignment_ref": assignment_ref, "package_ref": package_ref,
                "task_dir": str(task_dir), "project_root": str(self.project_root),
                "package_dir": str(package_dir), "config": self.config, "assignment": assignment,
                "required_review_files": _required_review_files(package_dir)}
        execution_scope({**base, "attempt_id": "prepare"})
        with self._lock(task_dir / ".prepare.lock"):
            path, prepared = task_dir / "prepare_request.json", task_dir / "prepared.json"
            if path.exists():
                request = read_json(path)
                identity_keys = set(base) - {"config"}
                if not json_equal({key: request.get(key) for key in identity_keys},
                                  {key: base[key] for key in identity_keys}):
                    raise ValueError("Prepared task input differs; create a new task")
            else:
                request = {**base, "package_files": _tree_manifest(package_dir)}
                freeze_json(path, request)
            if prepared.exists():
                saved = read_json(prepared)
                if type(saved.get("storage_version")) is not int or saved["storage_version"] != 3 or any(
                        not json_equal(saved.get(key), base[key])
                        for key in ("task_id", "assignment_ref", "package_ref")):
                    raise ValueError("Prepared task scope differs")
                from colombo.cell.instructions import INSTRUCTION_VERSION
                expected_mode = {"research_mode": research_mode, "specialization": specialization,
                                 "instruction_version": INSTRUCTION_VERSION}
                if any(saved.get(key, {"research_mode": "generic", "specialization": "general",
                                       "instruction_version": INSTRUCTION_VERSION}[key]) != value
                       for key, value in expected_mode.items()):
                    raise ValueError("Prepared Cell mode differs from its request")
                cell_config = read_json(task_dir / "cell/run.json")
                if not json_equal(cell_config.get("cell_mode"), expected_mode):
                    raise ValueError("Frozen Cell mode differs from run configuration")
                if not json_equal(cell_config.get("required_review_files", []),
                                  base["required_review_files"]):
                    raise ValueError("Prepared task review inputs differ")
                return
            from colombo.shared import runtime_budget as shared_budget
            prepare_timeout = self.prepare_timeout
            available = shared_budget.remaining(shared_budget.deadline(task_dir, work=True))
            if available is not None:
                prepare_timeout = min(prepare_timeout, available)
            completed = subprocess.run([self.python, "-B", str(self.worker), "prepare", "--request", str(path)],
                                       cwd=str(self.project_root), env=self._env(task_dir), capture_output=True,
                                       text=True, encoding="utf-8", timeout=prepare_timeout, **spawn_options())
            if completed.returncode or not prepared.exists():
                raise RuntimeError("Cell preparation failed: " + (completed.stderr or completed.stdout)[-4000:])

    def _attempt_dir(self, task_dir: Path, attempt_id: str) -> Path:
        return Path(task_dir).resolve() / "attempts" / _safe_id(attempt_id)

    def _unknown(self, task_dir: Path, attempt_id: str, reason: str) -> dict:
        return {"execution_status": "unknown", "accepted": False, "review_status": "unknown",
                "scientific_outcome": None, "summary": "Execution outcome needs reconciliation.",
                "stop_reason": reason, "artifacts": [], "run_dir": str(task_dir / "cell"),
                **execution_scope(self._stop_scope(task_dir, attempt_id))}

    def _stop_scope(self, task_dir, attempt_id):
        prepared = read_json(task_dir / "prepared.json")
        if type(prepared.get("storage_version")) is not int or prepared["storage_version"] != 3:
            raise ValueError("Unsupported prepared task storage version")
        if prepared.get("task_id") != task_dir.name:
            raise ValueError("Prepared task identity differs from its directory")
        return {"task_dir": str(task_dir), "attempt_id": attempt_id,
                **{key: prepared[key] for key in ("task_id", "assignment_ref", "package_ref")}}

    def _cancel_unstarted(self, task_dir, attempt_id, stop):
        """Caller holds dispatch/launch locks; never snapshots a possibly active older Cell."""
        folder = self._attempt_dir(task_dir, attempt_id)
        if (folder / "launch.json").exists():
            raise ValueError("Cannot treat a launched attempt as never started")
        result = {"execution_status": "cancelled", "accepted": False, "review_status": "not_started",
                  "scientific_outcome": None, "summary": "Pruned before this Cell attempt was started.",
                  "stop_reason": "pruned", "started": False, "artifacts": [],
                  "run_dir": str(task_dir / "cell"), **execution_scope(stop),
                  "stop_request": stop, "export_errors": []}
        result_path = task_dir / "results" / attempt_id / "result.json"
        freeze_json(result_path, result)
        complete_stop_request(folder, stop, result_path, result)
        return result

    def request_stop(self, task_dir: Path, attempt_id: str, decision_ref, request_id: str) -> dict:
        """Persist a reviewed stop request. Supervisor owns actual process-tree termination."""
        task_dir = Path(task_dir).resolve()
        folder = self._attempt_dir(task_dir, attempt_id)
        scope = self._stop_scope(task_dir, attempt_id)
        proposed = {"schema_version": 2, **execution_scope(scope), "decision_ref": decision_ref,
                    "request_id": request_id}
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("Stop request_id must be nonempty")
        if not ((isinstance(decision_ref, str) and decision_ref.strip()) or
                (isinstance(decision_ref, dict) and isinstance(decision_ref.get("id"), str) and decision_ref["id"].strip())):
            raise ValueError("A reviewed decision reference is required")
        folder.mkdir(parents=True, exist_ok=True)
        with self._lock(task_dir / ".dispatch.lock"), self._lock(folder / ".launch.lock"):
            stop = load_stop_request(folder, scope)
            if stop is not None and stop["request_id"] == request_id and not json_equal(stop, proposed):
                raise ValueError("Stop request ID was reused with different content")
            if stop is None:
                freeze_json(folder / "stop_request.json", proposed)
                stop = proposed
            if not (folder / "receipt.json").exists() and not (folder / "launch.json").exists():
                self._cancel_unstarted(task_dir, attempt_id, stop)
        result = self.reconcile(task_dir, attempt_id)
        status = ("requested" if result is None or result["execution_status"] == "unknown" else
                  "cancelled" if result["execution_status"] == "cancelled" else "already_completed")
        return {"status": status, "stop_request": stop}

    def _read_receipt(self, task_dir: Path, attempt_id: str, folder: Path) -> dict | None:
        """Read a completed attempt through the same binding and artifact checks."""
        receipt_path, request_path = folder / "receipt.json", folder / "request.json"
        if receipt_path.exists():
            receipt = read_json(receipt_path)
            if not request_path.exists():
                raise ValueError("Attempt receipt has no saved request")
            request = read_json(request_path)
            scope = execution_scope(self._stop_scope(task_dir, attempt_id))
            if not json_equal(execution_scope(request), scope) or not json_equal(execution_scope(receipt), scope):
                raise ValueError("Attempt receipt is not bound to its request and current task scope")
            if receipt.get("result_path") != f"results/{attempt_id}/result.json":
                raise ValueError("Receipt must name this attempt canonical result")
            result_path = task_dir / receipt["result_path"]
            if not result_path.resolve().is_relative_to(task_dir) or result_path.is_symlink():
                raise ValueError("Result receipt path escapes task")
            result = read_json(result_path)
            if not json_equal(execution_scope(result), scope):
                raise ValueError("Result belongs to another task or attempt")
            for artifact in result.get("artifacts", []):
                path = task_dir / artifact["path"]
                if not path.resolve().is_relative_to(task_dir) or path.is_symlink() or not path.is_file():
                    raise ValueError("Missing or invalid artifact path")
            stop = load_stop_request(folder, read_json(request_path))
            if stop is not None:
                complete_stop_request(folder, stop, result_path, result)
            return result
        return None

    def _receipt_or_unknown(self, task_dir: Path, attempt_id: str, folder: Path, reason: str) -> dict:
        # The supervisor may publish its receipt and exit after our first read
        # but before process identity is checked. Prefer its validated result;
        # absence or uncertainty still never authorizes a replacement worker.
        result = self._read_receipt(task_dir, attempt_id, folder)
        return result if result is not None else self._unknown(task_dir, attempt_id, reason)

    def reconcile(self, task_dir: Path, attempt_id: str) -> dict | None:
        task_dir = Path(task_dir).resolve()
        folder = self._attempt_dir(task_dir, attempt_id)
        result = self._read_receipt(task_dir, attempt_id, folder)
        if result is not None:
            return result
        launch_path = folder / "launch.json"
        if not launch_path.exists():
            if (folder / "stop_request.json").exists():
                with self._lock(task_dir / ".dispatch.lock"), self._lock(folder / ".launch.lock"):
                    if not launch_path.exists():
                        stop = load_stop_request(folder, self._stop_scope(task_dir, attempt_id))
                        return self._cancel_unstarted(task_dir, attempt_id, stop)
                return self.reconcile(task_dir, attempt_id)
            return None
        launch = read_json(launch_path)
        worker_path = folder / "worker.json"
        identity = None
        if worker_path.exists():
            worker = read_json(worker_path)
            if worker.get("nonce") != launch.get("nonce"):
                return self._receipt_or_unknown(task_dir, attempt_id, folder, "Worker identity nonce mismatch")
            identity = worker.get("identity")
        if not identity:
            identity = launch.get("identity")
        if identity:
            matches = process_matches(identity)
            if matches is True:
                return None
            return self._receipt_or_unknown(task_dir, attempt_id, folder,
                                 "Worker is absent or cannot be identified; no final receipt exists")
        if time.time() - launch["created_at"] < self.startup_wait:
            return None
        return self._receipt_or_unknown(task_dir, attempt_id, folder,
                             "Launch intent has no confirmed process identity; automatic relaunch is forbidden")

    def run(self, task_dir: Path, attempt_id: str, resume: bool = False, cancel_event=None, *, restart=False) -> dict:
        """Launch/rejoin one durable attempt; cancellation only detaches the waiter."""
        _check_cancelled(cancel_event)
        task_dir = Path(task_dir).resolve()
        scope = self._stop_scope(task_dir, attempt_id)
        folder = self._attempt_dir(task_dir, attempt_id)
        folder.mkdir(parents=True, exist_ok=True)
        request = {"task_dir": str(task_dir), "project_root": str(self.project_root),
                   **execution_scope(scope), "resume": bool(resume), "config": self.config}
        if restart:
            if not resume:
                raise ValueError("Restart must retain the existing Task workspace")
            request["restart"] = True
        timeout = self.config["run_timeout_seconds"]
        if timeout != "unlimited" and (type(timeout) is not int or timeout <= 0):
            raise ValueError('Cell run_timeout_seconds must be positive seconds or "unlimited"')
        spawned = None
        with self._lock(task_dir / ".dispatch.lock"), self._lock(folder / ".launch.lock"):
            _check_cancelled(cancel_event)
            stop = load_stop_request(folder, request)
            if stop is not None and not (folder / "launch.json").exists() and not (folder / "receipt.json").exists():
                return self._cancel_unstarted(task_dir, attempt_id, stop)
            request_path = folder / "request.json"
            freeze_json(request_path, request)
            if not (folder / "launch.json").exists() and not (folder / "receipt.json").exists():
                settled = []
                for sibling in sorted(folder.parent.iterdir()):
                    if sibling == folder or not (sibling / "launch.json").exists():
                        continue
                    prior = self.reconcile(task_dir, sibling.name)
                    if prior is None or prior.get("execution_status") == "unknown":
                        raise RuntimeError(f"Prior attempt {sibling.name} is active or unresolved")
                    settled.append(prior)
                if resume and not restart:
                    from colombo.brain.resume_eligibility import result_resume_eligibility
                    eligibility = result_resume_eligibility(settled[-1] if settled else None, self.config)
                    if eligibility["status"] != "allowed":
                        raise ValueError("Resume cannot start: " + eligibility["reason"]
                            + " Use an explicit planned restart only after reconciliation; "
                            "this committed dispatch is retained.")
                _check_cancelled(cancel_event)
                # Persist uncertainty before Popen. A crash in the following gap never permits blind replay.
                # Once this intent exists, finish launching before observing
                # cancellation so a normal detach does not strand an unknown intent.
                launch = {"nonce": uuid.uuid4().hex, "created_at": time.time(),
                          "state": "launching", "identity": None}
                write_json(folder / "launch.json", launch)
                try:
                    with (folder / "supervisor.log").open("ab") as stream:
                        process = subprocess.Popen(
                            [self.python, "-B", str(self.worker), "supervise", "--request", str(request_path)],
                            cwd=str(self.project_root), env=self._env(task_dir), stdin=subprocess.DEVNULL,
                            stdout=stream, stderr=subprocess.STDOUT, **spawn_options())
                    spawned = process
                    launch["identity"] = process_identity(process.pid)
                    launch["state"] = "started"
                    write_json(folder / "launch.json", launch)
                except Exception as exc:
                    # Popen may have succeeded; preserve an unknown outcome rather than assuming not executed.
                    launch["error"] = f"{type(exc).__name__}: {exc}"
                    write_json(folder / "launch.json", launch)
                    return self._unknown(task_dir, attempt_id, launch["error"])
        try:
            while True:
                _check_cancelled(cancel_event)
                result = self.reconcile(task_dir, attempt_id)
                if result is not None:
                    if spawned is not None and result["execution_status"] != "unknown":
                        deadline = time.monotonic() + self.terminate_wait
                        while spawned.poll() is None and time.monotonic() < deadline:
                            _poll_pause(cancel_event, self.process_poll)
                    return result
                _poll_pause(cancel_event, self.process_poll)
        except CellWaitCancelled:
            if spawned is not None and spawned.poll() is None:
                # Keep the process handle alive and reap eventual exit without
                # blocking controller shutdown or terminating the supervisor.
                threading.Thread(target=spawned.wait, name="cell-supervisor-reaper", daemon=True).start()
            raise
