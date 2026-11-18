"""Public bounded-scheduler metadata, without model or source content."""
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
from pathlib import Path
import time


def record_scheduler_event(workspace, run_id, event, *, setting_id=None, position=None, attempt=None, workers=1):
    if event not in {"batch_started", "item_started", "item_finished", "batch_finished"}:
        raise ValueError("Unknown scheduler event")
    path = Path(workspace) / "runs" / run_id / "scheduler.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {"event": event, "at": datetime.now(timezone.utc).isoformat(), "monotonic_ns": time.monotonic_ns(),
           "workers": workers, "setting_id": setting_id, "position": position, "attempt": attempt}
    with path.with_suffix(".lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            with path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
                stream.flush()
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)
