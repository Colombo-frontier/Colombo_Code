"""Apply explicit budget and diversity constraints to LLM-ranked opportunities."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import math


def _limit(request: dict, name: str, default: int) -> int:
    value = request.get(name, default)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _list(value, name):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
        raise ValueError(f"{name} must contain nonempty strings")
    return list(dict.fromkeys(value))


def select_opportunities(plan: dict, request: dict) -> dict:
    """Select at most ``max_candidates`` for complete candidate formulation.

    Scores are supplied by the planning Agent and have no evidentiary status.
    The returned objects are copies. Deferred means not selected in this wave,
    not mathematically invalid or absent from the literature. Final identity and
    research value require their independent LLM reviews.
    """
    opportunities = plan.get("opportunities", [])
    if not isinstance(opportunities, list):
        raise ValueError("plan.opportunities must be an array")
    pool_cap = _limit(request, "max_opportunities", 24)
    cap = _limit(request, "max_candidates", 16)
    seed_cap = _limit(request, "max_per_seed", 3)
    operator_cap = _limit(request, "max_per_operator", 5)
    steps_cap = _limit(request, "max_mutation_steps", 1)
    if len(opportunities) > pool_cap:
        raise ValueError("The planning output exceeds max_opportunities; revise the formal plan")
    allowed_operators = set(_list(request.get("allowed_operators", []), "allowed_operators"))
    allowed_axes = set(_list(request.get("allowed_axes", []), "allowed_axes"))
    allowed_targets = set(_list(request.get("target_task_ids", []), "target_task_ids"))
    allowed_seeds = set(_list(request.get("seed_setting_ids", []), "seed_setting_ids"))
    seen = set()
    entries = []
    for index, op in enumerate(opportunities):
        if not isinstance(op, dict) or not isinstance(op.get("opportunity_id"), str) or not op["opportunity_id"]:
            raise ValueError("Every opportunity requires a nonempty opportunity_id")
        oid = op["opportunity_id"]
        if oid in seen:
            raise ValueError(f"Duplicate opportunity_id: {oid}")
        seen.add(oid)
        score = op.get("priority_score")
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score) or not 0 <= score <= 100:
            raise ValueError(f"{oid}: priority_score must be a finite number in [0, 100]")
        steps = op.get("mutation_steps")
        if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
            raise ValueError(f"{oid}: mutation_steps must be a positive integer")
        fields = {name: _list(op.get(name, []), f"{oid}.{name}") for name in ("seed_setting_ids", "operators", "changed_axes", "target_task_ids")}
        if not fields["seed_setting_ids"] or not fields["operators"] or not fields["changed_axes"] or not fields["target_task_ids"]:
            raise ValueError(f"{oid}: seed, operator, changed axes, and target task declarations must be nonempty")
        entries.append((index, op, fields))
    entries.sort(key=lambda item: (-item[1]["priority_score"], item[0]))
    selected, deferred = [], []
    seed_use: Counter = Counter()
    operator_use: Counter = Counter()
    for _, op, fields in entries:
        reasons = []
        if allowed_seeds and not set(fields["seed_setting_ids"]).issubset(allowed_seeds):
            reasons.append("uses seed settings outside the explicit request")
        if allowed_operators and not set(fields["operators"]).issubset(allowed_operators):
            reasons.append("uses an operator outside the requested scope")
        if allowed_axes and not set(fields["changed_axes"]).issubset(allowed_axes):
            reasons.append("changes an axis outside the requested scope")
        if allowed_targets and not set(fields["target_task_ids"]).issubset(allowed_targets):
            reasons.append("targets a task outside the requested scope")
        if op["mutation_steps"] > steps_cap:
            reasons.append("exceeds max_mutation_steps")
        if not reasons and len(selected) >= cap:
            reasons.append("max_candidates reached for this wave")
        if not reasons and any(seed_use[s] >= seed_cap for s in fields["seed_setting_ids"]):
            reasons.append("max_per_seed reached for this wave")
        if not reasons and any(operator_use[o] >= operator_cap for o in fields["operators"]):
            reasons.append("max_per_operator reached for this wave")
        if reasons:
            deferred.append({"opportunity_id": op["opportunity_id"], "reason": "; ".join(reasons)})
            continue
        selected.append(deepcopy(op))
        seed_use.update(fields["seed_setting_ids"])
        operator_use.update(fields["operators"])
    return {"selected": selected, "deferred": deferred}
