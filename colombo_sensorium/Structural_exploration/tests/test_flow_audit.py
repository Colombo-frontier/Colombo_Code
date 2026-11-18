"""Independent forward audit of handoffs, recovery, authorization, and budgets without fabricating mathematical acceptance.

State-machine tests substitute fixed, schema-valid synthetic artifacts for completed model stages;
runner tests use a controlled transport to reproduce process interruption after persistence. These are not scientific acceptance
of actual paper research, real online models, or formal Atlas ingestion.
"""
from copy import deepcopy
import json

import pytest

from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.core.store import Workspace, digest, dumps
from oracle_atlas.providers.base import Reply, ToolCall
from oracle_atlas.runtime.runner import AgentRunner
from oracle_atlas.tools.host import ToolHost
from oracle_atlas.workflow.engine import Engine
from science_test_helpers import routing_joint_review
from test_atlas import profile as synthetic_profile, _SYNTHETIC


AXES = ("task", "model", "oracle", "algorithms", "output", "metric", "guarantee", "resource")


class NeverBackend:
    def complete(self, **request):
        raise AssertionError("State-machine tests must not request a real model")


@pytest.fixture
def engine(tmp_path):
    cfg = {"workspace": str(tmp_path / "work"), "atlas": str(tmp_path / "atlas"),
           "budgets": dict(DEFAULTS), "model": {}, "tasks": []}
    value = Engine(cfg, NeverBackend())
    yield value
    value.ws.close()


def candidate(engine, paper_ref, cid="candidate-a", *, revision=0):
    data = {"candidate_id": cid, "title": f"Protocol fixture revision {revision}",
            "paper_refs": [paper_ref],
            "common_specification": {a: {"summary": "Unassessed synthetic fixture.", "statements": []} for a in AXES},
            "views": [], "issues": [],
            "tag_facts": [{"concept_id": a.upper() + ":unknown", "axis": a.upper(),
                           "value": "unknown", "object_ref": None, "view_ref": None,
                           "operation_ref": None, "source_pointer": "/common_specification/" + a + "/summary",
                           "status": "unknown"} for a in AXES]}
    return engine.put("candidate", data)


def review(engine, subject_ref, review_type, verdict="approve", *, assessments=(), issues=()):
    return engine.put("review", {"subject_ref": subject_ref, "review_type": review_type,
                                "verdict": verdict, "assessments": list(assessments),
                                "issues": list(issues), "approved_bound_ids": [],
                                "summary": "Synthetic routing decision; no mathematical acceptance.",
                                **({"joint_review": routing_joint_review("approve" if verdict == "approve" else "defer")}
                                   if review_type == "profile" else {})})


def seed(engine, *, extraction_verdict="approve", persist=True):
    paper_ref = engine.put("paper", {"title": "Synthetic protocol fixture", "doi": None,
                                    "arxiv_id": None, "urls": [], "publication_events": [], "provenance": []})
    cref = candidate(engine, paper_ref)
    eref = engine.put("extraction", {"paper_ref": paper_ref, "candidate_refs": [cref]})
    rref = review(engine, eref, "extraction", extraction_verdict,
                  assessments=[{"subject_id": "candidate-a", "verdict": extraction_verdict, "reason": "Routing fixture."}])
    cid = digest({"paper": paper_ref, "candidate_id": "candidate-a"})[:24]
    case = {"case_id": cid, "paper_ref": paper_ref, "candidate_ref": cref,
            "extraction_ref": eref, "extraction_review_ref": rref,
            "budget_scope": "audit-scope", "state": "extraction_" + extraction_verdict,
            "history": [], "jobs": {}}
    if persist:
        engine.ws.save_case(case)
    return case


def identity(engine, case, decision="new"):
    retrieval_ref = engine.put("retrieval", {"candidate_ref": case["candidate_ref"],
                                            "inventory_version": engine.atlas.version(), "broaden": True})
    return engine.put("identity", {"candidate_ref": case["candidate_ref"], "decision": decision,
                                   "setting_id": None if decision == "unresolved" else "AUDIT_FIXTURE",
                                   "view_mapping": [], "normalization": "Synthetic routing fixture.",
                                   "comparisons": [], "retrieval_ref": retrieval_ref,
                                   "recall_audit": {"strategies": ["fixture-one", "fixture-two"],
                                                    "unresolved_ids": [], "reason": "No scientific assertion.",
                                                    "inventory_version": engine.atlas.version()}, "issues": []})


def completed(role, ref):
    return {"id": "audit-" + role, "role": role, "status": "complete"}, ref


