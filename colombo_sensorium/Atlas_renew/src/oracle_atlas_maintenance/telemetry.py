"""Durable public metadata and monotonic stage control; never model content.

This module accepts only named counters, known lifecycle labels and hashed IDs.
An interval with no observable event is opaque: it cannot establish whether the
provider was reasoning, queued, or performing network work.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import threading
import time
import uuid

from oracle_atlas.discovery.http import atomic_write

HARD_CAP_SECONDS = 1800.0
_PUBLIC_TYPES = {"thread.started", "turn.started", "turn.completed", "turn.failed", "item.started", "item.updated", "item.completed", "error"}
_ITEM_KINDS = {"mcp_tool_call", "command_execution", "web_search", "agent_message", "todo_list", "file_change"}
_SAFE_TOOLS = {"profile_read", "artifact_read", "bibliography_search", "bibliography_read", "search_replace",
               "source_fetch", "source_read", "source_find", "failure_resolve", "maintenance_status", "checkpoint_save", "checkpoint_read", "handoff_validate",
               "research_scope_freeze", "research_scope_extend", "candidate_dispositions", "bibliography_lookup"}
_PHASES = {"stage", "instruction_loading", "request_serialization", "transport_wait", "process_spawn", "native_session",
           "output_validation", "audit_finalization", "tool_queue", "tool_execution", "tool_audit_persist", "result_persist"}
_ACTIONS = {"phase_started", "phase_finished", "public_event", "process_started", "process_exited", "process_terminated",
            "close_requested", "controller_checkpoint", "stage_failed", "stage_complete", "replay", "heartbeat", "monitor_failed"}
_USAGE = {"input_tokens", "output_tokens", "cached_input_tokens", "total_tokens"}


def _dump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _save(path, value):
    atomic_write(Path(path), _dump(value).encode())


def _load(path):
    return json.loads(Path(path).read_text("utf-8"))


def _stamp():
    return datetime.now(timezone.utc).isoformat()


def _numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def sanitize_public_event(event):
    """Copy only allowlisted event metadata; never stringify arbitrary provider data."""
    if not isinstance(event, dict):
        return {"event_type": "other"}
    kind = event.get("type")
    result = {"event_type": kind if isinstance(kind, str) and kind in _PUBLIC_TYPES else "other"}
    item = event.get("item") if isinstance(event.get("item"), dict) else {}
    if item:
        item_kind = item.get("type")
        result["item_kind"] = item_kind if isinstance(item_kind, str) and item_kind in _ITEM_KINDS else "opaque_item"
        if isinstance(item.get("id"), str):
            result["item_id_sha256"] = hashlib.sha256(item["id"].encode()).hexdigest()
        tool = item.get("tool")
        if isinstance(tool, str):
            result["tool"] = tool if tool in _SAFE_TOOLS else "unrecognized"
        status = item.get("status")
        if isinstance(status, str) and status in {"in_progress", "completed", "failed", "cancelled"}:
            result["item_status"] = status
    if kind == "turn.completed" and isinstance(event.get("usage"), dict):
        result["usage"] = {k: v for k, v in event["usage"].items() if k in _USAGE and _numeric(v) and v >= 0}
    return result


def create_run_control(path, *, stage_key, role, timeout_seconds=1800, close_reserve_seconds=120,
                       resume_binding=None, telemetry_path=None, clock_ns=None):
    clock_ns = clock_ns or time.monotonic_ns
    timeout = float(timeout_seconds)
    reserve = float(close_reserve_seconds)
    if not math.isfinite(timeout) or timeout <= 0 or not math.isfinite(reserve) or reserve < 0:
        raise ValueError("Stage timeout must be finite and positive; reserve must be finite and nonnegative")
    timeout = min(timeout, HARD_CAP_SECONDS)
    reserve = min(reserve, max(0.0, timeout / 2))
    started = clock_ns()
    value = {"schema_version": 1, "stage_key": stage_key, "role": role, "clock": "monotonic_ns",
             "created_at": _stamp(), "started_monotonic_ns": started,
             "soft_deadline_monotonic_ns": started + int((timeout - reserve) * 1e9),
             "hard_deadline_monotonic_ns": started + int(timeout * 1e9),
             "hard_cap_seconds": timeout, "close_reserve_seconds": reserve,
             "close_requested": False, "close_reason": None, "checkpoint_binding": resume_binding,
             "telemetry_path": str(telemetry_path) if telemetry_path else None}
    _save(path, value)
    return value


def read_run_control(path, *, clock_ns=None):
    if path is None or not Path(path).is_file():
        return {"available": False, "close_requested": False, "remaining_seconds": None}
    value = _load(path)
    now = (clock_ns or time.monotonic_ns)()
    deadline = value["hard_deadline_monotonic_ns"]
    soft = value["soft_deadline_monotonic_ns"]
    remaining = max(0.0, (deadline - now) / 1e9)
    return {**value, "available": True, "remaining_seconds": remaining,
            "soft_remaining_seconds": max(0.0, (soft - now) / 1e9),
            "hard_expired": now >= deadline,
            "close_requested": bool(value.get("close_requested") or now >= soft),
            "close_reason": "hard_timeout" if now >= deadline else value.get("close_reason") or ("reserve_reached" if now >= soft else None)}


def request_close(path, reason="reserve_reached"):
    value = _load(path)
    if not value.get("close_requested"):
        value.update(close_requested=True, close_reason=reason, close_requested_at=_stamp())
        _save(path, value)
    return read_run_control(path)


class PhaseTelemetry:
    def __init__(self, path, *, clock_ns=None):
        self.path = Path(path)
        self.status_path = self.path.with_name("live-status.json")
        self.clock_ns = clock_ns or time.monotonic_ns

    @contextmanager
    def _lock(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.with_suffix(".lock").open("a+") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)

    def emit(self, action, **metadata):
        if not isinstance(action, str) or action not in _ACTIONS:
            raise ValueError("Unknown public telemetry action")
        # Metadata strings are identifiers from finite vocabularies, never free text.
        safe = {}
        for key, value in metadata.items():
            if key == "phase" and isinstance(value, str) and value in _PHASES:
                safe[key] = value
            elif key == "tool" and isinstance(value, str) and value in _SAFE_TOOLS:
                safe[key] = value
            elif key in {"token", "item_id_sha256"} and isinstance(value, str) and len(value) <= 64 and all(c in "0123456789abcdef" for c in value):
                safe[key] = value
            elif key in {"elapsed_seconds", "pid", "returncode", "journal_records"} and _numeric(value):
                safe[key] = value
            elif key == "reason" and isinstance(value, str) and value in {"reserve_reached", "hard_timeout", "controller_stop", "unknown"}:
                safe[key] = value
            elif key == "public_event" and isinstance(value, dict):
                # Re-sanitize even if a caller supplies a dictionary with extra fields.
                safe[key] = {k: v for k, v in value.items() if k in {"event_type", "item_kind", "item_id_sha256", "tool", "item_status", "usage"}}
                safe[key] = sanitize_public_event({"type": safe[key].get("event_type"),
                    "item": {"type": safe[key].get("item_kind"), "tool": safe[key].get("tool"), "status": safe[key].get("item_status")},
                    "usage": safe[key].get("usage")}) | ({"item_id_sha256": value["item_id_sha256"]} if isinstance(value.get("item_id_sha256"), str) and len(value["item_id_sha256"]) == 64 and all(c in "0123456789abcdef" for c in value["item_id_sha256"]) else {})
        with self._lock():
            state = _load(self.status_path) if self.status_path.is_file() else {"schema_version": 1, "sequence": 0, "phase_totals_seconds": {}, "active_phases": {}, "inflight_tools": {}, "attribution": "Opaque gaps are unobserved; network, queueing and model computation cannot be separated from public event silence."}
            now = self.clock_ns()
            record = {"sequence": state["sequence"], "at": _stamp(), "monotonic_ns": now, "action": action, **safe}
            with self.path.open("a", encoding="utf-8") as stream:
                stream.write(_dump(record) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
            state["sequence"] += 1
            state["updated_at"] = record["at"]
            state["updated_monotonic_ns"] = now
            if action == "phase_started":
                state["active_phases"][safe["token"]] = {"phase": safe["phase"], "started_monotonic_ns": now, **({"tool": safe["tool"]} if "tool" in safe else {})}
                if safe.get("phase") == "tool_execution":
                    state["inflight_tools"][safe["token"]] = state["active_phases"][safe["token"]]
            elif action == "phase_finished":
                state["active_phases"].pop(safe.get("token"), None)
                state["inflight_tools"].pop(safe.get("token"), None)
                phase = safe.get("phase")
                if phase:
                    state["phase_totals_seconds"][phase] = state["phase_totals_seconds"].get(phase, 0.0) + safe.get("elapsed_seconds", 0.0)
            elif action == "public_event":
                state["last_public_event"] = safe.get("public_event", {})
                state["last_public_event_monotonic_ns"] = now
            elif action.startswith("process_"):
                state["process"] = {"state": action.removeprefix("process_"), **safe, "observed_monotonic_ns": now}
            elif action == "close_requested":
                state["close_requested"] = True
                state["close_reason"] = safe.get("reason", "unknown")
            elif action in {"stage_complete", "stage_failed"}:
                state["terminal_status"] = action.removeprefix("stage_")
            _save(self.status_path, state)
            return record

    def start_phase(self, phase, *, tool=None):
        token = uuid.uuid4().hex
        started = self.clock_ns()
        self.emit("phase_started", phase=phase, token=token, tool=tool)
        return phase, token, started

    def finish_phase(self, handle):
        phase, token, started = handle
        elapsed = max(0.0, (self.clock_ns() - started) / 1e9)
        self.emit("phase_finished", phase=phase, token=token, elapsed_seconds=elapsed)
        return elapsed

    @contextmanager
    def phase(self, name, *, tool=None):
        token = self.start_phase(name, tool=tool)
        try:
            yield
        finally:
            self.finish_phase(token)

    def snapshot(self):
        with self._lock():
            state = _load(self.status_path) if self.status_path.is_file() else {}
        now = self.clock_ns()
        if state.get("last_public_event_monotonic_ns") is not None:
            state["seconds_since_last_public_event"] = max(0, (now - state["last_public_event_monotonic_ns"]) / 1e9)
        for field in ("active_phases", "inflight_tools"):
            for row in state.get(field, {}).values():
                row["elapsed_seconds"] = max(0, (now - row["started_monotonic_ns"]) / 1e9)
        return state


class NativeMonitor:
    def __init__(self, stage, telemetry, control_path, *, poll_seconds=0.5):
        self.stage, self.telemetry, self.control_path = Path(stage), telemetry, Path(control_path)
        self.poll_seconds = max(0.05, min(float(poll_seconds), 5))
        self.offset = 0
        self._close_emitted = False
        self._stop = threading.Event()
        self.thread = None

    def tick(self):
        events = self.stage / "events.jsonl"
        if events.is_file():
            with events.open("rb") as stream:
                stream.seek(self.offset)
                while True:
                    start = stream.tell()
                    line = stream.readline()
                    if not line:
                        break
                    if not line.endswith(b"\n"):
                        stream.seek(start)
                        break
                    self.offset = stream.tell()
                    try:
                        event = json.loads(line)
                    except (ValueError, UnicodeDecodeError):
                        continue
                    if isinstance(event, dict):
                        self.telemetry.emit("public_event", public_event=sanitize_public_event(event))
        control = read_run_control(self.control_path)
        if control.get("close_requested") and not self._close_emitted:
            request_close(self.control_path, control.get("close_reason") or "reserve_reached")
            self.telemetry.emit("close_requested", reason=control.get("close_reason") or "reserve_reached")
            checkpoint = {"schema_version": 1, "unapproved": True, "writer": "controller", "kind": "public_observation_only",
                          "reason": "cooperative_close_requested", "stage_key": control.get("stage_key"),
                          "last_public_event": self.telemetry.snapshot().get("last_public_event"),
                          "tool_journal_path": str(self.stage / "tools-events.jsonl"),
                          "model_checkpoint_path": str(self.stage / "checkpoint.json"),
                          "scientific_conclusion": None}
            _save(self.stage / "controller-checkpoint.json", checkpoint)
            self.telemetry.emit("controller_checkpoint")
            self._close_emitted = True

    def record_failure(self, exc):
        """Observer failure is diagnostic only; never mask lifecycle/audit cleanup."""
        known = {"TypeError", "ValueError", "OSError", "FileNotFoundError", "PermissionError", "RuntimeError", "KeyError", "JSONDecodeError"}
        name = type(exc).__name__
        diagnostic = {"schema_version": 1, "observer_failed": True,
                      "error_type": name if name in known else "ObserverError",
                      "at": _stamp(), "contents_recorded": False,
                      "audit_or_scientific_approval_changed": False}
        try:
            _save(self.stage / "monitor-failure.json", diagnostic)
        except Exception:
            pass  # A broken diagnostics destination cannot prevent audit fencing.
        try:
            self.telemetry.emit("monitor_failed")
        except Exception:
            pass

    def start(self):
        def run():
            while not self._stop.wait(self.poll_seconds):
                try:
                    self.tick()
                except Exception as exc:
                    self.record_failure(exc)
                    return
        self.thread = threading.Thread(target=run, daemon=True, name="maintenance-public-event-monitor")
        self.thread.start()

    def stop(self):
        self._stop.set()
        try:
            if self.thread:
                self.thread.join(timeout=max(1, self.poll_seconds * 2))
        except Exception as exc:
            self.record_failure(exc)
        try:
            self.tick()
        except Exception as exc:
            self.record_failure(exc)
