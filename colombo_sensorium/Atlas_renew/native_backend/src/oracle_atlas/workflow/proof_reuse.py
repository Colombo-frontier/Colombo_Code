"""Reuse catalog for pinned standalone propositions; current bound applicability and document publication approval are not reused.

The controller compares the proof and listed mathematical context with the pinned source closure only after an independent reviewer explicitly declares them self-contained and complete.
Python verifies only records, hashes, scopes, and approval chains; it does not infer mathematical relevance.
"""
from __future__ import annotations

from collections import Counter

from ..core.contracts import ProtocolError, references, resolve_pointer, validate
from ..core.store import digest, dumps
from .review_context import _Graph, _Unavailable, _get, _prior_review, _snapshot


MAX_PROOFS = 128
MAX_PROOF_REFERENCES = 512
MAX_CONTEXT_POINTERS = 64
MAX_CONTEXT_BYTES = 4_000_000
MAX_ISSUES = 200
MAX_ISSUE_SCAN_DEPTH = 32
MAX_ISSUE_SCAN_NODES = 50_000
MAX_ISSUE_SCAN_BYTES = 8_000_000
BLOCKING = {"bound", "profile", "publication"}
APPROVAL_KEYS = {"proof_ref", "scope", "assumptions_complete", "context_pointers", "reason"}
ISSUE_SCOPE_KEYS = {"issue_id", "affected_proof_refs", "scope_complete", "reason"}
ALWAYS_REVIEW = ["current_bound_applicability_and_quantifiers", "all_active_bound_adoption",
                 "changed_scientific_environment", "new_counterexamples_and_source_evidence",
                 "comparisons_and_coverage", "reader_and_current_prepared_five_files"]


def _proofs(artifacts, snapshot):
    research, profile = snapshot["research"]["data"], snapshot["profile"]
    refs = set(research.get("proof_refs", []))
    profile_refs = references(profile.get("proofs", []))
    result_refs = research.get("result_refs", [])
    if len(refs) > MAX_PROOFS or len(profile_refs) > MAX_PROOF_REFERENCES or len(result_refs) > MAX_PROOF_REFERENCES:
        raise _Unavailable("proof_reference_count_limit")
    for ref in profile_refs:
        item = _get(artifacts, ref)
        if item["kind"] == "proof":
            refs.add(ref)
    for ref in result_refs:
        item = _get(artifacts, ref, "result")
        refs.update(item["data"].get("proof_refs", []))
    if len(refs) > MAX_PROOFS:
        raise _Unavailable("proof_count_limit")
    values = {}
    ids = {}
    for ref in sorted(refs):
        item = _get(artifacts, ref, "proof")
        validate("proof", item["data"])
        values[ref] = item
        pid = item["data"]["proof_id"]
        ids.setdefault(pid, set()).add(ref)
    return values, ids


