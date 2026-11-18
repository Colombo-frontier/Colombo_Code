"""Interrupted jobs resume their unfinished phase in isolated synthetic Stores."""
from copy import deepcopy
from pathlib import Path
import os
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

from test_handoff import FakeBackend, P
from colombo.memory.contracts import ContractError, digest
from colombo.memory.store import atomic_json, read_json
from colombo_memory_agent.store import Store
from colombo_memory_agent.backend import BackendTransportError, CodexBackend
from colombo_memory_agent import backend as backend_module
from colombo_memory_agent.workflow import Workflow
from colombo_memory_agent import workflow as workflow_module


class InterruptedBackend(FakeBackend):
    def __init__(self, role, error):
        super().__init__()
        self.role, self.error = role, error

    def run(self, **kwargs):
        if kwargs['role'] == self.role:
            raise self.error('Synthetic interruption; no real process launched')
        return super().run(**kwargs)


class NoCallsBackend:
    def run(self, **kwargs):
        raise AssertionError('Recovery must reuse saved work without a model call')


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='memory-recovery-')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.store = Store(self.base / 'memory')
        self.store.initialize()
        self.source = self.base / 'source.txt'
        self.source.write_text('SYNTHETIC protocol fixture, not scientific review.')
        self.job = {'job_id': 'recovery-test', 'objective': 'Synthetic recovery test',
                    'source_files': [str(self.source)], 'focus_anchors': ['protocol'],
                    'publication_policy': 'stage_only', 'max_rounds': 1}
        self.checkpoint = self.base / 'jobs/recovery-test/checkpoint.json'

    def workflow(self, backend):
        return Workflow(self.store, backend, P, jobs_root=self.base / 'jobs')

    def interrupt_review(self, error=OSError):
        backend = InterruptedBackend('reviewer', error)
        with self.assertRaises(error):
            self.workflow(backend).run(self.job)
        return read_json(self.checkpoint)

    def test_final_round_review_resumes_without_repeating_curator(self):
        checkpoint = self.interrupt_review()
        self.assertEqual(checkpoint['status'], 'reviewing')
        backend = FakeBackend()
        result = self.workflow(backend).run(self.job, resume=True)
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(result['proposal_id'], checkpoint['proposal_id'])
        self.assertEqual([call['role'] for call in backend.calls], ['reviewer'])
        self.assertEqual(read_json(self.checkpoint)['round'], 1)

    def test_ctrl_c_during_review_keeps_the_pending_proposal(self):
        checkpoint = self.interrupt_review(KeyboardInterrupt)
        backend = FakeBackend()
        result = self.workflow(backend).run(self.job, resume=True)
        self.assertEqual(result['proposal_id'], checkpoint['proposal_id'])
        self.assertEqual([call['role'] for call in backend.calls], ['reviewer'])

    def test_review_transport_failure_can_resume_the_final_round(self):
        checkpoint = self.interrupt_review(BackendTransportError)
        self.assertEqual(checkpoint['status'], 'reviewing')
        backend = FakeBackend()
        result = self.workflow(backend).run(self.job, resume=True)
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(result['proposal_id'], checkpoint['proposal_id'])
        self.assertEqual([call['role'] for call in backend.calls], ['reviewer'])

    def test_legacy_prepared_checkpoint_can_complete_its_final_round(self):
        checkpoint = self.interrupt_review()
        checkpoint['status'] = 'prepared'
        checkpoint.pop('proposal_digest')
        checkpoint.pop('base_revisions_snapshot')
        atomic_json(self.checkpoint, checkpoint)
        backend = FakeBackend()
        result = self.workflow(backend).run(self.job, resume=True)
        self.assertEqual(result['status'], 'completed')
        self.assertEqual([call['role'] for call in backend.calls], ['reviewer'])

    def test_interrupted_curator_retries_current_round(self):
        with self.assertRaises(OSError):
            self.workflow(InterruptedBackend('curator', OSError)).run(self.job)
        self.assertEqual(read_json(self.checkpoint)['round'], 1)
        backend = FakeBackend()
        result = self.workflow(backend).run(self.job, resume=True)
        self.assertEqual(result['status'], 'completed')
        self.assertEqual([call['role'] for call in backend.calls], ['curator', 'reviewer'])
        self.assertEqual(read_json(self.checkpoint)['round'], 1)

    def test_saved_review_resumes_without_any_new_model_call(self):
        def interrupted_write(path, value):
            atomic_json(path, value)
            if path == self.checkpoint and value.get('status') == 'reviewed':
                raise OSError('Synthetic interruption after persisting validated review')
        with patch.object(workflow_module, 'atomic_json', side_effect=interrupted_write):
            with self.assertRaises(OSError):
                self.workflow(FakeBackend()).run(self.job)
        self.assertEqual(read_json(self.checkpoint)['status'], 'reviewed')
        result = self.workflow(NoCallsBackend()).run(self.job, resume=True)
        self.assertEqual(result['status'], 'completed')
        self.assertIsNone(result['receipt'])

    def test_publication_failure_resumes_from_saved_review(self):
        self.job['publication_policy'] = 'publish_reviewed'
        with patch.object(self.store, 'publish', side_effect=OSError('Synthetic publication interruption')):
            with self.assertRaises(OSError):
                self.workflow(FakeBackend()).run(self.job)
        self.assertEqual(read_json(self.checkpoint)['status'], 'publishing')
        publish = self.store.publish
        # Test-only bypass, restricted to this temporary fixture Store.
        with patch.object(self.store, 'publish', side_effect=lambda p, r, **kw:
                          publish(p, r, **kw, allow_test_receipt=True)):
            result = self.workflow(NoCallsBackend()).run(self.job, resume=True)
        self.assertEqual(result['receipt']['status'], 'published')
        self.assertEqual(self.store.manifest()['sequence'], 1)

    def test_committed_publication_recovery_returns_same_receipt(self):
        self.job['publication_policy'] = 'publish_reviewed'
        publish = self.store.publish
        committed = []
        def publish_then_interrupt(proposal, review, **kwargs):
            committed.append(publish(proposal, review, **kwargs, allow_test_receipt=True))
            raise OSError('Synthetic interruption after commit, before final result')
        with patch.object(self.store, 'publish', side_effect=publish_then_interrupt):
            with self.assertRaises(OSError):
                self.workflow(FakeBackend()).run(self.job)
        self.assertEqual(self.store.manifest()['sequence'], 1)
        with patch.object(self.store, 'publish', side_effect=lambda p, r, **kw:
                          publish(p, r, **kw, allow_test_receipt=True)):
            result = self.workflow(NoCallsBackend()).run(self.job, resume=True)
        self.assertEqual(result['receipt'], committed[0])
        self.assertEqual(self.store.manifest()['sequence'], 1)
        self.assertEqual(len(self.store.manifest()['receipts']), 1)

    def test_pending_proposal_still_requires_unchanged_source_bytes(self):
        self.interrupt_review()
        self.source.write_text('Changed source bytes')
        with self.assertRaisesRegex(ContractError, 'source bytes changed'):
            self.workflow(NoCallsBackend()).run(self.job, resume=True)

    def test_changed_proposal_is_rejected_before_resuming_review(self):
        checkpoint = self.interrupt_review()
        path = self.store.state_root / 'staging' / checkpoint['proposal_id'] / 'proposal.json'
        proposal = read_json(path)
        proposal['records'][0]['title'] = 'Tampered candidate'
        atomic_json(path, proposal)
        with self.assertRaisesRegex(ContractError, 'modified after preparation'):
            self.workflow(NoCallsBackend()).run(self.job, resume=True)

    def test_concurrent_publication_does_not_silently_rebase_pending_work(self):
        checkpoint = self.interrupt_review()
        old = self.store.load_proposal(checkpoint['proposal_id'])
        proposal = self.store.prepare(deepcopy(old['records']), curator_run_id='concurrent-C', job_id='concurrent')
        review = {'proposal_digest': proposal['digest'], 'curator_run_id': 'concurrent-C',
                  'reviewer_run_id': 'concurrent-R', 'backend': 'fake', 'coverage': ['SYNTHETIC'],
                  'items': [{'id': r['id'], 'record_hash': digest(r), 'decision': 'accept',
                             'content_fidelity': 'checked', 'navigation_fidelity': 'checked',
                             'proof_review': 'complete_local_argument_checked', 'issues': []}
                            for r in proposal['records']]}
        self.store.publish(proposal, review, authorized=True, allow_test_receipt=True)
        with self.assertRaisesRegex(ContractError, 'Base revision conflict'):
            self.workflow(NoCallsBackend()).run(self.job, resume=True)

    def test_modified_saved_review_cannot_be_reused(self):
        self.job['publication_policy'] = 'publish_reviewed'
        with patch.object(self.store, 'publish', side_effect=OSError('Synthetic interruption')):
            with self.assertRaises(OSError):
                self.workflow(FakeBackend()).run(self.job)
        checkpoint = read_json(self.checkpoint)
        path = Path(checkpoint['review_path'])
        review = read_json(path)
        review['coverage'].append('Undeclared extra coverage')
        atomic_json(path, review)
        with self.assertRaisesRegex(ContractError, 'review digest mismatch'):
            self.workflow(NoCallsBackend()).run(self.job, resume=True)
        self.assertEqual(self.store.manifest()['entries'], {})


