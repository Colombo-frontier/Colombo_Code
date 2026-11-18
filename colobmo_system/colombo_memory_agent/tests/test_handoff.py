"""Handoff integration tests. All model responses here are synthetic protocol fixtures."""
from __future__ import annotations
from copy import deepcopy
import hashlib,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
P=Path(__file__).resolve().parents[1]
CORE=P.parent
sys.path.insert(0,str(CORE/'src'));sys.path.insert(0,str(P/'runtime'));sys.path.insert(0,str(P/'tools'))
sys.path.insert(0,str(CORE/'tools/memory'))
from colombo.memory.store import atomic_json,read_json
from colombo.memory.contracts import ContractError,digest
from colombo.memory import integration as memory_integration
from colombo.memory.integration import register_builtin_memory
from colombo.memory.mcp_adapter import ScopedReader
from colombo.memory.retrieval import Reader
from colombo_memory_agent.store import WriterStore as Store
from colombo_memory_agent.backend import ModelResult,CodexBackend
from colombo_memory_agent.workflow import Workflow
from import_staging import import_dataset
from create_job import create_job
from freeze_application import freeze
from export_navigation import export
from smoke_readonly import smoke
from doctor import inspect
from memory_test_fixtures import candidate_records
EXAMPLES=json.loads((P/'examples/complete_candidate_records.json').read_text(encoding='utf-8'))

class MockMCP:
    def __init__(self):self.tools={}
    def tool(self,**kwargs):
        def register(fn):self.tools[kwargs.get('name',fn.__name__)]=fn;return fn
        return register

class FakeBackend:
    name='fake'
    def __init__(self,records=None,decision='accept',bind_sources=True):
        self.records=deepcopy(records or EXAMPLES);self.decision=decision;self.calls=[];self.bind_sources=bind_sources
    def run(self,*,role,prompt,schema,workspace,runs):
        run_id=f'{role}-SYNTHETIC-{len(self.calls)}';directory=runs/run_id;directory.mkdir(parents=True)
        self.calls.append({'role':role,'prompt':prompt,'run_id':run_id})
        if role=='curator':
            records=deepcopy(self.records)
            if self.bind_sources:
                # Synthetic protocol records must reference this synthetic job's
                # actual input snapshot, not the unrelated packaged math note.
                source=read_json(runs.parent/'source_manifest.json')[0]
                for record in records:
                    if record['kind']=='source':
                        record['content']['original_material'][0]['artifact_ref']=source['snapshot_path']
            payload={'records_json':json.dumps(records),'coverage':['SYNTHETIC: protocol fixture'],'remaining':[]}
        else:
            current=read_json(runs.parent/'current_review_input.json');proposal=read_json(Path(current['proposal_path']))
            items=[{'id':r['id'],'record_hash':digest(r),'decision':self.decision,'content_fidelity':'checked',
                    'navigation_fidelity':'checked','proof_review':'complete_local_argument_checked','issues':[]} for r in proposal['records']]
            payload={'items_json':json.dumps(items),'coverage':['SYNTHETIC: not an independent scientific review']}
        atomic_json(directory/'model-output.json',payload)
        return ModelResult(run_id,'fake',payload,directory)

class ReadIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.base=Path(cls.tmp.name);cls.root=cls.base/'memory'
        cls.records=candidate_records()
        store=Store(cls.root);store.initialize();store.install_leads(cls.records)
        cls.reader=Reader(store)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_local_doctor_no_model_call(self):
        r=inspect(root=self.root);self.assertTrue(r['local_data_tools_ready']);self.assertFalse(r['model_called']);self.assertEqual(r['store']['published_records'],0)
    def test_builtin_registration_uses_default_memory_root(self):
        m=MockMCP()
        with patch.object(memory_integration,'DEFAULT_MEMORY_ROOT',self.root):
            self.assertTrue(register_builtin_memory(m,research_mode='oracle_complexity'))
        r=m.tools['scientific_memory']('search',json.dumps({'query':'SPIDER','include_leads':True}))
        self.assertTrue(r['items']);self.assertFalse(r['items'][0]['certifies_applicability'])
    def test_registration_and_tool_contract(self):
        m=MockMCP();self.assertTrue(register_builtin_memory(m,research_mode='oracle_complexity',memory_root=self.root))
        r=m.tools['scientific_memory']('search',json.dumps({'query':'SPIDER','include_leads':True}))
        self.assertTrue(r['items']);self.assertFalse(r['items'][0]['certifies_applicability'])
    def test_relative_root_not_allowed(self):
        with self.assertRaises(ContractError):register_builtin_memory(MockMCP(),research_mode='generic',memory_root='relative')
    def test_unknown_mode_rejected(self):
        with self.assertRaises(ContractError):register_builtin_memory(MockMCP(),research_mode='invented',memory_root=self.root)
    def test_generic_only_theorem(self):
        m=MockMCP();register_builtin_memory(m,research_mode='generic',memory_root=self.root)
        r=m.tools['scientific_memory']('search',json.dumps({'query':'SPIDER','include_leads':True}))
        self.assertTrue(r['items']);self.assertTrue(all(c['ref']['kind']=='theorem' for c in r['items']))
    def test_generic_does_not_trust_ref_kind(self):
        hit=self.reader.search('SPIDER',kinds=['algorithm'],include_leads=True)['items'][0]
        ref=deepcopy(hit['ref']);ref['kind']='theorem'
        with self.assertRaises(ContractError):ScopedReader(self.root,allowed_kinds={'theorem'}).call('read',ref=ref)
    def test_new_reader_is_read_only(self):
        r=smoke(self.root,self.base/'smoke');self.assertTrue(r['memory_bytes_unchanged'])
    def test_export_preserves_unreviewed_state(self):
        r=export(self.root,self.base/'export',True)
        self.assertEqual(r['records'],len(self.records))
        self.assertEqual(r['paper_views'],sum(x['kind']=='source' for x in self.records))
        cards=[json.loads(x) for x in (self.base/'export/cards.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertTrue(all(c['ref']['tier']=='lead' for c in cards))
    def test_export_without_leads_is_empty(self):
        r=export(self.root,self.base/'export_published',False);self.assertEqual(r['records'],0)
    def test_export_cannot_write_library(self):
        with self.assertRaises(ContractError):export(self.root,self.root/'navigation',True)
    def test_freeze_inspiration_not_certificate(self):
        ref=self.reader.search('SPIDER',kinds=['algorithm'],include_leads=True)['items'][0]['ref']
        r=freeze(self.root,[ref],self.base/'frozen','check sample coupling','needs_transfer')
        self.assertEqual(r['status'],'frozen_not_certified');self.assertGreater(r['unfrozen_dependencies'],0)
    def test_lead_direct_refused(self):
        ref=self.reader.search('SPIDER',include_leads=True)['items'][0]['ref']
        with self.assertRaises(ContractError):freeze(self.root,[ref],self.base/'bad_direct','obligation','direct')
    def test_freeze_hash_and_path_guard(self):
        ref=deepcopy(self.reader.search('SPIDER',include_leads=True)['items'][0]['ref']);ref['content_hash']='0'*64
        with self.assertRaises(ContractError):freeze(self.root,[ref],self.base/'bad_hash','obligation')
        with self.assertRaises(ContractError):freeze(self.root,[ref],self.root/'frozen','obligation')

class JobTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name);self.root=self.base/'memory';self.store=Store(self.root);self.store.initialize()
        self.source=self.base/'original note.txt';self.source.write_text('SYNTHETIC transport fixture; not actual science review.')
    def tearDown(self):self.tmp.cleanup()
    def job(self,**overrides):
        x={'job_id':'test-job','objective':'protocol only','source_files':[str(self.source)],'focus_anchors':['test'],
           'publication_policy':'stage_only','max_rounds':2};x.update(overrides);return x
    def test_initialize_refuses_legacy_root(self):
        r=self.base/'legacy';r.mkdir();(r/'old').write_text('keep')
        with self.assertRaises(ContractError):Store(r).initialize()
        self.assertEqual((r/'old').read_text(),'keep')
    def test_job_generator_with_dependencies(self):
        records=candidate_records();self.store.install_leads(records)
        r=create_job(out=self.base/'jobs/fixture.json',job_id='fixture-test',sources=[self.source],papers=['PTEST'],
                     focus=['estimator'],objective='test',dataset_root=self.root)
        self.assertEqual(r['seed_records'],len(records));self.assertEqual(r['model_calls'],0)
        self.assertEqual(r['job']['publication_policy'],'stage_only')
    def test_job_generator_refuses_overwrite(self):
        kwargs=dict(out=self.base/'job.json',job_id='unique',sources=[self.source],papers=[],focus=[],objective='test')
        create_job(**kwargs)
        with self.assertRaises(ContractError):create_job(**kwargs)
    def test_job_generator_requires_original(self):
        with self.assertRaises(ContractError):create_job(out=self.base/'j.json',job_id='unique',sources=[],papers=['P038'],focus=[],objective='test')
    def test_default_job_logs_are_agent_scoped_without_creating_directories(self):
        package=self.base/'not-created-agent'
        workflow=Workflow(self.store,FakeBackend(),package)
        self.assertEqual(workflow.jobs_root,(package/'jobs').resolve())
        self.assertFalse(package.exists())
    def test_fresh_role_calls_and_source_snapshots(self):
        backend=FakeBackend();result=Workflow(self.store,backend,P,jobs_root=self.base/'jobs').run(self.job())
        self.assertEqual(result['status'],'completed');self.assertEqual([x['role'] for x in backend.calls],['curator','reviewer'])
        self.assertNotEqual(backend.calls[0]['run_id'],backend.calls[1]['run_id']);self.assertIsNone(result['receipt'])
        manifest=read_json(self.base/'jobs/test-job/source_manifest.json')
        self.assertEqual(Path(manifest[0]['snapshot_path']).read_bytes(),self.source.read_bytes())
        self.assertIn('query_memory.py',backend.calls[0]['prompt']);self.assertIn('seed_manifest.json',backend.calls[1]['prompt'])
        self.assertEqual(self.store.manifest()['entries'],{})
        proposal=self.store.load_proposal(result['proposal_id'])
        source=next(r for r in proposal['records'] if r['kind']=='source')
        self.assertEqual(source['content']['original_material'][0]['artifact_ref'],manifest[0]['snapshot_path'])
        self.assertEqual(source['content']['original_material'][0]['content_hash'],manifest[0]['sha256'])
    def test_source_hash_is_bound_by_runner_not_trusted_from_model(self):
        records=deepcopy(EXAMPLES);source=next(r for r in records if r['kind']=='source')
        source['content']['original_material'][0].update(artifact_ref=str(self.source),content_hash='0'*64)
        backend=FakeBackend(records=records,bind_sources=False)
        result=Workflow(self.store,backend,P,jobs_root=self.base/'jobs').run(self.job(max_rounds=1))
        self.assertEqual(result['status'],'completed');self.assertIsNone(result['receipt'])
        proposal=self.store.load_proposal(result['proposal_id'])
        prepared=next(r for r in proposal['records'] if r['kind']=='source')
        material=prepared['content']['original_material'][0]
        self.assertEqual(material['content_hash'],hashlib.sha256(self.source.read_bytes()).hexdigest())
        self.assertNotEqual(material['content_hash'],'0'*64)
        review=read_json(Path(result['review_path']))
        reviewed=next(i for i in review['items'] if i['id']==prepared['id'])
        self.assertEqual(reviewed['record_hash'],digest(prepared))
    def test_unregistered_source_path_enters_bounded_structural_repair(self):
        records=deepcopy(EXAMPLES);source=next(r for r in records if r['kind']=='source')
        source['content']['original_material'][0]['artifact_ref']=str(self.base/'not-a-job-input.txt')
        backend=FakeBackend(records=records,bind_sources=False)
        result=Workflow(self.store,backend,P,jobs_root=self.base/'jobs').run(self.job(max_rounds=2))
        self.assertEqual(result['status'],'budget_exhausted');self.assertEqual(result['last_status'],'rejected_candidate')
        self.assertEqual(result['feedback']['kind'],'structural')
        self.assertIn('not a registered job source',result['feedback']['error'])
        self.assertEqual([x['role'] for x in backend.calls],['curator','curator'])
        self.assertIn('not a registered job source',backend.calls[1]['prompt'])
        self.assertEqual(list((self.root/'staging').glob('proposal-*')),[])
        self.assertEqual(self.store.manifest()['entries'],{})
    def test_empty_or_remote_only_materials_do_not_bind_a_source(self):
        for index,materials in enumerate(([],[{'artifact_ref':'https://example.invalid/source','content_hash':'0'*64}])):
            with self.subTest(materials=materials):
                records=deepcopy(EXAMPLES);source=next(r for r in records if r['kind']=='source')
                source['content']['original_material']=materials
                backend=FakeBackend(records=records,bind_sources=False)
                result=Workflow(self.store,backend,P,jobs_root=self.base/'jobs').run(self.job(job_id=f'unbound-source-{index}',max_rounds=1))
                self.assertEqual(result['last_status'],'rejected_candidate')
                self.assertIn('actual job source',result['feedback']['error'])
                self.assertEqual([x['role'] for x in backend.calls],['curator'])
        self.assertEqual(list((self.root/'staging').glob('proposal-*')),[])
    def test_one_bound_material_does_not_excuse_an_unregistered_local_material(self):
        records=deepcopy(EXAMPLES);source=next(r for r in records if r['kind']=='source')
        source['content']['original_material']=[{'artifact_ref':str(self.source),'content_hash':'0'*64},
            {'artifact_ref':str(self.base/'unregistered.txt'),'content_hash':'0'*64}]
        result=Workflow(self.store,FakeBackend(records=records,bind_sources=False),P,jobs_root=self.base/'jobs').run(self.job(max_rounds=1))
        self.assertEqual(result['last_status'],'rejected_candidate')
        self.assertIn('unregistered.txt',result['feedback']['error'])
        self.assertEqual(list((self.root/'staging').glob('proposal-*')),[])
    def test_remote_metadata_can_supplement_an_actual_job_source(self):
        records=deepcopy(EXAMPLES);source=next(r for r in records if r['kind']=='source')
        source['content']['original_material']=[{'artifact_ref':str(self.source),'content_hash':'0'*64},
            {'artifact_ref':'https://example.invalid/bibliographic-entry','content_hash':None}]
        result=Workflow(self.store,FakeBackend(records=records,bind_sources=False),P,jobs_root=self.base/'jobs').run(self.job(max_rounds=1))
        self.assertEqual(result['status'],'completed')
        prepared=next(r for r in self.store.load_proposal(result['proposal_id'])['records'] if r['kind']=='source')
        self.assertEqual(prepared['content']['original_material'][0]['content_hash'],hashlib.sha256(self.source.read_bytes()).hexdigest())
        self.assertEqual(prepared['content']['original_material'][1]['artifact_ref'],'https://example.invalid/bibliographic-entry')
    def test_source_change_blocks_resume(self):
        backend=FakeBackend();w=Workflow(self.store,backend,P,jobs_root=self.base/'jobs');w.run(self.job());self.source.write_text('changed')
        with self.assertRaises(ContractError):w.run(self.job(),resume=True)
    def test_snapshot_tamper_blocks_completed_resume(self):
        w=Workflow(self.store,FakeBackend(),P,jobs_root=self.base/'jobs');w.run(self.job())
        m=read_json(self.base/'jobs/test-job/source_manifest.json')
        Path(m[0]['snapshot_path']).write_text('tampered')
        with self.assertRaises(ContractError):w.run(self.job(),resume=True)
    def test_policy_change_blocks_resume(self):
        w=Workflow(self.store,FakeBackend(),P,jobs_root=self.base/'jobs');w.run(self.job())
        with self.assertRaises(ContractError):w.run(self.job(publication_policy='publish_reviewed'),resume=True)
    def test_completed_resume_makes_no_new_model_calls(self):
        b=FakeBackend();w=Workflow(self.store,b,P,jobs_root=self.base/'jobs');a=w.run(self.job());c=w.run(self.job(),resume=True)
        self.assertEqual(a,c);self.assertEqual(len(b.calls),2)
    def test_resume_cannot_retarget_completed_agent_job_to_another_memory(self):
        backend=FakeBackend();jobs_root=self.base/'jobs'
        Workflow(self.store,backend,P,jobs_root=jobs_root).run(self.job())
        calls_before=len(backend.calls)
        other=Store(self.base/'other-memory');other.initialize()
        with self.assertRaises(ContractError):
            Workflow(other,backend,P,jobs_root=jobs_root).run(self.job(),resume=True)
        self.assertEqual(len(backend.calls),calls_before)
        self.assertEqual(other.manifest()['entries'],{})
    def test_fake_cannot_publish(self):
        with self.assertRaisesRegex(ContractError,'Simulation'):Workflow(self.store,FakeBackend(),P,jobs_root=self.base/'jobs').run(self.job(publication_policy='publish_reviewed'))
        self.assertEqual(self.store.manifest()['entries'],{})
    def test_deferred_budget_is_bounded(self):
        b=FakeBackend(decision='defer');r=Workflow(self.store,b,P,jobs_root=self.base/'jobs').run(self.job(max_rounds=2))
        self.assertEqual(r['status'],'completed_with_deferred_items');self.assertEqual(len(b.calls),4);self.assertIsNone(r['receipt'])
    def test_actual_review_persisted_in_simulated_store(self):
        # Explicit test-only bypass; this review is never used on the bundled scientific data.
        p=self.store.prepare(deepcopy(EXAMPLES),curator_run_id='TEST-C',job_id='TEST')
        review={'proposal_digest':p['digest'],'curator_run_id':'TEST-C','reviewer_run_id':'TEST-R','backend':'fake','coverage':['SYNTHETIC'],
          'items':[{'id':r['id'],'record_hash':digest(r),'decision':'accept','content_fidelity':'checked',
                    'navigation_fidelity':'checked','proof_review':'complete_local_argument_checked','issues':[]} for r in p['records']]}
        receipt=self.store.publish(p,review,authorized=True,allow_test_receipt=True)
        self.assertEqual(read_json(Store(self.root).state_root/'staging'/p['proposal_id']/'review.json'),review)
        card=Reader(self.store).search('coordinate')['items'][0]
        self.assertEqual(card['publication']['review_backend'],'fake');self.assertEqual(receipt['status'],'published')

if __name__=='__main__':unittest.main(verbosity=2)