def test_per_candidate_review_preserves_approved_sibling(engine, monkeypatch):
    """A bundle-wide revise must not suppress approved sibling candidates; an identity-only issue does not block extraction."""
    case = seed(engine, persist=False)
    sibling = candidate(engine, case["paper_ref"], "candidate-b")
    eref = engine.put("extraction", {"paper_ref": case["paper_ref"], "candidate_refs": [case["candidate_ref"], sibling]})
    issue = {"issue_id": "native-interface-unknown", "kind": "source_ambiguity", "scope": "candidate-a oracle",
             "subject_refs": [case["candidate_ref"]], "blocks": ["identity"],
             "message": "Faithful unknown, no extraction defect.", "evidence_refs": [], "resolves": []}
    rref = review(engine, eref, "extraction", "revise", assessments=[
        {"subject_id": "candidate-a", "verdict": "approve", "reason": "Faithfully recorded unknown."},
        {"subject_id": "candidate-b", "verdict": "defer", "reason": "The referenced appendix is unavailable."},
    ], issues=[issue])
    refs = {"extractor": eref, "extraction_reviewer": rref}
    monkeypatch.setattr(engine, "_job", lambda role, inputs, scope: completed(role, refs[role]))
    advanced = []
    def record_advance(current):
        advanced.append(current["candidate_ref"])
        return current
    monkeypatch.setattr(engine, "_advance", record_advance)
    result = engine.process_paper(case["paper_ref"])
    assert advanced == [case["candidate_ref"]]
    assert len(result["case_ids"]) == 2
    sibling_case = engine.ws.case(result["case_ids"][1])
    assert sibling_case["state"] == "extraction_defer"


def test_rescanning_does_not_advance_a_frozen_unresolved_identity(engine, monkeypatch):
    """A repeated scan is ordinary recovery, not new scientific evidence or new review authorization."""
    case = seed(engine)
    case.update(identity_ref=identity(engine, case, "unresolved"), state="identity_unresolved")
    engine.ws.save_case(case)
    calls = []

    def stage(role, inputs, scope):
        calls.append(role)
        if role == "extractor":
            return completed(role, case["extraction_ref"])
        if role == "extraction_reviewer":
            return completed(role, case["extraction_review_ref"])
        return {"id": "unexpected-" + role, "status": "needs_materials"}, None

    monkeypatch.setattr(engine, "_job", stage)
    engine.process_paper(case["paper_ref"])
    assert set(calls).issubset({"extractor", "extraction_reviewer"}), "Rescanning an existing unresolved identity must not start new downstream stages"
    assert engine.ws.case(case["case_id"])["state"] == "identity_unresolved"


def test_plain_resume_finishes_interrupted_extraction_revision_first(engine, monkeypatch):
    """When extraction of a new candidate completes but its reviewer is interrupted, resume must first continue that fixed new extraction review."""
    case = seed(engine, extraction_verdict="revise")
    updated = candidate(engine, case["paper_ref"], revision=1)
    updated_extraction = engine.put("extraction", {"paper_ref": case["paper_ref"], "candidate_refs": [updated]})
    calls = []

    def stage(role, inputs, scope):
        calls.append((role, deepcopy(inputs)))
        if role == "extractor":
            return completed(role, updated_extraction)
        return {"id": "paused-" + role, "status": "transport_uncertain"}, None

    monkeypatch.setattr(engine, "_job", stage)
    paused = engine.resume_case(case["case_id"], stage="extraction")
    assert paused["state"] == "extraction_reviewer:transport_uncertain"
    engine.resume_case(case["case_id"])
    assert calls[-1][0] == "extraction_reviewer", "An unfinished extraction review must not fall back to an old candidate and enter matching"
    assert calls[-1][1]["subject_ref"] == updated_extraction
    assert not any(role == "matcher" for role, _ in calls)


@pytest.mark.parametrize("requested_stage,producer_role", [("identity", "matcher"), ("research", "profile_researcher")])
def test_revision_producer_can_read_the_review_that_requested_revision(engine, monkeypatch, requested_stage, producer_role):
    """revise permits reworking, but the actual producer must also be authorized to read formal revision requirements as input."""
    case = seed(engine)
    iref = identity(engine, case)
    case["identity_ref"] = iref
    case["identity_review_ref"] = review(engine, iref, "identity", "revise" if requested_stage == "identity" else "approve")
    if requested_stage == "research":
        # The fixed finite toy profile is schema-valid, but this routing test
        # neither adopts its scripted bounds nor calls the Atlas writer.
        pref = engine.put("profile", synthetic_profile("AUDIT_FIXTURE"))
        rref = engine.put("research", {"candidate_ref": case["candidate_ref"], "identity_ref": iref,
                                      "action": "new", "setting_id": "AUDIT_FIXTURE", "base_version": None,
                                      "profile_ref": pref, "result_refs": [], "proof_refs": [], "issues": [],
                                      "change_summary": "Synthetic pending revision.",
                                      "research_scope": _SYNTHETIC.synthetic_research_scope()})
        case["research_ref"] = rref
        case["profile_review_ref"] = review(engine, rref, "profile", "revise")
    feedback_ref = case["identity_review_ref"] if requested_stage == "identity" else case["profile_review_ref"]
    case["state"] = "identity_revise" if requested_stage == "identity" else "profile_revise"
    engine.ws.save_case(case)
    observed = []

    def stage(role, inputs, scope):
        observed.append((role, deepcopy(inputs)))
        return {"id": "paused-" + role, "status": "needs_materials"}, None

    monkeypatch.setattr(engine, "_job", stage)
    engine.resume_case(case["case_id"], stage=requested_stage)
    role, inputs = observed[-1]
    assert role == producer_role
    assert inputs.get("repair_feedback_ref") == feedback_ref, "The new job lacks the fixed reviewer feedback it must address"
    # Correct routing alone is insufficient: tool read authorization must actually include this feedback.
    new_job = {"id": "audit-revision-producer", "role": role, "inputs": inputs}
    host = ToolHost(engine.ws, engine.atlas, new_job, engine.config)
    assert host.call("artifact_get", {"ref": feedback_ref, "pointer": "/summary", "offset": 0, "limit": 1000}, "read-feedback")["text"]


