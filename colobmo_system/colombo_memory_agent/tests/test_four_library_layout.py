"""Regression checks for the four-library layout; fake reviews are test fixtures only."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
P=Path(__file__).resolve().parents[1]
V=P.parent
sys.path[:0]=[str(V/'src'),str(P/'runtime'),str(P/'tools')]
from colombo.memory.store import Store as ReadStore,read_json
from colombo.memory.contracts import ContractError,LIBRARIES,digest
from colombo.memory.retrieval import Reader
from colombo.memory.integration import _validate_store
from colombo_memory_agent.store import WriterStore
from repair_layout import migrate
from memory_test_fixtures import candidate_records

EXAMPLES=read_json(P/'examples/complete_candidate_records.json')


def bytes_tree(root):
    return {x.relative_to(root).as_posix():hashlib.sha256(x.read_bytes()).hexdigest()
            for x in root.rglob('*') if x.is_file()}


def test_review(proposal):
    return {'proposal_digest':proposal['digest'],'curator_run_id':proposal['curator_run_id'],
            'reviewer_run_id':'TEST-REVIEW','backend':'fake','coverage':['TEST ONLY'],
            'items':[{'id':r['id'],'record_hash':digest(r),'decision':'accept',
                      'content_fidelity':'checked','navigation_fidelity':'checked',
                      'proof_review':'complete_local_argument_checked','issues':[]} for r in proposal['records']]}


class FourLibraryLayoutTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'memory';self.store=WriterStore(self.root);self.store.initialize()

    def assert_four(self):
        self.assertEqual({p.name for p in self.root.iterdir()},set(LIBRARIES.values()))
        self.assertTrue(all(p.is_file() and p.suffix=='.json' for d in self.root.iterdir() for p in d.iterdir()))

    def test_empty_initialization_creates_only_four_libraries(self):
        self.assert_four();_validate_store(self.store)

    def test_leads_are_content_files_not_snapshot_copies(self):
        leads=deepcopy(EXAMPLES)
        for r in leads:r['evidence']['readiness']='lead'
        self.store.install_leads(leads);self.assert_four()
        self.assertEqual(len(list(self.root.rglob('*.json'))),len(leads))
        self.assertFalse(list(self.store.state_root.glob('cache/**/records/*.json')))
        self.assertEqual({r['id']:digest(r) for r in leads},
                         {r['id']:digest(r) for r in self.store.lead_records()})
        _validate_store(self.store)

    def test_prepare_and_publication_never_add_workflow_files_to_libraries(self):
        p=self.store.prepare(deepcopy(EXAMPLES),curator_run_id='TEST-C',job_id='TEST-J')
        self.assert_four()
        self.assertTrue((self.store.state_root/'staging'/p['proposal_id']/'proposal.json').exists())
        receipt=self.store.publish(p,test_review(p),authorized=True,allow_test_receipt=True)
        self.assert_four();self.assertEqual(receipt['status'],'published');_validate_store(self.store)

    def test_promotion_keeps_one_current_file_and_pinned_history(self):
        leads=deepcopy(EXAMPLES)
        for r in leads:r['evidence']['readiness']='lead'
        self.store.install_leads(leads)
        p=self.store.prepare(deepcopy(EXAMPLES),curator_run_id='TEST-C',job_id='TEST-J')
        self.store.publish(p,test_review(p),authorized=True,allow_test_receipt=True)
        self.assertEqual(self.store.lead_records(),[])
        self.assertEqual(len(list(self.root.rglob('*.json'))),len(EXAMPLES))
        self.assertTrue(list((self.store.state_root/'history').rglob('r000001-*.json')))
        _validate_store(self.store)

    def test_old_published_reference_survives_new_revision(self):
        p=self.store.prepare(deepcopy(EXAMPLES),curator_run_id='TEST-C',job_id='TEST-J')
        a=self.store.publish(p,test_review(p),authorized=True,allow_test_receipt=True)
        ref=a['published_refs'][0];before=Reader(self.store)._record(ref)
        records=self.store.all_records()
        for r in records:r['summary']+=' Test-only annotation.'
        q=self.store.prepare(records,curator_run_id='TEST-C2',job_id='TEST-J2')
        self.store.publish(q,test_review(q),authorized=True,allow_test_receipt=True)
        self.assertEqual(Reader(self.store)._record(ref),before);self.assert_four();_validate_store(self.store)

    def test_failed_publication_restores_visible_files_and_pointers(self):
        p=self.store.prepare(deepcopy(EXAMPLES),curator_run_id='TEST-C',job_id='TEST-J')
        before=bytes_tree(self.root);old=read_json(self.store.state_root/'CURRENT.json')
        with patch.object(self.store,'_commit_generation',side_effect=OSError('TEST injected failure')):
            with self.assertRaises(OSError):self.store.publish(p,test_review(p),authorized=True,allow_test_receipt=True)
        self.assertEqual(bytes_tree(self.root),before)
        self.assertEqual(read_json(self.store.state_root/'CURRENT.json'),old)
        _validate_store(self.store)

    def test_interrupted_publication_restores_leads_and_pointers(self):
        leads=deepcopy(EXAMPLES)
        for r in leads:r['evidence']['readiness']='lead'
        self.store.install_leads(leads)
        p=self.store.prepare(deepcopy(EXAMPLES),curator_run_id='TEST-C',job_id='TEST-J')
        before=bytes_tree(self.root)
        pointers={name:(self.store.state_root/name).read_bytes() for name in ('CURRENT.json','LEADS.json')}
        with patch.object(self.store,'_commit_generation',side_effect=KeyboardInterrupt('TEST interruption')):
            with self.assertRaises(KeyboardInterrupt):
                self.store.publish(p,test_review(p),authorized=True,allow_test_receipt=True)
        self.assertEqual(bytes_tree(self.root),before)
        self.assertEqual({name:(self.store.state_root/name).read_bytes() for name in pointers},pointers)
        self.assertFalse((self.store.state_root/'.writer.lock').exists())
        _validate_store(self.store)

    def test_interrupted_import_restores_a_replaced_lead_pointer(self):
        leads=deepcopy(EXAMPLES)
        for r in leads:r['evidence']['readiness']='lead'
        self.store.install_leads(leads)
        before=bytes_tree(self.root);old=(self.store.state_root/'LEADS.json').read_bytes()
        for r in leads:r['summary']+=' Test-only changed candidate.'
        save=self.store._save_lead_catalog
        def interrupt(records):
            save(records)
            raise KeyboardInterrupt('TEST interruption after pointer replacement')
        with patch.object(self.store,'_save_lead_catalog',side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):self.store.install_leads(leads)
        self.assertEqual(bytes_tree(self.root),before)
        self.assertEqual((self.store.state_root/'LEADS.json').read_bytes(),old)
        _validate_store(self.store)

    def test_uncommitted_history_is_not_a_published_reference(self):
        p=self.store.prepare(deepcopy(EXAMPLES),curator_run_id='TEST-C',job_id='TEST-J')
        with patch.object(self.store,'_commit_generation',side_effect=OSError('TEST injected failure')):
            with self.assertRaises(OSError):self.store.publish(p,test_review(p),authorized=True,allow_test_receipt=True)
        self.assertTrue(list((self.store.state_root/'history').rglob('r000001-*.json')))
        self.assertEqual(self.store.manifest()['entries'],{})
        for r in p['records']:
            with self.assertRaisesRegex(ContractError,'has not been published'):
                Reader(self.store)._record(self.store.ref(r))
        _validate_store(self.store)

    def test_pinned_reads_match_committed_revision_kind_and_hash(self):
        p=self.store.prepare(deepcopy(EXAMPLES),curator_run_id='TEST-C',job_id='TEST-J')
        receipt=self.store.publish(p,test_review(p),authorized=True,allow_test_receipt=True)
        ref=receipt['published_refs'][0]
        records=self.store.all_records()
        for r in records:r['summary']+=' Test-only new revision.'
        q=self.store.prepare(records,curator_run_id='TEST-C2',job_id='TEST-J2')
        current=self.store.publish(q,test_review(q),authorized=True,allow_test_receipt=True)
        latest=next(x for x in current['published_refs'] if x['id']==ref['id'])
        self.assertEqual(Reader(self.store)._record(ref)['revision'],1)
        self.assertEqual(Reader(self.store)._record(latest)['revision'],2)
        for field,value in [('revision',2),('kind','theorem' if ref['kind']!='theorem' else 'source'),('content_hash',latest['content_hash'])]:
            forged={**ref,field:value}
            with self.assertRaisesRegex(ContractError,'has not been published'):
                Reader(self.store)._record(forged)

    def test_published_read_cannot_substitute_latest_for_a_missing_revision(self):
        p=self.store.prepare(deepcopy(EXAMPLES),curator_run_id='TEST-C',job_id='TEST-J')
        receipt=self.store.publish(p,test_review(p),authorized=True,allow_test_receipt=True)
        ref=receipt['published_refs'][0]
        for revision in (None,True,0,'1'):
            with self.assertRaisesRegex(ContractError,'exact positive revision'):
                Reader(self.store)._record({**ref,'revision':revision})

    def test_published_record_cannot_be_overwritten_by_candidate_import(self):
        p=self.store.prepare(deepcopy(EXAMPLES),curator_run_id='TEST-C',job_id='TEST-J')
        self.store.publish(p,test_review(p),authorized=True,allow_test_receipt=True)
        lead=deepcopy(EXAMPLES[0]);lead['evidence']['readiness']='lead'
        with self.assertRaises(ContractError):self.store.install_leads([lead])
        _validate_store(self.store)

    def test_untracked_files_fail_closed_instead_of_disappearing(self):
        (self.root/'source'/'unexpected.json').write_text('{}')
        with self.assertRaises(ContractError):_validate_store(self.store)


class LegacyMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.root=(Path(cls.tmp.name)/'memory').resolve()
        cls.root.mkdir()
        # Build the retired layout explicitly; public runtime must not depend on
        # private deployment archives or original model execution logs.
        from colombo.memory.store import atomic_json
        records=candidate_records()
        manifest={'schema':'colombo-memory-catalog/2','entries':{},'receipts':{},'sequence':0}
        atomic_json(cls.root/'.generations/g-fixture/manifest.json',manifest)
        atomic_json(cls.root/'CURRENT.json',{'generation':'g-fixture','manifest_hash':digest(manifest)})
        atomic_json(cls.root/'LEADS.json',{'path':'cache/fixture','count':len(records)})
        for record in records:
            atomic_json(cls.root/'cache/fixture/records'/(record['id']+'.json'),record)
        proposal={'records':records,'curator_run_id':'TEST-ONLY','job_id':'TEST-ONLY'}
        proposal['digest']=digest(proposal)
        atomic_json(cls.root/'staging/proposal-fixture/proposal.json',proposal)
        (cls.root/'legacy-note.txt').write_text('Synthetic legacy backup fixture.\n')
        cls.before=bytes_tree(cls.root)
        cls.dry=migrate(cls.root);cls.after_dry=bytes_tree(cls.root)
        old=read_json(cls.root/'LEADS.json');cls.original={p.stem:p.read_bytes() for p in (cls.root/old['path']/'records').glob('*.json')}
        cls.result=migrate(cls.root,apply=True);cls.store=ReadStore(cls.root)

    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()

    def test_dry_run_does_not_write(self):
        self.assertEqual(self.dry['status'],'plan_only');self.assertEqual(self.before,self.after_dry)

    def test_all_current_objects_preserve_exact_bytes(self):
        self.assertEqual(self.result['records'],len(self.original))
        for r in self.store.current_records():
            self.assertEqual(self.store.current_path(r['id'],r['kind']).read_bytes(),self.original[r['id']])

    def test_archive_contains_every_original_file_unchanged(self):
        with zipfile.ZipFile(self.store.state_root/'archive/previous_layout.zip') as z:
            actual={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()}
        self.assertEqual(self.before,actual)

    def test_prepared_proposals_are_retained(self):
        self.assertEqual(len(list((self.store.state_root/'staging').glob('proposal-*/proposal.json'))),1)
        with zipfile.ZipFile(self.store.state_root/'archive/previous_layout.zip') as archive:
            self.assertEqual((self.store.state_root/'staging/proposal-fixture/proposal.json').read_bytes(),
                             archive.read('staging/proposal-fixture/proposal.json'))

    def test_all_five_read_operations_are_read_only(self):
        before=(bytes_tree(self.root),bytes_tree(self.store.state_root));r=Reader(self.store)
        overview=r.overview(include_leads=True);self.assertEqual(sum(overview['counts'].values()),len(self.original))
        hit=r.search('coordinate',include_leads=True)['items'][0]
        self.assertTrue(r.browse(hit['research_use'][0]['concept_id'],include_leads=True)['items'])
        self.assertIn('text',r.read(hit['ref']));self.assertIn('items',r.expand(hit['ref'],include_leads=True))
        self.assertEqual(before,(bytes_tree(self.root),bytes_tree(self.store.state_root)))

    def test_idempotence_and_no_review_promotion(self):
        self.assertEqual(migrate(self.root,apply=True)['status'],'already_four_libraries')
        self.assertEqual(self.store.manifest()['entries'],{})
        self.assertTrue(all(r['evidence']['readiness']=='lead' for r in self.store.current_records()))

if __name__=='__main__':unittest.main()
