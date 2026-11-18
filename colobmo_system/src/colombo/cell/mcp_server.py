"""Research MCP tools: records, local audits, sources and parallel tasks."""
from __future__ import annotations

import os
from pathlib import Path as _BootstrapPath
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[2]))
from colombo.shared.file_io import Path
from mcp.server.fastmcp import FastMCP
from pydantic import StrictInt
from colombo.cell.record_store import Store
from colombo.cell.record_formats import ArchivePayload
from colombo.cell.record_formats import ArchiveOperations
from colombo.cell.record_formats import archive_input_schema
from colombo.cell.verifier.local_audit import audit as run_audit
from colombo.cell.settings import configure as configure_task
from colombo.cell.settings import normalize_role
from colombo.cell.recovery import budget_status as read_budget
from colombo.cell.recovery import finish_handoff as save_handoff
from colombo.shared.tool_jobs import submit_or_poll
from colombo.shared.tool_jobs import poll_job

RUN = Path(os.environ.get("CELL_RUN_DIR", ".")).resolve()
ROLE = normalize_role(os.environ.get("CELL_ROLE", "prover"))
if ROLE not in {"prover", "subcell"}:
    raise ValueError("Prover MCP only supports prover and subcell roles")
class ResearchMCP(FastMCP):
    async def list_tools(self):
        tools = await super().list_tools()
        for tool in tools:
            if tool.name == "archive":
                tool.inputSchema = archive_input_schema(tool.inputSchema)
        return tools


mcp = ResearchMCP("research")

# Verifier has a separate server and deliberately receives no live LTM reader.
from colombo.cell.instructions import read_cell_mode
from colombo.memory.integration import register_builtin_memory
register_builtin_memory(mcp, research_mode=read_cell_mode(RUN)["research_mode"])


def _store():
    return Store(RUN / "memory")


def _detail(value: str) -> None:
    if value not in {"summary", "full"}:
        raise ValueError("detail must be summary or full")


def _receipt(record: dict) -> dict:
    """Return identity and trust state without echoing mathematical content."""
    receipt = {key: record[key] for key in ("kind", "id", "revision")}
    payload = record["payload"]
    if "current_trust" in record:
        receipt["current_trust"] = record["current_trust"]
    for key in ("status", "tag", "audit_id", "challenged_by"):
        if key in payload:
            receipt[key] = payload[key]
    if record["kind"] == "examples":
        receipt["properties"] = [
            {key: prop[key] for key in ("id", "status", "audit_id", "challenged_by") if key in prop}
            for prop in payload.get("properties", [])
        ]
    return receipt


def lookup(query: str = "", url: str = "", limit: StrictInt | None = None) -> dict:
    """Search sources (Serper by default) or read one URL (Jina Reader by default).
    Provider choice comes from the central configuration; no API keys in tool arguments.
    limit controls search result count only; omission uses the central configuration.
    Preserve provenance; abstracts are not theorems.
    If this task has search disabled, returns search_disabled without making a request.
    Use configure(search_enabled=True, reason=...) to enable lookup for this task.
    """
    from colombo.shared.literature_access import lookup as search
    return search(query=query, url=url, limit=limit)


@mcp.tool()
def archive(kind: str, payload: ArchivePayload, record_id: str | None = None,
            expected_revision: int | None = None, request_id: str | None = None,
            detail: str = "summary") -> dict:
    """Save an immutable record revision. Kinds: claims/arguments/examples/attempts/sources/proof_state/experiment_result.
    Revision updates require expected_revision. proved arguments and checked example properties
    require a matching audit_id. Reviews/events are service-owned. Dependencies use {kind,id,revision}.
    Argument conclusions are [{target:{kind,id,revision},relation:"supports"|"refutes"}];
    put the derivation in content/body, not inside conclusions.
    experiment_result is created by run_experiment; archive edits only its observations,
    limitations and derived_refs (a partial payload is allowed), never execution facts.
    Returns a compact receipt; use retrieve for the saved body or detail='full' for its envelope.
    """
    _detail(detail)
    record = _store().archive(kind, payload, record_id, expected_revision, request_id)
    return record if detail == "full" else _receipt(record)

@mcp.tool()
def archive_result(records: ArchiveOperations, request_id: str, detail: str = "summary") -> dict:
    """Save related research records in one recoverable transaction.
    Each item has local_key and op=create/update/reference. create/update use kind,
    payload, optional record_id; update also requires expected_revision. reference
    uses ref. Payload references may use {local_key:...}, with optional property_ids.
    Argument conclusions contain only target and relation (supports/refutes).
    Mathematical Claim/construction changes require new IDs. No trust is granted.
    Reuse request_id only for identical inputs. Returns local_key to fixed-ref mapping.
    """
    _detail(detail)
    result = _store().archive_result(records, request_id)
    return result if detail == "full" else {**result, "records": [_receipt(r) for r in result["records"]]}

