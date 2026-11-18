"""Finder metadata must not break MCP or weaken scientific Memory checks."""
from __future__ import annotations

from datetime import timedelta
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.server.fastmcp import FastMCP

from colombo.configuration import PROJECT_ROOT, load_config
from colombo.brain.research_store import Store as ResearchStore
from colombo.memory.contracts import ContractError, LIBRARIES
from colombo.memory.integration import DEFAULT_MEMORY_ROOT, register_builtin_memory
from colombo.memory.store import Store as MemoryStore
from test_oracle_workflow import SETTING


def snapshot(root):
    locations = (("records", root), ("state", MemoryStore(root).state_root))
    return {f"{label}/{p.relative_to(location).as_posix()}": hashlib.sha256(p.read_bytes()).hexdigest()
            for label, location in locations for p in location.rglob("*") if p.is_file()}


def response_object(response):
    if response.structuredContent is not None:
        return response.structuredContent
    return json.loads("\n".join(part.text for part in response.content if part.type == "text"))


class MemoryMetadataTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="memory-metadata-")
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)
        self.library = self.folder / "memory"
        # Tests use a disposable copy of the paired library and external state.
        shutil.copytree(DEFAULT_MEMORY_ROOT, self.library, symlinks=True,
                        ignore=shutil.ignore_patterns(".DS_Store"))
        shutil.copytree(MemoryStore(DEFAULT_MEMORY_ROOT).state_root,
                        MemoryStore(self.library).state_root, symlinks=True)
        self.locations = [self.library, *(self.library / name for name in LIBRARIES.values())]

    def add_metadata(self):
        for index, folder in enumerate(self.locations):
            (folder / ".DS_Store").write_bytes(b"\x00Finder metadata fixture\xff" + bytes([index]))

    def register(self):
        return register_builtin_memory(FastMCP("metadata-fixture"),
            research_mode="oracle_complexity", memory_root=self.library)

    async def test_regular_metadata_registers_without_changing_records_or_state(self):
        self.add_metadata()
        before = snapshot(self.library)
        self.assertTrue(self.register())
        self.assertEqual(before, snapshot(self.library))

    async def test_unknown_files_and_directories_are_still_rejected(self):
        self.add_metadata()
        before = snapshot(self.library)
        for folder in self.locations:
            for name, directory in (("unexpected.txt", False), (".unknown", False),
                                    ("uncatalogued.json", False), ("unexpected-directory", True)):
                with self.subTest(folder=folder.name, name=name):
                    extra = folder / name
                    extra.mkdir() if directory else extra.write_text("{}", encoding="utf-8")
                    try:
                        with self.assertRaises(ContractError):
                            self.register()
                    finally:
                        extra.rmdir() if directory else extra.unlink()
        self.assertEqual(before, snapshot(self.library))

    async def test_metadata_named_directories_are_still_rejected(self):
        for folder in self.locations:
            with self.subTest(folder=folder.name):
                candidate = folder / ".DS_Store"
                candidate.mkdir()
                try:
                    with self.assertRaises(ContractError):
                        self.register()
                finally:
                    candidate.rmdir()

    async def test_metadata_named_symlinks_are_still_rejected(self):
        outside = self.folder / "outside-metadata"
        outside.write_bytes(b"not a scientific record")
        for folder in self.locations:
            with self.subTest(folder=folder.name):
                candidate = folder / ".DS_Store"
                try:
                    candidate.symlink_to(outside)
                except (OSError, NotImplementedError) as exc:
                    # Windows may require Developer Mode or symlink privileges.
                    self.skipTest(f"Symlink creation unavailable: {exc}")
                try:
                    with self.assertRaises(ContractError):
                        self.register()
                finally:
                    candidate.unlink()
        self.assertEqual(outside.read_bytes(), b"not a scientific record")

    async def test_metadata_does_not_hide_tampered_records(self):
        self.add_metadata()
        store = MemoryStore(self.library)
        record = store.current_records(include_leads=True)[0]
        visible = store.current_path(record["id"], record["kind"])
        changed = json.loads(visible.read_text(encoding="utf-8"))
        changed["metadata_regression_fixture"] = True
        visible.write_text(json.dumps(changed), encoding="utf-8")
        before = snapshot(self.library)
        with self.assertRaises(ContractError):
            self.register()
        self.assertEqual(before, snapshot(self.library))

    async def test_metadata_does_not_hide_missing_records(self):
        self.add_metadata()
        store = MemoryStore(self.library)
        record = store.current_records(include_leads=True)[0]
        store.current_path(record["id"], record["kind"]).unlink()
        before = snapshot(self.library)
        with self.assertRaises(ContractError):
            self.register()
        self.assertEqual(before, snapshot(self.library))

    async def test_real_stdio_can_read_and_submit_plan_with_metadata(self):
        self.add_metadata()
        before = snapshot(self.library)
        expected_count = len(MemoryStore(self.library).current_records(include_leads=True))
        run = self.folder / "run"
        store = ResearchStore.create(run, "Offline metadata MCP fixture", [], load_config())
        identity = {"role": "brain", "stage": "plan", "call_id": "metadata-stdio"}
        work = run / "brain/calls" / identity["call_id"]
        work.mkdir(parents=True)
        (work / "call.json").write_text(json.dumps(identity), encoding="utf-8")
        context = {**identity, "dispatch_remaining": 6}
        (work / "context.json").write_text(json.dumps(context), encoding="utf-8")
        store.set_meta(pending_call={**identity, "context": {"dispatch_remaining": 6}})
        # Only the test process selects the copied Memory through the Python override.
        bootstrap = (
            "import sys; from pathlib import Path; "
            "import colombo.memory.integration as memory; "
            "memory.DEFAULT_MEMORY_ROOT=Path(sys.argv[1]); "
            "from colombo.brain.mcp_server import serve; "
            "serve(sys.argv[2], 'brain', 'plan', 'metadata-stdio')"
        )
        params = StdioServerParameters(command=sys.executable,
            args=["-B", "-c", bootstrap, str(self.library), str(run)],
            cwd=str(PROJECT_ROOT), env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "src")})
        with (self.folder / "stdio-stderr.log").open("w", encoding="utf-8") as errors:
            async with stdio_client(params, errlog=errors) as (read, write):
                async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=20)) as session:
                    await session.initialize()
                    names = {tool.name for tool in (await session.list_tools()).tools}
                    self.assertTrue({"read_research", "scientific_memory", "submit_plan"}.issubset(names))
                    state = await session.call_tool("read_research", {})
                    self.assertFalse(state.isError)
                    self.assertIn("goal", response_object(state))
                    overview = await session.call_tool("scientific_memory", {
                        "mode": "overview", "arguments_json": json.dumps({"include_leads": True})})
                    self.assertFalse(overview.isError)
                    self.assertEqual(sum(response_object(overview)["counts"].values()), expected_count)
                    reply = await session.call_tool("submit_plan", {"payload": {
                        "rationale": "Offline metadata fixture; no research dispatch.",
                        "tasks": [], "setting_specification": SETTING}})
                    self.assertFalse(reply.isError)
                    receipt = response_object(reply)
                    self.assertEqual(store.read_record(receipt["ref"])["setting_specification"], SETTING)
        self.assertTrue((work / "submission.json").is_file())
        self.assertEqual(before, snapshot(self.library))


if __name__ == "__main__":
    unittest.main()
