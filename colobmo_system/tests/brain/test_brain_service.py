"""Versioned service and real MCP coverage; no model services are invoked."""
from __future__ import annotations
from brain_fixtures import write_review_package

import copy
import json
from pathlib import Path
import tempfile
import unittest

from colombo.configuration import PROJECT_ROOT
from colombo.configuration import load_config
from colombo.brain.proof_draft import initial_proof, write_proof
from colombo.brain.mcp_server import AgentService
from colombo.brain.research_records import state_view
from colombo.brain.research_store import Store
from colombo.brain.model_calls import BackendError
import test_mcp as mcp_helpers
import test_backend as backend_helpers


def create_fixture(test):
    temporary_root = PROJECT_ROOT / "validation/tmp"
    temporary_root.mkdir(parents=True, exist_ok=True)
    test.temporary = tempfile.TemporaryDirectory(prefix="service-v2-", dir=temporary_root)
    test.addCleanup(test.temporary.cleanup)
    test.folder = Path(test.temporary.name)
    config = load_config()
    test.store = Store.create(test.folder / "run", "Prove the sample statement", [], config, [])
    test.seed = write_proof(test.store, initial_proof(test.store), "initial-proof")
    test.store.set_meta(proof_ref=test.seed, result_events=[{"id": "E1", "state": "pending"}],
                        prune_commands=[], event_data=None)
    source = test.store.root / "tasks/T0001/results/A0001/proof.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Proof\nA fixed synthetic proof for service testing.\n", encoding="utf-8")
    test.artifact = {"path": source.relative_to(test.store.root).as_posix(),
                     "size": source.stat().st_size}
    test.result = test.store.write_record("result", {"accepted": True, "task_id": "T0001",
        "attempt_id": "A0001", "summary": "Synthetic fixture", "artifacts": [test.artifact]})

    from brain_fixtures import confirm_result, freeze_setting
    freeze_setting(test.store)
    confirm_result(test.store, test.result)


def observation(test):
    from brain_fixtures import confirm_result, progress
    rid = test.result["id"]
    confirm_result(test.store, test.result)
    proof = copy.deepcopy(test.store.read_record(test.seed)["proof_draft"])
    proof["body"] = "A fixed synthetic proof for service testing."
    proof["open_questions"] = []
    proof["steps"][0].update(status="checked", gaps=[], evidence=[{
        "result_ref": rid, "path": test.artifact["path"], "locator": "Proof"}])
    return {"summary": "Synthetic integration proposal", "result_refs": [rid],
        "update": {"admissions": [{"result_ref": rid, "verdict": "accepted", "goal_ids": ["G0"],
            "proof_step_ids": ["P0"], "reason": "Verified fixture Claim", "completion_status": "completed",
            "completed_parts": ["Assigned goal"], "remaining": []}],
            "proof_draft": proof, "rechecked_step_ids": [], "progress": progress([rid])},
        "prunes": [], "next_action": "continue", "rationale": "Partial progress needs final review"}


