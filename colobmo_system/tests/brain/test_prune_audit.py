"""Prune relations use exact, independently audited conditional claims.

All mathematical artifacts and model replies here are synthetic test fixtures.
"""
from __future__ import annotations

import copy
import json
import unittest
from unittest.mock import patch

from colombo.configuration import PROJECT_ROOT, load_config
from colombo.shared.file_io import freeze_json
from colombo.brain.mcp_server import AgentService
from colombo.brain.research_store import Store
import test_submission_validation as contracts
import test_mcp as mcp_helpers


PASS = {"verdict": "pass", "summary": "Synthetic relation is valid under the supplied premises.", "findings": []}


def with_premises(prune):
    result = copy.deepcopy(prune)
    result["premises"] = [{"result_ref": ref, "statement": "The target holds",
                           "assumptions": [], "scope": "All objects in the original goal"}
                          for ref in prune["evidence_refs"]]
    return result


class PruneAuditTests(unittest.TestCase):
    tearDown = contracts.SubmissionValidationTests.tearDown
    result = contracts.SubmissionValidationTests.result
    task = contracts.SubmissionValidationTests.task
    observation = contracts.SubmissionValidationTests.observation
    check = contracts.SubmissionValidationTests.check
    prepare_call = mcp_helpers.MCPServerTests.prepare_call

    def setUp(self):
        self.manual_audit = True
        contracts.SubmissionValidationTests.setUp(self)
        config = self.store.get_meta("config")
        self.store.set_meta(config=config)
        self.counter = 0
        self.refresh_service()

    def refresh_service(self):
        self.counter += 1
        call_id = "relation-parent-" + str(self.counter)
        self.prepare_call("brain", "process_results", call_id, **self.context)
        self.service = AgentService(self.store.root, "brain", "process_results", call_id)

    def relation(self):
        return with_premises(self.observation(prune=True)["prunes"][0])

    def review(self, relations=None, report=None, request_id=None):
        relations = [self.relation()] if relations is None else relations
        with patch("colombo.brain.evidence_audit.run_audit", return_value=copy.deepcopy(report or PASS)) as runner:
            reply = self.service.audit("Check these proposed implications.",
                {"prune_relations": copy.deepcopy(relations), "context": {"definitions": "Synthetic test domain"}},
                request_id=request_id)
        return reply, runner

    def proposal(self, reply, relations=None):
        value = self.observation(prune=True)
        value["prunes"] = [{**copy.deepcopy(p), "audit_ref": reply["ref"]["id"]}
                           for p in (relations if relations is not None else [self.relation()])]
        return value

    def test_default_policy_requires_relation_audit(self):
        self.assertEqual(load_config()["storage_version"], 4)
        override = self.root.parent / "disable-relation-audit.toml"
        for literal in ("false", "1", '"true"'):
            override.write_text("[workflow]\nprune_relation_audit = " + literal + "\n", encoding="utf-8")
            with self.subTest(setting=literal), self.assertRaises(ValueError):
                load_config(override)
        for prune in (self.observation(prune=True)["prunes"][0], self.relation()):
            value = self.observation(prune=True)
            value["prunes"] = [prune]
            with self.subTest(fields=sorted(prune)), self.assertRaises(ValueError):
                self.check(value)

    def test_relation_audit_binds_frozen_tasks_without_copying_source_proof(self):
        before = {k: self.store.get_meta(k) for k in ("proof_ref", "progress_ref", "prune_commands")}
        reply, runner = self.review(request_id="first-relation")
        self.assertEqual(reply["verdict"], "pass")
        proposal = self.proposal(reply)
        self.assertEqual(self.check(proposal), proposal)
        sent = runner.call_args.args[3]
        encoded = json.dumps(sent)
        self.assertIn(self.target["assignment_ref"]["id"], encoded)
        self.assertIn(self.result_ref["id"], encoded)
        self.assertIn("A complete proof", encoded)
        self.assertNotIn("Synthetic proof fixture T0001", encoded)
        self.assertEqual(before, {k: self.store.get_meta(k) for k in before})

    def test_generic_audit_pass_cannot_authorize_pruning(self):
        with patch("colombo.brain.evidence_audit.run_audit", return_value=copy.deepcopy(PASS)):
            reply = self.service.audit("Check an unrelated sum", {"expression": "1+1=2"})
        with self.assertRaises(ValueError):
            self.check(self.proposal(reply))

    def test_fail_uncertain_and_execution_error_cannot_authorize_pruning(self):
        for verdict in ("fail", "uncertain"):
            report = {"verdict": verdict, "summary": "Synthetic relation is not established.",
                      "findings": ["Its source scope is narrower than the target scope."]}
            reply, _ = self.review(report=report, request_id=verdict)
            with self.subTest(verdict=verdict), self.assertRaises(ValueError):
                self.check(self.proposal(reply))
        with patch("colombo.brain.evidence_audit.run_audit", side_effect=RuntimeError("Synthetic process failure")):
            reply = self.service.audit("Check relation", {"prune_relations": [self.relation()]}, request_id="error")
        self.assertEqual(reply["status"], "error")
        with self.assertRaises(ValueError):
            self.check(self.proposal(reply))

    def test_batch_pass_can_be_reused_for_each_exact_subset_without_another_call(self):
        third = self.task("T0003")
        self.context["task_snapshot"].append(third)
        self.refresh_service()
        first = self.relation()
        second = {**copy.deepcopy(first), "task_id": "T0003"}
        reply, runner = self.review([first, second], request_id="batch")
        for selection in ([first], [second], [first, second]):
            value = self.proposal(reply, selection)
            self.assertEqual(self.check(value), value)
        self.assertEqual(runner.call_count, 1)
        self.assertEqual(self.store.get_meta("audit_call_count"), 1)

    def test_changing_claim_assumptions_scope_or_relation_requires_new_audit(self):
        reply, _ = self.review()
        mutations = [
            lambda p: p["premises"][0].update(statement="An entirely different theorem"),
            lambda p: p["premises"][0].update(assumptions=["An extra condition"]),
            lambda p: p["premises"][0].update(scope="Only a strict subset"),
            lambda p: p.update(reason="refuted_target"),
            lambda p: p.update(relation_explanation="Different reasoning"),
            lambda p: p.update(scope_check="A changed domain"),
        ]
        for index, mutate in enumerate(mutations):
            value = self.proposal(reply)
            mutate(value["prunes"][0])
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.check(value)

    def test_pass_for_another_target_or_attempt_cannot_be_reused(self):
        reply, _ = self.review()
        third = self.task("T0003")
        context = {**self.context, "task_snapshot": [self.target, third]}
        value = self.proposal(reply)
        value["prunes"][0]["task_id"] = "T0003"
        with self.assertRaises(ValueError):
            self.check(value, context)
        changed = {**self.target, "active_attempt": "A0002"}
        self.store.save_task(changed)
        value = self.proposal(reply)
        value["prunes"][0]["attempt_id"] = "A0002"
        with self.assertRaises(ValueError):
            self.check(value, {**self.context, "task_snapshot": [changed]})

    def test_all_evidence_sources_must_have_explicit_premises(self):
        second, _ = self.result("T0003", True)
        relation = self.relation()
        relation["evidence_refs"].append(second["id"])
        with patch("colombo.brain.evidence_audit.run_audit") as runner, self.assertRaises(ValueError):
            self.service.audit("Check relation", {"prune_relations": [relation]})
        runner.assert_not_called()

        relation = self.relation()
        relation["premises"].append({"result_ref": second["id"], "statement": "Extra premise",
                                      "assumptions": [], "scope": "Same domain"})
        with patch("colombo.brain.evidence_audit.run_audit") as runner, self.assertRaises(ValueError):
            self.service.audit("Check relation", {"prune_relations": [relation]})
        runner.assert_not_called()

    def test_every_target_deliverable_must_be_covered_before_audit(self):
        relation = self.relation()
        for covered in (["An unrelated output"], ["A complete proof", "A complete proof"]):
            relation["covered_deliverables"] = covered
            with self.subTest(covered=covered), patch("colombo.brain.evidence_audit.run_audit") as runner:
                with self.assertRaisesRegex(ValueError, "every target deliverable"):
                    self.service.audit("Check relation", {"prune_relations": [relation]})
                runner.assert_not_called()

    def test_retained_or_stale_target_is_rejected_before_audit_process(self):
        stale = {**self.target, "state": "returned"}
        self.store.save_task(stale)
        with patch("colombo.brain.evidence_audit.run_audit") as runner, self.assertRaises(ValueError):
            self.service.audit("Check relation", {"prune_relations": [self.relation()]})
        runner.assert_not_called()
        self.assertEqual(self.store.get_meta("audit_call_count", 0), 0)
        retained = self.task("T0003", retain=True)
        self.context["task_snapshot"].append(retained)
        self.refresh_service()
        relation = {**self.relation(), "task_id": "T0003"}
        with patch("colombo.brain.evidence_audit.run_audit") as runner, self.assertRaises(ValueError):
            self.service.audit("Check retained task", {"prune_relations": [relation]})
        runner.assert_not_called()
        self.assertEqual(self.store.get_meta("audit_call_count", 0), 0)




