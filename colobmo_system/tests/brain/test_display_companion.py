import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("keep_display_awake", PROJECT / "scripts/keep_display_awake.py")
companion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(companion)


class DisplayCompanionTests(unittest.TestCase):
    def setUp(self):
        root = PROJECT / "validation/tmp"
        root.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="display-companion-", dir=root)
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)
        self.source, self.status = self.folder / "supervisor.json", self.folder / "companion.json"
        self.source.write_text(json.dumps({"status": "running",
            "supervisor": {"identity": {"pid": 1, "start_token": "one"}},
            "controller": {"identity": {"pid": 2, "start_token": "two"}}}), encoding="utf-8")

    def test_release_on_exit_and_pid_reuse_rejection(self):
        with patch.object(companion, "identity_or_error", return_value={"identity": None}), \
             patch.object(companion, "process_matches", side_effect=[True, True, True, False]) as matches, \
             patch.object(companion, "set_execution_state") as power, patch.object(companion.time, "sleep"):
            companion.watch(self.source, self.status)
        self.assertEqual(power.call_args_list[0].args, (0x80000003,))
        self.assertEqual(power.call_args_list[-1].args, (0x80000000,))
        self.assertEqual(matches.call_args.args[0], {"pid": 2, "start_token": "two"})
        state = json.loads(self.status.read_text(encoding="utf-8"))
        self.assertFalse(state["display_request_active"])
        self.assertEqual(state["reason"], "target_exited_or_identity_unconfirmed")

    def test_release_on_monitor_failure(self):
        with patch.object(companion, "identity_or_error", return_value={"identity": None}), \
             patch.object(companion, "process_matches", return_value=True), \
             patch.object(companion, "set_execution_state") as power, \
             patch.object(companion.time, "sleep", side_effect=RuntimeError("fixture")):
            with self.assertRaisesRegex(RuntimeError, "fixture"):
                companion.watch(self.source, self.status)
        self.assertEqual(power.call_args.args, (0x80000000,))
        self.assertFalse(json.loads(self.status.read_text(encoding="utf-8"))["display_request_active"])


if __name__ == "__main__":
    unittest.main()
