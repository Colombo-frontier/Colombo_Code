"""Isolated Cell preparation, supervision, execution, and snapshot export.

This executable never imports the Brain application's database or controller.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path as BootstrapPath
import shutil
import subprocess
import sys
import time
import traceback

if __package__ in {None, ""}:
    sys.path.insert(0, str(BootstrapPath(__file__).resolve().parents[2]))

from colombo.cell.diagnostics import read_stop_diagnostics, read_experiment_stop_diagnostics
from colombo.shared.runtime_budget import cell_operational
from colombo.shared.file_io import Path
from colombo.shared.file_io import atomic_write
from colombo.shared.process_control import execution_scope
from colombo.shared.file_io import file_lock
from colombo.shared.file_io import freeze_json
from colombo.shared.file_io import json_equal
from colombo.shared.process_control import process_identity
from colombo.shared.file_io import read_json
from colombo.shared.process_control import spawn_options
from colombo.shared.process_control import terminate_tree
from colombo.shared.file_io import write_json
from colombo.shared.process_control import managed_popen
from colombo.shared.process_control import close_process_job
from colombo.shared.process_control import load_stop_request
from colombo.shared.process_control import complete_stop_request


def _cell_imports(project: Path):
    if not (project / "src/colombo/cell/controller.py").is_file():
        raise ValueError("Cell runtime is missing")
    from colombo.cell.controller import initialize
    from colombo.cell.controller import solve
    from colombo.shared.file_io import Path as CellPath
    from colombo.cell.settings import configure
    from colombo.cell.record_store import Store
    from colombo.cell.verifier.proof_review import manuscript_is_current
    return initialize, solve, CellPath, configure, Store, manuscript_is_current


def _verify_inputs(task: Path) -> None:
    prepared = read_json(task / "prepared.json")
    request = read_json(task / "prepare_request.json")
    _cell_imports(Path(request["project_root"]))
    if any(type(row.get("storage_version")) is not int or row["storage_version"] not in {3, 4}
           for row in (prepared, request)):
        raise ValueError("Unsupported Cell preparation storage version")
    for key in ("task_id", "assignment_ref", "package_ref"):
        if not json_equal(prepared.get(key), request.get(key)):
            raise ValueError("Prepared task scope differs from its request")
    if request["task_id"] != task.name:
        raise ValueError("Prepared task identity differs")
    if not (task / "cell/problem.md").is_file():
        raise ValueError("Cell task statement is missing")
    frozen_problem = task / "input/cell_problem.md"
    if frozen_problem.is_file() and frozen_problem.read_bytes() != (task / "cell/problem.md").read_bytes():
        raise ValueError("Cell changed the fixed Task statement")
    if not json_equal(read_json(task / "cell/run.json").get("required_review_files", []),
                      request.get("required_review_files", [])):
        raise ValueError("Cell required review inputs differ from their preparation")
    from colombo.cell.instructions import validate_mode
    from colombo.cell.instructions import read_cell_mode
    expected_mode = validate_mode(request.get("research_mode", "generic"), request.get("specialization", "general"))
    for key in ("research_mode", "specialization"):
        if prepared.get(key, {"research_mode": "generic", "specialization": "general"}[key]) != expected_mode[key]:
            raise ValueError("Prepared Cell mode differs from its request")
    saved_mode = read_cell_mode(task / "cell")
    if not json_equal(saved_mode, expected_mode):
        raise ValueError("Frozen Cell mode differs from its preparation")
    config_mode = read_json(task / "cell/run.json").get("cell_mode")
    if config_mode is not None and not json_equal(config_mode, saved_mode):
        raise ValueError("Frozen Cell mode differs from run configuration")
    for row in request["package_files"]:
        path = task / "cell/inputs/package" / row["path"]
        if path.is_symlink() or not path.resolve().is_relative_to(task / "cell/inputs/package") or not path.is_file():
            raise ValueError("Missing or invalid input package path")
        if row.get("sha256") and hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            raise ValueError("Frozen Cell input package content differs")


def prepare(request_path: Path) -> None:
    request = read_json(request_path)
    if type(request.get("storage_version")) is not int or request["storage_version"] not in {3, 4}:
        raise ValueError("Unsupported Cell preparation storage version")
    execution_scope({**request, "attempt_id": "prepare"})
    task = Path(request["task_dir"]).resolve()
    project = Path(request["project_root"]).resolve()
    package = Path(request["package_dir"]).resolve()
    config = request["config"]
    initialize, _, CellPath, configure, _, _ = _cell_imports(project)
    from colombo.cell.instructions import validate_mode
    from colombo.cell.instructions import read_cell_mode
    cell_mode = validate_mode(request.get("research_mode", "generic"), request.get("specialization", "general"))
    if cell_mode["specialization"] == "experiment":
        from colombo.experiment_cell.controller import initialize
    mode_args = {key: cell_mode[key] for key in ("research_mode", "specialization")}
    original = (task / "input/problem.md").read_bytes()
    # The package index is included in the problem given to Cell.
    note = ("\n\n## Pinned Material Package Provided by Brain\n"
            "First read inputs/package/README.md and inputs/package/manifest.json, "
            "then read the actual materials according to their required/reference designations. The materials include provenance, versions, and limitations; "
            "Brain's judgments and unreviewed drafts must not automatically be treated as proved premises. "
            "Do not modify the input snapshots in inputs/package.\n")
    text = original.decode("utf-8-sig") + note
    prepared_problem = task / "input/cell_problem.md"
    data = text.encode("utf-8")
    if prepared_problem.exists() and prepared_problem.read_bytes() != data:
        raise ValueError("Frozen Cell problem differs")
    atomic_write(prepared_problem, data)
    cell = task / "cell"
    if not (cell / "run.json").exists():
        if "settings" in config:
            initialize(CellPath(prepared_problem), CellPath(cell),
                       settings_snapshot=config["settings"], profile=config["profile"],
                       **mode_args,
                       required_review_files=request.get("required_review_files", []))
        else:
            # Previously saved run/prepare requests keep their original meaning.
            from colombo.cell.settings import load_defaults
            from colombo.cell.settings import merge_settings
            legacy, selected = load_defaults(config.get("profile"))
            patch = dict(config.get("settings_overrides", {}))
            agents = dict(patch.get("agents", {}))
            if config.get("timeout_seconds") is not None:
                for name in ("prover", "subcell", "verifier", "report_check"):
                    agents[name + "_timeout_seconds"] = config["timeout_seconds"]
            if config.get("max_rounds") is not None:
                for name in ("prover", "verifier"):
                    agents[name + "_max_rounds"] = config["max_rounds"]
            patch["agents"] = agents
            if config.get("model"):
                patch["model"] = {**patch.get("model", {}), "name": config["model"]}
            legacy = merge_settings(legacy, patch)
            legacy["network"]["prover_search_enabled"] = config.get("search", False)
            initialize(CellPath(prepared_problem), CellPath(cell),
                       settings_snapshot=legacy,
                       profile=selected,
                       **mode_args,
                       required_review_files=request.get("required_review_files", []))
    elif (cell / "problem.md").read_bytes() != data:
        raise ValueError("Existing Cell workspace belongs to a different task")
    elif not json_equal(read_json(cell / "run.json").get("required_review_files", []),
                        request.get("required_review_files", [])):
        raise ValueError("Existing Cell review inputs differ")
    read_cell_mode(cell, **mode_args)
    target = cell / "inputs/package"
    target.mkdir(parents=True, exist_ok=True)
    for row in request["package_files"]:
        source = package / row["path"]
        if source.is_symlink() or not source.resolve().is_relative_to(package):
            raise ValueError("Package source escapes its directory")
        payload = source.read_bytes()
        destination = target / row["path"]
        if destination.is_symlink() or not destination.resolve().is_relative_to(target):
            raise ValueError("Package destination escapes its directory")
        if destination.exists() and destination.read_bytes() != payload:
            raise ValueError("Existing Cell input snapshot differs")
        atomic_write(destination, payload)
    write_json(task / "prepared.json", {"storage_version": request["storage_version"],
        **{key: request[key] for key in ("task_id", "assignment_ref", "package_ref")},
        **cell_mode,
        "prepared_at": time.time()})
    _verify_inputs(task)


def solve(request_path: Path) -> int:
    request = read_json(request_path)
    task = Path(request["task_dir"])
    result = {"returncode": None, "error": None, "failure": None}
    try:
        _verify_inputs(task)
        prepared = read_json(task / "prepared.json")
        if not json_equal(execution_scope(request), execution_scope({**prepared, "attempt_id": request["attempt_id"]})):
            raise ValueError("Execution request belongs to another task scope")
        _, cell_solve, CellPath, _, _, _ = _cell_imports(Path(request["project_root"]))
        empirical = prepared.get("specialization") == "experiment"
        if empirical:
            from colombo.experiment_cell.controller import solve as cell_solve
        cell = CellPath(task / "cell")
        config = request["config"]
        if config.get("policy_metadata"):
            # A new/reconciled execution adopts the one resolved root policy.
            # Counts, records, review phase, and process histories stay intact.
            from colombo.cell.settings import run_fields
            saved = read_json(cell / "run.json")
            saved.update(settings=config["settings"], profile=config["profile"],
                         policy_metadata=config["policy_metadata"])
            saved.update(run_fields(config["settings"]))
            write_json(cell / "run.json", saved)
        if request.get("restart"):
            if request.get("restart") is not True or request.get("resume") is not True:
                raise ValueError("Restart must explicitly continue the same prepared Task")
            from colombo.cell.restart_budget import grant_restart
            from colombo.cell.settings import get_settings
            grant_restart(cell, execution_scope(request), get_settings(cell), empirical=empirical)
        events_path = cell / "run_events.jsonl"
        events_before = len(events_path.read_text(encoding="utf-8").splitlines()) if events_path.is_file() else 0
        if not empirical and request["config"].get("stop_on_confirmed_error", False):
            # The frozen runner checks reviews after each prover exits. Intercept
            # that boundary in this isolated solver process, before it can start
            # another prover; never alter the baseline source or live settings.
            import colombo.cell.controller as cell_runner
            original = cell_runner._review_to_boundary
            existing_failure = confirmed_answer_failure(cell)
            # An explicitly resumed new attempt may repair a previously reported
            # error. A pending review completed now is still a new observation.
            repair_review_id = (existing_failure["review_id"]
                                if request.get("resume") and existing_failure else None)
            def checked_boundary(root):
                decision = original(root)
                failure = confirmed_answer_failure(root)
                if failure and failure["review_id"] != repair_review_id:
                    raise ConfirmedAnswerError(failure)
                return decision
            try:
                if existing_failure and not repair_review_id:
                    raise ConfirmedAnswerError(existing_failure)
                cell_runner._review_to_boundary = checked_boundary
                result["returncode"] = cell_solve(cell)
            finally:
                cell_runner._review_to_boundary = original
        else:
            result["returncode"] = cell_solve(cell)
        # The legacy runner catches individual prover failures and may return
        # incomplete. Preserve the reason instead of reporting only exit code 2.
        if result["returncode"] != 0 and events_path.is_file():
            for line in events_path.read_text(encoding="utf-8").splitlines()[events_before:]:
                event = json.loads(line)
                if event.get("action") == "prover_error":
                    result["failure"] = {"kind": "runtime_error", "message": event["error"],
                                         "source": "run_events.jsonl", "time": event.get("time")}
    except ConfirmedAnswerError as exc:
        result.update(returncode=2, failure=exc.failure)
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["failure"] = {"kind": "runtime_error", "message": result["error"]}
        traceback.print_exc()
    write_json(request_path.parent / "solve_result.json", result)
    return result["returncode"] if type(result["returncode"]) is int else 1


class ConfirmedAnswerError(Exception):
    def __init__(self, failure):
        self.failure = failure
        super().__init__(failure["message"])


def confirmed_answer_failure(root):
    """Return only current, independently confirmed explicit mathematical errors.

    Gaps, uncertainty and unconfirmed criticism never imply a wrong answer.
    Broken provenance raises instead of manufacturing a mathematical finding.
    """
    import colombo.cell.verifier.proof_review as review
    root = review.Path(root).resolve()
    if not (root / "submission.json").is_file():
        return None
    submission = review._load(root / "submission.json")
    if submission.get("status") != "needs_revision" or not submission.get("review_id"):
        return None
    item = next((row for row in review._index(root)["attempts"]
                 if row.get("id") == submission["review_id"]), None)
    if not item or item.get("protocol") != review.REVIEW_PROTOCOL or item.get("phase") != "complete" or item.get("status") != "revise":
        return None
    if not review.submission_matches(root, submission, item):
        raise ValueError("Confirmed error review does not match the current submission")
    folder = review._review_dir(root, item["id"])
    report, confirmation = review._report_pair(folder, item)
    findings = [row for row in report["findings"] if row["kind"] == "error"]
    if report["verdict"] != "revise" or not findings:
        return None
    revision = item["report_revision"]
    return {"kind": "mathematical_error", "message": report["summary"],
            "review_id": item["id"], "report_revision": revision,
            "findings": findings, "evidence": [
                {"cell_path": f"reviews/{item['id']}/reports/p{revision:04d}.json"},
                {"cell_path": f"reviews/{item['id']}/checks/p{revision:04d}/confirmation.json"}]}


def _publish_receipt(request_path, result_path, result):
    request = read_json(request_path)
    task = Path(request["task_dir"])
    if not json_equal(execution_scope(result), execution_scope(request)):
        raise ValueError("Exported result does not match this task and attempt")
    if result_path.relative_to(task).as_posix() != f"results/{request['attempt_id']}/result.json":
        raise ValueError("Result path does not name this attempt")
    for artifact in result.get("artifacts", []):
        path = task / artifact["path"]
        if path.is_symlink() or not path.resolve().is_relative_to(task) or not path.is_file():
            raise ValueError("Exported artifact path is invalid or missing")
    freeze_json(request_path.parent / "receipt.json", {
        **execution_scope(request), "result_path": result_path.relative_to(task).as_posix()})
    stop = load_stop_request(request_path.parent, request)
    if stop is not None:
        complete_stop_request(request_path.parent, stop, result_path, result)


def _research_process_ids(root):
    """Read durable actual researcher starts; preparation/review is not research."""
    folder = Path(root) / "runtime" / "research_starts"
    if not folder.is_dir():
        return []
    identifiers = []
    for path in folder.glob("*.json"):
        if path.is_symlink() or not path.resolve().is_relative_to(Path(root).resolve()):
            raise ValueError("Research start marker escapes its workspace")
        marker = read_json(path)
        if marker.get("role") != "prover" or marker.get("process_id") != path.stem:
            raise ValueError("Invalid research process start marker")
        identifiers.append(path.stem)
    return sorted(identifiers)


def _research_activity(request_path, snapshot):
    baseline = Path(request_path).parent / "research_baseline.json"
    if not baseline.is_file():
        # Legacy snapshots or unstarted cancellations provide no evidence of a
        # new researcher. Never grant a new integration clock on uncertainty.
        return {"started": False, "process_ids": []}
    before = read_json(baseline)["process_ids"]
    new = sorted(set(_research_process_ids(snapshot)) - set(before))
    return {"started": bool(new), "process_ids": new}


def export_result(request_path: Path, execution: str, reason: str, *, stop=None, started=True, failure=None) -> dict:
    request = read_json(request_path)
    task, project = Path(request["task_dir"]), Path(request["project_root"])
    cell = task / "cell"
    folder = task / "results" / request["attempt_id"]
    result_path = folder / "result.json"
    if result_path.exists():
        result = read_json(result_path)
        _publish_receipt(request_path, result_path, result)
        return result
    _, _, CellPath, _, Store, manuscript_is_current = _cell_imports(project)
    artifact_root = folder / "artifacts"
    artifact_root.mkdir(parents=True, exist_ok=True)
    errors, artifacts = [], []
    empirical = read_json(task / "prepared.json").get("specialization") == "experiment" if (task / "prepared.json").is_file() else False
    empirical_report = None
    if empirical:
        from colombo.experiment_cell.controller import current_report
        empirical_report = current_report(cell)
    accepted = False if empirical else manuscript_is_current(CellPath(cell))
    submission = {}
    if (cell / "submission.json").exists():
        try:
            submission = read_json(cell / "submission.json")
        except (OSError, ValueError) as exc:
            errors.append(f"submission: {exc}")

    def add_file(path: Path, kind: str):
        relative = path.relative_to(cell)
        if path.is_symlink() or not path.resolve().is_relative_to(cell):
            raise ValueError("Export source escapes Cell workspace")
        payload = path.read_bytes()
        destination = artifact_root / relative
        if destination.exists() and destination.read_bytes() != payload:
            raise ValueError("Frozen artifact already exists with different content")
        atomic_write(destination, payload)
        if any(a["path"] == destination.relative_to(task).as_posix() for a in artifacts):
            return
        artifacts.append({"path": destination.relative_to(task).as_posix(),
                          "size": len(payload), "kind": kind})

    for name in ("problem.md", "run.json", "submission.json", "draft.md", "manuscript.md", "run_events.jsonl",
                 "reviews/index.json", "runtime/prover_state.json"):
        path = cell / name
        if path.is_file():
            add_file(path, "cell_document")
    for name in submission.get("evidence_files", []):
        if isinstance(name, str):
            path = cell / name
            if path.is_file() and path.resolve().is_relative_to(cell):
                add_file(path, "submitted_evidence")
    # Confirmed top-level review artifacts, never the reviewer's authentication or runtime trees.
    if (cell / "reviews").is_dir():
        for review in sorted((cell / "reviews").iterdir()):
            if review.is_dir() and not review.is_symlink():
                for name in ("report.json", "confirmation.json", "manifest.json", "request.json", "error.json"):
                    if (review / name).is_file():
                        add_file(review / name, "review_receipt")
    # Canonical versioned reports used by confirmed failures, not only convenience views.
    for entry in (failure or {}).get("evidence", []):
        if isinstance(entry.get("cell_path"), str):
            add_file(cell / entry["cell_path"], "review_receipt")
    if (cell / "memory").is_dir():
        try:
            records = Store(CellPath(cell / "memory")).snapshot(with_trust=True)
            snapshot = artifact_root / "memory_snapshot.json"
            freeze_json(snapshot, {"schema_version": 2, "records": records})
            payload = snapshot.read_bytes()
            artifacts.append({"path": snapshot.relative_to(task).as_posix(),
                              "size": len(payload), "kind": "research_memory_snapshot"})
        except Exception as exc:
            errors.append(f"memory_snapshot: {type(exc).__name__}: {exc}")
            accepted = False
    # Every returned attempt freezes the complete research tree. The input package
    # remains selected context; this archive is the complete output history.
    from colombo.cell.attempt_archive import freeze_attempt_archive
    archive, full_artifacts = freeze_attempt_archive(cell, folder, task, add_file)
    artifacts.extend(full_artifacts)
    # Never issue acceptance if anything changed during snapshot export.
    if accepted and not manuscript_is_current(CellPath(cell)):
        accepted = False
        errors.append("Acceptance changed while exporting")
    # A valid saved manuscript can survive a later process failure/timeout; retain both facts.
    status = execution
    if not accepted and not empirical_report and status == "finished":
        status = "incomplete"
    if errors and execution != "cancelled":
        status = "error"
    if errors and failure is None:
        failure = {"kind": "runtime_error", "message": "Snapshot export failed: " + "; ".join(errors),
                   "source": "snapshot_export"}
    if failure is None and execution in {"error", "timeout"}:
        failure = {"kind": "timeout" if execution == "timeout" else "runtime_error", "message": reason}
    if failure and failure.get("kind") == "mathematical_error":
        current = confirmed_answer_failure(CellPath(cell))
        if not json_equal(current, failure):
            raise ValueError("Confirmed mathematical failure changed before export")
        for entry in failure["evidence"]:
            artifact = next((a for a in artifacts if a["path"] ==
                             (artifact_root / entry["cell_path"]).relative_to(task).as_posix()), None)
            if not artifact:
                raise ValueError("Mathematical failure evidence was not frozen")
    summary = "Cell manuscript passed its current review gate." if accepted else "Cell did not return a currently accepted manuscript."
    if empirical:
        summary = (empirical_report or {}).get("summary", "Experiment Cell returned without a complete empirical report.")
    if (cell / "draft.md").is_file() and not accepted:
        summary += " A draft is available for inspection; it is not an accepted result."
    if failure:
        summary += f" Failure [{failure['kind']}]: {failure['message']}"
    result = {"execution_status": status, "accepted": accepted,
              "review_status": "accepted" if accepted else submission.get("status", "not_submitted"),
              "scientific_outcome": submission.get("outcome") if accepted else None,
              "summary": summary, "stop_reason": reason,
              "artifacts": list({a["path"]: a for a in artifacts}.values()),
              "run_dir": str(cell), **execution_scope(request), "export_errors": errors,
              "exported_at": time.time()}
    result["archive"] = archive
    result["research_activity"] = _research_activity(request_path, artifact_root)
    result["evidence_kind"] = "empirical" if empirical else "proof"
    if empirical:
        result.update(empirical_report=empirical_report,
                      review_status="pending" if empirical_report else "not_submitted",
                      scientific_outcome=None)
    if empirical:
        result.update(read_experiment_stop_diagnostics(artifact_root, execution=status,
            report_complete=empirical_report is not None, reason=reason, failure=failure))
    else:
        result.update(read_stop_diagnostics(artifact_root, execution=status, accepted=accepted,
                                           reason=reason, failure=failure))
    if failure:
        result["failure"] = failure
    if execution == "cancelled":
        if stop is None:
            raise ValueError("Cancellation needs its fixed stop request")
        result.update(stop_request=stop, started=started)
    freeze_json(result_path, result)
    _publish_receipt(request_path, result_path, result)
    return result


def supervise(request_path: Path) -> None:
    request = read_json(request_path)
    folder = request_path.parent
    config = request["config"]
    lock_timeout = cell_operational(config, "task_lock_timeout_seconds", 1)
    lock_poll = cell_operational(config, "lock_poll_seconds", 0.05)
    process_poll = cell_operational(config, "process_poll_seconds", 0.2)
    terminate_wait = cell_operational(config, "terminate_wait_seconds", 10)
    with file_lock(folder / ".supervisor.lock", timeout=lock_timeout, poll_seconds=lock_poll):
        if (folder / "receipt.json").exists():
            return
        launch = read_json(folder / "launch.json")
        write_json(folder / "worker.json", {"nonce": launch["nonce"], "identity": process_identity(),
                                           "started_at": time.time()})
        limit = config["run_timeout_seconds"]
        if limit != "unlimited" and (type(limit) not in (int, float) or not math.isfinite(limit) or limit <= 0):
            raise ValueError('run_timeout_seconds must be positive seconds or "unlimited"')
        _cell_imports(Path(request["project_root"]))
        from colombo.shared.runtime_budget import inherited_deadline
        deadline = inherited_deadline(Path(request["task_dir"]))
        if limit != "unlimited":
            local_deadline = time.monotonic() + limit
            deadline = local_deadline if deadline is None else min(deadline, local_deadline)
        stop = load_stop_request(folder, request)
        if stop is not None:
            export_result(request_path, "cancelled", "pruned", stop=stop, started=False)
            return
        baseline = folder / "research_baseline.json"
        if not baseline.exists():
            freeze_json(baseline, {"process_ids": _research_process_ids(Path(request["task_dir"]) / "cell")})
        command = [sys.executable, "-B", str(Path(__file__).resolve()), "solve", "--request", str(request_path)]
        status, reason, failure = "error", "Solver did not start", None
        with (folder / "cell.log").open("ab") as log:
            process = managed_popen(command, terminate_wait_seconds=terminate_wait,
                                    cwd=request["project_root"], stdin=subprocess.DEVNULL,
                                    stdout=log, stderr=subprocess.STDOUT)
            try:
                write_json(folder / "solver.json", {"identity": process_identity(process.pid), "started_at": time.time()})
                while True:
                    code = process.poll()
                    if code is not None:
                        status = "finished" if code == 0 else "incomplete" if code == 2 else "error"
                        detail = read_json(folder / "solve_result.json") if (folder / "solve_result.json").exists() else {}
                        failure = detail.get("failure")
                        reason = ("confirmed_answer_error" if failure and failure.get("kind") == "mathematical_error"
                                  else detail.get("error") or (failure or {}).get("message") or f"Cell runner exited with code {code}")
                        stop = None  # A natural exit observed first retains its result.
                        break
                    stop = load_stop_request(folder, request)
                    if stop is not None:
                        if process.poll() is not None:
                            continue
                        status, reason = "cancelled", "pruned"
                        break
                    remaining = None if deadline is None else deadline - time.monotonic()
                    if remaining is not None and remaining <= 0:
                        status, reason = "timeout", "Cell reached the inherited research deadline"
                        break
                    try:
                        process.wait(timeout=process_poll if remaining is None else min(process_poll, remaining))
                    except subprocess.TimeoutExpired:
                        pass
                if not terminate_tree(process, timeout=terminate_wait, poll_seconds=process_poll):
                    write_json(folder / "supervisor_error.json", {"reason": "Could not confirm solver descendants stopped"})
                    return  # No stable snapshot is safe while the old solver might still write.
            finally:
                close_process_job(process)
        export_result(request_path, status, reason, stop=stop, failure=failure)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "supervise", "solve"])
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args()
    request_path = args.request.resolve()
    try:
        if args.mode == "prepare":
            prepare(request_path)
        elif args.mode == "solve":
            return solve(request_path)
        else:
            supervise(request_path)
        return 0
    except Exception as exc:
        traceback.print_exc()
        write_json(request_path.parent / (args.mode + "_error.json"),
                   {"type": type(exc).__name__, "error": str(exc), "time": time.time()})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
