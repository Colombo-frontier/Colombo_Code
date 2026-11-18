"""A completing supervisor must not be mistaken for a lost Cell execution."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from colombo.brain.cell_dispatch import CellAdapter
from colombo.shared.file_io import read_json, write_json


class ReceiptRaceTests(unittest.TestCase):
    def setUp(self):
        parent = PROJECT / "validation" / "tmp"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="receipt-race-", dir=parent)
        self.task = Path(self.temp.name) / "T0001"
        self.folder = self.task / "attempts" / "A0001"
        self.folder.mkdir(parents=True)
        self.scope = {"task_id": "T0001", "attempt_id": "A0001",
                      "assignment_ref": {"id": "assignment-1", "revision": 1},
                      "package_ref": {"id": "package-1", "revision": 1}}
        self.adapter = CellAdapter(PROJECT, {"cell": {"run_timeout_seconds": 30}})
        write_json(self.task / "prepared.json", {"storage_version": 3, **self.scope})
        write_json(self.folder / "request.json", {
            "task_dir": str(self.task), "project_root": str(PROJECT),
            **self.scope, "resume": False, "config": self.adapter.config})
        self.identity = {"pid": 123456, "platform": "windows", "start_token": "test"}
        self.launch = {"nonce": "test", "created_at": time.time() - 60,
                       "identity": self.identity, "state": "started"}
        write_json(self.folder / "launch.json", self.launch)
        write_json(self.folder / "worker.json", {"nonce": "test", "identity": self.identity})
        self.result = {**self.scope, "execution_status": "incomplete", "accepted": False,
                       "review_status": "not_submitted", "artifacts": []}

    def tearDown(self):
        self.temp.cleanup()

    def publish(self, *, receipt_changes=None, result_changes=None):
        result = {**self.result, **(result_changes or {})}
        write_json(self.task / "results/A0001/result.json", result)
        write_json(self.folder / "receipt.json", {
            **self.scope, "result_path": "results/A0001/result.json", **(receipt_changes or {})})
        return result

    def test_receipt_published_during_process_check_is_collected_once_without_relaunch(self):
        for matches in (False, None):
            with self.subTest(matches=matches):
                receipt = self.folder / "receipt.json"
                if receipt.exists():
                    receipt.unlink()

                def exited(_identity):
                    self.publish()
                    return matches

                with patch("colombo.brain.cell_dispatch.process_matches", side_effect=exited) as check, \
                     patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
                    self.assertEqual(self.adapter.run(self.task, "A0001"), self.result)
                    self.assertEqual(self.adapter.run(self.task, "A0001"), self.result)
                    self.assertEqual(check.call_count, 1)
                    launch.assert_not_called()

    def test_absent_or_unknown_worker_without_receipt_stays_unknown_without_relaunch(self):
        for matches in (False, None):
            with self.subTest(matches=matches), \
                 patch("colombo.brain.cell_dispatch.process_matches", return_value=matches), \
                 patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
                result = self.adapter.run(self.task, "A0001")
                self.assertEqual(result["execution_status"], "unknown")
                self.assertFalse((self.folder / "receipt.json").exists())
                launch.assert_not_called()

    def test_live_worker_without_receipt_remains_running(self):
        with patch("colombo.brain.cell_dispatch.process_matches", return_value=True):
            self.assertIsNone(self.adapter.reconcile(self.task, "A0001"))

    def test_late_receipt_before_nonce_mismatch_uses_full_receipt_validation(self):
        def read_then_publish(path):
            value = read_json(path)
            if path.name == "worker.json":
                self.publish()
                value["nonce"] = "stale-worker"
            return value

        with patch("colombo.brain.cell_dispatch.read_json", side_effect=read_then_publish):
            self.assertEqual(self.adapter.reconcile(self.task, "A0001"), self.result)

    def test_late_receipt_before_unidentified_launch_expiry_is_collected(self):
        (self.folder / "worker.json").unlink()
        write_json(self.folder / "launch.json", {**self.launch, "identity": None})
        now = time.time()

        def expired():
            self.publish()
            return now

        with patch("colombo.brain.cell_dispatch.time.time", side_effect=expired):
            self.assertEqual(self.adapter.reconcile(self.task, "A0001"), self.result)

    def test_late_malformed_receipt_is_not_accepted(self):
        def exited(_identity):
            (self.folder / "receipt.json").write_text("{", encoding="utf-8")
            return False

        with patch("colombo.brain.cell_dispatch.process_matches", side_effect=exited):
            with self.assertRaises(json.JSONDecodeError):
                self.adapter.reconcile(self.task, "A0001")

    def test_late_receipt_cannot_change_scope_or_canonical_result_path(self):
        for change in ({"attempt_id": "A0002"}, {"assignment_ref": {"id": "different"}},
                       {"package_ref": {"id": "different"}},
                       {"result_path": "results/A0002/result.json"}):
            with self.subTest(change=change):
                receipt = self.folder / "receipt.json"
                if receipt.exists():
                    receipt.unlink()

                def exited(_identity):
                    self.publish(receipt_changes=change)
                    return False

                with patch("colombo.brain.cell_dispatch.process_matches", side_effect=exited):
                    with self.assertRaises(ValueError):
                        self.adapter.reconcile(self.task, "A0001")

    def test_late_receipt_checks_result_scope_and_artifact_paths(self):
        for change in ({"attempt_id": "A0002"},
                       {"artifacts": [{"path": "missing.md"}]},
                       {"artifacts": [{"path": "../outside.md"}]}):
            with self.subTest(change=change):
                receipt = self.folder / "receipt.json"
                if receipt.exists():
                    receipt.unlink()

                def exited(_identity):
                    self.publish(result_changes=change)
                    return False

                with patch("colombo.brain.cell_dispatch.process_matches", side_effect=exited):
                    with self.assertRaises(ValueError):
                        self.adapter.reconcile(self.task, "A0001")

    def test_existing_receipt_is_replayed_without_process_check(self):
        self.publish()
        with patch("colombo.brain.cell_dispatch.process_matches") as check, \
             patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
            self.assertEqual(self.adapter.run(self.task, "A0001"), self.result)
            check.assert_not_called()
            launch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
