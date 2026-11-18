"""Real Cell STDIO permissions and isolated launch configuration; no model calls."""
from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import timedelta
import asyncio
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from colombo.cell import model_calls, settings
from colombo.cell.instructions import install_cell_pack, validate_mode
from colombo.memory.integration import DEFAULT_MEMORY_ROOT
from colombo.memory.store import Store

LEGACY_ENV = "COLOMBO_SCIENTIFIC_MEMORY_ROOT"
import test_models_cache_runtime as cache_fixture


def snapshot(root):
    # The read-only contract covers both scientific bodies and external state.
    locations = (("records", root), ("state", Store(root).state_root))
    return {f"{label}/{p.relative_to(location).as_posix()}": hashlib.sha256(p.read_bytes()).hexdigest()
            for label, location in locations for p in location.rglob("*") if p.is_file()}


def response_data(response):
    return response.structuredContent or json.loads("\n".join(c.text for c in response.content if c.type == "text"))


class CellScientificMemoryTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix=".scientific-memory-test-", dir=ROOT)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.library = DEFAULT_MEMORY_ROOT
        self.base = settings.get_settings()
        self.launch = self.root / "settings.json"
        self.launch.write_text(json.dumps(self.base))

    @asynccontextmanager
    async def server(self, role="prover", mode="oracle_complexity", *, experiment=False):
        work = self.root / (role + "-" + mode + ("-experiment" if experiment else ""))
        work.mkdir()
        specialization = "experiment" if experiment else "general"
        (work / "run.json").write_text(json.dumps({
            "role": role, "task_depth": int(role == "subcell"), "settings": self.base,
            "cell_mode": validate_mode(mode, specialization),
            **settings.run_fields(self.base), "agent_options": {"search_enabled": False},
        }))
        script = (ROOT / "src/colombo/experiment_cell/mcp_server.py" if experiment else
                  ROOT / "src/colombo/cell" / ("verifier/mcp_server.py" if role == "verifier" else "mcp_server.py"))
        params = StdioServerParameters(command=sys.executable, args=["-B", str(script)], cwd=str(work),
            env={**{k: v for k, v in os.environ.items() if k != LEGACY_ENV}, "CELL_RUN_DIR": str(work), "CELL_ROLE": role,
                 "CELL_SETTINGS_FILE": str(self.launch), "CELL_SEARCH_ENABLED": "0", "PYTHONUTF8": "1",
                 "PYTHONPATH": str(ROOT / "src")})
        with (self.root / (work.name + ".log")).open("w") as log:
            async with stdio_client(params, errlog=log) as (reader, writer):
                async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=20)) as session:
                    await session.initialize()
                    yield session

    async def memory(self, session, mode, **args):
        response = await session.call_tool("scientific_memory", {"mode": mode, "arguments_json": json.dumps(args)})
        self.assertFalse(response.isError, response.content)
        return response_data(response)

    async def test_prover_and_subcell_read_same_memory_without_writes(self):
        before = snapshot(self.library)
        refs = []
        for role in ("prover", "subcell"):
            with self.subTest(role=role):
                async with self.server(role) as session:
                    tools = {t.name: t for t in (await session.list_tools()).tools}
                    self.assertNotIn("recollect", tools)
                    self.assertTrue(tools["scientific_memory"].annotations.readOnlyHint)
                    results = await self.memory(session, "search", query="SPIDER", include_leads=True)
                    self.assertTrue(results["items"])
                    ref = results["items"][0]["ref"]
                    refs.append(ref)
                    body = await self.memory(session, "read", ref=ref, pointer="#/content", limit=100)
                    self.assertTrue(body["text"])
                    self.assertFalse(results["items"][0]["certifies_applicability"])
        self.assertEqual(refs[0], refs[1])
        self.assertEqual(before, snapshot(self.library))

    async def test_generic_projects_every_operation_and_rejects_forged_kind(self):
        before = snapshot(self.library)
        async with self.server("subcell") as unrestricted:
            algorithm = (await self.memory(unrestricted, "search", query="SPIDER", kinds=["algorithm"],
                                           include_leads=True))["items"][0]["ref"]
        async with self.server("prover", "generic") as session:
            overview = await self.memory(session, "overview", include_leads=True, limit=50)
            self.assertTrue(overview["counts"])
            self.assertTrue(all(key.endswith(":theorem") for key in overview["counts"]))
            concept = overview["branches"][0]["concept_id"]
            for mode, args in (("search", {"query": "SPIDER"}), ("browse", {"concept": concept})):
                results = await self.memory(session, mode, include_leads=True, **args)
                self.assertTrue(results["items"])
                self.assertTrue(all(c["ref"]["kind"] == "theorem" for c in results["items"]))
            hits = await self.memory(session, "search", query="SPIDER", include_leads=True)
            ref = hits["items"][0]["ref"]
            self.assertTrue((await self.memory(session, "read", ref=ref))["text"])
            expanded = await self.memory(session, "expand", ref=ref, include_leads=True, limit=1)
            self.assertTrue(all(item["ref"]["kind"] == "theorem" for item in expanded["items"]))
            for mode, args in (("search", {"kinds": ["algorithm"]}),
                               ("read", {"ref": {**algorithm, "kind": "theorem"}}),
                               ("expand", {"ref": {**algorithm, "kind": "theorem"}})):
                with self.subTest(mode=mode):
                    response = await session.call_tool("scientific_memory", {
                        "mode": mode, "arguments_json": json.dumps(args),
                    })
                    self.assertTrue(response.isError)
        self.assertEqual(before, snapshot(self.library))

    async def test_verifier_and_experiment_keep_existing_tool_surfaces(self):
        for role, experiment in (("verifier", False), ("prover", True)):
            with self.subTest(role=role, experiment=experiment):
                async with self.server(role, experiment=experiment) as session:
                    names = {t.name for t in (await session.list_tools()).tools}
                    self.assertNotIn("scientific_memory", names)
                    self.assertNotIn("recollect", names)
                    self.assertTrue((await session.call_tool("scientific_memory", {"mode": "overview"})).isError)


