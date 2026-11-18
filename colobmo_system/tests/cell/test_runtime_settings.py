"""Task configuration changes are isolated, logged and honest about activation."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from colombo.cell.settings import configure
from colombo.cell.settings import pin_task_settings
import colombo.cell.settings as settings


class RuntimeSettingsTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ)
        self.env.start()
        self.addCleanup(self.env.stop)
        for key in ("CELL_RUN_DIR", "CELL_ROLE", "CELL_SEARCH_ENABLED", "CELL_SETTINGS_FILE", "CELL_REQUESTED_MODEL",
                    "CELL_MODEL", "CELL_REASONING_EFFORT", "CELL_AGENT_TIMEOUT", "CELL_THEOREM_SEARCH_URL"):
            os.environ.pop(key, None)
        temp = tempfile.TemporaryDirectory(prefix=".runtime-settings-test-", dir=ROOT)
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.base = settings.get_settings()
        self.standard = settings.load_defaults(profile="standard")[0]
        self.user_defaults = settings.CONFIG_PATH.read_bytes()

    def task(self, name="task", role="prover", search=None, value=None):
        root = self.root / name
        root.mkdir()
        value = deepcopy(self.base if value is None else value)
        document = {**settings.run_fields(value), "settings": value, "role": role,
                    "task_depth": 1 if role in {"worker", "subcell"} else 0}
        if search is not None:
            document["agent_options"] = {"search_enabled": search}
        (root / "run.json").write_text(json.dumps(document), encoding="utf-8")
        return root

    def document(self, root):
        return json.loads((root / "run.json").read_text(encoding="utf-8"))

    def test_role_defaults_and_explicit_overrides_are_separate(self):
        parent = self.task(search=True)
        child = self.task("child", "subcell")
        self.assertTrue(settings.get_search_enabled("prover", self.base, parent))
        self.assertTrue(settings.get_search_enabled("subcell", self.base, parent))
        self.assertTrue(settings.get_search_enabled("subcell", self.base, child))
        self.assertTrue(settings.get_search_enabled("verifier", self.base, child))
        self.assertFalse(settings.get_search_enabled("audit", self.base, parent))
        result = configure(child, "subcell", search_enabled=False, reason="This local lemma needs no external search")
        self.assertFalse(result["lookup_enabled"])
        self.assertFalse(settings.get_search_enabled("worker", self.base, child))
        self.assertTrue(self.base["network"]["subcell_search_enabled"])

    def test_update_syncs_aliases_history_and_never_changes_defaults_or_sibling(self):
        task = self.task("task", "subcell", search=False)
        sibling = self.task("sibling", "subcell")
        sibling_bytes = (sibling / "run.json").read_bytes()
        result = configure(task, "subcell", {
            "model": {"name": "test-new-model", "reasoning_effort": "high"},
        }, True, "Need longer exploration and sources")
        document = self.document(task)
        self.assertEqual(document["model"], "test-new-model")
        self.assertEqual(document["task_timeout"], self.base["agents"]["subcell_timeout_seconds"])
        self.assertEqual(settings.get_settings(task)["model"]["reasoning_effort"], "high")
        self.assertEqual(document["settings_revision"], 1)
        self.assertEqual(document["settings_history"][0]["reason"], "Need longer exploration and sources")
        self.assertEqual(len(result["changes"]), 3)
        self.assertEqual((sibling / "run.json").read_bytes(), sibling_bytes)
        self.assertEqual(settings.CONFIG_PATH.read_bytes(), self.user_defaults)

    def test_get_settings_uses_live_task_instead_of_immutable_launch_snapshot(self):
        task = self.task()
        launch = self.root / "launch.json"
        launch.write_text(json.dumps(self.base), encoding="utf-8")
        with patch.dict(os.environ, {"CELL_RUN_DIR": str(task), "CELL_SETTINGS_FILE": str(launch)}):
            configure(task, "prover", {"network": {"theorem_search_url": "https://example.invalid/search"}}, reason="Broaden source search")
            self.assertEqual(settings.get_settings()["network"]["theorem_search_url"], "https://example.invalid/search")
            self.assertEqual(json.loads(launch.read_text())["network"]["theorem_search_url"], "")

    def test_report_distinguishes_live_lookup_from_native_search_and_startup_settings(self):
        task = self.task(role="subcell", search=False)
        launch = self.root / "launch.json"
        launch.write_text(json.dumps(self.base), encoding="utf-8")
        with patch.dict(os.environ, {"CELL_RUN_DIR": str(task), "CELL_SETTINGS_FILE": str(launch),
                                     "CELL_SEARCH_ENABLED": "0"}):
            result = configure(task, "subcell", {
                "model": {"reasoning_effort": "high"},
            }, True, "Search now and use deeper reasoning next turn")
            self.assertTrue(result["lookup_enabled"])
            self.assertFalse(result["native_search_enabled"])
            pending = {item["parameter"] for item in result["pending_next_start"]}
            self.assertEqual(pending, {"model.reasoning_effort", "native_search_enabled"})
            self.assertEqual(result["effect_timing"]["search_enabled"]["lookup"], "next_tool_call")
            again = configure(task, "subcell")
            self.assertEqual(again["pending_next_start"], result["pending_next_start"])

    def test_invalid_requests_leave_task_unchanged(self):
        task = self.task()
        before = (task / "run.json").read_bytes()
        for kwargs in (
            {"search_enabled": "true", "reason": "Invalid bool"},
            {"search_enabled": False},
            {"settings_overrides": {"network": {"read_timeout_seconds": 0}}, "reason": "Invalid number"},
            {"settings_overrides": {"parallel": {"max_worker": 3}}, "reason": "Misspelling"},
            {"settings_overrides": {"runtime": {"stop_hook_timeout_seconds": 600}}, "reason": "Removed setting"},
            {"settings_overrides": {"retrieval": {"search_results": 99}}, "reason": "Invalid coupled values"},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                configure(task, "prover", **kwargs)
            self.assertEqual((task / "run.json").read_bytes(), before)
        with self.assertRaises(ValueError):
            configure(task, "audit", search_enabled=True, reason="Wrong role")

    def test_new_review_and_handoff_settings_migrate_once_and_activate_next_start(self):
        old = deepcopy(self.base)
        old.pop("handoff")
        old["agents"].pop("report_check_timeout_seconds")
        old["agents"].pop("report_check_max_attempts")
        old["agents"]["prover_timeout_seconds"] = 751
        migrated = settings.migrate_settings(old)
        self.assertEqual(migrated["handoff"], self.base["handoff"])
        self.assertEqual(migrated["agents"]["prover_timeout_seconds"], 751)
        self.assertEqual(migrated["agents"]["report_check_max_attempts"],
                         self.standard["agents"]["report_check_max_attempts"])
        task = self.task()
        launch = self.root / "launch.json"
        launch.write_text(json.dumps(self.base), encoding="utf-8")
        with patch.dict(os.environ, {"CELL_RUN_DIR": str(task), "CELL_SETTINGS_FILE": str(launch)}):
            changed = configure(task, "prover", {"handoff": {"recovery_reasoning_effort": "medium"}},
                                reason="Use a different recovery reasoning effort next time")
            self.assertIn("handoff.recovery_reasoning_effort", {x["parameter"] for x in changed["pending_next_start"]})
            self.assertEqual(changed["changes"][0]["effective"], "next_agent_start")
        for patch_values in ({"handoff": {"recovery_seconds": -1}},
                             {"handoff": {"reserve_seconds": 0.5}},
                             {"agents": {"report_check_max_attempts": 0}}):
            with self.assertRaises(ValueError):
                settings.merge_settings(self.base, patch_values)
        with self.assertRaisesRegex(ValueError, "CLI overrides"):
            settings.apply_overrides(self.base, timeout=17)
        self.assertEqual(settings.CONFIG_PATH.read_bytes(), self.user_defaults)

    def test_resolved_default_model_does_not_look_like_a_pending_change(self):
        inherited = deepcopy(self.base)
        inherited["model"]["name"] = ""
        task = self.task(value=inherited)
        launch_value = deepcopy(self.base)
        launch_value["model"]["name"] = "resolved-user-default"
        launch = self.root / "launch.json"
        launch.write_text(json.dumps(launch_value), encoding="utf-8")
        with patch.dict(os.environ, {"CELL_RUN_DIR": str(task), "CELL_SETTINGS_FILE": str(launch),
                                     "CELL_REQUESTED_MODEL": ""}):
            self.assertEqual(configure(task, "prover")["pending_next_start"], [])
        explicit = self.task("explicit", value=launch_value)
        with patch.dict(os.environ, {"CELL_RUN_DIR": str(explicit), "CELL_SETTINGS_FILE": str(launch),
                                     "CELL_REQUESTED_MODEL": "resolved-user-default"}):
            result = configure(explicit, "prover", {"model": {"name": ""}}, reason="Use the user default next time")
            pending = result["pending_next_start"]
            self.assertEqual(pending, [{"parameter": "model.name", "running": "resolved-user-default", "next": ""}])

    def test_experiment_migration_and_task_override_do_not_change_user_defaults(self):
        old = deepcopy(self.base)
        old.pop("experiment")
        self.assertEqual(settings.migrate_settings(old)["experiment"], self.standard["experiment"])
        with self.assertRaises(ValueError):
            settings.validate_settings(old)
        task = self.task(role="subcell", search=False)
        changed = configure(task, "subcell", {"experiment": {"enabled": False}},
                            reason="Conserve computation until the obstruction is clearer")
        timing = {item["parameter"]: item["effective"] for item in changed["changes"]}
        self.assertEqual(timing["experiment.enabled"], "next_experiment_call")
        with self.assertRaisesRegex(ValueError, "outer config"):
            configure(task, "subcell", {"experiment": {"timeout_seconds": 61}}, reason="Forbidden override")
        self.assertFalse(settings.get_settings(task)["experiment"]["enabled"])
        self.assertFalse(changed["lookup_enabled"])
        self.assertEqual(settings.CONFIG_PATH.read_bytes(), self.user_defaults)
        for invalid in ({"max_runs": True}, {"max_runs": 0}, {"memory_limit": "2g"},
                        {"timeout_seconds": 15}, {"model": " "},
                        {"reasoning_effort": " "}, {"reasoning_effort": True},
                        {"artifact_max_bytes": self.base["experiment"]["max_total_artifact_bytes"] + 1}):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                settings.merge_settings(self.base, {"experiment": invalid})

    def test_experiment_effort_override_applies_only_to_next_experiment(self):
        task = self.task()
        result = configure(task, "prover", {"experiment": {"reasoning_effort": "high"}},
                           reason="Use a different effort for future hosted experiments")
        self.assertEqual(result["changes"], [{"parameter": "experiment.reasoning_effort",
            "before": "max", "after": "high", "effective": "next_experiment_run"}])
        selected = settings.get_settings(task)
        self.assertEqual(selected["experiment"]["reasoning_effort"], "high")
        self.assertEqual(selected["model"]["reasoning_effort"], "ultra")
        self.assertEqual(settings.CONFIG_PATH.read_bytes(), self.user_defaults)

    def test_challenge_defaults_migrate_and_live_limits_preserve_user_table(self):
        old = deepcopy(self.base)
        old.pop("challenge")
        self.assertEqual(settings.migrate_settings(old)["challenge"], self.standard["challenge"])
        with self.assertRaises(ValueError):
            settings.validate_settings(old)
        task = self.task()
        before = (task / "run.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "outer config"):
            configure(task, "prover", {"challenge": {"max_rounds": 3, "timeout_seconds": 91}},
                      reason="Cannot change a root-owned budget")
        self.assertEqual((task / "run.json").read_bytes(), before)
        self.assertEqual(settings.CONFIG_PATH.read_bytes(), self.user_defaults)
        for invalid in ({"max_rounds": 0}, {"max_check_attempts": True}, {"check_timeout_seconds": 1.5}):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                settings.merge_settings(self.base, {"challenge": invalid})

    def test_legacy_snapshots_migrate_names_and_keep_recorded_values(self):
        old = deepcopy(self.base)
        old["agents"]["worker_timeout_seconds"] = old["agents"].pop("subcell_timeout_seconds")
        old["parallel"]["max_workers"] = old["parallel"].pop("max_subcells")
        del old["network"]["prover_search_enabled"]
        del old["network"]["subcell_search_enabled"]
        task = self.task(role="worker")
        document = self.document(task)
        document["settings"] = old
        document["task_timeout"] = 91
        (task / "run.json").write_text(json.dumps(document), encoding="utf-8")
        self.assertTrue(settings.needs_run_migration(document))
        loaded = settings.get_settings(task)
        self.assertEqual(loaded["agents"]["subcell_timeout_seconds"], self.base["agents"]["subcell_timeout_seconds"])
        self.assertNotIn("worker_timeout_seconds", loaded["agents"])
        self.assertFalse(loaded["network"]["subcell_search_enabled"])
        configure(task, "worker", search_enabled=True, reason="Normalize restored task")
        self.assertEqual(self.document(task)["role"], "subcell")
        self.assertNotIn("max_workers", self.document(task)["settings"]["parallel"])
        self.assertFalse(settings.needs_run_migration(self.document(task)))

    def test_concurrent_updates_merge_and_keep_each_history_entry(self):
        task = self.task()
        patches = [
            {"model": {"reasoning_effort": "high"}},
            {"retrieval": {"include_context": False}},
            {"network": {"theorem_search_url": "https://example.invalid/search"}},
            {"experiment": {"enabled": False}},
            {"handoff": {"recovery_reasoning_effort": "medium"}},
        ]
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = [pool.submit(configure, task, "prover", patch, None, f"Update {index}")
                       for index, patch in enumerate(patches)]
            for future in futures:
                future.result()
        loaded = settings.get_settings(task)
        for change in patches:
            for section, values in change.items():
                for key, value in values.items():
                    self.assertEqual(loaded[section][key], value)
        document = self.document(task)
        self.assertEqual(document["settings_revision"], 5)
        self.assertEqual(len(document["settings_history"]), 5)
        # No caller writes an initializer byte before acquiring the lock.
        self.assertEqual((task / ".settings.lock").stat().st_size, 0)

    def test_removed_hook_setting_migrates_saved_task_and_launch_snapshot_once(self):
        task = self.task(search=False)
        document = self.document(task)
        document["settings"]["runtime"]["stop_hook_timeout_seconds"] = 987
        (task / "run.json").write_text(json.dumps(document), encoding="utf-8")
        launch = self.root / "legacy-launch.json"
        launch.write_text(json.dumps(document["settings"]), encoding="utf-8")
        launch_bytes = launch.read_bytes()
        self.assertTrue(settings.needs_run_migration(document))
        with patch.dict(os.environ, {"CELL_SETTINGS_FILE": str(launch)}):
            self.assertEqual(settings.get_settings(), self.base)
            inspected = configure(task, "prover")
            self.assertEqual(inspected["desired_settings"], self.base)
            self.assertEqual(inspected["pending_next_start"], [])
            pinned = pin_task_settings(task, "prover")
            self.assertEqual(pinned, self.base)
        saved = (task / "run.json").read_bytes()
        migrated = self.document(task)
        self.assertNotIn("stop_hook_timeout_seconds", migrated["settings"]["runtime"])
        self.assertFalse(migrated["agent_options"]["search_enabled"])
        self.assertTrue(migrated["settings_history"][0]["migration"])
        self.assertEqual(migrated["settings_revision"], 1)
        self.assertFalse(settings.needs_run_migration(migrated))
        self.assertEqual(pin_task_settings(task, "prover"), pinned)
        self.assertEqual((task / "run.json").read_bytes(), saved)
        self.assertEqual(launch.read_bytes(), launch_bytes)
        self.assertEqual(settings.CONFIG_PATH.read_bytes(), self.user_defaults)

    def test_removed_hook_setting_is_rejected_in_current_user_defaults(self):
        defaults = self.root / "obsolete-defaults.toml"
        defaults.write_text(self.user_defaults.decode("utf-8-sig").replace(
            "[cell.settings.runtime]", "[cell.settings.runtime]\nstop_hook_timeout_seconds = 600"), encoding="utf-8")
        with patch.object(settings, "CONFIG_PATH", defaults):
            with self.assertRaisesRegex(ValueError, r"Invalid config keys in \[runtime\]"):
                settings.get_settings()

    def test_auditor_own_snapshot_is_not_replaced_by_parent_task_state(self):
        parent = self.task()
        audit = parent / "audits" / "one"
        audit.mkdir(parents=True)
        frozen = deepcopy(self.base)
        frozen["model"]["reasoning_effort"] = "high"
        launch = self.root / "audit-launch.json"
        launch.write_text(json.dumps(frozen), encoding="utf-8")
        with patch.dict(os.environ, {"CELL_RUN_DIR": str(audit), "CELL_ROLE": "audit",
                                     "CELL_SETTINGS_FILE": str(launch)}):
            self.assertEqual(settings.get_settings(), frozen)

    def test_pin_legacy_task_once_and_root_changes_do_not_change_its_defaults(self):
        defaults = self.root / "defaults.toml"
        defaults.write_bytes(self.user_defaults)
        task = self.task(role="subcell")
        document = self.document(task)
        del document["role"]
        del document["settings"]["network"]["prover_search_enabled"]
        del document["settings"]["network"]["subcell_search_enabled"]
        (task / "run.json").write_text(json.dumps(document), encoding="utf-8")
        with patch.object(settings, "CONFIG_PATH", defaults):
            pinned = pin_task_settings(task, "subcell")
            self.assertFalse(pinned["network"]["subcell_search_enabled"])
            saved = (task / "run.json").read_bytes()
            self.assertEqual(self.document(task)["role"], "subcell")
            self.assertFalse(self.document(task)["agent_options"]["search_enabled"])
            self.assertTrue(self.document(task)["settings_history"][0]["migration"])
            defaults.write_text(defaults.read_text(encoding="utf-8-sig").replace(
                "subcell_search_enabled = false", "subcell_search_enabled = true"), encoding="utf-8")
            self.assertTrue(settings.get_settings()["network"]["subcell_search_enabled"])
            self.assertEqual(pin_task_settings(task, "subcell"), pinned)
            self.assertEqual((task / "run.json").read_bytes(), saved)

    def test_inspection_is_read_only_and_merge_rejects_unknown_keys(self):
        task = self.task()
        before = (task / "run.json").read_bytes()
        self.assertTrue(configure(task, "prover")["search_enabled"])
        self.assertEqual((task / "run.json").read_bytes(), before)
        self.assertFalse((task / ".settings.lock").exists())
        with self.assertRaises(ValueError):
            settings.merge_settings(self.base, {"network": {"enable_everything": True}})
        for source_root in (settings.CONFIG_PATH.parent, ROOT):
            with self.subTest(source_root=source_root), self.assertRaises(ValueError), \
                    patch("colombo.cell.settings._settings_lock",
                          side_effect=AssertionError("Source directory must be rejected before any write")):
                configure(source_root, "prover", search_enabled=False, reason="Forbidden destination")


if __name__ == "__main__":
    unittest.main()
