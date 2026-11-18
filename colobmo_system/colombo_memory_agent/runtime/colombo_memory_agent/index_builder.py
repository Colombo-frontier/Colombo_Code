"""Derived index generation, available only to the independent Memory Agent."""
from __future__ import annotations
import json
from pathlib import Path
import sqlite3
from colombo.memory.contracts import resolve_pointer
from colombo.memory.retrieval import _scope, record_card, tokens


def build_index(path: Path, records: list[dict], *, tier: str) -> None:
    db = sqlite3.connect(path)
    try:
        db.execute("CREATE TABLE scopes(rowid INTEGER PRIMARY KEY, entry_id TEXT, kind TEXT, scope_ref TEXT, card TEXT)")
        db.execute("CREATE VIRTUAL TABLE search USING fts5(text, tokenize='unicode61')")
        for r in records:
            groups = {}
            for f in r["navigation"]["facets"]:
                groups.setdefault(_scope(f["scope_ref"]), []).append(f)
            if not groups:
                groups["#/content"] = []
            for pointer, facets in groups.items():
                card = record_card(r, pointer, facets, tier)
                body = resolve_pointer(r, pointer)
                # Do not index other variants in this scope's full-text row.
                text = " ".join([r["title"], r["summary"], " ".join(r["aliases"]),
                    " ".join(r["use_when"]), " ".join(r["navigation"]["query_aliases"]),
                    json.dumps(body, ensure_ascii=False), json.dumps(facets, ensure_ascii=False),
                    json.dumps(r["navigation"]["research_use"], ensure_ascii=False)])
                rowid = db.execute("INSERT INTO scopes(entry_id,kind,scope_ref,card) VALUES(?,?,?,?)",
                    (r["id"], r["kind"], pointer, json.dumps(card, ensure_ascii=False))).lastrowid
                db.execute("INSERT INTO search(rowid,text) VALUES(?,?)", (rowid, " ".join(tokens(text))))
        db.execute("CREATE INDEX by_entry ON scopes(entry_id)"); db.commit()
    finally:
        db.close()
