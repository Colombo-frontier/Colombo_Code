from __future__ import annotations
import argparse
from datetime import datetime
import json
import sys
import uuid
from colombo.configuration import PROJECT_ROOT, load_config, require_current_workflow
from colombo.brain.research_store import Store
from colombo.brain.research_records import state_view
from colombo.brain.mcp_server import serve
from colombo.shared.file_io import Path


def adopt_current_policy(store):
    """Adopt the single source at a quiescent resume boundary, never reset usage."""
    saved = store.get_meta("config")
    # Budget policy adoption cannot upgrade a historical research protocol.
    require_current_workflow(saved)
    source = saved.get("policy_metadata", {}).get("source")
    current = load_config(source)
    if current == saved:
        return
    with store.exclusive():
        from colombo.shared.tool_jobs import pending_jobs
        if store.get_meta("pending_call") or store.unresolved_audits():
            raise ValueError("Resolve the pending model call/audit before adopting the updated config; saved policy and counters were retained")
        if pending_jobs(store.root):
            raise ValueError("Active tool jobs must finish or be reconciled before adopting the updated config")
        if any(task.get("state") in {"running", "stopping"} for task in store.list_tasks()):
            raise ValueError("Active Cell executions must finish or be reconciled before adopting the updated config")
        from colombo.shared.file_io import freeze_json
        revision = current["policy_metadata"]["revision"]
        freeze_json(store.root / "config_revisions" / (revision + ".json"), current)
        store.set_meta(config=current)
        store.event("config_policy_adopted", previous=saved.get("policy_metadata"),
                    current=current["policy_metadata"], counters_preserved=True,
                    historical_active_time_recorded=(store.root / "runtime/budget.json").is_file())


def main(argv=None):
    parser = argparse.ArgumentParser(description="Colombo: Oracle Complexity Brain and specialized Cells")
    commands = parser.add_subparsers(dest="command", required=True)
    new = commands.add_parser("run", help="Create and run a new programme")
    new.add_argument("goal", type=Path)
    new.add_argument("--criterion", action="append", default=[])
    new.add_argument("--material", action="append", type=Path, default=[])
    new.add_argument("--config", type=Path)
    new.add_argument("--run-dir", type=Path)
    new.add_argument("--prepare-only", action="store_true", help="Freeze input without calling any model")
    new.add_argument("--research-mode", choices=["oracle_complexity"],
                     help="Colombo is dedicated to Oracle Complexity")
    preview = commands.add_parser("config", help="Preview resolved parameters without creating a run or calling models")
    preview.add_argument("--config", type=Path, help="Select one complete configuration file; no overlay merging")
    for name in ("status", "resume", "reconcile-final-review"):
        cmd = commands.add_parser(name)
        cmd.add_argument("--run-dir", required=True, type=Path)
    mcp = commands.add_parser("mcp", help=argparse.SUPPRESS)
    mcp.add_argument("--run-dir", required=True, type=Path)
    mcp.add_argument("--role", choices=["brain", "verifier"], required=True)
    mcp.add_argument("--stage", required=True)
    mcp.add_argument("--call-id", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "config":
            config = load_config(args.config)
            print(json.dumps({"mode": "preview_only", "creates_run": False,
                "default_file": str(PROJECT_ROOT / "config.toml"),
                "selected_file": config.get("policy_metadata", {}).get("source"),
                "profile": config.get("profile"),
                "cell_resolution_order": ["single complete config", "selected root profile differences", "derived immutable settings"],
                "notes": [
                    "profile selects standard base settings or hard differences in this file.",
                    "Research is limited by Waves and per-Wave dispatches; concurrency is independent.",
                    "No whole-run research deadline or outer model-call/Assessment cap is applied.",
                    "integration.timeout_seconds limits each final integrate + Verifier stage, including its retries.",
                    "Cell-local counts, resource limits and infrastructure waits remain in force; usage is retained on resume.",
                    "Empty model/effort values inherit existing native CLI defaults at launch.",
                    "This preview does not create or modify a run, reset counters, or launch a model."],
                "effective_config": config}, ensure_ascii=False, indent=2))
            return 0
        if args.command == "mcp":
            serve(args.run_dir, args.role, args.stage, args.call_id)
            return 0
        if args.command == "run":
            config = load_config(args.config)
            if args.research_mode is not None:
                config = {**config, "research_mode": args.research_mode}
            root = args.run_dir or PROJECT_ROOT / "runs" / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6])
            store = Store.create(root, args.goal.read_text(encoding="utf-8-sig"), args.criterion, config, args.material)
            if args.prepare_only:
                print(json.dumps({"run_dir": str(store.root), **state_view(store)}, ensure_ascii=False, indent=2))
                return 0
        else:
            if not (args.run_dir / "state.sqlite").is_file():
                raise ValueError("Not an existing Colombo run: state.sqlite is missing")
            store = Store(args.run_dir)
        if args.command == "status":
            from colombo.brain.research_records import export_research
            export_research(store)
            print(json.dumps(state_view(store), ensure_ascii=False, indent=2))
            return 0
        if args.command == "reconcile-final-review":
            require_current_workflow(store.get_meta("config"))
            from colombo.brain.final_report import reconcile_completed_run
            ref = reconcile_completed_run(store)
            print(json.dumps({"run_dir": str(store.root), "status": store.get_meta("status"),
                              "conclusion_ref": ref, "proof_ref": store.get_meta("proof_ref"),
                              "final_review_ref": store.get_meta("final_review_ref")}, ensure_ascii=False, indent=2))
            return 0 if store.get_meta("status") == "completed" else 2
        if args.command == "resume":
            adopt_current_policy(store)
        require_current_workflow(store.get_meta("config"))
        from colombo.brain.controller import OracleController as Controller
        result = Controller(PROJECT_ROOT, store.root).run()
        print(json.dumps({"run_dir": str(store.root), **result}, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "completed" else 2
    except KeyboardInterrupt:
        print("Interrupted; committed work is retained. Use resume.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
