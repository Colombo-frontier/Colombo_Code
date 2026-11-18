"""Version identities, request replay and narrow reads without content digests."""
from __future__ import annotations

import copy
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest
from unittest.mock import patch

from colombo.configuration import load_config
from colombo.shared.file_io import Path as IOPath, freeze_json
from colombo.brain.pruning import validate_prune_audit
from colombo.brain.mcp_server import AgentService
from colombo.brain.research_store import Store, StoreError

PROJECT = Path(__file__).resolve().parents[2]
PASS = {"verdict": "pass", "summary": "Synthetic scoped implication holds.", "findings": []}


class HashlessBrainTests(unittest.TestCase):
    def setUp(self):
        parent = PROJECT / "validation/tmp"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="version-contract-", dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = Store.create(self.root / "run", "Synthetic implication fixture", [], load_config())
        self.source = self.store.write_record("result", {"task_id": "T0001", "attempt_id": "A0001",
            "accepted": True, "artifacts": [], "summary": "Synthetic source identity"})
        from brain_fixtures import confirm_result
        confirm_result(self.store, self.source, claims=[{"id":"P", "statement":"P", "assumptions":[],
            "scope":"All objects", "kind":"lemma", "expression":"", "evidence_paths":[]}])
        self.target = self.make_task("T0002")
        self.identity = {"role": "brain", "stage": "process_results", "call_id": "audit-parent"}
        work = self.store.root / "brain/calls/audit-parent"
        freeze_json(work / "context.json", {**self.identity, "task_snapshot": [self.target], "result_refs": [self.source]})
        freeze_json(work / "call.json", self.identity)
        self.store.set_meta(pending_call=self.identity)
        self.service = AgentService(self.store.root, **self.identity)

    def make_task(self, tid):
        spec = {"instructions": "Deduce the target from the source with the same domain.",
            "deliverables": ["Proof of Q"], "completion_criteria": ["All stated objects, no new assumptions"],
            "responsibility": {"claim": "Q", "assumptions": [], "scope": "All objects",
                "goal_ids": ["G0"], "proof_step_ids": [], "problem_id": "P1", "route_group": "Q", "retain": False}}
        assignment = self.store.write_record("assignment", {"task_id": tid, "spec": spec})
        task = {"task_id": tid, "active_attempt": "A0001", "state": "running", "assignment_ref": assignment}
        self.store.save_task(task)
        return task

    def relation(self):
        return {"task_id": "T0002", "attempt_id": "A0001", "reason": "subsumed",
            "evidence_refs": [self.source["id"]], "premises": [{"result_ref": self.source["id"],
                "statement": "P", "assumptions": [], "scope": "All objects"}],
            "relation_explanation": "P implies Q by the stated implication.",
            "scope_check": "The same objects and assumptions.", "covered_deliverables": ["Proof of Q"]}

    def test_record_request_replay_preserves_json_types(self):
        first = self.store.write_record("note", {"value": True}, request_id="typed")
        self.assertEqual(self.store.write_record("note", {"value": True}, request_id="typed"), first)
        with self.assertRaises(ValueError):
            self.store.write_record("note", {"value": 1}, request_id="typed")
        self.assertEqual(set(first), {"id", "revision"})

    def test_selected_artifact_read_does_not_open_sibling_bodies(self):
        selected, sibling = self.store.root / "selected.txt", self.store.root / "sibling.txt"
        selected.write_text("selected material", encoding="utf-8")
        sibling.write_text("unrelated material", encoding="utf-8")
        ref = self.store.write_record("material", {"artifacts": [{"path": "selected.txt"}, {"path": "sibling.txt"}]})
        real_read = IOPath.read_bytes
        opened = []
        def checked(path):
            opened.append(path.name)
            if path.name == "sibling.txt":
                self.fail("Reading one file must not read its sibling")
            return real_read(path)
        with patch.object(IOPath, "read_bytes", checked):
            page = self.store.read_artifact(ref, "selected.txt", limit=8)
        self.assertEqual(page["text"], "selected")
        self.assertEqual(opened.count("selected.txt"), 1)
        self.assertNotIn("sibling.txt", opened)

    def test_audit_anonymous_replay_distinguishes_json_types(self):
        with patch("colombo.brain.evidence_audit.run_audit", return_value=PASS) as run:
            true = self.service.audit("Check input", {"value": True})
            number = self.service.audit("Check input", {"value": 1})
            self.assertEqual(self.service.audit("Check input", {"value": True}), true)
        self.assertNotEqual(true["audit_id"], number["audit_id"])
        self.assertEqual(run.call_count, 2)
        self.assertEqual(self.store.get_meta("model_call_count"), 2)

    def test_concurrent_audit_reserves_one_process_with_and_without_request_id(self):
        for request_id in (None, "explicit"):
            with self.subTest(request_id=request_id):
                entered, release = threading.Event(), threading.Event()
                replies, errors = [], []
                inputs = {"case": request_id}
                def held(*_):
                    entered.set()
                    if not release.wait(10):
                        raise RuntimeError("Fixture did not release audit")
                    return copy.deepcopy(PASS)
                def invoke():
                    try:
                        replies.append(self.service.audit("Check concurrent input", inputs, request_id=request_id))
                    except BaseException as exc:
                        errors.append(exc)
                before = self.store.get_meta("model_call_count", 0)
                with patch("colombo.brain.evidence_audit.run_audit", side_effect=held) as run:
                    first = threading.Thread(target=invoke, daemon=True)
                    first.start()
                    try:
                        self.assertTrue(entered.wait(5))
                        with self.assertRaisesRegex(ValueError, "already started"):
                            self.service.audit("Check concurrent input", inputs, request_id=request_id)
                    finally:
                        release.set()
                        first.join(10)
                    self.assertFalse(first.is_alive())
                    self.assertFalse(errors, str(errors))
                    self.assertEqual(self.service.audit("Check concurrent input", inputs, request_id=request_id), replies[0])
                    self.assertEqual(run.call_count, 1)
                self.assertEqual(self.store.get_meta("model_call_count"), before + 1)

    def test_diagnostic_log_changes_do_not_invalidate_relation_audit(self):
        def audited(_project, _config, work, _input):
            work.mkdir(parents=True)
            (work / "events.jsonl").write_text("original diagnostic", encoding="utf-8")
            return copy.deepcopy(PASS)
        relation = self.relation()
        with patch("colombo.brain.evidence_audit.run_audit", side_effect=audited):
            reply = self.service.audit("Compare propositions", {"prune_relations": [relation]})
        candidate = {**relation, "audit_ref": reply["ref"]["id"]}
        log = self.store.root / "audits" / reply["audit_id"] / "workspace/events.jsonl"
        log.write_text("changed diagnostic", encoding="utf-8")
        self.assertEqual(validate_prune_audit(self.store, candidate, self.target)["ref"], reply["ref"])
        log.unlink()
        self.assertEqual(validate_prune_audit(self.store, candidate, self.target)["ref"], reply["ref"])

    def test_passing_audit_cannot_be_applied_to_another_task_or_premise(self):
        relation = self.relation()
        with patch("colombo.brain.evidence_audit.run_audit", return_value=PASS):
            reply = self.service.audit("Compare propositions", {"prune_relations": [relation]})
            generic = self.service.audit("An unrelated check", {"question": "Q"})
        candidate = {**relation, "audit_ref": reply["ref"]["id"]}
        self.assertEqual(validate_prune_audit(self.store, candidate, self.target)["ref"], reply["ref"])
        other = self.make_task("T0003")
        cases = [({**candidate, "task_id": "T0003"}, other),
                 ({**candidate, "attempt_id": "A0002"}, {**self.target, "active_attempt": "A0002"}),
                 ({**candidate, "audit_ref": generic["ref"]["id"]}, self.target),
                 ({**candidate, "premises": [{**candidate["premises"][0], "scope": "A smaller subset"}]}, self.target)]
        for changed, task in cases:
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                validate_prune_audit(self.store, changed, task)

    def test_new_store_has_no_content_digest_column_and_old_formats_are_rejected(self):
        self.assertEqual(Store(self.store.root).get_meta("storage_version"), 4)
        with closing(sqlite3.connect(self.store.db_path)) as db:
            self.assertEqual(list(db.execute("PRAGMA table_info(records)")), [])
            self.assertEqual({r[0] for r in db.execute("SELECT name FROM documents")},
                             {"research", "proof_draft", "working_notes"})
        for name, version in (("missing", None), ("old", 2), ("float", 3.0), ("bool", True)):
            old = self.root / name
            old.mkdir()
            with closing(sqlite3.connect(old / "state.sqlite")) as db:
                db.execute("CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT)")
                if version is not None:
                    db.execute("INSERT INTO meta VALUES('storage_version',?)", (json.dumps(version),))
                db.commit()
            with self.subTest(version=version), self.assertRaises(StoreError):
                Store(old)


if __name__ == "__main__":
    unittest.main()