class CellMemoryLaunchTests(unittest.TestCase):
    setUp = cache_fixture.ModelsCacheRuntimeTests.setUp

    def test_generated_mcp_configuration_reaches_builtin_memory_without_environment(self):
        home = model_calls._prepare_home(self.work, "prover", None, False, {}, settings=self.selected)
        server = tomllib.loads((home / "config.toml").read_text())["mcp_servers"]["research"]

        async def exercise():
            parameters = StdioServerParameters(command=server["command"], args=server["args"],
                cwd=server["cwd"], env={**server["env"], "PYTHONPATH": str(ROOT / "src")})
            with (self.root / "generated-config-mcp.log").open("w") as log:
                async with stdio_client(parameters, errlog=log) as (reader, writer):
                    async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=20)) as session:
                        await session.initialize()
                        response = await session.call_tool("scientific_memory", {
                            "mode": "search", "arguments_json": json.dumps({"query": "SPIDER", "include_leads": True})})
                        self.assertFalse(response.isError, response.content)
                        self.assertTrue(response_data(response)["items"])
        asyncio.run(exercise())

    def test_builtin_reader_needs_no_memory_environment_in_any_model_home(self):
        configured = str(self.root / "configured memory")
        for role in ("prover", "subcell", "verifier", "audit"):
            with self.subTest(role=role), patch.dict(os.environ, {LEGACY_ENV: configured}):
                home = model_calls._prepare_home(self.work, role, None, False, {}, settings=self.selected)
                config = tomllib.loads((home / "config.toml").read_text())
                env = config.get("mcp_servers", {}).get("research", {}).get("env", {})
                self.assertNotIn(LEGACY_ENV, env)
        for role in ("prover", "subcell"):
            with patch.dict(os.environ, {LEGACY_ENV: configured}):
                home = model_calls._prepare_home(self.work, role, None, False, {}, settings=self.selected, recovery_only=True)
                self.assertNotIn("mcp_servers", tomllib.loads((home / "config.toml").read_text()))

    def test_obsolete_memory_environment_is_not_forwarded_even_when_explicit(self):
        explicit = str(self.root / "explicit memory")
        with patch.dict(os.environ, {LEGACY_ENV: str(self.root / "ambient memory")}):
            home = model_calls._prepare_home(self.work, "prover", None, False,
                {LEGACY_ENV: explicit}, settings=self.selected)
            server = tomllib.loads((home / "config.toml").read_text())["mcp_servers"]["research"]
            self.assertNotIn(LEGACY_ENV, server["env"])
            (self.work / "run.json").write_text(json.dumps({"cell_mode": validate_mode("oracle_complexity", "experiment")}))
            home = model_calls._prepare_home(self.work, "prover", None, False, {}, settings=self.selected)
            server = tomllib.loads((home / "config.toml").read_text())["mcp_servers"]["research"]
            self.assertEqual(Path(server["args"][1]).resolve(),
                             (ROOT / "src/colombo/experiment_cell/mcp_server.py").resolve())
            self.assertNotIn(LEGACY_ENV, server["env"])


class ScientificMemoryInstructionTests(unittest.TestCase):
    def test_runtime_instruction_packs_include_local_guide_for_research_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            for mode, specialization in (("generic", "general"), ("oracle_complexity", "general"),
                                          ("oracle_complexity", "upper_bound"), ("oracle_complexity", "lower_bound"),
                                          ("oracle_complexity", "experiment")):
                work = Path(temporary) / (mode + "-" + specialization)
                work.mkdir()
                install_cell_pack(work, validate_mode(mode, specialization))
                guide = work / ".agents/skills/scientific-memory/GUIDE.md"
                self.assertEqual(guide.is_file(), specialization != "experiment")
                if specialization != "experiment":
                    self.assertIn("scientific-memory/SKILL.md", (work / "AGENTS.md").read_text())
                    self.assertTrue((guide.parent / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
