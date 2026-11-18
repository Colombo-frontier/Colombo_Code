"""Stable ID and tag-source bindings in the final specification.

Repair only ID/Pointer forms uniquely determined by the same frozen specification; do not infer scientific equivalence,
construct native operations from natural language, or migrate legacy profile content on behalf of researchers.
"""
from __future__ import annotations

from copy import deepcopy
import re
from typing import Any

from .tags import TagError, at, effective_native_operations, project_tags


_VIEW_POINTER = re.compile(r"^/views/(0|[1-9][0-9]*)$")
_OP_POINTER = re.compile(
    r"^(?P<base>/(?:common_specification/oracle/|views/(?:0|[1-9][0-9]*)/specification_overrides/oracle/)?operations)/(?P<key>[^/]+)(?P<suffix>/.*)?$"
)


def _declared_id(value: Any, keys: tuple[str, ...]) -> str | None:
    if not isinstance(value, dict):
        return None
    values = [value[k] for k in keys if k in value]
    if not values or any(not isinstance(x, str) or not x for x in values):
        return None
    return values[0] if all(x == values[0] for x in values) else None


def _position(token: str, size: int) -> int | None:
    # Check bounds by length first to avoid uncontrolled long integer strings triggering Python's int conversion limit.
    if not re.fullmatch(r"0|[1-9][0-9]*", token) or len(token) > len(str(max(size - 1, 0))):
        return None
    index = int(token)
    return index if index < size else None


