"""Exercise the real Brain adapter -> preparation worker -> Cell pack boundary."""
import json
import unittest
from unittest.mock import patch

import test_cell_adapter as fixture


class UpperBoundDispatchTests(unittest.TestCase):
    setUp = fixture.CellAdapterTests.setUp
    tearDown = fixture.CellAdapterTests.tearDown

    def test_real_preparation_freezes_upper_pack_and_replay_rejects_mode_switch(self):
        assignment = {"task_id": "T0001", "spec": {**self.assignment, "specialization": "upper_bound"},
                      "research_mode": "oracle_complexity"}
        self.adapter.prepare(self.task, assignment, self.package, **self.refs)
        mode = json.loads((self.task / "cell/run.json").read_text())["cell_mode"]
        self.assertEqual(mode, {"research_mode": "oracle_complexity", "specialization": "upper_bound",
                                "instruction_version": "v8.1"})
        self.assertTrue((self.task / "cell/.agents/skills/upper-bound/SKILL.md").is_file())
        self.assertTrue((self.task / "cell/upper_bound_review_guidance.md").is_file())
        self.assertFalse((self.task / "cell/runtime/prover_state.json").exists())
        self.adapter.prepare(self.task, assignment, self.package, **self.refs)
        switched = {**assignment, "spec": {**assignment["spec"], "specialization": "general"}}
        with self.assertRaises(ValueError):
            self.adapter.prepare(self.task, switched, self.package, **self.refs)
        saved = json.loads((self.task / "cell/run.json").read_text())["cell_mode"]
        self.assertEqual(saved, mode)

    def test_generic_cannot_launch_upper_preparation(self):
        assignment = {"task_id": "T0001", "spec": {**self.assignment, "specialization": "upper_bound"},
                      "research_mode": "generic"}
        with patch("colombo.brain.cell_dispatch.subprocess.run") as child:
            with self.assertRaisesRegex(ValueError, "oracle_complexity"):
                self.adapter.prepare(self.task, assignment, self.package, **self.refs)
        child.assert_not_called()
        self.assertFalse((self.task / "cell/cell_mode.json").exists())


if __name__ == "__main__":
    unittest.main()
