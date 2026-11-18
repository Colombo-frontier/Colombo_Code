"""Science gates at actual Host freeze boundaries; all science is synthetic."""
from copy import deepcopy
import json

import pytest

from oracle_atlas.atlas.store import Atlas
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ValidationDiagnostics
from oracle_atlas.core.store import Workspace, digest, dumps
from oracle_atlas.science.gates import research_context
from oracle_atlas.tools.host import ToolHost
from test_atlas import profile, facts, approve, _SYNTHETIC
from test_preflight_pipeline import candidate


NOTICE = "Explicit synthetic Host boundary test; no real research."
SCOPE = {"scope": NOTICE, "queries_complete": True, "unresolved_leads": []}


@pytest.fixture
def environment(tmp_path):
    atlas = Atlas(tmp_path / "atlas")
    ws = Workspace(tmp_path / "work")
    config = {"atlas": str(atlas.root), "workspace": str(ws.root), "budgets": dict(DEFAULTS), "model": {}}
    yield atlas, ws, config
    ws.close()


def host(environment, role="profile_researcher", inputs=None):
    atlas, ws, config = environment
    jid = ws.create_job(role, inputs or {})
    return ToolHost(ws, atlas, ws.job(jid), config)


def freeze(h, kind, data):
    return h.call("artifact_put", {"kind": kind, "json_text": dumps(data), "dependencies": []}, "freeze-" + kind)


def finite_profile(sid="HOST_FINITE"):
    p = profile(sid)
    p["research_scope"] = deepcopy(SCOPE)
    p["joint_analysis"]["synthesis_coverage"]["literature"] = {"status": "finite_scope_complete", "scope": NOTICE}
    return p


def scientific_review(subject_ref, prepared):
    return {"subject_ref": subject_ref, "review_type": "profile", "verdict": "approve", "assessments": [],
            "issues": [], "approved_bound_ids": ["u"], "summary": NOTICE,
            "joint_review": _SYNTHETIC.synthetic_joint_review(prepared)}


def test_profile_declares_scope_before_freeze_and_preflight_binds_real_tool_trace(environment, monkeypatch):
    h = host(environment)
    p = finite_profile()
    # This is an observed local synthetic tool event, not a network request.
    with h.ws.transaction() as db:
        db.execute("INSERT INTO tool_calls VALUES(?,?,?,?,?,?)", (
            "synthetic-source-read", h.job["id"], "source_read", "{}", "{}", "done"))
    captured = []
    original = h.atlas.preflight
    def observe(*args, **kwargs):
        captured.append(deepcopy(kwargs["research_context"]))
        return original(*args, **kwargs)
    monkeypatch.setattr(h.atlas, "preflight", observe)
    draft = h.call("draft_create", {"kind": "profile", "initial_json": dumps(p)}, "draft")
    checked = h.call("draft_validate", {"draft_id": draft["draft_id"], "tag_facts_json": dumps(facts(p))}, "check")
    assert checked["valid"], checked
    context = captured[-1]
    assert context["scope"] == SCOPE and context["producer_job"] == h.job["id"]
    assert context["observations"]["tool_call_count"] == 1
    assert context["authority"] == "producer_declaration_with_controller_log_binding"
    saved = h.call("draft_freeze", {"draft_id": draft["draft_id"]}, "freeze")
    assert h.artifacts.get(saved["ref"])["data"]["research_scope"] == SCOPE
    assert not list(h.atlas.settings.glob("*/profile.json"))


def test_missing_pre_freeze_scope_cannot_claim_finished_literature(environment):
    h = host(environment)
    p = finite_profile(); p.pop("research_scope")
    with pytest.raises(ValidationDiagnostics) as error:
        freeze(h, "profile", p)
    assert any("actual finished research scope" in x["message"] for x in error.value.diagnostics)
    assert freeze(h, "profile", profile("HOST_UNASSESSED"))["ref"]


