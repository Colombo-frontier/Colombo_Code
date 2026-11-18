"""Offline tests of actual provider protocols; these are not scientific acceptance by a real LLM."""
from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import socket
import subprocess
import time
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from oracle_atlas.providers.base import ProviderError, ProviderIncomplete, ProviderProtocolError, ProviderRefusal
from oracle_atlas.providers.responses import ResponsesBackend
from oracle_atlas.providers.mcp import MCPBridge, MCPError


class FakeResponses:
    def __init__(self, payload):
        self.payload = payload
        self.requests = []
    def create(self, **kwargs):
        self.requests.append(kwargs)
        return self.payload


def backend(payload, **config):
    response_api = FakeResponses(payload)
    b = ResponsesBackend({"model": "explicit-test-model", **config}, client=SimpleNamespace(responses=response_api))
    return b, response_api


SCHEMA = {"type": "object", "properties": {"status": {"type": "string"}},
          "required": ["status"], "additionalProperties": False}


class ResponseTests(unittest.TestCase):
    def test_structured_schema_and_encrypted_history_are_not_dropped(self):
        reasoning = {"type": "reasoning", "id": "rs_1", "encrypted_content": "opaque", "summary": []}
        payload = {"id": "resp_1", "status": "completed", "output": [reasoning,
                   {"type": "function_call", "name": "artifact_get", "call_id": "call_1", "arguments": '{"ref":"x"}'}],
                   "usage": {"input_tokens": 12, "output_tokens": 4}}
        b, api = backend(payload)
        reply = b.complete("rules", [{"role": "user", "content": "job"}], [], SCHEMA)
        self.assertEqual(reply.calls[0].arguments, {"ref": "x"})
        self.assertEqual(reply.output_items[0], reasoning)
        self.assertEqual(reply.usage["input_tokens"], 12)
        req = api.requests[0]
        self.assertEqual(req["text"]["format"]["schema"], SCHEMA)
        self.assertTrue(req["text"]["format"]["strict"])
        self.assertFalse(req["store"])
        self.assertNotIn("previous_response_id", req)
        self.assertEqual(req["include"], ["reasoning.encrypted_content"])

    def test_final_text_and_unknown_usage(self):
        b, _ = backend({"output": [{"type": "message", "content": [{"type": "output_text", "text": '{"status":"complete"}'}]}]})
        reply = b.complete("", [], [], SCHEMA)
        self.assertEqual(json.loads(reply.text)["status"], "complete")
        self.assertIsNone(reply.usage)

    def test_refusal_not_protocol_retry(self):
        b, _ = backend({"output": [{"type": "message", "content": [{"type": "refusal", "refusal": "declined"}]}]})
        with self.assertRaises(ProviderRefusal) as error:
            b.complete("", [], [], SCHEMA)
        self.assertNotIsInstance(error.exception, ProviderProtocolError)
        self.assertIn("output", error.exception.raw_response)

    def test_invalid_call_has_raw_paid_response(self):
        b, _ = backend({"id": "paid", "output": [{"type": "function_call", "name": "read", "call_id": "c", "arguments": "{"}]})
        with self.assertRaises(ProviderProtocolError) as err:
            b.complete("", [], [], SCHEMA)
        self.assertEqual(err.exception.raw_response["id"], "paid")

    def test_incomplete_is_not_valid_handoff(self):
        b, _ = backend({"id": "partial", "status": "incomplete", "output": []})
        with self.assertRaises(ProviderIncomplete):
            b.complete("", [], [], SCHEMA)

    def test_model_explicit_and_web_search_separate(self):
        with self.assertRaises(ProviderError):
            ResponsesBackend({}, client=object())
        b, api = backend({"output": []}, web_search=True)
        tools = [{"type": "function", "name": "read", "parameters": {"type": "object"}, "strict": False}]
        b.complete("", [], tools, SCHEMA)
        self.assertEqual(len(api.requests[0]["tools"]), 2)
        self.assertEqual(len(tools), 1)


