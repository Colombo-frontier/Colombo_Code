"""One-way launcher boundaries using fake models and real Agent orchestration."""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from colombo.downstream import launcher
from colombo.downstream.handoff import digest
from test_writing_agent import package_fixture, lean_fixture, manuscript_fixture, FakeModel as WritingModel


class LeanModel:
    def __init__(self, package):
        self.package = package
        self.calls = []

    def invoke(self, stage, work_dir, prompt, context, schema, timeout_seconds):
        self.calls.append({"stage": stage, "context": copy.deepcopy(context)})
        if stage == "lean-check":
            return {"status": "candidate", "proof_sha256": self.package["proof_sha256"],
                "source": "theorem main_sum : True := True.intro\ntheorem sum_step : True := True.intro\n",
                "mapping": copy.deepcopy(lean_fixture(self.package)["mapping"]), "limitations": []}
        if stage == "lean-review":
            return copy.deepcopy(lean_fixture(self.package)["semantic_review"])
        raise AssertionError("Unexpected Lean stage " + stage)


class LauncherTests(unittest.TestCase):
    def setUp(self):
        parent = PROJECT / ".runtime"
        parent.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="launcher-test-", dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.output = self.root / "downstream"
        self.package = package_fixture()
        self.config = launcher.load_config()
        self.template = self.root / "template"
        self.template.mkdir()
        (self.template / "lean-toolchain").write_text("leanprover/lean4:v4.19.0", encoding="utf-8")
        (self.template / "lakefile.toml").write_text('name = "formalization"', encoding="utf-8")
        self.config["lean"]["lean_project"] = str(self.template)
        self.lean_model = LeanModel(self.package)
        self.writer = WritingModel(manuscript_fixture(self.package))
        self.compiler_calls = 0

    def compile(self, project, names, **kwargs):
        self.compiler_calls += 1
        return {"status": "passed", "diagnostics": [], "declarations": names,
            "source_sha256": hashlib.sha256((project / "Main.lean").read_bytes()).hexdigest(),
            "axioms": {name: [] for name in names}, "declaration_printout": "simulated compiler theorem evidence"}

    def execute(self):
        with patch("colombo.lean_agent.agent.verify_lean", side_effect=self.compile):
            return launcher.run(self.package, self.output, self.config,
                                lean_model=self.lean_model, writing_model=self.writer)

    def main(self, arguments, **patches):
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(launcher, "load_config", return_value=copy.deepcopy(self.config)))
            for name, replacement in patches.items():
                stack.enter_context(patch.object(launcher, name, replacement))
            stdout, stderr = io.StringIO(), io.StringIO()
            stack.enter_context(contextlib.redirect_stdout(stdout))
            stack.enter_context(contextlib.redirect_stderr(stderr))
            code = launcher.main(arguments)
        return code, stdout.getvalue(), stderr.getvalue()

    def input_file(self, name="input.json"):
        path = self.root / name
        path.write_text(json.dumps(self.package), encoding="utf-8")
        return path

    def test_disabled_never_validates_package_calls_models_or_creates_files(self):
        self.config["enabled"] = False
        with patch.object(launcher, "validate_package", side_effect=AssertionError("unexpected validation")), \
                patch.object(launcher, "NativeModel", side_effect=AssertionError("unexpected native model")):
            self.assertEqual(launcher.run(None, self.output, self.config), {"status": "disabled"})
        self.assertFalse(self.output.exists())

    def test_lean_failure_never_starts_writing(self):
        with patch("colombo.lean_agent.agent.run", return_value={"status": "failed"}) as lean, \
                patch("colombo.writing_agent.agent.run") as writing:
            report = launcher.run(self.package, self.output, self.config,
                                  lean_model=self.lean_model, writing_model=self.writer)
        self.assertEqual(report["lean_status"], "failed")
        self.assertEqual(report["writing_status"], "skipped")
        self.assertEqual(report["status"], "failed")
        self.assertEqual(lean.call_args.args[0], self.package)
        writing.assert_not_called()

    def test_success_hands_the_exact_frozen_package_and_lean_evidence_to_writer(self):
        before = copy.deepcopy(self.package)
        report = self.execute()
        self.assertEqual(report["status"], "completed", report)
        self.assertEqual(report["writing_status"], "draft")
        self.assertEqual(self.package, before)
        self.assertEqual(json.loads((self.output / "handoff.json").read_text()), before)
        context = self.writer.calls[0]["context"]
        self.assertEqual({key: context[key] for key in before}, before)
        self.assertEqual(context["lean_result"]["status"], "passed")
        self.assertEqual(context["lean_result"]["semantic_review"]["checked_claim_ids"], before["required_claim_ids"])
        self.assertEqual(self.compiler_calls, 1)
        self.assertEqual([c["stage"] for c in self.lean_model.calls], ["lean-check", "lean-review"])
        self.assertTrue((self.output / "writing/manuscript.tex").is_file())

    def test_replay_reuses_results_and_changed_config_cannot_rebind_outputs(self):
        report = self.execute()
        calls = (len(self.lean_model.calls), len(self.writer.calls), self.compiler_calls)
        binding = (self.output / "binding.json").read_bytes()
        handoff = (self.output / "handoff.json").read_bytes()
        self.assertEqual(self.execute(), report)
        self.assertEqual((len(self.lean_model.calls), len(self.writer.calls), self.compiler_calls), calls)
        self.config["lean"]["max_compile_attempts"] += 1
        with self.assertRaisesRegex(ValueError, "changed inputs/configuration"):
            self.execute()
        self.assertEqual((self.output / "binding.json").read_bytes(), binding)
        self.assertEqual((self.output / "handoff.json").read_bytes(), handoff)
        self.assertEqual((len(self.lean_model.calls), len(self.writer.calls), self.compiler_calls), calls)

    def test_writing_can_be_disabled_without_disabling_lean(self):
        self.config["writing_enabled"] = False
        report = self.execute()
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["writing_status"], "skipped")
        self.assertEqual(self.writer.calls, [])
        self.assertFalse((self.output / "writing").exists())

    def test_explicit_writing_stage_respects_disable_without_calls_or_files(self):
        self.config["writing_enabled"] = False
        with patch.object(launcher, "validate_package", side_effect=AssertionError("unexpected validation")), \
                patch.object(launcher, "NativeModel", side_effect=AssertionError("unexpected native model")):
            result = launcher.run(None, self.output, self.config, stage="writing")
        self.assertEqual(result, {"status": "disabled"})
        self.assertFalse(self.output.exists())

    def test_separate_lean_then_writing_stages_share_exact_binding_without_rerunning_lean(self):
        with patch("colombo.lean_agent.agent.verify_lean", side_effect=self.compile):
            lean_summary = launcher.run(self.package, self.output, self.config, stage="lean",
                                       lean_model=self.lean_model, writing_model=self.writer)
        self.assertEqual(lean_summary["status"], "passed")
        self.assertEqual(self.writer.calls, [])
        binding = (self.output / "binding.json").read_bytes()
        lean = json.loads((self.output / "lean/result.json").read_text())
        with patch("colombo.lean_agent.agent.run", side_effect=AssertionError("must not rerun Lean")):
            result = launcher.run(self.package, self.output, self.config, stage="writing", lean_result=lean,
                                  writing_model=self.writer)
        self.assertEqual(result["status"], "completed")
        self.assertEqual((self.output / "binding.json").read_bytes(), binding)
        self.assertEqual(self.writer.calls[0]["context"]["lean_result"], lean)

    def test_unknown_stage_does_not_create_output(self):
        with self.assertRaisesRegex(ValueError, "Unknown downstream stage"):
            launcher.run(self.package, self.output, self.config, stage="unrecognized")
        self.assertFalse(self.output.exists())

    def test_output_with_orphan_files_is_not_adopted(self):
        self.output.mkdir()
        sentinel = self.output / "unrelated.txt"
        sentinel.write_text("preserve me", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "new or have a matching"):
            self.execute()
        self.assertEqual(sentinel.read_text(), "preserve me")
        self.assertEqual(self.lean_model.calls, [])

    def test_cli_rejects_outputs_inside_or_above_brain_run_before_handoff(self):
        brain = self.root / "brain/run"
        brain.mkdir(parents=True)
        marker = brain / "state.sqlite"
        marker.write_bytes(b"untouched")
        for output in [brain, brain / "downstream", brain.parent]:
            with self.subTest(output=output), patch.object(launcher, "from_brain_run") as read:
                code, _, error = self.main(["--brain-run", str(brain), "--output-dir", str(output)])
                self.assertEqual(code, 2)
                self.assertIn("separate from the Brain run", error)
                read.assert_not_called()
        self.assertEqual(marker.read_bytes(), b"untouched")
        self.assertEqual(list(brain.iterdir()), [marker])

    def test_cli_default_output_is_outside_brain_run(self):
        brain = self.root / "brain/run"
        brain.mkdir(parents=True)
        with patch.object(launcher, "PROJECT", self.root), \
                patch.object(launcher, "from_brain_run", return_value=self.package), \
                patch.object(launcher, "run", return_value={"status": "passed"}) as run:
            code, _, error = self.main(["--brain-run", str(brain)])
        self.assertEqual(code, 0, error)
        self.assertEqual(run.call_args.args[1], self.root / "downstream_runs/run")
        self.assertFalse(run.call_args.args[1].is_relative_to(brain))

    def test_cli_lean_stage_never_calls_writer(self):
        path = self.input_file()
        with patch("colombo.lean_agent.agent.run", return_value=lean_fixture(self.package)) as lean, \
                patch("colombo.writing_agent.agent.run") as writer:
            code, _, error = self.main(["--input", str(path), "--output-dir", str(self.output), "--stage", "lean"])
        self.assertEqual(code, 0, error)
        self.assertEqual(lean.call_args.args[0], self.package)
        self.assertEqual(lean.call_args.args[1], self.output / "lean")
        writer.assert_not_called()

    def test_cli_writing_stage_uses_supplied_lean_result_without_lean_invocation(self):
        path = self.input_file()
        lean_result = self.root / "lean-result.json"
        lean = lean_fixture(self.package)
        lean_result.write_text(json.dumps(lean), encoding="utf-8")
        before = lean_result.read_bytes()
        with patch("colombo.lean_agent.agent.run") as lean_agent, \
                patch("colombo.writing_agent.agent.run", return_value={"status": "draft", "proof_sha256": self.package["proof_sha256"]}) as writer:
            code, _, error = self.main(["--input", str(path), "--output-dir", str(self.output),
                "--stage", "writing", "--lean-result", str(lean_result)])
        self.assertEqual(code, 0, error)
        self.assertEqual(writer.call_args.args[:2], (self.package, lean))
        self.assertEqual(writer.call_args.args[2], self.output / "writing")
        self.assertEqual(lean_result.read_bytes(), before)
        lean_agent.assert_not_called()

    def test_cli_writing_requires_explicit_lean_result(self):
        path = self.input_file()
        with patch("colombo.writing_agent.agent.run") as writer:
            code, _, error = self.main(["--input", str(path), "--output-dir", str(self.output), "--stage", "writing"])
        self.assertEqual(code, 2)
        self.assertIn("requires --lean-result", error)
        writer.assert_not_called()

    def test_brain_passthrough_rejects_conflicting_or_duplicate_run_directories(self):
        brain = self.root / 'brain'
        other = self.root / 'other'
        for extra in [['--run-dir='+str(other)], ['--run-dir',str(brain),'--run-dir',str(other)],
                      ['--run-dir',str(brain),'--run-dir='+str(brain)]]:
            with self.subTest(extra=extra), patch.object(launcher.subprocess,'run') as launch:
                code, _, error = self.main(['--brain-run',str(brain),'--','resume',*extra])
                self.assertEqual(code,2,error)
                launch.assert_not_called()

    def test_brain_passthrough_supplies_exact_run_directory_and_stops_on_failure(self):
        brain = self.root / 'brain'
        with patch.object(launcher.subprocess,'run',return_value=type('Exit',(),{'returncode':2})()) as launch, \
                patch.object(launcher,'from_brain_run') as read:
            code, _, _ = self.main(['--brain-run',str(brain),'--','resume'])
            self.assertEqual(code,2)
            self.assertEqual(launch.call_args.args[0][-2:],['--run-dir',str(brain)])
            read.assert_not_called()

    def test_standalone_lean_rejects_rebinding_without_overwriting_frozen_handoff(self):
        path = self.input_file()
        arguments = ["--input", str(path), "--output-dir", str(self.output), "--stage", "lean"]
        with patch.object(launcher, "NativeModel", return_value=self.lean_model), \
                patch("colombo.lean_agent.agent.verify_lean", side_effect=self.compile):
            code, _, error = self.main(arguments)
            self.assertEqual(code, 0, error)
            original = (self.output / "handoff.json").read_bytes()
            changed = copy.deepcopy(self.package)
            changed["proof"]["title"] += " changed"
            changed["proof_sha256"] = digest(changed["proof"])
            changed["brain_check"]["proof_sha256"] = changed["proof_sha256"]
            path.write_text(json.dumps(changed), encoding="utf-8")
            code, _, error = self.main(arguments)
        self.assertEqual(code, 2)
        self.assertEqual((self.output / "handoff.json").read_bytes(), original,
                         "Rejected standalone rebind must not overwrite the original handoff")


if __name__ == "__main__":
    unittest.main()
