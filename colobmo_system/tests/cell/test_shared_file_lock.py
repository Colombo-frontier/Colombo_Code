"""Shared lock mechanics preserve each Cell operation's busy/error boundary."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.shared.file_io import file_lock
from colombo.cell.settings import _settings_lock
from colombo.cell.record_store import Store
from colombo.cell.verifier.proof_review import _exclusive_review, _ReviewBusy
from colombo.cell.verifier.challenge import _lock as challenge_lock, ChallengeError
from colombo.shared.experiment_execution import _operation, ExperimentError


class SharedFileLockTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="cell-lock-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()

    def test_nonblocking_operations_keep_their_busy_result(self):
        cases = [
            (self.root / ".review.lock", lambda: _exclusive_review(self.root / ".review.lock"), _ReviewBusy),
            (self.root / "challenges/.lock", lambda: challenge_lock(self.root), ChallengeError),
            (self.root / "experiments/.lock", lambda: _operation(self.root), ExperimentError),
        ]
        for path, operation, busy in cases:
            with self.subTest(path=path):
                with file_lock(path):
                    with self.assertRaises(busy):
                        with operation():
                            self.fail("A second writer acquired the same lock")

    def test_operation_timeout_is_not_reported_as_lock_contention(self):
        operations = [lambda: _exclusive_review(self.root / ".review.lock"),
                      lambda: challenge_lock(self.root), lambda: _operation(self.root),
                      lambda: _settings_lock(self.root, 0, 0.01)]
        for operation in operations:
            with self.subTest(operation=operation):
                failure = TimeoutError("The protected operation failed")
                with self.assertRaises(TimeoutError) as raised:
                    with operation():
                        raise failure
                self.assertIs(raised.exception, failure)
                # Exceptional exit still releases the OS lock.
                with operation():
                    pass

    def test_store_recovers_only_after_acquiring_its_writer_lock(self):
        store = Store(self.root / "memory")

        def recover():
            with self.assertRaises(TimeoutError):
                with file_lock(self.root / "memory/.lock", timeout=0):
                    self.fail("Recovery ran without the writer lock")

        with patch.object(store, "_recover", side_effect=recover) as recovery:
            with store._locked():
                recovery.assert_called_once_with()
        with file_lock(self.root / "memory/.lock", timeout=0):
            pass


if __name__ == "__main__":
    unittest.main()
