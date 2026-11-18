"""Unlimited long-process budgets keep typed, isolated settings and finite safeguards."""
from __future__ import annotations

import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from colombo.cell.settings import configure
from colombo.cell.record_store import Store
from colombo.cell.subcell_worker import run_subcell
from colombo.cell.subcell_dispatch import Tasks
import colombo.cell.verifier.proof_review as review
import colombo.cell.controller as run
import colombo.cell.settings as settings
from review_fixtures import confirmation_result
from review_fixtures import report_result


ROOT = Path(__file__).resolve().parents[2]
LONG_BUDGETS = (
    "prover_timeout_seconds", "subcell_timeout_seconds",
    "verifier_timeout_seconds", "report_check_timeout_seconds",
)


class UnlimitedSettingsTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        temporary = tempfile.TemporaryDirectory(prefix=".unlimited-settings-", dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.base = settings.get_settings()
        self.defaults = settings.CONFIG_PATH.read_bytes()
        self.problem = self.root / "question.md"
        self.problem.write_text("Prove that 2 is even.", encoding="utf-8")

    def task(self, name="task", *, timeout=None):
        work = self.root / name
        run.initialize(self.problem, work, search_enabled=False)
        return work

    @staticmethod
    def read(path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_four_long_process_budgets_accept_only_positive_integer_or_exact_unlimited(self):
        for key in LONG_BUDGETS:
            for value in (1, 300, "unlimited"):
                with self.subTest(key=key, value=value):
                    merged = settings.merge_settings(self.base, {"agents": {key: value}})
                    self.assertEqual(merged["agents"][key], value)
                    self.assertEqual(settings.validate_settings(merged), merged)
            for value in (True, False, 0, -1, 1.5, "300", "0", "Unlimited", "none", "", None,
                          float("inf"), float("nan")):
                with self.subTest(key=key, invalid=value), self.assertRaises(ValueError):
                    settings.merge_settings(self.base, {"agents": {key: value}})
        self.assertEqual(settings.CONFIG_PATH.read_bytes(), self.defaults)

    def test_unlimited_does_not_disable_short_operations_or_count_limits(self):
        for section, key in (
            ("agents", "prover_max_rounds"),
            ("agents", "verifier_max_rounds"), ("agents", "report_check_max_attempts"),
            ("challenge", "max_rounds"),
            ("experiment", "max_runs"), ("handoff", "reserve_seconds"),
            ("network", "connect_timeout_seconds"), ("network", "read_timeout_seconds"),
            ("runtime", "mcp_tool_timeout_seconds"), ("parallel", "max_subcells"),
        ):
            with self.subTest(section=section, key=key), self.assertRaises(ValueError):
                settings.merge_settings(self.base, {section: {key: "unlimited"}})

    def test_existing_integer_task_snapshot_and_aliases_are_unchanged(self):
        task = self.task()
        before = (task / "run.json").read_bytes()
        self.assertEqual(settings.migrate_settings(self.base), self.base)
        self.assertEqual(settings.get_settings(task), self.base)
        document = self.read(task / "run.json")
        self.assertEqual(document["prover_timeout"], self.base["agents"]["prover_timeout_seconds"])
        self.assertEqual(document["task_timeout"], self.base["agents"]["subcell_timeout_seconds"])
        self.assertEqual((task / "run.json").read_bytes(), before)

    def test_toml_option_is_pinned_for_new_task_without_rewriting_user_defaults(self):
        config = self.root / "defaults.toml"
        source=self.defaults.decode("utf-8-sig").replace('profile = "hard"','profile = "standard"',1)
        config.write_text(source,encoding="utf-8")
        with patch.object(settings,"CONFIG_PATH",config):
            task=self.task()
            self.assertNotIn("budget", settings.load_policy())
            self.assertEqual(settings.get_settings(task)["agents"]["prover_max_rounds"],3)
            config.write_text(source.replace('prover_max_rounds = 3','prover_max_rounds = 7'),encoding="utf-8")
            self.assertEqual(settings.get_settings()["agents"]["prover_max_rounds"],7)
            self.assertEqual(settings.get_settings(task)["agents"]["prover_max_rounds"],3)
            self.assertEqual(settings.get_settings(task)["agents"]["prover_timeout_seconds"],"unlimited")
        self.assertEqual(settings.CONFIG_PATH.read_bytes(),self.defaults)

    def test_cli_unlimited_and_numeric_budget_overrides_are_rejected(self):
        task=self.task()
        before=(task/"run.json").read_bytes()
        for value in ("unlimited","41"):
            with patch.object(run,"solve") as solver, patch.object(sys,"argv",["run.py","--run-dir",str(task),"--resume","--timeout",value]), patch("sys.stderr",new=io.StringIO()), self.assertRaises(SystemExit):
                run.main()
            solver.assert_not_called()
            self.assertEqual((task/"run.json").read_bytes(),before)

    def test_cli_rejects_invalid_timeout_before_creating_task(self):
        task = self.root / "invalid-cli"
        for value in ("0", "-1", "1.5", "Unlimited", "none"):
            with self.subTest(value=value), patch.object(run, "solve") as solve:
                with patch.object(sys, "argv", ["run.py", str(self.problem), "--run-dir", str(task), "--timeout", value]), \
                        patch("sys.stderr", new=io.StringIO()), self.assertRaises(SystemExit) as raised:
                    run.main()
                self.assertEqual(raised.exception.code, 2)
                solve.assert_not_called()
                self.assertFalse(task.exists())

    def test_configure_cannot_change_task_budget_or_sibling(self):
        task,sibling=self.task(),self.task("sibling")
        before=(task/"run.json").read_bytes();sibling_before=(sibling/"run.json").read_bytes()
        with self.assertRaisesRegex(ValueError,"outer config"):
            configure(task,"prover",{"agents":{"prover_timeout_seconds":42}},reason="Rejected local budget change")
        self.assertEqual((task/"run.json").read_bytes(),before)
        self.assertEqual((sibling/"run.json").read_bytes(),sibling_before)
        self.assertEqual(settings.CONFIG_PATH.read_bytes(),self.defaults)

    def test_subcell_inherits_unlimited_or_explicit_finite_budget_and_runner_receives_it(self):
        task = self.task(timeout="unlimited")
        store, tasks = Store(task / "memory"), Tasks(task)
        target = store.archive("claims", {"statement": "Analyze a scoped auxiliary assertion."})
        reference = {key: target[key] for key in ("kind", "id", "revision")}
        calls = []

        def agent_runner(prompt, work, output, **kwargs):
            calls.append(kwargs)
            output.write_text("Saved a partial result.", encoding="utf-8")
            return {"text": "Saved a partial result."}

        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as process:
            process.return_value.pid = 12345
            inherited = tasks.spawn_task(reference, "Inspect one route")
            with self.assertRaisesRegex(ValueError, "outer config"):
                tasks.spawn_task(reference, "Forbidden budget override",
                                 settings_overrides={"agents": {"subcell_timeout_seconds": 73}})
            finite = tasks.spawn_task(reference, "Inspect another route")
        for created, expected in ((inherited, "unlimited"), (finite, "unlimited")):
            work = Path(created["workspace"])
            self.assertEqual(settings.get_settings(work)["agents"]["subcell_timeout_seconds"], expected)
            self.assertEqual(self.read(work / "run.json")["task_timeout"], expected)
            result = run_subcell(work.parent, agent_runner=agent_runner)
            self.assertEqual(result["status"], "completed")
            self.assertEqual(calls[-1]["timeout"], expected)
        self.assertEqual(settings.get_settings(task)["agents"]["subcell_timeout_seconds"], "unlimited")

    def test_unlimited_time_does_not_reset_or_bypass_prover_launch_cap(self):
        task = self.task(timeout="unlimited")
        launches = self.base["agents"]["prover_max_rounds"]
        state = task / "runtime" / "prover_state.json"
        state.parent.mkdir()
        state.write_text(json.dumps({"launches": launches}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "outer config"):
            run.configure_run(task, timeout="unlimited")
        with patch.object(run, "run_agent") as agent:
            self.assertEqual(run.solve(task), 2)
            agent.assert_not_called()
        self.assertEqual(self.read(state)["launches"], launches)

    def test_full_verification_passes_unlimited_to_both_independent_processes(self):
        task = self.task(timeout="unlimited")
        (task / "draft.md").write_text("The integer 2 equals 2 times the integer 1, so it is even.", encoding="utf-8")
        (task / "submission.json").write_text(json.dumps({"status": "ready", "outcome": "proved", "draft_file": "draft.md"}), encoding="utf-8")
        report = {"verdict": "pass", "summary": "The explicit integer witness proves evenness.",
                  "target_alignment": "Both the problem and draft concern the integer 2.",
                  "coverage": "The only necessary inference is the definition of evenness with witness 1.",
                  "checks": [{"id": 7, "subject": "Witness for evenness", "location": "draft.md",
                              "status": "pass", "reason": "1 is an integer and 2=2*1."}],
                  "findings": [], "sources": []}
        calls = []

        def reviewer(prompt, work, output, **kwargs):
            stage = self.read(work / "review_request.json")["stage"]
            calls.append((stage, kwargs["timeout"]))
            return confirmation_result(work) if stage == "report_check" else report_result(work, report)

        with patch("colombo.cell.model_calls.run_agent", side_effect=reviewer):
            self.assertEqual(review.review_submission(task)["status"], "accepted")
        self.assertEqual(calls, [("proof", "unlimited"), ("report_check", "unlimited")])
        self.assertTrue(review.manuscript_is_current(task))


if __name__ == "__main__":
    unittest.main()
