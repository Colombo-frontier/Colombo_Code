"""Recovery stays bounded, observable and unable to certify mathematical claims."""
from __future__ import annotations

from contextlib import ExitStack
from copy import deepcopy
import io
import json
import os
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import colombo.cell.recovery as handoff
import colombo.cell.model_calls as processes
import colombo.cell.recovery as recovery
import colombo.cell.settings as settings
from colombo.shared.file_io import Path


ROOT = Path(__file__).resolve().parents[2]
SUMMARY = {"summary": "The saved proof state identifies one unresolved step.",
           "pending": ["The final implication remains open."],
           "next_steps": ["Resume the recorded implication."]}


class RecoveryLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(os.environ))
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        directory = tempfile.TemporaryDirectory(prefix=".recovery-life-", dir=str(ROOT))
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.work = self.root / "work"
        self.work.mkdir()
        (self.work / "problem.md").write_text("Prove the saved target.", encoding="utf-8")
        self.config = settings.get_settings()
        self.config["model"]["reasoning_effort"] = "max"
        self.config["handoff"].update(recovery_reasoning_effort="low", recovery_min_start_seconds=45)
        self.clock = 10.0
        self.stack.enter_context(patch.object(processes.time, "monotonic", lambda: self.clock))
        self.stack.enter_context(patch.object(processes.time, "time", lambda: 1000 + self.clock))
        self.identifier = "a" * 32
        handoff.begin_process(self.work, self.identifier, "prover", 100, self.config,
                              started_at=1000, started_monotonic=0)
        self.report = handoff.factual_handoff(self.work, self.identifier,
                                              log_path=self.work / "events.jsonl", reason="hard_timeout")
        self.original = self.read_report()
        self.source_bytes = (self.work / "problem.md").read_bytes()
        self.deadline = 100.0

    def read_report(self):
        return json.loads(self.report.read_text(encoding="utf-8"))

    def recover(self):
        return processes._recover_handoff(self.work, self.report, "prover", self.deadline,
                                            self.config, None)

    def assert_original_preserved(self, *, enriched=False):
        result = self.read_report()
        self.assertEqual({key: result[key] for key in self.original}, self.original)
        self.assertEqual((self.work / "problem.md").read_bytes(), self.source_bytes)
        self.assertFalse(result["has_review_authority"])
        self.assertEqual(result["execution_status"], "incomplete")
        self.assertFalse(result["recovery"]["has_review_authority"])
        if not enriched:
            self.assertNotIn("saved_evidence_summary", result)
        return result

    def test_success_records_lifecycle_and_changes_only_recovery_model_configuration(self):
        before = deepcopy(self.config)
        phases = []
        original_record = processes.record_recovery_status

        def record(path, value):
            phases.append(deepcopy(value))
            original_record(path, value)

        def reviewer(prompt, snapshot, output, **kwargs):
            self.assertEqual(kwargs["settings"]["model"]["reasoning_effort"], "low")
            self.assertEqual(self.config["model"]["reasoning_effort"], "max")
            self.assertTrue(kwargs["recovery_only"])
            self.assertFalse(kwargs["search"])
            self.assertEqual(kwargs["_absolute_deadline"], 100)
            self.assertEqual(kwargs["timeout"], 90)
            files = [p.name for p in snapshot.iterdir()]
            self.assertEqual(files, ["recovery_input.json"])
            packet = json.loads((snapshot / "recovery_input.json").read_text())
            self.assertFalse(packet["has_review_authority"])
            self.assertIn("Do not search for or read any other files", prompt)
            self.clock += 7
            return {"text": json.dumps(SUMMARY)}

        with patch.object(processes, "record_recovery_status", side_effect=record), \
                patch.object(processes, "run_agent", side_effect=reviewer) as runner:
            state = self.recover()
        runner.assert_called_once()
        self.assertEqual(state["status"], "success")
        self.assertEqual(state["reason"], "summary_saved")
        self.assertEqual(state["elapsed_seconds"], 7)
        self.assertEqual(state["remaining_seconds"], 83)
        self.assertEqual([row["stage"] for row in phases], ["prepare", "model", "publish"])
        self.assertEqual([row["status"] for row in phases], ["running", "running", "success"])
        self.assertEqual(self.config, before)
        report = self.assert_original_preserved(enriched=True)
        self.assertEqual(report["saved_evidence_summary"]["summary"], SUMMARY["summary"])
        self.assertFalse(report["saved_evidence_summary"]["has_review_authority"])

    def test_insufficient_balance_skips_preparation_and_model(self):
        self.clock = 70
        with patch.object(recovery, "build_recovery_packet") as packet, \
                patch.object(processes, "run_agent") as runner:
            state = self.recover()
        packet.assert_not_called()
        runner.assert_not_called()
        self.assertEqual(state["status"], "skipped")
        self.assertEqual(state["reason"], "insufficient_time_before_preparation")
        self.assertEqual(state["remaining_seconds"], 30)
        self.assert_original_preserved()

    def test_packet_preparation_consumes_the_same_budget(self):
        original_build = recovery.build_recovery_packet

        def slow_build(*args, **kwargs):
            result = original_build(*args, **kwargs)
            self.clock += 50
            return result

        with patch.object(recovery, "build_recovery_packet", side_effect=slow_build), \
                patch.object(processes, "run_agent") as runner:
            state = self.recover()
        runner.assert_not_called()
        self.assertEqual(state["status"], "skipped")
        self.assertEqual(state["reason"], "insufficient_time_after_preparation")
        self.assertEqual(state["elapsed_seconds"], 50)
        self.assertEqual(state["remaining_seconds"], 40)
        self.assertIn("input", state)
        self.assert_original_preserved()

    def test_preparation_failure_records_exception_without_model(self):
        with patch.object(recovery, "build_recovery_packet", side_effect=OSError("Cannot write recovery packet")), \
                patch.object(processes, "run_agent") as runner:
            state = self.recover()
        runner.assert_not_called()
        self.assertEqual((state["status"], state["stage"], state["reason"]),
                         ("failed", "prepare", "input_preparation_failed"))
        self.assertEqual(state["error_type"], "OSError")
        self.assert_original_preserved()

    def test_startup_and_model_failures_have_different_reasons(self):
        for failed_stage, reason in (("startup", "startup_failed"), ("model", "model_failed")):
            with self.subTest(stage=failed_stage):
                error = processes.AgentError("Explicit fixture failure")
                error.execution_stage = failed_stage
                with patch.object(processes, "run_agent", side_effect=error):
                    state = self.recover()
                self.assertEqual((state["status"], state["stage"], state["reason"]),
                                 ("failed", "model", reason))
                self.assertEqual(state["error_type"], "AgentError")
                self.assert_original_preserved()

    def test_timeout_is_recorded_without_resetting_deadline_or_recursing(self):
        def timeout(*args, **kwargs):
            self.assertEqual(kwargs["_absolute_deadline"], self.deadline)
            self.clock = self.deadline
            raise processes.AgentTimeout("The fixed enclosing deadline was reached")

        with patch.object(processes, "run_agent", side_effect=timeout) as runner:
            state = self.recover()
        runner.assert_called_once()
        self.assertEqual(state["status"], "failed")
        self.assertEqual(state["reason"], "timeout")
        self.assertEqual(state["remaining_seconds"], 0)
        self.assertEqual(self.clock, 100)
        self.assert_original_preserved()

    def test_invalid_summary_cannot_be_published_or_assert_authority(self):
        for text in ("{invalid", json.dumps({**SUMMARY, "verdict": "pass"}),
                     json.dumps({**SUMMARY, "summary": " "}),
                     json.dumps({**SUMMARY, "pending": [""]})):
            with self.subTest(text=text), patch.object(processes, "run_agent", return_value={"text": text}):
                state = self.recover()
            self.assertEqual((state["status"], state["stage"], state["reason"]),
                             ("failed", "parse", "invalid_output"))
            self.assert_original_preserved()

    def test_completed_output_after_deadline_is_not_published(self):
        def late(*args, **kwargs):
            self.clock = self.deadline
            return {"text": json.dumps(SUMMARY)}

        with patch.object(processes, "run_agent", side_effect=late), \
                patch.object(processes, "enrich_handoff") as publish:
            state = self.recover()
        publish.assert_not_called()
        self.assertEqual(state["reason"], "deadline_before_publish")
        self.assert_original_preserved()

    def test_summary_save_error_preserves_the_factual_report(self):
        with patch.object(processes, "run_agent", return_value={"text": json.dumps(SUMMARY)}), \
                patch.object(processes, "enrich_handoff", side_effect=PermissionError("Cannot add summary")):
            state = self.recover()
        self.assertEqual((state["status"], state["stage"], state["reason"]),
                         ("failed", "publish", "summary_write_failed"))
        self.assertEqual(state["error_type"], "PermissionError")
        self.assert_original_preserved()

    def test_real_launcher_uses_low_and_reports_balance_after_setup(self):
        auth = self.root / "auth"
        auth.mkdir()
        captured = []
        original_prepare = processes._prepare_home

        def prepare(*args, **kwargs):
            self.clock += 5
            return original_prepare(*args, **kwargs)

        class Input(io.StringIO):
            saved = ""

            def close(self):
                self.saved = self.getvalue()
                super().close()

        class Process:
            returncode = 0
            pid = 123

            def __init__(self):
                self.stdin = Input()

            def poll(self):
                return self.returncode

        def launch(command, **kwargs):
            home = Path(kwargs["env"]["CODEX_HOME"])
            configuration = tomllib.loads((home / "config.toml").read_text())
            selected_work = command[command.index("-C") + 1]
            self.assertEqual(selected_work, str(Path(selected_work)))
            self.assertIsInstance(kwargs["cwd"], str)
            self.assertIn(selected_work, configuration["projects"])
            packet = json.loads((Path(selected_work) / "recovery_input.json").read_text())
            self.assertFalse(packet["has_review_authority"])
            self.assertEqual(configuration["model_reasoning_effort"], "low")
            self.assertEqual(configuration["sandbox_mode"], "read-only")
            self.assertEqual(configuration["web_search"], "disabled")
            self.assertNotIn("mcp_servers", configuration)
            self.assertFalse(configuration["features"]["multi_agent"])
            output = Path(command[command.index("-o") + 1])
            output.write_text(json.dumps(SUMMARY), encoding="utf-8")
            process = Process()
            captured.append(process)
            return process

        with patch.object(processes, "ROOT", self.root / "runtime-project"), \
                patch.object(processes, "_user_home", return_value=auth), \
                patch.object(processes, "_user_settings", return_value={}), \
                patch.object(processes, "_prepare_home", side_effect=prepare), \
                patch.object(processes, "find_codex", return_value="test-model-not-executed"), \
                patch.object(processes.subprocess, "Popen", side_effect=launch), \
                patch.dict(os.environ, {"OPENAI_API_KEY": "test-fixture-no-network"}):
            state = self.recover()
        self.assertEqual(state["status"], "success")
        self.assertEqual(len(captured), 1)
        self.assertIn("at most 85.0 seconds remain", captured[0].stdin.saved)
        self.assertIn("There is no budget_status tool here", captured[0].stdin.saved)
        self.assertEqual(state["elapsed_seconds"], 5)
        self.assertEqual(self.config["model"]["reasoning_effort"], "max")
        self.assert_original_preserved(enriched=True)


if __name__ == "__main__":
    unittest.main()
