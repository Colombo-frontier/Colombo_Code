"""Cell record identity, directed evidence, trust and declared record references."""

from __future__ import annotations
import copy
from datetime import datetime, timezone
from uuid import uuid4
from colombo.cell.record_formats import OBLIGATION_WORK_STATUSES


METADATA = frozenset({"title", "notes", "description", "metadata", "sources", "source_refs",
                      "origin", "derived_from", "reformulates", "variant_of", "citation", "status", "tag",
                      "audit_id", "challenged_by"})

# Shared with the published archive schemas; omission means active without
# inserting a default into the caller's payload or request replay identity.


def core(payload: dict, *, example: bool = False) -> dict:
    """Only explicitly nonmathematical metadata can change under one identity."""
    excluded = METADATA | ({"properties", "dependencies", "evidence_refs", "evidence_files"} if example else set())
    return {key: value for key, value in payload.items() if key not in excluded}


def property_core(prop: dict) -> dict:
    # A new proof/dependency may repair the evidence for the same fixed property.
    return {key: value for key, value in prop.items()
            if key not in METADATA | {"basis", "proof", "dependencies", "evidence_refs"}}


def validate_identity(kind: str, old: dict | None, new: dict) -> None:
    from colombo.cell.record_store import StoreError
    from colombo.cell.record_store import json_equal
    if kind == "claims":
        if "proposition" in new and (not isinstance(new["proposition"], (str, dict)) or not new["proposition"]):
            raise StoreError("proposition must contain the fixed mathematical statement")
        if old is not None and not json_equal(core(old), core(new)):
            raise StoreError("Changed mathematical claim requires a new Claim ID")
    if kind == "examples" and old is not None:
        if not json_equal(core(old, example=True), core(new, example=True)):
            raise StoreError("Changed construction requires a new Example ID")
        before = {p["id"]: p for p in old.get("properties", [])}
        after = {p["id"]: p for p in new.get("properties", [])}
        if not before.keys() <= after.keys():
            raise StoreError("Keep existing properties; append a new property ID for a changed statement")
        for identifier, prop in before.items():
            if not json_equal(property_core(prop), property_core(after[identifier])):
                raise StoreError("Changed property statement requires a new property ID")
    if kind == "proof_state" and old is not None:
        old_routes = {route["route_id"]: route for route in old.get("routes", [])}
        for route in new.get("routes", []):
            previous = old_routes.get(route["route_id"])
            if previous is None:
                continue
            if previous["target_claim_ref"]["id"] != route["target_claim_ref"]["id"]:
                raise StoreError("A changed route target requires a new route_id")
            obligations = {o["id"]: o for o in previous.get("obligations", [])}
            for obligation in route.get("obligations", []):
                before = obligations.get(obligation["id"])
                if before and (before["target_claim_ref"]["id"] != obligation["target_claim_ref"]["id"] or
                               before.get("expected_relation", "supports") != obligation.get("expected_relation", "supports")):
                    raise StoreError("A changed obligation target/direction requires a new obligation ID")


def _fixed(store, reference: dict) -> dict:
    from colombo.cell.record_store import _ref
    record = store._resolve_ref(reference)
    ids = reference.get("property_ids", record.get("property_ids"))
    return {**_ref(record), **({"property_ids": list(ids)} if ids is not None else {})}


