"""Resolve the adjacent Atlas build root and reject root/symlink substitution."""
import os
from pathlib import Path


def checked_root(requested, expected):
    raw = Path(os.path.abspath(requested))
    expected = Path(expected).resolve()
    if raw.resolve() != expected:
        raise ValueError("The public builder writes only the Atlas adjacent to its source")
    for candidate in (raw, *raw.parents):
        if candidate.is_symlink():
            raise ValueError("A symlink cannot select the public build root")
    if not (raw / "data/settings").is_dir() or not (raw / "visualization/src").is_dir():
        raise ValueError("Missing adjacent Atlas data/source tree")
    for candidate in raw.rglob("*"):
        if candidate.is_symlink():
            raise ValueError("Symlink input/output is not a public build authority: " + str(candidate.relative_to(raw)))
    return expected
