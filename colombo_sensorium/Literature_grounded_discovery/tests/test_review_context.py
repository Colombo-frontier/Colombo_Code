"""Re-review candidates must bind valid independent approval and complete unchanged support; this file produces no scientific conclusions."""
from copy import deepcopy
import json
from pathlib import Path
import shutil

import pytest

from oracle_atlas.atlas import Atlas
from oracle_atlas.core.store import Workspace
from oracle_atlas.workflow import review_context as module
from oracle_atlas.workflow.review_context import build_review_context
from test_atlas import facts, profile, set_fixture_analysis


@pytest.fixture
def context(tmp_path):
    root = tmp_path / "atlas"
    shutil.copytree(Path(__file__).parent / "fixtures/native_atlas/data/schemas", root / "data/schemas")
    atlas, ws = Atlas(root), Workspace(tmp_path / "work")
    producer = ws.create_job("profile_researcher", {"engineering_fixture": "support closure"})
    paper = ws.artifacts.put("paper", {"title": "Synthetic review-dependency software fixture", "doi": None,
        "arxiv_id": None, "urls": [], "publication_events": [], "provenance": []}, producer)
    candidate = ws.artifacts.put("candidate", {"candidate_id": "engineering-candidate", "title": "Engineering fixture",
        "paper_refs": [paper], "common_specification": profile()["common_specification"], "views": profile()["views"],
        "tag_facts": facts(profile()), "issues": []}, producer)
    retrieval = ws.artifacts.put("retrieval", {}, "controller")
    identity = ws.artifacts.put("identity", {"candidate_ref": candidate, "decision": "new", "setting_id": None,
        "view_mapping": [], "normalization": "No mathematical inference in this fixture.", "comparisons": [],
        "retrieval_ref": retrieval, "recall_audit": {"strategies": [], "unresolved_ids": [], "reason": "Engineering fixture", "inventory_version": "fixture-baseline"},
        "issues": []}, producer)
    source = ws.artifacts.put("source", {"url": "https://example.invalid/fixture-baseline", "version": "fixed-baseline", "content_hash": "fixture-sha-baseline",
        "text": "Synthetic dependency record; no actual theorem.", "metadata": {}}, producer)

    def result(source_ref=source, version="fixed-baseline"):
        return ws.artifacts.put("result", {"result_id": "engineering-result", "comparison_key": {
            "setting_id": "REVIEW_CONTEXT", "view_id": "randomized", "guarantee_id": "g", "quantity_id": "q", "resource_projection_id": "rp", "regime_id": "r"},
            "direction": "upper", "statement": "Only an engineering fixture.", "formula_latex": "", "conditions": [],
            "parameter_region": "fixture", "algorithm_scope": "fixture", "witness_type": "deterministic", "guarantee": "fixture",
            "resource_accounting": "No model/network/Atlas commit.", "origin": "published_theorem", "source_refs": [source_ref],
            "source_locators": [{"source_ref": source_ref, "version": version, "locator": "fixture"}], "proof_refs": [], "status": "proposed", "issues": []}, producer)

    support = result()
    p = profile("REVIEW_CONTEXT")
    p["bounds"][0]["result_ref"] = support
    p["bounds"][0]["evidence_refs"] = ["evidence:u"]
    p["evidence"] = [{"id": "evidence:u", "result_ref": support}]

    def proposal(p, *, extra_dependencies=(), research_issues=()):
        p = deepcopy(p)
        set_fixture_analysis(p)
        prepared = atlas.prepare(p, facts(p))
        frozen = ws.artifacts.put("profile", prepared["files"]["profile.json"], "controller")
        raw = ws.artifacts.put("profile", deepcopy(p), producer)
        research = ws.artifacts.put("research", {"candidate_ref": candidate, "identity_ref": identity, "action": "new", "setting_id": p["setting_id"],
            "base_version": None, "profile_ref": raw, "result_refs": [b["result_ref"] for b in p["bounds"]], "proof_refs": [], "issues": list(research_issues), "change_summary": "Engineering fixture."}, producer)
        pref = ws.artifacts.put("prepared", prepared, "controller", extra_dependencies)
        return ws.artifacts.put("proposal", {"research_ref": research, "candidate_ref": candidate, "identity_ref": identity,
            "profile_ref": frozen, "prepared_ref": pref, "change_summary": "Engineering fixture.", "base_version": None,
            "inventory_version": "fixture-baseline", "mode": "new"}, "controller")

    prior = proposal(p)

    def review(subject=prior, *, role="profile_reviewer", validated=True, verdict="revise", approved=("u",), issues=()):
        reviewer = ws.create_job(role, {"subject_ref": subject}, nonce=str(len(ws.query("SELECT id FROM jobs"))))
        ref = ws.artifacts.put("review", {"subject_ref": subject, "review_type": "profile", "verdict": verdict,
            "assessments": [{"subject_id": bid, "verdict": "approve", "reason": "Engineering fixture only."} for bid in approved],
            "issues": list(issues), "approved_bound_ids": list(approved), "summary": "Does not assert a real scientific result. Reviewer=" + reviewer}, reviewer)
        ws.save_job(reviewer, "complete", {}, {"status": "complete", "artifact_refs": [ref], "summary": "fixture", "checkpoint_ref": None})
        if validated:
            ws.event(reviewer, "validated_handoff", {"refs": [ref], "status": "complete"})
        return ref, reviewer

    prior_review, reviewer = review()
    yield {"atlas": atlas, "ws": ws, "profile": p, "proposal": proposal, "prior": prior,
           "review": review, "prior_review": prior_review, "source": source, "result": result, "producer": producer, "reviewer": reviewer}
    ws.close()


