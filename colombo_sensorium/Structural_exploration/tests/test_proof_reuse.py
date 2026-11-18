"""Structural/authorization negative controls for standalone proposition reuse; all propositions are software fixtures without scientific approval."""
from copy import deepcopy
import json

import pytest

from oracle_atlas.core.store import digest
from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.workflow import proof_reuse as module
from oracle_atlas.workflow.proof_reuse import build_proof_review_context, proof_approval_errors
from test_review_context import context


@pytest.fixture
def proof_context(context):
    c = context
    art = c["ws"].artifacts

    def proof(pid="proof:fixture", *, dependencies=None, argument="Synthetic structural fixture only.", issues=()):
        return art.put("proof", {"proof_id": pid, "origin": "analyst_derivation", "proposition": "No real mathematical claim.",
            "premises": ["Engineering test only."], "argument": argument, "boundary_cases": "No scientific assertion.",
            "quantifiers": "Fixture.", "resource_accounting": "No model/Atlas commit.",
            "dependencies": [c["source"]] if dependencies is None else dependencies, "issues": list(issues)}, c["producer"])

    pref = proof()
    c["profile"]["proofs"].append({"id": "proof:fixture", "proof_ref": pref})
    c["prior"] = c["proposal"](c["profile"])

    def cert(ref=pref, pointers=("/common_specification",)):
        return {"proof_ref": ref, "scope": "standalone_proposition", "assumptions_complete": True,
                "context_pointers": list(pointers), "reason": "Fixture reviewer explicitly checks the complete standalone context; no mathematical certification."}

    def review(subject=None, *, approvals=None, scopes=(), issues=(), role="profile_reviewer", validated=True):
        ref, jid = c["review"](subject=subject or c["prior"], issues=issues, role=role, validated=validated)
        data = deepcopy(art.get(ref)["data"])
        data.update(proof_approvals=[cert()] if approvals is None else list(approvals), proof_issue_scopes=list(scopes),
                    proof_reuse_context_ref=None, reused_proof_refs=[])
        ref = art.put("review", data, jid)
        c["ws"].save_job(jid, "complete", {}, {"status": "complete", "artifact_refs": [ref], "summary": "fixture", "checkpoint_ref": None})
        if validated:
            c["ws"].event(jid, "validated_handoff", {"status": "complete", "refs": [ref]})
        return ref, jid

    def issue(iid="coverage-gap", subjects=("u",), blocks=("profile", "publication")):
        return {"issue_id": iid, "kind": "coverage", "scope": "Fixture envelope application only.",
                "subject_refs": list(subjects), "blocks": list(blocks), "message": "Fixture blocker, not a real theorem.",
                "evidence_refs": [c["source"]], "resolves": []}

    def scope(iid="coverage-gap", affected=(), complete=True):
        return {"issue_id": iid, "affected_proof_refs": list(affected), "scope_complete": complete,
                "reason": "Independent fixture reviewer checks standalone proof impact separately from current envelope application."}

    c.update(proof=proof, proof_ref=pref, cert=cert, proof_review=review, issue=issue, proof_scope=scope)
    c["proof_review_ref"], _ = review()
    yield c


def build(c, current=None, review=None):
    return build_proof_review_context(c["ws"].artifacts, c["ws"], current or c["proposal"](c["profile"]), review or c["proof_review_ref"])


def test_explicit_standalone_certificate_reuses_only_proof_not_bound_application(proof_context):
    c = proof_context
    out = build(c)
    assert out["reusable_proof_refs"] == [c["proof_ref"]]
    assert out["proof_candidates"][0]["dependency_count"] == 2
    assert "current_bound_applicability_and_quantifiers" in out["always_review"]
    assert "approved_bound_ids" not in out
    assert out["current_bundle_hash"]


