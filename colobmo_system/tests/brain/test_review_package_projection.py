"""One authorized projection supplies required bodies without duplicate storage."""
from __future__ import annotations
from brain_fixtures import write_review_package

import copy
import json
import unittest
from unittest.mock import patch

from colombo.brain.mcp_server import AgentService
from colombo.shared.file_io import json_bytes
from colombo.brain.research_store import Store
import test_mcp as mcp_helpers
import test_brain_service as fixtures


def prepare(test):
    fixtures.create_fixture(test)
    test.assessment = test.store.write_record("assessment", fixtures.observation(test))
    test.candidate = test.store.assessment_proof(test.assessment)
    file = test.store.root / "input/external-only.txt"
    file.write_text("ATTACHMENT_BODY_NOT_AUTOMATICALLY_INLINED", encoding="utf-8")
    test.material = test.store.write_record("material", {"summary": "External evidence",
        "artifacts": [{"path": "input/external-only.txt"}]})
    test.history = test.store.write_record("note", {"text": "ALLOWED_HISTORY_NOT_AUTOMATICALLY_INLINED"})
    test.outside = test.store.write_record("note", {"text": "OUTSIDE_PACKAGE_NOT_AUTHORIZED"})
    test.required = [test.store.get_meta("goal_ref"), test.assessment, test.candidate,
                     test.seed, test.result, test.material]
    test.package = {"goal_ref": test.required[0], "proposal_ref": test.assessment,
        "proof_candidate_ref": test.candidate, "previous_proof_ref": test.seed,
        "allowed_refs": [r["id"] for r in test.required] + [test.history["id"]],
        "required_checked_refs": [r["id"] for r in test.required],
        "references": test.required + [test.history], "prior_review_refs": []}
    test.package_ref = write_review_package(test.store, test.package)


class ReviewPackageProjectionTests(unittest.TestCase):
    setUp = prepare
    prepare_call = mcp_helpers.MCPServerTests.prepare_call

    def test_projection_matches_public_reads_deduplicates_proof_and_never_writes(self):
        before = self.store.snapshot()
        page = self.store.review_package_view(self.package_ref)
        self.assertEqual(page["required_checked_refs"], self.package["required_checked_refs"])
        for item in page["required_records"]:
            self.assertEqual(item["payload"], self.store.public_read(item["ref"]))
        assessment = next(item["payload"] for item in page["required_records"] if item["ref"] == self.assessment)
        self.assertEqual(assessment["update"]["proof_ref"], self.candidate)
        self.assertNotIn("proof_draft", assessment["update"])
        self.assertEqual(sum(item["ref"] == self.candidate for item in page["required_records"]), 1)
        text = json.dumps(page)
        for marker in ("ATTACHMENT_BODY_NOT_AUTOMATICALLY_INLINED", "ALLOWED_HISTORY_NOT_AUTOMATICALLY_INLINED", "OUTSIDE_PACKAGE_NOT_AUTHORIZED"):
            self.assertNotIn(marker, text)
        self.assertEqual(self.store.snapshot(), before)
        self.assertEqual(self.store.review_package_view(self.package_ref), page)

    def test_byte_bounded_pages_preserve_each_whole_required_version_once(self):
        sizes = [len(json_bytes({"ref": ref, "payload": self.store.public_read(ref)})) for ref in self.required]
        budget = max(1, min(sizes) + 10)
        records, pages, offset = [], [], 0
        with patch("colombo.brain.research_store.REVIEW_RECORD_BYTE_BUDGET", budget):
            while True:
                page = self.store.review_package_view(self.package_ref, offset=offset)
                pages.append(page)
                records.extend(page["required_records"])
                self.assertTrue(page["required_records"])
                if page["record_bytes"] > budget:
                    self.assertEqual(len(page["required_records"]), 1)
                    self.assertEqual(page["oversized_record"], page["required_records"][0]["ref"])
                else:
                    self.assertIsNone(page["oversized_record"])
                if page["next"] is None:
                    break
                self.assertEqual(page["next_offset"], offset + len(page["required_records"]))
                offset = page["next"]["offset"]
        self.assertGreater(len(pages), 1)
        self.assertEqual([item["ref"] for item in records], self.required)
        for item in records:
            self.assertEqual(item["payload"], self.store.public_read(item["ref"]))
        proof = next(item["payload"]["proof_draft"] for item in records if item["ref"] == self.candidate)
        self.assertEqual(proof, self.store.public_read(self.candidate)["proof_draft"])

    def test_scope_and_explicit_revision_mismatch_fail_closed(self):
        broken = copy.deepcopy(self.package)
        broken["allowed_refs"].remove(self.result["id"])
        wrong_version = copy.deepcopy(self.package)
        wrong_version["references"][2]["revision"] += 1
        duplicate = copy.deepcopy(self.package)
        duplicate["required_checked_refs"].append(self.result["id"])
        for value in (broken, wrong_version, duplicate):
            with self.subTest(value=value["required_checked_refs"]):
                package = write_review_package(self.store, value)
                with self.assertRaises(ValueError):
                    self.store.review_package_view(package)
        with self.assertRaises(ValueError):
            self.store.review_package_view({**self.package_ref, "revision": self.package_ref["revision"] + 1})

    def test_projection_uses_one_snapshot_even_if_later_history_is_appended(self):
        old_snapshot = self.store.snapshot()
        real_read = self.store._read_row
        changed = False
        def append_during_read(row, documents=None, **kwargs):
            nonlocal changed
            value = real_read(row, documents, **kwargs)
            if row["node_type"] == "review_package" and not changed:
                changed = True
                other = Store(self.store.root)
                other.write_record("note", {"text": "Concurrent history after the read snapshot"})
            return value
        with patch.object(self.store, "_read_row", side_effect=append_during_read):
            page = self.store.review_package_view(self.package_ref)
        self.assertTrue(changed)
        self.assertEqual(page, self.store.review_package_view(self.package_ref))
        self.assertGreater(self.store.get_meta("generation"), old_snapshot[1]["generation"])

    def test_paging_is_strict_and_out_of_range_offset_has_no_next(self):
        for offset, limit in ((True, 20), (1.0, 20), (-1, 20), (0, True), (0, 1.0), (0, 0), (0, 51)):
            with self.subTest(offset=offset, limit=limit), self.assertRaises(ValueError):
                self.store.review_package_view(self.package_ref, offset, limit)
        page = self.store.review_package_view(self.package_ref, 999)
        self.assertEqual(page["required_records"], [])
        self.assertIsNone(page["next"])


