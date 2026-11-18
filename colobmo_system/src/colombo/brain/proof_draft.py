"""Create, freeze, resolve and render one versioned ProofDraft."""
from __future__ import annotations
import copy
from colombo.brain.record_formats import TEXT
from colombo.brain.submission_validation import ContractError
from colombo.brain.research_store import StoreError


def export_current(store):
    """Rebuild the readable current ProofDraft from its fixed formal version."""
    from colombo.shared.file_io import atomic_write
    ref = store.get_meta("proof_ref")
    if not ref:
        return
    record = store.read_record(ref)
    store.artifact_entries(ref)
    text = render_proof(record["proof_draft"]) + "\n"
    text += "Authoritative record: " + ref["id"] + "\n"
    atomic_write(store.root / "proof/current.md", text.encode("utf-8"))


def initial_proof(store):
    goal = store.read_record(store.get_meta("goal_ref"))
    return {"title": "Global Proof Draft", "statement": goal["goal"], "assumptions": [],
        "body": "No proof has been developed yet. The goals and gaps below support resuming the research; this initial outline has not undergone proof review.",
        "steps": [{"id": f"P{i}", "title": target["id"], "statement": target["text"],
                   "status": "open", "depends_on": [], "evidence": [],
                   "gaps": ["Develop a complete argument and provide pinned evidence."]}
                  for i, target in enumerate(goal["targets"])],
        "open_questions": ["Identify a proof strategy and establish the goals above step by step."]}


def render_proof(payload):
    lines = ["# " + payload["title"], "", "## Goal", "", payload["statement"], "",
             "## Assumptions", "", *["- " + x for x in payload["assumptions"]], "",
             "## Proof", "", payload["body"], "", "## Proof Steps and Evidence Index", ""]
    for step in payload["steps"]:
        lines += [f"### {step['id']} — {step['title']} [{step['status']}]", "", step["statement"], "",
                  "Dependencies: " + (", ".join(step["depends_on"]) or "None"), ""]
        for evidence in step["evidence"]:
            lines += [f"- Source: {evidence['result_ref']}; file: {evidence['path']}; locator: {evidence['locator']}"]
            if evidence.get("record_ref") is not None:
                ref = evidence["record_ref"]
                lines += [f"  Record: {ref['kind']}/{ref['id']}; revision: {ref['revision']}"]
        label = "- Reason for retirement: " if step["status"] == "retired" else "- Gap: "
        lines += [label + gap for gap in step["gaps"]]
        lines.append("")
    lines += ["## Open Questions", "", *["- " + x for x in payload["open_questions"]], ""]
    return "\n".join(lines)


def write_proof(store, payload, request_id, previous_ref=None, assessment_ref=None, review_ref=None):
    """Save one proof body; acceptance is a pointer/state change, not a copy."""
    from colombo.brain.submission_validation import validate_proof_shape
    payload = validate_proof_shape(payload)
    for ref in (previous_ref, assessment_ref, review_ref):
        if ref:
            store.read_record(ref)
    return store.write_record("proof_draft", {"proof_draft": payload,
        "previous_ref": previous_ref, "assessment_ref": assessment_ref,
        "review_ref": review_ref, "artifacts": [], "summary": payload["title"]},
        request_id=request_id)


def resolve_proof_source(store, proof):
    """Return a copy with the selected full artifact as ``body``.

    This validates the Result type, local acceptance and artifact access. The
    caller must still check admission to the Brain's proof, evidence, and review
    requirements. It neither changes stored records nor rewrites the text.
    """
    if not isinstance(proof, dict):
        raise ContractError("Proof draft must be an object")
    if "body_source" not in proof:
        return copy.deepcopy(proof)
    if "body" in proof:
        raise ContractError("Proof draft must provide body or body_source, not both")
    source = proof["body_source"]
    if not isinstance(source, dict) or set(source) != {"result_ref", "path"}:
        raise ContractError("Proof body_source requires exactly result_ref and path")
    if not isinstance(source["path"], str) or not source["path"].strip():
        raise ContractError("Proof body_source path must be a nonempty string")
    try:
        result_ref = store.record_ref(source["result_ref"])
        if store.record_kind(result_ref) != "result":
            raise ContractError("Proof body_source requires a Result reference")
        result = store.read_record(result_ref)
        if result.get("evidence_kind") == "empirical":
            raise ContractError("Empirical Result cannot supply Proof body_source")
        if result.get("accepted") is not True:
            raise ContractError("Proof body_source requires a locally accepted Cell Result")
        matches = [entry for entry in store.artifact_entries(result_ref)
                   if entry["path"] == source["path"]]
        if len(matches) != 1:
            raise ContractError("Proof body_source must select one unique artifact authorized by this Result")
        content = store.read_artifact(result_ref, source["path"], limit=TEXT["maxLength"])
    except (StoreError, OSError) as exc:
        raise ContractError(f"Cannot read proof body_source: {exc}") from exc
    if content["total_chars"] > TEXT["maxLength"]:
        raise ContractError(f"Proof body_source exceeds {TEXT['maxLength']} characters")
    if not content["text"].strip():
        raise ContractError("Proof body_source must contain nonempty proof text")
    resolved = copy.deepcopy(proof)
    resolved["body"] = content["text"]
    return resolved

