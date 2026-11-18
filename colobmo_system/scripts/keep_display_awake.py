"""Keep the display awake only while an exact existing controller is running.

Modern Standby on battery expires system-only requests after five minutes.
This companion additionally holds a display request without changing the power
plan. It does not prevent user-initiated sleep or a closed-lid sleep action.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resume_background import ES_CONTINUOUS, ES_SYSTEM_REQUIRED, identity_or_error, set_execution_state, utc_now
from colombo.shared.file_io import json_bytes, write_json
from colombo.shared.process_control import process_matches

ES_DISPLAY_REQUIRED = 0x00000002


def target_identities(path):
    saved = json.loads(Path(path).read_text(encoding="utf-8"))
    if saved.get("status") != "running":
        raise ValueError("Supervisor must already be running")
    identities = {name: saved[name]["identity"] for name in ("supervisor", "controller")}
    for identity in identities.values():
        if (not isinstance(identity, dict) or type(identity.get("pid")) is not int
                or identity["pid"] < 1 or not identity.get("start_token")):
            raise ValueError("Both targets require exact process identities")
    return identities


def watch(supervisor_path, status_path):
    supervisor_path, status_path = Path(supervisor_path).resolve(), Path(status_path).resolve()
    identities = target_identities(supervisor_path)
    state = {"status": "starting", "started_at": utc_now(), "supervisor_file": str(supervisor_path),
             "targets": identities, "pid": os.getpid(), **identity_or_error(os.getpid()),
             "display_request_active": False}
    status_path.parent.mkdir(parents=True, exist_ok=True)
    with status_path.open("xb") as stream:
        stream.write(json_bytes(state))
    acquired = False
    try:
        while True:
            matches = {name: process_matches(identity) for name, identity in identities.items()}
            if any(value is not True for value in matches.values()):
                state.update(status="exited", reason="target_exited_or_identity_unconfirmed", target_matches=matches)
                break
            try:
                current_identities = target_identities(supervisor_path)
            except ValueError:
                state.update(status="exited", reason="supervisor_no_longer_running")
                break
            if current_identities != identities:
                state.update(status="exited", reason="target_identity_changed")
                break
            if not acquired:
                set_execution_state(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
                acquired = True
            state.update(status="running", display_request_active=True, checked_at=utc_now())
            write_json(status_path, state)
            time.sleep(10)
    except BaseException as exc:
        state.update(status="interrupted" if isinstance(exc, KeyboardInterrupt) else "failed",
                     error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        try:
            if acquired:
                set_execution_state(ES_CONTINUOUS)
        finally:
            state.update(display_request_active=False, ended_at=utc_now())
            write_json(status_path, state)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--supervisor", required=True, type=Path)
    parser.add_argument("--status-file", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        watch(args.supervisor, args.status_file)
        return 0
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
