"""Compiler evidence is mandatory, axiom honest, and tied to unchanged source."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from colombo.lean_agent.compiler import _run, verify_lean


class LeanCheckTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "Main.lean").write_text("theorem result : True := True.intro\n", encoding="utf-8")
        (self.root / "lean-toolchain").write_text("leanprover/lean4:v4.19.0\n", encoding="utf-8")
        (self.root / "lakefile.toml").write_text('name = "formalization"\n', encoding="utf-8")
        self.audit = "theorem result : True := True.intro\n'result' does not depend on any axioms\n"
        self.failure = None
        self.timeout = None
        self.exit_unconfirmed = None
        self.create_object = True
        self.mutate = False
        self.calls = []

    def fake_run(self, root, logs, label, arguments, deadline):
        self.calls.append((label, arguments))
        if label == "compile" and self.create_object:
            (root / ".lake/build/lib/lean/Main.olean").write_bytes(b"compiled")
        if label == "audit" and self.mutate:
            (root / "Main.lean").write_text("theorem changed : True := True.intro", encoding="utf-8")
        return {"argv": arguments, "returncode": 1 if label == self.failure else 0,
                "stdout": "Lean (version 4.19.0, release)" if label == "version" else self.audit if label == "audit" else "",
                "stderr": "", "timed_out": label == self.timeout,
                "process_tree_terminated": label != self.exit_unconfirmed}

    def verify(self, declarations=None):
        with patch("colombo.lean_agent.compiler.shutil.which", return_value="lake"), \
                patch("colombo.lean_agent.compiler._run", side_effect=self.fake_run):
            return verify_lean(self.root, ["result"] if declarations is None else declarations)

    def test_success_keeps_real_evidence_and_does_not_certify_semantics(self):
        report = self.verify()
        self.assertEqual(report["status"], "passed", report)
        self.assertEqual(report["axioms"], {"result": []})
        self.assertEqual(report["semantic_correspondence"], "not_checked")
        self.assertEqual([c[0] for c in self.calls], ["version", "compile", "audit"])
        self.assertIn("#print result", (Path(report["evidence_dir"]) / "Audit.lean").read_text())
        self.assertEqual(json.loads((Path(report["evidence_dir"]) / "report.json").read_text())["status"], "passed")

    def test_standard_axioms_accepted_for_every_declaration(self):
        self.audit += "theorem Other.second : True := True.intro\n'Other.second' depends on axioms: [propext,\n Classical.choice, Quot.sound]\n"
        report = self.verify(["result", "Other.second"])
        self.assertEqual(report["status"], "passed", report)
        self.assertEqual(report["axioms"]["Other.second"], ["propext", "Classical.choice", "Quot.sound"])

    def test_definition_of_proposition_is_not_a_proved_theorem(self):
        self.audit = "def result : Prop := False\n'result' does not depend on any axioms\n"
        report = self.verify()
        self.assertEqual(report["status"], "failed")
        self.assertIn("not a proved theorem", report["diagnostics"][0])

    def test_placeholders_custom_axioms_and_meta_execution_rejected_before_launch(self):
        for token in ["sorry", "admit", "sorryAx", "axiom", "unsafe", "macro", "elab",
                      "run_tac", "run_meta", "native_decide", "initialize", "#eval", "@[implemented_by other]"]:
            with self.subTest(token=token):
                self.calls.clear()
                (self.root / "Main.lean").write_text("theorem result : True := by " + token, encoding="utf-8")
                self.assertEqual(self.verify()["status"], "failed")
                self.assertEqual(self.calls, [])

    def test_comments_do_not_create_false_placeholder_failures(self):
        (self.root / "Main.lean").write_text("/- no sorry /- nested admit -/ here -/\n"
                                            "theorem result : True := True.intro -- no axiom\n", encoding="utf-8")
        self.assertEqual(self.verify()["status"], "passed")

    def test_unapproved_transitive_axioms_rejected(self):
        for axiom in ["sorryAx", "custom_assumption", "result._native.native_decide.ax_1_1"]:
            with self.subTest(axiom=axiom):
                self.audit = f"theorem result : True := True.intro\n'result' depends on axioms: [{axiom}]\n"
                report = self.verify()
                self.assertEqual(report["status"], "failed")
                self.assertIn("Unapproved axioms", report["diagnostics"][0])

    def test_compiler_exit_zero_without_axiom_evidence_fails(self):
        self.audit = "theorem result : True := True.intro\n"
        self.assertEqual(self.verify()["status"], "failed")

    def test_duplicated_axiom_evidence_fails(self):
        self.audit += "'result' does not depend on any axioms\n"
        self.assertEqual(self.verify()["status"], "failed")

    def test_empty_duplicate_or_injectable_declaration_names_fail(self):
        for names in [[], ["result", "result"], ["result\n#eval 1"], ["result; exit"], "result"]:
            with self.subTest(names=names):
                self.assertEqual(self.verify(names)["status"], "failed")
        self.assertEqual(self.calls, [])

    def test_failure_timeout_and_unknown_exit_never_pass(self):
        for field in ["failure", "timeout", "exit_unconfirmed"]:
            for label in ["version", "compile", "audit"]:
                with self.subTest(field=field, label=label):
                    setattr(self, field, label)
                    self.assertEqual(self.verify()["status"], "failed")
                    setattr(self, field, None)

    def test_stale_object_cannot_replace_actual_compilation(self):
        output = self.root / ".lake/build/lib/lean/Main.olean"
        output.parent.mkdir(parents=True)
        output.write_bytes(b"stale")
        self.create_object = False
        report = self.verify()
        self.assertEqual(report["status"], "failed")
        self.assertIn("did not produce", report["diagnostics"][0])

    def test_source_mutation_invalidates_build(self):
        self.mutate = True
        report = self.verify()
        self.assertEqual(report["status"], "failed")
        self.assertIn("inputs changed", report["diagnostics"][0])

    def test_missing_lake_is_blocked(self):
        with patch("colombo.lean_agent.compiler.shutil.which", return_value=None):
            self.assertEqual(verify_lean(self.root, ["result"])["status"], "blocked")

    def test_elan_proxy_uses_run_without_implicit_install(self):
        binary = self.root / "bin/lake.exe"
        binary.parent.mkdir()
        binary.write_bytes(b"proxy")
        (binary.parent / "elan.exe").write_bytes(b"elan")
        with patch("colombo.lean_agent.compiler.shutil.which", return_value=str(binary)), \
                patch("colombo.lean_agent.compiler._run", side_effect=self.fake_run):
            report = verify_lean(self.root, ["result"])
        self.assertEqual(report["status"], "passed", report)
        self.assertEqual(self.calls[0][1][1:4], ["run", "leanprover/lean4:v4.19.0", "lake"])
        self.assertNotIn("--install", self.calls[0][1])

    def test_version_must_match_pin(self):
        (self.root / "lean-toolchain").write_text("leanprover/lean4:v4.20.0", encoding="utf-8")
        self.assertEqual(self.verify()["status"], "failed")

    def test_floating_toolchain_and_executable_lake_config_fail(self):
        (self.root / "lean-toolchain").write_text("leanprover/lean4:stable", encoding="utf-8")
        self.assertEqual(self.verify()["status"], "failed")
        (self.root / "lean-toolchain").write_text("leanprover/lean4:v4.19.0", encoding="utf-8")
        (self.root / "lakefile.toml").unlink()
        (self.root / "lakefile.lean").write_text('import Lake\nopen Lake DSL\npackage formalization\n#eval IO.println "bad"', encoding="utf-8")
        self.assertEqual(self.verify()["status"], "failed")

    def test_simple_declarative_lean_configuration_is_supported(self):
        (self.root / "lakefile.toml").unlink()
        (self.root / "lakefile.lean").write_text("import Lake\nopen Lake DSL\npackage formalization where\nlean_lib Main where\n", encoding="utf-8")
        self.assertEqual(self.verify()["status"], "passed")

    def test_local_import_and_untrusted_compiler_option_fail(self):
        for source in ["import Forged\ntheorem result : True := True.intro",
                       "public meta import Forged\ntheorem result : True := True.intro",
                       "set_option debug.skipKernelTC true\ntheorem result : True := True.intro"]:
            with self.subTest(source=source):
                (self.root / "Main.lean").write_text(source, encoding="utf-8")
                self.assertEqual(self.verify()["status"], "failed")

    def test_mathlib_requires_matching_pinned_provisioned_manifest(self):
        (self.root / "Main.lean").write_text("import Mathlib\ntheorem result : True := True.intro", encoding="utf-8")
        self.assertEqual(self.verify()["status"], "failed")
        commit = "a" * 40
        (self.root / "lakefile.toml").write_text(f'name = "formalization"\n[[require]]\nname = "mathlib"\ngit = "https://github.com/leanprover-community/mathlib4.git"\nrev = "{commit}"\n', encoding="utf-8")
        self.assertEqual(self.verify()["status"], "failed")
        manifest = {"packages": [{"name": "mathlib", "rev": "b" * 40, "type": "git"}]}
        (self.root / "lake-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.assertEqual(self.verify()["status"], "failed")
        manifest["packages"][0]["rev"] = commit
        (self.root / "lake-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.assertEqual(self.verify()["status"], "blocked")
        (self.root / ".lake/packages/mathlib").mkdir(parents=True)
        self.assertEqual(self.verify()["status"], "passed")

    def test_process_runner_preserves_logs_and_terminates_timed_out_tree(self):
        class Process:
            def wait(self, timeout):
                raise subprocess.TimeoutExpired("lake", timeout)

        def launch(arguments, **kwargs):
            kwargs["stdout"].write(b"compiler output")
            kwargs["stderr"].write(b"compiler diagnostics")
            self.assertIs(kwargs["stdin"], subprocess.DEVNULL)
            self.assertNotIn("shell", kwargs)
            return Process()

        with patch("colombo.lean_agent.compiler.managed_popen", side_effect=launch), \
                patch("colombo.lean_agent.compiler.terminate_tree", return_value=True) as terminate:
            report = _run(self.root, self.root, "compile", ["lake", "env", "lean", "Main.lean"], 1)
        self.assertTrue(report["timed_out"])
        self.assertEqual(report["stdout"], "compiler output")
        self.assertEqual(report["stderr"], "compiler diagnostics")
        terminate.assert_called_once()

    @unittest.skipUnless(shutil.which("lake") and shutil.which("lean"), "Lean/lake are not provisioned on this host")
    def test_real_lean_compiler_smoke(self):
        version = subprocess.run(["lean", "--version"], cwd=self.root, capture_output=True,
                                 text=True, timeout=15, check=True).stdout
        match = re.search(r"version (4\.\d+\.\d+(?:-rc\d+)?)", version)
        self.assertIsNotNone(match)
        (self.root / "lean-toolchain").write_text("leanprover/lean4:v" + match[1], encoding="utf-8")
        report = verify_lean(self.root, ["result"])
        self.assertEqual(report["status"], "passed", report)
        (self.root / "Main.lean").write_text("theorem result : False := by trivial", encoding="utf-8")
        self.assertEqual(verify_lean(self.root, ["result"])["status"], "failed")


if __name__ == "__main__":
    unittest.main()
