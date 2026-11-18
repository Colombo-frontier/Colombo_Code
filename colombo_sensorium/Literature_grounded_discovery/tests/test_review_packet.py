from copy import deepcopy

from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.workflow.joint_review import require_frozen_analysis_read
from oracle_atlas.workflow.proof_reuse import build_proof_review_context
from oracle_atlas.workflow.review_context import build_review_context
from oracle_atlas.workflow.review_packet import assemble_review_packet, revision_materials
from test_review_context import context
import pytest


def make_packet(c, ref, previous=None):
    ws = c["ws"]
    return assemble_review_packet(ws.artifacts, ref, build_review_context(ws.artifacts, ws, ref, previous),
                                  build_proof_review_context(ws.artifacts, ws, ref, previous))


def test_first_review_gets_bound_source_locator_and_full_read_is_still_required(context):
    c = context
    packet = make_packet(c, c["prior"])
    assert packet["overview"]["mode"] == "full" and len(packet["overview"]["five_file_hashes"]) == 5
    support = c["profile"]["bounds"][0]["result_ref"]
    anchor = packet["evidence"]["results"][support]["source_locators"][0]
    assert anchor["source_ref"] == c["source"] and anchor["locator"] == "fixture" and anchor["version_matches"]
    assert packet["review_scope"]["reusable_bound_ids"] == []
    with pytest.raises(ProtocolError, match="frozen joint_analysis"):
        require_frozen_analysis_read(c["ws"], c["reviewer"], c["ws"].artifacts.get(c["prior"]))


def test_delta_preserves_whole_blocker_and_both_file_pointers(context):
    c = context
    issue = {"issue_id": "bad-scope", "kind": "applicability", "scope": "operator range",
             "message": "Verify the counterexample " * 20, "blocks": ["bound"], "subject_refs": ["u"],
             "evidence_refs": [c["source"]], "resolves": []}
    review, _ = c["review"](issues=[issue], approved=())
    p = deepcopy(c["profile"])
    p["bounds"][0]["statement"] = "A revised assertion awaiting independent assessment."
    ref = c["proposal"](p)
    packet = make_packet(c, ref, review)
    assert packet["overview"]["mode"] == "delta"
    assert packet["prior_issues"] == [issue]
    changes = packet["differences"]["profile.json"]
    bound = next(row for row in changes if row.get("id") == "u" and row.get("after") == "/bounds/0")
    assert bound["before"] == "/bounds/0" and bound["changed_fields"] == ["statement"]
    assert p["bounds"][0]["statement"] in bound["after_excerpt"]
    assert packet["review_scope"]["reusable_bound_ids"] == []
    prior_research = c["ws"].artifacts.get(c["prior"])["data"]["research_ref"]
    repair = revision_materials(c["ws"].artifacts, c["ws"], prior_research, review)
    assert repair["issues"] == [issue] and repair["evidence"]["sources"].get(c["source"])
    assert revision_materials(c["ws"].artifacts, c["ws"], c["source"], review) is None


def test_foreign_producer_verdict_cannot_provide_delta_credentials(context):
    c = context
    review, _ = c["review"](role="profile_researcher")
    packet = make_packet(c, c["prior"], review)
    assert packet["overview"]["mode"] == "full" and packet["prior_issues"] == []
    assert "previous_prepared_ref" not in packet["overview"]


def test_source_snippets_are_exact_substrings_and_undocumented_page_does_not_get_offsets():
    from oracle_atlas.workflow.review_packet import _literal_anchors, _paper_ranges

    text = "Front.\nPrevious citation of Theorem 4.\nA new PDF page.\nTheorem 4. Assumptions matter."
    offset = text.index("A new PDF page")
    source = {"text": text, "metadata": {"locators": [{"page": 2, "start": offset, "end": len(text)}]}}
    ranges = _paper_ranges("Theorem 4, PDF p. 2", source)
    assert ranges[0]["page_start_excerpt"] == text[offset:ranges[0]["excerpt_end"]]
    first = _literal_anchors("Theorem 4, PDF p. 2", text)[0]
    assert first["excerpt"] == text[first["offset"]:first["end"]]
    assert _paper_ranges("Theorem 4, journal p. 2", source) == []
    assert _paper_ranges("PDF p. 3", source) == []


@pytest.mark.parametrize("role", ["profile_reviewer", "bound_updater", "profile_researcher"])
def test_stage_supplies_packet_without_embedding_the_record(context, monkeypatch, role):
    from oracle_atlas.workflow.engine import Engine

    c = context
    ws = c["ws"]
    prop = ws.artifacts.get(c["prior"])["data"]
    engine = Engine.__new__(Engine)
    engine.ws, engine.artifacts = ws, ws.artifacts
    case = {"case_id": "fixture", "id": "fixture", "jobs": {}, "candidate_ref": prop["candidate_ref"],
            "repair_feedback_ref": c["prior_review"], "previous_artifact_ref": prop["research_ref"],
            "budget_scope": "fixture"}
    captured = {}
    monkeypatch.setattr(ws, "save_case", lambda case: None)

    def job(role, inputs, scope):
        captured.update(inputs)
        return {"id": "fixture-stage", "status": "queued"}, None

    monkeypatch.setattr(engine, "_job", job)
    inputs = {"subject_ref": c["prior"]} if role == "profile_reviewer" else {"identity_ref": prop["identity_ref"]}
    engine._stage(case, role, inputs)
    name = "review_packet_ref" if role == "profile_reviewer" else "revision_materials_ref"
    packet = ws.artifacts.get(captured[name])["data"]
    assert packet.get("subject_ref", packet.get("overview", {}).get("subject_ref")) == c["prior"]
    assert "evidence" not in captured and "differences" not in captured
    if role == "profile_reviewer":
        assert packet["review_scope"]["proof_scope_revalidation_index"] == {
            "ref": captured["proof_context_ref"], "pointer": "/proof_scope_revalidation_candidates", "count": 0}


