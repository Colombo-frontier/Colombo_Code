"""Synthetic decisions exercise real Controller/store/contract boundaries."""
import copy
import tempfile
import time
import unittest
import json
import asyncio
from pathlib import Path

from colombo.configuration import load_config, PROJECT_ROOT
from colombo.brain.research_store import Store
from colombo.brain.controller import OracleController
from colombo.brain.submission_validation import validate_semantics, ContractError, proof_complete
from controller_fixtures import FakeCell
from controller_fixtures import event_task, AsyncCellFixture
from prune_fixtures import bind_prunes
from colombo.brain.mcp_server import AgentService, create_server
from colombo.brain.submission_validation import validate_progress

SETTING = {"specification": {"common_specification": {"task": "fixture", "oracle": "fixture"}, "regimes": [{"id": "R1"}]},
    "provenance": [{"entry": "common_specification", "source": "fixture", "status": "provided"}],
    "unknowns": [], "near_optimal_policy": "Allow polylog factors"}

class Backend:
    def __init__(self, *, repair=False, supplement=False):
        self.calls = []
        self.repair = repair
        self.supplement = supplement
        self.final_reviews = 0

    def invoke(self, role, stage, run_root, call_id, prompt, context):
        self.calls.append(stage)
        store = Store(run_root)
        if stage == "plan":
            if not store.get_meta("setting_ref"):
                return {"rationale": "fixture initial", "tasks": [event_task("A")], "setting_specification": SETTING}
            return {"rationale": "fixture repair or supplement", "tasks": [event_task("B")]}
        if stage == "verify-progress":
            package = store.read_record(context["review_package_ref"])
            claims = []
            failed = False
            if package["review_kind"] == "result":
                rid = package["result_ref"]
                paths = [a["path"] for a in store.read_record(rid)["artifacts"]]
                claims = [{"id": kind, "kind": kind, "statement": "fixture " + kind,
                    "assumptions": [], "scope": "R1", "expression": "1", "evidence_paths": paths}
                    for kind in ("upper_bound", "lower_bound")]
                if store.read_record(rid)["execution_status"] == "cancelled":
                    claims = []
            else:
                self.final_reviews += 1
                failed = self.repair and self.final_reviews == 1
            completion = "partial"
            if package["review_kind"] == "proof" and not failed:
                proof = store.read_record(package["proof_ref"])["proof_draft"]
                completion = "completed" if proof_complete(proof) else "partial"
            return {"verdict": "revise" if failed else "pass", "summary": "fixture review",
                "findings": [{"subject": "composition", "reason": "repair fixture", "result_refs": []}] if failed else [],
                "checked_refs": package["required_checked_refs"], "review_kind": package["review_kind"],
                "result_ref": package["result_ref"], "confirmed_claims": claims,
                "completion_status": completion, "repair_kind": "research" if failed else "none"}
        refs = list(store.get_meta("result_reviews", {}))
        rid = next((r for r in reversed(refs) if store.read_record(store.get_meta("result_reviews")[r])["confirmed_claims"]), refs[-1])
        review = store.get_meta("result_reviews")[rid]["id"]
        complete = stage == "integrate"
        progress = {"overall": "Fixture progress description", "status": "completed" if complete else "in_progress",
            "items": [{"goal_id": "G0", "description": "fixture", "status": "supported" if complete else "partial", "result_refs": refs,
                "remaining": [] if complete else ["composition"]}], "remaining": [] if complete else ["composition"],
            "bracket": {"bounds": [{"id": kind, "direction": kind, "expression": "1", "scope": "R1", "assumptions": [],
                "source": "fixture", "evidence_state": "certified", "result_ref": rid, "review_ref": review, "claim_id": kind}
                for kind in ("upper_bound", "lower_bound")], "regimes": [{"id": "R1", "scope": "R1", "lower_bound_ids": ["lower_bound"],
                "upper_bound_ids": ["upper_bound"], "gap": "1", "candidate_rate": "1", "candidate_basis": "fixture",
                "status": "near_optimal" if complete else "partial", "comparison_review_ref": None,
                "comparison_claim_id": None, "remaining": [] if complete else ["composition"]}]}}
        value = {"summary": "fixture", "result_refs": refs, "update": {"admissions": [], "progress": progress},
            "prunes": [], "next_action": "plan" if self.supplement and len(refs) == 1 else "conclude" if complete else "continue", "rationale": "fixture"}
        if complete:
            value["update"].update(proof_draft={"title": "Fixture Proof", "statement": "fixture", "assumptions": [], "body": "Full fixture Proof.",
                "steps": [{"id": "P0", "title": "fixture", "statement": "fixture", "status": "checked", "depends_on": [],
                "evidence": [{"result_ref": rid, "path": store.read_record(rid)["artifacts"][0]["path"], "locator": "all"}], "gaps": []}], "open_questions": []},
                rechecked_step_ids=["P0"])
        return value

