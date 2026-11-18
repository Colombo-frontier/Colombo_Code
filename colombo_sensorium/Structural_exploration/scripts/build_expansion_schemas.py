"""Build the small expansion contracts; scientific specifications reuse the base candidate schema."""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = {"type": "string", "minLength": 1}
R = {"type": "string", "pattern": "^sha256:[a-f0-9]{64}$"}
N = {"anyOf": [R, {"type": "null"}]}
AXES = ["TASK", "MODEL", "ORACLE", "ALGORITHMS", "OUTPUT", "METRIC", "GUARANTEE", "RESOURCE"]
OPERATORS = ["oracle_substitution", "noise_protocol", "model_transfer", "layer_transfer", "target_change", "resource_change", "boundary_probe", "algorithm_permission"]

def array(item, **kw):
    return {"type": "array", "items": item, **kw}

def obj(properties, required=None, extra=False):
    return {"type": "object", "properties": properties, "required": list(properties) if required is None else required, "additionalProperties": extra}

def enum(*values):
    return {"type": "string", "enum": list(values)}

def positive(maximum):
    return {"type": "integer", "minimum": 1, "maximum": maximum}

def build():
    issue = deepcopy(json.loads((ROOT / "schemas/candidate.schema.json").read_text())["properties"]["issues"]["items"])
    issue["properties"]["blocks"]["items"]["enum"].append("expansion")
    request = obj({
        "source_task_ids": array(S, uniqueItems=True), "target_task_ids": array(S, uniqueItems=True),
        "seed_setting_ids": array(S, uniqueItems=True), "allowed_operators": array(enum(*OPERATORS), minItems=1, uniqueItems=True),
        "allowed_axes": array(enum(*AXES), minItems=1, uniqueItems=True), "fixed_constraints": array(S),
        "scope_description": {"type": "string"}, "priority": enum("balanced", "classical", "gaps"),
        "cutoff_date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
        "max_seeds": positive(40), "max_neighbors_per_seed": positive(30), "max_opportunities": positive(80),
        "max_candidates": positive(40), "max_profiles": positive(20), "max_mutation_steps": positive(2),
        "max_per_seed": positive(40), "max_per_operator": positive(40),
        "allow_existing_updates": {"type": "boolean"}, "run_label": {"type": "string"},
    })
    opportunity = obj({
        "opportunity_id": S, "title": S, "seed_setting_ids": array(S, minItems=1, uniqueItems=True),
        "neighbor_setting_ids": array(S, uniqueItems=True), "operators": array(enum(*OPERATORS), minItems=1, uniqueItems=True),
        "changed_axes": array(enum(*AXES), minItems=1, uniqueItems=True), "target_task_ids": array(S, minItems=1, uniqueItems=True),
        "mutation_steps": positive(2), "transformation": S, "selection_reason": S, "expected_value": S,
        "transfer_leads": array(S), "risks": array(S), "priority_score": {"type": "integer", "minimum": 0, "maximum": 100},
    })
    origin = obj({"kind": {"const": "atlas_expansion"}, "request_ref": R, "plan_ref": R,
                  "opportunity_id": S, "seed_refs": array(R, minItems=1, uniqueItems=True), "designed_contract": {"const": True}}, extra=True)
    schemas = {
        "expansion_request": request,
        "expansion_origin": origin,
        "expansion_plan": obj({"request_ref": R, "neighborhood_ref": R,
            "opportunities": array(opportunity), "not_pursued": array(obj({"direction": S, "reason": S})), "coverage_note": S}),
        "expansion": obj({"request_ref": R, "plan_ref": R, "opportunity_id": S, "candidate_ref": R,
            "changes": array(obj({"axis": enum(*AXES), "object_ref": {"type": ["string", "null"]}, "before": S, "after": S, "reason": S}), minItems=1),
            "well_posedness": obj({"nonempty": enum("supported", "unresolved"), "objective_defined": enum("supported", "unresolved"),
                "oracle_implementable": enum("supported", "unresolved"), "not_trivial": enum("supported", "unresolved"), "checks": array(S, minItems=1), "unknowns": array(S)}),
            "selection_reason": S, "issues": array(issue)}),
        "expansion_review": obj({"subject_ref": R, "candidate_ref": R, "verdict": enum("approve", "revise", "defer", "exclude"),
            "reason": S, "scope_assessment": S, "well_posedness_assessment": S, "value_assessment": S,
            "pending_comparisons": array(obj({"candidate_ref": R, "relation": enum("distinct", "equivalent", "unresolved"), "reason": S})),
            "duplicate_of_ref": N, "issues": array(issue), "required_changes": array(S)}),
    }
    candidate_path = ROOT / "schemas/candidate.schema.json"
    candidate_schema = json.loads(candidate_path.read_text())
    candidate_schema["properties"]["origin"] = origin
    candidate_path.write_text(json.dumps(candidate_schema, indent=2) + "\n")
    for name, schema in schemas.items():
        (ROOT / "schemas" / f"{name}.schema.json").write_text(json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema", "title": name, **schema}, indent=2) + "\n")
    return len(schemas)

if __name__ == "__main__":
    print(f"{build()} expansion schemas written")
