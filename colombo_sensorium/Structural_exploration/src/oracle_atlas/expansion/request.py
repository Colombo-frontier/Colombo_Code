"""Explicit finite discovery scope; these limits are scheduling choices, not scientific thresholds."""
from __future__ import annotations

from datetime import date

from ..core.contracts import ProtocolError, validate

OPERATORS = ("oracle_substitution", "noise_protocol", "model_transfer", "layer_transfer", "target_change", "resource_change", "boundary_probe", "algorithm_permission")
AXES = ("TASK", "MODEL", "ORACLE", "ALGORITHMS", "OUTPUT", "METRIC", "GUARANTEE", "RESOURCE")


def normalize_request(value: dict) -> dict:
    request = {
        "source_task_ids": [], "target_task_ids": [], "seed_setting_ids": [],
        "allowed_operators": list(OPERATORS), "allowed_axes": list(AXES),
        "fixed_constraints": [], "scope_description": "", "priority": "balanced",
        "cutoff_date": date.today().isoformat(), "max_seeds": 8, "max_neighbors_per_seed": 6,
        "max_opportunities": 24, "max_candidates": 16, "max_profiles": 10,
        "max_mutation_steps": 1, "max_per_seed": 3, "max_per_operator": 5,
        "allow_existing_updates": False, "run_label": "",
        **value,
    }
    validate("expansion_request", request)
    try:
        date.fromisoformat(request["cutoff_date"])
    except ValueError as exc:
        raise ProtocolError("cutoff_date must be a real calendar date") from exc
    if not request["max_profiles"] <= request["max_candidates"] <= request["max_opportunities"]:
        raise ProtocolError("Require max_profiles <= max_candidates <= max_opportunities")
    return request
