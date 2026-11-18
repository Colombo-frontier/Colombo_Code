"""Scoped research views with stable membership and freshly checked evidence.

All reads and cursor registration happen under the Store lock. Cursors name a
service-owned list of fixed references; client cursor fields never grant access.
"""
from __future__ import annotations

import copy
import json
from datetime import datetime
from datetime import timezone
from uuid import uuid4

from colombo.cell.research_records import core
from colombo.cell.research_records import certified_relations
from colombo.cell.research_records import obligation_view


RELATIONS = frozenset({"supports", "refutes", "attempts", "subjects", "uses"})
DOMAINS = frozenset({"trust", "payload", "execution", "obligation", "mathematical", "work"})


def _identity(ref):
    return ref["kind"], ref["id"], ref["revision"]


def _ref(record):
    return {key: record[key] for key in ("kind", "id", "revision")}


def _permission_scope(store, include_context):
    """Re-read grants so an old Store instance cannot preserve revoked access."""
    from colombo.cell.record_store import json_equal
    from colombo.cell.record_store import StoreError
    from colombo.cell.record_store import _kind
    store._context = store._load_context()
    grants = {}
    manifest_path = store.memory_dir.parent / "context" / "manifest.json"
    if store._context:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        grants = {(_kind(ref["kind"]), ref["id"], ref["revision"]): ref for ref in manifest["snapshot_refs"]}
        for key, record in store._context.items():
            selection = grants[key].get("property_ids", record.get("property_ids"))
            if selection is not None:
                available = {p["id"] for p in record["payload"].get("properties", [])}
                if record["kind"] != "examples" or not isinstance(selection, list) or not selection \
                        or any(not isinstance(p, str) for p in selection) or not set(selection) <= available:
                    raise StoreError("Invalid context property grant")
                record["property_ids"] = sorted(set(selection))
    scope = {"workspace": str(store.memory_dir), "include_context": include_context,
             "context": [{**_ref(record), **({"property_ids": record["property_ids"]}
                         if "property_ids" in record else {})}
                         for _, record in sorted(store._context.items())] if include_context else []}
    return scope


def _scoped(store, reference, include_context):
    from colombo.cell.record_store import json_equal
    from colombo.cell.record_store import StoreError
    record = copy.deepcopy(store._resolve_ref(reference))
    if record.get("read_only") and not include_context:
        raise StoreError("Reference is outside this query's permitted context scope")
    allowed = record.get("property_ids") if record.get("read_only") else None
    selected = reference.get("property_ids", allowed)
    if selected is not None:
        if allowed is not None and not set(selected) <= set(allowed):
            raise StoreError("Reference exceeds the granted example properties")
        record["property_ids"] = sorted(set(selected))
        record["payload"]["properties"] = [p for p in record["payload"].get("properties", [])
                                            if p["id"] in selected]
    return record


def _normalized_ref(store, reference, include_context):
    record = _scoped(store, reference, include_context)
    return {**_ref(record), **({"property_ids": list(record["property_ids"])}
                              if "property_ids" in record else {})}


def _same_target(store, reference, target, include_context):
    if not isinstance(reference, dict) or not {"kind", "id", "revision"} <= reference.keys():
        return False
    from colombo.cell.record_store import json_equal
    from colombo.cell.record_store import _kind
    try:
        if _kind(reference["kind"]) != target["kind"] or reference["id"] != target["id"]:
            return False
        linked = _scoped(store, reference, include_context)
    except (ValueError, KeyError):
        return False
    if target["kind"] == "claims":
        # Metadata revisions of one immutable proposition share evidence. A
        # different Claim ID, even with similar prose, never gets merged here.
        return core(linked["payload"]) == core(target["payload"])
    if linked["revision"] != target["revision"]:
        return False
    wanted = target.get("property_ids")
    selected = linked.get("property_ids")
    return wanted is None or selected is None or bool(set(wanted) & set(selected))


def _audited_relations(store, record):
    payload = record["payload"]
    covered = certified_relations(store, record) if record["kind"] == "arguments" else []
    if record["kind"] == "arguments" and record.get("origin") == "context" and payload.get("audit_id") \
            and (payload.get("status") == "proved" or payload.get("tag") == "proved"):
        # Parent review files need not be granted. Its fixed, service-created
        # support snapshot covers the exact argument payload that was granted.
        covered = payload.get("conclusions", [])
    return covered


