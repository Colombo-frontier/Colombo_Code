"""Controller identity rebinds retain actual research authority, never approval."""
from copy import deepcopy
import importlib.util
from pathlib import Path

import pytest

from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.core.store import digest


SCRIPT = Path(__file__).resolve().parents[1] / "examples/offline_expansion_demo.py"
SPEC = importlib.util.spec_from_file_location("scope_rebind_synthetic_demo", SCRIPT)
DEMO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DEMO)


@pytest.fixture(scope="module")
def rebound(tmp_path_factory):
    engine, backend, request = DEMO.setup_demo(tmp_path_factory.mktemp("scope-rebind"))
    before = engine.expand(request)
    calls = backend.calls_by_role["profile_researcher"]
    after = engine.publish(before["batch_id"])
    assert after["state_counts"]["committed"] == 2
    case = next(engine.ws.case(row["case_id"]) for row in after["cases"]
                if engine.ws.case(row["case_id"])["opportunity_id"] == "value_gradient")
    assert backend.calls_by_role["profile_researcher"] == calls
    yield engine, backend, case
    engine.ws.close()


def test_rebound_scope_uses_original_producer_and_unchanged_controller_trace(rebound):
    engine, backend, case = rebound
    current = engine.artifacts.get(case["research_ref"])
    audit = engine.artifacts.get(case["rebase_context_ref"])
    data = audit["data"]
    origin = engine.artifacts.get(data["origin_research_ref"])
    context = engine._research_context(case, current["data"])
    assert current["producer"] == audit["producer"] == "controller"
    assert engine.artifacts.owned(data["origin_research_ref"], data["research_producer_job"])
    assert not engine.artifacts.owned(case["research_ref"], data["research_producer_job"])
    assert context == data["research_context"] and digest(context) == data["research_context_hash"]
    assert context["producer_job"] == case["jobs"]["profile_researcher"]
    prepared = engine.artifacts.get(engine.artifacts.get(case["proposal_ref"])["data"]["prepared_ref"])["data"]
    review = engine.artifacts.get(case["profile_review_ref"])["data"]
    assert prepared["science"]["research_context"] == context
    assert review["joint_review"]["science_context_hash"] == prepared["science_hash"]
    assert origin["data"]["profile_ref"] == current["data"]["profile_ref"]


@pytest.mark.parametrize("field", ["change_summary", "research_scope"])
def test_controller_rebind_cannot_change_nonidentity_science_or_scope(rebound, field):
    engine, _, original = rebound
    case = deepcopy(original)
    research = deepcopy(engine.artifacts.get(case["research_ref"])["data"])
    if field == "research_scope":
        research[field]["scope"] += " Unapproved broader research claim."
    else:
        research[field] += " Unapproved changed scientific handoff."
    ref = engine.put("research", research)
    audit = deepcopy(engine.artifacts.get(case["rebase_context_ref"])["data"])
    audit["new_research_ref"] = ref
    case["research_ref"] = ref
    case["rebase_context_ref"] = engine.put("external_result", audit)
    with pytest.raises(ProtocolError, match="cannot alter scientific content"):
        engine._research_context(case, research)


def test_rebind_cannot_use_controller_artifact_as_an_owned_original_handoff(rebound):
    engine, _, original = rebound
    case = deepcopy(original)
    research = engine.artifacts.get(case["research_ref"])["data"]
    audit = deepcopy(engine.artifacts.get(case["rebase_context_ref"])["data"])
    audit["origin_research_ref"] = case["research_ref"]
    case["rebase_context_ref"] = engine.put("external_result", audit)
    with pytest.raises(ProtocolError, match="owned original scientific handoff"):
        engine._research_context(case, research)


def test_rebind_cannot_replace_actual_tool_context_with_a_claimed_context(rebound):
    engine, _, original = rebound
    case = deepcopy(original)
    research = engine.artifacts.get(case["research_ref"])["data"]
    audit = deepcopy(engine.artifacts.get(case["rebase_context_ref"])["data"])
    audit["research_context"]["observations"]["tool_call_count"] += 1
    audit["research_context_hash"] = digest(audit["research_context"])
    case["rebase_context_ref"] = engine.put("external_result", audit)
    with pytest.raises(ProtocolError, match="scope or tool evidence changed"):
        engine._research_context(case, research)


def test_two_separate_inventory_refreshes_keep_same_origin_without_new_research(tmp_path):
    engine, backend, request = DEMO.setup_demo(tmp_path)
    try:
        report = engine.expand(request)
        case = next(engine.ws.case(row["case_id"]) for row in report["cases"]
                    if engine.ws.case(row["case_id"])["opportunity_id"] == "value_gradient")
        original_ref = case["research_ref"]
        researcher_calls = backend.calls_by_role["profile_researcher"]
        reviews_before = engine.ws.query("SELECT COUNT(*) AS n FROM jobs WHERE role='profile_reviewer'")[0]["n"]
        registry = engine.atlas.data / "registry" / "synthetic-refresh-evidence.json"
        registry.parent.mkdir(parents=True, exist_ok=True)
        contexts = []
        for generation in (1, 2):
            registry.write_text('{"explicit_synthetic_generation":' + str(generation) + '}')
            case = engine._refresh_for_publication(engine.ws.case(case["case_id"]))
            assert case["state"] == "ready_for_approval", case
            audit = engine.artifacts.get(case["rebase_context_ref"])["data"]
            assert audit["origin_research_ref"] == original_ref
            contexts.append(audit["research_context_hash"])
            engine._clear_approval(case)
        assert contexts[0] == contexts[1]
        assert backend.calls_by_role["profile_researcher"] == researcher_calls
        assert engine.ws.query("SELECT COUNT(*) AS n FROM jobs WHERE role='profile_reviewer'")[0]["n"] == reviews_before + 2
    finally:
        engine.ws.close()
