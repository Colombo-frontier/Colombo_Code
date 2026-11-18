"""Independent empirical research lifecycle; never enters Proof acceptance."""
from __future__ import annotations

import hashlib
import json
from colombo.shared.file_io import Path
from colombo.shared.file_io import atomic_write
from colombo.cell.instructions import read_cell_mode
from colombo.cell.settings import get_settings
from colombo.cell.model_calls import run_agent
from colombo.cell.record_store import Store


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _save(path, value):
    atomic_write(Path(path), (json.dumps(value, ensure_ascii=False, indent=2,
                                             allow_nan=False) + "\n").encode("utf-8"))


def initialize(problem, root, **kwargs):
    from colombo.cell.controller import initialize as initialize_workspace
    initialize_workspace(problem, root, **kwargs)
    root = Path(root)
    record = Store(root / "memory").archive("proof_state", {
        "research_question": (root / "problem.md").read_text(encoding="utf-8"),
        "status": "unreviewed", "purpose": "Fixed empirical Task target; no mathematical certification"},
        request_id="experiment-task-initialization")
    config = _read(root / "run.json")
    config["experiment_target_ref"] = {key: record[key] for key in ("kind", "id", "revision")}
    _save(root / "run.json", config)


def target_ref(root):
    root = Path(root)
    mode = read_cell_mode(root, research_mode="oracle_complexity", specialization="experiment")
    ref = _read(root / "run.json")["experiment_target_ref"]
    store = Store(root / "memory")
    record = store.get(ref["kind"], ref["id"], ref["revision"])
    if record["payload"].get("research_question") != (root / "problem.md").read_text(encoding="utf-8"):
        raise ValueError("Experiment target differs from its fixed assignment")
    return ref


def validate_report(root, report):
    from colombo.shared.experiment_execution import _safe_file
    root = Path(root).resolve()
    if not isinstance(report, dict):
        raise ValueError("Empirical report must be an object")
    for key in ("summary", "actual_scope", "method", "uncertainty"):
        if not isinstance(report.get(key), str) or not report[key].strip():
            raise ValueError(f"Empirical report requires {key}")
    for key in ("measurements", "candidate_rates", "limitations", "failures"):
        if not isinstance(report.get(key), list):
            raise ValueError(f"Empirical report requires a {key} list")
    if report.get("outcome") not in {"observations", "inconclusive"}:
        raise ValueError("Empirical outcome must be observations or inconclusive, never proved")
    refs = report.get("experiment_refs")
    paths = report.get("artifact_paths")
    if not isinstance(refs, list) or not isinstance(paths, list):
        raise ValueError("Empirical report requires experiment_refs and artifact_paths")
    fixed = target_ref(root)
    store = Store(root / "memory")
    completed = False
    for ref in refs:
        if not isinstance(ref, dict) or set(ref) != {"kind", "id", "revision"} or ref["kind"] != "experiment_result":
            raise ValueError("Expected fixed experiment_result references")
        record = store.get(ref["kind"], ref["id"], ref["revision"])
        if record["payload"].get("target_ref") != fixed:
            raise ValueError("Experiment did not address this fixed Task target")
        completed |= record["payload"]["execution"]["status"] == "completed"
    for relative in paths:
        _safe_file(root, relative)
    if report["outcome"] == "observations" and (not completed or not paths or not report["measurements"]):
        raise ValueError("Observations require completed execution, measurements and preserved artifacts")
    if report["outcome"] == "inconclusive" and not report["limitations"]:
        raise ValueError("Inconclusive reports must explain their limitations")
    return report


def submit_report(root, report, body):
    root = Path(root)
    from colombo.shared.tool_jobs import pending_jobs
    if pending_jobs(root):
        raise ValueError("Retrieve pending Experiment jobs before submitting the report")
    validate_report(root, report)
    if not isinstance(body, str) or not body.strip():
        raise ValueError("A self-contained report body is required")
    _save(root / "empirical_report.json", report)
    atomic_write(root / "report.md", body.encode("utf-8"))
    receipt = {"evidence_kind": "empirical", "status": "submitted", "accepted": False,
        "target_ref": target_ref(root),
        "report_sha256": hashlib.sha256((root / "empirical_report.json").read_bytes()).hexdigest(),
        "body_sha256": hashlib.sha256((root / "report.md").read_bytes()).hexdigest()}
    _save(root / "empirical_submission.json", receipt)
    return receipt


def current_report(root):
    root = Path(root)
    if not (root / "empirical_submission.json").is_file():
        return None
    receipt = _read(root / "empirical_submission.json")
    for name, key in (("empirical_report.json", "report_sha256"), ("report.md", "body_sha256")):
        if not (root / name).is_file() or hashlib.sha256((root / name).read_bytes()).hexdigest() != receipt.get(key):
            return None
    if receipt.get("target_ref") != target_ref(root):
        raise ValueError("Empirical submission belongs to a different Task")
    return validate_report(root, _read(root / "empirical_report.json"))


def solve(root):
    from colombo.cell.controller import _exclusive_run
    from colombo.cell.controller import event
    from colombo.cell.restart_budget import effective_limit
    root = Path(root)
    with _exclusive_run(root):
        fixed = target_ref(root)
        settings = get_settings(root)
        state_path = root / "runtime" / "experiment_state.json"
        state = _read(state_path) if state_path.is_file() else {"launches": 0}
        if type(state.get("launches")) is not int or state["launches"] < 0:
            raise ValueError("Invalid persisted Experiment researcher start count")
        while not current_report(root):
            if state["launches"] >= effective_limit(root, "experiment_native", settings["agents"]["prover_max_rounds"]):
                return 2
            state["launches"] += 1
            _save(state_path, state)  # Save before launching; retries never grant new starts.
            event(root, "experiment_researcher_started", launch=state["launches"])
            try:
                run_agent("Read AGENTS.md, protocol.md and problem.md. Perform the fixed Experiment Task. "
                    "Use run_experiment/resume_experiment and retrieve every job's original result. "
                    f"The fixed target_ref is {json.dumps(fixed)}. "
                    "Conclude through submit_report with reproducible evidence or an honest inconclusive report. "
                    "Do not claim mathematical certification or change the assigned scope.",
                    root, root / "runtime" / f"experiment-{state['launches']:04d}.txt",
                    role="prover", settings=settings, extra_env={"CELL_RUN_DIR": str(root)})
            except Exception as exc:
                event(root, "experiment_researcher_error", error=f"{type(exc).__name__}: {exc}")
                return 2  # Ambiguous remote execution is recovered explicitly, never replaced.
        event(root, "empirical_report_returned")
        return 0
