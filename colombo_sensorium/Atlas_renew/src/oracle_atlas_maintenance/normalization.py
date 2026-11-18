"""Narrow, reviewed corrections to quantity presentation metadata.

This never changes the mathematical task, a quantity expression, a comparison
key, an oracle, or a parameter domain. Equivalence of distinct quantities still
requires a new bound with a reviewed conversion, not a string-based merge.
"""
from copy import deepcopy
import json

from .state import digest

ALLOWED_FIELDS = frozenset({"tracked_parameters", "fixed_parameters", "analysis_scope"})


def apply_quantity_normalizations(baseline, operations):
    proposed = deepcopy(baseline)
    changes, seen = [], set()
    known_parameters = {p.get("id", p.get("parameter_id")) for p in baseline.get("parameters", [])}
    known_parameters.discard(None)
    known_proofs = {p.get("id", p.get("proof_id")) for p in baseline.get("proofs", [])}
    for op in operations:
        qid = op["quantity_id"]
        if qid in seen:
            raise ValueError("Duplicate quantity metadata normalization")
        seen.add(qid)
        matches = [(i, q) for i, q in enumerate(proposed.get("quantities", []))
                   if q.get("id", q.get("quantity_id")) == qid]
        if len(matches) != 1:
            raise ValueError("Normalization must identify exactly one existing quantity")
        index, old = matches[0]
        if op["before_hash"] != digest(old):
            raise ValueError("Quantity normalization before_hash does not bind the baseline")
        updates = json.loads(op["changes_json"])
        if not isinstance(updates, dict) or not updates or set(updates) - ALLOWED_FIELDS:
            raise ValueError("Quantity normalization may change only tracked_parameters, fixed_parameters, analysis_scope")
        if not op["semantic_preservation_argument"].strip():
            raise ValueError("Normalization needs an explicit argument preserving the mathematical contract")
        if set(op["proof_refs"]) - known_proofs:
            raise ValueError("Normalization proof references must resolve in the frozen baseline")
        for field in ("tracked_parameters", "fixed_parameters"):
            if field in updates:
                refs = updates[field]
                if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs) or len(set(refs)) != len(refs):
                    raise ValueError("Quantity parameter metadata must contain unique parameter IDs")
                if set(refs) - known_parameters:
                    raise ValueError("Quantity normalization refers to an unknown parameter")
        new = {**old, **updates}
        if new == old:
            raise ValueError("Quantity normalization must make a concrete metadata correction")
        # tracked_parameters means recorded parameters, not necessarily varying ones.
        # The new joint_analysis target supplies the unambiguous quantifier roles.
        proposed["quantities"][index] = new
        changes.append({"collection": "quantities", "id": qid,
                        "before_hash": digest(old), "after_hash": digest(new)})
    if changes:
        log = deepcopy(proposed.get("quantity_metadata_normalization_log", []))
        log.append({"operations": deepcopy(operations), "changes": changes,
                    "note": "Proposed metadata normalization; adoption is bound by the independent native transaction review."})
        proposed["quantity_metadata_normalization_log"] = log
    return proposed, changes
