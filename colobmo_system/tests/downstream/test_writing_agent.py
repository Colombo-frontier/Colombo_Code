"""Standalone writing consumes fixed evidence and never re-runs a completed draft."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import ValidationError

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from colombo.downstream.handoff import digest
from colombo.writing_agent.agent import run
from colombo.lean_agent.evidence import EVIDENCE_VERSION, review_binding
from evidence_fixtures import compiler_fixture


def material(text):
    return {"name": "draft.md", "text": text,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}


def package_fixture():
    proof = {
        "title": "Nonnegative finite sums", "statement": "For nonnegative x and y, x + y >= 0.",
        "assumptions": ["x and y are real", "x >= 0", "y >= 0"],
        "body": "Adding the assumed inequalities x >= 0 and y >= 0 proves x + y >= 0.",
        "steps": [{"id": "sum", "title": "Add inequalities", "statement": "x + y >= 0",
                   "status": "checked", "depends_on": [], "evidence": [], "gaps": []}],
        "open_questions": [],
    }
    return {"schema_version": 1, "proof": proof, "proof_sha256": digest(proof),
            "main_claim_id": "main", "required_claim_ids": ["main", "sum"],
            "setting": {"domain": "real numbers"}, "goal": {"title": proof["title"]},
            "brain_check": {"verdict": "pass", "proof_sha256": digest(proof)},
            "source_materials": [material("Prior draft: x and y are nonnegative real numbers.")]}


def lean_fixture(package):
    source = "theorem main_sum : True := True.intro\ntheorem sum_step : True := True.intro\n"
    result = {"evidence_version": EVIDENCE_VERSION, "package_sha256": digest(package),
            "status": "passed", "proof_sha256": package["proof_sha256"], "source": source,
            "diagnostics": [],
            "required_claim_ids": list(package["required_claim_ids"]),
            "compiler": compiler_fixture(source, ["main_sum", "sum_step"]),
            "mapping": [{"claim_id": claim, "declaration": declaration,
                         "correspondence": "Same real domain, assumptions, and sum inequality."}
                        for claim, declaration in zip(package["required_claim_ids"], ["main_sum", "sum_step"])],
            "semantic_review": {"proof_sha256": package["proof_sha256"], "verdict": "pass",
                                "checked_claim_ids": list(package["required_claim_ids"]), "findings": []}}
    result["semantic_review_binding"] = review_binding(package, source, result["mapping"],
                                                       result["compiler"], result["semantic_review"])
    return result


def manuscript_fixture(package):
    return {"proof_sha256": package["proof_sha256"],
            "manuscript_md": "# Nonnegative sums\n\n## Theorem 1\nFor real x,y >= 0, x+y >= 0.\n\n"
                             "### Proof\nAdding the assumptions gives the result.\n",
            "manuscript_tex": r"\documentclass{article}\begin{document}"
                              r"\section{Theorem 1}\label{thm:sum}"
                              r"For real $x,y\ge0$, $x+y\ge0$."
                              r"\paragraph{Proof}\label{proof:sum}"
                              r"Adding the assumptions gives the result.\end{document}",
            "bibliography_bib": "",
            "claim_map": [{"claim_id": "main", "location": "Markdown Theorem 1; LaTeX thm:sum"},
                          {"claim_id": "sum", "location": "Markdown Proof; LaTeX proof:sum"}],
            "editorial_gaps": []}


class FakeModel:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def invoke(self, stage, work_dir, prompt, context, schema, timeout_seconds):
        self.calls.append({"stage": stage, "work_dir": work_dir, "context": copy.deepcopy(context),
                           "schema": schema, "timeout_seconds": timeout_seconds})
        return copy.deepcopy(self.payload)


class NoModelCalls:
    def invoke(self, *args, **kwargs):
        raise AssertionError("A completed or rejected writing request must not invoke a model")


class WritingAgentTests(unittest.TestCase):
    def setUp(self):
        # Keep even temporary validation artifacts inside the writable workspace.
        temporary_parent = (PROJECT / ".runtime").resolve()
        temporary_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="writing-test-", dir=temporary_parent)
        self.root = Path(self.temporary.name).resolve()
        self.assertTrue(self.root.is_relative_to(temporary_parent))
        self.addCleanup(self.temporary.cleanup)
        self.work = self.root / "writing"
        self.package = package_fixture()
        self.lean = lean_fixture(self.package)
        self.payload = manuscript_fixture(self.package)
        self.config = {"timeout_seconds": 60}

    def execute(self, model=None, **changes):
        return run(changes.get("package", self.package), changes.get("lean", self.lean),
                   changes.get("work", self.work), changes.get("config", self.config),
                   model if model is not None else FakeModel(self.payload))

    def test_complete_payload_exports_artifacts_without_changing_inputs(self):
        originals = copy.deepcopy((self.package, self.lean, self.config))
        model = FakeModel(self.payload)
        result = self.execute(model)
        self.assertEqual(result["status"], "draft")
        self.assertEqual(result["latex_compilation"], "not_run")
        self.assertEqual(result["mathematical_review"], "writer_self_check_only")
        self.assertEqual((self.package, self.lean, self.config), originals)
        self.assertEqual(len(model.calls), 1)
        self.assertEqual(model.calls[0]["stage"], "manuscript-writing")
        self.assertEqual(model.calls[0]["context"]["source_materials"], self.package["source_materials"])
        self.assertEqual(model.calls[0]["context"]["lean_result"], self.lean)
        for field, filename in (("manuscript_md", "manuscript.md"), ("manuscript_tex", "manuscript.tex"),
                                ("bibliography_bib", "references.bib")):
            self.assertEqual((self.work / filename).read_text(encoding="utf-8"), self.payload[field])
        claim_map = json.loads((self.work / "claim-map.json").read_text(encoding="utf-8"))
        self.assertEqual(claim_map["claim_map"], self.payload["claim_map"])
        self.assertEqual(claim_map["proof_sha256"], digest(self.package["proof"]))
        self.assertEqual(json.loads((self.work / "result.json").read_text(encoding="utf-8")), result)

    def test_editorial_gaps_are_preserved_as_draft_with_gaps(self):
        self.payload["editorial_gaps"] = ["Related-work comparison remains unverified."]
        result = self.execute()
        self.assertEqual(result["status"], "draft_with_gaps")
        self.assertEqual(result["manuscript"]["editorial_gaps"], self.payload["editorial_gaps"])

    def test_changed_proof_or_material_bytes_are_rejected_before_model_start(self):
        variants = []
        package = copy.deepcopy(self.package)
        package["proof"]["body"] = "A different argument with a stale proof digest."
        variants.append(package)
        package = copy.deepcopy(self.package)
        package["source_materials"][0]["text"] = "Changed draft without updating its digest."
        variants.append(package)
        package = copy.deepcopy(self.package)
        package["brain_check"]["verdict"] = "fail"
        variants.append(package)
        for index, package in enumerate(variants):
            with self.subTest(case=index):
                with self.assertRaises(ValueError):
                    self.execute(NoModelCalls(), package=package, work=self.root / f"invalid-package-{index}")

    def test_lean_must_pass_for_the_same_proof_before_model_start(self):
        for index, changes in enumerate(({"status": "failed"}, {"status": "incomplete"},
                                        {"proof_sha256": "b" * 64})):
            with self.subTest(changes=changes):
                lean = {**self.lean, **changes}
                with self.assertRaises(ValueError):
                    self.execute(NoModelCalls(), lean=lean, work=self.root / f"lean-rejection-{index}")

    def test_self_declared_pass_without_compiler_and_review_is_rejected(self):
        for field in ("compiler", "semantic_review"):
            with self.subTest(missing=field):
                lean = copy.deepcopy(self.lean)
                lean.pop(field)
                with self.assertRaises(ValueError):
                    self.execute(NoModelCalls(), lean=lean, work=self.root / ("missing-" + field))

    def test_tag_only_import_is_rejected_before_model_or_output_creation(self):
        # The audited writing-only probe: nested 'passed' labels are not evidence.
        lean = {"status": "passed", "proof_sha256": self.package["proof_sha256"],
                "compiler": {"status": "passed"},
                "semantic_review": copy.deepcopy(self.lean["semantic_review"])}
        with self.assertRaisesRegex(ValueError, "evidence version"):
            self.execute(NoModelCalls(), lean=lean)
        self.assertFalse(self.work.exists())
        # Adding the new envelope alone still does not supply compiler evidence.
        lean = {**self.lean, "compiler": {"status": "passed"}}
        with self.assertRaisesRegex(ValueError, "compiler"):
            self.execute(NoModelCalls(), lean=lean)
        self.assertFalse(self.work.exists())

    def test_incomplete_or_mismatched_embedded_evidence_is_rejected(self):
        variants = []
        for field in ("source", "mapping", "semantic_review_binding"):
            lean = copy.deepcopy(self.lean)
            lean.pop(field)
            variants.append(lean)
        for field in ("source_files", "project_sha256", "commands", "axioms", "compiled_sha256"):
            lean = copy.deepcopy(self.lean)
            lean["compiler"].pop(field)
            variants.append(lean)
        lean = copy.deepcopy(self.lean)
        lean["compiler"]["commands"][-1]["stdout"] += "changed output"
        variants.append(lean)
        lean = copy.deepcopy(self.lean)
        lean["semantic_review_binding"]["source_sha256"] = "0" * 64
        variants.append(lean)
        for index, lean in enumerate(variants):
            with self.subTest(case=index), self.assertRaises(ValueError):
                self.execute(NoModelCalls(), lean=lean, work=self.root / f"invalid-evidence-{index}")

    def test_same_proof_in_a_changed_setting_cannot_reuse_evidence(self):
        package = copy.deepcopy(self.package)
        package["setting"] = {"domain": "a different domain"}
        with self.assertRaisesRegex(ValueError, "handoff package"):
            self.execute(NoModelCalls(), package=package)

    def test_complete_import_is_marked_as_checked_without_recompilation(self):
        with patch("colombo.lean_agent.compiler.verify_lean", side_effect=AssertionError("no recompile")):
            result = self.execute()
        self.assertEqual(result["lean_evidence_origin"], "imported")
        self.assertEqual(result["lean_evidence_validation"], "embedded_structure_and_bindings")
        self.assertIs(result["lean_recompiled_for_writing"], False)

    def test_failed_or_incomplete_semantic_evidence_is_rejected(self):
        variants = []
        for field, value in (("verdict", "fail"), ("proof_sha256", "c" * 64),
                             ("checked_claim_ids", ["main"]),
                             ("checked_claim_ids", ["main", "sum", "sum"]),
                             ("findings", ["Scope differs from the fixed proof."])):
            lean = copy.deepcopy(self.lean)
            lean["semantic_review"][field] = value
            variants.append(lean)
        lean = copy.deepcopy(self.lean)
        lean["compiler"]["status"] = "failed"
        variants.append(lean)
        for index, lean in enumerate(variants):
            with self.subTest(case=index):
                with self.assertRaises(ValueError):
                    self.execute(NoModelCalls(), lean=lean, work=self.root / f"evidence-rejection-{index}")

    def test_missing_duplicate_or_unknown_claim_mapping_is_rejected(self):
        for ids in (["main"], ["main", "sum", "sum"], ["main", "unknown"]):
            with self.subTest(ids=ids):
                payload = copy.deepcopy(self.payload)
                payload["claim_map"] = [{"claim_id": key, "location": "Theorem 1"} for key in ids]
                with self.assertRaises(ValueError):
                    self.execute(FakeModel(payload), work=self.root / ("case-" + str(len(ids)) + "-" + ids[-1]))

    def test_changed_proof_hash_in_manuscript_is_rejected(self):
        self.payload["proof_sha256"] = "d" * 64
        with self.assertRaises(ValueError):
            self.execute()
        self.assertFalse((self.work / "manuscript.md").exists())

    def test_incomplete_output_schema_is_rejected(self):
        self.payload.pop("manuscript_tex")
        with self.assertRaises(ValidationError):
            self.execute()
        self.assertFalse((self.work / "result.json").exists())

    def test_replay_restores_exports_without_another_model_call(self):
        first = self.execute()
        (self.work / "manuscript.md").unlink()
        replay = self.execute(NoModelCalls())
        self.assertEqual(replay, first)
        self.assertEqual((self.work / "manuscript.md").read_text(encoding="utf-8"), self.payload["manuscript_md"])

    def test_modified_saved_result_is_not_adopted_on_replay(self):
        self.execute()
        path = self.work / "result.json"
        report = json.loads(path.read_text(encoding="utf-8"))
        report["manuscript"]["manuscript_md"] = "A different unreviewed article."
        path.write_text(json.dumps(report), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.execute(NoModelCalls())

    def test_orphaned_result_cannot_become_a_valid_receipt(self):
        self.work.mkdir()
        (self.work / "result.json").write_text(json.dumps({"manuscript": self.payload}), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.execute(NoModelCalls())

    def test_failed_call_does_not_reset_writing_deadline_on_retry(self):
        class FailedModel:
            def invoke(self, *args, **kwargs):
                raise RuntimeError("Synthetic process failure")

        with patch("colombo.writing_agent.agent.time.time", return_value=100):
            with self.assertRaises(RuntimeError):
                self.execute(FailedModel())
        with patch("colombo.writing_agent.agent.time.time", return_value=161):
            with self.assertRaises(TimeoutError):
                self.execute(NoModelCalls())

    def test_changed_input_or_configuration_cannot_reuse_workspace(self):
        self.execute()
        package = copy.deepcopy(self.package)
        package["source_materials"] = [material("Different explanatory draft, same checked proof.")]
        with self.assertRaises(ValueError):
            self.execute(NoModelCalls(), package=package)
        with self.assertRaises(ValueError):
            self.execute(NoModelCalls(), config={"timeout_seconds": 61})
        package = copy.deepcopy(self.package)
        package["proof"]["body"] += " The conclusion uses both assumptions."
        package["proof_sha256"] = digest(package["proof"])
        package["brain_check"]["proof_sha256"] = package["proof_sha256"]
        with self.assertRaises(ValueError):
            self.execute(NoModelCalls(), package=package, lean=lean_fixture(package))

    def test_model_cannot_mutate_callers_frozen_input_by_reference(self):
        payload = self.payload

        class MutatingModel:
            def invoke(self, stage, work_dir, prompt, context, schema, timeout_seconds):
                context["proof"]["body"] = "Changed mathematical claim."
                context["source_materials"][0]["text"] = "Changed evidence."
                context["lean_result"]["status"] = "failed"
                return copy.deepcopy(payload)

        originals = copy.deepcopy((self.package, self.lean))
        self.execute(MutatingModel())
        self.assertEqual((self.package, self.lean), originals)


if __name__ == "__main__":
    unittest.main()
