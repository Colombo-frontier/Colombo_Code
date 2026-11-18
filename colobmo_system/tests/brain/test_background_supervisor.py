"""No real power requests, controller processes or model calls."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch


PROJECT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("resume_background", PROJECT / "scripts/resume_background.py")
supervisor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(supervisor)


class BackgroundSupervisorTests(unittest.TestCase):
    def setUp(self):
        root = PROJECT / "validation/tmp"
        root.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="supervisor-", dir=root)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.run_dir = self.root / "run"
        self.run_dir.mkdir()
        (self.run_dir / "state.sqlite").write_bytes(b"fixture; never opened")
        self.logs = self.root / "logs"

    def test_power_request_is_released_after_failure(self):
        with patch.object(supervisor, "set_execution_state") as power:
            with self.assertRaisesRegex(RuntimeError, "fixture"):
                with supervisor.keep_system_awake():
                    raise RuntimeError("fixture")
        self.assertEqual([call.args[0] for call in power.call_args_list],
                         [supervisor.ES_CONTINUOUS | supervisor.ES_SYSTEM_REQUIRED, supervisor.ES_CONTINUOUS])

    def test_optional_display_request_is_scoped_to_the_supervisor(self):
        with patch.object(supervisor, "set_execution_state") as power:
            with supervisor.keep_system_awake(keep_display=True):
                self.assertEqual(power.call_args.args, (0x80000003,))
        self.assertEqual(power.call_args.args, (0x80000000,))

    def test_launch_failure_releases_power_and_keeps_failure_record(self):
        with patch.object(supervisor, "set_execution_state") as power, \
             patch.object(supervisor, "identity_or_error", return_value={"identity": {"pid": 1}}), \
             patch.object(supervisor.subprocess, "Popen", side_effect=OSError("fixture launch failed")):
            with self.assertRaises(OSError):
                supervisor.supervise(self.run_dir, self.logs)
        state = json.loads((self.logs / "supervisor.json").read_text(encoding="utf-8"))
        self.assertEqual(state["status"], "failed")
        self.assertFalse(state["keep_awake_active"])
        self.assertIsNone(state["controller"])
        self.assertEqual(power.call_args.args, (supervisor.ES_CONTINUOUS,))

    def test_controller_exit_is_recorded_and_existing_logs_are_not_overwritten(self):
        process = Mock(pid=42)
        process.wait.return_value = 2
        process.poll.return_value = 2
        with patch.object(supervisor, "set_execution_state") as power, \
             patch.object(supervisor, "identity_or_error", return_value={"identity": {"pid": 42, "start_token": "fixture"}}), \
             patch.object(supervisor.subprocess, "Popen", return_value=process) as launch:
            self.assertEqual(supervisor.supervise(self.run_dir, self.logs), 2)
            before = {path.name: path.read_bytes() for path in self.logs.iterdir()}
            with self.assertRaises(FileExistsError):
                supervisor.supervise(self.run_dir, self.logs)
            self.assertEqual(launch.call_count, 1)
            self.assertEqual(before, {path.name: path.read_bytes() for path in self.logs.iterdir()})
        state = json.loads((self.logs / "supervisor.json").read_text(encoding="utf-8"))
        self.assertEqual(state["returncode"], 2)
        self.assertEqual(state["status"], "exited")
        self.assertFalse(state["keep_awake_active"])
        self.assertEqual(state["controller"]["identity"]["start_token"], "fixture")
        self.assertIn("ended_at", state)
        self.assertEqual(power.call_args.args, (supervisor.ES_CONTINUOUS,))


if __name__ == "__main__":
    unittest.main()