def _relations(store, record, target, names, include_context):
    matches = []
    payload = record["payload"]
    covered = _audited_relations(store, record)
    current = store._assess(record)
    for relation in payload.get("conclusions", []) if record["kind"] == "arguments" else []:
        if relation["relation"] in names and _same_target(store, relation["target"], target, include_context):
            certified = relation in covered
            matches.append({**copy.deepcopy(relation), "audited": certified,
                            "currently_usable": certified and current["state"] == "supported"})
    if "attempts" in names and record["kind"] == "attempts":
        refs = [payload.get(key) for key in ("target_ref", "target_claim_ref", "claim_ref")]
        refs.extend(payload.get("target_refs", []))
        if any(_same_target(store, reference, target, include_context) for reference in refs):
            matches.append({"relation": "attempts", "target": _ref(target)})
    if "subjects" in names:
        for reference in payload.get("subject_refs", []):
            if _same_target(store, reference, target, include_context):
                matches.append({"relation": "subjects", "target": copy.deepcopy(reference)})
    if "uses" in names:
        dependencies = list(payload.get("dependencies", []))
        if record["kind"] == "examples":
            for prop in payload.get("properties", []):
                dependencies.extend(prop.get("dependencies", []))
        for reference in dependencies:
            if _same_target(store, reference, target, include_context):
                matches.append({"relation": "uses", "target": copy.deepcopy(reference),
                                "scope": "record_dependencies"})
    return matches


def _state_values(record, state_filter, obligation=None):
    if state_filter is None:
        return True
    domain, wanted = state_filter["domain"], state_filter["value"]
    if obligation is not None:
        value = {"obligation": obligation["satisfaction"], "mathematical": obligation["mathematical_state"],
                 "work": obligation.get("work_status", "active")}.get(domain)
    else:
        payload, trust = record["payload"], record.get("current_trust", {})
        value = {"trust": trust.get("state"), "payload": payload.get("status", payload.get("tag")),
                 "execution": payload.get("execution", {}).get("status"),
                 "mathematical": trust.get("state") if record["kind"] == "claims" else None}.get(domain)
    return value in wanted


def _normalize(store, query, kinds, record_id, revision, limit, include_context,
               target_ref, relations, route_id, state_filter, since_event):
    from colombo.cell.record_store import json_equal
    from colombo.cell.record_store import _kind
    from colombo.cell.record_store import _revision
    from colombo.cell.record_store import StoreError
    retrieval = store.settings["retrieval"]
    limit = retrieval["memory_results"] if limit is None else limit
    include_context = retrieval["include_context"] if include_context is None else include_context
    if not isinstance(query, str) or type(include_context) is not bool:
        raise StoreError("query must be text and include_context a boolean")
    if type(limit) is not int or not 1 <= limit <= retrieval["max_memory_results"]:
        raise StoreError("limit is outside the configured memory result range")
    if kinds is not None and (not isinstance(kinds, list) or not kinds):
        raise StoreError("kinds must be a nonempty list or None")
    kinds = sorted({_kind(k) for k in kinds}) if kinds is not None else None
    if record_id is not None:
        store._record_id(record_id)
    _revision(revision)
    if revision is not None and record_id is None:
        raise StoreError("revision requires record_id")
    if relations is not None and (not isinstance(relations, list) or not relations or
                                  any(not isinstance(r, str) or r not in RELATIONS for r in relations)):
        raise StoreError("relations must select supports/refutes/attempts/subjects/uses")
    if relations and target_ref is None:
        raise StoreError("relations requires a fixed target_ref")
    if route_id is not None and (not isinstance(route_id, str) or not route_id):
        raise StoreError("route_id must be a nonempty string")
    if state_filter is not None:
        if not isinstance(state_filter, dict) or set(state_filter) != {"domain", "value"} \
                or state_filter["domain"] not in DOMAINS:
            raise StoreError("state_filter requires an explicit supported domain and value")
        values = state_filter["value"]
        values = [values] if isinstance(values, str) else values
        if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v for v in values):
            raise StoreError("state_filter.value must contain one or more state names")
        state_filter = {"domain": state_filter["domain"], "value": sorted(set(values))}
    obligation_mode = route_id is not None or state_filter is not None and state_filter["domain"] in {"obligation", "work"}
    if obligation_mode and (relations or since_event is not None or
                            kinds is not None and kinds != ["proof_state"]):
        raise StoreError("Obligation views cannot combine event/relationship modes or non-proof_state kinds")
    if obligation_mode and state_filter and state_filter["domain"] not in {"obligation", "work", "mathematical"}:
        raise StoreError("An obligation view needs an obligation, mathematical or work state filter")
    if since_event is not None:
        if not isinstance(since_event, dict) or set(since_event) != {"scope", "stream", "sequence"} \
                or since_event["scope"] != "current_workspace" or since_event["stream"] != "memory" \
                or type(since_event["sequence"]) is not int or since_event["sequence"] < 0:
            raise StoreError("since_event requires current_workspace, memory and a nonnegative sequence")
    return {"query": " ".join(query.casefold().split()), "kinds": kinds, "record_id": record_id,
            "revision": revision, "limit": limit, "include_context": include_context,
            "target_ref": copy.deepcopy(target_ref), "relations": sorted(set(relations)) if relations else None,
            "route_id": route_id, "state_filter": state_filter, "since_event": copy.deepcopy(since_event),
            "mode": "obligations" if obligation_mode else "events" if since_event is not None else "records"}


