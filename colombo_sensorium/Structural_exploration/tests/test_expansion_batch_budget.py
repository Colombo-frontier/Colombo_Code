"""Batch limits supplement candidate budgets without counting cached responses twice.

Tests use scripted transports and local tool stubs, not a real model or network.
"""
import json

import pytest

from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.store import dumps
from oracle_atlas.providers.base import Reply, ToolCall
from oracle_atlas.tools.host import function
from oracle_atlas.workflow.engine import Engine


def config(tmp_path, **expansion):
    return {"workspace": str(tmp_path / "work"), "atlas": str(tmp_path / "atlas"),
            "budgets": dict(DEFAULTS), "model": {}, "expansion": expansion}


class StopBackend:
    def __init__(self):
        self.calls = 0

    def complete(self, **request):
        self.calls += 1
        return Reply(text=dumps({"status": "needs_materials", "artifact_refs": [],
                                 "summary": "Synthetic budget test.", "checkpoint_ref": None}))


def job(engine, candidate_scope, batch_scope=None, revision=0):
    inputs = {"budget_scope": candidate_scope, "revision": revision}
    if batch_scope is not None:
        inputs["batch_scope"] = batch_scope
    return engine.ws.create_job("task_scout", inputs)


def test_batch_model_limit_counts_distinct_candidate_scopes(tmp_path):
    backend = StopBackend()
    engine = Engine(config(tmp_path, max_batch_model_calls=2), backend)
    try:
        first, second, third = [job(engine, f"candidate-{i}", "batch-a") for i in range(3)]
        assert engine.runner.run(first)["status"] == "needs_materials"
        assert engine.runner.run(second)["status"] == "needs_materials"
        blocked = engine.runner.run(third)
        assert blocked["status"] == "budget_exhausted"
        assert "batch provider-call budget" in blocked["state"]["last_error"]
        assert backend.calls == 2
        assert not engine.ws.query("SELECT id FROM calls WHERE job=?", (third,))
        # A different batch and the legacy no-batch path do not inherit this cap.
        assert engine.runner.run(job(engine, "other", "batch-b"))["status"] == "needs_materials"
        assert engine.runner.run(job(engine, "legacy"))["status"] == "needs_materials"
        assert backend.calls == 4
    finally:
        engine.ws.close()


def test_candidate_model_limit_still_applies_inside_batch(tmp_path):
    cfg = config(tmp_path, max_batch_model_calls=10)
    cfg["budgets"]["max_total_calls"] = 1
    backend = StopBackend()
    engine = Engine(cfg, backend)
    try:
        assert engine.runner.run(job(engine, "one-candidate", "batch"))["status"] == "needs_materials"
        result = engine.runner.run(job(engine, "one-candidate", "batch", revision=1))
        assert result["status"] == "budget_exhausted"
        assert "for this run" in result["state"]["last_error"]
        assert backend.calls == 1
        assert engine.runner.run(job(engine, "another-candidate", "batch"))["status"] == "needs_materials"
    finally:
        engine.ws.close()


def test_batch_model_limit_has_a_default_and_is_opt_in(tmp_path):
    backend = StopBackend()
    cfg = config(tmp_path)
    cfg.pop("expansion")
    engine = Engine(cfg, backend)
    try:
        assert engine.runner.run(job(engine, "candidate", "batch"))["status"] == "needs_materials"
        assert engine.runner.run(job(engine, "legacy"))["status"] == "needs_materials"
        assert backend.calls == 2
    finally:
        engine.ws.close()


def test_saved_response_recovers_when_batch_limit_is_already_reached(tmp_path, monkeypatch):
    class ProcessDeath(BaseException):
        pass

    backend = StopBackend()
    engine = Engine(config(tmp_path, max_batch_model_calls=1), backend)
    original_event = engine.ws.event

    def die_after_persistence(job_id, event, payload):
        if event == "model_response":
            raise ProcessDeath()
        return original_event(job_id, event, payload)

    try:
        jid = job(engine, "candidate", "batch")
        monkeypatch.setattr(engine.ws, "event", die_after_persistence)
        with pytest.raises(ProcessDeath):
            engine.runner.run(jid)
        assert backend.calls == 1
        assert engine.ws.query("SELECT status FROM calls WHERE job=?", (jid,))[0]["status"] == "response"
        monkeypatch.setattr(engine.ws, "event", original_event)
        assert engine.runner.run(jid)["status"] == "needs_materials"
        assert backend.calls == 1
    finally:
        engine.ws.close()


