"""Structural-semantic validation of native sidecars; it does not judge mathematical identity or derive scientific facts."""
from __future__ import annotations

import re
from typing import Any

from .tags import (AXES, EXACT_CONCEPTS, PUBLIC_ROLES, TAG_PATTERN, TagError, _noise, _quality, at, effective_native_operations, effective_specification,
                   expand_concepts, human_concept, human_vocabulary_index,
                   match_interface, vocabulary_index)


def validate_sidecars(files: dict, vocabulary: dict | None = None, *, baseline_files=None) -> list[dict]:
    """Aggregate all managed source, scope, and vocabulary errors without modifying any input.

    Proposed concepts may be retained; unknown common axes use null sources. Controlled parent edges must come from the vocabulary;
    each source of a grouped human facet must still be supported by the bindings of its machine feature.
    """
    errors: list[dict] = []
    profile = files.get("profile.json") if isinstance(files, dict) else None

    def error(code: str, filename: str, path: str, message: str) -> None:
        item = {"code": code, "file": filename, "path": path, "message": message}
        if item not in errors:
            errors.append(item)

    if not isinstance(profile, dict):
        return [{"code": "profile_missing", "file": "profile.json", "path": "", "message": "Sidecar validation requires a profile object"}]
    def rows(value: Any, filename: str, path: str) -> list:
        if not isinstance(value, list):
            error("array", filename, path, "This field must be a list")
            return []
        return value

    views = rows(profile.get("views", []), "profile.json", "/views")
    view_ids = [v.get("view_id") for v in views if isinstance(v, dict)]
    if not view_ids or any(not isinstance(v, str) or not v for v in view_ids) or len(view_ids) != len(set(view_ids)):
        error("view_ids", "profile.json", "/views", "view_id values must be nonempty, unique strings")
    operations, declared_feedback = {}, {}
    exact_views = set()
    for vid in view_ids:
        if not isinstance(vid, str):
            continue
        try:
            normalized = effective_native_operations(profile, vid)
            operations[vid] = normalized["operations"]
            # An absent complete legacy interface remains unknown; invalid rows must not silently bypass contradictions in explicit operations.
            for row in operations[vid]:
                diagnostics = row.get("native_diagnostics", [])
                for item in diagnostics:
                    error("native_operation_declaration", "profile.json", item.get("path", row.get("source_pointer", "/views")), f"{vid}: {item.get('message', '')}")
                if not diagnostics:  # Support legacy frozen normalizer records.
                    for message in row.get("feedback_diagnostics", []):
                        error("native_operation_declaration", "profile.json", "/views", f"{vid}: {message}")
            # Enumerate source fields independently; the projector's own parsing result alone cannot establish projection completeness.
            spec, origins = effective_specification(profile, vid)
            oracle = spec.get("oracle", {})
            raw_ops = oracle.get("operations", []) if isinstance(oracle, dict) else []
            declared_feedback[vid] = {}
            for index, raw in enumerate(raw_ops if isinstance(raw_ops, list) else []):
                if not isinstance(raw, dict):
                    continue
                aliases = [raw[key] for key in ("id", "operation_id", "operation_ref") if key in raw]
                if not aliases or not isinstance(aliases[0], str) or any(v != aliases[0] for v in aliases[1:]):
                    continue
                op_id = aliases[0]
                contract = {}
                containers = [("", raw)]
                if isinstance(raw.get("response"), dict):
                    containers.append(("/response", raw["response"]))
                for field, names, decode in (("precision", ("feedback_quality", "precision", "quality"), _quality), ("noise", ("noise",), _noise)):
                    declarations = []
                    for prefix, obj in containers:
                        for name in names:
                            if name in obj:
                                logical = f"/oracle/operations/{index}" + prefix + "/" + name
                                try:
                                    decoded = decode(obj[name], allow_legacy_descriptor=name == "feedback_quality") if field == "precision" else decode(obj[name])
                                except TagError as exc:
                                    decoded = None
                                    error("native_operation_declaration", "profile.json", origins.get(logical, logical), f"{vid}: {exc}")
                                declarations.append((origins.get(logical), decoded))
                    if declarations and all(value == declarations[0][1] for _, value in declarations):
                        contract[field] = declarations[0][1]
                        contract[field + "_pointers"] = {p for p, _ in declarations if isinstance(p, str)}
                declared_feedback[vid][op_id] = contract
        except (TagError, AttributeError, TypeError, ValueError) as exc:
            error("native_operations", "profile.json", "/views", str(exc))
            operations[vid] = []
    try:
        exact_views = {v["view_id"] for v in match_interface(profile, {"precision": "exact"})["views"] if v["state"] == "matched"}
    except (TagError, AttributeError, TypeError, ValueError) as exc:
        error("native_interface", "profile.json", "/views", str(exc))
    vocab, human_vocab = vocabulary_index(vocabulary), human_vocabulary_index(vocabulary)

    def scope(row: dict, filename: str, path: str, inherited: list | None = None) -> list:
        ids = row.get("view_ids", inherited)
        if "view_ids" in row and not isinstance(ids, list):
            error("view_scope", filename, path, "view_ids must be a list of stable view IDs")
            return []
        if ids is None:
            ref = row.get("view_ref")
            ids = [ref] if ref is not None else view_ids[:]
        if not isinstance(ids, list) or any(not isinstance(v, str) for v in ids):
            error("view_scope", filename, path, "view_ids must be a list of stable view IDs")
            return []
        for vid in ids:
            if vid not in view_ids:
                error("unknown_view", filename, path, f"Unknown view ID: {vid}")
        return ids

    def pointer(value: Any, filename: str, path: str, ids: list | None = None,
                *, nullable: bool = False, merged: bool = False) -> bool:
        if value is None and nullable:
            return True
        if not isinstance(value, str) or not value.startswith("/"):
            error("source_pointer", filename, path, "The source must be a resolvable absolute JSON Pointer")
            return False
        try:
            at(profile, value)
        except TagError as exc:
            error("source_pointer", filename, path, str(exc))
            return False
        match = re.match(r"^/views/(0|[1-9][0-9]*)(?:/|$)", value)
        if match and ids is not None:
            owner_row = views[int(match.group(1))]
            owner = owner_row.get("view_id") if isinstance(owner_row, dict) else None
            if owner not in ids or (not merged and any(vid != owner for vid in ids)):
                error("pointer_view_scope", filename, path, f"The source belongs to {owner} and does not match the bound view")
        return True

    def sources(row: dict, filename: str, path: str, ids: list,
                *, merged: bool = False) -> list[str]:
        values = row.get("source_pointers", [])
        if not isinstance(values, list):
            error("source_pointers", filename, path + "/source_pointers", "source_pointers must be a list")
            values = []
        good = []
        if "source_pointer" in row:
            values = values + [row["source_pointer"]]
        for i, value in enumerate(values):
            if pointer(value, filename, path + f"/source_pointers/{i}", ids, merged=merged):
                good.append(value)
        return good

    def binding(row: dict, filename: str, path: str, ids: list,
                source_values: list[str]) -> None:
        op_ref = row.get("operation_ref")
        if op_ref is None or row.get("valid") is False:
            return
        if not isinstance(op_ref, str):
            error("operation_ref", filename, path, "operation_ref must be a declared stable operation ID")
            return
        for vid in ids:
            found = [op for op in operations.get(vid, []) if op.get("operation_ref") == op_ref]
            if len(found) != 1 or not found[0].get("valid"):
                error("operation_ref", filename, path, f"{op_ref} is not a uniquely identified valid native operation of {vid}")
                continue
            op = found[0]
            if row.get("object_ref") is not None and row["object_ref"] != op.get("object_ref"):
                error("operation_object", filename, path, "object_ref does not match the native operation target")
            for source in source_values:
                op_pointer = op["source_pointer"]
                if source == op_pointer or source.startswith(op_pointer + "/"):
                    continue
                probe, explicit = source, None
                while probe:
                    try:
                        value = at(profile, probe)
                    except TagError:
                        break
                    if isinstance(value, dict) and "operation_ref" in value:
                        explicit = value["operation_ref"]
                        break
                    probe = probe.rsplit("/", 1)[0]
                if explicit != op_ref:
                    error("operation_source", filename, path, f"Source {source} does not belong to operation {op_ref} and has no explicit statement binding")

    def concept(row: dict, filename: str, path: str, *, human: bool = False) -> None:
        cid = row.get("concept_id", row.get("id"))
        if not isinstance(cid, str) or not TAG_PATTERN.fullmatch(cid) or row.get("axis") != cid.split(":")[0]:
            error("concept_id", filename, path, "concept_id does not match axis or has an invalid format")
            return
        index = human_vocab if human else vocab
        controlled = row.get("normalization_state", "controlled") != "proposed"
        if controlled and vocabulary is not None and cid not in index:
            error("unregistered_concept", filename, path, f"Controlled concept is not registered: {cid}")
        if human:
            parent = row.get("parent_id")
            definition = human_vocab.get(cid, {})
            declared = {p for key in ("parent_ids", "retrieval_parent_ids") for p in (definition.get(key, []) if isinstance(definition.get(key, []), list) else []) if isinstance(p, str)}
            if isinstance(definition.get("parent_id"), str):
                declared.add(definition["parent_id"])
            if parent is not None and parent not in declared:
                error("undeclared_parent", filename, path, f"Unregistered navigation parent edge: {cid} → {parent}")
        else:
            parents = row.get("retrieval_parent_ids", [])
            if not isinstance(parents, list) or any(not isinstance(p, str) for p in parents) or set(parents) - (expand_concepts({cid}, vocabulary) - {cid}):
                error("undeclared_parent", filename, path, f"{cid} contains an unregistered retrieval parent edge")

    for filename in ("identity.json", "classification.json", "human_tags.json", "machine_tags.json"):
        value = files.get(filename)
        if not isinstance(value, dict):
            error("sidecar_missing", filename, "", "Missing sidecar object")
            continue
        if value.get("setting_id") != profile.get("setting_id"):
            error("setting_id", filename, "/setting_id", "setting_id does not match the profile")
        if "view_ids" in value and value["view_ids"] != view_ids:
            error("view_coverage", filename, "/view_ids", "Sidecar view_ids do not match the profile")
        if filename in {"identity.json", "human_tags.json"} and isinstance(value.get("views"), list):
            declared = [r.get("view_id") for r in value["views"] if isinstance(r, dict)]
            if declared != view_ids:
                error("view_coverage", filename, "/views", "Sidecar views must preserve all stable IDs declared in the profile")

    identity = files.get("identity.json", {})
    if isinstance(identity, dict):
        axes = identity.get("axes", {})
        if not isinstance(axes, dict):
            error("identity_axes", "identity.json", "/axes", "identity axes must be an object")
            axes = {}
        for key, row in axes.items():
            if not isinstance(row, dict):
                error("identity_axis", "identity.json", "/axes/" + key, "An identity axis must be an object")
                continue
            nullable = row.get("state") == "unknown" and row.get("source_fields") is None
            p = row.get("source_pointer")
            valid = pointer(p, "identity.json", "/axes/" + key + "/source_pointer", nullable=nullable)
            if valid and p is not None and row.get("source_fields") != at(profile, p):
                error("identity_source_fields", "identity.json", "/axes/" + key, "source_fields does not match the profile source content")
        params = identity.get("parameters", {})
        if isinstance(params, dict):
            pointer(params.get("source_pointer"), "identity.json", "/parameters/source_pointer", nullable="parameters" not in profile)
        for i, row in enumerate(rows(identity.get("views", []), "identity.json", "/views")):
            if not isinstance(row, dict):
                error("identity_view", "identity.json", f"/views/{i}", "An identity view must be an object")
                continue
            vid = row.get("view_id")
            pointer(row.get("source_pointer"), "identity.json", f"/views/{i}/source_pointer", [vid])
            original = next((v for v in views if v.get("view_id") == vid), None)
            if original is None:
                error("unknown_view", "identity.json", f"/views/{i}", f"Unknown view ID: {vid}")
            else:
                for key, default in (("algorithms", None), ("guarantees", None), ("specification_overrides", {})):
                    if row.get(key, default) != original.get(key, default):
                        error("identity_view_fields", "identity.json", f"/views/{i}/{key}", "The identity view copy does not match the profile")

    machine = files.get("machine_tags.json", {})
    features = rows(machine.get("features", []), "machine_tags.json", "/features") if isinstance(machine, dict) else []
    feature_ids = {row.get("feature_id"): row for row in features if isinstance(row, dict) and isinstance(row.get("feature_id"), str)}
    seen_features: set[str] = set()
    for i, row in enumerate(features):
        path, filename = f"/features/{i}", "machine_tags.json"
        if not isinstance(row, dict):
            error("feature", filename, path, "feature must be an object")
            continue
        fid = row.get("feature_id")
        if not isinstance(fid, str) or not fid or fid in seen_features:
            error("feature_id", filename, path, "feature_id values must be nonempty, unique strings")
        if isinstance(fid, str):
            seen_features.add(fid)
        concept(row, filename, path)
        ids = scope(row, filename, path)
        sources(row, filename, path, ids)
        for j, item in enumerate(rows(row.get("bindings", []), filename, path + "/bindings")):
            if not isinstance(item, dict):
                error("binding", filename, path + f"/bindings/{j}", "binding must be an object")
                continue
            bids = scope(item, filename, path + f"/bindings/{j}", ids)
            source_values = sources(item, filename, path + f"/bindings/{j}", bids)
            binding(item, filename, path + f"/bindings/{j}", bids, source_values)
    if isinstance(machine, dict):
        for i, row in enumerate(rows(machine.get("tag_facts", []), "machine_tags.json", "/tag_facts")):
            if isinstance(row, dict):
                path = f"/tag_facts/{i}"
                ids = scope(row, "machine_tags.json", path)
                source_values = sources(row, "machine_tags.json", path, ids)
                binding(row, "machine_tags.json", path, ids, source_values)
            else:
                error("tag_fact", "machine_tags.json", f"/tag_facts/{i}", "tag_fact must be an object")

    classification = files.get("classification.json", {})
    if isinstance(classification, dict):
        for i, row in enumerate(rows(classification.get("tags", []), "classification.json", "/tags")):
            if not isinstance(row, dict):
                error("classification_tag", "classification.json", f"/tags/{i}", "tag must be an object")
                continue
            path, filename = f"/tags/{i}", "classification.json"
            # classification has no normalization_state: precise but proposed concepts remain legal.
            checked = dict(row, normalization_state="controlled" if row.get("id") in vocab else "proposed")
            concept(checked, filename, path)
            ids = scope(row, filename, path)
            source_values = sources(row, filename, path, ids)
            binding(row, filename, path, ids, source_values)
            for j, item in enumerate(rows(row.get("evidence", []), filename, path + "/evidence")):
                if isinstance(item, dict):
                    eids = scope(item, filename, path + f"/evidence/{j}", ids)
                    sources(item, filename, path + f"/evidence/{j}", eids)

    for filename, value in (("classification.json", classification), ("machine_tags.json", machine)):
        if isinstance(value, dict):
            seen_operations = {}
            for i, row in enumerate(rows(value.get("operation_bindings", []), filename, "/operation_bindings")):
                if not isinstance(row, dict):
                    error("operation_binding", filename, f"/operation_bindings/{i}", "An operation binding must be an object")
                    continue
                path = f"/operation_bindings/{i}"
                ids = scope(row, filename, path)
                source_values = sources(row, filename, path, ids)
                if "precision_pointer" in row:
                    pointer(row["precision_pointer"], filename, path + "/precision_pointer", ids)
                if "noise_pointer" in row:
                    pointer(row["noise_pointer"], filename, path + "/noise_pointer", ids)
                binding(row, filename, path, ids, source_values)
                for vid in ids:
                    op_id = row.get("operation_ref")
                    key = (vid, op_id) if isinstance(op_id, str) else None
                    if key is not None:
                        seen_operations[key] = seen_operations.get(key, 0) + 1
                    found = [op for op in operations.get(vid, []) if op.get("operation_ref") == op_id]
                    if len(found) != 1:
                        continue
                    expected = found[0]
                    for field in ("precision", "sampled", "role", "valid", "object_ref", "source_pointer", "precision_pointer"):
                        if row.get(field) != expected.get(field):
                            error("operation_projection", filename, path + "/" + field, f"{vid}/{op_id} {field} does not match the effective native operation")
                    contract = declared_feedback.get(vid, {}).get(op_id, {})
                    for field in ("precision", "noise"):
                        if field in contract:
                            if row.get(field) != contract[field]:
                                error("declared_feedback_coverage", filename, path + "/" + field, f"{vid}/{op_id} explicitly declares {field} in the source specification; projection must not omit or alter it")
                            if row.get(field + "_pointer") not in contract[field + "_pointers"]:
                                error("declared_feedback_source", filename, path + "/" + field + "_pointer", f"{vid}/{op_id} {field} must point to the actual declaration field")
            for vid, declared in operations.items():
                for op in declared:
                    if isinstance(op.get("operation_ref"), str) and seen_operations.get((vid, op["operation_ref"]), 0) != 1:
                        error("operation_binding_coverage", filename, "/operation_bindings", f"{vid}/{op['operation_ref']} must have exactly one operation binding")

    # Known native precision must also appear in machine facts; deleting both equally incorrect indices must not bypass validation.
    for vid, declared in operations.items():
        for op in declared:
            precision = declared_feedback.get(vid, {}).get(op.get("operation_ref"), {}).get("precision", op.get("precision"))
            if not op.get("valid") or op.get("role") in PUBLIC_ROLES or not isinstance(precision, str) or not re.fullmatch(r"[a-z0-9_]+", precision):
                continue
            found = False
            for feature in features:
                if not isinstance(feature, dict) or feature.get("concept_id") != "ORACLE:feedback_quality:" + precision or feature.get("status") != "known":
                    continue
                bindings = feature.get("bindings", [])
                for item in bindings if isinstance(bindings, list) else []:
                    if isinstance(item, dict) and item.get("operation_ref") == op.get("operation_ref") and isinstance(item.get("view_ids"), list) and vid in item["view_ids"]:
                        found = True
                        break
            if not found:
                error("precision_feature_coverage", "machine_tags.json", "/features", f"{vid}/{op.get('operation_ref')} has explicit precision {precision} but lacks a scoped machine feature")

    human = files.get("human_tags.json", {})
    from .indexes import retained_navigation, regime_index
    if not isinstance(identity, dict) or identity.get("regime_predicates") != regime_index(profile):
        error("regime_index", "identity.json", "/regime_predicates", "Regime IDs and predicate pointers must match the current profile exactly")
    retained = retained_navigation(baseline_files or {}, profile, machine, vocabulary)
    if isinstance(human, dict):
        for collection in ("facets", "details"):
            for i, row in enumerate(rows(human.get(collection, []), "human_tags.json", "/" + collection)):
                if not isinstance(row, dict):
                    error("human_concept", "human_tags.json", f"/{collection}/{i}", "A human concept must be an object")
                    continue
                path, filename = f"/{collection}/{i}", "human_tags.json"
                ids = scope(row, filename, path)
                source_values = sources(row, filename, path, ids, merged=True)
                if collection == "facets":
                    concept(row, filename, path, human=True)
                    if row.get("concept_id") in EXACT_CONCEPTS and any(vid not in exact_views for vid in ids):
                        error("human_exact_scope", filename, path, "Exact navigation requires all native feedback on unknown objects in this view to be exact and nonsampled")
                linked = []
                verified = [retained[(row.get("concept_id"), vid)] for vid in ids
                            if collection == "facets" and (row.get("concept_id"), vid) in retained]
                links = rows(row.get("source_feature_ids", []), filename, path + "/source_feature_ids")
                if not links and not verified:
                    error("source_feature", filename, path, "A human concept must reference a machine feature that supports it")
                for fid in links:
                    if not isinstance(fid, str) or fid not in feature_ids:
                        error("source_feature", filename, path, f"Unknown source_feature_id: {fid}")
                    else:
                        linked.append(feature_ids[fid])
                if linked:
                    allowed_views = {v for f in linked for v in f.get("view_ids", [])}
                    allowed_pointers = {p for f in linked for p in f.get("source_pointers", [])}
                    allowed_pointers.update(p for item in verified for p in item["source_pointers"])
                    if set(ids) - allowed_views or set(source_values) - allowed_pointers:
                        error("human_feature_binding", filename, path, "The human source or view exceeds the scope of the referenced feature")
                    for feature in linked:
                        original = feature.get("concept_id")
                        if collection == "details":
                            if row.get("machine_concept_id") != original:
                                error("human_feature_concept", filename, path, "The detail machine concept does not match the referenced feature")
                        else:
                            if not isinstance(original, str) or not TAG_PATTERN.fullmatch(original):
                                continue
                            mapped, _, _ = human_concept(original, vocabulary)
                            if row.get("concept_id") != mapped and not any(feature.get("feature_id") in v["source_feature_ids"] for v in verified):
                                error("human_feature_concept", filename, path, "The facet is not a registered navigation mapping of the source feature")
                            if row.get("concept_id") in EXACT_CONCEPTS:
                                for item in feature.get("bindings", []):
                                    if item.get("operation_ref") is not None:
                                        for vid in set(ids) & set(item.get("view_ids", [])):
                                            source_ops = [op for op in operations.get(vid, []) if op.get("operation_ref") == item["operation_ref"]]
                                            if source_ops and source_ops[0].get("role") in PUBLIC_ROLES:
                                                error("human_exact_scope", filename, path, "The precision of a public auxiliary operation cannot support Exact navigation for an unknown object")
        for i, row in enumerate(rows(human.get("views", []), "human_tags.json", "/views")):
            if isinstance(row, dict):
                scope(row, "human_tags.json", f"/views/{i}")
                if row.get("view_id") not in view_ids:
                    error("unknown_view", "human_tags.json", f"/views/{i}", f"Unknown view ID: {row.get('view_id')}")
                facets = {f.get("concept_id"): f for f in rows(human.get("facets", []), "human_tags.json", "/facets") if isinstance(f, dict) and isinstance(f.get("concept_id"), str)}
                for cid in rows(row.get("facet_ids", []), "human_tags.json", f"/views/{i}/facet_ids"):
                    if not isinstance(cid, str) or cid not in facets or row.get("view_id") not in facets[cid].get("view_ids", []):
                        error("view_facet", "human_tags.json", f"/views/{i}", f"Facet {cid} does not belong to this view")
        exact_cid = human_concept("ORACLE:feedback_quality:exact", vocabulary)[0]
        for vid in exact_views:
            exact_facets = [f for f in human.get("facets", []) if isinstance(f, dict) and f.get("concept_id") == exact_cid and f.get("status") == "known" and vid in f.get("view_ids", [])] if isinstance(human.get("facets"), list) else []
            if not exact_facets:
                error("human_exact_coverage", "human_tags.json", "/facets", f"The complete native interface of {vid} is explicitly Exact but lacks {exact_cid} navigation")
            for index, view in enumerate(human.get("views", []) if isinstance(human.get("views"), list) else []):
                if isinstance(view, dict) and view.get("view_id") == vid and exact_cid not in (view.get("facet_ids") if isinstance(view.get("facet_ids"), list) else []):
                    error("human_exact_coverage", "human_tags.json", f"/views/{index}/facet_ids", f"Exact navigation for {vid} is not listed in the view")
        human_facets = rows(human.get("facets", []), "human_tags.json", "/facets")
        nav = {vid: sorted(f["concept_id"] for f in human_facets if isinstance(f, dict)
                           and isinstance(f.get("concept_id"), str) and f.get("status") == "known" and isinstance(f.get("view_ids"), list) and vid in f["view_ids"]) for vid in view_ids if isinstance(vid, str)}
        for row in rows(human.get("views", []), "human_tags.json", "/views"):
            if isinstance(row, dict) and {c for c in rows(row.get("facet_ids", []), "human_tags.json", "/views/facet_ids") if isinstance(c, str)} != set(nav.get(row.get("view_id"), [])):
                error("view_facet_coverage", "human_tags.json", "/views", "Each view must list all its current human navigation concepts")
        for (cid, vid), support in retained.items():
            entries = [f for f in human_facets if isinstance(f, dict) and f.get("concept_id") == cid and vid in f.get("view_ids", [])]
            if not entries or not any(support["source_pointers"] <= set(f.get("source_pointers", []))
                    and support["source_feature_ids"] <= set(f.get("source_feature_ids", []))
                    and any(e.get("view_id") == vid and all(a in e.get("assertions", []) for a in support["assertions"])
                            for e in f.get("evidence", [])) for f in entries):
                error("lost_source_navigation", "human_tags.json", "/facets", f"Source-bound navigation {cid} was lost in {vid}")
        if not isinstance(machine, dict) or machine.get("navigation_by_view") != nav:
            error("machine_navigation", "machine_tags.json", "/navigation_by_view", "Machine navigation must retain current human concepts in the same view")
        expected = expand_concepts({f["concept_id"] for f in features if isinstance(f, dict) and isinstance(f.get("concept_id"), str) and f.get("status") == "known"}, vocabulary)
        expected.update(cid for ids in nav.values() for cid in ids)
        if not isinstance(machine, dict) or machine.get("retrieval_concept_ids") != sorted(expected):
            error("machine_retrieval", "machine_tags.json", "/retrieval_concept_ids", "The retrieval index must contain the current precise concepts, their declared parents and source-bound navigation concepts")
    known = {axis: {r.get("concept_id") for r in features if isinstance(r, dict) and r.get("axis") == axis and r.get("status") == "known" and isinstance(r.get("concept_id"), str)} for axis in AXES}
    if isinstance(classification, dict) and isinstance(classification.get("axes"), dict):
        for axis in AXES:
            actual = classification["axes"].get(axis)
            if not isinstance(actual, list) or any(not isinstance(c, str) for c in actual) or set(actual) != known[axis]:
                error("axis_coverage", "classification.json", "/axes/" + axis, "The classification axis does not match the explicitly known machine facts")
    if isinstance(machine, dict) and isinstance(machine.get("axis_coverage"), dict):
        for axis in AXES:
            row = machine["axis_coverage"].get(axis)
            if not isinstance(row, dict):
                error("axis_coverage", "machine_tags.json", "/axis_coverage/" + axis, "Missing classification coverage object")
                continue
            actual = row.get("concept_ids")
            if not isinstance(actual, list) or any(not isinstance(c, str) for c in actual) or set(actual) != known[axis] or row.get("state") != ("classified" if known[axis] else "unknown"):
                error("axis_coverage", "machine_tags.json", "/axis_coverage/" + axis, "Coverage status does not match explicitly known facts")
    return errors
