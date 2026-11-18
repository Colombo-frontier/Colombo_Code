"""Scientific scope regressions using synthetic existing-setting contracts."""
from copy import deepcopy
from datetime import date
import json
from types import SimpleNamespace

import pytest

from oracle_atlas_maintenance.contracts import apply_delta, check_review, check_scope, compact
from oracle_atlas_maintenance.state import digest

CUTOFF = date.today().isoformat()


@pytest.fixture
def profile():
    return {
        "setting_id": "SYNTHETIC_EXISTING", "title": "Synthetic bracket contract",
        "common_specification": {"task": {"description": "synthetic test only"}},
        "views": [{"view_id": "randomized", "guarantees": [{"guarantee_id": "probability_2_3"}]}],
        "quantities": [{"id": "calls"}], "resource_projections": [{"id": "primitive_calls"}],
        "regimes": [{"id": "small_accuracy", "predicate_text": "0 < epsilon < 1", "extension": {"keep": True}}],
        "bounds": [{"id": "upper", "direction": "upper", "view_id": "randomized",
                    "guarantee_id": "probability_2_3", "quantity_ref": "calls",
                    "quantity_refs": ["calls"], "region_refs": ["small_accuracy"],
                    "formula_latex": "epsilon^{-2}", "eligible_for_bracket": True,
                    "source_refs": ["old_source"], "extension": {"preserve": True}}],
        "comparisons": [{"comparison_id": "main", "comparison_key": {
            "setting_id": "SYNTHETIC_EXISTING", "view_id": "randomized", "guarantee_id": "probability_2_3",
            "quantity_id": "calls", "resource_projection_id": "primitive_calls", "regime_id": "small_accuracy"},
            "status": {"code": "missing_lower", "label": "Lower bound missing", "missing_sides": ["lower"]},
            "bracket": {"upper_refs": ["upper"], "lower_refs": []}}],
        "evidence": [], "references": [{"id": "old_source"}], "proofs": [],
        "bracket_rows": [{"row_id": "row_main", "comparison_ids": ["main"]}],
        "summary_status": {"scope": "documented_comparison_domain", "comparison_count": 1,
            "status_counts": {"missing_lower": 1}, "missing_sides": ["lower"], "gap_classes": [],
            "badges": [{"code": "bounds_missing", "label": "Bounds missing"}], "special_statuses": []}, "aliases": [],
        "custom_extension": {"untouched": "retained scientific history"},
    }


def report(profile, *, outcome="candidate_change", impact="improve_upper"):
    return {"setting_id": profile["setting_id"], "base_version": "frozen-baseline", "cutoff": CUTOFF,
            "outcome": outcome, "scope": {"queries_complete": True, "examined_comparison_ids": ["main"],
            "unresolved_leads": [], "note": "Synthetic bounded test search"},
            "findings": [{"candidate_id": "new_theorem", "impact": impact, "comparison_ids": ["main"],
                          "source_hashes": ["a" * 64], "reason": "Synthetic evidence changes the upper envelope"}],
            "patch": [], "summary_status_json": None, "rationale": "Synthetic test only"}


def patch(profile, collection, row, *, key="id"):
    rid = row[key]
    old = next((r for r in profile.get(collection, []) if r.get(key) == rid), None)
    return {"collection": collection, "id_field": key, "id": rid,
            "before_hash": digest(old) if old is not None else None, "value_json": json.dumps(row)}


def improved(profile):
    result = report(profile)
    row = deepcopy(profile["bounds"][0])
    row["formula_latex"] = "epsilon^{-1}"
    result["patch"] = [patch(profile, "bounds", row)]
    return result


def context(profile):
    return {"setting_id": profile["setting_id"], "base_version": "frozen-baseline", "cutoff": CUTOFF,
            "compact_profile": compact(profile), "artifacts": {"baseline": deepcopy(profile)}}


def prepared(profile):
    return {"bundle_hash": "prepared-sha", "files": {"profile.json": deepcopy(profile)}}