def prepare_links(store, kind: str, payload: dict) -> dict:
    """Freeze declared mathematical roles without searching arbitrary prose."""
    from colombo.cell.record_store import StoreError
    from colombo.cell.record_store import json_equal
    payload = copy.deepcopy(payload)
    if "conclusions" in payload:
        if kind != "arguments" or not isinstance(payload["conclusions"], list) or not payload["conclusions"]:
            raise StoreError("conclusions is a nonempty list on an Argument")
        seen = set()
        for conclusion in payload["conclusions"]:
            if not isinstance(conclusion, dict) or set(conclusion) != {"target", "relation"}:
                raise StoreError("Each conclusion needs only target and relation")
            ref = _fixed(store, conclusion["target"])
            relation = conclusion["relation"]
            if relation not in {"supports", "refutes"} or ref["kind"] not in {"claims", "examples"}:
                raise StoreError("Conclusions support/refute a Claim or support selected Example properties")
            if ref["kind"] == "examples" and (not ref.get("property_ids") or relation != "supports"):
                raise StoreError("Example conclusions support explicit property_ids; express negation as a Claim")
            key = (ref["kind"], ref["id"], ref["revision"], tuple(sorted(ref.get("property_ids", []))), relation)
            if key in seen:
                raise StoreError("Duplicate conclusion")
            seen.add(key)
            conclusion["target"] = ref
            for dependency in payload.get("dependencies", []):
                actual = store._resolve_ref(dependency)
                if (actual["kind"], actual["id"]) != (ref["kind"], ref["id"]):
                    continue
                if ref["kind"] == "claims" or set(dependency.get("property_ids", ref["property_ids"])) & set(ref["property_ids"]):
                    raise StoreError("A conclusion cannot also be its own premise")
    if "subject_refs" in payload:
        if not isinstance(payload["subject_refs"], list):
            raise StoreError("subject_refs must be a list")
        payload["subject_refs"] = [_fixed(store, ref) for ref in payload["subject_refs"]]
    if "citation" in payload:
        citation = payload["citation"]
        if kind != "claims" or not isinstance(citation, dict) or not isinstance(citation.get("locator"), str) or not citation["locator"].strip():
            raise StoreError("External citation needs a precise locator")
        refs = citation.get("source_refs")
        if not isinstance(refs, list) or not refs:
            raise StoreError("External citation needs fixed Source references")
        citation["source_refs"] = [_fixed(store, ref) for ref in refs]
        if any(ref["kind"] != "sources" for ref in citation["source_refs"]):
            raise StoreError("citation.source_refs must refer to sources")
    return payload


def object_refs(payload: dict) -> list[dict]:
    """Objects the auditor must read, without treating them as known premises."""
    return [row["target"] for row in payload.get("conclusions", [])] + list(payload.get("subject_refs", []))


def source_refs(payload: dict) -> list[dict]:
    return list(payload.get("citation", {}).get("source_refs", []))


def validate_workflow(store, kind: str, payload: dict) -> None:
    from colombo.cell.record_store import StoreError
    from colombo.cell.record_store import json_equal
    def reference(value, expected_kind=None):
        record = store._resolve_ref(value)
        if expected_kind and record["kind"] != expected_kind:
            raise StoreError(f"Expected a {expected_kind} reference")
    if kind == "proof_state" and "routes" in payload:
        if not isinstance(payload["routes"], list):
            raise StoreError("routes must be a list")
        route_ids = set()
        for route_index, route in enumerate(payload["routes"]):
            if not isinstance(route, dict) or not isinstance(route.get("route_id"), str) or not route["route_id"] or route["route_id"] in route_ids:
                raise StoreError("Routes need distinct nonempty route_id values")
            route_ids.add(route["route_id"])
            reference(route.get("target_claim_ref"), "claims")
            if not isinstance(route.get("obligations", []), list):
                raise StoreError("obligations must be a list")
            ids = set()
            for obligation_index, obligation in enumerate(route.get("obligations", [])):
                if not isinstance(obligation, dict) or not isinstance(obligation.get("id"), str) or not obligation["id"] or obligation["id"] in ids:
                    raise StoreError("Obligations need distinct stable ids within the route")
                ids.add(obligation["id"])
                reference(obligation.get("target_claim_ref"), "claims")
                if obligation.get("expected_relation", "supports") not in {"supports", "refutes"}:
                    raise StoreError("expected_relation must be supports or refutes")
                work_status = obligation.get("work_status", "active")
                if not isinstance(work_status, str) or work_status not in OBLIGATION_WORK_STATUSES:
                    raise StoreError(
                        f"proof_state.routes[{route_index}].obligations[{obligation_index}].work_status "
                        f"must be one of {', '.join(OBLIGATION_WORK_STATUSES)}; "
                        f"received {work_status!r}. Omit it to use active.")
                for field, target_kind in (("owner_attempt_ref", "attempts"), ("closing_argument_ref", "arguments")):
                    if obligation.get(field) is not None:
                        reference(obligation[field], target_kind)
                for ref in obligation.get("evidence_refs", []):
                    reference(ref)
                if {"mathematical_state", "satisfaction", "satisfied", "current_trust"} & obligation.keys():
                    raise StoreError("Obligation evidence state is service-derived")
    if kind == "attempts" and "experiment_decision" in payload:
        decision = payload["experiment_decision"]
        if not isinstance(decision, dict) or decision.get("decision") not in {"run", "defer", "not_useful"}:
            raise StoreError("experiment_decision needs run, defer or not_useful")
        reference(decision.get("target_ref"))
        required = {"run": ("question", "outcome_actions", "scope_and_stop"),
                    "defer": ("reason", "reconsider_on"), "not_useful": ("reason",)}[decision["decision"]]
        if any(not decision.get(field) for field in required):
            raise StoreError("Incomplete experiment decision for the selected branch")
        for ref in decision.get("experiment_refs", []):
            reference(ref, "experiment_result")
    if kind == "attempts" and "route_review" in payload:
        review = payload["route_review"]
        if not isinstance(review, dict) or not review.get("decision") or not review.get("reason"):
            raise StoreError("A route_review needs its decision and reason")
    if "complexity_profile" in payload and (kind != "arguments" or not isinstance(payload["complexity_profile"], dict)):
        raise StoreError("complexity_profile is an optional object on an Argument")


