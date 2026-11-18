"""Review frozen mathematics, independently confirm the report, then reconcile trust."""
from __future__ import annotations

from colombo.cell.record_store import json_equal

from contextlib import contextmanager, ExitStack
import json
import os
from pathlib import PureWindowsPath
from colombo.shared.file_io import Path, file_lock
from colombo.shared.file_io import atomic_write
import re
import shutil
from typing import Callable
from uuid import uuid4

from colombo.cell.verifier.review_validation import RECEIPT_SCHEMA
from colombo.cell.verifier.review_validation import CONFIRMATION_RECEIPT_SCHEMA
from colombo.cell.verifier.review_validation import validate_receipt
from colombo.cell.verifier.review_validation import validate_report
from colombo.cell.verifier.review_validation import validate_report_notes
from colombo.cell.verifier.review_validation import validate_confirmation
from colombo.cell.verifier.review_validation import validate_confirmation_receipt
from colombo.cell.verifier.review_validation import validate_record_ref
from colombo.cell.settings import get_settings
from colombo.cell.restart_budget import effective_limit

REVIEW_PROTOCOL = "cell-proof-review-5"
from colombo.project_paths import CELL_AGENTS_ROOT
RESOURCES = Path(CELL_AGENTS_ROOT) / "verifier"


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain an object")
    return value


def _save(path: Path, value: dict) -> None:
    _save_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def _save_bytes(path: Path, content: bytes) -> None:
    atomic_write(path, content)


def _set_status(root: Path, status: str, reason: str, **details) -> dict:
    submission = _load(root / "submission.json")
    submission.update(status=status, review_reason=reason, **details)
    _save(root / "submission.json", submission)
    return {"status": status, "reason": reason, **details}


def _input_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Input paths must be nonempty strings")
    portable = PureWindowsPath(name)
    local = Path(name.replace("\\", "/"))
    if portable.drive or portable.root or local.is_absolute() or ".." in local.parts:
        raise ValueError(f"Input must stay inside the task directory: {name}")
    path = (root / local).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Input escapes the task directory: {name}")
    return path


def validate_required_review_files(root: Path, names) -> list[str]:
    """Pin explicit task-relative evidence; never expand a directory or dependency."""
    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        raise ValueError("required_review_files must be a list of paths")
    result = []
    for name in names:
        _input_path(root, name)
        relative = Path(name.replace("\\", "/")).as_posix()
        if relative in {"manuscript.md", "cell_record_evidence.json"}:
            raise ValueError(f"{relative} is reserved generated output")
        if relative not in result:
            result.append(relative)
    return result


def _required_names(root: Path) -> list[str]:
    config = _load(root / "run.json") if (root / "run.json").is_file() else {}
    return validate_required_review_files(root, config.get("required_review_files", []))


def _submitted_names(submission: dict, required=()) -> list[str]:
    evidence = submission.get("evidence_files", [])
    if not isinstance(evidence, list) or not all(isinstance(p, str) for p in evidence):
        raise ValueError("evidence_files must be a list of paths")
    if submission.get("problem_file", "problem.md") != "problem.md":
        raise ValueError("The original problem_file must be problem.md")
    return ["problem.md", submission.get("draft_file", "draft.md"), *required, *evidence]


def _protect_inputs(root: Path, submission: dict) -> None:
    output = root / "manuscript.md"
    for name in _submitted_names(submission, _required_names(root)):
        source = _input_path(root, name)
        if source == output.resolve() or (source.exists() and output.exists() and source.samefile(output)):
            raise ValueError("manuscript.md is reserved output and cannot be a submitted input")


