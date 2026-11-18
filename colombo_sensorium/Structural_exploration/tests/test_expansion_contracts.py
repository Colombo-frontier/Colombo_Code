"""Expansion recovery/approval contracts across persisted workflow boundaries.

These tests use real SQLite case state, with model/Atlas boundaries replaced by
small records. They do not simulate scientific conclusions or replace the full
offline pipeline acceptance example.
"""
from copy import deepcopy
import tempfile
import unittest
from unittest.mock import Mock, patch

from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.core.store import Workspace, digest
from oracle_atlas.expansion.engine import ExpansionEngine
from oracle_atlas.expansion.validation import checked_review
from oracle_atlas.workflow.engine import Engine


class Records:
    def __init__(self):
        self.items = {}
        self.owners = {}

    def put(self, kind, data, producer="controller", deps=()):
        ref = "sha256:" + digest({"kind": kind, "data": data})
        self.items[ref] = {"kind": kind, "data": deepcopy(data), "producer": producer, "deps": list(deps)}
        self.owners.setdefault(ref, set()).add(producer)
        return ref

    def get(self, ref):
        return deepcopy(self.items[ref])

    def owned(self, ref, job):
        return job in self.owners.get(ref, set())


class ExpansionFlowContracts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.engine = ExpansionEngine.__new__(ExpansionEngine)
        self.engine.ws = Workspace(self.tmp.name)
        self.addCleanup(self.engine.ws.db.close)
        self.engine.artifacts = Records()
        self.engine.config = {"publication": {"require_human_approval": True},
                              "budgets": {"max_science_revisions": 1},
                              "expansion": {"max_batch_jobs": 240}}
        self.engine._batch_scope = None
        self.engine.atlas = Mock()
        self.engine.atlas.version.return_value = "inventory-current"
        self.records = self.engine.artifacts
        self.request_ref = self.records.put("expansion_request", {
            "cutoff_date": "2026-11-09", "max_profiles": 1, "allow_existing_updates": False,
        })
        self.seed_ref = self.records.put("source", {"text": "Frozen seed"})
        self.neighborhood_ref = self.records.put("external_result", {
            "seeds": [{"setting_id": "SEED", "snapshot_ref": self.seed_ref}],
        })
        self.op = {"opportunity_id": "op", "seed_setting_ids": ["SEED"]}
        self.plan_ref = self.records.put("expansion_plan", {"opportunities": [self.op]})
        self.history_ref = self.records.put("external_result", {"cases": []})
        self.batch = {"kind": "expansion", "batch_id": "batch", "request_ref": self.request_ref,
                      "neighborhood_ref": self.neighborhood_ref, "plan_ref": self.plan_ref,
                      "history_ref": self.history_ref, "selected": ["op"], "deferred": [],
                      "case_ids": [], "research_case_ids": [], "status": "planned"}
        self.cid = digest({"batch": "batch", "opportunity": "op"})[:24]
        self.candidate_ref = self.records.put("candidate", {"candidate_id": "candidate"})
        self.expansion_ref = self.records.put("expansion", {"candidate_ref": self.candidate_ref})
        self.reviewer_job = self.engine.ws.create_job("expansion_reviewer", {"subject_ref": self.expansion_ref})
        self.engine.ws.save_job(self.reviewer_job, "complete", {})
        self.review_ref = self.records.put("expansion_review", {"verdict": "approve", "issues": [], "pending_comparisons": [],
            "candidate_ref": self.candidate_ref, "subject_ref": self.expansion_ref}, producer=self.reviewer_job)
        self.identity_ref = self.records.put("identity", {
            "decision": "new", "setting_id": None, "recall_audit": {"inventory_version": "inventory-current"},
        })
        self.identity_review_ref = self.records.put("review", {"verdict": "approve", "issues": []})
        self.case = {"case_id": self.cid, "paper_ref": None, "candidate_ref": self.candidate_ref,
                     "candidate_origin": "atlas_expansion", "candidate_review_ref": self.review_ref,
                     "batch_id": "batch", "budget_scope": self.cid, "opportunity_id": "op",
                     "seed_setting_ids": ["SEED"], "history": [], "jobs": {}, "state": "identity_confirmed",
                     "expansion_ref": self.expansion_ref, "origin_ref": self.records.put("external_result", {}),
                     "cutoff_date": "2026-11-09", "identity_ref": self.identity_ref,
                     "identity_review_ref": self.identity_review_ref}
        self.persist()

    def persist(self):
        self.batch["case_ids"] = [self.cid]
        self.engine.ws.save_run("batch", self.batch)
        self.engine.ws.save_case(self.case)

    def try_resume(self, stage):
        material_ref = self.records.put("external_result", {"new": "source clarification"})
        try:
            return self.engine.resume_expansion_case(self.cid, stage=stage, material_refs=[material_ref])
        except ProtocolError:
            # A rejected explicit action and an honest deferred state are both
            # acceptable; neither may launch the protected downstream work.
            return self.engine.ws.case(self.cid)

    def test_specification_resume_keeps_materials_and_same_request(self):
        material = self.records.put("external_result", {"clarification": "Necessary definition"})
        self.case.pop("candidate_review_ref")
        self.case["specification_material_refs"] = [material]
        self.case["specification_revision"] = {
            "revision": 1, "previous_candidate_ref": self.candidate_ref,
            "previous_artifact_ref": self.expansion_ref, "repair_feedback_ref": self.review_ref,
        }
        self.persist()
        captured = []

        def pending(role, inputs, scope):
            captured.append(deepcopy(inputs))
            return {"id": "pending", "status": "transport_uncertain"}, None

        self.engine._job = pending
        self.engine._specify(self.engine.batch("batch"), self.op)
        self.engine._specify(self.engine.batch("batch"), self.op)
        self.assertEqual(captured[0]["material_refs"], [material])
        self.assertEqual(captured[0], captured[1])

    def test_resume_cannot_bypass_candidate_review(self):
        self.case["candidate_review_ref"] = self.records.put("expansion_review", {"verdict": "defer", "issues": [],
            "candidate_ref": self.candidate_ref, "subject_ref": self.expansion_ref}, producer=self.reviewer_job)
        self.case["state"] = "expansion_defer"
        self.persist()
        with patch.object(Engine, "_advance", return_value=self.case) as downstream:
            self.try_resume("identity")
        downstream.assert_not_called()

    def test_resume_respects_existing_update_scope(self):
        self.case["identity_ref"] = self.records.put("identity", {
            "decision": "existing", "setting_id": "EXISTING", "recall_audit": {"inventory_version": "inventory-current"},
        })
        self.case["state"] = "redirected_existing"
        self.persist()
        with patch.object(Engine, "_advance", return_value=self.case) as downstream:
            self.try_resume("research")
        downstream.assert_not_called()

    def test_resume_does_not_exceed_profile_count_budget(self):
        self.case["state"] = "research_deferred_budget"
        self.batch["research_case_ids"] = ["previous-case-already-consumed-the-slot"]
        self.persist()
        with patch.object(Engine, "_advance", return_value=self.case) as downstream:
            self.try_resume("research")
        downstream.assert_not_called()

    def test_changed_proposal_cannot_reuse_boolean_human_approval(self):
        prepared_ref = self.records.put("prepared", {"bundle_hash": "new-content"})
        proposal_ref = self.records.put("proposal", {"prepared_ref": prepared_ref})
        self.case.update(proposal_ref=proposal_ref, human_approved=True,
                         approved_bundle_hash="old-content", state="ready_for_approval")
        self.persist()
        with patch.object(Engine, "_commit", return_value=self.case) as writer:
            try:
                self.engine._commit(self.engine.ws.case(self.cid))
            except ProtocolError:
                pass
        writer.assert_not_called()

    def test_scientific_revision_clears_previous_human_authorization(self):
        self.case.update(human_approved=True, approved_bundle_hash="previous-content")
        self.persist()
        observed = []

        def inspect(case):
            observed.append(deepcopy(case))
            return case

        with patch.object(Engine, "_advance", side_effect=inspect):
            self.try_resume("research")
        current = self.engine.ws.case(self.cid)
        self.assertFalse(current.get("human_approved", False))
        self.assertNotIn("approved_bundle_hash", current)
        for case in observed:
            self.assertFalse(case.get("human_approved", False))

    def test_publication_refresh_recovers_same_identity_attempt(self):
        profile_ref = self.records.put("profile", {"setting_id": "NEW"})
        research_ref = self.records.put("research", {"action": "new", "candidate_ref": self.candidate_ref,
            "identity_ref": self.identity_ref, "profile_ref": profile_ref})
        proposal_ref = self.records.put("proposal", {"mode": "new", "inventory_version": "old-inventory"})
        profile_review_ref = self.records.put("review", {"verdict": "approve", "subject_ref": proposal_ref})
        self.case.update(research_ref=research_ref, proposal_ref=proposal_ref,
                         profile_review_ref=profile_review_ref, state="ready_for_approval")
        self.persist()
        revisions = []

        def incomplete_identity(case):
            revisions.append(case.get("revision", 0))
            case["state"] = "matcher:transport_uncertain"
            self.engine.ws.save_case(case)
            return case

        self.engine.resolve_identity = incomplete_identity
        self.engine._refresh_for_publication(self.engine.ws.case(self.cid))
        self.engine._refresh_for_publication(self.engine.ws.case(self.cid))
        self.assertTrue(revisions)
        self.assertEqual(len(set(revisions)), 1, "A transport interruption must not start another scientific identity revision")

    def test_newly_approved_peer_is_compared_before_resumed_research(self):
        """Two initially interrupted reviews can both have frozen empty peer sets."""
        peer_candidate = self.records.put("candidate", {"candidate_id": "peer"})
        peer_expansion = self.records.put("expansion", {"candidate_ref": peer_candidate})
        peer_job = self.engine.ws.create_job("expansion_reviewer", {"subject_ref": peer_expansion})
        self.engine.ws.save_job(peer_job, "complete", {})
        peer_review = self.records.put("expansion_review", {"verdict": "approve", "issues": [],
            "candidate_ref": peer_candidate, "subject_ref": peer_expansion, "pending_comparisons": []}, producer=peer_job)
        peer = {**deepcopy(self.case), "case_id": "peer", "candidate_ref": peer_candidate,
                "expansion_ref": peer_expansion, "candidate_review_ref": peer_review,
                "peer_candidate_refs": [], "opportunity_id": "peer-op", "state": "specified"}
        self.case["peer_candidate_refs"] = []
        self.persist()
        self.engine.ws.save_case(peer)
        self.batch["case_ids"].append("peer")
        self.engine.ws.save_run("batch", self.batch)
        roles = []

        def reviewer(role, inputs, scope):
            roles.append(role)
            self.assertEqual(role, "expansion_reviewer", "Reuse the fixed candidate rather than rerunning the producer")
            job = self.engine.ws.create_job(role, inputs)
            self.engine.ws.save_job(job, "complete", {})
            data = {"verdict": "approve", "issues": [], "required_changes": [], "duplicate_of_ref": None,
                    "candidate_ref": inputs["candidate_ref"], "subject_ref": inputs["subject_ref"],
                    "pending_comparisons": [{"candidate_ref": ref, "relation": "distinct", "reason": "Fixture comparison"}
                                            for ref in inputs.get("peer_candidate_refs", [])]}
            ref = self.records.put("expansion_review", data, producer=job)
            return {"id": job, "status": "complete"}, ref

        def research(case):
            pair_covered = False
            for cid in (self.cid, "peer"):
                current = self.engine.ws.case(cid)
                review = self.records.get(current["candidate_review_ref"])["data"]
                other = peer_candidate if cid == self.cid else self.candidate_ref
                pair_covered |= any(r["candidate_ref"] == other and r["relation"] == "distinct"
                                    for r in review.get("pending_comparisons", []))
            self.assertTrue(pair_covered, "No candidate may enter research while an approved peer pair was never compared")
            return case

        self.engine._job = reviewer
        with patch.object(Engine, "_advance", side_effect=research):
            try:
                self.engine._advance(self.engine.ws.case(self.cid))
            except ProtocolError:
                pass
        self.assertNotIn("setting_expander", roles)

    def test_late_duplicate_review_does_not_consume_the_research_slot(self):
        """A resumed peer review can exclude a candidate before research starts."""
        peer_id = digest({"batch": "batch", "opportunity": "peer-op"})[:24]
        peer_candidate = self.records.put("candidate", {"candidate_id": "peer"})
        peer_expansion = self.records.put("expansion", {"candidate_ref": peer_candidate})
        peer_job = self.engine.ws.create_job("expansion_reviewer", {"subject_ref": peer_expansion})
        self.engine.ws.save_job(peer_job, "complete", {})
        peer_review = self.records.put("expansion_review", {"verdict": "approve", "issues": [],
            "candidate_ref": peer_candidate, "subject_ref": peer_expansion,
            "pending_comparisons": []}, producer=peer_job)
        peer = {**deepcopy(self.case), "case_id": peer_id, "budget_scope": peer_id,
                "candidate_ref": peer_candidate, "expansion_ref": peer_expansion,
                "candidate_review_ref": peer_review, "opportunity_id": "peer-op"}
        self.engine.ws.save_case(peer)
        self.batch["case_ids"].append(peer_id)
        self.batch["selected"].append("peer-op")
        self.batch["plan_ref"] = self.records.put("expansion_plan", {"opportunities": [
            self.op, {"opportunity_id": "peer-op", "seed_setting_ids": ["SEED"]}]})
        self.engine.ws.save_run("batch", self.batch)

        def reviewer(role, inputs, scope):
            self.assertEqual(role, "expansion_reviewer")
            self.assertEqual(inputs["candidate_ref"], self.candidate_ref)
            job = self.engine.ws.create_job(role, inputs)
            self.engine.ws.save_job(job, "complete", {})
            ref = self.records.put("expansion_review", {
                "verdict": "exclude", "issues": [], "required_changes": [],
                "candidate_ref": inputs["candidate_ref"], "subject_ref": inputs["subject_ref"],
                "duplicate_of_ref": peer_candidate, "pending_comparisons": [{
                    "candidate_ref": peer_candidate, "relation": "equivalent", "reason": "Fixture comparison"}]},
                producer=job)
            return {"id": job, "status": "complete"}, ref

        def specify(batch, op):
            cid = digest({"batch": "batch", "opportunity": op["opportunity_id"]})[:24]
            return self.engine.ws.case(cid)

        self.engine._job = reviewer
        self.engine._specify = specify
        self.engine.report = Mock(return_value={})
        with patch.object(Engine, "_advance", side_effect=lambda case: case) as research:
            self.engine.run_batch("batch")
        self.assertEqual(research.call_count, 1)
        self.assertEqual(research.call_args.args[0]["case_id"], peer_id)
        self.assertEqual(self.engine.ws.case(self.cid)["state"], "duplicate_pending")
        self.assertEqual(self.engine.batch("batch")["research_case_ids"], [peer_id])


class ExpansionReviewContracts(unittest.TestCase):
    def test_equivalent_pending_candidate_cannot_be_approved_as_distinct_work(self):
        records = Records()
        candidate = records.put("candidate", {"candidate_id": "one"}, producer="producer")
        peer = records.put("candidate", {"candidate_id": "peer"}, producer="earlier-producer")
        expansion = records.put("expansion", {"candidate_ref": candidate,
            "well_posedness": {k: "supported" for k in ("nonempty", "objective_defined", "oracle_implementable", "not_trivial")}}, producer="producer")
        data = {"subject_ref": expansion, "candidate_ref": candidate, "verdict": "approve",
                "pending_comparisons": [{"candidate_ref": peer, "relation": "equivalent", "reason": "Same complete contract"}],
                "duplicate_of_ref": None, "issues": [], "required_changes": []}
        inputs = {"subject_ref": expansion, "candidate_ref": candidate, "peer_candidate_refs": [peer]}
        with self.assertRaisesRegex(ProtocolError, "equivalent"):
            checked_review(data, inputs, records, "independent-reviewer")


if __name__ == "__main__":
    unittest.main()
