"""Exercise real Experiment preparation/lifecycle and frozen output, offline."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import asyncio
import os
import shutil
import runpy

PROJECT = Path(__file__).resolve().parents[2]
for source in (PROJECT / "src",):
    sys.path.insert(0, str(source))
from colombo.experiment_cell import controller as runtime
from colombo.cell.settings import load_defaults
from colombo.cell.instructions import read_cell_mode
from colombo.shared.file_io import write_json
from colombo.cell.attempt_archive import freeze_attempt_archive


class ExperimentDispatchTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".test-experiment-", dir=PROJECT)
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.problem = self.base / "problem.md"
        self.problem.write_text("Distinguish candidate rates in the assigned Oracle setting.", encoding="utf-8")
        self.root = self.base / "cell"
        settings, profile = load_defaults()
        settings["agents"]["prover_max_rounds"] = 2
        runtime.initialize(self.problem, self.root, settings_snapshot=settings, profile=profile,
                           research_mode="oracle_complexity", specialization="experiment")

    def report(self):
        return {"summary": "Finite measurements do not distinguish the hypotheses.",
                "actual_scope": "Assigned setting", "method": "Pilot calibration",
                "uncertainty": "Insufficient scale", "measurements": [], "candidate_rates": [],
                "limitations": ["Inconclusive at available scales"], "failures": [],
                "experiment_refs": [], "artifact_paths": [], "outcome": "inconclusive"}

    def test_frozen_target_real_record_and_no_mode_file(self):
        ref = runtime.target_ref(self.root)
        self.assertEqual(ref["kind"], "proof_state")
        self.assertEqual(read_cell_mode(self.root)["specialization"], "experiment")
        self.assertFalse((self.root / "cell_mode.json").exists())
        self.assertIn("Experiment Cell", (self.root / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertTrue((self.root / ".agents/skills/explore/SKILL.md").is_file())

    def test_installed_instructions_have_only_existing_local_links(self):
        from markdown_it import MarkdownIt
        from urllib.parse import unquote, urlsplit
        files = [self.root / "AGENTS.md", self.root / "protocol.md",
                 *(self.root / "skills").rglob("*.md"), *(self.root / ".agents/skills").rglob("*.md")]
        def links(tokens):
            for token in tokens:
                if token.type == "link_open":
                    yield token.attrGet("href")
                if token.children:
                    yield from links(token.children)
        for file in files:
            for href in links(MarkdownIt().parse(file.read_text(encoding="utf-8"))):
                parsed = urlsplit(href)
                if parsed.scheme or not parsed.path:
                    continue
                target = (file.parent / unquote(parsed.path)).resolve()
                with self.subTest(source=str(file.relative_to(self.root)), href=href):
                    self.assertTrue(target.is_relative_to(self.root))
                    self.assertTrue(target.is_file())

    def test_skill_resources_are_installed_in_both_trees_without_eval_fixtures(self):
        source = PROJECT / "agents/experiment_cell/skills"
        for name in ("estimate-epsilon-rate/scripts/gd_family_calibration.py",
                     "probe-mechanism/scripts/quadratic_inequality_probe.py"):
            original = (source / name).read_bytes()
            for prefix in ("skills", ".agents/skills"):
                with self.subTest(path=prefix + "/" + name):
                    self.assertEqual((self.root / prefix / name).read_bytes(), original)
        for prefix in ("skills", ".agents/skills"):
            names = [path.relative_to(self.root / prefix).as_posix() for path in (self.root / prefix).rglob("*")]
            self.assertIn("probe-mechanism/references/quadratic-inequality.md", names)
            self.assertIn("estimate-epsilon-rate/references/gd-family-calibration.md", names)
            self.assertFalse(any("experiment_skill_eval" in name or name.startswith("tests/") for name in names))

    def test_relocated_workspace_runs_its_installed_skill_resource(self):
        relocated = self.base / "relocated task with spaces"
        self.root.rename(relocated)
        ref = runtime.target_ref(relocated)
        self.assertEqual(ref["kind"], "proof_state")
        resource = relocated / "skills/estimate-epsilon-rate/scripts/gd_family_calibration.py"
        module = runpy.run_path(str(resource))
        output = relocated / "working/calibration"
        module["run"]({"mode": "all", "budgets": [0, 1, 4], "epsilons": [0.1], "max_steps": 100}, output)
        actual = json.loads((output / "measurements.json").read_text(encoding="utf-8"))
        self.assertEqual(actual["source"], "actual_gd_rollout")
        self.assertTrue(actual["cases"])
        self.assertTrue(all(case["measurements"] for case in actual["cases"]))

    def test_resume_keeps_installed_resources_after_source_pack_changes(self):
        from colombo.cell import instructions
        source_root = self.base / "source snapshot"
        source = source_root / "agents/experiment_cell"
        shutil.copytree(PROJECT / "agents/experiment_cell", source)
        resumed = self.base / "resume resource task"
        settings, profile = load_defaults()
        settings["agents"]["prover_max_rounds"] = 2
        with patch.object(instructions, "ROOT", source_root):
            runtime.initialize(self.problem, resumed, settings_snapshot=settings, profile=profile,
                               research_mode="oracle_complexity", specialization="experiment")
            with patch.object(runtime, "run_agent", side_effect=RuntimeError("Interrupted researcher")):
                self.assertEqual(runtime.solve(resumed), 2)
            relative = "skills/estimate-epsilon-rate/scripts/gd_family_calibration.py"
            original = (resumed / relative).read_bytes()
            (source / relative).write_text("raise RuntimeError('new source must not be installed on resume')", encoding="utf-8")
            def researcher(*args, **kwargs):
                self.assertEqual((resumed / relative).read_bytes(), original)
                runtime.submit_report(resumed, self.report(), "Fixed inconclusive report after recovery")
            with patch.object(runtime, "run_agent", side_effect=researcher):
                self.assertEqual(runtime.solve(resumed), 0)
            self.assertEqual((resumed / ".agents" / relative).read_bytes(), original)
            self.assertEqual(json.loads((resumed / "runtime/experiment_state.json").read_text())["launches"], 2)

    def test_empirical_submission_cannot_claim_proof_or_fake_observations(self):
        report = self.report()
        for outcome in ("proved", "observations"):
            with self.subTest(outcome=outcome), self.assertRaises(ValueError):
                runtime.submit_report(self.root, {**report, "outcome": outcome}, "Report")
        receipt = runtime.submit_report(self.root, report, "# Report\n\nAn honest inconclusive result.")
        self.assertFalse(receipt["accepted"])
        self.assertEqual(receipt["evidence_kind"], "empirical")
        self.assertEqual(runtime.current_report(self.root), report)
        (self.root / "report.md").write_text("tampered", encoding="utf-8")
        self.assertIsNone(runtime.current_report(self.root))

    def test_runtime_uses_independent_researcher_and_resume_preserves_starts(self):
        with patch.object(runtime, "run_agent", side_effect=RuntimeError("lost transport")) as launch:
            self.assertEqual(runtime.solve(self.root), 2)
            self.assertEqual(runtime.solve(self.root), 2)
            self.assertEqual(runtime.solve(self.root), 2)
        self.assertEqual(launch.call_count, 2)
        self.assertEqual(json.loads((self.root / "runtime/experiment_state.json").read_text())["launches"], 2)

    def test_runtime_returns_report_without_proof_verifier(self):
        def research(*args, **kwargs):
            runtime.submit_report(self.root, self.report(), "Complete empirical report")
            return {"text": "submitted"}
        with patch.object(runtime, "run_agent", side_effect=research) as launch:
            self.assertEqual(runtime.solve(self.root), 0)
            self.assertEqual(runtime.solve(self.root), 0)
        self.assertEqual(launch.call_count, 1)
        self.assertFalse((self.root / "manuscript.md").exists())

    def test_experiment_mcp_mounts_narrow_tools_and_fixed_target(self):
        import importlib.util
        import shutil
        from colombo.cell import model_calls as processes
        spec = importlib.util.spec_from_file_location("test_experiment_mcp_server", PROJECT / "src/colombo/experiment_cell/mcp_server.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        with patch.dict(os.environ, {"CELL_RUN_DIR": str(self.root)}):
            spec.loader.exec_module(module)
        tools = {tool.name: tool for tool in module.mcp._tool_manager.list_tools()}
        self.assertTrue({"run_experiment", "resume_experiment", "submit_report", "job_status"}.issubset(tools))
        self.assertNotIn("submit_proof", tools)
        self.assertNotIn("spawn_task", tools)
        self.assertNotIn("target_ref", tools["run_experiment"].parameters["properties"])
        self.assertFalse(module.submit_report(self.report(), "Empirical report")["accepted"])
        auth = self.base / "fake-auth"
        auth.mkdir()
        (auth / "auth.json").write_text("{}", encoding="utf-8")
        with patch.object(processes, "_user_home", return_value=auth):
            home = processes._prepare_home(self.root, "prover", None, False, {"CELL_RUN_DIR": str(self.root)})
        expected_parent = (PROJECT / ".runtime/cell/codex").resolve()
        self.assertTrue(Path(home).resolve().is_relative_to(expected_parent))
        try:
            config = (home / "config.toml").read_text(encoding="utf-8")
            self.assertIn("experiment_cell", config)
            self.assertNotIn("src/colombo/cell/prover/mcp/server.py", config.replace("\\\\", "/"))
        finally:
            shutil.rmtree(home)

    def test_full_archive_preserves_notes_subcells_and_experiments_across_attempts(self):
        task = self.base / "T0001"
        task.mkdir()
        files = {"draft.md": "old proof", "tasks/child/workspace/notes.md": "child reasoning",
                 "experiments/exp-x/code.py": "print(1)", "reviews/review/progress.md": "review reasoning",
                 "auth.json": "credential", ".codex/auth.json": "credential"}
        for name, value in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value, encoding="utf-8")
        def archive(attempt):
            folder = task / "results" / attempt
            folder.mkdir(parents=True)
            def copy(source, kind):
                dest = folder / "artifacts" / source.relative_to(self.root)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(source.read_bytes())
            return freeze_attempt_archive(self.root, folder, task, copy)[0]
        first = archive("A0001")
        original = (task / first["path"]).read_bytes()
        (self.root / "draft.md").write_text("new proof", encoding="utf-8")
        second = archive("A0002")
        self.assertEqual((task / first["path"]).read_bytes(), original)
        with zipfile.ZipFile(task / first["path"]) as result:
            self.assertEqual(result.read("draft.md"), b"old proof")
            self.assertIn("tasks/child/workspace/notes.md", result.namelist())
            self.assertIn("experiments/exp-x/code.py", result.namelist())
            self.assertNotIn("auth.json", result.namelist())
            self.assertNotIn(".codex/auth.json", result.namelist())
        self.assertNotEqual(first["sha256"], second["sha256"])

    def test_real_worker_prepares_experiment_and_exports_empirical_attempt(self):
        from colombo.brain.cell_dispatch import CellAdapter
        from colombo.cell import worker as cell_worker
        task = self.base / "T-real"
        package = task / "input/package"
        package.mkdir(parents=True)
        (task / "input/problem.md").write_bytes(self.problem.read_bytes())
        (package / "README.md").write_text("Fixed experiment materials", encoding="utf-8")
        write_json(package / "manifest.json", {"items": []})
        config = json.loads((self.root / "run.json").read_text(encoding="utf-8"))
        adapter = CellAdapter(PROJECT, {"cell": {"settings": config["settings"],
            "profile": config["profile"], "run_timeout_seconds": "unlimited"}})
        refs = {"assignment_ref": {"id": "assignment-real", "revision": 1},
                "package_ref": {"id": "package-real", "revision": 1}}
        adapter.prepare(task, {"task_id": task.name, "research_mode": "oracle_complexity",
                             "spec": {"specialization": "experiment"}}, package, **refs)
        self.assertEqual(runtime.target_ref(task / "cell")["kind"], "proof_state")
        request = {"task_dir": str(task), "project_root": str(PROJECT), "task_id": task.name,
                   "attempt_id": "A0001", "config": adapter.config, **refs}
        request_path = task / "attempts/A0001/request.json"
        write_json(request_path, request)
        def research(*args, **kwargs):
            runtime.submit_report(task / "cell", self.report(), "Full empirical report")
            return {"text": "submitted"}
        with patch.object(runtime, "run_agent", side_effect=research):
            self.assertEqual(cell_worker.solve(request_path), 0)
        result = cell_worker.export_result(request_path, "finished", "test")
        self.assertEqual(result["execution_status"], "finished")
        self.assertEqual(result["evidence_kind"], "empirical")
        self.assertEqual(result["review_status"], "pending")
        self.assertFalse(result["accepted"])
        self.assertTrue((task / result["archive"]["path"]).is_file())
        self.assertTrue(any(a["path"].endswith("/report.md") for a in result["artifacts"]))


if __name__ == "__main__":
    unittest.main()