def host(*, searches=True, exhausted=False, sources=None):
    return SimpleNamespace(search_log=[{"query": "synthetic"}] if searches else [],
                           budget_exhausted=exhausted, source_log=[] if sources is None else sources)


def test_better_bound_is_material_even_when_summary_status_is_identical(profile):
    before = deepcopy(profile)
    proposed, delta = apply_delta(profile, improved(profile))
    assert proposed["bounds"][0]["formula_latex"] == "epsilon^{-1}"
    assert proposed["summary_status"] == before["summary_status"]
    assert proposed["comparisons"] == before["comparisons"]
    assert profile == before, "Application must not mutate the frozen baseline"
    assert delta[0]["before_hash"] == digest(before["bounds"][0])
    assert delta[0]["after_hash"] == digest(proposed["bounds"][0])


def test_partial_row_update_preserves_extensions_history_and_other_regions(profile):
    candidate = report(profile)
    candidate["patch"] = [patch(profile, "bounds", {"id": "upper", "direction": "upper", "view_id": "randomized",
        "guarantee_id": "probability_2_3", "quantity_ref": "calls", "quantity_refs": ["calls"],
        "formula_latex": "epsilon^{-1}"})]
    proposed, _ = apply_delta(profile, candidate)
    assert proposed["bounds"][0]["extension"] == {"preserve": True}
    assert proposed["bounds"][0]["region_refs"] == ["small_accuracy"]
    assert proposed["bounds"][0]["source_refs"] == ["old_source"]
    assert proposed["regimes"] == profile["regimes"]
    assert proposed["views"] == profile["views"]
    assert proposed["common_specification"] == profile["common_specification"]
    assert proposed["custom_extension"] == profile["custom_extension"]


@pytest.mark.parametrize("field,value", [("view_id", "deterministic"), ("guarantee_id", "expectation"),
    ("quantity_id", "time"), ("quantity_ref", "time"), ("quantity_refs", ["time"]),
    ("resource_projection_id", "total_time"), ("resource_projection_ref", "total_time"),
    ("resource_projection_refs", ["total_time"]), ("direction", "lower")])
def test_cannot_reinterpret_existing_bound_contract(profile, field, value):
    candidate = improved(profile)
    row = json.loads(candidate["patch"][0]["value_json"])
    row[field] = value
    candidate["patch"][0]["value_json"] = json.dumps(row)
    with pytest.raises(ValueError, match="contract is immutable"):
        apply_delta(profile, candidate)


@pytest.mark.parametrize("field,value", [("view_id", "deterministic"), ("guarantee_id", "expectation"),
    ("quantity_id", "time"), ("resource_projection_id", "total_time"), ("regime_id", "other_window")])
def test_existing_comparison_key_is_frozen(profile, field, value):
    row = deepcopy(profile["comparisons"][0])
    row["comparison_key"][field] = value
    candidate = report(profile)
    candidate["patch"] = [patch(profile, "comparisons", row, key="comparison_id")]
    with pytest.raises(ValueError, match="contract keys are immutable"):
        apply_delta(profile, candidate)


def test_native_quantity_and_resource_id_aliases_are_supported(profile):
    profile["quantities"] = [{"quantity_id": "calls"}]
    profile["resource_projections"] = [{"resource_projection_id": "primitive_calls"}]
    proposed, _ = apply_delta(profile, improved(profile))
    assert proposed["quantities"] == profile["quantities"]
    assert proposed["resource_projections"] == profile["resource_projections"]


def test_native_flat_comparison_key_can_receive_bracket_delta(profile):
    row = profile["comparisons"][0]
    row.update(row.pop("comparison_key"))
    candidate = improved(profile)
    proposed, _ = apply_delta(profile, candidate)
    assert proposed["comparisons"][0]["view_id"] == "randomized"


def test_native_flat_comparison_contract_cannot_be_rewritten(profile):
    old = profile["comparisons"][0]
    old.update(old.pop("comparison_key"))
    row = deepcopy(old)
    row["view_id"] = "deterministic"
    candidate = report(profile)
    candidate["patch"] = [patch(profile, "comparisons", row, key="comparison_id")]
    with pytest.raises(ValueError):
        apply_delta(profile, candidate)


