"""Persistent proof-specific checks and source inspection for one independent review."""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path as _BootstrapPath
import sys
import threading

if __package__ in {None, ""}:
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[3]))
from colombo.shared.file_io import Path
from colombo.shared.file_io import atomic_write
from mcp.server.fastmcp import FastMCP

from colombo.shared.literature_access import lookup
from colombo.cell.verifier.review_validation import validate_receipt
from colombo.cell.verifier.review_validation import validate_records
from colombo.cell.verifier.review_validation import validate_report_notes
from colombo.cell.verifier.review_validation import validate_confirmation
from colombo.cell.verifier.review_validation import validate_confirmation_receipt
from colombo.cell.settings import get_settings


RUN = Path(os.environ.get("CELL_RUN_DIR", ".")).resolve()
if os.environ.get("CELL_ROLE", "verifier") != "verifier":
    raise ValueError("This MCP server is reserved for the verifier process")
mcp = FastMCP("cell_review")
_lock = threading.RLock()
_COLLECTIONS = ("checks", "findings", "sources")


def _request() -> dict:
    return json.loads((RUN / "review_request.json").read_text(encoding="utf-8"))


def _require_stage(stage: str) -> dict:
    request = _request()
    if request.get("stage", "proof") != stage:
        raise ValueError(f"This tool is only available during {stage}")
    return request


def _read_notes() -> dict:
    path = RUN / "review_notes.json"
    if not path.exists():
        return {key: [] for key in _COLLECTIONS}
    notes = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(notes, dict) or set(notes) != set(_COLLECTIONS):
        raise ValueError("review_notes.json has an invalid record structure")
    validate_records(notes["checks"], notes["findings"], notes["sources"])
    return notes


def _write_json(path: Path, payload: dict) -> None:
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    atomic_write(path, content.encode("utf-8"))


@mcp.tool()
def record_check(check_id: int, status: str, reason: str, subject: str, location: str,
                 findings: list[dict] | None = None) -> dict:
    """Record an actual proof obligation and replace its attached findings.

    Assign a stable positive ID within this proof, independent of reference-list
    numbering. subject names the claim/transition; location locates the evidence.
    Findings use id, check_id, kind, location, explanation, and repair. A failed
    item needs an error/gap; an unresolved item needs an uncertain finding.
    To correct an earlier concern, give the new reason and the complete current
    findings for this item. Omitted findings means an empty list.
    """
    check = {"id": check_id, "status": status, "reason": reason,
             "subject": subject, "location": location}
    findings = deepcopy(findings) if findings is not None else []
    validate_records([check], findings, [])
    with _lock:
        notes = _read_notes()
        notes["checks"] = [row for row in notes["checks"] if row["id"] != check_id] + [check]
        notes["findings"] = [row for row in notes["findings"] if row["check_id"] != check_id] + findings
        validate_records(notes["checks"], notes["findings"], notes["sources"])
        _write_json(RUN / "review_notes.json", notes)
        count = len(notes["checks"])
    return {"check_id": check_id, "status": status,
            "finding_ids": [row["id"] for row in findings], "recorded_checks": count}


@mcp.tool()
def record_source(citation: str, location: str, status: str,
                  evidence: str, application: str, check_id: int) -> dict:
    """Record a cited result at one manuscript location, replacing that occurrence.

    Use confirmed after inspecting the original statement and its application;
    mismatch means a demonstrated discrepancy; unavailable means not verified.
    check_id links the actual proof check; final mismatch/unavailable records
    need a corresponding finding on that check.
    """
    source = {"citation": citation, "location": location, "status": status,
              "evidence": evidence, "application": application, "check_id": check_id}
    validate_records([], [], [source])
    with _lock:
        notes = _read_notes()
        key = (citation, location)
        notes["sources"] = [row for row in notes["sources"]
                            if (row["citation"], row["location"]) != key] + [source]
        _write_json(RUN / "review_notes.json", notes)
    return {"citation": citation, "location": location, "status": status, "saved": True}


@mcp.tool()
def read_review(limit: int | None = None, reverse: bool | None = None,
                detail: str = "summary", check_id: int | None = None, offset: int = 0) -> dict:
    """Inspect recorded statuses; detail='full' reads saved evidence.

    Full records are paged separately per collection using offset/limit, in last
    update order; next_offsets identifies more pages. check_id filters checks and
    findings, leaving sources accessible. Paging assumes no intervening edits.
    Defaults use verifier_memory_results and verifier_reverse from this task.
    """
    settings = get_settings(RUN)["retrieval"]
    limit = settings["verifier_memory_results"] if limit is None else limit
    reverse = settings["verifier_reverse"] if reverse is None else reverse
    if type(limit) is not int or not 1 <= limit <= settings["max_memory_results"]:
        raise ValueError(f"limit must be an integer from 1 to {settings['max_memory_results']}")
    if type(reverse) is not bool:
        raise ValueError("reverse must be a boolean")
    if detail not in {"summary", "full"}:
        raise ValueError("detail must be summary or full")
    if type(offset) is not int or offset < 0:
        raise ValueError("offset must be a nonnegative integer")
    if check_id is not None and (type(check_id) is not int or check_id < 1):
        raise ValueError("check_id must be a positive integer")
    with _lock:
        notes = _read_notes()
    totals = {key: len(notes[key]) for key in _COLLECTIONS}
    if detail == "summary":
        by_status = {status: sorted(row["id"] for row in notes["checks"] if row["status"] == status)
                     for status in ("pass", "fail", "unresolved")}
        return {"totals": totals,
                "check_ids_by_status": by_status,
                "source_status_counts": {status: sum(row["status"] == status for row in notes["sources"])
                                         for status in ("confirmed", "mismatch", "unavailable")}}
    if check_id is not None:
        notes["checks"] = [row for row in notes["checks"] if row["id"] == check_id]
        notes["findings"] = [row for row in notes["findings"] if row["check_id"] == check_id]
    selected = {key: len(notes[key]) for key in _COLLECTIONS}
    result = {key: (list(reversed(notes[key])) if reverse else notes[key])[offset:offset + limit]
              for key in _COLLECTIONS}
    next_offsets = {key: offset + len(result[key]) for key in _COLLECTIONS
                    if offset + len(result[key]) < selected[key]}
    return {**result, "totals": totals, "selected_totals": selected,
            "next_offsets": next_offsets, "truncated": bool(next_offsets)}


