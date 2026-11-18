"""Recovery receives bounded saved navigation, never a complete memory replay."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import colombo.cell.recovery as recovery
import colombo.cell.settings as settings


ROOT = Path(__file__).resolve().parents[2]


def record(kind, name, revision, payload):
    return {"kind": kind, "id": name, "revision": revision, "payload": payload,
            "created_at": f"2000-01-01T00:00:{revision:02d}Z"}


def reference(row):
    return {key: row[key] for key in ("kind", "id", "revision")}


class RecoveryPacketTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix=".recovery-packet-", dir=ROOT)
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.work = self.root / "task"
        self.work.mkdir()
        self.config = settings.get_settings()
        self.config["handoff"].update(recovery_input_max_bytes=65536,
                                      recovery_source_max_bytes=8388608,
                                      recovery_max_records=12)
        self.handoff = self.work / "handoffs" / "one.json"
        self.write(self.handoff, {"kind": "handoff", "role": "prover", "stage": "prover",
                                  "has_review_authority": False, "summary": "Saved files only"})
        (self.work / "problem.md").write_text("Prove the scoped target.", encoding="utf-8")
        self.destination = self.root / "independent-snapshot"

    @staticmethod
    def write(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def collection(self, kind, rows, folder="memory"):
        self.write(self.work / folder / f"{kind}.json", {"schema_version": 2, "records": rows})

    def build(self, **kwargs):
        result = recovery.build_recovery_packet(self.work, self.handoff, self.destination,
                                                self.config, **kwargs)
        path = Path(result["packet_file"])
        packet = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(result["bytes"], path.stat().st_size)
        self.assertLessEqual(path.stat().st_size, self.config["handoff"]["recovery_input_max_bytes"])
        self.assertEqual(list(self.destination.iterdir()), [path])
        self.assertFalse(packet["has_review_authority"])
        return result, packet

    def test_latest_state_and_attempt_replace_history_without_editing_sources(self):
        states = [record("proof_state", "PS", index, {"route": f"route-{index}"}) for index in range(1, 10)]
        attempts = [record("attempts", "T", index, {"next_steps": [f"step-{index}"]}) for index in range(1, 5)]
        self.collection("proof_state", states)
        self.collection("attempts", attempts)
        before = {p.relative_to(self.work): p.read_bytes() for p in self.work.rglob("*") if p.is_file()}
        result, packet = self.build()
        self.assertEqual([(row["reference"]["kind"], row["reference"]["revision"]) for row in packet["records"]],
                         [("proof_state", 9), ("attempts", 4)])
        self.assertEqual(result["omitted_loaded_versions"], 11)
        self.assertEqual({p.relative_to(self.work): p.read_bytes() for p in self.work.rglob("*") if p.is_file()}, before)
        self.assertIn("Historical", packet["trust_notice"].replace("historical", "Historical"))

    def test_dependencies_keep_the_exact_pinned_revision_not_the_latest(self):
        old = record("arguments", "A", 1, {"proof": "old exact evidence", "status": "candidate"})
        new = record("arguments", "A", 2, {"proof": "different new evidence", "status": "candidate"})
        self.collection("arguments", [old, new])
        self.collection("proof_state", [record("proof_state", "PS", 1, {"dependencies": [reference(old)]})])
        _, packet = self.build()
        included = next(row for row in packet["records"] if row["reference"]["kind"] == "arguments")
        self.assertEqual(included["reference"], reference(old))
        self.assertEqual(included["payload"]["proof"], "old exact evidence")

    def test_active_attempt_products_precede_long_background_reference_lists(self):
        self.config["handoff"]["recovery_max_records"] = 3
        product = record("arguments", "recent-product", 1, {"proof": "next work"})
        old = record("reviews", "old-review", 1, {"summary": "background only"})
        self.collection("arguments", [product])
        self.collection("reviews", [old])
        self.collection("proof_state", [record("proof_state", "PS", 1, {"audit_refs": [reference(old)]})])
        self.collection("attempts", [record("attempts", "latest", 1, {"useful_products": [reference(product)]})])
        _, packet = self.build()
        self.assertEqual([row["reference"]["id"] for row in packet["records"]], ["PS", "latest", "recent-product"])

    def test_large_history_and_unicode_stay_within_actual_utf8_byte_limit(self):
        self.config["handoff"]["recovery_input_max_bytes"] = 4096
        self.collection("proof_state", [record("proof_state", "PS", index,
                            {"next_steps": ["Check the gap" * 10000], "route": f"route-{index}"}) for index in range(1, 5)])
        result, packet = self.build()
        self.assertTrue(result["truncated"])
        self.assertGreater(packet["truncation"]["content_items"], 0)
        self.assertEqual(packet["records"][0]["reference"]["revision"], 4)
        self.assertTrue(packet["records"][0]["truncated"])
        self.assertIn("incomplete", packet["records"][0]["excerpt_format"])
        self.assertEqual(result["omitted_loaded_versions"], 3)

    def test_oversized_source_is_skipped_before_opening(self):
        self.config["handoff"]["recovery_source_max_bytes"] = 4096
        self.collection("proof_state", [record("proof_state", "PS", 1, {"route": "x" * 9000})])
        original = recovery.Path.open

        def checked_open(path, *args, **kwargs):
            self.assertNotEqual(path.name, "proof_state.json", "Oversized source must not be opened")
            return original(path, *args, **kwargs)

        with patch.object(recovery.Path, "open", checked_open):
            _, packet = self.build()
        self.assertTrue(any(row["reason"] == "source_too_large" for row in packet["omissions"]))
        self.assertEqual(packet["records"], [])

    def test_invalid_missing_and_unpinned_references_are_reported(self):
        self.collection("proof_state", [record("proof_state", "PS", 1, {"dependencies": [
            {"kind": "arguments", "id": "missing", "revision": 3},
            {"kind": "arguments", "id": "unversioned"},
            {"kind": ["arguments"], "id": "invalid", "revision": 1},
            {"kind": "../../outside", "id": "invalid", "revision": 1},
        ]})])
        _, packet = self.build()
        self.assertEqual(packet["counts"]["unresolved_references"], 4)
        self.assertTrue(any(row["reason"] == "missing_pinned_revision" for row in packet["omissions"]))
        self.assertTrue(any(row["reason"] == "invalid_or_unpinned_reference" for row in packet["omissions"]))

    def test_context_only_exposes_manifest_granted_exact_records(self):
        allowed = record("claims", "C", 1, {"statement": "granted"})
        not_granted = record("claims", "hidden", 1, {"statement": "not in the grant"})
        self.collection("claims", [allowed, not_granted], folder="context")
        self.write(self.work / "context/manifest.json", {"snapshot_refs": [reference(allowed)]})
        self.collection("proof_state", [record("proof_state", "PS", 1,
                        {"dependencies": [reference(allowed), reference(not_granted)]})])
        _, packet = self.build()
        claims = [row for row in packet["records"] if row["reference"]["kind"] == "claims"]
        self.assertEqual([row["reference"]["id"] for row in claims], ["C"])
        self.assertEqual(claims[0]["source"], "context/claims.json")

    def test_context_example_property_grant_filters_body_before_dependencies(self):
        allowed_claim = record("claims", "allowed-claim", 1, {"statement": "allowed dependency"})
        hidden_claim = record("claims", "hidden-claim", 1, {"statement": "hidden dependency"})
        example = record("examples", "E", 1, {"construction": "One example", "properties": [
            {"id": "granted", "statement": "allowed property", "dependencies": [reference(allowed_claim)]},
            {"id": "outside_scope", "statement": "SECRET OUTSIDE PROPERTY", "dependencies": [reference(hidden_claim)]},
        ]})
        example["property_ids"] = ["granted"]
        grant = {**reference(example), "property_ids": ["granted"]}
        self.collection("examples", [example], folder="context")
        self.collection("claims", [allowed_claim, hidden_claim], folder="context")
        self.write(self.work / "context/manifest.json", {"snapshot_refs": [grant, reference(allowed_claim), reference(hidden_claim)]})
        for selected_ref in (grant, reference(example)):
            with self.subTest(explicit_selection="property_ids" in selected_ref):
                self.collection("proof_state", [record("proof_state", "PS", 1, {"dependencies": [selected_ref]})])
                _, packet = self.build()
                selected = next(row for row in packet["records"] if row["reference"]["kind"] == "examples")
                self.assertEqual(selected["reference"]["property_ids"], ["granted"])
                self.assertEqual([p["id"] for p in selected["payload"]["properties"]], ["granted"])
                self.assertNotIn("SECRET OUTSIDE PROPERTY", json.dumps(packet))
                ids = [row["reference"]["id"] for row in packet["records"]]
                self.assertIn("allowed-claim", ids)
                self.assertNotIn("hidden-claim", ids)

    def test_property_scope_intersects_reference_manifest_and_record_grant(self):
        example = record("examples", "E", 1, {"properties": [
            {"id": name, "statement": name} for name in ("a", "b", "c")
        ]})
        example["property_ids"] = ["b", "c"]
        self.collection("examples", [example], folder="context")
        self.write(self.work / "context/manifest.json", {"snapshot_refs": [
            {**reference(example), "property_ids": ["a", "b"]},
        ]})
        self.collection("proof_state", [record("proof_state", "PS", 1, {"dependencies": [
            {**reference(example), "property_ids": ["a", "b", "c"]},
        ]})])
        _, packet = self.build()
        selected = next(row for row in packet["records"] if row["reference"]["kind"] == "examples")
        self.assertEqual(selected["reference"]["property_ids"], ["b"])
        self.assertEqual([p["id"] for p in selected["payload"]["properties"]], ["b"])
        self.assertTrue(any(row["reason"] == "properties_outside_grant" for row in packet["omissions"]))

    def test_multiple_property_references_merge_without_expanding_scope_at_record_cap(self):
        self.config["handoff"]["recovery_max_records"] = 2
        example = record("examples", "E", 1, {"properties": [
            {"id": name, "statement": name} for name in ("a", "b", "outside")
        ]})
        self.collection("examples", [example], folder="context")
        self.write(self.work / "context/manifest.json", {"snapshot_refs": [
            {**reference(example), "property_ids": ["a", "b"]},
        ]})
        self.collection("proof_state", [record("proof_state", "PS", 1, {"dependencies": [
            {**reference(example), "property_ids": ["a"]},
            {**reference(example), "property_ids": ["b"]},
            {**reference(example), "property_ids": ["outside"]},
        ]})])
        _, packet = self.build()
        self.assertEqual(len(packet["records"]), 2)
        selected = packet["records"][1]
        self.assertEqual(selected["reference"]["property_ids"], ["a", "b"])
        self.assertEqual([p["id"] for p in selected["payload"]["properties"]], ["a", "b"])

    def test_local_example_preserves_explicit_property_selection(self):
        example = record("examples", "E", 1, {"properties": [
            {"id": "one", "statement": "selected"}, {"id": "two", "statement": "not selected"},
        ]})
        self.collection("examples", [example])
        self.collection("proof_state", [record("proof_state", "PS", 1, {"dependencies": [
            {**reference(example), "property_ids": ["one"]},
        ]})])
        _, packet = self.build()
        selected = next(row for row in packet["records"] if row["reference"]["kind"] == "examples")
        self.assertEqual(selected["reference"]["property_ids"], ["one"])
        self.assertEqual([p["id"] for p in selected["payload"]["properties"]], ["one"])

    def test_verifier_packet_keeps_stage_and_frozen_input_with_bounded_excerpts(self):
        self.write(self.handoff, {"kind": "handoff", "role": "verifier", "stage": "report_check"})
        self.write(self.work / "review_request.json", {"stage": "report_check", "review_id": "frozen-1",
                   "problem_file": "problem.md", "draft_file": "draft.md", "evidence_files": ["../../outside.txt"]})
        self.write(self.work / "confirmation_notes.json", {"pending": ["Check issue F1"]})
        (self.work / "input").mkdir()
        (self.work / "input/problem.md").write_text("Frozen problem", encoding="utf-8")
        (self.work / "input/draft.md").write_text("Frozen draft", encoding="utf-8")
        (self.root / "outside.txt").write_text("do not expose this", encoding="utf-8")
        _, packet = self.build()
        docs = {row["source"]: row for row in packet["documents"]}
        self.assertEqual(docs["review_request.json"]["content"]["stage"], "report_check")
        self.assertEqual(docs["input/draft.md"]["content"], "Frozen draft")
        self.assertIn("confirmation_notes.json", docs)
        self.assertNotIn("do not expose this", json.dumps(packet))
        self.assertTrue(any(row["reason"] == "unreadable_source" for row in packet["omissions"]))

    def test_expired_deadline_leaves_an_explicit_factual_packet_without_reading_sources(self):
        with patch.object(recovery.time, "monotonic", return_value=20):
            result, packet = self.build(deadline=10)
        self.assertTrue(result["deadline_reached"])
        self.assertEqual(result["source_files"], 0)
        self.assertEqual(packet["records"], [])
        self.assertEqual(packet["documents"], [])

    def test_record_limit_counts_versions_and_keeps_missing_queue_visible(self):
        self.config["handoff"]["recovery_max_records"] = 2
        arguments = [record("arguments", f"A{n}", 1, {"proof": str(n)}) for n in range(6)]
        self.collection("arguments", arguments)
        self.collection("proof_state", [record("proof_state", "PS", 1,
                         {"dependencies": [reference(row) for row in arguments]})])
        _, packet = self.build()
        self.assertEqual(len(packet["records"]), 2)
        self.assertGreater(packet["counts"]["unexpanded_references"], 0)

    def test_bad_json_is_observable_and_invalid_limits_do_not_silently_expand(self):
        (self.work / "memory").mkdir()
        (self.work / "memory/proof_state.json").write_text("{bad", encoding="utf-8")
        _, packet = self.build()
        self.assertTrue(any(row["source"] == "memory/proof_state.json" and
                            row["reason"] == "unreadable_source" for row in packet["omissions"]))
        for key, value in (("recovery_input_max_bytes", 1000), ("recovery_max_records", 0),
                           ("recovery_source_max_bytes", False)):
            changed = deepcopy(self.config)
            changed["handoff"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                recovery.build_recovery_packet(self.work, self.handoff, self.root / "invalid", changed)


if __name__ == "__main__":
    unittest.main()
