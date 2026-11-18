"""Format preflight through actual tools; no model calls or scientific approval of papers."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys

import pytest

from oracle_atlas.atlas.store import Atlas
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ValidationDiagnostics
from oracle_atlas.core.store import Workspace
from oracle_atlas.tools.host import ToolHost
from test_atlas import profile, facts


@pytest.fixture
def context(tmp_path):
    atlas_root = tmp_path / "atlas"
    shutil.copytree(Path(__file__).parent / "fixtures/native_atlas/data/schemas", atlas_root / "data/schemas")
    atlas = Atlas(atlas_root)
    ws = Workspace(tmp_path / "work")
    config = {"atlas": str(atlas_root), "workspace": str(ws.root), "budgets": dict(DEFAULTS), "model": {}}
    yield atlas, ws, config
    ws.close()


def host(context, role="profile_researcher", inputs=None):
    atlas, ws, config = context
    jid = ws.create_job(role, inputs or {})
    return ToolHost(ws, atlas, ws.job(jid), config)


def call(h, tool, **args):
    return h.call(tool, args, tool + str(len(h.ws.query("SELECT * FROM artifacts"))))


def candidate(p, paper):
    return {"candidate_id": "synthetic-preflight", "title": p["title"], "paper_refs": [paper],
            "common_specification": deepcopy(p["common_specification"]), "views": deepcopy(p["views"]),
            "tag_facts": facts(p), "issues": []}


def test_target_schema_is_exposed_and_profile_metadata_adapts_before_freeze(context):
    h = host(context)
    exposed = call(h, "schema_read", kind="profile")
    assert exposed["target_atlas"]["profile_contract"]["schema_version"]["const"] == "native-profile"
    value = call(h, "target_schema_read", name="profile", pointer="/properties/schema_version/const", offset=0, limit=1000)
    assert value.get("data", value.get("text")) == "native-profile"
    original = profile("PREFLIGHT_NEW")
    draft = call(h, "draft_create", kind="profile", initial_json=json.dumps(original))
    bad = facts(original)
    bad[0]["source_pointer"] = "/missing/task"
    bad[1]["source_pointer"] = "/missing/model"
    failed = call(h, "draft_validate", draft_id=draft["draft_id"], tag_facts_json=json.dumps(bad))
    assert not failed["valid"] and failed["error_count"] >= 2
    assert "projection_preview_ref" not in failed
    report = h._allowed(failed["report_ref"])["data"]
    assert any("/missing/task" in e["message"] for e in report["errors"])
    assert any("/missing/model" in e["message"] for e in report["errors"])
    assert not list(h.atlas.settings.glob("*/profile.json"))
    passed = call(h, "draft_validate", draft_id=draft["draft_id"], tag_facts_json=json.dumps(facts(original)))
    preview = h._allowed(passed["projection_preview_ref"])["data"]
    assert preview["bundle_hash"] == passed["bundle_hash"]
    assert set(preview["files"]) == {"profile.json","identity.json","classification.json","human_tags.json","machine_tags.json"}
    assert set(preview["hashes"]) == set(preview["files"])
    assert not list(h.atlas.settings.glob("*/profile.json"))
    assert passed["valid"], passed
    frozen = call(h, "draft_freeze", draft_id=draft["draft_id"])
    result = h.artifacts.get(frozen["ref"])["data"]
    assert result["schema_version"] == "native-profile"
    assert result["common_specification"] == original["common_specification"]
    assert result["bounds"] == original["bounds"]
    assert result["provenance"]["source_schema_version"] == "component-profile"
    assert h.ws.query("SELECT COUNT(*) n FROM jobs")[0]["n"] == 1
    assert not (h.ws.root / "transport").exists()


def test_candidate_id_paths_are_normalized_before_formal_extraction(context):
    atlas, ws, _ = context
    paper = ws.artifacts.put("paper", {"title": "Synthetic fixture", "doi": None, "arxiv_id": None,
                                     "urls": [], "publication_events": [], "provenance": []}, "seed")
    h = host(context, "extractor", {"paper_ref": paper})
    value = candidate(profile("PREFLIGHT_NEW"), paper)
    oracle = value["tag_facts"][2]
    oracle.update(view_ref="/views/0", operation_ref="/operations/0", object_ref="A", source_pointer="/operations/0")
    frozen = call(h, "artifact_put", kind="candidate", json_text=json.dumps(value), dependencies=[])
    stored = h.artifacts.get(frozen["ref"])["data"]
    assert stored["tag_facts"][2]["view_ref"] == "randomized"
    assert stored["tag_facts"][2]["operation_ref"] == "right"
    assert stored["tag_facts"][2]["source_pointer"] == "/common_specification/oracle/operations/0"
    bad = deepcopy(value)
    bad["tag_facts"][2]["operation_ref"] = "/operations/999"
    with pytest.raises(ValidationDiagnostics) as error:
        call(h, "artifact_put", kind="candidate", json_text=json.dumps(bad), dependencies=[])
    assert error.value.diagnostics
    assert h._allowed(error.value.report_ref)["kind"] == "external_result"
    assert ws.query("SELECT COUNT(*) n FROM artifacts WHERE kind='candidate'")[0]["n"] == 1


def test_prepared_sidecars_follow_target_interface_identifiers(context):
    atlas, _, _ = context
    expected = {}
    for name in ("identity", "classification"):
        path = atlas.data / "schemas" / (name + ".schema.json")
        definition = json.loads(path.read_text())
        expected[name + ".json"] = "target-" + name + "-interface"
        definition["properties"]["schema_version"] = {"const": expected[name + ".json"]}
        path.write_text(json.dumps(definition))
    incoming = profile("TARGET_INTERFACE")
    prepared = atlas.prepare(incoming, facts(incoming))
    for filename, identifier in expected.items():
        assert prepared["files"][filename]["schema_version"] == identifier
        assert any(change.get("file") == filename for change in prepared["schema_adaptation"])
    assert prepared["mechanical_validation"]["status"] == "passed"
    assert not list(atlas.settings.glob("*/profile.json"))


def test_relations_are_not_silently_turned_into_mathematical_comparison_keys(context):
    h = host(context)
    p = profile("BAD_COMPARISON")
    p["comparisons"] = [{"comparison_id": "nearby-setting", "description": "Related native interface, not a complexity bracket."}]
    p["tag_facts"] = facts(p)
    p["tag_facts"][0]["source_pointer"] = "/missing/task"
    d = call(h, "draft_create", kind="profile", initial_json=json.dumps(p))
    checked = call(h, "draft_validate", draft_id=d["draft_id"], tag_facts_json="")
    assert not checked["valid"]
    report = h._allowed(checked["report_ref"])["data"]
    assert any(e["code"] == "comparison_binding" for e in report["errors"])
    assert any(e["code"] == "unresolved_source_pointer" for e in report["errors"])
    # The researcher must provide scientific comparison keys explicitly; preflight neither guesses view/regime nor moves relational prose.
    assert h.ws.draft(d["draft_id"], h.job["id"])["data"] == p


def test_research_save_checks_final_facts_before_a_handoff_or_new_session(context):
    atlas, ws, _ = context
    p = profile("PREFLIGHT_NEW")
    paper = ws.artifacts.put("paper", {"title": "Synthetic fixture", "doi": None, "arxiv_id": None,
                                     "urls": [], "publication_events": [], "provenance": []}, "seed")
    cref = ws.artifacts.put("candidate", candidate(p, paper), "seed")
    retrieval = ws.artifacts.put("retrieval", {"candidate_ref": cref}, "seed")
    iref = ws.artifacts.put("identity", {"candidate_ref": cref, "decision": "new", "setting_id": None,
        "view_mapping": [{"candidate_view_id": "randomized", "atlas_view_id": None, "reason": "Unassessed test mapping."}],
        "normalization": "Synthetic software test.", "comparisons": [], "retrieval_ref": retrieval,
        "recall_audit": {"strategies": [], "unresolved_ids": [], "reason": "Software test only.", "inventory_version": atlas.version()},
        "issues": []}, "seed")
    h = host(context, inputs={"candidate_ref": cref, "identity_ref": iref, "base_version": None})
    pref = call(h, "artifact_put", kind="profile", json_text=json.dumps(p), dependencies=[])["ref"]
    data = {"candidate_ref": cref, "identity_ref": iref, "action": "new", "setting_id": p["setting_id"],
            "base_version": None, "profile_ref": pref, "result_refs": [], "proof_refs": [], "issues": [],
            "change_summary": "Synthetic interface check, not an adopted theorem.", "tag_facts": facts(p)}
    data["tag_facts"][0]["source_pointer"] = "/nonexistent/candidate/layout"
    with pytest.raises(ValidationDiagnostics):
        call(h, "artifact_put", kind="research", json_text=json.dumps(data), dependencies=[])
    assert ws.query("SELECT COUNT(*) n FROM artifacts WHERE kind='research'")[0]["n"] == 0
    data["tag_facts"] = facts(p)
    result = call(h, "artifact_put", kind="research", json_text=json.dumps(data), dependencies=[])
    assert h.artifacts.get(result["ref"])["data"]["tag_facts"] == facts(p)
    assert not list(atlas.settings.glob("*/profile.json"))


def test_native_stdio_mcp_exposes_target_schema_and_aggregated_preflight(context, tmp_path):
    pytest.importorskip("mcp")
    from oracle_atlas.providers.mcp import MCPBridge
    atlas, ws, config = context
    config_path = tmp_path / "config.toml"
    config_path.write_text(f'workspace = {json.dumps(str(ws.root))}\natlas = {json.dumps(str(atlas.root))}\n')
    jid = ws.create_job("profile_researcher", {})
    project = Path(__file__).resolve().parents[1]
    with MCPBridge([{"name": "test", "transport": "stdio", "command": sys.executable,
                    "args": ["-m", "oracle_atlas", "mcp", "--config", str(config_path), "--job", jid],
                    "env": {"PYTHONPATH": str(project / "src")}, "timeout": 15,
                    "allowed_tools": ["target_schema_read", "draft_create", "draft_validate", "draft_freeze"]}]) as bridge:
        def run(name, args):
            out = bridge.call("mcp__test__" + name, args)
            return json.loads(next(part["text"] for part in out["content"] if part["type"] == "text"))
        value = run("target_schema_read", {"name": "profile", "pointer": "/properties/schema_version/const", "offset": 0, "limit": 1000})
        assert value.get("data", value.get("text")) == "native-profile"
        p = profile("STDIO_PREFLIGHT")
        p["tag_facts"] = facts(p)
        p["tag_facts"][0]["source_pointer"] = "/missing/task"
        p["tag_facts"][1]["source_pointer"] = "/missing/model"
        draft = run("draft_create", {"kind": "profile", "initial_json": json.dumps(p)})
        checked = run("draft_validate", {"draft_id": draft["draft_id"], "tag_facts_json": ""})
        assert not checked["valid"] and checked["error_count"] >= 2
        failed = run("draft_freeze", {"draft_id": draft["draft_id"]})
        assert failed["error_type"] == "ValidationDiagnostics"
        assert failed["error_count"] >= 2 and failed["report_ref"].startswith("sha256:")
    assert not list(atlas.settings.glob("*/profile.json"))
