"""Compact read-only status for a running validation; no CLI/model is invoked."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3


def status(root):
    root = root.resolve()
    db = sqlite3.connect((root / "state.sqlite").as_uri() + "?mode=ro", uri=True, timeout=10)
    try:
        db.execute("BEGIN")
        meta = {key: json.loads(value) for key, value in db.execute("SELECT key,value FROM meta")}
        research = json.loads(db.execute("SELECT payload FROM documents WHERE name='research'").fetchone()[0])
        recent = [{"name": name, "time": at, "payload": json.loads(payload)} for name, at, payload in
                  db.execute("SELECT name,created_at,payload FROM events ORDER BY sequence DESC LIMIT 5")]
    finally:
        db.close()
    pending = meta.get("pending_call") or {}
    calls = []
    for path in sorted(root.glob("brain/calls/*/call.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        calls.append({key: value.get(key) for key in
                      ("call_id", "role", "stage", "status", "started_at", "ended_at", "returncode")})
    tasks = []
    for tid, task in research.get("tasks", {}).items():
        runtime = task.get("runtime", {})
        tasks.append({"task_id": tid, **{key: runtime.get(key) for key in
                     ("state", "active_attempt", "execution_status", "accepted", "review_status")}})
    return {"checked_at": datetime.now(timezone.utc).isoformat(), "run_dir": str(root),
            "state": {key: meta.get(key) for key in
                ("phase", "status", "round_no", "model_call_count", "dispatch_count", "stop_reason")},
            "pending_call": {key: pending.get(key) for key in ("call_id", "role", "stage", "status")},
            "tasks": tasks, "calls": calls, "recent_events": recent}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(status(args.run_dir), ensure_ascii=False, indent=2))
