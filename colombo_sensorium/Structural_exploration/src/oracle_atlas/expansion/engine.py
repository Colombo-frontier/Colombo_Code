"""A finite discovery frontend; identity, research, review and writing share the paper engine."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json

from ..core.contracts import MAIN_KINDS, ProtocolError, references
from ..core.store import digest, dumps
from ..workflow.engine import Engine
from .neighborhood import build_neighborhood
from .request import normalize_request
from .validation import checked_expansion, checked_plan, checked_review


class ExpansionEngine(Engine):
    """Expansion always stages finished profiles for explicit human publication."""

    def __init__(self, config, backend, **kwargs):
        config = deepcopy(config)
        config.setdefault("publication", {})["require_human_approval"] = True
        config["expansion"] = {"max_batch_model_calls": 1600, "max_batch_external_calls": 600,
                               "max_batch_jobs": 240, **config.get("expansion", {})}
        for name, value in config["expansion"].items():
            if name.startswith("max_") and (not isinstance(value, int) or isinstance(value, bool) or value <= 0):
                raise ProtocolError(f"expansion.{name} must be a positive integer")
        super().__init__(config, backend, **kwargs)
        self._batch_scope = None

    def batch(self, batch_id):
        rows = self.ws.query("SELECT record FROM runs WHERE id=?", (batch_id,))
        if not rows:
            raise ProtocolError("Unknown expansion batch")
        record = json.loads(rows[0]["record"])
        if record.get("kind") != "expansion":
            raise ProtocolError("This run belongs to the paper-scanning frontend")
        return record

    def _save(self, batch):
        self.ws.save_run(batch["batch_id"], batch)
        return batch

    def _job(self, role, inputs, scope):
        batch_scope = inputs.get("batch_scope") or self._batch_scope
        if batch_scope:
            inputs = {**inputs, "batch_scope": batch_scope}
            count = self.ws.query("SELECT COUNT(*) AS n FROM jobs WHERE json_extract(inputs,'$.batch_scope')=?", (batch_scope,))[0]["n"]
            if count >= self.config["expansion"]["max_batch_jobs"]:
                # Existing jobs remain recoverable at the cap; only new job creation is disallowed.
                from ..runtime.instructions import load_instructions
                _, manifest = load_instructions(role)
                probe = {**inputs, "budget_scope": scope, "instructions_version": manifest["contract_version"], "model_id": self.config.get("model", {}).get("model")}
                jid = digest({"role": role, "inputs": probe, "nonce": ""})[:24]
                if not self.ws.query("SELECT id FROM jobs WHERE id=?", (jid,)):
                    raise ProtocolError("The expansion batch job budget is exhausted; resume with an explicit budget increase")
        return super()._job(role, inputs, scope)

    def _validate_stage(self, job, output):
        role = job["role"]
        if role not in {"expansion_planner", "setting_expander", "expansion_reviewer"}:
            return super()._validate_stage(job, output)
        if output["status"] != "complete":
            return
        ref = next((r for r in output["artifact_refs"] if self.artifacts.get(r)["kind"] == MAIN_KINDS[role]), None)
        if not ref:
            raise ProtocolError("The expansion handoff lacks its primary artifact")
        data = self.artifacts.get(ref)["data"]
        if role == "expansion_planner":
            checked_plan(data, job["inputs"], self.artifacts)
        elif role == "setting_expander":
            checked_expansion(data, job["inputs"], self.artifacts, job["id"])
        else:
            checked_review(data, job["inputs"], self.artifacts, job["id"])

    def _stage(self, case, role, inputs):
        inputs = {**inputs, "batch_scope": case["batch_id"], "origin_ref": case["origin_ref"],
                  "expansion_ref": case["expansion_ref"], "literature_cutoff": case["cutoff_date"]}
        if case.get("rebase_context_ref"):
            inputs["rebase_context_ref"] = case["rebase_context_ref"]
        return super()._stage(case, role, inputs)

    def _research_context(self, case, research):
        """Keep original research authority across identity-only controller rebinding.

        A controller rebind changes no science and acquires no producer ownership.
        It must point back to the actual role output and its unchanged tool trace;
        the refreshed identity and final profile still require independent review.
        """
        role = "bound_updater" if research["action"] in {"update", "no_change"} else "profile_researcher"
        job_id = case.get("jobs", {}).get(role)
        current_ref = case.get("research_ref")
        if job_id and current_ref and self.artifacts.owned(current_ref, job_id):
            return super()._research_context(case, research)
        audit_ref = case.get("rebase_context_ref")
        if not audit_ref:
            raise ProtocolError("Rebound research requires its controller identity-refresh audit")
        audit_item = self.artifacts.get(audit_ref)
        current = self.artifacts.get(current_ref)
        audit = audit_item["data"]
        if (audit_item["kind"] != "external_result" or audit_item["producer"] != "controller"
                or not self.artifacts.owned(audit_ref, "controller")
                or current["kind"] != "research" or current["producer"] != "controller"
                or not self.artifacts.owned(current_ref, "controller")
                or audit.get("operation") != "identity_refresh_only"
                or audit.get("new_research_ref") != current_ref
                or audit.get("new_identity_ref") != case.get("identity_ref")
                or research != current["data"]):
            raise ProtocolError("Rebound research must bind the exact controller-owned identity-refresh records")
        origin_ref = audit.get("origin_research_ref")
        origin_job = audit.get("research_producer_job")
        if not origin_ref or not origin_job or origin_job != job_id:
            raise ProtocolError("Rebound research lacks its actual producing job and original artifact")
        origin = self.artifacts.get(origin_ref)
        old = self.artifacts.get(audit.get("old_research_ref"))
        if (origin["kind"] != "research" or not self.artifacts.owned(origin_ref, origin_job)
                or self.ws.job(origin_job)["role"] != "profile_researcher"
                or old["kind"] != "research" or origin["data"].get("action") != "new"
                or origin["data"].get("candidate_ref") != case.get("candidate_ref")
                or origin["data"].get("profile_ref") != audit.get("profile_ref")
                or old["data"].get("identity_ref") != audit.get("old_identity_ref")):
            raise ProtocolError("Rebound research origin is not an owned original scientific handoff")
        expected = deepcopy(origin["data"])
        expected["identity_ref"] = case["identity_ref"]
        old_expected = deepcopy(origin["data"])
        old_expected["identity_ref"] = old["data"].get("identity_ref")
        if research != expected or old["data"] != old_expected:
            raise ProtocolError("Identity refresh cannot alter scientific content, references or research scope")
        origin_case = dict(case, research_ref=origin_ref)
        observed = super()._research_context(origin_case, origin["data"])
        if (audit.get("research_context_hash") != digest(observed)
                or audit.get("research_context") != observed):
            raise ProtocolError("Original research scope or tool evidence changed after identity refresh")
        return observed

    def _snapshot(self, setting_id, expected_version):
        """Archive source bytes as a lead; external-workspace proof IDs are not imported as approvals."""
        before = self.atlas.version(setting_id)
        if before != expected_version:
            raise ProtocolError("Atlas changed while pinning the discovery seeds; start the plan again")
        profile = self.atlas.read(setting_id)
        if self.atlas.version(setting_id) != before:
            raise ProtocolError("Atlas changed while reading a seed snapshot")
        text = dumps(profile)
        return self.put("source", {"url": f"atlas://{setting_id}/{before}", "version": before,
            "content_hash": digest(profile), "text": text,
            "metadata": {"kind": "atlas_seed_snapshot", "setting_id": setting_id, "atlas_version": before,
                         "approval_status": "historical_lead_only", "note": "Embedded external archive IDs are text, not granted proof credentials in this workspace."}})

    def plan(self, value):
        request = normalize_request(value)
        batch_id = digest({"frontend": "atlas_expansion_v1", "request": request})[:24]
        old = self.ws.query("SELECT record FROM runs WHERE id=?", (batch_id,))
        if old:
            batch = self.batch(batch_id)
            if batch.get("plan_ref"):
                return batch
        else:
            history = [json.loads(r["record"]) for r in self.ws.query("SELECT record FROM runs")]
            neighborhood = build_neighborhood(self.atlas, request, history)
            if not neighborhood["seeds"]:
                raise ProtocolError("No seeds are available in the declared discovery scope")
            configured = {t["task_id"] for t in self.catalog()["tasks"] if t.get("approved")}
            available = set(neighborhood["available_task_ids"]) | configured
            target_tasks = request["target_task_ids"] or sorted({t for s in neighborhood["seeds"] for t in s["task_ids"]})
            if not target_tasks:
                raise ProtocolError("Seeds have unknown task membership; specify approved target_task_ids")
            if not set(target_tasks).issubset(available):
                raise ProtocolError("New target tasks require task-catalog approval before expansion")
            neighborhood["target_task_ids"] = target_tasks
            for seed in neighborhood["seeds"]:
                seed["snapshot_ref"] = self._snapshot(seed["setting_id"], seed["version"])
            if self.atlas.version() != neighborhood["inventory_version"]:
                raise ProtocolError("The Atlas inventory changed during discovery snapshot construction")
            request_ref = self.put("expansion_request", request)
            neighborhood_ref = self.put("external_result", neighborhood)
            history_rows = []
            for old_batch in history:
                if old_batch.get("kind") != "expansion":
                    continue
                for cid in old_batch.get("case_ids", []):
                    case = self.ws.case(cid)
                    history_rows.append({"case_id": cid, "opportunity_id": case.get("opportunity_id"), "state": case["state"],
                                         "candidate_ref": case.get("candidate_ref"), "seed_setting_ids": case.get("seed_setting_ids", [])})
            history_ref = self.put("external_result", {"cases": history_rows, "notice": "Finite history for avoiding repeated work; all statuses retain their original scope."})
            batch = {"kind": "expansion", "batch_id": batch_id, "request_ref": request_ref, "neighborhood_ref": neighborhood_ref,
                     "history_ref": history_ref, "seed_setting_ids": [s["setting_id"] for s in neighborhood["seeds"]],
                     "case_ids": [], "selected": [], "deferred": [], "status": "planning"}
            self._save(batch)
        self._batch_scope = batch_id
        job, ref = self._job("expansion_planner", {"request_ref": batch["request_ref"], "neighborhood_ref": batch["neighborhood_ref"], "history_ref": batch["history_ref"]}, batch_id + ":plan")
        batch.update(plan_job=job["id"], status=job["status"])
        if ref:
            selection = checked_plan(self.artifacts.get(ref)["data"], job["inputs"], self.artifacts)
            batch.update(plan_ref=ref, selected=[o["opportunity_id"] for o in selection["selected"]], deferred=selection["deferred"], status="planned")
        return self._save(batch)

    def _peer_refs(self, batch, exclude=None):
        """Compare every reviewed peer in this batch. Earlier pending batches remain paginated history leads."""
        peers = []
        for cid in batch["case_ids"]:
            if cid == exclude:
                continue
            case = self.ws.case(cid)
            if case.get("candidate_review_ref"):
                review = self.artifacts.get(case["candidate_review_ref"])["data"]
                if review["verdict"] == "approve":
                    peers.append(case["candidate_ref"])
        return list(dict.fromkeys(peers))

    def _specify(self, batch, op, *, revision=None, material_refs=()):
        request = self.artifacts.get(batch["request_ref"])["data"]
        neighborhood = self.artifacts.get(batch["neighborhood_ref"])["data"]
        seeds = {s["setting_id"]: s for s in neighborhood["seeds"]}
        cid = digest({"batch": batch["batch_id"], "opportunity": op["opportunity_id"]})[:24]
        rows = self.ws.query("SELECT record FROM cases WHERE id=?", (cid,))
        case = json.loads(rows[0]["record"]) if rows else None
        if case and case.get("candidate_review_ref") and not revision:
            return case
        if case and case.get("specification_revision") and revision is None:
            revision = case["specification_revision"]
            material_refs = case.get("specification_material_refs", [])
        inputs = {"request_ref": batch["request_ref"], "plan_ref": batch["plan_ref"], "opportunity_id": op["opportunity_id"],
                  "seed_refs": [seeds[s]["snapshot_ref"] for s in op["seed_setting_ids"]], "history_ref": batch["history_ref"],
                  "batch_scope": batch["batch_id"], "material_refs": list(material_refs)}
        if revision:
            inputs.update(revision)
        job, ref = self._job("setting_expander", inputs, cid)
        if not ref:
            batch.setdefault("incomplete_jobs", {})[op["opportunity_id"]] = job["id"]
            self._save(batch)
            return None
        expansion = self.artifacts.get(ref)["data"]
        cref = expansion["candidate_ref"]
        candidate = self.artifacts.get(cref)["data"]
        if case is None:
            case = {"case_id": cid, "paper_ref": None, "candidate_origin": "atlas_expansion", "batch_id": batch["batch_id"],
                    "budget_scope": cid, "cutoff_date": request["cutoff_date"], "opportunity_id": op["opportunity_id"],
                    "seed_setting_ids": op["seed_setting_ids"], "history": [], "jobs": {}, "state": "specified"}
        case.update(candidate_ref=cref, expansion_ref=ref, origin_ref=self.put("expansion_origin", candidate["origin"]))
        case["jobs"]["setting_expander"] = job["id"]
        # Freeze the peer set once, so resuming a review does not generate a new job key.
        if revision or "peer_candidate_refs" not in case:
            case["peer_candidate_refs"] = self._peer_refs(batch, cid)
        self.ws.save_case(case)
        if cid not in batch["case_ids"]:
            batch["case_ids"].append(cid)
        self._save(batch)
        review_inputs = {"subject_ref": ref, "candidate_ref": cref, "request_ref": batch["request_ref"], "plan_ref": batch["plan_ref"],
                         "peer_candidate_refs": case["peer_candidate_refs"], "history_ref": batch["history_ref"], "batch_scope": batch["batch_id"]}
        if revision:
            review_inputs.update(revision)
        rjob, rref = self._job("expansion_reviewer", review_inputs, cid)
        case["jobs"]["expansion_reviewer"] = rjob["id"]
        if not rref:
            case["state"] = "expansion_reviewer:" + rjob["status"]
            self.ws.save_case(case)
            return case
        review = self.artifacts.get(rref)["data"]
        case.update(candidate_review_ref=rref, state="specified" if review["verdict"] == "approve" else "expansion_" + review["verdict"])
        case.pop("specification_revision", None)
        if review["duplicate_of_ref"]:
            case.update(state="duplicate_pending", duplicate_of_ref=review["duplicate_of_ref"])
        self.ws.save_case(case)
        if review["verdict"] == "revise" and case.get("revision_counts", {}).get("specification", 0) < self.config["budgets"]["max_science_revisions"]:
            return self.revise_specification(cid)
        return case

    def _identity_ready(self, case):
        return (case.get("identity_ref") and case.get("identity_review_ref") and
                self.artifacts.get(case["identity_ref"])["data"]["decision"] != "unresolved" and
                self.artifacts.get(case["identity_review_ref"])["data"]["verdict"] == "approve")

    def _approved_candidate(self, case):
        ref = case.get("candidate_review_ref")
        if not ref:
            raise ProtocolError("Expansion identity/research requires its independent specification review")
        item = self.artifacts.get(ref)
        review = item["data"]
        if item["kind"] != "expansion_review" or review["verdict"] != "approve" or review["candidate_ref"] != case["candidate_ref"] or review["subject_ref"] != case["expansion_ref"]:
            raise ProtocolError("This candidate has no matching approved expansion review")
        jobs = self.ws.query("SELECT role,status FROM jobs WHERE id=?", (item["producer"],))
        if not jobs or jobs[0]["role"] != "expansion_reviewer" or jobs[0]["status"] != "complete":
            raise ProtocolError("A real completed independent expansion reviewer must issue the candidate approval")

    def _reserve_research(self, case):
        batch = self.batch(case["batch_id"])
        request = self.artifacts.get(batch["request_ref"])["data"]
        started = batch.setdefault("research_case_ids", [])
        if case["case_id"] not in started:
            if len(started) >= request["max_profiles"]:
                case["state"] = "research_deferred_budget"
                self.ws.save_case(case)
                return False
            started.append(case["case_id"])
            self._save(batch)
        return True

    def _ensure_peer_coverage(self, case):
        """A resumed early review may predate a later peer; close missing pairs before spending research budget."""
        batch = self.batch(case["batch_id"])
        own_review = self.artifacts.get(case["candidate_review_ref"])["data"]
        peers = []
        missing = []
        for cid in batch["case_ids"]:
            if cid == case["case_id"]:
                continue
            other = self.ws.case(cid)
            if not other.get("candidate_review_ref"):
                continue
            review = self.artifacts.get(other["candidate_review_ref"])["data"]
            if review["verdict"] != "approve":
                continue
            peers.append(other["candidate_ref"])
            forward = [r for r in own_review["pending_comparisons"] if r["candidate_ref"] == other["candidate_ref"]]
            reverse = [r for r in review["pending_comparisons"] if r["candidate_ref"] == case["candidate_ref"]]
            if not any(r["relation"] == "distinct" for r in forward + reverse):
                missing.append(other["candidate_ref"])
        if not missing:
            return True
        pending = case.get("pending_peer_review")
        if not pending or set(pending["peer_candidate_refs"]) != set(peers):
            pending = {"peer_candidate_refs": sorted(set(peers)), "previous_review_ref": case["candidate_review_ref"]}
            case["pending_peer_review"] = pending
            self.ws.save_case(case)
        inputs = {"subject_ref": case["expansion_ref"], "candidate_ref": case["candidate_ref"],
                  "request_ref": batch["request_ref"], "plan_ref": batch["plan_ref"], "history_ref": batch["history_ref"],
                  "batch_scope": batch["batch_id"], **pending}
        job, ref = self._job("expansion_reviewer", inputs, case["budget_scope"])
        case["jobs"]["expansion_reviewer"] = job["id"]
        if not ref:
            case["state"] = "expansion_reviewer:" + job["status"]
            self.ws.save_case(case)
            return False
        review = self.artifacts.get(ref)["data"]
        case.update(candidate_review_ref=ref, peer_candidate_refs=pending["peer_candidate_refs"])
        case.pop("pending_peer_review", None)
        if review["verdict"] != "approve":
            case["state"] = "duplicate_pending" if review["duplicate_of_ref"] else "expansion_" + review["verdict"]
            if review["duplicate_of_ref"]:
                case["duplicate_of_ref"] = review["duplicate_of_ref"]
        self.ws.save_case(case)
        return review["verdict"] == "approve"

    def _advance(self, case):
        """Central gates apply equally to batch execution and every resume/revision path."""
        self._approved_candidate(case)
        if case["state"] == "committed":
            return case
        if not self._ensure_peer_coverage(case):
            return case
        self.resolve_identity(case)
        if not self._identity_ready(case):
            return case
        request = self.artifacts.get(self.batch(case["batch_id"])["request_ref"])["data"]
        identity = self.artifacts.get(case["identity_ref"])["data"]
        if identity["decision"] == "existing" and not request["allow_existing_updates"]:
            case.update(state="redirected_existing", existing_setting_id=identity["setting_id"])
            self.ws.save_case(case)
            return case
        if not self._reserve_research(case):
            return case
        return super()._advance(case)

    def _commit(self, case):
        """A stale boolean cannot authorize a new or revised five-file package."""
        self._approved_candidate(case)
        proposal = self.artifacts.get(case["proposal_ref"])["data"]
        prepared = self.artifacts.get(proposal["prepared_ref"])["data"]
        if (not case.get("human_approved") or case.get("approved_bundle_hash") != prepared["bundle_hash"]
                or case.get("approved_proposal_ref") != case["proposal_ref"]):
            case.pop("human_approved", None)
            case["state"] = "ready_for_approval"
            self.ws.save_case(case)
            return case
        return super()._commit(case)

    def _clear_approval(self, case):
        for key in ("human_approved", "approved_bundle_hash", "approved_proposal_ref", "publication_refresh", "publication_approval"):
            case.pop(key, None)
        self.ws.save_case(case)

    def run_batch(self, batch_id, *, research=True):
        batch = self.batch(batch_id)
        self._batch_scope = batch_id
        if not batch.get("plan_ref"):
            return self.report(batch_id)
        request = self.artifacts.get(batch["request_ref"])["data"]
        plan = self.artifacts.get(batch["plan_ref"])["data"]
        opportunities = {o["opportunity_id"]: o for o in plan["opportunities"]}
        for oid in batch["selected"]:
            try:
                case = self._specify(batch, opportunities[oid])
                if not case or not case.get("candidate_review_ref"):
                    continue
                if self.artifacts.get(case["candidate_review_ref"])["data"]["verdict"] != "approve":
                    continue
                if case["state"] in {"committed", "ready_for_approval", "no_change", "redirected_existing", "superseded_existing"}:
                    continue
                case = self.resolve_identity(case)
                if not self._identity_ready(case):
                    if case["state"] == "identity_revise" and case.get("revision_counts", {}).get("identity", 0) < self.config["budgets"]["max_science_revisions"]:
                        # Keep the same no-research phase while applying a bounded identity repair.
                        case = self.revise_identity(case["case_id"], research=False)
                    if not self._identity_ready(case):
                        continue
                decision = self.artifacts.get(case["identity_ref"])["data"]
                if decision["decision"] == "existing" and not request["allow_existing_updates"]:
                    case.update(state="redirected_existing", existing_setting_id=decision["setting_id"])
                    self.ws.save_case(case)
            except ProtocolError as exc:
                batch.setdefault("diagnostics", {})[oid] = str(exc)
                self._save(batch)
        # All identity-ready candidates remain ranked by the planner's finite portfolio order.
        if research:
            for oid in batch["selected"]:
                cid = digest({"batch": batch_id, "opportunity": oid})[:24]
                if cid not in batch["case_ids"]:
                    continue
                case = self.ws.case(cid)
                if case["state"] in {"committed", "ready_for_approval", "no_change", "redirected_existing", "superseded_existing"}:
                    continue
                if not self._identity_ready(case):
                    continue
                try:
                    # _advance closes peer/identity gates before reserving a research slot.
                    # Excluded candidates must not consume another candidate's budget.
                    case = self._advance(case)
                    if case["state"] == "profile_revise" and case.get("revision_counts", {}).get("research", 0) < self.config["budgets"]["max_science_revisions"]:
                        super().resume_case(cid, stage="research")
                except ProtocolError as exc:
                    batch = self.batch(batch_id)
                    batch.setdefault("diagnostics", {})[oid] = str(exc)
                    self._save(batch)
        # Research reservation persists the batch independently; retain its latest state.
        batch = self.batch(batch_id)
        batch["status"] = "review_batch_available" if research else "candidates_available"
        self._save(batch)
        return self.report(batch_id)

    def expand(self, value, *, research=True):
        batch = self.plan(value)
        return self.run_batch(batch["batch_id"], research=research) if batch.get("plan_ref") else self.report(batch["batch_id"])

    def revise_specification(self, case_id, material_refs=()):
        case = self.ws.case(case_id)
        if case["state"] == "committed":
            raise ProtocolError("Committed specifications require a new update transaction")
        review = self.artifacts.get(case["candidate_review_ref"])["data"]
        old_materials = set(case.get("specification_material_refs", []))
        new_materials = set(material_refs) - old_materials
        if review["verdict"] != "revise" and not new_materials:
            raise ProtocolError("Specification revision requires new material or an explicit revise review")
        count = case.setdefault("revision_counts", {}).get("specification", 0)
        if not new_materials and count >= self.config["budgets"]["max_science_revisions"]:
            raise ProtocolError("The specification revision budget is exhausted")
        for ref in new_materials:
            self.artifacts.get(ref)
        case["history"].append(deepcopy({k: v for k, v in case.items() if k not in {"history", "jobs"}}))
        revision = {"revision": count + 1, "previous_candidate_ref": case["candidate_ref"],
                    "previous_artifact_ref": case["expansion_ref"], "repair_feedback_ref": case["candidate_review_ref"]}
        case["revision_counts"]["specification"] = count + 1
        case["specification_material_refs"] = sorted(old_materials | new_materials)
        case["specification_revision"] = revision
        self._clear_approval(case)
        for key in ("candidate_review_ref", "identity_ref", "identity_review_ref", "research_ref", "proposal_ref", "profile_review_ref", "receipt_ref"):
            case.pop(key, None)
        self.ws.save_case(case)
        batch = self.batch(case["batch_id"])
        self._batch_scope = batch["batch_id"]
        op = next(o for o in self.artifacts.get(batch["plan_ref"])["data"]["opportunities"] if o["opportunity_id"] == case["opportunity_id"])
        return self._specify(batch, op, revision=revision, material_refs=case["specification_material_refs"])

    def revise_identity(self, case_id, *, research=True, material_refs=()):
        case = self.ws.case(case_id)
        self._approved_candidate(case)
        self._clear_approval(case)
        return super().resume_case(case_id, stage="identity", material_refs=material_refs, identity_only=not research)

    def resume_expansion_case(self, case_id, *, stage=None, material_refs=()):
        case = self.ws.case(case_id)
        self._batch_scope = case["batch_id"]
        if stage == "specification":
            return self.revise_specification(case_id, material_refs)
        if stage in {"identity", "research"}:
            self._approved_candidate(case)
            self._clear_approval(case)
            return super().resume_case(case_id, stage=stage, material_refs=material_refs)
        if case.get("publication_refresh"):
            self.publish(case["batch_id"], [case_id])
            return self.ws.case(case_id)
        self.run_batch(case["batch_id"])
        return self.ws.case(case_id)

    def _refresh_for_publication(self, case):
        """Recheck identity on the current inventory; retain exact scientific objects, never inherited approval."""
        refresh = case.get("publication_refresh")
        if not refresh:
            refresh = {"phase": "identity", "old_review_ref": case["profile_review_ref"],
                       "old_research_ref": case["research_ref"], "old_identity_ref": case["identity_ref"]}
            case["history"].append(deepcopy({k: v for k, v in case.items() if k not in {"history", "jobs"}}))
            case["revision"] = case.get("revision", 0) + 1
            case["publication_refresh"] = refresh
            for key in ("identity_ref", "identity_review_ref", "human_approved"):
                case.pop(key, None)
            self.ws.save_case(case)
        self.resolve_identity(case)
        if not self._identity_ready(case):
            return case
        identity = self.artifacts.get(case["identity_ref"])["data"]
        if identity["decision"] != "new":
            case.update(state="superseded_existing", existing_setting_id=identity["setting_id"])
            self.ws.save_case(case)
            return case
        if refresh["phase"] == "rebound":
            return self._advance(case)
        old_research_ref = refresh["old_research_ref"]
        previous_review = refresh["old_review_ref"]
        research = deepcopy(self.artifacts.get(old_research_ref)["data"])
        if research["action"] != "new" or research["candidate_ref"] != case["candidate_ref"]:
            raise ProtocolError("Only an unchanged new-setting candidate may use publication identity refresh")
        # Bind observations to the original producer before changing the case's
        # research reference. Repeated refreshes preserve that same actual origin.
        original_context = self._research_context(
            dict(case, research_ref=old_research_ref, identity_ref=research["identity_ref"]), research)
        origin_ref = old_research_ref
        if case.get("rebase_context_ref"):
            previous_rebase = self.artifacts.get(case["rebase_context_ref"])["data"]
            if previous_rebase.get("new_research_ref") == old_research_ref:
                origin_ref = previous_rebase["origin_research_ref"]
        research["identity_ref"] = case["identity_ref"]
        case["research_ref"] = self.put("research", research, [old_research_ref, case["identity_review_ref"]])
        case["rebase_context_ref"] = self.put("external_result", {"operation": "identity_refresh_only", "old_identity_ref": refresh["old_identity_ref"],
            "new_identity_ref": case["identity_ref"], "old_research_ref": old_research_ref, "new_research_ref": case["research_ref"],
            "profile_ref": research["profile_ref"], "scientific_content_unchanged": True,
            "origin_research_ref": origin_ref, "research_producer_job": original_context["producer_job"],
            "research_context": original_context, "research_context_hash": digest(original_context),
            "previous_review_ref": previous_review, "notice": "Rebinding changes no claims and grants no current review approval."})
        case["repair_feedback_ref"] = previous_review
        case.pop("previous_artifact_ref", None)
        for key in ("proposal_ref", "profile_review_ref", "receipt_ref"):
            case.pop(key, None)
        refresh["phase"] = "rebound"
        self.ws.save_case(case)
        return self._advance(case)

    def publish(self, batch_id, case_ids=None):
        batch = self.batch(batch_id)
        self._batch_scope = batch_id
        selected = list(case_ids) if case_ids is not None else [cid for cid in batch["case_ids"] if self.ws.case(cid)["state"] == "ready_for_approval"]
        if not set(selected).issubset(batch["case_ids"]):
            raise ProtocolError("Publication selection includes a case outside this batch")
        for cid in selected:
            case = self.ws.case(cid)
            if case["state"] == "committed":
                continue
            if case["state"] not in {"ready_for_approval", "identity_stale"} and not case.get("publication_refresh"):
                raise ProtocolError(f"{cid} is not a reviewed profile awaiting approval")
            approval = case.get("publication_approval")
            if not approval:
                proposal_ref = case["proposal_ref"]
                proposal = self.artifacts.get(proposal_ref)["data"]
                approval = {"case_id": cid, "proposal_ref": proposal_ref,
                            "bundle_hash": self.artifacts.get(proposal["prepared_ref"])["data"]["bundle_hash"]}
                case["publication_approval"] = approval
                self.ws.event("human", "expansion_publication_authorized", approval)
                self.ws.save_case(case)
            approved_hash = approval["bundle_hash"]
            proposal = self.artifacts.get(case.get("proposal_ref") or approval["proposal_ref"])["data"]
            if case.get("publication_refresh") or (proposal["mode"] == "new" and proposal["inventory_version"] != self.atlas.version()):
                case = self._refresh_for_publication(case)
                if case["state"] != "ready_for_approval":
                    continue
            current = self.artifacts.get(case["proposal_ref"])["data"]
            current_hash = self.artifacts.get(current["prepared_ref"])["data"]["bundle_hash"]
            if current_hash != approved_hash:
                case.update(state="ready_for_approval", approval_note="The five-file content changed after refresh; inspect the new proposal before approving it.")
                self._clear_approval(case)
                self.ws.save_case(case)
                continue
            case["human_approved"] = True
            case["approved_bundle_hash"] = approved_hash
            case["approved_proposal_ref"] = case["proposal_ref"]
            self.ws.save_case(case)
            self._commit(case)
            if case["state"] == "committed":
                case.pop("publication_refresh", None)
                self.ws.save_case(case)
        return self.report(batch_id)

    def report(self, batch_id):
        batch = self.batch(batch_id)
        cases = [self.ws.case(cid) for cid in batch["case_ids"]]
        request = self.artifacts.get(batch["request_ref"])["data"]
        plan = self.artifacts.get(batch["plan_ref"])["data"] if batch.get("plan_ref") else {"opportunities": []}
        opportunities = {o["opportunity_id"]: o for o in plan["opportunities"]}
        rows = []
        for case in cases:
            op = opportunities.get(case["opportunity_id"], {})
            expansion = self.artifacts.get(case["expansion_ref"])["data"]
            row = {"case_id": case["case_id"], "candidate_ref": case["candidate_ref"], "title": op.get("title", ""), "state": case["state"],
                   "selection_reason": expansion["selection_reason"], "transformation": op.get("transformation", ""),
                   "expected_value": op.get("expected_value", ""), "risks": op.get("risks", []),
                   "changed_axes": op.get("changed_axes", []),
                   "seed_setting_ids": case["seed_setting_ids"], "operators": op.get("operators", []),
                   "candidate_review_ref": case.get("candidate_review_ref"), "proposal_ref": case.get("proposal_ref"),
                   "profile_review_ref": case.get("profile_review_ref"), "receipt_ref": case.get("receipt_ref"),
                   "duplicate_of_ref": case.get("duplicate_of_ref"), "existing_setting_id": case.get("existing_setting_id")}
            if case.get("identity_ref"):
                row["atlas_identity"] = self.artifacts.get(case["identity_ref"])["data"]["decision"]
            rows.append(row)
        state_counts = dict(Counter(c["state"] for c in cases))
        return {"batch_id": batch_id, "status": batch["status"], "request_ref": batch["request_ref"], "plan_ref": batch.get("plan_ref"),
                "neighborhood_ref": batch["neighborhood_ref"], "target_profiles": request["max_profiles"], "opportunities": len(plan["opportunities"]),
                "candidate_count": len(cases), "state_counts": state_counts, "cases": rows, "deferred": batch["deferred"],
                "diagnostics": batch.get("diagnostics", {}), "incomplete_jobs": batch.get("incomplete_jobs", {}),
                "notice": "New to this Atlas does not mean new to the literature or an open problem. A profile is ingested only with a commit receipt. Fewer than the requested maximum is a valid outcome."}
