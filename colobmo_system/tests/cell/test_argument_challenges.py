"""A challenge changes certificate usability only after bound, independent review."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from colombo.cell.verifier.challenge import ChallengeError
from colombo.cell.verifier.challenge import challenge_argument
from colombo.cell.verifier.challenge import challenge_from_audit
from colombo.cell.verifier.challenge import resume_argument_challenge
import colombo.cell.verifier.challenge as local_challenge
from colombo.shared.experiment_artifacts import manifest_for
from colombo.cell.record_store import Store
from colombo.cell.settings import get_settings


def ref(record):
    return {key: record[key] for key in ("kind", "id", "revision")}


def first(work, verdict="sustain"):
    request = json.loads((work / "request.json").read_text(encoding="utf-8"))
    findings = [] if verdict == "dismiss" else [{"id": "division-zero", "kind":
        "uncertain" if verdict == "inconclusive" else "error", "location": "Division by x",
        "explanation": "The domain includes x=0 and division by x is undefined there."}]
    return {"challenge_id": request["challenge_id"],
            "verdict": verdict, "summary": "The objection was checked against the stated domain.",
            "findings": findings}


def confirmation(work, verdict="confirmed"):
    request = json.loads((work / "request.json").read_text(encoding="utf-8"))
    report = json.loads((work / "first_report.json").read_text(encoding="utf-8"))
    status = "unsupported" if verdict == "needs_correction" else "uncertain" if verdict == "inconclusive" else "supported"
    return {"challenge_id": request["challenge_id"],
        "report_revision": request["report_revision"], "verdict": verdict,
        "summary": "Checked the original domain and the division step independently.",
        "findings": [{"finding_id": finding["id"], "status": status,
                      "reason": "Recomputed the claimed step at x=0."} for finding in report["findings"]],
        "decisive_steps": [{"location": "Domain and division step", "status": status,
                            "reason": "Evaluated the stated condition and formula at x=0."}],
        "new_findings": []}


class ArgumentChallengeTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for name in tuple(os.environ):
            if name.startswith("CELL_"):
                os.environ.pop(name)
        temporary = tempfile.TemporaryDirectory(prefix=".argument-challenge-", dir=Path(__file__).resolve().parents[2])
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store = Store(self.root / "memory")
        self.settings = get_settings()
        self.write_settings()
        (self.root / "problem.md").write_text("Prove the conclusion for every real x.", encoding="utf-8")
        self.target = self.proved()

    def write_settings(self):
        (self.root / "run.json").write_text(json.dumps({"settings": self.settings}), encoding="utf-8")

    def proved(self, payload=None):
        candidate = self.store.archive("arguments", payload or {"status": "candidate",
            "statement": "The conclusion holds for every real x", "proof": "Divide both sides by x."})
        review = self.store.write_review({"target": ref(candidate), "verdict": "pass", "properties": []})
        return self.store.archive("arguments", dict(candidate["payload"], status="proved", audit_id=review["id"]),
                                  record_id=candidate["id"], expected_revision=candidate["revision"])

    def trust(self, record=None):
        record = record or self.target
        return self.store.get(record["kind"], record["id"], record["revision"])["current_trust"]["state"]

    def state(self, result):
        return json.loads((self.root / result["state_file"]).read_text(encoding="utf-8"))

    @staticmethod
    def timeout(*_):
        raise TimeoutError("bounded review expired")

    def test_confirmed_objection_withdraws_exact_evidence_after_independent_check(self):
        before = (self.root / "memory/arguments.json").read_bytes()
        workspaces = []
        def reviewer(_, work):
            self.assertEqual(self.trust(), "suspended")
            workspaces.append(work)
            return first(work)
        def checker(_, work):
            self.assertEqual(self.trust(), "suspended")
            workspaces.append(work)
            frozen = json.loads((work / "input.json").read_text(encoding="utf-8"))
            self.assertTrue(any(r["payload"].get("proof") == "Divide both sides by x." for r in frozen["records"]))
            return confirmation(work)
        result = challenge_argument(self.root, ref(self.target), "Division fails at zero", reviewer=reviewer, checker=checker)
        self.assertEqual(result["status"], "withdrawn")
        self.assertTrue(result["has_confirmed_error"])
        self.assertEqual(self.trust(), "withdrawn")
        self.assertNotEqual(workspaces[0], workspaces[1])
        self.assertEqual(before, (self.root / "memory/arguments.json").read_bytes())
        self.assertEqual(self.state(result)["primary_launches"], 1)

    def test_first_dismissal_clears_only_this_suspension_without_recertifying(self):
        audit_id = self.target["payload"]["audit_id"]
        result = challenge_argument(self.root, ref(self.target), "Zero appears excluded", reviewer=lambda _, work: first(work, "dismiss"),
                                    checker=lambda *_: self.fail("No adverse opinion exists"))
        self.assertEqual(result["status"], "dismissed")
        self.assertEqual(self.trust(), "supported")
        self.assertEqual(self.store.get("arguments", self.target["id"])["payload"]["audit_id"], audit_id)
        self.assertIsNone(result["confirmation_file"])

    def test_disagreement_revises_opinion_and_requires_new_independent_confirmation(self):
        calls = []
        def reviewer(_, work):
            calls.append("proof")
            if calls.count("proof") == 2:
                self.assertTrue((work / "correction.json").is_file())
                self.assertEqual(self.trust(), "suspended")
                return first(work, "dismiss")
            return first(work)
        def checker(_, work):
            calls.append("check")
            return confirmation(work, "needs_correction" if calls.count("check") == 1 else "confirmed")
        result = challenge_argument(self.root, ref(self.target), "Consider x=0", reviewer=reviewer, checker=checker)
        self.assertEqual(calls, ["proof", "check", "proof", "check"])
        self.assertEqual(result["status"], "dismissed")
        self.assertIsNotNone(result["confirmation_file"])
        self.assertEqual(len(self.state(result)["check_attempts"]), 2)

    def test_timeout_resumes_same_phase_with_consumed_starts(self):
        result = challenge_argument(self.root, ref(self.target), "Consider x=0", reviewer=self.timeout)
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["phase"], "proof")
        self.assertEqual(result["primary_launches"], 1)
        self.assertIsNone(result["report_file"])
        self.assertEqual(self.trust(), "suspended")
        result = resume_argument_challenge(self.root, result["challenge_id"], reviewer=lambda _, w: first(w), checker=lambda _, w: confirmation(w))
        self.assertEqual(result["status"], "withdrawn")
        self.assertEqual(result["primary_launches"], 2)

    def test_uncertain_revision_keeps_correction_bound_to_the_original_disputed_opinion(self):
        self.settings["challenge"]["max_rounds"] = 3
        self.write_settings()
        reports = iter(["sustain", "inconclusive"])
        result = challenge_argument(self.root, ref(self.target), "Consider x=0",
            reviewer=lambda _, w: first(w, next(reports)), checker=lambda _, w: confirmation(w, "needs_correction"))
        self.assertEqual(result["stopping_reason"], "local_review_inconclusive")
        def reviewer(_, work):
            original = (work / "prior_report.json").read_bytes()
            criticism = json.loads((work / "correction.json").read_text(encoding="utf-8"))
            self.assertEqual(criticism["report_revision"], 1)
            self.assertEqual(json.loads(original)["verdict"], "sustain")
            return first(work, "dismiss")
        result = resume_argument_challenge(self.root, result["challenge_id"], reviewer=reviewer, checker=lambda _, w: confirmation(w))
        self.assertEqual(result["status"], "dismissed")

    def test_checker_timeout_never_repeats_primary_or_forgets_checkpoint(self):
        seen = []
        def timeout(_, work):
            seen.append(work)
            (work / "progress.md").write_text("The zero case still needs checking.", encoding="utf-8")
            raise TimeoutError()
        result = challenge_argument(self.root, ref(self.target), "Consider x=0", reviewer=lambda _, w: first(w), checker=timeout)
        self.assertEqual(result["phase"], "check")
        def resumed(_, work):
            self.assertEqual(work, seen[0])
            self.assertTrue((work / "progress.md").is_file())
            return confirmation(work)
        result = resume_argument_challenge(self.root, result["challenge_id"], reviewer=lambda *_: self.fail("Already completed"), checker=resumed)
        self.assertEqual(result["status"], "withdrawn")
        self.assertEqual(list(result["check_attempts"].values()), [2])

    def test_retry_exact_request_is_idempotent_and_changed_request_rejected(self):
        result = challenge_argument(self.root, ref(self.target), "Consider x=0", request_id="my-objection",
                                    reviewer=lambda _, w: first(w), checker=lambda _, w: confirmation(w))
        repeated = challenge_argument(self.root, ref(self.target), "Consider x=0", request_id="my-objection",
                                      reviewer=lambda *_: self.fail("Must not relaunch"))
        self.assertEqual(result, repeated)
        with self.assertRaises(ChallengeError):
            challenge_argument(self.root, ref(self.target), "Different concern", request_id="my-objection")

    def test_pending_challenges_cannot_release_each_other(self):
        pending = challenge_argument(self.root, ref(self.target), "Concern A", request_id="A", reviewer=self.timeout)
        dismissed = challenge_argument(self.root, ref(self.target), "Concern B", request_id="B", reviewer=lambda _, w: first(w, "dismiss"))
        self.assertEqual(dismissed["status"], "dismissed")
        self.assertEqual(self.trust(), "suspended")
        self.assertEqual(self.state(pending)["status"], "pending")

    def test_exhaustion_persists_but_raising_start_cap_can_resume(self):
        self.settings["challenge"]["max_rounds"] = 1
        self.settings["challenge"]["timeout_seconds"] = 120
        self.write_settings()
        result = challenge_argument(self.root, ref(self.target), "Concern", reviewer=self.timeout)
        frozen_timeout = self.state(result)["settings"]["challenge"]["timeout_seconds"]
        result = resume_argument_challenge(self.root, result["challenge_id"], reviewer=lambda *_: self.fail("Exhausted"))
        self.assertEqual(result["stopping_reason"], "review_budget_exhausted")
        self.settings["challenge"].update(max_rounds=2, timeout_seconds=frozen_timeout + 100)
        self.write_settings()
        result = resume_argument_challenge(self.root, result["challenge_id"], reviewer=lambda _, w: first(w, "dismiss"))
        self.assertEqual(result["status"], "dismissed")
        self.assertEqual(self.state(result)["settings"]["challenge"]["timeout_seconds"], frozen_timeout)

    def test_no_process_started_during_parent_closing_window(self):
        with patch.dict(os.environ, {"CELL_PROCESS_ID": "a" * 32}), patch("colombo.cell.verifier.challenge.budget_status",
                return_value={"work_remaining_seconds": 0, "hard_deadline": time.time() + 30}):
            result = challenge_argument(self.root, ref(self.target), "Concern", reviewer=lambda *_: self.fail("No work time"))
        self.assertEqual(result["primary_launches"], 0)
        self.assertEqual(result["stopping_reason"], "parent_work_budget")
        self.assertEqual(self.trust(), "suspended")

    def test_real_launcher_receives_remaining_work_budget_and_frozen_configuration(self):
        captured = []
        def run(prompt, work, output, **options):
            captured.append(options)
            self.assertLessEqual(options["timeout"], 3)
            self.assertEqual(options["role"], "audit")
            self.assertFalse(options["search"])
            self.assertIn("_absolute_deadline", options)
            return {"returncode": 0, "text": json.dumps(first(work, "dismiss"))}
        with patch.dict(os.environ, {"CELL_PROCESS_ID": "a" * 32}), patch("colombo.cell.verifier.challenge.budget_status",
                return_value={"work_remaining_seconds": 3, "hard_deadline": time.time() + 30}), \
                patch("colombo.cell.verifier.challenge.run_agent", side_effect=run):
            result = challenge_argument(self.root, ref(self.target), "Concern")
        self.assertEqual(result["status"], "dismissed")
        self.assertEqual(len(captured), 1)

    def test_invalid_confirmation_and_model_errors_do_not_withdraw(self):
        def invalid(_, work):
            result = confirmation(work)
            result["report_revision"] = 999
            return result
        result = challenge_argument(self.root, ref(self.target), "Concern", reviewer=lambda _, w: first(w), checker=invalid)
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["stopping_reason"], "review_execution_error")
        self.assertEqual(self.trust(), "suspended")
        self.assertIsNone(result["report_file"])
        def contradictory(_, work):
            value = confirmation(work)
            value["decisive_steps"][0]["status"] = "unsupported"
            return value
        result = resume_argument_challenge(self.root, result["challenge_id"], checker=contradictory)
        self.assertEqual(result["status"], "pending")
        self.assertEqual(self.trust(), "suspended")

    def test_failed_reaudit_reuses_saved_first_result(self):
        review = self.store.write_review({"target": ref(self.target), "verdict": "fail", "summary": "Division can be undefined",
                                         "findings": ["The zero case is omitted"], "properties": []})
        result = challenge_from_audit(self.root, self.target, review,
                    reviewer=lambda *_: self.fail("Do not repeat completed audit"), checker=lambda _, w: confirmation(w))
        self.assertEqual(result["status"], "withdrawn")
        self.assertEqual(result["primary_launches"], 1)
        self.assertEqual(sum(result["check_attempts"].values()), 1)

    def test_interrupted_published_adverse_report_is_recovered_before_any_new_primary(self):
        save = local_challenge._save
        def interrupted(path, value):
            save(path, value)
            if path.parent.name == "reports" and value.get("verdict") == "sustain":
                raise KeyboardInterrupt("Killed after result publication")
        with patch.object(local_challenge, "_save", side_effect=interrupted), self.assertRaises(KeyboardInterrupt):
            challenge_argument(self.root, ref(self.target), "Concern", reviewer=lambda _, w: first(w))
        identifier = next(p.name for p in (self.root / "challenges").iterdir() if p.name.startswith("ch-"))
        result = resume_argument_challenge(self.root, identifier, reviewer=lambda *_: self.fail("Published first result must be recovered"),
                                           checker=lambda _, w: confirmation(w))
        self.assertEqual(result["status"], "withdrawn")
        self.assertEqual(result["primary_launches"], 1)

    def test_interrupted_last_checker_result_can_finish_without_another_budget(self):
        self.settings["challenge"]["max_check_attempts"] = 1
        self.write_settings()
        save = local_challenge._save
        def interrupted(path, value):
            save(path, value)
            if path.parent.parent.name == "confirmations":
                raise KeyboardInterrupt("Killed after independent result publication")
        with patch.object(local_challenge, "_save", side_effect=interrupted), self.assertRaises(KeyboardInterrupt):
            challenge_argument(self.root, ref(self.target), "Concern", reviewer=lambda _, w: first(w), checker=lambda _, w: confirmation(w))
        identifier = next(p.name for p in (self.root / "challenges").iterdir() if p.name.startswith("ch-"))
        result = resume_argument_challenge(self.root, identifier, reviewer=lambda *_: self.fail("Already done"),
                                           checker=lambda *_: self.fail("Budget exhausted but result saved"))
        self.assertEqual(result["status"], "withdrawn")
        self.assertEqual(list(result["check_attempts"].values()), [1])

    def test_terminal_store_resolution_recovers_report_references_after_interruption(self):
        save = local_challenge._save
        def interrupted(path, value):
            if path.name == "state.json" and value.get("status") == "withdrawn":
                raise KeyboardInterrupt("Killed after Store commit")
            save(path, value)
        with patch.object(local_challenge, "_save", side_effect=interrupted), self.assertRaises(KeyboardInterrupt):
            challenge_argument(self.root, ref(self.target), "Concern", reviewer=lambda _, w: first(w), checker=lambda _, w: confirmation(w))
        identifier = next(p.name for p in (self.root / "challenges").iterdir() if p.name.startswith("ch-"))
        result = resume_argument_challenge(self.root, identifier, reviewer=lambda *_: self.fail("Already resolved"), checker=lambda *_: self.fail("Already resolved"))
        self.assertEqual(result["status"], "withdrawn")
        self.assertTrue((self.root / result["report_file"]).is_file())
        self.assertTrue((self.root / result["confirmation_file"]).is_file())

    def test_seed_report_published_atomically_before_suspension_registration(self):
        review = self.store.write_review({"target": ref(self.target), "verdict": "fail", "summary": "Division can be undefined",
                                         "findings": ["The zero case is omitted"], "properties": []})
        begin = Store.begin_argument_challenge
        def interrupted(store, *args):
            begin(store, *args)
            raise RuntimeError("Lost caller after registration")
        with patch.object(Store, "begin_argument_challenge", interrupted), self.assertRaises(RuntimeError):
            challenge_from_audit(self.root, self.target, review)
        result = challenge_from_audit(self.root, self.target, review,
                    reviewer=lambda *_: self.fail("Seed is already a completed first report"), checker=lambda _, w: confirmation(w))
        self.assertEqual(result["status"], "withdrawn")
        self.assertEqual(result["primary_launches"], 1)

    def test_uncertain_reaudit_suspends_without_asserting_falsehood(self):
        review = self.store.write_review({"target": ref(self.target), "verdict": "uncertain", "summary": "Need the zero case",
                                         "findings": ["Cannot judge zero case"], "properties": []})
        result = challenge_from_audit(self.root, self.target, review,
                    reviewer=lambda *_: self.fail("No immediate new round"), checker=lambda *_: self.fail("No definite error"))
        self.assertEqual(result["status"], "pending")
        self.assertFalse(result["has_confirmed_error"])
        self.assertEqual(self.trust(), "suspended")

    def test_exact_dependencies_and_selected_experiment_files_are_frozen(self):
        claim = self.store.archive("claims", {"statement": "Check x=0 exactly"})
        files = {"experiments/zero/code.py": b"assert 0 == 0\n", "experiments/zero/output.txt": b"zero\n"}
        for name, data in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        experiment = self.store.write_experiment_result("exp-zero", {"question": "Compute at zero", "target_ref": ref(claim),
            "parameters": {}, "code_file": "experiments/zero/code.py",
            "input_files": [], "execution": {"status": "completed", "backend": "fixture", "model": "fake",
                "started_at": 1, "deadline_at": 2, "artifact_limits": {k: self.settings["experiment"][k]
                for k in ("artifact_max_bytes", "max_total_artifact_bytes", "max_files")}}, "artifacts": manifest_for(files)})
        dependency = self.proved({"proof": "An independent parity argument."})
        target = self.proved({"proof": "Apply the parity lemma then divide by x.", "dependencies": [ref(dependency)]})
        result = challenge_argument(self.root, ref(target), "Check zero", [ref(experiment)], reviewer=self.timeout)
        # Later live files may disappear; this review resumes against its saved copy.
        (self.root / "experiments/zero/output.txt").unlink()
        def reviewer(_, work):
            frozen = json.loads((work / "input.json").read_text(encoding="utf-8"))
            self.assertTrue(any(ref(r) == ref(dependency) for r in frozen["records"]))
            self.assertEqual((work / "input/experiments/zero/output.txt").read_bytes(), b"zero\n")
            return first(work, "dismiss")
        result = resume_argument_challenge(self.root, result["challenge_id"], reviewer=reviewer)
        self.assertEqual(result["status"], "dismissed")


if __name__ == "__main__":
    unittest.main()
