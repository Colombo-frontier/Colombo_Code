"""A small audit certifies exact targets and directions, not nearby statements."""
from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from colombo.cell.verifier.local_audit import audit
from colombo.cell.verifier.local_audit import _premises
from colombo.cell.verifier.review_validation import validate_conclusion_results
from colombo.cell.record_store import Store
from colombo.shared.file_io import Path


ROOT = Path(__file__).resolve().parents[2]


def ref(record, **extra):
    return {**{key: record[key] for key in ("kind", "id", "revision")}, **extra}


def response(argument, verdict="pass", **extra):
    return {"verdict": verdict, "summary": "Checked each exact statement and its assumptions.",
            "findings": [] if verdict == "pass" else ["The stated inference is incomplete."],
            "properties": [],
            "conclusions": [{**copy.deepcopy(item), "verdict": verdict,
                             "reason": "The supplied derivation covers this target and direction."}
                            for item in argument["payload"].get("conclusions", [])], **extra}


class ConclusionAuditTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        temporary = tempfile.TemporaryDirectory(prefix=".conclusion-audit-", dir=str(ROOT))
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "problem.md").write_text("Study elementary real identities.", encoding="utf-8")
        self.store = Store(self.root / "memory")
        self.claim = self.store.archive("claims", {"proposition": {
            "assumptions": "x is real", "quantifiers": "for every x",
            "conclusion": "x squared is nonnegative"}})

    def candidate(self, *, relation="supports", target=None, **extra):
        return self.store.archive("arguments", {
            "status": "candidate", "proof": "The square of a real number is nonnegative.",
            "conclusions": [{"target": target or ref(self.claim), "relation": relation}], **extra})

    def run_audit(self, argument, result):
        return audit(self.root, "arguments", argument["id"], argument["revision"],
                     reviewer=lambda *_: copy.deepcopy(result))

    def assert_response_error(self, argument, result):
        audited = self.run_audit(argument, result)
        self.assertEqual(audited["review"]["payload"]["verdict"], "service_error")
        self.assertEqual(audited["review"]["payload"]["error_stage"], "validate_response")
        self.assertEqual(self.store.get("arguments", argument["id"])["revision"], argument["revision"])
        self.assertEqual(self.store.get("arguments", argument["id"])["payload"]["status"], "candidate")

    def test_pass_binds_audited_target_direction_and_version(self):
        argument = self.candidate()
        audited = self.run_audit(argument, response(argument))
        self.assertEqual(audited["record"]["payload"]["status"], "proved")
        checked = audited["review"]["payload"]["conclusions"]
        self.assertEqual(checked[0]["target"], ref(self.claim))
        self.assertEqual(checked[0]["relation"], "supports")
        self.assertEqual(checked[0]["verdict"], "pass")
        self.assertEqual(audited["review"]["payload"]["target"], ref(argument))

    def test_refutation_is_explicitly_bound_to_the_negative_direction(self):
        false_claim = self.store.archive("claims", {"proposition": {
            "assumptions": "x is real", "quantifiers": "for every x", "conclusion": "x squared is positive"}})
        argument = self.candidate(target=ref(false_claim), relation="refutes",
                                  proof="At x=0 the hypothesis holds and the claimed strict inequality fails.")
        audited = self.run_audit(argument, response(argument))
        self.assertEqual(audited["review"]["payload"]["conclusions"][0]["relation"], "refutes")
        self.assertEqual(audited["record"]["payload"]["status"], "proved")

    def test_missing_repeated_or_invented_conclusion_does_not_certify(self):
        for mutation in ("missing_field", "empty", "duplicate", "extra", "unknown_field", "direction", "revision"):
            with self.subTest(mutation=mutation):
                argument = self.candidate()
                result = response(argument)
                if mutation == "missing_field":
                    result.pop("conclusions")
                elif mutation == "empty":
                    result["conclusions"] = []
                elif mutation == "duplicate":
                    result["conclusions"] *= 2
                elif mutation == "extra":
                    extra = copy.deepcopy(result["conclusions"][0])
                    extra["target"]["id"] = "unrequested-claim"
                    result["conclusions"].append(extra)
                elif mutation == "unknown_field":
                    result["conclusions"][0]["target"]["unexpected"] = "extra"
                elif mutation == "direction":
                    result["conclusions"][0]["relation"] = "refutes"
                else:
                    result["conclusions"][0]["target"]["revision"] += 1
                self.assert_response_error(argument, result)

    def test_each_conclusion_checked_and_overall_verdict_matches(self):
        second = self.store.archive("claims", {"proposition": {"conclusion": "0 squared equals zero"}})
        argument = self.candidate(conclusions=[
            {"target": ref(self.claim), "relation": "supports"},
            {"target": ref(second), "relation": "supports"}])
        result = response(argument)
        result["conclusions"][1].update(verdict="uncertain", reason="No justification for the second step.")
        self.assert_response_error(argument, result)
        result.update(verdict="uncertain", findings=["Second conclusion remains unverified."])
        audited = self.run_audit(argument, result)
        self.assertEqual(audited["record"]["payload"]["status"], "candidate")
        self.assertEqual([row["verdict"] for row in audited["review"]["payload"]["conclusions"]],
                         ["pass", "uncertain"])

    def test_target_and_construction_are_not_supplied_as_premises(self):
        source = self.store.archive("sources", {"title": "Ordered field axioms",
                                                "statement": "A product of two nonnegative reals is nonnegative."})
        example = self.store.archive("examples", {"construction": "x=0", "properties": [
            {"id": "zero", "statement": "x squared equals zero", "status": "pending"}]})
        argument = self.candidate(dependencies=[ref(source)], subject_refs=[ref(example, property_ids=["zero"])])

        def reviewer(prompt, work):
            context = json.loads((work / "input.json").read_text(encoding="utf-8"))
            self.assertEqual([row["id"] for row in context["conclusion_targets"]], [self.claim["id"]])
            self.assertEqual([row["id"] for row in context["subjects"]], [example["id"]])
            self.assertEqual([row["id"] for row in context["dependencies"]], [source["id"]])
            return response(argument)

        audited = audit(self.root, "arguments", argument["id"], 1, reviewer=reviewer)
        self.assertEqual(audited["review"]["payload"]["verdict"], "pass")

    def test_cited_theorem_source_is_available_without_becoming_a_new_premise(self):
        source = self.store.archive("sources", {"title": "Ordered field reference",
                                                "locator": "Section 1, axiom 3",
                                                "statement": "The product of nonnegative elements is nonnegative."})
        cited = self.store.archive("claims", {"proposition": {
            "assumptions": "a and b are nonnegative reals", "conclusion": "a*b >= 0"},
            "citation": {"source_refs": [ref(source)], "locator": "Section 1, axiom 3"}})
        argument = self.candidate(dependencies=[ref(cited)])

        def reviewer(prompt, work):
            context = json.loads((work / "input.json").read_text(encoding="utf-8"))
            self.assertEqual([row["id"] for row in context["dependencies"]], [cited["id"]])
            self.assertEqual([row["id"] for row in context["reference_materials"]], [source["id"]])
            self.assertEqual(context["dependencies"][0]["payload"]["citation"]["locator"], "Section 1, axiom 3")
            return response(argument)

        audited = audit(self.root, "arguments", argument["id"], 1, reviewer=reviewer)
        self.assertEqual(audited["review"]["payload"]["verdict"], "pass")

    def test_concurrent_support_loss_downgrades_each_conclusion_without_new_objection(self):
        argument = self.candidate()
        original_context = Store.audit_context
        count = 0

        def changed_context(store, *args, **kwargs):
            nonlocal count
            result = original_context(store, *args, **kwargs)
            count += 1
            if count > 1:
                result["record"]["current_trust"]["state"] = "dependency_blocked"
            return result

        with patch.object(Store, "audit_context", new=changed_context), \
                patch("colombo.cell.verifier.challenge.challenge_from_audit") as challenge:
            audited = self.run_audit(argument, response(argument))
        challenge.assert_not_called()
        review = audited["review"]["payload"]
        self.assertEqual(review["verdict"], "uncertain")
        self.assertEqual(review["conclusions"][0]["verdict"], "uncertain")
        self.assertEqual(audited["record"]["payload"]["status"], "candidate")

    def test_registration_advice_is_separate_from_mathematical_correctness(self):
        argument = self.candidate()
        suggestion = {"source_ref": ref(argument), "location": "proof: final example",
                      "suggested_kind": "examples", "content": "The explicit construction x=0.",
                      "reason": "This construction can be reused independently."}
        audited = self.run_audit(argument, response(argument, registration_findings=[suggestion]))
        review = audited["review"]["payload"]
        self.assertEqual(review["verdict"], "pass")
        self.assertEqual(review["registration_status"], "findings")
        self.assertEqual(review["registration_findings"], [suggestion])
        self.assertEqual(self.store.retrieve(kinds=["examples"])["count"], 0)

    def test_registration_missing_empty_or_invalid_are_distinct(self):
        for extra, status in (({}, "not_checked"), ({"registration_findings": []}, "checked"),
                              ({"registration_findings": ["unstructured advice"]}, "failed")):
            with self.subTest(status=status):
                argument = self.candidate()
                audited = self.run_audit(argument, response(argument, **extra))
                review = audited["review"]["payload"]
                self.assertEqual(review["verdict"], "pass")
                self.assertEqual(review["registration_status"], status)
                self.assertEqual(audited["record"]["payload"]["status"], "proved")

    def test_unavailable_registration_source_does_not_gain_authority(self):
        argument = self.candidate()
        unknown = {**ref(argument), "id": "not-in-input"}
        suggestion = {"source_ref": unknown, "location": "proof", "suggested_kind": "claims",
                      "content": "A proposed theorem.", "reason": "Extract it."}
        audited = self.run_audit(argument, response(argument, registration_findings=[suggestion]))
        self.assertEqual(audited["review"]["payload"]["verdict"], "pass")
        self.assertEqual(audited["review"]["payload"]["registration_status"], "failed")
        self.assertNotIn("registration_findings", audited["review"]["payload"])

    def test_legacy_argument_stays_compatible_without_new_conclusion_authority(self):
        legacy = self.store.archive("arguments", {"proof": "x=x by reflexivity.", "status": "candidate"})
        result = {"verdict": "pass", "summary": "Reflexivity suffices.", "findings": [], "properties": []}
        audited = self.run_audit(legacy, result)
        self.assertEqual(audited["record"]["payload"]["status"], "proved")
        self.assertNotIn("conclusions", audited["review"]["payload"])
        bad = self.store.archive("arguments", {"proof": "x=x by reflexivity.", "status": "candidate"})
        extra = response(self.candidate())["conclusions"]
        self.assert_response_error(bad, {**result, "conclusions": extra})


