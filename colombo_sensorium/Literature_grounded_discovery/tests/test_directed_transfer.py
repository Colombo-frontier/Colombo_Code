"""Exercise the directed transfer branch without pretending scripted science is a real paper review."""
from copy import deepcopy

import pytest

from oracle_atlas.atlas.tags import facts_from_sidecars
from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.workflow import transfer
from test_pipeline_demo import DEMO


@pytest.fixture
def reviewed_source(tmp_path, monkeypatch):
    engine, backend, _, request = DEMO.setup_demo(tmp_path)
    engine.config["budgets"]["max_candidates"] = 1
    engine.config["publication"]["require_human_approval"] = True
    target = "DEMO_BINARY_VALUE"
    old_put = backend._put

    def put(kind, value, dependencies=()):
        if kind == "candidate" and value["synthetic_branch"] == "fill_bound":
            value["common_specification"]["model"]["summary"] = "Source considers an additional input outside the two-point target."
        if kind == "identity" and value.get("setting_id") == target:
            value.update(decision="new", setting_id=None)
            for row in value["comparisons"]:
                if row["setting_id"] == target:
                    row.update(relation="related", reason="The target is the two-input subclass of the source.")
        if kind == "review" and value["review_type"] == "profile":
            value["assessments"] += [{"subject_id":"transfer:"+key,"verdict":"approve",
                                     "reason":"Checked the two-input target under " + key} for key in transfer.CHECKS]
        return (yield from old_put(kind, value, dependencies))

    monkeypatch.setattr(backend, "_put", put)
    stage = engine._stage

    def start(case, role, inputs):
        if role == "profile_researcher":
            # Keep the ordinary source's potential new-setting research separate.
            engine.ws.save_case(case)
            return None
        return stage(case, role, inputs)

    monkeypatch.setattr(engine, "_stage", start)
    run = engine.scan(request)
    cid = run["cases"][0]
    original = engine.ws.case(cid)
    assert engine.artifacts.get(original["identity_ref"])["data"]["decision"] == "new"
    yield engine, original, target, backend
    engine.ws.close()


def test_transfer_updates_existing_target_only_after_fresh_review_and_human_receipt(reviewed_source):
    engine, original, target, backend = reviewed_source
    before = engine.atlas.snapshot(target)
    case = engine.assess_transfer(original["case_id"], target)
    assert case["state"] == "ready_for_approval", (case, backend.observed_tool_errors)
    assert engine.atlas.version(target) == before["version"]
    assert case["case_id"] != original["case_id"] and case["identity_ref"] == original["identity_ref"]
    scope = engine.artifacts.get(case["transfer_scope_ref"])["data"]
    assert set(scope["target_files"]) == set(before["files"])
    assert {k:engine.artifacts.get(ref)["data"]["content"] for k,ref in scope["target_files"].items()} == before["files"]
    assert set(case["jobs"]) == {"bound_updater","profile_reviewer"}
    assert all(engine.ws.job(j)["inputs"]["transfer_scope_ref"] == case["transfer_scope_ref"] for j in case["jobs"].values())
    assert engine.artifacts.get(case["research_ref"])["data"]["tag_facts"] == []
    assert engine.ws.case(original["case_id"]) == original

    result = engine.resume_case(case["case_id"], approve=True)
    assert result["state"] == "committed" and result["receipt_ref"]
    after = engine.atlas.snapshot(target)
    assert after["version"] != before["version"]
    assert after["files"]["profile.json"]["common_specification"] == before["files"]["profile.json"]["common_specification"]
    assert len(after["files"]["profile.json"]["bounds"]) == len(before["files"]["profile.json"]["bounds"]) + 1
    def tags(files):
        return {r["concept_id"] for r in facts_from_sidecars(files["profile.json"],files["machine_tags.json"],files["classification.json"])}
    assert tags(after["files"]) == tags(before["files"])
    previous_calls = backend.calls
    repeated = engine.assess_transfer(original["case_id"], target)
    assert repeated["receipt_ref"] == result["receipt_ref"] and backend.calls == previous_calls
    assert engine.ws.case(original["case_id"]) == original


