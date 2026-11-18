"""Run the normal first Brain plan, then stop before any Cell preparation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))

from colombo.configuration import load_config
from colombo.brain.controller import OracleController
from colombo.shared.file_io import atomic_write, json_bytes
from colombo.brain.research_store import Store


class NoCellAdapter:
    def __init__(self):
        self.calls = []

    def __getattr__(self, name):
        def reject(*args, **kwargs):
            self.calls.append(name)
            raise RuntimeError(f"Plan preview forbids Cell adapter action: {name}")
        return reject


class PlanOnlyController(OracleController):
    def _forbidden(self, *args, **kwargs):
        raise RuntimeError("Plan preview must stop before execution or integration")

    run = _prepare = _tick = _forbidden
    _integrate = _begin_integrate = _final_review = _conclude = _forbidden

    def _call(self, role, stage, prompt, context):
        if (role, stage) != ("brain", "plan"):
            raise RuntimeError("Plan preview permits only the Brain plan stage")
        return super()._call(role, stage, prompt, context)


def render_plan(proposal, jobs):
    lines = ["# Brain plan preview", "", "Cells prepared: 0. Cells started: 0.", "",
             "## Rationale", "", proposal.get("rationale", ""), ""]
    for index, task in enumerate(proposal["tasks"]):
        identity = jobs[index]["task_id"] if index < len(jobs) else str(index + 1)
        lines.extend([f"## {identity} — {task.get('specialization', 'general')}", ""])
        for key in ("title", "instructions", "deliverables", "completion_criteria", "responsibility", "package"):
            value = task.get(key)
            if value is None:
                continue
            lines += [f"### {key}", ""]
            if isinstance(value, str):
                lines += [value, ""]
            elif isinstance(value, list) and all(isinstance(v, str) for v in value):
                lines += [*["- " + v for v in value], ""]
            else:
                lines += ["```json", json.dumps(value, ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)


def preview(store, *, backend=None, require_exit_receipt=True):
    adapter = NoCellAdapter()
    controller = PlanOnlyController(PROJECT, store.root, backend=backend, adapter=adapter)
    with store.exclusive():
        if store.get_meta("model_call_count", 0) or store.get_meta("round_no", 0):
            raise ValueError("Preview requires a fresh run; it never automatically retries a model call")
        store.set_meta(preview_only=True, status="running")
        try:
            controller._start_budget()
            controller._initialize_proof()
            store.set_meta(research_routing={"research_mode": "oracle_complexity", "source": "fixed",
                                             "reason": "Colombo Oracle Complexity"})
            controller._plan()
            data = store.get_meta("round_data")
            proposal = store.read_record(data["plan_ref"])
            assert not adapter.calls, adapter.calls
            assert not (store.root / "tasks").exists(), "Unexpected Cell workspace"
            call = store.root / "brain/calls/C00001/call.json"
            manifest = json.loads(call.read_text(encoding="utf-8")) if call.is_file() else {}
            if require_exit_receipt:
                if not (manifest.get("status") == "submitted" and manifest.get("process_exit_confirmed")
                        and manifest.get("process_tree_terminated")):
                    raise RuntimeError("Brain process-tree exit is not confirmed")
            report = {"status": "plan_preview_complete", "plan_ref": data["plan_ref"],
                      "model": manifest.get("model"), "model_calls": store.get_meta("model_call_count"),
                      "audit_calls": store.get_meta("audit_call_count", 0),
                      "task_count": len(proposal["tasks"]), "cells_prepared": 0, "cells_started": 0,
                      "adapter_calls": adapter.calls, "brain_process_exit_confirmed": manifest.get("process_exit_confirmed"),
                      "brain_process_tree_terminated": manifest.get("process_tree_terminated"),
                      "jobs": data["jobs"], "plan": proposal}
            atomic_write(store.root / "plan_preview.json", json_bytes(report))
            atomic_write(store.root / "plan_preview.md", render_plan(proposal, data["jobs"]).encode("utf-8"))
            store.set_meta(status="paused", stop_reason="User requested stop after first plan, before any Cell preparation")
            store.event("plan_preview_complete", plan_ref=data["plan_ref"], cells_started=0)
            return report
        except BaseException as exc:
            store.set_meta(status="needs_attention", stop_reason=f"Plan preview stopped: {type(exc).__name__}: {exc}")
            raise
        finally:
            controller._pause_budget()
            controller._export_state()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--setting", required=True, type=Path)
    parser.add_argument("--run-dir", required=True, type=Path)
    args = parser.parse_args()
    goal = ("Establish near-optimal Oracle Complexity rates for the setting in the supplied setting.md, "
            "covering all of its declared Algorithm views and regimes. Preserve its mathematical Setting "
            "Specification and Resource accounting. Unless the input explicitly requires a stricter result, "
            "matching up to polylog factors in the tracked natural dimensionless parameters is sufficient. "
            "Treat supplied Bounds and references as source material with their stated evidence status.")
    store = Store.create(args.run_dir, goal, [], load_config(), [args.setting])
    print(json.dumps({"event": "brain_plan_started", "run_dir": str(store.root)}, ensure_ascii=False), flush=True)
    report = preview(store)
    print(json.dumps({key: value for key, value in report.items() if key not in {"plan", "jobs"}}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
