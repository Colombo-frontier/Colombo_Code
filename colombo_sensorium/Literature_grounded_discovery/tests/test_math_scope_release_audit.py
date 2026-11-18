"""Independent release negatives for narrow mathematical edges; synthetic only."""
from copy import deepcopy

import pytest

from oracle_atlas.workflow.proof_reuse import build_proof_review_context, proof_approval_errors
from oracle_atlas.workflow.review_context import _snapshot, bound_approval_errors
from oracle_atlas.workflow.scope_revalidation import mathematical_dependencies
from test_historical_issue_scopes import historical
from test_proof_reuse import proof_context
from test_review_context import context


def chained_subject(c, leaf):
    inner = c["proof"]("inner-leaf-proof", dependencies=[leaf])
    middle = c["proof"]("middle-proof", dependencies=[inner])
    outer = c["proof"]("proof:fixture", dependencies=[middle, c["transfer"]])
    profile = deepcopy(c["profile"])
    profile["proofs"][0]["proof_ref"] = outer
    subject = c["proposal"](profile)
    return subject, outer, inner, middle


@pytest.mark.parametrize("leaf_kind", ["source", "result", "proof"])
@pytest.mark.parametrize("scope", ["standalone_proposition", "standalone_proposition_explicit_context"])
def test_transitive_formal_math_defect_remains_blocking(historical, leaf_kind, scope):
    c, art = historical, historical["ws"].artifacts
    defect = c["issue"]("deep-math-defect", subjects=["actual-math-leaf"], blocks=["bound"])
    if leaf_kind == "source":
        data = deepcopy(art.get(c["source"])["data"])
        data["metadata"]["issues"] = [defect]
        leaf = art.put("source", data, c["producer"])
    elif leaf_kind == "result":
        data = deepcopy(art.get(c["profile"]["bounds"][0]["result_ref"])["data"])
        data["issues"] = [defect]
        leaf = art.put("result", data, c["producer"])
    else:
        leaf = c["proof"]("defective-leaf", issues=[defect])
    subject, outer, inner, middle = chained_subject(c, leaf)
    narrow = mathematical_dependencies(art, {outer})
    assert {leaf, outer, inner, middle}.issubset({row["ref"] for row in narrow})
    data, jid = c["certificate"](subject)
    data["proof_approvals"][0].update(proof_ref=outer, scope=scope)
    inputs = {"subject_ref": subject, "issue_scope_contract_version": "occurrence-bound-scope"}
    proof_errors = proof_approval_errors(data, inputs, art)
    bound_errors = bound_approval_errors(data, inputs, art)
    assert any("adopted_dependency_has_blocking_issue" in error["message"] for error in proof_errors)
    assert any("bound_dependency_has_blocking_issue" in error["message"] for error in bound_errors)
    # Even an incorrectly saved prior credential cannot manufacture a scope candidate.
    prior_review = c["freeze_certificate"](data, jid)
    catalog = build_proof_review_context(art, c["ws"], subject, prior_review)
    assert catalog["proof_scope_revalidation_candidates"] == []
    assert catalog["reusable_proof_refs"] == []


def test_transitive_result_source_version_mismatch_still_fails_closed(historical):
    c, art = historical, historical["ws"].artifacts
    result = c["result"](version="wrong-pinned-source-version")
    subject, outer, _, _ = chained_subject(c, result)
    # A normal certificate helper itself rejects this malformed source graph;
    # construct an attempted current handoff from a valid baseline instead.
    data, jid = c["certificate"]()
    data["subject_ref"] = subject
    data["proof_approvals"][0]["proof_ref"] = outer
    errors = bound_approval_errors(data, {"subject_ref": subject}, art)
    assert any("source_version_mismatch" in error["message"] for error in errors)
    _, jid = c["review"](subject=subject)
    prior_review = c["freeze_certificate"](data, jid)
    catalog = build_proof_review_context(art, c["ws"], subject, prior_review)
    assert catalog["proof_scope_revalidation_candidates"] == []
    assert catalog["reusable_proof_refs"] == []
    assert "source_version_mismatch" in catalog["validation_reason"]


def test_narrow_math_graph_does_not_erase_changed_historical_p7_variant(historical):
    c, art = historical, historical["ws"].artifacts
    old, _ = c["certificate"]()
    changed = deepcopy(art.get(c["historical_candidate"])["data"])
    changed["candidate_id"] = "distinct-p7-context"
    changed["issues"][0]["message"] = "A different unresolved scientific assertion with the same issue ID."
    changed_ref = art.put("candidate", changed, c["producer"])
    profile = deepcopy(c["profile"])
    profile["quarantined_claims"] = [{"id": "different-history", "candidate_ref": changed_ref}]
    subject = c["proposal"](profile)
    data, _ = c["certificate"](subject)
    # Replace complete current occurrence scopes with the old, incomplete ones.
    for key in ("proof_issue_scopes", "bound_issue_scopes"):
        data[key] = deepcopy(old[key])
    inputs = {"subject_ref": subject, "issue_scope_contract_version": "occurrence-bound-scope"}
    errors = proof_approval_errors(data, inputs, art) + bound_approval_errors(data, inputs, art)
    assert len(errors) == 2
    assert all("occurrence_scope_missing_or_changed" in error["message"] for error in errors)
    # Workflow provenance is absent from narrow math support, but remains in issue catalog.
    assert changed_ref not in {row["ref"] for row in mathematical_dependencies(art, {c["proof_ref"]})}
    from oracle_atlas.workflow.issue_semantics import dependency_issue_catalog
    catalog = dependency_issue_catalog(art, _snapshot(art, subject), data)
    assert any(row["artifact_ref"] == changed_ref and row["issue_id"] == "p7-hidden-sibling"
               for row in catalog["issue_occurrences"])