@mcp.tool()
def lookup_sources(query: str | None = None, url: str | None = None,
                   limit: int | None = None) -> dict:
    """Discover papers or fetch a source URL; returned text still needs review.

    limit bounds search hits, not downloaded source text. It defaults to
    verifier_search_results and cannot exceed max_search_results.
    """
    retrieval = get_settings(RUN)["retrieval"]
    limit = retrieval["verifier_search_results"] if limit is None else limit
    if type(limit) is not int or not 1 <= limit <= retrieval["max_search_results"]:
        raise ValueError(f"limit must be an integer from 1 to {retrieval['max_search_results']}")
    if query is not None and not isinstance(query, str):
        raise ValueError("query must be a string")
    if url is not None and not isinstance(url, str):
        raise ValueError("url must be a string")
    return lookup(query=query or "", url=url or "", limit=limit)


@mcp.tool()
def write_report(verdict: str, summary: str, target_alignment: str, coverage: str) -> dict:
    """Assemble a report from saved notes and return the final JSON receipt.

    coverage explains why the recorded checks cover the target, necessary claims,
    transitions, and citations. Record at least one substantive check. No saved
    checks, findings, or sources are inferred or omitted. verdict must agree with
    these records. Correct records before
    retrying a rejected report. Return this receipt unchanged as the final answer;
    later note edits require writing a new report. This validates consistency,
    not mathematical truth.
    """
    with _lock:
        request = _require_stage("proof")
        notes = _read_notes()
        payload = {"verdict": verdict, "summary": summary,
                   "target_alignment": target_alignment, "coverage": coverage, **notes}
        validate_report_notes(payload, notes)
        receipt = {"review_id": request["review_id"], "report_revision": request["report_revision"], "verdict": verdict}
        validate_receipt(receipt)
        target = RUN / "review_report.json"
        _write_json(target, payload)
    return receipt


@mcp.tool()
def write_confirmation(verdict: str, summary: str, assessment: dict,
                       covered_check_ids: list[int], findings: list[dict],
                       decisive_steps: list[dict], new_findings: list[dict]) -> dict:
    """Save the independent assessment of the whole first report.

    assessment requires target_alignment, coverage, reasoning, sources and
    record_mapping, each with status supported/disputed/unresolved and reason.
    Assess every first-report finding exactly once. Check decisive proof steps
    independently even when the first report passes. Any disagreement or newly
    found problem requires needs_correction; it stays inside the verifier.
    """
    with _lock:
        request = _require_stage("report_check")
        report_bytes = (RUN / "first_report.json").read_bytes()
        payload = {"verdict": verdict, "summary": summary, "review_id": request["review_id"],
                   "report_revision": request["report_revision"], "assessment": assessment,
                   "covered_check_ids": covered_check_ids, "findings": findings,
                   "decisive_steps": decisive_steps, "new_findings": new_findings}
        validate_confirmation(payload, json.loads(report_bytes), review_id=request["review_id"],
                              report_revision=request["report_revision"])
        target = RUN / "confirmation.json"
        _write_json(target, payload)
        receipt = {"review_id": request["review_id"], "report_revision": request["report_revision"], "verdict": verdict}
        return validate_confirmation_receipt(receipt)


@mcp.tool()
def save_confirmation_notes(summary: str, pending: list[str], evidence: list[dict]) -> dict:
    """Checkpoint unfinished report-check reasoning; this cannot approve a report."""
    _require_stage("report_check")
    if not summary.strip() or not all(isinstance(item, str) for item in pending):
        raise ValueError("summary must be nonempty and pending must contain strings")
    if not all(isinstance(item, dict) for item in evidence):
        raise ValueError("evidence must contain objects")
    with _lock:
        _write_json(RUN / "confirmation_notes.json", {
            "summary": summary, "pending": pending, "evidence": evidence})
    return {"saved": True, "path": "confirmation_notes.json"}


@mcp.tool()
def budget_status() -> dict:
    """Inspect remaining time and closing. Unlimited mode has time_limit_enabled=false,
    null deadlines/remaining times, and closing=false; explicit handoff remains available.
    """
    from colombo.cell.recovery import budget_status as inspect
    return inspect(RUN)


@mcp.tool()
def finish_handoff(summary: str, pending: list[str], next_steps: list[str],
                   references: list[str] | None = None, stopping_reason: str = "budget") -> dict:
    """After saving notes, hand this unfinished stage to the next verifier."""
    from colombo.cell.recovery import finish_handoff as finish
    return finish(RUN, summary, pending, next_steps, references, stopping_reason)


if __name__ == "__main__":
    mcp.run(transport="stdio")
