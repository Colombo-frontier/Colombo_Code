from concurrent.futures import ThreadPoolExecutor
import json
import shutil
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from colombo.brain.research_store import Store, StoreError, RunBusy
from colombo.configuration import load_config
from colombo.shared.file_io import io_path


class StoreTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).resolve().parents[2] / "validation"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.base = Path(self.temp.name)
        self.store = Store.create(self.base / "run", "Complete target", ["Criterion A"], load_config(), [])

    def tearDown(self):
        self.temp.cleanup()

    def test_create_freezes_goal_and_stable_target_ids(self):
        goal = self.store.read_record(self.store.get_meta("goal_ref"))
        self.assertEqual([x["id"] for x in goal["targets"]], ["G0", "G1"])
        self.assertEqual(self.store.get_meta("phase"), "planning")
        self.assertEqual(self.store.read_artifact(self.store.get_meta("goal_ref"))["text"], "Complete target")
        with self.assertRaises(StoreError):
            Store.create(self.store.root, "Changed", [], load_config(), [])

    def test_record_idempotency_and_type_sensitive_input(self):
        ref = self.store.write_record("note", {"text": "Keep"}, request_id="save-once")
        self.assertEqual(ref, self.store.write_record("note", {"text": "Keep"}, request_id="save-once"))
        with self.assertRaises(StoreError):
            self.store.write_record("note", {"text": "Changed"}, request_id="save-once")
        self.store.write_record("note", {"value": True}, request_id="typed")
        with self.assertRaises(StoreError):
            self.store.write_record("note", {"value": 1}, request_id="typed")

    def test_concurrent_idempotent_record_has_one_identity(self):
        def save(_):
            return Store(self.store.root).write_record("note", {"summary": "same"}, "parallel")
        with ThreadPoolExecutor(max_workers=4) as pool:
            refs = list(pool.map(save, range(8)))
        self.assertEqual(len({r["id"] for r in refs}), 1)
        self.assertEqual(len(self.store.retrieve("note")), 1)

    def test_reference_metadata_cannot_select_another_path(self):
        ref = self.store.write_record("note", {"text": "a"})
        with self.assertRaises(StoreError):
            self.store.read_record({**ref, "path": "input/goal.md"})
        for path in ("../outside", self.base / "outside"):
            with self.assertRaises(StoreError):
                self.store.safe_path(path)

    def test_material_snapshot_survives_original_edits(self):
        source = self.base / "source.txt"
        source.write_text("original “content”", encoding="utf-8")
        store = Store.create(self.base / "material_run", "goal", [], load_config(), [source])
        ref = store.get_meta("material_refs")[0]
        source.write_text("changed", encoding="utf-8")
        text = store.read_artifact(ref, offset=9, limit=1)
        self.assertEqual(text["text"], "“")
        self.assertTrue(text["truncated"])
        with self.assertRaises(StoreError):
            store.read_artifact(ref, "input/goal.md")

    def test_binary_read_is_an_explicit_error(self):
        path = self.store.root / "input/blob.bin"
        path.write_bytes(b"\xff\xfe\x00")
        ref = self.store.write_record("result", {"task_id": "T0001", "attempt_id": "A0001", "artifacts": [{'path': 'input/blob.bin', 'size': 3}]})
        with self.assertRaises(StoreError):
            self.store.read_artifact(ref)

    def test_request_ledger_requires_reconciliation(self):
        self.store.save_request("req1", {"task":"A"}, "pending")
        self.store.save_request("req1", {"task":"A"}, "unknown")
        with self.assertRaises(StoreError):
            self.store.save_request("req1", {"task":"A"}, "pending")
        self.store.save_request("req1", {"task":"A"}, "not_executed")
        self.store.save_request("req1", {"task":"A"}, "pending")
        self.store.save_request("req1", {"task":"A"}, "confirmed", {"result":1})
        self.store.save_request("req1", {"task":"A"}, "confirmed", {"result":1})
        with self.assertRaises(StoreError):
            self.store.save_request("req1", {"task":"A"}, "pending")
        with self.assertRaises(StoreError):
            self.store.save_request("req1", {"task":"B"}, "confirmed", {"result":1})
        self.assertEqual(self.store.get_request("req1")["result"], {"result":1})

    def test_task_identity_cannot_be_retargeted(self):
        self.store.save_task({"task_id":"T001", "assignment_ref":"A1", "status":"queued"})
        self.store.save_task({"task_id":"T001", "assignment_ref":"A1", "status":"finished"})
        with self.assertRaises(StoreError):
            self.store.save_task({"task_id":"T001", "assignment_ref":"A2", "status":"queued"})
        self.assertEqual(self.store.get_task("T001")["status"], "finished")

    def test_exclusive_lock_releases_after_exception(self):
        with self.store.exclusive():
            with self.assertRaises(RunBusy):
                with Store(self.store.root).exclusive():
                    self.fail("Concurrent controller acquired lock")
        with self.store.exclusive():
            pass
        with self.assertRaisesRegex(TimeoutError, "model timeout"):
            with self.store.exclusive():
                raise TimeoutError("model timeout")
        with self.store.exclusive():
            pass

    def test_meta_update_and_events_persist(self):
        self.store.set_meta(round_no=2, phase="integrating")
        self.store.event("returned", task_id="T001")
        reopened = Store(self.store.root)
        self.assertEqual(reopened.get_meta("round_no"), 2)
        self.assertEqual(reopened.events()[-1]["payload"], {"task_id":"T001"})

    def test_run_records_and_sqlite_support_paths_above_300_characters(self):
        parent = self.base / ("r" * 130)
        root = parent / ("n" * 130) / "long-run"
        try:
            store = Store.create(root,"Long path target",["criterion"],load_config(),[])
            ref = store.write_record("note",{"summary":"persisted"},"long-write")
            self.assertGreaterEqual(len(str(store.db_path)),300)
            self.assertFalse(str(store.root).startswith("\\\\?\\"))
            self.assertEqual(store.read_record(ref),{"summary":"persisted"})
            self.assertEqual(Store(store.root).get_meta("status"),"ready")
            with store.exclusive():
                pass
        finally:
            if parent.exists():
                shutil.rmtree(io_path(parent))


if __name__ == "__main__":
    unittest.main()
