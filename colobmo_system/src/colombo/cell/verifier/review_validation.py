"""Validate review receipts, confirmation and fixed local audit conclusions."""

from __future__ import annotations
import json
import copy
from copy import deepcopy
from colombo.shared.file_io import Path
from jsonschema import Draft202012Validator


REPORT_SCHEMA = json.loads(
    (Path(__file__).resolve().parent / "schemas" / "report.schema.json")
    .read_text(encoding="utf-8")
)
RECEIPT_SCHEMA = json.loads(
    (Path(__file__).resolve().parent / "schemas" / "receipt.schema.json")
    .read_text(encoding="utf-8")
)
CONFIRMATION_SCHEMA = json.loads(
    (Path(__file__).resolve().parent / "schemas" / "confirmation.schema.json")
    .read_text(encoding="utf-8")
)
CONFIRMATION_RECEIPT_SCHEMA = deepcopy(RECEIPT_SCHEMA)
CONFIRMATION_RECEIPT_SCHEMA["properties"]["verdict"]["enum"] = ["confirmed", "needs_correction"]


def _shape(value: object, schema: dict) -> None:
    error = next(Draft202012Validator(schema).iter_errors(value), None)
    if error is not None:
        location = ".".join(str(part) for part in error.absolute_path) or "report"
        raise ValueError(f"{location}: {error.message}")


def _record(value: dict, kind: str) -> None:
    _shape(value, {"$defs": REPORT_SCHEMA["$defs"], "$ref": f"#/$defs/{kind}"})


def validate_receipt(payload: dict) -> dict:
    """Check receipt shape; the runner separately binds it to fixed inputs and report bytes."""
    _shape(payload, RECEIPT_SCHEMA)
    return payload


def validate_record_ref(value: dict, *, require_position: bool = False) -> None:
    schema = deepcopy(REPORT_SCHEMA["$defs"]["record_ref"])
    if require_position:
        schema["required"].append("position")
    _shape(value, schema)
    if "position" in value and not value["position"].strip():
        raise ValueError("Record reference position must locate its use in the draft")


def validate_confirmation_receipt(payload: dict) -> dict:
    _shape(payload, CONFIRMATION_RECEIPT_SCHEMA)
    return payload


def validate_confirmation(payload: dict, report: dict, *, review_id: str,
                          report_revision: int) -> dict:
    """Require independent support for the whole exact report, not only its verdict."""
    _shape(payload, CONFIRMATION_SCHEMA)
    validate_report(report)
    if payload["review_id"] != review_id or payload["report_revision"] != report_revision:
        raise ValueError("Confirmation does not bind the exact inputs and first report")
    if sorted(payload["covered_check_ids"]) != sorted(item["id"] for item in report["checks"]):
        raise ValueError("Confirmation must cover all first-report check IDs exactly once")
    ids = [item["finding_id"] for item in payload["findings"]]
    if sorted(ids) != sorted(item["id"] for item in report["findings"]):
        raise ValueError("Confirmation must assess each first-report finding exactly once")
    assessments = [*payload["assessment"].values(), *payload["findings"], *payload["decisive_steps"]]
    agreed = all(item["status"] == "supported" for item in assessments) and not payload["new_findings"]
    expected = "confirmed" if agreed else "needs_correction"
    if payload["verdict"] != expected:
        raise ValueError(f"Confirmation verdict must be {expected!r}")
    return payload


def validate_check(value: dict) -> None:
    _record(value, "check")


def validate_finding(value: dict) -> None:
    _record(value, "finding")
    if value["kind"] != "note" and not value["repair"].strip():
        raise ValueError("An error, gap, or uncertainty needs an actionable repair or verification request")
    if value.get("scope", "draft") == "record" and not value.get("affected_refs"):
        raise ValueError("A record finding requires exact affected_refs")


def validate_source(value: dict) -> None:
    _record(value, "source")


