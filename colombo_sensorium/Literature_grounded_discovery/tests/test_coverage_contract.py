"""The coverage ledger tracks traceable obligations; it never automatically converts a checklist into scientific approval."""
from copy import deepcopy
from oracle_atlas.workflow.coverage import CHECKS,coverage_errors
from oracle_atlas.core.store import Workspace


def ledger():
    return {"scope":"synthetic structural test","checks":[{"check_id":k,"scope":"declared test region","status":"unresolved","reason":"Exact named scientific obligation remains; this test asserts no theorem.","result_refs":[],"proof_refs":[]} for k in CHECKS],"issue_resolutions":[]}


def issue(cid):
    return {"issue_id":cid,"kind":"coverage","scope":"parameter endpoint","subject_refs":[],"blocks":["publication"],"message":"Concrete missing endpoint proof.","evidence_refs":[],"resolves":[]}


def test_new_jobs_need_all_checks_but_unresolved_does_not_become_approval(tmp_path):
    ws=Workspace(tmp_path)
    inputs={"coverage_scope_ref":"sha256:"+"a"*64}
    assert coverage_errors({},inputs,"profile_researcher",ws.artifacts)[0]["code"]=="coverage_ledger_missing"
    data={"coverage_ledger":ledger()}
    assert coverage_errors(data,inputs,"profile_researcher",ws.artifacts)==[]
    data["coverage_ledger"]["checks"][0].update(status="verified")
    assert any(e["code"]=="coverage_basis" for e in coverage_errors(data,inputs,"profile_researcher",ws.artifacts))
    assert coverage_errors({}, {},"profile_researcher",ws.artifacts)==[]  # Old fixed records remain readable
    ws.close()


def test_revision_must_track_prior_issues_and_can_add_new_concrete_blocker(tmp_path):
    ws=Workspace(tmp_path)
    subject=ws.artifacts.put("checkpoint",{"summary":"fixture","refs":[],"remaining":[]},"seed")
    old=ws.artifacts.put("review",{"subject_ref":subject,"review_type":"profile","verdict":"revise","assessments":[],"issues":[issue("old")],"approved_bound_ids":[],"summary":"No approval asserted"},"reviewer")
    inputs={"coverage_scope_ref":subject,"repair_feedback_ref":old}
    data={"coverage_ledger":ledger()}
    assert any(e["code"]=="coverage_resolution_missing" for e in coverage_errors(data,inputs,"bound_updater",ws.artifacts))
    audit={"scope":"fixture","checks":ledger()["checks"],"resolved_issue_ids":["old"],"carried_issue_ids":[],"new_blocker_justifications":[],"followups":[],"reuse_context_ref":None,"reused_bound_ids":[]}
    newissue=issue("new");newissue["evidence_refs"]=[subject]
    review={"coverage_audit":audit,"issues":[newissue]}
    assert any(e["code"]=="coverage_new_blocker_basis" for e in coverage_errors(review,inputs,"profile_reviewer",ws.artifacts))
    audit["new_blocker_justifications"]=[{"issue_id":"new","category":"coverage","why_new":"New source or concrete original audit omission, with a precise proof obligation.","affected_subjects":["endpoint"]}]
    assert coverage_errors(review,inputs,"profile_reviewer",ws.artifacts)==[]
    # The program neither deletes the new blocker nor changes it to nonblocking.
    assert review["issues"][0]["blocks"]==["publication"]
    audit["resolved_issue_ids"]=[]
    assert any(e["code"]=="coverage_issue_omitted" for e in coverage_errors(review,inputs,"profile_reviewer",ws.artifacts))
    ws.close()


def test_reuse_declarations_are_checked_before_review_freeze(tmp_path):
    ws=Workspace(tmp_path)
    context=ws.artifacts.put("external_result",{"reusable_bound_ids":["unchanged"]},"controller")
    inputs={"coverage_scope_ref":context,"review_context_ref":context}
    audit={"scope":"fixture","checks":ledger()["checks"],"resolved_issue_ids":[],"carried_issue_ids":[],"new_blocker_justifications":[],"followups":[],"reuse_context_ref":context,"reused_bound_ids":["changed"]}
    data={"coverage_audit":audit,"issues":[],"approved_bound_ids":["changed"]}
    assert any(e["code"]=="review_reuse_scope" for e in coverage_errors(data,inputs,"profile_reviewer",ws.artifacts))
    audit["reused_bound_ids"]=["unchanged"]
    assert any(e["code"]=="review_reuse_adoption" for e in coverage_errors(data,inputs,"profile_reviewer",ws.artifacts))
    data["approved_bound_ids"]=["unchanged"]
    assert coverage_errors(data,inputs,"profile_reviewer",ws.artifacts)==[]
    ws.close()
