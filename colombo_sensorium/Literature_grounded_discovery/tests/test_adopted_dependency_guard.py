"""Adoption cannot decline direct-defect checks by declining reuse credentials.

All mathematical content is a synthetic software fixture. No model is called.
"""
from copy import deepcopy

import pytest

from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ProtocolError, schema
from oracle_atlas.core.store import dumps
from oracle_atlas.workflow.coverage import coverage_scope
from oracle_atlas.workflow.engine import Engine
from oracle_atlas.workflow.proof_reuse import adopted_proof_requirements, build_proof_review_context, proof_approval_errors
from oracle_atlas.workflow.review_context import _snapshot, build_review_context
from test_coverage_contract import ledger
from test_draft_clone import host
from test_historical_issue_scopes import historical, errors
from test_proof_reuse import proof_context
from test_review_context import context


def defective(c, kind, *, through_proof=True):
    a = c["ws"].artifacts
    issue = c["issue"]("direct-unrepaired-defect", subjects=["proof:fixture"], blocks=["bound"])
    p = deepcopy(c["profile"])
    if kind == "proof":
        pref = c["proof"](issues=[issue], dependencies=[c["source"], c["transfer"]])
    else:
        result = deepcopy(a.get(p["bounds"][0]["result_ref"])["data"])
        if kind == "source":
            source = deepcopy(a.get(c["source"])["data"])
            source["metadata"]["issues"] = [issue]
            sref = a.put("source", source, c["producer"])
            result["source_refs"] = [sref]
            result["source_locators"] = [{"source_ref": sref, "version": "fixed-baseline", "locator": "fixture"}]
        else:
            result["issues"] = [issue]
        rref = a.put("result", result, c["producer"])
        pref = c["proof"](dependencies=[rref, c["transfer"]])
        if not through_proof:
            p["bounds"][0]["result_ref"] = rref
            p["evidence"][0]["result_ref"] = rref
    if through_proof:
        p["proofs"][0]["proof_ref"] = pref
    else:
        p["bounds"][0].pop("proof_refs", None)
        p["proofs"] = []
    subject = c["proposal"](p)
    data, _ = c["certificate"](subject)
    data.update(bound_approvals=[], proof_approvals=[], proof_issue_scopes=[], bound_issue_scopes=[],
                proof_execution_checks=[{"proof_ref": pref, "execution_check": {
                    "required": False, "reason": "Synthetic fixture; no mathematical execution claim.", "check_refs": []}}] if through_proof else [])
    return data


@pytest.mark.parametrize("kind", ["proof", "result", "source"])
@pytest.mark.parametrize("credential_fields", ["empty", "omitted"])
def test_direct_defect_is_checked_without_optional_credentials(historical, kind, credential_fields):
    data = defective(historical, kind)
    if credential_fields == "omitted":
        for key in ("bound_approvals", "proof_approvals", "bound_issue_scopes", "proof_issue_scopes"):
            data.pop(key)
    found = errors(historical, data, issue_scope_contract_version="occurrence-bound-scope")
    assert any("adopted_dependency_has_blocking_issue: " + kind + ":" in row["message"] for row in found)


@pytest.mark.parametrize("kind", ["result", "source"])
def test_published_support_needs_guard_even_without_formal_proofs(historical, kind):
    c = historical
    data = defective(c, kind, through_proof=False)
    assert not adopted_proof_requirements(c["ws"].artifacts, _snapshot(c["ws"].artifacts, data["subject_ref"]), ["u"])
    assert any("adopted_dependency_has_blocking_issue" in row["message"]
               for row in errors(c, data, issue_scope_contract_version="occurrence-bound-scope"))


def test_nonadopted_and_provenance_defects_do_not_expand_adoption_gate(historical):
    c = historical
    data = defective(c, "proof")
    data.update(approved_bound_ids=[], proof_execution_checks=[])
    assert errors(c, data, issue_scope_contract_version="occurrence-bound-scope") == []
    # This context has genuine synthetic P7/P8 historical blockers; the narrow
    # scientific chain must not reinterpret those workflow records as direct defects.
    data, _ = c["certificate"]()
    assert errors(c, data, issue_scope_contract_version="occurrence-bound-scope") == []


def test_unreferenced_formal_defect_does_not_block_other_active_bound(historical):
    c = historical
    issue = c["issue"]("unadopted-defect", subjects=["proof:unadopted"], blocks=["bound"])
    unused = c["proof"]("proof:unadopted", issues=[issue])
    p = deepcopy(c["profile"])
    p["proofs"].append({"id": "proof:unadopted", "proof_ref": unused})
    subject = c["proposal"](p)
    data, _ = c["certificate"](subject)
    assert data["approved_bound_ids"] == ["u"]
    assert errors(c, data, issue_scope_contract_version="occurrence-bound-scope") == []


@pytest.mark.parametrize("kind", ["proof", "result", "source"])
def test_production_host_and_engine_reject_adoption_with_empty_credentials(historical, kind):
    c = historical; a = c["ws"].artifacts
    data = defective(c, kind); subject = data["subject_ref"]
    prop = a.get(subject)["data"]; prepared = a.get(prop["prepared_ref"])["data"]
    inputs = {"subject_ref": subject, "issue_scope_contract_version": "occurrence-bound-scope",
              "proof_context_ref": a.put("external_result", build_proof_review_context(a, c["ws"], subject), "controller"),
              "review_context_ref": a.put("external_result", build_review_context(a, c["ws"], subject), "controller"),
              "coverage_scope_ref": a.put("external_result", coverage_scope(prop["candidate_ref"]), "controller")}
    data.update(verdict="approve", prepared_hash=prepared["bundle_hash"],
                joint_checks={k: True for k in schema("review")["properties"]["joint_checks"]["required"]},
                coverage_audit={"scope": "Software gate fixture only", "checks": ledger()["checks"],
                    "resolved_issue_ids": [], "carried_issue_ids": [], "new_blocker_justifications": [],
                    "followups": [], "reuse_context_ref": None, "reused_bound_ids": []})
    config = {"atlas": str(c["atlas"].root), "workspace": str(c["ws"].root), "budgets": dict(DEFAULTS), "model": {}}
    h = host((c["atlas"], c["ws"], config), inputs, "profile_reviewer")
    h.call("artifact_get", {"ref": subject, "pointer": "", "offset": 0, "limit": 24000}, "read-proposal")
    offset = 0
    while True:
        args = {"ref": prop["profile_ref"], "pointer": "/joint_analysis", "offset": offset, "limit": 24000}
        call_id = "read-analysis-" + str(offset)
        result = h.call("artifact_get", args, call_id)
        # Actual executed pages are persisted as in the production runner.
        with c["ws"].transaction() as db:
            db.execute("INSERT INTO tool_calls VALUES(?,?,?,?,?,?)", (call_id, h.job["id"], "artifact_get", dumps(args), dumps(result), "done"))
        if result["next_offset"] is None:
            break
        offset = result["next_offset"]
    _, found, _ = h._validate_artifact("review", data)
    assert found and all("adopted_dependency_has_blocking_issue" in row["message"] for row in found)
    ref = a.put("review", data, h.job["id"])
    engine = Engine.__new__(Engine)
    engine.ws, engine.atlas, engine.artifacts, engine.config = c["ws"], c["atlas"], a, config
    with pytest.raises(ProtocolError, match="adopted_dependency_has_blocking_issue"):
        engine._validate_stage(c["ws"].job(h.job["id"]), {"status": "complete", "artifact_refs": [ref]})
