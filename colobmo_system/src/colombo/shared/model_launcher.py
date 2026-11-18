"""CLI discovery and immutable startup inputs shared by model callers.

Callers retain their configuration precedence, receipt and recovery lifecycles.
"""
import json
import os
import shutil
import tomllib

from colombo.shared.file_io import Path, atomic_write


def user_configuration(home, *, regular_file=True):
    path = Path(home) / "config.toml"
    available = path.is_file() if regular_file else path.exists()
    return tomllib.loads(path.read_text(encoding="utf-8-sig")) if available else {}


def transport_feature_lines(user, *, error_type=ValueError):
    """Preserve explicit transport preferences without importing unrelated features."""
    features = user.get("features", {})
    if not isinstance(features, dict):
        raise error_type("Codex features must be a table")
    if "respect_system_proxy" not in features:
        return []
    value = features["respect_system_proxy"]
    if type(value) is not bool:
        raise error_type("Codex features.respect_system_proxy must be a boolean")
    return ["respect_system_proxy = " + json.dumps(value)]


def discover_cli(*, explicit=None, config_homes=(), windows_roots=(), recursive=False,
                 resolve_paths=False, error_type=RuntimeError, missing_message="Codex CLI not found"):
    """Use the caller's ordered discovery locations without changing precedence."""
    def display(path):
        return str(path.resolve()) if resolve_paths else str(path)

    if explicit:
        path = Path(explicit).expanduser() if resolve_paths else Path(explicit)
        if not path.is_file():
            raise error_type("Configured Codex executable does not exist")
        return display(path) if resolve_paths else explicit
    for home in config_homes() if callable(config_homes) else config_homes:
        config = user_configuration(home)
        direct = config.get("CODEX_CLI_PATH")
        candidates = [direct] if direct else []
        candidates += [value["CODEX_CLI_PATH"] for value in config.values()
                       if isinstance(value, dict) and value.get("CODEX_CLI_PATH")]
        for value in candidates:
            if isinstance(value, str) and Path(value).is_file():
                return display(Path(value))
    if os.name == "nt":
        candidates = []
        roots = windows_roots() if callable(windows_roots) else windows_roots
        for root in map(Path, roots):
            if recursive:
                candidates.extend(root.rglob("codex.exe") if root.exists() else [])
            else:
                candidates.extend(root.glob("*/codex.exe"))
                candidates.extend(root.glob("codex.exe"))
        if candidates:
            return display(max(candidates, key=lambda path: path.stat().st_mtime))
    found = shutil.which("codex")
    if not found:
        raise error_type(missing_message)
    return found


def seed_model_cache(original, home):
    """Copy optional cache bytes without changing freshness or identity."""
    try:
        with (Path(original) / "models_cache.json").open("rb") as stream:
            data = stream.read(5 * 1024 * 1024 + 1)
        if len(data) > 5 * 1024 * 1024:
            return
        value = json.loads(data.decode("utf-8"))
        if isinstance(value, dict) and isinstance(value.get("models"), list):
            atomic_write(Path(home) / "models_cache.json", data)
    except (OSError, UnicodeError, ValueError, RecursionError):
        pass  # Optional discovery metadata never becomes a launch requirement.


def stage_model_catalog(value, model, effort, home, *, check_linked_parents=False,
                        require_effort=False, return_source=False):
    """Validate and freeze catalog bytes, preserving caller-specific path policy."""
    source = Path(value).expanduser()
    if not source.is_absolute():
        raise ValueError("Model catalog path must be absolute")
    parts = (source, *source.parents) if check_linked_parents else (source,)
    for part in parts:
        if part.is_symlink() or (check_linked_parents and getattr(part, "is_junction", lambda: False)()):
            raise ValueError("Model catalog must be an ordinary file without linked path components")
    if not source.is_file():
        raise ValueError("Model catalog must be an existing ordinary JSON file")
    source = source.resolve()
    with source.open("rb") as stream:
        data = stream.read(5 * 1024 * 1024 + 1)
    if len(data) > 5 * 1024 * 1024:
        raise ValueError("Model catalog exceeds 5 MiB")
    value = json.loads(data.decode("utf-8"))
    models = value.get("models") if isinstance(value, dict) else None
    if not isinstance(models, list) or not models:
        raise ValueError("Model catalog requires a nonempty models list")
    slugs = [item.get("slug") if isinstance(item, dict) else None for item in models]
    if any(not isinstance(slug, str) or not slug.strip() for slug in slugs) or len(set(slugs)) != len(slugs):
        raise ValueError("Model catalog requires unique nonempty model slugs")
    if not model or model not in slugs:
        raise ValueError("Selected model is absent from the explicit model catalog")
    levels = models[slugs.index(model)].get("supported_reasoning_levels", [])
    supported = [level.get("effort") for level in levels if isinstance(level, dict)] if isinstance(levels, list) else []
    if (require_effort or effort) and effort not in supported:
        raise ValueError("Selected reasoning effort is absent from the explicit model catalog")
    destination = Path(home) / "model_catalog.json"
    atomic_write(destination, data)
    return source if return_source else destination.resolve()
