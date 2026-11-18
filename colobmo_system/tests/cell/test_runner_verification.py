"""Exercise Python-owned draft/review cycles without paid model calls."""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock
from unittest.mock import patch

import colombo.cell.model_calls as processes
import colombo.cell.controller as run
import colombo.cell.settings as settings
from colombo.cell.verifier.proof_review import manuscript_is_current
from colombo.cell.verifier.proof_review import review_submission as _review_submission
from review_fixtures import confirmation_result

def review_submission(work, reviewer=None, **kwargs):
    return _review_submission(work, reviewer=reviewer, report_checker=confirmation_result, **kwargs)


ROOT = Path(__file__).resolve().parents[2]
PROBLEM = "Prove that n(n + 1) is even for every integer n."
PROOF = "One of the consecutive integers n and n + 1 is even, so their product is even."
BAD_PROOF = "Since n is even, n(n + 1) is even."
CORRECT = {
    "verdict": "pass", "summary": "Consecutive integers contain an even factor.",
    "target_alignment": "The argument covers every integer n in the original target.",
    "coverage": "Check 1 aligns the integer domain, 2 checks adjacent parity, and 3 checks the product conclusion. No external results are required.",
    "checks": [
        {"id": 1, "subject": "Integer domain and target", "location": "problem.md; draft.md", "status": "pass", "reason": "Both quantify over every integer n."},
        {"id": 2, "subject": "Consecutive parity", "location": "draft.md, first clause", "status": "pass", "reason": "If n=2k it is even; if n=2k+1 then n+1=2(k+1)."},
        {"id": 3, "subject": "Even factor implies even product", "location": "draft.md, final clause", "status": "pass", "reason": "An even factor 2k times an integer m is 2(km)."},
    ],
    "findings": [], "sources": [],
}
WRONG = deepcopy(CORRECT)
WRONG.update(verdict="revise", summary="The proof assumes n is even without justification.",
             target_alignment="The odd-integer cases of the original target are missing.")
WRONG["checks"][2].update(status="fail", reason="The premise allows odd n.")
WRONG["findings"] = [{"id": "missing-odd-case", "check_id": 3, "kind": "gap",
                      "location": "draft.md, first sentence",
                      "explanation": "The hypotheses do not imply that n is even.",
                      "repair": "Handle odd n by showing that n + 1 is even."}]


class RunnerVerificationTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        temporary = tempfile.TemporaryDirectory(prefix=".runner-test-", dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.problem = self.root / "source.md"
        self.problem.write_text(PROBLEM, encoding="utf-8")
        self.policy = settings.load_policy(profile="hard")
        policy_loader = patch.object(settings, "load_policy", side_effect=lambda *a, **k: deepcopy(self.policy))
        policy_loader.start()
        self.addCleanup(policy_loader.stop)

    def workspace(self, name="run", *, prover_rounds=3, review_rounds=3,
                  prover_timeout=11, verifier_timeout=73):
        work = self.root / name
        # Lifecycle limits are selected by the run owner, not task-local edits.
        self.policy["cell"]["settings"]["agents"].update(
            prover_max_rounds=prover_rounds, verifier_max_rounds=review_rounds)
        run.initialize(self.problem, work)
        config = self.read(work / "run.json")
        config["settings"]["agents"].update(
            prover_max_rounds=prover_rounds, verifier_max_rounds=review_rounds,
            prover_timeout_seconds=prover_timeout, verifier_timeout_seconds=verifier_timeout,
        )
        config.update(settings.run_fields(config["settings"]))
        self.write(work / "run.json", config)
        return work

    @staticmethod
    def read(path):
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def write(path, value):
        path.write_text(json.dumps(value), encoding="utf-8")

    def submit(self, work, proof=PROOF, status="ready"):
        (work / "draft.md").write_text(proof, encoding="utf-8")
        self.write(work / "submission.json", {
            "status": status, "outcome": "proved", "draft_file": "draft.md",
        })

    @staticmethod
    def prover_result(output):
        return {"session_id": "fake-prover", "log_path": str(output)}

    def verifier_result(self, directory, report=CORRECT):
        if self.read(directory / "review_request.json").get("stage") == "report_check":
            return confirmation_result(directory)
        self.write(directory / "review_report.json", report)
        self.write(directory / "review_notes.json", {
            key: report[key] for key in ("checks", "findings", "sources")
        })
        request = self.read(directory / "review_request.json")
        receipt = {"review_id": request["review_id"], "report_revision": request["report_revision"],
                   "verdict": report["verdict"]}
        return {"returncode": 0, "text": json.dumps(receipt)}

    def reviewer(self, *reports):
        queue = iter(reports or (CORRECT,))

        def process(prompt, directory, output, **kwargs):
            if self.read(directory / "review_request.json").get("stage") == "report_check":
                return confirmation_result(directory)
            item = next(queue)
            if isinstance(item, Exception):
                raise item
            return self.verifier_result(directory, item)

        return process

    def reviews(self, work):
        return self.read(work / "reviews" / "index.json")["attempts"]

    def test_ready_submission_is_reviewed_after_prover_returns_and_receipt_is_reused(self):
        work = self.workspace()
        order = []
        review_workspaces = []

        def prover(prompt, directory, output, **kwargs):
            order.append("prover_started")
            self.submit(directory)
            self.assertFalse((directory / "reviews").exists())
            order.append("prover_returned")
            return self.prover_result(output)

        def verifier(prompt, directory, output, **kwargs):
            order.append("verifier_started")
            review_workspaces.append(directory)
            return self.verifier_result(directory)

        with patch.object(run, "run_agent", side_effect=prover) as proof_process, \
                patch.object(processes, "run_agent", side_effect=verifier) as review_process:
            self.assertEqual(run.solve(work), 0)
            self.assertEqual(run.solve(work), 0)
        self.assertEqual(order, ["prover_started", "prover_returned", "verifier_started", "verifier_started"])
        proof_process.assert_called_once()
        self.assertEqual(review_process.call_count, 2)
        self.assertEqual(review_process.call_args.kwargs["role"], "verifier")
        self.assertNotEqual(review_workspaces[0], work)
        self.assertEqual((review_workspaces[0] / "input" / "draft.md").read_text(encoding="utf-8"), PROOF)
        self.assertEqual((review_workspaces[0] / "input" / "problem.md").read_text(encoding="utf-8"), PROBLEM)
        self.assertTrue(manuscript_is_current(work))
        self.assertEqual(self.read(work / "submission.json")["status"], "accepted")
        self.assertEqual([record["status"] for record in self.reviews(work)], ["accepted"])
        self.assertIn(PROOF, (work / "manuscript.md").read_text(encoding="utf-8"))

    def test_rejected_draft_is_repaired_from_saved_report_in_a_new_prover_process(self):
        work = self.workspace()
        attempts = []
        repaired_from = []

        def prover(prompt, directory, output, **kwargs):
            attempts.append(output)
            if len(attempts) == 1:
                self.submit(directory, BAD_PROOF)
            else:
                submission = self.read(directory / "submission.json")
                self.assertEqual(submission["status"], "needs_revision")
                report = self.read(directory / "reviews" / submission["review_id"] / "report.json")
                repaired_from.append(report)
                self.assertEqual((directory / "draft.md").read_text(encoding="utf-8"), BAD_PROOF)
                self.submit(directory, PROOF)
            return self.prover_result(output)

        with patch.object(run, "run_agent", side_effect=prover), \
                patch.object(processes, "run_agent", side_effect=self.reviewer(WRONG, CORRECT)) as reviewer:
            self.assertEqual(run.solve(work), 0)
        self.assertEqual(len(attempts), 2)
        self.assertNotEqual(attempts[0], attempts[1])
        self.assertEqual(reviewer.call_count, 4)
        self.assertEqual(repaired_from, [WRONG])
        records = self.reviews(work)
        self.assertEqual([record["status"] for record in records], ["revise", "accepted"])
        self.assertNotEqual(records[0]["id"], records[1]["id"])
        for record, proof in zip(records, (BAD_PROOF, PROOF)):
            frozen = work / "reviews" / record["id"] / "workspace" / "input" / "draft.md"
            self.assertEqual(frozen.read_text(encoding="utf-8"), proof)
        self.assertTrue(manuscript_is_current(work))

    def test_prover_transport_failure_after_ready_keeps_review_under_same_root_budget(self):
        work = self.workspace(prover_timeout=11, verifier_timeout=73)

        def prover(prompt, directory, output, **kwargs):
            self.submit(directory)
            raise TimeoutError("Prover transport failed after saving the submission")

        with patch.object(run, "run_agent", side_effect=prover) as proof_process, \
                patch.object(processes, "run_agent", side_effect=self.reviewer()) as review_process:
            self.assertEqual(run.solve(work), 0)
        self.assertEqual(proof_process.call_args.kwargs["timeout"], "unlimited")
        self.assertEqual([call.kwargs["timeout"] for call in review_process.call_args_list], ["unlimited", "unlimited"])
        self.assertTrue(manuscript_is_current(work))
        events = [json.loads(line) for line in (work / "run_events.jsonl").read_text(encoding="utf-8").splitlines()]
        actions = [event["action"] for event in events]
        self.assertLess(actions.index("prover_error"), actions.index("draft_review"))

    def test_missing_unready_and_forged_accepted_submissions_never_claim_success(self):
        for status in (None, "draft", "accepted"):
            with self.subTest(status=status):
                work = self.workspace(str(status), prover_rounds=1)

                def prover(prompt, directory, output, **kwargs):
                    if status is not None:
                        self.submit(directory, status=status)
                    return self.prover_result(output)

                with patch.object(run, "run_agent", side_effect=prover) as proof_process, \
                        patch.object(processes, "run_agent") as review_process:
                    self.assertEqual(run.solve(work), 2)
                proof_process.assert_called_once()
                review_process.assert_not_called()
                self.assertFalse(manuscript_is_current(work))
                self.assertFalse((work / "manuscript.md").exists())
                self.assertFalse((work / "reviews" / "index.json").exists())

    def test_prover_and_review_limits_both_end_without_success(self):
        work = self.workspace(prover_rounds=1)
        def prover(prompt, directory, output, **kwargs):
            self.submit(directory, BAD_PROOF)
            return self.prover_result(output)
        with patch.object(run, "run_agent", side_effect=prover) as proof_process, \
                patch.object(processes, "run_agent", side_effect=self.reviewer(WRONG)) as reviewer:
            self.assertEqual(run.solve(work), 2)
        proof_process.assert_called_once()
        self.assertEqual(reviewer.call_count, 2)
        self.assertEqual(self.read(work / "submission.json")["status"], "needs_revision")
        self.assertFalse(manuscript_is_current(work))

        limited = self.workspace("primary-limit", review_rounds=1)
        self.submit(limited, BAD_PROOF)
        self.assertEqual(review_submission(limited, lambda folder: self.verifier_result(folder, WRONG))["status"], "needs_revision")
        self.submit(limited, PROOF)
        no_budget = Mock(side_effect=AssertionError("No new primary process is allowed"))
        self.assertEqual(review_submission(limited, no_budget)["status"], "review_incomplete")
        no_budget.assert_not_called()
        self.assertEqual(len(self.reviews(limited)), 1)
        self.assertFalse(manuscript_is_current(limited))
    def test_verifier_timeout_resumes_same_stage_without_launching_another_prover(self):
        work = self.workspace()
        attempts = []
        verifier_workspaces = []
        queued = self.reviewer(TimeoutError("Verifier service timed out"), CORRECT)

        def prover(prompt, directory, output, **kwargs):
            attempts.append(output)
            self.submit(directory, PROOF)
            return self.prover_result(output)

        def verifier(prompt, directory, output, **kwargs):
            verifier_workspaces.append(directory)
            return queued(prompt, directory, output, **kwargs)

        with patch.object(run, "run_agent", side_effect=prover), \
                patch.object(processes, "run_agent", side_effect=verifier) as reviewer:
            self.assertEqual(run.solve(work), 0)
        self.assertEqual(len(attempts), 1)
        self.assertEqual(reviewer.call_count, 3)
        self.assertEqual(verifier_workspaces[0], verifier_workspaces[1])
        self.assertNotEqual(verifier_workspaces[1], verifier_workspaces[2])
        records = self.reviews(work)
        self.assertEqual([record["status"] for record in records], ["accepted"])
        self.assertEqual([item["stage"] for item in records[0]["launches"]], ["proof", "proof", "report_check"])
        self.assertEqual(self.read(work / "reviews" / "index.json")["primary_launches"], 2)
        self.assertTrue(manuscript_is_current(work))
    def test_unresolved_citation_can_be_rechecked_without_changing_the_draft(self):
        work = self.workspace()
        self.submit(work, PROOF + " This is also the elementary parity lemma cited here.")
        unresolved = deepcopy(CORRECT)
        unresolved.update(verdict="inconclusive", summary="The cited parity lemma is not yet checked.")
        unresolved["checks"][2].update(status="unresolved", reason="The source could not be read.")
        unresolved["findings"] = [{"id": "source-unread", "check_id": 3, "kind": "uncertain",
                                   "location": "draft.md, citation",
                                   "explanation": "The source statement is not yet available.",
                                   "repair": "Obtain and compare the cited statement."}]
        unresolved["sources"] = [{"citation": "Elementary parity lemma", "location": "draft.md, citation",
                                  "status": "unavailable", "evidence": "Simulated first lookup timed out.",
                                  "application": "The lemma is invoked for the even factor.", "check_id": 3}]
        confirmed = deepcopy(CORRECT)
        confirmed["checks"][2].update(reason="The cited parity statement applies to integer n.")
        confirmed["sources"] = [{**unresolved["sources"][0], "status": "confirmed",
                                  "evidence": "The simulated source states that consecutive integers have an even factor."}]
        self.assertEqual(review_submission(work, reviewer=lambda directory: self.verifier_result(directory, unresolved))["status"], "needs_revision")
        self.assertFalse(manuscript_is_current(work))
        submission = self.read(work / "submission.json")
        submission["status"] = "ready"
        self.write(work / "submission.json", submission)
        self.assertEqual(review_submission(work, reviewer=lambda directory: self.verifier_result(directory, confirmed))["status"], "accepted")
        records = self.reviews(work)
        self.assertEqual([item["status"] for item in records], ["inconclusive", "accepted"])
        self.assertNotEqual(records[0]["id"], records[1]["id"])
        self.assertTrue(manuscript_is_current(work))

    def test_malformed_or_inconsistent_reports_never_publish(self):
        for fault in ("malformed", "empty_checks", "contradictory_verdict", "saved_notes",
                      "missing_notes", "missing_report", "receipt_id", "receipt_revision",
                      "receipt_verdict", "receipt_path", "old_full_report"):
            with self.subTest(fault=fault):
                work = self.workspace(fault)
                self.submit(work)

                def reviewer(directory):
                    result = self.verifier_result(directory)
                    if fault == "malformed":
                        result["text"] = "not JSON"
                    elif fault in {"empty_checks", "contradictory_verdict"}:
                        report = deepcopy(CORRECT if fault == "empty_checks" else WRONG)
                        if fault == "empty_checks":
                            report["checks"].clear()
                        else:
                            report["verdict"] = "pass"
                        result = self.verifier_result(directory, report)
                    elif fault == "saved_notes":
                        notes = self.read(directory / "review_notes.json")
                        notes["checks"][0]["reason"] = "A different persisted check."
                        self.write(directory / "review_notes.json", notes)
                    elif fault == "missing_notes":
                        (directory / "review_notes.json").unlink()
                    elif fault == "missing_report":
                        (directory / "review_report.json").unlink()
                    elif fault == "old_full_report":
                        result["text"] = json.dumps(CORRECT)
                    else:
                        receipt = json.loads(result["text"])
                        key, value = {
                            "receipt_id": ("review_id", "r9999"),
                            "receipt_revision": ("report_revision", 999),
                            "receipt_verdict": ("verdict", "revise"),
                            "receipt_path": ("path", "another-report.json"),
                        }[fault]
                        receipt[key] = value
                        result["text"] = json.dumps(receipt)
                    return result

                self.assertEqual(review_submission(work, reviewer=reviewer)["status"], "pending_review")
                self.assertEqual(self.reviews(work)[0]["status"], "pending_review")
                self.assertEqual(self.reviews(work)[0]["launches"][-1]["status"], "execution_error")
                self.assertFalse(manuscript_is_current(work))
                self.assertFalse((work / "manuscript.md").exists())

    def test_changes_to_current_submission_or_request_make_review_stale(self):
        for changed in ("draft", "outcome", "request"):
            with self.subTest(changed=changed):
                work = self.workspace(changed)
                self.submit(work)

                def reviewer(directory):
                    result = self.verifier_result(directory)
                    if changed == "outcome":
                        submission = self.read(work / "submission.json")
                        submission["outcome"] = "disproved"
                        self.write(work / "submission.json", submission)
                    elif changed == "request":
                        request = self.read(directory / "review_request.json")
                        request["outcome"] = "disproved"
                        self.write(directory / "review_request.json", request)
                    else:
                        target = work / "draft.md" if changed == "draft" else directory / "input" / (
                            "problem.md" if changed == "frozen_problem" else "draft.md")
                        target.write_text("Changed after review started.", encoding="utf-8")
                    return result

                self.assertEqual(review_submission(work, reviewer=reviewer)["status"], "pending_review")
                self.assertEqual(self.reviews(work)[0]["status"], "pending_review")
                self.assertEqual(self.reviews(work)[0]["launches"][-1]["status"], "execution_error")
                self.assertFalse(manuscript_is_current(work))
                self.assertFalse((work / "manuscript.md").exists())

    def test_new_submission_does_not_reuse_old_acceptance(self):
        for change in ("draft", "review_id"):
            with self.subTest(change=change):
                work = self.workspace(change)
                self.submit(work)
                self.assertEqual(review_submission(work, reviewer=self.verifier_result)["status"], "accepted")
                if change == "draft":
                    (work / "draft.md").write_text("A new argument.", encoding="utf-8")
                else:
                    submission = self.read(work / "submission.json")
                    submission["review_id"] = "r9999"
                    self.write(work / "submission.json", submission)
                self.assertFalse(manuscript_is_current(work))


if __name__ == "__main__":
    unittest.main()
