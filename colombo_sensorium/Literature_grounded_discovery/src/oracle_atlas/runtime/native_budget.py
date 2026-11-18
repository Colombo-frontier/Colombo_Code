"""Recover native MCP budget stops from host evidence while preserving genuine material requests."""
import hashlib
import json
import time

from ..core.store import dumps

CHECKPOINT_RESERVE = 3
BUDGET_REASON = "NATIVE_TOOL_BUDGET_EXHAUSTED"
LEGACY_ERROR = "The tool budget for this job is exhausted; complete a checkpoint and return needs_materials"


def reserve_call(workspace, job_id, token, name, arguments, limit):
    """Atomically count and claim a slot across all MCP connections for the job."""
    checkpoint_write = name == "memory_save" or (name == "artifact_put" and arguments.get("kind") == "checkpoint")
    with workspace.transaction() as db:
        count = db.execute("SELECT COUNT(*) FROM tool_calls WHERE job=?", (job_id,)).fetchone()[0]
        if count >= limit and (not checkpoint_write or count >= limit + CHECKPOINT_RESERVE):
            row = db.execute("SELECT payload FROM events WHERE job=? AND event='native_tool_budget_exhausted' ORDER BY seq DESC LIMIT 1", (job_id,)).fetchone()
            if not row or json.loads(row[0])["limit"] != limit:
                db.execute("INSERT INTO events(job,event,payload,created) VALUES(?,?,?,?)",
                           (job_id, "native_tool_budget_exhausted", dumps({"limit": limit, "used": count}), time.time()))
            return False
        db.execute("INSERT INTO tool_calls VALUES(?,?,?,?,?,?)", (token, job_id, name, dumps(arguments), None, "pending"))
        return True


def exhausted_limit(workspace, job):
    """Use current host events or corroborate an older native receipt and the exact host error."""
    summary = (job.get("output") or {}).get("summary", "")
    prior = job["state"].get("native_budget_continuation", {}).get("limit", 0)
    rows = workspace.query("SELECT payload FROM events WHERE job=? AND event='native_tool_budget_exhausted' ORDER BY seq DESC LIMIT 1", (job["id"],))
    if rows:
        limit = json.loads(rows[0]["payload"])["limit"]
        return limit if limit >= prior and summary.startswith(BUDGET_REASON) else None
    if prior or "tool budget" not in summary.lower():
        return None
    calls = workspace.query("SELECT response FROM calls WHERE job=? AND status='response' ORDER BY created DESC LIMIT 1", (job["id"],))
    if not calls:
        return None
    try:
        response = json.loads(calls[0]["response"])
        thread = response.get("response_id")
        if not thread or json.loads(response["text"]) != job["output"]:
            return None
    except (TypeError, ValueError, KeyError):
        return None
    group = hashlib.sha256(job["id"].encode()).hexdigest()[:20]
    for final in (workspace.root / "transport" / "codex" / group).glob("*/*/final.json"):
        attempt = final.parent
        try:
            receipt = json.loads((attempt / "receipt.json").read_text())
            metadata = json.loads((attempt / "transport-metadata.json").read_text())
            if (receipt.get("status") != "completed" or receipt.get("request_hash") != attempt.parent.name
                    or metadata.get("request_hash") != attempt.parent.name or metadata.get("job_id") != job["id"]
                    or json.loads(final.read_text()) != job["output"]):
                continue
            same_thread = False
            tool_denied = False
            with (attempt / "events.jsonl").open(encoding="utf-8") as stream:
                for line in stream:
                    try:
                        event = json.loads(line)
                    except ValueError:
                        continue
                    if event.get("type") == "thread.started" and event.get("thread_id") == thread:
                        same_thread = True
                    item = event.get("item", {})
                    if (event.get("type") == "item.completed" and item.get("type") == "mcp_tool_call"
                            and item.get("server") == "oracle_atlas" and item.get("status") == "completed"):
                        for part in (item.get("result") or {}).get("content", []):
                            if part.get("type") == "text" and part.get("text") in (dumps({"error": LEGACY_ERROR}), json.dumps({"error": LEGACY_ERROR})):
                                tool_denied = True
            if same_thread and tool_denied:
                count = workspace.query("SELECT COUNT(*) n FROM tool_calls WHERE job=?", (job["id"],))[0]["n"]
                if count >= 8:
                    return count
        except (ValueError, OSError):
            continue
    return None


def continue_native_budget(workspace, job, config):
    """Claim a single continuation with a raised ceiling; bind it to the saved handoff and draft IDs."""
    if config.get("backend") != "codex":
        return False
    limit = config["budgets"]["max_turns"] * 8
    old = exhausted_limit(workspace, job)
    if old is None:
        return False
    used = workspace.query("SELECT COUNT(*) n FROM tool_calls WHERE job=?", (job["id"],))[0]["n"]
    if limit <= max(old, used):
        return False
    drafts = workspace.query("SELECT id,kind,revision FROM drafts WHERE job=? ORDER BY id", (job["id"],))
    continuation = {"previous_limit": old, "limit": limit, "used": used, "drafts": drafts,
                    "previous_handoff": job["output"],
                    "instruction": "Resume this same job from its listed drafts and formal results. Inspect the latest draft's validation and remaining obligations first. Preserve the previously verified evidence, then finish the frozen research handoff or state concrete missing materials."}
    state = job["state"]
    with workspace.transaction() as db:
        row = db.execute("SELECT status,output FROM jobs WHERE id=?", (job["id"],)).fetchone()
        if row[0] != "needs_materials" or json.loads(row[1]) != job["output"]:
            return False
        state["native_budget_continuation"] = {"limit": limit, "used": used}
        state["history"].append({"role": "user", "content": dumps(continuation)})
        db.execute("INSERT INTO events(job,event,payload,created) VALUES(?,?,?,?)",
                   (job["id"], "native_budget_continued", dumps(continuation), time.time()))
        db.execute("UPDATE jobs SET status='running',state=?,updated=? WHERE id=?",
                   (dumps(state), time.time(), job["id"]))
    return True
