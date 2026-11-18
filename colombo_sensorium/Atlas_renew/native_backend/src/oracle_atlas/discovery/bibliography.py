"""Bibliographic adapters for broad TASK searches; record publication events rather than inferring year membership from top-level year."""
from __future__ import annotations

import copy
from datetime import date as Date
import hashlib
import json
import os
import re
import shlex
import threading
import time
import xml.etree.ElementTree as ET
from urllib.parse import quote, urlencode

from .http import DiscoveryError, HTTPClient, display_url
from .sources import html_text

_ARXIV_LOCK = threading.Lock()
_LAST_ARXIV = [0.0]


def _unique(items):
    result, seen = [], set()
    for item in items:
        key = json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        if key not in seen:
            seen.add(key)
            result.append(copy.deepcopy(item))
    return result


def normalize_doi(value):
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", str(value or ""), flags=re.I)
    return re.sub(r"^doi:\s*", "", value, flags=re.I).strip().lower()


def _id(prefix, value):
    return prefix + ":" + hashlib.sha256(str(value).encode()).hexdigest()[:24]


def _provenance(provider, response, *, field=None):
    item = {"provider": provider, "url": display_url(response.url), "fetched_at": response.fetched_at}
    if field:
        item["field"] = field
    item["source_id"] = _id("bibsource", json.dumps(item, sort_keys=True))
    return item


def _event(kind, date, source, *, medium="unspecified", venue="", version_id=None, verified=False):
    if not isinstance(date, str):
        return None
    date = date.split("T", 1)[0].strip()
    if not re.fullmatch(r"\d{4}(?:-\d{2})?(?:-\d{2})?", date):
        return None
    try:
        parts = [int(x) for x in date.split("-")]
        Date(*(parts + [1] * (3 - len(parts))))
    except ValueError:
        return None
    event = {"kind": kind, "date": date, "year": int(date[:4]), "medium": medium,
             "venue": venue, "version_id": version_id, "verified": bool(verified),
             "verification_sources": [source["source_id"]] if verified else [],
             "source_refs": [source["source_id"]]}
    event["event_id"] = _id("event", json.dumps({k: event[k] for k in
                            ("kind", "date", "medium", "venue", "version_id")}, sort_keys=True))
    return event


def _parts_date(value):
    try:
        parts = value["date-parts"][0]
        if not parts or not isinstance(parts[0], int) or not 1000 <= parts[0] <= 9999:
            return None
        if len(parts) > 1 and not 1 <= parts[1] <= 12:
            return None
        if len(parts) > 2 and not 1 <= parts[2] <= 31:
            return None
        return "-".join([str(parts[0])] + [f"{v:02d}" for v in parts[1:3]])
    except (KeyError, IndexError, TypeError):
        return None


def qualifies_year(record: dict, years, event_kind="publication") -> bool:
    """Check only verified events. Neither top-level year nor verified participates in the decision.

    event_kind may be publication / preprint / revision / any; including preprints in the annual scope requires an explicit choice.
    """
    wanted = {years} if isinstance(years, int) and not isinstance(years, bool) else set(years)
    if not all(isinstance(y, int) and not isinstance(y, bool) for y in wanted):
        raise ValueError("years must be an integer or a list of integers.")
    if event_kind not in ("publication", "preprint", "revision", "any"):
        raise ValueError("Unknown event_kind.")
    for event in record.get("publication_events", []):
        if not isinstance(event, dict) or event.get("verified") is not True:
            continue
        if not event.get("verification_sources"):
            continue
        if event_kind != "any" and event.get("kind") != event_kind:
            continue
        year = event.get("year")
        date = event.get("date", "")
        if isinstance(date, str) and len(date) >= 4 and date[:4].isdigit() and year != int(date[:4]):
            continue
        if year in wanted:
            return True
    return False


def verify_publication(record: dict, *, date: str, source: dict, venue="", medium="unspecified",
                       event_kind="publication", version_id=None) -> dict:
    """The sole promotion path for bibliographic verification: add both a verified event and traceable provenance."""
    if event_kind not in ("publication", "preprint", "revision"):
        raise ValueError("Unknown event_kind.")
    if not source.get("url") and not source.get("artifact_ref"):
        raise ValueError("A verification source requires a URL or a pinned artifact_ref.")
    evidence = copy.deepcopy(source)
    evidence.setdefault("source_id", _id("bibsource", json.dumps(evidence, sort_keys=True)))
    event = _event(event_kind, date, evidence, medium=medium, venue=venue,
                   version_id=version_id, verified=True)
    if event is None:
        raise ValueError("Invalid verification date format.")
    updated = copy.deepcopy(record)
    updated["publication_events"] = _merge_events(record.get("publication_events", []), [event])
    updated["provenance"] = _unique(record.get("provenance", []) + [evidence])
    updated["metadata_status"] = "verified_metadata"
    return updated


