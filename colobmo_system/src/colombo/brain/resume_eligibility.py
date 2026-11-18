"""Read-only scheduling eligibility from a reconciled, frozen Cell Result.

This module deliberately does not import the Cell lifecycle, settings loader,
or record Store. Inspection must not pin settings, initialize counters, inspect
active research, or make a missing budget look like a fresh allocation.
"""
from __future__ import annotations

from copy import deepcopy


_ROLES = {"prover": "prover_max_rounds", "verifier": "verifier_max_rounds", "experiment_native": "prover_max_rounds",
          "report_check": "report_check_max_attempts"}


def _answer(status, stage, reason, *, suggested=None, restart="unknown", budget=None):
    return {"status": status, "stage": stage, "reason": reason,
            "suggested_mode": suggested, "restart_status": restart,
            "budget": budget}


def _unknown(reason, stage="unknown"):
    return _answer("unknown", stage, reason + " Reconcile the saved execution before dispatching.")


def _nonnegative(value):
    return type(value) is int and value >= 0


def _configured_limit(config, role):
    if not isinstance(config, dict):
        return None
    cell = config.get("cell", config)
    settings = cell.get("settings", {}) if isinstance(cell, dict) else {}
    agents = settings.get("agents", {}) if isinstance(settings, dict) else {}
    value = agents.get(_ROLES[role]) if isinstance(agents, dict) else None
    return value if type(value) is int and value > 0 else None


