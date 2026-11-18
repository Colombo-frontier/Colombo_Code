"""Project the same scoped facts into human navigation and machine-screening tags.

Normalize only explicit structural fields; do not prove equivalence from natural language or treat absent tags as negation.
All interface screening uses ``effective_native_operations`` to prevent divergence between human and machine representations.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import re
from typing import Any

AXES = ("TASK", "MODEL", "ORACLE", "ALGORITHMS", "OUTPUT", "METRIC", "GUARANTEE", "RESOURCE")
TAG_PATTERN = re.compile(r"^(TASK|MODEL|ORACLE|ALGORITHMS|OUTPUT|METRIC|GUARANTEE|RESOURCE):[a-z_]+:[a-z0-9_]+$")
UNKNOWN = {"unknown", "unspecified", "unresolved", "not_reported"}
EXACT_CONCEPTS = {"ORACLE:feedback_quality:exact", "ORACLE:quality:exact"}
PUBLIC_ROLES = {"public_auxiliary", "public", "auxiliary"}
PRIMITIVE_ROLES = {"primitive", "unknown_object_primitive", "native"}

# Compatibility names for display groups. A controlled navigation mapping exists only when the complete target concept is actually registered.
HUMAN_GROUP_ALIASES = {
    "TASK:task_family": "TASK:family",
    "ORACLE:feedback_quality": "ORACLE:quality",
    "ORACLE:access_order": "ORACLE:access",
}
# Explicit display mappings for complete concepts; they do not alter source facts or add permissions to native interfaces.
# exact_feedback may itself describe a stochastic reward; the complete native Exact check below is still required.
HUMAN_CONCEPT_ALIASES = {
    "ORACLE:feedback_quality:exact_feedback": "ORACLE:quality:exact",
}
LABELS = {
    "matrix_computation": "Matrix computation", "single_objective": "Single objective",
    "bilevel": "Bilevel optimization", "variational_inequality": "Variational inequality",
    "exact": "Exact", "zero": "Zeroth-order interface", "first": "First-order interface",
    "gradient_only": "Gradient only", "value_gradient": "Value and gradient",
    "exact_value": "Exact function value", "stochastic": "Stochastic feedback",
    "deterministic": "Deterministic algorithms",
    "private_randomness_allowed": "Randomization allowed",
}


class TagError(ValueError):
    """A repairable structural error; it is not a mathematical negation."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def at(value: Any, pointer: str) -> Any:
    """Strict RFC 6901 resolution; reject invalid escapes and Python negative indices."""
    if pointer == "":
        return value
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise TagError(f"JSON Pointer must start with /: {pointer!r}")
    try:
        for token in pointer[1:].split("/"):
            if re.search(r"~(?![01])", token):
                raise ValueError("invalid escape")
            token = token.replace("~1", "/").replace("~0", "~")
            if isinstance(value, list):
                if not re.fullmatch(r"0|[1-9][0-9]*", token):
                    raise ValueError("invalid array index")
                value = value[int(token)]
            else:
                value = value[token]
        return value
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise TagError(f"Unresolved JSON Pointer: {pointer}") from exc


