"""Finite-delivery regressions; these validate routing and provenance, not mathematical theorems."""
from copy import deepcopy

import pytest

from oracle_atlas.core.contracts import ProtocolError, check_review
from oracle_atlas.workflow.coverage import _delivery_errors, coverage_errors, coverage_scope, freeze_delivery_scope
from oracle_atlas.workflow.engine import Engine
from oracle_atlas.workflow.review_packet import assemble_review_packet
from oracle_atlas.workflow.review_context import build_review_context
from oracle_atlas.workflow.proof_reuse import build_proof_review_context
from test_review_context import context
from test_coverage_contract import ledger
from test_atlas import facts


def setup(c):
    a = c["ws"].artifacts
    proposal = a.get(c["prior"])["data"]
    anchor = a.put("external_result", freeze_delivery_scope(a, proposal["candidate_ref"], c["prior_review"]), "controller")
    inputs = {"coverage_scope_ref":a.put("external_result",coverage_scope(proposal["candidate_ref"]),"controller"),
              "delivery_scope_ref":anchor,"subject_ref":c["prior"],"repair_feedback_ref":c["prior_review"]}
    research = deepcopy(a.get(proposal["research_ref"])["data"])
    profile = deepcopy(a.get(research["profile_ref"])["data"])
    return a, proposal, inputs, research, profile


def followup(c):
    return {"scope":"comparison c", "description":"Investigate a distinct stronger construction; fixture only.",
            "reason_nonblocking":"The current registered bound remains valid; no global sharpness is asserted.",
            "obligation_id":"new-family", "evidence_refs":[c["source"]],
            "source_review_ref":None, "retained_claims_valid":True}


def reviewed(c, inputs, row, verdict="revise"):
    return {"subject_ref":inputs["subject_ref"],"review_type":"profile","verdict":verdict,
            "assessments":[],"issues":[],"approved_bound_ids":[],"summary":"Structural test only.",
            "coverage_audit":{"scope":"finite fixture","checks":ledger()["checks"],"resolved_issue_ids":[],"carried_issue_ids":[],
                              "new_blocker_justifications":[],"followups":[row],"reuse_context_ref":None,
                              "reused_bound_ids":[],"delivery_scope_ref":inputs["delivery_scope_ref"]}}


def register(c):
    a, proposal, inputs, research, profile = setup(c)
    row = followup(c)
    decision = reviewed(c, inputs, row)
    previous = a.put("review", decision, "independent-reviewer")
    inputs["repair_feedback_ref"] = previous
    row = {**row,"source_review_ref":previous}
    profile["delivery_followups"] = [row]
    analysis = profile["joint_analysis"]
    analysis["pending_obligations"].append(row["description"])
    analysis["synthesis_coverage"]["status"] = "partial"
    analysis["synthesis_coverage"]["obligations"].append({"id":row["obligation_id"],"kind":"material_lead",
        "comparison_ids":["c"],"cell_ids":[],"bound_refs":[],"state":"pending","affects_gap":True,
        "lead":row["description"],"argument":"Scoped fixture: stronger construction remains pending.","proof_refs":[]})
    research["coverage_ledger"] = {"scope":"finite fixture","checks":ledger()["checks"],"delivery_scope_ref":inputs["delivery_scope_ref"],
        "followups":[row],"issue_resolutions":[{"issue_id":row["obligation_id"],"status":"remaining",
                                             "reason":"Register without asserting a new theorem.","result_refs":[],"proof_refs":[]}]}
    return a, proposal, inputs, research, profile, row


def test_frontier_pins_first_evidence_and_stage_keeps_it_on_new_material(context, monkeypatch):
    c = context
    a, prop, inputs, _, _ = setup(c)
    frozen = a.get(inputs["delivery_scope_ref"])["data"]
    assert frozen["initial_subject_ref"] == c["prior"] and frozen["initial_review_ref"] == c["prior_review"]
    assert c["profile"]["bounds"][0]["result_ref"] in frozen["initial_evidence_refs"]
    engine = Engine.__new__(Engine)
    engine.ws, engine.artifacts = c["ws"], a
    captured = {}
    def job(role, inputs, scope):
        captured.update(inputs)
        return {"id":"paused-fixture","status":"queued"}, None
    monkeypatch.setattr(engine, "_job", job)
    monkeypatch.setattr(engine.ws, "save_case", lambda case: None)
    case = {"case_id":"fixture","jobs":{},"candidate_ref":prop["candidate_ref"],"identity_ref":prop["identity_ref"],
            "delivery_scope_ref":inputs["delivery_scope_ref"],"budget_scope":"fixture","material_refs":[c["source"]]}
    engine._stage(case,"profile_reviewer",{"subject_ref":c["prior"]})
    assert captured["delivery_scope_ref"] == inputs["delivery_scope_ref"]
    packet = a.get(captured["review_packet_ref"])["data"]
    assert packet["review_scope"]["delivery_frontier"] == frozen