class ConclusionContractTests(unittest.TestCase):
    def test_result_order_and_property_selection_order_do_not_change_binding(self):
        targets = [{"target": {"kind": "examples", "id": "E1", "revision": 1, "property_ids": ["p2", "p1"]},
                    "relation": "supports"},
                   {"target": {"kind": "claims", "id": "C1", "revision": 2}, "relation": "refutes"}]
        results = [{**copy.deepcopy(item), "verdict": "pass", "reason": "Exact scope checked."}
                   for item in reversed(targets)]
        results[1]["target"]["property_ids"].reverse()
        validate_conclusion_results(targets, results, "pass")

    def test_service_error_cannot_carry_a_passing_conclusion(self):
        result = {"target": {"kind": "claims", "id": "C1", "revision": 1},
                  "relation": "supports", "verdict": "pass", "reason": "Checked."}
        with self.assertRaisesRegex(ValueError, "cannot certify"):
            validate_conclusion_results([], [result], "service_error")

    def test_premise_walk_does_not_follow_target_associations_and_scopes_properties(self):
        source = {"kind": "sources", "id": "S1", "revision": 1,
                  "payload": {"text": "A supplied premise."}}
        hidden = {**source, "id": "S2"}
        target = {"kind": "claims", "id": "C1", "revision": 1,
                  "payload": {"proposition": "A statement to establish."}}
        example = {"kind": "examples", "id": "E1", "revision": 1,
                   "payload": {"properties": [
                       {"id": "p1", "dependencies": [ref(source)]},
                       {"id": "p2", "dependencies": [ref(hidden)]}],
                       "target_ref": ref(target)}}
        argument = {"kind": "arguments", "payload": {
            "dependencies": [ref(example, property_ids=["p1"])],
            "conclusions": [{"target": ref(target), "relation": "supports"}]}}
        premises = _premises(argument, [], [source, hidden, target, example])
        self.assertEqual([item["id"] for item in premises], ["E1", "S1"])
        self.assertEqual([prop["id"] for prop in premises[0]["payload"]["properties"]], ["p1"])


if __name__ == "__main__":
    unittest.main()