def test_expansion_neighbor_never_becomes_a_scientific_baseline(environment):
    atlas, ws, _ = environment
    p = profile("HOST_NEW")
    neighbor = ws.artifacts.put("native_record", {"setting_id": p["setting_id"], "version": "historical-neighbor",
                                                "content": deepcopy(p)}, "controller")
    h = host(environment, inputs={"base_version": None, "base_profile_ref": neighbor, "seed_refs": [neighbor]})
    p["joint_analysis"]["provenance"][0]["origin"] = "retained_baseline"
    with pytest.raises(ValidationDiagnostics) as error:
        freeze(h, "profile", p)
    assert any("no accepted scientific baseline" in x["message"] for x in error.value.diagnostics)


def test_update_requires_exact_controller_pinned_target_baseline(environment):
    atlas, ws, _ = environment
    p = profile("HOST_EXISTING")
    initial = atlas.prepare(p, facts(p)); atlas.commit(initial, approve(initial), "seed-host-existing")
    current = atlas.read(p["setting_id"]); version = atlas.version(p["setting_id"])
    incoming = deepcopy(current)
    incoming["joint_analysis"]["provenance"][0]["origin"] = "retained_baseline"
    h = host(environment, "bound_updater", {"setting_id": p["setting_id"], "base_version": version})
    with pytest.raises(ValidationDiagnostics) as missing:
        freeze(h, "profile", incoming)
    assert any("base_profile_ref" in x["message"] for x in missing.value.diagnostics)
    bad = ws.artifacts.put("native_record", {"setting_id": p["setting_id"], "version": "stale", "content": current}, "controller")
    h = host(environment, "bound_updater", {"setting_id": p["setting_id"], "base_version": version, "base_profile_ref": bad})
    with pytest.raises(ValidationDiagnostics) as mismatch:
        freeze(h, "profile", incoming)
    assert any("base_version" in x["message"] for x in mismatch.value.diagnostics)
    pinned = ws.artifacts.put("native_record", {"setting_id": p["setting_id"], "version": version, "content": current}, "controller")
    h = host(environment, "bound_updater", {"setting_id": p["setting_id"], "base_version": version, "base_profile_ref": pinned})
    assert freeze(h, "profile", incoming)["ref"]
    assert atlas.version(p["setting_id"]) == version


def research_fixture(environment):
    atlas, ws, _ = environment
    p = finite_profile("HOST_RESEARCH")
    paper = ws.artifacts.put("paper", {"title": NOTICE, "doi": None, "arxiv_id": None,
        "urls": [], "publication_events": [], "provenance": [], "synthetic": True}, "controller")
    cref = ws.artifacts.put("candidate", candidate(p, paper), "controller")
    retrieval = ws.artifacts.put("retrieval", {"candidate_ref": cref}, "controller")
    identity = {"candidate_ref": cref, "decision": "new", "setting_id": None,
                "view_mapping": [{"candidate_view_id": "randomized", "atlas_view_id": None, "reason": NOTICE}],
                "normalization": NOTICE, "comparisons": [], "retrieval_ref": retrieval,
                "recall_audit": {"strategies": [], "unresolved_ids": [], "reason": NOTICE, "inventory_version": atlas.version()},
                "issues": []}
    iref = ws.artifacts.put("identity", identity, "controller")
    h = host(environment, inputs={"candidate_ref": cref, "identity_ref": iref, "base_version": None})
    pref = freeze(h, "profile", p)["ref"]
    research = {"candidate_ref": cref, "identity_ref": iref, "action": "new", "setting_id": p["setting_id"],
                "base_version": None, "profile_ref": pref, "result_refs": [], "proof_refs": [], "issues": [],
                "change_summary": NOTICE, "tag_facts": facts(p), "research_scope": deepcopy(SCOPE)}
    return h, p, research


def test_final_research_scope_must_match_profile_and_reach_preflight(environment, monkeypatch):
    h, p, research = research_fixture(environment)
    observed = []
    original = h.atlas.preflight
    def capture(*args, **kwargs):
        observed.append(kwargs["research_context"])
        return original(*args, **kwargs)
    monkeypatch.setattr(h.atlas, "preflight", capture)
    mismatched = deepcopy(research); mismatched["research_scope"]["scope"] = "Different synthetic scope."
    with pytest.raises(ValidationDiagnostics) as error:
        freeze(h, "research", mismatched)
    assert any(x["code"] == "research_scope_mismatch" for x in error.value.diagnostics)
    result = freeze(h, "research", research)
    assert h.artifacts.get(result["ref"])["data"]["research_scope"] == SCOPE
    assert observed[-1]["scope"] == SCOPE and observed[-1]["producer_job"] == h.job["id"]


