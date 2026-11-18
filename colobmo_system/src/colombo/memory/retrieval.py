"""Read-only, scope-level retrieval. Similarity never establishes applicability."""
from __future__ import annotations
import json
from contextlib import closing
from pathlib import Path
import re
import sqlite3
from .contracts import ContractError, digest, resolve_pointer, safe_id, dependencies
from .store import Store, read_json


PRIVACY_PROJECTION_SCHEMA = "colombo-memory-privacy-projection/1"
PRIVACY_PROJECTION_TRANSFORMATION = "local-locators-and-pinned-hashes-v1"


def tokens(text: str) -> list[str]:
    # English/math identifiers plus Chinese unigrams/bigrams. No NLP service needed.
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_]*|[0-9]+", text.lower())
    for seq in re.findall(r"[\u3400-\u9fff]+", text):
        words.extend(seq); words.extend(seq[i:i+2] for i in range(len(seq)-1))
    return list(dict.fromkeys(words))


def _scope(pointer: str) -> str:
    m = re.match(r"(#/content/(?:variants|oracle_realizations|hardness_claims)/\d+)(?:/|$)", pointer)
    return m.group(1) if m else pointer


def record_card(r: dict, scope_ref: str, facets: list[dict], tier: str) -> dict:
    e = r["evidence"]
    return {"ref": {"id": r["id"], "revision": r["revision"], "kind": r["kind"],
                    "content_hash": digest(r), "tier": tier},
            "title": r["title"], "summary": r["summary"], "use_when": r["use_when"],
            "scope_ref": scope_ref, "facets": facets,
            "research_use": r["navigation"]["research_use"],
            "evidence": {k: e[k] for k in ("basis", "readiness", "statement_complete", "use_restrictions")},
            "unresolved": e.get("unresolved", []),
            "review_status": r.get("extraction_status", {}),
            "read_before_use": True, "certifies_applicability": False}




def render_record(r: dict) -> str:
    status = r["evidence"]["readiness"]
    return (f"# {r['title']}\n\nID: `{r['id']}` · Revision: `{r['revision']}` · Readiness: **{status}**\n\n"
            f"{r['summary']}\n\n## Scientific content\n\n```json\n" +
            json.dumps(r["content"], ensure_ascii=False, indent=2) + "\n```\n\n## Evidence and restrictions\n\n```json\n" +
            json.dumps(r["evidence"], ensure_ascii=False, indent=2) + "\n```\n\n## Sources\n\n```json\n" +
            json.dumps(r["source_refs"], ensure_ascii=False, indent=2) + "\n```\n")


