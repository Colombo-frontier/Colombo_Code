"""Exercise publication gates with synthetic examples; these are not mathematics reviews."""
from copy import deepcopy
import hashlib

import pytest

from oracle_atlas.atlas import Atlas, AtlasValidationError
from oracle_atlas.atlas.joint import analysis_template
from oracle_atlas.atlas.scientific import validate_profile_science
from oracle_atlas.atlas.tags import digest, json_bytes
from oracle_atlas.atlas.taxonomy import canonical_summary
from test_atlas import approve, facts, profile


@pytest.mark.parametrize("mutate", [
    lambda p: p["comparisons"][0].pop("status"),
    lambda p: p["comparisons"][0]["status"].update(code="tight"),
    lambda p: p["comparisons"][0]["status"].update(missing_sides=["upwards"]),
    lambda p: p["comparisons"][0]["status"].update(code="optimal", missing_sides=["lower"]),
    lambda p: p["comparisons"][0]["status"].update(code="optimal", missing_sides=[],
                                                    attributes={"exact_cost": 0, "ratio_applicable": True}),
    lambda p: p["comparisons"][0].update(gap_causes=["invented"]),
    lambda p: p["comparisons"][0].update(regimes=[{"status": {"code": "tight"}}]),
    lambda p: p["comparisons"][0]["bracket"].update(status={"code": "tight"}),
    lambda p: p["regimes"][0].update(status={"code": "tight"}),
    lambda p: p["summary_status"].update(comparison_count=True),
    lambda p: p["summary_status"].update(status_counts={"invented": 1}),
    lambda p: p["summary_status"].update(badges=[{"code": "fully_optimal", "label": "Fully optimal"}]),
    lambda p: p["summary_status"].update(code="optimal"),
    lambda p: p["summary_status"].update(gap_classes=["invented"]),
    lambda p: p["summary_status"]["badges"][0].update(label="Fully optimal"),
    lambda p: p.update(joint_analysis={}),
    lambda p: p["joint_analysis"]["target"].update(contract_refs=["/parameters/-1"]),
    lambda p: p["joint_analysis"]["domain_map"]["cells"][0].update(comparison_ids=["missing"]),
    lambda p: p["joint_analysis"].update(provenance=[]),
    lambda p: p["joint_analysis"]["provenance"][0].update(origin="retained_baseline"),
    lambda p: p["joint_analysis"]["synthesis_coverage"].update(obligations=[]),
    lambda p: p["joint_analysis"]["synthesis_coverage"].update(status="complete"),
    lambda p: p["joint_analysis"]["target"].update(fixed_parameters=[{"symbol":"n", "parameter_ref":"n", "domain":"fixed"}]),
])
def test_invalid_profile_rejected_by_prepare_even_without_target_schema(tmp_path, mutate):
    atlas = Atlas(tmp_path)
    p = profile()
    mutate(p)
    assert not atlas.preflight(p, facts(p))["valid"]
    assert atlas.version(p["setting_id"]) is None


def test_fully_rehashed_bundle_cannot_bypass_commit(tmp_path):
    atlas = Atlas(tmp_path)
    p = profile()
    prepared = atlas.prepare(p, facts(p))
    files = prepared["files"]
    files["profile.json"]["joint_analysis"]["synthesis_coverage"]["obligations"].clear()
    pretty = hashlib.sha256(json_bytes(files["profile.json"])).hexdigest()
    for name in ("classification.json", "identity.json"):
        files[name]["profile_sha256"] = pretty
    for name in ("human_tags.json", "machine_tags.json"):
        files[name]["profile_sha256"] = digest(files["profile.json"])
    files["machine_tags.json"]["source_classification_profile_sha256"] = pretty
    prepared["hashes"] = {name: hashlib.sha256(json_bytes(value)).hexdigest() for name, value in files.items()}
    prepared.update(bundle_hash=digest(files), version="target-" + digest(prepared["hashes"]))
    with pytest.raises(AtlasValidationError, match="Missing structured synthesis"):
        atlas.commit(prepared, approve(prepared), "forged")
    assert atlas.version(p["setting_id"]) is None


def test_open_formulation_commit_and_refinement(tmp_path):
    atlas = Atlas(tmp_path)
    pending = profile("OPEN_REFINEMENT")
    pending.update(comparisons=[], bounds=[], refinement_pending={
        "reason": "The source has not fixed the role of the parameter n",
        "next_evidence": "Obtain the quantifier over n from the formulation",
        "source_refs": ["fixture_source"]})
    pending["summary_status"] = canonical_summary(pending)
    pending["joint_analysis"] = analysis_template(pending)
    pre = atlas.prepare(pending, facts(pending))
    review = {**approve(pre), "approved_bound_ids": []}
    receipt = atlas.commit(pre, review, "open")
    written = atlas.read(pending["setting_id"])
    assert written["summary_status"]["badges"] == [] and not written["comparisons"]
    assert written["refinement_pending"] == pending["refinement_pending"]
    with pytest.raises(ValueError, match="No-change"):
        validate_profile_science(written, written, no_change=True)
    for key in ("reason", "source_refs"):
        incomplete = deepcopy(written)
        del incomplete["refinement_pending"][key]
        assert not atlas.preflight(incomplete, facts(incomplete), receipt["version"])["valid"]
    updated = profile("OPEN_REFINEMENT")
    assert not atlas.preflight(updated, facts(updated), receipt["version"])["valid"]
    updated["joint_analysis"]["impact"] = [{
        "finding_id": "refined", "kind": "explicit_region_registration", "comparison_ids":["c"],
        "old_envelope":"No native comparisons", "new_envelope":"u", "validity_region":"n >= 1",
        "improvement_region":"New registration only", "unchanged_region":"No other native regions",
        "witness":"n=1", "boundary_type":"not_applicable", "argument":"The fixed parameter role now permits a comparison.",
        "extension_witness":None}]
    fixed = atlas.prepare(updated, facts(updated), receipt["version"])
    atlas.commit(fixed, approve(fixed), "refined")
    assert "refinement_pending" not in atlas.read(updated["setting_id"])


def test_changed_bound_cannot_reuse_historical_provenance(tmp_path):
    p = profile()
    atlas = Atlas(tmp_path)
    frozen = atlas.prepare(p, facts(p))
    version = atlas.commit(frozen, approve(frozen), "initial")["version"]
    p["bounds"][0]["statement"] = "A changed theorem."
    p["joint_analysis"]["provenance"][0]["origin"] = "retained_baseline"
    failure = atlas.preflight(p, facts(p), version)
    assert not failure["valid"] and "non-baseline provenance" in str(failure["errors"])


@pytest.mark.parametrize("field", ["prepared_hash", "joint_checks"])
def test_review_must_supply_its_own_subject_hash_and_checks(tmp_path, field):
    p = profile()
    atlas = Atlas(tmp_path)
    prepared = atlas.prepare(p, facts(p))
    review = approve(prepared)
    del review[field]
    with pytest.raises(AtlasValidationError):
        atlas.commit(prepared, review, "incomplete-review")
    assert atlas.version(p["setting_id"]) is None
