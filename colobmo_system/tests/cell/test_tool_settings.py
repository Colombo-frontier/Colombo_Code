"""Exercise tool behavior with a non-default central configuration snapshot."""
from __future__ import annotations

import copy
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from colombo.cell.settings import get_settings
from colombo.cell.record_store import Store
from colombo.cell.record_store import StoreError

lookup_module = importlib.import_module("colombo.shared.literature_access")


class ToolSettingsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.settings = copy.deepcopy(get_settings())
        self.settings["retrieval"].update(
            search_results=2, verifier_search_results=2, max_search_results=3,
            memory_results=2, verifier_memory_results=2, max_memory_results=3,
            include_context=False, verifier_reverse=False,
        )
        self.settings["network"].update(
            connect_timeout_seconds=2, read_timeout_seconds=4,
            max_download_bytes=8, chunk_bytes=3, html_max_links=2,
            query_max_chars=5, arxiv_interval_seconds=7,
            theorem_search_url="", search_provider="arxiv", reader_provider="direct",
        )
        self.settings["runtime"].update(store_lock_timeout_seconds=2, lock_poll_seconds=0.01)
        self.settings["limits"].update(
            record_id_max_chars=32, request_id_max_chars=4,
        )
        snapshot = self.root / "settings.json"
        snapshot.write_text(json.dumps(self.settings), encoding="utf-8")
        env = patch.dict(os.environ, {"CELL_SETTINGS_FILE": str(snapshot)})
        env.start()
        self.addCleanup(env.stop)

    def test_download_uses_configured_timeouts_chunk_and_byte_cap(self):
        response = Mock()
        response.url = "https://example.invalid/paper"
        response.headers = {"Content-Type": "text/plain"}
        response.encoding = "utf-8"
        response.iter_content.return_value = [b"abc", b"def", b"ghi"]
        context = Mock()
        context.__enter__ = Mock(return_value=response)
        context.__exit__ = Mock(return_value=False)
        with patch.object(lookup_module.requests, "get", return_value=context) as get:
            result = lookup_module._request(response.url)
        self.assertEqual(get.call_args.kwargs["timeout"], (2, 4))
        response.iter_content.assert_called_once_with(chunk_size=3)
        self.assertEqual(result["data"], b"abcdefgh")
        self.assertTrue(result["download_truncated"])

    def test_search_defaults_and_limits_use_snapshot(self):
        fake = {"results": [], "warnings": []}
        with patch.object(lookup_module, "_arxiv_search", return_value=fake) as search:
            self.assertTrue(lookup_module.lookup(query="lemma")["ok"])
            search.assert_called_once_with("lemma", 2)
            self.assertFalse(lookup_module.lookup(query="lemma", limit=4)["ok"])
            self.assertFalse(lookup_module.lookup(query="longer")["ok"])
            self.assertEqual(search.call_count, 1)

    def test_pacing_and_html_link_cap_use_snapshot(self):
        with patch.object(lookup_module, "_last_arxiv_request", 10), \
                patch.object(lookup_module.time, "monotonic", return_value=12), \
                patch.object(lookup_module.time, "sleep") as sleep:
            lookup_module._pace_arxiv()
            sleep.assert_called_once_with(5)
        parser = lookup_module._HTMLText("https://example.invalid/")
        parser.feed('<p>Complete text</p><a href="a">A</a><a href="b">B</a><a href="c">C</a>')
        result = parser.result()
        self.assertEqual(len(result["links"]), 2)
        self.assertIn("C", result["text"])

    def test_store_uses_limits_defaults_and_context_policy(self):
        store = Store(self.root / "run" / "memory")
        self.assertEqual(store.lock_timeout, 2)
        for i in range(3):
            store.archive("claims", {"statement": f"claim {i}"}, f"C{i}")
        self.assertEqual(store.retrieve()["returned"], 2)
        with self.assertRaises(StoreError):
            store.retrieve(limit=4)
        with self.assertRaises(StoreError):
            store.archive("claims", {}, "x" * 33)
        with self.assertRaises(StoreError):
            store.archive("claims", {}, "valid", request_id="12345")
        with self.assertRaises(StoreError):
            store.archive("claims", {}, "../escape")
        context_record = copy.deepcopy(store.get("claims", "C0"))
        context_record.update(id="Context", origin="context", read_only=True)
        store._context[("claims", "Context", 1)] = context_record
        self.assertEqual(store.retrieve(kinds=["claims"])["count"], 3)
        self.assertEqual(store.retrieve(kinds=["claims"], include_context=True)["count"], 4)

    def test_verifier_search_and_review_retrieval_settings(self):
        with patch.dict(os.environ, {"CELL_ROLE": "verifier"}):
            verifier = importlib.import_module("colombo.cell.verifier.mcp_server")
        with patch.object(verifier, "RUN", self.root / "verifier"):
            with patch.object(verifier, "lookup", return_value={"results": []}) as search:
                verifier.lookup_sources("lemma")
                self.assertEqual(search.call_args.kwargs["limit"], 2)
                with self.assertRaises(ValueError):
                    verifier.lookup_sources("lemma", limit=99)
                search.assert_called_once()
            for i in range(3):
                verifier.record_check(i + 1, "pass", f"Checked step {i + 1}", f"Step {i + 1}", "draft.md")
            result = verifier.read_review(detail="full")
            self.assertEqual([r["id"] for r in result["checks"]], [1, 2])
            self.assertTrue(result["truncated"])
            self.assertEqual(result["totals"]["checks"], 3)
            with self.assertRaises(ValueError):
                verifier.read_review(limit=4)


if __name__ == "__main__":
    unittest.main()
