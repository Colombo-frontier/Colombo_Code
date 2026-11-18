"""No scientific claims: real handoff/lineage and explicit re-review boundaries."""
from copy import deepcopy

import pytest

from oracle_atlas.workflow.issue_semantics import dependency_issue_catalog
from oracle_atlas.workflow.review_context import _snapshot, build_review_context
from oracle_atlas.workflow.proof_reuse import build_proof_review_context, proof_approval_errors
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.workflow.engine import Engine
from test_draft_clone import host
from test_historical_issue_scopes import historical
from test_proof_reuse import proof_context
from test_review_context import context


def scopes(c, review):
    catalog = dependency_issue_catalog(c["ws"].artifacts, _snapshot(c["ws"].artifacts, review["subject_ref"]), review)
    groups = {}
    for row in catalog["issue_occurrences"]:
        groups.setdefault(row["issue_id"], []).append(row["occurrence_id"])
    for field, target in (("proof_issue_scopes", "affected_proof_refs"), ("bound_issue_scopes", "affected_bound_ids")):
        review[field] = [{"issue_id": iid, target: [], "occurrence_ids": sorted(ids), "scope_complete": True,
                          "reason": "Synthetic fixture independent scope; not mathematical approval."}
                         for iid, ids in sorted(groups.items())]


def test_verified_review_and_research_copies_do_not_become_new_issues(historical):
    c = historical; a = c["ws"].artifacts
    old = c["prior"]; profile_ref = a.get(old)["data"]["profile_ref"]
    issue = c["issue"]("delivery-note", subjects=[profile_ref], blocks=["bound"])
    old = c["proposal"](c["profile"], research_issues=[issue])
    data, jid = c["certificate"](old); data["issues"] = [issue]; scopes(c, data)
    prior_review = c["freeze_certificate"](data, jid)
    p = deepcopy(c["profile"]); p["reader_markdown"] = "Changed presentation."
    p["provenance"] = {"previous_review_ref": prior_review}
    provisional = c["proposal"](p)
    copy = deepcopy(issue); copy["subject_refs"] = [a.get(provisional)["data"]["profile_ref"]]
    current = c["proposal"](p, research_issues=[copy])
    for out, key in ((build_proof_review_context(a, c["ws"], current, prior_review), "reusable_proof_refs"),
                     (build_review_context(a, c["ws"], current, prior_review), "reusable_bound_ids")):
        assert out[key]
        assert any(row["artifact_ref"] == prior_review for row in out["issue_occurrences"])
        before = next(row for row in out["prior_issue_evidence"] if row["issue_id"] == "delivery-note")
        after = next(row for row in out["current_issue_evidence"] if row["issue_id"] == "delivery-note")
        assert set(after["occurrence_signatures"]).issubset(before["occurrence_signatures"])
        assert set(after["material_signatures"]) != set(before["material_signatures"])


def setup_revalidation(c, mode="parameter"):
    a = c["ws"].artifacts
    old, jid = c["certificate"](); prior_review = c["freeze_certificate"](old, jid)
    p = deepcopy(c["profile"])
    if mode == "parameter":
        p["parameters"].append({"id": "new_parameter", "summary": "Changed assumption must be reassessed."})
    else:
        extra = deepcopy(a.get(c["historical_candidate"])["data"])
        extra["candidate_id"] = "unseen-p7-origin"
        p["quarantined_claims"] = [{"id": "unseen-context", "candidate_ref": a.put("candidate", extra, c["producer"])}]
    current = c["proposal"](p)
    catalog = build_proof_review_context(a, c["ws"], current, prior_review)
    assert not catalog["reusable_proof_refs"]
    candidate = catalog["proof_scope_revalidation_candidates"][0]
    context_ref = a.put("external_result", catalog, "controller")
    review, _ = c["certificate"](current)
    review["proof_approvals"][0]["scope"] = "standalone_proposition_explicit_context"
    review["proof_reuse_context_ref"] = context_ref
    review["proof_scope_revalidations"] = [{"proof_ref": c["proof_ref"], "candidate_id": candidate["candidate_id"],
        "changes_reviewed": True, "reason": "Fixture reviewer reassesses changed assumptions/new issue origins and current application; no real mathematical judgment."}]
    inputs = {"subject_ref": current, "proof_context_ref": context_ref, "issue_scope_contract_version": "occurrence-bound-scope"}
    return review, inputs, catalog