def _merge_events(a, b):
    merged = {}
    for event in a + b:
        if not isinstance(event, dict):
            raise ValueError("A publication event must be an object.")
        semantic = {k: event.get(k) for k in ("kind", "date", "medium", "venue", "version_id")}
        key = json.dumps(semantic, sort_keys=True)
        if key not in merged:
            merged[key] = copy.deepcopy(event)
            continue
        old = merged[key]
        verified = old.get("verified") is True or event.get("verified") is True
        old.update({k: copy.deepcopy(v) for k, v in event.items() if k not in
                    ("verified", "verification_sources", "source_refs") and v is not None})
        old["verified"] = verified
        for field in ("verification_sources", "source_refs"):
            old[field] = _unique(old.get(field, []) + event.get(field, []))
    return list(merged.values())


def merge_records(a: dict, b: dict) -> dict:
    """Merge bibliographic records confirmed to describe the same paper; do not automatically merge scientific content based on title similarity."""
    left = a.get("identifiers", {})
    right = b.get("identifiers", {})
    for key in ("doi", "arxiv", "openalex"):
        if left.get(key) and right.get(key) and left[key] != right[key]:
            raise ValueError(f"Different {key} identifiers cannot be merged implicitly; an explicit version relationship is required.")
    merged = copy.deepcopy(a)
    # Verified records take precedence; unverified leads cannot overwrite a verified primary record.
    prefer_b = b.get("metadata_status") == "verified_metadata" or a.get("metadata_status") != "verified_metadata"
    for key, value in b.items():
        if key not in merged or merged[key] in (None, "", [], {}):
            merged[key] = copy.deepcopy(value)
        elif key in ("title", "authors", "abstract", "venue", "work_type") and prefer_b and value:
            merged[key] = copy.deepcopy(value)
    merged["identifiers"] = {**left, **right}
    merged["publication_events"] = _merge_events(a.get("publication_events", []), b.get("publication_events", []))
    for key in ("provenance", "urls", "versions", "task_ids", "source_refs", "aliases"):
        merged[key] = _unique(a.get(key, []) + b.get(key, []))
    if a.get("title") != b.get("title"):
        merged["alternate_titles"] = _unique(a.get("alternate_titles", []) + b.get("alternate_titles", []) +
                                            [x for x in (a.get("title"), b.get("title")) if x])
    if a.get("paper_id") and b.get("paper_id") != a["paper_id"] and b.get("paper_id"):
        merged["aliases"] = _unique(merged["aliases"] + [b["paper_id"]])
    if "verified_metadata" in (a.get("metadata_status"), b.get("metadata_status")):
        merged["metadata_status"] = "verified_metadata"
    # A paper already read does not revert to unread after a new search hit.
    rank = {"unread": 0, "fetched_unread": 1, "read": 2}
    merged["read_status"] = max((a.get("read_status", "unread"), b.get("read_status", "unread")),
                                key=lambda s: rank.get(s, 0))
    return merged


def deduplicate_records(records: list[dict]) -> list[dict]:
    """Deduplicate only by reliable bibliographic IDs; leave potential duplicates with similar titles to the LLM."""
    output = []
    lookup = {}
    for record in records:
        keys = [(kind, value) for kind, value in record.get("identifiers", {}).items() if value]
        indices = {lookup[k] for k in keys if k in lookup}
        if len(indices) > 1:
            # An ID links two existing groups and must be checked first; neither group may be silently selected or discarded.
            raise ValueError("Bibliographic identifiers link two record groups; explicitly verify their version relationship.")
        index = next(iter(indices)) if indices else len(output)
        if index == len(output):
            output.append(copy.deepcopy(record))
        else:
            output[index] = merge_records(output[index], record)
        for key in keys:
            lookup[key] = index
    return output


