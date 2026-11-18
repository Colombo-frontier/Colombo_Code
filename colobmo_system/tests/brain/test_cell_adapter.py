from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
import sys
import zipfile
from unittest.mock import patch

from colombo.brain.cell_dispatch import CellAdapter, CellWaitCancelled
from colombo.shared.file_io import atomic_write, freeze_json, json_equal, read_json, write_json
from colombo.shared.process_control import execution_scope, process_identity, process_matches
from colombo.shared.file_io import Path as IOPath, io_path


PROJECT = Path(__file__).resolve().parents[2]


FAKE_WORKER = r'''
import argparse,json,pathlib,time
p=argparse.ArgumentParser();p.add_argument('mode');p.add_argument('--request');a=p.parse_args()
f=pathlib.Path(a.request);r=json.loads(f.read_text());t=pathlib.Path(r['task_dir'])
folder=t/'results'/r['attempt_id'];folder.mkdir(parents=True,exist_ok=True)
payload=b'fixed fake worker output\n';artifact=folder/'artifact.txt';artifact.write_bytes(payload)
result={'execution_status':'incomplete','accepted':False,'review_status':'not_submitted','scientific_outcome':None,'summary':'fake result','stop_reason':'test','artifacts':[{'path':artifact.relative_to(t).as_posix(),'size':len(payload),'kind':'test'}],'run_dir':str(t/'cell'),**{k:r[k] for k in ('task_id','attempt_id','assignment_ref','package_ref')}}
out=folder/'result.json';out.write_text(json.dumps(result),encoding='utf-8')
receipt={**{k:r[k] for k in ('task_id','attempt_id','assignment_ref','package_ref')},'result_path':out.relative_to(t).as_posix()}
(f.parent/'receipt.json').write_text(json.dumps(receipt),encoding='utf-8')
'''


