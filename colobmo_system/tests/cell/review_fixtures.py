"""Explicit stage-aware mock receipts; no model process is launched here."""
from __future__ import annotations

import json


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _result(work, filename, payload):
    write(work / filename, payload)
    request = read(work / "review_request.json")
    receipt = {"review_id": request["review_id"], "report_revision": request["report_revision"],
               "verdict": payload["verdict"]}
    return {"returncode": 0, "text": json.dumps(receipt)}


def report_result(work, report):
    write(work / "review_notes.json", {key: report[key] for key in ("checks", "findings", "sources")})
    return _result(work, "review_report.json", report)


def confirmation(work, verdict="confirmed", mutate=None):
    request = read(work / "review_request.json")
    first = read(work / "first_report.json")
    payload = {"verdict": verdict, "review_id": request["review_id"],
        "report_revision": request["report_revision"],
        "summary": "Independent arithmetic and hypothesis checks support this report.",
        "assessment": {key: {"status": "supported", "reason": f"Independently checked {key}."}
                       for key in ("target_alignment", "coverage", "reasoning", "sources", "record_mapping")},
        "covered_check_ids": [row["id"] for row in first["checks"]],
        "findings": [{"finding_id": row["id"], "status": "supported", "reason": "Checked the exact criticized implication."}
                     for row in first["findings"]],
        "decisive_steps": [{"location": "draft.md", "status": "supported",
                            "reason": "Independently expanded the even and odd cases."}],
        "new_findings": []}
    if verdict == "needs_correction":
        payload["assessment"]["reasoning"] = {"status": "disputed", "reason": "The alleged error requires rechecking."}
    if mutate:
        mutate(payload)
    return payload


def confirmation_result(work, verdict="confirmed", mutate=None):
    return _result(work, "confirmation.json", confirmation(work, verdict, mutate))
