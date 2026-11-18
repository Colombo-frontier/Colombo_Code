"""Independent scoped credentials: real COLT issue wording, synthetic authorization.

No historical reviewer approval is rewritten and no scientific conclusion is
certified by these software tests. Original source hashes remain in the fixture.
"""
from copy import deepcopy
import json
from pathlib import Path

import pytest

from oracle_atlas.workflow.review_context import build_review_context, bound_approval_errors
from oracle_atlas.workflow.proof_reuse import build_proof_review_context
from test_review_context import context
from test_proof_reuse import proof_context


def certify(c, subject, issues=(), *, pointers=("/common_specification",), version=True,
            affected=(), complete=True, role="profile_reviewer", validated=True):
    ref, jid = c["review"](subject=subject, issues=issues, role=role, validated=validated)
    data = deepcopy(c["ws"].artifacts.get(ref)["data"])
    data.update(bound_approvals=[{"bound_id": "u", "scope": "bound_applicability", "assumptions_complete": True,
                    "context_pointers": list(pointers), "reason": "Synthetic independent scope check; no scientific certification."}],
                bound_issue_scopes=[{"issue_id": row["issue_id"], "affected_bound_ids": list(affected),
                    "scope_complete": complete, "reason": "The retained issue concerns positive-scale geometry/selection; this fixture checks zero-call scope."}
                    for row in issues])
    if version:
        data["issue_scope_version"] = "snapshot-bound-scope"
    ref = c["ws"].artifacts.put("review", data, jid)
    c["ws"].save_job(jid, "complete", {}, {"status": "complete", "artifact_refs": [ref], "summary": "fixture", "checkpoint_ref": None})
    if validated:
        c["ws"].event(jid, "validated_handoff", {"status": "complete", "refs": [ref]})
    return ref


@pytest.fixture
def zero(context):
    c = context
    source = json.loads((Path(__file__).parent / "fixtures/colt_zero_scope_regression.json").read_text())
    p = deepcopy(c["profile"])
    art = c["ws"].artifacts
    initial = art.get(c["prior"])["data"]
    candidate = deepcopy(art.get(initial["candidate_ref"])["data"])
    candidate["issues"] = [{**row, "subject_refs": [c["source"]], "evidence_refs": [c["source"]]}
                           for row in source["candidate_issues"]]
    candidate_ref = art.put("candidate", candidate, c["producer"])
    identity = deepcopy(art.get(initial["identity_ref"])["data"]); identity["candidate_ref"] = candidate_ref
    identity_ref = art.put("identity", identity, c["producer"])
    # The real zero proof retains the candidate in its immutable source
    # closure. Reproduce that dependency, including the original issue variants.
    result = deepcopy(art.get(p["bounds"][0]["result_ref"])["data"])
    result["conditions"] = ["Pinned source-contract fixture: " + candidate_ref]
    result_ref = art.put("result", result, c["producer"])
    p["bounds"][0]["result_ref"] = result_ref; p["evidence"][0]["result_ref"] = result_ref
    original_proposal = c["proposal"]

    def proposal(profile, **kwargs):
        ref = original_proposal(profile, **kwargs)
        data = deepcopy(art.get(ref)["data"])
        research = deepcopy(art.get(data["research_ref"])["data"])
        research.update(candidate_ref=candidate_ref, identity_ref=identity_ref)
        data.update(candidate_ref=candidate_ref, identity_ref=identity_ref,
                    research_ref=art.put("research", research, c["producer"]))
        return art.put("proposal", data, "controller")

    c["proposal"] = proposal
    # Keep fixture identifiers/specification; replay the real zero-scale claim
    # and the exact three long-lived issue statements without inferring scope.
    p["bounds"][0].update(statement=source["bound"]["statement"], formula_latex=source["bound"]["formula_latex"])
    old = c["proposal"](p)

    def issues(subject, *, raw_ref=None):
        proposal = c["ws"].artifacts.get(subject)["data"]
        research = c["ws"].artifacts.get(proposal["research_ref"])["data"]
        return [{**row, "subject_refs": [proposal["candidate_ref"], raw_ref or research["profile_ref"]],
                 "evidence_refs": [c["source"]]} for row in deepcopy(source["issues"])]

    old_issues = issues(old)
    cert = certify(c, old, old_issues)
    newp = deepcopy(p)
    newp["reader_markdown"] = "Changed presentation and separately researched positive-scale cells."
    newp["regimes"].append({"id": "unrelated-positive-scale"})
    provisional = c["proposal"](newp)
    new_issues = issues(provisional)
    current = c["proposal"](newp, research_issues=new_issues)
    c.update(old=old, cert=cert, p=p, newp=newp, current=current, old_issues=old_issues, new_issues=new_issues, rebound_issues=issues)
    return c


