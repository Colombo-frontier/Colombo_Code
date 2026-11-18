"""Local task processes with explicit context snapshots and cooperative isolation.

Directories and MCP scope are not operating-system access control. Child records
are returned as candidates; this module never imports their review authority.
"""

from __future__ import annotations

from contextlib import contextmanager, ExitStack
import copy
from datetime import datetime
from datetime import timezone
import json
import os
from colombo.project_paths import PROJECT_ROOT
from colombo.shared.file_io import Path, file_lock
from colombo.shared.file_io import atomic_write
import re
import shutil
import subprocess
import sys
import time
from uuid import uuid4

from colombo.cell.record_store import Store
from colombo.cell.record_store import json_equal
from colombo.cell.research_records import map_record_references
from colombo.cell.research_records import record_references
from colombo.shared.experiment_artifacts import read_artifact_groups
from colombo.shared.experiment_artifacts import experiment_group
from colombo.shared.experiment_artifacts import copy_artifacts
from colombo.shared.experiment_artifacts import manifest_for
from colombo.cell.settings import get_settings
from colombo.cell.settings import merge_settings
from colombo.cell.settings import run_fields


ACTIVE = {"starting", "running", "cancel_requested"}
TERMINAL = {"completed", "cancelled", "budget_exhausted", "incomplete", "failed"}
MEMORY_KINDS = ("claims", "arguments", "examples", "attempts", "sources",
                "proof_state", "experiment_result", "reviews", "events")
RESEARCH_KINDS = MEMORY_KINDS[:-2]
IMPORT_KINDS = frozenset(RESEARCH_KINDS) - {"proof_state"}
_TASK_ID = re.compile(r"[a-f0-9]{32}\Z")


class TaskError(ValueError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value) -> None:
    content = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False, default=str) + "\n"
    atomic_write(path, content.encode("utf-8"))


@contextmanager
def _tasks_lock(tasks_dir: Path):
    runtime = get_settings(tasks_dir.parent)["runtime"]
    with ExitStack() as stack:
        try:
            stack.enter_context(file_lock(tasks_dir / ".lock", runtime["task_lock_timeout_seconds"],
                                          runtime["lock_poll_seconds"]))
        except TimeoutError:
            raise TimeoutError("Timed out waiting for task registry") from None
        yield


def _ref(record: dict) -> dict:
    return {key: record[key] for key in ("kind", "id", "revision")}


def _key(ref: dict) -> tuple:
    return ref["kind"], ref["id"], ref["revision"]


def _task_view(task: dict) -> dict:
    """Present legacy process metadata using the current role name."""
    result = dict(task)
    if "worker_pid" in result:
        result.setdefault("subcell_pid", result.pop("worker_pid"))
    return result


