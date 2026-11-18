"""Check CLI arguments, receipts, isolated directories, and reuse of paid calls without starting real Codex."""
import json
from pathlib import Path
import tempfile
import unittest

from oracle_atlas.providers.codex import CodexBackend, CodexUncertain


class FakePopen:
    calls = []
    fail = False
    def __init__(self, command, **kwargs):
        type(self).calls.append((command, kwargs))
        self.returncode = 1 if self.fail else 0
        self.kwargs = kwargs
        if not self.fail:
            target = Path(command[command.index("--output-last-message") + 1])
            target.write_text('{"status":"complete","artifact_refs":[],"summary":"fixture","checkpoint_ref":null}')
            kwargs["stdout"].write(b'{"type":"thread.started","thread_id":"test-thread"}\n')
            kwargs["stdout"].write(b'{"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":3}}\n')
    def communicate(self, **kwargs):
        self.input = kwargs.get("input")
        return None, None


class CodexTests(unittest.TestCase):
    def setUp(self):
        FakePopen.calls = []
        FakePopen.fail = False
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        config_file = Path(self.tmp.name) / "config.json"
        config_file.write_text('{}')
        self.runtime = {"workspace": self.tmp.name, "config_path": str(config_file)}
        self.backend = CodexBackend({"model": "explicit-model"}, popen=FakePopen)
        self.backend.bind_job({"id": "test-job", "role": "extractor", "inputs": {}}, self.runtime)

    def test_explicit_instructions_required_mcp_and_cached_receipt(self):
        reply = self.backend.complete("Role protocol", [{"role": "user", "content": "refs only"}], [], {"type": "object"})
        self.assertEqual(reply.usage["input_tokens"], 10)
        cmd, kwargs = FakePopen.calls[0]
        self.assertIn("--output-schema", cmd)
        self.assertIn("--ephemeral", cmd)
        self.assertNotIn("--ignore-user-config", cmd)
        self.assertNotIn("--ignore-rules", cmd)
        self.assertTrue(any(x == 'mcp_servers.oracle_atlas.required=true' for x in cmd))
        self.assertIn('--job', " ".join(cmd))
        cwd = Path(kwargs["cwd"])
        self.assertEqual((cwd / "AGENTS.md").read_text(), "Role protocol")
        self.assertIn("refs only", (cwd / "input.json").read_text())
        self.backend.complete("Role protocol", [{"role": "user", "content": "refs only"}], [], {"type": "object"})
        self.assertEqual(len(FakePopen.calls), 1)
        self.assertIn("not observable", (cwd / "transport-metadata.json").read_text())

    def test_uncertain_is_not_reexecuted(self):
        FakePopen.fail = True
        with self.assertRaises(CodexUncertain):
            self.backend.complete("rules", [], [], {})
        FakePopen.fail = False
        with self.assertRaises(CodexUncertain):
            self.backend.complete("rules", [], [], {})
        self.assertEqual(len(FakePopen.calls), 1)

    def test_effort_is_pinned_in_actual_command_receipt_metadata_and_cache_key(self):
        for effort in ("max", "high"):
            backend = CodexBackend({"model": "gpt-6-astra", "reasoning_effort": effort}, popen=FakePopen)
            backend.bind_job({"id":"test-job", "inputs":{}}, self.runtime)
            backend.complete("rules", [], [], {})
            command, kwargs = FakePopen.calls[-1]
            self.assertIn('model_reasoning_effort="' + effort + '"', command)
            directory = Path(kwargs["cwd"])
            metadata = json.loads((directory / "transport-metadata.json").read_text())
            receipt = json.loads((directory / "receipt.json").read_text())
            self.assertEqual(metadata["reasoning_effort"], effort)
            self.assertEqual(metadata["reasoning_effort_source"], "explicit_cli_override")
            self.assertEqual(receipt["reasoning_effort"], effort)
            self.assertGreaterEqual(receipt["elapsed_seconds"], 0)
        self.assertEqual(len(FakePopen.calls), 2)
        self.assertNotEqual(FakePopen.calls[0][1]["cwd"], FakePopen.calls[1][1]["cwd"])

    def test_fresh_review_gets_distinct_request_directory(self):
        self.backend.complete("rules", [], [], {})
        self.backend.bind_job({"id": "review-job", "role": "extraction_reviewer", "inputs": {}}, self.runtime)
        self.backend.complete("rules", [], [], {})
        self.assertNotEqual(FakePopen.calls[0][1]["cwd"], FakePopen.calls[1][1]["cwd"])


    def test_explicit_generation_retains_old_uncertain_and_starts_new(self):
        FakePopen.fail = True
        with self.assertRaises(CodexUncertain):
            self.backend.complete("rules", [], [], {})
        first = Path(FakePopen.calls[0][1]["cwd"])
        FakePopen.fail = False
        self.backend.bind_job({"id": "test-job", "state": {"transport_retry_generation": 1}}, self.runtime)
        self.backend.complete("rules", [], [], {})
        second = Path(FakePopen.calls[1][1]["cwd"])
        self.assertNotEqual(first, second)
        self.assertEqual(json.loads((first / "receipt.json").read_text())["status"], "uncertain")
        self.assertEqual(json.loads((second / "receipt.json").read_text())["status"], "completed")

    def test_completed_native_trace_is_adopted_before_new_generation(self):
        self.backend.complete("rules", [], [], {})
        first = Path(FakePopen.calls[0][1]["cwd"])
        (first / "receipt.json").write_text('{"status":"uncertain"}')
        self.backend.bind_job({"id": "test-job", "state": {"transport_retry_generation": 1}}, self.runtime)
        self.backend.complete("rules", [], [], {})
        self.assertEqual(len(FakePopen.calls), 1)
        self.assertTrue(json.loads((first / "receipt.json").read_text())["reconciled"])


if __name__ == "__main__":
    unittest.main()
