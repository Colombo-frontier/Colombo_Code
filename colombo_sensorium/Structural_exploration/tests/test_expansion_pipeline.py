"""Actual offline expansion integration; fixed decisions are synthetic, not LLM science."""
import importlib.util
import json
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "examples" / "offline_expansion_demo.py"
SPEC = importlib.util.spec_from_file_location("offline_expansion_pipeline_fixture", SCRIPT)
DEMO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DEMO)


@pytest.fixture(scope="module")
def completed(tmp_path_factory):
    root = tmp_path_factory.mktemp("expansion-pipeline")
    engine, backend, request = DEMO.setup_demo(root)
    before = engine.expand(request)
    initial_catalog = engine.atlas.catalog()
    before_cases = {engine.ws.case(row["case_id"])["opportunity_id"]: engine.ws.case(row["case_id"]) for row in before["cases"]}
    research_calls = backend.calls_by_role["profile_researcher"]
    after = engine.publish(before["batch_id"])
    publish_research_calls = backend.calls_by_role["profile_researcher"] - research_calls
    calls_before_repeat = backend.calls
    versions = {row["setting_id"]: row["profile_version"] for row in engine.atlas.catalog()}
    repeated = engine.expand(request)
    cases = {engine.ws.case(row["case_id"])["opportunity_id"]: engine.ws.case(row["case_id"]) for row in after["cases"]}
    yield {"engine": engine, "backend": backend, "request": request, "before": before, "after": after,
           "initial_catalog": initial_catalog, "before_cases": before_cases, "cases": cases,
           "publish_research_calls": publish_research_calls, "calls_before_repeat": calls_before_repeat,
           "versions": versions, "repeated": repeated}
    engine.ws.close()


def test_paperless_expansion_requires_review_and_human_publication(completed):
    data = completed
    assert data["before"]["state_counts"] == {"ready_for_approval": 2, "redirected_existing": 1, "duplicate_pending": 1}
    assert len(data["initial_catalog"]) == 1
    assert data["after"]["state_counts"] == {"committed": 2, "redirected_existing": 1, "duplicate_pending": 1}
    assert data["engine"].ws.query("SELECT COUNT(*) AS n FROM artifacts WHERE kind='paper'")[0]["n"] == 0
    assert not {"paper_scanner", "extractor", "extraction_reviewer"}.intersection(data["backend"].calls_by_role)
    for case in data["cases"].values():
        assert case["paper_ref"] is None
        candidate = data["engine"].artifacts.get(case["candidate_ref"])["data"]
        assert candidate["paper_refs"] == []
        assert candidate["origin"]["kind"] == "atlas_expansion"
        assert candidate["origin"]["designed_contract"] is True


def test_independent_pending_duplicate_review_avoids_research(completed):
    engine, cases = completed["engine"], completed["cases"]
    duplicate = cases["duplicate_gradient"]
    assert duplicate["state"] == "duplicate_pending"
    assert duplicate["duplicate_of_ref"] == cases["gradient"]["candidate_ref"]
    assert "identity_ref" not in duplicate and "research_ref" not in duplicate
    review = engine.artifacts.get(duplicate["candidate_review_ref"])["data"]
    assert review["verdict"] == "exclude"
    assert len(review["pending_comparisons"]) == 3
    assert any(row["relation"] == "equivalent" and row["candidate_ref"] == duplicate["duplicate_of_ref"] for row in review["pending_comparisons"])


def test_existing_randomized_view_is_redirected_without_new_setting(completed):
    engine = completed["engine"]
    case = completed["cases"]["existing_view"]
    assert case["state"] == "redirected_existing"
    assert case["existing_setting_id"] == DEMO.SEED_ID
    assert "research_ref" not in case and "receipt_ref" not in case
    identity = engine.artifacts.get(case["identity_ref"])["data"]
    assert identity["decision"] == "existing"
    assert identity["view_mapping"][0]["candidate_view_id"] == "randomized"
    assert identity["view_mapping"][0]["atlas_view_id"] is None
    assert [view["view_id"] for view in engine.atlas.read(DEMO.SEED_ID)["views"]] == ["deterministic"]


def test_second_publication_refreshes_identity_without_research_regeneration(completed):
    engine = completed["engine"]
    assert completed["publish_research_calls"] == 0
    first = completed["cases"]["gradient"]
    second = completed["cases"]["value_gradient"]
    old = completed["before_cases"]["value_gradient"]
    assert "rebase_context_ref" not in first
    assert second["rebase_context_ref"]
    assert second["identity_ref"] != old["identity_ref"]
    assert second["identity_review_ref"] != old["identity_review_ref"]
    assert second["profile_review_ref"] != old["profile_review_ref"]
    assert second["proposal_ref"] != old["proposal_ref"]
    old_research = engine.artifacts.get(old["research_ref"])["data"]
    new_research = engine.artifacts.get(second["research_ref"])["data"]
    assert old_research["profile_ref"] == new_research["profile_ref"]
    assert old_research["proof_refs"] == new_research["proof_refs"]
    assert old_research["result_refs"] == new_research["result_refs"]
    old_proposal = engine.artifacts.get(old["proposal_ref"])["data"]
    new_proposal = engine.artifacts.get(second["proposal_ref"])["data"]
    assert engine.artifacts.get(old_proposal["prepared_ref"])["data"]["bundle_hash"] == engine.artifacts.get(new_proposal["prepared_ref"])["data"]["bundle_hash"]
    identity = engine.artifacts.get(second["identity_ref"])["data"]
    assert "DEMO_EXPANDED_GRADIENT" in {row["setting_id"] for row in identity["comparisons"]}


