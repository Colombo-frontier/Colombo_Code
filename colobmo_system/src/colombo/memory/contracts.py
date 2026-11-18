"""Structural contracts. These checks do NOT prove scientific claims."""
from __future__ import annotations
import hashlib
import json
import re
from typing import Any

SCHEMA = "colombo-scientific-memory/2"
LIBRARIES = {"algorithm": "algorithm_family_library", "hard_family": "hard_family_library",
             "theorem": "theorem_library", "proof_method": "theorem_library", "source": "source"}
AXES = {"TASK", "MODEL", "ORACLE", "ALGORITHMS", "OUTPUT", "METRIC", "GUARANTEE", "RESOURCE"}
ROLES = {"describes", "requires", "covers", "concludes", "limits"}
STATES = {"asserted", "unknown", "not_assumed", "not_applicable", "negated"}
TAG_GROUPS = {"goal", "mechanism", "bottleneck", "proof_method"}
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}\Z")

class ContractError(ValueError):
    pass

def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")

def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def safe_id(value: str) -> str:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ContractError(f"Unsafe identifier: {value!r}")
    return value

def resolve_pointer(document: Any, pointer: str) -> Any:
    if pointer in ("", "#"):
        return document
    if not isinstance(pointer, str) or not pointer.startswith("#/"):
        raise ContractError(f"Expected local JSON Pointer, got {pointer!r}")
    obj = document
    try:
        for raw in pointer[2:].split("/"):
            if re.search(r"~(?![01])", raw):
                raise KeyError("invalid escape")
            key = raw.replace("~1", "/").replace("~0", "~")
            if isinstance(obj, list):
                if not re.fullmatch(r"0|[1-9][0-9]*", key):
                    raise KeyError("invalid array index")
                obj = obj[int(key)]
            else:
                obj = obj[key]
        return obj
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise ContractError(f"Unresolved pointer: {pointer}") from exc

def _require(obj: dict, keys: tuple[str, ...], where: str) -> None:
    if not isinstance(obj, dict):
        raise ContractError(f"{where}: an object required")
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ContractError(f"{where}: missing {missing}")

def _array(value: Any, where: str) -> None:
    if not isinstance(value, list):
        raise ContractError(f"{where}: an array required")

