"""Historical-context credentials are opt-in, complete and independently bound.

Synthetic proof statements test the same provenance shape as the real matrix
failure. Passing these tests does not establish a mathematical proposition.
"""
from copy import deepcopy

import pytest

from oracle_atlas.core.store import digest, dumps
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.workflow.issue_semantics import dependency_issue_catalog
from oracle_atlas.workflow.review_context import _snapshot, bound_approval_errors, build_review_context
from oracle_atlas.workflow.proof_reuse import proof_approval_errors, build_proof_review_context
from test_proof_reuse import proof_context
from test_review_context import context
from test_draft_clone import host
from test_exact_checks import program


@pytest.fixture
def historical(proof_context):
    c = proof_context; a = c["ws"].artifacts
    proposal = a.get(c["prior"])["data"]
    old_candidate = deepcopy(a.get(proposal["candidate_ref"])["data"])
    old_candidate["candidate_id"] = "historical-sibling-p7"
    old_candidate["issues"] = [c["issue"]("p7-hidden-sibling", subjects=[c["source"]], blocks=["bound"])]
    cref = a.put("candidate", old_candidate, c["producer"])
    old_identity = deepcopy(a.get(proposal["identity_ref"])["data"])
    old_identity.update(candidate_ref=cref, issues=[c["issue"]("p8-source-scope", subjects=[cref], blocks=["bound"])])
    iref = a.put("identity", old_identity, c["producer"])
    old_review = {"subject_ref": iref, "review_type": "identity", "verdict": "approve", "assessments": [],
                  "issues": [c["issue"]("p8-source-scope", subjects=[cref], blocks=["bound"])],
                  "approved_bound_ids": [], "summary": "Synthetic historical source ambiguity retained."}
    rref = a.put("review", old_review, c["producer"])
    transfer = a.put("external_result", {"candidate_ref": cref, "identity_ref": iref, "identity_review_ref": rref}, c["producer"])
    pref = c["proof"](dependencies=[c["source"], transfer])
    p = deepcopy(c["profile"]); p["proofs"] = [{"id": "proof:fixture", "proof_ref": pref}]
    p["bounds"][0]["proof_refs"] = ["proof:fixture"]
    current = c["proposal"](p)
    c.update(profile=p, prior=current, proof_ref=pref, historical_candidate=cref,
             historical_identity=iref, historical_review=rref, transfer=transfer)

    def certificate(subject=current, *, version="occurrence-bound-scope", validated=True):
        reviewref, jid = c["review"](subject=subject, validated=validated)
        data = deepcopy(a.get(reviewref)["data"])
        data.update(issue_scope_version=version,
                    bound_approvals=[{"bound_id": "u", "scope": "bound_applicability", "assumptions_complete": True,
                       "context_pointers": ["/common_specification"], "reason": "Synthetic complete scope only."}],
                    proof_approvals=[{"proof_ref": pref, "scope": "standalone_proposition", "assumptions_complete": True,
                       "context_pointers": ["/common_specification"], "reason": "Synthetic complete proposition only."}],
                    bound_issue_scopes=[], proof_issue_scopes=[], proof_reuse_context_ref=None, reused_proof_refs=[])
        if version == "occurrence-bound-scope":
            data["proof_approvals"][0]["execution_check"] = {
                "required": False, "reason": "Software fixture contains no mathematical oracle simulation or branch algorithm.", "check_refs": []}
            catalog = dependency_issue_catalog(a, _snapshot(a, subject), data)
            groups = {}
            for occurrence in catalog["issue_occurrences"]:
                groups.setdefault(occurrence["issue_id"], []).append(occurrence["occurrence_id"])
            for iid, ids in groups.items():
                common = {"issue_id": iid, "scope_complete": True, "occurrence_ids": sorted(ids),
                          "reason": "Independent synthetic fixture explicitly checks every listed original variant; no mathematical certification."}
                data["bound_issue_scopes"].append({**common, "affected_bound_ids": []})
                data["proof_issue_scopes"].append({**common, "affected_proof_refs": []})
        return data, jid

    def freeze(data, jid):
        ref = a.put("review", data, jid)
        c["ws"].save_job(jid, "complete", {}, {"status": "complete", "artifact_refs": [ref], "summary": "fixture", "checkpoint_ref": None})
        c["ws"].event(jid, "validated_handoff", {"status": "complete", "refs": [ref]})
        return ref

    c.update(certificate=certificate, freeze_certificate=freeze)
    return c


