"""Confirmed objections change usability, never immutable mathematical history."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.cell.verifier.local_audit import audit
from colombo.cell.record_store import Store
from colombo.cell.record_store import StoreError
from colombo.cell.record_store import AuditRequired
from colombo.cell.subcell_dispatch import Tasks


def ref(record, **extra):
    return {**{k: record[k] for k in ("kind", "id", "revision")}, **extra}


def confirmed_packet(root, records, *, scope="record", kind="gap", review_id="confirmed-test", affected=None):
    references = [ref(r) for r in records]
    report = {"verdict": "revise", "coverage": "Check the supplied inference and its pinned support.",
              "checks": [{"id": 7, "subject": "Validity of the inference", "location": "Argument",
                          "status": "fail", "reason": "The missing case is not justified."}],
              "findings": [{"id": "gap-1", "scope": scope, "kind": kind,
              "explanation": "The asserted inference has a counterexample.",
              "repair": "Replace the inference and account for the missing case.",
              "affected_refs": affected if affected is not None else references}]}
    work = root / "reviews" / review_id
    work.mkdir(parents=True, exist_ok=True)
    report_path = work / "review_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    confirmation = {"verdict": "confirmed", "review_id": review_id, "report_revision": 1,
                    "assessment": {k: {"status": "supported", "reason": "Independently checked."}
                                   for k in ("target_alignment", "coverage", "reasoning", "sources", "record_mapping")},
                    "covered_check_ids": [7],
                    "findings": [{"finding_id": "gap-1", "status": "supported", "reason": "Checked the counterexample."}],
                    "decisive_steps": [{"location": "The inference", "status": "supported", "reason": "Recomputed."}],
                    "new_findings": []}
    confirmation_path = work / "confirmation.json"
    confirmation_path.write_text(json.dumps(confirmation, indent=2) + "\n", encoding="utf-8")
    return dict(review_id=review_id, report_revision=1, report=report, confirmation=confirmation,
                record_refs=references, report_path=report_path, confirmation_path=confirmation_path)


class ConfirmedTrustTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        temporary = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2])
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store = Store(self.root / "memory")

    def prove(self, payload=None, *, record_id=None, expected_revision=None):
        candidate = self.store.archive("arguments", payload or {"proof": "An unjustified inference.", "status": "candidate"},
                                       record_id=record_id, expected_revision=expected_revision)
        review = self.store.write_review({"target": ref(candidate), "verdict": "pass", "properties": []})
        promoted = self.store.archive("arguments", dict(candidate["payload"], status="proved", audit_id=review["id"]),
                                     record_id=candidate["id"], expected_revision=candidate["revision"])
        return candidate, promoted, review

    def example(self):
        candidate = self.store.archive("examples", {"construction": "x=2", "properties": [
            {"id": "positive", "statement": "x>0"}, {"id": "odd", "statement": "x is odd"}]})
        review = self.store.write_review({"target": ref(candidate), "verdict": "pass", "properties": [
            {"id": "positive", "verdict": "pass"}, {"id": "odd", "verdict": "pass"}]})
        payload = copy.deepcopy(candidate["payload"])
        for prop in payload["properties"]:
            prop.update(status="checked", audit_id=review["id"])
        promoted = self.store.archive("examples", payload, record_id=candidate["id"], expected_revision=1)
        return candidate, promoted, review

    def test_confirmed_withdrawal_preserves_payload_and_old_audit_and_is_idempotent(self):
        candidate, proved, review = self.prove()
        before = (self.root / "memory" / "arguments.json").read_bytes()
        packet = confirmed_packet(self.root, [proved])
        first = self.store.apply_confirmed_review(**packet)
        # An independently saved later review cannot break retry identity.
        self.store.write_review({"target": ref(candidate), "verdict": "pass", "properties": []})
        second = self.store.apply_confirmed_review(**packet)
        self.assertEqual(first, second)
        self.assertEqual((self.root / "memory" / "arguments.json").read_bytes(), before)
        record = self.store.get("arguments", proved["id"], proved["revision"])
        self.assertEqual(record["payload"], proved["payload"])
        self.assertEqual(record["payload"], proved["payload"])
        self.assertEqual(record["current_trust"]["state"], "withdrawn")
        self.assertEqual(self.store.get("reviews", review["id"])["payload"]["verdict"], "pass")
        self.assertEqual(self.store.get("arguments", candidate["id"], 1)["current_trust"]["state"], "withdrawn")
        matches = self.store.retrieve(kinds=["arguments"])["records"]
        self.assertEqual(matches[0]["current_trust"]["state"], "withdrawn")

    def test_old_certificate_and_same_evidence_reaudit_cannot_restore_support(self):
        candidate, proved, review = self.prove()
        self.store.apply_confirmed_review(**confirmed_packet(self.root, [proved]))
        with self.assertRaises(AuditRequired):
            self.store.archive("arguments", proved["payload"], record_id=proved["id"], expected_revision=2)
        candidate_again = self.store.archive("arguments", dict(candidate["payload"], challenged_by={"id": "changed-label"}),
                                              record_id=proved["id"], expected_revision=2)
        result = audit(self.root, "arguments", proved["id"], candidate_again["revision"], reviewer=lambda *_: {
            "verdict": "pass", "summary": "Looks good", "findings": [], "properties": []})
        self.assertNotEqual(result["review"]["payload"]["verdict"], "pass")
        self.assertEqual(result["record"]["current_trust"]["state"], "withdrawn")
        renamed = self.store.archive("arguments", candidate["payload"], record_id="renamed-copy")
        self.assertEqual(renamed["current_trust"]["state"], "withdrawn")
        self.assertTrue(self.store.audit_context("arguments", "renamed-copy", 1)["confirmed_objections"])

    def test_repaired_revision_has_original_objection_and_requires_fresh_audit(self):
        _, proved, _ = self.prove()
        self.store.apply_confirmed_review(**confirmed_packet(self.root, [proved]))
        repaired = self.store.archive("arguments", {"status": "candidate", "proof": "New complete case analysis.",
                                       "repair_response": "The missing case is now covered."}, record_id=proved["id"], expected_revision=2)
        seen = []
        def reviewer(_, work):
            seen.append(json.loads((work / "input.json").read_text(encoding="utf-8")))
            return {"verdict": "pass", "summary": "Cases now cover every input.", "findings": [], "properties": []}
        result = audit(self.root, "arguments", proved["id"], repaired["revision"], reviewer=reviewer)
        self.assertTrue(seen[0]["confirmed_objections"])
        self.assertEqual(result["record"]["current_trust"]["state"], "supported")
        self.assertEqual(self.store.get("arguments", proved["id"], 2)["current_trust"]["state"], "withdrawn")

    def test_dependencies_follow_pinned_version_recursively_and_need_new_reference(self):
        _, first, _ = self.prove()
        _, second, _ = self.prove({"proof": "Apply first", "dependencies": [ref(first)]})
        _, third, _ = self.prove({"proof": "Apply second", "dependencies": [ref(second)]})
        claim = self.store.archive("claims", {"statement": "This conclusion remains a mathematical question."})
        self.store.apply_confirmed_review(**confirmed_packet(self.root, [first]))
        self.assertEqual(self.store.get("arguments", second["id"])["current_trust"]["state"], "dependency_blocked")
        self.assertEqual(self.store.get("arguments", third["id"])["current_trust"]["state"], "dependency_blocked")
        self.assertEqual(self.store.get("claims", claim["id"])["payload"], claim["payload"])
        _, repaired, _ = self.prove({"proof": "A corrected proof."}, record_id=first["id"], expected_revision=2)
        self.assertEqual(self.store.get("arguments", second["id"])["current_trust"]["state"], "dependency_blocked")
        _, updated, _ = self.prove({"proof": "Apply repaired first", "dependencies": [ref(repaired)]},
                                   record_id=second["id"], expected_revision=2)
        self.assertEqual(self.store.get("arguments", updated["id"])["current_trust"]["state"], "supported")
        self.assertEqual(self.store.get("arguments", third["id"])["current_trust"]["state"], "dependency_blocked")

    def test_example_property_correction_does_not_withdraw_other_property(self):
        _, example, _ = self.example()
        _, positive, _ = self.prove({"proof": "Use positivity", "dependencies": [ref(example, property_ids=["positive"])]})
        _, odd, _ = self.prove({"proof": "Use oddness", "dependencies": [ref(example, property_ids=["odd"])]})
        packet = confirmed_packet(self.root, [example], affected=[ref(example, property_ids=["odd"])])
        self.store.apply_confirmed_review(**packet)
        properties = self.store.get("examples", example["id"])["current_trust"]["properties"]
        self.assertEqual(properties["positive"]["state"], "supported")
        self.assertEqual(properties["odd"]["state"], "withdrawn")
        self.assertEqual(self.store.get("arguments", positive["id"])["current_trust"]["state"], "supported")
        self.assertEqual(self.store.get("arguments", odd["id"])["current_trust"]["state"], "dependency_blocked")

    def test_application_error_does_not_withdraw_correct_lemma(self):
        _, proved, _ = self.prove()
        self.store.apply_confirmed_review(**confirmed_packet(self.root, [proved], scope="application"))
        self.assertEqual(self.store.get("arguments", proved["id"])["current_trust"]["state"], "supported")

    def test_record_note_and_uncertainty_do_not_withdraw_support(self):
        _, proved, _ = self.prove()
        for kind in ("note", "uncertain"):
            packet = confirmed_packet(self.root, [proved], kind=kind, review_id=f"review-{kind}")
            result = self.store.apply_confirmed_review(**packet)
            self.assertEqual(result["correction_count"], 0)
            self.assertEqual(self.store.get("arguments", proved["id"])["current_trust"]["state"], "supported")

    def test_unconfirmed_mismatched_or_unbound_reports_do_not_change_trust(self):
        _, proved, _ = self.prove()
        packet = confirmed_packet(self.root, [proved])
        packet["confirmation"]["verdict"] = "needs_correction"
        with self.assertRaises(StoreError):
            self.store.apply_confirmed_review(**packet)
        packet = confirmed_packet(self.root, [proved])
        packet["record_refs"] = []
        with self.assertRaises(StoreError):
            self.store.apply_confirmed_review(**packet)
        packet = confirmed_packet(self.root, [proved])
        packet["record_refs"][0]["revision"] = 1
        with self.assertRaises(StoreError):
            self.store.apply_confirmed_review(**packet)
        self.assertEqual(self.store.get("arguments", proved["id"])["current_trust"]["state"], "supported")

    def test_invalid_later_reference_is_atomic_and_properties_cannot_exceed_submission(self):
        _, proved, _ = self.prove()
        before = (self.root / "memory" / "reviews.json").read_bytes()
        packet = confirmed_packet(self.root, [proved], affected=[ref(proved), ref(proved, revision=1)])
        with self.assertRaises(StoreError):
            self.store.apply_confirmed_review(**packet)
        self.assertEqual((self.root / "memory" / "reviews.json").read_bytes(), before)
        _, example, _ = self.example()
        packet = confirmed_packet(self.root, [example], affected=[ref(example, property_ids=["odd"])])
        packet["record_refs"] = [ref(example, property_ids=["positive"])]
        before = (self.root / "memory" / "reviews.json").read_bytes()
        with self.assertRaises(StoreError):
            self.store.apply_confirmed_review(**packet)
        self.assertEqual((self.root / "memory" / "reviews.json").read_bytes(), before)

    def test_all_explicit_dependency_fields_are_validated_and_unusable_cannot_promote(self):
        missing = {"kind": "arguments", "id": "absent", "revision": 1}
        for kind in ("claims", "arguments", "examples", "attempts", "sources", "proof_state"):
            with self.subTest(kind=kind), self.assertRaises(KeyError):
                self.store.archive(kind, {"dependencies": [missing]})
        candidate = self.store.archive("arguments", {"proof": "Unproved premise"})
        with self.assertRaises(AuditRequired):
            self.prove({"proof": "Use premise", "dependencies": [ref(candidate)]})
        _, example, _ = self.example()
        with self.assertRaises(StoreError):
            self.store.archive("claims", {"dependencies": [ref(example, property_ids=["nonexistent"])]})

    def test_delayed_child_result_is_stale_but_saved_work_survives(self):
        _, proved, _ = self.prove()
        tasks = Tasks(self.root)
        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
            launch.return_value.pid = 12345
            task = tasks.spawn_task(ref(proved), "Explore the consequence")
        child = Store(Path(task["workspace"]) / "memory")
        saved = child.archive("claims", {"statement": "A useful independent observation."})
        self.store.apply_confirmed_review(**confirmed_packet(self.root, [proved]))
        collected = tasks.collect_task(task["task_id"], detail="full")
        self.assertEqual(collected["acceptance"], "stale")
        self.assertTrue(collected["stale_context"])
        self.assertEqual(collected["records"][0]["payload"], saved["payload"])
        self.assertEqual(collected["records"][0]["parent_acceptance"], "stale")
        self.assertTrue((Path(task["workspace"]).parent / "cancel.flag").exists())
        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
            launch.return_value.pid = 12346
            repair = tasks.spawn_task(ref(proved), "Repair this explicitly withdrawn argument")
        granted = Store(Path(repair["workspace"]) / "memory").get("arguments", proved["id"], 2)
        self.assertEqual(granted["current_trust"]["state"], "withdrawn")
        self.assertTrue(granted["current_trust"]["confirmed_objections"])


if __name__ == "__main__":
    unittest.main()
