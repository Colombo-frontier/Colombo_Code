"""The V4 database owns aggregate documents; exports and references are projections."""
import copy
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import tempfile
import unittest

from colombo.configuration import load_config
from colombo.brain.cell_package import build_package
from colombo.brain.research_store import Store, StoreError
from controller_fixtures import event_task


class AggregateStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        source = self.base / "material.txt"
        source.write_text("RAW_ATTACHMENT_UNIQUE_TEXT", encoding="utf-8")
        self.store = Store.create(self.base / "run", "Aggregate storage target", [], load_config(), [source])

    def tearDown(self):
        self.temp.cleanup()

    def plan(self):
        spec = event_task("Fixed task")
        spec["instructions"] = "DEFINITION_UNIQUE_TEXT"
        payload = {"rationale": "One fixed definition", "tasks": [spec]}
        ref = self.store.write_record("plan", payload, "submission:C00001")
        identity = self.store.plan_identity(ref)
        self.store.set_meta(round_no=identity["round_no"], round_data={**identity, "plan_ref": ref}, phase="preparing")
        return payload, ref, identity

    def candidate(self):
        self.plan()
        event = {"id": "E00001", "version": 1, "wave_id": "W0001"}
        self.store.set_meta(event_data=event)
        payload = {"summary": "Candidate", "result_refs": [], "prunes": [],
            "update": {"admissions": [], "proof_draft": {"title": "Proof", "body": "FULL_PROOF_UNIQUE_TEXT"},
                       "progress": {"overall": "in_progress"}, "rechecked_step_ids": []},
            "next_action": "continue", "rationale": "More evidence needed"}
        ref = self.store.write_record("assessment", payload, "submission:C00002")
        return payload, ref

    def test_plan_ids_and_definition_are_allocated_once_with_receipt(self):
        payload, ref, identity = self.plan()
        self.assertEqual(self.store.write_record("plan", payload, "submission:C00001"), ref)
        self.assertEqual(self.store.request_record("submission:C00001"), ref)
        self.assertEqual(identity["jobs"][0]["task_id"], "T0001")
        self.assertEqual(self.store.get_meta("task_counter"), 1)
        self.assertEqual(self.store.read_record(ref), payload)
        self.assertEqual(json.dumps(self.store.read_document("research")).count("DEFINITION_UNIQUE_TEXT"), 1)
        with self.assertRaises(StoreError):
            self.store.write_record("plan", {**payload, "rationale": "Different"}, "submission:C00001")

    def test_database_has_three_documents_and_no_record_body_ledger(self):
        self.candidate()
        with self.store._connect() as db:
            tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertNotIn("records", tables)
            self.assertNotIn("tasks", tables)
            self.assertEqual({r[0] for r in db.execute("SELECT name FROM documents")},
                             {"research", "proof_draft", "working_notes"})
            columns = {r[1] for r in db.execute("PRAGMA table_info(record_requests)")}
            self.assertNotIn("payload", columns)
            bodies = "".join(r[0] for r in db.execute("SELECT payload FROM documents"))
            self.assertEqual(bodies.count("FULL_PROOF_UNIQUE_TEXT"), 1)
        self.assertFalse((self.store.root / "records").exists())

    def test_package_contains_original_file_while_research_keeps_only_refs(self):
        spec = event_task("Read supplied material")
        spec["package"]["items"] = [{"ref": self.store.get_meta("material_refs")[0]["id"],
            "importance": "required", "purpose": "Read the supplied source", "limitations": "Unreviewed"}]
        plan = self.store.write_record("plan", {"rationale": "Use source", "tasks": [spec]})
        job = self.store.plan_jobs(plan)[0]
        destination = self.store.root / "tasks" / job["task_id"] / "input/package"
        manifest = build_package(self.store, job["task_id"], spec, destination)
        copied = destination / manifest["items"][0]["artifacts"][0]["package_path"]
        self.assertEqual(copied.read_text(), "RAW_ATTACHMENT_UNIQUE_TEXT")
        self.assertNotIn("RAW_ATTACHMENT_UNIQUE_TEXT", json.dumps(self.store.read_document("research")))

    def test_fixed_candidate_roundtrip_and_proof_adoption_do_not_copy_proof(self):
        payload, ref = self.candidate()
        proof_ref = self.store.assessment_proof(ref)
        fixed_proof = self.store.public_read(proof_ref)
        self.assertNotIn("proof_draft", self.store.public_read(ref)["update"])
        self.assertEqual(self.store.read_record(ref), payload)
        self.assertEqual(self.store.write_record("assessment", payload, "submission:C00002"), ref)
        self.store.set_meta(event_data={"id": "E00001", "version": 1, "wave_id": "W0001",
            "assessment_ref": ref, "proof_candidate_ref": proof_ref})
        self.store.set_meta(integration={"proof_ref": proof_ref})
        review = self.store.write_record("review", {"review_kind": "proof", "result_ref": None, "verdict": "pass", "findings": []}, "submission:C00003")
        event = self.store.get_meta("event_data")
        self.store.set_meta(event_data={**event, "review_ref": review, "adoption_status": "review_passed"})
        self.assertIsNone(self.store.read_record(proof_ref)["review_ref"])
        self.store.set_meta(event_data={**event, "review_ref": review, "adoption_status": "adopted"}, proof_ref=proof_ref)
        self.assertEqual(self.store.read_record(proof_ref)["review_ref"], review)
        self.assertEqual(self.store.public_read(proof_ref)["proof_draft"], fixed_proof["proof_draft"])
        self.assertEqual(self.store.public_read(proof_ref)["reviews"][review["id"]]["verdict"], "pass")
        self.assertEqual(len(self.store.read_document("proof_draft")["versions"]), 1)
        self.assertEqual(self.store.write_record("assessment", payload, "submission:C00002"), ref)

    def test_exports_share_generation_and_rebuild_from_database(self):
        self.candidate()
        self.store.write_record("note", {"text": "Remember the scope"})
        expected = self.store.export_documents()
        exported = {name: json.loads((self.store.root / (name + ".json")).read_text()) for name in expected}
        self.assertEqual(len({item["generation"] for item in exported.values()}), 1)
        for name in expected:
            self.assertEqual({k: v for k, v in exported[name].items() if k not in {"generation", "storage_version"}}, expected[name])
            (self.store.root / (name + ".json")).unlink()
        self.assertEqual(Store(self.store.root).export_documents(), expected)

    def test_parallel_returns_are_not_lost_and_old_version_refs_are_rejected(self):
        def save(index):
            return Store(self.store.root).write_record("result", {"task_id": f"T{index:04d}",
                "attempt_id": "A0001", "summary": f"RETURN_{index}", "artifacts": []}, f"result:{index}")
        with ThreadPoolExecutor(max_workers=4) as pool:
            refs = list(pool.map(save, range(1, 9)))
        self.assertEqual(self.store.reference_count("result"), 8)
        self.assertEqual(len(self.store.read_document("research")["tasks"]), 8)
        with self.assertRaises(StoreError):
            self.store.read_record({**refs[0], "revision": 2})
        with self.assertRaises(StoreError):
            self.store.read_record({**refs[0], "revision": True})


if __name__ == "__main__":
    unittest.main()