def result_resume_eligibility(result, config=None):
    """Inspect descriptive Result facts; never authorize a new budget implicitly.

    ``restart_status`` concerns an *explicit* new allocation for the same fixed
    Task. A restart cannot repair an ambiguous execution or replenish the checker
    quota for an unchanged report revision. Historical Results without diagnostics
    remain readable but do not become evidence of unused starts.
    """
    if not isinstance(result, dict):
        return _unknown("The latest Result is not an object.")
    if result.get("execution_status") not in {"finished", "incomplete", "error", "timeout", "cancelled"}:
        return _unknown("The latest Result does not establish a terminal execution.")
    stop = result.get("stop_info")
    snapshot = result.get("budget_snapshot")
    if not isinstance(stop, dict) or not isinstance(snapshot, dict):
        # A terminal accepted Result already certifies the publication boundary;
        # it does not need another model launch to be returned again.
        if result.get("accepted") is True:
            return _answer("allowed", "complete", "The terminal Result is already accepted; publication needs no model start.",
                           suggested="resume", restart="allowed")
        return _unknown("The latest Result has no frozen lifecycle/budget diagnostics.")
    stage = stop.get("stage")
    if not isinstance(stage, str):
        return _unknown("The frozen stop phase is malformed.")
    current = snapshot.get("current_review")
    submitted = snapshot.get("submission_review")
    if ((current is not None and not isinstance(current, dict))
            or (submitted is not None and not isinstance(submitted, dict))):
        return _unknown("The frozen review state is malformed.", stage)
    current = current if isinstance(current, dict) else {}
    submitted = submitted if isinstance(submitted, dict) else {}
    if current.get("state") is not None and not isinstance(current.get("state"), str):
        return _unknown("The frozen current review state is malformed.", stage)
    errors = snapshot.get("diagnostic_errors", [])
    if not isinstance(errors, list) or any(not isinstance(item, dict)
            or not isinstance(item.get("path"), str) or not isinstance(item.get("reason"), str) for item in errors):
        return _unknown("The frozen diagnostic error list is malformed.")
    restart_blockers = snapshot.get("restart_blockers", [])
    if not isinstance(restart_blockers, list) or any(not isinstance(item, str) for item in restart_blockers):
        return _unknown("The saved restart blockers are malformed.", stage)
    restart_status = "unknown" if restart_blockers else "allowed"
    if result.get("accepted") is True and stage == "complete":
        if current.get("state") == "active":
            return _unknown("Acceptance conflicts with an unfinished review.")
        return _answer("allowed", "complete", "The terminal Result is already accepted; publication needs no model start.",
                       suggested="resume", restart=restart_status)
    if stage == "complete":
        return _unknown("Completion is not backed by an accepted Result.")
    if stage not in {*_ROLES, "sync"}:
        return _unknown("The next necessary lifecycle phase is unknown.")

    # An exhausted prover with no submission and no review index is a normal,
    # determinate boundary. Never infer an unused verifier counter from this.
    no_review_files = {(item.get("path"), item.get("reason")) for item in errors}
    absent_review = {("reviews/index.json", "missing"), ("submission.json", "missing")} <= no_review_files
    allowed_absence = {"reviews/index.json", "submission.json", "reviews/index.json:primary_launches"}
    material_errors = [item for item in errors if not
        (stage == "prover" and absent_review and item.get("path") in allowed_absence)]
    # The next review phase does not consume a Prover launch. Its missing
    # counter is irrelevant, but a malformed counter is still inconsistent.
    missing_prover = ("runtime/prover_state.json", "missing") in no_review_files
    derived_missing_prover = ("runtime/prover_state.json:launches", "missing or invalid nonnegative integer")
    material_errors = [item for item in material_errors if not
        (stage in {"verifier", "report_check", "sync"}
         and missing_prover and (item.get("path"), item.get("reason")) in
         {("runtime/prover_state.json", "missing"), derived_missing_prover})]
    if material_errors:
        return _unknown("Frozen diagnostics contain missing or inconsistent lifecycle evidence.", stage)

    if current.get("state") == "active":
        phases = {"proof": "verifier", "report_check": "report_check", "sync": "sync"}
        if phases.get(current.get("phase")) != stage:
            return _unknown("The stop phase conflicts with the active review phase.", stage)
        if (not isinstance(current.get("review_id"), str) or not current["review_id"]
                or not _nonnegative(current.get("report_revision"))):
            return _unknown("The current review identity is incomplete.", stage)
    elif stage in {"report_check", "sync"}:
        return _unknown("The next phase is not bound to one active review.", stage)
    elif stage == "prover" and current.get("state") not in {"none", None} and not absent_review:
        return _unknown("The saved review state does not establish a Prover boundary.", stage)
    elif stage == "verifier" and current.get("state") not in {"none", None}:
        return _unknown("The saved review state does not establish a Verifier boundary.", stage)

    if stage == "sync":
        if current.get("report_revision", 0) <= 0:
            return _unknown("Synchronization is not bound to a positive report revision.", stage)
        return _answer("allowed", stage, "The confirmed report awaits synchronization; no model start is required.",
                       suggested="resume", restart=restart_status)

    if (stage == "verifier" and current.get("state") == "none"
            and submitted.get("state") == "bound" and submitted.get("phase") == "complete"
            and submitted.get("status") == "accepted"):
        if (not isinstance(submitted.get("review_id"), str) or not submitted["review_id"]
                or not _nonnegative(submitted.get("report_revision")) or submitted["report_revision"] == 0):
            return _unknown("The saved publication receipt has an invalid report identity.", stage)
        return _answer("allowed", "publication", "The exact submitted report is already accepted; its receipt may be republished without a model start.",
                       suggested="resume", restart=restart_status)

    saved = snapshot.get(stage)
    if not isinstance(saved, dict):
        return _unknown("The next phase has no saved budget.", stage)
    used, limit = saved.get("used"), saved.get("limit")
    if not _nonnegative(used) or type(limit) is not int or limit <= 0:
        return _unknown("The next phase's used/limit counters are unknown.", stage)
    if stage == "report_check":
        if (current.get("report_revision", 0) <= 0
                or saved.get("review_id") != current.get("review_id")
                or saved.get("report_revision") != current.get("report_revision")):
            return _unknown("The checker budget is not bound to the current report revision.", stage)
        nested = current.get("report_check")
        if not isinstance(nested, dict) or nested.get("used") != used or nested.get("limit") != limit:
            return _unknown("The current review and checker budget disagree.", stage)
    # Current root policy is authoritative, including decreases. A restart
    # adds its frozen usage baseline, never its old allowance, to that policy.
    baseline = 0
    cycle = snapshot.get("restart_cycle")
    if cycle is not None:
        if not isinstance(cycle, dict) or not isinstance(cycle.get("baselines"), dict):
            return _unknown("The frozen restart allocation is malformed.", stage)
        scope = cycle.get("scope")
        if not isinstance(scope, dict) or any(scope.get(key) != result.get(key) for key in
                                             ("task_id", "assignment_ref", "package_ref")):
            return _unknown("The frozen restart allocation belongs to another Task scope.", stage)
        if stage in {"prover", "verifier", "experiment_native"}:
            baseline = cycle["baselines"].get(stage)
            if not _nonnegative(baseline) or baseline > used:
                return _unknown("The restart usage baseline is inconsistent with cumulative usage.", stage)
    configured = _configured_limit(config, stage)
    effective = baseline + configured if configured is not None else limit
    budget = {"used": used, "saved_limit": limit, "limit": effective,
              "baseline": baseline, "remaining": max(0, effective - used)}
    if effective > used:
        return _answer("allowed", stage, "The next necessary model phase has remaining starts.",
                       suggested="resume", restart=restart_status, budget=budget)
    if stage == "report_check":
        return _answer("blocked", stage, "The checker quota for this exact report revision is exhausted; restarting does not replenish it.",
                       suggested="new", restart="blocked", budget=budget)
    return _answer("blocked", stage, "The next necessary model phase has exhausted its starts; resume preserves these counters.",
                   suggested=None if restart_blockers else "restart", restart=restart_status, budget=budget)


def task_resume_eligibility(store, task, config=None):
    """Read only the latest Result bound to this reconciled Task and attempt."""
    if not isinstance(task, dict) or task.get("state") not in {"returned", "failed", "cancelled"}:
        return _unknown("The Task is active or has not been reconciled.")
    ref = task.get("latest_result_ref")
    if not ref:
        return _unknown("The Task has no reconciled latest Result.")
    try:
        result = store.read_record(ref)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return _unknown("The latest Result cannot be read (" + type(exc).__name__ + ").")
    if not isinstance(result, dict):
        return _unknown("The latest Result is malformed.")
    attempt = task.get("finished_attempt") or task.get("outcome_attempt_id") or task.get("active_attempt")
    if not attempt or (task.get("active_attempt") and task["active_attempt"] != attempt):
        return _unknown("The Task's latest terminal attempt is ambiguous.")
    expected = {"task_id": task.get("task_id"), "attempt_id": attempt,
                "assignment_ref": task.get("assignment_ref"), "package_ref": task.get("package_ref")}
    if any(value is None or result.get(key) != value for key, value in expected.items()):
        return _unknown("The latest Result does not match the Task, attempt, assignment, and package.")
    if config is None:
        config = store.get_meta("config")
    answer = result_resume_eligibility(result, config)
    return {**answer, "result_ref": deepcopy(ref), "attempt_id": attempt}
