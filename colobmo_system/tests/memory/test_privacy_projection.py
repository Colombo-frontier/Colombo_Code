"""Privacy export identity checks; simulated reviews are temporary fixtures only."""
from copy import deepcopy
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[2]
MEMORY_AGENT = PROJECT / "colombo_memory_agent"
sys.path[:0] = [str(PROJECT / "src"), str(MEMORY_AGENT / "runtime")]

from colombo.memory.contracts import ContractError, digest, validate_review
from colombo.memory.integration import _validate_store
from colombo.memory.retrieval import (Reader, PRIVACY_PROJECTION_SCHEMA,
                                      PRIVACY_PROJECTION_TRANSFORMATION)
from colombo.memory.store import atomic_json, read_json
from colombo_memory_agent.store import WriterStore

SOURCE = next(record for record in read_json(MEMORY_AGENT / "examples/complete_candidate_records.json")
              if record["kind"] == "source")


def fixture_review(proposal):
    return {"proposal_digest": proposal["digest"], "curator_run_id": proposal["curator_run_id"],
            "reviewer_run_id": "TEST-REVIEWER", "backend": "fake", "coverage": ["TEST ONLY"],
            "items": [{"id": record["id"], "record_hash": digest(record), "decision": "accept",
                       "content_fidelity": "checked", "navigation_fidelity": "checked",
                       "proof_review": "statement_and_source_checked", "issues": []}
                      for record in proposal["records"]]}


def snapshot(root):
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file()}


class PrivacyProjectionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store = WriterStore(self.root / "memory")
        self.store.initialize()
        self.proposal = self.store.prepare([deepcopy(SOURCE)], curator_run_id="TEST-CURATOR", job_id="TEST-JOB")
        self.review = fixture_review(self.proposal)
        self.store.publish(self.proposal, self.review, authorized=True, allow_test_receipt=True)

    def project(self):
        original = self.store.all_records()[0]
        record = deepcopy(original)
        material = record["content"]["original_material"][0]
        material["artifact_ref"] = "urn:sha256:" + material["content_hash"]
        row = {"id": record["id"], "kind": record["kind"], "revision": record["revision"],
               "original_content_hash": digest(original), "projected_content_hash": digest(record),
               "change_pointers": ["#/content/original_material/0/artifact_ref"]}
        metadata = {"schema": PRIVACY_PROJECTION_SCHEMA, "no_new_review": True,
                    "transformation": PRIVACY_PROJECTION_TRANSFORMATION,
                    "original_content_hash": row["original_content_hash"],
                    "projected_content_hash": row["projected_content_hash"]}
        manifest = self.store.manifest()
        entry = manifest["entries"][record["id"]]
        entry.update(content_hash=digest(record), path=self.store._object_path(record), privacy_projection=metadata)
        for receipt in manifest["receipts"].values():
            receipt["status"] = "privacy_projected"
            for ref in receipt["published_refs"]:
                if ref["id"] == record["id"]:
                    ref["content_hash"] = digest(record)
        atomic_json(self.store._state_inside(entry["path"]), record)
        atomic_json(self.store.current_path(record["id"], record["kind"]), record)
        self.store._commit_generation(manifest)
        mapping = {"schema": PRIVACY_PROJECTION_SCHEMA, "no_new_review": True, "records": [row]}
        atomic_json(self.store.state_root / "PRIVACY_PROJECTION.json", mapping)
        return row, mapping

    def test_normal_publication_keeps_exact_revision_meaning(self):
        before = snapshot(self.root)
        _validate_store(self.store)
        publication = Reader(self.store).search()["items"][0]["publication"]
        self.assertNotIn("privacy_projection", publication)
        self.assertIn("this exact revision", publication["meaning"])
        self.assertEqual(publication["review_digest"], digest(self.review))
        self.assertEqual(before, snapshot(self.root))

    def test_projection_discloses_original_review_identity_without_new_review(self):
        row, _ = self.project()
        before = snapshot(self.root)
        _validate_store(self.store)
        card = Reader(self.store).search()["items"][0]
        publication = card["publication"]
        self.assertEqual(publication["review_digest"], digest(self.review))
        self.assertEqual(publication["review_scope"]["record_hash"], row["original_content_hash"])
        self.assertEqual(card["ref"]["content_hash"], row["projected_content_hash"])
        self.assertEqual(publication["privacy_projection"]["original_content_hash"], row["original_content_hash"])
        self.assertIn(row["original_content_hash"], publication["meaning"])
        self.assertIn(row["projected_content_hash"], publication["meaning"])
        self.assertIn("No new independent review", publication["meaning"])
        self.assertNotIn("this exact revision", publication["meaning"])
        self.assertTrue(Reader(self.store).read(card["ref"])["complete"])
        self.assertEqual(before, snapshot(self.root))

    def test_unchanged_export_mapping_keeps_the_original_review_meaning(self):
        record = self.store.all_records()[0]
        row = {"id": record["id"], "kind": record["kind"], "revision": record["revision"],
               "original_content_hash": digest(record), "projected_content_hash": digest(record),
               "change_pointers": []}
        atomic_json(self.store.state_root / "PRIVACY_PROJECTION.json",
                    {"schema": PRIVACY_PROJECTION_SCHEMA, "no_new_review": True, "records": [row]})
        _validate_store(self.store)
        publication = Reader(self.store).search()["items"][0]["publication"]
        self.assertNotIn("privacy_projection", publication)
        self.assertIn("this exact revision", publication["meaning"])

    def test_tampered_original_mapping_cannot_rebind_a_recorded_review(self):
        _, mapping = self.project()
        mapping["records"][0]["original_content_hash"] = "0" * 64
        atomic_json(self.store.state_root / "PRIVACY_PROJECTION.json", mapping)
        with self.assertRaisesRegex(ContractError, "original review and global mapping"):
            _validate_store(self.store)

    def test_tampered_projected_hash_is_not_a_published_identity(self):
        _, mapping = self.project()
        mapping["records"][0]["projected_content_hash"] = "0" * 64
        atomic_json(self.store.state_root / "PRIVACY_PROJECTION.json", mapping)
        with self.assertRaisesRegex(ContractError, "not a published revision"):
            _validate_store(self.store)

    def test_projection_requires_explicit_no_new_review_declaration(self):
        _, mapping = self.project()
        for case in ("missing", "false"):
            with self.subTest(case=case):
                changed = deepcopy(mapping)
                if case == "missing":
                    changed.pop("no_new_review")
                else:
                    changed["no_new_review"] = False
                atomic_json(self.store.state_root / "PRIVACY_PROJECTION.json", changed)
                with self.assertRaisesRegex(ContractError, "no-new-review declaration"):
                    _validate_store(self.store)

    def test_flagged_publication_requires_global_mapping(self):
        self.project()
        (self.store.state_root / "PRIVACY_PROJECTION.json").unlink()
        with self.assertRaisesRegex(ContractError, "require the global mapping"):
            _validate_store(self.store)

    def test_projection_cannot_turn_a_lead_into_a_reviewed_publication(self):
        _, mapping = self.project()
        lead = deepcopy(SOURCE)
        lead["id"] = "src.test_unreviewed"
        lead["evidence"]["readiness"] = "lead"
        self.store.install_leads([lead])
        mapping["records"].append({"id": lead["id"], "kind": "source", "revision": 1,
                                   "original_content_hash": "1" * 64,
                                   "projected_content_hash": "2" * 64,
                                   "change_pointers": ["#/content/original_material/0/artifact_ref"]})
        atomic_json(self.store.state_root / "PRIVACY_PROJECTION.json", mapping)
        with self.assertRaisesRegex(ContractError, "not a published revision"):
            _validate_store(self.store)
        lead_card = next(card for card in Reader(self.store).search(include_leads=True)["items"]
                         if card["ref"]["id"] == lead["id"])
        self.assertIsNone(lead_card["publication"])
        candidate = deepcopy(self.proposal)
        candidate["records"][0]["evidence"]["readiness"] = "lead"
        with self.assertRaisesRegex(ContractError, "Lead cannot be canonically published"):
            validate_review(candidate, fixture_review(candidate))

    def test_future_native_publication_remains_ordinary_outside_export_mapping(self):
        self.project()
        record = deepcopy(SOURCE)
        record["id"] = "src.test_future_native"
        proposal = self.store.prepare([record], curator_run_id="TEST-FUTURE-CURATOR", job_id="TEST-FUTURE-JOB")
        review = fixture_review(proposal)
        self.store.publish(proposal, review, authorized=True, allow_test_receipt=True)
        _validate_store(self.store)
        card = next(card for card in Reader(self.store).search()["items"] if card["ref"]["id"] == record["id"])
        self.assertNotIn("privacy_projection", card["publication"])
        self.assertIn("this exact revision", card["publication"]["meaning"])
        self.assertEqual(card["publication"]["review_digest"], digest(review))

    def test_future_native_revision_preserves_the_projected_historical_reference(self):
        self.project()
        historical = Reader(self.store).search()["items"][0]["ref"]
        old_record = Reader(self.store)._record(historical)
        record = deepcopy(old_record)
        record["summary"] += " Test-only next revision."
        proposal = self.store.prepare([record], curator_run_id="TEST-NEXT-CURATOR", job_id="TEST-NEXT-JOB")
        review = fixture_review(proposal)
        self.store.publish(proposal, review, authorized=True, allow_test_receipt=True)
        _validate_store(self.store)
        card = Reader(self.store).search()["items"][0]
        self.assertEqual(card["ref"]["revision"], 2)
        self.assertNotIn("privacy_projection", card["publication"])
        self.assertIn("this exact revision", card["publication"]["meaning"])
        self.assertEqual(Reader(self.store)._record(historical), old_record)

    def test_compact_scientific_objects_support_pinned_reads_and_future_publication(self):
        self.project()
        manifest = self.store.manifest()
        entry = next(iter(manifest["entries"].values()))
        pinned = {key: entry[key] for key in ("id", "kind", "revision", "content_hash", "tier")}
        original = self.store.get(entry["id"])
        old_path = self.store._state_inside(entry["path"])
        entry["path"] = "objects/" + entry["content_hash"] + ".json"
        compact = self.store._state_inside(entry["path"])
        compact.parent.mkdir()
        old_path.rename(compact)
        self.store._commit_generation(manifest)
        _validate_store(self.store)
        self.assertEqual(Reader(self.store)._record(pinned), original)

        updated = deepcopy(original)
        updated["summary"] += " Synthetic next publication."
        proposal = self.store.prepare([updated], curator_run_id="TEST-COMPACT-CURATOR", job_id="TEST-COMPACT-JOB")
        self.store.publish(proposal, fixture_review(proposal), authorized=True, allow_test_receipt=True)
        _validate_store(self.store)
        self.assertEqual(self.store.get(entry["id"])["revision"], 2)
        self.assertEqual(Reader(self.store)._record(pinned), original)


if __name__ == "__main__":
    unittest.main()
