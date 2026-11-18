"""Entrypoint bootstraps and installed instruction packs from an unrelated cwd."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class LayoutEntrypointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cwd = Path(self.temp.name)
        self.env = {key: value for key, value in os.environ.items()
                    if key != "PYTHONPATH" and not key.startswith("CELL_")}
        self.env.update(PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")

    def execute(self, *args):
        result = subprocess.run([sys.executable, "-B", *map(str, args)],
            cwd=self.cwd, env=self.env, capture_output=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_brain_and_standalone_cell_entrypoints_bootstrap_without_cwd_imports(self):
        preview = json.loads(self.execute(ROOT / "run.py", "config"))
        self.assertEqual(preview["effective_config"]["workflow"]["version"], 3)
        self.assertFalse(preview["creates_run"])
        help_text = self.execute(ROOT / "run_cell.py", "--help")
        self.assertIn("--specialization", help_text)
        self.assertIn("--resume", help_text)
        self.assertEqual(list(self.cwd.iterdir()), [])

    def test_cell_initialization_installs_split_instruction_packs_without_models(self):
        problem = self.cwd / "problem.md"
        problem.write_text("Establish the assigned Oracle Complexity rate.", encoding="utf-8")
        script = """
import pathlib, sys
sys.path.insert(0, sys.argv[1])
from colombo.cell.controller import initialize
from colombo.cell.settings import load_defaults
settings, profile = load_defaults()
for role in ('general', 'upper_bound', 'lower_bound'):
    initialize(pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]) / role,
               settings_snapshot=settings, profile=profile,
               research_mode='oracle_complexity', specialization=role)
"""
        self.execute("-c", script, ROOT / "src", problem, self.cwd)
        for role in ("general", "upper_bound", "lower_bound"):
            work = self.cwd / role
            source = ROOT / "agents/cell" / ("prover" if role == "general" else role)
            self.assertEqual((work / "AGENTS.md").read_bytes(), (source / "AGENTS.md").read_bytes())
            self.assertTrue((work / ".agents/skills/prove/SKILL.md").is_file())
            self.assertTrue((work / ".agents/skills/handoff/SKILL.md").is_file())
            mode = json.loads((work / "run.json").read_text(encoding="utf-8"))["cell_mode"]
            self.assertEqual(mode["specialization"], role)
            self.assertFalse((work / "runtime/processes").exists())
