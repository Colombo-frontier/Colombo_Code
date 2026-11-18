"""Assemble review navigation from frozen public records. Judgments stay with the reviewer."""
from __future__ import annotations

import re

from ..core.contracts import ProtocolError, resolve_pointer
from ..core.store import dumps
from ..atlas.projection_report import projection_report
from .review_context import _get, _prior_review, _snapshot


def _pointer(path, field):
    return path + "/" + str(field).replace("~", "~0").replace("/", "~1")


# Identity fields precede the fallback native id. Duplicate or unknown row ids
# are reported at their whole container; positional matches cannot certify reuse.
_ROW_IDS = ("id", "comparison_id", "finding_id", "cell_id", "row_id", "bound_id", "proof_id",
            "view_id", "parameter_id", "quantity_id", "resource_projection_id")


def _indexed(rows):
    output = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            return None
        key = next((row[field] for field in _ROW_IDS
                    if isinstance(row.get(field), str) and row[field]), None)
        if key is None or key in output:
            return None
        output[key] = (index, row)
    return output


def _difference(before, after, path=""):
    """Return exact changed pointers, with stable row locations for both versions."""
    if before == after:
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        entries = []
        for field in sorted(before.keys() | after.keys()):
            prefix = _pointer(path, field)
            if field not in before:
                entries.append({"after": prefix})
            elif field not in after:
                entries.append({"before": prefix})
            else:
                entries.extend(_difference(before[field], after[field], prefix))
        return entries
    if isinstance(before, list) and isinstance(after, list):
        old, new = _indexed(before), _indexed(after)
        if old is not None and new is not None:
            entries = []
            if [k for k in old if k in new] != [k for k in new if k in old]:
                entries.append({"before": path, "after": path, "change": "row_order"})
            for key in sorted(old.keys() | new.keys()):
                if key in old and key in new and old[key][1] == new[key][1]:
                    continue
                entry = {"id": key}
                if key in old:
                    entry["before"] = _pointer(path, old[key][0])
                if key in new:
                    entry["after"] = _pointer(path, new[key][0])
                if key in old and key in new:
                    left, right = old[key][1], new[key][1]
                    entry["changed_fields"] = sorted(field for field in left.keys() | right.keys()
                                                     if field not in left or field not in right or left[field] != right[field])
                entries.append(entry)
            return entries
    return [{"before": path, "after": path}]


def _paper_ranges(locator, source):
    """Only suggest original offsets when the locator explicitly specifies PDF page numbers."""
    text = source["text"]
    pages = {row["page"]: row for row in source.get("metadata", {}).get("locators", [])
             if isinstance(row, dict) and all(isinstance(row.get(k), int) for k in ("page", "start", "end"))}
    matches = re.finditer(r"\bPDF\s+(?:p{1,2}\.|pages?)\s*(\d{1,6})(?:\s*[-–—]\s*(\d{1,6}))?",
                          locator, re.IGNORECASE)
    ranges = []
    for match in matches:
        first, last = int(match[1]), int(match[2] or match[1])
        if first in pages and last in pages and first <= last:
            start, end = pages[first]["start"], pages[last]["end"]
            if 0 <= start < end <= len(text):
                excerpt_end = min(start + 260, end)
                ranges.append({"pages": [first, last], "offset": start, "end": end,
                               "excerpt_end": excerpt_end, "page_start_excerpt": text[start:excerpt_end]})
    return ranges


def _literal_anchors(locator, text):
    # Matches locate mentions, including citations. They are navigation aids;
    # only the reviewer judges whether a passage states the requested theorem.
    labels = re.findall(r"\b(?:Theorem|Lemma|Proposition|Corollary|Open Question)\s+\d+(?:\.\d+)*",
                        locator, re.IGNORECASE)
    anchors = []
    for label in dict.fromkeys(labels):
        pattern = re.compile(r"\b" + re.escape(label) + r"(?![\d.]*\d)", re.IGNORECASE)
        for match in pattern.finditer(text):
            start, end = max(0, match.start() - 65), min(len(text), match.end() + 110)
            anchors.append({"label": label, "offset": start, "end": end, "excerpt": text[start:end]})
            break
        if len(anchors) == 3:
            break
    return anchors


