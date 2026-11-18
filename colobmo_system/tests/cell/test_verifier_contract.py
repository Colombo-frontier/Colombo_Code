"""Exercise proof-specific coverage, source uncertainty, and durable review records."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from colombo.cell.verifier.review_validation import validate_receipt
from colombo.cell.verifier.review_validation import validate_report
from colombo.cell.verifier.review_validation import validate_confirmation
from colombo.cell.settings import get_settings
from review_fixtures import confirmation
from review_fixtures import write
from review_fixtures import read


def report() -> dict:
    return {
        "verdict": "pass",
        "summary": "The stated argument establishes the target.",
        "target_alignment": "The conclusion has exactly the assumptions and quantifiers in problem.md.",
        "coverage": "The target, necessary inference and source application are covered by checks 1, 7 and 42.",
        "checks": [{"id": i, "subject": f"Proof obligation {i}", "location": f"draft.md, step {i}", "status": "pass", "reason": f"Checked the local inference {i}."}
                   for i in (1, 7, 42)],
        "findings": [], "sources": [],
    }


def finding(check_id: int, kind: str, name: str = "F1") -> dict:
    return {"id": name, "check_id": check_id, "kind": kind,
            "location": "draft.md, paragraph 2", "explanation": "The cited implication has not been justified.",
            "repair": "Establish the missing implication under the stated assumptions."}


def source(status: str) -> dict:
    return {"citation": "Example paper, Theorem 2", "location": "draft.md, paragraph 2",
            "status": status, "evidence": "The available source text and its limitations are recorded here.",
            "application": "The argument invokes this result for the auxiliary construction.", "check_id": 42}


class ReviewContractTests(unittest.TestCase):
    def test_simple_proof_uses_only_actual_checks_with_arbitrary_positive_ids(self):
        payload = report()
        validate_report(payload)
        self.assertEqual(len(payload["checks"]), 3)
        self.assertEqual(payload["checks"][-1]["id"], 42)
        payload["checks"] = payload["checks"][:1]
        payload["coverage"] = "The sole direct inference proves this elementary target."
        validate_report(payload)
        payload["checks"][0]["status"] = "not_applicable"
        with self.assertRaises(ValueError):
            validate_report(payload)

    def test_coverage_and_identifiers_reject_omission_duplicates_and_boolean_ids(self):
        for mutation in (lambda p: p["checks"].clear(),
                         lambda p: p["checks"][0].update(id=7),
                         lambda p: p["checks"][0].update(id=True),
                         lambda p: p.update(coverage="  "),
                         lambda p: p.pop("coverage"),
                         lambda p: p["checks"][0].update(subject=""),
                         lambda p: p["checks"][0].update(location="")):
            with self.subTest(mutation=mutation):
                payload = report()
                mutation(payload)
                with self.assertRaises(ValueError):
                    validate_report(payload)

    def test_failure_requires_located_finding_and_repair_and_prevents_pass(self):
        payload = report()
        payload["checks"][1].update(status="fail", reason="An inference uses the reverse implication.")
        payload["verdict"] = "revise"
        with self.assertRaisesRegex(ValueError, "needs an error or gap"):
            validate_report(payload)
        payload["findings"] = [finding(7, "error")]
        validate_report(payload)
        payload["verdict"] = "pass"
        with self.assertRaisesRegex(ValueError, "Verdict must be 'revise'"):
            validate_report(payload)
        payload["verdict"] = "revise"
        payload["findings"][0]["repair"] = " "
        with self.assertRaisesRegex(ValueError, "actionable repair"):
            validate_report(payload)

    def test_unavailable_source_is_inconclusive_and_needs_reference_uncertainty(self):
        payload = report()
        payload["sources"] = [source("unavailable")]
        payload["verdict"] = "inconclusive"
        with self.assertRaisesRegex(ValueError, "unavailable source needs"):
            validate_report(payload)
        payload["checks"][2].update(status="unresolved", reason="The original theorem text could not be obtained.")
        payload["findings"] = [finding(42, "uncertain")]
        validate_report(payload)
        payload["verdict"] = "revise"
        with self.assertRaisesRegex(ValueError, "Verdict must be 'inconclusive'"):
            validate_report(payload)

    def test_source_mismatch_is_different_from_inability_to_find_source(self):
        payload = report()
        payload["sources"] = [source("mismatch")]
        payload["checks"][2].update(status="unresolved", reason="Source not found.")
        payload["findings"] = [finding(42, "uncertain")]
        payload["verdict"] = "revise"
        with self.assertRaisesRegex(ValueError, "mismatched source needs"):
            validate_report(payload)
        payload["checks"][2].update(status="fail", reason="The printed theorem requires compactness.")
        payload["findings"] = [finding(42, "error")]
        validate_report(payload)

    def test_confirmed_error_and_reference_uncertainty_can_coexist(self):
        payload = report()
        payload["checks"][2].update(status="fail", reason="One citation differs; another cannot yet be inspected.")
        payload["findings"] = [finding(42, "error"), finding(42, "uncertain", "F2")]
        missing = source("unavailable")
        missing["citation"] = "Second paper, Proposition 1"
        payload["sources"] = [source("mismatch"), missing]
        payload["verdict"] = "revise"
        validate_report(payload)

    def test_a_source_defect_requires_its_own_linked_check_not_an_unrelated_error(self):
        payload = report()
        payload["sources"] = [source("mismatch")]
        payload["checks"][1].update(status="fail", reason="An unrelated argument is invalid.")
        payload["findings"] = [finding(7, "error")]
        payload["verdict"] = "revise"
        with self.assertRaisesRegex(ValueError, "linked check"):
            validate_report(payload)

    def test_empty_explanations_and_unattached_findings_are_rejected(self):
        payload = report()
        payload["checks"][0]["reason"] = "\n\t "
        with self.assertRaises(ValueError):
            validate_report(payload)
        payload = report()
        payload["findings"] = [finding(7, "gap")]
        with self.assertRaisesRegex(ValueError, "requires a fail check"):
            validate_report(payload)
        payload["findings"] = [finding(7, "note"), finding(8, "note")]
        with self.assertRaisesRegex(ValueError, "Duplicate finding"):
            validate_report(payload)


class ReviewRecordTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "review_request.json").write_text(json.dumps({
            "review_id": "r0001", "report_revision": 1,
        }), encoding="utf-8")
        with patch.dict(os.environ, {"CELL_ROLE": "verifier"}):
            self.server = importlib.import_module("colombo.cell.verifier.mcp_server")
        settings = deepcopy(get_settings())
        settings["retrieval"].update(verifier_memory_results=2, max_memory_results=100,
                                     verifier_reverse=False, verifier_search_results=2,
                                     max_search_results=3)
        for item in (patch.object(self.server, "RUN", self.root),
                     patch.object(self.server, "get_settings", return_value=settings)):
            item.start()
            self.addCleanup(item.stop)

    def store_report_records(self, payload):
        for check in payload["checks"]:
            self.server.record_check(check["id"], check["status"], check["reason"], check["subject"], check["location"],
                                     [row for row in payload["findings"] if row["check_id"] == check["id"]])
        for record in payload["sources"]:
            self.server.record_source(**record)

    def test_check_corrections_replace_only_their_own_findings(self):
        self.server.record_check(7, "fail", "A missing step.", "Local implication", "draft.md, step", [finding(7, "gap")])
        self.server.record_check(8, "fail", "A different missing step.", "Local implication", "draft.md, step", [finding(8, "gap", "F2")])
        self.server.record_check(7, "pass", "The omitted step follows by substitution.", "Local implication", "draft.md, step")
        notes = self.server.read_review(limit=30, detail="full")
        self.assertEqual([row["id"] for row in notes["findings"]], ["F2"])
        self.assertEqual([row["id"] for row in notes["checks"]], [8, 7])
        before = (self.root / "review_notes.json").read_bytes()
        with self.assertRaises(ValueError):
            self.server.record_check(8, "fail", "Still missing.", "Local implication", "draft.md, step")
        self.assertEqual((self.root / "review_notes.json").read_bytes(), before)

    def test_source_occurrence_is_updated_without_duplicating_records(self):
        self.server.record_source(**source("unavailable"))
        self.server.record_source(**source("confirmed"))
        notes = self.server.read_review(detail="full")
        self.assertEqual(notes["totals"]["sources"], 1)
        self.assertEqual(notes["sources"][0]["status"], "confirmed")

    def test_report_assembles_all_evidence_and_cannot_ignore_saved_defects(self):
        payload = report()
        payload["checks"][1].update(status="fail", reason="A necessary implication is unproved.")
        payload["findings"] = [finding(7, "gap")]
        payload["sources"] = [source("confirmed")]
        payload["verdict"] = "revise"
        self.store_report_records(payload)
        with self.assertRaisesRegex(ValueError, "Verdict must be 'revise'"):
            self.server.write_report("pass", payload["summary"], payload["target_alignment"], payload["coverage"])
        self.assertFalse((self.root / "review_report.json").exists())
        result = self.server.write_report(payload["verdict"], payload["summary"], payload["target_alignment"], payload["coverage"])
        validate_receipt(result)
        saved_bytes = (self.root / "review_report.json").read_bytes()
        self.assertEqual(json.loads(saved_bytes), payload)
        self.assertEqual(result["report_revision"], 1)
        self.assertEqual(result["review_id"], "r0001")
        self.assertNotIn("checks", result)
        self.assertNotIn("path", result)

    def test_report_rejects_empty_records_and_source_with_missing_check(self):
        payload = report()
        with self.assertRaises(ValueError):
            self.server.write_report("pass", payload["summary"], payload["target_alignment"], payload["coverage"])
        payload["checks"].pop()
        self.store_report_records(payload)
        self.server.record_source(**source("confirmed"))
        before = (self.root / "review_notes.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "source must link"):
            self.server.write_report("pass", payload["summary"], payload["target_alignment"], payload["coverage"])
        self.assertEqual((self.root / "review_notes.json").read_bytes(), before)
        self.assertFalse((self.root / "review_report.json").exists())
        self.server.record_check(42, "pass", "The source statement supports this step.", "Source application", "draft.md, citation")
        self.server.write_report("pass", payload["summary"], payload["target_alignment"], payload["coverage"])
        saved = json.loads((self.root / "review_report.json").read_text(encoding="utf-8"))
        self.assertEqual(len(saved["checks"]), 3)
        self.assertEqual(saved["sources"], [source("confirmed")])

    def test_default_reads_and_write_receipts_do_not_repeat_mathematical_bodies(self):
        reason = "Long mathematical justification. " * 100
        saved = self.server.record_check(7, "fail", reason, "Local implication", "draft.md, step", [finding(7, "gap")])
        self.assertEqual(saved["check_id"], 7)
        self.assertEqual(saved["recorded_checks"], 1)
        self.assertNotIn(reason, json.dumps(saved))
        self.server.record_source(**source("unavailable"))
        summary = self.server.read_review()
        self.assertEqual(summary["check_ids_by_status"]["fail"], [7])
        self.assertEqual(summary["source_status_counts"]["unavailable"], 1)
        self.assertNotIn("missing_check_ids", summary)
        self.assertNotIn("checks", summary)
        body = self.server.read_review(detail="full", check_id=7)
        self.assertEqual(body["checks"][0]["reason"], reason)
        self.assertEqual(body["findings"][0], finding(7, "gap"))

    def test_read_limits_report_truncation_and_reverse_without_silent_clamping(self):
        for check_id in (1, 2, 3):
            self.server.record_check(check_id, "pass", "The local argument is explicit.", "Local implication", "draft.md, step")
        first = self.server.read_review(detail="full")
        self.assertEqual([row["id"] for row in first["checks"]], [1, 2])
        self.assertEqual(first["totals"]["checks"], 3)
        self.assertTrue(first["truncated"])
        self.assertEqual([row["id"] for row in self.server.read_review(detail="full", reverse=True)["checks"]], [3, 2])
        next_page = self.server.read_review(detail="full", offset=first["next_offsets"]["checks"])
        self.assertEqual([row["id"] for row in next_page["checks"]], [3])
        self.assertFalse(next_page["truncated"])
        for invalid in (0, 101, True, 2.5):
            with self.subTest(limit=invalid), self.assertRaises(ValueError):
                self.server.read_review(limit=invalid)
        for kwargs in ({"offset": -1}, {"offset": True}, {"check_id": True}, {"check_id": 0},
                       {"detail": "unknown"}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.server.read_review(**kwargs)

    def test_source_lookup_uses_verifier_defaults_and_rejects_invalid_limits(self):
        with patch.object(self.server, "lookup", return_value={"ok": True, "results": []}) as lookup:
            self.server.lookup_sources(query="lemma")
            lookup.assert_called_once_with(query="lemma", url="", limit=2)
            with self.assertRaises(ValueError):
                self.server.lookup_sources(query="lemma", limit=4)
            self.assertEqual(lookup.call_count, 1)

    def test_concurrent_tool_calls_keep_all_check_records(self):
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(self.server.record_check, i, "pass", f"Checked step {i}.", f"Step {i}", "draft.md")
                       for i in range(1, 31)]
            for task in futures:
                task.result()
        notes = self.server.read_review(limit=30, detail="full")
        self.assertEqual({row["id"] for row in notes["checks"]}, set(range(1, 31)))
        self.assertFalse(notes["truncated"])

    def prepare_report_check(self):
        first = report()
        write(self.root / "first_report.json", first)
        request = read(self.root / "review_request.json")
        request.update(stage="report_check", report_revision=1)
        write(self.root / "review_request.json", request)
        return first

    def test_independent_confirmation_tool_preserves_binding_and_separates_stages(self):
        self.prepare_report_check()
        payload = confirmation(self.root)
        args = {key: value for key, value in payload.items() if key not in {"review_id", "report_revision"}}
        receipt = self.server.write_confirmation(**args)
        self.assertEqual(receipt["verdict"], "confirmed")
        self.assertEqual(read(self.root / "confirmation.json"), payload)
        self.assertEqual(receipt["report_revision"], 1)
        with self.assertRaisesRegex(ValueError, "only available during proof"):
            self.server.write_report("pass", "summary", "alignment", "The recorded checks cover the target.")

    def test_confirmation_exactly_covers_dynamic_ids_and_rejects_coverage_disagreement(self):
        first = self.prepare_report_check()
        request = read(self.root / "review_request.json")
        validate = lambda value: validate_confirmation(value, first, review_id=request["review_id"],
                                                       report_revision=request["report_revision"])
        payload = confirmation(self.root)
        self.assertEqual(payload["covered_check_ids"], [1, 7, 42])
        validate(payload)
        for ids in ([1, 7], [1, 7, 7, 42], [1, 7, 42, 500], []):
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                validate({**payload, "covered_check_ids": ids})
        payload["assessment"]["coverage"].update(status="disputed", reason="The reduction omits a boundary case.")
        with self.assertRaisesRegex(ValueError, "needs_correction"):
            validate(payload)
        payload["verdict"] = "needs_correction"
        validate(payload)

    def test_checker_checkpoint_is_not_a_verdict_and_disagreement_cannot_confirm(self):
        self.prepare_report_check()
        saved = self.server.save_confirmation_notes("Checked parity", ["source still pending"], [{"location": "draft.md", "reason": "Computed cases"}])
        self.assertTrue(saved["saved"])
        self.assertFalse((self.root / "confirmation.json").exists())
        payload = confirmation(self.root)
        payload["new_findings"] = [{"location": "draft.md", "explanation": "New problem", "repair": "Recheck implication"}]
        args = {key: value for key, value in payload.items() if key not in {"review_id", "report_revision"}}
        with self.assertRaisesRegex(ValueError, "needs_correction"):
            self.server.write_confirmation(**args)
        args["verdict"] = "needs_correction"
        self.assertEqual(self.server.write_confirmation(**args)["verdict"], "needs_correction")

    def test_record_finding_requires_precise_target_and_application_stays_distinct(self):
        issue = {**finding(7, "error"), "scope": "record"}
        with self.assertRaisesRegex(ValueError, "exact affected_refs"):
            self.server.record_check(7, "fail", "The local record is wrong", "Local implication", "draft.md, step", [issue])
        issue["affected_refs"] = [{"kind": "arguments", "id": "lemma", "revision": 2}]
        self.server.record_check(7, "fail", "The local record is wrong", "Local implication", "draft.md, step", [issue])
        issue["scope"] = "application"
        self.server.record_check(7, "fail", "The lemma is correct but used outside its domain", "Local implication", "draft.md, step", [issue])
        self.assertEqual(self.server.read_review(detail="full")["findings"][0]["scope"], "application")


if __name__ == "__main__":
    unittest.main()
