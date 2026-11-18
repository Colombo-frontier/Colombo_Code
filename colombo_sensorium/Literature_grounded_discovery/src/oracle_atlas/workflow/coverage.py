"""Structural constraints for the finite coverage ledger; independent researchers always review mathematical closure."""
from __future__ import annotations

from ..core.contracts import ProtocolError, references, resolve_pointer

CHECKS = (
    "zero_query", "exact_reconstruction", "coarse_accuracy", "dimension_endpoints",
    "confidence_endpoints", "degenerate_instances", "envelopes_and_monotonicity",
    "moment_contracts", "supported_transfers",
)


def coverage_scope(candidate_ref: str) -> dict:
    return {"contract_version":"snapshot-bound-scope", "candidate_ref":candidate_ref,
            "checks":list(CHECKS),
            "policy":"For each item, state by view/regime whether it is proved, irrelevant, or specifically unresolved; the first review must consolidate all discovered mandatory obligations. New safety/correctness issues are never ignored because the frontier is frozen.",
            "scientific_limit":"The template does not prove that an arbitrary parameter domain is exhausted or promise to resolve every potential new algorithm; mark unevaluated directions explicitly as unassessed and do not claim exhaustive literature coverage or globally strongest results."}


def freeze_delivery_scope(artifacts, candidate_ref: str, review_ref: str) -> dict:
    """Pin the first reviewed delivery and its finite evidence/obligations, without judging mathematics."""
    review = artifacts.get(review_ref)
    if review["kind"] != "review" or review["data"]["review_type"] != "profile":
        raise ProtocolError("A delivery frontier requires a completed profile review")
    subject_ref = review["data"]["subject_ref"]
    subject = artifacts.get(subject_ref)
    research_ref = subject["data"]["research_ref"] if subject["kind"] == "proposal" else subject_ref
    research = artifacts.get(research_ref)
    if research["kind"] != "research" or research["data"]["candidate_ref"] != candidate_ref:
        raise ProtocolError("The delivery frontier must bind this candidate's research")
    body = research["data"]
    profile = artifacts.get(body["profile_ref"])["data"] if body.get("profile_ref") else {}
    return {"contract_version":"snapshot-bound-scope", "candidate_ref":candidate_ref,
            "identity_ref":body["identity_ref"], "initial_subject_ref":subject_ref,
            "initial_research_ref":research_ref, "initial_review_ref":review_ref,
            "initial_evidence_refs":sorted(references(body) | references(profile)),
            "mandatory_issue_ids":[i["issue_id"] for i in review["data"]["issues"]
                                   if set(i["blocks"]) & {"bound","profile","publication"}],
            "policy":"Finish the original finite delivery and its recorded obligations. Correctness, unsupported adoption, false optimality and source/contract defects always require repair. A newly invented compatible stronger construction is a typed synthesis followup unless it invalidates a current claim; preserve its evidence, affected cells and honest partial registered-envelope status. The independent reviewer decides the scientific distinction."}


