"""Nested feedback structures from real SLQ and projection completeness; engineering checks only, with no predetermined scientific conclusions."""
from copy import deepcopy
import json
import unittest
from unittest.mock import patch

from oracle_atlas.atlas.sidecars import validate_sidecars
from oracle_atlas.atlas.tags import effective_native_operations, match_interface, project_tags
from test_sidecar_validation import profile, vocabulary


def nested_profile():
    value = profile()
    value["common_specification"]["oracle"]["operations"] = [{
        "operation_id": "matvec", "object_ref": "A",
        "query": {"domain_ref": "Rn", "selection": "Algorithm chooses v."},
        "response": {"precision": "exact", "noise": "none", "text": "The full vector Av."},
    }]
    value["views"].append({"view_id": "slq_family", "algorithms": {}, "guarantees": [], "specification_overrides": {}})
    return value


def vocab():
    value = vocabulary()
    value["machine"]["concepts"].append({"concept_id": "ORACLE:feedback_quality:exact", "axis": "ORACLE", "group": "feedback_quality", "value": "exact", "label": "Exact"})
    return value


def bundle(value):
    return {"profile.json": value, **{name + ".json": data for name, data in project_tags(value, [], vocab()).items()}}


def exact_facets(files):
    return [row for row in files["human_tags.json"]["facets"] if row["concept_id"] == "ORACLE:quality:exact"]


class NestedFeedbackProjectionTests(unittest.TestCase):
    def test_real_slq_structure_reaches_both_scoped_bindings_and_exact_navigation(self):
        value = nested_profile()
        before = json.dumps(value, sort_keys=True)
        files = bundle(value)
        for name in ("classification.json", "machine_tags.json"):
            bindings = files[name]["operation_bindings"]
            self.assertEqual({row["view_ref"] for row in bindings}, {"adaptive", "slq_family"})
            for row in bindings:
                self.assertEqual(row["precision"], "exact")
                self.assertEqual(row["precision_pointer"], "/common_specification/oracle/operations/0/response/precision")
                self.assertEqual(row["noise"], "none")
                self.assertEqual(row["noise_pointer"], "/common_specification/oracle/operations/0/response/noise")
        self.assertEqual(exact_facets(files)[0]["view_ids"], ["adaptive", "slq_family"])
        self.assertEqual(match_interface(value, {"precision": "exact"})["state"], "matched")
        self.assertEqual(validate_sidecars(files, vocab()), [])
        self.assertEqual(json.dumps(value, sort_keys=True), before)

    def test_consistent_direct_and_nested_declarations_keep_real_source(self):
        value = nested_profile()
        value["common_specification"]["oracle"]["operations"][0]["feedback_quality"] = {"code": "exact"}
        files = bundle(value)
        self.assertEqual(files["machine_tags.json"]["operation_bindings"][0]["precision_pointer"], "/common_specification/oracle/operations/0/feedback_quality")
        self.assertEqual(validate_sidecars(files, vocab()), [])

    def test_direct_nested_precision_conflict_is_not_silently_chosen(self):
        value = nested_profile()
        value["common_specification"]["oracle"]["operations"][0]["precision"] = "stochastic"
        normalized = effective_native_operations(value, "adaptive")
        self.assertFalse(normalized["complete"])
        self.assertIsNone(normalized["operations"][0]["precision"])
        self.assertEqual(match_interface(value, {"precision": "exact"})["state"], "unknown")
        files = bundle(value)
        self.assertEqual(exact_facets(files), [])
        self.assertIn("native_operation_declaration", {e["code"] for e in validate_sidecars(files, vocab())})

    def test_view_override_uses_its_actual_nested_source_and_excludes_noisy_view(self):
        value = nested_profile()
        operation = deepcopy(value["common_specification"]["oracle"]["operations"][0])
        operation["response"].update(precision="stochastic", noise="gaussian")
        value["views"][1]["specification_overrides"] = {"oracle": {"operations": [operation]}}
        files = bundle(value)
        row = files["classification.json"]["operation_bindings"][1]
        self.assertEqual(row["precision"], "stochastic")
        self.assertEqual(row["precision_pointer"], "/views/1/specification_overrides/oracle/operations/0/response/precision")
        self.assertEqual(exact_facets(files)[0]["view_ids"], ["adaptive"])
        self.assertEqual(validate_sidecars(files, vocab()), [])

    def test_explicit_unknown_nested_precision_does_not_inherit_global_exact(self):
        value = nested_profile()
        value["common_specification"]["oracle"].update(precision="exact", feedback_applies_to_all_operations=True)
        value["common_specification"]["oracle"]["operations"][0]["response"]["precision"] = None
        self.assertEqual(match_interface(value, {"precision": "exact"})["state"], "unknown")
        self.assertEqual(exact_facets(bundle(value)), [])
        self.assertEqual(validate_sidecars(bundle(value), vocab()), [])

    def test_noise_none_alone_does_not_infer_exact_precision(self):
        value = nested_profile()
        del value["common_specification"]["oracle"]["operations"][0]["response"]["precision"]
        files = bundle(value)
        self.assertIsNone(files["classification.json"]["operation_bindings"][0]["precision"])
        self.assertEqual(match_interface(value, {"precision": "exact"})["state"], "unknown")
        self.assertEqual(exact_facets(files), [])
        self.assertEqual(validate_sidecars(files, vocab()), [])

    def test_sampled_exact_response_with_noise_is_not_fixed_object_exact(self):
        value = nested_profile()
        response = value["common_specification"]["oracle"]["operations"][0]["response"]
        response.update(noise="gaussian", target_scope="sampled_realization")
        normalized = effective_native_operations(value, "adaptive")
        self.assertTrue(normalized["complete"])
        self.assertEqual(normalized["operations"][0]["precision"], "exact")
        self.assertTrue(normalized["operations"][0]["sampled"])
        files = bundle(value)
        self.assertEqual(exact_facets(files), [])
        self.assertEqual(match_interface(value, {"precision": "exact"})["state"], "unknown")
        self.assertEqual(validate_sidecars(files, vocab()), [])

    def test_fixed_exact_with_declared_nonzero_noise_is_a_conflict(self):
        value = nested_profile()
        value["common_specification"]["oracle"]["operations"][0]["response"]["noise"] = "gaussian"
        normalized = effective_native_operations(value, "adaptive")
        self.assertFalse(normalized["complete"])
        self.assertIsNone(normalized["operations"][0]["precision"])
        self.assertTrue(validate_sidecars(bundle(value), vocab()))

    def test_conflicting_noise_and_sample_scope_are_diagnosed(self):
        value = nested_profile()
        operation = value["common_specification"]["oracle"]["operations"][0]
        operation.update(noise="gaussian", precision_scope="fixed_object")
        operation["response"]["target_scope"] = "sampled_function"
        normalized = effective_native_operations(value, "adaptive")
        self.assertFalse(normalized["complete"])
        self.assertTrue(any("noise" in d for d in normalized["diagnostics"]))
        self.assertTrue(any("fixed / sampled" in d for d in normalized["diagnostics"]))

    def test_mixed_native_operations_cannot_make_whole_interface_exact(self):
        value = nested_profile()
        value["common_specification"]["oracle"]["operations"].append({"id": "noisy", "target_object": "A", "response": {"precision": "stochastic", "noise": "gaussian"}})
        files = bundle(value)
        self.assertEqual(exact_facets(files), [])
        self.assertEqual(match_interface(value, {"precision": "exact"})["state"], "conflict")
        self.assertEqual(validate_sidecars(files, vocab()), [])
        value["common_specification"]["oracle"]["operations"][1]["role"] = "public_auxiliary"
        self.assertEqual(match_interface(value, {"precision": "exact"})["state"], "matched")
        self.assertEqual(validate_sidecars(bundle(value), vocab()), [])

    def test_legacy_unstructured_operation_names_remain_unknown_not_conflicting(self):
        value = nested_profile()
        value["common_specification"]["oracle"]["operations"] = ["f_value", "g_value"]
        files = bundle(value)
        self.assertEqual(match_interface(value, {"precision": "exact"})["state"], "unknown")
        self.assertEqual(exact_facets(files), [])
        self.assertEqual(validate_sidecars(files, vocab()), [])


