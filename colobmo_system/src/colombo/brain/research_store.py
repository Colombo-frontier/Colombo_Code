"""Transactional Task/Wave documents with fixed reference indexes."""
from __future__ import annotations
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import copy
import math
import os
import re
import sqlite3
import time
import uuid

from colombo.shared.file_io import Path, io_path, atomic_write, file_lock, json_bytes, json_equal


REVIEW_RECORD_BYTE_BUDGET = 24_000
NOTE_PREVIEW_CHARS = 240


def note_preview(text):
    """A display excerpt only; the free-form note remains unchanged in storage."""
    text = " ".join(text.split())
    return {"summary": text[:NOTE_PREVIEW_CHARS],
            "summary_truncated": len(text) > NOTE_PREVIEW_CHARS}


class StoreError(ValueError):
    pass


class RunBusy(StoreError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def linked(path):
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


class Store:
    def __init__(self, root):
        raw = Path(root).absolute()
        if linked(raw) or not raw.is_dir():
            raise StoreError("Run root must be an existing ordinary directory")
        self.root = raw.resolve()
        self.db_path = self.safe_path("state.sqlite")
        existing = self.db_path.exists()
        with self._connect() as db:
            if existing:
                tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                version = db.execute("SELECT value FROM meta WHERE key='storage_version'").fetchone() if "meta" in tables else None
                storage_version = json.loads(version[0]) if version else None
                if type(storage_version) is not int or storage_version not in (3, 4):
                    raise StoreError("Unsupported storage format; start a new storage_version=3 run")
            db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
              CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS documents(name TEXT PRIMARY KEY,payload TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS refs(id TEXT PRIMARY KEY,document TEXT NOT NULL,
                pointer TEXT NOT NULL,revision INTEGER NOT NULL,node_type TEXT NOT NULL,created_at TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS record_requests(id TEXT PRIMARY KEY,kind TEXT NOT NULL,
                ref_id TEXT NOT NULL,input_keys TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS events(sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,payload TEXT NOT NULL,created_at TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY,payload TEXT NOT NULL,
                state TEXT NOT NULL,result TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
            """)
            db.execute("INSERT OR IGNORE INTO meta VALUES('storage_version','3')")
            db.execute("INSERT OR IGNORE INTO meta VALUES('generation','0')")
            from colombo.brain.research_records import initial_documents
            for name, body in initial_documents().items():
                db.execute("INSERT OR IGNORE INTO documents VALUES(?,?)", (name, json_bytes(body).decode()))

    @classmethod
    def create(cls, root, goal, criteria, config, materials=None):
        root = Path(root).absolute()
        if not isinstance(goal, str) or not goal.strip():
            raise StoreError("Goal must be nonempty")
        if not isinstance(criteria, list) or any(not isinstance(x, str) or not x.strip() for x in criteria):
            raise StoreError("Criteria must contain nonempty strings")
        if not isinstance(config, dict):
            raise StoreError("Config must be an object")
        from colombo.configuration import require_current_workflow
        require_current_workflow(config)
        config = {**config, "storage_version": 4}
        json_bytes(config)
        if linked(root) or (root.exists() and any(root.iterdir())):
            raise StoreError("New run requires a new or empty directory")
        sources = []
        for source in materials or []:
            source = Path(source).absolute()
            if linked(source) or not source.is_file():
                raise StoreError(f"Input material is not an ordinary file: {source}")
            sources.append((source, source.read_bytes()))
        root.mkdir(parents=True, exist_ok=True)
        store = cls(root)
        store.set_meta(storage_version=config["storage_version"], config=config)
        atomic_write(store.safe_path("input/goal.md"), goal.encode("utf-8"))
        atomic_write(store.safe_path("config.snapshot.json"), json_bytes(config))
        refs = []
        for index, (source, data) in enumerate(sources, 1):
            name = re.sub(r"[^\w.\-]", "_", source.name)[:120] or "material"
            relative = f"input/materials/{index:04d}-{name}"
            atomic_write(store.safe_path(relative), data)
            refs.append(store.write_record("material", {"source": str(source), "name": source.name,
                "summary": f"Input material: {source.name}", "artifacts": [
                {"path": relative, "size": len(data), "name": source.name}]},
                request_id=f"initial-material-{index}"))
        targets = [{"id": "G0", "text": goal}] + [
            {"id": f"G{i}", "text": text} for i, text in enumerate(criteria, 1)]
        goal_ref = store.write_record("goal", {"goal": goal, "criteria": criteria,
            "targets": targets, "material_refs": refs, "artifacts": [{"path": "input/goal.md",
            "size": len(goal.encode("utf-8")), "name": "goal.md"}]},
            request_id="initial-goal")
        store.set_meta(goal_ref=goal_ref, config=config, round_no=0, phase="planning", status="ready",
                       progress_ref=None, material_refs=refs, created_at=now())
        store.set_meta(research_mode_request="oracle_complexity", research_routing={
            "research_mode": "oracle_complexity", "reason": "Explicit Programme mode selected at initialization.", "source": "explicit"})
        store.event("run_created", goal_ref=goal_ref)
        try:
            store.export_documents()
        except OSError as exc:
            store.event("research_export_failed", error=str(exc))
        return store

    def safe_path(self, relative, *, exists=False):
        relative = Path(relative)
        if relative.is_absolute() or relative.drive or ".." in relative.parts:
            raise StoreError("Path must remain relative to this run")
        current = self.root
        for part in relative.parts:
            current /= part
            if linked(current):
                raise StoreError("Symlink/junction paths are not permitted")
        path = current.resolve()
        if not path.is_relative_to(self.root):
            raise StoreError("Path escapes run")
        if exists and not path.is_file():
            raise StoreError(f"Missing artifact: {relative}")
        return path

    @contextmanager
    def _connect(self):
        self.safe_path("state.sqlite")
        db = sqlite3.connect(io_path(self.db_path), timeout=30)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA synchronous=FULL")
        try:
            with db:
                yield db
        finally:
            db.close()

    @contextmanager
    def writer_snapshot(self):
        """Hold one immediate transaction for document and control-state writes."""
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            documents, stored = self._documents(db), self._meta(db)
            yield db, documents, self._expand_meta(stored, documents)

    @staticmethod
    def _documents(db):
        return {r["name"]: json.loads(r["payload"]) for r in db.execute("SELECT * FROM documents")}

    @staticmethod
    def _meta(db):
        return {r["key"]: json.loads(r["value"]) for r in db.execute("SELECT * FROM meta")}

    def _flush_documents(self, db, documents):
        db.executemany("UPDATE documents SET payload=? WHERE name=?",
            [(json_bytes(value).decode(), name) for name, value in documents.items()])
        db.execute("UPDATE meta SET value=CAST(CAST(value AS INTEGER)+1 AS TEXT) WHERE key='generation'")

    def read_document(self, name):
        with self._connect() as db:
            row = db.execute("SELECT payload FROM documents WHERE name=?", (name,)).fetchone()
            if row is None:
                raise StoreError("Unknown domain document")
            return json.loads(row[0])

    domain_document = read_document

    def snapshot(self):
        with self._connect() as db:
            db.execute("BEGIN")
            documents = self._documents(db)
            meta = self._meta(db)
            refs = {r["id"]: dict(r) for r in db.execute("SELECT * FROM refs")}
        return documents, self._expand_meta(meta, documents), refs

    def _expand_meta(self, meta, documents):
        from colombo.brain.research_records import wave_history
        result = copy.deepcopy(meta)
        result["wave_history"] = wave_history(documents["research"])
        data = result.get("round_data")
        if data:
            for job in data.get("jobs", []):
                task = documents["research"]["tasks"].get(job["task_id"])
                if task and task.get("definition"):
                    job["spec"] = {**copy.deepcopy(task["definition"]),
                        "package": copy.deepcopy(task["inputs"]["selection"]),
                        "mode": "restart" if job.get("restart") else "resume" if job.get("resume") else "new",
                        "resume_task_id": job["task_id"] if job.get("resume") else None}
        admissions = result.get("admitted_results", {})
        for rid, current in admissions.items():
            if current.get("record_ref") and "verdict" not in current:
                row = self._row_from_documents(current["record_ref"])
                pointer = self._read_row(row, documents)
                assessment_row = self._row_from_documents(pointer["assessment_ref"])
                assessment = self._read_row(assessment_row, documents)
                index = pointer.get("admission_index")
                entries = assessment.get("update", {}).get("admissions", [])
                if type(index) is int and 0 <= index < len(entries):
                    admissions[rid] = {**entries[index], **current}
        return result

    def _row_from_documents(self, ref):
        with self._connect() as db:
            return dict(self._row(db, ref))

    def get_meta(self, key, default=None):
        with self._connect() as db:
            meta = self._meta(db)
            if key in {"wave_history", "round_data", "admitted_results"}:
                return self._expand_meta(meta, self._documents(db)).get(key, default)
            return meta.get(key, default)

    def set_meta(self, **values):
        self.update_meta_atomic(lambda meta: values)

    def update_meta_atomic(self, updater, *, with_documents=False):
        """Update control state against one locked database snapshot.

        Freshness guards can request the domain documents from this same writer
        transaction instead of opening a separate, potentially stale read.
        """
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            documents = self._documents(db)
            stored = self._meta(db)
            state = self._expand_meta(stored, documents)
            changes = updater(state, documents) if with_documents else updater(state)
            if changes is None:
                return False
            from colombo.brain.research_records import apply_control
            apply_control(documents, state, changes)
            changes = copy.deepcopy(changes)
            changes.pop("wave_history", None)
            if changes.get("round_data"):
                for job in changes["round_data"].get("jobs", []):
                    job.pop("spec", None)
            if changes.get("admitted_results"):
                for rid, admission in changes["admitted_results"].items():
                    if admission.get("record_ref"):
                        changes["admitted_results"][rid] = {k: admission[k] for k in ("record_ref", "review_ref") if k in admission}
            db.executemany("INSERT INTO meta VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                [(key, json_bytes(value).decode()) for key, value in changes.items()])
            if documents != self._documents(db):
                self._flush_documents(db, documents)
            return True

    def enqueue_result(self, task_id, attempt_id, result_ref):
        identifier = task_id + ":" + attempt_id
        def update(meta):
            queue = meta.get("result_events", [])
            previous = next((e for e in queue if e["id"] == identifier), None)
            if previous:
                if previous["result_ref"] != result_ref:
                    raise StoreError("One attempt produced different result events")
                return {}
            return {"result_events": [*queue, {"id": identifier, "task_id": task_id,
                "attempt_id": attempt_id, "result_ref": result_ref, "state": "queued"}]}
        self.update_meta_atomic(update)

    @staticmethod
    def _ref(row):
        return {"id": row["id"], "revision": row["revision"]}

    def write_record(self, kind, payload, request_id=None):
        from colombo.configuration import require_current_workflow
        require_current_workflow(self.get_meta("config"))
        if not isinstance(kind, str) or not re.fullmatch(r"[a-z][a-z0-9_\-]{0,63}", kind):
            raise StoreError("Invalid record kind")
        if not isinstance(payload, dict):
            raise StoreError("Record must be a JSON object")
        if request_id is not None and (not isinstance(request_id, str) or not request_id):
            raise StoreError("Invalid request_id")
        json_bytes(payload)  # Reject non-JSON values before acquiring the writer lock.
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            previous = db.execute("SELECT * FROM record_requests WHERE id=?", (request_id,)).fetchone() if request_id else None
            if previous:
                row = self._row(db, previous["ref_id"])
                from colombo.brain.research_records import read_node
                original = read_node(self, row, self._documents(db), replay=True)
                keys = json.loads(previous["input_keys"])
                if kind in {"task_relation", "prune_decision"} and "prune_index" not in keys:
                    original = self._read_row(row, self._documents(db))
                original = {key: original[key] for key in keys if key in original}
                if previous["kind"] != kind or not json_equal(original, payload):
                    raise StoreError("Idempotency key reused for different content")
                return self._ref(row)
            from colombo.brain.research_records import insert
            documents = self._documents(db)
            ref = insert(self, db, documents, kind, payload, self._meta(db))
            if request_id:
                db.execute("INSERT INTO record_requests VALUES(?,?,?,?)",
                           (request_id, kind, ref["id"], json.dumps(list(payload))))
            self._flush_documents(db, documents)
            return ref

    def _row(self, db, ref):
        identifier = ref.get("id") if isinstance(ref, dict) else ref
        if not isinstance(identifier, str):
            raise StoreError("Record reference needs id")
        row = db.execute("SELECT * FROM refs WHERE id=?", (identifier,)).fetchone()
        if row is None:
            raise StoreError(f"Unknown record: {identifier}")
        if isinstance(ref, dict):
            if set(ref) - {"id", "revision", "summary", "created_at"}:
                raise StoreError("Reference contains unsupported metadata")
            if "revision" in ref and (type(ref["revision"]) is not int or ref["revision"] != row["revision"]):
                raise StoreError("Record reference version mismatch")
        return row

    def write_lookup_material(self, call_id, payload):
        """Register a source only while its owning Brain call is still active."""
        json_bytes(payload)
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            meta = self._meta(db)
            pending = meta.get("pending_call") or {}
            if (pending.get("call_id") != call_id or pending.get("role") != "brain"
                    or pending.get("stage") not in {"plan", "process_results"}):
                raise StoreError("This Brain call is no longer active")
            from colombo.brain.research_records import insert
            documents = self._documents(db)
            ref = insert(self, db, documents, "material", payload, meta)
            self._flush_documents(db, documents)
            return ref

    def _read_row(self, row, documents=None, *, expand=True):
        from colombo.brain.research_records import read_node
        if documents is None:
            with self._connect() as db:
                documents = self._documents(db)
        return read_node(self, row, documents, expand=expand)

    def read_record(self, ref):
        with self._connect() as db:
            db.execute("BEGIN")
            return self._read_row(self._row(db, ref), self._documents(db))

    def public_read(self, ref):
        with self._connect() as db:
            db.execute("BEGIN")
            return self._read_row(self._row(db, ref), self._documents(db), expand=False)

    def review_package_view(self, ref, offset=0, limit=20):
        """Project each required fixed body once from the package's DB snapshot."""
        if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 50:
            raise StoreError("offset must be nonnegative and limit must be an integer from 1 to 50")
        with self._connect() as db:
            db.execute("BEGIN")
            package_row = self._row(db, ref)
            if package_row["node_type"] != "review_package":
                raise StoreError("Expected a fixed review package")
            documents = self._documents(db)
            package = self._read_row(package_row, documents, expand=False)
            required, allowed = package.get("required_checked_refs"), package.get("allowed_refs")
            if (not isinstance(required, list) or not isinstance(allowed, list)
                    or any(not isinstance(rid, str) for rid in required + allowed)
                    or len(required) != len(set(required)) or not set(required).issubset(allowed)):
                raise StoreError("Required review references must be distinct and inside the allowed package")
            versions = {}
            references = package.get("references", [])
            if not isinstance(references, list):
                raise StoreError("Review package references must be a list")
            for entry in references:
                row = self._row(db, entry)  # Also checks any explicitly frozen revision.
                if row["id"] not in allowed:
                    raise StoreError("Review reference is outside the frozen allowed package")
                versions[row["id"]] = row
            records, record_bytes = [], 0
            for rid in required[offset:offset + limit]:
                row = versions.get(rid)
                if row is None:
                    row = self._row(db, rid)  # IDs identify immutable versions, never 'latest'.
                item = {"ref": self._ref(row), "payload": self._read_row(row, documents, expand=False)}
                size = len(json_bytes(item))
                if records and record_bytes + size > REVIEW_RECORD_BYTE_BUDGET:
                    break
                records.append(item)
                record_bytes += size
                if record_bytes > REVIEW_RECORD_BYTE_BUDGET:
                    break  # One oversized node is returned whole, never truncated.
            total = len(required)
            following = offset + len(records)
            next_offset = following if following < total else None
            return {**package, "required_records": records, "offset": offset, "limit": limit,
                    "total": total, "next_offset": next_offset,
                    "record_bytes": record_bytes, "record_byte_budget": REVIEW_RECORD_BYTE_BUDGET,
                    "oversized_record": records[0]["ref"] if record_bytes > REVIEW_RECORD_BYTE_BUDGET else None,
                    "next": {"offset": next_offset, "limit": limit} if next_offset is not None else None}

    def record_ref(self, ref):
        with self._connect() as db:
            return self._ref(self._row(db, ref))

    def record_kind(self, ref):
        with self._connect() as db:
            return self._row(db, ref)["node_type"]

    def request_record(self, request_id):
        with self._connect() as db:
            row = db.execute("SELECT ref_id FROM record_requests WHERE id=?", (request_id,)).fetchone()
            return self._ref(self._row(db, row[0])) if row else None

    def assessment_proof(self, ref):
        return self.public_read(ref)["update"].get("proof_ref")

    def submission_input(self, ref):
        """Reconstruct the exact input form, including a proof's source selector."""
        from colombo.brain.research_records import read_node
        with self._connect() as db:
            db.execute("BEGIN")
            return read_node(self, self._row(db, ref), self._documents(db), replay=True)

    def plan_identity(self, ref):
        with self._connect() as db:
            row = self._row(db, ref)
            if row["node_type"] != "plan":
                raise StoreError("Expected a plan")
            docs = self._documents(db)
            from colombo.brain.research_records import at
            wave = at(docs, row["document"], row["pointer"])
            specs = self._read_row(row, docs)["tasks"]
            return {"round_no": wave["round_no"], "jobs": [
                {**member, "spec": spec} for member, spec in zip(wave["members"], specs)]}

    def plan_jobs(self, ref):
        return self.plan_identity(ref)["jobs"]

    def retrieve(self, kind=None, limit=20, offset=0):
        if type(limit) is not int or not 1 <= limit <= 200 or type(offset) is not int or offset < 0:
            raise StoreError("Invalid pagination")
        with self._connect() as db:
            db.execute("BEGIN")
            docs = self._documents(db)
            sql = "SELECT * FROM refs" + (" WHERE node_type=?" if kind else "") + " ORDER BY created_at DESC,id DESC LIMIT ? OFFSET ?"
            rows = db.execute(sql, ([kind] if kind else []) + [limit, offset]).fetchall()
            result = []
            for row in rows:
                payload = self._read_row(row, docs)
                summary = payload.get("summary") or payload.get("title") or payload.get("goal") or payload.get("reason") or ""
                preview = ({"summary": note_preview(payload["text"])["summary"]}
                           if row["node_type"] == "note" and isinstance(payload.get("text"), str)
                           else {"summary": str(summary)[:600]})
                result.append({**self._ref(row), **preview, "created_at": row["created_at"]})
            return result

    def note_directory(self, status=None):
        """Read current note versions as excerpts from one database snapshot.

        Superseded versions remain readable by their fixed references. Filtering
        happens after finding current versions, so resolving a note cannot bring
        its earlier open version back into the Brain context.
        """
        from colombo.brain.research_records import identity
        with self._connect() as db:
            db.execute("BEGIN")
            notes = json.loads(db.execute(
                "SELECT payload FROM documents WHERE name='working_notes'"
            ).fetchone()[0])["entries"]
            superseded = {identity(note["supersedes"]) for note in notes.values()
                          if note.get("supersedes")}
            rows = db.execute("SELECT * FROM refs WHERE node_type='note' ORDER BY created_at DESC,id DESC")
            result = []
            for row in rows:
                note = notes[row["id"]]
                if row["id"] in superseded or (status is not None and note.get("status", "open") != status):
                    continue
                result.append({**self._ref(row), **note_preview(note["text"]),
                    "related_refs": note.get("related_refs", []),
                    "status": note.get("status", "open"), "supersedes": note.get("supersedes"),
                    "created_at": row["created_at"]})
            return result

    def reference_count(self, kind=None):
        with self._connect() as db:
            return db.execute("SELECT COUNT(*) FROM refs" + (" WHERE node_type=?" if kind else ""),
                              (kind,) if kind else ()).fetchone()[0]

    def export_documents(self):
        # Serialize exporters, including status readers, so older snapshots cannot
        # overwrite a newer generation after a slow file replacement.
        with file_lock(self.safe_path(".export.lock")):
            documents, meta, _ = self.snapshot()
            for name, body in documents.items():
                atomic_write(self.safe_path(name + ".json"), json_bytes({"storage_version": self.get_meta("storage_version", 3),
                    "generation": meta.get("generation", 0), **body}))
        return documents

    def artifact_entries(self, ref):
        payload = self.read_record(ref)
        items = payload.get("artifacts", [])
        if not items and isinstance(payload.get("artifact"), dict):
            items = [payload["artifact"]]
        if not isinstance(items, list):
            raise StoreError("Artifact list must be a list")
        checked = []
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                raise StoreError("Artifact needs a relative path")
            self.safe_path(item["path"])
            checked.append(dict(item))
        return checked

    def read_artifact(self, record_ref, relative_path=None, offset=0, limit=12000):
        if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 100000:
            raise StoreError("Invalid read range")
        items = self.artifact_entries(record_ref)
        if relative_path is None:
            if len(items) != 1:
                raise StoreError("Select an artifact path listed in the record")
            item = items[0]
        else:
            item = next((item for item in items if item["path"] == relative_path), None)
            if item is None:
                raise StoreError("Artifact is not authorized by this record")
        data = self.safe_path(item["path"], exists=True).read_bytes()
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise StoreError("Artifact is not UTF-8 text; use the verified file reference") from exc
        return {"text": text[offset:offset+limit], "path": item["path"],
                "total_chars": len(text), "offset": offset, "truncated": offset+limit < len(text)}

    def event(self, name, **details):
        with self._connect() as db:
            cursor = db.execute("INSERT INTO events(name,payload,created_at) VALUES(?,?,?)", (name,json_bytes(details).decode(),now()))
            return cursor.lastrowid

    def events(self, after=0, limit=100):
        if type(after) is not int or after < 0 or type(limit) is not int or not 1 <= limit <= 1000:
            raise StoreError("Invalid event pagination")
        with self._connect() as db:
            return [{**dict(row),"payload":json.loads(row["payload"])} for row in db.execute(
                "SELECT * FROM events WHERE sequence>? ORDER BY sequence LIMIT ?", (after,limit))]

    def save_task(self, task):
        identifier = task.get("task_id", task.get("id"))
        if not isinstance(identifier, str) or not re.fullmatch(r"[A-Za-z0-9_.\-]{1,120}", identifier):
            raise StoreError("Task needs safe task_id")
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            docs = self._documents(db)
            from colombo.brain.research_records import task_node
            node = task_node(docs["research"], identifier)
            old = node["runtime"]
            for key in ("assignment_ref", "package_ref"):
                if key in old and task.get(key) != old[key]:
                    raise StoreError(f"Cannot change task identity: {key}")
                if node.get(key) and task.get(key) != node[key]:
                    raise StoreError(f"Cannot change fixed task identity: {key}")
            node["runtime"] = copy.deepcopy(task)
            attempt = task.get("active_attempt")
            if attempt:
                execution = node["attempts"].setdefault(attempt, {"attempt_id": attempt})
                execution["state"] = task.get("state")
            self._flush_documents(db, docs)

    def get_task(self, task_id):
        task = self.read_document("research")["tasks"].get(task_id)
        if task is None or not task["runtime"].get("state") and not task["runtime"].get("status"):
            return None
        return task["runtime"]

    def list_tasks(self):
        return [node["runtime"] for _, node in sorted(self.read_document("research")["tasks"].items())
                if node["runtime"].get("state") or node["runtime"].get("status")]

    def get_request(self, request_id):
        with self._connect() as db:
            row = db.execute("SELECT * FROM requests WHERE id=?",(request_id,)).fetchone()
            if row is None:
                return None
            return {**dict(row), "payload":json.loads(row["payload"]),
                    "result":json.loads(row["result"]) if row["result"] is not None else None}

    def unresolved_audits(self, call_id=None):
        """Reserved audits must be reconciled, never bypassed with a new call ID."""
        with self._connect() as db:
            rows = []
            for row in db.execute("SELECT * FROM requests WHERE id LIKE 'audit:%' AND state IN ('pending','unknown') ORDER BY created_at,id"):
                payload = json.loads(row["payload"])
                if call_id is None or payload.get("call_id") == call_id:
                    rows.append({**dict(row), "payload": payload,
                                 "result": json.loads(row["result"]) if row["result"] else None})
            return rows

    def reserve_audit(self, call_id, request_id, payload, *, execution_budget=None):
        """Atomically find a prior request or reserve one process and its budget."""
        from colombo.configuration import require_current_workflow
        require_current_workflow(self.get_meta("config"))
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            meta = {row[0]: json.loads(row[1]) for row in db.execute("SELECT key,value FROM meta")}
            active = meta.get("pending_call") or {}
            if active.get("call_id") != call_id or active.get("role") != "brain":
                raise StoreError("Audit requires an active Brain call")
            requests = list(db.execute("SELECT * FROM requests WHERE id LIKE 'audit:%'"))
            for row in requests:
                old = json.loads(row["payload"])
                if old.get("call_id") != call_id or old.get("request_id") != request_id:
                    continue
                same = json_equal(old.get("input"), payload)
                if request_id is None and not same:
                    continue
                if not same:
                    raise StoreError("Audit request ID reused with different input")
                return {**dict(row), "payload": old,
                        "result": json.loads(row["result"]) if row["result"] else None}, False
            if any(row["state"] in {"pending", "unknown"} for row in requests):
                raise StoreError("An earlier audit has unresolved execution; reconcile it before starting another audit")
            if execution_budget is not None:
                if (not isinstance(execution_budget, dict)
                        or set(execution_budget) != {"deadline_unix", "submission_reserve_seconds"}
                        or any(type(value) not in (int, float) or not math.isfinite(value) for value in execution_budget.values())
                        or execution_budget["submission_reserve_seconds"] < 0):
                    raise StoreError("Invalid parent audit execution budget")
                audit_timeout = meta["config"]["audit"]["timeout_seconds"]
                # Keep five seconds for launch/receipt persistence. The larger
                # submission reserve in context is advice, not an extra limit.
                margin = meta["config"].get("runtime", {}).get("audit_start_margin_seconds", 5)
                required = margin if audit_timeout == "unlimited" else audit_timeout + margin
                if time.time() + required > execution_budget["deadline_unix"]:
                    raise StoreError("New audit cannot fit within the parent deadline plus 5-second launch/receipt margin; submit without starting it")
            count = meta.get("model_call_count", 0)
            audit_id = "AUD" + uuid.uuid4().hex
            request = {"call_id": call_id, "request_id": request_id, "audit_id": audit_id, "input": payload}
            key, stamp = "audit:" + audit_id, now()
            db.execute("INSERT INTO requests VALUES(?,?,?,?,?,?)",
                       (key, json_bytes(request).decode(), "pending", None, stamp, stamp))
            for name, value in (("model_call_count", count + 1), ("audit_call_count", meta.get("audit_call_count", 0) + 1)):
                db.execute("INSERT INTO meta VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                           (name, json_bytes(value).decode()))
            return {"id": key, "payload": request, "state": "pending", "result": None}, True

    def save_request(self, request_id, payload, state, result=None):
        if not isinstance(request_id,str) or not request_id or state not in {"pending","unknown","confirmed","not_executed"}:
            raise StoreError("Invalid request id/state")
        encoded = json_bytes(payload).decode()
        encoded_result = json_bytes(result).decode() if result is not None else None
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute("SELECT * FROM requests WHERE id=?",(request_id,)).fetchone()
            if old:
                if old["payload"] != encoded:
                    raise StoreError("Request id reused with different payload")
                if old["state"] == "confirmed" and (state != "confirmed" or old["result"] != encoded_result):
                    raise StoreError("Confirmed request cannot be rewritten")
                if old["state"] == "unknown" and state == "pending":
                    raise StoreError("Unknown request requires reconciliation")
                db.execute("UPDATE requests SET state=?,result=?,updated_at=? WHERE id=?",(state,encoded_result,now(),request_id))
            else:
                stamp = now()
                db.execute("INSERT INTO requests VALUES(?,?,?,?,?,?)",(request_id,encoded,state,encoded_result,stamp,stamp))

    @contextmanager
    def exclusive(self):
        lock = file_lock(self.safe_path(".controller.lock"),timeout=0)
        try:
            lock.__enter__()
        except TimeoutError as exc:
            raise RunBusy("Another controller owns this run") from exc
        try:
            yield self
        finally:
            lock.__exit__(None,None,None)
