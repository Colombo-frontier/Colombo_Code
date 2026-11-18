"""Verify Host integration through the actual component CLI/stdio MCP, without models or external paper services."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

from oracle_atlas.core.store import Workspace
from oracle_atlas.providers.mcp import MCPBridge


@unittest.skipUnless(importlib.util.find_spec("mcp"), "Optional MCP SDK is not installed")
class ActualHostMCPTests(unittest.TestCase):
    def test_cli_host_memory_isolation_and_reviewer_write_boundary(self):
        project = Path(__file__).resolve().parents[1]
        tools = ["schema_read", "memory_save", "memory_search", "work_list", "artifact_put", "artifact_get"]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "config.toml"
            config.write_text(
                f'workspace = {json.dumps(str(root / "work"))}\n'
                f'atlas = {json.dumps(str(root / "atlas"))}\n'
                'backend = "codex"\n', encoding="utf-8")
            ws = Workspace(root / "work")
            try:
                producer = ws.create_job("extractor", {}, nonce="host-mcp-producer")

                def bridge(job_id):
                    return MCPBridge([{
                        "name": "atlas", "transport": "stdio", "command": sys.executable,
                        "args": ["-m", "oracle_atlas", "mcp", "--config", str(config), "--job", job_id],
                        "env": {"PYTHONPATH": str(project / "src")},
                        "allowed_tools": tools, "timeout": 10,
                    }])

                def call(client, name, arguments):
                    reply = client.call("mcp__atlas__" + name, arguments)
                    self.assertFalse(reply.get("isError", False), reply)
                    blocks = [part["text"] for part in reply["content"] if part.get("type") == "text"]
                    self.assertEqual(len(blocks), 1)
                    return json.loads(blocks[0])

                private_note = "producer-private-proof-note-731"
                with bridge(producer) as client:
                    model_schema = call(client, "schema_read", {"kind": "checkpoint"})
                    self.assertEqual(model_schema["data"]["required"], ["summary", "refs", "remaining"])
                    created = call(client, "artifact_put", {
                        "kind": "checkpoint", "json_text": json.dumps({
                            "summary": "Formal checkpoint for a transport test", "refs": [], "remaining": []}),
                        "dependencies": [],
                    })
                    ref = created["ref"]
                    saved = call(client, "memory_save", {"text": private_note, "refs": [ref]})
                    self.assertTrue(saved["memory_id"])
                    notes = call(client, "memory_search", {"query": private_note, "limit": 10})["notes"]
                    self.assertEqual([n["text"] for n in notes], [private_note])
                    listing = call(client, "work_list", {"offset": 0, "limit": 10})
                    self.assertIn(ref, [item["ref"] for item in listing["items"]])

                reviewer = ws.create_job("profile_reviewer", {"material_refs": [ref]}, nonce="host-mcp-reviewer")
                reviewer_note = "reviewer-private-check-note-902"
                with bridge(reviewer) as client:
                    # Formal materials are readable, but material references must not propagate producer private sessions/notes.
                    formal = call(client, "artifact_get", {"ref": ref, "pointer": "", "offset": 0, "limit": 4000})
                    self.assertEqual(formal["data"]["summary"], "Formal checkpoint for a transport test")
                    hidden = call(client, "memory_search", {"query": private_note, "limit": 10})
                    self.assertEqual(hidden["notes"], [])
                    self.assertEqual(call(client, "work_list", {"offset": 0, "limit": 10})["items"], [])
                    denied = call(client, "artifact_put", {"kind": "profile", "json_text": "{}", "dependencies": []})
                    self.assertEqual(denied["error_type"], "ProtocolError")
                    self.assertIn("profile_reviewer is not authorized to write profile", denied["message"])
                    call(client, "memory_save", {"text": reviewer_note, "refs": [ref]})
                    own = call(client, "memory_search", {"query": "", "limit": 10})["notes"]
                    self.assertEqual([n["text"] for n in own], [reviewer_note])

                # After restarting the actual MCP process, this job's memory and formal artifacts remain recoverable.
                with bridge(producer) as client:
                    notes = call(client, "memory_search", {"query": "", "limit": 10})["notes"]
                    self.assertEqual([n["text"] for n in notes], [private_note])
                    listing = call(client, "work_list", {"offset": 0, "limit": 10})
                    self.assertEqual(listing["total"], 1)
                    self.assertEqual(listing["items"][0]["ref"], ref)

                self.assertEqual(ws.query("SELECT COUNT(*) AS n FROM artifacts WHERE kind='profile'")[0]["n"], 0)
                self.assertEqual(ws.query("SELECT COUNT(*) AS n FROM tool_calls WHERE status!='done'")[0]["n"], 0)
                self.assertGreaterEqual(ws.query("SELECT COUNT(*) AS n FROM tool_calls")[0]["n"], 12)
            finally:
                ws.close()


if __name__ == "__main__":
    unittest.main()
