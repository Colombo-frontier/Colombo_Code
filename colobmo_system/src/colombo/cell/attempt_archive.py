"""Versioned full research snapshots, excluding credentials and disposable caches."""
from __future__ import annotations
import hashlib
import json
import os
import zipfile

from colombo.shared.file_io import Path
from colombo.shared.file_io import io_path
from colombo.shared.file_io import freeze_json

EXCLUDED_DIRS = {".git", ".venv", "venv", "__pycache__", ".codex", ".runtime", "node_modules"}
EXCLUDED_FILES = {"auth.json", "apikey.txt", ".env", "credentials.json"}


def research_files(root):
    root = Path(root).resolve()
    for base, dirs, names in os.walk(io_path(root), followlinks=False):
        folder = Path(base)
        for name in list(dirs):
            path = folder / name
            if name in EXCLUDED_DIRS:
                dirs.remove(name)
            elif path.is_symlink() or getattr(path, "is_junction", lambda: False)():
                raise ValueError("Research archive cannot include linked directories")
        for name in sorted(names):
            path = folder / name
            if name in EXCLUDED_FILES or name.endswith((".pyc", ".lock", ".tmp")):
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError("Research archive cannot include linked files")
            if path.is_file():
                yield path


def freeze_attempt_archive(cell, folder, task, add_file):
    cell, folder, task = map(Path, (cell, folder, task))
    for source in sorted(research_files(cell)):
        add_file(source, "research_file")
    artifacts = folder / "artifacts"
    rows = [{"path": p.relative_to(artifacts).as_posix(), "size": p.stat().st_size,
             "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(artifacts.rglob("*")) if p.is_file()]
    name = task.name + "-" + folder.name + ".zip"
    archive = folder / name
    temporary = folder / (name + ".tmp")
    with zipfile.ZipFile(io_path(temporary), "w", compression=zipfile.ZIP_DEFLATED) as output:
        for row in rows:
            output.write(io_path(artifacts / row["path"]), row["path"])
    with zipfile.ZipFile(io_path(temporary)) as checked:
        if checked.testzip() is not None or set(checked.namelist()) != {r["path"] for r in rows}:
            raise ValueError("Attempt archive validation failed")
        for row in rows:
            if hashlib.sha256(checked.read(row["path"])).hexdigest() != row["sha256"]:
                raise ValueError("Attempt archive content differs from its fixed artifact")
    # Never overwrite a published archive, including after an interrupted export.
    if archive.exists():
        with zipfile.ZipFile(io_path(archive)) as old:
            if set(old.namelist()) != {r["path"] for r in rows} or any(
                    hashlib.sha256(old.read(r["path"])).hexdigest() != r["sha256"] for r in rows):
                temporary.unlink()
                raise ValueError("Previously frozen attempt archive differs")
        temporary.unlink()
    else:
        temporary.replace(archive)
    index = folder / "archive_index.json"
    freeze_json(index, {"task_id": task.name, "attempt_id": folder.name,
                       "archive": name, "files": rows})
    metadata = {"path": archive.relative_to(task).as_posix(),
                "index_path": index.relative_to(task).as_posix(),
                "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(), "files": len(rows)}
    extras = [{"path": p.relative_to(task).as_posix(), "size": p.stat().st_size, "kind": kind}
              for p, kind in ((archive, "attempt_archive"), (index, "archive_index"))]
    return metadata, extras
