"""Real Store/service/recovery paths with synthetic Cell and verifier outputs."""
from __future__ import annotations
from brain_fixtures import write_review_package

import copy
import json
import unittest

from colombo.brain.model_calls import CodexBackend
from colombo.brain.submission_validation import ContractError
from colombo.brain.mcp_server import AgentService
from colombo.brain.research_store import Store, StoreError
from controller_fixtures import OracleTestFixture
from test_oracle_workflow import Backend
import test_mcp as mcp
import test_brain_service as fixtures


class ProofSourceSubmissionTests(unittest.TestCase):
    setUp = fixtures.create_fixture
    prepare_call = mcp.MCPServerTests.prepare_call
    service = fixtures.BrainServiceTests.service

    def payload(self):
        payload = fixtures.observation(self)
        proof = payload["update"]["proof_draft"]
        proof.pop("body")
        proof["body_source"] = {"result_ref": self.result["id"], "path": self.artifact["path"]}
        return payload

    def test_service_submission_replay_keeps_one_fixed_body_and_original_input(self):
        service = self.service()
        payload = self.payload()
        original = copy.deepcopy(payload)
        submitted = service.submit("integrate", payload)
        after = self.store.snapshot()
        self.assertEqual(service.submit("integrate", payload), submitted)
        self.assertEqual(after, self.store.snapshot())
        self.assertEqual(payload, original)
        self.assertEqual(self.store.submission_input(submitted["ref"]), payload)
        candidate = self.store.public_read(submitted["ref"])
        self.assertNotIn("proof_draft", candidate["update"])
        proof_ref = candidate["update"]["proof_ref"]
        proof = self.store.read_record(proof_ref)["proof_draft"]
        expected = (self.store.root / self.artifact["path"]).read_bytes().decode("utf-8")
        self.assertEqual(proof["body"], expected)
        self.assertEqual(proof["body_source"], payload["update"]["proof_draft"]["body_source"])
        research_text = json.dumps(self.store.read_document("research"), ensure_ascii=False)
        self.assertNotIn(json.dumps(expected, ensure_ascii=False), research_text)
        proofs = self.store.read_document("proof_draft")["versions"]
        self.assertEqual(sum(p["proof_draft"].get("body") == expected for p in proofs.values()), 1)
        self.assertEqual(self.store.reference_count("assessment"), 1)
        self.assertEqual(self.store.reference_count("proof_draft"), 2)  # seed and candidate

    def test_different_source_with_identical_text_cannot_replay_same_request(self):
        alternative = "tasks/T0001/results/A0002/proof-copy.md"
        data = self.store.safe_path(self.artifact["path"]).read_bytes()
        self.store.safe_path(alternative).parent.mkdir(parents=True)
        self.store.safe_path(alternative).write_bytes(data)
        self.result = self.store.write_record("result", {
            **self.store.read_record(self.result), "attempt_id": "A0002",
            "artifacts": [self.artifact, {"path": alternative, "size": len(data)}]})
        service = self.service()
        payload = self.payload()
        submitted = service.submit("integrate", payload)
        before = self.store.snapshot()
        changed = copy.deepcopy(payload)
        changed["update"]["proof_draft"]["body_source"]["path"] = alternative
        with self.assertRaisesRegex(StoreError, "different content"):
            service.submit("integrate", changed)
        self.assertEqual(before, self.store.snapshot())
        self.assertEqual(self.store.submission_input(submitted["ref"]), payload)

    def test_unreviewed_source_is_rejected_before_any_candidate_write(self):
        service = self.service()
        rejected = self.payload()
        self.store.set_meta(result_reviews={})
        before = self.store.snapshot()
        with self.assertRaisesRegex(ContractError, "Verifier"):
            service.submit("integrate", rejected)
        self.assertEqual(before, self.store.snapshot())

    def test_backend_receipt_and_missing_receipt_recovery_return_exact_input_form(self):
        service = self.service()
        payload = self.payload()
        service.submit("integrate", payload)
        path = service.work / "submission.json"
        manifest = json.loads((service.work / "call.json").read_text(encoding="utf-8"))
        self.assertEqual(CodexBackend._submission(path, manifest), payload)
        before = self.store.snapshot()
        path.unlink()
        restored = CodexBackend._committed_submission(path, manifest)
        self.assertEqual(restored, payload)
        self.assertNotIn("body", restored["update"]["proof_draft"])
        self.assertTrue(path.exists())
        self.assertEqual(before, self.store.snapshot())

    def test_failed_source_read_leaves_no_partial_candidate_or_receipt(self):
        service = self.service()
        self.store.safe_path(self.artifact["path"]).unlink()
        before = self.store.snapshot()
        with self.assertRaises(ContractError):
            service.submit("integrate", self.payload())
        self.assertEqual(before, self.store.snapshot())
        self.assertFalse((service.work / "submission.json").exists())


