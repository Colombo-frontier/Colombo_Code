"""Research identities, atomic results, and route outcomes with synthetic evidence.

Reviewer callbacks exercise certification transport and state transitions; they
are not mathematical verdicts about the intentionally contradictory fixture.
No model process or external service is used.
"""
from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from colombo.cell.verifier.local_audit import audit
from colombo.cell.verifier.challenge import challenge_argument
from colombo.cell.verifier.challenge import resume_argument_challenge
from colombo.cell.record_store import AuditRequired
from colombo.cell.record_store import RevisionConflict
from colombo.cell.record_store import Store
from colombo.cell.record_store import StoreError
from colombo.cell.subcell_dispatch import Tasks
from colombo.shared.file_io import Path
from test_argument_challenges import first as challenge_report
from test_argument_challenges import confirmation as challenge_confirmation


ROOT = Path(__file__).resolve().parents[2]


def ref(record, **extra):
    return {**{key: record[key] for key in ("kind", "id", "revision")}, **extra}


class ResearchRecordTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for name in tuple(os.environ):
            if name.startswith("CELL_"):
                os.environ.pop(name)
        temporary = tempfile.TemporaryDirectory(prefix=".research-records-", dir=str(ROOT))
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "problem.md").write_text("Study elementary real-number statements.", encoding="utf-8")
        self.store = Store(self.root / "memory")

    def claim(self, identifier="C1", conclusion="x squared is nonnegative", **extra):
        return self.store.archive("claims", {"proposition": {
            "assumptions": "x is real", "quantifiers": "for every x", "conclusion": conclusion},
            **extra}, record_id=identifier)

    def candidate(self, target, relation="supports", **extra):
        return self.store.archive("arguments", {
            "status": "candidate", "proof": "A synthetic exact derivation for the requested target.",
            "conclusions": [{"target": ref(target), "relation": relation}], **extra})

    @staticmethod
    def response(argument, verdict="pass"):
        return {"verdict": verdict, "summary": "Checked the selected mathematical relation.",
                "findings": [] if verdict == "pass" else ["Source applicability remains unestablished."],
                "properties": [], "conclusions": [
                    {**copy.deepcopy(row), "verdict": verdict, "reason": "A fixed synthetic review outcome."}
                    for row in argument["payload"].get("conclusions", [])]}

    def certify(self, candidate):
        result = audit(self.root, "arguments", candidate["id"], candidate["revision"],
                       reviewer=lambda *_: self.response(candidate))
        self.assertEqual(result["review"]["payload"]["verdict"], "pass")
        self.assertEqual(result["record"]["current_trust"]["state"], "supported")
        return result["record"]

    def proof_state(self, target, closing=None, expected="supports", **extra):
        obligation = {"id": "O1", "target_claim_ref": ref(target), "expected_relation": expected,
                      "work_status": "active", "evidence_refs": [],
                      "closing_argument_ref": ref(closing) if closing else None, **extra}
        return self.store.archive("proof_state", {"routes": [{"route_id": "R1",
            "target_claim_ref": ref(target), "obligations": [obligation]}]})

    def json_files(self):
        return {path.name: path.read_bytes() for path in (self.root / "memory").glob("*.json")}

    def test_claim_mathematical_edits_need_new_identity_and_keep_old_statement(self):
        claim = self.claim()
        original = copy.deepcopy(claim["payload"])
        edits = [dict(original["proposition"], assumptions="x is strictly positive"),
                 dict(original["proposition"], quantifiers="there exists x"),
                 dict(original["proposition"], conclusion="x squared is strictly positive")]
        before = self.json_files()
        for proposition in edits:
            with self.subTest(proposition=proposition), self.assertRaisesRegex(StoreError, "new Claim ID"):
                self.store.archive("claims", {"proposition": proposition}, claim["id"], expected_revision=1)
        self.assertEqual(self.json_files(), before)
        replacement = self.claim("C2", "x squared is strictly positive", derived_from=[ref(claim)])
        self.assertNotEqual(replacement["id"], claim["id"])
        self.assertEqual(self.store.get("claims", "C1")["payload"], original)
        self.assertEqual(replacement["current_trust"]["state"], "unresolved")

    def test_title_revision_keeps_same_proposition_and_old_audited_support(self):
        claim = self.claim(title="Initial title")
        proved = self.certify(self.candidate(claim))
        revised = self.store.archive("claims", {**claim["payload"], "title": "A clearer title"},
                                     claim["id"], expected_revision=1)
        self.assertEqual(revised["revision"], 2)
        self.assertNotEqual(revised["revision"], claim["revision"])
        self.assertEqual(revised["current_trust"]["state"], "proved")
        support = revised["current_trust"]["supports"][0]
        self.assertEqual(support["argument_ref"], ref(proved))
        self.assertEqual(support["audited_target"], ref(claim))
        self.assertEqual(self.store.get("claims", claim["id"], 1)["current_trust"]["state"], "proved")
        other = self.claim("C2", "x squared is strictly positive", derived_from=[ref(revised)])
        self.assertEqual(other["current_trust"]["state"], "unresolved")

    def test_example_construction_and_properties_have_stable_identities(self):
        example = self.store.archive("examples", {"construction": "x=0 in the real numbers",
            "properties": [{"id": "p1", "statement": "x squared equals zero", "status": "pending"}]}, "E1")
        changed = copy.deepcopy(example["payload"])
        changed["construction"] = "x=1 in the real numbers"
        with self.assertRaisesRegex(StoreError, "new Example ID"):
            self.store.archive("examples", changed, "E1", expected_revision=1)
        changed = copy.deepcopy(example["payload"])
        changed["properties"][0]["statement"] = "x squared is positive"
        with self.assertRaisesRegex(StoreError, "new property ID"):
            self.store.archive("examples", changed, "E1", expected_revision=1)
        with self.assertRaisesRegex(StoreError, "Keep existing properties"):
            self.store.archive("examples", {**example["payload"], "properties": []}, "E1", expected_revision=1)
        expanded = copy.deepcopy(example["payload"])
        expanded["properties"].append({"id": "p2", "statement": "x is an integer", "status": "pending"})
        updated = self.store.archive("examples", expanded, "E1", expected_revision=1)
        self.assertEqual(updated["revision"], 2)
        self.assertEqual([item["id"] for item in updated["payload"]["properties"]], ["p1", "p2"])
        variant = self.store.archive("examples", {"construction": "x=1 in the real numbers",
            "variant_of": ref(updated), "properties": []}, "E2")
        self.assertNotEqual(variant["id"], example["id"])

    def test_example_metadata_update_preserves_audited_property(self):
        example = self.store.archive("examples", {"construction": "x=0", "title": "Old title",
            "properties": [{"id": "p1", "statement": "x squared equals zero", "status": "pending"}]})
        checked = audit(self.root, "examples", example["id"], 1, reviewer=lambda *_: {
            "verdict": "pass", "summary": "The exact calculation is zero.", "findings": [],
            "properties": [{"id": "p1", "verdict": "pass", "reason": "0 times 0 equals 0."}]})["record"]
        updated = self.store.archive("examples", {**checked["payload"], "title": "Zero example"},
                                     checked["id"], expected_revision=checked["revision"])
        self.assertEqual(updated["current_trust"]["properties"]["p1"]["state"], "supported")
        self.assertEqual(updated["payload"]["properties"][0]["audit_id"],
                         checked["payload"]["properties"][0]["audit_id"])

    def result_operations(self):
        return [
            {"local_key": "c", "op": "create", "kind": "claims", "record_id": "C1",
             "payload": {"proposition": "For every real x, x squared is nonnegative"}},
            {"local_key": "e", "op": "create", "kind": "examples", "record_id": "E1",
             "payload": {"construction": "x=0", "properties": [
                 {"id": "p1", "statement": "x squared is zero", "status": "pending"}]}},
            {"local_key": "g", "op": "create", "kind": "arguments", "record_id": "G1",
             "payload": {"status": "candidate", "proof": "A square is nonnegative in the real ordered field.",
                         "conclusions": [{"target": {"local_key": "c"}, "relation": "supports"}],
                         "subject_refs": [{"local_key": "e", "property_ids": ["p1"]}],
                         "dependencies": []}}]

    def test_batch_local_targets_subjects_and_reference_aliases_resolve_to_fixed_records(self):
        operations = self.result_operations()
        operations.insert(0, {"local_key": "alias", "op": "reference", "ref": {"local_key": "c"}})
        operations[-1]["payload"]["conclusions"][0]["target"] = {"local_key": "alias"}
        result = self.store.archive_result(operations, "related-result")
        self.assertEqual(result["refs"]["alias"], result["refs"]["c"])
        argument = self.store.get("arguments", "G1")
        self.assertEqual(argument["payload"]["conclusions"][0]["target"], result["refs"]["c"])
        self.assertEqual(argument["payload"]["subject_refs"],
                         [{**result["refs"]["e"], "property_ids": ["p1"]}])
        self.assertEqual(len(self.store.snapshot(["claims", "examples", "arguments"])), 3)
        self.assertEqual(len(self.store.snapshot(["events"])), 3)

    def test_batch_can_reference_existing_record_update_attempt_and_create_argument(self):
        claim = self.claim()
        attempt = self.store.archive("attempts", {"skill": "prove", "target_ref": ref(claim)})
        result = self.store.archive_result([
            {"local_key": "target", "op": "reference", "ref": ref(claim)},
            {"local_key": "work", "op": "update", "kind": "attempts", "record_id": attempt["id"],
             "expected_revision": 1, "payload": {"skill": "prove", "target_ref": {"local_key": "target"},
                 "produced_refs": [{"local_key": "g"}], "next_steps": "Audit the completed derivation"}},
            {"local_key": "g", "op": "create", "kind": "arguments", "payload": {
                "status": "candidate", "proof": "The real square is nonnegative.",
                "conclusions": [{"target": {"local_key": "target"}, "relation": "supports"}]}}
        ], "mixed-operations")
        self.assertEqual(result["refs"]["target"], ref(claim))
        self.assertEqual(result["refs"]["work"]["revision"], 2)
        latest = self.store.get("attempts", attempt["id"])
        self.assertEqual(latest["payload"]["produced_refs"], [result["refs"]["g"]])
        self.assertEqual(len(self.store.snapshot(["claims"])), 1)

    def test_invalid_batch_or_conflicting_update_writes_nothing(self):
        attempt = self.store.archive("attempts", {"skill": "prove", "summary": "Start"}, "A1")
        before = self.json_files()
        bad = self.result_operations()
        bad[-1]["payload"]["status"] = "proved"
        with self.assertRaises((StoreError, AuditRequired)):
            self.store.archive_result(bad, "bad-certification")
        self.assertEqual(self.json_files(), before)
        conflict = self.result_operations() + [{"local_key": "a", "op": "update", "kind": "attempts",
            "record_id": attempt["id"], "expected_revision": 2, "payload": {"summary": "Wrong base"}}]
        with self.assertRaises(RevisionConflict):
            self.store.archive_result(conflict, "bad-base")
        self.assertEqual(self.json_files(), before)
        self.assertFalse((self.root / "memory" / ".pending.json").exists())

    def test_batch_request_retries_preserve_identity_and_reject_changed_input(self):
        operations = self.result_operations()
        first = self.store.archive_result(operations, "stable-request")
        before = self.json_files()
        again = self.store.archive_result(copy.deepcopy(operations), "stable-request")
        self.assertEqual(first["refs"], again["refs"])
        self.assertEqual(self.json_files(), before)
        changed = copy.deepcopy(operations)
        changed[0]["payload"]["proposition"] = "A different statement"
        with self.assertRaisesRegex(StoreError, "different input"):
            self.store.archive_result(changed, "stable-request")
        self.assertEqual(self.json_files(), before)

    def test_batch_journal_recovers_all_collections_events_and_request_identity(self):
        operations = self.result_operations()
        write = self.store._atomic_write
        interrupted = False

        def fail_during_replacement(name, document):
            nonlocal interrupted
            if name == "arguments.json" and not interrupted:
                interrupted = True
                raise OSError("Synthetic crash between collection replacements")
            return write(name, document)

        with patch.object(self.store, "_atomic_write", side_effect=fail_during_replacement):
            with self.assertRaisesRegex(OSError, "Synthetic crash"):
                self.store.archive_result(operations, "interrupted-result")
        self.assertTrue((self.root / "memory" / ".pending.json").exists())
        restored = Store(self.root / "memory")
        snapshot = restored.snapshot(["claims", "examples", "arguments"])
        self.assertEqual({(item["kind"], item["id"], item["revision"]) for item in snapshot},
                         {("claims", "C1", 1), ("examples", "E1", 1), ("arguments", "G1", 1)})
        self.assertFalse((self.root / "memory" / ".pending.json").exists())
        events = restored.snapshot(["events"])
        self.assertEqual([item["payload"]["sequence"] for item in events], [1, 2, 3])
        replay = restored.archive_result(operations, "interrupted-result")
        self.assertEqual(replay["refs"]["g"], ref(restored.get("arguments", "G1")))
        self.assertEqual(len(restored.snapshot(["events"])), 3)

    def test_positive_and_negative_certificates_have_distinct_claim_results(self):
        true_claim = self.claim()
        false_claim = self.claim("C2", "x squared is strictly positive")
        self.assertEqual(true_claim["current_trust"]["state"], "unresolved")
        positive = self.certify(self.candidate(true_claim))
        negative = self.certify(self.candidate(false_claim, "refutes", proof="Set x=0."))
        positive_trust = self.store.get("claims", "C1")["current_trust"]
        negative_trust = self.store.get("claims", "C2")["current_trust"]
        self.assertEqual(positive_trust["state"], "proved")
        self.assertEqual(positive_trust["supports"][0]["argument_ref"], ref(positive))
        self.assertEqual(negative_trust["state"], "refuted")
        self.assertEqual(negative_trust["refutes"][0]["argument_ref"], ref(negative))
        self.assertFalse(negative_trust["supports"])

    def test_contradictory_certificates_block_consumption_and_route_completion(self):
        # Deliberately contradictory reviewer fixtures exercise conflict handling,
        # not the correctness of either mathematical assertion.
        claim = self.claim()
        positive = self.certify(self.candidate(claim))
        self.certify(self.candidate(claim, "refutes", proof="Synthetic contrary certification."))
        trust = self.store.get("claims", claim["id"])["current_trust"]
        self.assertEqual(trust["state"], "conflicted")
        self.assertEqual(len(trust["supports"]), 1)
        self.assertEqual(len(trust["refutes"]), 1)
        child_target = self.claim("C2", "0 is nonnegative")
        dependent = self.candidate(child_target, dependencies=[ref(claim)])
        self.assertEqual(dependent["current_trust"]["state"], "dependency_blocked")
        result = audit(self.root, "arguments", dependent["id"], dependent["revision"],
                       reviewer=lambda *_: self.response(dependent))
        self.assertNotEqual(result["review"]["payload"]["verdict"], "pass")
        self.assertEqual(self.store.get("arguments", dependent["id"])["payload"]["status"], "candidate")
        self.assertEqual(self.proof_state(claim, positive)["obligations"][0]["satisfaction"], "blocked")

    def test_refuted_required_lemma_blocks_support_route_but_satisfies_refutation_task(self):
        claim = self.claim(conclusion="x squared is strictly positive")
        negative = self.certify(self.candidate(claim, "refutes", proof="At x=0, x squared equals 0."))
        positive_route = self.proof_state(claim, negative, "supports")
        negative_route = self.proof_state(claim, negative, "refutes")
        self.assertEqual(positive_route["obligations"][0]["mathematical_state"], "refuted")
        self.assertEqual(positive_route["obligations"][0]["satisfaction"], "blocked")
        self.assertEqual(negative_route["obligations"][0]["satisfaction"], "satisfied")

    def test_obligation_needs_matching_effective_closing_argument_not_just_finished_work(self):
        claim = self.claim()
        positive = self.certify(self.candidate(claim))
        another = self.claim("C2", "0 is nonnegative")
        unrelated = self.certify(self.candidate(another))
        for closing in (None, unrelated):
            with self.subTest(closing=closing and closing["id"]):
                view = self.proof_state(claim, closing, work_status="completed")["obligations"][0]
                self.assertEqual(view["mathematical_state"], "proved")
                self.assertEqual(view["satisfaction"], "unresolved")
        self.assertEqual(self.proof_state(claim, positive)["obligations"][0]["satisfaction"], "satisfied")

    def test_citation_is_readable_evidence_but_not_a_locally_completed_obligation(self):
        source = self.store.archive("sources", {"title": "Synthetic reference", "locator": "Statement 1",
            "statement": "For positive real x, x squared is positive.", "reading_scope": "full statement"})
        theorem = self.claim(conclusion="x squared is strictly positive", citation={
            "source_refs": [ref(source)], "locator": "Statement 1"})
        self.assertEqual(theorem["current_trust"]["state"], "cited")
        self.assertTrue(theorem["current_trust"]["citation_requires_application_check"])
        self.assertEqual(self.proof_state(theorem)["obligations"][0]["satisfaction"], "unresolved")
        application_target = self.claim("C2", "0 squared is strictly positive")
        application = self.candidate(application_target, dependencies=[ref(theorem)])
        seen = []

        def reviewer(_prompt, directory):
            context = json.loads((directory / "input.json").read_text(encoding="utf-8"))
            cited = next(row for row in context["dependencies"] if row["id"] == theorem["id"])
            self.assertEqual(cited["current_trust"]["state"], "cited")
            source_record = next(row for row in context["reference_materials"] if row["id"] == source["id"])
            self.assertEqual(source_record["payload"]["statement"], source["payload"]["statement"])
            seen.append(source_record["id"])
            return self.response(application, "uncertain")

        result = audit(self.root, "arguments", application["id"], 1, reviewer=reviewer)
        self.assertEqual(seen, [source["id"]])
        self.assertEqual(result["review"]["payload"]["verdict"], "uncertain")
        self.assertEqual(self.store.get("claims", "C2")["current_trust"]["state"], "unresolved")

    def test_target_cannot_be_its_own_premise_even_through_kind_alias(self):
        claim = self.claim()
        for spelling in ("claims", "claim"):
            with self.subTest(kind=spelling), self.assertRaisesRegex(StoreError, "own premise"):
                self.candidate(claim, dependencies=[{**ref(claim), "kind": spelling}])

    def test_same_property_cannot_be_both_conclusion_and_premise(self):
        example = self.store.archive("examples", {"construction": "x=0", "properties": [
            {"id": "p1", "statement": "x squared is zero", "status": "pending"}]})
        selected = ref(example, property_ids=["p1"])
        with self.assertRaisesRegex(StoreError, "own premise"):
            self.store.archive("arguments", {"status": "candidate", "proof": "Assume the required property.",
                "conclusions": [{"target": selected, "relation": "supports"}], "dependencies": [selected]})

    def example_with_independent_properties(self):
        return self.store.archive("examples", {"construction": "The real number x=0", "properties": [
            {"id": "p1", "statement": "x squared equals zero", "status": "pending"},
            {"id": "p2", "statement": "x squared is nonnegative", "status": "pending"},
            {"id": "p3", "statement": "UNSELECTED_PROPERTY_MARKER: a separate unexamined property", "status": "pending"}]})

    def property_argument(self, example, identifier, *, dependencies=None):
        return self.store.archive("arguments", {"status": "candidate",
            "proof": "Use the exact value zero and the order relation.",
            "conclusions": [{"target": ref(example, property_ids=[identifier]), "relation": "supports"}],
            "dependencies": dependencies or []})

    def test_argument_can_support_selected_property_without_mutating_example_certificate(self):
        example = self.example_with_independent_properties()
        before = (self.root / "memory/examples.json").read_bytes()
        argument = self.property_argument(example, "p1")
        proved = self.certify(argument)
        current = self.store.get("examples", example["id"])
        self.assertEqual((self.root / "memory/examples.json").read_bytes(), before)
        self.assertEqual(current["revision"], 1)
        self.assertEqual(current["payload"], example["payload"])
        self.assertEqual(current["payload"]["properties"][0]["status"], "pending")
        self.assertNotIn("audit_id", current["payload"]["properties"][0])
        properties = current["current_trust"]["properties"]
        self.assertEqual(properties["p1"]["state"], "supported")
        self.assertEqual(properties["p1"]["supports"][0]["argument_ref"], ref(proved))
        self.assertEqual(properties["p1"]["supports"][0]["audited_target"], ref(example, property_ids=["p1"]))
        self.assertEqual(properties["p2"]["state"], "unreviewed")
        self.assertEqual(properties["p3"]["state"], "unreviewed")

    def test_other_property_can_use_supported_property_of_same_example_without_false_cycle(self):
        example = self.example_with_independent_properties()
        first = self.certify(self.property_argument(example, "p1"))
        second = self.property_argument(example, "p2", dependencies=[ref(example, property_ids=["p1"])])
        self.assertEqual(second["current_trust"]["state"], "unreviewed")
        proved = self.certify(second)
        self.assertEqual(self.store.get("arguments", first["id"])["current_trust"]["state"], "supported")
        self.assertEqual(self.store.get("arguments", proved["id"])["current_trust"]["state"], "supported")
        properties = self.store.get("examples", example["id"])["current_trust"]["properties"]
        self.assertEqual(properties["p1"]["state"], "supported")
        self.assertEqual(properties["p2"]["state"], "supported")
        self.assertEqual(properties["p3"]["state"], "unreviewed")
        self.assertFalse(properties["p2"]["blockers"])

    def test_audit_keeps_target_property_separate_from_another_selected_premise_property(self):
        example = self.example_with_independent_properties()
        self.certify(self.property_argument(example, "p1"))
        argument = self.property_argument(example, "p2", dependencies=[ref(example, property_ids=["p1"])])
        observed = []

        def reviewer(_prompt, directory):
            raw = (directory / "input.json").read_text(encoding="utf-8")
            context = json.loads(raw)
            targets = context["conclusion_targets"]
            self.assertEqual(len(targets), 1)
            self.assertEqual(targets[0]["property_ids"], ["p2"])
            self.assertEqual([item["id"] for item in targets[0]["payload"]["properties"]], ["p2"])
            premises = context["dependencies"]
            self.assertEqual(len(premises), 1)
            self.assertEqual(premises[0]["property_ids"], ["p1"])
            self.assertEqual([item["id"] for item in premises[0]["payload"]["properties"]], ["p1"])
            self.assertNotIn("UNSELECTED_PROPERTY_MARKER", raw)
            observed.append(True)
            return self.response(argument)

        result = audit(self.root, "arguments", argument["id"], 1, reviewer=reviewer)
        self.assertEqual(observed, [True])
        self.assertEqual(result["review"]["payload"]["verdict"], "pass")

    def test_child_claim_loses_inherited_support_when_granted_argument_is_locally_suspended_or_withdrawn(self):
        claim = self.claim()
        parent_argument = self.certify(self.candidate(claim,
            proof="Divide by x and omit the permitted zero case; synthetic certificate fixture."))
        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
            launch.return_value.pid = 12345
            task = Tasks(self.root).spawn_task(ref(claim), "Check a consequence of this local claim",
                                              context_refs=[ref(parent_argument)])
        child_root = Path(task["workspace"])
        child = Store(child_root / "memory")
        self.assertEqual(child.get("claims", claim["id"])["current_trust"]["state"], "proved")
        payload = {key: value for key, value in parent_argument["payload"].items() if key != "audit_id"}
        local_copy = child.archive("arguments", {**payload, "status": "candidate"}, "local-copy")
        reviewed = audit(child_root, "arguments", local_copy["id"], 1,
                         reviewer=lambda *_: self.response(local_copy))["record"]
        self.assertEqual(reviewed["current_trust"]["state"], "supported")
        parent_bytes = (self.root / "memory/arguments.json").read_bytes()

        def timeout(*_):
            raise TimeoutError("Synthetic independent review needs continuation")

        pending = challenge_argument(child_root, ref(reviewed), "Division excludes the allowed x=0 case.",
                                     reviewer=timeout)
        self.assertEqual(pending["status"], "pending")
        self.assertEqual(child.get("arguments", parent_argument["id"], parent_argument["revision"])
                         ["current_trust"]["state"], "suspended")
        self.assertNotEqual(child.get("claims", claim["id"])["current_trust"]["state"], "proved")
        resolved = resume_argument_challenge(child_root, pending["challenge_id"],
            reviewer=lambda _prompt, directory: challenge_report(directory),
            checker=lambda _prompt, directory: challenge_confirmation(directory))
        self.assertEqual(resolved["status"], "withdrawn")
        self.assertEqual(child.get("arguments", parent_argument["id"], parent_argument["revision"])
                         ["current_trust"]["state"], "withdrawn")
        self.assertNotEqual(child.get("claims", claim["id"])["current_trust"]["state"], "proved")
        self.assertEqual(self.store.get("claims", claim["id"])["current_trust"]["state"], "proved")
        self.assertEqual((self.root / "memory/arguments.json").read_bytes(), parent_bytes)


if __name__ == "__main__":
    unittest.main()