class BackendFailureClassificationTests(unittest.TestCase):
    def check_process_failure(self, timeout):
        with tempfile.TemporaryDirectory(prefix='memory-transport-') as folder:
            root = Path(folder)
            process = Mock(returncode=1, pid=98765)
            if timeout:
                process.communicate.side_effect = [subprocess.TimeoutExpired('synthetic', 1), (None, None)]
            else:
                process.communicate.return_value = (None, None)
            with patch.object(backend_module.shutil, 'which', return_value='/synthetic/codex'), \
                    patch.object(CodexBackend, '_user_preferences', return_value={}), \
                    patch.object(backend_module.subprocess, 'Popen', return_value=process), \
                    patch.object(backend_module.os, 'killpg', create=True) as kill:
                with self.assertRaises(BackendTransportError):
                    CodexBackend(timeout=1).run(role='reviewer', prompt='SYNTHETIC', schema={},
                                              workspace=root, runs=root / 'runs')
                if timeout:
                    if os.name == 'nt':
                        process.kill.assert_called_once()
                    else:
                        kill.assert_called_once()
            receipt = read_json(next((root / 'runs').iterdir()) / 'run.json')
            self.assertEqual(receipt['status'], 'rejected_transport')
            self.assertIn('timed out' if timeout else 'exited with 1', receipt['error'])

    def test_nonzero_model_exit_is_a_resumable_transport_error(self):
        self.check_process_failure(timeout=False)

    def test_model_timeout_is_a_resumable_transport_error(self):
        self.check_process_failure(timeout=True)


if __name__ == '__main__':
    unittest.main()
