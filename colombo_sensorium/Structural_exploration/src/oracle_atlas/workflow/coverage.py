"""Structural constraints for the finite coverage ledger; independent researchers always review mathematical closure."""
from __future__ import annotations

from ..core.contracts import ProtocolError

CHECKS = (
    "zero_query", "exact_reconstruction", "coarse_accuracy", "dimension_endpoints",
    "confidence_endpoints", "degenerate_instances", "envelopes_and_monotonicity",
    "moment_contracts", "supported_transfers",
)


def coverage_scope(candidate_ref: str) -> dict:
    return {"contract_version":"1.0.2", "candidate_ref":candidate_ref,
            "checks":list(CHECKS),
            "policy":"For each item, state by view/regime whether it is proved, irrelevant, or specifically unresolved; the first review must consolidate all discovered mandatory obligations. New safety/correctness issues are never ignored because the frontier is frozen.",
            "scientific_limit":"The template does not prove that an arbitrary parameter domain is exhausted or promise to resolve every potential new algorithm; mark unevaluated directions explicitly as unassessed and do not claim exhaustive literature coverage or globally strongest results."}


def coverage_errors(data: dict, inputs: dict, role: str, artifacts, *, resolve=None) -> list[dict]:
    """Require the ledger only for new tasks explicitly bound to the 1.0.2 scope; older pinned records remain readable."""
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
        return [{"code":"coverage_ledger_missing","path":"/"+field,"message":"This task is bound to the 1.0.2 coverage ledger; first use schema_read and register each item. The ledger must not be omitted from the final handoff."}]
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
        return errors
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
    return errors
