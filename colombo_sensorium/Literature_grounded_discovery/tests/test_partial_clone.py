from copy import deepcopy

import pytest

from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.core.store import digest
from oracle_atlas.tools.host import ToolHost
from oracle_atlas.workflow.engine import Engine
from test_review_context import context


@pytest.mark.parametrize("failure", [None, "ambiguous", "other_job", "foreign_profile", "candidate", "identity",
                                      "setting", "base", "different_action", "unreturned", "no_handoff", "work_set"])
def test_material_resume_clones_unique_partial_in_actual_tool_or_uses_old_profile(context, monkeypatch, failure):
    c, ws = context, context["ws"]
    original = ws.artifacts.get(c["prior"])["data"]
    previous = ws.artifacts.get(original["research_ref"])["data"]
    base_inputs = {"candidate_ref": original["candidate_ref"], "identity_ref": original["identity_ref"],
                   "setting_id": None, "base_version": None, "budget_scope": "fixture"}
    role = "profile_researcher"
    job_id = ws.create_job(role, base_inputs)
    owner = "another-author" if failure == "other_job" else job_id
    p = deepcopy(c["profile"]); p["reader_markdown"] = "Unapproved repair progress."
    if failure == "setting":
        p["setting_id"] = "OTHER_SETTING"
    profile_ref = ws.artifacts.put("profile", p, "foreign-owner" if failure == "foreign_profile" else owner)
    research = {**previous, "profile_ref": profile_ref, "setting_id": p["setting_id"]}
    if failure == "candidate":
        research["candidate_ref"] = c["source"]
    if failure == "identity":
        research["identity_ref"] = c["source"]
    if failure == "base":
        research["base_version"] = "changed"
    if failure == "different_action":
        research["action"] = "update"
    ref = ws.artifacts.put("research", research, owner)
    returned = [] if failure == "unreturned" else [ref]
    if failure == "ambiguous":
        returned.append(ws.artifacts.put("research", {**research, "change_summary": "second study"}, owner))
    ws.save_job(job_id, "needs_materials", {}, {"status": "needs_materials", "artifact_refs": returned,
                                                "summary": "Unapproved fixture.", "checkpoint_ref": None})
    if failure != "no_handoff":
        ws.event(job_id, "validated_handoff", {"status": "needs_materials", "refs": returned})
    inputs = {**base_inputs, "resume_producer_job_id": job_id}
    case = {"case_id": "partial-clone", "candidate_ref": original["candidate_ref"],
            "identity_ref": original["identity_ref"], "previous_artifact_ref": original["research_ref"],
            "budget_scope": "fixture", "jobs": {role:job_id}, "partial_refs": {role: [] if failure == "work_set" else [ref, *returned]},
            "repair_feedback_ref": c["prior_review"], "history": [], "state": role + ":needs_materials",
            "paper_ref": ws.artifacts.get(original["candidate_ref"])["data"]["paper_refs"][0]}
    e = Engine.__new__(Engine)
    e.ws, e.artifacts, e.config = ws, ws.artifacts, {"budgets":dict(DEFAULTS)}
    captured = {}
    def launch(stage, values, scope):
        captured.update(values, budget_scope=scope)
        return {"id":"paused", "status":"needs_materials"}, None
    monkeypatch.setattr(e, "_job", launch)
    monkeypatch.setattr(e, "_advance", lambda s: e._stage(s, role, {k:v for k,v in base_inputs.items() if k != "budget_scope"}))
    ws.save_case(case)
    e.resume_case(case["case_id"], stage="research", material_refs=[c["source"]])
    assert captured["previous_artifact_ref"] == original["research_ref"] and captured["repair_feedback_ref"] == c["prior_review"]
    selected = captured["profile_clone_source"]
    assert selected["source_ref"] == (previous["profile_ref"] if failure else profile_ref)
    assert captured["resume_producer_job_id"] == job_id
    def host(values):
        jid = ws.create_job(role, values)
        return ToolHost(ws, c["atlas"], ws.job(jid), e.config)
    h = host(captured)
    result = h.call("draft_clone", selected, "accepted")
    assert ws.draft(result["draft_id"], h.job["id"])["data"] == ws.artifacts.get(selected["source_ref"])["data"]
    # Even when an immutable profile is readable as a reference, a forged clone descriptor
    # cannot grant a different author's draft or pick one of multiple partials.
    if failure:
        counterfeit = {"source_ref":profile_ref,"source_pointer":"","expected_digest":digest(p)}
        with pytest.raises(ProtocolError):
            host({**captured,"profile_clone_source":counterfeit}).call("draft_clone",counterfeit,"forged")
