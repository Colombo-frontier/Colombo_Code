"""Reuse catalog for pinned standalone propositions; current bound applicability and document publication approval are not reused.

The controller compares the proof and listed mathematical context with the pinned source closure only after an independent reviewer explicitly declares them self-contained and complete.
Python verifies only records, hashes, scopes, and approval chains; it does not infer mathematical relevance.
"""
from __future__ import annotations

from collections import Counter

from ..core.contracts import ProtocolError, references, resolve_pointer, validate
from ..core.store import digest, dumps
from .review_context import _Graph, _Unavailable, _get, _prior_review, _snapshot
from .issue_semantics import (ISSUE_SCOPE_VERSION, OCCURRENCE_SCOPE_VERSION, SEMANTIC_SCOPE_VERSIONS,
                              CONTEXTUAL_KINDS, dependency_issue_catalog, issue_audit, issue_signature)
from .issue_semantics import occurrence_signature, scope_diagnostic, verified_delivery_lineage
from .scope_revalidation import (EXPLICIT_SCOPE, declared_context, scientific_material,
                                 revalidation_candidate, mathematical_dependencies)


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


def adopted_scientific_dependencies(artifacts, snapshot, approved_bound_ids, *, active_only=True):
    """Follow adopted bounds' explicit mathematical support, not provenance.

    Proof/result/source defects belong to adoption even when no optional reuse
    credential is requested. Candidate, identity, review and external workflow
    objects are never recursively expanded by this narrow adoption traversal.
    """
    from ..atlas.store import _active_bounds
    from .review_context import _bound_map, _records
    profile = snapshot["profile"]
    bounds, invalid = _bound_map(profile)
    if invalid or not set(approved_bound_ids).issubset(bounds):
        raise _Unavailable("adopted_bound_scope_invalid")
    active = (_active_bounds(profile) & set(approved_bound_ids)) if active_only else set(approved_bound_ids)
    index, _ = _records(profile)
    fields = {"proof_refs": "proof", "proof_ref": "proof", "proof_artifact_ref": "proof",
              "result_refs": "result", "result_ref": "result", "result_artifact_ref": "result",
              "source_refs": "source", "source_ref": "source",
              "evidence_refs": None, "evidence_ref": None, "artifact_ref": None}
    by_ref = {}
    for bid in sorted(active):
        pending, visited = [], set()

        def support(data):
            for key, expected in fields.items():
                if key not in data:
                    continue
                values = data[key] if isinstance(data[key], list) else [data[key]]
                if any(not isinstance(v, str) for v in values):
                    raise _Unavailable("adopted_support_reference_shape_unknown")
                pending.extend((value, expected) for value in values)

        support(bounds[bid])
        while pending:
            value, expected = pending.pop()
            if (value, expected) in visited:
                continue
            visited.add((value, expected))
            if len(visited) > MAX_PROOF_REFERENCES:
                raise _Unavailable("adopted_proof_dependency_limit")
            if references(value) == {value}:
                item = _get(artifacts, value)
                if expected and item["kind"] != expected:
                    raise _Unavailable("adopted_support_kind_mismatch")
                if item["kind"] in {"proof", "result", "source"}:
                    by_ref.setdefault(value, {"kind": item["kind"], "bound_ids": set()})["bound_ids"].add(bid)
                if item["kind"] == "proof":
                    for dep in item["data"].get("dependencies", []):
                        # Explicit mathematical dependencies may be proof or
                        # result records. Reviews, candidates and identity
                        # archives are provenance, not a new execution target.
                        child = _get(artifacts, dep)
                        if child["kind"] in {"proof", "result", "source"}:
                            pending.append((dep, child["kind"]))
                elif item["kind"] == "result":
                    pending.extend((ref, "proof") for ref in item["data"].get("proof_refs", []))
                    pending.extend((ref, "source") for ref in item["data"].get("source_refs", []))
                    pending.extend((row["source_ref"], "source") for row in item["data"].get("source_locators", []))
                continue
            record = index.get(value)
            if record is None:
                raise _Unavailable("adopted_local_support_unknown: " + value)
            if expected == "proof" and record["table"] != "proofs":
                raise _Unavailable("adopted_local_proof_table_mismatch")
            support(record["record"])
    return [{"ref": ref, "kind": row["kind"], "bound_ids": sorted(row["bound_ids"])}
            for ref, row in sorted(by_ref.items())]