@mcp.tool()
def retrieve(query: str = "", kinds: list[str] | None = None,
             record_id: str | None = None, revision: int | None = None, limit: int | None = None,
             include_context: bool | None = None, target_ref: dict | None = None,
             relations: list[str] | None = None, route_id: str | None = None,
             state_filter: dict | None = None, since_event: dict | None = None,
             cursor: dict | None = None, detail: str = "full") -> dict:
    """Read fixed records or scoped research views, with fresh evidence state.
    target_ref pins a record; relations selects supports/refutes/attempts/subjects/uses.
    route_id selects obligations; state_filter requires domain and value (or a list).
    since_event uses {scope:current_workspace,stream:memory,sequence:N}; it reports
    direct memory events, not complete downstream trust propagation. Reuse all filters
    with cursor; page_cursor retries the current page. detail=summary limits excerpts.
    Legacy keyword/ID calls return complete records. Omitted limits use configuration.
    """
    return _store().retrieve(query, kinds, record_id, revision, limit, include_context,
                             target_ref=target_ref, relations=relations, route_id=route_id,
                             state_filter=state_filter, since_event=since_event, cursor=cursor, detail=detail)

@mcp.tool()
def run_experiment(question: str, target_ref: dict, code: str, request_id: str,
                   parameters: dict | None = None, input_files: list[str] | None = None,
                   attempt_ref: dict | None = None) -> dict:
    """Run a bounded Python experiment in an OpenAI-hosted container and save actual evidence.
    target_ref and optional attempt_ref require kind, id, revision.
    input_files are explicit task-relative files. The service saves the supplied code itself.
    Reuse request_id only with identical inputs to recover the same execution, never to rerun it.
    Execution success does not mark a mathematical claim proved or an example checked.
    """
    return submit_or_poll(RUN, "run_experiment", dict(question=question, target_ref=target_ref,
        code=code, request_id=request_id, parameters=parameters, input_files=input_files,
        attempt_ref=attempt_ref), request_id=request_id)

@mcp.tool()
def resume_experiment(experiment_id: str) -> dict:
    """Recover the original remote execution or download its evidence without a new paid request.
    Resuming preserves the original execution deadline and cumulative run count.
    """
    return submit_or_poll(RUN, "resume_experiment", {"experiment_id": experiment_id})

@mcp.tool()
def challenge_argument(record_ref: dict, reason: str, evidence_refs: list[dict] | None = None,
                       request_id: str | None = None) -> dict:
    """Use when research raises a concrete concern about an already certified argument.
    This is an optional channel, not a routine audit of previously certified records.
    Supply its fixed kind/id/revision and the specific concern; a confirmed error
    is not required to open the review.
    The service suspends this evidence while checking the objection; a second independent
    process must confirm an error before certification is withdrawn. History remains intact.
    Repeating the same request resumes its original frozen review, without resetting counters.
    A pending result is not an instruction to repair and does not assert the statement is false.
    """
    return submit_or_poll(RUN, "challenge_argument", dict(record_ref=record_ref, reason=reason,
        evidence_refs=evidence_refs, request_id=request_id), request_id=request_id)

@mcp.tool()
def resume_argument_challenge(challenge_id: str) -> dict:
    """Continue an unfinished local challenge at its saved stage, preserving input and spent attempts.
    Returns the current status, trust effects and report references; disagreement stays internal.
    """
    return submit_or_poll(RUN, "resume_argument_challenge", {"challenge_id": challenge_id})


@mcp.tool()
def job_status(job_id: str) -> dict:
    """Retrieve the original result of a running audit, challenge or Experiment job.
    A running receipt is not a mathematical verdict. Poll the same job_id until
    it returns its saved result; do not launch replacement jobs while it runs.
    """
    return poll_job(RUN, job_id)

