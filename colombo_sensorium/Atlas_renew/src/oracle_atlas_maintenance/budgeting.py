"""Pure role budgeting: exact frozen previews and feasible own-read schedules.

This module performs no I/O, tool call, source read, approval or publication.
An estimated read is never read credit. Scientific gates remain authoritative.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math


PREVIEW_ARTIFACT = "budgeting_previews"
PREVIEW_KEYS = ("compact_profile", "joint_analysis_template", "joint_analysis", "synthesis_catalog",
                "review_input_pack", "retained_adoption_catalog")
CATALOG_PREVIEW_KEYS = ("baseline_catalog", "synthesis_catalog")
CATALOG_PROJECTION_VERSION = 1


class BudgetingError(ValueError):
    """A deterministic budget cannot preserve the required frozen contract."""


def _dump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _hash(value):
    return hashlib.sha256(_dump(value).encode()).hexdigest()


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise BudgetingError(name + " must be a positive integer")
    return value


def _parts(pointer):
    if not isinstance(pointer, str) or pointer and not pointer.startswith("/"):
        raise BudgetingError("An exact frozen read requires a JSON Pointer")
    return tuple(part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")) if pointer else ()


def _pointer(parts):
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in parts) if parts else ""


def _at(value, parts):
    for part in parts:
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def _replace(value, parts, replacement):
    parent = _at(value, parts[:-1])
    if isinstance(parent, list):
        parent[int(parts[-1])] = replacement
    else:
        parent[parts[-1]] = replacement


def _preview_container(context):
    artifacts = context.setdefault("artifacts", {})
    bucket = artifacts.get(PREVIEW_ARTIFACT)
    if bucket is None:
        bucket = {"kind": "controller_budgeting_previews", "version": 1, "values": {}}
        artifacts[PREVIEW_ARTIFACT] = bucket
    if not isinstance(bucket, dict) or bucket.get("kind") != "controller_budgeting_previews" or \
            bucket.get("version") != 1 or not isinstance(bucket.get("values"), dict):
        raise BudgetingError("Reserved preview artifact is not a controller-owned budgeting container")
    return bucket


def _store_preview(context, key, value):
    values = _preview_container(context)["values"]
    if key in values and values[key] != value:
        raise BudgetingError("A frozen budgeting preview key cannot be overwritten")
    values[key] = deepcopy(value)
    return {"provided_complete": False, "artifact": PREVIEW_ARTIFACT, "pointer": "/values/" + key,
            "content_hash": _hash(value)}


def _catalog_reference(name, value):
    key = _hash({"context_pointer": [name], "original_sha256": _hash(value)})
    return {"provided_complete": False, "artifact": PREVIEW_ARTIFACT, "pointer": "/values/" + key,
            "content_hash": _hash(value), "note": "Read this complete exact derived catalog by artifact_read before approval. This reference grants no native/source read credit or scientific approval."}


def _catalog_context_supported(context):
    witness = context.get("finite_research_scope_witness", {})
    artifact = context.get("artifacts", {}).get("scout_research_scope")
    return (context.get("budgets", {}).get("finite_research_scope") is True
            and context.get("maintenance_role") == "reviewer" and isinstance(artifact, dict)
            and isinstance(witness, dict) and witness.get("artifact") == "scout_research_scope"
            and witness.get("pointer") == "" and witness.get("content_hash") == _hash(artifact))


def catalog_projection_reads(context):
    """Validate exact controller-owned whole-catalog descriptors, never math."""
    runtime = context.get("runtime_budget", {})
    version = runtime.get("catalog_projection_version")
    if version is None:
        if runtime.get("catalog_read_requirements") is not None or any(
                isinstance(context.get(key), dict) and context[key].get("provided_complete") is False
                and context[key].get("artifact") == PREVIEW_ARTIFACT for key in CATALOG_PREVIEW_KEYS):
            raise BudgetingError("Whole catalog projection requires its exact supported budgeting marker")
        return []
    if type(version) is not int or version != CATALOG_PROJECTION_VERSION:
        raise BudgetingError("Unsupported whole catalog projection version")
    if not _catalog_context_supported(context):
        raise BudgetingError("Whole catalog projection needs the controller-bound finite reviewer context")
    rows = runtime.get("catalog_read_requirements")
    if not isinstance(rows, list) or not rows or len(rows) > len(CATALOG_PREVIEW_KEYS):
        raise BudgetingError("Whole catalog projection needs its complete own-read inventory")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"context_key", "artifact", "pointer", "content_hash"}:
            raise BudgetingError("Invalid whole catalog read descriptor")
        name = row["context_key"]
        if name not in CATALOG_PREVIEW_KEYS or name in seen or row["artifact"] != PREVIEW_ARTIFACT:
            raise BudgetingError("Whole catalog projection changed a noncatalog context field")
        seen.add(name)
        try:
            value = _at(context["artifacts"][PREVIEW_ARTIFACT], _parts(row["pointer"]))
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise BudgetingError("Whole catalog frozen original is unavailable") from exc
        expected = _catalog_reference(name, value)
        if not isinstance(value, dict) or context.get(name) != expected or any(row[key] != expected[key]
                for key in ("artifact", "pointer", "content_hash")):
            raise BudgetingError("Whole catalog descriptor differs from its exact frozen original")
    projected = {name for name in CATALOG_PREVIEW_KEYS if isinstance(context.get(name), dict)
                 and context[name].get("provided_complete") is False and context[name].get("artifact") == PREVIEW_ARTIFACT}
    if projected != seen:
        raise BudgetingError("Whole catalog own-read inventory omits a projected catalog")
    return deepcopy(rows)


def require_catalog_projection_reads(context, host):
    from .evidence_basis import fully_read_frozen_value_or_ancestor
    for row in catalog_projection_reads(context):
        root = context["artifacts"][PREVIEW_ARTIFACT]
        if not fully_read_frozen_value_or_ancestor(host, PREVIEW_ARTIFACT, row["pointer"], root):
            raise BudgetingError("Reviewer must actually read every page of the omitted complete derived catalog")


def prompt_context(context):
    """The exact initial runtime accounting shape, including every artifact hash."""
    result = {key: value for key, value in context.items() if key != "artifacts"}
    result["frozen_artifact_hashes"] = {key: _hash(value) for key, value in context.get("artifacts", {}).items()}
    return result


def initial_input_characters(instructions, context):
    return len(instructions) + len(_dump(prompt_context(context)))


def _all_strings(value):
    if isinstance(value, str):
        return {value}
    if isinstance(value, dict):
        return set(value) | set().union(*(_all_strings(v) for v in value.values())) if value else set()
    if isinstance(value, list):
        return set().union(*(_all_strings(v) for v in value)) if value else set()
    return set()


def _read_schedule(artifacts, required, page_chars):
    """Minimum page-count exact-ancestor cover; ties prefer narrower objects."""
    schedules = []
    for artifact, pointers in sorted(required.items()):
        root = artifacts[artifact]
        wanted = {_parts(pointer) for pointer in pointers}
        def plan(prefix):
            value = _at(root, prefix)
            count = len(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))
            direct = [{"artifact": artifact, "pointer": _pointer(prefix), "content_hash": _hash(value),
                       "serialized_characters": count, "pages": max(1, math.ceil(count / page_chars))}]
            if prefix in wanted:
                return direct
            children = sorted({parts[len(prefix)] for parts in wanted if parts[:len(prefix)] == prefix and len(parts) > len(prefix)})
            split = [row for child in children for row in plan(prefix + (child,))]
            return direct if sum(row["pages"] for row in direct) < sum(row["pages"] for row in split) else split
        schedules.extend(plan(()))
    return schedules


def estimate_role_tool_budget(role, context, config, *, max_tool_calls=None):
    """Return an estimated role-owned read plan and opt-in effective hard cap."""
    if role not in {"scout", "reviewer"}:
        raise BudgetingError("Unknown maintenance role")
    budgets = config.get("budgets", {})
    adaptive = budgets.get("adaptive_tool_budget", False) is True
    base = _positive(budgets.get("max_tool_calls_per_stage", 40), "max_tool_calls_per_stage")
    page_chars = min(12000, _positive(budgets.get("max_tool_chars", 10000), "max_tool_chars"))
    source_limit = _positive(budgets.get("max_source_reads_per_setting", 12), "max_source_reads_per_setting")
    artifacts = context.get("artifacts", {})
    required = {}
    def add(artifact, pointer, expected=None):
        if artifact not in {"baseline", "prepared", "scout_research_scope", PREVIEW_ARTIFACT} or artifact in {"prepared", "scout_research_scope", PREVIEW_ARTIFACT} and role == "scout":
            return
        if artifact not in artifacts:
            raise BudgetingError("Missing frozen artifact for mandatory own-read: " + artifact)
        try:
            value = _at(artifacts[artifact], _parts(pointer))
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise BudgetingError("Unknown mandatory frozen pointer: " + artifact + pointer) from exc
        if expected is not None and _hash(value) != expected:
            raise BudgetingError("Mandatory frozen read hash disagrees: " + artifact + pointer)
        required.setdefault(artifact, set()).add(pointer)
    for name in ("baseline", "prepared") if role == "reviewer" else ("baseline",):
        if isinstance(artifacts.get(name), dict) and "joint_analysis" in artifacts[name]:
            add(name, "/joint_analysis")
    if (role == "scout" and budgets.get("finite_research_scope") is True
            and context.get("maintenance_lane", {}).get("candidate") == "closed_bracket_check"):
        for key in ("common_specification", "parameters", "views", "quantities", "resource_projections", "bounds", "comparisons", "proofs"):
            if key in artifacts.get("baseline", {}):
                add("baseline", "/" + key)
    findings = context.get("findings", [])
    for finding in findings:
        for ref in finding.get("baseline_refs", []):
            add("baseline", ref["pointer"], ref.get("sha256"))
    scope = context.get("review_scope", {})
    for item in scope.get("retention_read_obligations", []):
        add(item["artifact"], item["pointer"], item.get("sha256"))
    if role == "reviewer":
        for row in catalog_projection_reads(context):
            add(row["artifact"], row["pointer"], row["content_hash"])
        witness = context.get("finite_research_scope_witness")
        if isinstance(witness, dict) and witness.get("artifact") == "scout_research_scope":
            add("scout_research_scope", "", witness.get("content_hash"))
        for item in context.get("review_input_pack", {}).get("items", []):
            add(item["artifact"], item["pointer"], item.get("content_hash"))
        # Exact prepared claim/proof dependencies, never every retained old bound.
        prepared = artifacts.get("prepared", {})
        index = {}
        aliases = ("id", "bound_id", "comparison_id", "proof_id", "regime_id", "evidence_id", "source_id", "quantity_id", "parameter_id", "view_id")
        for collection in ("bounds", "proofs", "regimes", "evidence", "references", "quantities", "parameters", "resource_projections", "views"):
            for i, row in enumerate(prepared.get(collection, [])):
                rid = next((row[key] for key in aliases if key in row), None)
                if isinstance(rid, str):
                    index.setdefault(rid, []).append((f"/{collection}/{i}", row))
        seeds = set(scope.get("fresh_review_required_bound_ids", []))
        for change in context.get("delta", []):
            seeds.add(change["id"])
            if change.get("prepared_pointer"):
                add("prepared", change["prepared_pointer"])
                seeds |= _all_strings(_at(prepared, _parts(change["prepared_pointer"]))) & set(index)
        seen = set()
        while seeds - seen:
            rid = sorted(seeds - seen)[0]
            seen.add(rid)
            for pointer, row in index.get(rid, []):
                add("prepared", pointer)
                seeds |= _all_strings(row) & set(index)
    schedule = _read_schedule(artifacts, required, page_chars)
    source_hashes = sorted({sha for finding in findings if finding.get("impact") not in {"no_effect", "incomparable"}
                            for sha in finding.get("source_hashes", [])})
    if len(source_hashes) > source_limit:
        raise BudgetingError("Known source own-read requirements exceed the unchanged source-read cap")
    reserve = _positive(budgets.get("adaptive_tool_reserve", 10), "adaptive_tool_reserve")
    pages = sum(row["pages"] for row in schedule)
    mandatory_calls = pages + len(source_hashes)
    required_calls = mandatory_calls + reserve
    contingency = math.ceil(mandatory_calls / 4)
    role_key = "scout_tool_calls_cap" if role == "scout" else "reviewer_tool_calls_cap"
    role_cap = _positive(budgets.get(role_key, 64 if role == "scout" else 128), role_key)
    absolute = _positive(budgets.get("auto_tools_hard_cap", 128), "auto_tools_hard_cap")
    hard = min(role_cap, absolute) if adaptive else base
    if max_tool_calls is not None:
        hard = min(hard, _positive(max_tool_calls, "remaining max_tool_calls"))
    floor = min(40, hard) if max_tool_calls is not None else 40
    minimum = min(base, hard) if max_tool_calls is not None else base
    reserve_controls = budgets.get("reserve_control_calls", False) is True
    if reserve_controls:
        # Keep the configured research allowance distinct from the operational
        # reserve. A remaining-cycle cap cannot silently consume that reserve.
        minimum = base + reserve
    if required_calls > hard or (adaptive or reserve_controls) and max(floor, minimum) > hard:
        raise BudgetingError(f"Mandatory own-read schedule plus reserve needs {max(floor if adaptive else 0, minimum, required_calls)} calls; hard cap is {hard}")
    recommended = mandatory_calls + contingency + reserve
    if reserve_controls:
        recommended = max(base + reserve, recommended)
    effective = min(hard, max(floor, minimum, recommended)) if adaptive else hard
    result = {"role": role, "adaptive": adaptive, "configured_base_calls": base, "effective_tool_calls": effective,
            "hard_cap": hard, "page_characters": page_chars, "required_read_pages": pages,
            "mandatory_calls": mandatory_calls, "contingency_calls": contingency,
            "recommended_calls_before_hard_cap": recommended, "contingency_clipped": effective < recommended,
            "remaining_tool_limit": max_tool_calls,
            "required_source_hashes": source_hashes, "source_read_cap_unchanged": source_limit,
            "source_lengths_unknown": bool(source_hashes), "status_checkpoint_handoff_reserve": reserve,
            "read_schedule": schedule, "required_pointers": {name: sorted(values) for name, values in required.items()},
            "own_read_credit": False, "scientific_approval": False,
            "note": "A feasible complete-read estimate, not observed reads. Unknown discovery and source lengths can require further work; no cap or scientific gate is waived."}
    if reserve_controls:
        result.update(reserve_control_calls=True, operational_reserve_calls=reserve,
                      minimum_base_with_reserve_calls=base + reserve)
    return result


def _candidates(context):
    candidates = []
    def add(path, native=None, owner=None):
        value = _at(context, path)
        if isinstance(value, dict) and value.get("provided_complete") is False:
            return
        candidates.append({"path": path, "value": value, "native": native, "owner": owner,
                           "characters": len(_dump(value))})
    compact = context.get("compact_profile", {})
    for key in ("bounds", "comparisons"):
        if isinstance(compact.get(key), list) and compact[key]:
            add(("compact_profile", key))
    for key, artifact in (("joint_analysis_template", "baseline"), ("joint_analysis", "prepared")):
        value = context.get(key)
        if isinstance(value, dict) and value and value.get("provided_complete") is not False:
            native = (artifact, "/joint_analysis") if context.get("artifacts", {}).get(artifact, {}).get("joint_analysis") == value else None
            add((key,), native)
    for key in ("synthesis_catalog", "review_input_pack"):
        packet = context.get(key, {})
        if not isinstance(packet, dict):
            continue
        for i, item in enumerate(packet.get("items", [])):
            if isinstance(item, dict) and "value" in item:
                previous = item["value"]
                if isinstance(previous, dict) and previous.get("provided_complete") is False:
                    try:
                        preserved = _at(context["artifacts"][previous["artifact"]], _parts(previous["pointer"]))
                    except (KeyError, IndexError, TypeError, ValueError) as exc:
                        raise BudgetingError("Existing preview reference is not accessible in frozen artifacts") from exc
                    if previous.get("content_hash") != _hash(preserved) or item.get("content_hash") != _hash(preserved):
                        raise BudgetingError("Existing preview reference changed its frozen value hash")
                    continue
                native = None
                artifact, pointer = item.get("artifact"), item.get("pointer")
                if artifact in context.get("artifacts", {}) and isinstance(pointer, str):
                    try:
                        full = _at(context["artifacts"][artifact], _parts(pointer))
                    except (KeyError, IndexError, TypeError, ValueError):
                        full = object()
                    if full != item["value"] or item.get("content_hash") != _hash(full):
                        raise BudgetingError("Preview does not bind its exact frozen artifact value")
                    native = (artifact, pointer)
                add((key, "items", str(i), "value"), native, (key, "items", str(i)))
    for i, row in enumerate(context.get("retained_adoption_catalog", {}).get("rows", [])):
        if isinstance(row, dict) and "formula" in row:
            # Keep IDs, all contract/eligibility flags and selected references inline.
            add(("retained_adoption_catalog", "rows", str(i), "formula"))
    return sorted(candidates, key=lambda item: (-item["characters"], item["path"]))


def prepare_role_budget(role, instructions, context, config, *, max_chars=None, max_tool_calls=None):
    """Allocate preview payloads and an opt-in role hard cap before any paid call."""
    if role not in {"scout", "reviewer"} or not isinstance(instructions, str):
        raise BudgetingError("Budgeting requires a known role and complete instructions")
    result, effective = deepcopy(context), deepcopy(config)
    budgets = effective.setdefault("budgets", {})
    input_auto = budgets.get("adaptive_input_budget", False) is True
    tools_auto = budgets.get("adaptive_tool_budget", False) is True
    if not input_auto and not tools_auto:
        return {"context": result, "config": effective, "audit": {"version": 1, "enabled": False}}
    limit = _positive(max_chars if max_chars is not None else budgets.get("max_context_chars", 120000), "max_context_chars")
    original_artifacts = deepcopy(result.get("artifacts", {}))
    original_bucket = original_artifacts.get(PREVIEW_ARTIFACT)
    if original_bucket is not None:
        _preview_container(result)
    original_hashes = {key: _hash(result[key]) for key in PREVIEW_KEYS if key in result}
    original_chars = initial_input_characters(instructions, result)
    estimate = estimate_role_tool_budget(role, result, effective, max_tool_calls=max_tool_calls)
    plan_limit = _positive(budgets.get("adaptive_plan_preview_items", 6), "adaptive_plan_preview_items")
    def recommend(current):
        plan = {"provided_complete": len(current["read_schedule"]) <= plan_limit,
            "items": deepcopy(current["read_schedule"][:plan_limit]),
            "omitted_count": max(0, len(current["read_schedule"]) - plan_limit),
            "own_read_credit": False, "scientific_approval": False}
        if not plan["provided_complete"]:
            key = _hash({"kind": "role_read_plan", "role": role, "schedule": current["read_schedule"]})
            plan["full_plan"] = _store_preview(result, key, current["read_schedule"])
        return plan
    recommended_plan = recommend(estimate)
    if tools_auto:
        budgets["max_tool_calls_per_stage"] = estimate["effective_tool_calls"]
        result.setdefault("budgets", {})["max_tool_calls_per_stage"] = estimate["effective_tool_calls"]
    audit = {"version": 1, "enabled": True, "role": role, "adaptive_input_budget": input_auto, "adaptive_tool_budget": tools_auto,
             "max_context_characters": limit, "original_initial_characters": original_chars,
             "original_context_sha256": _hash(context), "original_config_sha256": _hash(config),
             "original_context_fields": {key: {"present": key in context, "value": deepcopy(context.get(key))}
                 for key in ("budgets", "runtime_budget")},
             "original_config_budgets": {"present": "budgets" in config, "value": deepcopy(config.get("budgets"))},
             "original_preview_hashes": original_hashes, "tool_estimate": estimate, "projections": [],
             "mandatory_calls": estimate["mandatory_calls"],
             "original_preview_artifact_sha256": _hash(original_bucket) if original_bucket is not None else None,
             "source_read_credit": False, "baseline_read_credit": False, "scientific_approval": False}
    if estimate.get("reserve_control_calls") is True:
        audit.update(reserve_control_calls=True, operational_reserve_calls=estimate["operational_reserve_calls"])
    def summary():
        metadata = {"version": 1, "role": role, "original_preview_hashes": original_hashes,
                "projected_values": len(audit["projections"]), "effective_tool_calls": estimate["effective_tool_calls"],
                "known_read_pages": estimate["required_read_pages"], "source_read_cap_unchanged": estimate["source_read_cap_unchanged"],
                "recommended_read_plan": recommended_plan,
                "own_read_credit": False, "scientific_approval": False, "full_audit_sha256": "0" * 64}
        if estimate.get("reserve_control_calls") is True:
            metadata.update(reserve_control_calls=True, operational_reserve_calls=estimate["operational_reserve_calls"])
        if "catalog_projection_version" in audit:
            metadata.update(catalog_projection_version=audit["catalog_projection_version"],
                            catalog_read_requirements=deepcopy(audit["catalog_read_requirements"]))
        return metadata
    result["runtime_budget"] = summary()
    actual = initial_input_characters(instructions, result)
    if actual > limit and input_auto:
        for candidate in _candidates(result):
            if actual <= limit:
                break
            path, value = candidate["path"], candidate["value"]
            native = candidate["native"]
            if native is None:
                key = _hash({"context_pointer": list(path), "original_sha256": _hash(value)})
                artifact, pointer = PREVIEW_ARTIFACT, "/values/" + key
            else:
                artifact, pointer = native
            reference = {"provided_complete": False, "artifact": artifact, "pointer": pointer,
                         "content_hash": _hash(value), "note": "Exact omitted preview value; this reference grants no native/source read credit or approval."}
            if isinstance(value, list):
                reference["record_count"] = len(value)
                reference["record_ids"] = [next((row[key] for key in ("id", "bound_id", "comparison_id") if key in row), None)
                                           for row in value if isinstance(row, dict)]
            if len(_dump(reference)) >= len(_dump(value)):
                continue
            if native is None:
                _store_preview(result, key, value)
            metadata_before = []
            def remember(parent_path, key):
                parent = _at(result, parent_path)
                metadata_before.append({"context_pointer": _pointer(parent_path + (key,)),
                    "present": key in parent, "value": deepcopy(parent.get(key))})
            if candidate["owner"]:
                remember(candidate["owner"], "provided_complete")
                remember((path[0],), "incomplete")
                if path[0] == "review_input_pack" and _at(result, candidate["owner"]).get("fixed_scope"):
                    remember((path[0],), "fixed_scope_incomplete")
            _replace(result, path, reference)
            if candidate["owner"]:
                _at(result, candidate["owner"])["provided_complete"] = False
                result[path[0]]["incomplete"] = True
                if path[0] == "review_input_pack" and _at(result, candidate["owner"]).get("fixed_scope"):
                    result[path[0]]["fixed_scope_incomplete"] = True
            audit["projections"].append({"context_pointer": _pointer(path), "original_sha256": _hash(value),
                "artifact": artifact, "pointer": pointer, "provided_complete": False,
                "metadata_before": metadata_before})
            result["runtime_budget"] = summary()
            actual = initial_input_characters(instructions, result)
    # Only after the existing exact leaf projections are insufficient, project
    # redundant derived catalogs. Findings, delta, fixed contract, pending work,
    # research/retention scope and all native reading requirements stay intact.
    if (actual > limit and input_auto and role == "reviewer"
            and config.get("budgets", {}).get("finite_research_scope") is True
            and _catalog_context_supported(result)):
        original_native_reads = {key: value for key, value in estimate["required_pointers"].items()
                                 if key != PREVIEW_ARTIFACT}
        candidates = sorted((key for key in CATALOG_PREVIEW_KEYS if isinstance(result.get(key), dict)
                            and result[key].get("provided_complete") is not False),
                            key=lambda key: (-len(_dump(result[key])), key))
        for name in candidates:
            if actual <= limit:
                break
            value = deepcopy(result[name])
            reference = _catalog_reference(name, value)
            if len(_dump(reference)) >= len(_dump(value)):
                continue
            key = reference["pointer"].rsplit("/", 1)[1]
            _store_preview(result, key, value)
            result[name] = reference
            audit["catalog_projection_version"] = CATALOG_PROJECTION_VERSION
            audit.setdefault("catalog_read_requirements", []).append({"context_key": name,
                **{field: reference[field] for field in ("artifact", "pointer", "content_hash")}})
            audit["projections"].append({"context_pointer": "/" + name, "original_sha256": _hash(value),
                "artifact": PREVIEW_ARTIFACT, "pointer": reference["pointer"], "provided_complete": False,
                "metadata_before": []})
            result["runtime_budget"] = summary()
            # Re-estimate from the configured base, not the already allocated
            # effective cap; otherwise each projection would reserve twice.
            estimate = estimate_role_tool_budget(role, result, config, max_tool_calls=max_tool_calls)
            if {key: value for key, value in estimate["required_pointers"].items()
                    if key != PREVIEW_ARTIFACT} != original_native_reads:
                raise AssertionError("Whole catalog projection changed mandatory native/source proof reads")
            recommended_plan = recommend(estimate)
            if tools_auto:
                budgets["max_tool_calls_per_stage"] = estimate["effective_tool_calls"]
                result.setdefault("budgets", {})["max_tool_calls_per_stage"] = estimate["effective_tool_calls"]
            audit["tool_estimate"], audit["mandatory_calls"] = estimate, estimate["mandatory_calls"]
            result["runtime_budget"] = summary()
            actual = initial_input_characters(instructions, result)
    if actual > limit:
        raise BudgetingError(f"Mandatory role input needs {actual} characters after all permitted preview projections; hard cap is {limit}")
    if any(result["artifacts"].get(key) != value for key, value in original_artifacts.items() if key != PREVIEW_ARTIFACT):
        raise AssertionError("Adaptive budgeting changed an original frozen artifact")
    if original_bucket is not None:
        current_bucket = result["artifacts"][PREVIEW_ARTIFACT]
        if {key: value for key, value in current_bucket.items() if key != "values"} != {key: value for key, value in original_bucket.items() if key != "values"} or \
                any(key not in current_bucket["values"] or current_bucket["values"][key] != value
                    for key, value in original_bucket["values"].items()):
            raise AssertionError("Adaptive budgeting changed existing frozen preview entries or metadata")
    old_keys = set(original_bucket["values"]) if original_bucket else set()
    new_keys = set(result.get("artifacts", {}).get(PREVIEW_ARTIFACT, {}).get("values", {}))
    audit["preview_artifact_added_keys"] = sorted(new_keys - old_keys)
    audit["final_initial_characters"] = actual
    audit["remaining_characters"] = limit - actual
    result["runtime_budget"]["full_audit_sha256"] = _hash(audit)
    if initial_input_characters(instructions, result) != actual:
        raise AssertionError("Final runtime-budget accounting changed after its exact postcheck")
    return {"context": result, "config": effective, "audit": audit}
