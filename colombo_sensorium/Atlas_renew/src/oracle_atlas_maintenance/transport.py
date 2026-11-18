"""Spawn-isolated Responses transport with a parent-owned monotonic deadline.

Only bounded JSON crosses back from the worker. Provider text remains in the
ordinary private Reply archive; errors expose an allowlisted type, never a body.
Process termination cannot establish whether a remote paid request completed.
"""
from __future__ import annotations

from dataclasses import asdict
import json
import math
import multiprocessing
import os
from pathlib import Path
import tempfile
import time

from oracle_atlas.providers.base import Reply, ToolCall


MAX_REPLY_BYTES = 8 * 1024 * 1024
POLL_SECONDS = 0.025
TERMINATE_GRACE_SECONDS = 0.2
KILL_GRACE_SECONDS = 0.5
_ERROR_TYPES = frozenset({"TimeoutError", "ConnectionError", "ValueError", "TypeError",
                          "ProviderError", "ProviderProtocolError", "ProviderIncomplete", "ProviderRefusal"})


class TransportError(RuntimeError):
    """Safe process/transport classification, with no provider response body."""
    def __init__(self, error_type="WorkerError"):
        self.error_type = error_type
        super().__init__("Isolated Responses transport failed: " + error_type)


class TransportDeadlineExceeded(TransportError):
    def __init__(self):
        super().__init__("DeadlineExceeded")


def _vendor_complete(model_cfg, payload):
    from oracle_atlas.providers.responses import ResponsesBackend
    backend = ResponsesBackend(model_cfg)
    try:
        return backend.complete(**payload)
    finally:
        if hasattr(backend, "close"):
            backend.close()


def _write_envelope(path, envelope):
    # Atomic file IPC avoids an unbounded recv waiting on a partial pipe frame.
    temporary = path + ".tmp"
    size = 0
    try:
        with open(temporary, "xb") as stream:
            for chunk in json.JSONEncoder(ensure_ascii=False, separators=(",", ":"), allow_nan=False).iterencode(envelope):
                encoded = chunk.encode("utf-8")
                size += len(encoded)
                if size > MAX_REPLY_BYTES:
                    raise OverflowError("Bounded IPC reply exceeded")
                stream.write(encoded)
            stream.flush()
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def _worker(path, model_cfg, payload, target):
    try:
        reply = (target or _vendor_complete)(model_cfg, payload)
        if not isinstance(reply, Reply):
            raise TypeError("Worker did not return Reply")
        _write_envelope(path, {"status": "completed", "reply": asdict(reply)})
    except BaseException as exc:
        kind = type(exc).__name__
        safe = "ReplyTooLarge" if isinstance(exc, OverflowError) else kind if kind in _ERROR_TYPES else "WorkerError"
        try:
            _write_envelope(path, {"status": "error", "error_type": safe})
        except BaseException:
            pass  # Parent treats a missing envelope as uncertain worker failure.


def _stop(process):
    """Bound cleanup separately from the paid-call deadline."""
    if process.is_alive():
        process.terminate()
        process.join(TERMINATE_GRACE_SECONDS)
    if process.is_alive():
        process.kill()
        process.join(KILL_GRACE_SECONDS)
    if process.is_alive():
        raise TransportError("WorkerCleanupFailed")
    process.join(timeout=0)


def _reply(value):
    if not isinstance(value, dict) or set(value) != {"output_items", "calls", "text", "usage", "response_id"}:
        raise TransportError("InvalidReply")
    if not isinstance(value["output_items"], list) or any(not isinstance(row, dict) for row in value["output_items"]) or \
            not isinstance(value["calls"], list) or not isinstance(value["text"], str) or \
            value["usage"] is not None and not isinstance(value["usage"], dict) or \
            value["response_id"] is not None and not isinstance(value["response_id"], str):
        raise TransportError("InvalidReply")
    calls = []
    for item in value["calls"]:
        if not isinstance(item, dict) or set(item) != {"name", "arguments", "call_id"} or \
                not isinstance(item["name"], str) or not isinstance(item["arguments"], dict) or not isinstance(item["call_id"], str):
            raise TransportError("InvalidReply")
        calls.append(ToolCall(**item))
    return Reply(**{**value, "calls": calls})


def transport_call(model_cfg, payload, remaining_seconds, worker_target=None):
    """Return one Reply or stop its worker by deadline; never retry a paid call.

    ``worker_target`` is a top-level picklable pure fake for local spawn tests.
    The normal target uses the original dependency transport and model selection.
    """
    if isinstance(remaining_seconds, bool) or not isinstance(remaining_seconds, (int, float)) or \
            not math.isfinite(remaining_seconds) or remaining_seconds <= 0:
        raise TransportDeadlineExceeded()
    deadline = time.monotonic() + remaining_seconds
    configured = dict(model_cfg)
    timeout = float(configured.get("timeout", 120))
    if not math.isfinite(timeout) or timeout <= 0:
        raise TransportError("InvalidTimeout")
    configured["timeout"] = min(timeout, remaining_seconds)
    context = multiprocessing.get_context("spawn")
    with tempfile.TemporaryDirectory(prefix="atlas-responses-") as directory:
        path = Path(directory) / "reply.json"
        process = context.Process(target=_worker, args=(str(path), configured, payload, worker_target), daemon=True)
        started = False
        try:
            process.start()
            started = True
            while process.is_alive():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TransportDeadlineExceeded()
                process.join(timeout=min(POLL_SECONDS, remaining))
            if time.monotonic() >= deadline:
                raise TransportDeadlineExceeded()
            if process.exitcode != 0 or not path.is_file():
                raise TransportError("WorkerExited")
            with path.open("rb") as stream:
                raw = stream.read(MAX_REPLY_BYTES + 1)
            if len(raw) > MAX_REPLY_BYTES:
                raise TransportError("ReplyTooLarge")
            try:
                envelope = json.loads(raw)
            except (ValueError, UnicodeError, RecursionError) as exc:
                raise TransportError("InvalidReply") from exc
            if not isinstance(envelope, dict):
                raise TransportError("InvalidReply")
            if envelope.get("status") != "completed":
                kind = envelope.get("error_type")
                raise TransportError(kind if isinstance(kind, str) and (kind in _ERROR_TYPES or kind == "ReplyTooLarge") else "WorkerError")
            result = _reply(envelope.get("reply"))
            if time.monotonic() >= deadline:
                raise TransportDeadlineExceeded()
            return result
        except (TransportError, KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:
            raise TransportError("WorkerStartFailed" if not started else "WorkerError") from exc
        finally:
            if started:
                _stop(process)
                process.close()
