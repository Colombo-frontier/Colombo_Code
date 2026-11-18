"""Verify per-subcell launch choices, isolation, and legacy task metadata."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import Mock
from unittest.mock import patch

from colombo.cell.record_store import Store
from colombo.cell.subcell_worker import run_subcell
from colombo.cell.subcell_dispatch import TaskError
from colombo.cell.subcell_dispatch import Tasks
from colombo.cell.settings import CONFIG_PATH
from colombo.cell.settings import get_search_enabled
from colombo.cell.settings import get_settings
from colombo.cell.settings import run_fields
import colombo.cell.model_calls as processes


class SubcellTaskTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for name in ("CELL_SETTINGS_FILE", "CELL_RUN_DIR", "CELL_MODEL", "CELL_ROLE",
                     "CELL_REASONING_EFFORT", "CELL_AGENT_TIMEOUT", "CELL_THEOREM_SEARCH_URL"):
            os.environ.pop(name, None)
        temporary = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2])
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.settings = get_settings()
        self.settings["parallel"]["max_depth"] = 2
        self.settings["network"]["subcell_search_enabled"] = False
        self.root_config = CONFIG_PATH.read_bytes()
        parent = dict(run_fields(self.settings), settings=self.settings, task_depth=0,
                      role="prover", agent_options={"search_enabled": True})
        (self.root / "run.json").write_text(json.dumps(parent), encoding="utf-8")
        self.parent_bytes = (self.root / "run.json").read_bytes()
        self.store = Store(self.root / "memory")
        self.target = self.store.archive("claims", {"statement": "For each integer n, n+n is even."})
        self.ref = {key: self.target[key] for key in ("kind", "id", "revision")}
        self.tasks = Tasks(self.root)
        process = patch("colombo.cell.subcell_dispatch.subprocess.Popen")
        self.launch = process.start()
        self.launch.return_value.pid = 12345
        self.addCleanup(process.stop)

    @staticmethod
    def config(task):
        return json.loads((Path(task["workspace"]) / "run.json").read_text(encoding="utf-8"))

    def test_role_default_not_parent_current_search_and_explicit_override_isolated(self):
        plain = self.tasks.spawn_task(self.ref, "Use the supplied material")
        online = self.tasks.spawn_task(self.ref, "Check an external lemma", search_enabled=True)
        self.assertFalse(self.config(plain)["agent_options"]["search_enabled"])
        self.assertTrue(self.config(online)["agent_options"]["search_enabled"])
        self.assertEqual(self.config(plain)["role"], "subcell")
        self.assertEqual(self.config(plain)["settings"], self.settings)
        self.assertEqual((self.root / "run.json").read_bytes(), self.parent_bytes)
        self.assertEqual(CONFIG_PATH.read_bytes(), self.root_config)
        self.assertEqual(Path(self.launch.call_args.args[0][1]).name, "subcell_worker.py")
        grandchild = Tasks(Path(online["workspace"])).spawn_task(self.ref, "A follow-up derivation")
        self.assertFalse(self.config(grandchild)["agent_options"]["search_enabled"])

    def test_launch_settings_patch_only_changes_that_child_and_is_persisted(self):
        patch_values = {"model": {"reasoning_effort": "high"}}
        before = copy.deepcopy(patch_values)
        task = self.tasks.spawn_task(self.ref, "Try an elementary proof", settings_overrides=patch_values)
        sibling = self.tasks.spawn_task(self.ref, "Try induction")
        saved = self.config(task)
        self.assertEqual(saved["settings"]["agents"]["subcell_timeout_seconds"], "unlimited")
        self.assertEqual(saved["task_timeout"], "unlimited")
        self.assertEqual(saved["settings"]["model"]["reasoning_effort"], "high")
        self.assertEqual(task["settings_overrides"], before)
        self.assertEqual(patch_values, before)
        self.assertEqual(self.config(sibling)["settings"], self.settings)
        self.assertEqual((self.root / "run.json").read_bytes(), self.parent_bytes)
        self.assertEqual(CONFIG_PATH.read_bytes(), self.root_config)

    def test_invalid_override_rejected_before_launch_or_workspace_creation(self):
        for extra in ({"search_enabled": 1}, {"search_enabled": "true"},
                      {"settings_overrides": {"agents": {"subcell_timeout_seconds": 0}}},
                      {"settings_overrides": {"bogus": {"enabled": True}}}):
            with self.subTest(extra=extra), self.assertRaises((TaskError, ValueError)):
                self.tasks.spawn_task(self.ref, "Rejected configuration", **extra)
        self.launch.assert_not_called()
        self.assertFalse(self.tasks.tasks_dir.exists())

    def test_local_parent_material_remains_readable_without_search(self):
        task = self.tasks.spawn_task(self.ref, "Read the supplied statement")
        work = Path(task["workspace"])
        self.assertFalse(get_search_enabled("subcell", get_settings(work), work))
        records = Store(work / "memory").retrieve(record_id=self.ref["id"])["records"]
        self.assertEqual(records[0]["payload"], self.target["payload"])
        self.assertTrue(records[0]["read_only"])
        with self.assertRaisesRegex(ValueError, "read-only"):
            Store(work / "memory").archive("claims", {"statement": "Changed"}, record_id=self.ref["id"])

    def test_subcell_runner_uses_persisted_configuration_and_new_role(self):
        task = self.tasks.spawn_task(self.ref, "Look for a proof", search_enabled=True,
                                     settings_overrides={"model": {"reasoning_effort": "high"}})
        work = Path(task["workspace"])
        calls = []

        def runner(prompt, work_dir, output_file, **kwargs):
            calls.append(kwargs)
            self.assertEqual(work_dir, work)
            self.assertEqual(kwargs["role"], "subcell")
            self.assertEqual(kwargs["extra_env"]["CELL_ROLE"], "subcell")
            self.assertNotIn("search", kwargs)
            self.assertTrue(get_search_enabled(kwargs["role"], kwargs["settings"], work_dir))
            output_file.write_text("The supplied claim is proved by factoring out 2.", encoding="utf-8")
            return {"returncode": 0}

        result = run_subcell(work.parent, agent_runner=runner)
        self.assertEqual(result["status"], "completed")
        self.assertNotIn("mathematical_outcome", result)
        self.assertEqual(calls[0]["timeout"], "unlimited")
        self.assertEqual(calls[0]["settings"]["model"]["reasoning_effort"], "high")
        status = self.tasks.task_status(task["task_id"])
        self.assertIn("subcell_pid", status)
        self.assertNotIn("worker_pid", status)
        found = self.tasks.collect_task(task["task_id"], include_result=True)
        self.assertEqual(Path(found["artifacts"]["subcell_log"]).name, "subcell.log")
        self.assertIn("factoring", found["result_text"])

    def test_collection_summary_full_retry_and_appended_records(self):
        task = self.tasks.spawn_task(self.ref, "Try a proof")
        child = Store(Path(task["workspace"]) / "memory")
        claim = child.archive("claims", {"statement": "A child lemma"})
        argument = child.archive("arguments", {"status": "partial", "proof": "evidence " * 200,
                                                "dependencies": [{key: claim[key] for key in
                                                                  ("kind", "id", "revision")}]})
        first = self.tasks.collect_task(task["task_id"], limit=2)
        self.assertEqual(first["count"], 2)
        self.assertNotIn("records", first)
        self.assertNotIn("evidence evidence", json.dumps(first))
        self.assertNotIn("events", first["totals"])
        appended = child.archive("claims", {"statement": "Arrived after the summary"})
        full = self.tasks.collect_task(task["task_id"], detail="full", cursor=first["cursor"], limit=2)
        self.assertEqual(full["records"], [claim, argument])
        self.assertEqual(full["record_refs"], first["record_refs"])
        new = self.tasks.collect_task(task["task_id"], detail="full", cursor=full["next_cursor"])
        self.assertEqual(new["records"], [appended])
        self.assertTrue(new["requires_parent_audit"])
        self.assertFalse((Path(task["workspace"]).parent / "collected.json").exists())

    def test_collection_pages_preserve_all_revisions_and_exact_dependency_reads(self):
        task = self.tasks.spawn_task(self.ref, "Try a proof")
        child = Store(Path(task["workspace"]) / "memory")
        first = child.archive("claims", {"statement": "Original statement"})
        second = child.archive("claims", {"statement": "Original statement", "title": "A clearer title"}, first["id"], 1)
        argument = child.archive("arguments", {"proof": "Uses the original statement",
                                                "dependencies": [{key: first[key] for key in
                                                                  ("kind", "id", "revision")}]})
        cursor, collected = None, []
        for index in range(3):
            page = self.tasks.collect_task(task["task_id"], detail="full", limit=1, cursor=cursor)
            self.assertEqual(page["count"], 1)
            collected.extend(page["records"])
            cursor = page["next_cursor"]
        self.assertEqual(collected, [first, second, argument])
        empty = self.tasks.collect_task(task["task_id"], cursor=cursor)
        self.assertEqual(empty["count"], 0)
        pinned = self.tasks.collect_task(task["task_id"], record_ref=argument["payload"]["dependencies"][0])
        self.assertEqual(pinned["records"], [first])
        bad_ref = {**argument["payload"]["dependencies"][0], "revision": 999}
        with self.assertRaises((TaskError, KeyError)):
            self.tasks.collect_task(task["task_id"], record_ref=bad_ref)
        events = self.tasks.collect_task(task["task_id"], kinds=["events"], detail="full")
        self.assertEqual(events["count"], 3)
        self.assertTrue(all(row["kind"] == "events" for row in events["records"]))

    def test_legacy_collection_bookkeeping_does_not_hide_evidence(self):
        task = self.tasks.spawn_task(self.ref, "Recover an old task")
        work = Path(task["workspace"])
        child = Store(work / "memory")
        record = child.archive("claims", {"statement": "Previously returned evidence"})
        legacy = work.parent / "collected.json"
        legacy.write_text(json.dumps([json.dumps([record["kind"], record["id"],
                                                 record["revision"]])]), encoding="utf-8")
        before = legacy.read_bytes()
        result = self.tasks.collect_task(task["task_id"], detail="full")
        self.assertEqual(result["records"], [record])
        self.assertEqual(legacy.read_bytes(), before)

    def test_collection_cursor_is_task_bound_and_validated(self):
        task = self.tasks.spawn_task(self.ref, "First task")
        sibling = self.tasks.spawn_task(self.ref, "Second task")
        cursor = self.tasks.collect_task(task["task_id"])["cursor"]
        with self.assertRaisesRegex(TaskError, "another task"):
            self.tasks.collect_task(sibling["task_id"], cursor=cursor)
        with self.assertRaisesRegex(TaskError, "collection set"):
            self.tasks.collect_task(task["task_id"], cursor=cursor, kinds=["claims"])
        for position in (-1, True, "0"):
            bad = copy.deepcopy(cursor)
            bad["positions"]["claims"] = position
            with self.subTest(position=position), self.assertRaises(TaskError):
                self.tasks.collect_task(task["task_id"], cursor=bad)
        for options in ({"limit": 0}, {"limit": True}, {"detail": "all"}, {"include_result": 1},
                        {"kinds": []}, {"kinds": ["claims", "claims"]},
                        {"record_ref": {"kind": "claims", "id": "X", "revision": True}},
                        {"record_ref": self.ref, "cursor": cursor}):
            with self.subTest(options=options), self.assertRaises(TaskError):
                self.tasks.collect_task(task["task_id"], **options)

    def test_collection_errors_do_not_consume_unread_rows(self):
        task = self.tasks.spawn_task(self.ref, "Try a proof")
        work = Path(task["workspace"])
        child = Store(work / "memory")
        record = child.archive("claims", {"statement": "Saved evidence"})
        path = work / "memory" / "claims.json"
        saved = path.read_bytes()
        path.write_text("invalid JSON", encoding="utf-8")
        broken = self.tasks.collect_task(task["task_id"])
        self.assertEqual(broken["count"], 0)
        self.assertTrue(broken["warnings"])
        path.write_bytes(saved)
        restored = self.tasks.collect_task(task["task_id"], cursor=broken["next_cursor"], detail="full")
        self.assertEqual(restored["records"], [record])
        path.write_text('{"schema_version": 2, "records": []}', encoding="utf-8")
        with self.assertRaisesRegex(TaskError, "shorter"):
            self.tasks.collect_task(task["task_id"], cursor=restored["next_cursor"])

    def test_result_body_is_opt_in_and_never_duplicated(self):
        task = self.tasks.spawn_task(self.ref, "Try a proof")
        work = Path(task["workspace"])
        body = "Unique complete result with mathematical evidence."
        (work / "task_result.md").write_text(body, encoding="utf-8")
        (work.parent / "result.json").write_text(json.dumps({
            "status": "completed", "mathematical_outcome": "unresolved",
            "agent_result": {"text": body, "session_id": "test-session", "returncode": 0}}), encoding="utf-8")
        summary = self.tasks.collect_task(task["task_id"])
        self.assertNotIn(body, json.dumps(summary))
        self.assertNotIn("result_text", summary)
        self.assertEqual(summary["result"]["status"], "completed")
        full = self.tasks.collect_task(task["task_id"], include_result=True)
        self.assertEqual(json.dumps(full).count(body), 1)
        self.assertEqual(full["result_text"], body)
        self.assertNotIn("text", full["result"]["agent_result"])

    def test_protocol_is_available_in_child_workspace(self):
        task = self.tasks.spawn_task(self.ref, "Use the record protocol")
        source = Path(__file__).resolve().parents[2] / "agents/cell" / "prover" / "protocol.md"
        self.assertEqual((Path(task["workspace"]) / "protocol.md").read_bytes(), source.read_bytes())

    def test_legacy_logs_and_pid_are_read_without_rewriting_history(self):
        task = self.tasks.spawn_task(self.ref, "A task created by an older version")
        directory = Path(task["workspace"]).parent
        (directory / "subcell.log").rename(directory / "worker.log")
        stored = json.loads((directory / "task.json").read_text(encoding="utf-8"))
        stored["worker_pid"] = 23456
        (directory / "task.json").write_text(json.dumps(stored), encoding="utf-8")
        before = (directory / "task.json").read_bytes()
        status = self.tasks.task_status(task["task_id"])
        self.assertEqual(status["subcell_pid"], 23456)
        self.assertNotIn("worker_pid", status)
        found = self.tasks.collect_task(task["task_id"])
        self.assertEqual(Path(found["artifacts"]["subcell_log"]).name, "worker.log")
        self.assertEqual((directory / "task.json").read_bytes(), before)

    def test_subcell_launch_reaches_native_search_configuration(self):
        fake_auth = self.root / "empty-auth"
        fake_auth.mkdir()
        for enabled in (False, True):
            with self.subTest(enabled=enabled):
                task = self.tasks.spawn_task(self.ref, "Inspect startup configuration", search_enabled=enabled)
                work = Path(task["workspace"])
                (work / "task_result.md").write_text("A mocked model result.", encoding="utf-8")
                process = Mock(returncode=0)
                process.poll.return_value = 0
                with patch.object(processes, "ROOT", self.root / "isolated-launch"), \
                        patch.object(processes, "_user_home", return_value=fake_auth), \
                        patch.object(processes, "_user_settings", return_value={}), \
                        patch.object(processes, "find_codex", return_value="unused-model-test.exe"), \
                        patch.dict(os.environ, {"OPENAI_API_KEY": "test-only-not-a-real-key"}), \
                        patch.object(processes.subprocess, "Popen", return_value=process) as launch:
                    result = run_subcell(work.parent)
                self.assertEqual(result["status"], "completed")
                env = launch.call_args.kwargs["env"]
                actual = tomllib.loads((Path(env["CODEX_HOME"]) / "config.toml").read_text(encoding="utf-8"))
                self.assertEqual(actual["web_search"], "live" if enabled else "disabled")
                self.assertEqual(env["CELL_SEARCH_ENABLED"], "1" if enabled else "0")
                self.assertEqual(actual["mcp_servers"]["research"]["env"]["CELL_ROLE"], "subcell")


if __name__ == "__main__":
    unittest.main()
