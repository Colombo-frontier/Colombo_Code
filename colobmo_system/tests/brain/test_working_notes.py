"""Free-form research notes and later-call navigation; no model calls."""
import json
import unittest

from colombo.brain.research_records import state_view
from colombo.brain.research_store import Store
import test_mcp as mcp_helpers
import test_brain_service as fixtures


class WorkingNoteTests(unittest.TestCase):
    setUp = fixtures.create_fixture
    prepare_call = mcp_helpers.MCPServerTests.prepare_call
    service = fixtures.BrainServiceTests.service

    def test_free_text_and_links_round_trip_without_promoting_research(self):
        service = self.service()
        before = self.store.snapshot()[0]
        text = "  ## An Unverified Idea\r\n\r\nTry the change of variables $u=x-y$.\n\n" \
               "- Record only new observations; see the Proof section of the linked record for the original proof.\n  "
        links = [self.seed["id"], self.result["id"]]
        ref = service.save_note(text, related_refs=links)
        payload = service.read_research(ref=ref["id"])["payload"]
        self.assertEqual(payload["text"], text)
        self.assertEqual(payload["related_refs"], links)
        self.assertEqual(payload["status"], "open")
        self.assertIsNone(payload["supersedes"])
        after = self.store.snapshot()[0]
        self.assertEqual(after["research"], before["research"])
        self.assertEqual(after["proof_draft"], before["proof_draft"])
        self.assertEqual(after["working_notes"]["entries"][ref["id"]], payload)
        self.assertIsNone(self.store.get_meta("progress_ref"))

    def test_preview_is_bounded_but_long_free_text_is_preserved(self):
        service = self.service()
        text = "A Direction Worth Pursuing\n\n" + "A new idea, retaining the formula $x^2+y^2$.\n" * 700
        ref = service.save_note(text, related_refs=[self.result["id"]])
        state = state_view(self.store)
        self.assertEqual(len(state["notes"]), 1)
        item = state["notes"][0]
        self.assertEqual(item["id"], ref["id"])
        self.assertEqual(item["revision"], ref["revision"])
        self.assertTrue(item["summary"].startswith("A Direction Worth Pursuing"))
        self.assertNotIn("\n", item["summary"])
        self.assertLessEqual(len(item["summary"]), 240)
        self.assertTrue(item["summary_truncated"])
        self.assertEqual(item["related_refs"], [self.result["id"]])
        self.assertNotIn("text", item)
        self.assertEqual(service.read_research(ref=ref["id"])["payload"]["text"], text)
        self.assertNotIn(text, json.dumps(state, ensure_ascii=False))
        overview = service.read_research()
        self.assertEqual(overview["notes"], state["notes"])
        self.assertEqual(overview["notes_next_read"], state["notes_next_read"])

    def test_current_versions_and_closed_notes_preserve_exact_history(self):
        service = self.service()
        original = service.save_note("Initial intuition", related_refs=[self.seed["id"]])
        revised = service.save_note("Revised initial intuition", related_refs=[self.result["id"]],
                                    supersedes=original["id"])
        resolved = service.save_note("This question has been resolved", status="resolved", supersedes=revised["id"])
        abandoned = service.save_note("An abandoned approach", status="abandoned")
        open_note = service.save_note("A lesson that does not require closure")
        self.assertEqual(resolved["revision"], 3)
        state = state_view(self.store)
        self.assertEqual([item["id"] for item in state["notes"]], [open_note["id"]])
        page = service.read_research(section="notes")
        self.assertEqual({item["id"] for item in page["items"]},
                         {resolved["id"], abandoned["id"], open_note["id"]})
        self.assertEqual(page["total"], 3)
        self.assertIsNone(page["next"])
        old_payload = service.read_research(ref=original["id"])["payload"]
        self.assertEqual(old_payload["text"], "Initial intuition")
        self.assertEqual(old_payload["related_refs"], [self.seed["id"]])
        middle = service.read_research(section="notes", id=revised["id"])["payload"]
        self.assertEqual(middle["supersedes"], original["id"])
        current = service.read_research(ref=resolved["id"])["payload"]
        self.assertEqual(current["supersedes"], revised["id"])

    def test_context_limits_recent_notes_and_navigation_reaches_the_rest(self):
        service = self.service()
        saved = [service.save_note(f"Independent idea {index}", related_refs=[self.result["id"]])
                 for index in range(25)]
        state = state_view(self.store)
        self.assertEqual(len(state["notes"]), 20)
        self.assertEqual([item["id"] for item in state["notes"]],
                         [ref["id"] for ref in reversed(saved[-20:])])
        self.assertEqual(state["notes_next_read"], {"section": "notes", "offset": 0, "limit": 20})
        page = service.read_research(**state["notes_next_read"])
        seen = []
        while True:
            seen.extend(item["id"] for item in page["items"])
            self.assertEqual(page["total"], 25)
            if page["next"] is None:
                break
            page = service.read_research(**page["next"])
        self.assertEqual(seen, [ref["id"] for ref in reversed(saved)])
        self.assertEqual(len(seen), len(set(seen)))
        self.assertEqual(self.store.reference_count("note"), 25)

    def test_later_invocation_and_reopened_store_read_saved_note(self):
        initial = self.service(stage="plan", call_id="notes-first-call")
        ref = initial.save_note("An idea worth revisiting when processing subsequent results", related_refs=[self.result["id"]])
        later = self.service(stage="process_results", call_id="notes-later-call")
        state = state_view(later.store)
        self.assertEqual(state["notes"][0]["id"], ref["id"])
        self.assertFalse(state["notes"][0]["summary_truncated"])
        reopened = Store(self.store.root)
        self.assertEqual(state_view(reopened)["notes"], state["notes"])
        self.assertEqual(later.read_research(ref=ref["id"])["payload"]["call_id"], "notes-first-call")
        exported = reopened.export_documents()
        saved = json.loads((self.store.root / "working_notes.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["entries"], exported["working_notes"]["entries"])
        self.assertEqual(saved["entries"][ref["id"]]["text"], "An idea worth revisiting when processing subsequent results")

    def test_invalid_relationships_and_inactive_call_do_not_write_anything(self):
        service = self.service()
        for arguments in ({"text": "Conjecture", "related_refs": [self.result["id"], "missing-note"]},
                          {"text": "Conjecture", "related_refs": self.result["id"]},
                          {"text": "Conjecture", "related_refs": [self.result]},
                          {"text": "Conjecture", "supersedes": self.result["id"]},
                          {"text": "Conjecture", "supersedes": ""},
                          {"text": "Conjecture", "status": "proved"},
                          {"text": "Conjecture", "status": []},
                          {"text": None},
                          {"text": "  \n\t"}):
            before = self.store.snapshot()
            with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                service.save_note(**arguments)
            self.assertEqual(self.store.snapshot(), before)
        self.store.set_meta(pending_call={"call_id": "replacement-call"})
        before = self.store.snapshot()
        with self.assertRaises(ValueError):
            service.save_note("Note from an expired session")
        self.assertEqual(self.store.snapshot(), before)


class WorkingNoteMCPTests(unittest.IsolatedAsyncioTestCase):
    setUp = mcp_helpers.MCPServerTests.setUp
    prepare_call = mcp_helpers.MCPServerTests.prepare_call
    connect = mcp_helpers.MCPServerTests.connect

    async def test_real_stdio_tool_accepts_free_text_and_only_requires_text(self):
        self.prepare_call("brain", "plan", "free-note-mcp")
        async with self.connect("brain", "plan", "free-note-mcp") as session:
            tools = {tool.name: tool for tool in (await session.list_tools()).tools}
            schema = tools["save_note"].inputSchema
            self.assertEqual(schema["required"], ["text"])
            self.assertEqual(set(schema["properties"]), {"text", "related_refs", "status", "supersedes"})
            text = "\n## Free-form Notes\nThis is only an idea to be verified: $f(x)=x^2$.\n"
            saved = await session.call_tool("save_note", {"text": text, "related_refs": [self.material_ref["id"]]})
            self.assertFalse(saved.isError, mcp_helpers.error_text(saved))
            ref = mcp_helpers.response_object(saved)
            read = await session.call_tool("read_research", {"ref": ref["id"]})
            self.assertFalse(read.isError, mcp_helpers.error_text(read))
            payload = mcp_helpers.response_object(read)["payload"]
            self.assertEqual(payload["text"], text)
            self.assertEqual(payload["related_refs"], [self.material_ref["id"]])
            self.assertEqual(payload["status"], "open")
            self.assertIsNone(payload["supersedes"])
            directory = await session.call_tool("read_research", {"section": "notes"})
            self.assertFalse(directory.isError, mcp_helpers.error_text(directory))
            item = mcp_helpers.response_object(directory)["items"][0]
            self.assertEqual(item["id"], ref["id"])
            self.assertTrue(item["summary"])
            self.assertNotIn("text", item)


if __name__ == "__main__":
    unittest.main()
