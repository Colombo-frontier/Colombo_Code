"""Structural/operational tests only. Synthetic reviews are never real reviews."""
from __future__ import annotations
from copy import deepcopy
import json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'tools'));sys.path.insert(0,str(P/'runtime'))
from _agent_bootstrap import AGENT_ROOT,DEFAULT_MEMORY_ROOT,DATASET_ROOT
from dataset import load_dataset,digest,ContractError
from import_staging import import_dataset,RECEIPT
from colombo_memory_agent.store import Store
from colombo.memory.store import read_json
from colombo.memory.contracts import validate_review,validate_record,resolve_pointer
from colombo.memory.retrieval import Reader
import create_job as jobs
from memory_test_fixtures import candidate_records

class DeliveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rs=candidate_records();cls.by={r['id']:r for r in cls.rs}
        cls.tmp=tempfile.TemporaryDirectory(prefix='colombo-import-tests-')
        cls.dataset_root=Path(cls.tmp.name)/'candidates'
        fixture=Store(cls.dataset_root);fixture.initialize();fixture.install_leads(cls.rs)
        cls.root=Path(cls.tmp.name)/'memory'
        cls.import_result=import_dataset(cls.root,dataset_root=cls.dataset_root)
        cls.store=Store(cls.root);cls.receipt=read_json(cls.store.state_root/RECEIPT)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_all_fixture_records_imported(self):
        self.assertEqual({r['id'] for r in self.store.lead_records()},set(self.by))
    def test_no_false_acceptance(self):
        for r in self.rs:
            self.assertEqual(r['evidence']['readiness'],'lead')
    def test_navigation_preserved(self):
        for r in self.rs:
            self.assertEqual(read_json(self.store.current_path(r['id'],r['kind']))['navigation'],r['navigation'])
    def test_all_pointers_resolve(self):
        for r in self.rs:
            validate_record(r)
            for f in r['navigation']['facets']:
                resolve_pointer(r,f['scope_ref'])
                for x in f['evidence_refs']:resolve_pointer(r,x)
    def test_all_links_resolve(self):
        for r in self.rs:
            for s in r['source_refs']:self.assertEqual(self.by[s['source_id']]['kind'],'source')
            for l in r['links']:self.assertIn(l['target_id'],self.by)
    def test_import_groups_one_proposal_per_paper(self):
        self.assertEqual(self.import_result['records'],len(self.rs))
        self.assertEqual(self.import_result['proposals'],1)
        self.assertEqual(len(self.receipt['proposals']),1)
    def test_published_empty(self):self.assertEqual(self.store.manifest()['entries'],{})
    def test_prepared_hashes_and_revision(self):
        for entry in self.receipt['proposals']:
            p=self.store.load_proposal(entry['proposal_id'])
            self.assertEqual(p['digest'],entry['digest'])
            for r in p['records']:
                self.assertEqual(r['revision'],1)
                self.assertEqual(digest(r),entry['prepared_record_hashes'][r['id']])
    def test_repeat_import_checks_snapshot(self):
        repeated=import_dataset(self.root,dataset_root=self.dataset_root)
        self.assertEqual(repeated['status'],'already_imported_verified')
        self.assertEqual(repeated['canonical_published'],0)
    def test_new_import_has_only_four_current_scientific_libraries(self):
        self.assertEqual({p.name for p in self.root.iterdir()},
                         {'algorithm_family_library','hard_family_library','theorem_library','source'})
        self.assertEqual({r['id']:digest(r) for r in load_dataset(self.root)},
                         {r['id']:digest(r) for r in self.rs})
        self.assertFalse((self.root/'ingest').exists())
        self.assertFalse((self.root/'staging').exists())
        self.assertTrue((self.store.state_root/RECEIPT).is_file())
    def test_new_source_job_does_not_read_r3_without_explicit_paper(self):
        source=Path(self.tmp.name)/'new-original.md';source.write_text('Synthetic new-source protocol fixture.')
        with patch.object(jobs,'load_dataset',side_effect=AssertionError('Dataset must not be read')):
            result=jobs.create_job(out=Path(self.tmp.name)/'new-source-job.json',job_id='without-r3',
                sources=[source],papers=[],focus=['new source'],objective='protocol fixture',
                dataset_root=Path(self.tmp.name)/'missing-dataset')
        self.assertEqual(result['seed_records'],0)
        self.assertEqual(result['job']['seed_files'],[])
        self.assertEqual(result['model_calls'],0)
    def test_different_selection_refused(self):
        with self.assertRaises(ContractError):import_dataset(self.root,['P999'],dataset_root=self.dataset_root)
    def test_nonempty_root_refused(self):
        root=Path(self.tmp.name)/'legacy';root.mkdir(exist_ok=True)
        (root/'old.json').write_text('do not overwrite')
        with self.assertRaises(ContractError):import_dataset(root,['PTEST'],dataset_root=self.dataset_root)
        self.assertEqual((root/'old.json').read_text(),'do not overwrite')
    def test_unknown_paper_refused(self):
        with self.assertRaises(ContractError):import_dataset(Path(self.tmp.name)/'unknown',['P999'],dataset_root=self.dataset_root)
    def test_missing_independent_reviews_not_auto_accept(self):
        self.assertEqual(self.receipt['independent_reviews_run_by_this_import'],0)
        self.assertEqual(self.receipt['canonical_records_published_by_this_import'],0)
        self.assertTrue(all(p['review_state']=='not_executed' for p in self.receipt['proposals']))
    def test_default_search_excludes_leads(self):
        self.assertEqual(Reader(self.store).search('coordinate')['items'],[])
    def test_discovery_search_has_review_warning(self):
        hits=Reader(self.store).search('coordinate',include_leads=True)['items']
        self.assertTrue(hits)
        for card in hits:
            self.assertEqual(card['ref']['tier'],'lead')
            self.assertFalse(card['review_status'].get('independent_review_performed',False))
            self.assertFalse(card['certifies_applicability'])
            self.assertTrue(card['evidence']['use_restrictions'])
    def test_read_uses_fixed_candidate_hash(self):
        reader=Reader(self.store)
        hit=reader.search('coordinate',include_leads=True,limit=1)['items'][0]
        got=reader.read(hit['ref'],limit=20000)
        self.assertTrue(got['text']);self.assertEqual(got['ref']['content_hash'],hit['ref']['content_hash'])
        wrong=deepcopy(hit['ref']);wrong['content_hash']='0'*64
        with self.assertRaises(ContractError):reader.read(wrong)
    def test_fake_lead_acceptance_rejected(self):
        p=self.store.load_proposal(self.receipt['proposals'][0]['proposal_id']);r=p['records'][0]
        fake={'proposal_digest':p['digest'],'curator_run_id':p['curator_run_id'],
              'reviewer_run_id':'TEST-ONLY-independent-name','backend':'fake','coverage':['TEST ONLY'],
              'items':[{'id':r['id'],'record_hash':digest(r),'decision':'accept',
                        'content_fidelity':'checked','navigation_fidelity':'checked',
                        'proof_review':'not_checked','issues':[]}]}
        with self.assertRaisesRegex(ContractError,'Lead cannot'):validate_review(p,fake)
        with self.assertRaisesRegex(ContractError,'Simulation'):self.store.publish(p,fake,authorized=True)
        self.assertEqual(self.store.manifest()['entries'],{})
    def test_stale_review_digest_rejected(self):
        p=self.store.load_proposal(self.receipt['proposals'][0]['proposal_id'])
        fake={'proposal_digest':'0'*64,'curator_run_id':p['curator_run_id'],
              'reviewer_run_id':'TEST-ONLY','backend':'fake','coverage':['TEST ONLY'],'items':[]}
        with self.assertRaisesRegex(ContractError,'different proposal'):validate_review(p,fake)
    def test_same_call_cannot_be_reviewer(self):
        p=self.store.load_proposal(self.receipt['proposals'][0]['proposal_id'])
        fake={'proposal_digest':p['digest'],'curator_run_id':p['curator_run_id'],
              'reviewer_run_id':p['curator_run_id'],'backend':'fake','coverage':['TEST ONLY'],'items':[]}
        with self.assertRaisesRegex(ContractError,'separate calls'):validate_review(p,fake)
    def test_no_assumption_not_negation(self):
        c={'facets':[{'axis':'MODEL','concept_id':'strong_convexity','state':'not_assumed','role':'requires','subject':'f'}]}
        result=Reader._checks(c,[{'axis':'MODEL','concept_id':'strong_convexity','state':'asserted'}])
        self.assertEqual(result[0]['status'],'unknown')
    def test_reference_records_cannot_be_reimported_as_leads(self):
        references=deepcopy(self.rs)
        for record in references:record['evidence']['readiness']='reference'
        with patch('import_staging.load_dataset',return_value=references):
            with self.assertRaisesRegex(ContractError,'reviewed references'):
                import_dataset(Path(self.tmp.name)/'reimport',dataset_root=self.dataset_root)

if __name__=='__main__':unittest.main(verbosity=2)
