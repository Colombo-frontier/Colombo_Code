"""State-machine boundaries: independent confirmation, continuation, and trust sync."""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock
from unittest.mock import patch

from colombo.cell.record_store import Store
import colombo.cell.verifier.proof_review as review
from colombo.cell.verifier.review_validation import validate_confirmation
import colombo.cell.controller as run
import colombo.cell.settings as settings
from review_fixtures import read
from review_fixtures import write
from review_fixtures import report_result
from review_fixtures import confirmation
from review_fixtures import confirmation_result
from test_runner_verification import CORRECT
from test_runner_verification import WRONG
from test_runner_verification import PROBLEM
from test_runner_verification import PROOF


class TwoStageReviewTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                del os.environ[key]
        temp = tempfile.TemporaryDirectory(prefix="cell-two-stage-")
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name).resolve()
        problem = self.folder / "source.md"
        problem.write_text(PROBLEM, encoding="utf-8")
        self.root = self.folder / "run"
        selected, profile = run.load_defaults()
        selected["agents"]["prover_max_rounds"] = 4
        # Trusted root-policy fixture, not a public budget override.
        run.initialize(problem, self.root, settings_snapshot=selected, profile=profile)
        (self.root / "draft.md").write_text(PROOF, encoding="utf-8")
        write(self.root / "submission.json", {"status": "ready", "outcome": "proved", "draft_file": "draft.md"})

    def settings(self, **agents):
        value = read(self.root / "run.json")
        value["settings"]["agents"].update(agents)
        value.update(settings.run_fields(value["settings"]))
        write(self.root / "run.json", value)

    def state(self):
        return read(self.root / "reviews" / "index.json")

    def test_actual_launches_bind_identity_guidance_to_each_report_version(self):
        """The real launch boundary delivers the guidance through a correction cycle.

        Simulated receipts exercise both independent stages; this does not claim
        that an untested model will always obey the instruction.
        """
        import colombo.cell.model_calls as processes

        reports = iter((WRONG, CORRECT))
        observed = []

        def process(prompt, work, output, **kwargs):
            request = read(work / "review_request.json")
            identity = (request["stage"], request["review_id"], request["report_revision"])
            observed.append((identity, work))
            self.assertEqual(kwargs["role"], "verifier")
            self.assertIn(f"review_id={request['review_id']}, report_revision={request['report_revision']}", prompt)
            self.assertIn("necessary direct body comparisons", prompt)
            self.assertIn("do not compute or attach content hashes", prompt)
            self.assertIn("not hash functions that are themselves part of the mathematical problem", prompt)
            self.assertEqual((work / "AGENTS.md").read_bytes(), (review.RESOURCES / "AGENTS.md").read_bytes())
            skill = "check-report" if request["stage"] == "report_check" else "review-proof"
            relative = Path(".agents/skills") / skill / "SKILL.md"
            self.assertEqual((work / relative).read_bytes(), (review.RESOURCES / relative).read_bytes())
            self.assertEqual((work / "input/draft.md").read_text(encoding="utf-8"), PROOF)
            if request["stage"] == "report_check":
                expected = WRONG if request["report_revision"] == 1 else CORRECT
                self.assertEqual(read(work / "first_report.json"), expected)
                return confirmation_result(work, "needs_correction" if request["report_revision"] == 1 else "confirmed")
            return report_result(work, next(reports))

        with patch.object(processes, "run_agent", side_effect=process):
            result = review.review_submission(self.root)
        self.assertEqual(result["status"], "accepted")
        self.assertEqual([item[0] for item in observed], [
            ("proof", "r0001", 1), ("report_check", "r0001", 1),
            ("proof", "r0001", 2), ("report_check", "r0001", 2)])
        self.assertNotEqual(observed[1][1], observed[3][1])
        self.assertEqual(self.state()["primary_launches"], 2)
        self.assertEqual(self.state()["attempts"][0]["check_attempts"], {"1": 1, "2": 1})

    def certified_argument(self, proof, dependencies=None):
        store = Store(self.root / "memory")
        payload = {"proof": proof, "status": "candidate"}
        if dependencies:
            payload["dependencies"] = dependencies
        candidate = store.archive("arguments", payload)
        ref = lambda row: {key: row[key] for key in ("kind", "id", "revision")}
        certificate = store.write_review({"target": ref(candidate), "verdict": "pass", "properties": []})
        promoted = store.archive("arguments", {**payload, "status": "proved", "audit_id": certificate["id"]},
                                 record_id=candidate["id"], expected_revision=candidate["revision"])
        return ref(promoted)

    def suspend_argument(self, reference):
        from colombo.cell.verifier.challenge import challenge_argument
        def timeout(*_):
            raise TimeoutError("Simulated unfinished local review")
        result = challenge_argument(self.root, reference, "Check the missing case in this inference", reviewer=timeout)
        self.assertEqual(result["status"], "pending")
        return result

    def test_suspended_direct_or_transitive_evidence_cannot_publish_passing_global_report(self):
        for indirect in (False, True):
            with self.subTest(indirect=indirect):
                # Each subcase is a new submitted graph; all reports deliberately pass.
                target = self.certified_argument(f"Base parity argument {indirect}")
                submitted = self.certified_argument("Conclusion uses the base lemma", [target]) if indirect else target
                self.suspend_argument(target)
                write(self.root / "submission.json", {"status": "ready", "outcome": "proved", "draft_file": "draft.md",
                      "record_refs": [{**submitted, "position": "draft.md, main inference"}]})
                snapshot = review._capture(self.root, read(self.root / "submission.json"))
                with self.assertRaisesRegex(ValueError, "suspended|dependency-blocked"):
                    review._check_current_support(self.root, snapshot)
                if not indirect:
                    self.settings(verifier_max_rounds=1)
                    result = review.review_submission(self.root, lambda work: report_result(work, CORRECT), confirmation_result)
                    self.assertEqual(result["status"], "review_incomplete")
                    self.assertFalse((self.root / "manuscript.md").exists())
                    self.assertFalse(review.manuscript_is_current(self.root))

    def test_new_suspension_invalidates_an_existing_accepted_receipt(self):
        target = self.certified_argument("Parity supports the final product")
        write(self.root / "submission.json", {"status": "ready", "outcome": "proved", "draft_file": "draft.md",
              "record_refs": [{**target, "position": "draft.md, final inference"}]})
        result = review.review_submission(self.root, lambda work: report_result(work, CORRECT), confirmation_result)
        self.assertEqual(result["status"], "accepted")
        self.assertTrue(review.manuscript_is_current(self.root))
        self.suspend_argument(target)
        self.assertFalse(review.manuscript_is_current(self.root))
        no_launch = Mock(side_effect=AssertionError("An old receipt cannot bypass support checks"))
        self.assertEqual(review.review_submission(self.root, no_launch, no_launch)["status"], "needs_revision")
        no_launch.assert_not_called()
        self.assertFalse((self.root / "manuscript.md").exists())

    def test_false_criticism_is_corrected_internally_before_publication(self):
        reports = iter((WRONG, CORRECT))
        primary_workspaces, check_workspaces = [], []
        def primary(work):
            primary_workspaces.append(work)
            if len(primary_workspaces) == 2:
                self.assertTrue((work / "internal" / "report_check.json").exists())
                self.assertFalse((work.parent / "report.json").exists())
                self.assertNotEqual(read(self.root / "submission.json")["status"], "needs_revision")
            return report_result(work, next(reports))
        def checker(work):
            check_workspaces.append(work)
            self.assertFalse((work / "review_notes.json").exists())
            self.assertEqual((work / "input" / "draft.md").read_text(), PROOF)
            return confirmation_result(work, "needs_correction" if len(check_workspaces) == 1 else "confirmed")
        result = review.review_submission(self.root, primary, checker)
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(primary_workspaces[0], primary_workspaces[1])
        self.assertNotEqual(check_workspaces[0], check_workspaces[1])
        self.assertEqual(self.state()["primary_launches"], 2)
        self.assertEqual(len(self.state()["attempts"]), 1)

    def test_new_checker_defect_must_be_written_and_confirmed_in_first_report(self):
        sequence = iter((CORRECT, WRONG))
        checks = 0
        def checker(work):
            nonlocal checks
            checks += 1
            if checks == 1:
                def new_problem(value):
                    value["new_findings"] = [{"location": "draft.md", "explanation": "A required case is missing.", "repair": "Check both cases."}]
                return confirmation_result(work, "needs_correction", new_problem)
            return confirmation_result(work)
        result = review.review_submission(self.root, lambda work: report_result(work, next(sequence)), checker)
        self.assertEqual(result["status"], "needs_revision")
        final = self.root / "reviews" / result["review_id"]
        self.assertEqual(read(final / "report.json"), WRONG)
        self.assertEqual(checks, 2)
        self.assertTrue(read(final / "confirmation.json")["verdict"] == "confirmed")

    def test_checker_timeout_resumes_checker_notes_and_retains_primary_budget(self):
        workspaces = []
        primary = Mock(side_effect=lambda work: report_result(work, CORRECT))
        def interrupted(work):
            workspaces.append(work)
            write(work / "confirmation_notes.json", {"summary": "Cases checked", "pending": ["source"], "evidence": []})
            # A complete-looking saved artifact must not be auto-promoted.
            confirmation_result(work)
            raise TimeoutError("simulated checker timeout")
        self.assertEqual(review.review_submission(self.root, primary, interrupted)["status"], "pending_review")
        self.assertEqual(self.state()["attempts"][0]["phase"], "report_check")
        self.assertFalse((self.root / "manuscript.md").exists())
        def resumed(work):
            self.assertEqual(work, workspaces[0])
            self.assertTrue((work / "confirmation_notes.json").exists())
            self.assertFalse((work / "confirmation.json").exists())
            return confirmation_result(work)
        self.assertEqual(review.review_submission(self.root, primary, resumed)["status"], "accepted")
        primary.assert_called_once()
        self.assertEqual(self.state()["primary_launches"], 1)
        self.assertEqual(list(self.state()["attempts"][0]["check_attempts"].values()), [2])

    def test_cooperative_handoff_and_primary_timeout_never_become_prover_feedback(self):
        for stopping in ("handoff", "timeout"):
            with self.subTest(stopping=stopping):
                if stopping == "timeout":
                    # Continue the same pending primary stage after its handoff.
                    self.assertTrue(review.has_pending_review(self.root))
                def interrupted(work):
                    write(work / "review_notes.json", {"checks": [CORRECT["checks"][0]], "findings": [], "sources": []})
                    if stopping == "timeout":
                        raise TimeoutError("primary timeout")
                    return {"execution_status": "handoff", "handoff_path": "handoffs/saved.json"}
                checker = Mock(side_effect=AssertionError("Incomplete primary cannot reach checker"))
                self.assertEqual(review.review_submission(self.root, interrupted, checker)["status"], "pending_review")
                checker.assert_not_called()
                self.assertEqual(self.state()["attempts"][0]["phase"], "proof")
                self.assertFalse((self.root / "manuscript.md").exists())
        def resume(work):
            self.assertEqual(len(read(work / "review_notes.json")["checks"]), 1)
            return report_result(work, CORRECT)
        self.assertEqual(review.review_submission(self.root, resume, confirmation_result)["status"], "accepted")
        self.assertEqual(self.state()["primary_launches"], 3)

    def test_checker_budget_is_durable_per_exact_report(self):
        self.settings(report_check_max_attempts=1)
        failure = Mock(side_effect=TimeoutError("checker timeout"))
        primary = Mock(side_effect=lambda work: report_result(work, CORRECT))
        self.assertEqual(review.review_submission(self.root, primary, failure)["status"], "review_incomplete")
        self.assertEqual(review.review_submission(self.root, primary, failure)["status"], "review_incomplete")
        primary.assert_called_once()
        failure.assert_called_once()
        self.assertTrue(review.has_pending_review(self.root))

    def test_corrected_report_gets_new_checker_budget(self):
        self.settings(report_check_max_attempts=1)
        reports = iter((WRONG, CORRECT))
        checks = iter(("needs_correction", "confirmed"))
        result = review.review_submission(self.root, lambda work: report_result(work, next(reports)),
                                         lambda work: confirmation_result(work, next(checks)))
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(sorted(self.state()["attempts"][0]["check_attempts"].values()), [1, 1])

    def test_disagreement_exhaustion_does_not_release_criticism(self):
        self.settings(verifier_max_rounds=1)
        result = review.review_submission(self.root, lambda work: report_result(work, WRONG),
                                         lambda work: confirmation_result(work, "needs_correction"))
        self.assertEqual(result["status"], "review_incomplete")
        item = self.state()["attempts"][0]
        self.assertEqual(item["phase"], "proof")
        self.assertFalse((self.root / "reviews" / item["id"] / "report.json").exists())
        self.assertFalse((self.root / "memory" / "reviews.json").exists())

    def test_confirmation_binds_full_report_and_rejects_disguised_disagreement(self):
        faults = [lambda p: p.update(report_revision=999),
                  lambda p: p.update(covered_check_ids=[1, 2]),
                  lambda p: p["assessment"]["sources"].update(status="unresolved"),
                  lambda p: p.update(decisive_steps=[]),
                  lambda p: p.update(findings=[])]
        def checker(work):
            for mutate in faults:
                with self.assertRaises(ValueError):
                    payload = confirmation(work, mutate=mutate)
                    validate_confirmation(payload, WRONG,
                        review_id=read(work / "review_request.json")["review_id"],
                        report_revision=read(work / "review_request.json")["report_revision"])
            return confirmation_result(work)
        self.assertEqual(review.review_submission(self.root, lambda work: report_result(work, WRONG), checker)["status"], "needs_revision")

    def test_changed_frozen_report_stops_without_unbounded_redispatch(self):
        def pause(work):
            return {"execution_status": "handoff", "handoff_path": "saved.json"}
        self.assertEqual(review.review_submission(self.root, lambda work: report_result(work, CORRECT), pause)["status"], "pending_review")
        item = self.state()["attempts"][0]
        path = self.root / "reviews" / item["id"] / "reports" / "p0001.json"
        path.write_text("{}", encoding="utf-8")
        checker = Mock(side_effect=AssertionError("Corrupted evidence must not dispatch"))
        self.assertEqual(review.review_submission(self.root, None, checker)["status"], "review_incomplete")
        checker.assert_not_called()

    def test_sync_failure_keeps_feedback_internal_and_retry_is_idempotent(self):
        original = Store.apply_confirmed_review
        calls = []
        def commit_then_fail(store, **kwargs):
            calls.append(kwargs["review_id"])
            original(store, **kwargs)
            raise OSError("simulated crash after store commit")
        primary = Mock(side_effect=lambda work: report_result(work, WRONG))
        checker = Mock(side_effect=confirmation_result)
        with patch.object(Store, "apply_confirmed_review", new=commit_then_fail):
            self.assertEqual(review.review_submission(self.root, primary, checker)["status"], "review_incomplete")
        self.assertEqual(self.state()["attempts"][0]["phase"], "sync")
        self.assertEqual(review.review_submission(self.root, primary, checker)["status"], "needs_revision")
        primary.assert_called_once()
        checker.assert_called_once()
        self.assertEqual(len(read(self.root / "memory" / "reviews.json")["records"]), 1)

    def test_changed_support_returns_to_primary_before_any_sync_or_feedback(self):
        reports = iter((CORRECT, WRONG))
        primary_calls = []
        def primary(work):
            primary_calls.append(work)
            if len(primary_calls) == 2:
                notice = read(work / "internal" / "report_check.json")
                self.assertIn("withdrawn", notice["reason"])
                self.assertFalse((self.root / "memory" / "reviews.json").exists())
                self.assertNotEqual(read(self.root / "submission.json")["status"], "needs_revision")
            return report_result(work, next(reports))
        with patch.object(review, "_check_current_support", side_effect=review._SupportChanged("withdrawn support")):
            result = review.review_submission(self.root, primary, confirmation_result)
        self.assertEqual(result["status"], "needs_revision")
        self.assertEqual(len(primary_calls), 2)
        self.assertEqual(len(read(self.root / "memory" / "reviews.json")["records"]), 1)

    def test_exact_record_mapping_is_frozen_and_confirmed_error_withdraws_support(self):
        store = Store(self.root / "memory")
        candidate = store.archive("arguments", {"statement": "n is even", "proof": "Assume it", "status": "candidate"}, "bad-lemma")
        audit = store.write_review({"target": {key: candidate[key] for key in ("kind", "id", "revision")},
            "verdict": "pass", "reason": "simulated mistaken small audit"})
        promoted = store.archive("arguments", {**candidate["payload"], "status": "proved", "audit_id": audit["id"]},
                                 "bad-lemma", expected_revision=1)
        ref = {key: promoted[key] for key in ("kind", "id", "revision")}
        ref["position"] = "draft.md, first sentence"
        submission = read(self.root / "submission.json")
        submission["record_refs"] = [ref]
        write(self.root / "submission.json", submission)
        wrong = deepcopy(WRONG)
        wrong["findings"][0].update(scope="record", affected_refs=[ref])
        def primary(work):
            frozen = read(work / "input" / "cell_record_evidence.json")[0]
            self.assertEqual(frozen["revision"], promoted["revision"])
            self.assertEqual(frozen["supporting_audits"][0]["review"]["id"], audit["id"])
            return report_result(work, wrong)
        result = review.review_submission(self.root, primary, confirmation_result)
        self.assertEqual(result["status"], "needs_revision")
        self.assertEqual(store.get("arguments", "bad-lemma")["current_trust"]["state"], "withdrawn")
        self.assertEqual(store.get("arguments", "bad-lemma")["payload"]["status"], "proved")


if __name__ == "__main__":
    unittest.main()