def validate_records(checks: list, findings: list, sources: list,
                     *, require_source_links: bool = False) -> None:
    """Check the consistency of complete or in-progress proof-specific records.

    Source records can be collected before the associated proof obligation is
    assessed. Their links become mandatory when the final report is submitted.
    """
    if not all(isinstance(items, list) for items in (checks, findings, sources)):
        raise ValueError("checks, findings, and sources must be lists")
    by_id = {}
    for check in checks:
        validate_check(check)
        if check["id"] in by_id:
            raise ValueError(f"Duplicate check {check['id']}")
        by_id[check["id"]] = check
    finding_ids = set()
    kinds_by_check = {key: set() for key in by_id}
    for finding in findings:
        validate_finding(finding)
        if finding["id"] in finding_ids:
            raise ValueError(f"Duplicate finding {finding['id']}")
        finding_ids.add(finding["id"])
        check = by_id.get(finding["check_id"])
        if check is None:
            raise ValueError(f"Finding {finding['id']} has no recorded check")
        kind, status = finding["kind"], check["status"]
        if kind in {"error", "gap"} and status != "fail":
            raise ValueError(f"Finding {finding['id']} requires a fail check")
        if kind == "uncertain" and status not in {"unresolved", "fail"}:
            raise ValueError(f"Finding {finding['id']} requires an unresolved or fail check")
        kinds_by_check[check["id"]].add(kind)
    for check_id, check in by_id.items():
        kinds = kinds_by_check[check_id]
        if check["status"] == "fail" and not kinds & {"error", "gap"}:
            raise ValueError(f"Failed check {check_id} needs an error or gap finding")
        if check["status"] == "unresolved" and "uncertain" not in kinds:
            raise ValueError(f"Unresolved check {check_id} needs an uncertain finding")
    source_keys = set()
    for source in sources:
        validate_source(source)
        key = (source["citation"], source["location"])
        if key in source_keys:
            raise ValueError(f"Duplicate source occurrence: {key}")
        source_keys.add(key)
        if not require_source_links:
            continue
        if source["check_id"] not in by_id:
            raise ValueError("A source must link to a recorded check")
        reference_kinds = kinds_by_check[source["check_id"]]
        if source["status"] == "mismatch" and not reference_kinds & {"error", "gap"}:
            raise ValueError("A mismatched source needs an error or gap in its linked check")
        if source["status"] == "unavailable" and "uncertain" not in reference_kinds:
            raise ValueError("An unavailable source needs an uncertain finding in its linked check")


def validate_report(payload: dict) -> dict:
    """Require explicit coverage and a verdict supported by the actual checks."""
    _shape(payload, REPORT_SCHEMA)
    checks, findings, sources = (payload[key] for key in ("checks", "findings", "sources"))
    validate_records(checks, findings, sources, require_source_links=True)
    failed = (any(check["status"] == "fail" for check in checks)
              or any(finding["kind"] in {"error", "gap"} for finding in findings)
              or any(source["status"] == "mismatch" for source in sources))
    uncertain = (any(check["status"] == "unresolved" for check in checks)
                 or any(finding["kind"] == "uncertain" for finding in findings)
                 or any(source["status"] == "unavailable" for source in sources))
    expected = "revise" if failed else "inconclusive" if uncertain else "pass"
    if payload["verdict"] != expected:
        raise ValueError(f"Verdict must be {expected!r} for these checks, findings, and sources")
    return payload


def validate_report_notes(report: dict, notes: dict) -> None:
    """Reject omissions or changes between the final report and its review notes."""
    validate_report(report)
    if not isinstance(notes, dict) or set(notes) != {"checks", "findings", "sources"}:
        raise ValueError("Review notes must contain checks, findings, and sources")
    validate_records(notes["checks"], notes["findings"], notes["sources"])
    orders = {"checks": lambda item: item["id"],
              "findings": lambda item: item["id"],
              "sources": lambda item: (item["citation"], item["location"])}
    for collection, order in orders.items():
        if sorted(report[collection], key=order) != sorted(notes[collection], key=order):
            raise ValueError("Report checks, findings, and sources must match all persisted review notes")