def test_unrelated_new_regime_does_not_change_explicit_standalone_context(proof_context):
    c = proof_context
    p = deepcopy(c["profile"])
    p["regimes"].append({"id": "new-envelope-only-region"})
    p["reader_markdown"] = "A newly reviewed reader is still required."
    out = build(c, c["proposal"](p))
    assert out["reusable_proof_refs"] == [c["proof_ref"]]
    assert "regimes" in out["changed_profile_fields"]


def test_explicit_application_blocker_can_be_unaffected_standalone_scope(proof_context):
    c = proof_context
    issue = c["issue"]()
    review, _ = c["proof_review"](issues=[issue], scopes=[c["proof_scope"]()])
    out = build(c, review=review)
    assert out["reusable_proof_refs"] == [c["proof_ref"]]


@pytest.mark.parametrize("direct", ["ref", "id"])
def test_direct_proof_blocker_cannot_be_overruled_by_unaffected_scope(proof_context, direct):
    c = proof_context
    target = c["proof_ref"] if direct == "ref" else "proof:fixture"
    review, _ = c["proof_review"](issues=[c["issue"](subjects=[target])], scopes=[c["proof_scope"]()])
    out = build(c, review=review)
    assert out["reusable_proof_refs"] == []
    assert "direct_proof_blocker" in out["validation_reason"]


@pytest.mark.parametrize("scopes,expected", [("missing", "proof_issue_scope_missing"), ("incomplete", "proof_issue_scope_incomplete"), ("affected", "scoped_proof_blocker")])
def test_missing_unknown_or_affected_issue_scope_fails_closed(proof_context, scopes, expected):
    c = proof_context
    rows = [] if scopes == "missing" else [c["proof_scope"](complete=scopes != "incomplete", affected=[c["proof_ref"]] if scopes == "affected" else [])]
    review, _ = c["proof_review"](issues=[c["issue"]()], scopes=rows)
    out = build(c, review=review)
    assert not out["reusable_proof_refs"]
    assert expected in out["validation_reason"]


def test_scoped_other_proof_blocker_does_not_poison_approved_proof(proof_context):
    c = proof_context
    second = c["proof"]("proof:second", argument="A distinct synthetic statement.")
    p = deepcopy(c["profile"])
    p["proofs"].append({"id": "proof:second", "proof_ref": second})
    old = c["proposal"](p)
    review, _ = c["proof_review"](subject=old, issues=[c["issue"](subjects=[second])], scopes=[c["proof_scope"](affected=[second])])
    out = build(c, c["proposal"](p), review)
    assert out["reusable_proof_refs"] == [c["proof_ref"]]


def test_research_issues_must_be_explicitly_scoped_by_reviewer(proof_context):
    c = proof_context
    old = c["proposal"](c["profile"], research_issues=[c["issue"]()])
    review, _ = c["proof_review"](subject=old)
    out = build(c, review=review)
    assert not out["reusable_proof_refs"] and "proof_issue_scope_missing" in out["validation_reason"]


@pytest.mark.parametrize("field", ["native", "declared_context"])
def test_native_contract_or_explicit_mathematical_context_change_invalidates(proof_context, field):
    c = proof_context
    pointers = ["/common_specification", "/parameters"]
    review, _ = c["proof_review"](approvals=[c["cert"](pointers=pointers)])
    p = deepcopy(c["profile"])
    if field == "native":
        p["common_specification"]["oracle"]["summary"] = "A changed native contract."
    else:
        p["parameters"].append({"id": "changed_assumption"})
    out = build(c, c["proposal"](p), review)
    assert not out["reusable_proof_refs"]
    assert out["invalidated_proofs"][0]["reason"] == "proof_context_or_dependency_changed"


@pytest.mark.parametrize("pointers", [[], ["/parameters"], ["/common_specification", "/missing"], ["/common_specification", "/common_specification"], ["/common_specification", "/bad~2escape"]])
def test_missing_ambiguous_or_bad_context_pointer_denies_certificate(proof_context, pointers):
    c = proof_context
    if not pointers or len(pointers) != len(set(pointers)):
        with pytest.raises(ProtocolError):
            c["proof_review"](approvals=[c["cert"](pointers=pointers)])
        return
    review, _ = c["proof_review"](approvals=[c["cert"](pointers=pointers)])
    assert not build(c, review=review)["reusable_proof_refs"]


