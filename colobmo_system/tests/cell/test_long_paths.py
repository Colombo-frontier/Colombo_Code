"""Real deep-directory I/O, including process state and local audit preparation."""
from __future__ import annotations

import json
import os
from pathlib import Path as OrdinaryPath
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import colombo.shared.file_io as file_utils
import colombo.cell.recovery as handoff
import colombo.cell.controller as run
import colombo.cell.settings as settings
from colombo.shared.file_io import Path
from colombo.shared.file_io import atomic_write
from colombo.shared.file_io import io_path
import colombo.cell.verifier.local_audit as auditing
from colombo.cell.record_store import Store
from colombo.cell.subcell_dispatch import Tasks


ROOT = Path(__file__).resolve().parents[2]


class LongPathTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for name in tuple(os.environ):
            if name.startswith("CELL_"):
                os.environ.pop(name)
        self.root = Path(tempfile.mkdtemp(prefix=".long-paths-", dir=ROOT)).resolve()
        self.addCleanup(self.cleanup)

    def cleanup(self):
        # Only this test's verified private directory is removed. The extended
        # root keeps shutil's internal string traversal valid for descendants.
        root = self.root.resolve()
        if root.parent != ROOT.resolve() or not root.name.startswith(".long-paths-"):
            raise AssertionError("Refusing cleanup outside the private test directory")
        if root.exists():
            shutil.rmtree(root)

    def directory_length(self, length, name="case"):
        current = self.root / name
        gap = length - len(str(current))
        if gap < 0:
            raise AssertionError("Requested path is shorter than the test root")
        pieces = []
        while gap > 61:
            pieces.append("d" * 60)
            gap -= 61
        if gap == 1:
            if not pieces:
                current = self.root / (name + "x")
                gap = 0
            else:
                pieces[-1] = pieces[-1][:-1]
                gap = 2
        if gap:
            pieces.append("d" * (gap - 1))
        path = current.joinpath(*pieces)
        self.assertEqual(len(str(path)), length)
        return path

    def test_exact_boundary_paths_replace_and_roundtrip_without_temporary_files(self):
        filename = "f" * 32 + ".json"
        for length in (229, 259, 260, 267, 350):
            with self.subTest(length=length):
                path = self.directory_length(length - len(filename) - 1, str(length)) / filename
                atomic_write(path, b'{"version":1}')
                atomic_write(path, b'{"version":2}')
                self.assertEqual(json.loads(path.read_text()), {"version": 2})
                self.assertEqual(list(path.parent.iterdir()), [path])
                self.assertEqual(path.resolve(), path)
                self.assertEqual(Path(io_path(path)), path)
                self.assertEqual(path, OrdinaryPath(str(path)))

    def test_atomic_failure_retains_previous_file_and_cleans_short_temporary_name(self):
        target = self.directory_length(310) / ("record-" + "a" * 80 + ".json")
        atomic_write(target, b"old")
        seen = []

        def fail_replace(source, destination):
            seen.append(Path(source))
            self.assertEqual(Path(source).parent, target.parent)
            self.assertLess(len(Path(source).name), 30)
            raise PermissionError("simulated replacement failure")

        with patch.object(file_utils.os, "replace", side_effect=fail_replace):
            with self.assertRaisesRegex(PermissionError, "simulated"):
                atomic_write(target, b"new")
        self.assertEqual(target.read_bytes(), b"old")
        self.assertTrue(seen)
        self.assertFalse(seen[0].exists())
        self.assertEqual(list(target.parent.iterdir()), [target])

    def test_recursive_copy_and_search_start_from_short_root_and_reach_long_descendants(self):
        source = self.root / "source"
        nested = source / ("a" * 100) / ("b" * 100) / ("c" * 60)
        target = nested / "saved.txt"
        atomic_write(target, b"saved evidence")
        self.assertGreater(len(str(target)), 300)
        copied = self.root / "copy"
        shutil.copytree(source, copied)
        found = list(copied.rglob("saved.txt"))
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].read_bytes(), b"saved evidence")
        self.assertEqual(found[0].relative_to(copied), target.relative_to(source))
        shutil.copyfile(found[0], found[0].with_name("copy.txt"))
        os.replace(found[0].with_name("copy.txt"), found[0].with_name("moved.txt"))
        self.assertEqual(found[0].with_name("moved.txt").read_bytes(), b"saved evidence")
        shutil.rmtree(copied)
        self.assertFalse(copied.exists())

    @unittest.skipUnless(os.name == "nt", "Windows prefix normalization")
    def test_extended_drive_and_unc_paths_have_one_plain_identity(self):
        path = self.root / "ordinary.txt"
        self.assertTrue(io_path(path).startswith("\\\\?\\"))
        self.assertFalse(str(Path(io_path(path))).startswith("\\\\?\\"))
        self.assertEqual(Path(io_path(path)), path)
        unc = "\\\\server\\share\\folder\\file.json"
        self.assertEqual(io_path(unc), "\\\\?\\UNC\\server\\share\\folder\\file.json")
        self.assertEqual(str(Path(io_path(unc))), unc)

    def test_native_python_subprocess_uses_short_bootstrap_and_explicit_long_io_output(self):
        work = self.directory_length(305)
        work.mkdir(parents=True)
        output = work / "child-output.txt"
        result = subprocess.run(
            [sys.executable, "-B", "-c", "import sys; open(sys.argv[1], 'w').write('ok')", io_path(output)],
            cwd=self.root, check=True, capture_output=True, text=True, timeout=15,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(output.read_text(), "ok")

    def test_real_subcell_helper_opens_long_absolute_task_directory_from_short_bootstrap(self):
        task = self.directory_length(305)
        workspace = task / "workspace"
        effective = settings.get_settings()
        config = {**settings.run_fields(effective), "settings": effective, "role": "subcell",
                  "task_depth": 2, "agent_options": {"search_enabled": False}}
        atomic_write(workspace / "run.json", json.dumps(config).encode("utf-8"))
        # An already-completed fixture exercises initialization and lookup but
        # must not start a model, use credentials or contact a service.
        atomic_write(task / "task.json", b'{"status":"completed"}')
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "src/colombo/cell/subcell_worker.py"), "--task-dir", str(task)],
            cwd=ROOT, check=True, capture_output=True, text=True, timeout=15,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0,
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue((workspace / "protocol.md").is_file())
        self.assertTrue((workspace / ".agents/skills/handoff/SKILL.md").is_file())
        self.assertEqual(json.loads((workspace / "run.json").read_text())["settings"], effective)

    def test_two_level_task_audit_writes_real_deep_state_and_preserves_certification_boundaries(self):
        problem = self.root / "question.md"
        problem.write_text("Show that 2 is even.", encoding="utf-8")
        work = self.directory_length(max(105, len(str(self.root)) + 12), "run")
        run.initialize(problem, work, profile="hard", search_enabled=False)
        parent = work
        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
            launch.return_value.pid = 12345
            for level in (1, 2):
                target = Store(parent / "memory").archive("claims", {"statement": "2 is even"})
                ref = {key: target[key] for key in ("kind", "id", "revision")}
                child = Tasks(parent).spawn_task(ref, "Check the evenness argument")
                parent = Path(child["workspace"])
                self.assertEqual(settings.get_settings(parent)["parallel"]["max_depth"], 2)
                handoff.begin_process(parent, str(level) * 32, "subcell", 30, settings.get_settings(parent))
                handoff.close_process(parent, str(level) * 32, "completed")
        store = Store(parent / "memory")
        state_paths = []

        def reviewer(verdict):
            def inspect(prompt, audit_work):
                context = json.loads((audit_work / "input.json").read_text(encoding="utf-8"))
                self.assertIn("problem", context)
                handoff.begin_process(audit_work, "a" * 32, "audit", 30, settings.get_settings(parent))
                state = audit_work / "runtime" / "processes" / ("a" * 32 + ".json")
                state_paths.append(state)
                self.assertGreater(len(str(state)), 260)
                self.assertEqual(json.loads(state.read_text())["status"], "running")
                handoff.close_process(audit_work, "a" * 32, "completed")
                if verdict == "service_error":
                    raise OSError("simulated reviewer startup failure")
                return {"verdict": verdict, "summary": "Checked the explicit integer witness",
                        "findings": [] if verdict == "pass" else ["The claimed witness does not establish the result"],
                        "properties": []}
            return inspect

        for verdict in ("pass", "fail", "service_error"):
            record = store.archive("arguments", {"statement": "2 is even", "status": "candidate",
                                                  "proof": "2 = 2 * 1 with 1 an integer."})
            result = auditing.audit(parent, "arguments", record["id"], record["revision"], reviewer=reviewer(verdict))
            self.assertEqual(result["review"]["payload"]["verdict"], verdict)
            self.assertEqual(result["record"]["payload"]["status"], "proved" if verdict == "pass" else "candidate")
        self.assertEqual(len(state_paths), 3)
        self.assertFalse(list(parent.rglob("*.tmp")))


if __name__ == "__main__":
    unittest.main()
