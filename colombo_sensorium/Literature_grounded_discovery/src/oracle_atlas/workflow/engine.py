"""Research Agent orchestration with a small dependency graph; scientific judgment remains with independent roles."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from ..atlas.store import Atlas, AtlasConflict, AtlasValidationError
from ..core.contracts import MAIN_KINDS, ProtocolError, blocking, check_review, references, resolve_pointer
from ..core.store import Workspace, digest
from ..discovery.bibliography import merge_records, qualifies_year
from ..runtime.instructions import load_instructions
from ..runtime.runner import AgentRunner
from .coverage import coverage_scope, coverage_errors, freeze_delivery_scope
from . import transfer


AXES={"TASK","MODEL","ORACLE","ALGORITHMS","OUTPUT","METRIC","GUARANTEE","RESOURCE"}


def profile_facts(candidate,identity,profile,explicit=None):
    """Rewrite Pointers only using reviewed view ID mappings; research Agents still declare semantic operation/object transformations."""
    if explicit is not None:return explicit
    mapping={m["candidate_view_id"]:(m["atlas_view_id"] or m["candidate_view_id"]) for m in identity["view_mapping"]}
    positions={v["view_id"]:i for i,v in enumerate(profile["views"])}
    facts=copy.deepcopy(candidate["tag_facts"])
    for fact in facts:
        view=fact.get("view_ref")
        if view is not None:fact["view_ref"]=mapping.get(view,view)
        parts=fact["source_pointer"].split("/")
        if len(parts)>2 and parts[1]=="views" and parts[2].isdigit():
            index=int(parts[2])
            if index>=len(candidate["views"]):raise ProtocolError("Candidate view Pointer is out of bounds")
            source_id=candidate["views"][index]["view_id"]
            target_id=mapping.get(source_id,source_id)
            if target_id not in positions:raise ProtocolError("The view mapping does not resolve to the final profile; provide complete target bindings in research.tag_facts")
            parts[2]=str(positions[target_id]);fact["source_pointer"]="/".join(parts)
    return facts


class Engine:
    def __init__(self, config: dict, backend, *, bridge=None, bibliography=None):
        self.config=config; self.ws=Workspace(config["workspace"])
        self.atlas=Atlas(config["atlas"])
        self.runner=AgentRunner(self.ws,self.atlas,backend,config,bridge=bridge,bibliography=bibliography)
        self.artifacts=self.ws.artifacts

    def put(self,kind,data,deps=()):
        return self.artifacts.put(kind,data,"controller",deps)

    def _main(self,job):
        if job["status"]!="complete": return None
        return next(r for r in job["output"]["artifact_refs"] if self.artifacts.get(r)["kind"]==MAIN_KINDS[job["role"]])

    def _job(self,role,inputs,scope):
        _,manifest=load_instructions(role)
        inputs={**inputs,"budget_scope":scope,"instructions_version":manifest["contract_version"],"model_id":self.config.get("model",{}).get("model")}
        job_id=self.ws.create_job(role,inputs)
        count=self.ws.query("SELECT COUNT(*) AS n FROM jobs WHERE json_extract(inputs,'$.budget_scope')=?",(scope,))[0]["n"]
        if count>self.config["budgets"]["max_jobs"]:
            self.ws.save_job(job_id,"budget_exhausted",{"last_error":"The budget for this job is exhausted"})
            return self.ws.job(job_id),None
        job=self.runner.run(job_id,validate_output=self._validate_stage)
        return job,self._main(job)

    def _validate_stage(self,job,output):
        if output["status"]!="complete": return
        ref=next((r for r in output["artifact_refs"] if self.artifacts.get(r)["kind"]==MAIN_KINDS[job["role"]]),None)
        if not ref: raise ProtocolError("Primary artifact is missing")
        data=self.artifacts.get(ref)["data"]; inputs=job["inputs"]; role=job["role"]
        ledger_errors=coverage_errors(data,inputs,role,self.artifacts)
        if ledger_errors:
            raise ProtocolError("Coverage ledger validation failed: "+json.dumps(ledger_errors,ensure_ascii=False))
        if role=="profile_reviewer" and (inputs.get("proof_context_ref") or inputs.get("issue_scope_contract_version") == "occurrence-bound-scope"):
            if inputs.get("issue_scope_contract_version") == "occurrence-bound-scope" and not all(inputs.get(key) for key in ("proof_context_ref", "review_context_ref")):
                raise ProtocolError("A occurrence-bound-scope profile review requires controller-generated proof and bound contexts; missing catalogs cannot disable validation.")
            from .proof_reuse import proof_approval_errors
            proof_errors=proof_approval_errors(data,inputs,self.artifacts)
            if proof_errors:
                raise ProtocolError("Proof reuse credential validation failed: "+json.dumps(proof_errors,ensure_ascii=False))
        if role=="profile_reviewer":
            from ..atlas.projection_report import mechanical_repair_request
            mechanical_repair_request(data)
            from .review_context import bound_approval_errors
            bound_errors=bound_approval_errors(data,inputs,self.artifacts)
            if bound_errors:
                raise ProtocolError("Bound reuse credential validation failed: "+json.dumps(bound_errors,ensure_ascii=False))
        if role=="profile_reviewer" and inputs.get("review_context_ref"):
            audit=data.get("coverage_audit",{})
            reused=set(audit.get("reused_bound_ids",[]))
            if reused:
                context=self.artifacts.get(inputs["review_context_ref"])["data"]
                allowed=set(context.get("reusable_bound_ids",[]))
                if audit.get("reuse_context_ref")!=inputs["review_context_ref"] or not reused.issubset(allowed):
                    raise ProtocolError("Per-bound reuse must bind the current controller context and its validated candidates; an identical ID cannot imply inherited approval.")
                if not reused.issubset(set(data["approved_bound_ids"])):
                    raise ProtocolError("Reused bounds must still be explicitly listed in approved_bound_ids in the current review.")
        if role.endswith("reviewer"):
            typ={"extraction_reviewer":"extraction","identity_reviewer":"identity","profile_reviewer":"profile"}[role]
            check_review(data,inputs["subject_ref"],typ)
            if typ == "profile" and inputs.get("transfer_scope_ref"):
                transfer.check_transfer_review(data)
            if self.artifacts.owned(inputs["subject_ref"],job["id"]):
                raise ProtocolError("A role cannot review a pinned object it produced")
            if typ=="extraction":
                extraction=self.artifacts.get(inputs["subject_ref"])["data"]
                for cref in extraction["candidate_refs"]:
                    candidate_id=self.artifacts.get(cref)["data"]["candidate_id"]
                    items=[a for a in data["assessments"] if a["subject_id"] in {cref,candidate_id}]
                    if len(items)!=1:raise ProtocolError("Extraction review must provide exactly one assessment for each candidate")
                    if items[0]["verdict"]=="approve" and (blocking(data["issues"],"extraction",cref) or blocking(data["issues"],"extraction",candidate_id)):
                        raise ProtocolError("Candidate approve conflicts with extraction blockers for that candidate")
            if typ=="profile" and data["verdict"]=="approve":
                from .joint_review import require_frozen_analysis_read, require_joint_checks, validate_no_change
                require_joint_checks(data)
                subject=self.artifacts.get(inputs["subject_ref"])
                require_frozen_analysis_read(self.ws, job["id"], subject)
                if subject["kind"]=="research" and subject["data"]["action"]=="no_change":
                    validate_no_change(self.atlas, subject["data"])
                if subject["kind"]=="proposal":
                    prepared=self.artifacts.get(subject["data"]["prepared_ref"])["data"]
                    try:self.atlas.validate_review(prepared,data)
                    except AtlasValidationError as exc:raise ProtocolError(f"The review adoption scope does not match the frozen proposal: {exc}") from exc
        elif role=="coordinator":
            request=self.artifacts.get(inputs["request_ref"])["data"]
            catalog=self.artifacts.get(inputs["catalog_ref"])["data"]
            approved={t["task_id"] for t in catalog["tasks"] if t["approved"]}
            if not set(data["task_ids"]).issubset(approved & set(request["task_ids"])):
                raise ProtocolError("A plan may use only tasks approved in this request; propose new tasks in a recommendation report first")
            if set(data["years"])!=set(request["years"]) or data["paper_limit"]>request["paper_limit"] or data["query_budget"]>request["query_budget"]:
                raise ProtocolError("The plan expanded the approved years or budget")
        elif role=="extractor":
            if data["paper_ref"]!=inputs["paper_ref"]: raise ProtocolError("The extraction bundle binds the wrong paper")
            seen=set()
            for c in data["candidate_refs"]:
                item=self.artifacts.get(c)
                if item["kind"]!="candidate" or not self.artifacts.owned(c,job["id"]): raise ProtocolError("Candidates must be produced by the current extractor")
                candidate=item["data"]
                if candidate["candidate_id"] in seen: raise ProtocolError("Duplicate candidate_id in the same bundle")
                seen.add(candidate["candidate_id"])
                if inputs["paper_ref"] not in candidate["paper_refs"]: raise ProtocolError("The candidate does not bind the triggering paper")
                if {f["axis"] for f in candidate["tag_facts"]}!=AXES:
                    raise ProtocolError("Tag facts must be registered for all eight axes; explicitly use unknown when material is unknown, without omitting an entire axis")
                for fact in candidate["tag_facts"]:
                    resolve_pointer(candidate,fact["source_pointer"])
                from ..atlas.bindings import normalize_tag_facts
                normalized = normalize_tag_facts(candidate, candidate["tag_facts"])
                if normalized["errors"]:
                    raise ProtocolError("Candidate bindings failed early validation: " + json.dumps(normalized["errors"], ensure_ascii=False))
                if normalized["changes"]:
                    raise ProtocolError("The candidate still contains path-form IDs; normalize through artifact_put/draft_freeze and freeze again without rewriting existing references")
            if inputs.get("previous_candidate_ref") and len(data["candidate_refs"])!=1:
                raise ProtocolError("A single-candidate revision must return exactly one candidate without modifying sibling candidates")
            if inputs.get("previous_candidate_ref"):
                old=self.artifacts.get(inputs["previous_candidate_ref"])["data"]
                new=self.artifacts.get(data["candidate_refs"][0])["data"]
                if old["candidate_id"]!=new["candidate_id"]:raise ProtocolError("A single-candidate revision must preserve candidate_id")
        elif role=="matcher":
            if data["candidate_ref"]!=inputs["candidate_ref"]: raise ProtocolError("identity binds the wrong candidate")
            retrieval=self.artifacts.get(data["retrieval_ref"])
            if retrieval["kind"]!="retrieval" or retrieval["data"].get("candidate_ref")!=data["candidate_ref"]:
                raise ProtocolError("The identity retrieval_ref does not belong to the current candidate")
            if data["recall_audit"]["inventory_version"]!=retrieval["data"].get("inventory_version"):
                raise ProtocolError("recall_audit inventory_version does not match the retrieval snapshot")
            if data["decision"]=="existing" and (not data["setting_id"] or self.atlas.version(data["setting_id"]) is None):
                raise ProtocolError("existing must refer to an actual Atlas setting")
            if data["decision"]=="new":
                if len(set(data["recall_audit"]["strategies"]))<2 or not retrieval["data"].get("broaden"):
                    raise ProtocolError("new requires broad multichannel recall; expand retrieval rather than treating an empty top-k as evidence for a new setting")
                if data["recall_audit"]["unresolved_ids"]:
                    raise ProtocolError("decision must be unresolved while credible unresolved neighbors remain")
            if data["decision"]!="unresolved" and blocking(data["issues"],"identity"):
                raise ProtocolError("The formal identity conclusion conflicts with its identity blockers; bound-only concerns do not affect this check")
        elif role in {"bound_updater","profile_researcher"}:
            if data["candidate_ref"]!=inputs["candidate_ref"] or data["identity_ref"]!=inputs["identity_ref"]:
                raise ProtocolError("research does not bind the current candidate/identity")
            identity=self.artifacts.get(inputs["identity_ref"])["data"]
            if data["base_version"]!=inputs.get("base_version"):
                raise ProtocolError("Incorrect research baseline version")
            if inputs.get("transfer_scope_ref"):
                scope = self.artifacts.get(inputs["transfer_scope_ref"])["data"]
                transfer.check_transfer_research(scope, data, self.artifacts.get)
            elif role=="bound_updater" and (data["action"] not in {"update","no_change"} or data["setting_id"]!=identity["setting_id"]):
                raise ProtocolError("An existing setting may only update its original ID or use no_change")
            if role=="profile_researcher" and data["action"]!="new": raise ProtocolError("Research for a new setting must output new")
            if data["action"]=="no_change":
                from .joint_review import validate_no_change
                validate_no_change(self.atlas, data)
            if data["action"]!="no_change":
                if not data["profile_ref"]: raise ProtocolError("A complete profile draft is missing")
                p=self.artifacts.get(data["profile_ref"])
                if p["kind"]!="profile" or p["data"]["setting_id"]!=data["setting_id"]: raise ProtocolError("profile setting_id does not match")
                try:
                    candidate=self.artifacts.get(inputs["candidate_ref"])["data"]
                    facts=(transfer.target_facts(data.get("tag_facts")) if inputs.get("transfer_scope_ref") else
                           profile_facts(candidate,identity,p["data"],data.get("tag_facts")))
                    if data["action"]=="new" and {f["axis"] for f in facts}!=AXES:raise ProtocolError("New profile tags must register every axis, including explicit unknown entries")
                    self.atlas.prepare(p["data"],facts,data["base_version"])
                except AtlasValidationError as exc:
                    raise ProtocolError(f"Atlas five-file adaptation validation failed; repair the current profile and resubmit research: {exc}") from exc
            from .joint_review import require_finite_literature
            require_finite_literature(self.ws, job["id"], data)
            for result_ref in data["result_refs"]:
                card=self.artifacts.get(result_ref)
                if card["kind"]!="result": raise ProtocolError("result_refs must point to atomic result cards")
                if card["data"]["origin"]!="published_theorem" and not card["data"]["proof_refs"]:
                    raise ProtocolError("Analyst derivations/transformations require a self-contained proof_ref; a conclusion alone is insufficient")
                for locator in card["data"]["source_locators"]:
                    source=self.artifacts.get(locator["source_ref"])
                    if source["kind"]!="source" or locator["version"]!=source["data"]["version"]:
                        raise ProtocolError("Source locators must bind the same source version")

    def catalog(self):
        path=self.ws.root/"approved_tasks.json"
        if path.exists(): return json.loads(path.read_text(encoding="utf-8"))
        return {"tasks":self.config.get("tasks",[])}

    def task_scout(self,notes="",material_refs=()):
        catalog_ref=self.put("catalog",self.catalog())
        scope=digest({"task_scout":catalog_ref,"notes":notes,"materials":list(material_refs)})[:24]
        job,ref=self._job("task_scout",{"catalog_ref":catalog_ref,"material_refs":list(material_refs),"notes":notes},scope)
        return {"job_id":job["id"],"status":job["status"],"proposal_ref":ref,"automatic_scope_expansion":False}

    def approve_task(self,proposal_ref,task_id):
        from ..core.store import atomic_json
        item=self.artifacts.get(proposal_ref)
        if item["kind"]!="task_proposal": raise ProtocolError("task_proposal is required")
        task=next((t for t in item["data"]["proposals"] if t["task_id"]==task_id),None)
        if not task: raise ProtocolError("The task does not exist in the report")
        catalog=self.catalog()
        if any(t["task_id"]==task_id for t in catalog["tasks"]): raise ProtocolError("task_id is already in the catalog; its definition cannot be silently replaced")
        catalog["tasks"].append({**task,"approved":True,"approval_source":proposal_ref})
        atomic_json(self.ws.root/"approved_tasks.json",catalog)
        self.ws.event("human","task_approved",{"task_id":task_id,"proposal_ref":proposal_ref})
        return catalog

    def scan(self,request:dict,run_label:str=""):
        request_ref=self.put("request",request); catalog_ref=self.put("catalog",self.catalog())
        scope=digest({"request":request_ref,"catalog":catalog_ref,"run_label":run_label})[:24]
        plan_job,plan_ref=self._job("coordinator",{"request_ref":request_ref,"catalog_ref":catalog_ref},scope)
        record={"run_id":scope,"run_label":run_label,"request_ref":request_ref,"plan_job":plan_job["id"],"cases":[],"status":plan_job["status"]}
        if not plan_ref: self.ws.save_run(scope,record); return record
        scanner,batch_ref=self._job("paper_scanner",{"plan_ref":plan_ref,"request_ref":request_ref,"catalog_ref":catalog_ref},scope)
        record.update(scanner_job=scanner["id"],paper_batch_ref=batch_ref,status=scanner["status"])
        if not batch_ref: self.ws.save_run(scope,record); return record
        batch=self.artifacts.get(batch_ref)["data"]
        # First merge all events for the same DOI/arXiv, then determine annual membership; retain unverified leads in the queue.
        merged={}
        for ref in batch["paper_refs"]:
            p=self.artifacts.get(ref)
            if p["kind"]!="paper": raise ProtocolError("paper_batch references a non-paper artifact")
            identifiers=p["data"].get("identifiers",{})
            key=(p["data"].get("doi") or identifiers.get("doi") or p["data"].get("arxiv_id") or identifiers.get("arxiv") or ref)
            if key in merged:
                combined=merge_records(merged[key][1],p["data"])
                merged[key]=(self.put("paper",combined,[merged[key][0],ref]),combined)
            else: merged[key]=(ref,p["data"])
        eligible=[]; pending=[]
        for ref,paper in merged.values():
            (eligible if qualifies_year(paper,request["years"],request["event_kind"]) else pending).append(ref)
        record.update(verified_year_papers=len(eligible),unverified_or_other_year_refs=pending,selected_paper_refs=eligible[:request["paper_limit"]],coverage=batch["coverage"])
        for ref in eligible[:request["paper_limit"]]:
            outcome=self.process_paper(ref,budget_scope=scope)
            record["cases"].extend(outcome["case_ids"])
            record.setdefault("papers",[]).append(outcome)
            self.ws.save_run(scope,record)
        record["status"]="finished_with_results"
        record["counts"]=self.counts(record["cases"])
        self.ws.save_run(scope,record)
        return record

    def process_paper(self,paper_ref,budget_scope=None,*,research_material_refs=()):
        for material in research_material_refs:self.artifacts.get(material)
        scope=budget_scope or digest({"paper":paper_ref})[:24]
        extraction,eref=self._job("extractor",{"paper_ref":paper_ref},scope)
        outcome={"paper_ref":paper_ref,"extraction_job":extraction["id"],"case_ids":[],"status":extraction["status"]}
        if not eref: return outcome
        review,rref=self._job("extraction_reviewer",{"subject_ref":eref,"paper_ref":paper_ref},scope)
        outcome.update(review_job=review["id"],status=review["status"])
        if not rref: return outcome
        candidate_refs=self.artifacts.get(eref)["data"]["candidate_refs"]
        for index,cref in enumerate(candidate_refs):
            candidate=self.artifacts.get(cref)["data"]
            cid=digest({"paper":paper_ref,"candidate_id":candidate["candidate_id"]})[:24]
            outcome["case_ids"].append(cid)
            try:
                case=self.ws.case(cid)
                if set(research_material_refs)-set(case.get("research_material_refs",[])):
                    raise ProtocolError("For new research material in an existing case, use resume --stage research --material-ref/--material-file; run-paper reference material binds only the initial case and cannot trigger silent resampling.")
            except KeyError:
                case={"case_id":cid,"paper_ref":paper_ref,"candidate_ref":cref,"extraction_ref":eref,"extraction_review_ref":rref,"budget_scope":scope,"state":"extracted","history":[],"jobs":{},"research_material_refs":list(research_material_refs)}
            # Preserve processed sibling branches; repeated scans do not overwrite their states.
            if case["state"] in {"committed","no_change"}: continue
            # The limit applies to every automatic stage, including extraction revise and pending recovery.
            # Retain review results for unselected candidates as records; do not open another model task before checking the limit.
            if index>=self.config["budgets"]["max_candidates"]:
                case["state"]="queued_by_limit"; self.ws.save_case(case); continue
            if case.get("pending_extraction"):
                self.resume_case(cid);continue
            cref=case["candidate_ref"];candidate=self.artifacts.get(cref)["data"]
            verdict=self._candidate_verdict(case["extraction_review_ref"],cref,candidate["candidate_id"])
            if verdict!="approve":
                case["state"]="extraction_"+verdict; self.ws.save_case(case)
                if verdict=="revise" and case.get("revision_counts",{}).get("extraction",0)<self.config["budgets"]["max_science_revisions"]:
                    self.resume_case(cid,stage="extraction")
                continue
            case["state"]="identity_pending"; self.ws.save_case(case)
            advanced=self._advance(case)
            if advanced["state"] in {"identity_revise","profile_revise"}:
                revision_stage="identity" if advanced["state"].startswith("identity") else "research"
                if advanced.get("revision_counts",{}).get(revision_stage,0)<self.config["budgets"]["max_science_revisions"]:
                    self.resume_case(cid,stage=revision_stage)
        return outcome

    def _candidate_verdict(self,review_ref,cref,candidate_id):
        r=self.artifacts.get(review_ref)["data"]
        entries=[a for a in r["assessments"] if a["subject_id"] in {cref,candidate_id}]
        verdict=entries[0]["verdict"] if entries else r["verdict"]
        issues=blocking(r["issues"],"extraction",cref)+blocking(r["issues"],"extraction",candidate_id)
        if verdict=="approve" and issues: return "revise"
        return verdict

    def _profile_clone_source(self,case,inputs,role=None):
        """Provide a compact descriptor of a pinned source; do not copy scientific approval or place the full text in model input."""
        previous=case.get("previous_artifact_ref")
        if role and inputs.get("resume_producer_job_id"):
            from .partial_clone import partial_clone_source
            source = partial_clone_source(self.ws, role, {**inputs, "budget_scope": case["budget_scope"],
                "previous_artifact_ref": previous, "prior_unreviewed_work_refs": case.get("resume_work_refs", [])})
            if source:
                return source
        if previous:
            item=self.artifacts.get(previous)
            if item["kind"]=="research" and item["data"].get("profile_ref"):
                research=item["data"]
                if research.get("candidate_ref")!=case["candidate_ref"] or research.get("identity_ref")!=inputs["identity_ref"]:
                    raise ProtocolError("The revision draft source does not bind the current candidate/identity")
                if inputs.get("setting_id") is not None and research.get("setting_id")!=inputs["setting_id"]:
                    raise ProtocolError("The revision draft source does not match the current setting target")
                ref=research["profile_ref"]
                profile=self.artifacts.get(ref)
                if profile["kind"]!="profile" or profile["data"].get("setting_id")!=research.get("setting_id"):
                    raise ProtocolError("The formal profile source for the revision draft does not match")
                return {"source_ref":ref,"source_pointer":"","expected_digest":digest(profile["data"])}
        ref=inputs.get("base_profile_ref")
        if ref:
            item=self.artifacts.get(ref)
            if item["kind"]!="native_record" or item["data"].get("version")!=inputs.get("base_version"):
                raise ProtocolError("The formal version of the baseline draft does not match")
            native=item["data"]
            if not inputs.get("setting_id") or native.get("setting_id")!=inputs["setting_id"] or not isinstance(native.get("content"),dict) or native["content"].get("setting_id")!=inputs["setting_id"]:
                raise ProtocolError("The baseline draft does not match the current setting target")
            return {"source_ref":ref,"source_pointer":"/content","expected_digest":digest(item["data"]["content"])}
        return None

    def assess_transfer(self, case_id, setting_id, *, material_refs=()):
        return transfer.transfer_case(self, case_id, setting_id, material_refs)

    def _stage(self,case,role,inputs):
        if case.get("transfer_scope_ref") and role in {"bound_updater", "profile_reviewer"}:
            inputs = {**inputs, **transfer.stage_inputs(self.artifacts.get, case, role)}
        if role in {"bound_updater","profile_researcher","profile_reviewer"}:
            inputs={**inputs,"coverage_scope_ref":self.put("external_result",coverage_scope(case["candidate_ref"]))}
            # Migrate a resumed lineage using its earliest available formal review,
            # never a producer's self-selected later frontier or a changed identity.
            if not case.get("delivery_scope_ref"):
                for saved in (*case.get("history", []), case):
                    if saved.get("candidate_ref") != case["candidate_ref"]:
                        continue
                    ref=saved.get("profile_review_ref") or saved.get("repair_feedback_ref")
                    if not ref:
                        continue
                    item=self.artifacts.get(ref)
                    if item["kind"] != "review" or item["data"].get("review_type") != "profile":
                        continue
                    anchor=freeze_delivery_scope(self.artifacts,case["candidate_ref"],ref)
                    if anchor["identity_ref"] != case.get("identity_ref",inputs.get("identity_ref")):
                        continue
                    case["delivery_scope_ref"]=self.put("external_result",anchor)
                    break
            if case.get("delivery_scope_ref"):
                inputs["delivery_scope_ref"]=case["delivery_scope_ref"]
        if role in {"bound_updater","profile_researcher"}:
            if case.get("resume_producer_job_id"):
                inputs["resume_producer_job_id"] = case["resume_producer_job_id"]
            source=self._profile_clone_source(case,inputs,role)
            if source:
                inputs={**inputs,"profile_clone_source":source}
            if case.get("repair_feedback_ref") and case.get("previous_artifact_ref"):
                from .review_packet import revision_materials
                repairs = revision_materials(self.artifacts, self.ws, case["previous_artifact_ref"], case["repair_feedback_ref"])
                if repairs:
                    inputs["revision_materials_ref"] = self.put("external_result", repairs)
        if role=="profile_reviewer" and self.artifacts.get(inputs["subject_ref"])["kind"]=="proposal":
            inputs["issue_scope_contract_version"] = "occurrence-bound-scope"
            from .review_context import build_review_context
            from .proof_reuse import build_proof_review_context
            from .review_packet import assemble_review_packet
            context=build_review_context(self.artifacts,self.ws,inputs["subject_ref"],case.get("repair_feedback_ref"))
            inputs["review_context_ref"]=self.put("external_result",context)
            proof_context=build_proof_review_context(self.artifacts,self.ws,inputs["subject_ref"],case.get("repair_feedback_ref"))
            inputs["proof_context_ref"]=self.put("external_result",proof_context)
            packet = assemble_review_packet(self.artifacts, inputs["subject_ref"], context, proof_context,
                                            delivery_scope_ref=case.get("delivery_scope_ref"),
                                            proof_context_ref=inputs["proof_context_ref"])
            inputs["review_packet_ref"] = self.put("external_result", packet)
            if case.get("projection_repair_ref"):
                inputs["projection_repair_ref"] = case["projection_repair_ref"]
        prior_work=case.get("resume_work_refs",[]) if not role.endswith("reviewer") else []
        materials=case.get("material_refs",[])
        if role in {"bound_updater","profile_researcher","profile_reviewer"}:materials=list(dict.fromkeys(materials+case.get("research_material_refs",[])))
        job,ref=self._job(role,{**inputs,"material_refs":materials,"material_policy":"Additional research material is an unapproved lead only; recheck genuine sources and proofs, and do not present it as independent approval in the current run.","revision":case.get("revision",0),"repair_feedback_ref":case.get("repair_feedback_ref"),"previous_artifact_ref":case.get("previous_artifact_ref"),"prior_unreviewed_work_refs":prior_work},case["budget_scope"])
        case["jobs"][role]=job["id"]
        if ref and role=="profile_reviewer" and not case.get("delivery_scope_ref"):
            case["delivery_scope_ref"]=self.put("external_result",freeze_delivery_scope(self.artifacts,case["candidate_ref"],ref))
        if not ref:
            case["state"]=role+":"+job["status"]
            if job.get("output"):
                prior=list(job["output"]["artifact_refs"])
                if job["output"].get("checkpoint_ref"):prior.append(job["output"]["checkpoint_ref"])
                case.setdefault("partial_refs",{})[role]=list(dict.fromkeys(prior))
        self.ws.save_case(case)
        return ref

    def _advance(self,case):
        cref=case["candidate_ref"]
        if not case.get("identity_ref"):
            iref=self._stage(case,"matcher",{"candidate_ref":cref,"extraction_review_ref":case["extraction_review_ref"],"atlas_version":self.atlas.version()})
            if not iref: return case
            identity=self.artifacts.get(iref)["data"]; case["identity_ref"]=iref
            if identity["decision"]=="unresolved":
                case["state"]="identity_unresolved"; self.ws.save_case(case); return case
        iref=case["identity_ref"]; identity=self.artifacts.get(iref)["data"]
        if identity["decision"]=="unresolved":
            case["state"]="identity_unresolved";self.ws.save_case(case);return case
        if not case.get("identity_review_ref"):
            review_ref=self._stage(case,"identity_reviewer",{"subject_ref":iref,"candidate_ref":cref,"extraction_review_ref":case["extraction_review_ref"]})
            if not review_ref: return case
            case["identity_review_ref"]=review_ref
        ir=self.artifacts.get(case["identity_review_ref"])["data"]
        if ir["verdict"]!="approve": case["state"]="identity_"+ir["verdict"]; self.ws.save_case(case); return case
        scope = self.artifacts.get(case["transfer_scope_ref"])["data"] if case.get("transfer_scope_ref") else None
        if scope and not transfer.source_is_current(self, scope):
            case["state"] = "identity_stale"; self.ws.save_case(case); return case
        if scope and self.atlas.version(scope["setting_id"]) != scope["base_version"] and not case.get("proposal_ref"):
            case["state"]="atlas_conflict"; case["diagnostic"]="The pinned transfer target changed; refresh the research baseline."
            self.ws.save_case(case); return case
        role="bound_updater" if scope or identity["decision"]=="existing" else "profile_researcher"
        if not case.get("research_ref"):
            sid = scope["setting_id"] if scope else identity["setting_id"]
            base = scope["base_version"] if scope else self.atlas.version(sid) if role=="bound_updater" else None
            inputs={"candidate_ref":cref,"identity_ref":iref,"identity_review_ref":case["identity_review_ref"],"base_version":base,"setting_id":sid}
            if scope:
                inputs["base_profile_ref"] = scope["target_files"]["profile.json"]
            elif base:
                inputs["base_profile_ref"]=self.put("native_record",{"setting_id":sid,"version":base,"content":self.atlas.read(sid)})
            rref=self._stage(case,role,inputs)
            if not rref:return case
            case["research_ref"]=rref
        rref=case["research_ref"]; research=self.artifacts.get(rref)["data"]
        if scope:
            transfer.check_transfer_research(scope, research, self.artifacts.get)
        if research["action"]=="no_change":
            if not case.get("profile_review_ref"):
                rr=self._stage(case,"profile_reviewer",{"subject_ref":rref,"mode":"no_change","candidate_ref":cref})
                if not rr:return case
                case["profile_review_ref"]=rr
            verdict=self.artifacts.get(case["profile_review_ref"])["data"]["verdict"]
            if verdict=="approve":
                from .joint_review import require_joint_checks, validate_no_change
                final_review = self.artifacts.get(case["profile_review_ref"])["data"]
                require_joint_checks(final_review)
                if scope: transfer.check_profile_handoff(self, case, rref)
                validate_no_change(self.atlas, research)
            case["state"]="no_change" if verdict=="approve" else "profile_"+verdict
            self.ws.save_case(case);return case
        if not case.get("proposal_ref"):
            try:
                case["proposal_ref"] = self._prepare_proposal(case)
            except (ValueError,KeyError) as exc:
                case["state"]="proposal_protocol_error";case["diagnostic"]=str(exc);self.ws.save_case(case);return case
        pref=case["proposal_ref"]
        if not case.get("profile_review_ref"):
            rr=self._stage(case,"profile_reviewer",{"subject_ref":pref,"mode":research["action"],"candidate_ref":cref})
            if not rr:return case
            case["profile_review_ref"]=rr
        review=self.artifacts.get(case["profile_review_ref"])["data"]
        if review["verdict"]!="approve":
            case["state"]="profile_"+review["verdict"];self.ws.save_case(case)
            from ..atlas.projection_report import mechanical_repair_request
            from ..atlas.store import _active_bounds
            prop=self.artifacts.get(case["proposal_ref"])["data"]
            active=_active_bounds(self.artifacts.get(prop["profile_ref"])["data"])
            if mechanical_repair_request(review, active_bound_ids=active):
                if prop["profile_ref"] not in case.get("projection_repair_attempts", []):
                    return self.reprepare_case(case["case_id"], mechanical=True)
                case["state"]="projection_review_unresolved"
                self.ws.save_case(case)
            return case
        if self.config.get("publication",{}).get("require_human_approval",False) and not case.get("human_approved"):
            case["state"]="ready_for_approval";self.ws.save_case(case);return case
        return self._commit(case)

    def _prepare_proposal(self, case):
        research = self.artifacts.get(case["research_ref"])["data"]
        profile = self.artifacts.get(research["profile_ref"])["data"]
        identity = self.artifacts.get(case["identity_ref"])["data"]
        candidate = self.artifacts.get(case["candidate_ref"])["data"]
        facts = (transfer.target_facts(research.get("tag_facts")) if case.get("transfer_scope_ref")
                 else profile_facts(candidate, identity, profile, research.get("tag_facts")))
        prepared = self.atlas.prepare(profile, facts, research["base_version"])
        frozen = self.put("profile", prepared["files"]["profile.json"], [case["research_ref"]])
        return self.put("proposal", {
            "research_ref":case["research_ref"], "candidate_ref":case["candidate_ref"],
            "identity_ref":case["identity_ref"], "profile_ref":frozen,
            "prepared_ref":self.put("prepared", prepared, [frozen]), "change_summary":research["change_summary"],
            "base_version":research["base_version"], "inventory_version":identity["recall_audit"]["inventory_version"],
            "mode":research["action"],
        })

    def reprepare_case(self, case_id, *, mechanical=False):
        """Reproject an unadopted frozen study and submit changed native sidecars for a new review."""
        from ..core.store import dumps

        case = self.ws.case(case_id)
        interrupted = case["state"] == "profile_reviewer:transport_uncertain"
        if interrupted:
            reviewer = self.ws.job(case["jobs"]["profile_reviewer"])
            if (reviewer["status"] != "transport_uncertain" or reviewer["role"] != "profile_reviewer"
                    or reviewer["inputs"]["subject_ref"] != case["proposal_ref"]
                    or case.get("profile_review_ref") or case.get("receipt_ref")):
                raise ProtocolError("Reprojection requires an interrupted reviewer of this exact unadopted proposal.")
        elif case["state"] not in {"profile_revise","profile_defer","ready_for_approval"}:
            raise ProtocolError("Reprojection requires a finished or interrupted independent review of an uncommitted proposal.")
        prior_record = dumps(case)
        prior = self.artifacts.get(case["proposal_ref"])["data"]
        if not interrupted:
            prior_review = self.artifacts.get(case["profile_review_ref"])["data"]
            check_review(prior_review, case["proposal_ref"], "profile")
        if mechanical:
            from ..atlas.projection_report import mechanical_repair_request
            from ..atlas.store import _active_bounds
            active=_active_bounds(self.artifacts.get(prior["profile_ref"])["data"])
            if interrupted or not mechanical_repair_request(prior_review, active_bound_ids=active):
                raise ProtocolError("Automatic reprojection requires a review containing only declared mechanical sidecar blockers")
            if prior["profile_ref"] in case.get("projection_repair_attempts", []):
                raise ProtocolError("This scientific snapshot already received its automatic projection review")
        try:
            new_ref = self._prepare_proposal(case)
            revised = self.artifacts.get(new_ref)["data"]
            if revised["profile_ref"] != prior["profile_ref"]:
                raise ProtocolError("Reprojection changed the scientific profile. Use a research revision.")
            old_hash = self.artifacts.get(prior["prepared_ref"])["data"]["bundle_hash"]
            new_hash = self.artifacts.get(revised["prepared_ref"])["data"]["bundle_hash"]
        except (ValueError, KeyError) as exc:
            if not mechanical:
                raise
            case.update(state="projection_protocol_error", diagnostic=str(exc),
                projection_diagnostic_ref=self.put("external_result", {
                    "kind": "mechanical_reprojection_failure", "proposal_ref": case["proposal_ref"],
                    "review_ref": case["profile_review_ref"], "errors": getattr(exc, "diagnostics", [{"code": "projection_error", "message": str(exc)}])}))
            with self.ws.transaction() as db:
                changed = db.execute("UPDATE cases SET record=?,state=? WHERE id=? AND record=?",
                                     (dumps(case),case["state"],case_id,prior_record)).rowcount
                if not changed:
                    raise ProtocolError("The case advanced concurrently. Reload its current review.") from exc
            return case
        if new_hash == old_hash and not mechanical:
            return case
        if mechanical:
            from ..atlas.projection_report import projection_report
            case.setdefault("projection_repair_attempts", []).append(prior["profile_ref"])
            case["projection_repair_ref"] = self.put("external_result", {
                "kind": "mechanical_reprojection", "previous_review_ref": case["profile_review_ref"],
                "previous_proposal_ref": case["proposal_ref"], "subject_ref": new_ref,
                "scientific_profile_unchanged": True, "bundle_changed": new_hash != old_hash,
                "requested_repairs": prior_review["projection_repairs"],
                "projection": projection_report(self.artifacts.get(revised["prepared_ref"])["data"]),
                "instruction": "Independently recheck each claimed sidecar defect against the actual field directory and generated files. No scientific issue or approval is cleared by reprojection; complete all current review checks."})
        case["history"].append({key:value for key,value in case.items() if key not in {"history","jobs"}})
        if case.get("profile_review_ref"):
            case["repair_feedback_ref"] = case.pop("profile_review_ref")
        case.update(proposal_ref=new_ref, revision=case.get("revision",0)+1, state="proposal_reprojected")
        case.pop("human_approved", None)
        with self.ws.transaction() as db:
            changed = db.execute("UPDATE cases SET record=?,state=? WHERE id=? AND record=?",
                                 (dumps(case),case["state"],case_id,prior_record)).rowcount
            if not changed:
                raise ProtocolError("The case advanced concurrently. Reload its current review.")
        return self._advance(case)

    def _commit(self,case):
        proposal=self.artifacts.get(case["proposal_ref"])["data"]
        prepared=self.artifacts.get(proposal["prepared_ref"])["data"]
        review=copy.deepcopy(self.artifacts.get(case["profile_review_ref"])["data"])
        check_review(review,case["proposal_ref"],"profile")
        if review["verdict"]!="approve": raise ProtocolError("profile approval has not yet been obtained")
        if case.get("transfer_scope_ref"):
            scope = self.artifacts.get(case["transfer_scope_ref"])["data"]
            if not transfer.source_is_current(self, scope):
                case["state"]="identity_stale";self.ws.save_case(case);return case
            research = self.artifacts.get(proposal["research_ref"])["data"]
            transfer.check_transfer_research(scope, research, self.artifacts.get)
            transfer.check_profile_handoff(self, case, case["proposal_ref"])
            original = self.artifacts.get(scope["target_files"]["profile.json"])["data"]["content"]
            transfer.check_transfer_profile(prepared["files"]["profile.json"], original)
            if (proposal["mode"] != "update" or prepared["base_version"] != scope["base_version"] or
                    proposal["identity_ref"] != scope["identity_ref"] or proposal["candidate_ref"] != scope["candidate_ref"]):
                raise ProtocolError("Transfer proposal no longer binds the pinned source and target")
        # A new-setting decision has an inventory-wide validity window; if the write succeeded but the local case was not persisted, reconcile the existing receipt first.
        key=digest({"proposal":case["proposal_ref"],"review":case["profile_review_ref"]})
        if proposal["mode"]=="new" and self.atlas.version()!=proposal["inventory_version"]:
            import hashlib
            receipt_path=self.atlas.state/"receipts"/(hashlib.sha256(key.encode()).hexdigest()+".json")
            if not receipt_path.exists():
                case["state"]="identity_stale";self.ws.save_case(case);return case
        try:
            receipt=self.atlas.commit(prepared,review,idempotency_key=key)
        except AtlasConflict as exc:
            case["state"]="atlas_conflict";case["diagnostic"]=str(exc);self.ws.save_case(case);return case
        receipt.update(proposal_ref=case["proposal_ref"],review_ref=case["profile_review_ref"],case_id=case["case_id"])
        case["receipt_ref"]=self.put("receipt",receipt);case["state"]="committed"
        self.ws.save_case(case)
        self.ws.promote(case["proposal_ref"],case["profile_review_ref"])
        return case

    def _interrupted_revision_anchor(self, case, stage, producers):
        """Recover the frozen draft and review from this uninterrupted producer revision."""
        review_type = {"research": "profile", "identity": "identity", "extraction": "extraction"}[stage]
        # Older versions could already have cleared both references on material
        # resume. Walk back only through the same producer and candidate lineage.
        for saved in (case, *reversed(case.get("history", []))):
            role = saved["state"].split(":", 1)[0]
            if role not in producers or saved.get("candidate_ref") != case["candidate_ref"]:
                break
            if stage == "research" and saved.get("identity_ref") != case.get("identity_ref"):
                break
            feedback, previous = saved.get("repair_feedback_ref"), saved.get("previous_artifact_ref")
            if not feedback or not previous:
                continue
            item = self.artifacts.get(feedback)
            source = self.artifacts.get(previous)
            if item["kind"] != "review" or item["data"]["review_type"] != review_type or source["kind"] != stage:
                break
            data = source["data"]
            if stage == "extraction" and data["paper_ref"] != case["paper_ref"]:
                break
            if stage != "extraction" and data["candidate_ref"] != case["candidate_ref"]:
                break
            if stage == "research" and data["identity_ref"] != case.get("identity_ref"):
                break
            reviewed = item["data"]["subject_ref"]
            if reviewed != previous and stage == "research":
                subject = self.artifacts.get(reviewed)
                if subject["kind"] == "proposal":
                    reviewed = subject["data"]["research_ref"]
            if reviewed == previous:
                return feedback, previous
            break
        return None, None

    def resume_case(self,case_id,*,stage=None,material_refs=(),approve=False):
        case=self.ws.case(case_id)
        if case.get("transfer_scope_ref") and stage not in {None, "research"}:
            raise ProtocolError("Assess transfer is independent of source extraction and identity; revise only its research stage")
        if approve:
            if case["state"]!="ready_for_approval":raise ProtocolError("This case is not awaiting human approval")
            case["human_approved"]=True; self.ws.save_case(case);return self._commit(case)
        if case["state"] in {"committed","no_change"}: return case
        if stage:
            if stage not in {"extraction","identity","research"}: raise ProtocolError("Unknown revision stage")
            for ref in material_refs:self.artifacts.get(ref)
            old_materials=set(case.get("material_refs",[])); new_materials=set(material_refs)-old_materials
            feedback=case.get("profile_review_ref") if stage=="research" else case.get("identity_review_ref") if stage=="identity" else case.get("extraction_review_ref")
            review=self.artifacts.get(feedback)["data"] if feedback else {}
            candidate_revise=(stage=="extraction" and self._candidate_verdict(feedback,case["candidate_ref"],self.artifacts.get(case["candidate_ref"])["data"]["candidate_id"])=="revise") if feedback else False
            atlas_changed=(stage=="identity" and case.get("identity_ref") and self.artifacts.get(case["identity_ref"])["data"]["recall_audit"]["inventory_version"]!=self.atlas.version())
            refresh = False
            if stage == "research" and case.get("transfer_scope_ref"):
                scope = self.artifacts.get(case["transfer_scope_ref"])["data"]
                refresh = self.atlas.version(scope["setting_id"]) != scope["base_version"]
            if not new_materials and review.get("verdict")!="revise" and not candidate_revise and not atlas_changed and not refresh:
                raise ProtocolError("Scientific revision requires new material or an explicit revise review request; ordinary resume does not resample a rejection")
            revision=case.get("revision",0)+1
            count=case.setdefault("revision_counts",{}).get(stage,0)+1
            if not new_materials and not atlas_changed and not refresh and count>self.config["budgets"]["max_science_revisions"]:
                raise ProtocolError("The revision budget for the same review is exhausted; new material is required")
            source_roles={"extraction":["extractor"],"identity":["matcher"],"research":["bound_updater","profile_researcher"]}[stage]
            previous=case.get({"extraction":"extraction_ref","identity":"identity_ref","research":"research_ref"}[stage])
            if new_materials and not feedback and not previous:
                feedback, previous = self._interrupted_revision_anchor(case, stage, source_roles)
            case["history"].append(copy.deepcopy({k:v for k,v in case.items() if k not in {"history","jobs"}}))
            case["revision"]=revision;case["material_refs"]=sorted(old_materials|new_materials)
            case["revision_counts"][stage]=count
            case["repair_feedback_ref"]=feedback
            case["previous_artifact_ref"]=previous
            role, _, status = case["state"].partition(":")
            case.pop("resume_producer_job_id", None)
            if stage == "research" and role in source_roles and status == "needs_materials":
                case["resume_producer_job_id"] = case["jobs"].get(role)
            case["resume_work_refs"]=list(dict.fromkeys(r for role in source_roles for r in case.get("partial_refs",{}).get(role,[])))
            remove=["research_ref","proposal_ref","profile_review_ref","receipt_ref"]
            remove += ["projection_repair_ref"]
            if stage in {"extraction","identity"}:remove += ["identity_ref","identity_review_ref"]
            if stage in {"extraction","identity"}:remove += ["delivery_scope_ref"]
            for key in remove:case.pop(key,None)
            if stage=="extraction":
                case["pending_extraction"]={"previous_candidate_ref":case["candidate_ref"],"feedback_ref":feedback}
            if case.get("transfer_scope_ref"): case.pop("human_approved", None)
            if refresh: transfer.refresh_target(self, case)
            case["state"]=stage+"_revised"; self.ws.save_case(case)
        elif case["state"] in {"identity_unresolved","identity_revise","identity_defer","profile_revise","profile_defer","extraction_revise","extraction_defer","identity_stale","atlas_conflict","proposal_protocol_error"}:
            return case
        if case.get("pending_extraction"):
            pending=case["pending_extraction"];old=pending["previous_candidate_ref"]
            er=self._stage(case,"extractor",{"paper_ref":case["paper_ref"],"previous_candidate_ref":old,"repair_feedback_ref":pending["feedback_ref"]})
            if not er:return case
            rr=self._stage(case,"extraction_reviewer",{"subject_ref":er,"paper_ref":case["paper_ref"],"previous_candidate_ref":old,"repair_feedback_ref":pending["feedback_ref"]})
            if not rr:return case
            cr=self.artifacts.get(er)["data"]["candidate_refs"][0];c=self.artifacts.get(cr)["data"]
            case.update(candidate_ref=cr,extraction_ref=er,extraction_review_ref=rr)
            case.pop("pending_extraction")
            verdict=self._candidate_verdict(rr,cr,c["candidate_id"])
            if verdict!="approve":case["state"]="extraction_"+verdict;self.ws.save_case(case);return case
            self.ws.save_case(case)
        return self._advance(case)

    def counts(self,case_ids=None):
        ids=set(case_ids) if case_ids is not None else None
        records=[json.loads(x["record"]) for x in self.ws.query("SELECT record FROM cases")]
        if ids is not None:records=[x for x in records if x["case_id"] in ids]
        result={"candidates":len(records),"committed":0,"no_change":0,"remaining":0}
        for c in records:
            key=c["state"] if c["state"] in {"committed","no_change"} else "remaining"
            result[key]+=1
        return result
