"""ProofDraft -> exact Cell record navigation through contracts and real MCP."""
from __future__ import annotations
from brain_fixtures import write_review_package

import copy
import json
import unittest

from colombo.brain.submission_validation import ContractError
from colombo.brain.submission_validation import validate_semantics
from colombo.brain.proof_draft import render_proof, write_proof
from colombo.brain.mcp_server import AgentService
import test_mcp as mcp_helpers
import test_brain_service as service_helpers


def cell_record(kind, identifier, revision, payload, trust):
    return {"kind": kind, "id": identifier, "revision": revision, "payload": payload,
            "current_trust": {"state": trust, "blockers": []}}


def record_ref(record):
    return {key: record[key] for key in ("kind", "id", "revision")}


def create_fixture(test):
    service_helpers.create_fixture(test)
    test.unrelated_result = test.result
    test.claim = cell_record("claims", "claim-lemma", 1,
        {"statement": "An integer is even or odd.", "status": "proved"}, "proved")
    test.old_argument = cell_record("arguments", "argument-parity", 1,
        {"statement": "Two consecutive integers have an even product.",
         "body": "Earlier argument: take any integer n and consider the cases where n is even or odd." * 30,
         "conclusions": [{"target": record_ref(test.claim), "relation": "supports"}],
         "dependencies": [record_ref(test.claim)], "status": "proved"}, "supported")
    test.new_argument = cell_record("arguments", "argument-parity", 2,
        {**test.old_argument["payload"], "body": "A later revision with different content."}, "unreviewed")
    snapshot = {"schema_version": 2, "records": [test.claim, test.old_argument, test.new_argument]}
    path = test.store.root / "tasks/T0001/results/A0002/memory_snapshot.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    test.artifact = {"path": path.relative_to(test.store.root).as_posix(),
        "size": path.stat().st_size,
        "kind": "research_memory_snapshot"}
    test.result = test.store.write_record("result", {"accepted": True, "task_id": "T0001",
        "attempt_id": "A0002", "summary": "Snapshot navigation fixture", "artifacts": [test.artifact]})
    test.evidence = {"result_ref": test.result["id"], "path": test.artifact["path"],
        "locator": "Parity argument",
        "record_ref": record_ref(test.old_argument)}


def observation(test):
    value = service_helpers.observation(test)
    value["update"]["proof_draft"]["steps"][0]["evidence"] = [copy.deepcopy(test.evidence)]
    return value


