"""Real process-tree cancellation and durable stop/result arbitration."""
from pathlib import Path
import importlib
import json
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from colombo.brain.cell_dispatch import CellAdapter
from colombo.shared.process_control import execution_scope, process_identity, process_matches
from colombo.shared.file_io import read_json, write_json


PROJECT = Path(__file__).resolve().parents[2]
from colombo.cell import worker as worker


class StopProtocolTests(unittest.TestCase):
    def setUp(self):
        parent = PROJECT / "validation/tmp"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="stop-", dir=parent)
        self.root = Path(self.temp.name)
        self.task = self.root / "T0001"
        package = self.task / "input/package"
        package.mkdir(parents=True)
        (self.task / "input/problem.md").write_text("Synthetic cancellation fixture", encoding="utf-8")
        (package / "README.md").write_text("No additional inputs", encoding="utf-8")
        write_json(package / "manifest.json", {"items": []})
        self.config = {"cell": {"max_rounds": 1, "timeout_seconds": 60,
            "run_timeout_seconds": 30, "search": False,
            "settings_overrides": {"parallel": {"max_depth": 0}}}}
        self.adapter = CellAdapter(PROJECT, self.config)
        self.adapter.prepare(self.task, {"task_id": "T0001", "instructions": "fixture"}, package,
                             assignment_ref={"id": "assignment-1"}, package_ref={"id": "package-1"})
        self.folder = self.task / "attempts/A0001"
        self.decision = {"id": "prune-decision-fixed", "kind": "prune_decision"}

    def tearDown(self):
        self.temp.cleanup()

    def request(self):
        self.folder.mkdir(parents=True, exist_ok=True)
        value = {"task_dir": str(self.task), "project_root": str(PROJECT),
                 "attempt_id": "A0001", "resume": False, "config": self.adapter.config,
                 **execution_scope({**read_json(self.task / "prepared.json"), "attempt_id": "A0001"})}
        write_json(self.folder / "request.json", value)
        write_json(self.folder / "launch.json", {"nonce": "fixture", "created_at": time.time()})
        return self.folder / "request.json"

    def stop(self, request_id="stop-1", decision=None):
        return self.adapter.request_stop(self.task, "A0001", decision or self.decision, request_id)

    def test_stop_before_start_never_launches_and_replays(self):
        outcome = self.stop()
        self.assertEqual(outcome["status"], "cancelled")
        with patch("colombo.brain.cell_dispatch.subprocess.Popen") as spawn:
            result = self.adapter.run(self.task, "A0001")
            spawn.assert_not_called()
        self.assertEqual(result["execution_status"], "cancelled")
        self.assertFalse(result["started"])
        self.assertFalse(result["accepted"])
        self.assertEqual(result["artifacts"], [])
        self.assertFalse((self.folder / "launch.json").exists())
        self.assertEqual(CellAdapter(PROJECT, self.config).reconcile(self.task, "A0001"), result)
        self.assertEqual(read_json(self.folder / "stop_receipt.json")["status"], "cancelled")

    def test_duplicate_stop_preserves_first_decision_and_rejects_id_conflict(self):
        self.stop()
        original = (self.folder / "stop_request.json").read_bytes()
        self.assertEqual(self.stop()["status"], "cancelled")
        next_stop = self.stop("stop-2", {"id": "another-reviewed-decision"})
        self.assertEqual(next_stop["stop_request"]["request_id"], "stop-1")
        self.assertEqual((self.folder / "stop_request.json").read_bytes(), original)
        with self.assertRaisesRegex(ValueError, "reused"):
            self.stop("stop-1", {"id": "changed"})

    def test_stop_schema_version_requires_integer_two(self):
        self.stop()
        path = self.folder / "stop_request.json"
        original = read_json(path)
        for version in (None, 1, True, 2.0):
            with self.subTest(version=version):
                write_json(path, {**original, "schema_version": version})
                with self.assertRaises(ValueError):
                    self.adapter.reconcile(self.task, "A0001")
        write_json(path, original)

    def test_stop_is_bound_to_frozen_scope_and_cancelled_result(self):
        self.stop()
        path = self.task / "prepared.json"
        old = read_json(path)
        write_json(path, {**old, "assignment_ref": {"id": "another-assignment"}})
        with self.assertRaisesRegex(ValueError, "scope"):
            self.adapter.reconcile(self.task, "A0001")
        write_json(path, old)
        result = self.task / "results/A0001/result.json"
        write_json(result, {**read_json(result), "attempt_id": "A0002"})
        with self.assertRaises(ValueError):
            self.adapter.reconcile(self.task, "A0001")

    def test_natural_result_is_preserved_when_stop_arrives_late(self):
        request = self.request()
        result = worker.export_result(request, "finished", "normal")
        fixed = (self.task / "results/A0001/result.json").read_bytes()
        outcome = self.stop()
        self.assertEqual(outcome["status"], "already_completed")
        self.assertEqual(self.adapter.reconcile(self.task, "A0001"), result)
        self.assertEqual((self.task / "results/A0001/result.json").read_bytes(), fixed)
        self.assertEqual(read_json(self.folder / "stop_receipt.json")["status"], "already_completed")

    def test_result_freeze_before_receipt_can_be_replayed_without_reexport(self):
        request = self.request()
        with patch.object(worker, "_publish_receipt", side_effect=RuntimeError("crash after result freeze")):
            with self.assertRaises(RuntimeError):
                worker.export_result(request, "incomplete", "fixture")
        result_file = self.task / "results/A0001/result.json"
        frozen = result_file.read_bytes()
        self.assertFalse((self.folder / "receipt.json").exists())
        with patch.object(worker, "_cell_imports", side_effect=AssertionError("Must not re-export")):
            replay = worker.export_result(request, "error", "changed retry reason")
        self.assertEqual(result_file.read_bytes(), frozen)
        self.assertEqual(self.adapter.reconcile(self.task, "A0001"), replay)

    def test_stop_before_supervisor_launches_solver_prevents_solver_start(self):
        request = self.request()
        self.assertEqual(self.stop()["status"], "requested")
        with patch.object(worker, "managed_popen") as spawn:
            worker.supervise(request)
            spawn.assert_not_called()
        result = self.adapter.reconcile(self.task, "A0001")
        self.assertEqual(result["execution_status"], "cancelled")
        self.assertFalse(result["started"])
        self.assertEqual(read_json(self.folder / "stop_receipt.json")["status"], "cancelled")

    def test_cancel_does_not_erase_previously_valid_acceptance(self):
        request = self.request()
        self.stop()
        stop = read_json(self.folder / "stop_request.json")
        (self.task / "cell/manuscript.md").write_text("Synthetic previously accepted proof", encoding="utf-8")
        write_json(self.task / "cell/submission.json", {"outcome": "proved", "status": "accepted"})
        imports = worker._cell_imports(PROJECT)
        with patch.object(worker, "_cell_imports", return_value=(*imports[:-1], lambda _: True)):
            result = worker.export_result(request, "cancelled", "pruned", stop=stop)
        self.assertEqual(result["execution_status"], "cancelled")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["scientific_outcome"], "proved")
        self.assertEqual(result["stop_request"]["decision_ref"], self.decision)

    def test_supervisor_stops_real_process_tree_and_preserves_partial_material(self):
        request = self.request()
        fixture = self.root / "tree_solver.py"
        fixture.write_text('''import argparse,json,pathlib,subprocess,sys,time
sys.path.insert(0, SOURCE)
from colombo.shared.process_control import process_identity
from colombo.shared.file_io import write_json
p=argparse.ArgumentParser();p.add_argument('mode');p.add_argument('--request');a=p.parse_args()
r=json.loads(pathlib.Path(a.request).read_text());task=pathlib.Path(r['task_dir'])
child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])
(task/'cell/draft.md').write_text('Synthetic partial research survives pruning',encoding='utf-8')
write_json(task/'tree-ready.json',{'parent':process_identity(),'child':process_identity(child.pid)})
time.sleep(60)
'''.replace("SOURCE", repr(str(PROJECT / "src"))), encoding="utf-8")
        errors = []
        def supervise():
            try:
                worker.supervise(request)
            except BaseException as exc:
                errors.append(exc)
        with patch.object(worker, "__file__", str(fixture)):
            thread = threading.Thread(target=supervise, daemon=True)
            thread.start()
            try:
                deadline = time.monotonic() + 8
                while not (self.task / "tree-ready.json").exists() and time.monotonic() < deadline:
                    time.sleep(0.03)
                self.assertTrue((self.task / "tree-ready.json").exists())
                identities = read_json(self.task / "tree-ready.json")
                self.assertTrue(process_matches(identities["parent"]))
                self.assertTrue(process_matches(identities["child"]))
                began = time.monotonic()
                self.stop()
                thread.join(8)
                self.assertFalse(thread.is_alive())
                self.assertLess(time.monotonic() - began, 8)
                self.assertFalse(errors, str(errors))
                self.assertFalse(process_matches(identities["parent"]))
                self.assertFalse(process_matches(identities["child"]))
                result = self.adapter.reconcile(self.task, "A0001")
                self.assertEqual(result["execution_status"], "cancelled")
                self.assertEqual(result["stop_reason"], "pruned")
                self.assertTrue(result["started"])
                self.assertFalse(result["accepted"])
                draft = next(a for a in result["artifacts"] if a["path"].endswith("draft.md"))
                self.assertIn("partial research", (self.task / draft["path"]).read_text())
                self.assertEqual(read_json(self.folder / "stop_receipt.json")["status"], "cancelled")
                with patch("colombo.brain.cell_dispatch.subprocess.Popen") as spawn:
                    replay = CellAdapter(PROJECT, self.config).run(self.task, "A0001")
                    spawn.assert_not_called()
                self.assertEqual(replay, result)
            finally:
                if thread.is_alive():
                    self.stop()
                    thread.join(12)

    def test_natural_exit_observed_before_stop_wins_race(self):
        request = self.request()
        class Completed:
            pid = process_identity()["pid"]
            def poll(self):
                return 0
        def completed(*args, **kwargs):
            self.stop()
            return Completed()
        with patch.object(worker, "managed_popen", side_effect=completed), \
             patch.object(worker, "terminate_tree", return_value=True), \
             patch.object(worker, "close_process_job"):
            worker.supervise(request)
        result = self.adapter.reconcile(self.task, "A0001")
        self.assertNotEqual(result["execution_status"], "cancelled")
        self.assertEqual(read_json(self.folder / "stop_receipt.json")["status"], "already_completed")


if __name__ == "__main__":
    unittest.main()
