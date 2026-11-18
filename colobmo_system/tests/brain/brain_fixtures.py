"""Current-protocol data fixtures; all Claims and review outcomes are synthetic."""
import copy
from colombo.brain.proof_draft import initial_proof, write_proof

SETTING = {"specification": {"regimes": [{"id": "R1", "scope": "All objects in the original goal"}]},
    "provenance": [], "unknowns": [], "near_optimal_policy": "Allow polylog gaps in varying dimensionless parameters."}


def freeze_setting(store):
    ref = store.get_meta("setting_ref")
    if not ref:
        ref = store.write_record("setting", copy.deepcopy(SETTING), request_id="fixture-setting")
        store.set_meta(setting_ref=ref)
    return ref


def confirm_result(store, result_ref, *, completion="completed", claims=None):
    reviews = store.get_meta("result_reviews", {})
    rid = result_ref["id"] if isinstance(result_ref, dict) else result_ref
    if rid in reviews:
        return reviews[rid]
    result = store.read_record(rid)
    if claims is None:
        claims = [{"id": "fixture-claim", "statement": "The target holds", "assumptions": [],
            "scope": "All objects in the original goal", "kind": "lemma", "expression": "",
            "evidence_paths": [a["path"] for a in result.get("artifacts", [])]}]
    report = {"verdict": "pass", "summary": "Synthetic independent Result review", "findings": [],
        "checked_refs": [rid], "review_kind": "result", "result_ref": rid,
        "confirmed_claims": copy.deepcopy(claims), "completion_status": completion, "repair_kind": "none"}
    ref = store.write_record("review", report)
    reviews[rid] = ref
    store.set_meta(result_reviews=reviews)
    return ref


def progress(result_refs=()):
    return {"overall": "Synthetic progress description", "status": "in_progress",
        "items": [{"goal_id": "G0", "description": "The fixed goal", "status": "partial",
                   "result_refs": list(result_refs), "remaining": ["Final composition"]}],
        "bracket": {"bounds": [], "regimes": []}, "remaining": ["Final composition"]}


def write_review_package(store, payload, request_id=None):
    """Give reader tests a current, explicitly identified Proof review package."""
    proof = store.get_meta("proof_ref")
    if not proof:
        proof = write_proof(store, initial_proof(store), "fixture-package-proof")
        store.set_meta(proof_ref=proof)
    payload.setdefault("review_kind", "proof")
    payload.setdefault("result_ref", None)
    payload.setdefault("proof_ref", proof)
    return store.write_record("review_package", payload, request_id)
