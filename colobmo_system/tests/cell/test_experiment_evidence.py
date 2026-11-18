"""Computational evidence remains reproducible and separate from mathematical authority."""
from __future__ import annotations

from colombo.shared.tool_jobs import experiment_context
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.cell.verifier.local_audit import audit
from colombo.shared.experiment_artifacts import read_artifacts
from colombo.shared.experiment_artifacts import manifest_for
from colombo.cell.record_store import Store
from colombo.cell.record_store import StoreError
from colombo.cell.record_store import AuditRequired
from colombo.cell.subcell_dispatch import Tasks
from colombo.cell.verifier.proof_review import _capture
from colombo.cell.verifier.proof_review import _prepare_workspace
from colombo.cell.verifier.proof_review import _request
from colombo.cell.settings import get_settings
from colombo.cell.settings import run_fields
from test_confirmed_trust import confirmed_packet
from test_experiment_runtime import Remote
import colombo.shared.experiment_execution as execution


def ref(record, **extra):
    return {**{key: record[key] for key in ("kind", "id", "revision")}, **extra}


PASS = {"verdict": "pass", "summary": "Checked the exact finite computation.", "findings": [], "properties": []}


class ExperimentEvidenceTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for name in tuple(os.environ):
            if name.startswith("CELL_"):
                os.environ.pop(name)
        temporary = tempfile.TemporaryDirectory(prefix=".experiment-evidence-", dir=Path(__file__).resolve().parents[2])
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.settings = get_settings()
        self.write_json(self.root / "run.json", {"settings": self.settings, **run_fields(self.settings)})
        self.store = Store(self.root / "memory")
        self.target = self.store.archive("claims", {"statement": "n(n+1) is even for every integer n."})
        (self.root / "problem.md").write_text("Prove the parity assertion.", encoding="utf-8")

    @staticmethod
    def write_json(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def computation(self, store=None, identifier="exp-evidence", *, status="completed", dependencies=None,
                    target=None, files=None):
        store = store or self.store
        root = store.memory_dir.parent
        files = files or {f"experiments/{identifier}/code.py": b"assert all(n*(n+1)%2 == 0 for n in range(8))\n",
                          f"experiments/{identifier}/output.json": b'{"tested":8,"exceptions":[]}'}
        for name, data in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        payload = {"question": "Check the first eight integers", "target_ref": ref(target or self.target),
                   "parameters": {"n": 8}, "code_file": next(iter(files)),
                   "input_files": [], "execution": {"status": status, "backend": "test_fixture",
                   "model": "fake", "started_at": 100, "deadline_at": 200,
                   "artifact_limits": {key: self.settings["experiment"][key] for key in
                       ("artifact_max_bytes", "max_total_artifact_bytes", "max_files")}},
                   "artifacts": manifest_for(files)}
        if dependencies:
            payload["dependencies"] = dependencies
        return store.write_experiment_result(identifier, payload)

    def argument(self, payload=None):
        candidate = self.store.archive("arguments", payload or {"proof": "n(n+1) is even", "status": "candidate"})
        review = self.store.write_review({"target": ref(candidate), **PASS})
        return self.store.archive("arguments", {**candidate["payload"], "status": "proved", "audit_id": review["id"]},
                                  record_id=candidate["id"], expected_revision=candidate["revision"])

    def test_singular_collection_service_facts_and_interpretation_revisions(self):
        result = self.computation(status="running")
        self.assertTrue((self.root / "memory" / "experiment_result.json").is_file())
        with self.assertRaises(StoreError):
            self.store.archive("experiment_results", {})
        with self.assertRaises(StoreError):
            self.store.archive("experiment_result", result["payload"])
        with self.assertRaises(StoreError):
            self.store.archive("experiment_result", result["payload"], record_id="forged")
        updated = self.store.archive("experiment_result", {"observations": ["No exception in n=0..7"],
                    "limitations": "Finite exploration only", "derived_refs": []},
                    record_id=result["id"], expected_revision=1)
        for changed in ({"execution": {"status": "completed"}}, {"code_file": "forged"},
                        {"artifacts": []}, {"status": "proved"}, {"unknown": None}):
            with self.subTest(changed=changed), self.assertRaises(StoreError):
                self.store.archive("experiment_result", changed, record_id=result["id"], expected_revision=2)
        payload = copy.deepcopy(result["payload"])
        payload["execution"]["status"] = "completed"
        final = self.store.write_experiment_result(result["id"], payload)
        self.assertEqual(final["payload"]["observations"], updated["payload"]["observations"])
        self.assertEqual(final["current_trust"]["state"], "computational_evidence")
        self.assertNotIn("dependencies", final["payload"])
        self.assertEqual(self.store.write_experiment_result(result["id"], payload)["revision"], final["revision"])
        self.assertEqual(self.store.get("experiment_result", result["id"], 1)["payload"], result["payload"])
        payload["question"] = "A different question is a new run"
        with self.assertRaises(StoreError):
            self.store.write_experiment_result(result["id"], payload)

    def test_missing_failed_or_tampered_computation_never_supports_proof(self):
        result = self.computation(status="failed")
        candidate = self.store.archive("arguments", {"proof": "All eight checked values are even.",
                                                      "dependencies": [ref(result)]})
        reviewed = audit(self.root, "arguments", candidate["id"], 1, reviewer=lambda *_: copy.deepcopy(PASS))
        self.assertEqual(reviewed["review"]["payload"]["verdict"], "uncertain")
        good = self.computation(identifier="exp-good")
        candidate = self.store.archive("arguments", {"proof": "Finite check", "dependencies": [ref(good)]})
        path = self.root / good["payload"]["artifacts"][0]["path"]
        path.write_bytes(b"tampered")
        self.assertEqual(self.store.get("experiment_result", good["id"])["current_trust"]["state"], "dependency_blocked")
        self.assertEqual(self.store.get("arguments", candidate["id"])["current_trust"]["state"], "dependency_blocked")
        with self.assertRaises(StoreError):
            self.store.evidence_bundle([ref(candidate)])
        with self.assertRaises(StoreError):
            self.store.archive("experiment_result", {"observations": "Hide tampering"}, record_id=good["id"], expected_revision=1)

    def test_audit_materializes_selected_files_and_rechecks_after_review(self):
        result = self.computation()
        candidate = self.store.archive("arguments", {"proof": "Exact enumeration of a finite domain", "dependencies": [ref(result)]})
        calls = []
        def reviewer(prompt, work):
            context = json.loads((work / "input.json").read_text(encoding="utf-8"))
            self.assertEqual(context["experiment_artifacts"], result["payload"]["artifacts"])
            self.assertTrue(any(row["kind"] == "experiment_result" for row in context["dependencies"]))
            for item in context["experiment_artifacts"]:
                self.assertEqual((work / item["path"]).read_bytes(), (self.root / item["path"]).read_bytes())
            calls.append(work)
            return copy.deepcopy(PASS)
        response = audit(self.root, "arguments", candidate["id"], 1, reviewer=reviewer)
        self.assertEqual(response["record"]["payload"]["status"], "proved")
        self.assertEqual(response["review"]["payload"]["experiment_artifacts"], result["payload"]["artifacts"])
        other = self.store.archive("arguments", {"proof": "Second finite enumeration", "dependencies": [ref(result)]})
        def vandal(prompt, work):
            (work / result["payload"]["artifacts"][0]["path"]).write_bytes(b"changed after read")
            return copy.deepcopy(PASS)
        rejected = audit(self.root, "arguments", other["id"], 1, reviewer=vandal)
        self.assertEqual(rejected["review"]["payload"]["verdict"], "service_error")
        self.assertNotEqual(rejected["record"]["payload"].get("status"), "proved")

    def test_verifier_freezes_recursive_experiment_evidence(self):
        result = self.computation()
        candidate = self.store.archive("arguments", {"proof": "finite claim", "dependencies": [ref(result)]})
        outer = self.store.archive("arguments", {"proof": "uses finite claim", "dependencies": [ref(candidate)]})
        (self.root / "draft.md").write_text("Consecutive integers have opposite parity.", encoding="utf-8")
        run = json.loads((self.root / "run.json").read_text())
        self.write_json(self.root / "run.json", run)
        submission = {"outcome": "proved", "record_refs": [ref(outer, position="finite check")]}
        captured = _capture(self.root, submission)
        for item in result["payload"]["artifacts"]:
            self.assertIn(item["path"], captured["manifest"]["files"])
        records = json.loads(captured["files"]["cell_record_evidence.json"])
        self.assertEqual({row["id"] for row in records}, {outer["id"], candidate["id"], result["id"]})
        work = self.root / "frozen"
        _prepare_workspace(work, captured, _request("fixture-review", captured))
        self.assertEqual((work / "input" / result["payload"]["artifacts"][0]["path"]).read_bytes(),
                         captured["files"][result["payload"]["artifacts"][0]["path"]])
        (self.root / result["payload"]["artifacts"][0]["path"]).write_bytes(b"after capture")
        with self.assertRaises(StoreError):
            _capture(self.root, submission)

    def test_only_explicit_dependencies_are_expanded_and_limits_are_per_run(self):
        first = self.computation(identifier="exp-first", files={"experiments/exp-first/output.json": b"1"})
        second = self.computation(identifier="exp-second", files={"experiments/exp-second/output.json": b"2"})
        for record in (first, second):
            payload = copy.deepcopy(record["payload"])
            # New fixture records each have an immutable one-file allowance.
            payload["execution"]["artifact_limits"]["max_files"] = 1
            self.store.write_experiment_result(record["id"] + "-pinned", payload)
        records = [self.store.get("experiment_result", r["id"] + "-pinned") for r in (first, second)]
        bundle = self.store.evidence_bundle([ref(r) for r in records])
        self.assertEqual(len(bundle["files"]), 2)
        self.assertNotIn(self.target["id"], {r["id"] for r in bundle["records"]})
        self.store.settings["experiment"]["artifact_max_bytes"] = 1
        larger = self.store.get("experiment_result", first["id"])
        self.assertEqual(larger["current_trust"]["state"], "computational_evidence")

    def test_artifact_paths_and_file_budgets(self):
        for name in ("../outside", "experiments/../outside", "experiments/./code.py", "/experiments/code.py",
                     "C:/outside", "AGENTS.md", "experiments\\code.py"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                read_artifacts(self.root, [{"path": name, "size": 0}])
        result = self.computation(files={"experiments/exp-image/chart.png": b"\x89PNG\x00binary"})
        bundle = self.store.evidence_bundle([ref(result)])
        self.assertEqual(next(iter(bundle["files"].values())), b"\x89PNG\x00binary")
        with self.assertRaises(ValueError):
            read_artifacts(self.root, result["payload"]["artifacts"] * 2)

    def test_parent_grants_only_explicit_files_and_collect_imports_portable_candidates(self):
        parent_result = self.computation(identifier="exp-parent")
        self.computation(identifier="exp-hidden")
        tasks = Tasks(self.root)
        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
            launch.return_value.pid = 12345
            task = tasks.spawn_task(ref(self.target), "Investigate this finite claim", context_refs=[ref(parent_result)])
        child_root = Path(task["workspace"])
        self.assertFalse((child_root / "experiments" / "exp-hidden").exists())
        child_store = Store(child_root / "memory")
        self.assertTrue(child_store.get("experiment_result", parent_result["id"])["read_only"])
        child_target = child_store.archive("claims", {"statement": "A child-local target"})
        child_result = self.computation(child_store, identifier="exp-child", target=child_target,
                       files={"experiments/exp-child/code.py": b"print(2+2)",
                              "experiments/exp-child/chart.png": b"\x89PNG\x00"})
        collected = tasks.collect_task(task["task_id"], record_ref=ref(child_result))
        imported_ref = collected["records"][0]["imported_record_ref"]
        imported = self.store.get(imported_ref["kind"], imported_ref["id"], imported_ref["revision"])
        self.assertEqual(imported["payload"]["origin"]["record_ref"], ref(child_result))
        self.assertNotEqual(imported["payload"]["target_ref"]["id"], child_target["id"])
        for item in imported["payload"]["artifacts"]:
            self.assertTrue(item["path"].startswith(f"experiments/imports/{task['task_id']}/"))
            self.assertTrue((self.root / item["path"]).is_file())
        # Recovery is independent of the child files once collection completes.
        for item in child_result["payload"]["artifacts"]:
            (child_root / item["path"]).unlink()
        self.assertTrue(self.store.evidence_bundle([imported_ref])["files"])
        again = tasks.collect_task(task["task_id"], record_ref=ref(child_result))
        self.assertEqual(again["records"][0]["imported_record_ref"], imported_ref)

    def test_withdrawn_premise_invalidates_interpretation_without_rewriting_execution(self):
        premise = self.argument()
        result = self.computation(dependencies=[ref(premise)])
        original = copy.deepcopy(result["payload"])
        downstream = self.argument({"proof": "Conditional finite consequence", "dependencies": [ref(result)]})
        self.store.apply_confirmed_review(**confirmed_packet(self.root, [premise]))
        current = self.store.get("experiment_result", result["id"])
        self.assertEqual(current["payload"], original)
        self.assertEqual(current["current_trust"]["state"], "dependency_blocked")
        self.assertEqual(self.store.get("arguments", downstream["id"])["current_trust"]["state"], "dependency_blocked")

    def test_actual_grant_then_child_runtime_ignores_inherited_run_and_reuses_request_id(self):
        self.settings["experiment"]["max_runs"] = 1
        self.write_json(self.root / "run.json", {"settings": self.settings, **run_fields(self.settings)})
        parent_remote = Remote(self.root)
        arguments = {"question": "Inspect a finite residual", "target_ref": ref(self.target),
                     "code": "print(0)", "request_id": "same-request-in-each-task"}
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-only-private-key"}), \
                patch.object(execution, "_Client", side_effect=parent_remote.factory):
            parent_receipt = execution.run_experiment(self.root, context=experiment_context(self.root), **arguments)
        self.assertEqual(parent_receipt["status"], "completed")
        parent_record = self.store.get("experiment_result", parent_receipt["experiment_id"])
        tasks = Tasks(self.root)
        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
            launch.return_value.pid = 12345
            task = tasks.spawn_task(ref(self.target), "Continue from this experiment", context_refs=[ref(parent_record)])
        child_root = Path(task["workspace"])
        frozen = {item["path"]: (child_root / item["path"]).read_bytes() for item in parent_record["payload"]["artifacts"]}
        self.assertTrue(any(path.endswith("plan.json") for path in frozen))
        self.assertFalse((child_root / "experiments" / parent_receipt["experiment_id"] / "state.json").exists())
        child_remote = Remote(child_root)
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-only-private-key"}), \
                patch.object(execution, "_Client", side_effect=child_remote.factory):
            child_receipt = execution.run_experiment(child_root, context=experiment_context(child_root), **arguments)
            with self.assertRaises(execution.ExperimentError):
                execution.resume_experiment(child_root, parent_receipt["experiment_id"], context=experiment_context(child_root))
        self.assertEqual(child_receipt["status"], "completed")
        self.assertNotEqual(child_receipt["experiment_id"], parent_receipt["experiment_id"])
        self.assertEqual(sum(method == "POST" and path == "/responses" for method, path, _ in child_remote.calls), 1)
        for name, data in frozen.items():
            self.assertEqual((child_root / name).read_bytes(), data)


if __name__ == "__main__":
    unittest.main()
