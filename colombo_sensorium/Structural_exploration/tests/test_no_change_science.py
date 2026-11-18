"""Engine no-change boundaries with explicit toy science and no model/network.

The scripted job adapter still freezes through the actual ToolHost and invokes
Engine._validate_stage. It substitutes software fixtures for scientific work;
it does not claim that any real theorem or literature has been approved.
"""
from copy import deepcopy
import json

import pytest

from oracle_atlas.atlas.store import FILES
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.store import dumps
from oracle_atlas.science.joint import JOINT_CHECKS
from oracle_atlas.tools.host import ToolHost
from oracle_atlas.workflow.coverage import CHECKS
from oracle_atlas.workflow.engine import Engine
from test_atlas import profile, facts, approve, _SYNTHETIC
from test_preflight_pipeline import candidate


NOTICE = "Synthetic finite Engine no-change fixture; no model, source survey or real scientific approval."
SCOPE = {"scope": NOTICE, "queries_complete": True, "unresolved_leads": []}
OLD_SCOPE = {**SCOPE, "scope": NOTICE + " Previous fixture round."}


class NoBackend:
    def complete(self, **request):
        raise AssertionError("No-change contract tests must not request a model")


def coverage_checks():
    return [{"check_id": name, "scope": "Only the explicit fixed finite toy family.",
             "status": "not_applicable", "reason": "No varying parameter in this scripted finite fixture.",
             "result_refs": [], "proof_refs": []} for name in CHECKS]


def scientific_review(subject, prepared):
    return {"subject_ref": subject, "review_type": "profile", "verdict": "approve",
            "assessments": [], "issues": [], "approved_bound_ids": ["u"], "summary": NOTICE,
            "joint_review": _SYNTHETIC.synthetic_joint_review(prepared),
            "coverage_audit": {"scope": NOTICE, "checks": coverage_checks(),
                "resolved_issue_ids": [], "carried_issue_ids": [], "new_blocker_justifications": [],
                "followups": [], "reuse_context_ref": None, "reused_bound_ids": []}}


@pytest.fixture
def scenario(tmp_path):
    config = {"workspace": str(tmp_path / "work"), "atlas": str(tmp_path / "atlas"),
              "budgets": dict(DEFAULTS), "model": {"model": "synthetic-never-called"}}
    engine = Engine(config, NoBackend())
    p = profile("NO_CHANGE_TOY")
    p["research_scope"] = deepcopy(OLD_SCOPE)
    p["joint_analysis"]["synthesis_coverage"]["literature"] = {
        "status": "finite_scope_complete", "scope": OLD_SCOPE["scope"]}
    prepared = engine.atlas.prepare(p, facts(p), research_context={"scope": deepcopy(OLD_SCOPE)})
    engine.atlas.commit(prepared, approve(prepared), "synthetic-initial-baseline")
    paper = engine.put("paper", {"title": NOTICE, "doi": None, "arxiv_id": None,
        "urls": [], "publication_events": [], "provenance": []})
    cref = engine.put("candidate", candidate(p, paper))
    candidate_review = engine.put("review", {"subject_ref": cref, "review_type": "extraction",
        "verdict": "approve", "assessments": [], "issues": [], "approved_bound_ids": [], "summary": NOTICE})
    retrieval = engine.put("retrieval", {"candidate_ref": cref, "inventory_version": engine.atlas.version(), "broaden": True})
    iref = engine.put("identity", {"candidate_ref": cref, "decision": "existing", "setting_id": p["setting_id"],
        "view_mapping": [{"candidate_view_id": "randomized", "atlas_view_id": "randomized", "reason": NOTICE}],
        "normalization": NOTICE, "comparisons": [], "retrieval_ref": retrieval,
        "recall_audit": {"strategies": ["synthetic-one", "synthetic-two"], "unresolved_ids": [],
            "reason": NOTICE, "inventory_version": engine.atlas.version()}, "issues": []})
    ireview = engine.put("review", {"subject_ref": iref, "review_type": "identity", "verdict": "approve",
        "assessments": [], "issues": [], "approved_bound_ids": [], "summary": NOTICE})
    case = {"case_id": "no-change-science", "paper_ref": paper, "candidate_ref": cref,
        "candidate_review_ref": candidate_review, "identity_ref": iref, "identity_review_ref": ireview,
        "state": "identity_confirmed", "budget_scope": "no-change-toy", "history": [], "jobs": {}}
    engine.ws.save_case(case)
    value = {"engine": engine, "case": case, "profile": p, "prepared": prepared,
             "scope": deepcopy(SCOPE), "calls": [], "errors": [], "review_mutation": None,
             "after_producer": None, "during_reviewer": None, "pause_review": False}
    yield value
    engine.ws.close()


