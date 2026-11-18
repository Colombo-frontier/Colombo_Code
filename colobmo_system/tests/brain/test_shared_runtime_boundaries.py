"""Discovery and lock boundaries retained when role runtimes share helpers."""
import os
from contextlib import chdir
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.brain import model_calls as brain_calls
from colombo.cell import model_calls as cell_calls
from colombo.shared import file_io, model_launcher


class SharedRuntimeBoundaryTests(unittest.TestCase):
    def test_cell_explicit_relative_cli_retains_current_directory_prefix(self):
        with tempfile.TemporaryDirectory(prefix="relative-cell-cli-") as folder, chdir(folder):
            Path("codex.exe").write_bytes(b"discovery fixture; never executed")
            with patch.dict(os.environ, {"CELL_CODEX_BIN": "./codex.exe"}, clear=True):
                # Dropping ./ changes an explicit path into a PATH lookup on POSIX.
                self.assertEqual(cell_calls.find_codex(), "./codex.exe")

    def test_lock_retry_wait_cannot_exceed_its_remaining_timeout(self):
        with tempfile.TemporaryDirectory(prefix="bounded-lock-") as folder:
            path = Path(folder) / ".lock"
            with file_io.file_lock(path):
                with patch.object(file_io.time, "monotonic", side_effect=[0, 0, 0, 0.2]), \
                        patch.object(file_io.time, "sleep") as sleep:
                    with self.assertRaises(TimeoutError):
                        with file_io.file_lock(path, timeout=0.2, poll_seconds=100):
                            self.fail("A competing writer acquired the lock")
                sleep.assert_called_once_with(0.2)

    def test_brain_explicit_cli_never_needs_home_or_user_configuration(self):
        with tempfile.TemporaryDirectory(prefix="explicit-brain-cli-") as folder:
            executable = Path(folder) / "codex.exe"
            executable.write_bytes(b"not executed")
            with patch.dict(os.environ, {}, clear=True), \
                    patch.object(Path, "home", side_effect=AssertionError("Home was consulted")), \
                    patch.object(model_launcher, "user_configuration", side_effect=AssertionError("Config was read")):
                self.assertEqual(brain_calls.find_codex({"codex_bin": str(executable)}), str(executable.resolve()))

    def test_cell_explicit_cli_never_needs_home_or_user_configuration(self):
        with tempfile.TemporaryDirectory(prefix="explicit-cell-cli-") as folder:
            executable = Path(folder) / "codex.exe"
            executable.write_bytes(b"not executed")
            with patch.dict(os.environ, {"CELL_CODEX_BIN": str(executable)}, clear=True), \
                    patch.object(Path, "home", side_effect=AssertionError("Home was consulted")), \
                    patch.object(model_launcher, "user_configuration", side_effect=AssertionError("Config was read")):
                self.assertEqual(cell_calls.find_codex(), str(executable))


if __name__ == "__main__":
    unittest.main()