def adopted_proof_requirements(artifacts, snapshot, approved_bound_ids):
    """Only adopted formal proofs need execution declarations; inline legacy
    proofs remain subject to full scientific review without invented CAS IDs.
    """
    return [{"proof_ref": row["ref"], "bound_ids": row["bound_ids"]}
            for row in adopted_scientific_dependencies(artifacts, snapshot, approved_bound_ids)
            if row["kind"] == "proof"]


def _require_adopted_dependencies_clear(review, snapshot, artifacts):
    """A direct unresolved mathematical defect cannot opt out with creds=[]."""
    for row in adopted_scientific_dependencies(artifacts, snapshot, review.get("approved_bound_ids", [])):
        for issue in _structured_issues(_get(artifacts, row["ref"], row["kind"])["data"]):
            if BLOCKING.intersection(issue["blocks"]):
                raise _Unavailable("adopted_dependency_has_blocking_issue: " + row["kind"] + ":" + row["ref"]
                                   + ":" + issue["issue_id"])


def _execution_adoption_errors(review, snapshot, artifacts):
    from ..tools.exact_checks import validate_execution_check
    requirements = adopted_proof_requirements(artifacts, snapshot, review.get("approved_bound_ids", []))
    declarations = {}
    rows = review.get("proof_execution_checks", [])
    if not isinstance(rows, list) or len(rows) > MAX_PROOFS:
        raise _Unavailable("proof_execution_declarations_invalid")
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"proof_ref", "execution_check"} or row["proof_ref"] in declarations:
            raise _Unavailable("proof_execution_declaration_ambiguous")
        _get(artifacts, row["proof_ref"], "proof")
        declarations[row["proof_ref"]] = row["execution_check"]
    for row in review.get("proof_approvals", []):
        if "execution_check" not in row:
            continue
        ref, check = row["proof_ref"], row["execution_check"]
        if ref in declarations and declarations[ref] != check:
            raise _Unavailable("proof_execution_declaration_conflict")
        declarations[ref] = check
    missing = {row["proof_ref"] for row in requirements} - declarations.keys()
    if missing:
        raise _Unavailable("adopted_proof_execution_declaration_missing: " + ", ".join(sorted(missing)))
    for ref, check in declarations.items():
        errors = validate_execution_check(check, ref, artifacts, subject_ref=snapshot["ref"])
        if errors:
            raise _Unavailable("proof_execution_check: " + "; ".join(errors))
    return requirements


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


def _structured_issues(*documents, with_pointers=False):
    """Scan only actual dict/list objects; do not interpret natural language or JSON embedded in strings.

    Scientific issues may appear in any structured container, including proofs/evidence/quarantined_claims.
    The full traversal shares depth, node, and serialized-byte budgets; unknown structures cannot become evidence for reuse.
    """
    pending = [(document, 0, "normal", "") for document in reversed(documents)]
    nodes = byte_count = 0
    required = {"issue_id", "kind", "scope", "subject_refs", "blocks", "message", "evidence_refs", "resolves"}
    while pending:
        value, depth, mode, pointer = pending.pop()
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
            yield (value, pointer) if with_pointers else value
        if isinstance(value, dict):
            for key, child in reversed(list(value.items())):
                path = pointer + "/" + key.replace("~", "~0").replace("/", "~1")
                if key == "issues":
                    if not isinstance(child, list):
                        raise _Unavailable("issue_list_unknown")
                    pending.append((child, depth + 1, "issue_array", path))
                else:
                    pending.append((child, depth + 1, "normal", path))
        elif isinstance(value, list):
            child_mode = "issue_row" if mode == "issue_array" else "normal"
            pending.extend((child, depth + 1, child_mode, pointer + "/" + str(index))
                           for index, child in reversed(list(enumerate(value))))


