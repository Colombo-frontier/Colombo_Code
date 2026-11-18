"""Derive goal completion from an exact, explicit final review.

Open research questions stay in the immutable proof.  Only the final Verifier
can certify that they do not prevent completion of the original goal.
"""
from __future__ import annotations

import copy

from colombo.brain.research_store import StoreError
from colombo.shared.file_io import json_equal


def proof_steps_complete(proof):
    steps = proof.get("steps", [])
    active = [s for s in steps if s.get("status") != "retired"]
    return bool(active) and all(s.get("status") == "checked" and s.get("gaps") == []
                                for s in active)


def review_completes_goal(review):
    return (review.get("review_kind") == "proof" and review.get("result_ref") is None
            and review.get("verdict") == "pass"
            and review.get("completion_status") == "completed"
            and review.get("repair_kind") == "none" and review.get("findings") == [])


def reviewed_progress(progress, proof, review):
    """Normalize control fields only after an explicit completed-goal review."""
    value = copy.deepcopy(progress)
    if not review_completes_goal(review):
        return value
    if not proof_steps_complete(proof):
        return value
    regimes = value.get("bracket", {}).get("regimes", [])
    if (not regimes or any(r.get("status") != "near_optimal" or r.get("remaining")
                           or not r.get("lower_bound_ids") or not r.get("upper_bound_ids")
                           for r in regimes)):
        return value
    value["status"] = "completed"
    value["remaining"] = []
    for item in value["items"]:
        if item["status"] != "refuted":
            item["status"] = "supported"
        item["remaining"] = []
    if progress.get("status") != "completed" or progress.get("remaining"):
        value["overall"] = ("The original Goal is complete according to the final Verifier. "
                            "The adopted proof retains its disclosed open research questions.")
    return value


def final_progress_payload(store, stage, review_ref, previous_ref):
    """Check the fixed review scope before deriving a new progress version.

    The review is already stored beneath the proof version, although its adopted
    review_ref pointer is not set until the Controller commits the transition.
    """
    review_ref = store.record_ref(review_ref)
    proof_ref = store.record_ref(stage["proof_ref"])
    assessment_ref = store.record_ref(stage["assessment_ref"])
    package_ref = store.record_ref(stage["review_package_ref"])
    expected = ((review_ref, "review"), (proof_ref, "proof_draft"),
                (assessment_ref, "assessment"), (package_ref, "review_package"))
    if any(store.record_kind(ref) != kind for ref, kind in expected):
        raise StoreError("Final completion requires the fixed proof, assessment and review package")
    review = store.read_record(review_ref)
    proof = store.read_record(proof_ref)
    package = store.read_record(package_ref)
    assessment = store.read_record(assessment_ref)
    public_assessment = store.public_read(assessment_ref)
    if (package.get("review_kind") != "proof"
            or not json_equal(package.get("proof_ref"), proof_ref)
            or not json_equal(package.get("proposal_ref"), assessment_ref)
            or not json_equal(proof.get("assessment_ref"), assessment_ref)
            or not json_equal(public_assessment.get("update", {}).get("proof_ref"), proof_ref)
            or not json_equal(proof.get("reviews", {}).get(review_ref["id"]), review)
            or not json_equal(proof.get("review_packages", {}).get(package_ref["id"]), package)):
        raise StoreError("Final review is not bound to this proof, assessment and package")
    lists = [package.get("required_checked_refs"), review.get("checked_refs"),
             package.get("allowed_refs")]
    if any(not isinstance(items, list) or not all(isinstance(r, str) for r in items)
           or len(items) != len(set(items)) for items in lists):
        raise StoreError("Final review evidence must use unique reference ID lists")
    required, checked, allowed = map(set, lists)
    core_refs = [store.get_meta("goal_ref"), store.get_meta("setting_ref"),
                 proof_ref, assessment_ref, *store.get_meta("material_refs", [])]
    if (any(not ref for ref in core_refs)
            or not {ref["id"] for ref in core_refs}.issubset(required)
            or not required.issubset(checked) or not checked.issubset(allowed)):
        raise StoreError("Final review did not check the required Goal and pinned evidence")
    versions = {ref["id"]: ref for ref in package.get("references", [])}
    if not required.issubset(versions):
        raise StoreError("Final review package lacks pinned evidence versions")
    for ref in [*versions.values(), *core_refs]:
        if not json_equal(store.record_ref(ref), ref):
            raise StoreError("Final review package evidence revision mismatch")
    if any(not json_equal(versions.get(ref["id"]), ref) for ref in core_refs):
        raise StoreError("Final review package does not match current Goal evidence")

    original = assessment["update"]["progress"]
    progress = reviewed_progress(original, proof["proof_draft"], review)
    if review_completes_goal(review) and (not proof_steps_complete(proof["proof_draft"])
                                         or progress.get("status") != "completed"):
        raise StoreError("Completed final review conflicts with unresolved proof or regime structure")
    if not review_completes_goal(review) and progress.get("status") == "completed":
        progress["status"] = "in_progress"
        progress["remaining"] = list(dict.fromkeys([
            *progress.get("remaining", []),
            "Final Verifier did not certify completion of the original Goal."]))
    # Validate scientific coverage before adding the final-composition bindings.
    # No Bound, scope, regime state or mathematical expression is rewritten.
    from colombo.brain.submission_validation import validate_progress
    validate_progress(store, progress, final_candidate=True)
    for regime in progress["bracket"]["regimes"]:
        if regime["status"] == "near_optimal" and not regime["comparison_review_ref"]:
            regime.update(comparison_review_ref=review_ref["id"],
                          comparison_claim_id="final-composition")
    value = {"progress": progress, "result_refs": assessment["result_refs"],
             "assessment_ref": assessment_ref, "review_ref": review_ref,
             "proof_ref": proof_ref, "previous_ref": previous_ref}
    if review_completes_goal(review):
        value["completion_resolution"] = {
            "basis": "explicit_completed_final_review", "review_ref": review_ref,
            "candidate_status": original["status"],
            "candidate_overall": original.get("overall", ""),
            "candidate_remaining": copy.deepcopy(original.get("remaining", [])),
            "candidate_items": [{"goal_id": i["goal_id"], "status": i["status"],
                                 "remaining": copy.deepcopy(i["remaining"])}
                                for i in original["items"]],
            "retained_open_questions": copy.deepcopy(proof["proof_draft"].get("open_questions", []))}
    return value