def build(c, current=None, review=None):
    return build_review_context(c["ws"].artifacts, c["ws"], current or c["proposal"](c["profile"]), review or c["prior_review"])


def test_validated_revise_can_supply_bound_candidate_without_publication_approval(context):
    out = build(context)
    assert out["reusable_bound_ids"] == ["u"]
    assert out["reuse_candidates"][0]["dependency_count"] >= 2
    assert out["previous_review_ref"] == context["prior_review"]
    assert "prepared_sidecars" in out["always_review"]
    assert "comparisons" in out["always_review"]
    assert "approved_bound_ids" not in out


@pytest.mark.parametrize("field", ["common_specification", "parameters", "views"])
def test_unchanged_bound_does_not_reuse_changed_scientific_environment(context, field):
    p = deepcopy(context["profile"])
    if field == "common_specification":
        p[field]["oracle"]["operations"][0]["precision_scope"] = "sampled_function"
    elif field == "parameters":
        p[field].append({"id": "new_assumption", "summary": "A changed global condition."})
    else:
        p[field][0]["algorithms"]["adaptivity"] = "nonadaptive_only"
    out = build(context, context["proposal"](p))
    assert out["unchanged_bound_ids"] == ["u"]
    assert out["reusable_bound_ids"] == []
    assert out["invalidated_bounds"][0]["reason"] == "scientific_environment_or_dependency_changed"


def test_source_version_change_in_local_support_invalidates_candidate(context):
    c, p = context, deepcopy(context["profile"])
    new_source = c["ws"].artifacts.put("source", {"url": "https://example.invalid/fixture-changed", "version": "fixed-changed", "content_hash": "fixture-sha-changed",
        "text": "A different immutable source version.", "metadata": {}}, c["producer"])
    p["references"] = [{"id": "ref:source", "source_ref": new_source}]
    # The bound text is unchanged, but its referenced local evidence and fixed source have changed.
    p["evidence"][0]["source_refs"] = [new_source]
    out = build(c, c["proposal"](p))
    assert out["reusable_bound_ids"] == []
    assert out["unchanged_bound_ids"] == ["u"]


