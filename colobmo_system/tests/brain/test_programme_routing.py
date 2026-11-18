"""Routing, package assembly and receipt recovery without model/network calls."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.configuration import PROJECT_ROOT
from colombo.configuration import load_config
from colombo.brain.submission_validation import ContractError, validate_semantics
from colombo.configuration import effective_mode
from colombo.brain.mcp_server import AgentService, create_server
from colombo.brain.research_store import Store
import test_backend as backend_fixture
import test_cell_adapter as adapter_fixture
from test_submission_validation import task_spec


class ProgrammeRoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=PROJECT_ROOT / "validation")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def make_store(self, mode="oracle_complexity", **limits):
        config = load_config()
        config["research_mode"] = mode
        config["limits"].update(limits)
        store = Store.create(self.root / "run", "Find an Oracle complexity upper bound", [], config)
        from brain_fixtures import freeze_setting
        freeze_setting(store)
        return store




    def test_current_mode_is_oracle_without_a_router_decision(self):
        from colombo.configuration import load_config as current_config
        config = current_config()
        store = Store.create(self.root / "current", "Find a near-optimal rate", [], config)
        self.assertEqual(effective_mode(store), "oracle_complexity")
        self.assertEqual(store.get_meta("model_call_count", 0), 0)
        self.assertEqual(store.retrieve("routing"), [])
        self.prepare_call(store, "route")
        with self.assertRaisesRegex(ValueError, "role/stage"):
            create_server(store.root, "brain", "route", "C00001")



    def test_upper_bound_requires_mode_and_optional_general_is_default(self):
        store = self.make_store("oracle_complexity")
        task = task_spec()
        task["responsibility"]["proof_step_ids"] = []
        plan = {"rationale": "Test", "tasks": [task]}
        self.assertNotIn("specialization", validate_semantics("plan", plan, store, {})["tasks"][0])
        task["specialization"] = "upper_bound"
        self.assertEqual(validate_semantics("plan", plan, store, {})["tasks"][0]["specialization"], "upper_bound")
        task["specialization"] = "other"
        with self.assertRaises(ContractError):
            validate_semantics("plan", plan, store, {})

    def prepare_call(self, store, stage):
        work = store.root / "brain/calls/C00001"
        work.mkdir(parents=True)
        identity = {"role": "brain", "stage": stage, "call_id": "C00001"}
        (work / "context.json").write_text(json.dumps(identity), encoding="utf-8")
        (work / "call.json").write_text(json.dumps(identity), encoding="utf-8")
        store.set_meta(pending_call=identity)


    def test_current_schema_advertises_all_supported_cell_specializations(self):
        store = self.make_store()
        self.prepare_call(store, "plan")
        server = create_server(store.root, "brain", "plan", "C00001")
        tool = next(t for t in server._tool_manager.list_tools() if t.name == "submit_plan")
        task = tool.parameters["properties"]["payload"]["properties"]["tasks"]["items"]
        self.assertEqual(task["properties"]["specialization"]["enum"], ["general", "upper_bound", "lower_bound", "experiment"])
        self.assertNotIn("specialization", task["required"])

    def test_resume_preserves_specialization_and_optional_default_receipt(self):
        store = self.make_store("oracle_complexity")
        task = task_spec()
        task["responsibility"]["proof_step_ids"] = []
        first = store.write_record("plan", {"rationale": "Initial", "tasks": [task]})
        job = store.plan_jobs(first)[0]
        # The immutable plan already created the task definition.
        docs, _, _ = store.snapshot()
        assignment_ref = docs["research"]["tasks"][job["task_id"]]["assignment_ref"]
        package_ref = store.write_record("context_package", {"task_id": job["task_id"],
            "selection": task["package"], "artifacts": []})
        result_ref = store.write_record("result", {"task_id": job["task_id"], "attempt_id": "A0001",
            "assignment_ref": assignment_ref, "package_ref": package_ref, "execution_status": "incomplete",
            "accepted": False, "artifacts": [], "stop_info": {"stage": "prover"},
            "budget_snapshot": {"prover": {"used": 1, "limit": 15, "remaining": 14},
                "current_review": {"state": "none"}, "diagnostic_errors": []}})
        store.save_task({"task_id": job["task_id"], "state": "returned", "attempt_no": 1,
                         "assignment_ref": assignment_ref, "package_ref": package_ref,
                         "active_attempt": "A0001", "finished_attempt": "A0001", "latest_result_ref": result_ref})
        store.set_meta(round_no=1)
        resume = copy.deepcopy(task)
        resume.update(mode="resume", resume_task_id=job["task_id"], specialization="general")
        payload = {"rationale": "Continue the same scope", "tasks": [resume]}
        validated = validate_semantics("plan", payload, store, {})
        second = store.write_record("plan", validated, request_id="resume-plan")
        self.assertEqual(store.write_record("plan", validated, request_id="resume-plan"), second)
        self.assertEqual(store.read_record(second), payload)
        resume["specialization"] = "upper_bound"
        with self.assertRaises(ContractError):
            validate_semantics("plan", payload, store, {})


class RoutingWorkspaceTests(unittest.TestCase):
    """Use the existing fake native process harness, never a real Codex call."""
    spawn = backend_fixture.BackendTests.spawn
    write_submission = backend_fixture.BackendTests.write_submission

    def setUp(self):
        backend_fixture.BackendTests.setUp(self)

    def test_brain_uses_role_instructions_without_domain_directory(self):
        for mode in ("generic", "oracle_complexity"):
            def callback(proc, prompt, timeout):
                work = Path(proc.command[proc.command.index("-C") + 1])
                self.assertFalse((work / "domain_guidance.md").exists())
                self.assertNotIn("domain_guidance.md", prompt)
                self.assertEqual((work / "AGENTS.md").read_bytes(),
                                 (self.project / "agents/brain/AGENTS.md").read_bytes())
                self.assertTrue((work / ".agents/skills/plan/SKILL.md").is_file())
                self.assertFalse((work / ".agents/skills/route").exists())
                self.write_submission(proc)
            with self.spawn(callback):
                self.backend.invoke("brain", "plan", self.run_root, mode, "Plan", {
                    "research_routing": {"research_mode": mode}})
            # A second direct backend plan uses a fresh Wave in this assembly fixture.
            self.store.set_meta(round_no=1)

    def test_removed_router_is_rejected_before_workspace_or_process_creation(self):
        from colombo.brain.model_calls import BackendError
        for version in (2, 3):
            with self.subTest(workflow=version):
                self.config["workflow"]["version"] = version
                with patch("colombo.brain.model_calls.managed_popen") as launch:
                    with self.assertRaisesRegex(BackendError, "Invalid role/stage"):
                        self.backend.invoke("brain", "route", self.run_root, "removed-router", "Route", {})
                launch.assert_not_called()
                self.assertFalse((self.run_root / "brain/calls/removed-router").exists())

    def test_verifier_uses_role_instructions_without_domain_directory(self):
        from colombo.brain.proof_draft import initial_proof, write_proof
        self.store.set_meta(proof_ref=write_proof(self.store, initial_proof(self.store), "workspace-proof"))
        for mode in ("generic", "oracle_complexity"):
            def callback(proc, prompt, timeout):
                work = Path(proc.command[proc.command.index("-C") + 1])
                self.assertFalse((work / "domain_guidance.md").exists())
                self.assertNotIn("domain_guidance.md", prompt)
                self.assertEqual((work / "AGENTS.md").read_bytes(),
                                 (self.project / "agents/brain/verifier/AGENTS.md").read_bytes())
                self.assertTrue((work / ".agents/skills/verify-progress/SKILL.md").is_file())
                self.store.set_meta(integration={"proof_ref": self.store.get_meta("proof_ref")})
                self.write_submission(proc, {"review_kind": "proof", "result_ref": None, "verdict": "pass"})
            with self.spawn(callback):
                self.backend.invoke("verifier", "verify-progress", self.run_root, "review-" + mode,
                                    "Review", {"research_routing": {"research_mode": mode}})


class SpecializedAdapterTests(unittest.TestCase):
    setUp = adapter_fixture.CellAdapterTests.setUp
    tearDown = adapter_fixture.CellAdapterTests.tearDown

    def test_real_prepare_installs_upper_pack_and_freezes_it(self):
        assignment = {"task_id": "T0001", "research_mode": "oracle_complexity",
                      "spec": {**self.assignment, "specialization": "upper_bound"}}
        self.adapter.prepare(self.task, assignment, self.package, **self.refs)
        mode = json.loads((self.task / "cell/run.json").read_text())["cell_mode"]
        self.assertFalse((self.task / "cell/cell_mode.json").exists())
        self.assertEqual(mode, {"research_mode": "oracle_complexity", "specialization": "upper_bound",
                                "instruction_version": "v8.1"})
        self.assertTrue((self.task / "cell/.agents/skills/upper-bound/SKILL.md").is_file())
        prepared = json.loads((self.task / "prepared.json").read_text())
        self.assertTrue(all(prepared[key] == value for key, value in mode.items()))
        self.adapter.prepare(self.task, assignment, self.package, **self.refs)
        changed = copy.deepcopy(assignment)
        changed["spec"]["specialization"] = "general"
        with self.assertRaisesRegex(ValueError, "input differs"):
            self.adapter.prepare(self.task, changed, self.package, **self.refs)
        config_path = self.task / "cell/run.json"
        config = json.loads(config_path.read_text())
        config["cell_mode"] = {**mode, "specialization": "general"}
        config_path.write_text(json.dumps(config))
        with self.assertRaisesRegex(ValueError, "mode differs"):
            self.adapter.prepare(self.task, assignment, self.package, **self.refs)

    def test_generic_prepare_omits_upper_pack(self):
        self.adapter.prepare(self.task, self.assignment, self.package, **self.refs)
        self.assertFalse((self.task / "cell/.agents/skills/upper-bound").exists())
        self.assertFalse((self.task / "cell/upper_bound_review_guidance.md").exists())
        invalid = {**self.assignment, "specialization": "upper_bound"}
        with self.assertRaisesRegex(ValueError, "requires oracle_complexity"):
            self.adapter.prepare(self.task, invalid, self.package, **self.refs)


if __name__ == "__main__":
    unittest.main()
