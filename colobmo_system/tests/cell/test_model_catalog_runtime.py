"""Explicit native model catalogs validate before startup; no real model calls."""
from __future__ import annotations

from contextlib import ExitStack
import json
import os
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import colombo.cell.model_calls as processes
import colombo.cell.settings as settings


ROOT = Path(__file__).resolve().parents[2]


class ModelCatalogRuntimeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".model-catalog-test-", dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.assertTrue(self.root.is_relative_to(ROOT.resolve()))
        self.auth = self.root / "auth"
        self.auth.mkdir()
        (self.auth / "auth.json").write_text("not a real credential", encoding="utf-8")
        self.work = self.root / "work"
        self.work.mkdir()
        self.catalog = self.root / "catalog.json"
        self.selected, _ = settings.load_defaults(profile="standard")
        self.selected["model"].update(name="chosen-model", reasoning_effort="medium")
        self.payload = {"models": [{"slug": "chosen-model", "display_name": "Fixture",
            "supported_reasoning_levels": [{"effort": "medium", "description": "Fixture"}]}]}
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.object(processes, "ROOT", self.root / "runtime"))
        self.stack.enter_context(patch.object(processes, "_user_home", return_value=self.auth))
        self.stack.enter_context(patch.dict(os.environ))
        os.environ.pop("CELL_MODEL_CATALOG_JSON", None)

    def enable(self, payload=None):
        self.catalog.write_text(json.dumps(self.payload if payload is None else payload, indent=2) + "\n",
                                encoding="utf-8")
        os.environ["CELL_MODEL_CATALOG_JSON"] = str(self.catalog)

    def prepare(self, role="prover", recovery_only=False):
        home = processes._prepare_home(self.work, role, None, False, {}, settings=self.selected,
                                       recovery_only=recovery_only)
        config = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
        self.assertEqual(config["model"], "chosen-model")
        self.assertEqual(config["model_reasoning_effort"], "medium")
        self.assertEqual(json.loads((home / "settings.json").read_text(encoding="utf-8")), self.selected)
        return home, config

    def test_default_is_dynamic_and_all_explicit_roles_get_private_exact_copies(self):
        home, config = self.prepare()
        self.assertNotIn("model_catalog_json", config)
        self.assertFalse((home / "model_catalog.json").exists())
        self.enable()
        original = self.catalog.read_bytes()
        source_mtime = self.catalog.stat().st_mtime_ns
        homes = []
        for role, recovery in (("prover", False), ("subcell", False), ("verifier", False),
                               ("audit", False), ("prover", True)):
            with self.subTest(role=role, recovery=recovery):
                home, config = self.prepare(role, recovery)
                homes.append(home)
                self.assertEqual(Path(config["model_catalog_json"]), home / "model_catalog.json")
                self.assertEqual((home / "model_catalog.json").read_bytes(), original)
                if role != "audit" and not recovery:
                    forwarded = config["mcp_servers"]["research"]["env"]["CELL_MODEL_CATALOG_JSON"]
                    self.assertEqual(forwarded, str(self.catalog))
                    self.assertNotEqual(forwarded, config["model_catalog_json"])
        self.assertEqual(len(set(homes)), len(homes))
        self.assertEqual(self.catalog.read_bytes(), original)
        self.assertEqual(self.catalog.stat().st_mtime_ns, source_mtime)

    def test_filtered_mcp_environment_preserves_source_for_nested_audit(self):
        self.enable()
        parent_home, parent_config = self.prepare()
        environment = parent_config["mcp_servers"]["research"]["env"]
        with patch.dict(os.environ, environment, clear=True):
            child_home, child_config = self.prepare("audit")
        self.assertNotEqual(parent_home, child_home)
        self.assertEqual((child_home / "model_catalog.json").read_bytes(), self.catalog.read_bytes())
        self.assertNotIn("mcp_servers", child_config)

    def test_invalid_catalog_or_model_and_effort_mismatch_fail_closed(self):
        invalid = [b'{broken', b'\xff', b'[]', b'{"models":[]}', b'{"models":[1]}',
                   b'{"models":[{"slug":""}]}',
                   json.dumps({"models": [self.payload["models"][0]] * 2}).encode(),
                   b'{"models":[{"slug":"other-model"}]}',
                   b'{"models":[{"slug":"chosen-model"}]}',
                   b'{"models":[{"slug":"chosen-model","supported_reasoning_levels":[{"effort":"high"}]}]}',
                   json.dumps(self.payload).encode() + b' ' * (5 * 1024 * 1024)]
        os.environ["CELL_MODEL_CATALOG_JSON"] = str(self.catalog)
        with patch.object(processes.subprocess, "Popen") as launch:
            for data in invalid:
                with self.subTest(prefix=data[:70]):
                    self.catalog.write_bytes(data)
                    with self.assertRaisesRegex(processes.AgentError, "Explicit model catalog"):
                        self.prepare()
            self.catalog.unlink()
            with self.assertRaisesRegex(processes.AgentError, "existing ordinary"):
                self.prepare()
            self.catalog.mkdir()
            with self.assertRaisesRegex(processes.AgentError, "existing ordinary"):
                self.prepare()
            os.environ["CELL_MODEL_CATALOG_JSON"] = "relative-catalog.json"
            with self.assertRaisesRegex(processes.AgentError, "absolute"):
                self.prepare()
            launch.assert_not_called()

    def test_explicit_catalog_copy_failure_is_not_silently_ignored(self):
        self.enable()
        with patch("colombo.shared.model_launcher.atomic_write", side_effect=PermissionError("fixture denied")):
            with self.assertRaisesRegex(processes.AgentError, "fixture denied"):
                self.prepare()


if __name__ == "__main__":
    unittest.main()