def _structured_issues(*documents):
    """Scan only actual dict/list objects; do not interpret natural language or JSON embedded in strings.

    Scientific issues may appear in any structured container, including proofs/evidence/quarantined_claims.
    The full traversal shares depth, node, and serialized-byte budgets; unknown structures cannot become evidence for reuse.
    """
    pending = [(document, 0, "normal") for document in reversed(documents)]
    nodes = byte_count = 0
    required = {"issue_id", "kind", "scope", "subject_refs", "blocks", "message", "evidence_refs", "resolves"}
    while pending:
        value, depth, mode = pending.pop()
        nodes += 1
        if depth > MAX_ISSUE_SCAN_DEPTH:
            raise _Unavailable("issue_scan_depth_limit")
        if nodes > MAX_ISSUE_SCAN_NODES:
            raise _Unavailable("issue_scan_node_limit")
        if isinstance(value, dict):
            if any(not isinstance(key, str) for key in value):
                raise _Unavailable("issue_scan_unknown_json_key")
            byte_count += 2 + max(0, len(value) - 1) + sum(len(dumps(key).encode("utf-8")) + 1 for key in value)
        elif isinstance(value, list):
            byte_count += 2 + max(0, len(value) - 1)
        elif value is None or isinstance(value, (str, int, float, bool)):
            byte_count += len(dumps(value).encode("utf-8"))
        else:
            raise _Unavailable("issue_scan_unknown_json_value")
        if byte_count > MAX_ISSUE_SCAN_BYTES:
            raise _Unavailable("issue_scan_byte_limit")
        if mode == "issue_row":
            if not isinstance(value, dict) or not required.issubset(value):
                raise _Unavailable("issue_scope_unknown")
            if any(not isinstance(value[key], str) or not value[key].strip() for key in ("issue_id", "kind", "scope", "message")):
                raise _Unavailable("issue_scope_unknown")
            if any(not isinstance(value[key], list) or any(not isinstance(item, str) for item in value[key])
                   for key in ("subject_refs", "blocks", "evidence_refs", "resolves")):
                raise _Unavailable("issue_subject_scope_unknown")
            if not set(value["blocks"]).issubset(BLOCKING | {"extraction", "identity"}):
                raise _Unavailable("issue_block_scope_unknown")
            yield value
        if isinstance(value, dict):
            for key, child in reversed(list(value.items())):
                if key == "issues":
                    if not isinstance(child, list):
                        raise _Unavailable("issue_list_unknown")
                    pending.append((child, depth + 1, "issue_array"))
                else:
                    pending.append((child, depth + 1, "normal"))
        elif isinstance(value, list):
            child_mode = "issue_row" if mode == "issue_array" else "normal"
            pending.extend((child, depth + 1, child_mode) for child in reversed(value))


def _blocking_issues(snapshot, review):
    issues = {}
    for row in _structured_issues(snapshot["profile"], snapshot["research"]["data"], review):
        if not BLOCKING.intersection(row["blocks"]):
            continue
        iid, subjects = row["issue_id"], row["subject_refs"]
        # A stable issue may have both producer text and review notes; scope declarations must cover
        # all versions, rather than the controller inferring from free text which version has been superseded.
        previous = issues.setdefault(iid, {"issue_id": iid, "subject_refs": [], "blocks": [], "variant_signatures": []})
        previous["subject_refs"] = sorted(set(previous["subject_refs"]) | set(subjects))
        previous["blocks"] = sorted(set(previous["blocks"]) | set(row["blocks"]))
        previous["variant_signatures"] = sorted(set(previous["variant_signatures"]) | {digest(row)})
        if len(issues) > MAX_ISSUES:
            raise _Unavailable("issue_count_limit")
    return issues


def _approvals(review):
    rows = review.get("proof_approvals", [])
    if not isinstance(rows, list) or len(rows) > MAX_PROOFS:
        raise _Unavailable("proof_approval_list_invalid")
    out = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != APPROVAL_KEYS:
            raise _Unavailable("proof_approval_shape_invalid")
        ref = row["proof_ref"]
        if not isinstance(ref, str) or references(ref) != {ref} or ref in out:
            raise _Unavailable("proof_approval_reference_ambiguous")
        if row["scope"] != "standalone_proposition" or row["assumptions_complete"] is not True:
            raise _Unavailable("proof_approval_not_complete_standalone_scope")
        if not isinstance(row["reason"], str) or not row["reason"].strip():
            raise _Unavailable("proof_approval_reason_missing")
        pointers = row["context_pointers"]
        if not isinstance(pointers, list) or not pointers or len(pointers) > MAX_CONTEXT_POINTERS:
            raise _Unavailable("proof_context_pointer_limit_or_missing")
        if any(not isinstance(p, str) for p in pointers) or len(set(pointers)) != len(pointers):
            raise _Unavailable("proof_context_pointer_ambiguous")
        if "/common_specification" not in pointers:
            raise _Unavailable("proof_context_native_contract_missing")
        out[ref] = row
    return out