def _evidence(artifacts, snapshot):
    profile, research = snapshot["profile"], snapshot["research"]["data"]
    groups, sources, proofs = {}, {}, {}
    result_refs = dict.fromkeys(research.get("result_refs", []))
    proof_refs = dict.fromkeys(research.get("proof_refs", []))
    # Native records can also carry pinned formal results from earlier updates.
    for table, keys, into in (("bounds", ("result_ref", "result_artifact_ref"), result_refs),
                              ("evidence", ("result_ref", "result_artifact_ref"), result_refs),
                              ("proofs", ("proof_ref", "proof_artifact_ref"), proof_refs)):
        for row in profile.get(table, []):
            if isinstance(row, dict):
                for field in keys:
                    ref = row.get(field)
                    if isinstance(ref, str) and re.fullmatch(r"sha256:[a-f0-9]{64}", ref):
                        into.setdefault(ref)
    source_cache = {}
    def source_data(ref):
        if ref not in source_cache:
            source = _get(artifacts, ref, "source")["data"]
            source_cache[ref] = source
            sources[ref] = {"ref": ref, "url": source["url"], "version": source["version"]}
        return source_cache[ref]
    for ref in result_refs:
        result = _get(artifacts, ref, "result")["data"]
        for source_ref in result["source_refs"]:
            source_data(source_ref)
        anchors = []
        for entry in result["source_locators"]:
            source_ref = entry["source_ref"]
            source = source_data(source_ref)
            matches = source["version"] == entry["version"]
            anchors.append({**entry, "version_matches": matches,
                            "first_literal_mentions": _literal_anchors(entry["locator"], source["text"]) if matches else [],
                            "pdf_ranges": _paper_ranges(entry["locator"], source) if matches else []})
        groups[ref] = {"ref": ref, "id": result["result_id"], "comparison_key": result["comparison_key"],
                       "origin": result["origin"], "source_locators": anchors, "proof_refs": result["proof_refs"]}
        proof_refs.update(dict.fromkeys(result["proof_refs"]))
    for ref in proof_refs:
        proof = _get(artifacts, ref, "proof")["data"]
        proofs[ref] = {"ref": ref, "id": proof["proof_id"], "dependencies": proof["dependencies"]}
    return {"results": groups, "proofs": proofs, "sources": sources}


def _available_evidence(artifacts, snapshot):
    try:
        return _evidence(artifacts, snapshot)
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        # Legacy source pointers or unresolved materials still permit an independent
        # rejection/defer. Expose the original graph explicitly without inventing supports.
        return {"index_unavailable": str(exc)[:240], "research_ref": snapshot["proposal"]["research_ref"],
                "profile_ref": snapshot["proposal"]["profile_ref"]}


def _comparison_scope(old, new, changes):
    """List affected frozen comparison IDs; unfamiliar or global scopes expand to every ID."""
    all_ids = set()
    by_bound = {}
    for profile in (old, new):
        for row in profile.get("joint_analysis", {}).get("comparisons", []):
            key = row["comparison_id"]
            all_ids.add(key)
            for use in row.get("bound_uses", []):
                by_bound.setdefault(use["bound_id"], set()).add(key)
        all_ids.update(row["comparison_id"] for row in profile.get("comparisons", []))
    affected = set()
    for entry in changes:
        path = entry.get("after", entry.get("before"))
        if path.startswith(("/comparisons/", "/joint_analysis/comparisons/")) and entry.get("id") in all_ids:
            affected.add(entry["id"])
        elif path.startswith(("/bounds/", "/joint_analysis/provenance/")) and entry.get("id") in by_bound:
            affected.update(by_bound[entry["id"]])
        else:
            return {"scope": "all", "comparison_ids": sorted(all_ids), "reason_pointer": path}
    return {"scope": "declared_rows", "comparison_ids": sorted(affected)}