def test_related_and_current_independent_review_are_required(reviewed_source):
    engine, original, target, _ = reviewed_source
    with pytest.raises(ProtocolError, match="related"):
        engine.assess_transfer(original["case_id"], "DEMO_SIGNED_LINEAR")
    with engine.ws.transaction() as db:
        db.execute("DELETE FROM events WHERE event='validated_handoff' AND job=?",
                   (original["jobs"]["identity_reviewer"],))
    with pytest.raises(ProtocolError, match="independent"):
        engine.assess_transfer(original["case_id"], target)


def test_scope_mismatch_and_missing_transfer_proof_are_rejected(reviewed_source):
    engine, original, target, _ = reviewed_source
    case = engine.assess_transfer(original["case_id"], target)
    scope = engine.artifacts.get(case["transfer_scope_ref"])["data"]
    research = engine.artifacts.get(case["research_ref"])["data"]
    for changes in ({"action":"new"}, {"setting_id":"SOURCE_SETTING"}, {"proof_refs":[]}):
        with pytest.raises(ProtocolError):
            transfer.check_transfer_research(scope, {**research, **changes},engine.artifacts.get)
    wrong = deepcopy(engine.artifacts.get(research["result_refs"][0])["data"])
    wrong["direction"] = "upper"
    wrong_ref = engine.put("result", wrong)
    with pytest.raises(ProtocolError, match="same-direction"):
        transfer.check_transfer_research(scope, {**research, "result_refs":[wrong_ref]}, engine.artifacts.get)
    with pytest.raises(ProtocolError, match="target tags unchanged"):
        transfer.check_transfer_research(scope, {**research,"tag_facts":[{"view_ref":"deterministic"}]},engine.artifacts.get)
    profile = engine.artifacts.get(research["profile_ref"])["data"]
    changed = deepcopy(profile)
    changed["common_specification"]["model"]["summary"] = "Use the broader source model."
    ref = engine.put("profile", changed)
    with pytest.raises(ProtocolError, match="common specification"):
        transfer.check_transfer_research(scope, {**research,"profile_ref":ref},engine.artifacts.get)
    with pytest.raises(ProtocolError, match="revise only"):
        engine.resume_case(case["case_id"],stage="identity")
    review = deepcopy(engine.artifacts.get(case["profile_review_ref"])["data"])
    review["assessments"] = [r for r in review["assessments"] if r["subject_id"]!="transfer:direction"]
    with pytest.raises(ProtocolError, match="transfer:direction"):
        transfer.check_transfer_review(review)


def test_stale_source_cannot_commit_even_after_human_approval(reviewed_source):
    engine, original, target, _ = reviewed_source
    case = engine.assess_transfer(original["case_id"], target)
    base = engine.atlas.version(target)
    engine.ws.save_case({**original, "extraction_review_ref": None})
    assert engine.resume_case(case["case_id"], approve=True)["state"] == "identity_stale"
    assert engine.atlas.version(target) == base


def test_research_revision_pins_same_target_and_preserves_original(reviewed_source, monkeypatch):
    engine, original, target, _ = reviewed_source
    case = engine.assess_transfer(original["case_id"], target)
    extra = engine.put("external_result", {"description":"Additional synthetic test material."})
    jobs = []
    def record_routing(branch, role, inputs):
        jobs.append((role, inputs))
    monkeypatch.setattr(engine, "_stage", record_routing)
    revised = engine.resume_case(case["case_id"], stage="research", material_refs=[extra])
    assert [j[0] for j in jobs] == ["bound_updater"]
    assert jobs[0][1]["setting_id"] == target and jobs[0][1]["base_version"] == engine.atlas.version(target)
    assert revised["case_id"] == case["case_id"] and revised["transfer_scope_ref"] == case["transfer_scope_ref"]
    assert revised["history"][-1]["profile_review_ref"] == case["profile_review_ref"]
    assert not revised.get("profile_review_ref") and extra in revised["material_refs"]
    assert engine.ws.case(original["case_id"]) == original
