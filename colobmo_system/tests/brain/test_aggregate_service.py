"""Unified research navigation and role-scoped MCP; no model calls."""
from brain_fixtures import write_review_package
import asyncio
import json
import unittest

from colombo.brain.mcp_server import AgentService, create_server
import test_mcp as helpers
import test_brain_service as fixtures
from controller_fixtures import event_task


class AggregateServiceTests(unittest.TestCase):
    setUp = fixtures.create_fixture
    prepare_call = helpers.MCPServerTests.prepare_call
    service = fixtures.BrainServiceTests.service

    def test_each_brain_stage_exposes_only_its_submission(self):
        common = {"read_research", "read_material", "audit", "save_note", "lookup", "scientific_memory", "job_status"}
        for stage, submit in (("plan", "submit_plan"), ("process_results", "record_results")):
            call = "inventory-" + stage
            self.prepare_call("brain", stage, call)
            server = create_server(self.store.root, "brain", stage, call)
            stage_tools = {"format_package_literal"} if stage == "plan" else set()
            self.assertEqual({tool.name for tool in asyncio.run(server.list_tools())}, common | {submit} | stage_tools)

    def test_retired_conclude_stage_is_not_a_model_interface(self):
        self.prepare_call("brain", "conclude", "retired-conclude")
        with self.assertRaisesRegex(ValueError, "role/stage"):
            create_server(self.store.root, "brain", "conclude", "retired-conclude")

    def test_advertised_payload_and_cell_reference_schemas_match_contracts(self):
        from colombo.brain.record_formats import REVIEW
        from colombo.brain.record_formats import PLAN, OBSERVATION
        from colombo.brain.cell_evidence import RECORD_REF_SCHEMA
        from jsonschema import Draft202012Validator
        from pydantic import TypeAdapter
        for role, stage, tool_name, contract in (("brain", "plan", "submit_plan", PLAN),
                ("brain", "process_results", "record_results", OBSERVATION),
                ("verifier", "verify-progress", "write_review", REVIEW)):
            call = "schema-" + stage
            kwargs = {}
            if role == "verifier":
                kwargs["review_package_ref"] = write_review_package(self.store, {
                    "allowed_refs": [self.seed["id"]], "required_checked_refs": [self.seed["id"]]})
            self.prepare_call(role, stage, call, **kwargs)
            server = create_server(self.store.root, role, stage, call)
            tools = {tool.name: tool for tool in asyncio.run(server.list_tools())}
            advertised = tools[tool_name].inputSchema["properties"]["payload"]
            self.assertEqual({k: v for k, v in advertised.items() if k != "title"}, contract)
            material = tools["read_material"].inputSchema
            ref_shapes = material["properties"]["record_ref"]["anyOf"]
            self.assertIn(RECORD_REF_SCHEMA, ref_shapes)
            validator = Draft202012Validator(material)
            good = {"ref": "result-id", "path": "snapshot.json", "record_ref": {
                "kind": "arguments", "id": "argument-id", "revision": 1}}
            validator.validate(good)
            for field, value in (("kind", "argument"), ("revision", True), ("revision", "1")):
                bad = json.loads(json.dumps(good))
                bad["record_ref"][field] = value
                self.assertFalse(validator.is_valid(bad))
            validator.validate({"ref": "result-id"})
            validator.validate({"ref": "result-id", "record_ref": None})

    def test_fixed_read_and_navigation_cannot_be_ambiguously_combined(self):
        service = self.service()
        read = service.read_research(ref=self.result["id"])
        self.assertEqual(read["ref"], self.result)
        self.assertEqual(set(read["ref"]), {"id", "revision"})
        for kwargs in ({"section":"tasks", "ref":self.result["id"]},
                       {"id":"T0001", "ref":self.result["id"]},
                       {"offset":True}, {"limit":False}, {"offset":-1}, {"limit":51}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                service.read_research(**kwargs)

    def test_note_history_is_navigable_and_pagination_preserves_fixed_refs(self):
        service = self.service()
        old = service.save_note("An open idea")
        service.save_note("A different idea")
        current = service.save_note("The original idea was resolved", status="resolved", supersedes=old["id"])
        page = service.read_research(section="notes", limit=1)
        seen = []
        while True:
            seen.extend(item["id"] for item in page["items"])
            if page["next"] is None:
                break
            page = service.read_research(**page["next"])
        self.assertEqual(len(seen), 2)
        self.assertEqual(len(set(seen)), 2)
        self.assertNotIn(old["id"], seen)
        self.assertIn(current["id"], seen)
        self.assertEqual(service.read_research(ref=old["id"])["payload"]["text"], "An open idea")

    def test_submission_receipt_reuses_one_candidate_without_proof_body_in_research(self):
        service = self.service()
        payload = fixtures.observation(self)
        submitted = service.submit("integrate", payload)
        self.assertEqual(service.submit("integrate", payload), submitted)
        receipt = json.loads((service.work / "submission.json").read_text(encoding="utf-8"))
        self.assertNotIn("payload", receipt)
        candidate = service.read_research(ref=submitted["ref"]["id"])["payload"]
        self.assertNotIn("proof_draft", candidate["update"])
        self.assertIn("proof_ref", candidate["update"])
        self.assertEqual(self.store.read_record(submitted["ref"]), payload)
        self.assertIsNone(self.store.get_meta("progress_ref"))

    def test_verifier_can_only_read_authorized_fixed_versions(self):
        package = write_review_package(self.store, {
            "allowed_refs":[self.seed["id"]], "required_checked_refs":[self.seed["id"]]})
        self.prepare_call("verifier", "verify-progress", "restricted", review_package_ref=package)
        service = AgentService(self.store.root, "verifier", "verify-progress", "restricted")
        server = create_server(self.store.root, "verifier", "verify-progress", "restricted")
        self.assertEqual({tool.name for tool in asyncio.run(server.list_tools())},
                         {"read_research", "read_material", "read_review_package", "write_review"})
        self.assertEqual(service.read_research(ref=self.seed["id"])["ref"], self.seed)
        for kwargs in ({}, {"section":"proof"}, {"section":"tasks", "id":"T0001"},
                       {"ref":self.result["id"]}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                service.read_research(**kwargs)

    def test_plan_is_immediately_readable_as_task_and_wave(self):
        self.store.set_meta(result_events=[])
        service = self.service(stage="plan", call_id="planned-navigation")
        submitted = service.submit("plan", {"rationale":"Two independent routes", "tasks":[
            event_task("First route", retain=True), event_task("Second route", retain=True)]})
        tasks = service.read_research(section="tasks", limit=1)
        self.assertEqual(tasks["total"], 2)
        self.assertEqual(len(tasks["items"]), 1)
        self.assertIsNotNone(tasks["next"])
        wave = service.read_research(section="waves", id="W0001")
        self.assertEqual(wave["wave"]["plan_ref"], submitted["ref"])
        self.assertEqual({m["task_id"] for m in wave["wave"]["members"]}, {"T0001", "T0002"})
        task = service.read_research(section="tasks", id="T0001")
        self.assertEqual(task["task"]["definition"]["title"], "First route")
        self.assertEqual(task["items"][0]["attempt_id"], "A0001")


if __name__ == "__main__":
    unittest.main()
