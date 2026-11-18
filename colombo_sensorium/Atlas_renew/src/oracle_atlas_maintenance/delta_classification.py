"""Strict bookkeeping classification for claim provenance and support scope.

The complete native objects remain the publication/review subjects. These pure
functions do not authorize adoption, prove a transfer, or credit another role's
source/premise reads. They distinguish an unchanged claim's new adoption from a
changed claim and remove adoption back-indexes only from scientific dependency
traversal, never from frozen objects or their hashes.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import re

from oracle_atlas.atlas.store import _active_bounds

from .joint import _conflicts, _index, _ineligible, _key, _quantities, _resource_ids, _selected
from .state import digest

_CONTRACT = ("setting_id", "view_id", "guarantee_id", "quantity_id", "resource_projection_id")
_SUMMARY_COUNTS = frozenset({"comparison_count", "status_counts"})
_SUMMARY_DERIVED = _SUMMARY_COUNTS | {"missing_sides", "badges"}
_MISSING_STATUS_SIDES = {"missing_lower": ["lower"], "missing_upper": ["upper"],
                         "missing_both": ["lower", "upper"]}
_NONSCIENTIFIC_IMPACTS = frozenset({"no_effect", "incomparable", "synthesis_only"})
_ARGUMENT_FIELDS = ("body", "statement", "derivation", "argument", "steps", "proof")


def _string_list(value):
    return isinstance(value, list) and all(isinstance(x, str) for x in value) and len(value) == len(set(value))


def _argument_text(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        return any(_argument_text(child) for child in value.values())
    if isinstance(value, list):
        return any(_argument_text(child) for child in value)
    return False


def _proof_content(proof):
    # Structural presence of an explicit argument only. Its mathematical
    # completeness and applicability remain independent scientific judgments.
    return any(_argument_text(proof.get(field)) for field in _ARGUMENT_FIELDS)


def _changed_argument(proof, previous):
    return (_proof_content(proof) and (previous is None or any(
        proof.get(field) != previous.get(field) and _argument_text(proof.get(field))
        for field in _ARGUMENT_FIELDS)))


def _references(value, name):
    result = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == name and _string_list(child):
                result.update(child)
            elif key != name:
                result.update(_references(child, name))
    elif isinstance(value, list):
        for child in value:
            result.update(_references(child, name))
    return result


def _analysis_rows(profile, cid):
    analysis = profile.get("joint_analysis", {})
    if not isinstance(analysis, dict):
        return []
    return [row for row in analysis.get("comparisons", []) if row.get("comparison_id") == cid]


def _mapping_refs(profile, cid, bid, proofs):
    uses = [use for row in _analysis_rows(profile, cid) for use in row.get("bound_uses", [])
            if use.get("bound_id") == bid and use.get("disposition") == "included"]
    if len(uses) != 1:
        return set()
    refs = uses[0].get("mapping_proof_refs")
    if not _string_list(refs) or not refs or not set(refs).issubset(proofs):
        return set()
    if not all(_proof_content(proofs[ref]) for ref in refs):
        return set()
    return set(refs)


def _same_prior_contract(baseline, comparison, bid):
    target = {key: _key(comparison).get(key) for key in _CONTRACT}
    if any(value is None for value in target.values()):
        return False
    return any(bid in _selected(baseline, old)
               and {key: _key(old).get(key) for key in _CONTRACT} == target
               for old in baseline.get("comparisons", []))


def _contract_compatible(baseline, proposed, comparison, bound, proofs):
    mapping = _mapping_refs(proposed, comparison["comparison_id"], bound.get("id", bound.get("bound_id")), proofs)
    if _conflicts(bound, comparison):
        # A declared identity conflict is not a bookkeeping change. A distinct
        # scientific statement needs its own bound rather than this exception.
        return False
    key = _key(comparison)
    explicit = (bound.get("view_id") == key.get("view_id") is not None
                and bound.get("guarantee_id") == key.get("guarantee_id") is not None
                and key.get("quantity_id") in _quantities(bound)
                and key.get("resource_projection_id") in _resource_ids(bound))
    # Missing resource metadata is not a compatibility proof. Reuse an exact
    # prior adoption contract or require an explicit reviewed mapping argument.
    return explicit or _same_prior_contract(baseline, comparison, bound.get("id", bound.get("bound_id"))) or bool(mapping)


def _bound_baseline_refs(finding, baseline):
    from .evidence_basis import pointer_value
    refs = finding.get("baseline_refs")
    if not isinstance(refs, list) or not refs:
        return False
    try:
        return all(digest(pointer_value(baseline, ref["pointer"])) == ref["sha256"] for ref in refs)
    except (KeyError, IndexError, TypeError, ValueError):
        return False


def _linked_proofs(proposed, comparison, proofs):
    selected = _selected(proposed, comparison)
    bounds, evidence = _index(proposed, "bounds"), {
        row.get("id", row.get("evidence_id")): row for row in proposed.get("evidence", [])}
    objects = [comparison] + [bounds[bid] for bid in selected if bid in bounds]
    refs = set().union(*(_references(obj, "proof_refs") for obj in objects))
    evidence_refs = set().union(*(_references(obj, "evidence_refs") for obj in objects))
    seen = set()
    while evidence_refs - seen:
        eid = next(iter(evidence_refs - seen))
        seen.add(eid)
        if eid in evidence:
            refs |= _references(evidence[eid], "proof_refs")
            evidence_refs |= _references(evidence[eid], "evidence_refs")
    for row in _analysis_rows(proposed, comparison["comparison_id"]):
        for use in row.get("bound_uses", []):
            mapping = use.get("mapping_proof_refs", [])
            if use.get("disposition") == "included" and _string_list(mapping):
                refs.update(mapping)
    seen = set()
    while refs - seen:
        pid = next(iter(refs - seen))
        seen.add(pid)
        if pid in proofs:
            refs |= _references(proofs[pid], "proof_refs")
    return refs


def _new_adoption_supported(baseline, proposed, comparison, report, proofs):
    if not isinstance(report, dict):
        return False
    cid = comparison["comparison_id"]
    scoped = [f for f in report.get("findings", [])
              if isinstance(f.get("impact"), str) and f["impact"] not in _NONSCIENTIFIC_IMPACTS
              and cid in f.get("comparison_ids", [])]
    for finding in scoped:
        hashes = finding.get("source_hashes")
        if (finding.get("evidence_basis", "primary_source") == "primary_source"
                and _string_list(hashes) and hashes
                and all(re.fullmatch(r"[a-f0-9]{64}", value) for value in hashes)):
            # This is a structural support declaration only. Both roles must
            # still perform their own actual source_read in check_evidence_basis.
            return True
    derivations = [f for f in scoped if f.get("evidence_basis") == "retained_baseline_derivation"
                   and _bound_baseline_refs(f, baseline)]
    if not derivations:
        return False
    previous = _index(baseline, "proofs")
    changed = {pid for pid, proof in proofs.items() if _changed_argument(proof, previous.get(pid))}
    return bool(changed & _linked_proofs(proposed, comparison, proofs))


def _summary_counts_only(baseline, proposed):
    before, after = baseline.get("summary_status"), proposed.get("summary_status")
    if not isinstance(before, dict) or not isinstance(after, dict) or before == after:
        return False
    if {key: value for key, value in before.items() if key not in _SUMMARY_COUNTS} != {
            key: value for key, value in after.items() if key not in _SUMMARY_COUNTS}:
        return False
    for profile, summary in ((baseline, before), (proposed, after)):
        comparisons = profile.get("comparisons", [])
        count, histogram = summary.get("comparison_count"), summary.get("status_counts")
        if type(count) is not int or count != len(comparisons) or not isinstance(histogram, dict):
            return False
        if any(type(value) is not int or value < 0 for value in histogram.values()):
            return False
        codes = []
        for row in comparisons:
            status = row.get("status")
            code = status.get("code") if isinstance(status, dict) else status
            if not isinstance(code, str):
                return False
            codes.append(code)
        if histogram != dict(Counter(codes)):
            return False
    return True


def _comparison_summary(profile):
    """Derive a deliberately narrow aggregate; unknown shapes fail closed.

    This is not a status vocabulary or a scientific status validator. Custom
    nonoptimal code/label pairs can only be copied literally. In particular, no
    gap label, alias, or global optimality claim is inferred here.
    """
    comparisons = profile.get("comparisons")
    if not isinstance(comparisons, list) or not comparisons:
        return None
    ids, labels, badges, codes, sides = set(), {}, {}, [], set()
    for row in comparisons:
        if not isinstance(row, dict):
            return None
        cid, status = row.get("comparison_id"), row.get("status")
        if not isinstance(cid, str) or not cid.strip() or cid != cid.strip() or cid in ids:
            return None
        ids.add(cid)
        if not isinstance(status, dict) or set(status) != {"code", "label", "missing_sides"}:
            return None
        code, label, missing = status["code"], status["label"], status["missing_sides"]
        if any(not isinstance(value, str) or not value.strip() or value != value.strip()
               for value in (code, label)):
            return None
        if (not isinstance(missing, list) or any(not isinstance(side, str) or side not in {"lower", "upper"}
                                                 for side in missing)
                or missing != sorted(set(missing))):
            return None
        if code in labels and labels[code] != label:
            return None
        labels[code] = label
        codes.append(code)
        sides.update(missing)
        if code == "optimal":
            if missing:
                return None
            continue
        # A global fully-optimal aggregate is outside this copy-only rule.
        if code == "fully_optimal":
            return None
        if code in _MISSING_STATUS_SIDES:
            if missing != _MISSING_STATUS_SIDES[code]:
                return None
            badge_code, badge_label = "bounds_missing", "Bounds missing"
        else:
            badge_code, badge_label = code, label
        if badge_code in badges and badges[badge_code] != badge_label:
            return None
        badges[badge_code] = badge_label
    if not badges:
        return None
    return {"comparison_count": len(comparisons), "status_counts": dict(Counter(codes)),
            "missing_sides": sorted(sides),
            "badges": [{"code": code, "label": badges[code]} for code in sorted(badges)]}


def _summary_derived_only(baseline, proposed):
    """Prove both rich summaries are exact copies of their own native rows.

    Only the four aggregate fields may differ. The old counts-only route stays
    separate, including its legacy shapes. This classification only narrows the
    scientific-support traversal, never the actual review/publication objects.
    """
    before, after = baseline.get("summary_status"), proposed.get("summary_status")
    if not isinstance(before, dict) or not isinstance(after, dict) or before == after:
        return False
    changed = {key for key in set(before) | set(after) if before.get(key) != after.get(key)}
    if (not changed.issubset(_SUMMARY_DERIVED) or changed.issubset(_SUMMARY_COUNTS)
            or before.get("scope") != "documented_comparison_domain"
            or after.get("scope") != "documented_comparison_domain"):
        return False
    if {key: value for key, value in before.items() if key not in _SUMMARY_DERIVED} != {
            key: value for key, value in after.items() if key not in _SUMMARY_DERIVED}:
        return False
    for profile, summary in ((baseline, before), (proposed, after)):
        aggregate = _comparison_summary(profile)
        if (aggregate is None or not _SUMMARY_DERIVED.issubset(summary)
                or type(summary["comparison_count"]) is not int
                or not isinstance(summary["status_counts"], dict)
                or any(type(value) is not int for value in summary["status_counts"].values())
                or {key: summary[key] for key in _SUMMARY_DERIVED} != aggregate):
            return False
    return True


def classify_delta(baseline, proposed, report=None):
    """Return narrowly verified bookkeeping classifications, not scientific approval."""
    old_bounds, new_bounds = _index(baseline, "bounds"), _index(proposed, "bounds")
    old_comparisons, comparisons = _index(baseline, "comparisons"), _index(proposed, "comparisons")
    proofs = _index(proposed, "proofs")
    active = _active_bounds(baseline)
    updates = []
    for bid in sorted(set(old_bounds) & set(new_bounds)):
        old, new = old_bounds[bid], new_bounds[bid]
        if old == new or {key: value for key, value in old.items() if key != "selected_in_regimes"} != {
                key: value for key, value in new.items() if key != "selected_in_regimes"}:
            continue
        left, right = old.get("selected_in_regimes", []), new.get("selected_in_regimes")
        if (not _string_list(left) or not _string_list(right) or len(right) <= len(left)
                or right[:len(left)] != left or bid not in active or _ineligible(old) or _ineligible(new)):
            continue
        added = right[len(left):]
        valid = True
        for cid in added:
            comparison = comparisons.get(cid)
            if (comparison is None or bid not in _selected(proposed, comparison)
                    or not _contract_compatible(baseline, proposed, comparison, new, proofs)):
                valid = False
                break
            old_comparison = old_comparisons.get(cid)
            new_adoption = old_comparison is None or bid not in _selected(baseline, old_comparison)
            if new_adoption and not _new_adoption_supported(baseline, proposed, comparison, report, proofs):
                valid = False
                break
        if valid:
            updates.append({"bound_id": bid, "added_comparison_ids": added})
    return {"adoption_only_bound_ids": [row["bound_id"] for row in updates],
            "adoption_updates": updates, "summary_counts_only": _summary_counts_only(baseline, proposed),
            "summary_derived_only": _summary_derived_only(baseline, proposed)}


def scientific_support_comparisons(baseline, proposed, delta, report=None):
    """Compute scientific support scope without changing the default review cone.

    Keep real claim-change seeds, even if selection metadata is removed from the
    traversal view. Only strictly classified monotone adoption updates lose a
    claim-change seed; their new native comparison still supplies its own seed.
    """
    from .contracts import affected_comparisons
    classification = classify_delta(baseline, proposed, report)
    adoption_ids = set(classification["adoption_only_bound_ids"])
    scientific_delta = [row for row in delta
                        if not (row["collection"] == "bounds" and row["id"] in adoption_ids)]
    left, right = deepcopy(baseline), deepcopy(proposed)
    for profile in (left, right):
        profile.pop("joint_analysis", None)
        comparisons = _index(profile, "comparisons")
        forward = {cid: set() for cid in comparisons}
        for bound in profile.get("bounds", []):
            bid = bound.get("id", bound.get("bound_id"))
            selected = bound.pop("selected_in_regimes", None)
            if isinstance(selected, list):
                for cid in selected:
                    if isinstance(cid, str) and cid in comparisons and isinstance(bid, str):
                        forward[cid].add(bid)
        for cid, bids in forward.items():
            if bids:
                # A changed claim/proof must still reach a legacy comparison
                # linked only by this index. The reverse comparison->claim edge
                # stays absent. This field exists only in the temporary view.
                field = "_maintenance_selected_bound_refs"
                while field in comparisons[cid]:
                    field = "_" + field
                comparisons[cid][field] = sorted(bids)
    if classification["summary_counts_only"] or classification["summary_derived_only"]:
        right["summary_status"] = deepcopy(left["summary_status"])
    return affected_comparisons(left, right, scientific_delta)
