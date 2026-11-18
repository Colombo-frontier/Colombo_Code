"""Runtime boundaries: mocked model transport and read-only registration checks."""
from __future__ import annotations

from copy import deepcopy
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
CORE_ROOT = PACKAGE.parent
sys.path.insert(0, str(CORE_ROOT / "src"))
sys.path.insert(0, str(PACKAGE / "runtime"))
sys.path.insert(0, str(PACKAGE / "tools"))

from colombo.memory import integration
from colombo.memory import retrieval as core_retrieval
from colombo.memory.contracts import ContractError, digest
from colombo.memory.store import Store as ReadStore, atomic_json, read_json
from colombo_memory_agent import backend as backend_module
from colombo_memory_agent.backend import CodexBackend
from colombo_memory_agent.store import WriterStore as Store
import doctor


def snapshot(root: Path):
    """Include paths as well as bytes, so accidental database creation is visible."""
    if not root.exists():
        return None
    return {str(path.relative_to(root)): (
        "directory" if path.is_dir() else hashlib.sha256(path.read_bytes()).hexdigest()
    ) for path in root.rglob("*")}


class BackendIsolationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="memory-backend-safety-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.codex_home = self.root / "codex-home"
        self.codex_home.mkdir()
        self.env = patch.dict(os.environ, {"CODEX_HOME": str(self.codex_home)})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.calls = []

    def run_backend(self, backend=None, role="curator"):
        def fake_process(command, **kwargs):
            self.calls.append((list(command), kwargs))
            output = Path(command[command.index("--output-last-message") + 1])
            output.write_text('{"mock_transport": true}', encoding="utf-8")
            return SimpleNamespace(returncode=0, communicate=lambda data, timeout: (None, None))

        with patch.object(backend_module.shutil, "which", return_value="/mock/codex"), \
                patch.object(backend_module.subprocess, "Popen", side_effect=fake_process):
            result = (backend or CodexBackend()).run(
                role=role, prompt="Synthetic transport fixture; no scientific review.",
                schema={"type": "object"}, workspace=self.root, runs=self.root / "runs")
        return result, read_json(result.run_directory / "run.json")

    def test_fresh_process_ignores_configuration_and_keeps_read_only_transport(self):
        first, receipt = self.run_backend()
        second, _ = self.run_backend(role="reviewer")
        self.assertNotEqual(first.run_id, second.run_id)
        self.assertEqual(len(self.calls), 2)
        for command, kwargs in self.calls:
            for flag in ("--ignore-user-config", "--ephemeral", "--json", "--output-schema"):
                self.assertIn(flag, command)
            self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
            self.assertEqual(command[command.index("--ask-for-approval") + 1], "never")
            self.assertEqual(command[-1], "-")
            self.assertNotIn("resume", command)
            # The existing authentication home remains available; no copied credentials.
            effective_env = kwargs.get("env") or os.environ
            self.assertEqual(effective_env["CODEX_HOME"], str(self.codex_home))
            self.assertEqual(kwargs["cwd"], self.root)
        self.assertEqual(receipt["config_mode"], "ignore-user-config")
        self.assertEqual(receipt["status"], "transport_complete")
        self.assertIn("model", receipt)
        self.assertIn("model_source", receipt)
        self.assertEqual(receipt["transport_preferences"], {})

    def test_only_top_level_configured_model_is_forwarded(self):
        (self.codex_home / "config.toml").write_text(
            'model = "configured-test-model"\n'
            '[mcp_servers.unrelated]\ncommand = "must-not-launch"\n'
            '[profiles.unselected]\nmodel = "profile-test-model"\n', encoding="utf-8")
        _, receipt = self.run_backend()
        command, _ = self.calls[-1]
        self.assertEqual(command[command.index("--model") + 1], "configured-test-model")
        self.assertEqual(receipt["model"], "configured-test-model")
        self.assertNotIn("must-not-launch", json.dumps(command))
        self.assertNotIn("profile-test-model", json.dumps(command))

    def test_explicit_models_take_priority_while_proxy_preference_is_preserved(self):
        config = self.codex_home / "config.toml"
        # An unused model value must not override or invalidate explicit models.
        config.write_text('model = 123\n[features]\nrespect_system_proxy = true\n', encoding="utf-8")
        backend = CodexBackend(model="explicit-curator", reviewer_model="explicit-reviewer")
        _, curator = self.run_backend(backend)
        _, reviewer = self.run_backend(backend, role="reviewer")
        self.assertEqual(curator["model"], "explicit-curator")
        self.assertEqual(reviewer["model"], "explicit-reviewer")
        for receipt in (curator, reviewer):
            self.assertEqual(receipt["transport_preferences"], {"respect_system_proxy": True})
        self.assertEqual(curator["model_source"], "explicit")
        self.assertEqual(reviewer["model_source"], "reviewer_model")

    def test_proxy_boolean_values_are_forwarded_without_other_configuration(self):
        for value in (False, True):
            with self.subTest(respect_system_proxy=value):
                (self.codex_home / "config.toml").write_text(
                    'model = "configured-test-model"\n'
                    '[features]\nrespect_system_proxy = ' + json.dumps(value) + '\nplugins = true\n'
                    '[plugins.unrelated]\nenabled = true\n'
                    '[mcp_servers.unrelated]\ncommand = "do-not-copy-mcp-command"\n'
                    '[model_providers.unselected]\nenv_key = "DO_NOT_COPY_PROVIDER_ENV_NAME"\n',
                    encoding="utf-8")
                _, receipt = self.run_backend()
                command, _ = self.calls[-1]
                self.assertIn("--ignore-user-config", command)
                self.assertEqual([command[i + 1] for i, item in enumerate(command) if item == "-c"],
                                 ["features.respect_system_proxy=" + json.dumps(value)])
                self.assertEqual(command[command.index("--model") + 1], "configured-test-model")
                self.assertEqual(receipt["transport_preferences"], {"respect_system_proxy": value})
                serialized = json.dumps(receipt)
                for omitted in ("do-not-copy-mcp-command", "DO_NOT_COPY_PROVIDER_ENV_NAME", "plugins.unrelated",
                                "features.plugins", "model_providers"):
                    self.assertNotIn(omitted, serialized)

    def test_absent_proxy_preference_does_not_override_cli_transport_defaults(self):
        (self.codex_home / "config.toml").write_text('[features]\nplugins = true\n', encoding="utf-8")
        _, receipt = self.run_backend(CodexBackend(model="explicit-test-model"))
        self.assertNotIn("-c", self.calls[-1][0])
        self.assertEqual(receipt["transport_preferences"], {})

    def test_invalid_proxy_preference_is_rejected_before_a_model_process_is_created(self):
        for value in (1, "true", [], {"enabled": True}):
            with self.subTest(value=value):
                # An inline table is legal TOML but is not an allowed proxy bool.
                raw = '{enabled = true}' if isinstance(value, dict) else json.dumps(value)
                (self.codex_home / "config.toml").write_text(
                    '[features]\nrespect_system_proxy = ' + raw + '\n', encoding="utf-8")
                with self.assertRaisesRegex(ContractError, "respect_system_proxy must be a boolean"):
                    self.run_backend(CodexBackend(model="explicit-test-model"))
                self.assertEqual(self.calls, [])

    def test_reviewer_uses_shared_explicit_model_when_no_override_is_given(self):
        _, receipt = self.run_backend(CodexBackend(model="shared-explicit"), role="reviewer")
        self.assertEqual(receipt["model"], "shared-explicit")

    def test_missing_configuration_keeps_cli_default_without_creating_config(self):
        before = snapshot(self.codex_home)
        _, receipt = self.run_backend()
        self.assertNotIn("--model", self.calls[-1][0])
        self.assertIsNone(receipt["model"])
        self.assertEqual(snapshot(self.codex_home), before)


