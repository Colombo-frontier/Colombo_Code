"""Mechanical reprojection exercises the real flow; scripted judgments are not science acceptance."""
from copy import deepcopy

import pytest

from oracle_atlas.atlas.projection_report import mechanical_repair_request, projection_report
from oracle_atlas.core.contracts import ProtocolError
from test_pipeline_demo import DEMO
from test_preflight_pipeline import context, host, call
from test_atlas import profile, facts


def sidecar_issue():
    return {"issue_id": "regime_location", "kind": "protocol_error", "scope": "generated index",
            "subject_refs": [], "blocks": ["publication"], "message": "Synthetic wrong field-location request.",
            "evidence_refs": [], "resolves": []}


def repair_row():
    return {"issue_id": "regime_location", "file": "machine_tags.json", "pointer": "/registry/regimes",
            "reason": "Synthetic request for an index already present in identity.json."}


def test_preview_reports_actual_index_not_optional_registry(context):
    import json
    h = host(context)
    p = profile("PROJECTION_LOCATION")
    draft = call(h, "draft_create", kind="profile", initial_json=json.dumps(p))
    result = call(h, "draft_validate", draft_id=draft["draft_id"], tag_facts_json=json.dumps(facts(p)))
    preview = h._allowed(result["projection_preview_ref"])["data"]
    report = preview["projection_report"]
    assert result["validation"]["status"] == "passed"
    assert report["field_directory"]["regime_predicates"] == "/files/identity.json/regime_predicates"
    assert result["regime_index_count"] == len(p["regimes"]) > 0
    assert preview["files"]["machine_tags.json"]["registry"] == {}
    assert set(report["files"]) == set(preview["files"]) and len(report["files"]) == 5


def test_routing_never_waives_a_scientific_blocker():
    review = {"review_type": "profile", "verdict": "revise", "issues": [sidecar_issue()], "projection_repairs": [repair_row()]}
    assert mechanical_repair_request(review)
    scientific = {**sidecar_issue(), "issue_id": "counterexample", "kind": "proof_gap", "blocks": ["bound", "publication"]}
    review["issues"].append(scientific)
    assert not mechanical_repair_request(review)
    review["projection_repairs"].append({**repair_row(), "issue_id": "counterexample"})
    with pytest.raises(ProtocolError, match="scientific blockers"):
        mechanical_repair_request(review)


def test_future_bound_issue_needs_current_complete_credentials_for_projection_route():
    review = {"review_type": "profile", "verdict": "revise", "issues": [sidecar_issue(),
        {**sidecar_issue(), "issue_id": "future_work", "kind": "applicability", "blocks": ["bound"]}],
        "projection_repairs": [repair_row()], "issue_scope_version": "occurrence-bound-scope",
        "approved_bound_ids": ["adopted"], "bound_approvals": [{"bound_id": "adopted"}],
        "bound_issue_scopes": [{"issue_id": "future_work", "scope_complete": True,
                                "affected_bound_ids": [], "occurrence_ids": ["occurrence:fixture"]}]}
    # The caller supplies the actual current active IDs only after the stored
    # review's complete occurrence credentials pass the normal runtime validator.
    assert not mechanical_repair_request(review)
    assert mechanical_repair_request(review, active_bound_ids={"adopted"})
    assert not mechanical_repair_request(review, active_bound_ids={"adopted", "missing_credential"})
    review["bound_issue_scopes"][0]["affected_bound_ids"] = ["adopted"]
    assert not mechanical_repair_request(review, active_bound_ids={"adopted"})
    review["bound_issue_scopes"][0]["affected_bound_ids"] = []
    review["issues"][1]["blocks"].append("publication")
    assert not mechanical_repair_request(review, active_bound_ids={"adopted"})