class ArgumentNavigationTests(unittest.TestCase):
    setUp = create_fixture
    prepare_call = mcp_helpers.MCPServerTests.prepare_call
    service = service_helpers.BrainServiceTests.service

    def read(self, service, evidence=None, **kwargs):
        source = self.evidence if evidence is None else evidence
        return service.read_material(source["result_ref"], **{key: value for key, value in source.items()
            if key not in {"locator", "result_ref"}}, **kwargs)

    def check(self, value):
        return validate_semantics("integrate", value, self.store,
            {"result_refs": [self.result], "previous_proof_ref": self.seed, "task_snapshot": []})

    def test_proof_citation_reads_exact_historical_argument_page_by_page(self):
        proof_ref = write_proof(self.store, observation(self)["update"]["proof_draft"], "cited-proof", previous_ref=self.seed)
        service = self.service()
        saved = service.read_research(section="proof", id=proof_ref["id"])
        source = saved["payload"]["proof_draft"]["steps"][0]["evidence"][0]
        offset, pieces = 0, []
        while True:
            page = self.read(service, source, offset=offset, limit=137)
            self.assertEqual(page["record_ref"], record_ref(self.old_argument))
            self.assertEqual(page["offset"], offset)
            self.assertLessEqual(len(page["text"]), 137)
            pieces.append(page["text"])
            offset += len(page["text"])
            if not page["truncated"]:
                self.assertEqual(offset, page["total_chars"])
                break
            self.assertTrue(page["text"], "Pagination must make progress")
        actual = json.loads("".join(pieces))
        self.assertEqual(actual, self.old_argument)
        self.assertNotEqual(actual["payload"]["body"], self.new_argument["payload"]["body"])

    def test_dependency_and_current_trust_are_readable_without_promoting_trust(self):
        service = self.service()
        argument = json.loads(self.read(service)["text"])
        source = {**self.evidence, "record_ref": argument["payload"]["dependencies"][0]}
        claim = json.loads(self.read(service, source)["text"])
        self.assertEqual(claim, self.claim)
        source["record_ref"] = record_ref(self.new_argument)
        later = json.loads(self.read(service, source)["text"])
        self.assertEqual(later["current_trust"]["state"], "unreviewed")
        self.assertIsNone(self.store.get_meta("progress_ref"))

    def test_bad_citation_fields_and_missing_pins_fail_without_fallback(self):
        service = self.service()
        bad_sources = [
            {**self.evidence, "path": "input/goal.md"},
            {**self.evidence, "record_ref": {**self.evidence["record_ref"], "id": "missing"}},
            {**self.evidence, "record_ref": {**self.evidence["record_ref"], "revision": 3}},
        ]
        for source in bad_sources:
            with self.subTest(source=source), self.assertRaises(ValueError):
                self.read(service, source)
        with self.assertRaises(ValueError):
            service.read_material(self.result["id"], record_ref=record_ref(self.old_argument))

    def test_verifier_can_read_only_records_in_its_frozen_package(self):
        package = write_review_package(self.store, {
            "allowed_refs": [self.result["id"]], "required_checked_refs": [self.result["id"]]})
        self.prepare_call("verifier", "verify-progress", "verify-record", review_package_ref=package)
        service = AgentService(self.store.root, "verifier", "verify-progress", "verify-record")
        args = {key: value for key, value in self.evidence.items() if key not in {"locator", "result_ref"}}
        self.assertEqual(json.loads(service.read_material(self.result["id"], **args)["text"]), self.old_argument)
        with self.assertRaisesRegex(ValueError, "outside"):
            service.read_material(self.unrelated_result["id"], **args)


    def test_valid_record_citation_is_saved_and_rendered_without_promoting_progress(self):
        value = observation(self)
        self.assertEqual(self.check(value), value)
        rendered = render_proof(value["update"]["proof_draft"])
        self.assertIn(self.old_argument["id"], rendered)
        line = next(line for line in rendered.splitlines() if self.old_argument["id"] in line)
        self.assertIn(str(self.old_argument["revision"]), line)
        saved = self.service().submit("integrate", value)
        candidate = self.store.read_record(saved["ref"])
        self.assertEqual(candidate["update"]["proof_draft"]["steps"][0]["evidence"][0], self.evidence)
        self.assertEqual(self.store.get_meta("proof_ref"), self.seed)
        self.assertIsNone(self.store.get_meta("progress_ref"))

    def test_contract_rejects_unresolvable_or_incomplete_record_refs(self):
        for change in ({"id": "missing"}, {"revision": 3}, {"kind": "claims"}):
            value = observation(self)
            value["update"]["proof_draft"]["steps"][0]["evidence"][0]["record_ref"].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.check(value)
        value = observation(self)
        del value["update"]["proof_draft"]["steps"][0]["evidence"][0]["record_ref"]["revision"]
        with self.assertRaises(ContractError):
            self.check(value)

    def test_different_records_at_same_locator_remain_distinct(self):
        value = observation(self)
        source = {**self.evidence, "record_ref": record_ref(self.claim)}
        value["update"]["proof_draft"]["steps"][0]["evidence"].append(source)
        self.assertEqual(self.check(value), value)
        value["update"]["proof_draft"]["steps"][0]["evidence"].append(copy.deepcopy(source))
        self.assertEqual(self.check(value), value)

    def test_file_only_citation_remains_valid(self):
        value = observation(self)
        del value["update"]["proof_draft"]["steps"][0]["evidence"][0]["record_ref"]
        self.assertEqual(self.check(value), value)
        source = value["update"]["proof_draft"]["steps"][0]["evidence"][0]
        page = self.read(self.service(), source)
        self.assertEqual(len(json.loads(page["text"])["records"]), 3)


    def test_revised_argument_remains_unadopted_until_final_review(self):
        value = observation(self)
        previous = write_proof(self.store, value["update"]["proof_draft"], "checked-proof", previous_ref=self.seed)
        value["update"]["proof_draft"]["steps"][0]["evidence"][0]["record_ref"] = record_ref(self.new_argument)
        submitted = self.service().submit("integrate", value)
        self.assertEqual(self.store.read_record(previous)["proof_draft"]["steps"][0]["evidence"][0]["record_ref"], record_ref(self.old_argument))
        self.assertEqual(self.store.get_meta("proof_ref"), self.seed)
        self.assertIsNone(self.store.get_meta("final_review_ref"))
        self.assertTrue(submitted["ref"])


