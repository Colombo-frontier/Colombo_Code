"""Local objections suspend fixed support and only confirmed errors withdraw it."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.cell.verifier.local_audit import audit
from colombo.cell.verifier.challenge import challenge_argument
from colombo.shared.experiment_artifacts import manifest_for
from colombo.cell.record_store import Store
from colombo.cell.record_store import StoreError
from colombo.cell.record_store import AuditRequired
from colombo.cell.subcell_dispatch import Tasks
from colombo.cell.subcell_dispatch import TaskError
from test_confirmed_trust import confirmed_packet
from test_confirmed_trust import ref


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return path


class LocalChallengeTrustTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        temporary = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2])
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store = Store(self.root / "memory")

    def prove(self, payload=None, *, record_id=None, expected_revision=None, store=None):
        store = store or self.store
        candidate = store.archive("arguments", payload or {"proof": "Divide by x without considering zero.",
                                                           "status": "candidate"},
                                  record_id=record_id, expected_revision=expected_revision)
        review = store.write_review({"target": ref(candidate), "verdict": "pass", "properties": []})
        return store.archive("arguments", dict(candidate["payload"], status="proved", audit_id=review["id"]),
                             record_id=candidate["id"], expected_revision=candidate["revision"])

    def begin(self, target, identifier="objection-one"):
        reason = "The proof divides by x although x=0 is allowed."
        frozen = {"challenge_id": identifier, "target_ref": ref(target), "reason": reason, "evidence_refs": []}
        save(self.root / "challenges" / identifier / "input.json", frozen)
        result = self.store.begin_argument_challenge(identifier, ref(target), reason, [])
        return result

    def resolution(self, pending, outcome="withdrawn", *, confirmed=True):
        value = pending["payload"]
        identifier = value["challenge_id"]
        report = {"challenge_id": identifier,
                  "verdict": "sustain" if outcome == "withdrawn" else "dismiss",
                  "summary": "Checked the division and the zero case.", "findings": []}
        if outcome == "withdrawn":
            report["findings"] = [{"id": "zero", "kind": "gap", "location": "Division by x",
                                   "explanation": "The missing x=0 case is allowed by the hypotheses."}]
        directory = self.root / "challenges" / identifier
        report_path = directory / "report.json"
        save(report_path, report)
        confirmation = None
        confirmation_path = None
        if confirmed:
            confirmation = {"challenge_id": identifier,
                            "report_revision": 1, "verdict": "confirmed",
                            "summary": "Independently recomputed the zero case.",
                            "findings": [{"finding_id": item["id"], "status": "supported", "reason": "x=0 is allowed."}
                                         for item in report["findings"]],
                            "decisive_steps": [{"location": "Division by x", "status": "supported",
                                                "reason": "Checked the hypotheses and calculation."}], "new_findings": []}
            confirmation_path = directory / "confirmation.json"
            save(confirmation_path, confirmation)
        return dict(challenge_id=identifier, outcome=outcome, report_revision=1, first_report=report,
                    first_report_path=report_path, confirmation=confirmation, confirmation_path=confirmation_path)

    def state(self, record):
        return self.store.get(record["kind"], record["id"], record["revision"])["current_trust"]["state"]

    def registered_import_task(self, child_root):
        identifier = "a" * 32
        save(self.root / "tasks" / identifier / "task.json",
             {"task_id": identifier, "workspace": str(child_root), "status": "completed"})
        return identifier

    def test_suspension_blocks_old_versions_and_dependents_without_editing_history(self):
        first = self.prove()
        second = self.prove({"proof": "Apply A.", "dependencies": [ref(first)]})
        original = (self.root / "memory/arguments.json").read_bytes()
        pending = self.begin(first)
        self.assertEqual(self.state(first), "suspended")
        self.assertEqual(self.store.get("arguments", first["id"], 1)["current_trust"]["state"], "suspended")
        self.assertEqual(self.state(second), "dependency_blocked")
        self.assertEqual((self.root / "memory/arguments.json").read_bytes(), original)
        result = self.store.resolve_argument_challenge(**self.resolution(pending))
        self.assertEqual(result["payload"]["status"], "withdrawn")
        self.assertEqual(self.state(first), "withdrawn")
        self.assertEqual(self.state(second), "dependency_blocked")
        self.assertEqual((self.root / "memory/arguments.json").read_bytes(), original)
        self.assertEqual(self.store.get("reviews", first["payload"]["audit_id"])["payload"]["verdict"], "pass")
        self.assertEqual(self.begin(first), result)
        self.assertEqual(self.store.resolve_argument_challenge(**self.resolution(pending)), result)

    def test_concurrent_objections_and_global_withdrawal_cannot_be_cleared_by_dismissal(self):
        target = self.prove()
        first = self.begin(target, "first")
        second = self.begin(target, "second")
        self.store.resolve_argument_challenge(**self.resolution(first, "dismissed", confirmed=False))
        self.assertEqual(self.state(target), "suspended")
        self.store.resolve_argument_challenge(**self.resolution(second))
        third = self.begin(target, "third")
        self.store.resolve_argument_challenge(**self.resolution(third, "dismissed", confirmed=False))
        self.assertEqual(self.state(target), "withdrawn")
        other = self.prove({"proof": "A different inference."})
        local = self.begin(other, "global-and-local")
        self.store.apply_confirmed_review(**confirmed_packet(self.root, [other]))
        self.store.resolve_argument_challenge(**self.resolution(local, "dismissed", confirmed=False))
        self.assertEqual(self.state(other), "withdrawn")

    def test_dismissal_restores_same_certificate_and_dependent(self):
        target = self.prove()
        dependent = self.prove({"proof": "Use the unchanged A.", "dependencies": [ref(target)]})
        pending = self.begin(target)
        self.store.resolve_argument_challenge(**self.resolution(pending, "dismissed", confirmed=False))
        self.assertEqual(self.state(target), "supported")
        self.assertEqual(self.state(dependent), "supported")

    def test_pending_copy_origin_and_reaudit_cannot_launder_certificate(self):
        target = self.prove()
        pending = self.begin(target)
        with self.assertRaises(AuditRequired):
            self.store.archive("arguments", target["payload"], record_id=target["id"], expected_revision=2)
        copied = {key: value for key, value in target["payload"].items() if key != "audit_id"}
        copied.update(status="candidate", origin={"task_id": "some-child"})
        alias = self.store.archive("arguments", copied, record_id="alias")
        self.assertEqual(self.state(alias), "suspended")
        result = audit(self.root, "arguments", alias["id"], 1, reviewer=lambda *_: {
            "verdict": "pass", "summary": "The copied proof seems fine.", "findings": [], "properties": []})
        self.assertEqual(result["review"]["payload"]["verdict"], "uncertain")
        self.assertEqual(self.state(alias), "suspended")
        self.store.resolve_argument_challenge(**self.resolution(pending))
        self.assertEqual(self.state(alias), "withdrawn")

    def test_real_repair_requires_new_audit_and_explicit_dependency_update(self):
        target = self.prove()
        dependent = self.prove({"proof": "Apply the result.", "dependencies": [ref(target)]})
        pending = self.begin(target)
        repaired = self.store.archive("arguments", {"proof": "First handle x=0; then divide only when x is nonzero."},
                                      record_id=target["id"], expected_revision=2)
        with self.assertRaises(AuditRequired):
            self.store.archive("arguments", dict(repaired["payload"], status="proved", audit_id=target["payload"]["audit_id"]),
                               record_id=target["id"], expected_revision=3)
        result = audit(self.root, "arguments", target["id"], 3, reviewer=lambda *_: {
            "verdict": "pass", "summary": "Both cases now follow.", "findings": [], "properties": []})
        self.assertEqual(result["record"]["current_trust"]["state"], "supported")
        self.assertEqual(self.state(target), "suspended")
        self.assertEqual(self.state(dependent), "dependency_blocked")
        updated = self.prove({"proof": "Apply the repaired result.", "dependencies": [ref(result["record"])]},
                             record_id=dependent["id"], expected_revision=2)
        self.assertEqual(self.state(updated), "supported")
        self.store.resolve_argument_challenge(**self.resolution(pending))
        self.assertEqual(self.state(target), "withdrawn")
        self.assertEqual(self.state(result["record"]), "supported")

    def test_unconfirmed_wrong_revision_and_incomplete_confirmation_stay_suspended(self):
        target = self.prove()
        pending = self.begin(target)
        with self.assertRaises(StoreError):
            self.store.resolve_argument_challenge(**self.resolution(pending, confirmed=False))
        packet = self.resolution(pending)
        packet["confirmation"]["findings"][0]["status"] = "unsupported"
        save(packet["confirmation_path"], packet["confirmation"])
        with self.assertRaises(StoreError):
            self.store.resolve_argument_challenge(**packet)
        packet = self.resolution(pending)
        packet["report_revision"] = 2
        with self.assertRaises(StoreError):
            self.store.resolve_argument_challenge(**packet)
        self.assertEqual(self.state(target), "suspended")
        with self.assertRaises(StoreError):
            self.store.archive("reviews", {"status": "dismissed"})

    def test_negative_reaudit_of_certificate_uses_confirmation_and_preserves_revision(self):
        target = self.prove()
        dependent = self.prove({"proof": "Use A.", "dependencies": [ref(target)]})
        seen = []
        def checker(_, work):
            data = json.loads((work / "request.json").read_text(encoding="utf-8"))
            seen.append(data)
            report = json.loads((work / "first_report.json").read_text(encoding="utf-8"))
            return {"challenge_id": report["challenge_id"], 
                    "report_revision": data["report_revision"], "verdict": "confirmed",
                    "summary": "The missing zero case is a real gap.",
                    "findings": [{"finding_id": item["id"], "status": "supported", "reason": "Recomputed."}
                                 for item in report["findings"]],
                    "decisive_steps": [{"location": "Division", "status": "supported", "reason": "Zero is allowed."}],
                    "new_findings": []}
        result = audit(self.root, "arguments", target["id"], target["revision"], reviewer=lambda *_: {
            "verdict": "fail", "summary": "Missing zero case.", "findings": ["Division excludes zero."], "properties": []},
            challenge_checker=checker)
        self.assertEqual(len(seen), 1)
        self.assertEqual(result["challenge"]["status"], "withdrawn")
        self.assertNotIn("review", result)
        self.assertIn("review_ref", result)
        self.assertEqual(result["record"]["revision"], 2)
        self.assertEqual(self.state(target), "withdrawn")
        self.assertEqual(self.state(dependent), "dependency_blocked")

    def test_uncertain_certificate_is_pending_but_new_candidate_failure_is_ordinary(self):
        target = self.prove()
        result = audit(self.root, "arguments", target["id"], 2, reviewer=lambda *_: {
            "verdict": "uncertain", "summary": "The zero case needs clarification.", "findings": ["Cannot resolve zero."], "properties": []})
        self.assertEqual(result["challenge"]["status"], "pending")
        self.assertNotIn("review", result)
        self.assertEqual(self.store.resolve_record_refs([result["review_ref"]])[0]["payload"]["verdict"], "uncertain")
        self.assertEqual(self.state(target), "suspended")
        self.assertEqual(result["record"]["revision"], 2)
        candidate = self.store.archive("arguments", {"proof": "A different incomplete proof."})
        failed = audit(self.root, "arguments", candidate["id"], 1, reviewer=lambda *_: {
            "verdict": "fail", "summary": "A step is unjustified.", "findings": ["Missing justification."], "properties": []})
        self.assertNotIn("challenge", failed)
        self.assertEqual(failed["record"]["payload"]["status"], "candidate")
        self.assertEqual(failed["record"]["current_trust"]["state"], "unreviewed")

    def test_negative_reaudit_timeout_does_not_return_unconfirmed_repair_findings(self):
        target = self.prove()
        def timeout(*_):
            raise TimeoutError("Independent review needs another invocation")
        result = audit(self.root, "arguments", target["id"], 2, reviewer=lambda *_: {
            "verdict": "fail", "summary": "An objection needs review.",
            "findings": ["UNCONFIRMED_DETAIL: replace the division immediately."], "properties": []},
            challenge_checker=timeout)
        self.assertEqual(result["challenge"]["status"], "pending")
        self.assertNotIn("review", result)
        self.assertNotIn("UNCONFIRMED_DETAIL", json.dumps(result))
        self.assertIn("not a confirmed repair instruction", result["warning"])
        saved = self.store.resolve_record_refs([result["review_ref"]])[0]
        self.assertEqual(saved["payload"]["verdict"], "fail")
        self.assertEqual(self.state(target), "suspended")

    def test_service_error_cannot_revoke_or_suspend(self):
        target = self.prove()
        result = audit(self.root, "arguments", target["id"], 2, reviewer=lambda *_: {"returncode": 1})
        self.assertEqual(result["review"]["payload"]["verdict"], "service_error")
        self.assertNotIn("challenge", result)
        self.assertEqual(self.state(target), "supported")

    def test_dismissal_after_negative_opinion_requires_independent_recheck(self):
        target = self.prove()
        pending = self.begin(target)
        state = {"challenge_id": pending["payload"]["challenge_id"],
                 "had_adverse_report": True}
        save(self.root / "challenges" / state["challenge_id"] / "state.json", state)
        with self.assertRaises(StoreError):
            self.store.resolve_argument_challenge(**self.resolution(pending, "dismissed", confirmed=False))
        self.assertEqual(self.state(target), "suspended")
        self.store.resolve_argument_challenge(**self.resolution(pending, "dismissed"))
        self.assertEqual(self.state(target), "supported")

    def test_parent_suspension_marks_late_child_stale_and_snapshot_is_readonly(self):
        target = self.prove()
        tasks = Tasks(self.root)
        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
            launch.return_value.pid = 12345
            task = tasks.spawn_task(ref(target), "Study a consequence")
        child_root = Path(task["workspace"])
        child = Store(child_root / "memory")
        saved = child.archive("claims", {"statement": "Useful work should remain available."})
        self.begin(target)
        # Grants are finite launch snapshots; collect performs the parent-side comparison.
        self.assertEqual(child.get("arguments", target["id"], 2)["current_trust"]["state"], "supported")
        with self.assertRaises(ValueError):
            challenge_argument(child_root, ref(target), "Check inherited proof")
        collected = tasks.collect_task(task["task_id"], detail="full")
        self.assertEqual(collected["acceptance"], "stale")
        self.assertEqual(collected["records"][0]["payload"], saved["payload"])
        self.assertEqual(collected["stale_context"][0]["current_trust"]["state"], "suspended")
        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
            launch.return_value.pid = 12346
            repair = tasks.spawn_task(ref(target), "Study the suspended proof")
        granted = Store(Path(repair["workspace"]) / "memory").get("arguments", target["id"], 2)
        self.assertEqual(granted["current_trust"]["state"], "suspended")

    def test_import_provenance_cannot_hide_suspended_parent_copy(self):
        target = self.prove()
        child_root = self.root / "isolated-child"
        child = Store(child_root / "memory")
        copied = child.archive("arguments", {"proof": target["payload"]["proof"], "status": "candidate"})
        self.begin(target)
        task_id = self.registered_import_task(child_root)
        imported = Tasks(self.root)._import_experiment(task_id, child, copied)
        local = self.store.resolve_record_refs([imported["record_ref"]])[0]
        self.assertEqual(local["current_trust"]["state"], "suspended")
        blocked_source = dict(copied, current_trust={"state": "suspended"})
        with self.assertRaises(TaskError):
            Tasks(self.root)._import_experiment(task_id, child, blocked_source)

    def test_child_local_objection_blocks_identical_grant_without_changing_parent(self):
        target = self.prove()
        tasks = Tasks(self.root)
        with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
            launch.return_value.pid = 12345
            task = tasks.spawn_task(ref(target), "Examine this argument")
        child_root = Path(task["workspace"])
        child = Store(child_root / "memory")
        copied = self.prove({"proof": target["payload"]["proof"]}, store=child)
        dependent = self.prove({"proof": "Apply the inherited argument.", "dependencies": [ref(target)]}, store=child)
        frozen = {"challenge_id": "local-copy-objection", "target_ref": ref(copied),
                  "reason": "The zero case is omitted.", "evidence_refs": []}
        save(child_root / "challenges/local-copy-objection/input.json", frozen)
        child.begin_argument_challenge("local-copy-objection", ref(copied), frozen["reason"], [])
        self.assertEqual(child.get("arguments", target["id"], 2)["current_trust"]["state"], "suspended")
        self.assertEqual(child.get("arguments", dependent["id"], 2)["current_trust"]["state"], "dependency_blocked")
        self.assertEqual(self.state(target), "supported")
        child.apply_confirmed_review(**confirmed_packet(child_root, [copied]))
        self.assertEqual(child.get("arguments", target["id"], 2)["current_trust"]["state"], "withdrawn")
        self.assertEqual(self.state(target), "supported")

    def test_cached_experiment_import_still_rejects_new_child_objection(self):
        child_root = self.root / "isolated-child"
        child = Store(child_root / "memory")
        premise = self.prove(store=child)
        target = child.archive("claims", {"statement": "Check one value using the premise."})
        data = b"print(1)\n"
        path = child_root / "experiments/sample/code.py"
        path.parent.mkdir(parents=True)
        path.write_bytes(data)
        result = child.write_experiment_result("sample", {
            "question": "Check one value", "target_ref": ref(target), "dependencies": [ref(premise)],
            "parameters": {}, "execution": {"status": "completed"},
            "artifacts": manifest_for({"experiments/sample/code.py": data})})
        tasks = Tasks(self.root)
        task_id = self.registered_import_task(child_root)
        tasks._import_experiment(task_id, child, result)
        frozen = {"challenge_id": "new-objection", "target_ref": ref(premise),
                  "reason": "The zero case is omitted.", "evidence_refs": []}
        save(child_root / "challenges/new-objection/input.json", frozen)
        child.begin_argument_challenge("new-objection", ref(premise), frozen["reason"], [])
        path.unlink()
        current = child.get("experiment_result", result["id"], result["revision"])
        self.assertEqual(current["current_trust"]["state"], "dependency_blocked")
        with self.assertRaises(TaskError):
            tasks._import_experiment(task_id, child, current)

    def test_inherited_objection_cannot_be_laundered_by_child_copy(self):
        target = self.prove()
        pending = self.begin(target)
        tasks = Tasks(self.root)
        for outcome in ("suspended", "withdrawn"):
            if outcome == "withdrawn":
                self.store.resolve_argument_challenge(**self.resolution(pending))
            with patch("colombo.cell.subcell_dispatch.subprocess.Popen") as launch:
                launch.return_value.pid = 12345
                task = tasks.spawn_task(ref(target), "Find a genuine repair")
            child_root = Path(task["workspace"])
            child = Store(child_root / "memory")
            copied = child.archive("arguments", {"proof": target["payload"]["proof"]}, record_id="copied")
            self.assertEqual(copied["current_trust"]["state"], outcome)
            result = audit(child_root, "arguments", copied["id"], 1, reviewer=lambda *_: {
                "verdict": "pass", "summary": "The unchanged copy looks fine.", "findings": [], "properties": []})
            self.assertEqual(result["review"]["payload"]["verdict"], "uncertain")
            self.assertEqual(result["record"]["current_trust"]["state"], outcome)

    def test_global_confirmation_requires_exact_nonempty_actual_check_ids(self):
        target = self.prove()
        for ids in ([], [7, 8], list(range(1, 31))):
            packet = confirmed_packet(self.root, [target])
            packet["confirmation"]["covered_check_ids"] = ids
            save(packet["confirmation_path"], packet["confirmation"])
            with self.assertRaises(StoreError):
                self.store.apply_confirmed_review(**packet)
        packet = confirmed_packet(self.root, [target])
        packet["report"].pop("checks")
        save(packet["report_path"], packet["report"])
        save(packet["confirmation_path"], packet["confirmation"])
        with self.assertRaises(StoreError):
            self.store.apply_confirmed_review(**packet)
        self.assertEqual(self.state(target), "supported")


if __name__ == "__main__":
    unittest.main()
