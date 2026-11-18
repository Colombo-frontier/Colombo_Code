from __future__ import annotations

import json
from contextlib import contextmanager
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / "src"))

from colombo.brain.model_calls import BackendError, CallUncertain, CodexBackend, find_codex, reconcile_call
from colombo.brain.research_store import Store


class FakeProcess:
    def __init__(self, callback, command, **kwargs):
        self.callback = callback
        self.command = command
        self.kwargs = kwargs
        self.pid = 12345
        self.returncode = None

    def communicate(self, prompt, timeout):
        self.callback(self, prompt, timeout)
        self.returncode = 0
        return None, None

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        self.returncode = 0
        return 0


class BackendTests(unittest.TestCase):
    def setUp(self):
        temporary_root = PROJECT / "validation"
        temporary_root.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="backend-", dir=temporary_root)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project"
        shutil.copytree(PROJECT / "agents", self.project / "agents")
        (self.project / "run.py").write_text("", encoding="utf-8")
        self.auth = self.root / "login"
        self.auth.mkdir()
        (self.auth / "auth.json").write_text('{"fake":"do-not-publish"}', encoding="utf-8")
        (self.auth / "config.toml").write_text(
            'model = "configured-model"\nmodel_reasoning_effort = "medium"\nmodel_provider = "test"\n'
            '[model_providers.test]\nname="Test"\nbase_url="https://example.invalid"\nwire_api="responses"\n'
            'requires_openai_auth=true\n[features]\nplugins=true\n'
            '[mcp_servers.unrelated]\ncommand="unrelated"\n', encoding="utf-8")
        self.exe = self.root / "codex.exe"
        self.exe.write_bytes(b"fake")
        self.run_root = self.root / "run"
        self.run_root.mkdir()
        from colombo.configuration import load_config
        self.config = load_config()
        self.config["runtime"].update(auth_home=str(self.auth), codex_bin=str(self.exe))
        self.config["brain"].update(model="", reasoning_effort="", timeout_seconds=20)
        self.config["verifier"].update(model="review-model", reasoning_effort="", timeout_seconds=10)
        self.config["audit"].update(model="", reasoning_effort="")
        self.store = Store.create(self.run_root, "Backend receipt fixture", [], self.config)
        self.backend = CodexBackend(self.project, self.config)

    @contextmanager
    def spawn(self, callback):
        def factory(command, **kwargs):
            return FakeProcess(callback, command, **kwargs)
        def terminate(process, **kwargs):
            process.wait()
            return True
        with patch("colombo.brain.model_calls.managed_popen", side_effect=factory) as launch, \
             patch("colombo.brain.model_calls.process_identity", return_value={"pid": 12345, "start_token": "fake", "platform": "test"}), \
             patch("colombo.brain.model_calls.terminate_tree", side_effect=terminate), \
             patch("colombo.brain.model_calls.close_process_job"):
            yield launch

    def review_payload(self):
        result_ref = self.store.write_record("result", {
            "task_id": "transport-review-task", "attempt_id": "A0001",
            "execution_status": "finished", "accepted": False, "artifacts": [],
        }, request_id="transport-review-result")
        return {"verdict": "pass", "summary": "Synthetic transport review", "findings": [],
                "checked_refs": [result_ref["id"]], "review_kind": "result",
                "result_ref": result_ref["id"], "confirmed_claims": [],
                "completion_status": "partial", "repair_kind": "none"}

    def write_submission(self, process, payload=None, *, emit_receipt=True):
        work = Path(process.command[process.command.index("-C") + 1])
        context = json.loads((work / "context.json").read_text(encoding="utf-8"))
        kind = {"plan": "plan", "process_results": "assessment", "integrate": "assessment",
                "verify-progress": "review", "conclude": "conclusion"}[context["stage"]]
        if payload is None:
            payload = {"rationale": "test", "tasks": []} if kind == "plan" else {"rationale": "test"}
        if kind == "review" and "review_kind" not in payload:
            payload = {**BackendTests.review_payload(self), **payload}
        ref = self.store.write_record(kind, payload, request_id="submission:" + context["call_id"])
        if emit_receipt:
            (work / "submission.json").write_text(json.dumps({"ref": ref,
                **{k: context[k] for k in ("call_id", "role", "stage")}}), encoding="utf-8")
        return ref

    def test_commits_only_service_receipt_and_isolates_config(self):
        captured = {}
        def callback(proc, prompt, timeout):
            home = Path(proc.kwargs["env"]["CODEX_HOME"])
            captured["home"] = home
            work = Path(proc.command[proc.command.index("-C") + 1])
            context = json.loads((work / "context.json").read_text(encoding="utf-8"))
            manifest = json.loads((work / "call.json").read_text(encoding="utf-8"))
            budget = context["call_budget"]
            self.assertEqual(budget["started_at_unix"], manifest["started_at"])
            self.assertEqual(budget["deadline_unix"], manifest["started_at"] + 20)
            self.assertLessEqual(timeout, 20)
            self.assertGreater(timeout, 0)
            self.assertTrue(budget["audit_wait_counts_toward_call"])
            self.assertNotIn("call_budget", manifest["input"]["context"])
            cfg = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
            self.assertEqual(cfg["model"], "configured-model")
            self.assertEqual(set(cfg["mcp_servers"]), {"colombo"})
            self.assertFalse(cfg["features"]["plugins"])
            self.assertEqual(cfg["sandbox_mode"], "read-only")
            self.assertIn("read_research", (work / "AGENTS.md").read_text(encoding="utf-8") +
                          (work / "protocol.md").read_text(encoding="utf-8"))
            self.assertNotIn("do-not-publish", prompt)
            self.write_submission(proc)
        with self.spawn(callback) as mock:
            out = self.backend.invoke("brain", "plan", self.run_root, "call-1", "Plan tasks", {})
            cached = self.backend.invoke("brain", "plan", self.run_root, "call-1", "Plan tasks", {})
        self.assertEqual(out, cached)
        self.assertEqual(mock.call_count, 1)
        receipt = json.loads((self.run_root / "brain/calls/call-1/submission.json").read_text(encoding="utf-8"))
        self.assertNotIn("payload", receipt)
        self.assertEqual(set(receipt["ref"]), {"id", "revision"})
        self.assertFalse((captured["home"] / "auth.json").exists())
        self.assertTrue((self.auth / "auth.json").is_file())

    def test_rejects_changed_call_input_and_wrong_receipt_identity(self):
        with self.spawn(lambda p, *_: self.write_submission(p)):
            self.backend.invoke("brain", "plan", self.run_root, "call-1", "Plan", {})
        with self.assertRaisesRegex(BackendError, "different input"):
            self.backend.invoke("brain", "plan", self.run_root, "call-1", "Different", {})
        receipt = self.run_root / "brain/calls/call-1/submission.json"
        saved = json.loads(receipt.read_text(encoding="utf-8"))
        receipt.write_text(json.dumps({**saved, "call_id": "other-call"}), encoding="utf-8")
        with self.assertRaisesRegex(BackendError, "different call"):
            self.backend.invoke("brain", "plan", self.run_root, "call-1", "Plan", {})
        unrelated = self.store.write_record("note", {"text": "Not this call's submission"})
        receipt.write_text(json.dumps({**saved, "ref": unrelated}), encoding="utf-8")
        with self.assertRaisesRegex(BackendError, "this call's committed submission"):
            self.backend.invoke("brain", "plan", self.run_root, "call-1", "Plan", {})

    def test_unlimited_brain_has_no_process_deadline_and_still_commits_once(self):
        self.config["brain"]["timeout_seconds"] = "unlimited"
        for stage in ("plan", "process_results"):
            with self.subTest(stage=stage):
                call_id = "unlimited-" + stage

                def callback(proc, prompt, timeout):
                    self.assertIsNone(timeout)
                    work = Path(proc.command[proc.command.index("-C") + 1])
                    context = json.loads((work / "context.json").read_text(encoding="utf-8"))
                    manifest = json.loads((work / "call.json").read_text(encoding="utf-8"))
                    budget = context["call_budget"]
                    self.assertEqual(manifest["timeout_seconds"], "unlimited")
                    self.assertEqual(budget["timeout_seconds"], "unlimited")
                    self.assertEqual(budget["started_at_unix"], manifest["started_at"])
                    self.assertIsNone(budget["deadline_unix"])
                    self.assertIsNone(budget["recommended_audit_start_by_unix"])
                    self.assertEqual(budget["submission_reserve_seconds"], 0)
                    self.assertEqual(budget["audit_timeout_seconds"], "unlimited")
                    self.assertTrue(budget["audit_wait_counts_toward_call"])
                    self.assertNotIn("call_budget", manifest["input"]["context"])
                    self.assertRegex(prompt, r"unlimited|no time limit|no.*time limit")
                    for instruction in ("check the remaining time", "recommended latest audit time", "reserve time for audits and final submission"):
                        self.assertNotIn(instruction, prompt)
                    self.write_submission(proc)

                with self.spawn(callback) as launch:
                    result = self.backend.invoke("brain", stage, self.run_root, call_id, "Work", {})
                    replay = self.backend.invoke("brain", stage, self.run_root, call_id, "Work", {})
                self.assertEqual(result, replay)
                self.assertEqual(launch.call_count, 1)
                saved = json.loads((self.run_root / "brain/calls" / call_id / "call.json").read_text(encoding="utf-8"))
                self.assertEqual(saved["status"], "submitted")
                self.assertIsNotNone(saved["ended_at"])

    def test_unlimited_brain_remains_interruptible_and_cleans_up(self):
        self.config["brain"]["timeout_seconds"] = "unlimited"
        captured = {}

        def callback(proc, prompt, timeout):
            self.assertIsNone(timeout)
            captured["process"] = proc
            raise KeyboardInterrupt()

        with self.spawn(callback):
            with self.assertRaises(KeyboardInterrupt):
                self.backend.invoke("brain", "plan", self.run_root, "interrupted-unlimited", "Plan", {})
        saved = json.loads((self.run_root / "brain/calls/interrupted-unlimited/call.json").read_text(encoding="utf-8"))
        self.assertIsNotNone(captured["process"].poll())
        self.assertTrue(saved["process_exit_confirmed"])
        self.assertTrue(saved["process_tree_terminated"])
        self.assertNotEqual(saved["status"], "submitted")

    def test_backend_timeout_defaults_and_validation_are_role_specific(self):
        self.config["brain"].pop("timeout_seconds")
        self.assertEqual(self.backend._settings("brain")["timeout_seconds"], "unlimited")
        self.assertEqual(self.backend._settings("verifier")["timeout_seconds"], 10)
        invalid = (True, False, 0, -1, "forever", "300", None, float("inf"), float("nan"))
        for value in invalid:
            with self.subTest(role="brain", value=value):
                self.config["brain"]["timeout_seconds"] = value
                with self.assertRaises(BackendError):
                    self.backend._settings("brain")
        self.config["brain"]["timeout_seconds"] = "unlimited"
        self.config["verifier"]["timeout_seconds"] = "unlimited"
        self.assertEqual(self.backend._settings("verifier")["timeout_seconds"], "unlimited")
        self.config["verifier"].pop("timeout_seconds")
        self.assertEqual(self.backend._settings("verifier")["timeout_seconds"], "unlimited")
        self.config["brain"]["timeout_seconds"] = 22
        self.assertEqual(self.backend._settings("verifier")["timeout_seconds"], 22)

    def test_mcp_explicitly_carries_resolved_login_source_for_nested_audit(self):
        self.config["runtime"]["auth_home"] = ""
        parent_home = self.root / "parent-runtime"
        with patch.dict(os.environ, {"CODEX_HOME": str(self.auth), "OPENAI_API_KEY": ""}):
            self.backend._prepare_home(parent_home, "brain", "process_results", self.run_root,
                self.root / "brain-work", "parent", self.backend._settings("brain"))
        config_text = (parent_home / "config.toml").read_text(encoding="utf-8")
        server_env = tomllib.loads(config_text)["mcp_servers"]["colombo"]["env"]
        self.assertEqual(Path(server_env["CODEX_HOME"]), self.auth.resolve())
        self.assertNotEqual(Path(server_env["CODEX_HOME"]), parent_home)
        self.assertNotIn("do-not-publish", config_text)
        # Reproduce a fresh MCP subprocess that receives no ambient CODEX_HOME:
        # only the explicit MCP env may provide the nested auditor's login source.
        nested_home = self.root / "audit-runtime"
        with patch.dict(os.environ, server_env, clear=True):
            original, model = self.backend._prepare_home(nested_home, "audit", "audit", self.run_root,
                self.root / "audit-work", "nested", self.backend._settings("brain"), enable_mcp=False)
        self.assertEqual(original, self.auth.resolve())
        self.assertEqual(model, "configured-model")
        self.assertTrue((nested_home / "auth.json").is_file())
        self.assertNotIn("mcp_servers", tomllib.loads((nested_home / "config.toml").read_text(encoding="utf-8")))

    def test_lookup_keys_are_forwarded_by_name_only_to_brain_mcp(self):
        dummy_keys = {"SERPER_API_KEY": "dummy-serper-never-render-this-value",
                      "JINA_API_KEY": "dummy-jina-never-render-this-value"}
        for role, stage in (("brain", "plan"), ("verifier", "verify-progress")):
            with self.subTest(role=role):
                home = self.root / ("lookup-runtime-" + role)
                with patch.dict(os.environ, dummy_keys):
                    self.backend._prepare_home(home, role, stage, self.run_root,
                        self.root / ("lookup-work-" + role), "lookup", self.backend._settings(role))
                text = (home / "config.toml").read_text(encoding="utf-8")
                config = tomllib.loads(text)["mcp_servers"]["colombo"]
                self.assertEqual(config.get("env_vars", []), list(dummy_keys) if role == "brain" else [])
                for key, value in dummy_keys.items():
                    self.assertNotIn(value, text)
                    self.assertNotIn(key, config.get("env", {}))

    def test_explicit_auth_home_takes_precedence_over_ambient_home_for_mcp(self):
        other = self.root / "empty-ambient-home"
        other.mkdir()
        runtime_home = self.root / "explicit-auth-runtime"
        with patch.dict(os.environ, {"CODEX_HOME": str(other), "OPENAI_API_KEY": ""}):
            self.backend._prepare_home(runtime_home, "brain", "plan", self.run_root,
                self.root / "explicit-auth-work", "explicit", self.backend._settings("brain"))
        config = tomllib.loads((runtime_home / "config.toml").read_text(encoding="utf-8"))
        self.assertEqual(Path(config["mcp_servers"]["colombo"]["env"]["CODEX_HOME"]), self.auth.resolve())

    def test_fresh_brain_and_nested_audit_keep_original_model_cache_and_settings(self):
        cached = json.dumps({"fetched_at": "2000-01-01T00:00:00Z", "client_version": "0.166.0",
            "identity": {"fixture": "same-login"}, "models": [{"slug": "cached-other-model"}]}).encode()
        (self.auth / "models_cache.json").write_bytes(cached)
        (self.auth / "sessions").mkdir()
        (self.auth / "sessions/private.json").write_text("not runtime input", encoding="utf-8")
        for role, enabled in (("brain", True), ("audit", False)):
            with self.subTest(role=role):
                home = self.root / (role + "-cached-home")
                original, model = self.backend._prepare_home(home, role, "plan" if enabled else "audit",
                    self.run_root, self.root / (role + "-work"), role, self.backend._settings("brain"),
                    enable_mcp=enabled)
                self.assertEqual((home / "models_cache.json").read_bytes(), cached)
                self.assertEqual((original / "models_cache.json").read_bytes(), cached)
                self.assertFalse((home / "sessions").exists())
                config = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
                self.assertEqual(model, "configured-model")
                self.assertEqual(config["model_reasoning_effort"], "medium")
                self.assertEqual(config["model_provider"], "test")
                self.assertNotIn("model_catalog_json", config)

    def test_optional_bad_model_cache_does_not_block_preparation(self):
        for index, cached in enumerate((None, b"{broken", b"[]", b'{"models":false}', b"\xff",
                                        b" " * (5 * 1024 * 1024 + 1))):
            with self.subTest(index=index):
                source = self.auth / "models_cache.json"
                source.unlink(missing_ok=True)
                if cached is not None:
                    source.write_bytes(cached)
                home = self.root / f"invalid-cache-{index}"
                _, model = self.backend._prepare_home(home, "brain", "plan", self.run_root,
                    self.root / "work", str(index), self.backend._settings("brain"))
                self.assertEqual(model, "configured-model")
                self.assertTrue((home / "config.toml").is_file())
                self.assertFalse((home / "models_cache.json").exists())

    def test_cache_copy_io_failure_does_not_block_launch_configuration(self):
        source = self.auth / "models_cache.json"
        source.write_text('{"models":[]}', encoding="utf-8")
        home = self.root / "unwritable-cache-home"
        with patch.object(Path, "write_bytes", side_effect=PermissionError("cache unavailable")):
            _, model = self.backend._prepare_home(home, "brain", "plan", self.run_root,
                self.root / "work", "cache-io", self.backend._settings("brain"))
        self.assertEqual(model, "configured-model")
        self.assertTrue((home / "config.toml").is_file())
        self.assertEqual(source.read_text(encoding="utf-8"), '{"models":[]}')

    def test_explicit_static_catalog_is_frozen_for_each_role_without_changing_model(self):
        source = self.root / "selected-catalog.json"
        catalog = {"models": [{"slug": name, "multi_agent_version": "v2",
                               "supported_reasoning_levels": [{"effort": "medium"}]}
                              for name in ("configured-model", "review-model")]}
        data = json.dumps(catalog).encode()
        source.write_bytes(data)
        self.config["runtime"]["model_catalog_json"] = str(source.resolve())
        for role, stage in (("brain", "plan"), ("verifier", "verify-progress"), ("audit", "audit")):
            home = self.root / ("static-" + role)
            _, model = self.backend._prepare_home(home, role, stage, self.run_root,
                self.root / "work", role, self.backend._settings(role), enable_mcp=role != "audit")
            config = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
            fixed = Path(config["model_catalog_json"])
            self.assertEqual(fixed.parent, home)
            self.assertEqual(fixed.read_bytes(), data)
            self.assertEqual(config["model"], model)
            self.assertEqual(config["model_reasoning_effort"], "medium")
            self.assertEqual(config["model_provider"], "test")
            self.assertFalse(config["features"]["multi_agent"])
            self.assertFalse(config["features"]["multi_agent_v2"])
            self.assertFalse(config["agents"]["enabled"])
        source.write_text('{"models":[]}', encoding="utf-8")
        self.assertEqual((self.root / "static-brain/model_catalog.json").read_bytes(), data)

    def test_invalid_explicit_catalog_never_launches_a_model(self):
        source = self.root / "invalid-catalog.json"
        self.config["runtime"]["model_catalog_json"] = str(source.resolve())
        cases = (None, b"broken", b'{"models":[]}', b'{"models":[{}]}',
                 b'{"models":[{"slug":"other-model"}]}',
                 b'{"models":[{"slug":"configured-model"}]}',
                 b'{"models":[{"slug":"configured-model"},{"slug":"configured-model"}]}')
        for index, data in enumerate(cases):
            with self.subTest(index=index):
                source.unlink(missing_ok=True)
                if data is not None:
                    source.write_bytes(data)
                with patch("colombo.brain.model_calls.managed_popen") as spawn:
                    with self.assertRaises(BackendError):
                        self.backend.invoke("brain", "plan", self.run_root, f"bad-catalog-{index}", "Plan", {})
                    spawn.assert_not_called()
        self.assertFalse(any(self.project.glob(".runtime/brain/*/auth.json")))

    def test_controller_explicitly_passes_static_catalog_to_cell_adapter(self):
        from colombo.brain.controller import OracleController as Controller
        self.config["runtime"]["model_catalog_json"] = str(self.root / "selected-catalog.json")
        self.store.set_meta(config=self.config)
        with patch("colombo.brain.controller.CellAdapter") as adapter:
            Controller(self.project, self.run_root)
        passed = adapter.call_args.args[1]
        self.assertEqual(passed["cell"]["model_catalog_json"], self.config["runtime"]["model_catalog_json"])

    def test_chat_final_text_is_not_a_submission(self):
        def callback(proc, *_):
            Path(proc.command[proc.command.index("--output-last-message") + 1]).write_text('{"rationale":"uncommitted"}', encoding="utf-8")
        with self.spawn(callback):
            with self.assertRaisesRegex(BackendError, "without a committed"):
                self.backend.invoke("brain", "plan", self.run_root, "call-1", "Plan", {})
        with patch("colombo.brain.model_calls.managed_popen") as launch:
            with self.assertRaises(CallUncertain):
                self.backend.invoke("brain", "plan", self.run_root, "call-1", "Plan", {})
            launch.assert_not_called()

    def test_verifier_is_new_role_scoped_invocation(self):
        expected = self.review_payload()
        def callback(proc, *_):
            cfg = tomllib.loads((Path(proc.kwargs["env"]["CODEX_HOME"]) / "config.toml").read_text(encoding="utf-8"))
            self.assertEqual(cfg["model"], "review-model")
            self.assertIn("verifier", cfg["mcp_servers"]["colombo"]["args"])
            work = Path(proc.command[proc.command.index("-C") + 1])
            context = json.loads((work / "context.json").read_text(encoding="utf-8"))
            self.assertEqual(context["review_package_ref"], {"id": "review-package-1"})
            self.assertTrue((work / ".agents/skills/verify-progress/SKILL.md").exists())
            self.assertEqual((work / "protocol.md").read_bytes(),
                             (self.project / "agents/brain/verifier/protocol.md").read_bytes())
            self.write_submission(proc, expected)
        with self.spawn(callback):
            self.assertEqual(self.backend.invoke("verifier", "verify-progress", self.run_root, "review-1", "Review", {"review_package_ref": {"id": "review-package-1"}}), expected)

    def test_timeout_retains_committed_receipt(self):
        def callback(proc, *_):
            self.write_submission(proc)
            raise subprocess.TimeoutExpired(proc.command, 20)
        with self.spawn(callback):
            result = self.backend.invoke("brain", "plan", self.run_root, "call-1", "Plan", {})
        self.assertEqual(result, {"rationale": "test", "tasks": []})
        call = json.loads((self.run_root / "brain/calls/call-1/call.json").read_text(encoding="utf-8"))
        self.assertEqual(call["status"], "submitted")
        self.assertTrue(call["process_timed_out"])

    def test_exit_recovers_lost_receipt_for_each_submission_channel(self):
        cases = [("brain", "plan", {"rationale": "test", "tasks": []}),
                 ("brain", "process_results", {"rationale": "assessment fixture"}),
                 ("verifier", "verify-progress", self.review_payload())]
        for role, stage, payload in cases:
            with self.subTest(stage=stage):
                call_id = "lost-" + stage
                captured = {}
                def callback(proc, *_):
                    captured["ref"] = self.write_submission(proc, payload, emit_receipt=False)
                    work = Path(proc.command[proc.command.index("-C") + 1])
                    self.assertFalse((work / "submission.json").exists())
                with self.spawn(callback) as launch:
                    result = self.backend.invoke(role, stage, self.run_root, call_id, "Submit", {})
                    replay = self.backend.invoke(role, stage, self.run_root, call_id, "Submit", {})
                self.assertEqual(result, payload)
                self.assertEqual(replay, payload)
                self.assertEqual(launch.call_count, 1)
                receipt = json.loads((self.run_root / "brain/calls" / call_id / "submission.json").read_text(encoding="utf-8"))
                self.assertEqual(receipt, {"call_id": call_id, "role": role, "stage": stage, "ref": captured["ref"]})
                self.assertEqual(self.store.request_record("submission:" + call_id), captured["ref"])

    def test_timeout_recovers_committed_submission_without_receipt(self):
        captured = {}
        def callback(proc, *_):
            captured["ref"] = self.write_submission(proc, emit_receipt=False)
            raise subprocess.TimeoutExpired(proc.command, 20)
        with self.spawn(callback) as launch:
            result = self.backend.invoke("brain", "plan", self.run_root, "lost-timeout", "Plan", {})
        self.assertEqual(result, {"rationale": "test", "tasks": []})
        folder = self.run_root / "brain/calls/lost-timeout"
        self.assertEqual(json.loads((folder / "submission.json").read_text(encoding="utf-8"))["ref"], captured["ref"])
        call = json.loads((folder / "call.json").read_text(encoding="utf-8"))
        self.assertEqual(call["status"], "submitted")
        self.assertTrue(call["process_timed_out"])
        self.assertEqual(launch.call_count, 1)

    def test_existing_call_recovers_lost_receipt_but_rejects_changed_input_first(self):
        with self.spawn(lambda p, *_: self.write_submission(p)):
            expected = self.backend.invoke("brain", "plan", self.run_root, "lost-reentry", "Plan", {})
        receipt = self.run_root / "brain/calls/lost-reentry/submission.json"
        committed = self.store.request_record("submission:lost-reentry")
        receipt.unlink()
        with patch("colombo.brain.model_calls.managed_popen") as launch:
            with self.assertRaisesRegex(BackendError, "different input"):
                self.backend.invoke("brain", "plan", self.run_root, "lost-reentry", "Changed", {})
            self.assertFalse(receipt.exists())
            self.assertEqual(self.backend.invoke("brain", "plan", self.run_root, "lost-reentry", "Plan", {}), expected)
            launch.assert_not_called()
        self.assertEqual(json.loads(receipt.read_text(encoding="utf-8"))["ref"], committed)

    def test_role_and_identifier_guards(self):
        for role, stage, call_id in [("verifier", "plan", "a"), ("brain", "plan", "../escape")]:
            with self.assertRaises(BackendError):
                self.backend.invoke(role, stage, self.run_root, call_id, "", {})

    def test_no_auth_is_error_without_launch(self):
        (self.auth / "auth.json").unlink()
        with patch.dict(os.environ, {}, clear=True), patch("colombo.brain.model_calls.managed_popen") as launch:
            with self.assertRaisesRegex(BackendError, "No file login"):
                self.backend.invoke("brain", "plan", self.run_root, "call-1", "Plan", {})
        launch.assert_not_called()

    def test_explicit_executable_is_not_silently_ignored(self):
        self.assertEqual(find_codex({"codex_bin": str(self.exe)}), str(self.exe.resolve()))
        with self.assertRaises(BackendError):
            find_codex({"codex_bin": str(self.root / "missing")})

    def saved_call(self, status="running", identity=True, **extra):
        folder = self.run_root / "brain/calls/reconcile-1"
        folder.mkdir(parents=True, exist_ok=True)
        manifest = {"call_id": "reconcile-1", "role": "brain", "stage": "plan", "status": status, **extra}
        if identity:
            manifest["process_identity"] = {"pid": 12345, "start_token": "creation-1", "platform": "test"}
        (folder / "call.json").write_text(json.dumps(manifest), encoding="utf-8")
        return folder

    def test_reconcile_live_process_overrides_failed_label(self):
        for status in ("running", "timeout", "failed"):
            self.saved_call(status)
            with patch("colombo.brain.model_calls.process_matches", return_value=True):
                self.assertEqual(reconcile_call(self.run_root, "reconcile-1")["state"], "running")

    def test_reconcile_only_confirms_failure_after_identity_is_gone(self):
        for status in ("running", "timeout", "failed"):
            self.saved_call(status)
            with patch("colombo.brain.model_calls.process_matches", return_value=False):
                self.assertEqual(self.backend.reconcile_call(self.run_root, "reconcile-1")["state"], "failed")
            with patch("colombo.brain.model_calls.process_matches", return_value=None):
                self.assertEqual(reconcile_call(self.run_root, "reconcile-1")["state"], "unknown")

    def test_reconcile_launch_identity_gap_remains_unknown(self):
        for status in ("launch_intent", "running", "timeout", "failed"):
            self.saved_call(status, identity=False, lifecycle_version=2)
            self.assertEqual(reconcile_call(self.run_root, "reconcile-1")["state"], "unknown")
        self.saved_call("preparing", identity=False, lifecycle_version=2)
        self.assertEqual(reconcile_call(self.run_root, "reconcile-1")["state"], "not_started")
        self.saved_call("failed", identity=False, process_exit_confirmed=True)
        self.assertEqual(reconcile_call(self.run_root, "reconcile-1")["state"], "failed")

    def test_reconcile_returns_only_committed_submission_payload(self):
        folder = self.saved_call()
        payload = {"rationale": "test", "tasks": []}
        ref = self.store.write_record("plan", payload, request_id="submission:reconcile-1")
        (folder / "submission.json").write_text(json.dumps({"call_id": "reconcile-1", "role": "brain",
            "stage": "plan", "ref": ref}), encoding="utf-8")
        self.assertEqual(reconcile_call(self.run_root, "reconcile-1"), {"state": "submitted", "payload": payload})
        (folder / "submission.json").write_text('{"payload":{}}', encoding="utf-8")
        self.assertEqual(reconcile_call(self.run_root, "reconcile-1")["state"], "unknown")
        self.assertEqual((folder / "submission.json").read_text(encoding="utf-8"), '{"payload":{}}')

    def test_reconcile_recovers_committed_submission_before_process_state(self):
        folder = self.saved_call(status="failed")
        payload = {"rationale": "committed before receipt failure", "tasks": []}
        ref = self.store.write_record("plan", payload, request_id="submission:reconcile-1")
        with patch("colombo.brain.model_calls.process_matches") as inspect, patch("colombo.brain.model_calls.managed_popen") as launch:
            self.assertEqual(reconcile_call(self.run_root, "reconcile-1"), {"state": "submitted", "payload": payload})
            inspect.assert_not_called()
            launch.assert_not_called()
        self.assertEqual(json.loads((folder / "submission.json").read_text(encoding="utf-8"))["ref"], ref)

    def test_recovery_rejects_a_committed_record_for_the_wrong_stage(self):
        folder = self.saved_call()
        ref = self.store.write_record("note", {"text": "Not a plan"}, request_id="submission:reconcile-1")
        self.assertEqual(reconcile_call(self.run_root, "reconcile-1")["state"], "unknown")
        self.assertFalse((folder / "submission.json").exists())
        invalid = {"call_id": "reconcile-1", "role": "brain", "stage": "plan", "ref": ref}
        (folder / "submission.json").write_text(json.dumps(invalid), encoding="utf-8")
        self.assertEqual(reconcile_call(self.run_root, "reconcile-1")["state"], "unknown")
        self.assertEqual(json.loads((folder / "submission.json").read_text(encoding="utf-8")), invalid)

    def test_reconcile_absent_call_has_not_started(self):
        self.assertEqual(reconcile_call(self.run_root, "absent")["state"], "not_started")


if __name__ == "__main__":
    unittest.main()