class BrainServiceTests(unittest.TestCase):
    setUp = create_fixture
    prepare_call = mcp_helpers.MCPServerTests.prepare_call

    def service(self, stage="integrate", call_id="integrate-1", **context):
        self.prepare_call("brain", stage, call_id, result_refs=[self.result], previous_proof_ref=self.seed,
                          task_snapshot=[], **context)
        return AgentService(self.store.root, "brain", stage, call_id)

    def test_seed_view_and_exact_historical_proof_navigation(self):
        service = self.service()
        view = service.read_research()
        self.assertEqual(view["proof_ref"], self.seed)
        self.assertFalse(view["proof_revision_reviewed"])
        self.assertNotIn("body", view["proof_index"])
        self.assertEqual(view["pending_returns"][0]["id"], "E1")
        proof = service.read_research(section="proof")
        self.assertIn("body", proof["payload"]["proof_draft"])
        self.assertEqual(service.read_research(section="proof", id=self.seed["id"])["payload"], proof["payload"])
        with self.assertRaisesRegex(ValueError, "research section"):
            service.read_research(section="proof", id=self.result["id"])
        self.assertEqual(service.read_research(ref=self.seed["id"])["payload"]["proof_draft"],
                         proof["payload"]["proof_draft"])

    def test_evidence_navigation_rejects_unauthorized_and_missing_artifacts(self):
        service = self.service()
        read = service.read_material(self.result["id"], self.artifact["path"])
        self.assertIn("fixed synthetic", read["text"])
        with self.assertRaises(ValueError):
            service.read_material(self.result["id"], "input/goal.md")
        with self.assertRaises(ValueError):
            service.read_material(self.seed["id"], self.artifact["path"])
        (self.store.root / self.artifact["path"]).unlink()
        with self.assertRaises(ValueError):
            service.read_material(self.result["id"], self.artifact["path"])

    def test_observation_is_idempotent_candidate_not_official_progress(self):
        service = self.service()
        payload = observation(self)
        submitted = service.submit("integrate", payload)
        self.assertEqual(self.store.record_kind(submitted["ref"]), "assessment")
        self.assertEqual(service.submit("integrate", payload)["ref"], submitted["ref"])
        self.assertIsNone(self.store.get_meta("progress_ref"))
        self.assertEqual(self.store.get_meta("proof_ref"), self.seed)
        self.assertEqual(self.store.get_meta("prune_commands"), [])
        changed = copy.deepcopy(payload)
        changed["summary"] = "A different logical submission"
        with self.assertRaises(ValueError):
            service.submit("integrate", changed)

    def test_role_stage_version_and_stale_write_guards(self):
        service = self.service()
        with self.assertRaisesRegex(ValueError, "stage"):
            service.submit("plan", {})
        self.store.set_meta(pending_call=None)
        with self.assertRaisesRegex(ValueError, "no longer active"):
            service.submit("integrate", observation(self))
        config = self.store.get_meta("config")
        config["workflow"]["version"] = 1
        self.store.set_meta(config=config)
        with self.assertRaisesRegex(ValueError, "workflow version"):
            AgentService(self.store.root, "brain", "integrate", "integrate-1")

    def test_verifier_reads_only_frozen_proof_versions(self):
        other = write_proof(self.store, initial_proof(self.store), "unrelated-proof")
        package = write_review_package(self.store, {
            "allowed_refs": [self.seed["id"]], "required_checked_refs": [self.seed["id"]]})
        self.prepare_call("verifier", "verify-progress", "verify-1", review_package_ref=package)
        service = AgentService(self.store.root, "verifier", "verify-progress", "verify-1")
        self.assertEqual(service.read_research(ref=self.seed["id"])["ref"], self.seed)
        with self.assertRaisesRegex(ValueError, "outside"):
            service.read_research(ref=other["id"])
        with self.assertRaises(ValueError):
            service.read_research(section="proof")


class BrainMCPTests(unittest.IsolatedAsyncioTestCase):
    setUp = create_fixture
    prepare_call = mcp_helpers.MCPServerTests.prepare_call
    connect = mcp_helpers.MCPServerTests.connect

    async def test_real_mcp_record_results_and_proof_tools(self):
        self.prepare_call("brain", "integrate", "mcp-current", result_refs=[self.result],
                          previous_proof_ref=self.seed, task_snapshot=[])
        async with self.connect("brain", "integrate", "mcp-current") as session:
            names = {tool.name for tool in (await session.list_tools()).tools}
            self.assertEqual(names, {"read_research", "read_material", "save_note", "record_results", "audit", "lookup", "scientific_memory", "job_status"})
            removed = await session.call_tool("record_observation", {"payload": observation(self)})
            self.assertTrue(removed.isError)
            proof = await session.call_tool("read_research", {"section":"proof"})
            self.assertFalse(proof.isError, mcp_helpers.error_text(proof))
            self.assertEqual(mcp_helpers.response_object(proof)["ref"], self.seed)
            source = await session.call_tool("read_material", {"ref": self.result["id"], "path": self.artifact["path"]})
            self.assertFalse(source.isError, mcp_helpers.error_text(source))
            submitted = await session.call_tool("record_results", {"payload": observation(self)})
            self.assertFalse(submitted.isError, mcp_helpers.error_text(submitted))
            self.assertEqual(self.store.record_kind(mcp_helpers.response_object(submitted)["ref"]), "assessment")
            replay = await session.call_tool("record_results", {"payload": observation(self)})
            self.assertFalse(replay.isError, mcp_helpers.error_text(replay))
            self.assertEqual(mcp_helpers.response_object(replay)["ref"], mcp_helpers.response_object(submitted)["ref"])
            changed = observation(self)
            changed["summary"] = "A different result assessment"
            rejected = await session.call_tool("record_results", {"payload": changed})
            self.assertTrue(rejected.isError)
            self.assertEqual(self.store.get_meta("proof_ref"), self.seed)
            self.assertIsNone(self.store.get_meta("progress_ref"))
            denied = await session.call_tool("write_review", {"payload": {}})
            self.assertTrue(denied.isError)

    async def test_record_results_rejects_plan_stage(self):
        self.prepare_call("brain", "plan", "plan-cannot-record-results")
        async with self.connect("brain", "plan", "plan-cannot-record-results") as session:
            rejected = await session.call_tool("record_results", {"payload": observation(self)})
            self.assertTrue(rejected.isError)
            self.assertIn("Unknown tool", mcp_helpers.error_text(rejected))
            self.assertIsNone(self.store.get_meta("progress_ref"))