def test_other_bound_and_its_named_evidence_do_not_invalidate_unchanged_support(context):
    c, p = context, deepcopy(context["profile"])
    extra = deepcopy(p["bounds"][0]); extra.update(id="new_bound", statement="A separate unadopted fixture retained as evidence.",
                                                  evidence_refs=["evidence:new"], eligible_for_bracket=False)
    p["bounds"].append(extra)
    p["evidence"].append({"id": "evidence:new", "result_ref": extra["result_ref"]})
    out = build(c, c["proposal"](p))
    assert out["added_bound_ids"] == ["new_bound"]
    assert out["reusable_bound_ids"] == ["u"]


def test_changed_bound_and_different_id_never_inherit_candidate(context):
    p = deepcopy(context["profile"])
    p["bounds"][0]["statement"] = "A changed mathematical assertion."
    out = build(context, context["proposal"](p))
    assert out["changed_bound_ids"] == ["u"] and not out["reusable_bound_ids"]
    p["bounds"][0]["id"] = "different"
    p["comparisons"][0]["bracket"]["upper_refs"] = ["different"]
    out = build(context, context["proposal"](p))
    assert out["added_bound_ids"] == ["different"] and out["removed_bound_ids"] == ["u"]
    assert not out["reusable_bound_ids"]


@pytest.mark.parametrize("role,validated", [("profile_researcher", True), ("profile_reviewer", False)])
def test_producer_forgery_or_unvalidated_handoff_cannot_supply_reuse(context, role, validated):
    ref, _ = context["review"](role=role, validated=validated)
    out = build(context, review=ref)
    assert out["reusable_bound_ids"] == []
    assert out["previous_review_ref"] is None
    assert out["reuse_status"] == "prior_review_unavailable"


def test_review_subject_job_binding_is_verified(context):
    ref, jid = context["review"]()
    with context["ws"].transaction() as db:
        db.execute("UPDATE jobs SET inputs=? WHERE id=?", (json.dumps({"subject_ref": context["source"]}), jid))
    out = build(context, review=ref)
    assert not out["reusable_bound_ids"]
    assert "subject_mismatch" in out["validation_reason"]


def test_missing_source_fails_closed(context):
    c = context
    with c["ws"].transaction() as db:
        db.execute("DELETE FROM artifacts WHERE ref=?", (c["source"],))
    out = build(c)
    assert not out["reusable_bound_ids"]
    assert out["invalidated_bounds"][0]["reason"].startswith("dependency_unavailable")


@pytest.mark.parametrize("name,value,reason", [
    ("MAX_DEPENDENCY_BYTES", 1, "dependency_byte_limit"),
    ("MAX_DEPENDENCIES", 1, "dependency_count_or_depth_limit"),
    ("MAX_DEPENDENCY_DEPTH", 0, "dependency_count_or_depth_limit"),
])
def test_complete_but_excessive_dependency_closure_is_not_reusable(context, monkeypatch, name, value, reason):
    monkeypatch.setattr(module, name, value)
    out = build(context)
    assert not out["reusable_bound_ids"]
    assert reason in out["invalidated_bounds"][0]["reason"]


def test_dependency_cycle_cannot_be_treated_as_complete(context):
    c = context
    with c["ws"].transaction() as db:
        db.execute("UPDATE artifacts SET deps=? WHERE ref=?", (json.dumps([c["source"]]), c["source"]))
    out = build(c)
    assert not out["reusable_bound_ids"]
    assert "dependency_cycle" in out["invalidated_bounds"][0]["reason"]


def test_source_locator_version_mismatch_denies_reuse_even_if_prior_review_listed_it(context):
    c, p = context, deepcopy(context["profile"])
    bad = c["result"](version="arXiv-label-instead-of-fixed-version")
    p["bounds"][0]["result_ref"] = bad
    p["evidence"][0]["result_ref"] = bad
    prior = c["proposal"](p)
    review, _ = c["review"](subject=prior)
    out = build(c, c["proposal"](p), review)
    assert not out["reusable_bound_ids"]
    assert "result_source_version_mismatch" in out["invalidated_bounds"][0]["reason"]


