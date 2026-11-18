"""Native Atlas five-file adaptation and single-writer transactions.

The program checks format, references, review scope, and versions; mathematical conclusions come only from frozen independent LLM reviews.
Commit first persists all new files and the journal, then atomically replaces each file. All component reads hold the lock;
after interruption, recovery can only roll forward from that journal. It neither repeats model calls nor overwrites unrecognized external changes.
"""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import time
from typing import Any, Iterator
from urllib.parse import urljoin, urlparse

from .tags import AXES, TagError, at, canonical_bytes, digest, facts_from_sidecars, inherit_unchanged_facts, json_bytes, project_tags

FILES = ("profile.json", "identity.json", "classification.json", "human_tags.json", "machine_tags.json")
DERIVED_VOCABULARY = {"browse_facets.json", "browse_index.json", "catalog.json"}
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,159}$")


class AtlasError(ValueError):
    """An operational Atlas error; it never indicates a mathematical error in a paper."""


class AtlasConflict(AtlasError):
    """The frozen baseline has changed; the affected identity or update must be rechecked first."""


class AtlasValidationError(AtlasError):
    """An interface or material-binding error that can be returned to the producing Agent for revision."""

    def __init__(self, message: str, diagnostics: list[dict] | None = None):
        super().__init__(message)
        self.diagnostics = diagnostics or [{"code": "atlas_validation", "message": message}]


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_id(value: str) -> str:
    if not isinstance(value, str) or not SAFE_ID.fullmatch(value) or value in {".", ".."}:
        raise AtlasValidationError(f"Invalid setting_id: {value!r}")
    return value


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise AtlasValidationError(f"Cannot read JSON: {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise AtlasValidationError(f"The top-level file value must be an object: {path.name}")
    return value


def _fsync_dir(path: Path) -> None:
    if os.name != "posix":
        return
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _atomic(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".tmp-{os.getpid()}-{time.time_ns()}")
    try:
        with temporary.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        _fsync_dir(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def _merge_unmanaged(old: dict, fresh: dict) -> dict:
    """Replace projector-owned fields in full; preserve unknown extension fields."""
    value = deepcopy(old)
    value.update(deepcopy(fresh))
    return value


class Atlas:
    """An Atlas adapter compatible with the five files under ``data/settings/<setting_id>/``."""

    def __init__(self, root: str | Path, lock_timeout: float = 30.0):
        self.root = Path(root).expanduser().resolve()
        self.data = self.root / "data"
        if (self.root / "settings").exists() and not self.data.exists():
            self.data = self.root
        self.settings = self.data / "settings"
        self.state = self.data / "intake" / "oracle_atlas_agents"
        self.settings.mkdir(parents=True, exist_ok=True)
        self.state.mkdir(parents=True, exist_ok=True)
        self.lock_timeout = lock_timeout
        self._catalog_cache: tuple[str, list[dict]] | None = None
        self.recover()

    @contextmanager
    def _lock(self) -> Iterator[None]:
        # Reuse the existing Atlas write-lock location so old and new writers also serialize during upgrades.
        path = self.data / "intake" / "oracle_scout" / "write.lock"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a+b") as handle:
            started = time.monotonic()
            if os.name == "nt":
                import msvcrt
                if path.stat().st_size == 0:
                    handle.write(b"\0")
                    handle.flush()
                while True:
                    try:
                        handle.seek(0)
                        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                        break
                    except OSError:
                        if time.monotonic() - started >= self.lock_timeout:
                            raise AtlasConflict("Timed out waiting for the Atlas write lock")
                        time.sleep(0.05)
                try:
                    yield
                finally:
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                while True:
                    try:
                        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                        break
                    except BlockingIOError:
                        if time.monotonic() - started >= self.lock_timeout:
                            raise AtlasConflict("Timed out waiting for the Atlas write lock")
                        time.sleep(0.05)
                try:
                    yield
                finally:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def _path(self, sid: str, filename: str) -> Path:
        _safe_id(sid)
        if filename not in FILES:
            raise AtlasValidationError("Only the five native Atlas file types may be read")
        path = self.settings / sid / filename
        if not path.resolve().is_relative_to(self.settings.resolve()):
            raise AtlasValidationError("Setting path escapes the allowed directory")
        return path

    def _hash_file(self, path: Path) -> str | None:
        return _sha(path.read_bytes()) if path.is_file() else None

    def _target_version(self, sid: str) -> str | None:
        hashes = {name: self._hash_file(self._path(sid, name)) for name in FILES}
        return "target-" + digest(hashes) if any(hashes.values()) else None

    def _science_files(self) -> list[Path]:
        files = []
        for directory in sorted(self.settings.iterdir()):
            if not directory.is_dir() or not SAFE_ID.fullmatch(directory.name):
                continue
            for name in FILES:
                path = self._path(directory.name, name)
                if path.is_file():
                    files.append(path)
        for folder in ("schemas", "registry", "vocabulary"):
            schema_paths = (self.data / folder).rglob("*.json") if folder == "schemas" else (self.data / folder).glob("*.json")
            for path in sorted(schema_paths):
                if folder == "vocabulary" and path.name in DERIVED_VOCABULARY:
                    continue
                if not path.resolve().is_relative_to(self.root):
                    raise AtlasValidationError("Scientific vocabulary or schema path escapes the allowed directory")
                files.append(path)
        for path in sorted(self.data.glob("aliases*.json")):
            files.append(path)
        return files

    def _inventory_version(self) -> str:
        return "inventory-v2-" + digest({p.relative_to(self.root).as_posix(): self._hash_file(p) for p in self._science_files()})

    def _semantics_version(self) -> str:
        files = [p for p in self._science_files() if not p.is_relative_to(self.settings)]
        return digest({p.relative_to(self.root).as_posix(): self._hash_file(p) for p in files})

    def _check_other_writers(self) -> None:
        # Incomplete transactions from the old component must first be recovered with that component; they must not compete with a new writer.
        old_pending = self.data / "intake" / "oracle_scout" / "pending.json"
        if old_pending.exists():
            raise AtlasConflict("The old Oracle Scout has an incomplete transaction; recover it using the old component first")

    def read(self, setting_id: str, filename: str = "profile.json") -> dict:
        with self._lock():
            self._recover_locked()
            self._check_other_writers()
            return _read_json(self._path(setting_id, filename))

    def version(self, setting_id: str | None = None) -> str | None:
        """Return the version of one setting or the scientific inventory; return None for a nonexistent setting."""
        with self._lock():
            self._recover_locked()
            self._check_other_writers()
            return self._target_version(setting_id) if setting_id is not None else self._inventory_version()

    def review_snapshot(self, setting_id, expected_version, *, research_context):
        """Freeze a read-only five-file snapshot for a new no-change review."""
        with self._lock():
            self._recover_locked()
            self._check_other_writers()
            actual = self._target_version(setting_id)
            if actual is None or actual != expected_version:
                raise AtlasConflict("The no-change baseline changed; research must be repeated")
            files = {name: _read_json(self._path(setting_id, name)) for name in FILES}
            profile = files["profile.json"]
            self._validate_files(files, baseline=profile, research_context=research_context)
            from ..science.gates import freeze_science_context
            science = freeze_science_context(profile, baseline=profile, research_context=research_context)
            hashes = {name: _sha(json_bytes(files[name])) for name in FILES}
            return {"setting_id": setting_id, "files": files, "base_version": actual,
                    "version": "target-" + digest(hashes), "hashes": hashes,
                    "bundle_hash": digest(files), "inventory_version": self._inventory_version(),
                    "semantics_version": self._semantics_version(),
                    "science": science, "science_hash": digest(science), "read_only": True}

    def vocabulary(self) -> dict:
        with self._lock():
            self._recover_locked()
            return self._vocabulary()

    def _vocabulary(self) -> dict:
        result = {}
        for key, filename in (("human", "human_tags.json"), ("machine", "machine_tags.json")):
            path = self.data / "vocabulary" / filename
            if path.exists():
                result[key] = _read_json(path)
        return result

    def catalog(self) -> list[dict]:
        """A compact retrieval catalog; it does not load research prose or the full set of identity-exclusion proofs."""
        with self._lock():
            self._recover_locked()
            self._check_other_writers()
            version = self._inventory_version()
            if self._catalog_cache and self._catalog_cache[0] == version:
                return deepcopy(self._catalog_cache[1])
            result = []
            for path in sorted(self.settings.glob("*/profile.json")):
                sid = _safe_id(path.parent.name)
                diagnostics = []
                try:
                    profile = _read_json(self._path(sid, "profile.json"))
                except AtlasValidationError as exc:
                    result.append({"setting_id": sid, "title": sid, "profile_version": self._target_version(sid), "tag_facts": [], "unknown_axes": list(AXES), "aliases": [], "diagnostics": [str(exc)]})
                    continue
                sidecars = {}
                for name in ("machine_tags.json", "classification.json"):
                    other = self._path(sid, name)
                    if other.exists():
                        try:
                            sidecars[name] = _read_json(other)
                        except AtlasValidationError as exc:
                            diagnostics.append(str(exc))
                facts = facts_from_sidecars(profile, sidecars.get("machine_tags.json"), sidecars.get("classification.json"))
                # Native legacy tags with mismatched hashes remain weak retrieval signals, but cannot establish matched status.
                machine_hash = sidecars.get("machine_tags.json", {}).get("profile_sha256")
                if machine_hash and machine_hash != digest(profile):
                    diagnostics.append("The machine_tags profile hash is stale; use only as a weak retrieval signal")
                    for fact in facts:
                        fact["status"] = "unknown"
                known_axes = {f["axis"] for f in facts if f.get("status") == "known"}
                aliases = []
                for row in profile.get("aliases", []):
                    if isinstance(row, dict):
                        alias = row.get("legacy_id", row.get("alias_id"))
                        if isinstance(alias, str):
                            aliases.append(alias)
                    elif isinstance(row, str):
                        aliases.append(row)
                for view in profile.get("views", []):
                    aliases.extend(x for x in view.get("alias_ids", []) if isinstance(x, str))
                task = profile.get("common_specification", {}).get("task", {})
                task_text = " ".join(str(task.get(k, "")) for k in ("summary", "formulation", "formulation_code", "solution_goal", "description_paragraphs")) if isinstance(task, dict) else ""
                result.append({"setting_id": sid, "title": profile.get("title", sid), "profile_version": self._target_version(sid), "tag_facts": facts, "unknown_axes": [a for a in AXES if a not in known_axes], "primary_domain": profile.get("primary_domain"), "task_text": task_text[:1800], "view_ids": [v.get("view_id") for v in profile.get("views", [])], "aliases": sorted(set(aliases)), "diagnostics": diagnostics})
            self._catalog_cache = (version, result)
            return deepcopy(result)

    def _validate_files(self, files: dict, *, baseline=None, research_context=None) -> None:
        if not isinstance(files, dict) or set(files) != set(FILES) or any(not isinstance(files[n], dict) for n in FILES):
            raise AtlasValidationError("prepare must contain exactly five native JSON objects")
        profile = files["profile.json"]
        sid = _safe_id(profile.get("setting_id"))
        from .target_schema import validate_target_files
        from .sidecars import validate_sidecars
        diagnostics = validate_target_files(files, self.data)
        from ..science.gates import profile_contract_errors
        diagnostics.extend(profile_contract_errors(profile, baseline=baseline, research_context=research_context))
        for name, value in files.items():
            if value.get("setting_id") != sid:
                diagnostics.append({"code": "setting_id_mismatch", "file": name, "path": "/setting_id", "message": f"{name} setting_id mismatch"})
        pretty, canonical = _sha(json_bytes(profile)), digest(profile)
        for name in ("identity.json", "classification.json"):
            if files[name].get("profile_sha256") != pretty:
                diagnostics.append({"code": "profile_hash", "file": name, "message": f"{name} profile byte-hash binding is incorrect"})
        for name in ("human_tags.json", "machine_tags.json"):
            if files[name].get("profile_sha256") != canonical:
                diagnostics.append({"code": "profile_hash", "file": name, "message": f"{name} profile canonical-JSON hash binding is incorrect"})
        if files["machine_tags.json"].get("source_classification_profile_sha256") != pretty:
            diagnostics.append({"code": "classification_hash", "file": "machine_tags.json", "message": "The machine_tags classification binding is incorrect"})
        try:
            _validate_profile_bindings(profile)
        except (AtlasValidationError, KeyError, TypeError, IndexError) as exc:
            diagnostics.extend(getattr(exc, "diagnostics", [{"code": "profile_shape", "message": str(exc)}]))
        diagnostics.extend(validate_sidecars(files, self._vocabulary()))
        if diagnostics:
            raise AtlasValidationError("Five-file validation failed: \n" + "\n".join(d.get("message", str(d)) for d in diagnostics), diagnostics)

    def preflight(self, profile: dict, tag_facts: list, expected_version: str | None = None, *, research_context=None) -> dict:
        """Perform a full preflight without writing the five files. Multiple revisions are allowed within the same Agent session."""
        try:
            prepared = self.prepare(profile, tag_facts, expected_version, research_context=research_context)
            return {"valid": True, "errors": [], "prepared": prepared}
        except AtlasValidationError as exc:
            return {"valid": False, "errors": exc.diagnostics}
        except AtlasConflict as exc:
            return {"valid": False, "errors": [{"code": "atlas_conflict", "message": str(exc)}]}

    def prepare(self, profile: dict, tag_facts: list, expected_version: str | None = None, *, research_context=None) -> dict:
        """Create a five-file snapshot for review; do not write to Atlas or automatically replace an existing setting identity."""
        with self._lock():
            self._recover_locked()
            self._check_other_writers()
            profile = deepcopy(profile)
            sid = _safe_id(profile.get("setting_id"))
            actual = self._target_version(sid)
            if actual != expected_version:
                raise AtlasConflict(f"{sid} baseline mismatch: expected={expected_version!r}, actual={actual!r}")
            old = {}
            if actual is not None:
                old = {name: (_read_json(self._path(sid, name)) if self._path(sid, name).exists() else {}) for name in FILES}
                previous = old["profile.json"]
                if not previous:
                    raise AtlasValidationError("An existing setting lacks profile.json; recover the original transaction first. Sidecars cannot be used to invent a scientific specification")
                # Preserve additional top-level metadata; express removal from scientific arrays through explicit withdrawn entries.
                profile = _merge_unmanaged(previous, profile)
                for field, key in (("views", "view_id"), ("bounds", "id")):
                    before = {row.get(key, row.get("bound_id")) for row in previous.get(field, []) if isinstance(row, dict)}
                    after = {row.get(key, row.get("bound_id")) for row in profile.get(field, []) if isinstance(row, dict)}
                    if not before.issubset(after):
                        raise AtlasValidationError(f"Updates must not discard existing {field} IDs; preserve them and explicitly mark them withdrawn or invalid")
                old_aliases = {digest(a) for a in previous.get("aliases", [])}
                new_aliases = {digest(a) for a in profile.get("aliases", [])}
                if not old_aliases.issubset(new_aliases):
                    raise AtlasValidationError("Updates must not lose existing ID aliases")
            from .target_schema import adapt_profile, validate_profile_target
            from .bindings import normalize_tag_facts
            adapted = adapt_profile(profile, self.data, previous=old.get("profile.json"))
            profile = adapted["profile"]
            normalized = normalize_tag_facts(profile, tag_facts)
            diagnostics = list(normalized["errors"]) + validate_profile_target(profile, self.data) + comparison_binding_errors(profile)
            from ..science.gates import profile_contract_errors, freeze_science_context
            diagnostics.extend(profile_contract_errors(profile, baseline=old.get("profile.json"), research_context=research_context))
            if diagnostics:
                raise AtlasValidationError("Profile/tag preflight failed: \n" + "\n".join(d.get("message", str(d)) for d in diagnostics), diagnostics)
            tag_facts = normalized["facts"]
            # The content-addressed store round-trips through canonical JSON. Fix field order first so the pretty-printed byte hash
            # does not change with dictionary insertion order across prepare → archive → review → commit.
            profile = json.loads(canonical_bytes(profile))
            try:
                combined_facts, inheritance = inherit_unchanged_facts(
                    old.get("profile.json", {}), profile,
                    old.get("machine_tags.json", {}), old.get("classification.json", {}), tag_facts)
                projections = project_tags(profile, combined_facts, self._vocabulary())
            except TagError as exc:
                raise AtlasValidationError(str(exc)) from exc
            files = {"profile.json": profile}
            for kind, value in projections.items():
                name = kind + ".json"
                files[name] = _merge_unmanaged(old.get(name, {}), value)
            files = json.loads(canonical_bytes(files))
            self._validate_files(files, baseline=old.get("profile.json"), research_context=research_context)
            hashes = {name: _sha(json_bytes(files[name])) for name in FILES}
            science = freeze_science_context(profile, baseline=old.get("profile.json"), research_context=research_context)
            return {"setting_id": sid, "files": files, "base_version": actual, "version": "target-" + digest(hashes), "bundle_hash": digest(files), "inventory_version": self._inventory_version(), "semantics_version": self._semantics_version(), "hashes": hashes, "tag_inheritance": inheritance, "binding_normalization": normalized["changes"], "schema_adaptation": adapted["changes"], "science": science, "science_hash": digest(science)}

    def validate_review(self, prepared: dict, review: dict) -> None:
        """A mechanical adoption check without writes; the controller invokes the same boundary before caching a review handoff.

        Check only the fixed five files, explicit adoption status, and item-by-item approvals. Do not turn every quarantined concern in the document
        into a publication blocker. Baseline conflicts are handled separately under the lock during the actual commit.
        """
        if not isinstance(prepared, dict) or not isinstance(review, dict):
            raise AtlasValidationError("prepared / review must be objects")
        sid = _safe_id(prepared.get("setting_id"))
        files = prepared.get("files")
        science = prepared.get("science", {})
        self._validate_files(files, baseline=science.get("baseline_profile"), research_context=science.get("research_context"))
        from ..science.gates import validate_joint_review
        try:
            validate_joint_review(review, prepared)
        except (ValueError, KeyError, TypeError) as exc:
            raise AtlasValidationError("The exact science review is invalid: " + str(exc), getattr(exc, "diagnostics", None)) from exc
        if files["profile.json"]["setting_id"] != sid:
            raise AtlasValidationError("prepared setting_id does not match the frozen profile")
        bundle_hash = digest(files)
        if prepared.get("bundle_hash") != bundle_hash:
            raise AtlasValidationError("The pending-write snapshot was modified after freezing")
        hashes = {name: _sha(json_bytes(files[name])) for name in FILES}
        if prepared.get("hashes") != hashes or prepared.get("version") != "target-" + digest(hashes):
            raise AtlasValidationError("Pending-write file hashes or target version do not match")
        if review.get("verdict") != "approve":
            raise AtlasValidationError("Adoption requires an independent review with approve status")
        if review.get("prepared_hash") is not None and review["prepared_hash"] != bundle_hash:
            raise AtlasValidationError("The review is bound to a different five-file snapshot")
        active = _active_bounds(files["profile.json"])
        approved = review.get("approved_bound_ids", [])
        if not isinstance(approved, list) or any(not isinstance(x, str) for x in approved):
            raise AtlasValidationError("approved_bound_ids must be a list of strings")
        if not active.issubset(set(approved)):
            raise AtlasValidationError("Active bounds lack individual approval: " + ", ".join(sorted(active - set(approved))))
        bound_ids = _ids(files["profile.json"]["bounds"], "bound_id", "id")
        if not set(approved).issubset(bound_ids):
            raise AtlasValidationError("approved_bound_ids contains bounds that do not belong to this profile")
        inactive = {b.get("id", b.get("bound_id")) for b in files["profile.json"]["bounds"] if _ineligible(b)}
        if set(approved) & inactive:
            raise AtlasValidationError("approved_bound_ids cannot adopt bounds still explicitly quarantined, withdrawn, or marked inapplicable")
        for issue in review.get("issues", []):
            if isinstance(issue, dict) and "publication" in issue.get("blocks", []):
                raise AtlasValidationError("The review still contains publication blockers")

    def commit(self, prepared: dict, review: dict, idempotency_key: str) -> dict:
        """Adopt a snapshot after its fixed review; raw LLM output cannot directly invoke this method to bypass review."""
        if isinstance(prepared, dict) and prepared.get("read_only"):
            raise AtlasValidationError("A no-change review snapshot is read-only and cannot be published")
        if not isinstance(idempotency_key, str) or not idempotency_key or len(idempotency_key) > 500:
            raise AtlasValidationError("idempotency_key must contain 1–500 characters")
        key_hash = _sha(idempotency_key.encode("utf-8"))
        with self._lock():
            self._recover_locked()
            self._check_other_writers()
            self.validate_review(prepared, review)
            sid, files = prepared["setting_id"], prepared["files"]
            bundle_hash, hashes, version = prepared["bundle_hash"], prepared["hashes"], prepared["version"]
            active = _active_bounds(files["profile.json"])
            request_hash = digest({"bundle_hash": bundle_hash, "review": review, "base_version": prepared.get("base_version")})
            receipt_path = self.state / "receipts" / (key_hash + ".json")
            if receipt_path.exists():
                receipt = _read_json(receipt_path)
                if receipt["request_hash"] != request_hash:
                    raise AtlasConflict("The same idempotency key cannot be used for different snapshots or reviews")
                return receipt
            if self._target_version(sid) != prepared.get("base_version"):
                raise AtlasConflict("The target setting changed during review; the differences require rechecking")
            if prepared.get("base_version") is not None:
                current_profile = _read_json(self._path(sid, "profile.json"))
                if digest(current_profile) != prepared["science"].get("baseline_hash"):
                    raise AtlasConflict("The scientific baseline in the prepared context does not match the actual target")
            if self._semantics_version() != prepared.get("semantics_version"):
                raise AtlasConflict("The target schema, vocabulary, or alias definitions changed during review")
            if prepared.get("base_version") is None and self._inventory_version() != prepared.get("inventory_version"):
                raise AtlasConflict("The Atlas catalog for the new setting changed after identity review; duplicate checking must be repeated")
            txid = request_hash
            transaction = self.state / "transactions" / txid
            for name in FILES:
                _atomic(transaction / "new" / name, json_bytes(files[name]))
            journal = {"transaction_id": txid, "setting_id": sid, "key_hash": key_hash, "request_hash": request_hash, "base_version": prepared.get("base_version"), "version": version, "bundle_hash": bundle_hash, "created_at": _now(), "state": "prepared", "files": {name: {"old_sha256": self._hash_file(self._path(sid, name)), "new_sha256": hashes[name]} for name in FILES}, "review_subject_ref": review.get("subject_ref"), "approved_bound_ids": sorted(active)}
            _atomic(transaction / "journal.json", json_bytes(journal))
            # The marker must exist only after all new files and the journal are durable.
            _atomic(self.state / "pending.json", json_bytes({"transaction_id": txid}))
            return self._finish_transaction(journal)

    def _finish_transaction(self, journal: dict) -> dict:
        sid, txid = journal["setting_id"], journal["transaction_id"]
        transaction = self.state / "transactions" / txid
        for name in FILES:
            detail = journal["files"][name]
            path = self._path(sid, name)
            current = self._hash_file(path)
            if current not in {detail["old_sha256"], detail["new_sha256"]}:
                raise AtlasConflict(f"External modification detected during recovery: {sid}/{name}; the journal has been preserved")
            new = transaction / "new" / name
            if not new.is_file() or self._hash_file(new) != detail["new_sha256"]:
                raise AtlasValidationError(f"Transaction source file is corrupt: {name}; recovery stopped")
        for name in FILES:
            path = self._path(sid, name)
            if self._hash_file(path) != journal["files"][name]["new_sha256"]:
                _atomic(path, (transaction / "new" / name).read_bytes())
        if self._target_version(sid) != journal["version"]:
            raise AtlasValidationError("The five file versions do not match after writing")
        receipt = {"receipt_id": "atlas-" + txid[:24], "setting_id": sid, "request_hash": journal["request_hash"], "bundle_hash": journal["bundle_hash"], "base_version": journal.get("base_version"), "version": journal["version"], "files": {name: detail["new_sha256"] for name, detail in journal["files"].items()}, "review_subject_ref": journal.get("review_subject_ref"), "approved_bound_ids": journal["approved_bound_ids"], "committed_at": _now(), "status": "committed"}
        receipt_path = self.state / "receipts" / (journal["key_hash"] + ".json")
        if receipt_path.exists():
            existing = _read_json(receipt_path)
            if existing.get("request_hash") != journal["request_hash"]:
                raise AtlasConflict("The existing receipt does not match the transaction")
            receipt = existing
        else:
            _atomic(receipt_path, json_bytes(receipt))
        journal["state"] = "committed"
        _atomic(transaction / "journal.json", json_bytes(journal))
        (self.state / "pending.json").unlink(missing_ok=True)
        _fsync_dir(self.state)
        self._catalog_cache = None
        return receipt

    def _recover_locked(self) -> dict | None:
        pending = self.state / "pending.json"
        if not pending.exists():
            return None
        txid = _read_json(pending).get("transaction_id")
        if not isinstance(txid, str) or not re.fullmatch(r"[0-9a-f]{64}", txid):
            raise AtlasValidationError("Invalid transaction ID for recovery")
        journal = _read_json(self.state / "transactions" / txid / "journal.json")
        if journal.get("transaction_id") != txid:
            raise AtlasValidationError("journal and pending do not match")
        return self._finish_transaction(journal)

    def recover(self) -> dict | None:
        with self._lock():
            return self._recover_locked()


def _ids(rows: Any, *fields: str) -> set[str]:
    if not isinstance(rows, list):
        raise AtlasValidationError("The scientific record collection must be a list")
    found = []
    for row in rows:
        if not isinstance(row, dict):
            raise AtlasValidationError("A scientific record must be an object")
        values = [row[k] for k in fields if k in row]
        if not values or any(value != values[0] for value in values) or not isinstance(values[0], str) or not values[0]:
            raise AtlasValidationError(f"The record lacks a consistent ID: {'/'.join(fields)}")
        found.append(values[0])
    if len(set(found)) != len(found):
        raise AtlasValidationError(f"Duplicate ID: {'/'.join(fields)}")
    return set(found)


def _local_schema_registry(directory: Path):
    """Register resources only from the schemas directory; unknown URIs never trigger network downloads.

    File URIs provide base URIs for relative $ref values. Existing absolute $id values are also registered; relative references in the same file tree
    can resolve within that declared URI namespace without requiring an $id in every common file.
    """
    from referencing import Registry, Resource
    from referencing.exceptions import NoSuchResource
    from referencing.jsonschema import DRAFT202012

    root = directory.resolve()
    contents, resources, sources = {}, {}, {}

    def deny_remote(uri):
        raise NoSuchResource(ref=uri)

    def register(uri, resource, source):
        if uri in sources and sources[uri] != source:
            raise AtlasValidationError(f"Schema URI points to multiple local files: {uri}")
        resources[uri], sources[uri] = resource, source

    paths = sorted(directory.rglob("*.json"))
    basename_count = {p.name: sum(q.name == p.name for q in paths) for p in paths}
    for path in paths:
        path = path.resolve()
        if not path.is_relative_to(root):
            raise AtlasValidationError("Schema symbolic links must not point outside the schemas directory")
        data = _read_json(path)
        data.setdefault("$id", path.as_uri())
        try:
            resource = Resource.from_contents(data, default_specification=DRAFT202012)
        except Exception as exc:
            raise AtlasValidationError(f"Cannot register local schema: {path.name}: {exc}") from exc
        uri = path.as_uri()
        contents[uri] = data
        register(uri, resource, uri)
        register(path.relative_to(root).as_posix(), resource, uri)
        if basename_count[path.name] == 1:
            register(path.name, resource, uri)
        declared = data.get("$id")
        if isinstance(declared, str):
            register(urljoin(uri, declared), resource, uri)
    # Map declared hierarchical URIs to the same read-only file tree; never contact the server at that URI.
    for path in paths:
        path = path.resolve()
        base = contents[path.as_uri()].get("$id")
        if not isinstance(base, str) or urlparse(base).scheme not in {"http", "https", "file"}:
            continue
        for target in paths:
            target = target.resolve()
            relative = Path(os.path.relpath(target, path.parent)).as_posix()
            register(urljoin(base, relative), resources[target.as_uri()], target.as_uri())
    return Registry(retrieve=deny_remote).with_resources(resources.items()), contents


def comparison_binding_errors(profile: dict) -> list[dict]:
    """Check only explicit comparison keys; do not infer views, guarantees, or parameter regions from explanatory prose."""
    errors = []
    fields = (("views", "view_id"), ("quantities", "quantity_id", "id"),
              ("resource_projections", "resource_projection_id", "projection_id", "id"),
              ("regimes", "regime_id", "region_id", "id"))
    choices = {"setting_id": {profile.get("setting_id")}}
    for rows, *aliases in fields:
        try:
            values = _ids(profile.get(rows, []), *aliases)
        except (AtlasValidationError, TypeError) as exc:
            errors.append({"code": "profile_id", "file": "profile.json", "path": "/"+rows, "message": str(exc)})
            values = set()
        choices[aliases[0]] = values
    guarantees = {}
    for view in profile.get("views", []):
        if not isinstance(view, dict):
            continue
        try:
            guarantees[view.get("view_id")] = _ids(view.get("guarantees", []), "guarantee_id", "id")
        except (AtlasValidationError, TypeError) as exc:
            errors.append({"code": "profile_id", "file": "profile.json", "path": "/views", "message": str(exc)})
    for index, row in enumerate(profile.get("comparisons", [])):
        if not isinstance(row, dict):
            errors.append({"code": "comparison_type", "file": "profile.json", "path": f"/comparisons/{index}", "message": "comparison must be an object"})
            continue
        key = row.get("comparison_key", row)
        if not isinstance(key, dict):
            key = {}
        for field, allowed in {**choices, "guarantee_id": guarantees.get(key.get("view_id"), set())}.items():
            value = key.get(field)
            if not isinstance(value, str) or value not in allowed:
                errors.append({"code": "comparison_binding", "file": "profile.json", "path": f"/comparisons/{index}/comparison_key/{field}",
                               "message": f"comparison.{field} is missing or unbound; an explicit, complete comparison key is required. Put relationship descriptions in relations; the program will not infer missing fields"})
    return errors


def _validate_profile_bindings(profile: dict) -> None:
    required = {"setting_id", "title", "common_specification", "views", "quantities", "resource_projections", "regimes", "bounds", "comparisons", "summary_status", "proofs", "evidence", "references", "aliases"}
    if not required.issubset(profile):
        raise AtlasValidationError("profile is missing fields: " + ", ".join(sorted(required - profile.keys())))
    sid = profile["setting_id"]
    view_ids = _ids(profile["views"], "view_id")
    if not view_ids:
        raise AtlasValidationError("At least one algorithm view is required")
    guarantee_ids = {v["view_id"]: _ids(v.get("guarantees", []), "guarantee_id", "id") for v in profile["views"]}
    quantities = _ids(profile["quantities"], "quantity_id", "id")
    projections = _ids(profile["resource_projections"], "resource_projection_id", "projection_id", "id")
    regimes = _ids(profile["regimes"], "regime_id", "region_id", "id")
    bounds = _ids(profile["bounds"], "bound_id", "id")
    _ids(profile["comparisons"], "comparison_id", "id")
    for comparison in profile["comparisons"]:
        key = comparison.get("comparison_key", comparison)
        expected = {"setting_id": {sid}, "view_id": view_ids, "quantity_id": quantities, "resource_projection_id": projections, "regime_id": regimes}
        for name, choices in expected.items():
            if key.get(name) not in choices:
                raise AtlasValidationError(f"comparison {name} is missing or unbound: {key.get(name)!r}")
            if name in comparison and comparison[name] != key[name]:
                raise AtlasValidationError(f"Top-level comparison {name} conflicts with comparison_key")
        if key.get("guarantee_id") not in guarantee_ids[key["view_id"]]:
            raise AtlasValidationError("comparison guarantee_id is not bound to the same view")
    referenced = _profile_bracket_refs(profile)
    if not referenced.issubset(bounds):
        raise AtlasValidationError("comparison / bracket_rows references a nonexistent bound")
    explicitly_inactive = {b.get("id", b.get("bound_id")) for b in profile["bounds"] if _ineligible(b)}
    adopted_inactive = explicitly_inactive & _active_bounds(profile)
    if adopted_inactive:
        raise AtlasValidationError("Quarantined, withdrawn, or explicitly inapplicable bounds cannot enter an active bracket: " + ", ".join(sorted(adopted_inactive)))
    for bound in profile["bounds"]:
        if bound.get("view_id") is not None and bound["view_id"] not in view_ids:
            raise AtlasValidationError("bound references an unknown view")
        if bound.get("guarantee_id") is not None and bound["guarantee_id"] not in guarantee_ids.get(bound.get("view_id"), set()):
            raise AtlasValidationError("The bound guarantee does not belong to its view")
        quantity = bound.get("quantity_id", bound.get("quantity_ref"))
        if quantity is not None and quantity not in quantities:
            raise AtlasValidationError("bound references an unknown quantity")
        rrefs = bound.get("region_refs", bound.get("regime_ids", []))
        if not isinstance(rrefs, list) or not set(rrefs).issubset(regimes):
            raise AtlasValidationError("bound references an unknown regime")
    for alias in profile.get("aliases", []):
        if not isinstance(alias, dict) or not isinstance(alias.get("legacy_id", alias.get("alias_id")), str) or alias.get("view_id") not in view_ids:
            raise AtlasValidationError("Legacy ID aliases must be bound to existing views in the setting")


def _bracket_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if not isinstance(value, dict):
        return refs
    for key, child in value.items():
        if key in {"upper_refs", "lower_refs", "achievable_refs", "necessary_refs", "claim_refs", "bound_refs"}:
            if not isinstance(child, list) or any(not isinstance(item, str) for item in child):
                raise AtlasValidationError(f"bracket {key} must be a list of strings")
            refs.update(child)
        elif key in {"claim_ref", "bound_ref"}:
            if not isinstance(child, str):
                raise AtlasValidationError(f"bracket {key} must be a string")
            refs.add(child)
        elif isinstance(child, dict):
            refs.update(_bracket_refs(child))
        elif isinstance(child, list):
            for item in child:
                refs.update(_bracket_refs(item))
    return refs


def _profile_bracket_refs(profile: dict) -> set[str]:
    refs = set()
    for comparison in profile.get("comparisons", []):
        refs.update(_bracket_refs(comparison.get("bracket", {})))
    for row in profile.get("bracket_rows", []):
        refs.update(_bracket_refs(row))
    return refs


def _ineligible(bound: dict) -> bool:
    status = bound.get("status")
    if isinstance(status, dict):
        status = status.get("code")
    return (bound.get("eligible_for_bracket") is False
            or (isinstance(status, str) and status in {"quarantined", "withdrawn", "ineligible"}))


def _active_bounds(profile: dict) -> set[str]:
    refs = set()
    for bound in profile.get("bounds", []):
        status = bound.get("status")
        if isinstance(status, dict):
            status = status.get("code")
        if bound.get("eligible_for_bracket") is True or bound.get("included_in_bracket") is True or (isinstance(status, str) and status in {"active", "accepted", "adopted"}):
            refs.add(bound.get("id", bound.get("bound_id")))
    refs.update(_profile_bracket_refs(profile))
    return refs