class CoreReaderBoundaryTests(unittest.TestCase):
    def test_core_exposes_read_capabilities_without_writer_or_index_builder(self):
        with tempfile.TemporaryDirectory(prefix="memory-capability-boundary-") as folder:
            root = Path(folder) / "not-initialized"
            reader = ReadStore(root)
            writer = Store(root)
            self.assertIsInstance(writer, ReadStore)
            for capability in ("initialize", "install_leads", "prepare", "publish"):
                with self.subTest(capability=capability):
                    self.assertFalse(hasattr(reader, capability))
                    self.assertTrue(callable(getattr(writer, capability)))
            self.assertTrue(callable(reader.manifest))
            self.assertTrue(callable(reader.get))
            self.assertFalse(hasattr(core_retrieval, "build_index"))
            self.assertFalse(root.exists(), "Constructing a reader or writer must not initialize memory")


class RegistrationValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="memory-registration-safety-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "memory"
        self.store = Store(self.root)
        self.store.initialize()

    def assert_registration_rejected_without_writes(self):
        before = snapshot(self.root)
        with patch.object(integration, "register_memory") as register:
            with self.assertRaises(ContractError) as error:
                integration.register_builtin_memory(
                    object(), research_mode="generic", memory_root=self.root)
            self.assertTrue(str(error.exception).strip())
            register.assert_not_called()
        self.assertEqual(snapshot(self.root), before)

    def replace_manifest(self, value):
        pointer = read_json(self.store.state_root / "CURRENT.json")
        generation = self.store.state_root / ".generations" / pointer["generation"]
        atomic_json(generation / "manifest.json", value)
        pointer["manifest_hash"] = digest(value)
        atomic_json(self.store.state_root / "CURRENT.json", pointer)

    def test_builtin_default_root_is_validated_and_registered_without_writes(self):
        before = snapshot(self.root)
        with patch.object(integration, "DEFAULT_MEMORY_ROOT", self.root), \
                patch.object(integration, "register_memory") as register:
            self.assertTrue(integration.register_builtin_memory(object(), research_mode="generic"))
            register.assert_called_once()
            self.assertEqual(Path(register.call_args.kwargs["memory_root"]), self.root)
        self.assertEqual(snapshot(self.root), before)

    def test_valid_registration_is_read_only_including_leads(self):
        self.store.install_leads([])
        before = snapshot(self.root)
        with patch.object(integration, "register_memory") as register:
            self.assertTrue(integration.register_builtin_memory(
                object(), research_mode="oracle_complexity", memory_root=self.root))
            register.assert_called_once()
        self.assertEqual(snapshot(self.root), before)

    def test_uninitialized_path_is_not_created(self):
        self.root = Path(self.temporary.name) / "not-created" / "memory"
        self.assert_registration_rejected_without_writes()
        self.assertFalse(self.root.exists())

    def test_invalid_current_pointer_fails_before_tool_registration(self):
        for pointer in ([], {}, {"generation": "../escape", "manifest_hash": "0" * 64}):
            with self.subTest(pointer=pointer):
                atomic_json(self.store.state_root / "CURRENT.json", pointer)
                self.assert_registration_rejected_without_writes()

    def test_manifest_structure_is_validated_not_just_json_decoded(self):
        original = self.store.manifest()
        replacements = ({"schema": "unrecognized"}, {"entries": []}, {"receipts": []},
                        {"sequence": -1}, {"sequence": True})
        for replacement in replacements:
            with self.subTest(replacement=replacement):
                value = deepcopy(original)
                value.update(replacement)
                self.replace_manifest(value)
                self.assert_registration_rejected_without_writes()

    def test_manifest_hash_mismatch_is_rejected(self):
        manifest_path = self.store.generation() / "manifest.json"
        manifest = read_json(manifest_path)
        manifest["sequence"] += 1
        atomic_json(manifest_path, manifest)
        self.assert_registration_rejected_without_writes()

    def test_missing_index_is_not_silently_created(self):
        index = self.store.generation() / "catalog.sqlite"
        index.unlink()
        self.assert_registration_rejected_without_writes()
        self.assertFalse(index.exists())

    def test_corrupt_index_is_rejected_without_repair(self):
        (self.store.generation() / "catalog.sqlite").write_bytes(b"not a SQLite database")
        self.assert_registration_rejected_without_writes()

    def test_index_needs_both_scope_and_search_tables(self):
        index = self.store.generation() / "catalog.sqlite"
        original = index.read_bytes()
        for table in ("scopes", "search"):
            with self.subTest(table=table):
                index.write_bytes(original)
                with closing(sqlite3.connect(index)) as db:
                    db.execute("DROP TABLE " + table)
                    db.commit()
                self.assert_registration_rejected_without_writes()

    def test_configured_lead_snapshot_is_also_checked(self):
        self.store.install_leads([])
        pointer = read_json(self.store.state_root / "LEADS.json")
        index = self.store.state_root / pointer["path"] / "catalog.sqlite"
        index.unlink()
        self.assert_registration_rejected_without_writes()
        self.assertFalse(index.exists())


class DoctorFlagTests(unittest.TestCase):
    def test_doctor_reports_isolation_flags_without_model_calls(self):
        def completed(command, **kwargs):
            text = "codex-test" if "--version" in command else (
                "--output-schema --output-last-message --sandbox --json "
                "--ignore-user-config --ephemeral")
            return subprocess.CompletedProcess(command, 0, stdout=text, stderr="")

        with patch.object(doctor.shutil, "which", return_value="/mock/codex"), \
                patch.object(doctor.subprocess, "run", side_effect=completed) as run:
            result = doctor.inspect(check_codex=True)
        self.assertFalse(result["model_called"])
        self.assertFalse(result["authentication_verified"])
        for flag in ("--ignore-user-config", "--ephemeral"):
            self.assertTrue(result["required_cli_flags"][flag])
        for call in run.call_args_list:
            self.assertNotIn("--output-last-message", call.args[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
