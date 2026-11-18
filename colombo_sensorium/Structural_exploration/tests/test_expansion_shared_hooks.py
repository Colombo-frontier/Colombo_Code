"""Shared routing tests, not scientific acceptance of expansion proposals.

Expansion frontends validate the independent specification review. These tests
substitute that completed boundary and exercise only identity/research separation.
"""
from copy import deepcopy

import pytest

from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.workflow.engine import Engine


AXES = ("task", "model", "oracle", "algorithms", "output", "metric", "guarantee", "resource")


@pytest.fixture
def engine(tmp_path):
    config = {"workspace": str(tmp_path / "work"), "atlas": str(tmp_path / "atlas"),
              "budgets": dict(DEFAULTS), "model": {}}
    value = Engine(config, object())
    yield value
    value.ws.close()


def seed(engine, *, legacy=False):
    candidate = engine.put("candidate", {
        "candidate_id": "expansion-routing-fixture", "title": "Synthetic candidate",
        "paper_refs": [], "common_specification": {
            axis: {"summary": "Routing fixture only.", "statements": []} for axis in AXES},
        "views": [], "tag_facts": [], "issues": [],
    })
    origin = engine.put("external_result", {"synthetic": True, "origin": "neighborhood_expansion"})
    # Independent review validation belongs to the caller; use a non-scientific
    # marker here so these unit tests do not manufacture a publishable approval.
    candidate_review = engine.put("external_result", {"synthetic": True, "candidate_ref": candidate,
                                                       "boundary": "frontend review already validated"})
    case = {"case_id": "hook-fixture", "paper_ref": None, "candidate_ref": candidate,
            "origin_ref": origin, "expansion_ref": origin, "budget_scope": "hook-test",
            "state": "candidate_reviewed", "history": [], "jobs": {}}
    case["extraction_review_ref" if legacy else "candidate_review_ref"] = candidate_review
    engine.ws.save_case(case)
    return case


def identity(engine, case, *, decision="new"):
    retrieval = engine.put("retrieval", {"candidate_ref": case["candidate_ref"],
                                          "inventory_version": engine.atlas.version(), "broaden": True})
    return engine.put("identity", {
        "candidate_ref": case["candidate_ref"], "decision": decision, "setting_id": None,
        "view_mapping": [], "normalization": "Synthetic routing fixture.", "comparisons": [],
        "retrieval_ref": retrieval, "recall_audit": {
            "strategies": ["fixture-one", "fixture-two"], "unresolved_ids": [],
            "reason": "No mathematical conclusion.", "inventory_version": engine.atlas.version()},
        "issues": [],
    })


def review(engine, subject, verdict="approve"):
    return engine.put("review", {
        "subject_ref": subject, "review_type": "identity", "verdict": verdict,
        "assessments": [], "issues": [], "approved_bound_ids": [],
        "summary": "Synthetic routing decision only.",
    })


def install_stages(engine, monkeypatch, case, *, decision="new", verdict="approve", pause_reviewer=False):
    iref = identity(engine, case, decision=decision)
    rref = review(engine, iref, verdict)
    calls = []

    def job(role, inputs, scope):
        calls.append((role, deepcopy(inputs)))
        if role == "matcher":
            return {"id": "fixture-matcher", "status": "complete"}, iref
        if role == "identity_reviewer" and not pause_reviewer:
            return {"id": "fixture-reviewer", "status": "complete"}, rref
        return {"id": "paused-" + role, "status": "needs_materials"}, None

    monkeypatch.setattr(engine, "_job", job)
    return calls, iref, rref


def test_paperless_identity_hook_stops_before_research_and_is_reusable(engine, monkeypatch):
    case = seed(engine)
    calls, iref, rref = install_stages(engine, monkeypatch, case)
    result = engine.resolve_identity(case)
    assert result["state"] == "identity_confirmed"
    assert result["identity_ref"] == iref and result["identity_review_ref"] == rref
    assert [role for role, _ in calls] == ["matcher", "identity_reviewer"]
    assert result["paper_ref"] is None and "research_ref" not in result
    for _, inputs in calls:
        assert inputs["candidate_review_ref"] == case["candidate_review_ref"]
        assert inputs["origin_ref"] == case["origin_ref"]
        assert inputs["expansion_ref"] == case["expansion_ref"]
        assert "extraction_review_ref" not in inputs
    engine.resolve_identity(engine.ws.case(case["case_id"]))
    assert len(calls) == 2


def test_legacy_review_reference_is_preserved_as_alias(engine, monkeypatch):
    case = seed(engine, legacy=True)
    calls, _, _ = install_stages(engine, monkeypatch, case)
    engine.resolve_identity(case)
    for _, inputs in calls:
        assert inputs["candidate_review_ref"] == case["extraction_review_ref"]
        assert inputs["extraction_review_ref"] == case["extraction_review_ref"]


def test_identity_hook_requires_a_real_candidate_review_reference(engine):
    case = seed(engine)
    case.pop("candidate_review_ref")
    with pytest.raises(ProtocolError, match="candidate review"):
        engine.resolve_identity(case)
    case["candidate_review_ref"] = "sha256:" + "f" * 64
    with pytest.raises((KeyError, ProtocolError, FileNotFoundError)):
        engine.resolve_identity(case)


@pytest.mark.parametrize("verdict", ["revise", "defer"])
def test_nonapproving_identity_review_stops_research(engine, monkeypatch, verdict):
    case = seed(engine)
    calls, _, _ = install_stages(engine, monkeypatch, case, verdict=verdict)
    result = engine._advance(case)
    assert result["state"] == "identity_" + verdict
    assert [role for role, _ in calls] == ["matcher", "identity_reviewer"]


def test_unresolved_identity_does_not_invoke_review_or_research(engine, monkeypatch):
    case = seed(engine)
    calls, _, _ = install_stages(engine, monkeypatch, case, decision="unresolved")
    assert engine._advance(case)["state"] == "identity_unresolved"
    assert [role for role, _ in calls] == ["matcher"]


def test_interrupted_identity_review_preserves_match_for_resume(engine, monkeypatch):
    case = seed(engine)
    calls, iref, _ = install_stages(engine, monkeypatch, case, pause_reviewer=True)
    result = engine.resolve_identity(case)
    assert result["state"] == "identity_reviewer:needs_materials"
    assert result["identity_ref"] == iref
    assert "identity_review_ref" not in result
    engine.resolve_identity(result)
    assert [role for role, _ in calls] == ["matcher", "identity_reviewer", "identity_reviewer"]


def test_explicit_advance_runs_research_after_identity_selection(engine, monkeypatch):
    case = seed(engine)
    calls, _, _ = install_stages(engine, monkeypatch, case)
    engine.resolve_identity(case)
    assert engine._advance(case)["state"] == "profile_researcher:needs_materials"
    assert [role for role, _ in calls] == ["matcher", "identity_reviewer", "profile_researcher"]


@pytest.mark.parametrize("state,reference", [
    ("profile_researcher:needs_materials", None),
    ("ready_for_approval", "proposal_ref"),
    ("committed", "receipt_ref"),
])
def test_identity_hook_does_not_replace_downstream_state(engine, monkeypatch, state, reference):
    case = seed(engine)
    calls, _, _ = install_stages(engine, monkeypatch, case)
    engine.resolve_identity(case)
    case["state"] = state
    case["jobs"]["profile_researcher"] = "previous-research-job"
    if reference:
        case[reference] = engine.put("external_result", {"synthetic": True, "stage": reference})
    before = deepcopy(case)
    result = engine.resolve_identity(case)
    assert result == before
    assert len(calls) == 2