class Bibliography:
    def __init__(self, client=None, *, cache_dir=None, timeout=30, contact=None,
                 openalex_api_key_env="OPENALEX_API_KEY", arxiv_interval=3.0):
        self.client = client or HTTPClient(cache_dir=cache_dir, timeout=timeout,
                                          user_agent="AtlasNativeBackend" + (f" (mailto:{contact})" if contact else ""))
        self.contact = contact
        self.openalex_api_key_env = openalex_api_key_env
        self.arxiv_interval = max(0, float(arxiv_interval))
        self._arxiv_lock = _ARXIV_LOCK

    def search(self, provider, query, year=None, limit=20, cursor=None):
        if provider not in ("arxiv", "crossref", "openalex"):
            raise ValueError("provider must be arxiv/crossref/openalex.")
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must not be empty.")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 100:
            raise ValueError("limit must be in the range 1-100.")
        if year is not None and (isinstance(year, bool) or not isinstance(year, int) or not 1000 <= year <= 9999):
            raise ValueError("year must be a four-digit year.")
        if provider == "arxiv":
            result = self._arxiv(query, year, limit, cursor)
        elif provider == "crossref":
            result = self._crossref(query, year, limit, cursor)
        else:
            result = self._openalex(query, year, limit, cursor)
        result.update({"provider": provider, "query": query, "year": year,
                       "coverage": {"exhaustive": False, "read_papers": 0,
                                    "scope": "One page of bibliography for this query; it does not establish that the annual literature has been fully read or exhaustively searched."}})
        return result

    def _arxiv(self, query, year, limit, cursor):
        start = int(cursor or 0)
        if start < 0:
            raise ValueError("arXiv cursor must be a nonnegative offset.")
        if not re.search(r"\b(?:ti|au|abs|co|jr|cat|rn|id|all):", query):
            words = shlex.split(query)
            query = " AND ".join('all:"' + word.replace('"', '') + '"' for word in words)
        if year:
            query = f"({query}) AND submittedDate:[{year}01010000 TO {year}12312359]"
        params = {"search_query": query, "start": start, "max_results": limit,
                  "sortBy": "submittedDate", "sortOrder": "descending"}
        url = "https://export.arxiv.org/api/query?" + urlencode(params)
        with self._arxiv_lock:
            wait = self.arxiv_interval - (time.monotonic() - _LAST_ARXIV[0])
            if wait > 0:
                time.sleep(wait)
            response = self.client.get(url)
            _LAST_ARXIV[0] = time.monotonic()
        try:
            root = ET.fromstring(response.body)
        except ET.ParseError as exc:
            raise DiscoveryError("arXiv did not return valid Atom XML.") from exc
        ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom",
              "o": "http://a9.com/-/spec/opensearch/1.1/"}
        provenance = _provenance("arxiv", response)
        records = []
        for entry in root.findall("a:entry", ns):
            identifier = entry.findtext("a:id", "", ns)
            if "/api/errors" in identifier:
                raise DiscoveryError("arXiv rejected the query syntax; revise query.")
            versioned = identifier.rsplit("/abs/", 1)[-1]
            base = re.sub(r"v\d+$", "", versioned)
            published = entry.findtext("a:published", "", ns)
            updated = entry.findtext("a:updated", "", ns)
            events = [_event("preprint", published, provenance, medium="arxiv", version_id=base + "v1", verified=True)]
            if updated != published:
                events.append(_event("revision", updated, provenance, medium="arxiv", version_id=versioned, verified=True))
            doi = normalize_doi(entry.findtext("x:doi", "", ns))
            identifiers = {"arxiv": base}
            if doi:
                identifiers["doi"] = doi
            urls = [link.attrib.get("href") for link in entry.findall("a:link", ns) if link.attrib.get("href")]
            records.append({"paper_id": "arxiv:" + base,
                "title": " ".join(entry.findtext("a:title", "", ns).split()),
                "authors": [author.findtext("a:name", "", ns) for author in entry.findall("a:author", ns)],
                "abstract": " ".join(entry.findtext("a:summary", "", ns).split()),
                "identifiers": identifiers, "urls": _unique(urls),
                "venue": entry.findtext("x:journal_ref", "", ns), "work_type": "preprint",
                "publication_events": [e for e in events if e], "provenance": [provenance],
                "versions": [{"version_id": versioned, "kind": "arxiv", "url": identifier, "date": updated,
                              "source_ref": provenance["source_id"]}],
                "read_status": "unread", "metadata_status": "verified_metadata"})
        total = int(root.findtext("o:totalResults", str(len(records)), ns))
        next_cursor = str(start + len(records)) if records and start + len(records) < total else None
        return {"records": records, "next_cursor": next_cursor, "total": total,
                "provenance": [provenance], "cached": response.cached}

    def _crossref(self, query, year, limit, cursor):
        params = {"query": query, "rows": limit, "cursor": cursor or "*"}
        if year:
            params["filter"] = f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31"
        if self.contact:
            params["mailto"] = self.contact
        response = self.client.get("https://api.crossref.org/works?" + urlencode(params))
        raw = response.json()
        if not isinstance(raw, dict) or not isinstance(raw.get("message"), dict):
            raise DiscoveryError("Crossref returned an invalid structure.")
        payload = raw["message"]
        records = [self._crossref_record(row, response) for row in payload.get("items", [])]
        next_cursor = payload.get("next-cursor") if records and len(records) >= limit else None
        return {"records": records, "next_cursor": next_cursor, "total": payload.get("total-results"),
                "provenance": [_provenance("crossref", response)], "cached": response.cached}

    def lookup_doi(self, doi):
        """Targeted bibliographic verification; return a record with verified events that merge_records can merge directly into the annual catalog."""
        doi = normalize_doi(doi)
        if not doi.startswith("10.") or "/" not in doi:
            raise ValueError("Invalid DOI.")
        response = self.client.get("https://api.crossref.org/works/" + quote(doi, safe=""))
        payload = response.json().get("message")
        if not isinstance(payload, dict):
            raise DiscoveryError("Crossref DOI lookup returned an invalid structure.")
        return self._crossref_record(payload, response)

    def _crossref_record(self, row, response):
        doi = normalize_doi(row.get("DOI"))
        provenance = _provenance("crossref", response)
        title = " ".join(row.get("title") or [])
        venue = " ".join(row.get("container-title") or [])
        events, sources = [], [provenance]
        work_type = row.get("type", "unknown")
        for field, medium in (("published-online", "online"), ("published-print", "print"),
                              ("published", "unspecified"), ("issued", "issued")):
            date = _parts_date(row.get(field, {}))
            if not date:
                continue
            source = _provenance("crossref", response, field=field)
            sources.append(source)
            kind = "preprint" if work_type == "posted-content" else "publication"
            events.append(_event(kind, date, source, medium=medium, venue=venue, version_id=doi, verified=True))
        urls = [row.get("URL")] + [link.get("URL") for link in row.get("link", [])]
        if doi:
            urls.append("https://doi.org/" + doi)
        return {"paper_id": "doi:" + doi if doi else _id("crossref", title), "title": title,
                "authors": [" ".join(filter(None, (a.get("given"), a.get("family")))) or a.get("name", "")
                            for a in row.get("author", [])],
                "abstract": html_text(row.get("abstract", "")), "identifiers": {"doi": doi} if doi else {},
                "urls": _unique([u for u in urls if u]), "venue": venue, "work_type": work_type,
                "publication_events": [e for e in events if e], "provenance": sources,
                "versions": [{"version_id": doi, "kind": work_type, "url": row.get("URL"),
                              "source_ref": provenance["source_id"]}],
                "metadata_status": "verified_metadata" if events else "lead", "read_status": "unread"}

    def _openalex(self, query, year, limit, cursor):
        params = {"search": query, "per_page": limit, "cursor": cursor or "*"}
        if year:
            params["filter"] = f"publication_year:{year}"
        if self.contact:
            params["mailto"] = self.contact
        key = os.environ.get(self.openalex_api_key_env)
        if key:
            params["api_key"] = key
        response = self.client.get("https://api.openalex.org/works?" + urlencode(params))
        payload = response.json()
        if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
            raise DiscoveryError("OpenAlex returned an invalid structure.")
        provenance, records = _provenance("openalex", response), []
        for row in payload["results"]:
            identifiers = {"openalex": row.get("id", "")}
            doi = normalize_doi(row.get("doi"))
            if doi:
                identifiers["doi"] = doi
            locations = row.get("locations") or [row.get("primary_location") or {}]
            urls = [loc.get(field) for loc in locations for field in ("landing_page_url", "pdf_url") if loc]
            location = row.get("primary_location") or {}
            venue = (location.get("source") or {}).get("display_name", "")
            event = _event("publication", row.get("publication_date"), provenance, venue=venue,
                           version_id=row.get("id"), verified=False)
            inverted = row.get("abstract_inverted_index") or {}
            positions = [(position, word) for word, locs in inverted.items() for position in locs]
            abstract = " ".join(word for _, word in sorted(positions))
            records.append({"paper_id": row.get("id") or _id("openalex", row.get("title", "")),
                            "title": row.get("title") or "", "abstract": abstract,
                            "authors": [(a.get("author") or {}).get("display_name", "") for a in row.get("authorships", [])],
                            "identifiers": identifiers, "urls": _unique([u for u in urls if u]),
                            "venue": venue, "work_type": row.get("type", "unknown"),
                            "publication_events": [event] if event else [], "provenance": [provenance],
                            "versions": [], "metadata_status": "lead", "read_status": "unread"})
        return {"records": records, "next_cursor": payload.get("meta", {}).get("next_cursor") if records else None,
                "total": payload.get("meta", {}).get("count"), "provenance": [provenance], "cached": response.cached}
