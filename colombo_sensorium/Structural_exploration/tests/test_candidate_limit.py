"""Candidate limits cover revision and recovery; scheduling checks only, with no predetermined scientific conclusions."""
from oracle_atlas.workflow.engine import Engine
from oracle_atlas.core.config import DEFAULTS


def test_limit_is_applied_before_extraction_revise_and_pending_resume(tmp_path, monkeypatch):
    cfg={"workspace":str(tmp_path/"work"),"atlas":str(tmp_path/"atlas"),
         "budgets":{**DEFAULTS,"max_candidates":1},"model":{}}
    e=Engine(cfg, object())
    paper=e.put("paper",{"title":"Queue fixture","doi":None,"arxiv_id":None,"urls":[],"publication_events":[],"provenance":[]})
    # Other tests cover complete candidate content; read only candidate_id here to avoid simulating scientific judgment.
    def item(cid):
        return {"candidate_id":cid,"title":cid,"paper_refs":[paper],"common_specification":{},"views":[],"tag_facts":[],"issues":[]}
    # ArtifactStore rejects incomplete eight-axis schemas; use an existing native record for the scheduling fixture.
    refs=[e.put("native_record",item(cid)) for cid in ("selected","needs_revision","pending")]
    extraction=e.put("extraction",{"paper_ref":paper,"candidate_refs":refs})
    review=e.put("review",{"subject_ref":extraction,"review_type":"extraction","verdict":"revise",
        "assessments":[{"subject_id":refs[0],"verdict":"approve","reason":"scheduling fixture"},
                       {"subject_id":refs[1],"verdict":"revise","reason":"scheduling fixture"},
                       {"subject_id":refs[2],"verdict":"revise","reason":"scheduling fixture"}],
        "issues":[],"approved_bound_ids":[],"summary":"No scientific acceptance asserted."})
    monkeypatch.setattr(e,"_job",lambda role,inputs,scope:({"id":role,"status":"complete"},extraction if role=="extractor" else review))
    selected=[]
    def advance(case):
        selected.append(case["candidate_ref"])
        case["state"]="identity_pending";e.ws.save_case(case);return case
    monkeypatch.setattr(e,"_advance",advance)
    monkeypatch.setattr(e,"resume_case",lambda *a,**k:(_ for _ in ()).throw(AssertionError("out-of-limit revision started")))
    result=e.process_paper(paper)
    assert selected==[refs[0]]
    assert [e.ws.case(cid)["state"] for cid in result["case_ids"]]==["identity_pending","queued_by_limit","queued_by_limit"]
    queued=e.ws.case(result["case_ids"][2]);queued["pending_extraction"]={"previous_candidate_ref":refs[2],"feedback_ref":review};e.ws.save_case(queued)
    # Rescanning must not resume pending jobs outside the selected scope.
    e.process_paper(paper)
    assert e.ws.case(queued["case_id"])["pending_extraction"]
    assert e.ws.case(queued["case_id"])["state"]=="queued_by_limit"
    e.ws.close()
