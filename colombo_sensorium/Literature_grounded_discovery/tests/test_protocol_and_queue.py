"""Mechanical integration regressions; these are not mathematical conclusions or acceptance by a real model."""
import json
from datetime import date
from pathlib import Path

from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.store import Workspace
from oracle_atlas.providers.base import Reply, ToolCall, ProviderRefusal
from oracle_atlas.workflow.engine import Engine
from oracle_atlas.discovery.bibliography import verify_publication


def config(tmp_path):
    return {'workspace':str(tmp_path/'work'),'atlas':str(tmp_path/'atlas'),'budgets':dict(DEFAULTS),'model':{'model':'synthetic'},'tasks':[{'task_id':'test','label':'Test fixture','queries':['fixture'],'approved':True}]}


class RepairBackend:
    def __init__(self):self.calls=0
    def complete(self,**request):
        self.calls+=1
        if self.calls<=2:
            return Reply(text='{"status":"complete"}',output_items=[{'role':'assistant','type':'message','content':[{'type':'output_text','text':'{"status":"complete"}'}]}])
        if self.calls==3:
            args={'kind':'task_proposal','json_text':json.dumps({'proposals':[],'report_zh':'Offline protocol recovery test, without scientific conclusions.'}),'dependencies':[]}
            call=ToolCall('artifact_put',args,'write-once')
            return Reply(calls=[call],output_items=[{'type':'function_call','call_id':call.call_id,'name':call.name,'arguments':json.dumps(args)}])
        output=next(x for x in reversed(request['input_items']) if x.get('type')=='function_call_output')
        ref=json.loads(output['output'])['ref']
        return Reply(text=json.dumps({'status':'complete','artifact_refs':[ref],'summary':'Protocol recovery verification only','checkpoint_ref':None}))


def test_rejected_response_is_consumed_and_explicit_repair_advances(tmp_path):
    cfg=config(tmp_path);cfg['budgets']['max_protocol_repairs']=1
    backend=RepairBackend();e=Engine(cfg,backend)
    job=e.ws.create_job('task_scout',{'notes':'offline'})
    first=e.runner.run(job,validate_output=e._validate_stage)
    assert first['status']=='protocol_error' and backend.calls==2
    assert e.runner.run(job)['status']=='protocol_error' and backend.calls==2
    final=e.runner.run(job,validate_output=e._validate_stage,repair_protocol=True)
    assert final['status']=='complete' and backend.calls==4
    assert len(e.ws.query("SELECT id FROM calls WHERE status='rejected'"))==2
    assert len(e.ws.query("SELECT ref FROM artifacts WHERE kind='task_proposal'"))==1
    assert e.runner.run(job)['status']=='complete' and backend.calls==4
    feedback=e.ws.query("SELECT ref FROM artifacts WHERE kind='external_result'")
    assert len(feedback)==1  # Identical rejected bodies may be content-deduplicated; both request/rejection records remain distinct
    assert 'invalid_output_json' in e.artifacts.get(feedback[0]['ref'])['data']
    e.ws.close()


def test_refusal_is_never_protocol_resampled(tmp_path):
    class Refuse:
        n=0
        def complete(self,**kwargs):
            self.n+=1;raise ProviderRefusal('refused',{'output':[{'refusal':'fixture'}]})
    backend=Refuse();e=Engine(config(tmp_path),backend)
    job=e.ws.create_job('task_scout',{'notes':'offline'})
    assert e.runner.run(job)['status']=='blocked'
    assert e.runner.run(job,repair_protocol=True)['status']=='blocked'
    assert backend.n==1
    assert e.ws.query('SELECT status FROM calls')[0]['status']=='refusal'
    e.ws.close()


def test_verification_merge_year_queue_complete_handoff(tmp_path,monkeypatch):
    e=Engine(config(tmp_path),object());refs=[]
    for i in range(282):
        paper={'title':f'Queue fixture {i}','doi':f'10.fixture/{i}','arxiv_id':None,'identifiers':{'doi':f'10.fixture/{i}'},'urls':[],'publication_events':[],'provenance':[]}
        refs.append(e.put('paper',paper))
        if i<20:
            verified=verify_publication(paper,date=date(date.today().year, 6, 1).isoformat(),source={'url':'https://example.org/fixture','field':'publication_date'})
            refs.append(e.put('paper',verified))
    request={'task_ids':['test'],'years':[date.today().year],'sources':['crossref'],'query_budget':4,'paper_limit':30,'event_kind':'publication','notes':'synthetic queue regression'}
    plan=e.put('plan',{k:v for k,v in request.items() if k!='event_kind'})
    batch=e.put('paper_batch',{'paper_refs':refs,'coverage':{'fixture':True},'search_refs':[]})
    def job(role,inputs,scope):
        return {'id':role,'status':'complete'},plan if role=='coordinator' else batch
    monkeypatch.setattr(e,'_job',job)
    selected=[]
    def process(ref,budget_scope=None):
        selected.append(ref);return {'paper_ref':ref,'case_ids':[],'status':'fixture_only'}
    monkeypatch.setattr(e,'process_paper',process)
    result=e.scan(request)
    assert result['verified_year_papers']==20
    assert len(result['unverified_or_other_year_refs'])==262
    assert len(selected)==20
    for ref in selected:
        p=e.artifacts.get(ref)['data']
        assert p['publication_events'][0]['verified'] and p['publication_events'][0]['verification_sources']
        assert p['provenance']
    e.ws.close()


def test_document_approval_does_not_approve_a_quarantined_bound():
    import pytest
    from oracle_atlas.core.contracts import check_review, ProtocolError
    subject='sha256:'+'0'*64
    issue={'issue_id':'u-check','kind':'proof_gap','scope':'bound','subject_refs':['u'],'blocks':['bound'],'message':'One proof is unverified.','evidence_refs':[],'resolves':[]}
    review={'subject_ref':subject,'review_type':'profile','verdict':'approve','assessments':[],'issues':[issue],'approved_bound_ids':[],'summary':'The document explicitly quarantines u.'}
    check_review(review,subject,'profile')
    review['approved_bound_ids']=['u']
    with pytest.raises(ProtocolError,match='still subject to a bound blocker'):
        check_review(review,subject,'profile')


def test_candidate_view_positions_are_mapped_to_stable_atlas_view_ids():
    from oracle_atlas.workflow.engine import profile_facts
    candidate={'views':[{'view_id':'random'}],'tag_facts':[{'view_ref':'random','source_pointer':'/views/0/algorithms/randomization'}]}
    identity={'view_mapping':[{'candidate_view_id':'random','atlas_view_id':'randomized','reason':'explicit reviewed normalization'}]}
    profile={'views':[{'view_id':'deterministic'},{'view_id':'randomized'}]}
    facts=profile_facts(candidate,identity,profile)
    assert facts[0]['view_ref']=='randomized'
    assert facts[0]['source_pointer']=='/views/1/algorithms/randomization'
    assert candidate['tag_facts'][0]['source_pointer']=='/views/0/algorithms/randomization'
