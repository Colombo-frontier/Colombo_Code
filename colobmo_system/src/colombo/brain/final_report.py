"""Deterministic publication of already adopted research; never invokes a model."""
from __future__ import annotations

import json

from colombo.shared.file_io import atomic_write, json_bytes, json_equal
from colombo.brain.research_store import StoreError, now


def conclude(store, *, require_proof=True):
    """Publish a fixed Conclusion and restore its status after export recovery."""
    ref = finalize(store, require_proof=require_proof)
    export_final(store)
    # Export can fail after Conclusion commits. Only a successful replay may
    # restore its original completed/partial status from needs_attention.
    conclusion = store.read_record(ref)
    basis = store.get_meta("finalization", {})
    stop_reason = "" if conclusion["status"] == "completed" else basis.get("reason", store.get_meta("stop_reason"))
    if store.get_meta("status") != conclusion["status"] or store.get_meta("stop_reason") != stop_reason:
        store.set_meta(status=conclusion["status"], stop_reason=stop_reason)
    return ref


def _publication_alignment(meta, progress, proof, read, require_proof):
    """A scientific status string cannot replace review of the exact final draft."""
    if not require_proof:
        return True
    from colombo.brain.final_completion import proof_steps_complete, review_completes_goal
    if not proof or not progress or progress.get("proof_ref") != meta.get("proof_ref"):
        return False
    review_ref = proof.get("review_ref")
    if (not review_ref or not proof_steps_complete(proof["proof_draft"])
            or progress.get("review_ref") != review_ref
            or progress.get("assessment_ref") != proof.get("assessment_ref")
            or meta.get("integration_review_ref") not in (None, review_ref)):
        return False
    review = read(review_ref)
    if not review_completes_goal(review):
        return False
    final_ref = meta.get("final_review_ref")
    final_id = final_ref.get("id") if isinstance(final_ref, dict) else final_ref
    review_id = review_ref.get("id") if isinstance(review_ref, dict) else review_ref
    proof_ref = meta.get("proof_ref")
    proof_id = proof_ref.get("id") if isinstance(proof_ref, dict) else proof_ref
    checked = review.get("checked_refs", [])
    return (final_id == review_id and final_ref == review_ref
            and isinstance(checked, list) and all(isinstance(r, str) for r in checked)
            and len(checked) == len(set(checked))
            and proof_id in checked
            and (not progress.get("assessment_ref")
                 or progress["assessment_ref"]["id"] in checked))


