"""Versioned JSON memory with one writer lock and service-owned reviews.

Only expose ``archive`` and ``retrieve`` to a research agent. ``write_review``
is a trusted service entry point, not an authentication boundary against code
running under the same operating-system account.
"""

from __future__ import annotations

import copy
import json
import os
from colombo.shared.file_io import Path, file_lock
from colombo.shared.file_io import atomic_write
import re
import time
from contextlib import contextmanager, ExitStack
from datetime import datetime
from datetime import timezone
from typing import Any
from uuid import uuid4
from colombo.cell.settings import get_settings
from colombo.shared.experiment_artifacts import read_artifact_groups
from colombo.shared.experiment_artifacts import experiment_group
from colombo.shared.experiment_artifacts import manifest_for
import colombo.cell.research_records as research_records


class StoreError(ValueError):
    """A rejected request or invalid on-disk memory."""


class RevisionConflict(StoreError):
    pass


class AuditRequired(StoreError):
    pass


from colombo.cell.record_formats import WRITABLE_KINDS
from colombo.cell.record_formats import READABLE_KINDS
from colombo.cell.record_formats import ALIASES
VERDICTS = frozenset({"pass", "fail", "uncertain", "service_error"})
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]*\Z")
_AUTHORITY_FIELDS = frozenset({
    "audit_status", "review_status", "audit_result", "review_result",
    "verified", "is_verified", "verification_status", "verdict", "approved",
    "certified", "reviewer", "reviewer_identity", "current_trust",
})
_TRUSTED_LABELS = frozenset({
    "proved", "verified", "audited", "accepted", "approved", "certified",
    "checked", "pass",
})
_CONTROL_FIELDS = frozenset({"status", "tag", "audit_id"})
_EXPERIMENT_INTERPRETATION = frozenset({"observations", "limitations", "derived_refs"})
_EXPERIMENT_STATUSES = frozenset({"preparing", "submitted", "running", "remote_unknown",
    "download_pending", "completed", "failed", "cancelled", "timed_out", "expired"})


