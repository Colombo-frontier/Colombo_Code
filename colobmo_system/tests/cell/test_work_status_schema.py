"""Published obligation constraints match storage without rewriting raw input."""
from __future__ import annotations

import asyncio
from copy import deepcopy
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from colombo.cell.record_store import ALIASES
from colombo.cell.record_store import Store
from colombo.cell.record_store import StoreError
from colombo.cell.research_records import OBLIGATION_WORK_STATUSES
from colombo.cell.settings import get_settings


def proof_payload(reference, work_status="active"):
    return {"routes": [{"route_id": "R1", "target_claim_ref": deepcopy(reference),
        "obligations": [{"id": "O1", "target_claim_ref": deepcopy(reference),
                         "work_status": work_status}]}]}


class WorkStatusSchemaTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "run.json").write_text(json.dumps({"role": "prover", "settings": get_settings(),
            "agent_options": {"search_enabled": False}}), encoding="utf-8")
        self.server = importlib.import_module("colombo.cell.mcp_server")
        for name, value in (("RUN", self.root), ("ROLE", "prover")):
            setting = patch.object(self.server, name, value)
            setting.start()
            self.addCleanup(setting.stop)
        self.store = Store(self.root / "memory")
        self.store.archive("claim", {"proposition": "n=n"}, "C1")
        self.claim = {"kind": "claim", "id": "C1", "revision": 1}

    def schemas(self):
        return {tool.name: tool.inputSchema for tool in asyncio.run(self.server.mcp.list_tools())}

    @staticmethod
    def arguments(name, payload, kind="proof_state", *, update=False):
        if name == "archive":
            return {"kind": kind, "payload": payload}
        operation = {"local_key": "state", "kind": kind, "payload": payload}
        if update:
            operation.update(op="update", record_id="PS1", expected_revision=1)
        return {"records": [operation], "request_id": "schema-test"}

    def test_condition_only_applies_to_proof_state_and_covers_create_update(self):
        schemas = self.schemas()
        self.assertEqual(schemas, self.schemas())  # No mutation/duplicate condition per tools/list.
        kinds = ["proof_state", *[k for k, v in ALIASES.items() if v == "proof_state"]]
        for name in ("archive", "archive_result"):
            schema = schemas[name]
            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema)
            for kind in kinds:
                for update in (False, True):
                    for status in OBLIGATION_WORK_STATUSES:
                        payload = proof_payload(self.claim, status)
                        validator.validate(self.arguments(name, payload, kind, update=update))
                    for bad in ("in_progress", "", True, 1, None, [], {}):
                        payload = proof_payload(self.claim, bad)
                        self.assertTrue(list(validator.iter_errors(
                            self.arguments(name, payload, kind, update=update))))
                    payload = proof_payload(self.claim)
                    del payload["routes"][0]["obligations"][0]["work_status"]
                    validator.validate(self.arguments(name, payload, kind, update=update))
            for kind in ("attempt", "attempts"):
                # The same names may be extensions on other record types.
                payload = {"work_status": "in_progress", "routes": [{"obligations": [
                    {"work_status": {"custom": "in_progress"}}]}]}
                validator.validate(self.arguments(name, payload, kind))
                self.store.archive(kind, payload)

    def test_store_accepts_all_declared_values_and_rejects_bad_value_without_write(self):
        for index, status in enumerate(OBLIGATION_WORK_STATUSES):
            payload = proof_payload(self.claim, status)
            record = self.store.archive("proof_state", payload, f"PS{index}")
            self.assertEqual(record["payload"], payload)
        before = {p.name: p.read_bytes() for p in (self.root / "memory").glob("*.json")}
        for bad in ("in_progress", None, True, {}, []):
            with self.subTest(value=bad), self.assertRaises(StoreError) as caught:
                self.store.archive("proof_state", proof_payload(self.claim, bad), "invalid", request_id="bad")
            message = str(caught.exception)
            self.assertIn("proof_state.routes[0].obligations[0].work_status", message)
            for status in OBLIGATION_WORK_STATUSES:
                self.assertIn(status, message)
        self.assertEqual(before, {p.name: p.read_bytes() for p in (self.root / "memory").glob("*.json")})

    def test_reference_fields_are_described_and_default_is_not_inserted(self):
        schemas = self.schemas()
        payload = proof_payload(self.claim)
        obligation = payload["routes"][0]["obligations"][0]
        del obligation["work_status"]
        obligation.update(owner_attempt_ref=None, closing_argument_ref=None, evidence_refs=[self.claim])
        request = {"kind": "proof_state", "payload": payload, "record_id": "PS1", "request_id": "raw-state"}
        Draft202012Validator(schemas["archive"]).validate(request)
        asyncio.run(self.server.mcp.call_tool("archive", deepcopy(request)))
        ledger = json.loads((self.root / "memory/.requests.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger["raw-state"]["input"]["payload"], payload)
        before = (self.root / "memory/proof_state.json").read_bytes()
        asyncio.run(self.server.mcp.call_tool("archive", deepcopy(request)))
        self.assertEqual(before, (self.root / "memory/proof_state.json").read_bytes())
        changed = deepcopy(request)
        changed["payload"]["routes"][0]["obligations"][0]["work_status"] = "active"
        with self.assertRaises(Exception):
            asyncio.run(self.server.mcp.call_tool("archive", changed))
        for field in ("mathematical_state", "satisfaction", "satisfied", "current_trust"):
            bad = deepcopy(request)
            bad["payload"]["routes"][0]["obligations"][0][field] = "proved"
            self.assertTrue(list(Draft202012Validator(schemas["archive"]).iter_errors(bad)))

    def test_real_stdio_tools_list_and_atomic_batch_with_local_refs(self):
        from mcp import ClientSession
        from mcp import StdioServerParameters
        from mcp.client.stdio import stdio_client

        async def check():
            env = {**os.environ, "PYTHONUTF8": "1", "CELL_RUN_DIR": str(self.root), "CELL_ROLE": "prover"}
            params = StdioServerParameters(command=sys.executable, args=["-B", str(ROOT / "src/colombo/cell/mcp_server.py")], env=env)
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    schemas = {t.name: t.inputSchema for t in (await session.list_tools()).tools}
                    self.assertIn("allOf", schemas["archive"])
                    records = [
                        {"local_key": "goal", "kind": "claim", "payload": {"proposition": "m=m"}},
                        {"local_key": "work", "kind": "attempt", "payload": {"work_status": "in_progress"}},
                        {"local_key": "state", "kind": "proof_state", "payload": proof_payload({"local_key": "goal"}, "in_progress")},
                    ]
                    request = {"records": records, "request_id": "bad-batch"}
                    validator = Draft202012Validator(schemas["archive_result"])
                    self.assertTrue(list(validator.iter_errors(request)))
                    before = {p.name: p.read_bytes() for p in (self.root / "memory").glob("*.json")}
                    failed = await session.call_tool("archive_result", request)
                    self.assertTrue(failed.isError)
                    error = " ".join(c.text for c in failed.content if c.type == "text")
                    self.assertIn("routes[0].obligations[0].work_status", error)
                    self.assertEqual(before, {p.name: p.read_bytes() for p in (self.root / "memory").glob("*.json")})
                    del records[-1]["payload"]["routes"][0]["obligations"][0]["work_status"]
                    request["request_id"] = "good-batch"
                    validator.validate(request)
                    result = await session.call_tool("archive_result", request)
                    self.assertFalse(result.isError)
                    ledger = json.loads((self.root / "memory/.requests.json").read_text(encoding="utf-8"))
                    self.assertNotIn("bad-batch", ledger)
                    self.assertEqual(ledger["good-batch"]["input"]["records"], records)
                    frozen = {p.name: p.read_bytes() for p in (self.root / "memory").glob("*.json")}
                    self.assertFalse((await session.call_tool("archive_result", deepcopy(request))).isError)
                    self.assertEqual(frozen, {p.name: p.read_bytes() for p in (self.root / "memory").glob("*.json")})

        asyncio.run(check())


if __name__ == "__main__":
    unittest.main()
