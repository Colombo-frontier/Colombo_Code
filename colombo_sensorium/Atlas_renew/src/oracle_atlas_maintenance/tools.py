"""Bounded, read-only access to one frozen setting and shared literature evidence.

The controller alone may write profiles. Tool results and source text are untrusted
reference material; cache presence never grants mathematical applicability.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import time
import unicodedata
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from oracle_atlas.discovery.bibliography import Bibliography
from oracle_atlas.discovery.http import HTTPClient, atomic_write, display_url
from oracle_atlas.discovery.sources import fetch_source

from .literature_lookup import canonical_identifier, lookup_metadata, record_id


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha(value: Any) -> str:
    return hashlib.sha256(_json(value).encode()).hexdigest()


def _strict_json(text):
    def reject_constant(value):
        raise ValueError(f"Non-finite constant is not standard JSON: {value}")
    return json.loads(text, parse_constant=reject_constant)


def _parse_handoff_report(report_json, schema):
    """Strictly parse the original role report and every embedded *_json value."""
    report = _strict_json(report_json)
    if not isinstance(report, dict):
        raise ValueError("A handoff must encode one JSON object")
    errors = []
    def parse_nested(value, pointer="", depth=0):
        if depth > 64:
            errors.append({"pointer": pointer, "message": "Nested JSON exceeds the supported validation depth"})
            return
        if isinstance(value, dict):
            for key, child in value.items():
                loc = pointer + "/" + key
                if key.endswith("_json") and child is not None:
                    try:
                        parsed = _strict_json(child)
                        if json.loads(_json(parsed)) != parsed:
                            raise ValueError("Nested JSON did not round-trip")
                        parse_nested(parsed, loc + "/$parsed", depth + 1)
                    except (ValueError, TypeError, AssertionError) as exc:
                        errors.append({"pointer": loc, "message": str(exc)[:500]})
                else:
                    parse_nested(child, loc, depth + 1)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                parse_nested(child, pointer + "/" + str(index), depth + 1)
    parse_nested(report)
    for error in Draft202012Validator(schema).iter_errors(report):
        errors.append({"pointer": "/" + "/".join(map(str, error.absolute_path)), "message": error.message[:500]})
        if len(errors) >= 16:
            break
    return report, errors[:16]


def _validated_handoff_binding(host, role):
    path = getattr(host, "handoff_path", None)
    control_path = getattr(host, "run_control_path", None)
    if path is None or control_path is None:
        raise ValueError("This stage has no controller-owned validated handoff destination")
    stage = Path(path).absolute()
    if any(p.is_symlink() for p in (stage, *stage.parents)):
        raise ValueError("Validated handoff destinations must not follow symlinks")
    if Path(control_path).absolute() != stage / "run-control.json" or Path(control_path).is_symlink():
        raise ValueError("Validated handoff control must belong to the current stage")
    control = _strict_json(Path(control_path).read_text("utf-8"))
    if control.get("role") != role or control.get("stage_key") != stage.name or not re.fullmatch(r"[0-9a-f]{64}", str(control.get("request_sha256", ""))):
        raise ValueError("Validated handoff role or current stage binding does not match")
    if control.get("checkpoint_binding") != host.context.get("resume_binding"):
        raise ValueError("Validated handoff resume binding changed")
    binding = {"stage_key": stage.name, "role": role, "request_sha256": control["request_sha256"],
               "resume_binding": host.context.get("resume_binding"),
               "setting_id": host.context.get("setting_id"), "base_version": host.context.get("base_version"),
               "cutoff": host.context.get("cutoff"), "prepared_hash": host.context.get("prepared_hash")}
    return stage, binding


def _object(properties: dict, required: list[str]) -> dict:
    return {"type": "object", "properties": properties, "required": required, "additionalProperties": False}


def _pointer(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    if not pointer.startswith("/"):
        raise ValueError("Use an RFC 6901 JSON Pointer, or an empty pointer for the root.")
    for part in pointer[1:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            if not part.isdecimal() or (part.startswith("0") and part != "0"):
                raise ValueError("Invalid array index in pointer.")
            value = value[int(part)]
        elif isinstance(value, dict):
            value = value[part]
        else:
            raise ValueError("Pointer traverses a scalar.")
    return value


_PAGE = {"pointer": {"type": "string"}, "offset": {"type": "integer", "minimum": 0},
         "limit": {"type": "integer", "minimum": 1, "maximum": 12000}}
_DEFINITIONS = [
    {"name": "profile_read", "description": "Read only the current frozen setting baseline at a JSON Pointer. Output is paginated serialized JSON; offsets count characters.",
     "parameters": _object(_PAGE, list(_PAGE))},
    {"name": "artifact_read", "description": "Read a frozen baseline, prepared profile, or draft joint_template. Never searches settings. Prepared is available only to its independent reviewer. A template is not approved science.",
     "parameters": _object({"name": {"type": "string", "enum": ["baseline", "prepared", "joint_template", "continuation_work", "budgeting_previews"]}, **_PAGE}, ["name", *_PAGE])},
    {"name": "bibliography_search", "description": "Search one page of literature metadata. This discovers leads, not verified theorems. Window dates are research scope; inspect publication/revision dates and apply native provider query syntax when filtering. next_cursor explicitly reports unexamined pages.",
     "parameters": _object({"provider": {"type": "string", "enum": ["arxiv", "crossref", "openalex"]},
          "query": {"type": "string", "minLength": 1, "maxLength": 3000},
          "year": {"type": ["integer", "null"], "minimum": 1000, "maximum": 9999},
          "cursor": {"type": ["string", "null"], "maxLength": 1000},
          "limit": {"type": "integer", "minimum": 1, "maximum": 25}}, ["provider", "query", "year", "cursor", "limit"])},
    {"name": "bibliography_read", "description": "Read omitted record indices from an already downloaded bibliography page, without HTTP or another search. Continue next_record_offset until null; next_cursor remains a separate provider-page obligation.",
     "parameters": _object({"search_id": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
          "offset": {"type": "integer", "minimum": 0}, "limit": {"type": "integer", "minimum": 1, "maximum": 25}}, ["search_id", "offset", "limit"])},
    {"name": "search_replace", "description": "Explicitly refine a noisy successful metadata query to a distinct, fully exposed terminal replacement query. Archives the old corpus/cursors and reason; retiring a query does not claim its corpus was exhausted. Cannot retire unread metadata, self-reference, or a failed/retired/nonterminal replacement.",
     "parameters": _object({"search_id": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
          "replacement_search_id": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
          "reason": {"type": "string", "minLength": 1, "maxLength": 3000}}, ["search_id", "replacement_search_id", "reason"])},
    {"name": "source_fetch", "description": "Archive a public primary-source HTML/PDF/text URL. Identify the theorem's original paper/version, correction or withdrawal; metadata/abstracts are not theorem evidence. Fetch alone does not mark text read.",
     "parameters": _object({"url": {"type": "string", "minLength": 1, "maxLength": 10000}}, ["url"])},
    {"name": "source_read", "description": "Read an immutable source version by SHA256. Cite this hash and a precise theorem/page/character locator. Text extraction may lose mathematical notation; verify any decisive uncertain formula.",
     "parameters": _object({"source_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
          "offset": {"type": "integer", "minimum": 0}, "limit": {"type": "integer", "minimum": 1, "maximum": 12000}}, ["source_hash", "offset", "limit"])},
    {"name": "source_find", "description": "Locate a literal in a granted, hash-verified archived source and return bounded text offsets/snippets. Use source_read at the decisive range; finding a literal does not count as reading theorem evidence.",
     "parameters": _object({"source_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
          "literal": {"type": "string", "minLength": 1, "maxLength": 2000},
          "limit": {"type": "integer", "minimum": 1, "maximum": 10}}, ["source_hash", "literal", "limit"])},
    {"name": "failure_resolve", "description": "Explicitly link a transient failed call to a successful replacement event and explain why it covers the same obligation. Source failures require a successful nonempty source_read; discovery failures require successful bibliography discovery/read. Budget exhaustion cannot be resolved. All historical events remain archived.",
     "parameters": _object({"failure_id": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
          "replacement_event_id": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
          "reason": {"type": "string", "minLength": 1, "maxLength": 3000}}, ["failure_id", "replacement_event_id", "reason"])},
    {"name": "maintenance_status", "description": "Read the current stage deadline, remaining budgets and cooperative close request. Operational status is not scientific evidence or a successful check.",
     "parameters": _object({}, [])},
    {"name": "checkpoint_save", "description": "Save bounded UNAPPROVED working progress for an explicit later continuation. Save after baseline triage and each material research phase. This never publishes, validates a theorem, resolves a failure or grants another attempt reading credit. draft_report_json may be null; a non-null draft is mechanically parsed only.",
     "parameters": _object({"phase": {"type": "string", "enum": ["baseline", "discovery", "source_verification", "synthesis", "handoff"]},
          "summary": {"type": "string", "maxLength": 6000},
          "pending_obligations": {"type": "array", "maxItems": 40, "items": {"type": "string", "maxLength": 2000}},
          "next_actions": {"type": "array", "maxItems": 20, "items": {"type": "string", "maxLength": 2000}},
          "draft_report_json": {"type": ["string", "null"], "maxLength": 120000}},
          ["phase", "summary", "pending_obligations", "next_actions", "draft_report_json"])},
    {"name": "checkpoint_read", "description": "Read pages of this stage's own unapproved working checkpoint. No previous approval or source-reading credit is inherited.",
     "parameters": _object(_PAGE, list(_PAGE))},
    {"name": "handoff_validate", "description": "Actually parse a serialized draft handoff and its nested JSON strings, and validate the role schema. Returns mechanical errors without changing the draft or granting scientific approval. Use this instead of requesting shell/Python execution.",
     "parameters": _object({"role": {"type": "string", "enum": ["scout", "reviewer"]},
          "report_json": {"type": "string", "maxLength": 150000}}, ["role", "report_json"])},
]

_DISCOVERY_DEFINITIONS = [
    {"name": "research_scope_freeze", "description": "Freeze the finite research routes, dates, top-K/page limits and required/optional source obligations BEFORE any literature access. This declares finite coverage, never exhaustive literature or theorem verification.",
     "parameters": _object({"plan_json": {"type": "string", "minLength": 2, "maxLength": 30000}}, ["plan_json"])},
    {"name": "research_scope_extend", "description": "Append explicit routes or increase a declared finite page/top-K window. Existing routes, exposed candidates, failures and source obligations cannot be erased or shrunk.",
     "parameters": _object({"extension_json": {"type": "string", "minLength": 2, "maxLength": 20000}}, ["extension_json"])},
    {"name": "candidate_dispositions", "description": "Batch dispositions for stable IDs of metadata actually exposed in this stage. Metadata screening is not theorem evidence. checked_source requires linked source hashes actually read in this stage; unresolved checks remain pending.",
     "parameters": _object({"items": {"type": "array", "minItems": 1, "maxItems": 100, "items": _object({
         "record_id": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
         "disposition": {"type": "string", "enum": ["metadata_screened_incomparable", "needs_check", "checked_source"]},
         "reason": {"type": "string", "minLength": 1, "maxLength": 3000},
         "source_hashes": {"type": "array", "uniqueItems": True, "maxItems": 16, "items": {"type": "string", "pattern": "^[0-9a-f]{64}$"}}},
         ["record_id", "disposition", "reason", "source_hashes"])}}, ["items"])},
    {"name": "bibliography_lookup", "description": "Resolve one exact DOI, arXiv ID/version or public primary URL to bounded identity/revision metadata. Known DOI uses exact lookup, never broad title search. Metadata lookup grants no source hash or theorem-reading credit; unresolved version history remains explicit.",
     "parameters": _object({"kind": {"type": "string", "enum": ["doi", "arxiv", "url"]},
         "identifier": {"type": "string", "minLength": 1, "maxLength": 10000}}, ["kind", "identifier"])},
]


class MaintenanceTools:
    """Each instance has one setting's budget; cache entries can be shared across settings."""
    def __init__(self, atlas_root: Path, cache_dir: Path, context: dict, config: dict):
        self.atlas_root = Path(atlas_root).resolve()
        self.cache_dir = Path(cache_dir).resolve()
        self.context, self.config = copy.deepcopy(context), copy.deepcopy(config)
        self.budgets = config.get("budgets", {})
        self.search_log: list[dict] = []
        self.source_log: list[dict] = []
        self.events: list[dict] = []
        self.budget_exhausted = False
        self.failed = False
        self._searches = self._sources = self._reads = self._finds = 0
        self._fetch_attempts = 0
        self._failures: dict[str, dict] = {}
        self._search_pages: dict[str, dict] = {}
        self._persistent_failed = False
        self._orphan_failure_ids = set()
        self.grants = set(context.get("allowed_source_hashes", []))
        self.artifacts = self.context.get("artifacts", {})
        if "baseline" not in self.artifacts:
            sid = context.get("setting_id", "")
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,199}", sid):
                raise ValueError("Invalid existing setting ID.")
            data = self.atlas_root / "data" if (self.atlas_root / "data" / "settings").is_dir() else self.atlas_root
            path = data / "settings" / sid / "profile.json"
            if not path.resolve().is_relative_to((data / "settings").resolve()):
                raise ValueError("Setting path escapes Atlas.")
            self.artifacts["baseline"] = json.loads(path.read_text("utf-8"))
        self._bibliography = None
        self._lookup_log = []
        self._lookup_records = {}
        self._source_declarations = []
        self._finite_scope = None
        if self.budgets.get("finite_research_scope") is True:
            from .finite_scope import FiniteScope
            self._finite_scope = FiniteScope(self.context, self.config)
            if self.context.get("maintenance_role") == "reviewer" and self.context.get("finite_verification_plan") is not None:
                self._finite_scope.freeze(copy.deepcopy(self.context["finite_verification_plan"]))

    def specs(self) -> list[dict]:
        definitions = copy.deepcopy(_DEFINITIONS)
        if self._finite_scope is not None:
            definitions += copy.deepcopy(_DISCOVERY_DEFINITIONS)
            next(x for x in definitions if x["name"] == "artifact_read")["parameters"]["properties"]["name"]["enum"].append("scout_research_scope")
            fetch = next(x for x in definitions if x["name"] == "source_fetch")["parameters"]
            fetch["properties"].update(purpose={"type": "string", "enum": ["required", "historical_optional"]},
                                       obligation_id={"type": "string", "minLength": 1, "maxLength": 200})
            fetch["required"] = ["url", "purpose", "obligation_id"]
        return [{"type": "function", **item, "strict": True} for item in definitions]

    def _limit(self, name: str, default: int) -> int:
        return max(1, int(self.budgets.get(name, default)))

    def _page(self, value: Any, pointer: str, offset: int, limit: int) -> dict:
        selected = _pointer(value, pointer)
        # Native transport canonicalizes object order before the server loads it.
        # Page offsets and exact-read checks must use identical bytes in every backend.
        text = json.dumps(selected, ensure_ascii=False, indent=2, sort_keys=True)
        count = min(limit, self._limit("max_tool_chars", 10000))
        if offset > len(text):
            raise ValueError("Offset exceeds this artifact's serialized length.")
        return {"pointer": pointer, "offset": offset, "text": text[offset:offset + count],
                "total_characters": len(text), "next_offset": offset + count if offset + count < len(text) else None,
                "sha256": hashlib.sha256(text.encode()).hexdigest(), "content_hash": _sha(selected),
                "hash_note": "content_hash is the canonical hash of the complete selected value; copy it as patch.before_hash.",
                "untrusted_reference_data": True}

    def call(self, name: str, arguments: dict) -> dict:
        event_id = self._event_id(name, arguments)
        try:
            if len(self.events) >= self._limit("max_tool_calls_per_stage", 40):
                self.budget_exhausted = True
                raise RuntimeError("The fixed stage tool budget is exhausted; finish with explicit pending obligations")
            definition = next((d for d in self.specs() if d["name"] == name), None)
            if definition is None:
                raise ValueError("Tool is not authorized.")
            Draft202012Validator(definition["parameters"]).validate(arguments)
            execution = self._execution_status()
            if self._finite_scope is not None and name in {"bibliography_search", "bibliography_read", "bibliography_lookup",
                                                          "source_fetch", "source_read", "source_find", "search_replace"}:
                self._finite_scope.assert_frozen()
            if execution.get("close_requested") and name in {"bibliography_search", "bibliography_lookup", "source_fetch"}:
                raise RuntimeError("Stage is closing: do not start new network research; save pending work and return an honest incomplete result")
            from .cache_control import cache_operation
            with cache_operation(self.cache_dir, name, arguments, self.config,
                                 run_control_path=getattr(self, "run_control_path", None),
                                 network_needed=lambda: self._needs_network(name, arguments)):
                if name == "profile_read":
                    result = self._page(self.artifacts["baseline"], **arguments)
                elif name == "artifact_read":
                    args = dict(arguments)
                    artifact_name = args.pop("name")
                    if artifact_name not in self.artifacts:
                        raise ValueError("This frozen artifact is unavailable in the current role.")
                    result = self._page(self.artifacts[artifact_name], **args)
                elif name == "bibliography_search":
                    result = self._search(**arguments)
                elif name == "bibliography_read":
                    result = self._bibliography_read(**arguments)
                elif name == "search_replace":
                    result = self._search_replace(**arguments)
                elif name == "source_fetch":
                    args = dict(arguments)
                    if self._finite_scope is not None:
                        self._source_obligation = self._declare_source(**args)
                        self._source_purpose = args["purpose"]
                        args = {"url": args["url"]}
                    result = self._fetch(**args)
                elif name == "source_read":
                    result = self._read(**arguments)
                elif name == "source_find":
                    result = self._find(**arguments)
                elif name == "maintenance_status":
                    result = self._execution_status()
                elif name == "checkpoint_save":
                    result = self._checkpoint_save(**arguments)
                elif name == "checkpoint_read":
                    result = self._checkpoint_read(**arguments)
                elif name == "handoff_validate":
                    result = self._handoff_validate(**arguments)
                elif name == "research_scope_freeze":
                    result = self._scope_freeze(**arguments)
                elif name == "research_scope_extend":
                    result = self._scope_extend(**arguments)
                elif name == "candidate_dispositions":
                    result = self._candidate_dispositions(**arguments)
                elif name == "bibliography_lookup":
                    result = self._lookup(**arguments)
                else:
                    result = self._failure_resolve(**arguments)
                if self._finite_scope is not None and not result.get("error"):
                    self._source_scope_effect(name, arguments, result)
        except Exception as exc:
            result = {"error": str(exc)[:1200], "error_type": type(exc).__name__,
                      "budget_exhausted": self.budget_exhausted, "complete": False,
                      "failure_id": event_id}
            if isinstance(getattr(exc, "details", None), dict):
                details = copy.deepcopy(exc.details)
                encoded = _json(details)
                result["details"] = details if len(encoded) <= 12000 else {
                    "truncated": True, "characters": len(encoded), "sha256": _sha(details)}
            if name in {"bibliography_search", "bibliography_lookup"}:
                result["audit"] = {**arguments, "success": False, **result}
                if self._finite_scope is not None and name == "bibliography_search":
                    result["audit"]["finite_provider_attempt"] = copy.deepcopy(getattr(self, "_finite_provider_attempt", None))
                if self._finite_scope is not None and name == "bibliography_lookup":
                    result["audit"]["finite_lookup_attempt"] = copy.deepcopy(getattr(self, "_finite_lookup_attempt", None))
                (self.search_log if name == "bibliography_search" else self._lookup_log).append(result["audit"])
            elif name in {"source_fetch", "source_read", "source_find"}:
                public_arguments = copy.deepcopy(arguments)
                if name == "source_fetch" and (self._finite_scope is not None or self.budgets.get("source_recovery") is True) and isinstance(arguments.get("url"), str):
                    public_arguments["url"] = display_url(arguments["url"])
                    public_arguments["requested_url"] = display_url(arguments["url"])
                    public_arguments["requested_url_sha256"] = hashlib.sha256(arguments["url"].encode()).hexdigest()
                result["audit"] = {"tool": name, **public_arguments, "success": False, **result}
                self.source_log.append(result["audit"])
                if self._finite_scope is not None:
                    obligations = self._source_failure_obligations(name, arguments)
                    result["audit"]["finite_source_failure_obligations"] = obligations
                    for oid in obligations:
                        self._finite_scope.source_failed(oid, result["error"])
        finally:
            # The callback and dispatcher must agree at one cache admission
            # instant, even if wall time crosses the TTL boundary between them.
            # This is per-operation state, never inherited by a later tool call.
            self.__dict__.pop("_cache_admission_epoch", None)
            self.__dict__.pop("_finite_provider_attempt", None)
            self.__dict__.pop("_finite_lookup_attempt", None)
            self.__dict__.pop("_source_obligation", None)
            self.__dict__.pop("_source_purpose", None)
        result["event_id"] = event_id
        if isinstance(result.get("audit"), dict):
            result["audit"]["event_id"] = event_id
        self._record_effect(name, arguments, result)
        self.events.append({"tool": name, "arguments": copy.deepcopy(arguments), "result": copy.deepcopy(result)})
        result["budget_remaining"] = self.budget_remaining()
        execution = self._execution_status()
        if execution:
            result["execution_status"] = execution
        if len(self.events) >= 0.6 * self._limit("max_tool_calls_per_stage", 40):
            result["budget_hint"] = "At least 60% of tool calls used: finish any supported delta; keep other leads explicitly pending."
        self.events[-1]["result"] = copy.deepcopy(result)
        if self._finite_scope is not None:
            result["finite_scope_state_sha256"] = _sha(self._finite_scope.state())
            self.events[-1]["result"] = copy.deepcopy(result)
        return result

    def _needs_network(self, name, arguments):
        """Under the cache lock, skip provider delay only for the exact valid cache hit.

        This is a scheduling hint, never a source grant or reading credit. The
        original implementation repeats its immutable-content checks and audit.
        """
        self._cache_admission_epoch = time.time()
        now = self._cache_admission_epoch
        try:
            if name == "bibliography_lookup":
                key = self._lookup_key(**arguments)
                item = _strict_json((self.cache_dir / "lookups" / (_sha(key) + ".json")).read_text("utf-8"))
                ttl = max(0, float(self.config.get("cache", {}).get("search_ttl_seconds", 21600)))
                return not (0 <= now - item["saved_epoch"] <= ttl and item.get("sha256") == _sha(item["result"]))
            if name == "bibliography_search":
                key = {"provider": arguments["provider"], "query": arguments["query"].strip(),
                       "year": arguments["year"], "cursor": arguments["cursor"], "limit": arguments["limit"],
                       "window_start": self.context.get("window_start"), "cutoff": self.context.get("cutoff"), "version": 1}
                path = self.cache_dir / "search" / (_sha(key) + ".json")
                item = json.loads(path.read_text("utf-8"))
                ttl = max(0, float(self.config.get("cache", {}).get("search_ttl_seconds", 21600)))
                return not (0 <= now - item["saved_epoch"] <= ttl and item.get("sha256") == _sha(item["result"]))
            if name == "source_fetch":
                key = hashlib.sha256(arguments["url"].encode()).hexdigest()
                item = json.loads((self.cache_dir / "source_urls" / (key + ".json")).read_text("utf-8"))
                ttl = max(0, float(self.config.get("cache", {}).get("source_ttl_seconds", 21600)))
                if not 0 <= now - item["saved_epoch"] <= ttl:
                    return True
                metadata = json.loads((self.cache_dir / "sources/metadata" / (item["source_hash"] + ".json")).read_text("utf-8"))
                raw = (self.cache_dir / "sources/text" / (item["source_hash"] + ".txt")).read_bytes()
                if hashlib.sha256(raw).hexdigest() != metadata.get("text_sha256"):
                    return True
                if self.budgets.get("source_recovery") is True:
                    originals = list((self.cache_dir / "sources/originals").glob(item["source_hash"] + ".*"))
                    if len(originals) != 1 or any(p.is_symlink() for p in (originals[0], *originals[0].parents)):
                        return True
                    maximum = int(self.config.get("literature", {}).get("max_source_file_bytes", 80000000))
                    if not originals[0].is_file() or originals[0].stat().st_size > maximum:
                        return True
                    digest = hashlib.sha256()
                    with originals[0].open("rb") as stream:
                        for chunk in iter(lambda: stream.read(1048576), b""):
                            digest.update(chunk)
                    if digest.hexdigest() != item["source_hash"]:
                        return True
                return False
        except (KeyError, ValueError, TypeError, OSError):
            return True
        return name in {"bibliography_search", "bibliography_lookup", "source_fetch"}

    def _execution_status(self):
        path = getattr(self, "run_control_path", None)
        if path is None:
            return {"finite_research_scope": self._finite_scope.summary()} if self._finite_scope is not None else {}
        control = json.loads(Path(path).read_text("utf-8"))
        now = time.monotonic_ns()
        remaining = max(0.0, (control["hard_deadline_monotonic_ns"] - now) / 1e9)
        soft_remaining = max(0.0, (control["soft_deadline_monotonic_ns"] - now) / 1e9)
        closing = bool(control.get("close_requested")) or soft_remaining == 0
        result = {"remaining_seconds": round(remaining, 3), "research_seconds_remaining": round(soft_remaining, 3),
                "close_requested": closing,
                "instruction": "Stop new research, save unapproved progress, and finalize supported work or incomplete now." if closing else "Save a checkpoint after each research phase; reserve time for the final handoff.",
                "budget_remaining": self.budget_remaining()}
        if self._finite_scope is not None:
            result["finite_research_scope"] = self._finite_scope.summary()
        return result

    def _checkpoint_binding(self):
        binding = {key: self.context.get(key) for key in
                   ("setting_id", "base_version", "cutoff", "policy", "semantics", "contract_hash", "resume_binding")}
        control_path = getattr(self, "run_control_path", None)
        if control_path is None:
            raise ValueError("Checkpoint requires a controller-owned stage identity")
        control = json.loads(Path(control_path).read_text("utf-8"))
        identity = {k: control.get(k) for k in ("stage_key", "role", "request_sha256")}
        if any(not isinstance(value, str) or not value for value in identity.values()):
            raise ValueError("Checkpoint requires exact stage, role and request identity")
        binding["stage_identity"] = identity
        return binding

    def _checkpoint_destination(self):
        path = getattr(self, "checkpoint_path", None)
        if path is None:
            raise ValueError("This role has no controller-owned checkpoint destination")
        path = Path(path).absolute()
        if any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError("Checkpoint destinations must not follow symlinks")
        return path

    def _checkpoint_save(self, **progress):
        path = self._checkpoint_destination()
        draft = progress.get("draft_report_json")
        if draft is not None:
            parsed = _strict_json(draft)
            if not isinstance(parsed, dict):
                raise ValueError("draft_report_json must encode one JSON object")
        material = {"kind": "unapproved_working_checkpoint", "version": 1,
                    "binding": self._checkpoint_binding(), "progress": progress,
                    "event_count_before_save": len(self.events),
                    "source_hashes": sorted(self.grants),
                    "note": "Working memory only. Fresh own reads, source applicability, prepared hashes and independent review remain mandatory."}
        record = {**material, "checkpoint_hash": _sha(material)}
        snapshot = path.with_name(f"checkpoint-{len(self.events):06d}.json")
        if snapshot.exists():
            raise ValueError("Checkpoint snapshot identity already exists")
        atomic_write(snapshot, (_json(record) + "\n").encode())
        atomic_write(path, (_json(record) + "\n").encode())
        return {"saved": True, "checkpoint_hash": record["checkpoint_hash"], "phase": progress["phase"],
                "scientific_approval": False, "reading_credit": False}

    def _checkpoint_read(self, **arguments):
        path = self._checkpoint_destination()
        if not path.is_file():
            raise ValueError("No working checkpoint has been saved in this stage")
        record = json.loads(Path(path).read_text("utf-8"))
        material = {k: v for k, v in record.items() if k != "checkpoint_hash"}
        if record.get("checkpoint_hash") != _sha(material) or record.get("binding") != self._checkpoint_binding():
            raise ValueError("Working checkpoint hash or frozen-stage binding changed")
        return self._page(record, **arguments)

    def _scout_controller_preflight(self, report):
        """Repeat available original pre-writer gates without adopting any result."""
        from .contracts import check_scope, apply_delta, affected_comparisons
        from .joint import validate_joint_analysis
        from .evidence_basis import check_evidence_basis
        from .analysis_reuse import require_own_analysis_read
        baseline = self.artifacts["baseline"]
        errors, checks = [], []
        def run_gate(name, action):
            try:
                result = action()
            except ValueError as exc:
                diagnostic = {"pointer": "", "code": "controller_mechanical", "gate": name, "message": str(exc)[:3000]}
                if name == "apply_delta" and isinstance(getattr(exc, "details", None), dict):
                    diagnostic["details"] = copy.deepcopy(exc.details)
                errors.append(diagnostic)
                checks.append({"gate": name, "valid": False})
                return None
            checks.append({"gate": name, "valid": True})
            return result
        run_gate("check_scope", lambda: check_scope(report, self.context, self))
        # The authoritative engine returns incomplete before requiring a full
        # analysis, source support or a prepared native profile.
        if report["outcome"] == "incomplete":
            return errors, checks
        applied = run_gate("apply_delta", lambda: apply_delta(baseline, report))
        analysis = None
        reuse = report.get("joint_analysis_reuse")
        if reuse is not None:
            def bind_reuse():
                if self.context.get("pending_work"):
                    raise ValueError("Pending working notes require a full current assessment; an analysis reference cannot resolve them")
                if reuse != self.context.get("accepted_analysis_reuse"):
                    raise ValueError("No-change reuse must bind the exact controller-qualified baseline version and joint hash")
                require_own_analysis_read(baseline, self)
                if not isinstance(baseline.get("joint_analysis"), dict):
                    raise ValueError("Qualified reuse requires a frozen baseline joint analysis")
                return copy.deepcopy(baseline["joint_analysis"])
            analysis = run_gate("qualified_analysis_reference_and_own_read", bind_reuse)
        else:
            def parse_analysis():
                if not isinstance(report.get("joint_analysis_json"), str):
                    raise ValueError("Live maintenance requires joint_analysis_json (complete body) or an eligible no-change reference")
                value = _strict_json(report["joint_analysis_json"])
                if not isinstance(value, dict):
                    raise ValueError("Live joint_analysis_json must encode a complete joint-analysis object")
                return value
            analysis = run_gate("parse_joint_analysis", parse_analysis)
        if applied is not None:
            proposed, delta = applied
            expected = self.context["compact_profile"]["comparison_ids"] if report["outcome"] == "no_change" else sorted(affected_comparisons(baseline, proposed, delta))
            if analysis is not None:
                run_gate("validate_joint_analysis", lambda: validate_joint_analysis(analysis, baseline, proposed,
                    report=report, expected_comparison_ids=expected, require_current=reuse is None))
            # Independent evidence diagnostics are useful even when the joint
            # representation has another mechanical error; the engine repeats
            # both original gates before constructing a native writer.
            if report["outcome"] == "candidate_change":
                run_gate("check_evidence_basis", lambda: check_evidence_basis(report, baseline, proposed, self))
        return errors, checks

    def _handoff_validate(self, role, report_json):
        from .runtime import _instructions
        _, schema, _ = _instructions(role)
        try:
            report, errors = _parse_handoff_report(report_json, schema)
        except (ValueError, TypeError) as exc:
            return {"mechanically_valid": False, "errors": [{"pointer": "", "message": str(exc)[:500]}],
                    "scientific_approval": False, "prepared_or_review_gate_waived": False}
        controller_mechanical, controller_checks = "not_applicable", []
        if not errors and role == "scout" and "baseline" in self.artifacts and "compact_profile" in self.context:
            controller_mechanical = "checked"
            extra_errors, controller_checks = self._scout_controller_preflight(report)
            errors.extend(extra_errors)
        result = {"mechanically_valid": not errors, "report_hash": _sha(report), "errors": errors,
                  "controller_mechanical": controller_mechanical, "controller_checks": controller_checks,
                  "controller_only_gates": "External acceptance/certificate pins, completed finite-search evidence, native preparation and independent review remain authoritative engine checks.",
                  "scientific_approval": False, "prepared_or_review_gate_waived": False}
        if not errors and self.config.get("observability", {}).get("compact_handoff", False):
            stage, binding = _validated_handoff_binding(self, role)
            report_hash = _sha(report)
            material = {"kind": "mechanically_validated_handoff", "schema_version": 1, "binding": binding,
                        "report_hash": report_hash, "report": report, "scientific_approval": False,
                        "prepared_or_review_gate_waived": False}
            record = {**material, "record_hash": _sha(material)}
            path = stage / ("validated-handoff-" + report_hash + ".json")
            if path.is_symlink():
                raise ValueError("Validated handoff files must not follow symlinks")
            raw = (_json(record) + "\n").encode()
            if path.exists():
                if path.read_bytes() != raw:
                    raise ValueError("An immutable validated handoff artifact already differs")
            else:
                atomic_write(path, raw)
            result.update(validated_handoff_ref=path.name, handoff_record_hash=record["record_hash"],
                          handoff_file_sha256=hashlib.sha256(raw).hexdigest())
        return result

    def budget_remaining(self):
        result = {"tool_calls": max(0, self._limit("max_tool_calls_per_stage", 40) - len(self.events)),
                "searches": max(0, self._limit("max_searches_per_setting", 3) - self._searches),
                "fetches": max(0, self._limit("max_sources_per_setting", 3) - self._sources),
                "fetch_attempts": max(0, self._limit("max_source_attempts_per_setting", 2 * self._limit("max_sources_per_setting", 3)) - self._fetch_attempts),
                "reads": max(0, self._limit("max_source_reads_per_setting", 12) - self._reads),
                "finds": max(0, self._limit("max_source_finds_per_setting", 12) - self._finds)}
        if self._finite_scope is not None:
            state = self._finite_scope.state()
            data, limits = state["data"], state["limits"]
            result["searches"] = max(0, limits["queries"] - len(data["routes"]))
            result["discovery_network_attempts"] = max(0, limits["network_attempts"] - data["network_attempts"])
            result["metadata_records"] = max(0, limits["metadata_records"] - data["exposed_metadata"])
        return result

    def _event_id(self, name, arguments):
        return _sha({"setting_id": self.context.get("setting_id"), "base_version": self.context.get("base_version"),
                     "prepared_hash": self.context.get("prepared_hash"), "sequence": len(self.events),
                     "tool": name, "arguments": arguments})

    def _own_source_reads(self):
        return {row["source_hash"] for row in self.source_log if row.get("tool") == "source_read"
                and row.get("success") is True and row.get("characters_read", 0) > 0}

    def _scope_freeze(self, plan_json):
        plan = _strict_json(plan_json)
        from .evidence_basis import fully_read_frozen_value_or_ancestor
        own = set()
        for ref in plan.get("baseline_refs", []):
            pointer, expected = ref.get("pointer"), ref.get("sha256")
            if not isinstance(pointer, str):
                raise ValueError("Scope baseline refs require exact pointers")
            value = _pointer(self.artifacts["baseline"], pointer)
            if _sha(value) != expected or not fully_read_frozen_value_or_ancestor(self, "baseline", pointer, self.artifacts["baseline"]):
                raise ValueError("Scope proof premises require exact current baseline hashes and complete own reads")
            own.add((pointer, expected))
        result = self._finite_scope.freeze(plan, own_baseline_refs=own)
        return {"frozen": True, "scope": result, "plan_hash": result["plan_hash"],
                "note": "Finite scope declaration; no theorem or scientific approval."}

    def _scope_extend(self, extension_json):
        extension = _strict_json(extension_json)
        result = self._finite_scope.extend(extension)
        for search_id, page in self._search_pages.items():
            allowed = self._finite_scope.page_allowance(search_id)
            page.update(allowed_indices=allowed, count=len(allowed))
            for audit in page["audits"]:
                audit["output_truncated"] = page["seen"] != set(allowed)
                audit["records_exposed"] = len(page["seen"])
        return {"extended": True, "scope": result, "plan_hash": result["plan_hash"],
                "note": "Prior routes, records and unresolved obligations remain archived."}

    @staticmethod
    def _requested_source_matches(row, url):
        if row.get("requested_url_sha256") is not None:
            return row["requested_url_sha256"] == hashlib.sha256(url.encode()).hexdigest()
        return row.get("requested_url", row.get("url")) in {url, display_url(url)}

    def _candidate_dispositions(self, items):
        result = self._finite_scope.dispose(items, own_source_reads=self._own_source_reads(),
                                            source_bindings=self._candidate_source_bindings())
        return {"recorded": True, "dispositions": result, "scientific_approval": False}

    def _candidate_source_bindings(self):
        bindings = {}
        state = self._finite_scope.state()
        sources = state.get("data", {}).get("sources", {})
        obligations = [row["declaration"] for row in sources.values()]
        rows = obligations.values() if isinstance(obligations, dict) else obligations
        for obligation in rows:
            oid = obligation.get("obligation_id")
            hashes = {row["source_hash"] for row in self.source_log if row.get("tool") == "source_fetch"
                      and row.get("success") is True and any(d.get("obligation_id") == oid and self._requested_source_matches(row, d["url"])
                                                            for d in self._source_declarations)}
            for rid in obligation.get("record_ids", []):
                bindings.setdefault(rid, set()).update(hashes)
        return bindings

    def _optional_unused_source_failures(self, report):
        # No report means no assertion that an optional object is unused.
        if not isinstance(report, dict):
            return []
        strings = []
        def visit(value):
            if isinstance(value, str):
                strings.append(value)
                try:
                    parsed = _strict_json(value)
                except (ValueError, TypeError):
                    return
                if isinstance(parsed, (dict, list)):
                    visit(parsed)
            elif isinstance(value, dict):
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)
        # Transparent history/pending/scope text is not a new scientific use.
        # Fresh findings, native patches and normalization claims are uses.
        for key in ("findings", "patch", "quantity_normalizations", "normalization_requests"):
            visit(report.get(key, []))
        analysis = report.get("joint_analysis_json")
        if isinstance(analysis, str):
            try:
                analysis = _strict_json(analysis)
            except (ValueError, TypeError):
                analysis = None
        if isinstance(analysis, dict):
            for row in analysis.get("provenance", []):
                if row.get("origin") != "retained_baseline":
                    visit(row)
            for key in ("impact", "impact_findings", "findings", "quantity_normalizations"):
                visit(analysis.get(key, []))
        state = self._finite_scope.state()
        obligations = [row["declaration"] for row in state.get("data", {}).get("sources", {}).values()]
        rows = list(obligations.values()) if isinstance(obligations, dict) else obligations
        by_id = {r["obligation_id"]: r for r in rows}
        result = []
        for failure_id, failure in self._failures.items():
            if failure["name"] != "source_fetch" or failure["result"].get("budget_exhausted"):
                continue
            args = failure["arguments"]
            obligation = by_id.get(args.get("obligation_id"))
            if not obligation or obligation.get("required") is not False:
                continue
            markers = {args.get("url", ""), obligation.get("identifier", "")}
            if args.get("url"):
                markers.add(display_url(args["url"]))
            markers.update(row["source_hash"] for row in self.source_log if row.get("success") is True
                           and row.get("tool") == "source_fetch" and self._requested_source_matches(row, args.get("url", "")))
            if any(marker and any(marker in text for text in strings) for marker in markers):
                continue
            result.append(failure_id)
        return sorted(result)

    def _declare_source(self, url, purpose, obligation_id):
        obligation = self._finite_scope.before_source(purpose, obligation_id, url)
        declaration = {"url": url, "purpose": purpose, "obligation_id": obligation_id}
        if declaration not in self._source_declarations:
            self._source_declarations.append(declaration)
        return obligation

    def _source_scope_effect(self, name, arguments, result):
        if name == "source_fetch":
            self._finite_scope.source_fetched(arguments.get("obligation_id"), result["source_hash"])
        elif name == "source_read" and result.get("audit", {}).get("characters_read", 0) > 0:
            source_hash = arguments["source_hash"]
            if self.context.get("maintenance_role") == "reviewer":
                plan = self.context.get("finite_verification_plan", {})
                for obligation in plan.get("source_obligations", []):
                    if obligation.get("kind") == "source_hash" and obligation.get("identifier") == source_hash:
                        self._finite_scope.source_checked(obligation["obligation_id"], source_hash)
            for declaration in self._source_declarations:
                if any(row.get("tool") == "source_fetch" and row.get("success") is True
                       and row.get("source_hash") == source_hash and self._requested_source_matches(row, declaration["url"])
                       for row in self.source_log):
                    self._finite_scope.source_checked(declaration.get("obligation_id"), source_hash)

    def _source_failure_obligations(self, name, arguments):
        sources = self._finite_scope.state()["data"]["sources"]
        if name == "source_fetch":
            row = getattr(self, "_source_obligation", None)
            return [row["obligation_id"]] if row is not None else []
        return sorted(oid for oid, row in sources.items()
                      if arguments.get("source_hash") in row["fetched_hashes"])

    def _lookup_key(self, kind, identifier):
        key = {"kind": kind, "identifier": canonical_identifier(kind, identifier),
                "window_start": self.context.get("window_start"), "cutoff": self.context.get("cutoff"), "version": 1}
        if kind == "arxiv":
            base = re.sub(r"v\d+$", "", key["identifier"])
            frozen = _json(self.artifacts["baseline"])
            key["known_versions"] = sorted(set(re.findall(re.escape(base) + r"v[1-9]\d*", frozen)))
        return key

    def _lookup(self, kind, identifier):
        key = self._lookup_key(kind, identifier)
        cache = self.cache_dir / "lookups" / (_sha(key) + ".json")
        now = getattr(self, "_cache_admission_epoch", None)
        now = time.time() if now is None else now
        ttl = max(0, float(self.config.get("cache", {}).get("search_ttl_seconds", 21600)))
        saved, cached = None, False
        if cache.is_file():
            item = _strict_json(cache.read_text("utf-8"))
            if 0 <= now - item["saved_epoch"] <= ttl and item.get("sha256") == _sha(item["result"]):
                saved, cached = item["result"], True
        ticket = self._finite_scope.before_lookup(kind, key["identifier"], network_attempted=not cached)
        self._finite_lookup_attempt = {"ticket": ticket, "network_attempted": not cached}
        if saved is None:
            options = self.config.get("literature", {})
            client = HTTPClient(timeout=float(options.get("timeout", 30)),
                                max_bytes=min(int(options.get("max_bytes", 20000000)), 2000000), cache_ttl=0)
            bibliography = Bibliography(client=client, contact=options.get("contact"), arxiv_interval=0)
            try:
                saved = lookup_metadata(kind, key["identifier"], bibliography=bibliography, client=client,
                                        known_versions=key.get("known_versions", []))
            except Exception as exc:
                self._finite_scope.record_lookup_failure(ticket, str(exc)[:1200])
                raise
            atomic_write(cache, _json({"saved_epoch": time.time(), "sha256": _sha(saved), "result": saved}).encode())
        lookup_id = _sha({"query": key, "result_sha256": _sha(saved)})
        path = self.cache_dir / "lookup_pages" / (lookup_id + ".json")
        if not path.exists():
            atomic_write(path, _json({"query": key, "sha256": _sha(saved), "result": saved}).encode())
        self._finite_scope.record_lookup(ticket, saved, lookup_id, cached=cached, network_attempted=not cached)
        record = self._metadata_record(saved["record"])
        record["record_id"] = record_id(saved["record"])
        self._lookup_records[lookup_id] = {"key": key, "result_sha256": _sha(saved), "record_id": record["record_id"]}
        audit = {"tool": "bibliography_lookup", **key, "success": True, "cached": cached,
                 "lookup_id": lookup_id, "result_sha256": _sha(saved), "record_id": record["record_id"],
                 "source_read_credit": False, "source_grant": False}
        self._lookup_log.append(audit)
        result = {k: copy.deepcopy(v) for k, v in saved.items() if k != "record"}
        result.update(record=record, lookup_id=lookup_id, audit=audit,
                      note="Metadata identity only; fetch and actually read the exact primary source before claiming a theorem.")
        return result

    def known_primary_locations(self, obligation=None):
        """Only actual successful exact lookup locations; never model-asserted URLs."""
        locations = []
        for lookup_id, granted in self._lookup_records.items():
            item = self._immutable_metadata("lookup_pages", lookup_id)
            if obligation is not None:
                key = granted["key"]
                if key["kind"] != obligation.get("kind") or key["identifier"] != canonical_identifier(key["kind"], obligation.get("identifier", "")):
                    continue
            for url in item["result"]["record"].get("urls", []):
                try:
                    value = canonical_identifier("url", url)
                except ValueError:
                    continue
                if value not in locations:
                    locations.append(value)
        return locations

    def _record_effect(self, name, arguments, result):
        if result.get("error"):
            failure_id = result.get("failure_id", result["event_id"])
            self._failures[failure_id] = {"name": name, "arguments": copy.deepcopy(arguments), "result": result}
        else:
            for failure_id, failure in list(self._failures.items()):
                if (failure["name"] == name and failure["arguments"] == arguments and not failure["result"].get("budget_exhausted")
                        and not (self._finite_scope is not None and name == "source_fetch")):
                    self._mark_resolved(failure_id, result["event_id"], "Successful exact retry of the failed call")
        if result.get("budget_exhausted"):
            self.budget_exhausted = True
        self.failed = bool(self._failures or self._orphan_failure_ids or self._persistent_failed)

    def _mark_resolved(self, failure_id, replacement_event_id, reason):
        failure = self._failures.pop(failure_id)
        audit = failure["result"].get("audit")
        if audit is not None:
            audit.update(resolved=True, replacement_event_id=replacement_event_id, resolution_reason=reason)
        for row in self.search_log + self.source_log + self._lookup_log:
            if row.get("failure_id") == failure_id:
                row.update(resolved=True, replacement_event_id=replacement_event_id, resolution_reason=reason)
        self.failed = bool(self._failures or self._orphan_failure_ids or self._persistent_failed)

    def _failure_resolve(self, failure_id, replacement_event_id, reason):
        if not reason.strip():
            raise ValueError("A nonempty reason for equivalent coverage is required")
        if failure_id not in self._failures:
            raise ValueError("This failure is unknown or already resolved")
        failure = self._failures[failure_id]
        if failure["result"].get("budget_exhausted"):
            raise ValueError("Budget exhaustion cannot be resolved within the same stage")
        replacement = next((e for e in self.events if e["result"].get("event_id") == replacement_event_id), None)
        if replacement is None or replacement["result"].get("error"):
            raise ValueError("Replacement must be an observed successful event in this stage")
        source_tools, discovery_tools = {"source_fetch", "source_read", "source_find"}, {"bibliography_search", "bibliography_read", "bibliography_lookup"}
        original, successful = failure["name"], replacement["tool"]
        if original in source_tools:
            if successful != "source_read" or replacement["result"].get("audit", {}).get("characters_read", 0) < 1:
                raise ValueError("A source failure requires an actually read replacement source")
            if self._finite_scope is not None:
                sources = self._finite_scope.state()["data"]["sources"]
                if original == "source_fetch":
                    obligations = {failure["arguments"].get("obligation_id")}
                else:
                    failed_hash = failure["arguments"].get("source_hash")
                    obligations = set(failure["result"].get("audit", {}).get("finite_source_failure_obligations", []))
                    obligations.update(oid for oid, source in sources.items() if failed_hash in source["fetched_hashes"])
                actual_hash = replacement["arguments"].get("source_hash")
                if not any(oid in sources and actual_hash in sources[oid]["fetched_hashes"] for oid in obligations):
                    raise ValueError("A finite source failure requires an actual primary-text read linked to the same declared source obligation")
        elif original in discovery_tools:
            if successful not in discovery_tools:
                raise ValueError("A discovery failure requires successful replacement bibliography access")
        elif original != successful:
            raise ValueError("Replacement must have the same tool category")
        self._mark_resolved(failure_id, replacement_event_id, reason.strip())
        return {"resolved": True, "failure_id": failure_id, "replacement_event_id": replacement_event_id,
                "reason": reason.strip(), "note": "Coverage linkage is audited; mathematical equivalence still requires role judgment and independent review."}

    def restore(self, name: str, arguments: dict, result: dict) -> None:
        """Rehydrate recorded tool effects without another network request on model replay."""
        result = copy.deepcopy(result)
        if self._finite_scope is not None and result.get("event_id") != self._event_id(name, arguments):
            raise ValueError("Finite research event identity/sequence/arguments changed")
        result.setdefault("event_id", self._event_id(name, arguments))
        registration = None
        if self._finite_scope is not None:
            registration = self._restore_finite_before(name, arguments, result)
        if name == "bibliography_search":
            self._searches += 1
            audit = copy.deepcopy(result.get("audit", {**arguments, "success": not result.get("error"), **result}))
            self.search_log.append(audit)
            if result.get("search_id") and not result.get("error"):
                search_id = result["search_id"]
                page = self._search_pages.setdefault(search_id, {"audit": audit, "audits": [], "seen": set(),
                                              "count": result.get("page_records_total", len(result.get("records", [])))})
                page["audit"] = audit
                page["audits"].append(audit)
                if registration is not None:
                    page["finite_registration"] = registration
                    page["allowed_indices"] = registration["allowed_indices"]
                    page["count"] = len(registration["allowed_indices"])
                self._cover_search(search_id, result.get("record_indices", []))
        elif name == "bibliography_read" and not result.get("error"):
            self._cover_search(arguments["search_id"], result.get("record_indices", []))
        elif name == "search_replace" and not result.get("error"):
            self._search_replace(**arguments)
        elif name in {"source_fetch", "source_read", "source_find"}:
            if name == "source_fetch":
                self._fetch_attempts += 1
                if not result.get("error"):
                    self._sources += 1
            elif name == "source_read":
                self._reads += 1
            else:
                self._finds += 1
            self.source_log.append(copy.deepcopy(result.get("audit", {"tool": name, **arguments, "success": not result.get("error"), **result})))
            if result.get("source_hash"):
                self.grants.add(result["source_hash"])
        elif name == "failure_resolve" and not result.get("error"):
            if self._finite_scope is not None:
                expected = self._failure_resolve(**arguments)
                if any(result.get(key) != value for key, value in expected.items()):
                    raise ValueError("Replayed source failure resolution changed its verified obligation linkage")
            else:
                self._mark_resolved(arguments["failure_id"], arguments["replacement_event_id"], arguments["reason"])
        self._record_effect(name, arguments, result)
        self.events.append({"tool": name, "arguments": copy.deepcopy(arguments), "result": copy.deepcopy(result)})
        if self._finite_scope is not None:
            if not result.get("error"):
                self._source_scope_effect(name, arguments, result)
            if result.get("finite_scope_state_sha256") != _sha(self._finite_scope.state()):
                raise ValueError("Replayed finite research state differs from its exact journaled transition")
        remaining = result.get("budget_remaining", {})
        for field, attr, budget, default in (("searches", "_searches", "max_searches_per_setting", 3),
                ("fetches", "_sources", "max_sources_per_setting", 3), ("reads", "_reads", "max_source_reads_per_setting", 12),
                ("fetch_attempts", "_fetch_attempts", "max_source_attempts_per_setting", 2 * self._limit("max_sources_per_setting", 3)),
                ("finds", "_finds", "max_source_finds_per_setting", 12)):
            value = remaining.get(field)
            if isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= self._limit(budget, default):
                setattr(self, attr, self._limit(budget, default) - value)

    def _restore_finite_before(self, name, arguments, result):
        """Rebuild authoritative effects from immutable local metadata; never HTTP."""
        if not result.get("error"):
            definition = next((row for row in self.specs() if row["name"] == name), None)
            if definition is None:
                raise ValueError("Successful finite research replay used an unauthorized tool")
            Draft202012Validator(definition["parameters"]).validate(arguments)
        if name in {"source_fetch", "source_read", "source_find"} and result.get("error"):
            for oid in result.get("audit", {}).get("finite_source_failure_obligations", []):
                sources = self._finite_scope.state()["data"]["sources"]
                if oid not in sources:
                    raise ValueError("Replayed source failure changed its declared obligation")
                if name == "source_fetch":
                    self._finite_scope.before_source(arguments["purpose"], arguments["obligation_id"], arguments["url"])
                    if oid != arguments["obligation_id"]:
                        raise ValueError("Replayed source failure changed its declaration")
                elif arguments.get("source_hash") not in sources[oid]["fetched_hashes"]:
                    raise ValueError("Replayed source failure changed its source grant")
                self._finite_scope.source_failed(oid, result["error"])
            return None
        if name in {"research_scope_freeze", "research_scope_extend", "candidate_dispositions"} and not result.get("error"):
            method = {"research_scope_freeze": self._scope_freeze, "research_scope_extend": self._scope_extend,
                      "candidate_dispositions": self._candidate_dispositions}[name]
            expected = method(**arguments)
            if any(result.get(key) != value for key, value in expected.items()):
                raise ValueError("Replayed scope plan or candidate disposition differs from its journal")
        elif name == "bibliography_search":
            if result.get("error"):
                attempt = result.get("audit", {}).get("finite_provider_attempt")
                if attempt is not None:
                    ticket = self._finite_scope.before_search(**arguments, network_attempted=attempt["network_attempted"])
                    if ticket != attempt["ticket"]:
                        raise ValueError("Replayed failed search ticket changed")
                    self._finite_scope.record_search_failure(ticket, result["error"])
                return None
            search_id = result["search_id"]
            item = self._immutable_metadata("search_pages", search_id)
            query = item["query"]
            expected_query = {**arguments, "query": arguments["query"].strip(),
                              "window_start": self.context.get("window_start"), "cutoff": self.context.get("cutoff"), "version": 1}
            if query != expected_query:
                raise ValueError("Replayed bibliography page belongs to another exact query/window")
            audit = result["audit"]
            ticket = self._finite_scope.before_search(**arguments, network_attempted=not audit["cached"])
            registration = self._finite_scope.record_search(ticket, item["result"], search_id,
                cached=audit["cached"], network_attempted=not audit["cached"], fetched_epoch=audit.get("fetched_epoch"))
            if registration != audit.get("finite_registration"):
                raise ValueError("Replayed bibliography finite registration changed")
            self._verify_metadata_records(result, item["result"], registration["allowed_indices"])
            return registration
        elif name == "bibliography_read" and not result.get("error"):
            search_id = arguments["search_id"]
            item = self._immutable_metadata("search_pages", search_id)
            if search_id not in self._search_pages:
                raise ValueError("Replayed local page has no current-stage search grant")
            self._verify_metadata_records(result, item["result"], self._search_pages[search_id]["allowed_indices"])
        elif name == "bibliography_lookup" and result.get("error"):
            attempt = result.get("audit", {}).get("finite_lookup_attempt")
            self._lookup_log.append(copy.deepcopy(result["audit"]))
            if attempt is not None:
                ticket = self._finite_scope.before_lookup(arguments["kind"], canonical_identifier(**arguments),
                    network_attempted=attempt["network_attempted"])
                if ticket != attempt["ticket"]:
                    raise ValueError("Replayed failed exact lookup ticket changed")
                self._finite_scope.record_lookup_failure(ticket, result["error"])
        elif name == "bibliography_lookup" and not result.get("error"):
            lookup_id = result["lookup_id"]
            item = self._immutable_metadata("lookup_pages", lookup_id)
            if item["query"] != self._lookup_key(**arguments):
                raise ValueError("Replayed exact lookup belongs to another identity/window")
            expected_record = self._metadata_record(item["result"]["record"])
            expected_record["record_id"] = record_id(item["result"]["record"])
            if result.get("record") != expected_record or any(result.get(k) != v for k, v in item["result"].items() if k != "record"):
                raise ValueError("Replayed lookup metadata or identity differs from its archive")
            cached = result["audit"]["cached"]
            ticket = self._finite_scope.before_lookup(arguments["kind"], item["query"]["identifier"], network_attempted=not cached)
            self._finite_scope.record_lookup(ticket, item["result"], lookup_id, cached=cached, network_attempted=not cached)
            self._lookup_log.append(copy.deepcopy(result["audit"]))
            self._lookup_records[lookup_id] = {"key": item["query"], "result_sha256": item["sha256"], "record_id": expected_record["record_id"]}
        elif name == "source_fetch" and {"url", "purpose", "obligation_id"}.issubset(arguments):
            if not result.get("error"):
                self._declare_source(**arguments)
                source_hash = result["source_hash"]
                if not re.fullmatch(r"[0-9a-f]{64}", str(source_hash)):
                    raise ValueError("Replayed source archive has an invalid content identity")
                metadata = _strict_json((self.cache_dir / "sources/metadata" / (source_hash + ".json")).read_text("utf-8"))
                raw = (self.cache_dir / "sources/text" / (source_hash + ".txt")).read_bytes()
                if hashlib.sha256(raw).hexdigest() != metadata.get("text_sha256") or result.get("audit", {}).get("text_sha256") != metadata.get("text_sha256"):
                    raise ValueError("Replayed fetched source failed its immutable text binding")
        elif name == "source_read" and not result.get("error"):
            text, metadata = self._source_text(arguments["source_hash"])
            offset = arguments["offset"]
            expected = text[offset:offset + min(arguments["limit"], self._limit("max_tool_chars", 10000))]
            if result.get("text") != expected or result.get("audit", {}).get("text_sha256") != metadata["text_sha256"]:
                raise ValueError("Replayed source read differs from its granted immutable slice")
        return None

    def _immutable_metadata(self, directory, identity):
        if not re.fullmatch(r"[0-9a-f]{64}", str(identity)):
            raise ValueError("Invalid immutable metadata archive identity")
        path = self.cache_dir / directory / (identity + ".json")
        if any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError("Metadata replay must not follow symbolic links")
        item = _strict_json(path.read_text("utf-8"))
        key = "page_sha256" if directory == "search_pages" else "result_sha256"
        if item.get("sha256") != _sha(item["result"]) or _sha({"query": item["query"], key: item["sha256"]}) != identity:
            raise ValueError("Immutable metadata archive failed its content/query identity")
        return item

    def _verify_metadata_records(self, result, provider_result, allowed):
        indices = result.get("record_indices", [])
        if len(indices) != len(set(indices)) or not set(indices).issubset(allowed):
            raise ValueError("Metadata exposure exceeds its declared finite prefix")
        expected = []
        for index in indices:
            value = self._metadata_record(provider_result["records"][index])
            value["record_id"] = record_id(provider_result["records"][index])
            expected.append(value)
        if result.get("records") != expected:
            raise ValueError("Exposed metadata/record identities differ from their immutable page")

    def state(self) -> dict:
        result = {"events": self.events, "search_log": self.search_log, "source_log": self.source_log,
                "budget_exhausted": self.budget_exhausted, "failed": self.failed,
                "unresolved_failure_ids": sorted(set(self._failures) | self._orphan_failure_ids),
                "persistent_failed": self._persistent_failed, "budget_remaining": self.budget_remaining()}
        if self._finite_scope is not None:
            result.update(finite_scope=self._finite_scope.state(), lookup_log=self._lookup_log,
                          discovery_cache_dir=str(self.cache_dir), discovery_context_sha256=self._discovery_context_sha256())
        return result

    def _discovery_context_sha256(self):
        return _sha({k: self.context.get(k) for k in ("setting_id", "base_version", "cutoff", "window_start", "policy",
            "semantics", "contract_hash", "maintenance_role", "finite_verification_plan", "allowed_source_hashes")})

    def import_state(self, state: dict) -> None:
        journal_keys = {"events", "budget_exhausted", "failed", "unresolved_failure_ids", "persistent_failed"}
        # The native journal stores actual events plus only these four flags;
        # runtime and _native_stage bind every reconstructed state to its exact
        # recorded state_sha256. A full snapshot never receives this exemption.
        journal_envelope = set(state) == journal_keys or state == {"events": []}
        self.events, self.search_log, self.source_log = [], [], []
        self.budget_exhausted = self.failed = False
        self._persistent_failed, self._orphan_failure_ids = False, set()
        self._failures, self._search_pages = {}, {}
        self._searches = self._sources = self._reads = self._finds = 0
        self._fetch_attempts = 0
        self._lookup_log, self._lookup_records, self._source_declarations = [], {}, []
        if self._finite_scope is not None:
            from .finite_scope import FiniteScope
            self.grants = set(self.context.get("allowed_source_hashes", []))
            self._finite_scope = FiniteScope(self.context, self.config)
            if self.context.get("maintenance_role") == "reviewer" and self.context.get("finite_verification_plan") is not None:
                self._finite_scope.freeze(copy.deepcopy(self.context["finite_verification_plan"]))
            if not journal_envelope and state.get("discovery_context_sha256") != self._discovery_context_sha256():
                raise ValueError("Finite research replay belongs to another setting/base/policy/window/role")
        for event in state.get("events", []):
            self.restore(event["tool"], event["arguments"], event["result"])
        self.budget_exhausted = self.budget_exhausted or bool(state.get("budget_exhausted"))
        self._orphan_failure_ids = set(state.get("unresolved_failure_ids", [])) - set(self._failures)
        self._persistent_failed = bool(state.get("persistent_failed")) or (bool(state.get("failed")) and not self._failures)
        self.failed = bool(self._failures or self._orphan_failure_ids or self._persistent_failed)
        if self._finite_scope is not None and not journal_envelope and state.get("finite_scope") != self._finite_scope.state():
            raise ValueError("Claimed finite research state differs from its actual journal replay")
        if self._finite_scope is not None and not journal_envelope and any(state.get(key) != value for key, value in (
                ("lookup_log", self._lookup_log), ("search_log", self.search_log), ("source_log", self.source_log))):
            raise ValueError("Claimed literature audit logs differ from their actual event replay")

    def _search(self, provider: str, query: str, year: int | None, cursor: str | None, limit: int) -> dict:
        if self._finite_scope is None and self._searches >= self._limit("max_searches_per_setting", 3):
            self.budget_exhausted = True
            raise RuntimeError("Search budget exhausted; preserve incomplete scope and do not advance the successful watermark.")
        self._searches += 1
        key_data = {"provider": provider, "query": query.strip(), "year": year, "cursor": cursor, "limit": limit,
                    "window_start": self.context.get("window_start"), "cutoff": self.context.get("cutoff"), "version": 1}
        cache = self.cache_dir / "search" / (_sha(key_data) + ".json")
        admission = getattr(self, "_cache_admission_epoch", None)
        now, cached, result, fetched = time.time() if admission is None else admission, False, None, None
        ttl = max(0, float(self.config.get("cache", {}).get("search_ttl_seconds", 21600)))
        if cache.is_file():
            item = json.loads(cache.read_text("utf-8"))
            if 0 <= now - item["saved_epoch"] <= ttl and item.get("sha256") == _sha(item["result"]):
                cached, result, fetched = True, item["result"], item["saved_epoch"]
        ticket = None
        if self._finite_scope is not None:
            ticket = self._finite_scope.before_search(provider, query, year, cursor, limit, network_attempted=not cached)
            self._finite_provider_attempt = {"ticket": ticket, "network_attempted": not cached}
        if result is None:
            if self._bibliography is None:
                options = self.config.get("literature", {})
                client = HTTPClient(timeout=float(options.get("timeout", 30)), max_bytes=int(options.get("max_bytes", 20000000)), cache_ttl=0)
                self._bibliography = Bibliography(client=client, contact=options.get("contact"), arxiv_interval=float(options.get("arxiv_interval", 3)))
            try:
                result = self._bibliography.search(provider, query, year=year, limit=limit, cursor=cursor)
            except Exception as exc:
                if self._finite_scope is not None:
                    self._finite_scope.record_search_failure(ticket, str(exc)[:1200])
                raise
            fetched = time.time()
            atomic_write(cache, _json({"saved_epoch": fetched, "sha256": _sha(result), "result": result}).encode())
        audit = {**key_data, "success": True, "cached": cached, "fresh": True, "fetched_epoch": fetched,
                 "next_cursor": result.get("next_cursor"), "total": result.get("total"),
                 "records_returned": len(result.get("records", [])), "exhaustive": False}
        self.search_log.append(audit)
        page_hash = _sha(result)
        search_id = _sha({"query": key_data, "page_sha256": page_hash})
        page_path = self.cache_dir / "search_pages" / (search_id + ".json")
        if not page_path.is_file():
            atomic_write(page_path, _json({"query": key_data, "sha256": page_hash, "result": result}).encode())
        audit["search_id"] = search_id
        page = self._search_pages.setdefault(search_id, {"audit": audit, "audits": [], "seen": set(), "count": len(result.get("records", []))})
        prior = page["audit"]
        if prior.get("retired"):
            audit.update({k: prior[k] for k in ("retired", "replacement_search_id", "retirement_reason")})
        page["audit"] = audit
        page["audits"].append(audit)
        if self._finite_scope is not None:
            registration = self._finite_scope.record_search(ticket, result, search_id, cached=cached,
                network_attempted=not cached, fetched_epoch=fetched)
            page["finite_registration"] = registration
            page["allowed_indices"] = registration["allowed_indices"]
            page["count"] = len(registration["allowed_indices"])
            audit["finite_registration"] = registration
            audit["provider_page_records_total"] = len(result.get("records", []))
            audit["provider_date_semantics"] = {"literal_query": query,
                "year_filter": "submission" if provider == "arxiv" and year else "publication" if year else None,
                "server_window_filter_claimed": False,
                "note": "Scope is the declared finite returned prefix. Metadata dates require inspection; no global revision coverage is claimed."}
        response = self._metadata_page(search_id, result, 0, limit)
        response["audit"] = audit
        self._cover_search(search_id, response["record_indices"])
        response["scope_note"] = "One query page; dates are metadata. No mathematical applicability has been certified."
        if audit["output_truncated"]:
            response["scope_note"] += " Read omitted cached records with bibliography_read(search_id,next_record_offset,limit); no HTTP is needed."
        return response

    @staticmethod
    def _metadata_record(record):
        value = {k: copy.deepcopy(record[k]) for k in ("paper_id", "title", "identifiers", "urls", "publication_events", "versions", "work_type") if k in record}
        value["abstract"] = record.get("abstract", "")[:1500]
        return value

    def _metadata_page(self, search_id, result, offset, limit):
        records = result.get("records", [])
        allowed = self._search_pages.get(search_id, {}).get("allowed_indices", list(range(len(records))))
        if offset > len(allowed):
            raise ValueError("Record offset exceeds the saved bibliography page")
        response = {"search_id": search_id, "offset": offset, "records": [], "record_indices": [],
                    "page_records_total": len(allowed), "next_record_offset": None,
                    "next_cursor": result.get("next_cursor"), "total": result.get("total"),
                    "untrusted_reference_data": True}
        cap = self._limit("max_tool_chars", 10000)
        for index in allowed[offset:offset + limit]:
            value = self._metadata_record(records[index])
            if self._finite_scope is not None:
                value["record_id"] = record_id(records[index])
            response["records"].append(value)
            response["record_indices"].append(index)
            if len(_json(response)) > cap:
                response["records"].pop()
                response["record_indices"].pop()
                break
        next_offset = offset + len(response["records"])
        response["next_record_offset"] = next_offset if next_offset < len(allowed) else None
        response["output_truncated"] = response["next_record_offset"] is not None
        return response

    def _cover_search(self, search_id, indices):
        if search_id not in self._search_pages:
            raise ValueError("Bibliography page has not been granted to this stage")
        page = self._search_pages[search_id]
        page["seen"].update(indices)
        if self._finite_scope is not None:
            self._finite_scope.record_exposure(search_id, indices)
        for audit in page["audits"]:
            audit["output_truncated"] = page["seen"] != set(range(page["count"]))
            audit["records_exposed"] = len(page["seen"])

    def _bibliography_read(self, search_id, offset, limit):
        if search_id not in self._search_pages:
            raise ValueError("Bibliography page has not been granted to this stage")
        cache = self.cache_dir / "search_pages" / (search_id + ".json")
        item = json.loads(cache.read_text("utf-8"))
        if item.get("sha256") != _sha(item["result"]) or _sha({"query": item["query"], "page_sha256": item["sha256"]}) != search_id:
            raise ValueError("Saved bibliography page failed its immutable hash check")
        response = self._metadata_page(search_id, item["result"], offset, limit)
        self._cover_search(search_id, response["record_indices"])
        response["cached_page_complete"] = not self._search_pages[search_id]["audit"]["output_truncated"]
        return response

    def _search_replace(self, search_id, replacement_search_id, reason):
        if not reason.strip() or search_id == replacement_search_id:
            raise ValueError("Scope refinement needs a distinct replacement and nonempty reason")
        if search_id not in self._search_pages or replacement_search_id not in self._search_pages:
            raise ValueError("Both queries must have successful observed pages in this stage")
        old, replacement = self._search_pages[search_id]["audit"], self._search_pages[replacement_search_id]["audit"]
        if old.get("retired") or old.get("output_truncated"):
            raise ValueError("Original query is already retired or still has unexposed metadata")
        if not replacement.get("success") or replacement.get("retired") or replacement.get("output_truncated") or replacement.get("next_cursor"):
            raise ValueError("Replacement must be successful, fully exposed, terminal, and not retired")
        for audit in self._search_pages[search_id]["audits"]:
            audit.update(retired=True, replacement_search_id=replacement_search_id, retirement_reason=reason.strip())
        return {"retired": True, "search_id": search_id, "replacement_search_id": replacement_search_id,
                "reason": reason.strip(), "note": "The old fuzzy corpus remains unexhausted and archived; the recorded research scope has been refined."}

    def _fetch(self, url: str) -> dict:
        if self._sources >= self._limit("max_sources_per_setting", 3):
            self.budget_exhausted = True
            raise RuntimeError("Source budget exhausted; leave unresolved leads pending.")
        if self._fetch_attempts >= self._limit("max_source_attempts_per_setting", 2 * self._limit("max_sources_per_setting", 3)):
            self.budget_exhausted = True
            raise RuntimeError("Source request-attempt budget exhausted; preserve the failed requests")
        self._fetch_attempts += 1
        url_key = hashlib.sha256(url.encode()).hexdigest()
        index = self.cache_dir / "source_urls" / (url_key + ".json")
        ttl = max(0, float(self.config.get("cache", {}).get("source_ttl_seconds", 21600)))
        saved, cached = None, False
        admission = getattr(self, "_cache_admission_epoch", None)
        now = time.time() if admission is None else admission
        if index.is_file():
            item = json.loads(index.read_text("utf-8"))
            if 0 <= now - item["saved_epoch"] <= ttl:
                meta = self.cache_dir / "sources" / "metadata" / (item["source_hash"] + ".json")
                text_path = self.cache_dir / "sources" / "text" / (item["source_hash"] + ".txt")
                if meta.is_file() and text_path.is_file():
                    metadata = json.loads(meta.read_text("utf-8"))
                    if hashlib.sha256(text_path.read_bytes()).hexdigest() == metadata.get("text_sha256"):
                        saved = {"content_hash": item["source_hash"], "metadata": metadata, "url": url}
                        cached = True
        recovery = None
        if self.config.get("budgets", {}).get("source_recovery") is True:
            from .source_recovery import SourceRecovery
            from .cache_control import _arxiv_operation, _interval, _lock_path, _wait_provider
            obligation = getattr(self, "_source_obligation", None) or {}
            kind, identifier = obligation.get("kind"), obligation.get("identifier")
            expected = ({kind: identifier} if kind in {"doi", "arxiv"} else
                        {"content_hash": identifier} if kind == "source_hash" else None)

            def remaining():
                execution = self._execution_status()
                if execution.get("close_requested"):
                    return 0
                return execution.get("research_seconds_remaining", execution.get("remaining_seconds", 1800))

            def before_attempt(target, attempt_index):
                if attempt_index == 0 or not _arxiv_operation("source_fetch", {"url": target}):
                    return
                if not _arxiv_operation("source_fetch", {"url": url}):
                    raise ValueError("Cross-provider arXiv recovery needs a separate admitted source request")
                timestamp = _lock_path(self.cache_dir.resolve(), "arxiv-start.json")
                _wait_provider(timestamp, _interval(self.config), getattr(self, "run_control_path", None))
                atomic_write(timestamp, (_json({"last_start_monotonic_ns": time.monotonic_ns()}) + "\n").encode())

            downloader = SourceRecovery(self.atlas_root, self.cache_dir, self.context, self.config,
                fetch_source=fetch_source, remaining_seconds=remaining, before_attempt=before_attempt)
            if saved is not None:
                originals = list((self.cache_dir / "sources/originals").glob(saved["content_hash"] + ".*"))
                if len(originals) != 1 or originals[0].is_symlink():
                    raise ValueError("Cached source requires its exact single archived original")
                saved["path"] = str(originals[0])
                recovery = downloader.verify_cached(saved, url, expected_identity=expected)
            else:
                alternatives = [candidate for candidate in self.known_primary_locations(obligation) if candidate != url] if obligation and expected else []
                saved = downloader.fetch(url, expected_identity=expected, official_urls=alternatives,
                                         obligation_id=obligation.get("obligation_id"))
                recovery = saved.pop("_recovery")
                atomic_write(index, _json({"saved_epoch": time.time(), "source_hash": saved["content_hash"]}).encode())
        if saved is None:
            options = self.config.get("literature", {})
            saved = fetch_source(url, self.cache_dir / "sources", timeout=float(options.get("timeout", 30)),
                                 max_bytes=int(options.get("max_bytes", 20000000)), refresh=True)
            atomic_write(index, _json({"saved_epoch": time.time(), "source_hash": saved["content_hash"]}).encode())
        sha = saved["content_hash"]
        self._sources += 1
        self.grants.add(sha)
        audit = {"tool": "source_fetch", "source_hash": sha, "url": saved["url"], "success": True,
                 "cached": cached, "fetched_at": saved["metadata"].get("fetched_at"),
                 "text_sha256": saved["metadata"].get("text_sha256"), "characters_read": 0}
        if recovery is not None:
            from oracle_atlas.discovery.http import display_url
            audit["requested_url"] = display_url(url)
            audit["requested_url_sha256"] = hashlib.sha256(url.encode()).hexdigest()
        self.source_log.append(audit)
        metadata_preview = {k: copy.deepcopy(v) for k, v in saved["metadata"].items() if k not in {"locators", "text_path"}}
        metadata_preview["locator_count"] = len(saved["metadata"].get("locators", []))
        return {"source_hash": sha, "url": saved["url"], "metadata": metadata_preview, "audit": audit,
                **({"recovery": recovery} if recovery is not None else {}),
                "note": "Archived, not yet read. Fetch is not evidence that this page is a primary theorem source. Read returns overlapping page locators."}

    def _read(self, source_hash: str, offset: int, limit: int) -> dict:
        if self._reads >= self._limit("max_source_reads_per_setting", 12):
            self.budget_exhausted = True
            raise RuntimeError("Source reading budget exhausted; preserve precise unread obligations.")
        self._reads += 1
        text, metadata = self._source_text(source_hash)
        if offset > len(text):
            raise ValueError("Source offset exceeds text length.")
        count = min(limit, self._limit("max_tool_chars", 10000))
        excerpt = text[offset:offset + count]
        audit = {"tool": "source_read", "source_hash": source_hash, "success": True, "offset": offset,
                 "end": offset + len(excerpt), "characters_read": len(excerpt), "text_sha256": metadata["text_sha256"]}
        self.source_log.append(audit)
        return {"source_hash": source_hash, "text": excerpt, "offset": offset, "total_characters": len(text),
                "next_offset": offset + count if offset + count < len(text) else None, "audit": audit,
                "locators": [loc for loc in metadata.get("locators", [])
                             if loc.get("start", 0) < offset + len(excerpt) and loc.get("end", 0) > offset][:100],
                "limitations": metadata.get("limitations", []), "untrusted_reference_data": True}

    def _source_text(self, source_hash):
        if source_hash not in self.grants:
            raise ValueError("Source hash has not been granted to this stage; fetch its URL or use controller-pinned reviewed sources.")
        path = self.cache_dir / "sources" / "text" / (source_hash + ".txt")
        metadata = json.loads((self.cache_dir / "sources" / "metadata" / (source_hash + ".json")).read_text("utf-8"))
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != metadata.get("text_sha256"):
            raise ValueError("Archived source text failed its content hash check.")
        return raw.decode("utf-8"), metadata

    def _find(self, source_hash, literal, limit):
        if self._finds >= self._limit("max_source_finds_per_setting", 12):
            self.budget_exhausted = True
            raise RuntimeError("Source locating budget exhausted; preserve unread theorem obligations")
        self._finds += 1
        text, metadata = self._source_text(source_hash)
        matches, start = [], 0
        while len(matches) < limit:
            found = text.find(literal, start)
            if found < 0:
                break
            matches.append({"offset": found, "end": found + len(literal),
                            "snippet": text[max(0, found - 64):min(len(text), found + min(len(literal), 120) + 64)],
                            "snippet_truncated": len(literal) > 120})
            start = found + max(1, len(literal))
        match_mode = "literal"
        if not matches:
            for compact, mode in ((False, "unicode_nfkc_whitespace"), (True, "unicode_nfkc_compact_whitespace")):
                normalized, starts, ends = self._locator_text(text, compact)
                needle = self._locator_text(literal, compact)[0]
                if not needle:
                    break
                cursor = 0
                while len(matches) < limit:
                    position = normalized.find(needle, cursor)
                    if position < 0:
                        break
                    raw_start, raw_end = starts[position], ends[position + len(needle) - 1]
                    matches.append({"offset": raw_start, "end": raw_end,
                                    "snippet": text[max(0, raw_start - 64):min(len(text), raw_start + 184)],
                                    "snippet_truncated": raw_end - raw_start > 120})
                    cursor = position + max(1, len(needle))
                match_mode = mode
                if matches:
                    break
        audit = {"tool": "source_find", "source_hash": source_hash, "success": True,
                 "characters_read": 0, "matches_returned": len(matches), "text_sha256": metadata["text_sha256"]}
        self.source_log.append(audit)
        return {"source_hash": source_hash, "literal": literal, "matches": matches, "match_mode": match_mode, "audit": audit,
                "note": "Literal matches locate candidate text only. Read the decisive range with source_read; no theorem evidence has been marked read."}

    @staticmethod
    def _locator_text(text, compact=False):
        chars, starts, ends = [], [], []
        for offset, raw in enumerate(text):
            for char in unicodedata.normalize("NFKC", raw):
                if char.isspace():
                    if compact:
                        continue
                    if chars and chars[-1] == " ":
                        ends[-1] = offset + 1
                        continue
                    char = " "
                chars.append(char)
                starts.append(offset)
                ends.append(offset + 1)
        return "".join(chars), starts, ends