def _all_records(store, include_context, kinds=None):
    from colombo.cell.record_store import json_equal
    from colombo.cell.record_store import READABLE_KINDS
    from colombo.cell.record_store import StoreError
    records = []
    selected = READABLE_KINDS - {"events"} if kinds is None else set(kinds) - {"events"}
    for kind in sorted(selected):
        local = store._collection(kind)["records"]
        if include_context and any(store._context_has_id(kind, r["id"]) for r in local):
            raise StoreError("Local records collide with read-only context identities")
        records.extend(local)
        if include_context:
            records.extend(store._context_records(kind))
    return records


def _text_matches(record, terms):
    body = json.dumps(record["payload"], ensure_ascii=False, sort_keys=True).casefold() + " " + record["id"].casefold()
    return all(term in body for term in terms)


def _find_members(store, filters, upper):
    from colombo.cell.record_store import json_equal
    from colombo.cell.record_store import StoreError
    include_context = filters["include_context"]
    target = _scoped(store, filters["target_ref"], include_context) if filters["target_ref"] else None
    kinds, terms = filters["kinds"], filters["query"].split()
    def matches(record, *, compare_target=True, compare_text=True):
        if kinds is not None and record["kind"] not in kinds:
            return False
        if filters["record_id"] is not None and record["id"] != filters["record_id"]:
            return False
        if filters["revision"] is not None and record["revision"] != filters["revision"]:
            return False
        if compare_text and not _text_matches(record, terms):
            return False
        if target and compare_target:
            if filters["relations"]:
                if not _relations(store, record, target, filters["relations"], include_context):
                    return False
            elif _identity(record) != _identity(target):
                return False
        return True
    members = []
    if filters["mode"] == "events":
        lower = filters["since_event"]["sequence"]
        if lower > upper:
            raise StoreError("since_event.sequence exceeds this workspace's event stream")
        for event in store._collection("events")["records"]:
            if not lower < event["payload"]["sequence"] <= upper:
                continue
            changed = _scoped(store, event["payload"]["target"], False)
            changed = store._with_trust(changed)
            if matches(changed) and _state_values(changed, filters["state_filter"]):
                members.append({"record_ref": _ref(event)})
        return members
    selected_kinds = kinds
    if filters["mode"] == "obligations":
        selected_kinds = ["proof_state"]
    elif filters["relations"] and not set(filters["relations"]) & {"subjects", "uses"}:
        relevant = ({"arguments"} if set(filters["relations"]) & {"supports", "refutes"} else set()) \
            | ({"attempts"} if "attempts" in filters["relations"] else set())
        selected_kinds = sorted(relevant if kinds is None else relevant & set(kinds))
    records = [target] if target and not filters["relations"] and filters["mode"] == "records" \
        else _all_records(store, include_context, selected_kinds)
    if kinds is not None and "events" in kinds:
        records += store._collection("events")["records"]
    latest = {}
    for record in records:
        if filters["revision"] is not None and record["revision"] != filters["revision"]:
            continue
        key = record["kind"], record["id"]
        if key not in latest or record["revision"] > latest[key]["revision"]:
            latest[key] = record
    if target and not filters["relations"] and filters["mode"] == "records":
        latest = {(target["kind"], target["id"]): target}
    candidates = list(latest.values())
    if target and set(filters["relations"] or []) & {"supports", "refutes"}:
        # An unfinished newer revision does not erase a still usable old
        # certificate. Keep one revision per certificate, plus latest work.
        certificates = {}
        for record in records:
            payload = record["payload"]
            if record["kind"] != "arguments" or not payload.get("audit_id") or not (
                    payload.get("status") == "proved" or payload.get("tag") == "proved"):
                continue
            if filters["revision"] is not None and record["revision"] != filters["revision"]:
                continue
            if not any(c["relation"] in filters["relations"] and
                       _same_target(store, c["target"], target, include_context)
                       for c in _audited_relations(store, record)):
                continue
            key = record["id"], payload["audit_id"]
            if key not in certificates or record["revision"] > certificates[key]["revision"]:
                certificates[key] = record
        present = {_identity(record) for record in candidates}
        candidates.extend(record for record in certificates.values() if _identity(record) not in present)
    ordered = sorted(candidates, key=lambda r: (r["created_at"], r["kind"], r["id"]), reverse=True)
    for raw in ordered:
        record = _scoped(store, _ref(raw), include_context)
        if filters["mode"] == "obligations":
            if record["kind"] != "proof_state" or not matches(record, compare_target=False, compare_text=False):
                continue
            for obligation in obligation_view(store, record):
                if filters["route_id"] is not None and obligation["route_id"] != filters["route_id"]:
                    continue
                if target and not _same_target(store, obligation["target_claim_ref"], target, include_context):
                    continue
                if not _text_matches({"id": obligation["id"], "payload": obligation}, terms):
                    continue
                if _state_values(record, filters["state_filter"], obligation):
                    members.append({"record_ref": _ref(record), "route_id": obligation["route_id"],
                                    "obligation_id": obligation["id"]})
        elif matches(record):
            record = store._with_trust(record)
            if _state_values(record, filters["state_filter"]):
                selected = target.get("property_ids") if target and _identity(record) == _identity(target) else record.get("property_ids")
                reference = {**_ref(record), **({"property_ids": selected} if selected else {})}
                members.append({"record_ref": reference})
    return members


