"""User defaults, task configuration and immutable process-start snapshots."""

from __future__ import annotations
import json
import math
import os
import tomllib
import time
from copy import deepcopy
from functools import lru_cache
from colombo.shared.file_io import Path, file_lock, atomic_write
from colombo.project_paths import PROJECT_ROOT, CELL_CODE_ROOT, CELL_AGENTS_ROOT
from contextlib import contextmanager, ExitStack
from datetime import datetime, timezone


CONFIG_PATH = Path(PROJECT_ROOT) / "config.toml"

# Validation describes the contract, never a second set of default values.
_STRINGS = {
    "model": {"name", "reasoning_effort"},
    "handoff": {"recovery_reasoning_effort"},
    "network": {"theorem_search_url", "search_provider", "reader_provider", "api_key_file"},
    "experiment": {"model", "reasoning_effort", "memory_limit"},
}
_PROCESS_TIMEOUTS = {
    "agents": {"prover_timeout_seconds", "subcell_timeout_seconds", "verifier_timeout_seconds",
               "report_check_timeout_seconds", "audit_timeout_seconds"},
    "challenge": {"timeout_seconds", "check_timeout_seconds"},
    "experiment": {"timeout_seconds"},
}
_INTEGERS = {
    "agents": {"prover_max_rounds", "verifier_max_rounds",
               "report_check_max_attempts"},
    "handoff": {"reserve_seconds", "recovery_seconds", "recovery_min_start_seconds",
                "recovery_input_max_bytes", "recovery_source_max_bytes", "recovery_max_records"},
    "challenge": {"max_rounds", "max_check_attempts"},
    "experiment": {"max_runs", "max_tool_calls", "max_output_tokens",
                   "artifact_max_bytes", "max_total_artifact_bytes", "max_files", "download_reserve_seconds"},
    "parallel": {"max_subcells", "max_depth", "context_dependency_depth"},
    "retrieval": {"search_results", "verifier_search_results", "max_search_results",
                  "memory_results", "verifier_memory_results", "max_memory_results", "summary_max_chars"},
    "network": {"max_download_bytes", "chunk_bytes", "html_max_links", "query_max_chars"},
    "runtime": {"mcp_startup_timeout_seconds", "mcp_tool_timeout_seconds"},
    "limits": {"record_id_max_chars", "request_id_max_chars", "group_id_max_chars"},
}
_NUMBERS = {
    "experiment": {"poll_seconds"},
    "network": {"connect_timeout_seconds", "read_timeout_seconds", "arxiv_interval_seconds"},
    "runtime": {"process_poll_seconds", "terminate_wait_seconds", "task_lock_timeout_seconds",
                "store_lock_timeout_seconds", "lock_poll_seconds"},
}
_BOOLS = {"experiment": {"enabled"}, "retrieval": {"include_context", "verifier_reverse"},
          "network": {"prover_search_enabled", "subcell_search_enabled"}}
_ZERO_ALLOWED = {("parallel", "max_depth"), ("parallel", "context_dependency_depth"),
                 ("handoff", "reserve_seconds"), ("handoff", "recovery_seconds")}
_ALIASES = {
    "model": ("model", "name"),
    "prover_timeout": ("agents", "prover_timeout_seconds"),
    "max_prover_rounds": ("agents", "prover_max_rounds"),
    "verification_timeout": ("agents", "verifier_timeout_seconds"),
    "audit_timeout": ("agents", "audit_timeout_seconds"),
    "task_timeout": ("agents", "subcell_timeout_seconds"),
    "max_review_rounds": ("agents", "verifier_max_rounds"),
    "task_max_concurrency": ("parallel", "max_subcells"),
    "task_max_depth": ("parallel", "max_depth"),
}


def parse_process_timeout(value: int | str) -> int | str:
    """A long research process has either positive seconds or no wall-clock limit."""
    if value == "unlimited" or (type(value) is int and value >= 1):
        return value
    raise ValueError('Process timeout must be a positive integer or the exact string "unlimited"')


def normalize_role(role: str) -> str:
    """Accept historical worker roles while exposing the current name."""
    role = "subcell" if role == "worker" else role
    if role not in {"prover", "subcell", "audit", "verifier"}:
        raise ValueError(f"Unknown agent role: {role}")
    return role


