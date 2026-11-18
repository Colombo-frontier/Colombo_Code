"""Navigation and mechanical diagnostics for controller-generated native files."""
from __future__ import annotations

from ..core.contracts import ProtocolError

SIDECARS = ("identity.json", "classification.json", "human_tags.json", "machine_tags.json")


def projection_report(prepared):
    files = prepared["files"]
    return {
        "bundle_hash": prepared["bundle_hash"],
        "validation": prepared.get("mechanical_validation", {
            "status": "historical_snapshot_without_validation_receipt", "diagnostics": []}),
        "files": {name: {"pointer": "/files/" + name,
                         "byte_sha256": prepared["hashes"][name],
                         "fields": sorted(value)} for name, value in files.items()},
        "field_directory": {
            "scientific_regimes": "/files/profile.json/regimes",
            "regime_predicates": "/files/identity.json/regime_predicates",
            "machine_tag_facts": "/files/machine_tags.json/tag_facts",
            "machine_operations": "/files/machine_tags.json/operation_bindings",
            "machine_registry": "/files/machine_tags.json/registry",
            "human_facets": "/files/human_tags.json/facets",
        },
        "counts": {"scientific_regimes": len(files["profile.json"].get("regimes", [])),
                   "regime_predicates": len(files["identity.json"].get("regime_predicates", []))},
        "ownership": "The controller generates the four sidecars from the scientific profile and final tag facts. "
                     "machine_tags.registry is optional profile.registry passthrough, not the regime index. "
                     "Validation confirms structural consistency, not mathematical correctness. "
                     "Read existing hashes/value_digest; do not reserialize a full profile to calculate them.",
    }


def mechanical_repair_request(review, *, active_bound_ids=None):
    """Validate an independent review's explicit routing; never classify issue prose."""
    rows = review.get("projection_repairs", [])
    if not rows:
        return False
    if review.get("review_type") != "profile" or review.get("verdict") not in {"revise", "defer"}:
        raise ProtocolError("projection_repairs requires a non-approving profile review")
    issues = {row["issue_id"]: row for row in review.get("issues", [])}
    ids = [row["issue_id"] for row in rows]
    if len(set(ids)) != len(ids):
        raise ProtocolError("projection_repairs must identify distinct issues")
    for row in rows:
        issue = issues.get(row["issue_id"])
        if (not issue or issue["kind"] != "protocol_error" or not issue["blocks"]
                or set(issue["blocks"]) - {"profile", "publication"}
                or row["file"] not in SIDECARS or not row["pointer"].startswith("/")
                or not row["reason"].strip()):
            raise ProtocolError("projection_repairs may route only explicit sidecar protocol errors; scientific blockers remain with research")
    # This opt-in is used only after the stored review passed its independent
    # credential validation. Future-claim bound issues must not force authors
    # to rewrite generated files, but an unscoped or currently affected claim does.
    credentials = {row.get("bound_id") for row in review.get("bound_approvals", [])}
    audited = (active_bound_ids is not None and bool(credentials)
               and review.get("issue_scope_version") == "occurrence-bound-scope"
               and set(active_bound_ids) <= credentials
               and set(active_bound_ids) <= set(review.get("approved_bound_ids", [])))
    unrelated = {row["issue_id"] for row in review.get("bound_issue_scopes", [])
                 if audited and row.get("scope_complete") is True
                 and row.get("affected_bound_ids") == [] and row.get("occurrence_ids")}
    blocking = {row["issue_id"] for row in issues.values()
                if set(row.get("blocks", [])) & {"bound", "profile", "publication", "identity", "extraction"}
                and not (set(row.get("blocks", [])) == {"bound"} and row["issue_id"] in unrelated)}
    return blocking == set(ids)
