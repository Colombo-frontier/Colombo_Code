"""Lower-bound instruction preparation and compatibility contracts, without model calls."""
import copy
import json
import tempfile
import unittest
from unittest.mock import patch

from colombo.configuration import PROJECT_ROOT
from colombo.configuration import load_config
from colombo.brain.submission_validation import ContractError, validate_semantics
from colombo.brain.controller import OracleController
from colombo.configuration import effective_mode
from brain_fixtures import SETTING, freeze_setting
from colombo.brain.mcp_server import AgentService, create_server
from colombo.brain.research_store import Store
from test_submission_validation import task_spec


def lower_task():
    task = task_spec()
    task.update(title="Zero-query Lower Bound", specialization="lower_bound",
                instructions="Prove the assigned Lower-bound Claim for every randomized zero-query Algorithm.")
    task["responsibility"].update(proof_step_ids=[],
        claim="Worst-case expected objective gap is at least 1/2 with zero Oracle calls.",
        scope="The fixed two-quadratic Function Class, arbitrary randomized output, exact first-order Oracle.")
    return task


class LowerBackend:
    def __init__(self):
        self.stages = []

    def invoke(self, role, stage, root, call_id, prompt, context):
        self.stages.append(stage)
        if stage == "plan":
            from test_oracle_workflow import SETTING
            return {"rationale": "A fixed-Family Lower-bound Task needs the dedicated pack.",
                    "tasks": [lower_task()], "setting_specification": SETTING}
        raise AssertionError("Unexpected model stage: " + stage)


class LowerBoundDispatchTests(unittest.TestCase):
    def setUp(self):
        parent = PROJECT_ROOT / "validation/tmp"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="lower-dispatch-", dir=parent)
        self.addCleanup(self.temp.cleanup)
        from pathlib import Path
        self.root = Path(self.temp.name)

    def make_store(self, mode="oracle_complexity"):
        config = {**load_config(), "research_mode": mode}
        return Store.create(self.root / "run", "Establish the zero-query Oracle Lower Bound", [], config)

    def prepare_call(self, store):
        work = store.root / "brain/calls/C00001"
        work.mkdir(parents=True)
        identity = {"role": "brain", "stage": "plan", "call_id": "C00001"}
        (work / "context.json").write_text(json.dumps(identity), encoding="utf-8")
        (work / "call.json").write_text(json.dumps(identity), encoding="utf-8")
        store.set_meta(pending_call=identity)

    def test_current_plan_to_real_lower_cell_preparation_and_idempotent_resume(self):
        from colombo.configuration import load_config as current_config
        store = Store.create(self.root / "run", "Establish the zero-query Oracle Lower Bound", [], current_config())
        backend = LowerBackend()
        controller = OracleController(PROJECT_ROOT, store.root, backend=backend)
        controller._initialize_proof()
        controller._plan()
        controller._prepare()
        self.assertEqual(backend.stages, ["plan"])
        self.assertEqual(store.get_meta("model_call_count"), 1)
        self.assertEqual(effective_mode(store), "oracle_complexity")
        task = store.get_task("T0001")
        assignment = store.read_record(task["assignment_ref"])
        folder = store.root / "tasks/T0001"
        mode = json.loads((folder / "cell/run.json").read_text())["cell_mode"]
        self.assertEqual(mode, {"research_mode": "oracle_complexity", "specialization": "lower_bound",
                                "instruction_version": "v8.1"})
        source = PROJECT_ROOT / "agents/cell/lower_bound"
        self.assertEqual((folder / "cell/AGENTS.md").read_bytes(), (source / "AGENTS.md").read_bytes())
        self.assertEqual((folder / "cell/lower_bound_review_guidance.md").read_bytes(),
                         (source / "review_guidance.md").read_bytes())
        self.assertTrue((folder / "cell/.agents/skills/lower-bound/SKILL.md").is_file())
        self.assertFalse((folder / "cell/.agents/skills/upper-bound").exists())
        self.assertFalse((folder / "cell/upper_bound_review_guidance.md").exists())
        self.assertFalse((folder / "cell/runtime/prover_state.json").exists())
        with patch("colombo.brain.cell_dispatch.subprocess.run") as launch:
            controller.tasks.adapter.prepare(folder, assignment, folder / "input/package",
                assignment_ref=task["assignment_ref"], package_ref=task["package_ref"])
        launch.assert_not_called()

    def test_oracle_mcp_schema_accepts_lower_and_freezes_submission_receipt(self):
        store = self.make_store()
        self.prepare_call(store)
        server = create_server(store.root, "brain", "plan", "C00001")
        tool = next(t for t in server._tool_manager.list_tools() if t.name == "submit_plan")
        schema = tool.parameters["properties"]["payload"]["properties"]["tasks"]["items"]
        self.assertEqual(schema["properties"]["specialization"]["enum"],
                         ["general", "upper_bound", "lower_bound", "experiment"])
        self.assertNotIn("specialization", schema["required"])
        service = AgentService(store.root, "brain", "plan", "C00001")
        payload = {"rationale": "Lower-bound research", "tasks": [lower_task()], "setting_specification": SETTING}
        receipt = service.submit("plan", payload)
        self.assertEqual(service.submit("plan", payload), receipt)
        self.assertEqual(store.read_record(receipt["ref"]), payload)

    def test_standalone_generic_instruction_pack_rejects_lower_bound(self):
        from colombo.cell.instructions import validate_mode
        with self.assertRaisesRegex(ValueError, "requires oracle_complexity"):
            validate_mode("generic", "lower_bound")

    def test_lower_resume_cannot_silently_switch_to_upper_or_general(self):
        store = self.make_store()
        freeze_setting(store)
        task = lower_task()
        first = store.write_record("plan", {"rationale": "Initial", "tasks": [task]})
        job = store.plan_jobs(first)[0]
        docs, _, _ = store.snapshot()
        assignment = docs["research"]["tasks"][job["task_id"]]["assignment_ref"]
        package = store.write_record("context_package", {"task_id": job["task_id"],
            "selection": task["package"], "artifacts": []})
        result = store.write_record("result", {"task_id": job["task_id"], "attempt_id": "A0001",
            "assignment_ref": assignment, "package_ref": package, "execution_status": "incomplete",
            "accepted": False, "artifacts": [], "stop_info": {"stage": "prover"},
            "budget_snapshot": {"prover": {"used": 1, "limit": 15, "remaining": 14},
                "current_review": {"state": "none"}, "diagnostic_errors": []}})
        store.save_task({"task_id": job["task_id"], "state": "returned", "attempt_no": 1,
                         "assignment_ref": assignment, "package_ref": package,
                         "active_attempt": "A0001", "finished_attempt": "A0001", "latest_result_ref": result})
        store.set_meta(round_no=1)
        resume = copy.deepcopy(task)
        resume.update(mode="resume", resume_task_id=job["task_id"])
        payload = {"rationale": "Continue original scope", "tasks": [resume]}
        self.assertEqual(validate_semantics("plan", payload, store, {}), payload)
        for changed in ("general", "upper_bound"):
            with self.subTest(changed=changed):
                altered = copy.deepcopy(payload)
                altered["tasks"][0]["specialization"] = changed
                with self.assertRaisesRegex(ContractError, "fixed Task"):
                    validate_semantics("plan", altered, store, {})


if __name__ == "__main__":
    unittest.main()
