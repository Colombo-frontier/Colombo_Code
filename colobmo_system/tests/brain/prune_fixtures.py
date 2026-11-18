"""Synthetic relation opinions exercising the real audit request/receipt path."""
import copy
import uuid
from unittest.mock import patch

from colombo.brain.evidence_audit import audit
from colombo.brain.pruning import prepare_relation_audit


def bind_prunes(store, context, proposals):
    if not proposals:
        return []
    relations = copy.deepcopy(proposals)
    for relation in relations:
        relation.pop("audit_ref", None)
        relation.setdefault("premises", [{"result_ref": ref, "statement": "Synthetic fixture premise",
            "assumptions": [], "scope": "Synthetic fixture domain"} for ref in relation["evidence_refs"]])
    goal, inputs, binding = prepare_relation_audit(store, context, "Check synthetic fixture relations",
                                                  {"prune_relations": relations})
    previous = store.get_meta("pending_call")
    call_id = (previous or {}).get("call_id") or "fixture-" + uuid.uuid4().hex
    store.set_meta(pending_call={"call_id": call_id, "role": "brain", "stage": "process_results"})
    try:
        with patch("colombo.brain.evidence_audit.run_audit", return_value={"verdict": "pass",
                "summary": "Synthetic fixture relation oracle", "findings": []}):
            reply = audit(store, call_id, goal, inputs, _binding=binding)
    finally:
        store.set_meta(pending_call=previous)
    return [{**relation, "audit_ref": reply["ref"]["id"]} for relation in relations]
