"""Unlimited tool research and legacy unmanaged deadline compatibility; no API calls."""
from __future__ import annotations

from contextlib import ExitStack
from contextlib import contextmanager
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

import colombo.cell.verifier.challenge as challenge
import colombo.shared.experiment_execution as experiment
from colombo.cell.record_store import Store
from colombo.cell.settings import get_settings
import test_argument_challenges as challenge_fixtures
import test_experiment_runtime as experiment_fixtures


class UnlimitedConsumerTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        os.environ["CELL_PROCESS_ID"] = "test-parent"
        temporary = tempfile.TemporaryDirectory(prefix=".unlimited-consumers-", dir=Path(__file__).resolve().parents[2])
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.settings = get_settings()

    @contextmanager
    def hosted(self, parent):
        config = self.settings
        config["experiment"].update(timeout_seconds=10, download_reserve_seconds=2)
        clock = experiment_fixtures.Clock()
        remote = experiment_fixtures.Remote(self.root)
        memory = experiment_fixtures.Memory()
        with ExitStack() as stack:
            stack.enter_context(patch.dict(os.environ, {"OPENAI_API_KEY": "test-only-private-key"}))
            stack.enter_context(patch.object(experiment, "_Client", side_effect=remote.factory))
            stack.enter_context(patch("colombo.cell.recovery.budget_status", return_value=parent))
            stack.enter_context(patch.object(experiment.time, "time", clock.time))
            # Advance wall and monotonic time together when fake polling sleeps.
            stack.enter_context(patch.object(experiment.time, "monotonic", clock.time))
            stack.enter_context(patch.object(experiment.time, "sleep", clock.sleep))
            self.experiment_context = experiment_fixtures.execution_context(self.root, config, memory)
            yield remote, clock

    def run_experiment(self):
        return experiment.run_experiment(self.root, "Is this residual zero?",
            {"kind": "claims", "id": "claim-a", "revision": 1},
            "print(0)", "unlimited-parent-case", context=self.experiment_context)

    def experiment_state(self, result):
        return json.loads((self.root / result["state_file"]).read_text(encoding="utf-8"))["execution"]

    def test_unmanaged_legacy_experiment_keeps_finite_saved_deadlines(self):
        with self.hosted({"time_limit_enabled": False, "work_remaining_seconds": None,
                          "hard_deadline": None}) as (remote, clock):
            result = self.run_experiment()
            self.assertEqual(result["status"], "completed")
            execution = self.experiment_state(result)
            self.assertEqual(execution["deadline_at"], 1008)
            self.assertEqual(execution["total_deadline_at"], 1010)
            self.assertEqual(remote.deadline, 1010)

    def test_unmanaged_legacy_experiment_timeout_still_cancels_remote_work(self):
        with self.hosted({"time_limit_enabled": False, "work_remaining_seconds": None,
                          "hard_deadline": None}) as (remote, clock):
            remote.waiting = True
            result = self.run_experiment()
            self.assertEqual(result["status"], "timed_out")
            self.assertTrue(any(path.endswith("/cancel") for method, path, _ in remote.calls))
            self.assertLessEqual(clock.now, 1010)
            self.assertEqual(self.experiment_state(result)["deadline_at"], 1008)

    def test_finite_legacy_parent_still_caps_experiment(self):
        with self.hosted({"work_remaining_seconds": 5, "hard_deadline": 1007}):
            result = self.run_experiment()
            execution = self.experiment_state(result)
            self.assertEqual(execution["deadline_at"], 1003)
            self.assertEqual(execution["total_deadline_at"], 1005)

    def test_zero_or_expired_parent_prevents_remote_experiment_submission(self):
        for budget in ({"work_remaining_seconds": 0, "hard_deadline": None},
                       {"work_remaining_seconds": None, "hard_deadline": 999}):
            with self.subTest(budget=budget), self.hosted(budget) as (remote, _):
                with self.assertRaisesRegex(experiment.ExperimentError, "Insufficient parent work budget"):
                    self.run_experiment()
                self.assertEqual(remote.calls, [])
                self.assertEqual(list((self.root / "experiments").glob("exp-*/plan.json")), [])

    def certified_argument(self):
        (self.root / "run.json").write_text(json.dumps({"settings": self.settings}), encoding="utf-8")
        store = Store(self.root / "memory")
        candidate = store.archive("arguments", {"statement": "For every real x the conclusion follows",
            "proof": "Divide both sides by x.", "status": "candidate"})
        review = store.write_review({"target": challenge_fixtures.ref(candidate), "verdict": "pass", "properties": []})
        target = store.archive("arguments", dict(candidate["payload"], status="proved", audit_id=review["id"]),
                               record_id=candidate["id"], expected_revision=candidate["revision"])
        return store, target

    def test_unlimited_parent_allows_both_local_review_stages_without_local_caps(self):
        store, target = self.certified_argument()
        calls = []

        def review(prompt, work, output, **kwargs):
            request = json.loads((work / "request.json").read_text(encoding="utf-8"))
            calls.append((request["stage"], kwargs))
            report = challenge_fixtures.first(work) if request["stage"] == "proof" else challenge_fixtures.confirmation(work)
            return {"returncode": 0, "text": json.dumps(report)}

        with patch.object(challenge, "budget_status", return_value={"time_limit_enabled": False,
                "work_remaining_seconds": None, "hard_deadline": None}), patch.object(challenge, "run_agent", side_effect=review):
            result = challenge.challenge_argument(self.root, challenge_fixtures.ref(target), "The domain includes zero")
        self.assertEqual(result["status"], "withdrawn")
        self.assertEqual([stage for stage, _ in calls], ["proof", "check"])
        for stage, kwargs in calls:
            self.assertEqual(kwargs["timeout"], "unlimited")
            self.assertIsNone(kwargs["_absolute_deadline"])
        self.assertEqual(store.get("arguments", target["id"], target["revision"])["current_trust"]["state"], "withdrawn")

    def test_zero_parent_review_budget_leaves_suspension_without_consuming_attempt(self):
        store, target = self.certified_argument()
        with patch.object(challenge, "budget_status", return_value={"work_remaining_seconds": 0,
                "hard_deadline": None}), patch.object(challenge, "run_agent") as launch:
            result = challenge.challenge_argument(self.root, challenge_fixtures.ref(target), "The domain includes zero")
        launch.assert_not_called()
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["primary_launches"], 0)
        self.assertEqual(result["stopping_reason"], "parent_work_budget")
        self.assertEqual(store.get("arguments", target["id"], target["revision"])["current_trust"]["state"], "suspended")


if __name__ == "__main__":
    unittest.main()