def test_frozen_prepared_hash_and_reviewer_independence_are_checked(context):
    c = context
    art = c["ws"].artifacts
    old = art.get(c["prior"])["data"]
    badprepared = deepcopy(art.get(old["prepared_ref"])["data"])
    badprepared["bundle_hash"] = "0" * 64
    badref = art.put("prepared", badprepared, "controller")
    badprop = art.put("proposal", {**old, "prepared_ref": badref}, "controller")
    review, _ = c["review"](subject=badprop)
    out = build(c, review=review)
    assert not out["reusable_bound_ids"] and "prepared_hash_mismatch" in out["validation_reason"]
    ref, jid = c["review"]()
    with c["ws"].transaction() as db:
        db.execute("INSERT INTO ownership VALUES(?,?)", (c["prior"], jid))
    out = build(c, review=ref)
    assert not out["reusable_bound_ids"] and "not_independent" in out["validation_reason"]


def test_structural_unassessed_fields_remain_for_new_review(context):
    p = deepcopy(context["profile"])
    p["summary_status"]["note"] = "Changed reader annotation requires independent review."
    p["reader_markdown"] = "Changed reader text needs current independent review."
    out = build(context, context["proposal"](p))
    assert out["reusable_bound_ids"] == ["u"]
    assert {"summary_status", "reader_markdown"}.issubset(out["changed_profile_fields"])
    assert {"summary_status", "reader_markdown", "prepared_sidecars"}.issubset(out["always_review"])


def test_resolved_audit_history_does_not_change_mathematical_support(context):
    p = deepcopy(context["profile"])
    p["issues"] = [{"issue_id": "format-fixed", "kind": "protocol_error", "scope": "previous draft",
        "subject_refs": [], "blocks": [], "message": "A mechanically resolved bookkeeping issue.",
        "evidence_refs": [context["prior"]], "resolves": []}]
    out = build(context, context["proposal"](p))
    assert out["reusable_bound_ids"] == ["u"]
    assert "current_and_resolved_issues" in out["always_review"]


def test_new_global_or_same_bound_issue_revokes_candidate(context):
    p = deepcopy(context["profile"])
    p["issues"] = [{"issue_id": "new-counterexample", "kind": "proof_gap", "scope": "A newly discovered decisive gap.",
        "subject_refs": ["u"], "blocks": ["bound", "publication"], "message": "This is deliberately not cleared by reuse.",
        "evidence_refs": [], "resolves": []}]
    out = build(context, context["proposal"](p))
    assert not out["reusable_bound_ids"]
    assert out["invalidated_bounds"][0]["reason"] == "new_bound_blocker_or_unresolved_scope"


def bound_issue(subjects):
    return {"issue_id": "explicit-bound-obligation", "kind": "proof_gap", "scope": "No inferred mathematical scope in this fixture.",
        "subject_refs": subjects, "blocks": ["bound"], "message": "An unresolved engineering negative-control obligation.",
        "evidence_refs": [], "resolves": []}


def profile_with_proof(context):
    c = context
    proof = c["ws"].artifacts.put("proof", {"proof_id": "engineering-proof", "origin": "analyst_derivation",
        "proposition": "Software dependency fixture only.", "premises": [], "argument": "Not scientific evidence.",
        "boundary_cases": "Not applicable.", "quantifiers": "Fixture only.", "resource_accounting": "No model/network.",
        "dependencies": [], "issues": []}, c["producer"])
    p = deepcopy(c["profile"])
    card = deepcopy(c["ws"].artifacts.get(p["bounds"][0]["result_ref"])["data"])
    card["proof_refs"] = [proof]
    support = c["ws"].artifacts.put("result", card, c["producer"])
    p["bounds"][0]["result_ref"] = support
    p["evidence"][0]["result_ref"] = support
    return p, proof


