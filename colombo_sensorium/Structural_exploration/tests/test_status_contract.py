"""Closed taxonomy and aggregate checks, independent of mathematical approval."""
from copy import deepcopy
import json
from pathlib import Path

import pytest

from oracle_atlas.science.status import (
    COMPARISON_CODES, canonical_summary, status_contract, validate_status_taxonomy,
)
from oracle_atlas.core.config import resources_root
from oracle_atlas.science.status import GAP_CAUSES, StatusTaxonomyError


def profile(codes=("optimal",)):
    rows = []
    for index, code in enumerate(codes):
        sides = {"missing_lower": ["lower"], "missing_upper": ["upper"],
                 "missing_both": ["lower", "upper"]}.get(code, [])
        rows.append({"comparison_id": "c" + str(index), "view_id": "v",
                     "status": {"code": code, "label": "A source-faithful display label", "missing_sides": sides},
                     "bracket": {}})
    result = {"comparisons": rows, "summary_status": {"gap_details": [], "source_note": "preserve"}}
    result["summary_status"] = canonical_summary(result)
    return result


@pytest.mark.parametrize("code", sorted(COMPARISON_CODES))
def test_all_ten_registered_codes_have_a_self_consistent_scoped_summary(code):
    value = profile((code,))
    before = deepcopy(value)
    validate_status_taxonomy(value)
    assert value == before
    assert value["summary_status"]["source_note"] == "preserve"


@pytest.mark.parametrize("code", ["tight", "exact_zero", "gap", "fully_optimal", "custom", "", None, [], {}])
def test_unknown_comparison_codes_cannot_be_published_or_silently_normalized(code):
    value = profile()
    value["comparisons"][0]["status"]["code"] = code
    before = deepcopy(value)
    with pytest.raises(ValueError, match="status/code"):
        validate_status_taxonomy(value)
    with pytest.raises(ValueError, match="status/code"):
        canonical_summary(value)
    assert value == before


@pytest.mark.parametrize("field,value", [
    ("scope", "all_parameter_domain"), ("comparison_count", True), ("comparison_count", 2),
    ("status_counts", {"optimal": True}), ("status_counts", {"optimal": 1, "tight": 0}),
    ("gap_classes", ["tight"]), ("gap_classes", ["missing_lower"]),
    ("missing_sides", ["lower"]), ("badges", []),
    ("badges", [{"code": "optimal", "label": "Not a summary badge"}]),
    ("badges", [{"code": [], "label": "Invalid shape"}]),
    ("special_statuses", [{"code": "infinite_complexity", "label": "Not present"}]),
])
def test_summary_rejects_wrong_codes_counts_scope_and_missing_side_union(field, value):
    item = profile()
    item["summary_status"][field] = value
    with pytest.raises(ValueError, match="summary_status"):
        validate_status_taxonomy(item)


@pytest.mark.parametrize("field", ["scope", "badges", "special_statuses", "gap_classes", "missing_sides", "comparison_count", "status_counts"])
def test_publication_requires_the_complete_summary(field):
    item = profile()
    del item["summary_status"][field]
    with pytest.raises(ValueError, match="complete canonical summary"):
        validate_status_taxonomy(item)


def test_local_optimum_does_not_grant_profile_fully_optimal_and_gaps_remain_registered():
    item = profile(("optimal", "logarithmic_gap", "other_quantified_gap", "polynomial_gap", "missing_upper"))
    summary = item["summary_status"]
    assert {row["code"] for row in summary["badges"]} == {"polynomial_gap", "bounds_missing"}
    assert set(summary["gap_classes"]) == {"logarithmic_gap", "other_quantified_gap", "polynomial_gap"}
    validate_status_taxonomy(item)
    summary["badges"].append({"code": "logarithmic_gap", "label": "A supported additional badge"})
    summary["gap_classes"].reverse()
    validate_status_taxonomy(item)
    summary["badges"].append({"code": "fully_optimal", "label": "Unsupported profile claim"})
    with pytest.raises(ValueError, match="fully_optimal"):
        validate_status_taxonomy(item)


