"""Optional model-cache seeding preserves isolated configuration; no model calls."""
from __future__ import annotations

from contextlib import ExitStack
import json
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import colombo.cell.model_calls as processes
import colombo.cell.settings as settings


ROOT = Path(__file__).resolve().parents[2]


class ModelsCacheRuntimeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".models-cache-test-", dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.assertTrue(self.root.is_relative_to(ROOT.resolve()))
        self.auth = self.root / "auth"
        self.auth.mkdir()
        (self.auth / "auth.json").write_text("test fixture; not a real credential", encoding="utf-8")
        self.cache = self.auth / "models_cache.json"
        self.work = self.root / "work"
        self.work.mkdir()
        self.selected, _ = settings.load_defaults(profile="standard")
        self.selected["model"].update(name="configured-model", reasoning_effort="medium")
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.object(processes, "ROOT", self.root / "runtime"))
        self.stack.enter_context(patch.object(processes, "_user_home", return_value=self.auth))

    def prepare(self, role="prover"):
        home = processes._prepare_home(self.work, role, None, False,
                                       {"CELL_PROCESS_ID": "fixed-process-id"}, settings=self.selected)
        config = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
        self.assertEqual(config["model"], "configured-model")
        self.assertEqual(config["model_reasoning_effort"], "medium")
        self.assertEqual(json.loads((home / "settings.json").read_text(encoding="utf-8")), self.selected)
        self.assertNotIn("model_catalog_json", config)
        if role == "prover":
            env = config["mcp_servers"]["research"]["env"]
            self.assertEqual(env["CELL_AUTH_HOME"], str(self.auth))
            self.assertEqual(env["CELL_PROCESS_ID"], "fixed-process-id")
            self.assertEqual(Path(env["CELL_SETTINGS_FILE"]), home / "settings.json")
        return home

    def test_complete_cache_is_copied_byte_for_byte_into_independent_homes(self):
        raw = (b'{\r\n  "fetched_at":"2024-01-01T00:00:00Z", "client_version":"old", '
               b'"identity":{"account":"fixture"}, "models":[{"slug":"cached-other-model", '
               b'"nested":{"capability":[1,true]}}], "future_field":"preserved"\r\n}\r\n')
        self.cache.write_bytes(raw)
        source_mtime = self.cache.stat().st_mtime_ns
        first, second = self.prepare(), self.prepare("audit")
        self.assertNotEqual(first, second)
        self.assertEqual((first / "models_cache.json").read_bytes(), raw)
        self.assertEqual((second / "models_cache.json").read_bytes(), raw)
        (first / "models_cache.json").write_bytes(b'{"models":[]}')
        self.assertEqual((second / "models_cache.json").read_bytes(), raw)
        self.assertEqual(self.cache.read_bytes(), raw)
        self.assertEqual(self.cache.stat().st_mtime_ns, source_mtime)
        self.assertFalse((first / "auth.json").exists())  # Existing credential-copy timing is unchanged.

    def test_missing_bad_or_oversized_cache_does_not_change_configuration(self):
        for data in (None, b'{broken', b'\xff', b'[]', b'{}', b'{"models":{}}',
                     b'{"models":[]}' + b' ' * (5 * 1024 * 1024)):
            with self.subTest(kind="missing" if data is None else repr(data[:25])):
                self.cache.unlink(missing_ok=True)
                if data is not None:
                    self.cache.write_bytes(data)
                home = self.prepare()
                self.assertFalse((home / "models_cache.json").exists())
                if data is not None:
                    self.assertEqual(self.cache.read_bytes(), data)

    def test_cache_read_failure_is_optional(self):
        self.cache.mkdir()  # Opening a directory as a cache file raises OSError.
        home = self.prepare()
        self.assertFalse((home / "models_cache.json").exists())

    def test_cache_write_failure_is_optional_and_source_unchanged(self):
        raw = b'{"models":[],"fetched_at":"unchanged","client_version":"fixture"}'
        self.cache.write_bytes(raw)
        with patch("colombo.shared.model_launcher.atomic_write", side_effect=PermissionError("test write denial")):
            home = self.prepare()
        self.assertFalse((home / "models_cache.json").exists())
        self.assertEqual(self.cache.read_bytes(), raw)


if __name__ == "__main__":
    unittest.main()
