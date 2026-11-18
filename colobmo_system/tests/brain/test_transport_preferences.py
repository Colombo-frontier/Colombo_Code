"""Isolated startup preserves explicit transport choices without model calls."""
from __future__ import annotations

from contextlib import ExitStack
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch


PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from colombo.brain.model_calls import BackendError, CodexBackend
from colombo.cell import model_calls as cell_calls
from colombo.cell.settings import load_defaults
from colombo.configuration import load_config


MISSING = object()
BRAIN_ROLES = (("brain", False), ("verifier", False), ("audit", False))
CELL_ROLES = (("prover", False), ("subcell", False), ("verifier", False),
              ("audit", False), ("prover", True))


class TransportPreferenceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="colombo transport preferences ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.auth = self.root / "source-auth"
        self.auth.mkdir()
        (self.auth / "auth.json").write_text('{"fixture":"not-a-real-credential"}', encoding="utf-8")
        self.ambient = self.root / "ambient-auth"
        self.ambient.mkdir()
        (self.ambient / "auth.json").write_text('{"fixture":"other-source"}', encoding="utf-8")
        (self.ambient / "config.toml").write_text(
            '[features]\nrespect_system_proxy = false\n', encoding="utf-8")
        self.work = self.root / "work"
        self.work.mkdir()
        self.config = load_config()
        self.config["runtime"]["auth_home"] = str(self.auth)
        for role in ("brain", "verifier", "audit"):
            self.config[role].update(model="", reasoning_effort="")
        self.backend = CodexBackend(PROJECT, self.config)
        self.selected, _ = load_defaults(profile="standard")
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(os.environ, {
            "CELL_AUTH_HOME": str(self.auth), "CODEX_HOME": str(self.ambient),
            "OPENAI_API_KEY": "",
        }))
        os.environ.pop("CELL_MODEL_CATALOG_JSON", None)
        self.stack.enter_context(patch.object(cell_calls, "ROOT", self.root / "cell-runtime"))
        self.stack.enter_context(patch("colombo.brain.model_calls.managed_popen",
                                      side_effect=AssertionError("No model process is permitted")))
        self.stack.enter_context(patch.object(cell_calls.subprocess, "Popen",
                                      side_effect=AssertionError("No model process is permitted")))
        self.counter = 0

    def write_preferences(self, proxy=MISSING, websocket=MISSING, *, features_raw=None):
        lines = ['model = "configured-model"', 'model_reasoning_effort = "medium"',
                 'model_provider = "fixture.provider"']
        if features_raw is not None:
            lines.append("features = " + features_raw)
        lines += ['[model_providers."fixture.provider"]', 'name = "Fixture provider"',
                  'base_url = "https://example.invalid/v1"', 'wire_api = "responses"',
                  'requires_openai_auth = true', 'env_key = "FIXTURE_PROVIDER_KEY_NAME"',
                  'http_headers = { Authorization = "fixture-header-must-not-be-copied" }']
        if websocket is not MISSING:
            lines.append("supports_websockets = " + json.dumps(websocket))
        lines += ['[model_providers.unselected]', 'name = "Unselected provider"',
                  'env_key = "UNSELECTED_PROVIDER_KEY_MUST_NOT_BE_COPIED"']
        if features_raw is None:
            lines += ['[features]', 'apps = true', 'plugins = true', 'hooks = true',
                      'multi_agent = true', 'multi_agent_v2 = true']
            if proxy is not MISSING:
                lines.append("respect_system_proxy = " + json.dumps(proxy))
        lines += ['[mcp_servers.unrelated]', 'command = "unrelated-server-must-not-be-copied"']
        (self.auth / "config.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def source_snapshot(self):
        return {p.name: p.read_bytes() for p in self.auth.iterdir() if p.is_file()}

    def prepare(self, caller, role, recovery=False, *, model=None):
        self.counter += 1
        before = self.source_snapshot()
        if caller == "brain":
            home = self.root / ("brain-home-" + str(self.counter))
            selected = self.backend._settings(role)
            if model is not None:
                selected["model"] = model
            original, _ = self.backend._prepare_home(
                home, role, "audit" if role == "audit" else "plan" if role == "brain" else "verify-progress",
                self.root / "run", self.work, "fixture-" + str(self.counter), selected,
                enable_mcp=role != "audit")
            self.assertEqual(original, self.auth.resolve())
        else:
            selected = deepcopy(self.selected)
            home = cell_calls._prepare_home(self.work, role, model, False, {},
                                            settings=selected, recovery_only=recovery)
        self.assertEqual(before, self.source_snapshot())
        text = (home / "config.toml").read_text(encoding="utf-8")
        return home, tomllib.loads(text), text

    def roles(self):
        return [("brain", role, recovery) for role, recovery in BRAIN_ROLES] + [
                ("cell", role, recovery) for role, recovery in CELL_ROLES]

    def test_true_and_false_proxy_preferences_reach_every_isolated_role(self):
        for value in (True, False):
            self.write_preferences(proxy=value)
            for caller, role, recovery in self.roles():
                with self.subTest(value=value, caller=caller, role=role, recovery=recovery):
                    _, config, _ = self.prepare(caller, role, recovery)
                    self.assertIs(config["features"]["respect_system_proxy"], value)

    def test_omitted_proxy_is_not_invented(self):
        self.write_preferences()
        for caller, role, recovery in self.roles():
            with self.subTest(caller=caller, role=role, recovery=recovery):
                _, config, _ = self.prepare(caller, role, recovery)
                self.assertNotIn("respect_system_proxy", config["features"])

    def test_malformed_proxy_values_fail_before_creating_runtime_homes(self):
        for raw in ('"true"', '"false"', "0", "1", "[]", "{}"):
            text = ('model = "configured-model"\n[features]\n'
                    'respect_system_proxy = ' + raw + "\n")
            (self.auth / "config.toml").write_text(text, encoding="utf-8")
            for caller, error in (("brain", BackendError), ("cell", cell_calls.AgentError)):
                with self.subTest(raw=raw, caller=caller):
                    homes = sorted(str(p) for p in self.root.rglob("config.toml"))
                    with self.assertRaisesRegex(error, "respect_system_proxy.*boolean"):
                        self.prepare(caller, "brain" if caller == "brain" else "prover")
                    self.assertEqual(homes, sorted(str(p) for p in self.root.rglob("config.toml")))

    def test_malformed_features_table_is_rejected(self):
        for raw in ('"false"', "false", "1", "[]"):
            self.write_preferences(features_raw=raw)
            for caller, error in (("brain", BackendError), ("cell", cell_calls.AgentError)):
                with self.subTest(raw=raw, caller=caller):
                    with self.assertRaisesRegex(error, "features.*table"):
                        self.prepare(caller, "brain" if caller == "brain" else "prover")

    def test_websocket_true_and_false_reach_selected_provider_for_every_role(self):
        for value in (True, False):
            self.write_preferences(websocket=value)
            for caller, role, recovery in self.roles():
                with self.subTest(value=value, caller=caller, role=role, recovery=recovery):
                    _, config, _ = self.prepare(caller, role, recovery)
                    self.assertEqual(config["model_provider"], "fixture.provider")
                    self.assertIs(config["model_providers"]["fixture.provider"]["supports_websockets"], value)

    def test_omitted_websocket_preference_is_not_invented(self):
        self.write_preferences()
        for caller, role, recovery in self.roles():
            with self.subTest(caller=caller, role=role, recovery=recovery):
                _, config, _ = self.prepare(caller, role, recovery)
                self.assertNotIn("supports_websockets", config["model_providers"]["fixture.provider"])

    def test_auth_and_model_precedence_remain_intact(self):
        self.write_preferences(proxy=True, websocket=False)
        for caller in ("brain", "cell"):
            with self.subTest(caller=caller):
                _, config, _ = self.prepare(caller, "brain" if caller == "brain" else "prover",
                                             model="explicit-model")
                self.assertIs(config["features"]["respect_system_proxy"], True)
                self.assertEqual(config["model"], "explicit-model")
                self.assertEqual(config["model_reasoning_effort"], "medium")
        self.assertNotEqual(self.auth.resolve(), self.ambient.resolve())

    def test_only_approved_transport_fields_are_inherited(self):
        self.write_preferences(proxy=True, websocket=False)
        for caller, role, recovery in self.roles():
            with self.subTest(caller=caller, role=role, recovery=recovery):
                _, config, text = self.prepare(caller, role, recovery)
                for feature in ("apps", "plugins", "hooks", "multi_agent", "multi_agent_v2"):
                    self.assertIs(config["features"][feature], False)
                self.assertFalse(config["agents"]["enabled"])
                self.assertEqual(set(config["model_providers"]), {"fixture.provider"})
                self.assertNotIn("http_headers", config["model_providers"]["fixture.provider"])
                self.assertNotIn("unrelated", config.get("mcp_servers", {}))
                for marker in ("fixture-header-must-not-be-copied", "unrelated-server-must-not-be-copied",
                               "UNSELECTED_PROVIDER_KEY_MUST_NOT_BE_COPIED", "not-a-real-credential"):
                    self.assertNotIn(marker, text)


if __name__ == "__main__":
    unittest.main()
