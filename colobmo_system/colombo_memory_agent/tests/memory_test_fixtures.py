"""Synthetic records for import and migration tests; no historical job data."""
import json
from pathlib import Path


def candidate_records():
    package = Path(__file__).resolve().parents[1]
    text = (package / "examples/complete_candidate_records.json").read_text(encoding="utf-8")
    for record in json.loads(text):
        prefix, name = record["id"].split(".", 1)
        text = text.replace(record["id"], f"{prefix}.PTEST.{name}")
    records = json.loads(text)
    for record in records:
        record["revision"] = None
        record["evidence"]["readiness"] = "lead"
        record["aliases"].append("SPIDER synthetic transport fixture")
    return records
