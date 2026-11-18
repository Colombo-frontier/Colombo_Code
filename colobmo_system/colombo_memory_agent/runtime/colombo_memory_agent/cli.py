"""Trusted operator commands for the independent Memory Agent."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from colombo.memory.contracts import ContractError
from colombo.project_paths import PROJECT_ROOT as CORE_ROOT
from .store import Store, read_json

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="colombo-memory-agent")
    p.add_argument("--root", type=Path, default=CORE_ROOT / "long_term_memory",
                   help="Scientific memory root; defaults to the parent system's long_term_memory")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    a = sub.add_parser("install-leads"); a.add_argument("file", type=Path)
    a = sub.add_parser("stage"); a.add_argument("file", type=Path); a.add_argument("--curator-run-id", required=True); a.add_argument("--job-id", required=True)
    a = sub.add_parser("publish"); a.add_argument("proposal_id"); a.add_argument("review", type=Path); a.add_argument("--authorized", action="store_true")
    a = sub.add_parser("run-job"); a.add_argument("file", type=Path)
    a.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parents[2])
    a.add_argument("--jobs-root", type=Path, help="Execution logs and snapshots; defaults to the Agent's jobs directory")
    a.add_argument("--model"); a.add_argument("--reviewer-model"); a.add_argument("--codex", default="codex"); a.add_argument("--timeout", type=int, default=900); a.add_argument("--resume", action="store_true")
    args = p.parse_args(argv)
    try:
        store = Store(args.root)
        if args.command == "init":
            result = store.initialize()
        elif args.command == "install-leads":
            result = store.install_leads(read_json(args.file))
        elif args.command == "stage":
            result = store.prepare(read_json(args.file), curator_run_id=args.curator_run_id, job_id=args.job_id)
        elif args.command == "publish":
            result = store.publish(store.load_proposal(args.proposal_id), read_json(args.review), authorized=args.authorized)
        else:
            from .backend import CodexBackend
            from .workflow import Workflow
            result = Workflow(store, CodexBackend(model=args.model, reviewer_model=args.reviewer_model, executable=args.codex, timeout=args.timeout), args.package_root, jobs_root=args.jobs_root).run(read_json(args.file), resume=args.resume)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command == "run-job" and result.get("status") not in {
            "completed", "completed_with_deferred_items"
        }:
            return 2
        return 0
    except (ContractError, KeyError, ValueError, OSError, TypeError) as exc:
        print(json.dumps({"error": str(exc), "type": type(exc).__name__}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
