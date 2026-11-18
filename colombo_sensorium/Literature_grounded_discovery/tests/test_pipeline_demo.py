"""Offline end-to-end acceptance; all scientific judgments are predetermined by the example script and are not a real model evaluation."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from oracle_atlas.atlas import Atlas


MODULE_PATH = Path(__file__).resolve().parents[1] / "examples" / "offline_demo.py"
SPEC = importlib.util.spec_from_file_location("oracle_atlas_synthetic_demo", MODULE_PATH)
DEMO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DEMO)


class OfflinePipelineDemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.engine, cls.backend, cls.bibliography, cls.request = DEMO.setup_demo(Path(cls.temp.name))
        cls.first = cls.engine.scan(cls.request)
        cls.first_calls = cls.backend.calls
        cls.versions = {row["setting_id"]: row["profile_version"] for row in cls.engine.atlas.catalog()}
        cls.second = cls.engine.scan(cls.request)
        cls.cases = {cls.engine.artifacts.get(cls.engine.ws.case(cid)["candidate_ref"])["data"]["synthetic_branch"]: cls.engine.ws.case(cid) for cid in cls.first["cases"]}

    @classmethod
    def tearDownClass(cls):
        cls.engine.ws.db.close()
        cls.temp.cleanup()

    def test_one_verified_fixture_reaches_three_receipts(self):
        tools = {row["name"] for row in self.engine.ws.query("SELECT DISTINCT name FROM tool_calls")}
        self.assertTrue({"draft_outline", "draft_read_batch", "exact_check"}.issubset(tools))
        self.assertEqual(self.first["verified_year_papers"], 1)
        self.assertEqual(self.first["counts"], {"candidates": 3, "committed": 3, "no_change": 0, "remaining": 0})
        self.assertEqual(set(self.cases), {"fill_bound", "add_view", "new_setting"})
        for case in self.cases.values():
            self.assertEqual(case["state"], "committed", case.get("diagnostic"))
            receipt = self.engine.artifacts.get(case["receipt_ref"])
            self.assertEqual(receipt["kind"], "receipt")
            self.assertEqual(receipt["data"]["status"], "committed")
            self.assertEqual(len(receipt["data"]["files"]), 5)

    def test_existing_bound_update_keeps_profile_and_alias(self):
        p = self.engine.atlas.read("DEMO_BINARY_VALUE")
        self.assertEqual([v["view_id"] for v in p["views"]], ["deterministic"])
        self.assertEqual({b["id"] for b in p["bounds"]}, {"deterministic_upper", "deterministic_lower"})
        self.assertEqual(p["aliases"], [{"legacy_id": "DEMO_BINARY_VALUE_det", "view_id": "deterministic"}])
        self.assertEqual(p["comparisons"][0]["bracket"]["lower_refs"], ["deterministic_lower"])

    def test_new_view_is_added_to_existing_setting(self):
        p = self.engine.atlas.read("DEMO_SIGNED_LINEAR")
        self.assertEqual({v["view_id"] for v in p["views"]}, {"deterministic", "randomized"})
        self.assertEqual(len(p["bounds"]), 4)
        upper = next(b for b in p["bounds"] if b["id"] == "randomized_upper")
        self.assertEqual(upper["witness_type"], "deterministic")
        self.assertEqual(len(self.engine.atlas.catalog()), 3)

    def test_new_view_preserves_unchanged_old_view_tags(self):
        tags = self.engine.atlas.read("DEMO_SIGNED_LINEAR", "machine_tags.json")
        algorithms = {row["concept_id"]: set(row["view_ids"]) for row in tags["features"] if row["axis"] == "ALGORITHMS" and row.get("status") == "known"}
        self.assertIn("deterministic", algorithms.get("ALGORITHMS:randomization:deterministic", set()))
        self.assertIn("randomized", algorithms.get("ALGORITHMS:randomization:private_randomness_allowed", set()))

    def test_new_setting_has_the_distinct_native_interface(self):
        p = self.engine.atlas.read("DEMO_QUADRATIC_GRADIENT")
        self.assertEqual(p["common_specification"]["oracle"]["operations"][0]["returns"], ["gradient"])
        self.assertTrue(p["provenance"]["synthetic"])
        self.assertIn("fully_optimal", [b["code"] for b in p["summary_status"]["badges"]])

    def test_independent_review_subjects_and_job_ownership(self):
        ws = self.engine.ws
        producer = ws.job(self.first["papers"][0]["extraction_job"])
        extraction_review = ws.job(self.first["papers"][0]["review_job"])
        self.assertNotEqual(producer["id"], extraction_review["id"])
        for case in self.cases.values():
            for field, subject in (("extraction_review_ref", "extraction_ref"), ("identity_review_ref", "identity_ref"), ("profile_review_ref", "proposal_ref")):
                review = self.engine.artifacts.get(case[field])
                self.assertEqual(review["data"]["subject_ref"], case[subject])
                self.assertNotEqual(review["producer"], self.engine.artifacts.get(case[subject])["producer"])
            self.assertNotEqual(case["jobs"]["matcher"], case["jobs"]["identity_reviewer"])
            self.assertEqual(ws.job(case["jobs"]["profile_reviewer"])["role"], "profile_reviewer")

    def test_original_sources_and_formal_proofs_survive_handoffs(self):
        for case in self.cases.values():
            research = self.engine.artifacts.get(case["research_ref"])["data"]
            self.assertTrue(research["proof_refs"])
            self.assertTrue(research["result_refs"])
            for ref in research["result_refs"]:
                card = self.engine.artifacts.get(ref)["data"]
                self.assertEqual(card["origin"], "analyst_derivation")
                self.assertEqual(card["proof_refs"], research["proof_refs"])
                for locator in card["source_locators"]:
                    source = self.engine.artifacts.get(locator["source_ref"])
                    self.assertEqual(source["kind"], "source")
                    self.assertEqual(source["data"]["version"], locator["version"])
                    self.assertTrue(source["data"]["metadata"]["synthetic"])

    def test_actual_tools_drafts_retrieval_and_memory_isolation(self):
        calls = self.engine.ws.query("SELECT name,result FROM tool_calls")
        names = {row["name"] for row in calls}
        self.assertTrue({"artifact_put", "draft_create", "draft_patch", "draft_freeze", "atlas_search", "atlas_read", "source_read", "schema_read", "bibliography_search"}.issubset(names))
        self.assertEqual(sum(row["name"] == "atlas_search" for row in calls), 6)
        self.assertEqual(self.backend.observed_tool_errors, [])
        self.assertTrue(self.backend.review_memory)
        self.assertTrue(all(row["notes"] == [] for row in self.backend.review_memory))

    def test_repeat_scan_reuses_validated_handoffs_and_receipts(self):
        self.assertEqual(self.backend.calls, self.first_calls)
        self.assertEqual(self.bibliography.calls, 1)
        self.assertEqual(self.first["cases"], self.second["cases"])
        self.assertEqual(self.second["counts"], self.first["counts"])
        self.assertEqual(self.versions, {row["setting_id"]: row["profile_version"] for row in self.engine.atlas.catalog()})

    def test_context_envelope_never_contains_the_whole_archive(self):
        requests = self.engine.ws.query("SELECT request FROM calls")
        self.assertGreater(len(requests), 20)
        for row in requests:
            request = json.loads(row["request"])
            self.assertLess(len(json.dumps(request, ensure_ascii=False)), 65000)
        initial_jobs = self.engine.ws.query("SELECT inputs FROM jobs")
        self.assertTrue(all(len(row["inputs"]) < 3000 for row in initial_jobs))


if __name__ == "__main__":
    unittest.main()
