from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from colombo.shared.runtime_budget import BudgetExhausted
from colombo.shared.runtime_budget import budget_environment
from colombo.shared.runtime_budget import get_budget_context
from colombo.shared.runtime_budget import inherited_deadline
from colombo.shared.runtime_budget import pause_budget
from colombo.shared.runtime_budget import start_budget
from colombo.cell.settings import load_policy


class SharedResearchBudgetTests(unittest.TestCase):
    def setUp(self):
        base=Path(__file__).resolve().parents[2]/'validation'/'tmp'
        base.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.env=patch.dict(os.environ)
        self.env.start();self.addCleanup(self.env.stop)
        os.environ.pop('COLOMBO_BUDGET_FILE',None)
        self.config=load_policy()
        # Exercise the retained historical ledger explicitly. Colombo policy itself
        # has no research time cap (covered by test_budget_policy).
        self.config['workflow']={'version':2}
        self.config.pop('integration',None)
        self.config['budget']={'research':{'total_active_seconds':'unlimited'}}
        self.config['cell']['settings']['handoff']['reserve_seconds']=0
        self.config['cell']['settings']['handoff']['recovery_seconds']=0

    def cap(self,value):
        config=copy.deepcopy(self.config)
        config['budget']['research']['total_active_seconds']=value
        config['policy_metadata']['revision']='test-'+str(value)
        return config

    def test_all_descendants_share_the_same_deadline_not_a_fresh_duration(self):
        with patch('colombo.shared.runtime_budget.time.time',return_value=1000):
            start_budget(self.root,self.cap(100))
        child=self.root/'tasks'/'T1'/'cell'/'audits'/'a'
        child.mkdir(parents=True)
        with patch('colombo.shared.runtime_budget.time.time',return_value=1080),patch('colombo.shared.runtime_budget.time.monotonic',return_value=50):
            self.assertEqual(get_budget_context(child)['total_remaining_seconds'],20)
            self.assertEqual(inherited_deadline(child),70)
            self.assertEqual(budget_environment(child)['COLOMBO_BUDGET_FILE'],str(self.root/'runtime'/'budget.json'))

    def test_unlimited_has_no_old_numeric_cutoff(self):
        with patch('colombo.shared.runtime_budget.time.time',return_value=1000):
            start_budget(self.root,self.cap('unlimited'))
        with patch('colombo.shared.runtime_budget.time.time',return_value=10000000):
            context=get_budget_context(self.root)
            self.assertIsNone(context['deadline_unix'])
            self.assertIsNone(inherited_deadline(self.root))
            self.assertFalse(context['closing'])
            self.assertGreater(context['elapsed_seconds'],3600)

    def test_resume_excludes_confirmed_pause_and_preserves_used_time(self):
        with patch('colombo.shared.runtime_budget.time.time',return_value=1000): start_budget(self.root,self.cap(100))
        with patch('colombo.shared.runtime_budget.time.time',return_value=1030): pause_budget(self.root)
        with patch('colombo.shared.runtime_budget.time.time',return_value=5000):
            paused=get_budget_context(self.root)
            self.assertEqual(paused['work_remaining_seconds'],70)
            self.assertFalse(paused['closing'])
            context=start_budget(self.root,self.cap(100))
            self.assertEqual(context['elapsed_seconds'],30)
            self.assertEqual(context['deadline_unix'],5070)
            self.assertEqual(context['total_remaining_seconds'],70)

    def test_lowering_cap_below_usage_does_not_reset_usage(self):
        with patch('colombo.shared.runtime_budget.time.time',return_value=1000): start_budget(self.root,self.cap(100))
        with patch('colombo.shared.runtime_budget.time.time',return_value=1030): pause_budget(self.root)
        with patch('colombo.shared.runtime_budget.time.time',return_value=5000):
            with self.assertRaises(BudgetExhausted): start_budget(self.root,self.cap(20))
            self.assertEqual(get_budget_context(self.root)['elapsed_seconds'],30)
            context=start_budget(self.root,self.cap('unlimited'))
            self.assertEqual(context['elapsed_seconds'],30)
            self.assertIsNone(context['deadline_unix'])

    def test_unclosed_crash_interval_is_charged_and_marked(self):
        with patch('colombo.shared.runtime_budget.time.time',return_value=1000): start_budget(self.root,self.cap(100))
        with patch('colombo.shared.runtime_budget.time.time',return_value=1030):
            context=start_budget(self.root,self.cap(100))
            self.assertEqual(context['total_remaining_seconds'],70)
            self.assertTrue(context['recovered_unclosed_interval'])

    def test_reserves_are_partitioned_once_and_visible_to_children(self):
        config=self.cap(300)
        config['cell']['settings']['handoff'].update(reserve_seconds=60,recovery_seconds=90)
        with patch('colombo.shared.runtime_budget.time.time',return_value=1000): start_budget(self.root,config)
        child=self.root/'a'/'b';child.mkdir(parents=True)
        with patch('colombo.shared.runtime_budget.time.time',return_value=1100):
            root=get_budget_context(self.root);nested=get_budget_context(child)
            self.assertEqual(root['work_deadline_unix'],1150)
            self.assertEqual(nested['work_deadline_unix'],1150)
            self.assertEqual(nested['hard_deadline_unix'],1210)
            self.assertEqual(nested['deadline_unix'],1300)

    def test_paused_or_expired_budget_refuses_new_work(self):
        with patch('colombo.shared.runtime_budget.time.time',return_value=1000): start_budget(self.root,self.cap(10))
        with patch('colombo.shared.runtime_budget.time.time',return_value=1011):
            with self.assertRaises(BudgetExhausted): inherited_deadline(self.root)

    def test_reattach_and_resume_do_not_restart_closing_window(self):
        config=self.cap(300)
        config['cell']['settings']['handoff'].update(reserve_seconds=60,recovery_seconds=90)
        with patch('colombo.shared.runtime_budget.time.time',return_value=1000): start_budget(self.root,config)
        with patch('colombo.shared.runtime_budget.time.time',return_value=1180):
            reattached=start_budget(self.root,config)
            self.assertEqual(reattached['work_deadline_unix'],1150)
            self.assertEqual(reattached['hard_deadline_unix'],1210)
            pause_budget(self.root)
        with patch('colombo.shared.runtime_budget.time.time',return_value=5000):
            resumed=start_budget(self.root,config)
            self.assertTrue(resumed['closing'])
            self.assertEqual(resumed['work_remaining_seconds'],0)
            self.assertEqual(resumed['hard_deadline_unix'],5030)
            self.assertEqual(resumed['deadline_unix'],5120)
            pause_budget(self.root)
            with self.assertRaises(BudgetExhausted): inherited_deadline(self.root)