def _issue_scopes(review, issues, proofs):
    rows = review.get("proof_issue_scopes", [])
    if not isinstance(rows, list) or len(rows) > MAX_ISSUES:
        raise _Unavailable("proof_issue_scope_list_invalid")
    scopes = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != ISSUE_SCOPE_KEYS:
            raise _Unavailable("proof_issue_scope_shape_invalid")
        iid = row["issue_id"]
        refs = row["affected_proof_refs"]
        if not isinstance(iid, str) or iid in scopes or iid not in issues:
            raise _Unavailable("proof_issue_scope_id_unknown_or_ambiguous")
        if not isinstance(refs, list) or any(not isinstance(r, str) for r in refs) or len(refs) != len(set(refs)) or not set(refs).issubset(proofs):
            raise _Unavailable("proof_issue_scope_reference_unknown")
        if type(row["scope_complete"]) is not bool or not isinstance(row["reason"], str) or not row["reason"].strip():
            raise _Unavailable("proof_issue_scope_not_explicit")
        scopes[iid] = row
    if set(issues) != set(scopes):
        raise _Unavailable("proof_issue_scope_missing")
    return scopes


def _issue_blocks(ref, proof, issues, scopes):
    for iid, issue in issues.items():
        subjects = issue.get("subject_refs")
        if not isinstance(subjects, list) or any(not isinstance(s, str) for s in subjects):
            return "issue_subject_scope_unknown"
        # An unaffected declaration cannot override a genuine blocker that directly targets this proof.
        if ref in subjects or proof["proof_id"] in subjects:
            return "direct_proof_blocker"
        scope = scopes[iid]
        if not scope["scope_complete"]:
            return "proof_issue_scope_incomplete"
        if ref in scope["affected_proof_refs"]:
            return "scoped_proof_blocker"
    return None


def _fingerprint(artifacts, snapshot, ref, approval, graph):
    proof = _get(artifacts, ref, "proof")["data"]
    context = {p: resolve_pointer(snapshot["profile"], p) for p in approval["context_pointers"]}
    if len(dumps(context).encode("utf-8")) > MAX_CONTEXT_BYTES:
        raise _Unavailable("proof_context_byte_limit")
    roots = {ref} | references(context)
    closure, byte_count = graph.closure(roots)
    # A profile-level declaration cannot remove blockers retained by source or proof objects themselves.
    dependencies = [graph.item(row["ref"])["data"] for row in closure]
    for issue in _structured_issues(*dependencies):
        if BLOCKING.intersection(issue["blocks"]):
            raise _Unavailable("proof_dependency_has_blocking_issue")
    return {"fingerprint": digest({"proof": proof, "proof_ref": ref, "context": context, "closure": closure,
                                  "prepared_semantics_version": snapshot["prepared"].get("semantics_version")}),
            "context_digest": digest(context), "context_pointers": sorted(approval["context_pointers"]),
            "dependency_count": len(closure), "dependency_bytes": byte_count,
            "dependency_refs": [row["ref"] for row in closure]}


def _contract(artifacts, snapshot, review):
    proofs, ids = _proofs(artifacts, snapshot)
    approvals = _approvals(review)
    if not set(approvals).issubset(proofs):
        raise _Unavailable("proof_approval_not_in_current_scientific_record")
    issues = _blocking_issues(snapshot, review)
    scopes = _issue_scopes(review, issues, proofs)
    graph = _Graph(artifacts)
    fingerprints = {}
    for ref, approval in approvals.items():
        if len(ids[proofs[ref]["data"]["proof_id"]]) != 1:
            raise _Unavailable("proof_id_ambiguous")
        reason = _issue_blocks(ref, proofs[ref]["data"], issues, scopes)
        if reason:
            raise _Unavailable(reason)
        fingerprints[ref] = _fingerprint(artifacts, snapshot, ref, approval, graph)
    return proofs, approvals, fingerprints, issues, scopes