def build(c, current=None, review=None):
    return build_review_context(c["ws"].artifacts, c["ws"], current or c["current"], review or c["cert"])


def test_real_three_long_lived_issues_do_not_blanket_invalidate_scoped_zero_call_bound(zero):
    c = zero
    old, _ = c["review"](subject=c["old"], issues=c["old_issues"])
    legacy = build(c, review=old)
    assert legacy["invalidated_bounds"][0]["reason"] == "prior_bound_blocker"
    out = build(c)
    assert out["reusable_bound_ids"] == ["u"]
    assert out["reuse_candidates"][0]["scope"] == "bound_applicability"
    assert out["current_issue_evidence"][0]["semantic_signatures"] == out["prior_issue_evidence"][0]["semantic_signatures"]
    assert out["current_issue_evidence"][0]["material_signatures"] != out["prior_issue_evidence"][0]["material_signatures"]
    assert out["current_issue_evidence"][0]["evidence_refs"] == [c["source"]]
    assert "joint_analysis" in out["always_review"] and "prepared_sidecars" in out["always_review"]
    assert "approved_bound_ids" not in out


@pytest.mark.parametrize("field", ["message", "scope", "kind", "blocks", "direct_subject", "new_issue", "evidence_ref", "foreign_profile"])
def test_real_issue_math_evidence_and_unbound_addresses_remain_conservative(zero, field):
    c = zero; issues = deepcopy(c["new_issues"])
    if field in {"message", "scope"}:
        issues[0][field] += " Changed mathematical obligation."
    elif field == "kind":
        issues[0][field] = "proof_gap"
    elif field == "blocks":
        issues[0][field].append("publication")
    elif field == "direct_subject":
        issues[0]["subject_refs"].append("u")
    elif field == "new_issue":
        issues.append({**issues[0], "issue_id": "new-direct-counterexample", "subject_refs": ["u"]})
    elif field == "evidence_ref":
        # Even a current-profile SHA in evidence_refs is not a subject address.
        issues[0]["evidence_refs"].append(c["ws"].artifacts.get(c["current"])["data"]["profile_ref"])
    else:
        otherp = deepcopy(c["p"]); otherp["reader_markdown"] = "Unbound profile."
        foreign = c["proposal"](otherp)
        issues[0]["subject_refs"] = [c["ws"].artifacts.get(foreign)["data"]["profile_ref"]]
    out = build(c, c["proposal"](c["newp"], research_issues=issues))
    assert out["reusable_bound_ids"] == []
    assert out["invalidated_bounds"][0]["reason"] == "new_bound_blocker_or_unresolved_scope"


@pytest.mark.parametrize("field", ["oracle", "parameters", "effective_view", "bound_proof", "dependency"])
def test_true_mathematical_changes_invalidate_even_with_unaffected_issue_scopes(zero, field):
    c = zero; p = deepcopy(c["newp"])
    if field == "oracle":
        p["common_specification"]["oracle"]["summary"] = "A genuinely different native oracle."
    elif field == "parameters":
        p["parameters"].append({"id": "changed_zero_scale_assumption"})
    elif field == "effective_view":
        p["views"][0]["algorithms"]["adaptivity"] = "nonadaptive_only"
    elif field == "bound_proof":
        p["bounds"][0]["statement"] += " Under changed assumptions."
    else:
        replacement = c["ws"].artifacts.put("source", {"url": "https://example.invalid/changed", "version": "changed",
            "content_hash": "changed", "text": "Changed source theorem.", "metadata": {}}, c["producer"])
        p["evidence"][0]["source_refs"] = [replacement]
    provisional = c["proposal"](p)
    out = build(c, c["proposal"](p, research_issues=c["rebound_issues"](provisional)))
    assert not out["reusable_bound_ids"]


