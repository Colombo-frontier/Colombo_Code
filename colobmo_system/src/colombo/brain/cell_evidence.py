"""Resolve pinned Cell records inside a Result's immutable memory snapshot.

This reader resolves identity and version, not mathematical correctness. Trust and
dependency references are returned exactly as exported by that Cell attempt;
they do not grant access to other snapshots or to the Cell's live memory.
"""
from __future__ import annotations

import copy
import json



# Cell prover/mcp/store.py READABLE_KINDS. Keep this reader independent
# of the Cell runtime (and of contracts, which reuse RECORD_REF_SCHEMA).
RECORD_KINDS = frozenset({
    "claims", "arguments", "examples", "attempts", "sources", "proof_state",
    "experiment_result", "reviews", "events",
})
_REF_FIELDS = ("kind", "id", "revision")
RECORD_REF_SCHEMA = {
    "type": "object",
    "properties": {
        "kind": {"type": "string", "enum": sorted(RECORD_KINDS)},
        "id": {"type": "string", "minLength": 1, "pattern": r"\S"},
        "revision": {"type": "integer", "minimum": 1},
    },
    "required": list(_REF_FIELDS),
    "additionalProperties": False,
}


class EvidenceError(ValueError):
    """A record reference or its authorized snapshot failed validation."""


def _check_ref(ref):
    if not isinstance(ref, dict) or set(ref) != set(_REF_FIELDS):
        raise EvidenceError("record_ref requires exactly kind, id, revision")
    if not isinstance(ref["kind"], str) or ref["kind"] not in RECORD_KINDS:
        raise EvidenceError("record_ref kind is not a readable Cell collection")
    if not isinstance(ref["id"], str) or not ref["id"].strip():
        raise EvidenceError("record_ref id must be a nonempty string")
    if type(ref["revision"]) is not int or ref["revision"] < 1:
        raise EvidenceError("record_ref revision must be a positive integer")


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise EvidenceError(f"Duplicate snapshot JSON field: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise EvidenceError(f"Snapshot must contain finite JSON data: {value}")


def resolve_record(store, result_ref, path, record_ref):
    """Return one exact full envelope, including its snapshot-time current_trust.

    There is no latest-revision fallback or dependency expansion.
    The caller remains responsible for its role's Result access permissions.
    """
    _check_ref(record_ref)
    if not isinstance(path, str) or not path.strip():
        raise EvidenceError("Snapshot path must be a nonempty string")
    try:
        result = store.record_ref(result_ref)
        if store.record_kind(result) != "result":
            raise EvidenceError("Cell record evidence requires a Result reference")
        matches = [entry for entry in store.artifact_entries(result) if entry["path"] == path]
        if len(matches) != 1:
            raise EvidenceError("Snapshot must be a unique artifact authorized by this Result")
        entry = matches[0]
        if entry.get("kind") != "research_memory_snapshot":
            raise EvidenceError("Record evidence requires a research_memory_snapshot artifact")
        data = store.safe_path(path, exists=True).read_bytes()
        snapshot = json.loads(data.decode("utf-8-sig"), object_pairs_hook=_object,
                              parse_constant=_reject_constant)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EvidenceError("Cannot read a valid UTF-8 JSON memory snapshot") from exc
    if (not isinstance(snapshot, dict) or type(snapshot.get("schema_version")) is not int
            or snapshot["schema_version"] != 2 or not isinstance(snapshot.get("records"), list)):
        raise EvidenceError("Expected memory snapshot schema_version 2 with a records list")

    selected = None
    identities = set()
    target = tuple(record_ref[field] for field in ("kind", "id", "revision"))
    for record in snapshot["records"]:
        if not isinstance(record, dict):
            raise EvidenceError("Snapshot records must be Cell record objects")
        reference = {field: record[field] for field in _REF_FIELDS if field in record}
        _check_ref(reference)
        identity = tuple(reference[field] for field in ("kind", "id", "revision"))
        if identity in identities:
            raise EvidenceError("Duplicate Cell record identity in snapshot")
        identities.add(identity)
        if identity == target:
            selected = record
    if selected is None:
        raise EvidenceError("Exact Cell record revision is absent from the authorized snapshot")
    if not isinstance(selected.get("payload"), dict):
        raise EvidenceError("Cell record payload must be a JSON object")
    return copy.deepcopy(selected)


def read_record_evidence(store, result_ref, path, record_ref, offset=0, limit=12000):
    """Read a character page of the selected full record, never the whole snapshot."""
    if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 100000:
        raise EvidenceError("Invalid read range")
    record = resolve_record(store, result_ref, path, record_ref)
    text = json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
    return {"text": text[offset:offset+limit], "path": path,
            "record_ref": copy.deepcopy(record_ref), "offset": offset,
            "total_chars": len(text), "truncated": offset+limit < len(text)}