def errors(c, data, **inputs):
    inputs = {"subject_ref": data["subject_ref"], **inputs}
    return bound_approval_errors(data, inputs, c["ws"].artifacts) + proof_approval_errors(data, inputs, c["ws"].artifacts)


def test_complete_contextual_occurrences_are_readable_and_do_not_erase_history(historical):
    c = historical; a = c["ws"].artifacts
    catalog = dependency_issue_catalog(a, _snapshot(a, c["prior"]))
    assert len(catalog["issue_occurrences"]) == 3
    assert not catalog["hard_dependency_blockers"]
    for row in catalog["issue_occurrences"]:
        assert row["variant_hash"] == digest(row["issue"])
        assert row["issue_pointer"] == "/issues/0"
        assert row["artifact_role"] in {"historical_candidate", "historical_identity", "historical_identity_review"}
        assert a.get(row["artifact_ref"])["data"]["issues"][0] == row["issue"]
    current, jid = c["certificate"]()
    assert errors(c, current, issue_scope_contract_version="occurrence-bound-scope") == []
    ref = c["freeze_certificate"](current, jid)
    assert build_review_context(a, c["ws"], c["prior"], ref)["reusable_bound_ids"] == ["u"]
    assert build_proof_review_context(a, c["ws"], c["prior"], ref)["reusable_proof_refs"] == [c["proof_ref"]]


@pytest.mark.parametrize("mode", ["missing_sibling", "missing_occurrence", "changed_hash", "duplicate_occurrence", "unknown_occurrence"])
def test_unseen_sibling_or_unlisted_variant_cannot_be_implicitly_covered(historical, mode):
    c = historical; data, _ = c["certificate"]()
    for field in ("bound_issue_scopes", "proof_issue_scopes"):
        if mode == "missing_sibling":
            data[field] = [r for r in data[field] if r["issue_id"] != "p7-hidden-sibling"]
            continue
        row = next(r for r in data[field] if r["issue_id"] == "p8-source-scope")
        if mode == "missing_occurrence": row["occurrence_ids"].pop()
        elif mode == "duplicate_occurrence": row["occurrence_ids"].append(row["occurrence_ids"][0])
        else: row["occurrence_ids"][0] = "occurrence:" + ("0" if mode == "changed_hash" else "1") * 64
    found = errors(c, data)
    assert len(found) == 2
    assert all("scope_missing" in e["message"] or "occurrence_scope_missing_or_changed" in e["message"] for e in found)


def test_old_scope_is_not_reinterpreted_and_new_task_cannot_select_old_version(historical):
    c = historical; old, _ = c["certificate"](version="snapshot-bound-scope")
    found = errors(c, old)
    assert {e["message"] for e in found} == {"bound_dependency_has_blocking_issue", "proof_dependency_has_blocking_issue"}
    found = errors(c, old, issue_scope_contract_version="occurrence-bound-scope")
    assert {e["code"] for e in found} == {"bound_issue_scope_version", "proof_issue_scope_version"}