@pytest.mark.parametrize("resolve", [True, False])
def test_sidecar_only_revise_runs_one_independent_review_without_author_rewrite(tmp_path, monkeypatch, resolve):
    engine, backend, _, request = DEMO.setup_demo(tmp_path)
    original = backend._put
    def put(kind, value, *args, **kwargs):
        if kind == "review" and value.get("review_type") == "profile":
            value = deepcopy(value)
            feedback = backend.current_job["inputs"].get("repair_feedback_ref")
            if feedback and resolve:
                value["coverage_audit"]["resolved_issue_ids"] = ["regime_location"]
            else:
                value.update(verdict="revise", issues=[sidecar_issue()], projection_repairs=[repair_row()])
                if feedback:
                    value["coverage_audit"]["carried_issue_ids"] = ["regime_location"]
        return (yield from original(kind, value, *args, **kwargs))
    monkeypatch.setattr(backend, "_put", put)
    try:
        run = engine.scan(request)
        for cid in run["cases"]:
            case = engine.ws.case(cid)
            assert case["state"] == ("committed" if resolve else "projection_review_unresolved"), case
            assert case.get("revision_counts", {}).get("research", 0) == 0
            assert len(case["projection_repair_attempts"]) == 1
            repair = engine.artifacts.get(case["projection_repair_ref"])["data"]
            assert repair["scientific_profile_unchanged"] and not repair["bundle_changed"]
            assert repair["projection"]["validation"]["status"] == "passed"
            assert repair["projection"]["counts"]["regime_predicates"] > 0
            old = engine.artifacts.get(repair["previous_review_ref"])
            new = engine.artifacts.get(case["profile_review_ref"])
            assert old["data"]["verdict"] == "revise" and old["producer"] != new["producer"]
            assert engine.ws.job(new["producer"])["inputs"]["issue_scope_contract_version"] == "occurrence-bound-scope"
            if resolve:
                receipt = engine.artifacts.get(case["receipt_ref"])["data"]
                assert receipt["review_subject_ref"] == repair["subject_ref"] and len(receipt["files"]) == 5
            else:
                assert not case.get("receipt_ref")
    finally:
        engine.ws.close()


@pytest.mark.parametrize("concurrent", [False, True])
def test_failed_reprojection_preserves_diagnostics_without_overwriting_concurrent_progress(tmp_path, monkeypatch, concurrent):
    from oracle_atlas.atlas.store import AtlasValidationError
    engine, backend, _, request = DEMO.setup_demo(tmp_path)
    original_put, original_prepare = backend._put, engine._prepare_proposal
    touched = []
    def put(kind, value, *args, **kwargs):
        if kind == "review" and value.get("review_type") == "profile":
            value = deepcopy(value)
            value.update(verdict="revise", issues=[sidecar_issue()], projection_repairs=[repair_row()])
        return (yield from original_put(kind, value, *args, **kwargs))
    def prepare(case):
        if case.get("profile_review_ref"):
            touched.append(case["case_id"])
            if concurrent:
                current = engine.ws.case(case["case_id"])
                current.update(state="externally_advanced", concurrent_marker="preserve me")
                engine.ws.save_case(current)
            raise AtlasValidationError("Synthetic projection failure", [{"code": "fixture_projection", "file": "identity.json", "path": "/regime_predicates", "message": "Synthetic failure"}])
        return original_prepare(case)
    monkeypatch.setattr(backend, "_put", put)
    monkeypatch.setattr(engine, "_prepare_proposal", prepare)
    try:
        if concurrent:
            with pytest.raises(ProtocolError, match="advanced concurrently"):
                engine.scan(request)
            case = engine.ws.case(touched[0])
            assert case["state"] == "externally_advanced" and case["concurrent_marker"] == "preserve me"
            assert "projection_diagnostic_ref" not in case
        else:
            run = engine.scan(request)
            for cid in run["cases"]:
                case = engine.ws.case(cid)
                assert case["state"] == "projection_protocol_error" and not case.get("receipt_ref")
                report = engine.artifacts.get(case["projection_diagnostic_ref"])["data"]
                assert report["review_ref"] == case["profile_review_ref"]
                assert report["errors"][0]["code"] == "fixture_projection"
    finally:
        engine.ws.close()
