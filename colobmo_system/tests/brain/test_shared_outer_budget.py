"""Exercise actual outer launch boundaries without invoking a model."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.brain.model_calls import CodexBackend
from colombo.configuration import PROJECT_ROOT, load_config
from colombo.system_commands import adopt_current_policy
from colombo.brain.research_store import Store
from colombo.brain.controller import OracleController as Controller
from colombo.shared.runtime_budget import start_budget, pause_budget, get_budget_context
import test_backend as backend_fixture


class SharedOuterBudgetTests(unittest.TestCase):
    def fixture(self, seconds, runtime=None):
        f = backend_fixture.BackendTests()
        f.setUp()
        self.addCleanup(f.doCleanups)
        config = load_config()
        self.assertEqual(seconds, 'unlimited')
        config['runtime'].update(auth_home=str(f.auth), codex_bin=str(f.exe))
        config['cell']['settings']['runtime'].update(runtime or {})
        f.config = config
        f.store.set_meta(config=config)
        f.backend = CodexBackend(f.project, config)
        start_budget(f.run_root, config)
        return f

    def test_hard_global_verifier_has_no_hidden_process_timer(self):
        f = self.fixture('unlimited')
        def respond(proc, prompt, timeout):
            self.assertIsNone(timeout)
            f.write_submission(proc, {'verdict':'pass','summary':'Fixture',
                                      'findings':[], 'checked_refs':[]})
        with f.spawn(respond):
            f.backend.invoke('verifier', 'verify-progress', f.run_root, 'review', 'Review', {})
        manifest = json.loads((f.run_root/'brain/calls/review/call.json').read_text())
        self.assertIsNone(manifest['deadline_unix'])

    def test_finite_root_deadline_is_rejected_by_current_policy(self):
        f = self.fixture('unlimited')
        config = {**f.config, 'budget': {'research': {'total_active_seconds': 200}}}
        with self.assertRaisesRegex(ValueError, 'whole-run research deadline'):
            start_budget(f.run_root, config)
        self.assertIsNone(get_budget_context(f.run_root)['deadline_unix'])

    def test_paused_root_cannot_launch_new_work(self):
        f = self.fixture('unlimited')
        pause_budget(f.run_root)
        with f.spawn(lambda *_: self.fail('Must not start a model')) as launch:
            with self.assertRaisesRegex(TimeoutError, 'paused'):
                f.backend.invoke('brain','plan',f.run_root,'paused','Plan',{})
            launch.assert_not_called()

    def test_managed_outer_launch_and_cleanup_use_shared_runtime_settings(self):
        f = self.fixture('unlimited', {'terminate_wait_seconds':7, 'process_poll_seconds':0.13})
        def respond(proc, prompt, timeout):
            self.assertEqual(proc.kwargs['terminate_wait_seconds'], 7)
            f.write_submission(proc)
        with f.spawn(respond), patch('colombo.brain.model_calls.terminate_tree', return_value=True) as cleanup:
            f.backend.invoke('brain','plan',f.run_root,'configured','Plan',{})
        self.assertEqual(cleanup.call_args.kwargs, {'timeout':7, 'poll_seconds':0.13})
        controller = Controller(f.project, f.run_root, backend=object(), adapter=object())
        self.assertEqual(controller.process_poll_seconds, 0.13)

    def test_resume_adopts_selected_source_without_resetting_counts(self):
        with tempfile.TemporaryDirectory(dir=PROJECT_ROOT/'validation/tmp') as name:
            root = Path(name)
            source = root/'config.toml'
            original = (PROJECT_ROOT/'config.toml').read_text(encoding='utf-8-sig')
            source.write_text(original,encoding='utf-8')
            config = load_config(source)
            store = Store.create(root/'run','Goal',[],config)
            store.set_meta(model_call_count=7, dispatch_count=3, round_no=2, audit_call_count=1)
            start_budget(store.root,config)
            pause_budget(store.root)
            budget_path=store.root/'runtime/budget.json'
            recorded_budget=budget_path.read_bytes()
            source.write_text(original.replace('max_rounds = 8','max_rounds = 9',1),encoding='utf-8')
            adopt_current_policy(store)
            self.assertEqual(store.get_meta('config')['limits']['max_rounds'],9)
            self.assertEqual(store.get_meta('model_call_count'),7)
            self.assertEqual(store.get_meta('dispatch_count'),3)
            self.assertEqual(store.get_meta('round_no'),2)
            self.assertEqual(store.get_meta('audit_call_count'),1)
            self.assertEqual(budget_path.read_bytes(),recorded_budget)
            store.set_meta(pending_call={'call_id':'unresolved'})
            source.write_text(original,encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'pending model call'):
                adopt_current_policy(store)
            self.assertEqual(store.get_meta('config')['limits']['max_rounds'],9)

    def test_resume_blocks_running_tools_and_cells_before_policy_mutation(self):
        with tempfile.TemporaryDirectory(dir=PROJECT_ROOT/'validation/tmp') as name:
            root = Path(name)
            source = root/'config.toml'
            original = (PROJECT_ROOT/'config.toml').read_text(encoding='utf-8-sig')
            source.write_text(original, encoding='utf-8')
            saved = load_config(source)
            store = Store.create(root/'run', 'Goal', [], saved)
            source.write_text(original.replace('max_rounds = 8', 'max_rounds = 9', 1), encoding='utf-8')
            with patch('colombo.shared.tool_jobs.pending_jobs', return_value=[{'status': 'running'}]):
                with self.assertRaisesRegex(ValueError, 'Active tool jobs'):
                    adopt_current_policy(store)
            with patch.object(store, 'list_tasks', return_value=[{'state':'stopping'}]):
                with self.assertRaisesRegex(ValueError, 'Active Cell'):
                    adopt_current_policy(store)
            self.assertEqual(store.get_meta('config'), saved)

    def test_controller_keeps_shared_clock_active_for_unconfirmed_workers(self):
        f = self.fixture('unlimited')
        controller = Controller(f.project, f.run_root, backend=object(), adapter=object())
        with patch('colombo.shared.tool_jobs.pending_jobs', return_value=[{'status':'running'}]):
            controller._pause_budget()
        self.assertEqual(get_budget_context(f.run_root)['status'], 'active')
        with patch.object(controller.store, 'list_tasks', return_value=[{'state':'stopping'}]):
            controller._pause_budget()
        self.assertEqual(get_budget_context(f.run_root)['status'], 'active')
        path = f.run_root/'brain/calls/unconfirmed/call.json'
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({'status':'unknown', 'process_tree_terminated':False}), encoding='utf-8')
        controller.store.set_meta(pending_call={'call_id':'unconfirmed'})
        controller._pause_budget()
        self.assertEqual(get_budget_context(f.run_root)['status'], 'active')
        path.write_text(json.dumps({'status':'failed', 'process_tree_terminated':True}), encoding='utf-8')
        controller._pause_budget()
        self.assertEqual(get_budget_context(f.run_root)['status'], 'paused')


if __name__ == '__main__':
    unittest.main()
