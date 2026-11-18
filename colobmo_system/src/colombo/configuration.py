"""Resolve one outer configuration and its difference-only preset.

This module has no numerical defaults. Colombo research is bounded by Waves and
dispatches. Generated unlimited fields preserve Cell execution interfaces.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tomllib

from colombo.project_paths import PROJECT_ROOT

CONFIG_PATH = Path(PROJECT_ROOT) / "config.toml"
RESEARCH_TIMEOUTS = {
    "agents": ("prover_timeout_seconds", "subcell_timeout_seconds",
               "verifier_timeout_seconds", "report_check_timeout_seconds", "audit_timeout_seconds"),
    "challenge": ("timeout_seconds", "check_timeout_seconds"),
    "experiment": ("timeout_seconds",),
}


def merge(base, patch, path=()):
    """Apply explicit preset differences; typoed paths never create new options."""
    if not isinstance(base, dict) or not isinstance(patch, dict):
        raise ValueError("Configuration presets must be TOML tables")
    result = deepcopy(base)
    for key, value in patch.items():
        name = '.'.join((*path, key))
        if key not in base:
            raise ValueError(f"Unknown config key: {name}")
        if isinstance(base[key], dict):
            if not isinstance(value, dict):
                raise ValueError(f"Config table expected: {name}")
            result[key] = merge(base[key], value, (*path, key))
        elif isinstance(value, dict):
            raise ValueError(f"Config scalar expected: {name}")
        else:
            result[key] = deepcopy(value)
    return result


def _validate_base(document):
    current = isinstance(document, dict) and document.get("workflow", {}).get("version") == 3
    required = {"profile", "storage_version", "workflow", "brain", "verifier",
                "audit", "limits", "runtime", "cell", "profiles"}
    required.add("integration" if current else "budget")
    optional = {"research_mode"}
    if not isinstance(document, dict) or not required <= set(document) or set(document) - required - optional:
        present = set(document) if isinstance(document, dict) else set()
        raise ValueError(f"A complete outer config is required; missing={sorted(required-present)}, "
                         f"unknown={sorted(present-required-optional)}. --config selects one complete file, not an overlay.")
    if current and document.get("research_mode", "oracle_complexity") != "oracle_complexity":
        raise ValueError("Colombo research_mode is fixed to oracle_complexity")
    if document.get("research_mode", "generic") not in ("auto", "generic", "oracle_complexity"):
        raise ValueError("research_mode must be auto, generic or oracle_complexity")
    if current:
        expected = {"max_rounds", "max_dispatches_per_wave", "max_parallel_cells"}
        if not isinstance(document["limits"], dict) or set(document["limits"]) != expected:
            raise ValueError("Colombo limits require max_rounds, max_dispatches_per_wave and max_parallel_cells; "
                             "remove historical run-wide dispatch/model-call and Assessment caps")
        for key, value in document["limits"].items():
            if type(value) is not int or value <= 0:
                raise ValueError(f"limits.{key} must be a positive integer")
        integration = document["integration"]
        if not isinstance(integration, dict) or set(integration) != {"timeout_seconds"}:
            raise ValueError("integration requires only timeout_seconds")
        if type(integration["timeout_seconds"]) is not int or integration["timeout_seconds"] <= 0:
            raise ValueError("integration.timeout_seconds must be positive integer seconds")
    else:
        # Historical policy snapshots remain readable by legacy fixture/runtime
        # consumers. Public Colombo load_config separately rejects workflow != 3.
        research = document.get("budget", {}).get("research", {})
        if set(document["budget"]) != {"research"} or set(research) != {"total_active_seconds"}:
            raise ValueError("budget.research must contain only total_active_seconds")
        value = research["total_active_seconds"]
        if not (value == "unlimited" or type(value) is int and value > 0):
            raise ValueError('budget.research.total_active_seconds must be positive integer seconds or "unlimited"')
    for role in ("brain", "verifier", "audit"):
        allowed = {"model", "reasoning_effort"} | ({"search_enabled"} if role == "brain" else set())
        if not isinstance(document[role], dict) or set(document[role]) != allowed:
            raise ValueError(f"{role} must contain {sorted(allowed)}; no independent research time setting is allowed")
    cell = document["cell"]
    if not isinstance(cell, dict) or set(cell) != {"python", "stop_on_confirmed_error", "settings"}:
        raise ValueError("cell requires python, stop_on_confirmed_error, settings; choose profile at the top level")
    settings = cell["settings"]
    for section, keys in RESEARCH_TIMEOUTS.items():
        if not isinstance(settings.get(section), dict):
            raise ValueError(f"Missing Cell settings section: {section}")
        duplicate = set(settings[section]) & set(keys)
        if duplicate:
            raise ValueError(f"Research timeout fields are derived, not separately configured: {section}.{sorted(duplicate)}")


def resolve_document(document, *, source=None, profile=None):
    """Return effective full config. Profiles are patches over the standard base."""
    _validate_base(document)
    presets = document["profiles"]
    if not isinstance(presets, dict):
        raise ValueError("profiles must be a table")
    selected = document["profile"] if profile is None else profile
    if not isinstance(selected, str) or selected != 'standard' and selected not in presets:
        raise ValueError(f"Unknown profile {selected!r}; choose standard or one of {sorted(presets)}")
    baseline = {k: deepcopy(v) for k,v in document.items() if k not in {"profile", "profiles"}}
    baseline.setdefault("research_mode", "oracle_complexity" if baseline.get("workflow", {}).get("version") == 3 else "generic")
    for name, patch in presets.items():
        if not isinstance(name,str) or not name or name.strip()!=name or name=='standard':
            raise ValueError("Profile names must be nonempty; standard is the base and must not be duplicated")
        resolved = merge(baseline, patch)
        _validate_base({**resolved, "profile":name,"profiles":{}})
    resolved = baseline if selected=='standard' else merge(baseline, presets[selected])
    # Legacy execution interfaces receive no independent research timer.
    for role in ("brain", "verifier", "audit"):
        resolved[role]["timeout_seconds"] = "unlimited"
    resolved["cell"]["run_timeout_seconds"] = "unlimited"
    for section, keys in RESEARCH_TIMEOUTS.items():
        for key in keys:
            resolved["cell"]["settings"][section][key] = "unlimited"
    resolved["profile"] = selected
    revision = hashlib.sha256(json.dumps(resolved,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    resolved["policy_metadata"] = {"revision":revision,"profile":selected,
                                   "source":str(Path(source).resolve()) if source else str(CONFIG_PATH)}
    return resolved


def load_policy(path=None, *, profile=None):
    source = CONFIG_PATH if path is None else Path(path)
    document = tomllib.loads(source.read_text(encoding="utf-8-sig"))
    return resolve_document(document,source=source,profile=profile)


def require_current_workflow(config):
    """Never run a historical workflow against the current single protocol."""
    version = config.get("workflow", {}).get("version", 1)
    if type(version) is not int or version != 3:
        raise ValueError("Colombo supports workflow version 3 only; start a new current-format run.")


def _resolve_cell(config):
    from colombo.cell.settings import load_defaults
    cell = config["cell"]
    settings, profile = load_defaults(document=config)
    if not isinstance(cell["python"], str):
        raise ValueError("cell.python must be a string")
    if type(cell["stop_on_confirmed_error"]) is not bool:
        raise ValueError("cell.stop_on_confirmed_error must be boolean")
    return {key:deepcopy(cell[key]) for key in
            ("python", "run_timeout_seconds", "stop_on_confirmed_error")} | {
                "profile":profile, "settings":settings,
                "policy_metadata":deepcopy(config["policy_metadata"])}


def load_config(path=None):
    """Load exactly one complete config, then resolve its selected preset once."""
    base = load_policy(PROJECT_ROOT / "config.toml" if path is None else path)
    for key, value in base["limits"].items():
        if type(value) is not int or value < 1:
            raise ValueError(f"limits.{key} must be a positive integer")
    for role in ("brain", "verifier", "audit"):
        for key in ("model", "reasoning_effort"):
            if not isinstance(base[role][key],str):
                raise ValueError(f"{role}.{key} must be a string")
    if type(base["brain"].get("search_enabled")) is not bool:
        raise ValueError("brain.search_enabled must be boolean")
    base["cell"] = _resolve_cell(base)
    runtime = base["runtime"]
    catalog = runtime.get("model_catalog_json", "")
    if not isinstance(catalog,str) or catalog and not Path(catalog).expanduser().is_absolute():
        raise ValueError("runtime.model_catalog_json must be empty or an absolute path string")
    for key in ("cell_prepare_timeout_seconds", "cell_launch_grace_seconds", "audit_start_margin_seconds", "submission_reserve_seconds"):
        if type(runtime.get(key)) is not int or runtime[key] < 1:
            raise ValueError(f"runtime.{key} must be a positive integer")
    fraction=runtime.get("submission_reserve_fraction")
    if type(fraction) not in (int,float) or not 0 < fraction < 1:
        raise ValueError("runtime.submission_reserve_fraction must be between 0 and 1")
    require_current_workflow(base)
    if type(base.get("storage_version")) is not int or base["storage_version"] != 4:
        raise ValueError("New Brain runs require storage_version = 4")
    return base


def requested_mode(store):
    return store.get_meta("research_mode_request", store.get_meta("config", {}).get("research_mode", "generic"))


def effective_mode(store):
    if store.get_meta("config", {}).get("workflow", {}).get("version") == 3:
        return "oracle_complexity"
    decision = store.get_meta("research_routing")
    mode = decision["research_mode"] if decision else requested_mode(store)
    if mode not in MODES:
        raise ValueError("Programme routing must finish before research execution")
    return mode


def initialize_routing(store, requested):
    if requested not in REQUEST_MODES:
        raise ValueError("research_mode must be auto, generic or oracle_complexity")
    original = store.get_meta("research_mode_request")
    if original is not None and original != requested:
        raise ValueError("Programme routing request is already frozen")
    if store.get_meta("research_routing"):
        return
    values = {"research_mode_request": requested}
    if requested != "auto":
        values["research_routing"] = {"research_mode": requested,
            "reason": "Explicit Programme mode selected at initialization.", "source": "explicit"}
    store.set_meta(**values)


from colombo.cell.instructions import MODES
REQUEST_MODES = (*MODES, "auto")