def test_conflicting_flat_and_nested_comparison_keys_are_rejected(profile):
    candidate = improved(profile)
    row = deepcopy(profile["comparisons"][0])
    row["view_id"] = "deterministic"
    candidate["patch"].append(patch(profile, "comparisons", row, key="comparison_id"))
    with pytest.raises(ValueError, match="Flat comparison fields"):
        apply_delta(profile, candidate)


def test_wrong_before_hash_rejects_stale_producer_patch(profile):
    candidate = improved(profile)
    candidate["patch"][0]["before_hash"] = "b" * 64
    with pytest.raises(ValueError, match="before_hash"):
        apply_delta(profile, candidate)


def test_missing_before_hash_cannot_replace_an_existing_row(profile):
    candidate = improved(profile)
    candidate["patch"][0]["before_hash"] = None
    with pytest.raises(ValueError, match="before_hash"):
        apply_delta(profile, candidate)


def test_duplicate_patch_cannot_overwrite_intermediate_result(profile):
    candidate = improved(profile)
    candidate["patch"].append(deepcopy(candidate["patch"][0]))
    with pytest.raises(ValueError, match="duplicate"):
        apply_delta(profile, candidate)


def test_stable_row_id_cannot_be_changed_via_payload(profile):
    candidate = improved(profile)
    row = json.loads(candidate["patch"][0]["value_json"])
    row["id"] = "other_bound"
    candidate["patch"][0]["value_json"] = json.dumps(row)
    with pytest.raises(ValueError, match="stable ID"):
        apply_delta(profile, candidate)


def test_evidence_only_addition_does_not_trigger_bracket_publication(profile):
    candidate = report(profile)
    candidate["patch"] = [patch(profile, "evidence", {"id": "new_evidence", "statement": "same asymptotic theorem"})]
    with pytest.raises(ValueError, match="Evidence-only"):
        apply_delta(profile, candidate)


def test_unused_ineligible_bound_is_not_a_bracket_change(profile):
    candidate = report(profile)
    candidate["patch"] = [patch(profile, "bounds", {"id": "unused", "direction": "upper", "formula_latex": "1",
        "eligible_for_bracket": False, "view_id": "randomized", "guarantee_id": "probability_2_3"})]
    with pytest.raises(ValueError, match="Evidence-only"):
        apply_delta(profile, candidate)


def test_new_unused_regime_is_not_a_bracket_change(profile):
    candidate = report(profile)
    candidate["patch"] = [patch(profile, "regimes", {"id": "unused_region", "predicate_text": "not adopted"})]
    with pytest.raises(ValueError, match="Evidence-only"):
        apply_delta(profile, candidate)


@pytest.mark.parametrize("outcome", ["no_change", "incomplete"])
def test_non_candidate_outcome_cannot_smuggle_profile_edits(profile, outcome):
    candidate = improved(profile)
    candidate["outcome"] = outcome
    with pytest.raises(ValueError, match="Only candidate_change"):
        apply_delta(profile, candidate)


def test_no_change_without_edits_preserves_baseline(profile):
    candidate = report(profile, outcome="no_change", impact="no_effect")
    proposed, delta = apply_delta(profile, candidate)
    assert proposed == profile
    assert proposed is not profile
    assert delta == []


@pytest.mark.parametrize("condition", ["queries_incomplete", "unresolved_lead", "comparison_not_examined", "no_search", "exhausted", "change_finding"])
def test_incomplete_search_cannot_be_successful_no_change(profile, condition):
    candidate = report(profile, outcome="no_change", impact="no_effect")
    tool_host = host()
    if condition == "queries_incomplete":
        candidate["scope"]["queries_complete"] = False
    elif condition == "unresolved_lead":
        candidate["scope"]["unresolved_leads"] = ["unread new theorem"]
    elif condition == "comparison_not_examined":
        candidate["scope"]["examined_comparison_ids"] = []
    elif condition == "no_search":
        tool_host = host(searches=False)
    elif condition == "exhausted":
        tool_host = host(exhausted=True)
    elif condition == "change_finding":
        candidate["findings"][0]["impact"] = "improve_lower"
    with pytest.raises(ValueError):
        check_scope(candidate, context(profile), tool_host)


