"""Target metadata adaptation must not implicitly authorize another job's artifacts for the current job."""
from copy import deepcopy
import json
from pathlib import Path
import shutil

import pytest

from oracle_atlas.atlas.store import Atlas
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ProtocolError, references
from oracle_atlas.core.store import Workspace, dumps
from oracle_atlas.tools.host import ToolHost
from test_atlas import approve, facts, profile


@pytest.fixture
def context(tmp_path):
    atlas_root = tmp_path / "atlas"
    shutil.copytree(Path(__file__).parent / "fixtures/native_atlas/data/schemas", atlas_root / "data/schemas")
    atlas = Atlas(atlas_root)
    ws = Workspace(tmp_path / "work")
    other_job = ws.create_job("profile_researcher", {"scope": "another producer"})
    foreign = ws.artifacts.put("proof", {
        "proof_id": "foreign-software-fixture", "origin": "analyst_derivation",
        "proposition": "Engineering permission fixture, not a scientific claim.",
        "premises": [], "argument": "Not used as mathematical evidence.",
        "boundary_cases": "Not applicable.", "quantifiers": "Software fixture only.",
        "resource_accounting": "No model or network calls.", "dependencies": [], "issues": [],
    }, other_job)
    old = profile("AUTHORITY_BOUNDARY")
    old["provenance"] = {"foreign_ref": foreign}
    prepared = atlas.prepare(old, facts(old))
    atlas.commit(prepared, approve(prepared), "seed-synthetic-legacy-profile")
    config = {"atlas": str(atlas_root), "workspace": str(ws.root), "budgets": dict(DEFAULTS), "model": {}}
    raw = profile("AUTHORITY_BOUNDARY")
    raw["title"] = "Incoming unapproved engineering fixture"
    assert references(raw) == set()
    yield atlas, ws, config, raw, foreign
    ws.close()


def make_host(context, *, authorize_foreign=False):
    atlas, ws, config, _, foreign = context
    inputs = {"base_version": atlas.version("AUTHORITY_BOUNDARY")}
    if authorize_foreign:
        inputs["material_refs"] = [foreign]
    job_id = ws.create_job("bound_updater", inputs)
    return ToolHost(ws, atlas, ws.job(job_id), config)


def test_put_rechecks_references_added_by_target_adaptation(context):
    atlas, ws, _, raw, foreign = context
    h = make_host(context)
    baseline = atlas.version("AUTHORITY_BOUNDARY")
    with pytest.raises(ProtocolError):
        h._allowed(foreign)
    with pytest.raises(ProtocolError):
        h._put("profile", deepcopy(raw))
    assert foreign not in h.grants
    assert ws.query("SELECT COUNT(*) n FROM artifacts WHERE kind='profile'")[0]["n"] == 0
    assert atlas.version("AUTHORITY_BOUNDARY") == baseline
    with pytest.raises(ProtocolError):
        h._allowed(foreign)


def test_validate_reports_and_restored_tool_results_cannot_mint_foreign_permission(context):
    atlas, ws, config, raw, foreign = context
    h = make_host(context)
    baseline = atlas.version("AUTHORITY_BOUNDARY")
    draft = h.call("draft_create", {"kind": "profile", "initial_json": json.dumps(raw)}, "authority-draft")
    checked = h.call("draft_validate", {"draft_id": draft["draft_id"],
                    "tag_facts_json": json.dumps(facts(raw))}, "authority-validate")
    assert checked["valid"] is False
    assert checked["error_count"] > 0
    assert foreign not in references(checked)
    assert foreign not in h.grants
    report = h._allowed(checked["report_ref"])
    assert report["kind"] == "external_result"
    assert foreign not in references(report["data"])
    assert foreign not in report["dependencies"]
    assert foreign not in h.grants
    # Native MCP and Responses both persist tool responses; rebuilding a Host must not restore unauthorized references from them.
    with ws.transaction() as db:
        db.execute("INSERT INTO tool_calls VALUES(?,?,?,?,?,?)", (
            "authority-stored-result", h.job["id"], "draft_validate", "{}", dumps(checked), "done"))
    restored = ToolHost(ws, atlas, ws.job(h.job["id"]), config)
    restored._allowed(checked["report_ref"])
    assert foreign not in restored.grants
    with pytest.raises(ProtocolError):
        restored._allowed(foreign)
    assert ws.draft(draft["draft_id"], h.job["id"])["data"] == raw
    assert atlas.version("AUTHORITY_BOUNDARY") == baseline


def test_explicitly_authorized_formal_reference_remains_usable(context):
    _, ws, _, raw, foreign = context
    h = make_host(context, authorize_foreign=True)
    result = h._put("profile", deepcopy(raw))
    stored = h._allowed(result["ref"])
    assert stored["data"]["provenance"]["foreign_ref"] == foreign
    assert foreign in stored["dependencies"]
    assert h._allowed(foreign)["producer"] != h.job["id"]
    assert ws.artifacts.owned(result["ref"], h.job["id"])