def test_special_status_and_joint_missing_budget_are_not_gap_classes():
    item = profile(("joint_budget_unclosed", "infeasible_task", "infinite_complexity"))
    assert item["summary_status"]["badges"] == []
    validate_status_taxonomy(item)
    item["comparisons"][0]["status"]["missing_sides"] = ["necessary_resource_constraint", "achievable_budget"]
    item["summary_status"] = canonical_summary(item)
    assert item["summary_status"]["badges"][0]["code"] == "bounds_missing"
    assert item["summary_status"]["gap_classes"] == []
    validate_status_taxonomy(item)


@pytest.mark.parametrize("code,sides", [("optimal", ["lower"]), ("missing_lower", []),
    ("missing_both", ["upper"]), ("joint_budget_unclosed", ["lower"]),
    ("joint_budget_unclosed", ["necessary_resource_constraint"] * 2)])
def test_code_and_missing_side_contract_cannot_disagree(code, sides):
    item = profile((code,))
    item["comparisons"][0]["status"]["missing_sides"] = sides
    with pytest.raises(ValueError, match="missing_sides"):
        validate_status_taxonomy(item)


def test_zero_cost_and_saturation_are_properties_of_optimal_comparison_not_new_codes():
    item = profile()
    item["comparisons"][0]["status"]["attributes"] = {"exact_cost": 0, "ratio_applicable": False, "saturation": True}
    item["comparisons"][0]["bracket"]["ratio"] = {"applicable": False, "value": None}
    validate_status_taxonomy(item)
    assert item["summary_status"]["badges"][0]["code"] == "fully_optimal"
    # That badge covers only the registered comparison domain.
    assert item["summary_status"]["scope"] == "documented_comparison_domain"


@pytest.mark.parametrize("ratio", [1, 0, "0/0", {"applicable": True, "value": 1}, {"applicable": False, "value": 0}])
def test_exact_zero_cannot_manufacture_a_positive_or_undefined_ratio(ratio):
    item = profile()
    item["comparisons"][0]["status"]["attributes"] = {"exact_cost": 0, "ratio_applicable": False}
    item["comparisons"][0]["bracket"]["ratio"] = ratio
    with pytest.raises(ValueError, match="zero cost"):
        validate_status_taxonomy(item)


@pytest.mark.parametrize("attributes", [{"exact_cost": True}, {"exact_cost": -1}, {"exact_cost": 0},
    {"exact_cost": 0, "ratio_applicable": True}, {"saturation": "true"}])
def test_endpoint_attributes_are_typed_and_zero_ratio_inapplicability_is_explicit(attributes):
    item = profile()
    item["comparisons"][0]["status"]["attributes"] = attributes
    with pytest.raises(ValueError):
        validate_status_taxonomy(item)


def test_canonical_summary_preserves_extensions_and_only_current_gap_details_without_mutating():
    item = profile(("optimal", "polynomial_gap"))
    item["summary_status"]["gap_details"] = [
        {"comparison_id": "c1", "view_id": "v", "region": "Synthetic registered regime", "expression": "A supported native gap"},
        {"comparison_id": "c0", "view_id": "v", "region": "Synthetic registered regime", "expression": "Stale closed-branch gap"},
        {"comparison_id": "absent", "view_id": "v", "region": "Synthetic registered regime", "expression": "Stale ID"}]
    before = deepcopy(item)
    with pytest.raises(ValueError, match="gap_details"):
        validate_status_taxonomy(item)
    result = canonical_summary(item)
    assert result["gap_details"] == [item["summary_status"]["gap_details"][0]]
    assert result["source_note"] == "preserve" and item == before
    item["summary_status"] = result
    validate_status_taxonomy(item)


@pytest.mark.parametrize("text", ["0/0", "undefined: 0 / 0", r"$\frac{0}{0}$", r"$\dfrac{0}{0}$"])
def test_exact_zero_rejects_literal_undefined_ratio_in_the_actual_native_display_field(text):
    item = profile()
    item["comparisons"][0]["status"]["attributes"] = {"exact_cost": 0, "ratio_applicable": False}
    item["comparisons"][0]["bracket"]["ratio_or_gap"] = text
    with pytest.raises(ValueError, match="must not display 0/0"):
        validate_status_taxonomy(item)