class Tasks:
    def __init__(self, run_dir: Path):
        self.run_dir = Path(run_dir).resolve()
        self.tasks_dir = self.run_dir / "tasks"
        self.store = Store(self.run_dir / "memory")

    def _config(self) -> dict:
        config = _read_json(self.run_dir / "run.json", {})
        if not isinstance(config, dict):
            raise TaskError("run.json must contain an object")
        settings = get_settings(self.run_dir)
        config.update(run_fields(settings), settings=settings)
        depth = config.get("task_depth", 0)
        if type(depth) is not int or depth < 0:
            raise TaskError("task_depth must be an integer >= 0")
        config["task_depth"] = depth
        return config

    def _task_dir(self, task_id: str) -> Path:
        if not isinstance(task_id, str) or not _TASK_ID.fullmatch(task_id):
            raise TaskError("Invalid task_id")
        path = self.tasks_dir / task_id
        if path.is_symlink() or path.resolve().parent != self.tasks_dir.resolve():
            raise TaskError("Task directory is outside this run")
        if not (path / "task.json").is_file():
            raise KeyError(f"Unknown task: {task_id}")
        return path

    def _all(self) -> list[dict]:
        if not self.tasks_dir.exists():
            return []
        return [_task_view(_read_json(path / "task.json")) for path in sorted(self.tasks_dir.iterdir())
                if _TASK_ID.fullmatch(path.name) and not path.is_symlink()
                and (path / "task.json").is_file()]

    def _resolve(self, ref: dict) -> dict:
        if (not isinstance(ref, dict) or not {"kind", "id", "revision"} <= ref.keys()
                or set(ref) - {"kind", "id", "revision", "property_ids", "position"}
                or type(ref["revision"]) is not int or ref["revision"] < 1):
            raise TaskError("Record references require kind, id and a pinned positive revision")
        # Snapshot serialization needs the original record envelope; public
        # readers receive the selected-property view instead.
        record = self.store.get(ref["kind"], ref["id"], ref.get("revision"), project=False)
        if record.get("read_only") and "property_ids" in record:
            requested = ref.get("property_ids", record["property_ids"])
            if not isinstance(requested, list) or any(not isinstance(item, str) for item in requested) or not set(requested) <= set(record["property_ids"]):
                raise TaskError("Requested properties exceed the granted context")
        if "property_ids" in ref:
            record = self.store.resolve_record_refs([{**_ref(record),
                                                     "property_ids": ref["property_ids"]}], project=False)[0]
        return record

    @staticmethod
    def _snapshot_ref(record: dict) -> dict:
        result = _ref(record)
        if "property_ids" in record:
            result["property_ids"] = record["property_ids"]
        return result

    def _snapshot_changes(self, task: dict) -> list[dict]:
        """Compare a finite grant with current parent support, not latest versions."""
        changes = []
        frozen = Store(self._task_dir(task["task_id"]) / "workspace" / "memory")
        for ref in task.get("snapshot_refs", []):
            try:
                current = self._resolve(ref)
                trust = current["current_trust"]
                original = frozen._context.get(_key(ref), {}).get("current_trust", {})
                if json_equal(original, trust):
                    continue
                if current["kind"] == "examples":
                    ids = ref.get("property_ids", list(trust["properties"]))
                    bad = [p for p in ids if trust["properties"][p]["state"] in {"withdrawn", "suspended", "dependency_blocked"}]
                    if bad:
                        changes.append({"ref": ref, "property_ids": bad, "current_trust": trust})
                elif trust["state"] in {"withdrawn", "suspended", "dependency_blocked", "conflicted"} or (
                        current["kind"] == "claims" and original.get("state") in {"proved", "refuted"}
                        and trust["state"] != original.get("state")):
                    changes.append({"ref": ref, "current_trust": trust})
            except (KeyError, ValueError) as exc:
                changes.append({"ref": ref, "reason": f"Cannot validate parent support: {exc}"})
        return changes

    def spawn_task(self, target_ref: dict, instructions: str,
                   context_refs: list[dict] | None = None, group_id: str = "",
                   search_enabled: bool | None = None,
                   settings_overrides: dict | None = None) -> dict:
        if not isinstance(instructions, str) or not instructions.strip():
            raise TaskError("instructions must be a nonempty string")
        if context_refs is not None and not isinstance(context_refs, list):
            raise TaskError("context_refs must be a list")
        if search_enabled is not None and type(search_enabled) is not bool:
            raise TaskError("search_enabled must be true, false or omitted")
        config = self._config()
        from colombo.cell.instructions import read_cell_mode
        from colombo.cell.instructions import validate_mode
        from colombo.cell.instructions import install_cell_pack
        # A helper's mathematical task is general unless Brain assigns a separate
        # specialized Cell. Inherit programme scope, never the parent skill pack.
        child_mode = validate_mode(read_cell_mode(self.run_dir)["research_mode"], "general")
        from colombo.cell.settings import reject_budget_overrides
        reject_budget_overrides(settings_overrides)
        child_settings = merge_settings(config["settings"], settings_overrides)
        from colombo.cell.recovery import caller_deadline
        parent_deadline = caller_deadline(self.run_dir)
        if parent_deadline is not None and parent_deadline <= time.monotonic():
            raise TaskError("No parent work budget remains for a Subcell")
        parent_deadline_unix = (None if parent_deadline is None
                                else time.time() + max(0.0, parent_deadline - time.monotonic()))
        # A parent's current search override belongs to that task only. A new
        # subcell starts from its role default unless explicitly overridden.
        child_search = (child_settings["network"]["subcell_search_enabled"]
                        if search_enabled is None else search_enabled)
        group_limit = config["settings"]["limits"]["group_id_max_chars"]
        if not isinstance(group_id, str) or len(group_id) > group_limit:
            raise TaskError(f"group_id must be a string of at most {group_limit} characters")
        if config["task_depth"] >= config["task_max_depth"]:
            raise TaskError("Maximum task depth reached")
        target = self._resolve(target_ref)
        granted = [target] + [self._resolve(ref) for ref in (context_refs or [])]
        snapshot = {}
        def grant(record):
            key = _key(record)
            if key not in snapshot:
                snapshot[key] = record
                return True
            previous = snapshot[key]
            before = copy.deepcopy(previous.get("property_ids"))
            if "property_ids" not in record:
                previous.pop("property_ids", None)
            elif "property_ids" in previous:
                previous["property_ids"] = sorted(set(previous["property_ids"]) | set(record["property_ids"]))
            return before != previous.get("property_ids")
        for record in granted:
            grant(record)
        dependency_depth = config["settings"]["parallel"]["context_dependency_depth"]
        frontier = list(snapshot.values())
        for _ in range(dependency_depth):
            following = []
            for record in frontier:
                payload = copy.deepcopy(record["payload"])
                if record["kind"] == "examples":
                    payload["properties"] = [prop for prop in payload.get("properties", [])
                                             if "property_ids" not in record or prop["id"] in record["property_ids"]]
                for link in record_references(payload, roles={"dependency", "target", "subject", "source", "definition"}):
                    resolved = self._resolve(link["ref"])
                    if grant(resolved):
                        following.append(resolved)
            frontier = following
            if not frontier:
                break
        scope = {"target_ref": _ref(target)}
        artifact_groups = [experiment_group(record["payload"]) for record in snapshot.values()
                           if record["kind"] == "experiment_result"]
        granted_files = read_artifact_groups(self.run_dir, artifact_groups, settings=child_settings)
        task_id = uuid4().hex
        task_dir = self.tasks_dir / task_id
        workspace = task_dir / "workspace"
        with _tasks_lock(self.tasks_dir):
            existing = self._all()
            if sum(task["status"] in ACTIVE for task in existing) >= config["task_max_concurrency"]:
                raise TaskError("Maximum concurrent task count reached")
            if group_id and any(task["group_id"] == group_id and task["scope"] != scope
                                for task in existing):
                raise TaskError("Competition group has a different target, version or content")
            workspace.mkdir(parents=True)
            (workspace / "memory").mkdir()
            context = workspace / "context"
            context.mkdir()
            copy_artifacts(workspace, granted_files)
            for kind in {record["kind"] for record in snapshot.values()}:
                _write_json(context / f"{kind}.json", {"schema_version": 2,
                            "records": [record for record in snapshot.values() if record["kind"] == kind]})
            _write_json(context / "manifest.json", {
                "target_ref": _ref(target), "scope": scope,
                "explicit_refs": list({_key(r): _ref(r) for r in granted}.values()),
                "snapshot_refs": [self._snapshot_ref(r) for r in snapshot.values()],
                "experiment_artifacts": manifest_for(granted_files),
                "dependency_depth": dependency_depth, "access": "read_only_by_convention",
            })
            target_description = copy.deepcopy(target["payload"])
            if target["kind"] == "examples" and "property_ids" in target:
                target_description["properties"] = [prop for prop in target_description.get("properties", [])
                                                     if prop["id"] in target["property_ids"]]
            problem = ("# Assigned mathematical target\n\n" +
                       json.dumps(target_description, ensure_ascii=False, indent=2) + "\n")
            (workspace / "problem.md").write_bytes(problem.encode("utf-8"))
            child_config = dict(run_fields(child_settings), settings=child_settings)
            if "profile" in config:
                child_config["profile"] = config["profile"]
            child_config.update({"task_depth": config["task_depth"] + 1,
                                 "task_id": task_id,
                                 "role": "subcell",
                                 "cell_mode": child_mode,
                                 "agent_options": {"search_enabled": child_search},
                                 "storage_version": 2})
            _write_json(workspace / "run.json", child_config)
            task_text = (f"# Subtask {task_id}\n\n{instructions}\n\n"
                         "See problem.md for the goal and conditions, and context/manifest.json for the authorized context.\n"
                         "Conduct research under the subcell rules in AGENTS.md and return task_result.md, listing the scope of the conclusions, "
                         "pinned version references for artifacts, remaining questions, and missing materials.\n")
            (workspace / "TASK.md").write_text(task_text, encoding="utf-8")
            install_cell_pack(workspace, child_mode)
            task = {"task_id": task_id, "group_id": group_id, "scope": scope,
                    "parent_deadline_unix": parent_deadline_unix,
                    "status": "starting", "created_at": _now(), "workspace": str(workspace),
                    "depth": child_config["task_depth"], "instructions": instructions, "cell_mode": child_mode,
                    "search_enabled_at_launch": child_search,
                    "settings_overrides": settings_overrides or {},
                    "snapshot_refs": [self._snapshot_ref(r) for r in snapshot.values()], "pid": None}
            _write_json(task_dir / "task.json", task)
        try:
            from colombo.shared.runtime_budget import budget_environment
            environment = dict(os.environ)
            environment.update(budget_environment(self.run_dir))
            with (task_dir / "subcell.log").open("ab") as log:
                # Windows CreateProcess can reject a long current directory
                # even when file I/O supports it. The helper receives its
                # absolute task directory and initializes that workspace itself.
                process = subprocess.Popen(
                    [sys.executable, str(Path(__file__).with_name("subcell_worker.py")),
                     "--task-dir", str(task_dir)], cwd=PROJECT_ROOT,
                    stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                    env=environment,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0,
                    shell=False)
            with _tasks_lock(self.tasks_dir):
                task = _read_json(task_dir / "task.json")
                task["pid"] = process.pid
                _write_json(task_dir / "task.json", task)
            return task
        except Exception as exc:
            with _tasks_lock(self.tasks_dir):
                task = _read_json(task_dir / "task.json")
                task.update(status="failed", ended_at=_now(), execution_error=str(exc))
                _write_json(task_dir / "task.json", task)
            raise TaskError(f"Could not start subcell: {exc}") from exc

    def task_status(self, task_id: str | None = None) -> dict:
        with _tasks_lock(self.tasks_dir):
            if task_id is not None:
                return _task_view(_read_json(self._task_dir(task_id) / "task.json"))
            tasks = self._all()
            return {"tasks": tasks, "count": len(tasks),
                    "active": sum(task["status"] in ACTIVE for task in tasks)}

    def cancel_task(self, task_id: str) -> dict:
        with _tasks_lock(self.tasks_dir):
            task_dir = self._task_dir(task_id)
            task = _read_json(task_dir / "task.json")
            if task["status"] not in TERMINAL:
                (task_dir / "cancel.flag").touch()
                task.update(status="cancel_requested", cancel_requested_at=_now())
                _write_json(task_dir / "task.json", task)
            return task

    def import_records(self, task_id: str, record_refs: list[dict], request_id: str) -> dict:
        self._task_dir(task_id)
        with _tasks_lock(self.tasks_dir):
            return self._import_records(task_id, record_refs, request_id)

    def _import_records(self, task_id: str, record_refs: list[dict], request_id: str) -> dict:
        """Copy an explicitly selected research graph as parent-local candidates.

        The ordinary records are one Store transaction. Referenced experiment
        execution records/files use their existing independent, idempotent
        service import; they are not claimed to be part of that transaction.
        """
        if not isinstance(record_refs, list) or not record_refs:
            raise TaskError("import_refs must be a nonempty list of fixed record references")
        maximum = self.store.settings["limits"]["request_id_max_chars"]
        if not isinstance(request_id, str) or not request_id or len(request_id) > maximum:
            raise TaskError("An import requires a nonempty request_id within the configured limit")
        task_dir = self._task_dir(task_id)
        child = Store(task_dir / "workspace" / "memory")
        rows = child.snapshot(include_context=True, with_trust=True)
        available = {_key(row): row for row in rows}
        imports_dir = task_dir / "imports"
        if imports_dir.is_symlink() or imports_dir.resolve() != imports_dir:
            raise TaskError("Import plans must stay in the ordinary task directory")
        request_input = {"record_refs": copy.deepcopy(record_refs)}
        saved_plan, plan_path = None, None
        for candidate in imports_dir.glob("*.json"):
            if candidate.is_symlink():
                raise TaskError("Import plans cannot be links")
            item = _read_json(candidate)
            if not isinstance(item, dict):
                raise TaskError("Invalid saved import plan")
            if item.get("request_id") == request_id:
                if saved_plan is not None:
                    raise TaskError("Repeated import request identity")
                saved_plan, plan_path = item, candidate
        if saved_plan is not None:
            if not json_equal(saved_plan["input"], request_input):
                raise TaskError("request_id was already used for different import_refs")
            operation = saved_plan["operation"]
        else:
            operation = "task-import-" + uuid4().hex
            plan_path = imports_dir / f"{operation}.json"
        seen, visiting, scopes = {}, set(), {}

        def resolve(ref):
            if (not isinstance(ref, dict) or not {"kind", "id", "revision"} <= ref.keys() or
                    ref["kind"] not in IMPORT_KINDS or not isinstance(ref["id"], str) or
                    type(ref["revision"]) is not int or ref["revision"] < 1):
                raise TaskError("Import references must pin a research record kind, id and revision")
            try:
                source = available[_key(ref)]
            except KeyError as exc:
                raise TaskError("Import reference is absent from the child and its granted context") from exc
            if "property_ids" in ref:
                selected = ref["property_ids"]
                actual = {prop["id"] for prop in source["payload"].get("properties", [])}
                allowed = set(source.get("property_ids", actual))
                if (source["kind"] != "examples" or not isinstance(selected, list) or not selected or
                        any(not isinstance(item, str) for item in selected) or
                        len(selected) != len(set(selected)) or not set(selected) <= allowed):
                    raise TaskError("Import property selection exceeds the child record or grant")
            return source

        def source_payload(source):
            payload = copy.deepcopy(source["payload"])
            if source["kind"] == "examples":
                payload["properties"] = [prop for prop in payload.get("properties", [])
                                         if prop["id"] in scopes[_key(source)]]
            return payload

        def preflight(ref, role="selected"):
            source = resolve(ref)
            key = _key(source)
            if key in visiting:
                raise TaskError("Cannot import a cyclic research record graph")
            if source["kind"] == "examples":
                selected = set(ref.get("property_ids", source.get("property_ids", [
                    prop["id"] for prop in source["payload"].get("properties", [])])))
                if key in seen and selected <= scopes[key]:
                    return
                scopes[key] = scopes.get(key, set()) | selected
            elif key in seen:
                return
            if key not in seen and len(seen) + len(visiting) >= self.store.settings["retrieval"]["max_memory_results"]:
                raise TaskError("Research result import exceeds max_memory_results")
            trust = source.get("current_trust", {})
            rejected = trust.get("state") in {"withdrawn", "suspended"}
            if source["kind"] == "examples":
                rejected = any(trust.get("properties", {}).get(identifier, {}).get("state") in {
                    "withdrawn", "suspended"} for identifier in scopes[key])
            if source["kind"] == "experiment_result" and trust.get("state") == "dependency_blocked":
                rejected = True
            if not source.get("read_only") and source["kind"] in {"arguments", "examples", "experiment_result"} and rejected:
                artifact_only = source["kind"] == "experiment_result" and trust.get("blockers") and all(
                    item.get("type") == "experiment_artifact" for item in trust["blockers"])
                if not artifact_only:
                    raise TaskError("Cannot import evidence whose child support is suspended, withdrawn or blocked")
            visiting.add(key)
            # A granted parent snapshot already has a parent identity. Do not
            # walk beyond this grant to rediscover its ungranted relations.
            if not source.get("read_only"):
                for link in record_references(source_payload(source)):
                    preflight(link["ref"], link["role"])
            visiting.remove(key)
            seen[key] = source

        for ref in record_refs:
            preflight(ref)

        def execute_plan(plan):
            batch = self.store.archive_result(plan["entries"], operation)

            def committed(ref):
                if "local_key" not in ref:
                    return ref
                return {**batch["refs"][ref["local_key"]],
                        **{key: value for key, value in ref.items() if key != "local_key"}}

            return {"record_refs": [committed(ref) for ref in plan["selected"]], "records": batch["records"],
                    "mapped_refs": [{"source": item["source"], "imported": committed(item["imported"])}
                                    for item in plan["mapped_refs"]],
                    "experiment_imports": plan["experiments"], "requires_parent_audit": True}

        if saved_plan is not None:
            # The frozen plan is reused even if the parent's current revision
            # changed after a successful commit. Store replays its exact receipt.
            return execute_plan(saved_plan)
        entries, mapped, experiments, local_keys = [], {}, [], {}

        def bring(ref, role="related"):
            source = resolve(ref)
            key = _key(source)
            if key not in mapped:
                original = _ref(source)
                local_key = local_keys.setdefault(key, f"r_{len(local_keys) + 1:04d}")
                if source.get("read_only"):
                    local = self._resolve(original)
                    mapped[key] = _ref(local)
                elif source["kind"] == "experiment_result":
                    imported = self._import_experiment(task_id, child, source)
                    mapped[key] = imported["record_ref"]
                    experiments.append(imported["record_ref"])
                else:
                    identifier, existing = self._import_identity(task_id, source)
                    if existing is not None:
                        origin = existing["payload"].get("origin", {})
                        if origin.get("task_id") != task_id or origin.get("record_ref") != original:
                            raise TaskError("Imported identity collides with unrelated evidence")
                    missing = (scopes[key] - {prop["id"] for prop in existing["payload"].get("properties", [])}
                               if source["kind"] == "examples" and existing is not None else set())
                    if existing is not None and not missing:
                        entries.append({"local_key": local_key, "op": "reference",
                                        "ref": _ref(existing)})
                    else:
                        selected_payload = source_payload(source)
                        if source["kind"] == "examples" and existing is not None:
                            # Only newly requested properties need new dependency
                            # imports. Preserve the parent's already audited body.
                            added = [prop for prop in selected_payload["properties"] if prop["id"] in missing]
                            payload = copy.deepcopy(existing["payload"])
                            additions = map_record_references({"properties": added}, bring)["properties"]
                            for prop in additions:
                                prop.pop("audit_id", None)
                                prop.pop("challenged_by", None)
                                prop["status"] = "pending"
                            payload["properties"].extend(additions)
                        else:
                            payload = map_record_references(selected_payload, bring)
                        if source["kind"] == "arguments":
                            payload.pop("audit_id", None)
                            payload.pop("challenged_by", None)
                            status = "partial" if payload.get("status", payload.get("tag")) == "partial" else "candidate"
                            payload["status"] = status
                            if "tag" in payload:
                                payload["tag"] = status
                        elif source["kind"] == "examples" and existing is None:
                            for prop in payload.get("properties", []):
                                prop.pop("audit_id", None)
                                prop.pop("challenged_by", None)
                                prop["status"] = "pending"
                        if existing is None:
                            payload["origin"] = {"task_id": task_id, "record_ref": original,
                                                 "import_request_id": operation}
                        if source["kind"] == "examples":
                            metadata = payload.setdefault("metadata", {})
                            if not isinstance(metadata, dict):
                                raise TaskError("Example metadata must be an object to record an import scope")
                            metadata["cell_import_properties"] = sorted(scopes[key] | set(
                                metadata.get("cell_import_properties", []) if existing is not None else []))
                        entries.append({"local_key": local_key, "op": "update" if existing is not None else "create",
                                        "kind": source["kind"], "record_id": identifier, "payload": payload,
                                        **({"expected_revision": existing["revision"]} if existing is not None else {})})
                    mapped[key] = {"local_key": local_key}
            result = copy.deepcopy(mapped[key])
            if "property_ids" in ref:
                result["property_ids"] = copy.deepcopy(ref["property_ids"])
            elif source.get("read_only") and "property_ids" in source:
                result["property_ids"] = copy.deepcopy(source["property_ids"])
            if "position" in ref:
                result["position"] = ref["position"]
            return result

        selected = [bring(ref) for ref in record_refs]
        # Root aliases make the requested selection part of idempotency too:
        # selecting [argument] differs from [claim, argument], even when both
        # operations discover the same transitive graph.
        entries.extend({"local_key": f"selected_{index}", "op": "reference", "ref": ref}
                       for index, ref in enumerate(selected))
        plan = {"request_id": request_id, "operation": operation, "input": request_input, "entries": entries, "selected": selected,
                "mapped_refs": [{"source": {"kind": key[0], "id": key[1], "revision": key[2]},
                                 "imported": value} for key, value in mapped.items()], "experiments": experiments}
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        _write_json(plan_path, plan)
        return execute_plan(plan)

    def _import_identity(self, task_id: str, source: dict) -> tuple[str, dict | None]:
        """Reserve an import ID once under the caller's task lock.

        Provenance in an editable research payload is descriptive. Only this
        service-owned mapping assigns a local identity to a child version.
        """
        path = self._task_dir(task_id) / "import-map.json"
        if path.is_symlink():
            raise TaskError("Import mapping cannot be a link")
        entries = _read_json(path, [])
        if not isinstance(entries, list) or any(not isinstance(row, dict) for row in entries):
            raise TaskError("Invalid import mapping")
        matches = [row for row in entries if json_equal(row.get("source"), _ref(source))]
        if len(matches) > 1:
            raise TaskError("Source has multiple imported identities")
        if matches:
            identifier = matches[0]["record_id"]
        else:
            identifier = "import-" + uuid4().hex
            entries.append({"source": _ref(source), "record_id": identifier})
            _write_json(path, entries)
        try:
            record = self.store.get(source["kind"], identifier,
                                    None if source["kind"] == "examples" else 1)
        except KeyError:
            record = None
        return identifier, record

    def _import_experiment(self, task_id: str, child_store: Store, record: dict) -> dict:
        """Import explicit computation evidence and fresh candidate premises, never audit authority."""
        imported, visiting = {}, set()

        def bring(source: dict) -> dict:
            trust = source.get("current_trust", {})
            # A previously copied computation remains portable after the child
            # deletes its files. Only artifact availability may be replaced by
            # the parent's preserved copy; mathematical objections cannot.
            artifact_only = source["kind"] == "experiment_result" and trust.get("blockers") and all(
                blocker.get("type") == "experiment_artifact" for blocker in trust["blockers"])
            if trust.get("state") in {"withdrawn", "suspended", "dependency_blocked"} and not (
                    trust["state"] == "dependency_blocked" and artifact_only):
                raise TaskError("Cannot import evidence whose child support is suspended, withdrawn or blocked")
            key = (source["kind"], source["id"], source["revision"])
            if key in imported:
                return imported[key]
            if key in visiting:
                raise TaskError("Cannot import a cyclic child evidence graph")
            if len(imported) + len(visiting) >= self.store.settings["retrieval"]["max_memory_results"]:
                raise TaskError("Child evidence import exceeds max_memory_results")
            visiting.add(key)
            original = _ref(source)
            try:
                local = self.store.get(source["kind"], source["id"], source["revision"])
            except (KeyError, ValueError):
                local = None
            if source.get("read_only") and local is not None:
                if source["kind"] == "experiment_result":
                    self.store.evidence_bundle([original])
                imported[key] = _ref(local)
                visiting.remove(key)
                return imported[key]
            if source.get("read_only"):
                raise TaskError("Granted parent record no longer matches its original identity")
            identifier, local = self._import_identity(task_id, source)
            if local is not None:
                origin = local["payload"].get("origin", {})
                if origin.get("task_id") != task_id or origin.get("record_ref") != original:
                    raise TaskError("Imported record identity collides with different evidence")
                if source["kind"] == "experiment_result":
                    self.store.evidence_bundle([_ref(local)])
                imported[key] = _ref(local)
                visiting.remove(key)
                return imported[key]

            def mapped(ref: dict, role="related") -> dict:
                selected = child_store.get(ref["kind"], ref["id"], ref["revision"])
                result = bring(selected)
                if "property_ids" in ref:
                    actual = {prop["id"] for prop in selected["payload"].get("properties", [])}
                    allowed = set(selected.get("property_ids", actual))
                    if not isinstance(ref["property_ids"], list) or not set(ref["property_ids"]) <= allowed:
                        raise TaskError("Requested properties exceed the granted child evidence")
                    result = dict(result, property_ids=ref["property_ids"])
                elif selected.get("read_only") and "property_ids" in selected:
                    result = dict(result, property_ids=selected["property_ids"])
                return result

            payload = map_record_references(source["payload"], mapped)
            origin = {"task_id": task_id, "record_ref": original}
            if source["kind"] == "experiment_result":
                files = read_artifact_groups(child_store.memory_dir.parent, [experiment_group(payload)], settings=self.store.settings)
                # Keep the original relative path below a unique import directory,
                # so identical filenames from distinct child runs never collide.
                names = {name: f"experiments/imports/{task_id}/{identifier}/{name.removeprefix('experiments/')}"
                         for name in files}
                copied = {names[name]: data for name, data in files.items()}
                copy_artifacts(self.run_dir, copied)
                origin["artifact_paths"] = names
                payload["artifacts"] = manifest_for(copied)
                if payload.get("code_file") in names:
                    payload["code_file"] = names[payload["code_file"]]
                for item in payload.get("input_files", []):
                    if item.get("saved_path") in names:
                        item["saved_path"] = names[item["saved_path"]]
                for item in payload["execution"].get("output_files", {}).values():
                    if item.get("path") in names:
                        item["path"] = names[item["path"]]
            elif source["kind"] == "arguments":
                payload.pop("audit_id", None)
                payload.pop("challenged_by", None)
                payload["status"] = "partial" if payload.get("status", payload.get("tag")) == "partial" else "candidate"
                if "tag" in payload:
                    payload["tag"] = payload["status"]
            elif source["kind"] == "examples":
                for prop in payload.get("properties", []):
                    prop.pop("audit_id", None)
                    prop.pop("challenged_by", None)
                    prop["status"] = "pending"
            elif source["kind"] in {"reviews", "events"}:
                raise TaskError("Child review authority cannot be imported as a mathematical premise")
            payload["origin"] = origin
            if source["kind"] == "experiment_result":
                local = self.store.write_experiment_result(identifier, payload,
                                                           request_id=f"import:{task_id}:{identifier}")
            else:
                local = self.store.archive(source["kind"], payload, record_id=identifier,
                                           request_id=f"import:{task_id}:{identifier}")
            imported[key] = _ref(local)
            visiting.remove(key)
            return imported[key]

        result = bring(record)
        return {"record_ref": result, "mapped_refs": [{"source": {"kind": key[0], "id": key[1],
                "revision": key[2]}, "imported": value} for key, value in imported.items()]}

    def collect_task(self, task_id: str, detail: str = "summary", limit: int | None = None,
                     cursor: dict | None = None, kinds: list[str] | None = None,
                     record_ref: dict | None = None, include_result: bool = False,
                     import_refs: list[dict] | None = None, request_id: str | None = None) -> dict:
        """Read child records without consuming them or transferring audit authority.

        A cursor holds append-only offsets and a page scan's upper bounds, bound
        to this task and collection set. Completed scans return a polling cursor.
        Reuse the returned cursor to retry a page (including switching to full
        detail); pass next_cursor to advance or poll for records appended later.
        No cursor starts at the beginning. Exact pinned reads ignore pagination.
        """
        if not isinstance(detail, str) or detail not in {"summary", "full"}:
            raise TaskError("detail must be summary or full")
        if type(include_result) is not bool:
            raise TaskError("include_result must be a boolean")
        if import_refs is not None:
            if cursor is not None or kinds is not None or record_ref is not None or include_result or limit is not None:
                raise TaskError("import_refs cannot be combined with collection paging or result-reading options")
            result = self.import_records(task_id, import_refs, request_id)
            if detail == "summary":
                result = {key: value for key, value in result.items() if key != "records"}
            return {"task_id": task_id, "import_result": result, "requires_parent_audit": True}
        if request_id is not None:
            raise TaskError("request_id applies only to an explicit import_refs operation")
        retrieval = get_settings(self.run_dir)["retrieval"]
        limit = retrieval["memory_results"] if limit is None else limit
        if type(limit) is not int or not 1 <= limit <= retrieval["max_memory_results"]:
            raise TaskError(f"limit must be an integer from 1 to {retrieval['max_memory_results']}")
        if kinds is not None and (not isinstance(kinds, list) or not kinds or
                                  any(kind not in MEMORY_KINDS for kind in kinds) or
                                  len(set(kinds)) != len(kinds)):
            raise TaskError("kinds must be a nonempty list of distinct memory collection names")
        if record_ref is not None:
            if cursor is not None or kinds is not None:
                raise TaskError("record_ref cannot be combined with cursor or kinds")
            if (not isinstance(record_ref, dict) or
                    not {"kind", "id", "revision"} <= record_ref.keys() or
                    record_ref["kind"] not in MEMORY_KINDS or
                    not isinstance(record_ref["id"], str) or
                    type(record_ref["revision"]) is not int or record_ref["revision"] < 1):
                raise TaskError("record_ref requires a valid kind, id and positive integer revision")
            selected = [record_ref["kind"]]
        elif cursor is not None:
            if (not isinstance(cursor, dict) or set(cursor) != {"version", "task_id", "positions", "ends"} or
                    type(cursor["version"]) is not int or cursor["version"] != 1 or
                    cursor["task_id"] != task_id or not isinstance(cursor["positions"], dict) or
                    not cursor["positions"] or
                    any(kind not in MEMORY_KINDS or type(offset) is not int or offset < 0
                        for kind, offset in cursor["positions"].items())):
                raise TaskError("Invalid cursor or cursor belongs to another task")
            if cursor["ends"] is not None and (
                    not isinstance(cursor["ends"], dict) or
                    set(cursor["ends"]) != set(cursor["positions"]) or
                    any(type(end) is not int or end < cursor["positions"][kind]
                        for kind, end in cursor["ends"].items())):
                raise TaskError("Invalid cursor collection bounds")
            selected = [kind for kind in MEMORY_KINDS if kind in cursor["positions"]]
            if kinds is not None and set(kinds) != set(selected):
                raise TaskError("Cursor collection set cannot change; start a new scan")
        else:
            selected = [kind for kind in MEMORY_KINDS if kind in (kinds or RESEARCH_KINDS)]
        positions = ({kind: cursor["positions"][kind] for kind in selected} if cursor is not None
                     else {kind: 0 for kind in selected})
        with _tasks_lock(self.tasks_dir):
            task_dir = self._task_dir(task_id)
            task = _read_json(task_dir / "task.json")
            workspace = task_dir / "workspace"
            records, warnings, totals = [], [], {}
            stale = self._snapshot_changes(task)
            if stale:
                task["stale_context"] = stale
                if task["status"] in ACTIVE:
                    (task_dir / "cancel.flag").touch()
                    task.update(status="cancel_requested", cancel_requested_at=_now())
                _write_json(task_dir / "task.json", task)
                warnings.append("Parent support for the granted context is withdrawn or blocked. Preserve this work as candidates; repair dependencies and re-audit before use.")
            next_positions = dict(positions)
            ends = dict(positions)
            child_store = Store(workspace / "memory")
            try:
                # One locked Store view prevents observing only part of an
                # archive_result commit across several collection files.
                snapshot = child_store.snapshot(kinds=selected, include_context=False)
                rows_by_kind = {kind: [] for kind in selected}
                for row in snapshot:
                    rows_by_kind[row["kind"]].append(row)
                snapshot_error = None
            except (OSError, ValueError, KeyError, TypeError) as exc:
                rows_by_kind, snapshot_error = {}, exc
            for kind in selected:
                try:
                    if snapshot_error is not None:
                        raise ValueError(f"Cannot obtain a consistent Store snapshot: {snapshot_error}")
                    rows = rows_by_kind[kind]
                    if positions[kind] > len(rows):
                        raise TaskError(f"Collection {kind} became shorter than its cursor")
                    totals[kind] = len(rows)
                    ends[kind] = (cursor["ends"][kind] if cursor is not None and cursor["ends"] is not None
                                  else len(rows))
                    if ends[kind] > len(rows):
                        raise TaskError(f"Collection {kind} became shorter than its scan bounds")
                    if record_ref is not None:
                        page = [row for row in rows if _key(row) == _key(record_ref)]
                        if len(page) != 1:
                            raise KeyError(f"Pinned child record not found: {record_ref}")
                    else:
                        page = rows[positions[kind]:min(ends[kind], positions[kind] +
                                                       max(0, limit - len(records)))]
                    for record in page:
                        if record["kind"] != kind:
                            raise ValueError("record kind does not match collection")
                        _ref(record)
                    records.extend(page)
                    next_positions[kind] += len(page)
                except TaskError:
                    raise
                except (OSError, ValueError, KeyError, TypeError) as exc:
                    if record_ref is not None:
                        raise TaskError(f"Cannot read pinned child record: {exc}") from exc
                    warnings.append(f"{kind}: {exc}")
            result_path = workspace / "task_result.md"
            try:
                result = _read_json(task_dir / "result.json")
                if result is not None and not isinstance(result, dict):
                    raise ValueError("invalid result metadata")
                result = dict(result) if result else None
                if result is not None:
                    # Legacy subcells always wrote an unresolved placeholder,
                    # even when their actual saved result proved the target.
                    result.pop("mathematical_outcome", None)
                agent_result = result.pop("agent_result", None) if result is not None else None
                if isinstance(agent_result, dict) and result is not None:
                    result["agent_result"] = {key: agent_result[key] for key in
                                              ("returncode", "session_id", "log_path", "elapsed_seconds")
                                              if key in agent_result}
                result_text = None
                if include_result:
                    result_text = (result_path.read_text(encoding="utf-8", errors="replace")
                                   if result_path.exists() else
                                   agent_result.get("text") if isinstance(agent_result, dict) else None)
            except (OSError, ValueError) as exc:
                result, result_text = None, None
                warnings.append(f"result: {exc}")
            subcell_log = task_dir / "subcell.log"
            if not subcell_log.exists() and (task_dir / "worker.log").exists():
                subcell_log = task_dir / "worker.log"
            response = {"task_id": task_id, "status": task["status"], "scope": task["scope"],
                        "group_id": task["group_id"], "detail": "full" if record_ref else detail,
                        "record_refs": [_ref(record)
                                        for record in records], "count": len(records),
                        "totals": totals, "requires_parent_audit": True, "result": result,
                        "stale_context": stale, "acceptance": "stale" if stale else "candidate",
                        "warnings": warnings,
                        "artifacts": {"workspace": str(workspace), "memory_dir": str(workspace / "memory"),
                                      "subcell_log": str(subcell_log),
                                      "agent_log": str(workspace / "task_result.md.events.jsonl"),
                                      "result_file": str(result_path)}}
            if detail == "full" or record_ref is not None:
                response["records"] = [child_store.get(r["kind"], r["id"], r["revision"]) for r in records]
                for record in response["records"]:
                    if record["kind"] == "experiment_result":
                        imported = self._import_experiment(task_id, child_store, record)
                        record["imported_record_ref"] = imported["record_ref"]
                        record["imported_refs"] = imported["mapped_refs"]
                if stale:
                    for record in response["records"]:
                        record["parent_acceptance"] = "stale"
            if include_result:
                response["result_text"] = result_text
            if record_ref is None:
                scan_has_more = any(ends[kind] > next_positions[kind] for kind in ends)
                response.update(
                    cursor={"version": 1, "task_id": task_id, "positions": positions, "ends": ends},
                    next_cursor={"version": 1, "task_id": task_id, "positions": next_positions,
                                 "ends": ends if scan_has_more else None},
                    has_more=any(totals[kind] > next_positions[kind] for kind in totals),
                    incremental=True)
            return response