class ReviewPackageMCPTests(unittest.IsolatedAsyncioTestCase):
    setUp = prepare
    prepare_call = mcp_helpers.MCPServerTests.prepare_call
    connect = mcp_helpers.MCPServerTests.connect

    async def test_real_stdio_schema_paging_scope_and_review_after_aggregate_read(self):
        work = self.prepare_call("verifier", "verify-progress", "aggregate-review", review_package_ref=self.package_ref)
        async with self.connect("verifier", "verify-progress", "aggregate-review") as session:
            tools = {tool.name: tool for tool in (await session.list_tools()).tools}
            self.assertEqual(set(tools), {"read_review_package", "read_research", "read_material", "write_review"})
            fields = tools["read_review_package"].inputSchema["properties"]
            self.assertEqual(fields["offset"]["minimum"], 0)
            self.assertEqual(fields["limit"]["maximum"], 50)
            self.assertEqual(fields["limit"]["default"], 20)
            initial = await session.call_tool("read_review_package", {})
            self.assertFalse(initial.isError, mcp_helpers.error_text(initial))
            page = mcp_helpers.response_object(initial)
            self.assertEqual(page["allowed_refs"], self.package["allowed_refs"])
            self.assertEqual(page["required_records"], self.store.review_package_view(self.package_ref)["required_records"])
            collected, offset = [], 0
            while True:
                response = await session.call_tool("read_review_package", {"offset": offset, "limit": 2})
                self.assertFalse(response.isError, mcp_helpers.error_text(response))
                part = mcp_helpers.response_object(response)
                collected.extend(part["required_records"])
                if part["next"] is None:
                    break
                offset = part["next"]["offset"]
            self.assertEqual([item["ref"] for item in collected], self.required)
            for params in ({"offset": True}, {"offset": 1.0}, {"limit": True}, {"limit": 2.0}, {"limit": 51}):
                response = await session.call_tool("read_review_package", params)
                self.assertTrue(response.isError, params)
            for name in ("read_research", "read_material"):
                response = await session.call_tool(name, {"ref": self.outside["id"]})
                self.assertTrue(response.isError)
            denied = await session.call_tool("read_research", {"section": "tasks"})
            self.assertTrue(denied.isError)
            incomplete = {"review_kind":"proof", "result_ref":None, "confirmed_claims":[], "completion_status":"partial", "repair_kind":"none", "verdict": "pass", "summary": "Synthetic review", "findings": [], "checked_refs": []}
            denied = await session.call_tool("write_review", {"payload": incomplete})
            self.assertTrue(denied.isError)
            self.assertFalse((work / "submission.json").exists())
            complete = {**incomplete, "checked_refs": self.package["required_checked_refs"]}
            submitted = await session.call_tool("write_review", {"payload": complete})
            replay = await session.call_tool("write_review", {"payload": complete})
            self.assertFalse(submitted.isError, mcp_helpers.error_text(submitted))
            self.assertEqual(mcp_helpers.response_object(submitted), mcp_helpers.response_object(replay))
            self.assertIsNone(self.store.get_meta("progress_ref"))


if __name__ == "__main__":
    unittest.main()