def test_changed_proof_or_source_is_not_same_certified_proposition(proof_context):
    c = proof_context
    second = c["proof"](argument="Changed full proof body.")
    p = deepcopy(c["profile"])
    p["proofs"] = [row for row in p["proofs"] if row.get("id") != "proof:fixture"] + [{"id": "proof:fixture", "proof_ref": second}]
    out = build(c, c["proposal"](p))
    assert not out["reusable_proof_refs"]
    assert out["invalidated_proofs"][0]["reason"] == "no_explicit_prior_proof_approval"


def test_bound_approval_without_explicit_proof_certificate_never_implies_reuse(proof_context):
    c = proof_context
    review, _ = c["review"](subject=c["prior"])
    out = build(c, review=review)
    assert out["reuse_status"] == "no_explicit_prior_proof_approval"
    assert not out["reusable_proof_refs"]


@pytest.mark.parametrize("role,validated", [("profile_researcher", True), ("profile_reviewer", False)])
def test_producer_forgery_or_unvalidated_review_cannot_certify_proof(proof_context, role, validated):
    c = proof_context
    ref, _ = c["proof_review"](role=role, validated=validated)
    assert not build(c, review=ref)["reusable_proof_refs"]


def test_reviewer_cannot_reuse_its_own_proof(proof_context):
    c = proof_context
    ref, jid = c["proof_review"]()
    with c["ws"].transaction() as db:
        db.execute("INSERT INTO ownership VALUES(?,?)", (c["proof_ref"], jid))
    out = build(c, review=ref)
    assert not out["reusable_proof_refs"]
    assert out["invalidated_proofs"][0]["reason"] == "proof_reviewer_not_independent"


def test_new_scientific_issue_requires_new_independent_scope_review(proof_context):
    c = proof_context
    current = c["proposal"](c["profile"], research_issues=[c["issue"]("new-counterexample", subjects=[c["proof_ref"]])])
    out = build(c, current)
    assert not out["reusable_proof_refs"]
    assert out["invalidated_proofs"][0]["reason"] == "new_scientific_issue_requires_review"


def test_proof_dependency_own_blocker_is_not_erased_by_profile_scope(proof_context):
    c = proof_context
    proof = c["proof"](issues=[c["issue"](subjects=["proof:fixture"], blocks=["bound"])])
    p = deepcopy(c["profile"]);p["proofs"] = [row for row in p["proofs"] if row.get("id") != "proof:fixture"] + [{"id": "proof:fixture", "proof_ref": proof}]
    old = c["proposal"](p)
    review, _ = c["proof_review"](subject=old, approvals=[c["cert"](proof)])
    out = build(c, c["proposal"](p), review)
    assert not out["reusable_proof_refs"]
    assert "dependency_has_blocking_issue" in out["validation_reason"]


def test_source_version_mismatch_and_missing_dependency_fail_closed(proof_context):
    c = proof_context
    result = c["result"](version="incorrect-fixed-version")
    proof = c["proof"](dependencies=[result])
    p = deepcopy(c["profile"]);p["proofs"] = [row for row in p["proofs"] if row.get("id") != "proof:fixture"] + [{"id": "proof:fixture", "proof_ref": proof}]
    old = c["proposal"](p)
    review, _ = c["proof_review"](subject=old, approvals=[c["cert"](proof)])
    out = build(c, c["proposal"](p), review)
    assert not out["reusable_proof_refs"] and "source_version_mismatch" in out["validation_reason"]
    with c["ws"].transaction() as db:
        db.execute("DELETE FROM artifacts WHERE ref=?", (c["source"],))
    assert not build(c)["reusable_proof_refs"]


