"""Explicit, scoped research-result import through the existing task interface."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.cell.research_records import map_record_references
from colombo.cell.research_records import record_references
from colombo.cell.record_store import Store
from colombo.cell.record_store import StoreError
from colombo.cell.subcell_dispatch import Tasks
from colombo.cell.subcell_dispatch import TaskError
from colombo.cell.settings import get_settings
from colombo.cell.settings import run_fields


def ref(record, **extra):
    return {**{name: record[name] for name in ("kind", "id", "revision")}, **extra}


class ResearchImportTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for name in ("CELL_SETTINGS_FILE", "CELL_RUN_DIR", "CELL_MODEL", "CELL_ROLE",
                     "CELL_REASONING_EFFORT", "CELL_AGENT_TIMEOUT"):
            os.environ.pop(name, None)
        temporary = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2])
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        settings = get_settings()
        settings["parallel"]["max_depth"] = 2
        (self.root / "run.json").write_text(json.dumps({"settings": settings, **run_fields(settings),
                                                       "task_depth": 0, "role": "prover"}), encoding="utf-8")
        self.store = Store(self.root / "memory")
        self.target = self.store.archive("claims", {"proposition": {"conclusion": "n+n is even for integer n"}}, "main")
        self.tasks = Tasks(self.root)
        launch = patch("colombo.cell.subcell_dispatch.subprocess.Popen")
        self.launch = launch.start()
        self.addCleanup(launch.stop)
        self.launch.return_value.pid = 12345
        self.task = self.tasks.spawn_task(ref(self.target), "Study a local subproblem")
        self.child = Store(Path(self.task["workspace"]) / "memory")

    def certify_argument(self, payload):
        candidate = self.child.archive("arguments", payload)
        review = self.child.write_review({"target": ref(candidate), "verdict": "pass", "summary": "Checked",
            "findings": [], "properties": [], "conclusions": [
                {**item, "verdict": "pass", "reason": "The exact target follows"}
                for item in candidate["payload"].get("conclusions", [])]})
        return self.child.archive("arguments", {**candidate["payload"], "status": "proved", "audit_id": review["id"]},
                                  candidate["id"], candidate["revision"])

    def checked_example(self):
        example = self.child.archive("examples", {"construction": "n=2", "properties": [
            {"id": "p1", "statement": "n is an integer", "status": "pending"},
            {"id": "p2", "statement": "n+n=4", "status": "pending"}]})
        review = self.child.write_review({"target": ref(example), "verdict": "pass", "summary": "Checked",
            "findings": [], "properties": [{"id": item["id"], "verdict": "pass", "reason": "exact"}
                                            for item in example["payload"]["properties"]]})
        payload = copy.deepcopy(example["payload"])
        for item in payload["properties"]:
            item.update(status="checked", audit_id=review["id"])
        return self.child.archive("examples", payload, example["id"], 1)

    def test_editable_origin_cannot_choose_an_imported_identity(self):
        source = self.child.archive("claims", {"proposition": "The actual child statement"})
        unrelated = self.store.archive("claims", {
            "proposition": "An unrelated parent statement",
            "origin": {"task_id": self.task["task_id"], "record_ref": ref(source)}}, "misleading-origin")
        reply = self.tasks.import_records(self.task["task_id"], [ref(source)], "first-import")
        imported = self.store.get(**reply["record_refs"][0])
        self.assertNotEqual(imported["id"], unrelated["id"])
        self.assertEqual(imported["payload"]["proposition"], source["payload"]["proposition"])
        mapping = json.loads((Path(self.task["workspace"]).parent / "import-map.json").read_text())
        self.assertEqual(mapping, [{"source": ref(source), "record_id": imported["id"]}])
        repeated = self.tasks.import_records(self.task["task_id"], [ref(source)], "another-request")
        self.assertEqual(repeated["record_refs"], reply["record_refs"])

    def test_selective_graph_maps_targets_subjects_provenance_and_properties(self):
        claim = self.child.archive("claims", {"proposition": {"conclusion": "2+2=4"},
                                               "derived_from": ref(self.target)}, "local-claim")
        source = self.child.archive("sources", {"title": "Elementary arithmetic", "locator": "Section 1"})
        example = self.checked_example()
        argument = self.certify_argument({"proof": "Substitute n=2", "status": "candidate",
            "conclusions": [{"target": ref(claim), "relation": "supports"}],
            "subject_refs": [ref(example, property_ids=["p2"])],
            "dependencies": [ref(example, property_ids=["p2"])], "source_refs": [ref(source)]})
        attempt = self.child.archive("attempts", {"target_ref": ref(claim), "skill": "prove",
            "produced_refs": [ref(argument)], "route_review": {"decision": "continue", "reason": "The local result is useful",
                                                               "evidence_refs": [ref(example, property_ids=["p1"])]}})
        hidden = self.child.archive("claims", {"proposition": {"conclusion": "Unselected research"}})
        reply = self.tasks.collect_task(self.task["task_id"], import_refs=[ref(attempt)], request_id="chosen", detail="full")
        result = reply["import_result"]
        mapping = {item["source"]["id"]: item["imported"] for item in result["mapped_refs"]}
        self.assertNotIn(hidden["id"], mapping)
        self.assertEqual(mapping[self.target["id"]], ref(self.target))
        parent_argument = self.store.get("arguments", mapping[argument["id"]]["id"])
        self.assertEqual(parent_argument["payload"]["conclusions"][0]["target"], mapping[claim["id"]])
        self.assertEqual(parent_argument["payload"]["source_refs"][0], mapping[source["id"]])
        self.assertEqual(parent_argument["payload"]["dependencies"][0]["property_ids"], ["p2"])
        self.assertEqual(parent_argument["payload"]["status"], "candidate")
        self.assertNotIn("audit_id", parent_argument["payload"])
        parent_example = self.store.get("examples", mapping[example["id"]]["id"])
        self.assertTrue(all(item["status"] == "pending" and "audit_id" not in item
                            for item in parent_example["payload"]["properties"]))
        self.assertEqual(parent_argument["payload"]["origin"]["record_ref"], ref(argument))
        self.assertEqual(self.store.retrieve(kinds=["reviews"])["count"], 0)

    def test_reads_do_not_import_and_same_name_local_record_does_not_merge(self):
        payload = {"proposition": {"conclusion": "A separately discovered assertion"}}
        parent = self.store.archive("claims", payload, "same-name")
        local = self.child.archive("claims", payload, "same-name")
        before = self.store.snapshot()
        self.tasks.collect_task(self.task["task_id"], detail="full")
        self.assertEqual(self.store.snapshot(), before)
        result = self.tasks.import_records(self.task["task_id"], [ref(local)], "copy")
        self.assertNotEqual(result["record_refs"][0]["id"], parent["id"])
        self.assertEqual(self.store.get("claims", parent["id"])["payload"], payload)

    def test_retry_and_reuse_keep_first_import_identity_and_selection_is_bound(self):
        claim = self.child.archive("claims", {"proposition": {"conclusion": "x=x"}})
        argument = self.child.archive("arguments", {"status": "partial", "proof": "A partial derivation",
            "conclusions": [{"target": ref(claim), "relation": "supports"}]})
        first = self.tasks.import_records(self.task["task_id"], [ref(argument)], "save")
        before = self.store.snapshot()
        again = self.tasks.import_records(self.task["task_id"], [ref(argument)], "save")
        self.assertEqual(first, again)
        self.assertEqual(self.store.snapshot(), before)
        reused = self.tasks.import_records(self.task["task_id"], [ref(argument)], "another-selection")
        self.assertEqual(reused["record_refs"], first["record_refs"])
        imported = self.store.get("arguments", first["record_refs"][0]["id"])
        self.assertEqual(imported["payload"]["status"], "partial")
        with self.assertRaises((StoreError, TaskError)):
            self.tasks.import_records(self.task["task_id"], [ref(claim), ref(argument)], "save")

    def test_unknown_or_bad_revision_reference_does_not_partly_save(self):
        claim = self.child.archive("claims", {"proposition": {"conclusion": "x=x"}})
        hidden = self.store.archive("claims", {"proposition": {"conclusion": "Not granted"}})
        before = self.store.snapshot()
        for invalid in (ref(hidden), ref(claim, revision=999)):
            with self.subTest(invalid=invalid), self.assertRaises(TaskError):
                self.tasks.import_records(self.task["task_id"], [ref(claim), invalid], "bad")
            self.assertEqual(self.store.snapshot(), before)

    def test_declared_links_only_and_origin_remains_child_provenance(self):
        identity = ref(self.target)
        payload = {"target_ref": identity, "origin": {"record_ref": identity},
                   "parameters": {"arbitrary": identity},
                   "conclusions": [{"target": identity, "relation": "supports"}],
                   "properties": [{"id": "p", "dependencies": [identity]}]}
        mapped = map_record_references(payload, lambda reference, role: {**reference, "id": "mapped"})
        self.assertEqual(mapped["target_ref"]["id"], "mapped")
        self.assertEqual(mapped["origin"]["record_ref"], identity)
        self.assertEqual(mapped["parameters"]["arbitrary"], identity)
        self.assertEqual([item["role"] for item in record_references(payload)], ["target", "target", "dependency"])

    def test_spawn_grants_declared_targets_subjects_but_not_unrelated_records(self):
        lemma = self.store.archive("claims", {"proposition": {"conclusion": "A local lemma"}})
        example = self.store.archive("examples", {"construction": "x=0", "properties": [
            {"id": "p", "statement": "x is real", "status": "pending"}]})
        hidden = self.store.archive("claims", {"proposition": {"conclusion": "Unrelated"}})
        argument = self.store.archive("arguments", {"status": "candidate", "proof": "To check",
            "conclusions": [{"target": ref(lemma), "relation": "supports"}],
            "subject_refs": [ref(example, property_ids=["p"])], "unrelated_data": ref(hidden)})
        task = self.tasks.spawn_task(ref(argument), "Check the candidate")
        granted = Store(Path(task["workspace"]) / "memory")
        self.assertTrue(granted.get("claims", lemma["id"])["read_only"])
        self.assertEqual(granted.get("examples", example["id"])["property_ids"], ["p"])
        with self.assertRaises(KeyError):
            granted.get("claims", hidden["id"])

    def test_spawn_keeps_external_citation_available_without_granting_unrelated_sources(self):
        source = self.store.archive("sources", {"title": "A theorem reference", "url": "https://example.org/theorem"})
        hidden = self.store.archive("sources", {"title": "An unselected source"})
        claim = self.store.archive("claims", {"proposition": {"conclusion": "A cited theorem"},
            "citation": {"locator": "Theorem 1", "source_refs": [ref(source)]}})
        task = self.tasks.spawn_task(ref(claim), "Check this cited target")
        granted = Store(Path(task["workspace"]) / "memory")
        self.assertEqual(granted.get("sources", source["id"])["payload"], source["payload"])
        with self.assertRaises(KeyError):
            granted.get("sources", hidden["id"])

    def test_nested_grant_and_import_cannot_widen_a_property_selection(self):
        example = self.store.archive("examples", {"construction": "x=0", "properties": [
            {"id": "p1", "statement": "x is real", "status": "pending"},
            {"id": "p2", "statement": "x is an integer", "status": "pending"}]})
        task = self.tasks.spawn_task(ref(self.target), "Use the selected property",
                                     context_refs=[ref(example, property_ids=["p1"])])
        nested = Tasks(Path(task["workspace"]))
        with self.assertRaisesRegex(TaskError, "granted context"):
            nested.spawn_task(ref(example, property_ids=["p2"]), "Cannot widen access")
        with self.assertRaisesRegex(TaskError, "selection exceeds"):
            self.tasks.import_records(task["task_id"], [ref(example, property_ids=["p2"])], "bad-scope")
        imported = self.tasks.import_records(task["task_id"], [ref(example)], "existing-parent")
        self.assertEqual(imported["record_refs"], [ref(example, property_ids=["p1"])])

    def test_example_scope_grows_under_one_identity_and_preserves_parent_certificate(self):
        extra = self.child.archive("claims", {"proposition": {"conclusion": "A premise only p2 needs"}})
        example = self.child.archive("examples", {"construction": "x=0", "properties": [
            {"id": "p1", "statement": "x is real", "status": "pending"},
            {"id": "p2", "statement": "x is an integer", "status": "pending", "dependencies": [ref(extra)]}]})
        first = self.tasks.import_records(self.task["task_id"], [ref(example, property_ids=["p1"])], "p1")
        parent_ref = first["record_refs"][0]
        self.assertNotIn(extra["id"], {item["source"]["id"] for item in first["mapped_refs"]})
        local = self.store.get("examples", parent_ref["id"])
        self.assertEqual([item["id"] for item in local["payload"]["properties"]], ["p1"])
        review = self.store.write_review({"target": ref(local), "verdict": "pass", "summary": "Exact",
            "findings": [], "properties": [{"id": "p1", "verdict": "pass", "reason": "0 is real"}]})
        payload = copy.deepcopy(local["payload"])
        payload["properties"][0].update(status="checked", audit_id=review["id"])
        certified = self.store.archive("examples", payload, local["id"], local["revision"])
        second = self.tasks.import_records(self.task["task_id"], [ref(example, property_ids=["p2"])], "p2")
        self.assertEqual(second["record_refs"][0]["id"], local["id"])
        self.assertEqual(second["record_refs"][0]["property_ids"], ["p2"])
        extended = self.store.get("examples", local["id"])
        self.assertEqual(extended["payload"]["properties"][0], certified["payload"]["properties"][0])
        self.assertEqual(extended["current_trust"]["properties"]["p1"]["state"], "supported")
        self.assertEqual(extended["payload"]["properties"][1]["status"], "pending")
        self.assertEqual(extended["payload"]["metadata"]["cell_import_properties"], ["p1", "p2"])
        self.store.archive("examples", {**extended["payload"], "title": "User's current title"},
                           extended["id"], extended["revision"])
        repeated = self.tasks.import_records(self.task["task_id"], [ref(example, property_ids=["p2"])], "p2")
        self.assertEqual(repeated, second)
        self.assertEqual(self.store.get("examples", local["id"])["payload"]["title"], "User's current title")

    def test_failed_commit_retains_frozen_plan_for_retry_without_partial_records(self):
        claim = self.child.archive("claims", {"proposition": {"conclusion": "x=x"}})
        argument = self.child.archive("arguments", {"status": "candidate", "proof": "Reflexivity",
            "conclusions": [{"target": ref(claim), "relation": "supports"}]})
        before = self.store.snapshot()
        with patch.object(self.tasks.store, "_commit", side_effect=OSError("Simulated storage interruption")):
            with self.assertRaises(OSError):
                self.tasks.import_records(self.task["task_id"], [ref(argument)], "interrupted")
        self.assertEqual(self.store.snapshot(), before)
        result = self.tasks.import_records(self.task["task_id"], [ref(argument)], "interrupted")
        self.assertEqual(len({item["imported"]["id"] for item in result["mapped_refs"]}), 2)
        self.assertEqual(self.tasks.import_records(self.task["task_id"], [ref(argument)], "interrupted"), result)

    def test_same_local_identity_in_different_tasks_stays_distinct(self):
        sibling = self.tasks.spawn_task(ref(self.target), "An independent discovery")
        other = Store(Path(sibling["workspace"]) / "memory")
        payload = {"proposition": {"conclusion": "A local finding"}}
        one = self.child.archive("claims", payload, "C1")
        two = other.archive("claims", payload, "C1")
        first = self.tasks.import_records(self.task["task_id"], [ref(one)], "copy")
        second = self.tasks.import_records(sibling["task_id"], [ref(two)], "copy")
        self.assertNotEqual(first["record_refs"][0]["id"], second["record_refs"][0]["id"])

    def test_pending_premises_remain_pending_in_a_recovered_partial_argument(self):
        premise = self.child.archive("arguments", {"status": "partial", "proof": "Still missing a case"})
        target = self.child.archive("claims", {"proposition": {"conclusion": "A conditional target"}})
        partial = self.child.archive("arguments", {"status": "partial", "proof": "Conditional step",
            "dependencies": [ref(premise)], "conclusions": [{"target": ref(target), "relation": "supports"}]})
        self.assertEqual(partial["current_trust"]["state"], "dependency_blocked")
        result = self.tasks.import_records(self.task["task_id"], [ref(partial)], "pending")
        imported = self.store.get("arguments", result["record_refs"][0]["id"])
        self.assertEqual(imported["payload"]["status"], "partial")
        self.assertEqual(imported["current_trust"]["state"], "dependency_blocked")

    def test_interrupted_scope_update_never_overwrites_a_concurrent_parent_revision(self):
        example = self.checked_example()
        first = self.tasks.import_records(self.task["task_id"], [ref(example, property_ids=["p1"])], "first-property")
        identity = first["record_refs"][0]["id"]
        with patch.object(self.tasks.store, "_commit", side_effect=OSError("Before commit")):
            with self.assertRaises(OSError):
                self.tasks.import_records(self.task["task_id"], [ref(example, property_ids=["p2"])], "second-property")
        current = self.store.get("examples", identity)
        self.store.archive("examples", {**current["payload"], "title": "Concurrent parent edit"},
                           identity, current["revision"])
        with self.assertRaisesRegex(StoreError, "current expected_revision"):
            self.tasks.import_records(self.task["task_id"], [ref(example, property_ids=["p2"])], "second-property")
        untouched = self.store.get("examples", identity)
        self.assertEqual([item["id"] for item in untouched["payload"]["properties"]], ["p1"])
        self.assertEqual(untouched["payload"]["title"], "Concurrent parent edit")
        recovered = self.tasks.import_records(self.task["task_id"], [ref(example, property_ids=["p2"])], "retry-after-conflict")
        self.assertEqual(recovered["record_refs"][0]["id"], identity)
        self.assertEqual(self.store.get("examples", identity)["payload"]["title"], "Concurrent parent edit")


if __name__ == "__main__":
    unittest.main()
