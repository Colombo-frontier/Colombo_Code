"""A rejected historical theorem is retained, without becoming a new premise."""
from copy import deepcopy

import pytest

from oracle_atlas.workflow.proof_reuse import _contract, adopted_scientific_dependencies
from oracle_atlas.workflow.review_context import _snapshot, _bound_contract, _Unavailable
from test_historical_issue_scopes import historical
from test_proof_reuse import proof_context
from test_review_context import context


@pytest.mark.parametrize("direct", [False, True])
def test_audit_review_descendants_are_not_mathematical_support(historical, direct):
    c = historical; a = c["ws"].artifacts
    defect = c["issue"]("old-rejected-proof", subjects=["proof:old-rejected"], blocks=["bound"])
    rejected = c["proof"]("proof:old-rejected", issues=[defect])
    audit_issue = c["issue"]("old-rejected-proof", subjects=[rejected], blocks=["bound"])
    audit = a.put("review", {"subject_ref": rejected, "review_type": "profile", "verdict": "revise",
        "assessments": [], "issues": [audit_issue], "approved_bound_ids": [], "summary": "Historical rejected proof, software fixture only."}, c["producer"])
    fixed = c["proof"](argument="Independent replacement proof; the audit is not a premise.",
                       dependencies=[c["source"], rejected if direct else audit])
    p = deepcopy(c["profile"]); p["proofs"][0]["proof_ref"] = fixed
    subject = c["proposal"](p); review, _ = c["certificate"](subject)
    review["proof_approvals"][0]["proof_ref"] = fixed
    snap = _snapshot(a, subject)
    actual = {row["ref"] for row in adopted_scientific_dependencies(a, snap, ["u"])}
    assert (rejected in actual) is direct
    if direct:
        for fn in (_contract, _bound_contract):
            with pytest.raises(_Unavailable, match="dependency_has_blocking_issue"):
                fn(a, snap, review)
    else:
        _, _, fingerprints, _, _ = _contract(a, snap, review)
        assert rejected in fingerprints[fixed]["dependency_refs"]  # Retain raw evidence closure.
        assert audit in fingerprints[fixed]["dependency_refs"]
        _, _, _, bound_fingerprints = _bound_contract(a, snap, review)
        assert rejected in bound_fingerprints["u"]["dependency_refs"]
        assert any(row["issue_id"] == "old-rejected-proof" for row in review["proof_issue_scopes"])
