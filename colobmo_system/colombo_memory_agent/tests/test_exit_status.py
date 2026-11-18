"""CLI regressions use isolated Stores and synthetic model responses only."""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(PACKAGE / "tests"), str(PACKAGE / "tools")]
from _agent_bootstrap import CORE_ROOT
from colombo.memory.contracts import ContractError
from colombo_memory_agent import cli
from colombo_memory_agent.store import Store
from test_handoff import FakeBackend


class ExitStatusTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="memory-exit-status-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.memory = self.root / "memory"
        self.store = Store(self.memory)
        self.store.initialize()
        source = self.root / "source.txt"
        source.write_text("Synthetic protocol source; not a scientific review.", encoding="utf-8")
        self.job_file = self.root / "job.json"
        self.job_file.write_text(json.dumps({
            "job_id": "exit-status", "objective": "Synthetic protocol check",
            "source_files": [str(source)], "focus_anchors": ["synthetic"],
            "publication_policy": "stage_only", "max_rounds": 1,
        }), encoding="utf-8")

    def arguments(self):
        return ["--root", str(self.memory), "run-job", str(self.job_file),
                "--jobs-root", str(self.root / "jobs")]

    def run_cli(self, backend):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch("colombo_memory_agent.backend.CodexBackend", return_value=backend), \
                redirect_stdout(stdout), redirect_stderr(stderr):
            code = cli.main(self.arguments())
        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_exhausted_candidate_repair_returns_nonzero_and_preserves_diagnostics(self):
        backend = FakeBackend()
        with patch.object(backend, "run", side_effect=ContractError("Synthetic invalid candidate")):
            code, result, stderr = self.run_cli(backend)
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "budget_exhausted")
        self.assertFalse(result["published"])
        self.assertIn("Synthetic invalid candidate", result["feedback"]["error"])
        self.assertEqual(stderr, "")
        self.assertEqual(self.store.manifest()["entries"], {})

    def test_successful_stage_only_job_returns_zero_without_publication(self):
        backend = FakeBackend()
        code, result, stderr = self.run_cli(backend)
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "completed")
        self.assertIsNone(result["receipt"])
        self.assertEqual([call["role"] for call in backend.calls], ["curator", "reviewer"])
        self.assertEqual(self.store.manifest()["entries"], {})
        self.assertEqual(stderr, "")

    def test_valid_deferred_outcome_remains_a_successful_command(self):
        code, result, stderr = self.run_cli(FakeBackend(decision="defer"))
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "completed_with_deferred_items")
        self.assertIsNone(result["receipt"])
        self.assertEqual(stderr, "")
        self.assertEqual(self.store.manifest()["entries"], {})

    def test_unrecognized_job_outcome_is_not_reported_as_success(self):
        stdout = io.StringIO()
        with patch("colombo_memory_agent.workflow.Workflow.run", return_value={"status": "failed"}), \
                redirect_stdout(stdout):
            code = cli.main(self.arguments())
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(stdout.getvalue()), {"status": "failed"})

    def test_non_job_init_keeps_success_exit_status(self):
        stdout = io.StringIO()
        root = self.root / "other-memory"
        with redirect_stdout(stdout):
            code = cli.main(["--root", str(root), "init"])
        self.assertEqual(code, 0)
        self.assertIsInstance(json.loads(stdout.getvalue()), dict)
        self.assertEqual({path.name for path in root.iterdir()}, {
            "algorithm_family_library", "hard_family_library", "theorem_library", "source"
        })

    def test_real_entrypoint_propagates_failed_job_exit_status(self):
        # A missing executable exercises Backend -> Workflow -> CLI -> SystemExit,
        # with no model process, network request, or user configuration changes.
        command = [sys.executable, "-B", str(PACKAGE / "run.py"), *self.arguments(),
                   "--codex", str(self.root / "codex-does-not-exist")]
        result = subprocess.run(command, capture_output=True, text=True,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=30)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, "")
        payload = json.loads(result.stderr)
        self.assertEqual(payload["type"], "BackendTransportError")
        self.assertIn("Codex CLI not found", payload["error"])
        checkpoint = json.loads((self.root / "jobs/exit-status/checkpoint.json").read_text())
        self.assertEqual(checkpoint["status"], "curating")
        self.assertEqual(checkpoint["round"], 1)
        self.assertEqual(self.store.manifest()["entries"], {})


if __name__ == "__main__":
    unittest.main()