def validate_finite_scope_state(snapshot, context, config, report=None):
    """Rebuild finite coverage from actual tool events, never a claimed complete flag.

    The engine supplies its frozen current context/config. Immutable metadata and
    source archives are read locally; this function cannot perform network I/O.
    """
    if config.get("budgets", {}).get("finite_research_scope") is not True:
        return {"enabled": False, "complete": False, "blocking": ["Finite research scope is disabled"],
                "optional_unused_failure_ids": []}
    if isinstance(snapshot, MaintenanceTools):
        snapshot = snapshot.state()
    elif not isinstance(snapshot, dict):
        snapshot = vars(snapshot)
    cache = Path(snapshot.get("discovery_cache_dir", ""))
    if not cache.is_absolute() or any(p.is_symlink() for p in (cache, *cache.parents)):
        raise ValueError("Finite research replay requires its exact regular local cache root")
    host = MaintenanceTools(Path("."), cache, context, config)
    host.import_state(snapshot)
    completion = host._finite_scope.completion(no_change=bool(report and report.get("outcome") == "no_change"),
        own_source_reads=host._own_source_reads(), source_bindings=host._candidate_source_bindings(), report=report)
    audit = {**host._finite_scope.public_audit(), **copy.deepcopy(completion)}
    audit["enabled"] = True
    audit["replayed_state_sha256"] = _sha(host._finite_scope.state())
    optional = set(host._optional_unused_source_failures(report))
    audit["optional_unused_failure_ids"] = sorted(optional)
    blocking = (set(host._failures) | host._orphan_failure_ids) - optional
    reasons = set(audit.get("reasons", []))
    if blocking:
        reasons.add("tool_failure_unresolved")
    if host._persistent_failed:
        reasons.add("persistent_tool_failure")
    if host.budget_exhausted:
        reasons.add("stage_budget_exhausted")
    audit["blocking_failure_ids"] = sorted(blocking)
    audit["failure_scope_clean"] = not (blocking or host._persistent_failed or host.budget_exhausted)
    audit["reasons"] = sorted(reasons)
    if reasons:
        audit["finite_scope_complete"] = False
        audit["no_change_eligible"] = False
    audit["completion"] = {key: copy.deepcopy(audit[key]) for key in (*completion.keys(),
        "optional_unused_failure_ids", "blocking_failure_ids", "failure_scope_clean")}
    return audit
