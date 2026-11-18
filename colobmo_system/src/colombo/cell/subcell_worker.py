"""Execute one task; cancellation and timeout preserve committed partial work."""

from __future__ import annotations

import argparse
import os
from pathlib import Path as _BootstrapPath
import shutil
import sys
import time

# The helper is launched as a script; --task-dir selects its private workspace.
if __package__ in {None, ""}:
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[2]))

from colombo.project_paths import CELL_AGENTS_ROOT
from colombo.shared.file_io import Path
from colombo.cell.subcell_dispatch import _now
from colombo.cell.subcell_dispatch import _read_json
from colombo.cell.subcell_dispatch import _tasks_lock
from colombo.cell.subcell_dispatch import _write_json
from colombo.cell.settings import pin_task_settings
from colombo.cell.recovery import install_handoff_skill
from colombo.shared.runtime_budget import BudgetExhausted


def run_subcell(task_dir: Path, agent_runner=None) -> dict:
    task_dir = Path(task_dir).resolve()
    workspace = task_dir / "workspace"
    cancel_file = task_dir / "cancel.flag"
    task_path = task_dir / "task.json"
    from colombo.cell.instructions import read_cell_mode
    read_cell_mode(workspace)
    settings = pin_task_settings(workspace, "subcell")
    install_handoff_skill(workspace)
    if not (workspace / "protocol.md").exists():
        shutil.copyfile(CELL_AGENTS_ROOT / "prover" / "protocol.md", workspace / "protocol.md")
    with _tasks_lock(task_dir.parent):
        task = _read_json(task_path)
        if not isinstance(task, dict):
            raise ValueError("Missing task metadata")
        if task["status"] in {"completed", "cancelled", "budget_exhausted", "incomplete", "failed"}:
            return _read_json(task_dir / "result.json", {"status": task["status"]})
        task.update(status="cancel_requested" if cancel_file.exists() else "running",
                    started_at=_now(), subcell_pid=os.getpid())
        task.pop("worker_pid", None)  # Legacy task metadata remains readable.
        _write_json(task_path, task)
    # Process completion does not determine the mathematical outcome.
    result = {"task_id": task["task_id"], "status": "cancelled"}
    if not cancel_file.exists():
        try:
            if agent_runner is None:
                from colombo.cell.model_calls import run_agent
                agent_runner = run_agent
            prompt = ("Complete the scoped task in TASK.md under AGENTS.md. Return useful "
                      "record references, the precise conclusion and remaining obligations.")
            response = agent_runner(
                prompt, workspace, workspace / "task_result.md",
                timeout=settings["agents"]["subcell_timeout_seconds"],
                model=settings["model"]["name"] or None, settings=settings,
                role="subcell", extra_env={
                    "CELL_RUN_DIR": str(workspace), "CELL_ROLE": "subcell",
                    "CELL_CANCEL_FILE": str(cancel_file),
                }, _absolute_deadline=(None if task.get("parent_deadline_unix") is None
                                       else time.monotonic() + task["parent_deadline_unix"] - time.time()))
            result.update(status=("incomplete" if response.get("execution_status") == "incomplete" else
                                  "budget_exhausted" if response.get("execution_status") == "handoff" else "completed"),
                          agent_result=response)
            if response.get("handoff_path"):
                result["handoff_path"] = response["handoff_path"]
        except (TimeoutError, BudgetExhausted) as exc:
            result.update(status="budget_exhausted", execution_error=str(exc))
            if getattr(exc, "handoff_path", None):
                result["handoff_path"] = str(exc.handoff_path)
        except Exception as exc:
            result.update(status="failed", execution_error=f"{type(exc).__name__}: {exc}")
    with _tasks_lock(task_dir.parent):
        if cancel_file.exists():
            result["status"] = "cancelled"
        result["ended_at"] = _now()
        result["partial_work_preserved"] = True
        _write_json(task_dir / "result.json", result)
        task = _read_json(task_path)
        task.update(status=result["status"], ended_at=result["ended_at"])
        if "execution_error" in result:
            task["execution_error"] = result["execution_error"]
        _write_json(task_path, task)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-dir", type=Path, required=True)
    args = parser.parse_args()
    result = run_subcell(args.task_dir)
    return 1 if result["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
