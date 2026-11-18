"""Real Colombo STDIO transport, with no model or external API calls."""
from datetime import timedelta
import os
from pathlib import Path
import sys
import tempfile
import unittest

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from colombo.configuration import load_config, PROJECT_ROOT
from colombo.brain.research_store import Store
import test_mcp as transport
from test_mcp import response_object, error_text
from test_oracle_workflow import SETTING


class OracleMCPTransportTests(unittest.IsolatedAsyncioTestCase):
    prepare_call = transport.MCPServerTests.prepare_call
    connect = transport.MCPServerTests.connect

    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="colombo-mcp-")
        self.addCleanup(tmp.cleanup)
        self.folder = Path(tmp.name)
        self.store = Store.create(self.folder / "run", "Oracle fixture", [], load_config())

    async def test_first_plan_commits_setting_payload_over_stdio(self):
        self.prepare_call("brain", "plan", "Colombo-PLAN", dispatch_remaining=6)
        async with self.connect("brain", "plan", "Colombo-PLAN") as session:
            tools = {t.name for t in (await session.list_tools()).tools}
            self.assertIn("submit_plan", tools)
            reply = await session.call_tool("submit_plan", {"payload": {
                "rationale": "No new Task is needed for this transport fixture.",
                "tasks": [], "setting_specification": SETTING}})
            self.assertFalse(reply.isError, error_text(reply))
            receipt = response_object(reply)
            self.assertEqual(self.store.read_record(receipt["ref"])["setting_specification"], SETTING)

    async def test_integrate_exposes_new_record_results_schema(self):
        self.prepare_call("brain", "integrate", "Colombo-INTEGRATE")
        async with self.connect("brain", "integrate", "Colombo-INTEGRATE") as session:
            tools = {t.name: t for t in (await session.list_tools()).tools}
            self.assertIn("record_results", tools)
            self.assertNotIn("submit_plan", tools)
            update = tools["record_results"].inputSchema["properties"]["payload"]["properties"]["update"]
            self.assertIn("proof_draft", update["required"])
            self.assertIn("bracket", update["properties"]["progress"]["properties"])


class ExperimentMCPTransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_independent_experiment_stdio_returns_empirical_receipt(self):
        from test_experiment_dispatch import ExperimentDispatchTests
        fixture = ExperimentDispatchTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        env = {**os.environ, "CELL_RUN_DIR": str(fixture.root),
               "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
        params = StdioServerParameters(command=sys.executable,
            args=["-B", str(PROJECT_ROOT / "src/colombo/experiment_cell/mcp_server.py")],
            cwd=str(PROJECT_ROOT), env=env)
        with (fixture.base / "stdio.log").open("w", encoding="utf-8") as errors:
            async with stdio_client(params, errlog=errors) as (read, write):
                async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=20)) as session:
                    await session.initialize()
                    names = {t.name for t in (await session.list_tools()).tools}
                    self.assertTrue({"run_experiment", "resume_experiment", "submit_report"}.issubset(names))
                    self.assertNotIn("submit_proof", names)
                    self.assertNotIn("scientific_memory", names)
                    self.assertNotIn("recollect", names)
                    reply = await session.call_tool("submit_report", {"report": fixture.report(),
                        "body": "# Empirical report\n\nThe pilot remains inconclusive."})
                    self.assertFalse(reply.isError, error_text(reply))
                    receipt = response_object(reply)
                    self.assertEqual(receipt["evidence_kind"], "empirical")
                    self.assertFalse(receipt["accepted"])


if __name__ == "__main__":
    unittest.main()