def test_research_cannot_hide_unconfirmed_external_call_as_completed(environment):
    h, _, research = research_fixture(environment)
    with h.ws.transaction() as db:
        db.execute("INSERT INTO tool_calls VALUES(?,?,?,?,?,?)", (
            "pending-request", h.job["id"], "bibliography_search", "{}", None, "pending"))
    with pytest.raises(ValidationDiagnostics) as error:
        freeze(h, "research", research)
    assert any("unconfirmed external calls" in x["message"] for x in error.value.diagnostics)


def review_fixture(environment, *, no_change=False):
    atlas, ws, _ = environment
    p = profile("HOST_REVIEW")
    prepared = atlas.prepare(p, facts(p))
    if no_change:
        atlas.commit(prepared, approve(prepared), "seed-review-snapshot")
        prepared = atlas.review_snapshot(p["setting_id"], atlas.version(p["setting_id"]),
            research_context={"scope": {"scope": NOTICE, "queries_complete": False, "unresolved_leads": []}})
        marker = ws.artifacts.put("external_result", {"synthetic": True}, "controller")
        subject = ws.artifacts.put("research", {"candidate_ref": marker, "identity_ref": marker,
            "action": "no_change", "setting_id": p["setting_id"], "base_version": atlas.version(p["setting_id"]),
            "profile_ref": None, "result_refs": [], "proof_refs": [], "issues": [], "change_summary": NOTICE,
            "research_scope": {"scope": NOTICE, "queries_complete": False, "unresolved_leads": []}}, "producer")
        pref = ws.artifacts.put("prepared", prepared, "controller")
        inputs = {"subject_ref": subject, "science_prepared_ref": pref}
    else:
        pref = ws.artifacts.put("prepared", prepared, "controller")
        marker = ws.artifacts.put("external_result", {"synthetic": True}, "controller")
        subject = ws.artifacts.put("proposal", {"research_ref": marker, "candidate_ref": marker, "identity_ref": marker,
            "profile_ref": marker, "prepared_ref": pref, "change_summary": NOTICE, "base_version": None,
            "inventory_version": atlas.version(), "mode": "new"}, "controller")
        inputs = {"subject_ref": subject}
    h = host(environment, "profile_reviewer", inputs)
    return h, scientific_review(subject, prepared), prepared


@pytest.mark.parametrize("no_change", [False, True])
def test_profile_reviews_bind_exact_proposal_or_no_change_science_snapshot(environment, no_change):
    h, review, prepared = review_fixture(environment, no_change=no_change)
    bad = deepcopy(review); bad["joint_review"]["science_context_hash"] = "0" * 64
    with pytest.raises(ValidationDiagnostics) as error:
        freeze(h, "review", bad)
    assert any("science_context_hash" in x["message"] for x in error.value.diagnostics)
    assert freeze(h, "review", review)["ref"]
    assert prepared["science_hash"] == review["joint_review"]["science_context_hash"]


def test_profile_reviewer_cannot_switch_subject_or_self_review(environment):
    h, review, prepared = review_fixture(environment)
    other_proposal = deepcopy(h.artifacts.get(h.job["inputs"]["subject_ref"])["data"])
    other_proposal["change_summary"] += " Distinct self-produced boundary fixture."
    other = h.artifacts.put("proposal", other_proposal, h.job["id"])
    changed = deepcopy(review); changed["subject_ref"] = other
    with pytest.raises(ValidationDiagnostics) as error:
        freeze(h, "review", changed)
    assert any("fixed subject_ref" in x["message"] for x in error.value.diagnostics)
    # Even an input-pinned self-produced subject has no independent-review authority.
    h.job["inputs"]["subject_ref"] = other
    with pytest.raises(ValidationDiagnostics) as error:
        freeze(h, "review", changed)
    assert any("own subject" in x["message"] for x in error.value.diagnostics)
