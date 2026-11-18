"""Small durable queue and successful-scope ledger, separate from native Atlas data."""
from __future__ import annotations

from contextlib import contextmanager
from datetime import date, datetime, timezone
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3
import os
import math
import re
import uuid


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".{os.getpid()}.{uuid.uuid4().hex}.tmp")
    try:
        with tmp.open("x", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
        descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    finally:
        tmp.unlink(missing_ok=True)


def now():
    return datetime.now(timezone.utc).isoformat()


class State:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        # Each worker constructs its own State/connection in that worker thread.
        self.db = sqlite3.connect(self.root / "maintenance.sqlite3", timeout=30.0)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA busy_timeout=30000")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript("""
          PRAGMA journal_mode=WAL;
          CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY, plan TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS items(run_id TEXT, position INTEGER, setting_id TEXT,
            status TEXT NOT NULL, attempt INTEGER NOT NULL DEFAULT 0, result TEXT,
            PRIMARY KEY(run_id,position));
          CREATE TABLE IF NOT EXISTS checks(setting_id TEXT PRIMARY KEY, version TEXT,
            semantics TEXT, policy TEXT, cutoff TEXT, scope TEXT, checked_at TEXT);
          CREATE TABLE IF NOT EXISTS workspace_meta(name TEXT PRIMARY KEY, value TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS budget_lineages(
            budget_key TEXT PRIMARY KEY, identity TEXT NOT NULL UNIQUE,
            atlas_root TEXT NOT NULL, sid TEXT NOT NULL, base_version TEXT NOT NULL,
            cutoff TEXT NOT NULL, semantics TEXT NOT NULL, created_at TEXT NOT NULL);
          CREATE INDEX IF NOT EXISTS budget_lineages_sid ON budget_lineages(atlas_root,sid);
          CREATE TABLE IF NOT EXISTS setting_budgets(
            budget_key TEXT PRIMARY KEY REFERENCES budget_lineages(budget_key),
            max_seconds REAL NOT NULL, max_tool_calls INTEGER NOT NULL, max_sessions INTEGER NOT NULL,
            charged_seconds REAL NOT NULL DEFAULT 0, charged_tool_calls INTEGER NOT NULL DEFAULT 0,
            charged_sessions INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS budget_stages(
            reservation_id TEXT PRIMARY KEY, budget_key TEXT NOT NULL REFERENCES setting_budgets(budget_key),
            task_key TEXT NOT NULL, role TEXT NOT NULL, timeout REAL NOT NULL,
            tool_limit INTEGER NOT NULL, session_limit INTEGER NOT NULL,
            status TEXT NOT NULL, created_at TEXT NOT NULL, started_at TEXT, settlement TEXT,
            UNIQUE(budget_key,task_key,role));
          CREATE INDEX IF NOT EXISTS budget_stages_active ON budget_stages(budget_key,status);
          CREATE TABLE IF NOT EXISTS controller_charges(
            budget_key TEXT NOT NULL REFERENCES setting_budgets(budget_key),
            task_key TEXT NOT NULL, observed_seconds REAL NOT NULL,
            charged_seconds REAL NOT NULL, overshoot_seconds REAL NOT NULL, receipt TEXT NOT NULL,
            PRIMARY KEY(budget_key,task_key));
          CREATE TABLE IF NOT EXISTS budget_adjustments(
            reservation_id TEXT PRIMARY KEY REFERENCES budget_stages(reservation_id),
            budget_key TEXT NOT NULL REFERENCES setting_budgets(budget_key),
            old_settlement TEXT NOT NULL, old_settlement_sha256 TEXT NOT NULL,
            evidence TEXT NOT NULL, evidence_sha256 TEXT NOT NULL,
            correction TEXT NOT NULL, created_at TEXT NOT NULL);
          CREATE TRIGGER IF NOT EXISTS budget_adjustments_no_update
            BEFORE UPDATE ON budget_adjustments BEGIN
              SELECT RAISE(ABORT,'Budget adjustments are append-only');
            END;
          CREATE TRIGGER IF NOT EXISTS budget_adjustments_no_delete
            BEFORE DELETE ON budget_adjustments BEGIN
              SELECT RAISE(ABORT,'Budget adjustments are append-only');
            END;
        """)

    @contextmanager
    def _transaction(self):
        if self.db.in_transaction:
            raise RuntimeError("Finish the caller's SQLite transaction before a durable State operation")
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield self.db
        except BaseException:
            self.db.rollback()
            raise
        else:
            self.db.commit()

    @contextmanager
    def lock(self):
        with (self.root / "controller.lock").open("a+") as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise RuntimeError("Another maintenance controller owns this workspace") from exc
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)

    def bind(self, atlas_root):
        path = self.root / "atlas-binding.json"
        value = {"atlas_root": str(Path(atlas_root).resolve())}
        encoded = json.dumps(value, sort_keys=True)
        with self._transaction() as db:
            row = db.execute("SELECT value FROM workspace_meta WHERE name='atlas_root'").fetchone()
            if row is not None and row[0] != encoded or path.exists() and json.loads(path.read_text()) != value or \
                    db.execute("SELECT 1 FROM budget_lineages WHERE atlas_root<>? LIMIT 1", (value["atlas_root"],)).fetchone():
                raise ValueError("Use a separate workspace for each Atlas root")
            if row is None:
                db.execute("INSERT INTO workspace_meta VALUES('atlas_root',?)", (encoded,))
            write_json(path, value)

    def create(self, plan):
        # A new queue is not a new budget cycle. Identity omits implementation,
        # budget and run IDs intentionally; new cutoff/baseline starts a new cycle.
        run_id = digest({**plan, "created_at": now(), "nonce": uuid.uuid4().hex})[:24]
        with self._transaction() as db:
            self._validate_plan_budgets(db, plan)
            db.execute("INSERT INTO runs VALUES(?,?)", (run_id, json.dumps(plan, allow_nan=False)))
            db.executemany("INSERT INTO items(run_id,position,setting_id,status) VALUES(?,?,?,?)",
                           [(run_id, i, sid, "pending") for i, sid in enumerate(plan["setting_ids"])])
        write_json(self.root / "runs" / run_id / "plan.json", plan)
        return run_id

    def plan(self, run_id):
        row = self.db.execute("SELECT plan FROM runs WHERE id=?", (run_id,)).fetchone()
        if row is None:
            raise ValueError("Unknown run ID")
        return json.loads(row[0])

    def items(self, run_id):
        return [dict(r) for r in self.db.execute("SELECT * FROM items WHERE run_id=? ORDER BY position", (run_id,))]

    def save(self, run_id, position, status, result=None, attempt=None):
        with self._transaction():
            self.db.execute("UPDATE items SET status=?,result=?,attempt=COALESCE(?,attempt) WHERE run_id=? AND position=?",
                            (status, json.dumps(result) if result is not None else None, attempt, run_id, position))

    def last(self, sid):
        row = self.db.execute("SELECT * FROM checks WHERE setting_id=?", (sid,)).fetchone()
        return dict(row) if row else None

    def success(self, sid, version, semantics, policy, cutoff, scope):
        with self._transaction():
            last = self.last(sid)
            if last and (last["version"], last["semantics"], last["policy"]) == (version, semantics, policy) and last["cutoff"] > cutoff:
                return
            self.db.execute("INSERT OR REPLACE INTO checks VALUES(?,?,?,?,?,?,?)",
                            (sid, version, semantics, policy, cutoff, json.dumps(scope), now()))

    def due(self, sid, version, semantics, policy, cutoff, days):
        last = self.last(sid)
        return not last or (last["version"], last["semantics"], last["policy"]) != (version, semantics, policy) or \
            (date.fromisoformat(cutoff) - date.fromisoformat(last["cutoff"])).days >= days

    def summary(self, run_id):
        items = self.items(run_id)
        counts = {}
        for row in items:
            counts[row["status"]] = counts.get(row["status"], 0) + 1
        return {"run_id": run_id, "total": len(items), "counts": counts,
                "items": [{"position": r["position"], "setting_id": r["setting_id"], "status": r["status"],
                           "result": json.loads(r["result"]) if r["result"] else None} for r in items]}


    @staticmethod
    def _cycle_identity(identity):
        if not isinstance(identity, dict):
            raise ValueError("Budget lineage needs an audited cycle identity")
        sid = identity.get("sid", identity.get("setting_id"))
        if "sid" in identity and "setting_id" in identity and identity["sid"] != identity["setting_id"]:
            raise ValueError("Budget identity sid and setting_id disagree")
        value = {"atlas_root": identity.get("atlas_root"), "sid": sid,
                 "base_version": identity.get("base_version"), "cutoff": identity.get("cutoff"),
                 "semantics": identity.get("semantics")}
        if any(not isinstance(v, str) or not v for v in value.values()):
            raise ValueError("Budget identity requires atlas_root, sid, base_version, cutoff and semantics")
        value["atlas_root"] = str(Path(value["atlas_root"]).expanduser().resolve())
        date.fromisoformat(value["cutoff"])
        return value

    @staticmethod
    def _finite_number(value, name, *, positive=False):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0 or positive and value <= 0:
            raise ValueError(f"{name} must be a finite {'positive' if positive else 'nonnegative'} number")
        return float(value)

    @staticmethod
    def _integer(value, name, *, positive=False):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0 or positive and value <= 0 or value > 2147483647:
            raise ValueError(f"{name} must be a {'positive' if positive else 'nonnegative'} bounded integer")
        return value

    @classmethod
    def _limits(cls, limits):
        if not isinstance(limits, dict):
            raise ValueError("Cumulative budget limits must be explicit")
        def take(config, short):
            if config in limits and short in limits and limits[config] != limits[short]:
                raise ValueError("Conflicting cumulative budget limit aliases")
            return limits.get(config, limits.get(short))
        return {"seconds": cls._finite_number(take("setting_max_seconds", "seconds"), "setting_max_seconds", positive=True),
                "tool_calls": cls._integer(take("setting_max_tool_calls", "tool_calls"), "setting_max_tool_calls", positive=True),
                "sessions": cls._integer(take("setting_max_sessions", "sessions"), "setting_max_sessions", positive=True)}

    def _lineage(self, db, identity, proposed_key=None):
        identity = self._cycle_identity(identity)
        bound = db.execute("SELECT value FROM workspace_meta WHERE name='atlas_root'").fetchone()
        if bound is not None and json.loads(bound[0])["atlas_root"] != identity["atlas_root"]:
            raise ValueError("Budget lineage must use this workspace's bound Atlas root")
        key = digest(identity)
        if proposed_key is not None and proposed_key != key:
            raise ValueError("A budget cycle key must equal its deterministic audited identity; new plans cannot reset it")
        encoded = json.dumps(identity, sort_keys=True, separators=(",", ":"))
        row = db.execute("SELECT identity FROM budget_lineages WHERE budget_key=?", (key,)).fetchone()
        if row is not None and row[0] != encoded:
            raise ValueError("Persisted budget lineage identity changed")
        if row is None:
            db.execute("INSERT INTO budget_lineages VALUES(?,?,?,?,?,?,?,?)", (key, encoded,
                identity["atlas_root"], identity["sid"], identity["base_version"], identity["cutoff"], identity["semantics"], now()))
        return key

    def budget_lineage(self, identity, proposed_key=None):
        with self._transaction() as db:
            return self._lineage(db, identity, proposed_key)

    def _ensure_budget(self, db, key, limits):
        row = db.execute("SELECT * FROM setting_budgets WHERE budget_key=?", (key,)).fetchone()
        if row is None and limits is None:
            return None
        if db.execute("SELECT 1 FROM budget_lineages WHERE budget_key=?", (key,)).fetchone() is None:
            raise ValueError("Register the exact budget_lineage identity before enabling its cumulative budget")
        requested = self._limits(limits) if limits is not None else None
        if row is None:
            db.execute("INSERT INTO setting_budgets(budget_key,max_seconds,max_tool_calls,max_sessions,created_at) VALUES(?,?,?,?,?)",
                       (key, requested["seconds"], requested["tool_calls"], requested["sessions"], now()))
            row = db.execute("SELECT * FROM setting_budgets WHERE budget_key=?", (key,)).fetchone()
        elif requested is not None and requested != self._row_limits(row):
            raise ValueError("Cumulative caps are immutable within this cycle; changing a plan/config does not reset or extend the ledger")
        return row

    @staticmethod
    def _row_limits(row):
        return {"seconds": row["max_seconds"], "tool_calls": row["max_tool_calls"], "sessions": row["max_sessions"]}

    @staticmethod
    def _reservation(row):
        return {"reservation_id": row["reservation_id"], "id": row["reservation_id"], "budget_key": row["budget_key"],
                "task_key": row["task_key"], "role": row["role"], "timeout": row["timeout"],
                "tool_limit": row["tool_limit"], "session_limit": row["session_limit"], "status": row["status"],
                "paid_started": row["started_at"] is not None, "created_at": row["created_at"], "started_at": row["started_at"]}

    def _snapshot(self, db, key, row):
        if row is None:
            lineage = db.execute("SELECT identity FROM budget_lineages WHERE budget_key=?", (key,)).fetchone()
            return {"enabled": False, "budget_key": key, "identity": json.loads(lineage[0]) if lineage else None,
                    "remaining": None, "outstanding": []}
        lineage = db.execute("SELECT * FROM budget_lineages WHERE budget_key=?", (key,)).fetchone()
        stages = db.execute("SELECT * FROM budget_stages WHERE budget_key=? AND status IN ('reserved','started') ORDER BY created_at", (key,)).fetchall()
        reserved = {"seconds": sum(r["timeout"] for r in stages), "tool_calls": sum(r["tool_limit"] for r in stages), "sessions": sum(r["session_limit"] for r in stages)}
        charged = {"seconds": row["charged_seconds"], "tool_calls": row["charged_tool_calls"], "sessions": row["charged_sessions"]}
        limits = self._row_limits(row)
        remaining = {k: max(0, limits[k] - charged[k] - reserved[k]) for k in limits}
        past = [r[0] for r in db.execute("SELECT budget_key FROM budget_lineages WHERE atlas_root=? AND sid=? AND budget_key<>? ORDER BY created_at,budget_key", (lineage["atlas_root"], lineage["sid"], key))]
        controller = db.execute("SELECT COALESCE(SUM(overshoot_seconds),0) FROM controller_charges WHERE budget_key=?", (key,)).fetchone()[0]
        adjustments = [json.loads(r[0]) for r in db.execute("SELECT correction FROM budget_adjustments WHERE budget_key=? ORDER BY created_at,reservation_id", (key,))]
        credited = {name: sum(a["credited"][name] for a in adjustments) for name in ("seconds", "tool_calls", "sessions")}
        return {"enabled": True, "budget_key": key, "identity": json.loads(lineage["identity"]), "limits": limits,
                "charged": charged, "reserved": reserved, "remaining": remaining,
                "remaining_seconds": remaining["seconds"], "remaining_tool_calls": remaining["tool_calls"],
                "remaining_sessions": remaining["sessions"], "outstanding": [self._reservation(r) for r in stages],
                "blocked_by_outstanding": bool(stages), "exhausted": any(v <= 0 for v in remaining.values()),
                "paid_started_stages": db.execute("SELECT COUNT(*) FROM budget_stages WHERE budget_key=? AND started_at IS NOT NULL", (key,)).fetchone()[0],
                "uncertain_stages": db.execute("SELECT COUNT(*) FROM budget_stages WHERE budget_key=? AND json_extract(settlement,'$.uncertain')=1", (key,)).fetchone()[0],
                "reconciled_not_started_stages": len(adjustments), "credited": credited,
                "controller_overshoot_seconds": controller, "past_cycle_keys": past}

    def budget_snapshot(self, budget_key, limits=None):
        with self._transaction() as db:
            return self._snapshot(db, budget_key, self._ensure_budget(db, budget_key, limits))

    def budget_cycles(self, setting_id, atlas_root=None):
        with self._transaction() as db:
            sql, args = "SELECT budget_key FROM budget_lineages WHERE sid=?", [setting_id]
            if atlas_root is not None:
                sql += " AND atlas_root=?"
                args.append(str(Path(atlas_root).resolve()))
            keys = [r[0] for r in db.execute(sql + " ORDER BY created_at,budget_key", args)]
            return [self._snapshot(db, key, self._ensure_budget(db, key, None)) for key in keys]

    def _validate_plan_budgets(self, db, plan):
        keys, limits = plan.get("budget_keys"), plan.get("budget_limits")
        complete = all(k in plan for k in ("atlas_root", "versions", "cutoff", "semantics"))
        if keys is not None and (not isinstance(keys, dict) or set(keys) != set(plan["setting_ids"])):
            raise ValueError("Every planned setting needs its exact cumulative budget cycle key")
        if keys is not None and not complete or limits is not None and keys is None:
            raise ValueError("Budgeted plans need exact atlas/baseline/cutoff/semantics and budget_keys")
        if not complete:
            return  # Historical minimal queue-only plans retain their old behavior.
        for sid in plan["setting_ids"]:
            identity = self._cycle_identity({"atlas_root": plan["atlas_root"], "sid": sid,
                "base_version": plan["versions"][sid], "cutoff": plan["cutoff"], "semantics": plan["semantics"]})
            key = digest(identity)
            if keys is None:
                if db.execute("SELECT 1 FROM setting_budgets WHERE budget_key=?", (key,)).fetchone():
                    raise ValueError("This exact setting cycle already has a cumulative budget; a new unbudgeted plan cannot reset it")
                continue
            self._lineage(db, identity, keys[sid])
            if self._ensure_budget(db, key, limits) is None:
                raise ValueError("A new cumulative budget cycle needs explicit positive limits")

    def _get_reservation(self, db, reservation):
        token = reservation.get("reservation_id", reservation.get("id")) if isinstance(reservation, dict) else reservation
        row = db.execute("SELECT * FROM budget_stages WHERE reservation_id=?", (token,)).fetchone()
        if row is None:
            raise ValueError("Unknown cumulative budget reservation")
        if isinstance(reservation, dict):
            for key in ("budget_key", "task_key", "role", "timeout", "tool_limit", "session_limit"):
                if key in reservation and reservation[key] != row[key]:
                    raise ValueError("Reservation identity or allocation changed")
        return row

    def reserve_stage(self, key, task_key, role, timeout, tool_limit, session_limit=1, *, limits=None):
        timeout = self._finite_number(timeout, "timeout", positive=True)
        tool_limit = self._integer(tool_limit, "tool_limit", positive=True)
        session_limit = self._integer(session_limit, "session_limit", positive=True)
        if not isinstance(task_key, str) or not task_key or not isinstance(role, str) or role not in {"scout", "reviewer"}:
            raise ValueError("Stage reservations need a stable task key and scout/reviewer role")
        with self._transaction() as db:
            row = self._ensure_budget(db, key, limits)
            if row is None:
                raise ValueError("Cumulative stage reservation requires an enabled budget")
            snapshot = self._snapshot(db, key, row)
            if snapshot["outstanding"]:
                raise CumulativeBudgetError("An outstanding stage reservation is crash-uncertain; reconcile it before any new paid stage", "outstanding_reservation", snapshot)
            if db.execute("SELECT 1 FROM budget_stages WHERE budget_key=? AND task_key=? AND role=?", (key, task_key, role)).fetchone():
                raise CumulativeBudgetError("This stage task already has a reservation; never automatically repeat a paid attempt", "duplicate_stage", snapshot)
            allocation = {"seconds": timeout, "tool_calls": tool_limit, "sessions": session_limit}
            if any(allocation[k] > snapshot["remaining"][k] for k in allocation):
                raise CumulativeBudgetError("The requested stage exceeds the cumulative remaining allocation", "budget_exhausted", snapshot)
            token = uuid.uuid4().hex
            db.execute("INSERT INTO budget_stages VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (token, key, task_key, role, timeout, tool_limit, session_limit, "reserved", now(), None, None))
            return self._reservation(db.execute("SELECT * FROM budget_stages WHERE reservation_id=?", (token,)).fetchone())

    def mark_stage_started(self, reservation):
        with self._transaction() as db:
            row = self._get_reservation(db, reservation)
            if row["status"] != "reserved" or row["started_at"] is not None:
                raise CumulativeBudgetError("A paid stage already started or closed; no automatic repeat is allowed", "duplicate_paid_start")
            db.execute("UPDATE budget_stages SET status='started',started_at=? WHERE reservation_id=?", (now(), row["reservation_id"]))
            return self._reservation(db.execute("SELECT * FROM budget_stages WHERE reservation_id=?", (row["reservation_id"],)).fetchone())

    def settle_stage(self, reservation, elapsed_seconds, tool_calls, uncertain=False, sessions=None):
        elapsed_seconds = self._finite_number(elapsed_seconds, "elapsed_seconds")
        tool_calls = self._integer(tool_calls, "tool_calls")
        if not isinstance(uncertain, bool):
            raise ValueError("uncertain must be a boolean")
        if sessions is not None:
            sessions = self._integer(sessions, "sessions")
        with self._transaction() as db:
            row = self._get_reservation(db, reservation)
            observed_sessions = sessions if sessions is not None else int(row["started_at"] is not None)
            request = {"elapsed_seconds": elapsed_seconds, "tool_calls": tool_calls, "sessions": observed_sessions, "uncertain": uncertain}
            if row["status"] == "settled":
                prior = json.loads(row["settlement"])
                if prior["request"] != request:
                    raise ValueError("An immutable budget settlement cannot be replaced or refunded by a different report")
                return prior
            if row["status"] == "cancelled":
                raise ValueError("A cancelled unstarted reservation cannot later become a paid stage")
            if row["started_at"] is None and not uncertain and (tool_calls or observed_sessions):
                raise ValueError("Observed model/tools require an explicit paid-stage start or an uncertain full charge")
            allocation = {"seconds": row["timeout"], "tool_calls": row["tool_limit"], "sessions": row["session_limit"]}
            observed = {"seconds": elapsed_seconds, "tool_calls": tool_calls, "sessions": observed_sessions}
            # Before paid start, overhead is a controller charge, not a model session.
            charged = dict(allocation) if uncertain else ({k: min(observed[k], allocation[k]) for k in allocation} if row["started_at"] else {"seconds": 0.0, "tool_calls": 0, "sessions": 0})
            receipt = {"reservation_id": row["reservation_id"], "budget_key": row["budget_key"], "task_key": row["task_key"],
                "role": row["role"], "status": "settled", "request": request, "observed": observed, "charged": charged,
                "overshoot": {k: max(0, observed[k] - allocation[k]) for k in allocation}, "uncertain": uncertain,
                "paid_started": row["started_at"] is not None, "settled_at": now()}
            db.execute("UPDATE setting_budgets SET charged_seconds=charged_seconds+?,charged_tool_calls=charged_tool_calls+?,charged_sessions=charged_sessions+? WHERE budget_key=?",
                       (charged["seconds"], charged["tool_calls"], charged["sessions"], row["budget_key"]))
            db.execute("UPDATE budget_stages SET status='settled',settlement=? WHERE reservation_id=?", (json.dumps(receipt, allow_nan=False), row["reservation_id"]))
            return receipt

    def cancel_stage(self, reservation):
        with self._transaction() as db:
            row = self._get_reservation(db, reservation)
            if row["status"] == "cancelled":
                return json.loads(row["settlement"])
            if row["status"] != "reserved" or row["started_at"] is not None:
                raise ValueError("Only an explicitly unstarted reservation can be cancelled without charge")
            receipt = {"reservation_id": row["reservation_id"], "budget_key": row["budget_key"], "status": "cancelled",
                       "charged": {"seconds": 0.0, "tool_calls": 0, "sessions": 0}, "cancelled_at": now()}
            db.execute("UPDATE budget_stages SET status='cancelled',settlement=? WHERE reservation_id=?", (json.dumps(receipt), row["reservation_id"]))
            return receipt

    def reconcile_not_started(self, reservation, observed_seconds, evidence_descriptor):
        """Append one engine-qualified correction; never replace a paid receipt.

        State validates descriptor structure/binding only. Its controller must
        first verify actual stopped native startup and every pinned source file.
        Unknown, incomplete, or possibly paid outcomes are never qualified here.
        """
        observed_seconds = self._finite_number(observed_seconds, "observed_seconds")
        with self._transaction() as db:
            row = self._get_reservation(db, reservation)
            evidence = evidence_descriptor
            if not isinstance(evidence, dict) or evidence.get("kind") != "readonly_verified_native_startup_not_started" or \
                    evidence.get("reservation_id") != row["reservation_id"] or evidence.get("task_key") != row["task_key"] or \
                    evidence.get("role") != row["role"] or not isinstance(evidence.get("stage_path"), str) or not evidence["stage_path"]:
                raise ValueError("Startup reconciliation requires an exact engine-qualified evidence descriptor")
            pins = evidence.get("source_pins")
            required = {"request.json", "stderr.log", "events.jsonl", "metrics.json"}
            if not isinstance(pins, dict) or any(not isinstance(k, str) or not k or not isinstance(v, str) or not re.fullmatch(r"[0-9a-f]{64}", v) for k, v in pins.items()) or \
                    not required.issubset({Path(k).name for k in pins}):
                raise ValueError("Startup reconciliation requires exact request/stderr/events/metrics source pins")
            encoded = json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
            evidence_hash = hashlib.sha256(encoded.encode()).hexdigest()
            prior = db.execute("SELECT * FROM budget_adjustments WHERE reservation_id=?", (row["reservation_id"],)).fetchone()
            if prior is not None:
                correction = json.loads(prior["correction"])
                if prior["old_settlement"] != row["settlement"] or prior["evidence"] != encoded or \
                        correction["observed_seconds"] != observed_seconds:
                    raise ValueError("An append-only startup reconciliation cannot be changed or repeated with different proof")
                return correction
            if row["status"] != "settled" or not isinstance(row["settlement"], str):
                raise ValueError("Only a settled uncertain full reservation can be reconciled")
            old = json.loads(row["settlement"])
            allocation = {"seconds": row["timeout"], "tool_calls": row["tool_limit"], "sessions": row["session_limit"]}
            if old.get("uncertain") is not True or old.get("request", {}).get("uncertain") is not True or old.get("charged") != allocation:
                raise ValueError("Only a settled uncertain full reservation can be reconciled")
            if db.execute("SELECT 1 FROM budget_stages WHERE budget_key=? AND status IN ('reserved','started') LIMIT 1", (row["budget_key"],)).fetchone():
                raise CumulativeBudgetError("An outstanding stage must close before startup reconciliation", "outstanding_reservation")
            retained_seconds = min(observed_seconds, old["charged"]["seconds"])
            credited = {"seconds": old["charged"]["seconds"] - retained_seconds,
                        "tool_calls": old["charged"]["tool_calls"], "sessions": old["charged"]["sessions"]}
            budget = db.execute("SELECT * FROM setting_budgets WHERE budget_key=?", (row["budget_key"],)).fetchone()
            current = {"seconds": budget["charged_seconds"], "tool_calls": budget["charged_tool_calls"], "sessions": budget["charged_sessions"]}
            if any(credited[k] > current[k] for k in credited):
                raise ValueError("Startup correction would make the persistent cumulative debit negative")
            old_hash = hashlib.sha256(row["settlement"].encode()).hexdigest()
            correction = {"kind": "known_native_startup_not_started_budget_correction", "reservation_id": row["reservation_id"],
                "budget_key": row["budget_key"], "task_key": row["task_key"], "role": row["role"],
                "old_settlement_sha256": old_hash, "evidence_sha256": evidence_hash, "observed_seconds": observed_seconds,
                "retained_charge": {"seconds": retained_seconds, "tool_calls": 0, "sessions": 0}, "credited": credited,
                "observed_overshoot_seconds": max(0, observed_seconds - retained_seconds), "created_at": now(),
                "original_settlement_rewritten": False, "new_cycle_created": False, "scientific_approval": False}
            db.execute("INSERT INTO budget_adjustments VALUES(?,?,?,?,?,?,?,?)", (row["reservation_id"], row["budget_key"],
                row["settlement"], old_hash, encoded, evidence_hash, json.dumps(correction, ensure_ascii=False, allow_nan=False), correction["created_at"]))
            db.execute("UPDATE setting_budgets SET charged_seconds=charged_seconds-?,charged_tool_calls=charged_tool_calls-?,charged_sessions=charged_sessions-? WHERE budget_key=?",
                       (credited["seconds"], credited["tool_calls"], credited["sessions"], row["budget_key"]))
            return correction

    def charge_controller(self, key, task_key, elapsed_seconds, *, limits=None):
        elapsed_seconds = self._finite_number(elapsed_seconds, "elapsed_seconds")
        if not isinstance(task_key, str) or not task_key:
            raise ValueError("Controller charges need a stable idempotency task key")
        with self._transaction() as db:
            row = self._ensure_budget(db, key, limits)
            if row is None:
                raise ValueError("Controller charging requires an enabled cumulative budget")
            snapshot = self._snapshot(db, key, row)
            if snapshot["outstanding"]:
                raise CumulativeBudgetError("Settle the outstanding model stage before charging controller work", "outstanding_reservation", snapshot)
            prior = db.execute("SELECT * FROM controller_charges WHERE budget_key=? AND task_key=?", (key, task_key)).fetchone()
            if prior is not None:
                if prior["observed_seconds"] != elapsed_seconds:
                    raise ValueError("An immutable controller charge cannot be replaced by different elapsed time")
                return json.loads(prior["receipt"])
            charged = min(elapsed_seconds, snapshot["remaining"]["seconds"])
            receipt = {"budget_key": key, "task_key": task_key, "observed_seconds": elapsed_seconds,
                       "charged": {"seconds": charged, "tool_calls": 0, "sessions": 0},
                       "overshoot_seconds": max(0, elapsed_seconds - charged), "charged_at": now()}
            db.execute("UPDATE setting_budgets SET charged_seconds=charged_seconds+? WHERE budget_key=?", (charged, key))
            db.execute("INSERT INTO controller_charges VALUES(?,?,?,?,?,?)", (key, task_key, elapsed_seconds, charged,
                       receipt["overshoot_seconds"], json.dumps(receipt, allow_nan=False)))
            return receipt


class CumulativeBudgetError(RuntimeError):
    """A durable budget boundary, never permission to reset/retry a paid stage."""
    def __init__(self, message, reason="budget_exhausted", snapshot=None):
        super().__init__(message)
        self.reason = reason
        self.snapshot = snapshot
