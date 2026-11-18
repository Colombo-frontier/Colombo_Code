"""Integrity and historical-version tests for exact Cell evidence reads."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from colombo.brain.cell_evidence import RECORD_KINDS, RECORD_REF_SCHEMA, read_record_evidence, resolve_record
from colombo.shared.file_io import atomic_write, json_bytes
from colombo.configuration import load_config
from colombo.brain.research_store import Store


def reference(record):
    return {field: record[field] for field in ("kind", "id", "revision")}


def cell_record(revision=1):
    dependency = {"kind": "claims", "id": "claim-not-exported", "revision": 3}
    payload = {"title": "Parity Proof", "proof": "Take any integer n and consider its parity." * 20,
               "status": "candidate" if revision == 1 else "proved", "dependencies": [dependency],
               "conclusions": [{"target": dependency, "relation": "supports"}], "remaining_gaps": []}
    if revision != 1:
        payload["audit_id"] = "review-exact-revision"
    return {"kind": "arguments", "id": "argument-parity", "revision": revision,
            "created_at": "2000-01-01T00:00:00+00:00", "payload": payload,
            "current_trust": {"state": "unreviewed" if revision == 1 else "supported", "blockers": []}}


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).resolve().parents[2] / "validation/tmp"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.store = Store.create(Path(self.temp.name) / "run", "Verify parity", [], load_config())
        self.old = cell_record(1)
        self.new = cell_record(2)
        self.sequence = 0
        self.result, self.path = self.snapshot([self.old, self.new])

    def tearDown(self):
        self.temp.cleanup()

    def snapshot(self, records, *, artifact_kind="research_memory_snapshot", body=None, record_kind="result"):
        self.sequence += 1
        relative = f"tasks/T0001/results/A{self.sequence:04d}/artifacts/memory_snapshot.json"
        data = json_bytes({"schema_version": 2, "records": records} if body is None else body)
        atomic_write(self.store.root / relative, data)
        artifact = {"path": relative, "size": len(data), "kind": artifact_kind}
        result = self.store.write_record(record_kind, {"task_id": "T0001", "accepted": True,
            "attempt_id": f"A{self.sequence:04d}", "artifacts": [artifact]})
        return result, relative

    def resolve(self, ref=None, source=None):
        return resolve_record(self.store, *(source or (self.result, self.path)),
                              reference(self.old) if ref is None else ref)

    def test_exact_historical_revision_returns_full_envelope_and_snapshot_trust(self):
        self.assertEqual(self.resolve(), self.old)
        self.assertEqual(self.resolve(reference(self.new)), self.new)
        self.assertNotEqual(self.old["revision"], self.new["revision"])

    def test_retains_dependencies_and_conclusions_without_reading_missing_context(self):
        record = self.resolve()
        self.assertEqual(record["payload"]["dependencies"], self.old["payload"]["dependencies"])
        self.assertEqual(record["payload"]["conclusions"], self.old["payload"]["conclusions"])
        with self.assertRaisesRegex(ValueError, "absent"):
            self.resolve(record["payload"]["dependencies"][0])

    def test_unknown_revision_id_or_kind_never_falls_back(self):
        for field, value in (("revision", 3), ("id", "argument-other"), ("kind", "claims")):
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.resolve({**reference(self.old), field: value})




    def test_rejects_duplicate_identity_including_unselected_record(self):
        for records in ([self.old, self.old], [self.old, self.new, self.new]):
            with self.subTest(records=len(records)), self.assertRaisesRegex(ValueError, "Duplicate"):
                self.resolve(source=self.snapshot(records))

    def test_requires_result_and_explicit_snapshot_artifact_kind(self):
        for kwargs in ({"record_kind": "material"}, {"artifact_kind": "manuscript"}, {"artifact_kind": None}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.resolve(source=self.snapshot([self.old], **kwargs))

    def test_rejects_path_not_authorized_by_result(self):
        other = self.snapshot([self.old])
        with self.assertRaisesRegex(ValueError, "authorized"):
            self.resolve(source=(self.result, other[1]))
        with self.assertRaises(ValueError):
            self.resolve(source=(self.result, "../memory_snapshot.json"))

    def test_ref_must_be_exactly_three_strict_fields(self):
        good = reference(self.old)
        invalid = [None, {}, {**good, "locator": "free text"}, {**good, "kind": "argument"},
                   {**good, "kind": []}, {**good, "id": " "}, {**good, "id": 4},
                   {**good, "revision": True}, {**good, "revision": 0}, {**good, "revision": 1.0}]
        for ref in invalid:
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                resolve_record(self.store, self.result, self.path, ref)

    def test_rejects_malformed_snapshot_and_record_envelopes(self):
        for body in ([], load_config(), {"schema_version": True, "records": []}, {"schema_version": 1, "records": []},
                     {"schema_version": 2, "records": {}}, {"schema_version": 2, "records": [None]},
                     {"schema_version": 2, "records": [{}]}):
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.resolve(source=self.snapshot([], body=body))
        record = {**self.old, "payload": []}
        with self.assertRaisesRegex(ValueError, "payload"):
            self.resolve(source=self.snapshot([record]))

    def test_pagination_returns_only_selected_record_with_pinned_metadata(self):
        result = read_record_evidence(self.store, self.result, self.path,
                                      reference(self.old), limit=100000)
        self.assertEqual(set(result), {"text", "path", "record_ref", "offset", "total_chars", "truncated"})
        self.assertEqual(json.loads(result["text"]), self.old)
        self.assertEqual(result["record_ref"], reference(self.old))
        self.assertEqual(result["path"], self.path)
        self.assertFalse(result["truncated"])
        parts = []
        for offset in range(0, result["total_chars"], 37):
            page = read_record_evidence(self.store, self.result, self.path,
                                        reference(self.old), offset=offset, limit=37)
            self.assertEqual(page["offset"], offset)
            self.assertEqual(page["truncated"], offset + 37 < result["total_chars"])
            parts.append(page["text"])
        self.assertEqual("".join(parts), result["text"])
        empty = read_record_evidence(self.store, self.result, self.path,
                                     reference(self.old), offset=result["total_chars"])
        self.assertEqual(empty["text"], "")
        self.assertFalse(empty["truncated"])

    def test_rejects_invalid_pagination(self):
        for offset, limit in ((-1, 10), (True, 10), (0, 0), (0, 100001), (0, True), (0, 1.5)):
            with self.subTest(offset=offset, limit=limit), self.assertRaisesRegex(ValueError, "read range"):
                read_record_evidence(self.store, self.result, self.path,
                                     reference(self.old), offset=offset, limit=limit)

    def test_every_readable_kind_is_supported_without_inventing_trust(self):
        for kind in RECORD_KINDS:
            record = {**self.old, "kind": kind}
            record.pop("current_trust")
            with self.subTest(kind=kind):
                self.assertEqual(self.resolve(reference(record), self.snapshot([record])), record)
        self.assertEqual(set(RECORD_REF_SCHEMA["properties"]["kind"]["enum"]), RECORD_KINDS)
        self.assertFalse(RECORD_REF_SCHEMA["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