def test_every_accepted_candidate_has_fresh_independent_review_jobs(completed):
    engine = completed["engine"]
    for case in completed["cases"].values():
        expansion = engine.artifacts.get(case["expansion_ref"])
        candidate = engine.artifacts.get(case["candidate_ref"])
        review = engine.artifacts.get(case["candidate_review_ref"])
        assert review["producer"] != expansion["producer"]
        assert review["producer"] != candidate["producer"]
        assert engine.ws.job(review["producer"])["role"] == "expansion_reviewer"
        assert review["data"]["subject_ref"] == case["expansion_ref"]
        assert review["data"]["candidate_ref"] == case["candidate_ref"]
        if case.get("identity_ref"):
            identity_review = engine.artifacts.get(case["identity_review_ref"])
            assert identity_review["data"]["subject_ref"] == case["identity_ref"]
            assert engine.ws.job(identity_review["producer"])["role"] == "identity_reviewer"
        if case.get("profile_review_ref"):
            profile_review = engine.artifacts.get(case["profile_review_ref"])
            assert profile_review["data"]["subject_ref"] == case["proposal_ref"]
            assert engine.ws.job(profile_review["producer"])["role"] == "profile_reviewer"
    assert completed["backend"].review_memory
    assert all(item["notes"] == [] for item in completed["backend"].review_memory)


def test_actual_receipts_and_exact_eight_axis_tags_are_written(completed):
    engine = completed["engine"]
    assert len(engine.atlas.catalog()) == 3
    for oid, returns in (("gradient", ["gradient"]), ("value_gradient", ["value", "gradient"])):
        case = completed["cases"][oid]
        receipt = engine.artifacts.get(case["receipt_ref"])["data"]
        assert receipt["status"] == "committed"
        assert len(receipt["files"]) == 5
        sid = DEMO.case_definition(oid)["setting_id"]
        profile = engine.atlas.read(sid)
        assert profile["common_specification"]["oracle"]["operations"][0]["returns"] == returns
        assert profile["provenance"]["synthetic"]
        assert {item["direction"] for item in profile["bounds"]} == {"upper", "lower"}
        features = engine.atlas.read(sid, "machine_tags.json")["features"]
        assert {row["axis"] for row in features} == {"TASK", "MODEL", "ORACLE", "ALGORITHMS", "OUTPUT", "METRIC", "GUARANTEE", "RESOURCE"}


def test_repeat_batch_has_no_new_calls_or_versions(completed):
    assert completed["backend"].calls == completed["calls_before_repeat"]
    assert completed["backend"].observed_tool_errors == []
    assert completed["repeated"]["state_counts"] == completed["after"]["state_counts"]
    assert completed["versions"] == {row["setting_id"]: row["profile_version"] for row in completed["engine"].atlas.catalog()}
    for row in completed["repeated"]["cases"]:
        assert row["selection_reason"]
        assert row["transformation"]


def test_two_phase_batch_resolves_identities_before_selected_research(tmp_path):
    engine, backend, request = DEMO.setup_demo(tmp_path)
    try:
        candidates = engine.expand(request, research=False)
        assert candidates["state_counts"] == {"identity_confirmed": 2, "redirected_existing": 1, "duplicate_pending": 1}
        assert backend.calls_by_role["profile_researcher"] == 0
        match_calls = backend.calls_by_role["matcher"]
        reviewed = engine.run_batch(candidates["batch_id"], research=True)
        assert reviewed["state_counts"]["ready_for_approval"] == 2
        assert backend.calls_by_role["matcher"] == match_calls
        assert len(engine.atlas.catalog()) == 1
    finally:
        engine.ws.close()


def test_specification_revision_uses_expansion_roles_and_preserves_candidate_id(tmp_path):
    engine, backend, request = DEMO.setup_demo(tmp_path, revise_first=True)
    try:
        report = engine.expand(request, research=False)
        case = next(engine.ws.case(row["case_id"]) for row in report["cases"] if engine.ws.case(row["case_id"])["opportunity_id"] == "gradient")
        assert case["state"] == "identity_confirmed", report
        assert case["revision_counts"]["specification"] == 1
        assert len(case["history"]) == 1
        old = engine.artifacts.get(case["history"][0]["candidate_ref"])["data"]
        new = engine.artifacts.get(case["candidate_ref"])["data"]
        assert old["candidate_id"] == new["candidate_id"]
        assert old["common_specification"]["output"]["statements"][0]["status"] == "unknown"
        assert new["common_specification"]["output"]["statements"][0]["status"] == "known"
        producer = engine.ws.job(case["jobs"]["setting_expander"])
        assert producer["inputs"]["repair_feedback_ref"] == case["history"][0]["candidate_review_ref"]
        assert not {"extractor", "extraction_reviewer"}.intersection(backend.calls_by_role)
        assert backend.observed_tool_errors == []
    finally:
        engine.ws.close()


def test_example_exports_its_explanations_and_limits(tmp_path):
    report = DEMO.run_demo(tmp_path)
    saved = json.loads((tmp_path / "offline_expansion_report.json").read_text())
    markdown = (tmp_path / "offline_expansion_report.md").read_text()
    assert saved["real_model_calls"] == saved["network_calls"] == 0
    assert saved["paper_artifact_count"] == 0
    assert len(saved["receipt_refs"]) == 2
    assert saved["repeat_added_calls"] == saved["publication_added_research_calls"] == 0
    assert report["identity_refresh_cases"]
    assert "| Candidate | Result | Selection reason |" in markdown
    assert "No findings from real literature" in markdown
