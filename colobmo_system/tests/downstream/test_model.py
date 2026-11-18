"""Native adapter lifecycle checks with a fake process; no CLI or model is run."""
import json
import os
from pathlib import Path
import sys
import tempfile
import tomllib
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from colombo.downstream.model import NativeModel


class FakeProcess:
    pid = 424242

    def __init__(self, output, result, returncode=0):
        self.output, self.result = output, result
        self.exitcode = returncode
        self.returncode = None
        self.prompts = []

    def communicate(self, prompt, timeout):
        self.prompts.append((prompt, timeout))
        self.output.write_text(json.dumps(self.result), encoding="utf-8")
        self.returncode = self.exitcode
        return None, None


class NativeModelTests(unittest.TestCase):
    def setUp(self):
        temporary_parent = (PROJECT / ".runtime").resolve()
        temporary_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="model-test-", dir=temporary_parent)
        self.root = Path(self.temporary.name).resolve()
        self.assertTrue(self.root.is_relative_to(temporary_parent))
        self.addCleanup(self.temporary.cleanup)
        self.project = self.root / "project"
        self.source = self.project / "agents" / "writing"
        skill = self.source / ".agents" / "skills" / "manuscript-writing"
        skill.mkdir(parents=True)
        (self.source / "AGENTS.md").write_text("Read input.json and return structured output.\n", encoding="utf-8")
        (skill / "SKILL.md").write_text("Preserve the supplied mathematical claims.\n", encoding="utf-8")
        references = skill / "references"
        references.mkdir()
        self.reference = references / "principles.md"
        self.reference.write_text("Original reference guidance.\n", encoding="utf-8")
        self.auth_source = self.root / "auth-source"
        self.auth_source.mkdir()
        (self.auth_source / "auth.json").write_text('{"test_credential":"synthetic-only"}', encoding="utf-8")
        self.work = self.root / "call"
        self.context = {"proof_sha256": "f" * 64, "proof": "A fixed proof."}
        self.schema = {"type": "object", "properties": {"text": {"type": "string"}},
                       "required": ["text"], "additionalProperties": False}
        self.result = {"text": "Complete structured output."}
        self.exitcode = 0
        self.processes = []
        self.launches = []
        self.model = NativeModel(self.project, "writing", {"auth_home": str(self.auth_source),
                                                         "search_enabled": False})
        for name, replacement in (
            ("model_launcher.user_configuration", {}),
            ("model_launcher.discover_cli", str(self.root / "fake-codex.exe")),
            ("model_launcher.seed_model_cache", None),
            ("process_identity", {"pid": 424242, "start_token": "synthetic-process"}),
        ):
            mocked = patch("colombo.downstream.model." + name, return_value=replacement)
            mocked.start()
            self.addCleanup(mocked.stop)
        self.popen_patch = patch("colombo.downstream.model.managed_popen", side_effect=self.fake_launch)
        self.popen = self.popen_patch.start()
        self.addCleanup(self.popen_patch.stop)
        self.terminate_patch = patch("colombo.downstream.model.terminate_tree", return_value=True)
        self.terminate = self.terminate_patch.start()
        self.addCleanup(self.terminate_patch.stop)
        self.close_patch = patch("colombo.downstream.model.close_process_job")
        self.close = self.close_patch.start()
        self.addCleanup(self.close_patch.stop)

    def fake_launch(self, command, **kwargs):
        self.launches.append((command, kwargs))
        staged_home = Path(kwargs["env"]["CODEX_HOME"])
        self.assertTrue((staged_home / "auth.json").is_file())
        output = Path(command[command.index("--output-last-message") + 1])
        process = FakeProcess(output, self.result, self.exitcode)
        self.processes.append(process)
        return process

    def invoke(self):
        return self.model.invoke("manuscript-writing", self.work, "Write the fixed result.",
                                 self.context, self.schema, 30)

    def manifest(self):
        return json.loads((self.work / "process.json").read_text(encoding="utf-8"))

    def assert_cleanup(self):
        self.assertFalse((self.work / ".auth" / "auth.json").exists())
        self.assertTrue((self.auth_source / "auth.json").is_file())
        self.assertFalse((self.work / ".call.lock").exists())
        self.assertIn("ended_at", self.manifest())

    def test_structured_output_and_replay_without_second_process(self):
        self.assertEqual(self.invoke(), self.result)
        command, _ = self.launches[0]
        self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
        schema_path = Path(command[command.index("--output-schema") + 1])
        self.assertEqual(json.loads(schema_path.read_text(encoding="utf-8")), self.schema)
        self.assertEqual(json.loads((self.work / "input.json").read_text(encoding="utf-8")), self.context)
        self.assertEqual(self.manifest()["status"], "completed")
        self.assertTrue(self.manifest()["process_tree_terminated"])
        self.assert_cleanup()
        self.assertEqual(self.invoke(), self.result)
        self.assertEqual(self.popen.call_count, 1)

    def test_windows_config_selects_mxc_runtime_for_readonly_tools(self):
        # Replace only this module's OS view. Changing the real os.name would
        # make pathlib select WindowsPath on POSIX test hosts.
        windows = SimpleNamespace(name="nt", environ=os.environ, getenv=os.getenv)
        with patch("colombo.downstream.model.os", windows):
            self.assertEqual(self.invoke(), self.result)
        config = tomllib.loads((self.work / ".auth" / "config.toml").read_text(encoding="utf-8"))
        self.assertIs(config["features"].get("prefer_mxc"), True)
        self.assertEqual(config["sandbox_mode"], "read-only")
        self.assertEqual(config["windows"]["sandbox"], "elevated")
        self.assert_cleanup()

    def test_process_failure_removes_staged_credentials(self):
        self.exitcode = 2
        with self.assertRaisesRegex(RuntimeError, "exited unsuccessfully"):
            self.invoke()
        self.assertEqual(self.manifest()["status"], "failed")
        self.assert_cleanup()
        self.close.assert_called_once()

    def test_terminate_exception_still_removes_credentials_and_records_unknown_exit(self):
        self.terminate.side_effect = OSError("Synthetic termination error")
        with self.assertRaisesRegex(RuntimeError, "exit is unconfirmed"):
            self.invoke()
        self.assertEqual(self.manifest()["status"], "unknown")
        self.assertFalse(self.manifest()["process_tree_terminated"])
        self.assert_cleanup()
        self.close.assert_called_once()

    def test_job_close_exception_cannot_skip_credential_cleanup(self):
        self.close.side_effect = OSError("Synthetic handle-close error")
        with self.assertRaises(OSError):
            self.invoke()
        self.assert_cleanup()

    def test_unsettled_call_is_not_relaunched(self):
        self.terminate.return_value = False
        with self.assertRaisesRegex(RuntimeError, "exit is unconfirmed"):
            self.invoke()
        self.assertEqual(self.manifest()["status"], "unknown")
        self.terminate.return_value = True
        with self.assertRaisesRegex(RuntimeError, "not completed"):
            self.invoke()
        self.assertEqual(self.popen.call_count, 1)
        self.assert_cleanup()

    def test_modified_result_or_reference_cannot_reuse_completed_call(self):
        self.invoke()
        (self.work / "final.json").write_text('{"text":"Altered output."}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "output changed"):
            self.invoke()
        (self.work / "final.json").write_text(json.dumps(self.result), encoding="utf-8")
        self.reference.write_text("Changed reference guidance.\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "different input"):
            self.invoke()
        self.assertEqual(self.popen.call_count, 1)


if __name__ == "__main__":
    unittest.main()
