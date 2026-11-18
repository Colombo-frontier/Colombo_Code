"""Validate structure, references, and scope only; Python does not determine mathematical truth."""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator
from .config import resources_root


class ProtocolError(ValueError):
    pass


class ValidationDiagnostics(ProtocolError):
    """Return complete, pageable deterministic diagnostics within the current tool session without starting another model job."""

    def __init__(self, errors: list[dict], report_ref: str, changes=()):
        self.diagnostics = errors
        self.report_ref = report_ref
        self.changes = list(changes)
        super().__init__(f"Artifact preflight found {len(errors)} errors; read /errors in {report_ref} with artifact_get and repair the current draft.")


def tool_error(exc: Exception) -> dict:
    """Responses and native MCP use the same error handoff format."""
    result = {"error_type": type(exc).__name__, "message": str(exc)[:5000], "recoverable": True}
    if isinstance(exc, ValidationDiagnostics):
        result.update(report_ref=exc.report_ref, error_count=len(exc.diagnostics),
                      diagnostics=exc.diagnostics[:8], normalization_changes=exc.changes[:8])
    return result


ROLE_KINDS = {
    "coordinator": {"plan"}, "task_scout": {"task_proposal"},
    "paper_scanner": {"paper_batch", "paper"},
    "extractor": {"extraction", "candidate"},
    "extraction_reviewer": {"review"}, "matcher": {"identity"},
    "identity_reviewer": {"review"},
    "bound_updater": {"research", "profile", "result", "proof"},
    "profile_researcher": {"research", "profile", "result", "proof"},
    "profile_reviewer": {"review"},
    "expansion_planner": {"expansion_plan"},
    "setting_expander": {"expansion", "candidate", "proof"},
    "expansion_reviewer": {"expansion_review"},
}
MAIN_KINDS = {r: next(iter(k)) for r, k in ROLE_KINDS.items() if len(k) == 1}
MAIN_KINDS.update(paper_scanner="paper_batch", extractor="extraction", bound_updater="research", profile_researcher="research", setting_expander="expansion")


@lru_cache(maxsize=64)
def schema(kind: str) -> dict:
    if not re.fullmatch(r"[a-z_]+", kind):
        raise ProtocolError("Invalid schema name")
    path = resources_root() / "schemas" / f"{kind}.schema.json"
    if not path.is_file():
        raise ProtocolError(f"Unknown artifact kind: {kind}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate(kind: str, data: object) -> None:
    errors = sorted(Draft202012Validator(schema(kind)).iter_errors(data), key=lambda e: str(e.path))
    if errors:
        lines = [f"/{'/'.join(str(p) for p in e.path)}: {e.message}" for e in errors[:16]]
        raise ProtocolError(f"{kind} output protocol error:\n" + "\n".join(lines))
    if kind == "profile":
        # This is context-free metadata validation only. Joint applicability,
        # retained-baseline evidence and research scope require the writer's
        # exact frozen context; never validate an update as a new profile here.
        from ..science.status import validate_status_taxonomy
        try:
            validate_status_taxonomy(data)
        except ValueError as exc:
            raise ProtocolError(str(exc)) from exc


def references(value: object) -> set[str]:
    if isinstance(value, str):
        return {value} if re.fullmatch(r"sha256:[0-9a-f]{64}", value) else set()
    if isinstance(value, dict):
        return set().union(*(references(x) for x in value.values())) if value else set()
    if isinstance(value, list):
        return set().union(*(references(x) for x in value)) if value else set()
    return set()


def resolve_pointer(data: object, pointer: str) -> object:
    if pointer == "":
        return data
    if not pointer.startswith("/"):
        raise ProtocolError("JSON Pointer must be empty or begin with /")
    node = data
    for part in pointer[1:].split("/"):
        if re.search(r"~(?![01])", part):
            raise ProtocolError("Invalid JSON Pointer escape")
        key = part.replace("~1", "/").replace("~0", "~")
        try:
            if isinstance(node, list):
                if not re.fullmatch(r"0|[1-9][0-9]*", key):
                    raise ValueError(key)
                node = node[int(key)]
            elif isinstance(node, dict):
                node = node[key]
            else:
                raise TypeError(key)
        except (KeyError, IndexError, ValueError, TypeError) as exc:
            raise ProtocolError(f"Pointer does not exist: {pointer}") from exc
    return node


def blocking(issues: list[dict], stage: str, subject: str | None = None) -> list[dict]:
    return [i for i in issues if stage in i.get("blocks", []) and
            (subject is None or not i.get("subject_refs") or subject in i["subject_refs"])]


def check_review(review: dict, subject_ref: str, review_type: str) -> None:
    validate("review", review)
    if review["subject_ref"] != subject_ref or review["review_type"] != review_type:
        raise ProtocolError("Review subject_ref/review_type does not match the fixed assignment")
    # Do not treat every unresolved issue as rejection; check only its declared blocker at the same stage.
    if review["verdict"] == "approve" and blocking(review["issues"], review_type, subject_ref):
        raise ProtocolError("approve contradicts a blocker for the same review subject and stage; retain the issue and correct verdict/scope")
    if review_type == "profile" and review["verdict"] == "approve" and blocking(review["issues"], "publication"):
        raise ProtocolError("approve contradicts a publication blocker")
    approved=set(review["approved_bound_ids"])
    for assessment in review["assessments"]:
        if assessment["subject_id"] in approved and assessment["verdict"]!="approve":
            raise ProtocolError("The assessment and approved_bound_ids contradict each other for the same bound")
    for issue in review["issues"]:
        if "bound" in issue["blocks"] and approved and (not issue["subject_refs"] or approved.intersection(issue["subject_refs"])):
            raise ProtocolError("approved_bound_ids includes a claim still subject to a bound blocker; the document may be approved while that bound remains quarantined")

