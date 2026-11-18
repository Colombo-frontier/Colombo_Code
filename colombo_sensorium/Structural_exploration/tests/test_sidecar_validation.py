"""Regressions for navigation regrouping, missing common axes, and cross-view source errors found in real acceptance."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest

from oracle_atlas.atlas.sidecars import validate_sidecars
from oracle_atlas.atlas.tags import project_tags

_HELPER_SPEC = importlib.util.spec_from_file_location("sidecar_test_synthetic_contracts", Path(__file__).resolve().parents[1] / "examples/synthetic_contracts.py")
_SYNTHETIC = importlib.util.module_from_spec(_HELPER_SPEC)
_HELPER_SPEC.loader.exec_module(_SYNTHETIC)


def profile():
    return _SYNTHETIC.complete_synthetic_profile({
        "schema_version": "6.1.0", "setting_id": "PSD_TRACE_STRUCTURAL_FIXTURE",
        "title": "Structural fixture, not a mathematical result", "primary_domain": "matrix_computation",
        "common_specification": {
            "task": {"navigation_domains": ["matrix_computation"], "summary": "Estimate a trace."},
            "model": {"summary": "Fixed symmetric PSD matrix."},
            "oracle": {"operations": [{"id": "right", "operation_code": "matrix_right_matvec", "target_object": "A", "feedback_quality": {"code": "exact"}, "role": "unknown_object_primitive"}]},
            "output": {"summary": "Scalar."}, "metric": {"summary": "Relative trace error."},
            "resource": {"summary": "One call per vector."},
        },
        "parameters": [],
        "views": [{"view_id": "adaptive", "algorithms": {"randomization": "private"}, "guarantees": [{"guarantee_id": "g"}], "specification_overrides": {}}],
        "quantities": [{"id": "q"}], "resource_projections": [{"id": "rp"}], "regimes": [{"id": "r"}],
        "comparisons": [{"comparison_id": "c", "comparison_key": {"setting_id": "PSD_TRACE_STRUCTURAL_FIXTURE", "view_id": "adaptive", "guarantee_id": "g", "quantity_id": "q", "resource_projection_id": "rp", "regime_id": "r"}, "bracket": {}, "status": {"code": "missing_both", "label": "Both bounds missing", "missing_sides": ["lower", "upper"]}}],
    })


def vocabulary():
    return {
        "human": {"concepts": [{"id": "ORACLE:quality:exact", "axis": "ORACLE", "group": "quality", "value": "exact", "label": "Exact", "parent_id": "ORACLE:quality"}]},
        "machine": {"concepts": [{"concept_id": "ORACLE:feedback_quality:exact_feedback", "axis": "ORACLE", "group": "feedback_quality", "value": "exact_feedback", "label": "Source-declared exact feedback (may be random)", "parent_id": "ORACLE:feedback_quality"}]},
    }


def source_fact():
    return {"concept_id": "ORACLE:feedback_quality:exact_feedback", "axis": "ORACLE", "value": "exact_feedback", "view_ref": "adaptive", "operation_ref": "right", "object_ref": "A", "source_pointer": "/common_specification/oracle/operations/0/feedback_quality", "status": "known"}


def files(p=None, vocab=None):
    p = p or profile()
    projected = project_tags(p, [source_fact()], vocab)
    return {"profile.json": p, **{name + ".json": data for name, data in projected.items()}}


class SidecarProjectionTests(unittest.TestCase):
    def test_exact_source_fact_has_registered_navigation_without_changing_fact(self):
        v = vocabulary()
        bundle = files(vocab=v)
        facets = bundle["human_tags.json"]["facets"]
        exact = next(row for row in facets if row["concept_id"] == "ORACLE:quality:exact")
        self.assertEqual(exact["normalization_state"], "controlled")
        self.assertEqual(exact["value"], "exact")
        self.assertNotIn("ORACLE:quality:exact_feedback", [row["concept_id"] for row in facets])
        self.assertIn(source_fact(), bundle["machine_tags.json"]["tag_facts"])
        self.assertEqual(validate_sidecars(bundle, v), [])

    def test_exact_sample_fact_does_not_make_fixed_interface_exact(self):
        p, v = profile(), vocabulary()
        p["common_specification"]["oracle"]["operations"][0]["precision_scope"] = "sampled_function"
        bundle = files(p, v)
        self.assertNotIn("ORACLE:quality:exact", [row["concept_id"] for row in bundle["human_tags.json"]["facets"]])
        self.assertIn(source_fact(), bundle["machine_tags.json"]["tag_facts"])
        self.assertEqual(validate_sidecars(bundle, v), [])

    def test_exact_public_auxiliary_is_not_a_navigation_source(self):
        p, v = profile(), vocabulary()
        p["common_specification"]["oracle"]["operations"].append({"id": "projection", "operation_code": "known_projection", "target_object": "public_set", "feedback_quality": {"code": "exact"}, "role": "public_auxiliary"})
        f = source_fact()
        f.update(operation_ref="projection", object_ref="public_set", source_pointer="/common_specification/oracle/operations/1/feedback_quality")
        projected = project_tags(p, [f], v)
        bundle = {"profile.json": p, **{name + ".json": data for name, data in projected.items()}}
        source = next(row for row in bundle["machine_tags.json"]["features"] if row["concept_id"] == f["concept_id"])
        exact = next(row for row in bundle["human_tags.json"]["facets"] if row["concept_id"] == "ORACLE:quality:exact")
        self.assertNotIn(source["feature_id"], exact["source_feature_ids"])
        self.assertEqual(validate_sidecars(bundle, v), [])
        exact["source_feature_ids"].append(source["feature_id"])
        exact["source_pointers"].append(f["source_pointer"])
        self.assertTrue(any(e["code"] == "human_exact_scope" for e in validate_sidecars(bundle, v)))

    def test_no_registered_human_alias_retains_proposed_source_id(self):
        v = vocabulary(); v["human"]["concepts"] = []
        bundle = files(vocab=v)
        facet = next(row for row in bundle["human_tags.json"]["facets"] if row["concept_id"] == source_fact()["concept_id"])
        self.assertEqual(facet["normalization_state"], "proposed")
        self.assertIsNone(facet["parent_id"])
        self.assertEqual(validate_sidecars(bundle, v), [])

    def test_empty_vocabulary_is_proposed_not_a_hard_error(self):
        for v in (None, {}):
            bundle = files(vocab=v)
            self.assertTrue(all(row["normalization_state"] == "proposed" for row in bundle["human_tags.json"]["facets"]))
            self.assertEqual(validate_sidecars(bundle, v), [])

    def test_unknown_common_axes_have_null_source_and_real_view_is_preserved(self):
        bundle = files(vocab=vocabulary())
        identity = bundle["identity.json"]
        for axis in ("algorithms", "guarantee"):
            self.assertEqual(identity["axes"][axis], {"source_pointer": None, "source_fields": None, "state": "unknown"})
        self.assertEqual(identity["views"][0]["algorithms"], bundle["profile.json"]["views"][0]["algorithms"])
        self.assertEqual(identity["views"][0]["guarantees"], bundle["profile.json"]["views"][0]["guarantees"])
        self.assertEqual(validate_sidecars(bundle, vocabulary()), [])


class SidecarValidationTests(unittest.TestCase):
    def test_old_real_failure_shapes_are_reported_together_without_mutation(self):
        v = vocabulary(); bundle = files(vocab=v)
        human = bundle["human_tags.json"]
        exact = next(row for row in human["facets"] if row["concept_id"] == "ORACLE:quality:exact")
        exact.update(concept_id="ORACLE:quality:exact_feedback", value="exact_feedback")
        for axis in ("algorithms", "guarantee"):
            bundle["identity.json"]["axes"][axis]["source_pointer"] = "/common_specification/" + axis
        original = json.dumps(bundle, sort_keys=True)
        errors = validate_sidecars(bundle, v)
        self.assertTrue(any(e["code"] == "unregistered_concept" and "exact_feedback" in e["message"] for e in errors))
        missing = {e["path"] for e in errors if e["file"] == "identity.json" and e["code"] == "source_pointer"}
        self.assertEqual(missing, {"/axes/algorithms/source_pointer", "/axes/guarantee/source_pointer"})
        self.assertEqual(json.dumps(bundle, sort_keys=True), original)

    def test_invented_parent_edges_are_rejected(self):
        v = vocabulary(); bundle = files(vocab=v)
        feature = bundle["machine_tags.json"]["features"][0]
        feature["retrieval_parent_ids"] = ["MODEL:made_up:ancestor"]
        facet = next(row for row in bundle["human_tags.json"]["facets"] if row["concept_id"] == "ORACLE:quality:exact")
        facet["parent_id"] = "ORACLE:made_up"
        errors = validate_sidecars(bundle, v)
        self.assertEqual({e["file"] for e in errors if e["code"] == "undeclared_parent"}, {"human_tags.json", "machine_tags.json"})

    def test_wrong_operation_and_cross_view_source_are_detected(self):
        p, v = profile(), vocabulary()
        p["views"].append({"view_id": "other", "algorithms": {}, "guarantees": [], "specification_overrides": {}})
        bundle = files(p, v)
        feature = bundle["machine_tags.json"]["features"][0]
        feature["bindings"][0]["operation_ref"] = "/operations/0"
        feature["bindings"][0]["source_pointer"] = "/views/1/algorithms"
        errors = validate_sidecars(bundle, v)
        self.assertTrue(any(e["code"] == "operation_ref" for e in errors))
        self.assertTrue(any(e["code"] == "pointer_view_scope" for e in errors))

    def test_identity_copy_cannot_change_scientific_view(self):
        v = vocabulary(); bundle = files(vocab=v)
        bundle["identity.json"]["views"][0]["algorithms"]["restrictions"] = ["made up"]
        self.assertTrue(any(e["code"] == "identity_view_fields" for e in validate_sidecars(bundle, v)))

    def test_unlinked_human_facet_is_not_accepted_as_evidence(self):
        v = vocabulary(); bundle = files(vocab=v)
        bundle["human_tags.json"]["facets"][0]["source_feature_ids"] = []
        self.assertTrue(any(e["code"] == "source_feature" for e in validate_sidecars(bundle, v)))

    def test_view_and_axis_coverage_must_match_the_underlying_profile_and_features(self):
        v = vocabulary(); bundle = files(vocab=v)
        bundle["machine_tags.json"]["view_ids"].append("invented_view")
        bundle["classification.json"]["axes"]["MODEL"] = ["MODEL:structure:invented"]
        bundle["machine_tags.json"]["axis_coverage"]["OUTPUT"] = {"state": "classified", "concept_ids": ["OUTPUT:object:invented"]}
        codes = {e["code"] for e in validate_sidecars(bundle, v)}
        self.assertIn("view_coverage", codes)
        self.assertIn("axis_coverage", codes)

    def test_malformed_collection_shapes_return_multiple_diagnostics(self):
        bundle = files(vocab=vocabulary())
        bundle["machine_tags.json"]["features"] = None
        bundle["identity.json"]["axes"] = None
        bundle["human_tags.json"]["facets"] = None
        errors = validate_sidecars(bundle, vocabulary())
        self.assertIn("identity_axes", {e["code"] for e in errors})
        self.assertGreaterEqual(sum(e["code"] == "array" for e in errors), 2)


if __name__ == "__main__":
    unittest.main()
