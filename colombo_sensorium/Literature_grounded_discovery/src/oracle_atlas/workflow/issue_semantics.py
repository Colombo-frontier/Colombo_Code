"""Separate a scoped issue's mathematical contract from its snapshot address.

This is structural identity, not a natural-language equivalence test. Only the
subject address of a verified current snapshot may be rebound. Source/evidence
hashes, arbitrary subjects, mathematical wording and every other field remain
part of the fingerprint. Raw hashes are always retained for audit.
"""
from ..core.store import digest
from ..core.contracts import references


ISSUE_SCOPE_VERSION = "snapshot-bound-scope"
OCCURRENCE_SCOPE_VERSION = "occurrence-bound-scope"
SEMANTIC_SCOPE_VERSIONS = {ISSUE_SCOPE_VERSION, OCCURRENCE_SCOPE_VERSION}
CONTEXTUAL_KINDS = {"candidate", "identity", "review"}


def dependency_issue_catalog(artifacts, snapshot, review=None):
    """List exact issue occurrences without interpreting or erasing any issue.

    All pinned profile scientific references and registered research support are
    traversed under the normal bounded graph contract. Historical context can
    be scoped by a fresh independent review; issues inside proof/result/source
    (and unknown object kinds) remain hard blockers. The raw closure is retained
    even when an issue is independently judged outside a proposition's scope.
    """
    from .review_context import _Graph, _Unavailable
    from .proof_reuse import BLOCKING, MAX_ISSUES, _structured_issues

    graph = _Graph(artifacts)
    proposal = snapshot["proposal"]
    research = snapshot["research"]["data"]
    roots = references(snapshot["profile"]) | set(research.get("result_refs", [])) | set(research.get("proof_refs", []))
    roots.update((proposal["candidate_ref"], proposal["identity_ref"]))
    closure, byte_count = graph.closure(roots)
    documents = {row["ref"]: graph.item(row["ref"]) for row in closure}
    documents.update({proposal["profile_ref"]: {"kind": "profile", "data": snapshot["profile"]},
                      proposal["research_ref"]: snapshot["research"],
                      proposal["candidate_ref"]: snapshot["candidate"]})
    current_roles = {proposal["profile_ref"]: "current_profile", proposal["research_ref"]: "current_research",
                     proposal["candidate_ref"]: "current_candidate", proposal["identity_ref"]: "current_identity"}
    occurrences, hard = [], []
    current_scientific = {proposal["profile_ref"], proposal["research_ref"]}

    def collect(ref, item, role, *, contextual):
        for issue, pointer in _structured_issues(item["data"], with_pointers=True):
            if not BLOCKING.intersection(issue["blocks"]):
                continue
            variant_hash = digest(issue)
            identity = {"artifact_ref": ref, "subject_ref": snapshot["ref"] if ref is None else None,
                        "issue_pointer": pointer, "variant_hash": variant_hash}
            row = {"occurrence_id": "occurrence:" + digest(identity), "issue_id": issue["issue_id"],
                   "artifact_ref": ref, "artifact_kind": item["kind"], "artifact_role": role,
                   "issue_pointer": pointer, "variant_hash": variant_hash, "issue": issue,
                   "subject_ref": identity["subject_ref"]}
            (occurrences if contextual else hard).append(row)
            if len(occurrences) + len(hard) > MAX_ISSUES * 8:
                raise _Unavailable("issue_occurrence_count_limit")

    for ref, item in sorted(documents.items()):
        role = current_roles.get(ref)
        if role is None:
            role = "historical_" + (str(item["data"].get("review_type", "unknown")) + "_review"
                                   if item["kind"] == "review" else item["kind"])
        collect(ref, item, role, contextual=ref in current_scientific or item["kind"] in CONTEXTUAL_KINDS)
    if review:
        collect(None, {"kind": "review", "data": review}, "current_review", contextual=True)
    return {"issue_scope_version": OCCURRENCE_SCOPE_VERSION, "current_proposal_ref": snapshot["ref"],
            "issue_occurrences": sorted(occurrences, key=lambda row: row["occurrence_id"]),
            "hard_dependency_blockers": sorted(hard, key=lambda row: row["occurrence_id"]),
            "dependency_count": len(closure), "dependency_bytes": byte_count,
            "dependency_refs": [row["ref"] for row in closure]}