@pytest.mark.parametrize("container", ["proof", "result", "source"])
def test_direct_scientific_defects_cannot_be_scoped_away(historical, container):
    c = historical; a = c["ws"].artifacts
    issue = c["issue"]("direct-unrepaired-defect", subjects=["proof:fixture"], blocks=["bound"])
    if container == "proof":
        pref = c["proof"](dependencies=[c["source"], c["transfer"]], issues=[issue])
    elif container == "result":
        result = deepcopy(a.get(c["profile"]["bounds"][0]["result_ref"])["data"]); result["issues"] = [issue]
        pref = c["proof"](dependencies=[a.put("result", result, c["producer"]), c["transfer"]])
    else:
        source = deepcopy(a.get(c["source"])["data"])
        source["metadata"]["issues"] = [issue]
        pref = c["proof"](dependencies=[a.put("source", source, c["producer"]), c["transfer"]])
    p = deepcopy(c["profile"]); p["proofs"][0]["proof_ref"] = pref
    subject = c["proposal"](p); data, _ = c["certificate"](subject)
    data["proof_approvals"][0]["proof_ref"] = pref
    found = errors(c, data)
    assert any(e["message"] == "bound_dependency_has_blocking_issue" for e in found)
    assert any(e["message"].startswith("adopted_dependency_has_blocking_issue:") for e in found)
    catalog = dependency_issue_catalog(a, _snapshot(a, subject))
    assert any(row["artifact_kind"] == container for row in catalog["hard_dependency_blockers"])


def test_new_historical_occurrence_invalidates_reuse_even_with_same_issue_text(historical):
    c = historical; a = c["ws"].artifacts
    data, jid = c["certificate"](); prior_review = c["freeze_certificate"](data, jid)
    extra = deepcopy(a.get(c["historical_candidate"])["data"])
    extra["candidate_id"] = "new-unreviewed-provenance-context"
    ref = a.put("candidate", extra, c["producer"])
    p = deepcopy(c["profile"])
    # New unrelated profile context does not change the standalone proof or its
    # declared common-specification pointers; its unseen issue still needs scope.
    p["quarantined_claims"] = [{"id": "new-context", "candidate_ref": ref}]
    current = c["proposal"](p)
    out = build_proof_review_context(a, c["ws"], current, prior_review)
    assert out["reusable_proof_refs"] == []
    assert out["invalidated_proofs"][0]["reason"] == "new_scientific_issue_requires_review"


def test_dependency_change_still_revokes_the_certificate(historical):
    c = historical; a = c["ws"].artifacts
    data, jid = c["certificate"](); prior_review = c["freeze_certificate"](data, jid)
    pref = c["proof"](dependencies=[c["source"], c["transfer"]], argument="Changed synthetic proof body.")
    p = deepcopy(c["profile"]); p["proofs"][0]["proof_ref"] = pref
    current = c["proposal"](p)
    assert not build_review_context(a, c["ws"], current, prior_review)["reusable_bound_ids"]
    assert not build_proof_review_context(a, c["ws"], current, prior_review)["reusable_proof_refs"]


def test_new_first_review_receives_occurrence_catalog_without_prior_credentials(historical):
    c = historical; a = c["ws"].artifacts
    for out in (build_review_context(a, c["ws"], c["prior"]), build_proof_review_context(a, c["ws"], c["prior"])):
        assert out["issue_scope_version"] == "occurrence-bound-scope"
        assert out["issue_catalog_status"] == "complete"
        assert len(out["issue_occurrences"]) == 3
        assert out["reuse_status"] == "no_prior_review"


def test_new_review_issue_ids_are_computed_by_preflight_not_by_the_model(historical):
    c = historical; data, _ = c["certificate"]()
    data["issues"] = [c["issue"]("new-publication-note", subjects=["metadata-only"], blocks=["publication"])]
    found = errors(c, data)
    assert len(found) == 2
    for error in found:
        diagnostic = error["scope_diagnostic"]
        current = diagnostic["current_review_occurrences"]
        assert len(current) == 1 and current[0]["artifact_ref"] is None
        assert current[0]["subject_ref"] == c["prior"] and current[0]["issue_pointer"] == "/issues/0"
        expected = next(r for r in diagnostic["expected_issue_scopes"] if r["issue_id"] == "new-publication-note")
        assert expected["occurrence_ids"] == [current[0]["occurrence_id"]]


