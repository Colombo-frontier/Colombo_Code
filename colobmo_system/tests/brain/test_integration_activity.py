"""Integration clocks follow actual new researcher starts, not return counts."""
import copy
import json
import tempfile
import time
import unittest
import sys
from pathlib import Path
from unittest.mock import patch

from colombo.configuration import PROJECT_ROOT, load_config
from colombo.cell.worker import _research_activity
from colombo.brain.controller import OracleController
from colombo.brain.controller import NeedsAttention
from colombo.brain.research_store import Store
from controller_fixtures import FakeCell
from test_oracle_workflow import Backend


class IntegrationActivityTests(unittest.TestCase):
    def make(self, root):
        config = load_config()
        config["limits"].update(max_dispatches_per_wave=2, max_rounds=1)
        store = Store.create(Path(root) / "run", "fixture", [], config)
        return store, OracleController(PROJECT_ROOT, store.root, Backend(), FakeCell())

    def returned(self, store, attempt, *, status="error", started=False, process_ids=()):
        result = store.write_record("result", {"task_id": "T0001", "attempt_id": attempt,
            "execution_status": status, "started": started, "accepted": False, "artifacts": [],
            "research_activity": {"started": bool(process_ids), "process_ids": list(process_ids)}})
        store.set_meta(processed_results=[*store.get_meta("processed_results", []), result["id"]])
        return result

    def expired_pending(self, store, phase="integrating"):
        pending = {"call_id": "C00001", "role": "brain" if phase == "integrating" else "verifier",
                   "stage": "integrate" if phase == "integrating" else "verify-progress"}
        store.set_meta(phase=phase, integration={"started_at": 1, "deadline_unix": 2,
            "research_generation": 0, "revision": 1}, pending_call=pending)
        return pending

    def test_expired_recovery_preserves_running_or_unknown_model_call(self):
        for phase in ("integrating", "final_reviewing"):
            for state in ("running", "unknown"):
                with self.subTest(phase=phase, state=state), tempfile.TemporaryDirectory() as root:
                    store, controller = self.make(root)
                    pending = self.expired_pending(store, phase)
                    controller.calls.backend.reconcile_call = lambda *args: {"state": state}
                    with self.assertRaises(NeedsAttention):
                        controller.run()
                    self.assertEqual(store.get_meta("pending_call"), pending)
                    self.assertEqual(store.get_meta("phase"), phase)
                    self.assertEqual(store.get_meta("status"), "needs_attention")
                    self.assertIsNone(store.get_meta("conclusion_ref"))
                    self.assertEqual(controller.calls.backend.calls, [])

    def test_expired_recovery_requires_native_process_tree_exit_even_after_submission(self):
        with tempfile.TemporaryDirectory() as root:
            store, controller = self.make(root)
            pending = self.expired_pending(store)
            work = store.root / "brain/calls/C00001"
            work.mkdir(parents=True)
            (work / "call.json").write_text(json.dumps({"call_id": "C00001", "status": "submitted",
                "process_exit_confirmed": True, "process_tree_terminated": False}), encoding="utf-8")
            controller.calls.backend.reconcile_call = lambda *args: {"state": "submitted"}
            with self.assertRaises(NeedsAttention):
                controller.run()
            self.assertEqual(store.get_meta("pending_call"), pending)
            self.assertEqual(store.get_meta("status"), "needs_attention")
            self.assertIsNone(store.get_meta("conclusion_ref"))

    def test_expired_recovery_can_conclude_after_confirmed_native_exit(self):
        with tempfile.TemporaryDirectory() as root:
            store, controller = self.make(root)
            self.expired_pending(store)
            work = store.root / "brain/calls/C00001"
            work.mkdir(parents=True)
            (work / "call.json").write_text(json.dumps({"call_id": "C00001", "status": "timeout",
                "process_exit_confirmed": True, "process_tree_terminated": True}), encoding="utf-8")
            controller.calls.backend.reconcile_call = lambda *args: {"state": "failed"}
            self.assertEqual(controller.run()["status"], "partial")
            self.assertEqual(store.get_meta("phase"), "done")
            self.assertIsNone(store.get_meta("pending_call"))
            self.assertEqual(store.get_meta("stop_reason"), "integration_timeout")
            self.assertEqual(controller.calls.backend.calls, [])

    def test_current_call_timeout_with_confirmed_exit_still_concludes(self):
        class TimedOutBackend(Backend):
            def invoke(self, role, stage, root, cid, prompt, context):
                self.calls.append(stage)
                store = Store(root)
                integration = store.get_meta("integration")
                integration["deadline_unix"] = 1
                store.set_meta(integration=integration)
                work = store.root / "brain/calls" / cid
                work.mkdir(parents=True)
                (work / "call.json").write_text(json.dumps({"call_id": cid, "status": "timeout",
                    "process_exit_confirmed": True, "process_tree_terminated": True}), encoding="utf-8")
                raise RuntimeError("Simulated timed-out model, terminated by backend")
        with tempfile.TemporaryDirectory() as root:
            store, controller = self.make(root)
            controller.calls.backend = TimedOutBackend()
            store.set_meta(phase="integrating", integration={"started_at": time.time(),
                "deadline_unix": time.time() + 3600, "research_generation": 0, "revision": 0})
            self.assertEqual(controller.run()["status"], "partial")
            self.assertEqual(store.get_meta("phase"), "done")
            self.assertIsNone(store.get_meta("pending_call"))
            self.assertEqual(controller.calls.backend.calls, ["integrate"])

    def test_nonresearch_returns_and_replay_do_not_reset_stage(self):
        with tempfile.TemporaryDirectory() as root:
            store, controller = self.make(root)
            with patch("colombo.brain.controller.time.time", return_value=100):
                controller._begin_integrate("initial")
            initial = store.get_meta("integration")
            for attempt, status, started in (("A0001", "cancelled", False),
                    ("A0002", "error", False), ("A0003", "error", True), ("A0004", "finished", True)):
                self.returned(store, attempt, status=status, started=started)
                with patch("colombo.brain.controller.time.time", return_value=200):
                    controller._begin_integrate("returned without new research")
                self.assertEqual(store.get_meta("integration"), initial)

    def test_new_research_failure_can_reset_but_duplicate_process_cannot(self):
        with tempfile.TemporaryDirectory() as root:
            store, controller = self.make(root)
            with patch("colombo.brain.controller.time.time", return_value=100):
                controller._begin_integrate("initial")
            result = self.returned(store, "A0001", status="error", started=True, process_ids=["native-1"])
            with patch("colombo.brain.controller.time.time", return_value=200):
                controller._begin_integrate("new researcher failed after launch")
            stage = store.get_meta("integration")
            self.assertEqual(stage["deadline_unix"], 7400)
            self.assertEqual(stage["research_tokens"], ["T0001:native-1"])
            store.set_meta(processed_results=[result["id"], result["id"]])
            self.returned(store, "A0002", started=True, process_ids=["native-1"])
            with patch("colombo.brain.controller.time.time", return_value=300):
                controller._begin_integrate("duplicate receipt")
            self.assertEqual(store.get_meta("integration"), stage)
            self.returned(store, "A0003", started=True, process_ids=["native-2"])
            with patch("colombo.brain.controller.time.time", return_value=400):
                controller._begin_integrate("genuine second researcher")
            self.assertEqual(store.get_meta("integration")["deadline_unix"], 7600)

    def test_marker_format_adoption_does_not_reset_an_existing_clock(self):
        with tempfile.TemporaryDirectory() as root:
            store, controller = self.make(root)
            store.set_meta(integration={"started_at": 100, "deadline_unix": 7300,
                "research_generation": 1, "revision": 3})
            self.returned(store, "A0001", started=True, process_ids=["native-1"])
            with patch("colombo.brain.controller.time.time", return_value=200):
                controller._begin_integrate("resume existing stage")
            self.assertEqual(store.get_meta("integration")["deadline_unix"], 7300)
            self.assertEqual(store.get_meta("integration")["revision"], 3)

    def test_frozen_worker_baseline_excludes_noop_resume_and_review_only_work(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            attempt = root / "attempt"
            attempt.mkdir()
            snapshot = root / "snapshot"
            markers = snapshot / "runtime/research_starts"
            markers.mkdir(parents=True)
            (markers / "old.json").write_text(json.dumps({"process_id": "old", "role": "prover"}), encoding="utf-8")
            request = attempt / "request.json"
            # Missing baseline and worker launch alone cannot authorize a reset.
            self.assertFalse(_research_activity(request, snapshot)["started"])
            (attempt / "research_baseline.json").write_text(json.dumps({"process_ids": ["old"]}), encoding="utf-8")
            (snapshot / "runtime/prover_state.json").write_text('{"launches": 99}', encoding="utf-8")
            self.assertFalse(_research_activity(request, snapshot)["started"])
            (markers / "new.json").write_text(json.dumps({"process_id": "new", "role": "prover"}), encoding="utf-8")
            self.assertEqual(_research_activity(request, snapshot), {"started": True, "process_ids": ["new"]})
            self.assertEqual(_research_activity(request, snapshot)["process_ids"], ["new"])

    def test_resume_clears_current_outcome_and_keeps_previous_attempt(self):
        class ResumeBackend(Backend):
            def invoke(self, role, stage, root, cid, prompt, context):
                store = Store(root)
                if stage == "plan" and store.get_meta("setting_ref"):
                    spec = copy.deepcopy(store.read_record(store.get_task("T0001")["assignment_ref"])["spec"])
                    spec.update(mode="resume", resume_task_id="T0001")
                    return {"rationale": "Resume fixed Task", "tasks": [spec]}
                return super().invoke(role, stage, root, cid, prompt, context)
        with tempfile.TemporaryDirectory() as root:
            store, controller = self.make(root)
            controller.calls.backend = ResumeBackend()
            controller._initialize_proof()
            controller._plan()
            controller._prepare()
            controller.tasks.run_job(controller.tasks.jobs()[0])
            old = store.get_task("T0001")
            old.update(failure={"kind": "old_error"}, result_summary="Old result", outcome_attempt_id="A0001")
            store.save_task(old)
            store.set_meta(planning_wave=1)
            controller._plan()
            controller._prepare()
            current = store.get_task("T0001")
            self.assertEqual(current["active_attempt"], "A0002")
            self.assertEqual(current["latest_result_ref"], old["latest_result_ref"])
            self.assertEqual(current["finished_attempt"], "A0001")
            for name in ("accepted", "review_status", "failure", "result_summary", "outcome_attempt_id", "execution_status"):
                self.assertIsNone(current[name], name)
            self.assertTrue(store.read_record(old["latest_result_ref"])["accepted"])


if __name__ == "__main__":
    unittest.main()