def migrate_settings(value: dict, *, defaults: dict | None = None) -> dict:
    """Normalize historical snapshots; current TOML and override keys stay strict."""
    if not isinstance(value, dict):
        raise ValueError("Cell settings must be an object/table")
    value = deepcopy(value)
    for section, old, new in (("agents", "worker_timeout_seconds", "subcell_timeout_seconds"),
                              ("parallel", "max_workers", "max_subcells")):
        table = value.get(section)
        if isinstance(table, dict) and old in table:
            if new in table and table[new] != table[old]:
                raise ValueError(f"Conflicting saved settings: {section}.{old} and {new}")
            table[new] = table.pop(old)
    runtime = value.get("runtime")
    if isinstance(runtime, dict):
        # Final verification now runs directly under Python, with its own timeout.
        runtime.pop("stop_hook_timeout_seconds", None)
    limits = value.get("limits")
    if isinstance(limits, dict):
        limits.pop("verifier_run_id_max_chars", None)
    # Add only known new fields to historical snapshots; existing user choices
    # remain pinned and unrelated omissions/misspellings still fail validation.
    # Preserve the backends of historical task snapshots on ordinary resume.
    # Before effort was split, an existing Experiment inherited its owning
    # Cell's saved effort. Preserve that choice rather than today's profile.
    experiment = value.get("experiment")
    if isinstance(experiment, dict) and "reasoning_effort" not in experiment:
        saved_model = value.get("model", {})
        if isinstance(saved_model, dict) and "reasoning_effort" in saved_model:
            experiment["reasoning_effort"] = saved_model["reasoning_effort"]
    if isinstance(value.get("network"), dict):
        value["network"].setdefault("search_provider", "arxiv")
        value["network"].setdefault("reader_provider", "direct")
        value["network"].setdefault("api_key_file", "")
    for section, keys in {
        "network": {"prover_search_enabled", "subcell_search_enabled"},
        "retrieval": {"summary_max_chars"},
        "agents": {"report_check_timeout_seconds", "report_check_max_attempts"},
        "handoff": _STRINGS["handoff"] | _INTEGERS["handoff"],
        "challenge": _INTEGERS["challenge"] | _PROCESS_TIMEOUTS["challenge"],
        "experiment": _STRINGS["experiment"] | _INTEGERS["experiment"] | _NUMBERS["experiment"] | _BOOLS["experiment"] | _PROCESS_TIMEOUTS["experiment"],
    }.items():
        table = value.setdefault(section, {}) if section in {"handoff", "experiment", "challenge"} else value.get(section)
        if isinstance(table, dict):
            for key in keys - table.keys():
                if defaults is None:
                    defaults = _user_config()[0]
                table[key] = defaults[section][key]
    return validate_settings(value)


def needs_run_migration(run: dict, *, defaults: dict | None = None) -> bool:
    """Tell resume whether an old task needs its normalized defaults pinned once."""
    if not isinstance(run, dict):
        raise ValueError("run.json must contain an object")
    options = run.get("agent_options")
    return ("settings" not in run or "role" not in run or run.get("role") == "worker"
            or not isinstance(options, dict) or "search_enabled" not in options
            or migrate_settings(run["settings"], defaults=defaults) != run["settings"])


def merge_settings(settings: dict, overrides: dict | None = None) -> dict:
    """Apply a nested partial update, rejecting misspellings and invalid values."""
    result = validate_settings(settings)
    if overrides is None:
        return result
    if not isinstance(overrides, dict):
        raise ValueError("settings_overrides must be an object/table")
    for section, changes in overrides.items():
        if section not in result or not isinstance(changes, dict):
            raise ValueError(f"Unknown settings section or invalid patch: {section}")
        unknown = set(changes) - set(result[section])
        if unknown:
            raise ValueError(f"Unknown settings in [{section}]: {sorted(unknown)}")
        result[section].update(deepcopy(changes))
    return validate_settings(result)


def _read_run(run_dir: Path | None) -> dict | None:
    if run_dir is None:
        return None
    path = Path(run_dir) / "run.json"
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("run.json must contain an object")
    return value


