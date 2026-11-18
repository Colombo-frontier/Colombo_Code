"""Process identities, owned process trees and fixed stop receipts."""
from __future__ import annotations
import ctypes
import os
import signal
import subprocess
import time
from colombo.shared.file_io import Path, io_path, atomic_write, freeze_json, read_json, json_equal

def execution_scope(value) -> dict:
    """The exact task assignment and invocation named by an external effect."""
    keys = ("task_id", "attempt_id", "assignment_ref", "package_ref")
    if not isinstance(value, dict) or any(key not in value for key in keys):
        raise ValueError("Incomplete execution scope")
    scope = {key: value[key] for key in keys}
    for key in ("task_id", "attempt_id"):
        if not isinstance(scope[key], str) or not scope[key].strip():
            raise ValueError(f"Execution scope requires {key}")
    for key in ("assignment_ref", "package_ref"):
        ref = scope[key]
        if not isinstance(ref, dict) or not isinstance(ref.get("id"), str) or not ref["id"]:
            raise ValueError(f"Execution scope requires {key}")
    return scope


def load_stop_request(folder, request):
    """Read a durable stop intent bound to this exact Cell attempt and scope."""
    folder = Path(folder)
    path = folder / "stop_request.json"
    if not path.exists():
        return None
    stop = read_json(path)
    expected = execution_scope(request)
    if (type(stop.get("schema_version")) is not int or stop["schema_version"] != 2
            or not json_equal(execution_scope(stop), expected)):
        raise ValueError("Stop request does not match this task, attempt and frozen scope")
    if not isinstance(stop.get("request_id"), str) or not stop["request_id"].strip():
        raise ValueError("Stop request needs a durable request ID")
    decision = stop.get("decision_ref")
    if not ((isinstance(decision, str) and decision.strip()) or
            (isinstance(decision, dict) and isinstance(decision.get("id"), str) and decision["id"].strip())):
        raise ValueError("Stop request needs its reviewed decision reference")
    return stop


def complete_stop_request(folder, stop, result_path, result):
    """Freeze the outcome of a stop after a stable result exists; first result wins."""
    folder, result_path = Path(folder), Path(result_path)
    status = "cancelled" if result["execution_status"] == "cancelled" else "already_completed"
    if not json_equal(execution_scope(result), execution_scope(stop)):
        raise ValueError("Stopped result belongs to another task or attempt")
    if status == "cancelled" and not json_equal(result.get("stop_request"), stop):
        raise ValueError("Cancelled result is not bound to its stop request")
    receipt = {**execution_scope(stop), "request_id": stop["request_id"],
               "decision_ref": stop["decision_ref"], "status": status,
               "result_path": result_path.relative_to(folder.parent.parent).as_posix()}
    freeze_json(folder / "stop_receipt.json", receipt)
    return receipt


def process_identity(pid: int | None = None) -> dict | None:
    """PID plus OS creation identity; None means known absent, never just PID reuse."""
    pid = os.getpid() if pid is None else int(pid)
    if os.name == "nt":
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
        kernel.GetProcessTimes.restype = wintypes.BOOL
        kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            error = ctypes.get_last_error()
            if error in (87, 1168):
                return None
            raise OSError(error, "Cannot inspect process identity")
        try:
            exit_code = wintypes.DWORD()
            if not kernel.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                raise ctypes.WinError(ctypes.get_last_error())
            if exit_code.value != 259:
                return None
            times = [wintypes.FILETIME() for _ in range(4)]
            if not kernel.GetProcessTimes(handle, *(ctypes.byref(t) for t in times)):
                raise ctypes.WinError(ctypes.get_last_error())
            created = (times[0].dwHighDateTime << 32) | times[0].dwLowDateTime
            return {"pid": pid, "start_token": str(created), "platform": "windows"}
        finally:
            kernel.CloseHandle(handle)
    proc = Path(f"/proc/{pid}/stat")
    if proc.exists():
        try:
            fields = proc.read_text().rsplit(")", 1)[1].split()
            if fields[0] == "Z":
                return None
            boot = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
            return {"pid": pid, "start_token": boot + ":" + fields[19], "platform": "linux"}
        except FileNotFoundError:
            return None
    # macOS fallback: kernel-backed process start timestamp, not a plain liveness check.
    check = subprocess.run(["ps", "-p", str(pid), "-o", "lstart="], capture_output=True,
                           text=True, timeout=5)
    stamp = check.stdout.strip()
    return {"pid": pid, "start_token": stamp, "platform": "posix"} if stamp else None


def process_matches(identity: dict) -> bool | None:
    try:
        current = process_identity(identity["pid"])
        return current is not None and current == identity
    except (OSError, ValueError, KeyError, subprocess.SubprocessError):
        return None


