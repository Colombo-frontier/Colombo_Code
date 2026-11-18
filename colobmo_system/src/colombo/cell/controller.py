"""Run one mathematical research problem and enforce its final verification gate."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime
from datetime import timezone
import json
import os
from pathlib import Path as BootstrapPath
import shutil
import sys
import uuid

if __package__ in {None, ""}:
    sys.path.insert(0, str(BootstrapPath(__file__).resolve().parents[2]))

from colombo.shared.file_io import Path
from colombo.project_paths import PROJECT_ROOT
from colombo.project_paths import CELL_AGENTS_ROOT
ROOT = Path(PROJECT_ROOT)

from colombo.cell.model_calls import run_agent
from colombo.cell.recovery import install_handoff_skill
from colombo.cell.instructions import validate_mode
from colombo.cell.instructions import read_cell_mode
from colombo.cell.instructions import install_cell_pack
from colombo.cell.settings import apply_overrides
from colombo.cell.settings import get_profile_overrides
from colombo.cell.settings import get_search_enabled
from colombo.cell.settings import get_settings
from colombo.cell.settings import load_defaults
from colombo.cell.settings import merge_settings
from colombo.cell.settings import parse_process_timeout
from colombo.cell.settings import run_fields
from colombo.cell.settings import validate_settings
from colombo.cell.settings import configure as configure_task
from colombo.cell.settings import pin_task_settings
from colombo.cell.restart_budget import effective_limit
from colombo.cell.verifier.proof_review import review_submission
from colombo.cell.verifier.proof_review import manuscript_is_current
from colombo.cell.verifier.proof_review import has_pending_review


def event(root, action, **details):
    root = Path(root)
    with (root / "run_events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(), "action": action, **details}, ensure_ascii=False) + "\n")


def initialize(problem: Path, root: Path, *, model=None, timeout=None, max_rounds=None,
               search_enabled=None, profile=None, required_review_files=None,
               settings_snapshot=None, research_mode="generic", specialization="general"):
    problem, root = Path(problem), Path(root)
    cell_mode = validate_mode(research_mode, specialization)
    from colombo.cell.verifier.proof_review import validate_required_review_files
    required = validate_required_review_files(root.resolve(), [] if required_review_files is None else required_review_files)
    if settings_snapshot is None:
        defaults, selected_profile = load_defaults(profile)
        settings = apply_overrides(defaults, model=model, timeout=timeout, max_rounds=max_rounds)
    else:
        # Brain already resolved the single config at run creation. Later Waves
        # must not reload a changed file, environment, or preset definition.
        if any(value is not None for value in (model, timeout, max_rounds, search_enabled)):
            raise ValueError("A frozen settings snapshot cannot be combined with initialization overrides")
        if not isinstance(profile, str) or not profile.strip():
            raise ValueError("A frozen settings snapshot requires its saved profile label")
        settings = validate_settings(settings_snapshot)
        selected_profile = profile
    if search_enabled is not None and type(search_enabled) is not bool:
        raise ValueError("search_enabled must be true or false")
    if root.exists() and any(root.iterdir()):
        raise ValueError("Run directory is not empty; use --resume to continue it")
    root.mkdir(parents=True, exist_ok=True)
    data = problem.read_bytes()
    if not data.decode("utf-8-sig").strip():
        raise ValueError("Problem is empty")
    (root / "problem.md").write_bytes(data)
    (root / "memory").mkdir(exist_ok=True)
    config = {"storage_version": 2, "budget_policy": "wave_dispatch", **run_fields(settings), "required_review_files": required, "cell_mode": cell_mode,
              "settings": settings, "profile": selected_profile, "task_depth": 0, "role": "prover",
              "agent_options": {"search_enabled": get_search_enabled("prover", settings, root)
                                if search_enabled is None else search_enabled}}
    (root / "run.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    install_cell_pack(root, cell_mode)
    install_handoff_skill(root)
    event(root, "initialized", problem_file="problem.md", config_file="run.json", profile=selected_profile)


def configure_run(root: Path, *, model=None, timeout=None, max_rounds=None, search_enabled=None,
                  profile=None) -> dict:
    """Persist non-budget overrides; root config owns profile and resource limits."""
    if any(value is not None for value in (timeout, max_rounds, profile)):
        raise ValueError("Choose the profile and budgets in the outer config.toml")
    root = Path(root)
    overrides = {} if profile is None else get_profile_overrides(profile)
    current = merge_settings(get_settings(root), overrides)
    settings = apply_overrides(current, model=model, timeout=timeout, max_rounds=max_rounds)
    fields = []
    if model is not None:
        fields.append(("model", "name"))
    if timeout is not None:
        fields.extend(("agents", f"{role}_timeout_seconds")
                      for role in ("prover", "subcell", "verifier", "report_check"))
        if timeout != "unlimited":
            fields.append(("agents", "audit_timeout_seconds"))
    if max_rounds is not None:
        fields.extend(("agents", f"{role}_max_rounds") for role in ("prover", "verifier"))
    for section, key in fields:
        overrides.setdefault(section, {})[key] = settings[section][key]
    # Merge only explicitly selected fields under the task lock. Unrelated MCP
    # updates made since the read above must survive a CLI profile switch.
    result = configure_task(root, "prover", settings_overrides=overrides, search_enabled=search_enabled,
                            reason="Explicit CLI launch/resume overrides", profile_name=profile)
    event(root, "settings_updated", config_file="run.json", profile=profile)
    return result["desired_settings"]


def _prover_state(root: Path) -> dict:
    path = root / "runtime" / "prover_state.json"
    if path.exists():
        state = json.loads(path.read_text(encoding="utf-8"))
        if type(state.get("launches")) is not int or state["launches"] < 0:
            raise ValueError("Invalid persisted prover launch count")
        return state
    # Migrate prior task histories without granting extra launches on resume.
    launches = 0
    events = root / "run_events.jsonl"
    if events.exists():
        for line in events.read_text(encoding="utf-8").splitlines():
            try:
                launches += json.loads(line).get("action") == "prover_started"
            except (ValueError, AttributeError):
                continue
    return {"launches": launches}


def _save_prover_state(root: Path, state: dict) -> None:
    path = root / "runtime" / "prover_state.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def _review_to_boundary(root: Path) -> dict:
    """A timeout or disputed report belongs to verification until settled."""
    while True:
        decision = review_submission(root)
        event(root, "draft_review", decision=decision)
        if decision.get("status") != "pending_review":
            return decision
        print("Verification is unfinished; continuing in a fresh verifier process.", flush=True)


def _ready_submission(root: Path) -> bool:
    try:
        return json.loads((root / "submission.json").read_text(encoding="utf-8")).get("status") == "ready"
    except (OSError, ValueError, AttributeError):
        return False


class _RunBusy(Exception):
    pass


@contextmanager
def _exclusive_run(root: Path):
    """One lifecycle driver owns prover counts and transitions for each task."""
    path = root / ".run.lock"
    if path.is_symlink():
        raise ValueError("Run lock must be a local ordinary file")
    with path.open("a+b") as handle:
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                # Lock beyond EOF; initializing the byte races another owner.
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, BlockingIOError) as exc:
            raise _RunBusy from exc
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def solve(root: Path, *, timeout=None, max_turns=None, review_only=False):
    from colombo.shared.runtime_budget import BudgetExhausted
    if timeout is not None or max_turns is not None:
        raise ValueError("Choose time/count budgets in the outer config.toml")
    root = Path(root).resolve()
    read_cell_mode(root)
    try:
        with _exclusive_run(root):
            from colombo.shared.runtime_budget import find_budget_file
            from colombo.shared.runtime_budget import get_budget_context
            from colombo.shared.runtime_budget import start_budget
            from colombo.shared.runtime_budget import pause_budget
            from colombo.shared.runtime_budget import BudgetExhausted
            from colombo.shared.runtime_budget import configured_seconds
            from colombo.cell.settings import load_policy
            from colombo.cell.settings import apply_budget_policy
            inherited = find_budget_file(root)
            owned = inherited is None or inherited == root / "runtime" / "budget.json"
            if owned:
                policy = load_policy()
                previous = get_budget_context(root)
                same_policy = (previous is not None
                    and previous.get("policy_revision") == policy.get("policy_metadata", {}).get("revision")
                    and previous.get("configured_seconds") == configured_seconds(policy)
                    and previous.get("policy_settings") == policy["cell"]["settings"])
                if not same_policy and _active_children(root):
                    reason = ("Active child tasks or tool jobs must finish or be reconciled before adopting "
                              "the updated config; saved policy and counters were retained.")
                    event(root, "policy_adoption_deferred", reason=reason)
                    print(reason, flush=True)
                    return 2
                saved = json.loads((root / "run.json").read_text(encoding="utf-8"))
                selected = apply_budget_policy(get_settings(root), policy["cell"]["settings"])
                saved.update(run_fields(selected), settings=selected, profile=policy["profile"])
                from colombo.shared.file_io import atomic_write
                atomic_write(root / "run.json", (json.dumps(saved, ensure_ascii=False, indent=2)+"\n").encode())
                start_budget(root, policy)
            try:
                if review_only:
                    pin_task_settings(root, "prover")
                    print(json.dumps(_review_to_boundary(root), ensure_ascii=False))
                    return 0 if manuscript_is_current(root) else 2
                return _solve_locked(root, timeout=timeout, max_turns=max_turns)
            except BudgetExhausted as exc:
                event(root, "budget_exhausted", reason=str(exc))
                return 2
            finally:
                # Detached jobs/children may still be finishing. Do not claim a
                # paused clock until their terminal state is known.
                if owned and not _active_children(root):
                    pause_budget(root)
    except _RunBusy:
        reason = "Another runner is already solving this task."
        event(root, "runner_busy", reason=reason)
        print(reason, flush=True)
        return 2
    except BudgetExhausted as exc:
        event(root, "budget_exhausted", reason=str(exc))
        return 2


def _active_children(root):
    from colombo.shared.tool_jobs import pending_jobs
    workspaces = [root]
    while workspaces:
        work = workspaces.pop()
        try:
            if pending_jobs(work):
                return True
            for path in work.glob("tasks/*/task.json"):
                status = json.loads(path.read_text(encoding="utf-8")).get("status")
                if status in {"starting", "running", "cancel_requested"}:
                    return True
                workspaces.append(path.parent / "workspace")
        except (OSError, ValueError):
            return True
    return False


def _solve_locked(root: Path, *, timeout=None, max_turns=None):
    pin_task_settings(root, "prover")
    # Older task workspaces predate this on-demand reference. Do not overwrite
    # an existing task's instructions or reference (which may be customized).
    if not (root / "protocol.md").exists():
        shutil.copyfile(CELL_AGENTS_ROOT / "prover" / "protocol.md", root / "protocol.md")
    install_handoff_skill(root)
    if manuscript_is_current(root):
        return 0
    state = _prover_state(root)
    stop_statuses = {"busy", "incomplete", "review_incomplete", "error"}
    if has_pending_review(root) or _ready_submission(root):
        decision = _review_to_boundary(root)
        if manuscript_is_current(root):
            return 0
        if decision.get("status") in stop_statuses or decision.get("primary_launches_remaining") == 0:
            print(decision.get("reason", "Verification remains incomplete."), flush=True)
            return 2
    while True:
        from colombo.shared.runtime_budget import inherited_deadline
        inherited_deadline(root, phase="work")
        # Agent-requested startup changes take effect on the next turn.
        settings = get_settings(root)
        turn_limit = effective_limit(root, "prover", settings["agents"]["prover_max_rounds"]) if max_turns is None else max_turns
        if state["launches"] >= turn_limit:
            break
        turn_timeout = settings["agents"]["prover_timeout_seconds"] if timeout is None else timeout
        stamp = uuid.uuid4().hex[:12]
        prompt = (
            "Solve problem.md under AGENTS.md. This is a fresh process: start recovery with "
            "the latest proof_state record, then read the referenced evidence as needed. "
            "If submission.json exists, inspect its current status and referenced review or error "
            "before continuing; use protocol.md for record and submission conventions. "
            "Read the latest prover handoff referenced in runtime/prover_state.json, if present. "
            "Use budget_status to reserve time for the handoff skill."
        )
        state["launches"] += 1
        _save_prover_state(root, state)
        event(root, "prover_started", turn=state["launches"])
        print(f"Research turn {state['launches']}: {root}", flush=True)
        try:
            result = run_agent(prompt, root, root / "logs" / f"prover-{stamp}.txt",
                               timeout=turn_timeout, model=settings["model"]["name"] or None,
                               role="prover", settings=settings)
            if result.get("handoff_path"):
                state["handoff_path"] = result["handoff_path"]
                _save_prover_state(root, state)
            event(root, "prover_finished", session_id=result.get("session_id"), output=result.get("log_path"),
                  execution_status=result.get("execution_status", "completed"))
            if result.get("execution_status") == "incomplete":
                event(root, "pending_tool_jobs", jobs=result.get("pending_jobs", []))
                return 2
        except Exception as exc:
            if getattr(exc, "handoff_path", None):
                state["handoff_path"] = str(exc.handoff_path)
                _save_prover_state(root, state)
            event(root, "prover_error", error=f"{type(exc).__name__}: {exc}")
            print(f"Research process did not complete: {exc}", flush=True)
        # The verifier starts a fresh process under the same root budget.
        print("Checking final submission...", flush=True)
        decision = _review_to_boundary(root)
        if manuscript_is_current(root):
            print(f"Manuscript accepted: {root / 'manuscript.md'}", flush=True)
            return 0
        if decision.get("status") in stop_statuses or decision.get("primary_launches_remaining") == 0:
            print(decision.get("reason", "Verification remains incomplete."), flush=True)
            break
        print(decision.get("reason", "No accepted manuscript yet; continuing from saved records."), flush=True)
    event(root, "incomplete", reason="No accepted manuscript within the configured turns/reviews")
    print("Incomplete: saved research is available; no successful proof is claimed.", flush=True)
    return 2


def _timeout_argument(value: str) -> int | str:
    try:
        return parse_process_timeout(value if value == "unlimited" else int(value))
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Use positive integer seconds or "unlimited"') from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", type=Path, nargs="?")
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--check", action="store_true", help="Only execute final verification gate")
    parser.add_argument("--model")
    parser.add_argument("--research-mode", choices=("generic", "oracle_complexity"),
                        help="Programme scope for a new standalone Cell; resume must match the frozen value")
    parser.add_argument("--specialization", choices=("general", "upper_bound", "lower_bound"),
                        help="Instruction pack for a new Cell; bound specializations require oracle_complexity")
    parser.add_argument("--profile", metavar="NAME",
                        help="Removed: select the profile in the outer config.toml")
    parser.add_argument("--timeout", type=_timeout_argument, metavar="SECONDS|unlimited",
                        help="Removed: set the total research budget in the outer config.toml")
    parser.add_argument("--max-rounds", type=int, help="Removed: set process limits in the outer config.toml")
    parser.add_argument("--search", action=argparse.BooleanOptionalAction, default=None,
                        help="Override only this main task's search default (--search/--no-search)")
    args = parser.parse_args()
    if any(value is not None for value in (args.timeout, args.max_rounds, args.profile)):
        parser.error("Choose profile and budgets in the outer config.toml; CLI budget overrides are disabled")
    root = (args.run_dir or ROOT / "runs" / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6])).resolve()
    if args.resume or args.check:
        read_cell_mode(root, research_mode=args.research_mode, specialization=args.specialization)
    if args.check:
        pin_task_settings(root, "prover")
        if any(value is not None for value in (args.model, args.timeout, args.max_rounds, args.search, args.profile)):
            configure_run(root, model=args.model, timeout=args.timeout, max_rounds=args.max_rounds,
                          search_enabled=args.search, profile=args.profile)
        return solve(root, review_only=True)
    if not args.resume:
        if not args.problem:
            parser.error("problem.md is required unless --resume or --check is used")
        initialize(args.problem.resolve(), root, model=args.model, timeout=args.timeout, max_rounds=args.max_rounds,
                   search_enabled=args.search, profile=args.profile,
                   research_mode=args.research_mode or "generic", specialization=args.specialization or "general")
    else:
        pin_task_settings(root, "prover")
        if any(value is not None for value in (args.model, args.timeout, args.max_rounds, args.search, args.profile)):
            configure_run(root, model=args.model, timeout=args.timeout, max_rounds=args.max_rounds,
                          search_enabled=args.search, profile=args.profile)
    return solve(root)


if __name__ == "__main__":
    sys.exit(main())