def test_scope_revalidation_packet_points_to_formal_deltas_without_copying_them(context):
    from oracle_atlas.core.contracts import resolve_pointer
    from oracle_atlas.core.store import dumps

    c, ws = context, context["ws"]
    ref = c["prior"]
    bounds = build_review_context(ws.artifacts, ws, ref)
    proofs = build_proof_review_context(ws.artifacts, ws, ref)
    # Navigation fixture, not a controller-verified eligibility claim.
    proofs["proof_scope_revalidation_candidates"] = [{"candidate_id": "fixture-navigation",
        "proof_ref": c["source"], "context_changes": {"changes": [{"excerpt": "x" * 9000}], "truncated": True},
        "new_issue_occurrence_ids": ["fixture-occurrence"]}]
    catalog_ref = ws.artifacts.put("external_result", proofs, "controller")
    packet = assemble_review_packet(ws.artifacts, ref, bounds, proofs, proof_context_ref=catalog_ref)
    row = packet["review_scope"]["proof_scope_revalidation_candidates"][0]
    assert row == {"candidate_id": "fixture-navigation", "proof_ref": c["source"],
        "context_change_count": 1, "context_changes_truncated": True, "new_issue_occurrence_count": 1,
        "details": {"ref": catalog_ref, "pointer": "/proof_scope_revalidation_candidates/0"}}
    formal = ws.artifacts.get(row["details"]["ref"])["data"]
    assert resolve_pointer(formal, row["details"]["pointer"]) == proofs["proof_scope_revalidation_candidates"][0]
    assert "x" * 9000 not in dumps(packet)
    assert packet["review_scope"]["reusable_proof_refs"] == []


@pytest.mark.parametrize("producer", ["profile_researcher", "bound_updater"])
@pytest.mark.parametrize("already_cleared", [False, True])
def test_material_resume_after_interrupted_repair_preserves_delta_and_clone(context, monkeypatch, producer, already_cleared):
    from oracle_atlas.workflow.engine import Engine

    c, ws = context, context["ws"]
    old = ws.artifacts.get(c["prior"])["data"]
    paper_ref = ws.artifacts.get(old["candidate_ref"])["data"]["paper_refs"][0]
    origin = {"case_id": "material-resume", "state": producer + ":needs_materials", "paper_ref": paper_ref,
              "candidate_ref": old["candidate_ref"], "identity_ref": old["identity_ref"],
              "budget_scope": "fixture", "repair_feedback_ref": c["prior_review"],
              "previous_artifact_ref": old["research_ref"]}
    case = {**origin, "history": [], "jobs": {}}
    if already_cleared:
        case.update(previous_artifact_ref=None, repair_feedback_ref=None, history=[origin])
    ws.save_case(case)
    e = Engine.__new__(Engine)
    e.ws, e.artifacts, e.config = ws, ws.artifacts, {}
    captured = {}
    def job(role, inputs, scope):
        captured[role] = inputs
        return {"id": "interrupted-" + role, "status": "needs_materials"}, None

    monkeypatch.setattr(e, "_job", job)
    changed = deepcopy(c["profile"])
    changed["bounds"][0]["statement"] = "A changed assertion that requires an independent decision."
    fresh = c["proposal"](changed)
    def advance(state):
        e._stage(state, producer, {"identity_ref": old["identity_ref"]})
        e._stage(state, "profile_reviewer", {"subject_ref": fresh})
        return state
    monkeypatch.setattr(e, "_advance", advance)
    e.resume_case(case["case_id"], stage="research", material_refs=[c["source"]])
    assert captured[producer]["previous_artifact_ref"] == old["research_ref"]
    assert captured[producer]["profile_clone_source"]["source_ref"] == ws.artifacts.get(old["research_ref"])["data"]["profile_ref"]
    assert captured[producer]["repair_feedback_ref"] == c["prior_review"]
    assert ws.artifacts.get(captured[producer]["revision_materials_ref"])["data"]["review_ref"] == c["prior_review"]
    dossier = ws.artifacts.get(captured["profile_reviewer"]["review_packet_ref"])["data"]
    assert dossier["overview"]["mode"] == "delta" and dossier["overview"]["previous_review_ref"] == c["prior_review"]
    assert any(r.get("id") == "u" for r in dossier["differences"]["profile.json"])
