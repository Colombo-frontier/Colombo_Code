"""Search defaults and live task overrides across process and MCP boundaries."""
from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import timedelta
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import tomllib
import unittest
from unittest.mock import Mock
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import colombo.cell.model_calls as processes
import colombo.cell.controller as run
import colombo.cell.settings as settings
import colombo.cell.verifier.proof_review as review
from colombo.cell.settings import configure

lookup_module = importlib.import_module("colombo.shared.literature_access")
ENV_KEYS = ("CELL_RUN_DIR", "CELL_ROLE", "CELL_SEARCH_ENABLED", "CELL_REQUESTED_MODEL", "CELL_SETTINGS_FILE",
            "CELL_MODEL", "CELL_REASONING_EFFORT", "CELL_AGENT_TIMEOUT", "CELL_THEOREM_SEARCH_URL")


class SearchRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ)
        self.env.start()
        self.addCleanup(self.env.stop)
        for name in ENV_KEYS:
            os.environ.pop(name, None)
        self.temp = tempfile.TemporaryDirectory(prefix=".search-test-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = settings.get_settings()
        self.base["network"].update(search_provider="arxiv", reader_provider="direct")

    def write_run(self, path, role, search):
        path.mkdir(parents=True, exist_ok=True)
        (path / "run.json").write_text(json.dumps({
            "role": role, "settings": self.base, **settings.run_fields(self.base),
            "agent_options": {"search_enabled": search},
        }), encoding="utf-8")

    def test_role_defaults_generate_profile_specific_subcell_search(self):
        auth = self.root / "auth"
        auth.mkdir()
        work = self.root / "work"
        work.mkdir()
        with patch.object(processes, "ROOT", self.root), \
                patch.object(processes, "_user_home", return_value=auth), \
                patch.object(processes, "_user_settings", return_value={}), \
                patch.dict(os.environ, {"OPENAI_API_KEY": "test-only"}):
            for profile, child_search in (("standard", "disabled"), ("hard", "live")):
                selected, _ = settings.load_defaults(profile=profile)
                for role, expected in (("prover", "live"), ("subcell", child_search),
                                       ("worker", child_search), ("verifier", "live"), ("audit", "disabled")):
                    with self.subTest(profile=profile, role=role):
                        home = processes._prepare_home(work, role, None, None, {}, settings=selected)
                        cfg = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
                        self.assertEqual(cfg["web_search"], expected)
                        if role != "audit":
                            self.assertEqual(cfg["mcp_servers"]["research"]["env"]["CELL_SEARCH_ENABLED"],
                                             "1" if expected == "live" else "0")

    def test_disabled_lookup_never_reaches_search_or_http(self):
        work = self.root / "child"
        self.write_run(work, "subcell", False)
        with patch.dict(os.environ, {"CELL_RUN_DIR": str(work), "CELL_ROLE": "subcell"}), \
                patch.object(lookup_module, "_arxiv_search") as arxiv, \
                patch.object(lookup_module.requests, "get") as http:
            for kwargs in ({"query": "convexity"}, {"url": "https://example.invalid/paper"}):
                result = lookup_module.lookup(**kwargs)
                self.assertFalse(result["ok"])
                self.assertEqual(result["error"]["kind"], "search_disabled")
            arxiv.assert_not_called()
            http.assert_not_called()
            with self.assertRaises(lookup_module.LookupError):
                lookup_module._request("https://example.invalid/paper")
            http.assert_not_called()

    def test_provider_environment_is_forwarded_by_name_without_serializing_keys(self):
        auth = self.root / "auth"
        auth.mkdir()
        work = self.root / "work"
        work.mkdir()
        secrets = {"SERPER_API_KEY": "fake-private-serper-key", "JINA_API_KEY": "fake-private-jina-key"}
        with patch.object(processes, "ROOT", self.root), \
                patch.object(processes, "_user_home", return_value=auth), \
                patch.object(processes, "_user_settings", return_value={}), \
                patch.dict(os.environ, {"OPENAI_API_KEY": "test-only", **secrets}):
            for role in ("prover", "subcell", "verifier"):
                with self.subTest(role=role):
                    home = processes._prepare_home(work, role, None, None, {}, settings=self.base)
                    text = (home / "config.toml").read_text(encoding="utf-8")
                    config = tomllib.loads(text)
                    mcp = config["mcp_servers"]["research"]
                    self.assertTrue(set(secrets) <= set(mcp["env_vars"]))
                    self.assertFalse(set(secrets) & set(mcp["env"]))
                    snapshot = (home / "settings.json").read_text(encoding="utf-8")
                    for secret in secrets.values():
                        self.assertNotIn(secret, text)
                        self.assertNotIn(secret, snapshot)
    def test_review_search_uses_nearest_task_without_overriding_independent_subcell(self):
        parent = self.root / "offline"
        self.write_run(parent, "prover", False)
        primary = parent / "reviews/r0001/workspace"
        checker = parent / "reviews/r0001/checks/p0001/workspace"
        for work in (parent, primary, checker):
            self.assertFalse(settings.get_search_enabled("verifier", self.base, work))
        child = parent / "tasks/independent"
        self.write_run(child, "subcell", True)
        self.assertTrue(settings.get_search_enabled("subcell", self.base, child))
        self.assertTrue(settings.get_search_enabled("verifier", self.base, child / "reviews/r0001/workspace"))
        self.assertFalse(settings.get_search_enabled("audit", self.base, child / "audits/a1"))
        with patch.dict(os.environ, {"CELL_RUN_DIR": str(checker)}):
            self.assertFalse(settings.get_search_enabled("verifier", self.base))

    def test_offline_launch_persists_disabled_search_for_prover_both_reviews_and_audit(self):
        problem = self.root / "problem.md"
        problem.write_text("Prove 2 is even.", encoding="utf-8")
        task = self.root / "offline"
        run.initialize(problem, task, search_enabled=False)
        selected = settings.get_settings(task)
        original = (task / "run.json").read_bytes()
        auth = self.root / "empty-auth"
        auth.mkdir()
        launches = []

        def fake_launch(command, **kwargs):
            output = Path(command[command.index("-o") + 1])
            output.write_text("{}", encoding="utf-8")
            home = Path(kwargs["env"]["CODEX_HOME"])
            saved = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
            launches.append((kwargs["env"]["CELL_ROLE"], home))
            self.assertEqual(saved["web_search"], "disabled")
            self.assertEqual(kwargs["env"]["CELL_SEARCH_ENABLED"], "0")
            if kwargs["env"]["CELL_ROLE"] != "audit":
                self.assertEqual(saved["mcp_servers"]["research"]["env"]["CELL_SEARCH_ENABLED"], "0")
            process = Mock(returncode=0)
            process.poll.return_value = 0
            return process

        with patch.object(processes, "ROOT", self.root / "runtime-project"), \
                patch.object(processes, "_user_home", return_value=auth), \
                patch.object(processes, "_user_settings", return_value={}), \
                patch.object(processes, "find_codex", return_value="no-model-test-executable"), \
                patch.object(processes.subprocess, "Popen", side_effect=fake_launch), \
                patch.dict(os.environ, {"OPENAI_API_KEY": "test-only-no-network"}):
            processes.run_agent("Test offline prover", task, task / "response.json", role="prover", settings=selected)
            for stage, suffix in (("proof", "workspace"), ("report_check", "checks/p0001/workspace")):
                work = task / "reviews/r0001" / suffix
                work.mkdir(parents=True)
                (work / "review_request.json").write_text(json.dumps({"stage": stage,
                    "review_id": "r0001", "report_revision": 1}), encoding="utf-8")
                (work / "receipt.schema.json").write_text('{"type":"object","properties":{}}', encoding="utf-8")
                review._launch_review(work, selected)
            work = task / "audits/a1"
            processes.run_agent("Test offline audit", work, work / "response.json", role="audit", settings=selected)

        self.assertEqual([role for role, _ in launches], ["prover", "verifier", "verifier", "audit"])
        for _, home in launches:
            self.assertEqual(tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))["web_search"], "disabled")
        self.assertEqual((task / "run.json").read_bytes(), original)

    def test_review_rejects_invalid_owner_search_option(self):
        task = self.root / "invalid"
        self.write_run(task, "prover", "false")
        with self.assertRaisesRegex(ValueError, "search_enabled must be true or false"):
            settings.get_search_enabled("verifier", self.base, task / "reviews/r0001/workspace")

    def test_offline_primary_and_independent_review_lookup_never_reaches_http(self):
        task = self.root / "offline"
        self.write_run(task, "prover", False)
        for suffix in ("workspace", "checks/p0001/workspace"):
            with self.subTest(stage=suffix):
                work = task / "reviews/r0001" / suffix
                with patch.dict(os.environ, {"CELL_RUN_DIR": str(work), "CELL_ROLE": "verifier"}), \
                        patch.object(lookup_module, "_arxiv_search") as arxiv, \
                        patch.object(lookup_module.requests, "get") as http:
                    for kwargs in ({"query": "variance bound"}, {"url": "https://example.invalid/paper"}):
                        result = lookup_module.lookup(**kwargs)
                        self.assertFalse(result["ok"])
                        self.assertEqual(result["error"]["kind"], "search_disabled")
                    with self.assertRaises(lookup_module.LookupError):
                        lookup_module._request("https://example.invalid/paper")
                    arxiv.assert_not_called()
                    http.assert_not_called()

    def test_main_launch_and_resume_search_override_leave_user_defaults_untouched(self):
        before = settings.CONFIG_PATH.read_bytes()
        problem = self.root / "problem.md"
        problem.write_text("Prove 2 is even.", encoding="utf-8")
        work = self.root / "main"
        with patch.object(run, "solve", return_value=0):
            with patch.object(sys, "argv", ["run.py", str(problem), "--run-dir", str(work), "--no-search"]):
                self.assertEqual(run.main(), 0)
            self.assertFalse(settings.get_search_enabled("prover", settings.get_settings(work), work))
            with patch.object(sys, "argv", ["run.py", "--run-dir", str(work), "--resume", "--search"]):
                self.assertEqual(run.main(), 0)
        self.assertTrue(settings.get_search_enabled("prover", settings.get_settings(work), work))
        self.assertEqual(settings.get_settings(work)["network"]["subcell_search_enabled"],
                         self.base["network"]["subcell_search_enabled"])
        self.assertEqual(settings.CONFIG_PATH.read_bytes(), before)

    def test_prover_next_turn_reloads_requested_settings(self):
        problem = self.root / "problem.md"
        problem.write_text("Prove 2 is even.", encoding="utf-8")
        work = self.root / "main"
        run.initialize(problem, work)
        policy = settings.load_policy(profile="hard")
        policy["cell"]["settings"]["agents"]["prover_max_rounds"] = 2
        observed = []

        def model(prompt, directory, output, **kwargs):
            observed.append((kwargs["timeout"], kwargs["model"],
                             settings.get_search_enabled("prover", kwargs["settings"], directory)))
            if len(observed) == 1:
                configure(work, "prover", {"model": {"name": "next-model", "reasoning_effort": "high"}},
                          search_enabled=False, reason="Use deeper reasoning on the next attempt")
            return {"session_id": "test", "log_path": str(output)}

        with patch.object(run, "run_agent", side_effect=model), \
                patch.object(settings, "load_policy", return_value=policy), \
                patch.object(run, "manuscript_is_current", return_value=False), \
                patch.object(run, "review_submission", return_value={"status": "pending", "reason": "Test pending proof"}):
            self.assertEqual(run.solve(work), 2)
        self.assertEqual(len(observed), 2)
        self.assertEqual(observed[1], ("unlimited", "next-model", False))


class MCPLiveSettingsTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.env = patch.dict(os.environ)
        self.env.start()
        self.addCleanup(self.env.stop)
        for name in ENV_KEYS:
            os.environ.pop(name, None)
        self.temp = tempfile.TemporaryDirectory(prefix=".mcp-search-test-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = settings.get_settings()
        self.base["network"].update(search_provider="arxiv", reader_provider="direct")
        self.user_before = settings.CONFIG_PATH.read_bytes()
        self.work = self.root / "subcell"
        self.work.mkdir()
        (self.work / "run.json").write_text(json.dumps({
            "role": "subcell", "task_depth": 1, "settings": self.base,
            **settings.run_fields(self.base), "agent_options": {"search_enabled": False},
        }), encoding="utf-8")
        self.launch = self.root / "settings.json"
        self.launch.write_text(json.dumps(self.base), encoding="utf-8")

    @asynccontextmanager
    async def server(self):
        from mcp import ClientSession
        from mcp import StdioServerParameters
        from mcp.client.stdio import stdio_client
        params = StdioServerParameters(
            command=sys.executable, args=["-B", str(ROOT / "src/colombo/cell/mcp_server.py")], cwd=ROOT,
            env={**os.environ, "CELL_RUN_DIR": str(self.work), "CELL_ROLE": "subcell",
                 "CELL_SETTINGS_FILE": str(self.launch), "CELL_SEARCH_ENABLED": "0", "PYTHONUTF8": "1",
                 "CELL_CODEX_BIN": str(self.root / "no-model.exe")},
        )
        with (self.root / "mcp.log").open("w", encoding="utf-8") as log:
            async with stdio_client(params, errlog=log) as (reader, writer):
                async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=20)) as session:
                    await session.initialize()
                    yield session

    def data(self, response):
        self.assertFalse(response.isError, response.content)
        return response.structuredContent or json.loads(next(c.text for c in response.content if c.type == "text"))

    async def test_same_mcp_session_toggles_search_and_reads_new_tool_settings(self):
        hits = []

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                hits.append(self.path)
                body = b"Full source text: every even integer has the form 2k."
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        http = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=http.serve_forever, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{http.server_port}/paper"
        try:
            async with self.server() as server:
                names = {tool.name for tool in (await server.list_tools()).tools}
                self.assertTrue({"configure", "lookup", "retrieve", "spawn_task"} <= names)
                blocked = self.data(await server.call_tool("lookup", {"url": url}))
                self.assertEqual(blocked["error"]["kind"], "search_disabled")
                self.assertEqual(hits, [])
                enabled = self.data(await server.call_tool("configure", {
                    "search_enabled": True, "settings_overrides": {"retrieval": {"include_context": False}},
                    "reason": "Need to read a source and narrow record retrieval",
                }))
                self.assertTrue(enabled["lookup_enabled"])
                self.assertFalse(enabled["native_search_enabled"])
                self.assertTrue(any(p["parameter"] == "native_search_enabled" for p in enabled["pending_next_start"]))
                found = self.data(await server.call_tool("lookup", {"url": url}))
                self.assertTrue(found["ok"], found)
                self.assertIn("every even integer", found["results"][0]["text"])
                self.assertEqual(hits, ["/paper"])
                for i in range(2):
                    self.data(await server.call_tool("archive", {"kind": "claims", "record_id": f"c{i}",
                                                                 "payload": {"statement": str(i)}}))
                records = self.data(await server.call_tool("retrieve", {"kinds": ["claims"], "limit": 1}))
                self.assertEqual(records["returned"], 1)
                self.data(await server.call_tool("configure", {"search_enabled": False, "reason": "Source reading complete"}))
                blocked = self.data(await server.call_tool("lookup", {"url": url}))
                self.assertEqual(blocked["error"]["kind"], "search_disabled")
                self.assertEqual(hits, ["/paper"])
                current = self.data(await server.call_tool("configure", {}))
                self.assertFalse(current["lookup_enabled"])
                self.assertEqual(current["pending_next_start"], [])
                self.assertEqual(current["settings_revision"], 2)
        finally:
            http.shutdown()
            http.server_close()
            thread.join(timeout=5)
        self.assertEqual(settings.CONFIG_PATH.read_bytes(), self.user_before)
        self.assertEqual(json.loads(self.launch.read_text(encoding="utf-8")), self.base)
        saved = json.loads((self.work / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(len(saved["settings_history"]), 2)


if __name__ == "__main__":
    unittest.main()
