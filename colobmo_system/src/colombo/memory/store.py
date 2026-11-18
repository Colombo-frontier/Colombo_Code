"""Read-only scientific records in four visible libraries.

Current scientific content lives in <root>/<library>/<id>.json.  Indexes,
review proposals and pinned historical revisions live in a sibling state
folder; they are not additional scientific libraries.  Readers never write.
"""
from __future__ import annotations
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
from .contracts import ContractError, LIBRARIES, canonical_bytes, digest, safe_id


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".tmp-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(canonical_bytes(obj)); f.flush(); os.fsync(f.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class Store:
    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self.state_root = self.root.with_name("." + self.root.name + "_state")

    @staticmethod
    def _contained(base: Path, relative: str) -> Path:
        if not isinstance(relative, str) or Path(relative).is_absolute():
            raise ContractError("Expected a relative storage path")
        p = (base / relative).resolve()
        if not p.is_relative_to(base):
            raise ContractError("Path escapes the configured storage root")
        return p

    def _inside(self, relative: str) -> Path:
        return self._contained(self.root, relative)

    def _state_inside(self, relative: str) -> Path:
        return self._contained(self.state_root, relative)

    def current_path(self, ident: str, kind: str) -> Path:
        safe_id(ident)
        if kind not in LIBRARIES:
            raise ContractError("Unknown record kind")
        return self._inside(f"{LIBRARIES[kind]}/{ident}.json")

    def generation(self) -> Path:
        try:
            p = read_json(self.state_root / "CURRENT.json")
        except FileNotFoundError as exc:
            raise ContractError("Four-library memory state is missing; run the explicit layout migration, not a research reader") from exc
        safe_id(p["generation"])
        return self._state_inside(".generations/" + p["generation"])

    def manifest(self) -> dict:
        return read_json(self.generation() / "manifest.json")

    def published_path(self, ref: dict) -> Path:
        """Locate an immutable scientific object, including compact distributions.

        Compact stores retain pinned scientific objects by digest without
        shipping the execution history that originally produced them.
        """
        content_hash = ref["content_hash"]
        if (not isinstance(content_hash, str) or len(content_hash) != 64
                or any(c not in "0123456789abcdef" for c in content_hash)):
            raise ContractError("Published object needs an exact SHA-256 content hash")
        compact = self._state_inside(f"objects/{content_hash}.json")
        if compact.is_file():
            return compact
        safe_id(ref["id"])
        if ref["kind"] not in LIBRARIES or type(ref["revision"]) is not int or ref["revision"] < 1:
            raise ContractError("Invalid published object identity")
        return self._state_inside(
            f"history/{LIBRARIES[ref['kind']]}/{ref['id']}/"
            f"r{ref['revision']:06d}-{content_hash}.json")

    def get(self, ident: str, *, revision: int | None = None, content_hash: str | None = None,
            kind: str | None = None) -> dict:
        safe_id(ident)
        if revision is None:
            item = self.manifest()["entries"].get(ident)
            if item is None:
                raise ContractError(f"No published record: {ident}")
            path = self._state_inside(item["path"])
            content_hash = item["content_hash"]
        else:
            if type(revision) is not int or revision < 1 or kind not in LIBRARIES:
                raise ContractError("Pinned read needs kind and positive revision")
            if not isinstance(content_hash, str) or len(content_hash) != 64 or any(c not in "0123456789abcdef" for c in content_hash):
                raise ContractError("Pinned read needs an exact SHA-256 content hash")
            # An interrupted publication may leave an immutable object behind.
            # Existence and a matching hash alone do not establish publication.
            manifest = self.manifest()
            expected = {"id": ident, "revision": revision, "kind": kind, "content_hash": content_hash}
            current = manifest["entries"].get(ident)
            candidates = ([current] if current else []) + [
                old for receipt in manifest["receipts"].values()
                for old in receipt["published_refs"]
            ]
            if not any(item.get("tier") == "published" and
                       all(item.get(key) == value for key, value in expected.items())
                       for item in candidates):
                raise ContractError("Pinned reference has not been published with this exact identity")
            path = self.published_path(expected)
        if not path.is_file():
            raise ContractError("Pinned record is unavailable; do not silently substitute the latest version")
        r = read_json(path)
        if (digest(r) != content_hash or r["id"] != ident or (kind is not None and r["kind"] != kind)
                or (revision is not None and r["revision"] != revision)):
            raise ContractError("Immutable record hash/identity mismatch")
        return r

    def ref(self, record: dict) -> dict:
        return {"id": record["id"], "revision": record["revision"], "kind": record["kind"],
                "content_hash": digest(record), "tier": "published"}

    def all_records(self, manifest: dict | None = None) -> list[dict]:
        m = manifest if manifest is not None else self.manifest()
        result = []
        for ident, item in m["entries"].items():
            r = read_json(self._state_inside(item["path"]))
            if digest(r) != item["content_hash"] or r["id"] != ident:
                raise ContractError(f"Hash/identity mismatch: {ident}")
            result.append(r)
        return result

    def lead_manifest(self) -> dict:
        pointer = self.state_root / "LEADS.json"
        if not pointer.exists():
            return {"entries": {}, "count": 0}
        value = read_json(pointer)
        if value.get("schema") != "colombo-four-library-leads/1":
            raise ContractError("Legacy lead layout requires explicit migration")
        if value.get("count") != len(value.get("entries", {})):
            raise ContractError("Lead catalog count mismatch")
        return value

    def lead(self, ref: dict) -> dict:
        ident = safe_id(ref["id"])
        item = self.lead_manifest()["entries"].get(ident)
        if item is None:
            raise ContractError("Lead missing or already published; retrieve a current card explicitly")
        p = self.current_path(ident, item["kind"])
        if not p.is_file():
            raise ContractError("Lead record missing from its scientific library")
        r = read_json(p)
        if digest(r) != ref["content_hash"] or digest(r) != item["content_hash"] or r["id"] != ident:
            raise ContractError("Lead changed; retrieve the current card explicitly")
        if r["evidence"]["readiness"] != "lead":
            raise ContractError("Lead readiness changed without a review publication")
        return r

    def lead_records(self) -> list[dict]:
        return [self.lead({"id": ident, "content_hash": item["content_hash"]})
                for ident, item in self.lead_manifest()["entries"].items()]

    def lead_catalog(self) -> Path | None:
        lead = self.lead_manifest()
        if not lead.get("path"):
            return None
        return self._state_inside(lead["path"]) / "catalog.sqlite"

    def current_records(self, *, include_leads: bool = True) -> list[dict]:
        records = {r["id"]: r for r in self.lead_records()} if include_leads else {}
        records.update({r["id"]: r for r in self.all_records()})
        return [records[i] for i in sorted(records)]
