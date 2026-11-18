import pytest

from oracle_atlas.core.config import resources_root
from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.core.store import Workspace, bounded, dumps
from oracle_atlas.runtime.instructions import load_instructions
from oracle_atlas.workflow.joint_review import require_finite_literature, require_frozen_analysis_read, require_joint_checks


def test_three_roles_load_identical_complete_scientific_contract():
    root = resources_root()
    common = ["standards/status_taxonomy.json", "standards/status_taxonomy.md", "standards/joint_parameter_standard.md"]
    manifests = []
    for role in ["bound_updater", "profile_researcher", "profile_reviewer"]:
        text, manifest = load_instructions(role)
        manifests.append({r["path"]: r["sha256"] for r in manifest["loaded"] if r["path"] in common})
        for name in common:
            assert (root/name).read_text("utf-8") in text
    assert manifests[0] == manifests[1] == manifests[2]
    assert "## 7. Structured synthesis" in (root/common[-1]).read_text()
    assert not any(p["path"] in common for p in load_instructions("paper_scanner")[1]["loaded"])


def record(ws, job, call_id, tool, args, result):
    ws.db.execute("INSERT INTO tool_calls VALUES(?,?,?,?,?,?)",
                  (call_id, job, tool, dumps(args), dumps(result), "done"))


def test_review_read_requires_every_page_from_this_job(tmp_path):
    ws = Workspace(tmp_path)
    analysis = {"version": "complete", "domain_map": {"cells": ["local", "unassessed"]}}
    seed = ws.artifacts.put("external_result", {"scope": "fixture"}, "controller")
    ref = ws.artifacts.put("research", {"joint_analysis":analysis, "candidate_ref":seed, "identity_ref":seed,
        "action":"no_change","setting_id":"TOY","base_version":"pinned","profile_ref":None,
        "result_refs":[],"proof_refs":[],"issues":[],"change_summary":"Test scoped reading only."}, "research")
    subject = ws.artifacts.get(ref)
    args = {"ref":ref, "pointer":"/joint_analysis", "offset":0, "limit":25}
    first = bounded(analysis, 0, 25)
    second = bounded(analysis, 25, 200)
    record(ws, "author", "not-review", "artifact_get", args, bounded(analysis, 0, 500))
    record(ws, "review", "first", "artifact_get", args, first)
    with pytest.raises(ProtocolError, match="in full"):
        require_frozen_analysis_read(ws, "review", subject)
    record(ws, "review", "last", "read_batch",
           {"requests":[{"tool":"artifact_get","arguments":{**args, "offset":25}}]}, {"items":[{"result":second}]})
    require_frozen_analysis_read(ws, "review", subject)
    ws.close()


def test_unread_bibliographic_record_cannot_close_scope(tmp_path):
    ws = Workspace(tmp_path)
    analysis = {"synthesis_coverage":{"literature":{"status":"finite_scope_complete"}}}
    ref = ws.artifacts.put("source", {"text":"Pinned mathematical source.", "url":"urn:test:source","version":"baseline","content_hash":"fixture","metadata":{}}, "controller")
    research = {"action":"no_change", "joint_analysis":analysis,
                "literature_scope":{"mode":"bounded_search","source_refs":[ref],"search_refs":[],"unresolved_leads":[]}}
    with pytest.raises(ProtocolError, match="actual|archived searches"):
        require_finite_literature(ws, "research", research)
    research["literature_scope"]["mode"] = "fixed_sources"
    with pytest.raises(ProtocolError, match="actual read"):
        require_finite_literature(ws, "research", research)
    record(ws, "research", "actual-page", "source_read", {"ref":ref}, bounded("Pinned mathematical source."))
    require_finite_literature(ws, "research", research)
    ws.close()


def test_false_joint_check_cannot_approve():
    keys = ["parameter_roles", "guarded_envelopes", "domain_accounting", "improvement_regions", "provenance", "display_consistency"]
    with pytest.raises(ProtocolError, match="requires revise"):
        require_joint_checks({"joint_checks":{**dict.fromkeys(keys, True), "provenance":False}})
