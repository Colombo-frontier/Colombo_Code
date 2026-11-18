"""Explicit Cell budget cycles; cumulative usage and frozen evidence never reset.

Only the owning execution worker grants a cycle. Ordinary resume merely reads
the latest grant. Existing Subcells, per-report checks and per-Challenge quotas
retain their original scope; a parent grant never propagates into their roots.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json
import re

from colombo.shared.file_io import Path, json_equal, read_json, write_json
from colombo.shared.process_control import execution_scope


_KINDS = {"prover", "verifier", "experiment_native", "experiment_hosted"}
_PENDING_EXPERIMENT = {"preparing", "submitted", "running", "remote_unknown", "download_pending"}


def _count(value, label):
    if type(value) is not int or value < 0:
        raise ValueError(f"Invalid cumulative restart count: {label}")
    return value


def _local(root, relative):
    root = Path(root).resolve()
    path = root / relative
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError("Restart budget path escapes its Cell")
    return path


def _ledger(root):
    path = _local(root, "runtime/restart_budget.json")
    if not path.exists():
        return {"schema_version": 1, "cycles": []}
    value = read_json(path)
    if value.get("schema_version") != 1 or not isinstance(value.get("cycles"), list):
        raise ValueError("Invalid restart budget ledger")
    seen = set()
    for row in value["cycles"]:
        scope = execution_scope(row.get("scope"))
        if scope["attempt_id"] in seen or set(row.get("baselines", {})) != _KINDS:
            raise ValueError("Invalid restart budget cycle")
        seen.add(scope["attempt_id"])
        for key, count in row["baselines"].items():
            _count(count, key)
    return value


def effective_limit(root, kind, configured):
    """Return an absolute cumulative cap, without changing policy or counters."""
    if kind not in _KINDS:
        raise ValueError(f"Unknown restart budget: {kind}")
    _count(configured, kind)
    cycles = _ledger(root)["cycles"]
    return configured + (cycles[-1]["baselines"][kind] if cycles else 0)


def current_cycle(root):
    """Read the local active grant for diagnostics; never initialize a ledger."""
    cycles = _ledger(root)["cycles"]
    return cycles[-1] if cycles else None


def restart_blockers(root):
    """Frozen metadata that needs reconciliation before granting fresh work."""
    root = Path(root).resolve()
    blockers = []
    for path in _local(root, "experiments").glob("exp-*/state.json"):
        path = _local(root, path.relative_to(root))
        status = read_json(path).get("execution", {}).get("status")
        if status in _PENDING_EXPERIMENT or not isinstance(status, str):
            blockers.append(f"Reconcile unfinished hosted experiment {path.parent.name} ({status}) before Restart")
    return blockers


def cumulative_usage(root):
    """Read the same durable counters used by the native and hosted drivers."""
    root = Path(root).resolve()
    prover_path = _local(root, "runtime/prover_state.json")
    if prover_path.is_file():
        prover = _count(read_json(prover_path).get("launches"), "prover")
    else:
        events = _local(root, "run_events.jsonl")
        prover = 0
        if events.is_file():
            for line in events.read_text(encoding="utf-8").splitlines():
                try:
                    prover += json.loads(line).get("action") == "prover_started"
                except json.JSONDecodeError:
                    continue  # Same legacy migration as controller._prover_state.
    index_path = _local(root, "reviews/index.json")
    index = read_json(index_path) if index_path.is_file() else {"attempts": []}
    verifier = _count(index.get("primary_launches", len(index.get("attempts", []))), "verifier")
    native_path = _local(root, "runtime/experiment_state.json")
    native = _count(read_json(native_path).get("launches"), "experiment_native") if native_path.is_file() else 0
    hosted = 0
    for path in _local(root, "experiments").glob("exp-*/plan.json"):
        path = _local(root, path.relative_to(root))
        state = _local(root, path.parent.relative_to(root) / "state.json")
        if state.is_file():
            hosted += 1
    return {"prover": prover, "verifier": verifier,
            "experiment_native": native, "experiment_hosted": hosted}


def grant_restart(root, scope, settings, *, empirical=False):
    """Grant once for a new explicit attempt while the Cell is quiescent.

    The existing run lock serializes grants against every solver. The caller
    must also hold its normal task dispatch ownership. Completed older attempts
    cannot switch the current grant or mint a second cycle when replayed.
    """
    root = Path(root).resolve()
    scope = execution_scope(scope)
    from colombo.cell.controller import _exclusive_run, _active_children
    with _exclusive_run(root):
        ledger = _ledger(root)
        cycles = ledger["cycles"]
        for index, row in enumerate(cycles):
            if row["scope"]["attempt_id"] == scope["attempt_id"]:
                if not json_equal(row["scope"], scope):
                    raise ValueError("Restart attempt reused with different fixed scope")
                if index != len(cycles) - 1:
                    raise ValueError("Cannot replay an obsolete restart budget cycle")
                return row
        if cycles:
            last = cycles[-1]["scope"]
            if not json_equal({k: v for k, v in last.items() if k != "attempt_id"},
                              {k: v for k, v in scope.items() if k != "attempt_id"}):
                raise ValueError("Restart cannot change the fixed Task assignment or package")
            old, new = last["attempt_id"], scope["attempt_id"]
            if not re.fullmatch(r"A[0-9]+", new) or not re.fullmatch(r"A[0-9]+", old) or int(new[1:]) <= int(old[1:]):
                raise ValueError("Restart requires a newer attempt")
        if _active_children(root):
            raise ValueError("Reconcile active Subcells/tool jobs before Restart")
        blockers = restart_blockers(root)
        if blockers:
            raise ValueError("; ".join(blockers))
        allowances = {"prover": settings["agents"]["prover_max_rounds"],
                      "verifier": settings["agents"]["verifier_max_rounds"],
                      "experiment_native": settings["agents"]["prover_max_rounds"],
                      "experiment_hosted": settings["experiment"]["max_runs"]}
        for key, value in allowances.items():
            _count(value, key)
        row = {"scope": scope, "created_at": datetime.now(timezone.utc).isoformat(),
               "empirical": bool(empirical), "baselines": cumulative_usage(root),
               "allowances_at_grant": allowances,
               "retained_scopes": ["existing_subcells", "per_report_checks", "per_challenge"]}
        cycles.append(row)
        write_json(_local(root, "runtime/restart_budget.json"), ledger)
        return row