def subject_aliases(snapshot):
    proposal = snapshot["proposal"]
    return {ref: role for ref, role in (
        (snapshot["ref"], "snapshot:proposal"),
        (proposal["prepared_ref"], "snapshot:prepared"),
        (proposal["research_ref"], "snapshot:research"),
        (proposal["profile_ref"], "snapshot:profile"),
        (snapshot["research"]["data"]["profile_ref"], "snapshot:profile"),
    )}


def verified_delivery_lineage(prior, current, previous_review_ref):
    """Comparison-only aliases after the caller validates the prior review.

    This never changes raw catalog rows or scope IDs. Only the two pinned
    deliveries and that exact independent review may change their delivery
    role; other history, including an unseen sibling candidate, keeps its
    origin. Evidence, wording and non-delivery subjects are never normalized.
    """
    return {"aliases": {**subject_aliases(prior), **subject_aliases(current)},
            "delivery_refs": {previous_review_ref, prior["proposal"]["profile_ref"],
                              prior["proposal"]["research_ref"],
                              prior["research"]["data"]["profile_ref"]}}


def issue_signature(issue, snapshot, *, scoped=False, lineage=None):
    material = digest(issue)
    if not scoped:
        return material
    aliases = lineage["aliases"] if lineage else subject_aliases(snapshot)
    # Do not replace SHA text inside a formula/message, source locator or
    # evidence_refs. Those can encode actual mathematical changes.
    value = {**issue, "subject_refs": [aliases.get(ref, ref) for ref in issue["subject_refs"]]}
    return digest(value)


def occurrence_signature(row, snapshot, *, lineage=None):
    """A new historical context is not covered by an old same-named issue.

    Current profile/research/review copies may move during the handoff without
    changing the mathematical issue. Historical objects retain their actual
    source identity and pointer; their contexts are never silently equated.
    """
    current = row["artifact_role"] in {"current_profile", "current_research", "current_review"}
    if lineage and row["artifact_ref"] in lineage["delivery_refs"]:
        current = True
    return digest({"origin": "current_delivery" if current else row["artifact_ref"],
                   "pointer": None if current else row["issue_pointer"],
                   "semantic_variant": issue_signature(row["issue"], snapshot, scoped=True, lineage=lineage)})


def scope_diagnostic(artifacts, snapshot, review):
    """Machine-computed IDs for draft validation, including unsaved review rows.

    The full historical text is already available in the controller catalog.
    Return current-review rows and the exact required ID sets so a reviewer
    never needs to implement hashing or guess an occurrence identifier.
    """
    catalog = dependency_issue_catalog(artifacts, snapshot, review)
    grouped = {}
    for row in catalog["issue_occurrences"]:
        grouped.setdefault(row["issue_id"], []).append(row["occurrence_id"])
    return {"issue_scope_version": OCCURRENCE_SCOPE_VERSION,
            "expected_issue_scopes": [{"issue_id": iid, "occurrence_ids": sorted(ids)} for iid, ids in sorted(grouped.items())],
            "current_review_occurrences": [row for row in catalog["issue_occurrences"] if row["artifact_role"] == "current_review"],
            "hard_dependency_blockers": catalog["hard_dependency_blockers"]}


def issue_audit(issues):
    """Bounded callers retain both the semantic comparison and original SHA trail."""
    return [{"issue_id": iid, "semantic_signatures": row["variant_signatures"],
             "material_signatures": row["material_signatures"],
             "occurrence_signatures": row.get("occurrence_signatures", []),
             "subject_refs": row["subject_refs"], "evidence_refs": row["evidence_refs"]}
            for iid, row in sorted(issues.items())]