def test_declining_credentials_does_not_omit_adopted_proof_execution_declaration(historical):
    c = historical; data, _ = c["certificate"]()
    declaration = {"proof_ref": c["proof_ref"], "execution_check": data["proof_approvals"][0]["execution_check"]}
    data["proof_approvals"] = []; data["bound_approvals"] = []
    found = errors(c, data, issue_scope_contract_version="occurrence-bound-scope")
    assert any("adopted_proof_execution_declaration_missing" in row["message"] for row in found)
    assert found[-1]["adopted_proof_requirements"] == [{"proof_ref": c["proof_ref"], "bound_ids": ["u"]}]
    data["proof_execution_checks"] = [declaration]
    assert errors(c, data, issue_scope_contract_version="occurrence-bound-scope") == []
    # No approval is being attempted: the unused historical proof is not an
    # execution target merely because a context archive mentions it.
    data["approved_bound_ids"] = []; data["proof_execution_checks"] = []
    assert errors(c, data, issue_scope_contract_version="occurrence-bound-scope") == []


def test_actual_execution_receipt_is_required_and_cannot_be_fabricated(historical):
    c = historical; a = c["ws"].artifacts; data, jid = c["certificate"]()
    check = {"required": True, "reason": "Exercise a synthetic rational branch, not a scientific theorem.", "check_refs": []}
    data["proof_approvals"][0]["execution_check"] = check
    assert any("executed receipts" in row["message"] for row in errors(c, data))
    config = {"atlas": str(c["atlas"].root), "workspace": str(c["ws"].root), "budgets": dict(DEFAULTS), "model": {}}
    h = host((c["atlas"], c["ws"], config), {}, "profile_reviewer", job_id=jid)
    h.call("artifact_get", {"ref": c["prior"], "pointer": "", "offset": 0, "limit": 24000}, "read-proposal")
    profile_ref = a.get(c["prior"])["data"]["profile_ref"]
    h.call("artifact_get", {"ref": profile_ref, "pointer": "/proofs", "offset": 0, "limit": 24000}, "read-declared-proofs")
    result = h.call("exact_check", {"label": "Credential fixture branch", "program_json": dumps(program()),
                    "evidence_refs": [c["proof_ref"]]}, "scope-actual-execution")
    check["check_refs"] = [result["check_ref"]]
    assert errors(c, data) == []
    body = deepcopy(a.get(result["check_ref"])["data"]); body["label"] = "Self-written fake execution"
    fake = a.put("external_result", body, jid)
    check["check_refs"] = [fake]
    assert any("actual tool execution" in row["message"] for row in errors(c, data))
    bad = h.call("exact_check", {"label": "Executed failing fixture", "program_json": dumps(program("1")),
                 "evidence_refs": [c["proof_ref"]]}, "scope-failed-execution")
    check["check_refs"] = [bad["check_ref"]]
    assert any("failed" in row["message"] for row in errors(c, data))
    check["check_refs"] = [result["check_ref"]]
    prior_review = c["freeze_certificate"](data, jid)
    assert build_proof_review_context(a, c["ws"], c["prior"], prior_review)["reusable_proof_refs"] == [c["proof_ref"]]
    p = deepcopy(c["profile"]); p["reader_markdown"] = "Presentation changed; synthetic proof and contract did not."
    current = c["proposal"](p); renewed, _ = c["certificate"](current)
    renewed["proof_approvals"][0]["execution_check"] = check
    assert errors(c, renewed) == []


def test_execution_targets_do_not_expand_through_historical_context(historical):
    c = historical; a = c["ws"].artifacts
    unrelated = c["proof"]("unadopted-context-proof", argument="Historical unrelated theorem fixture.")
    # Add an unused formally stored proof to the profile. It is not on an
    # adopted bound's explicit scientific support chain.
    p = deepcopy(c["profile"]); p["proofs"].append({"id": "unadopted-context-proof", "proof_ref": unrelated})
    current = c["proposal"](p); out = build_proof_review_context(a, c["ws"], current)
    assert out["adopted_proof_requirements"] == [{"proof_ref": c["proof_ref"], "bound_ids": ["u"]}]
