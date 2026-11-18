"""SQLite state and content-addressed scientific records; raw responses are not valid handoff caches."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

from .contracts import ProtocolError, references, resolve_pointer, validate


def dumps(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: object) -> str:
    return hashlib.sha256(dumps(value).encode("utf-8")).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    with temp.open("w", encoding="utf-8") as f:
        f.write(dumps(value)); f.flush(); os.fsync(f.fileno())
    os.replace(temp, path)


class Workspace:
    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self.db = sqlite3.connect(self.root / "state.sqlite3", timeout=30, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS artifacts(ref TEXT PRIMARY KEY,kind TEXT,producer TEXT,deps TEXT,created REAL);
        CREATE TABLE IF NOT EXISTS ownership(ref TEXT,job TEXT,PRIMARY KEY(ref,job));
        CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY,role TEXT,inputs TEXT,status TEXT,state TEXT,output TEXT,created REAL,updated REAL);
        CREATE TABLE IF NOT EXISTS calls(id TEXT PRIMARY KEY,job TEXT,request_hash TEXT,status TEXT,request TEXT,response TEXT,diagnostic TEXT,created REAL);
        CREATE TABLE IF NOT EXISTS tool_calls(id TEXT PRIMARY KEY,job TEXT,name TEXT,args TEXT,result TEXT,status TEXT);
        CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY AUTOINCREMENT,job TEXT,event TEXT,payload TEXT,created REAL);
        CREATE TABLE IF NOT EXISTS drafts(id TEXT PRIMARY KEY,job TEXT,kind TEXT,revision INTEGER,data TEXT);
        CREATE TABLE IF NOT EXISTS draft_ops(token TEXT PRIMARY KEY,result TEXT);
        CREATE TABLE IF NOT EXISTS draft_origins(draft_id TEXT PRIMARY KEY,job TEXT,source TEXT,created REAL);
        CREATE TABLE IF NOT EXISTS draft_clone_ops(token TEXT PRIMARY KEY,job TEXT,request_hash TEXT,result TEXT);
        CREATE TABLE IF NOT EXISTS draft_deltas(draft_id TEXT,revision INTEGER,job TEXT,token TEXT,patches TEXT,before_digest TEXT,after_digest TEXT,created REAL,PRIMARY KEY(draft_id,revision));
        CREATE TABLE IF NOT EXISTS memory(id TEXT PRIMARY KEY,job TEXT,role TEXT,text TEXT,refs TEXT,shared INTEGER,created REAL);
        CREATE TABLE IF NOT EXISTS cases(id TEXT PRIMARY KEY,paper_ref TEXT,candidate_ref TEXT,state TEXT,record TEXT);
        CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY,record TEXT);
        """)
        self.db.commit()
        self.artifacts = ArtifactStore(self)

    @contextmanager
    def transaction(self):
        with self._lock:
            try:
                self.db.execute("BEGIN IMMEDIATE")
                yield self.db
                self.db.commit()
            except BaseException:
                self.db.rollback()
                raise

    def query(self, sql, args=()):
        with self._lock:
            return [dict(r) for r in self.db.execute(sql, args).fetchall()]

    def event(self, job: str, name: str, payload: object):
        with self.transaction() as db:
            db.execute("INSERT INTO events(job,event,payload,created) VALUES(?,?,?,?)", (job, name, dumps(payload), time.time()))

    def create_job(self, role: str, inputs: dict, *, nonce: str = "") -> str:
        job_id = digest({"role": role, "inputs": inputs, "nonce": nonce})[:24]
        now = time.time()
        with self.transaction() as db:
            db.execute("INSERT OR IGNORE INTO jobs VALUES(?,?,?,?,?,?,?,?)", (job_id, role, dumps(inputs), "queued", "{}", None, now, now))
        return job_id

    def job(self, job_id: str) -> dict:
        rows = self.query("SELECT * FROM jobs WHERE id=?", (job_id,))
        if not rows:
            raise KeyError(job_id)
        row = rows[0]
        for key in ("inputs", "state", "output"):
            row[key] = json.loads(row[key]) if row[key] else None
        return row

    def save_job(self, job_id: str, status: str, state: dict, output=None):
        with self.transaction() as db:
            db.execute("UPDATE jobs SET status=?,state=?,output=?,updated=? WHERE id=?", (status, dumps(state), dumps(output) if output is not None else None, time.time(), job_id))

    def case(self, case_id: str) -> dict:
        rows = self.query("SELECT record FROM cases WHERE id=?", (case_id,))
        if not rows:
            raise KeyError(case_id)
        return json.loads(rows[0]["record"])

    def create_case_once(self, data: dict):
        with self.transaction() as db:
            db.execute("INSERT OR IGNORE INTO cases VALUES(?,?,?,?,?)", (data["case_id"], data["paper_ref"], data["candidate_ref"], data["state"], dumps(data)))

    def save_case(self, data: dict):
        with self.transaction() as db:
            db.execute("INSERT INTO cases VALUES(?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET candidate_ref=excluded.candidate_ref,state=excluded.state,record=excluded.record", (data["case_id"], data["paper_ref"], data["candidate_ref"], data["state"], dumps(data)))

    def save_run(self, run_id: str, record: dict):
        with self.transaction() as db:
            db.execute("INSERT INTO runs VALUES(?,?) ON CONFLICT(id) DO UPDATE SET record=excluded.record", (run_id, dumps(record)))

    def memory_save(self, job: str, role: str, text: str, refs: list[str]) -> str:
        if len(text) > 5000:
            raise ProtocolError("Working memory is limited to 5000 characters; store complete proofs in proof objects")
        for ref in refs:
            self.artifacts.get(ref)
        mid = digest({"job": job, "text": text, "refs": refs})[:24]
        with self.transaction() as db:
            db.execute("INSERT OR IGNORE INTO memory VALUES(?,?,?,?,?,?,?)", (mid, job, role, text, dumps(refs), 0, time.time()))
        return mid

    def memory_search(self, job: str, query: str, limit: int = 8) -> list[dict]:
        # Do not inherit producer conversations; only the host promotes formal result summaries to shared memory after approval.
        rows = self.query("SELECT id,text,refs,shared FROM memory WHERE (job=? OR shared=1) AND text LIKE ? ORDER BY created DESC LIMIT ?", (job, "%" + query + "%", min(max(limit, 1), 20)))
        for row in rows:
            row["refs"] = json.loads(row["refs"])
        return rows

    def promote(self, ref: str, review_ref: str):
        data = self.artifacts.get(ref)
        review = self.artifacts.get(review_ref)
        if review["kind"] != "review" or review["data"]["verdict"] != "approve":
            raise ProtocolError("Only formal knowledge with an approving review may be shared")
        mid = digest({"ref": ref, "review": review_ref})[:24]
        summary=str(data["data"].get("change_summary",data["data"].get("statement","")))[:1800]
        title=""
        if data["data"].get("profile_ref"):
            profile=self.artifacts.get(data["data"]["profile_ref"])["data"]
            title=str(profile.get("title",""))+" "+str(profile.get("primary_domain",""))
        with self.transaction() as db:
            db.execute("INSERT OR IGNORE INTO memory VALUES(?,?,?,?,?,?,?)", (mid, "system", "reviewed", f"Reviewed {data['kind']}: {title}\n{summary}\n{ref}", dumps([ref, review_ref]), 1, time.time()))

    def draft_create(self, job: str, kind: str, data: object, token: str) -> dict:
        draft_id = digest({"job": job, "token": token})[:24]
        with self.transaction() as db:
            db.execute("INSERT OR IGNORE INTO drafts VALUES(?,?,?,?,?)", (draft_id, job, kind, 0, dumps(data)))
            row = dict(db.execute("SELECT * FROM drafts WHERE id=?", (draft_id,)).fetchone())
        return {"draft_id": draft_id, "revision": row["revision"], "kind": row["kind"]}

    def draft_clone_receipt(self, job: str, source: dict, token: str) -> dict | None:
        """Fixed clone requests are recoverable; changing the source or hash under the same token must not silently reuse an old draft."""
        rows = self.query("SELECT * FROM draft_clone_ops WHERE token=?", (token,))
        if not rows:
            return None
        row = rows[0]
        if row["job"] != job or row["request_hash"] != digest({"job": job, "source": source}):
            raise ProtocolError("draft_clone call_id was reused for a different clone source")
        return json.loads(row["result"])

    def draft_clone(self, job: str, data: dict, source: dict, token: str) -> dict:
        """Mechanical copying after host authorization and version checks; the source is unchanged and scientific approval is not inherited."""
        if digest(data) != source.get("source_digest"):
            raise ProtocolError("draft_clone content does not match the fixed payload digest")
        validate("profile", data)
        request_hash = digest({"job": job, "source": source})
        draft_id = digest({"job": job, "clone_token": token})[:24]
        text = dumps(data)
        result = {"draft_id": draft_id, "revision": 0, "kind": "profile", "clone_source": source,
                  "copied_chars": len(text), "copied_bytes": len(text.encode("utf-8"))}
        with self.transaction() as db:
            prior = db.execute("SELECT * FROM draft_clone_ops WHERE token=?", (token,)).fetchone()
            if prior:
                if prior["job"] != job or prior["request_hash"] != request_hash:
                    raise ProtocolError("draft_clone call_id was reused for a different clone source")
                return json.loads(prior["result"])
            db.execute("INSERT INTO drafts VALUES(?,?,?,?,?)", (draft_id, job, "profile", 0, text))
            db.execute("INSERT INTO draft_origins VALUES(?,?,?,?)", (draft_id, job, dumps(source), time.time()))
            db.execute("INSERT INTO draft_clone_ops VALUES(?,?,?,?)", (token, job, request_hash, dumps(result)))
            db.execute("INSERT INTO events(job,event,payload,created) VALUES(?,?,?,?)",
                       (job, "draft_cloned", dumps(result), time.time()))
        return result

    def draft(self, draft_id: str, job: str) -> dict:
        rows = self.query("SELECT * FROM drafts WHERE id=? AND job=?", (draft_id, job))
        if not rows:
            raise ProtocolError("The draft does not exist or access is not authorized")
        r = rows[0]; r["data"] = json.loads(r["data"])
        origins = self.query("SELECT source FROM draft_origins WHERE draft_id=? AND job=?", (draft_id, job))
        if origins:
            r["clone_source"] = json.loads(origins[0]["source"])
        return r

    def draft_patch(self, draft_id: str, job: str, revision: int, patches: list, token: str) -> dict:
        with self.transaction() as db:
            prior = db.execute("SELECT result FROM draft_ops WHERE token=?", (token,)).fetchone()
            if prior:
                return json.loads(prior[0])
            row = db.execute("SELECT * FROM drafts WHERE id=? AND job=?", (draft_id, job)).fetchone()
            if not row or row["revision"] != revision:
                raise ProtocolError("Draft revision conflict; read the current draft first")
            data = json.loads(row["data"])
            before_digest = digest(data)
            for patch in patches:
                data = patch_json(data, patch)
            result = {"draft_id": draft_id, "revision": revision + 1}
            db.execute("UPDATE drafts SET revision=?,data=? WHERE id=?", (revision + 1, dumps(data), draft_id))
            db.execute("INSERT INTO draft_ops VALUES(?,?)", (token, dumps(result)))
            if db.execute("SELECT 1 FROM draft_origins WHERE draft_id=? AND job=?", (draft_id, job)).fetchone():
                # Cloned drafts additionally retain a delta chain; the full source remains in CAS, so deltas do not require the model to resend the baseline.
                db.execute("INSERT INTO draft_deltas VALUES(?,?,?,?,?,?,?,?)",
                           (draft_id, revision + 1, job, token, dumps(patches), before_digest, digest(data), time.time()))
        return result

    def close(self):
        self.db.close()