def test_dependency_cycle_or_budget_limit_never_supplies_candidate(proof_context, monkeypatch):
    c = proof_context
    with c["ws"].transaction() as db:
        db.execute("UPDATE artifacts SET deps=? WHERE ref=?", (json.dumps([c["source"]]), c["source"]))
    assert not build(c)["reusable_proof_refs"]
    with c["ws"].transaction() as db:
        db.execute("UPDATE artifacts SET deps='[]' WHERE ref=?", (c["source"],))
    monkeypatch.setattr(module, "MAX_CONTEXT_BYTES", 1)
    assert not build(c)["reusable_proof_refs"]


def test_valid_current_reuse_is_explicit_and_bound_to_controller_context(proof_context):
    c = proof_context
    current = c["proposal"](c["profile"])
    context = build(c, current)
    context_ref = c["ws"].artifacts.put("external_result", context, "controller")
    review_ref, _ = c["proof_review"](subject=current)
    review = c["ws"].artifacts.get(review_ref)["data"]
    review.update(proof_reuse_context_ref=context_ref, reused_proof_refs=[c["proof_ref"]])
    inputs = {"subject_ref": current, "proof_context_ref": context_ref}
    assert proof_approval_errors(review, inputs, c["ws"].artifacts) == []
    bad = deepcopy(review);bad["proof_reuse_context_ref"] = c["source"]
    assert any(e["code"] == "proof_reuse_context" for e in proof_approval_errors(bad, inputs, c["ws"].artifacts))
    bad = deepcopy(review);bad["proof_approvals"] = []
    assert any(e["code"] == "proof_reuse_adoption" for e in proof_approval_errors(bad, inputs, c["ws"].artifacts))


def test_reuse_outside_verified_context_or_wrong_proposal_is_rejected(proof_context):
    c = proof_context
    current = c["proposal"](c["profile"])
    data = build(c, current);data["reusable_proof_refs"] = []
    context_ref = c["ws"].artifacts.put("external_result", data, "controller")
    ref, _ = c["proof_review"](subject=current)
    review = c["ws"].artifacts.get(ref)["data"]
    review.update(proof_reuse_context_ref=context_ref, reused_proof_refs=[c["proof_ref"]])
    inputs = {"subject_ref": current, "proof_context_ref": context_ref}
    errors = proof_approval_errors(review, inputs, c["ws"].artifacts)
    assert any("controller" in row["message"] for row in errors)
    bad = deepcopy(review);bad["subject_ref"] = c["source"]
    assert any(e["code"] == "proof_review_subject" for e in proof_approval_errors(bad, inputs, c["ws"].artifacts))


def test_current_contract_required_only_when_controller_enables_it(proof_context):
    c = proof_context
    ref, _ = c["review"](subject=c["prior"])
    legacy = c["ws"].artifacts.get(ref)["data"]
    assert proof_approval_errors(legacy, {"subject_ref": c["prior"]}, c["ws"].artifacts) == []
    errors = proof_approval_errors(legacy, {"subject_ref": c["prior"], "proof_context_ref": c["source"]}, c["ws"].artifacts)
    assert any(e["code"] == "proof_contract_missing" for e in errors)


def test_forged_context_cannot_invent_reuse_without_prior_certificate(proof_context):
    c = proof_context
    current = c["proposal"](c["profile"])
    data = build_proof_review_context(c["ws"].artifacts, c["ws"], current)
    data["reusable_proof_refs"] = [c["proof_ref"]]
    context_ref = c["ws"].artifacts.put("external_result", data, "controller")
    ref, _ = c["proof_review"](subject=current)
    review = c["ws"].artifacts.get(ref)["data"]
    review.update(proof_reuse_context_ref=context_ref, reused_proof_refs=[c["proof_ref"]])
    errors = proof_approval_errors(review, {"subject_ref": current, "proof_context_ref": context_ref}, c["ws"].artifacts)
    assert any("no_independent_prior" in row["message"] for row in errors)


