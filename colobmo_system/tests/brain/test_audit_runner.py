"""The lightweight auditor is a fresh, bounded process with no workflow tools."""
from __future__ import annotations

from contextlib import contextmanager
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from colombo.brain.evidence_audit import AuditError, run_audit, validate_result
from colombo.shared.process_control import managed_popen as real_managed_popen


PASS = {"verdict": "pass", "summary": "The stated implication holds.", "findings": []}


class FakeProcess:
    def __init__(self, callback, command, **kwargs):
        self.callback, self.command, self.kwargs = callback, command, kwargs
        self.pid, self.returncode = 23456, None

    def communicate(self, prompt, timeout):
        self.callback(self, prompt, timeout)
        if self.returncode is None:
            self.returncode = 0

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        if self.returncode is None:
            self.returncode = -1
        return self.returncode


class AuditRunnerTests(unittest.TestCase):
    def setUp(self):
        parent = PROJECT / "validation/tmp"
        parent.mkdir(exist_ok=True, parents=True)
        self.temp = tempfile.TemporaryDirectory(prefix="audit-runner-", dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project"
        self.project.mkdir()
        self.auth = self.root / "login"
        self.auth.mkdir()
        (self.auth / "auth.json").write_text('{"fake":"do-not-publish"}', encoding="utf-8")
        (self.auth / "config.toml").write_text(
            'model="user-model"\nmodel_reasoning_effort="medium"\n'
            '[mcp_servers.unrelated]\ncommand="unrelated"\n', encoding="utf-8")
        self.executable = self.root / "codex.exe"
        self.executable.write_bytes(b"test-fixture")
        self.config = {"brain": {"model": "brain-model", "reasoning_effort": "low", "timeout_seconds": 300},
                       "runtime": {"auth_home": str(self.auth), "codex_bin": str(self.executable)}}
        self.work = self.root / "run/audits/A1/workspace"
        self.payload = {"goal": "Does P imply Q under the supplied conditions?",
                        "inputs": {"P": "x is an even integer", "Q": "x is an integer"},
                        "records": [], "materials": []}

    @contextmanager
    def spawn(self, callback, cleanup=True):
        def finish(proc, **kwargs):
            proc.wait()
            return cleanup
        with patch("colombo.brain.evidence_audit.managed_popen", side_effect=lambda command, **kwargs:
                   FakeProcess(callback, command, **kwargs)) as launch, \
             patch("colombo.brain.evidence_audit.process_identity", return_value={"pid": 23456, "start_token": "audit-test"}), \
             patch("colombo.brain.evidence_audit.terminate_tree", side_effect=finish) as terminate, \
             patch("colombo.brain.evidence_audit.close_process_job"):
            yield launch, terminate

    def write_result(self, process, result=PASS):
        path = process.command[process.command.index("--output-last-message") + 1]
        Path(path).write_text(json.dumps(result), encoding="utf-8")

    def manifest(self):
        return json.loads((self.work / "process.json").read_text(encoding="utf-8"))

    def test_fresh_process_has_only_explicit_inputs_and_no_workflow_tools(self):
        captured = {}
        def callback(proc, prompt, timeout):
            captured["home"] = Path(proc.kwargs["env"]["CODEX_HOME"])
            config = tomllib.loads((captured["home"] / "config.toml").read_text(encoding="utf-8"))
            self.assertNotIn("mcp_servers", config)
            self.assertEqual(config["project_doc_max_bytes"], 0)
            self.assertEqual(config["model"], "brain-model")
            self.assertEqual(config["model_reasoning_effort"], "low")
            self.assertEqual(config["sandbox_mode"], "read-only")
            self.assertTrue(all(config["features"][key] is False for key in ("apps", "plugins", "hooks", "multi_agent")))
            self.assertIsNone(timeout)
            self.assertIn("--ephemeral", proc.command)
            self.assertIn("--output-schema", proc.command)
            self.assertNotIn("do-not-publish", prompt)
            self.assertFalse((self.work / "protocol.md").exists())
            self.assertFalse((self.work / ".agents").exists())
            self.assertEqual(json.loads((self.work / "input.json").read_text(encoding="utf-8")), self.payload)
            self.write_result(proc)
        with self.spawn(callback) as (launch, terminate):
            self.assertEqual(run_audit(self.project, self.config, self.work, self.payload), PASS)
        self.assertEqual(launch.call_count, 1)
        self.assertEqual(terminate.call_count, 1)
        self.assertFalse((captured["home"] / "auth.json").exists())
        self.assertTrue((self.auth / "auth.json").is_file())
        self.assertEqual(self.manifest()["status"], "completed")
        self.assertTrue(self.manifest()["process_exit_confirmed"])

    def test_audit_can_override_model_and_timeout(self):
        self.config["audit"] = {"model": "audit-model", "reasoning_effort": "high", "timeout_seconds": 12}
        def callback(proc, prompt, timeout):
            cfg = tomllib.loads((Path(proc.kwargs["env"]["CODEX_HOME"]) / "config.toml").read_text())
            self.assertEqual((cfg["model"], cfg["model_reasoning_effort"]), ("audit-model", "high"))
            self.assertGreater(timeout, 0)
            self.assertLessEqual(timeout, 12)
            self.write_result(proc)
        with self.spawn(callback):
            run_audit(self.project, self.config, self.work, self.payload)
        self.assertEqual(self.config["brain"]["model"], "brain-model")

    def test_fail_and_uncertain_are_successful_audit_opinions(self):
        for verdict in ("fail", "uncertain"):
            with self.subTest(verdict=verdict):
                result = {"verdict": verdict, "summary": "Scope is insufficient.", "findings": ["The supplied domain is narrower."]}
                with self.spawn(lambda p, *_: self.write_result(p, result)):
                    self.assertEqual(run_audit(self.project, self.config, self.work / verdict, self.payload), result)

    def test_result_contract_rejects_ambiguous_or_contradictory_outputs(self):
        invalid = [{}, [], {**PASS, "extra": 1}, {**PASS, "verdict": "accepted"},
                   {**PASS, "summary": " "}, {**PASS, "findings": ["unresolved"]},
                   {**PASS, "verdict": "fail", "findings": [""]}]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(AuditError):
                validate_result(value)

    def test_invalid_json_is_execution_failure(self):
        def callback(proc, *_):
            Path(proc.command[proc.command.index("--output-last-message") + 1]).write_text("not JSON")
        with self.spawn(callback), self.assertRaisesRegex(AuditError, "valid JSON"):
            run_audit(self.project, self.config, self.work, self.payload)
        self.assertEqual(self.manifest()["status"], "failed")

    def test_nonzero_exit_does_not_certify_even_valid_output(self):
        def callback(proc, *_):
            self.write_result(proc)
            proc.returncode = 7
        with self.spawn(callback), self.assertRaisesRegex(AuditError, "exit successfully"):
            run_audit(self.project, self.config, self.work, self.payload)
        self.assertEqual(self.manifest()["returncode"], 7)

    def test_timeout_cleans_process_and_never_accepts_written_result(self):
        def callback(proc, prompt, timeout):
            self.write_result(proc)
            raise subprocess.TimeoutExpired(proc.command, timeout)
        with self.spawn(callback) as (_, terminate):
            with self.assertRaisesRegex(AuditError, "timed out"):
                run_audit(self.project, self.config, self.work, self.payload)
        self.assertEqual(terminate.call_count, 1)
        self.assertEqual(self.manifest()["status"], "timeout")
        self.assertTrue(self.manifest()["process_exit_confirmed"])


    def test_uncertain_process_cleanup_blocks_success(self):
        with self.spawn(lambda p, *_: self.write_result(p), cleanup=False), \
             self.assertRaisesRegex(AuditError, "termination could not be confirmed"):
            run_audit(self.project, self.config, self.work, self.payload)
        self.assertEqual(self.manifest()["status"], "unknown")

    def test_workspace_is_not_reused_and_bad_input_never_launches(self):
        with self.spawn(lambda p, *_: self.write_result(p)) as (launch, _):
            run_audit(self.project, self.config, self.work, self.payload)
            with self.assertRaisesRegex(AuditError, "new or empty"):
                run_audit(self.project, self.config, self.work, self.payload)
            with self.assertRaisesRegex(AuditError, "nonempty goal"):
                run_audit(self.project, self.config, self.work / "invalid", {"goal": ""})
            bad = copy.deepcopy(self.config)
            bad["audit"] = {"timeout_seconds": float("nan")}
            with self.assertRaisesRegex(AuditError, "timeout_seconds"):
                run_audit(self.project, bad, self.work / "invalid", self.payload)
        self.assertEqual(launch.call_count, 1)

    def test_actual_child_process_returns_and_is_confirmed_exited(self):
        script = "import sys,pathlib; sys.stdin.read(); pathlib.Path(sys.argv[1]).write_text(sys.argv[2],encoding='utf-8')"
        def native_fixture(command, **kwargs):
            final = command[command.index("--output-last-message") + 1]
            return real_managed_popen([sys.executable, "-c", script, final, json.dumps(PASS)], **kwargs)
        with patch("colombo.brain.evidence_audit.managed_popen", side_effect=native_fixture):
            self.assertEqual(run_audit(self.project, self.config, self.work, self.payload), PASS)
        saved = self.manifest()
        self.assertNotEqual(saved["pid"], os.getpid())
        self.assertEqual(saved["status"], "completed")
        self.assertTrue(saved["process_exit_confirmed"])
        self.assertTrue(saved["process_tree_terminated"])


if __name__ == "__main__":
    unittest.main()