class Reader:
    def __init__(self, root: str | Path, *, allowed_kinds: set[str] | None = None):
        self.store = root if isinstance(root, Store) else Store(root)
        self.allowed_kinds = allowed_kinds

    def _databases(self, include_leads: bool):
        yield self.store.generation() / "catalog.sqlite"
        if include_leads:
            catalog = self.store.lead_catalog()
            if catalog is not None:
                yield catalog

    def _cards(self, include_leads: bool, query: str = "") -> list[tuple[dict, float]]:
        result = []
        query_tokens = tokens(query)[:80]
        match = " OR ".join('"' + t.replace('"', '""') + '"' for t in query_tokens)
        for path in self._databases(include_leads):
            uri = path.resolve().as_uri() + "?mode=ro&immutable=1"
            with closing(sqlite3.connect(uri, uri=True)) as db:
                kinds = sorted(self.allowed_kinds) if self.allowed_kinds is not None else None
                if kinds == []:
                    continue
                projection = (" AND s.kind IN (" + ",".join("?" for _ in kinds) + ")") if kinds else ""
                if match:
                    rows = db.execute("SELECT s.card, bm25(search) FROM search JOIN scopes s ON s.rowid=search.rowid WHERE search MATCH ?" + projection + " ORDER BY bm25(search) LIMIT 500", [match] + (kinds or [])).fetchall()
                else:
                    rows = db.execute("SELECT s.card, 0.0 FROM scopes s WHERE 1=1" + projection, kinds or []).fetchall()
                result.extend((json.loads(c), float(score)) for c, score in rows)
        current = self.store.manifest()["entries"]
        for card, _ in result:
            entry = current.get(card["ref"]["id"])
            if (card["ref"]["tier"] == "published" and entry
                    and entry["content_hash"] == card["ref"]["content_hash"]):
                card["publication"] = {k: entry.get(k) for k in (
                    "revision", "reviewer_run_id", "review_backend", "review_digest", "review_scope")}
                if "privacy_projection" in entry:
                    projection = entry["privacy_projection"]
                    if not isinstance(projection, dict):
                        raise ContractError("Invalid privacy projection metadata")
                    card["publication"]["privacy_projection"] = projection
                    card["publication"]["meaning"] = (
                        "Recorded independent review applies to original content hash "
                        + str(projection.get("original_content_hash"))
                        + "; current content hash " + str(projection.get("projected_content_hash"))
                        + " is a privacy projection with local metadata removed and pinned hashes remapped. "
                        "No new independent review was performed for the projected bytes."
                    )
                else:
                    card["publication"]["meaning"] = "Recorded review for this exact revision; not independent reproof of every claim"
            else:
                card["publication"] = None
        return result

    @staticmethod
    def _checks(card: dict, requested: list[dict]) -> list[dict]:
        checks = []
        for req in requested:
            # Unknown and not_assumed never imply a negative proposition.
            candidates = [f for f in card["facets"] if f["axis"] == req["axis"] and f["concept_id"] == req["concept_id"]
                          and (not req.get("role") or f["role"] == req["role"])
                          and (not req.get("subject") or f["subject"] == req["subject"])]
            states = {f["state"] for f in candidates}
            wanted = req.get("state", "asserted")
            status = "matching" if wanted in states else ("conflict" if wanted == "asserted" and "negated" in states else "unknown")
            checks.append({"requested": req, "status": status, "observed_states": sorted(states)})
        return checks

    def search(self, query: str = "", *, facets: list[dict] | None = None, kinds: list[str] | None = None,
               include_leads: bool = False, limit: int = 12, offset: int = 0,
               intent: str = "explore", exact: bool = False, concept: str | None = None) -> dict:
        if not 1 <= limit <= 50 or offset < 0:
            raise ContractError("limit=1..50 and nonnegative offset required")
        if intent not in {"explore", "apply", "challenge"}:
            raise ContractError("intent must be explore, apply or challenge")
        requested = facets or []
        for f in requested:
            if not isinstance(f, dict) or not f.get("axis") or not f.get("concept_id"):
                raise ContractError("Each filter needs axis and concept_id")
        pool = self._cards(include_leads, query)
        # Facets and use tags add a parallel recall channel, not an AND filter.
        if requested or concept:
            existing = {(c["ref"]["tier"], c["ref"]["id"], c["scope_ref"]) for c, _ in pool}
            for card, _ in self._cards(include_leads):
                key = (card["ref"]["tier"], card["ref"]["id"], card["scope_ref"])
                hit = any(f["axis"] == q["axis"] and f["concept_id"] == q["concept_id"] for f in card["facets"] for q in requested)
                tagged = concept and any(t["concept_id"] == concept for t in card["research_use"])
                if key not in existing and (hit or tagged):
                    pool.append((card, 0.0)); existing.add(key)
        ranked = []
        for card, lexical in pool:
            if kinds and card["ref"]["kind"] not in kinds:
                continue
            if concept and not any(t["concept_id"] == concept for t in card["research_use"]):
                continue
            checks = self._checks(card, requested)
            conflicts = [c for c in checks if c["status"] == "conflict"]
            if exact and conflicts:
                continue
            matched = sum(c["status"] == "matching" for c in checks)
            unknown = sum(c["status"] == "unknown" for c in checks)
            score = -lexical + 2.0 * matched - 0.3 * len(conflicts)
            if card["ref"]["tier"] == "published":
                score += 0.1
            purpose = "challenge_material" if intent == "challenge" else ("transfer_lead" if unknown or conflicts else "context_candidate")
            card.update(match_checks=checks, why_returned={"lexical_score": -lexical, "matching_facets": matched,
                "unknown_conditions": unknown, "conflicts": len(conflicts)}, use_hint=purpose,
                application_status="not_assessed", score=score)
            ranked.append(card)
        # Same scope from a published record wins over its obsolete seed.
        ranked.sort(key=lambda c: (c["ref"]["tier"] != "published", -c["score"], c["ref"]["id"]))
        deduped = {}; selected = []
        for c in ranked:
            key = (c["ref"]["id"], c["scope_ref"])
            if key not in deduped:
                deduped[key] = True; selected.append(c)
        selected.sort(key=lambda c: (-c["score"], c["ref"]["id"], c["scope_ref"]))
        page = selected[offset:offset+limit]
        return {"items": page, "total_candidates": len(selected), "next_offset": offset+limit if offset+limit < len(selected) else None,
                "recall_exhaustive": False, "note": "Retrieval is a reading recommendation, not an applicability proof. No hit is not evidence of absence."}

    def overview(self, *, include_leads: bool = True, limit: int = 16, offset: int = 0, group: str | None = None) -> dict:
        if not 1 <= limit <= 50 or offset < 0:
            raise ContractError("Invalid overview window")
        cards = self._cards(include_leads)
        entries = {}; concepts = {}
        for c, _ in cards:
            entries[(c["ref"]["tier"], c["ref"]["id"])] = c
            for t in c["research_use"]:
                key = t["concept_id"]
                b = concepts.setdefault(key, {"concept_id": key, "group": t["group"], "examples": [], "entry_ids": set()})
                b["entry_ids"].add(c["ref"]["id"])
                if len(b["examples"]) < 3 and c["ref"]["id"] not in [e["ref"]["id"] for e in b["examples"]]:
                    b["examples"].append({"title": c["title"], "ref": c["ref"], "readiness": c["evidence"]["readiness"]})
        for b in concepts.values():
            b["count"] = len(b.pop("entry_ids"))
        counts = {}
        for (tier, _), card in entries.items():
            key = tier + ":" + card["ref"]["kind"]
            counts[key] = counts.get(key, 0) + 1
        branches = sorted([b for b in concepts.values() if group is None or b["group"] == group], key=lambda b: (b["group"], b["concept_id"]))
        return {"counts": counts, "branches": branches[offset:offset+limit], "next_offset": offset+limit if offset+limit < len(branches) else None, "total_branches": len(branches),
                "note": "Global method map; not restricted to the current setting or Atlas ID. Paginated: do not treat the first page as exhaustive."}

    def browse(self, concept: str, **kwargs) -> dict:
        return self.search(concept=concept, **kwargs)

    def _record(self, ref: dict) -> dict:
        if ref.get("tier") == "lead":
            return self.store.lead(ref)
        if ref.get("tier") != "published" or type(ref.get("revision")) is not int or ref["revision"] < 1:
            raise ContractError("Published reference needs its exact positive revision; retrieve a current card explicitly")
        return self.store.get(ref["id"], revision=ref["revision"], content_hash=ref["content_hash"], kind=ref["kind"])

    def read(self, ref: dict, *, pointer: str = "#", offset: int = 0, limit: int = 10000) -> dict:
        if offset < 0 or not 1 <= limit <= 20000:
            raise ContractError("Invalid read window")
        r = self._record(ref); value = resolve_pointer(r, pointer)
        text = json.dumps(value, ensure_ascii=False, indent=2)
        end = min(offset + limit, len(text)); current = self.store.manifest()["entries"].get(r["id"])
        warnings = []
        manifest = self.store.manifest()
        for dep, used_revision in dependencies(r):
            current_dep = manifest["entries"].get(dep)
            if current_dep and (current_dep["revision"] != used_revision or current_dep.get("use_restrictions")):
                warnings.append({"id": dep, "used_revision": used_revision,
                    "current_revision": current_dep["revision"], "current_use_restrictions": current_dep.get("use_restrictions", []),
                    "note": "Direct dependency changed or has restrictions; no automatic mathematical invalidation is inferred."})
        return {"ref": ref, "pointer": pointer, "text": text[offset:end], "offset": offset, "dependency_warnings": warnings,
                "complete": end >= len(text), "next_offset": end if end < len(text) else None,
                "current_revision": current["revision"] if current else None,
                "current_use_restrictions": current.get("use_restrictions", []) if current else [],
                "note": "A partial page is not a complete statement. Historical bytes are preserved; inspect current restrictions."}

    def expand(self, ref: dict, *, relations: list[str] | None = None, limit: int = 12, offset: int = 0, include_leads: bool = False) -> dict:
        if not 1 <= limit <= 50 or offset < 0:
            raise ContractError("Invalid expansion window")
        r = self._record(ref); links = list(r["links"])
        lead_records = {}
        if include_leads or ref.get("tier") == "lead":
            lead_records = {x["id"]: x for x in self.store.lead_records()}
        if r["kind"] == "source":
            # Match the scientific source version, not just the bibliographic family.
            version = r["content"].get("bibliographic_identity", {}).get("version")
            related = dict(lead_records)
            related.update({x["id"]: x for x in self.store.all_records()})
            for other in related.values():
                if any(s["source_id"] == r["id"] and s["source_version"] == version for s in other["source_refs"]):
                    links.append({"relation": "paper_contribution", "target_id": other["id"],
                        "target_revision": other["revision"], "note": other["title"], "scope_ref": "#/content"})
        if relations:
            links = [x for x in links if x["relation"] in relations]
        result = []
        manifest = self.store.manifest()
        for link in links[offset:offset+limit]:
            target = manifest["entries"].get(link["target_id"])
            item = dict(link)
            if target and (link["target_revision"] is None or target["revision"] == link["target_revision"]):
                item["ref"] = {k: target[k] for k in ("id", "revision", "kind", "content_hash", "tier")}
            elif link["target_revision"] is not None:
                for receipt in manifest["receipts"].values():
                    for old in receipt["published_refs"]:
                        if old["id"] == link["target_id"] and old["revision"] == link["target_revision"]:
                            item["ref"] = old
            if "ref" not in item and link["target_id"] in lead_records:
                candidate = lead_records[link["target_id"]]
                item["ref"] = {"id": candidate["id"], "kind": candidate["kind"], "revision": None,
                    "content_hash": digest(candidate), "tier": "lead"}
            if "ref" not in item:
                item["unresolved"] = True
            result.append(item)
        return {"items": result, "next_offset": offset+limit if offset+limit < len(links) else None,
                "note": "Related/discovery links do not assert mathematical implication."}

    def call(self, mode: str, **kwargs) -> dict:
        if mode not in {"overview", "browse", "search", "read", "expand"}:
            raise ContractError("Unknown memory operation")
        return getattr(self, mode)(**kwargs)
