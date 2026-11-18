"""Joint-contract engineering fixtures, never claims about real literature."""
from copy import deepcopy

import pytest
from jsonschema import Draft202012Validator

from oracle_atlas.atlas.tags import digest
from oracle_atlas.core.contracts import schema
from oracle_atlas.science.joint import (
    JOINT_CHECKS, JointValidationError, build_joint_draft, validate_joint_profile,
)


NOTICE = "Explicit synthetic algebra fixture; no literature or theorem certification."


def native_profile():
    return {
        "setting_id": "SYNTHETIC_JOINT", "common_specification": {"task": {"summary": NOTICE}},
        "parameters": [{"id": "p_d", "symbol": "d"}, {"id": "p_eps", "symbol": "epsilon"},
                       {"id": "p_nu", "symbol": "nu"}],
        "views": [{"view_id": "v", "guarantees": [{"guarantee_id": "g"}]}],
        "quantities": [{"id": "q"}, {"id": "other_q"}],
        "resource_projections": [{"id": "rp"}],
        "regimes": [{"id": "r", "predicate_text": "d>=1, epsilon>0; 0<nu<1 fixed"}],
        "references": [{"id": "s", "label": NOTICE}],
        "proofs": [{"id": "proof", "statement": NOTICE}], "evidence": [],
        "bounds": [{"id": "u", "direction": "upper", "view_id": "v", "guarantee_id": "g",
                    "quantity_ref": "q", "resource_projection_id": "rp", "region_refs": ["r"],
                    "eligible_for_bracket": True, "formula_latex": "d/epsilon", "source_refs": ["s"],
                    "proof_refs": ["proof"], "applicability": {"conditions": ["epsilon <= 1/64"]}},
                   {"id": "l", "direction": "lower", "view_id": "v", "guarantee_id": "g",
                    "quantity_ref": "q", "resource_projection_id": "rp", "region_refs": ["r"],
                    "eligible_for_bracket": True, "formula_latex": "d", "source_refs": ["s"], "proof_refs": ["proof"]}],
        "comparisons": [{"comparison_id": "c", "comparison_key": {"setting_id": "SYNTHETIC_JOINT",
            "view_id": "v", "guarantee_id": "g", "quantity_id": "q", "resource_projection_id": "rp", "regime_id": "r"},
            "status": {"code": "polynomial_gap"}, "bracket": {"upper_refs": ["u"], "lower_refs": ["l"],
                "claim_guards": {"u": [{"region_ref": "r", "predicate_text": "d>=98304"}]},
                "envelopes": {"upper": {"claim_refs": ["u"], "expression_latex": "d/epsilon"},
                              "lower": {"claim_refs": ["l"], "expression_latex": "d"}}, "ratio_or_gap": "1/epsilon"}}],
        "bracket_rows": [],
    }


def resolved_profile():
    p = native_profile()
    a = build_joint_draft(p)
    a["target"].update(joint_variables=["p_d", "p_eps"], fixed_parameters=[{
        "symbol": "nu", "parameter_ref": "p_nu", "domain": "0<nu<1 fixed"}],
        uniform_in=["p_d", "p_eps"], allowed_constant_dependencies=["nu"],
        full_domain="d>=1,epsilon>0,0<nu<1 fixed", resolution="resolved")
    a["normalization_requests"] = []
    a["pending_obligations"] = []
    a["domain_map"].update(status="accounted", residual_domain="empty", partition_argument=NOTICE)
    for row in a["comparisons"]:
        row["constant_dependencies"] = ["nu"]
    a["provenance"] = [{"bound_id": b["id"], "origin": "source_theorem", "source_refs": ["s"],
        "proof_refs": ["proof"], "source_locator": NOTICE, "source_domain": "r", "target_domain": "r",
        "mapping": "Synthetic identity mapping."} for b in p["bounds"]]
    a["synthesis_coverage"].update(status="complete", literature={"status": "not_assessed", "scope": NOTICE})
    a["synthesis_coverage"]["obligations"] = [o for o in a["synthesis_coverage"]["obligations"] if o["kind"] != "material_lead"]
    for row in a["synthesis_coverage"]["obligations"]:
        row.update(state="resolved", argument=NOTICE)
    p["joint_analysis"] = a
    return p