def _json(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise StoreError("Payload must be finite JSON data") from exc


def json_equal(left: Any, right: Any) -> bool:
    """Type-sensitive JSON equality; object key order is not significant."""
    return _json(left) == _json(right)


def evidence_body(payload: dict) -> dict:
    """Actual reviewed mathematics, excluding only promotion metadata."""
    return copy.deepcopy({k: v for k, v in payload.items()
                          if k not in _CONTROL_FIELDS | {"title", "notes", "description", "metadata"}})


def support_body(payload: dict) -> dict:
    """Actual support basis; changing provenance cannot repair mathematics."""
    return copy.deepcopy({k: v for k, v in payload.items()
                          if k not in _CONTROL_FIELDS | {"challenged_by", "origin", "title", "notes", "description", "metadata"}})


def _unique(values: list[dict]) -> list[dict]:
    result = []
    for value in values:
        if not any(json_equal(value, item) for item in result):
            result.append(value)
    return result


def _ref(record: dict) -> dict:
    return {key: record[key] for key in ("kind", "id", "revision")}


def _kind(kind: str, *, writable: bool = False) -> str:
    if not isinstance(kind, str):
        raise StoreError("kind must be a supported collection name")
    kind = ALIASES.get(kind, kind)
    if kind not in (WRITABLE_KINDS if writable else READABLE_KINDS):
        raise StoreError(f"Unsupported or service-only kind: {kind!r}")
    return kind


def _record_id(value: str, max_chars: int | None = None) -> str:
    if max_chars is None:
        max_chars = get_settings()["limits"]["record_id_max_chars"]
    if not isinstance(value, str) or len(value) > max_chars or not _ID.fullmatch(value):
        raise StoreError(f"record_id must be 1-{max_chars} safe identifier characters")
    return value


def _revision(value: int | None) -> None:
    if value is not None and (type(value) is not int or value < 1):
        raise StoreError("revision must be a positive integer")


class Store:
    def __init__(self, memory_dir: Path, lock_timeout: float | None = None):
        self.memory_dir = Path(memory_dir).resolve()
        self.settings = get_settings(self.memory_dir.parent)
        if lock_timeout is None:
            lock_timeout = self.settings["runtime"]["store_lock_timeout_seconds"]
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        if lock_timeout < 0:
            raise StoreError("lock_timeout cannot be negative")
        self.lock_timeout = lock_timeout
        # A child workspace may grant a fixed set of parent revisions. Only
        # this immediate neighbour is consulted; never walk ancestor stores.
        with self._locked():
            marker = self._read(".storage.json", None)
            if marker is None:
                if any(self.memory_dir.glob("*.json")):
                    raise StoreError("Existing memory has no current storage version; start a new run")
                self._atomic_write(".storage.json", {"storage_version": 2})
            elif not json_equal(marker, {"storage_version": 2}):
                raise StoreError("Unsupported memory storage version; start a new run")
        self._context = self._load_context()

    def _record_id(self, value: str) -> str:
        return _record_id(value, self.settings["limits"]["record_id_max_chars"])

    def _request_id(self, value: str | None) -> None:
        max_chars = self.settings["limits"]["request_id_max_chars"]
        if value is not None and (not isinstance(value, str) or not value or len(value) > max_chars):
            raise StoreError(f"request_id must be a nonempty string of at most {max_chars} characters")

    def _load_context(self) -> dict[tuple, dict]:
        directory = self.memory_dir.parent / "context"
        manifest_path = directory / "manifest.json"
        if self.memory_dir.name != "memory" or not manifest_path.exists():
            return {}
        if directory.is_symlink() or directory.resolve() != directory \
                or manifest_path.is_symlink():
            raise StoreError("Context must be an adjacent ordinary directory")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise StoreError("Cannot read context manifest") from exc
        if not isinstance(manifest, dict) or not isinstance(manifest.get("snapshot_refs"), list):
            raise StoreError("Context manifest requires snapshot_refs")
        granted = {}
        for ref in manifest["snapshot_refs"]:
            if not isinstance(ref, dict) or not {"kind", "id", "revision"} <= ref.keys():
                raise StoreError("Context references need kind, id and revision")
            kind = _kind(ref["kind"])
            self._record_id(ref["id"])
            _revision(ref["revision"])
            if ref["revision"] is None:
                raise StoreError("Context references must pin revisions")
            granted[(kind, ref["id"], ref["revision"])] = ref
        snapshots = {}
        for kind in {key[0] for key in granted}:
            path = directory / f"{kind}.json"
            if path.is_symlink() or path.resolve().parent != directory:
                raise StoreError("Context collection cannot redirect outside the snapshot")
            try:
                document = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise StoreError(f"Cannot read granted context collection: {kind}") from exc
            if not isinstance(document, dict) or document.get("schema_version") != 2 \
                    or not isinstance(document.get("records"), list):
                raise StoreError(f"Invalid context collection: {kind}")
            for record in document["records"]:
                if not isinstance(record, dict) or not isinstance(record.get("id"), str) \
                        or type(record.get("revision")) is not int:
                    raise StoreError("Invalid context record envelope")
                key = (kind, record.get("id"), record.get("revision"))
                if key not in granted:
                    continue
                if record.get("kind") != kind or not isinstance(record.get("payload"), dict) \
                        or not isinstance(record.get("created_at"), str):
                    raise StoreError("Context record content or identity does not match its envelope")
                if key in snapshots:
                    raise StoreError("Duplicate context record version")
                snapshots[key] = dict(record, origin="context", read_only=True)
                if "property_ids" in granted[key]:
                    ids = granted[key]["property_ids"]
                    valid = {p["id"] for p in record["payload"].get("properties", [])}
                    if kind != "examples" or not isinstance(ids, list) or not ids or len(ids) != len(set(ids)) or not set(ids) <= valid:
                        raise StoreError("Invalid property scope in context manifest")
                    snapshots[key]["property_ids"] = list(ids)
        if set(snapshots) != set(granted):
            raise StoreError("Context manifest refers to missing record revisions")
        return snapshots

    def _context_records(self, kind: str) -> list[dict]:
        return [record for (record_kind, _, _), record in self._context.items() if record_kind == kind]

    def _context_has_id(self, kind: str, record_id: str) -> bool:
        return any(key[0] == kind and key[1] == record_id for key in self._context)

    def _path(self, name: str) -> Path:
        allowed = {f"{kind}.json" for kind in READABLE_KINDS}
        allowed |= {".lock", ".pending.json", ".requests.json", ".queries.json", ".storage.json"}
        if name not in allowed:
            raise StoreError("Invalid internal storage path")
        path = self.memory_dir / name
        if path.is_symlink():
            raise StoreError(f"Storage files cannot be symbolic links: {name}")
        return path

    @contextmanager
    def _locked(self):
        path = self._path(".lock")
        with ExitStack() as stack:
            try:
                stack.enter_context(file_lock(path, self.lock_timeout,
                                              self.settings["runtime"]["lock_poll_seconds"]))
            except TimeoutError as exc:
                raise TimeoutError("Timed out waiting for memory writer lock") from exc
            self._recover()
            yield

    def _read(self, name: str, default: Any) -> Any:
        path = self._path(name)
        if not path.exists():
            return copy.deepcopy(default)
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise StoreError(f"Cannot read valid memory file: {name}") from exc

    def _atomic_write(self, name: str, data: Any) -> None:
        destination = self._path(name)
        text = _json(data)
        atomic_write(destination, (text + "\n").encode("utf-8"), sync_directory=True)

    def _recover(self) -> None:
        journal = self._read(".pending.json", None)
        if journal is None:
            return
        if not isinstance(journal, dict) or set(journal) != {"writes"}:
            raise StoreError("Invalid pending transaction")
        writes = journal["writes"]
        if not isinstance(writes, dict) or not writes:
            raise StoreError("Invalid pending transaction writes")
        allowed = {f"{kind}.json" for kind in READABLE_KINDS} | {".requests.json", ".queries.json"}
        if not set(writes) <= allowed:
            raise StoreError("Invalid transaction destination")
        for name, document in writes.items():
            self._atomic_write(name, document)
        self._path(".pending.json").unlink()

    def _commit(self, writes: dict) -> None:
        # The journal makes record + event + idempotency updates recoverable
        # after a process interruption between individual atomic replacements.
        self._atomic_write(".pending.json", {"writes": writes})
        self._recover()

    def _collection(self, kind: str) -> dict:
        if kind in getattr(self, "_staged_collections", {}):
            return self._staged_collections[kind]
        document = self._read(f"{kind}.json", {"schema_version": 2, "records": []})
        if not isinstance(document, dict) or document.get("schema_version") != 2 \
                or not isinstance(document.get("records"), list):
            raise StoreError(f"Invalid collection: {kind}")
        return document

    def _get(self, kind: str, record_id: str, revision: int | None = None) -> dict:
        local = self._collection(kind)["records"]
        if self._context_has_id(kind, record_id) and any(r["id"] == record_id for r in local):
            raise StoreError("Local record collides with a read-only context identity")
        matches = [r for r in local + self._context_records(kind)
                   if r["id"] == record_id and (revision is None or r["revision"] == revision)]
        if not matches:
            raise KeyError(f"No record {kind}/{record_id}@{revision or 'latest'}")
        return max(matches, key=lambda r: r["revision"])

    @staticmethod
    def _envelope(kind: str, payload: dict, record_id: str, revision: int) -> dict:
        return {"kind": kind, "id": record_id, "revision": revision,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "payload": payload}

    def get(self, kind: str, id: str, revision: int | None = None, *, project: bool = True) -> dict:
        kind = _kind(kind)
        self._record_id(id)
        _revision(revision)
        with self._locked():
            return self._with_trust(self._get(kind, id, revision), project=project)

    def snapshot(self, kinds: list[str] | None = None, include_context: bool = False,
                 with_trust: bool = False) -> list[dict]:
        """Read a complete service snapshot, including history, under one lock."""
        selected = sorted(READABLE_KINDS) if kinds is None else [_kind(k) for k in kinds]
        with self._locked():
            records = [record for kind in selected for record in
                       self._collection(kind)["records"] + (self._context_records(kind) if include_context else [])]
            return [self._with_trust(r) for r in records] if with_trust else copy.deepcopy(records)

    def archive_result(self, records: list[dict], request_id: str) -> dict:
        return research_records.archive_result(self, records, request_id)

    def _resolve_ref(self, ref: dict) -> dict:
        if not isinstance(ref, dict) or not {"kind", "id", "revision"} <= ref.keys():
            raise StoreError("Record references require kind, id and pinned revision")
        if set(ref) - {"kind", "id", "revision", "property_ids", "position"}:
            raise StoreError("Record reference has unsupported fields")
        kind = _kind(ref["kind"])
        self._record_id(ref["id"])
        _revision(ref["revision"])
        if ref["revision"] is None:
            raise StoreError("Record references must pin a revision")
        record = self._get(kind, ref["id"], ref["revision"])
        if "property_ids" in ref:
            ids = ref["property_ids"]
            valid = {p["id"] for p in record["payload"].get("properties", [])}
            if kind != "examples" or not isinstance(ids, list) or not ids \
                    or any(not isinstance(p, str) for p in ids) \
                    or len(ids) != len(set(ids)) or not set(ids) <= valid:
                raise StoreError("property_ids must select distinct existing example properties")
            if record.get("origin") == "context" and "property_ids" in record and not set(ids) <= set(record["property_ids"]):
                raise StoreError("Requested properties exceed the granted context scope")
        return record

    def resolve_record_refs(self, refs: list[dict], *, project: bool = True) -> list[dict]:
        """Freeze explicitly granted versions; never expand into ancestor stores."""
        if not isinstance(refs, list):
            raise StoreError("record_refs must be a list")
        with self._locked():
            result = []
            for ref in refs:
                raw = copy.deepcopy(self._resolve_ref(ref))
                if "property_ids" in ref:
                    raw["property_ids"] = ref["property_ids"]
                record = self._with_trust(raw, project=project)
                for key in ("position", "property_ids"):
                    if key in ref:
                        record[key] = copy.deepcopy(ref[key])
                result.append(record)
            return result

    def _evidence_records(self, refs: list[dict]) -> list[dict]:
        """Freeze declared evidence and research objects without expanding permissions."""
        pending, records, selections = list(refs), {}, {}
        limit = self.settings["retrieval"]["max_memory_results"]
        while pending:
            ref = pending.pop(0)
            record = self._resolve_ref(ref)
            key = (record["kind"], record["id"], record["revision"])
            scope = ref.get("property_ids", record.get("property_ids"))
            selected = set(scope) if scope is not None else None
            if key in records:
                prior = selections[key]
                if prior is None or selected is not None and selected <= prior:
                    continue
                selected = None if selected is None else prior | selected
            elif len(records) >= limit:
                raise StoreError("Selected evidence dependency graph exceeds max_memory_results")
            selections[key] = selected
            record = self._with_trust(record)
            if selected is not None:
                record["property_ids"] = sorted(selected)
                record["payload"]["properties"] = [p for p in record["payload"].get("properties", []) if p["id"] in selected]
            records[key] = record
            dependencies = list(record["payload"].get("dependencies", []))
            dependencies.extend(research_records.object_refs(record["payload"]))
            dependencies.extend(research_records.source_refs(record["payload"]))
            if record["kind"] == "examples":
                for prop in record["payload"].get("properties", []):
                    if selected is None or prop["id"] in selected:
                        dependencies.extend(prop.get("dependencies", []))
            pending.extend(dependencies)
        return list(records.values())

    def evidence_bundle(self, refs: list[dict]) -> dict:
        """Freeze an explicitly selected graph and verify every declared experiment file."""
        with self._locked():
            records = self._evidence_records(refs)
            groups = [experiment_group(record["payload"]) for record in records if record["kind"] == "experiment_result"]
            try:
                files = read_artifact_groups(self.memory_dir.parent, groups, settings=self.settings)
            except ValueError as exc:
                raise StoreError(str(exc)) from exc
            return {"records": records, "artifacts": manifest_for(files), "artifact_groups": groups, "files": files}

    def _corrections(self, kind: str, record_id: str | None = None) -> list[dict]:
        result = []
        for review in self._collection("reviews")["records"] + self._context_records("reviews"):
            value = review["payload"]
            if value.get("type") != "confirmed_review" and not (
                    value.get("type") == "argument_challenge" and value.get("status") == "withdrawn"):
                continue
            for correction in review["payload"].get("corrections", []):
                target = correction["target"]
                if target["kind"] == kind and (record_id is None or target["id"] == record_id):
                    result.append(dict(correction, review_ref=_ref(review)))
        if kind == "arguments":
            for granted in self._context_records(kind):
                # A finite grant already includes its negative trust evidence.
                # Copying its mathematical payload under another ID cannot
                # discard that evidence merely because reviews were not granted.
                for correction in granted.get("current_trust", {}).get("objections", []):
                    if record_id is None or correction["target"]["id"] == record_id:
                        result.append(dict(copy.deepcopy(correction), basis=support_body(granted["payload"])))
        return _unique(result)

    def _challenge_states(self) -> dict[str, dict]:
        """Latest service state per challenge; past pending revisions are history."""
        states = {}
        for review in self._collection("reviews")["records"]:
            if review["payload"].get("type") == "argument_challenge":
                challenge_id = review["payload"]["challenge_id"]
                if challenge_id not in states or review["revision"] > states[challenge_id]["revision"]:
                    states[challenge_id] = review
        return states

    def _suspensions(self, record: dict) -> list[dict]:
        if record["kind"] != "arguments":
            return []
        basis, audit_id = support_body(record["payload"]), record["payload"].get("audit_id")
        pending = [dict(copy.deepcopy(review["payload"]), review_ref=_ref(review))
                   for review in self._challenge_states().values() if review["payload"]["status"] == "pending"]
        for granted in self._context_records("arguments"):
            pending.extend(copy.deepcopy(granted.get("current_trust", {}).get("pending_challenges", [])))
        matches = [item for item in pending if json_equal(item["basis"], basis) or audit_id in item["audit_ids"]]
        return _unique(matches)

    def _withdrawals(self, record: dict, property_id: str | None = None,
                     payload: dict | None = None) -> list[dict]:
        value = record["payload"] if payload is None else payload
        if record["kind"] == "examples":
            prop = next((p for p in value.get("properties", []) if p["id"] == property_id), {})
            basis = copy.deepcopy({"base": support_body({k: v for k, v in value.items() if k != "properties"}),
                                  "property": support_body(prop)})
            audit_id = prop.get("audit_id")
        else:
            basis, audit_id = support_body(value), value.get("audit_id")
        matches = []
        for correction in self._corrections(record["kind"]):
            if correction.get("property_id") != property_id:
                continue
            same = json_equal(correction["basis"], basis) or audit_id in correction["audit_ids"]
            if same:
                matches.append(correction)
        return matches

    def _assess(self, record: dict, visiting: set | None = None) -> dict:
        key = (record["kind"], record["id"], record["revision"])
        if record["kind"] == "examples" and "property_ids" in record:
            key += (tuple(sorted(record["property_ids"])),)
        visiting = set() if visiting is None else set(visiting)
        if key in visiting:
            return {"state": "dependency_blocked", "blockers": [{"ref": _ref(record), "reason": "dependency_cycle"}]}
        visiting.add(key)
        payload, kind = record["payload"], record["kind"]
        if kind == "examples" and "property_ids" in record:
            payload = {**payload, "properties": [p for p in payload.get("properties", [])
                                                 if p["id"] in record["property_ids"]]}
        if kind == "claims":
            return research_records.claim_trust(self, record, visiting)
        # A fixed grant carries the parent's assessment as of launch. A child
        # must not discover additional parent files to recompute that snapshot.
        if record.get("origin") == "context" and isinstance(record.get("current_trust"), dict):
            trust = copy.deepcopy(record["current_trust"])
            if kind == "examples" and "property_ids" in record:
                trust["properties"] = {key: value for key, value in trust.get("properties", {}).items()
                                       if key in record["property_ids"]}
                states = {value["state"] for value in trust["properties"].values()}
                trust["state"] = next(iter(states)) if len(states) == 1 else "partially_supported" if "supported" in states else "unreviewed"
            if kind == "examples":
                # A parent's derived property certificate may rely on an
                # Argument also granted here. Local challenges of that support
                # apply without editing or reading beyond the parent snapshot.
                for prop in payload.get("properties", []):
                    assessment = trust.get("properties", {}).get(prop["id"], {})
                    supports = assessment.get("supports", [])
                    if assessment.get("state") != "supported" or not supports or prop.get("status") == "checked":
                        continue
                    alive = False
                    for support in supports:
                        try:
                            argument = self._resolve_ref(support["argument_ref"])
                        except KeyError:
                            alive = True  # Keep unexposed parent evidence frozen.
                            continue
                        if self._assess(argument, visiting)["state"] == "supported":
                            alive = True
                    if not alive:
                        assessment["state"] = "dependency_blocked"
                        assessment["blockers"] = [{"reason": "granted_property_support_unavailable"}]
                states = {item["state"] for item in trust.get("properties", {}).values()}
                trust["state"] = next(iter(states)) if len(states) == 1 else "partially_supported" if "supported" in states else "unreviewed"
            if kind == "arguments":
                # The parent's grant remains fixed. New objections learned in
                # this child still apply to identical local evidence; this is
                # an overlay in this store, never a write to the parent.
                objections, pending = self._withdrawals(record), self._suspensions(record)
                if objections:
                    trust["state"] = "withdrawn"
                    for field in ("objections", "confirmed_objections"):
                        trust[field] = _unique(trust.get(field, []) + objections)
                elif pending and trust["state"] != "withdrawn":
                    trust["state"] = "suspended"
                if pending:
                    trust["pending_challenges"] = _unique(trust.get("pending_challenges", []) + pending)
            if kind == "experiment_result":
                try:
                    read_artifact_groups(self.memory_dir.parent, [experiment_group(payload)], settings=self.settings)
                except (ValueError, OSError) as exc:
                    return {"state": "dependency_blocked", "blockers": [{"reason": str(exc)}]}
            return trust
        blockers = self._dependency_blockers(payload, visiting)
        if kind == "experiment_result":
            try:
                read_artifact_groups(self.memory_dir.parent, [experiment_group(payload)], settings=self.settings)
            except (ValueError, OSError) as exc:
                blockers.append({"reason": str(exc), "type": "experiment_artifact"})
            state = "computational_evidence" if payload["execution"]["status"] == "completed" else "incomplete"
            return {"state": "dependency_blocked" if blockers else state, "blockers": blockers,
                    "execution_status": payload["execution"]["status"], "mathematical_status": "not_certified"}
        if kind == "arguments":
            objections = self._withdrawals(record)
            pending = self._suspensions(record)
            state = "withdrawn" if objections else "suspended" if pending else "supported" if \
                (payload.get("status") == "proved" or payload.get("tag") == "proved") else "unreviewed"
            if blockers and state not in {"withdrawn", "suspended"}:
                state = "dependency_blocked"
            return {"state": state, "blockers": blockers, "objections": objections,
                    "pending_challenges": pending,
                    "confirmed_objections": self._corrections(kind, record["id"])}
        if kind == "examples":
            properties = {}
            for prop in payload.get("properties", []):
                objections = self._withdrawals(record, prop["id"])
                prop_blockers = blockers + self._dependency_blockers(prop, visiting)
                supporting = research_records.property_support(self, record, prop, visiting)
                state = "withdrawn" if objections else "supported" if prop.get("status") == "checked" or supporting else "unreviewed"
                if prop_blockers and state != "withdrawn":
                    state = "dependency_blocked"
                properties[prop["id"]] = {"state": state, "blockers": prop_blockers, "objections": objections,
                                          "supports": supporting}
            states = {p["state"] for p in properties.values()}
            state = next(iter(states)) if len(states) == 1 else "partially_supported" if "supported" in states else "unreviewed"
            return {"state": state, "properties": properties, "blockers": blockers,
                    "confirmed_objections": self._corrections(kind, record["id"])}
        return {"state": "dependency_blocked" if blockers else "recorded", "blockers": blockers}

    def _dependency_blockers(self, payload: dict, visiting: set | None = None) -> list[dict]:
        blockers = []
        for dependency in payload.get("dependencies", []):
            record = self._resolve_ref(dependency)
            if record["kind"] == "examples" and "property_ids" in dependency:
                record = dict(record, property_ids=dependency["property_ids"])
            trust = self._assess(record, visiting)
            if record["kind"] == "examples":
                ids = dependency.get("property_ids", list(trust.get("properties", {})))
                bad = [p for p in ids if trust.get("properties", {}).get(p, {}).get("state") != "supported"]
                if bad:
                    blockers.append({"ref": _ref(record), "property_ids": bad, "state": trust["state"]})
            elif trust["state"] in {"withdrawn", "dependency_blocked"} or \
                    record["kind"] == "arguments" and trust["state"] != "supported" or \
                    record["kind"] == "claims" and trust["state"] not in \
                    ({"proved", "cited", "recorded"} if "conclusions" not in payload else {"proved", "cited"}) or \
                    record["kind"] == "experiment_result" and trust["state"] != "computational_evidence":
                blockers.append({"ref": _ref(record), "state": trust["state"]})
            elif record["kind"] == "arguments":
                # Keep both local audit receipts intact when a Claim conflicts,
                # but do not let a consumer bypass that conflict by citing only
                # the supporting Argument instead of the Claim itself.
                for conclusion in record["payload"].get("conclusions", []):
                    if conclusion["target"]["kind"] != "claims":
                        continue
                    target = self._resolve_ref(conclusion["target"])
                    if self._assess(target, visiting)["state"] == "conflicted":
                        blockers.append({"ref": _ref(record), "target": _ref(target),
                                         "state": "conflicted", "reason": "dependency_conclusion_conflicted"})
        return blockers

    def _with_trust(self, record: dict, *, project: bool = True) -> dict:
        result = dict(copy.deepcopy(record), current_trust=self._assess(record))
        if project and record["kind"] == "examples" and "property_ids" in record:
            result["payload"]["properties"] = [p for p in result["payload"].get("properties", [])
                                                 if p["id"] in record["property_ids"]]
        if record["kind"] == "proof_state" and "routes" in record["payload"]:
            result["obligations"] = research_records.obligation_view(self, record)
        return result

    def audit_context(self, kind: str, record_id: str, revision: int,
                      property_ids: list[str] | None = None) -> dict:
        """The auditor gets current support and every earlier confirmed objection."""
        with self._locked():
            def selected(ref):
                target = copy.deepcopy(self._resolve_ref(ref))
                ids = ref.get("property_ids", target.get("property_ids"))
                if ids is not None:
                    target["property_ids"] = list(ids)
                    target["payload"]["properties"] = [p for p in target["payload"].get("properties", [])
                                                        if p["id"] in ids]
                return self._with_trust(target)
            record = self._get(_kind(kind), record_id, revision)
            dependencies = [self._with_trust(self._resolve_ref(d))
                            for d in record["payload"].get("dependencies", [])]
            if record["kind"] == "examples":
                for prop in record["payload"].get("properties", []):
                    if property_ids is None or prop["id"] in property_ids:
                        dependencies.extend(self._with_trust(self._resolve_ref(d)) for d in prop.get("dependencies", []))
            objections = self._corrections(record["kind"], record_id) + \
                copy.deepcopy(record.get("current_trust", {}).get("confirmed_objections", []))
            selections = property_ids if record["kind"] == "examples" else [None]
            if selections is None:
                selections = [p["id"] for p in record["payload"].get("properties", [])]
            for property_id in selections:
                for objection in self._withdrawals(record, property_id):
                    if objection not in objections:
                        objections.append(objection)
            return {"record": self._with_trust(record), "dependencies": dependencies,
                    "conclusion_targets": [selected(c["target"])
                                           for c in record["payload"].get("conclusions", [])],
                    "subjects": [selected(ref)
                                 for ref in record["payload"].get("subject_refs", [])],
                    "confirmed_objections": objections}

    def _dependencies(self, payload: dict) -> None:
        dependencies = payload.get("dependencies", [])
        if not isinstance(dependencies, list):
            raise StoreError("dependencies must be a list of versioned record references")
        for dependency in dependencies:
            self._resolve_ref(dependency)

    def _reject_authority(self, value: Any, kind: str, path: tuple = ()) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in _AUTHORITY_FIELDS:
                    raise StoreError(f"{key} is service-owned; reference a review instead")
                if key in {"status", "tag"} and isinstance(child, str) and child in _TRUSTED_LABELS:
                    is_argument_promotion = kind == "arguments" and not path and child == "proved"
                    is_property = kind == "examples" and len(path) == 2 \
                        and path[0] == "properties" and key == "status" and child == "checked"
                    if not (is_argument_promotion or is_property):
                        raise AuditRequired(f"Unsupported trusted label at {'.'.join(map(str, path + (key,)))}")
                self._reject_authority(child, kind, path + (key,))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                self._reject_authority(child, kind, path + (index,))

    def _review_target(self, audit_id: str, kind: str, record_id: str) -> tuple[dict, dict]:
        self._record_id(audit_id)
        review = self._get("reviews", audit_id)["payload"]
        target = review["target"]
        if target["kind"] != kind or target["id"] != record_id:
            raise AuditRequired("Review belongs to a different record")
        reviewed = self._get(kind, record_id, target["revision"])
        return review, reviewed["payload"]

    def _validate_payload(self, kind: str, record_id: str, payload: dict) -> None:
        # Execution metadata may contain arbitrary remote filenames and package
        # names. It is service-owned factual data, never mathematical authority.
        self._reject_authority({k: v for k, v in payload.items() if k != "execution"}
                               if kind == "experiment_result" else payload, kind)
        self._dependencies(payload)
        research_records.prepare_links(self, kind, payload)
        research_records.validate_workflow(self, kind, payload)
        if kind == "claims" and (payload.get("status") in {"refuted", "conflicted"}
                                 or payload.get("tag") in {"refuted", "conflicted"}):
            raise AuditRequired("Claim evidence state is derived from audited conclusions")
        if kind == "experiment_result":
            self._validate_experiment(payload)
        if kind == "arguments":
            if payload.get("status") == "proved" or payload.get("tag") == "proved":
                if not isinstance(payload.get("audit_id"), str):
                    raise AuditRequired("proved arguments require audit_id")
                review, reviewed = self._review_target(payload["audit_id"], kind, record_id)
                if review["verdict"] != "pass" or not json_equal(evidence_body(payload), evidence_body(reviewed)):
                    raise AuditRequired("A passing review of this exact argument and dependencies is required")
                if payload.get("conclusions"):
                    from colombo.cell.verifier.review_validation import validate_conclusion_results
                    try:
                        validate_conclusion_results(payload["conclusions"], review.get("conclusions", []), review["verdict"])
                    except ValueError as exc:
                        raise AuditRequired("The review must cover each exact conclusion and direction") from exc
                proposed = {"kind": kind, "id": record_id, "payload": payload}
                if self._withdrawals(proposed) or self._suspensions(proposed) or self._dependency_blockers(payload):
                    raise AuditRequired("Argument support is suspended or withdrawn, or a pinned dependency is not usable; resolve the review or repair and re-audit")
        if kind == "examples":
            properties = payload.get("properties", [])
            if not isinstance(properties, list):
                raise StoreError("Example properties must be a list")
            seen = set()
            for prop in properties:
                if not isinstance(prop, dict) or not isinstance(prop.get("id"), str) \
                        or not prop["id"] or prop["id"] in seen:
                    raise StoreError("Example properties need unique nonempty string ids")
                seen.add(prop["id"])
                self._dependencies(prop)
                if prop.get("status", "pending") not in {"pending", "checked"}:
                    raise StoreError("Example property status must be pending or checked")
                if prop.get("status") != "checked":
                    continue
                if not isinstance(prop.get("audit_id"), str):
                    raise AuditRequired("checked properties require audit_id")
                review, reviewed = self._review_target(prop["audit_id"], kind, record_id)
                results = {p["id"]: p for p in review.get("properties", [])}
                old_properties = {p["id"]: p for p in reviewed.get("properties", [])}
                base = {k: v for k, v in payload.items() if k != "properties"}
                old_base = {k: v for k, v in reviewed.items() if k != "properties"}
                if review["verdict"] == "service_error" or results.get(prop["id"], {}).get("verdict") != "pass" \
                        or prop["id"] not in old_properties \
                        or not json_equal(evidence_body(base), evidence_body(old_base)) \
                        or not json_equal(evidence_body(prop), evidence_body(old_properties[prop["id"]])):
                    raise AuditRequired("Property or construction differs from its passing review")
                if self._withdrawals({"kind": kind, "id": record_id, "payload": payload}, prop["id"]) \
                        or self._dependency_blockers(payload) or self._dependency_blockers(prop):
                    raise AuditRequired("Property support was withdrawn or a pinned dependency is not usable; repair and re-audit")

    def _append(self, kind: str, payload: dict, record_id: str | None,
                expected_revision: int | None, request_id: str | None, request_input: dict) -> dict:
        requests = self._read(".requests.json", {})
        if not isinstance(requests, dict):
            raise StoreError("Invalid idempotency registry")
        if request_id is not None and request_id in requests:
            previous = requests[request_id]
            if not json_equal(previous["input"], request_input):
                raise StoreError("request_id was already used for different input")
            if self._context_has_id(kind, previous["result"]["id"]):
                raise StoreError("Cannot write or shadow a read-only context record")
            return copy.deepcopy(previous["result"])
        collection = self._collection(kind)
        record_id = record_id or f"{kind.rstrip('s')}-{uuid4().hex[:16]}"
        if self._context_has_id(kind, record_id):
            raise StoreError("Cannot write or shadow a read-only context record; create a new id")
        existing = [r for r in collection["records"] if r["id"] == record_id]
        if existing:
            current_revision = max(r["revision"] for r in existing)
            if expected_revision != current_revision:
                raise RevisionConflict(f"Expected revision {expected_revision}; current revision is {current_revision}")
            revision = current_revision + 1
        else:
            if expected_revision is not None:
                raise RevisionConflict("Cannot set expected_revision for a new record")
            revision = 1
        if kind in WRITABLE_KINDS:
            prior = max(existing, key=lambda r: r["revision"])["payload"] if existing else None
            research_records.validate_identity(kind, prior, payload)
            self._validate_payload(kind, record_id, payload)
        record = self._envelope(kind, payload, record_id, revision)
        collection["records"].append(record)
        events = self._collection("events")
        sequence = len(events["records"]) + 1
        event_payload = {"sequence": sequence, "action": "review" if kind == "reviews" else "archive",
                         "target": {"kind": kind, "id": record_id, "revision": revision},
                         "request_id": request_id}
        events["records"].append(self._envelope("events", event_payload, f"event-{sequence:08d}", 1))
        writes = {f"{kind}.json": collection, "events.json": events}
        if request_id is not None:
            requests[request_id] = {"input": request_input, "result": record}
            writes[".requests.json"] = requests
        self._commit(writes)
        return copy.deepcopy(record)

    def archive(self, kind: str, payload: dict, record_id: str | None = None,
                expected_revision: int | None = None, request_id: str | None = None) -> dict:
        kind = _kind(kind, writable=True)
        if not isinstance(payload, dict):
            raise StoreError("payload must be a JSON object")
        if record_id is not None:
            self._record_id(record_id)
        _revision(expected_revision)
        self._request_id(request_id)
        payload = json.loads(_json(payload))
        request_input = copy.deepcopy({"kind": kind, "payload": payload, "record_id": record_id,
                                    "expected_revision": expected_revision})
        with self._locked():
            payload = research_records.prepare_links(self, kind, payload)
            if kind == "experiment_result":
                if record_id is None:
                    raise StoreError("Experiment execution records are created by the experiment service")
                try:
                    existing = self._get(kind, record_id)["payload"]
                except KeyError as exc:
                    raise StoreError("Experiment execution records are created by the experiment service") from exc
                for key, value in payload.items():
                    if key not in _EXPERIMENT_INTERPRETATION and (key not in existing or existing[key] != value):
                        raise StoreError(f"Experiment field {key} is service-owned")
                payload = {**existing, **payload}
            return self._with_trust(self._append(kind, payload, record_id, expected_revision, request_id, request_input))

    def _validate_experiment(self, payload: dict) -> None:
        if not isinstance(payload.get("question"), str) or not payload["question"].strip():
            raise StoreError("An experiment needs its mathematical question")
        self._resolve_ref(payload.get("target_ref"))
        execution = payload.get("execution")
        if not isinstance(execution, dict) or execution.get("status") not in _EXPERIMENT_STATUSES:
            raise StoreError("Invalid experiment execution status")
        if not isinstance(payload.get("parameters", {}), dict):
            raise StoreError("Experiment parameters must be an object")
        try:
            files = read_artifact_groups(self.memory_dir.parent, [experiment_group(payload)], settings=self.settings)
        except (ValueError, OSError) as exc:
            raise StoreError(str(exc)) from exc
        if execution["status"] == "completed" and not files:
            raise StoreError("Completed experiments need preserved execution artifacts")

    def write_experiment_result(self, record_id: str, payload: dict, *,
                                expected_revision: int | None = None,
                                request_id: str | None = None) -> dict:
        """Trusted execution service; agents use archive only for interpretations."""
        self._record_id(record_id)
        _revision(expected_revision)
        self._request_id(request_id)
        payload = json.loads(_json(payload))
        if not isinstance(payload, dict):
            raise StoreError("Experiment payload must be an object")
        request_input = copy.deepcopy({"service": "experiment", "id": record_id, "payload": payload,
                                    "expected_revision": expected_revision})
        with self._locked():
            if request_id is not None and request_id in self._read(".requests.json", {}):
                return self._with_trust(self._append("experiment_result", payload, record_id,
                                                    expected_revision, request_id, request_input))
            prior = [r for r in self._collection("experiment_result")["records"] if r["id"] == record_id]
            if prior:
                latest = max(prior, key=lambda r: r["revision"])
                old = latest["payload"]
                if expected_revision is None:
                    expected_revision = latest["revision"]
                for key in old.keys() | payload.keys():
                    if key not in {"execution", "artifacts"} | _EXPERIMENT_INTERPRETATION and old.get(key) != payload.get(key):
                        raise StoreError(f"An experiment rerun needs a new id; {key} cannot change")
                for key in _EXPERIMENT_INTERPRETATION:
                    if key in old:
                        payload[key] = copy.deepcopy(old[key])
                before, after = old["execution"], payload["execution"]
                fixed = {"backend", "model", "container_id", "response_id", "started_at", "deadline_at",
                         "total_deadline_at", "artifact_limits"}
                for key, value in before.items():
                    if value is not None and (key in fixed or before["status"] == "completed") and after.get(key) != value:
                        raise StoreError(f"Recorded execution field {key} cannot change")
                new_files = {f["path"]: f for f in payload["artifacts"]}
                if any(new_files.get(f["path"]) != f for f in old["artifacts"]):
                    raise StoreError("Previously published experiment artifacts cannot be removed or replaced")
                if payload == old and request_id is None and expected_revision == latest["revision"]:
                    self._validate_experiment(payload)
                    return self._with_trust(latest)
            return self._with_trust(self._append("experiment_result", payload, record_id,
                                                expected_revision, request_id, request_input))

    def retrieve(self, query: str = "", kinds: list[str] | None = None,
                 record_id: str | None = None, revision: int | None = None, limit: int | None = None,
                 include_context: bool | None = None, *, target_ref: dict | None = None,
                 relations: list[str] | None = None, route_id: str | None = None,
                 state_filter: dict | None = None, since_event: dict | None = None,
                 cursor: dict | None = None, detail: str = "full") -> dict:
        if any(value is not None for value in (target_ref, relations, route_id, state_filter, since_event, cursor)) or detail != "full":
            from colombo.cell.record_queries import query as research_query
            return research_query(self, query, kinds, record_id, revision, limit, include_context,
                                  target_ref=target_ref, relations=relations, route_id=route_id,
                                  state_filter=state_filter, since_event=since_event, cursor=cursor, detail=detail)
        retrieval = self.settings["retrieval"]
        if limit is None:
            limit = retrieval["memory_results"]
        if include_context is None:
            include_context = retrieval["include_context"]
        if not isinstance(query, str):
            raise StoreError("query must be a string")
        if type(limit) is not int or not 1 <= limit <= retrieval["max_memory_results"]:
            raise StoreError(f"limit must be between 1 and {retrieval['max_memory_results']}")
        if type(include_context) is not bool:
            raise StoreError("include_context must be a boolean")
        if kinds is not None and (not isinstance(kinds, list) or not kinds):
            raise StoreError("kinds must be a nonempty list or None")
        selected = sorted(READABLE_KINDS - {"events"}) if kinds is None else list(dict.fromkeys(_kind(k) for k in kinds))
        if record_id is not None:
            self._record_id(record_id)
        _revision(revision)
        if revision is not None and record_id is None:
            raise StoreError("revision requires record_id")
        terms = query.casefold().split()
        with self._locked():
            matches = []
            for kind in selected:
                records = self._collection(kind)["records"]
                if include_context:
                    if any(self._context_has_id(kind, r["id"]) for r in records):
                        raise StoreError("Local record collides with a read-only context identity")
                    records += self._context_records(kind)
                current = {}
                for record in records:
                    if record_id is not None and record["id"] != record_id:
                        continue
                    if revision is not None and record["revision"] != revision:
                        continue
                    if record["id"] not in current or record["revision"] > current[record["id"]]["revision"]:
                        current[record["id"]] = record
                for record in current.values():
                    searchable = _json(record["payload"]).casefold() + " " + record["id"].casefold()
                    if all(term in searchable for term in terms):
                        matches.append(record)
            matches.sort(key=lambda r: (r["created_at"], r["kind"], r["id"]), reverse=True)
            return {"records": [self._with_trust(r) for r in matches[:limit]], "count": len(matches),
                    "returned": min(limit, len(matches))}

    def write_review(self, review: dict) -> dict:
        """Trusted service only: validate and persist an immutable audit report.

        Required target: {kind, id, revision}. Example property
        results use [{id, verdict, ...}]. An overall fail/uncertain report may
        still contain individual passing properties. ``request_id`` is optional
        service retry metadata and is removed from the stored report body.
        """
        if not isinstance(review, dict):
            raise StoreError("review must be a JSON object")
        review = json.loads(_json(review))
        request_id = review.pop("request_id", None)
        self._request_id(request_id)
        target = review.get("target")
        if not isinstance(target, dict) or not {"kind", "id", "revision"} <= target.keys():
            raise StoreError("Review target requires kind, id and revision")
        target["kind"] = _kind(target["kind"])
        if target["kind"] not in {"arguments", "examples"}:
            raise StoreError("Local audits target arguments or examples")
        self._record_id(target["id"])
        _revision(target["revision"])
        if target["revision"] is None or review.get("verdict") not in VERDICTS:
            raise StoreError("Review needs a pinned target revision and supported verdict")
        properties = review.get("properties", [])
        if not isinstance(properties, list):
            raise StoreError("Review properties must be a list")
        with self._locked():
            record = self._get(target["kind"], target["id"], target["revision"])
            if record["payload"].get("conclusions") and review["verdict"] != "service_error":
                from colombo.cell.verifier.review_validation import validate_conclusion_results
                validate_conclusion_results(record["payload"]["conclusions"], review.get("conclusions", []), review["verdict"])
            target_ids = {p["id"] for p in record["payload"].get("properties", [])} \
                if target["kind"] == "examples" else set()
            seen = set()
            for prop in properties:
                if not isinstance(prop, dict) or not isinstance(prop.get("id"), str) \
                        or prop["id"] not in target_ids or prop["id"] in seen \
                        or prop.get("verdict") not in VERDICTS:
                    raise StoreError("Invalid or repeated reviewed property")
                seen.add(prop["id"])
                if review["verdict"] == "pass" and prop["verdict"] != "pass":
                    raise StoreError("Passing review cannot contain failing or uncertain properties")
            request_input = copy.deepcopy({"operation": "write_review", "payload": review})
            return self._append("reviews", review, None, None, request_id, request_input)

    def _challenge_artifact(self, challenge_id: str, path: Path, expected_value: dict | None = None) -> dict:
        directory = self.memory_dir.parent / "challenges" / challenge_id
        candidate = Path(path)
        resolved = candidate.resolve()
        if directory.resolve() != directory or candidate.is_symlink() or not resolved.is_relative_to(directory):
            raise StoreError("Challenge artifacts must belong to the ordinary challenge directory")
        try:
            raw = resolved.read_bytes()
            value = json.loads(raw)
        except (OSError, ValueError) as exc:
            raise StoreError("Cannot read a saved challenge artifact") from exc
        if expected_value is not None and not json_equal(value, expected_value):
            raise StoreError("Challenge artifact does not match the submitted report")
        return value

    def begin_argument_challenge(self, challenge_id: str, target_ref: dict, reason: str,
                                 evidence_refs: list[dict]) -> dict:
        """Service-only suspension of fixed evidence while an objection is unresolved."""
        self._record_id(challenge_id)
        if not isinstance(reason, str) or not reason.strip() or not isinstance(evidence_refs, list):
            raise StoreError("A challenge needs a concrete reason and selected evidence references")
        identity = {"challenge_id": challenge_id, "target_ref": target_ref, "reason": reason,
                    "evidence_refs": evidence_refs}
        frozen = self._challenge_artifact(challenge_id,
            self.memory_dir.parent / "challenges" / challenge_id / "input.json")
        if any(frozen.get(key) != identity[key] for key in ("challenge_id", "target_ref", "reason", "evidence_refs")):
            raise StoreError("Challenge identity differs from its frozen input")
        with self._locked():
            previous = self._challenge_states().get(challenge_id)
            if previous is not None:
                if any(previous["payload"].get(key) != value for key, value in identity.items()):
                    raise StoreError("Challenge identifier belongs to different frozen evidence")
                return copy.deepcopy(previous)
            record = self._resolve_ref(target_ref)
            payload = record["payload"]
            if record["kind"] != "arguments" or record.get("read_only"):
                raise StoreError("Only a local Argument can be challenged by its owning task")
            if not (payload.get("status") == "proved" or payload.get("tag") == "proved") or not payload.get("audit_id"):
                raise StoreError("A challenge must target a historically certified Argument")
            original_review, reviewed = self._review_target(payload["audit_id"], "arguments", record["id"])
            if original_review.get("verdict") != "pass" or not json_equal(evidence_body(payload), evidence_body(reviewed)):
                raise StoreError("The target does not have a matching historical certificate")
            for reference in evidence_refs:
                self._resolve_ref(reference)
            basis = support_body(payload)
            ids, certificates = {payload["audit_id"]}, []
            for review in self._collection("reviews")["records"] + self._context_records("reviews"):
                value, target = review["payload"], review["payload"].get("target", {})
                if value.get("verdict") != "pass" or target.get("kind") != "arguments":
                    continue
                old = self._resolve_ref(target)
                if json_equal(support_body(old["payload"]), basis) or review["id"] in ids:
                    ids.add(review["id"])
                    certificates.append({"review_ref": _ref(review), "target": copy.deepcopy(target)})
            value = {"type": "argument_challenge", **copy.deepcopy(identity), "status": "pending",
                     "basis": basis, "audit_ids": sorted(ids), "certificates": certificates,
                     "corrections": []}
            identifier = "challenge-" + challenge_id
            return self._append("reviews", value, identifier, None, None, copy.deepcopy(identity))

    def resolve_argument_challenge(self, challenge_id: str, *, outcome: str, report_revision: int,
                                   first_report: dict, first_report_path: Path,
                                   confirmation: dict | None = None, confirmation_path: Path | None = None) -> dict:
        """Save a checked disposition; never edit the Argument or an old certificate."""
        self._record_id(challenge_id)
        if type(report_revision) is not int or report_revision < 1:
            raise StoreError("report_revision must identify a positive report version")
        if outcome not in {"withdrawn", "dismissed"}:
            raise StoreError("Only a completed review can resolve an Argument challenge")
        from colombo.cell.verifier.challenge import validate_first_report
        from colombo.cell.verifier.challenge import validate_confirmation
        try:
            validate_first_report(first_report, challenge_id=challenge_id)
            if first_report["verdict"] != ("sustain" if outcome == "withdrawn" else "dismiss"):
                raise StoreError("Disposition does not match the first report")
            self._challenge_artifact(challenge_id, first_report_path, first_report)
            if confirmation is None:
                if outcome == "withdrawn" or confirmation_path is not None:
                    raise StoreError("Withdrawal requires an independent confirmation")
            else:
                validate_confirmation(confirmation, first_report, challenge_id=challenge_id,
                                      report_revision=report_revision)
                if confirmation["verdict"] != "confirmed":
                    raise StoreError("A disputed review cannot resolve the challenge")
                self._challenge_artifact(challenge_id, confirmation_path, confirmation)
        except StoreError:
            raise
        except Exception as exc:
            raise StoreError(f"Invalid challenge disposition: {exc}") from exc
        with self._locked():
            previous = self._challenge_states().get(challenge_id)
            if previous is None:
                raise StoreError("No matching pending challenge exists")
            value = copy.deepcopy(previous["payload"])
            frozen = self._challenge_artifact(challenge_id,
                self.memory_dir.parent / "challenges" / challenge_id / "input.json")
            if confirmation is None:
                state_path = self.memory_dir.parent / "challenges" / challenge_id / "state.json"
                state = {}
                if state_path.exists():
                    if state_path.is_symlink() or state_path.resolve() != state_path:
                        raise StoreError("Challenge controller state cannot redirect outside its directory")
                    try:
                        state = json.loads(state_path.read_text(encoding="utf-8"))
                    except (OSError, ValueError) as exc:
                        raise StoreError("Cannot validate challenge controller state") from exc
                    if state.get("challenge_id") != challenge_id:
                        raise StoreError("Challenge controller state differs from the frozen input")
                if state.get("had_adverse_report") or frozen.get("initial_audit", {}).get("payload", {}).get("verdict") == "fail":
                    raise StoreError("A dismissal following an adverse report requires independent confirmation")
            resolution = {"status": outcome, "report_revision": report_revision,
                          "first_report_path": str(Path(first_report_path).resolve().relative_to(self.memory_dir.parent)),
                          "confirmation_path": str(Path(confirmation_path).resolve().relative_to(self.memory_dir.parent))
                          if confirmation_path is not None else None}
            if value["status"] != "pending":
                if any(value.get(key) != val for key, val in resolution.items()):
                    raise StoreError("A completed challenge cannot be overwritten")
                return copy.deepcopy(previous)
            value.update(resolution)
            value["corrections"] = [{"target": copy.deepcopy(value["target_ref"]), "property_id": None,
                                      "basis": value["basis"], "audit_ids": value["audit_ids"],
                                      "certificates": value["certificates"], "finding": copy.deepcopy(finding)}
                                     for finding in first_report["findings"]] if outcome == "withdrawn" else []
            return self._append("reviews", value, previous["id"], previous["revision"], None, copy.deepcopy(value))

    def apply_confirmed_review(self, *, review_id: str, report_revision: int, report: dict,
                               confirmation: dict,
                               record_refs: list[dict], report_path: Path,
                               confirmation_path: Path) -> dict:
        """Service-only reconciliation of a completed independent report check.

        One immutable review transaction records all corrections. Mathematical
        payloads and old audit reports are never changed.
        The verifier remains responsible for checking its frozen input bundle.
        This is deliberately not an MCP operation.
        """
        self._record_id(review_id)
        directory = (self.memory_dir.parent / "reviews" / review_id).resolve()
        for path, expected_value in (
                (report_path, report), (confirmation_path, confirmation)):
            path = Path(path)
            resolved = path.resolve()
            if path.is_symlink() or not resolved.is_relative_to(directory):
                raise StoreError("Confirmed review artifacts must belong to this review directory")
            raw = resolved.read_bytes()
            if not json_equal(json.loads(raw), expected_value):
                raise StoreError("Confirmed review artifact does not match the submitted report")
        if confirmation.get("verdict") != "confirmed" or confirmation.get("review_id") != review_id \
                or type(report_revision) is not int or report_revision < 1 \
                or type(confirmation.get("report_revision")) is not int \
                or confirmation["report_revision"] != report_revision:
            raise StoreError("Review is not independently confirmed for this exact input and report")
        sections = {"target_alignment", "coverage", "reasoning", "sources", "record_mapping"}
        assessment = confirmation.get("assessment", {})
        checks = confirmation.get("covered_check_ids", [])
        actual_checks = [check.get("id") for check in report.get("checks", [])]
        if set(assessment) != sections or any(v.get("status") != "supported" for v in assessment.values()) \
                or not actual_checks or any(type(value) is not int or value < 1 for value in actual_checks) \
                or len(actual_checks) != len(set(actual_checks)) \
                or any(type(value) is not int for value in checks) or sorted(checks) != sorted(actual_checks):
            raise StoreError("Independent confirmation must support all review assessments and checks")
        findings = report.get("findings", [])
        if report.get("verdict") not in {"pass", "revise", "inconclusive"}:
            raise StoreError("A completed mathematical report is required")
        expected_ids = [f["id"] for f in findings]
        responses = confirmation.get("findings", [])
        if len(expected_ids) != len(set(expected_ids)) \
                or sorted(r.get("finding_id", "") for r in responses) != sorted(expected_ids) \
                or any(r.get("status") != "supported" for r in responses) \
                or not confirmation.get("decisive_steps") \
                or any(s.get("status") != "supported" for s in confirmation["decisive_steps"]) \
                or confirmation.get("new_findings") != []:
            raise StoreError("Disputed or incomplete findings cannot change memory support")
        if not isinstance(record_refs, list):
            raise StoreError("record_refs must be a list")
        with self._locked():
            bound = {}
            for ref in record_refs:
                record = self._resolve_ref(ref)
                key = (record["kind"], record["id"], record["revision"])
                selection = set(ref.get("property_ids", [p["id"] for p in record["payload"].get("properties", [])]))
                bound.setdefault(key, set()).update(selection)
            corrections = []
            for finding in findings:
                if finding.get("scope", "draft") != "record" or finding.get("kind") not in {"error", "gap"}:
                    continue
                if not finding.get("affected_refs"):
                    raise StoreError("Record finding requires exact affected_refs")
                for ref in finding["affected_refs"]:
                    record = self._resolve_ref(ref)
                    key = (record["kind"], record["id"], record["revision"])
                    if key not in bound or record["kind"] not in {"arguments", "examples"}:
                        raise StoreError("Correction must name a submitted argument or example version")
                    selections = ref.get("property_ids", sorted(bound[key])) if record["kind"] == "examples" else [None]
                    if record["kind"] == "examples" and (not selections or not set(selections) <= bound[key]):
                        raise StoreError("Correction exceeds the submitted example properties")
                    for property_id in selections:
                        payload = record["payload"]
                        if property_id is None:
                            basis = support_body(payload)
                            ids = {payload["audit_id"]} if payload.get("audit_id") else set()
                        else:
                            prop = next(p for p in payload["properties"] if p["id"] == property_id)
                            basis = copy.deepcopy({"base": support_body({k: v for k, v in payload.items() if k != "properties"}),
                                                  "property": support_body(prop)})
                            ids = {prop["audit_id"]} if prop.get("audit_id") else set()
                        certificates = []
                        # A micro-audit targets the candidate version, while a
                        # submitted record commonly names its promoted revision.
                        # Bind both versions through the exact reviewed evidence.
                        for local in self._collection("reviews")["records"] + self._context_records("reviews"):
                            value = local["payload"]
                            target = value.get("target", {})
                            if target.get("kind") != record["kind"] or target.get("id") != record["id"]:
                                continue
                            old = self._resolve_ref(target)
                            if property_id is None:
                                same = value.get("verdict") == "pass" and json_equal(support_body(old["payload"]), basis)
                            else:
                                oldprop = next((p for p in old["payload"].get("properties", []) if p["id"] == property_id), None)
                                oldbase = {k: v for k, v in old["payload"].items() if k != "properties"}
                                same = oldprop is not None and any(p["id"] == property_id and p["verdict"] == "pass" for p in value.get("properties", [])) \
                                    and json_equal({"base": support_body(oldbase), "property": support_body(oldprop)}, basis)
                            if same or local["id"] in ids:
                                ids.add(local["id"])
                                certificates.append({"review_ref": _ref(local), "target": target})
                        corrections.append({"target": _ref(record), "property_id": property_id,
                                            "basis": basis, "audit_ids": sorted(ids),
                                            "certificates": certificates, "finding": copy.deepcopy(finding)})
            if corrections and report["verdict"] == "pass":
                raise StoreError("Passing report cannot withdraw support for confirmed errors or gaps")
            payload = {"type": "confirmed_review", "review_id": review_id, "report_revision": report_revision,
                       "report_path": str(Path(report_path).resolve().relative_to(self.memory_dir.parent)),
                       "confirmation_path": str(Path(confirmation_path).resolve().relative_to(self.memory_dir.parent)),
                       "record_refs": copy.deepcopy(record_refs), "corrections": corrections}
            request_id = f"confirmed:{review_id}:{report_revision}"
            # Only the confirmed input identifies a retry. Later local audits
            # must not change this transaction's request_input or its old evidence.
            request_input = {"identity": {k: v for k, v in payload.items() if k != "corrections"},
                             "report": copy.deepcopy(report), "confirmation": copy.deepcopy(confirmation)}
            result = self._append("reviews", payload, None, None, request_id, request_input)
            saved_corrections = result["payload"]["corrections"]
            return {"review_ref": _ref(result), "correction_count": len(saved_corrections),
                    "affected_refs": [c["target"] for c in saved_corrections]}