def finalize(store, *, reason=None, require_proof=True):
    """Commit the conclusion and terminal control state in one writer snapshot."""
    from colombo.brain.research_records import apply_control, insert
    from colombo.brain.research_records import unresolved_reviews

    with store.writer_snapshot() as (db, documents, meta):

        def read(ref):
            return store._read_row(store._row(db, ref), documents)

        if meta.get("phase") == "done" and meta.get("conclusion_ref"):
            return meta["conclusion_ref"]
        if meta.get("pending_call"):
            raise StoreError("Cannot finalize an unresolved model invocation")
        registered = {e["id"]: e["result_ref"] for e in meta.get("result_events", [])}
        for task in documents["research"]["tasks"].values():
            runtime = task.get("runtime", {})
            aid = runtime.get("active_attempt")
            if aid and not task.get("attempts", {}).get(aid, {}).get("result_ref"):
                raise StoreError("Cannot finalize an execution without a reconciled result")
            if require_proof and task.get("assignment_ref"):
                for attempt_id, attempt in task.get("attempts", {}).items():
                    result_ref = attempt.get("result_ref")
                    if result_ref and registered.get(task["task_id"] + ":" + attempt_id) != result_ref:
                        raise StoreError("Cannot finalize before durable results are registered")
        if any(c.get("state") not in {"confirmed", "already_completed", "superseded"}
               for c in meta.get("prune_commands", [])):
            raise StoreError("Cannot finalize before stop commands are reconciled")
        progress_ref, proof_ref = meta.get("progress_ref"), meta.get("proof_ref")
        progress = read(progress_ref) if progress_ref else None
        proof = read(proof_ref) if proof_ref else None
        feedback = unresolved_reviews(meta, read)
        if meta.get("integration_review_ref"):
            latest_review = meta["integration_review_ref"]
            report = read(latest_review)
            if report.get("verdict") != "pass" and not any(x["review_ref"] == latest_review for x in feedback):
                feedback.append({"review_ref": latest_review, "review": report})
        pending = [e for e in meta.get("result_events", [])
                   if e.get("state") not in {"processed", "processed_cancellation"}]
        aligned = _publication_alignment(meta, progress, proof, read, require_proof)
        complete = bool(progress and progress["progress"].get("status") == "completed"
            and aligned and not pending and not feedback and not meta.get("unresolved_review_ref"))
        stop_reason = reason or meta.get("stop_reason") or ("goal_completed" if complete else "research_stopped")
        remaining = []
        if not complete:
            if progress:
                remaining.extend(progress["progress"].get("remaining", []))
                for item in progress["progress"].get("items", []):
                    remaining.extend(item.get("remaining", []))
                for regime in progress["progress"].get("bracket", {}).get("regimes", []):
                    remaining.extend(regime.get("remaining", []))
            else:
                remaining.append("No goal progress has yet passed global review and been formally adopted.")
            if proof:
                remaining.extend(proof["proof_draft"].get("open_questions", []))
                for step in proof["proof_draft"].get("steps", []):
                    if step.get("status") != "retired":
                        remaining.extend(step.get("gaps", []))
            remaining.extend("Result not yet formally adopted: " + e["id"] for e in pending)
            for item in feedback:
                remaining.extend(f.get("reason", str(f)) for f in item["review"].get("findings", []))
            if meta.get("unresolved_review_ref") and not feedback:
                remaining.append("Unresolved global review comments remain.")
            remaining.append("Reason for ending the run: " + stop_reason)
            remaining = list(dict.fromkeys(remaining))
        status = "completed" if complete else "partial"
        summary = ("The original goal has been formally completed; this report summarizes the adopted progress and proof without introducing new research judgments." if complete
                   else "This research phase has ended. The formally adopted results and outstanding items are retained below; unreviewed candidates do not establish completion.")
        payload = {"status": status, "summary": summary,
                   "result_refs": progress.get("result_refs", []) if progress else [], "remaining": remaining}
        if complete and proof and proof.get("proof_draft", {}).get("open_questions"):
            payload["open_questions"] = list(proof["proof_draft"]["open_questions"])
        request_id = "controller-finalization"
        previous = db.execute("SELECT * FROM record_requests WHERE id=?", (request_id,)).fetchone()
        if previous:
            ref = store._ref(store._row(db, previous["ref_id"]))
            if not json_equal(read(ref), payload):
                raise StoreError("Finalization replay differs from its committed conclusion")
        else:
            ref = insert(store, db, documents, "conclusion", payload, meta)
            db.execute("INSERT INTO record_requests VALUES(?,?,?,?)",
                       (request_id, "conclusion", ref["id"], json.dumps(list(payload))))
        changes = {"phase": "done", "status": status, "pending_call": None,
                   "conclusion_ref": ref, "stop_reason": "" if complete else stop_reason,
                   "finalization": {"renderer_version": 2, "progress_ref": progress_ref,
                       "proof_ref": proof_ref, "review_refs": [x["review_ref"] for x in feedback],
                       "draft_ref": meta.get("integration_draft_ref"),
                       "final_review_ref": meta.get("final_review_ref"),
                       "reason": stop_reason}}
        apply_control(documents, meta, changes)
        db.executemany("INSERT INTO meta VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                       [(k, json_bytes(v).decode()) for k, v in changes.items()])
        store._flush_documents(db, documents)
        db.execute("INSERT INTO events(name,payload,created_at) VALUES(?,?,?)",
                   ("conclusion_generated", json_bytes({"conclusion_ref": ref, "status": status}).decode(), now()))
        return ref


def export_final(store):
    """Rebuild the report from the committed conclusion and fixed adopted sources."""
    ref = store.get_meta("conclusion_ref")
    if not ref:
        return
    conclusion = store.read_record(ref)
    basis = store.get_meta("finalization")
    if not basis:  # Historical completed runs keep their existing publication.
        return
    lines = ["# Colombo Research Report", "", "Status: " + conclusion["status"], "", conclusion["summary"], "",
             "Reason for ending: " + basis["reason"], ""]
    if basis.get("progress_ref"):
        progress = store.read_record(basis["progress_ref"])
        lines += ["## Formal Goal Progress", "", "Pinned reference: " + basis["progress_ref"]["id"], ""]
        if basis.get("renderer_version", 1) >= 2:
            lines += [progress["progress"].get("overall", ""), ""]
        for item in progress["progress"].get("items", []):
            lines.append(f"- {item['goal_id']}: {item['status']}; {item['description']}")
        lines.append("")
        bracket = progress["progress"].get("bracket")
        if bracket:
            lines += ["### Live Complexity Bracket", "", "```json",
                      json.dumps(bracket, ensure_ascii=False, indent=2), "```", ""]
    if basis.get("proof_ref"):
        proof = store.read_record(basis["proof_ref"])
        if proof.get("review_ref"):
            from colombo.brain.proof_draft import render_proof
            lines += ["## Formally Adopted Proof", "", "Pinned reference: " + basis["proof_ref"]["id"],
                      "Review reference: " + proof["review_ref"]["id"], "",
                      "The pinned body text is reproduced below. Any wording that described it as a candidate at submission does not alter its subsequent formal adoption.", "",
                      render_proof(proof["proof_draft"]), ""]
    if basis.get("draft_ref") and basis["draft_ref"] != basis.get("proof_ref"):
        from colombo.brain.proof_draft import render_proof
        draft = store.read_record(basis["draft_ref"])
        lines += ["## ProofDraft Awaiting Final Verifier Approval", "",
                  "The following draft is retained for subsequent revision and is not a certified complete Proof.", "",
                  "Pinned reference: " + basis["draft_ref"]["id"], "",
                  render_proof(draft["proof_draft"]), ""]
    if conclusion["remaining"]:
        lines += ["## Outstanding Items", "", *["- " + x for x in conclusion["remaining"]], ""]
    if basis.get("review_refs"):
        lines += ["Unresolved reviews: ", "", *["- " + x["id"] for x in basis["review_refs"]], ""]
    if conclusion.get("open_questions"):
        lines += ["## Open Research Questions", "",
                  "The final review certifies the original Goal as complete. These questions are retained for further research, not as unresolved gaps in that Goal.", "",
                  *["- " + x for x in conclusion["open_questions"]], ""]
    lines += ["## Supporting Evidence", "", *["- " + x for x in conclusion["result_refs"]], "",
              "Conclusion reference: " + ref["id"], ""]
    atomic_write(store.root / "output/final.md", "\n".join(lines).encode("utf-8"))


def reconcile_completed_run(store):
    """Append a deterministic correction using an already completed final review."""
    from colombo.brain.completion_recovery import reconcile_completed_run as reconcile
    return reconcile(store)
