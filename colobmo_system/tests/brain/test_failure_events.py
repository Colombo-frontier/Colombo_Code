"""Current Controller execution faults remain distinct from terminal Cell Results."""
import unittest
from unittest.mock import patch
from colombo.brain.controller import NeedsAttention
from colombo.brain.research_records import state_view
from controller_fixtures import OracleTestFixture
from test_oracle_workflow import Backend


class FailureEventTests(OracleTestFixture, unittest.TestCase):
    def test_unreconciled_worker_exception_is_visible_without_claiming_termination(self):
        backend = Backend()
        controller = self.controller(backend)
        with patch.object(self.adapter, 'run', side_effect=RuntimeError('Synthetic supervisor identity lost')):
            with self.assertRaisesRegex(RuntimeError, 'identity lost'):
                controller.run()
        state = state_view(self.store)
        self.assertEqual(state['status'], 'needs_attention')
        self.assertTrue(state['execution_faults'])
        self.assertTrue(all(not x['payload']['termination_confirmed'] for x in state['execution_faults']))
        self.assertEqual(self.store.get_meta('result_events'), [])
        self.assertIsNone(self.store.get_meta('progress_ref'))
        self.assertFalse('process_results' in backend.calls)
        fault_count = len(self.store.retrieve('execution_fault'))
        restored = self.controller(backend).run()
        self.assertEqual(restored['status'], 'completed')
        self.assertEqual(restored['execution_faults'], [])
        self.assertEqual(len(self.store.retrieve('execution_fault')), fault_count)

    def test_unknown_receipt_is_not_fabricated_as_finished_error_result(self):
        backend = Backend()
        with patch.object(self.adapter, 'run', return_value={'execution_status': 'unknown', 'stop_reason': 'No reliable receipt'}):
            with self.assertRaises(NeedsAttention):
                self.controller(backend).run()
        view = state_view(self.store)
        self.assertEqual(view['status'], 'needs_attention')
        self.assertTrue(view['execution_faults'])
        self.assertEqual(self.store.retrieve('result'), [])

    def test_detaching_waiter_does_not_create_false_solver_failure(self):
        backend = Backend()
        with patch.object(self.adapter, 'run', side_effect=InterruptedError('Synthetic user detach')):
            with self.assertRaises(InterruptedError):
                self.controller(backend).run()
        self.assertEqual(state_view(self.store)['execution_faults'], [])
        self.assertEqual(self.store.retrieve('execution_fault'), [])

    def test_recovery_does_not_overwrite_running_attempt_with_previous_failure(self):
        backend = Backend()
        self.controller(backend).run()
        task = self.store.get_task('T0001')
        task.update(active_attempt='A0002', state='running')
        self.store.save_task(task)
        self.controller(backend).tasks.recover_events()
        self.assertEqual(self.store.get_task('T0001')['state'], 'running')

    def test_explicit_resume_clears_current_failure_but_preserves_old_result(self):
        controller = self.controller(Backend())
        controller._initialize_proof()
        controller._plan()
        controller._prepare()
        task = self.store.get_task('T0001')
        result = self.store.write_record('result', {'task_id': 'T0001', 'attempt_id': 'A0001',
            'accepted': False, 'execution_status': 'incomplete', 'artifacts': [],
            'failure': {'kind': 'mathematical_error', 'message': 'Synthetic previous error'}})
        task.update(state='failed', finished_attempt='A0001', latest_result_ref=result,
                    result_refs=[result])
        self.store.save_task(task)
        controller.tasks.publish_task_outcome('T0001', result)
        self.assertEqual(self.store.get_task('T0001')['outcome_attempt_id'], 'A0001')
        data = self.store.get_meta('round_data')
        data['prepare_jobs'] = [{**data['jobs'][0], 'resume': True, 'attempt_id': 'A0002', 'attempt_no': 2}]
        data['jobs'] = data['prepare_jobs']
        self.store.set_meta(round_data=data)
        controller._prepare()
        controller.tasks.recover_events()
        current = self.store.get_task('T0001')
        self.assertEqual(current['active_attempt'], 'A0002')
        self.assertEqual(current['state'], 'prepared')
        for field in ('execution_status', 'accepted', 'review_status', 'result_summary', 'failure', 'outcome_attempt_id'):
            self.assertIsNone(current[field], field)
        self.assertEqual(current['latest_result_ref'], result)
        self.assertEqual(self.store.read_record(result)['failure']['kind'], 'mathematical_error')