def obligation_view(store, state: dict) -> list[dict]:
    """A refuted required lemma blocks its route; it is not a satisfied premise."""
    from colombo.cell.record_store import _ref
    rows = []
    for route in state["payload"].get("routes", []):
        for obligation in route.get("obligations", []):
            claim = store._resolve_ref(obligation["target_claim_ref"])
            trust = store._assess(claim)
            mathematical = trust["state"]
            expected = obligation.get("expected_relation", "supports")
            wanted = "proved" if expected == "supports" else "refuted"
            opposite = "refuted" if expected == "supports" else "proved"
            satisfaction = "blocked" if mathematical in {opposite, "conflicted"} else "unresolved"
            closing = obligation.get("closing_argument_ref")
            closing_trust = None
            if closing:
                argument = store._resolve_ref(closing)
                closing_trust = store._assess(argument)
                relations = certified_relations(store, argument)
                if mathematical == wanted and closing_trust["state"] == "supported" and any(
                        c["relation"] == expected and _same_claim(store, c["target"], claim) for c in relations):
                    satisfaction = "satisfied"
            rows.append({**copy.deepcopy(obligation), "route_id": route["route_id"],
                         "proof_state_ref": _ref(state), "mathematical_state": mathematical,
                         "satisfaction": satisfaction, "closing_trust": closing_trust})
    return rows


def _same_claim(store, reference: dict, claim: dict) -> bool:
    if reference.get("kind") != "claims" or reference.get("id") != claim["id"]:
        return False
    try:
        return core(store._resolve_ref(reference)["payload"]) == core(claim["payload"])
    except (KeyError, ValueError):
        return False


def certified_relations(store, argument: dict) -> list[dict]:
    """Read only the exact scope explicitly covered by the argument's receipt."""
    from colombo.cell.verifier.review_validation import validate_conclusion_results
    payload = argument["payload"]
    expected = payload.get("conclusions", [])
    if not expected or not payload.get("audit_id"):
        return []
    try:
        review, reviewed = store._review_target(payload["audit_id"], "arguments", argument["id"])
        from colombo.cell.record_store import evidence_body
        from colombo.cell.record_store import json_equal
        if review["verdict"] != "pass" or not json_equal(evidence_body(payload), evidence_body(reviewed)):
            return []
        validate_conclusion_results(expected, review.get("conclusions", []), review["verdict"])
    except (KeyError, ValueError):
        return []
    return expected