def test_new_research_issue_on_fixed_proof_revokes_candidate(context):
    c = context
    p, proof = profile_with_proof(c)
    prior = c["proposal"](p)
    review, _ = c["review"](subject=prior)
    current = c["proposal"](p, research_issues=[bound_issue([proof])])
    out = build(c, current, review)
    assert out["unchanged_bound_ids"] == ["u"]
    assert not out["reusable_bound_ids"]
    assert out["invalidated_bounds"][0]["reason"] == "new_bound_blocker_or_unresolved_scope"
    assert "research_issues" in out["always_review"]


@pytest.mark.parametrize("subjects", [[], ["unregistered-ambiguous-scope"]])
def test_unresolved_new_research_scope_fails_closed(context, subjects):
    c = context
    out = build(c, c["proposal"](c["profile"], research_issues=[bound_issue(subjects)]))
    assert not out["reusable_bound_ids"]
    assert out["invalidated_bounds"][0]["reason"] == "new_bound_blocker_or_unresolved_scope"


def test_prior_review_proof_blocker_cannot_supply_reuse_even_with_bound_approved(context):
    c = context
    p, proof = profile_with_proof(c)
    prior = c["proposal"](p)
    # Generic check_review checks contradictions by direct bound ID only; explicit dependency closure must be checked here.
    review, _ = c["review"](subject=prior, approved=["u"], issues=[bound_issue([proof])])
    out = build(c, c["proposal"](p), review)
    assert out["reuse_status"] == "candidates_verified"
    assert not out["reusable_bound_ids"]
    assert out["invalidated_bounds"][0]["reason"] == "prior_bound_blocker"


@pytest.mark.parametrize("issue_location", ["research", "profile", "prior_review"])
def test_explicitly_other_bound_blocker_does_not_revoke_unaffected_candidate(context, issue_location):
    c = context
    p = deepcopy(c["profile"])
    other = deepcopy(p["bounds"][0])
    other.update(id="other", evidence_refs=["evidence:other"])
    p["bounds"].append(other)
    p["evidence"].append({"id": "evidence:other", "result_ref": other["result_ref"]})
    prior = c["proposal"](p)
    issue = bound_issue(["other"])
    review, _ = c["review"](subject=prior, issues=[issue] if issue_location=="prior_review" else [])
    current = deepcopy(p)
    if issue_location=="profile":current["issues"]=[issue]
    prop = c["proposal"](current, research_issues=[issue] if issue_location=="research" else [])
    out = build(c, prop, review)
    assert out["reusable_bound_ids"] == ["u"]
    assert next(row for row in out["invalidated_bounds"] if row["bound_id"]=="other")["reason"] == "not_previously_approved_bound"


def test_controller_commit_cannot_supply_a_missing_reviewer_hash(context):
    from oracle_atlas.atlas.store import AtlasValidationError
    from oracle_atlas.core.config import DEFAULTS
    from oracle_atlas.workflow.engine import Engine
    from test_atlas import JOINT_CHECKS

    c = context
    cfg = {"workspace": str(c["ws"].root), "atlas": str(c["atlas"].root),
           "budgets": dict(DEFAULTS), "model": {}, "tasks": []}
    controller = Engine(cfg, backend=None)
    try:
        old = controller.artifacts.get(c["prior"])["data"]
        proposal = controller.put("proposal", {**old, "inventory_version": controller.atlas.version()})
        subject_ref, reviewer = c["review"](subject=proposal, verdict="approve", approved=["u"])
        original = controller.artifacts.get(subject_ref)["data"]
        review_ref = controller.artifacts.put("review", {**original, "joint_checks": JOINT_CHECKS}, reviewer)
        case = {"proposal_ref": proposal, "profile_review_ref": review_ref, "case_id": "unbound-scientific-review"}
        with pytest.raises(AtlasValidationError, match="five-file snapshot"):
            controller._commit(case)
        assert controller.atlas.version("REVIEW_CONTEXT") is None
        assert "prepared_hash" not in controller.artifacts.get(review_ref)["data"]
    finally:
        controller.ws.close()