def _blocking_issues(snapshot, review, *, scoped=False, occurrences=None, lineage=None):
    issues = {}
    documents = [snapshot["profile"], snapshot["research"]["data"], review]
    if scoped:
        # Candidate-level source ambiguities also need an explicit complete
        # scope. Include their original variants, not merely the later summary.
        documents.append(snapshot["candidate"]["data"])
    records = _structured_issues(*documents) if occurrences is None else (o["issue"] for o in occurrences)
    for row in records:
        if not BLOCKING.intersection(row["blocks"]):
            continue
        iid, subjects = row["issue_id"], row["subject_refs"]
        # A stable issue may have both producer text and review notes; scope declarations must cover
        # all versions, rather than the controller inferring from free text which version has been superseded.
        previous = issues.setdefault(iid, {"issue_id": iid, "subject_refs": [], "blocks": [], "variant_signatures": [],
                                          "material_signatures": [], "evidence_refs": [], "occurrence_ids": [], "occurrence_signatures": []})
        previous["subject_refs"] = sorted(set(previous["subject_refs"]) | set(subjects))
        previous["blocks"] = sorted(set(previous["blocks"]) | set(row["blocks"]))
        previous["variant_signatures"] = sorted(set(previous["variant_signatures"]) | {issue_signature(row, snapshot, scoped=scoped, lineage=lineage)})
        previous["material_signatures"] = sorted(set(previous["material_signatures"]) | {digest(row)})
        previous["evidence_refs"] = sorted(set(previous["evidence_refs"]) | set(row["evidence_refs"]))
        if len(issues) > MAX_ISSUES:
            raise _Unavailable("issue_count_limit")
    if occurrences is not None:
        for row in occurrences:
            issues[row["issue_id"]]["occurrence_ids"].append(row["occurrence_id"])
            issues[row["issue_id"]]["occurrence_signatures"].append(occurrence_signature(row, snapshot, lineage=lineage))
        for row in issues.values():
            row["occurrence_ids"] = sorted(set(row["occurrence_ids"]))
            row["occurrence_signatures"] = sorted(set(row["occurrence_signatures"]))
    return issues


def _comparison_issues(artifacts, prior, current, review, previous_review_ref):
    """Call only after validating the prior independent review and its scopes."""
    scoped = review.get("issue_scope_version") in SEMANTIC_SCOPE_VERSIONS
    occurrence_scoped = review.get("issue_scope_version") == OCCURRENCE_SCOPE_VERSION
    lineage = verified_delivery_lineage(prior, current, previous_review_ref) if occurrence_scoped else None
    values = []
    for snapshot, document in ((prior, review), (current, {})):
        catalog = dependency_issue_catalog(artifacts, snapshot, document) if occurrence_scoped else None
        values.append(_blocking_issues(snapshot, document, scoped=scoped,
            occurrences=catalog["issue_occurrences"] if catalog else None, lineage=lineage))
    return values


def _approvals(review):
    rows = review.get("proof_approvals", [])
    if not isinstance(rows, list) or len(rows) > MAX_PROOFS:
        raise _Unavailable("proof_approval_list_invalid")
    out = {}
    for row in rows:
        expected = APPROVAL_KEYS | ({"execution_check"} if review.get("issue_scope_version") == OCCURRENCE_SCOPE_VERSION else set())
        if not isinstance(row, dict) or set(row) != expected:
            raise _Unavailable("proof_approval_shape_invalid")
        ref = row["proof_ref"]
        if not isinstance(ref, str) or references(ref) != {ref} or ref in out:
            raise _Unavailable("proof_approval_reference_ambiguous")
        if row["scope"] not in {"standalone_proposition", EXPLICIT_SCOPE} or row["assumptions_complete"] is not True:
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
        occurrence_scope = review.get("issue_scope_version") == OCCURRENCE_SCOPE_VERSION
        expected = ISSUE_SCOPE_KEYS | ({"occurrence_ids"} if occurrence_scope else set())
        if not isinstance(row, dict) or set(row) != expected:
            raise _Unavailable("proof_issue_scope_shape_invalid")
        iid = row["issue_id"]
        refs = row["affected_proof_refs"]
        if not isinstance(iid, str) or iid in scopes or iid not in issues:
            raise _Unavailable("proof_issue_scope_id_unknown_or_ambiguous")
        if not isinstance(refs, list) or any(not isinstance(r, str) for r in refs) or len(refs) != len(set(refs)) or not set(refs).issubset(proofs):
            raise _Unavailable("proof_issue_scope_reference_unknown")
        if type(row["scope_complete"]) is not bool or not isinstance(row["reason"], str) or not row["reason"].strip():
            raise _Unavailable("proof_issue_scope_not_explicit")
        if occurrence_scope:
            ids = row["occurrence_ids"]
            if (not isinstance(ids, list) or any(not isinstance(i, str) for i in ids) or len(ids) != len(set(ids))
                    or set(ids) != set(issues[iid]["occurrence_ids"])):
                raise _Unavailable("proof_issue_occurrence_scope_missing_or_changed")
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