def property_support(store, example: dict, prop: dict, visiting: set) -> list[dict]:
    from colombo.cell.record_store import _ref
    result, seen = [], set()
    for argument in reversed(store._collection("arguments")["records"] + store._context_records("arguments")):
        payload = argument["payload"]
        identity = (argument["id"], payload.get("audit_id"))
        if identity in seen or not (payload.get("status") == "proved" or payload.get("tag") == "proved"):
            continue
        seen.add(identity)
        for conclusion in payload.get("conclusions", []):
            ref = conclusion["target"]
            if ref["kind"] != "examples" or ref["id"] != example["id"] or prop["id"] not in ref.get("property_ids", []) or conclusion["relation"] != "supports":
                continue
            target = store._resolve_ref(ref)
            old = next((p for p in target["payload"].get("properties", []) if p["id"] == prop["id"]), None)
            if old is None or core(target["payload"], example=True) != core(example["payload"], example=True) or property_core(old) != property_core(prop):
                continue
            if store._assess(argument, visiting)["state"] != "supported":
                continue
            if argument.get("origin") != "context" and conclusion not in certified_relations(store, argument):
                continue
            result.append({"argument_ref": _ref(argument), "audited_target": ref})
    return result


def claim_trust(store, claim: dict, visiting: set) -> dict:
    from colombo.cell.record_store import _ref
    from colombo.cell.record_store import json_equal
    supports, refutes = [], []
    # Authorized parent trust is a frozen statement of its scope. Local child
    # evidence may add to it; no ancestor store is consulted to recompute it.
    inherited = claim.get("current_trust", {}) if claim.get("origin") == "context" else {}
    arguments = store._collection("arguments")["records"] + store._context_records("arguments")
    seen = set()
    for argument in reversed(arguments):
        payload = argument["payload"]
        identity = (argument["id"], payload.get("audit_id"))
        if identity in seen or not (payload.get("status") == "proved" or payload.get("tag") == "proved"):
            continue
        seen.add(identity)
        matching = [c for c in payload.get("conclusions", []) if _same_claim(store, c["target"], claim)]
        if not matching or store._assess(argument, visiting)["state"] != "supported":
            continue
        if argument.get("origin") != "context":
            covered = certified_relations(store, argument)
            matching = [c for c in matching if c in covered]
        for conclusion in matching:
            (supports if conclusion["relation"] == "supports" else refutes).append(
                {"argument_ref": _ref(argument), "audited_target": conclusion["target"]})
    def inherited_alive(side, states):
        if inherited.get("state") not in states:
            return False
        evidence = inherited.get(side, [])
        if not evidence:
            return True  # A frozen grant need not expose the parent's full proof.
        for item in evidence:
            try:
                argument = store._resolve_ref(item["argument_ref"])
            except KeyError:
                return True  # Do not traverse an ancestor to resolve it.
            if store._assess(argument, visiting)["state"] == "supported":
                return True
        return False
    has_support = bool(supports) or inherited_alive("supports", {"proved", "conflicted"})
    has_refutation = bool(refutes) or inherited_alive("refutes", {"refuted", "conflicted"})
    state = "conflicted" if has_support and has_refutation else "proved" if has_support else "refuted" if has_refutation else \
        "cited" if claim["payload"].get("citation") else "unresolved" if "proposition" in claim["payload"] else "recorded"
    return {"state": state,
            "supports": supports, "refutes": refutes,
            "citation_requires_application_check": state == "cited",
            "inherited_state": inherited.get("state"),
            "blockers": [{"reason": "conflicting_certified_evidence"}] if state == "conflicted" else []}


