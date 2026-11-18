"""Shared lookup provider behavior using fake HTTP only; no real API keys or calls."""
from __future__ import annotations

import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from colombo.cell.settings import get_settings

lookup_module = importlib.import_module("colombo.shared.literature_access")


class LookupProviderTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        for name in ("SERPER_API_KEY", "JINA_API_KEY", "CELL_RUN_DIR", "CELL_ROLE",
                     "CELL_SETTINGS_FILE", "CELL_THEOREM_SEARCH_URL"):
            os.environ.pop(name, None)
        self.temp = tempfile.TemporaryDirectory(prefix=".lookup-provider-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.key_file = self.root / "keys.txt"
        self.settings = get_settings()
        self.settings["network"].update(
            search_provider="serper", reader_provider="jina",
            api_key_file=str(self.key_file), theorem_search_url="",
            connect_timeout_seconds=2, read_timeout_seconds=4,
        )
        self.settings["retrieval"].update(search_results=2, max_search_results=5)
        for verb in ("get", "post"):
            mocked = patch.object(lookup_module.requests, verb,
                                  side_effect=AssertionError("Unexpected HTTP in isolated lookup test"))
            setattr(self, verb, mocked.start())
            self.addCleanup(mocked.stop)

    def call(self, *, enabled=True, **kwargs):
        return lookup_module.lookup_with_context(
            settings=self.settings, search_enabled=enabled, **kwargs)

    def response(self, payload, *, endpoint="https://google.serper.dev/search", status=200):
        data = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
        response = MagicMock()
        response.status_code = status
        response.url = endpoint
        response.headers = {"Content-Type": "application/json"}
        response.encoding = "utf-8"
        response.iter_content.return_value = [data]
        response.__enter__.return_value = response
        response.__exit__.return_value = False
        self.post.side_effect = None
        self.post.return_value = response
        return response

    def serper_response(self):
        return self.response({"organic": [
            {"title": "A theorem", "link": "https://example.org/paper", "snippet": "An abstract.", "position": 1},
            {"title": "Another source", "link": "https://example.org/other", "snippet": "A related technique.", "position": 2},
        ]})

    def jina_response(self, content="Assume x >= 0. Then x^2 >= 0.\nProof: ..."):
        return self.response({"code": 200, "data": {
            "title": "Original theorem", "url": "https://example.org/paper",
            "content": content, "usage": {"tokens": 20},
        }}, endpoint="https://r.jina.ai/")

    def assert_no_secret(self, result, *secrets):
        serialized = json.dumps(result)
        for secret in secrets:
            self.assertNotIn(secret, serialized)

    def test_serper_query_preserves_input_and_returns_unverified_sources(self):
        os.environ["SERPER_API_KEY"] = "fake-serper-env-key"
        self.serper_response()
        query = 'finite sample variance site:arxiv.org'
        result = self.call(query=query)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["provider"], "serper")
        self.assertEqual(result["mode"], "search")
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["results"][0]["url"], "https://example.org/paper")
        self.assertEqual(result["results"][0]["content_kind"], "search_snippet")
        self.assertFalse(result["results"][0]["theorem_text_verified"])
        self.assertEqual(self.post.call_args.args, ("https://google.serper.dev/search",))
        self.assertEqual(self.post.call_args.kwargs["json"], {"q": query, "num": 2})
        self.assertEqual(self.post.call_args.kwargs["headers"]["X-API-KEY"], "fake-serper-env-key")
        self.assertEqual(self.post.call_args.kwargs["timeout"], (2, 4))
        self.assertFalse(self.post.call_args.kwargs["allow_redirects"])
        self.get.assert_not_called()
        self.assert_no_secret(result, "fake-serper-env-key")

    def test_jina_reader_preserves_source_and_full_markdown(self):
        os.environ["JINA_API_KEY"] = "fake-jina-env-key"
        content = "# Theorem\n\nAssume $x \\in [a,b]$.\n\n" + "A proof step.\n" * 400
        self.jina_response(content)
        result = self.call(url="https://example.org/paper", limit=1)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["provider"], "jina_reader")
        self.assertEqual(result["count"], 1)
        item = result["results"][0]
        self.assertEqual(item["text"], content)
        self.assertEqual(item["requested_url"], "https://example.org/paper")
        self.assertEqual(item["url"], "https://example.org/paper")
        self.assertEqual(item["content_kind"], "reader_markdown")
        self.assertEqual(item["returned_characters"], len(content))
        self.assertFalse(item["truncated"])
        self.assertFalse(item["theorem_text_verified"])
        self.assertEqual(self.post.call_args.args, ("https://r.jina.ai/",))
        self.assertEqual(self.post.call_args.kwargs["json"], {"url": "https://example.org/paper"})
        headers = self.post.call_args.kwargs["headers"]
        self.assertEqual(headers["Authorization"], "Bearer fake-jina-env-key")
        self.assertEqual(headers["Accept"], "application/json")
        self.assertEqual(headers["X-Respond-With"], "markdown")
        self.assertFalse(self.post.call_args.kwargs["allow_redirects"])
        self.assert_no_secret(result, "fake-jina-env-key")

    def test_url_takes_precedence_without_a_search_request(self):
        os.environ["JINA_API_KEY"] = "fake-jina-only-key"
        self.jina_response()
        result = self.call(query="unused query", url="https://example.org/paper")
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["mode"], "read")
        self.assertEqual(self.post.call_count, 1)
        self.assertEqual(self.post.call_args.args, ("https://r.jina.ai/",))

    def test_file_supports_inline_assignments_and_environment_override(self):
        self.key_file.write_text("SERPER_API_KEY=fake-file-serper\nJINA_API_KEY=fake-file-jina\n", encoding="utf-8")
        self.serper_response()
        result = self.call(query="theorem")
        self.assertTrue(result["ok"], result)
        self.assertEqual(self.post.call_args.kwargs["headers"]["X-API-KEY"], "fake-file-serper")
        os.environ["SERPER_API_KEY"] = "fake-override-serper"
        result = self.call(query="another theorem")
        self.assertTrue(result["ok"], result)
        self.assertEqual(self.post.call_args.kwargs["headers"]["X-API-KEY"], "fake-override-serper")
        self.assert_no_secret(result, "fake-file-serper", "fake-file-jina", "fake-override-serper")

    def test_file_supports_provider_labels_followed_by_key_line(self):
        self.key_file.write_text("\ufeff\njina:\nfake-labelled-jina\n\nserper：\nfake-labelled-serper\n", encoding="utf-8")
        self.serper_response()
        searched = self.call(query="theorem")
        self.assertTrue(searched["ok"], searched)
        self.assertEqual(self.post.call_args.kwargs["headers"]["X-API-KEY"], "fake-labelled-serper")
        self.jina_response()
        read = self.call(url="https://example.org/paper")
        self.assertTrue(read["ok"], read)
        self.assertEqual(self.post.call_args.kwargs["headers"]["Authorization"], "Bearer fake-labelled-jina")
        self.assert_no_secret(read, "fake-labelled-serper", "fake-labelled-jina")

    def test_missing_key_fails_before_http(self):
        for kwargs in ({"query": "theorem"}, {"url": "https://example.org/paper"}):
            with self.subTest(kwargs=kwargs):
                result = self.call(**kwargs)
                self.assertFalse(result["ok"])
                self.assertEqual(result["error"]["kind"], "missing_api_key")
        self.post.assert_not_called()
        self.get.assert_not_called()

    def test_blank_provider_key_cannot_consume_another_provider_assignment(self):
        self.key_file.write_text("SERPER_API_KEY=\nJINA_API_KEY=fake-other-provider-key\n", encoding="utf-8")
        result = self.call(query="theorem")
        self.assertFalse(result["ok"], result)
        self.assertEqual(result["error"]["kind"], "missing_api_key")
        self.post.assert_not_called()
        self.get.assert_not_called()
        self.assert_no_secret(result, "fake-other-provider-key")
        self.jina_response()
        read = self.call(url="https://example.org/paper")
        self.assertTrue(read["ok"], read)
        self.assertEqual(self.post.call_args.kwargs["headers"]["Authorization"], "Bearer fake-other-provider-key")

    def test_disabled_lookup_does_not_read_keys_or_request_http(self):
        with patch.object(lookup_module.Path, "read_text", side_effect=AssertionError("Disabled lookup read a file")):
            for kwargs in ({"query": "theorem"}, {"url": "https://example.org/paper"}):
                result = self.call(enabled=False, **kwargs)
                self.assertFalse(result["ok"])
                self.assertEqual(result["error"]["kind"], "search_disabled")
        self.post.assert_not_called()
        self.get.assert_not_called()

    def test_invalid_inputs_never_reach_http(self):
        for kwargs in ({"query": ""}, {"query": 42}, {"url": "file:///tmp/paper"},
                       {"url": "https://user:password@example.org/paper"},
                       {"query": "theorem", "limit": True}, {"query": "theorem", "limit": 6}):
            with self.subTest(kwargs=kwargs):
                result = self.call(**kwargs)
                self.assertFalse(result["ok"])
        self.post.assert_not_called()
        self.get.assert_not_called()

    def test_http_errors_do_not_echo_credentials_or_fall_back(self):
        os.environ["SERPER_API_KEY"] = "fake-private-token"
        for status in (401, 429, 500):
            with self.subTest(status=status):
                response = self.serper_response()
                response.status_code = status
                response.raise_for_status.side_effect = lookup_module.requests.HTTPError(
                    "Provider echoed fake-private-token", response=response)
                result = self.call(query="theorem")
                self.assertFalse(result["ok"])
                self.assertEqual(result["error"]["kind"], "http_error")
                self.assertEqual(result["error"]["status_code"], status)
                self.assert_no_secret(result, "fake-private-token")
        self.assertEqual(self.post.call_count, 3)
        self.get.assert_not_called()

    def test_authenticated_requests_reject_redirects(self):
        os.environ["SERPER_API_KEY"] = "fake-private-token"
        response = self.response(b"", status=302)
        response.headers["Location"] = "https://example.org/redirect"
        result = self.call(query="theorem")
        self.assertFalse(result["ok"], result)
        self.assertFalse(self.post.call_args.kwargs["allow_redirects"])
        self.assertEqual(self.post.call_count, 1)
        self.get.assert_not_called()
        self.assert_no_secret(result, "fake-private-token")

    def test_malformed_search_responses_are_errors_not_empty_success(self):
        os.environ["SERPER_API_KEY"] = "fake-serper-env-key"
        for payload in (b"<html>Unavailable</html>", [], {"error": "bad request"}, {"organic": "wrong type"}):
            with self.subTest(payload=payload):
                self.response(payload)
                result = self.call(query="theorem")
                self.assertFalse(result["ok"], result)
                self.assertEqual(result["error"]["kind"], "invalid_response")
        self.get.assert_not_called()

    def test_malformed_reader_response_never_claims_source_was_read(self):
        os.environ["JINA_API_KEY"] = "fake-jina-env-key"
        for payload in (b"not-json", {"data": None}, {"data": {"content": []}}, {"data": {"content": ""}}):
            with self.subTest(payload=payload):
                self.response(payload, endpoint="https://r.jina.ai/")
                result = self.call(url="https://example.org/paper")
                self.assertFalse(result["ok"], result)
                self.assertEqual(result["count"], 0)
        self.get.assert_not_called()

    def test_json_byte_limit_rejects_partial_provider_response(self):
        os.environ["SERPER_API_KEY"] = "fake-serper-env-key"
        self.settings["network"]["max_download_bytes"] = 10
        self.serper_response()
        result = self.call(query="theorem")
        self.assertFalse(result["ok"], result)
        self.assertEqual(result["error"]["kind"], "response_too_large")
        self.assertEqual(result["count"], 0)

    def test_timeout_has_safe_typed_error_and_no_automatic_retry(self):
        os.environ["JINA_API_KEY"] = "fake-private-token"
        self.post.side_effect = lookup_module.requests.Timeout("fake-private-token")
        result = self.call(url="https://example.org/paper")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["kind"], "network_timeout")
        self.assertEqual(self.post.call_count, 1)
        self.get.assert_not_called()
        self.assert_no_secret(result, "fake-private-token")

    def test_shared_context_ignores_cell_role_and_is_reset_after_call(self):
        os.environ["CELL_ROLE"] = "audit"
        os.environ["SERPER_API_KEY"] = "fake-serper-env-key"
        self.serper_response()
        result = self.call(query="theorem")
        self.assertTrue(result["ok"], result)
        self.assertEqual(os.environ["CELL_ROLE"], "audit")
        with patch.object(lookup_module, "get_settings", return_value=self.settings):
            blocked = lookup_module.lookup(query="theorem")
        self.assertFalse(blocked["ok"])
        self.assertEqual(blocked["error"]["kind"], "search_disabled")
        self.assertEqual(self.post.call_count, 1)

    def test_arxiv_and_direct_remain_explicit_keyless_backends(self):
        self.settings["network"].update(search_provider="arxiv", reader_provider="direct")
        with patch.object(lookup_module, "_arxiv_search", return_value={"provider": "arxiv", "results": []}) as arxiv:
            result = self.call(query="theorem")
            self.assertTrue(result["ok"], result)
            self.assertEqual(result["provider"], "arxiv")
            arxiv.assert_called_once_with("theorem", 2)
        response = MagicMock()
        response.url = "https://example.org/paper"
        response.status_code = 200
        response.headers = {"Content-Type": "text/plain; charset=utf-8"}
        response.encoding = "utf-8"
        response.iter_content.return_value = [b"All original source text."]
        response.__enter__.return_value = response
        response.__exit__.return_value = False
        self.get.side_effect = None
        self.get.return_value = response
        result = self.call(url="https://example.org/paper")
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["provider"], "url")
        self.assertEqual(result["results"][0]["text"], "All original source text.")
        self.assertNotIn("Authorization", self.get.call_args.kwargs["headers"])
        self.assertNotIn("X-API-KEY", self.get.call_args.kwargs["headers"])
        self.post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
