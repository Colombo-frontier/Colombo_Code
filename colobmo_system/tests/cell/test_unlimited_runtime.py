"""Unlimited process time is an absent deadline, with cancellation and handoff intact."""
from __future__ import annotations

from contextlib import ExitStack
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import colombo.cell.recovery as handoff
import colombo.cell.model_calls as processes
import colombo.cell.settings as settings
from colombo.shared.file_io import Path


ROOT = Path(__file__).resolve().parents[2]


class UnlimitedRuntimeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".unlimited-runtime-", dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.work = self.root / "work"
        self.work.mkdir()
        (self.work / "problem.md").write_text("A saved research target", encoding="utf-8")
        self.auth = self.root / "auth"
        self.auth.mkdir()
        (self.auth / "auth.json").write_text("test fixture", encoding="utf-8")
        self.clock = 0.0
        self.completion = None
        self.on_sleep = None
        self.calls, self.homes, self.stops = [], [], []
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(os.environ))
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        os.environ.pop("COLOMBO_BUDGET_FILE", None)
        self.config = settings.get_settings()
        self.config["runtime"]["process_poll_seconds"] = 60
        self.stack.enter_context(patch.object(processes.time, "monotonic", lambda: self.clock))
        self.stack.enter_context(patch.object(processes.time, "time", lambda: 1000 + self.clock))
        self.stack.enter_context(patch.object(processes.time, "sleep", self.sleep))
        self.stack.enter_context(patch.object(processes, "find_codex", return_value="test-codex"))
        self.stack.enter_context(patch.object(processes, "_user_home", return_value=self.auth))
        self.stack.enter_context(patch.object(processes, "_prepare_home", side_effect=self.prepare))
        self.stack.enter_context(patch.object(processes, "_terminate_tree", side_effect=self.stop))
        self.stack.enter_context(patch.object(processes.subprocess, "Popen", side_effect=self.launch))
        self.recover = self.stack.enter_context(patch.object(processes, "_recover_handoff"))

    def sleep(self, seconds):
        self.clock += seconds
        if self.on_sleep:
            self.on_sleep()
        if self.clock > 20000:
            raise AssertionError("Test process did not reach its intended exit")

    def prepare(self, *args, **kwargs):
        home = self.root / f"home-{len(self.homes)}"
        home.mkdir()
        self.homes.append(home)
        return home

    def launch(self, command, **options):
        owner = self
        selected_work = command[command.index("-C") + 1]
        self.assertEqual(selected_work, str(Path(selected_work)))
        self.assertIsInstance(options["cwd"], str)
        output = Path(command[command.index("-o") + 1])

        class Process:
            stdin = io.StringIO()
            pid = 1234
            returncode = None

            def poll(self):
                if self.returncode is None and owner.completion is not None and owner.clock >= owner.completion:
                    output.write_text("Saved result", encoding="utf-8")
                    self.returncode = 0
                return self.returncode

        process = Process()
        self.calls.append({"process": process, "command": command, **options,
                           "cwd": Path(options["cwd"])})
        return process

    def stop(self, process, wait_seconds):
        self.stops.append(wait_seconds)
        process.returncode = -1

    def run_process(self, **kwargs):
        return processes.run_agent("Research", self.work, self.work / "output.txt",
                                   settings=self.config, **kwargs)

    def state(self):
        identifier = self.calls[0]["env"]["CELL_PROCESS_ID"]
        return json.loads((self.work / "runtime/processes" / f"{identifier}.json").read_text(encoding="utf-8"))

    def test_each_long_role_can_finish_normally_after_old_deadline(self):
        for role in ("prover", "subcell", "verifier"):
            with self.subTest(role=role):
                self.config["agents"][f"{role}_timeout_seconds"] = "unlimited"
                self.completion = self.clock + 3660
                result = self.run_process(role=role)
                self.assertEqual(result["returncode"], 0)
                self.assertGreater(result["elapsed_seconds"], 300)
                self.assertFalse(self.stops)
        self.recover.assert_not_called()
        for home in self.homes:
            self.assertFalse((home / "auth.json").exists())

    def test_budget_reports_no_deadline_or_closing_and_serializes_strict_json(self):
        identifier = "a" * 32
        handoff.begin_process(self.work, identifier, "prover", None, self.config)
        self.clock = 1000000
        budget = handoff.budget_status(self.work)
        self.assertFalse(budget["time_limit_enabled"])
        self.assertFalse(budget["closing"])
        for key in ("total_seconds", "work_seconds", "soft_deadline", "hard_deadline", "total_deadline",
                    "remaining_seconds", "work_remaining_seconds"):
            self.assertIsNone(budget[key], key)
        self.assertEqual(budget["reserve_seconds"], 0)
        self.assertEqual(budget["recovery_seconds"], 0)
        json.dumps(budget, allow_nan=False)
        result = handoff.finish_handoff(self.work, "Saved research", ["One open step"], ["Resume it"])
        report = json.loads(Path(result["handoff_path"]).read_text(encoding="utf-8"))
        self.assertIsNone(report["budget"]["total_seconds"])
        self.assertFalse(report["budget"]["time_limit_enabled"])

    def test_unlimited_process_can_end_through_explicit_handoff(self):
        def finish():
            if self.clock >= 3600:
                budget = handoff.budget_status(self.work)
                self.assertFalse(budget["closing"])
                handoff.finish_handoff(self.work, "Saved partial proof", ["Remaining case"], ["Continue"],
                                       stopping_reason="deliberate_pause")
        self.on_sleep = finish
        result = self.run_process(role="prover", timeout="unlimited")
        self.assertEqual(result["execution_status"], "handoff")
        self.assertEqual(self.state()["status"], "handoff")
        self.assertEqual(self.stops, [self.config["runtime"]["terminate_wait_seconds"]])
        self.recover.assert_not_called()

    def test_unlimited_subcell_cancellation_retains_bounded_cleanup(self):
        cancel = self.work / "cancel.flag"
        self.on_sleep = lambda: cancel.touch() if self.clock >= 3600 else None
        with self.assertRaisesRegex(processes.AgentError, "cancelled"):
            self.run_process(role="subcell", timeout="unlimited", extra_env={"CELL_CANCEL_FILE": str(cancel)})
        self.assertEqual(self.stops, [self.config["runtime"]["terminate_wait_seconds"]])
        self.assertFalse((self.homes[0] / "auth.json").exists())
        self.recover.assert_not_called()

    def test_keyboard_interrupt_cleans_up_unlimited_process(self):
        def interrupt():
            raise KeyboardInterrupt
        self.on_sleep = interrupt
        with self.assertRaises(KeyboardInterrupt):
            self.run_process(role="prover", timeout="unlimited")
        self.assertEqual(self.stops, [self.config["runtime"]["terminate_wait_seconds"]])
        self.assertFalse((self.homes[0] / "auth.json").exists())
        self.recover.assert_not_called()

    def test_explicit_finite_timeout_still_overrides_unlimited_default(self):
        self.config["agents"]["prover_timeout_seconds"] = "unlimited"
        with self.assertRaises(processes.AgentTimeout):
            self.run_process(role="prover", timeout=300)
        state = self.state()
        self.assertTrue(state["time_limit_enabled"])
        self.assertEqual(state["total_seconds"], 300)
        self.assertEqual(state["work_seconds"], 300 - self.config["handoff"]["reserve_seconds"]
                         - self.config["handoff"]["recovery_seconds"])
        self.assertEqual(self.clock, 300 - self.config["handoff"]["recovery_seconds"])

    def test_outer_deadline_caps_unlimited_process_and_visible_budget(self):
        self.config["handoff"].update(reserve_seconds=0, recovery_seconds=0)
        with self.assertRaises(processes.AgentTimeout):
            self.run_process(role="prover", timeout="unlimited", _absolute_deadline=7)
        state = self.state()
        self.assertTrue(state["time_limit_enabled"])
        self.assertEqual(state["total_seconds"], 7)
        self.assertEqual(state["total_deadline"], 1007)
        self.assertEqual(self.clock, 7)
        self.assertEqual(self.stops, [0])

    def test_expired_outer_deadline_starts_no_process(self):
        with self.assertRaises(processes.AgentTimeout):
            self.run_process(role="prover", timeout="unlimited", _absolute_deadline=-1)
        self.assertFalse(self.calls)
        self.assertFalse(self.homes)

    def test_recovery_and_explicit_deadlines_reject_invalid_nonfinite_budgets(self):
        for options in ({"role": "prover", "timeout": "unlimited", "recovery_only": True},
                        {"role": "prover", "timeout": float("inf"), "recovery_only": True},
                        {"role": "prover", "timeout": "unlimited", "_absolute_deadline": float("inf")}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.run_process(**options)
        self.assertEqual(len(self.calls), 0)

    def test_local_audit_can_finish_after_all_old_timeouts(self):
        self.completion = 4000
        result = self.run_process(role="audit", timeout="unlimited")
        self.assertEqual(result["returncode"], 0)
        self.assertGreaterEqual(result["elapsed_seconds"], 4000)
        self.assertEqual(len(self.stops), 0)

    def test_managed_unlimited_audit_replaces_old_snapshot_and_explicit_timeout(self):
        from colombo.shared.runtime_budget import start_budget
        policy = settings.load_policy(profile="hard")
        policy["cell"]["settings"]["runtime"]["process_poll_seconds"] = 60
        context = start_budget(self.work, policy)
        self.config["agents"]["audit_timeout_seconds"] = 75
        self.completion = 4000
        result = self.run_process(role="audit", timeout=75)
        self.assertGreaterEqual(result["elapsed_seconds"], 4000)
        self.assertFalse(self.state()["time_limit_enabled"])
        self.assertEqual(self.calls[0]["env"]["COLOMBO_BUDGET_FILE"], context["budget_file"])
        self.assertEqual(len(self.stops), 0)

    def test_expired_shared_budget_never_launches_a_model(self):
        from colombo.shared.runtime_budget import start_budget
        from colombo.shared.runtime_budget import BudgetExhausted
        policy = settings.load_policy(profile="standard")
        # Explicit historical ledger fixture; current Colombo has no shared deadline.
        policy["workflow"] = {"version": 2}
        policy["budget"] = {"research": {"total_active_seconds": 10}}
        start_budget(self.work, policy)
        self.clock = 11
        with self.assertRaises(BudgetExhausted):
            self.run_process(role="audit")
        self.assertEqual(len(self.calls), 0)
        self.assertEqual(len(self.homes), 0)

    def test_pending_tool_job_prevents_completed_result(self):
        self.completion = 1
        with patch("colombo.shared.tool_jobs.pending_jobs", return_value=[{"job_id": "job-pending"}]):
            result = self.run_process(role="prover", timeout="unlimited")
        self.assertEqual(result["execution_status"], "incomplete")
        self.assertEqual(self.state()["status"], "incomplete")

    def test_legacy_finite_budget_without_new_flag_remains_readable(self):
        identifier = "b" * 32
        self.config["handoff"].update(reserve_seconds=60, recovery_seconds=30)
        state = handoff.begin_process(self.work, identifier, "prover", 300, self.config)
        state.pop("time_limit_enabled")
        path = self.work / "runtime/processes" / f"{identifier}.json"
        path.write_text(json.dumps(state), encoding="utf-8")
        self.clock = 250
        budget = handoff.budget_status(self.work)
        self.assertTrue(budget["time_limit_enabled"])
        self.assertTrue(budget["closing"])
        self.assertEqual(budget["remaining_seconds"], 20)


if __name__ == "__main__":
    unittest.main()