@pytest.fixture
def profile():
    return resolved_profile()


def add_pending(profile, text="Synthetic unread plausible route.", *, kind="material_lead", **extra):
    a = profile["joint_analysis"]
    a["pending_obligations"].append(text)
    a["synthesis_coverage"]["status"] = "partial"
    a["synthesis_coverage"]["obligations"].append({"id": "pending-" + str(len(a["synthesis_coverage"]["obligations"])),
        "kind": kind, "comparison_ids": ["c"], "bound_refs": [], "cell_ids": [], "state": "pending",
        "affects_gap": True, "lead": text, "argument": NOTICE, "proof_refs": [], **extra})


def test_source_profile_hashes_are_bound_without_maintenance_dependency(profile):
    before = deepcopy(profile)
    result = validate_joint_profile(profile)
    assert result["valid"] and result["analysis_hash"] == digest(profile["joint_analysis"])
    assert result["baseline_hash"] is None and result["research_context_hash"] is None
    assert set(JOINT_CHECKS) == {"parameter_roles", "guarded_envelopes", "domain_accounting", "improvement_regions", "provenance", "display_consistency"}
    assert profile == before


def test_draft_is_deterministic_unassessed_and_grants_no_source_provenance():
    p = native_profile(); before = deepcopy(p)
    draft = build_joint_draft(p)
    Draft202012Validator(schema("joint_analysis")).validate(draft)
    assert build_joint_draft(p) == draft and p == before
    assert draft["version"] == 2 and draft["target"]["resolution"] == "normalization_required"
    assert draft["provenance"] == [] and draft["pending_obligations"]
    assert draft["synthesis_coverage"]["literature"]["status"] == "not_assessed"
    assert all(c["closure"] == "not_claimed" and c["publication"] == "unassessed" for c in draft["domain_map"]["cells"])
    use = draft["comparisons"][0]["bound_uses"][0]
    if use["bound_id"] != "u":
        use = draft["comparisons"][0]["bound_uses"][1]
    assert "epsilon <= 1/64" in use["validity_region"] and "98304" in use["adopted_region"]
    p["joint_analysis"] = draft
    with pytest.raises(JointValidationError, match="resolve") as error:
        validate_joint_profile(p)
    assert error.value.path == "/joint_analysis/target/resolution"


@pytest.mark.parametrize("origin", ["retained_baseline", "retained_baseline_derivation"])
def test_new_profile_cannot_borrow_seed_baseline(profile, origin):
    if origin == "retained_baseline":
        profile["joint_analysis"]["provenance"][0]["origin"] = origin
    else:
        profile["evidence"] = [{"id": "e", "evidence_basis": origin}]
    with pytest.raises(JointValidationError, match="no accepted scientific baseline"):
        validate_joint_profile(profile)


def test_every_new_native_bound_has_provenance_even_when_quarantined(profile):
    extra = deepcopy(profile["bounds"][0]); extra.update(id="inactive", eligible_for_bracket=False, status="quarantined")
    profile["bounds"].append(extra)
    with pytest.raises(JointValidationError, match="Every native bound"):
        validate_joint_profile(profile)


def test_existing_frozen_baseline_can_retain_unchanged_claim(profile):
    baseline = deepcopy(profile)
    for row in profile["joint_analysis"]["provenance"]:
        row["origin"] = "retained_baseline"
    context = {"baseline_hash": digest(baseline), "scope": {"queries_complete": False, "unresolved_leads": []}}
    result = validate_joint_profile(profile, baseline=baseline, research_context=context)
    assert result["baseline_hash"] == digest(baseline)
    assert result["research_context_hash"] == digest(context)
    profile["proofs"][0]["statement"] += " Changed premise."
    with pytest.raises(JointValidationError, match="dependency changed"):
        validate_joint_profile(profile, baseline=baseline, research_context=context)