def normalize_tag_facts(profile: dict, facts: list) -> dict:
    """Return ``{facts, changes, errors}`` without modifying caller input.

    The canonical form for ``view_ref`` and ``operation_ref`` is the declared ID.
    When the entity is unique and its scope explicit, a mistakenly supplied Pointer may be replaced with that ID, recording the change.
    ``source_pointer`` always refers to the final profile; only explicit path aliases for the same native operation
    are supported. Statements are not moved across field layouts, and sources are not inferred from tag meaning.

    All diagnostics are JSON-serializable ``path/code/message`` objects. Results with errors
    cannot be ingested. Unknown facts may remain unknown; when a native operation is missing, use
    operation_ref=null rather than having the program invent permissions or precision from prose.
    """
    errors: list[dict] = []
    changes: list[dict] = []

    def error(path: str, code: str, message: str, details: dict | None = None) -> None:
        item = {"path": path, "code": code, "message": message, **(details or {})}
        if item not in errors:
            errors.append(item)

    if not isinstance(facts, list):
        error("/tag_facts", "invalid_type", "tag_facts must be a list")
        return {"facts": [], "changes": changes, "errors": errors}
    result = deepcopy(facts)
    if not isinstance(profile, dict):
        error("", "invalid_type", "The final profile must be an object")
        return {"facts": result, "changes": changes, "errors": errors}

    views = profile.get("views", [])
    if not isinstance(views, list):
        views = []
    view_ids = [v.get("view_id") if isinstance(v, dict) else None for v in views]
    valid_views = bool(view_ids) and all(isinstance(v, str) and v for v in view_ids) and len(set(view_ids)) == len(view_ids)
    if not valid_views:
        error("/views", "invalid_view_ids", "views must declare nonempty unique view_id values")

    native: dict[str, dict] = {}
    if valid_views:
        native = {vid: effective_native_operations(profile, vid) for vid in view_ids}

    def changed(index: int, fact: dict, key: str, value: str, reason: str) -> None:
        old = fact.get(key)
        if old != value:
            fact[key] = value
            changes.append({"path": f"/tag_facts/{index}/{key}", "from": old, "to": value, "reason": reason})

    def resolve_operation(raw: str, scope: list[str]) -> tuple[list[dict], str | None, str | None, dict | None]:
        """Require all applicable views to resolve to the same explicit operation; do not borrow permissions from one view."""
        declared_matches = [[op for op in native[vid]["operations"] if op.get("operation_ref") == raw]
                            for vid in scope]
        if declared_matches and all(len(rows) == 1 and rows[0].get("valid") for rows in declared_matches):
            return [rows[0] for rows in declared_matches], None, None, None
        match = _OP_POINTER.fullmatch(raw)
        pointer_form = raw.startswith("/")
        declaration = None
        if pointer_form:
            if match is None or match.group("suffix"):
                return [], "invalid_operation_pointer", "An operation_ref Pointer must refer to a complete native operation", None
            try:
                declaration = at(profile, raw)
            except TagError:
                pass
        found = []
        for vid in scope:
            info = native[vid]
            operations = info["operations"]
            if not operations:
                return [], "operation_scope_missing", f"{vid} does not declare canonical oracle.operations; native interfaces cannot be invented from prose or top-level operations", None
            candidates = [op for op in operations if op.get("operation_ref") == raw] if not pointer_form else []
            if not pointer_form and not candidates:
                # The normalizer may already have set operation_ref=null for rows with conflicting ID aliases.
                # Still recognize actual string IDs in native declarations to report structural errors rather than falsely reporting absence.
                for op in operations:
                    try:
                        source = at(profile, op.get("source_pointer", ""))
                    except TagError:
                        continue
                    if isinstance(source, dict) and any(source.get(key) == raw for key in ("id", "operation_id", "operation_ref")):
                        candidates.append(op)
            if pointer_form:
                # Effective sources take precedence; a common interface replaced by a view override must not be reused.
                candidates = [op for op in operations if op.get("source_pointer") == raw]
                if not candidates and match.group("base") == "/operations":
                    declared = _declared_id(declaration, ("id", "operation_id", "operation_ref"))
                    if declaration is not None:
                        if declared:
                            candidates = [op for op in operations if op.get("operation_ref") == declared]
                    elif re.fullmatch(r"0|[1-9][0-9]*", match.group("key")):
                        index = _position(match.group("key"), len(operations))
                        candidates = operations[index:index + 1] if index is not None else []
                    else:
                        candidates = [op for op in operations if op.get("operation_ref") == match.group("key")]
                elif not candidates and declaration is None and match.group("base") != "/operations":
                    # An ID was mistakenly used as an array index; repair only if both the source array and ID match exactly.
                    candidates = [op for op in operations
                                  if op.get("operation_ref") == match.group("key")
                                  and op.get("source_pointer", "").rsplit("/", 1)[0] == match.group("base")]
            if not candidates:
                return [], "unknown_operation", f"{raw!r} is not declared as a native operation ID/source in the effective scope of {vid}", None
            if len(candidates) != 1 or not candidates[0].get("valid"):
                diagnostics = [item for op in candidates for item in op.get("native_diagnostics", [])]
                if not diagnostics:
                    diagnostics = [{"code": "invalid_native_declaration", "path": op.get("source_pointer"), "message": message}
                                   for op in candidates for message in info.get("diagnostics", [])]
                pointers = sorted({op.get("source_pointer") for op in candidates if isinstance(op.get("source_pointer"), str)})
                detail = {"view_ref": vid, "operation_ref": raw,
                          "source_pointer": pointers[0] if len(pointers) == 1 else None,
                          "operation_source_pointers": pointers, "native_diagnostics": diagnostics}
                message = f"{raw!r} is declared in {vid}, but the native operation structure is invalid or its ID is not unique; repair the following native fields rather than changing only the ID."
                return [], "invalid_native_operation", message, detail
            operation = candidates[0]
            if isinstance(declaration, dict) and match.group("base") == "/operations":
                for keys, actual in [(("object_ref", "object_id", "target_object"), operation.get("object_ref")),
                                     (("operation_code", "code"), operation.get("operation_code"))]:
                    declared = _declared_id(declaration, keys)
                    if declared is not None and actual is not None and declared != actual:
                        return [], "conflicting_operation_declaration", "The top-level operation declaration conflicts with structural fields of the effective native operation", None
            found.append(operation)
        if pointer_form and len({(op.get("operation_ref"), op.get("source_pointer"), op.get("object_ref")) for op in found}) != 1:
            return [], "ambiguous_operation_pointer", f"{raw!r} resolves to different operations across views; specify view_ref explicitly", None
        return found, None, None, None

    # project_tags uses setting_id only to generate projection identifiers; a candidate can undergo the same binding validation before identity assignment.
    validation_profile = deepcopy(profile)
    if not isinstance(validation_profile.get("setting_id"), str) or not validation_profile.get("setting_id"):
        validation_profile["setting_id"] = "binding_validation_only"

    validation_indices = []

    for index, fact in enumerate(result):
        start_errors = len(errors)
        prefix = f"/tag_facts/{index}"
        if not isinstance(fact, dict):
            error(prefix, "invalid_type", "Each tag_facts item must be an object")
            continue
        view = fact.get("view_ref")
        if view is not None and view not in view_ids:
            match = _VIEW_POINTER.fullmatch(view) if isinstance(view, str) else None
            if match:
                position = _position(match.group(1), len(views))
                if position is not None and valid_views:
                    changed(index, fact, "view_ref", view_ids[position], "The Pointer uniquely refers to a declared view_id")
                    view = fact["view_ref"]
                else:
                    error(prefix + "/view_ref", "unknown_view", f"The view Pointer is absent or its declaration is not unique: {view!r}")
            else:
                error(prefix + "/view_ref", "unknown_view", f"view_ref must be a declared view_id: {view!r}")

        operations: list[dict] = []
        raw = fact.get("operation_ref")
        if raw is not None:
            if not isinstance(raw, str) or not raw:
                error(prefix + "/operation_ref", "invalid_type", "operation_ref must be a nonempty ID or null")
            elif valid_views and (view is None or view in view_ids):
                operations, code, message, detail = resolve_operation(raw, [view] if view is not None else view_ids)
                if code:
                    error(prefix + "/operation_ref", code, message, detail)
                elif raw.startswith("/"):
                    changed(index, fact, "operation_ref", operations[0]["operation_ref"], "The Pointer uniquely corresponds to a native operation ID in the applicable view")
                # Repair an object Pointer only when the same operation explicitly specifies the target object; retain existing valid bindings.
                obj = fact.get("object_ref")
                targets = {op.get("object_ref") for op in operations}
                if operations and isinstance(obj, str) and obj.startswith("/") and targets != {obj}:
                    try:
                        declared_obj = _declared_id(at(profile, obj), ("id", "object_id", "object_ref"))
                    except TagError:
                        declared_obj = None
                    if declared_obj is not None and targets == {declared_obj}:
                        declared_objects = [o for o in profile.get("objects", []) if isinstance(o, dict)
                                            and _declared_id(o, ("id", "object_id", "object_ref")) == declared_obj]
                        if len(declared_objects) > 1:
                            error(prefix + "/object_ref", "ambiguous_object_id", "The object ID is duplicated; the Pointer cannot be collapsed into a nonunique ID")
                        else:
                            changed(index, fact, "object_ref", declared_obj, "The object Pointer matches the explicit target ID of the same operation")

        pointer = fact.get("source_pointer")
        if isinstance(pointer, str) and operations:
            alias = _OP_POINTER.fullmatch(pointer)
            if alias:
                stem = alias.group("base") + "/" + alias.group("key")
                mapped, code, _, _ = resolve_operation(stem, [view] if view is not None else view_ids)
                if code is None and {op.get("operation_ref") for op in mapped} == {fact.get("operation_ref")}:
                    pointers = {op["source_pointer"] + (alias.group("suffix") or "") for op in mapped}
                    if len(pointers) == 1:
                        target = next(iter(pointers))
                        try:
                            at(profile, target)
                        except TagError:
                            pass
                        else:
                            changed(index, fact, "source_pointer", target, "An explicit source path for the same native operation")
                            pointer = target
        try:
            if not isinstance(pointer, str) or not pointer.startswith("/"):
                raise TagError("source_pointer must be a JSON Pointer within the final profile")
            at(profile, pointer)
        except TagError as exc:
            error(prefix + "/source_pointer", "unresolved_source_pointer", str(exc))
        if valid_views and len(errors) == start_errors:
            validation_indices.append(index)

    # Project once on the normal path to avoid recomputing the full profile hash and four sidecars for every fact.
    # Locate individual failures only on error, while still returning all fact diagnostics together.
    if valid_views:
        try:
            project_tags(validation_profile, [result[i] for i in validation_indices])
        except (TagError, KeyError, IndexError, TypeError, ValueError) as exc:
            if not validation_indices:
                error("", "profile_binding_invalid", str(exc))
            for index in validation_indices:
                try:
                    project_tags(validation_profile, [result[index]])
                except (TagError, KeyError, IndexError, TypeError, ValueError) as item_exc:
                    error(f"/tag_facts/{index}", "binding_invalid", str(item_exc))

    return {"facts": result, "changes": changes, "errors": errors}