def test_unknown_comparison_is_not_treated_as_current_setting_scope(profile):
    candidate = report(profile, outcome="incomplete")
    candidate["scope"]["examined_comparison_ids"] = ["different_setting_comparison"]
    with pytest.raises(ValueError, match="unknown comparison"):
        check_scope(candidate, context(profile), host())


def test_failed_search_cannot_advance_no_change_cutoff(profile):
    candidate = report(profile, outcome="no_change", impact="no_effect")
    tool_host = host()
    tool_host.search_log = [{"query": "synthetic", "success": False, "error": "provider unavailable"}]
    tool_host.failed = True
    with pytest.raises(ValueError):
        check_scope(candidate, context(profile), tool_host)


def review(profile):
    return {"setting_id": profile["setting_id"], "base_version": "frozen-baseline", "prepared_hash": "prepared-sha",
            "verdict": "approve", "approved_bound_ids": ["upper"], "reviewed_comparison_ids": ["main"],
            "issues": [], "rationale": "Synthetic independent review"}


def test_approval_requires_independent_source_read_not_fetch_only(profile):
    with pytest.raises(ValueError, match="independently read"):
        check_review(review(profile), context(profile), prepared(profile), improved(profile),
                     host(sources=[{"action": "fetch", "sha256": "a" * 64}]))
    check_review(review(profile), context(profile), prepared(profile), improved(profile),
                 host(sources=[{"action": "source_read", "source_hash": "a" * 64}]))


def test_approval_accepts_real_tool_source_read_audit_shape(profile):
    check_review(review(profile), context(profile), prepared(profile), improved(profile),
                 host(sources=[{"tool": "source_read", "source_hash": "a" * 64,
                                "success": True, "offset": 100, "end": 1100, "characters_read": 1000}]))


def test_real_reviewer_cannot_approve_without_reading_prepared_profile(profile):
    tool_host = host(sources=[{"tool": "source_read", "source_hash": "a" * 64,
        "success": True, "characters_read": 1000}])
    tool_host.events = []
    with pytest.raises(ValueError, match="read the frozen prepared"):
        check_review(review(profile), context(profile), prepared(profile), improved(profile), tool_host)
    tool_host.events = [{"tool": "artifact_read", "arguments": {"name": "prepared"}, "result": {"text": "observed prepared row"}}]
    check_review(review(profile), context(profile), prepared(profile), improved(profile), tool_host)


def test_empty_source_excerpt_is_not_independent_theorem_verification(profile):
    with pytest.raises(ValueError, match="independently read"):
        check_review(review(profile), context(profile), prepared(profile), improved(profile),
                     host(sources=[{"tool": "source_read", "source_hash": "a" * 64,
                                    "success": True, "offset": 100, "end": 100, "characters_read": 0}]))


def test_approval_must_cover_each_affected_comparison(profile):
    decision = review(profile)
    decision["reviewed_comparison_ids"] = []
    with pytest.raises(ValueError, match="every affected comparison"):
        check_review(decision, context(profile), prepared(profile), improved(profile),
                     host(sources=[{"action": "read", "sha256": "a" * 64}]))


def test_approval_is_bound_to_frozen_prepared_bundle(profile):
    decision = review(profile)
    decision["prepared_hash"] = "other-prepared-sha"
    with pytest.raises(ValueError, match="prepared_hash"):
        check_review(decision, context(profile), prepared(profile), improved(profile), host())


def test_compact_preview_has_paths_and_explicit_incomplete_marker(profile):
    profile["bounds"][0]["formula_latex"] = "x" * 1000
    preview = compact(profile, limit=850)
    assert preview["comparison_ids"] == ["main"]
    assert preview["preview_incomplete"] is True
    assert preview["read_contract_at"] == "/common_specification"
