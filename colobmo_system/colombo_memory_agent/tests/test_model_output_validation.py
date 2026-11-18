"""Malformed model payloads remain bounded, repairable contract failures."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(PACKAGE / "runtime"), str(PACKAGE.parent / "src")]

from colombo.memory.contracts import ContractError, digest, validate_record, validate_review
from colombo.memory.store import read_json
from colombo_memory_agent.store import Store
from colombo_memory_agent.workflow import Workflow
from test_handoff import EXAMPLES, FakeBackend


def theorem():
    record = deepcopy(next(record for record in EXAMPLES if record["kind"] == "theorem"))
    # Contract-only cases do not run prepare, which normally assigns these.
    for source in record["source_refs"]:
        source["source_revision"] = source["source_revision"] or 1
    for link in record["links"]:
        link["target_revision"] = link["target_revision"] or 1
    return record


class ProofSequenceBackend(FakeBackend):
    def __init__(self, malformed_attempts):
        super().__init__()
        self.malformed_attempts = malformed_attempts
        self.curator_attempts = 0

    def run(self, **arguments):
        if arguments["role"] == "curator":
            self.curator_attempts += 1
            self.records = deepcopy(EXAMPLES)
            if self.curator_attempts <= self.malformed_attempts:
                next(record for record in self.records if record["kind"] == "theorem")["content"]["proofs"] = ["malformed proof"]
        return super().run(**arguments)


class ModelOutputContractTests(unittest.TestCase):
    def test_valid_theorem_remains_unchanged(self):
        record = theorem()
        before = digest(record)
        validate_record(record)
        self.assertEqual(digest(record), before)

    def test_proofs_requires_an_array(self):
        for value in (None, "proof", {}, 42):
            with self.subTest(value=value):
                record = theorem()
                record["content"]["proofs"] = value
                with self.assertRaisesRegex(ContractError, r"theorem\.content\.proofs: an array required"):
                    validate_record(record)

    def test_every_proof_requires_an_object(self):
        for value in (None, "malformed proof", [], 42):
            with self.subTest(value=value):
                record = theorem()
                record["content"]["proofs"] = [value]
                with self.assertRaisesRegex(ContractError, r"theorem\.content\.proofs\[0\]: an object required"):
                    validate_record(record)

    def test_malformed_later_proof_is_not_hidden_by_valid_local_argument(self):
        record = theorem()
        record["content"]["proofs"].append("malformed later proof")
        with self.assertRaisesRegex(ContractError, r"proofs\[1\]: an object required"):
            validate_record(record)

    def test_object_with_no_complete_proof_is_still_rejected(self):
        record = theorem()
        record["content"]["proofs"] = [{}]
        with self.assertRaisesRegex(ContractError, "complete local argument"):
            validate_record(record)

    def test_nested_statement_requires_an_object(self):
        record = theorem()
        record["content"]["statement"] = "not a statement object"
        with self.assertRaisesRegex(ContractError, "statement: an object required"):
            validate_record(record)

    def test_navigation_collections_require_arrays(self):
        for field in ("facets", "research_use", "query_aliases"):
            with self.subTest(field=field):
                record = theorem()
                record["navigation"][field] = None
                with self.assertRaisesRegex(ContractError, "navigation." + field):
                    validate_record(record)

    def test_navigation_elements_require_objects(self):
        for field in ("facets", "research_use"):
            with self.subTest(field=field):
                record = theorem()
                record["navigation"][field] = [None]
                with self.assertRaisesRegex(ContractError, "an object required"):
                    validate_record(record)

    def test_facet_evidence_refs_requires_an_array(self):
        record = theorem()
        record["navigation"]["facets"][0]["evidence_refs"] = None
        with self.assertRaisesRegex(ContractError, "facet.evidence_refs"):
            validate_record(record)

    def test_review_collections_and_elements_report_contract_errors(self):
        record = theorem()
        proposal = {"digest": "test-proposal", "curator_run_id": "curator-test", "records": [record]}
        item = {"id": record["id"], "record_hash": digest(record), "decision": "defer",
                "content_fidelity": "not_checked", "navigation_fidelity": "not_checked",
                "proof_review": "not_checked", "issues": []}
        review = {"proposal_digest": proposal["digest"], "curator_run_id": "curator-test",
                  "reviewer_run_id": "reviewer-test", "backend": "fake", "items": [item], "coverage": []}
        mutations = [
            ("items array", lambda value: value.update(items=None), "review.items"),
            ("coverage array", lambda value: value.update(coverage=None), "review.coverage"),
            ("item object", lambda value: value.update(items=[None]), "review item"),
            ("issues array", lambda value: value["items"][0].update(issues=None), "review item.issues"),
            ("issue object", lambda value: value["items"][0].update(issues=[None]), "review issue"),
        ]
        for name, mutate, diagnostic in mutations:
            with self.subTest(name=name):
                candidate = deepcopy(review)
                mutate(candidate)
                with self.assertRaisesRegex(ContractError, diagnostic):
                    validate_review(proposal, candidate)


class ModelOutputRepairTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="colombo-output-validation-")
        self.root = Path(self.temporary.name)
        self.store = Store(self.root / "memory")
        self.store.initialize()
        self.source = self.root / "source.txt"
        self.source.write_text("SYNTHETIC protocol fixture; not independent scientific evidence.")
        self.job = {"job_id": "malformed-proof-repair", "objective": "Synthetic protocol test only",
                    "source_files": [str(self.source)], "focus_anchors": ["synthetic"],
                    "publication_policy": "stage_only", "max_rounds": 2}

    def tearDown(self):
        self.temporary.cleanup()

    def test_malformed_proof_can_be_repaired_in_next_round(self):
        backend = ProofSequenceBackend(malformed_attempts=1)
        result = Workflow(self.store, backend, PACKAGE, jobs_root=self.root / "jobs").run(self.job)
        self.assertEqual(result["status"], "completed")
        self.assertEqual([call["role"] for call in backend.calls], ["curator", "curator", "reviewer"])
        self.assertIn("proofs[0]: an object required", backend.calls[1]["prompt"])
        proposal = self.store.load_proposal(result["proposal_id"])
        for record in proposal["records"]:
            validate_record(record, require_revision=True)
        self.assertEqual(self.store.manifest()["entries"], {})

    def test_persistent_malformed_proofs_exhaust_budget_without_crashing(self):
        backend = ProofSequenceBackend(malformed_attempts=2)
        result = Workflow(self.store, backend, PACKAGE, jobs_root=self.root / "jobs").run(self.job)
        self.assertEqual(result["status"], "budget_exhausted")
        self.assertEqual(result["last_status"], "rejected_candidate")
        self.assertIn("proofs[0]: an object required", result["feedback"]["error"])
        self.assertEqual([call["role"] for call in backend.calls], ["curator", "curator"])
        checkpoint = read_json(self.root / "jobs/malformed-proof-repair/checkpoint.json")
        self.assertEqual(checkpoint["round"], 2)
        self.assertEqual(self.store.manifest()["entries"], {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
