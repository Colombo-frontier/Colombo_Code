"""Synthetic persisted Cell states; no models or experimental runners are used."""
from __future__ import annotations

import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from colombo.cell.diagnostics import read_stop_diagnostics


PROJECT = Path(__file__).resolve().parents[2]
from colombo.cell import worker as worker
PROTOCOL = "cell-proof-review-5"


class CellDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        temporary_root = PROJECT / "validation/tmp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="diagnostics-", dir=temporary_root)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.put("run.json", {"settings": {"agents": {"prover_max_rounds": 3,
            "verifier_max_rounds": 3, "report_check_max_attempts": 2}}})
        self.put("runtime/prover_state.json", {"launches": 3})
        self.put("reviews/index.json", {"protocol": PROTOCOL, "primary_launches": 0, "attempts": []})

    def put(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def result(self, **options):
        return read_stop_diagnostics(self.root, **{"execution": "incomplete", "accepted": False,
                                     "reason": "Cell runner exited with code 2", **options})

    def review(self, phase, *, primary=1, revision=2, checks=None, reason="pending", launches=None):
        item = {"id": "r0001", "protocol": PROTOCOL, "phase": phase, "report_revision": revision,
                "check_attempts": {str(revision): 2} if checks is None else checks,
                "launches": launches or []}
        self.put("reviews/index.json", {"protocol": PROTOCOL, "primary_launches": primary, "attempts": [item]})
        self.put("submission.json", {"status": "review_incomplete", "review_id": "r0001", "review_reason": reason})
        return item

    def test_prover_budget_is_read_only_and_repeatable(self):
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        first, second = self.result(), self.result()
        self.assertEqual(first, second)
        self.assertEqual(first["budget_snapshot"]["prover"], {"used": 3, "limit": 3, "remaining": 0})
        self.assertEqual(first["stop_info"]["kind"], "budget_exhausted")
        self.assertEqual(first["stop_info"]["stage"], "prover")
        self.assertEqual(before, {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_actual_saved_alias_limits_follow_cell_precedence(self):
        config = json.loads((self.root / "run.json").read_text())
        config["max_prover_rounds"] = 7
        config["max_review_rounds"] = 5
        self.put("run.json", config)
        result = self.result()
        self.assertEqual(result["budget_snapshot"]["prover"], {"used": 3, "limit": 7, "remaining": 4})
        self.assertEqual(result["budget_snapshot"]["verifier"]["limit"], 5)
        self.assertEqual(result["stop_info"]["kind"], "incomplete")

    def test_exhausted_prover_does_not_prevent_ready_review(self):
        self.put("submission.json", {"status": "ready"})
        result = self.result()
        self.assertEqual(result["stop_info"]["stage"], "verifier")
        self.assertEqual(result["stop_info"]["kind"], "incomplete")
        self.assertEqual(result["budget_snapshot"]["verifier"]["remaining"], 3)

    def test_primary_exhaustion_before_first_review_record(self):
        self.put("submission.json", {"status": "review_incomplete",
            "review_reason": "The cumulative primary verifier budget is exhausted."})
        self.put("reviews/index.json", {"protocol": PROTOCOL, "primary_launches": 3, "attempts": []})
        result = self.result()
        self.assertEqual(result["stop_info"]["stage"], "verifier")
        self.assertEqual(result["stop_info"]["kind"], "budget_exhausted")

    def test_checker_count_is_bound_to_exact_report_revision(self):
        self.review("report_check", revision=3, checks={"1": 20, "2": 8, "3": 2},
                    reason="Independent checker budget exhausted for this exact report; no provisional feedback is released.")
        result = self.result()
        self.assertEqual(result["budget_snapshot"]["report_check"], {
            "review_id": "r0001", "report_revision": 3, "used": 2, "limit": 2, "remaining": 0})
        self.assertEqual(result["stop_info"]["kind"], "budget_exhausted")
        self.assertEqual(result["stop_info"]["stage"], "report_check")

    def test_primary_review_budget_is_distinct_from_prover_budget(self):
        self.put("runtime/prover_state.json", {"launches": 1})
        self.review("proof", primary=3, reason="Primary verifier process budget exhausted; unfinished audit remains with verifier.")
        result = self.result()
        self.assertEqual(result["stop_info"]["kind"], "budget_exhausted")
        self.assertEqual(result["stop_info"]["stage"], "verifier")
        self.assertEqual(result["budget_snapshot"]["prover"]["remaining"], 2)

    def test_new_report_revision_does_not_inherit_previous_check_count(self):
        self.review("report_check", revision=3, checks={"2": 8})
        result = self.result()
        self.assertEqual(result["budget_snapshot"]["report_check"]["used"], 0)
        self.assertEqual(result["stop_info"]["kind"], "incomplete")

    def test_completed_submission_keeps_exact_review_usage_without_current_work(self):
        item = self.review("complete", revision=1, checks={"1": 1}, launches=[
            {"stage": "proof", "status": "report_saved"},
            {"stage": "report_check", "status": "confirmed"}])
        item["status"] = "accepted"
        self.put("reviews/index.json", {"protocol": PROTOCOL, "primary_launches": 3,
            "attempts": [item, {**item, "id": "r0002", "report_revision": 2, "check_attempts": {"2": 2}}]})
        self.put("submission.json", {"status": "accepted", "review_id": "r0001"})
        self.put("reviews/r0001/confirmation.json", {"review_id": "r0001", "report_revision": 1,
                                                    "verdict": "confirmed"})
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*.json")}
        result = self.result(execution="finished", accepted=True)
        budgets = result["budget_snapshot"]
        self.assertEqual(budgets["current_review"]["state"], "none")
        self.assertIsNone(budgets["current_review"]["report_check"]["used"])
        self.assertEqual(budgets["report_check"], {"review_id": "r0001", "report_revision": 1,
                                                 "used": 1, "limit": 2, "remaining": 1})
        self.assertEqual(budgets["submission_review"]["phase"], "complete")
        self.assertEqual(budgets["submission_review"]["status"], "accepted")
        self.assertEqual(budgets["submission_review"]["primary_launches"], 1)
        self.assertEqual(budgets["submission_review"]["revision_source"], "review_index")
        self.assertEqual(budgets["verifier"]["used"], 3)
        self.assertEqual(result["stop_info"]["review_id"], "r0001")
        self.assertEqual(result, self.result(execution="finished", accepted=True))
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*.json")})

    def test_current_review_and_submission_report_are_separate(self):
        completed = self.review("complete", revision=1, checks={"1": 1})
        active = {**completed, "id": "r0002", "phase": "report_check", "report_revision": 3,
                  "check_attempts": {"3": 2}}
        self.put("reviews/index.json", {"protocol": PROTOCOL, "primary_launches": 2,
                                        "attempts": [completed, active]})
        self.put("submission.json", {"status": "accepted", "review_id": "r0001", "report_revision": 1})
        budgets = self.result()["budget_snapshot"]
        self.assertEqual(budgets["current_review"]["review_id"], "r0002")
        self.assertEqual(budgets["current_review"]["report_check"]["used"], 2)
        self.assertEqual(budgets["submission_review"]["review_id"], "r0001")
        self.assertEqual(budgets["submission_review"]["report_check"]["used"], 1)
        self.assertEqual(budgets["report_check"]["review_id"], "r0002")

    def test_completed_report_missing_counter_stays_unknown(self):
        self.review("complete", revision=3, checks={"2": 1})
        self.put("submission.json", {"status": "accepted", "review_id": "r0001"})
        budgets = self.result(accepted=True)["budget_snapshot"]
        self.assertIsNone(budgets["report_check"]["used"])
        self.assertIsNone(budgets["report_check"]["remaining"])
        self.assertTrue(budgets["diagnostic_errors"])

    def test_submission_wrong_id_revision_or_duplicate_identity_does_not_guess(self):
        item = self.review("complete", revision=2, checks={"2": 1})
        for submission in ({"review_id": "r9999"}, {"review_id": "r0001", "report_revision": 1},
                           {"review_id": "r0001", "report_revision": True}, {"review_id": "../other"}):
            with self.subTest(submission=submission):
                self.put("submission.json", {"status": "accepted", **submission})
                budgets = self.result(accepted=True)["budget_snapshot"]
                self.assertEqual(budgets["submission_review"]["state"], "unknown")
                self.assertIsNone(budgets["report_check"]["used"])
        self.put("submission.json", {"status": "accepted", "review_id": "r0001"})
        self.put("reviews/index.json", {"protocol": PROTOCOL, "primary_launches": 2,
                                        "attempts": [item, item]})
        self.assertIsNone(self.result()["budget_snapshot"]["report_check"]["used"])

    def test_completed_confirmation_wrong_version_does_not_supply_usage(self):
        self.review("complete", revision=2, checks={"1": 1, "2": 2})
        self.put("submission.json", {"status": "accepted", "review_id": "r0001"})
        for confirmation in ({"review_id": "r0001", "report_revision": 1},
                             {"review_id": "r0002", "report_revision": 2}):
            self.put("reviews/r0001/confirmation.json", confirmation)
            budgets = self.result(accepted=True)["budget_snapshot"]
            self.assertEqual(budgets["submission_review"]["state"], "unknown")
            self.assertIsNone(budgets["report_check"]["used"])
            self.assertTrue(any("confirmation identity" in e["reason"] for e in budgets["diagnostic_errors"]))

    def test_sync_is_not_a_model_budget_exhaustion(self):
        self.review("sync", primary=3, reason="Confirmed review awaits trust synchronization: StoreError: locked")
        result = self.result()
        self.assertEqual(result["stop_info"]["stage"], "sync")
        self.assertEqual(result["stop_info"]["kind"], "incomplete")
        self.assertIn("synchronization", result["stop_info"]["message"])

    def test_invalid_review_inputs_are_not_relabelled_as_exhaustion(self):
        self.review("proof", primary=3, reason="An unfinished review's frozen submission changed; restore it before resuming.")
        self.assertEqual(self.result()["stop_info"]["kind"], "incomplete")

    def test_current_reviewer_error_is_reported_alongside_budget_snapshot(self):
        self.review("proof", primary=3, launches=[{"stage": "proof", "status": "execution_error", "reason": "ValueError: malformed report"}],
                    reason="The verifier stage needs continuation; see its handoff and internal error record.")
        result = self.result()
        self.assertEqual(result["stop_info"]["kind"], "runtime_error")
        self.assertIn("malformed report", result["stop_info"]["message"])
        self.assertEqual(result["budget_snapshot"]["verifier"]["remaining"], 0)

    def test_stale_error_from_other_review_phase_is_not_current_failure(self):
        self.review("sync", primary=3, launches=[{"stage": "proof", "status": "execution_error"}])
        self.assertEqual(self.result()["stop_info"]["kind"], "incomplete")

    def test_explicit_faults_take_precedence_and_acceptance_is_independent(self):
        for kind in ("mathematical_error", "runtime_error", "timeout"):
            with self.subTest(kind=kind):
                result = self.result(failure={"kind": kind, "message": "fixed fact"})
                self.assertEqual(result["stop_info"]["kind"], kind)
                self.assertEqual(result["stop_info"]["message"], "fixed fact")
        result = self.result(execution="timeout", accepted=True)
        self.assertEqual(result["stop_info"]["kind"], "timeout")
        self.assertEqual(result["stop_info"]["stage"], "complete")
        self.assertEqual(self.result(execution="cancelled")["stop_info"]["kind"], "cancelled")

    def test_missing_and_corrupted_data_stay_unknown(self):
        self.put("run.json", {"settings": {"agents": {"prover_max_rounds": True}}})
        self.put("runtime/prover_state.json", {"launches": True})
        (self.root / "reviews/index.json").write_text("not JSON", encoding="utf-8")
        result = self.result()
        self.assertEqual(result["budget_snapshot"]["prover"], {"used": None, "limit": None, "remaining": None})
        self.assertIsNone(result["budget_snapshot"]["verifier"]["used"])
        self.assertEqual(result["stop_info"]["stage"], "unknown")
        self.assertEqual(result["stop_info"]["kind"], "incomplete")
        self.assertTrue(result["budget_snapshot"]["diagnostic_errors"])

    def test_multiple_pending_reviews_do_not_guess_a_current_report(self):
        first = self.review("report_check")
        self.put("reviews/index.json", {"protocol": PROTOCOL, "primary_launches": 3,
            "attempts": [first, {**first, "id": "r0002"}]})
        result = self.result()
        self.assertEqual(result["stop_info"]["stage"], "unknown")
        self.assertIsNone(result["budget_snapshot"]["report_check"]["review_id"])

    def test_foreign_protocol_attempt_is_unknown_not_a_prover_budget_stop(self):
        item = self.review("proof", primary=3)
        self.put("reviews/index.json", {"protocol": PROTOCOL, "primary_launches": 3,
            "attempts": [{**item, "protocol": "unsupported"}]})
        result = self.result()
        self.assertEqual(result["stop_info"]["stage"], "unknown")
        self.assertEqual(result["stop_info"]["kind"], "incomplete")
        self.assertIsNone(result["budget_snapshot"]["verifier"]["used"])

    def test_export_freezes_diagnostics_and_replay_reuses_original(self):
        task = self.root / "T0001"
        cell = task / "cell"
        for source in list(self.root.rglob("*.json")):
            target = cell / source.relative_to(self.root)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
        request_path = task / "attempts/A0001/request.json"
        request_path.parent.mkdir(parents=True)
        request_path.write_text(json.dumps({"task_id": "T0001", "attempt_id": "A0001", "task_dir": str(task),
            "project_root": str(PROJECT), "assignment_ref": {"id": "assignment-1"}, "package_ref": {"id": "package-1"}}), encoding="utf-8")
        with patch.object(worker, "_cell_imports", return_value=(None, None, Path, None, None, lambda root: False)):
            first = worker.export_result(request_path, "incomplete", "Cell runner exited with code 2")
            (cell / "runtime/prover_state.json").write_text('{"launches":99}', encoding="utf-8")
            second = worker.export_result(request_path, "incomplete", "different live state")
        self.assertEqual(first, second)
        self.assertEqual(first["budget_snapshot"]["prover"]["used"], 3)
        frozen = task / "results/A0001/artifacts/runtime/prover_state.json"
        self.assertEqual(json.loads(frozen.read_text())["launches"], 3)
        self.assertEqual(json.loads((cell / "runtime/prover_state.json").read_text())["launches"], 99)


if __name__ == "__main__":
    unittest.main()
