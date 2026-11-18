"""Budget accounting, isolated completion markers and non-authoritative recovery."""
from __future__ import annotations

from contextlib import ExitStack
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import colombo.cell.recovery as handoff
import colombo.cell.model_calls as processes
import colombo.cell.settings as settings
from colombo.shared.file_io import Path


class Clock:
    now = 0.0

    def monotonic(self):
        return self.now

    def time(self):
        return 1000 + self.now

    def sleep(self, seconds):
        self.now += seconds


class Process:
    def __init__(self):
        self.stdin = io.StringIO()
        self.returncode = None
        self.pid = 100

    def poll(self):
        return self.returncode


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".handoff-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.work = self.root / "work"
        self.work.mkdir()
        (self.work / "problem.md").write_text("Prove 2 is even.", encoding="utf-8")
        self.config = settings.get_settings()
        self.config["handoff"].update(reserve_seconds=2, recovery_seconds=2, recovery_min_start_seconds=1)
        self.config["runtime"]["process_poll_seconds"] = 0.5
        self.auth = self.root / "login"
        self.auth.mkdir()
        (self.auth / "auth.json").write_text("test credential", encoding="utf-8")
        self.clock = Clock()
        self.calls = []
        self.homes = []
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(os.environ))
        os.environ.pop("CELL_PROCESS_ID", None)
        os.environ.pop("CELL_SETTINGS_FILE", None)
        self.stack.enter_context(patch.object(processes.time, "monotonic", self.clock.monotonic))
        self.stack.enter_context(patch.object(processes.time, "time", self.clock.time))
        self.stack.enter_context(patch.object(processes.time, "sleep", self.clock.sleep))
        self.stack.enter_context(patch.object(processes, "find_codex", return_value="test-codex"))
        self.stack.enter_context(patch.object(processes, "_user_home", return_value=self.auth))
        self.stack.enter_context(patch.object(processes, "_prepare_home", side_effect=self.prepare))
        self.stack.enter_context(patch.object(processes, "_terminate_tree", side_effect=self.stop))
        self.stack.enter_context(patch.object(processes.subprocess, "Popen", side_effect=self.launch))

    def prepare(self, *args, **kwargs):
        home = self.root / f"home-{len(self.homes)}"
        home.mkdir()
        self.homes.append(home)
        return home

    def launch(self, command, **kwargs):
        process = Process()
        selected_work = command[command.index("-C") + 1]
        self.assertEqual(selected_work, str(Path(selected_work)))
        self.assertIsInstance(kwargs["cwd"], str)
        self.calls.append({"command": command, "env": kwargs["env"], "process": process,
                           "started": self.clock.now, "cwd": Path(kwargs["cwd"]),
                           "work_dir": Path(selected_work)})
        return process

    def stop(self, process, wait_seconds):
        process.returncode = -1

    def run_process(self, role="prover", timeout=10):
        return processes.run_agent("Task", self.work, self.work / "output.json",
                                   role=role, timeout=timeout, settings=self.config)

    def read_report(self, error):
        return json.loads(Path(error.handoff_path).read_text(encoding="utf-8"))

    def test_windows_are_within_total_and_small_runs_retain_work(self):
        for total, reserve, recovery in ((900, 60, 30), (1, 60, 30), (10, 0, 0), (90, 60, 30)):
            window = handoff.budget_windows(total, reserve, recovery)
            self.assertAlmostEqual(window["work_seconds"] + window["reserve_seconds"] + window["recovery_seconds"], total)
            self.assertGreater(window["work_seconds"], 0)
            self.assertLessEqual(window["reserve_seconds"], reserve)
            self.assertLessEqual(window["recovery_seconds"], recovery)

    def test_experiment_execution_handles_survive_factual_handoff(self):
        experiment = self.work / "experiments" / ("exp-" + "a" * 24)
        experiment.mkdir(parents=True)
        for name in ("state.json", "plan.json", "large-output.json"):
            (experiment / name).write_text("{}", encoding="utf-8")
        references = handoff.saved_references(self.work)
        self.assertIn(experiment.relative_to(self.work).as_posix() + "/state.json", references)
        self.assertIn(experiment.relative_to(self.work).as_posix() + "/plan.json", references)
        self.assertFalse(any("large-output" in name for name in references))

    def test_local_challenge_identity_and_state_survive_handoff(self):
        challenge = self.work / "challenges" / ("ch-" + "a" * 24)
        challenge.mkdir(parents=True)
        for name in ("state.json", "input.json", "large-output.json"):
            (challenge / name).write_text("{}", encoding="utf-8")
        references = handoff.saved_references(self.work)
        self.assertIn(challenge.relative_to(self.work).as_posix() + "/state.json", references)
        self.assertIn(challenge.relative_to(self.work).as_posix() + "/input.json", references)
        self.assertFalse(any("large-output" in name for name in references))

    def test_cooperative_handoff_exits_without_final_review_schema(self):
        notes = self.work / "review_notes.json"
        notes.write_text('{"checks":[{"id":1,"status":"pass"}]}', encoding="utf-8")
        (self.work / "review_request.json").write_text(json.dumps({
            "stage": "proof", "review_id": "r0001", "report_revision": 1}), encoding="utf-8")
        original_sleep = self.clock.sleep

        def finish(seconds):
            original_sleep(seconds)
            if self.clock.now >= 6:
                with patch.dict(os.environ, {"CELL_PROCESS_ID": self.calls[0]["env"]["CELL_PROCESS_ID"]}):
                    budget = handoff.budget_status(self.work)
                    self.assertTrue(budget["closing"])
                    handoff.finish_handoff(self.work, "Checked item 1", ["Items 2–30 remain"],
                                           ["Resume item 2"], ["review_notes.json"])

        with patch.object(processes.time, "sleep", finish):
            result = self.run_process("verifier")
        self.assertEqual(result["execution_status"], "handoff")
        self.assertEqual(result["text"], "")
        self.assertEqual(len(self.calls), 1)
        report = json.loads(Path(result["handoff_path"]).read_text(encoding="utf-8"))
        self.assertEqual(report["recipient"], "next_verifier")
        self.assertEqual(report["review_id"], "r0001")
        self.assertNotIn("verdict", report)
        self.assertEqual(len(json.loads(notes.read_text())["checks"]), 1)
        self.assertFalse((self.homes[0] / "auth.json").exists())

    def test_stale_marker_and_modified_report_cannot_end_another_process(self):
        old_id, new_id = "a" * 32, "b" * 32
        handoff.begin_process(self.work, old_id, "prover", 10, self.config)
        handoff.finish_handoff(self.work, "Old", [], [])
        handoff.begin_process(self.work, new_id, "prover", 10, self.config)
        self.assertIsNone(handoff.completed_handoff(self.work, new_id))
        self.assertIsNotNone(handoff.completed_handoff(self.work, old_id))
        (self.work / "handoffs" / f"{old_id}.json").write_text("{}")
        self.assertIsNone(handoff.completed_handoff(self.work, old_id))
        with patch.dict(os.environ, {"CELL_PROCESS_ID": old_id}):
            self.assertEqual(handoff.budget_status(self.work)["process_id"], old_id)

    def test_timeout_includes_fallback_and_never_recursively_retries(self):
        notes = self.work / "review_notes.json"
        notes.write_text('{"checks":[]}', encoding="utf-8")
        with self.assertRaises(processes.AgentTimeout) as caught:
            self.run_process("verifier")
        self.assertEqual(self.clock.now, 10)
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(self.calls[1]["started"], 8)
        self.assertIn("read-only", self.calls[1]["command"])
        self.assertEqual(self.calls[1]["env"]["CELL_SEARCH_ENABLED"], "0")
        self.assertNotEqual(self.calls[1]["cwd"], self.work)
        packet = json.loads((self.calls[1]["work_dir"] / "recovery_input.json").read_text())
        documents = {row["source"]: row["content"] for row in packet["documents"]}
        self.assertEqual(documents["review_notes.json"], {"checks": []})
        self.assertFalse((self.calls[1]["work_dir"] / "review_notes.json").exists())
        report = self.read_report(caught.exception)
        self.assertFalse(report["has_review_authority"])
        self.assertEqual(report["recipient"], "next_verifier")
        self.assertNotIn("saved_evidence_summary", report)
        self.assertEqual(report["recovery"]["status"], "failed")
        self.assertEqual(report["recovery"]["reason"], "timeout")
        self.assertEqual(notes.read_text(), '{"checks":[]}')
        for home in self.homes:
            self.assertFalse((home / "auth.json").exists())

    def test_failed_packager_keeps_factual_report_and_original_notes(self):
        with patch.object(processes, "_recover_handoff", side_effect=ValueError("invalid model output")):
            with self.assertRaises(TimeoutError) as caught:
                self.run_process()
        report = self.read_report(caught.exception)
        self.assertEqual(report["source"], "runtime")
        self.assertEqual(report["execution_status"], "incomplete")
        self.assertEqual(report["recipient"], "next_prover")
        self.assertEqual(report["recovery"]["reason"], "unexpected_recovery_error")

    def test_successful_packager_reads_snapshot_and_adds_navigation_only(self):
        (self.work / "input").mkdir()
        (self.work / "input" / "draft.md").write_text("Saved draft", encoding="utf-8")
        (self.work / "review_request.json").write_text(json.dumps({
            "stage": "report_check", "review_id": "r0002", "report_revision": 2,
            "draft_file": "draft.md", "evidence_files": []}), encoding="utf-8")
        (self.work / "confirmation_notes.json").write_text('{"pending":["Issue F1"]}', encoding="utf-8")

        def launch(command, **kwargs):
            process = self.launch(command, **kwargs)
            if "read-only" in command:
                selected_work = Path(command[command.index("-C") + 1])
                packet = json.loads((selected_work / "recovery_input.json").read_text())
                documents = {row["source"]: row["content"] for row in packet["documents"]}
                self.assertEqual(documents["input/draft.md"], "Saved draft")
                self.assertEqual(documents["confirmation_notes.json"], {"pending": ["Issue F1"]})
                self.assertFalse((selected_work / "input/draft.md").exists())
                Path(command[command.index("-o") + 1]).write_text(json.dumps({
                    "summary": "Confirmation notes retain issue F1.", "pending": ["Issue F1"],
                    "next_steps": ["Resume report confirmation."]}), encoding="utf-8")
                process.returncode = 0
            return process

        with patch.object(processes.subprocess, "Popen", side_effect=launch):
            with self.assertRaises(TimeoutError) as caught:
                self.run_process("verifier")
        report = self.read_report(caught.exception)
        self.assertEqual(report["review_id"], "r0002")
        self.assertEqual(report["report_revision"], 2)
        self.assertEqual(report["saved_evidence_summary"]["pending"], ["Issue F1"])
        self.assertFalse(report["has_review_authority"])
        self.assertEqual(report["recipient"], "next_verifier")
        self.assertEqual(report["recovery"]["status"], "success")
        self.assertEqual((self.work / "input/draft.md").read_text(), "Saved draft")
        self.assertLessEqual(self.clock.now, 10)

    def test_termination_time_consumes_recovery_budget(self):
        def slow_stop(process, wait_seconds):
            self.clock.sleep(wait_seconds)
            process.returncode = -1

        with patch.object(processes, "_terminate_tree", side_effect=slow_stop):
            with self.assertRaises(TimeoutError):
                self.run_process()
        self.assertEqual(self.clock.now, 10)
        self.assertEqual(len(self.calls), 1)

    def test_setup_does_not_grant_a_fresh_process_budget(self):
        def slow_setup(*args, **kwargs):
            self.clock.sleep(10)
            return self.prepare(*args, **kwargs)

        with patch.object(processes, "_prepare_home", side_effect=slow_setup):
            with self.assertRaises(TimeoutError) as caught:
                self.run_process()
        self.assertEqual(self.clock.now, 10)
        self.assertEqual(len(self.calls), 0)
        self.assertEqual(self.read_report(caught.exception)["execution_status"], "incomplete")

    def test_short_budget_uses_python_report_without_extra_model(self):
        self.config["handoff"].update(reserve_seconds=60, recovery_seconds=30)
        with self.assertRaises(TimeoutError) as caught:
            self.run_process(timeout=1)
        report = self.read_report(caught.exception)
        self.assertLessEqual(self.clock.now, 1)
        self.assertEqual(len(self.calls), 1)
        self.assertAlmostEqual(report["budget"]["recovery_seconds"], 1 / 6)

    def test_recovery_summary_cannot_overwrite_review_authority(self):
        process_id = "a" * 32
        handoff.begin_process(self.work, process_id, "verifier", 10, self.config)
        path = handoff.factual_handoff(self.work, process_id, log_path=self.work / "log", reason="hard_timeout")
        handoff.enrich_handoff(path, {"summary": "Saved item 1", "pending": ["Other items"],
                                     "next_steps": ["Continue checks"], "verdict": "pass",
                                     "recipient": "prover", "has_review_authority": True})
        report = json.loads(path.read_text())
        self.assertFalse(report["has_review_authority"])
        self.assertFalse(report["saved_evidence_summary"]["has_review_authority"])
        self.assertEqual(report["recipient"], "next_verifier")
        self.assertNotIn("verdict", report)