def test_existing_baseline_hash_and_identity_are_checked(profile):
    baseline = deepcopy(profile)
    with pytest.raises(JointValidationError, match="baseline_hash"):
        validate_joint_profile(profile, baseline=baseline, research_context={"baseline_hash": "0" * 64})
    baseline["setting_id"] = "OTHER"
    with pytest.raises(JointValidationError, match="identity"):
        validate_joint_profile(profile, baseline=baseline)


def test_finite_literature_scope_uses_actual_context_and_never_fabricates_it(profile):
    profile["joint_analysis"]["synthesis_coverage"]["literature"]["status"] = "finite_scope_complete"
    with pytest.raises(JointValidationError, match="actual finished research scope"):
        validate_joint_profile(profile)
    bad = {"scope": {"queries_complete": False, "unresolved_leads": []}}
    with pytest.raises(JointValidationError, match="finished research scope"):
        validate_joint_profile(profile, research_context=bad)
    actual = {"scope": {"scope": "Explicitly synthetic bounded route.", "queries_complete": True, "unresolved_leads": []}}
    assert validate_joint_profile(profile, research_context=actual)["research_context_hash"] == digest(actual)


def test_constant_query_target_does_not_invent_varying_parameters(profile):
    profile["parameters"] = []
    a = profile["joint_analysis"]
    a["target"].update(joint_variables=[], fixed_parameters=[], uniform_in=[], allowed_constant_dependencies=[],
                       full_domain="The exact declared synthetic two-instance family.")
    a["comparisons"][0]["constant_dependencies"] = []
    assert validate_joint_profile(profile)["joint_scope_complete"]


@pytest.mark.parametrize("fault", ["joint_fixed", "hidden_accuracy", "not_uniform", "ambiguous_alias"])
def test_parameter_role_conflicts_are_structural_errors(profile, fault):
    target = profile["joint_analysis"]["target"]
    if fault == "joint_fixed":
        target["fixed_parameters"].append({"symbol": "epsilon", "parameter_ref": "p_eps", "domain": "fixed"})
    elif fault == "hidden_accuracy":
        target["allowed_constant_dependencies"].append("p_eps")
    elif fault == "not_uniform":
        target["uniform_in"] = ["p_d"]
    else:
        profile["parameters"].append({"id": "evil", "symbol": "epsilon"})
        target["joint_variables"] = ["d", "epsilon"]
    with pytest.raises(JointValidationError):
        validate_joint_profile(profile)


def test_slice_must_be_explicit_and_cannot_masquerade_as_primary_joint_target(profile):
    row = profile["joint_analysis"]["comparisons"][0]
    row["fixed_parameters"] = ["p_eps"]
    with pytest.raises(JointValidationError, match="fixes a target joint"):
        validate_joint_profile(profile)
    row.update(role="slice", slice="epsilon=c/d for explicitly fixed c in (0,1)")
    assert validate_joint_profile(profile)["valid"]
    profile["comparisons"][0]["bracket"]["fixed_parameters"] = ["p_eps"]
    row.update(role="joint", slice=None, fixed_parameters=[])
    with pytest.raises(JointValidationError, match="Native fixed-parameter slice"):
        validate_joint_profile(profile)


def test_compatible_candidates_and_excluded_native_bracket_must_agree(profile):
    profile["bounds"].append({**profile["bounds"][0], "id": "alt"})
    profile["joint_analysis"]["provenance"].append({**profile["joint_analysis"]["provenance"][0], "bound_id": "alt"})
    with pytest.raises(JointValidationError, match="accounted for"):
        validate_joint_profile(profile)
    profile = resolved_profile()
    profile["joint_analysis"]["comparisons"][0]["bound_uses"][0]["disposition"] = "dominated"
    with pytest.raises(JointValidationError, match="native bracket"):
        validate_joint_profile(profile)


def test_cross_quantity_and_unknown_guard_reference_are_rejected(profile):
    profile["bounds"][0]["quantity_ref"] = "other_q"
    with pytest.raises(JointValidationError, match="mapping proof"):
        validate_joint_profile(profile)
    profile = resolved_profile()
    profile["comparisons"][0]["bracket"]["claim_guards"]["u"][0]["region_ref"] = "absent"
    with pytest.raises(JointValidationError, match="unknown native regime") as error:
        validate_joint_profile(profile)
    assert error.value.path.endswith("/region_ref")


