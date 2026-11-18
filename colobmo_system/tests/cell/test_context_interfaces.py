"""Compact MCP receipts preserve complete evidence and runtime semantics."""
from __future__ import annotations

import importlib
import asyncio
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from colombo.cell.verifier.local_audit import audit as audit_record
from colombo.cell.record_store import Store
import colombo.cell.settings as settings
from colombo.cell.settings import get_settings


class ContextInterfaceTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for key in ("CELL_RUN_DIR", "CELL_ROLE", "CELL_SETTINGS_FILE", "CELL_SEARCH_ENABLED",
                    "CELL_REQUESTED_MODEL", "CELL_MODEL", "CELL_AGENT_TIMEOUT"):
            os.environ.pop(key, None)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.settings = get_settings()
        (self.work / "run.json").write_text(json.dumps({
            "role": "prover", "settings": self.settings,
            "agent_options": {"search_enabled": True},
        }), encoding="utf-8")
        self.server = importlib.import_module("colombo.cell.mcp_server")
        for name, value in (("RUN", self.work), ("ROLE", "prover")):
            setting = patch.object(self.server, name, value)
            setting.start()
            self.addCleanup(setting.stop)

    def test_saved_proof_is_complete_retrievable_and_write_retry_is_idempotent(self):
        payload = {"body": "A complete derivation with all assumptions. " * 400,
                   "status": "candidate"}
        receipt = self.server.archive("arguments", payload, "A1", request_id="save-1")
        self.assertNotIn("payload", receipt)
        full = self.server.retrieve(kinds=[receipt["kind"]], record_id=receipt["id"],
                                    revision=receipt["revision"])["records"][0]
        self.assertEqual(full["payload"], payload)
        self.assertEqual(full["revision"], receipt["revision"])
        replay = self.server.archive("arguments", payload, "A1", request_id="save-1", detail="full")
        self.assertEqual(replay, full)
        changed = {**payload, "body": payload["body"] + "Revised final step."}
        next_receipt = self.server.archive("arguments", changed, "A1", expected_revision=1)
        self.assertEqual(next_receipt["revision"], 2)
        self.assertEqual(self.server.retrieve(kinds=["arguments"], record_id="A1", revision=1)
                         ["records"][0], full)

    def test_invalid_display_option_does_not_write_or_launch(self):
        with self.assertRaises(ValueError):
            self.server.archive("claims", {"statement": "n=n"}, "C1", detail="invalid")
        self.assertEqual(Store(self.work / "memory").retrieve(kinds=["claims"])["count"], 0)
        with patch.object(self.server, "submit_or_poll") as launch:
            with self.assertRaises(ValueError):
                self.server.audit("arguments", "A1", 1, detail="invalid")
            launch.assert_not_called()

    def test_published_archive_schema_explains_conclusions_and_batch_operations(self):
        from jsonschema import Draft202012Validator
        schemas = {tool.name: tool.inputSchema for tool in asyncio.run(self.server.mcp.list_tools())}
        valid = {"kind": "argument", "payload": {"content": "Proof", "conclusions": [
            {"target": {"kind": "claim", "id": "C1", "revision": 1}, "relation": "supports"}]}}
        validator = Draft202012Validator(schemas["archive"])
        validator.validate(valid)
        for conclusion in [{"target": {"kind": "claim", "id": "C1", "revision": 1}, "relation": "supports", "reason": "bad"},
                           {"claim_ref": {"kind": "claim", "id": "C1", "revision": 1}, "relation": "supports"}]:
            bad = deepcopy(valid)
            bad["payload"]["conclusions"] = [conclusion]
            self.assertTrue(list(validator.iter_errors(bad)))
        operations = [
            {"local_key": "target", "kind": "claim", "payload": {"proposition": "n=n"}},
            {"local_key": "alias", "op": "reference", "ref": {"local_key": "target"}},
            {"local_key": "proof", "op": "create", "kind": "argument", "payload": {"status": "candidate", "content": "Identity", "conclusions": [
                {"target": {"local_key": "alias"}, "relation": "supports"}]}},
            {"local_key": "update", "op": "update", "kind": "attempt", "record_id": "A1", "expected_revision": 1, "payload": {"notes": "next"}},
        ]
        validator = Draft202012Validator(schemas["archive_result"])
        validator.validate({"records": operations, "request_id": "result-1"})
        bad = deepcopy(operations)
        del bad[-1]["expected_revision"]
        self.assertTrue(list(validator.iter_errors({"records": bad, "request_id": "result-1"})))

    def test_mcp_archive_batch_keeps_aliases_omissions_and_boolean_replay_inputs(self):
        operations = [
            {"local_key": "target", "kind": "claim", "payload": {"proposition": "n=n", "metadata": {"flag": True}}},
            {"local_key": "alias", "op": "reference", "ref": {"local_key": "target"}},
            {"local_key": "proof", "kind": "argument", "payload": {"content": "Identity", "status": "candidate", "conclusions": [
                {"target": {"local_key": "alias"}, "relation": "supports"}]}},
        ]
        arguments = {"records": operations, "request_id": "raw-batch"}
        asyncio.run(self.server.mcp.call_tool("archive_result", deepcopy(arguments)))
        ledger = json.loads((self.work / "memory/.requests.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger["raw-batch"]["input"]["records"], operations)
        self.assertNotIn("op", ledger["raw-batch"]["input"]["records"][0])
        first = (self.work / "memory/arguments.json").read_bytes()
        asyncio.run(self.server.mcp.call_tool("archive_result", deepcopy(arguments)))
        self.assertEqual((self.work / "memory/arguments.json").read_bytes(), first)
        changed = deepcopy(operations)
        changed[0]["payload"]["metadata"]["flag"] = 1
        with self.assertRaises(Exception):
            asyncio.run(self.server.mcp.call_tool("archive_result", {"records": changed, "request_id": "raw-batch"}))

    def test_example_conclusion_schema_requires_selected_properties_and_supports(self):
        from jsonschema import Draft202012Validator
        schemas = {tool.name: tool.inputSchema for tool in asyncio.run(self.server.mcp.list_tools())}
        for name in ("archive", "archive_result"):
            validator = Draft202012Validator(schemas[name])

            def arguments(conclusion):
                payload = {"content": "Proof", "conclusions": [conclusion]}
                if name == "archive":
                    return {"kind": "arguments", "payload": payload}
                return {"records": [{"local_key": "proof", "kind": "argument", "payload": payload}],
                        "request_id": "example-scope"}

            for kind in ("example", "examples"):
                conclusion = {"target": {"kind": kind, "id": "E1", "revision": 1, "property_ids": ["p1"]},
                              "relation": "supports"}
                validator.validate(arguments(conclusion))
                missing = deepcopy(conclusion)
                del missing["target"]["property_ids"]
                self.assertTrue(list(validator.iter_errors(arguments(missing))))
                empty = deepcopy(conclusion)
                empty["target"]["property_ids"] = []
                self.assertTrue(list(validator.iter_errors(arguments(empty))))
                self.assertTrue(list(validator.iter_errors(arguments({**conclusion, "relation": "refutes"}))))
            validator.validate(arguments({"target": {"kind": "claim", "id": "C1", "revision": 1},
                                          "relation": "refutes"}))
            if name == "archive_result":
                validator.validate(arguments({"target": {"local_key": "target"}, "relation": "refutes"}))

    def test_route_review_schema_explains_attempt_object_and_preserves_structured_values(self):
        from jsonschema import Draft202012Validator
        schemas = {tool.name: tool.inputSchema for tool in asyncio.run(self.server.mcp.list_tools())}
        reviews = [None, {"decision": "continue", "reason": "A remaining step is now accessible."},
                   {"decision": {"action": "reformulate"}, "reason": ["The scope changed."], "extra": True}]
        for name in ("archive", "archive_result"):
            validator = Draft202012Validator(schemas[name])
            if name == "archive":
                payload_schemas = [schemas[name]["properties"]["payload"]]
            else:
                payload_schemas = [branch["properties"]["payload"] for branch in
                    schemas[name]["properties"]["records"]["items"]["oneOf"] if "payload" in branch["properties"]]
            for payload_schema in payload_schemas:
                review_schema = payload_schema["properties"]["route_review"]
                self.assertIn("object, not a string", review_schema["description"])
                self.assertIn("decision", review_schema["properties"])
                self.assertIn("reason", review_schema["properties"])
                self.assertNotIn("route_review", payload_schema.get("required", []))
                for field in review_schema["properties"].values():
                    self.assertNotIn("type", field)
                    self.assertNotIn("enum", field)
            for index, review in enumerate(reviews):
                payload = {"summary": "Review a route"}
                if review is not None:
                    payload["route_review"] = deepcopy(review)
                request_id = f"{name}-route-review-{index}"
                if name == "archive":
                    arguments = {"kind": "attempt", "payload": payload, "request_id": request_id}
                else:
                    arguments = {"records": [{"local_key": "work", "kind": "attempt", "payload": payload}],
                                 "request_id": request_id}
                validator.validate(arguments)
                asyncio.run(self.server.mcp.call_tool(name, deepcopy(arguments)))
                before = (self.work / "memory/attempts.json").read_bytes()
                asyncio.run(self.server.mcp.call_tool(name, deepcopy(arguments)))
                self.assertEqual((self.work / "memory/attempts.json").read_bytes(), before)
                ledger = json.loads((self.work / "memory/.requests.json").read_text(encoding="utf-8"))
                original = ledger[request_id]["input"]
                self.assertEqual(original["payload"] if name == "archive" else original["records"][0]["payload"], payload)
                if name == "archive_result":
                    self.assertNotIn("op", original["records"][0])
                    self.assertEqual(original["records"][0]["kind"], "attempt")

    def test_configuration_summary_preserves_change_timing_and_full_query(self):
        before = settings.CONFIG_PATH.read_bytes()
        snapshot = self.work / "launch.json"
        snapshot.write_text(json.dumps(self.settings), encoding="utf-8")
        with patch.dict(os.environ, {"CELL_RUN_DIR": str(self.work), "CELL_SEARCH_ENABLED": "1",
                                     "CELL_SETTINGS_FILE": str(snapshot)}):
            response = self.server.configure({"model": {"reasoning_effort": "high"}},
                                             search_enabled=False, reason="Check dynamic vs startup settings")
            self.assertNotIn("desired_settings", response)
            self.assertNotIn("launch_settings", response)
            self.assertFalse(response["lookup_enabled"])
            self.assertTrue(response["native_search_enabled"])
            self.assertTrue(any(row["parameter"] == "native_search_enabled"
                                for row in response["pending_next_start"]))
            full = self.server.configure(detail="full")
            self.assertEqual(full["settings_revision"], response["settings_revision"])
            self.assertEqual(full["desired_settings"]["model"]["reasoning_effort"], "high")
            self.assertEqual(full["launch_settings"], self.settings)
        self.assertEqual(settings.CONFIG_PATH.read_bytes(), before)

    def test_resume_installs_missing_protocol_without_overwriting_task_instructions(self):
        import colombo.cell.controller as run
        (self.work / "AGENTS.md").write_text("Task-specific instructions", encoding="utf-8")
        with patch.object(run, "manuscript_is_current", return_value=False), \
                patch.object(run, "_prover_state", return_value={"launches": self.settings["agents"]["prover_max_rounds"]}):
            self.assertEqual(run.solve(self.work), 2)
        self.assertEqual((self.work / "protocol.md").read_bytes(),
                         (ROOT / "agents/cell/prover/protocol.md").read_bytes())
        self.assertEqual((self.work / "AGENTS.md").read_text(encoding="utf-8"), "Task-specific instructions")
        (self.work / "protocol.md").write_text("Task-specific protocol", encoding="utf-8")
        with patch.object(run, "manuscript_is_current", return_value=False), \
                patch.object(run, "_prover_state", return_value={"launches": self.settings["agents"]["prover_max_rounds"]}):
            self.assertEqual(run.solve(self.work), 2)
        self.assertEqual((self.work / "protocol.md").read_text(encoding="utf-8"), "Task-specific protocol")

    def test_small_audit_has_full_file_input_and_receipt_keeps_audited_revision(self):
        (self.work / "problem.md").write_text("Prove 2 is even.", encoding="utf-8")
        claim = self.server.archive("claims", {"statement": "2 is even."}, "C1")
        dependency = {k: claim[k] for k in ("kind", "id", "revision")}
        saved = self.server.archive("arguments", {"body": "2=2*1, and 1 is an integer.",
                                    "status": "candidate", "dependencies": [dependency]}, "A1")

        def reviewer(prompt, directory):
            context = json.loads((directory / "input.json").read_text(encoding="utf-8"))
            self.assertEqual(context["problem"], "Prove 2 is even.")
            self.assertEqual({key: context["record"][key] for key in ("kind", "id", "revision")},
                             {key: saved[key] for key in ("kind", "id", "revision")})
            self.assertEqual(context["record"]["payload"]["body"], "2=2*1, and 1 is an integer.")
            self.assertEqual(context["dependencies"][0]["id"], "C1")
            return {"verdict": "pass", "summary": "2 has the required form.",
                    "findings": [], "properties": []}

        def local_audit(root, operation, payload):
            self.assertEqual(operation, "audit")
            return audit_record(root, **payload, reviewer=reviewer)

        with patch.object(self.server, "submit_or_poll", side_effect=local_audit):
            result = self.server.audit("arguments", "A1", 1)
        self.assertNotIn("payload", result["record"])
        self.assertEqual(result["record"]["status"], "proved")
        self.assertEqual(result["record"]["revision"], 2)
        self.assertEqual(result["review"]["payload"]["target"]["revision"], 1)
        self.assertEqual(Store(self.work / "memory").get("arguments", "A1", 2)["payload"]
                         ["body"], "2=2*1, and 1 is an integer.")

    def test_audit_summary_does_not_repeat_experiment_file_inventory(self):
        manifest = [{"path": "experiments/test/data.bin", "size": 100}]
        complete = {"review": {"payload": {"verdict": "uncertain", "experiment_artifacts": manifest}},
                    "record": None}
        with patch.object(self.server, "submit_or_poll", return_value=complete):
            compact = self.server.audit("arguments", "A1", 1)
            self.assertNotIn("experiment_artifacts", compact["review"]["payload"])
            self.assertEqual(compact["review"]["payload"]["experiment_artifact_count"], 1)
            self.assertEqual(self.server.audit("arguments", "A1", 1, detail="full"), complete)
        self.assertEqual(complete["review"]["payload"]["experiment_artifacts"], manifest)


if __name__ == "__main__":
    unittest.main()
