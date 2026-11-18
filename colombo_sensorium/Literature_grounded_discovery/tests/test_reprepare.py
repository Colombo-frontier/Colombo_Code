"""Reprojection replaces only native sidecars and requires a real second reviewer handoff."""
from copy import deepcopy
import hashlib
import json

from oracle_atlas.atlas.tags import json_bytes
from oracle_atlas.core.store import digest
from test_pipeline_demo import DEMO


def test_changed_projection_reuses_frozen_research_but_requires_new_review(tmp_path, monkeypatch):
    engine, backend, _, request = DEMO.setup_demo(tmp_path)
    engine.config["publication"]["require_human_approval"] = True
    run = engine.scan(request)
    case = engine.ws.case(run["cases"][0])
    assert case["state"] == "ready_for_approval"
    assert engine.reprepare_case(case["case_id"]) == case
    previous = engine.atlas.prepare

    def changed_adapter(profile, facts, version):
        prepared = deepcopy(previous(profile, facts, version))
        prepared["files"]["identity.json"]["projection_version"] = "fixture-2"
        prepared["files"] = json.loads(json.dumps(prepared["files"],sort_keys=True))
        prepared["bundle_hash"] = digest(prepared["files"])
        hashes = {name:hashlib.sha256(json_bytes(value)).hexdigest() for name,value in prepared["files"].items()}
        prepared.update(hashes=hashes, version="target-"+digest(hashes))
        return prepared

    monkeypatch.setattr(engine.atlas, "prepare", changed_adapter)
    before = backend.calls_by_role.copy()
    after = engine.reprepare_case(case["case_id"])
    assert after["state"] == "ready_for_approval"
    assert after["research_ref"] == case["research_ref"] and after["proposal_ref"] != case["proposal_ref"]
    assert after["profile_review_ref"] != case["profile_review_ref"]
    assert after["history"][-1]["proposal_ref"] == case["proposal_ref"]
    assert after["repair_feedback_ref"] == case["profile_review_ref"]
    assert not after.get("human_approved") and not after.get("receipt_ref")
    assert backend.calls_by_role["profile_reviewer"] > before["profile_reviewer"]
    assert backend.calls_by_role["bound_updater"] == before["bound_updater"]
    final = engine.resume_case(case["case_id"], approve=True)
    assert final["state"] == "committed"
    receipt = engine.artifacts.get(final["receipt_ref"])["data"]
    assert receipt["review_subject_ref"] == after["proposal_ref"]
    engine.ws.close()


def test_interrupted_review_must_bind_the_actual_proposal(tmp_path, monkeypatch):
    import pytest
    from oracle_atlas.core.contracts import ProtocolError

    engine, _, _, request = DEMO.setup_demo(tmp_path)
    # A provider failure during complete is archived by the ordinary runner.
    backend = engine.runner.backend
    original_complete = backend.complete
    def complete(**arguments):
        if backend.current_job["role"] == "profile_reviewer":
            raise RuntimeError("Fixture interrupted before serving reviewer.")
        return original_complete(**arguments)
    monkeypatch.setattr(backend, "complete", complete)
    run = engine.scan(request)
    case = engine.ws.case(run["cases"][0])
    assert case["state"] == "profile_reviewer:transport_uncertain"
    assert not case.get("profile_review_ref")
    assert engine.reprepare_case(case["case_id"]) == case
    case["jobs"]["profile_reviewer"] = engine.ws.case(run["cases"][1])["jobs"]["profile_reviewer"]
    engine.ws.save_case(case)
    with pytest.raises(ProtocolError,match="exact unadopted"):
        engine.reprepare_case(case["case_id"])
    engine.ws.close()
