"""Bounded, explicit experiment file manifests. Files are data, never executed."""
from __future__ import annotations

from pathlib import PureWindowsPath
from colombo.shared.file_io import Path
import re

from colombo.cell.settings import get_settings


def artifact_path(root: Path, name: str) -> Path:
    root = Path(root).resolve()
    if not isinstance(name, str) or not name or "\\" in name:
        raise ValueError("Experiment artifact paths must use task-relative forward slashes")
    relative = Path(name)
    portable = PureWindowsPath(name)
    if portable.drive or portable.root or relative.is_absolute() or any(
            part in {".", ".."} for part in name.split("/")) or "" in name.split("/"):
        raise ValueError("Experiment artifact path must stay inside the task")
    if relative.parts[0] != "experiments":
        raise ValueError("Experiment artifacts must be inside experiments/")
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            raise ValueError("Experiment artifact paths cannot traverse links")
    if not path.resolve().is_relative_to(root):
        raise ValueError("Experiment artifact path escapes its task")
    return path


def read_artifacts(root: Path, manifest: list[dict], *, settings: dict | None = None) -> dict[str, bytes]:
    """Verify size and content before returning an explicit finite file bundle."""
    limits = (settings or get_settings(root))["experiment"]
    if not isinstance(manifest, list) or len(manifest) > limits["max_files"]:
        raise ValueError("Experiment artifact manifest exceeds max_files or is not a list")
    files, total = {}, 0
    for item in manifest:
        if not isinstance(item, dict) or set(item) != {"path", "size"}:
            raise ValueError("Each experiment artifact needs path and size")
        name, size = item["path"], item["size"]
        path = artifact_path(root, name)
        if name.casefold() in {p.casefold() for p in files}:
            raise ValueError("Duplicate experiment artifact path")
        if type(size) is not int or size < 0 or size > limits["artifact_max_bytes"]:
            raise ValueError("Experiment artifact exceeds artifact_max_bytes or has invalid size")
        total += size
        if total > limits["max_total_artifact_bytes"]:
            raise ValueError("Experiment artifacts exceed max_total_artifact_bytes")
        if not path.is_file() or path.stat().st_size != size:
            raise ValueError(f"Experiment artifact missing or size changed: {name}")
        with path.open("rb") as handle:
            data = handle.read(size + 1)
        if len(data) != size:
            raise ValueError(f"Experiment artifact size changed: {name}")
        files[name] = data
    return files


def copy_artifacts(destination: Path, files: dict[str, bytes]) -> None:
    """Copy verified bytes without executing them or overwriting different data."""
    for name, data in files.items():
        path = artifact_path(destination, name)
        if path.exists():
            if path.read_bytes() != data:
                raise ValueError(f"Experiment artifact destination has different content: {name}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation prevents replacing a concurrent writer's files.
        with path.open("xb") as handle:
            handle.write(data)


def experiment_group(payload: dict) -> dict:
    return {"artifacts": payload.get("artifacts"), "limits": payload["execution"].get("artifact_limits")}


def read_artifact_groups(root: Path, groups: list[dict], *, settings: dict | None = None) -> dict[str, bytes]:
    """Per-experiment limits apply separately; conflicting shared paths are rejected."""
    files = {}
    settings = settings or get_settings(root)
    for group in groups:
        active = settings
        if group.get("limits") is not None:
            limits = group["limits"]
            names = {"artifact_max_bytes", "max_total_artifact_bytes", "max_files"}
            if not isinstance(limits, dict) or set(limits) != names or any(
                    type(value) is not int or value < 1 for value in limits.values()) or \
                    limits["artifact_max_bytes"] > limits["max_total_artifact_bytes"]:
                raise ValueError("Invalid immutable experiment artifact limits")
            active = {**settings, "experiment": {**settings["experiment"], **limits}}
        for name, data in read_artifacts(root, group["artifacts"], settings=active).items():
            if name in files and files[name] != data:
                raise ValueError("Selected experiment manifests disagree about an artifact")
            files[name] = data
    return files


def manifest_for(files: dict[str, bytes]) -> list[dict]:
    return [{"path": name, "size": len(data)}
            for name, data in sorted(files.items())]
