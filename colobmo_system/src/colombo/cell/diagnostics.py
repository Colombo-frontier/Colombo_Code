"""Read-only execution diagnostics from a Cell's frozen result artifacts.

This module does not import the Cell runner: inspecting a budget must never
initialize counters, apply defaults, reconfigure a run, or launch a process.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


REVIEW_PROTOCOL = "cell-proof-review-5"


def read_experiment_stop_diagnostics(root, *, execution, reason, report_complete=False, failure=None):
    """Describe a frozen Experiment Cell without applying live defaults."""
    root = Path(root)
    errors = []
    run = _load(root, "run.json", errors)
    state = _load(root, "runtime/experiment_state.json", errors)
    settings = (run or {}).get("settings", {})
    agents = settings.get("agents", {}) if isinstance(settings, dict) else {}
    experiments = settings.get("experiment", {}) if isinstance(settings, dict) else {}
    configured = (run or {}).get("max_prover_rounds", agents.get("prover_max_rounds"))
    native_limit = _count(configured, "run.json:prover_max_rounds", errors, positive=True)
    hosted_limit = _count(experiments.get("max_runs"), "run.json:experiment.max_runs", errors, positive=True)
    native_used = _count((state or {}).get("launches"), "runtime/experiment_state.json:launches", errors)
    from colombo.cell.restart_budget import effective_limit, current_cycle, cumulative_usage, restart_blockers
    cycle = None
    hosted_used = None
    try:
        if native_limit is not None:
            native_limit = effective_limit(root, "experiment_native", native_limit)
        if hosted_limit is not None:
            hosted_limit = effective_limit(root, "experiment_hosted", hosted_limit)
        cycle = current_cycle(root)
        hosted_used = cumulative_usage(root)["experiment_hosted"]
    except (OSError, ValueError, TypeError) as exc:
        errors.append({"path": "runtime/restart_budget.json", "reason": str(exc)})
        native_limit = hosted_limit = None
    budgets = {"experiment_native": _budget(native_used, native_limit),
               "experiment_hosted": _budget(hosted_used, hosted_limit), "diagnostic_errors": errors}
    if cycle is not None:
        budgets["restart_cycle"] = cycle
    try:
        blockers = restart_blockers(root)
        if blockers:
            budgets["restart_blockers"] = blockers
    except (OSError, ValueError, TypeError) as exc:
        budgets["restart_blockers"] = [f"Cannot reconcile hosted experiment metadata: {exc}"]
    stage = "complete" if report_complete else "experiment_native"
    kind, message = "incomplete", reason
    if execution == "cancelled":
        kind = "cancelled"
    elif failure:
        kind = failure.get("kind", "runtime_error")
        message = failure.get("message") or reason
    elif execution in {"error", "timeout", "unknown"}:
        kind = "runtime_error" if execution == "error" else execution
    elif report_complete:
        kind = "completed"
    elif budgets["experiment_native"]["remaining"] == 0:
        kind = "budget_exhausted"
        message = f"Experiment researcher launch budget exhausted ({native_used}/{native_limit}). {reason}"
    return {"stop_info": {"kind": kind, "message": message, "stage": stage,
                          "review_id": None, "report_revision": None}, "budget_snapshot": budgets}


def _load(root, relative, errors):
    path = root / relative
    try:
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("diagnostic path escapes the snapshot")
        value = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(value, dict):
            raise ValueError("expected a JSON object")
        return value
    except FileNotFoundError:
        errors.append({"path": relative, "reason": "missing"})
    except (OSError, ValueError, TypeError) as exc:
        errors.append({"path": relative, "reason": f"{type(exc).__name__}: {exc}"})
    return None


def _count(value, path, errors, *, positive=False):
    if type(value) is int and value >= (1 if positive else 0):
        return value
    errors.append({"path": path, "reason": "missing or invalid positive integer" if positive
                   else "missing or invalid nonnegative integer"})
    return None


def _budget(used, limit):
    return {"used": used, "limit": limit,
            "remaining": max(0, limit - used) if used is not None and limit is not None else None}


def _review_view(item, limit, errors, *, state="unknown"):
    """Describe one identified report, never select a report by recency."""
    review_id = revision = check_used = primary_used = None
    phase = status = None
    if item is not None:
        review_id = item.get("id") if isinstance(item.get("id"), str) and item["id"] else None
        revision = _count(item.get("report_revision"), "reviews/index.json:report_revision", errors)
        phase, status = item.get("phase"), item.get("status")
        checks = item.get("check_attempts")
        if not isinstance(checks, dict):
            errors.append({"path": "reviews/index.json:check_attempts", "reason": "missing or invalid counter map"})
        elif review_id and revision is not None and revision > 0:
            # An absent entry for a new, unfinished report explicitly means no
            # checker launch yet. A completed report must have an actual count.
            count = checks.get(str(revision), None if phase == "complete" else 0)
            check_used = _count(count, f"reviews/index.json:{review_id}.check_attempts.{revision}", errors)
        launches = item.get("launches")
        if isinstance(launches, list) and all(isinstance(row, dict) and row.get("stage") in
                                             {"proof", "report_check"} for row in launches):
            primary_used = sum(row["stage"] == "proof" for row in launches)
    return {"state": state, "review_id": review_id, "report_revision": revision,
            "phase": phase, "status": status, "primary_launches": primary_used,
            "report_check": _budget(check_used, limit)}


def _submission_review(root, submission, attempts, index_valid, limit, errors):
    if submission is None:
        return _review_view(None, limit, errors)
    review_id = submission.get("review_id")
    if not review_id:
        return _review_view(None, limit, errors,
                            state="none" if submission.get("status") == "ready" else "unknown")
    matches = [row for row in attempts if row.get("id") == review_id]
    if (not index_valid or not isinstance(review_id, str)
            or not re.fullmatch(r"r\d{4,}", review_id) or len(matches) != 1):
        errors.append({"path": "submission.json:review_id", "reason": "does not bind one valid review index entry"})
        return _review_view(None, limit, errors)
    item = matches[0]
    revision = item.get("report_revision")
    if "report_revision" in submission and (type(submission["report_revision"]) is not int
                                           or submission["report_revision"] != revision):
        errors.append({"path": "submission.json:report_revision", "reason": "differs from the bound review index version"})
        return _review_view(None, limit, errors)
    # The submission currently stores the review ID; its unique index entry
    # supplies the exact report revision. Cross-check a saved confirmation when
    # present without scanning unrelated reports or replacing missing counters.
    if item.get("phase") == "complete":
        relative = f"reviews/{review_id}/confirmation.json"
        if (root / relative).exists():
            confirmation = _load(root, relative, errors)
            if (confirmation is None or confirmation.get("review_id") != review_id
                    or type(confirmation.get("report_revision")) is not int
                    or confirmation["report_revision"] != revision):
                errors.append({"path": relative, "reason": "confirmation identity differs from the bound report version"})
                return _review_view(None, limit, errors)
    view = _review_view(item, limit, errors, state="bound")
    view["revision_source"] = "submission" if "report_revision" in submission else "review_index"
    return view


def read_stop_diagnostics(root, *, execution, accepted, reason, failure=None):
    """Return descriptive facts only; neither this nor a zero count authorizes retry.

    ``root`` is the exported artifact directory, so diagnostics refer to exactly
    the same snapshots as the Result. Missing data remains null/unknown.
    """
    root = Path(root)
    errors = []
    run = _load(root, "run.json", errors)
    prover = _load(root, "runtime/prover_state.json", errors)
    index = _load(root, "reviews/index.json", errors)
    submission = _load(root, "submission.json", errors)
    settings = (run or {}).get("settings")
    agents = settings.get("agents") if isinstance(settings, dict) else None
    agents = agents if isinstance(agents, dict) else {}
    # These aliases have the same precedence in colombo.cell.settings.get_settings.
    # Read only the saved run; never fall back to Brain or machine defaults.
    limits = {}
    for role, key, alias in (("prover", "prover_max_rounds", "max_prover_rounds"),
                             ("verifier", "verifier_max_rounds", "max_review_rounds"),
                             ("report_check", "report_check_max_attempts", None)):
        value = run[alias] if run is not None and alias in run else agents.get(key)
        limits[role] = _count(value, f"run.json:{alias if run is not None and alias in run else 'settings.agents.' + key}",
                              errors, positive=True)
        if role in {"prover", "verifier"} and limits[role] is not None:
            from colombo.cell.restart_budget import effective_limit
            try:
                limits[role] = effective_limit(root, role, limits[role])
            except (OSError, ValueError, TypeError) as exc:
                errors.append({"path": "runtime/restart_budget.json", "reason": str(exc)})
                limits[role] = None

    index_valid = index is not None and index.get("protocol") == REVIEW_PROTOCOL and isinstance(index.get("attempts"), list)
    if index_valid:
        index_valid = all(isinstance(item, dict) and item.get("protocol") == REVIEW_PROTOCOL
                          for item in index["attempts"])
    if index is not None and not index_valid:
        errors.append({"path": "reviews/index.json", "reason": "invalid review index or protocol"})
    attempts = index["attempts"] if index_valid else []
    active = [item for item in attempts if item.get("protocol") == REVIEW_PROTOCOL
              and item.get("phase") != "complete"]
    item = active[-1] if len(active) == 1 else None
    if len(active) > 1:
        errors.append({"path": "reviews/index.json", "reason": "multiple unfinished reviews; current stage is ambiguous"})

    used = _count((prover or {}).get("launches"), "runtime/prover_state.json:launches", errors)
    primary_used = _count(index.get("primary_launches") if index_valid else None,
                          "reviews/index.json:primary_launches", errors)
    current = _review_view(item, limits["report_check"], errors,
                           state="active" if item is not None else "none" if index_valid and not active else "unknown")
    submitted = _submission_review(root, submission, attempts, index_valid, limits["report_check"], errors)
    # Keep the existing flat summary for consumers. It describes the active
    # report, or (only when no review is active) this exact submission's report.
    selected = current if active or not index_valid else submitted
    review_id, revision = selected["review_id"], selected["report_revision"]
    budgets = {"prover": _budget(used, limits["prover"]),
               "verifier": _budget(primary_used, limits["verifier"]),
               "report_check": {"review_id": review_id, "report_revision": revision,
                                **selected["report_check"]},
               "current_review": current, "submission_review": submitted}
    from colombo.cell.restart_budget import current_cycle, restart_blockers
    try:
        cycle = current_cycle(root)
        if cycle is not None:
            budgets["restart_cycle"] = cycle
        blockers = restart_blockers(root)
        if blockers:
            budgets["restart_blockers"] = blockers
    except (OSError, ValueError, TypeError) as exc:
        errors.append({"path": "runtime/restart_budget.json", "reason": str(exc)})
    status = (submission or {}).get("status")
    index_broken = any(error["path"] == "reviews/index.json" and error["reason"] != "missing" for error in errors)
    if accepted:
        stage = "complete"
    elif index_broken:
        stage = "unknown"
    elif item is not None:
        stage = {"proof": "verifier", "report_check": "report_check", "sync": "sync"}.get(item.get("phase"), "unknown")
    elif status in {"ready", "pending_review", "review_incomplete"}:
        # A ready draft can exhaust the primary budget before a review is created.
        stage = "verifier" if status == "ready" or (submission or {}).get("review_reason") == "The cumulative primary verifier budget is exhausted." else "unknown"
    elif submission is not None or prover is not None:
        stage = "prover" if status != "accepted" else "unknown"
    else:
        stage = "unknown"

    review_reason = (submission or {}).get("review_reason")
    review_reason = review_reason if isinstance(review_reason, str) else ""
    launches = item.get("launches", []) if item else []
    latest_launch = launches[-1] if isinstance(launches, list) and launches and isinstance(launches[-1], dict) else {}
    pending_runtime_error = (item is not None and latest_launch.get("stage") == item.get("phase")
                             and latest_launch.get("status") == "execution_error")
    kind, message = "incomplete", reason
    if execution == "cancelled":
        kind = "cancelled"
    elif failure:
        kind = failure.get("kind") if failure.get("kind") in {"runtime_error", "timeout", "mathematical_error"} else "runtime_error"
        message = failure.get("message") or reason
    elif execution in {"error", "timeout"}:
        kind = "timeout" if execution == "timeout" else "runtime_error"
    elif accepted:
        kind = "completed"
    elif execution == "unknown":
        kind = "unknown"
    elif pending_runtime_error:
        kind = "runtime_error"
        message = latest_launch.get("reason") or review_reason or reason
    else:
        role = stage if stage in budgets else None
        explicitly_exhausted = review_reason.startswith((
            "The cumulative primary verifier budget is exhausted.",
            "Primary verifier process budget exhausted;",
            "Independent checker budget exhausted for this exact report;"))
        # review_incomplete also covers invalid frozen inputs and sync failures.
        # A counter at its limit alone does not turn those failures into exhaustion.
        review_boundary = explicitly_exhausted or review_reason == "The verifier stage needs continuation; see its handoff and internal error record."
        if role and budgets[role]["remaining"] == 0 and (stage == "prover" or review_boundary):
            kind = "budget_exhausted"
            message = (review_reason if stage != "prover" else
                       f"Prover launch budget exhausted ({used}/{limits['prover']}). {reason}")
        elif (status == "needs_revision" and type((submission or {}).get("primary_launches_remaining")) is int
              and submission["primary_launches_remaining"] == 0
              and budgets["verifier"]["remaining"] == 0):
            kind = "budget_exhausted"
            message = "The review ended with no remaining primary verifier launches. " + (review_reason or reason)
        elif review_reason:
            message = review_reason

    budgets["diagnostic_errors"] = errors
    return {"stop_info": {"kind": kind, "message": message, "stage": stage,
                          "review_id": review_id, "report_revision": revision},
            "budget_snapshot": budgets}
