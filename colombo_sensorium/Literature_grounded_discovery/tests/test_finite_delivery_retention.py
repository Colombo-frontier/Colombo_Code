"""A rejecting review must not erase a previously authored typed followup.

The lineage is synthetic; no mathematical claims or model calls occur here.
"""
from copy import deepcopy

import pytest

from oracle_atlas.workflow.coverage import coverage_errors, freeze_delivery_scope
from test_atlas import facts
from test_finite_delivery import register
from test_review_context import context


def first_author(c):
    a, prop, inputs, research, profile, row = register(c)
    row["source_review_ref"] = None  # First recorded by the author, before a review.
    profile["delivery_followups"] = [deepcopy(row)]
    research["coverage_ledger"]["followups"] = [deepcopy(row)]
    inputs.pop("repair_feedback_ref"); inputs.pop("delivery_scope_ref")
    research["coverage_ledger"].pop("delivery_scope_ref")
    research["profile_ref"] = a.put("profile", profile, c["producer"])
    assert coverage_errors(research, inputs, "profile_researcher", a) == []
    research_ref = a.put("research", research, c["producer"])
    prepared = c["atlas"].prepare(profile, facts(profile))
    proposal_ref = a.put("proposal", {**prop, "research_ref": research_ref, "profile_ref": research["profile_ref"],
                         "prepared_ref": a.put("prepared", prepared, "controller")}, "controller")
    inputs["subject_ref"] = proposal_ref
    review = {"subject_ref": proposal_ref, "review_type": "profile", "verdict": "revise", "assessments": [],
              "issues": [], "approved_bound_ids": [], "summary": "Synthetic structural fixture only.",
              "coverage_audit": {"scope": "fixture", "checks": research["coverage_ledger"]["checks"],
                    "resolved_issue_ids": [], "carried_issue_ids": [], "new_blocker_justifications": [],
                    "followups": [], "reuse_context_ref": None, "reused_bound_ids": []}}
    return a, inputs, research, research_ref, profile, row, review


@pytest.mark.parametrize("verdict", ["revise", "defer", "approve"])
def test_first_review_cannot_omit_current_author_followup(context, verdict):
    a, inputs, _, _, _, _, review = first_author(context)
    review["verdict"] = verdict
    assert "delivery_followup_lost" in {e["code"] for e in coverage_errors(review, inputs, "profile_reviewer", a)}


@pytest.mark.parametrize("verdict", ["revise", "defer", "approve"])
def test_author_origin_null_can_be_carried_without_inventing_a_prior_review(context, verdict):
    a, inputs, _, _, _, row, review = first_author(context)
    review["verdict"] = verdict
    review["coverage_audit"]["followups"] = [row]
    assert coverage_errors(review, inputs, "profile_reviewer", a) == []


@pytest.mark.parametrize("retained_location", ["both", "profile_only", "ledger_only", "anchor_only"])
def test_legacy_reviewer_omission_cannot_erase_previous_author_record(context, retained_location):
    c = context
    a, inputs, research, research_ref, profile, row, review = first_author(c)
    # Reproduce the previously accepted first-review omission without claiming
    # that a new controller would accept it now.
    legacy_review = a.put("review", review, "legacy-reviewer-fixture")
    candidate = research["candidate_ref"]
    anchor = a.put("external_result", freeze_delivery_scope(a, candidate, legacy_review), "controller")
    previous = deepcopy(research); previous_profile = deepcopy(profile)
    if retained_location == "profile_only":
        previous["coverage_ledger"]["followups"] = []
    elif retained_location == "ledger_only":
        previous_profile.pop("delivery_followups")
    previous["profile_ref"] = a.put("profile", previous_profile, c["producer"])
    previous_ref = a.put("research", previous, c["producer"])
    inputs.update(delivery_scope_ref=anchor, repair_feedback_ref=legacy_review, previous_artifact_ref=previous_ref)
    if retained_location == "anchor_only":
        inputs.pop("previous_artifact_ref")
    revised = deepcopy(research); current_profile = deepcopy(profile)
    current_profile.pop("delivery_followups")
    current_profile["joint_analysis"]["pending_obligations"].remove(row["description"])
    obligations = current_profile["joint_analysis"]["synthesis_coverage"]["obligations"]
    current_profile["joint_analysis"]["synthesis_coverage"]["obligations"] = [o for o in obligations if o["id"] != row["obligation_id"]]
    c["atlas"].prepare(current_profile, facts(current_profile))  # Native math shape alone does not catch the lost lineage.
    revised["profile_ref"] = a.put("profile", current_profile, c["producer"])
    revised["coverage_ledger"].update(delivery_scope_ref=anchor, followups=[], issue_resolutions=[])
    assert "delivery_followup_lost" in {e["code"] for e in coverage_errors(revised, inputs, "profile_researcher", a)}
    # Retain the original author provenance and resolve/retain the native
    # obligation normally; do not fabricate a review that never contained it.
    revised["profile_ref"] = a.put("profile", profile, c["producer"])
    revised["coverage_ledger"].update(followups=[row], issue_resolutions=research["coverage_ledger"]["issue_resolutions"])
    assert coverage_errors(revised, inputs, "profile_researcher", a) == []


def test_rejecting_reviewer_may_add_but_not_replace_authored_followup_evidence(context):
    a, inputs, _, _, _, row, review = first_author(context)
    amended = {**row, "evidence_refs": [context["prior_review"]]}
    review["coverage_audit"]["followups"] = [amended]
    assert "delivery_followup_lost" in {e["code"] for e in coverage_errors(review, inputs, "profile_reviewer", a)}
    amended["evidence_refs"].extend(row["evidence_refs"])
    assert coverage_errors(review, inputs, "profile_reviewer", a) == []
