"""Behavioral acceptance for native interfaces, retrieval, five-file commits, and interruption recovery."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from oracle_atlas.atlas import Atlas, AtlasConflict, AtlasValidationError, effective_native_operations, match_interface, project_tags, retrieve
from oracle_atlas.atlas.tags import AXES, TagError, at, expand_concepts
from oracle_atlas.atlas.retrieval import match_tag_filters, scope_search
from oracle_atlas.atlas import store as store_module
from oracle_atlas.atlas.joint import analysis_template
from oracle_atlas.atlas.taxonomy import canonical_summary

JOINT_CHECKS = dict.fromkeys(("parameter_roles", "guarded_envelopes", "domain_accounting",
                             "improvement_regions", "provenance", "display_consistency"), True)


def profile(sid="MATRIX_EXAMPLE"):
    common = {axis.lower(): {"summary": f"Explicit {axis.lower()} specification.", "statements": []} for axis in AXES}
    common["task"]["navigation_domains"] = ["matrix_computation"]
    common["oracle"]["operations"] = [{"id": "right", "operation_code": "right_matvec", "target_object": "A", "feedback_quality": {"code": "exact"}, "returns": ["matrix_product"]}]
    p = {
        "schema_version": "component-profile", "setting_id": sid, "title": "Synthetic exact matrix recovery",
        "primary_domain": "matrix_computation", "common_specification": common,
        "views": [{"view_id": "randomized", "label": "Randomized", "algorithms": {"randomization": "randomized_allowed"}, "guarantees": [{"guarantee_id": "g", "summary": "Per-instance success."}], "specification_overrides": {}, "alias_ids": []}],
        "parameters": [{"id": "n", "symbol": "n"}], "symbols": [], "quantities": [{"id": "q"}], "resource_projections": [{"id": "rp"}], "regimes": [{"id": "r"}],
        "bounds": [{"id": "u", "direction": "upper", "view_id": "randomized", "guarantee_id": "g", "quantity_ref": "q", "region_refs": ["r"], "eligible_for_bracket": True, "witness_type": "deterministic"}],
        "comparisons": [{"comparison_id": "c", "comparison_key": {"setting_id": sid, "view_id": "randomized", "guarantee_id": "g", "quantity_id": "q", "resource_projection_id": "rp", "regime_id": "r"}, "bracket": {"upper_refs": ["u"], "lower_refs": []}}],
        "bracket_rows": [], "summary_status": {"label": "Missing bounds"}, "proofs": [], "evidence": [], "references": [{"id":"fixture_source"}], "relations": [], "facets": [], "aliases": [], "provenance": {},
    }
    p["comparisons"][0]["status"] = {"code": "missing_lower", "label": "Missing lower bound", "missing_sides": ["lower"]}
    p["summary_status"] = canonical_summary(p)
    set_fixture_analysis(p)
    return p


def set_fixture_analysis(p):
    """Populate synthetic reference bookkeeping after a test changes native fixture IDs."""
    analysis = analysis_template(p)
    analysis["target"].update(resolution="resolved", joint_variables=["n"], uniform_in=["n"], full_domain="Integers n >= 1.")
    analysis["normalization_requests"] = []
    analysis["provenance"] = [
        {"bound_id": b["id"], "origin":"source_theorem", "source_refs":[p["references"][0]["id"]],
         "proof_refs": [], "source_locator":"Synthetic fixture, claim " + b["id"], "source_domain":"n >= 1",
         "target_domain":"n >= 1", "mapping":"Same matrix contract"}
        for b in p["bounds"] if b.get("eligible_for_bracket", True)]
    p["joint_analysis"] = analysis


def facts(p):
    values = {"TASK": ("task_family", "matrix_computation"), "MODEL": ("structure", "arbitrary_real_matrix"), "ORACLE": ("operation", "right_matvec"), "ALGORITHMS": ("randomization", "private_randomness_allowed"), "OUTPUT": ("object", "matrix"), "METRIC": ("criterion", "exact_recovery"), "GUARANTEE": ("mode", "probability"), "RESOURCE": ("measure", "oracle_calls")}
    return [{"concept_id": f"{axis}:{group}:{value}", "axis": axis, "value": value, "object_ref": None, "view_ref": None, "operation_ref": None, "source_pointer": f"/common_specification/{axis.lower()}/summary", "status": "known"} for axis, (group, value) in values.items()]


def approve(prepared):
    return {"subject_ref": "sha256:" + "1" * 64, "verdict": "approve", "approved_bound_ids": ["u"], "issues": [], "prepared_hash": prepared["bundle_hash"], "joint_checks": JOINT_CHECKS}


class InterfaceTests(unittest.TestCase):
    def test_exact_unknown_and_local_bound(self):
        p = profile()
        p["common_specification"]["oracle"]["operations"].append({"id": "mystery", "operation_code": "unregistered", "target_object": "A", "feedback_quality": None})
        self.assertEqual(match_interface(p, {"precision": "exact"})["state"], "unknown")
        self.assertEqual(match_interface(p, {"operation_ref": "right", "object_ref": "A", "precision": "exact"})["state"], "matched")
        tags = project_tags(p, facts(p))
        self.assertNotIn("ORACLE:quality:exact", [x["concept_id"] for x in tags["human_tags"]["facets"]])
        self.assertIn("ORACLE:feedback_quality:exact", [x["concept_id"] for x in tags["machine_tags"]["features"]])

    def test_view_override_replaces_operation_list(self):
        p = profile()
        p["views"][0]["specification_overrides"] = {"oracle": {"operations": [{"id": "left", "operation_code": "left_matvec", "feedback_quality": None}]}}
        data = effective_native_operations(p, "randomized")
        self.assertEqual([o["operation_ref"] for o in data["operations"]], ["left"])
        self.assertIsNone(data["operations"][0]["precision"])

    def test_explicit_null_does_not_inherit_global_exact(self):
        p = profile()
        p["common_specification"]["oracle"].update({"precision": "exact", "feedback_applies_to_all_operations": True})
        p["common_specification"]["oracle"]["operations"][0]["feedback_quality"] = None
        self.assertEqual(match_interface(p, {"precision": "exact"})["state"], "unknown")

    def test_invalid_alias_and_code_do_not_crash(self):
        p = profile()
        op = p["common_specification"]["oracle"]["operations"][0]
        op["object_ref"] = "different"
        op["operation_code"] = ["bad"]
        data = effective_native_operations(p, "randomized")
        self.assertFalse(data["complete"])
        self.assertGreater(len(data["diagnostics"]), 1)
        self.assertEqual(match_interface(p, {"precision": "exact"})["state"], "unknown")

    def test_exact_sample_not_exact_fixed_interface(self):
        p = profile()
        p["common_specification"]["oracle"]["operations"][0]["precision_scope"] = "sampled_function"
        self.assertEqual(match_interface(p, {"precision": "exact"})["state"], "unknown")
        self.assertEqual(match_interface(p, {"operation_ref": "right", "precision": "exact"})["state"], "matched")

    def test_public_auxiliary_does_not_pollute_exact(self):
        p = profile()
        p["common_specification"]["oracle"]["operations"].append({"id": "projection", "operation_code": "known_projection", "role": "public_auxiliary", "precision": None})
        self.assertEqual(match_interface(p, {"precision": "exact"})["state"], "matched")

    def test_native_vs_supplies(self):
        p = profile()
        op = p["common_specification"]["oracle"]["operations"][0]
        op.update({"operation_code": "first_order", "returns": ["value", "gradient"]})
        self.assertEqual(match_interface(p, {"returns": ["value"]}, "native")["state"], "conflict")
        result = match_interface(p, {"returns": ["value"]}, "supplies")
        self.assertEqual(result["state"], "matched")
        self.assertEqual(result["views"][0]["extra_capabilities"], ["gradient"])
        self.assertEqual(result["views"][0]["conversions"][0]["additional_calls"], 0)

    def test_only_declared_parents(self):
        cid = "MODEL:smoothness:holder"
        self.assertEqual(expand_concepts({cid}), {cid})
        self.assertEqual(expand_concepts({cid}, {"concepts": [{"id": cid, "parent_id": "MODEL:smoothness"}]}), {cid, "MODEL:smoothness"})

    def test_matrix_exact_combination_and_eight_axes(self):
        p = profile()
        tags = project_tags(p, facts(p))
        facet_ids = {row["concept_id"] for row in tags["human_tags"]["facets"]}
        self.assertIn("TASK:family:matrix_computation", facet_ids)
        self.assertIn("ORACLE:quality:exact", facet_ids)
        self.assertEqual(tags["classification"]["unclassified_axes"], [])
        verdict = match_tag_filters(p, facts(p), [{"concept_id": "TASK:family:matrix_computation"}, {"concept_id": "ORACLE:quality:exact"}])
        self.assertEqual(verdict["state"], "matched")

    def test_pointer_negative_or_bad_escape_rejected(self):
        for pointer in ("/x/-1", "/x/01", "/a~2"):
            with self.subTest(pointer=pointer), self.assertRaises(TagError):
                at({"x": [1], "a~2": 2}, pointer)

    def test_cross_operation_fact_rejected(self):
        p = profile()
        f = facts(p)
        f.append({"concept_id": "ORACLE:feedback_quality:exact", "axis": "ORACLE", "value": "exact", "view_ref": "randomized", "object_ref": "B", "operation_ref": "right", "source_pointer": "/common_specification/oracle/operations/0", "status": "known"})
        with self.assertRaises(TagError):
            project_tags(p, f)

    def test_pointer_cannot_borrow_other_operation(self):
        p = profile()
        p["common_specification"]["oracle"]["operations"].append({"id": "left", "operation_code": "left_matvec", "target_object": "A", "feedback_quality": {"code": "stochastic"}})
        f = facts(p)
        f.append({"concept_id": "ORACLE:feedback_quality:exact", "axis": "ORACLE", "value": "exact", "view_ref": "randomized", "object_ref": "A", "operation_ref": "left", "source_pointer": "/common_specification/oracle/operations/0/feedback_quality/code", "status": "known"})
        with self.assertRaises(TagError):
            project_tags(p, f)

    def test_duplicate_operation_id_is_not_local_match(self):
        p = profile()
        p["common_specification"]["oracle"]["operations"].append({"id": "right", "operation_code": "other", "precision": "stochastic"})
        self.assertEqual(match_interface(p, {"operation_ref": "right", "precision": "exact"})["state"], "unknown")

    def test_conflicting_precision_fields_unknown(self):
        p = profile()
        p["common_specification"]["oracle"]["operations"][0]["precision"] = "stochastic"
        self.assertEqual(match_interface(p, {"precision": "exact"})["state"], "unknown")

    def test_view_source_pointer_cannot_be_common_fact(self):
        p = profile()
        f = facts(p)
        f[3]["source_pointer"] = "/views/0/algorithms/randomization"
        with self.assertRaises(TagError):
            project_tags(p, f)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.atlas = Atlas(self.temp.name)

    def publish(self, p=None, key="first"):
        p = p or profile()
        prepared = self.atlas.prepare(p, facts(p), self.atlas.version(p["setting_id"]))
        return prepared, self.atlas.commit(prepared, approve(prepared), key)

    def test_commit_read_five_files_and_idempotency(self):
        prepared, receipt = self.publish()
        self.assertEqual(receipt["status"], "committed")
        self.assertEqual(self.atlas.version("MATRIX_EXAMPLE"), receipt["version"])
        self.assertEqual(self.atlas.commit(prepared, approve(prepared), "first"), receipt)
        for name in store_module.FILES:
            self.assertEqual(self.atlas.read("MATRIX_EXAMPLE", name)["setting_id"], "MATRIX_EXAMPLE")

    def test_changed_request_cannot_reuse_idempotency_key(self):
        self.publish()
        p = self.atlas.read("MATRIX_EXAMPLE")
        p["title"] = "Changed title"
        prepared = self.atlas.prepare(p, facts(p), self.atlas.version(p["setting_id"]))
        with self.assertRaises(AtlasConflict):
            self.atlas.commit(prepared, approve(prepared), "first")

    def test_active_bound_needs_individual_approval(self):
        p = profile()
        prepared = self.atlas.prepare(p, facts(p))
        review = approve(prepared)
        review["approved_bound_ids"] = []
        with self.assertRaises(AtlasValidationError):
            self.atlas.commit(prepared, review, "x")
        self.assertIsNone(self.atlas.version(p["setting_id"]))

    def test_review_can_be_validated_before_handoff_without_writing(self):
        p = profile()
        prepared = self.atlas.prepare(p, facts(p))
        self.assertIsNone(self.atlas.validate_review(prepared, approve(prepared)))
        bad = approve(prepared)
        bad["approved_bound_ids"] = []
        with self.assertRaises(AtlasValidationError):
            self.atlas.validate_review(prepared, bad)
        self.assertIsNone(self.atlas.version(p["setting_id"]))
        self.assertFalse((self.atlas.state / "receipts").exists())

    def test_local_relative_schema_refs_and_missing_ref_diagnostic(self):
        folder = self.atlas.data / "schemas"
        folder.mkdir(parents=True)
        main = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://atlas.invalid/schemas/profile.schema.json", "type": "object", "properties": {"setting_id": {"$ref": "common.schema.json#/$defs/setting_id"}}}
        common = {"$defs": {"setting_id": {"type": "string", "pattern": "^MATRIX_"}}}
        (folder / "profile.schema.json").write_text(json.dumps(main))
        (folder / "common.schema.json").write_text(json.dumps(common))
        p = profile()
        prepared = self.atlas.prepare(p, facts(p))
        self.assertIsNone(self.atlas.validate_review(prepared, approve(prepared)))
        invalid = profile("WRONG_PREFIX")
        with self.assertRaises(AtlasValidationError):
            self.atlas.prepare(invalid, facts(invalid))
        (folder / "common.schema.json").unlink()
        with patch("urllib.request.urlopen") as network:
            with self.assertRaisesRegex(AtlasValidationError, "schema reference cannot be resolved locally"):
                self.atlas.prepare(p, facts(p))
            network.assert_not_called()

    def test_explicit_ineligible_or_quarantined_reference_is_rejected(self):
        for status in ("quarantined", "withdrawn", "ineligible"):
            with self.subTest(status=status):
                p = profile()
                p["bounds"][0].update(status=status, eligible_for_bracket=False, included_in_bracket=False)
                with self.assertRaises(AtlasValidationError):
                    self.atlas.prepare(p, facts(p))
        p = profile()
        p["bounds"][0]["eligible_for_bracket"] = False
        with self.assertRaises(AtlasValidationError):
            self.atlas.prepare(p, facts(p))

    def test_bracket_row_references_require_approval(self):
        p = profile()
        p["bounds"][0].pop("eligible_for_bracket")
        p["comparisons"][0]["bracket"] = {"upper_refs": [], "lower_refs": []}
        p["bracket_rows"] = [{"row_id": "row", "comparison_id": "c", "upper_refs": ["u"]}]
        prepared = self.atlas.prepare(p, facts(p))
        bad = approve(prepared)
        bad["approved_bound_ids"] = []
        with self.assertRaises(AtlasValidationError):
            self.atlas.validate_review(prepared, bad)
        self.assertIsNone(self.atlas.validate_review(prepared, approve(prepared)))

    def test_bracket_row_unknown_or_quarantined_references_rejected(self):
        p = profile()
        p["bracket_rows"] = [{"row_id": "row", "upper_refs": ["missing"]}]
        with self.assertRaises(AtlasValidationError):
            self.atlas.prepare(p, facts(p))
        p["bounds"][0].update(status={"code": "quarantined"}, eligible_for_bracket=False)
        p["comparisons"][0]["bracket"] = {"upper_refs": [], "lower_refs": []}
        p["bracket_rows"] = [{"row_id": "row", "lower_refs": ["u"]}]
        with self.assertRaises(AtlasValidationError):
            self.atlas.prepare(p, facts(p))

    def test_partial_document_retains_unadopted_quarantined_bound(self):
        p = profile()
        isolated = deepcopy(p["bounds"][0])
        isolated.update(id="quarantined_claim", status="quarantined", eligible_for_bracket=False, included_in_bracket=False)
        p["bounds"].append(isolated)
        prepared = self.atlas.prepare(p, facts(p))
        review = approve(prepared)
        review["issues"] = [{"blocks": ["bound"], "subject_refs": ["quarantined_claim"]}]
        self.assertIsNone(self.atlas.validate_review(prepared, review))
        self.assertEqual(self.atlas.commit(prepared, review, "partial-document")["status"], "committed")

    def test_scientific_issue_can_remain_if_not_publication_block(self):
        p = profile()
        prepared = self.atlas.prepare(p, facts(p))
        review = approve(prepared)
        review["issues"] = [{"issue_id": "old-proof", "blocks": ["bound"], "subject_refs": ["quarantined-bound"]}]
        self.assertEqual(self.atlas.commit(prepared, review, "x")["status"], "committed")

    def test_bad_review_and_frozen_mutation_block(self):
        p = profile()
        prepared = self.atlas.prepare(p, facts(p))
        review = approve(prepared)
        review["verdict"] = "revise"
        with self.assertRaises(AtlasValidationError):
            self.atlas.commit(prepared, review, "x")
        prepared["files"]["profile.json"]["title"] = "mutated"
        with self.assertRaises(AtlasValidationError):
            self.atlas.commit(prepared, approve(prepared), "x")

    def test_metadata_unknown_fields_preserved(self):
        p = profile()
        p["future_extension"] = {"trace": ["retain"]}
        self.publish(p)
        path = self.atlas.settings / p["setting_id"] / "machine_tags.json"
        machine = json.loads(path.read_text())
        machine["future_index"] = {"retain": True}
        path.write_bytes(store_module.json_bytes(machine))
        update = deepcopy(p)
        del update["future_extension"]
        update["title"] = "Updated exact matrix recovery"
        prepared = self.atlas.prepare(update, facts(update), self.atlas.version(p["setting_id"]))
        self.assertEqual(prepared["files"]["profile.json"]["future_extension"], p["future_extension"])
        self.assertEqual(prepared["files"]["machine_tags.json"]["future_index"], {"retain": True})

    def test_removed_old_ids_rejected(self):
        p = profile()
        p["aliases"] = [{"legacy_id": "old_matrix", "view_id": "randomized"}]
        self.publish(p)
        p["aliases"] = []
        with self.assertRaises(AtlasValidationError):
            self.atlas.prepare(p, facts(p), self.atlas.version(p["setting_id"]))

    def test_changed_model_text_does_not_inherit_old_fact(self):
        p = profile()
        p["common_specification"]["model"]["summary"] = "The declared functions are convex."
        old = facts(p)
        model = next(f for f in old if f["axis"] == "MODEL")
        model.update(concept_id="MODEL:convexity:convex", value="convex")
        prepared = self.atlas.prepare(p, old, None)
        self.atlas.commit(prepared, approve(prepared), "convex-initial")
        changed = deepcopy(p)
        changed["common_specification"]["model"]["summary"] = "A corrected instance class; convexity has not been established."
        new = [f for f in facts(changed) if f["axis"] != "MODEL"]
        amended = self.atlas.prepare(changed, new, self.atlas.version(p["setting_id"]))
        features = amended["files"]["machine_tags.json"]["features"]
        self.assertFalse(any(f["concept_id"] == "MODEL:convexity:convex" and f["status"] == "known" for f in features))

    def test_explicit_unknown_replaces_same_concept_known(self):
        p = profile()
        self.publish(p)
        new = facts(p)
        model = next(f for f in new if f["axis"] == "MODEL")
        model["status"] = "unknown"
        prepared = self.atlas.prepare(p, new, self.atlas.version(p["setting_id"]))
        features = [f for f in prepared["files"]["machine_tags.json"]["features"] if f["concept_id"] == model["concept_id"]]
        self.assertTrue(features)
        self.assertTrue(all(f["status"] == "unknown" for f in features))

    def test_explicit_same_group_correction_supersedes_old_value(self):
        p = profile()
        self.publish(p)
        new = facts(p)
        model = next(f for f in new if f["axis"] == "MODEL")
        model.update(concept_id="MODEL:structure:general_matrix", value="general_matrix")
        prepared = self.atlas.prepare(p, new, self.atlas.version(p["setting_id"]))
        ids = {f["concept_id"] for f in prepared["files"]["machine_tags.json"]["features"]}
        self.assertIn("MODEL:structure:general_matrix", ids)
        self.assertNotIn("MODEL:structure:arbitrary_real_matrix", ids)

    def test_stale_tag_hash_cannot_be_inherited(self):
        p = profile()
        self.publish(p)
        path = self.atlas.settings / p["setting_id"] / "machine_tags.json"
        machine = json.loads(path.read_text())
        machine["profile_sha256"] = "0" * 64
        path.write_bytes(store_module.json_bytes(machine))
        new = [f for f in facts(p) if f["axis"] != "MODEL"]
        prepared = self.atlas.prepare(p, new, self.atlas.version(p["setting_id"]))
        self.assertFalse(prepared["tag_inheritance"]["legacy_hash_verified"])
        self.assertFalse(any(f["axis"] == "MODEL" for f in prepared["files"]["machine_tags.json"]["features"]))

    def test_derived_files_not_science_version(self):
        self.publish()
        v = self.atlas.version()
        folder = self.atlas.data / "vocabulary"
        folder.mkdir(parents=True)
        (folder / "browse_facets.json").write_text('{"rendered":true}')
        self.assertEqual(self.atlas.version(), v)
        (folder / "concepts.json").write_text('{"concepts":[]}')
        self.assertNotEqual(self.atlas.version(), v)

    def test_new_setting_requires_inventory_recheck(self):
        p = profile("NEW_ONE")
        prepared = self.atlas.prepare(p, facts(p))
        self.publish(profile("OTHER"))
        with self.assertRaises(AtlasConflict):
            self.atlas.commit(prepared, approve(prepared), "new-one")

    def test_independent_existing_update_not_false_conflict(self):
        self.publish(profile("ONE"), "one")
        self.publish(profile("TWO"), "two")
        p1 = self.atlas.read("ONE")
        p2 = self.atlas.read("TWO")
        p1["title"] += " updated"
        p2["title"] += " updated"
        a = self.atlas.prepare(p1, facts(p1), self.atlas.version("ONE"))
        b = self.atlas.prepare(p2, facts(p2), self.atlas.version("TWO"))
        self.atlas.commit(a, approve(a), "one-update")
        self.assertEqual(self.atlas.commit(b, approve(b), "two-update")["status"], "committed")

    def test_partial_transaction_recovers_without_model(self):
        p = profile()
        prepared = self.atlas.prepare(p, facts(p))
        real_atomic = store_module._atomic
        def interrupted(path, data):
            real_atomic(path, data)
            if path == self.atlas.settings / p["setting_id"] / "identity.json":
                raise OSError("simulated interruption after a durable file")
        with patch.object(store_module, "_atomic", interrupted), self.assertRaises(OSError):
            self.atlas.commit(prepared, approve(prepared), "crash")
        self.assertTrue((self.atlas.state / "pending.json").exists())
        recovered = Atlas(self.temp.name)
        self.assertFalse((recovered.state / "pending.json").exists())
        self.assertEqual(recovered.version(p["setting_id"]), prepared["version"])
        self.assertEqual(recovered.commit(prepared, approve(prepared), "crash")["status"], "committed")

    def test_external_mutation_during_recovery_not_overwritten(self):
        p = profile()
        prepared = self.atlas.prepare(p, facts(p))
        real_atomic = store_module._atomic
        def interrupted(path, data):
            real_atomic(path, data)
            if path == self.atlas.settings / p["setting_id"] / "profile.json":
                raise OSError("stop")
        with patch.object(store_module, "_atomic", interrupted), self.assertRaises(OSError):
            self.atlas.commit(prepared, approve(prepared), "crash")
        path = self.atlas.settings / p["setting_id"] / "profile.json"
        path.write_text('{"external":"change"}')
        with self.assertRaises(AtlasConflict):
            Atlas(self.temp.name)
        self.assertEqual(json.loads(path.read_text()), {"external": "change"})

    def test_all_candidates_paginated_unknown_not_excluded(self):
        for n in range(4):
            self.publish(profile(f"SETTING_{n}"), f"insert-{n}")
        query = {"title": "A completely different problem", "tag_facts": []}
        first = retrieve(self.atlas, query, limit=2)
        second = retrieve(self.atlas, query, limit=2, offset=2)
        self.assertEqual(first["total"], 4)
        self.assertTrue(first["has_more"])
        self.assertEqual(len({x["setting_id"] for x in first["candidates"] + second["candidates"]}), 4)
        self.assertEqual(first["query"]["hard_exclusions"], 0)

    def test_scope_matrix_and_exact(self):
        self.publish()
        result = scope_search(self.atlas, [{"concept_id": "TASK:family:matrix_computation"}, {"concept_id": "ORACLE:quality:exact"}])
        self.assertEqual(result["matched_count"], 1)
        self.assertEqual(result["items"][0]["setting_id"], "MATRIX_EXAMPLE")


class LegacyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        source = Path(__file__).parent / "fixtures" / "native_atlas"
        shutil.copytree(source, self.temp.name, dirs_exist_ok=True)
        self.atlas = Atlas(self.temp.name)

    def test_two_native_profiles_and_aliases_read(self):
        catalog = self.atlas.catalog()
        self.assertEqual(len(catalog), 2)
        row = next(x for x in catalog if x["setting_id"] == "SO_ZO_E01")
        self.assertIn("SO_ZO_E01_det", row["aliases"])
        result = retrieve(self.atlas, {"candidate_id": "SO_ZO_E01_det", "title": "new candidate", "tag_facts": []})
        self.assertEqual(result["candidates"][0]["setting_id"], "SO_ZO_E01")

    @unittest.skipUnless(importlib.util.find_spec("jsonschema"), "native target schema validation requires jsonschema")
    def test_native_schema_compatible_prepare_and_commit(self):
        sid = "CV_S_STRICT_MATRIX_SADDLE_COMPARE"
        p = self.atlas.read(sid)
        p["summary"] = "Synthetic maintenance of an existing fixture; not a new literature result."
        p["summary_status"] = canonical_summary(p)
        p["joint_analysis"] = analysis_template(p)
        p["refinement_pending"] = {"reason": "Determine native parameter roles in this retained fixture",
                                   "next_evidence": "Re-read the comparison domains", "source_refs": [p["references"][0]["id"]]}
        # Use tag facts with exact mappings in the original structure; retain unknown for other axes.
        prepared = self.atlas.prepare(p, [], self.atlas.version(sid))
        review = {"verdict": "approve", "prepared_hash": prepared["bundle_hash"], "approved_bound_ids": [b["id"] for b in p["bounds"]], "issues": [], "joint_checks": JOINT_CHECKS}
        result = self.atlas.commit(prepared, review, "native-fixture")
        self.assertEqual(result["status"], "committed")
        self.assertEqual(self.atlas.read(sid)["title"], p["title"])


if __name__ == "__main__":
    unittest.main()
