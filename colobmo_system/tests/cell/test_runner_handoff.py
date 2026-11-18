"""Keep unfinished verification ahead of prover work and persist launch budgets."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import colombo.cell.verifier.proof_review as review
import colombo.cell.controller as run
import colombo.cell.settings as settings
from review_fixtures import confirmation_result


class RunnerHandoffTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        for name in tuple(os.environ):
            if name.startswith("CELL_"):
                os.environ.pop(name)
        temporary = tempfile.TemporaryDirectory(prefix=".runner-handoff-", dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)
        source = self.folder / "question.md"
        source.write_text("Prove that 2 is even.", encoding="utf-8")
        self.work = self.folder / "run"
        self.policy = settings.load_policy()
        self.policy["cell"]["settings"]["agents"]["prover_max_rounds"] = 2
        # solve/resume adopts the root policy, so configure this fixture at that
        # boundary rather than supplying now-forbidden per-call count overrides.
        policy_patch = patch.object(settings, "load_policy", return_value=self.policy)
        policy_patch.start()
        self.addCleanup(policy_patch.stop)
        run.initialize(source, self.work)

    def state(self):
        return json.loads((self.work / "runtime/prover_state.json").read_text(encoding="utf-8"))

    def test_cooperative_prover_handoff_is_given_to_next_prover(self):
        handoff_path = self.work / "handoffs/previous.json"
        observed = []

        def prover(prompt, directory, output, **kwargs):
            observed.append(kwargs["role"])
            if len(observed) == 1:
                return {"execution_status": "handoff", "handoff_path": str(handoff_path)}
            self.assertEqual(self.state()["handoff_path"], str(handoff_path))
            self.assertIn("runtime/prover_state.json", prompt)
            return {"text": "Saved a further partial argument."}

        with patch.object(run, "manuscript_is_current", return_value=False), \
                patch.object(run, "has_pending_review", return_value=False), \
                patch.object(run, "review_submission", return_value={"status": "pending"}), \
                patch.object(run, "run_agent", side_effect=prover):
            self.assertEqual(run.solve(self.work), 2)
        self.assertEqual(observed, ["prover", "prover"])
        self.assertEqual(self.state()["launches"], 2)

    def test_pending_verifier_resumes_even_when_prover_budget_exhausted(self):
        run._save_prover_state(self.work, {"launches": 2})
        decisions = [{"status": "pending_review", "reason": "Verifier handoff saved."},
                     {"status": "accepted"}]
        with patch.object(run, "manuscript_is_current", side_effect=[False, True]), \
                patch.object(run, "has_pending_review", return_value=True), \
                patch.object(run, "review_submission", side_effect=decisions) as reviewer, \
                patch.object(run, "run_agent") as prover:
            self.assertEqual(run.solve(self.work), 0)
        self.assertEqual(reviewer.call_count, 2)
        prover.assert_not_called()
        self.assertEqual(self.state()["launches"], 2)

    def test_prover_only_resumes_after_confirmed_revision_decision(self):
        order = []
        run._save_prover_state(self.work, {"launches": 1})

        def verifier(root):
            order.append("verifier")
            if len(order) == 1:
                return {"status": "pending_review"}
            if len(order) == 2:
                return {"status": "needs_revision", "reason": "Confirmed report and record sync complete."}
            return {"status": "pending"}

        def prover(*args, **kwargs):
            order.append("prover")
            return {"text": "Saved updated attempt."}

        with patch.object(run, "manuscript_is_current", return_value=False), \
                patch.object(run, "has_pending_review", return_value=True), \
                patch.object(run, "review_submission", side_effect=verifier), \
                patch.object(run, "run_agent", side_effect=prover):
            self.assertEqual(run.solve(self.work), 2)
        self.assertEqual(order, ["verifier", "verifier", "prover", "verifier"])

    def test_repeated_resume_does_not_reset_prover_count(self):
        with patch.object(run, "manuscript_is_current", return_value=False), \
                patch.object(run, "has_pending_review", return_value=False), \
                patch.object(run, "review_submission", return_value={"status": "pending"}), \
                patch.object(run, "run_agent", return_value={"execution_status": "handoff"}) as prover:
            for _ in range(3):
                self.assertEqual(run.solve(self.work), 2)
        self.assertEqual(prover.call_count, 2)
        self.assertEqual(self.state()["launches"], 2)

    def test_legacy_event_history_also_preserves_used_launches(self):
        run.event(self.work, "prover_started", turn=1)
        run.event(self.work, "prover_started", turn=2)
        with patch.object(run, "manuscript_is_current", return_value=False), \
                patch.object(run, "has_pending_review", return_value=False), \
                patch.object(run, "run_agent") as prover:
            self.assertEqual(run.solve(self.work), 2)
        prover.assert_not_called()
        self.assertEqual(run._prover_state(self.work)["launches"], 2)

    def test_overlapping_solve_cannot_launch_second_prover_or_spend_budget(self):
        launches = []
        nested_results = []
        self.policy["cell"]["settings"]["agents"]["prover_max_rounds"] = 1

        def prover(*args, **kwargs):
            launches.append("prover")
            if len(launches) == 1:
                nested_results.append(run.solve(self.work))
            return {"text": "Partial work saved."}

        with patch.object(run, "manuscript_is_current", return_value=False), \
                patch.object(run, "has_pending_review", return_value=False), \
                patch.object(run, "review_submission", return_value={"status": "pending"}), \
                patch.object(run, "run_agent", side_effect=prover):
            self.assertEqual(run.solve(self.work), 2)
        self.assertEqual(nested_results, [2])
        self.assertEqual(launches, ["prover"])
        self.assertEqual(self.state()["launches"], 1)
        events = [json.loads(line) for line in (self.work / "run_events.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(sum(item["action"] == "runner_busy" for item in events), 1)

    def test_record_sync_failure_stays_at_verifier_on_repeated_resume(self):
        (self.work / "draft.md").write_text("2 = 2 times 1, with 1 an integer.", encoding="utf-8")
        (self.work / "submission.json").write_text(json.dumps({
            "status": "ready", "outcome": "proved", "draft_file": "draft.md"}), encoding="utf-8")
        report = {"verdict": "pass", "summary": "The definition of even applies.",
                  "target_alignment": "The proof treats exactly the integer 2.",
                  "coverage": "The single witness and integer check covers the evenness definition.",
                  "checks": [{"id": 1, "subject": "Integer witness for evenness", "location": "draft.md",
                              "status": "pass", "reason": "2=2*1 and 1 is an integer."}],
                  "findings": [], "sources": []}

        def reviewer(work):
            (work / "review_report.json").write_text(json.dumps(report), encoding="utf-8")
            (work / "review_notes.json").write_text(json.dumps({
                key: report[key] for key in ("checks", "findings", "sources")}), encoding="utf-8")
            request = json.loads((work / "review_request.json").read_text(encoding="utf-8"))
            receipt = {"review_id": request["review_id"], "report_revision": request["report_revision"],
                       "verdict": "pass"}
            return {"text": json.dumps(receipt)}

        actual_review = review.review_submission
        with patch.object(run, "review_submission", side_effect=lambda root: actual_review(root, reviewer, confirmation_result)), \
                patch.object(review, "_synchronize", side_effect=OSError("Simulated record store failure")) as sync, \
                patch.object(run, "run_agent") as prover:
            self.assertEqual(run.solve(self.work), 2)
            self.assertEqual(run.solve(self.work), 2)
        prover.assert_not_called()
        self.assertEqual(sync.call_count, 2)
        index = json.loads((self.work / "reviews/index.json").read_text(encoding="utf-8"))
        self.assertEqual(index["attempts"][0]["phase"], "sync")
        self.assertEqual(index["primary_launches"], 1)
        self.assertFalse(review.manuscript_is_current(self.work))


if __name__ == "__main__":
    unittest.main()
