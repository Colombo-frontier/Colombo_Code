"""Pinned, independently reviewable context deltas, never automatic approval.

The controller proves only that the previously read formal mathematical
material is unchanged. The new independent reviewer must assess every changed
assumption/application and every newly visible issue and sign a fresh scope.
"""
from ..core.contracts import references, resolve_pointer
from ..core.store import digest, dumps
from .review_context import _get, _Unavailable


EXPLICIT_SCOPE = "standalone_proposition_explicit_context"


def declared_context(snapshot, approval):
    values = {p: resolve_pointer(snapshot["profile"], p) for p in approval["context_pointers"]}
    if approval["scope"] != EXPLICIT_SCOPE:
        values["/parameters"] = snapshot["profile"].get("parameters")
    return values


def mathematical_dependencies(artifacts, roots):
    """Traverse formal mathematical edges; workflow history remains separate."""
    from .proof_reuse import MAX_PROOF_REFERENCES
    pending = set(roots)
    seen, rows = set(), []
    while pending:
        item_ref = pending.pop()
        if item_ref in seen:
            continue
        seen.add(item_ref)
        if len(seen) > MAX_PROOF_REFERENCES:
            raise _Unavailable("scope_revalidation_dependency_limit")
        item = _get(artifacts, item_ref)
        if item["kind"] not in {"proof", "result", "source"}:
            continue
        data = item["data"]
        rows.append({"ref": item_ref, "kind": item["kind"]})
        if item["kind"] == "proof":
            pending.update(data.get("dependencies", []))
        elif item["kind"] == "result":
            pending.update(data.get("proof_refs", []))
            pending.update(data.get("source_refs", []))
            pending.update(row["source_ref"] for row in data.get("source_locators", []))
    rows.sort(key=lambda row: row["ref"])
    return rows


def scientific_material(artifacts, snapshot, ref, approval):
    """Hash formal proof/result/source support, excluding workflow provenance.

    Direct defects are checked by the ordinary current contract as well. Any
    different formal proof, source or result requires full mathematical review.
    New contextual issues are retained separately for explicit impact review.
    """
    from .proof_reuse import BLOCKING, _structured_issues
    rows = mathematical_dependencies(artifacts, {ref} | references(declared_context(snapshot, approval)))
    for row in rows:
        if any(BLOCKING.intersection(issue["blocks"]) for issue in _structured_issues(_get(artifacts, row["ref"])["data"])):
            raise _Unavailable("scope_revalidation_direct_dependency_defect")
    return {"fingerprint": digest(rows), "dependencies": rows}


def context_changes(prior, current, approval):
    before, after = declared_context(prior, approval), declared_context(current, approval)
    changes, truncated = [], False
    missing = {"__missing_context_value__": True}

    def value(v):
        encoded = dumps(v)
        return {"digest": digest(v), "excerpt": encoded[:2400], "truncated": len(encoded) > 2400}

    def walk(a, b, path):
        nonlocal truncated
        if a == b:
            return
        if len(changes) >= 64:
            truncated = True
            return
        if isinstance(a, dict) and isinstance(b, dict):
            for key in sorted(a.keys() | b.keys()):
                walk(a.get(key, missing), b.get(key, missing), path + "/" + key.replace("~", "~0").replace("/", "~1"))
        elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
            for index, (left, right) in enumerate(zip(a, b)):
                walk(left, right, path + "/" + str(index))
        else:
            changes.append({"pointer": path, "before": value(a), "after": value(b)})

    for pointer in sorted(before):
        walk(before[pointer], after[pointer], pointer)
    return {"changes": changes, "truncated": truncated, "previous_context_digest": digest(before),
            "current_context_digest": digest(after),
            "previous_profile_ref": prior["proposal"]["profile_ref"],
            "current_profile_ref": current["proposal"]["profile_ref"],
            "complete_context_pointers": sorted(before)}


def revalidation_candidate(artifacts, prior, current, review_ref, ref, approval,
                           prior_issues, current_issues, current_occurrences):
    from .issue_semantics import occurrence_signature, verified_delivery_lineage
    proof_id = _get(artifacts, ref, "proof")["data"]["proof_id"]
    if any({ref, proof_id}.intersection(issue["subject_refs"]) for issue in current_issues.values()):
        return None  # A direct unresolved proof defect cannot be an unaffected-scope shortcut.
    previous = scientific_material(artifacts, prior, ref, approval)
    now = scientific_material(artifacts, current, ref, approval)
    if previous != now or prior["prepared"].get("semantics_version") != current["prepared"].get("semantics_version"):
        return None
    lineage = verified_delivery_lineage(prior, current, review_ref)
    added = [row["occurrence_id"] for row in current_occurrences
             if occurrence_signature(row, current, lineage=lineage) not in
             prior_issues.get(row["issue_id"], {}).get("occurrence_signatures", [])]
    delta = context_changes(prior, current, approval)
    if not delta["changes"] and not delta["truncated"] and not added:
        return None
    body = {"proof_ref": ref, "previous_review_ref": review_ref, "previous_proposal_ref": prior["ref"],
            "current_proposal_ref": current["ref"], "previous_approval": approval,
            "scientific_material_fingerprint": now["fingerprint"], "scientific_dependencies": now["dependencies"],
            "context_changes": delta, "new_issue_occurrence_ids": sorted(added),
            "current_issue_signatures": {iid: {key: row[key] for key in ("variant_signatures", "occurrence_signatures")}
                                         for iid, row in sorted(current_issues.items())},
            "review_requirement": "Read changed contexts and newly visible issue occurrences, reconsider every old assumption including any excluded from the new explicit scope, verify the current application, and explicitly sign a new complete scope. This is not an unchanged-context reuse credential."}
    return {"candidate_id": "scope-revalidation:" + digest(body), **body}