class FakeSession:
    async def call_tool(self, name, arguments):
        return {"isError": False, "structuredContent": {"name": name, "arguments": arguments}}


class LifecycleBridge(MCPBridge):
    async def _connect(self, stack):
        self.open_task = asyncio.current_task()
        self.close_task = None
        async def cleanup():
            self.close_task = asyncio.current_task()
        stack.push_async_callback(cleanup)
        self._sessions["test"] = FakeSession()
        self._names = {"mcp__test__echo": ("test", "echo")}
        self._definitions = [{"name": "mcp__test__echo", "type": "function", "parameters": {"type": "object"}, "strict": False}]


class MCPTests(unittest.TestCase):
    def test_allowlist_mandatory_and_no_wildcard(self):
        for allow in (None, ["*"]):
            with self.assertRaises(MCPError):
                MCPBridge([{"name": "test", "command": "example", "allowed_tools": allow}])

    def test_lifetime_and_tool_deny(self):
        bridge = LifecycleBridge([{"name": "test", "command": "unused", "allowed_tools": ["echo"]}])
        self.assertEqual(bridge.tools()[0]["name"], "mcp__test__echo")
        self.assertEqual(bridge.call("mcp__test__echo", {"x": 3})["structuredContent"]["arguments"], {"x": 3})
        with self.assertRaises(MCPError):
            bridge.call("mcp__test__delete", {})
        bridge.close()
        self.assertIs(bridge.open_task, bridge.close_task)
        with self.assertRaises(MCPError):
            bridge.tools()
        bridge.close()  # Idempotent close

    def test_empty_bridge_needs_no_sdk(self):
        with MCPBridge([]) as bridge:
            self.assertEqual(bridge.tools(), [])

    @unittest.skipUnless(importlib.util.find_spec("mcp"), "Optional MCP SDK is not installed; this is an explicit integration-test gap")
    def test_real_sdk_stdio_local_tool(self):
        with tempfile.TemporaryDirectory() as tmp:
            server = Path(tmp) / "server.py"
            server.write_text('from mcp.server.fastmcp import FastMCP\n'
                              'm = FastMCP("fixture")\n'
                              '@m.tool()\ndef echo(text: str) -> str:\n    return text\n'
                              'if __name__ == "__main__": m.run()\n')
            with MCPBridge([{"name": "local", "command": sys.executable, "args": [str(server)],
                             "allowed_tools": ["echo"], "timeout": 10}]) as bridge:
                result = bridge.call(bridge.tools()[0]["name"], {"text": "offline-local-test"})
                self.assertFalse(result.get("isError", False))
                self.assertIn("offline-local-test", json.dumps(result))


    @unittest.skipUnless(importlib.util.find_spec("mcp"), "Optional MCP SDK is not installed")
    def test_real_sdk_streamable_http_local_tool(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
        with tempfile.TemporaryDirectory() as tmp:
            server = Path(tmp) / "http_server.py"
            server.write_text('from mcp.server.fastmcp import FastMCP\n'
                              f'm = FastMCP("fixture", host="127.0.0.1", port={port}, log_level="ERROR")\n'
                              '@m.tool()\ndef echo(text: str) -> str:\n    return text\n'
                              'if __name__ == "__main__": m.run(transport="streamable-http")\n')
            process = subprocess.Popen([sys.executable, str(server)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                for _ in range(100):
                    try:
                        with socket.create_connection(("127.0.0.1", port), timeout=.1):
                            break
                    except OSError:
                        if process.poll() is not None:
                            self.fail("local HTTP MCP server exited")
                        time.sleep(.05)
                else:
                    self.fail("local HTTP MCP server did not start")
                with MCPBridge([{"name": "http", "transport": "http", "url": f"http://127.0.0.1:{port}/mcp",
                                 "allowed_tools": ["echo"], "timeout": 10, "trust_env": False}]) as bridge:
                    result = bridge.call(bridge.tools()[0]["name"], {"text": "local-http-test"})
                    self.assertIn("local-http-test", json.dumps(result))
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


if __name__ == "__main__":
    unittest.main()
