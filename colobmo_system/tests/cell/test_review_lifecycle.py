"""Regression coverage for overlapping runners and invalidated publications."""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import colombo.cell.verifier.proof_review as review
import colombo.cell.controller as run
from review_fixtures import confirmation_result


class ReviewLifecycleTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        temporary = tempfile.TemporaryDirectory(prefix=".review-lifecycle-", dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)
        original = self.folder / "original.md"
        original.write_text("Prove n(n+1) is even for every integer n.", encoding="utf-8")
        self.work = self.folder / "run"
        selected, profile = run.load_defaults()
        selected["agents"]["prover_max_rounds"] = 3
        # Trusted fixture supplies the resolved root policy; public CLI budget
        # overrides are covered separately and remain forbidden.
        run.initialize(original, self.work, settings_snapshot=selected, profile=profile)
        (self.work / "draft.md").write_text(
            "One of n and n+1 is even, so their product is even.", encoding="utf-8")
        self.write(self.work / "submission.json", {
            "status": "ready", "outcome": "proved", "draft_file": "draft.md",
        })
        from test_runner_verification import CORRECT
        self.report = deepcopy(CORRECT)

    @staticmethod
    def write(path: Path, value: dict):
        path.write_text(json.dumps(value), encoding="utf-8")

    @staticmethod
    def read(path: Path):
        return json.loads(path.read_text(encoding="utf-8"))

    def reviewer(self, work: Path, report=None):
        report = report or self.report
        self.write(work / "review_report.json", report)
        self.write(work / "review_notes.json", {
            key: report[key] for key in ("checks", "findings", "sources")
        })
        request = self.read(work / "review_request.json")
        receipt = {"review_id": request["review_id"], "report_revision": request["report_revision"],
                   "verdict": report["verdict"]}
        return {"returncode": 0, "text": json.dumps(receipt)}

    def test_busy_gate_does_not_start_a_second_prover(self):
        result = {"session_id": "fake-prover", "log_path": "simulated.events.jsonl"}
        with review._exclusive_review(self.work / ".review.lock"), \
                patch.object(run, "run_agent", return_value=result) as prover, \
                patch.object(review, "_launch_review") as reviewer:
            self.assertEqual(run.solve(self.work), 2)
        prover.assert_not_called()
        reviewer.assert_not_called()
        self.assertFalse(review.manuscript_is_current(self.work))

    def test_required_materials_are_frozen_and_manifest_describes_actual_inputs(self):
        required = self.work / "inputs" / "required.md"
        required.parent.mkdir()
        required.write_text("Required original evidence.", encoding="utf-8")
        (required.parent / "unselected.md").write_text("Not selected.", encoding="utf-8")
        config = self.read(self.work / "run.json")
        config["required_review_files"] = ["inputs/required.md"]
        self.write(self.work / "run.json", config)
        self.assertEqual(review.review_submission(self.work, self.reviewer, confirmation_result)["status"], "accepted")
        folder = self.work / "reviews" / "r0001"
        for workspace in [folder / "workspace", folder / "checks" / "p0001" / "workspace"]:
            request = self.read(workspace / "review_request.json")
            manifest = self.read(workspace / request["input_manifest_file"])
            actual = sorted(p.relative_to(workspace / "input").as_posix()
                            for p in (workspace / "input").rglob("*") if p.is_file())
            self.assertEqual(manifest["files"], actual)
            self.assertIn("inputs/required.md", manifest["required_files"])
            self.assertEqual(manifest["selected_evidence_files"], [])
            self.assertNotIn("inputs/unselected.md", actual)
            self.assertEqual((workspace / "input/inputs/required.md").read_bytes(), required.read_bytes())
        with patch.object(review, "_launch_review") as launch:
            self.assertEqual(review.review_submission(self.work)["status"], "accepted")
        launch.assert_not_called()

    def test_missing_required_material_does_not_launch_or_spend_review_budget(self):
        config = self.read(self.work / "run.json")
        config["required_review_files"] = ["inputs/missing.md"]
        self.write(self.work / "run.json", config)
        with patch.object(review, "_launch_review") as launch:
            result = review.review_submission(self.work)
        self.assertEqual(result["status"], "needs_revision")
        self.assertIn("Invalid review inputs", result["reason"])
        launch.assert_not_called()
        self.assertFalse((self.work / "reviews/index.json").exists())

    def test_manuscript_preserves_reviewed_draft_without_task_control_text(self):
        original = (self.work / "problem.md").read_bytes() + b"\nPRIVATE_TASK_CONTROL_MARKER"
        (self.work / "problem.md").write_bytes(original)
        draft = (self.work / "draft.md").read_bytes()
        self.assertEqual(review.review_submission(self.work, self.reviewer, confirmation_result)["status"], "accepted")
        publication = (self.work / "manuscript.md").read_bytes()
        self.assertTrue(publication.endswith(draft))
        self.assertNotIn(b"PRIVATE_TASK_CONTROL_MARKER", publication)
        self.assertEqual((self.work / "reviews/r0001/input/problem.md").read_bytes(), original)

    def test_required_review_paths_are_optional_and_cannot_escape_task(self):
        self.assertEqual(self.read(self.work / "run.json")["required_review_files"], [])
        original = self.folder / "original.md"
        for invalid in ["../outside.md", "D:/outside.md", "manuscript.md", "cell_record_evidence.json"]:
            with self.subTest(path=invalid), self.assertRaises(ValueError):
                run.initialize(original, self.folder / "invalid", required_review_files=[invalid])
        target = self.folder / "explicit"
        run.initialize(original, target, required_review_files=["inputs/required.md"])
        self.assertEqual(self.read(target / "run.json")["required_review_files"], ["inputs/required.md"])

    def test_missing_submission_removes_publication_but_keeps_review_evidence(self):
        self.assertEqual(review.review_submission(self.work, self.reviewer, confirmation_result)["status"], "accepted")
        submission = self.read(self.work / "submission.json")
        receipt_manuscript = self.work / "reviews" / submission["review_id"] / "manuscript.md"
        (self.work / "submission.json").unlink()
        reviewer = Mock(side_effect=AssertionError("No draft was submitted for review"))
        decision = review.review_submission(self.work, reviewer)
        self.assertEqual(decision["status"], "pending")
        reviewer.assert_not_called()
        self.assertFalse((self.work / "manuscript.md").exists())
        self.assertTrue(receipt_manuscript.exists())
        self.assertFalse(review.manuscript_is_current(self.work))

    def test_reserved_publication_submitted_as_input_is_preserved_before_rejection(self):
        publication = self.work / "manuscript.md"
        alias = self.work / "publication-alias.md"
        contents = b"Submitted mathematical content must survive rejection."
        for status in ("ready", "accepted"):
            for field in ("draft_file", "evidence_files"):
                for aliased in (False, True):
                    with self.subTest(status=status, field=field, aliased=aliased):
                        publication.write_bytes(contents)
                        alias.unlink(missing_ok=True)
                        if aliased:
                            os.link(publication, alias)
                        submitted_name = alias.name if aliased else publication.name
                        submission = {"status": status, "outcome": "proved", "draft_file": "draft.md"}
                        submission[field] = [submitted_name] if field == "evidence_files" else submitted_name
                        self.write(self.work / "submission.json", submission)
                        reviewer = Mock(side_effect=AssertionError("Invalid inputs cannot dispatch a model"))
                        decision = review.review_submission(self.work, reviewer, reviewer)
                        self.assertEqual(decision["status"], "needs_revision")
                        reviewer.assert_not_called()
                        self.assertEqual(publication.read_bytes(), contents)
                        self.assertEqual((self.work / submitted_name).read_bytes(), contents)
                        self.assertFalse((self.work / "reviews" / "index.json").exists())

    def test_changing_problem_does_not_reset_original_target(self):
        rejected = deepcopy(self.report)
        rejected.update(verdict="revise", summary="The draft assumes the required even factor.")
        rejected["checks"][2].update(status="fail", reason="The required step is asserted without an argument.")
        rejected["findings"] = [{
            "id": "missing-parity-step", "check_id": 3, "kind": "gap", "location": "draft.md",
            "explanation": "The parity alternatives have not been established.",
            "repair": "Supply the even and odd cases for n.",
        }]
        first = review.review_submission(self.work, lambda work: self.reviewer(work, rejected), confirmation_result)
        self.assertEqual(first["status"], "needs_revision")
        before = self.read(self.work / "reviews" / "index.json")
        replacement = b"Prove n(n+1) is even for every even integer n."
        (self.work / "problem.md").write_bytes(replacement)
        submission = self.read(self.work / "submission.json")
        submission["status"] = "ready"
        self.write(self.work / "submission.json", submission)
        reviewer = Mock(side_effect=AssertionError("Changed target must not reach a new review"))
        decision = review.review_submission(self.work, reviewer)
        reviewer.assert_not_called()
        self.assertNotEqual(decision["status"], "accepted")
        after = self.read(self.work / "reviews" / "index.json")
        self.assertEqual(len(before["attempts"]), len(after["attempts"]))
        self.assertFalse(review.manuscript_is_current(self.work))
        self.assertFalse((self.work / "manuscript.md").exists())


if __name__ == "__main__":
    unittest.main()
