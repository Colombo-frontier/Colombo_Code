"""Current Controller recovery and isolation; all decisions are synthetic fixtures."""
import copy
import io
import threading
import time
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from colombo.brain.submission_validation import ContractError, validate_semantics
from colombo.brain.controller import NeedsAttention
from colombo.brain.research_store import Store
from controller_fixtures import AsyncCellFixture, FakeCell, OracleTestFixture, event_task
from prune_fixtures import bind_prunes
from test_oracle_workflow import Backend, SETTING


class RecoveryTests(OracleTestFixture, unittest.TestCase):
    def test_changed_prune_target_cannot_receive_a_stop_request(self):
        controller = self.controller(Backend())
        controller._initialize_proof()
        controller._plan()
        controller._prepare()
        task = self.store.get_task("T0001")
        command = {"id": "stop-fixture", "state": "pending", "task_id": "T0001",
                   "attempt_id": "A0001", "assignment_ref": task["assignment_ref"],
                   "decision_ref": {"id": "must-not-be-read"}}
        self.store.set_meta(prune_commands=[command])
        for change in ({"active_attempt": "A0002"}, {"assignment_ref": {"id": "different-assignment"}}):
            with self.subTest(change=change), \
                    patch.object(controller.store, "get_task", return_value={**task, **change}), \
                    patch.object(self.adapter, "request_stop", create=True) as stop:
                with self.assertRaisesRegex(NeedsAttention, "Pruning target changed"):
                    controller.tasks.apply_stops()
                stop.assert_not_called()
        self.assertEqual(self.store.get_meta("prune_commands"), [command])

    def test_unconfirmed_stop_blocks_supplement_next_wave_and_integration(self):
        controller = self.controller(Backend())
        controller._initialize_proof()
        controller._plan()
        controller._prepare()
        self.store.set_meta(prune_commands=[{"id": "stop-fixture", "state": "requested"}])
        controller.tasks._futures = {}
        controller.config["limits"]["max_rounds"] = 2
        # Each case would advance without the stop coordination gate: optional
        # supplementation, final integration, or an otherwise finished Wave.
        for dispatch, flags in ((2, {"supplement_requested": True, "integration_requested": False}),
                                (1, {"supplement_requested": False, "integration_requested": True}),
                                (1, {"supplement_requested": False, "integration_requested": False})):
            with self.subTest(flags=flags):
                controller.config["limits"]["max_dispatches_per_wave"] = dispatch
                self.store.set_meta(**flags)
                with patch.object(controller.tasks, "poll_workers"), \
                        patch.object(controller.tasks, "apply_stops"), \
                        patch.object(controller, "_pending_results", return_value=[]), \
                        patch.object(controller.tasks, "terminal", return_value=True), \
                        patch.object(controller.tasks, "start_available") as existing_queue, \
                        patch.object(controller, "_transition") as transition, \
                        patch.object(controller, "_begin_integrate") as integrate:
                    controller._tick()
                existing_queue.assert_called_once()
                transition.assert_not_called()
                integrate.assert_not_called()
                self.assertEqual(self.store.get_meta("phase"), "running")

    def test_durable_prune_stop_recovery_does_not_duplicate_execution(self):
        class PruningBackend(Backend):
            def invoke(inner, role, stage, root, call_id, prompt, context):
                value = super().invoke(role, stage, root, call_id, prompt, context)
                store = Store(root)
                if stage == "plan":
                    value["tasks"].append(event_task("B"))
                if stage == "process_results" and not store.get_meta("processed_results", []):
                    source = context["result_refs"][0]["id"]
                    proposal = {"task_id": "T0002", "attempt_id": "A0001", "reason": "subsumed",
                        "evidence_refs": [source], "relation_explanation": "fixture implication",
                        "scope_check": "fixture scopes", "covered_deliverables": ["A complete synthetic proof"],
                        "premises": [{"result_ref": source, "statement": "fixture upper_bound",
                                      "assumptions": [], "scope": "R1"}]}
                    value["prunes"] = bind_prunes(store, context, [proposal])
                return value

        config = self.store.get_meta("config")
        config["limits"]["max_dispatches_per_wave"] = 2
        self.store.set_meta(config=config)
        self.adapter = AsyncCellFixture()
        self.adapter.first_stop_crash = True
        backend = PruningBackend()
        with self.assertRaisesRegex(RuntimeError, "durable stop request"):
            self.controller(backend).run()
        self.assertEqual(len(self.store.get_meta("result_reviews")), 1)
        self.assertTrue(self.adapter.effective_stops)
        self.assertEqual(self.controller(backend).run()["status"], "completed")
        self.assertEqual(len(self.adapter.launches), 2)
        self.assertEqual(len(self.adapter.effective_stops), 1)
        self.assertTrue(all(c["state"] == "confirmed" for c in self.store.get_meta("prune_commands")))
        before = (list(backend.calls), list(self.adapter.launches))
        self.controller(backend).run()
        self.assertEqual(before, (backend.calls, self.adapter.launches))

    def test_result_commit_recovery_does_not_repeat_cell_execution(self):
        backend = Backend()
        controller = self.controller(backend)
        original = controller.store.save_task
        fail = [True]

        def interrupted(task):
            if task.get("state") == "returned" and fail[0]:
                fail[0] = False
                raise RuntimeError("Interrupted after durable Result")
            return original(task)

        with patch.object(controller.store, "save_task", side_effect=interrupted):
            with self.assertRaisesRegex(RuntimeError, "durable Result"):
                controller.run()
        self.assertEqual(self.store.reference_count("result"), 1)
        self.assertEqual(self.adapter.launches, 1)
        self.assertEqual(self.controller(backend).run()["status"], "completed")
        self.assertEqual(self.adapter.launches, 1)
        self.assertEqual(self.store.reference_count("result"), 1)
        self.assertEqual(len(self.store.get_meta("result_events")), 1)
        recovered = [e for e in self.store.events() if e["name"] == "cell_return_recovered"]
        self.assertEqual(len(recovered), 1)
        self.controller(backend).run()
        self.assertEqual([e for e in self.store.events() if e["name"] == "cell_return_recovered"], recovered)

    def test_durable_result_recovery_rejects_mismatched_attempt_and_fixed_inputs(self):
        controller = self.controller(Backend())
        controller._initialize_proof()
        controller._plan()
        controller._prepare()
        task = self.store.get_task("T0001")
        payload = {"task_id": "T0001", "attempt_id": "A0001", "execution_status": "finished",
                   "accepted": False, "artifacts": [], "assignment_ref": task["assignment_ref"],
                   "package_ref": task["package_ref"]}
        ref = self.store.write_record("result", payload, request_id="result:T0001:A0001")
        for key, wrong in (("task_id", "T0002"), ("attempt_id", "A0002"),
                           ("assignment_ref", {"id": "other"}), ("package_ref", {"id": "other"})):
            with self.subTest(field=key), \
                    patch.object(controller.tasks, "validate_artifacts", return_value={**payload, key: wrong}), \
                    patch.object(self.adapter, "run") as launch:
                with self.assertRaisesRegex(NeedsAttention, "Committed Result does not match"):
                    controller.tasks.recover_events()
                launch.assert_not_called()
                self.assertEqual(self.store.get_task("T0001"), task)
                self.assertEqual(self.store.get_meta("result_events"), [])
        self.assertEqual(self.store.request_record("result:T0001:A0001"), ref)

    def test_completed_replay_rebuilds_proof_without_new_model_or_cell(self):
        backend = Backend()
        self.controller(backend).run()
        before = (list(backend.calls), self.adapter.launches)
        (self.root / "proof/current.md").write_text("edited export", encoding="utf-8")
        self.controller(backend).run()
        self.assertEqual(before, (backend.calls, self.adapter.launches))
        self.assertIn("Full fixture Proof.", (self.root / "proof/current.md").read_text(encoding="utf-8"))

    def test_update_commit_recovery_reuses_verified_result_and_submission(self):
        backend = Backend()
        controller = self.controller(backend)
        original = controller._transition
        fail = [True]

        def interrupted(phase, **values):
            if values.get("processed_results") and fail[0]:
                fail[0] = False
                raise RuntimeError("Interrupted before update adoption")
            return original(phase, **values)

        with patch.object(controller, "_transition", side_effect=interrupted):
            with self.assertRaisesRegex(RuntimeError, "update adoption"):
                controller.run()
        self.assertIsNone(self.store.get_meta("progress_ref"))
        self.assertEqual(len(self.store.get_meta("result_reviews")), 1)
        self.assertEqual(self.controller(backend).run()["status"], "completed")
        self.assertEqual(backend.calls.count("process_results"), 1)
        self.assertEqual(backend.calls.count("verify-progress"), 2)  # Result, then Proof.
        self.assertEqual(self.adapter.launches, 1)

    def test_interruption_detaches_other_waiters_promptly(self):
        started, released = threading.Event(), threading.Event()

        class InterruptedCell(FakeCell):
            def run(inner, task_dir, attempt_id, resume=False, cancel_event=None):
                if task_dir.name == "T0001":
                    if not started.wait(2):
                        raise AssertionError("Second worker never started")
                    raise KeyboardInterrupt()
                started.set()
                if cancel_event.wait(3):
                    released.set()
                    raise InterruptedError("Controller stopped waiting")
                raise AssertionError("Controller failed to cancel wait")

        class ParallelBackend(Backend):
            def invoke(inner, role, stage, root, call_id, prompt, context):
                value = super().invoke(role, stage, root, call_id, prompt, context)
                if stage == "plan":
                    value["tasks"].append(event_task("B"))
                return value

        config = self.store.get_meta("config")
        config["limits"]["max_dispatches_per_wave"] = 2
        self.store.set_meta(config=config)
        self.adapter = InterruptedCell()
        began = time.monotonic()
        with self.assertRaises(KeyboardInterrupt):
            self.controller(ParallelBackend()).run()
        self.assertTrue(released.is_set())
        self.assertLess(time.monotonic() - began, 2)
        self.assertEqual(self.store.get_meta("status"), "needs_attention")
        self.assertEqual(self.store.retrieve("result"), [])
        self.assertEqual(self.store.retrieve("execution_fault"), [])

    def test_plan_rejects_unknown_responsibility_before_write(self):
        spec = event_task("A")
        spec["responsibility"]["goal_ids"] = ["unknown-goal"]
        payload = {"rationale": "fixture", "tasks": [spec], "setting_specification": SETTING}
        with self.assertRaisesRegex(ContractError, "Unknown Goal responsibility"):
            validate_semantics("plan", payload, self.store, {})
        self.assertEqual(self.store.retrieve("plan"), [])

    def test_status_does_not_create_a_database_in_non_run_directory(self):
        from colombo.system_commands import main
        empty = Path(self.temp.name) / "not-a-run"
        empty.mkdir()
        with redirect_stderr(io.StringIO()):
            code = main(["status", "--run-dir", str(empty)])
        self.assertEqual(code, 2)
        self.assertEqual(list(empty.iterdir()), [])

    def test_result_review_receives_fixed_inputs_and_required_package_sources(self):
        backend = Backend()
        controller = self.controller(backend)
        controller._initialize_proof()
        controller._plan()
        controller._prepare()
        job = controller.tasks.jobs()[0]
        ref = controller.tasks.run_job(job)
        package = controller._review_package(result_ref=ref)
        result = self.store.read_record(ref)
        required = set(package["required_checked_refs"])
        self.assertIn(ref["id"], required)
        self.assertIn(self.store.get_meta("setting_ref")["id"], required)
        for field in ("assignment_ref", "package_ref"):
            self.assertIn(result[field]["id"], required)
        artifact = self.root / result["artifacts"][0]["path"]
        artifact.unlink()
        with self.assertRaisesRegex(ValueError, "Missing or invalid frozen artifact"):
            controller._review_package(result_ref=ref)
