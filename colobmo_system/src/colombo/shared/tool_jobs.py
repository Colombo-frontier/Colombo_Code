"""Durable, idempotent long-tool jobs behind short MCP requests.

The whitelist below is deliberately not a general process execution interface.
Workers inherit the research budget and process tree; a transport wait is never
used as their research deadline. A lost worker is reported, never auto-replayed.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from colombo.shared.file_io import Path
from colombo.shared.file_io import atomic_write
from colombo.shared.runtime_budget import budget_environment
from colombo.shared.runtime_budget import file_lock
from colombo.shared.runtime_budget import inherited_deadline

from colombo.project_paths import PROJECT_ROOT
from colombo.project_paths import SOURCE_ROOT
PROJECT = Path(PROJECT_ROOT)
OPERATIONS = {"audit", "run_experiment", "resume_experiment", "challenge_argument",
              "resume_argument_challenge", "brain_audit", "budget_status"}
_PROCESS_HANDLES = {}


def _save(path, value):
    atomic_write(path,(json.dumps(value,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))


def _read(path):
    value=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value,dict): raise ValueError("Invalid tool job record")
    return value


def _settings(root):
    # Brain root has no run.json; its resolved frozen config lives in SQLite.
    if (Path(root)/"state.sqlite").exists():
        from colombo.brain.research_store import Store
        return Store(root).get_meta("config")["cell"]["settings"]
    from colombo.cell.settings import get_settings
    return get_settings(root)


def _identity(pid=None):
    from colombo.shared.process_control import process_identity
    return process_identity(pid)


def _alive(identity):
    from colombo.shared.process_control import process_matches
    return process_matches(identity)


def _folder(root, job_id):
    if not isinstance(job_id,str) or not re.fullmatch(r"job-[0-9a-f]{32}",job_id):
        raise ValueError("Invalid tool job ID")
    root=Path(root).resolve()
    base=root/"runtime"/"tool_jobs"
    if base.is_symlink() or not base.resolve().is_relative_to(root):
        raise ValueError("Tool jobs must stay inside the workspace")
    path=base/job_id
    if path.is_symlink() or not path.resolve().is_relative_to(base.resolve()):
        raise ValueError("Tool job must be an ordinary directory")
    return path


def _owner(payload):
    return str(payload.get("call_id") or os.getenv("CELL_PROCESS_ID") or "standalone")


def submit_or_poll(root, operation, payload, request_id=None):
    """Return a saved original result or a running receipt; never wait on a model."""
    if operation not in OPERATIONS or not isinstance(payload,dict):
        raise ValueError("Unknown tool job operation or invalid arguments")
    root=Path(root).resolve()
    settings=_settings(root)
    if request_id is not None and (not isinstance(request_id,str) or not request_id.strip()
            or len(request_id)>settings["limits"]["request_id_max_chars"]):
        raise ValueError("Invalid tool job request_id")
    # Explicit experiment/challenge IDs still retain their own stronger replay guards.
    owner=_owner(payload)
    canonical=json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False)
    identity=json.dumps([owner,operation,request_id if request_id is not None else canonical],ensure_ascii=False)
    job_id="job-"+hashlib.sha256(identity.encode()).hexdigest()[:32]
    folder=_folder(root,job_id)
    runtime=settings["runtime"]
    with file_lock(folder/"job.lock",runtime["task_lock_timeout_seconds"],runtime["lock_poll_seconds"]):
        request_path=folder/"request.json"
        if request_path.exists():
            saved=_read(request_path)
            if saved["operation"]!=operation or saved["payload"]!=payload:
                raise ValueError("Tool job request_id replay changed its inputs")
        else:
            inherited_deadline(root)  # Refuse new work once its inherited budget is gone.
            request={"version":1,"job_id":job_id,"root":str(root),"owner":owner,
                     "operation":operation,"payload":payload,"request_id":request_id,
                     "created_at":time.time()}
            _save(request_path,request)
            _save(folder/"state.json",{"status":"starting","job_id":job_id,"owner":owner,
                                       "created_at":time.time(),"identity":None,
                                       "launcher_identity":_identity()})
            env=dict(os.environ)
            env.update(budget_environment(root))
            env["PYTHONUTF8"]="1"
            paths=[str(SOURCE_ROOT)]
            if env.get("PYTHONPATH"): paths.append(env["PYTHONPATH"])
            env["PYTHONPATH"]=os.pathsep.join(paths)
            command=[sys.executable,"-B","-m","colombo.shared.tool_jobs","--request",str(request_path)]
            try:
                with (folder/"worker.log").open("ab") as log:
                    process=subprocess.Popen(command,cwd=str(PROJECT),env=env,stdin=subprocess.DEVNULL,
                        stdout=log,stderr=subprocess.STDOUT,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name=="nt" else 0)
                _PROCESS_HANDLES[job_id]=process
                _save(folder/"state.json",{"status":"running","job_id":job_id,"owner":owner,
                    "created_at":request["created_at"],"identity":_identity(process.pid),
                    "launcher_identity":_identity()})
            except Exception as exc:
                _save(folder/"result.json",{"ok":False,"job_id":job_id,"status":"error",
                     "error":{"type":type(exc).__name__,"message":str(exc)},"retryable":False})
                raise
    return poll_job(root,job_id)


def poll_job(root,job_id,owner=None):
    folder=_folder(root,job_id)
    if not (folder/"request.json").is_file(): raise ValueError("Unknown tool job")
    if owner is not None and _read(folder/"request.json").get("owner") != owner:
        raise ValueError("Tool job belongs to a different invocation")
    handle=_PROCESS_HANDLES.get(job_id)
    observed_exit = handle.poll() if handle is not None else None
    if observed_exit is not None:
        _PROCESS_HANDLES.pop(job_id,None)
    if (folder/"result.json").is_file():
        saved=_read(folder/"result.json")
        return saved["result"] if saved.get("ok") else saved
    state=_read(folder/"state.json")
    identity=state.get("identity") or state.get("launcher_identity")
    if observed_exit is not None or identity and _alive(identity) is False:
        # The worker may publish its receipt and exit after the first read.
        # A committed success/error remains authoritative over a liveness check.
        if (folder/"result.json").is_file():
            saved=_read(folder/"result.json")
            return saved["result"] if saved.get("ok") else saved
        receipt={"ok":False,"status":"interrupted","job_id":job_id,
                "error":{"type":"WorkerInterrupted","message":"Worker exited without a final receipt; saved records remain. No automatic re-execution."},
                "retryable":False}
        _save(folder/"result.json",receipt)
        return receipt
    return {"status":"running","job_id":job_id,"owner":state["owner"],
            "message":"Research continues within the inherited budget. Use job_status(job_id) to retrieve the original result; do not resubmit a new job."}


def pending_jobs(root,owner=None):
    pending=[]
    for path in sorted((Path(root)/"runtime"/"tool_jobs").glob("job-*/state.json")):
        state=_read(path)
        if owner is not None and state.get("owner")!=owner: continue
        result=poll_job(root,path.parent.name)
        if result.get("status")=="running" and result.get("job_id")==path.parent.name:
            pending.append(result)
    return pending



def experiment_context(root):
    """Bind a dispatched experiment to the caller's fixed Cell workspace."""
    from colombo.cell.record_store import Store
    from colombo.cell.settings import get_settings, managed_settings
    from colombo.cell.recovery import caller_deadline
    from colombo.shared.experiment_execution import ExperimentContext
    root = Path(root)
    resolver = None

    def resolve_refs(refs):
        # Initial input validation precedes opening research storage. Reuse the
        # same reader for the target and optional attempt, as the Cell did.
        nonlocal resolver
        if resolver is None:
            resolver = Store(root / "memory")
        return resolver.resolve_record_refs(refs)

    def write_result(experiment_id, payload):
        # Each durable checkpoint reopens the Store, retaining its original
        # settings/context refresh and recovery boundary.
        return Store(root / "memory").write_experiment_result(experiment_id, payload)

    return ExperimentContext(
        read_settings=lambda: get_settings(root),
        resolve_refs=resolve_refs,
        write_result=write_result,
        restore_settings=lambda snapshot: managed_settings(root, snapshot, partial=True),
        deadline=lambda phase: caller_deadline(root, phase=phase),
    )

