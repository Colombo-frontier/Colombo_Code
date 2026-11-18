"""Integrate explicitly permitted MCP tools into the unified tool loop.

The same worker task opens, calls, and closes all async contexts, avoiding exit from an AnyIO
cancel scope across tasks. Instructions in tool descriptions are not executed, and unlisted tools are not automatically approved.
"""
from __future__ import annotations

import asyncio
import copy
import hashlib
import json
import os
import queue
import re
import threading
from concurrent.futures import Future, TimeoutError as FutureTimeout
from contextlib import AsyncExitStack
from datetime import timedelta
from urllib.parse import urlparse

from .base import ProviderError


class MCPError(ProviderError):
    pass


def _dump(obj):
    return obj.model_dump(mode="json", by_alias=True, exclude_none=True) if hasattr(obj, "model_dump") else obj


def _function_name(server: str, tool: str) -> str:
    raw = f"mcp__{server}__{tool}"
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", raw)
    if safe != raw or len(safe) > 64:
        safe = safe[:51] + "_" + hashlib.sha256(raw.encode()).hexdigest()[:12]
    return safe


class MCPBridge:
    """Each instance exclusively owns its client sessions; the component shutdown path must call close.

    Each config entry requires name, transport, and allowed_tools. stdio requires command/args;
    http requires url. headers_env maps HTTP header names to environment variable names to keep plaintext secrets out of configuration.
    """
    def __init__(self, config: list):
        self.config = copy.deepcopy(config)
        self._validate()
        self._queue: queue.Queue = queue.Queue()
        self._ready: Future = Future()
        self._thread: threading.Thread | None = None
        self._start_lock = threading.Lock()
        self._closed = False
        self._definitions: list[dict] = []
        self._names: dict[str, tuple[str, str]] = {}
        self._sessions: dict = {}
        self._timeouts = {c["name"]: float(c.get("timeout", 45)) for c in self.config}

    def _validate(self):
        if not isinstance(self.config, list):
            raise MCPError("MCP configuration must be a list.")
        seen = set()
        for entry in self.config:
            if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
                raise MCPError("Each MCP server requires a string name.")
            if not entry["name"] or entry["name"] in seen:
                raise MCPError("MCP name is empty or duplicated.")
            seen.add(entry["name"])
            allowed = entry.get("allowed_tools", entry.get("allow_tools"))
            if not isinstance(allowed, list) or not all(isinstance(x, str) and x for x in allowed):
                raise MCPError(f"MCP {entry['name']} requires an explicit allowed_tools list; implicit unrestricted access is not permitted.")
            if "*" in allowed:
                raise MCPError("MCP allowed_tools does not accept *; list tool names explicitly.")
            entry["allowed_tools"] = sorted(set(allowed))
            transport = entry.get("transport", "stdio")
            if transport == "stdio":
                if not isinstance(entry.get("command"), str) or not entry["command"]:
                    raise MCPError("stdio MCP requires command.")
                if not isinstance(entry.get("args", []), list):
                    raise MCPError("MCP args must be a list of strings.")
            elif transport in ("http", "streamable_http"):
                parsed = urlparse(entry.get("url", ""))
                if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username:
                    raise MCPError("HTTP MCP requires an http(s) URL without userinfo.")
            else:
                raise MCPError("MCP transport supports only stdio or http/streamable_http.")
            if float(entry.get("timeout", 45)) <= 0:
                raise MCPError("MCP timeout must be positive.")

    def _ensure_started(self):
        with self._start_lock:
            if self._closed:
                raise MCPError("MCPBridge is closed.")
            if self._thread is None:
                self._thread = threading.Thread(target=self._thread_main, name="atlas-mcp", daemon=True)
                self._thread.start()
        try:
            self._ready.result(timeout=sum(self._timeouts.values()) + 10)
        except FutureTimeout as exc:
            raise MCPError("MCP initialization timed out; tool calls were not retried.") from exc

    def _thread_main(self):
        try:
            asyncio.run(self._serve())
        except BaseException as exc:
            wrapped = MCPError(f"MCP session failed: {type(exc).__name__}.")
            wrapped.__cause__ = exc
            if not self._ready.done():
                self._ready.set_exception(wrapped)
            # Wake requests not yet consumed. Do not automatically resend when the call outcome is unknown.
            while True:
                try:
                    _, _, future = self._queue.get_nowait()
                except queue.Empty:
                    break
                if not future.done():
                    future.set_exception(wrapped)

    async def _serve(self):
        async with AsyncExitStack() as stack:
            await self._connect(stack)
            self._ready.set_result(True)
            while True:
                action, payload, future = await asyncio.to_thread(self._queue.get)
                if action == "close":
                    if not future.done():
                        future.set_result(None)
                    break
                if future.cancelled():
                    continue
                try:
                    result = await self._dispatch(action, payload)
                    if not future.done():
                        future.set_result(result)
                except Exception as exc:
                    if not future.done():
                        if isinstance(exc, MCPError):
                            future.set_exception(exc)
                        else:
                            future.set_exception(MCPError(f"MCP tool call failed: {type(exc).__name__}."))
        # All transports/contexts exit in the same task that created them.

    async def _connect(self, stack):
        if not any(c["allowed_tools"] for c in self.config):
            return
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
            from mcp.client import streamable_http as http_transport
        except ImportError as exc:
            raise MCPError('MCP 1.x SDK is missing; run pip install ".[mcp]".') from exc
        for entry in self.config:
            if not entry["allowed_tools"]:
                continue
            timeout = self._timeouts[entry["name"]]
            if entry.get("transport", "stdio") == "stdio":
                env = {k: os.environ[k] for k in entry.get("env_passthrough", []) if k in os.environ}
                env.update(entry.get("env", {}))
                params = StdioServerParameters(command=entry["command"], args=entry.get("args", []),
                                                env=env or None, cwd=entry.get("cwd"))
                streams = await stack.enter_async_context(stdio_client(params))
                read, write = streams[0], streams[1]
            else:
                headers = dict(entry.get("headers", {}))
                for header, env_name in entry.get("headers_env", {}).items():
                    if env_name not in os.environ:
                        raise MCPError(f"MCP credential environment variable {env_name} is not set.")
                    headers[header] = os.environ[env_name]
                import httpx
                # Supported by older and newer 1.x SDKs; an explicit client also lets local services avoid inheriting proxy settings.
                def make_http_client(**options):
                    options["trust_env"] = entry.get("trust_env", True)
                    return httpx.AsyncClient(**options)
                if hasattr(http_transport, "streamable_http_client"):
                    client = await stack.enter_async_context(make_http_client(
                        headers=headers or None, timeout=httpx.Timeout(timeout), follow_redirects=True))
                    connector = http_transport.streamable_http_client(entry["url"], http_client=client)
                else:
                    connector = http_transport.streamablehttp_client(
                        entry["url"], headers=headers or None, timeout=timedelta(seconds=timeout),
                        sse_read_timeout=timedelta(seconds=timeout), httpx_client_factory=make_http_client)
                streams = await stack.enter_async_context(connector)
                read, write = streams[0], streams[1]
            session = await stack.enter_async_context(
                ClientSession(read, write, read_timeout_seconds=timedelta(seconds=timeout)))
            await asyncio.wait_for(session.initialize(), timeout=timeout)
            self._sessions[entry["name"]] = session
            found, cursor = set(), None
            # Paginate MCP tools/list to avoid silently omitting tools after the first page.
            for _ in range(100):
                page = _dump(await asyncio.wait_for(session.list_tools(cursor=cursor), timeout=timeout))
                for tool in page.get("tools", []):
                    tool = _dump(tool)
                    if tool.get("name") not in entry["allowed_tools"]:
                        continue
                    found.add(tool["name"])
                    function_name = _function_name(entry["name"], tool["name"])
                    if function_name in self._names:
                        raise MCPError("MCP tool function names conflict.")
                    schema = tool.get("inputSchema", tool.get("input_schema", {}))
                    if not isinstance(schema, dict) or schema.get("type", "object") != "object":
                        raise MCPError("MCP inputSchema must describe a JSON object.")
                    self._names[function_name] = (entry["name"], tool["name"])
                    self._definitions.append({"type": "function", "name": function_name,
                        "description": str(tool.get("description", ""))[:4000],
                        "parameters": schema, "strict": False})
                next_cursor = page.get("nextCursor", page.get("next_cursor"))
                if not next_cursor:
                    break
                if next_cursor == cursor:
                    raise MCPError("MCP tools/list returned a duplicate cursor.")
                cursor = next_cursor
            else:
                raise MCPError("MCP tools/list exceeded the page limit.")
            missing = set(entry["allowed_tools"]) - found
            if missing:
                raise MCPError(f"MCP {entry['name']} did not provide configured tools: {', '.join(sorted(missing))}.")

    async def _dispatch(self, action, payload):
        if action != "call":
            raise MCPError("Unknown MCP bridge action.")
        name, args = payload
        server_name, tool_name = self._names[name]
        try:
            result = await asyncio.wait_for(
                self._sessions[server_name].call_tool(tool_name, arguments=args),
                timeout=self._timeouts[server_name])
        except asyncio.TimeoutError as exc:
            raise MCPError("MCP call timed out; the outcome is unknown and the call will not be automatically resent.") from exc
        # Preserve isError, structuredContent, and source links; ToolHost archives them and bounds context size.
        return _dump(result)

    def tools(self) -> list[dict]:
        self._ensure_started()
        return copy.deepcopy(self._definitions)

    def call(self, name: str, args: dict):
        self._ensure_started()
        if name not in self._names:
            raise MCPError("The tool is not on the current MCP allowlist.")
        if not isinstance(args, dict):
            raise MCPError("MCP arguments must be a JSON object.")
        if self._thread is None or not self._thread.is_alive():
            raise MCPError("The MCP session has terminated; reconnect explicitly.")
        future: Future = Future()
        self._queue.put(("call", (name, copy.deepcopy(args)), future))
        server, _ = self._names[name]
        try:
            return future.result(timeout=self._timeouts[server] + 10)
        except FutureTimeout as exc:
            future.cancel()
            raise MCPError("MCP worker timed out; the outcome is unknown and the call will not be automatically resent.") from exc

    def close(self):
        with self._start_lock:
            if self._closed:
                return
            self._closed = True
            thread = self._thread
        if thread is None:
            return
        if thread.is_alive():
            future: Future = Future()
            self._queue.put(("close", None, future))
            try:
                future.result(timeout=max(self._timeouts.values(), default=1) + 10)
            except (FutureTimeout, MCPError):
                pass
            thread.join(timeout=10)
            if thread.is_alive():
                raise MCPError("MCP shutdown is incomplete; background calls may still be finishing.")

    def __enter__(self):
        self._ensure_started()
        return self

    def __exit__(self, *_):
        self.close()
