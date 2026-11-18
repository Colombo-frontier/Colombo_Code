"""Process handoffs and bounded recovery packets; never mathematical review decisions."""

from __future__ import annotations
import json
import os
import re
import shutil
import time
import heapq
from colombo.shared.file_io import Path, atomic_write
from colombo.project_paths import CELL_AGENTS_ROOT


def _save(path: Path, value: dict) -> None:
    atomic_write(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def _read(path: Path) -> dict:
    path = Path(path)
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected an object in {path.name}")
    return value


def _process_path(root: Path, process_id: str) -> Path:
    if not isinstance(process_id, str) or not re.fullmatch(r"[0-9a-f]{32}", process_id):
        raise ValueError("Invalid process identifier")
    return root / "runtime" / "processes" / f"{process_id}.json"


def budget_windows(total: float | None, reserve: float, recovery: float) -> dict:
    """The three windows partition T; short runs keep time for actual work."""
    if (total is not None and total <= 0) or reserve < 0 or recovery < 0:
        raise ValueError("Budget must be positive and reserves nonnegative")
    if total is None:
        return {"total_seconds": None, "work_seconds": None,
                "reserve_seconds": 0, "recovery_seconds": 0}
    # Preserve half of a short budget for work. Shrink both closing windows
    # proportionally instead of rejecting legacy small per-process timeouts.
    scale = total / (2 * (reserve + recovery)) if reserve + recovery >= total else 1.0
    reserve, recovery = reserve * scale, recovery * scale
    return {"total_seconds": total, "work_seconds": total - reserve - recovery,
            "reserve_seconds": reserve, "recovery_seconds": recovery}


def begin_process(run_dir: Path, process_id: str, role: str, total: float | None,
                  settings: dict, *, started_at: float | None = None,
                  started_monotonic: float | None = None, shared_budget: dict | None = None) -> dict:
    root = Path(run_dir).resolve()
    config = settings["handoff"]
    enabled = role in {"prover", "subcell", "verifier"}
    windows = budget_windows(total, config["reserve_seconds"] if enabled else 0,
                             config["recovery_seconds"] if enabled else 0)
    started_at = time.time() if started_at is None else started_at
    started_monotonic = time.monotonic() if started_monotonic is None else started_monotonic
    if shared_budget is not None:
        # One root owner partitions its deadline. Descendants inherit those
        # windows instead of subtracting another reserve at every depth.
        deadline = shared_budget.get("deadline_unix")
        if deadline is None and total is None:
            windows = budget_windows(None, 0, 0)
        elif deadline is not None:
            own_deadline = deadline if total is None else min(deadline, started_at + total)
            hard = min(own_deadline, shared_budget.get("hard_deadline_unix") or own_deadline)
            work = min(hard, shared_budget.get("work_deadline_unix") or hard)
            total = max(0.0, own_deadline - started_at)
            windows = {"total_seconds": total,
                       "work_seconds": max(0.0, work - started_at),
                       "reserve_seconds": max(0.0, hard - max(work, started_at)),
                       "recovery_seconds": max(0.0, own_deadline - max(hard, started_at))}
    request_path = root / "review_request.json"
    request = _read(request_path) if request_path.exists() else {}
    state = {"process_id": process_id, "role": role, "stage": request.get("stage", role),
             "review_id": request.get("review_id"), "report_revision": request.get("report_revision"),
             "status": "running", "started_at": started_at, **windows,
             "time_limit_enabled": total is not None,
             "started_monotonic": started_monotonic,
             "soft_deadline": None if total is None else started_at + windows["work_seconds"],
             "hard_deadline": None if total is None else started_at + total - windows["recovery_seconds"],
             "total_deadline": None if total is None else started_at + total}
    if shared_budget is not None:
        state["shared_budget"] = {key: shared_budget.get(key) for key in
            ("policy_revision", "source", "deadline_unix", "work_deadline_unix", "hard_deadline_unix")}
    _save(_process_path(root, process_id), state)
    _save(root / "runtime" / "active_process.json", {"process_id": process_id})
    return state


def _current(run_dir: Path, process_id: str | None = None) -> tuple[Path, dict]:
    root = Path(run_dir).resolve()
    process_id = process_id or os.getenv("CELL_PROCESS_ID")
    if not process_id:
        process_id = _read(root / "runtime" / "active_process.json")["process_id"]
    state = _read(_process_path(root, process_id))
    if state.get("process_id") != process_id:
        raise ValueError("Process state does not match the current invocation")
    return root, state


def budget_status(run_dir: Path) -> dict:
    """Return this process's remaining work/closing time, not a new budget."""
    _, state = _current(run_dir)
    elapsed = max(0.0, time.monotonic() - state["started_monotonic"])
    limited = state["total_seconds"] is not None
    from colombo.shared.runtime_budget import get_budget_context
    shared = get_budget_context(run_dir)
    return {**state, "elapsed_seconds": elapsed, "root_budget": shared,
            "time_limit_enabled": limited,
            "remaining_seconds": max(0.0, state["total_seconds"] - state["recovery_seconds"] - elapsed) if limited else None,
            "work_remaining_seconds": max(0.0, state["work_seconds"] - elapsed) if limited else None,
            "closing": limited and elapsed >= state["work_seconds"],
            "handoff_skill": ".agents/skills/handoff/SKILL.md"}


def install_handoff_skill(work_dir: Path) -> Path:
    destination = Path(work_dir) / ".agents" / "skills" / "handoff" / "SKILL.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CELL_AGENTS_ROOT / "shared" / "handoff" / "SKILL.md", destination)
    return destination


def _strings(values, name: str) -> list[str]:
    if not isinstance(values, list) or not all(isinstance(item, str) and item.strip() for item in values):
        raise ValueError(f"{name} must be a list of nonempty strings")
    return values


def saved_references(run_dir: Path) -> list[str]:
    root = Path(run_dir)
    names = ["problem.md", "draft.md", "submission.json", "review_request.json", "review_notes.json",
             "confirmation_notes.json", "first_report.json", "review_report.json", "report.json", "confirmation.json"]
    request_file = root / "review_request.json"
    if request_file.is_file():
        try:
            request = _read(request_file)
        except (OSError, ValueError):
            request = {}
        evidence = request.get("evidence_files", [])
        evidence = evidence if isinstance(evidence, list) else []
        names += ["input/" + name for name in
                  [request.get("problem_file"), request.get("draft_file"), *evidence]
                  if isinstance(name, str)]
        if isinstance(request.get("correction_file"), str):
            names.append(request["correction_file"])
    if (root / "memory").is_dir():
        names += [p.relative_to(root).as_posix() for p in sorted((root / "memory").glob("*.json"))]
    # Keep remote execution identifiers available even if a process stopped
    # before the result entered memory. Do not scan or inject large raw outputs.
    for basename in ("state.json", "plan.json"):
        names += [p.relative_to(root).as_posix()
                  for p in sorted((root / "experiments").glob("exp-*/" + basename))]
    for basename in ("state.json", "input.json"):
        names += [p.relative_to(root).as_posix()
                  for p in sorted((root / "challenges").glob("ch-*/" + basename))]
    return list(dict.fromkeys(name for name in names if (root / name).is_file()
                              and not Path(name).is_absolute() and ".." not in Path(name).parts
                              and (root / name).resolve().is_relative_to(root.resolve())))


def _report(root: Path, state: dict, summary: str, pending: list[str], next_steps: list[str],
            references: list[str], reason: str, source: str) -> dict:
    return {"kind": "handoff", "process_id": state["process_id"], "role": state["role"],
            "stage": state["stage"], "review_id": state.get("review_id"),
            "report_revision": state.get("report_revision"),
            "recipient": "next_verifier" if state["role"] == "verifier" else "next_" + state["role"],
            "elapsed_seconds": max(0.0, time.monotonic() - state["started_monotonic"]),
            "stopping_reason": reason, "source": source,
            "summary": summary, "pending": pending, "next_steps": next_steps,
            "references": references, "execution_status": "incomplete",
            "has_review_authority": False,
            "budget": {"time_limit_enabled": state["total_seconds"] is not None,
                       **{key: state[key] for key in
                          ("total_seconds", "work_seconds", "reserve_seconds", "recovery_seconds")}}}


def finish_handoff(run_dir: Path, summary: str, pending: list[str], next_steps: list[str],
                   references: list[str] | None = None, stopping_reason: str = "budget") -> dict:
    """Commit a cooperative handoff after the agent saves its existing records."""
    root, state = _current(run_dir)
    elapsed = time.monotonic() - state["started_monotonic"]
    if state["status"] != "running" or (state["total_seconds"] is not None and
            elapsed >= state["total_seconds"] - state["recovery_seconds"]):
        raise ValueError("This process no longer accepts a cooperative handoff")
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("summary must be a nonempty string")
    if not isinstance(stopping_reason, str) or not stopping_reason.strip():
        raise ValueError("stopping_reason must be a nonempty string")
    references = _strings(references or [], "references")
    report = _report(root, state, summary, _strings(pending, "pending"),
                     _strings(next_steps, "next_steps"), references, stopping_reason, "agent")
    path = root / "handoffs" / f"{state['process_id']}.json"
    _save(path, report)
    _save(root / "runtime" / "processes" / f"{state['process_id']}.finished.json",
          {"process_id": state["process_id"], "report_path": str(path)})
    return {"execution_status": "handoff", "handoff_path": str(path), "recipient": report["recipient"]}


def completed_handoff(run_dir: Path, process_id: str) -> Path | None:
    root = Path(run_dir)
    marker = root / "runtime" / "processes" / f"{process_id}.finished.json"
    report = root / "handoffs" / f"{process_id}.json"
    if not marker.is_file() or not report.is_file():
        return None
    try:
        receipt, content = _read(marker), _read(report)
        if (receipt.get("process_id") == process_id and content.get("process_id") == process_id
                and receipt.get("report_path") == str(report)):
            return report
    except (OSError, ValueError):
        pass
    return None


def close_process(run_dir: Path, process_id: str, status: str) -> None:
    root, state = _current(run_dir, process_id)
    state.update(status=status, ended_at=time.time())
    _save(_process_path(root, process_id), state)


def factual_handoff(run_dir: Path, process_id: str, *, log_path: Path, reason: str) -> Path:
    """Always available without a model; it makes no inference about mathematics."""
    root, state = _current(run_dir, process_id)
    report = _report(root, state, "Process stopped; only previously saved files are available.",
                     ["Unsaved work is unavailable; a mathematical conclusion has not been established by this handoff."],
                     ["Read the saved records and resume the same task and audit stage."],
                     saved_references(root), reason, "runtime")
    report["log_path"] = str(log_path)
    path = root / "handoffs" / f"{process_id}.json"
    _save(path, report)
    return path


def enrich_handoff(path: Path, value: dict) -> None:
    """A packager may add navigation only; it cannot replace authoritative fields."""
    summary = value.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("Recovery summary is missing")
    pending = _strings(value.get("pending"), "pending")
    next_steps = _strings(value.get("next_steps"), "next_steps")
    report = _read(path)
    report["saved_evidence_summary"] = {"summary": summary, "pending": pending, "next_steps": next_steps,
                                        "has_review_authority": False}
    _save(path, report)


def record_recovery_status(path: Path, value: dict) -> None:
    """Record the packager's lifecycle without changing the factual handoff."""
    report = _read(Path(path))
    report["recovery"] = {**value, "has_review_authority": False}
    _save(Path(path), report)


_KINDS = frozenset({"claims", "arguments", "examples", "attempts", "sources",
                    "proof_state", "experiment_result", "reviews", "events"})
_ALIASES = {"claim": "claims", "argument": "arguments", "example": "examples",
            "attempt": "attempts", "source": "sources", "review": "reviews", "event": "events"}
_NAVIGATION_KEYS = ("status", "next_steps", "open_obligations", "pending", "gaps", "obstacles",
                    "route", "routes", "obligations", "summary", "decision_reason", "active_attempts", "target_ref",
                    "experiment_decision", "route_review")
_REF_PRIORITY = {"dependencies": 0, "active_attempts": 1, "useful_products": 1,
                 "produced_refs": 1, "result_refs": 1, "pending_refs": 1, "gap_refs": 1,
                 "target_ref": 2, "claim_ref": 2, "previous_detailed_state_ref": 2,
                 "owner_attempt_ref": 1, "closing_argument_ref": 1, "target_claim_ref": 2,
                 "conclusions": 2, "subject_refs": 2, "experiment_refs": 2}
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]*\Z")


