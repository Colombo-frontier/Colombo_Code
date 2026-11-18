"""The public config command resolves parameters without creating research state."""
from contextlib import redirect_stdout, redirect_stderr
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from colombo import system_commands as cli
from colombo.configuration import PROJECT_ROOT, load_config
from test_unified_config import toml_document
import tomllib


class ConfigurationPreviewTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        temporary_root = PROJECT_ROOT / "validation/tmp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="config-preview-", dir=temporary_root)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_preview_reports_resolved_profile_and_integration_budget_without_store(self):
        selected = self.root / "config.toml"
        document = tomllib.loads((PROJECT_ROOT / "config.toml").read_text(encoding="utf-8-sig"))
        document["profile"] = "standard"
        document["integration"]["timeout_seconds"] = 25200
        selected.write_text(toml_document(document), encoding="utf-8")
        expected = load_config(selected)
        stream = io.StringIO()
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        with patch.object(cli, "Store", side_effect=AssertionError("preview must not open a Store")), redirect_stdout(stream):
            self.assertEqual(cli.main(["config", "--config", str(selected)]), 0)
        response = json.loads(stream.getvalue())
        self.assertFalse(response["creates_run"])
        self.assertEqual(response["effective_config"], expected)
        effective = response["effective_config"]
        self.assertEqual(effective["profile"], "standard")
        self.assertEqual(effective["integration"]["timeout_seconds"], 25200)
        self.assertNotIn("budget", effective)
        self.assertEqual(effective["cell"]["run_timeout_seconds"], "unlimited")
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_invalid_preview_rejects_without_opening_store(self):
        path = self.root / "bad.toml"
        path.write_text('[cell]\ntimeout_seconds=9\n', encoding="utf-8")
        error = io.StringIO()
        with patch.object(cli, "Store", side_effect=AssertionError("must not open Store")), redirect_stderr(error):
            self.assertEqual(cli.main(["config", "--config", str(path)]), 2)
        self.assertIn("complete outer config", error.getvalue())
        self.assertEqual([p.name for p in self.root.iterdir()], ["bad.toml"])

    def test_actual_cli_preview_has_no_run_artifacts_or_model_launch(self):
        before = set(self.root.iterdir())
        completed = subprocess.run([sys.executable, "-B", "-X", "utf8", str(PROJECT_ROOT / "run.py"), "config"],
                                   cwd=self.root, capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["mode"], "preview_only")
        self.assertEqual(result["effective_config"], load_config())
        self.assertEqual(result["effective_config"]["brain"]["timeout_seconds"], "unlimited")
        self.assertEqual(result["effective_config"]["brain"]["reasoning_effort"], "ultra")
        self.assertEqual(result["effective_config"]["cell"]["settings"]["model"]["reasoning_effort"], "ultra")
        self.assertEqual(result["effective_config"]["cell"]["settings"]["experiment"]["reasoning_effort"], "max")
        self.assertEqual(before, set(self.root.iterdir()))
