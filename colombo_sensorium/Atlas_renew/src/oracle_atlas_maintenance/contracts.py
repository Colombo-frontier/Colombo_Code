"""Mechanical scope and delta checks. The model judges mathematical applicability."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from jsonschema import Draft202012Validator

from .state import digest
from .normalization import apply_quantity_normalizations
from .taxonomy import validate_status_taxonomy

FIELDS = {"bounds": ("id", "bound_id"), "comparisons": ("comparison_id",), "regimes": ("id", "regime_id"),
          "evidence": ("id", "evidence_id"), "references": ("id", "source_id"), "proofs": ("id", "proof_id"),
          "bracket_rows": ("row_id",), "quantities": ("id", "quantity_id")}
IMMUTABLE = ("setting_id", "common_specification", "views", "parameters", "symbols", "quantities",
             "resource_projections", "aliases", "primary_domain", "title", "facets", "relations")
KEY = ("setting_id", "view_id", "guarantee_id", "quantity_id", "resource_projection_id", "regime_id")


class FindingCoverageError(ValueError):
    """Unchanged rejection rule with bounded actionable mechanical ID metadata."""
    def __init__(self, affected, declared, known):
        super().__init__("Findings must cover every mechanically affected comparison and refer only to declared comparisons")
        self.details = {}
        for name, values in (("affected_comparison_ids", affected), ("missing_comparison_ids", affected - declared),
                             ("unknown_comparison_ids", declared - known)):
            ordered = sorted(values)
            self.details[name] = ordered[:128]
            self.details[name + "_count"] = len(ordered)
            self.details[name + "_sha256"] = digest(ordered)
        self.details["truncated"] = any(self.details[name + "_count"] > 128 for name in
            ("affected_comparison_ids", "missing_comparison_ids", "unknown_comparison_ids"))
        self.details["scientific_approval"] = False


def schema(role):
    return json.loads((Path(__file__).parent / "resources" / f"{role}.schema.json").read_text())


def validate(role, data):
    Draft202012Validator(schema(role)).validate(data)


def row_id(row, collection):
    return next((row[k] for k in FIELDS[collection] if k in row), None)


def _strings(value):
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return set().union(*(_strings(v) for v in value)) if value else set()
    if isinstance(value, dict):
        return set(value) | (set().union(*(_strings(v) for v in value.values())) if value else set())
    return set()


def affected_comparisons(baseline, proposed, delta):
    """Conservative ID-reference closure; this is scope accounting, not a proof of applicability."""
    changed = {d["id"] for d in delta}
    rows = [(collection, r) for profile in (baseline, proposed) for collection in FIELDS
            for r in profile.get(collection, [])]
    while True:
        expanded = changed | {row_id(row, collection) for collection, row in rows
                              if _strings(row) & changed and row_id(row, collection) is not None}
        if expanded == changed:
            break
        changed = expanded
    comparison_ids = {row_id(r, "comparisons") for r in proposed.get("comparisons", [])}
    if baseline.get("joint_analysis") != proposed.get("joint_analysis"):
        before = {r["comparison_id"]: r for r in baseline.get("joint_analysis", {}).get("comparisons", [])}
        after = {r["comparison_id"]: r for r in proposed.get("joint_analysis", {}).get("comparisons", [])}
        changed |= {cid for cid in set(before) | set(after) if before.get(cid) != after.get(cid)}
        # A target/domain reinterpretation affects every comparison, including those
        # not mentioned by a proposed annotation. This is intentionally conservative.
        for field in ("target", "domain_map", "normalization_requests"):
            if baseline.get("joint_analysis", {}).get(field) != proposed.get("joint_analysis", {}).get(field):
                changed |= comparison_ids
        before_analysis, after_analysis = baseline.get("joint_analysis", {}), proposed.get("joint_analysis", {})
        old_provenance = {r["bound_id"]: r for r in before_analysis.get("provenance", [])}
        new_provenance = {r["bound_id"]: r for r in after_analysis.get("provenance", [])}
        provenance_ids = {bid for bid in set(old_provenance) | set(new_provenance)
                          if old_provenance.get(bid) != new_provenance.get(bid)}
        changed |= provenance_ids
        for analysis in (before_analysis, after_analysis):
            for row in analysis.get("comparisons", []):
                if {u["bound_id"] for u in row.get("bound_uses", [])} & provenance_ids:
                    changed.add(row["comparison_id"])
        old_impact = {r["finding_id"]: r for r in before_analysis.get("impact", [])}
        new_impact = {r["finding_id"]: r for r in after_analysis.get("impact", [])}
        for fid in set(old_impact) | set(new_impact):
            if old_impact.get(fid) != new_impact.get(fid):
                changed |= set(old_impact.get(fid, {}).get("comparison_ids", [])) | set(new_impact.get(fid, {}).get("comparison_ids", []))
        if before_analysis.get("pending_obligations") != after_analysis.get("pending_obligations"):
            changed |= comparison_ids
        while True:
            expanded = changed | {row_id(row, collection) for collection, row in rows
                                  if _strings(row) & changed and row_id(row, collection) is not None}
            if expanded == changed:
                break
            changed = expanded
    if baseline.get("summary_status") != proposed.get("summary_status"):
        return comparison_ids
    return changed & comparison_ids


def bracket_signature(profile):
    """Pin operative rows, rather than treating every archived bound as a bracket change."""
    comparisons = profile.get("comparisons", [])
    used = _strings(comparisons)
    bounds = [r for r in profile.get("bounds", []) if row_id(r, "bounds") in used or
              set(r.get("selected_in_regimes", [])) & {row_id(c, "comparisons") for c in comparisons}]
    used |= _strings(bounds)
    regimes = []
    while True:
        selected = [r for r in profile.get("regimes", []) if row_id(r, "regimes") in used]
        expanded = used | _strings(selected)
        regimes = selected
        if expanded == used:
            break
        used = expanded
    return {"comparisons": comparisons, "bounds": bounds, "regimes": regimes,
            "summary_status": profile.get("summary_status"), "joint_analysis": profile.get("joint_analysis")}


def compact(profile, limit=14000):
    """No silent context truncation: IDs and on-demand paths survive bounded previews."""
    result = {"setting_id": profile["setting_id"], "title": profile["title"],
              "summary_status": profile.get("summary_status"),
              "contract_hash": digest({k: profile.get(k) for k in IMMUTABLE}),
              "counts": {k: len(profile.get(k, [])) for k in FIELDS},
              "comparison_ids": [row_id(r, "comparisons") for r in profile.get("comparisons", [])],
              "read_contract_at": "/common_specification", "comparisons": [], "bounds": []}
    for collection, keys in (("comparisons", ("comparison_id", "comparison_key", "status", "bracket", "predicate_text")),
                             ("bounds", ("id", "bound_id", "direction", "formula_latex", "view_id", "guarantee_id", "region_refs", "eligible_for_bracket"))):
        for index, row in enumerate(profile.get(collection, [])):
            preview = {k: row[k] for k in keys if k in row}
            preview["read_at"] = f"/{collection}/{index}"
            preview["before_hash"] = digest(row)
            if len(json.dumps(result, ensure_ascii=False)) + len(json.dumps(preview, ensure_ascii=False)) > limit:
                result["preview_incomplete"] = True
                break
            result[collection].append(preview)
    return result


def reviewer_context_view(context, current_findings):
    """Exact reviewer-only input deduplication, never evidence or reading credit.

    The scout context remains intact. Full native arrays remain behind existing
    baseline artifact pointers; only prior findings that are byte-equivalent
    after canonical JSON encoding reference the current full finding object.
    """
    if "reviewer_input_view" in context:
        raise ValueError("A reviewer input view cannot be projected again")
    view = deepcopy(context)
    projected = []
    preview = view.get("compact_profile")
    if isinstance(preview, dict):
        for collection in ("bounds", "comparisons"):
            if not isinstance(preview.get(collection), list):
                continue
            artifacts = context.get("artifacts")
            baseline = artifacts.get("baseline") if isinstance(artifacts, dict) else None
            if not isinstance(baseline, dict) or not isinstance(baseline.get(collection), list):
                raise ValueError("Reviewer preview descriptors require the complete frozen baseline collection")
            rows = baseline[collection]
            preview[collection] = {
                "provided_complete": False, "artifact": "baseline", "pointer": "/" + collection,
                "content_hash": digest(rows), "record_count": len(rows),
                "note": "The full frozen native collection is available at this exact pointer. Omitted preview values are not read or approved."}
            projected.append(collection)
    pending = view.get("pending_work")
    referenced = 0
    if isinstance(pending, dict) and isinstance(pending.get("findings"), list) and isinstance(current_findings, list):
        def encoded(value):
            return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        candidates = [(index, row, digest(row), encoded(row)) for index, row in enumerate(current_findings)
                      if isinstance(row, dict) and isinstance(row.get("candidate_id"), str) and row["candidate_id"]]
        for index, old in enumerate(pending["findings"]):
            if not isinstance(old, dict) or not isinstance(old.get("candidate_id"), str) or not old["candidate_id"]:
                continue
            old_hash, old_encoding = digest(old), encoded(old)
            match = next(((current_index, current) for current_index, current, current_hash, current_encoding in candidates
                          if old_hash == current_hash and old == current and old_encoding == current_encoding), None)
            if match is not None:
                current_index, current = match
                pending["findings"][index] = {"current_finding_index": current_index,
                    "candidate_id": current["candidate_id"], "sha256": old_hash}
                referenced += 1
    view["reviewer_input_view"] = {
        "version": 1, "mode": "exact_same_initial_input_deduplication",
        "prior_findings_referenced": referenced, "baseline_preview_collections": projected,
        "note": "References identify exact objects already in this initial input. No source/tool-read/approval credit is granted."}
    return view


def apply_delta(baseline, report):
    validate("scout", report)
    if report.get("joint_analysis_reuse") is not None and (report["outcome"] != "no_change" or report.get("joint_analysis_json") is not None):
        raise ValueError("An analysis reference is exclusive with a full body and is available only for no_change")
    if report["outcome"] != "candidate_change":
        if report["patch"] or report["summary_status_json"] is not None or report.get("quantity_metadata_normalizations"):
            raise ValueError("Only candidate_change may propose profile edits")
        return deepcopy(baseline), []
    normalized, normalization_delta = apply_quantity_normalizations(baseline, report.get("quantity_metadata_normalizations", []))
    proposed = deepcopy(normalized)
    touched = set()
    delta = list(normalization_delta)
    for op in report["patch"]:
        collection, field, rid = op["collection"], op["id_field"], op["id"]
        if collection == "quantities":
            raise ValueError("Quantity metadata uses the explicit normalization path, never a general row patch")
        if field not in FIELDS[collection] or (collection, rid) in touched:
            raise ValueError("Invalid or duplicate patch row")
        touched.add((collection, rid))
        try:
            value = json.loads(op["value_json"])
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid nested JSON in patch {collection}/{rid} value_json: {exc.msg} "
                             f"at line {exc.lineno}, column {exc.colno}, character {exc.pos}") from exc
        if not isinstance(value, dict) or value.get(field) != rid or row_id(value, collection) != rid:
            raise ValueError("Patch row ID does not match its explicit stable ID")
        rows = proposed.setdefault(collection, [])
        matches = [i for i, row in enumerate(rows) if row_id(row, collection) == rid]
        if len(matches) > 1:
            raise ValueError("Duplicate baseline row ID")
        old = rows[matches[0]] if matches else None
        if op["before_hash"] != (digest(old) if old is not None else None):
            raise ValueError("Patch before_hash does not match the frozen baseline row")
        if old is not None:
            merged = {**old, **value}
            if collection == "comparisons" and {k: old.get("comparison_key", old).get(k) for k in KEY} != {k: merged.get("comparison_key", merged).get(k) for k in KEY}:
                raise ValueError("Existing comparison contract keys are immutable")
            if collection == "bounds":
                for key in ("direction", "view_id", "guarantee_id", "quantity_id", "quantity_ref", "quantity_refs",
                            "resource_projection_id", "resource_projection_ref", "resource_projection_refs"):
                    if old.get(key) != merged.get(key):
                        raise ValueError("Existing bound contract is immutable; add a new bound ID")
            # Keep extensions and scientific history unless explicitly replaced at a field.
            rows[matches[0]] = merged
        else:
            rows.append(value)
        delta.append({"collection": collection, "id": rid, "before_hash": op["before_hash"],
                      "after_hash": digest(rows[matches[0]] if matches else value)})
    if report["summary_status_json"] is not None:
        status = json.loads(report["summary_status_json"])
        if not isinstance(status, dict):
            raise ValueError("summary_status must be an object")
        proposed["summary_status"] = status
    if report.get("joint_analysis_json") is not None:
        analysis = json.loads(report["joint_analysis_json"])
        if not isinstance(analysis, dict):
            raise ValueError("joint_analysis_json must encode an object")
        proposed["joint_analysis"] = analysis
    if any(proposed.get(k) != normalized.get(k) for k in IMMUTABLE):
        raise ValueError("Maintenance must preserve the fixed setting contract")
    if proposed == baseline or not report["findings"] or not any(f["impact"] not in {"no_effect", "incomparable"} for f in report["findings"]):
        raise ValueError("Candidate change needs a concrete delta and supported findings")
    views = {v["view_id"]: {g["guarantee_id"] for g in v.get("guarantees", [])} for v in baseline["views"]}
    quantities = {r.get("id", r.get("quantity_id")) for r in baseline["quantities"]}
    resources = {r.get("id", r.get("resource_projection_id")) for r in baseline["resource_projections"]}
    regimes = {row_id(r, "regimes") for r in proposed["regimes"]}
    for row in proposed["comparisons"]:
        key = row.get("comparison_key", row)
        if set(KEY) - set(key) or key["setting_id"] != baseline["setting_id"] or \
           key["view_id"] not in views or key["guarantee_id"] not in views[key["view_id"]] or \
           key["quantity_id"] not in quantities or key["resource_projection_id"] not in resources or key["regime_id"] not in regimes:
            raise ValueError("Comparison must use existing view/guarantee/quantity/resource contracts and declared regimes")
        if any(field in row and row[field] != key[field] for field in KEY):
            raise ValueError("Flat comparison fields must agree with comparison_key")
    # Trigger by complete scoped bracket content, never only a summary label or a parsed formula.
    material = bracket_signature(proposed) != bracket_signature(baseline)
    if not material:
        raise ValueError("Evidence-only additions belong in the audit ledger, not a bracket publication")
    affected = affected_comparisons(baseline, proposed, delta)
    known = {row_id(r, "comparisons") for r in proposed["comparisons"]}
    declared = set().union(*(set(f["comparison_ids"]) for f in report["findings"]))
    if not declared.issubset(known) or not affected.issubset(declared):
        raise FindingCoverageError(affected, declared, known)
    validate_status_taxonomy(proposed)
    return proposed, delta


def baseline_catalog(profile, limit=6000):
    """Bounded row locations for directed maintenance, without injecting complete old arrays."""
    catalog = {"premise": "Existing curated profile is the accepted maintenance baseline; unchanged science is retained conditionally, not recertified.",
               "bounds": [], "proofs": [], "references": [], "resources": []}
    fields = {"bounds": ("id", "bound_id", "direction", "view_id", "guarantee_id", "formula_latex", "proof_refs", "source_refs"),
              "proofs": ("id", "proof_id", "title", "source_refs"),
              "references": ("id", "title", "version", "url"),
              "resource_projections": ("id", "resource_projection_id", "mode", "expression", "description")}
    for collection in ("resource_projections", "references", "proofs", "bounds"):
        target = "resources" if collection == "resource_projections" else collection
        for i, row in enumerate(profile.get(collection, [])):
            item = {k: row[k] for k in fields[collection] if k in row}
            item["read_at"] = f"/{collection}/{i}"
            if len(json.dumps(catalog, ensure_ascii=False)) + len(json.dumps(item, ensure_ascii=False)) > limit:
                catalog["incomplete"] = True
                break
            catalog[target].append(item)
    return catalog


def _bound_dependency_hash(profile, bound_id):
    index = {}
    for collection in ("bounds", "regimes", "proofs", "evidence", "references"):
        for row in profile.get(collection, []):
            rid = row_id(row, collection)
            if rid is not None:
                index.setdefault(rid, []).append((collection, row))
    queue, seen, records = [bound_id], set(), {}
    while queue:
        rid = queue.pop()
        if rid in seen:
            continue
        seen.add(rid)
        for collection, row in index.get(rid, []):
            records[f"{collection}:{rid}"] = row
            queue.extend((_strings(row) & set(index)) - seen)
    return digest({"fixed_contract": {k: profile.get(k) for k in IMMUTABLE}, "dependencies": records})


def maintenance_review_scope(baseline, proposed, report):
    """Conditional preservation of unchanged, dependency-pinned baseline claims."""
    from oracle_atlas.atlas.store import _active_bounds
    from .retention import retention_projection
    identity_before, identity_after, projection_reasons, operations, obligations = retention_projection(baseline, proposed, report)
    # Store each exact reason once. Certificates use zero-based indices into
    # this shared inventory; this changes no claim, identity or read obligation.
    projection_reasons = list({digest(reason): reason for reason in projection_reasons}.values())
    before_ids = {row_id(r, "bounds") for r in baseline.get("bounds", [])}
    active = _active_bounds(proposed)
    invalidated = set()
    for finding in report["findings"]:
        if finding["impact"] == "invalidate":
            targets = set(finding["comparison_ids"])
            for profile in (baseline, proposed):
                for row in profile.get("comparisons", []):
                    if row_id(row, "comparisons") in targets:
                        invalidated |= _strings(row) & active
    retained, fingerprints, certificates = [], {}, {}
    for bid in sorted(active & before_ids):
        old_hash, new_hash = _bound_dependency_hash(baseline, bid), _bound_dependency_hash(proposed, bid)
        old_identity = _bound_dependency_hash(identity_before, bid)
        new_identity = _bound_dependency_hash(identity_after, bid)
        if bid not in invalidated and old_identity == new_identity:
            retained.append(bid)
            fingerprints[bid] = new_hash
            certificates[bid] = {"baseline_full_dependency_sha256": old_hash,
                                 "prepared_full_dependency_sha256": new_hash,
                                 "scientific_identity_sha256": new_identity,
                                 "projection_reason_indices": list(range(len(projection_reasons))) if old_hash != new_hash else []}
    normalization_retention = bool(operations and retained)
    return {"version": 2, "mode": "conditional_existing_baseline", "setting_id": baseline["setting_id"],
            "retained_baseline_bound_ids": retained, "fresh_review_required_bound_ids": sorted(active - set(retained)),
            "dependency_sha256": fingerprints, "invalidated_baseline_bound_ids": sorted(invalidated),
            "retention_certificates": certificates,
            "projection_reasons": deepcopy(projection_reasons),
            "normalization_projection_operations": operations if normalization_retention else [],
            "retention_read_obligations": obligations if normalization_retention else [],
            "normalization_review_contract": "Approve with all six joint_checks true explicitly confirms semantic preservation of every listed exact normalization operation after independently reading all role-appropriate retention_read_obligations. The projection is not a mathematical approval.",
            "limitations": "Baseline retention is not an authenticated prior review or fresh full-profile certification. Actual dependency hashes still bind complete prepared objects; identity projection only compares validated metadata/adoption bookkeeping. Freshly verify every normalization, new adoption, mapping, premise and envelope overlap; counterevidence or contradictions suspend affected retention. Preserve unknown/unassessed scopes."}


def retained_adoption_catalog(profile, review_scope, max_chars=12000):
    """Exact mechanical adoption inventory; conditional retention is not a new scientific review."""
    from oracle_atlas.atlas.store import _active_bounds, _bracket_refs, _ineligible
    if not isinstance(max_chars, int) or isinstance(max_chars, bool) or max_chars < 2048:
        raise ValueError("Retained adoption catalog budget must be at least 2048 serialized characters")
    if review_scope.get("setting_id") != profile.get("setting_id"):
        raise ValueError("Retained adoption scope does not bind this setting")
    indexed = {row_id(row, "bounds"): (index, row) for index, row in enumerate(profile.get("bounds", []))}
    if None in indexed or len(indexed) != len(profile.get("bounds", [])):
        raise ValueError("Retained adoption inventory requires unique stable bound IDs")
    active = _active_bounds(profile)
    retained = set(review_scope.get("retained_baseline_bound_ids", []))
    invalidated = set(review_scope.get("invalidated_baseline_bound_ids", []))
    if not active.issubset(indexed) or not retained.issubset(active) or retained & invalidated:
        raise ValueError("Retained adoption inventory contains missing, inactive, or invalidated claims")
    fingerprints = review_scope.get("dependency_sha256", {})
    for bid in retained:
        if fingerprints.get(bid) != _bound_dependency_hash(profile, bid):
            raise ValueError("Retained adoption dependency fingerprint does not match the prepared profile")
        certificate = review_scope.get("retention_certificates", {}).get(bid)
        if review_scope.get("version") == 2 and (not isinstance(certificate, dict)
                or certificate.get("prepared_full_dependency_sha256") != fingerprints[bid]):
            raise ValueError("Retained adoption certificate does not bind the actual prepared dependency fingerprint")
        if review_scope.get("version") == 2:
            indices = certificate.get("projection_reason_indices")
            reasons = review_scope.get("projection_reasons")
            if (not isinstance(reasons, list) or not isinstance(indices, list)
                    or any(type(index) is not int or not 0 <= index < len(reasons) for index in indices)
                    or len(set(indices)) != len(indices)):
                raise ValueError("Retained adoption certificate contains invalid projection-reason indices")
    blocked = {bid for bid in active if _ineligible(indexed[bid][1])}
    adoptable = retained - blocked
    records = []
    formula_fields = ("formula_latex", "formula", "expression_latex", "expression", "rate_latex")
    contract_fields = ("view_id", "guarantee_id", "quantity_ref", "quantity_refs", "quantity_id",
                       "resource_projection_id", "resource_projection_ref", "resource_projection_refs", "region_ref", "region_refs",
                       "lower_scope_type", "witness_type", "algorithm_class_scope")
    eligibility_fields = ("eligible_for_bracket", "included_in_bracket", "status", "adoption_status", "quarantined", "withdrawn", "inapplicable")
    for bid in sorted(adoptable):
        index, row = indexed[bid]
        selected = {"comparisons": [row_id(r, "comparisons") for r in profile.get("comparisons", []) if bid in _bracket_refs(r.get("bracket", {}))],
                    "bracket_rows": [row_id(r, "bracket_rows") for r in profile.get("bracket_rows", []) if bid in _bracket_refs(r)]}
        if "selected_in_regimes" in row:
            selected["selected_in_regimes"] = deepcopy(row["selected_in_regimes"])
        records.append({"id": bid, "prepared_pointer": f"/bounds/{index}", "row_sha256": digest(row),
                        "dependency_sha256": fingerprints[bid], "direction": deepcopy(row.get("direction")),
                        "formula": {k: deepcopy(row[k]) for k in formula_fields if k in row},
                        "contract": {k: deepcopy(row[k]) for k in contract_fields if k in row},
                        "eligibility_flags": {k: deepcopy(row[k]) for k in eligibility_fields if k in row},
                        "selected_refs": selected})
    packet = {"version": 1, "setting_id": profile["setting_id"], "prepared_profile_sha256": digest(profile),
              "native_active_bound_ids": sorted(active), "retained_adoption_ids": sorted(adoptable),
              "fresh_review_required_bound_ids": sorted(active - adoptable), "blocked_ineligible_bound_ids": sorted(blocked),
              "invalidated_baseline_bound_ids": sorted(invalidated), "rows": [],
              "omitted": [{k: row[k] for k in ("id", "prepared_pointer", "row_sha256", "dependency_sha256")} for row in records],
              "incomplete": bool(records), "serialized_character_budget": max_chars,
              "note": "Mechanical native-active and dependency-consistency inventory only. Retained IDs may be preserved under the accepted-baseline premise without rereading old bounds merely to enumerate approvals. This is not a fresh scientific approval; counterevidence or a genuine missing overlap premise requires targeted reads. Omitted row values remain available at exact prepared pointers."}
    def length():
        return len(json.dumps(packet, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    if length() > max_chars:
        raise ValueError("Retained adoption ID/pointer inventory exceeds its budget; increase retained_adoption_catalog_chars")
    for record, omission in zip(records, list(packet["omitted"])):
        packet["omitted"].remove(omission)
        packet["rows"].append(record)
        if length() > max_chars:
            packet["rows"].pop()
            packet["omitted"].append(omission)
    packet["omitted"].sort(key=lambda row: row["id"])
    packet["incomplete"] = bool(packet["omitted"])
    if length() > max_chars:
        raise AssertionError("Retained adoption catalog exceeded its serialized character budget")
    return packet


def review_input_pack(baseline, proposed, delta, max_chars=18000):
    """Bounded exact controller input, with no partial scientific values or invented read traces."""
    if not isinstance(max_chars, int) or isinstance(max_chars, bool) or max_chars < 2048:
        raise ValueError("Review input budget must be at least 2048 serialized characters")
    if baseline.get("setting_id") != proposed.get("setting_id"):
        raise ValueError("Review input profiles must have the same stable setting ID")
    rows, changed = [], []
    for item in delta:
        collection, rid = item["collection"], item["id"]
        current = next(((i, r) for i, r in enumerate(proposed.get(collection, [])) if row_id(r, collection) == rid), None)
        if current is None:
            raise ValueError("Every changed row must exist in the prepared profile")
        index, row = current
        changed.append((collection, index, row))
    ids = {rid for _, _, row in changed for rid in _strings(row)}
    ids |= _strings(proposed.get("common_specification", {}))
    direct_comparisons = [r for r in proposed.get("comparisons", []) if row_id(r, "comparisons") in ids or _strings(r) & {row_id(row, coll) for coll, _, row in changed if coll == "bounds"}]
    for row in direct_comparisons:
        ids |= _strings(row)
    view_ids = {r.get("comparison_key", r).get("view_id") for r in direct_comparisons}
    view_ids |= {r.get("view_id") for coll, _, r in changed if coll == "bounds"}
    for row in proposed.get("views", []):
        if row.get("view_id") in view_ids:
            ids |= _strings(row)
    # Keep explicit regime/quantity/parameter dependency closure, not every old bound or proof.
    scoped_collections = ("regimes", "quantities", "resource_projections", "parameters", "symbols")
    aliases = {"regimes": ("id", "regime_id"), "quantities": ("id", "quantity_id"),
               "resource_projections": ("id", "resource_projection_id"), "parameters": ("id", "parameter_id"), "symbols": ("id", "symbol_id")}
    selected = {}
    while True:
        previous = set(ids)
        for collection in scoped_collections:
            for index, row in enumerate(proposed.get(collection, [])):
                rid = next((row[k] for k in aliases[collection] if k in row), None)
                if rid in ids:
                    selected[(collection, index)] = row
                    ids |= _strings(row)
        if previous == ids:
            break
    def add(artifact, pointer, value, kind, fixed=False):
        rows.append({"artifact": artifact, "pointer": pointer, "content_hash": digest(value),
                     "kind": kind, "fixed_scope": fixed, "value": value})
    add("prepared", "/common_specification", proposed["common_specification"], "common_specification", True)
    for index, row in enumerate(proposed.get("views", [])):
        if row.get("view_id") in view_ids:
            add("prepared", f"/views/{index}", row, "view_with_exact_guarantees", True)
    for collection in scoped_collections:
        for (name, index), row in selected.items():
            if name == collection:
                add("prepared", f"/{collection}/{index}", row, collection, True)
    for collection, index, row in changed:
        add("prepared", f"/{collection}/{index}", row, "changed_" + collection)
    for collection, _, row in changed:
        rid = row_id(row, collection)
        previous = next(((i, r) for i, r in enumerate(baseline.get(collection, [])) if row_id(r, collection) == rid), None)
        if previous is not None:
            add("baseline", f"/{collection}/{previous[0]}", previous[1], "baseline_changed_" + collection)
    unique = {}
    for row in rows:
        unique.setdefault((row["artifact"], row["pointer"]), row)
    rows = list(unique.values())
    packet = {"version": 1, "setting_id": proposed["setting_id"],
              "baseline_profile_sha256": digest(baseline), "prepared_profile_sha256": digest(proposed),
              "immutable_contract_unchanged": all(baseline.get(k) == proposed.get(k) for k in IMMUTABLE),
              "items": [{k: v for k, v in row.items() if k != "value"} for row in rows],
              "catalog_items_total": len(rows), "catalog_incomplete": False,
              "incomplete": False, "fixed_scope_incomplete": False,
              "note": "Exact controller-provided values are initial input, not tool reads or scientific approval. Omitted values require the stated artifact_read pointers. Retain unaffected baseline bounds conditionally; do not recertify every old bound without new counterevidence."}
    for row in packet["items"]:
        row["provided_complete"] = False
    def length():
        return len(json.dumps(packet, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    # If even catalogs exceed the cap, omit explicit records with a visible inventory gap.
    while packet["items"] and length() > max_chars:
        packet["items"].pop()
        packet["catalog_incomplete"] = True
        packet["incomplete"] = packet["fixed_scope_incomplete"] = True
    if length() > max_chars:
        raise ValueError("Review input budget cannot fit its bounded identity and scope metadata")
    for item, row in zip(packet["items"], rows):
        item.update(value=row["value"], provided_complete=True)
        if length() > max_chars:
            item.pop("value")
            item["provided_complete"] = False
    packet["incomplete"] = packet["incomplete"] or any(not item["provided_complete"] for item in packet["items"]) or len(packet["items"]) < len(rows)
    packet["fixed_scope_incomplete"] = packet["fixed_scope_incomplete"] or any(item["fixed_scope"] and not item["provided_complete"] for item in packet["items"])
    if length() > max_chars:
        raise AssertionError("Review packet exceeded its configured serialized character budget")
    return packet

def current_finite_research_audit(host, context, report=None, config=None):
    """Rebuild new operational coverage; never accept an asserted complete flag."""
    if context.get("budgets", {}).get("finite_research_scope") is not True:
        return None
    from .tools import validate_finite_scope_state
    actual_config = config or getattr(host, "config", None) or {"budgets": context.get("budgets", {})}
    return validate_finite_scope_state(host, context, actual_config, report=report)


def finite_review_context(audit, granted_hashes):
    """Pure controller verification inputs; no inherited reading or approval."""
    return {
        "maintenance_role": "reviewer",
        "finite_research_scope_witness": {
            "artifact": "scout_research_scope", "pointer": "", "content_hash": digest(audit),
            "provided_complete": False, "reading_credit": False,
            "note": "Read the full actual scout scope audit; this is an operational witness, not source-reading or scientific approval."},
        "finite_verification_plan": {"routes": [], "source_obligations": [
            {"obligation_id": "review-source-" + sha, "kind": "source_hash", "identifier": sha,
             "required": True, "verification": "primary_text", "record_ids": [],
             "reason": "Independently read this exact granted scout source; the original decisive-source gates remain binding."}
            for sha in sorted(granted_hashes)]}}


def check_scope(report, context, host):
    validate("scout", report)
    if report.get("joint_analysis_reuse") is not None and (report["outcome"] != "no_change" or report.get("joint_analysis_json") is not None):
        raise ValueError("An analysis reference is exclusive with a full body and is available only for no_change")
    for key in ("setting_id", "base_version", "cutoff"):
        if report[key] != context[key]:
            raise ValueError(f"Report does not bind current {key}")
    examined = set(report["scope"]["examined_comparison_ids"])
    expected = set(context["compact_profile"]["comparison_ids"])
    if not examined.issubset(expected):
        raise ValueError("Report refers to an unknown comparison")
    if report["outcome"] == "no_change":
        validate_status_taxonomy(context.get("artifacts", {}).get("baseline", {}))
        if not report["scope"]["queries_complete"] or report["scope"]["unresolved_leads"] or examined != expected:
            raise ValueError("Incomplete scope cannot become a successful no-change check")
        finite = current_finite_research_audit(host, context, report)
        if finite is not None:
            if not finite.get("no_change_eligible") or getattr(host, "budget_exhausted", False):
                raise ValueError("No-change needs its frozen finite scope, all exposed candidates and required sources completed: " + str(finite.get("reasons", []))[:1500])
        else:
            active_searches = [r for r in host.search_log if not r.get("resolved") and not r.get("retired")]
            if not active_searches or getattr(host, "budget_exhausted", False) or getattr(host, "failed", False) or any(r.get("success") is False for r in active_searches):
                raise ValueError("No-change needs an actual bounded search with no exhausted tool budget")
        if any(f["impact"] not in {"no_effect", "incomparable"} for f in report["findings"]):
            raise ValueError("A potential bracket change cannot be reported as no_change")


def check_review(review, context, prepared, report, host):
    validate("reviewer", review)
    for key, value in (("setting_id", context["setting_id"]), ("base_version", context["base_version"]),
                       ("prepared_hash", prepared["bundle_hash"])):
        if review[key] != value:
            raise ValueError(f"Review binds an incorrect {key}")
    material_findings = [f for f in report["findings"] if f["impact"] not in {"no_effect", "incomparable"}]
    affected = set(context.get("affected_comparison_ids", [])) | set().union(*(set(f["comparison_ids"]) for f in material_findings))
    if review["verdict"] == "approve":
        validate_status_taxonomy(prepared.get("files", {}).get("profile.json", {}))
        from .budgeting import require_catalog_projection_reads
        require_catalog_projection_reads(context, host)
        finite = current_finite_research_audit(host, context, report)
        if finite is not None:
            from .evidence_basis import fully_read_frozen_value
            witness = context.get("finite_research_scope_witness", {})
            audit = context.get("artifacts", {}).get("scout_research_scope")
            if (not isinstance(audit, dict) or witness.get("content_hash") != digest(audit)
                    or not fully_read_frozen_value(host, "scout_research_scope", "", audit)):
                raise ValueError("Reviewer must independently read the complete exact scout finite-research audit")
            if not finite.get("finite_scope_complete"):
                raise ValueError("Reviewer verification scope has unfinished required evidence: " + str(finite.get("reasons", []))[:1500])
        if context.get("joint_analysis_hash") is not None:
            from .joint import validate_joint_analysis
            expected_hash = digest(prepared["files"]["profile.json"].get("joint_analysis"))
            if review.get("joint_analysis_hash") != expected_hash or context["joint_analysis_hash"] != expected_hash:
                raise ValueError("Review must bind the exact prepared joint analysis")
            checks = review.get("joint_checks", {})
            expected_checks = {"parameter_roles", "guarded_envelopes", "domain_accounting", "improvement_regions", "provenance", "display_consistency"}
            if set(checks) != expected_checks or any(checks[k] is not True for k in expected_checks):
                raise ValueError("Approval requires all independent joint-synthesis checks")
            if context.get("joint_analysis", {}).get("provided_complete") is False:
                from .evidence_basis import fully_read_frozen_value
                frozen_profile = prepared["files"]["profile.json"]
                if not (fully_read_frozen_value(host, "prepared", "/joint_analysis", frozen_profile["joint_analysis"])
                        or fully_read_frozen_value(host, "prepared", "", frozen_profile)):
                    raise ValueError("Reviewer must actually read every page of the omitted frozen prepared joint analysis")
            validate_joint_analysis(prepared["files"]["profile.json"]["joint_analysis"],
                                    context["artifacts"]["baseline"], prepared["files"]["profile.json"],
                                    report=report, expected_comparison_ids=affected, require_current=True)
        if (getattr(host, "failed", False) and (finite is None or not finite.get("finite_scope_complete"))) or getattr(host, "budget_exhausted", False):
            raise ValueError("An incomplete or failed reviewer session cannot approve publication")
        if hasattr(host, "events") and not any(e.get("tool") == "artifact_read" and
                e.get("arguments", {}).get("name") == "prepared" and
                not e.get("result", {}).get("error") and bool(e.get("result", {}).get("text"))
                for e in host.events):
            raise ValueError("Reviewer must actually read the frozen prepared profile before adoption")
        if review["issues"] or not affected.issubset(set(review["reviewed_comparison_ids"])):
            raise ValueError("Approved review must cover every affected comparison without unresolved issues")
        from .evidence_basis import check_evidence_basis
        baseline = context.get("artifacts", {}).get("baseline", {})
        proposed = prepared.get("files", {}).get("profile.json", {})
        if baseline and proposed:
            scope = maintenance_review_scope(baseline, proposed, report)
            if "review_scope" in context and context["review_scope"] != scope:
                raise ValueError("Review scope no longer matches the exact frozen retention certificate")
            from .evidence_basis import check_retention_read_obligations
            check_retention_read_obligations(scope, baseline, proposed, host, role="reviewer")
        elif report.get("quantity_metadata_normalizations") or "review_scope" in context:
            raise ValueError("Conditional retention requires complete frozen baseline and prepared artifacts")
        if any(f.get("evidence_basis", "primary_source") != "primary_source" for f in material_findings) and not proposed:
            raise ValueError("Baseline-supported review requires complete frozen baseline and prepared profile artifacts")
        check_evidence_basis(report, baseline, proposed, host)