class BrainBackendTests(unittest.TestCase):
    setUp = backend_helpers.BackendTests.setUp
    spawn = backend_helpers.BackendTests.spawn
    write_submission = backend_helpers.BackendTests.write_submission

    def test_process_results_routes_update_and_prune_in_one_call(self):
        self.config["workflow"] = {"version": 3}
        def callback(process, prompt, timeout):
            work = Path(process.command[process.command.index("-C") + 1])
            self.assertEqual((work / "protocol.md").read_text(encoding="utf-8"),
                             (self.project / "agents/brain/protocol.md").read_text(encoding="utf-8"))
            paths = [".agents/skills/update/SKILL.md", ".agents/skills/prune/SKILL.md"]
            for path in paths:
                self.assertTrue((work / path).is_file())
            self.assertFalse((work / ".agents/skills/process_results/SKILL.md").exists())
            self.assertLess(prompt.index(paths[0]), prompt.index(paths[1]))
            self.assertIn("record_results", prompt)
            context = json.loads((work / "context.json").read_text(encoding="utf-8"))
            self.assertEqual(context["workflow_version"], 3)
            self.assertEqual(context["stage"], "process_results")
            manifest = json.loads((work / "call.json").read_text(encoding="utf-8"))
            self.assertNotIn("call_budget", manifest["input"]["context"])
            budget = context.pop("call_budget")
            self.assertEqual(manifest["input"]["context"], context)
            self.assertEqual(budget["started_at_unix"], manifest["started_at"])
            self.assertEqual(budget["timeout_seconds"], manifest["timeout_seconds"])
            self.assertEqual(budget["deadline_unix"], manifest["started_at"] + manifest["timeout_seconds"])
            self.assertGreater(timeout, 0)
            self.assertLessEqual(timeout, budget["timeout_seconds"])
            self.assertEqual(manifest["input"]["prompt"], "Process the result")
            self.write_submission(process)
        with self.spawn(callback) as launch:
            result = self.backend.invoke("brain", "process_results", self.run_root, "process-results-1", "Process the result", {})
            replay = self.backend.invoke("brain", "process_results", self.run_root, "process-results-1", "Process the result", {})
        self.assertEqual(result, replay)
        self.assertEqual(launch.call_count, 1)


    def test_conclude_cannot_launch_a_model(self):
        with self.spawn(lambda *args: self.fail("conclude must not spawn")) as launch:
            with self.assertRaises(BackendError):
                self.backend.invoke("brain", "conclude", self.run_root, "finish-1", "Conclude", {})
        self.assertEqual(launch.call_count, 0)

    def test_legacy_run_cannot_invoke_process_results(self):
        self.config["workflow"] = {"version": 1}
        with self.assertRaisesRegex(BackendError, "workflow version"):
            self.backend.invoke("brain", "process_results", self.run_root, "process-results-1", "Process results", {})


if __name__ == "__main__":
    unittest.main()