class ProofSourceMCPDiscoveryTests(unittest.IsolatedAsyncioTestCase):
    setUp = fixtures.create_fixture
    prepare_call = mcp.MCPServerTests.prepare_call
    connect = mcp.MCPServerTests.connect
    payload = ProofSourceSubmissionTests.payload

    async def test_real_tools_list_exposes_both_update_shapes_and_exclusive_source(self):
        from jsonschema import Draft202012Validator

        common = {"read_research", "read_material", "audit", "save_note", "lookup", "scientific_memory", "job_status"}
        for stage, submit in (("plan", "submit_plan"), ("integrate", "record_results")):
            call_id = "source-schema-" + stage
            self.prepare_call("brain", stage, call_id, result_refs=[self.result],
                              previous_proof_ref=self.seed, task_snapshot=[])
            async with self.connect("brain", stage, call_id) as session:
                inventory = {tool.name: tool for tool in (await session.list_tools()).tools}
                stage_tools = {"format_package_literal"} if stage == "plan" else set()
                self.assertEqual(set(inventory), common | {submit} | stage_tools)
                if stage != "integrate":
                    continue
                schema = inventory[submit].inputSchema
                full = schema["properties"]["payload"]["properties"]["update"]
                self.assertEqual(set(full["properties"]), {"admissions", "progress", "proof_draft", "rechecked_step_ids"})
                proof_schema = full["properties"]["proof_draft"]
                source = proof_schema["properties"]["body_source"]
                self.assertEqual(set(source["properties"]), {"result_ref", "path"})
                self.assertEqual(set(source["required"]), {"result_ref", "path"})
                self.assertFalse(source["additionalProperties"])
                self.assertTrue(all(value["type"] == "string" for value in source["properties"].values()))
                validator = Draft202012Validator(schema)
                wave = self.payload()
                validator.validate({"payload": wave})
                validator.validate({"payload": fixtures.observation(self)})
                result = {**wave, "update": {"admissions": wave["update"]["admissions"]},
                          "next_action": "continue"}
                self.assertFalse(validator.is_valid({"payload": result}))
                ambiguous = copy.deepcopy(wave)
                ambiguous["update"]["proof_draft"]["body"] = "Same proof in a second input form"
                self.assertFalse(validator.is_valid({"payload": ambiguous}))
                no_body = copy.deepcopy(wave)
                no_body["update"]["proof_draft"].pop("body_source")
                self.assertFalse(validator.is_valid({"payload": no_body}))
                for field in ("result_ref", "path"):
                    incomplete = copy.deepcopy(wave)
                    incomplete["update"]["proof_draft"]["body_source"].pop(field)
                    self.assertFalse(validator.is_valid({"payload": incomplete}))

        package = write_review_package(self.store, {
            "allowed_refs": [self.seed["id"]], "required_checked_refs": [self.seed["id"]]})
        self.prepare_call("verifier", "verify-progress", "source-schema-verifier", review_package_ref=package)
        async with self.connect("verifier", "verify-progress", "source-schema-verifier") as session:
            self.assertEqual({tool.name for tool in (await session.list_tools()).tools}, {
                "read_review_package", "read_research", "read_material", "write_review"})


class SourceScript(Backend):
    def __init__(self, adapter):
        super().__init__()
        self.source = None
        self.checked_proof = None
        self.package = None

    def invoke(self, role, stage, root, call_id, prompt, context):
        result = super().invoke(role, stage, root, call_id, prompt, context)
        if stage == "plan":
            result["tasks"] = result["tasks"][:1]
        elif stage == "integrate" and "proof_draft" in result["update"]:
            proof = result["update"]["proof_draft"]
            self.source = {key: proof["steps"][0]["evidence"][0][key] for key in ("result_ref", "path")}
            proof.pop("body")
            proof["body_source"] = self.source
        elif stage == "verify-progress":
            store = Store(root)
            self.package = store.read_record(context["review_package_ref"])
            if self.package.get("proof_ref"):
                self.checked_proof = store.read_record(self.package["proof_ref"])["proof_draft"]
        return result


class ProofSourceControllerTests(OracleTestFixture, unittest.TestCase):

    def test_full_source_proof_reviewed_adopted_and_resume_does_not_launch(self):
        script = SourceScript(self.adapter)
        self.assertEqual(self.controller(script).run()["status"], "completed")
        self.assertIsNotNone(script.source)
        expected = self.store.read_artifact(script.source["result_ref"], script.source["path"])["text"]
        self.assertEqual(script.checked_proof["body"], expected)
        self.assertEqual(script.checked_proof["body_source"], script.source)
        proof_ref = self.store.get_meta("proof_ref")
        self.assertIn(proof_ref["id"], script.package["required_checked_refs"])
        self.assertEqual(self.store.read_record(proof_ref)["proof_draft"]["body"], expected)
        verifier_work = self.store.root / "brain/calls" / "source-read-verifier"
        verifier_work.mkdir(parents=True)
        identity = {"role": "verifier", "stage": "verify-progress", "call_id": "source-read-verifier"}
        (verifier_work / "context.json").write_text(json.dumps({**identity,
            "review_package_ref": self.store.retrieve("review_package", limit=1)[0]}), encoding="utf-8")
        (verifier_work / "call.json").write_text(json.dumps(identity), encoding="utf-8")
        # Reads of the authorized review package remain independent of whether
        # this diagnostic service is an active writer.
        service = AgentService(self.store.root, "verifier", "verify-progress", "source-read-verifier")
        package = service.read_review_package()
        required_records = package["required_records"]
        while package.get("next"):
            package = service.read_review_package(**package["next"])
            required_records.extend(package["required_records"])
        proof_record = next(r for r in required_records if r["ref"] == proof_ref)
        self.assertEqual(proof_record["payload"]["proof_draft"]["body"], expected)
        before = (copy.deepcopy(script.calls), self.adapter.launches, self.store.get_meta("conclusion_ref"))
        report = (self.root / "output/final.md").read_text(encoding="utf-8")
        self.assertIn(expected, report)
        (self.root / "output/final.md").unlink()
        self.assertEqual(self.controller(script).run()["status"], "completed")
        self.assertEqual(before, (script.calls, self.adapter.launches, self.store.get_meta("conclusion_ref")))
        self.assertEqual(report, (self.root / "output/final.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
