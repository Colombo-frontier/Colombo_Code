"""Read-only discovery and pagination of target Atlas schemas, with purely mechanical metadata adaptation.

Adapt only version and traceable source metadata here; do not modify specifications, views, bounds, or mathematical conditions.
Locally declared schema URIs may serve as aliases; unknown references never trigger network access.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urljoin

from .tags import TagError, at, canonical_bytes


SOURCE_FIELDS = ("source_schema_version", "source_snapshot", "source_profile", "source_json_sha256", "source_order")
ADAPTER_KEY = "oracle_atlas_target_adapter"


class TargetSchemaError(ValueError):
    """A target-file or schema-path error does not imply an incorrect scientific conclusion."""


def _data_root(root: str | Path) -> Path:
    root = Path(root).expanduser().resolve()
    if not (root / "schemas").is_dir() and (root / "data" / "schemas").is_dir():
        root = root / "data"
    return root


def _schema_paths(data_root: str | Path) -> list[Path]:
    directory = _schema_directory(data_root)
    if not directory.exists():
        return []
    root = directory.resolve()
    paths = []
    for path in sorted(directory.rglob("*.json")):
        if not path.resolve().is_relative_to(root):
            raise TargetSchemaError("A target schema path cannot escape the schemas directory")
        if path.is_file():
            paths.append(path)
    return paths


def _schema_directory(data_root: str | Path) -> Path:
    root = _data_root(data_root)
    directory = root / "schemas"
    if not directory.resolve().is_relative_to(root):
        raise TargetSchemaError("The target schemas directory cannot link outside the Atlas data directory")
    return directory


def _schema_name(name: str) -> str:
    if not isinstance(name, str):
        raise TargetSchemaError("schema name must be a string")
    if name.startswith("atlas-schema:"):
        name = name[len("atlas-schema:"):]
    if name in {"profile", "identity", "classification", "human_tags", "machine_tags"}:
        name += ".schema.json"
    elif name in {"profile.json", "identity.json", "classification.json", "human_tags.json", "machine_tags.json"}:
        name = name[:-5] + ".schema.json"
    path = PurePosixPath(name)
    if not name or "\\" in name or path.is_absolute() or any(part in {".", ".."} for part in path.parts) or not name.endswith(".json"):
        raise TargetSchemaError("JSON schemas within schemas may be read only by relative name")
    return path.as_posix()


def _read(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise TargetSchemaError(f"Unable to read target schema: {path.name}: {exc}") from exc
    if not isinstance(data, dict):
        raise TargetSchemaError(f"The target schema top level must be an object: {path.name}")
    return data


def _select(data_root: str | Path, name: str) -> Path:
    name = _schema_name(name)
    directory = _schema_directory(data_root)
    path = directory / name
    if not path.resolve().is_relative_to(directory.resolve()):
        raise TargetSchemaError("A target schema path cannot escape the schemas directory")
    if not path.is_file():
        raise TargetSchemaError(f"The target Atlas does not contain schema: {name}")
    return path


def _summary(data: dict) -> dict:
    required = data.get("required", [])
    properties = data.get("properties", {})
    if not isinstance(properties, dict):
        properties = {}
    version = properties.get("schema_version", {})
    provenance = properties.get("provenance", {})
    return {
        "required": required[:80] if isinstance(required, list) else [],
        "required_count": len(required) if isinstance(required, list) else 0,
        "schema_version": {k: deepcopy(version[k]) for k in ("type", "const", "enum") if isinstance(version, dict) and k in version},
        "provenance_required": list(provenance.get("required", []))[:80] if isinstance(provenance, dict) else [],
        "summary_only": True,
    }


def schema_manifest(data_root: str | Path, offset: int = 0, limit: int = 20) -> dict:
    """Return a bounded catalog; read complete constraints through schema_ref pagination."""
    if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0 or isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise TargetSchemaError("offset/limit out of range")
    paths = _schema_paths(data_root)
    directory = _schema_directory(data_root)
    limit = min(limit, 30)
    items = []
    profile_contract = None
    for path in paths:
        name = path.relative_to(directory).as_posix()
        if name == "profile.schema.json":
            data = _read(path)
            profile_contract = {"schema_ref": "atlas-schema:" + name, **_summary(data)}
    for path in paths[offset:offset + limit]:
        data = _read(path)
        name = path.relative_to(directory).as_posix()
        raw = path.read_bytes()
        items.append({"name": name, "schema_ref": "atlas-schema:" + name, "schema_id": data.get("$id"),
                      "schema_sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), **_summary(data)})
    return {"target_schema_available": bool(paths), "items": items, "total": len(paths),
            "next_offset": offset + limit if offset + limit < len(paths) else None,
            "profile_contract": profile_contract,
            "adaptation_policy": "Mechanically adapt only the target schema_version and traceable source metadata; mathematical specifications, views, bounds, and conditions remain unchanged."}


def read_target_schema(data_root: str | Path, name: str, pointer: str = "", offset: int = 0, limit: int = 10000) -> dict:
    """Read local schemas only; return the same data/text pagination shape as artifact_get."""
    from ..core.store import bounded
    path = _select(data_root, name)
    data = _read(path)
    try:
        selected = at(data, pointer)
    except TagError as exc:
        raise TargetSchemaError(str(exc)) from exc
    if isinstance(offset, bool) or isinstance(limit, bool):
        raise TargetSchemaError("offset/limit out of range")
    relative = path.relative_to(_data_root(data_root) / "schemas").as_posix()
    return {"name": relative, "schema_ref": "atlas-schema:" + relative, "schema_id": data.get("$id"),
            "schema_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "pointer": pointer,
            **bounded(selected, offset, min(limit, 24000))}


def _next_source_order(data_root: str | Path) -> int | float:
    root = _data_root(data_root)
    orders = []
    for path in sorted((root / "settings").glob("*/profile.json")):
        if not path.resolve().is_relative_to(root):
            raise TargetSchemaError("An existing profile path cannot escape the Atlas data directory")
        try:
            provenance = json.loads(path.read_text(encoding="utf-8")).get("provenance", {})
        except (OSError, ValueError, AttributeError) as exc:
            raise TargetSchemaError(f"Unable to determine new entry order: {path.parent.name}: {exc}") from exc
        value = provenance.get("source_order") if isinstance(provenance, dict) else None
        if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
            orders.append(value)
    return max(orders, default=0) + 1


def adapt_profile(profile: dict, data_root: str | Path, previous: dict | None = None,
                  source_ref: str | None = None, inventory_version: str | None = None) -> dict:
    """Adapt format metadata only; repeated adaptation does not modify generated source records or frozen hashes."""
    if not isinstance(profile, dict):
        raise TargetSchemaError("profile must be an object")
    result = deepcopy(profile)
    path = _data_root(data_root) / "schemas" / "profile.schema.json"
    if not path.exists():
        return {"profile": result, "changes": []}
    schema = _read(_select(data_root, "profile"))
    properties = schema.get("properties", {})
    properties = properties if isinstance(properties, dict) else {}
    version_rule = properties.get("schema_version", {})
    provenance_rule = properties.get("provenance", {})
    required = provenance_rule.get("required", []) if isinstance(provenance_rule, dict) else []
    changes = []
    input_hash = hashlib.sha256(canonical_bytes(profile)).hexdigest()
    input_version = profile.get("schema_version")

    def set_value(obj: dict, key: str, value: Any, pointer: str, reason: str) -> None:
        if key not in obj or obj[key] != value:
            entry = {"path": pointer, "value": deepcopy(value), "reason": reason}
            if key in obj:
                entry["previous"] = deepcopy(obj[key])
            obj[key] = deepcopy(value)
            changes.append(entry)

    if isinstance(version_rule, dict) and "const" in version_rule:
        set_value(result, "schema_version", version_rule["const"], "/schema_version", "target_schema_const")
    needs_provenance = ("provenance" in result or any(k in required for k in SOURCE_FIELDS)
                        or isinstance((previous or {}).get("provenance"), dict))
    if needs_provenance and isinstance(result.get("provenance", {}), dict):
        provenance = result.setdefault("provenance", {})
        old_provenance = (previous or {}).get("provenance", {})
        if isinstance(old_provenance, dict):
            for key, value in old_provenance.items():
                if key not in provenance and key not in SOURCE_FIELDS:
                    set_value(provenance, key, value, "/provenance/" + key.replace("~", "~0").replace("/", "~1"), "preserve_existing_provenance_extension")
            for key in SOURCE_FIELDS:
                if key in old_provenance:
                    set_value(provenance, key, old_provenance[key], "/provenance/" + key, "preserve_existing_source_lineage")
        generated = {
            "source_schema_version": input_version,
            "source_snapshot": inventory_version or "oracle-atlas-draft-sha256:" + input_hash,
            "source_profile": source_ref or "urn:oracle-atlas:input-profile:sha256:" + input_hash,
            "source_json_sha256": input_hash,
        }
        for key in SOURCE_FIELDS:
            if key in required and key not in provenance:
                value = _next_source_order(data_root) if key == "source_order" else generated[key]
                set_value(provenance, key, value, "/provenance/" + key, "traceable_input_metadata")
        if changes and ADAPTER_KEY not in provenance:
            provenance[ADAPTER_KEY] = {"kind": "mechanical_target_schema_adaptation", "input_schema_version": input_version,
                                       "input_json_sha256": input_hash, "source_ref": source_ref,
                                       "inventory_version": inventory_version, "scientific_fields_unchanged": True}
    return {"profile": result, "changes": changes}


def adapt_sidecar_schema_identifiers(files: dict, data_root: str | Path) -> list[dict]:
    """Read target interface identifiers instead of embedding release numbers."""
    changes = []
    for name in ("identity.json", "classification.json", "human_tags.json", "machine_tags.json"):
        path = _data_root(data_root) / "schemas" / _schema_name(name)
        if name not in files or not path.exists():
            continue
        definition = _read(_select(data_root, name))
        rule = definition.get("properties", {}).get("schema_version", {})
        if isinstance(rule, dict) and "const" in rule and files[name].get("schema_version") != rule["const"]:
            changes.append({"file": name, "path": "/schema_version", "previous": files[name].get("schema_version"),
                            "value": deepcopy(rule["const"]), "reason": "target_schema_const"})
            files[name]["schema_version"] = deepcopy(rule["const"])
    return changes


def _pointer(tokens) -> str:
    return "".join("/" + str(t).replace("~", "~0").replace("/", "~1") for t in tokens)


def _diagnostic(code: str, message: str, *, filename: str | None = None, path: str = "", schema_path: str = "") -> dict:
    return {"code": code, "file": filename, "path": path, "schema_path": schema_path, "message": message}


def _references(schema: Any, pointer: str = "", base_uri: str = ""):
    if isinstance(schema, dict):
        if isinstance(schema.get("$id"), str):
            base_uri = urljoin(base_uri, schema["$id"])
        for key, value in schema.items():
            child = pointer + "/" + str(key).replace("~", "~0").replace("/", "~1")
            if key in {"$ref", "$dynamicRef"} and isinstance(value, str):
                yield child, value, base_uri
            else:
                yield from _references(value, child, base_uri)
    elif isinstance(schema, list):
        for index, value in enumerate(schema):
            yield from _references(value, pointer + f"/{index}", base_uri)


def validate_target_files(files: dict, data_root: str | Path) -> list[dict]:
    """Aggregate all target schema errors; report unknown local/remote references without downloading them."""
    import jsonschema
    from referencing.exceptions import Unresolvable
    from .store import _local_schema_registry
    if not isinstance(files, dict):
        return [_diagnostic("target_files_type", "files must be an object")]
    try:
        paths = _schema_paths(data_root)
        if not paths:
            return []
        registry, schemas = _local_schema_registry(_data_root(data_root) / "schemas")
    except (ValueError, OSError) as exc:
        return [_diagnostic("target_schema_resource", str(exc))]
    errors = []
    invalid_schema_uris = set()
    for uri, definition in schemas.items():
        try:
            jsonschema.Draft202012Validator.check_schema(definition)
        except jsonschema.SchemaError as exc:
            invalid_schema_uris.add(uri)
            errors.append(_diagnostic("target_schema_invalid", exc.message, filename=Path(uri).name, schema_path=_pointer(exc.absolute_schema_path)))
        for pointer, ref, base_uri in _references(definition, base_uri=uri):
            try:
                registry.resolver(base_uri=base_uri).lookup(ref)
            except (Unresolvable, ValueError) as exc:
                invalid_schema_uris.add(uri)
                errors.append(_diagnostic("target_schema_unresolved_ref", f"The schema reference cannot be resolved locally; no network retrieval was performed: {ref}: {exc}",
                                          filename=Path(uri).name, schema_path=pointer))
    for filename, value in sorted(files.items(), key=lambda item: str(item[0])):
        try:
            path = _select(data_root, filename)
        except TargetSchemaError as exc:
            # Adapter structural checks remain responsible when the target does not provide a sidecar schema.
            if isinstance(filename, str) and filename in {"profile.json", "identity.json", "classification.json", "human_tags.json", "machine_tags.json"} and not (_data_root(data_root) / "schemas" / _schema_name(filename)).exists():
                continue
            errors.append(_diagnostic("target_schema_resource", str(exc), filename=str(filename)))
            continue
        uri = path.resolve().as_uri()
        if uri in invalid_schema_uris:
            continue
        try:
            for error in jsonschema.Draft202012Validator(schemas[uri], registry=registry).iter_errors(value):
                errors.append(_diagnostic("target_schema_" + str(error.validator), error.message, filename=str(filename),
                                          path=_pointer(error.absolute_path), schema_path=_pointer(error.absolute_schema_path)))
        except (Unresolvable, ValueError) as exc:
            errors.append(_diagnostic("target_schema_unresolved_ref", f"The schema reference cannot be resolved locally; no network retrieval was performed: {exc}", filename=str(filename)))
    return errors


def validate_profile_target(profile: dict, data_root: str | Path) -> list[dict]:
    return validate_target_files({"profile.json": profile}, data_root)