def _changes_with_excerpts(old, new):
    changes = _difference(old, new)
    for change in changes:
        for side, document in (("before", old), ("after", new)):
            if side not in change:
                continue
            value = resolve_pointer(document, change[side])
            if "changed_fields" in change:
                value = {k: value[k] for k in change["changed_fields"] if k in value}
            text = value if isinstance(value, str) else dumps(value)
            change[side + "_excerpt"] = text[:350]
            if len(text) > 350:
                change[side + "_chars"] = len(text)
    return changes


def assemble_review_packet(artifacts, subject_ref, bounds, proofs, *, delivery_scope_ref=None, proof_context_ref=None):
    """Build an immutable dossier, paged with artifact_get, with no implicit read or approval."""
    try:
        current = _snapshot(artifacts, subject_ref)
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        prop = _get(artifacts, subject_ref, "proposal")["data"]
        return {"overview": {"mode": "full", "subject_ref": subject_ref, "prepared_ref": prop["prepared_ref"],
                             "profile_ref": prop["profile_ref"], "research_ref": prop["research_ref"],
                             "joint_analysis_pointer": "/files/profile.json/joint_analysis",
                             "index_unavailable": str(exc)[:240]}, "review_scope": {"reusable_bound_ids": [],
                             "reusable_proof_refs": [], "always_review": bounds["always_review"]},
                "prior_issues": [], "differences": {}, "evidence": {"research_ref": prop["research_ref"]}}
    prop, prepared = current["proposal"], current["prepared"]
    native = prepared["files"]["profile.json"]
    packet = {
        "overview": {"mode": "full", "subject_ref": subject_ref, "prepared_ref": prop["prepared_ref"],
                     "profile_ref": prop["profile_ref"], "research_ref": prop["research_ref"],
                     "bundle_hash": prepared["bundle_hash"], "five_file_hashes": prepared["hashes"],
                     "joint_analysis_pointer": "/files/profile.json/joint_analysis",
                     "joint_sections": list(native.get("joint_analysis", {}))},
        "evidence": _available_evidence(artifacts, current),
        "native_projection": projection_report(prepared),
        "issue_scope_version": "occurrence-bound-scope",
        "adopted_proof_requirements": proofs.get("adopted_proof_requirements", []),
        "issue_occurrences": list({row["occurrence_id"]: row for context in (bounds, proofs)
                                   for row in context.get("issue_occurrences", [])}.values()),
        "hard_dependency_blockers": {"bounds": bounds.get("hard_dependency_blockers", []),
                                     "proofs": proofs.get("hard_dependency_blockers", [])},
        "prior_issues": [], "differences": {}, "review_scope": {
            "reusable_bound_ids": [], "reusable_proof_refs": [], "always_review": bounds["always_review"],
            "unverified_bounds": [row.get("id", row.get("bound_id")) for row in native["bounds"] if isinstance(row, dict)]},
    }
    # Navigation only: the full immutable context/issue deltas stay in the
    # already-saved proof catalog and are read on demand, not copied here.
    scope_candidates = proofs.get("proof_scope_revalidation_candidates", [])
    packet["review_scope"]["proof_scope_revalidation_candidates"] = [
        {"candidate_id": row["candidate_id"], "proof_ref": row["proof_ref"],
         "context_change_count": len(row["context_changes"]["changes"]),
         "context_changes_truncated": row["context_changes"]["truncated"],
         "new_issue_occurrence_count": len(row["new_issue_occurrence_ids"]),
         "details": {"ref": proof_context_ref, "pointer": f"/proof_scope_revalidation_candidates/{index}"}}
        for index, row in enumerate(scope_candidates)]
    packet["review_scope"]["proof_scope_revalidation_index"] = {
        "ref": proof_context_ref, "pointer": "/proof_scope_revalidation_candidates", "count": len(scope_candidates)}
    if delivery_scope_ref:
        packet["overview"]["delivery_scope_ref"] = delivery_scope_ref
        packet["review_scope"]["delivery_frontier"] = _get(artifacts, delivery_scope_ref, "external_result")["data"]
        packet["review_scope"]["recorded_followups"] = native.get("delivery_followups", [])
    prior_ref = bounds.get("previous_proposal_ref")
    if not prior_ref or bounds.get("reuse_status") != "candidates_verified":
        return packet
    prior = _snapshot(artifacts, prior_ref)
    if any(prior["proposal"][key] != prop[key] for key in ("candidate_ref","identity_ref","base_version","mode")) or prior["profile"]["setting_id"] != native["setting_id"]:
        return packet
    prior_review_ref = bounds["previous_review_ref"]
    prior_review = _get(artifacts, prior_review_ref, "review")["data"]
    packet["overview"].update(mode="delta", previous_review_ref=prior_review_ref,
                              previous_prepared_ref=prior["proposal"]["prepared_ref"],
                              previous_profile_ref=prior["proposal"]["profile_ref"])
    packet["prior_issues"] = prior_review["issues"]
    packet["review_scope"]["prior_followups"] = prior_review.get("coverage_audit", {}).get("followups", [])
    for name, file in prepared["files"].items():
        old = prior["prepared"]["files"][name]
        if old != file:
            packet["differences"][name] = _changes_with_excerpts(old, file)
    proof_reuse = proofs.get("reusable_proof_refs", []) if proofs.get("previous_review_ref") == prior_review_ref else []
    packet["review_scope"].update(reusable_bound_ids=bounds["reusable_bound_ids"], reusable_proof_refs=proof_reuse,
                                  unverified_bounds=bounds["invalidated_bounds"], invalidated_proofs=proofs["invalidated_proofs"])
    packet["review_scope"]["comparison_impact"] = _comparison_scope(
        prior["profile"], native, packet["differences"].get("profile.json", []))
    packet["overview"]["changed_files"] = list(packet["differences"])
    # Rows under a top-level field are contiguous. Reviewers can jump to an
    # affected row or page instead of reading the complete old and new profiles.
    groups = {}
    for index, row in enumerate(packet["differences"].get("profile.json", [])):
        path = row.get("after", row.get("before"))
        parts = path.split("/")
        key = "/".join(parts[:3] if path.startswith("/joint_analysis/") else parts[:2])
        group = groups.setdefault(key, {"first_index": index, "count": 0})
        group["count"] += 1
    packet["overview"]["profile_difference_groups"] = groups
    return packet


def revision_materials(artifacts, ws, previous_research_ref, review_ref):
    """Provide the producer a validated issue ledger and supporting references before it revises a frozen draft."""
    try:
        review, prior, job = _prior_review(artifacts, ws, review_ref)
    except (ProtocolError, KeyError, TypeError, ValueError):
        return None
    if review["verdict"] != "revise" or prior["proposal"]["research_ref"] != previous_research_ref:
        return None
    packet_ref = ws.job(job)["inputs"].get("review_packet_ref")
    if packet_ref:
        packet = _get(artifacts, packet_ref, "external_result")["data"]
        if packet.get("overview", {}).get("subject_ref") != review["subject_ref"]:
            packet_ref = None
    return {"review_ref": review_ref, "subject_ref": review["subject_ref"],
            "profile_ref": prior["proposal"]["profile_ref"], "prepared_ref": prior["proposal"]["prepared_ref"],
            "issues": review["issues"], "review_packet_ref": packet_ref,
            "native_projection": projection_report(prior["prepared"]),
            "followups": review.get("coverage_audit", {}).get("followups", []),
            "evidence": None if packet_ref else _available_evidence(artifacts, prior)}