def _delivery_errors(data, inputs, role, read):
    """Validate the finite handoff and durable followups; never infer scientific validity from prose."""
    anchor_ref = inputs.get("delivery_scope_ref")
    field = "coverage_ledger" if role in {"bound_updater","profile_researcher"} else "coverage_audit"
    if not anchor_ref:
        # New first-pass findings also need durable typed registration. Legacy
        # frozen ledgers remain readable without manufacturing a frontier.
        try:
            scope = read(inputs["coverage_scope_ref"])["data"]
        except (ProtocolError, KeyError, TypeError, ValueError):
            return []
        if scope.get("contract_version") != "snapshot-bound-scope":
            return []
    errors = []
    def add(code, path, message):
        errors.append({"code":code,"path":path,"message":message})
    producer = role in {"bound_updater","profile_researcher"}
    ledger = data.get(field, {})
    try:
        anchor = read(anchor_ref)["data"] if anchor_ref else None
        if anchor_ref and ledger.get("delivery_scope_ref") != anchor_ref:
            add("delivery_scope_binding", "/"+field, "Bind the controller's frozen delivery_scope_ref; a revision must not silently expand or replace its first-review frontier.")
        if producer:
            research = data
            profile = read(data["profile_ref"])["data"] if data.get("profile_ref") else {}
        else:
            subject = read(inputs["subject_ref"])
            if subject["kind"] == "proposal":
                research = read(subject["data"]["research_ref"])["data"]
                profile = read(subject["data"]["prepared_ref"])["data"]["files"]["profile.json"]
            else:
                research, profile = subject["data"], {}
        if anchor and (research["candidate_ref"] != anchor["candidate_ref"] or research["identity_ref"] != anchor["identity_ref"]):
            add("delivery_scope_identity", "/"+field, "The finite delivery frontier belongs to another candidate or identity.")
        previous = read(inputs["repair_feedback_ref"])["data"] if inputs.get("repair_feedback_ref") else {}
        prior = previous.get("coverage_audit", {}).get("followups", [])
        # A revise/defer review can omit an author's previously registered
        # finding just as an approval can. Preserve the authored ledger as an
        # independent inheritance source, including pre-fix historical reviews
        # that accidentally omitted it. Never use the current producer's own
        # draft as evidence that a historical finding has been retained.
        authored = []
        author_origins = {}
        inherited_research = []
        if anchor and anchor.get("initial_research_ref"):
            inherited_research.append(read(anchor["initial_research_ref"]))
        if inputs.get("previous_artifact_ref"):
            item = read(inputs["previous_artifact_ref"])
            if item["kind"] == "proposal":
                item = read(item["data"]["research_ref"])
            if item["kind"] == "research":
                inherited_research.append(item)
        if not producer:
            inherited_research.append({"kind": "research", "data": research})
        for item in inherited_research:
            body = item["data"]
            if item["kind"] != "research" or any(body.get(k) != research.get(k) for k in ("candidate_ref", "identity_ref")):
                add("delivery_history_identity", "/"+field, "Inherited followups must bind this candidate and identity.")
                continue
            rows = list(body.get("coverage_ledger", {}).get("followups", []))
            if body.get("profile_ref"):
                rows.extend(read(body["profile_ref"])["data"].get("delivery_followups", []))
            for row in rows:
                if row.get("obligation_id"):
                    authored.append(row)
                    # The earliest frozen authored record fixes provenance.
                    # None means author-originated, not a missing review ID.
                    author_origins.setdefault(row["obligation_id"], row.get("source_review_ref"))
        if not producer:
            for row in profile.get("delivery_followups", []):
                if row.get("obligation_id"):
                    authored.append(row)
                    author_origins.setdefault(row["obligation_id"], row.get("source_review_ref"))
        followups = ledger.get("followups", [])
        indexed = {f.get("obligation_id"):f for f in followups}
        profile_rows = profile.get("delivery_followups", [])
        analysis = profile.get("joint_analysis", research.get("joint_analysis", {}))
        synthesis = analysis.get("synthesis_coverage", {})
        obligations = {o["id"]:o for o in synthesis.get("obligations", [])}
        cells = {c["cell_id"] for c in analysis.get("domain_map", {}).get("cells", [])}
        comparisons = {c["comparison_id"] for c in analysis.get("comparisons", [])}
        required = {"scope","description","reason_nonblocking","obligation_id","evidence_refs","source_review_ref","retained_claims_valid"}
        if len(indexed) != len(followups):
            add("delivery_followup_duplicate", "/"+field+"/followups", "Each followup needs a unique native obligation_id.")
        for n, row in enumerate(followups):
            path = f"/{field}/followups/{n}"
            if not required.issubset(row) or not row.get("obligation_id") or row.get("retained_claims_valid") is not True or not row.get("evidence_refs"):
                add("delivery_followup_contract", path, "Provide typed followup fields, fixed evidence, native obligation_id and an independent explanation that retained claims remain valid. Errors cannot be deferred as improvements.")
                continue
            for ref in row["evidence_refs"]:
                read(ref)
            if row["source_review_ref"]:
                source = read(row["source_review_ref"])
                if source["kind"] != "review" or source["data"].get("review_type") != "profile":
                    add("delivery_followup_origin", path, "source_review_ref must identify the originating profile review.")
                elif not any(f.get("obligation_id") == row["obligation_id"] and f.get("description") == row["description"]
                             for f in source["data"].get("coverage_audit", {}).get("followups", [])):
                    add("delivery_followup_origin", path, "The cited originating review must actually contain this finding and obligation ID.")
            # A rejecting reviewer may introduce a followup for the author's next local edit.
            # An approval must already bind the exact authored and frozen publication record.
            if not producer and data.get("verdict") != "approve" and row not in profile_rows:
                continue
            obligation = obligations.get(row["obligation_id"])
            if not obligation:
                add("delivery_followup_obligation", path, "Register this followup in joint_analysis.synthesis_coverage.obligations before publication.")
                continue
            if not (obligation["cell_ids"] or obligation["comparison_ids"]) or not set(obligation["cell_ids"]).issubset(cells) or not set(obligation["comparison_ids"]).issubset(comparisons):
                add("delivery_followup_cells", path, "Bind existing affected cells/comparisons, including an explicit unassessed cell when necessary.")
            if obligation["state"] == "pending":
                if synthesis.get("status") == "complete" or synthesis.get("gap_basis") != "registered_envelope":
                    add("delivery_followup_synthesis", path, "Pending improvements require honest partial/unassessed synthesis with registered_envelope gap basis.")
                if row["description"] not in analysis.get("pending_obligations", []):
                    add("delivery_followup_visibility", path, "Preserve the exact followup description in pending_obligations; known stronger routes must remain visible.")
            if row not in profile_rows:
                add("delivery_followup_profile", path, "The same evidence-bearing followup must be retained in the frozen profile.delivery_followups.")
        inherited = [(old, author_origins[old["obligation_id"]]) for old in authored]
        for old in prior:
            oid = old.get("obligation_id")
            if oid:
                origin = author_origins[oid] if oid in author_origins else old.get("source_review_ref") or inputs["repair_feedback_ref"]
                inherited.append((old, origin))
        checked_inheritance = set()
        for old, origin in inherited:
            oid = old.get("obligation_id")
            if not oid:  # Legacy text-only records cannot manufacture a typed obligation.
                continue
            signature = (oid, old.get("description"), tuple(sorted(old.get("evidence_refs", []))), origin)
            if signature in checked_inheritance:
                continue
            checked_inheritance.add(signature)
            row = indexed.get(oid)
            if not row or row.get("description") != old["description"] or not set(old.get("evidence_refs", [])).issubset(row.get("evidence_refs", [])):
                add("delivery_followup_lost", "/"+field+"/followups", f"Retain followup {oid}, its original description and evidence; resolve its native obligation instead of deleting the finding.")
                continue
            if row.get("source_review_ref") != origin:
                add("delivery_followup_origin", "/"+field+"/followups", f"Preserve the recorded origin for {oid}; null denotes an author-originated finding.")
            if producer:
                resolution = next((r for r in ledger.get("issue_resolutions", []) if r["issue_id"] == oid), None)
                state = obligations.get(oid, {}).get("state")
                if not resolution or {"remaining":"pending","resolved":"resolved","not_applicable":"not_applicable"}.get(resolution["status"]) != state:
                    add("delivery_followup_resolution", "/coverage_ledger/issue_resolutions", f"Formally address {oid} and agree with its native obligation state. Remaining is a valid disposition if existing claims stay supported.")
        if producer and followups != profile_rows:
            add("delivery_followup_profile", "/coverage_ledger/followups", "Research and profile must preserve the same full followup ledger.")
        if not producer and data.get("verdict") == "approve":
            if followups != research.get("coverage_ledger", {}).get("followups", []) or followups != profile_rows:
                add("delivery_followup_unrecorded", "/coverage_audit/followups", "New findings cannot be appended after signing. Have the author register or resolve the typed obligations in research and the five-file profile, then review those local changes.")
        if not producer and anchor:
            prior_ids = {i["issue_id"] for i in previous.get("issues", [])}
            reasons = {r["issue_id"]:r for r in ledger.get("new_blocker_justifications", [])}
            for issue in data.get("issues", []):
                if issue["kind"] != "coverage" or not set(issue["blocks"]) & {"profile","publication"} or issue["issue_id"] in prior_ids:
                    continue
                reason = reasons.get(issue["issue_id"], {})
                basis = reason.get("basis")
                if basis not in {"current_claim_invalid","frozen_obligation","first_review_omission","new_evidence_defect"}:
                    add("delivery_new_construction", "/coverage_audit/new_blocker_justifications", "A newly invented compatible stronger construction does not extend this delivery automatically. Record a typed followup, or identify the concrete invalid claim, frozen obligation or source/contract defect requiring repair.")
                elif basis == "frozen_obligation":
                    ids = set(reason.get("frozen_issue_ids", []))
                    if not ids or not ids.issubset(anchor["mandatory_issue_ids"]):
                        add("delivery_frozen_obligation", "/coverage_audit/new_blocker_justifications", "Name the actual first-review obligation IDs.")
                else:
                    pointers = reason.get("affected_profile_pointers", [])
                    if not pointers or any(not p.startswith("/") for p in pointers):
                        add("delivery_affected_claim", "/coverage_audit/new_blocker_justifications", "Identify current profile fields affected by this concrete error or omission.")
                    for pointer in pointers:
                        resolve_pointer(profile, pointer)
    except (ProtocolError, KeyError, TypeError, ValueError) as exc:
        add("delivery_reference", "/"+field, str(exc))
    return errors


