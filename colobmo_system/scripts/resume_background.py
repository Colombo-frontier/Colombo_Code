"""Resume a run while a Windows supervisor prevents automatic idle sleep.

Start this script itself with Start-Process -WindowStyle Hidden. It remains alive
until the controller exits; closing the monitoring chat does not stop it. The
power request belongs only to this thread and is released on exit. Use
--keep-display-awake on battery-powered Modern Standby systems; system-only
requests can expire after five minutes. Neither mode changes power settings or
prevents explicit user sleep.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import ctypes
from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
import sys
import time


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from colombo.shared.file_io import json_bytes, write_json
from colombo.shared.process_control import process_identity, terminate_tree


ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def set_execution_state(flags):
    if os.name != "nt":
        raise RuntimeError("This supervisor requires Windows")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.SetThreadExecutionState.argtypes = [ctypes.c_uint32]
    kernel.SetThreadExecutionState.restype = ctypes.c_uint32
    if not kernel.SetThreadExecutionState(flags):
        raise ctypes.WinError(ctypes.get_last_error())


@contextmanager
def keep_system_awake(*, keep_display=False):
    flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    if keep_display:
        flags |= ES_DISPLAY_REQUIRED
    set_execution_state(flags)
    try:
        yield
    finally:
        set_execution_state(ES_CONTINUOUS)


def identity_or_error(pid):
    try:
        return {"identity": process_identity(pid)}
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return {"identity": None, "identity_error": type(exc).__name__}


def supervise(run_dir, log_dir, *, keep_display_awake=False):
    run_dir, log_dir = Path(run_dir).resolve(), Path(log_dir).resolve()
    if not (run_dir / "state.sqlite").is_file():
        raise ValueError("Existing run state.sqlite is required")
    log_dir.mkdir(parents=True, exist_ok=True)
    stdout_path, stderr_path = log_dir / "controller.stdout.log", log_dir / "controller.stderr.log"
    status_path = log_dir / "supervisor.json"
    if any(path.exists() for path in (stdout_path, stderr_path, status_path)):
        raise FileExistsError("Use a fresh log directory; existing launch records are preserved")
    command = [sys.executable, "-B", str(PROJECT / "run.py"), "resume", "--run-dir", str(run_dir)]
    started = time.monotonic()
    state = {"schema_version": 1, "status": "starting", "started_at": utc_now(),
             "run_dir": str(run_dir), "command": command,
             "supervisor": {"pid": os.getpid(), **identity_or_error(os.getpid())},
             "controller": None, "stdout": str(stdout_path), "stderr": str(stderr_path),
             "keep_awake_active": False, "keep_display_awake": keep_display_awake, "returncode": None}
    # Claim this launch record atomically so two invocations cannot overwrite it.
    with status_path.open("xb") as stream:
        stream.write(json_bytes(state))
        stream.flush()
        os.fsync(stream.fileno())
    process = None
    try:
        with keep_system_awake(keep_display=keep_display_awake):
            state["keep_awake_active"] = True
            write_json(status_path, state)
            with stdout_path.open("x", encoding="utf-8") as stdout, stderr_path.open("x", encoding="utf-8") as stderr:
                # This supervisor must survive the launching chat. In particular,
                # do not attach it or the controller to a kill-on-close job here.
                options = {"creationflags": subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {}
                process = subprocess.Popen(command, cwd=str(PROJECT), stdin=subprocess.DEVNULL,
                                           stdout=stdout, stderr=stderr, **options)
                state.update(status="running", controller={"pid": process.pid, **identity_or_error(process.pid)},
                             controller_started_at=utc_now())
                while True:
                    state["checked_at"] = utc_now()
                    write_json(status_path, state)
                    try:
                        code = process.wait(timeout=30)
                        break
                    except subprocess.TimeoutExpired:
                        continue
                state.update(status="exited", returncode=code, controller_ended_at=utc_now())
    except BaseException as exc:
        state.update(status="interrupted" if isinstance(exc, KeyboardInterrupt) else "failed",
                     error_type=type(exc).__name__, error=str(exc))
        if process is not None and process.poll() is None:
            state["controller_tree_terminated"] = terminate_tree(process)
        raise
    finally:
        state.update(keep_awake_active=False, ended_at=utc_now(), elapsed_seconds=round(time.monotonic() - started, 3))
        if process is not None:
            state["returncode"] = process.poll()
        write_json(status_path, state)
    return code


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--log-dir", required=True, type=Path)
    parser.add_argument("--keep-display-awake", action="store_true",
                        help="Keep the display on as well; needed for sustained execution on battery with Modern Standby")
    args = parser.parse_args(argv)
    try:
        return supervise(args.run_dir, args.log_dir, keep_display_awake=args.keep_display_awake)
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