def build_proof_review_context(artifacts, ws, current_proposal_ref, previous_review_ref=None):
    """Build a compact catalog; only explicit standalone proposition certificates can supply candidates, and automatic approval is never returned."""
    out = {"context_version": "1.0.3", "current_proposal_ref": current_proposal_ref,
           "previous_review_ref": None, "reuse_status": "no_prior_review",
           "proof_catalog": [], "reusable_proof_refs": [], "proof_candidates": [],
           "invalidated_proofs": [], "always_review": ALWAYS_REVIEW[:],
           "issue_scan_limits": {"depth": MAX_ISSUE_SCAN_DEPTH, "nodes": MAX_ISSUE_SCAN_NODES, "bytes": MAX_ISSUE_SCAN_BYTES},
           "notice": "Reuse only the reviewed proof reading for a pinned standalone proposition, without approving the current application/bound/envelope/document; any new scientific evidence may still veto it."}
    try:
        current = _snapshot(artifacts, current_proposal_ref)
        current_proofs, current_ids = _proofs(artifacts, current)
        out.update(current_prepared_ref=current["proposal"]["prepared_ref"],
                   current_bundle_hash=current["prepared"]["bundle_hash"])
        for ref, item in current_proofs.items():
            out["proof_catalog"].append({"proof_ref": ref, "proof_id": item["data"]["proof_id"],
                 "proposition_excerpt": item["data"]["proposition"][:240]})
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        out.update(reuse_status="current_snapshot_unavailable", validation_reason=str(exc)[:240])
        return out
    if not previous_review_ref:
        return out
    try:
        review, prior, reviewer_job = _prior_review(artifacts, ws, previous_review_ref)
        if not review.get("proof_approvals"):
            out["reuse_status"] = "no_explicit_prior_proof_approval"
            return out
        prior_proofs, approvals, fingerprints, _, _ = _contract(artifacts, prior, review)
        if prior["profile"]["setting_id"] != current["profile"]["setting_id"]:
            raise _Unavailable("different_setting_id")
        # Unreviewed scientific issues from the current producer cannot be skipped because a standalone proposition was approved previously.
        current_issues = _blocking_issues(current, {})
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        out.update(reuse_status="prior_proof_contract_unavailable", validation_reason=str(exc)[:240])
        return out
    out.update(previous_review_ref=previous_review_ref, previous_proposal_ref=prior["ref"],
               previous_prepared_ref=prior["proposal"]["prepared_ref"], previous_reviewer_job_id=reviewer_job,
               reuse_status="candidates_verified", changed_profile_fields=sorted(k for k in prior["profile"].keys() | current["profile"].keys() if prior["profile"].get(k) != current["profile"].get(k)))
    graph = _Graph(artifacts)
    prior_issues = _blocking_issues(prior, review)
    for ref, item in current_proofs.items():
        reason = None
        if len(current_ids[item["data"]["proof_id"]]) != 1:
            reason = "proof_id_ambiguous"
        elif ref not in approvals:
            reason = "no_explicit_prior_proof_approval"
        elif artifacts.owned(ref, reviewer_job) or prior_proofs[ref].get("producer") == reviewer_job:
            reason = "proof_reviewer_not_independent"
        else:
            try:
                before = fingerprints[ref]
                after = _fingerprint(artifacts, current, ref, approvals[ref], graph)
                if before["fingerprint"] != after["fingerprint"]:
                    reason = "proof_context_or_dependency_changed"
                else:
                    # A previous review may explain only issues it checked at the time; new or changed issues require a fresh independent impact assessment.
                    for iid, issue in current_issues.items():
                        if iid not in prior_issues or not set(issue["variant_signatures"]).issubset(prior_issues[iid]["variant_signatures"]):
                            reason = "new_scientific_issue_requires_review"
                            break
                    if reason is None:
                        out["reusable_proof_refs"].append(ref)
                        out["proof_candidates"].append({"proof_ref": ref, "proof_id": item["data"]["proof_id"],
                             "previous_review_ref": previous_review_ref, "previous_proposal_ref": prior["ref"],
                             **{k: after[k] for k in ("fingerprint", "context_digest", "context_pointers", "dependency_count", "dependency_bytes")},
                             "reason": "Explicit standalone proposition approval with an independently completed validated_handoff; the proof, fully declared context, and pinned dependencies are unchanged; the current application requires fresh review."})
            except (ProtocolError, KeyError, TypeError, ValueError) as exc:
                reason = "proof_dependency_unavailable: " + str(exc)[:180]
        if reason:
            out["invalidated_proofs"].append({"proof_ref": ref, "reason": reason})
    out["invalidation_counts"] = dict(Counter(row["reason"].split(":", 1)[0] for row in out["invalidated_proofs"]))
    return out


