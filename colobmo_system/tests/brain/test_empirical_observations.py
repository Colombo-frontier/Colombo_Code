"""Composed Experiment dispatch, hosted evidence, outer review and archive.

The researcher callback and HTTP client are fakes. Preparation, Experiment
transport, local Store, empirical submission, worker export and outer contracts
are real. No Codex model or paid API request is made.
"""
from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

PROJECT = Path(__file__).resolve().parents[2]
for source in (PROJECT / "src",):
    if str(source) not in sys.path:
        sys.path.insert(0, str(source))

from colombo.brain.cell_dispatch import CellAdapter
from colombo.configuration import load_config
from colombo.brain.submission_validation import ContractError, validate_progress, validate_semantics
from colombo.shared.file_io import write_json
from colombo.brain.research_store import Store
from colombo.experiment_cell import controller as runtime
from colombo.shared import experiment_execution as experiment
from colombo.shared.tool_jobs import experiment_context
from colombo.cell.record_store import Store as CellStore
from colombo.cell import worker as cell_worker


def _remote_fixture():
    name = "empirical_transport_fixture"
    spec = importlib.util.spec_from_file_location(name, PROJECT / "tests/cell/test_experiment_runtime.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module.Remote


class EmpiricalObservationsIntegrationTests(unittest.TestCase):
    def test_completed_observations_traverse_dispatch_review_and_archive_without_proof_promotion(self):
        temporary = tempfile.TemporaryDirectory(prefix=".test-empirical-composed-", dir=PROJECT)
        self.addCleanup(temporary.cleanup)
        config = load_config()
        config["cell"]["settings"]["agents"]["prover_max_rounds"] = 1
        store = Store.create(Path(temporary.name) / "run", "Establish the near-optimal Oracle rate", [], config)
        task = store.root / "tasks/T0001"
        cell = task / "cell"
        package = task / "input/package"
        package.mkdir(parents=True)
        (task / "input/problem.md").write_text(
            "Run a finite calibration experiment, record its residual, and report limitations. "
            "The finite observation cannot prove a uniform Oracle Complexity Bound.", encoding="utf-8")
        (package / "README.md").write_text("Fixed calibration Setting; no additional Oracle information.", encoding="utf-8")
        write_json(package / "manifest.json", {"items": []})
        refs = {"assignment_ref": {"id": "assignment-calibration", "revision": 1},
                "package_ref": {"id": "package-calibration", "revision": 1}}
        adapter = CellAdapter(PROJECT, config)
        adapter.prepare(task, {"task_id": task.name, "research_mode": "oracle_complexity",
            "spec": {"specialization": "experiment"}}, package, **refs)
        request = {"task_dir": str(task), "project_root": str(PROJECT), "task_id": task.name,
            "attempt_id": "A0001", "config": adapter.config, **refs}
        request_path = task / "attempts/A0001/request.json"
        write_json(request_path, request)
        remote = _remote_fixture()(cell)
        observed = {}
        resource_path = "skills/estimate-epsilon-rate/scripts/gd_family_calibration.py"
        resource_bytes = (cell / resource_path).read_bytes()
        code = ("import json, runpy\nfrom pathlib import Path\n"
                "module = runpy.run_path(INPUT_FILES[" + repr(resource_path) + "])\n"
                "module['run']({'mode':'all','budgets':[0,1,4],'epsilons':[0.1],'max_steps':100}, OUTPUT_DIR)\n"
                "residual = 0\nPath(OUTPUT_DIR, 'answer.json').write_text(json.dumps({'residual': residual}))\n"
                "print('answer=0')\n")

        def researcher(*args, **kwargs):
            arguments = {"question": "What is the residual in this finite calibration sample?",
                "target_ref": runtime.target_ref(cell), "code": code, "request_id": "calibration-1",
                "parameters": {"sample": 0}, "input_files": [resource_path]}
            receipt = experiment.run_experiment(cell, context=experiment_context(cell), **arguments)
            self.assertEqual(receipt["status"], "completed")
            replay = experiment.run_experiment(cell, context=experiment_context(cell), **arguments)
            self.assertEqual(replay["record_ref"], receipt["record_ref"])
            state = json.loads((cell / receipt["state_file"]).read_text(encoding="utf-8"))
            data_path = state["downloads"]["answer.json"]["path"]
            measurement = json.loads((cell / data_path).read_text(encoding="utf-8"))
            record = CellStore(cell / "memory").get(**{
                "kind": receipt["record_ref"]["kind"], "id": receipt["record_ref"]["id"],
                "revision": receipt["record_ref"]["revision"]})
            self.assertEqual(record["payload"]["target_ref"], runtime.target_ref(cell))
            self.assertEqual(record["payload"]["execution"]["status"], "completed")
            artifact_paths = [item["path"] for item in state["artifacts"]]
            self.assertIn(data_path, artifact_paths)
            self.assertTrue(any(path.endswith("requested_code.py") for path in artifact_paths))
            plan = json.loads((cell / receipt["plan_file"]).read_text(encoding="utf-8"))
            saved_resource = plan["input_files"][0]["saved_path"]
            self.assertEqual((cell / saved_resource).read_bytes(), resource_bytes)
            report = {"summary": "The finite calibration sample has zero residual.",
                "actual_scope": "One fixed calibration sample", "method": "Evaluate and preserve the sampled residual",
                "uncertainty": "A finite calibration sample does not determine a uniform rate.",
                "measurements": [measurement], "candidate_rates": [],
                "limitations": ["No extrapolation to all instances or regimes"], "failures": [],
                "experiment_refs": [receipt["record_ref"]], "artifact_paths": artifact_paths,
                "outcome": "observations"}
            submission = runtime.submit_report(cell, report,
                "# Calibration report\n\nThe recorded sample residual is 0. "
                "Code, raw data and execution receipts are attached. "
                "This is empirical evidence; no uniform Bound or near-optimal rate is proved.")
            self.assertFalse(submission["accepted"])
            observed.update(receipt=receipt, data_path=data_path, artifact_paths=artifact_paths,
                            saved_resource=saved_resource)
            return {"text": "Empirical observations submitted."}

        with patch.dict(os.environ, {"OPENAI_API_KEY": "offline-fixture-key"}), \
                patch.object(experiment, "_Client", side_effect=remote.factory), \
                patch.object(runtime, "run_agent", side_effect=researcher) as native:
            code_result = cell_worker.solve(request_path)
            self.assertEqual(code_result, 0, (request_path.parent / "solve_result.json").read_text(encoding="utf-8"))
        self.assertEqual(native.call_count, 1)
        self.assertEqual(sum(method == "POST" and path == "/responses" for method, path, _ in remote.calls), 1)
        result = cell_worker.export_result(request_path, "finished", "completed empirical calibration")
        self.assertEqual(result["execution_status"], "finished")
        self.assertEqual(result["evidence_kind"], "empirical")
        self.assertFalse(result["accepted"])
        self.assertEqual(result["review_status"], "pending")
        self.assertEqual(result["empirical_report"]["outcome"], "observations")
        with zipfile.ZipFile(task / result["archive"]["path"]) as archive:
            self.assertEqual(archive.read(observed["data_path"]), b'{"residual":0}')
            self.assertEqual(archive.read("experiments/" + observed["receipt"]["experiment_id"] + "/requested_code.py"), code.encode())
            self.assertEqual(archive.read(observed["saved_resource"]), resource_bytes)
            self.assertEqual(archive.read(resource_path), resource_bytes)
            self.assertEqual(json.loads(archive.read("empirical_report.json"))["outcome"], "observations")
            self.assertIn("report.md", archive.namelist())
            self.assertIn("memory/experiment_result.json", archive.namelist())
        frozen_paths = {row["path"] for row in result["artifacts"]}
        self.assertIn("results/A0001/artifacts/" + observed["data_path"], frozen_paths)

        # Feed this actual returned Result into the outer Task review contract.
        returned = deepcopy(result)
        returned["artifacts"] = [{**row, "path": "tasks/T0001/" + row["path"]} for row in result["artifacts"]]
        rid = store.write_record("result", returned)["id"]
        report_path = "tasks/T0001/results/A0001/artifacts/report.md"
        review_package = store.write_record("review_package", {"review_kind": "result", "result_ref": rid,
            "required_checked_refs": [rid], "allowed_refs": [rid]})
        claim = {"id": "calibration-observation", "kind": "empirical",
            "statement": "The saved finite sample has residual 0.", "scope": "One fixed calibration sample",
            "assumptions": [], "expression": "residual = 0", "evidence_paths": [report_path]}
        review = {"review_kind": "result", "result_ref": rid, "verdict": "pass", "summary": "Fixture empirical review",
            "findings": [], "checked_refs": [rid], "confirmed_claims": [claim],
            "completion_status": "completed", "repair_kind": "none"}
        checked = validate_semantics("verify-progress", review, store, {"review_package_ref": review_package})
        review_ref = store.write_record("review", checked)
        store.set_meta(result_reviews={rid: review_ref})
        forged = deepcopy(review)
        forged["confirmed_claims"][0]["kind"] = "upper_bound"
        with self.assertRaisesRegex(ContractError, "cannot certify mathematics"):
            validate_semantics("verify-progress", forged, store, {"review_package_ref": review_package})
        progress = {"overall": "Calibration complete; the mathematical rate remains open.", "status": "in_progress",
            "items": [{"goal_id": "G0", "description": "Near-optimal Oracle rate", "status": "partial",
                       "result_refs": [rid], "remaining": ["Prove matching Bounds"]}],
            "bracket": {"bounds": [], "regimes": []}, "remaining": ["Establish the mathematical rate"]}
        validate_progress(store, progress)

        # Synthetic Brain judgment goes through the real Controller adoption
        # path. It completes this Experiment responsibility, not the Goal.
        from colombo.brain.controller import OracleController
        admission = {"result_ref": rid, "verdict": "accepted", "goal_ids": ["G0"], "proof_step_ids": [],
            "reason": "The reviewed finite calibration answers its fixed Task", "completion_status": "completed",
            "completed_parts": ["Finite calibration"], "remaining": []}
        proposal = {"summary": "Adopt the reviewed finite observation", "result_refs": [rid],
            "update": {"admissions": [admission], "progress": deepcopy(progress)}, "prunes": [],
            "next_action": "continue", "rationale": "The uniform rate still needs mathematical Proof"}
        class FixedBrain:
            def invoke(self, role, stage, *args):
                if (role, stage) != ("brain", "process_results"):
                    raise AssertionError("Unexpected research or review call")
                return deepcopy(proposal)
        controller = OracleController(PROJECT, store.root, backend=FixedBrain(), adapter=object())
        controller._initialize_proof()
        returned_event = {"result_ref": store.record_ref(rid), "state": "pending"}
        store.set_meta(round_no=1, processing_result=returned_event, result_events=[returned_event])
        controller._process_results()
        adopted = store.read_record(store.get_meta("progress_ref"))
        self.assertEqual(adopted["progress"], progress)
        assessment = store.read_record(adopted["assessment_ref"])
        self.assertEqual(assessment["update"]["admissions"], [admission])
        self.assertEqual(store.get_meta("event_data")["adoption_status"], "adopted")
        self.assertIn(rid, store.get_meta("processed_results"))
        self.assertFalse(store.read_record(rid)["accepted"])
        progress["items"][0]["status"] = "supported"
        with self.assertRaisesRegex(ContractError, "confirmed mathematical Claims"):
            validate_progress(store, progress)


if __name__ == "__main__":
    unittest.main()
