"""A completed final review updates control state without rewriting science."""
import copy
import unittest
from unittest.mock import patch

from colombo.brain import completion_recovery
from colombo.brain.final_completion import (
    proof_steps_complete, review_completes_goal, reviewed_progress,
)
from colombo.brain.final_report import reconcile_completed_run
from colombo.brain.research_store import Store, StoreError
from colombo.brain.submission_validation import proof_complete
from controller_fixtures import OracleTestFixture
from test_oracle_workflow import Backend


OPEN_QUESTION = "Are sharper logarithmic factors possible beyond this Goal?"
PENDING_REVIEW = "Final verification of this particular manuscript is pending."


class CompletionPolicyTests(unittest.TestCase):
    def setUp(self):
        self.proof = {"steps": [
            {"id": "P0", "status": "checked", "gaps": []},
            {"id": "old", "status": "retired", "gaps": ["Retired route"]},
        ], "open_questions": [OPEN_QUESTION]}
        self.review = {"verdict": "pass", "review_kind": "proof",
            "completion_status": "completed", "repair_kind": "none", "findings": []}
        self.progress = {"overall": "Reviewed results; final verification pending.",
            "status": "in_progress", "remaining": [PENDING_REVIEW],
            "items": [{"goal_id": "G0", "description": "Fixed Goal", "status": "partial",
                       "result_refs": [], "remaining": [PENDING_REVIEW]}],
            "bracket": {"bounds": [
                {"id": "L", "direction": "lower_bound"},
                {"id": "U", "direction": "upper_bound"},
            ], "regimes": [{"id": "R1", "status": "near_optimal", "remaining": [],
                            "lower_bound_ids": ["L"], "upper_bound_ids": ["U"]}]}}

    def test_reviewed_open_research_does_not_change_strict_pre_review_gate(self):
        self.assertTrue(proof_steps_complete(self.proof))
        self.assertFalse(proof_complete(self.proof))
        self.assertTrue(review_completes_goal(self.review))
        self.assertEqual(self.proof["open_questions"], [OPEN_QUESTION])

    def test_completed_review_normalizes_only_a_deep_copy(self):
        original = copy.deepcopy((self.progress, self.proof, self.review))
        result = reviewed_progress(self.progress, self.proof, self.review)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["remaining"], [])
        self.assertEqual(result["items"][0]["status"], "supported")
        self.assertEqual(result["items"][0]["remaining"], [])
        self.assertEqual((self.progress, self.proof, self.review), original)
        result["bracket"]["regimes"][0]["remaining"].append("Changed copy")
        self.assertEqual(self.progress["bracket"]["regimes"][0]["remaining"], [])

    def test_partial_missing_or_nonfinal_review_never_promotes(self):
        changes = [
            {"completion_status": "partial"}, {"completion_status": "incomplete"},
            {"completion_status": "unknown"}, {"completion_status": None},
            {"verdict": "revise"}, {"verdict": "inconclusive"},
            {"review_kind": "result"}, {"repair_kind": "presentation"},
            {"findings": [{"subject": "proof", "reason": "Unresolved", "result_refs": []}]},
        ]
        for change in changes:
            report = {**self.review, **change}
            with self.subTest(change=change):
                self.assertFalse(review_completes_goal(report))
                self.assertEqual(reviewed_progress(self.progress, self.proof, report), self.progress)
        report = dict(self.review)
        del report["completion_status"]
        self.assertFalse(review_completes_goal(report))
        self.assertEqual(reviewed_progress(self.progress, self.proof, report), self.progress)

    def test_structural_proof_gaps_cannot_be_hidden_by_completed_review(self):
        for change in (
            lambda p: p["steps"][0].update(status="draft"),
            lambda p: p["steps"][0].update(gaps=["Missing essential argument"]),
            lambda p: p["steps"][0].update(status="retired"),
            lambda p: p.update(steps=[]),
        ):
            proof = copy.deepcopy(self.proof)
            change(proof)
            with self.subTest(proof=proof):
                self.assertFalse(proof_steps_complete(proof))
                self.assertEqual(reviewed_progress(self.progress, proof, self.review), self.progress)

    def test_incomplete_regime_or_missing_bound_cannot_be_promoted(self):
        for change in (
            lambda r: r.update(status="partial"),
            lambda r: r.update(remaining=["Missing comparison proof"]),
            lambda r: r.update(lower_bound_ids=[]),
            lambda r: r.update(upper_bound_ids=[]),
        ):
            progress = copy.deepcopy(self.progress)
            change(progress["bracket"]["regimes"][0])
            with self.subTest(regime=progress["bracket"]["regimes"][0]):
                self.assertEqual(reviewed_progress(progress, self.proof, self.review), progress)