def _capture(root: Path, submission: dict) -> dict:
    _protect_inputs(root, submission)
    if submission.get("outcome") not in {"proved", "disproved"}:
        raise ValueError("outcome must be proved or disproved")
    required = _required_names(root)
    files = {}
    for name in _submitted_names(submission, required):
        path = _input_path(root, name)
        relative = Path(name.replace("\\", "/")).as_posix()
        files[relative] = path.read_bytes()
    from colombo.cell.instructions import review_guidance
    from colombo.cell.instructions import read_cell_mode
    from colombo.cell.instructions import pack_for_mode
    cell_mode = read_cell_mode(root)
    pack = pack_for_mode(cell_mode)
    guidance = review_guidance(root)
    if guidance is not None:
        files[pack["review_file"]] = guidance
        required = list(dict.fromkeys([*required, pack["review_file"]]))
    draft = Path(submission.get("draft_file", "draft.md").replace("\\", "/")).as_posix()
    if draft == "problem.md":
        raise ValueError("The draft must be separate from problem.md")
    for name in ("problem.md", draft):
        if not files[name].decode("utf-8-sig").strip():
            raise ValueError(f"{name} is empty")
    refs = submission.get("record_refs", [])
    if not isinstance(refs, list):
        raise ValueError("record_refs must be a list of exact record references")
    for ref in refs:
        validate_record_ref(ref, require_position=True)
    from colombo.cell.record_store import Store
    store = Store(root / "memory")
    records = store.resolve_record_refs(refs) if refs else []
    bundle = store.evidence_bundle(refs)
    submitted_keys = {(r["kind"], r["id"], r["revision"]) for r in records}
    records.extend(row for row in bundle["records"]
                   if (row["kind"], row["id"], row["revision"]) not in submitted_keys)
    for name, data in bundle["files"].items():
        if name in files and files[name] != data:
            raise ValueError("Experiment artifact conflicts with submitted evidence")
        files[name] = data
    for row in records:
        payload = row["payload"]
        ids = {payload["audit_id"]} if payload.get("audit_id") else set()
        ids.update(prop["audit_id"] for prop in payload.get("properties", []) if prop.get("audit_id")
                   and (not row.get("property_ids") or prop["id"] in row["property_ids"]))
        audits = []
        for audit_id in sorted(ids):
            audit = store.get("reviews", audit_id)
            target = audit["payload"]["target"]
            audits.append({"review": audit, "reviewed_record": store.get(
                target["kind"], target["id"], target["revision"])})
        row["supporting_audits"] = audits
    # Trust is derived from subsequent reviews; immutable mathematical content
    # and exact original audit evidence identify this submission's snapshot.
    def stable(value):
        if isinstance(value, dict):
            return {key: stable(item) for key, item in value.items() if key != "current_trust"}
        return [stable(item) for item in value] if isinstance(value, list) else value
    trust_context = [{"kind": row["kind"], "id": row["id"], "revision": row["revision"],
                      "current_trust": row.get("current_trust", {})} for row in records]
    records = stable(records)
    reserved = "cell_record_evidence.json"
    if reserved in files:
        raise ValueError(f"{reserved} is reserved for resolved record evidence")
    files[reserved] = (json.dumps(records, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    manifest = {"protocol": REVIEW_PROTOCOL, "outcome": submission["outcome"], "draft_file": draft,
                "record_refs": refs,
                "experiment_artifacts": bundle["artifacts"],
                "required_files": list(dict.fromkeys(["problem.md", draft, *required])),
                "selected_evidence_files": list(dict.fromkeys(
                    Path(name.replace("\\", "/")).as_posix() for name in submission.get("evidence_files", []))),
                "files": sorted(files)}
    if guidance is not None:
        manifest["cell_mode"] = cell_mode
    return {"manifest": manifest, "files": files, "settings": get_settings(root),
            "trust_context": (json.dumps(trust_context, ensure_ascii=False, indent=2) + "\n").encode("utf-8")}


def _review_dir(root: Path, review_id: str) -> Path:
    if not isinstance(review_id, str) or not re.fullmatch(r"r\d{4,}", review_id):
        raise ValueError("Invalid review identifier")
    folder = root / "reviews" / review_id
    if not folder.resolve().is_relative_to(root):
        raise ValueError("Review directory escapes the task")
    return folder


def _index(root: Path) -> dict:
    path = root / "reviews" / "index.json"
    if not path.exists():
        return {"protocol": REVIEW_PROTOCOL, "attempts": [], "primary_launches": 0}
    index = _load(path)
    if not isinstance(index.get("attempts"), list) or not all(isinstance(x, dict) for x in index["attempts"]):
        raise ValueError("Review index has malformed attempts")
    if index.get("protocol") != REVIEW_PROTOCOL:
        raise ValueError("Unrecognized review protocol")
    index.setdefault("primary_launches", len(index["attempts"]))
    if type(index["primary_launches"]) is not int or index["primary_launches"] < 0:
        raise ValueError("Invalid primary launch counter")
    return index


def _persist(root: Path, index: dict) -> None:
    _save(root / "reviews" / "index.json", index)


def has_pending_review(run_dir: Path) -> bool:
    """Pending includes exhausted audits: they must never fall through to prover."""
    try:
        return any(item.get("protocol") == REVIEW_PROTOCOL and item.get("phase") != "complete"
                   for item in _index(Path(run_dir).resolve())["attempts"])
    except (OSError, ValueError, TypeError):
        return (Path(run_dir) / "reviews" / "index.json").exists()


def _same_submission(capture: dict, folder: Path) -> bool:
    try:
        return (json_equal(_load(folder / "snapshot.json"), capture["manifest"]) and
                all((folder / "input" / name).read_bytes() == data
                    for name, data in capture["files"].items()))
    except (OSError, ValueError):
        return False


def submission_matches(root: Path, submission: dict, item: dict) -> bool:
    """Compare a current submission to the review's fixed submission snapshot."""
    try:
        return _same_submission(_capture(root, submission), _review_dir(root, item["id"]))
    except (OSError, ValueError, KeyError, TypeError):
        return False


def _report_pair(folder: Path, item: dict) -> tuple[dict, dict]:
    report_data = (folder / "reports" / f"p{item['report_revision']:04d}.json").read_bytes()
    confirmation_data = (folder / "checks" / f"p{item['report_revision']:04d}" / "confirmation.json").read_bytes()
    report = validate_report(json.loads(report_data))
    confirmation = validate_confirmation(json.loads(confirmation_data), report,
        review_id=item["id"], report_revision=item["report_revision"])
    if confirmation["verdict"] != "confirmed" or not item.get("trust_synced"):
        raise ValueError("The report is not confirmed and synchronized")
    return report, confirmation


def _valid_receipt(root: Path, capture: dict, index: dict) -> dict | None:
    for item in reversed(index["attempts"]):
        if (item.get("protocol") != REVIEW_PROTOCOL or not _same_submission(capture, _review_dir(root, item["id"]))
                or item.get("status") != "accepted" or item.get("phase") != "complete"):
            continue
        try:
            folder = _review_dir(root, item["id"])
            report, _ = _report_pair(folder, item)
            _check_current_support(root, capture)
            if report["verdict"] == "pass" and (folder / "manuscript.md").is_file():
                return item
        except (OSError, ValueError, KeyError, TypeError):
            continue
    return None


def manuscript_is_current(run_dir: Path) -> bool:
    root = Path(run_dir).resolve()
    try:
        submission = _load(root / "submission.json")
        if submission.get("status") != "accepted":
            return False
        capture = _capture(root, submission)
        receipt = _valid_receipt(root, capture, _index(root))
        return bool(receipt and submission.get("review_id") == receipt["id"]
                    and (root / "manuscript.md").is_file())
    except (OSError, ValueError, KeyError, TypeError):
        return False


def _request(review_id: str, capture: dict, *, stage: str = "proof", **details) -> dict:
    return {"review_id": review_id, "report_revision": details.pop("report_revision", 1), "stage": stage,
            "outcome": capture["manifest"]["outcome"], "problem_file": "problem.md",
            "draft_file": capture["manifest"]["draft_file"],
            "input_manifest_file": "review_input_manifest.json",
            "record_evidence_file": "cell_record_evidence.json",
            "evidence_files": [name for name in capture["files"]
                               if name not in {"problem.md", capture["manifest"]["draft_file"]}], **details}


def _prepare_workspace(work: Path, capture: dict, request: dict) -> Path:
    work.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(RESOURCES / "AGENTS.md", work / "AGENTS.md")
    from colombo.cell.instructions import pack_for_mode
    pack = pack_for_mode(capture["manifest"]["cell_mode"]) if "cell_mode" in capture["manifest"] else None
    if pack and pack["review_file"]:
        with (work / "AGENTS.md").open("a", encoding="utf-8") as handle:
            handle.write("\n\nThis is the " + pack["label"] + " Cell review. Read input/" + pack["review_file"] +
                         " as scoped reviewer guidance before checking this proof or its review report. "
                         "Apply only requirements relevant to the submitted Claim; do not expand its assigned scope.\n")
    shutil.copytree(RESOURCES / ".agents", work / ".agents", dirs_exist_ok=True)
    from colombo.cell.recovery import install_handoff_skill
    install_handoff_skill(work)
    context = work / "prior_record_trust.json"
    if context.exists() and context.read_bytes() != capture["trust_context"]:
        raise ValueError("Frozen prior trust context changed")
    _save_bytes(context, capture["trust_context"])
    _save(work / "review_input_manifest.json", capture["manifest"])
    for name, content in capture["files"].items():
        target = work / "input" / name
        if target.exists() and target.read_bytes() != content:
            raise ValueError("Frozen workspace inputs changed")
        if not target.exists():
            _save_bytes(target, content)
    _save(work / "review_request.json", request)
    schema = CONFIRMATION_RECEIPT_SCHEMA if request["stage"] == "report_check" else RECEIPT_SCHEMA
    _save(work / "receipt.schema.json", schema)
    return work


def _workspace(folder: Path, capture: dict) -> Path:
    _save(folder / "snapshot.json", capture["manifest"])
    for name, content in capture["files"].items():
        _save_bytes(folder / "input" / name, content)
    _save_bytes(folder / "prior_record_trust.json", capture["trust_context"])
    return _prepare_workspace(folder / "workspace", capture, _request(folder.name, capture))


def _launch_review(work: Path, settings: dict) -> dict:
    from colombo.cell.model_calls import run_agent
    request = _load(work / "review_request.json")
    checking = request["stage"] == "report_check"
    skill = "check-report" if checking else "review-proof"
    tool = "write_confirmation" if checking else "write_report"
    return run_agent(
        f"Continue the {request['stage']} stage in review_request.json using AGENTS.md and {skill}. "
        f"Review identity: review_id={request['review_id']}, report_revision={request['report_revision']}. "
        "For file or record identity, use the saved IDs, revisions, frozen paths and necessary direct body comparisons; "
        "do not compute or attach content hashes, digests or fingerprints. This restriction concerns material "
        "bookkeeping, not hash functions that are themselves part of the mathematical problem. "
        "Read saved notes and the latest handoff when present. Save progress before the closing window; "
        f"use finish_handoff when unfinished. Otherwise return the {tool} receipt as final JSON.",
        work, work / "final_response.json", role="verifier",
        timeout=settings["agents"]["report_check_timeout_seconds" if checking else "verifier_timeout_seconds"],
        model=settings["model"]["name"] or None, settings=settings, schema=work / "receipt.schema.json")


def _receipt(result, *, checking: bool, review_id: str, report_revision: int) -> dict:
    if isinstance(result, dict):
        if result.get("returncode", 0) != 0:
            raise ValueError("Reviewer process did not exit successfully")
        raw = result.get("text", "")
    else:
        raw = result
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("Reviewer returned no final receipt")
    validate = validate_confirmation_receipt if checking else validate_receipt
    receipt = validate(json.loads(raw))
    if receipt["review_id"] != review_id or receipt["report_revision"] != report_revision:
        raise ValueError("Receipt does not match the fixed review inputs")
    return receipt


def _collect_report(work: Path, result, *, review_id: str, report_revision: int) -> dict:
    receipt = _receipt(result, checking=False, review_id=review_id, report_revision=report_revision)
    data = (work / "review_report.json").read_bytes()
    report = validate_report(json.loads(data))
    if receipt["verdict"] != report["verdict"]:
        raise ValueError("Receipt does not match the saved first report")
    validate_report_notes(report, _load(work / "review_notes.json"))
    return report


def _collect_confirmation(work: Path, result, item: dict, report: dict) -> dict:
    receipt = _receipt(result, checking=True, review_id=item["id"], report_revision=item["report_revision"])
    data = (work / "confirmation.json").read_bytes()
    confirmation = validate_confirmation(json.loads(data), report, review_id=item["id"],
                                         report_revision=item["report_revision"])
    if receipt["verdict"] != confirmation["verdict"]:
        raise ValueError("Receipt does not match the saved independent assessment")
    return confirmation


def _unchanged(root: Path, capture: dict, work: Path, request: dict) -> None:
    if not json_equal(_load(work / "review_request.json"), request):
        raise ValueError("Reviewer changed its request")
    if not _same_submission(_capture(root, _load(root / "submission.json")), _review_dir(root, request["review_id"])):
        raise ValueError("The current draft or record mapping changed during review")


def _validate_refs(report: dict, capture: dict) -> None:
    refs = capture["manifest"]["record_refs"]
    frozen = json.loads(capture["files"]["cell_record_evidence.json"])
    for finding in report["findings"]:
        if finding.get("scope") == "record" and any(ref.get("kind") not in {"arguments", "examples"}
                                                   for ref in finding.get("affected_refs", [])):
            raise ValueError("Record-level trust findings require arguments or examples")
        for affected in finding.get("affected_refs", []):
            matches = [ref for ref in refs if all(ref.get(key) == affected.get(key)
                       for key in ("kind", "id", "revision"))]
            if affected.get("position"):
                matches = [ref for ref in matches if ref["position"] == affected["position"]]
            if not matches:
                raise ValueError("A finding targets a record not bound to this submission")
            if affected.get("property_ids"):
                record = next(row for row in frozen if all(row.get(key) == affected.get(key)
                              for key in ("kind", "id", "revision")))
                actual = {prop["id"] for prop in record["payload"].get("properties", [])}
                if affected["kind"] != "examples" or not set(affected["property_ids"]) <= actual:
                    raise ValueError("A finding targets nonexistent example properties")
            if affected.get("property_ids") and not any(
                not ref.get("property_ids") or set(affected["property_ids"]) <= set(ref["property_ids"])
                for ref in matches):
                raise ValueError("A finding targets properties outside the submitted selection")


def _check_current_support(root: Path, capture: dict) -> None:
    from colombo.cell.record_store import Store
    for row in Store(root / "memory").evidence_bundle(capture["manifest"]["record_refs"])["records"]:
        trust = row.get("current_trust", {})
        if row["kind"] == "examples":
            selected = row.get("property_ids", list(trust.get("properties", {})))
            unusable = any(trust.get("properties", {}).get(key, {}).get("state")
                           in {"withdrawn", "suspended", "dependency_blocked"} for key in selected)
        else:
            unusable = trust.get("state") in {"withdrawn", "suspended", "dependency_blocked"} or (
                row["kind"] == "experiment_result" and trust.get("state") != "computational_evidence")
        if unusable:
            raise _SupportChanged("Publication references suspended, withdrawn or dependency-blocked support")


class _SupportChanged(ValueError):
    pass


def _publish(root: Path, capture: dict, receipt: dict) -> dict:
    _save_bytes(root / "manuscript.md", (_review_dir(root, receipt["id"]) / "manuscript.md").read_bytes())
    return _set_status(root, "accepted", "The draft passed review and independent report checking.",
                       review_id=receipt["id"])


def _defer(root: Path, index: dict, item: dict, reason: str, *, exhausted: bool = False) -> dict:
    item["status"] = "review_incomplete" if exhausted else "pending_review"
    item["reason"] = reason
    _persist(root, index)
    return _set_status(root, item["status"], reason, review_id=item["id"], review_stage=item["phase"])


def _synchronize(root: Path, capture: dict, item: dict, folder: Path) -> dict:
    report = validate_report(_load(folder / "report.json"))
    confirmation = validate_confirmation(_load(folder / "confirmation.json"), report,
        review_id=item["id"], report_revision=item["report_revision"])
    if confirmation["verdict"] != "confirmed":
        raise ValueError("Unconfirmed review cannot be synchronized")
    from colombo.cell.record_store import Store
    result = Store(root / "memory").apply_confirmed_review(
        review_id=item["id"], report_revision=item["report_revision"], report=report, confirmation=confirmation,
        record_refs=capture["manifest"]["record_refs"], report_path=folder / "reports" / f"p{item['report_revision']:04d}.json",
        confirmation_path=folder / "checks" / f"p{item['report_revision']:04d}" / "confirmation.json")
    item["trust_synced"] = True
    item["trust_update"] = result
    return report


def _review_locked(root: Path, reviewer: Callable | None, report_checker: Callable | None) -> dict:
    if not (root / "submission.json").exists():
        (root / "manuscript.md").unlink(missing_ok=True)
        return {"status": "review_incomplete" if has_pending_review(root) else "pending",
                "reason": "No submission.json is available."}
    submission = _load(root / "submission.json")
    pending = has_pending_review(root)
    # Submitted inputs take precedence over cleanup, even when they incorrectly
    # name the reserved publication or a hard-link/symlink alias of it.
    try:
        _protect_inputs(root, submission)
    except (OSError, ValueError, TypeError) as exc:
        return _set_status(root, "review_incomplete" if pending else "needs_revision",
                           f"Invalid review inputs: {exc}")
    if submission.get("status") == "accepted" and manuscript_is_current(root):
        return {"status": "accepted", "reason": "The current manuscript has a confirmed review."}
    (root / "manuscript.md").unlink(missing_ok=True)
    if submission.get("status") == "accepted" and not pending:
        return _set_status(root, "needs_revision", "Acceptance is outdated or changed; resubmit status=ready for the current protocol.")
    if submission.get("status") not in {"ready", "pending_review", "review_incomplete"} and not pending:
        return {"status": submission.get("status", "pending"), "reason": "No ready submission."}
    try:
        capture = _capture(root, submission)
    except (OSError, ValueError, TypeError) as exc:
        return _set_status(root, "review_incomplete" if pending else "needs_revision", f"Invalid review inputs: {exc}")
    index = _index(root)
    if index["attempts"]:
        original = _review_dir(root, index["attempts"][0]["id"]) / "input" / "problem.md"
        if original.read_bytes() != capture["files"]["problem.md"]:
            return _set_status(root, "review_incomplete", "The original problem changed; restore the original task.")
    active = [item for item in index["attempts"] if item.get("protocol") == REVIEW_PROTOCOL
              and item.get("phase") != "complete"]
    if active:
        item = active[-1]
        if not _same_submission(capture, _review_dir(root, item["id"])):
            return _defer(root, index, item, "An unfinished review's frozen submission changed; restore it before resuming.", exhausted=True)
    else:
        prior = _valid_receipt(root, capture, index)
        if prior:
            return _publish(root, capture, prior)
        rejected = next((old for old in index["attempts"] if old.get("protocol") == REVIEW_PROTOCOL
                        and _same_submission(capture, _review_dir(root, old["id"])) and old.get("status") == "revise"), None)
        if rejected:
            return _set_status(root, "needs_revision", "This exact draft has confirmed defects; revise it before resubmitting.", review_id=rejected["id"],
                primary_launches_remaining=max(0, effective_limit(root, "verifier", capture["settings"]["agents"]["verifier_max_rounds"]) - index["primary_launches"]))
        if index["primary_launches"] >= effective_limit(root, "verifier", capture["settings"]["agents"]["verifier_max_rounds"]):
            _persist(root, index)
            return _set_status(root, "review_incomplete", "The cumulative primary verifier budget is exhausted.")
        item = {"id": f"r{len(index['attempts']) + 1:04d}",
                "protocol": REVIEW_PROTOCOL, "status": "pending_review",
                "phase": "proof", "report_revision": 0, "check_attempts": {}, "launches": []}
        index["attempts"].append(item)
        _persist(root, index)
        _workspace(_review_dir(root, item["id"]), capture)
    folder = _review_dir(root, item["id"])
    capture["trust_context"] = (folder / "prior_record_trust.json").read_bytes()
    settings = capture["settings"]
    while True:
        phase = item["phase"]
        if phase == "sync":
            try:
                if not _same_submission(_capture(root, _load(root / "submission.json")), folder):
                    raise ValueError("The submission changed before synchronizing confirmed findings")
                report = validate_report(_load(folder / "report.json"))
                if report["verdict"] == "pass":
                    _check_current_support(root, capture)
                report = _synchronize(root, capture, item, folder)
                if report["verdict"] == "pass":
                    header = (f"# Mathematical manuscript\n\nOutcome: {capture['manifest']['outcome']}\n"
                              f"Review: {item['id']}, report revision {item['report_revision']}\n"
                              "Original responsibility: problem.md (retained in the frozen review inputs).\n\n")
                    _save_bytes(folder / "manuscript.md", header.encode("utf-8") +
                                capture["files"][capture["manifest"]["draft_file"]])
                item.update(phase="complete", status="accepted" if report["verdict"] == "pass" else report["verdict"])
                _persist(root, index)
                if item["status"] == "accepted":
                    return _publish(root, capture, item)
                return _set_status(root, "needs_revision",
                    f"Read reviews/{item['id']}/report.json, independently confirmed and synchronized with record trust.",
                    review_id=item["id"],
                    primary_launches_remaining=max(0, effective_limit(root, "verifier", settings["agents"]["verifier_max_rounds"]) - index["primary_launches"]))
            except _SupportChanged as exc:
                from colombo.cell.record_store import Store
                _save(folder / "workspace" / "internal" / "report_check.json", {
                    "reason": str(exc), "instruction": "Reassess the report against currently unusable support; distinguish pending objections from confirmed errors and record the exact issue or unresolved repair. Do not modify frozen input.",
                    "current_records": Store(root / "memory").resolve_record_refs(capture["manifest"]["record_refs"])})
                item.update(phase="proof", correction_pending=True)
                _persist(root, index)
                continue
            except Exception as exc:
                # A store failure is not a mathematical criticism and cannot send
                # the prover ahead with stale approvals. Restart retries sync only.
                return _defer(root, index, item, f"Confirmed review awaits trust synchronization: {type(exc).__name__}: {exc}", exhausted=True)
        checking = phase == "report_check"
        from colombo.shared.runtime_budget import inherited_deadline
        from colombo.shared.runtime_budget import BudgetExhausted
        try:
            inherited_deadline(root, phase="work")
        except BudgetExhausted as exc:
            return _defer(root, index, item, str(exc), exhausted=True)
        if not checking and index["primary_launches"] >= effective_limit(root, "verifier", settings["agents"]["verifier_max_rounds"]):
            return _defer(root, index, item, "Verifier process budget exhausted; unfinished audit remains with Verifier.", exhausted=True)
        if checking and item["check_attempts"].get(str(item["report_revision"]), 0) >= settings["agents"]["report_check_max_attempts"]:
            return _defer(root, index, item, "Independent checker budget exhausted for this exact report; no provisional feedback is released.", exhausted=True)
        launch = None
        try:
            if checking:
                request = _request(item["id"], capture, stage="report_check", report_revision=item["report_revision"])
                work = _prepare_workspace(folder / "checks" / f"p{item['report_revision']:04d}" / "workspace", capture, request)
                first_bytes = (folder / "reports" / f"p{item['report_revision']:04d}.json").read_bytes()
                target = work / "first_report.json"
                if target.exists() and target.read_bytes() != first_bytes:
                    raise ValueError("Checker changed its frozen first report")
                _save_bytes(target, first_bytes)
                item["check_attempts"][str(item["report_revision"])] = item["check_attempts"].get(str(item["report_revision"]), 0) + 1
                callback = report_checker
            else:
                details = {"correction_file": "internal/report_check.json"} if item.get("correction_pending") else {}
                request = _request(item["id"], capture, report_revision=item["report_revision"] + 1, **details)
                work = _prepare_workspace(folder / "workspace", capture, request)
                index["primary_launches"] += 1
                callback = reviewer
            # A subsequent process must issue its own receipt. Partial notes are
            # preserved, but stopped processes cannot silently complete review.
            for stale in ("final_response.json", "confirmation.json" if checking else "review_report.json"):
                (work / stale).unlink(missing_ok=True)
            launch = {"stage": phase, "number": len(item["launches"]) + 1, "status": "running"}
            item["launches"].append(launch)
            _persist(root, index)  # Charge before dispatch: a crash cannot reset budgets.
            result = callback(work) if callback else _launch_review(work, settings)
            if isinstance(result, dict) and result.get("execution_status") == "handoff":
                launch.update(status="handoff", handoff_path=result.get("handoff_path"))
                return _defer(root, index, item, "Saved handoff continues in the next verifier at the same stage.")
            _unchanged(root, capture, work, request)
            if checking:
                if (work / "first_report.json").read_bytes() != first_bytes:
                    raise ValueError("Checker modified the first report")
                report = validate_report(json.loads(first_bytes))
                confirmation = _collect_confirmation(work, result, item, report)
                evidence = folder / "checks" / f"p{item['report_revision']:04d}" / "confirmation.json"
                _save(evidence, confirmation)
                launch["status"] = confirmation["verdict"]
                if confirmation["verdict"] == "needs_correction":
                    _save(folder / "workspace" / "internal" / "report_check.json", confirmation)
                    item.update(phase="proof", correction_pending=True)
                else:
                    _save_bytes(folder / "report.json", first_bytes)
                    _save_bytes(folder / "confirmation.json", evidence.read_bytes())
                    item["phase"] = "sync"
            else:
                report = _collect_report(work, result, review_id=item["id"], report_revision=item["report_revision"] + 1)
                _validate_refs(report, capture)
                item["report_revision"] += 1
                target = folder / "reports" / f"p{item['report_revision']:04d}.json"
                _save(target, report)
                if item.get("correction_pending") and json_equal(report, _load(folder / "reports" / f"p{item['report_revision']-1:04d}.json")):
                    raise ValueError("Correction must resolve or explicitly address the independent objections in a revised report")
                item.update(phase="report_check", correction_pending=False)
                launch["status"] = "report_saved"
            _persist(root, index)
        except Exception as exc:
            if launch is not None and launch.get("status") == "running":
                launch.update(status="handoff" if isinstance(exc, TimeoutError) else "execution_error",
                              reason=f"{type(exc).__name__}: {exc}")
                if getattr(exc, "handoff_path", None):
                    launch["handoff_path"] = str(exc.handoff_path)
            _save(folder / "error.json", {"stage": phase, "error": f"{type(exc).__name__}: {exc}"})
            exhausted = launch is None or (index["primary_launches"] >= effective_limit(root, "verifier", settings["agents"]["verifier_max_rounds"]) if not checking
                         else item["check_attempts"].get(str(item["report_revision"]), 0) >= settings["agents"]["report_check_max_attempts"])
            return _defer(root, index, item, "The verifier stage needs continuation; see its handoff and internal error record.", exhausted=exhausted)

class _ReviewBusy(Exception):
    pass


@contextmanager
def _exclusive_review(path: Path):
    with ExitStack() as stack:
        try:
            stack.enter_context(file_lock(path, timeout=0))
        except TimeoutError as exc:
            raise _ReviewBusy from exc
        yield


def review_submission(run_dir: Path, reviewer: Callable | None = None,
                      report_checker: Callable | None = None) -> dict:
    """Continue bounded audit stages; only a confirmed report reaches the prover."""
    root = Path(run_dir).resolve()
    if not root.is_dir():
        return {"status": "pending", "reason": "The task directory does not exist."}
    try:
        with _exclusive_review(root / ".review.lock"):
            return _review_locked(root, reviewer, report_checker)
    except _ReviewBusy:
        return {"status": "busy", "reason": "Another runner is reviewing this task."}
    except Exception as exc:
        return {"status": "error", "reason": f"Review could not complete: {type(exc).__name__}: {exc}"}