def spawn_options() -> dict:
    return ({"creationflags": subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP}
            if os.name == "nt" else {"start_new_session": True})


def managed_popen(command: list[str], *, terminate_wait_seconds: float = 5, **kwargs) -> subprocess.Popen:
    """On Windows, attach a suspended solver to a kill-on-close job before it can fork."""
    if os.name != "nt":
        return subprocess.Popen(command, **kwargs, **spawn_options())
    from ctypes import wintypes
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    class BasicLimits(ctypes.Structure):
        _fields_ = [("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
                    ("flags", wintypes.DWORD), ("minimum", ctypes.c_size_t),
                    ("maximum", ctypes.c_size_t), ("active", wintypes.DWORD),
                    ("affinity", ctypes.c_size_t), ("priority", wintypes.DWORD),
                    ("scheduling", wintypes.DWORD)]
    class IOCounters(ctypes.Structure):
        _fields_ = [(name, ctypes.c_ulonglong) for name in
                    ("read_ops", "write_ops", "other_ops", "read_bytes", "write_bytes", "other_bytes")]
    class ExtendedLimits(ctypes.Structure):
        _fields_ = [("basic", BasicLimits), ("io", IOCounters),
                    ("process_memory", ctypes.c_size_t), ("job_memory", ctypes.c_size_t),
                    ("peak_process", ctypes.c_size_t), ("peak_job", ctypes.c_size_t)]
    kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel.CreateJobObjectW.restype = wintypes.HANDLE
    kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    job = kernel.CreateJobObjectW(None, None)
    if not job:
        raise ctypes.WinError(ctypes.get_last_error())
    limits = ExtendedLimits()
    limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    process = None
    try:
        if not kernel.SetInformationJobObject(job, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            raise ctypes.WinError(ctypes.get_last_error())
        options = spawn_options()
        options["creationflags"] |= 0x00000004  # CREATE_SUSPENDED
        process = subprocess.Popen(command, **kwargs, **options)
        if not kernel.AssignProcessToJobObject(job, wintypes.HANDLE(int(process._handle))):
            raise ctypes.WinError(ctypes.get_last_error())
        ntdll = ctypes.WinDLL("ntdll")
        ntdll.NtResumeProcess.argtypes = [wintypes.HANDLE]
        ntdll.NtResumeProcess.restype = ctypes.c_long
        status = ntdll.NtResumeProcess(wintypes.HANDLE(int(process._handle)))
        if status != 0:
            raise OSError(f"NtResumeProcess failed: {status}")
        process._colombo_job = job
        return process
    except BaseException:
        if process is not None:
            process.kill()
            process.wait(timeout=terminate_wait_seconds)
        kernel.CloseHandle(job)
        raise


def close_process_job(process: subprocess.Popen) -> None:
    job = getattr(process, "_colombo_job", None)
    if job is not None:
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle(job)
        process._colombo_job = None


def terminate_tree(process: subprocess.Popen, timeout: float = 10, poll_seconds: float = 0.05) -> bool:
    job = getattr(process, "_colombo_job", None)
    if job is not None:
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        kernel.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p,
                                                     wintypes.DWORD, ctypes.c_void_p]
        class Accounting(ctypes.Structure):
            _fields_ = [("user_time", ctypes.c_longlong), ("kernel_time", ctypes.c_longlong),
                        ("period_user", ctypes.c_longlong), ("period_kernel", ctypes.c_longlong),
                        ("page_faults", wintypes.DWORD), ("total", wintypes.DWORD),
                        ("active", wintypes.DWORD), ("terminated", wintypes.DWORD)]
        if not kernel.TerminateJobObject(job, 1):
            return False
        try:
            process.wait(timeout=timeout)
            deadline = time.monotonic() + timeout
            while True:
                accounting = Accounting()
                if not kernel.QueryInformationJobObject(job, 1, ctypes.byref(accounting),
                                                       ctypes.sizeof(accounting), None):
                    return False
                if accounting.active == 0:
                    break
                if time.monotonic() >= deadline:
                    return False
                time.sleep(poll_seconds)
            close_process_job(process)
            return True
        except subprocess.TimeoutExpired:
            return False
    if process.poll() is not None:
        return True
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                           capture_output=True, timeout=timeout,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        except (OSError, subprocess.TimeoutExpired):
            return False
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            return True
    try:
        process.wait(timeout=timeout)
        return True
    except subprocess.TimeoutExpired:
        if os.name != "nt":
            try:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=timeout)
                return True
            except (ProcessLookupError, subprocess.TimeoutExpired):
                pass
        return False
