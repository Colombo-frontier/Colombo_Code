"""Offline evaluation-harness checks; never launch research or hosted execution."""
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
from unittest.mock import Mock

PROJECT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("experiment_skill_eval", PROJECT / "scripts/evaluate_experiment_skills.py")
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)


class EvaluationHarnessTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".eval-harness-test-", dir=PROJECT)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "evaluation"
        # Synthetic pre-change pack for offline installation tests. Never depend
        # on excluded historical validation directories in a clean package.
        self.baseline = Path(temporary.name) / "baseline"
        shutil.copytree(PROJECT / "agents", self.baseline / "agents")
        added = (self.baseline / "agents/experiment_cell/skills/probe-mechanism").resolve()
        self.assertTrue(added.is_relative_to(self.baseline.resolve()))
        if added.exists():
            shutil.rmtree(added)

    def prepare(self):
        return evaluation.prepare(self.root, sys.executable, baseline=self.baseline)

    def test_config_caps_and_model_are_explicit_without_changing_production(self):
        before = (PROJECT / "config.toml").read_bytes()
        raw, config = evaluation.evaluation_config(sys.executable)
        self.assertEqual(config["profile"], "standard")
        self.assertEqual(config["cell"]["settings"]["agents"]["prover_max_rounds"], 3)
        self.assertEqual(config["cell"]["settings"]["experiment"]["max_runs"], 2)
        self.assertEqual(config["limits"]["max_parallel_cells"], 1)
        self.assertTrue(config["cell"]["settings"]["model"]["name"])
        self.assertEqual(config["verifier"]["reasoning_effort"], "medium")
        self.assertEqual(before, (PROJECT / "config.toml").read_bytes())

    def test_prepare_freezes_exact_authorized_tasks_and_detects_fixture_change(self):
        manifest = self.prepare()
        self.assertEqual(len(manifest["keys"]), 12)
        self.assertEqual({k for k in manifest["keys"] if k.startswith("baseline")},
                         {"baseline-" + c for c in evaluation.BASELINE_CASES})
        evaluation.verify_frozen(self.root)
        with self.assertRaisesRegex(ValueError, "already frozen"):
            self.prepare()
        (self.root / "fixtures/cases.json").write_text("[]", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "fixtures changed"):
            evaluation.verify_frozen(self.root)

    def test_actual_worker_prepares_baseline_without_candidate_scripts_or_rubrics(self):
        self.prepare()
        cases = {c["id"]: c for c in evaluation.read(self.root / "fixtures/cases.json")}
        controller = evaluation.make_controller(self.root, "baseline-S07", cases["S07"])
        cell = controller.root / "tasks/T0001/cell"
        self.assertTrue((cell / "AGENTS.md").is_file())
        self.assertTrue((cell / "skills/estimate-epsilon-rate/SKILL.md").is_file())
        self.assertFalse((cell / "skills/probe-mechanism").exists())
        self.assertFalse((cell / "runtime/experiment_state.json").exists())
        names = [p.name for p in cell.rglob("*") if p.is_file()]
        self.assertNotIn("rubrics.json", names)
        self.assertNotIn("cases.json", names)
        problem = (cell / "problem.md").read_text(encoding="utf-8")
        self.assertNotIn("S07", problem)
        self.assertNotIn("Invalid candidate", problem)
        before = evaluation.inventory(cell / "skills")
        evaluation.make_controller(self.root, "baseline-S07", cases["S07"])
        self.assertEqual(before, evaluation.inventory(cell / "skills"))

    def test_grade_requires_structured_actual_frozen_evidence(self):
        rubric = {"criteria": [{"id": "C1", "expected": "Read data"}]}
        grade = {"finding": "Finite observation", "criteria": [{"id": "C1", "verdict": "pass",
            "reason": "Saved measurement supports the finding", "evidence_paths": ["data.json"]}],
            "fatal_errors": [], "case_grade": "pass"}
        review = {"summary": json.dumps(grade), "verdict": "pass", "completion_status": "completed"}
        self.assertEqual(evaluation.parse_grade(review, rubric, {"data.json"})["case_grade"], "pass")
        self.assertEqual(evaluation.parse_grade(review, rubric, set())["status"], "ungraded")
        review["summary"] = "Looks good; keywords: parameter drift, censored."
        self.assertEqual(evaluation.parse_grade(review, rubric, {"data.json"})["status"], "ungraded")

    def test_absence_of_leak_indicator_is_not_clean_holdout(self):
        cell = self.root / "cell"
        (cell / "runtime").mkdir(parents=True)
        log = cell / "runtime/experiment-0001.txt.events.jsonl"
        log.write_text(json.dumps({"type": "item.completed", "item": {"type": "command_execution",
            "command": "read data.json", "status": "completed"}}) + "\n", encoding="utf-8")
        result = evaluation.trace_summary(cell)
        self.assertEqual(result["status"], "unknown")
        self.assertEqual(len(result["tool_events"]), 1)
        self.assertEqual(result["suspicious_events"], [])

    def test_adoption_server_removes_launching_tools_only(self):
        server = Mock()
        with patch("colombo.brain.mcp_server.create_server", return_value=server) as create:
            returned = evaluation.adoption_server(self.root, "C00002")
        create.assert_called_once_with(self.root, "brain", "process_results", "C00002")
        self.assertIs(returned, server)
        self.assertEqual([c.args[0] for c in server.remove_tool.call_args_list], ["audit", "job_status", "lookup"])

    def test_uncommitted_original_call_cannot_be_relaunched(self):
        controller = Mock()
        controller.store.get_meta.return_value = {"role": "verifier", "stage": "verify-progress", "call_id": "C00001"}
        controller.calls.backend.reconcile_call.return_value = {"state": "failed"}
        with self.assertRaisesRegex(RuntimeError, "cap forbids replacement"):
            evaluation.recover_committed_call(controller, "verifier", "verify-progress")
        controller._call.assert_not_called()

    def test_summary_never_treats_unstarted_tasks_as_success_and_audit_binds_logs(self):
        self.prepare()
        with patch.object(evaluation.EvaluationBackend, "invoke", side_effect=AssertionError("No model allowed")):
            result = evaluation.summarize(self.root)
        self.assertEqual(result["totals"]["research_tasks_attempted"], 0)
        self.assertTrue(all(not row["held_out_success"] for row in result["cases"]))
        key = "candidate-S03"
        log = self.root / "runs" / key / "tasks/T0001/cell/runtime/experiment-0001.txt.events.jsonl"
        log.parent.mkdir(parents=True)
        log.write_text("{}\n", encoding="utf-8")
        required = evaluation.read_audit_status(self.root, key)["required_logs"]
        evaluation.save(self.root / "read-audits" / (key + ".json"), {"status": "clean", "reviewer": "offline test",
            "reason": "Test only", "inspected_logs": required})
        self.assertEqual(evaluation.read_audit_status(self.root, key)["status"], "clean")
        log.write_text("{}\n{}\n", encoding="utf-8")
        self.assertEqual(evaluation.read_audit_status(self.root, key)["status"], "unknown")

    def test_real_store_review_and_update_entrypoints_are_idempotent_with_fake_models(self):
        from colombo.brain.task_execution import TaskExecution
        from colombo.brain.model_calls import CodexBackend
        self.prepare()
        calls = []

        def research(execution, job):
            store = execution.store
            task = store.get_task(job["task_id"])
            relative = "tasks/T0001/results/A0001/report.md"
            data = b"Offline fixture observation; no real model or hosted execution."
            destination = store.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            result = {"task_id": "T0001", "attempt_id": "A0001", "execution_status": "finished",
                "evidence_kind": "empirical", "accepted": False, "review_status": "pending",
                "assignment_ref": task["assignment_ref"], "package_ref": task["package_ref"],
                "empirical_report": {"outcome": "inconclusive"},
                "artifacts": [{"path": relative, "size": len(data)}]}
            ref = store.write_record("result", result)
            task.update(latest_result_ref=ref, state="returned", finished_attempt="A0001", result_refs=[ref])
            store.save_task(task)
            return ref

        def model(backend, role, stage, run_root, call_id, prompt, context):
            from colombo.brain.research_store import Store
            store = Store(run_root)
            calls.append(stage)
            if stage == "verify-progress":
                package = store.read_record(context["review_package_ref"])
                rid = package["result_ref"]
                path = store.read_record(rid)["artifacts"][0]["path"]
                grade = {"finding": "Offline fake review for control-flow testing only",
                    "criteria": [{"id": f"C{i}", "verdict": "pass", "reason": "Fixture",
                                  "evidence_paths": [path]} for i in (1, 2, 3)],
                    "fatal_errors": [], "case_grade": "pass"}
                return {"review_kind": "result", "result_ref": rid, "verdict": "pass",
                    "summary": json.dumps(grade), "findings": [], "checked_refs": package["required_checked_refs"],
                    "confirmed_claims": [{"id": "sample", "kind": "empirical", "statement": "Fixture observation",
                        "scope": "One fixture", "assumptions": [], "expression": "", "evidence_paths": [path]}],
                    "completion_status": "completed", "repair_kind": "none"}
            rid = context["result_refs"][0]["id"]
            return {"summary": "Fixture empirical adoption", "result_refs": [rid],
                "update": {"admissions": [{"result_ref": rid, "verdict": "accepted", "goal_ids": ["G0"],
                    "proof_step_ids": [], "reason": "Fixture review passed", "completion_status": "completed",
                    "completed_parts": ["Empirical responsibility"], "remaining": []}],
                    "progress": {"overall": "Empirical task complete; mathematics remains open.", "status": "in_progress",
                        "items": [{"goal_id": "G0", "description": "Mathematical research", "status": "partial",
                                   "result_refs": [rid], "remaining": ["Proof"]}],
                        "bracket": {"bounds": [], "regimes": []}, "remaining": ["Proof"]}},
                "prunes": [], "next_action": "continue", "rationale": "No new dispatch"}

        with patch.object(TaskExecution, "run_job", research), patch.object(CodexBackend, "invoke", model):
            result = evaluation.run_one(self.root, "candidate-S01")
            again = evaluation.run_one(self.root, "candidate-S01")
        self.assertEqual(calls, ["verify-progress", "process_results"])
        self.assertEqual(result["state"], "finished")
        self.assertEqual(result["grade"], "pass")
        self.assertTrue(result["mathematical_goal_preserved"])
        self.assertFalse(result["held_out_success"])
        self.assertEqual(result, again)


if __name__ == "__main__":
    unittest.main()
