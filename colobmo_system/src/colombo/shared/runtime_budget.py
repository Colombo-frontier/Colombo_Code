"""Durable research usage accounting and historical shared-deadline support.

Colombo Wave-based runs always create an unlimited accounting ledger with no closing
reserves. Descendants inherit that ledger, never a historical ancestor deadline.
The legacy bounded ledger remains readable for historical runtime consumers.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import time
from colombo.shared.file_io import Path, atomic_write, file_lock

ENVIRONMENT_KEY = "COLOMBO_BUDGET_FILE"


class BudgetExhausted(RuntimeError):
    pass


def _read(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("version") != 1:
        raise ValueError("Unsupported research budget ledger")
    return value


def _write(path, value):
    atomic_write(path, (json.dumps(value, ensure_ascii=False, indent=2)+"\n").encode("utf-8"))




def _own_file(root):
    return Path(root).resolve()/"runtime"/"budget.json"


def find_budget_file(work_dir=None):
    nearest = None
    wave_boundary = False
    if work_dir is not None:
        here = Path(work_dir).resolve()
        for parent in (here, *here.parents):
            path = parent/"runtime"/"budget.json"
            if path.is_file():
                if nearest is None:
                    nearest = path
                if _read(path).get("accounting_only"):
                    return path
            # A new standalone Colombo Cell must not inherit a previous run's
            # finite deadline from the environment or its containing folder.
            run_file = parent / "run.json"
            if run_file.is_file():
                try:
                    wave_based = json.loads(run_file.read_text(encoding="utf-8")).get("budget_policy") == "wave_dispatch"
                except (OSError, ValueError, AttributeError):
                    wave_based = False
                wave_boundary = wave_boundary or wave_based
    if wave_boundary:
        return None
    explicit = os.environ.get(ENVIRONMENT_KEY)
    if explicit:
        path = Path(explicit).resolve()
        if not path.is_file():
            raise ValueError("Inherited research budget file is missing")
        return path
    return nearest


def configured_seconds(config):
    """Wave-based research records elapsed time but has no time allocation."""
    if config.get("workflow", {}).get("version") == 3:
        if "budget" in config:
            raise ValueError("Colombo does not accept a whole-run research deadline")
        return "unlimited"
    return config["budget"]["research"]["total_active_seconds"]


def _elapsed(state, now):
    started = state.get("active_started_at")
    return float(state["used_seconds"]) + (max(0.0, now-started) if started is not None else 0.0)


def start_budget(run_root, config, source=None):
    """Start/resume under the caller's run lock; retain all spent time.

    A previously unclosed interval is conservatively charged, including sleep or
    a controller crash. Only a confirmed pause stops elapsed accounting.
    """
    cap = configured_seconds(config)
    if not (cap == "unlimited" or type(cap) is int and cap > 0):
        raise ValueError("Research time must be positive seconds or unlimited")
    settings = config["cell"]["settings"]
    runtime = settings["runtime"]
    path = _own_file(run_root)
    metadata = config.get("policy_metadata", {})
    revision = metadata.get("revision") or hashlib.sha256(
        json.dumps(config, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    with file_lock(path.with_suffix(".lock"), runtime["task_lock_timeout_seconds"], runtime["lock_poll_seconds"]):
        previous = _read(path) if path.exists() else None
        now = time.time()
        used = _elapsed(previous, now) if previous else 0.0
        remaining = None if cap == "unlimited" else max(0.0, cap-used)
        same_policy = bool(previous and previous.get("policy_revision") == revision
                           and previous.get("configured_seconds") == cap)
        if same_policy and previous.get("active_started_at") is not None and previous.get("status") == "active":
            # Reattach to a still-running tree without reallocating its reserves.
            previous["recovered_unclosed_interval"] = True
            if remaining is not None and remaining <= 0:
                previous.update(status="exhausted", used_seconds=used, active_started_at=None)
            _write(path, previous)
            if previous["status"] == "exhausted":
                raise BudgetExhausted("Research time is exhausted; increase it in the outer config before resuming")
            return get_budget_context(run_root, _path=path)
        closing = settings["handoff"]["reserve_seconds"]
        recovery = settings["handoff"]["recovery_seconds"]
        if remaining is None:
            closing = recovery = 0.0
        elif closing+recovery >= remaining:
            scale = remaining/(2*(closing+recovery)) if closing+recovery else 0
            closing, recovery = closing*scale, recovery*scale
        deadline = None if remaining is None else now+remaining
        work_deadline = None if deadline is None else deadline-closing-recovery
        hard_deadline = None if deadline is None else deadline-recovery
        if same_policy and previous.get("active_started_at") is None and remaining is not None:
            # Resume the SAME partition, including a previously entered closing window.
            work_left = max(0.0, previous.get("work_until_used_seconds", used)-used)
            hard_left = max(0.0, previous.get("hard_until_used_seconds", used)-used)
            work_left, hard_left = min(work_left, remaining), min(hard_left, remaining)
            work_deadline, hard_deadline = now+work_left, now+hard_left
            closing, recovery = max(0.0, hard_left-work_left), max(0.0, remaining-hard_left)
        revisions = list(previous.get("revisions", [])) if previous else []
        if not previous or previous.get("policy_revision") != revision:
            revisions.append({"revision": revision, "adopted_at": now, "used_seconds": used,
                              "limit_seconds": cap, "source": source or metadata.get("source")})
        state = {"version": 1, "run_root": str(Path(run_root).resolve()),
                 "accounting_only": config.get("workflow", {}).get("version") == 3,
                 "policy_revision": revision, "source": source or metadata.get("source"),
                 "profile": config.get("profile", config["cell"].get("profile")),
                 "policy_settings": settings,
                 "configured_seconds": cap, "used_seconds": used, "active_started_at": now,
                 "status": "active" if remaining is None or remaining > 0 else "exhausted",
                 "deadline_unix": deadline,
                 "work_deadline_unix": work_deadline,
                 "hard_deadline_unix": hard_deadline,
                 "work_until_used_seconds": None if work_deadline is None else used+work_deadline-now,
                 "hard_until_used_seconds": None if hard_deadline is None else used+hard_deadline-now,
                 "closing_reserve_seconds": closing, "recovery_reserve_seconds": recovery,
                 "clock": "active_wall", "suspend_counts_as_active": True,
                 "unobserved_interval": "charge_and_report", "revisions": revisions,
                 "recovered_unclosed_interval": bool(previous and previous.get("active_started_at") is not None),
                 "elapsed_basis": previous.get("elapsed_basis", "since_budget_policy_adoption") if previous else "since_budget_policy_adoption",
                 "lock_timeout_seconds": runtime["task_lock_timeout_seconds"],
                 "lock_poll_seconds": runtime["lock_poll_seconds"]}
        _write(path, state)
    result = get_budget_context(run_root, _path=path)
    if state["status"] == "exhausted":
        raise BudgetExhausted("Research time is exhausted; increase it in the outer config before resuming")
    return result


def pause_budget(run_root):
    """Call only after the owner has confirmed no descendants still execute."""
    path = _own_file(run_root)
    if not path.exists():
        return None
    snapshot = _read(path)
    with file_lock(path.with_suffix(".lock"), snapshot["lock_timeout_seconds"], snapshot["lock_poll_seconds"]):
        state = _read(path)
        now = time.time()
        state["used_seconds"] = _elapsed(state, now)
        state["active_started_at"] = None
        state["status"] = "paused"
        state["paused_at"] = now
        _write(path, state)
    return get_budget_context(run_root, _path=path)


def get_budget_context(work_dir=None, *, _path=None):
    path = _path or find_budget_file(work_dir)
    if path is None:
        return None
    state = _read(path)
    now = time.time()
    limit = state["configured_seconds"]
    used = _elapsed(state, now)
    remaining = None if limit == "unlimited" else max(0.0, limit-used)
    work_remaining = None if state["work_deadline_unix"] is None else max(0.0,state["work_deadline_unix"]-now)
    if state.get("active_started_at") is None and state.get("work_until_used_seconds") is not None:
        work_remaining = max(0.0,state["work_until_used_seconds"]-used)
    return {**state, "budget_file": str(path), "time_limit_enabled": limit != "unlimited",
            "elapsed_seconds": used, "total_remaining_seconds": remaining,
            "remaining_seconds": remaining,
            "work_remaining_seconds": work_remaining,
            "limiting_scope": "run" if limit != "unlimited" else None,
            "closing": work_remaining is not None and work_remaining <= 0}


def inherited_deadline(work_dir=None, *, phase="total"):
    context = get_budget_context(work_dir)
    if context is None:
        return None
    if context["status"] != "active":
        raise BudgetExhausted("The inherited research budget is paused or exhausted")
    key = {"total":"deadline_unix", "work":"work_deadline_unix", "hard":"hard_deadline_unix"}[phase]
    deadline = context[key]
    if deadline is None:
        return None
    remaining = deadline-time.time()
    if remaining <= 0:
        raise BudgetExhausted("The inherited research deadline has expired")
    return time.monotonic()+remaining


def budget_environment(run_root=None):
    path = find_budget_file(run_root)
    return {ENVIRONMENT_KEY:str(path)} if path is not None else {}


def context(root=None):
    return get_budget_context(root)


def environment(root):
    return budget_environment(root)


def start(root, config):
    if "budget" not in config and config.get("workflow", {}).get("version") != 3:
        return None
    return start_budget(root, config)


def pause(root, config):
    if "budget" not in config and config.get("workflow", {}).get("version") != 3:
        return None
    return pause_budget(root)


def deadline(root, local_seconds="unlimited", *, work=False, phase=None):
    """Resolve one epoch deadline before preparation; children never reset it."""
    local = None if local_seconds == "unlimited" else time.time() + local_seconds
    shared = context(root)
    if shared is not None:
        if shared.get("status") != "active":
            raise TimeoutError("Shared research budget is paused or exhausted")
        key = "hard_deadline_unix" if phase == "hard" else "work_deadline_unix" if work else "deadline_unix"
        inherited = shared.get(key)
        if inherited is not None:
            local = inherited if local is None else min(local, inherited)
    return local


def remaining(deadline_unix):
    if deadline_unix is None:
        return None
    seconds = deadline_unix - time.time()
    if seconds <= 0:
        raise TimeoutError("Shared research time budget exhausted before starting new work")
    return seconds


def ensure_available(root):
    shared = context(root)
    if shared is not None:
        if shared.get("status") != "active":
            raise TimeoutError("Shared research budget is paused or exhausted")
        remaining(shared.get("deadline_unix"))


def operational(config, key, legacy_default):
    runtime = config.get("runtime", {})
    if ("budget" in config or config.get("workflow", {}).get("version") == 3) and key not in runtime:
        raise ValueError(f"Missing centrally configured runtime.{key}")
    return runtime.get(key, legacy_default)


def cell_operational(config, key, legacy_default):
    """Shared infrastructure settings, accepting an outer or derived Cell config."""
    cell = config.get("cell", config)
    runtime = cell.get("settings", {}).get("runtime", {})
    if ("budget" in config or "policy_metadata" in cell) and key not in runtime:
        raise ValueError(f"Missing centrally configured cell.settings.runtime.{key}")
    return runtime.get(key, legacy_default)


def finite_min(*values):
    finite = [v for v in values if v is not None]
    return min(finite) if finite else None


def remaining_seconds(deadline, *, wall=False):
    return float("inf") if deadline is None else max(0.0, deadline - (time.time() if wall else time.monotonic()))


def expired(deadline, *, wall=False):
    return deadline is not None and remaining_seconds(deadline, wall=wall) <= 0