class CellAdapterTests(unittest.TestCase):
    def setUp(self):
        temporary_root = PROJECT / "validation" / "tmp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="cell-", dir=temporary_root)
        self.root = Path(self.tmp.name)
        self.task = self.root / "T0001"
        package = self.task / "input/package"
        package.mkdir(parents=True)
        (self.task / "input/problem.md").write_text("Prove that 2 is even.", encoding="utf-8")
        (package / "README.md").write_text("Read the attached definition.", encoding="utf-8")
        (package / "definition.md").write_text("An integer n is even iff n = 2k for an integer k.", encoding="utf-8")
        write_json(package / "manifest.json", {"package_id": "PKG-T0001", "items": []})
        self.package = package
        self.assignment = {"task_id": "T0001", "title": "Parity", "instructions": "Prove that 2 is even.",
                           "deliverables": ["proof"], "completion_criteria": ["A justified statement"],
                           "package": {"items": []}, "mode": "new", "resume_task_id": ""}
        self.config = {"cell": {"max_rounds": 1, "timeout_seconds": 60, "run_timeout_seconds": 30,
                                "search": False, "settings_overrides": {"parallel": {"max_depth": 0}}}}
        self.adapter = CellAdapter(PROJECT, self.config)
        self.refs = {"assignment_ref": {"id": "assignment-1", "kind": "assignment", "path": "records/a.json"},
                     "package_ref": {"id": "package-1", "kind": "context_package", "path": "records/p.json"}}

    def tearDown(self):
        self.tmp.cleanup()

    def test_static_model_catalog_is_explicit_and_source_path_is_forwarded(self):
        with patch.dict(os.environ, {"CELL_MODEL_CATALOG_JSON": "unrelated-host-catalog.json"}):
            self.assertNotIn("CELL_MODEL_CATALOG_JSON", self.adapter._env())
            self.adapter.config["model_catalog_json"] = "validation/explicit-catalog.json"
            self.assertEqual(self.adapter._env()["CELL_MODEL_CATALOG_JSON"],
                             str(PROJECT / "validation/explicit-catalog.json"))
            source = self.root / "catalog.json"
            self.adapter.config["model_catalog_json"] = str(source)
            self.assertEqual(self.adapter._env()["CELL_MODEL_CATALOG_JSON"], str(source))

    def test_prepare_initializes_original_cell_before_research_and_is_idempotent(self):
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        config = json.loads((self.task / "cell/run.json").read_text())
        problem = (self.task / "cell/problem.md").read_bytes()
        self.assertEqual(config["storage_version"], 2)  # Embedded Cell retains its own format.
        self.assertEqual(json.loads((self.task / "prepared.json").read_text())["storage_version"], 3)
        self.assertIn("inputs/package/README.md", problem.decode())
        self.assertEqual((self.task / "cell/inputs/package/definition.md").read_bytes(),
                         (self.package / "definition.md").read_bytes())
        self.assertFalse((self.task / "cell/runtime/prover_state.json").exists())
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)

    def test_changed_assignment_or_package_reference_cannot_replace_existing_inputs(self):
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        with self.assertRaises(ValueError):
            self.adapter.prepare(self.task, {**self.assignment, "instructions": "Different target"}, self.package, **self.refs)
        with self.assertRaises(ValueError):
            self.adapter.prepare(self.task, self.assignment, self.package,
                                 **{**self.refs, "package_ref": {"id": "different-package"}})

    def test_required_package_items_are_fixed_review_inputs(self):
        write_json(self.package / "record.json", {"id": "material-1"})
        write_json(self.package / "manifest.json", {"items": [{"importance": "required",
            "record_path": "record.json", "artifacts": [{"package_path": "definition.md"}]}]})
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        config_path = self.task / "cell/run.json"
        config = read_json(config_path)
        self.assertEqual(config["required_review_files"], ["inputs/package/README.md", "inputs/package/manifest.json",
                                                         "inputs/package/record.json", "inputs/package/definition.md"])
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        write_json(config_path, {**config, "required_review_files": []})
        with self.assertRaisesRegex(ValueError, "review inputs"):
            self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)

    def test_missing_required_package_file_is_rejected_before_preparation(self):
        write_json(self.package / "manifest.json", {"items": [{"importance": "required",
            "record_path": "missing.json", "artifacts": []}]})
        with patch("colombo.brain.cell_dispatch.subprocess.run") as launch:
            with self.assertRaisesRegex(ValueError, "missing or outside"):
                self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        launch.assert_not_called()

    def test_prepared_storage_version_requires_integer_two(self):
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        path = self.task / "prepared.json"
        original = read_json(path)
        for version in (None, 1, True, 2.0):
            with self.subTest(version=version):
                write_json(path, {**original, "storage_version": version})
                with self.assertRaises(ValueError):
                    self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
                with self.assertRaises(ValueError):
                    self.adapter.run(self.task, "A0001")
        write_json(path, original)

    def test_supervisor_result_replayed_without_relaunch_and_wrong_attempt_rejected(self):
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        fake = self.root / "fake.py"
        fake.write_text(FAKE_WORKER, encoding="utf-8")
        self.adapter.worker = fake
        result = self.adapter.run(self.task, "A0001")
        self.assertFalse(result["accepted"])
        with patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
            self.assertEqual(self.adapter.run(self.task, "A0001"), result)
            launch.assert_not_called()
        receipt_path = self.task / "attempts/A0001/receipt.json"
        write_json(receipt_path, {**read_json(receipt_path), "attempt_id": "A0002"})
        with self.assertRaises(ValueError):
            self.adapter.reconcile(self.task, "A0001")

    def test_reconcile_reads_receipt_and_result_without_scanning_artifact_bodies(self):
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        fake = self.root / "fake.py"
        fake.write_text(FAKE_WORKER, encoding="utf-8")
        self.adapter.worker = fake
        expected = self.adapter.run(self.task, "A0001")
        with patch.object(Path, "read_bytes", side_effect=AssertionError("No attachment body scan")):
            self.assertEqual(self.adapter.reconcile(self.task, "A0001"), expected)

    def test_receipt_cannot_redirect_to_another_result_or_assignment(self):
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        fake = self.root / "fake.py"
        fake.write_text(FAKE_WORKER, encoding="utf-8")
        self.adapter.worker = fake
        self.adapter.run(self.task, "A0001")
        receipt_path = self.task / "attempts/A0001/receipt.json"
        original = read_json(receipt_path)
        for change in ({"assignment_ref": {"id": "assignment-2"}},
                       {"package_ref": {"id": "package-2"}},
                       {"result_path": "results/A0002/result.json"}):
            with self.subTest(change=change):
                write_json(receipt_path, {**original, **change})
                with self.assertRaises(ValueError):
                    self.adapter.reconcile(self.task, "A0001")
        write_json(receipt_path, original)

    def test_uncertain_launch_never_restarts_automatically(self):
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        folder = self.task / "attempts/A0001"
        folder.mkdir(parents=True)
        write_json(folder / "launch.json", {"nonce": "test", "created_at": time.time() - 60,
                                           "identity": None, "state": "launching"})
        with patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
            result = self.adapter.run(self.task, "A0001")
            launch.assert_not_called()
        self.assertEqual(result["execution_status"], "unknown")

    def test_cancelling_wait_keeps_started_supervisor_recoverable(self):
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        fake = self.root / "delayed_fake.py"
        pause = """
(t/'worker-ready').write_text('ready')
deadline=time.monotonic()+10
while not (t/'continue-worker').exists() and time.monotonic()<deadline:
    time.sleep(0.02)
if not (t/'continue-worker').exists():
    raise SystemExit('Test did not release worker')
"""
        fake.write_text(FAKE_WORKER.replace("folder=t/'results'", pause + "\nfolder=t/'results'"), encoding="utf-8")
        self.adapter.worker = fake
        cancellation = threading.Event()
        errors = []

        def wait_for_attempt():
            try:
                self.adapter.run(self.task, "A0001", cancel_event=cancellation)
            except BaseException as exc:
                errors.append(exc)

        thread = threading.Thread(target=wait_for_attempt, daemon=True)
        thread.start()
        try:
            deadline = time.monotonic() + 5
            launch_path = self.task / "attempts/A0001/launch.json"
            while time.monotonic() < deadline:
                if (self.task / "worker-ready").exists() and launch_path.is_file():
                    if read_json(launch_path).get("identity"):
                        break
                time.sleep(0.02)
            self.assertTrue((self.task / "worker-ready").exists())
            identity = read_json(launch_path)["identity"]
            cancellation.set()
            thread.join(1)
            self.assertFalse(thread.is_alive(), "Cancellation must promptly release the controller thread")
            self.assertEqual(len(errors), 1)
            self.assertIsInstance(errors[0], CellWaitCancelled)
            self.assertTrue(process_matches(identity), "Detaching must not terminate the supervisor")
            self.assertFalse((self.task / "attempts/A0001/receipt.json").exists())
            self.assertIsNone(self.adapter.reconcile(self.task, "A0001"))
            (self.task / "continue-worker").touch()
            # Mock only this module's launch API; process identity checks retain
            # the real subprocess module, including macOS ps queries.
            with patch("colombo.brain.cell_dispatch.subprocess") as launch:
                result = self.adapter.run(self.task, "A0001")
                launch.Popen.assert_not_called()
                launch.run.assert_not_called()
            self.assertEqual(result["execution_status"], "incomplete")
            self.assertEqual(self.adapter.reconcile(self.task, "A0001"), result)
        finally:
            (self.task / "continue-worker").touch()
            cancellation.set()
            thread.join(5)
            # Allow the detached process to close its own files before teardown.
            if launch_path.is_file():
                identity = read_json(launch_path).get("identity")
                deadline = time.monotonic() + 5
                while identity and process_matches(identity) and time.monotonic() < deadline:
                    time.sleep(0.02)

    def test_pre_cancelled_wait_never_starts_an_attempt(self):
        cancellation = threading.Event()
        cancellation.set()
        with patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
            with self.assertRaises(CellWaitCancelled):
                self.adapter.run(self.task, "A0001", cancel_event=cancellation)
            launch.assert_not_called()
        self.assertFalse((self.task / "attempts/A0001").exists())

    def test_process_identity_checks_creation_token(self):
        identity = process_identity()
        self.assertTrue(process_matches(identity))
        self.assertFalse(process_matches({**identity, "start_token": "wrong"}))

    def test_new_attempt_is_blocked_while_previous_execution_is_unknown(self):
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        folder = self.task / "attempts/A0001"
        folder.mkdir(parents=True)
        write_json(folder / "launch.json", {"nonce": "test", "created_at": time.time() - 60,
                                           "identity": None, "state": "launching"})
        with patch("colombo.brain.cell_dispatch.subprocess.Popen") as launch:
            with self.assertRaises(RuntimeError):
                self.adapter.run(self.task, "A0002", resume=True)
            launch.assert_not_called()

    def test_actual_worker_failure_exports_partial_material_without_false_acceptance(self):
        # A nonexistent explicit binary prevents every model call, exercising actual runner/export paths.
        self.config["cell"]["codex_bin"] = str(self.root / "does-not-exist.exe")
        self.adapter = CellAdapter(PROJECT, self.config)
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        result = self.adapter.run(self.task, "A0001")
        self.assertFalse(result["accepted"])
        self.assertIn(result["execution_status"], {"incomplete", "error"})
        self.assertIsNone(result["scientific_outcome"])
        kinds = {a["kind"] for a in result["artifacts"]}
        self.assertIn("research_memory_snapshot", kinds)
        self.assertIn("cell_document", kinds)
        self.assertTrue((self.task / "attempts/A0001/receipt.json").exists())

    def test_supervisor_enforces_timeout_without_controller(self):
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        folder = self.task / "attempts/A0001"
        folder.mkdir(parents=True)
        prepared = json.loads((self.task / "prepared.json").read_text())
        request = {"task_dir": str(self.task), "project_root": str(PROJECT), "attempt_id": "A0001",
                   **execution_scope({**prepared, "attempt_id": "A0001"}), "config": {"run_timeout_seconds": 0.2}}
        write_json(folder / "request.json", request)
        write_json(folder / "launch.json", {"nonce": "timeout-test", "created_at": time.time()})
        sleeper = self.root / "sleep_worker.py"
        sleeper.write_text("import time\ntime.sleep(60)\n", encoding="utf-8")
        from colombo.cell import worker as cell_worker
        started = time.monotonic()
        with patch.object(cell_worker, "__file__", str(sleeper)):
            cell_worker.supervise(folder / "request.json")
        self.assertLess(time.monotonic() - started, 15)
        result = self.adapter.reconcile(self.task, "A0001")
        self.assertEqual(result["execution_status"], "timeout")
        self.assertFalse(result["accepted"])
        identity = json.loads((folder / "solver.json").read_text())["identity"]
        self.assertFalse(process_matches(identity))


