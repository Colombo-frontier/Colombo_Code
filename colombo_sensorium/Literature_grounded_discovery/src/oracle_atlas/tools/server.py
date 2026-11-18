"""Local stdio MCP for Codex; shares ToolHost and the same role permissions with the API runner."""
from __future__ import annotations

import json
import uuid
import time

from jsonschema import Draft202012Validator
from ..atlas.store import Atlas
from ..core.store import Workspace, dumps
from ..core.contracts import ProtocolError, references, tool_error
from .host import ToolHost
from ..runtime.native_budget import BUDGET_REASON, reserve_call


async def serve(config: dict, job_id: str):
    try:
        from mcp.server import Server
        from mcp.server.stdio import stdio_server
        from mcp.types import Tool, TextContent
    except ImportError as exc:
        raise RuntimeError('Local MCP requires pip install ".[mcp]"') from exc
    ws=Workspace(config["workspace"]); atlas=Atlas(config["atlas"])
    job=ws.job(job_id); bridge=None
    if config.get("mcp"):
        from ..providers.mcp import MCPBridge
        bridge=MCPBridge(config["mcp"])
    host=ToolHost(ws,atlas,job,config,bridge=bridge)
    definitions=host.definitions(); defs={x["name"]:x for x in definitions}
    server=Server("oracle-atlas-"+job["role"])

    @server.list_tools()
    async def list_tools():
        return [Tool(name=x["name"],description=x["description"],inputSchema=x["parameters"]) for x in definitions]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        token="native-"+uuid.uuid4().hex
        started, monotonic_started = time.time(), time.monotonic()
        if not reserve_call(ws, job_id, token, name, arguments, config["budgets"]["max_turns"] * 8):
            return [TextContent(type="text", text=dumps({"error": BUDGET_REASON, "message": "Up to three reserved calls can save memory or an artifact_put checkpoint. If this ceiling prevents completion, return needs_materials with summary starting NATIVE_TOOL_BUDGET_EXHAUSTED. Report genuine missing scientific material separately."}))]
        try:
            if name not in defs:raise ProtocolError("Tool is not authorized")
            errors=list(Draft202012Validator(defs[name]["parameters"]).iter_errors(arguments))
            if errors:raise ProtocolError("; ".join(e.message for e in errors[:8]))
            result=host.call(name,arguments,token)
            if len(dumps(result))>config["budgets"]["max_tool_chars"]+2000:
                ref=ws.artifacts.put("external_result",{"tool":name,"result":result},job_id)
                host.grants.add(ref)
                result={"archived_result_ref":ref,"message":"Read in pages using artifact_get /result"}
        except Exception as exc:
            result=tool_error(exc)
        with ws.transaction() as db:
            db.execute("UPDATE tool_calls SET result=?,status='done' WHERE id=?",(dumps(result),token))
        ws.event(job_id, "native_tool_timing", {"call_id": token, "tool": name,
            "started_at_unix": started, "finished_at_unix": time.time(),
            "elapsed_seconds": time.monotonic() - monotonic_started,
            "scope": "One native MCP invocation, including any internal batch reads; excludes model and provider waiting.",
            "response_characters": len(dumps(result)), "error": isinstance(result, dict) and ("error_type" in result or "error" in result)})
        return [TextContent(type="text",text=dumps(result))]

    try:
        async with stdio_server() as (reader,writer):
            await server.run(reader,writer,server.create_initialization_options())
    finally:
        if bridge:bridge.close()
        ws.close()