def archive_result(store, records: list[dict], request_id: str) -> dict:
    """Stage an entire related result in memory, then commit it once."""
    from colombo.cell.record_store import StoreError
    from colombo.cell.record_store import RevisionConflict
    from colombo.cell.record_store import _kind
    from colombo.cell.record_store import _ref
    from colombo.cell.record_store import json_equal
    from colombo.cell.record_store import _json
    store._request_id(request_id)
    if not request_id or not isinstance(records, list) or not records:
        raise StoreError("archive_result requires records and a stable request_id")
    if len(records) > store.settings["retrieval"]["max_memory_results"]:
        raise StoreError("Batch exceeds max_memory_results")
    request_input = copy.deepcopy({"operation": "archive_result", "records": records})
    with store._locked():
        requests = store._read(".requests.json", {})
        if request_id in requests:
            previous = requests[request_id]
            if not json_equal(previous["input"], request_input):
                raise StoreError("request_id was already used for different input")
            result = copy.deepcopy(previous["result"])
            result["records"] = [store._with_trust(r) for r in result["records"]]
            return result
        entries, reserved, prior, written = {}, {}, {}, set()
        for item in records:
            if not isinstance(item, dict) or not isinstance(item.get("local_key"), str) or not item["local_key"]:
                raise StoreError("Each batch item needs a distinct local_key")
            key, op = item["local_key"], item.get("op", "create")
            if key in entries or op not in {"create", "update", "reference"}:
                raise StoreError("Duplicate local_key or invalid operation")
            entries[key] = copy.deepcopy(item)
            if op == "reference":
                if set(item) - {"local_key", "op", "ref"}:
                    raise StoreError("A reference operation accepts only ref")
                local = item.get("ref")
                reserved[key] = None if isinstance(local, dict) and "local_key" in local else _fixed(store, local)
                continue
            if set(item) - {"local_key", "op", "kind", "payload", "record_id", "expected_revision"}:
                raise StoreError("Unknown batch operation fields")
            kind = _kind(item.get("kind"), writable=True)
            if kind == "experiment_result":
                raise StoreError("Experiment execution is owned by its service; use archive for interpretations")
            identifier = item.get("record_id") or f"{kind.rstrip('s')}-{uuid4().hex[:16]}"
            store._record_id(identifier)
            if store._context_has_id(kind, identifier):
                raise StoreError("Cannot write a read-only context identity")
            if (kind, identifier) in written:
                raise StoreError("A batch may write an identity only once")
            written.add((kind, identifier))
            try:
                old = store._get(kind, identifier)
            except KeyError:
                old = None
            if op == "create" and (old is not None or item.get("expected_revision") is not None):
                raise RevisionConflict("create requires a new identity without expected_revision")
            if op == "update" and (old is None or type(item.get("expected_revision")) is not int or item["expected_revision"] != old["revision"]):
                raise RevisionConflict("update requires an existing identity and its current expected_revision")
            if not isinstance(item.get("payload"), dict):
                raise StoreError("Batch payload must be an object")
            _json(item["payload"])
            prior[key] = old
            reserved[key] = {"kind": kind, "id": identifier, "revision": old["revision"] + 1 if old else 1}
        completed, visiting = {}, set()
        staging = {}
        # The overlay is private to this Store while its process lock is held.
        def collection(kind):
            if kind not in staging:
                staging[kind] = copy.deepcopy(store._collection(kind))
            return staging[kind]
        for ref in reserved.values():
            if ref:
                collection(ref["kind"])
        def resolve_value(value):
            if isinstance(value, dict):
                if "local_key" in value:
                    if set(value) - {"local_key", "property_ids"} or value["local_key"] not in entries:
                        raise StoreError("Invalid batch-local reference")
                    result = _ref(build(value["local_key"]))
                    inherited_selection = completed[value["local_key"]].get("property_ids")
                    if inherited_selection is not None:
                        result["property_ids"] = list(inherited_selection)
                    if "property_ids" in value:
                        if inherited_selection is not None and not set(value["property_ids"]) <= set(inherited_selection):
                            raise StoreError("A batch-local reference cannot expand its alias property scope")
                        result["property_ids"] = copy.deepcopy(value["property_ids"])
                    return result
                return {k: resolve_value(v) for k, v in value.items()}
            if isinstance(value, list):
                return [resolve_value(v) for v in value]
            return value
        def build(key):
            if key in completed:
                return completed[key]
            if key in visiting:
                raise StoreError("Cyclic batch-local references; keep evidence links one-way")
            visiting.add(key)
            item, ref = entries[key], reserved[key]
            if item.get("op") == "reference":
                ref = resolve_value(item["ref"])
                store._staged_collections = staging
                try:
                    record = copy.deepcopy(store._resolve_ref(ref))
                finally:
                    del store._staged_collections
                if "property_ids" in ref:
                    record["property_ids"] = list(ref["property_ids"])
            else:
                payload = resolve_value(item["payload"])
                store._staged_collections = staging
                try:
                    payload = prepare_links(store, ref["kind"], payload)
                finally:
                    del store._staged_collections
                record = store._envelope(ref["kind"], payload, ref["id"], ref["revision"])
                staging[ref["kind"]]["records"].append(record)
            completed[key] = record
            visiting.remove(key)
            return record
        for key in entries:
            build(key)
        store._staged_collections = staging
        try:
            # Freeze role references in topological order so dependent records
            # include the canonical target, not the author's abbreviated ref.
            for key, record in completed.items():
                if entries[key].get("op") == "reference":
                    continue
                payload = record["payload"]
                validate_identity(record["kind"], prior[key]["payload"] if prior[key] else None, payload)
                store._validate_payload(record["kind"], record["id"], payload)
                if payload != record["payload"]:
                    record.update(payload=payload)
            # Validate final references before committing the complete group.
            for key, record in completed.items():
                if entries[key].get("op") != "reference":
                    store._validate_payload(record["kind"], record["id"], record["payload"])
            result = {"records": [copy.deepcopy(completed[k]) for k in entries],
                      "refs": {key: {**_ref(completed[key]), **({"property_ids": completed[key]["property_ids"]}
                               if "property_ids" in completed[key] else {})} for key in entries}}
        finally:
            del store._staged_collections
        events = copy.deepcopy(store._collection("events"))
        writes = {}
        for key, record in completed.items():
            if entries[key].get("op") == "reference":
                continue
            writes[f"{record['kind']}.json"] = staging[record["kind"]]
            sequence = len(events["records"]) + 1
            events["records"].append(store._envelope("events", {"sequence": sequence, "action": "archive",
                "target": _ref(record), "request_id": request_id}, f"event-{sequence:08d}", 1))
        requests[request_id] = {"input": request_input, "result": result}
        writes.update({"events.json": events, ".requests.json": requests})
        store._commit(writes)
        result["records"] = [store._with_trust(r) for r in result["records"]]
        return result