def _escape(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def effective_specification(profile: dict, view: str | dict | None = None) -> tuple[dict, dict]:
    """Override objects recursively and replace lists in full; preserve explicit null values and record the actual source of each leaf."""
    origins: dict[str, str] = {}

    def record(value: Any, logical: str, source: str) -> None:
        origins[logical] = source
        if isinstance(value, dict):
            for key, child in value.items():
                record(child, logical + "/" + _escape(key), source + "/" + _escape(key))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                record(child, logical + f"/{index}", source + f"/{index}")

    def merge(base: Any, override: Any, logical: str, source: str) -> Any:
        if isinstance(base, dict) and isinstance(override, dict):
            for key, val in override.items():
                child = logical + "/" + _escape(key)
                base[key] = merge(base.get(key), val, child, source + "/" + _escape(key))
            return base
        for old in list(origins):
            if old == logical or old.startswith(logical + "/"):
                del origins[old]
        record(override, logical, source)
        return deepcopy(override)

    common = deepcopy(profile.get("common_specification", {}))
    if not isinstance(common, dict):
        raise TagError("common_specification must be an object")
    record(common, "", "/common_specification")
    if view is None:
        return common, origins
    selected = None
    for index, item in enumerate(profile.get("views", [])):
        if item is view or (isinstance(view, str) and item.get("view_id") == view) or (isinstance(view, dict) and item.get("view_id") == view.get("view_id")):
            selected = (index, item)
            break
    if selected is None:
        raise TagError(f"Unknown view: {view!r}")
    index, item = selected
    overrides = item.get("specification_overrides", {})
    if not isinstance(overrides, dict):
        raise TagError("specification_overrides must be an object; null cannot represent the entire override object")
    result = merge(common, overrides, "", f"/views/{index}/specification_overrides")
    # algorithms / guarantees are declared natively on the view and share the scope of the common specification.
    for key in ("algorithms", "guarantees"):
        if key in item:
            result[key] = merge(result.get(key), item[key], "/" + key, f"/views/{index}/{key}")
    return result, origins


def _alias(obj: dict, names: tuple[str, ...], diagnostics: list[str], label: str) -> Any:
    values = [obj[name] for name in names if name in obj]
    if not values:
        return None
    if any(value != values[0] for value in values[1:]):
        diagnostics.append(f"Conflicting aliases for {label}: {','.join(name for name in names if name in obj)}")
        return None
    value = values[0]
    if value is not None and not isinstance(value, str):
        diagnostics.append(f"{label} must be a string or null")
        return None
    return value


def _quality(value: Any, *, allow_legacy_descriptor: bool = False) -> str | None:
    """Structural aliases for explicit precision codes; do not infer scientific permissions from text/description."""
    if isinstance(value, dict):
        aliases = [name for name in ("code", "kind", "model") if name in value]
        decoded = [_quality(value[name]) if not isinstance(value[name], dict) else _unsupported_quality_alias(name)
                   for name in aliases]
        if decoded and any(item != decoded[0] for item in decoded[1:]):
            raise TagError("Conflicting code/kind/model declarations in the precision object")
        status = value.get("status", "known")
        if status is None or (isinstance(status, str) and status in UNKNOWN | {"not_applicable"}):
            return None
        if status != "known":
            raise TagError("precision.status must be known, unknown/not_applicable, or null")
        if not aliases:
            if allow_legacy_descriptor and "status" not in value and "feedback" in value:
                # The native legacy catalog stores the full response description in feedback_quality.feedback;
                # retain only unknown status; never infer precision from that description.
                return None
            raise TagError("The precision object must explicitly declare code/kind/model; text/description cannot replace a code")
        return decoded[0]
    if value is None or (isinstance(value, str) and value in UNKNOWN):
        return None
    if not isinstance(value, str) or not value.strip():
        raise TagError("precision must be a nonempty code string, null, or an object containing code/kind/model")
    return {"noiseless": "exact", "noisy": "stochastic", "approximate": "inexact"}.get(value, value)


def _unsupported_quality_alias(name: str):
    raise TagError(f"precision.{name} must be a code string or null; it cannot contain an undeclared object structure")


def _noise(value: Any) -> str | None:
    """Normalize only explicit noise enumerations; a declaration of no noise does not by itself imply exact precision."""
    if isinstance(value, dict):
        value = value.get("code", value.get("kind"))
    if isinstance(value, bool):
        return "present" if value else "none"
    if not isinstance(value, str) or value in UNKNOWN:
        return None
    return {"no_noise": "none", "noiseless": "none", "zero": "none", "noisy": "present"}.get(value, value)


def _operation_feedback(raw: dict, operation_code: str | None) -> tuple[dict, list[str]]:
    """Read explicitly declared feedback attributes under operation and response; do not read natural-language text."""
    containers = [("", raw)]
    if isinstance(raw.get("response"), dict):
        containers.append(("/response", raw["response"]))
    quality_fields, noise_fields, scope_kinds = [], [], set()
    errors, declaration_diagnostics = [], []

    def declaration_error(code, path, message):
        errors.append(message)
        declaration_diagnostics.append({"code": code, "path": path, "message": message})
    sampled_names = {"sample", "sampled_function", "sampled_realization", "sample_value"}
    fixed_names = {"fixed", "fixed_object", "target_object", "full_object"}
    for prefix, obj in containers:
        for name in ("feedback_quality", "precision", "quality"):
            if name in obj:
                path = prefix + "/" + name
                try:
                    quality = _quality(obj[name], allow_legacy_descriptor=name == "feedback_quality")
                except TagError as exc:
                    quality = None
                    declaration_error("invalid_precision", path, str(exc))
                quality_fields.append((path, quality))
        if "noise" in obj:
            noise_fields.append((prefix + "/noise", _noise(obj["noise"])))
        for name in ("precision_scope", "target_scope", "response_target"):
            value = obj.get(name)
            if isinstance(value, dict):
                value = value.get("code", value.get("kind"))
            if isinstance(value, str):
                if value in sampled_names:
                    scope_kinds.add("sampled")
                elif value in fixed_names:
                    scope_kinds.add("fixed")
        if isinstance(obj.get("sampled_object"), bool):
            scope_kinds.add("sampled" if obj["sampled_object"] else "fixed")
    if operation_code in {"sample_value", "exact_sample_value", "sample_function_value"}:
        scope_kinds.add("sampled")
    precision = quality_fields[0][1] if quality_fields else None
    noise = noise_fields[0][1] if noise_fields else None
    if any(value != precision for _, value in quality_fields[1:]):
        declaration_error("conflicting_precision", quality_fields[0][0], "Conflicting feedback_quality / precision / quality declarations in operation / response")
        precision = None
    if any(value != noise for _, value in noise_fields[1:]):
        declaration_error("conflicting_noise", noise_fields[0][0], "Conflicting noise declarations in operation / response")
        noise = None
    if len(scope_kinds) > 1:
        declaration_error("conflicting_feedback_scope", "", "Conflicting fixed / sampled feedback scopes in operation / response")
    sampled = "sampled" in scope_kinds
    if precision == "exact" and noise not in {None, "none"} and not sampled:
        declaration_error("conflicting_feedback", quality_fields[0][0] if quality_fields else "", "Exact precision for a fixed object conflicts with an explicit nonzero-noise declaration")
        precision = None
    return {"precision": precision, "precision_path": quality_fields[0][0] if quality_fields else None,
            "noise": noise, "noise_path": noise_fields[0][0] if noise_fields else None,
            "sampled": sampled, "declaration_diagnostics": declaration_diagnostics}, errors


def effective_native_operations(profile: dict, view: str | dict | None = None) -> dict:
    """The complete native operation inventory, including operations not yet covered by the vocabulary and operations with unknown precision.

    The legacy exact_value structural code is the sole narrow compatibility entry point; the program never infers permissions from text.
    When complete=False is returned, legacy tags alone must not make an unqualified interface assertion matched.
    """
    diagnostics: list[str] = []
    try:
        spec, origins = effective_specification(profile, view)
    except TagError as exc:
        return {"operations": [], "diagnostics": [str(exc)], "complete": False}
    oracle = spec.get("oracle")
    if not isinstance(oracle, dict):
        return {"operations": [], "diagnostics": ["oracle is not explicitly declared as an object"], "complete": False}
    rows = oracle.get("operations")
    legacy = False
    if rows is None and "operations" not in oracle and oracle.get("code") == "exact_value":
        rows = [{"id": "legacy_exact_value", "operation_code": "function_value", "feedback_quality": {"code": "exact"}, "returns": ["value"], "role": "unknown_object_primitive"}]
        legacy = True
    if not isinstance(rows, list):
        return {"operations": [], "diagnostics": ["oracle.operations is not fully declared as a list"], "complete": False}
    operations, ids = [], set()
    for index, raw in enumerate(rows):
        own: list[str] = []
        native_diagnostics, noted_messages = [], set()
        pointer = origins.get(f"/oracle/operations/{index}", origins.get("/oracle", "/common_specification/oracle"))
        if legacy:
            pointer = origins.get("/oracle/code", "/common_specification/oracle/code")
        if not isinstance(raw, dict):
            diagnostics.append(f"operation[{index}] is not an object")
            operations.append({"operation_ref": None, "operation_code": None, "object_ref": None, "role": "unknown", "precision": None, "returns": None, "sampled": False, "source_pointer": pointer, "valid": False})
            continue

        def native_error(code: str, relative: str, message: str) -> None:
            source = origins.get(f"/oracle/operations/{index}" + relative, pointer + relative)
            text = f"{source}: {message}"
            own.append(text)
            noted_messages.add(text)
            native_diagnostics.append({"code": code, "path": source, "message": message})
        op_id = _alias(raw, ("id", "operation_id", "operation_ref"), own, "operation id")
        op_code = _alias(raw, ("operation_code", "code"), own, "operation code")
        object_ref = _alias(raw, ("object_ref", "object_id", "target_object"), own, "object")
        if not op_id or op_id in ids:
            own.append("operation id is missing or duplicated")
        if op_id:
            ids.add(op_id)
        # operations are themselves declared as native primitives; public auxiliaries require an explicit declaration.
        role = raw.get("role", raw.get("operation_role", "unknown_object_primitive"))
        if not isinstance(role, str) or role not in (PUBLIC_ROLES | PRIMITIVE_ROLES):
            role = "unknown"
            own.append("The operation role is unknown; it cannot be excluded as a free public auxiliary")
        feedback, feedback_errors = _operation_feedback(raw, op_code)
        feedback_errors = []
        for item in feedback["declaration_diagnostics"]:
            native_error(item["code"], item["path"], item["message"])
            feedback_errors.append(own[-1])
        precision, precision_path = feedback["precision"], feedback["precision_path"]
        if precision_path is None and oracle.get("feedback_applies_to_all_operations") is True:
            try:
                precision = _quality(oracle.get("feedback_quality", oracle.get("precision")), allow_legacy_descriptor="feedback_quality" in oracle)
            except TagError as exc:
                native_error("invalid_precision", "", "Invalid global precision structure: " + str(exc))
                feedback_errors.append(own[-1])
                precision = None
            if precision == "exact" and feedback["noise"] not in {None, "none"} and not feedback["sampled"]:
                message = "Global exact precision conflicts with an explicit nonzero-noise declaration on the operation"
                own.append(message)
                feedback_errors.append(message)
                precision = None
        return_fields = []
        for name in ("returns", "return_components"):
            if name not in raw:
                continue
            value = raw[name]
            if isinstance(value, str):
                # Preserve an explicit opaque return label; never infer mathematical components from text such as Av.
                value = [value]
            elif value is not None and not isinstance(value, list):
                native_error("invalid_returns", "/" + name, "returns must be a single string, a list of strings, or null")
                value = None
            elif isinstance(value, list):
                for position, component in enumerate(value):
                    if not isinstance(component, str):
                        native_error("invalid_returns", f"/{name}/{position}", "Return components must be strings")
                if any(not isinstance(component, str) for component in value):
                    value = None
                else:
                    value = list(value)
            return_fields.append((name, value))
        replies = return_fields[0][1] if return_fields else None
        if any(value != replies for _, value in return_fields[1:]):
            native_error("conflicting_returns", "/" + return_fields[0][0], "Conflicting returns and return_components declarations")
            replies = None
        for message in own:
            if message not in noted_messages:
                native_diagnostics.append({"code": "invalid_native_declaration", "path": pointer, "message": message})
        row = {
            "operation_ref": op_id, "operation_code": op_code, "object_ref": object_ref,
            "role": role, "precision": precision, "sampled": feedback["sampled"], "returns": replies,
            "noise": feedback["noise"],
            "feedback_diagnostics": feedback_errors,
            "native_diagnostics": native_diagnostics,
            "source_pointer": pointer, "precision_pointer": pointer if legacy or precision_path is None else origins.get(f"/oracle/operations/{index}" + precision_path, pointer + precision_path),
            "noise_pointer": pointer if legacy or feedback["noise_path"] is None else origins.get(f"/oracle/operations/{index}" + feedback["noise_path"], pointer + feedback["noise_path"]),
            "query_signature": raw.get("query_signature"), "response_signature": raw.get("response_signature"),
            "domain_ref": raw.get("domain_ref"), "cost_rule_ref": raw.get("cost_rule_ref"),
            "view_ref": view if isinstance(view, str) else (view or {}).get("view_id"),
            "valid": not own, "legacy_structured": legacy,
        }
        operations.append(row)
        diagnostics.extend(f"operation[{index}]: {message}" for message in own)
    counts = {}
    for operation in operations:
        op_id = operation["operation_ref"]
        if op_id is not None:
            counts[op_id] = counts.get(op_id, 0) + 1
    for operation in operations:
        if counts.get(operation["operation_ref"], 0) > 1:
            operation["valid"] = False
            operation.setdefault("native_diagnostics", []).append({"code": "duplicate_operation_id", "path": operation["source_pointer"], "message": "Duplicate native operation ID prevents unique binding"})
    return {"operations": operations, "diagnostics": diagnostics, "complete": not diagnostics and bool(rows)}


def match_interface(profile: dict, requirement: dict, mode: str = "native") -> dict:
    """Three-valued interface screening: native requires the exact return set; supplies allows extra return quantities to be discarded.

    This function recognizes only free disposal of return components; it never derives mathematical reductions such as finite differences or probability conversions.
    """
    if mode not in {"native", "supplies"}:
        raise TagError("mode must be native or supplies")
    outcomes = []
    views = profile.get("views", []) or [{"view_id": None}]
    for view in views:
        vid = view.get("view_id")
        if requirement.get("view_ref") is not None and requirement["view_ref"] != vid:
            continue
        normalized = effective_native_operations(profile, vid)
        primitive = [op for op in normalized["operations"] if op["role"] not in PUBLIC_ROLES]
        specific = any(requirement.get(k) is not None for k in ("operation_ref", "operation_code", "object_ref", "returns"))
        if not specific:
            known = [op for op in primitive if op["valid"]]
            wanted = requirement.get("precision")
            if not normalized["complete"] or not known or any(op["precision"] is None or op["sampled"] for op in known):
                state = "unknown"
            elif wanted is None or all(op["precision"] == wanted for op in known):
                state = "matched"
            else:
                state = "conflict"
            outcomes.append({"view_id": vid, "state": state, "extra_capabilities": [], "conversions": [], "diagnostics": normalized["diagnostics"]})
            continue
        matched, maybe, extra = [], False, []
        for op in primitive:
            if not op["valid"]:
                maybe = True
                continue
            mismatch, unknown = False, False
            for key in ("operation_ref", "operation_code", "object_ref", "precision"):
                expected = requirement.get(key)
                if expected is None:
                    continue
                if op.get(key) is None:
                    unknown = True
                elif op[key] != expected:
                    mismatch = True
            required_returns = requirement.get("returns")
            if required_returns is not None:
                if not isinstance(required_returns, list) or any(not isinstance(x, str) for x in required_returns):
                    raise TagError("requirement.returns must be a list of strings")
                if op.get("returns") is None:
                    unknown = True
                elif mode == "native" and set(op["returns"]) != set(required_returns):
                    mismatch = True
                elif mode == "supplies" and not set(required_returns).issubset(op["returns"]):
                    mismatch = True
            if mismatch:
                continue
            if unknown:
                maybe = True
            else:
                matched.append(op["operation_ref"])
                extra.extend(sorted(set(op.get("returns") or []) - set(required_returns or op.get("returns") or [])))
        state = "matched" if matched else ("unknown" if maybe or not normalized["complete"] else "conflict")
        outcomes.append({"view_id": vid, "state": state, "operation_refs": matched, "extra_capabilities": sorted(set(extra)), "conversions": ([{"kind": "discard_return_components", "additional_calls": 0}] if extra else []), "diagnostics": normalized["diagnostics"]})
    state = "matched" if any(x["state"] == "matched" for x in outcomes) else ("unknown" if not outcomes or any(x["state"] == "unknown" for x in outcomes) else "conflict")
    return {"state": state, "mode": mode, "views": outcomes, "identity_decision": "requires_llm_reasoning"}


def vocabulary_index(vocabulary: dict | None) -> dict[str, dict]:
    """Accept the original Atlas human/machine sections or a single concepts vocabulary."""
    if not vocabulary:
        return {}
    result = {}
    for source in (vocabulary.get("machine", {}), vocabulary.get("human", {}), vocabulary):
        rows = source.get("concepts", []) if isinstance(source, dict) else []
        if isinstance(rows, dict):
            rows = rows.values()
        for row in rows:
            if isinstance(row, dict):
                cid = row.get("concept_id", row.get("id"))
                if isinstance(cid, str):
                    result[cid] = row
    return result


def human_vocabulary_index(vocabulary: dict | None) -> dict[str, dict]:
    """When a human section exists, consult only that section; machine registration does not imply approval of a navigation concept."""
    if not vocabulary:
        return {}
    if "human" in vocabulary or "machine" in vocabulary:
        return vocabulary_index(vocabulary.get("human", {}))
    return vocabulary_index(vocabulary)


def human_concept(concept_id: str, vocabulary: dict | None) -> tuple[str, dict, bool]:
    """Deterministic mapping of complete IDs; for an unregistered target, retain the original fact ID as proposed."""
    human = human_vocabulary_index(vocabulary)
    axis, group, value = concept_id.split(":")
    alias = HUMAN_CONCEPT_ALIASES.get(concept_id)
    grouped = HUMAN_GROUP_ALIASES.get(f"{axis}:{group}", f"{axis}:{group}") + ":" + value
    for target in (alias, grouped, concept_id):
        if target is not None and target in human:
            return target, human[target], True
    if not vocabulary_index(vocabulary):
        # Offline or new catalogs without a controlled vocabulary remain navigable, without falsely claiming that concepts are registered.
        return alias or grouped, {}, False
    return concept_id, {}, False


def expand_concepts(ids: set[str], vocabulary: dict | None = None) -> set[str]:
    """Follow only parent edges explicitly declared in the vocabulary; do not rely on colon prefixes or string similarity."""
    index, expanded, pending = vocabulary_index(vocabulary), set(ids), list(ids)
    while pending:
        row = index.get(pending.pop(), {})
        parents = row.get("retrieval_parent_ids", row.get("parent_ids", []))
        if not isinstance(parents, list):
            parents = []
        if isinstance(row.get("parent_id"), str):
            parents = parents + [row["parent_id"]]
        for parent in parents:
            if isinstance(parent, str) and parent not in expanded:
                expanded.add(parent)
                pending.append(parent)
    return expanded


def _facts(profile: dict, supplied: list[dict]) -> list[dict]:
    """Combine input facts with explicit enumerations that can be safely registered mechanically."""
    result = deepcopy(supplied)
    common = profile.get("common_specification", {})
    views = profile.get("views", [])

    def add(axis: str, group: str, value: str, pointer: str, view: str | None = None, op: str | None = None, obj: str | None = None) -> None:
        if not isinstance(value, str) or not re.fullmatch(r"[a-z0-9_]+", value):
            return
        result.append({"concept_id": f"{axis}:{group}:{value}", "axis": axis, "value": value, "object_ref": obj, "view_ref": view, "operation_ref": op, "source_pointer": pointer, "status": "known"})

    if isinstance(profile.get("primary_domain"), str):
        add("TASK", "task_family", profile["primary_domain"], "/primary_domain")
    task = common.get("task", {})
    if isinstance(task, dict):
        for index, domain in enumerate(task.get("navigation_domains", []) if isinstance(task.get("navigation_domains"), list) else []):
            add("TASK", "task_family", domain, f"/common_specification/task/navigation_domains/{index}")
        if isinstance(task.get("formulation_code"), str):
            add("TASK", "formulation", task["formulation_code"], "/common_specification/task/formulation_code")
    for view in views:
        vid = view["view_id"]
        normalized = effective_native_operations(profile, vid)
        for op in normalized["operations"]:
            if not op["valid"] or op["role"] in PUBLIC_ROLES:
                continue
            add("ORACLE", "operation", op["operation_code"], op["source_pointer"], vid, op["operation_ref"], op["object_ref"])
            if op["precision"]:
                add("ORACLE", "feedback_quality", op["precision"], op["precision_pointer"], vid, op["operation_ref"], op["object_ref"])
    unique = {}
    for fact in result:
        if not isinstance(fact, dict):
            raise TagError("Each tag_facts item must be an object")
        unique[digest(fact)] = fact
    return list(unique.values())


def project_tags(profile: dict, tag_facts: list, vocabulary: dict | None = None) -> dict:
    """Return the four native sidecars; the display layer does not alter source facts or unknown status."""
    if not isinstance(tag_facts, list):
        raise TagError("tag_facts must be a list")
    views = profile.get("views", [])
    view_ids = [v.get("view_id") for v in views]
    if not view_ids or any(not isinstance(v, str) or not v for v in view_ids) or len(set(view_ids)) != len(view_ids):
        raise TagError("profile must have nonempty, unique view_id values")
    sid = profile.get("setting_id")
    if not isinstance(sid, str) or not sid:
        raise TagError("setting_id is missing")
    vocab = vocabulary_index(vocabulary)
    vocab_version = (vocabulary or {}).get("version", (vocabulary or {}).get("machine", {}).get("version", "component-default/1"))
    facts = _facts(profile, tag_facts)
    feature_rows, classification_rows, facets, details = [], [], [], []
    axes = {axis: [] for axis in AXES}
    unknown_facts = []
    exact_views = {r["view_id"] for r in match_interface(profile, {"precision": "exact"})["views"] if r["state"] == "matched"}
    for fact in facts:
        cid, axis = fact.get("concept_id"), fact.get("axis")
        if not isinstance(cid, str) or not TAG_PATTERN.fullmatch(cid) or axis not in AXES or cid.split(":")[0] != axis:
            raise TagError(f"Tag concept_id / axis mismatch: {cid!r}, {axis!r}")
        _, group, cid_value = cid.split(":")
        pointer = fact.get("source_pointer")
        if not isinstance(pointer, str) or not pointer.startswith("/"):
            raise TagError(f"{cid} lacks a valid source_pointer")
        at(profile, pointer)
        view = fact.get("view_ref")
        if view is not None and view not in view_ids:
            raise TagError(f"{cid} is bound to an unknown view: {view}")
        scoped_pointer = re.match(r"^/views/(0|[1-9][0-9]*)(?:/|$)", pointer)
        if scoped_pointer:
            pointer_view = views[int(scoped_pointer.group(1))]["view_id"]
            if view != pointer_view:
                raise TagError(f"The source_pointer of {cid} belongs to {pointer_view}; it must not be bound to another view or as a common fact")
        status = fact.get("status", "unknown")
        if status not in {"known", "unknown", "not_applicable"}:
            raise TagError(f"{cid} has an invalid status")
        fviews = [view] if view else view_ids[:]
        operation_ref = fact.get("operation_ref")
        if operation_ref is not None:
            for vid in fviews:
                ops = effective_native_operations(profile, vid)
                found = [o for o in ops["operations"] if o["operation_ref"] == operation_ref]
                if len(found) != 1 or not found[0]["valid"]:
                    raise TagError(f"{cid} is bound to an unknown or invalid operation: {operation_ref} @ {vid}")
                if fact.get("object_ref") is not None and found[0]["object_ref"] != fact["object_ref"]:
                    raise TagError(f"{cid} object and operation have different scopes")
                op_pointer = found[0]["source_pointer"]
                if not (pointer == op_pointer or pointer.startswith(op_pointer + "/")):
                    # A specification statement may explicitly reference this operation; do not infer bindings from proximity.
                    statement_ref = None
                    probe = pointer
                    while probe:
                        val = at(profile, probe)
                        if isinstance(val, dict) and "operation_ref" in val:
                            statement_ref = val["operation_ref"]
                            break
                        probe = probe.rsplit("/", 1)[0]
                    if statement_ref != operation_ref:
                        raise TagError(f"{cid} source_pointer does not belong to its operation and has no explicit statement binding")
        value = fact.get("value", cid_value)
        if not isinstance(value, str) or not value:
            raise TagError(f"{cid} value must be a nonempty string")
        label = vocab.get(cid, {}).get("label", LABELS.get(cid_value, cid_value.replace("_", " ").capitalize()))
        fid = "feat_" + digest(fact)[:20]
        parent_ids = sorted(expand_concepts({cid}, vocabulary) - {cid})
        feature = {
            "feature_id": fid, "concept_id": cid, "axis": axis, "group": group, "value": value, "label": label,
            "status": status, "view_ids": fviews, "source_pointers": [pointer], "evidence_state": "structured",
            "bindings": [{"source_pointer": pointer, "view_ids": fviews, "view_scope_kind": "specific", "evidence_state": "structured", "pointer_state": "resolved", "object_ref": fact.get("object_ref"), "operation_ref": operation_ref}],
            "normalization_state": "controlled" if cid in vocab else "proposed", "retrieval_parent_ids": parent_ids,
        }
        feature_rows.append(feature)
        if status == "known":
            axes[axis].append(cid)
            classification_rows.append({"id": cid, "axis": axis, "group": group, "value": value, "label": label, "source_pointers": [pointer], "view_ids": fviews, "evidence_state": "structured", "evidence": [{"source_pointer": pointer, "view_ids": fviews, "state": "structured"}], "object_ref": fact.get("object_ref"), "operation_ref": operation_ref})
        else:
            unknown_facts.append(fact)
        nav_cid, nav_def, nav_controlled = human_concept(cid, vocabulary)
        nav_axis, nav_group, nav_value = nav_cid.split(":")
        exact_navigation = cid in EXACT_CONCEPTS or nav_cid == "ORACLE:quality:exact"
        nav_views = []
        for vid in fviews:
            if exact_navigation:
                if vid not in exact_views:
                    continue
                if operation_ref is not None:
                    source_ops = [op for op in effective_native_operations(profile, vid)["operations"] if op["operation_ref"] == operation_ref]
                    if not source_ops or source_ops[0]["role"] in PUBLIC_ROLES:
                        continue
            nav_views.append(vid)
        detail = {"concept_id": "detail:" + cid, "machine_concept_id": cid, "axis": axis, "group": group, "label": label, "parent_id": nav_cid if status == "known" and nav_views else None, "view_ids": fviews, "source_feature_ids": [fid], "source_pointers": [pointer], "display_level": "detail", "status": status, "normalization_state": "controlled" if cid in vocab else "proposed"}
        details.append(detail)
        if status == "known" and nav_views:
            facets.append({"concept_id": nav_cid, "axis": nav_axis, "group": nav_group, "value": nav_value, "label": nav_def.get("label", label), "parent_id": nav_def.get("parent_id"), "view_ids": nav_views, "source_feature_ids": [fid], "source_pointers": [pointer], "display_level": "navigation", "status": status, "normalization_state": "controlled" if nav_controlled else "proposed"})
    for axis in AXES:
        axes[axis] = sorted(set(axes[axis]))
    # Merge the same navigation concept while preserving the scope of every source and view.
    grouped: dict[str, dict] = {}
    for facet in facets:
        target = grouped.setdefault(facet["concept_id"], deepcopy(facet))
        for key in ("view_ids", "source_feature_ids", "source_pointers"):
            target[key] = sorted(set(target[key]) | set(facet[key]))
    operations = [dict(op, view_ref=vid) for vid in view_ids for op in effective_native_operations(profile, vid)["operations"]]
    canonical_hash, pretty_hash = digest(profile), hashlib.sha256(json_bytes(profile)).hexdigest()
    coverage = {axis: {"state": "classified" if axes[axis] else "unknown", "concept_ids": axes[axis]} for axis in AXES}
    unclassified = [axis for axis in AXES if not axes[axis]]
    classification = {"schema_version": "1.0.0", "taxonomy_version": vocab_version, "record_type": "setting_classification", "setting_id": sid, "profile_schema_version": profile.get("schema_version"), "profile_sha256": pretty_hash, "axes": axes, "tags": classification_rows, "operation_bindings": operations, "unparsed_count": len(unknown_facts), "unclassified_axes": unclassified, "classification_policy": "explicit_source_facts_only; missing_is_unknown; no_equivalence_claim"}
    human = {"schema_version": "1.0.0", "vocabulary_version": vocab_version, "setting_id": sid, "title": profile.get("title", sid), "profile_sha256": canonical_hash, "view_ids": view_ids, "facets": list(grouped.values()), "details": details, "views": [{"view_id": vid, "label": next(v.get("label", vid) for v in views if v["view_id"] == vid), "facet_ids": [f["concept_id"] for f in grouped.values() if vid in f["view_ids"]], "unknown_axes": unclassified} for vid in view_ids], "interface_notes": [], "notes": ["Navigation labels screen candidates; full specifications determine identity."]}
    machine = {"schema_version": "1.0.0", "vocabulary_version": vocab_version, "setting_id": sid, "profile_sha256": canonical_hash, "source_classification_profile_sha256": pretty_hash, "view_ids": view_ids, "features": feature_rows, "axis_coverage": coverage, "operation_bindings": operations, "unparsed_source_items": unknown_facts, "retrieval_concept_ids": sorted(expand_concepts({f["concept_id"] for f in feature_rows if f["status"] == "known"}, vocabulary)), "identity_decision": "requires_llm_reasoning", "purpose": "high_recall_screening_only", "review_state": "see_publication_receipt", "registry": deepcopy(profile.get("registry", {})), "tag_facts": facts}
    identity_axes = {"task": "task", "instance_model": "model", "oracle_interface": "oracle", "output": "output", "metric": "metric", "resource_model": "resource", "algorithms": "algorithms", "guarantee": "guarantee"}
    identity = {"schema_version": "1.0.0", "record_type": "setting_identity", "setting_id": sid, "normalization_version": "oracle-atlas-agents/1", "profile_sha256": pretty_hash, "axes": {key: {"source_pointer": "/common_specification/" + source if source in profile.get("common_specification", {}) else None, "state": "source_structured" if source in profile.get("common_specification", {}) else "unknown", "source_fields": deepcopy(profile.get("common_specification", {}).get(source))} for key, source in identity_axes.items()}, "parameters": {"source_pointer": "/parameters" if "parameters" in profile else None, "cross_setting_alignment": "requires_review"}, "views": [{"view_id": view["view_id"], "source_pointer": f"/views/{index}", "algorithms": deepcopy(view.get("algorithms")), "guarantees": deepcopy(view.get("guarantees")), "specification_overrides": deepcopy(view.get("specification_overrides", {}))} for index, view in enumerate(views)], "view_override_policy": {"object_values": "recursive_key_merge", "array_and_scalar_values": "override_replaces_entire_value", "absent_override_keys": "inherit_from_common_specification", "null": "explicit_value_not_deletion"}, "matching_policy": {"identity_decision": "requires_explicit_axis_correspondences_and_review", "hash_semantics": "integrity_only_not_mathematical_equivalence"}, "missing_field_semantics": "unknown_not_unrestricted"}
    return {"classification": classification, "human_tags": human, "machine_tags": machine, "identity": identity}


def facts_from_sidecars(profile: dict, machine: dict | None = None, classification: dict | None = None) -> list[dict]:
    """Read-only adaptation of legacy indices; do not write back or invent complete object/operation bindings."""
    machine, classification = machine or {}, classification or {}
    if isinstance(machine.get("tag_facts"), list):
        return deepcopy(machine["tag_facts"])
    result = []
    source_rows = machine.get("features", []) or classification.get("tags", [])
    for row in source_rows:
        if not isinstance(row, dict):
            continue
        cid = row.get("concept_id", row.get("id"))
        axis = row.get("axis")
        if not isinstance(cid, str) or axis not in AXES:
            continue
        bindings = row.get("bindings", []) or [{"source_pointer": pointer, "view_ids": row.get("view_ids", [])} for pointer in row.get("source_pointers", [])]
        for binding in bindings:
            for view in binding.get("view_ids", row.get("view_ids", [])) or [None]:
                fact = {"concept_id": cid, "axis": axis, "value": str(row.get("value", cid.split(":")[-1])), "object_ref": binding.get("object_ref"), "operation_ref": binding.get("operation_ref"), "view_ref": view, "source_pointer": binding.get("source_pointer"), "status": row.get("status", "known"), "legacy_binding": True}
                try:
                    at(profile, fact["source_pointer"])
                except (TagError, TypeError):
                    fact["status"] = "unknown"
                result.append(fact)
    return result


def inherit_unchanged_facts(previous: dict, current: dict, machine: dict,
                            classification: dict, supplied: list[dict]) -> tuple[list[dict], dict]:
    """Partial updates preserve bound facts of existing views; do not unconditionally transfer old known status to a new specification.

    Require the correct old profile hash, identical source values, an identical view contract, and a valid operation.
    Inherit an original common fact after expanding it over existing views; do not extend the conclusion to newly added views.
    New facts take precedence for the same scope/concept or source/group, allowing an explicit downgrade to unknown.
    """
    report = {"inherited": 0, "skipped": 0, "legacy_hash_verified": False}
    previous_hash = digest(previous) if previous else None
    if not previous or not machine or machine.get("profile_sha256") != previous_hash:
        return deepcopy(supplied), report
    report["legacy_hash_verified"] = True
    old_views = {v["view_id"]: v for v in previous.get("views", [])}
    new_views = {v["view_id"]: v for v in current.get("views", [])}
    old_ops, new_ops = {}, {}
    retained = []

    def shadows(new: dict, old: dict) -> bool:
        if new.get("object_ref") != old.get("object_ref") or new.get("operation_ref") != old.get("operation_ref"):
            return False
        # A new common fact overrides existing views for that source; a new local fact overrides only that view.
        if new.get("view_ref") not in (None, old.get("view_ref")):
            return False
        if new.get("concept_id") == old.get("concept_id"):
            return True
        new_id, old_id = new.get("concept_id", ""), old.get("concept_id", "")
        return (isinstance(new_id, str) and isinstance(old_id, str)
                and new_id.rsplit(":", 1)[0] == old_id.rsplit(":", 1)[0]
                and new.get("source_pointer") == old.get("source_pointer"))

    for original in facts_from_sidecars(previous, machine, classification):
        pointer = original.get("source_pointer")
        try:
            if canonical_bytes(at(previous, pointer)) != canonical_bytes(at(current, pointer)):
                report["skipped"] += 1
                continue
        except (TagError, TypeError):
            report["skipped"] += 1
            continue
        scope_views = [original["view_ref"]] if original.get("view_ref") else list(old_views)
        for vid in scope_views:
            if vid not in old_views or vid not in new_views or canonical_bytes(old_views[vid]) != canonical_bytes(new_views[vid]):
                report["skipped"] += 1
                continue
            fact = deepcopy(original)
            fact["view_ref"] = vid
            if any(shadows(new, fact) for new in supplied if isinstance(new, dict)):
                report["skipped"] += 1
                continue
            op_ref = fact.get("operation_ref")
            if op_ref is not None:
                if vid not in old_ops:
                    old_ops[vid] = effective_native_operations(previous, vid)
                    new_ops[vid] = effective_native_operations(current, vid)
                before = [op for op in old_ops[vid]["operations"] if op["operation_ref"] == op_ref]
                after = [op for op in new_ops[vid]["operations"] if op["operation_ref"] == op_ref]
                if len(before) != 1 or len(after) != 1 or not before[0]["valid"] or not after[0]["valid"] or canonical_bytes(before[0]) != canonical_bytes(after[0]):
                    report["skipped"] += 1
                    continue
            # Legacy native formats sometimes allow broader scopes than this version. Check with the same projection validator
            # so unknown legacy bindings neither block new facts nor bypass the new source/view/operation rules.
            try:
                project_tags(current, [fact])
            except TagError:
                report["skipped"] += 1
                continue
            fact["inherited_from_profile_sha256"] = previous_hash
            retained.append(fact)
            report["inherited"] += 1
    return retained + deepcopy(supplied), report
