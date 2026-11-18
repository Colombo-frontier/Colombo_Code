"""Scientific Memory through real Brain STDIO; no model or network calls."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import shutil
import tomllib
import unittest
from unittest.mock import patch

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import test_mcp as fixture
import test_backend as backend_fixture
from brain_fixtures import write_review_package

PROJECT = Path(__file__).resolve().parents[2]
from colombo.memory.integration import DEFAULT_MEMORY_ROOT, register_builtin_memory
from colombo.memory.store import Store
from colombo.memory.contracts import ContractError
from mcp.server.fastmcp import FastMCP

LEGACY_ENV = "COLOMBO_SCIENTIFIC_MEMORY_ROOT"


def installed_record_count():
    return sum(1 for library in ("algorithm_family_library", "hard_family_library",
                                 "theorem_library", "source")
               for _ in (DEFAULT_MEMORY_ROOT / library).glob("*.json"))


def snapshot(root):
    # The read-only contract covers both scientific bodies and external state.
    locations = (("records", root), ("state", Store(root).state_root))
    return {f"{label}/{p.relative_to(location).as_posix()}": hashlib.sha256(p.read_bytes()).hexdigest()
            for label, location in locations for p in location.rglob("*") if p.is_file()}


class ScientificMemoryMCPTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        fixture.MCPServerTests.setUp(self)
        self.library = DEFAULT_MEMORY_ROOT
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, {"PYTHONPATH": str(PROJECT / "src")}).start()
        os.environ.pop(LEGACY_ENV, None)

    prepare_call = fixture.MCPServerTests.prepare_call
    connect = fixture.MCPServerTests.connect

    async def memory(self, session, mode, **args):
        response = await session.call_tool("scientific_memory", {
            "mode": mode, "arguments_json": json.dumps(args),
        })
        self.assertFalse(response.isError, fixture.error_text(response))
        return fixture.response_object(response)

    async def test_five_operations_keep_library_and_research_state_unchanged(self):
        self.prepare_call("brain", "plan", "scientific-roundtrip")
        before = snapshot(self.library)
        research = self.store.read_document("research")
        async with self.connect("brain", "plan", "scientific-roundtrip") as session:
            tools = {tool.name: tool for tool in (await session.list_tools()).tools}
            self.assertNotIn("recollect", tools)
            tool = tools["scientific_memory"]
            self.assertTrue(tool.annotations.readOnlyHint)
            self.assertFalse(tool.annotations.destructiveHint)
            self.assertEqual(set(tool.inputSchema["properties"]), {"mode", "arguments_json"})
            self.assertEqual(tool.inputSchema["required"], ["mode"])
            overview = await self.memory(session, "overview", include_leads=True, limit=50)
            self.assertTrue(overview["branches"])
            concept = overview["branches"][0]["concept_id"]
            browse = await self.memory(session, "browse", concept=concept, include_leads=True)
            self.assertTrue(browse["items"])
            published = await self.memory(session, "search", query="SPIDER")
            self.assertTrue(published["items"])
            self.assertTrue(all(item["ref"]["tier"] == "published" for item in published["items"]))
            hits = await self.memory(session, "search", query="SPIDER", include_leads=True)
            self.assertTrue(hits["items"])
            ref = hits["items"][0]["ref"]
            first = await self.memory(session, "read", ref=ref, pointer="#/content", limit=50)
            self.assertFalse(first["complete"])
            second = await self.memory(session, "read", ref=ref, pointer="#/content",
                                       offset=first["next_offset"], limit=50)
            self.assertEqual(second["offset"], first["next_offset"])
            self.assertNotEqual(first["text"], second["text"])
            expanded = await self.memory(session, "expand", ref=ref, include_leads=True)
            self.assertIn("items", expanded)
            self.assertTrue((await session.call_tool("recollect", {"query": "gradient descent"})).isError)
            self.assertEqual(sum(overview["counts"].values()), installed_record_count())
        self.assertEqual(before, snapshot(self.library))
        self.assertEqual(research, self.store.read_document("research"))

    async def test_default_inventory_ignores_obsolete_environment_and_needs_no_external_package(self):
        self.prepare_call("brain", "plan", "scientific-default")
        # An old launcher environment cannot silently redirect the current library.
        with patch.dict(os.environ, {LEGACY_ENV: "/missing/retired-external-library"}):
            async with self.connect("brain", "plan", "scientific-default") as session:
                self.assertEqual({t.name for t in (await session.list_tools()).tools}, {
                    "read_research", "read_material", "submit_plan", "audit", "save_note",
                    "lookup", "scientific_memory", "job_status", "format_package_literal",
                })
                result = await self.memory(session, "overview", include_leads=True)
                self.assertEqual(sum(result["counts"].values()), installed_record_count())

    async def test_historical_references_are_explicitly_retired_without_remapping(self):
        self.prepare_call("brain", "plan", "scientific-legacy-ref")
        legacy = {"id": "ALG-GD::S-CONVEX", "version": "1.0.0",
                  "content_hash": "0" * 64, "index_version": "1" * 64}
        async with self.connect("brain", "plan", "scientific-legacy-ref") as session:
            for mode in ("read", "expand"):
                response = await session.call_tool("scientific_memory", {
                    "mode": mode, "arguments_json": json.dumps({"ref": legacy})})
                self.assertTrue(response.isError)
                self.assertIn("legacy_ref_retired", fixture.error_text(response))

    async def test_verifier_has_no_live_reader_even_with_invalid_configuration(self):
        package = write_review_package(self.store, {
            "allowed_refs": [self.material_ref["id"]], "required_checked_refs": [self.material_ref["id"]],
        })
        self.prepare_call("verifier", "verify-progress", "scientific-verifier", review_package_ref=package)
        with patch.dict(os.environ, {LEGACY_ENV: "invalid-relative-path"}):
            async with self.connect("verifier", "verify-progress", "scientific-verifier") as session:
                names = {t.name for t in (await session.list_tools()).tools}
                self.assertNotIn("scientific_memory", names)
                self.assertNotIn("recollect", names)
                self.assertTrue((await session.call_tool("scientific_memory", {"mode": "search"})).isError)

    async def test_reader_has_no_write_or_model_selected_library_argument(self):
        self.prepare_call("brain", "plan", "scientific-boundary")
        before = snapshot(self.library)
        async with self.connect("brain", "plan", "scientific-boundary") as session:
            for mode, args in (("publish", {}), ("search", {"memory_root": "/tmp/other"}),
                               ("read", {"ref": {"id": "invented"}})):
                with self.subTest(mode=mode, args=args):
                    response = await session.call_tool("scientific_memory", {
                        "mode": mode, "arguments_json": json.dumps(args),
                    })
                    self.assertTrue(response.isError)
        self.assertEqual(before, snapshot(self.library))


class ScientificMemoryConfigurationTests(unittest.TestCase):
    setUp = backend_fixture.BackendTests.setUp

    def test_generated_mcp_configuration_reaches_the_builtin_memory(self):
        work = self.run_root / "brain/calls/generated-memory"
        work.mkdir(parents=True)
        identity = {"role": "brain", "stage": "plan", "call_id": "generated-memory"}
        (work / "context.json").write_text(json.dumps(identity))
        (work / "call.json").write_text(json.dumps(identity))
        self.store.set_meta(pending_call={**identity, "context": {}})
        self.backend.project_root = PROJECT
        home = self.root / "generated-memory-home"
        with patch.dict(os.environ, {LEGACY_ENV: "/obsolete/not-the-current-memory"}):
            self.backend._prepare_home(home, "brain", "plan", self.run_root, work,
                                      "generated-memory", self.backend._settings("brain"))
        server = tomllib.loads((home / "config.toml").read_text())["mcp_servers"]["colombo"]

        async def exercise():
            parameters = StdioServerParameters(command=server["command"], args=server["args"],
                cwd=server["cwd"], env={**server["env"], "PYTHONPATH": str(PROJECT / "src")})
            with (self.root / "generated-config-mcp.log").open("w") as log:
                async with stdio_client(parameters, errlog=log) as (read, write):
                    async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=20)) as session:
                        await session.initialize()
                        response = await session.call_tool("scientific_memory", {
                            "mode": "search", "arguments_json": json.dumps({"query": "SPIDER", "include_leads": True})})
                        self.assertFalse(response.isError, fixture.error_text(response))
                        self.assertTrue(fixture.response_object(response)["items"])
        asyncio.run(exercise())

    def test_private_model_homes_do_not_forward_external_memory_configuration(self):
        for role in ("brain", "verifier"):
            with self.subTest(role=role), patch.dict(os.environ, {LEGACY_ENV: str(self.root / "configured-library")}):
                home = self.root / ("memory-home-" + role)
                self.backend._prepare_home(home, role, "plan" if role == "brain" else "verify-progress",
                    self.run_root, self.root / "work", "fixture", self.backend._settings(role))
                server = tomllib.loads((home / "config.toml").read_text())["mcp_servers"]["colombo"]
                self.assertNotIn(LEGACY_ENV, server["env"])
        with patch.dict(os.environ, {LEGACY_ENV: str(self.root / "configured-library")}):
            home = self.root / "audit-memory-home"
            self.backend._prepare_home(home, "audit", "audit", self.run_root, self.root / "work", "fixture",
                self.backend._settings("brain"), enable_mcp=False)
            self.assertNotIn("mcp_servers", tomllib.loads((home / "config.toml").read_text()))


class BuiltinMemoryRegistrationTests(unittest.TestCase):
    def test_default_is_one_installed_memory_and_the_legacy_loaders_are_gone(self):
        self.assertEqual(DEFAULT_MEMORY_ROOT, PROJECT / "long_term_memory")
        for name in ("library_search.py", "scientific_memory.py"):
            self.assertFalse((PROJECT / "src/colombo/shared" / name).exists())
        self.assertFalse((PROJECT / "scientific_memory").exists())
        self.assertTrue((PROJECT / "colombo_memory_agent").is_dir())
        self.assertFalse((PROJECT / "colombo_memory_agent/long_term_memory").exists())
        for retired in ("scripts/recollect.py", "indexes/recollect.json", "schemas/recollect_policy.json"):
            self.assertFalse((DEFAULT_MEMORY_ROOT / retired).exists())
        self.assertTrue(register_builtin_memory(FastMCP("builtin"), research_mode="oracle_complexity"))

    def test_python_override_is_for_isolated_stores_not_environment_selection(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "memory"
            shutil.copytree(DEFAULT_MEMORY_ROOT, target)
            # A portable library consists of its four bodies and sibling state;
            # registration must fail without creating or repairing missing state.
            target_state = Store(target).state_root
            with self.assertRaises(ContractError):
                register_builtin_memory(FastMCP("state-absent"), research_mode="generic", memory_root=target)
            self.assertFalse(target_state.exists())
            shutil.copytree(Store(DEFAULT_MEMORY_ROOT).state_root, target_state)
            before = snapshot(target)
            self.assertTrue(register_builtin_memory(FastMCP("isolated"), research_mode="generic", memory_root=target))
            self.assertEqual(before, snapshot(target))
            absent = Path(temporary) / "not-created"
            with self.assertRaises(ContractError):
                register_builtin_memory(FastMCP("absent"), research_mode="generic", memory_root=absent)
            self.assertFalse(absent.exists())
        with self.assertRaises(ContractError):
            register_builtin_memory(FastMCP("relative"), research_mode="generic", memory_root="relative")


if __name__ == "__main__":
    unittest.main()