class ToolJobTests(unittest.TestCase):
    def setUp(self):
        base=Path(__file__).resolve().parents[2]/'validation'/'tmp'
        base.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.config=load_policy()
        self.env=patch.dict(os.environ)
        self.env.start();self.addCleanup(self.env.stop)
        os.environ.pop('COLOMBO_BUDGET_FILE',None)
        (self.root/'run.json').write_text(json.dumps({'settings':self.config['cell']['settings']}),encoding='utf-8')
        start_budget(self.root,self.config)

    def test_real_worker_replays_same_job_without_relaunch(self):
        from colombo.shared.tool_jobs import submit_or_poll
        from colombo.shared.tool_jobs import poll_job
        first=submit_or_poll(self.root,'budget_status',{},request_id='read-one')
        files=list((self.root/'runtime'/'tool_jobs').glob('job-*/request.json'))
        self.assertEqual(len(files),1)
        job_id=files[0].parent.name
        end=time.monotonic()+10
        result=first
        while result.get('status')=='running' and time.monotonic()<end:
            time.sleep(0.025);result=poll_job(self.root,job_id)
        self.assertIn('budget',result)
        replay=submit_or_poll(self.root,'budget_status',{},request_id='read-one')
        self.assertEqual(replay,result)
        self.assertEqual(len(list((self.root/'runtime'/'tool_jobs').glob('job-*'))),1)
        with self.assertRaisesRegex(ValueError,'changed its inputs'):
            submit_or_poll(self.root,'budget_status',{'unexpected':1},request_id='read-one')

    def test_unknown_operation_and_path_escape_are_rejected(self):
        from colombo.shared.tool_jobs import submit_or_poll
        from colombo.shared.tool_jobs import poll_job
        with self.assertRaises(ValueError): submit_or_poll(self.root,'exec',{})
        with self.assertRaises(ValueError): poll_job(self.root,'../other')

    def test_expired_budget_does_not_launch_job(self):
        from colombo.shared.tool_jobs import submit_or_poll
        config=copy.deepcopy(self.config)
        config['workflow']={'version':2}
        config.pop('integration',None)
        config['budget']={'research':{'total_active_seconds':1}}
        with patch('colombo.shared.runtime_budget.time.time',return_value=time.time()-10): start_budget(self.root,config)
        with self.assertRaises(BudgetExhausted): submit_or_poll(self.root,'budget_status',{})
        self.assertEqual(len(list((self.root/'runtime'/'tool_jobs').glob('job-*/request.json'))),0)

    def test_crashed_launcher_returns_interrupted_without_replay(self):
        from colombo.shared.tool_jobs import poll_job
        from colombo.shared.tool_jobs import pending_jobs
        job_id='job-'+'a'*32
        folder=self.root/'runtime'/'tool_jobs'/job_id
        folder.mkdir(parents=True)
        (folder/'request.json').write_text(json.dumps({'owner':'standalone'}),encoding='utf-8')
        (folder/'state.json').write_text(json.dumps({'status':'starting','owner':'standalone',
            'identity':None,'launcher_identity':{'pid':123,'start_token':'dead'}}),encoding='utf-8')
        with patch('colombo.shared.tool_jobs._alive',return_value=False):
            self.assertEqual(poll_job(self.root,job_id)['status'],'interrupted')
            self.assertEqual(pending_jobs(self.root),[])
        with self.assertRaisesRegex(ValueError,'different invocation'):
            poll_job(self.root,job_id,owner='another-call')

    def test_late_worker_receipt_is_preserved_after_exit_observation(self):
        from colombo.shared.tool_jobs import poll_job
        for index, succeeded in enumerate((True, False)):
            with self.subTest(succeeded=succeeded):
                job_id='job-'+str(index+3)*32
                folder=self.root/'runtime'/'tool_jobs'/job_id
                folder.mkdir(parents=True)
                (folder/'request.json').write_text(json.dumps({'owner':'standalone'}),encoding='utf-8')
                (folder/'state.json').write_text(json.dumps({'status':'running','owner':'standalone',
                    'identity':{'pid':123,'start_token':'fixture-worker'}}),encoding='utf-8')
                saved=({'ok':True,'job_id':job_id,'result':{'budget':{'fixture':'completed'}}} if succeeded else
                       {'ok':False,'job_id':job_id,'status':'error','error':{'type':'ValueError','message':'Worker error'},
                        'retryable':False})
                encoded=json.dumps(saved)
                def complete_then_report_exited(identity):
                    # Deterministically publish between the first receipt read
                    # and the liveness result; no real process or sleep needed.
                    (folder/'result.json').write_text(encoded,encoding='utf-8')
                    return False
                expected=saved['result'] if succeeded else saved
                with patch('colombo.shared.tool_jobs._alive',side_effect=complete_then_report_exited) as alive, \
                        patch('colombo.shared.tool_jobs.subprocess.Popen') as launch:
                    self.assertEqual(poll_job(self.root,job_id),expected)
                    self.assertEqual((folder/'result.json').read_text(encoding='utf-8'),encoded)
                    self.assertEqual(poll_job(self.root,job_id),expected)
                    alive.assert_called_once()
                    launch.assert_not_called()

    def test_malformed_late_receipt_is_not_replaced_with_interruption(self):
        from colombo.shared.tool_jobs import poll_job
        for index, (encoded, error) in enumerate((('{broken', ValueError), ('[]', ValueError), ('{"ok":true}', KeyError))):
            with self.subTest(receipt=encoded):
                job_id='job-'+str(index+5)*32
                folder=self.root/'runtime'/'tool_jobs'/job_id
                folder.mkdir(parents=True)
                (folder/'request.json').write_text(json.dumps({'owner':'standalone'}),encoding='utf-8')
                (folder/'state.json').write_text(json.dumps({'status':'running','owner':'standalone',
                    'identity':{'pid':123,'start_token':'fixture-worker'}}),encoding='utf-8')
                def publish_invalid_then_report_exited(identity):
                    (folder/'result.json').write_text(encoded,encoding='utf-8')
                    return False
                with patch('colombo.shared.tool_jobs._alive',side_effect=publish_invalid_then_report_exited), \
                        self.assertRaises(error):
                    poll_job(self.root,job_id)
                self.assertEqual((folder/'result.json').read_text(encoding='utf-8'),encoded)

    def test_bootstrap_exit_without_identity_is_durably_interrupted(self):
        from colombo.shared.tool_jobs import poll_job
        from colombo.shared.tool_jobs import _PROCESS_HANDLES
        from unittest.mock import Mock
        job_id='job-'+'b'*32
        folder=self.root/'runtime'/'tool_jobs'/job_id
        folder.mkdir(parents=True)
        (folder/'request.json').write_text(json.dumps({'owner':'standalone'}),encoding='utf-8')
        (folder/'state.json').write_text(json.dumps({'status':'running','owner':'standalone',
            'identity':None,'launcher_identity':None}),encoding='utf-8')
        _PROCESS_HANDLES[job_id]=Mock(poll=Mock(return_value=1))
        self.addCleanup(_PROCESS_HANDLES.pop,job_id,None)
        first=poll_job(self.root,job_id)
        self.assertEqual(first['status'],'interrupted')
        self.assertNotIn(job_id,_PROCESS_HANDLES)
        self.assertEqual(poll_job(self.root,job_id),first)


if __name__=='__main__': unittest.main()
