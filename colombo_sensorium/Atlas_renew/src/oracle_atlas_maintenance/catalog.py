"""Project reviewed native states into an existing browsing catalogue.

Projection never guesses a scientific status from a formula.  A caller supplies
only committed five-file bundles, and keeps publication receipts separately.
The pure function preserves all nonselected rows and the existing order.
"""
from copy import deepcopy

from .taxonomy import validate_status_taxonomy


def project_catalog_rows(catalog, profiles):
    """Refresh counts and status filters for explicitly selected native profiles.

    Tag membership and unrelated editorial metadata are not inferred here.
    This returns a value; the publication controller owns locks and atomic I/O.
    """
    result = deepcopy(catalog)
    rows = result.get("profiles")
    if not isinstance(rows, list):
        raise ValueError("Catalogue must contain profiles")
    ids = [row.get("id") for row in rows]
    if any(not isinstance(sid, str) for sid in ids) or len(ids) != len(set(ids)):
        raise ValueError("Catalogue IDs must be unique")
    if not set(profiles).issubset(ids):
        raise ValueError("Status projection cannot insert unreviewed settings")
    for row in rows:
        sid = row["id"]
        if sid not in profiles:
            continue
        profile = profiles[sid]
        if profile.get("setting_id") != sid:
            raise ValueError("Native profile and catalogue setting IDs disagree")
        validate_status_taxonomy(profile)
        summary = profile["summary_status"]
        statuses = {}
        for item in summary["badges"] + summary["special_statuses"]:
            statuses[item["code"]] = item.get("label", item["code"])
        for comparison in profile["comparisons"]:
            state = comparison["status"]
            statuses.setdefault(state["code"], state.get("label", state["code"]))
        per_view = {}
        for view in profile.get("views", []):
            vid = view["view_id"]
            comparisons = [c for c in profile["comparisons"] if c["view_id"] == vid]
            codes = list(dict.fromkeys(c["status"]["code"] for c in comparisons))
            if "fully_optimal" in statuses:
                codes.append("fully_optimal")
            if any(c["status"].get("missing_sides") for c in comparisons):
                codes.append("bounds_missing")
            per_view[vid] = list(dict.fromkeys(codes))
        row.update(statusCodes=list(statuses), statusLabels=list(statuses.values()),
                   viewStatusCodes=per_view)
        for key in ("views", "comparisons", "regimes", "bounds"):
            if key in row:
                row[key] = len(profile.get(key, []))
    return result
