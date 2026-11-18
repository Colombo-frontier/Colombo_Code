"""Actual science instruction bodies/hashes and bounded startup, without models."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil

import pytest

from oracle_atlas.core.config import DEFAULTS, resources_root
from oracle_atlas.core.contracts import MAIN_KINDS, ProtocolError, schema
from oracle_atlas.core.store import Workspace, digest, dumps
from oracle_atlas.runtime.instructions import (
    JOINT_SCHEMA, SCIENCE_RESOURCES, SCIENCE_ROLES, load_instructions,
    verify_instruction_manifest,
)
from oracle_atlas.runtime.runner import AgentRunner
from oracle_atlas.tools.host import ToolHost


@pytest.fixture
def resource_tree(tmp_path, monkeypatch):
    source = resources_root()
    target = tmp_path / "resources"
    target.mkdir()
    for name in ("agents", "skills", "standards", "schemas"):
        shutil.copytree(source / name, target / name)
    shutil.copy2(source / "protocol.md", target / "protocol.md")
    monkeypatch.setenv("ORACLE_ATLAS_RESOURCES", str(target))
    return target


@pytest.mark.parametrize("role", sorted(SCIENCE_ROLES))
def test_science_roles_receive_complete_identical_versioned_bodies(role):
    text, manifest = load_instructions(role)
    root = resources_root()
    records = {item["path"]: item for item in manifest["loaded"]}
    for relative in SCIENCE_RESOURCES:
        raw = (root / relative).read_bytes()
        assert f"\n## {relative}\n{raw.decode()}" in text
        actual = hashlib.sha256(raw).hexdigest()
        assert records[relative]["sha256"] == actual
        assert manifest["dependency_hashes"][relative] == actual
    taxonomy = json.loads((root / "standards/status_taxonomy.json").read_text())
    assert manifest["science_contract"]["taxonomy_version"] == taxonomy["version"]
    assert manifest["science_contract"]["joint_analysis_version"] == 2
    verify_instruction_manifest(text, manifest)


def test_producer_and_reviewer_science_fingerprints_are_the_same():
    contracts = [load_instructions(role)[1]["science_contract"] for role in sorted(SCIENCE_ROLES)]
    assert contracts[0] == contracts[1] == contracts[2]


def test_complete_joint_schema_is_hash_bound_but_not_pasted_into_startup():
    raw = (resources_root() / JOINT_SCHEMA).read_bytes()
    for role in SCIENCE_ROLES:
        text, manifest = load_instructions(role)
        item = manifest["science_contract"]["joint_schema"]
        assert item == {"path": JOINT_SCHEMA, "sha256": hashlib.sha256(raw).hexdigest(),
                        "read_with": "schema_read(joint_analysis)", "body_loaded": False}
        assert manifest["dependency_hashes"][JOINT_SCHEMA] == item["sha256"]
        assert raw.decode() not in text
        assert "schema_read(joint_analysis)" in text


@pytest.mark.parametrize("relative", [*SCIENCE_RESOURCES, JOINT_SCHEMA])
def test_missing_mandatory_resource_fails_instead_of_loading_a_short_catalog(resource_tree, relative):
    (resource_tree / relative).unlink()
    with pytest.raises(ProtocolError, match="Required instruction resource"):
        load_instructions("profile_reviewer")


@pytest.mark.parametrize("fault", ["missing_loaded", "wrong_loaded_hash", "missing_dependency_hash",
                                  "wrong_schema_hash", "wrong_text_hash", "wrong_contract_hash"])
def test_missing_or_tampered_manifest_hashes_fail(fault):
    text, original = load_instructions("profile_reviewer")
    manifest = deepcopy(original)
    if fault == "missing_loaded":
        manifest["loaded"].pop()
    elif fault == "wrong_loaded_hash":
        manifest["loaded"][-1]["sha256"] = "0" * 64
    elif fault == "missing_dependency_hash":
        del manifest["dependency_hashes"][SCIENCE_RESOURCES[-1]]
    elif fault == "wrong_schema_hash":
        manifest["science_contract"]["joint_schema"]["sha256"] = "0" * 64
    elif fault == "wrong_text_hash":
        text += "\nchanged"
    else:
        manifest["contract_version"] = "0" * 64
    with pytest.raises(ProtocolError):
        verify_instruction_manifest(text, manifest)


def test_required_body_cannot_be_omitted_even_if_text_hash_is_recomputed():
    text, manifest = load_instructions("profile_reviewer")
    body = (resources_root() / SCIENCE_RESOURCES[-1]).read_text()
    text = text.replace(body, "[short catalog only]", 1)
    manifest["instructions_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    manifest["chars"] = len(text)
    with pytest.raises(ProtocolError, match="body is missing or truncated"):
        verify_instruction_manifest(text, manifest)


def test_resource_change_invalidates_the_old_manifest_and_job_recovery(resource_tree, tmp_path):
    text, manifest = load_instructions("profile_reviewer")
    ws = Workspace(tmp_path / "work")
    try:
        jid = ws.create_job("profile_reviewer", {"budget_scope": "instruction-fixture"})
        ws.save_job(jid, "pending", {"manifest_hash": digest(manifest)})
        path = resource_tree / SCIENCE_RESOURCES[-1]
        path.write_text(path.read_text() + "\nNew contract revision.\n")
        with pytest.raises(ProtocolError, match="resource hash mismatch"):
            verify_instruction_manifest(text, manifest)
        new_text, changed = load_instructions("profile_reviewer")
        assert changed["contract_version"] != manifest["contract_version"]
        assert changed["instructions_sha256"] != manifest["instructions_sha256"]
        assert "New contract revision." in new_text
        runner = AgentRunner(ws, object(), object(), {"budgets": dict(DEFAULTS)})
        with pytest.raises(ProtocolError, match="Instructions changed during execution"):
            runner.run(jid)
        assert not ws.query("SELECT id FROM calls WHERE job=?", (jid,))
    finally:
        ws.close()


def test_full_v2_scientific_obligations_and_exact_review_context_are_loaded():
    text, _ = load_instructions("profile_reviewer")
    for term in ("joint_variables", "normalized_variables", "fixed_parameters", "uniform_in",
                 "allowed_constant_dependencies", "validity_region", "adopted_region",
                 "replacement_branch", "resource_projection", "closed_region_publication",
                 "material_lead", "outside_old_witness", "explicit_region_registration",
                 "closure_proof_refs", "research_scope", "registered_envelope",
                 "finite_scope_complete", "science_context_hash", "science_prepared_ref",
                 "parameter_roles", "guarded_envelopes", "domain_accounting",
                 "improvement_regions", "provenance", "display_consistency"):
        assert term in text
    assert "No third model role" in text
    assert "without v2" in text.lower()
    assert "/science/research_context/observations/activity" in text
    assert "tool_trace_hash" in text


def _host(role):
    # Actual definitions and schema_read path, without a live Atlas or model.
    host = ToolHost.__new__(ToolHost)
    host.role = role
    host.bridge = None
    host.cap = DEFAULTS["max_tool_chars"]
    host.config = {"budgets": dict(DEFAULTS)}
    host.call_id = ""
    # Local schema reading uses no artifact grants or workspace state.
    host._refresh_owned = lambda: None
    return host


@pytest.mark.parametrize("role", sorted(SCIENCE_ROLES))
def test_actual_fixed_input_and_a_joint_schema_page_fit_original_60000_budget(role):
    text, _ = load_instructions(role)
    host = _host(role)
    initial = {"role": "user", "content": dumps({"job_id": "science-budget-fixture", "inputs": {
        "candidate_ref": "sha256:" + "a" * 64, "identity_ref": "sha256:" + "b" * 64,
        "identity_review_ref": "sha256:" + "c" * 64, "coverage_scope_ref": "sha256:" + "d" * 64,
        "proof_context_ref": "sha256:" + "e" * 64, "review_context_ref": "sha256:" + "f" * 64,
        "subject_ref": "sha256:" + "1" * 64, "science_prepared_ref": "sha256:" + "2" * 64,
        "research_scope": {"queries_complete": True, "unresolved_leads": [], "scope": "Finite fixture"}}})}
    fixed = len(text) + len(dumps(host.definitions())) + len(dumps(schema("handoff")))
    result = host.call("schema_read", {"kind": "joint_analysis"}, "read-joint-schema")
    history = [initial, {"type": "function_call", "call_id": "read-joint-schema",
                        "name": "schema_read", "arguments": dumps({"kind": "joint_analysis"})},
               {"type": "function_call_output", "call_id": "read-joint-schema", "output": dumps(result)}]
    assert DEFAULTS["max_input_chars"] == 60000
    assert fixed + len(dumps(history)) <= 60000, (role, fixed, len(dumps(history)))


def test_existing_roles_only_and_frontend_scope_stays_separate():
    assert SCIENCE_ROLES == {"profile_researcher", "bound_updater", "profile_reviewer"}
    assert set(MAIN_KINDS) == {"coordinator", "task_scout", "paper_scanner", "extractor",
        "extraction_reviewer", "matcher", "identity_reviewer", "profile_researcher",
        "bound_updater", "profile_reviewer", "expansion_planner", "setting_expander", "expansion_reviewer"}
    for role in ("setting_expander", "expansion_reviewer"):
        text, manifest = load_instructions(role)
        assert "science_contract" not in manifest
        assert not set(SCIENCE_RESOURCES) & {row["path"] for row in manifest["loaded"]}
        assert "## Parameter scope and later closure obligations" in text
        assert "diagnostic slice" in text
