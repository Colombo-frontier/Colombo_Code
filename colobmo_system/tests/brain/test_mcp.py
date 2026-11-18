"""Exercise the actual STDIO MCP server; no model or external service is called."""
from __future__ import annotations
from brain_fixtures import write_review_package

from contextlib import asynccontextmanager
from datetime import timedelta
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))
from colombo.configuration import load_config
from colombo.brain.research_store import Store
from colombo.brain.proof_draft import initial_proof, write_proof


def response_object(response):
    if response.isError:
        return None
    if response.structuredContent is not None:
        return response.structuredContent
    texts = [part.text for part in response.content if part.type == "text"]
    return json.loads("\n".join(texts))


def error_text(response):
    return "\n".join(part.text for part in response.content if part.type == "text")


class MCPServerTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        temporary_root = PROJECT / "validation"
        temporary_root.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="mcp-", dir=temporary_root)
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        material = self.folder / "source.txt"
        material.write_text("Explicitly supplied source material.\n", encoding="utf-8")
        config = load_config()
        self.store = Store.create(self.folder / "run", "Complete the sample task", ["Explain the result"],
                                  config, [material])
        self.seed = write_proof(self.store, initial_proof(self.store), "initial-proof")
        self.store.set_meta(proof_ref=self.seed)
        self.goal_ref = self.store.get_meta("goal_ref")
        self.material_ref = self.store.get_meta("material_refs")[0]

    def prepare_call(self, role, stage, call_id, **context):
        work = self.store.root / "brain/calls" / call_id
        work.mkdir(parents=True)
        identity = {"role": role, "stage": stage, "call_id": call_id}
        (work / "context.json").write_text(json.dumps({**context, **identity}), encoding="utf-8")
        (work / "call.json").write_text(json.dumps(identity), encoding="utf-8")
        self.store.set_meta(pending_call={**identity, "context": context})
        if role == "verifier" and context.get("review_package_ref"):
            package = self.store.read_record(context["review_package_ref"])
            if package.get("proof_ref"):
                self.store.set_meta(integration={"proof_ref": package["proof_ref"]})
        return work

    @asynccontextmanager
    async def connect(self, role, stage, call_id):
        env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
        parameters = StdioServerParameters(
            command=sys.executable,
            args=["-B", str(PROJECT / "run.py"), "mcp", "--run-dir", str(self.store.root),
                  "--role", role, "--stage", stage, "--call-id", call_id],
            env=env,
            cwd=str(PROJECT),
        )
        with (self.folder / f"{call_id}-stderr.log").open("w", encoding="utf-8") as error_log:
            async with stdio_client(parameters, errlog=error_log) as (read, write):
                async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=15)) as session:
                    await session.initialize()
                    yield session

    def plan(self):
        from brain_fixtures import SETTING
        return {"setting_specification": SETTING,
            "rationale": "The first task is self-contained with one explicit source.",
            "tasks": [{
                "title": "Read the supplied material",
                "instructions": "Explain the supplied material and its limits.",
                "deliverables": ["An explanation"],
                "completion_criteria": ["Cites the supplied source"],
                "mode": "new", "resume_task_id": None,
                "responsibility": {"problem_id":"G0", "claim":"Explain the supplied material", "assumptions":[],
                    "scope":"The supplied source", "goal_ids":["G0","G1"], "proof_step_ids":[],
                    "route_group":"explanation", "retain":False},
                "package": {"background": "A sample programme", "selection_reason": "The source is directly relevant.",
                            "items": [{"ref": self.material_ref["id"], "importance": "required",
                                       "purpose": "Read before answering", "limitations": "Only this short source is provided."}]},
            }],
        }

    def assessment(self, result_ref):
        from brain_fixtures import confirm_result
        confirm_result(self.store, result_ref, completion="incomplete", claims=[])
        goal = self.store.read_record(self.goal_ref)
        return {"summary": "There is partial progress.", "result_refs": [result_ref["id"]],
                "update": {"admissions": [{"result_ref":result_ref["id"],"verdict":"rejected",
                    "goal_ids":["G0"],"proof_step_ids":[],"reason":"No reviewed proof yet",
                    "completion_status":"incomplete","completed_parts":[],"remaining":["Complete proof"]}],
                    "progress": {"overall": "Partial verified Result", "status": "in_progress", "bracket":{"bounds":[],"regimes":[]}, "items": [
                    {"goal_id": target["id"], "description": target["text"], "status": "partial",
                     "result_refs": [result_ref["id"]], "remaining": ["Complete the explanation"]}
                    for target in goal["targets"]], "remaining": ["Complete the explanation"]}},
                "prunes":[], "next_action": "continue", "rationale": "More work is needed."}

    async def test_brain_tool_inventory_read_state_and_committed_plan(self):
        work = self.prepare_call("brain", "plan", "brain-plan-1")
        async with self.connect("brain", "plan", "brain-plan-1") as session:
            tool_names = {tool.name for tool in (await session.list_tools()).tools}
            self.assertEqual(tool_names, {"read_research", "read_material", "submit_plan", "audit", "save_note", "lookup", "scientific_memory", "job_status", "format_package_literal"})
            state = response_object(await session.call_tool("read_research", {}))
            self.assertEqual([item["id"] for item in state["goal"]["targets"]], ["G0", "G1"])
            self.assertIsNone(state["progress_ref"])
            source = await session.call_tool("read_material", {"ref": self.material_ref["id"]})
            self.assertFalse(source.isError, error_text(source))
            self.assertIn("Explicitly supplied", json.dumps(response_object(source)))

            # A plan-stage call may read data but may not submit an assessment.
            wrong_stage = await session.call_tool("record_assessment", {"payload": {}})
            self.assertTrue(wrong_stage.isError)
            self.assertIn("Unknown tool", error_text(wrong_stage))
            self.assertFalse((work / "submission.json").exists())

            submitted = await session.call_tool("submit_plan", {"payload": self.plan()})
            self.assertFalse(submitted.isError, error_text(submitted))
            receipt = response_object(submitted)
            self.assertEqual(receipt["status"], "submitted")
            self.assertEqual(self.store.record_kind(receipt["ref"]), "plan")
            stored = json.loads((work / "submission.json").read_text(encoding="utf-8"))
            self.assertNotIn("payload", stored)
            self.assertEqual(self.store.read_record(stored["ref"]), self.plan())
            self.assertEqual(stored["ref"], receipt["ref"])

            repeated = response_object(await session.call_tool("submit_plan", {"payload": self.plan()}))
            self.assertEqual(repeated["ref"], receipt["ref"])
            changed = self.plan()
            changed["rationale"] = "A different logical submission"
            conflict = await session.call_tool("submit_plan", {"payload": changed})
            self.assertTrue(conflict.isError)
            self.assertEqual(len(self.store.retrieve("plan")), 1)

    async def test_lookup_respects_frozen_switch_and_rejects_coerced_limits(self):
        config = self.store.get_meta("config")
        config["brain"]["search_enabled"] = False
        self.store.set_meta(config=config)
        self.prepare_call("brain", "plan", "lookup-disabled")
        async with self.connect("brain", "plan", "lookup-disabled") as session:
            response = await session.call_tool("lookup", {"query": "theorem"})
            self.assertFalse(response.isError, error_text(response))
            self.assertEqual(response_object(response)["error"]["kind"], "search_disabled")
            for limit in (True, "2"):
                response = await session.call_tool("lookup", {"query": "theorem", "limit": limit})
                self.assertTrue(response.isError)
    async def test_read_pagination_bounds_are_advertised_for_both_roles(self):
        from jsonschema import Draft202012Validator
        for role, stage in (("brain", "plan"), ("verifier", "verify-progress")):
            call_id = "paging-" + role
            context = {}
            if role == "verifier":
                context["review_package_ref"] = write_review_package(self.store, {
                    "allowed_refs": [self.material_ref["id"]],
                    "required_checked_refs": [self.material_ref["id"]]})
            self.prepare_call(role, stage, call_id, **context)
            async with self.connect(role, stage, call_id) as session:
                tools = {tool.name: tool for tool in (await session.list_tools()).tools}
                for name, maximum, default in (("read_research", 50, 20), ("read_material", 32000, 12000)):
                    with self.subTest(role=role, tool=name):
                        schema = tools[name].inputSchema
                        fields = schema["properties"]
                        self.assertEqual(fields["offset"]["minimum"], 0)
                        self.assertEqual(fields["offset"]["default"], 0)
                        self.assertEqual(fields["limit"]["minimum"], 1)
                        self.assertEqual(fields["limit"]["maximum"], maximum)
                        self.assertEqual(fields["limit"]["default"], default)
                        validator = Draft202012Validator(schema)
                        base = {"ref": self.material_ref["id"]}
                        validator.validate(base)
                        validator.validate({**base, "offset": 0, "limit": maximum})
                        for invalid in ({"offset": -1}, {"limit": 0}, {"limit": maximum + 1}):
                            self.assertFalse(validator.is_valid({**base, **invalid}))
                # Schema metadata does not replace the existing runtime behavior:
                # material reads still clamp a zero limit to one character.
                response = await session.call_tool("read_material", {"ref": self.material_ref["id"], "limit": 0})
                self.assertFalse(response.isError, error_text(response))
                self.assertEqual(response_object(response)["text"], "E")

    async def test_stale_call_cannot_write_notes_or_submit(self):
        self.prepare_call("brain", "plan", "brain-stale-1")
        async with self.connect("brain", "plan", "brain-stale-1") as session:
            self.store.set_meta(pending_call={"call_id": "another-call"})
            for tool, arguments in [("save_note", {"text": "A late note"}),
                                    ("submit_plan", {"payload": self.plan()})]:
                response = await session.call_tool(tool, arguments)
                self.assertTrue(response.isError)
                self.assertIn("no longer active", error_text(response))
            self.assertEqual(self.store.retrieve("note"), [])

    async def test_assessment_is_only_a_candidate_and_cannot_promote_progress(self):
        result_ref = self.store.write_record("result", {"accepted": False, "task_id":"T0001", "attempt_id":"A0001", "summary": "Partial output", "artifacts": []})
        proposal = self.assessment(result_ref)
        work = self.prepare_call("brain", "process_results", "brain-integrate-1", result_refs=[result_ref])
        async with self.connect("brain", "process_results", "brain-integrate-1") as session:
            submitted = await session.call_tool("record_results", {"payload": proposal})
            self.assertFalse(submitted.isError, error_text(submitted))
            self.assertEqual(self.store.record_kind(response_object(submitted)["ref"]), "assessment")
            self.assertTrue((work / "submission.json").is_file())
            self.assertIsNone(self.store.get_meta("progress_ref"))
            state = response_object(await session.call_tool("read_research", {}))
            self.assertIsNone(state["confirmed_progress"])

    async def test_verifier_is_limited_to_frozen_refs_and_cannot_change_progress(self):
        result_ref = self.store.write_record("result", {"accepted": False, "task_id":"T0001", "attempt_id":"A0001", "summary": "Partial output", "artifacts": []})
        plan_ref = self.store.write_record("plan", self.plan())
        proposal_ref = self.store.write_record("assessment", self.assessment(result_ref))
        unrelated = self.store.write_record("note", {"text": "Unrelated private working note"})
        allowed = [self.goal_ref["id"], self.material_ref["id"], result_ref["id"], plan_ref["id"], proposal_ref["id"]]
        required = [self.goal_ref["id"], result_ref["id"], plan_ref["id"], proposal_ref["id"]]
        package_ref = write_review_package(self.store, {"allowed_refs": allowed, "required_checked_refs": required,
            "goal_ref": self.goal_ref, "proposal_ref": proposal_ref, "result_refs": [result_ref], "plan_ref": plan_ref})
        work = self.prepare_call("verifier", "verify-progress", "review-1", review_package_ref=package_ref)
        async with self.connect("verifier", "verify-progress", "review-1") as session:
            names = {tool.name for tool in (await session.list_tools()).tools}
            self.assertEqual(names, {"read_review_package", "read_research", "read_material", "write_review"})
            package = response_object(await session.call_tool("read_review_package", {}))
            self.assertEqual(package["allowed_refs"], allowed)
            permitted = await session.call_tool("read_research", {"ref": result_ref["id"]})
            self.assertFalse(permitted.isError, error_text(permitted))
            for tool in ("read_research", "read_material"):
                denied = await session.call_tool(tool, {"ref": unrelated["id"]})
                self.assertTrue(denied.isError)
                self.assertIn("outside", error_text(denied))
            absent_tool = await session.call_tool("record_assessment", {"payload": self.assessment(result_ref)})
            self.assertTrue(absent_tool.isError)

            insufficient = await session.call_tool("write_review", {"payload": {
                "verdict": "pass", "summary": "Incomplete coverage", "findings": [], "checked_refs": [self.goal_ref["id"]]}})
            self.assertTrue(insufficient.isError)
            self.assertFalse((work / "submission.json").exists())
            review = {"verdict": "pass", "summary": "Accurate partial progress with explicit remaining work.",
                      "findings": [], "checked_refs": required, "review_kind":"proof", "result_ref":None,
                      "confirmed_claims":[], "completion_status":"partial", "repair_kind":"none"}
            submitted = await session.call_tool("write_review", {"payload": review})
            self.assertFalse(submitted.isError, error_text(submitted))
            self.assertEqual(self.store.record_kind(response_object(submitted)["ref"]), "review")
            self.assertIsNone(self.store.get_meta("progress_ref"))
            self.assertEqual(self.store.read_record(proposal_ref), self.assessment(result_ref))

    async def test_model_cannot_submit_a_final_conclusion(self):
        work = self.prepare_call("brain", "plan", "brain-no-finish")
        async with self.connect("brain", "plan", "brain-no-finish") as session:
            inventory = {tool.name: tool for tool in (await session.list_tools()).tools}
            self.assertNotIn("submit_conclusion", inventory)
            self.assertIn("tasks", inventory["submit_plan"].inputSchema["properties"]["payload"]["properties"])
            denied = await session.call_tool("submit_conclusion", {"payload": {
                "status": "completed", "summary": "Unsupported completion", "result_refs": [], "remaining": []}})
            self.assertTrue(denied.isError)
            self.assertFalse((work / "submission.json").exists())


if __name__ == "__main__":
    unittest.main()