class ArtifactStore:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.root = workspace.root / "objects"

    def put(self, kind: str, data: object, producer: str, dependencies=()) -> str:
        validate(kind, data)
        deps = sorted(set(dependencies) | references(data))
        for ref in deps:
            self.get(ref)
        envelope = {"kind": kind, "data": data}
        code = digest(envelope); ref = "sha256:" + code
        path = self.root / code[:2] / (code + ".json")
        if not path.exists():
            atomic_json(path, envelope)
        with self.workspace.transaction() as db:
            db.execute("INSERT OR IGNORE INTO artifacts VALUES(?,?,?,?,?)", (ref, kind, producer, dumps(deps), time.time()))
            db.execute("INSERT OR IGNORE INTO ownership VALUES(?,?)", (ref, producer))
        return ref

    def get(self, ref: str) -> dict:
        if not isinstance(ref, str) or not re.fullmatch(r"sha256:[a-f0-9]{64}", ref):
            raise ProtocolError(f"Invalid or unpinned ref: {str(ref)[:100]}")
        code = ref[7:]
        rows = self.workspace.query("SELECT * FROM artifacts WHERE ref=?", (ref,))
        if not rows:
            raise ProtocolError(f"Reference does not exist: {ref}")
        path = self.root / code[:2] / (code + ".json")
        data = json.loads(path.read_text(encoding="utf-8"))
        if digest(data) != code:
            raise ProtocolError(f"Archive hash mismatch: {ref}")
        return {**data, "ref": ref, "producer": rows[0]["producer"], "dependencies": json.loads(rows[0]["deps"])}

    def read(self, ref: str, pointer: str = "", offset: int = 0, limit: int = 12000) -> dict:
        item = self.get(ref)
        return {"ref": ref, "kind": item["kind"], **bounded(resolve_pointer(item["data"], pointer), offset, limit)}

    def owned(self, ref: str, job: str) -> bool:
        return bool(self.workspace.query("SELECT 1 FROM ownership WHERE ref=? AND job=?", (ref, job)))


