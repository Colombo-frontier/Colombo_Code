from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from colombo.configuration import PROJECT_ROOT
from colombo.configuration import load_config
from colombo.brain.submission_validation import ContractError
from colombo.brain.submission_validation import proof_complete, validate_semantics
from colombo.shared.file_io import atomic_write
from colombo.brain.proof_draft import initial_proof, write_proof
from colombo.brain.research_store import Store
from prune_fixtures import bind_prunes


def responsibility(retain=False):
    return {"problem_id": "problem-1", "claim": "The target holds", "assumptions": [],
            "scope": "All objects in the original goal", "goal_ids": ["G0"],
            "proof_step_ids": ["P0"], "route_group": "route-1", "retain": retain}


def task_spec(retain=False):
    return {"title": "Independent route", "instructions": "Establish the target",
        "deliverables": ["A complete proof"], "completion_criteria": ["All assumptions stated"],
        "mode": "new", "resume_task_id": None,
        "package": {"background": "Synthetic fixture", "selection_reason": "Self contained", "items": []},
        "responsibility": responsibility(retain)}


class SubmissionValidationTests(unittest.TestCase):
    def setUp(self):
        from brain_fixtures import freeze_setting
        parent = PROJECT_ROOT / "validation/tmp"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.root = Path(self.temp.name) / "run"
        self.store = Store.create(self.root, "Establish the target", [], load_config())
        freeze_setting(self.store)
        self.seed = initial_proof(self.store)
        self.proof_ref = write_proof(self.store, self.seed, "initial-proof")
        self.store.set_meta(proof_ref=self.proof_ref)
        self.result_ref, self.evidence = self.result("T0001", True)
        self.target = self.task("T0002")
        self.context = {"result_refs": [self.result_ref], "previous_proof_ref": self.proof_ref,
                        "task_snapshot": [self.target]}

    def tearDown(self):
        self.temp.cleanup()

    def result(self, task_id, accepted):
        from brain_fixtures import confirm_result
        content = ("Synthetic proof fixture " + task_id).encode()
        relative = f"tasks/{task_id}/results/A0001/manuscript.md"
        atomic_write(self.root / relative, content)
        entry = {"path": relative, "size": len(content)}
        ref = self.store.write_record("result", {"task_id": task_id, "attempt_id": "A0001",
            "accepted": accepted, "execution_status": "finished", "artifacts": [entry]})
        if accepted:
            confirm_result(self.store, ref)
        return ref, {"result_ref": ref["id"], "path": relative, "locator": "entire proof"}

    def task(self, task_id, retain=False):
        assignment = self.store.write_record("assignment", {"task_id": task_id, "spec": task_spec(retain)})
        task = {"task_id": task_id, "state": "running", "active_attempt": "A0001", "assignment_ref": assignment}
        self.store.save_task(task)
        return task

    def observation(self, prune=False, complete=False):
        from brain_fixtures import progress
        proof = copy.deepcopy(self.seed)
        proof.update(body="Synthetic proof of the target.", open_questions=[])
        proof["steps"][0].update(status="checked", gaps=[], evidence=[self.evidence])
        rid = self.result_ref["id"]
        value = {"summary": "Synthetic admission", "result_refs": [rid],
            "update": {"admissions": [{"result_ref": rid, "verdict": "accepted", "goal_ids": ["G0"],
                "proof_step_ids": ["P0"], "reason": "Covers the target", "completion_status": "completed",
                "completed_parts": ["The target"], "remaining": []}], "progress": progress([rid])},
            "prunes": [], "next_action": "continue", "rationale": "Use independently reviewed Result"}
        if prune:
            value["prunes"] = [{"task_id": "T0002", "attempt_id": "A0001", "reason": "redundant",
                "evidence_refs": [rid], "premises": [{"result_ref":rid,"statement":"The target holds","assumptions":[],"scope":"All objects in the original goal"}], "relation_explanation": "The same complete proof obligation",
                "scope_check": "Same assumptions, scope and quantifiers", "covered_deliverables": ["A complete proof"]}]
            if not getattr(self, "manual_audit", False):
                value["prunes"] = bind_prunes(self.store, self.context, value["prunes"])
        else:
            value["update"].update(proof_draft=proof, rechecked_step_ids=[])
        if complete:
            prog=value["update"]["progress"]
            prog.update(status="completed", remaining=[])
            prog["items"][0].update(status="supported", remaining=[])
            prog["bracket"]={"bounds":[{"id": side, "direction":side,"expression":"1","scope":"R1",
                "assumptions":[],"source":"Synthetic baseline","evidence_state":"baseline",
                "result_ref":None,"review_ref":None,"claim_id":None} for side in ("lower_bound","upper_bound")],
                "regimes":[{"id":"R1","scope":"R1","lower_bound_ids":["lower_bound"],"upper_bound_ids":["upper_bound"],
                    "gap":"1","candidate_rate":"1","candidate_basis":"Synthetic", "status":"near_optimal",
                    "comparison_review_ref":None,"comparison_claim_id":None,"remaining":[]}]}
        return value

    def check(self, value, context=None):
        stage="integrate" if "proof_draft" in value["update"] else "process_results"
        return validate_semantics(stage, value, self.store, context or self.context)

    def test_current_integration_and_separate_reviewed_pruning_are_valid(self):
        value = self.observation(complete=True)
        self.assertEqual(self.check(value), value)
        self.assertTrue(proof_complete(value["update"]["proof_draft"]))
        self.check(self.observation(prune=True))

    def test_missing_verifier_review_rejects_update_and_integration(self):
        self.store.set_meta(result_reviews={})
        for value in (self.observation(), {**self.observation(), "update": {k:v for k,v in self.observation()["update"].items() if k not in {"proof_draft","rechecked_step_ids"}}}):
            with self.assertRaisesRegex(ContractError, "Verifier"):
                self.check(value)

    def test_partial_verifier_report_does_not_complete_task(self):
        from brain_fixtures import confirm_result
        self.store.set_meta(result_reviews={})
        confirm_result(self.store,self.result_ref,completion="partial")
        with self.assertRaisesRegex(ContractError,"Partial Result"):
            self.check(self.observation())
        value=self.observation()
        value["update"]["admissions"][0].update(completion_status="partial",remaining=["A missing case"])
        self.check(value)

    def test_unconfirmed_claims_cannot_be_admitted(self):
        from brain_fixtures import confirm_result
        self.store.set_meta(result_reviews={})
        confirm_result(self.store,self.result_ref,claims=[])
        with self.assertRaisesRegex(ContractError,"confirmed Claims"):
            self.check(self.observation())

    def test_integrate_cannot_prune(self):
        value=self.observation()
        value["prunes"]=self.observation(prune=True)["prunes"]
        with self.assertRaisesRegex(ContractError,"integrate cannot prune"):
            self.check(value)

    def test_fixed_prune_remains_readable_after_target_returns(self):
        value = self.observation(prune=True)
        self.store.save_task({**self.target, "state": "returned"})
        self.assertEqual(self.check(value), value)

    def test_retired_route_does_not_block_a_complete_independent_route(self):
        value = self.observation(complete=True)
        proof = value["update"]["proof_draft"]
        replacement = {**copy.deepcopy(proof["steps"][0]), "id": "P1"}
        proof["steps"][0].update(status="retired", evidence=[], gaps=["Superseded by P1"])
        proof["steps"].append(replacement)
        value["update"]["admissions"][0]["proof_step_ids"] = ["P1"]
        self.check(value)
        replacement["depends_on"] = ["P0"]
        with self.assertRaisesRegex(ContractError, "unchecked"):
            self.check(value)

    def test_progress_requires_each_fixed_goal(self):
        value=self.observation()
        value["update"]["progress"]["items"]=[]
        with self.assertRaisesRegex(ContractError,"each Goal"):
            self.check(value)

    def test_changed_fixed_setting_and_resumed_task_are_rejected(self):
        from brain_fixtures import SETTING
        spec=task_spec()
        plan={"rationale":"Test","tasks":[spec]}
        validate_semantics("plan",plan,self.store,{})
        plan["setting_specification"]={**SETTING,"near_optimal_policy":"Different"}
        with self.assertRaisesRegex(ContractError,"fixed"):
            validate_semantics("plan",plan,self.store,{})
        self.store.save_task({**self.target,"state":"returned"})
        spec.update(mode="resume",resume_task_id="T0002")
        spec["responsibility"]["scope"]="A changed scope"
        with self.assertRaisesRegex(ContractError,"fixed Task"):
            validate_semantics("plan",{"rationale":"Resume","tasks":[spec]},self.store,{})

    def test_dispatch_budget_is_per_wave(self):
        with self.assertRaisesRegex(ContractError,"Wave dispatch"):
            validate_semantics("plan",{"rationale":"Test","tasks":[task_spec(),task_spec()]},self.store,{"dispatch_remaining":1})

    def test_duplicate_proof_step_and_dependency_cycle_are_rejected(self):
        value=self.observation()
        value["update"]["proof_draft"]["steps"].append(copy.deepcopy(value["update"]["proof_draft"]["steps"][0]))
        with self.assertRaisesRegex(ContractError,"unique"):
            self.check(value)
        value=self.observation()
        value["update"]["proof_draft"]["steps"][0]["depends_on"]=["P0"]
        with self.assertRaisesRegex(ContractError,"cyclic"):
            self.check(value)

    def test_checked_step_rejects_gap_or_unchecked_dependency(self):
        for change in ("gap","dependency"):
            value=self.observation();proof=value["update"]["proof_draft"]
            if change=="gap":proof["steps"][0]["gaps"]=["Unresolved"]
            else:
                proof["steps"].append({**copy.deepcopy(proof["steps"][0]),"id":"P1","status":"open"})
                proof["steps"][0]["depends_on"]=["P1"]
            with self.assertRaises(ContractError):self.check(value)

    def test_proof_evidence_requires_fixed_artifact(self):
        value=self.observation()
        value["update"]["proof_draft"]["steps"][0]["evidence"][0]["path"]="input/goal.md"
        with self.assertRaisesRegex(ContractError,"fixed returned artifacts"):
            self.check(value)

    def test_completion_requires_checked_nonretired_steps_and_no_questions(self):
        for mutation in (lambda p:p["steps"][0].update(status="retired"),lambda p:p.update(open_questions=["Open"]),lambda p:p["steps"][0].update(status="draft")):
            value=self.observation(complete=True);mutation(value["update"]["proof_draft"])
            with self.assertRaisesRegex(ContractError,"incomplete ProofDraft"):
                self.check(value)

    def test_proof_versions_are_immutable_and_packageable(self):
        value=self.observation()["update"]["proof_draft"]
        ref=write_proof(self.store,value,"event-proof",previous_ref=self.proof_ref)
        self.assertEqual(ref,write_proof(self.store,value,"event-proof",previous_ref=self.proof_ref))
        from colombo.brain.cell_package import build_package
        spec={"package":{"background":"Proof reuse","selection_reason":"Fixed version","items":[{"ref":ref["id"],"importance":"required","purpose":"Read","limitations":""}]}}
        target=self.root/"tasks/proof-package/input/package"
        package=build_package(self.store,"proof-package",spec,target)
        saved=json.loads((target/package["items"][0]["record_path"]).read_text(encoding="utf-8"))
        self.assertEqual(saved["proof_draft"],value)
        value["body"]+=" changed"
        with self.assertRaisesRegex(ValueError,"different (input|content)"):
            write_proof(self.store,value,"event-proof",previous_ref=self.proof_ref)
