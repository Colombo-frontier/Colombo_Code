"""Bind a lightweight relation audit to the exact proposed pruning inputs."""
from __future__ import annotations

import copy

from colombo.brain.submission_validation import ContractError
from colombo.shared.file_io import json_equal


RELATION_AUDIT_GOAL = (
    "Check every proposed pruning relation and all target obligations under its exact scopes. "
    "Use only the explicitly listed premises as assumptions; other supplied material is "
    "definitions or reference, not extra premises. Check implication or refutation and "
    "retained independent work. Do not re-prove premise truth. Pass only if every listed "
    "relation and obligation is justified; otherwise fail or uncertain."
)


def _canonical_relation(store, proposal, task):
    from colombo.brain.record_formats import PRUNE
    from colombo.brain.submission_validation import _shape

    relation = copy.deepcopy(proposal)
    relation.pop("audit_ref", None)
    candidate_schema = {**PRUNE, "required": [name for name in PRUNE["required"] if name != "audit_ref"]}
    relation = _shape(candidate_schema, relation)
    if not relation.get("premises"):
        raise ContractError("Relation audit requires explicit source premises")
    if {item["result_ref"] for item in relation["premises"]} != set(relation["evidence_refs"]):
        raise ContractError("Prune premises must cover exactly its evidence_refs")
    tid = task.get("task_id", task.get("id"))
    if tid != relation["task_id"] or task.get("active_attempt") != relation["attempt_id"]:
        raise ContractError("Relation audit task/attempt does not match the fixed target")
    assignment_ref = store.record_ref(task.get("assignment_ref"))
    if store.record_kind(assignment_ref) != "assignment":
        raise ContractError("Relation audit target needs an assignment record")
    assignment = store.read_record(assignment_ref)
    if assignment.get("task_id") != tid:
        raise ContractError("Relation audit assignment belongs to another task")
    spec = assignment["spec"]
    if spec["responsibility"]["retain"]:
        raise ContractError("A retained independent task cannot be pruned")
    if (set(relation["covered_deliverables"]) != set(spec["deliverables"])
            or len(relation["covered_deliverables"]) != len(set(relation["covered_deliverables"]))):
        raise ContractError("Relation audit must account for every target deliverable")
    sources = []
    for rid in relation["evidence_refs"]:
        ref = store.record_ref(rid)
        if store.record_kind(ref) != "result":
            raise ContractError("Relation premises must reference Cell results")
        result = store.read_record(ref)
        from colombo.brain.submission_validation import result_review
        _, report = result_review(store, rid)
        premises = [p for p in relation["premises"] if p["result_ref"] == rid]
        if result.get("evidence_kind") == "empirical" or any(not any(
                c["kind"] != "empirical" and all(c[k] == p[k] for k in ("statement", "assumptions", "scope"))
                for c in report["confirmed_claims"]) for p in premises):
            raise ContractError("Pruning premises must exactly match verified mathematical Claims")
        if result.get("task_id") == tid:
            raise ContractError("A target cannot use its own result to prune its active attempt")
        sources.append(ref)
    return {"proposal": relation,
            "target": {"task_id": tid, "attempt_id": relation["attempt_id"],
                       "assignment_ref": assignment_ref,
                       **{key: copy.deepcopy(spec[key]) for key in
                          ("responsibility", "instructions", "deliverables", "completion_criteria")}},
            "source_results": sources}


def prepare_relation_audit(store, context, goal, inputs):
    """Create small, program-bound relation inputs from an active process_results snapshot."""
    from colombo.brain.record_formats import ACTIVE_TASK_STATES

    if not isinstance(goal, str) or not goal.strip():
        raise ContractError("Relation audit goal must be nonempty")
    if not isinstance(inputs, dict) or set(inputs) - {"prune_relations", "context"}:
        raise ContractError("Relation audit inputs use prune_relations and optional context only")
    relations = inputs.get("prune_relations")
    if not isinstance(relations, list) or not 1 <= len(relations) <= 40:
        raise ContractError("Relation audit requires between 1 and 40 proposed relations")
    if not isinstance(inputs.get("context", {}), dict):
        raise ContractError("Relation audit context must be a JSON object")
    snapshot = {t["task_id"]: t for t in context.get("task_snapshot", [])}
    prepared, targeted = [], set()
    for relation in relations:
        if not isinstance(relation, dict) or "audit_ref" in relation:
            raise ContractError("Relation audit input cannot contain an audit_ref")
        tid = relation.get("task_id")
        if not isinstance(tid, str) or tid in targeted:
            raise ContractError("Relation audit requires distinct target tasks")
        task = snapshot.get(tid)
        live = store.get_task(tid)
        if (not task or not live or task.get("state") not in ACTIVE_TASK_STATES
                or live.get("state") not in ACTIVE_TASK_STATES
                or live.get("active_attempt") != task.get("active_attempt")
                or live.get("assignment_ref") != task.get("assignment_ref")):
            raise ContractError("Relation audit target is stale or outside the active snapshot")
        targeted.add(tid)
        prepared.append(_canonical_relation(store, relation, task))
    binding = {"kind": "prune_relations", "version": 2}
    effective = {"focus": goal, "context": copy.deepcopy(inputs.get("context", {})),
                 "prune_relations": prepared}
    return RELATION_AUDIT_GOAL, effective, binding


def validate_prune_audit(store, prune, task):
    """Return {ref,payload} only for a passing, exact, committed relation audit."""
    if not prune.get("audit_ref") or not prune.get("premises"):
        raise ContractError("Pruning requires a passing relation audit and explicit premises")
    ref = store.record_ref(prune["audit_ref"])
    if store.record_kind(ref) != "audit":
        raise ContractError("Prune audit_ref must name an audit record")
    record = store.read_record(ref)
    if (record.get("status") != "completed" or record.get("execution_unknown")
            or record.get("result", {}).get("verdict") != "pass"
            or record.get("result", {}).get("findings")):
        raise ContractError("Pruning needs a completed passing relation audit")
    binding = record.get("binding", {})
    if binding.get("kind") != "prune_relations" or binding.get("version") != 2:
        raise ContractError("A generic audit cannot authorize a pruning relation")
    audit_id = record.get("audit_id")
    if not isinstance(audit_id, str):
        raise ContractError("Relation audit identity is missing")
    request = store.get_request("audit:" + audit_id)
    if not request or request["state"] != "confirmed" or request.get("result", {}).get("ref") != ref:
        raise ContractError("Relation audit does not have a confirmed service receipt")
    frozen = request["payload"]
    if any(frozen.get(key) != record.get(key) for key in ("call_id", "request_id", "audit_id")):
        raise ContractError("Relation audit request identity differs from its record")
    payload = frozen["input"]
    if not json_equal(payload.get("binding"), binding) or payload.get("goal") != RELATION_AUDIT_GOAL:
        raise ContractError("Relation audit does not bind the expected input")
    relations = payload.get("inputs", {}).get("prune_relations", [])
    matches = [item for item in relations if item.get("target", {}).get("task_id") == prune["task_id"]
               and item.get("target", {}).get("attempt_id") == prune["attempt_id"]]
    if len(matches) != 1 or not json_equal(matches[0], _canonical_relation(store, prune, task)):
        raise ContractError("Prune proposal differs from the audited relation or task version")
    return {"ref": ref, "payload": record}