@pytest.mark.parametrize("mode", ["parameter", "new_issue"])
def test_context_only_revalidation_requires_new_independent_scope(historical, mode):
    c = historical; review, inputs, catalog = setup_revalidation(c, mode)
    candidate = catalog["proof_scope_revalidation_candidates"][0]
    assert bool(candidate["context_changes"]["changes"]) == (mode == "parameter")
    assert bool(candidate["new_issue_occurrence_ids"]) == (mode == "new_issue")
    assert proof_approval_errors(review, inputs, c["ws"].artifacts) == []
    assert review["reused_proof_refs"] == []


@pytest.mark.parametrize("mutation", ["unsigned", "not_reviewed", "wrong_candidate", "reuse", "missing_issue", "affected_issue", "foreign_context"])
def test_scope_revalidation_cannot_bypass_current_contract(historical, mutation):
    c = historical; review, inputs, _ = setup_revalidation(c, "new_issue")
    if mutation == "unsigned": review["proof_approvals"] = []
    elif mutation == "not_reviewed": review["proof_scope_revalidations"][0]["changes_reviewed"] = False
    elif mutation == "wrong_candidate": review["proof_scope_revalidations"][0]["candidate_id"] = "scope-revalidation:" + "0" * 64
    elif mutation == "reuse": review["reused_proof_refs"] = [c["proof_ref"]]
    elif mutation == "missing_issue": review["proof_issue_scopes"].pop()
    elif mutation == "affected_issue": review["proof_issue_scopes"][0]["affected_proof_refs"] = [c["proof_ref"]]
    else: review["proof_reuse_context_ref"] = c["source"]
    assert proof_approval_errors(review, inputs, c["ws"].artifacts)


def test_explicit_context_does_not_silently_inherit_legacy_approval(historical):
    c = historical; a = c["ws"].artifacts
    old, jid = c["certificate"](); prior_review = c["freeze_certificate"](old, jid)
    catalog = build_proof_review_context(a, c["ws"], c["prior"], prior_review)
    ref = a.put("external_result", catalog, "controller")
    review, _ = c["certificate"](); review["proof_approvals"][0]["scope"] = "standalone_proposition_explicit_context"
    review.update(proof_reuse_context_ref=ref, reused_proof_refs=[c["proof_ref"]])
    found = proof_approval_errors(review, {"subject_ref": c["prior"], "proof_context_ref": ref}, a)
    assert any("declaration_changed" in row["message"] for row in found)


def test_changed_proof_or_source_has_no_context_only_candidate(historical):
    c = historical; a = c["ws"].artifacts
    old, jid = c["certificate"](); prior_review = c["freeze_certificate"](old, jid)
    proof_ref = c["proof"](argument="A changed mathematical proof must receive full review.")
    p = deepcopy(c["profile"]); p["proofs"][0]["proof_ref"] = proof_ref
    out = build_proof_review_context(a, c["ws"], c["proposal"](p), prior_review)
    assert not out["proof_scope_revalidation_candidates"]


def test_changed_formal_source_in_declared_context_is_not_only_a_parameter_delta(historical):
    c = historical; a = c["ws"].artifacts
    old, jid = c["certificate"](); prior_review = c["freeze_certificate"](old, jid)
    source = deepcopy(a.get(c["source"])["data"]); source["version"] = "different-scientific-source"
    p = deepcopy(c["profile"]); p["parameters"].append({"id": "changed-source-assumption", "source_ref": a.put("source", source, c["producer"])})
    out = build_proof_review_context(a, c["ws"], c["proposal"](p), prior_review)
    assert not out["proof_scope_revalidation_candidates"]