def script_jobs(scenario, monkeypatch):
    e = scenario["engine"]
    def job(role, inputs, scope):
        scenario["calls"].append((role, deepcopy(inputs)))
        jid = e.ws.create_job(role, inputs)
        if role == "profile_reviewer" and scenario["pause_review"]:
            e.ws.save_job(jid, "needs_materials", {})
            return e.ws.job(jid), None
        try:
            h = ToolHost(e.ws, e.atlas, e.ws.job(jid), e.config)
            if role == "bound_updater":
                value = {"candidate_ref": inputs["candidate_ref"], "identity_ref": inputs["identity_ref"],
                    "action": "no_change", "setting_id": inputs["setting_id"], "base_version": inputs["base_version"],
                    "profile_ref": None, "result_refs": [], "proof_refs": [], "issues": [], "change_summary": NOTICE,
                    "research_scope": deepcopy(scenario["scope"]),
                    "coverage_ledger": {"scope": NOTICE, "checks": coverage_checks(), "issue_resolutions": []}}
                kind = "research"
            else:
                assert role == "profile_reviewer"
                prepared = e.artifacts.get(inputs["science_prepared_ref"])["data"]
                value = scientific_review(inputs["subject_ref"], prepared)
                if scenario["review_mutation"]:
                    scenario["review_mutation"](value)
                if scenario["during_reviewer"]:
                    scenario["during_reviewer"]()
                kind = "review"
            ref = h.call("artifact_put", {"kind": kind, "json_text": dumps(value), "dependencies": []}, "freeze-" + kind)["ref"]
            output = {"status": "complete", "artifact_refs": [ref], "summary": NOTICE, "checkpoint_ref": None}
            e._validate_stage(e.ws.job(jid), output)
            e.ws.save_job(jid, "complete", {}, output)
        except ValueError as exc:
            scenario["errors"].append(str(exc))
            e.ws.save_job(jid, "protocol_error", {"last_error": str(exc)})
            return e.ws.job(jid), None
        if role == "bound_updater" and scenario["after_producer"]:
            scenario["after_producer"]()
        return e.ws.job(jid), ref
    monkeypatch.setattr(e, "_job", job)


def atlas_bytes(e):
    return {str(path.relative_to(e.atlas.data)): path.read_bytes()
            for sid in e.atlas.settings.iterdir() if sid.is_dir()
            for name in FILES if (path := sid / name).exists()}


def alter_native_profile(scenario, mutate):
    e = scenario["engine"]
    path = e.atlas.settings / scenario["profile"]["setting_id"] / "profile.json"
    data = json.loads(path.read_text())
    mutate(data)
    path.write_text(dumps(data))


def test_engine_no_change_is_new_independent_snapshot_review_without_receipt_or_write(scenario, monkeypatch):
    e = scenario["engine"]
    before = atlas_bytes(e)
    receipts = {p.name: p.read_bytes() for p in (e.atlas.state / "receipts").glob("*.json")}
    version = e.atlas.version(scenario["profile"]["setting_id"])
    script_jobs(scenario, monkeypatch)
    result = e.resume_case(scenario["case"]["case_id"])
    assert result["state"] == "no_change", scenario["errors"]
    assert [role for role, _ in scenario["calls"]] == ["bound_updater", "profile_reviewer"]
    research = e.artifacts.get(result["research_ref"])["data"]
    snapshot = e.artifacts.get(result["science_prepared_ref"])["data"]
    review = e.artifacts.get(result["profile_review_ref"])["data"]
    assert research["profile_ref"] is None and snapshot["read_only"] is True
    assert snapshot["science"]["research_context"]["scope"] == SCOPE
    assert snapshot["files"]["profile.json"]["research_scope"] == OLD_SCOPE
    assert review["subject_ref"] == result["research_ref"]
    assert {c["check_id"] for c in review["joint_review"]["checks"]} == set(JOINT_CHECKS)
    assert review["joint_review"]["prepared_hash"] == snapshot["bundle_hash"]
    assert review["joint_review"]["analysis_hash"] == snapshot["science"]["analysis_hash"]
    assert review["joint_review"]["science_context_hash"] == snapshot["science_hash"]
    assert "receipt_ref" not in result and "proposal_ref" not in result
    assert e.atlas.version(scenario["profile"]["setting_id"]) == version
    assert atlas_bytes(e) == before
    assert {p.name: p.read_bytes() for p in (e.atlas.state / "receipts").glob("*.json")} == receipts
    assert not e.ws.query("SELECT ref FROM artifacts WHERE kind='receipt'")
    assert e.resume_case(result["case_id"]) == result
    assert len(scenario["calls"]) == 2


@pytest.mark.parametrize("scope", [
    {**SCOPE, "queries_complete": False},
    {**SCOPE, "queries_complete": False, "unresolved_leads": ["An unread synthetic material route."]},
    {**SCOPE, "unresolved_leads": ["An unread synthetic material route."]},
])
def test_engine_no_change_requires_completed_actual_scope(scenario, monkeypatch, scope):
    scenario["scope"] = scope
    script_jobs(scenario, monkeypatch)
    result = scenario["engine"].resume_case(scenario["case"]["case_id"])
    assert result["state"] == "bound_updater:protocol_error"
    assert [role for role, _ in scenario["calls"]] == ["bound_updater"]
    assert scenario["errors"]
    assert "receipt_ref" not in result


