"""Resolve all paths relative to the configuration file, independently of the caller's working directory."""
from __future__ import annotations

import os
import tomllib
from pathlib import Path


DEFAULTS = {
    "max_input_chars": 60000,
    "max_tool_chars": 12000,
    "max_turns": 50,
    "max_segments": 4,
    "max_protocol_repairs": 2,
    "max_science_revisions": 1,
    "max_total_calls": 160,
    "max_candidates": 12,
    "max_jobs": 80,
    "max_external_calls": 80,
}


def resources_root() -> Path:
    override = os.getenv("ORACLE_ATLAS_RESOURCES")
    if override:
        return Path(override).resolve()
    project = Path(__file__).resolve().parents[3]
    if (project / "agents").is_dir() and (project / "protocol.md").is_file():
        return project
    return Path(__file__).resolve().parents[1] / "resources"


def load_config(path: str | Path) -> dict:
    p = Path(path).resolve()
    with p.open("rb") as stream:
        cfg = tomllib.load(stream)
    cfg["config_path"] = str(p)
    for name, default in (("workspace", "./work"), ("atlas", "./atlas")):
        value = Path(cfg.get(name, default))
        cfg[name] = str((p.parent / value).resolve() if not value.is_absolute() else value)
    cfg["budgets"] = {**DEFAULTS, **cfg.get("budgets", {})}
    if any(not isinstance(v, int) or isinstance(v, bool) or v <= 0 for v in cfg["budgets"].values()):
        raise ValueError("budgets must contain positive integers")
    cfg.setdefault("model", {})
    cfg.setdefault("mcp", [])
    cfg.setdefault("tasks", [])
    return cfg

