"""Provide conservative, verifiable differences and per-bound reuse candidates for independent re-review; never approve automatically.

Mathematical judgment remains with the reviewer. This module verifies only pinned records, actual roles and handoffs, hashes, and
explicit dependencies. Missing data, ambiguity, or exceeding the bounded closure requires full review.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Any

from ..atlas.store import _ineligible
from ..atlas.tags import effective_specification, json_bytes
from ..core.contracts import ProtocolError, check_review, references, resolve_pointer, validate
from ..core.store import digest, dumps
from .issue_semantics import (ISSUE_SCOPE_VERSION, OCCURRENCE_SCOPE_VERSION, SEMANTIC_SCOPE_VERSIONS,
                              CONTEXTUAL_KINDS, dependency_issue_catalog, issue_audit)
from .issue_semantics import scope_diagnostic


MAX_DEPENDENCIES = 256
MAX_DEPENDENCY_BYTES = 4_000_000
MAX_DEPENDENCY_DEPTH = 32
MAX_PROFILE_BYTES = 4_000_000
MAX_BOUNDS = 400
MAX_LOCAL_RECORDS = 800
MAX_ISSUES = 100
FILES = {"profile.json", "identity.json", "classification.json", "human_tags.json", "machine_tags.json"}
RECORD_TABLES = ("proofs", "evidence", "references")
NON_ENVIRONMENT = {"bounds", "comparisons", "bracket_rows", "summary_status", "reader_markdown", "provenance", "title", "issues", *RECORD_TABLES}
ALWAYS_REVIEW = ["current_identity_and_scope", "comparisons", "bracket_rows", "summary_status", "joint_analysis", "refinement_pending", "reader_markdown", "prepared_sidecars", "current_and_resolved_issues", "research_issues", "coverage_and_new_safety_evidence"]


class _Unavailable(ValueError):
    pass


def _get(artifacts, ref: str, kind: str | None = None) -> dict:
    item = artifacts.get(ref)
    if kind is not None and item["kind"] != kind:
        raise _Unavailable(f"expected_{kind}_artifact")
    if "sha256:" + digest({"kind": item["kind"], "data": item["data"]}) != ref:
        raise _Unavailable("artifact_content_hash_mismatch")
    return item


def _snapshot(artifacts, ref: str) -> dict:
    proposal = _get(artifacts, ref, "proposal")["data"]
    validate("proposal", proposal)
    prepared = _get(artifacts, proposal["prepared_ref"], "prepared")["data"]
    profile = _get(artifacts, proposal["profile_ref"], "profile")["data"]
    if len(dumps(profile).encode("utf-8")) > MAX_PROFILE_BYTES:
        raise _Unavailable("profile_dependency_byte_limit")
    research = _get(artifacts, proposal["research_ref"], "research")
    raw_profile = _get(artifacts, research["data"]["profile_ref"], "profile")["data"]
    candidate = _get(artifacts, proposal["candidate_ref"], "candidate")
    identity = _get(artifacts, proposal["identity_ref"], "identity")["data"]
    files = prepared.get("files")
    if not isinstance(files, dict) or set(files) != FILES or any(not isinstance(v, dict) for v in files.values()):
        raise _Unavailable("prepared_five_files_missing")
    if files["profile.json"] != profile or prepared.get("setting_id") != profile.get("setting_id"):
        raise _Unavailable("prepared_profile_binding_mismatch")
    if not isinstance(profile.get("setting_id"), str) or not profile["setting_id"]:
        raise _Unavailable("setting_id_missing")
    hashes = {name: hashlib.sha256(json_bytes(value)).hexdigest() for name, value in files.items()}
    if prepared.get("bundle_hash") != digest(files) or prepared.get("hashes") != hashes:
        raise _Unavailable("prepared_hash_mismatch")
    if prepared.get("version") != "target-" + digest(hashes):
        raise _Unavailable("prepared_version_mismatch")
    if research["data"].get("candidate_ref") != proposal.get("candidate_ref") or research["data"].get("identity_ref") != proposal.get("identity_ref"):
        raise _Unavailable("proposal_research_identity_binding_mismatch")
    if identity.get("candidate_ref") != proposal["candidate_ref"] or research["data"].get("setting_id") != profile["setting_id"]:
        raise _Unavailable("proposal_setting_or_candidate_mismatch")
    if raw_profile.get("setting_id") != profile["setting_id"]:
        raise _Unavailable("research_profile_setting_mismatch")
    if research["data"].get("action") != proposal["mode"] or research["data"].get("base_version") != proposal["base_version"]:
        raise _Unavailable("proposal_research_mode_or_baseline_mismatch")
    return {"ref": ref, "proposal": proposal, "prepared": prepared, "profile": profile, "research": research, "candidate": candidate}


def _bound_map(profile: dict) -> tuple[dict, list[str]]:
    values = profile.get("bounds")
    if not isinstance(values, list) or len(values) > MAX_BOUNDS:
        raise _Unavailable("bounds_missing_or_limit")
    result, invalid = {}, []
    for row in values:
        if not isinstance(row, dict):
            invalid.append("non_object_bound")
            continue
        ids = [row[k] for k in ("id", "bound_id") if k in row]
        if not ids or any(not isinstance(v, str) or not v for v in ids) or len(set(ids)) != 1:
            invalid.append("missing_or_conflicting_bound_id")
            continue
        key = ids[0]
        if key in result:
            invalid.append(key)
        else:
            result[key] = row
    for key in invalid:
        result.pop(key, None)
    return result, invalid


def _strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _strings(child)


def _records(profile: dict) -> tuple[dict, list]:
    """Registered IDs track native records only; mathematical dependencies or equivalences are not inferred from text."""
    index, unnamed, total = {}, [], 0
    for table in RECORD_TABLES:
        rows = profile.get(table, [])
        if not isinstance(rows, list):
            raise _Unavailable("local_dependency_table_invalid")
        for row in rows:
            total += 1
            if total > MAX_LOCAL_RECORDS:
                raise _Unavailable("local_dependency_record_limit")
            if not isinstance(row, dict):
                unnamed.append({"table": table, "record": row})
                continue
            ids = {row[k] for k in ("id", "proof_id", "evidence_id", "reference_id", "ref_id") if isinstance(row.get(k), str) and row[k]}
            if len(ids) > 1:
                raise _Unavailable("ambiguous_local_record_aliases")
            if not ids:
                # A native free-form object has no verifiable ID, so its irrelevance to a bound cannot be established.
                unnamed.append({"table": table, "record": row})
                continue
            rid = next(iter(ids))
            if rid in index:
                raise _Unavailable("duplicate_local_dependency_id")
            index[rid] = {"table": table, "record": row}
    return index, unnamed


class _Graph:
    def __init__(self, artifacts):
        self.artifacts = artifacts
        self.cache = {}

    def item(self, ref):
        if ref not in self.cache:
            self.cache[ref] = _get(self.artifacts, ref)
        return self.cache[ref]

    def closure(self, roots: set[str]) -> tuple[list[dict], int]:
        seen, visiting, total_bytes = {}, set(), 0

        def walk(ref, depth):
            nonlocal total_bytes
            if ref in visiting:
                raise _Unavailable("dependency_cycle")
            if ref in seen:
                return
            if depth > MAX_DEPENDENCY_DEPTH or len(seen) + len(visiting) >= MAX_DEPENDENCIES:
                raise _Unavailable("dependency_count_or_depth_limit")
            item = self.item(ref)
            total_bytes += len(dumps({"kind": item["kind"], "data": item["data"]}).encode("utf-8"))
            if total_bytes > MAX_DEPENDENCY_BYTES:
                raise _Unavailable("dependency_byte_limit")
            visiting.add(ref)
            deps = set(item.get("dependencies", [])) | references(item["data"])
            if any(not isinstance(dep, str) for dep in deps):
                raise _Unavailable("dependency_reference_invalid")
            for dep in sorted(deps):
                walk(dep, depth + 1)
            # Mixing version names with content versions cannot establish reuse eligibility, even if another validation mistakenly accepted it.
            if item["kind"] == "result":
                for loc in item["data"].get("source_locators", []):
                    source = self.item(loc["source_ref"])
                    if source["kind"] != "source" or loc["version"] != source["data"].get("version"):
                        raise _Unavailable("result_source_version_mismatch")
            visiting.remove(ref)
            seen[ref] = {"ref": ref, "kind": item["kind"]}

        for ref in sorted(roots):
            walk(ref, 0)
        return [seen[ref] for ref in sorted(seen)], total_bytes


def _fingerprint(snapshot: dict, bound: dict, graph: _Graph, approval: dict | None = None) -> dict:
    profile = snapshot["profile"]
    key = bound.get("comparison_key", {})
    vids = [bound[k] for k in ("view_id", "view_ref") if bound.get(k) is not None]
    if isinstance(key, dict) and key.get("view_id") is not None:
        vids.append(key["view_id"])
    if not vids or any(not isinstance(v, str) for v in vids) or len(set(vids)) != 1:
        raise _Unavailable("bound_view_missing_or_ambiguous")
    vid = vids[0]
    views = [v for v in profile.get("views", []) if isinstance(v, dict) and v.get("view_id") == vid]
    if len(views) != 1:
        raise _Unavailable("bound_view_not_unique")
    if isinstance(key, dict) and key.get("setting_id", profile["setting_id"]) != profile["setting_id"]:
        raise _Unavailable("bound_setting_mismatch")
    effective, _ = effective_specification(profile, vid)
    if approval is None:
        env = {k: v for k, v in profile.items() if k not in NON_ENVIRONMENT}
    else:
        # A completed independent certificate declares the full applicability
        # context. Native contracts, global parameters and the effective view
        # are mandatory, even if the declared pointers would omit them.
        env = {"setting_id": profile["setting_id"], "common_specification": profile["common_specification"],
               "parameters": profile.get("parameters"),
               "declared_context": {p: resolve_pointer(profile, p) for p in approval["context_pointers"]}}
    env["prepared_semantics_version"] = snapshot["prepared"].get("semantics_version")
    if len(dumps(env).encode("utf-8")) > MAX_PROFILE_BYTES:
        raise _Unavailable("bound_context_byte_limit")
    index, unnamed = _records(profile)
    env["unindexed_scientific_records"] = unnamed
    selected, pending = {}, [bound, env, effective]
    # Include registered IDs appearing in free text, preferring excess inclusion to missing dependencies in older native layouts.
    # Candidate reuse is explicitly rejected below for unregistered external literature without a pinned sha.
    while pending:
        value = pending.pop()
        texts = list(_strings(value))
        for rid, record in index.items():
            if rid not in selected and any(rid in text for text in texts):
                selected[rid] = record
                pending.append(record)
    support = {"bound": bound, "records": {k: selected[k] for k in sorted(selected)}}
    roots = references({"environment": env, "effective_view": effective, "support": support})
    if not references(support):
        raise _Unavailable("bound_has_no_fixed_support_reference")
    closure, byte_count = graph.closure(roots)
    return {"fingerprint": digest({"environment": env, "effective_view": effective, "support": support, "closure": closure}),
            "dependency_count": len(closure), "dependency_bytes": byte_count,
            "support_refs": sorted(references(support)), "local_record_ids": sorted(selected),
            "dependency_refs": [row["ref"] for row in closure],
            "context_refs": sorted(references({"environment": env, "effective_view": effective}))}


def _bound_contract(artifacts, snapshot, review):
    """Validate explicit per-bound credentials; legacy reviews use the old path."""
    # Local import avoids a module cycle while keeping the bounded recursive
    # issue scan shared with standalone proof certificates.
    from .proof_reuse import _blocking_issues
    if review.get("issue_scope_version") not in SEMANTIC_SCOPE_VERSIONS:
        raise _Unavailable("bound_issue_scope_version_missing")
    occurrence_scoped = review.get("issue_scope_version") == OCCURRENCE_SCOPE_VERSION
    bounds, invalid = _bound_map(snapshot["profile"])
    if invalid:
        raise _Unavailable("ambiguous_profile_bound_ids")
    rows = review.get("bound_approvals", [])
    if not isinstance(rows, list) or len(rows) > MAX_BOUNDS:
        raise _Unavailable("bound_approval_list_invalid")
    approvals = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"bound_id", "scope", "assumptions_complete", "context_pointers", "reason"}:
            raise _Unavailable("bound_approval_shape_invalid")
        bid, pointers = row["bound_id"], row["context_pointers"]
        if not isinstance(bid, str) or bid in approvals or bid not in bounds or bid not in review.get("approved_bound_ids", []):
            raise _Unavailable("bound_approval_not_in_adoption_scope")
        if row["scope"] != "bound_applicability" or row["assumptions_complete"] is not True or not isinstance(row["reason"], str) or not row["reason"].strip():
            raise _Unavailable("bound_approval_not_complete_scope")
        if (not isinstance(pointers, list) or not pointers or len(pointers) > 64
                or any(not isinstance(p, str) for p in pointers) or len(set(pointers)) != len(pointers)
                or "/common_specification" not in pointers):
            raise _Unavailable("bound_context_pointer_missing_or_ambiguous")
        if _ineligible(bounds[bid]):
            raise _Unavailable("bound_explicitly_ineligible")
        approvals[bid] = row
    catalog = dependency_issue_catalog(artifacts, snapshot, review) if occurrence_scoped else None
    issues = _blocking_issues(snapshot, review, scoped=True,
                             occurrences=catalog["issue_occurrences"] if catalog else None)
    rows = review.get("bound_issue_scopes", [])
    if not isinstance(rows, list) or len(rows) > 200:
        raise _Unavailable("bound_issue_scope_list_invalid")
    scopes = {}
    for row in rows:
        expected = {"issue_id", "affected_bound_ids", "scope_complete", "reason"} | ({"occurrence_ids"} if occurrence_scoped else set())
        if not isinstance(row, dict) or set(row) != expected:
            raise _Unavailable("bound_issue_scope_shape_invalid")
        iid, affected = row["issue_id"], row["affected_bound_ids"]
        if not isinstance(iid, str) or iid not in issues or iid in scopes:
            raise _Unavailable("bound_issue_scope_id_unknown_or_ambiguous")
        if (not isinstance(affected, list) or any(not isinstance(b, str) for b in affected)
                or len(set(affected)) != len(affected) or not set(affected).issubset(bounds)):
            raise _Unavailable("bound_issue_scope_reference_unknown")
        if type(row["scope_complete"]) is not bool or not isinstance(row["reason"], str) or not row["reason"].strip():
            raise _Unavailable("bound_issue_scope_not_explicit")
        if occurrence_scoped:
            ids = row["occurrence_ids"]
            if (not isinstance(ids, list) or any(not isinstance(i, str) for i in ids) or len(ids) != len(set(ids))
                    or set(ids) != set(issues[iid]["occurrence_ids"])):
                raise _Unavailable("bound_issue_occurrence_scope_missing_or_changed")
        scopes[iid] = row
    if set(scopes) != set(issues):
        raise _Unavailable("bound_issue_scope_missing")
    graph = _Graph(artifacts)
    fingerprints = {}
    for bid, approval in approvals.items():
        fp = _fingerprint(snapshot, bounds[bid], graph, approval)
        # A source/candidate address names a shared document, not necessarily
        # this bound. The independent issue scope decides that relation. A
        # blocker naming this bound, a local dependency ID, or its actual
        # proof/result artifact cannot be declared unrelated.
        if occurrence_scoped:
            from .proof_reuse import adopted_scientific_dependencies
            from .scope_revalidation import mathematical_dependencies
            actual = adopted_scientific_dependencies(artifacts, snapshot, [bid], active_only=False)
            actual.extend(mathematical_dependencies(artifacts, fp["context_refs"]))
            mathematical_refs = {row["ref"] for row in actual}
        else:
            mathematical_refs = set(fp["dependency_refs"])
        support = {bid} | set(fp["local_record_ids"]) | {ref for ref in mathematical_refs
                   if graph.item(ref)["kind"] in {"proof", "result"}}
        for iid, issue in issues.items():
            if support.intersection(issue["subject_refs"]):
                raise _Unavailable("direct_bound_blocker")
            if not scopes[iid]["scope_complete"]:
                raise _Unavailable("bound_issue_scope_incomplete")
            if bid in scopes[iid]["affected_bound_ids"]:
                raise _Unavailable("scoped_bound_blocker")
        # A high-level scope declaration never erases a blocker retained by an
        # immutable proof/result/source in the bound's own dependency closure.
        from .proof_reuse import BLOCKING, _structured_issues
        dependency_data = [graph.item(ref)["data"] for ref in mathematical_refs
                           if ref != snapshot["proposal"]["candidate_ref"]
                           and not (occurrence_scoped and graph.item(ref)["kind"] in CONTEXTUAL_KINDS)]
        # The exact current candidate's issue variants are already included in
        # the mandatory independent scopes above; all other immutable object
        # blockers (especially proof/result/source) remain fail-closed.
        for issue in _structured_issues(*dependency_data):
            if BLOCKING.intersection(issue["blocks"]):
                raise _Unavailable("bound_dependency_has_blocking_issue")
        fingerprints[bid] = fp
    return approvals, issues, scopes, fingerprints


def _bound_issue_applies(issue: Any, bid: str, footprint: dict, known_bounds: set[str]) -> bool:
    """Assess impact only from registered IDs/pinned dependencies; conservatively invalidate any bound scope that cannot be explicitly excluded."""
    if not isinstance(issue, dict):
        return True
    if "bound" not in issue.get("blocks", []):
        return False
    support = set(footprint["dependency_refs"]) | set(footprint["local_record_ids"]) | {bid}
    subjects = issue.get("subject_refs", [])
    if not isinstance(subjects, list) or not subjects or any(not isinstance(ref, str) for ref in subjects):
        return True
    if support.intersection(subjects):
        return True
    return not set(subjects).issubset(known_bounds - {bid})


def _scientific_issues(snapshot: dict) -> list:
    """Both profile and research are formal scientific artifacts for this run; issues in research must not be overlooked."""
    issues = []
    for data in (snapshot["profile"], snapshot["research"]["data"]):
        values = data.get("issues", [])
        if not isinstance(values, list):
            return [None]  # Invalid/unknown scopes do not provide reuse candidates.
        issues.extend(values)
    return issues


def _new_bound_issue(prior: dict, current: dict, bid: str, footprint: dict) -> bool:
    """Merge new issues from both formal artifacts; the current review still explicitly rechecks old issues whose values are unchanged."""
    previous = {dumps(row) for row in _scientific_issues(prior) if isinstance(row, dict)}
    known_bounds, _ = _bound_map(current["profile"])
    for issue in _scientific_issues(current):
        if isinstance(issue, dict) and dumps(issue) in previous:
            continue
        if _bound_issue_applies(issue, bid, footprint, set(known_bounds)):
            return True
    return False


def _prior_review(artifacts, ws, ref: str) -> tuple[dict, dict, str]:
    item = _get(artifacts, ref, "review")
    review = item["data"]
    prior = _snapshot(artifacts, review["subject_ref"])
    check_review(review, prior["ref"], "profile")
    if review.get("prepared_hash") is not None and review["prepared_hash"] != prior["prepared"]["bundle_hash"]:
        raise _Unavailable("review_prepared_hash_mismatch")
    producer = item.get("producer")
    job = ws.job(producer)
    output = job.get("output") or {}
    if job["role"] != "profile_reviewer" or job["status"] != "complete" or output.get("status") != "complete" or ref not in output.get("artifact_refs", []):
        raise _Unavailable("prior_review_not_completed_independent_reviewer")
    if job.get("inputs", {}).get("subject_ref") != prior["ref"]:
        raise _Unavailable("review_job_subject_mismatch")
    if artifacts.owned(prior["ref"], producer) or prior["research"].get("producer") == producer:
        raise _Unavailable("review_not_independent_of_producer")
    handoffs = ws.query("SELECT payload FROM events WHERE job=? AND event='validated_handoff'", (producer,))
    if not any((payload := json.loads(row["payload"])).get("status") == "complete" and ref in payload.get("refs", []) for row in handoffs):
        raise _Unavailable("prior_review_handoff_not_validated")
    if review["verdict"] not in {"approve", "revise"}:
        raise _Unavailable("prior_review_has_no_reusable_adoption_scope")
    bounds, invalid = _bound_map(prior["profile"])
    if invalid or not set(review["approved_bound_ids"]).issubset(bounds) or any(_ineligible(bounds[bid]) for bid in review["approved_bound_ids"]):
        raise _Unavailable("prior_approved_bound_scope_invalid")
    return review, prior, producer


def build_review_context(artifacts, ws, current_proposal_ref: str, previous_review_ref: str | None = None) -> dict:
    """Return a compact catalog that can be paginated and stored as external_result; every candidate still requires explicit approval in a new review.

    Conservatively include global specifications and all structural definitions in the environment hash. Include proof/evidence/reference records with IDs through
    registered IDs and the pinned-ref closure; include records without IDs globally. Literature search and mathematical reductions are never treated
    as Python rules. Failure only revokes reuse candidates and does not relax the final publication boundary.
    """
    out = {"context_version": "bound-review-context", "current_proposal_ref": current_proposal_ref,
           "previous_review_ref": None, "reuse_status": "no_prior_review",
           "reusable_bound_ids": [], "reuse_candidates": [], "invalidated_bounds": [],
           "added_bound_ids": [], "changed_bound_ids": [], "unchanged_bound_ids": [], "removed_bound_ids": [],
           "changed_profile_fields": [], "previous_issues_ledger": [], "always_review": ALWAYS_REVIEW[:],
           "limits": {"artifacts_per_bound": MAX_DEPENDENCIES, "bytes_per_bound": MAX_DEPENDENCY_BYTES, "depth": MAX_DEPENDENCY_DEPTH, "profile_bytes": MAX_PROFILE_BYTES},
           "notice": "Provide only per-bound reuse candidates with verified unchanged dependencies. This is not approval of the current proposal; new counterexamples, source issues, or applicability issues may always block it. The final independent review must still explicitly approve every current active bound and all five files."}
    try:
        current = _snapshot(artifacts, current_proposal_ref)
        current_bounds, current_invalid = _bound_map(current["profile"])
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        out.update(reuse_status="current_snapshot_unavailable", validation_reason=type(exc).__name__ + ": " + str(exc)[:240])
        return out
    out["current_prepared_ref"] = current["proposal"]["prepared_ref"]
    out["current_bundle_hash"] = current["prepared"]["bundle_hash"]
    out["added_bound_ids"] = sorted(current_bounds)
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
        previous_bounds, previous_invalid = _bound_map(prior["profile"])
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        # Do not return rejected foreign/non-review references unchanged in the package, to prevent the catalog from becoming an authorization bypass.
        out.update(reuse_status="prior_review_unavailable", validation_reason=type(exc).__name__ + ": " + str(exc)[:240])
        return out
    out.update(previous_review_ref=previous_review_ref, previous_proposal_ref=prior["ref"],
               previous_prepared_ref=prior["proposal"]["prepared_ref"], previous_reviewer_job_id=reviewer_job,
               reuse_status="candidates_verified")
    oldp, newp = prior["profile"], current["profile"]
    out["changed_profile_fields"] = sorted(k for k in oldp.keys() | newp.keys() if oldp.get(k) != newp.get(k))
    out["added_bound_ids"] = sorted(current_bounds.keys() - previous_bounds.keys())
    out["removed_bound_ids"] = sorted(previous_bounds.keys() - current_bounds.keys())
    common = current_bounds.keys() & previous_bounds.keys()
    out["unchanged_bound_ids"] = sorted(k for k in common if current_bounds[k] == previous_bounds[k])
    out["changed_bound_ids"] = sorted(common - set(out["unchanged_bound_ids"]))
    issues = review.get("issues", [])
    out["previous_issues_count"] = len(issues)
    out["previous_issues_ledger"] = [{"issue_id": i["issue_id"], "kind": i["kind"], "scope": i["scope"][:300],
         "blocks": i["blocks"], "subject_refs": i["subject_refs"][:20], "evidence_refs": i["evidence_refs"][:8],
         "resolves": i["resolves"], "message_excerpt": i["message"][:220], "review_ref": previous_review_ref}
        for i in issues[:MAX_ISSUES]]
    out["previous_issues_truncated"] = len(issues) > MAX_ISSUES
    approved = set(review.get("approved_bound_ids", []))
    scoped_approvals, prior_scoped_issues, scoped_fingerprints = {}, {}, {}
    scope_error = None
    if review.get("bound_approvals"):
        try:
            scoped_approvals, prior_scoped_issues, _, scoped_fingerprints = _bound_contract(artifacts, prior, review)
            from .proof_reuse import _comparison_issues
            occurrence_scoped = review.get("issue_scope_version") == OCCURRENCE_SCOPE_VERSION
            prior_scoped_issues, current_scoped_issues = _comparison_issues(
                artifacts, prior, current, review, previous_review_ref)
            out.update(previous_issue_scope_version=review.get("issue_scope_version"),
                       prior_issue_evidence=issue_audit(prior_scoped_issues),
                       current_issue_evidence=issue_audit(current_scoped_issues))
        except (ProtocolError, KeyError, TypeError, ValueError) as exc:
            scope_error = "prior_bound_contract_unavailable: " + str(exc)[:180]
    graph = _Graph(artifacts)
    for bid in sorted(current_bounds):
        reason = None
        if oldp.get("setting_id") != newp.get("setting_id"):
            reason = "different_setting_id"
        elif current_invalid or previous_invalid:
            reason = "ambiguous_profile_bound_ids"
        elif bid not in previous_bounds:
            reason = "new_bound_id"
        elif bid not in approved:
            reason = "not_previously_approved_bound"
        elif _ineligible(current_bounds[bid]):
            reason = "bound_explicitly_ineligible"
        elif current_bounds[bid] != previous_bounds[bid]:
            reason = "bound_record_changed"
        if reason is None:
            try:
                if scope_error:
                    raise _Unavailable(scope_error)
                approval = scoped_approvals.get(bid)
                before = scoped_fingerprints[bid] if approval else _fingerprint(prior, previous_bounds[bid], graph)
                after = _fingerprint(current, current_bounds[bid], graph, approval)
                if approval and any(iid not in prior_scoped_issues or
                                    not set(issue["variant_signatures"]).issubset(prior_scoped_issues[iid]["variant_signatures"]) or
                                    occurrence_scoped and not set(issue["occurrence_signatures"]).issubset(prior_scoped_issues[iid]["occurrence_signatures"])
                                    for iid, issue in current_scoped_issues.items()):
                    reason = "new_bound_blocker_or_unresolved_scope"
                elif not approval and any(_bound_issue_applies(issue, bid, before, set(previous_bounds)) for issue in issues):
                    reason = "prior_bound_blocker"
                elif before["fingerprint"] != after["fingerprint"]:
                    reason = "scientific_environment_or_dependency_changed"
                elif not approval and _new_bound_issue(prior, current, bid, after):
                    reason = "new_bound_blocker_or_unresolved_scope"
                else:
                    out["reusable_bound_ids"].append(bid)
                    out["reuse_candidates"].append({"bound_id": bid, "fingerprint": after["fingerprint"],
                        "previous_review_ref": previous_review_ref, "previous_proposal_ref": prior["ref"],
                        "dependency_count": after["dependency_count"], "dependency_bytes": after["dependency_bytes"],
                        "support_refs": after["support_refs"][:12], "support_reference_count": len(after["support_refs"]),
                        "scope": "bound_applicability" if approval else "legacy_full_environment",
                        "context_pointers": sorted(approval["context_pointers"]) if approval else [],
                        "reason": "Independent per-bound approval with a validated handoff; the bound, scientific environment, and pinned explicit dependency closure are unchanged value by value. The current reviewer still reviews new impacts and decides on adoption."})
            except (ProtocolError, KeyError, TypeError, ValueError) as exc:
                reason = "dependency_unavailable: " + type(exc).__name__ + ": " + str(exc)[:180]
        if reason is not None:
            out["invalidated_bounds"].append({"bound_id": bid, "reason": reason})
    out["invalidation_counts"] = dict(Counter(row["reason"].split(":", 1)[0] for row in out["invalidated_bounds"]))
    return out


def bound_approval_errors(review, inputs, artifacts, *, resolve=None):
    """Validate certificates on freeze and handoff, including current reuse scope.

    Credentials are optional for old/no-change records. Declining credentials
    never declines the full ordinary scientific review or the final approval.
    """
    fields = {"bound_approvals", "bound_issue_scopes"}
    if not fields.intersection(review):
        return []
    errors = []

    def add(code, path, message):
        errors.append({"code": code, "path": path, "message": message})

    if review.get("review_type") != "profile" or review.get("subject_ref") != inputs.get("subject_ref"):
        add("bound_review_subject", "/subject_ref", "Bound credentials bind this independent profile-review subject only.")
        return errors
    if (inputs.get("issue_scope_contract_version") == OCCURRENCE_SCOPE_VERSION and review.get("bound_approvals")
            and review.get("issue_scope_version") != OCCURRENCE_SCOPE_VERSION):
        add("bound_issue_scope_version", "/issue_scope_version", "This task requires occurrence-bound occurrence-bound-scope credentials; older scopes cannot certify previously unlisted history.")
        return errors
    if not review.get("bound_approvals") and not review.get("coverage_audit", {}).get("reused_bound_ids"):
        return errors  # Includes a no-change research review explicitly declining credentials.
    try:
        snapshot = _snapshot(artifacts, review["subject_ref"])
        if review.get("prepared_hash") is not None and review["prepared_hash"] != snapshot["prepared"]["bundle_hash"]:
            raise _Unavailable("review_prepared_hash_mismatch")
        if not review.get("bound_approvals"):
            if review.get("coverage_audit", {}).get("reused_bound_ids"):
                raise _Unavailable("bound_reuse_requires_current_explicit_approval")
            return errors
        approvals, _, _, _ = _bound_contract(artifacts, snapshot, review)
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        add("bound_approval_contract", "/bound_approvals", str(exc))
        if review.get("issue_scope_version") == OCCURRENCE_SCOPE_VERSION:
            try:
                errors[-1]["scope_diagnostic"] = scope_diagnostic(artifacts, _snapshot(artifacts, review["subject_ref"]), review)
            except (ProtocolError, KeyError, TypeError, ValueError):
                pass  # Original fail-closed error remains authoritative.
        return errors
    audit = review.get("coverage_audit", {})
    reused = audit.get("reused_bound_ids", [])
    if reused:
        try:
            context_ref = inputs.get("review_context_ref")
            if not context_ref or audit.get("reuse_context_ref") != context_ref:
                raise _Unavailable("bound_reuse_context_binding_mismatch")
            item = (resolve or artifacts.get)(context_ref)
            context = item["data"]
            if item["kind"] != "external_result" or context.get("current_proposal_ref") != review["subject_ref"] or context.get("current_bundle_hash") != snapshot["prepared"]["bundle_hash"]:
                raise _Unavailable("bound_reuse_context_binding_mismatch")
            ws = getattr(artifacts, "workspace", None)
            if ws is None or not context.get("previous_review_ref"):
                raise _Unavailable("bound_reuse_context_has_no_independent_prior_review")
            verified = build_review_context(artifacts, ws, review["subject_ref"], context["previous_review_ref"])
            keys = ("current_proposal_ref", "current_prepared_ref", "current_bundle_hash", "previous_review_ref", "reusable_bound_ids", "reuse_candidates")
            if any(context.get(key) != verified.get(key) for key in keys):
                raise _Unavailable("bound_reuse_context_not_controller_verifiable")
            if not isinstance(reused, list) or any(not isinstance(b, str) for b in reused) or len(set(reused)) != len(reused) or not set(reused).issubset(approvals):
                raise _Unavailable("bound_reuse_requires_current_explicit_approval")
            candidates = {row["bound_id"]: row for row in verified["reuse_candidates"]}
            if not set(reused).issubset(candidates):
                raise _Unavailable("bound_reuse_outside_controller_candidates")
            for bid in reused:
                candidate = candidates[bid]
                if candidate.get("scope") != "bound_applicability" or sorted(approvals[bid]["context_pointers"]) != candidate.get("context_pointers"):
                    raise _Unavailable("reused_bound_context_declaration_changed")
        except (ProtocolError, KeyError, TypeError, ValueError) as exc:
            add("bound_reuse_context", "/coverage_audit/reused_bound_ids", str(exc))
    return errors
