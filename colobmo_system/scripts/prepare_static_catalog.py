#!/usr/bin/env python3
"""Explicitly prepare a bounded-run Codex catalog; never launch a model.

The only executable invocation is native Codex ``--version``. The source cache
and an independently produced reference cache are read without reading auth
files. The exported catalog contains the complete, unchanged ``models`` array.
The separate manifest deliberately omits cache identity and ETag values.

This is an opt-in validation utility, not a change to normal dynamic discovery.
Static catalogs disable native freshness/identity/ETag revalidation during the
configured run. Generate a new validated snapshot for a new run.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
from typing import Any


MAX_CACHE_BYTES = 5 * 1024 * 1024
MAX_SOURCE_AGE_SECONDS = 300


class CatalogError(ValueError):
    """A diagnostic safe to print without exposing source values."""


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CatalogError("JSON contains a duplicate object key")
        result[key] = value
    return result


def _nonfinite(_value: str) -> None:
    raise CatalogError("JSON contains a non-finite number")


def _read_cache(home: Path, label: str) -> tuple[Path, dict[str, Any]]:
    path = home.resolve(strict=True) / "models_cache.json"
    if path.is_symlink() or not stat.S_ISREG(path.stat().st_mode):
        raise CatalogError(f"{label} cache must be an ordinary file")
    with path.open("rb") as handle:
        data = handle.read(MAX_CACHE_BYTES + 1)
    if len(data) > MAX_CACHE_BYTES:
        raise CatalogError(f"{label} cache exceeds the size limit")
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_object,
                           parse_constant=_nonfinite)
    except (UnicodeError, json.JSONDecodeError, RecursionError):
        raise CatalogError(f"{label} cache is not valid UTF-8 JSON") from None
    if not isinstance(value, dict):
        raise CatalogError(f"{label} cache must be a JSON object")
    return path, value


def _timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise CatalogError(f"{label} fetched_at must be a timestamp")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise CatalogError(f"{label} fetched_at is invalid") from None
    if result.tzinfo is None or result.utcoffset() is None:
        raise CatalogError(f"{label} fetched_at must include a timezone")
    return result.astimezone(timezone.utc)


def _models(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise CatalogError(f"{label} models must be a nonempty array")
    seen: set[str] = set()
    for model in value:
        if not isinstance(model, dict):
            raise CatalogError(f"{label} models must contain objects")
        slug = model.get("slug")
        if not isinstance(slug, str) or not slug.strip() or slug != slug.strip():
            raise CatalogError(f"{label} model slug must be a nonempty trimmed string")
        if slug in seen:
            raise CatalogError(f"{label} model slugs must be unique")
        seen.add(slug)
    return value


def validate_snapshot(source: dict[str, Any], reference: dict[str, Any], *,
                      client_version: str, requested_models: list[str],
                      effort: str, now: datetime) -> dict[str, Any]:
    """Validate provenance metadata; return only nonsecret inspection fields."""
    if now.tzinfo is None:
        raise CatalogError("Validation time must include a timezone")
    now = now.astimezone(timezone.utc)
    source_time = _timestamp(source.get("fetched_at"), "source")
    reference_time = _timestamp(reference.get("fetched_at"), "reference")
    source_age = (now - source_time).total_seconds()
    if source_age < 0 or reference_time > now:
        raise CatalogError("Source or reference fetched_at is in the future")
    if source_age > MAX_SOURCE_AGE_SECONDS:
        raise CatalogError("Source cache is older than 300 seconds; refresh it through Codex")
    for label, value in (("source", source), ("reference", reference)):
        if value.get("client_version") != client_version:
            raise CatalogError(f"{label} cache client_version does not match native Codex")
        identity = value.get("identity")
        if not isinstance(identity, str) or not identity.strip():
            raise CatalogError(f"{label} cache identity must be a nonempty string")
    if source["identity"] != reference["identity"]:
        raise CatalogError("Source and reference cache identities do not match")
    source_models = _models(source.get("models"), "source")
    reference_models = _models(reference.get("models"), "reference")
    if (not requested_models or any(not isinstance(name, str) or not name.strip()
                                    for name in requested_models)
            or len(set(requested_models)) != len(requested_models)):
        raise CatalogError("Requested models must be nonempty and unique")
    if not isinstance(effort, str) or not effort.strip():
        raise CatalogError("Requested effort must be nonempty")
    by_slug = {model["slug"]: model for model in source_models}
    for name in requested_models:
        if name not in by_slug:
            raise CatalogError("A requested model is absent from the source catalog")
        levels = by_slug[name].get("supported_reasoning_levels")
        if not isinstance(levels, list) or not levels:
            raise CatalogError("A requested model has no supported reasoning levels")
        supported: set[str] = set()
        for level in levels:
            if (not isinstance(level, dict) or not isinstance(level.get("effort"), str)
                    or not level["effort"].strip() or level["effort"] in supported):
                raise CatalogError("A requested model has invalid reasoning levels")
            supported.add(level["effort"])
        if effort not in supported:
            raise CatalogError("Requested effort is not supported by a requested model")
    # JSON text comparison preserves true/1 and integer/float distinctions;
    # it is not stored as a fingerprint or used as an execution identity.
    strict_equal = json.dumps(source_models, sort_keys=True, allow_nan=False) == json.dumps(
        reference_models, sort_keys=True, allow_nan=False)
    return {
        "source_fetched_at": source["fetched_at"],
        "reference_fetched_at": reference["fetched_at"],
        "source_age_seconds_at_validation": source_age,
        "client_version": client_version,
        "identity_matches_reference": True,
        "models_match_reference": strict_equal,
        "model_count": len(source_models),
        "requested_models": requested_models,
        "reasoning_effort": effort,
    }


def _native_codex(explicit: str | None) -> Path:
    configured = explicit or next((os.environ[name] for name in (
        "COLOMBO_CODEX_BIN", "CELL_CODEX_BIN", "CODEX_BIN") if os.environ.get(name)), None)
    if configured:
        result = Path(configured).expanduser().resolve(strict=True)
    elif os.name == "nt":
        local = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local")))
        folder = local / "OpenAI/Codex/bin"
        candidates = list(folder.glob("*/codex.exe")) + list(folder.glob("codex.exe"))
        if not candidates:
            raise CatalogError("Native Codex unavailable; provide --codex-bin")
        result = max(candidates, key=lambda item: item.stat().st_mtime).resolve()
    else:
        found = shutil.which("codex")
        if not found:
            raise CatalogError("Native Codex unavailable; provide --codex-bin")
        result = Path(found).resolve(strict=True)
    if not result.is_file() or (os.name == "nt" and result.suffix.lower() != ".exe"):
        raise CatalogError("--codex-bin must identify the native executable")
    return result


def native_version(executable: Path) -> tuple[str, str]:
    result = subprocess.run([str(executable), "--version"], capture_output=True,
                            text=True, encoding="utf-8", timeout=15, check=False)
    if result.returncode:
        raise CatalogError("Native Codex --version failed")
    match = re.fullmatch(r"codex(?:-cli)?\s+(\d+\.\d+\.\d+)([-+][0-9A-Za-z.+-]+)?\s*",
                         result.stdout.strip())
    if not match:
        raise CatalogError("Native Codex --version returned an unsupported format")
    return match.group(1) + (match.group(2) or ""), match.group(1)


def _write_pair(output: Path, manifest_path: Path, catalog: dict[str, Any],
                manifest: dict[str, Any]) -> None:
    for path in (output, manifest_path):
        if path.exists() or path.is_symlink():
            raise CatalogError("Output catalog or manifest already exists; refusing to replace it")
    contents = [json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
                for value in (catalog, manifest)]
    output.parent.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    try:
        for path, text in zip((output, manifest_path), contents):
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                created.append(path)
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
    except BaseException:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-home", type=Path, required=True)
    parser.add_argument("--reference-runtime-home", type=Path, required=True)
    parser.add_argument("--model", action="append", required=True,
                        help="Requested model; repeat for multiple models using the same effort")
    parser.add_argument("--effort", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--codex-bin", help="Native Codex executable (only --version is invoked)")
    args = parser.parse_args(argv)
    try:
        output = args.output.expanduser().absolute()
        manifest_path = output.with_name(output.name + ".manifest.json")
        if any(path.exists() or path.is_symlink() for path in (output, manifest_path)):
            raise CatalogError("Output catalog or manifest already exists; refusing to replace it")
        source_path, source = _read_cache(args.source_home.expanduser(), "source")
        reference_path, reference = _read_cache(args.reference_runtime_home.expanduser(), "reference")
        if source_path.samefile(reference_path):
            raise CatalogError("Reference must be a separate CLI-produced runtime cache")
        executable = _native_codex(args.codex_bin)
        full_version, client_version = native_version(executable)
        now = datetime.now(timezone.utc)
        checks = validate_snapshot(source, reference, client_version=client_version,
                                   requested_models=args.model, effort=args.effort, now=now)
        manifest = {
            "manifest_version": 1,
            "mode": "explicit_static_catalog_for_one_bounded_run",
            "generated_at": now.isoformat().replace("+00:00", "Z"),
            "source_cache": str(source_path),
            "reference_cache": str(reference_path),
            "native_codex": str(executable),
            "native_codex_version": full_version,
            **checks,
            "source_timestamp_modified": False,
            "catalog_revalidated_during_run": False,
            "identity_check_scope": "Equality with the supplied runtime cache; not independent proof of current login identity",
            "schema_validation_scope": "JSON, metadata, model slugs and requested effort checked here; native Codex parses the full ModelsResponse at startup",
            "limitations": [
                "Static discovery bypasses native cache TTL, version, auth identity and ETag revalidation during the configured run.",
                "Inference authentication remains enforced by the provider; no access is granted by this catalog.",
                "Generate and validate a new snapshot for a new run; do not alter fetched_at to make a stale cache appear fresh.",
                "A fixed catalog does not address inference capacity, network errors or other timeout causes.",
            ],
        }
        _write_pair(output, manifest_path, {"models": source["models"]}, manifest)
        print(json.dumps({"catalog": str(output), "manifest": str(manifest_path), **checks},
                         ensure_ascii=False, allow_nan=False))
        return 0
    except (CatalogError, OSError, subprocess.SubprocessError, ValueError, RecursionError) as error:
        # OSError details can contain paths but never read credential contents.
        message = str(error) if isinstance(error, CatalogError) else type(error).__name__
        print("Catalog preparation refused: " + message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