def get_search_enabled(role: str, settings: dict, run_dir: Path | None = None) -> bool:
    """Resolve task search, including reviewers nested inside their owning task.

    Independent subcells keep their own options. Review workspaces have no
    run.json of their own, so their nearest enclosing task supplies an explicit
    search choice; without one, the historical verifier default remains live.
    """
    role = normalize_role(role)
    if role == "audit":
        return False
    if run_dir is None and os.getenv("CELL_RUN_DIR"):
        run_dir = Path(os.environ["CELL_RUN_DIR"])
    run = _read_run(run_dir)
    if role == "verifier" and run is None and run_dir is not None:
        for parent in Path(run_dir).resolve().parents:
            run = _read_run(parent)
            if run is not None:
                break
    if run is not None:
        saved_role = normalize_role(run.get("role", "subcell" if run.get("task_depth", 0) else "prover"))
        options = run.get("agent_options", {})
        if not isinstance(options, dict):
            raise ValueError("agent_options must be an object")
        if (saved_role == role or role == "verifier") and "search_enabled" in options:
            value = options["search_enabled"]
            if type(value) is not bool:
                raise ValueError("agent_options.search_enabled must be true or false")
            return value
    if role == "verifier":
        return True
    value = settings["network"][f"{role}_search_enabled"]
    if type(value) is not bool:
        raise ValueError(f"network.{role}_search_enabled must be true or false")
    return value


def validate_settings(value: dict) -> dict:
    if not isinstance(value, dict):
        raise ValueError("Cell settings must be an object/table")
    expected = {}
    for groups in (_STRINGS, _PROCESS_TIMEOUTS, _INTEGERS, _NUMBERS, _BOOLS):
        for section, keys in groups.items():
            expected.setdefault(section, set()).update(keys)
    if set(value) != set(expected):
        raise ValueError(f"Invalid config sections: missing={set(expected)-set(value)}, unknown={set(value)-set(expected)}")
    for section, keys in expected.items():
        table = value[section]
        if not isinstance(table, dict) or set(table) != keys:
            raise ValueError(f"Invalid config keys in [{section}]; expected {sorted(keys)}")
        for key, item in table.items():
            name = f"{section}.{key}"
            if key in _STRINGS.get(section, set()):
                if not isinstance(item, str) or (key.endswith("reasoning_effort") and not item.strip()):
                    raise ValueError(f"{name} must be a string (reasoning effort must be non-empty)")
            elif key in _BOOLS.get(section, set()):
                if type(item) is not bool:
                    raise ValueError(f"{name} must be true or false")
            elif key in _PROCESS_TIMEOUTS.get(section, set()):
                try:
                    parse_process_timeout(item)
                except ValueError as exc:
                    raise ValueError(f'{name} must be a positive integer or "unlimited"') from exc
            else:
                integer = key in _INTEGERS.get(section, set())
                if (type(item) is not int if integer else type(item) not in (int, float)):
                    raise ValueError(f"{name} must be {'an integer' if integer else 'a number'}")
                minimum = 0 if (section, key) in _ZERO_ALLOWED else 1 if integer else 0
                if not math.isfinite(item) or item < minimum or (not integer and item == 0):
                    raise ValueError(f"{name} must be {'>= '+str(minimum) if integer else 'finite and > 0'}")
    for key, allowed in {"search_provider": {"serper", "arxiv"},
                         "reader_provider": {"jina", "direct"}}.items():
        if value["network"][key] not in allowed:
            raise ValueError(f"network.{key} must be one of {sorted(allowed)}")
    for key in ("record_id_max_chars",):
        if value["limits"][key] < 32:
            raise ValueError(f"limits.{key} must be >= 32 to fit generated identifiers")
    if value["handoff"]["recovery_input_max_bytes"] < 2048:
        raise ValueError("handoff.recovery_input_max_bytes must be >= 2048 for the handoff envelope")
    retrieval = value["retrieval"]
    for key in ("search_results", "verifier_search_results"):
        if retrieval[key] > retrieval["max_search_results"]:
            raise ValueError(f"retrieval.{key} exceeds max_search_results")
    for key in ("memory_results", "verifier_memory_results"):
        if retrieval[key] > retrieval["max_memory_results"]:
            raise ValueError(f"retrieval.{key} exceeds max_memory_results")
    experiment = value["experiment"]
    if not experiment["model"].strip():
        raise ValueError("experiment.model must name an API model supporting Code Interpreter")
    if experiment["memory_limit"] not in {"1g", "4g", "16g", "64g"}:
        raise ValueError("experiment.memory_limit must be 1g, 4g, 16g or 64g")
    if experiment["timeout_seconds"] != "unlimited" and experiment["download_reserve_seconds"] >= experiment["timeout_seconds"]:
        raise ValueError("experiment.download_reserve_seconds must be less than timeout_seconds")
    if experiment["artifact_max_bytes"] > experiment["max_total_artifact_bytes"]:
        raise ValueError("experiment.artifact_max_bytes exceeds max_total_artifact_bytes")
    return deepcopy(value)