@pytest.mark.parametrize("legacy", ["missing", "v1"])
def test_engine_no_change_rejects_legacy_joint_even_with_previous_approval(scenario, monkeypatch, legacy):
    e = scenario["engine"]
    # Emulate a historical Atlas import in the temporary fixture, keeping the
    # previous real writer receipt/approval available as historical evidence.
    alter_native_profile(scenario, lambda p: p.pop("joint_analysis") if legacy == "missing"
                         else p["joint_analysis"].update(version=1))
    old_review = scientific_review(scenario["case"]["identity_ref"], scenario["prepared"])
    scenario["case"]["profile_review_ref"] = e.put("review", old_review)
    e.ws.save_case(scenario["case"])
    script_jobs(scenario, monkeypatch)
    result = e.resume_case(scenario["case"]["case_id"])
    assert result["state"] == "bound_updater:protocol_error"
    assert scenario["errors"] and "joint_analysis" in scenario["errors"][-1]
    assert [role for role, _ in scenario["calls"]] == ["bound_updater"]
    assert "science_prepared_ref" not in result


@pytest.mark.parametrize("fault", ["prepared_hash", "analysis_hash", "science_context_hash", "missing_check", "deferred_check"])
def test_engine_new_no_change_reviewer_must_pin_snapshot_and_all_six_checks(scenario, monkeypatch, fault):
    def mutation(review):
        if fault == "missing_check": review["joint_review"]["checks"].pop()
        elif fault == "deferred_check": review["joint_review"]["checks"][0]["verdict"] = "defer"
        else: review["joint_review"][fault] = "0" * 64
    scenario["review_mutation"] = mutation
    script_jobs(scenario, monkeypatch)
    result = scenario["engine"].resume_case(scenario["case"]["case_id"])
    assert result["state"] == "profile_reviewer:protocol_error"
    assert len(scenario["calls"]) == 2 and scenario["errors"]
    assert "receipt_ref" not in result


def test_engine_no_change_rejects_baseline_changed_after_producer(scenario, monkeypatch):
    scenario["after_producer"] = lambda: alter_native_profile(scenario, lambda p: p.update(title=NOTICE + " External change."))
    script_jobs(scenario, monkeypatch)
    result = scenario["engine"].resume_case(scenario["case"]["case_id"])
    assert result["state"] == "proposal_protocol_error"
    assert "baseline changed" in result["diagnostic"]
    assert [role for role, _ in scenario["calls"]] == ["bound_updater"]


def test_engine_no_change_rejects_baseline_changed_while_independent_reviewer_runs(scenario, monkeypatch):
    scenario["during_reviewer"] = lambda: alter_native_profile(scenario, lambda p: p.update(title=NOTICE + " Concurrent change."))
    script_jobs(scenario, monkeypatch)
    result = scenario["engine"].resume_case(scenario["case"]["case_id"])
    assert result["state"] == "atlas_conflict", "A stale read-only approval cannot certify the changed current baseline"
    assert "baseline changed" in result["diagnostic"]
    assert "receipt_ref" not in result


def test_engine_no_change_rejects_semantic_inventory_change_during_review(scenario, monkeypatch):
    e = scenario["engine"]
    def change_alias():
        (e.atlas.data / "aliases_external.json").write_text(dumps({"synthetic": "Concurrent semantic fixture change."}))
    scenario["during_reviewer"] = change_alias
    script_jobs(scenario, monkeypatch)
    result = e.resume_case(scenario["case"]["case_id"])
    assert result["state"] == "atlas_conflict"
    assert "Atlas changed during no-change review" in result["diagnostic"]
    assert "receipt_ref" not in result


@pytest.mark.parametrize("fault", ["prepared_hash", "analysis_hash", "science_context_hash", "subject_ref", "deferred_check"])
def test_engine_no_change_revalidates_cached_review_instead_of_inheriting_approval(scenario, monkeypatch, fault):
    e = scenario["engine"]
    scenario["pause_review"] = True
    script_jobs(scenario, monkeypatch)
    paused = e.resume_case(scenario["case"]["case_id"])
    assert paused["state"] == "profile_reviewer:needs_materials"
    prepared = e.artifacts.get(paused["science_prepared_ref"])["data"]
    stale = scientific_review(paused["research_ref"], prepared)
    if fault == "subject_ref": stale["subject_ref"] = paused["identity_ref"]
    elif fault == "deferred_check": stale["joint_review"]["checks"][0]["verdict"] = "defer"
    else: stale["joint_review"][fault] = "0" * 64
    # Emulate a schema-valid cached legacy/recovery record. It intentionally
    # bypasses Host freeze here so final consumption must enforce exact review.
    paused["profile_review_ref"] = e.put("review", stale)
    e.ws.save_case(paused)
    result = e.resume_case(paused["case_id"])
    assert result["state"] == "proposal_protocol_error"
    assert result["diagnostic"] and "receipt_ref" not in result
    assert len(scenario["calls"]) == 2  # No extra producer or reviewer execution.