def coverage_errors(data: dict, inputs: dict, role: str, artifacts, *, resolve=None) -> list[dict]:
    """Require the ledger only for new tasks explicitly bound to the bound-review-context scope; older pinned records remain readable."""
    if not inputs.get("coverage_scope_ref"):
        return []
    producer=role in {"bound_updater","profile_researcher"}
    reviewer=role=="profile_reviewer"
    if not (producer or reviewer):
        return []
    field="coverage_ledger" if producer else "coverage_audit"
    read=resolve or artifacts.get
    value=data.get(field)
    errors=[]
    def add(code,path,message):
        errors.append({"code":code,"path":path,"message":message})
    if not isinstance(value,dict):
        return [{"code":"coverage_ledger_missing","path":"/"+field,"message":"This task is bound to the bound-review-context coverage ledger; first use schema_read and register each item. The ledger must not be omitted from the final handoff."}]
    seen=set()
    for i,row in enumerate(value.get("checks",[])):
        if not isinstance(row,dict):continue  # The schema validates shape.
        cid=row.get("check_id")
        if cid in CHECKS:seen.add(cid)
        if not str(row.get("reason","")).strip():
            add("coverage_reason",f"/{field}/checks/{i}/reason","Coverage status must specify its scope/basis or the unresolved missing step.")
        if not str(row.get("scope","")).strip():
            add("coverage_scope",f"/{field}/checks/{i}/scope","A check must specify its actual view/regime scope.")
        if row.get("status")=="verified" and not (row.get("result_refs") or row.get("proof_refs")):
            add("coverage_basis",f"/{field}/checks/{i}","A verified check must cite a verifiable formal result/proof; stating that it was checked is insufficient.")
        for k,kind in (("result_refs","result"),("proof_refs","proof")):
            for j,ref in enumerate(row.get(k,[])):
                try:
                    if read(ref)["kind"]!=kind:
                        add("coverage_dependency_kind",f"/{field}/checks/{i}/{k}/{j}",f"A formal {kind} artifact must be referenced here.")
                except (ProtocolError,KeyError,ValueError) as exc:
                    add("coverage_dependency",f"/{field}/checks/{i}/{k}/{j}",str(exc))
    for cid in set(CHECKS)-seen:
        add("coverage_check_missing",f"/{field}/checks",f"Coverage check {cid} is missing; even if not applicable, record an explicit reason.")
    prior={}
    ref=inputs.get("repair_feedback_ref")
    if ref:
        try:
            item=read(ref)
            if item["kind"]=="review" and item["data"].get("review_type")=="profile":
                prior={i["issue_id"]:i for i in item["data"].get("issues",[])
                       if set(i.get("blocks",[])) & {"profile","publication"}}
        except (ProtocolError,KeyError,ValueError) as exc:
            add("coverage_feedback","/coverage_audit",str(exc))
    if producer:
        resolutions={r.get("issue_id"):r for r in value.get("issue_resolutions",[]) if isinstance(r,dict)}
        for cid in prior.keys()-resolutions.keys():
            add("coverage_resolution_missing","/coverage_ledger/issue_resolutions",f"The revision must address historical blocker {cid} individually, including unresolved items and their specific missing steps.")
        return errors + _delivery_errors(data, inputs, role, read)
    resolved=set(value.get("resolved_issue_ids",[]));carried=set(value.get("carried_issue_ids",[]))
    current={i.get("issue_id"):i for i in data.get("issues",[])}
    if resolved & carried:
        add("coverage_issue_state","/coverage_audit","The same historical issue cannot be marked both resolved and carried.")
    for cid in prior.keys()-(resolved|carried):
        add("coverage_issue_omitted","/coverage_audit",f"Historical blocker {cid} has not been explicitly resolved or carried forward and cannot silently disappear.")
    for cid in carried:
        if cid not in current:
            add("coverage_issue_missing","/coverage_audit/carried_issue_ids",f"Carried item {cid} must remain in current issues with its actual scope.")
    for cid in resolved:
        if cid in current and set(current[cid].get("blocks",[])) & {"profile","publication"}:
            add("coverage_issue_state","/coverage_audit/resolved_issue_ids",f"{cid} still blocks current publication and cannot also be claimed as resolved.")
    reasons={r.get("issue_id"):r for r in value.get("new_blocker_justifications",[]) if isinstance(r,dict)}
    for issue in data.get("issues",[]):
        if issue.get("kind")!="coverage" or not (set(issue.get("blocks",[])) & {"profile","publication"}):continue
        cid=issue.get("issue_id")
        if cid in prior:continue
        reason=reasons.get(cid,{})
        if not str(reason.get("why_new","")).strip() or not issue.get("evidence_refs"):
            add("coverage_new_blocker_basis","/coverage_audit/new_blocker_justifications",f"New coverage blocker {cid} must state the specific omission/new evidence and why it was discovered only in this round, and bind formal evidence; merely saying it is insufficient is not enough.")
    reused=set(value.get("reused_bound_ids",[]))
    if reused:
        context_ref=inputs.get("review_context_ref")
        if not context_ref or value.get("reuse_context_ref")!=context_ref:
            add("review_reuse_context","/coverage_audit/reuse_context_ref","A reuse declaration must bind the review_context_ref provided by the controller for this task.")
        else:
            try:
                item=read(context_ref)
                if item["kind"]!="external_result" or not reused.issubset(set(item["data"].get("reusable_bound_ids",[]))):
                    add("review_reuse_scope","/coverage_audit/reused_bound_ids","Select only per-bound candidates whose unchanged dependencies the controller has verified; an identical ID or unapproved historical material is insufficient for reuse.")
            except (ProtocolError,KeyError,TypeError,ValueError) as exc:
                add("review_reuse_context","/coverage_audit/reuse_context_ref",str(exc))
        if not reused.issubset(set(data.get("approved_bound_ids",[]))):
            add("review_reuse_adoption","/approved_bound_ids","Reused candidates must still be explicitly listed in approved_bound_ids in the current review.")
    return errors + _delivery_errors(data, inputs, role, read)