@lru_cache(maxsize=8)
def _read_cached(path: str, stamp: int, size: int) -> dict:
    source = Path(path)
    text = source.read_text(encoding="utf-8-sig")
    return json.loads(text) if source.suffix == ".json" else tomllib.loads(text)


def _read_document(path: Path) -> dict:
    path = Path(path).resolve()
    try:
        stat = path.stat()
        return deepcopy(_read_cached(str(path), stat.st_mtime_ns, stat.st_size))
    except (OSError, ValueError) as exc:
        raise ValueError(f"Cannot load Cell configuration {path}: {exc}") from exc


def load_policy(document: dict | None = None, *, profile: str | None = None) -> dict:
    """Resolve the sole outer configuration; snapshots are never input overlays."""
    from colombo.configuration import resolve_document
    document = _read_document(CONFIG_PATH) if document is None else deepcopy(document)
    if "policy_metadata" in document:
        if profile is not None and profile != document["profile"]:
            raise ValueError("Cannot select another profile from an already resolved policy")
        return document
    return resolve_document(document, source=CONFIG_PATH, profile=profile)


def _user_config(document: dict | None = None) -> tuple[dict, dict, str]:
    raw = _read_document(CONFIG_PATH) if document is None else deepcopy(document)
    if "policy_metadata" in raw:
        return validate_settings(raw["cell"]["settings"]), {}, raw["profile"]
    base = load_policy(raw, profile="standard")
    profiles = {}
    for name in raw["profiles"]:
        selected = load_policy(raw, profile=name)
        profiles[name] = validate_settings(selected["cell"]["settings"])
    return validate_settings(base["cell"]["settings"]), profiles, raw["profile"]


def get_profile_overrides(profile: str) -> dict:
    """Compatibility helper for an explicit root-selected preset."""
    return load_defaults(profile=profile)[0]


def load_defaults(profile: str | None = None, *, document: dict | None = None) -> tuple[dict, str]:
    """Resolve the selected root preset; budget environment overrides are ignored."""
    resolved = load_policy(document, profile=profile)
    settings = deepcopy(resolved["cell"]["settings"])
    # Non-budget compatibility options remain local behavior choices.
    for env, section, key in (
        ("CELL_MODEL", "model", "name"),
        ("CELL_REASONING_EFFORT", "model", "reasoning_effort"),
        ("CELL_THEOREM_SEARCH_URL", "network", "theorem_search_url"),
    ):
        if env in os.environ:
            settings[section][key] = os.environ[env]
    return validate_settings(settings), resolved["profile"]


_NON_BUDGET_OVERRIDES = {
    "model": {"name", "reasoning_effort"},
    "handoff": {"recovery_reasoning_effort"},
    "network": {"prover_search_enabled", "subcell_search_enabled", "search_provider",
                "reader_provider", "theorem_search_url", "api_key_file"},
    "experiment": {"enabled", "model", "reasoning_effort"},
    "retrieval": {"include_context", "verifier_reverse"},
}


def reject_budget_overrides(overrides: dict | None) -> None:
    """Public runtime tools may change behavior, never root-owned budgets."""
    if overrides is None:
        return
    if not isinstance(overrides, dict):
        raise ValueError("settings_overrides must be an object/table")
    for section, values in overrides.items():
        if not isinstance(values, dict):
            raise ValueError(f"Invalid settings section: {section}")
        forbidden = set(values) - _NON_BUDGET_OVERRIDES.get(section, set())
        if forbidden:
            fields = ', '.join(f"{section}.{key}" for key in sorted(forbidden))
            raise ValueError(f"Budget/resource settings are owned by the outer config.toml: {fields}")