def test_domain_complement_is_explicit_without_claiming_unassessed_is_open(profile):
    profile["joint_analysis"]["domain_map"]["residual_domain"] = ""
    with pytest.raises(JointValidationError, match="explicit residual"):
        validate_joint_profile(profile)
    profile = resolved_profile()
    profile["joint_analysis"]["domain_map"]["cells"].append({"cell_id": "unread", "predicate": "Outside the read source window",
        "role": "unassessed", "comparison_ids": [], "state": "unassessed", "note": NOTICE,
        "closure": "not_claimed", "publication": "unassessed", "closure_proof_refs": []})
    assert validate_joint_profile(profile)["valid"]


def test_optimal_native_comparison_needs_published_closure_and_proof(profile):
    profile["comparisons"][0]["status"] = {"code": "optimal"}
    with pytest.raises(JointValidationError, match="Newly closed"):
        validate_joint_profile(profile)
    cell = profile["joint_analysis"]["domain_map"]["cells"][0]
    cell.update(closure="established", publication="native_comparison", closure_proof_refs=["proof"])
    assert validate_joint_profile(profile)["valid"]
    cell["closure_proof_refs"] = ["artifact-handle-not-a-native-proof"]
    with pytest.raises(JointValidationError, match="native proof"):
        validate_joint_profile(profile)


def test_unclaimed_closure_cannot_publish_or_carry_proof(profile):
    profile["joint_analysis"]["domain_map"]["cells"][0]["publication"] = "native_comparison"
    with pytest.raises(JointValidationError):
        validate_joint_profile(profile)


def test_unpublished_derived_closure_stays_pending_partial(profile):
    cell = profile["joint_analysis"]["domain_map"]["cells"][0]
    cell.update(closure="established", publication="unpublished", closure_proof_refs=["proof"])
    with pytest.raises(JointValidationError, match="pending publication"):
        validate_joint_profile(profile)
    add_pending(profile, "Publish synthetic derived closure.", kind="closed_region_publication", cell_ids=[cell["cell_id"]])
    profile["joint_analysis"]["synthesis_coverage"]["obligations"].append({
        **profile["joint_analysis"]["synthesis_coverage"]["obligations"][-1], "id": "publication-lead", "kind": "material_lead"})
    assert validate_joint_profile(profile)["synthesis_coverage"]["unpublished_closed_cells"]


def test_known_lead_cannot_hide_outside_ledger_or_claim_complete(profile):
    context = {"scope": {"queries_complete": False, "unresolved_leads": ["Synthetic unread plausible route."]}}
    with pytest.raises(JointValidationError, match="material_lead"):
        validate_joint_profile(profile, research_context=context)
    add_pending(profile)
    assert validate_joint_profile(profile, research_context=context)["synthesis_coverage"]["pending_gap_obligations"]
    profile["joint_analysis"]["synthesis_coverage"]["status"] = "complete"
    with pytest.raises(JointValidationError, match="Fully synthesized"):
        validate_joint_profile(profile, research_context=context)


def test_strict_domain_extension_requires_outside_old_witness(profile):
    profile["joint_analysis"]["impact"] = [{"finding_id": "extension", "comparison_ids": ["c"],
        "kind": "domain_extension", "old_envelope": "old", "new_envelope": "new", "validity_region": "r",
        "improvement_region": "r2", "unchanged_region": "rest", "witness": NOTICE, "boundary_type": "exact",
        "argument": NOTICE, "extension_witness": None}]
    with pytest.raises(JointValidationError, match="old-domain-exterior"):
        validate_joint_profile(profile)
    profile["joint_analysis"]["impact"][0].update(kind="explicit_region_registration", extension_witness=None)
    assert not validate_joint_profile(profile)["synthesis_coverage"]["domain_extension_claims"]


def test_wrong_version_and_schema_paths_are_actionable(profile):
    profile["joint_analysis"]["version"] = 1
    with pytest.raises(JointValidationError) as error:
        validate_joint_profile(profile)
    assert error.value.path == "/joint_analysis/version"
    assert error.value.diagnostics[0]["code"] == "joint_schema"