def bounded(value: object, offset: int = 0, limit: int = 12000) -> dict:
    if not isinstance(offset, int) or offset < 0 or not isinstance(limit, int) or limit < 1:
        raise ProtocolError("offset/limit out of range")
    text = value if isinstance(value, str) else dumps(value)
    limit = min(limit, 24000)
    end = min(len(text), offset + limit)
    result = {"text": text[offset:end], "offset": offset, "next_offset": end if end < len(text) else None, "total_chars": len(text)}
    if offset == 0 and end == len(text) and not isinstance(value, str):
        result["data"] = value
        result.pop("text")  # Do not return JSON and an identical text representation together.
    return result


def patch_json(data: object, patch: dict) -> object:
    if patch.get("op") not in {"add", "replace", "remove", "test"}:
        raise ProtocolError("Supported operations: add/replace/remove/test")
    path = patch.get("path")
    if not isinstance(path, str):
        raise ProtocolError("patch.path must be a JSON Pointer")
    if patch["op"] == "test":
        if resolve_pointer(data, path) != patch.get("value"):
            raise ProtocolError("JSON Patch test failed")
        return data
    if path == "":
        if patch["op"] == "remove":
            raise ProtocolError("The entire draft cannot be removed")
        return copy.deepcopy(patch["value"])
    parent_path, _, key = path.rpartition("/")
    if not path.startswith("/"):
        raise ProtocolError("Invalid patch.path")
    parent = resolve_pointer(data, parent_path)
    if re.search(r"~(?![01])", key):
        raise ProtocolError("Invalid JSON Pointer escape")
    key = key.replace("~1", "/").replace("~0", "~")
    if isinstance(parent, dict):
        if patch["op"] != "add" and key not in parent:
            raise ProtocolError(f"Pointer does not exist: {path}")
        if patch["op"] == "remove":
            del parent[key]
        else:
            parent[key] = copy.deepcopy(patch["value"])
    elif isinstance(parent, list):
        if key == "-" and patch["op"] == "add":
            parent.append(copy.deepcopy(patch["value"]))
        else:
            if not re.fullmatch(r"0|[1-9][0-9]*", key):
                raise ProtocolError("Invalid array Pointer")
            idx = int(key)
            if idx >= len(parent) + (patch["op"] == "add"):
                raise ProtocolError("Array Pointer out of range")
            if patch["op"] == "add": parent.insert(idx, copy.deepcopy(patch["value"]))
            elif patch["op"] == "remove": parent.pop(idx)
            else: parent[idx] = copy.deepcopy(patch["value"])
    else:
        raise ProtocolError("The patch parent is not an object or array")
    return data