def _summary(store, record):
    trust = record.get("current_trust", {})
    result = {**_ref(record), "current_trust": {key: trust[key] for key in
              ("state", "citation_requires_application_check", "execution_status", "mathematical_status")
              if key in trust}}
    payload = record["payload"]
    preview_limit = store.settings["retrieval"]["memory_results"]
    for key in ("status", "tag", "target_ref", "target_claim_ref", "claim_ref", "conclusions", "subject_refs", "dependencies"):
        if key in payload:
            value = payload[key]
            if isinstance(value, list):
                result[key] = copy.deepcopy(value[:preview_limit])
                if len(value) > preview_limit:
                    result[f"{key}_omitted"] = len(value) - preview_limit
            else:
                result[key] = copy.deepcopy(value)
    for key in ("read_only", "property_ids"):
        if key in record:
            result[key] = record[key]
    if record["kind"] == "examples":
        properties = payload.get("properties", [])
        result["properties"] = [{"id": prop["id"], "state": value.get("state")}
                                for prop in properties[:preview_limit]
                                for value in [trust.get("properties", {}).get(prop["id"], {})]]
        if len(properties) > preview_limit:
            result["properties_omitted"] = len(properties) - preview_limit
    maximum = store.settings["retrieval"].get("summary_max_chars", 0)
    if maximum:
        text = next((payload[key] for key in ("title", "proposition", "statement", "summary", "construction", "question")
                     if payload.get(key)), "")
        if not isinstance(text, str):
            text = json.dumps(text, ensure_ascii=False, sort_keys=True)
        result["excerpt"], result["excerpt_truncated"] = text[:maximum], len(text) > maximum
    return result


def _obligation_summary(store, row):
    result = {key: copy.deepcopy(row[key]) for key in (
        "id", "route_id", "proof_state_ref", "target_claim_ref", "owner_attempt_ref",
        "closing_argument_ref", "expected_relation", "work_status", "mathematical_state", "satisfaction")
        if key in row}
    result["closing_trust"] = {"state": row["closing_trust"]["state"]} if row.get("closing_trust") else None
    maximum = store.settings["retrieval"].get("summary_max_chars", 0)
    if maximum and isinstance(row.get("remaining_gap"), str):
        result["remaining_gap"] = row["remaining_gap"][:maximum]
        result["remaining_gap_truncated"] = len(row["remaining_gap"]) > maximum
    refs = row.get("evidence_refs", [])
    result["evidence_refs"] = copy.deepcopy(refs[:store.settings["retrieval"]["memory_results"]])
    result["evidence_refs_omitted"] = len(refs) - len(result["evidence_refs"])
    return result


