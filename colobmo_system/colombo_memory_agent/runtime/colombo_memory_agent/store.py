"""The single trusted writer for scientific memory; no proof scheduler."""
from __future__ import annotations
from contextlib import contextmanager
from copy import deepcopy
import os
from pathlib import Path
import shutil
import tempfile
import uuid
from colombo.memory.contracts import (ContractError, LIBRARIES, canonical_bytes, dependencies,
                                     digest, safe_id, validate_record, validate_review)
from colombo.memory.store import Store as ReadStore, atomic_json, now, read_json


def _restore_files(backups: dict[Path, bytes | None]) -> None:
    """Restore exact prior bytes atomically, including pointers replaced before an interruption."""
    for path, data in backups.items():
        if data is None:
            path.unlink(missing_ok=True)
            continue
        fd, temporary = tempfile.mkstemp(prefix=".rollback-", dir=path.parent)
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(data); f.flush(); os.fsync(f.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


class WriterStore(ReadStore):
    @contextmanager
    def writer(self):
        created_state = not self.state_root.exists()
        self.state_root.mkdir(parents=True, exist_ok=True)
        lock = self.state_root / ".writer.lock"
        try:
            lock.mkdir()
        except FileExistsError as exc:
            raise ContractError("Writer lock exists. Inspect its owner; never auto-delete a possibly live lock.") from exc
        try:
            atomic_json(lock / "owner.json", {"pid": os.getpid(), "created_at": now()})
            yield
        finally:
            shutil.rmtree(lock, ignore_errors=True)
            if created_state and self.state_root.exists() and not any(self.state_root.iterdir()):
                self.state_root.rmdir()

    def initialize(self) -> dict:
        with self.writer():
            if (self.state_root / "CURRENT.json").exists():
                return self.manifest()
            if self.root.exists() and any(self.root.iterdir()):
                raise ContractError("Nonempty unrecognized library: migrate explicitly, never initialize over it")
            if any(p.name != ".writer.lock" for p in self.state_root.iterdir()):
                raise ContractError("Unrecognized state directory; inspect before initialization")
            for library in set(LIBRARIES.values()):
                (self.root / library).mkdir(parents=True, exist_ok=True)
            for directory in ("staging", ".generations", "history", "cache"):
                (self.state_root / directory).mkdir(parents=True, exist_ok=True)
            manifest = {"schema": "colombo-memory-catalog/2", "entries": {}, "receipts": {}, "sequence": 0}
            self._commit_generation(manifest)
            return manifest

    def _object_path(self, record: dict) -> str:
        return f"history/{LIBRARIES[record['kind']]}/{safe_id(record['id'])}/r{record['revision']:06d}-{digest(record)}.json"

    def _commit_generation(self, manifest: dict) -> None:
        from .index_builder import build_index
        generation = "g-" + uuid.uuid4().hex
        target = self._state_inside(".generations/" + generation)
        target.mkdir(parents=True)
        records = self.all_records(manifest)
        build_index(target / "catalog.sqlite", records, tier="published")
        atomic_json(target / "manifest.json", manifest)
        # Generation and all derived data exist before visibility changes.
        atomic_json(self.state_root / "CURRENT.json", {"generation": generation, "manifest_hash": digest(manifest)})

    def _save_lead_catalog(self, records: list[dict]) -> None:
        """Derived index and references only; no second directory of scientific JSON."""
        from .index_builder import build_index
        name = "cache/leads-" + uuid.uuid4().hex
        directory = self._state_inside(name)
        directory.mkdir(parents=True)
        build_index(directory / "catalog.sqlite", records, tier="lead")
        entries = {r["id"]: {"kind": r["kind"], "content_hash": digest(r),
                   "path": f"{LIBRARIES[r['kind']]}/{r['id']}.json"} for r in records}
        atomic_json(self.state_root / "LEADS.json", {"schema": "colombo-four-library-leads/1",
                    "path": name, "entries": entries, "count": len(entries), "created_at": now()})

    def install_leads(self, records: list[dict]) -> dict:
        """Put candidates directly in their scientific libraries, without promoting evidence."""
        with self.writer():
            known = {r["id"]: r for r in self.lead_records()}
            published = self.manifest()["entries"]
            prepared = []
            for original in records:
                r = deepcopy(original); r["revision"] = None
                if r["evidence"]["readiness"] != "lead":
                    raise ContractError("install-leads cannot bypass review for a reference")
                validate_record(r)
                if r["id"] in published:
                    raise ContractError("Do not overwrite a published record with a lead; use prepare/review/publish")
                if r["id"] in known and known[r["id"]]["kind"] != r["kind"]:
                    raise ContractError("Changing scientific kind needs explicit reconciliation")
                known[r["id"]] = r; prepared.append(r)
            previous = {self.current_path(r["id"], r["kind"]):
                        (self.current_path(r["id"], r["kind"]).read_bytes()
                         if self.current_path(r["id"], r["kind"]).exists() else None) for r in prepared}
            lead_pointer = self.state_root / "LEADS.json"
            previous[lead_pointer] = lead_pointer.read_bytes() if lead_pointer.exists() else None
            try:
                for r in prepared:
                    atomic_json(self.current_path(r["id"], r["kind"]), r)
                self._save_lead_catalog(list(known.values()))
            except BaseException:
                _restore_files(previous)
                raise
            return {"installed_leads": len(records), "total_leads": len(known), "published": 0}

    def prepare(self, records: list[dict], *, curator_run_id: str, job_id: str,
                base_revisions: dict[str, int | None] | None = None) -> dict:
        safe_id(curator_run_id); safe_id(job_id)
        if not records:
            raise ContractError("Empty proposal")
        with self.writer():
            manifest = self.manifest(); ids = [r["id"] for r in records]
            if len(ids) != len(set(ids)):
                raise ContractError("Duplicate record IDs in proposal")
            lead_entries = self.lead_manifest()["entries"]
            for candidate in records:
                prior = manifest["entries"].get(candidate["id"], lead_entries.get(candidate["id"]))
                if prior is not None and prior["kind"] != candidate["kind"]:
                    raise ContractError("Changing scientific kind needs explicit reconciliation")
            bases = {i: manifest["entries"].get(i, {}).get("revision") for i in ids}
            if base_revisions is not None and base_revisions != bases:
                raise ContractError("Base revision conflict")
            revisions = {i: (bases[i] or 0) + 1 for i in ids}
            prepared = deepcopy(records)
            for r in prepared:
                safe_id(r["id"]); r["revision"] = revisions[r["id"]]
                # Bind new batch references before review, never after it.
                for s in r["source_refs"]:
                    if s["source_revision"] is None:
                        s["source_revision"] = revisions.get(s["source_id"], manifest["entries"].get(s["source_id"], {}).get("revision"))
                for link in r["links"]:
                    if link["relation"] != "related" and link["target_revision"] is None:
                        link["target_revision"] = revisions.get(link["target_id"], manifest["entries"].get(link["target_id"], {}).get("revision"))
                validate_record(r, require_revision=True)
                for dep, rev in dependencies(r):
                    possible = revisions.get(dep) or manifest["entries"].get(dep, {}).get("revision")
                    if rev is None or (rev != possible and not self._revision_exists(dep, rev, manifest)):
                        raise ContractError(f"Unresolved dependency {dep}@{rev}")
            by_id = {r["id"]: r for r in prepared}
            for r in prepared:
                if r["evidence"]["readiness"] != "reference":
                    continue
                for src in r["source_refs"]:
                    target = by_id.get(src["source_id"])
                    if target is None or target["revision"] != src["source_revision"]:
                        target = None
                        item = manifest["entries"].get(src["source_id"])
                        if item and item["revision"] == src["source_revision"]:
                            target = self.get(src["source_id"])
                        else:
                            for receipt in manifest["receipts"].values():
                                for fixed in receipt["published_refs"]:
                                    if fixed["id"] == src["source_id"] and fixed["revision"] == src["source_revision"]:
                                        target = self.get(fixed["id"], revision=fixed["revision"], content_hash=fixed["content_hash"], kind=fixed["kind"])
                    if target is None or target["kind"] != "source":
                        raise ContractError("source_ref must resolve to a Source record")
                    actual = target["content"].get("bibliographic_identity", {}).get("version")
                    if actual != src["source_version"]:
                        raise ContractError(f"Source version mismatch: {src['source_id']}: {src['source_version']} != {actual}")
            p = {"schema": "colombo-memory-proposal/2", "proposal_id": "proposal-" + uuid.uuid4().hex,
                 "job_id": job_id, "curator_run_id": curator_run_id, "created_at": now(),
                 "base_revisions": bases, "records": prepared}
            p["digest"] = digest(p)
            atomic_json(self.state_root / "staging" / p["proposal_id"] / "proposal.json", p)
            return p

    def _revision_exists(self, ident: str, rev: int, manifest: dict) -> bool:
        # Scientific dependencies must refer to a published revision, not an abandoned proposal.
        for receipt in manifest["receipts"].values():
            if any(x["id"] == ident and x["revision"] == rev for x in receipt["published_refs"]):
                return True
        return manifest["entries"].get(ident, {}).get("revision") == rev

    def load_proposal(self, ident: str) -> dict:
        safe_id(ident)
        p = read_json(self.state_root / "staging" / ident / "proposal.json")
        raw = {k: v for k, v in p.items() if k != "digest"}
        if digest(raw) != p["digest"]:
            raise ContractError("Proposal was modified after preparation")
        return p

    def publish(self, proposal: dict, review: dict, *, authorized: bool,
                allow_test_receipt: bool = False) -> dict:
        if not authorized:
            raise ContractError("Publication not authorized by the caller")
        if review.get("backend") == "fake" and not allow_test_receipt:
            raise ContractError("Simulation reviews cannot authorize production publication")
        validate_review(proposal, review)
        raw = {k: v for k, v in proposal.items() if k != "digest"}
        if digest(raw) != proposal["digest"]:
            raise ContractError("Proposal digest mismatch")
        with self.writer():
            manifest = self.manifest()
            if proposal["digest"] in manifest["receipts"]:
                return manifest["receipts"][proposal["digest"]]
            records = {r["id"]: r for r in proposal["records"]}
            accepted = {i["id"] for i in review["items"] if i["decision"] == "accept"}
            withheld = {i: "not accepted by the independent reviewer" for i in records if i not in accepted}
            # Dependent objects wait; independent accepted objects may advance.
            changed = True
            while changed:
                changed = False
                for ident in list(accepted):
                    for dep, rev in dependencies(records[ident]):
                        if dep in records and rev == records[dep]["revision"] and dep not in accepted:
                            accepted.remove(ident); withheld[ident] = f"depends on unaccepted {dep}@{rev}"
                            changed = True; break
            if not accepted:
                return {"status": "nothing_publishable", "published_refs": [], "withheld": withheld}
            for ident in accepted:
                current = manifest["entries"].get(ident, {}).get("revision")
                if current != proposal["base_revisions"][ident]:
                    raise ContractError(f"Concurrent modification: {ident}; rebase and review the changed candidate")
                r = records[ident]; validate_record(r, require_revision=True)
                for dep, rev in dependencies(r):
                    if dep not in accepted and not self._revision_exists(dep, rev, manifest):
                        raise ContractError(f"Dependency disappeared: {dep}@{rev}")
            refs = []
            for ident in sorted(accepted):
                r = records[ident]; rel = self._object_path(r); path = self._state_inside(rel)
                if path.exists() and read_json(path) != r:
                    raise ContractError("Immutable object collision")
                if not path.exists():
                    atomic_json(path, r)
                ref = self.ref(r); refs.append(ref)
                manifest["entries"][ident] = {**ref, "path": rel, "reviewer_run_id": review["reviewer_run_id"],
                    "use_restrictions": r["evidence"]["use_restrictions"],
                    "review_backend": review["backend"], "review_digest": digest(review),
                    "review_scope": next(i for i in review["items"] if i["id"] == ident)}
            receipt = {"status": "published", "proposal_digest": proposal["digest"],
                       "review_digest": digest(review), "published_at": now(), "published_refs": refs,
                       "withheld": withheld, "scientific_certification": "none; record fidelity review only unless explicitly scoped"}
            manifest["receipts"][proposal["digest"]] = receipt
            manifest["sequence"] += 1
            # Retain the actual review, not only a caller-supplied filename or its digest.
            atomic_json(self.state_root / "staging" / proposal["proposal_id"] / "review.json", review)
            # The visible file is the current scientific object, regardless of review status.
            remaining_leads = [r for r in self.lead_records() if r["id"] not in accepted]
            current_backups = {self.current_path(records[i]["id"], records[i]["kind"]):
                               (self.current_path(records[i]["id"], records[i]["kind"]).read_bytes()
                                if self.current_path(records[i]["id"], records[i]["kind"]).exists() else None)
                               for i in accepted}
            pointers = {self.state_root / name: ((self.state_root / name).read_bytes()
                         if (self.state_root / name).exists() else None) for name in ("CURRENT.json", "LEADS.json")}
            try:
                for ident in accepted:
                    r = records[ident]
                    atomic_json(self.current_path(ident, r["kind"]), r)
                self._save_lead_catalog(remaining_leads)
                self._commit_generation(manifest)
            except BaseException:
                _restore_files({**current_backups, **pointers})
                raise
            # The manifest already holds the receipt if the following write is interrupted.
            atomic_json(self.state_root / "staging" / proposal["proposal_id"] / "receipt.json", receipt)
            return receipt


# Existing operator tools use this alias; the read-only core never imports this module.
Store = WriterStore