class ProcessFileTests(unittest.TestCase):
    def test_json_comparison_preserves_boolean_and_number_types(self):
        self.assertFalse(json_equal({"value": True}, {"value": 1}))
        self.assertFalse(json_equal({"value": 1}, {"value": 1.0}))
        self.assertTrue(json_equal({"b": 2, "a": 1}, {"a": 1, "b": 2}))

    def test_atomic_write_and_frozen_json_support_paths_over_300_characters(self):
        base = PROJECT / "validation/tmp"
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as name:
            root = Path(name)
            target = root.joinpath(*[(str(i) + "x" * 59) for i in range(4)], "result.json")
            self.assertGreaterEqual(len(str(target)), 300)
            self.assertEqual(str(IOPath(target)), str(target))
            self.assertEqual(IOPath(target).relative_to(IOPath(root)).as_posix(), target.relative_to(root).as_posix())
            self.assertEqual(str(IOPath(io_path(target))), str(target))
            # Read and remove via the native extended path, independently from
            # the helper under test; no machine-wide long-path setting is needed.
            native = Path("\\\\?\\" + str(target)) if os.name == "nt" else target
            try:
                atomic_write(target, b'{"version": 1}')
                self.assertEqual(native.read_bytes(), b'{"version": 1}')
                self.assertEqual(IOPath(target).read_bytes(), b'{"version": 1}')
                atomic_write(target, b'{"version": 2}')
                self.assertEqual(read_json(target), {"version": 2})
                freeze_json(target.parent / "frozen.json", {"fixed": True})
                freeze_json(target.parent / "frozen.json", {"fixed": True})
                with self.assertRaises(ValueError):
                    freeze_json(target.parent / "frozen.json", {"fixed": False})
                self.assertEqual({p.name for p in native.parent.iterdir()}, {"result.json", "frozen.json"})
            finally:
                if native.parent.exists():
                    for item in native.parent.iterdir():
                        item.unlink()
                current = native.parent
                for _ in range(4):
                    if current.exists():
                        current.rmdir()
                    current = current.parent


