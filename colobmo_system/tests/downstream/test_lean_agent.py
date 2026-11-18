"""Independent Lean orchestration preserves both gates and bounded artifacts."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from colombo.lean_agent.agent import SCHEMAS, _validate_response, run
from colombo.downstream.handoff import digest


class FakeModel:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def invoke(self, stage, work_dir, prompt, context, schema, timeout_seconds):
        self.calls.append({"stage": stage, "work_dir": str(work_dir), "context": copy.deepcopy(context)})
        value = self.responses.pop(0)
        if isinstance(value, Exception):
            raise value
        return copy.deepcopy(value)


class LeanAgentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.template = self.root / "template"
        self.template.mkdir()
        (self.template / "lean-toolchain").write_text("leanprover/lean4:v4.19.0", encoding="utf-8")
        (self.template / "lakefile.toml").write_text('name = "formalization"', encoding="utf-8")
        self.work = self.root / "agent"
        proof = {"statement": "True", "steps": []}
        self.package = {"proof": proof, "proof_sha256": digest(proof),
                        "setting": {}, "required_claim_ids": ["main"]}
        self.config = {"lean_project": str(self.template), "max_compile_attempts": 3,
                       "timeout_seconds": 120, "compile_timeout_seconds": 5, "lake_bin": "lake"}
        self.candidate = {"proof_sha256": self.package["proof_sha256"], "status": "candidate",
            "source": "theorem result : True := True.intro\n", "mapping": [
                {"claim_id": "main", "declaration": "result", "correspondence": "The complete main Claim"}],
            "limitations": []}
        self.review = {"proof_sha256": self.package["proof_sha256"], "verdict": "pass",
                       "checked_claim_ids": ["main"], "findings": []}

    def compile(self, project, names, **kwargs):
        return {"status": "passed", "source_sha256": hashlib.sha256((project / "Main.lean").read_bytes()).hexdigest(),
                "declarations": names, "declaration_printout": "theorem result : True := True.intro",
                "axioms": {"result": []}, "diagnostics": []}

    def invoke(self, model, compiler=None):
        with patch("colombo.lean_agent.agent.verify_lean", side_effect=compiler or self.compile):
            return run(self.package, self.work, self.config, model)

    def test_compiler_and_separate_correspondence_review_are_both_required(self):
        model = FakeModel([self.candidate, self.review])
        report = self.invoke(model)
        self.assertEqual(report["status"], "passed", report)
        self.assertEqual([c["stage"] for c in model.calls], ["lean-check", "lean-review"])
        self.assertNotEqual(model.calls[0]["work_dir"], model.calls[1]["work_dir"])
        self.assertEqual(model.calls[1]["context"]["compiler"]["axioms"], {"result": []})
        self.assertEqual(report["proof_sha256"], self.package["proof_sha256"])
        self.assertTrue((self.work / "attempts/A0001/project/Main.lean").is_file())
        self.assertTrue((self.work / "attempts/A0001/compiler.json").is_file())
        self.assertTrue((self.work / "attempts/A0001/review.json").is_file())
        self.assertFalse((self.template / "Main.lean").exists())

    def test_compiler_failure_is_feedback_for_next_fresh_candidate(self):
        count = 0
        def compiler(project, names, **kwargs):
            nonlocal count
            count += 1
            if count == 1:
                return {"status": "failed", "diagnostics": ["unknown identifier"]}
            return self.compile(project, names, **kwargs)
        model = FakeModel([self.candidate, self.candidate, self.review])
        report = self.invoke(model, compiler)
        self.assertEqual(report["status"], "passed", report)
        self.assertEqual(count, 2)
        self.assertEqual([c["stage"] for c in model.calls], ["lean-check", "lean-check", "lean-review"])
        self.assertEqual(model.calls[1]["context"]["previous_feedback"]["compiler"]["diagnostics"], ["unknown identifier"])

    def test_semantic_failure_returns_to_formalizer_with_findings(self):
        rejected = {**self.review, "verdict": "fail", "findings": ["Quantifier order changed"]}
        model = FakeModel([self.candidate, rejected, self.candidate, self.review])
        report = self.invoke(model)
        self.assertEqual(report["status"], "passed", report)
        self.assertEqual(model.calls[2]["context"]["previous_feedback"]["semantic_review"]["findings"], rejected["findings"])
        self.assertEqual(len(report["attempts"]), 2)

    def test_missing_infrastructure_does_not_start_semantic_review(self):
        model = FakeModel([self.candidate])
        report = self.invoke(model, lambda *args, **kwargs: {"status": "blocked", "diagnostics": ["lake absent"]})
        self.assertEqual(report["status"], "blocked")
        self.assertEqual(len(model.calls), 1)

    def test_missing_project_does_not_call_model(self):
        self.config["lean_project"] = ""
        model = FakeModel([])
        self.assertEqual(self.invoke(model)["status"], "blocked")
        self.assertEqual(model.calls, [])

    def test_incomplete_preserves_partial_source_without_compiling(self):
        candidate = {**self.candidate, "status": "incomplete", "mapping": [], "limitations": ["Missing analytic Lemma"]}
        model = FakeModel([candidate])
        with patch("colombo.lean_agent.agent.verify_lean") as compiler:
            report = run(self.package, self.work, self.config, model)
        self.assertEqual(report["status"], "incomplete")
        self.assertEqual(report["source"], candidate["source"])
        compiler.assert_not_called()

    def test_scope_incomplete_candidate_cannot_enter_compiler(self):
        self.config["max_compile_attempts"] = 1
        model = FakeModel([{**self.candidate, "mapping": []}])
        with patch("colombo.lean_agent.agent.verify_lean") as compiler:
            report = run(self.package, self.work, self.config, model)
        self.assertEqual(report["status"], "failed")
        compiler.assert_not_called()

    def test_proof_hash_and_review_coverage_are_not_model_assertions(self):
        self.config["max_compile_attempts"] = 1
        model = FakeModel([self.candidate, {**self.review, "checked_claim_ids": []}])
        self.assertEqual(self.invoke(model)["status"], "failed")
        self.package["proof"]["statement"] = "False"
        with self.assertRaisesRegex(ValueError, "hash"):
            self.invoke(FakeModel([]))

    def test_review_output_schema_omits_provider_unsupported_unique_items(self):
        def inspect_schema(value):
            if isinstance(value, dict):
                self.assertNotIn("uniqueItems", value)
                for child in value.values():
                    inspect_schema(child)
            elif isinstance(value, list):
                for child in value:
                    inspect_schema(child)
        inspect_schema(SCHEMAS["lean-review"])

    def test_duplicate_review_claim_ids_are_rejected_locally_for_both_verdicts(self):
        for verdict in ("pass", "fail"):
            with self.subTest(verdict=verdict):
                review = {**self.review, "verdict": verdict, "checked_claim_ids": ["main", "main"],
                          "findings": [] if verdict == "pass" else ["Statement correspondence unresolved"]}
                with self.assertRaisesRegex(ValueError, "unique Claim IDs"):
                    _validate_response("lean-review", review, self.package)

    def test_valid_unique_review_claim_ids_preserve_both_verdicts(self):
        for verdict in ("pass", "fail"):
            with self.subTest(verdict=verdict):
                review = {**self.review, "verdict": verdict,
                          "findings": [] if verdict == "pass" else ["Statement correspondence unresolved"]}
                self.assertIsNone(_validate_response("lean-review", review, self.package))

    def test_compiler_evidence_for_different_source_fails(self):
        model = FakeModel([self.candidate])
        report = self.invoke(model, lambda *args, **kwargs: {"status": "passed", "source_sha256": "wrong"})
        self.assertEqual(report["status"], "failed")
        self.assertEqual(len(model.calls), 1)

    def test_attempt_cap_and_model_failure_stop_cleanly(self):
        self.config["max_compile_attempts"] = 2
        model = FakeModel([self.candidate, self.candidate])
        report = self.invoke(model, lambda *args, **kwargs: {"status": "failed", "diagnostics": ["bad source"]})
        self.assertEqual(report["status"], "failed")
        self.assertEqual(len(model.calls), 2)
        fresh = self.root / "separate-agent"
        model = FakeModel([RuntimeError("native call exit unknown")])
        report = run(self.package, fresh, self.config, model)
        self.assertEqual(report["status"], "blocked")

    def test_completed_agent_is_idempotent_and_rejects_config_rebinding(self):
        model = FakeModel([self.candidate, self.review])
        report = self.invoke(model)
        self.assertEqual(self.invoke(FakeModel([])), report)
        self.config["max_compile_attempts"] = 4
        with self.assertRaisesRegex(ValueError, "another package or configuration"):
            self.invoke(FakeModel([]))

    def test_interrupted_compiler_directory_is_not_reused(self):
        model = FakeModel([self.candidate, self.review])
        self.invoke(model)
        (self.work / "result.json").unlink()
        (self.work / "attempts/A0001/compiler.json").unlink()
        model = FakeModel([])
        self.assertEqual(self.invoke(model)["status"], "blocked")
        self.assertEqual(model.calls, [])

    def test_original_deadline_is_not_reset_on_reentry(self):
        self.invoke(FakeModel([self.candidate, self.review]))
        (self.work / "result.json").unlink()
        state = json.loads((self.work / "state.json").read_text())
        state["deadline_unix"] = 1
        (self.work / "state.json").write_text(json.dumps(state), encoding="utf-8")
        report = self.invoke(FakeModel([]))
        self.assertEqual(report["status"], "incomplete")
        self.assertEqual(json.loads((self.work / "state.json").read_text())["deadline_unix"], 1)

    def test_concurrent_or_unreconciled_run_fails_closed(self):
        self.work.mkdir()
        (self.work / ".agent.lock").write_text("active", encoding="utf-8")
        self.assertEqual(self.invoke(FakeModel([]))["status"], "blocked")
        self.assertTrue((self.work / ".agent.lock").is_file())

    def test_agent_has_no_brain_cell_store_import(self):
        import ast
        for path in (PROJECT / "src/colombo/lean_agent").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    self.assertFalse((node.module or "").startswith(("colombo.brain", "colombo.cell")), str(path))
                elif isinstance(node, ast.Import):
                    self.assertFalse(any(n.name.startswith(("colombo.brain", "colombo.cell")) for n in node.names), str(path))


if __name__ == "__main__":
    unittest.main()
