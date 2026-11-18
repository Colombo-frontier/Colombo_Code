"""Fixed-profile cloning, incremental auditing, and authorization negative controls; all use software fixtures without model scientific approval."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys

import pytest

from oracle_atlas.atlas.store import Atlas
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ProtocolError, references
from oracle_atlas.core.store import Workspace, digest, dumps
from oracle_atlas.tools.host import ToolHost
from test_atlas import approve, facts, profile


@pytest.fixture
def context(tmp_path):
    root = tmp_path / "atlas"
    shutil.copytree(Path(__file__).parent / "fixtures/native_atlas/data/schemas", root / "data/schemas")
    atlas = Atlas(root)
    ws = Workspace(tmp_path / "work")
    config = {"atlas": str(root), "workspace": str(ws.root), "budgets": dict(DEFAULTS), "model": {}}
    yield atlas, ws, config
    ws.close()


def host(context, inputs, role="profile_researcher", job_id=None):
    atlas, ws, config = context
    jid = job_id or ws.create_job(role, inputs)
    return ToolHost(ws, atlas, ws.job(jid), config)


def clone(h, ref, value, pointer="", call_id="clone-fixed"):
    return h.call("draft_clone", {"source_ref": ref, "source_pointer": pointer,
                                  "expected_digest": digest(value)}, call_id)


def seed_native(context, sid="CLONE_NATIVE"):
    atlas, ws, _ = context
    raw = profile(sid)
    prepared = atlas.prepare(raw, facts(raw))
    atlas.commit(prepared, approve(prepared), "software-fixture-seed")
    current, version = atlas.read(sid), atlas.version(sid)
    record = {"setting_id": sid, "version": version, "content": current}
    ref = ws.artifacts.put("native_record", record, "controller-software-fixture")
    h = host(context, {"base_profile_ref": ref, "setting_id": sid, "base_version": version}, "bound_updater")
    return h, ref, current, record


def test_clone_delta_retains_source_and_freezes_current_profile(context):
    _, ws, _ = context
    value = profile("CLONE_DELTA")
    value["tag_facts"] = facts(value)
    ref = ws.artifacts.put("profile", value, "seed")
    h = host(context, {"material_refs": [ref], "setting_id": value["setting_id"]})
    result = clone(h, ref, value)
    assert result["kind"] == "profile" and result["revision"] == 0
    assert result["copied_chars"] == len(dumps(value))
    assert result["copied_bytes"] == len(dumps(value).encode("utf-8"))
    assert "data" not in result and len(dumps(result)) < 1000
    assert ws.draft(result["draft_id"], h.job["id"])["data"] == value
    patch = [{"op": "test", "path": "/setting_id", "value": "CLONE_DELTA"},
             {"op": "replace", "path": "/title", "value": "Incremental software fixture"}]
    updated = h.call("draft_patch", {"draft_id": result["draft_id"], "revision": 0,
                                     "patches_json": dumps(patch)}, "small-delta")
    assert updated["revision"] == 1
    checked = h.call("draft_validate", {"draft_id": result["draft_id"], "tag_facts_json": dumps(facts(value))}, "preflight")
    assert checked["valid"], checked
    frozen = h.call("draft_freeze", {"draft_id": result["draft_id"]}, "freeze")
    changed = ws.artifacts.get(frozen["ref"])["data"]
    assert changed["title"] == "Incremental software fixture"
    assert changed["bounds"] == value["bounds"] and changed["views"] == value["views"]
    assert ws.artifacts.get(ref)["data"] == value
    audit = ws.query("SELECT * FROM draft_deltas WHERE draft_id=?", (result["draft_id"],))
    assert len(audit) == 1 and json.loads(audit[0]["patches"]) == patch
    assert audit[0]["before_digest"] == digest(value)
    patched = deepcopy(value); patched["title"] = "Incremental software fixture"
    assert audit[0]["after_digest"] == digest(patched)
    assert ws.query("SELECT payload FROM events WHERE event='draft_clone_frozen'")
    assert not list(h.atlas.settings.glob("*/profile.json"))


def test_clone_fixed_native_profile_and_record_origin_without_atlas_write(context):
    h, ref, current, record = seed_native(context)
    result = clone(h, ref, current, "/content")
    assert result["clone_source"] == {"source_ref": ref, "source_pointer": "/content",
        "source_kind": "native_record", "source_digest": digest(current), "source_version": record["version"]}
    h.call("draft_patch", {"draft_id": result["draft_id"], "revision": 0,
        "patches_json": dumps([{"op": "replace", "path": "/title", "value": "Changed draft only"}])}, "native-delta")
    assert h.atlas.read(current["setting_id"]) == current
    assert h.atlas.version(current["setting_id"]) == record["version"]
    assert h.ws.draft(result["draft_id"], h.job["id"])["data"]["title"] == "Changed draft only"


def test_clone_receipt_is_once_and_survives_patch_restart_and_atlas_change(context):
    h, ref, current, _ = seed_native(context)
    first = clone(h, ref, current, "/content")
    h.call("draft_patch", {"draft_id": first["draft_id"], "revision": 0,
        "patches_json": dumps([{"op": "replace", "path": "/title", "value": "Persisted delta"}])}, "persisted-patch")
    replacement = deepcopy(current); replacement["title"] = "Concurrent Atlas update"
    prepared = h.atlas.prepare(replacement, facts(replacement), h.atlas.version(current["setting_id"]))
    h.atlas.commit(prepared, approve(prepared), "concurrent-software-fixture")
    ws2 = Workspace(h.ws.root)
    try:
        second = ToolHost(ws2, h.atlas, ws2.job(h.job["id"]), h.config)
        assert clone(second, ref, current, "/content") == first
        assert ws2.draft(first["draft_id"], h.job["id"])["revision"] == 1
        assert len(ws2.query("SELECT * FROM drafts")) == 1
        assert len(ws2.query("SELECT * FROM draft_origins")) == 1
        assert len(ws2.query("SELECT * FROM draft_deltas")) == 1
        assert len(ws2.query("SELECT * FROM events WHERE event='draft_cloned'")) == 1
        stale = second.call("draft_validate", {"draft_id": first["draft_id"],
            "tag_facts_json": dumps(facts(current))}, "stale-current-preflight")
        assert not stale["valid"] and any(e["code"] == "atlas_conflict" for e in stale["errors"])
        with pytest.raises(ProtocolError, match="stale"):
            clone(second, ref, current, "/content", "new-operation-on-stale-base")
    finally:
        ws2.close()


def test_clone_call_id_cannot_change_source(context):
    _, ws, _ = context
    one = profile("SAME_TARGET"); two = deepcopy(one); two["title"] = "Other fixed source"
    r1, r2 = (ws.artifacts.put("profile", x, "seed") for x in [one, two])
    h = host(context, {"material_refs": [r1, r2]})
    clone(h, r1, one)
    with pytest.raises(ProtocolError, match="call_id was reused"):
        clone(h, r2, two)
    assert len(ws.query("SELECT * FROM drafts")) == 1


def test_clone_authority_restores_across_live_hosts_but_not_from_patch(context):
    atlas, ws, config = context
    support = ws.artifacts.put("checkpoint", {"summary": "Authorized software support", "refs": [], "remaining": []}, "other-producer")
    value = profile("RESTORED_CLONE"); value["tag_facts"] = facts(value)
    value["provenance"]["formal_refs"] = [support]
    ref = ws.artifacts.put("profile", value, "seed")
    first = host(context, {"material_refs": [ref]})
    ws2 = Workspace(ws.root)
    try:
        second = ToolHost(ws2, atlas, ws2.job(first.job["id"]), config)
        assert support not in second.grants
        draft = clone(first, ref, value)
        # Restore clone sources through formal authorization without putting support again or reading the entire profile.
        frozen = second.call("draft_freeze", {"draft_id": draft["draft_id"]}, "second-host-freeze")
        assert support in references(ws.artifacts.get(frozen["ref"])["data"])
        foreign = ws.artifacts.put("checkpoint", {"summary": "Private other job", "refs": [], "remaining": []},
                                   ws.create_job("profile_researcher", {"scope": "private"}))
        second.call("draft_patch", {"draft_id": draft["draft_id"], "revision": 0,
            "patches_json": dumps([{"op": "add", "path": "/provenance/foreign", "value": foreign}])}, "foreign-patch")
        denied = second.call("draft_validate", {"draft_id": draft["draft_id"], "tag_facts_json": ""}, "foreign-preflight")
        assert not denied["valid"] and foreign not in references(denied)
        with pytest.raises(ProtocolError, match="[Uu]nauthorized"):
            second.call("draft_freeze", {"draft_id": draft["draft_id"]}, "foreign-freeze")
        assert foreign not in second.grants
    finally:
        ws2.close()


@pytest.mark.parametrize("kind,pointer", [("checkpoint", ""), ("proof", ""), ("profile", "/views/0")])
def test_clone_refuses_cast_or_subtree(context, kind, pointer):
    _, ws, _ = context
    value = profile("NO_CAST")
    if kind == "checkpoint":
        value = {"summary": "Not a profile", "refs": [], "remaining": []}
    elif kind == "proof":
        value = {"proof_id": "software-proof", "origin": "analyst_derivation",
            "proposition": "Software schema fixture only.", "premises": [],
            "argument": "No scientific claim.", "boundary_cases": "None.",
            "quantifiers": "None.", "resource_accounting": "None.", "dependencies": [], "issues": []}
    ref = ws.artifacts.put(kind, value, "seed")
    h = host(context, {"material_refs": [ref]})
    with pytest.raises(ProtocolError):
        clone(h, ref, value.get("content", value), pointer)
    assert not ws.query("SELECT * FROM drafts")


@pytest.mark.parametrize("digest_value", ["", "guess", "a" * 63, "sha256:" + "a" * 64, "0" * 64])
def test_clone_rejects_unfixed_or_wrong_payload_digest(context, digest_value):
    _, ws, _ = context
    value = profile("DIGEST_BOUND"); ref = ws.artifacts.put("profile", value, "seed")
    h = host(context, {"material_refs": [ref]})
    with pytest.raises(ProtocolError, match="digest|hex"):
        h.call("draft_clone", {"source_ref": ref, "source_pointer": "", "expected_digest": digest_value}, "bad-digest")
    assert not ws.query("SELECT * FROM drafts")


@pytest.mark.parametrize("change", ["version", "content", "filename", "record_setting", "job_setting", "job_version", "pointer"])
def test_native_clone_rejects_forged_baseline_bindings(context, change):
    h, ref, current, record = seed_native(context)
    altered = deepcopy(record); inputs = deepcopy(h.job["inputs"]); pointer = "/content"
    if change == "version": altered["version"] = "target-pretend"
    if change == "content": altered["content"]["title"] = "Forged content with real version"
    if change == "filename": altered["filename"] = "identity.json"
    if change == "record_setting": altered["setting_id"] = "OTHER"
    if change == "job_setting": inputs["setting_id"] = "OTHER"
    if change == "job_version": inputs["base_version"] = None
    if change == "pointer": pointer = ""
    ref = h.ws.artifacts.put("native_record", altered, "seed")
    inputs["base_profile_ref"] = ref
    other = host(context, inputs)
    with pytest.raises(ProtocolError):
        clone(other, ref, altered["content"], pointer)
    assert not h.ws.query("SELECT * FROM drafts")


def test_clone_foreign_source_and_draft_are_never_granted(context):
    _, ws, _ = context
    value = profile("PRIVATE_CLONE")
    ref = ws.artifacts.put("profile", value, "private-producer")
    allowed = host(context, {"material_refs": [ref]})
    draft = clone(allowed, ref, value)
    denied = host(context, {"scope": "foreign"})
    with pytest.raises(ProtocolError, match="[Uu]nauthorized"):
        clone(denied, ref, value)
    for name, args in [("draft_read", {"draft_id": draft["draft_id"], "pointer": "", "offset": 0, "limit": 10}),
                       ("draft_patch", {"draft_id": draft["draft_id"], "revision": 0, "patches_json": "[]"}),
                       ("draft_freeze", {"draft_id": draft["draft_id"]})]:
        with pytest.raises(ProtocolError, match="not authorized"):
            denied.call(name, args, "denied-" + name)
    assert len(ws.query("SELECT * FROM drafts")) == 1


def test_clone_rejects_wrong_target_corrupt_cas_and_oversized_source(context):
    _, ws, _ = context
    value = profile("ACTUAL_ID"); ref = ws.artifacts.put("profile", value, "seed")
    h = host(context, {"material_refs": [ref], "setting_id": "OTHER_ID"})
    with pytest.raises(ProtocolError, match="setting_id"):
        clone(h, ref, value)
    right = host(context, {"material_refs": [ref]})
    path = ws.artifacts.root / ref[7:9] / (ref[7:] + ".json")
    obj = json.loads(path.read_text()); obj["data"]["title"] = "Corrupted CAS bytes"
    path.write_text(dumps(obj))
    with pytest.raises(ProtocolError, match="hash"):
        clone(right, ref, value)
    large = profile("LARGE_SOURCE"); large["reader_markdown"] = "x" * 4_000_001
    large_ref = ws.artifacts.put("profile", large, "seed")
    h = host(context, {"material_refs": [large_ref]})
    with pytest.raises(ProtocolError, match="4 MB"):
        clone(h, large_ref, large)
    assert not ws.query("SELECT * FROM drafts")


def test_public_clone_contract_and_small_page_digest(context):
    _, ws, _ = context
    value = profile("PUBLIC_CLONE"); ref = ws.artifacts.put("profile", value, "seed")
    h = host(context, {"material_refs": [ref]})
    definition = next(t for t in h.definitions() if t["name"] == "draft_clone")
    assert set(definition["parameters"]["required"]) == {"source_ref", "source_pointer", "expected_digest"}
    page = h.call("artifact_get", {"ref": ref, "pointer": "", "offset": 0, "limit": 1}, "digest-only-page")
    assert page["value_digest"] == digest(value) and len(page["text"]) == 1
    for role in ["extractor", "matcher", "profile_reviewer", "coordinator"]:
        other = host(context, {"material_refs": [ref]}, role)
        assert "draft_clone" not in {d["name"] for d in other.definitions()}
        with pytest.raises(ProtocolError, match="does not have tool"):
            clone(other, ref, value)


def test_actual_stdio_mcp_clone_delta_cross_host_and_full_preflight(context, tmp_path):
    pytest.importorskip("mcp")
    from oracle_atlas.providers.mcp import MCPBridge
    atlas, ws, _ = context
    value = profile("MCP_CLONE"); value["tag_facts"] = facts(value)
    ref = ws.artifacts.put("profile", value, "seed")
    h = host(context, {"material_refs": [ref]})
    config = tmp_path / "config.toml"
    config.write_text(f'workspace = {json.dumps(str(ws.root))}\natlas = {json.dumps(str(atlas.root))}\n')
    project = Path(__file__).resolve().parents[1]
    tools = ["draft_clone", "draft_read", "draft_patch", "draft_validate", "draft_freeze", "artifact_get"]
    servers = [{"name": name, "transport": "stdio", "command": sys.executable,
        "args": ["-m", "oracle_atlas", "mcp", "--config", str(config), "--job", h.job["id"]],
        "env": {"PYTHONPATH": str(project / "src")}, "timeout": 15, "allowed_tools": tools} for name in ["a", "b"]]
    with MCPBridge(servers) as bridge:
        bridge.tools()
        def run(server, name, args):
            out = bridge.call(f"mcp__{server}__{name}", args)
            assert not out.get("isError"), out
            value = json.loads(next(c["text"] for c in out["content"] if c["type"] == "text"))
            assert "error_type" not in value, value
            return value
        page = run("a", "artifact_get", {"ref": ref, "pointer": "", "offset": 0, "limit": 1})
        draft = run("a", "draft_clone", {"source_ref": ref, "source_pointer": "", "expected_digest": page["value_digest"]})
        run("b", "draft_patch", {"draft_id": draft["draft_id"], "revision": 0,
            "patches_json": dumps([{"op": "replace", "path": "/title", "value": "Actual MCP cloned delta"}])})
        check = run("b", "draft_validate", {"draft_id": draft["draft_id"], "tag_facts_json": dumps(facts(value))})
        assert check["valid"], check
        frozen = run("b", "draft_freeze", {"draft_id": draft["draft_id"]})
        assert ws.artifacts.get(frozen["ref"])["data"]["title"] == "Actual MCP cloned delta"
    assert len(ws.query("SELECT * FROM drafts")) == 1
    assert len(ws.query("SELECT * FROM draft_deltas")) == 1
    assert not list(atlas.settings.glob("*/profile.json"))
