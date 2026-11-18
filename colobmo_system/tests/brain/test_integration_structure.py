"""Completed publication needs structural completion and review of the new draft."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from colombo.configuration import PROJECT_ROOT, load_config
from colombo.brain.submission_validation import ContractError, validate_semantics
from colombo.brain.controller import OracleController
from colombo.brain.research_store import Store
from controller_fixtures import FakeCell
from test_oracle_workflow import Backend


class DraftBackend(Backend):
    def __init__(self, *, partial=False):
        super().__init__()
        self.partial = partial
        self.integration_contexts = []

    def invoke(self, role, stage, root, cid, prompt, context):
        value = super().invoke(role, stage, root, cid, prompt, context)
        if stage == "integrate":
            self.integration_contexts.append(copy.deepcopy(context))
            first = len(self.integration_contexts) == 1
            if first:
                value["update"]["proof_draft"]["steps"][0]["status"] = "draft"
                value["update"]["rechecked_step_ids"] = []
                value["update"]["proof_draft"]["body"] = "First self-contained fixture body."
            else:
                value["update"]["proof_draft"]["body"] = "Rechecked self-contained fixture body."
            if self.partial:
                value["update"]["progress"].update(status="in_progress", remaining=["Finish composition"])
                value["update"]["progress"]["items"][0].update(status="partial", remaining=["Finish composition"])
        return value


class LegacyCandidateController(OracleController):
    """Replay a candidate accepted before the completed-entry validation existed."""
    first_pass = None
    review_submitted = False

    def _integrate(self):
        if not self.calls.backend.integration_contexts:
            # Only emulate the historical submission gate. The final review,
            # publication guard, storage and subsequent submission are real.
            with patch("colombo.brain.submission_validation.proof_complete", return_value=True):
                super()._integrate()
            if self.review_submitted:
                stage = self.store.get_meta("integration")
                self._call("verifier", "verify-progress", "Fixture already-submitted review",
                    {**self._integration_context(), "review_package_ref": stage["review_package_ref"],
                     "proof_ref": stage["proof_ref"]})
            return
        return super()._integrate()

    def _final_review(self):
        super()._final_review()
        if self.first_pass is None and self.store.get_meta("publication_feedback"):
            self.first_pass = {
                key: copy.deepcopy(self.store.get_meta(key)) for key in (
                    "phase", "conclusion_ref", "progress_ref", "proof_ref", "final_review_ref",
                    "integration", "integration_review_ref", "publication_feedback", "pending_call")}


class IntegrationStructureTests(unittest.TestCase):
    def make(self, root):
        config = load_config()
        config["limits"].update(max_dispatches_per_wave=1, max_rounds=1)
        return Store.create(Path(root) / "run", "fixture", [], config)

    def test_completed_draft_is_rejected_before_final_review(self):
        with tempfile.TemporaryDirectory() as root:
            store, backend = self.make(root), DraftBackend()
            with self.assertRaisesRegex(ContractError, "Proof step P0 has status=draft"):
                OracleController(PROJECT_ROOT, store.root, backend, FakeCell()).run()
            self.assertEqual(backend.final_reviews, 0)
            self.assertIsNone(store.get_meta("conclusion_ref"))
            self.assertIsNone(store.get_meta("final_review_ref"))
            self.assertEqual(store.read_record(store.get_meta("progress_ref"))["progress"]["status"], "in_progress")

    def test_legacy_pass_requires_new_candidate_and_new_review(self):
        with tempfile.TemporaryDirectory() as root:
            store, backend = self.make(root), DraftBackend()
            controller = LegacyCandidateController(PROJECT_ROOT, store.root, backend, FakeCell())
            controller.review_submitted = True
            controller.run()
            first = controller.first_pass
            self.assertEqual(first["phase"], "integrating")
            self.assertIsNone(first["conclusion_ref"])
            self.assertIsNone(first["final_review_ref"])
            self.assertIsNone(first["pending_call"])
            self.assertEqual(store.read_record(first["progress_ref"])["progress"]["status"], "in_progress")
            feedback = first["publication_feedback"]
            self.assertEqual(feedback["kind"], "incomplete_proof_structure")
            self.assertIn("P0", " ".join(feedback["issues"]))
            first_proof = store.read_record(feedback["proof_ref"])["proof_draft"]
            self.assertEqual(first_proof["steps"][0]["status"], "draft")
            self.assertEqual(first_proof["body"], "First self-contained fixture body.")
            first_review = store.read_record(feedback["review_ref"])
            self.assertEqual(first_review["verdict"], "pass")
            self.assertEqual(first_review["findings"], [])
            self.assertEqual(backend.integration_contexts[1]["publication_feedback"], feedback)
            deadlines = [c["integration_deadline_unix"] for c in backend.integration_contexts]
            self.assertEqual(deadlines, [first["integration"]["deadline_unix"]] * 2)
            self.assertEqual(store.get_meta("integration")["deadline_unix"], deadlines[0])
            self.assertEqual(backend.calls.count("integrate"), 2)
            self.assertEqual(backend.final_reviews, 2)
            self.assertNotEqual(store.get_meta("final_review_ref"), feedback["review_ref"])
            self.assertEqual(store.get_meta("status"), "completed")
            self.assertEqual(store.get_meta("phase"), "done")
            self.assertIsNone(store.get_meta("publication_feedback"))
            final = (store.root / "output/final.md").read_text(encoding="utf-8")
            self.assertIn("Rechecked self-contained fixture body.", final)
            self.assertNotIn("First self-contained fixture body.", final)

    def test_legacy_preflight_revises_without_starting_verifier(self):
        with tempfile.TemporaryDirectory() as root:
            store, backend = self.make(root), DraftBackend()
            controller = LegacyCandidateController(PROJECT_ROOT, store.root, backend, FakeCell())
            controller.run()
            first = controller.first_pass
            self.assertEqual(first["phase"], "integrating")
            self.assertIsNone(first["pending_call"])
            self.assertIsNone(first["integration_review_ref"])
            self.assertIsNone(first["conclusion_ref"])
            feedback = first["publication_feedback"]
            self.assertIsNone(feedback["review_ref"])
            self.assertEqual(backend.integration_contexts[1]["publication_feedback"], feedback)
            self.assertEqual(backend.calls, ["plan", "verify-progress", "process_results", "integrate", "integrate", "verify-progress"])
            self.assertEqual(backend.final_reviews, 1)
            self.assertEqual(store.get_meta("integration")["deadline_unix"], first["integration"]["deadline_unix"])
            self.assertEqual(store.get_meta("status"), "completed")
            self.assertEqual(store.read_record(feedback["proof_ref"])["proof_draft"]["steps"][0]["status"], "draft")

    def test_legitimate_partial_draft_is_reviewed_and_exported(self):
        with tempfile.TemporaryDirectory() as root:
            store, backend = self.make(root), DraftBackend(partial=True)
            OracleController(PROJECT_ROOT, store.root, backend, FakeCell()).run()
            self.assertEqual(backend.calls.count("integrate"), 1)
            self.assertEqual(backend.final_reviews, 1)
            self.assertEqual(store.get_meta("status"), "partial")
            self.assertEqual(store.get_meta("phase"), "done")
            self.assertIsNone(store.get_meta("publication_feedback"))
            self.assertEqual(store.read_record(store.get_meta("proof_ref"))["proof_draft"]["steps"][0]["status"], "draft")
            final = (store.root / "output/final.md").read_text(encoding="utf-8")
            self.assertIn("First self-contained fixture body.", final)
            self.assertIn("Finish composition", final)

    def test_completed_structure_reports_other_unresolved_work(self):
        with tempfile.TemporaryDirectory() as root:
            store, backend = self.make(root), Backend()
            OracleController(PROJECT_ROOT, store.root, backend, FakeCell()).run()
            original = store.read_record(store.get_meta("integration")["assessment_ref"])
            for change, message in (
                (lambda p: p["steps"][0].update(gaps=["missing argument"]), "P0 still lists unresolved gaps"),
                (lambda p: p.update(open_questions=["unfinished case"]), "still lists open_questions"),
                (lambda p: p["steps"][0].update(status="retired"), "no active proof steps"),
            ):
                with self.subTest(message=message):
                    candidate = copy.deepcopy(original)
                    change(candidate["update"]["proof_draft"])
                    with self.assertRaisesRegex(ContractError, message):
                        validate_semantics("integrate", candidate, store, {})


if __name__ == "__main__":
    unittest.main()