# These fields carry links, not mathematical text. ``origin`` is deliberately
# excluded: its child-local identity is provenance, not a parent-library link.
# Declared record reference traversal

REFERENCE_FIELDS = frozenset({
    "target_ref", "claim_ref", "target_claim_ref", "owner_attempt_ref",
    "closing_argument_ref", "attempt_ref", "previous_detailed_state_ref",
    "source_ref", "definition_ref", "definition_refs", "dependencies", "subject_refs", "source_refs", "derived_refs",
    "evidence_refs", "useful_products", "produced_refs", "result_refs",
    "pending_refs", "gap_refs", "active_attempts", "variant_of", "variants",
    "derived_from", "reformulates", "superseded_by", "related_claim_refs", "experiment_refs",
})


def is_record_ref(value) -> bool:
    return isinstance(value, dict) and {"kind", "id", "revision"} <= value.keys()


def map_record_references(payload: dict, mapper) -> dict:
    """Map only declared link slots; mapper receives (fixed_ref, role).

    Roles distinguish an inference premise from a target, a construction under
    study, or a navigation/provenance relation. No role grants additional access.
    """
    def field(value, role):
        if is_record_ref(value):
            return mapper(copy.deepcopy(value), role)
        if isinstance(value, list):
            return [field(item, role) for item in value]
        return walk(value)

    def walk(value):
        if isinstance(value, list):
            return [walk(item) for item in value]
        if not isinstance(value, dict):
            return copy.deepcopy(value)
        result = {}
        for key, item in value.items():
            if key == "origin":
                result[key] = copy.deepcopy(item)
            elif key == "conclusions" and isinstance(item, list):
                result[key] = [
                    {name: field(part, "target") if name == "target" else walk(part)
                     for name, part in conclusion.items()}
                    if isinstance(conclusion, dict) else copy.deepcopy(conclusion)
                    for conclusion in item
                ]
            elif key in REFERENCE_FIELDS:
                role = ("dependency" if key == "dependencies" else
                        "subject" if key == "subject_refs" else
                        "source" if key in {"source_ref", "source_refs"} else
                        "definition" if key in {"definition_ref", "definition_refs"} else
                        "target" if key in {"target_ref", "claim_ref", "target_claim_ref"} else
                        "related")
                result[key] = field(item, role)
            else:
                result[key] = walk(item)
        return result

    return walk(payload)


def record_references(payload: dict, *, roles=None) -> list[dict]:
    """Return declared references, with their roles, without modifying payload."""
    found = []

    def collect(ref, role):
        if roles is None or role in roles:
            found.append({"ref": ref, "role": role})
        return ref

    map_record_references(payload, collect)
    return found
