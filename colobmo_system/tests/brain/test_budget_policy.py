"""Colombo Wave allocation must not inherit a historical research deadline."""
from copy import deepcopy
import json
import math
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.shared import runtime_budget as outer_budget
from colombo.configuration import load_config, require_current_workflow
from colombo.shared.runtime_budget import budget_environment, configured_seconds, get_budget_context, inherited_deadline, pause_budget, start_budget
from colombo.cell import recovery as handoff
from colombo.configuration import load_policy, resolve_document
from colombo.cell.verifier import challenge
from colombo.shared import experiment_execution as experiment
import tomllib
from colombo.configuration import PROJECT_ROOT


class BudgetPolicyTests(unittest.TestCase):
    def setUp(self):
        base = PROJECT_ROOT / "validation" / "tmp"
        base.mkdir(parents=True, exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        os.environ.pop("COLOMBO_BUDGET_FILE", None)
        self.config = load_config()

    def legacy_policy(self, seconds):
        value = deepcopy(self.config)
        value["workflow"] = {"version": 2}
        value.pop("integration")
        value["budget"] = {"research": {"total_active_seconds": seconds}}
        value["policy_metadata"]["revision"] = "legacy-fixture"
        return value

    def test_profiles_preserve_wave_limits_and_cell_local_caps(self):
        hard = self.config
        standard = load_policy(profile="standard")
        self.assertEqual(hard["limits"], {"max_rounds": 8, "max_dispatches_per_wave": 6,
                                          "max_parallel_cells": 4})
        self.assertEqual(standard["limits"], {"max_rounds": 3, "max_dispatches_per_wave": 3,
                                              "max_parallel_cells": 2})
        for config in (hard, standard):
            self.assertNotIn("budget", config)
            self.assertEqual(config["integration"], {"timeout_seconds": 7200})
            self.assertEqual(configured_seconds(config), "unlimited")
        self.assertEqual(hard["cell"]["settings"]["agents"]["prover_max_rounds"], 15)
        self.assertEqual(hard["cell"]["settings"]["agents"]["verifier_max_rounds"], 20)
        self.assertEqual(hard["cell"]["settings"]["challenge"], {
            "max_rounds": 4, "max_check_attempts": 4,
            "timeout_seconds": "unlimited", "check_timeout_seconds": "unlimited"})

    def test_usage_persists_across_resume_without_a_time_limit(self):
        with patch("colombo.shared.runtime_budget.time.time", return_value=1000):
            state = outer_budget.start(self.root, self.config)
        self.assertTrue(state["accounting_only"])
        for field in ("deadline_unix", "work_deadline_unix", "hard_deadline_unix"):
            self.assertIsNone(state[field])
        self.assertEqual(state["closing_reserve_seconds"], 0)
        self.assertEqual(state["recovery_reserve_seconds"], 0)
        with patch("colombo.shared.runtime_budget.time.time", return_value=10000):
            paused = outer_budget.pause(self.root, self.config)
        self.assertEqual(paused["used_seconds"], 9000)
        with patch("colombo.shared.runtime_budget.time.time", return_value=20000):
            resumed = outer_budget.start(self.root, self.config)
        self.assertEqual(resumed["elapsed_seconds"], 9000)
        self.assertIsNone(resumed["remaining_seconds"])
        self.assertEqual(resumed["status"], "active")

    def test_cells_and_tools_ignore_stale_finite_ancestor_environment(self):
        ancestor = self.root / "old"
        old = start_budget(ancestor, self.legacy_policy(1))
        current = ancestor / "new-current"
        new = start_budget(current, self.config)
        cell = current / "tasks" / "T0001" / "cell"
        cell.mkdir(parents=True)
        (cell / "run.json").write_text(json.dumps({"budget_policy": "wave_dispatch"}), encoding="utf-8")
        os.environ["COLOMBO_BUDGET_FILE"] = old["budget_file"]
        context = get_budget_context(cell)
        self.assertEqual(context["budget_file"], new["budget_file"])
        self.assertIsNone(inherited_deadline(cell))
        self.assertEqual(budget_environment(cell)["COLOMBO_BUDGET_FILE"], new["budget_file"])
        selected = self.config["cell"]["settings"]
        self.assertIsNone(challenge._deadline(cell, selected))
        self.assertTrue(math.isinf(experiment._window(selected["experiment"], handoff.caller_deadline(cell))))
        process = handoff.begin_process(cell, "a" * 32, "prover", None, selected,
                                        shared_budget=context)
        self.assertIsNone(process["soft_deadline"])
        self.assertIsNone(process["total_deadline"])

    def test_standalone_cell_does_not_adopt_old_environment_deadline(self):
        old = start_budget(self.root / "old", self.legacy_policy(1))
        os.environ["COLOMBO_BUDGET_FILE"] = old["budget_file"]
        cell = self.root / "standalone"
        cell.mkdir()
        (cell / "run.json").write_text('{"budget_policy":"wave_dispatch"}', encoding="utf-8")
        self.assertIsNone(get_budget_context(cell))
        state = start_budget(cell, self.config)
        self.assertTrue(state["accounting_only"])
        self.assertEqual(get_budget_context(cell)["budget_file"], state["budget_file"])

    def test_old_global_caps_are_rejected_not_reinterpreted(self):
        document = tomllib.loads((PROJECT_ROOT / "config.toml").read_text(encoding="utf-8-sig"))
        for key in ("max_dispatches", "max_model_calls", "max_assessment_versions"):
            value = deepcopy(document)
            value["limits"][key] = 24
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "historical"):
                resolve_document(value)
        value = deepcopy(document)
        value["budget"] = {"research": {"total_active_seconds": 3600}}
        with self.assertRaises(ValueError):
            resolve_document(value)
        with self.assertRaisesRegex(ValueError, "workflow version 3"):
            require_current_workflow({"workflow": {"version": 2}})


if __name__ == "__main__":
    unittest.main()
