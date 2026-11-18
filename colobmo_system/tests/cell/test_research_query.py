"""Research queries preserve identity, scope, page membership and current trust."""
from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from colombo.cell.record_queries import query
from colombo.cell.record_store import Store
from colombo.cell.record_store import StoreError
from colombo.shared.file_io import Path
from test_confirmed_trust import confirmed_packet


ROOT = Path(__file__).resolve().parents[2]


def ref(record, **extra):
    return {**{key: record[key] for key in ("kind", "id", "revision")}, **extra}


class ResearchQueryTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        temporary = tempfile.TemporaryDirectory(prefix=".research-query-", dir=str(ROOT))
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store = Store(self.root / "memory")

    def claim(self, statement="For every real x, x squared is nonnegative", **extra):
        return self.store.archive("claims", {"proposition": statement, **extra})

    def prove(self, claim, relation="supports", *, proof="Exact supplied reasoning.", dependencies=None):
        argument = self.store.archive("arguments", {"status": "candidate", "proof": proof,
            "dependencies": dependencies or [], "conclusions": [{"target": ref(claim), "relation": relation}]})
        checked = [{**copy.deepcopy(item), "verdict": "pass", "reason": "Verified the exact direction."}
                   for item in argument["payload"]["conclusions"]]
        review = self.store.write_review({"target": ref(argument), "verdict": "pass", "properties": [],
                                         "conclusions": checked})
        return self.store.archive("arguments", {**argument["payload"], "status": "proved", "audit_id": review["id"]},
                                  record_id=argument["id"], expected_revision=argument["revision"])

    def state(self, claim, closing=None):
        return self.store.archive("proof_state", {"routes": [{"route_id": "direct", "target_claim_ref": ref(claim),
            "obligations": [{"id": "lemma", "target_claim_ref": ref(claim), "work_status": "active",
                             "remaining_gap": "Establish the required positive statement.",
                             "closing_argument_ref": ref(closing) if closing else None}]}]})

    def test_fixed_target_and_metadata_revision_find_original_evidence(self):
        claim = self.claim()
        argument = self.prove(claim)
        updated = self.store.archive("claims", {**claim["payload"], "title": "A better display title"},
                                     record_id=claim["id"], expected_revision=1)
        result = query(self.store, target_ref=ref(updated), relations=["supports"], detail="summary")
        self.assertEqual(result["target_ref"], ref(updated))
        self.assertEqual([r["id"] for r in result["records"]], [argument["id"]])
        relationship = result["records"][0]["relation_matches"][0]
        self.assertTrue(relationship["audited"])
        self.assertTrue(relationship["currently_usable"])
        self.assertEqual(relationship["target"], ref(claim))
        other = self.claim("For every nonzero real x, x squared is positive", title="A better display title")
        self.assertEqual(query(self.store, target_ref=ref(other), relations=["supports"])["count"], 0)
        pinned = query(self.store, target_ref=ref(claim))["records"][0]
        self.assertEqual(pinned["revision"], 1)

    def test_directions_pending_relationships_and_actual_dependencies_are_distinct(self):
        claim = self.claim()
        support = self.prove(claim)
        refutation = self.store.archive("arguments", {"status": "candidate", "proof": "A proposed counterexample.",
            "conclusions": [{"target": ref(claim), "relation": "refutes"}]})
        observation = self.store.archive("arguments", {"status": "partial", "subject_refs": [ref(claim)],
                                                       "proof": "Study the statement."})
        user = self.store.archive("arguments", {"status": "candidate", "dependencies": [ref(support)],
                                                "proof": "Use the local result."})
        found = query(self.store, target_ref=ref(claim), relations=["supports", "refutes"],
                      state_filter={"domain": "payload", "value": ["proved", "candidate"]})
        self.assertEqual({r["id"] for r in found["records"]}, {support["id"], refutation["id"]})
        pending = next(r for r in found["records"] if r["id"] == refutation["id"])
        self.assertFalse(pending["relation_matches"][0]["audited"])
        self.assertEqual(query(self.store, target_ref=ref(claim), relations=["uses"])["count"], 0)
        self.assertEqual(query(self.store, target_ref=ref(claim), relations=["subjects"])["records"][0]["id"], observation["id"])
        self.assertEqual(query(self.store, target_ref=ref(support), relations=["uses"])["records"][0]["id"], user["id"])

    def test_unfinished_new_revision_does_not_hide_the_original_certificate(self):
        claim = self.claim()
        proof = self.prove(claim)
        revised = self.store.archive("arguments", {**proof["payload"], "status": "candidate",
            "audit_id": None, "proof": "Try a different derivation, not yet complete."},
            record_id=proof["id"], expected_revision=proof["revision"])
        result = query(self.store, target_ref=ref(claim), relations=["supports"])
        self.assertEqual({r["revision"] for r in result["records"]}, {proof["revision"], revised["revision"]})
        usable = [r for r in result["records"] if r["relation_matches"][0]["currently_usable"]]
        self.assertEqual([ref(r) for r in usable], [ref(proof)])
        self.assertEqual(self.store.get("claims", claim["id"])["current_trust"]["state"], "proved")

    def test_keyword_kind_and_state_dimensions_are_and_with_or_within_lists(self):
        claim = self.claim("needle proposition", status="open")
        other = self.claim("another proposition", status="open")
        source = self.store.archive("sources", {"title": "needle source", "status": "candidate"})
        self.store.archive("attempts", {"summary": "needle", "status": "candidate"})
        result = query(self.store, query="needle", kinds=["claims", "sources"],
                       state_filter={"domain": "payload", "value": ["open", "candidate"]})
        self.assertEqual({r["id"] for r in result["records"]}, {claim["id"], source["id"]})
        self.assertNotIn(other["id"], {r["id"] for r in result["records"]})

    def test_membership_is_stable_across_append_revision_and_cursor_retry(self):
        originals = [self.claim(f"Statement {number}") for number in range(3)]
        first = query(self.store, kinds=["claims"], limit=1)
        second = query(self.store, cursor=first["cursor"])
        extra = self.claim("Created after the scan")
        revised = self.store.archive("claims", {**originals[0]["payload"], "title": "Later metadata"},
                                     record_id=originals[0]["id"], expected_revision=1)
        retry = query(self.store, cursor=first["cursor"])
        self.assertEqual([ref(r) for r in retry["records"]], [ref(r) for r in second["records"]])
        third = query(self.store, cursor=second["cursor"])
        combined = first["records"] + second["records"] + third["records"]
        self.assertEqual({r["id"] for r in combined}, {r["id"] for r in originals})
        self.assertTrue(all(r["revision"] == 1 for r in combined))
        self.assertIsNone(third["cursor"])
        fresh = query(self.store, kinds=["claims"])
        self.assertIn(extra["id"], {r["id"] for r in fresh["records"]})
        self.assertIn(ref(revised), [ref(r) for r in fresh["records"]])

    def test_state_filter_membership_stays_fixed_but_revocation_is_visible(self):
        claim = self.claim()
        proof = self.prove(claim)
        first = query(self.store, kinds=["arguments"], state_filter={"domain": "trust", "value": "supported"})
        self.store.apply_confirmed_review(**confirmed_packet(self.root, [proof]))
        again = query(self.store, cursor=first["page_cursor"])
        self.assertEqual([ref(r) for r in first["records"]], [ref(r) for r in again["records"]])
        self.assertEqual(again["records"][0]["current_trust"]["state"], "withdrawn")
        self.assertFalse(again["records"][0]["state_filter_matches_now"])
        self.assertEqual(query(self.store, kinds=["arguments"],
                               state_filter={"domain": "trust", "value": "supported"})["count"], 0)

    def test_refuted_requirement_is_blocked_and_not_a_satisfied_obligation(self):
        claim = self.claim("For every real x, x squared is strictly positive")
        refutation = self.prove(claim, "refutes", proof="x=0 violates the proposed strict inequality.")
        state = self.state(claim, refutation)
        result = query(self.store, route_id="direct", state_filter={"domain": "obligation", "value": "blocked"})
        self.assertEqual(result["records"], [])
        row = result["obligations"][0]
        self.assertEqual(row["mathematical_state"], "refuted")
        self.assertEqual(row["satisfaction"], "blocked")
        self.assertEqual(row["proof_state_ref"], ref(state))
        self.assertEqual(query(self.store, route_id="direct",
                               state_filter={"domain": "obligation", "value": "satisfied"})["count"], 0)
        work = query(self.store, route_id="direct", state_filter={"domain": "work", "value": "active"})
        self.assertEqual(work["count"], 1)

    def test_obligation_cursor_rechecks_a_previously_valid_closing_argument(self):
        claim = self.claim()
        proof = self.prove(claim)
        self.state(claim, proof)
        result = query(self.store, route_id="direct", state_filter={"domain": "obligation", "value": "satisfied"})
        self.store.apply_confirmed_review(**confirmed_packet(self.root, [proof]))
        retry = query(self.store, cursor=result["page_cursor"], detail="summary")
        self.assertEqual(retry["count"], 1)
        self.assertEqual(retry["obligations"][0]["satisfaction"], "unresolved")
        self.assertFalse(retry["obligations"][0]["state_filter_matches_now"])

    def test_obligation_keyword_must_match_that_obligation_not_a_neighbor(self):
        claim = self.claim()
        state = self.state(claim)
        payload = copy.deepcopy(state["payload"])
        payload["routes"][0]["obligations"].append({"id": "neighbor", "target_claim_ref": ref(claim),
                                                   "remaining_gap": "A unique needle to inspect."})
        self.store.archive("proof_state", payload, record_id=state["id"], expected_revision=1)
        result = query(self.store, query="needle", route_id="direct")
        self.assertEqual([o["id"] for o in result["obligations"]], ["neighbor"])

    def test_events_have_local_upper_bound_without_claiming_full_impact_propagation(self):
        first = self.claim("First")
        self.claim("Second")
        initial = query(self.store, since_event={"scope": "current_workspace", "stream": "memory", "sequence": 0}, limit=1)
        self.assertEqual(initial["records"][0]["event"]["target"], ref(first))
        self.assertFalse(initial["scan"]["complete_trust_change_feed"])
        upper = initial["scan"]["upper_sequence"]
        self.claim("Third, after the stream snapshot")
        page = query(self.store, cursor=initial["cursor"])
        self.assertIsNone(page["cursor"])
        self.assertEqual(page["scan"]["upper_sequence"], upper)
        later = query(self.store, since_event={"scope": "current_workspace", "stream": "memory", "sequence": upper})
        self.assertEqual(later["count"], 1)
        self.assertEqual(later["records"][0]["event"]["sequence"], upper + 1)

    def test_filters_cursor_tampering_and_cross_workspace_cursors_are_rejected(self):
        self.claim()
        result = query(self.store, kinds=["claims"], limit=1)
        invalid = [dict(cursor={"query_id": "invented", "offset": 0}),
                   dict(cursor={**result["page_cursor"], "offset": -1}),
                   dict(cursor={**result["page_cursor"], "offset": 99}),
                   dict(cursor={**result["page_cursor"], "records": []}),
                   dict(cursor=result["page_cursor"], kinds=["arguments"]),
                   dict(cursor=result["page_cursor"], limit=2)]
        for request in invalid:
            with self.subTest(request=request), self.assertRaises(StoreError):
                query(self.store, **request)
        elsewhere = Store(self.root / "other" / "memory")
        with self.assertRaisesRegex(StoreError, "Unknown"):
            query(elsewhere, cursor=result["page_cursor"])

    def test_invalid_mode_combinations_fail_before_registering_a_query(self):
        claim = self.claim()
        invalid = [dict(relations=["supports"]), dict(target_ref=ref(claim), relations=["equivalent"]),
                   dict(route_id="direct", kinds=["arguments"]),
                   dict(route_id="direct", target_ref=ref(claim), relations=["supports"]),
                   dict(route_id="direct", state_filter={"domain": "execution", "value": "completed"}),
                   dict(since_event={"scope": "current_workspace", "stream": "runner", "sequence": 0}),
                   dict(since_event={"scope": "current_workspace", "stream": "memory", "sequence": 999}),
                   dict(state_filter={"domain": "unknown", "value": "proved"}),
                   dict(revision=1)]
        for request in invalid:
            with self.subTest(request=request), self.assertRaises(StoreError):
                query(self.store, **request)
        self.assertFalse((self.root / "memory" / ".queries.json").exists())

    def child(self, example):
        directory = self.root / "child"
        context = directory / "context"
        context.mkdir(parents=True)
        grant = ref(example, property_ids=["public"])
        (context / "manifest.json").write_text(json.dumps({"snapshot_refs": [grant]}), encoding="utf-8")
        (context / "examples.json").write_text(json.dumps({"schema_version": 2, "records": [example]}), encoding="utf-8")
        return Store(directory / "memory"), context

    def test_context_properties_and_reverse_lookup_never_expand_the_grant(self):
        example = self.store.archive("examples", {"construction": "A two-property object", "properties": [
            {"id": "public", "statement": "Public property", "status": "pending"},
            {"id": "private", "statement": "Unshared property", "status": "pending"}]})
        child, _ = self.child(example)
        visible = query(child, target_ref=ref(example))
        self.assertEqual([p["id"] for p in visible["records"][0]["payload"]["properties"]], ["public"])
        with self.assertRaises(StoreError):
            query(child, target_ref=ref(example, property_ids=["private"]))
        with self.assertRaises(StoreError):
            query(child, target_ref=ref(example), include_context=False)
        hidden_claim = self.claim("Not granted to the child")
        with self.assertRaises((StoreError, KeyError)):
            query(child, target_ref=ref(hidden_claim), relations=["uses"])

    def test_cursor_is_invalidated_when_the_context_grant_changes(self):
        example = self.store.archive("examples", {"construction": "x=0", "properties": [
            {"id": "public", "statement": "x is zero", "status": "pending"}]})
        child, context = self.child(example)
        initial = query(child, kinds=["examples"])
        (context / "manifest.json").write_text(json.dumps({"snapshot_refs": []}), encoding="utf-8")
        with self.assertRaisesRegex(StoreError, "context changed"):
            query(child, cursor=initial["page_cursor"])
        self.assertEqual(query(child, kinds=["examples"])["count"], 0)

    def test_summary_is_bounded_and_does_not_repeat_proof_body(self):
        claim = self.claim("x=x " * 2000)
        argument = self.prove(claim, proof="A long proof paragraph. " * 1000)
        result = query(self.store, target_ref=ref(argument), detail="summary")
        row = result["records"][0]
        self.assertNotIn("payload", row)
        self.assertNotIn("proof", row)
        self.assertEqual(row["conclusions"], argument["payload"]["conclusions"])
        short = query(self.store, target_ref=ref(claim), detail="summary")["records"][0]
        self.assertLessEqual(len(short["excerpt"]), self.store.settings["retrieval"]["summary_max_chars"])
        self.assertTrue(short["excerpt_truncated"])
        self.assertEqual(query(self.store, target_ref=ref(claim))["records"][0]["payload"], claim["payload"])

    def test_open_attempt_query_follows_the_precise_local_goal(self):
        claim, other = self.claim("Local goal"), self.claim("Different goal")
        attempt = self.store.archive("attempts", {"target_ref": ref(claim), "status": "active", "skill": "prove"})
        self.store.archive("attempts", {"target_ref": ref(other), "status": "active", "skill": "prove"})
        result = query(self.store, target_ref=ref(claim), relations=["attempts"],
                       state_filter={"domain": "payload", "value": "active"})
        self.assertEqual([r["id"] for r in result["records"]], [attempt["id"]])


if __name__ == "__main__":
    unittest.main()