@pytest.mark.parametrize("field", ["comparison_id", "view_id", "region", "expression"])
def test_gap_detail_keeps_native_renderer_required_fields(field):
    item = profile(("polynomial_gap",))
    detail = {"comparison_id": "c0", "view_id": "v", "region": "Synthetic native regime", "expression": "A native gap"}
    del detail[field]
    item["summary_status"]["gap_details"] = [detail]
    with pytest.raises(ValueError, match="gap_details"):
        validate_status_taxonomy(item)


def test_versioned_resource_is_the_exact_contract_and_callers_cannot_mutate_it():
    resource = resources_root() / "standards/status_taxonomy.json"
    assert status_contract() == json.loads(resource.read_text("utf-8"))
    copy = status_contract()
    copy["comparison_statuses"].append("tight")
    assert "tight" not in status_contract()["comparison_statuses"]
    assert len(COMPARISON_CODES) == 10 and len(GAP_CAUSES) == 6


@pytest.mark.parametrize("value", [None, "optimal", [], {"label": "No code"}])
def test_missing_or_wrong_status_never_uses_an_optimal_default(value):
    item = profile()
    item["comparisons"][0]["status"] = value
    original = deepcopy(item)
    with pytest.raises(StatusTaxonomyError) as caught:
        validate_status_taxonomy(item)
    assert caught.value.path.startswith("/comparisons/0/status")
    assert caught.value.message and item == original


def test_omitted_status_and_bad_ids_have_path_specific_diagnostics():
    item = profile()
    del item["comparisons"][0]["status"]
    with pytest.raises(StatusTaxonomyError) as caught:
        validate_status_taxonomy(item)
    assert caught.value.path == "/comparisons/0/status"
    assert "canonical status" in caught.value.message
    item = profile()
    item["comparisons"].append(deepcopy(item["comparisons"][0]))
    with pytest.raises(StatusTaxonomyError, match="unique nonempty"):
        validate_status_taxonomy(item)


@pytest.mark.parametrize("location", ["regime", "comparison_regime", "bracket"])
@pytest.mark.parametrize("status", [{"code": "tight"}, {"code": "optimal"}, None])
def test_secondary_status_locations_are_rejected_even_for_a_known_code(location, status):
    item = profile()
    if location == "regime":
        item["regimes"] = [{"regime_id": "r", "status": status}]
        path = "/regimes/0/status"
    elif location == "comparison_regime":
        item["comparisons"][0]["regimes"] = [{"regime_id": "r", "status": status}]
        path = "/comparisons/0/regimes/0/status"
    else:
        item["comparisons"][0]["bracket"]["status"] = status
        path = "/comparisons/0/bracket/status"
    original = deepcopy(item)
    for operation in (validate_status_taxonomy, canonical_summary):
        with pytest.raises(StatusTaxonomyError) as caught:
            operation(item)
        assert caught.value.path == path
    assert item == original


def test_joint_analysis_workflow_statuses_are_not_comparison_codes():
    item = profile()
    item["joint_analysis"] = {"target": {"status": "unassessed"},
        "domain_map": {"status": "unknown", "regions": [{"status": "pending"}]},
        "comparisons": [{"status": "synthesis_pending", "bracket": {"status": "unassessed"}}]}
    original = deepcopy(item)
    validate_status_taxonomy(item)
    assert canonical_summary(item) == item["summary_status"]
    assert item == original


@pytest.mark.parametrize("causes", [[], sorted(GAP_CAUSES), ["literature_pending"], ["mathematical_gap"]])
def test_optional_gap_causes_are_scoped_reasons_not_status_inference(causes):
    item = profile(("missing_upper",))
    item["regimes"] = [{"regime_id": "r", "gap_causes": causes}]
    item["comparisons"][0]["gap_causes"] = causes
    original = deepcopy(item)
    validate_status_taxonomy(item)
    assert item == original
    assert item["comparisons"][0]["status"]["code"] == "missing_upper"


@pytest.mark.parametrize("causes", [None, "mathematical_gap", ["unknown"], ["unassessed", "unassessed"],
    [True], [{}], {"mathematical_gap": True}])
def test_gap_causes_reject_unknown_values_duplicates_and_wrong_shapes(causes):
    item = profile()
    item["regimes"] = [{"regime_id": "r", "gap_causes": causes}]
    with pytest.raises(StatusTaxonomyError) as caught:
        validate_status_taxonomy(item)
    assert caught.value.path == "/regimes/0/gap_causes"


