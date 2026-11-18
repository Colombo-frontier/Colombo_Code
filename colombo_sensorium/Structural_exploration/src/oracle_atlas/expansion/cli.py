"""Standalone neighborhood-discovery entry point, sharing the installed Atlas runtime."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ..cli import LazyBackend, doctor, export_case, import_source, print_json
from ..core.config import load_config, resources_root
from ..core.contracts import ProtocolError
from ..core.store import atomic_json
from .engine import ExpansionEngine


def build_parser(*, prog="oracle-atlas-expand"):
    parser = argparse.ArgumentParser(prog=prog, description="Discover finite portfolios of Atlas settings through explicit structural transformations")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create an expansion configuration; the Atlas is not modified")
    init.add_argument("--config", default="expansion.local.toml")
    init.add_argument("--atlas", required=True)
    init.add_argument("--workspace", default="./expansion_work")
    init.add_argument("--backend", choices=["codex", "responses"], default="codex")
    init.add_argument("--model", default="")
    for name in ("doctor", "plan", "run", "resume", "status", "export", "publish", "import-source"):
        command = commands.add_parser(name)
        command.add_argument("--config", required=True)
        if name in {"plan", "run"}:
            command.add_argument("--request", required=True, help="JSON with explicit finite discovery scope; unspecified limits use documented defaults")
            if name == "run":
                command.add_argument("--candidates-only", action="store_true", help="Stop after candidate reviews and identity matching")
        elif name == "resume":
            group = command.add_mutually_exclusive_group(required=True)
            group.add_argument("--batch-id"); group.add_argument("--case-id"); group.add_argument("--job-id")
            command.add_argument("--stage", choices=["specification", "identity", "research"])
            command.add_argument("--material-ref", action="append", default=[])
            command.add_argument("--material-file", action="append", default=[])
            command.add_argument("--retry-transport", action="store_true")
            command.add_argument("--repair-protocol", action="store_true")
            command.add_argument("--continue-budget", action="store_true")
            command.add_argument("--candidates-only", action="store_true")
        elif name in {"status", "export", "publish"}:
            command.add_argument("--batch-id", required=name != "status")
            if name == "export":
                command.add_argument("--out", required=True)
            if name == "publish":
                group = command.add_mutually_exclusive_group(required=True)
                group.add_argument("--case-id", action="append")
                group.add_argument("--all-ready", action="store_true", help="Approve all currently ready profiles; later content changes require new approval")
        elif name == "import-source":
            command.add_argument("--file", required=True)
    return parser


def export_batch(engine, batch_id, output):
    report = engine.report(batch_id)
    target = Path(output).resolve()
    target.mkdir(parents=True, exist_ok=True)
    atomic_json(target / "batch_report.json", report)
    batch = engine.batch(batch_id)
    atomic_json(target / "request.json", engine.artifacts.get(batch["request_ref"])["data"])
    atomic_json(target / "neighborhood.json", engine.artifacts.get(batch["neighborhood_ref"])["data"])
    if batch.get("plan_ref"):
        atomic_json(target / "plan.json", engine.artifacts.get(batch["plan_ref"])["data"])
    lines = ["# Atlas expansion batch", "", f"Batch: `{batch_id}`", "", report["notice"], "",
             f"Opportunities: {report['opportunities']}. Full candidates: {report['candidate_count']}. Maximum research cases: {report['target_profiles']}.", ""]
    for row in report["cases"]:
        case = engine.ws.case(row["case_id"])
        export_case(engine, row["case_id"], target / "cases" / row["case_id"])
        lines.extend([f"## {row['title']}", "", f"Status: **{row['state']}**", "",
                      "Transformation: " + row["transformation"], "", "Selection rationale: " + row["selection_reason"], "",
                      "Seed settings: " + ", ".join(row["seed_setting_ids"]), "",
                      f"[Case and profile files](cases/{row['case_id']}/)", ""])
        # Preserve frontend provenance as formal objects alongside the shared scientific export.
        for field in ("expansion_ref", "origin_ref", "candidate_review_ref"):
            if case.get(field):
                atomic_json(target / "cases" / row["case_id"] / (field + ".json"), engine.artifacts.get(case[field]))
    (target / "BATCH_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return {"directory": str(target), "batch_id": batch_id, "state_counts": report["state_counts"]}


def main(argv=None, *, prog="oracle-atlas-expand"):
    args = build_parser(prog=prog).parse_args(argv)
    try:
        if args.command == "init":
            destination = Path(args.config).resolve()
            if destination.exists():
                raise ProtocolError("The configuration already exists; edit it or choose another path")
            template = (resources_root() / "config" / "expansion.example.toml").read_text(encoding="utf-8")
            for field, value in (("atlas", str(Path(args.atlas).resolve())), ("workspace", str(Path(args.workspace).resolve())), ("backend", args.backend), ("model", args.model)):
                import re
                template = re.sub(r"(?m)^" + field + r" = .*?$", lambda _: field + " = " + json.dumps(value), template, count=1)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(template, encoding="utf-8")
            print_json({"config": str(destination), "next": "Run doctor, then plan/run with a request JSON. Expansion profiles wait for explicit publication."})
            return
        config = load_config(args.config)
        if args.command == "doctor":
            print_json(doctor(config))
            return
        backend = LazyBackend(config)
        bridge = None
        if config.get("mcp") and config.get("backend", "responses") == "responses" and args.command not in {"status", "export", "import-source"}:
            from ..providers.mcp import MCPBridge
            bridge = MCPBridge(config["mcp"])
        engine = ExpansionEngine(config, backend, bridge=bridge)
        try:
            if args.command in {"plan", "run"}:
                request = json.loads(Path(args.request).read_text(encoding="utf-8"))
                if args.command == "plan":
                    batch = engine.plan(request)
                    result = engine.report(batch["batch_id"])
                else:
                    result = engine.expand(request, research=not args.candidates_only)
            elif args.command == "resume":
                if args.job_id:
                    job = engine.ws.job(args.job_id)
                    engine._batch_scope = job["inputs"].get("batch_scope")
                    job = engine.runner.run(args.job_id, validate_output=engine._validate_stage, retry_transport=args.retry_transport,
                                            repair_protocol=args.repair_protocol, continue_budget=args.continue_budget)
                    result = {"job_id": job["id"], "status": job["status"], "output": job["output"], "next": "Resume the batch or case to consume the validated handoff."}
                elif args.case_id:
                    refs = args.material_ref + [import_source(engine, p) for p in args.material_file]
                    result = engine.resume_expansion_case(args.case_id, stage=args.stage, material_refs=refs)
                else:
                    if args.stage or args.material_ref or args.material_file:
                        raise ProtocolError("A scientific stage revision requires --case-id")
                    batch = engine.batch(args.batch_id)
                    if not batch.get("plan_ref"):
                        request = engine.artifacts.get(batch["request_ref"])["data"]
                        engine.plan(request)
                    result = engine.run_batch(args.batch_id, research=not args.candidates_only)
            elif args.command == "status":
                result = engine.report(args.batch_id) if args.batch_id else {"batches": [json.loads(r["record"]) for r in engine.ws.query("SELECT record FROM runs") if json.loads(r["record"]).get("kind") == "expansion"], "jobs": engine.ws.query("SELECT id,role,status FROM jobs ORDER BY created")}
            elif args.command == "export":
                result = export_batch(engine, args.batch_id, args.out)
            elif args.command == "publish":
                result = engine.publish(args.batch_id, args.case_id)
            elif args.command == "import-source":
                result = {"source_ref": import_source(engine, args.file)}
            else:
                raise ProtocolError("Unsupported expansion command")
            print_json(result)
        finally:
            backend.close()
            if bridge:
                bridge.close()
            engine.ws.close()
    except (ProtocolError, ValueError, RuntimeError, OSError, KeyError) as exc:
        print(json.dumps({"error_type": type(exc).__name__, "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)


def structural_main(argv=None):
    """Branded entry point; preserve the established CLI as a compatibility alias."""
    return main(argv, prog="structural-exploration")


if __name__ == "__main__":
    main()
