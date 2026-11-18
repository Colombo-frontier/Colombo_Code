"""Describe raw JSON inputs without coercing or filling their replay identity."""
from copy import deepcopy
from typing import Annotated

from pydantic import Field



WRITABLE_KINDS = frozenset({
    "claims", "arguments", "examples", "attempts", "sources", "proof_state", "experiment_result",
})
READABLE_KINDS = WRITABLE_KINDS | {"reviews", "events"}
ALIASES = {
    "claim": "claims", "argument": "arguments", "example": "examples",
    "attempt": "attempts", "source": "sources", "review": "reviews",
    "event": "events",
}
OBLIGATION_WORK_STATUSES = (
    "active", "pending", "paused", "suspended", "cancelled", "abandoned", "superseded", "completed",
)

def _object(properties, required):
    return {"type": "object", "properties": properties, "required": required,
            "additionalProperties": False}


TEXT = {"type": "string", "minLength": 1}
PROPERTIES = {"type": "array", "items": TEXT, "minItems": 1, "uniqueItems": True}
KINDS = sorted(READABLE_KINDS | set(ALIASES))
WRITABLE = sorted(WRITABLE_KINDS | {k for k, v in ALIASES.items() if v in WRITABLE_KINDS})
FIXED_REF = _object({"kind": {"enum": KINDS}, "id": TEXT,
                     "revision": {"type": "integer", "minimum": 1},
                     "property_ids": PROPERTIES}, ["kind", "id", "revision"])
LOCAL_REF = _object({"local_key": TEXT, "property_ids": PROPERTIES}, ["local_key"])
BATCH_REF = {"anyOf": [FIXED_REF, LOCAL_REF]}
CLAIM_REF = {**FIXED_REF, "properties": {**FIXED_REF["properties"],
             "kind": {"enum": ["claim", "claims"]}}}
EXAMPLE_REF = {**FIXED_REF, "properties": {**FIXED_REF["properties"],
               "kind": {"enum": ["example", "examples"]}},
               "required": ["kind", "id", "revision", "property_ids"]}


def proof_state_schema(*, allow_local=False):
    def reference(kind=None, nullable=False):
        fixed = deepcopy(FIXED_REF)
        if kind:
            fixed["properties"]["kind"] = {"enum": sorted(
                {kind} | {alias for alias, target in ALIASES.items() if target == kind})}
        branches = [fixed]
        if allow_local:
            branches.append(LOCAL_REF)
        if nullable:
            branches.append({"type": "null"})
        return branches[0] if len(branches) == 1 else {"anyOf": branches}

    obligation = {
        "type": "object", "additionalProperties": True,
        "required": ["id", "target_claim_ref"],
        "properties": {
            "id": TEXT,
            "target_claim_ref": reference("claims"),
            "expected_relation": {"enum": ["supports", "refutes"],
                                  "description": "Omission means supports."},
            "work_status": {"type": "string", "enum": list(OBLIGATION_WORK_STATUSES),
                "description": "Work status only, not a mathematical verdict. Omission means active; "
                    "in_progress is not a supported value. No default is inserted into the saved request."},
            "owner_attempt_ref": reference("attempts", nullable=True),
            "closing_argument_ref": reference("arguments", nullable=True),
            "evidence_refs": {"type": "array", "items": reference()},
        },
        "not": {"anyOf": [{"required": [name]} for name in
            ("mathematical_state", "satisfaction", "satisfied", "current_trust")]},
    }
    route = {"type": "object", "additionalProperties": True,
             "required": ["route_id", "target_claim_ref"],
             "properties": {"route_id": TEXT, "target_claim_ref": reference("claims"),
                            "obligations": {"type": "array", "items": obligation}}}
    return {"type": "object", "additionalProperties": True,
            "properties": {"routes": {"type": "array", "items": route,
                "description": "ProofState routes with distinct route_id values; each route's obligation ids are distinct."}}}


def proof_state_condition(*, allow_local=False):
    # Kind is a sibling of payload, both in archive and in each batch operation.
    # Other records may use routes/work_status as their own unconstrained fields.
    kinds = sorted({"proof_state"} | {key for key, value in ALIASES.items() if value == "proof_state"})
    return {"if": {"properties": {"kind": {"enum": kinds}}, "required": ["kind"]},
            "then": {"properties": {"payload": proof_state_schema(allow_local=allow_local)}}}


def archive_input_schema(schema):
    """Add cross-argument semantics to FastMCP's published schema only."""
    result = deepcopy(schema)
    result.setdefault("allOf", []).append(proof_state_condition())
    return result


def payload_schema(*, allow_local=False):
    branches = [
        _object({"target": CLAIM_REF, "relation": {"enum": ["supports", "refutes"]}}, ["target", "relation"]),
        _object({"target": EXAMPLE_REF, "relation": {"const": "supports"}}, ["target", "relation"]),
    ]
    if allow_local:
        # The referenced local operation's kind is resolved by the Store.
        branches.append(_object({"target": LOCAL_REF, "relation": {"enum": ["supports", "refutes"]}},
                                ["target", "relation"]))
    conclusion = {"oneOf": branches}
    return {"type": "object", "additionalProperties": True,
            "properties": {"conclusions": {"type": "array", "minItems": 1, "items": conclusion,
                "description": "Argument conclusions contain only target and relation; no proof text or verdict here."},
                # This payload schema is shared by all record kinds. Describe
                # the Attempt-only rule without restricting other extensions
                # or narrowing the Store's supported structured field values.
                "route_review": {
                    "description": "On attempts (alias attempt), this optional field must be an object, not a string. "
                        "When present, include nonempty decision and reason fields. For example: "
                        "{\"decision\": \"continue\", \"reason\": \"The remaining gap can now be checked.\"}. "
                        "The Store permits text or structured field values and has no fixed decision enum.",
                    "properties": {
                        "decision": {"description": "The route decision; required and nonempty when an Attempt has route_review."},
                        "reason": {"description": "Why that route decision is justified; required and nonempty when an Attempt has route_review."},
                    }}}}


_common = {"local_key": TEXT, "kind": {"enum": [x for x in WRITABLE if x != "experiment_result"]},
           "payload": payload_schema(allow_local=True), "record_id": {"type": ["string", "null"]}}
CREATE = _object({**_common, "op": {"const": "create"}, "expected_revision": {"type": "null"}},
                 ["local_key", "kind", "payload"])
UPDATE = _object({**_common, "op": {"const": "update"},
                  "record_id": TEXT,
                  "expected_revision": {"type": "integer", "minimum": 1}},
                 ["local_key", "op", "kind", "payload", "record_id", "expected_revision"])
for operation in (CREATE, UPDATE):
    operation["allOf"] = [proof_state_condition(allow_local=True)]
REFERENCE = _object({"local_key": TEXT, "op": {"const": "reference"}, "ref": BATCH_REF},
                    ["local_key", "op", "ref"])

# Field adds JSON Schema only. Plain dict/list values still reach the Store
# unchanged, including omitted op, kind aliases and local references.
ArchivePayload = Annotated[dict, Field(json_schema_extra=payload_schema())]
ArchiveOperations = Annotated[list[dict], Field(json_schema_extra={
    "type": "array", "minItems": 1, "items": {"oneOf": [CREATE, UPDATE, REFERENCE]}})]
