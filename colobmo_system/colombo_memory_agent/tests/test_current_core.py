"""Entrypoints and generated queries share the parent system core and Store."""
import contextlib
import io
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "tools"))
from _agent_bootstrap import CORE_ROOT, DEFAULT_MEMORY_ROOT
from colombo.memory.integration import DEFAULT_MEMORY_ROOT as READER_ROOT
from colombo.project_paths import PROJECT_ROOT
from colombo_memory_agent import cli
from colombo_memory_agent.store import WriterStore
from colombo_memory_agent.workflow import Workflow


class CurrentCoreTests(unittest.TestCase):
    def test_writer_and_reader_default_to_same_current_store(self):
        expected = PACKAGE.parent
        self.assertEqual(CORE_ROOT, expected)
        self.assertEqual(PROJECT_ROOT, expected)
        self.assertEqual(DEFAULT_MEMORY_ROOT, expected / "long_term_memory")
        self.assertEqual(DEFAULT_MEMORY_ROOT, READER_ROOT)
        with patch.object(cli, "Store") as store, contextlib.redirect_stdout(io.StringIO()):
            store.return_value.initialize.return_value = {"test_only": True}
            self.assertEqual(cli.main(["init"]), 0)
            store.assert_called_once_with(DEFAULT_MEMORY_ROOT)

    @unittest.skipUnless(sys.platform != "win32", "POSIX command execution")
    def test_generated_query_uses_current_core_without_writing_store(self):
        with tempfile.TemporaryDirectory(prefix="memory current core ") as directory:
            root = Path(directory)
            store = WriterStore(root / "memory")
            store.initialize()
            before = {path.relative_to(root): path.read_bytes()
                      for path in root.rglob("*") if path.is_file()}
            workflow = Workflow(store, None, PACKAGE)
            prompt = workflow._role_prompt("curator", {}, root / "job", "")
            line = next(line for line in prompt.splitlines() if line.startswith("Use the read-only query command: "))
            command = line.removeprefix("Use the read-only query command: ").removesuffix(" '<JSON request>'.")
            arguments = shlex.split(command)
            self.assertEqual(Path(arguments[2]), CORE_ROOT / "tools/memory/query_memory.py")
            result = subprocess.run([*arguments, json.dumps({"mode": "overview"})],
                                    cwd=root, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(sum(json.loads(result.stdout)["counts"].values()), 0)
            self.assertEqual(before, {path.relative_to(root): path.read_bytes()
                                      for path in root.rglob("*") if path.is_file()})

    def test_nested_entrypoints_work_from_an_unrelated_directory(self):
        with tempfile.TemporaryDirectory(prefix="memory entrypoint cwd ") as directory:
            root = Path(directory)
            cli_result = subprocess.run(
                [sys.executable, "-E", "-B", str(PACKAGE / "run.py"), "--help"],
                cwd=root, capture_output=True, text=True, timeout=30)
            self.assertEqual(cli_result.returncode, 0, cli_result.stderr)
            self.assertIn("publish", cli_result.stdout)
            doctor_result = subprocess.run(
                [sys.executable, "-E", "-B", str(PACKAGE / "tools/doctor.py")],
                cwd=root, capture_output=True, text=True, timeout=30)
            self.assertEqual(doctor_result.returncode, 0, doctor_result.stderr)
            result = json.loads(doctor_result.stdout)
            self.assertEqual(Path(result["store"]["root"]), DEFAULT_MEMORY_ROOT)
            self.assertFalse(result["model_called"])
            self.assertEqual(list(root.iterdir()), [])

    def test_privacy_export_loads_the_nested_writer_from_an_unrelated_directory(self):
        with tempfile.TemporaryDirectory(prefix="memory projection cwd ") as directory:
            root = Path(directory)
            source = root / "source" / "long_term_memory"
            store = WriterStore(source)
            store.initialize()
            store.install_leads([])
            before = {path.relative_to(source.parent): path.read_bytes()
                      for path in source.parent.rglob("*") if path.is_file()}
            result = subprocess.run(
                [sys.executable, "-I", "-B",
                 str(CORE_ROOT / "tools/memory/export_privacy_projection.py"),
                 "--component-repo", str(CORE_ROOT),
                 "--live-memory-root", str(source),
                 "--output-root", str(root / "projected"),
                 "--report-path", str(root / "report.json")],
                cwd=root, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "passed")
            self.assertEqual(report["model_calls"], 0)
            self.assertEqual(before, {path.relative_to(source.parent): path.read_bytes()
                                      for path in source.parent.rglob("*") if path.is_file()})


if __name__ == "__main__":
    unittest.main()