def _fingerprint(artifacts, snapshot, ref, approval, graph, *, scoped=False, occurrence_scoped=False):
    proof = _get(artifacts, ref, "proof")["data"]
    # Legacy credentials conservatively include all parameters. The explicit
    # scope is a new independent declaration covering every necessary assumption;
    # it must not silently inherit an old wider credential.
    context = declared_context(snapshot, approval)
    if len(dumps(context).encode("utf-8")) > MAX_CONTEXT_BYTES:
        raise _Unavailable("proof_context_byte_limit")
    roots = {ref} | references(context)
    closure, byte_count = graph.closure(roots)
    # A profile-level declaration cannot remove blockers retained by source or proof objects themselves.
    if occurrence_scoped:
        # The full graph above remains a pinned audit/fingerprint. A prior
        # review's rejected proof descendants are not this proof's premises.
        dependencies = [graph.item(row["ref"])["data"] for row in mathematical_dependencies(artifacts, roots)]
    else:
        dependencies = [graph.item(row["ref"])["data"] for row in closure
                        if not (scoped and row["ref"] == snapshot["proposal"]["candidate_ref"])]
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
    occurrence_scoped = review.get("issue_scope_version") == OCCURRENCE_SCOPE_VERSION
    catalog = dependency_issue_catalog(artifacts, snapshot, review) if occurrence_scoped else None
    issues = _blocking_issues(snapshot, review, scoped=review.get("issue_scope_version") in SEMANTIC_SCOPE_VERSIONS,
                             occurrences=catalog["issue_occurrences"] if catalog else None)
    scopes = _issue_scopes(review, issues, proofs)
    graph = _Graph(artifacts)
    fingerprints = {}
    for ref, approval in approvals.items():
        if len(ids[proofs[ref]["data"]["proof_id"]]) != 1:
            raise _Unavailable("proof_id_ambiguous")
        reason = _issue_blocks(ref, proofs[ref]["data"], issues, scopes)
        if reason:
            raise _Unavailable(reason)
        if occurrence_scoped:
            from ..tools.exact_checks import validate_execution_check
            errors = validate_execution_check(approval["execution_check"], ref, artifacts, subject_ref=snapshot["ref"])
            if errors:
                raise _Unavailable("proof_execution_check: " + "; ".join(errors))
        fingerprints[ref] = _fingerprint(artifacts, snapshot, ref, approval, graph,
                                         scoped=review.get("issue_scope_version") in SEMANTIC_SCOPE_VERSIONS,
                                         occurrence_scoped=occurrence_scoped)
    return proofs, approvals, fingerprints, issues, scopes


