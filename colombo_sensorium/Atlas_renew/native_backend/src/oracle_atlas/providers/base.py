"""Minimal model transport boundary; it contains neither scientific judgments nor workflow state."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]
    call_id: str


@dataclass(frozen=True)
class Reply:
    output_items: list[dict[str, Any]] = field(default_factory=list)
    calls: list[ToolCall] = field(default_factory=list)
    text: str = ""
    usage: dict[str, Any] | None = None
    response_id: str | None = None


class Backend(Protocol):
    def complete(self, instructions: str, input_items: list,
                 tools: list, output_schema: dict) -> Reply: ...


class ProviderError(RuntimeError):
    """Reportable transport or configuration error; the message contains no credentials."""


class ProviderProtocolError(ProviderError):
    """A response was obtained but cannot be decoded. Archive raw_response before protocol repair."""
    def __init__(self, message: str, raw_response: dict | None = None):
        super().__init__(message)
        self.raw_response = raw_response


class ProviderIncomplete(ProviderProtocolError):
    """An incomplete response was returned; it must not be represented as a valid handoff."""


class ProviderRefusal(ProviderError):
    """Model refusal is distinct from formatting failure and does not trigger automatic protocol repair."""
    def __init__(self, message: str, raw_response: dict | None = None):
        super().__init__(message)
        self.raw_response = raw_response