def apply_budget_policy(settings: dict, policy_settings: dict) -> dict:
    """Adopt root-owned fields at a safe resume boundary, keeping local behavior."""
    # Both arguments may be frozen before new fields were introduced. Upgrade
    # their shape using pinned values before validation, including pending jobs
    # whose root budget has not yet adopted the current configuration.
    policy = migrate_settings(policy_settings)
    result = migrate_settings(settings, defaults=policy)
    for section, values in policy.items():
        for key, value in values.items():
            if key not in _NON_BUDGET_OVERRIDES.get(section, set()):
                result[section][key] = deepcopy(value)
    return validate_settings(result)


def _read_settings(path: Path, *, defaults: dict | None = None) -> dict:
    # Internal process snapshots contain resolved settings, never a live preset.
    value = _read_document(path)
    return migrate_settings(value, defaults=defaults) if Path(path).suffix == ".json" else validate_settings(value)


def get_settings(run_dir: Path | None = None) -> dict:
    """Task snapshot > process snapshot > root table with compatibility env overrides."""
    if run_dir is None and os.getenv("CELL_RUN_DIR"):
        run_dir = Path(os.environ["CELL_RUN_DIR"])
    from colombo.shared.runtime_budget import get_budget_context
    context = get_budget_context(run_dir)
    policy_settings = context.get("policy_settings") if context is not None else None
    if policy_settings is not None:
        policy_settings = migrate_settings(policy_settings)
    run = _read_run(run_dir)
    if run is not None and "settings" in run:
        settings = migrate_settings(run["settings"], defaults=policy_settings)
    elif os.getenv("CELL_SETTINGS_FILE"):
        settings = _read_settings(Path(os.environ["CELL_SETTINGS_FILE"]), defaults=policy_settings)
    elif policy_settings is not None:
        settings = deepcopy(policy_settings)
    else:
        settings, _ = load_defaults()
    # Legacy aliases are output compatibility fields, never another authority.
    if policy_settings is not None:
        settings = apply_budget_policy(settings, policy_settings)
    return validate_settings(settings)


def run_fields(settings: dict) -> dict:
    """Keep established run.json fields as compatibility aliases of the snapshot."""
    settings = validate_settings(settings)
    fields = {alias: settings[section][key] for alias, (section, key) in _ALIASES.items()}
    fields["model"] = fields["model"] or None
    return fields


def apply_overrides(settings: dict, *, model=None, timeout=None, max_rounds=None) -> dict:
    settings = validate_settings(settings)
    if model is not None:
        settings["model"]["name"] = model
    if timeout is not None or max_rounds is not None:
        raise ValueError("Budget CLI overrides are disabled; edit the outer config.toml and select its profile")
    return validate_settings(settings)


# Task-scoped settings updates

@contextmanager
def _settings_lock(root: Path, timeout: float, interval: float):
    """Serialize settings updates without classifying errors from the update body."""
    root.mkdir(parents=True, exist_ok=True)
    lock_path = root / ".settings.lock"
    if lock_path.is_symlink():
        raise ValueError("Settings lock must be a local ordinary file")
    with ExitStack() as stack:
        try:
            stack.enter_context(file_lock(lock_path, timeout, interval))
        except TimeoutError:
            raise TimeoutError("Timed out waiting for task settings lock") from None
        yield


def _read_run_document(path: Path) -> dict:
    if not path.exists():
        return {}
    if path.is_symlink() or path.resolve().parent != path.parent:
        raise ValueError("run.json must be a local ordinary file")
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("run.json must contain an object")
    return value


def _save(path: Path, value: dict) -> None:
    content = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    atomic_write(path, content.encode("utf-8"))


def _timing(section: str, key: str, role: str) -> str:
    if section in {"model", "handoff"} or (section == "agents" and key == f"{role}_timeout_seconds"):
        return "next_agent_start"
    if section == "runtime" and key in {
        "mcp_startup_timeout_seconds", "mcp_tool_timeout_seconds",
        "process_poll_seconds", "terminate_wait_seconds",
    }:
        return "next_agent_start"
    if section == "agents":
        return "next_prover_turn" if key == "prover_max_rounds" else "next_related_agent_start"
    if section == "parallel":
        return "next_spawn_task"
    if section == "experiment":
        return "next_experiment_call" if key in {"enabled", "max_runs"} else "next_experiment_run"
    if section == "challenge":
        return "next_challenge_call" if key in {"max_rounds", "max_check_attempts"} else "next_challenge"
    if section == "network" and key.endswith("_search_enabled"):
        return "next_task_start_default"
    return "next_tool_call"


