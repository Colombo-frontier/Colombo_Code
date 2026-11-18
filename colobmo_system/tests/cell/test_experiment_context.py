"""Explicit Experiment bindings retain the original storage-open boundaries."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from colombo.cell import record_store
from colombo.shared.experiment_execution import ExperimentError, run_experiment
from colombo.shared.tool_jobs import experiment_context


class ExperimentContextTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="experiment-context-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "workspace"

    def test_invalid_request_does_not_open_or_initialize_research_storage(self):
        with patch.object(record_store, "Store") as store:
            context = experiment_context(self.root)
            store.assert_not_called()
            context = replace(context, read_settings=lambda: {
                "experiment": {}, "limits": {"request_id_max_chars": 100}})
            with self.assertRaisesRegex(ExperimentError, "nonempty strings"):
                run_experiment(self.root, "", {"kind": "claims", "id": "a", "revision": 1},
                               "print(0)", "request-1", context=context)
            store.assert_not_called()
        self.assertFalse(self.root.exists())

    def test_fixed_refs_share_reader_but_each_checkpoint_reopens_store(self):
        reader, first_writer, second_writer = Mock(), Mock(), Mock()
        target = {"kind": "claims", "id": "a", "revision": 1}
        attempt = {"kind": "attempts", "id": "b", "revision": 1}
        reader.resolve_record_refs.side_effect = [[target], [attempt]]
        first_writer.write_experiment_result.return_value = {"revision": 1}
        second_writer.write_experiment_result.return_value = {"revision": 2}
        with patch.object(record_store, "Store", side_effect=[reader, first_writer, second_writer]) as store:
            context = experiment_context(self.root)
            self.assertEqual(context.resolve_refs([target]), [target])
            self.assertEqual(context.resolve_refs([attempt]), [attempt])
            self.assertEqual(store.call_count, 1)
            self.assertEqual(context.write_result("exp-a", {"status": "running"}), {"revision": 1})
            self.assertEqual(context.write_result("exp-a", {"status": "completed"}), {"revision": 2})
            self.assertEqual(store.call_count, 3)
            for call in store.call_args_list:
                self.assertEqual(call.args, (self.root / "memory",))
        reader.write_experiment_result.assert_not_called()
        first_writer.write_experiment_result.assert_called_once_with("exp-a", {"status": "running"})
        second_writer.write_experiment_result.assert_called_once_with("exp-a", {"status": "completed"})


if __name__ == "__main__":
    unittest.main()
