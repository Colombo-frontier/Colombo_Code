"""Integration of inherited deadlines with model-backed tools, without model calls."""
from contextlib import ExitStack
from copy import deepcopy
import json
import math
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

import colombo.shared.runtime_budget as budget
import colombo.cell.recovery as handoff
import colombo.cell.settings as settings
import colombo.cell.controller as run
from colombo.cell.recovery import caller_deadline
import colombo.cell.verifier.challenge as challenge
import colombo.shared.experiment_execution as experiment
import colombo.cell.settings as configure


class SharedBudgetRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(os.environ))
        for key in ('CELL_PROCESS_ID', 'COLOMBO_BUDGET_FILE', 'CELL_RUN_DIR'):
            os.environ.pop(key, None)
        self.tmp = self.stack.enter_context(tempfile.TemporaryDirectory())
        self.root = Path(self.tmp)
        self.policy = settings.load_policy(profile='standard')
        # Explicit historical policy fixture; current Colombo never inherits a cap.
        self.policy['workflow'] = {'version': 2}
        self.policy.pop('integration', None)
        self.policy['budget'] = {'research': {'total_active_seconds': 3600}}
        self.selected = self.policy['cell']['settings']

    def start(self, seconds):
        self.policy['budget']['research']['total_active_seconds'] = seconds
        return budget.start_budget(self.root, self.policy)

    def test_children_share_one_closing_and_recovery_partition(self):
        shared = self.start(1000)
        start = shared['active_started_at']
        parent = handoff.begin_process(self.root, 'a'*32, 'prover', 1000, self.selected,
                                      started_at=start, started_monotonic=0, shared_budget=shared)
        child = handoff.begin_process(self.root/'child', 'b'*32, 'subcell', 800, self.selected,
                                     started_at=start+200, started_monotonic=200, shared_budget=shared)
        self.assertEqual(parent['soft_deadline'], child['soft_deadline'])
        self.assertEqual(parent['hard_deadline'], child['hard_deadline'])
        self.assertEqual(parent['total_deadline'], child['total_deadline'])
        self.assertEqual(child['work_seconds'], parent['work_seconds']-200)

    def test_tool_windows_inherit_the_same_finite_root(self):
        context = self.start(1000)
        local = challenge._deadline(self.root, self.selected)
        self.assertIsNotNone(local)
        self.assertLessEqual(local-time.monotonic(), 850)
        self.assertLessEqual(experiment._window(self.selected['experiment'], caller_deadline(self.root)), 850)
        self.assertGreater(experiment._window(self.selected['experiment'], caller_deadline(self.root)), 800)

    def test_unlimited_is_none_in_persisted_state_not_infinity(self):
        self.start('unlimited')
        self.assertIsNone(challenge._deadline(self.root, self.selected))
        self.assertTrue(math.isinf(experiment._window(self.selected['experiment'], caller_deadline(self.root))))
        state = budget.get_budget_context(self.root)
        self.assertIsNone(state['deadline_unix'])
        json.dumps(state, allow_nan=False)

    def test_paused_budget_refuses_child_work(self):
        self.start(1000)
        budget.pause_budget(self.root)
        with self.assertRaises(budget.BudgetExhausted):
            caller_deadline(self.root)

    def test_configure_rejects_budget_before_creating_task_files(self):
        with self.assertRaisesRegex(ValueError, 'outer config.toml'):
            configure.configure(self.root, 'prover', {'agents': {'prover_timeout_seconds': 9999}},
                                reason='Must not expand the policy')
        self.assertEqual(list(self.root.iterdir()), [])

    def test_unlimited_experiment_still_has_finite_network_timeouts(self):
        client = experiment._Client('test-fixture-key', self.selected, None)
        self.addCleanup(client.close)
        with patch.object(client.session, 'request') as request:
            request.return_value.status_code = 200
            client._request('GET', '/responses/test')
            self.assertEqual(request.call_args.kwargs['timeout'],
                (self.selected['network']['connect_timeout_seconds'], self.selected['network']['read_timeout_seconds']))

    def saved_run(self):
        self.start(1000)
        (self.root/'run.json').write_text(json.dumps({'settings': self.selected, 'role': 'prover'}))
        (self.root/'runtime/prover_state.json').write_text(json.dumps({'launches': 3}))
        return {name: (self.root/name).read_bytes() for name in
                ('run.json', 'runtime/budget.json', 'runtime/prover_state.json')}

    def assert_policy_adoption_deferred(self, before):
        changed = deepcopy(self.policy)
        changed['budget']['research']['total_active_seconds'] = 'unlimited'
        changed['policy_metadata']['revision'] = 'updated-test-policy'
        with patch.object(settings, 'load_policy', return_value=changed), \
                patch.object(run, '_solve_locked') as launch:
            self.assertEqual(run.solve(self.root), 2)
        launch.assert_not_called()
        for name, data in before.items():
            self.assertEqual((self.root/name).read_bytes(), data)
        events = [json.loads(line) for line in (self.root/'run_events.jsonl').read_text().splitlines()]
        self.assertEqual(events[-1]['action'], 'policy_adoption_deferred')

    def test_changed_policy_waits_for_active_child_without_changing_counters(self):
        before = self.saved_run()
        child = self.root/'tasks'/('a'*32)
        child.mkdir(parents=True)
        (child/'task.json').write_text(json.dumps({'status': 'running'}))
        self.assert_policy_adoption_deferred(before)

    def test_changed_policy_waits_for_live_tool_job_without_changing_ledger(self):
        before = self.saved_run()
        with patch('colombo.shared.tool_jobs.pending_jobs', return_value=[{'job_id': 'job-live', 'status': 'running'}]):
            self.assert_policy_adoption_deferred(before)

    def test_same_policy_resume_keeps_existing_job_deadlines(self):
        before = self.saved_run()
        prior = json.loads(before['runtime/budget.json'])
        with patch.object(settings, 'load_policy', return_value=self.policy), \
                patch('colombo.shared.tool_jobs.pending_jobs', return_value=[{'job_id': 'job-live', 'status': 'running'}]), \
                patch.object(run, '_solve_locked', return_value=2) as launch:
            self.assertEqual(run.solve(self.root), 2)
        launch.assert_called_once()
        after = budget.get_budget_context(self.root)
        self.assertEqual(after['status'], 'active')
        for key in ('deadline_unix', 'work_deadline_unix', 'hard_deadline_unix', 'policy_revision'):
            self.assertEqual(after[key], prior[key])
        self.assertEqual((self.root/'runtime/prover_state.json').read_bytes(), before['runtime/prover_state.json'])

    def test_changed_policy_is_adopted_after_jobs_finish_without_resetting_usage(self):
        before = self.saved_run()
        budget.pause_budget(self.root)
        changed = deepcopy(self.policy)
        changed['budget']['research']['total_active_seconds'] = 'unlimited'
        changed['policy_metadata']['revision'] = 'updated-test-policy'
        with patch.object(settings, 'load_policy', return_value=changed), \
                patch.object(run, '_solve_locked', return_value=2):
            self.assertEqual(run.solve(self.root), 2)
        after = budget.get_budget_context(self.root)
        self.assertEqual(after['policy_revision'], 'updated-test-policy')
        self.assertEqual(after['configured_seconds'], 'unlimited')
        self.assertGreaterEqual(after['used_seconds'], json.loads(before['runtime/budget.json'])['used_seconds'])
        self.assertEqual((self.root/'runtime/prover_state.json').read_bytes(), before['runtime/prover_state.json'])


if __name__ == '__main__':
    unittest.main()
