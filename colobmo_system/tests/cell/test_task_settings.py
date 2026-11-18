"""Exercise task and audit configuration propagation without model calls."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.cell.verifier.local_audit import audit
from colombo.cell.record_store import Store
from colombo.cell.subcell_dispatch import TaskError
from colombo.cell.subcell_dispatch import Tasks
from colombo.cell.subcell_worker import run_subcell
from colombo.cell.verifier.proof_review import review_submission
from colombo.cell.settings import get_settings
from colombo.cell.settings import run_fields
from review_fixtures import confirmation_result


class TaskSettingsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2])
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.settings = get_settings()
        self.settings["model"]["name"] = "configured-test-model"
        self.settings["agents"].update(subcell_timeout_seconds=31, audit_timeout_seconds=17,
                                       verifier_timeout_seconds=19, verifier_max_rounds=2)
        self.write_settings()
        self.store = Store(self.root / "memory")
        self.tasks = Tasks(self.root)
        self.target = self.store.archive("claims", {"statement": "The assigned target"})
        started = patch("colombo.cell.subcell_dispatch.subprocess.Popen")
        self.process = started.start()
        self.process.return_value.pid = 12345
        self.addCleanup(started.stop)

    def write_settings(self, **metadata):
        value = dict(run_fields(self.settings), settings=self.settings, task_depth=0, **metadata)
        (self.root / "run.json").write_text(json.dumps(value), encoding="utf-8")

    @staticmethod
    def ref(record):
        return {key: record[key] for key in ("kind", "id", "revision")}

    def test_child_inherits_full_settings_and_subcell_uses_them(self):
        task = self.tasks.spawn_task(self.ref(self.target), "Investigate this target")
        work = Path(task["workspace"])
        saved = json.loads((work / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["settings"], self.settings)
        self.assertEqual(saved["audit_timeout"], 17)
        self.assertEqual(saved["task_timeout"], 31)
        self.assertEqual(saved["task_depth"], 1)
        calls = []

        def runner(prompt, work_dir, output_file, **kwargs):
            calls.append(kwargs)
            output_file.write_text("Partial result", encoding="utf-8")
            return {"text": "Partial result"}

        result = run_subcell(work.parent, agent_runner=runner)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(calls[0]["settings"], self.settings)
        self.assertEqual(calls[0]["timeout"], 31)
        self.assertEqual(calls[0]["model"], "configured-test-model")

    def test_context_dependency_depth_changes_real_snapshot(self):
        leaf = self.store.archive("claims", {"statement": "Leaf"})
        middle = self.store.archive("claims", {"statement": "Middle", "dependencies": [self.ref(leaf)]})
        target = self.store.archive("claims", {"statement": "Root", "dependencies": [self.ref(middle)]})
        expected = ({target["id"]}, {target["id"], middle["id"]},
                    {target["id"], middle["id"], leaf["id"]})
        for depth, ids in enumerate(expected):
            with self.subTest(depth=depth):
                self.settings["parallel"]["context_dependency_depth"] = depth
                self.write_settings()
                task = self.tasks.spawn_task(self.ref(target), "Check dependencies")
                manifest = json.loads((Path(task["workspace"]) / "context/manifest.json").read_text(encoding="utf-8"))
                self.assertEqual({r["id"] for r in manifest["snapshot_refs"]}, ids)
                self.assertEqual(manifest["dependency_depth"], depth)

    def test_dependency_cycles_stop_without_duplicate_records(self):
        a = dict(self.target, id="cycle-a", payload={"dependencies": [{"kind": "claims", "id": "cycle-b", "revision": 1}]})
        b = dict(self.target, id="cycle-b", payload={"dependencies": [self.ref(a)]})
        records = {a["id"]: a, b["id"]: b}
        self.settings["parallel"]["context_dependency_depth"] = 20
        self.write_settings()
        with patch.object(self.tasks, "_resolve", side_effect=lambda ref: records[ref["id"]]) as resolve:
            task = self.tasks.spawn_task(self.ref(a), "Check cyclic dependency traversal")
        manifest = json.loads((Path(task["workspace"]) / "context/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual({r["id"] for r in manifest["snapshot_refs"]}, {"cycle-a", "cycle-b"})
        self.assertEqual(resolve.call_count, 3)

    def test_group_length_and_parallel_limits_follow_settings(self):
        self.settings["limits"]["group_id_max_chars"] = 3
        self.settings["parallel"].update(max_subcells=1, max_depth=1)
        self.write_settings()
        with self.assertRaisesRegex(TaskError, "3 characters"):
            self.tasks.spawn_task(self.ref(self.target), "Route", group_id="long")
        task = self.tasks.spawn_task(self.ref(self.target), "Route", group_id="one")
        with self.assertRaisesRegex(TaskError, "concurrent"):
            self.tasks.spawn_task(self.ref(self.target), "Other route")
        with self.assertRaisesRegex(TaskError, "depth"):
            Tasks(Path(task["workspace"])).spawn_task(self.ref(self.target), "Too deep")

    def test_child_small_audit_uses_inherited_timeout(self):
        task = self.tasks.spawn_task(self.ref(self.target), "Derive a lemma")
        work = Path(task["workspace"])
        argument = Store(work / "memory").archive("arguments", {"body": "A candidate derivation", "status": "candidate"})
        report = {"verdict": "pass", "summary": "The argument is valid.", "findings": [], "properties": []}
        with patch("colombo.cell.verifier.local_audit.run_agent", return_value={"text": json.dumps(report), "returncode": 0}) as agent:
            result = audit(work, "arguments", argument["id"], argument["revision"])
        self.assertEqual(result["review"]["payload"]["verdict"], "pass")
        self.assertEqual(agent.call_args.kwargs["timeout"], 17)
        self.assertEqual(agent.call_args.kwargs["settings"], self.settings)

    def test_verifier_uses_snapshot_timeout_and_total_review_budget(self):
        self.settings["agents"]["verifier_max_rounds"] = 1
        problem = b"Prove the assigned target."
        self.write_settings(storage_version=2)
        (self.root / "problem.md").write_bytes(problem)
        (self.root / "draft.md").write_text("An incomplete proof.", encoding="utf-8")
        (self.root / "submission.json").write_text(json.dumps({"status": "ready", "outcome": "proved",
                                                               "draft_file": "draft.md"}), encoding="utf-8")
        report = {"verdict": "revise", "summary": "The derivation is missing.",
                  "target_alignment": "The submitted draft does not establish the assigned target.",
                  "coverage": "The draft contains only the unsupported conclusion; its necessary derivation is the sole obligation.",
                  "checks": [{"id": 7, "subject": "Derivation of the target", "location": "draft.md",
                              "status": "fail", "reason": "The required deduction is absent."}],
                  "findings": [{"id": "missing-derivation", "check_id": 7, "kind": "gap",
                                "location": "draft.md", "explanation": "No derivation supports the conclusion.",
                                "repair": "Supply the missing derivation."}], "sources": []}

        def reviewer(prompt, work, output, **kwargs):
            (work / "review_report.json").write_text(json.dumps(report), encoding="utf-8")
            notes = {key: report[key] for key in ("checks", "findings", "sources")}
            (work / "review_notes.json").write_text(json.dumps(notes), encoding="utf-8")
            request = json.loads((work / "review_request.json").read_text(encoding="utf-8"))
            receipt = {"review_id": request["review_id"], "report_revision": request.get("report_revision", 1),
                       "verdict": report["verdict"]}
            return {"text": json.dumps(receipt), "returncode": 0}

        with patch("colombo.cell.model_calls.run_agent", side_effect=reviewer) as agent:
            self.assertEqual(review_submission(self.root, report_checker=confirmation_result)["status"], "needs_revision")
        self.assertEqual(agent.call_args.kwargs["timeout"], 19)
        self.assertEqual(agent.call_args.kwargs["settings"], self.settings)
        submission = json.loads((self.root / "submission.json").read_text(encoding="utf-8"))
        self.assertEqual(submission["status"], "needs_revision")
        state = json.loads((self.root / "reviews/index.json").read_text(encoding="utf-8"))
        self.assertEqual(len(state["attempts"]), 1)
        self.assertEqual(state["attempts"][0]["status"], "revise")
        # A confirmed criticism can be returned even at the primary launch
        # limit; a changed proof cannot silently reset that cumulative budget.
        (self.root / "draft.md").write_text("A different candidate proof.", encoding="utf-8")
        submission["status"] = "ready"
        (self.root / "submission.json").write_text(json.dumps(submission), encoding="utf-8")
        with patch("colombo.cell.model_calls.run_agent") as additional:
            self.assertEqual(review_submission(self.root)["status"], "review_incomplete")
            additional.assert_not_called()


if __name__ == "__main__":
    unittest.main()
