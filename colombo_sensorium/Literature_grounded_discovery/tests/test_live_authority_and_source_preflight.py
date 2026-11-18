"""Live same-job authorization and early source-version validation; engineering fixtures only, without models or scientific approval."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys

import pytest

from oracle_atlas.atlas.store import Atlas
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ProtocolError, ValidationDiagnostics, references
from oracle_atlas.core.store import Workspace, dumps
from oracle_atlas.tools.host import ToolHost
from test_atlas import approve, facts, profile


@pytest.fixture
def context(tmp_path):
    root = tmp_path / "atlas"
    shutil.copytree(Path(__file__).parent / "fixtures/native_atlas/data/schemas", root / "data/schemas")
    atlas, ws = Atlas(root), Workspace(tmp_path / "work")
    config = {"atlas": str(root), "workspace": str(ws.root), "budgets": dict(DEFAULTS), "model": {}}
    yield atlas, ws, config
    ws.close()


def make_host(context, inputs=None, *, workspace=None, job_id=None):
    atlas, ws, config = context
    jid = job_id or ws.create_job("profile_researcher", inputs or {})
    return ToolHost(workspace or ws, atlas, (workspace or ws).job(jid), config)


def invoke(host, name, **args):
    return host.call(name, args, f"{name}-{len(host.ws.query('SELECT * FROM artifacts'))}-{len(host.ws.query('SELECT * FROM drafts'))}")


def checkpoint(summary="Fixture", refs=()):
    return {"summary": summary, "refs": list(refs), "remaining": []}


def source(ws, producer="seed", version="f" * 64):
    return ws.artifacts.put("source", {"url": "https://example.org/source-fixture", "version": version,
        "content_hash": "f" * 64, "text": "Software fixture only.", "metadata": {}}, producer)


def result(ref, version="f" * 64):
    return {"result_id": "version-fixture", "comparison_key": {"setting_id": "VERSION_FIXTURE", "view_id": "randomized",
        "guarantee_id": "g", "quantity_id": "q", "resource_projection_id": "rp", "regime_id": "r"},
        "direction": "upper", "statement": "Engineering fixture, not a mathematical claim.", "formula_latex": "1",
        "conditions": [], "parameter_region": "Software fixture only.", "algorithm_scope": "No scientific adoption.",
        "witness_type": "deterministic", "guarantee": "Software fixture only.", "resource_accounting": "No model calls.",
        "origin": "published_theorem", "source_refs": [ref],
        "source_locators": [{"source_ref": ref, "version": version, "locator": "fixture p.1"}],
        "proof_refs": [], "status": "proposed", "issues": []}


def test_two_live_hosts_share_only_current_job_owned_objects(context):
    atlas, ws, config = context
    first = make_host(context)
    second_ws = Workspace(ws.root)
    try:
        second = make_host(context, workspace=second_ws, job_id=first.job["id"])
        created = invoke(first, "artifact_put", kind="checkpoint", json_text=json.dumps(checkpoint("A-created")), dependencies=[])["ref"]
        # B was initialized before A's creation; it can reference A legitimately without storing A again or restarting Host.
        combined = invoke(second, "artifact_put", kind="checkpoint", json_text=json.dumps(checkpoint("B-links", [created])), dependencies=[])
        assert second.artifacts.get(combined["ref"])["data"]["refs"] == [created]
        assert invoke(second, "artifact_get", ref=created, pointer="", offset=0, limit=1000)["ref"] == created
        newer = invoke(first, "artifact_put", kind="checkpoint", json_text=json.dumps(checkpoint("A-created-later")), dependencies=[])["ref"]
        p = profile("LIVE_OWNERSHIP")
        p["provenance"]["checkpoint_ref"] = newer
        draft = invoke(second, "draft_create", kind="profile", initial_json=json.dumps(p))
        checked = invoke(second, "draft_validate", draft_id=draft["draft_id"], tag_facts_json=json.dumps(facts(p)))
        assert checked["valid"], checked
        frozen = invoke(second, "draft_freeze", draft_id=draft["draft_id"])
        assert newer in second.artifacts.get(frozen["ref"])["dependencies"]
        assert not list(atlas.settings.glob("*/profile.json"))
        # Concurrent objects from other jobs remain unavailable for reading or saving references; diagnostics do not grant authorization.
        other = ws.create_job("profile_researcher", {"scope": "foreign job"})
        foreign = ws.artifacts.put("checkpoint", checkpoint("Foreign"), other)
        with pytest.raises(ProtocolError):
            invoke(second, "artifact_get", ref=foreign, pointer="", offset=0, limit=1000)
        with pytest.raises(ProtocolError):
            invoke(second, "artifact_put", kind="checkpoint", json_text=json.dumps(checkpoint("Bad", [foreign])), dependencies=[])
        bad = invoke(second, "draft_create", kind="checkpoint", initial_json=json.dumps(checkpoint("Bad-draft", [foreign])))
        rejected = invoke(second, "draft_validate", draft_id=bad["draft_id"], tag_facts_json="")
        assert not rejected["valid"] and foreign not in references(rejected)
        report = second._allowed(rejected["report_ref"])
        assert foreign not in references(report["data"])
        with ws.transaction() as db:
            db.execute("INSERT INTO tool_calls VALUES(?,?,?,?,?,?)", ("live-permission-report", first.job["id"], "draft_validate", "{}", dumps(rejected), "done"))
        restored = make_host(context, job_id=first.job["id"])
        with pytest.raises(ProtocolError):
            restored._allowed(foreign)
    finally:
        second_ws.close()


def test_result_version_errors_are_aggregated_before_freeze(context):
    _, ws, _ = context
    ref = source(ws)
    h = make_host(context, {"material_refs": [ref]})
    bad = result(ref, "arXiv2105.06595v2")
    bad["source_locators"].append({"source_ref": ref, "version": "another-paper-name", "locator": "fixture p.2"})
    draft = invoke(h, "draft_create", kind="result", initial_json=json.dumps(bad))
    checked = invoke(h, "draft_validate", draft_id=draft["draft_id"], tag_facts_json="")
    assert not checked["valid"]
    assert {e["path"] for e in checked["errors"]} == {"/source_locators/0/version", "/source_locators/1/version"}
    assert all(e["code"] == "source_version_mismatch" and e["expected_version"] == "f" * 64 for e in checked["errors"])
    for tool, args in [("artifact_put", {"kind": "result", "json_text": json.dumps(bad), "dependencies": []}),
                       ("draft_freeze", {"draft_id": draft["draft_id"]})]:
        with pytest.raises(ValidationDiagnostics) as error:
            invoke(h, tool, **args)
        assert len(error.value.diagnostics) == 2
    assert not ws.query("SELECT ref FROM artifacts WHERE kind='result'")
    assert not (ws.root / "transport").exists()
    good = result(ref)
    invoke(h, "draft_patch", draft_id=draft["draft_id"], revision=0,
        patches_json=json.dumps([{"op": "replace", "path": "", "value": good}]))
    assert invoke(h, "draft_validate", draft_id=draft["draft_id"], tag_facts_json="")["valid"]
    frozen = invoke(h, "draft_freeze", draft_id=draft["draft_id"])
    assert h.artifacts.get(frozen["ref"])["data"] == good


def test_result_reference_kind_and_missing_source_are_early_diagnostics(context):
    _, ws, _ = context
    wrong = ws.artifacts.put("checkpoint", checkpoint(), "seed")
    missing = "sha256:" + "0" * 64
    h = make_host(context, {"material_refs": [wrong, missing]})
    value = result(wrong)
    value["source_locators"].append({"source_ref": missing, "version": "missing", "locator": "fixture p.2"})
    value["proof_refs"] = [wrong]
    draft = invoke(h, "draft_create", kind="result", initial_json=json.dumps(value))
    checked = invoke(h, "draft_validate", draft_id=draft["draft_id"], tag_facts_json="")
    codes = {(e["code"], e["path"]) for e in checked["errors"]}
    assert ("artifact_reference_kind", "/source_refs/0") in codes
    assert ("artifact_reference_kind", "/proof_refs/0") in codes
    assert ("artifact_reference_kind", "/source_locators/0/source_ref") in codes
    assert ("artifact_reference_unavailable", "/source_locators/1/source_ref") in codes


def test_foreign_source_preflight_does_not_disclose_or_grant_it(context):
    _, ws, _ = context
    foreign = source(ws, producer=ws.create_job("profile_researcher", {"scope": "private source"}))
    h = make_host(context)
    draft = invoke(h, "draft_create", kind="result", initial_json=json.dumps(result(foreign)))
    rejected = invoke(h, "draft_validate", draft_id=draft["draft_id"], tag_facts_json="")
    assert not rejected["valid"] and foreign not in references(rejected)
    assert foreign not in references(h._allowed(rejected["report_ref"])["data"])
    assert foreign not in h.grants
    with pytest.raises(ProtocolError):
        h._allowed(foreign)


def test_version_diagnostic_cannot_mint_foreign_reference(context):
    _, ws, _ = context
    ref = source(ws)
    foreign = ws.artifacts.put("checkpoint", checkpoint("Private diagnostic fixture"),
        ws.create_job("profile_researcher", {"scope": "foreign diagnostic"}))
    h = make_host(context, {"material_refs": [ref]})
    # Even an exact hash of another job mistakenly placed in a version field must not become read authorization through diagnostics.
    draft = invoke(h, "draft_create", kind="result", initial_json=json.dumps(result(ref, foreign)))
    rejected = invoke(h, "draft_validate", draft_id=draft["draft_id"], tag_facts_json="")
    assert not rejected["valid"] and foreign not in references(rejected)
    mismatch = next(e for e in rejected["errors"] if e["code"] == "source_version_mismatch")
    assert mismatch["actual_version"].startswith("unavailable-artifact-reference:")
    report = h._allowed(rejected["report_ref"])
    assert foreign not in references(report["data"])
    with ws.transaction() as db:
        db.execute("INSERT INTO tool_calls VALUES(?,?,?,?,?,?)", ("version-diagnostic-restore", h.job["id"], "draft_validate", "{}", dumps(rejected), "done"))
    restored = make_host(context, job_id=h.job["id"])
    with pytest.raises(ProtocolError):
        restored._allowed(foreign)


def test_research_revalidates_legacy_result_versions_in_current_session(context):
    atlas, ws, _ = context
    fixture = profile("VERSION_FIXTURE")
    prepared = atlas.prepare(fixture, facts(fixture))
    atlas.commit(prepared, approve(prepared), "legacy-source-test")
    assessed = deepcopy(fixture["joint_analysis"])
    assessed["pending_obligations"] = []
    assessed["domain_map"].update(status="accounted", residual_domain="Empty beyond the declared synthetic domain",
                                  partition_argument="One cell contains every positive integer n.")
    coverage = assessed["synthesis_coverage"]
    coverage["status"] = "complete"
    coverage["literature"] = {"status": "finite_scope_complete", "scope": "Only the synthetic fixture source."}
    coverage["obligations"] = [row for row in coverage["obligations"] if row["kind"] != "material_lead"]
    for row in coverage["obligations"]:
        row.update(state="resolved", argument="Checked the fixture's sole available result.")

    ref = source(ws)
    legacy = ws.artifacts.put("result", result(ref, "arXiv2105.06595v2"), "seed")
    token = ws.artifacts.put("checkpoint", checkpoint("Research identifiers fixture"), "seed")
    h = make_host(context, {"candidate_ref": token, "identity_ref": token, "material_refs": [legacy, ref]})
    # no_change may also include result cards and must not bypass source-version preflight.
    research = {"candidate_ref": token, "identity_ref": token, "action": "no_change", "setting_id": "VERSION_FIXTURE",
        "base_version": prepared["version"], "joint_analysis": assessed, "profile_ref": None, "result_refs": [legacy], "proof_refs": [], "issues": [],
        "change_summary": "Software-only legacy version regression."}
    draft = invoke(h, "draft_create", kind="research", initial_json=json.dumps(research))
    checked = invoke(h, "draft_validate", draft_id=draft["draft_id"], tag_facts_json="")
    assert not checked["valid"]
    assert any(e["code"] == "source_version_mismatch" and e["path"] == "/result_refs/0/data/source_locators/0/version" for e in checked["errors"])
    with pytest.raises(ValidationDiagnostics):
        invoke(h, "draft_freeze", draft_id=draft["draft_id"])
    fixed = ws.artifacts.put("result", result(ref), h.job["id"])
    research["result_refs"] = [fixed]
    research["literature_scope"] = {"mode": "fixed_sources", "source_refs": [ref], "search_refs": [], "unresolved_leads": []}
    with pytest.raises(ValidationDiagnostics):
        invoke(h, "artifact_put", kind="research", json_text=json.dumps(research), dependencies=[])
    args = {"ref": ref, "offset": 0, "limit": 1000}
    delivered = h.call("source_read", args, "read-fixed-scope")
    with ws.transaction() as db:
        db.execute("INSERT INTO tool_calls VALUES(?,?,?,?,?,?)",
                   ("read-fixed-scope", h.job["id"], "source_read", dumps(args), dumps(delivered), "done"))
    saved = invoke(h, "artifact_put", kind="research", json_text=json.dumps(research), dependencies=[])
    assert h.artifacts.get(saved["ref"])["data"] == research


def test_read_batch_reads_authorized_pages_and_does_not_grant_foreign_refs(context):
    _, ws, _ = context
    ref = source(ws)
    other = ws.create_job("profile_researcher", {"scope": "private batch source"})
    foreign = source(ws, producer=other, version="e" * 64)
    h = make_host(context, {"material_refs": [ref]})
    own = invoke(h, "artifact_put", kind="checkpoint", json_text=json.dumps(checkpoint("Batch artifact")), dependencies=[])["ref"]
    requests = [
        {"tool": "source_read", "arguments": {"ref": ref, "offset": 0, "limit": 5000}},
        {"tool": "artifact_get", "arguments": {"ref": own, "pointer": "/summary", "offset": 0, "limit": 5000}},
        {"tool": "source_read", "arguments": {"ref": foreign, "offset": 0, "limit": 5000}},
    ]
    before = deepcopy(requests)
    out = invoke(h, "read_batch", requests=requests)
    assert requests == before
    assert out["count"] == 3
    assert out["items"][0]["result"]["text"] == "Software fixture only."
    assert out["items"][1]["result"]["text"] == "Batch artifact"
    assert out["items"][2]["error"]["error_type"] == "ProtocolError"
    assert "arguments" not in dumps(out) and foreign not in dumps(out)
    assert len(dumps(out)) <= h.cap
    with ws.transaction() as db:
        db.execute("INSERT INTO tool_calls VALUES(?,?,?,?,?,?)", ("batch-error-restore", h.job["id"], "read_batch", "{}", dumps(out), "done"))
    restored = make_host(context, job_id=h.job["id"])
    with pytest.raises(ProtocolError):
        restored._allowed(foreign)


@pytest.mark.parametrize("tool", ["artifact_put", "source_fetch", "bibliography_search", "read_batch"])
def test_read_batch_rejects_non_read_tools_before_any_work(context, tool):
    _, ws, _ = context
    h = make_host(context)
    before = ws.query("SELECT COUNT(*) n FROM artifacts")[0]["n"]
    with pytest.raises(ProtocolError):
        invoke(h, "read_batch", requests=[{"tool": tool, "arguments": {}}])
    assert ws.query("SELECT COUNT(*) n FROM artifacts")[0]["n"] == before


def test_read_batch_is_limited_to_eight_requests_and_respects_role_schema(context):
    atlas, ws, config = context
    ref = source(ws)
    h = make_host(context, {"material_refs": [ref]})
    request = {"tool": "source_read", "arguments": {"ref": ref, "offset": 0, "limit": 100000}}
    assert invoke(h, "read_batch", requests=[deepcopy(request) for _ in range(8)])["count"] == 8
    for requests in ([], [deepcopy(request) for _ in range(9)]):
        with pytest.raises(ProtocolError):
            invoke(h, "read_batch", requests=requests)
    # Validate every tool name and its arguments against that tool's published schema; source_read arguments cannot masquerade as artifact_get.
    out = invoke(h, "read_batch", requests=[{"tool": "artifact_get", "arguments": request["arguments"]}])
    assert "error" in out["items"][0]
    extractor_job = ws.create_job("extractor", {"material_refs": [ref]})
    extractor = ToolHost(ws, atlas, ws.job(extractor_job), config)
    with pytest.raises(ProtocolError):
        invoke(extractor, "read_batch", requests=[{"tool": "atlas_read", "arguments": {
            "setting_id": "UNAVAILABLE", "filename": "profile.json", "pointer": "", "offset": 0, "limit": 1000}}])
    assert not ws.query("SELECT ref FROM artifacts WHERE kind='native_record'")


def test_read_batch_archives_only_requested_pages_under_shared_cap(context):
    atlas, ws, config = context
    ref = ws.artifacts.put("source", {"url": "https://example.org/" + "x" * 5000, "version": "baseline",
        "content_hash": "a" * 64, "text": "A" * 50000, "metadata": {}}, "seed")
    h = make_host((atlas, ws, {**config, "budgets": {**config["budgets"], "max_tool_chars": 2048}}), {"material_refs": [ref]})
    out = invoke(h, "read_batch", requests=[{"tool": "source_read", "arguments": {"ref": ref, "offset": 10, "limit": 50000}} for _ in range(2)])
    assert "archived_result_ref" in out and len(dumps(out)) <= h.cap
    archived = h._allowed(out["archived_result_ref"])["data"]["result"]
    assert archived["count"] == 2
    for item in archived["items"]:
        page = item["result"]
        assert page["offset"] == 10 and page["total_chars"] == 50000
        assert len(page["text"]) <= archived["per_item_limit"] < 50000
        assert page["next_offset"] == 10 + len(page["text"])
    assert not list(atlas.settings.glob("*/profile.json"))


def test_native_mcp_live_ownership_and_source_version_preflight(context, tmp_path):
    pytest.importorskip("mcp")
    from oracle_atlas.providers.mcp import MCPBridge
    atlas, ws, _ = context
    ref = source(ws)
    jid = ws.create_job("profile_researcher", {"material_refs": [ref]})
    path = tmp_path / "config.toml"
    path.write_text(f'workspace = {json.dumps(str(ws.root))}\natlas = {json.dumps(str(atlas.root))}\n')
    project = Path(__file__).resolve().parents[1]
    servers = [{"name": name, "transport": "stdio", "command": sys.executable,
        "args": ["-m", "oracle_atlas", "mcp", "--config", str(path), "--job", jid],
        "env": {"PYTHONPATH": str(project / "src")}, "timeout": 15,
        "allowed_tools": ["artifact_put", "draft_create", "draft_validate", "draft_freeze", "read_batch"]} for name in ("a", "b")]
    with MCPBridge(servers) as bridge:
        bridge.tools()  # Initialize both MCP Hosts before A registers a new artifact.
        def run(server, tool, **args):
            out = bridge.call(f"mcp__{server}__{tool}", args)
            return json.loads(next(item["text"] for item in out["content"] if item["type"] == "text"))
        created = run("a", "artifact_put", kind="checkpoint", json_text=json.dumps(checkpoint("Native A")), dependencies=[])["ref"]
        linked = run("b", "artifact_put", kind="checkpoint", json_text=json.dumps(checkpoint("Native B", [created])), dependencies=[])
        assert linked["ref"].startswith("sha256:")
        draft = run("b", "draft_create", kind="result", initial_json=json.dumps(result(ref, "paper-version-name")))
        rejected = run("b", "draft_freeze", draft_id=draft["draft_id"])
        assert rejected["error_type"] == "ValidationDiagnostics"
        assert rejected["diagnostics"][0]["path"] == "/source_locators/0/version"
        assert rejected["diagnostics"][0]["code"] == "source_version_mismatch"
        good = run("b", "artifact_put", kind="result", json_text=json.dumps(result(ref)), dependencies=[])
        assert ws.artifacts.get(good["ref"])["data"]["source_locators"][0]["version"] == "f" * 64
        before = ws.query("SELECT COUNT(*) n FROM tool_calls")[0]["n"]
        batch = run("b", "read_batch", requests=[
            {"tool": "source_read", "arguments": {"ref": ref, "offset": 0, "limit": 1000}},
            {"tool": "artifact_get", "arguments": {"ref": good["ref"], "pointer": "/result_id", "offset": 0, "limit": 1000}},
        ])
        assert batch["items"][0]["result"]["text"] == "Software fixture only."
        assert batch["items"][1]["result"]["text"] == "version-fixture"
        assert ws.query("SELECT COUNT(*) n FROM tool_calls")[0]["n"] == before + 1
    assert not list(atlas.settings.glob("*/profile.json"))