@pytest.mark.parametrize("mode", ["missing_version", "missing_scope", "incomplete", "affected", "direct", "producer", "unvalidated"])
def test_scope_requires_actual_completed_independent_full_scope(zero, mode):
    c = zero; issues = deepcopy(c["old_issues"])
    if mode == "direct":
        issues[0]["subject_refs"].append("u")
    ref = certify(c, c["old"], issues, version=mode != "missing_version", complete=mode != "incomplete",
                  affected=["u"] if mode == "affected" else [], role="profile_researcher" if mode == "producer" else "profile_reviewer",
                  validated=mode != "unvalidated")
    if mode == "missing_scope":
        data = deepcopy(c["ws"].artifacts.get(ref)["data"]); data["bound_issue_scopes"] = []
        errors = bound_approval_errors(data, {"subject_ref": c["old"]}, c["ws"].artifacts)
        assert any("scope_missing" in e["message"] for e in errors)
    else:
        assert not build(c, review=ref)["reusable_bound_ids"]


def test_bound_reuse_current_freeze_is_explicit_and_recomputed(zero):
    c = zero; out = build(c)
    context_ref = c["ws"].artifacts.put("external_result", out, "controller")
    ref = certify(c, c["current"], c["new_issues"])
    data = deepcopy(c["ws"].artifacts.get(ref)["data"])
    data["coverage_audit"] = {"reused_bound_ids": ["u"], "reuse_context_ref": context_ref}
    inputs = {"subject_ref": c["current"], "review_context_ref": context_ref}
    assert bound_approval_errors(data, inputs, c["ws"].artifacts) == []
    tampered = deepcopy(data); tampered["bound_approvals"][0]["context_pointers"].append("/regimes")
    assert any("declaration_changed" in e["message"] for e in bound_approval_errors(tampered, inputs, c["ws"].artifacts))
    tampered_context = deepcopy(out); tampered_context["reuse_candidates"][0]["fingerprint"] = "forged"
    fake = c["ws"].artifacts.put("external_result", tampered_context, "controller")
    data["coverage_audit"]["reuse_context_ref"] = fake
    assert any("controller_verifiable" in e["message"] for e in bound_approval_errors(data, {**inputs, "review_context_ref": fake}, c["ws"].artifacts))


@pytest.mark.parametrize("scoped", [True, False])
def test_proof_scope_inherits_only_opted_in_snapshot_address_semantics(proof_context, scoped):
    c = proof_context; art = c["ws"].artifacts
    oldraw = art.get(art.get(c["prior"])["data"]["research_ref"])["data"]["profile_ref"]
    issue = c["issue"](subjects=[oldraw])
    ref, jid = c["proof_review"](issues=[issue], scopes=[c["proof_scope"]()])
    if scoped:
        review = deepcopy(art.get(ref)["data"]); review["issue_scope_version"] = "snapshot-bound-scope"
        ref = art.put("review", review, jid)
        c["ws"].save_job(jid, "complete", {}, {"status": "complete", "artifact_refs": [ref], "summary": "fixture", "checkpoint_ref": None})
        c["ws"].event(jid, "validated_handoff", {"status": "complete", "refs": [ref]})
    p = deepcopy(c["profile"]); p["reader_markdown"] = "Updated current presentation."
    provisional = c["proposal"](p)
    raw = art.get(art.get(provisional)["data"]["research_ref"])["data"]["profile_ref"]
    current = c["proposal"](p, research_issues=[{**issue, "subject_refs": [raw]}])
    out = build_proof_review_context(art, c["ws"], current, ref)
    assert out["reusable_proof_refs"] == ([c["proof_ref"]] if scoped else [])
    if scoped:
        changed = c["proposal"](p, research_issues=[{**issue, "subject_refs": [raw], "message": "The zero-scale proof now has a new defect."}])
        assert not build_proof_review_context(art, c["ws"], changed, ref)["reusable_proof_refs"]
