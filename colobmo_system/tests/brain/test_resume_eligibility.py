"""Frozen Result scheduling tests; no Cell lifecycle or model is started."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from colombo.brain.resume_eligibility import result_resume_eligibility, task_resume_eligibility


def result_for(stage="prover", *, used=15, limit=15):
    current = {"state": "none"}
    budget = {"used": used, "limit": limit, "remaining": max(0, limit-used)}
    if stage in {"verifier", "report_check", "sync"}:
        current = {"state": "active", "phase": {"verifier": "proof", "report_check": "report_check", "sync": "sync"}[stage],
                   "review_id": "r0001", "report_revision": 1,
                   "report_check": {"used": used, "limit": limit, "remaining": max(0, limit-used)}}
    if stage == "report_check":
        budget.update(review_id="r0001", report_revision=1)
    return {"task_id": "T0001", "attempt_id": "A0002", "assignment_ref": {"id": "assignment-1", "revision": 1},
            "package_ref": {"id": "package-1", "revision": 1}, "execution_status": "incomplete", "accepted": False,
            "stop_info": {"stage": stage, "kind": "incomplete"},
            "budget_snapshot": {stage: budget, "prover": budget if stage == "prover" else {"used": 15, "limit": 15, "remaining": 0},
                                "current_review": current, "submission_review": {"state": "none"}, "diagnostic_errors": []}}


def policy(prover=15, verifier=20, checker=4):
    return {"cell": {"settings": {"agents": {"prover_max_rounds": prover,
        "verifier_max_rounds": verifier, "report_check_max_attempts": checker}}}}


class MemoryStore:
    def __init__(self, result):
        self.result = deepcopy(result)
        self.reads = []

    def read_record(self, ref):
        self.reads.append(ref)
        return self.result

    def get_meta(self, key):
        assert key == "config"
        return policy()


class ResumeEligibilityTests(unittest.TestCase):
    def test_depleted_prover_requires_explicit_restart(self):
        outcome = result_resume_eligibility(result_for(), policy())
        self.assertEqual(outcome["status"], "blocked")
        self.assertEqual(outcome["suggested_mode"], "restart")
        self.assertEqual(outcome["restart_status"], "allowed")

    def test_remaining_prover_starts_allow_resume(self):
        self.assertEqual(result_resume_eligibility(result_for(used=14), policy())["status"], "allowed")

    def test_current_root_policy_increase_and_decrease_are_authoritative(self):
        self.assertEqual(result_resume_eligibility(result_for(), policy(prover=16))["status"], "allowed")
        self.assertEqual(result_resume_eligibility(result_for(used=14), policy(prover=10))["status"], "blocked")

    def test_review_with_remaining_starts_ignores_exhausted_prover(self):
        result = result_for("verifier", used=19, limit=20)
        self.assertEqual(result_resume_eligibility(result, policy())["status"], "allowed")
        result["budget_snapshot"]["verifier"]["used"] = 20
        self.assertEqual(result_resume_eligibility(result, policy())["suggested_mode"], "restart")

    def test_real_diagnostics_review_before_first_prover_ignores_only_missing_counter(self):
        from colombo.cell.diagnostics import read_stop_diagnostics
        project = Path(__file__).resolve().parents[2]
        temporary = project / "validation/tmp"
        temporary.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="resume-eligibility-", dir=temporary) as directory:
            root = Path(directory)
            (root / "reviews").mkdir()
            (root / "run.json").write_text(json.dumps(policy()["cell"]), encoding="utf-8")
            for stage, phase in (("verifier", "proof"), ("report_check", "report_check"), ("sync", "sync")):
                item = {"id": "r0001", "protocol": "cell-proof-review-5", "phase": phase,
                    "status": "pending_review", "report_revision": 1, "check_attempts": {"1": 1}, "launches": []}
                (root / "reviews/index.json").write_text(json.dumps({"protocol": "cell-proof-review-5",
                    "primary_launches": 1, "attempts": [item]}), encoding="utf-8")
                (root / "submission.json").write_text(json.dumps({"status": "pending_review", "review_id": "r0001"}), encoding="utf-8")
                with self.subTest(stage=stage):
                    diagnostic = read_stop_diagnostics(root, execution="incomplete", accepted=False, reason="fixture")
                    self.assertEqual(diagnostic["stop_info"]["stage"], stage)
                    self.assertEqual({e["path"] for e in diagnostic["budget_snapshot"]["diagnostic_errors"]},
                        {"runtime/prover_state.json", "runtime/prover_state.json:launches"})
                    self.assertEqual(result_resume_eligibility({"execution_status": "incomplete", "accepted": False,
                        **diagnostic}, policy())["status"], "allowed")
            # The same derived error from an existing malformed counter must
            # not be hidden: it is inconsistent state, not an unused counter.
            (root / "runtime").mkdir()
            (root / "runtime/prover_state.json").write_text('{"launches": true}', encoding="utf-8")
            diagnostic = read_stop_diagnostics(root, execution="incomplete", accepted=False, reason="fixture")
            self.assertEqual(result_resume_eligibility({"execution_status": "incomplete", "accepted": False,
                **diagnostic}, policy())["status"], "unknown")

    def test_ready_draft_starts_first_verifier(self):
        result = result_for("verifier", used=0, limit=20)
        result["budget_snapshot"]["current_review"] = {"state": "none"}
        self.assertEqual(result_resume_eligibility(result, policy())["status"], "allowed")

    def test_checker_quota_is_exact_report_and_not_restarted(self):
        result = result_for("report_check", used=4, limit=4)
        result["budget_snapshot"]["verifier"] = {"used": 20, "limit": 20, "remaining": 0}
        outcome = result_resume_eligibility(result, policy())
        self.assertEqual((outcome["status"], outcome["restart_status"]), ("blocked", "blocked"))
        self.assertEqual(outcome["suggested_mode"], "new")
        self.assertEqual(result_resume_eligibility(result, policy(checker=5))["status"], "allowed")

    def test_checker_remaining_allows_without_prover_or_verifier(self):
        result = result_for("report_check", used=3, limit=4)
        self.assertEqual(result_resume_eligibility(result, policy())["status"], "allowed")

    def test_checker_wrong_revision_and_counter_disagreement_are_unknown(self):
        result = result_for("report_check", used=3, limit=4)
        result["budget_snapshot"]["report_check"]["report_revision"] = 2
        self.assertEqual(result_resume_eligibility(result)["status"], "unknown")
        result["budget_snapshot"]["report_check"]["report_revision"] = 1
        result["budget_snapshot"]["current_review"]["report_check"]["used"] = 2
        self.assertEqual(result_resume_eligibility(result)["status"], "unknown")

    def test_sync_and_accepted_publication_do_not_need_starts(self):
        self.assertEqual(result_resume_eligibility(result_for("sync"), policy())["status"], "allowed")
        result = result_for("verifier", used=20, limit=20)
        result["budget_snapshot"]["current_review"] = {"state": "none"}
        result["budget_snapshot"]["submission_review"] = {"state": "bound", "phase": "complete", "status": "accepted",
            "review_id": "r0001", "report_revision": 1}
        self.assertEqual(result_resume_eligibility(result, policy())["stage"], "publication")
        self.assertEqual(result_resume_eligibility({"execution_status": "finished", "accepted": True})["status"], "allowed")

    def test_current_terminal_acceptance_does_not_require_unused_counters(self):
        result = result_for()
        result.update(accepted=True)
        result["stop_info"]["stage"] = "complete"
        self.assertEqual(result_resume_eligibility(result)["status"], "allowed")

    def test_publication_and_sync_preserve_restart_reconciliation_blockers(self):
        complete = result_for()
        complete["accepted"] = True
        complete["stop_info"]["stage"] = "complete"
        publication = result_for("verifier", used=20, limit=20)
        publication["budget_snapshot"].update(current_review={"state": "none"}, submission_review={
            "state": "bound", "phase": "complete", "status": "accepted", "review_id": "r0001", "report_revision": 1})
        for result in (complete, publication, result_for("sync")):
            result["budget_snapshot"]["restart_blockers"] = ["An unfinished hosted execution needs reconciliation"]
            with self.subTest(stage=result["stop_info"]["stage"]):
                answer = result_resume_eligibility(result, policy())
                self.assertEqual((answer["status"], answer["restart_status"]), ("allowed", "unknown"))

    def test_missing_unused_review_files_still_block_real_depleted_prover(self):
        result = result_for()
        result["budget_snapshot"]["current_review"] = {"state": "unknown"}
        result["budget_snapshot"]["diagnostic_errors"] = [
            {"path": "reviews/index.json", "reason": "missing"}, {"path": "submission.json", "reason": "missing"},
            {"path": "reviews/index.json:primary_launches", "reason": "missing or invalid nonnegative integer"}]
        self.assertEqual(result_resume_eligibility(result, policy())["status"], "blocked")

    def test_unknown_or_inconsistent_lifecycle_never_grants_restart(self):
        for result in ({"execution_status": "incomplete"}, result_for("unknown"), {**result_for(), "execution_status": "unknown"}):
            with self.subTest(result=result):
                answer = result_resume_eligibility(result)
                self.assertEqual((answer["status"], answer["restart_status"]), ("unknown", "unknown"))
        result = result_for("report_check", used=1, limit=4)
        result["budget_snapshot"]["current_review"]["phase"] = "proof"
        self.assertEqual(result_resume_eligibility(result)["status"], "unknown")
        result = result_for()
        result["budget_snapshot"]["diagnostic_errors"] = [{"path": "reviews/index.json", "reason": "corrupt"}]
        self.assertEqual(result_resume_eligibility(result)["status"], "unknown")

    def test_bad_counters_remain_unknown(self):
        for value in (None, True, -1, "15"):
            result = result_for()
            result["budget_snapshot"]["prover"]["used"] = value
            self.assertEqual(result_resume_eligibility(result)["status"], "unknown")

    def test_malformed_diagnostic_fields_fail_closed_without_crashing(self):
        for key, value in (("current_review", "broken"), ("current_review", {"state": []}),
                           ("diagnostic_errors", [{"path": "reviews/index.json", "reason": {}}])):
            result = result_for()
            result["budget_snapshot"][key] = value
            self.assertEqual(result_resume_eligibility(result)["status"], "unknown")
        result = result_for()
        result["stop_info"]["stage"] = []
        self.assertEqual(result_resume_eligibility(result)["status"], "unknown")

    def test_uncompleted_experiment_has_its_own_native_budget(self):
        result = result_for("experiment_native", used=14, limit=15)
        result["evidence_kind"] = "empirical"
        self.assertEqual(result_resume_eligibility(result, policy())["status"], "allowed")
        result["budget_snapshot"]["experiment_native"]["used"] = 15
        answer = result_resume_eligibility(result, policy())
        self.assertEqual((answer["status"], answer["restart_status"]), ("blocked", "allowed"))
        result["budget_snapshot"]["restart_blockers"] = ["An existing hosted execution requires reconciliation"]
        answer = result_resume_eligibility(result, policy())
        self.assertEqual((answer["status"], answer["restart_status"]), ("blocked", "unknown"))

    def test_restart_baseline_uses_current_policy_including_decrease(self):
        result = result_for(used=27, limit=30)
        result["budget_snapshot"]["restart_cycle"] = {"scope": {key: result[key] for key in
            ("task_id", "attempt_id", "assignment_ref", "package_ref")}, "baselines": {"prover": 15, "verifier": 0}}
        answer = result_resume_eligibility(result, policy(prover=15))
        self.assertEqual((answer["status"], answer["budget"]["limit"]), ("allowed", 30))
        answer = result_resume_eligibility(result, policy(prover=10))
        self.assertEqual((answer["status"], answer["budget"]["limit"]), ("blocked", 25))
        result["budget_snapshot"]["restart_cycle"]["scope"]["task_id"] = "T9999"
        self.assertEqual(result_resume_eligibility(result, policy())["status"], "unknown")

    def test_task_checks_scope_and_reads_no_live_cell(self):
        result = result_for()
        store = MemoryStore(result)
        task = {key: result[key] for key in ("task_id", "assignment_ref", "package_ref")}
        task.update(state="returned", active_attempt="A0002", finished_attempt="A0002", latest_result_ref={"id": "result-1"})
        before = deepcopy((store.result, task))
        self.assertEqual(task_resume_eligibility(store, task)["status"], "blocked")
        self.assertEqual((store.result, task), before)
        self.assertEqual(store.reads, [task["latest_result_ref"]])
        for key, bad in (("assignment_ref", {"id": "other"}), ("package_ref", {"id": "other"}),
                         ("finished_attempt", "A0001"), ("state", "running")):
            with self.subTest(key=key):
                self.assertEqual(task_resume_eligibility(store, {**task, key: bad})["status"], "unknown")


if __name__ == "__main__":
    unittest.main()