@pytest.mark.parametrize("mode", ["valid", "wrong_candidate", "empty_declarations"])
def test_actual_host_and_engine_validate_scope_revalidation(historical, mode):
    c = historical; a = c["ws"].artifacts
    data, inputs, _ = setup_revalidation(c, "new_issue")
    subject = data["subject_ref"]
    inputs["review_context_ref"] = a.put("external_result", build_review_context(a, c["ws"], subject), "controller")
    # A revise verdict still certifies individual propositions; no publication
    # approval or mathematical assessment is implied by this software fixture.
    data["verdict"] = "revise"
    valid = mode == "valid"
    expected = "scope_revalidation_not_current_candidate"
    if mode == "wrong_candidate":
        data["proof_scope_revalidations"][0]["candidate_id"] = "scope-revalidation:" + "0" * 64
    elif mode == "empty_declarations":
        data["proof_execution_checks"] = [{"proof_ref": c["proof_ref"], "execution_check": data["proof_approvals"][0]["execution_check"]}]
        for key in ("proof_approvals", "bound_approvals", "proof_issue_scopes", "bound_issue_scopes", "proof_scope_revalidations"):
            data[key] = []
        expected = "proof_issue_scope_missing"
    config = {"atlas": str(c["atlas"].root), "workspace": str(c["ws"].root), "budgets": dict(DEFAULTS), "model": {}}
    h = host((c["atlas"], c["ws"], config), inputs, "profile_reviewer")
    _, errors, _ = h._validate_artifact("review", data)
    assert bool(errors) is not valid
    if errors:
        assert any(expected in row["message"] for row in errors)
    ref = a.put("review", data, h.job["id"])
    engine = Engine.__new__(Engine)
    engine.ws, engine.atlas, engine.artifacts, engine.config = c["ws"], c["atlas"], a, config
    if valid:
        engine._validate_stage(c["ws"].job(h.job["id"]), {"status": "complete", "artifact_refs": [ref]})
    else:
        with pytest.raises(ProtocolError, match=expected):
            engine._validate_stage(c["ws"].job(h.job["id"]), {"status": "complete", "artifact_refs": [ref]})


def test_full_review_may_decline_credentials_but_must_register_new_issue_scope(historical):
    c = historical; data, inputs, _ = setup_revalidation(c, "new_issue")
    data["proof_execution_checks"] = [{"proof_ref": c["proof_ref"], "execution_check": data["proof_approvals"][0]["execution_check"]}]
    data.update(proof_approvals=[], bound_approvals=[], bound_issue_scopes=[], proof_scope_revalidations=[])
    # Complete current occurrence scope remains, without reusable credentials.
    assert proof_approval_errors(data, inputs, c["ws"].artifacts) == []
    data["proof_issue_scopes"][0]["affected_proof_refs"] = [c["proof_ref"]]
    assert any("scoped_proof_blocker" in row["message"] for row in proof_approval_errors(data, inputs, c["ws"].artifacts))
    data["approved_bound_ids"] = []
    assert proof_approval_errors(data, inputs, c["ws"].artifacts) == []


def test_new_issue_semantics_are_not_removed_by_delivery_lineage(historical):
    c = historical; a = c["ws"].artifacts
    old, jid = c["certificate"](); prior_review = c["freeze_certificate"](old, jid)
    issue = c["issue"]("new-scientific-assertion", subjects=[c["proof_ref"]], blocks=["bound"])
    current = c["proposal"](c["profile"], research_issues=[issue])
    out = build_proof_review_context(a, c["ws"], current, prior_review)
    assert out["reusable_proof_refs"] == []
    new, _ = c["certificate"](current)
    assert any("direct_proof_blocker" in row["message"] for row in proof_approval_errors(new, {"subject_ref": current}, a))
