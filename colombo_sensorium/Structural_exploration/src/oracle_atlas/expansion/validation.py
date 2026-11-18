"""Mechanical expansion handoff checks. Agents decide mathematical validity and identity."""
from __future__ import annotations

from ..atlas.bindings import normalize_tag_facts
from ..core.contracts import ProtocolError, blocking, resolve_pointer, validate
from .request import AXES
from .selection import select_opportunities


def checked_plan(data, inputs, artifacts):
    if data["request_ref"] != inputs["request_ref"] or data["neighborhood_ref"] != inputs["neighborhood_ref"]:
        raise ProtocolError("Expansion plan binds a different request or neighborhood")
    request = artifacts.get(inputs["request_ref"])["data"]
    neighborhood = artifacts.get(inputs["neighborhood_ref"])["data"]
    seeds = {s["setting_id"] for s in neighborhood["seeds"]}
    known_neighbors = seeds | {n["setting_id"] for s in neighborhood["seeds"] for n in s["neighbors"]}
    targets = set(neighborhood["target_task_ids"])
    for op in data["opportunities"]:
        if not set(op["seed_setting_ids"]).issubset(seeds):
            raise ProtocolError("Opportunity uses a seed outside this frozen discovery wave")
        if not set(op["neighbor_setting_ids"]).issubset(known_neighbors):
            raise ProtocolError("Opportunity references an undeclared neighborhood analogue")
        if not set(op["target_task_ids"]).issubset(targets):
            raise ProtocolError("Opportunity expands the authorized target tasks")
    return select_opportunities(data, {**request, "seed_setting_ids": sorted(seeds), "target_task_ids": sorted(targets)})


def checked_expansion(data, inputs, artifacts, job_id):
    for key in ("request_ref", "plan_ref", "opportunity_id"):
        if data[key] != inputs[key]:
            raise ProtocolError(f"Expansion binds a different {key}")
    candidate = artifacts.get(data["candidate_ref"])
    if candidate["kind"] != "candidate" or not artifacts.owned(data["candidate_ref"], job_id):
        raise ProtocolError("The current setting_expander must produce the frozen candidate")
    value = candidate["data"]
    origin = value.get("origin")
    validate("expansion_origin", origin)
    for key in ("request_ref", "plan_ref", "opportunity_id"):
        if origin[key] != inputs[key]:
            raise ProtocolError(f"Candidate provenance disagrees on {key}")
    if set(origin["seed_refs"]) != set(inputs["seed_refs"]):
        raise ProtocolError("Candidate provenance must retain the exact pinned seed snapshots")
    if {fact["axis"] for fact in value["tag_facts"]} != set(AXES):
        raise ProtocolError("All eight axes require scoped tags, including explicit unknown declarations")
    for fact in value["tag_facts"]:
        resolve_pointer(value, fact["source_pointer"])
    normalized = normalize_tag_facts(value, value["tag_facts"])
    if normalized["errors"] or normalized["changes"]:
        raise ProtocolError("Normalize actual candidate bindings through artifact_put/draft_freeze before handoff")
    request = artifacts.get(inputs["request_ref"])["data"]
    if not {c["axis"] for c in data["changes"]}.issubset(request["allowed_axes"]):
        raise ProtocolError("The completed specification changes an axis outside the request")
    plan = artifacts.get(inputs["plan_ref"])["data"]
    op = next(o for o in plan["opportunities"] if o["opportunity_id"] == data["opportunity_id"])
    if not {c["axis"] for c in data["changes"]}.issubset(op["changed_axes"]):
        raise ProtocolError("Unplanned specification-axis changes require a new opportunity, not silent scope expansion")
    tasks = value["common_specification"]["task"].get("navigation_domains", [])
    if not tasks or not set(tasks).issubset(op["target_task_ids"]):
        raise ProtocolError("Register the actual target tasks in task.navigation_domains within the selected opportunity")
    previous = inputs.get("previous_candidate_ref")
    if previous and value["candidate_id"] != artifacts.get(previous)["data"]["candidate_id"]:
        raise ProtocolError("A specification revision must preserve candidate_id")
    for paper_ref in value["paper_refs"]:
        if artifacts.get(paper_ref)["kind"] != "paper":
            raise ProtocolError("paper_refs may be empty; they may never impersonate seed snapshots")


def checked_review(data, inputs, artifacts, job_id):
    if data["subject_ref"] != inputs["subject_ref"] or data["candidate_ref"] != inputs["candidate_ref"]:
        raise ProtocolError("Expansion review does not bind the frozen expansion and candidate")
    if artifacts.owned(data["subject_ref"], job_id) or artifacts.owned(data["candidate_ref"], job_id):
        raise ProtocolError("An expansion producer cannot independently review its own artifact")
    expansion = artifacts.get(data["subject_ref"])["data"]
    if expansion["candidate_ref"] != data["candidate_ref"]:
        raise ProtocolError("The reviewed expansion contains another candidate")
    expected = set(inputs.get("peer_candidate_refs", []))
    compared = [row["candidate_ref"] for row in data["pending_comparisons"]]
    if set(compared) != expected or len(compared) != len(expected):
        raise ProtocolError("Review every supplied pending peer once; do not silently omit a duplicate risk")
    duplicate = data["duplicate_of_ref"]
    equivalents = {r["candidate_ref"] for r in data["pending_comparisons"] if r["relation"] == "equivalent"}
    unresolved = any(r["relation"] == "unresolved" for r in data["pending_comparisons"])
    if duplicate and (duplicate not in equivalents or data["verdict"] != "exclude"):
        raise ProtocolError("A merged duplicate must bind an equivalent peer and use exclude")
    if equivalents and not duplicate:
        raise ProtocolError("Record the equivalent pending candidate explicitly; do not research it twice")
    if data["verdict"] == "approve":
        if unresolved or data["required_changes"]:
            raise ProtocolError("Approve conflicts with unresolved peer identity or required specification repairs")
        if any(blocking(data["issues"], stage) for stage in ("expansion", "extraction", "identity")):
            raise ProtocolError("Approve conflicts with a candidate validity or identity blocker")
        if any(expansion["well_posedness"][key] != "supported" for key in ("nonempty", "objective_defined", "oracle_implementable", "not_trivial")):
            raise ProtocolError("An approved candidate requires supported well-posedness checks; retain unresolved designs as proposals")