def _launch_state(root: Path) -> tuple[dict | None, bool | None, str | None]:
    # Environment values describe this process, never another task queried by a caller.
    env_root = os.getenv("CELL_RUN_DIR")
    if env_root and Path(env_root).resolve() != root:
        return None, None, None
    launch = None
    if os.getenv("CELL_SETTINGS_FILE"):
        from colombo.shared.runtime_budget import get_budget_context
        context = get_budget_context(root)
        launch = migrate_settings(json.loads(Path(os.environ["CELL_SETTINGS_FILE"]).read_text(encoding="utf-8-sig")),
                                  defaults=context["policy_settings"] if context is not None else None)
    native = os.getenv("CELL_SEARCH_ENABLED")
    if native is not None and native not in {"0", "1"}:
        raise ValueError("CELL_SEARCH_ENABLED must be 0 or 1")
    requested_model = os.getenv("CELL_REQUESTED_MODEL")
    if requested_model is None and launch is not None:
        requested_model = launch["model"]["name"]
    return launch, None if native is None else native == "1", requested_model


def _report(root: Path, role: str, settings: dict, search: bool, revision: int,
            changes: list[dict] | None = None) -> dict:
    launch, native, requested_model = _launch_state(root)
    pending = []
    if launch is not None:
        for section, table in settings.items():
            for key, value in table.items():
                previous_request = requested_model if (section, key) == ("model", "name") else launch[section][key]
                if _timing(section, key, role) == "next_agent_start" and value != previous_request:
                    pending.append({"parameter": f"{section}.{key}", "running": launch[section][key], "next": value})
    if native is not None and native != search:
        pending.append({"parameter": "native_search_enabled", "running": native, "next": search})
    return {
        "ok": True, "role": role, "settings_revision": revision,
        "settings_file": str(root / "run.json"), "desired_settings": settings,
        "search_enabled": search, "lookup_enabled": search,
        "native_search_enabled": native, "launch_settings": launch,
        "pending_next_start": pending, "changes": changes or [],
        "effect_timing": {
            "search_enabled": {"lookup": "next_tool_call", "native_search": "next_agent_start"},
            "model_and_current_process_timeouts": "next_agent_start",
            "parallel": "next_spawn_task",
            "other_settings": "See each changes entry; existing processes retain their startup parameters.",
        },
        "notes": [
            "Root config.toml is user defaults and is never changed by this tool.",
            "Existing sibling/child tasks retain their own configuration; this task's search override is not inherited.",
            "Native web search changes require a new agent process; this tool does not restart or cancel processes.",
        ],
    }