class RecoveryHomeTests(unittest.TestCase):
    def test_packager_home_disables_mcp_search_and_subagents(self):
        with tempfile.TemporaryDirectory(prefix=".handoff-config-", dir=ROOT) as name:
            root = Path(name)
            auth = root / "auth"
            auth.mkdir()
            with patch.object(processes, "ROOT", root), \
                    patch.object(processes, "_user_home", return_value=auth), \
                    patch.object(processes, "_user_settings", return_value={}), \
                    patch.dict(os.environ, {"OPENAI_API_KEY": "test-only"}):
                home = processes._prepare_home(root, "verifier", None, True, {},
                                               settings=settings.get_settings(), recovery_only=True)
            config = tomllib.loads((home / "config.toml").read_text())
            self.assertEqual(config["web_search"], "disabled")
            self.assertEqual(config["sandbox_mode"], "read-only")
            self.assertNotIn("mcp_servers", config)
            self.assertFalse(config["features"]["multi_agent"])
            self.assertFalse(config["features"]["multi_agent_v2"])
            self.assertEqual(config["agents"], {"enabled": False})
            if os.name == "nt":
                self.assertTrue(config["features"]["prefer_mxc"])
            self.assertFalse((home / "auth.json").exists())


if __name__ == "__main__":
    unittest.main()