class CellExportPathTests(unittest.TestCase):
    """Real snapshot/receipt paths; no solver, model or worker process is launched."""

    def setUp(self):
        from colombo.cell import worker as cell_worker
        self.worker = cell_worker
        parent = IOPath(PROJECT / "validation/tmp")
        parent.mkdir(parents=True, exist_ok=True)
        # Keep the native extended prefix for TemporaryDirectory cleanup too.
        self.tmp = tempfile.TemporaryDirectory(prefix="export-path-", dir=io_path(parent))
        self.addCleanup(self.tmp.cleanup)
        self.root = IOPath(self.tmp.name)
        self.task = self.root / "T0001"
        self.cell = self.task / "cell"
        self.cell.mkdir(parents=True)
        (self.cell / "draft.md").write_text("Synthetic incomplete draft", encoding="utf-8")
        self.refs = {"assignment_ref": {"id": "assignment-path", "revision": 1},
                     "package_ref": {"id": "package-path", "revision": 1}}
        write_json(self.task / "prepared.json", {"storage_version": 3, "task_id": "T0001", **self.refs})
        self.request = self.task / "attempts/A0001/request.json"
        write_json(self.request, {"task_dir": str(self.task), "project_root": str(PROJECT),
            "task_id": "T0001", "attempt_id": "A0001", **self.refs})
        self.adapter = CellAdapter(PROJECT, {"cell": {}})
        self.deep_relative = "/".join(["tasks", *("nested-" + str(i) + "x" * 48 for i in range(3)), "evidence.json"])
        self.payload = b'{"synthetic": true}\n'
        atomic_write(self.cell / self.deep_relative, self.payload)
        self.exported = self.task / "results/A0001/artifacts" / self.deep_relative
        self.assertGreaterEqual(len(str(self.exported)), 300)

    def test_deep_snapshot_exports_receipt_and_reconciles(self):
        result = self.worker.export_result(self.request, "incomplete", "Synthetic stopped solver")
        self.assertFalse(result["accepted"])
        self.assertEqual(self.exported.read_bytes(), self.payload)
        self.assertTrue(any(a["path"] == self.exported.relative_to(self.task).as_posix()
                            for a in result["artifacts"]))
        self.assertTrue((self.request.parent / "receipt.json").is_file())
        with zipfile.ZipFile(io_path(self.task / result["archive"]["path"])) as archive:
            self.assertEqual(archive.read(self.deep_relative), self.payload)
        self.assertEqual(self.adapter.reconcile(Path(str(self.task)), "A0001"), result)

    def test_deep_frozen_result_replays_receipt_without_reexport(self):
        with patch.object(self.worker, "_publish_receipt", side_effect=RuntimeError("Interrupted after freeze")):
            with self.assertRaisesRegex(RuntimeError, "Interrupted"):
                self.worker.export_result(self.request, "incomplete", "Original reason")
        result_file = self.task / "results/A0001/result.json"
        fixed = result_file.read_bytes()
        self.assertFalse((self.request.parent / "receipt.json").exists())
        with patch.object(self.worker, "_cell_imports", side_effect=AssertionError("No live re-export")):
            replay = self.worker.export_result(self.request, "error", "Must not replace saved Result")
        self.assertEqual(result_file.read_bytes(), fixed)
        self.assertEqual(replay["stop_reason"], "Original reason")
        self.assertEqual(self.adapter.reconcile(self.task, "A0001"), replay)

    def test_extended_path_support_still_rejects_artifacts_outside_task(self):
        result = self.worker.export_result(self.request, "incomplete", "Synthetic stopped solver")
        outside = self.root / "outside.txt"
        outside.write_text("Outside the fixed Task", encoding="utf-8")
        result_file = self.task / "results/A0001/result.json"
        for invalid in ("../outside.txt", str(outside)):
            with self.subTest(path=invalid):
                changed = {**result, "artifacts": [*result["artifacts"], {"path": invalid}]}
                with self.assertRaisesRegex(ValueError, "artifact path"):
                    self.worker._publish_receipt(self.request, result_file, changed)
                write_json(result_file, changed)
                with self.assertRaisesRegex(ValueError, "artifact path"):
                    self.adapter.reconcile(self.task, "A0001")
        write_json(result_file, result)


if __name__ == "__main__":
    unittest.main()
