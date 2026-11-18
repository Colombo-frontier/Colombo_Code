"""Final publication is bound to the reviewed draft, not a positive summary."""
import copy
import unittest

from colombo.brain.final_report import _publication_alignment


class FinalPublicationTests(unittest.TestCase):
    def setUp(self):
        self.meta = {"config": {"workflow": {"version": 3}},
                     "proof_ref": {"id": "P2", "revision": 1},
                     "final_review_ref": {"id": "V2", "revision": 1}}
        self.progress = {"proof_ref": self.meta["proof_ref"],
                         "review_ref": self.meta["final_review_ref"], "progress": {
            "overall": "We have useful results in some regimes.", "status": "completed"}}
        self.proof = {"review_ref": self.meta["final_review_ref"], "proof_draft": {
            "steps": [{"id": "S1", "status": "checked", "gaps": []}], "open_questions": []}}
        self.report = {"verdict": "pass", "review_kind": "proof", "checked_refs": ["P2"],
                       "completion_status": "completed", "findings": [], "repair_kind": "none"}

    def aligned(self):
        return _publication_alignment(self.meta, self.progress, self.proof,
                                      lambda ref: copy.deepcopy(self.report), True)

    def test_exact_reviewed_complete_draft_can_be_published(self):
        self.assertTrue(self.aligned())

    def test_review_of_previous_draft_does_not_certify_new_draft(self):
        self.report["checked_refs"] = ["P1"]
        self.assertFalse(self.aligned())

    def test_result_review_cannot_substitute_for_final_proof_review(self):
        self.report["review_kind"] = "result"
        self.assertFalse(self.aligned())

    def test_pass_with_unresolved_proof_gap_is_not_complete(self):
        self.proof["proof_draft"]["steps"][0]["gaps"] = ["Composition still missing"]
        self.assertFalse(self.aligned())

    def test_reviewed_open_questions_do_not_prevent_completion(self):
        self.proof["proof_draft"]["open_questions"] = ["Sharp logarithmic powers remain open beyond this Goal."]
        self.assertTrue(self.aligned())

    def test_pass_partial_or_missing_completion_cannot_certify_completion(self):
        for value in ("partial", "incomplete", "unknown", None):
            with self.subTest(completion_status=value):
                if value is None:
                    self.report.pop("completion_status", None)
                else:
                    self.report["completion_status"] = value
                self.assertFalse(self.aligned())

    def test_findings_or_required_repairs_block_completion(self):
        self.report["findings"] = [{"subject": "proof", "reason": "Unresolved issue", "result_refs": []}]
        self.assertFalse(self.aligned())
        self.report["findings"] = []
        self.report["repair_kind"] = "presentation"
        self.assertFalse(self.aligned())

    def test_progress_must_be_bound_to_same_draft(self):
        self.progress["proof_ref"] = {"id": "P1", "revision": 1}
        self.assertFalse(self.aligned())

    def test_missing_final_adoption_is_not_completion(self):
        self.meta["final_review_ref"] = None
        self.assertFalse(self.aligned())


if __name__ == "__main__":
    unittest.main()