class OracleWorkflowTests(unittest.TestCase):
    def make(self, directory, dispatch=1, waves=1):
        cfg = load_config()
        cfg["limits"].update(max_dispatches_per_wave=dispatch, max_rounds=waves)
        return Store.create(Path(directory) / "run", "fixture", [], cfg)

    def test_verifier_first_and_final_composition(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make(tmp)
            backend = Backend()
            OracleController(PROJECT_ROOT, store.root, backend, FakeCell()).run()
            self.assertEqual(backend.calls, ["plan", "verify-progress", "process_results", "integrate", "verify-progress"])
            self.assertEqual(store.get_meta("status"), "completed")
            self.assertFalse((store.root / "input/manifest.json").exists())
            self.assertTrue((store.root / "input/setting.json").exists())
            progress = store.read_record(store.get_meta("progress_ref"))["progress"]
            self.assertEqual(progress["overall"], "Fixture progress description")
            self.assertEqual(progress["bracket"]["regimes"][0]["comparison_review_ref"], store.get_meta("final_review_ref")["id"])
            docs = store.read_document("research") if hasattr(store, "read_document") else None

    def test_resume_after_plan_before_any_cell_is_prepared(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make(tmp)
            backend, cell = Backend(), FakeCell()
            preview = OracleController(PROJECT_ROOT, store.root, backend, cell)
            preview._initialize_proof()
            preview._plan()
            plan_ref = store.get_meta("round_data")["plan_ref"]
            store.set_meta(status="paused")
            self.assertEqual(store.get_meta("phase"), "preparing")
            self.assertEqual(store.list_tasks(), [])
            self.assertEqual(cell.launches, 0)

            OracleController(PROJECT_ROOT, store.root, backend, cell).run()

            self.assertEqual(backend.calls.count("plan"), 1)
            self.assertEqual(store.get_meta("round_data")["plan_ref"], plan_ref)
            self.assertEqual(store.get_meta("dispatch_count"), 1)
            self.assertEqual(cell.launches, 1)
            self.assertEqual(store.get_meta("status"), "completed")

    def source_backend(self, reject_first=False):
        class SourceBackend(Backend):
            def invoke(self, role, stage, root, cid, prompt, context):
                store = Store(root)
                if stage == "plan" and not store.get_meta("setting_ref"):
                    self.calls.append(stage)
                    return {"rationale": "Input already contains a complete source Proof", "tasks": [], "setting_specification": SETTING}
                if stage == "plan" and reject_first:
                    assert store.get_meta("progress_ref") is None
                    assert store.get_meta("final_review_ref") is None
                if stage == "integrate" and not store.get_meta("result_reviews"):
                    self.calls.append(stage)
                    source = store.get_meta("material_refs")[0]["id"]
                    progress = {"overall": "All source regimes proved", "status": "completed",
                        "items": [{"goal_id": "G0", "description": "source result", "status": "supported", "result_refs": [], "remaining": []}],
                        "remaining": [], "bracket": {"bounds": [{"id": kind, "direction": kind, "expression": "1", "scope": "R1",
                        "assumptions": [], "source": source, "evidence_state": "baseline", "result_ref": None, "review_ref": None, "claim_id": None}
                        for kind in ("upper_bound", "lower_bound")], "regimes": [{"id": "R1", "scope": "R1",
                        "lower_bound_ids": ["lower_bound"], "upper_bound_ids": ["upper_bound"], "gap": "1",
                        "candidate_rate": "", "candidate_basis": "", "status": "near_optimal",
                        "comparison_review_ref": None, "comparison_claim_id": None, "remaining": []}]}}
                    with self_test.assertRaises(ContractError):
                        validate_progress(store, progress)  # Ordinary update has no source-only shortcut.
                    return {"summary": "Integrate supplied source Proof", "result_refs": [],
                        "update": {"admissions": [], "progress": progress, "proof_draft": {
                            "title": "Source Proof", "statement": "fixed fixture", "assumptions": [],
                            "body": "Complete self-contained source fixture Proof.", "open_questions": [],
                            "steps": [{"id": "S1", "title": "Source derivation", "statement": "fixed fixture", "status": "checked",
                                "depends_on": [], "evidence": [], "gaps": []}]}, "rechecked_step_ids": ["S1"]},
                        "prunes": [], "next_action": "conclude", "rationale": "Source Proof needs final verification"}
                if stage == "verify-progress" and not store.get_meta("result_reviews"):
                    package = store.read_record(context["review_package_ref"])
                    if package["review_kind"] == "proof":
                        self.calls.append(stage)
                        self.final_reviews += 1
                        for ref in store.get_meta("material_refs"):
                            assert ref["id"] in package["required_checked_refs"]
                        failed = reject_first and self.final_reviews == 1
                        return {"verdict": "revise" if failed else "pass", "summary": "Source Proof review",
                            "findings": [{"subject": "source Proof", "reason": "Missing argument", "result_refs": []}] if failed else [],
                            "checked_refs": package["required_checked_refs"], "review_kind": "proof", "result_ref": None,
                            "confirmed_claims": [], "completion_status": "incomplete" if failed else "completed",
                            "repair_kind": "research" if failed else "none"}
                return super().invoke(role, stage, root, cid, prompt, context)
        self_test = self
        return SourceBackend()

    def make_source_run(self, tmp):
        source = Path(tmp) / "source-proof.md"
        source.write_text("Complete self-contained source fixture Proof.", encoding="utf-8")
        cfg = load_config()
        cfg["limits"].update(max_dispatches_per_wave=1, max_rounds=1)
        return Store.create(Path(tmp) / "run", "fixed fixture", [], cfg, [source])

    def test_already_proved_input_integrates_without_cells(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_source_run(tmp)
            cell, backend = FakeCell(), self.source_backend()
            OracleController(PROJECT_ROOT, store.root, backend, cell).run()
            self.assertEqual(backend.calls, ["plan", "integrate", "verify-progress"])
            self.assertEqual(cell.launches, 0)
            self.assertEqual(store.get_meta("dispatch_count"), 0)
            self.assertEqual(store.get_meta("round_no"), 1)
            self.assertEqual(store.get_meta("status"), "completed")
            adopted = store.read_record(store.get_meta("progress_ref"))["progress"]
            validate_progress(store, adopted)
            changed = copy.deepcopy(adopted)
            changed["items"][0]["description"] = "A different unreviewed claim"
            with self.assertRaises(ContractError):
                validate_progress(store, changed)

    def test_rejected_source_proof_is_not_adopted_and_dispatches_repair(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_source_run(tmp)
            cell, backend = FakeCell(), self.source_backend(reject_first=True)
            OracleController(PROJECT_ROOT, store.root, backend, cell).run()
            self.assertEqual(backend.calls[:4], ["plan", "integrate", "verify-progress", "plan"])
            self.assertEqual(cell.launches, 1)
            self.assertEqual(store.get_meta("dispatch_count"), 1)
            self.assertEqual(backend.final_reviews, 2)
            self.assertEqual(store.get_meta("status"), "completed")

    def test_final_failure_dispatches_repair_without_resetting_quota(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make(tmp, dispatch=1, waves=2)
            backend = Backend(repair=True)
            OracleController(PROJECT_ROOT, store.root, backend, FakeCell()).run()
            self.assertEqual(store.get_meta("dispatch_count"), 2)
            self.assertEqual(backend.final_reviews, 2)
            self.assertEqual(store.get_meta("round_no"), 2)

    def test_supplemental_plan_is_immutable(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make(tmp, dispatch=2)
            backend = Backend(supplement=True)
            OracleController(PROJECT_ROOT, store.root, backend, FakeCell()).run()
            plans = store.retrieve("plan")
            self.assertEqual(len(plans), 2)
            self.assertEqual([len(store.read_record(p)["tasks"]) for p in plans], [1, 1])
            self.assertEqual(store.get_meta("round_no"), 1)
            self.assertEqual(store.get_meta("dispatch_count"), 2)

    def test_final_repair_can_resume_same_task_within_same_wave(self):
        class ResumeBackend(Backend):
            def invoke(self, role, stage, root, cid, prompt, context):
                store = Store(root)
                if stage == "plan" and store.get_meta("setting_ref"):
                    self.calls.append(stage)
                    task = copy.deepcopy(store.read_record(store.get_task("T0001")["assignment_ref"])["spec"])
                    task.update(mode="resume", resume_task_id="T0001")
                    return {"rationale": "Repair the same fixed Task", "tasks": [task]}
                value = super().invoke(role, stage, root, cid, prompt, context)
                if stage == "process_results":
                    value["next_action"] = "conclude"
                return value
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make(tmp, dispatch=2)
            backend = ResumeBackend(repair=True)
            cell = FakeCell()
            OracleController(PROJECT_ROOT, store.root, backend, cell).run()
            self.assertEqual(store.get_meta("dispatch_count"), 2)
            self.assertEqual(store.get_meta("round_no"), 1)
            self.assertEqual(store.get_task("T0001")["finished_attempt"], "A0002")
            self.assertEqual(cell.launches, 2)
            self.assertEqual(len(store.read_document("research")["tasks"]["T0001"]["attempts"]), 2)

    def test_audited_pruning_waits_for_verified_return_and_stop_receipt(self):
        class PruningBackend(Backend):
            def invoke(self, role, stage, root, cid, prompt, context):
                value = super().invoke(role, stage, root, cid, prompt, context)
                store = Store(root)
                if stage == "plan":
                    value["tasks"].append(event_task("B"))
                if stage == "process_results" and len(store.get_meta("processed_results", [])) == 0:
                    source = context["result_refs"][0]["id"]
                    assert source in store.get_meta("result_reviews")
                    proposal = {"task_id": "T0002", "attempt_id": "A0001", "reason": "subsumed",
                        "evidence_refs": [source], "relation_explanation": "fixture implication", "scope_check": "fixture scopes",
                        "covered_deliverables": ["A complete synthetic proof"], "premises": [{"result_ref": source,
                        "statement": "fixture upper_bound", "assumptions": [], "scope": "R1"}]}
                    value["prunes"] = bind_prunes(store, context, [proposal])
                return value
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make(tmp, dispatch=2)
            cell = AsyncCellFixture()
            try:
                OracleController(PROJECT_ROOT, store.root, PruningBackend(), cell).run()
                self.assertTrue(cell.stop_requests)
                self.assertEqual(store.get_task("T0002")["execution_status"], "cancelled")
                self.assertTrue(all(c["state"] == "confirmed" for c in store.get_meta("prune_commands")))
            finally:
                cell.close()

    def test_unreviewed_and_empirical_claims_cannot_certify_bounds(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make(tmp)
            with self.assertRaises(ContractError):
                from colombo.brain.submission_validation import result_review
                result_review(store, "unreviewed")

    def test_real_service_submission_and_tool_schemas(self):
        class ServiceBackend(Backend):
            def invoke(self, role, stage, root, cid, prompt, context):
                value = super().invoke(role, stage, root, cid, prompt, context)
                work = Path(root) / "brain/calls" / cid
                work.mkdir(parents=True)
                (work / "context.json").write_text(json.dumps(context), encoding="utf-8")
                (work / "call.json").write_text(json.dumps({"role": role, "stage": stage, "call_id": cid}), encoding="utf-8")
                # Read the real registered tool table without opening the Windows
                # asyncio self-pipe (blocked in some desktop sandboxes).
                tools = create_server(root, role, stage, cid)._tool_manager.list_tools()
                names = {t.name for t in tools}
                assert ("record_results" if stage in {"integrate", "process_results"} else "submit_plan" if stage == "plan" else "write_review") in names
                service = AgentService(root, role, stage, cid)
                if role == "verifier":
                    service.read_review_package()
                service.submit(stage, value)
                return value
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make(tmp)
            OracleController(PROJECT_ROOT, store.root, ServiceBackend(), FakeCell()).run()
            self.assertEqual(store.get_meta("status"), "completed")

    def test_expired_integrate_does_not_restart_clock_or_launch_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make(tmp)
            backend = Backend()
            controller = OracleController(PROJECT_ROOT, store.root, backend, FakeCell())
            controller._initialize_proof()
            store.set_meta(phase="integrating", integration={"started_at": 1, "deadline_unix": 2,
                "research_generation": 0, "revision": 5})
            controller.run()
            self.assertEqual(backend.calls, [])
            self.assertEqual(store.get_meta("stop_reason"), "integration_timeout")
            self.assertNotEqual(store.get_meta("status"), "completed")

    def test_recovery_retains_previous_jobs_during_supplement_prepare(self):
        class FailPreparation(FakeCell):
            def prepare(self, *args, **kwargs):
                raise RuntimeError("simulated preparation interruption")
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make(tmp, dispatch=2)
            controller = OracleController(PROJECT_ROOT, store.root, Backend(), FakeCell())
            controller._initialize_proof()
            controller._plan()
            controller._prepare()
            first = controller.tasks.jobs()[0]
            controller.tasks.run_job(first)
            store.set_meta(planning_wave=1)
            controller._plan()
            controller.tasks.adapter = FailPreparation()
            with self.assertRaises(RuntimeError):
                controller._prepare()
            self.assertEqual(len(controller.tasks.jobs()), 2)
            self.assertEqual(controller._remaining_dispatch(), 0)
            self.assertTrue(controller.tasks.terminal(first))
            controller.tasks.adapter = FakeCell()
            controller._prepare()
            self.assertEqual(len(controller.tasks.jobs()), 2)

if __name__ == "__main__":
    unittest.main()
