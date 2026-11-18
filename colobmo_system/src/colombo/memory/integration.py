"""Register Colombo's builtin current Memory without creating or repairing it."""
from __future__ import annotations
from contextlib import closing
from pathlib import Path
import sqlite3
from .contracts import ContractError, LIBRARIES, digest, safe_id
from .mcp_adapter import register_memory
from .store import Store, read_json
from .retrieval import PRIVACY_PROJECTION_SCHEMA, PRIVACY_PROJECTION_TRANSFORMATION
from colombo.project_paths import PROJECT_ROOT

DEFAULT_MEMORY_ROOT = PROJECT_ROOT / "long_term_memory"


def _object(path: Path, description: str) -> dict:
    try:
        value = read_json(path)
    except (OSError, ValueError) as exc:
        raise ContractError(f"Scientific memory {description} is missing or unreadable: {path}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"Scientific memory {description} must be a JSON object: {path}")
    return value


def _hash(value) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def _validate_index(path: Path) -> None:
    if not path.is_file():
        raise ContractError(f"Scientific memory catalog index is missing: {path}")
    try:
        # Opening with mode=ro cannot create a missing database or repair it.
        uri = path.resolve().as_uri() + "?mode=ro&immutable=1"
        with closing(sqlite3.connect(uri, uri=True)) as db:
            db.execute("SELECT rowid, entry_id, kind, scope_ref, card FROM scopes LIMIT 0")
            db.execute("SELECT rowid, text FROM search LIMIT 0")
            definition = db.execute("SELECT sql FROM sqlite_master WHERE name='search' AND type='table'").fetchone()
            if not definition or not isinstance(definition[0], str) or "using fts5" not in definition[0].lower():
                raise ContractError(f"Scientific memory search index must use FTS5: {path}")
            db.execute("SELECT rowid FROM search WHERE search MATCH ? LIMIT 1", ('"preflight"',)).fetchall()
    except sqlite3.Error as exc:
        raise ContractError(f"Scientific memory catalog index is invalid or unreadable: {path}: {exc}") from exc


def _finder_metadata(path: Path) -> bool:
    """Ignore only regular Finder metadata, never links or directories."""
    return path.name == ".DS_Store" and not path.is_symlink() and path.is_file()


def _validate_privacy_projection(store: Store, manifest: dict) -> None:
    """Validate exported-byte identities without granting a new review decision.

    The mapping preserves original review identities. It neither replaces
    prepare/review/publish nor changes the acceptance contract. Subsequent
    native publications may add ordinary revisions outside this fixed export.
    """
    path = store.state_root / "PRIVACY_PROJECTION.json"
    marked = {ident: entry for ident, entry in manifest["entries"].items()
              if "privacy_projection" in entry}
    if not path.exists():
        if marked:
            raise ContractError("Privacy projection entries require the global mapping")
        return
    if not path.is_file() or path.is_symlink():
        raise ContractError("Privacy projection mapping must be a regular file")
    projection = _object(path, "privacy projection mapping")
    if (projection.get("schema") != PRIVACY_PROJECTION_SCHEMA
            or projection.get("no_new_review") is not True
            or not isinstance(projection.get("records"), list)):
        raise ContractError("Invalid privacy projection schema or no-new-review declaration")
    if any("privacy_projection" in entry for entry in store.lead_manifest()["entries"].values()):
        raise ContractError("Privacy projection review metadata cannot be applied to leads")

    published = set()
    references = list(manifest["entries"].values())
    for receipt in manifest["receipts"].values():
        if not isinstance(receipt.get("published_refs"), list):
            raise ContractError("Privacy projection requires explicit published receipt references")
        references.extend(receipt["published_refs"])
    for ref in references:
        if (not isinstance(ref, dict) or ref.get("tier") != "published"
                or not isinstance(ref.get("kind"), str) or ref["kind"] not in LIBRARIES
                or type(ref.get("revision")) is not int or ref["revision"] < 1
                or not _hash(ref.get("content_hash"))):
            raise ContractError("Invalid published reference in privacy projection")
        safe_id(ref.get("id"))
        published.add((ref["id"], ref["kind"], ref["revision"], ref["content_hash"]))

    mapped = {}
    for row in projection["records"]:
        if (not isinstance(row, dict) or not isinstance(row.get("kind"), str) or row["kind"] not in LIBRARIES
                or type(row.get("revision")) is not int or row["revision"] < 1
                or not _hash(row.get("original_content_hash"))
                or not _hash(row.get("projected_content_hash"))
                or not isinstance(row.get("change_pointers"), list)
                or any(not isinstance(pointer, str) or (pointer != "#" and not pointer.startswith(("#/", "/")))
                       for pointer in row["change_pointers"])):
            raise ContractError("Invalid privacy projection record mapping")
        safe_id(row.get("id"))
        identity = (row["id"], row["kind"], row["revision"])
        key = (*identity, row["projected_content_hash"])
        if identity in mapped:
            raise ContractError("Duplicate privacy projection record mapping")
        if key not in published:
            raise ContractError("Privacy projection mapping is not a published revision")
        changed = row["original_content_hash"] != row["projected_content_hash"]
        if bool(row["change_pointers"]) != changed:
            raise ContractError("Privacy projection changes and hashes disagree")
        history = store.published_path({**row, "content_hash": row["projected_content_hash"]})
        record = _object(history, "privacy projection history")
        if (digest(record) != row["projected_content_hash"]
                or any(record.get(field) != row[field] for field in ("id", "kind", "revision"))
                or not isinstance(record.get("evidence"), dict)
                or record["evidence"].get("readiness") != "reference"):
            raise ContractError("Privacy projection history hash or published identity mismatch")
        mapped[identity] = row

    for ident, entry in manifest["entries"].items():
        row = mapped.get((ident, entry["kind"], entry["revision"]))
        metadata = entry.get("privacy_projection")
        if row is None:
            if "privacy_projection" in entry:
                raise ContractError("Privacy projection entry is absent from the global mapping")
            continue
        if entry["content_hash"] != row["projected_content_hash"]:
            raise ContractError("Privacy projection entry hash disagrees with the global mapping")
        changed = row["original_content_hash"] != row["projected_content_hash"]
        if not changed:
            if "privacy_projection" in entry:
                raise ContractError("Unchanged publication cannot claim a privacy projection")
            continue
        scope = entry.get("review_scope")
        if (not isinstance(metadata, dict)
                or metadata.get("schema") != PRIVACY_PROJECTION_SCHEMA
                or metadata.get("transformation") != PRIVACY_PROJECTION_TRANSFORMATION
                or metadata.get("no_new_review", True) is not True
                or metadata.get("original_content_hash") != row["original_content_hash"]
                or metadata.get("projected_content_hash") != row["projected_content_hash"]
                or not isinstance(scope, dict)
                or scope.get("record_hash") != row["original_content_hash"]
                or scope.get("decision") != "accept"):
            raise ContractError("Privacy projection entry does not match its original review and global mapping")


def _validate_store(store: Store) -> None:
    current = _object(store.state_root / "CURRENT.json", "CURRENT pointer")
    if not isinstance(current.get("generation"), str) or not _hash(current.get("manifest_hash")):
        raise ContractError("Scientific memory CURRENT pointer needs generation and SHA-256 manifest_hash")
    safe_id(current["generation"])
    generation = store._state_inside(".generations/" + current["generation"])
    manifest = _object(generation / "manifest.json", "manifest")
    if (manifest.get("schema") != "colombo-memory-catalog/2"
            or not isinstance(manifest.get("entries"), dict)
            or not isinstance(manifest.get("receipts"), dict)
            or type(manifest.get("sequence")) is not int or manifest["sequence"] < 0):
        raise ContractError("Scientific memory manifest has invalid schema, entries, receipts or sequence")
    for ident, entry in manifest["entries"].items():
        safe_id(ident)
        if (not isinstance(entry, dict) or entry.get("id") != ident
                or not isinstance(entry.get("kind"), str) or entry["kind"] not in LIBRARIES
                or type(entry.get("revision")) is not int or entry["revision"] < 1
                or not _hash(entry.get("content_hash")) or not isinstance(entry.get("path"), str)):
            raise ContractError(f"Scientific memory manifest entry is invalid: {ident}")
        if not entry["path"] or Path(entry["path"]).is_absolute():
            raise ContractError(f"Scientific memory manifest entry needs a relative object path: {ident}")
        if not store._state_inside(entry["path"]).is_file():
            raise ContractError(f"Scientific memory manifest object is missing: {ident}")
    if any(not _hash(key) or not isinstance(value, dict) for key, value in manifest["receipts"].items()):
        raise ContractError("Scientific memory manifest receipts must map proposal hashes to receipt objects")
    if digest(manifest) != current["manifest_hash"]:
        raise ContractError("Scientific memory manifest hash does not match CURRENT pointer")
    _validate_index(generation / "catalog.sqlite")
    # Scientific content is exactly the four libraries; Finder may add metadata.
    expected = set(LIBRARIES.values())
    if {p.name for p in store.root.iterdir() if not _finder_metadata(p)} != expected:
        raise ContractError("Memory root must contain only the four scientific library directories")
    current_records = store.current_records(include_leads=True)
    expected_files = {store.current_path(r["id"], r["kind"]) for r in current_records}
    actual_files = set()
    for library in expected:
        folder = store.root / library
        if not folder.is_dir() or folder.is_symlink():
            raise ContractError("Scientific libraries must be actual directories, not links")
        for path in folder.iterdir():
            if _finder_metadata(path):
                continue
            if not path.is_file() or path.is_symlink() or path.suffix != ".json":
                raise ContractError(f"Unexpected item in scientific library: {path}")
            actual_files.add(path.resolve())
    if actual_files != expected_files:
        raise ContractError("Visible scientific files and record catalog disagree; no automatic repair")
    for record in current_records:
        current_path = store.current_path(record["id"], record["kind"])
        if digest(read_json(current_path)) != digest(record):
            raise ContractError(f"Visible scientific record changed without a transaction: {record['id']}")
    lead_catalog = store.lead_catalog()
    if lead_catalog is not None:
        _validate_index(lead_catalog)
    _validate_privacy_projection(store, manifest)


def register_builtin_memory(mcp, *, research_mode: str, memory_root: str | Path | None = None) -> bool:
    """Use the installed Colombo Store; a Python-only override supports isolated tests.

    The model tool has no library-path argument. Ambient environment variables
    do not select a different library or disable the installed reader.
    """
    if research_mode not in {"generic", "oracle_complexity"}:
        raise ContractError("Unknown research mode; define its capabilities explicitly")
    root = Path(memory_root).expanduser() if memory_root is not None else DEFAULT_MEMORY_ROOT
    if not root.is_absolute():
        raise ContractError("The Python Memory-root override must be an absolute installation path")
    _validate_store(Store(root))  # Fail before registration; readers never create or repair indexes.
    register_memory(mcp, memory_root=root, research_mode=research_mode)
    return True
