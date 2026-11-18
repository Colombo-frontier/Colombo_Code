"""Shared path identities and durable file writes for Brain and Cell runtimes.

Stored paths stay ordinary pathlib values. Windows extended paths are applied
only at the I/O boundary; no global pathlib or operating-system patch is used.
"""
from __future__ import annotations

from contextlib import contextmanager
import json
import os
import time
from pathlib import Path as _Path, PurePath
import tempfile


def _display_path(value) -> str:
    value = str(value) if isinstance(value, PurePath) else os.fspath(value)
    if not isinstance(value, str):
        raise TypeError("Paths must be strings or string path-like objects")
    if os.name == "nt":
        if value.startswith("\\\\?\\UNC\\"):
            return "\\\\" + value[8:]
        if value.startswith("\\\\?\\") and len(value) >= 7 and value[5:7] == ":\\":
            return value[4:]
    return value


def io_path(value) -> str:
    """Extend Windows paths for I/O while retaining ordinary stored identities."""
    value = _display_path(value)
    if os.name != "nt" or value.startswith(("\\\\?\\", "\\\\.\\")):
        return value
    absolute = os.path.abspath(value)
    # Recursive APIs may turn the root into a string before walking children.
    # Extend short roots too, since their descendants can exceed MAX_PATH.
    return "\\\\?\\UNC\\" + absolute[2:] if absolute.startswith("\\\\") else "\\\\?\\" + absolute


_ConcretePath = type(_Path())


class Path(_ConcretePath):
    """Normal pathlib identities with extended Windows paths only at I/O."""
    __slots__ = ()

    def __new__(cls, *parts):
        return super().__new__(cls, *(_display_path(part) for part in parts))

    def __init__(self, *parts):
        # Python 3.12 moved pathlib parsing from __new__ into __init__.
        if _ConcretePath.__init__ is not object.__init__:
            super().__init__(*(_display_path(part) for part in parts))

    def __fspath__(self) -> str:
        return io_path(str(self))


def atomic_write(path, data: bytes, *, sync_directory: bool = False) -> None:
    """Replace a file atomically using a short, exclusive temporary sibling."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # A sibling is required for atomic replacement. Do not repeat the possibly
    # long destination filename in the temporary basename.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("wb", dir=io_path(destination.parent),
                                         prefix=".w-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
        temporary = None
        if sync_directory and os.name != "nt":
            descriptor = os.open(destination.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def json_bytes(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                      allow_nan=False).encode("utf-8")


def json_equal(left, right) -> bool:
    """Compare JSON content without Python's bool/number coercion."""
    return json_bytes(left) == json_bytes(right)


def write_json(path: Path, value) -> None:
    atomic_write(path, json_bytes(value))


def freeze_json(path: Path, value) -> None:
    path = Path(path)
    data = json_bytes(value)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f"Immutable file differs: {path}")
        return
    atomic_write(path, data)


def read_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


@contextmanager
def file_lock(path: Path, timeout: float = 30, poll_seconds: float = 0.05):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError("Lock path cannot be a symbolic link")
    with path.open("a+b") as stream:
        deadline = time.monotonic() + timeout
        while True:
            try:
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"Busy: {path}")
                time.sleep(min(poll_seconds, max(0, deadline - time.monotonic())))
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_UN)