def configure(run_dir: Path, role: str, settings_overrides: dict | None = None,
              search_enabled: bool | None = None, reason: str = "", *,
              profile_name: str | None = None) -> dict:
    """Inspect with no arguments, or atomically update only the caller's task."""
    role = normalize_role(role)
    if role not in {"prover", "subcell"}:
        raise ValueError("Only prover and subcell can configure their own task")
    root = Path(run_dir).resolve()
    path = root / "run.json"
    if root in {CONFIG_PATH.resolve().parent, CELL_CODE_ROOT, CELL_AGENTS_ROOT}:
        raise ValueError("Use a task workspace, not the user configuration or Cell source directory")
    if search_enabled is not None and type(search_enabled) is not bool:
        raise ValueError("search_enabled must be true or false")
    if settings_overrides is not None and not isinstance(settings_overrides, dict):
        raise ValueError("settings_overrides must be an object/table")
    reject_budget_overrides(settings_overrides)
    # CLI-only provenance, recorded atomically alongside resolved settings.
    # The MCP tool exposes parameter patches, not edits to user preset definitions.
    if profile_name is not None and (not isinstance(profile_name, str) or not profile_name.strip()):
        raise ValueError("profile_name must be a nonempty string")
    if profile_name is not None:
        raise ValueError("Select the profile in the outer config.toml; task-local profile changes are disabled")
    editing = bool(settings_overrides) or search_enabled is not None or profile_name is not None
    if editing and (not isinstance(reason, str) or not reason.strip()):
        raise ValueError("Provide a nonempty reason when changing task parameters")
    initial = get_settings(root)
    # Fail before acquiring or creating files for malformed configuration patches.
    merge_settings(initial, settings_overrides)
    # Inspect process metadata before committing; malformed launch metadata must
    # not turn a successful write into an apparent failed update.
    _launch_state(root)
    if not editing:
        run = _read_run_document(path)
        return _report(root, role, initial, get_search_enabled(role, initial, root),
                       run.get("settings_revision", 0))
    runtime = initial["runtime"]
    with _settings_lock(root, runtime["task_lock_timeout_seconds"], runtime["lock_poll_seconds"]):
        run = _read_run_document(path)
        saved_role = normalize_role(run.get("role", "subcell" if run.get("task_depth", 0) else role))
        if saved_role != role:
            raise ValueError("Cannot configure a task owned by another agent role")
        current = get_settings(root)
        new = merge_settings(current, settings_overrides)
        previous_search = get_search_enabled(role, current, root)
        wanted_search = previous_search if search_enabled is None else search_enabled
        changes = []
        for section, values in new.items():
            for key, value in values.items():
                if value != current[section][key]:
                    changes.append({"parameter": f"{section}.{key}", "before": current[section][key],
                                    "after": value, "effective": _timing(section, key, role)})
        if wanted_search != previous_search:
            changes.append({"parameter": "search_enabled", "before": previous_search, "after": wanted_search,
                            "effective": {"lookup": "next_tool_call", "native_search": "next_agent_start"}})
        if profile_name is not None and profile_name != run.get("profile"):
            changes.append({"parameter": "profile", "before": run.get("profile"), "after": profile_name,
                            "effective": "selection_recorded; each parameter keeps its own effect timing"})
        revision = run.get("settings_revision", 0)
        history = run.get("settings_history", [])
        if type(revision) is not int or revision < 0 or not isinstance(history, list):
            raise ValueError("Invalid task settings history")
        migration = needs_run_migration(run, defaults=current)
        if changes or migration:
            revision += 1
            history.append({"revision": revision, "time": datetime.now(timezone.utc).isoformat(),
                            "actor": role, "reason": reason.strip(), "changes": changes,
                            "migration": migration})
        options = run.get("agent_options", {})
        if not isinstance(options, dict):
            raise ValueError("agent_options must be an object")
        run.update(run_fields(new), role=role, settings=new, settings_revision=revision,
                   settings_history=history, agent_options={**options, "search_enabled": wanted_search})
        if profile_name is not None:
            run["profile"] = profile_name
        # The configuration and its audit trail are one atomic document.
        _save(path, run)
        return _report(root, role, new, wanted_search, revision, changes)


def pin_task_settings(run_dir: Path, role: str) -> dict:
    """Normalize an old task once, preserving already-canonical resume files."""
    root = Path(run_dir).resolve()
    role = normalize_role(role)
    if not (root / "run.json").is_file():
        raise FileNotFoundError(f"No existing task configuration: {root / 'run.json'}")
    run = _read_run_document(root / "run.json")
    current = get_settings(root)
    if needs_run_migration(run, defaults=current):
        # Internal normalization is not an agent-editable budget override.
        with _settings_lock(root, current["runtime"]["task_lock_timeout_seconds"],
                            current["runtime"]["lock_poll_seconds"]):
            run = _read_run_document(root / "run.json")
            current = get_settings(root)
            # Another process may have normalized the document while we waited.
            if needs_run_migration(run, defaults=current):
                revision = run.get("settings_revision", 0)
                history = run.get("settings_history", [])
                options = run.get("agent_options", {})
                if type(revision) is not int or revision < 0 or not isinstance(history, list):
                    raise ValueError("Invalid task settings history")
                if not isinstance(options, dict):
                    raise ValueError("agent_options must be an object")
                search = get_search_enabled(role, current, root)
                revision += 1
                history.append({"revision": revision, "time": datetime.now(timezone.utc).isoformat(),
                                "actor": role, "reason": "Normalize saved task settings",
                                "changes": [], "migration": True})
                run.update(run_fields(current), settings=current, role=role,
                           settings_revision=revision, settings_history=history,
                           agent_options={**options, "search_enabled": search})
                _save(root / "run.json", run)
    return current


def managed_settings(run_dir, snapshot, *, partial=False):
    """Apply the adopted run policy to old snapshots without changing models."""
    from colombo.shared.runtime_budget import get_budget_context
    context = get_budget_context(run_dir)
    if context is None:
        return snapshot
    full = merge_settings(get_settings(run_dir), snapshot) if partial else snapshot
    return apply_budget_policy(full, context["policy_settings"])
