"""Publication uses adopted state and is resumable without another model call."""
import unittest
from unittest.mock import patch

from colombo.brain.final_report import finalize, export_final
from colombo.brain.research_store import StoreError
from controller_fixtures import OracleTestFixture
from test_oracle_workflow import Backend
from test_integration_structure import DraftBackend


class DeterministicFinalizationTests(OracleTestFixture, unittest.TestCase):

    def test_completed_report_uses_adopted_proof_and_resume_only_reexports(self):
        script = Backend()
        self.assertEqual(self.controller(script).run()["status"], "completed")
        before = (list(script.calls), self.adapter.launches, self.store.get_meta("conclusion_ref"))
        report = (self.root / "output/final.md").read_text(encoding="utf-8")
        proof_ref = self.store.get_meta("proof_ref")
        proof = self.store.read_record(proof_ref)["proof_draft"]
        self.assertIn(proof["body"], report)
        self.assertIn(proof_ref["id"], report)
        self.assertNotIn("conclude", script.calls)
        (self.root / "output/final.md").unlink()
        self.assertEqual(self.controller(script).run()["status"], "completed")
        self.assertEqual(before, (script.calls, self.adapter.launches, self.store.get_meta("conclusion_ref")))
        self.assertEqual((self.root / "output/final.md").read_text(encoding="utf-8"), report)
        self.assertEqual(self.store.reference_count("conclusion"), 1)

    def test_export_failure_after_commit_recovers_original_conclusion(self):
        script = Backend()
        with patch("colombo.brain.final_report.atomic_write", side_effect=OSError("Simulated report export interruption")):
            with self.assertRaises(OSError):
                self.controller(script).run()
        self.assertEqual(self.store.get_meta("phase"), "done")
        before = (list(script.calls), self.store.get_meta("conclusion_ref"))
        self.assertEqual(self.controller(script).run()["status"], "completed")
        self.assertEqual(before, (script.calls, self.store.get_meta("conclusion_ref")))
        self.assertEqual(self.store.reference_count("conclusion"), 1)

    def test_partial_progress_produces_partial_report_and_preserves_remaining(self):
        script = DraftBackend(partial=True)
        self.assertEqual(self.controller(script).run()["status"], "partial")
        conclusion = self.store.read_record(self.store.get_meta("conclusion_ref"))
        self.assertTrue(conclusion["remaining"])
        self.assertNotIn("conclude", script.calls)

    def test_partial_export_failure_restores_partial_conclusion_without_new_calls(self):
        script = DraftBackend(partial=True)
        with patch("colombo.brain.final_report.atomic_write", side_effect=OSError("Interrupted report export")):
            with self.assertRaises(OSError):
                self.controller(script).run()
        conclusion_ref = self.store.get_meta("conclusion_ref")
        conclusion = self.store.read_record(conclusion_ref)
        basis = self.store.get_meta("finalization")
        calls = list(script.calls)
        self.assertEqual(conclusion["status"], "partial")
        self.assertEqual(self.store.get_meta("status"), "needs_attention")
        self.assertEqual(self.controller(script).run()["status"], "partial")
        self.assertEqual(script.calls, calls)
        self.assertEqual(self.store.get_meta("conclusion_ref"), conclusion_ref)
        self.assertEqual(self.store.read_record(conclusion_ref), conclusion)
        self.assertEqual(self.store.get_meta("stop_reason"), basis["reason"])
        self.assertIn("Status: partial", (self.root / "output/final.md").read_text(encoding="utf-8"))

    def test_unresolved_external_call_cannot_be_finalized(self):
        self.store.set_meta(pending_call={"call_id": "C00077", "role": "brain", "stage": "plan"})
        with self.assertRaisesRegex(StoreError, "unresolved model"):
            finalize(self.store)
        self.assertEqual(self.store.reference_count("conclusion"), 0)

    def test_unregistered_result_cannot_hide_behind_completed_progress(self):
        script = Backend()
        self.controller(script).run()
        events = self.store.get_meta("result_events")
        self.store.set_meta(phase="concluding", result_events=events[:-1])
        with self.assertRaisesRegex(StoreError, "durable results"):
            finalize(self.store)
        self.assertEqual(self.store.reference_count("conclusion"), 1)


if __name__ == "__main__":
    unittest.main()
