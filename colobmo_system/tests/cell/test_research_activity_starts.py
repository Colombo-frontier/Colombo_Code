"""Actual native launch evidence, distinct from reserved rounds and reviews."""
import unittest
from unittest.mock import patch

import test_unlimited_runtime as fixture
import colombo.cell.model_calls as processes


class ResearchStartMarkerTests(unittest.TestCase):
    def prepare(self):
        case = fixture.UnlimitedRuntimeTests("test_budget_reports_no_deadline_or_closing_and_serializes_strict_json")
        case.setUp()
        self.addCleanup(case.doCleanups)
        case.completion = 0
        return case

    def markers(self, case):
        return list((case.work / "runtime/research_starts").glob("*.json"))

    def test_only_successfully_launched_researcher_marks_activity(self):
        case = self.prepare()
        case.run_process(role="prover")
        self.assertEqual(len(self.markers(case)), 1)
        case.run_process(role="verifier")
        case.run_process(role="prover", recovery_only=True, timeout=30)
        self.assertEqual(len(self.markers(case)), 1)

    def test_process_creation_failure_does_not_mark_research(self):
        case = self.prepare()
        with patch.object(processes.subprocess, "Popen", side_effect=OSError("startup fixture failure")):
            with self.assertRaises(OSError):
                case.run_process(role="prover")
        self.assertEqual(self.markers(case), [])


if __name__ == "__main__":
    unittest.main()