@pytest.mark.parametrize("field,value", [("comparison_count", -1), ("status_counts", {"optimal": -1}),
    ("status_counts", {"optimal": 0}), ("status_counts", {"optimal": False})])
def test_negative_zero_and_boolean_counts_do_not_pass_python_numeric_equality(field, value):
    item = profile()
    item["summary_status"][field] = value
    with pytest.raises(StatusTaxonomyError):
        validate_status_taxonomy(item)


def test_summary_derivation_is_explicit_preserves_extensions_and_does_not_fix_unknown_codes():
    item = profile(("missing_lower",))
    item["summary_status"].update(comparison_count=99,
        badges=[{"code": "fully_optimal", "label": "False global claim"}], extension={"stable": True})
    original = deepcopy(item)
    with pytest.raises(StatusTaxonomyError):
        validate_status_taxonomy(item)
    corrected = canonical_summary(item)
    assert corrected["comparison_count"] == 1
    assert corrected["badges"][0]["code"] == "bounds_missing"
    assert corrected["extension"] == {"stable": True} and item == original
    item["summary_status"] = corrected
    validate_status_taxonomy(item)
    item["comparisons"][0]["status"]["code"] = "exact_zero"
    with pytest.raises(StatusTaxonomyError, match="unknown comparison code"):
        canonical_summary(item)


def test_component_profile_schema_requires_v2_and_canonical_status_without_repair():
    from oracle_atlas.core.contracts import ProtocolError, validate
    from test_atlas import profile as complete_profile
    item = complete_profile()
    validate("profile", item)
    for fault in ("missing_joint", "old_joint", "missing_status", "unknown_status"):
        invalid = deepcopy(item)
        if fault == "missing_joint":
            del invalid["joint_analysis"]
        elif fault == "old_joint":
            invalid["joint_analysis"]["version"] = 1
        elif fault == "missing_status":
            del invalid["comparisons"][0]["status"]
        else:
            invalid["comparisons"][0]["status"]["code"] = "tight"
        with pytest.raises(ProtocolError):
            validate("profile", invalid)


def test_research_scope_schema_is_shared_with_the_optional_profile_declaration():
    from oracle_atlas.core.contracts import ProtocolError, schema, validate
    declared = {"scope": "Explicit finite synthetic scope", "queries_complete": False, "unresolved_leads": []}
    validate("research_scope", declared)
    assert "research_scope" in schema("research")["required"]
    assert "research_scope" not in schema("profile")["required"]
    assert schema("profile")["properties"]["research_scope"] == schema("research")["properties"]["research_scope"]
    for missing in declared:
        invalid = {k: v for k, v in declared.items() if k != missing}
        with pytest.raises(ProtocolError):
            validate("research_scope", invalid)


def test_profile_review_schema_requires_three_hashes_and_each_independent_check_once():
    from oracle_atlas.core.contracts import ProtocolError, validate
    from oracle_atlas.science.joint import JOINT_CHECKS
    item = {"subject_ref": "sha256:" + "1" * 64, "review_type": "profile", "verdict": "approve",
            "assessments": [], "issues": [], "approved_bound_ids": [], "summary": "Synthetic schema test"}
    with pytest.raises(ProtocolError, match="joint_review"):
        validate("review", item)
    item["joint_review"] = {"prepared_hash": "2" * 64, "analysis_hash": "3" * 64,
        "science_context_hash": "4" * 64,
        "checks": [{"check_id": name, "verdict": "approve", "reason": "Synthetic independent check"} for name in JOINT_CHECKS]}
    validate("review", item)
    for fault in ("missing_hash", "duplicate_check", "missing_check", "empty_reason", "bool_flags"):
        invalid = deepcopy(item)
        if fault == "missing_hash":
            del invalid["joint_review"]["science_context_hash"]
        elif fault == "duplicate_check":
            invalid["joint_review"]["checks"][1] = deepcopy(invalid["joint_review"]["checks"][0])
        elif fault == "missing_check":
            invalid["joint_review"]["checks"].pop()
        elif fault == "empty_reason":
            invalid["joint_review"]["checks"][0]["reason"] = ""
        else:
            invalid["joint_review"]["checks"] = {name: True for name in JOINT_CHECKS}
        with pytest.raises(ProtocolError):
            validate("review", invalid)

