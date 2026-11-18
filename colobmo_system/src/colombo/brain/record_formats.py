"""Current Brain record and MCP payload formats; data versions remain unchanged."""
import copy
from colombo.cell.instructions import SPECIALIZATIONS
from colombo.brain.cell_evidence import RECORD_REF_SCHEMA


def obj(properties, required=None):
    return {"type": "object", "properties": properties, "required": list(properties) if required is None else required,
            "additionalProperties": False}


TEXT = {"type": "string", "minLength": 1, "maxLength": 100000, "pattern": r"\S"}
STRING = {"type": "string", "maxLength": 100000}
STRINGS = {"type": "array", "items": TEXT, "maxItems": 100}
REFS = {"type": "array", "items": TEXT, "uniqueItems": True, "maxItems": 100}
PACKAGE = obj({"background": STRING, "selection_reason": TEXT, "items": {"type": "array", "maxItems": 40,
    "items": obj({"ref": TEXT, "importance": {"enum": ["required", "reference"]}, "purpose": TEXT, "limitations": STRING})}})

IDS = {**REFS, "maxItems": 400}
STEP_ID = {"type": "string", "pattern": r"^[A-Za-z][A-Za-z0-9_.-]{0,63}$"}
RESPONSIBILITY = obj({"problem_id": TEXT, "claim": TEXT, "assumptions": STRINGS,
    "scope": TEXT, "goal_ids": {**REFS, "minItems": 1}, "proof_step_ids": IDS,
    "route_group": STRING, "retain": {"type": "boolean"}})

EVIDENCE = obj({"result_ref": TEXT, "path": TEXT,
    "locator": TEXT,
    "record_ref": RECORD_REF_SCHEMA}, required=["result_ref", "path", "locator"])
STEP = obj({"id": STEP_ID, "title": TEXT, "statement": TEXT,
    "status": {"enum": ["open", "draft", "checked", "blocked", "invalidated", "retired"]},
    "depends_on": IDS, "evidence": {"type": "array", "items": EVIDENCE, "maxItems": 100},
    "gaps": STRINGS})
PROOF = obj({"title": TEXT, "statement": TEXT, "assumptions": STRINGS,
    "body": TEXT, "steps": {"type": "array", "minItems": 1, "maxItems": 400, "items": STEP},
    "open_questions": STRINGS})
# A source is an alternative input, not a second copy of the manuscript. Storage
# materializes it once in the proof version; the verifier still sees its full text.
PROOF_INPUT = copy.deepcopy(PROOF)
PROOF_INPUT["properties"]["body_source"] = obj({"result_ref": TEXT, "path": TEXT})
PROOF_INPUT["required"].remove("body")
PROOF_INPUT["oneOf"] = [{"required": ["body"], "not": {"required": ["body_source"]}},
                         {"required": ["body_source"], "not": {"required": ["body"]}}]
ADMISSION = obj({"result_ref": TEXT,
    "verdict": {"enum": ["accepted", "partial", "rejected", "inconclusive", "conflict"]},
    "goal_ids": REFS, "proof_step_ids": IDS, "reason": TEXT,
    "completion_status": {"enum": ["completed", "partial", "incomplete", "unknown"]},
    "completed_parts": STRINGS, "remaining": STRINGS})
PREMISE = obj({"result_ref": TEXT, "statement": TEXT, "assumptions": STRINGS, "scope": TEXT})
PRUNE = obj({"task_id": TEXT, "attempt_id": TEXT,
    "reason": {"enum": ["redundant", "subsumed", "refuted_target"]},
    "evidence_refs": {**REFS, "minItems": 1}, "relation_explanation": TEXT,
    "scope_check": TEXT, "covered_deliverables": {**STRINGS, "minItems": 1},
    "premises": {"type": "array", "items": PREMISE, "minItems": 1, "maxItems": 100},
    "audit_ref": TEXT}, required=["task_id", "attempt_id", "reason", "evidence_refs",
        "relation_explanation", "scope_check", "covered_deliverables", "premises", "audit_ref"])

ACTIVE_TASK_STATES = {"prepared", "queued", "running"}

TASK = obj({"title": TEXT, "instructions": TEXT, "deliverables": {**STRINGS, "minItems": 1},
    "completion_criteria": {**STRINGS, "minItems": 1}, "mode": {"enum": ["new", "resume", "restart"]},
    "resume_task_id": {"type": ["string", "null"]}, "package": copy.deepcopy(PACKAGE),
    "specialization": {"enum": list(SPECIALIZATIONS)}, "responsibility": RESPONSIBILITY},
    required=["title", "instructions", "deliverables", "completion_criteria", "mode", "resume_task_id",
              "package", "responsibility"])