def _text(value: Any, where: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{where}: nonempty text required")

def dependencies(record: dict) -> list[tuple[str, int | None]]:
    result = [(s["source_id"], s.get("source_revision")) for s in record["source_refs"]]
    for link in record.get("links", []):
        if link["relation"] in {"depends_on", "performance", "model_membership", "proves", "uses"}:
            result.append((link["target_id"], link.get("target_revision")))
    return result

def validate_record(record: dict, *, require_revision: bool = False) -> None:
    if not isinstance(record, dict):
        raise ContractError("A record must be an object")
    _require(record, ("schema", "id", "revision", "kind", "title", "aliases", "summary",
                     "use_when", "content", "navigation", "source_refs", "links", "evidence"), "record")
    if record["schema"] != SCHEMA or record["kind"] not in LIBRARIES:
        raise ContractError("Unsupported schema/kind; legacy records need an explicit adapter")
    safe_id(record["id"])
    rev = record["revision"]
    if rev is not None and (type(rev) is not int or rev < 1):
        raise ContractError("revision must be null or a positive integer")
    if require_revision and rev is None:
        raise ContractError("A prepared/published record needs a revision")
    for k in ("title", "summary"):
        _text(record[k], k)
    for k in ("aliases", "use_when", "source_refs", "links"):
        if not isinstance(record[k], list):
            raise ContractError(f"{k} must be an array")
    for k in ("content", "navigation", "evidence"):
        if not isinstance(record[k], dict):
            raise ContractError(f"{k} must be an object")
    e = record["evidence"]
    _require(e, ("basis", "readiness", "statement_complete", "checked_locators", "unresolved", "use_restrictions"), "evidence")
    if e["basis"] not in {"reading_lead", "source_statement", "atlas_reported", "local_argument", "conjectural"}:
        raise ContractError("Unknown evidence basis")
    if e["readiness"] not in {"lead", "reference"} or type(e["statement_complete"]) is not bool:
        raise ContractError("Invalid readiness/statement_complete")
    for k in ("checked_locators", "unresolved", "use_restrictions"):
        if not isinstance(e[k], list):
            raise ContractError(f"evidence.{k} must be an array")
    nav = record["navigation"]
    _require(nav, ("facets", "research_use", "query_aliases"), "navigation")
    for key in ("facets", "research_use", "query_aliases"):
        _array(nav[key], "navigation." + key)
    for facet in nav["facets"]:
        _require(facet, ("axis", "concept_id", "role", "subject", "scope_ref", "evidence_refs", "state"), "facet")
        _array(facet["evidence_refs"], "facet.evidence_refs")
        if facet["axis"] not in AXES or facet["role"] not in ROLES or facet["state"] not in STATES:
            raise ContractError("Invalid facet axis/role/state")
        _text(facet["concept_id"], "facet.concept_id")
        _text(facet["subject"], "facet.subject")
        resolve_pointer(record, facet["scope_ref"])
        if facet["state"] in {"asserted", "negated"} and not facet["evidence_refs"]:
            raise ContractError("Asserted/negated facets need evidence pointers")
        for ref in facet["evidence_refs"]:
            resolve_pointer(record, ref)
    for tag in nav["research_use"]:
        _require(tag, ("group", "concept_id", "reason", "scope_ref"), "research_use")
        if tag["group"] not in TAG_GROUPS:
            raise ContractError("Unknown research-use group")
        resolve_pointer(record, tag["scope_ref"])
        _text(tag["reason"], "research-use reason")
    for src in record["source_refs"]:
        _require(src, ("source_id", "source_revision", "source_version", "locator"), "source_ref")
        safe_id(src["source_id"])
        if src["source_revision"] is not None and (type(src["source_revision"]) is not int or src["source_revision"] < 1):
            raise ContractError("source_revision must be null or a positive integer")
        _text(src["locator"], "source locator")
    for link in record["links"]:
        _require(link, ("relation", "target_id", "target_revision", "scope_ref", "note"), "link")
        safe_id(link["target_id"])
        resolve_pointer(record, link["scope_ref"])
        if link["target_revision"] is not None and (type(link["target_revision"]) is not int or link["target_revision"] < 1):
            raise ContractError("target_revision must be null or a positive integer")
    if e["readiness"] == "reference":
        _validate_reference(record)

def _validate_reference(r: dict) -> None:
    c, e = r["content"], r["evidence"]
    if e["basis"] in {"reading_lead", "conjectural", "atlas_reported"}:
        raise ContractError("Leads, conjectures and inherited Atlas reports are not ready references")
    if not r["source_refs"] and e["basis"] != "local_argument" and r["kind"] != "source":
        raise ContractError("A literature reference requires a source")
    for src in r["source_refs"]:
        if not src["source_version"] or src["source_version"] == "unknown":
            raise ContractError("Reference requires a pinned source version")
    if e["basis"] == "source_statement" and not e["checked_locators"]:
        raise ContractError("Source-statement references need actual checked locators")
    kind = r["kind"]
    if kind == "theorem":
        if not e["statement_complete"]:
            raise ContractError("Incomplete statement cannot be a reference theorem")
        _require(c, ("claim_type", "statement", "complexity_scope", "proofs", "application_guidance"), "theorem")
        _array(c["proofs"], "theorem.content.proofs")
        for index, proof in enumerate(c["proofs"]):
            _require(proof, (), f"theorem.content.proofs[{index}]")
        _require(c["statement"], ("objects_and_definitions", "assumptions", "quantifiers_and_randomness", "parameter_domains", "conclusion"), "statement")
        for k in ("objects_and_definitions", "quantifiers_and_randomness", "parameter_domains", "conclusion"):
            _text(c["statement"][k], "statement." + k)
        if c["claim_type"] == "performance" and not isinstance(c["complexity_scope"], dict):
            raise ContractError("Performance theorem requires complexity_scope")
        if isinstance(c["complexity_scope"], dict):
            _require(c["complexity_scope"], ("upper_witness_or_lower_coverage", "oracle", "output_and_metric", "guarantee", "resource", "regime", "hidden_constants"), "complexity_scope")
        if e["basis"] == "local_argument" and not any(p.get("kind") == "local_complete" and p.get("full_local_argument") for p in c["proofs"]):
            raise ContractError("A local theorem needs a complete local argument")
    elif kind == "algorithm":
        _require(c, ("family", "variants", "components", "performance_links", "limitations"), "algorithm")
        if not c["variants"]:
            raise ContractError("Algorithm needs at least one variant")
        for v in c["variants"]:
            _require(v, ("variant_id", "name", "public_inputs", "state_and_initialization", "requirements", "query_and_update", "tuning_and_stopping", "output", "cost"), "variant")
            for k in ("state_and_initialization", "requirements", "query_and_update", "output", "cost"):
                _text(v[k], "variant." + k)
    elif kind == "hard_family":
        _require(c, ("construction", "oracle_realizations", "hardness_claims", "components", "escape_conditions"), "hard_family")
        _require(c["construction"], ("definition", "parameters", "hidden_objects", "public_information", "model_membership_refs"), "construction")
        for key in ("definition", "parameters", "hidden_objects", "public_information"):
            _text(c["construction"][key], "construction." + key)
        if not c["oracle_realizations"]:
            raise ContractError("Hard family needs an explicit oracle realization")
        for oracle in c["oracle_realizations"]:
            _require(oracle, ("oracle_id", "query_and_feedback", "choices_and_history", "sampling_and_reuse", "cost", "information_bottleneck", "information_to_error", "supporting_claim_refs"), "oracle realization")
    elif kind == "source":
        _require(c, ("bibliographic_identity", "original_material", "necessary_context", "coverage"), "source")
        _require(c["bibliographic_identity"], ("title", "authors", "version", "canonical_url"), "source identity")
        for key in ("title", "version", "canonical_url"):
            _text(c["bibliographic_identity"][key], "source identity." + key)
        if c["bibliographic_identity"]["version"] == "unknown":
            raise ContractError("Source with unknown version remains a lead")
    elif kind == "proof_method":
        _require(c, ("goal_pattern", "required_inputs", "key_choice", "key_relation", "proof_skeleton", "transfer_obligations", "failure_modes", "worked_proof_refs"), "proof_method")
    for dep_id, revision in dependencies(r):
        if revision is None:
            raise ContractError(f"Scientific dependency {dep_id} is not revision-pinned")

def validate_review(proposal: dict, review: dict) -> None:
    _require(review, ("proposal_digest", "reviewer_run_id", "curator_run_id", "backend", "items", "coverage"), "review")
    _array(review["items"], "review.items")
    _array(review["coverage"], "review.coverage")
    if review["proposal_digest"] != proposal["digest"]:
        raise ContractError("Review is bound to a different proposal")
    if review["curator_run_id"] != proposal["curator_run_id"] or review["reviewer_run_id"] == proposal["curator_run_id"]:
        raise ContractError("Curator and Reviewer must be separate calls")
    records = {r["id"]: r for r in proposal["records"]}
    seen = set()
    for item in review["items"]:
        _require(item, ("id", "record_hash", "decision", "content_fidelity", "navigation_fidelity", "proof_review", "issues"), "review item")
        _array(item["issues"], "review item.issues")
        if item["id"] not in records or item["id"] in seen:
            raise ContractError("Unknown or duplicate review item")
        seen.add(item["id"])
        if item["record_hash"] != digest(records[item["id"]]):
            raise ContractError("Review record hash mismatch")
        if item["decision"] not in {"accept", "revise", "defer"}:
            raise ContractError("Unknown review decision")
        for issue in item["issues"]:
            _require(issue, ("category", "severity", "target", "reason", "impact", "repair", "evidence"), "review issue")
            if issue["severity"] not in {"blocker", "usage_restriction", "info"}:
                raise ContractError("Unknown issue severity")
            resolve_pointer(records[item["id"]], issue["target"])
        if item["decision"] == "accept":
            if records[item["id"]]["evidence"]["readiness"] != "reference":
                raise ContractError("Lead cannot be canonically published; complete/revise and reprepare before review")
            if item["content_fidelity"] != "checked" or item["navigation_fidelity"] != "checked":
                raise ContractError("Accept requires content and navigation fidelity checks")
            if any(i["severity"] == "blocker" for i in item["issues"]):
                raise ContractError("An accepted item cannot have an extraction blocker")
            if any(i["severity"] == "usage_restriction" for i in item["issues"]) and not records[item["id"]]["evidence"]["use_restrictions"]:
                raise ContractError("Accepted source ambiguities must be recorded as use restrictions")
            r = records[item["id"]]
            if r["evidence"]["basis"] == "local_argument" and r["kind"] == "theorem" and item["proof_review"] != "complete_local_argument_checked":
                raise ContractError("Local derivation requires review of its actual argument")
    # Missing objects are treated as deferred by the publisher, never accepted implicitly.
