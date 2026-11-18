"""Restart dispatch preserves Task identity, receipts, and Wave accounting."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from brain_fixtures import freeze_setting
from controller_fixtures import OracleTestFixture, event_task
from colombo.brain.cell_dispatch import CellAdapter
from colombo.brain.research_records import state_view
from colombo.brain.research_store import Store
from colombo.brain.submission_validation import ContractError, validate_semantics
from colombo.brain.task_execution import TaskExecution
from colombo.shared.file_io import read_json, write_json


class RestartPlanTests(OracleTestFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        config = self.store.get_meta("config")
        config["limits"].update(max_rounds=3, max_dispatches_per_wave=6)
        self.store.set_meta(config=config, dispatch_count=1, planning_wave=1)
        freeze_setting(self.store)
        self.original = event_task("Fixed target")
        self.initial_plan = self.store.write_record("plan", {
            "rationale": "Initial fixed Task", "tasks": [self.original]}, "initial-plan")
        job = self.store.plan_jobs(self.initial_plan)[0]
        self.tid = job["task_id"]
        node = self.store.read_document("research")["tasks"][self.tid]
        self.assignment_ref = node["assignment_ref"]
        self.package_ref = self.store.write_record("context_package", {
            "task_id": self.tid, "selection": self.original["package"], "artifacts": []})
        self.task = {"task_id": self.tid, "assignment_ref": self.assignment_ref,
                     "package_ref": self.package_ref, "state": "returned", "attempt_no": 1,
                     "active_attempt": "A0001", "finished_attempt": "A0001", "result_refs": []}
        self.install_result(used=15)

    def install_result(self, *, used, diagnostics=True):
        if self.task.get("latest_result_ref"):
            number = self.task["attempt_no"] + 1
            self.task.update(attempt_no=number, active_attempt=f"A{number:04d}",
                             finished_attempt=f"A{number:04d}")
        result = {"task_id": self.tid, "attempt_id": self.task["active_attempt"], "assignment_ref": self.assignment_ref,
                  "package_ref": self.package_ref, "execution_status": "incomplete",
                  "accepted": False, "artifacts": []}
        if diagnostics:
            result.update(stop_info={"stage": "prover"}, budget_snapshot={
                "prover": {"used": used, "limit": 15, "remaining": max(0, 15-used)},
                "current_review": {"state": "none"}, "submission_review": {"state": "none"},
                "diagnostic_errors": []})
        ref = self.store.write_record("result", result)
        self.task.update(latest_result_ref=ref, result_refs=[ref])
        self.store.save_task(self.task)
        return ref

    def proposal(self, mode="restart"):
        spec = {**copy.deepcopy(self.original), "mode": mode, "resume_task_id": self.tid}
        return {"rationale": "Continue the same fixed target", "tasks": [spec]}

    def validate(self, proposal):
        return validate_semantics("plan", proposal, self.store, {"dispatch_remaining": 5})

    def test_restart_reuses_assignment_and_package_and_replays_once(self):
        proposal = self.proposal()
        self.validate(proposal)
        old_assignment = self.store.read_record(self.assignment_ref)
        old_package = self.store.read_record(self.package_ref)
        ref = self.store.write_record("plan", proposal, "restart-plan")
        jobs = self.store.plan_jobs(ref)
        self.assertEqual(len(jobs), 1)
        self.assertEqual((jobs[0]["task_id"], jobs[0]["attempt_id"]), (self.tid, "A0002"))
        self.assertTrue(jobs[0]["resume"])
        self.assertIs(jobs[0]["restart"], True)
        self.store.set_meta(round_data={"round_no": 1, "plan_ref": ref, "jobs": jobs, "result_refs": []})
        reopened = Store(self.store.root)
        self.assertEqual(reopened.read_record(ref), proposal)
        self.assertEqual(reopened.plan_jobs(ref), jobs)
        self.assertEqual(reopened.get_meta("round_data")["jobs"][0]["spec"]["mode"], "restart")
        self.assertEqual(reopened.write_record("plan", proposal, "restart-plan"), ref)
        wave = reopened.read_document("research")["waves"]["W0001"]
        self.assertEqual(wave["dispatch_used"], 2)
        self.assertEqual(len(wave["members"]), 2)
        self.assertEqual(reopened.read_record(self.assignment_ref), old_assignment)
        self.assertEqual(reopened.read_record(self.package_ref), old_package)
        self.assertEqual(reopened.get_task(self.tid)["assignment_ref"], self.assignment_ref)
        self.assertEqual(reopened.get_task(self.tid)["package_ref"], self.package_ref)

    def test_legacy_new_and_resume_keep_their_original_json_shapes(self):
        self.install_result(used=14)
        proposal = self.proposal("resume")
        self.validate(proposal)
        ref = self.store.write_record("plan", proposal, "legacy-resume")
        reopened = Store(self.store.root)
        for plan in (self.initial_plan, ref):
            job = reopened.plan_jobs(plan)[0]
            self.assertNotIn("restart", job)
        self.assertEqual(reopened.read_record(ref), proposal)
        self.assertEqual(reopened.read_record(self.initial_plan)["tasks"], [self.original])
        self.assertEqual(reopened.write_record("plan", proposal, "legacy-resume"), ref)

    def test_exhausted_resume_rejected_before_new_dispatch_or_attempt(self):
        before = self.store.read_document("research")
        counter = self.store.get_meta("dispatch_count")
        with self.assertRaises(ContractError):
            self.validate(self.proposal("resume"))
        self.assertEqual(self.store.read_document("research"), before)
        self.assertEqual(self.store.get_meta("dispatch_count"), counter)
        self.validate(self.proposal("restart"))

    def test_brain_view_explains_exhaustion_and_explicit_restart_option(self):
        view = state_view(self.store)
        task = next(task for task in view["tasks"] if task["task_id"] == self.tid)
        eligibility = task["resume_eligibility"]
        self.assertEqual(eligibility["status"], "blocked")
        self.assertEqual(eligibility["stage"], "prover")
        self.assertEqual(eligibility["suggested_mode"], "restart")
        self.assertEqual(eligibility["restart_status"], "allowed")
        self.assertEqual(eligibility["budget"]["remaining"], 0)

    def test_missing_diagnostics_do_not_authorize_resume_or_restart(self):
        self.install_result(used=15, diagnostics=False)
        for mode in ("resume", "restart"):
            with self.subTest(mode=mode), self.assertRaises(ContractError):
                self.validate(self.proposal(mode))

    def test_restart_cannot_change_fixed_target_or_package(self):
        for field, replacement in (("instructions", "A different target"),
                                   ("package", {**self.original["package"], "background": "Changed input"})):
            proposal = self.proposal()
            proposal["tasks"][0][field] = replacement
            with self.subTest(field=field), self.assertRaisesRegex(ContractError, "fixed Task or package"):
                self.validate(proposal)

    def test_restart_requires_reconciled_task_and_cannot_repeat_same_task(self):
        for status in ("running", "stopping", "unknown", "needs_attention", "prepared"):
            self.task["state"] = status
            self.store.save_task(self.task)
            with self.subTest(status=status), self.assertRaisesRegex(ContractError, "reconciled Task"):
                self.validate(self.proposal())
        self.task["state"] = "returned"
        self.store.save_task(self.task)
        proposal = self.proposal()
        proposal["tasks"] *= 2
        with self.assertRaisesRegex(ContractError, "reconciled Task"):
            self.validate(proposal)

    def test_task_execution_forwards_restart_only_when_requested(self):
        class ReturnedCell:
            def __init__(self):
                self.options = []

            def run(self, task_dir, attempt_id, **options):
                self.options.append(options)
                return {"attempt_id": attempt_id, "execution_status": "incomplete", "artifacts": []}

        adapter = ReturnedCell()
        execution = TaskExecution(self.store, adapter, self.store.get_meta("config"), lambda *a, **kw: None)
        ref = execution._execute_job({"task_id": self.tid, "attempt_id": "A0002",
                                      "resume": True, "restart": True})
        self.assertIs(adapter.options[0]["restart"], True)
        self.assertTrue(adapter.options[0]["resume"])
        self.assertEqual(execution._execute_job({"task_id": self.tid, "attempt_id": "A0002",
                                                "resume": True, "restart": True}), ref)
        self.assertEqual(len(adapter.options), 1)
        execution._execute_job({"task_id": self.tid, "attempt_id": "A0003", "resume": True})
        self.assertNotIn("restart", adapter.options[1])


class RestartRequestTests(unittest.TestCase):
    def setUp(self):
        parent = PROJECT / "validation/tmp"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="restart-request-", dir=parent)
        self.task = Path(self.temp.name) / "T0001"
        self.folder = self.task / "attempts/A0002"
        self.folder.mkdir(parents=True)
        self.scope = {"task_id": "T0001", "attempt_id": "A0002",
                      "assignment_ref": {"id": "assignment-1", "revision": 1},
                      "package_ref": {"id": "package-1", "revision": 1}}
        self.adapter = CellAdapter(PROJECT, {"cell": {"run_timeout_seconds": 30}})
        write_json(self.task / "prepared.json", {"storage_version": 3, **self.scope})

    def tearDown(self):
        self.temp.cleanup()

    def freeze_request(self, *, restart=False, receipt=False):
        request = {"task_dir": str(self.task), "project_root": str(PROJECT), **self.scope,
                   "resume": True, "config": self.adapter.config}
        if restart:
            request["restart"] = True
        write_json(self.folder / "request.json", request)
        write_json(self.folder / "launch.json", {"nonce": "old", "identity": None,
                   "state": "launching", "created_at": time.time()-60})
        if receipt:
            result = {**self.scope, "execution_status": "incomplete", "artifacts": []}
            write_json(self.task / "results/A0002/result.json", result)
            write_json(self.folder / "receipt.json", {**self.scope, "result_path": "results/A0002/result.json"})
            return result

    def prior_result(self, *, used=15, receipt=True):
        folder = self.task / "attempts/A0001"
        scope = {**self.scope, "attempt_id": "A0001"}
        write_json(folder / "request.json", {"task_dir": str(self.task), **scope})
        write_json(folder / "launch.json", {"nonce": "prior", "identity": None,
                   "state": "started", "created_at": time.time()-60})
        result = {**scope, "execution_status": "incomplete", "accepted": False, "artifacts": [],
                  "stop_info": {"stage": "prover"}, "budget_snapshot": {
                      "prover": {"used": used, "limit": 15, "remaining": max(0, 15-used)},
                      "current_review": {"state": "none"}, "diagnostic_errors": []}}
        write_json(self.task / "results/A0001/result.json", result)
        if receipt:
            write_json(folder / "receipt.json", {**scope, "result_path": "results/A0001/result.json"})
        return result

    def test_committed_exhausted_resume_does_not_write_launch_intent_or_spawn(self):
        self.prior_result()
        with patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
            with self.assertRaisesRegex(ValueError, "Resume cannot start"):
                self.adapter.run(self.task, "A0002", resume=True)
            launch.assert_not_called()
        self.assertTrue((self.folder / "request.json").is_file())
        self.assertFalse((self.folder / "launch.json").exists())

    def test_queued_resume_respects_decreased_current_policy(self):
        self.prior_result(used=14)
        self.adapter.config["settings"] = {"agents": {"prover_max_rounds": 10}}
        with patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
            with self.assertRaisesRegex(ValueError, "Resume cannot start"):
                self.adapter.run(self.task, "A0002", resume=True)
            launch.assert_not_called()
        self.assertFalse((self.folder / "launch.json").exists())

    def test_queued_resume_can_use_increased_current_policy(self):
        self.prior_result()
        self.adapter.config["settings"] = {"agents": {"prover_max_rounds": 16}}
        expected = {**self.scope, "execution_status": "incomplete", "artifacts": []}

        class FinishedWorker:
            pid = 123456

            def poll(self):
                return 0

        def finish(*args, **kwargs):
            write_json(self.task / "results/A0002/result.json", expected)
            write_json(self.folder / "receipt.json", {**self.scope, "result_path": "results/A0002/result.json"})
            return FinishedWorker()

        with patch("colombo.brain.cell_dispatch.subprocess.Popen", side_effect=finish) as launch, \
             patch("colombo.brain.cell_dispatch.process_identity", return_value={"pid": 123456}):
            self.assertEqual(self.adapter.run(self.task, "A0002", resume=True), expected)
            launch.assert_called_once()
        self.assertTrue((self.folder / "launch.json").is_file())

    def test_unreconciled_prior_attempt_blocks_resume_before_launch_intent(self):
        self.prior_result(receipt=False)
        with patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
            with self.assertRaisesRegex(RuntimeError, "active or unresolved"):
                self.adapter.run(self.task, "A0002", resume=True)
            launch.assert_not_called()
        self.assertFalse((self.folder / "launch.json").exists())

    def test_restart_requires_resume_of_existing_task(self):
        with patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
            with self.assertRaisesRegex(ValueError, "existing Task"):
                self.adapter.run(self.task, "A0002", restart=True)
            launch.assert_not_called()
        self.assertFalse((self.folder / "request.json").exists())

    def test_same_attempt_cannot_switch_between_resume_and_restart(self):
        for original in (False, True):
            self.freeze_request(restart=original)
            with self.subTest(original=original), \
                 patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
                with self.assertRaises(ValueError):
                    self.adapter.run(self.task, "A0002", resume=True, restart=not original)
                launch.assert_not_called()

    def test_restart_receipt_rejoin_never_launches_again(self):
        expected = self.freeze_request(restart=True, receipt=True)
        with patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
            self.assertEqual(self.adapter.run(self.task, "A0002", resume=True, restart=True), expected)
            self.assertEqual(self.adapter.run(self.task, "A0002", resume=True, restart=True), expected)
            launch.assert_not_called()
        self.assertIs(read_json(self.folder / "request.json")["restart"], True)

    def test_legacy_resume_receipt_remains_unchanged(self):
        expected = self.freeze_request(receipt=True)
        before = (self.folder / "request.json").read_bytes()
        with patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
            self.assertEqual(self.adapter.run(self.task, "A0002", resume=True), expected)
            launch.assert_not_called()
        self.assertEqual((self.folder / "request.json").read_bytes(), before)
        self.assertNotIn("restart", read_json(self.folder / "request.json"))


if __name__ == "__main__":
    unittest.main()
