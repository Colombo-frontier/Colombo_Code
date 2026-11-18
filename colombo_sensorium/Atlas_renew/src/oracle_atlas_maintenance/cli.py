"""Reviewable ordered maintenance plans with explicit native publication commands."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tomllib

from .engine import Maintenance, Inventory
from .audit import audit_inventory, create_draft, outside_atlas, validate_files
from .state import write_json


def load_config(path):
    path = Path(path).resolve()
    config = tomllib.loads(path.read_text("utf-8"))
    for field in ("atlas", "workspace"):
        if not isinstance(config.get(field), str) or not config[field]:
            raise ValueError(f"Configure {field} as a nonempty filesystem path")
        config[field] = str((path.parent / config[field]).resolve())
    if config.get("backend", "codex") not in {"codex", "responses"}:
        raise ValueError("backend must be codex or responses")
    config.setdefault("backend", "codex")
    for key, value in config.get("budgets", {}).items():
        if key in {"adaptive_input_budget", "adaptive_tool_budget", "reserve_control_calls", "finite_research_scope", "source_recovery"}:
            if not isinstance(value, bool):
                raise ValueError(f"Budget {key} must be boolean")
            continue
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"Budget {key} must be a positive integer")
    for key in ("min_recheck_days", "overlap_days"):
        value = config.get("maintenance", {}).get(key, 14 if key == "min_recheck_days" else 30)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"maintenance.{key} must be a nonnegative integer")
    workers = config.get("execution", {}).get("max_workers", 1)
    if isinstance(workers, bool) or not isinstance(workers, int) or not 1 <= workers <= 64:
        raise ValueError("execution.max_workers must be an integer from 1 to 64")
    literature = config.get("literature", {})
    for key in ("max_bytes", "max_source_file_bytes", "max_source_download_bytes", "max_source_download_attempts"):
        value = literature.get(key)
        if value is not None and (isinstance(value, bool) or not isinstance(value, int) or value < 1):
            raise ValueError(f"literature.{key} must be a positive integer")
    if literature.get("max_source_file_bytes", literature.get("max_bytes", 20000000)) < literature.get("max_bytes", 20000000):
        raise ValueError("literature.max_source_file_bytes must cover the initial max_bytes allowance")
    replacements = literature.get("max_source_replacements", 2)
    if isinstance(replacements, bool) or not isinstance(replacements, int) or not 0 <= replacements <= 2:
        raise ValueError("literature.max_source_replacements must be an integer from zero to two")
    for key, maximum in (("max_source_file_bytes", 80000000), ("max_source_download_bytes", 160000000), ("max_source_download_attempts", 16)):
        if literature.get(key, maximum) > maximum:
            raise ValueError(f"literature.{key} exceeds the recovery hard policy {maximum}")
    atlas_root, workspace = Path(config["atlas"]), Path(config["workspace"])
    data = atlas_root / "data" if (atlas_root / "data" / "settings").is_dir() else atlas_root
    if workspace.is_relative_to(data / "settings") or workspace == atlas_root:
        raise ValueError("Keep the maintenance workspace separate from native setting directories")
    return config


def main(argv=None):
    parser = argparse.ArgumentParser(description="Maintain existing Atlas brackets with a frozen bounded concurrent queue")
    parser.add_argument("--config", required=True, help="TOML configuration (paths relative to this file)")
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan", help="Freeze existing IDs and versions without model calls or Atlas writes")
    plan.add_argument("--ids", help="JSON array of existing setting IDs in the exact requested order")
    plan.add_argument("--cutoff", help="Research cutoff, YYYY-MM-DD; defaults to configured local date")
    plan.add_argument("--force", action="store_true", help="Check even recently completed settings")
    plan_review = commands.add_parser("plan-review", help="Plan fresh independent review of pinned original unapproved scout candidates; no new scout call")
    plan_review.add_argument("--source-run", required=True, help="Original run in this same workspace")
    plan_review.add_argument("--ids", required=True, help="JSON array of exact existing setting IDs")
    plan_review.add_argument("--cutoff", help="Optional assertion; must equal the original scout cutoff")
    run = commands.add_parser("run", help="Resume bounded concurrent screening and independent review")
    run.add_argument("run_id")
    run.add_argument("--jobs", type=int, help="Concurrent settings, at most execution.max_workers; each role retains independent sessions")
    run.add_argument("--limit", type=int, help="Maximum settings attempted in this invocation")
    run.add_argument("--retry-incomplete", action="store_true", help="Explicitly start a new attempt for errors/incomplete items; may incur new model calls")
    run.add_argument("--commit", action="store_true", help="Publish independently approved deltas through native five-file transactions")
    checkpoint = commands.add_parser("checkpoint", help="Inspect a stopped attempt's verified breakpoint without model calls")
    checkpoint.add_argument("run_id")
    checkpoint.add_argument("--setting", required=True, help="One existing setting in that frozen run")
    reconcile = commands.add_parser("reconcile-startup", help="Read-only verify a known pre-model startup failure and append an audited budget correction; no model call")
    reconcile.add_argument("run_id")
    reconcile.add_argument("--setting", required=True)
    reconcile.add_argument("--evidence", help="Optional operator-reviewed hash snapshot inside this workspace when filesystem ctime is unreliable")
    reconcile.add_argument("--evidence-sha256", help="Explicit SHA256 approval of the exact operator snapshot")
    continuation = commands.add_parser("continue", help="Explicitly start one new paid-capable attempt from a verified unapproved breakpoint")
    continuation.add_argument("run_id")
    continuation.add_argument("--setting", required=True, help="One stopped error/incomplete setting; all original bindings must match")
    continuation.add_argument("--commit", action="store_true", help="Allow publication only after a fresh independent review passes all gates")
    status = commands.add_parser("status")
    status.add_argument("run_id")
    apply = commands.add_parser("apply", help="Publish previously frozen, independently approved staged bundles")
    apply.add_argument("run_id")
    apply.add_argument("--setting", help="Apply only this existing setting ID")
    audit = commands.add_parser("audit", help="Read-only joint-parameter preflight; no model calls or Atlas writes")
    audit.add_argument("--ids", help="Optional JSON array of existing IDs")
    audit.add_argument("--output", help="Save full report outside the Atlas")
    draft = commands.add_parser("draft-analysis", help="Create an unreviewed joint-analysis draft outside the Atlas")
    draft.add_argument("--setting", required=True)
    draft.add_argument("--out", required=True)
    validate = commands.add_parser("validate-analysis", help="Structural/reference checks only; not scientific approval")
    validate.add_argument("--profile", required=True)
    validate.add_argument("--analysis")
    validate.add_argument("--baseline")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        if args.command in {"audit", "draft-analysis", "validate-analysis"}:
            inventory = Inventory(config["atlas"])
            if args.command == "audit":
                ids = json.loads(Path(args.ids).read_text()) if args.ids else None
                result = audit_inventory(inventory, ids)
                if args.output:
                    destination = outside_atlas(args.output, inventory)
                    write_json(destination, result)
                    result = {key: value for key, value in result.items() if key != "profiles"}
                    result["output"] = str(destination)
            elif args.command == "draft-analysis":
                result = create_draft(inventory, args.setting, args.out)
            else:
                result = validate_files(args.profile, args.analysis, args.baseline)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        controller = Maintenance(config)
        if args.command == "plan":
            ids = json.loads(Path(args.ids).read_text()) if args.ids else None
            if ids is not None and (not isinstance(ids, list) or any(not isinstance(sid, str) for sid in ids)):
                raise ValueError("--ids must be a JSON array of existing ID strings")
            result = controller.plan(ids=ids, cutoff=args.cutoff, force=args.force)
        elif args.command == "plan-review":
            ids = json.loads(Path(args.ids).read_text())
            if not isinstance(ids, list) or any(not isinstance(sid, str) for sid in ids):
                raise ValueError("--ids must be a JSON array of existing ID strings")
            result = controller.plan_review(source_run=args.source_run, ids=ids, cutoff=args.cutoff)
        elif args.command == "run":
            result = controller.run(args.run_id, limit=args.limit, retry_incomplete=args.retry_incomplete, commit=args.commit, jobs=args.jobs)
        elif args.command == "checkpoint":
            result = controller.checkpoint(args.run_id, setting_id=args.setting)
        elif args.command == "reconcile-startup":
            result = controller.reconcile_startup(args.run_id, setting_id=args.setting,
                                                  evidence_snapshot=args.evidence, evidence_sha256=args.evidence_sha256)
        elif args.command == "continue":
            result = controller.continue_run(args.run_id, setting_id=args.setting, commit=args.commit)
        elif args.command == "apply":
            result = controller.apply(args.run_id, setting_id=args.setting)
        else:
            controller.state.plan(args.run_id)
            result = controller.state.summary(args.run_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, RuntimeError) as exc:
        print(json.dumps({"error_type": type(exc).__name__, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
