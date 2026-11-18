"""Bounded Experiment Skill evaluation using the production Cell/Brain lifecycle.

prepare is offline. run is explicitly live and never starts replacement reviews.
Researcher workspaces contain neutral cases, not rubrics. A read-trace assessment
is deliberately separate: lack of detected leakage is not proof of isolation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time
import tomllib
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from colombo.configuration import load_config, resolve_document, _resolve_cell
from colombo.brain.controller import OracleController
from colombo.brain.model_calls import CodexBackend
from colombo.brain.research_store import Store
from colombo.shared.file_io import atomic_write, file_lock

FIXTURES = PROJECT / "tests/fixtures/experiment_skill_eval"
DEFAULT_ROOT = PROJECT / "validation/experiment-cell/evaluation"
BASELINE = PROJECT / "validation/experiment-cell/baseline"
BASELINE_CASES = {"S03", "S04", "S07", "S08"}
HARNESS = Path(__file__).resolve()


class EvaluationBackend(CodexBackend):
    """Production backend with only adoption-time model-launching tools removed."""
    def invoke(self, role, stage, run_root, call_id, prompt, context):
        if role == "brain" and stage == "process_results":
            prompt += ("\nEvaluation adoption only: use the already reviewed findings. No new research, "
                       "audits, direct model/API clients, new Tasks or Pruning are authorized. "
                       "Submit prunes=[]; record next research needs as future recommendations only. "
                       "The original mathematical Goal stays open; experimental completion is separate.")
        return super().invoke(role, stage, run_root, call_id, prompt, context)

    def _prepare_home(self, home, role, stage, run_root, work, call_id, settings, *, enable_mcp=True):
        result = super()._prepare_home(home, role, stage, run_root, work, call_id, settings,
                                       enable_mcp=enable_mcp)
        if enable_mcp and role == "brain" and stage == "process_results":
            path = Path(home) / "config.toml"
            text = path.read_text(encoding="utf-8")
            old_args = tomllib.loads(text)["mcp_servers"]["colombo"]["args"]
            new_args = ["-B", str(HARNESS), "serve-adoption", "--run-root", str(run_root), "--call-id", call_id]
            old_line = "args = " + json.dumps(old_args)
            if text.count(old_line) != 1:
                raise ValueError("Cannot bind evaluation adoption MCP")
            path.write_text(text.replace(old_line, "args = " + json.dumps(new_args)), encoding="utf-8")
        return result


def adoption_server(run_root, call_id):
    from colombo.brain.mcp_server import create_server
    server = create_server(run_root, "brain", "process_results", call_id)
    for name in ("audit", "job_status", "lookup"):
        server.remove_tool(name)
    return server


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    atomic_write(Path(path), (json.dumps(value, ensure_ascii=False, indent=2,
                                       allow_nan=False) + "\n").encode("utf-8"))


def inventory(root):
    root = Path(root)
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()
            and "__pycache__" not in p.parts and p.suffix != ".pyc"}


def evaluation_config(codex_bin):
    selected = load_config()
    raw = tomllib.loads((PROJECT / "config.toml").read_text(encoding="utf-8-sig"))
    raw["profile"], raw["profiles"] = "standard", {}
    model = selected["cell"]["settings"]["model"]["name"] or selected["brain"]["model"]
    if not model:
        raise ValueError("Evaluation requires an explicitly frozen model")
    for role in ("brain", "verifier", "audit"):
        raw[role].update(model=model, reasoning_effort="medium")
    raw["cell"]["settings"]["model"].update(name=model, reasoning_effort="medium")
    raw["cell"]["settings"]["agents"]["prover_max_rounds"] = 3
    raw["cell"]["settings"]["experiment"].update(max_runs=2,
        model=selected["cell"]["settings"]["experiment"]["model"], reasoning_effort="medium")
    raw["limits"].update(max_rounds=1, max_dispatches_per_wave=1, max_parallel_cells=1)
    raw["runtime"]["codex_bin"] = str(Path(codex_bin).resolve())
    resolved = resolve_document(raw, source=PROJECT / "config.toml")
    resolved["cell"] = _resolve_cell(resolved)
    resolved["cell"]["codex_bin"] = resolved["runtime"]["codex_bin"]
    if resolved["runtime"].get("auth_home"):
        resolved["cell"]["auth_home"] = resolved["runtime"]["auth_home"]
    return raw, resolved


def prepare(root, codex_bin, baseline=BASELINE):
    root = Path(root).resolve()
    if (root / "manifest.json").exists():
        raise ValueError("Evaluation already frozen; choose run/status, not prepare")
    if root.exists() and any(root.iterdir()):
        raise ValueError("Prepare requires an empty evaluation directory")
    cases, rubrics = read(FIXTURES / "cases.json"), read(FIXTURES / "rubrics.json")
    if {c["id"] for c in cases} != {f"S{i:02d}" for i in range(1, 9)}:
        raise ValueError("Expected exactly eight cases")
    if len(cases) != 8 or len(rubrics) != 8 or {r["id"] for r in rubrics} != {c["id"] for c in cases}:
        raise ValueError("Cases and evaluator rubrics must have unique matching identities")
    raw, config = evaluation_config(codex_bin)
    root.mkdir(parents=True, exist_ok=True)
    save(root / "config.input.json", raw)
    save(root / "config.snapshot.json", config)
    save(root / "fixtures/cases.json", cases)
    save(root / "fixtures/rubrics.json", rubrics)
    for label, source in (("candidate", PROJECT), ("baseline", Path(baseline))):
        shutil.copytree(source / "agents", root / "packs" / label / "agents")
    shutil.copytree(PROJECT / "src", root / "source/src", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copyfile(PROJECT / "run.py", root / "source/run.py")
    shutil.copyfile(PROJECT / "requirements.txt", root / "source/requirements.txt")
    shutil.copyfile(HARNESS, root / "source/evaluate_experiment_skills.py")
    keys = [f"candidate-{c['id']}" for c in cases]
    keys += [f"baseline-{c['id']}" for c in cases if c["id"] in BASELINE_CASES]
    manifest = {"schema_version": 1, "created_at": time.time(), "keys": keys,
        "limits": {"research_tasks": 12, "starts_per_task": 3, "hosted_per_task": 2,
                   "reviews_per_task": 1, "brain_updates": 2, "concurrency": 1},
        "runtime_source": inventory(PROJECT / "src"),
        "candidate_source": inventory(PROJECT / "agents"),
        "packs": {name: inventory(root / "packs" / name) for name in ("candidate", "baseline")},
        "fixture_hashes": inventory(root / "fixtures"),
        "source_snapshot": inventory(root / "source"),
        "entrypoint_sha256": hashlib.sha256((PROJECT / "run.py").read_bytes()).hexdigest(),
        "harness_sha256": hashlib.sha256(HARNESS.read_bytes()).hexdigest(),
        "config_sha256": hashlib.sha256((root / "config.snapshot.json").read_bytes()).hexdigest()}
    save(root / "manifest.json", manifest)
    save(root / "ledger.json", {key: {"state": "prepared", "research_attempted": False,
        "review_attempted": False, "update_attempted": False} for key in keys})
    return manifest


def verify_frozen(root):
    manifest = read(root / "manifest.json")
    for name, source in (("runtime_source", PROJECT / "src"), ("candidate_source", PROJECT / "agents")):
        if inventory(source) != manifest[name]:
            raise ValueError(f"{name} changed after evaluation freeze")
    if inventory(root / "fixtures") != manifest["fixture_hashes"]:
        raise ValueError("Frozen evaluation fixtures changed")
    if inventory(root / "source") != manifest["source_snapshot"]:
        raise ValueError("Frozen runtime/harness snapshot changed")
    if hashlib.sha256(HARNESS.read_bytes()).hexdigest() != manifest["harness_sha256"]:
        raise ValueError("Evaluation harness changed after freeze")
    if hashlib.sha256((PROJECT / "run.py").read_bytes()).hexdigest() != manifest["entrypoint_sha256"]:
        raise ValueError("Runtime entrypoint changed after freeze")
    for name, expected in manifest["packs"].items():
        if inventory(root / "packs" / name) != expected:
            raise ValueError("Frozen instruction pack changed")
    if hashlib.sha256((root / "config.snapshot.json").read_bytes()).hexdigest() != manifest["config_sha256"]:
        raise ValueError("Frozen evaluation config changed")
    return manifest


def install_snapshot(cell, snapshot):
    """Select frozen pack before the first model launch; keep runtime handoff."""
    import colombo.cell.instructions as instructions
    cell = Path(cell).resolve()
    if (cell / "runtime/experiment_state.json").exists():
        raise ValueError("Cannot replace instructions after researcher starts")
    with tempfile.TemporaryDirectory(prefix=".eval-pack-", dir=cell.parent) as tmp:
        stage = Path(tmp)
        with patch.object(instructions, "ROOT", snapshot):
            instructions.install_cell_pack(stage, instructions.validate_mode("oracle_complexity", "experiment"))
        handoff = cell / ".agents/skills/handoff"
        if handoff.exists() and not (stage / ".agents/skills/handoff").exists():
            shutil.copytree(handoff, stage / ".agents/skills/handoff")
        for relative in ("skills", ".agents/skills"):
            target = (cell / relative).resolve()
            if not target.is_relative_to(cell) or target == cell:
                raise ValueError("Invalid pack replacement target")
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(stage / relative, target)
        for name in ("AGENTS.md", "protocol.md"):
            shutil.copyfile(stage / name, cell / name)


def make_controller(root, key, case):
    config = read(root / "config.snapshot.json")
    run_root = root / "runs" / key
    if not (run_root / "state.sqlite").exists():
        public = root / "inputs" / key
        public.mkdir(parents=True, exist_ok=True)
        paths = []
        for name, text in case["files"].items():
            target = public / name
            target.write_text(text, encoding="utf-8")
            paths.append(target)
        goal = "Investigate the fixed experimental question and identify the remaining mathematical research obligation. " + case["question"]
        store = Store.create(run_root, goal, [], config, materials=paths)
        setting = {"specification": case["setting"], "provenance": [{"entry": "case Setting",
            "source": "Fixed evaluation assignment", "status": "provided"}],
            "unknowns": [], "near_optimal_policy": "No mathematical certification from empirical evidence."}
        sref = store.write_record("setting", setting, request_id="setting:initial")
        save(run_root / "input/setting.json", setting)
        store.set_meta(setting_ref=sref, planning_wave=1)
        spec = {"title": case["title"], "instructions": case["instructions"],
            "deliverables": ["Self-contained empirical report and traceable supporting artifacts"],
            "completion_criteria": case["completion_criteria"], "mode": "new", "resume_task_id": None,
            "specialization": "experiment", "package": {"background": "Fixed research material; assess its claims independently.",
                "selection_reason": "All supplied inputs are relevant to this question.", "items": [
                    {"ref": ref["id"], "importance": "required", "purpose": "Supplied research material",
                     "limitations": "Supplied claims are unreviewed; inspect actual contents."}
                    for ref in store.get_meta("material_refs", [])]},
            "responsibility": {"problem_id": "study", "claim": case["question"], "assumptions": [],
                "scope": "The supplied Setting", "goal_ids": ["G0"], "proof_step_ids": [],
                "route_group": "", "retain": True}}
        pref = store.write_record("plan", {"rationale": "One explicitly assigned evaluation Task; no automatic research dispatch.",
            "tasks": [spec]}, request_id="evaluation-plan")
        jobs = store.plan_jobs(pref)
        store.set_meta(round_no=1, round_data={"round_no": 1, "plan_ref": pref, "jobs": jobs}, phase="preparing")
    controller = OracleController(PROJECT, run_root, backend=EvaluationBackend(PROJECT, config))
    controller._initialize_proof()
    task = controller.store.get_task("T0001")
    if not task or not task.get("package_ref"):
        controller.tasks.prepare()
    if not (run_root / "installed_pack.json").exists():
        install_snapshot(run_root / "tasks/T0001/cell", root / "packs" / key.split("-")[0])
        save(run_root / "installed_pack.json", inventory(run_root / "tasks/T0001/cell/skills"))
    return controller


def review_prompt(rubric):
    return (
        "Perform the normal independent empirical Result review. Read the fixed assignment, Setting, "
        "actual code/data/receipts and all evidence needed for the claims. Confirm only empirical Claims "
        "with frozen evidence paths; never certify general mathematics. A reliable scientific inconclusive "
        "can pass and complete the experimental responsibility. Do not repair the research or launch research Tasks. "
        "The following is evaluator-only acceptance guidance, not evidence. Check it against actual artifacts. "
        "Do not rubber-stamp expected answers. Use the normal review schema and write_review MCP. "
        "For this evaluation only, make summary a JSON-encoded object (a string in the normal schema) with "
        "keys finding (scoped text), criteria (array of {id, verdict: pass|fail|unresolved, reason, evidence_paths}), "
        "fatal_errors (array of text), case_grade (pass|fail|incomplete). Include every criterion. "
        "Every criteria[].evidence_paths entry must be copied verbatim from Result.artifacts[*].path; "
        "do not use original input paths, aliases or fragments, even for identical content. "
        "A pass needs all criteria supported and no fatal errors. Keep confirmed_claims as actual research "
        "findings, not scoring labels. Missing evidence is unresolved. No extra reviewer retry will be run.\n" +
        json.dumps(rubric, ensure_ascii=False))


def parse_grade(review, rubric, allowed_paths):
    """Validate structure and evidence identity; scientific judgment stays with reviewer."""
    try:
        grade = json.loads(review["summary"])
        if not isinstance(grade, dict) or not isinstance(grade.get("finding"), str) or not grade["finding"].strip():
            raise ValueError("Missing scoped finding")
        rows = grade["criteria"]
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise ValueError("Invalid criteria array")
        expected = {c["id"] for c in rubric["criteria"]}
        if len(rows) != len(expected) or {c["id"] for c in rows} != expected:
            raise ValueError("Incomplete criterion judgments")
        for row in rows:
            if row["verdict"] not in {"pass", "fail", "unresolved"} or not row.get("reason"):
                raise ValueError("Invalid criterion judgment")
            if not isinstance(row.get("evidence_paths"), list) or not set(row["evidence_paths"]) <= allowed_paths:
                raise ValueError("Criterion evidence outside frozen Result")
            if row["verdict"] == "pass" and not row["evidence_paths"]:
                raise ValueError("Passing criterion lacks evidence")
        if grade["case_grade"] not in {"pass", "fail", "incomplete"} or not isinstance(grade["fatal_errors"], list):
            raise ValueError("Invalid overall grade")
        if grade["case_grade"] == "pass" and (grade["fatal_errors"] or any(c["verdict"] != "pass" for c in rows)
                or review["verdict"] != "pass" or review["completion_status"] != "completed"):
            raise ValueError("Passing grade conflicts with review")
        return {**grade, "status": "graded"}
    except (ValueError, TypeError, KeyError) as exc:
        return {"status": "ungraded", "case_grade": "incomplete", "reason": str(exc)}


def trace_summary(cell):
    logs = sorted(Path(cell).glob("runtime/*.events.jsonl"))
    rows, usage, suspicious = [], [], []
    for path in logs:
        for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            try:
                event = json.loads(line)
            except ValueError:
                continue
            item = event.get("item", {})
            if event.get("usage"):
                usage.append({"log": str(path), "line": line_number, "usage": event["usage"]})
            if item.get("type") in {"command_execution", "mcp_tool_call", "web_search", "file_change"}:
                row = {"log": str(path), "line": line_number, "item": item}
                rows.append(row)
                text = json.dumps(item).lower()
                if any(marker in text for marker in ("rubrics.json", "grader notes", "expected_answers", "experiment_skill_eval")):
                    suspicious.append(row)
    return {"status": "unknown", "reason": "Workspace-write is not read isolation; human review of actual reads is required.",
            "logs": [str(p) for p in logs], "tool_events": rows, "suspicious_events": suspicious, "usage": usage}


def recover_committed_call(controller, role, stage):
    """Read only the already committed original call; never authorize a retry."""
    pending = controller.store.get_meta("pending_call")
    if not pending or pending.get("role") != role or pending.get("stage") != stage:
        raise RuntimeError("Original call cannot be identified; call cap forbids replacement")
    if not pending.get("response_ref"):
        outcome = controller.calls.backend.reconcile_call(controller.root, pending["call_id"])
        if outcome.get("state") != "submitted":
            raise RuntimeError("Original call has no committed response; call cap forbids replacement")
        controller._call(role, stage, pending["prompt"], pending["context"])
    return controller.store.get_meta("pending_call")["response_ref"]


def usage_summary(run_root):
    run_root = Path(run_root)
    cell = run_root / "tasks/T0001/cell"
    state = cell / "runtime/experiment_state.json"
    executions = []
    for path in sorted(cell.glob("experiments/exp-*/state.json")):
        if (path.parent / "plan.json").is_file():
            execution = read(path)["execution"]
            executions.append({"id": path.parent.name, **{k: execution.get(k) for k in
                ("status", "model", "started_at", "completed_at", "reason", "usage")}})
    calls = [read(p) for p in sorted(run_root.glob("brain/calls/*/call.json"))]
    return {"native_starts_reserved": read(state).get("launches", 0) if state.exists() else 0,
            "native_starts_launched": len(list(cell.glob("runtime/research_starts/*.json"))),
            "hosted_runs_reserved": len(executions), "hosted_runs": executions,
            "outer_calls": [{k: call.get(k) for k in ("call_id", "role", "stage", "status", "started_at", "ended_at")}
                            for call in calls]}


def read_audit_status(root, key):
    """A human read-trace audit must bind every current researcher log by hash."""
    logs = sorted((root / "runs" / key / "tasks/T0001/cell").glob("runtime/*.events.jsonl"))
    hashes = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in logs}
    path = root / "read-audits" / (key + ".json")
    if not path.is_file():
        return {"status": "unknown", "reason": "No completed read-trace audit", "required_logs": hashes}
    audit = read(path)
    if (audit.get("status") not in {"clean", "contaminated", "unknown"}
            or not audit.get("reviewer") or not audit.get("reason")
            or not hashes or audit.get("inspected_logs") != hashes):
        return {"status": "unknown", "reason": "Audit does not bind all current researcher logs", "required_logs": hashes}
    return {"status": audit["status"], "reason": audit["reason"], "reviewer": audit["reviewer"], "required_logs": hashes}


def summarize(root):
    """Read-only summary; never launches or retries anything and never fills missing grades."""
    root = Path(root).resolve()
    manifest, ledger = read(root / "manifest.json"), read(root / "ledger.json")
    rows = []
    for key in manifest["keys"]:
        entry = ledger[key]
        audit = read_audit_status(root, key)
        usage = usage_summary(root / "runs" / key)
        grade_path = root / "grades" / (key + ".json")
        grade = read(grade_path) if grade_path.is_file() else {"status": "ungraded", "case_grade": "incomplete"}
        held_out = key.split("-")[1] in BASELINE_CASES
        passed = entry.get("state") == "finished" and grade.get("status") == "graded" and grade.get("case_grade") == "pass"
        adoption = entry.get("mathematical_goal_preserved") if key in {"candidate-S01", "candidate-S02"} else None
        rows.append({"key": key, "state": entry["state"], "behavioral_grade": grade.get("case_grade"),
            "grade_status": grade.get("status"), "read_audit": audit,
            "held_out_success": held_out and passed and audit["status"] == "clean",
            "adoption_boundary_pass": adoption, "usage": usage,
            "reason": entry.get("reason")})
    totals = {"research_tasks_attempted": sum(bool(e["research_attempted"]) for e in ledger.values()),
        "native_starts_reserved": sum(r["usage"]["native_starts_reserved"] for r in rows),
        "native_starts_launched": sum(r["usage"]["native_starts_launched"] for r in rows),
        "hosted_runs_reserved": sum(r["usage"]["hosted_runs_reserved"] for r in rows),
        "review_attempts": sum(bool(e["review_attempted"]) for e in ledger.values()),
        "brain_update_attempts": sum(bool(e["update_attempted"]) for e in ledger.values())}
    violations = [r["key"] for r in rows if r["usage"]["native_starts_reserved"] > 3 or r["usage"]["hosted_runs_reserved"] > 2]
    return {"limits": manifest["limits"], "totals": totals, "budget_violations": violations, "cases": rows,
            "interpretation": "Finite behavioral checks; unknown/contaminated read traces never count as held-out success."}


def run_one(root, key):
    root = Path(root).resolve()
    manifest = verify_frozen(root)
    if key not in manifest["keys"]:
        raise ValueError("Key is not an authorized evaluation Task")
    cases = {c["id"]: c for c in read(root / "fixtures/cases.json")}
    rubrics = {c["id"]: c for c in read(root / "fixtures/rubrics.json")}
    case, rubric = cases[key.split("-")[1]], rubrics[key.split("-")[1]]
    with file_lock(root / ".live.lock", timeout=1, poll_seconds=0.1):
        ledger = read(root / "ledger.json")
        entry = ledger[key]
        if entry.get("state") == "finished":
            return entry
        controller = make_controller(root, key, case)
        store = controller.store
        controller._start_budget()
        try:
            job = store.get_meta("round_data")["jobs"][0]
            task = store.get_task("T0001")
            if not task.get("latest_result_ref"):
                entry.update(state="researching", research_attempted=True, research_started_at=time.time())
                save(root / "ledger.json", ledger)
                result_ref = controller.tasks.run_job(job)
            else:
                result_ref = task["latest_result_ref"]
            entry["result_ref"] = result_ref
            result = store.read_record(result_ref)
            cell = store.root / "tasks/T0001/cell"
            save(root / "traces" / (key + ".json"), trace_summary(cell))
            if not result.get("empirical_report"):
                entry.update(state="incomplete", reason="No empirical report returned", execution_status=result.get("execution_status"))
                return entry
            rid = result_ref["id"]
            review_ref = store.get_meta("result_reviews", {}).get(rid)
            if not review_ref:
                if entry["review_attempted"]:
                    # Reconcile a committed original response only. Never reserve a replacement.
                    review_ref = recover_committed_call(controller, "verifier", "verify-progress")
                else:
                    package = controller._review_package(result_ref=result_ref)
                    pref = store.write_record("review_package", package, request_id="result-package:" + rid)
                    entry.update(review_attempted=True, state="reviewing")
                    save(root / "ledger.json", ledger)
                    store.set_meta(phase="result_reviewing", processing_result={"result_ref": result_ref,
                        "task_id": "T0001", "attempt_id": "A0001"}, result_review_package=pref, pending_call=None)
                    controller._call("verifier", "verify-progress", review_prompt(rubric),
                        {"review_package_ref": pref, "review_kind": "result"})
                    review_ref = store.get_meta("pending_call")["response_ref"]
                store.set_meta(result_reviews={rid: review_ref}, pending_call=None, phase="processing_results")
            review = store.read_record(review_ref)
            entry["review_ref"] = review_ref
            grade = parse_grade(review, rubric, {a["path"] for a in result.get("artifacts", [])})
            save(root / "grades" / (key + ".json"), grade)
            entry.update(grade=grade["case_grade"], grade_status=grade["status"], contamination="unknown",
                         held_out_success=False)
            if key in {"candidate-S01", "candidate-S02"} and rid not in store.get_meta("processed_results", []):
                if entry["update_attempted"]:
                    recover_committed_call(controller, "brain", "process_results")
                entry.update(update_attempted=True, state="updating")
                save(root / "ledger.json", ledger)
                # One real production update. Never call controller.run(), _plan or integrate.
                controller._process_results()
                entry["progress_ref"] = store.get_meta("progress_ref")
                progress = store.read_record(entry["progress_ref"])["progress"]
                entry["mathematical_goal_preserved"] = progress["status"] != "completed" and not progress["bracket"]["bounds"]
            entry.update(state="finished", finished_at=time.time())
            return entry
        except Exception as exc:
            entry.update(state="incomplete", error_type=type(exc).__name__, reason=str(exc), failed_at=time.time())
            raise
        finally:
            cell = store.root / "tasks/T0001/cell"
            save(root / "traces" / (key + ".json"), trace_summary(cell))
            entry["usage"] = usage_summary(store.root)
            save(root / "ledger.json", ledger)
            controller._pause_budget()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "run", "status", "summarize", "serve-adoption"))
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--codex-bin", help="Explicit native executable; required for prepare")
    parser.add_argument("--key", help="One frozen key; omitted run processes all remaining keys serially")
    parser.add_argument("--live", action="store_true", help="Explicitly permit approved model/API evaluation")
    parser.add_argument("--run-root", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--call-id", help=argparse.SUPPRESS)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.action == "serve-adoption":
        if not args.run_root or not args.call_id:
            parser.error("serve-adoption requires a real bound run and call")
        adoption_server(args.run_root, args.call_id).run(transport="stdio")
    elif args.action == "prepare":
        if not args.codex_bin:
            parser.error("prepare requires --codex-bin")
        value = prepare(root, args.codex_bin, args.baseline)
        print(json.dumps({"state": "prepared", "tasks": value["keys"], "root": str(root)}, ensure_ascii=False))
    elif args.action == "status":
        print(json.dumps(read(root / "ledger.json"), indent=2, ensure_ascii=False))
    elif args.action == "summarize":
        print(json.dumps(summarize(root), indent=2, ensure_ascii=False))
    else:
        if not args.live:
            parser.error("run requires --live; prepare/status never launch a model")
        keys = [args.key] if args.key else read(root / "manifest.json")["keys"]
        for key in keys:
            print(json.dumps({"starting": key}), flush=True)
            try:
                print(json.dumps({"key": key, "result": run_one(root, key)}, ensure_ascii=False), flush=True)
            except Exception as exc:
                print(json.dumps({"key": key, "state": "incomplete", "error_type": type(exc).__name__,
                                  "reason": str(exc)}, ensure_ascii=False), flush=True)
                # Unknown/infrastructure failures need reconciliation, not batch-wide repeat costs.
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