class BibliographyStub:
    def __init__(self):
        self.calls = 0

    def search(self, *args, **kwargs):
        self.calls += 1
        return {"records": [], "synthetic": True}


class BridgeStub:
    def __init__(self):
        self.calls = 0

    def tools(self):
        return [function("mcp_fixture_probe", "Local budget test only.", {})]

    def call(self, name, args):
        assert name == "mcp_fixture_probe"
        self.calls += 1
        return {"synthetic": True}


class OneToolBackend(StopBackend):
    def __init__(self, tool):
        super().__init__()
        self.tool = tool
        self.seen = set()
        self.outputs = []

    def complete(self, **request):
        self.calls += 1
        jid = json.loads(request["input_items"][0]["content"])["job_id"]
        if jid not in self.seen:
            self.seen.add(jid)
            args = ({"provider": "arxiv", "query": "synthetic", "year": None,
                     "limit": 1, "cursor": None} if self.tool == "bibliography_search" else {})
            call = ToolCall(self.tool, args, "external-once")
            return Reply(calls=[call], output_items=[{"type": "function_call", "call_id": call.call_id,
                                                     "name": call.name, "arguments": dumps(args)}])
        last = next(item for item in reversed(request["input_items"]) if item.get("type") == "function_call_output")
        self.outputs.append(json.loads(last["output"]))
        return Reply(text=dumps({"status": "needs_materials", "artifact_refs": [],
                                 "summary": "Synthetic tool budget test.", "checkpoint_ref": None}))


@pytest.mark.parametrize("tool", ["bibliography_search", "mcp_fixture_probe"])
def test_external_batch_cap_counts_current_registered_attempt_and_all_candidates(tmp_path, tool):
    bibliography = BibliographyStub()
    bridge = BridgeStub()
    backend = OneToolBackend(tool)
    engine = Engine(config(tmp_path, max_batch_external_calls=1), backend,
                    bibliography=bibliography, bridge=bridge)
    actual = bibliography if tool == "bibliography_search" else bridge
    try:
        assert engine.runner.run(job(engine, "candidate-a", "batch"))["status"] == "needs_materials"
        assert actual.calls == 1
        assert "error_type" not in backend.outputs[-1]
        assert engine.runner.run(job(engine, "candidate-b", "batch"))["status"] == "needs_materials"
        assert actual.calls == 1
        assert backend.outputs[-1]["error_type"] == "ProtocolError"
        assert "batch external-call budget" in backend.outputs[-1]["message"]
        # Two attempts are archived, but only the first reaches the external stub.
        assert len(engine.ws.query("SELECT id FROM tool_calls WHERE name=?", (tool,))) == 2
        assert engine.runner.run(job(engine, "candidate-c", "other-batch"))["status"] == "needs_materials"
        assert engine.runner.run(job(engine, "legacy"))["status"] == "needs_materials"
        assert actual.calls == 3
    finally:
        engine.ws.close()


def test_candidate_external_cap_still_applies_with_larger_batch_allowance(tmp_path):
    cfg = config(tmp_path, max_batch_external_calls=10)
    cfg["budgets"]["max_external_calls"] = 1
    bibliography = BibliographyStub()
    backend = OneToolBackend("bibliography_search")
    engine = Engine(cfg, backend, bibliography=bibliography)
    try:
        engine.runner.run(job(engine, "same-candidate", "batch"))
        engine.runner.run(job(engine, "same-candidate", "batch", revision=1))
        assert bibliography.calls == 1
        assert "for this round" in backend.outputs[-1]["message"]
    finally:
        engine.ws.close()
