"""Pure, replayable finite discovery accounting. No search, read or approval.

An exhausted provider is different from a completed declared finite window.
Unknown tails remain explicit; exposed plausible leads cannot be discarded.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import date
import hashlib
import json
import re


PROVIDERS = ("arxiv", "crossref", "openalex")
DISPOSITIONS = ("metadata_screened_incomparable", "needs_check", "checked_source")
REASONS = ("scope_not_frozen", "declared_window_unprocessed", "metadata_not_exposed",
    "candidate_not_classified", "plausible_lead_unresolved", "required_source_unverified",
    "required_version_unchecked", "network_attempts_exhausted", "metadata_limit_exhausted",
    "source_failure_unresolved", "scope_complete_finite", "provider_tail_unassessed", "checked_source_not_reported",
    "lookup_material_alert_unassessed")


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


class FiniteScopeError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def require(ok, code, message):
    if not ok:
        raise FiniteScopeError(code, message)


def integer(value, name, maximum=None):
    require(type(value) is int and value > 0 and (maximum is None or value <= maximum),
            "invalid_scope", name + " must be a positive bounded integer")
    return value


def text(value, name, maximum=3000):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= maximum,
            "invalid_scope", name + " must be nonempty bounded text")
    return value.strip()


def day(value, nullable=False):
    if value is None and nullable:
        return None
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is not None,
            "invalid_scope", "Dates must be exact ISO calendar dates")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise FiniteScopeError("invalid_scope", "Invalid calendar date") from exc
    return value


def at(value, pointer):
    require(isinstance(pointer, str) and (not pointer or pointer.startswith("/")), "invalid_scope", "Invalid JSON pointer")
    for part in pointer[1:].split("/") if pointer else []:
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def _compact_page(result):
    """Keep identities/dates and an exact upstream hash, not abstracts/pages."""
    value = {key: deepcopy(result[key]) for key in ("next_cursor", "total", "identity", "latest_version_verified", "requested_version",
        "version_history_complete", "metadata_response_sha256", "metadata_url", "metadata_fetched_at",
        "material_alerts", "known_baseline_versions", "official_update_metadata", "correction_status") if key in result}
    fields = ("paper_id", "title", "identifiers", "urls", "publication_events", "versions", "metadata_status", "work_type")
    if isinstance(result.get("records"), list):
        value["records"] = [{k: deepcopy(row[k]) for k in fields if k in row} for row in result["records"]]
    if isinstance(result.get("record"), dict):
        value["record"] = {k: deepcopy(result["record"][k]) for k in fields if k in result["record"]}
    value["upstream_sha256"] = digest(result)
    return value


def metadata_date_state(record, route):
    """Metadata screening only, never source-version/theorem certification."""
    kinds = {"submission": {"preprint", "submission"}, "publication": {"publication"}, "revision": {"revision"}}
    dates = []
    for event in record.get("publication_events", []):
        if not isinstance(event, dict) or event.get("kind") not in kinds[route["date_kind"]]:
            continue
        try:
            dates.append(day(event.get("date", "")[:10]))
        except (FiniteScopeError, TypeError):
            continue
    if route["date_kind"] == "revision":
        for version in record.get("versions", []):
            try:
                dates.append(day(version.get("date", "")[:10]))
            except (FiniteScopeError, TypeError):
                continue
    if not dates:
        return "unknown"
    return "in_window" if any((route["date_from"] is None or route["date_from"] <= d) and d <= route["date_to"] for d in dates) else "out_of_window"


def plan_schema():
    """Machine-readable handoff shape; normalise_plan also checks semantics."""
    nullable_date = {"type": ["string", "null"]}
    route = {"type": "object", "additionalProperties": False, "required": ["route_id", "provider", "query"],
        "properties": {"route_id": {"type": "string"}, "provider": {"enum": list(PROVIDERS)}, "query": {"type": "string"},
        "year": {"type": ["integer", "null"]}, "limit": {"type": "integer", "minimum": 1, "maximum": 25},
        "max_pages": {"type": "integer", "minimum": 1, "maximum": 4}, "max_records": {"type": "integer", "minimum": 1, "maximum": 200},
        "date_kind": {"enum": ["submission", "revision", "publication"]}, "date_from": nullable_date,
        "date_to": {"type": "string"}, "purpose": {"enum": ["novelty", "refinement"]},
        "refinement_of": {"type": ["string", "null"]}}}
    obligation = {"type": "object", "additionalProperties": False,
        "required": ["obligation_id", "kind", "identifier", "reason"], "properties": {
        "obligation_id": {"type": "string"}, "kind": {"enum": ["doi", "arxiv", "url", "source_hash"]},
        "identifier": {"type": "string"}, "required": {"type": "boolean"}, "reason": {"type": "string"},
        "record_ids": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "verification": {"enum": ["primary_text", "metadata_version"]}}}
    return {"type": "object", "additionalProperties": False, "required": ["routes"], "properties": {
        "version": {"const": 1}, "window_start": nullable_date, "cutoff": {"type": "string"},
        "routes": {"type": "array", "minItems": 0, "maxItems": 6, "items": route},
        "source_obligations": {"type": "array", "maxItems": 40, "items": obligation},
        "mode": {"enum": ["standard", "closed_bracket_check"]}, "proof_check": {"type": "string"},
        "comparison_ids": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "baseline_refs": {"type": "array", "items": {"type": "object", "additionalProperties": False,
            "required": ["pointer", "sha256"], "properties": {"pointer": {"type": "string"}, "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}}}},
        "self_contained_reason": {"type": "string"}}}


def _validate_shape(value, schema):
    from jsonschema import Draft202012Validator
    errors = list(Draft202012Validator(schema).iter_errors(value))
    require(not errors, "invalid_scope", "Finite plan does not match its declared schema" + (": " + errors[0].message[:200] if errors else ""))


def _limits(config):
    budget = config.get("budgets", {})
    return {"queries": integer(budget.get("max_discovery_queries", 6), "max_discovery_queries", 64),
        "refinement_reserve": integer(budget.get("refinement_query_reserve", 2), "refinement_query_reserve", 63),
        "network_attempts": integer(budget.get("max_provider_page_attempts", 24), "max_provider_page_attempts", 256),
        "pages_per_route": integer(budget.get("max_pages_per_route", 4), "max_pages_per_route", 4),
        "metadata_records": integer(budget.get("max_metadata_records", 200), "max_metadata_records", 10000)}


def _route(row, context, limits):
    value = deepcopy(row)
    value.setdefault("year", None)
    value.setdefault("limit", 10)
    value.setdefault("max_pages", 1)
    value.setdefault("max_records", value["limit"] * value["max_pages"])
    value.setdefault("purpose", "novelty")
    value.setdefault("refinement_of", None)
    value.setdefault("date_kind", "submission" if value["provider"] == "arxiv" else "publication")
    value.setdefault("date_from", context.get("window_start"))
    value.setdefault("date_to", context["cutoff"])
    for key in ("route_id", "query"):
        value[key] = text(value[key], key)
    require(value["provider"] in PROVIDERS, "invalid_scope", "Unknown provider")
    require(value["year"] is None or type(value["year"]) is int and 1000 <= value["year"] <= 9999,
            "invalid_scope", "Invalid provider year")
    integer(value["limit"], "limit", 25)
    integer(value["max_pages"], "max_pages", limits["pages_per_route"])
    integer(value["max_records"], "max_records", limits["metadata_records"])
    require(value["max_records"] <= value["limit"] * value["max_pages"], "invalid_scope", "Declared page capacity cannot cover max_records")
    day(value["date_from"], True)
    day(value["date_to"])
    require(value["date_to"] <= context["cutoff"] and (value["date_from"] is None or value["date_from"] <= value["date_to"]),
            "invalid_scope", "Route date window exceeds the frozen cutoff or is reversed")
    if value["year"] is not None:
        require(str(value["year"]) <= context["cutoff"][:4], "invalid_scope", "Provider year exceeds cutoff")
    require(value["purpose"] in {"novelty", "refinement"} and value["date_kind"] in {"submission", "revision", "publication"},
            "invalid_scope", "Invalid route purpose or date kind")
    require(value["date_kind"] == ("submission" if value["provider"] == "arxiv" else "publication"),
            "unsupported_date_semantics", "Discovery providers do not establish global revision-order coverage; use exact metadata-version lookups")
    require((value["purpose"] == "novelty" and value["refinement_of"] is None)
            or (value["purpose"] == "refinement" and isinstance(value["refinement_of"], str) and value["refinement_of"]),
            "invalid_scope", "Refinement must identify an original route")
    return value


def _obligation(row, context):
    value = deepcopy(row)
    for key in ("obligation_id", "identifier", "reason"):
        value[key] = text(value[key], key)
    value.setdefault("required", True)
    value.setdefault("record_ids", [])
    value.setdefault("verification", "primary_text")
    require(type(value["required"]) is bool and value["kind"] in {"doi", "arxiv", "url", "source_hash"}
            and value["verification"] in {"primary_text", "metadata_version"}, "invalid_scope", "Invalid source obligation")
    require(isinstance(value["record_ids"], list) and len(set(value["record_ids"])) == len(value["record_ids"])
            and all(isinstance(x, str) and x for x in value["record_ids"]), "invalid_scope", "Invalid source candidate linkage")
    require(value["required"] or not value["record_ids"], "invalid_scope", "Optional historical sources cannot stand in for candidate obligations")
    if value["kind"] == "url":
        require(value["identifier"].startswith(("https://", "http://")), "invalid_scope", "Source URL must be public HTTP(S)")
    if value["kind"] == "source_hash":
        require(context.get("maintenance_role") == "reviewer" and value["identifier"] in context.get("allowed_source_hashes", [])
                and re.fullmatch(r"[0-9a-f]{64}", value["identifier"]) and value["required"]
                and value["verification"] == "primary_text", "invalid_scope", "Reviewer source hashes must be exact granted required primary-text identities")
    elif value["kind"] == "url" and value["verification"] == "primary_text":
        from urllib.parse import urlsplit
        parsed = urlsplit(value["identifier"])
        require(parsed.scheme in {"http", "https"} and parsed.hostname and not parsed.username and not parsed.password,
                "invalid_scope", "A primary source needs an HTTP(S) identity without embedded credentials")
        # Source access keeps its exact private request identity. Metadata URL
        # lookup has a stricter public-query policy in its separate namespace.
    else:
        from .literature_lookup import canonical_identifier
        value["identifier"] = canonical_identifier(value["kind"], value["identifier"])
    return value


def normalise_plan(plan, context, config, *, own_baseline_refs=None):
    _validate_shape(plan, plan_schema())
    limits = _limits(config)
    require(limits["refinement_reserve"] < limits["queries"], "invalid_scope", "Refinement reserve must leave a novelty slot")
    value = deepcopy(plan)
    value.setdefault("version", 1)
    value.setdefault("window_start", context.get("window_start"))
    value.setdefault("cutoff", context["cutoff"])
    value.setdefault("source_obligations", [])
    value.setdefault("mode", "standard")
    value.setdefault("proof_check", "")
    value.setdefault("comparison_ids", [])
    value.setdefault("baseline_refs", [])
    value.setdefault("self_contained_reason", "")
    day(value["window_start"], True)
    day(value["cutoff"])
    require(value["cutoff"] == context["cutoff"] and value["window_start"] == context.get("window_start"),
            "invalid_scope", "Plan must bind the frozen research window exactly")
    value["routes"] = [_route(row, context, limits) for row in value["routes"]]
    ids = [row["route_id"] for row in value["routes"]]
    fingerprints = [digest({k: row[k] for k in ("provider", "query", "year", "limit")}) for row in value["routes"]]
    require(len(ids) == len(set(ids)) and len(fingerprints) == len(set(fingerprints)), "invalid_scope", "Duplicate route ID or request identity")
    novelty = [row for row in value["routes"] if row["purpose"] == "novelty"]
    reviewer = context.get("maintenance_role") == "reviewer"
    require((novelty or reviewer and not ids) and len(novelty) <= limits["queries"] - limits["refinement_reserve"] and len(ids) <= limits["queries"],
            "invalid_scope", "Novelty plan consumes the reserved refinement slots")
    for row in value["routes"]:
        require(row["refinement_of"] is None or row["refinement_of"] in ids and row["refinement_of"] != row["route_id"],
                "invalid_scope", "Unknown or self-referential refinement route")
        seen, parent = set(), row["refinement_of"]
        while parent is not None:
            require(parent not in seen, "invalid_scope", "Refinement ancestry cannot cycle")
            seen.add(parent)
            parent = next(r for r in value["routes"] if r["route_id"] == parent)["refinement_of"]
    minimum = integer(config.get("budgets", {}).get("light_min_novelty_records" if value["mode"] == "closed_bracket_check"
        else "min_novelty_records", 1), "minimum novelty records", limits["metadata_records"])
    require(all(row["max_records"] >= minimum for row in novelty), "invalid_scope", "Declared novelty window is below its configured minimum")
    value["source_obligations"] = [_obligation(row, context) for row in value["source_obligations"]]
    source_ids = [row["obligation_id"] for row in value["source_obligations"]]
    require(len(source_ids) == len(set(source_ids)), "invalid_scope", "Duplicate source obligation")
    baseline = context.get("artifacts", {}).get("baseline", {})
    for ref in value["baseline_refs"]:
        try:
            require(digest(at(baseline, ref["pointer"])) == ref["sha256"], "invalid_scope", "Frozen baseline reference hash differs")
        except (KeyError, IndexError, TypeError) as exc:
            raise FiniteScopeError("invalid_scope", "Unknown frozen baseline reference") from exc
    if value["mode"] == "closed_bracket_check":
        text(value["proof_check"], "proof_check", 6000)
        comparisons = baseline.get("comparisons", [])
        require(comparisons and all(row.get("status", {}).get("code") == "optimal"
                and row.get("status", {}).get("missing_sides", []) == [] for row in comparisons),
                "invalid_scope", "Closed-bracket lane requires all registered statuses optimal; labels prove no exact cost")
        expected = {row.get("comparison_id", row.get("id")) for row in comparisons}
        require(set(value["comparison_ids"]) == expected, "invalid_scope", "Closed-bracket plan omits registered comparisons")
        own = {tuple(row) for row in own_baseline_refs or []}
        pointers = {row["pointer"] for row in value["baseline_refs"] if (row["pointer"], row["sha256"]) in own}
        require(len(pointers) == len(value["baseline_refs"]), "invalid_scope", "Closed-bracket references require complete own frozen reads")
        for name in ("common_specification", "parameters", "views", "quantities", "resource_projections", "bounds", "proofs", "comparisons"):
            require(name in baseline, "invalid_scope", "Missing fixed-target section")
            covered = "" in pointers or "/" + name in pointers
            if not covered and isinstance(baseline[name], list):
                covered = all(f"/{name}/{i}" in pointers for i in range(len(baseline[name])))
            require(covered, "invalid_scope", "Closed-bracket lane did not read complete fixed-target section: " + name)
        require(value["self_contained_reason"].strip() or any(row["required"] and row["verification"] == "metadata_version"
                for row in value["source_obligations"]), "invalid_scope", "Declare version/correction checks or justify self-contained proof")
    return value


class FiniteScope:
    """Mutable pure state; callers bind its events to the actual tool journal."""
    def __init__(self, context, config):
        self.context, self.config = deepcopy(context), deepcopy(config)
        self.enabled = config.get("budgets", {}).get("finite_research_scope", False) is True
        self.limits = _limits(config)
        self.identity = {key: context.get(key) for key in ("setting_id", "base_version", "cutoff", "window_start", "policy", "prepared_hash", "maintenance_role")}
        self.history = []
        self.data = {"plan": None, "routes": {}, "pages": {}, "candidates": {}, "sources": {}, "tickets": {},
                     "network_attempts": 0, "exposed_metadata": 0, "lookup_count": 0, "own_source_reads": [], "source_read_sequences": {}}

    def _call(self, operation, arguments):
        old = deepcopy(self.data)
        try:
            result = getattr(self, "_" + operation)(**deepcopy(arguments))
            record = {"sequence": len(self.history), "previous_hash": self.history[-1]["event_hash"] if self.history else None,
                      "operation": operation, "arguments": deepcopy(arguments), "state_sha256": digest(self.data)}
            record["event_hash"] = digest(record)
            self.history.append(record)
            return result
        except Exception:
            self.data = old
            raise

    def assert_frozen(self):
        require(self.enabled and self.data["plan"] is not None, "scope_not_frozen", "Freeze a finite research plan before literature access")

    def freeze(self, plan, *, own_baseline_refs=None):
        return self._call("freeze", {"plan": plan, "own_baseline_refs": sorted([list(row) for row in own_baseline_refs or []])})

    def _freeze(self, plan, own_baseline_refs):
        require(self.enabled and self.data["plan"] is None, "scope_already_frozen", "A finite scope can be frozen only once")
        value = normalise_plan(plan, self.context, self.config, own_baseline_refs=own_baseline_refs)
        self.data["plan"] = value
        for route in value["routes"]:
            self._add_route(route)
        for row in value["source_obligations"]:
            self._add_source(row)
        return self.summary()

    def _add_route(self, route):
        self.data["routes"][route["route_id"]] = {"declaration": deepcopy(route), "pages": [], "next_cursor": None,
                                                  "started": False, "terminal": False, "admitted_records": 0}

    def _add_source(self, row):
        self.data["sources"][row["obligation_id"]] = {"declaration": deepcopy(row),
            "fetched_hashes": [row["identifier"]] if row["kind"] == "source_hash" else [], "read_hashes": [],
            "metadata_checked": False, "failed": False, "material_alerts": [], "alert_after_sequence": None}

    def extend(self, extension):
        return self._call("extend", {"extension": extension})

    def _extend(self, extension):
        self.assert_frozen()
        require(isinstance(extension, dict) and set(extension) <= {"reason", "routes", "route_extensions", "source_obligations"},
                "invalid_scope", "Extensions cannot replace or retire existing scope")
        text(extension.get("reason"), "extension reason")
        require(any(extension.get(k) for k in ("routes", "route_extensions", "source_obligations")), "invalid_scope", "Empty extension")
        for row in extension.get("routes", []):
            _validate_shape(row, plan_schema()["properties"]["routes"]["items"])
            route = _route(row, self.context, self.limits)
            require(route["purpose"] == "refinement" and route["refinement_of"] in self.data["routes"],
                    "invalid_scope", "Additional queries must be explicit refinements of an existing route")
            require(route["route_id"] not in self.data["routes"] and len(self.data["routes"]) < self.limits["queries"],
                    "query_limit_exhausted", "Distinct-query ceiling reached or duplicate route")
            identity = {k: route[k] for k in ("provider", "query", "year", "limit")}
            require(not any({k: item["declaration"][k] for k in identity} == identity for item in self.data["routes"].values()),
                    "invalid_scope", "An existing query must use a monotone window extension")
            self._add_route(route)
        for ext in extension.get("route_extensions", []):
            require(set(ext) == {"route_id", "max_pages", "max_records"} and ext["route_id"] in self.data["routes"],
                    "invalid_scope", "Invalid route extension")
            old = self.data["routes"][ext["route_id"]]["declaration"]
            integer(ext["max_pages"], "max_pages", self.limits["pages_per_route"])
            integer(ext["max_records"], "max_records", self.limits["metadata_records"])
            require(ext["max_pages"] >= old["max_pages"] and ext["max_records"] >= old["max_records"]
                    and (ext["max_pages"], ext["max_records"]) != (old["max_pages"], old["max_records"]),
                    "invalid_scope", "A finite window cannot shrink or silently retire observed leads")
            require(ext["max_records"] <= ext["max_pages"] * old["limit"], "invalid_scope", "Extended page capacity cannot cover max_records")
            old.update(max_pages=ext["max_pages"], max_records=ext["max_records"])
            route = self.data["routes"][ext["route_id"]]
            available = old["max_records"]
            admitted = 0
            for key in route["pages"]:
                page = self.data["pages"][key]
                count = min(len(page["record_ids"]), available)
                extra = set(range(count)) - set(page["allowed_indices"])
                if extra:
                    original = next(event["arguments"]["provider_result"] for event in self.history
                        if event["operation"] == "record_search" and event["arguments"]["search_id"] == page["search_id"])
                    for index in sorted(extra):
                        self._candidate(ext["route_id"], page["record_ids"][index], original["records"][index])
                page["allowed_indices"] = list(range(count))
                admitted += count
                available -= count
            route["admitted_records"] = admitted
        for row in extension.get("source_obligations", []):
            _validate_shape(row, plan_schema()["properties"]["source_obligations"]["items"])
            row = _obligation(row, self.context)
            require(row["obligation_id"] not in self.data["sources"], "invalid_scope", "Source obligations are append-only")
            self._add_source(row)
        return self.summary()

    @staticmethod
    def _cursor(provider, cursor):
        starts = (None, "", "0", 0) if provider == "arxiv" else (None, "", "*")
        return "__start__" if cursor in starts else str(cursor)

    def before_search(self, provider, query, year, cursor, limit, *, network_attempted=False):
        return self._call("before_search", dict(provider=provider, query=query, year=year, cursor=cursor,
            limit=limit, network_attempted=network_attempted))

    def _before_search(self, provider, query, year, cursor, limit, network_attempted):
        self.assert_frozen()
        matches = [(rid, row) for rid, row in self.data["routes"].items() if all(row["declaration"][k] == v
                   for k, v in dict(provider=provider, query=query.strip(), year=year, limit=limit).items())]
        require(len(matches) == 1, "unplanned_query", "Search must match one frozen provider/query/year/page-size route")
        rid, route = matches[0]
        token = self._cursor(provider, cursor)
        page_key = digest({"route_id": rid, "cursor": token})
        repeat = page_key in self.data["pages"]
        if not repeat:
            require(not self._route_done(route), "declared_window_complete", "Extend scope explicitly before another provider page")
            expected = self._cursor(provider, route["next_cursor"]) if route["started"] else "__start__"
            require(token == expected, "invalid_cursor", "Provider cursor does not continue the exact frozen route")
            require(all(set(self.data["pages"][key]["allowed_indices"]) <= set(self.data["pages"][key]["exposed_indices"])
                        for key in route["pages"]), "metadata_not_exposed", "Expose the existing saved page before requesting another")
        require(not any(t.get("page_key") == page_key and t["status"] == "pending" for t in self.data["tickets"].values()),
                "duplicate_pending_request", "One pending request already owns this cursor")
        self._network(network_attempted)
        ticket = {"ticket_id": digest({"identity": self.identity, "sequence": len(self.history), "page_key": page_key}),
                  "route_id": rid, "page_key": page_key, "cursor": token, "network_attempted": network_attempted,
                  "repeat": repeat, "status": "pending", "kind": "search"}
        self.data["tickets"][ticket["ticket_id"]] = deepcopy(ticket)
        return {**ticket, "route": deepcopy(route["declaration"])}

    def _network(self, network_attempted):
        require(type(network_attempted) is bool, "invalid_scope", "Network observation must be a boolean")
        if network_attempted:
            require(self.data["network_attempts"] < self.limits["network_attempts"], "network_attempts_exhausted", "Provider network-attempt ceiling reached")
            self.data["network_attempts"] += 1

    def _ticket(self, ticket, kind):
        require(isinstance(ticket, dict) and ticket.get("ticket_id") in self.data["tickets"], "invalid_ticket", "Unknown scope request ticket")
        saved = self.data["tickets"][ticket["ticket_id"]]
        require(saved["status"] == "pending" and saved["kind"] == kind
                and all(ticket.get(k) == v for k, v in saved.items()), "invalid_ticket", "Request ticket differs or has already settled")
        return saved

    def record_search(self, ticket, provider_result, search_id, *, cached, network_attempted, fetched_epoch=None):
        return self._call("record_search", dict(ticket=ticket, provider_result=_compact_page(provider_result), search_id=search_id,
            cached=cached, network_attempted=network_attempted, fetched_epoch=fetched_epoch))

    def _record_search(self, ticket, provider_result, search_id, cached, network_attempted, fetched_epoch):
        saved = self._ticket(ticket, "search")
        require(type(cached) is bool and saved["network_attempted"] == network_attempted and not (cached and network_attempted),
                "invalid_scope", "Cache/network observation differs from admitted request")
        require(isinstance(provider_result, dict) and isinstance(provider_result.get("records"), list), "invalid_scope", "Invalid provider page")
        route = self.data["routes"][saved["route_id"]]
        key = saved["page_key"]
        from .literature_lookup import record_id
        ids = [record_id(row) for row in provider_result["records"]]
        if saved["repeat"]:
            page = self.data["pages"][key]
            require(page["provider_page_sha256"] == provider_result["upstream_sha256"] and page["record_ids"] == ids,
                    "page_identity_changed", "A known cursor returned changed metadata; use an explicit new scope, not overwritten evidence")
        else:
            available = route["declaration"]["max_records"] - route["admitted_records"]
            allowed = list(range(min(len(ids), available)))
            require(len(provider_result["records"]) <= route["declaration"]["limit"], "invalid_scope", "Provider page exceeds requested size")
            page = {"route_id": saved["route_id"], "cursor": saved["cursor"], "search_id": search_id,
                "provider_page_sha256": provider_result["upstream_sha256"], "record_ids": ids, "allowed_indices": allowed,
                "date_states": [metadata_date_state(row, route["declaration"]) for row in provider_result["records"]],
                "exposed_indices": [], "next_cursor": provider_result.get("next_cursor"), "total": provider_result.get("total"),
                "cached": cached, "fetched_epoch": fetched_epoch}
            self.data["pages"][key] = page
            route["pages"].append(key)
            route["admitted_records"] += len(allowed)
            route.update(started=True, terminal=not bool(provider_result.get("next_cursor")), next_cursor=provider_result.get("next_cursor"))
            require(not (route["terminal"] is False and not ids), "invalid_scope", "Empty nonterminal provider page is not progress")
            if not route["terminal"]:
                next_node = self._cursor(route["declaration"]["provider"], route["next_cursor"])
                require(all(self.data["pages"][key]["cursor"] != next_node for key in route["pages"]),
                        "invalid_cursor", "Provider cursor cycles into an already observed page")
            for i in allowed:
                self._candidate(saved["route_id"], ids[i], provider_result["records"][i])
        saved["status"] = "succeeded"
        return {"record_ids": ids, "allowed_indices": deepcopy(page["allowed_indices"]), "route_id": saved["route_id"],
                "date_states": deepcopy(page["date_states"]),
                "finite_window_complete": self._route_done(route), "provider_terminal": route["terminal"], "read_credit": False}

    def _candidate(self, route_id, identifier, row):
        candidate = self.data["candidates"].setdefault(identifier, {"record_id": identifier, "routes": [],
            "observations": [], "exposed": False, "plausible": False, "disposition": None,
            "reason": None, "source_hashes": [], "read_after_sequence": None})
        if route_id not in candidate["routes"]:
            candidate["routes"].append(route_id)
        observation = {k: deepcopy(row[k]) for k in ("paper_id", "title", "identifiers", "versions", "publication_events", "urls") if k in row}
        if observation not in candidate["observations"]:
            if candidate["observations"] and row.get("versions") and any(o.get("versions") != row["versions"] for o in candidate["observations"]):
                candidate.update(plausible=True, disposition="needs_check", reason="A newly observed version remains unverified", source_hashes=[])
                candidate["read_after_sequence"] = len(self.history)
            candidate["observations"].append(observation)

    def page_allowance(self, search_id):
        pages = [row for row in self.data["pages"].values() if row["search_id"] == search_id]
        require(len(pages) == 1, "invalid_scope", "Unknown saved metadata page")
        return deepcopy(pages[0]["allowed_indices"])

    def record_search_failure(self, ticket, error):
        return self._call("record_search_failure", {"ticket": ticket, "error": str(error)[:1200]})

    def _record_search_failure(self, ticket, error):
        saved = self._ticket(ticket, "search")
        saved.update(status="failed", error=error)
        return {"recorded": True, "network_attempt_preserved": saved["network_attempted"], "scientific_approval": False}

    def record_exposure(self, search_id, record_indices):
        return self._call("record_exposure", {"search_id": search_id, "record_indices": list(record_indices)})

    def _record_exposure(self, search_id, record_indices):
        self.assert_frozen()
        pages = [p for p in self.data["pages"].values() if p["search_id"] == search_id]
        require(len(pages) == 1 and all(type(i) is int for i in record_indices), "invalid_scope", "Unknown saved page or invalid record index")
        page = pages[0]
        require(set(record_indices) <= set(page["allowed_indices"]), "outside_finite_window", "Extend scope before exposing records outside its declared top-K window")
        ids = [page["record_ids"][i] for i in record_indices]
        new = {rid for rid in ids if not self.data["candidates"][rid]["exposed"]}
        require(self.data["exposed_metadata"] + len(new) <= self.limits["metadata_records"], "metadata_limit_exhausted", "Exposed metadata ceiling reached")
        self.data["exposed_metadata"] += len(new)
        page["exposed_indices"] = sorted(set(page["exposed_indices"]) | set(record_indices))
        for rid in ids:
            self.data["candidates"][rid]["exposed"] = True
        return {"record_ids": ids, "newly_exposed": len(new), "read_credit": False}

    def dispose(self, items, *, own_source_reads=None, source_bindings=None):
        return self._call("dispose", {"items": items, "own_source_reads": sorted(own_source_reads or []),
            "source_bindings": {k: sorted(v) for k, v in (source_bindings or {}).items()}})

    def _dispose(self, items, own_source_reads, source_bindings):
        self.assert_frozen()
        require(isinstance(items, list) and items, "invalid_scope", "Candidate dispositions must be a nonempty array")
        for item in items:
            require(isinstance(item, dict) and set(item) == {"record_id", "disposition", "reason", "source_hashes"}, "invalid_scope", "Invalid disposition fields")
            rid = item["record_id"]
            require(rid in self.data["candidates"] and self.data["candidates"][rid]["exposed"], "invalid_scope", "Disposition needs actually exposed metadata")
            candidate = self.data["candidates"][rid]
            disposition = item["disposition"]
            require(disposition in DISPOSITIONS, "invalid_scope", "Unknown operational candidate disposition")
            reason = text(item["reason"], "candidate reason", 6000)
            hashes = item["source_hashes"]
            require(isinstance(hashes, list) and len(hashes) == len(set(hashes)) and all(isinstance(h, str) and re.fullmatch(r"[0-9a-f]{64}", h) for h in hashes), "invalid_scope", "Invalid source hashes")
            if disposition == "metadata_screened_incomparable":
                require(not candidate["plausible"] and not hashes, "plausible_lead_unresolved", "A plausible lead cannot be dropped by later metadata-only screening")
            elif disposition == "needs_check":
                require(not hashes, "invalid_scope", "Pending metadata is not source verification")
                candidate["plausible"] = True
            else:
                linked = set(source_bindings.get(rid, [])) | {h for source in self.data["sources"].values()
                    if rid in source["declaration"]["record_ids"] for h in source["read_hashes"]}
                require(hashes and set(hashes) <= set(own_source_reads) and set(hashes) <= linked,
                        "required_source_unverified", "Checked candidate requires its linked actual own source reads")
                if candidate["read_after_sequence"] is not None:
                    require(any(self.data["source_read_sequences"].get(h, -1) > candidate["read_after_sequence"] for h in hashes),
                            "required_source_unverified", "A newly observed version needs a fresh linked own source check")
            candidate.update(disposition=disposition, reason=reason, source_hashes=hashes)
            self.data["own_source_reads"] = sorted(set(self.data["own_source_reads"]) | set(hashes))
        return self.completion()

    def before_lookup(self, kind, identifier, *, network_attempted=False):
        return self._call("before_lookup", dict(kind=kind, identifier=identifier, network_attempted=network_attempted))

    def _before_lookup(self, kind, identifier, network_attempted):
        self.assert_frozen()
        from .literature_lookup import canonical_identifier
        identifier = canonical_identifier(kind, identifier)
        sources = [oid for oid, row in self.data["sources"].items() if row["declaration"]["kind"] == kind
                   and row["declaration"]["identifier"] == identifier]
        require(sources, "unplanned_lookup", "Exact lookup needs a predeclared source obligation")
        self._network(network_attempted)
        ticket = {"ticket_id": digest({"identity": self.identity, "sequence": len(self.history), "source": sources[0]}),
                  "obligation_id": sources[0], "obligation_ids": sources, "kind": "lookup", "network_attempted": network_attempted, "status": "pending"}
        self.data["tickets"][ticket["ticket_id"]] = deepcopy(ticket)
        return ticket

    def record_lookup(self, ticket, result, lookup_id, *, cached, network_attempted):
        return self._call("record_lookup", dict(ticket=ticket, result=_compact_page(result), lookup_id=lookup_id,
            cached=cached, network_attempted=network_attempted))

    def _record_lookup(self, ticket, result, lookup_id, cached, network_attempted):
        saved = self._ticket(ticket, "lookup")
        require(type(cached) is bool and network_attempted == saved["network_attempted"] and not(cached and network_attempted), "invalid_scope", "Lookup cache/network mismatch")
        require(isinstance(result, dict) and isinstance(result.get("record"), dict) and isinstance(result.get("identity"), dict),
                "required_version_unchecked", "Exact lookup has no verified identity metadata")
        source = self.data["sources"][saved["obligation_id"]]
        declaration = source["declaration"]
        from .literature_lookup import canonical_identifier, record_id
        kind = declaration["kind"]
        observed = result["identity"].get("returned_version" if kind == "arxiv" and re.search(r"v\d+$", declaration["identifier"]) else kind)
        require(kind in {"doi", "arxiv", "url"} and observed is not None
                and canonical_identifier(kind, observed) == declaration["identifier"], "required_version_unchecked", "Exact metadata lookup changed source identity")
        identifiers = result["record"].get("identifiers", {})
        if kind in {"doi", "arxiv"}:
            require(kind in identifiers and canonical_identifier(kind, identifiers[kind])
                    == (re.sub(r"v\d+$", "", declaration["identifier"]) if kind == "arxiv" else declaration["identifier"]),
                    "required_version_unchecked", "Lookup record does not match its exact identity proof")
        verified = result["record"].get("metadata_status") != "publisher_page_metadata_unverified"
        source.update(metadata_checked=verified, failed=False, lookup_id=lookup_id, lookup_sha256=result["upstream_sha256"])
        source["record_id"] = record_id(result["record"])
        for alert in result.get("material_alerts", []):
            require(isinstance(alert, dict) and isinstance(alert.get("kind"), str), "invalid_scope", "Invalid material metadata alert")
            if alert not in source["material_alerts"]:
                source["material_alerts"].append(deepcopy(alert))
                source["alert_after_sequence"] = len(self.history)
        for key in ("known_baseline_versions", "official_update_metadata", "correction_status", "version_history_complete"):
            if key in result:
                source[key] = deepcopy(result[key])
        for oid in saved["obligation_ids"]:
            if oid != saved["obligation_id"]:
                other = self.data["sources"][oid]
                for key in ("metadata_checked", "failed", "lookup_id", "lookup_sha256", "record_id", "material_alerts", "alert_after_sequence",
                            "known_baseline_versions", "official_update_metadata", "correction_status", "version_history_complete"):
                    if key in source:
                        other[key] = deepcopy(source[key])
        self.data["lookup_count"] += 1
        saved["status"] = "succeeded"
        return {"metadata_checked": verified, "obligation_id": saved["obligation_id"], "theorem_read_credit": False,
                "version_history_complete": result.get("version_history_complete", False)}

    def record_lookup_failure(self, ticket, error):
        return self._call("record_lookup_failure", {"ticket": ticket, "error": str(error)[:1200]})

    def _record_lookup_failure(self, ticket, error):
        saved = self._ticket(ticket, "lookup")
        saved.update(status="failed", error=error)
        for oid in saved["obligation_ids"]:
            self.data["sources"][oid].update(failed=True, error=error)
        return {"recorded": True, "scientific_approval": False}

    def before_source(self, purpose, obligation_id, url):
        self.assert_frozen()
        require(obligation_id in self.data["sources"], "unplanned_source", "Declare source purpose before fetching")
        row = self.data["sources"][obligation_id]["declaration"]
        require(purpose in {"required", "historical_optional"} and (purpose == "required") == row["required"], "invalid_scope", "Source purpose cannot demote a required obligation")
        if row["kind"] == "url":
            require(url == row["identifier"], "invalid_scope", "Source URL differs from declared identity")
        return deepcopy(row)

    def source_fetched(self, obligation_id, source_hash):
        return self._call("source_fetched", {"obligation_id": obligation_id, "source_hash": source_hash})

    def _source_fetched(self, obligation_id, source_hash):
        self.assert_frozen()
        require(obligation_id in self.data["sources"] and isinstance(source_hash, str) and re.fullmatch(r"[0-9a-f]{64}", source_hash), "invalid_scope", "Unknown source or invalid immutable hash")
        source = self.data["sources"][obligation_id]
        if source_hash not in source["fetched_hashes"]:
            source["fetched_hashes"].append(source_hash)
        return {"fetched": True, "read_credit": False}

    def source_failed(self, obligation_id, error):
        return self._call("source_failed", {"obligation_id": obligation_id, "error": str(error)[:1200]})

    def _source_failed(self, obligation_id, error):
        self.assert_frozen()
        require(obligation_id in self.data["sources"], "unplanned_source", "Unknown source obligation")
        self.data["sources"][obligation_id].update(failed=True, error=error)
        return {"failure_recorded": True, "required": self.data["sources"][obligation_id]["declaration"]["required"], "scientific_approval": False}

    def source_checked(self, obligation_id, source_hash):
        return self._call("source_checked", {"obligation_id": obligation_id, "source_hash": source_hash})

    def _source_checked(self, obligation_id, source_hash):
        require(obligation_id in self.data["sources"] and source_hash in self.data["sources"][obligation_id]["fetched_hashes"],
                "required_source_unverified", "Own-read evidence needs the declared fetched source identity")
        source = self.data["sources"][obligation_id]
        if source_hash not in source["read_hashes"]:
            source["read_hashes"].append(source_hash)
        self.data["own_source_reads"] = sorted(set(self.data["own_source_reads"]) | {source_hash})
        self.data["source_read_sequences"][source_hash] = len(self.history)
        source["failed"] = False
        return {"obligation_id": obligation_id, "source_hash": source_hash, "host_verified_own_read": True, "scientific_approval": False}

    def _route_done(self, route):
        return route["started"] and (route["terminal"] or len(route["pages"]) >= route["declaration"]["max_pages"]
            or route["admitted_records"] >= route["declaration"]["max_records"])

    def completion(self, *, no_change=False, own_source_reads=None, source_bindings=None, report=None):
        reasons, tails, optional_pending = [], [], []
        if not self.data["plan"]:
            reasons.append("scope_not_frozen")
        for rid, route in self.data["routes"].items():
            if not self._route_done(route):
                reasons.append("declared_window_unprocessed")
            if route["started"] and not route["terminal"]:
                tails.append({"route_id": rid, "next_cursor": route["next_cursor"], "status": "provider_tail_unassessed"})
        for page in self.data["pages"].values():
            if not set(page["allowed_indices"]) <= set(page["exposed_indices"]):
                reasons.append("metadata_not_exposed")
            if len(page["allowed_indices"]) < len(page["record_ids"]):
                tails.append({"route_id": page["route_id"], "search_id": page["search_id"],
                    "record_indices": sorted(set(range(len(page["record_ids"]))) - set(page["allowed_indices"])), "status": "provider_tail_unassessed"})
        own = set(own_source_reads) if own_source_reads is not None else set(self.data["own_source_reads"])
        for row in self.data["candidates"].values():
            if row["exposed"] and row["disposition"] is None:
                reasons.append("candidate_not_classified")
            if row["exposed"] and (row["disposition"] == "needs_check" or row["disposition"] == "checked_source" and not set(row["source_hashes"]) <= own):
                reasons.append("plausible_lead_unresolved")
            if no_change and report is not None and row["disposition"] == "checked_source":
                supported = {h for finding in report.get("findings", []) if finding.get("impact") in {"no_effect", "incomparable"}
                             for h in finding.get("source_hashes", [])}
                if not set(row["source_hashes"]) <= supported:
                    reasons.append("checked_source_not_reported")
        for oid, row in self.data["sources"].items():
            if row["declaration"]["required"]:
                if row["declaration"]["verification"] == "metadata_version" and not row["metadata_checked"]:
                    reasons.append("required_version_unchecked")
                if row["declaration"]["verification"] == "primary_text" and not (set(row["read_hashes"]) & own):
                    reasons.append("required_source_unverified")
            if row["failed"] and row["declaration"]["required"]:
                reasons.append("source_failure_unresolved")
            if not row["declaration"]["required"] and (row["failed"] or not row["read_hashes"] and not row["metadata_checked"]):
                optional_pending.append({"obligation_id": oid, "kind": row["declaration"]["kind"],
                    "identifier": row["declaration"]["identifier"], "error": row.get("error"), "required": False,
                    "failed": row["failed"],
                    "reason": row["declaration"]["reason"]})
            if row["material_alerts"]:
                linked = set(row["read_hashes"])
                for candidate_source in self.data["sources"].values():
                    same_identity = all(row["declaration"][key] == candidate_source["declaration"][key] for key in ("kind", "identifier"))
                    if same_identity or row.get("record_id") in candidate_source["declaration"]["record_ids"]:
                        linked.update(candidate_source["read_hashes"])
                fresh = {h for h in linked & own if self.data["source_read_sequences"].get(h, -1) > row["alert_after_sequence"]}
                assessed = {h for finding in (report or {}).get("findings", [])
                    if finding.get("evidence_basis") == "primary_source" and finding.get("comparison_ids")
                    and (finding.get("impact") in {"no_effect", "incomparable"} if no_change else finding.get("impact") != "synthesis_only")
                    for h in finding.get("source_hashes", [])}
                if not fresh & assessed:
                    reasons.append("lookup_material_alert_unassessed")
        if any(row["status"] == "pending" for row in self.data["tickets"].values()):
            reasons.append("declared_window_unprocessed")
        return {"finite_scope_complete": not reasons, "no_change_eligible": bool(no_change and not reasons),
                "reasons": sorted(set(reasons)), "unassessed_tail": tails, "provider_exhaustion_claim": False,
                "optional_pending": optional_pending,
                "scientific_approval": False, "read_credit": False}

    def summary(self):
        return {"enabled": self.enabled, "frozen": self.data["plan"] is not None,
                "plan_hash": digest(self.data["plan"]) if self.data["plan"] is not None else None,
                "scope_sha256": digest(self.data), "distinct_queries": len(self.data["routes"]),
                "executed_distinct_queries": len({x["route_id"] for x in self.data["tickets"].values() if x["kind"] == "search"}),
                "unique_provider_pages": len(self.data["pages"]), "network_attempts": self.data["network_attempts"],
                "exposed_metadata": self.data["exposed_metadata"], "lookup_count": self.data["lookup_count"],
                "completion": self.completion()}

    def public_audit(self):
        """Inspectable finite scope, not archived tool bodies or read credit.

        The initial plan never changes. Current declarations and append-only
        extensions are shown separately, with metadata-page hashes for replay.
        Completion is recomputed from current evidence rather than copied from
        a provider/cache result or an earlier summary.
        """
        pages = []
        locations = {}
        for key, row in self.data["pages"].items():
            pages.append({"page_key": key, **{field: deepcopy(row[field]) for field in
                ("route_id", "cursor", "search_id", "provider_page_sha256", "allowed_indices",
                 "exposed_indices", "date_states", "next_cursor", "total", "cached", "fetched_epoch")},
                "record_ids": deepcopy(row["record_ids"])})
            for index in row["allowed_indices"]:
                locations.setdefault(row["record_ids"][index], []).append({"search_id": row["search_id"],
                    "record_index": index, "provider_page_sha256": row["provider_page_sha256"],
                    "exposed": index in row["exposed_indices"]})
        candidates = []
        for rid, row in self.data["candidates"].items():
            observations = [{"metadata_sha256": digest(observation), **{field: deepcopy(observation[field])
                for field in ("paper_id", "title", "identifiers", "publication_events", "versions")
                if field in observation}} for observation in row["observations"]]
            candidates.append({"record_id": rid, "candidate_sha256": digest(row),
                "title": row["observations"][-1].get("title") if row["observations"] else None,
                **{field: deepcopy(row[field]) for field in
                ("routes", "exposed", "plausible", "disposition", "reason", "source_hashes")},
                "observations": observations, "metadata_locations": locations.get(rid, [])})
        sources = []
        for oid, row in self.data["sources"].items():
            source = {"obligation_id": oid, **{field: deepcopy(row[field]) for field in
                ("declaration", "fetched_hashes", "read_hashes", "metadata_checked", "failed", "material_alerts",
                 "lookup_id", "lookup_sha256", "record_id", "known_baseline_versions", "official_update_metadata",
                 "correction_status", "version_history_complete") if field in row}}
            if row.get("error") is not None:
                source["error_sha256"] = digest(row["error"])
            sources.append(source)
        lookups, extensions = [], []
        for event in self.history:
            arguments = event["arguments"]
            if event["operation"] == "record_lookup":
                result = arguments["result"]
                record = result.get("record", {})
                lookups.append({"lookup_id": arguments["lookup_id"],
                    "obligation_ids": deepcopy(arguments["ticket"]["obligation_ids"]),
                    "provider_result_sha256": result["upstream_sha256"],
                    "cached": arguments["cached"], "network_attempted": arguments["network_attempted"],
                    "record": {field: deepcopy(record[field]) for field in
                        ("paper_id", "title", "identifiers", "publication_events", "versions", "metadata_status") if field in record},
                    **{field: deepcopy(result[field]) for field in
                        ("identity", "latest_version_verified", "requested_version", "version_history_complete",
                         "metadata_response_sha256", "material_alerts", "known_baseline_versions",
                         "official_update_metadata", "correction_status") if field in result}})
            elif event["operation"] == "extend":
                extension = arguments["extension"]
                extensions.append({"sequence": event["sequence"], "reason": extension["reason"],
                    "extension": deepcopy(extension), "extension_sha256": digest(extension), "event_hash": event["event_hash"]})
        completion = self.completion()
        for pending in completion["optional_pending"]:
            error = pending.pop("error", None)
            if error is not None:
                pending["error_sha256"] = digest(error)
        return {"version": 1, "enabled": self.enabled, "frozen": self.data["plan"] is not None,
            "plan": deepcopy(self.data["plan"]),
            "plan_hash": digest(self.data["plan"]) if self.data["plan"] is not None else None,
            "scope_sha256": digest(self.data), "limits": deepcopy(self.limits),
            "routes": [{"route_id": rid, "declaration": deepcopy(row["declaration"]),
                "coverage": {field: deepcopy(row[field]) for field in
                    ("started", "terminal", "next_cursor", "admitted_records")},
                "page_keys": deepcopy(row["pages"]), "finite_window_complete": self._route_done(row)}
                for rid, row in self.data["routes"].items()],
            "pages": pages, "candidates": candidates, "source_obligations": sources,
            "lookups": lookups, "extensions": extensions,
            "counters": {field: self.data[field] for field in ("network_attempts", "exposed_metadata", "lookup_count")},
            "completion": completion, "scientific_approval": False, "read_credit": False}

    def state(self):
        return {"version": 1, "enabled": self.enabled, "identity": deepcopy(self.identity), "limits": deepcopy(self.limits),
                "data": deepcopy(self.data), "history": deepcopy(self.history)}

    def restore(self, state):
        require(isinstance(state, dict) and state.get("identity") == self.identity and state.get("limits") == self.limits
                and state.get("enabled") == self.enabled and state.get("version") == 1, "invalid_replay", "Finite scope belongs to another frozen identity or budget")
        fresh = FiniteScope(self.context, self.config)
        for event in state.get("history", []):
            require(isinstance(event, dict) and event.get("operation") in {"freeze", "extend", "before_search", "record_search", "record_search_failure",
                    "record_exposure", "dispose", "before_lookup", "record_lookup", "record_lookup_failure", "source_fetched", "source_checked", "source_failed"}, "invalid_replay", "Unknown finite-scope operation")
            fresh._call(event["operation"], event["arguments"])
            require(digest(fresh.history[-1]) == digest(event), "invalid_replay", "Finite-scope history/hash chain changed")
        require(digest(fresh.state()) == digest(state), "invalid_replay", "Finite-scope snapshot differs from its complete event replay")
        self.data, self.history = fresh.data, fresh.history


FiniteScopeManager = FiniteScope