def query(store, query="", kinds=None, record_id=None, revision=None, limit=None, include_context=None,
          *, target_ref=None, relations=None, route_id=None, state_filter=None, since_event=None,
          cursor=None, detail="full"):
    """Read one scope: records, proof-state obligations, or direct memory events.

    Filters combine with AND; values in a relation/state/kinds list combine with
    OR. With a cursor, omitted filters retain their original values. Explicitly
    changing one requires a new query. detail may change without changing members.
    """
    from colombo.cell.record_store import json_equal
    from colombo.cell.record_store import StoreError
    if detail not in {"summary", "full"}:
        raise StoreError("detail must be summary or full")
    supplied = dict(query=query, kinds=kinds, record_id=record_id, revision=revision, limit=limit,
                    include_context=include_context, target_ref=target_ref, relations=relations,
                    route_id=route_id, state_filter=state_filter, since_event=since_event)
    with store._locked():
        registry = store._read(".queries.json", {})
        if not isinstance(registry, dict):
            raise StoreError("Invalid query cursor registry")
        if cursor is not None:
            if not isinstance(cursor, dict) or set(cursor) != {"query_id", "offset"} \
                    or not isinstance(cursor["query_id"], str) or type(cursor["offset"]) is not int:
                raise StoreError("cursor requires a service query_id and integer offset")
            saved = registry.get(cursor["query_id"])
            if not isinstance(saved, dict):
                raise StoreError("Unknown query cursor")
            inherited = {key: saved["filters"][key] for key in supplied}
            for key, value in supplied.items():
                if value is not None and not (key == "query" and value == ""):
                    inherited[key] = value
            filters = _normalize(store, **inherited)
        else:
            filters = _normalize(store, **supplied)
        scope = _permission_scope(store, filters["include_context"])
        if filters["target_ref"] is not None:
            filters["target_ref"] = _normalized_ref(store, filters["target_ref"], filters["include_context"])
        if cursor is not None:
            if not json_equal(saved["scope"], scope) or not json_equal(saved["filters"], filters):
                raise StoreError("Cursor filters or authorized context changed; start a new query")
            query_id, offset = cursor["query_id"], cursor["offset"]
            if offset < 0 or offset > len(saved["members"]) or offset % filters["limit"]:
                raise StoreError("Cursor offset is outside its registered pages")
        else:
            events = store._collection("events")["records"]
            upper = max((event["payload"]["sequence"] for event in events), default=0)
            members = _find_members(store, filters, upper)
            query_id, offset = uuid4().hex, 0
            saved = {"filters": filters, "scope": scope, "members": members,
                     "upper_sequence": upper, "created_at": datetime.now(timezone.utc).isoformat()}
            registry[query_id] = saved
            store._commit({".queries.json": registry})
        checked_at = datetime.now(timezone.utc).isoformat()
        target = _scoped(store, filters["target_ref"], filters["include_context"]) if filters["target_ref"] else None
        rows, obligations = [], []
        for member in saved["members"][offset:offset + filters["limit"]]:
            record = _scoped(store, member["record_ref"], filters["include_context"])
            if filters["mode"] == "obligations":
                views = [row for row in obligation_view(store, record)
                         if row["route_id"] == member["route_id"] and row["id"] == member["obligation_id"]]
                if len(views) != 1:
                    raise StoreError("Pinned obligation membership no longer matches stored proof_state")
                row = views[0] if detail == "full" else _obligation_summary(store, views[0])
                row["state_filter_matches_now"] = _state_values(record, filters["state_filter"], views[0])
                obligations.append(row)
                continue
            record = store._with_trust(record)
            changed = record
            if filters["mode"] == "events":
                changed = store._with_trust(_scoped(store, record["payload"]["target"], False))
            row = record if detail == "full" else _summary(store, record)
            row["state_filter_matches_now"] = _state_values(changed, filters["state_filter"])
            if target and filters["relations"]:
                row["relation_matches"] = _relations(store, changed, target, filters["relations"], filters["include_context"])
            if filters["mode"] == "events":
                row["event"] = copy.deepcopy(record["payload"])
                row["target_current_trust"] = changed["current_trust"]
            rows.append(row)
        total, returned = len(saved["members"]), len(rows) + len(obligations)
        next_offset = offset + returned
        result = {"records": rows, "count": total, "returned": returned, "detail": detail,
                  "cursor": {"query_id": query_id, "offset": next_offset} if next_offset < total else None,
                  "page_cursor": {"query_id": query_id, "offset": offset}, "state_checked_at": checked_at,
                  "scan": {"scope": "current_workspace", "stream": "memory", "upper_sequence": saved["upper_sequence"],
                           "membership_fixed_at": saved["created_at"], "membership_fixed": True,
                           "complete_trust_change_feed": False, "uses_scope": "record_dependencies"}}
        if filters["mode"] == "obligations":
            result["obligations"] = obligations
        if filters["target_ref"]:
            result["target_ref"] = copy.deepcopy(filters["target_ref"])
        return result