def build_proof_review_context(artifacts, ws, current_proposal_ref, previous_review_ref=None):
    """Build a compact catalog; only explicit standalone proposition certificates can supply candidates, and automatic approval is never returned."""
    out = {"context_version": "proof-review-context", "current_proposal_ref": current_proposal_ref,
           "previous_review_ref": None, "reuse_status": "no_prior_review",
           "proof_catalog": [], "reusable_proof_refs": [], "proof_candidates": [],
           "proof_scope_revalidation_candidates": [],
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
        from ..atlas.store import _active_bounds
        out["adopted_proof_requirements"] = adopted_proof_requirements(artifacts, current, sorted(_active_bounds(current["profile"])))
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        out.update(reuse_status="current_snapshot_unavailable", validation_reason=str(exc)[:240])
        return out
    try:
        catalog = dependency_issue_catalog(artifacts, current)
        out.update(issue_scope_version=OCCURRENCE_SCOPE_VERSION, issue_catalog_status="complete",
                   issue_occurrences=catalog["issue_occurrences"], hard_dependency_blockers=catalog["hard_dependency_blockers"])
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        out.update(issue_scope_version=OCCURRENCE_SCOPE_VERSION, issue_catalog_status="unavailable",
                   issue_catalog_reason=str(exc)[:240], issue_occurrences=[], hard_dependency_blockers=[])
    if not previous_review_ref:
        return out
    try:
        review, prior, reviewer_job = _prior_review(artifacts, ws, previous_review_ref)
        if not review.get("proof_approvals"):
            out["reuse_status"] = "no_explicit_prior_proof_approval"
            return out
        prior_proofs, approvals, fingerprints, prior_issues, _ = _contract(artifacts, prior, review)
        if prior["profile"]["setting_id"] != current["profile"]["setting_id"]:
            raise _Unavailable("different_setting_id")
        # Unreviewed scientific issues from the current producer cannot be skipped because a standalone proposition was approved previously.
        occurrence_scoped = review.get("issue_scope_version") == OCCURRENCE_SCOPE_VERSION
        prior_issues, current_issues = _comparison_issues(artifacts, prior, current, review, previous_review_ref)
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        out.update(reuse_status="prior_proof_contract_unavailable", validation_reason=str(exc)[:240])
        return out
    out.update(previous_review_ref=previous_review_ref, previous_proposal_ref=prior["ref"],
               previous_prepared_ref=prior["proposal"]["prepared_ref"], previous_reviewer_job_id=reviewer_job,
               reuse_status="candidates_verified", changed_profile_fields=sorted(k for k in prior["profile"].keys() | current["profile"].keys() if prior["profile"].get(k) != current["profile"].get(k)))
    graph = _Graph(artifacts)
    out["previous_issue_scope_version"] = review.get("issue_scope_version")
    out["prior_issue_evidence"] = issue_audit(prior_issues)
    out["current_issue_evidence"] = issue_audit(current_issues)
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
                after = _fingerprint(artifacts, current, ref, approvals[ref], graph,
                                     scoped=review.get("issue_scope_version") in SEMANTIC_SCOPE_VERSIONS,
                                     occurrence_scoped=occurrence_scoped)
                if before["fingerprint"] != after["fingerprint"]:
                    reason = "proof_context_or_dependency_changed"
                else:
                    # A previous review may explain only issues it checked at the time; new or changed issues require a fresh independent impact assessment.
                    for iid, issue in current_issues.items():
                        if (iid not in prior_issues or not set(issue["variant_signatures"]).issubset(prior_issues[iid]["variant_signatures"])
                                or occurrence_scoped and not set(issue["occurrence_signatures"]).issubset(prior_issues[iid]["occurrence_signatures"])):
                            reason = "new_scientific_issue_requires_review"
                            break
                    if reason is None:
                        out["reusable_proof_refs"].append(ref)
                        out["proof_candidates"].append({"proof_ref": ref, "proof_id": item["data"]["proof_id"], "scope": approvals[ref]["scope"],
                             "previous_review_ref": previous_review_ref, "previous_proposal_ref": prior["ref"],
                             **{k: after[k] for k in ("fingerprint", "context_digest", "context_pointers", "dependency_count", "dependency_bytes")},
                             "reason": "Explicit standalone proposition approval with an independently completed validated_handoff; the proof, fully declared context, and pinned dependencies are unchanged; the current application requires fresh review."})
            except (ProtocolError, KeyError, TypeError, ValueError) as exc:
                reason = "proof_dependency_unavailable: " + str(exc)[:180]
        if reason in {"proof_context_or_dependency_changed", "new_scientific_issue_requires_review"} and occurrence_scoped:
            try:
                candidate = revalidation_candidate(artifacts, prior, current, previous_review_ref, ref,
                    approvals[ref], prior_issues, current_issues, out.get("issue_occurrences", []))
                if candidate:
                    out["proof_scope_revalidation_candidates"].append(candidate)
            except (ProtocolError, KeyError, TypeError, ValueError):
                pass  # Ordinary full independent review remains available.
        if reason:
            out["invalidated_proofs"].append({"proof_ref": ref, "reason": reason})
    out["invalidation_counts"] = dict(Counter(row["reason"].split(":", 1)[0] for row in out["invalidated_proofs"]))
    return out


def _scope_revalidation_errors(review, inputs, artifacts, snapshot, approvals, resolve=None):
    rows = review.get("proof_scope_revalidations", [])
    if not rows:
        return []
    try:
        if not isinstance(rows, list) or len(rows) > MAX_PROOFS:
            raise _Unavailable("scope_revalidation_list_invalid")
        refs = set()
        for row in rows:
            if (not isinstance(row, dict) or set(row) != {"proof_ref", "candidate_id", "changes_reviewed", "reason"}
                    or row["changes_reviewed"] is not True or not isinstance(row["reason"], str) or not row["reason"].strip()
                    or row["proof_ref"] in refs or row["proof_ref"] not in approvals):
                raise _Unavailable("scope_revalidation_requires_explicit_current_approval")
            refs.add(row["proof_ref"])
        if refs.intersection(review.get("reused_proof_refs", [])):
            raise _Unavailable("scope_revalidation_is_not_unchanged_context_reuse")
        context_ref = inputs.get("proof_context_ref")
        if not context_ref or review.get("proof_reuse_context_ref") != context_ref:
            raise _Unavailable("scope_revalidation_context_binding_missing")
        item = (resolve or artifacts.get)(context_ref)
        context = item["data"]
        if (item["kind"] != "external_result" or context.get("current_proposal_ref") != snapshot["ref"]
                or context.get("current_bundle_hash") != snapshot["prepared"]["bundle_hash"]):
            raise _Unavailable("scope_revalidation_context_binding_mismatch")
        ws = getattr(artifacts, "workspace", None)
        if ws is None or not context.get("previous_review_ref"):
            raise _Unavailable("scope_revalidation_prior_review_missing")
        verified = build_proof_review_context(artifacts, ws, snapshot["ref"], context["previous_review_ref"])
        candidates = verified["proof_scope_revalidation_candidates"]
        if context.get("proof_scope_revalidation_candidates") != candidates:
            raise _Unavailable("scope_revalidation_catalog_not_controller_verifiable")
        by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
        for row in rows:
            candidate = by_id.get(row["candidate_id"])
            if not candidate or candidate["proof_ref"] != row["proof_ref"]:
                raise _Unavailable("scope_revalidation_not_current_candidate")
            # A newly signed narrower scope must still preserve the immutable
            # mathematical material. Current _contract already validates its
            # complete declarations, all issues and execution applicability.
            now = scientific_material(artifacts, snapshot, row["proof_ref"], approvals[row["proof_ref"]])
            if now["fingerprint"] != candidate["scientific_material_fingerprint"]:
                raise _Unavailable("scope_revalidation_scientific_dependencies_changed")
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        return [{"code": "proof_scope_revalidation", "path": "/proof_scope_revalidations", "message": str(exc)}]
    return []


def _require_revalidation_adoption_scope(review, inputs, artifacts, snapshot, resolve=None):
    """Declining credentials cannot skip newly exposed adoption issues.

    This extra obligation applies only to a real controller catalog with a
    verified scope-revalidation candidate. It does not force a reusable proof
    credential or alter an older full-review job without such candidates.
    """
    context_ref = inputs.get("proof_context_ref")
    if not context_ref:
        return
    item = (resolve or artifacts.get)(context_ref)
    context = item["data"]
    if not context.get("previous_review_ref"):
        return
    if (item["kind"] != "external_result" or context.get("current_proposal_ref") != snapshot["ref"]
            or context.get("current_bundle_hash") != snapshot["prepared"]["bundle_hash"]):
        raise _Unavailable("scope_revalidation_context_binding_mismatch")
    ws = getattr(artifacts, "workspace", None)
    if ws is None:
        raise _Unavailable("scope_revalidation_prior_review_missing")
    verified = build_proof_review_context(artifacts, ws, snapshot["ref"], context["previous_review_ref"])
    candidates = verified["proof_scope_revalidation_candidates"]
    if not candidates:
        return
    if context.get("proof_scope_revalidation_candidates") != candidates:
        raise _Unavailable("scope_revalidation_catalog_not_controller_verifiable")
    adopted = adopted_proof_requirements(artifacts, snapshot, review.get("approved_bound_ids", []))
    if not adopted:
        return
    if review.get("issue_scope_version") != OCCURRENCE_SCOPE_VERSION:
        raise _Unavailable("scope_revalidation_adoption_requires_occurrence_scope")
    catalog = dependency_issue_catalog(artifacts, snapshot, review)
    issues = _blocking_issues(snapshot, review, scoped=True, occurrences=catalog["issue_occurrences"])
    proofs, _ = _proofs(artifacts, snapshot)
    proofs.update({row["proof_ref"]: _get(artifacts, row["proof_ref"], "proof") for row in adopted})
    scopes = _issue_scopes(review, issues, proofs)
    for row in adopted:
        ref = row["proof_ref"]
        error = _issue_blocks(ref, proofs[ref]["data"], issues, scopes)
        if error:
            raise _Unavailable("scope_revalidation_adoption_" + error)


def proof_approval_errors(review, inputs, artifacts, *, resolve=None):
    """Recheck before freezing the review and at engine handoff; older uncertified records remain readable but cannot be reused through this mechanism."""
    enabled = bool(inputs.get("proof_context_ref"))
    current_contract = inputs.get("issue_scope_contract_version") == OCCURRENCE_SCOPE_VERSION
    fields = {"proof_approvals", "proof_issue_scopes", "proof_reuse_context_ref", "reused_proof_refs"}
    if not enabled and not current_contract and not (fields | {"proof_execution_checks", "proof_scope_revalidations"}).intersection(review):
        return []
    errors = []

    def add(code, path, message):
        errors.append({"code": code, "path": path, "message": message})

    if enabled and not fields.issubset(review):
        add("proof_contract_missing", "/", "This task must explicitly submit proof approvals, issue scopes, and reuse fields; even empty lists must be recorded explicitly.")
    if review.get("review_type") != "profile" or review.get("subject_ref") != inputs.get("subject_ref"):
        add("proof_review_subject", "/subject_ref", "A proof certificate must bind the pinned proposal under the current profile review.")
        return errors
    if current_contract and review.get("issue_scope_version") != OCCURRENCE_SCOPE_VERSION:
        add("proof_issue_scope_version", "/issue_scope_version", "This task requires occurrence-bound occurrence-bound-scope credentials and explicit executable-check applicability.")
        return errors
    try:
        snapshot = _snapshot(artifacts, review["subject_ref"])
        if current_contract or review.get("issue_scope_version") == OCCURRENCE_SCOPE_VERSION:
            _require_adopted_dependencies_clear(review, snapshot, artifacts)
            _execution_adoption_errors(review, snapshot, artifacts)
        _require_revalidation_adoption_scope(review, inputs, artifacts, snapshot, resolve)
        # Proof reuse is an optional optimization. Unknown legacy free-form objects may receive full review in the current independent review,
        # but they must explicitly declare that no proof certificates are issued and no proofs are reused; a scan failure must not block ordinary scientific review.
        if review.get("proof_approvals", []) == [] and review.get("reused_proof_refs", []) == []:
            context_ref = review.get("proof_reuse_context_ref")
            if context_ref is not None and context_ref != inputs.get("proof_context_ref"):
                add("proof_reuse_context", "/proof_reuse_context_ref", "Without reuse, retain only this job catalog or null; do not rebind to another context.")
            errors.extend(_scope_revalidation_errors(review, inputs, artifacts, snapshot, {}, resolve))
            return errors
        proofs, approvals, _, _, _ = _contract(artifacts, snapshot, review)
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        add("proof_approval_contract", "/proof_approvals", str(exc))
        if review.get("issue_scope_version") == OCCURRENCE_SCOPE_VERSION:
            try:
                current_snapshot = _snapshot(artifacts, review["subject_ref"])
                errors[-1]["scope_diagnostic"] = scope_diagnostic(artifacts, current_snapshot, review)
                errors[-1]["adopted_proof_requirements"] = adopted_proof_requirements(artifacts, current_snapshot, review.get("approved_bound_ids", []))
            except (ProtocolError, KeyError, TypeError, ValueError):
                pass
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
                if item["kind"] != "external_result" or context.get("context_version") != "proof-review-context" or context.get("current_proposal_ref") != review["subject_ref"] or context.get("current_bundle_hash") != snapshot["prepared"]["bundle_hash"]:
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
                if any(sorted(approvals[ref]["context_pointers"]) != candidates[ref]["context_pointers"]
                       or approvals[ref]["scope"] != candidates[ref]["scope"] for ref in reused):
                    raise _Unavailable("reused_proof_context_declaration_changed")
            except (ProtocolError, KeyError, TypeError, ValueError) as exc:
                add("proof_reuse_context", "/proof_reuse_context_ref", str(exc))
    errors.extend(_scope_revalidation_errors(review, inputs, artifacts, snapshot, approvals, resolve))
    return errors
