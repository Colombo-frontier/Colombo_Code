"""Exercise edited settings across CLI, process and real MCP boundaries; no models."""
from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import timedelta
import asyncio
import copy
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import Mock
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import colombo.cell.model_calls as processes
import colombo.cell.controller as run
import colombo.cell.settings as settings


ENV_OVERRIDES = (
    "CELL_SETTINGS_FILE", "CELL_MODEL", "CELL_REASONING_EFFORT",
    "CELL_AGENT_TIMEOUT", "CELL_THEOREM_SEARCH_URL",
)


class ConfigurationIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        for name in ENV_OVERRIDES:
            os.environ.pop(name, None)
        self.temp = tempfile.TemporaryDirectory(prefix=".settings-test-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.problem = self.root / "question.md"
        self.problem.write_text("Prove that 2 is even.", encoding="utf-8")
        self.base = settings.get_settings()

    def variant_file(self, **values):
        source = settings.CONFIG_PATH.read_text(encoding="utf-8-sig")
        # Profiles intentionally repeat a few keys; this helper edits only the
        # user base table so existing precedence tests keep their original scope.
        values = {"profile": "standard", **values}
        base, separator, profiles = source.partition("\n[profiles.")
        for key, value in values.items():
            replacement = json.dumps(value) if isinstance(value, str) else str(value)
            base, count = re.subn(
                rf"(?m)^{re.escape(key)}\s*=\s*[^\n#]+", f"{key} = {replacement}", base,
            )
            self.assertEqual(count, 1, key)
        source = base + separator + profiles
        path = self.root / "edited-config.toml"
        path.write_text(source, encoding="utf-8")
        return path

    def write_snapshot(self, value, name="settings.json"):
        path = self.root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_cli_omissions_use_edited_root_and_new_run_pins_values(self):
        config = self.variant_file(
            prover_max_rounds=5, verifier_max_rounds=6, max_subcells=2, max_depth=2,
        )
        task = self.root / "research"
        with patch.object(settings, "CONFIG_PATH", config), patch.object(run, "solve", return_value=0):
            with patch.object(sys, "argv", ["run.py", str(self.problem), "--run-dir", str(task)]):
                self.assertEqual(run.main(), 0)
            effective = settings.get_settings(task)
            self.assertEqual(effective["agents"]["prover_timeout_seconds"], "unlimited")
            self.assertEqual(effective["agents"]["subcell_timeout_seconds"], "unlimited")
            self.assertEqual(effective["agents"]["verifier_timeout_seconds"], "unlimited")
            self.assertEqual(effective["agents"]["audit_timeout_seconds"], "unlimited")
            self.assertEqual(effective["agents"]["prover_max_rounds"], 5)
            self.assertEqual(effective["agents"]["verifier_max_rounds"], 6)
            self.assertEqual(effective["parallel"]["max_subcells"], 2)
            stored = json.loads((task / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(stored["settings"], effective)
            config.write_text(config.read_text(encoding="utf-8").replace("prover_max_rounds = 5", "prover_max_rounds = 7"), encoding="utf-8")
            self.assertNotIn("budget", settings.load_policy())
            self.assertEqual(settings.get_settings()["agents"]["prover_max_rounds"], 7)
            self.assertEqual(settings.get_settings(task)["agents"]["prover_max_rounds"], 5)
            self.assertEqual(settings.get_settings(task)["agents"]["prover_timeout_seconds"], "unlimited")

    def test_cli_budget_overrides_are_rejected_and_model_override_still_works(self):
        task = self.root / "research"
        with self.assertRaisesRegex(ValueError,"CLI overrides"):
            run.initialize(self.problem, task, model="test-model", timeout=77, max_rounds=2)
        self.assertFalse(task.exists())
        run.initialize(self.problem, task, model="test-model")
        before=(task / "run.json").read_bytes()
        with patch.object(run,"solve",return_value=0):
            with patch.object(sys,"argv",["run.py","--run-dir",str(task),"--resume","--timeout","88"]), self.assertRaises(SystemExit):
                run.main()
            self.assertEqual((task / "run.json").read_bytes(),before)
            with patch.object(sys,"argv",["run.py","--run-dir",str(task),"--resume","--model","replacement-model"]):
                self.assertEqual(run.main(),0)
        changed=settings.get_settings(task)
        self.assertEqual(changed["model"]["name"],"replacement-model")
        self.assertEqual(changed["agents"]["prover_max_rounds"],self.base["agents"]["prover_max_rounds"])

    def test_snapshot_does_not_pick_up_later_environment_overrides(self):
        with patch.dict(os.environ, {
            "CELL_MODEL": "environment-model", "CELL_REASONING_EFFORT": "high",
            "CELL_AGENT_TIMEOUT": "123", "CELL_THEOREM_SEARCH_URL": "https://search.invalid/theorems",
        }):
            selected = settings.get_settings()
        self.assertEqual(selected["model"]["name"], "environment-model")
        self.assertEqual(selected["model"]["reasoning_effort"], "high")
        self.assertEqual(selected["experiment"]["reasoning_effort"], "max")
        self.assertEqual(selected["agents"]["audit_timeout_seconds"], "unlimited")
        self.assertEqual(selected["network"]["theorem_search_url"], "https://search.invalid/theorems")
        snapshot = self.write_snapshot(selected)
        with patch.dict(os.environ, {"CELL_SETTINGS_FILE": str(snapshot), "CELL_REASONING_EFFORT": "low"}):
            self.assertEqual(settings.get_settings(), selected)
            changed = settings.get_settings()
            changed["agents"]["audit_timeout_seconds"] = 1
            self.assertEqual(settings.get_settings(), selected)

    def test_historical_task_snapshot_pins_experiment_effort_before_next_cell_change(self):
        saved = copy.deepcopy(self.base)
        saved["model"]["reasoning_effort"] = "high"
        del saved["experiment"]["reasoning_effort"]
        task = self.root / "historical-task"
        task.mkdir()
        (task / "run.json").write_text(json.dumps({"settings": saved}), encoding="utf-8")
        selected = settings.get_settings(task)
        self.assertEqual(selected["model"]["reasoning_effort"], "high")
        self.assertEqual(selected["experiment"]["reasoning_effort"], "high")
        changed = settings.merge_settings(selected, {"model": {"reasoning_effort": "ultra"}})
        (task / "run.json").write_text(json.dumps({"settings": changed}), encoding="utf-8")
        with patch.dict(os.environ, {"CELL_REASONING_EFFORT": "low"}):
            reread = settings.get_settings(task)
        self.assertEqual(reread["model"]["reasoning_effort"], "ultra")
        self.assertEqual(reread["experiment"]["reasoning_effort"], "high")

    def test_invalid_or_unknown_setting_fails_before_process_launch(self):
        for section, key, bad in (
            ("parallel", "max_subcells", True), ("parallel", "max_depth", -1),
            ("runtime", "process_poll_seconds", float("nan")),
            ("network", "read_timeout_seconds", 0),
        ):
            with self.subTest(section=section, key=key):
                value = copy.deepcopy(self.base)
                value[section][key] = bad
                with self.assertRaises(ValueError):
                    settings.validate_settings(value)
        value = copy.deepcopy(self.base)
        value["agents"]["prover_timout_seconds"] = 900
        with self.assertRaises(ValueError):
            settings.validate_settings(value)
        value = copy.deepcopy(self.base)
        del value["agents"]["prover_timeout_seconds"]
        with self.assertRaises(ValueError):
            settings.validate_settings(value)

    def test_all_role_configs_and_model_process_receive_same_snapshot(self):
        selected = copy.deepcopy(self.base)
        selected["model"].update(name="test-model", reasoning_effort="high")
        selected["runtime"].update(
            mcp_startup_timeout_seconds=41, mcp_tool_timeout_seconds=444,
        )
        fake_project = self.root / "project"
        fake_auth = self.root / "empty-auth"
        fake_auth.mkdir()
        work = self.root / "work"
        work.mkdir()
        with patch.object(processes, "ROOT", fake_project), \
                patch.object(processes, "_user_home", return_value=fake_auth), \
                patch.object(processes, "_user_settings", return_value={}), \
                patch.dict(os.environ, {"OPENAI_API_KEY": "test-only-not-a-real-key"}):
            for role in ("prover", "subcell", "audit", "verifier"):
                with self.subTest(role=role):
                    home = processes._prepare_home(work, role, None, False, {}, settings=selected)
                    cfg = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
                    self.assertEqual(cfg["model"], "test-model")
                    self.assertEqual(cfg["model_reasoning_effort"], "high")
                    self.assertEqual(json.loads((home / "settings.json").read_text(encoding="utf-8")), selected)
                    self.assertEqual(selected["experiment"]["reasoning_effort"], "max")
                    if role != "audit":
                        mcp = cfg["mcp_servers"]["research"]
                        self.assertEqual(mcp["startup_timeout_sec"], 41)
                        self.assertEqual(mcp["tool_timeout_sec"], 444)
                        self.assertEqual(Path(mcp["env"]["CELL_SETTINGS_FILE"]), home / "settings.json")
                        self.assertEqual(mcp["env_vars"], (["OPENAI_API_KEY"] if role in {"prover", "subcell"} else []) + ["SERPER_API_KEY", "JINA_API_KEY"])
                        self.assertNotIn("OPENAI_API_KEY", mcp["env"])
                    self.assertNotIn("test-only-not-a-real-key", (home / "config.toml").read_text())
                    self.assertFalse(cfg["features"]["hooks"])
                    self.assertFalse(cfg["features"]["multi_agent"])
                    self.assertFalse(cfg["features"]["multi_agent_v2"])
                    self.assertEqual(cfg["agents"], {"enabled": False})
                    if os.name == "nt":
                        self.assertTrue(cfg["features"]["prefer_mxc"])
                        self.assertIn("sandbox", cfg["windows"])
                    self.assertFalse((home / "hooks.json").exists())
            output = work / "final.txt"
            output.write_text("A mocked model result.", encoding="utf-8")
            process = Mock(returncode=0)
            process.poll.return_value = 0
            with patch.object(processes, "find_codex", return_value="disabled-test-executable"), \
                    patch.object(processes.subprocess, "Popen", return_value=process) as launch:
                result = processes.run_agent("Test", work, output, role="subcell", settings=selected)
            self.assertEqual(result["returncode"], 0)
            effective_file = Path(launch.call_args.kwargs["env"]["CELL_SETTINGS_FILE"])
            self.assertEqual(json.loads(effective_file.read_text(encoding="utf-8")), selected)

    def test_hard_cell_native_launch_uses_ultra_and_freezes_experiment_max(self):
        fake_project = self.root / "hard-project"
        fake_auth = self.root / "hard-empty-auth"
        fake_auth.mkdir()
        work = self.root / "hard-work"
        work.mkdir()
        with patch.object(processes, "ROOT", fake_project), \
                patch.object(processes, "_user_home", return_value=fake_auth), \
                patch.object(processes, "_user_settings", return_value={"model": "different-default"}), \
                patch.dict(os.environ, {"OPENAI_API_KEY": "test-only-not-a-real-key"}):
            home = processes._prepare_home(work, "prover", None, False, {}, settings=self.base)
        native = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
        frozen = json.loads((home / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual(native["model"], "gpt-6-astra")
        self.assertEqual(native["model_reasoning_effort"], "ultra")
        self.assertEqual(frozen["experiment"]["reasoning_effort"], "max")
        self.assertEqual(frozen, self.base)


class MCPConfigurationIntegrationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        for name in ENV_OVERRIDES:
            os.environ.pop(name, None)
        self.temp = tempfile.TemporaryDirectory(prefix=".mcp-settings-test-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        selected = settings.get_settings()
        selected["retrieval"].update(memory_results=1, verifier_memory_results=2,
                                     max_memory_results=4, verifier_reverse=False)
        self.snapshot = self.root / "settings.json"
        self.snapshot.write_text(json.dumps(selected), encoding="utf-8")

    @asynccontextmanager
    async def server(self, role):
        from mcp import ClientSession
        from mcp import StdioServerParameters
        from mcp.client.stdio import stdio_client
        params = StdioServerParameters(
            command=sys.executable,
            args=["-B", str(ROOT / "src/colombo/cell" / role / "mcp/server.py")], cwd=ROOT,
            env={**os.environ, "CELL_RUN_DIR": str(self.root), "CELL_ROLE": role,
                 "CELL_SETTINGS_FILE": str(self.snapshot), "PYTHONUTF8": "1",
                 "CELL_CODEX_BIN": str(self.root / "model-disabled.exe")},
        )
        with (self.root / f"{role}.log").open("w", encoding="utf-8") as log:
            async with stdio_client(params, errlog=log) as (reader, writer):
                async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=15)) as session:
                    await session.initialize()
                    yield session

    def data(self, response):
        self.assertFalse(response.isError, response.content)
        if response.structuredContent is not None:
            return response.structuredContent
        return json.loads(next(item.text for item in response.content if item.type == "text"))

    async def test_prover_stdio_uses_nondefault_retrieval_count_and_upper_bound(self):
        async with self.server("prover") as server:
            for index in range(3):
                self.data(await server.call_tool("archive", {
                    "kind": "claims", "record_id": f"C{index}", "payload": {"statement": str(index)},
                }))
            found = self.data(await server.call_tool("retrieve", {"kinds": ["claims"]}))
            self.assertEqual(found["returned"], 1)
            self.assertEqual(len(found["records"]), 1)
            rejected = await server.call_tool("retrieve", {"limit": 5})
            self.assertTrue(rejected.isError)

    async def test_verifier_stdio_uses_nondefault_count_and_record_order(self):
        async with self.server("verifier") as server:
            for index in range(3):
                self.data(await server.call_tool("record_check", {
                    "check_id": index + 1, "status": "pass", "reason": f"Checked item {index + 1}",
                    "subject": f"Deduction {index + 1}", "location": f"Proof paragraph {index + 1}",
                }))
            result = self.data(await server.call_tool("read_review", {"detail": "full"}))
            self.assertEqual([item["id"] for item in result["checks"]], [1, 2])
            self.assertTrue(result["truncated"])
            rejected = await server.call_tool("read_review", {"limit": 5})
            self.assertTrue(rejected.isError)

    async def test_prover_exposes_local_challenge_and_recovery(self):
        async with self.server("prover") as server:
            tools = await server.list_tools()
            names = {tool.name for tool in tools.tools}
            self.assertTrue({"challenge_argument", "resume_argument_challenge", "job_status"} <= names)
            invalid = self.data(await server.call_tool("challenge_argument", {
                "record_ref": {"kind": "claims", "id": "missing", "revision": 1},
                "reason": "A claim has no argument certificate to challenge",
            }))
            # Long operations return a receipt immediately. Validation happens
            # in the original worker and is retrieved by polling that same job.
            for _ in range(150):
                if invalid.get("status") != "running":
                    break
                await asyncio.sleep(0.1)
                invalid = self.data(await server.call_tool("job_status", {"job_id": invalid["job_id"]}))
            self.assertEqual(invalid["status"], "error")
            self.assertFalse(invalid["ok"])
            self.assertEqual(invalid["error"]["type"], "KeyError")
            self.assertIn("claims/missing", invalid["error"]["message"])

    async def test_mcp_rejects_budget_changes_and_keeps_model_choices_separate_from_launch(self):
        default_bytes = settings.CONFIG_PATH.read_bytes()
        launch_bytes = self.snapshot.read_bytes()
        long_budgets = ("prover_timeout_seconds", "subcell_timeout_seconds",
                        "verifier_timeout_seconds", "report_check_timeout_seconds")
        async with self.server("prover") as server:
            rejected = await server.call_tool("configure", {
                "settings_overrides": {"agents": {key: "unlimited" for key in long_budgets}},
                "reason": "Attempt to change research budgets through MCP",
            })
            self.assertTrue(rejected.isError)
            self.assertFalse((self.root / "run.json").exists())
            result = self.data(await server.call_tool("configure", {
                "settings_overrides": {"model": {"reasoning_effort": "high"}},
                "reason": "Change the next agent's reasoning effort",
                "detail": "full",
            }))
            for key in long_budgets:
                self.assertEqual(result["desired_settings"]["agents"][key], "unlimited")
                self.assertEqual(result["launch_settings"]["agents"][key],
                                 json.loads(launch_bytes)["agents"][key])
            change = next(item for item in result["changes"] if item["parameter"] == "model.reasoning_effort")
            self.assertEqual(change["effective"], "next_agent_start")
            before_rejection = (self.root / "run.json").read_bytes()
            rejected = await server.call_tool("configure", {
                "settings_overrides": {"agents": {"audit_timeout_seconds": "unlimited"}},
                "reason": "Attempt to change a root-owned audit budget",
            })
            self.assertTrue(rejected.isError)
            self.assertEqual((self.root / "run.json").read_bytes(), before_rejection)
        # A new MCP process reloads task choices, while its original immutable
        # launch snapshot remains separate from those desired next-start values.
        async with self.server("prover") as server:
            reread = self.data(await server.call_tool("configure", {"detail": "full"}))
            self.assertEqual(reread["desired_settings"]["agents"]["prover_timeout_seconds"], "unlimited")
            self.assertEqual(reread["desired_settings"]["model"]["reasoning_effort"], "high")
            self.assertEqual(reread["launch_settings"]["model"]["reasoning_effort"],
                             json.loads(launch_bytes)["model"]["reasoning_effort"])
        self.assertEqual(settings.CONFIG_PATH.read_bytes(), default_bytes)
        self.assertEqual(self.snapshot.read_bytes(), launch_bytes)


if __name__ == "__main__":
    unittest.main()