TASK["properties"]["package"]["properties"]["items"]["items"]["properties"]["artifact_paths"] = STRINGS
TASK["properties"]["package"]["properties"]["regime_ids"] = STRINGS

NULLREF = {"type": ["string", "null"]}
SETTING = obj({"specification": {"type": "object", "minProperties": 1},
    "provenance": {"type": "array", "items": obj({"entry": TEXT, "source": TEXT,
        "status": {"enum": ["provided", "completed", "unknown"]}})},
    "unknowns": STRINGS, "near_optimal_policy": TEXT})
PLAN = obj({"rationale": TEXT, "tasks": {"type": "array", "maxItems": 40, "items": TASK},
            "setting_specification": SETTING}, required=["rationale", "tasks"])
BOUND_DESCRIPTION = obj({"direction": {"enum": ["upper_bound", "lower_bound"]},
    "expression": TEXT, "scope": TEXT, "assumptions": STRINGS})
CLAIM = obj({"id": TEXT, "statement": TEXT, "assumptions": STRINGS, "scope": TEXT,
    "kind": {"enum": ["upper_bound", "lower_bound", "lemma", "comparison", "empirical"]},
    "expression": STRING, "evidence_paths": STRINGS})
# Optional for other Claims; mandatory for a mathematical comparison. Use the
# complete Bound descriptions instead of future Brain-assigned IDs, which do
# not yet exist when a returned Result is reviewed.
CLAIM["properties"]["comparison_bounds"] = {"type": "array", "minItems": 2,
    "items": BOUND_DESCRIPTION}
REVIEW = obj({"verdict": {"enum": ["pass", "revise", "inconclusive"]}, "summary": TEXT,
    "findings": {"type": "array", "maxItems": 100,
        "items": obj({"subject": TEXT, "reason": TEXT, "result_refs": REFS})}, "checked_refs": {**REFS, "maxItems": 10000},
    "review_kind": {"enum": ["result", "proof"]}, "result_ref": NULLREF,
    "confirmed_claims": {"type": "array", "items": CLAIM},
    "completion_status": {"enum": ["completed", "partial", "incomplete", "unknown"]},
    "repair_kind": {"enum": ["none", "presentation", "research"]}})
BOUND = obj({"id": TEXT, "direction": {"enum": ["upper_bound", "lower_bound"]},
    "expression": TEXT, "scope": TEXT, "assumptions": STRINGS, "source": TEXT,
    "evidence_state": {"enum": ["baseline", "certified", "unknown"]},
    "result_ref": NULLREF, "review_ref": NULLREF, "claim_id": NULLREF})
REGIME = obj({"id": TEXT, "scope": TEXT, "lower_bound_ids": REFS, "upper_bound_ids": REFS,
    "gap": TEXT, "candidate_rate": STRING, "candidate_basis": STRING,
    "status": {"enum": ["open", "partial", "near_optimal", "unknown"]},
    "comparison_review_ref": NULLREF, "comparison_claim_id": NULLREF, "remaining": STRINGS})
REGIME["properties"]["assumptions"] = STRINGS
PROGRESS = obj({"overall": TEXT, "status": {"enum": ["in_progress", "completed"]},
    "items": {"type": "array", "items": obj({"goal_id": TEXT, "description": TEXT,
        "status": {"enum": ["open", "in_progress", "partial", "supported", "refuted", "unknown"]},
        "result_refs": REFS, "remaining": STRINGS})},
    "bracket": obj({"bounds": {"type": "array", "items": BOUND},
        "regimes": {"type": "array", "items": REGIME}}), "remaining": STRINGS})
UPDATE = obj({"admissions": {"type": "array", "items": ADMISSION}, "progress": PROGRESS})
OBSERVATION = obj({"summary": TEXT, "result_refs": REFS, "update": UPDATE,
    "prunes": {"type": "array", "items": PRUNE},
    "next_action": {"enum": ["continue", "plan", "conclude"]}, "rationale": TEXT})
INTEGRATION = copy.deepcopy(OBSERVATION)
INTEGRATION["properties"]["update"]["properties"].update(proof_draft=PROOF_INPUT,
    rechecked_step_ids=REFS)
INTEGRATION["properties"]["update"]["required"] += ["proof_draft", "rechecked_step_ids"]
SCHEMAS = {"plan": PLAN, "process_results": OBSERVATION, "integrate": INTEGRATION,
           "verify-progress": REVIEW}