class SimulatedProcessDeath(BaseException):
    pass


class DraftBackend:
    """Demonstrate the tool protocol only: create and update a checkpoint draft, then report that materials are needed."""
    def __init__(self, job_id):
        self.job_id = job_id
        self.calls = 0

    def complete(self, **request):
        self.calls += 1
        if self.calls == 1:
            call = ToolCall("draft_create", {"kind": "checkpoint", "initial_json": dumps({"summary": "saved", "refs": [], "remaining": []})}, "create")
        elif self.calls == 2:
            did = digest({"job": self.job_id, "token": "create"})[:24]
            call = ToolCall("draft_patch", {"draft_id": did, "revision": 0, "patches_json": dumps([{"op": "add", "path": "/remaining/-", "value": "Read source page 7."}])}, "patch")
        else:
            return Reply(text=dumps({"status": "needs_materials", "artifact_refs": [], "summary": "Protocol-only test finished.", "checkpoint_ref": None}))
        return Reply(output_items=[{"type": "function_call", "call_id": call.call_id, "name": call.name, "arguments": dumps(call.arguments)}], calls=[call])


def test_paid_response_and_draft_patch_survive_process_death_exactly_once(engine, monkeypatch):
    """The window after response persistence and draft mutation but before tool-receipt persistence must recover idempotently."""
    jid = engine.ws.create_job("extractor", {})
    backend = DraftBackend(jid)
    runner = AgentRunner(engine.ws, engine.atlas, backend, engine.config)
    original = ToolHost.call
    died = False

    def crash_after_patch(self, name, args, call_id):
        nonlocal died
        result = original(self, name, args, call_id)
        if name == "draft_patch" and not died:
            died = True
            raise SimulatedProcessDeath()
        return result

    monkeypatch.setattr(ToolHost, "call", crash_after_patch)
    with pytest.raises(SimulatedProcessDeath):
        runner.run(jid)
    assert backend.calls == 2
    saved_calls = engine.ws.query("SELECT status FROM calls WHERE job=? ORDER BY created", (jid,))
    assert len(saved_calls) == 2 and saved_calls[-1]["status"] == "response"
    # A new connection simulates restart and recovers only persisted state, without the previous runner's memory.
    restored = Workspace(engine.ws.root)
    try:
        outcome = AgentRunner(restored, engine.atlas, backend, engine.config).run(jid)
        did = digest({"job": jid, "token": "create"})[:24]
        draft = restored.draft(did, jid)
        assert draft["revision"] == 1
        assert draft["data"]["remaining"] == ["Read source page 7."]
        assert outcome["status"] == "needs_materials"
        assert backend.calls == 3, "Restart must not request the already persisted second paid response again"
    finally:
        restored.close()


def test_reviewer_reads_are_bounded_and_do_not_expose_producer_memory(engine):
    """Paginate large source text by fixed reference; independent reviewers do not inherit producer private notes."""
    text = "Original source line.\n" * 3000
    source_ref = engine.put("source", {"url": "fixture://bounded-source", "version": "fixture-v1",
                                       "content_hash": digest(text), "text": text, "metadata": {}})
    subject_ref = engine.put("native_record", {"source_ref": source_ref, "summary": "Read the source by page."})
    producer = engine.ws.create_job("extractor", {"source_ref": source_ref})
    engine.ws.memory_save(producer, "extractor", "PRIVATE_SENTINEL_UNTRUSTED_SELF_ASSESSMENT", [source_ref])
    reviewer = engine.ws.create_job("extraction_reviewer", {"subject_ref": subject_ref})
    cfg = deepcopy(engine.config)
    cfg["budgets"]["max_tool_chars"] = 200
    host = ToolHost(engine.ws, engine.atlas, engine.ws.job(reviewer), cfg)
    with pytest.raises(ProtocolError, match="Reference is unauthorized"):
        host.call("source_read", {"ref": source_ref, "offset": 0, "limit": 100000}, "too-early")
    host.call("artifact_get", {"ref": subject_ref, "pointer": "", "offset": 0, "limit": 1000}, "subject")
    first = host.call("source_read", {"ref": source_ref, "offset": 0, "limit": 100000}, "source-one")
    second = host.call("source_read", {"ref": source_ref, "offset": first["next_offset"], "limit": 100000}, "source-two")
    assert first["text"] + second["text"] == text[:400]
    assert first["next_offset"] == 200 and second["next_offset"] == 400
    assert first["total_chars"] == len(text)
    memory = host.call("memory_search", {"query": "PRIVATE_SENTINEL", "limit": 8}, "memory")
    assert memory["notes"] == []