def test_profile_or_research_variants_of_same_issue_are_all_scoped(proof_context):
    c = proof_context
    original = c["issue"]()
    current = c["proposal"](c["profile"], research_issues=[original])
    amended = {**original, "message": "Reviewer adds a different explanatory note for the same stable issue."}
    review, _ = c["proof_review"](subject=current, issues=[amended], scopes=[c["proof_scope"]()])
    out = build(c, current, review)
    assert out["reusable_proof_refs"] == [c["proof_ref"]]


def test_same_named_proof_in_different_setting_never_reuses(proof_context):
    c = proof_context
    p = deepcopy(c["profile"])
    p["setting_id"] = "OTHER_SETTING"
    for comparison in p["comparisons"]:
        comparison["comparison_key"]["setting_id"] = p["setting_id"]
    # Fixture identity/research binding is setting-agnostic, as in a new-profile case.
    out = build(c, c["proposal"](p))
    assert not out["reusable_proof_refs"]
    assert "different_setting_id" in out["validation_reason"]


def test_current_reuse_cannot_silently_change_certified_context_declaration(proof_context):
    c = proof_context
    old_review, _ = c["proof_review"](approvals=[c["cert"](pointers=["/common_specification", "/parameters"])])
    current = c["proposal"](c["profile"])
    data = build(c, current, old_review)
    context_ref = c["ws"].artifacts.put("external_result", data, "controller")
    ref, _ = c["proof_review"](subject=current)
    review = c["ws"].artifacts.get(ref)["data"]
    review.update(proof_reuse_context_ref=context_ref, reused_proof_refs=[c["proof_ref"]])
    errors = proof_approval_errors(review, {"subject_ref": current, "proof_context_ref": context_ref}, c["ws"].artifacts)
    assert any("declaration_changed" in row["message"] for row in errors)


def test_current_duplicate_proof_id_is_not_a_verified_reuse_candidate(proof_context):
    c = proof_context
    another = c["proof"](argument="Different content sharing the same local proof ID.")
    p = deepcopy(c["profile"])
    p["proofs"].append({"id": "different-local-record", "proof_ref": another})
    out = build(c, c["proposal"](p))
    assert not out["reusable_proof_refs"]
    assert all(row["reason"] == "proof_id_ambiguous" for row in out["invalidated_proofs"])


def test_corrupted_fixed_proof_content_never_supplies_candidate(proof_context):
    c = proof_context
    ref = c["proof_ref"];path = c["ws"].root / "objects" / ref[7:9] / (ref[7:] + ".json")
    obj = json.loads(path.read_text());obj["data"]["argument"] = "Illicit mutation of the content-addressed proof."
    path.write_text(json.dumps(obj))
    out = build(c, c["prior"])
    assert not out["reusable_proof_refs"]
    assert out["reuse_status"] == "current_snapshot_unavailable"


@pytest.mark.parametrize("container", ["proofs", "evidence", "quarantined_claims"])
def test_nested_new_counterexample_in_scientific_container_invalidates(proof_context, container):
    c = proof_context
    p = deepcopy(c["profile"])
    nested = {"id": "nested-counterexample-record", "issues": [c["issue"]("nested-counterexample", subjects=[c["proof_ref"]])]}
    p.setdefault(container, []).append(nested)
    out = build(c, c["proposal"](p))
    assert not out["reusable_proof_refs"]
    assert out["invalidated_proofs"][0]["reason"] == "new_scientific_issue_requires_review"


def test_nested_direct_variant_cannot_be_hidden_by_top_level_unaffected_variant(proof_context):
    c = proof_context
    p = deepcopy(c["profile"])
    p["quarantined_claims"] = [{"claim_id": "nested", "issues": [c["issue"](subjects=[c["proof_ref"]])]}]
    prior = c["proposal"](p)
    review, _ = c["proof_review"](subject=prior, issues=[c["issue"](subjects=["u"])], scopes=[c["proof_scope"]()])
    out = build(c, c["proposal"](p), review)
    assert not out["reusable_proof_refs"]
    assert "direct_proof_blocker" in out["validation_reason"]