class ArgumentNavigationMCPTests(unittest.IsolatedAsyncioTestCase):
    setUp = create_fixture
    prepare_call = mcp_helpers.MCPServerTests.prepare_call
    connect = mcp_helpers.MCPServerTests.connect

    async def test_brain_mcp_follows_proof_record_reference_and_submits_candidate(self):
        value = observation(self)
        proof_ref = write_proof(self.store, value["update"]["proof_draft"], "mcp-cited-proof", previous_ref=self.seed)
        self.prepare_call("brain", "integrate", "mcp-argument", result_refs=[self.result],
                          previous_proof_ref=self.seed, task_snapshot=[])
        async with self.connect("brain", "integrate", "mcp-argument") as session:
            proof = await session.call_tool("read_research", {"ref": proof_ref["id"]})
            self.assertFalse(proof.isError, mcp_helpers.error_text(proof))
            source = mcp_helpers.response_object(proof)["payload"]["proof_draft"]["steps"][0]["evidence"][0]
            args = {key: item for key, item in source.items() if key != "locator"}
            response = await session.call_tool("read_material", {**{k:v for k,v in args.items() if k != "result_ref"}, "ref":args["result_ref"]})
            self.assertFalse(response.isError, mcp_helpers.error_text(response))
            self.assertEqual(json.loads(mcp_helpers.response_object(response)["text"]), self.old_argument)
            invalid = await session.call_tool("read_material", {**{k:v for k,v in args.items() if k != "result_ref"}, "ref":args["result_ref"], "record_ref": {**args["record_ref"], "revision": 999}})
            self.assertTrue(invalid.isError)
            submitted = await session.call_tool("record_results", {"payload": value})
            self.assertFalse(submitted.isError, mcp_helpers.error_text(submitted))
            self.assertEqual(self.store.record_kind(mcp_helpers.response_object(submitted)["ref"]), "assessment")
            self.assertIsNone(self.store.get_meta("progress_ref"))

    async def test_verifier_mcp_record_read_preserves_package_authorization(self):
        package = write_review_package(self.store, {
            "allowed_refs": [self.result["id"]], "required_checked_refs": [self.result["id"]]})
        self.prepare_call("verifier", "verify-progress", "mcp-verify-argument", review_package_ref=package)
        async with self.connect("verifier", "verify-progress", "mcp-verify-argument") as session:
            args = {key: item for key, item in self.evidence.items() if key not in {"locator", "result_ref"}}
            response = await session.call_tool("read_material", {"ref": self.result["id"], **args})
            self.assertFalse(response.isError, mcp_helpers.error_text(response))
            self.assertEqual(json.loads(mcp_helpers.response_object(response)["text"]), self.old_argument)
            denied = await session.call_tool("read_material", {"ref": self.unrelated_result["id"], **args})
            self.assertTrue(denied.isError)
            self.assertIn("outside", mcp_helpers.error_text(denied))


if __name__ == "__main__":
    unittest.main()
