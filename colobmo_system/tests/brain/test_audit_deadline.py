"""Parent audit deadline is checked only when reserving a genuinely new call."""
from __future__ import annotations

import copy
import json
import shutil
import unittest
from unittest.mock import patch

from colombo.brain.mcp_server import AgentService
from colombo.brain.model_calls import CodexBackend
from colombo.configuration import PROJECT_ROOT
from test_backend import FakeProcess
import test_mcp as mcp_helpers
import test_brain_service as fixtures


PASS = {"verdict": "pass", "summary": "Synthetic deadline fixture", "findings": []}


class AuditDeadlineTests(unittest.TestCase):
    prepare_call = mcp_helpers.MCPServerTests.prepare_call

    def setUp(self):
        fixtures.create_fixture(self)
        config = self.store.get_meta("config")
        config["brain"]["timeout_seconds"] = 300
        config["audit"]["timeout_seconds"] = 120
        self.store.set_meta(config=config)
        self.call_id = "budget-parent"
        self.budget = {"started_at_unix": 1000, "deadline_unix": 1300, "timeout_seconds": 300,
                       "audit_timeout_seconds": 120, "submission_reserve_seconds": 45}
        self.work = self.prepare_call("brain", "plan", self.call_id, call_budget=self.budget)
        self.manifest = json.loads((self.work / "call.json").read_text())
        original = json.loads((self.work / "context.json").read_text())
        original.pop("call_budget")
        self.manifest.update(started_at=1000, timeout_seconds=300,
                             input={"role": "brain", "stage": "plan", "context": original})
        (self.work / "call.json").write_text(json.dumps(self.manifest))
        self.service = AgentService(self.store.root, "brain", "plan", self.call_id)

    def call(self, request_id="one"):
        return self.service.audit("Check P implies P", {"claim": "P implies P"}, request_id=request_id)

    def test_late_new_request_is_refused_without_request_record_counter_or_launch(self):
        with patch("colombo.brain.research_store.time.time", return_value=1272.555), patch("colombo.brain.evidence_audit.run_audit") as run:
            with self.assertRaisesRegex(ValueError, "5-second"):
                self.call()
            run.assert_not_called()
        self.assertEqual(self.store.get_meta("model_call_count", 0), 0)
        self.assertEqual(self.store.get_meta("audit_call_count", 0), 0)
        self.assertEqual(self.store.unresolved_audits(), [])
        self.assertEqual(self.store.reference_count("audit"), 0)
        with self.store._connect() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM requests").fetchone()[0], 0)
        self.assertFalse((self.store.root / "audits").exists())

    def test_full_audit_fits_until_hard_boundary_and_late_replay_reuses_original(self):
        # 175 seconds is the hard last start; the suggested 135 seconds must
        # not reduce the existing call allocation or become an implicit limit.
        with patch("colombo.brain.research_store.time.time", return_value=1175), patch("colombo.brain.evidence_audit.run_audit", return_value=PASS) as run:
            first = self.call()
            with patch("colombo.brain.research_store.time.time", return_value=1400):
                second = self.call()
            self.assertEqual(first, second)
            self.assertEqual(run.call_count, 1)
        self.assertEqual(self.store.get_meta("model_call_count"), 1)
        self.assertEqual(self.store.get_meta("audit_call_count"), 1)
        request = self.store.get_request("audit:" + first["audit_id"])["payload"]
        self.assertEqual(set(request["input"]), {"goal", "inputs", "records", "materials"})
        self.assertNotIn("call_budget", request)
        with patch("colombo.brain.research_store.time.time", return_value=1175.001), patch("colombo.brain.evidence_audit.run_audit") as run:
            with self.assertRaisesRegex(ValueError, "5-second"):
                self.call("different")
            run.assert_not_called()
        self.assertEqual(self.store.get_meta("model_call_count"), 1)

    def test_deadline_cannot_be_changed_independently_of_frozen_call_identity(self):
        for field, value in (("deadline_unix", 2300), ("started_at_unix", 999),
                             ("timeout_seconds", 600), ("audit_timeout_seconds", 1),
                             ("submission_reserve_seconds", 0), ("deadline_unix", True)):
            with self.subTest(field=field, value=value), patch("colombo.brain.evidence_audit.run_audit") as run:
                self.service.context["call_budget"] = {**self.budget, field: value}
                with self.assertRaisesRegex(ValueError, "call_budget"):
                    self.call()
                run.assert_not_called()
        self.assertEqual(self.store.get_meta("model_call_count", 0), 0)

    def unlimited_parent(self):
        config = self.store.get_meta("config")
        config["brain"]["timeout_seconds"] = "unlimited"
        self.store.set_meta(config=config)
        budget = {**self.budget, "timeout_seconds": "unlimited", "deadline_unix": None,
                  "submission_reserve_seconds": 0, "recommended_audit_start_by_unix": None,
                  "audit_wait_counts_toward_call": True}
        context = {**self.service.context, "call_budget": budget}
        manifest = {**self.manifest, "timeout_seconds": "unlimited"}
        (self.work / "context.json").write_text(json.dumps(context), encoding="utf-8")
        (self.work / "call.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.service = AgentService(self.store.root, "brain", "plan", self.call_id)
        return budget

    def test_unlimited_parent_allows_late_audits_and_preserves_audit_own_limit(self):
        self.unlimited_parent()
        with patch("colombo.brain.research_store.time.time", return_value=999999), patch("colombo.brain.evidence_audit.run_audit", return_value=PASS) as run:
            first = self.call()
            self.assertEqual(self.call(), first)
            second = self.call("another")
        self.assertEqual(first["verdict"], "pass")
        self.assertEqual(second["verdict"], "pass")
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args.args[1]["audit"]["timeout_seconds"], 120)
        self.assertEqual(self.store.get_meta("model_call_count"), 2)

    def test_unlimited_budget_requires_manifest_and_run_config_agreement(self):
        budget = self.unlimited_parent()
        for changed in ("manifest", "config", "frozen_input"):
            with self.subTest(changed=changed), patch("colombo.brain.evidence_audit.run_audit") as run:
                config = self.store.get_meta("config")
                config["brain"]["timeout_seconds"] = 300 if changed == "config" else "unlimited"
                self.store.set_meta(config=config)
                self.service.manifest = {**self.manifest, "timeout_seconds": "unlimited"}
                if changed == "manifest":
                    self.service.manifest["timeout_seconds"] = 300
                elif changed == "frozen_input":
                    self.service.manifest["input"] = {"context": {"call_budget": self.budget}}
                self.service.context["call_budget"] = copy.deepcopy(budget)
                with self.assertRaisesRegex(ValueError, "call_budget"):
                    self.call()
                run.assert_not_called()
        self.assertEqual(self.store.get_meta("model_call_count", 0), 0)

    def test_unlimited_budget_rejects_malformed_or_forged_fields(self):
        budget = self.unlimited_parent()
        for field, value in (("deadline_unix", 1300), ("timeout_seconds", 300),
                             ("started_at_unix", 999), ("audit_timeout_seconds", 1),
                             ("submission_reserve_seconds", 45), ("submission_reserve_seconds", False),
                             ("recommended_audit_start_by_unix", 1135),
                             ("audit_wait_counts_toward_call", False), ("unexpected", None)):
            with self.subTest(field=field, value=value), patch("colombo.brain.evidence_audit.run_audit") as run:
                self.service.context["call_budget"] = {**budget, field: value}
                with self.assertRaisesRegex(ValueError, "call_budget"):
                    self.call()
                run.assert_not_called()
        self.assertEqual(self.store.get_meta("model_call_count", 0), 0)

    def test_old_context_without_budget_preserves_prior_behavior(self):
        self.prepare_call("brain", "plan", "legacy-fixture")
        service = AgentService(self.store.root, "brain", "plan", "legacy-fixture")
        with patch("colombo.brain.research_store.time.time", return_value=999999), patch("colombo.brain.evidence_audit.run_audit", return_value=PASS) as run:
            result = service.audit("Check a fixture", {}, request_id="one")
        self.assertEqual(result["verdict"], "pass")
        self.assertEqual(run.call_count, 1)

    def test_late_pending_replay_remains_unresolved_and_never_gets_a_new_allocation(self):
        with patch("colombo.brain.research_store.time.time", return_value=1100), patch("colombo.brain.evidence_audit.run_audit", side_effect=KeyboardInterrupt) as run:
            with self.assertRaises(KeyboardInterrupt):
                self.call()
            with patch("colombo.brain.research_store.time.time", return_value=1500):
                with self.assertRaisesRegex(ValueError, "without a confirmed result"):
                    self.call()
            self.assertEqual(run.call_count, 1)
        self.assertEqual(self.store.get_meta("audit_call_count"), 1)
        self.assertEqual(len(self.store.unresolved_audits()), 1)

    def check_actual_backend_context(self, timeout_seconds):
        project = self.folder / "backend-project"
        shutil.copytree(PROJECT_ROOT / "agents", project / "agents")
        (project / "run.py").write_text("")
        auth = self.folder / "auth"
        auth.mkdir()
        (auth / "auth.json").write_text('{"fixture":"not-real"}')
        executable = self.folder / "codex.exe"
        executable.write_bytes(b"fixture; never executed")
        config = self.store.get_meta("config")
        config["runtime"].update(auth_home=str(auth), codex_bin=str(executable))
        config["brain"]["timeout_seconds"] = timeout_seconds
        self.store.set_meta(config=config, pending_call={"call_id": "real-backend-fixture", "role": "brain", "stage": "plan"})
        backend = CodexBackend(project, config)
        seen = []

        def conversation(process, prompt, timeout):
            service = AgentService(self.store.root, "brain", "plan", "real-backend-fixture")
            budget = service.context["call_budget"]
            self.assertEqual(len(budget), 7)
            self.assertIs(budget["audit_wait_counts_toward_call"], True)
            if timeout_seconds == "unlimited":
                self.assertIsNone(timeout)
                self.assertIsNone(budget["deadline_unix"])
                self.assertIsNone(budget["recommended_audit_start_by_unix"])
                self.assertEqual(budget["submission_reserve_seconds"], 0)
            else:
                self.assertEqual(budget["recommended_audit_start_by_unix"], budget["started_at_unix"] + 135)
            self.assertNotIn("call_budget", service.manifest["input"]["context"])
            first = service.audit("Check P", {"claim": "P"}, request_id="from-backend")
            with patch("colombo.brain.research_store.time.time", return_value=(budget["deadline_unix"] or budget["started_at_unix"] + 999999) + 1):
                replay = service.audit("Check P", {"claim": "P"}, request_id="from-backend")
            self.assertEqual(first, replay)
            seen.append(first)
            # Commit a synthetic plan through the same domain ledger so the
            # real backend completes its receipt path without a real model.
            self.store.write_record("plan", {"rationale": "Synthetic backend fixture", "tasks": []},
                                    request_id="submission:real-backend-fixture")

        with patch("colombo.brain.model_calls.managed_popen", side_effect=lambda command, **kw: FakeProcess(conversation, command, **kw)) as launch, \
             patch("colombo.brain.model_calls.process_identity", return_value={"pid": 12345, "start_token": "fixture", "platform": "windows"}), \
             patch("colombo.brain.model_calls.terminate_tree", side_effect=lambda process, **kwargs: (process.wait() == 0)), \
             patch("colombo.brain.model_calls.close_process_job"), \
             patch("colombo.brain.evidence_audit.run_audit", return_value=PASS) as audit_model:
            backend.invoke("brain", "plan", self.store.root, "real-backend-fixture", "Fixture", {})
        self.assertEqual(len(seen), 1)
        self.assertEqual(audit_model.call_count, 1)
        self.assertEqual(launch.call_count, 1)

    def test_actual_backend_context_and_manifest_are_accepted_by_audit_service(self):
        self.check_actual_backend_context(300)

    def test_actual_unlimited_backend_context_and_manifest_are_accepted_by_audit_service(self):
        self.check_actual_backend_context("unlimited")

    def test_optional_budget_fields_are_checked_and_unknown_fields_rejected(self):
        for extra in ({"recommended_audit_start_by_unix": 1136},
                      {"recommended_audit_start_by_unix": True},
                      {"audit_wait_counts_toward_call": False},
                      {"audit_wait_counts_toward_call": 1}, {"unexpected": 1}):
            with self.subTest(extra=extra), patch("colombo.brain.evidence_audit.run_audit") as run:
                self.service.context["call_budget"] = {**self.budget, **extra}
                with self.assertRaisesRegex(ValueError, "call_budget"):
                    self.call()
                run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