class FeedbackCoverageValidationTests(unittest.TestCase):
    def test_old_null_binding_bug_is_caught_even_when_both_sidecars_agree(self):
        files = bundle(nested_profile())
        for name in ("classification.json", "machine_tags.json"):
            for row in files[name]["operation_bindings"]:
                row.update(precision=None, precision_pointer=row["source_pointer"])
        codes = {e["code"] for e in validate_sidecars(files, vocab())}
        self.assertIn("declared_feedback_coverage", codes)
        self.assertIn("declared_feedback_source", codes)

    def test_missing_operation_row_and_wrong_noise_are_caught(self):
        files = bundle(nested_profile())
        files["machine_tags.json"]["operation_bindings"].pop()
        files["classification.json"]["operation_bindings"][0]["noise"] = None
        codes = {e["code"] for e in validate_sidecars(files, vocab())}
        self.assertIn("operation_binding_coverage", codes)
        self.assertIn("declared_feedback_coverage", codes)

    def test_missing_exact_navigation_is_a_coverage_error_without_dangling_view_link(self):
        files = bundle(nested_profile())
        files["human_tags.json"]["facets"] = [row for row in files["human_tags.json"]["facets"] if row["concept_id"] != "ORACLE:quality:exact"]
        for view in files["human_tags.json"]["views"]:
            view["facet_ids"] = [cid for cid in view["facet_ids"] if cid != "ORACLE:quality:exact"]
        self.assertIn("human_exact_coverage", {e["code"] for e in validate_sidecars(files, vocab())})

    def test_missing_precision_feature_is_detected_independently_of_axis_lists(self):
        files = bundle(nested_profile())
        files["machine_tags.json"]["features"] = [row for row in files["machine_tags.json"]["features"] if row["group"] != "feedback_quality"]
        self.assertIn("precision_feature_coverage", {e["code"] for e in validate_sidecars(files, vocab())})

    def test_source_coverage_check_still_catches_shared_normalizer_regression(self):
        value = nested_profile()
        files = bundle(value)
        normalized = effective_native_operations(value, "adaptive")
        for row in normalized["operations"]:
            row.update(precision=None, precision_pointer=row["source_pointer"])
        for name in ("classification.json", "machine_tags.json"):
            for row in files[name]["operation_bindings"]:
                row.update(precision=None, precision_pointer=row["source_pointer"])
        with patch("oracle_atlas.atlas.sidecars.effective_native_operations", return_value=normalized), patch("oracle_atlas.atlas.sidecars.match_interface", return_value={"views": []}):
            errors = validate_sidecars(files, vocab())
        self.assertIn("declared_feedback_coverage", {e["code"] for e in errors})


if __name__ == "__main__":
    unittest.main()
