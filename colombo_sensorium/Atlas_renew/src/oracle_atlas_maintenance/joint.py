"""Joint-parameter bookkeeping, not symbolic mathematics or theorem certification.

The LLM and independent reviewer establish implications, transfers and dominance.
This module checks explicit roles, reference closure, and agreement with native
bracket participation. It never proves a parameter partition by sampling points.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from .state import digest

_REF_LISTS = {"upper_refs", "lower_refs", "achievable_refs", "necessary_refs", "claim_refs", "bound_refs"}
_REF_SINGLE = {"claim_ref", "bound_ref"}
_ID_FIELDS = {"comparisons": ("comparison_id", "id"), "bounds": ("id", "bound_id"),
              "regimes": ("id", "regime_id", "region_id"), "proofs": ("id", "proof_id"),
              "references": ("id", "source_id"), "parameters": ("id", "parameter_id")}


def _id(row, collection):
    return next((row[k] for k in _ID_FIELDS[collection] if k in row), None)


def _index(profile, collection):
    rows = profile.get(collection, [])
    index = {_id(r, collection): r for r in rows}
    if None in index or len(index) != len(rows):
        raise ValueError(f"joint analysis requires unique {collection} IDs")
    return index


def _refs(value):
    result = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in _REF_LISTS:
                if not isinstance(child, list) or any(not isinstance(x, str) for x in child):
                    raise ValueError(f"{key} must be a list of bound IDs")
                result.update(child)
            elif key in _REF_SINGLE:
                if not isinstance(child, str):
                    raise ValueError(f"{key} must be a bound ID")
                result.add(child)
            else:
                result.update(_refs(child))
    elif isinstance(value, list):
        for child in value:
            result.update(_refs(child))
    return result


def _brackets(profile, comparison):
    records = [comparison.get("bracket", {})]
    cid = _id(comparison, "comparisons")
    for row in profile.get("bracket_rows", []):
        if row.get("comparison_ref", row.get("comparison_id")) == cid or cid in row.get("comparison_ids", []):
            records.append(row)
    return records


def _selected(profile, comparison):
    return set().union(*(_refs(row) for row in _brackets(profile, comparison)))


def _side_refs(value, side):
    result = set()
    names = {"upper_refs", "achievable_refs"} if side == "upper" else {"lower_refs", "necessary_refs"}
    if isinstance(value, dict):
        for key, child in value.items():
            if key in names:
                result.update(child)
            elif key == "envelopes" and isinstance(child, dict):
                result.update(_refs(child.get(side)))
            else:
                result.update(_side_refs(child, side))
    elif isinstance(value, list):
        for child in value:
            result.update(_side_refs(child, side))
    return result


def _key(comparison):
    return comparison.get("comparison_key", comparison)


def _ineligible(bound):
    status = bound.get("status")
    status = status.get("code") if isinstance(status, dict) else status
    return (bound.get("eligible_for_bracket") is False or status in {"quarantined", "withdrawn", "ineligible"}
            or any(bound.get(k) is True for k in ("quarantined", "withdrawn", "inapplicable")))


def _eligible(bound):
    status = bound.get("status")
    status = status.get("code") if isinstance(status, dict) else status
    return not _ineligible(bound) and (bound.get("eligible_for_bracket") is True
        or bound.get("included_in_bracket") is True or status in {"active", "accepted", "adopted"})


def _quantities(bound):
    values = set(bound.get("quantity_refs", []))
    value = bound.get("quantity_id", bound.get("quantity_ref"))
    if value is not None:
        values.add(value)
    return values


def _resource_ids(bound):
    values = set(bound.get("resource_projection_refs", []))
    value = bound.get("resource_projection_id", bound.get("resource_projection_ref"))
    if value is not None:
        values.add(value)
    return values


def _conflicts(bound, comparison):
    key = _key(comparison)
    result = [field for field in ("view_id", "guarantee_id")
              if bound.get(field) is not None and bound.get(field) != key.get(field)]
    quantities = _quantities(bound)
    resources = _resource_ids(bound)
    if quantities and key.get("quantity_id") not in quantities:
        result.append("quantity_id")
    if resources and key.get("resource_projection_id") not in resources:
        result.append("resource_projection_id")
    return result


def _candidates(profile, comparison):
    """Conservative inventory; missing resource metadata does not prove compatibility."""
    key = _key(comparison)
    return {bid for bid, bound in _index(profile, "bounds").items()
        if _eligible(bound) and bound.get("view_id") == key.get("view_id")
        and bound.get("guarantee_id") == key.get("guarantee_id")
        and key.get("quantity_id") in _quantities(bound) and not _conflicts(bound, comparison)}


def _predicate(profile, comparison):
    if comparison.get("predicate_text"):
        return comparison["predicate_text"]
    rid = _key(comparison).get("regime_id")
    row = _index(profile, "regimes").get(rid, {})
    return row.get("predicate_text", "UNASSESSED: comparison region has no readable predicate")


def _validity(profile, bound):
    regions = _index(profile, "regimes")
    refs = bound.get("region_refs", bound.get("regime_ids", []))
    texts = [regions[r].get("predicate_text", r) for r in refs if r in regions]
    parts = ["Referenced regions: (" + ") OR (".join(texts) + ")"] if texts else []
    applicability = bound.get("applicability")
    conditions = applicability.get("conditions") if isinstance(applicability, dict) else applicability
    for value in (conditions, bound.get("conditions")):
        if value:
            items = value if isinstance(value, list) else [value]
            parts.extend("(" + _text(item) + ")" for item in items)
    return " AND ".join(parts) or "UNASSESSED: read bound conditions and source theorem"


def _adopted_region(profile, comparison, bound):
    """Preserve explicit restrictions; never replace a narrow guard by its parent region."""
    parts = ["Comparison region: (" + _predicate(profile, comparison) + ")",
             "Bound validity: (" + _validity(profile, bound) + ")"]
    bid = _id(bound, "bounds")
    for bracket in _brackets(profile, comparison):
        guards = bracket.get("claim_guards", {}).get(bid)
        if guards:
            parts.append("Native claim-guard declaration (retain its branch semantics): " + _text(guards))
    return " AND ".join(parts)


def _envelope(comparison, side):
    bracket = comparison.get("bracket", {})
    entry = (bracket.get("envelopes") or {}).get(side, {})
    if isinstance(entry, str):
        return entry
    if not isinstance(entry, dict):
        return "UNASSESSED: no recorded " + side + " envelope"
    for field in ("expression_latex", "expression", "formula_latex", "formula"):
        if isinstance(entry.get(field), str):
            return entry[field]
    return "UNASSESSED: no recorded " + side + " envelope"


def _text(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)


def analysis_template(profile, *, version=1):
    """Return an honest draft; copying an old bracket is not a new review."""
    bounds = _index(profile, "bounds")
    comparisons, cells, used = [], [], set()
    for comparison in profile.get("comparisons", []):
        cid = _id(comparison, "comparisons")
        selected = _selected(profile, comparison)
        candidates = _candidates(profile, comparison) | selected
        predicate = _predicate(profile, comparison)
        uses = []
        for bid in sorted(candidates):
            bound = bounds.get(bid, {})
            uses.append({"bound_id": bid, "disposition": "included" if bid in selected else "unresolved",
                "validity_region": _validity(profile, bound),
                "adopted_region": _adopted_region(profile, comparison, bound) if bid in selected else "Not yet adopted in this comparison",
                "reason": "Copied from the accepted baseline; applicability and envelope overlap are not recertified."
                          if bid in selected else "Eligible same-contract candidate requires an explicit inclusion or exclusion judgment.",
                "mapping_proof_refs": []})
        used.update(selected)
        bracket = comparison.get("bracket", {})
        fixed = [str(x) for x in bracket.get("fixed_parameters", [])]
        role = "slice" if fixed else "joint"
        comparisons.append({"comparison_id": cid, "role": role,
            "slice": predicate if role == "slice" else None, "fixed_parameters": fixed,
            "constant_dependencies": [], "bound_uses": uses,
            "upper_envelope": _envelope(comparison, "upper"), "lower_envelope": _envelope(comparison, "lower"),
            "gap": _text(bracket.get("ratio_or_gap", "UNASSESSED")),
            "boundary_checks": ["UNASSESSED: endpoints, source guards, saturation and dominance crossovers"],
            "remaining_gap": "Copied bracket does not establish global optimality or a literature-open problem."})
        envelope_rows = bracket.get("envelopes") or {}
        upper = bool(bracket.get("upper_refs") or bracket.get("achievable_refs") or _refs(envelope_rows.get("upper")))
        lower = bool(bracket.get("lower_refs") or bracket.get("necessary_refs") or _refs(envelope_rows.get("lower")))
        state = "bounds_recorded" if upper and lower else "missing_lower" if upper else "missing_upper" if lower else "missing_both"
        cells.append({"cell_id": "existing-" + cid, "predicate": predicate,
            "role": "slice" if role == "slice" else "joint_region", "comparison_ids": [cid],
            "state": state, "note": "Existing registered region; overlaps and the target-domain complement remain unassessed."})
    provenance = []
    source_ids = set(_index(profile, "references"))
    proof_ids = set(_index(profile, "proofs"))
    for bid in sorted(used & set(bounds)):
        bound = bounds[bid]
        provenance.append({"bound_id": bid, "origin": "retained_baseline",
            "source_refs": [r for r in bound.get("source_refs", []) if r in source_ids],
            "proof_refs": [r for r in bound.get("proof_refs", []) if r in proof_ids],
            "source_locator": "Read retained evidence/proof records; not independently reverified by this template",
            "source_domain": "UNASSESSED: distinguish original theorem from target-domain transfer",
            "target_domain": _validity(profile, bound),
            "mapping": "Conditional baseline retention only; no new source theorem or transfer is asserted."})
    result = {"version": 1,
        "target": {"joint_variables": [], "normalized_variables": [], "fixed_parameters": [],
            "uniform_in": [], "allowed_constant_dependencies": [],
            "full_domain": "UNASSESSED: derive the full parameter domain from the immutable mathematical contract",
            "contract_refs": ["/common_specification", "/parameters", "/quantities", "/views", "/resource_projections"],
            "resolution": "normalization_required"},
        "domain_map": {"status": "unknown", "cells": cells,
            "residual_domain": "Full target domain minus the union of the recorded joint regions; not yet characterized",
            "partition_argument": "UNASSESSED: copying existing comparisons does not establish a partition"},
        "comparisons": comparisons, "provenance": provenance, "impact": [],
        "normalization_requests": [{"path": "/quantities", "issue": "Joint variables, fixed structure and hidden-constant roles require explicit resolution",
            "proposed_resolution": "Resolve roles against the fixed contract; never silently rewrite a view, guarantee, resource or quantity",
            "changes_mathematical_contract": False}],
        "pending_obligations": ["Resolve the joint-parameter target and uniformity convention.",
            "Assess compatible-bound participation, source validity versus actual improvement, endpoints and uncovered regions."]}
    if version == 2:
        result["version"] = 2
        for cell in result["domain_map"]["cells"]:
            cell.update(closure="not_claimed", publication="unassessed", closure_proof_refs=[])
        result["synthesis_coverage"] = synthesis_template(profile, profile)
        for index, lead in enumerate(result["pending_obligations"]):
            result["synthesis_coverage"]["obligations"].append({
                "id": "draft-lead-" + str(index), "kind": "material_lead",
                "comparison_ids": sorted(_index(profile, "comparisons")), "bound_refs": [], "cell_ids": [],
                "state": "pending", "affects_gap": True, "lead": lead,
                "argument": "UNASSESSED: the draft does not resolve this obligation.", "proof_refs": []})
    elif version != 1:
        raise ValueError("Unsupported joint-analysis template version")
    return result


def synthesis_catalog(profile, comparison_ids=None, max_chars=10000, *, artifact="baseline"):
    """Bounded exact objects with pointers and hashes; never truncates an object."""
    if not isinstance(max_chars, int) or isinstance(max_chars, bool) or max_chars < 2048:
        raise ValueError("Synthesis catalogue budget must be at least 2048 characters")
    if artifact not in {"baseline", "prepared"}:
        raise ValueError("Synthesis catalogue artifact must be baseline or prepared")
    indexed = _index(profile, "comparisons")
    wanted = set(indexed) if comparison_ids is None else set(comparison_ids)
    if not wanted.issubset(indexed):
        raise ValueError("Synthesis catalogue has unknown comparison IDs")
    selected_bounds = set()
    for cid in wanted:
        selected_bounds |= _selected(profile, indexed[cid]) | _candidates(profile, indexed[cid])
    if not selected_bounds.issubset(_index(profile, "bounds")):
        raise ValueError("Synthesis catalogue cannot resolve a selected bound ID")
    records = []
    for collection, wanted_ids in (("comparisons", wanted), ("bounds", selected_bounds)):
        for index, row in enumerate(profile.get(collection, [])):
            rid = _id(row, collection)
            if rid not in wanted_ids:
                continue
            record = {"kind": collection, "id": rid, "artifact": artifact, "pointer": f"/{collection}/{index}", "content_hash": digest(row), "value": row}
            if collection == "comparisons":
                record["selected_bound_ids"] = sorted(_selected(profile, row))
                record["candidate_bound_ids"] = sorted(_candidates(profile, row))
            records.append(record)
    packet = {"version": 1, "setting_id": profile["setting_id"], "artifact": artifact, "profile_sha256": digest(profile),
        "requested_comparison_count": len(wanted), "candidate_bound_count": len(selected_bounds),
        "items": [], "omitted": [], "omitted_inventory": [], "incomplete": False,
        "note": "Mechanical candidate inventory only; missing resource metadata is not evidence of compatibility. Exact complete objects are included or omitted, never truncated. Inclusion/exclusion and mathematical guards require review."}
    # Reserve space for array-level fallback pointers if individual omission records exceed budget.
    reserve = 900
    for record in records:
        packet["items"].append(record)
        if len(json.dumps(packet, ensure_ascii=False)) <= max_chars - reserve:
            continue
        packet["items"].pop()
        packet["incomplete"] = True
        omitted = {k: record[k] for k in ("kind", "id", "artifact", "pointer", "content_hash")}
        packet["omitted"].append(omitted)
        if len(json.dumps(packet, ensure_ascii=False)) > max_chars - reserve:
            packet["omitted"].pop()
            collection = record["kind"]
            group = next((r for r in packet["omitted_inventory"] if r["kind"] == collection), None)
            if group is None:
                group = {"kind": collection, "artifact": artifact, "pointer": "/" + collection,
                    "content_hash": digest(profile.get(collection, [])), "unlisted_omission_count": 0,
                    "note": "Read the exact parent array by pagination; catalogue does not enumerate all omitted IDs."}
                packet["omitted_inventory"].append(group)
            group["unlisted_omission_count"] += 1
    if len(json.dumps(packet, ensure_ascii=False)) > max_chars:
        raise ValueError("Catalogue budget cannot fit its bounded metadata")
    return deepcopy(packet)


def _unique(rows, field, label):
    ids = [row[field] for row in rows]
    if len(set(ids)) != len(ids):
        raise ValueError(f"Duplicate {label} IDs")
    return set(ids)


def _pointer_exists(profile, pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        return False
    value = profile
    try:
        for part in pointer[1:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            value = value[int(part)] if isinstance(value, list) else value[part]
        return True
    except (KeyError, IndexError, TypeError, ValueError):
        return False


def joint_scope_complete(analysis):
    """Bookkeeping completion, never a claim of solved science or complete literature."""
    return (analysis.get("target", {}).get("resolution") == "resolved"
        and analysis.get("domain_map", {}).get("status") == "accounted"
        and bool(analysis.get("target", {}).get("joint_variables"))
        and not analysis.get("normalization_requests") and not analysis.get("pending_obligations")
        and not any(u.get("disposition") == "unresolved" for c in analysis.get("comparisons", []) for u in c.get("bound_uses", []))
        and (analysis.get("version") != 2 or synthesis_scope_complete(analysis)))


def synthesis_requirements(baseline, proposed, comparison_ids=None):
    """Return bounded review opportunities, never inferred mathematical transfers.

    The declared comparison scope selects candidate/withdrawal checks. New,
    changed or newly used claims also expose possible projections to other
    same-view/guarantee comparisons. A different resource ID triggers an
    obligation to judge a map, not permission to identify quantities or combine
    different algorithms.
    """
    comparisons = _index(proposed, "comparisons")
    old_comparisons = _index(baseline, "comparisons")
    bounds, old_bounds = _index(proposed, "bounds"), _index(baseline, "bounds")
    scope = set(comparisons) if comparison_ids is None else set(comparison_ids)
    if not scope.issubset(comparisons):
        raise ValueError("Synthesis requirements reference an unknown comparison")
    rows = []
    def add(kind, cid, bids):
        rows.append({"kind": kind, "comparison_ids": [cid], "bound_refs": sorted(bids)})
    fresh = {bid for bid, bound in bounds.items() if _eligible(bound)
             and (bid not in old_bounds or digest(bound) != digest(old_bounds[bid]))}
    for cid in sorted(scope):
        comparison = comparisons[cid]
        selected = _selected(proposed, comparison)
        add("compatible_candidates", cid, selected | _candidates(proposed, comparison))
        previous = old_comparisons.get(cid)
        if previous:
            old_selected = _selected(baseline, previous)
            for bid in sorted(old_selected):
                if bid in old_bounds and _eligible(old_bounds[bid]) and (bid not in selected or bid not in bounds or _ineligible(bounds[bid])):
                    add("replacement_branch", cid, {bid})
            fresh |= selected - old_selected
        else:
            fresh |= selected
    for bid in sorted(fresh):
        bound = bounds.get(bid)
        if bound is None:
            continue
        # A component claim may affect a sum/joint resource even if its native
        # comparison was not edited.  Only flag a review opportunity; never
        # project or identify the distinct resources automatically.
        for cid in sorted(comparisons):
            comparison = comparisons[cid]
            key = _key(comparison)
            if (bound.get("view_id") == key.get("view_id")
                    and bound.get("guarantee_id") == key.get("guarantee_id")
                    and set(_conflicts(bound, comparison)) & {"quantity_id", "resource_projection_id"}):
                add("resource_projection", cid, {bid})
    return rows


def synthesis_template(baseline, proposed, comparison_ids=None):
    """Unassessed plan for authors; no generated row is a resolved proof."""
    scope = sorted(_index(proposed, "comparisons") if comparison_ids is None else comparison_ids)
    while True:
        requirements = synthesis_requirements(baseline, proposed, scope)
        expanded = sorted(set(scope) | {cid for row in requirements for cid in row["comparison_ids"]})
        if expanded == scope:
            break
        scope = expanded
    return {"status": "unassessed", "comparison_ids": scope, "gap_basis": "registered_envelope",
            "literature": {"status": "not_assessed", "scope": "No finite literature scope assessed yet."},
            "obligations": [{"id": "synthesis-" + str(index), **row, "cell_ids": [], "state": "pending",
                "affects_gap": True, "lead": None, "argument": "UNASSESSED: independently judge this synthesis obligation.",
                "proof_refs": []} for index, row in enumerate(requirements)]}


def synthesis_scope_complete(analysis):
    coverage = analysis.get("synthesis_coverage", {})
    return (analysis.get("version") == 2 and coverage.get("status") == "complete"
            and not any(row.get("state") == "pending" for row in coverage.get("obligations", [])))


def validate_synthesis_coverage(analysis, baseline, proposed, report=None,
                                expected_comparison_ids=None, *, require_current=False):
    """Validate a declared synthesis audit, not theorem truth or set nonemptiness.

    Legacy analyses remain readable and explicitly unknown at this layer. New
    live handoffs must use the current structured format. Resolved proof/witness text is an assertion for the
    independent reviewer, never something this structural check has solved.
    """
    if analysis.get("version") != 2:
        if require_current:
            raise ValueError("New maintenance assessments require joint-analysis version 2 synthesis coverage")
        return {"status": "legacy_unknown", "gap_basis": "registered_envelope",
                "literature_status": "not_assessed", "domain_extension_claims": [],
                "limitations": "Legacy synthesis and impact claims are not newly confirmed."}
    coverage = analysis["synthesis_coverage"]
    comparisons, bounds = _index(proposed, "comparisons"), _index(proposed, "bounds")
    old_bounds, old_comparisons = _index(baseline, "bounds"), _index(baseline, "comparisons")
    proofs = _index(proposed, "proofs")
    cells = {row["cell_id"]: row for row in analysis["domain_map"]["cells"]}
    scope = set(coverage["comparison_ids"])
    expected = set(comparisons) if expected_comparison_ids is None else set(expected_comparison_ids)
    if not scope.issubset(comparisons) or not expected.issubset(scope):
        raise ValueError("Synthesis coverage must include the affected comparison scope")
    obligations = coverage["obligations"]
    _unique(obligations, "id", "synthesis obligation")
    for row in obligations:
        if (not set(row["comparison_ids"]).issubset(comparisons)
                or not set(row["bound_refs"]).issubset(set(bounds) | set(old_bounds))
                or not set(row["cell_ids"]).issubset(cells)
                or not set(row["proof_refs"]).issubset(proofs)):
            raise ValueError("Synthesis obligation has an unknown native reference")
        if not row["argument"].strip() or (row["lead"] is not None and not row["lead"].strip()):
            raise ValueError("Synthesis obligation needs a substantive judgment or explicit pending lead")
        if row["state"] == "pending" and not analysis["pending_obligations"]:
            raise ValueError("Pending structured synthesis must also remain visible in pending_obligations")
    for requirement in synthesis_requirements(baseline, proposed, scope):
        if not set(requirement["comparison_ids"]).issubset(scope):
            raise ValueError("Synthesis coverage must include comparisons with a new resource-projection opportunity")
        if not any(row["kind"] == requirement["kind"]
                   and set(requirement["comparison_ids"]).issubset(row["comparison_ids"])
                   and set(requirement["bound_refs"]).issubset(row["bound_refs"]) for row in obligations):
            raise ValueError("Missing structured synthesis obligation: " + requirement["kind"])
    leads = set(analysis["pending_obligations"])
    if report is not None:
        leads.update(report.get("scope", {}).get("unresolved_leads", []))
    recorded_leads = {row["lead"] for row in obligations if row["kind"] == "material_lead"}
    if not leads.issubset(recorded_leads):
        raise ValueError("Every remaining textual lead must have a structured material_lead obligation")
    if any(row["lead"] in leads and row["state"] != "pending" for row in obligations):
        raise ValueError("An unresolved lead cannot be marked resolved or inapplicable")
    unpublished = []
    for cell in cells.values():
        if cell["closure"] != "established":
            if cell["publication"] != "unassessed":
                raise ValueError("Unclaimed closure must keep its closure publication unassessed")
            if cell["closure_proof_refs"]:
                raise ValueError("Unclaimed closure cannot carry a closure proof certificate")
            continue
        if not cell["closure_proof_refs"] or not set(cell["closure_proof_refs"]).issubset(proofs):
            raise ValueError("Established closure requires explicit native proof references")
        if cell["publication"] == "native_comparison":
            if not cell["comparison_ids"] or any(comparisons[cid].get("status", {}).get("code") != "optimal"
                                                 for cid in cell["comparison_ids"]):
                raise ValueError("Native closed cell must link its optimal native comparisons")
        elif cell["publication"] == "unpublished":
            unpublished.append(cell["cell_id"])
            if not any(row["kind"] == "closed_region_publication" and cell["cell_id"] in row["cell_ids"]
                       and row["state"] == "pending" and row["affects_gap"] for row in obligations):
                raise ValueError("Unpublished established closure needs a pending publication obligation")
        else:
            raise ValueError("Established closure must be published or explicitly unpublished")
    newly_closed = {cid for cid, row in comparisons.items() if row.get("status", {}).get("code") == "optimal"
                    and (cid not in old_comparisons or digest(row) != digest(old_comparisons[cid]))}
    represented_closed = {cid for cell in cells.values() if cell["closure"] == "established"
                          and cell["publication"] == "native_comparison" for cid in cell["comparison_ids"]}
    if not newly_closed.issubset(represented_closed):
        raise ValueError("Newly closed native comparisons require explicit published closure cells")
    confirmed = []
    for impact in analysis["impact"]:
        witness = impact.get("extension_witness")
        if impact["kind"] == "domain_extension":
            if not isinstance(witness, dict) or not witness["proof_refs"] or not set(witness["proof_refs"]).issubset(proofs):
                raise ValueError("Confirmed domain extension requires an explicit old-domain-exterior witness and native proof")
            if any(not witness[field].strip() for field in ("old_domain", "new_domain", "outside_old_witness", "outside_old_argument")):
                raise ValueError("Domain extension must state old/new regions and justify a nonempty old-domain-exterior witness")
            confirmed.append(impact["finding_id"])
        elif witness is not None:
            raise ValueError("Only a claimed strict domain extension may carry extension_witness")
    pending = [row["id"] for row in obligations if row["state"] == "pending"]
    if coverage["status"] == "complete" and (pending or leads or unpublished):
        raise ValueError("Fully synthesized coverage cannot contain pending leads or unpublished closure")
    if report is not None and coverage["literature"]["status"] == "finite_scope_complete":
        if not report.get("scope", {}).get("queries_complete") or report["scope"].get("unresolved_leads"):
            raise ValueError("Finite literature coverage must agree with the actual finished research scope")
    if report and report.get("outcome") == "no_change" and coverage["literature"]["status"] != "finite_scope_complete":
        raise ValueError("No-change requires explicit finite literature coverage, not a global completeness claim")
    if report and report.get("outcome") == "no_change" and not synthesis_scope_complete(analysis):
        raise ValueError("No-change cannot claim a completed check with unfinished synthesis")
    return {"status": coverage["status"], "gap_basis": coverage["gap_basis"],
            "literature_status": coverage["literature"]["status"], "pending_obligations": pending,
            "pending_gap_obligations": [row["id"] for row in obligations if row["state"] == "pending" and row["affects_gap"]],
            "unpublished_closed_cells": unpublished, "domain_extension_claims": confirmed,
            "limitations": "Reference and publication checks only; the reviewer must prove transfers, dominance, witness membership and nonemptiness."}


def validate_joint_analysis(analysis, baseline, proposed, report=None, expected_comparison_ids=None, *, require_current=False):
    """Raise ValueError on mechanical errors; return a non-certifying diagnostic."""
    schema = json.loads((Path(__file__).parent / "resources" / "joint_analysis.schema.json").read_text("utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(analysis), key=lambda e: str(list(e.path)))
    if errors:
        raise ValueError("Invalid joint analysis at " + "/".join(map(str, errors[0].path)) + ": " + errors[0].message)
    if baseline.get("setting_id") != proposed.get("setting_id"):
        raise ValueError("Joint analysis must bind one setting")
    comparisons, bounds = _index(proposed, "comparisons"), _index(proposed, "bounds")
    old_comparisons, old_bounds = _index(baseline, "comparisons"), _index(baseline, "bounds")
    proofs, sources, parameters = _index(proposed, "proofs"), _index(proposed, "references"), _index(proposed, "parameters")
    target = analysis["target"]
    alias_options = {pid: {pid} for pid in parameters}
    for pid, parameter in parameters.items():
        for value in (pid, parameter.get("symbol"), parameter.get("source_parameter_id")):
            if isinstance(value, str):
                # Canonical IDs always identify themselves; a display alias cannot shadow one.
                if value not in parameters:
                    alias_options.setdefault(value, set()).add(pid)
    # A fixed native identity must use a literal native alias. New normalized
    # coordinates below cannot turn their symbols into aliases for native refs.
    native_alias_options = {name: frozenset(options) for name, options in alias_options.items()}
    aliases = {name: next(iter(options)) for name, options in alias_options.items() if len(options) == 1}
    ambiguous = {name for name, options in alias_options.items() if len(options) > 1}
    for row in target["normalized_variables"]:
        if not set(row["parameter_refs"]).issubset(parameters):
            raise ValueError("Normalized variable references an unknown parameter")
        if target["resolution"] == "resolved" and row["symbol"] in aliases:
            original = parameters.get(aliases[row["symbol"]], {})
            if original and original.get("kind", "independent") != "derived":
                raise ValueError("A normalization cannot redefine a declared independent parameter symbol")
        if row["symbol"] not in aliases:
            aliases[row["symbol"]] = row["symbol"]
    _unique(target["normalized_variables"], "symbol", "normalized variable")
    _unique(target["fixed_parameters"], "symbol", "fixed parameter")
    if target["resolution"] == "resolved" and any(x not in aliases and x not in ambiguous for x in target["joint_variables"]):
        raise ValueError("Resolved joint variable must identify a declared or explicitly normalized parameter")
    def canonical(values):
        if target["resolution"] == "resolved" and set(values) & ambiguous:
            raise ValueError("Ambiguous parameter alias; use canonical parameter IDs")
        return {aliases.get(x, x) for x in values}
    joint = canonical(target["joint_variables"])
    if target["resolution"] == "resolved" and not joint.issubset(canonical(target["uniform_in"])):
        raise ValueError("Resolved target must explicitly require uniformity in every joint variable")
    fixed = set()
    for row in target["fixed_parameters"]:
        ref = row["parameter_ref"]
        if ref is not None and ref not in parameters:
            raise ValueError("Fixed parameter references an unknown parameter")
        if ref is not None:
            owners = native_alias_options.get(row["symbol"])
            if owners is None:
                raise ValueError("Fixed parameter symbol must be an exact native alias for its parameter_ref")
            if len(owners) != 1:
                raise ValueError("Ambiguous fixed parameter alias; use its canonical parameter ID")
            if ref not in owners:
                raise ValueError("Fixed parameter symbol disagrees with its explicit parameter_ref")
        fixed.add(ref or aliases.get(row["symbol"], row["symbol"]))
    if joint & fixed:
        raise ValueError("A parameter cannot be both joint and fixed")
    if canonical(target["allowed_constant_dependencies"]) & (joint | canonical(target["uniform_in"])):
        raise ValueError("A joint or uniform parameter cannot be hidden in constants")
    if not canonical(target["allowed_constant_dependencies"]).issubset(fixed):
        raise ValueError("Allowed constant dependencies must be explicitly fixed parameters")
    if target["resolution"] == "resolved" and (not joint or not target["full_domain"].strip()):
        raise ValueError("Resolved target needs nonempty joint variables and full domain")
    if any(not _pointer_exists(proposed, ref) for ref in target["contract_refs"]):
        raise ValueError("Joint target has an invalid contract pointer")
    for request in analysis["normalization_requests"]:
        if not _pointer_exists(proposed, request["path"]):
            raise ValueError("Normalization request must point to existing profile data")
    if target["resolution"] == "resolved" and analysis["normalization_requests"]:
        raise ValueError("Unresolved normalization requests cannot have a resolved target")
    actual = _unique(analysis["comparisons"], "comparison_id", "analysis comparison")
    expected = set(comparisons) if expected_comparison_ids is None else set(expected_comparison_ids)
    if report and report.get("outcome") == "no_change":
        expected = set(comparisons)
    if not expected.issubset(comparisons) or not actual.issubset(comparisons) or not expected.issubset(actual):
        raise ValueError("Joint analysis does not cover the expected comparison IDs")
    warnings = []
    used_ids = set()
    for row in analysis["comparisons"]:
        cid = row["comparison_id"]
        comparison = comparisons[cid]
        uses = {u["bound_id"]: u for u in row["bound_uses"]}
        _unique(row["bound_uses"], "bound_id", "bound use")
        selected = _selected(proposed, comparison)
        if not selected.issubset(bounds) or not set(uses).issubset(bounds):
            raise ValueError("Joint analysis references an unknown bound")
        if not (selected | _candidates(proposed, comparison)).issubset(uses):
            raise ValueError("Every selected and compatible eligible bound must be accounted for")
        included = {bid for bid, use in uses.items() if use["disposition"] == "included"}
        if included != selected:
            raise ValueError("Included bound uses must equal native bracket participants")
        if row["role"] == "slice" and not row["slice"]:
            raise ValueError("Slice comparison requires an explicit slice relation")
        if row["role"] == "joint" and row["slice"] is not None:
            raise ValueError("A joint comparison cannot silently contain a fixed-precision slice")
        local_fixed = canonical(row["fixed_parameters"])
        if row["role"] == "joint" and local_fixed & joint:
            raise ValueError("Joint comparison fixes a target joint variable")
        native_fixed = [x for x in comparison.get("bracket", {}).get("fixed_parameters", []) if isinstance(x, str)]
        if target["resolution"] == "resolved" and row["role"] == "joint" and canonical(native_fixed) & joint:
            raise ValueError("Native fixed-parameter slice cannot be relabelled as a joint comparison")
        allowed = canonical(target["allowed_constant_dependencies"]) | local_fixed
        if not canonical(row["constant_dependencies"]).issubset(allowed):
            raise ValueError("Comparison hides an undeclared parameter in constants")
        if row["role"] == "joint" and canonical(row["constant_dependencies"]) & joint:
            raise ValueError("Joint comparison hides a joint parameter in constants")
        for bid, use in uses.items():
            if not set(use["mapping_proof_refs"]).issubset(proofs):
                raise ValueError("Bound use has an unknown mapping proof")
            if any(not use[field].strip() for field in ("validity_region", "adopted_region", "reason")):
                raise ValueError("Every bound disposition requires validity, adopted region and justification")
            if bid not in included:
                continue
            bound = bounds[bid]
            if _ineligible(bound):
                raise ValueError("Ineligible bound cannot enter a joint envelope")
            conflict = _conflicts(bound, comparison)
            if conflict and not use["mapping_proof_refs"]:
                unchanged = (cid in old_comparisons and bid in old_bounds
                    and digest(bound) == digest(old_bounds[bid])
                    and _key(comparison) == _key(old_comparisons[cid])
                    and bid in _selected(baseline, old_comparisons[cid]))
                if not (unchanged and analysis["normalization_requests"] and analysis["pending_obligations"]):
                    raise ValueError("Included cross-contract bound needs an explicit mapping proof")
                warnings.append(f"{cid}/{bid}: unresolved retained legacy contract mismatch ({', '.join(conflict)})")
        for side in ("upper", "lower"):
            side_ids = set().union(*(_side_refs(row, side) for row in _brackets(proposed, comparison)))
            for bid in side_ids:
                directions = {side, "achievable" if side == "upper" else "necessary", "both", "exact", "two_sided_statement", None}
                if bid in bounds and bounds[bid].get("direction") not in directions:
                    raise ValueError("Bound direction disagrees with its envelope side")
        used_ids |= included
    _unique(analysis["domain_map"]["cells"], "cell_id", "domain cell")
    represented = set()
    for cell in analysis["domain_map"]["cells"]:
        if not set(cell["comparison_ids"]).issubset(comparisons):
            raise ValueError("Domain cell references an unknown comparison")
        represented.update(cell["comparison_ids"])
        if cell["role"] == "unassessed" and cell["state"] != "unassessed":
            raise ValueError("An unassessed domain cell cannot assert assessed bounds")
    domain = analysis["domain_map"]
    if domain["status"] == "accounted" and (not expected.issubset(represented)
            or not domain["partition_argument"].strip() or not domain["residual_domain"].strip()):
        raise ValueError("Accounted domain requires cells, explicit residual and partition argument")
    provenance_ids = _unique(analysis["provenance"], "bound_id", "provenance")
    if not provenance_ids.issubset(bounds):
        raise ValueError("Provenance references an unknown bound")
    for item in analysis["provenance"]:
        if not set(item["source_refs"]).issubset(sources) or not set(item["proof_refs"]).issubset(proofs):
            raise ValueError("Provenance references an unknown source or proof")
        if item["origin"] == "source_theorem" and not item["source_refs"]:
            raise ValueError("Source theorem provenance requires an actual source reference")
        if item["origin"] in {"subclass_transfer", "oracle_reduction", "analyst_derivation"} and not item["proof_refs"]:
            raise ValueError("Transferred or analyst-derived claim requires an explicit proof record")
        if any(not item[field].strip() for field in ("source_locator", "source_domain", "target_domain", "mapping")):
            raise ValueError("Provenance must state source locator, source domain, target domain and mapping")
    impacts = {i["finding_id"]: i for i in analysis["impact"]}
    _unique(analysis["impact"], "finding_id", "impact")
    for item in impacts.values():
        if not set(item["comparison_ids"]).issubset(comparisons):
            raise ValueError("Impact references an unknown comparison")
        if item["kind"] == "bound_improvement" and any(not item[k].strip() for k in
                ("old_envelope", "new_envelope", "improvement_region", "witness", "argument")):
            raise ValueError("Bound improvement requires old/new envelopes, improvement domain, witness and argument")
    if report and report.get("outcome") == "candidate_change":
        from oracle_atlas.atlas.store import _active_bounds
        from .delta_classification import classify_delta
        adoption_only = set(classify_delta(baseline, proposed, report)["adoption_only_bound_ids"])
        # Native publication adopts every eligible/active claim, not only displayed participants.
        fresh = {bid for bid in _active_bounds(proposed)
                 if bid in bounds and (bid not in old_bounds or digest(bounds[bid]) != digest(old_bounds[bid]))}
        if not fresh.issubset(provenance_ids):
            raise ValueError("Changed adopted bounds require provenance")
        for item in analysis["provenance"]:
            if item["bound_id"] in fresh and item["origin"] == "retained_baseline" and item["bound_id"] not in adoption_only:
                raise ValueError("Changed bound cannot claim unchanged-baseline provenance")
        for finding in report.get("findings", []):
            if finding.get("impact") in {"no_effect", "incomparable"}:
                continue
            impact = impacts.get(finding["candidate_id"])
            if not finding.get("comparison_ids"):
                raise ValueError("Material finding requires a nonempty comparison scope")
            if impact is None or not set(finding.get("comparison_ids", [])).issubset(impact["comparison_ids"]):
                raise ValueError("Every material finding requires a scoped impact explanation")
            if impact["kind"] == "no_effect":
                raise ValueError("Material finding cannot disappear into a no_effect impact")
    synthesis = validate_synthesis_coverage(analysis, baseline, proposed, report, expected_comparison_ids, require_current=require_current)
    return {"valid": True, "joint_scope_complete": joint_scope_complete(analysis),
        "comparison_ids": sorted(actual), "warnings": warnings, "synthesis_coverage": synthesis,
        "limitations": "Structural checks only. Source interpretation, parameter implications, dominance, partition correctness and mathematical validity require independent review."}


def render_analysis(analysis):
    """Render all synthesis sections without implying new scientific approval."""
    esc = lambda x: _text(x).replace("|", "\\|").replace("\n", " ")
    out = ["# Joint-parameter analysis", "",
        "Bookkeeping status: **" + ("accounted" if joint_scope_complete(analysis) else "draft / partial")
        + "**. This report is not a mathematical or literature-completeness certificate.", "", "## Target", ""]
    if analysis.get("version") != 2:
        out[4:4] = ["Synthesis coverage: **legacy_unknown**. Existing impact claims have not been recertified under version 2.", ""]
    target = analysis["target"]
    for key in ("joint_variables", "fixed_parameters", "uniform_in", "allowed_constant_dependencies", "normalized_variables", "full_domain", "resolution"):
        out += [f"- **{key}**: {esc(target[key])}"]
    out += ["", "## Domain map", "", "| Cell | Region | Role | State | Comparisons | Note |",
        "| --- | --- | --- | --- | --- | --- |"]
    for c in analysis["domain_map"]["cells"]:
        out.append("| " + " | ".join(esc(c[k]) for k in ("cell_id", "predicate", "role", "state", "comparison_ids", "note")) + " |")
    if analysis.get("version") == 2:
        out += ["", "Closure/publication declarations:", ""]
        for c in analysis["domain_map"]["cells"]:
            out.append("- " + esc(c["cell_id"]) + ": " + esc(c["closure"]) + "/" + esc(c["publication"]) + "; proofs " + esc(c["closure_proof_refs"]))
    out += ["", "**Residual domain:** " + analysis["domain_map"]["residual_domain"], "",
        "**Partition argument:** " + analysis["domain_map"]["partition_argument"], "", "## Comparisons", ""]
    for c in analysis["comparisons"]:
        out += ["### " + c["comparison_id"], "", "- Role: " + c["role"], "- Slice: " + str(c["slice"]),
            "- Fixed parameters: " + esc(c["fixed_parameters"]), "- Constant dependencies: " + esc(c["constant_dependencies"]),
            "- Upper: " + c["upper_envelope"], "- Lower: " + c["lower_envelope"], "- Registered-envelope gap: " + c["gap"],
            "- Boundary checks: " + esc(c["boundary_checks"]), "- Remaining question: " + c["remaining_gap"], "",
            "| Bound | Decision | Validity | Adopted region | Reason / mapping proofs |", "| --- | --- | --- | --- | --- |"]
        for u in c["bound_uses"]:
            out.append("| " + " | ".join(esc(u[k]) for k in ("bound_id", "disposition", "validity_region", "adopted_region"))
                + " | " + esc(u["reason"] + " " + str(u["mapping_proof_refs"])) + " |")
        out.append("")
    for title, name in (("Provenance", "provenance"), ("Impact", "impact"), ("Normalization requests", "normalization_requests")):
        out += ["## " + title, ""]
        for row in analysis[name]:
            out += ["- " + "; ".join("**" + key + "**: " + esc(value) for key, value in row.items())]
        if not analysis[name]:
            out.append("None recorded.")
        out.append("")
    out += ["## Pending obligations", ""] + ["- " + x for x in analysis["pending_obligations"]]
    if not analysis["pending_obligations"]:
        out.append("None recorded; this alone does not establish complete literature coverage.")
    if analysis.get("version") == 2:
        coverage = analysis["synthesis_coverage"]
        out += ["", "## Synthesis coverage", "", "- Status: " + coverage["status"],
                "- Gap basis: " + coverage["gap_basis"], "- Literature coverage: " + esc(coverage["literature"])]
        for row in coverage["obligations"]:
            out += ["- " + esc(row)]
    return "\n".join(out) + "\n"