@mcp.tool()
def audit(kind: str, record_id: str, revision: int, property_ids: list[str] | None = None,
          detail: str = "summary") -> dict:
    """Launch a fresh lightweight correctness reviewer. Archive a candidate first, then pass its
    exact ID/version. A pass promotes that argument to proved or selected example properties
    to checked. Failure/uncertainty/service errors are retained without promotion.
    An adverse re-audit of a certified argument enters the local challenge workflow;
    withdrawal requires independent confirmation and affects the referenced old evidence.
    Ordinary audits return the review and a record receipt. Certified adverse re-audits
    return the original review_ref and challenge receipt; its final report is authoritative
    only after resolution. detail='full' also includes the complete record.
    Experiment artifact inventories remain in the stored review; summary returns their count.
    """
    _detail(detail)
    result = submit_or_poll(RUN, "audit", dict(kind=kind, record_id=record_id,
                            revision=revision, property_ids=property_ids))
    if detail == "summary" and result.get("record") is not None:
        result = {**result, "record": _receipt(result["record"])}
    if detail == "summary" and "experiment_artifacts" in result.get("review", {}).get("payload", {}):
        payload = dict(result["review"]["payload"])
        payload["experiment_artifact_count"] = len(payload.pop("experiment_artifacts"))
        result = {**result, "review": {**result["review"], "payload": payload, "detail": "summary"}}
    return result

mcp.tool()(lookup)

@mcp.tool()
def configure(settings_overrides: dict | None = None, search_enabled: bool | None = None,
              reason: str = "", detail: str = "summary") -> dict:
    """Inspect or update non-budget task behavior; budgets belong to outer config.toml.
    Omit arguments to inspect. Updates require a reason. settings_overrides is a nested
    partial settings table. lookup changes apply on its next call; native web search,
    model and launch-time settings require a new model process, not an automatic restart.
    Returns search state, changes, effective timing and pending startup changes.
    detail='full' also returns desired_settings and launch_settings. Sibling tasks are unaffected.
    """
    _detail(detail)
    result = configure_task(RUN, ROLE, settings_overrides, search_enabled, reason)
    if detail == "full":
        return result
    return {key: value for key, value in result.items()
            if key not in {"desired_settings", "launch_settings", "notes"}}

def _tasks():
    from colombo.cell.subcell_dispatch import Tasks
    return Tasks(RUN)


@mcp.tool()
def budget_status() -> dict:
    """Read time remaining and whether handoff is due. Unlimited mode returns
    time_limit_enabled=false, null deadlines/remaining times, and closing=false.
    """
    return read_budget(RUN)


@mcp.tool()
def finish_handoff(summary: str, pending: list[str], next_steps: list[str],
                   references: list[str] | None = None, stopping_reason: str = "budget") -> dict:
    """Save progress for the next prover/subcell, then end this process cooperatively.
    Follow the shared handoff skill. Include evidence paths; this is not a proof verdict.
    """
    return save_handoff(RUN, summary, pending, next_steps, references, stopping_reason)

@mcp.tool()
def spawn_task(target_ref: dict, instructions: str, context_refs: list[dict] | None = None,
               group_id: str = "", search_enabled: bool | None = None,
               settings_overrides: dict | None = None) -> dict:
    """Start a subcell with a pinned target and selected context snapshots.
    Optional search_enabled and non-budget settings_overrides apply only to this child.
    Time, count, concurrency and resource limits always inherit the root policy.
    Omitted search uses the subcell role default, not the parent's current search override.
    """
    return _tasks().spawn_task(target_ref, instructions, context_refs, group_id,
                              search_enabled=search_enabled, settings_overrides=settings_overrides)

@mcp.tool()
def task_status(task_id: str | None = None) -> dict:
    """Inspect child task states. No implicit acceptance or pruning."""
    return _tasks().task_status(task_id)

@mcp.tool()
def cancel_task(task_id: str) -> dict:
    """Request cancellation of one redundant route, preserving its saved research records."""
    return _tasks().cancel_task(task_id)

@mcp.tool()
def collect_task(task_id: str, detail: str = "summary", limit: int | None = None,
                 cursor: dict | None = None, kinds: list[str] | None = None,
                 record_ref: dict | None = None, include_result: bool = False,
                 import_refs: list[dict] | None = None, request_id: str | None = None) -> dict:
    """Read a child result index; detail='full' returns bounded record bodies.
    Pass next_cursor to continue/poll; replay a cursor to retry a page. Reviews/events need
    explicit kinds. record_ref={kind,id,revision} reads one exact record, independent of paging.
    include_result=True reads the final answer once. To import selected research records,
    provide import_refs (fixed child references) and a stable request_id. Imports preserve
    provenance, map references, and require parent audit; ordinary summary reads do not import.
    """
    return _tasks().collect_task(task_id, detail=detail, limit=limit, cursor=cursor,
                                 kinds=kinds, record_ref=record_ref, include_result=include_result,
                                 import_refs=import_refs, request_id=request_id)


if __name__ == "__main__":
    mcp.run(transport="stdio")
