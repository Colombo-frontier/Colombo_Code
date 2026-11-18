"""Bounded lightweight checks are evidence, never direct programme updates."""
from __future__ import annotations
from brain_fixtures import write_review_package

import copy
import json
import unittest
from unittest.mock import patch

from colombo.brain.mcp_server import AgentService
import test_mcp as mcp_helpers
import test_brain_service as fixtures


PASS = {"verdict": "pass", "summary": "The supplied implication holds.", "findings": []}
INPUTS = {"premise": "For every real x, f(x) >= 2.",
          "target": "For every real x, f(x) >= 1."}
GOAL = "Check whether the premise implies the target under the same domain."


class BrainAuditTests(unittest.TestCase):
    prepare_call = mcp_helpers.MCPServerTests.prepare_call

    def setUp(self):
        fixtures.create_fixture(self)
        self.prepare_call("brain", "process_results", "audit-parent",
                          result_refs=[self.result], previous_proof_ref=self.seed, task_snapshot=[])
        self.service = AgentService(self.store.root, "brain", "process_results", "audit-parent")

    def audit(self, **kwargs):
        return self.service.audit(GOAL, copy.deepcopy(INPUTS), **kwargs)

    def authoritative_state(self):
        return {"tasks": self.store.list_tasks(), **{key: self.store.get_meta(key) for key in
                ("progress_ref", "proof_ref", "prune_commands", "pending_call", "result_events")}}

    def test_selected_inputs_are_frozen_without_implicit_history_or_state_changes(self):
        self.store.write_record("note", {"text": "Unrelated private draft must not enter this check."})
        before = self.authoritative_state()
        self.store.set_meta(model_call_count=5)
        with patch("colombo.brain.evidence_audit.run_audit", return_value=copy.deepcopy(PASS)) as run:
            result = self.audit(record_refs=[self.result["id"]], materials=[{'ref': self.result['id'], 'path': self.artifact['path']}], request_id="relation-P-Q")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["verdict"], "pass")
        self.assertEqual(self.store.record_kind(result["ref"]), "audit")
        payload = run.call_args.args[3]
        self.assertEqual(payload["goal"], GOAL)
        self.assertEqual(payload["inputs"], INPUTS)
        self.assertEqual([r["ref"]["id"] for r in payload["records"]], [self.result["id"]])
        self.assertEqual(payload["records"][0]["payload"], self.store.read_record(self.result))
        material = payload["materials"][0]
        self.assertEqual(material["text"], (self.store.root / self.artifact["path"]).read_bytes().decode("utf-8-sig"))
        self.assertNotIn("Unrelated private draft", str(payload))
        self.assertEqual(self.authoritative_state(), before)
        self.assertEqual(self.store.get_meta("model_call_count"), 6)
        self.assertEqual(self.store.get_meta("audit_call_count"), 1)
        self.assertEqual(self.store.retrieve("audit")[0]["id"], result["ref"]["id"])
        self.assertEqual(self.service.read_research(ref=result["ref"]["id"])["ref"], result["ref"])

    def test_same_request_replays_without_another_call_and_changed_inputs_are_rejected(self):
        with patch("colombo.brain.evidence_audit.run_audit", return_value=copy.deepcopy(PASS)) as run:
            first = self.audit(request_id="repeat-me")
            second = self.audit(request_id="repeat-me")
            self.assertEqual(first, second)
            with self.assertRaises(ValueError):
                self.service.audit("A different question", INPUTS, request_id="repeat-me")
        self.assertEqual(run.call_count, 1)
        self.assertEqual(self.store.get_meta("model_call_count"), 1)
        self.assertEqual(self.store.get_meta("audit_call_count"), 1)
        self.assertEqual(len(self.store.retrieve("audit")), 1)


    def test_interrupted_pending_or_unknown_request_never_launches_a_duplicate(self):
        with patch("colombo.brain.evidence_audit.run_audit", side_effect=KeyboardInterrupt) as run:
            with self.assertRaises(KeyboardInterrupt):
                self.audit(request_id="interrupted-check")
            event = next(event for event in self.store.events() if event["name"] == "audit_started")
            key = "audit:" + event["payload"]["audit_id"]
            saved = self.store.get_request(key)
            self.assertEqual(saved["state"], "pending")
            with self.assertRaises(ValueError):
                self.audit(request_id="interrupted-check")
            self.store.save_request(key, saved["payload"], "unknown")
            with self.assertRaises(ValueError):
                self.audit(request_id="interrupted-check")
        self.assertEqual(run.call_count, 1)
        self.assertEqual(self.store.get_meta("model_call_count"), 1)
        self.assertEqual(self.store.get_meta("audit_call_count"), 1)
        self.assertEqual(self.store.retrieve("audit"), [])

    def test_old_global_call_usage_does_not_cap_current_audit(self):
        self.store.set_meta(model_call_count=100000)
        before = self.authoritative_state()
        with patch("colombo.brain.evidence_audit.run_audit", return_value=copy.deepcopy(PASS)) as run:
            result = self.audit()
        self.assertEqual(result["status"], "completed")
        run.assert_called_once()
        self.assertEqual(self.store.get_meta("model_call_count"), 100001)
        self.assertEqual(self.authoritative_state(), before)

    def test_process_failure_is_not_a_mathematical_failure_and_is_not_retried_implicitly(self):
        before = self.authoritative_state()
        with patch("colombo.brain.evidence_audit.run_audit", side_effect=TimeoutError("Synthetic timeout")) as run:
            result = self.audit(request_id="failed-worker")
            replay = self.audit(request_id="failed-worker")
        self.assertEqual(result["status"], "error")
        self.assertNotIn("verdict", result)
        self.assertEqual(result, replay)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(self.store.get_meta("audit_call_count"), 1)
        self.assertEqual(self.authoritative_state(), before)

    def test_unconfirmed_process_exit_keeps_request_unknown_and_workspace_out_of_fixed_evidence(self):
        before = self.authoritative_state()
        workspaces = []
        def unresolved(_project, _config, work, _payload):
            work.mkdir(parents=True, exist_ok=True)
            workspaces.append(work)
            (work / "process.json").write_text(json.dumps({"status": "unknown", "pid": 123,
                "process_exit_confirmed": False, "process_tree_terminated": False}), encoding="utf-8")
            (work / "events.jsonl").write_text("initial process output\n", encoding="utf-8")
            raise RuntimeError("Synthetic process termination was not confirmed")
        with patch("colombo.brain.evidence_audit.run_audit", side_effect=unresolved) as run:
            result = self.audit(request_id="unresolved-worker")
            self.assertEqual(result["status"], "error")
            self.assertTrue(result["execution_unknown"])
            self.assertNotIn("verdict", result)
            request = self.store.get_request("audit:" + result["audit_id"])
            self.assertEqual(request["state"], "unknown")
            self.assertEqual(request["result"]["ref"], result["ref"])
            fixed = self.store.read_record(result["ref"])
            paths = [item["path"] for item in self.store.artifact_entries(result["ref"])]
            self.assertEqual(len(paths), 2)
            self.assertTrue(any(path.endswith("/request.json") for path in paths))
            self.assertTrue(any(path.endswith("/result.json") for path in paths))
            self.assertFalse(any("/workspace/" in path for path in paths))
            (workspaces[0] / "events.jsonl").write_text("late output from unresolved process\n", encoding="utf-8")
            self.assertEqual(self.store.read_record(result["ref"]), fixed)
            self.assertEqual([item["path"] for item in self.store.artifact_entries(result["ref"])], paths)
            with self.assertRaises(ValueError):
                self.audit(request_id="unresolved-worker")
        self.assertEqual(run.call_count, 1)
        self.assertEqual(self.store.get_meta("audit_call_count"), 1)
        self.assertEqual(self.authoritative_state(), before)

    def test_failed_or_uncertain_math_checks_remain_audit_evidence_only(self):
        before = self.authoritative_state()
        for verdict in ("fail", "uncertain"):
            report = {"verdict": verdict, "summary": "The requested conclusion is not established.",
                      "findings": ["The supplied premise has a narrower domain."]}
            with self.subTest(verdict=verdict), patch("colombo.brain.evidence_audit.run_audit", return_value=report):
                result = self.audit(request_id=verdict)
                self.assertEqual(result["status"], "completed")
                self.assertEqual(result["verdict"], verdict)
        self.assertEqual(self.authoritative_state(), before)

    def test_invalid_worker_output_is_an_execution_error_not_a_mathematical_pass(self):
        reports = [{"verdict": "pass", "summary": "", "findings": []},
                   {"verdict": "pass", "summary": "Inconsistent report", "findings": ["A gap remains."]},
                   {"verdict": "pass", "summary": "Missing required findings"}]
        before = self.authoritative_state()
        for index, report in enumerate(reports):
            with self.subTest(index=index), patch("colombo.brain.evidence_audit.run_audit", return_value=report):
                result = self.audit(request_id=f"invalid-report-{index}")
                self.assertEqual(result["status"], "error")
                self.assertNotIn("verdict", result)
        self.assertEqual(self.authoritative_state(), before)

    def test_malformed_input_is_rejected_without_charging_budget(self):
        cases = [("", INPUTS), (GOAL, []), (GOAL, {"not_json": object()}),
                 (GOAL, {"oversized": "x" * 250001})]
        with patch("colombo.brain.evidence_audit.run_audit") as run:
            for goal, inputs in cases:
                with self.subTest(goal=bool(goal), input_type=type(inputs).__name__), \
                     self.assertRaises((ValueError, TypeError)):
                    self.service.audit(goal, inputs)
        run.assert_not_called()
        self.assertEqual(self.store.get_meta("model_call_count", 0), 0)

    def test_material_must_belong_to_selected_reference(self):
        selections = [
            {"ref": self.result["id"], "path": "input/goal.md"},
            {"ref": "missing-record", "path": self.artifact["path"]},
        ]
        with patch("colombo.brain.evidence_audit.run_audit") as run:
            for item in selections:
                with self.subTest(selection=item), self.assertRaises(ValueError):
                    self.audit(materials=[item])
        run.assert_not_called()
        self.assertEqual(self.store.get_meta("model_call_count", 0), 0)

    def test_selected_text_is_not_silently_truncated(self):
        text = "A bounded, explicitly selected mathematical definition.\n" * 900
        path = self.store.root / "input/long-definition.txt"
        path.write_text(text, encoding="utf-8")
        data = path.read_bytes()
        ref = self.store.write_record("material", {"artifacts": [{'path': 'input/long-definition.txt', 'size': len(data)}]})
        with patch("colombo.brain.evidence_audit.run_audit", return_value=copy.deepcopy(PASS)) as run:
            result = self.audit(materials=[{"ref": ref["id"], "path": "input/long-definition.txt"}])
        self.assertEqual(result["status"], "completed")
        self.assertEqual(run.call_args.args[3]["materials"][0]["text"], data.decode("utf-8-sig"))


    def test_only_current_active_brain_calls_may_launch_audits(self):
        package = write_review_package(self.store, {
            "allowed_refs": [self.seed["id"]], "required_checked_refs": [self.seed["id"]]})
        self.prepare_call("verifier", "verify-progress", "audit-forbidden", review_package_ref=package)
        verifier = AgentService(self.store.root, "verifier", "verify-progress", "audit-forbidden")
        with patch("colombo.brain.evidence_audit.run_audit") as run:
            with self.assertRaises(ValueError):
                verifier.audit(GOAL, INPUTS)
            with self.assertRaises(ValueError):
                self.audit()  # The original Brain call is now stale.
            config = self.store.get_meta("config")
            config["workflow"]["version"] = 1
            self.store.set_meta(config=config)
            self.prepare_call("brain", "plan", "legacy-audit")
            with self.assertRaises(ValueError):
                AgentService(self.store.root, "brain", "plan", "legacy-audit")
        run.assert_not_called()


class BrainAuditMCPTests(unittest.IsolatedAsyncioTestCase):
    setUp = fixtures.create_fixture
    prepare_call = mcp_helpers.MCPServerTests.prepare_call
    connect = mcp_helpers.MCPServerTests.connect

    async def test_real_stdio_exposes_audit_and_rejects_invalid_input_before_launch(self):
        self.prepare_call("brain", "process_results", "audit-mcp", result_refs=[self.result],
                          previous_proof_ref=self.seed, task_snapshot=[])
        async with self.connect("brain", "process_results", "audit-mcp") as session:
            names = {tool.name for tool in (await session.list_tools()).tools}
            self.assertIn("audit", names)
            denied = await session.call_tool("audit", {"goal": "", "inputs": INPUTS})
            self.assertTrue(denied.isError)
        self.assertEqual(self.store.get_meta("model_call_count", 0), 0)
        self.assertEqual(self.store.retrieve("audit"), [])


if __name__ == "__main__":
    unittest.main()
