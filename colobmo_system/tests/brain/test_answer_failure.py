"""Real Cell runner boundaries with explicitly synthetic two-stage review data.

No model is called: these tests establish stop/reporting semantics, not the
mathematical detection quality of an external model.
"""
from copy import deepcopy
import importlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch


PROJECT = Path(__file__).resolve().parents[2]
from colombo.cell import worker as worker
worker._cell_imports(PROJECT)
sys.path.insert(0, str(PROJECT / "tests/cell"))
fixtures = importlib.import_module("test_runner_verification")
review_fixtures = importlib.import_module("review_fixtures")
sys.path.pop(0)
from colombo.cell import controller as run, model_calls as processes


ERROR = deepcopy(fixtures.WRONG)
ERROR["summary"] = "Synthetic explicit mathematical error: an odd integer is asserted even."
ERROR["findings"][0]["kind"] = "error"


class AnswerFailureTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.RunnerVerificationTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.cell = self.fixture.workspace("T0001/cell")
        self.task = Path(self.cell).parent
        self.request = self.task / "attempts/A0001/request.json"
        self.request.parent.mkdir(parents=True)
        (self.task / "prepared.json").write_text(json.dumps({"storage_version": 3, "task_id": "T0001",
            "assignment_ref": {"id": "assignment-1"}, "package_ref": {"id": "package-1"}}), encoding="utf-8")
        self.request.write_text(json.dumps({"task_dir": str(self.task), "project_root": str(PROJECT),
            "task_id": "T0001", "attempt_id": "A0001", "assignment_ref": {"id": "assignment-1"},
            "package_ref": {"id": "package-1"}, "resume": False,
            "config": {"stop_on_confirmed_error": True, "run_timeout_seconds": "unlimited"}}), encoding="utf-8")

    def call(self, reports, *, policy=True, resume=False, checker=None):
        request = json.loads(self.request.read_text(encoding="utf-8"))
        request.update(resume=resume)
        request["config"]["stop_on_confirmed_error"] = policy
        self.request.write_text(json.dumps(request), encoding="utf-8")
        count = []
        def prover(prompt, directory, output, **kwargs):
            count.append(1)
            self.fixture.submit(directory, fixtures.BAD_PROOF if len(count) == 1 and not resume else fixtures.PROOF)
            return self.fixture.prover_result(output)
        original_boundary = run._review_to_boundary
        reviewer = self.fixture.reviewer(*reports)
        if checker:
            first = reviewer
            def reviewer(prompt, directory, output, **kwargs):
                request = self.fixture.read(directory / "review_request.json")
                if request.get("stage") == "report_check":
                    return checker(directory)
                return first(prompt, directory, output, **kwargs)
        with patch.object(worker, "_verify_inputs"), patch.object(run, "run_agent", side_effect=prover), \
                patch.object(processes, "run_agent", side_effect=reviewer):
            code = worker.solve(self.request)
        self.assertIs(run._review_to_boundary, original_boundary)
        result = json.loads((self.request.parent / "solve_result.json").read_text(encoding="utf-8"))
        return code, result, len(count)

    def test_confirmed_error_stops_before_second_prover_and_exports_bound_findings(self):
        code, solved, launches = self.call([ERROR])
        self.assertEqual((code, launches), (2, 1))
        failure = solved["failure"]
        self.assertEqual(failure["kind"], "mathematical_error")
        self.assertEqual(failure["findings"][0]["kind"], "error")
        result = worker.export_result(self.request, "incomplete", "confirmed_answer_error", failure=failure)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["failure"], failure)
        self.assertIn("mathematical_error", result["summary"])
        self.assertTrue(any(a["path"].endswith("run_events.jsonl") for a in result["artifacts"]))
        for evidence in failure["evidence"]:
            self.assertTrue(any(a["path"].endswith(evidence["cell_path"])
                                for a in result["artifacts"]))

    def test_pending_ready_submission_error_stops_before_any_prover(self):
        self.fixture.submit(self.cell, fixtures.BAD_PROOF)
        code, solved, launches = self.call([ERROR])
        self.assertEqual((code, launches), (2, 0))
        self.assertEqual(solved["failure"]["kind"], "mathematical_error")

    def test_supervisor_returns_confirmed_error_receipt_and_stops_tree(self):
        self.call([ERROR])
        (self.request.parent / "launch.json").write_text(json.dumps({"nonce": "synthetic-supervisor"}), encoding="utf-8")
        process = Mock(pid=1234)
        process.poll.return_value = 2
        with patch.object(worker, "managed_popen", return_value=process), \
                patch.object(worker, "process_identity", return_value={"synthetic": True}), \
                patch.object(worker, "terminate_tree", return_value=True) as terminate, \
                patch.object(worker, "close_process_job"):
            worker.supervise(self.request)
        terminate.assert_called_once_with(process, timeout=10, poll_seconds=0.2)
        result = json.loads((self.task / "results/A0001/result.json").read_text(encoding="utf-8"))
        self.assertEqual(result["stop_reason"], "confirmed_answer_error")
        self.assertEqual(result["execution_status"], "incomplete")
        self.assertEqual(result["failure"]["kind"], "mathematical_error")
        self.assertTrue((self.request.parent / "receipt.json").is_file())

    def test_existing_pending_review_finishing_on_resume_stops_before_prover(self):
        from colombo.cell.verifier.proof_review import review_submission
        self.fixture.submit(self.cell, fixtures.BAD_PROOF)
        def interrupted_checker(work):
            raise RuntimeError("Synthetic checker interruption")
        decision = review_submission(self.cell,
            reviewer=lambda work: review_fixtures.report_result(work, ERROR), report_checker=interrupted_checker)
        self.assertEqual(decision["status"], "pending_review")
        code, solved, launches = self.call([ERROR], resume=True)
        self.assertEqual((code, launches), (2, 0))
        self.assertEqual(solved["failure"]["kind"], "mathematical_error")

    def test_gap_is_repaired_and_does_not_become_mathematical_error(self):
        code, solved, launches = self.call([fixtures.WRONG, fixtures.CORRECT])
        self.assertEqual((code, launches), (0, 2))
        self.assertIsNone(solved["failure"])

    def test_policy_off_retains_original_repair_behavior(self):
        code, solved, launches = self.call([ERROR, fixtures.CORRECT], policy=False)
        self.assertEqual((code, launches), (0, 2))
        self.assertIsNone(solved["failure"])

    def test_explicit_resume_may_repair_previously_reported_error(self):
        self.call([ERROR])
        code, solved, launches = self.call([fixtures.CORRECT], resume=True)
        self.assertEqual((code, launches), (0, 1))
        self.assertIsNone(solved["failure"])

    def test_unconfirmed_criticism_is_not_mathematical_failure(self):
        code, solved, launches = self.call([ERROR, ERROR, ERROR],
            checker=lambda work: review_fixtures.confirmation_result(work, "needs_correction"))
        self.assertEqual(code, 2)
        self.assertEqual(launches, 1)
        self.assertIsNone(solved["failure"])

    def test_new_submission_cannot_reuse_previous_confirmed_error(self):
        self.call([ERROR])
        (self.cell / "draft.md").write_text("New submission after review", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "current submission"):
            worker.confirmed_answer_failure(self.cell)

    def test_runtime_error_and_timeout_export_structured_failure(self):
        with patch.object(worker, "_verify_inputs", side_effect=RuntimeError("Synthetic runner exception")):
            self.assertEqual(worker.solve(self.request), 1)
        solved = json.loads((self.request.parent / "solve_result.json").read_text(encoding="utf-8"))
        self.assertEqual(solved["failure"]["kind"], "runtime_error")
        self.assertIn("Synthetic runner exception", solved["failure"]["message"])
        result = worker.export_result(self.request, "timeout", "Synthetic wall-clock timeout")
        self.assertEqual(result["failure"]["kind"], "timeout")
        self.assertFalse(result["accepted"])

    def test_runner_caught_prover_exception_still_reaches_result_diagnostics(self):
        with patch.object(worker, "_verify_inputs"), \
                patch.object(run, "run_agent", side_effect=RuntimeError("Synthetic prover process crash")):
            self.assertEqual(worker.solve(self.request), 2)
        solved = json.loads((self.request.parent / "solve_result.json").read_text(encoding="utf-8"))
        self.assertEqual(solved["failure"]["kind"], "runtime_error")
        self.assertIn("Synthetic prover process crash", solved["failure"]["message"])

    def test_accepted_manuscript_is_retained_across_later_runtime_error(self):
        code, solved, _ = self.call([fixtures.CORRECT])
        self.assertEqual(code, 0)
        result = worker.export_result(self.request, "error", "Synthetic post-proof process error")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["execution_status"], "error")
        self.assertEqual(result["failure"]["kind"], "runtime_error")


if __name__ == "__main__":
    unittest.main()
