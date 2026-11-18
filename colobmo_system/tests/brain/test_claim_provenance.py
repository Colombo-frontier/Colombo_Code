"""Verified comparison and Goal status cannot be reassigned to other evidence."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from colombo.configuration import PROJECT_ROOT, load_config
from colombo.brain.research_store import Store
from colombo.brain.submission_validation import ContractError, validate_semantics, validate_progress


class ClaimProvenanceTests(unittest.TestCase):
    def setUp(self):
        base = PROJECT_ROOT / "validation" / "tmp"
        base.mkdir(parents=True, exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temp.cleanup)
        self.store = Store.create(Path(temp.name) / "run", "Oracle Complexity", [], load_config())
        (self.store.root / "proof.txt").write_text("Fixture proof evidence", encoding="utf-8")
        self.rid = self.store.write_record("result", {"task_id": "T0001", "attempt_id": "A0001",
            "evidence_kind": "mathematical", "artifacts": [{"path": "proof.txt"}]})["id"]
        self.package = self.store.write_record("review_package", {"review_kind": "result", "result_ref": self.rid,
            "required_checked_refs": [self.rid], "allowed_refs": [self.rid]})

    def claim(self, kind, expression="1", identifier=None):
        return {"id": identifier or kind, "kind": kind, "statement": "Fixture " + kind,
            "expression": expression, "scope": "R1", "assumptions": [], "evidence_paths": ["proof.txt"]}

    def report(self, claims):
        return {"review_kind": "result", "result_ref": self.rid, "verdict": "pass", "summary": "Fixture",
            "findings": [], "checked_refs": [self.rid], "confirmed_claims": claims,
            "completion_status": "partial", "repair_kind": "none"}

    def register(self, report):
        valid = validate_semantics("verify-progress", report, self.store, {"review_package_ref": self.package})
        ref = self.store.write_record("review", valid)
        self.store.set_meta(result_reviews={self.rid: ref})
        return ref["id"]

    def progress(self, review, comparison=True):
        bounds = [{"id": kind, "direction": kind, "expression": "1", "scope": "R1", "assumptions": [],
            "source": "Fixture", "evidence_state": "certified", "result_ref": self.rid,
            "review_ref": review, "claim_id": kind} for kind in ("lower_bound", "upper_bound")]
        return {"overall": "Research progress", "status": "in_progress",
            "items": [{"goal_id": "G0", "description": "Goal", "status": "supported",
                "result_refs": [self.rid], "remaining": []}], "remaining": [],
            "bracket": {"bounds": bounds, "regimes": [{"id": "R1", "scope": "R1",
                "lower_bound_ids": ["lower_bound"], "upper_bound_ids": ["upper_bound"],
                "gap": "1", "candidate_rate": "1", "candidate_basis": "Conjecture",
                "status": "near_optimal", "comparison_review_ref": review if comparison else None,
                "comparison_claim_id": "comparison" if comparison else None, "remaining": []}]}}

    def comparison(self):
        claim = self.claim("comparison")
        claim["comparison_bounds"] = [{"direction": side, "expression": "1", "scope": "R1", "assumptions": []}
            for side in ("lower_bound", "upper_bound")]
        return claim

    def test_reviewed_comparison_cannot_be_reused_with_a_different_certified_bound(self):
        claims = [self.claim("lower_bound"), self.claim("upper_bound"),
            self.claim("upper_bound", "2", "other_upper"), self.comparison()]
        review = self.register(self.report(claims))
        progress = self.progress(review)
        validate_progress(self.store, progress)
        progress["bracket"]["bounds"][1].update(expression="2", claim_id="other_upper")
        with self.assertRaisesRegex(ContractError, "verified Bounds"):
            validate_progress(self.store, progress)

    def test_comparison_review_requires_exact_bound_descriptions(self):
        with self.assertRaisesRegex(ContractError, "exact Lower and Upper"):
            self.register(self.report([self.claim("comparison")]))

    def test_conditional_comparison_cannot_drop_assumptions(self):
        comparison = self.comparison()
        comparison["assumptions"] = ["Additional regularity condition"]
        review = self.register(self.report([self.claim("lower_bound"), self.claim("upper_bound"), comparison]))
        progress = self.progress(review)
        with self.assertRaisesRegex(ContractError, "assumptions"):
            validate_progress(self.store, progress)
        progress["bracket"]["regimes"][0]["assumptions"] = comparison["assumptions"]
        validate_progress(self.store, progress)

    def test_empirical_claim_cannot_mark_mathematical_goal_supported(self):
        review = self.register(self.report([self.claim("empirical")]))
        progress = self.progress(review)
        progress["bracket"] = {"bounds": [], "regimes": []}
        with self.assertRaisesRegex(ContractError, "confirmed mathematical"):
            validate_progress(self.store, progress)

    def test_rejected_result_without_confirmed_claims_cannot_mark_goal_supported(self):
        report = self.report([])
        report.update(verdict="revise", repair_kind="research")
        review = self.register(report)
        progress = self.progress(review)
        progress["bracket"] = {"bounds": [], "regimes": []}
        with self.assertRaisesRegex(ContractError, "confirmed mathematical"):
            validate_progress(self.store, progress)

    def test_unregistered_review_cannot_certify_a_bound(self):
        review = self.register(self.report([self.claim("lower_bound"), self.claim("upper_bound"), self.comparison()]))
        progress = self.progress(review)
        self.store.set_meta(result_reviews={})
        with self.assertRaisesRegex(ContractError, "not returned through Verifier"):
            validate_progress(self.store, progress)


if __name__ == "__main__":
    unittest.main()
