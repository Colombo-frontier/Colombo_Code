"""Explicit restart grants renew allowances without resetting historical use."""
from contextlib import ExitStack
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.cell.restart_budget import cumulative_usage, effective_limit, grant_restart
from colombo.cell import controller
from colombo.cell.diagnostics import read_stop_diagnostics, read_experiment_stop_diagnostics
from colombo.cell.verifier import proof_review
from colombo.shared.file_io import write_json, read_json


class RestartBudgetTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        temp = tempfile.TemporaryDirectory(prefix=".test-restart-", dir=Path(__file__).resolve().parents[2])
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "cell"
        self.root.mkdir()
        self.settings, _ = controller.load_defaults()
        self.settings["agents"].update(prover_max_rounds=3, verifier_max_rounds=4)
        self.settings["experiment"]["max_runs"] = 2
        self.scope = {"task_id": "T0007", "attempt_id": "A0007",
                      "assignment_ref": {"id": "assignment-fixed", "revision": 1},
                      "package_ref": {"id": "package-fixed", "revision": 1}}
        write_json(self.root / "runtime/prover_state.json", {"launches": 15})
        write_json(self.root / "reviews/index.json", {"protocol": proof_review.REVIEW_PROTOCOL,
                                                     "attempts": [], "primary_launches": 20})

    def grant(self, attempt=None):
        scope = {**self.scope, **({"attempt_id": attempt} if attempt else {})}
        return grant_restart(self.root, scope, self.settings)

    def test_resume_does_not_renew_and_restart_keeps_counters(self):
        before = cumulative_usage(self.root)
        self.assertEqual(effective_limit(self.root, "prover", 3), 3)
        self.assertEqual(effective_limit(self.root, "verifier", 4), 4)
        row = self.grant()
        self.assertEqual(row["baselines"], before)
        self.assertEqual(cumulative_usage(self.root), before)
        self.assertEqual(effective_limit(self.root, "prover", 3), 18)
        self.assertEqual(effective_limit(self.root, "verifier", 4), 24)

    def test_same_attempt_is_idempotent_and_older_cycle_cannot_regrant(self):
        first = self.grant()
        write_json(self.root / "runtime/prover_state.json", {"launches": 17})
        self.assertEqual(self.grant(), first)
        self.assertEqual(effective_limit(self.root, "prover", 3), 18)
        self.grant("A0008")
        self.assertEqual(effective_limit(self.root, "prover", 3), 20)
        with self.assertRaisesRegex(ValueError, "obsolete"):
            self.grant()
        with self.assertRaisesRegex(ValueError, "newer"):
            self.grant("A0006")
        self.assertEqual(len(read_json(self.root / "runtime/restart_budget.json")["cycles"]), 2)

    def test_fixed_scope_cannot_change(self):
        self.grant()
        for attempt in ["A0007", "A0008"]:
            changed = {**self.scope, "attempt_id": attempt, "package_ref": {"id": "different"}}
            with self.assertRaises(ValueError):
                grant_restart(self.root, changed, self.settings)

    def test_rejects_active_solver_and_pending_children(self):
        with controller._exclusive_run(self.root):
            with self.assertRaises(controller._RunBusy):
                self.grant()
        with patch.object(controller, "_active_children", return_value=True):
            with self.assertRaisesRegex(ValueError, "Subcells"):
                self.grant()
        self.assertFalse((self.root / "runtime/restart_budget.json").exists())

    def test_hosted_and_native_experiment_counters_get_separate_allowances(self):
        write_json(self.root / "runtime/experiment_state.json", {"launches": 12})
        for i in range(2):
            path = self.root / "experiments" / f"exp-{i}"
            write_json(path / "plan.json", {"request_id": str(i)})
            write_json(path / "state.json", {"execution": {"status": "completed"}})
        self.grant()
        self.assertEqual(effective_limit(self.root, "experiment_native", 3), 15)
        self.assertEqual(effective_limit(self.root, "experiment_hosted", 2), 4)
        self.assertEqual(cumulative_usage(self.root)["experiment_hosted"], 2)

    def test_unresolved_hosted_call_blocks_new_grant(self):
        path = self.root / "experiments/exp-unknown/state.json"
        for status in ["remote_unknown", "download_pending", "submitted"]:
            write_json(path, {"execution": {"status": status}})
            with self.assertRaisesRegex(ValueError, "unfinished hosted"):
                self.grant()
        self.assertFalse((self.root / "runtime/restart_budget.json").exists())

    def test_grants_do_not_propagate_to_existing_subcell_or_old_snapshot(self):
        self.grant()
        child = self.root / "tasks/child/workspace"
        child.mkdir(parents=True)
        self.assertEqual(effective_limit(child, "prover", 3), 3)
        historical = self.root.parent / "frozen-artifacts"
        historical.mkdir()
        self.assertEqual(effective_limit(historical, "prover", 3), 3)

    def test_prover_controller_starts_exact_fresh_allowance_then_resume_stays_exhausted(self):
        (self.root / "protocol.md").write_text("fixture", encoding="utf-8")
        self.grant()
        with ExitStack() as stack:
            stack.enter_context(patch.object(controller, "pin_task_settings"))
            stack.enter_context(patch.object(controller, "install_handoff_skill"))
            stack.enter_context(patch.object(controller, "manuscript_is_current", return_value=False))
            stack.enter_context(patch.object(controller, "has_pending_review", return_value=False))
            stack.enter_context(patch.object(controller, "_ready_submission", return_value=False))
            stack.enter_context(patch.object(controller, "get_settings", return_value=self.settings))
            stack.enter_context(patch.object(controller, "_review_to_boundary", return_value={"status": "pending"}))
            stack.enter_context(patch("colombo.shared.runtime_budget.inherited_deadline"))
            stack.enter_context(patch("sys.stdout", new=io.StringIO()))
            launch = stack.enter_context(patch.object(controller, "run_agent", return_value={}))
            self.assertEqual(controller._solve_locked(self.root), 2)
            self.assertEqual(launch.call_count, 3)
            self.assertEqual(read_json(self.root / "runtime/prover_state.json")["launches"], 18)
            self.assertEqual(controller._solve_locked(self.root), 2)
            self.assertEqual(launch.call_count, 3)

    def test_verifier_restarts_with_cumulative_history_intact(self):
        from test_runner_verification import CORRECT, PROBLEM, PROOF
        from review_fixtures import report_result, confirmation_result
        from colombo.cell.settings import run_fields
        (self.root / "problem.md").write_text(PROBLEM, encoding="utf-8")
        (self.root / "draft.md").write_text(PROOF, encoding="utf-8")
        write_json(self.root / "run.json", {"settings": self.settings, **run_fields(self.settings)})
        write_json(self.root / "submission.json", {"status": "ready", "outcome": "proved", "draft_file": "draft.md"})
        reviewer = lambda work: report_result(work, deepcopy(CORRECT))
        before = proof_review.review_submission(self.root, reviewer=reviewer, report_checker=confirmation_result)
        self.assertEqual(before["status"], "review_incomplete")
        self.grant()
        after = proof_review.review_submission(self.root, reviewer=reviewer, report_checker=confirmation_result)
        self.assertEqual(after["status"], "accepted")
        self.assertEqual(read_json(self.root / "reviews/index.json")["primary_launches"], 21)

    def test_diagnostics_reads_frozen_cycle_without_resetting_report_caps(self):
        from colombo.cell.settings import run_fields
        write_json(self.root / "run.json", {"settings": self.settings, **run_fields(self.settings)})
        self.grant()
        diag = read_stop_diagnostics(self.root, accepted=False, execution="incomplete", reason="fixture")
        self.assertEqual(diag["budget_snapshot"]["prover"], {"used": 15, "limit": 18, "remaining": 3})
        self.assertEqual(diag["budget_snapshot"]["verifier"], {"used": 20, "limit": 24, "remaining": 4})
        self.assertEqual(diag["budget_snapshot"]["report_check"]["limit"], self.settings["agents"]["report_check_max_attempts"])
        self.assertEqual(diag["budget_snapshot"]["restart_cycle"]["baselines"]["prover"], 15)

    def test_empirical_diagnostics_reports_native_cycle_and_remaining(self):
        from colombo.cell.settings import run_fields
        write_json(self.root / "run.json", {"settings": self.settings, **run_fields(self.settings)})
        write_json(self.root / "runtime/experiment_state.json", {"launches": 12})
        before = read_experiment_stop_diagnostics(self.root, execution="incomplete", reason="fixture")
        self.assertEqual(before["stop_info"]["stage"], "experiment_native")
        self.assertEqual(before["stop_info"]["kind"], "budget_exhausted")
        self.grant()
        after = read_experiment_stop_diagnostics(self.root, execution="incomplete", reason="fixture")
        self.assertEqual(after["stop_info"]["kind"], "incomplete")
        self.assertEqual(after["budget_snapshot"]["experiment_native"], {"used": 12, "limit": 15, "remaining": 3})
        self.assertEqual(after["budget_snapshot"]["restart_cycle"]["baselines"]["experiment_native"], 12)

    def test_duplicate_worker_solve_does_not_grant_again(self):
        from colombo.cell import worker
        task = self.root.parent
        write_json(task / "prepared.json", {**self.scope, "specialization": "general"})
        request = task / "attempts/A0007/request.json"
        write_json(request, {**self.scope, "task_dir": str(task), "project_root": str(task),
                             "config": {}, "restart": True, "resume": True})
        def solver(root):
            state = read_json(root / "runtime/prover_state.json")
            state["launches"] += 1
            write_json(root / "runtime/prover_state.json", state)
            return 2
        with patch.object(worker, "_verify_inputs"), patch.object(worker, "_cell_imports",
                return_value=(None, solver, Path, None, None, None)), \
                patch("colombo.cell.settings.get_settings", return_value=self.settings):
            self.assertEqual(worker.solve(request), 2)
            self.assertEqual(worker.solve(request), 2)
        cycles = read_json(self.root / "runtime/restart_budget.json")["cycles"]
        self.assertEqual(len(cycles), 1)
        self.assertEqual(cycles[0]["baselines"]["prover"], 15)
        self.assertEqual(effective_limit(self.root, "prover", 3), 18)
        self.assertEqual(cumulative_usage(self.root)["prover"], 17)

    def test_archive_includes_grant_and_native_diagnostics_exposes_hosted_blocker(self):
        from colombo.cell.attempt_archive import research_files
        from colombo.cell.settings import run_fields
        self.grant()
        self.assertIn("runtime/restart_budget.json", [p.relative_to(self.root).as_posix() for p in research_files(self.root)])
        write_json(self.root / "run.json", {"settings": self.settings, **run_fields(self.settings)})
        write_json(self.root / "runtime/experiment_state.json", {"launches": 1})
        write_json(self.root / "experiments/exp-unknown/state.json", {"execution": {"status": "remote_unknown"}})
        diag = read_experiment_stop_diagnostics(self.root, execution="incomplete", reason="fixture")
        self.assertEqual(diag["stop_info"]["stage"], "experiment_native")
        self.assertGreater(diag["budget_snapshot"]["experiment_native"]["remaining"], 0)
        self.assertIn("remote_unknown", diag["budget_snapshot"]["restart_blockers"][0])


if __name__ == "__main__":
    unittest.main()