# Bounded recovery packet construction

def _encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def _identity(value) -> tuple | None:
    if not isinstance(value, dict):
        return None
    kind = value.get("kind")
    if not isinstance(kind, str):
        return None
    kind = _ALIASES.get(kind, kind)
    name, revision = value.get("id"), value.get("revision")
    if (kind not in _KINDS or not isinstance(name, str) or not _ID.fullmatch(name)
            or type(revision) is not int or revision < 1):
        return None
    return kind, name, revision


def _references(value):
    """Walk explicit JSON references; never infer identities from prose or filenames."""
    stack = [(value, 3)]
    while stack:
        item, priority = stack.pop()
        if isinstance(item, dict):
            if "kind" in item and "id" in item:
                yield priority, item
            else:
                stack.extend((part, _REF_PRIORITY.get(key, priority))
                             for key, part in reversed(list(item.items())))
        elif isinstance(item, list):
            stack.extend((part, priority) for part in reversed(item))


def build_recovery_packet(work_dir: Path, handoff_path: Path, destination: Path,
                          settings: dict, *, deadline: float | None = None) -> dict:
    """Write one size-bounded file without editing source records or making judgments.

    References are navigation for the next same-role process, not permission for
    the short-lived packager to open files outside this independent packet.
    """
    root, destination = Path(work_dir).resolve(), Path(destination)
    config = settings["handoff"]
    maximum = config["recovery_input_max_bytes"]
    source_maximum = config["recovery_source_max_bytes"]
    record_limit = config["recovery_max_records"]
    if type(maximum) is not int or maximum < 2048:
        raise ValueError("recovery_input_max_bytes must be an integer >= 2048")
    if type(source_maximum) is not int or source_maximum < 1:
        raise ValueError("recovery_source_max_bytes must be a positive integer")
    if type(record_limit) is not int or record_limit < 1:
        raise ValueError("recovery_max_records must be a positive integer")

    def identity(value):
        key = _identity(value)
        return key if key is not None and len(key[1]) <= settings["limits"]["record_id_max_chars"] else None

    diagnostics, sources, cache, selected = [], [], {}, []
    diagnostic_count = 0
    selected_by_key = {}
    counts = {"loaded_record_versions": 0, "selected_records": 0,
              "unresolved_references": 0, "unexpanded_references": 0}
    expired = False

    def time_available():
        nonlocal expired
        if deadline is not None and time.monotonic() >= deadline:
            expired = True
        return not expired

    def note(source, reason, **details):
        nonlocal diagnostic_count
        diagnostic_count += 1
        if len(diagnostics) < record_limit:
            diagnostics.append({"source": source, "reason": reason, **details})

    def safe_path(relative):
        if not isinstance(relative, str):
            raise ValueError("source path must be relative text")
        path = Path(relative)
        if path.is_absolute() or path.drive or ".." in path.parts:
            raise ValueError("source is outside the task")
        path = (root / path).resolve()
        if not path.is_relative_to(root):
            raise ValueError("source redirects outside the task")
        return path

    def read_source(relative, *, json_value=True):
        if not time_available():
            return None
        try:
            path = safe_path(relative)
            size = path.stat().st_size
            if size > source_maximum:
                note(relative, "source_too_large", bytes=size)
                return None
            with path.open("rb") as handle:
                # Plain documents need only a packet-sized prefix. JSON sources
                # need complete syntax, but are capped before and during reads.
                limit = source_maximum if json_value else min(source_maximum, maximum)
                data = handle.read(limit + 1)
            if json_value and len(data) > source_maximum:
                note(relative, "source_grew_beyond_limit", bytes=len(data))
                return None
            text = data[:limit].decode("utf-8-sig", errors="replace" if not json_value else "strict")
            value = json.loads(text) if json_value else text
            sources.append({"source": relative, "bytes": size,
                            "read_bytes": min(len(data), limit), "prefix_only": len(data) > limit})
            return value
        except (OSError, ValueError, RecursionError) as exc:
            note(relative, "missing_source" if isinstance(exc, FileNotFoundError) else "unreadable_source",
                 error=type(exc).__name__)
            return None

    def collection(kind):
        if kind in cache:
            return cache[kind]
        records = {}
        relative = f"memory/{kind}.json"
        document = read_source(relative)
        if document is not None:
            if not isinstance(document, dict) or document.get("schema_version") != 2 or not isinstance(document.get("records"), list):
                note(relative, "invalid_collection")
            else:
                counts["loaded_record_versions"] += len(document["records"])
                for record in document["records"]:
                    if not time_available():
                        break
                    key = identity(record)
                    if key is not None and key[0] == kind and isinstance(record.get("payload"), dict):
                        records[key] = (record, relative)
                    else:
                        note(relative, "invalid_record_envelope")
        cache[kind] = records
        return records

    context_manifest = None

    def context_record(key):
        nonlocal context_manifest
        if context_manifest is None:
            document = read_source("context/manifest.json")
            refs = document.get("snapshot_refs", []) if isinstance(document, dict) else []
            if not isinstance(refs, list):
                note("context/manifest.json", "invalid_context_manifest")
                refs = []
            context_manifest = {identity(ref): ref for ref in refs if identity(ref) is not None}
        if key not in context_manifest:
            return None
        cache_key = "context:" + key[0]
        if cache_key not in cache:
            relative = f"context/{key[0]}.json"
            document = read_source(relative)
            rows = document.get("records", []) if isinstance(document, dict) and document.get("schema_version") == 2 else []
            if not isinstance(rows, list):
                note(relative, "invalid_context_collection")
                rows = []
            cache[cache_key] = {identity(row): (row, relative) for row in rows
                                if identity(row) in context_manifest and isinstance(row.get("payload"), dict)}
        found = cache[cache_key].get(key)
        return found

    queue = []
    queued_count = 0

    def take(record, source, reference=None):
        nonlocal queued_count
        key = identity(record)
        prior = selected_by_key.get(key)
        if prior is None and len(selected) >= record_limit:
            return
        payload = record["payload"]
        selection = None
        if key[0] == "examples":
            properties = payload.get("properties")
            if (not isinstance(properties, list) or any(not isinstance(prop, dict) or
                    not isinstance(prop.get("id"), str) for prop in properties)):
                note(source, "invalid_example_properties", reference=list(key))
                return
            available = {prop["id"] for prop in properties}
            if len(available) != len(properties):
                note(source, "duplicate_example_properties", reference=list(key))
                return
            allowed = set(available)
            restrictions = [record]
            if source.startswith("context/"):
                restrictions.append(context_manifest[key])
            for constraint in restrictions:
                if "property_ids" not in constraint:
                    continue
                ids = constraint["property_ids"]
                if (not isinstance(ids, list) or not ids or any(not isinstance(item, str) for item in ids)
                        or len(ids) != len(set(ids)) or not set(ids) <= available):
                    note(source, "invalid_property_grant", reference=list(key))
                    return
                allowed.intersection_update(ids)
            requested = set(reference["property_ids"]) if reference and "property_ids" in reference else set(allowed)
            selection = requested & allowed
            if requested - allowed:
                note(source, "properties_outside_grant", reference=list(key),
                     property_ids=sorted(requested - allowed))
            if not selection:
                note(source, "no_authorized_properties", reference=list(key))
                return
            if prior is not None:
                selection |= set(prior["reference"]["property_ids"])
                if selection == set(prior["reference"]["property_ids"]):
                    return
            # Filter before dependency traversal. An unselected property's
            # statement, trust label and references must not enter this packet.
            payload = {**payload, "properties": [prop for prop in properties if prop["id"] in selection]}
        elif prior is not None:
            return
        ordered = {name: payload[name] for name in _NAVIGATION_KEYS if name in payload}
        ordered.update({name: value for name, value in payload.items() if name not in ordered})
        row = {"source": source, "reference": {"kind": key[0], "id": key[1], "revision": key[2],
                       **({"property_ids": sorted(selection)} if selection is not None else {})},
               "historical_status_only": True, "payload": ordered}
        if prior is None:
            selected.append(row)
            selected_by_key[key] = row
        else:
            prior.update(row)
        for priority, reference in _references(payload):
            heapq.heappush(queue, (priority, queued_count, reference))
            queued_count += 1

    # The latest state is the entry point, rather than all of its old revisions.
    states = collection("proof_state")
    if states:
        state, source = max(states.values(), key=lambda item: (str(item[0].get("created_at", "")), item[0]["revision"]))
        take(state, source)
    attempts = collection("attempts")
    if attempts and len(selected) < record_limit:
        attempt, source = max(attempts.values(), key=lambda item: (str(item[0].get("created_at", "")), item[0]["revision"]))
        take(attempt, source)
    seen_refs = set()
    deferred_references = 0
    while queue and time_available():
        _, _, reference = heapq.heappop(queue)
        key = identity(reference)
        if key is None:
            counts["unresolved_references"] += 1
            note("record_reference", "invalid_or_unpinned_reference")
            continue
        property_ids = reference.get("property_ids")
        if "property_ids" in reference and (key[0] != "examples" or not isinstance(property_ids, list)
                or not property_ids or any(not isinstance(item, str) for item in property_ids)
                or len(property_ids) != len(set(property_ids))):
            counts["unresolved_references"] += 1
            note("record_reference", "invalid_property_selection", reference=list(key))
            continue
        marker = (key, tuple(sorted(property_ids)) if property_ids is not None else None)
        if marker in seen_refs:
            continue
        seen_refs.add(marker)
        if len(selected) >= record_limit and key not in selected_by_key:
            deferred_references += 1
            continue
        found = collection(key[0]).get(key) or context_record(key)
        if not found:
            counts["unresolved_references"] += 1
            note(f"memory/{key[0]}.json", "missing_pinned_revision", reference=list(key))
            continue
        record, source = found
        take(record, source, reference)
    counts["unexpanded_references"] = len(queue) + deferred_references
    counts["selected_records"] = len(selected)
    counts["unselected_loaded_versions"] = max(0, counts["loaded_record_versions"] - sum(row["source"].startswith("memory/") for row in selected))

    documents = []
    handoff_relative = None
    try:
        handoff_relative = Path(handoff_path).resolve().relative_to(root).as_posix()
    except ValueError:
        note("handoff", "handoff_outside_task")
    names = [handoff_relative, "review_request.json", "review_notes.json", "confirmation_notes.json",
             "first_report.json", "review_report.json", "confirmation.json", "submission.json"]
    request = None
    for relative in (name for name in names if name):
        if not time_available():
            break
        # Optional absent review files are common in a prover; record only the
        # handoff and files which actually exist as missing/read errors.
        if relative != handoff_relative:
            try:
                if not safe_path(relative).exists():
                    continue
            except (OSError, ValueError):
                note(relative, "source_outside_task")
                continue
        document = read_source(relative)
        if document is not None:
            documents.append({"source": relative, "content": document})
        if relative == "review_request.json" and isinstance(document, dict):
            request = document
    text_names = ["problem.md"]
    if request:
        text_names = ["input/" + value for key in ("problem_file", "draft_file")
                      if isinstance((value := request.get(key)), str)]
        evidence = request.get("evidence_files", [])
        if isinstance(evidence, list):
            text_names += ["input/" + name for name in evidence[:record_limit] if isinstance(name, str)]
            if len(evidence) > record_limit:
                note("review_request.json", "evidence_file_limit", omitted=len(evidence) - record_limit)
    for relative in dict.fromkeys(text_names):
        text = read_source(relative, json_value=False)
        if text is not None:
            documents.append({"source": relative, "content": text})

    packet = {
        "kind": "recovery_input", "has_review_authority": False,
        "scope": "Read only this packet. Source paths and record references are navigation for the next same-role process, not permission to open external files.",
        "trust_notice": "Copied labels are historical only; no current mathematical trust was calculated. This packet cannot certify or reject anything.",
        "selection": "Latest saved proof_state, latest Attempt, then explicit pinned references. Unlisted collections and other historical versions were not copied.",
        "counts": counts, "deadline_reached": expired,
        "records": [], "documents": [], "sources": [], "omissions": [],
        "truncation": {"content_items": 0, "index_items": 0},
    }
    packet["counts"]["diagnostic_events"] = diagnostic_count
    packet["counts"]["diagnostic_events_not_listed"] = max(0, diagnostic_count - len(diagnostics))
    # Reserve space for changing counters. Each body also gets a fair share so
    # one large proof_state cannot crowd out all referenced records and notes.
    body_limit = maximum // max(1, len(selected) + len(documents))
    content_ceiling = maximum - 512

    def append_bounded(section, row, content_key=None):
        target = packet[section]
        if not time_available():
            packet["truncation"]["index_items" if content_key is None else "content_items"] += 1
            return
        if content_key is None:
            target.append(row)
            if len(_encode(packet)) > content_ceiling:
                target.pop()
                packet["truncation"]["index_items"] += 1
            return
        text = json.dumps(row[content_key], ensure_ascii=False, separators=(",", ":"), allow_nan=False)
        target.append(row)
        if len(_encode(row)) <= body_limit and len(_encode(packet)) <= content_ceiling:
            return
        target.pop()
        excerpt = {key: value for key, value in row.items() if key != content_key}
        excerpt.update({"content_excerpt": "", "excerpt_format": "verbatim JSON prefix; incomplete",
                        "original_content_bytes": len(text.encode("utf-8")), "truncated": True})
        target.append(excerpt)
        if len(_encode(packet)) > content_ceiling:
            target.pop()
            packet["truncation"]["content_items"] += 1
            return
        low, high = 0, len(text)
        while low < high:
            if not time_available():
                break
            middle = (low + high + 1) // 2
            excerpt["content_excerpt"] = text[:middle]
            if len(_encode(excerpt)) <= body_limit and len(_encode(packet)) <= content_ceiling:
                low = middle
            else:
                high = middle - 1
        excerpt["content_excerpt"] = text[:low]
        packet["truncation"]["content_items"] += 1

    for row in selected:
        append_bounded("records", row, "payload")
    for row in documents:
        append_bounded("documents", row, "content")
    for row in sources:
        append_bounded("sources", row)
    for row in diagnostics:
        append_bounded("omissions", row)
    packet["deadline_reached"] = expired
    data = _encode(packet)
    if len(data) > maximum:
        raise ValueError("Recovery packet metadata exceeds its configured byte limit")
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / "recovery_input.json"
    atomic_write(output, data)
    return {"packet_file": str(output), "bytes": len(data), "included_records": len(packet["records"]),
            "source_files": len(sources), "deadline_reached": expired,
            "truncated": any(packet["truncation"].values()) or bool(diagnostics) or bool(counts["unexpanded_references"]),
            "omitted_loaded_versions": counts["unselected_loaded_versions"]}


def caller_deadline(run_dir, *, status_reader=None, phase="work"):
    from colombo.shared.runtime_budget import inherited_deadline
    deadline = inherited_deadline(run_dir, phase=phase)
    if os.getenv("CELL_PROCESS_ID"):
        status = (status_reader or budget_status)(run_dir)
        remaining = status.get("work_remaining_seconds" if phase == "work" else "remaining_seconds")
        if remaining is not None:
            local = time.monotonic() + remaining
            deadline = local if deadline is None else min(deadline, local)
        hard = status.get("hard_deadline")
        if hard is not None:
            local = time.monotonic() + max(0.0, hard-time.time())
            deadline = local if deadline is None else min(deadline, local)
    return deadline
