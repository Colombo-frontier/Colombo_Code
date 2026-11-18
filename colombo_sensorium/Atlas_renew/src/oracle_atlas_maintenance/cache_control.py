"""Cross-process serialization for the shared literature cache, without read credit.

The native MCP servers are separate processes even when the controller uses a
thread pool. All cache operations take the same filesystem lock. arXiv requests
also take a provider lock first and record their start only after the cache lock
has been acquired. Neither lock, nor a cache hit, grants another stage evidence.
"""
from __future__ import annotations

from contextlib import contextmanager
import fcntl
import json
import math
import os
from pathlib import Path
import stat
import time
from urllib.parse import urlsplit

from oracle_atlas.discovery.http import atomic_write

from .telemetry import read_run_control


CACHE_OPERATIONS = frozenset({"bibliography_search", "bibliography_read", "bibliography_lookup", "search_replace",
                              "source_fetch", "source_read", "source_find"})
_NETWORK_OPERATIONS = frozenset({"bibliography_search", "bibliography_lookup", "source_fetch"})
_POLL_SECONDS = 0.02


class CacheWaitAborted(RuntimeError):
    """The current stage must close instead of waiting for shared research I/O."""


def _check_control(path, *, closing=False):
    if path is None:
        return
    value = read_run_control(path)
    if not value.get("available"):
        raise CacheWaitAborted("Stage control is unavailable; shared-cache work was not started")
    if value.get("hard_expired") or (closing and value.get("close_requested")):
        raise CacheWaitAborted("Stage is closing; shared-cache wait or new research was stopped")


def _lock_path(root, name):
    directory = root / ".cache-control"
    if directory.is_symlink():
        raise ValueError("Cache control directory must not be a symbolic link")
    directory.mkdir(parents=True, exist_ok=True)
    if not directory.is_dir() or directory.resolve().parent != root:
        raise ValueError("Cache control directory escapes the cache root")
    path = directory / name
    if path.is_symlink():
        raise ValueError("Cache control file must not be a symbolic link")
    return path


@contextmanager
def _locked(path, control):
    flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    acquired = False
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError("Cache control lock must be a regular file")
        while True:
            _check_control(control)
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
                break
            except BlockingIOError:
                _check_control(control, closing=True)
                time.sleep(_POLL_SECONDS)
        yield
    finally:
        if acquired:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _arxiv_operation(name, arguments):
    if name == "bibliography_search":
        return arguments.get("provider") == "arxiv"
    if name == "bibliography_lookup":
        if arguments.get("kind") == "arxiv":
            return True
        if arguments.get("kind") != "url":
            return False
        host = urlsplit(arguments.get("identifier", "")).hostname
        return isinstance(host, str) and (host == "arxiv.org" or host.endswith(".arxiv.org"))
    if name != "source_fetch":
        return False
    host = urlsplit(arguments.get("url", "")).hostname
    return isinstance(host, str) and (host == "arxiv.org" or host.endswith(".arxiv.org"))


def _interval(config):
    value = config.get("literature", {}).get("arxiv_interval", 3.0)
    if isinstance(value, bool):
        raise ValueError("arxiv_interval must be a finite nonnegative number")
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError("arxiv_interval must be a finite nonnegative number")
    return result


def _wait_provider(path, interval, control):
    last = 0
    if path.exists():
        if path.is_symlink() or not path.is_file():
            raise ValueError("Provider timestamp must be a regular non-symlink file")
        value = json.loads(path.read_text("utf-8"))
        last = value.get("last_start_monotonic_ns")
        if type(last) is not int or last < 0:
            raise ValueError("Invalid shared provider timestamp")
    now = time.monotonic_ns()
    # Monotonic timestamps do not survive a host reboot. An old future timestamp
    # cannot impose an unbounded delay in the new boot's monotonic clock domain.
    if last > now:
        last = 0
    end = last + int(interval * 1e9)
    while True:
        _check_control(control, closing=True)
        remaining = (end - time.monotonic_ns()) / 1e9
        if remaining <= 0:
            return
        time.sleep(min(_POLL_SECONDS, remaining))


@contextmanager
def cache_operation(cache_dir, name, arguments, config, *, run_control_path=None,
                    network_needed=None):
    """Guard one existing cache operation; do not execute it or change its result.

    ``run_control_path`` is the current role's controller-provided control file.
    Waiting is cooperative and checked in short intervals. An immediate local
    read remains allowed during the soft close reserve; queued work can abort,
    and no new network operation starts after close is requested.

    ``network_needed`` may be a pure cache-validity callback. For arXiv it is
    evaluated under both locks, so another process cannot replace the checked
    cache entry before the operation. Only an exact False skips rate waiting and
    timestamp updates; the cache mutex and original stage accounting remain.
    """
    if name not in CACHE_OPERATIONS:
        yield
        return
    network = name in _NETWORK_OPERATIONS
    _check_control(run_control_path, closing=network)
    root = Path(cache_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    cache_lock = _lock_path(root, "cache.lock")
    if _arxiv_operation(name, arguments):
        provider_lock = _lock_path(root, "arxiv.lock")
        timestamp = _lock_path(root, "arxiv-start.json")
        interval = _interval(config)
        # A single lock order everywhere: provider, then global cache.
        with _locked(provider_lock, run_control_path):
            with _locked(cache_lock, run_control_path):
                _check_control(run_control_path, closing=True)
                needed = True if network_needed is None else network_needed()
                if type(needed) is not bool:
                    raise ValueError("Network-needed callback must return a bool")
                if needed:
                    _wait_provider(timestamp, interval, run_control_path)
                    atomic_write(timestamp, (json.dumps({"last_start_monotonic_ns": time.monotonic_ns()}) + "\n").encode())
                yield
    else:
        with _locked(cache_lock, run_control_path):
            _check_control(run_control_path, closing=network)
            yield
