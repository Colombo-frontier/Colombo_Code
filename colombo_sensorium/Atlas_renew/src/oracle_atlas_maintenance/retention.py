"""Narrow comparison projections; actual frozen objects and hashes stay intact.

Identity equality is a conditional baseline premise, not mathematical approval.
New quantity-role interpretations and new adoptions still require independent
review of the actual prepared profile and its complete recorded premises.
"""
from copy import deepcopy
import json

from .normalization import apply_quantity_normalizations
from .state import digest


def retention_projection(baseline, proposed, report):
    from .contracts import IMMUTABLE, row_id
    from .delta_classification import classify_delta

    left, right = deepcopy(baseline), deepcopy(proposed)
    operations, reasons, reads = [], [], {}

    def obligation(artifact, pointer, value, role, operation_hash):
        key = (artifact, pointer)
        item = reads.setdefault(key, {"artifact": artifact, "pointer": pointer,
                                      "sha256": digest(value), "role": role,
                                      "operation_sha256s": []})
        if item["sha256"] != digest(value):
            raise ValueError("Conflicting exact retention premise")
        if operation_hash not in item["operation_sha256s"]:
            item["operation_sha256s"].append(operation_hash)

    normalization_ops = report.get("quantity_metadata_normalizations", [])
    if normalization_ops:
        normalized, _ = apply_quantity_normalizations(baseline, normalization_ops)
        if any(proposed.get(key) != normalized.get(key) for key in IMMUTABLE):
            raise ValueError("Conditional retention requires the exact validated quantity-normalization fixed contract")
        for op in normalization_ops:
            qid, op_hash = op["quantity_id"], digest(op)
            old_matches = [(i, q) for i, q in enumerate(baseline.get("quantities", []))
                           if row_id(q, "quantities") == qid]
            new_matches = [(i, q) for i, q in enumerate(proposed.get("quantities", []))
                           if row_id(q, "quantities") == qid]
            if len(old_matches) != 1 or len(new_matches) != 1:
                raise ValueError("Retention normalization requires unique stable quantity IDs")
            old_index, old = old_matches[0]
            new_index, new = new_matches[0]
            updates = json.loads(op["changes_json"])
            fields = sorted(key for key in updates
                            if (key in old) != (key in new) or old.get(key) != new.get(key))
            # Only explicitly changed, validated presentation keys disappear
            # from BOTH comparison copies. All unmentioned metadata survives.
            for profile, index in ((left, old_index), (right, new_index)):
                for key in fields:
                    profile["quantities"][index].pop(key, None)
            old_pointer, new_pointer = f"/quantities/{old_index}", f"/quantities/{new_index}"
            record = {"quantity_id": qid, "operation_sha256": op_hash, "fields": fields,
                      "baseline_quantity_sha256": digest(old), "prepared_quantity_sha256": digest(new),
                      "baseline_pointer": old_pointer, "prepared_pointer": new_pointer,
                      "semantic_preservation_argument": op["semantic_preservation_argument"],
                      "proof_refs": deepcopy(op["proof_refs"])}
            operations.append(record)
            reasons.append({"kind": "validated_quantity_metadata_normalization", "quantity_id": qid,
                            "operation_sha256": op_hash, "fields": fields})
            obligation("baseline", old_pointer, old, "old_quantity", op_hash)
            obligation("prepared", new_pointer, new, "new_quantity", op_hash)
            for pid in op["proof_refs"]:
                matches = [(i, p) for i, p in enumerate(baseline.get("proofs", []))
                           if row_id(p, "proofs") == pid]
                if len(matches) != 1:
                    raise ValueError("Retention normalization needs unique frozen proof references")
                index, proof = matches[0]
                obligation("baseline", f"/proofs/{index}", proof, "normalization_proof", op_hash)

    classification = classify_delta(baseline, proposed, report)
    adoption_ids = set(classification["adoption_only_bound_ids"])
    for profile in (left, right):
        for bound in profile.get("bounds", []):
            if row_id(bound, "bounds") in adoption_ids:
                bound.pop("selected_in_regimes", None)
    reasons.extend({"kind": "validated_monotone_adoption_only", **deepcopy(update)}
                   for update in classification["adoption_updates"])
    return left, right, reasons, operations, list(reads.values())
