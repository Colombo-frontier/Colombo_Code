"""Thin OpenAI Responses API adapter. The runtime manages history, retries, caches, and budgets."""
from __future__ import annotations

import copy
import json
import os
from typing import Any

from .base import ProviderError, ProviderIncomplete, ProviderProtocolError, ProviderRefusal, Reply, ToolCall


def _jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json", exclude_none=True)
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return value


class ResponsesBackend:
    """config must specify a model; a client may be injected for offline transport tests."""
    def __init__(self, config: dict, *, client=None):
        self.config = dict(config)
        self.model = config.get("model")
        if not isinstance(self.model, str) or not self.model.strip():
            raise ProviderError("Specify an available OpenAI model ID in the configuration.")
        if client is not None:
            self.client = client
            return
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ProviderError('Optional dependency missing; run pip install ".[openai]".') from exc
        key_name = config.get("api_key_env", "OPENAI_API_KEY")
        api_key = os.environ.get(key_name)
        if not api_key:
            raise ProviderError(f"API key environment variable {key_name} is not set.")
        # The SDK does not resample independently. The runtime's durable receipt governs recovery of paid calls.
        kwargs = {"api_key": api_key, "timeout": float(config.get("timeout", 120)),
                  "max_retries": 0}
        if config.get("base_url"):
            kwargs["base_url"] = config["base_url"]
        if config.get("organization"):
            kwargs["organization"] = config["organization"]
        if config.get("project"):
            kwargs["project"] = config["project"]
        self.client = OpenAI(**kwargs)

    def complete(self, instructions: str, input_items: list,
                 tools: list, output_schema: dict) -> Reply:
        if not isinstance(output_schema, dict):
            raise ProviderError("output_schema must be a complete JSON Schema.")
        available_tools = copy.deepcopy(tools)
        web_search = self.config.get("web_search", False)
        if web_search and not any(t.get("type") == "web_search" for t in available_tools):
            options = web_search if isinstance(web_search, dict) else {}
            available_tools.append({**options, "type": "web_search"})
        kwargs = {
            "model": self.model,
            "instructions": instructions,
            "input": copy.deepcopy(input_items),
            "tools": available_tools,
            "text": {"format": {"type": "json_schema", "name": "agent_handoff",
                                 "strict": True, "schema": copy.deepcopy(output_schema)}},
            "max_output_tokens": int(self.config.get("max_output_tokens", 12000)),
            "parallel_tool_calls": False,
            "store": False,
        }
        if self.config.get("reasoning_effort"):
            kwargs["reasoning"] = {"effort": self.config["reasoning_effort"]}
        # Retain API-returned encrypted reasoning items in bounded store=False sessions; do not inspect or infer hidden reasoning.
        if self.config.get("encrypted_reasoning", True):
            kwargs["include"] = ["reasoning.encrypted_content"]
        raw = _jsonable(self.client.responses.create(**kwargs))
        if not isinstance(raw, dict):
            raise ProviderProtocolError("The Responses return value is not an object.")
        if raw.get("status") not in (None, "completed"):
            raise ProviderIncomplete(
                f"Responses status is {raw.get('status')}; archive and handle it before continuing.", raw)
        output = raw.get("output", [])
        if not isinstance(output, list):
            raise ProviderProtocolError("Responses.output is not a list.", raw)
        calls, texts = [], []
        for item in output:
            if not isinstance(item, dict):
                raise ProviderProtocolError("Responses.output contains a non-object item.", raw)
            if item.get("type") == "function_call":
                try:
                    args = item.get("arguments", "{}")
                    args = json.loads(args) if isinstance(args, str) else args
                    if not isinstance(args, dict):
                        raise ValueError("arguments is not an object")
                    if not item.get("call_id") or not item.get("name"):
                        raise ValueError("missing call_id or name")
                except (ValueError, TypeError) as exc:
                    raise ProviderProtocolError("Function-call arguments are not a valid JSON object.", raw) from exc
                calls.append(ToolCall(item["name"], args, item["call_id"]))
            elif item.get("type") == "message":
                for part in item.get("content", []):
                    if part.get("type") == "output_text":
                        texts.append(part.get("text", ""))
                    elif part.get("type") == "refusal":
                        # Refusal is not a formatting error; do not automatically repeat paid sampling.
                        raise ProviderRefusal("The model returned a refusal; no automatic resampling.", raw)
        usage = raw.get("usage")
        return Reply(output_items=output, calls=calls, text="\n".join(texts),
                     usage=usage if isinstance(usage, dict) else None,
                     response_id=raw.get("id"))

    def close(self) -> None:
        close = getattr(self.client, "close", None)
        if close:
            close()
