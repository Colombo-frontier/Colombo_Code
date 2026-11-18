"""Closed native status taxonomy. Validation never guesses scientific aliases."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re


_RESOURCE = Path(__file__).parent / "resources" / "status_taxonomy.json"
_CONTRACT = json.loads(_RESOURCE.read_text("utf-8"))
COMPARISON_CODES = frozenset(_CONTRACT["comparison_statuses"])
GAP_CODES = frozenset(_CONTRACT["gap_classes"])
SPECIAL_CODES = frozenset(_CONTRACT["special_statuses"])
_GAP_PRIORITY = tuple(_CONTRACT["gap_badge_priority"])
_SIDES = {"missing_lower": {"lower"}, "missing_upper": {"upper"},
          "missing_both": {"lower", "upper"}}
_JOINT_SIDES = {"achievable_budget", "necessary_resource_constraint"}
_SUMMARY_FIELDS = {"scope", "badges", "special_statuses", "gap_classes",
                   "missing_sides", "comparison_count", "status_counts"}


class StatusTaxonomyError(ValueError):
    pass


def status_contract():
    """Return the exact versioned contract supplied to both model roles."""
    return deepcopy(_CONTRACT)


def _fail(pointer, message):
    raise StatusTaxonomyError(f"Status taxonomy {pointer}: {message}")


def _strings(value, pointer, allowed):
    if (not isinstance(value, list) or any(not isinstance(x, str) for x in value)
            or len(value) != len(set(value)) or set(value) - allowed):
        _fail(pointer, "expected unique canonical values from " + ", ".join(sorted(allowed)))
    return set(value)


def _named_rows(value, pointer, allowed):
    if not isinstance(value, list):
        _fail(pointer, "expected an array of status objects")
    codes = []
    for i, row in enumerate(value):
        if (not isinstance(row, dict) or not isinstance(row.get("code"), str) or row["code"] not in allowed
                or not isinstance(row.get("label"), str) or not row["label"].strip()):
            _fail(f"{pointer}/{i}", "expected a registered code and a nonempty display label")
        codes.append(row["code"])
    if len(codes) != len(set(codes)):
        _fail(pointer, "duplicate status code")
    return set(codes)


def _comparison_records(profile):
    comparisons = profile.get("comparisons")
    if not isinstance(comparisons, list) or not comparisons:
        _fail("/comparisons", "a published profile needs a nonempty comparison array")
    counts, missing, records = Counter(), set(), {}
    for i, row in enumerate(comparisons):
        pointer = f"/comparisons/{i}"
        if not isinstance(row, dict):
            _fail(pointer, "expected a native comparison object")
        cid = row.get("comparison_id")
        if not isinstance(cid, str) or not cid.strip() or cid in records:
            _fail(pointer + "/comparison_id", "expected a unique nonempty native comparison ID")
        status = row.get("status")
        if not isinstance(status, dict):
            _fail(pointer + "/status", "expected a canonical status object")
        code = status.get("code")
        if not isinstance(code, str) or code not in COMPARISON_CODES:
            _fail(pointer + "/status/code", "unknown comparison code; explicitly correct the proposal, never infer an alias")
        if not isinstance(status.get("label"), str) or not status["label"].strip():
            _fail(pointer + "/status/label", "expected a nonempty display label")
        if "gap_class" in status and (code not in GAP_CODES or status["gap_class"] != code):
            _fail(pointer + "/status/gap_class", "a redundant gap class must use the same canonical quantified-gap code")
        allowed = _JOINT_SIDES if code == "joint_budget_unclosed" else {"lower", "upper"}
        sides = _strings(status.get("missing_sides"), pointer + "/status/missing_sides", allowed)
        if code != "joint_budget_unclosed" and sides != _SIDES.get(code, set()):
            _fail(pointer + "/status/missing_sides", "does not agree with the canonical comparison code")
        # Endpoint/saturation facts are attributes, never additional main codes.
        attributes = status.get("attributes", {})
        if not isinstance(attributes, dict):
            _fail(pointer + "/status/attributes", "expected an object")
        if "saturation" in attributes and type(attributes["saturation"]) is not bool:
            _fail(pointer + "/status/attributes/saturation", "expected a boolean")
        if "exact_cost" in attributes:
            cost = attributes["exact_cost"]
            if type(cost) is not int or cost < 0:
                _fail(pointer + "/status/attributes/exact_cost", "expected a nonnegative integer")
            if code != "optimal":
                _fail(pointer + "/status/attributes/exact_cost", "an exact complexity belongs to optimal in this comparison's declared domain")
            if cost == 0:
                if attributes.get("ratio_applicable") is not False:
                    _fail(pointer + "/status/attributes/ratio_applicable", "zero cost requires an explicitly inapplicable multiplicative ratio")
                bracket = row.get("bracket", {})
                if isinstance(bracket, dict):
                    for key in ("ratio", "gap_ratio", "upper_lower_ratio"):
                        ratio = bracket.get(key)
                        if ratio is not None and not (isinstance(ratio, dict) and ratio.get("applicable") is False
                                                     and ratio.get("value") is None):
                            _fail(pointer + "/bracket/" + key, "zero cost cannot carry a positive ratio or 0/0")
                    displayed = bracket.get("ratio_or_gap")
                    if displayed is not None:
                        if not isinstance(displayed, str):
                            _fail(pointer + "/bracket/ratio_or_gap", "expected explanatory text for the inapplicable ratio")
                        if (re.search(r"(?<![0-9])0\s*/\s*0(?![0-9])", displayed)
                                or re.search(r"\\(?:d?frac|tfrac)\s*\{\s*0\s*\}\s*\{\s*0\s*\}", displayed)):
                            _fail(pointer + "/bracket/ratio_or_gap", "an exact zero-cost comparison must not display 0/0")
        if "ratio_applicable" in attributes and type(attributes["ratio_applicable"]) is not bool:
            _fail(pointer + "/status/attributes/ratio_applicable", "expected a boolean")
        counts[code] += 1
        missing.update(sides)
        records[cid] = row
    return counts, missing, records


def _valid_gap_details(value, records):
    if not isinstance(value, list):
        _fail("/summary_status/gap_details", "expected an array")
    kept = []
    for item in value:
        if not isinstance(item, dict):
            _fail("/summary_status/gap_details", "expected native gap-detail objects")
        if any(not isinstance(item.get(key), str) or not item[key].strip()
               for key in ("comparison_id", "view_id", "region", "expression")):
            continue
        cid = item["comparison_id"]
        row = records.get(cid) if isinstance(cid, str) else None
        if row is None or row["status"]["code"] not in GAP_CODES:
            continue
        view = row.get("comparison_key", row).get("view_id")
        if item["view_id"] != view:
            continue
        kept.append(deepcopy(item))
    return kept


def canonical_summary(profile, scope="documented_comparison_domain"):
    """Derive aggregate metadata only, without changing or inferring comparison codes.

    Callers explicitly choose to replace their summary with this returned object.
    Validation never silently invokes this correction on a publication proposal.
    """
    if not isinstance(profile, dict):
        _fail("", "expected a profile object")
    if scope != "documented_comparison_domain":
        _fail("/summary_status/scope", "fully_optimal applies only to documented comparison domains")
    counts, missing, records = _comparison_records(profile)
    old = profile.get("summary_status", {})
    if not isinstance(old, dict):
        _fail("/summary_status", "expected an object")
    summary = deepcopy(old)
    summary.pop("code", None)
    codes = set(counts)
    gaps, specials = codes & GAP_CODES, codes & SPECIAL_CODES
    badges = []
    if codes == {"optimal"}:
        badges.append("fully_optimal")
    else:
        badges.extend(code for code in _GAP_PRIORITY if code in gaps)
        # Keep the original primary-gap display convention. All gap classes are
        # still recorded below; this does not erase any comparison or gap fact.
        badges = badges[:1]
        if missing:
            badges.append("bounds_missing")
    labels = _CONTRACT["summary_labels"]
    summary.update(scope=scope, comparison_count=sum(counts.values()), status_counts=dict(sorted(counts.items())),
                   missing_sides=sorted(missing), gap_classes=[c for c in _GAP_PRIORITY if c in gaps],
                   badges=[{"code": c, "label": labels[c]} for c in badges],
                   special_statuses=[{"code": c, "label": labels[c]} for c in sorted(specials)])
    if "gap_details" in summary:
        summary["gap_details"] = _valid_gap_details(summary["gap_details"], records)
    return summary


def validate_status_taxonomy(profile):
    """Reject unknown or inconsistent status metadata; grant no scientific/read credit."""
    if not isinstance(profile, dict):
        _fail("", "expected a profile object")
    counts, missing, records = _comparison_records(profile)
    summary = profile.get("summary_status")
    if not isinstance(summary, dict) or not _SUMMARY_FIELDS.issubset(summary):
        _fail("/summary_status", "a complete canonical summary is required: " + ", ".join(sorted(_SUMMARY_FIELDS)))
    if "code" in summary:
        _fail("/summary_status/code", "summary uses scoped badges/special statuses, never a standalone main code")
    if summary["scope"] != "documented_comparison_domain":
        _fail("/summary_status/scope", "summary claims are scoped to documented comparisons, never the entire parameter domain")
    if type(summary["comparison_count"]) is not int or summary["comparison_count"] != sum(counts.values()):
        _fail("/summary_status/comparison_count", "must equal the actual comparison count")
    histogram = summary["status_counts"]
    if (not isinstance(histogram, dict) or any(type(n) is not int or n < 1 for n in histogram.values())
            or histogram != dict(counts)):
        _fail("/summary_status/status_counts", "must exactly count canonical comparison codes")
    if _strings(summary["missing_sides"], "/summary_status/missing_sides", {"lower", "upper"} | _JOINT_SIDES) != missing:
        _fail("/summary_status/missing_sides", "must equal the union of comparison missing sides")
    codes = set(counts)
    gaps, specials = codes & GAP_CODES, codes & SPECIAL_CODES
    if _strings(summary["gap_classes"], "/summary_status/gap_classes", GAP_CODES) != gaps:
        _fail("/summary_status/gap_classes", "must equal the actual quantified-gap classes; closed or missing-side codes are not gaps")
    actual_specials = _named_rows(summary["special_statuses"], "/summary_status/special_statuses", SPECIAL_CODES)
    if actual_specials != specials:
        _fail("/summary_status/special_statuses", "must equal the actual special comparison statuses")
    allowed_badges = frozenset(_CONTRACT["summary_badges"])
    badges = _named_rows(summary["badges"], "/summary_status/badges", allowed_badges)
    if ("fully_optimal" in badges) != (codes == {"optimal"}):
        _fail("/summary_status/badges", "fully_optimal is required exactly when every documented comparison is optimal")
    if ("bounds_missing" in badges) != bool(missing):
        _fail("/summary_status/badges", "bounds_missing must agree with the actual missing-side union")
    if badges & GAP_CODES - gaps:
        _fail("/summary_status/badges", "a gap badge must have an actual comparison of that class")
    if gaps and next(code for code in _GAP_PRIORITY if code in gaps) not in badges:
        _fail("/summary_status/badges", "must include the highest-priority actual gap class")
    if "gap_details" in summary and _valid_gap_details(summary["gap_details"], records) != summary["gap_details"]:
        _fail("/summary_status/gap_details", "each detail must bind a current quantified-gap comparison and its exact view")