def test_first_validated_review_creates_the_case_anchor(context, monkeypatch):
    c = context
    a = c["ws"].artifacts
    prop = a.get(c["prior"])["data"]
    engine = Engine.__new__(Engine)
    engine.ws, engine.artifacts = c["ws"], a
    monkeypatch.setattr(engine, "_job", lambda role, inputs, scope: ({"id":c["reviewer"],"status":"complete"},c["prior_review"]))
    monkeypatch.setattr(engine.ws, "save_case", lambda case: None)
    case = {"case_id":"fixture","jobs":{},"candidate_ref":prop["candidate_ref"],"identity_ref":prop["identity_ref"],"budget_scope":"fixture"}
    engine._stage(case,"profile_reviewer",{"subject_ref":c["prior"]})
    frozen = a.get(case["delivery_scope_ref"])["data"]
    assert frozen["initial_review_ref"] == c["prior_review"]
    assert frozen["initial_research_ref"] == prop["research_ref"]


def test_new_extension_needs_author_registration_before_approval(context):
    c = context
    a, _, inputs, _, _ = setup(c)
    data = reviewed(c, inputs, followup(c))
    assert _delivery_errors(data, inputs, "profile_reviewer", a.get) == []
    data["verdict"] = "approve"
    codes = {e["code"] for e in _delivery_errors(data, inputs, "profile_reviewer", a.get)}
    assert {"delivery_followup_obligation","delivery_followup_unrecorded"} <= codes
    # Initial snapshot-bound-scope reviews also require typed provenance, before a frontier exists.
    inputs.pop("delivery_scope_ref")
    data["verdict"] = "revise"
    data["coverage_audit"]["followups"] = [{"scope":"c","description":"Only prose","reason_nonblocking":"Unknown"}]
    assert "delivery_followup_contract" in {e["code"] for e in coverage_errors(data, inputs, "profile_reviewer", a)}


def test_registered_pending_extension_is_traceable_in_author_profile_and_fresh_review(context):
    c = context
    a, prop, inputs, research, profile, row = register(c)
    research["profile_ref"] = a.put("profile", profile, c["producer"])
    assert coverage_errors(research, inputs, "profile_researcher", a) == []
    rref = a.put("research", research, c["producer"])
    prepared = c["atlas"].prepare(profile, facts(profile))
    assert prepared["files"]["profile.json"]["delivery_followups"] == [row]
    current = a.put("proposal", {**prop,"research_ref":rref,"profile_ref":research["profile_ref"],
                                 "prepared_ref":a.put("prepared",prepared,"controller")}, "controller")
    inputs["subject_ref"] = current
    data = reviewed(c, inputs, row, "approve")
    assert coverage_errors(data, inputs, "profile_reviewer", a) == []
    # This structural pass does not supply the six independent scientific checks or a receipt.
    assert "joint_checks" not in data and "receipt" not in data


@pytest.mark.parametrize("mutation,code", [
    ("delete","delivery_followup_lost"), ("erase_evidence","delivery_followup_lost"),
    ("hide_pending","delivery_followup_visibility"), ("complete","delivery_followup_synthesis"),
    ("unresolved_author","delivery_followup_resolution"), ("unknown_cell","delivery_followup_cells"),
])
def test_pending_findings_cannot_be_dropped_or_mislabeled(context, mutation, code):
    c = context
    a, _, inputs, research, profile, _ = register(c)
    if mutation == "delete":
        research["coverage_ledger"]["followups"] = []
        profile["delivery_followups"] = []
    elif mutation == "erase_evidence":
        research["coverage_ledger"]["followups"][0]["evidence_refs"] = [c["prior_review"]]
    elif mutation == "hide_pending":
        profile["joint_analysis"]["pending_obligations"] = []
    elif mutation == "complete":
        profile["joint_analysis"]["synthesis_coverage"]["status"] = "complete"
    elif mutation == "unresolved_author":
        research["coverage_ledger"]["issue_resolutions"] = []
    else:
        profile["joint_analysis"]["synthesis_coverage"]["obligations"][-1]["cell_ids"] = ["invented"]
    research["profile_ref"] = a.put("profile", profile, c["producer"])
    assert code in {e["code"] for e in _delivery_errors(research, inputs, "profile_researcher", a.get)}


def test_late_actual_counterexample_still_blocks_and_new_optimization_does_not_expand_frontier(context):
    c = context
    a, _, inputs, _, _ = setup(c)
    data = reviewed(c, inputs, followup(c))
    data["coverage_audit"]["followups"] = []
    issue = {"issue_id":"late-error","kind":"coverage","scope":"active upper", "subject_refs":["u"],
             "blocks":["publication"],"message":"A synthetic counterexample invalidates the declared active upper.",
             "evidence_refs":[c["source"]],"resolves":[]}
    data["issues"] = [issue]
    why = {"issue_id":"late-error","category":"correctness","why_new":"The changed premise exposes this defect.",
           "affected_subjects":["u"],"basis":"current_claim_invalid","affected_profile_pointers":["/bounds/0"],"frozen_issue_ids":[]}
    data["coverage_audit"]["new_blocker_justifications"] = [why]
    assert _delivery_errors(data, inputs, "profile_reviewer", a.get) == []
    data["verdict"] = "approve"
    with pytest.raises(ProtocolError):
        check_review(data, inputs["subject_ref"], "profile")
    data["verdict"] = "revise"
    why["basis"] = "new_construction"
    assert "delivery_new_construction" in {e["code"] for e in _delivery_errors(data, inputs, "profile_reviewer", a.get)}
    why.update(basis="frozen_obligation",frozen_issue_ids=["invented-first-review-issue"])
    assert "delivery_frozen_obligation" in {e["code"] for e in _delivery_errors(data, inputs, "profile_reviewer", a.get)}
