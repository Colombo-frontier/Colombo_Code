"""Durability and failure boundaries of the shared file writer."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.shared import file_io as file_utils


class AtomicWriteTests(unittest.TestCase):
    def test_flush_and_fsync_precede_atomic_replacement(self):
        with tempfile.TemporaryDirectory(prefix="atomic-write-") as directory:
            destination = Path(directory) / "record.json"
            destination.write_bytes(b"old")
            events = []
            original_fsync = os.fsync
            original_replace = os.replace

            def sync(descriptor):
                self.assertEqual(destination.read_bytes(), b"old")
                temporary, = destination.parent.glob(".w-*.tmp")
                # The buffered payload must already have reached the file.
                self.assertEqual(temporary.read_bytes(), b"new")
                original_fsync(descriptor)
                events.append("fsync")

            def replace(source, target):
                self.assertEqual(events, ["fsync"])
                self.assertEqual(Path(str(source)).parent, destination.parent)
                original_replace(source, target)
                events.append("replace")

            with patch.object(file_utils.os, "fsync", side_effect=sync), \
                    patch.object(file_utils.os, "replace", side_effect=replace):
                file_utils.atomic_write(destination, b"new")
            self.assertEqual(events, ["fsync", "replace"])
            self.assertEqual(destination.read_bytes(), b"new")
            self.assertEqual(list(destination.parent.iterdir()), [destination])

    def test_fsync_failure_preserves_previous_file_and_removes_temporary(self):
        with tempfile.TemporaryDirectory(prefix="atomic-write-") as directory:
            destination = Path(directory) / "record.json"
            destination.write_bytes(b"old")
            with patch.object(file_utils.os, "fsync", side_effect=OSError("disk sync failed")), \
                    patch.object(file_utils.os, "replace") as replace:
                with self.assertRaisesRegex(OSError, "disk sync failed"):
                    file_utils.atomic_write(destination, b"new")
            replace.assert_not_called()
            self.assertEqual(destination.read_bytes(), b"old")
            self.assertEqual(list(destination.parent.iterdir()), [destination])


if __name__ == "__main__":
    unittest.main()