class PendingFinalBackend(Backend):
    """A genuine completed review of a still-pending candidate declaration."""
    def __init__(self, *, completion="completed"):
        super().__init__()
        self.completion = completion

    def invoke(self, role, stage, root, cid, prompt, context):
        result = super().invoke(role, stage, root, cid, prompt, context)
        if stage == "integrate":
            progress = result["update"]["progress"]
            progress.update(status="in_progress", remaining=[PENDING_REVIEW])
            progress["items"][0].update(status="partial", remaining=[PENDING_REVIEW])
            result["update"]["proof_draft"]["open_questions"] = [OPEN_QUESTION]
        elif stage == "verify-progress":
            package = Store(root).read_record(context["review_package_ref"])
            if package["review_kind"] == "proof":
                result["completion_status"] = self.completion
        return result


class CompletionLifecycleTests(OracleTestFixture, unittest.TestCase):
    def test_controller_completes_reviewed_goal_and_keeps_original_candidate(self):
        script = PendingFinalBackend()
        self.assertEqual(self.controller(script).run()["status"], "completed")
        proof_ref = self.store.get_meta("proof_ref")
        proof = self.store.read_record(proof_ref)
        self.assertEqual(proof["proof_draft"]["open_questions"], [OPEN_QUESTION])
        progress = self.store.read_record(self.store.get_meta("progress_ref"))
        self.assertEqual(progress["progress"]["status"], "completed")
        self.assertEqual(progress["progress"]["remaining"], [])
        candidate = self.store.read_record(self.store.get_meta("integration")["assessment_ref"])
        self.assertEqual(candidate["update"]["progress"]["status"], "in_progress")
        self.assertEqual(candidate["update"]["progress"]["remaining"], [PENDING_REVIEW])
        self.assertEqual(candidate["update"]["proof_draft"]["open_questions"], [OPEN_QUESTION])
        review = self.store.read_record(self.store.get_meta("final_review_ref"))
        self.assertEqual((review["verdict"], review["completion_status"]), ("pass", "completed"))
        self.assertIn(proof_ref["id"], review["checked_refs"])
        report = (self.root / "output/final.md").read_text()
        self.assertIn("Status: completed", report)
        self.assertIn(OPEN_QUESTION, report)

    def test_pass_partial_remains_partial_even_when_all_steps_checked(self):
        script = PendingFinalBackend(completion="partial")
        self.assertEqual(self.controller(script).run()["status"], "partial")
        progress = self.store.read_record(self.store.get_meta("progress_ref"))["progress"]
        self.assertEqual(progress["status"], "in_progress")
        self.assertEqual(progress["remaining"], [PENDING_REVIEW])
        self.assertEqual(self.store.read_record(self.store.get_meta("proof_ref"))[
            "proof_draft"]["open_questions"], [OPEN_QUESTION])

    def legacy_run(self):
        script = PendingFinalBackend()
        self.assertEqual(self.controller(script).run()["status"], "completed")
        old = self.store.read_record(self.store.get_meta("progress_ref"))
        legacy = copy.deepcopy(old)
        legacy["previous_ref"] = self.store.get_meta("progress_ref")
        legacy["progress"].update(status="in_progress", remaining=[PENDING_REVIEW])
        legacy["progress"]["items"][0].update(status="partial", remaining=[PENDING_REVIEW])
        progress_ref = self.store.write_record("goal_progress", legacy,
                                              request_id="fixture-legacy-pending-progress")
        conclusion_ref = self.store.write_record("conclusion", {
            "status": "partial", "summary": "Legacy pending final-review projection.",
            "result_refs": legacy["result_refs"], "remaining": [PENDING_REVIEW, OPEN_QUESTION]},
            request_id="fixture-legacy-partial-conclusion")
        basis = self.store.get_meta("finalization")
        basis.update(progress_ref=progress_ref, reason="goal_ready")
        self.store.set_meta(phase="done", status="partial", progress_ref=progress_ref,
                            conclusion_ref=conclusion_ref, finalization=basis,
                            stop_reason="goal_ready")
        return script, progress_ref, conclusion_ref

    def records(self):
        return {rid: self.store.read_record({"id": rid, "revision": row["revision"]})
                for rid, row in self.store.snapshot()[2].items()}

    def counts(self):
        return {key: self.store.get_meta(key) for key in (
            "round_no", "dispatch_count", "model_call_count", "audit_call_count")}

    def test_historical_reconciliation_is_append_only_and_idempotent(self):
        script, old_progress, old_conclusion = self.legacy_run()
        old_records, old_counts = self.records(), self.counts()
        proof_ref, review_ref = self.store.get_meta("proof_ref"), self.store.get_meta("final_review_ref")
        launches, calls = self.adapter.launches, list(script.calls)
        conclusions = self.store.reference_count("conclusion")
        progresses = self.store.reference_count("goal_progress")
        new_ref = reconcile_completed_run(self.store)
        self.assertNotEqual(new_ref, old_conclusion)
        self.assertEqual(new_ref, self.store.get_meta("conclusion_ref"))
        self.assertEqual(self.store.get_meta("status"), "completed")
        self.assertEqual(self.store.get_meta("phase"), "done")
        self.assertEqual(self.store.get_meta("stop_reason"), "")
        self.assertEqual(self.store.read_record(new_ref)["status"], "completed")
        self.assertNotEqual(self.store.get_meta("progress_ref"), old_progress)
        self.assertEqual(self.store.get_meta("proof_ref"), proof_ref)
        self.assertEqual(self.store.get_meta("final_review_ref"), review_ref)
        self.assertEqual(self.counts(), old_counts)
        self.assertEqual((self.adapter.launches, script.calls), (launches, calls))
        for rid, original in old_records.items():
            self.assertEqual(self.store.read_record(rid), original, rid)
        self.assertEqual(self.store.reference_count("conclusion"), conclusions + 1)
        self.assertEqual(self.store.reference_count("goal_progress"), progresses + 1)
        snapshot = self.store.snapshot()
        report = (self.root / "output/final.md").read_bytes()
        self.assertEqual(reconcile_completed_run(self.store), new_ref)
        self.assertEqual(self.store.snapshot(), snapshot)
        self.assertEqual((self.root / "output/final.md").read_bytes(), report)
        self.assertIn(OPEN_QUESTION.encode(), report)

    def test_historical_export_failure_replays_committed_correction(self):
        _, _, old_conclusion = self.legacy_run()
        before = self.store.reference_count("conclusion")
        with patch("colombo.brain.final_report.atomic_write", side_effect=OSError("Export interrupted")):
            with self.assertRaises(OSError):
                reconcile_completed_run(self.store)
        committed = self.store.get_meta("conclusion_ref")
        self.assertNotEqual(committed, old_conclusion)
        self.assertEqual(self.store.read_record(committed)["status"], "completed")
        self.assertEqual(self.store.reference_count("conclusion"), before + 1)
        self.assertEqual(reconcile_completed_run(self.store), committed)
        self.assertEqual(self.store.reference_count("conclusion"), before + 1)
        self.assertIn("Status: completed", (self.root / "output/final.md").read_text())
        self.assertIn(OPEN_QUESTION, (self.root / "proof/current.md").read_text())

    def test_mismatched_unreviewed_assessment_cannot_be_reconciled(self):
        _, _, _ = self.legacy_run()
        progress = self.store.read_record(self.store.get_meta("progress_ref"))
        original_assessment = progress["assessment_ref"]
        other = next({"id": rid, "revision": row["revision"]}
                     for rid, row in self.store.snapshot()[2].items()
                     if row["node_type"] == "assessment" and rid != original_assessment["id"])
        progress["assessment_ref"] = other
        invalid = self.store.write_record("goal_progress", progress,
                                         request_id="fixture-unreviewed-assessment-progress")
        self.store.set_meta(progress_ref=invalid)
        before = self.store.snapshot()
        with self.assertRaises(StoreError):
            reconcile_completed_run(self.store)
        self.assertEqual(self.store.snapshot(), before)

    def test_pending_model_call_cannot_be_reconciled(self):
        self.legacy_run()
        self.store.set_meta(pending_call={"call_id": "C00999", "role": "brain", "stage": "integrate"})
        before = self.store.snapshot()
        with self.assertRaises(StoreError):
            reconcile_completed_run(self.store)
        self.assertEqual(self.store.snapshot(), before)

    def test_unprocessed_result_cannot_be_reconciled(self):
        self.legacy_run()
        events = self.store.get_meta("result_events")
        events[0]["state"] = "processing"
        self.store.set_meta(result_events=events)
        before = self.store.snapshot()
        with self.assertRaises(StoreError):
            reconcile_completed_run(self.store)
        self.assertEqual(self.store.snapshot(), before)

    def test_live_workflow_cannot_be_reconciled(self):
        self.legacy_run()
        self.store.set_meta(phase="running", status="running")
        before = self.store.snapshot()
        with self.assertRaises(StoreError):
            reconcile_completed_run(self.store)
        self.assertEqual(self.store.snapshot(), before)

    def test_historical_pass_partial_cannot_be_reconciled_as_completed(self):
        script = PendingFinalBackend(completion="partial")
        self.assertEqual(self.controller(script).run()["status"], "partial")
        before = self.store.snapshot()
        with self.assertRaises(StoreError):
            reconcile_completed_run(self.store)
        self.assertEqual(self.store.snapshot(), before)

    def test_unresolved_global_review_cannot_be_reconciled(self):
        self.legacy_run()
        self.store.set_meta(unresolved_review_ref=self.store.get_meta("final_review_ref"))
        before = self.store.snapshot()
        with self.assertRaises(StoreError):
            reconcile_completed_run(self.store)
        self.assertEqual(self.store.snapshot(), before)

    def test_meta_only_result_change_after_validation_aborts_reconciliation(self):
        self.legacy_run()
        original = completion_recovery.final_progress_payload
        generation = self.store.get_meta("generation")
        old_conclusion = self.store.get_meta("conclusion_ref")
        conclusions = self.store.reference_count("conclusion")
        progresses = self.store.reference_count("goal_progress")

        def processing_result_after_validation(*args, **kwargs):
            payload = original(*args, **kwargs)
            events = self.store.get_meta("result_events")
            events[0]["state"] = "processing"
            self.store.set_meta(result_events=events)
            self.assertEqual(self.store.get_meta("generation"), generation)
            return payload

        with patch.object(completion_recovery, "final_progress_payload",
                          side_effect=processing_result_after_validation):
            with self.assertRaisesRegex(StoreError, "changed"):
                reconcile_completed_run(self.store)
        self.assertEqual(self.store.get_meta("conclusion_ref"), old_conclusion)
        self.assertEqual(self.store.get_meta("status"), "partial")
        self.assertEqual(self.store.reference_count("conclusion"), conclusions)
        self.assertEqual(self.store.reference_count("goal_progress"), progresses)
        self.assertEqual(self.store.get_meta("result_events")[0]["state"], "processing")

    def late_audit_blocks_writer(self, state):
        self.legacy_run()
        original = completion_recovery.final_progress_payload
        generation = self.store.get_meta("generation")
        old_conclusion = self.store.get_meta("conclusion_ref")
        conclusions = self.store.reference_count("conclusion")
        progresses = self.store.reference_count("goal_progress")
        request_id = "audit:fixture-late-" + state

        def audit_after_validation(*args, **kwargs):
            payload = original(*args, **kwargs)
            self.store.save_request(request_id, {"call_id": "fixture-late-audit"}, state)
            self.assertEqual(self.store.get_meta("generation"), generation)
            return payload

        with patch.object(completion_recovery, "final_progress_payload",
                          side_effect=audit_after_validation):
            with self.assertRaisesRegex(StoreError, "pending audit"):
                reconcile_completed_run(self.store)
        self.assertEqual(self.store.get_request(request_id)["state"], state)
        self.assertEqual(self.store.get_meta("conclusion_ref"), old_conclusion)
        self.assertEqual(self.store.get_meta("status"), "partial")
        self.assertEqual(self.store.reference_count("conclusion"), conclusions)
        self.assertEqual(self.store.reference_count("goal_progress"), progresses)

    def test_pending_audit_arriving_after_validation_blocks_writer(self):
        self.late_audit_blocks_writer("pending")

    def test_unknown_audit_arriving_after_validation_blocks_writer(self):
        self.late_audit_blocks_writer("unknown")

    def test_replay_revalidates_package_before_using_its_receipt(self):
        self.legacy_run()
        corrected = reconcile_completed_run(self.store)
        stage = self.store.get_meta("integration")
        package = self.store.read_record(stage["review_package_ref"])
        proof_ref = self.store.get_meta("proof_ref")
        other_proof = next({"id": rid, "revision": row["revision"]}
                           for rid, row in self.store.snapshot()[2].items()
                           if row["node_type"] == "proof_draft" and rid != proof_ref["id"])
        cases = []
        unrelated = copy.deepcopy(package)
        unrelated["proof_ref"] = other_proof
        cases.append(("unrelated-proof", unrelated))
        missing_source = copy.deepcopy(package)
        missing_source["required_checked_refs"].remove(self.store.get_meta("goal_ref")["id"])
        cases.append(("missing-required-goal", missing_source))
        for name, payload in cases:
            with self.subTest(case=name):
                bad_package = self.store.write_record("review_package", payload,
                    request_id="fixture-replay-package-" + name)
                changed_stage = copy.deepcopy(stage)
                changed_stage["review_package_ref"] = bad_package
                self.store.set_meta(integration=changed_stage)
                before = self.store.snapshot()
                with patch.object(completion_recovery, "_export") as export:
                    with self.assertRaises(StoreError):
                        reconcile_completed_run(self.store)
                    export.assert_not_called()
                self.assertEqual(self.store.snapshot(), before)
                self.assertEqual(self.store.get_meta("conclusion_ref"), corrected)
                self.store.set_meta(integration=stage)

    def test_replay_rejects_wrong_package_revision(self):
        self.legacy_run()
        corrected = reconcile_completed_run(self.store)
        stage = self.store.get_meta("integration")
        stage["review_package_ref"]["revision"] += 1
        self.store.set_meta(integration=stage)
        before = self.store.snapshot()
        with patch.object(completion_recovery, "_export") as export:
            with self.assertRaises(StoreError):
                reconcile_completed_run(self.store)
            export.assert_not_called()
        self.assertEqual(self.store.snapshot(), before)
        self.assertEqual(self.store.get_meta("conclusion_ref"), corrected)


if __name__ == "__main__":
    unittest.main()
