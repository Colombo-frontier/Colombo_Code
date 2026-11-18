"""Versioned identities and actual mathematical content replace digests."""
import json
import tempfile
import unittest
from pathlib import Path

from colombo.cell.record_store import Store
from colombo.cell.record_store import StoreError
from colombo.cell.record_store import evidence_body
from colombo.cell.record_store import json_equal
from colombo.cell.record_store import support_body


class StorageV2Tests(unittest.TestCase):
    def test_json_equality_preserves_types_and_ignores_object_key_order(self):
        self.assertTrue(json_equal({"a": 1, "b": 2}, {"b": 2, "a": 1}))
        self.assertFalse(json_equal(True, 1))
        self.assertFalse(json_equal(1, 1.0))

    def test_record_has_versioned_identity_without_content_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory) / "memory")
            record = store.archive("claims", {"proposition": "P"})
            self.assertEqual(set(record), {"kind", "id", "revision", "created_at", "payload", "current_trust"})
            self.assertEqual(json.loads((store.memory_dir / ".storage.json").read_text()), {"storage_version": 2})
            self.assertEqual(json.loads((store.memory_dir / "claims.json").read_text())["schema_version"], 2)

    def test_old_unversioned_memory_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = Path(directory) / "memory"
            memory.mkdir()
            (memory / "claims.json").write_text(json.dumps({"schema_version": 1, "records": []}))
            with self.assertRaisesRegex(StoreError, "start a new run"):
                Store(memory)

    def test_request_replay_uses_actual_type_sensitive_input(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory) / "memory")
            first = store.archive("sources", {"value": True}, request_id="one")
            self.assertEqual(store.archive("sources", {"value": True}, request_id="one"), first)
            with self.assertRaisesRegex(StoreError, "different input"):
                store.archive("sources", {"value": 1}, request_id="one")
            saved = json.loads((store.memory_dir / ".requests.json").read_text())["one"]
            self.assertEqual(set(saved), {"input", "result"})
            self.assertIs(saved["input"]["payload"]["value"], True)

    def test_promotion_and_withdrawal_have_distinct_content_rules(self):
        base = {"proof": "A implies B", "assumptions": ["A"], "status": "candidate"}
        promoted = dict(base, status="proved", audit_id="audit-one", title="New title")
        self.assertTrue(json_equal(evidence_body(base), evidence_body(promoted)))
        imported = dict(promoted, origin={"task_id": "child"}, challenged_by="objection")
        self.assertFalse(json_equal(evidence_body(base), evidence_body(imported)))
        self.assertTrue(json_equal(support_body(base), support_body(imported)))
        repaired = dict(imported, proof="A and C imply B", assumptions=["A", "C"])
        self.assertFalse(json_equal(support_body(base), support_body(repaired)))


if __name__ == "__main__":
    unittest.main()
