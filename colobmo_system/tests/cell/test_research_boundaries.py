"""Independent integration checks for derived evidence and batch reference roles."""
from __future__ import annotations

import copy
import unittest
from unittest.mock import patch

from colombo.cell.verifier.local_audit import audit
from colombo.cell.verifier.challenge import challenge_argument
from colombo.cell.record_store import Store
from colombo.cell.subcell_dispatch import Tasks
from colombo.shared.file_io import Path
import test_research_records as record_fixture
from test_confirmed_trust import confirmed_packet

ref = record_fixture.ref


class ResearchBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.fixture = record_fixture.ResearchRecordTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root, self.store = self.fixture.root, self.fixture.store

    def test_conflicted_claim_cannot_be_consumed_indirectly_through_supporting_argument(self):
        claim = self.fixture.claim()
        support = self.fixture.certify(self.fixture.candidate(claim))
        self.fixture.certify(self.fixture.candidate(claim, "refutes", proof="Synthetic contrary certificate"))
        self.assertEqual(self.store.get("claims", claim["id"])["current_trust"]["state"], "conflicted")
        self.assertEqual(self.store.get("arguments", support["id"])["current_trust"]["state"], "supported")
        next_target = self.fixture.claim("next", "A further conclusion")
        dependent = self.fixture.candidate(next_target, dependencies=[ref(support)])
        self.assertEqual(dependent["current_trust"]["state"], "dependency_blocked")
        attempted = audit(self.root, "arguments", dependent["id"], dependent["revision"],
                          reviewer=lambda *_: self.fixture.response(dependent))
        self.assertNotEqual(attempted["review"]["payload"]["verdict"], "pass")

    def test_granted_derived_property_loses_support_with_its_granted_argument(self):
        example = self.fixture.example_with_independent_properties()
        parent_argument = self.fixture.certify(self.fixture.property_argument(example, "p1"))
        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
            launch.return_value.pid = 12345
            task = Tasks(self.root).spawn_task(ref(example, property_ids=["p1"]), "Study this property",
                                               context_refs=[ref(parent_argument)])
        child_root = Path(task["workspace"])
        child = Store(child_root / "memory")
        payload = copy.deepcopy(parent_argument["payload"])
        payload.pop("audit_id", None)
        payload["status"] = "candidate"
        candidate = child.archive("arguments", payload, "local-copy")
        local = audit(child_root, "arguments", candidate["id"], candidate["revision"],
                      reviewer=lambda *_: self.fixture.response(candidate))["record"]

        def unfinished(*_):
            raise TimeoutError("Independent review has not completed")

        pending = challenge_argument(child_root, ref(local), "The calculation needs a concrete correction",
                                     reviewer=unfinished)
        self.assertEqual(pending["status"], "pending")
        self.assertEqual(child.get("arguments", parent_argument["id"], parent_argument["revision"])
                         ["current_trust"]["state"], "suspended")
        properties = child.get("examples", example["id"])["current_trust"]["properties"]
        self.assertNotEqual(properties["p1"]["state"], "supported")
        self.assertEqual(self.store.get("examples", example["id"])
                         ["current_trust"]["properties"]["p1"]["state"], "supported")

    def test_reference_to_old_revision_can_precede_an_update_of_that_identity(self):
        claim = self.fixture.claim()
        result = self.store.archive_result([
            {"local_key": "old", "op": "reference", "ref": ref(claim)},
            {"local_key": "new", "op": "update", "kind": "claims", "record_id": claim["id"],
             "expected_revision": claim["revision"], "payload": {**claim["payload"], "title": "New display title"}},
            {"local_key": "argument", "op": "create", "kind": "arguments", "payload": {
                "status": "candidate", "proof": "Use the originally stated target",
                "conclusions": [{"target": {"local_key": "old"}, "relation": "supports"}]}}
        ], "reference-before-update")
        self.assertEqual(result["refs"]["old"], ref(claim))
        self.assertEqual(result["refs"]["new"]["revision"], 2)
        argument = self.store.get("arguments", result["refs"]["argument"]["id"])
        self.assertEqual(argument["payload"]["conclusions"][0]["target"], ref(claim))

    def test_mutual_claim_support_does_not_survive_withdrawal_of_its_independent_basis(self):
        first = self.fixture.claim("first")
        second = self.fixture.claim("second", "A consequence of the first statement")
        basis = self.fixture.certify(self.fixture.candidate(first))
        forward = self.fixture.certify(self.fixture.candidate(second, dependencies=[ref(first)]))
        backward = self.fixture.certify(self.fixture.candidate(first, dependencies=[ref(second)]))
        self.store.apply_confirmed_review(**confirmed_packet(self.root, [basis]))
        self.assertEqual(self.store.get("claims", first["id"])["current_trust"]["state"], "unresolved")
        self.assertEqual(self.store.get("claims", second["id"])["current_trust"]["state"], "unresolved")
        self.assertEqual(self.store.get("arguments", forward["id"])["current_trust"]["state"], "dependency_blocked")
        self.assertEqual(self.store.get("arguments", backward["id"])["current_trust"]["state"], "dependency_blocked")

    def scoped_child(self):
        example = self.fixture.example_with_independent_properties()
        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
            launch.return_value.pid = 12345
            task = Tasks(self.root).spawn_task(ref(example, property_ids=["p1"]), "Inspect just p1")
        child_root = Path(task["workspace"])
        return example, child_root, Store(child_root / "memory")

    def test_public_get_and_legacy_retrieve_respect_property_view_and_source_identity(self):
        example, _, child = self.scoped_child()
        returned = [child.get("examples", example["id"], example["revision"]),
                    child.retrieve(kinds=["examples"], record_id=example["id"],
                                   revision=example["revision"])["records"][0]]
        for record in returned:
            self.assertEqual(ref(record), ref(example))
            self.assertEqual(record["property_ids"], ["p1"])
            self.assertEqual([p["id"] for p in record["payload"]["properties"]], ["p1"])

    def test_default_context_example_audit_selects_only_granted_properties(self):
        example, child_root, _ = self.scoped_child()
        observed = []

        def reviewer(_prompt, directory):
            import json
            text = (directory / "input.json").read_text(encoding="utf-8")
            data = json.loads(text)
            self.assertEqual(data["property_ids"], ["p1"])
            self.assertNotIn("UNSELECTED_PROPERTY_MARKER", text)
            observed.append(True)
            return {"verdict": "pass", "summary": "The selected property holds", "findings": [],
                    "properties": [{"id": "p1", "verdict": "pass", "reason": "Exact substitution"}]}

        result = audit(child_root, "examples", example["id"], example["revision"], reviewer=reviewer)
        self.assertEqual(observed, [True])
        self.assertEqual(result["review"]["payload"]["verdict"], "pass")

    def test_batch_alias_cannot_expand_selected_properties(self):
        example = self.fixture.example_with_independent_properties()
        with self.assertRaisesRegex(ValueError, "alias property scope"):
            self.store.archive_result([
                {"local_key": "selected", "op": "reference", "ref": ref(example, property_ids=["p1"])},
                {"local_key": "broader", "op": "reference", "ref": {"local_key": "selected", "property_ids": ["p2"]}},
            ], "cannot-expand-alias")

    def test_duplicate_property_scope_in_audit_result_is_rejected_locally(self):
        from colombo.cell.verifier.review_validation import validate_conclusion_results
        example = self.fixture.example_with_independent_properties()
        expected = [{"target": ref(example, property_ids=["p1"]), "relation": "supports"}]
        repeated = [{"target": ref(example, property_ids=["p1", "p1"]), "relation": "supports",
                     "verdict": "pass", "reason": "The model duplicated a selected property"}]
        with self.assertRaisesRegex(ValueError, "Repeated property"):
            validate_conclusion_results(expected, repeated, "pass")


if __name__ == "__main__":
    unittest.main()
