"""Explicit, append-only repair of a finalized completion-state projection."""
from __future__ import annotations

import copy
import json

from colombo.brain.final_completion import final_progress_payload, review_completes_goal
from colombo.brain.research_records import apply_control, insert, unresolved_reviews, state_view
from colombo.brain.research_store import StoreError, now
from colombo.shared.file_io import atomic_write, json_bytes, json_equal


def _export(store):
    from colombo.brain.final_report import export_final
    from colombo.brain.proof_draft import export_current
    export_final(store)
    export_current(store)
    store.export_documents()
    view = state_view(store)
    text = ("# Brain state\n\nThis file is a rebuildable view; the authoritative state "
            "is stored in the research records in state.sqlite.\n\n```json\n"
            + json.dumps(view, ensure_ascii=False, indent=2) + "\n```\n")
    atomic_write(store.root / "memory/brain_state.md", text.encode("utf-8"))


def reconcile_completed_run(store):
    """Correct control state from an existing final review; never invoke models.

    Old records and receipts remain immutable.  The replacement progress and
    conclusion explicitly retain their predecessors and original finalization.
    """
    from colombo.configuration import require_current_workflow
    from colombo.brain.final_report import _publication_alignment
    with store.exclusive():
        documents, meta, refs = store.snapshot()
        require_current_workflow(meta["config"])
        if meta.get("phase") != "done" or not meta.get("conclusion_ref"):
            raise StoreError("Completion reconciliation requires an already finalized run")
        if meta.get("pending_call") or store.unresolved_audits():
            raise StoreError("Cannot reconcile completion with a pending model call or audit")

        def read(ref):
            row = refs.get(ref["id"] if isinstance(ref, dict) else ref)
            if row is None:
                raise StoreError("Unknown reconciliation evidence reference")
            if isinstance(ref, dict) and ref.get("revision") != row["revision"]:
                raise StoreError("Reconciliation evidence revision mismatch")
            return store._read_row(row, documents)

        registered = {e["id"]: e["result_ref"] for e in meta.get("result_events", [])}
        if any(e.get("state") not in {"processed", "processed_cancellation"}
               for e in meta.get("result_events", [])):
            raise StoreError("Cannot reconcile completion before results are processed")
        for tid, task in documents["research"]["tasks"].items():
            runtime = task.get("runtime", {})
            aid = runtime.get("active_attempt")
            if (runtime.get("state") in {"prepared", "running", "stopping", "unknown", "needs_attention"}
                    or runtime.get("execution_fault_ref")
                    or aid and not task.get("attempts", {}).get(aid, {}).get("result_ref")):
                raise StoreError("Cannot reconcile completion with an unsettled Cell execution")
            for attempt_id, attempt in task.get("attempts", {}).items():
                result_ref = attempt.get("result_ref")
                if result_ref and registered.get(tid + ":" + attempt_id) != result_ref:
                    raise StoreError("Cannot reconcile completion with unregistered results")
        if (meta.get("unresolved_review_ref") or unresolved_reviews(meta, read)
                or any(c.get("state") not in {"confirmed", "already_completed", "superseded"}
                       for c in meta.get("prune_commands", []))):
            raise StoreError("Cannot reconcile completion with unresolved reviews or stops")

        stage = meta.get("integration", {})
        basis = meta.get("finalization", {})
        proof_ref, review_ref = meta.get("proof_ref"), meta.get("final_review_ref")
        if not proof_ref or not review_ref or not meta.get("progress_ref"):
            raise StoreError("Completion reconciliation requires a final proof and review")
        progress, proof, review = read(meta["progress_ref"]), read(proof_ref), read(review_ref)
        if (not review_completes_goal(review)
                or not json_equal(progress.get("proof_ref"), proof_ref)
                or not json_equal(progress.get("review_ref"), review_ref)
                or not json_equal(proof.get("review_ref"), review_ref)
                or not json_equal(stage.get("proof_ref"), proof_ref)
                or not json_equal(progress.get("assessment_ref"), stage.get("assessment_ref"))
                or not json_equal(proof.get("assessment_ref"), stage.get("assessment_ref"))
                or not json_equal(basis.get("proof_ref"), proof_ref)
                or not json_equal(basis.get("progress_ref"), meta["progress_ref"])
                or not json_equal(basis.get("final_review_ref"), review_ref)
                or meta.get("integration_review_ref") not in (None, review_ref)):
            raise StoreError("Completion reconciliation final evidence is not exactly aligned")
        if not _publication_alignment(meta, progress, proof, read, True):
            raise StoreError("Completion reconciliation lacks a complete, adopted final review")

        # Revalidate the complete package even when replaying a prior repair.
        payload = final_progress_payload(store, stage, review_ref, meta["progress_ref"])
        if payload["progress"].get("status") != "completed":
            raise StoreError("Final review does not establish completed Goal coverage")
        request_id = "final-completion-reconciliation:" + review_ref["id"]
        prior = store.request_record(request_id)
        if prior:
            if prior != meta["conclusion_ref"] or read(prior).get("status") != "completed":
                raise StoreError("Completion reconciliation receipt differs from current conclusion")
            _export(store)
            return prior
        if read(meta["conclusion_ref"]).get("status") == "completed":
            _export(store)
            return meta["conclusion_ref"]

        # The exclusive controller lock and this second snapshot prevent a stale
        # repair from applying over an intervening control/evidence change.
        with store.writer_snapshot() as (db, current_documents, current_meta):
            # Metadata-only writes and audit request changes need not increment
            # the document generation.  Check both inside the writer transaction.
            if not json_equal(current_meta, meta):
                raise StoreError("Run changed during completion reconciliation")
            if db.execute("SELECT 1 FROM requests WHERE id LIKE 'audit:%' "
                          "AND state IN ('pending','unknown') LIMIT 1").fetchone():
                raise StoreError("Cannot reconcile completion with a pending audit")
            new_progress = insert(store, db, current_documents, "goal_progress", payload, current_meta)
            correction = {"version": 1, "review_ref": review_ref,
                          "previous_progress_ref": meta["progress_ref"],
                          "previous_conclusion_ref": meta["conclusion_ref"],
                          "previous_finalization": copy.deepcopy(basis)}
            conclusion = {
                "status": "completed",
                "summary": "The original Goal is complete according to the exact final Verifier review. The earlier completion-state projection is retained in the linked historical conclusion.",
                "result_refs": payload["result_refs"], "remaining": [],
                "open_questions": copy.deepcopy(proof["proof_draft"].get("open_questions", [])),
                "supersedes": meta["conclusion_ref"], "completion_reconciliation": correction}
            ref = insert(store, db, current_documents, "conclusion", conclusion, current_meta)
            db.execute("INSERT INTO record_requests VALUES(?,?,?,?)",
                       (request_id, "conclusion", ref["id"], json.dumps(list(conclusion))))
            changes = {"phase": "done", "status": "completed", "stop_reason": "",
                       "progress_ref": new_progress, "conclusion_ref": ref,
                       "finalization": {**copy.deepcopy(basis), "progress_ref": new_progress,
                                        "reason": "goal_completed", "completion_reconciliation": correction}}
            apply_control(current_documents, current_meta, changes)
            db.executemany("INSERT INTO meta VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                           [(k, json_bytes(v).decode()) for k, v in changes.items()])
            store._flush_documents(db, current_documents)
            db.execute("INSERT INTO events(name,payload,created_at) VALUES(?,?,?)",
                       ("completion_state_reconciled", json_bytes({"conclusion_ref": ref,
                        "progress_ref": new_progress, **correction}).decode(), now()))
        _export(store)
        return ref