def _execute(request):
    root=Path(request["root"])
    payload=dict(request["payload"])
    op=request["operation"]
    if op=="brain_audit":
        from colombo.brain.mcp_server import AgentService
        call_id=payload.pop("call_id")
        role=payload.pop("role","brain")
        stage=payload.pop("stage")
        return AgentService(root,role,stage,call_id).audit(**payload)
    if op=="audit":
        from colombo.cell.verifier.local_audit import audit
        return audit(root,**payload)
    if op in {"run_experiment","resume_experiment"}:
        import colombo.shared.experiment_execution as experiment
        return getattr(experiment,op)(root, context=experiment_context(root), **payload)
    if op in {"challenge_argument","resume_argument_challenge"}:
        import colombo.cell.verifier.challenge as challenge
        return getattr(challenge,op)(root,**payload)
    if op=="budget_status":
        from colombo.shared.runtime_budget import get_budget_context
        return {"budget":get_budget_context(root)}
    raise ValueError("Unknown worker operation")


def run_worker(request_path):
    request_path=Path(request_path).resolve()
    request=_read(request_path)
    folder=_folder(request["root"],request["job_id"])
    if folder.resolve()!=request_path.parent or request["operation"] not in OPERATIONS:
        raise ValueError("Tool worker request identity mismatch")
    runtime=_settings(request["root"])["runtime"]
    # Wait for the launcher's identity commit; no race with a fast result.
    with file_lock(folder/"job.lock",runtime["task_lock_timeout_seconds"],runtime["lock_poll_seconds"]):
        state=_read(folder/"state.json")
        if (folder/"result.json").exists(): return
        state.update(status="running",identity=_identity(),started_at=time.time())
        _save(folder/"state.json",state)
    try:
        inherited_deadline(request["root"])
        result=_execute(request)
        receipt={"ok":True,"job_id":request["job_id"],"result":result}
    except Exception as exc:
        receipt={"ok":False,"status":"error","job_id":request["job_id"],
                 "error":{"type":type(exc).__name__,"message":str(exc)},"retryable":False}
    _save(folder/"result.json",receipt)
    state.update(status="completed" if receipt["ok"] else "error",ended_at=time.time())
    _save(folder/"state.json",state)


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--request",required=True)
    run_worker(parser.parse_args().request)
