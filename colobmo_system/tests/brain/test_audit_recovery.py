"""Recover stopped audit execution without launching a model or inventing a verdict."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import colombo.brain.evidence_audit as auditing
from colombo.configuration import PROJECT_ROOT
from colombo.configuration import load_config
from colombo.brain.controller import OracleController, NeedsAttention
from colombo.shared.file_io import freeze_json
from colombo.brain.research_store import Store


PASS = {"verdict": "pass", "summary": "Synthetic audit opinion", "findings": []}
GOAL = "Check the supplied implication"
INPUTS = {"premise": "P", "conclusion": "Q"}


class AuditRecoveryTests(unittest.TestCase):
    def setUp(self):
        parent = PROJECT_ROOT / "validation/tmp"
        parent.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="audit-recovery-", dir=parent)
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name).resolve()
        self.assertTrue(self.folder.is_relative_to(PROJECT_ROOT / "validation/tmp"))
        self.project = self.folder / "project"
        self.auth = self.folder / "original-auth"
        self.auth.mkdir()
        (self.auth / "auth.json").write_text("synthetic original credential", encoding="utf-8")
        config = load_config()
        config["runtime"]["auth_home"] = str(self.auth)
        self.store = Store.create(self.folder / "run", "Audit recovery fixture", [], config)
        self.call_id = "C00001"
        identity = {"call_id": self.call_id, "role": "brain", "stage": "plan"}
        self.store.set_meta(pending_call={**identity, "prompt": "fixture", "context": {}}, model_call_count=1)
        self.call_work = self.store.root / "brain/calls" / self.call_id
        self.call_work.mkdir(parents=True)
        freeze_json(self.call_work / "context.json", identity)
        self.parent = {**identity, "status": "timeout", "pid": 11001,
            "process_identity": {"pid": 11001, "platform": "windows", "start_token": "parent-created"},
            "process_exit_confirmed": True, "process_tree_terminated": True}
        self.save_parent()
        self.child = {"role": "audit", "status": "running", "pid": 11002,
            "process_identity": {"pid": 11002, "platform": "windows", "start_token": "child-created"}}
        self.addCleanup(patch.stopall)
        patch("colombo.brain.evidence_audit.PROJECT_ROOT", self.project).start()
        self.dead = patch("colombo.brain.evidence_audit.process_matches", return_value=False).start()
        self.launch = patch("colombo.brain.evidence_audit.run_audit", side_effect=self.worker).start()
        self.worker_returns = False
        self.raw_final = False

    def save_parent(self):
        (self.call_work / "call.json").write_text(json.dumps(self.parent), encoding="utf-8")

    def worker(self, project, config, work, payload):
        self.work = work
        work.mkdir(parents=True, exist_ok=True)
        freeze_json(work / "input.json", payload)
        freeze_json(work / "process.json", self.child)
        if self.raw_final:
            freeze_json(work / "final.json", PASS)
            (work / "events.jsonl").write_text(json.dumps({"type": "agent_message", "text": json.dumps(PASS)}))
        if self.worker_returns:
            return copy.deepcopy(PASS)
        raise KeyboardInterrupt

    def start(self, **kwargs):
        with self.assertRaises(KeyboardInterrupt):
            auditing.audit(self.store, self.call_id, GOAL, INPUTS, request_id="one", **kwargs)
        saved = self.store.unresolved_audits(self.call_id)[0]
        self.key, self.request = saved["id"], saved["payload"]
        return saved

    def recover(self):
        return auditing.reconcile_interrupted_audits(self.store, self.call_id)

    def test_interruption_is_error_even_with_raw_pass_and_replay_never_relaunches(self):
        self.raw_final = True
        self.start()
        home = self.project / ".runtime/audit" / ("a" * 32)
        home.mkdir(parents=True)
        (home / "config.toml").write_text('[projects.' + json.dumps(str(self.work)) + ']\ntrust_level="trusted"\n')
        (home / "auth.json").write_text("synthetic copied credential")
        unrelated = self.project / ".runtime/audit" / ("b" * 32)
        unrelated.mkdir()
        (unrelated / "auth.json").write_text("keep this unrelated copy")
        details = self.recover()
        self.assertEqual(details[0]["basis"], "confirmed_interruption")
        self.assertEqual(details[0]["auth_cleanup"]["status"], "removed_or_absent")
        self.assertFalse((home / "auth.json").exists())
        self.assertTrue((unrelated / "auth.json").exists())
        self.assertTrue((self.auth / "auth.json").exists())
        first = auditing.audit(self.store, self.call_id, GOAL, INPUTS, request_id="one")
        second = auditing.audit(self.store, self.call_id, GOAL, INPUTS, request_id="one")
        self.assertEqual(first, second)
        self.assertEqual(first["audit_id"], self.request["audit_id"])
        self.assertEqual(first["status"], "error")
        self.assertEqual(first["error"]["type"], "InterruptedAudit")
        self.assertNotIn("verdict", first)
        self.assertEqual(self.store.get_request(self.key)["state"], "confirmed")
        self.assertEqual(self.store.reference_count("audit"), 1)
        self.assertEqual(self.store.get_meta("model_call_count"), 2)
        self.assertEqual(self.store.get_meta("audit_call_count"), 1)
        manifest = json.loads((self.work / "process.json").read_text())
        self.assertEqual(manifest["status"], "interrupted")
        self.assertEqual(manifest["reconciled_from_status"], "running")
        self.assertTrue(manifest["process_exit_confirmed"])
        self.assertTrue(manifest["process_tree_terminated"])
        self.assertEqual(manifest["process_identity"], self.child["process_identity"])
        self.assertNotIn("ended_at", manifest)
        self.assertNotIn("returncode", manifest)
        saved_manifest = (self.work / "process.json").read_bytes()
        self.assertEqual(self.recover(), [])
        self.assertEqual((self.work / "process.json").read_bytes(), saved_manifest)
        self.assertEqual(self.launch.call_count, 1)

    def test_active_unknown_parent_or_unterminated_tree_remains_blocked(self):
        self.start()
        for field, value in (("process_exit_confirmed", False), ("process_tree_terminated", False)):
            with self.subTest(field=field):
                self.parent[field] = value
                self.save_parent()
                with self.assertRaises(auditing.AuditRecoveryBlocked):
                    self.recover()
                self.parent[field] = True
        self.save_parent()
        for alive in (True, None):
            with self.subTest(process_match=alive):
                self.dead.return_value = alive
                with self.assertRaises(auditing.AuditRecoveryBlocked):
                    self.recover()
        self.assertEqual(self.store.get_request(self.key)["state"], "pending")
        self.assertFalse((self.work.parent / "result.json").exists())
        self.assertEqual(self.store.reference_count("audit"), 0)

    def test_active_or_uninspectable_child_is_not_overridden_by_parent_cleanup_flag(self):
        self.start()
        for alive in (True, None):
            self.dead.side_effect = lambda identity, alive=alive: False if identity["pid"] == 11001 else alive
            with self.assertRaises(auditing.AuditRecoveryBlocked):
                self.recover()
        self.assertEqual(self.store.get_request(self.key)["state"], "pending")

    def test_frozen_input_and_binding_mismatches_are_rejected(self):
        self.start(_binding={"kind": "prune_relations", "version": 2})
        for path, original in ((self.work.parent / "request.json", self.request),
                               (self.work / "input.json", self.request["input"])):
            changed = copy.deepcopy(original)
            payload = changed["input"] if "input" in changed else changed
            payload["binding"]["version"] = True
            path.write_text(json.dumps(changed))
            with self.assertRaisesRegex(auditing.AuditRecoveryBlocked, "binding"):
                self.recover()
            path.write_text(json.dumps(original))
        self.parent["call_id"] = "C-other"
        self.save_parent()
        with self.assertRaisesRegex(auditing.AuditRecoveryBlocked, "identity"):
            self.recover()
        self.assertEqual(self.store.reference_count("audit"), 0)

    def test_complete_frozen_outcome_is_reused_after_record_write_interruption(self):
        self.worker_returns = True
        with patch.object(self.store, "write_record", side_effect=KeyboardInterrupt):
            self.start()
        self.assertTrue((self.work.parent / "result.json").exists())
        self.assertEqual(self.recover()[0]["basis"], "existing_frozen_outcome")
        response = auditing.audit(self.store, self.call_id, GOAL, INPUTS, request_id="one")
        self.assertEqual(response["verdict"], "pass")
        manifest = json.loads((self.work / "process.json").read_text())
        self.assertEqual(manifest["status"], "completed")
        self.assertEqual(manifest["reconciled_from_status"], "running")
        self.assertNotIn("ended_at", manifest)
        self.assertNotIn("returncode", manifest)
        self.assertEqual(self.launch.call_count, 1)

    def test_existing_terminal_process_diagnostics_are_not_rewritten(self):
        self.child.update(status="timeout", ended_at=1234.5, returncode=9)
        self.start()
        original = (self.work / "process.json").read_bytes()
        self.recover()
        self.assertEqual((self.work / "process.json").read_bytes(), original)

    def test_dynamic_call_budget_is_not_part_of_the_frozen_invocation_identity(self):
        self.start()
        context = json.loads((self.call_work / "context.json").read_text())
        self.parent["input"] = {"role": "brain", "stage": "plan", "context": copy.deepcopy(context)}
        self.save_parent()
        context["call_budget"] = {"started_at_unix": 1000, "deadline_unix": 1300,
            "timeout_seconds": 300, "audit_timeout_seconds": 120, "submission_reserve_seconds": 45}
        (self.call_work / "context.json").write_text(json.dumps(context))
        self.assertEqual(self.recover()[0]["basis"], "confirmed_interruption")

    def test_reservation_interrupted_before_first_file_freeze_is_recovered_without_launch(self):
        payload = {"goal": GOAL, "inputs": INPUTS, "records": [], "materials": []}
        saved, created = self.store.reserve_audit(self.call_id, "before-freeze", payload)
        self.assertTrue(created)
        details = self.recover()
        self.assertEqual(details[0]["basis"], "confirmed_interruption")
        response = auditing.audit(self.store, self.call_id, GOAL, INPUTS, request_id="before-freeze")
        self.assertEqual(response["audit_id"], saved["payload"]["audit_id"])
        self.assertEqual(response["error"]["type"], "InterruptedAudit")
        self.launch.assert_not_called()

    def test_recovery_interrupted_after_record_commit_reuses_that_same_record(self):
        self.start()
        with patch.object(self.store, "save_request", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.recover()
        ref = self.store.request_record(self.key)
        self.assertIsNotNone(ref)
        self.assertEqual(self.recover()[0]["basis"], "existing_formal_record")
        self.assertEqual(self.store.get_request(self.key)["result"]["ref"], ref)
        self.assertEqual(self.store.reference_count("audit"), 1)
        self.assertEqual(self.store.get_meta("audit_call_count"), 1)
        self.assertEqual(self.launch.call_count, 1)

    def test_formal_record_is_reused_after_receipt_write_interruption(self):
        self.worker_returns = True
        with patch.object(self.store, "save_request", side_effect=KeyboardInterrupt):
            self.start()
        old_ref = self.store.request_record(self.key)
        self.assertIsNotNone(old_ref)
        self.assertEqual(self.recover()[0]["basis"], "existing_formal_record")
        self.assertEqual(self.store.get_request(self.key)["result"]["ref"], old_ref)
        self.assertEqual(self.store.reference_count("audit"), 1)
        self.assertEqual(self.launch.call_count, 1)

    def test_unknown_formal_error_is_preserved_but_original_receipt_becomes_confirmed(self):
        def unresolved(project, config, work, payload):
            try:
                self.worker(project, config, work, payload)
            except KeyboardInterrupt:
                raise RuntimeError("Synthetic unconfirmed termination")
        self.launch.side_effect = unresolved
        before = auditing.audit(self.store, self.call_id, GOAL, INPUTS, request_id="one")
        self.assertTrue(before["execution_unknown"])
        key = "audit:" + before["audit_id"]
        self.assertEqual(self.store.get_request(key)["state"], "unknown")
        record = self.store.read_record(before["ref"])
        self.recover()
        self.assertEqual(self.store.get_request(key)["state"], "confirmed")
        self.assertEqual(self.store.read_record(before["ref"]), record)
        self.assertEqual(auditing.audit(self.store, self.call_id, GOAL, INPUTS, request_id="one"), before)
        self.assertEqual(self.store.reference_count("audit"), 1)

    def test_ambiguous_temporary_auth_matches_are_retained_with_explanation(self):
        self.start()
        homes = []
        for name in ("a", "b"):
            home = self.project / ".runtime/audit" / (name * 32)
            home.mkdir(parents=True)
            (home / "config.toml").write_text('[projects.' + json.dumps(str(self.work)) + ']\ntrust_level="trusted"\n')
            (home / "auth.json").write_text("synthetic copy")
            homes.append(home)
        cleanup = self.recover()[0]["auth_cleanup"]
        self.assertEqual(cleanup["status"], "not_cleaned")
        self.assertEqual(cleanup["matches"], 2)
        self.assertTrue(all((home / "auth.json").exists() for home in homes))

    def test_controller_preserves_pending_until_audit_reconciled_and_blocks_new_identity_bypass(self):
        self.start()
        backend = Mock()
        backend.reconcile_call.return_value = {"state": "failed"}
        controller = OracleController(self.project, self.store.root, backend=backend, adapter=Mock())
        self.parent["process_tree_terminated"] = False
        self.save_parent()
        with self.assertRaises(NeedsAttention):
            controller._reconcile_pending()
        self.assertEqual(self.store.get_meta("pending_call")["call_id"], self.call_id)
        self.store.set_meta(pending_call={"call_id": "new-call", "role": "brain", "stage": "plan"})
        with self.assertRaisesRegex(ValueError, "earlier audit"):
            auditing.audit(self.store, "new-call", GOAL, INPUTS, request_id="different-name")
        self.store.set_meta(pending_call=None)
        for cls in (OracleController,):
            blocked = cls(self.project, self.store.root, backend=backend, adapter=Mock())
            with self.assertRaisesRegex(NeedsAttention, "pending audits"):
                blocked.calls.reserve("brain", "plan", "new", {})
        self.store.set_meta(pending_call={"call_id": self.call_id, "role": "brain", "stage": "plan"})
        self.parent["process_tree_terminated"] = True
        self.save_parent()
        controller._reconcile_pending()
        self.assertIsNone(self.store.get_meta("pending_call"))
        self.assertEqual(self.store.get_request(self.key)["state"], "confirmed")
        self.assertEqual(self.store.get_meta("model_call_count"), 2)
        self.assertEqual(self.launch.call_count, 1)


if __name__ == "__main__":
    unittest.main()