# Local audit conclusions

_REFERENCE_BASE = {
    "type": "object", "additionalProperties": False,
    "required": ["kind", "id", "revision"],
    "properties": {
        "kind": {"type": "string"}, "id": {"type": "string", "minLength": 1},
        "revision": {"type": "integer", "minimum": 1},
    },
}
_PROPERTY_REFERENCE = copy.deepcopy(_REFERENCE_BASE)
_PROPERTY_REFERENCE["required"].append("property_ids")
_PROPERTY_REFERENCE["properties"]["property_ids"] = {
    "type": "array", "minItems": 1,
    "items": {"type": "string", "minLength": 1},
}
# The CLI removes optional object fields before requesting structured output.
# Both reference shapes therefore have complete required-field lists.
REFERENCE_SCHEMA = {"anyOf": [_REFERENCE_BASE, _PROPERTY_REFERENCE]}

CONCLUSION_RESULT_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["target", "relation", "verdict", "reason"],
    "properties": {
        "target": REFERENCE_SCHEMA,
        "relation": {"type": "string", "enum": ["supports", "refutes"]},
        "verdict": {"type": "string", "enum": ["pass", "fail", "uncertain"]},
        "reason": {"type": "string", "minLength": 1},
    },
}

REGISTRATION_FINDINGS_SCHEMA = {
    "type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["source_ref", "location", "suggested_kind", "content", "reason"],
        "properties": {
            "source_ref": REFERENCE_SCHEMA,
            "location": {"type": "string", "minLength": 1},
            "suggested_kind": {"type": "string", "enum": ["claims", "examples"]},
            "content": {"type": "string", "minLength": 1},
            "reason": {"type": "string", "minLength": 1},
        },
    },
}


def conclusion_key(item: dict) -> str:
    """Treat property selection as a set, never infer mathematical equivalence."""
    target = copy.deepcopy(item["target"])
    if "property_ids" in target:
        if len(target["property_ids"]) != len(set(target["property_ids"])):
            raise ValueError("Repeated property IDs in an audit conclusion")
        target["property_ids"] = sorted(target["property_ids"])
    return json.dumps({"target": target, "relation": item["relation"]},
                      sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def validate_conclusion_results(expected: list[dict], results: list[dict],
                                overall_verdict: str) -> None:
    """Reject omitted, repeated, redirected or inconsistent audit conclusions.

    A service error carries no mathematical certification and may omit results.
    Otherwise every declared target and direction needs its own exact result.
    """
    from jsonschema import validate

    if not isinstance(expected, list) or not isinstance(results, list):
        raise ValueError("Audit conclusions must be lists")
    if overall_verdict == "service_error":
        if results:
            raise ValueError("A service error cannot certify conclusions")
        return
    if overall_verdict not in {"pass", "fail", "uncertain"}:
        raise ValueError("Invalid overall conclusion verdict")
    validate(results, {"type": "array", "items": CONCLUSION_RESULT_SCHEMA})
    expected_keys = [conclusion_key(item) for item in expected]
    received_keys = [conclusion_key(item) for item in results]
    if len(expected_keys) != len(set(expected_keys)) or \
            len(received_keys) != len(set(received_keys)) or set(received_keys) != set(expected_keys):
        raise ValueError("Audit did not cover exactly the declared conclusion targets and directions")
    if any(not item["reason"].strip() for item in results):
        raise ValueError("Audit conclusion reasons cannot be blank")
    if results:
        verdicts = {item["verdict"] for item in results}
        combined = "fail" if "fail" in verdicts else "uncertain" if "uncertain" in verdicts else "pass"
        if overall_verdict != combined:
            raise ValueError("Inconsistent overall argument verdict")
