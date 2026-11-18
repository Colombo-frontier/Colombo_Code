"""Empirical findings may guide research; only Proof Results certify steps."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))
from colombo.configuration import load_config
from colombo.brain.research_store import Store
from colombo.brain.submission_validation import ContractError, validate_progress, validate_semantics
from colombo.brain.proof_draft import resolve_proof_source
from brain_fixtures import freeze_setting, progress


class EmpiricalProofBoundaryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".test-empirical-boundary-", dir=PROJECT)
        self.addCleanup(temporary.cleanup)
        self.store = Store.create(Path(temporary.name) / "run", "Prove a uniform rate", [], load_config())
        freeze_setting(self.store)
        self.sequence = 0

    def result(self, *, empirical=True, accepted=False, outcome="observations"):
        self.sequence += 1
        path = f"tasks/T{self.sequence:04d}/results/A0001/artifacts/computation.md"
        destination = self.store.safe_path(path)
        destination.parent.mkdir(parents=True)
        destination.write_text("Fixed computational material; scope is established by its review.", encoding="utf-8")
        result = self.store.write_record("result", {"task_id": f"T{self.sequence:04d}", "attempt_id": "A0001",
            "evidence_kind": "empirical" if empirical else "proof", "accepted": accepted,
            "empirical_report": {"outcome": outcome} if empirical else None, "artifacts": [{"path": path}]})
        rid = result["id"]
        package = self.store.write_record("review_package", {"review_kind": "result", "result_ref": rid,
            "required_checked_refs": [rid], "allowed_refs": [rid]})
        claim = {"id": "C1", "kind": "empirical" if empirical else "lemma", "statement": "A bounded finding",
            "scope": "Fixed investigated scope", "assumptions": [], "expression": "", "evidence_paths": [path]}
        review = {"review_kind": "result", "result_ref": rid, "verdict": "pass", "summary": "Fixed scope checked",
            "findings": [], "checked_refs": [rid], "confirmed_claims": [claim],
            "completion_status": "completed" if empirical else "partial", "repair_kind": "none"}
        validate_semantics("verify-progress", review, self.store, {"review_package_ref": package})
        ref = self.store.write_record("review", review)
        self.store.set_meta(result_reviews={**self.store.get_meta("result_reviews", {}), rid: ref})
        return rid, path, ref

    def candidate(self, rid, path, status="checked"):
        return {"summary": "Candidate composition", "result_refs": [rid], "update": {
            "admissions": [], "progress": progress([rid]), "rechecked_step_ids": [],
            "proof_draft": {"title": "Partial Proof", "statement": "Uniform rate", "assumptions": [],
                "body": "Candidate argument awaiting independent final review.", "open_questions": ["Uniform extension"],
                "steps": [{"id": "P0", "title": "Local step", "statement": "Local statement", "status": status,
                    "depends_on": [], "gaps": [] if status == "checked" else ["Needs mathematical verification"],
                    "evidence": [{"result_ref": rid, "path": path, "locator": "Fixed computation"}]}]}},
            "prunes": [], "next_action": "continue", "rationale": "The global Goal remains open"}

    def test_empirical_result_cannot_certify_checked_step(self):
        rid, path, _ = self.result()
        with self.assertRaisesRegex(ContractError, "Empirical Result"):
            validate_semantics("integrate", self.candidate(rid, path), self.store, {})

    def test_empirical_result_can_remain_draft_evidence(self):
        rid, path, _ = self.result()
        value = validate_semantics("integrate", self.candidate(rid, path, "draft"), self.store, {})
        self.assertEqual(value["update"]["proof_draft"]["steps"][0]["status"], "draft")

    def test_partial_proof_result_with_confirmed_mathematical_claim_is_eligible(self):
        rid, path, _ = self.result(empirical=False, accepted=False)
        value = validate_semantics("integrate", self.candidate(rid, path), self.store, {})
        self.assertEqual(value["update"]["proof_draft"]["steps"][0]["status"], "checked")
        self.assertFalse(self.store.read_record(rid)["accepted"])

    def test_empirical_body_source_rejected_even_if_accepted_flag_is_true(self):
        rid, path, _ = self.result(accepted=True)
        with self.assertRaisesRegex(ContractError, "Empirical Result"):
            resolve_proof_source(self.store, {"body_source": {"result_ref": rid, "path": path}})

    def test_inconclusive_empirical_task_can_be_accepted_and_completed(self):
        rid, path, _ = self.result(outcome="inconclusive")
        value = self.candidate(rid, path, "draft")
        value["update"].pop("proof_draft")
        value["update"].pop("rechecked_step_ids")
        value["update"]["admissions"] = [{"result_ref": rid, "verdict": "accepted", "goal_ids": ["G0"],
            "proof_step_ids": [], "reason": "Reliable indistinguishability answers the assigned question",
            "completion_status": "completed", "completed_parts": ["Experiment question"], "remaining": []}]
        checked = validate_semantics("process_results", value, self.store, {})
        self.assertEqual(checked["update"]["admissions"][0]["completion_status"], "completed")
        self.assertEqual(checked["update"]["progress"]["items"][0]["status"], "partial")

    def test_empirical_claim_does_not_certify_bound_or_mathematical_goal(self):
        rid, _, review = self.result()
        value = progress([rid])
        for status in ("supported", "refuted"):
            with self.subTest(status=status):
                changed = copy.deepcopy(value)
                changed["items"][0]["status"] = status
                with self.assertRaisesRegex(ContractError, "mathematical Claims"):
                    validate_progress(self.store, changed)
        value["bracket"]["bounds"] = [{"id": "B1", "direction": "upper_bound", "expression": "",
            "scope": "Fixed investigated scope", "assumptions": [], "source": "Experiment",
            "evidence_state": "certified", "result_ref": rid, "review_ref": review["id"], "claim_id": "C1"}]
        with self.assertRaisesRegex(ContractError, "Certified Bound"):
            validate_progress(self.store, value)

    def test_empirical_result_cannot_supply_pruning_premise(self):
        from colombo.brain.pruning import _canonical_relation
        from test_submission_validation import task_spec
        rid, _, _ = self.result()
        spec = task_spec()
        assignment = self.store.write_record("assignment", {"task_id": "T0099", "spec": spec})
        target = {"task_id": "T0099", "active_attempt": "A0001", "assignment_ref": assignment}
        relation = {"task_id": "T0099", "attempt_id": "A0001", "reason": "redundant",
            "evidence_refs": [rid], "relation_explanation": "Attempt to use empirical evidence as a premise",
            "scope_check": "Fixed investigated scope", "covered_deliverables": spec["deliverables"],
            "premises": [{"result_ref": rid, "statement": "A bounded finding",
                          "scope": "Fixed investigated scope", "assumptions": []}]}
        with self.assertRaisesRegex(ContractError, "verified mathematical Claims"):
            _canonical_relation(self.store, relation, target)

    def test_returned_empirical_report_requires_new_repair_task(self):
        from test_submission_validation import task_spec
        rid, _, _ = self.result(outcome="inconclusive")
        spec = {**task_spec(), "specialization": "experiment"}
        assignment = self.store.write_record("assignment", {"task_id": "T0001", "spec": spec})
        self.store.save_task({"task_id": "T0001", "state": "returned", "assignment_ref": assignment,
                              "latest_result_ref": self.store.record_ref(rid)})
        resumed = {**spec, "mode": "resume", "resume_task_id": "T0001"}
        with self.assertRaisesRegex(ContractError, "new repair Task"):
            validate_semantics("plan", {"rationale": "Revise existing empirical report", "tasks": [resumed]},
                               self.store, {})


if __name__ == "__main__":
    unittest.main()