def test_nested_unrelated_issue_requires_and_accepts_explicit_independent_scope(proof_context):
    c = proof_context
    p = deepcopy(c["profile"])
    p["quarantined_claims"] = [{"claim_id": "source-literal", "issues": [c["issue"](subjects=["quarantined-source-literal"])]}]
    prior = c["proposal"](p)
    review, _ = c["proof_review"](subject=prior, scopes=[c["proof_scope"]()])
    out = build(c, c["proposal"](p), review)
    assert out["reusable_proof_refs"] == [c["proof_ref"]]
    missing, _ = c["proof_review"](subject=prior)
    assert not build(c, c["proposal"](p), missing)["reusable_proof_refs"]


@pytest.mark.parametrize("name,value,reason", [("MAX_ISSUE_SCAN_DEPTH", 1, "issue_scan_depth_limit"),
    ("MAX_ISSUE_SCAN_NODES", 5, "issue_scan_node_limit"), ("MAX_ISSUE_SCAN_BYTES", 30, "issue_scan_byte_limit")])
def test_bounded_structural_issue_scan_never_infers_no_issues_after_limit(proof_context, monkeypatch, name, value, reason):
    c = proof_context
    monkeypatch.setattr(module, name, value)
    out = build(c)
    assert not out["reusable_proof_refs"]
    assert reason in out["validation_reason"]


def test_issue_json_inside_reader_string_is_not_parsed_as_structured_issue(proof_context):
    c = proof_context
    p = deepcopy(c["profile"])
    p["reader_markdown"] = json.dumps({"issues": [c["issue"]("string-only", subjects=[c["proof_ref"]])]})
    out = build(c, c["proposal"](p))
    assert out["reusable_proof_refs"] == [c["proof_ref"]]


def test_unknown_nested_issue_shape_disables_certificates_but_allows_explicit_decline(proof_context):
    c = proof_context
    p = deepcopy(c["profile"])
    p["quarantined_claims"] = [{"claim_id": "legacy-free-object", "issues": {"legacy": "unknown issue format"}}]
    current = c["proposal"](p)
    out = build(c, current)
    assert not out["reusable_proof_refs"]
    assert "issue_list_unknown" in out["validation_reason"]
    context_ref = c["ws"].artifacts.put("external_result", out, "controller")
    ref, _ = c["proof_review"](subject=current, approvals=[])
    review = c["ws"].artifacts.get(ref)["data"]
    inputs = {"subject_ref": current, "proof_context_ref": context_ref}
    assert proof_approval_errors(review, inputs, c["ws"].artifacts) == []
    attempted = deepcopy(review);attempted["proof_approvals"] = [c["cert"]()]
    assert any(error["code"] == "proof_approval_contract" for error in proof_approval_errors(attempted, inputs, c["ws"].artifacts))
    attempted = deepcopy(review);attempted["reused_proof_refs"] = [c["proof_ref"]]
    assert proof_approval_errors(attempted, inputs, c["ws"].artifacts)


def test_explicit_decline_does_not_bypass_subject_or_context_binding(proof_context):
    c = proof_context
    ref, _ = c["proof_review"](approvals=[])
    review = c["ws"].artifacts.get(ref)["data"]
    inputs = {"subject_ref": c["prior"], "proof_context_ref": c["source"]}
    bad = deepcopy(review);bad["subject_ref"] = c["source"]
    assert any(error["code"] == "proof_review_subject" for error in proof_approval_errors(bad, inputs, c["ws"].artifacts))
    bad = deepcopy(review);bad["proof_reuse_context_ref"] = c["proof_ref"]
    assert any(error["code"] == "proof_reuse_context" for error in proof_approval_errors(bad, inputs, c["ws"].artifacts))