def proof_approval_errors(review, inputs, artifacts, *, resolve=None):
    """Recheck before freezing the review and at engine handoff; older uncertified records remain readable but cannot be reused through this mechanism."""
    enabled = bool(inputs.get("proof_context_ref"))
    fields = {"proof_approvals", "proof_issue_scopes", "proof_reuse_context_ref", "reused_proof_refs"}
    if not enabled and not fields.intersection(review):
        return []
    errors = []

    def add(code, path, message):
        errors.append({"code": code, "path": path, "message": message})

    if enabled and not fields.issubset(review):
        add("proof_contract_missing", "/", "This task must explicitly submit proof approvals, issue scopes, and reuse fields; even empty lists must be recorded explicitly.")
    if review.get("review_type") != "profile" or review.get("subject_ref") != inputs.get("subject_ref"):
        add("proof_review_subject", "/subject_ref", "A proof certificate must bind the pinned proposal under the current profile review.")
        return errors
    try:
        snapshot = _snapshot(artifacts, review["subject_ref"])
        # Proof reuse is an optional optimization. Unknown legacy free-form objects may receive full review in the current independent review,
        # but they must explicitly declare that no proof certificates are issued and no proofs are reused; a scan failure must not block ordinary scientific review.
        if review.get("proof_approvals", []) == [] and review.get("reused_proof_refs", []) == []:
            context_ref = review.get("proof_reuse_context_ref")
            if context_ref is not None and context_ref != inputs.get("proof_context_ref"):
                add("proof_reuse_context", "/proof_reuse_context_ref", "Without reuse, retain only this job catalog or null; do not rebind to another context.")
            return errors
        proofs, approvals, _, _, _ = _contract(artifacts, snapshot, review)
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        add("proof_approval_contract", "/proof_approvals", str(exc))
        return errors
    reused = review.get("reused_proof_refs", [])
    if not isinstance(reused, list) or any(not isinstance(ref, str) for ref in reused) or len(set(reused)) != len(reused):
        add("proof_reuse_scope", "/reused_proof_refs", "Reused proof references must be unique and refer to formal proof artifacts.")
        return errors
    if not set(reused).issubset(approvals):
        add("proof_reuse_adoption", "/reused_proof_refs", "Reused candidates must still be explicitly approved in this round of proof_approvals; this does not approve current bound applicability.")
    if reused:
        context_ref = inputs.get("proof_context_ref")
        if not context_ref or review.get("proof_reuse_context_ref") != context_ref:
            add("proof_reuse_context", "/proof_reuse_context_ref", "A reuse declaration must bind the controller catalog for this job.")
        else:
            try:
                item = (resolve or artifacts.get)(context_ref)
                context = item["data"]
                if item["kind"] != "external_result" or context.get("context_version") != "1.0.3" or context.get("current_proposal_ref") != review["subject_ref"] or context.get("current_bundle_hash") != snapshot["prepared"]["bundle_hash"]:
                    raise _Unavailable("proof_reuse_context_binding_mismatch")
                # Even if a fabricated external_result is mistakenly passed from an outer layer, self-reported candidates cannot
                # obtain reuse. Mechanically recompute the current job catalog and the genuine independent approval chain.
                ws = getattr(artifacts, "workspace", None)
                if ws is None or not context.get("previous_review_ref"):
                    raise _Unavailable("proof_reuse_context_has_no_independent_prior_review")
                verified = build_proof_review_context(artifacts, ws, review["subject_ref"], context["previous_review_ref"])
                keys = ("current_proposal_ref", "current_prepared_ref", "current_bundle_hash", "previous_review_ref", "reusable_proof_refs", "proof_candidates")
                if any(context.get(key) != verified.get(key) for key in keys):
                    raise _Unavailable("proof_reuse_context_not_controller_verifiable")
                if not set(reused).issubset(set(context.get("reusable_proof_refs", []))):
                    raise _Unavailable("proof_reuse_outside_controller_candidates")
                candidates = {row["proof_ref"]: row for row in verified["proof_candidates"]}
                if any(sorted(approvals[ref]["context_pointers"]) != candidates[ref]["context_pointers"] for ref in reused):
                    raise _Unavailable("reused_proof_context_declaration_changed")
            except (ProtocolError, KeyError, TypeError, ValueError) as exc:
                add("proof_reuse_context", "/proof_reuse_context_ref", str(exc))
    return errors
