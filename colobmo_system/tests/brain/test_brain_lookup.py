"""Shared source lookup and fixed material delivery; providers are mocked."""
from brain_fixtures import write_review_package
import copy
import json
import unittest
from unittest.mock import patch

from colombo.configuration import load_config
from colombo.brain.cell_package import build_package
from colombo.brain.mcp_server import AgentService
from colombo.brain.research_store import Store
import test_mcp as helpers
import test_brain_service as fixtures


SOURCE = {
    "ok": True, "mode": "read", "provider": "jina_reader", "count": 1,
    "warnings": ["Check the original theorem and assumptions."],
    "results": [{"url": "https://example.org/paper", "title": "Source theorem",
        "text": "# Source theorem\nA deliberately distinctive original proof body.\n",
        "content_kind": "reader_text", "retrieved_at": "2000-01-01T00:00:00Z",
        "truncated": False, "truncation_reasons": []}],
}


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


class BrainLookupTests(unittest.TestCase):
    setUp = fixtures.create_fixture
    prepare_call = helpers.MCPServerTests.prepare_call
    service = fixtures.BrainServiceTests.service

    def test_read_source_is_fixed_material_and_packages_body_without_json_copy(self):
        service = self.service(stage="plan")
        with patch("colombo.brain.mcp_server._lookup_sources", return_value=copy.deepcopy(SOURCE)) as provider:
            result = service.lookup(url="https://example.org/paper")
        args = provider.call_args
        self.assertEqual(args.kwargs["settings"], self.store.get_meta("config")["cell"]["settings"])
        self.assertIs(args.kwargs["search_enabled"], True)
        ref, artifact = result["material_ref"], result["artifact"]
        self.assertEqual(self.store.record_kind(ref), "material")
        self.assertEqual(set(ref), {"id", "revision"})
        self.assertEqual(service.read_material(ref["id"])["text"], SOURCE["results"][0]["text"])
        payload = service.read_research(ref=ref["id"])["payload"]
        self.assertFalse(payload["theorem_text_verified"])
        self.assertEqual(payload["source_info"]["retrieved_at"], SOURCE["results"][0]["retrieved_at"])
        self.assertNotIn(SOURCE["results"][0]["text"], list(strings(self.store.snapshot()[0])))
        self.assertIsNone(self.store.get_meta("progress_ref"))
        package = {"background": "Use a discovered source", "selection_reason": "Relevant assumptions",
            "items": [{"ref": ref["id"], "importance": "required", "purpose": "Check applicability",
                       "limitations": "Retrieved text has not been audited"}]}
        destination = self.store.root / "tasks/T0002/input/package"
        manifest = build_package(self.store, "T0002", {"package": package}, destination)
        entry = manifest["items"][0]
        self.assertEqual(entry["source_ref"], ref)
        self.assertEqual(entry["artifacts"][0]["source_path"], artifact["path"])
        self.assertEqual((destination / entry["artifacts"][0]["package_path"]).read_text(encoding="utf-8"),
                         SOURCE["results"][0]["text"])
        self.store.export_documents()
        restored = Store(self.store.root)
        self.assertEqual(restored.read_artifact(ref)["text"], SOURCE["results"][0]["text"])
        exported = json.loads((self.store.root / "research.json").read_text(encoding="utf-8"))
        self.assertNotIn(SOURCE["results"][0]["text"], list(strings(exported)))

    def test_search_and_error_do_not_create_materials(self):
        service = self.service(stage="process_results")
        before = self.store.reference_count("material")
        for result in ({"ok": True, "mode": "search", "results": [{"url": "https://example.org"}]},
                       {"ok": False, "mode": "read", "results": [], "error": {"kind": "network_error"}}):
            with patch("colombo.brain.mcp_server._lookup_sources", return_value=result):
                self.assertEqual(service.lookup(query="a theorem"), result)
        self.assertEqual(self.store.reference_count("material"), before)

    def test_frozen_brain_switch_is_independent_of_cell_search(self):
        service = self.service(stage="process_results")
        config = self.store.get_meta("config")
        config["brain"]["search_enabled"] = False
        config["cell"]["settings"]["network"]["prover_search_enabled"] = True
        self.store.set_meta(config=config)
        with patch("colombo.brain.mcp_server._lookup_sources") as provider:
            result = service.lookup(query="a theorem")
            self.assertEqual(result["error"]["kind"], "search_disabled")
            provider.assert_not_called()
        config["brain"]["search_enabled"] = True
        config["cell"]["settings"]["network"]["prover_search_enabled"] = False
        self.store.set_meta(config=config)
        with patch("colombo.brain.mcp_server._lookup_sources", return_value={"ok": True, "mode": "search"}) as provider:
            self.assertTrue(service.lookup(query="a theorem")["ok"])
            self.assertIs(provider.call_args.kwargs["search_enabled"], True)

    def test_retired_call_and_verifier_cannot_request_lookup(self):
        service = self.service(stage="process_results")
        self.store.set_meta(pending_call=None)
        with patch("colombo.brain.mcp_server._lookup_sources") as provider, self.assertRaisesRegex(ValueError, "active"):
            service.lookup(query="a theorem")
        provider.assert_not_called()
        package = write_review_package(self.store, {"allowed_refs": [self.seed["id"]],
            "required_checked_refs": [self.seed["id"]]})
        self.prepare_call("verifier", "verify-progress", "lookup-review", review_package_ref=package)
        reviewer = AgentService(self.store.root, "verifier", "verify-progress", "lookup-review")
        with patch("colombo.brain.mcp_server._lookup_sources") as provider, self.assertRaisesRegex(ValueError, "Brain only"):
            reviewer.lookup(query="a theorem")
        provider.assert_not_called()

    def test_call_retired_during_network_does_not_save_source(self):
        service = self.service(stage="process_results")
        def finish(*args, **kwargs):
            self.store.set_meta(pending_call=None)
            return copy.deepcopy(SOURCE)
        with patch("colombo.brain.mcp_server._lookup_sources", side_effect=finish), self.assertRaisesRegex(ValueError, "active"):
            service.lookup(url="https://example.org/paper")
        self.assertEqual(self.store.reference_count("material"), 0)
        self.assertEqual(list((self.store.root / "input/materials").glob("lookup-*.txt")), [])

    def test_call_retired_at_material_commit_removes_unregistered_artifact(self):
        service = self.service(stage="process_results")
        commit = service.store.write_lookup_material
        def retire(call_id, payload):
            self.store.set_meta(pending_call=None)
            return commit(call_id, payload)
        with patch("colombo.brain.mcp_server._lookup_sources", return_value=copy.deepcopy(SOURCE)), \
                patch.object(service.store, "write_lookup_material", side_effect=retire), \
                self.assertRaisesRegex(ValueError, "active"):
            service.lookup(url="https://example.org/paper")
        self.assertEqual(self.store.reference_count("material"), 0)
        self.assertEqual(list((self.store.root / "input/materials").glob("lookup-*.txt")), [])

    def test_new_read_creates_new_fixed_material_without_changing_old_source(self):
        service = self.service(stage="process_results")
        with patch("colombo.brain.mcp_server._lookup_sources", return_value=copy.deepcopy(SOURCE)):
            first = service.lookup(url="https://example.org/paper")
        changed = copy.deepcopy(SOURCE)
        changed["results"][0]["text"] = "Changed source text."
        with patch("colombo.brain.mcp_server._lookup_sources", return_value=changed):
            second = service.lookup(url="https://example.org/paper")
        self.assertNotEqual(first["material_ref"], second["material_ref"])
        self.assertEqual(service.read_material(first["material_ref"]["id"])["text"], SOURCE["results"][0]["text"])
        self.assertEqual(service.read_material(second["material_ref"]["id"])["text"], "Changed source text.")

    def test_brain_search_config_rejects_non_boolean(self):
        from colombo.configuration import PROJECT_ROOT
        original = (PROJECT_ROOT / "config.toml").read_text(encoding="utf-8")
        for value in ('"true"', "1"):
            path = self.folder / "invalid.toml"
            path.write_text(original.replace("search_enabled = true", "search_enabled = " + value, 1), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "search_enabled"):
                load_config(path)


if __name__ == "__main__":
    unittest.main()
