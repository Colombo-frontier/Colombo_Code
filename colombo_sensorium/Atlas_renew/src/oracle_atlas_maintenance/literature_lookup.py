"""Exact, bounded metadata identity lookups. Never theorem evidence or a grant."""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import json
import re
import xml.etree.ElementTree as ET
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from oracle_atlas.discovery.bibliography import normalize_doi


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def canonical_identifier(kind, identifier):
    if not isinstance(identifier, str) or not identifier.strip() or len(identifier) > 10000:
        raise ValueError("A bounded exact metadata identifier is required")
    identifier = identifier.strip()
    if kind == "doi":
        value = normalize_doi(identifier)
        if not re.fullmatch(r"10\.\d{4,9}/[^\s<>]+", value):
            raise ValueError("Invalid exact DOI")
        return value
    if kind == "arxiv":
        value = re.sub(r"^(?:arxiv:|https?://(?:export\.)?arxiv\.org/(?:abs|pdf)/)", "", identifier, flags=re.I)
        value = re.sub(r"\.pdf$", "", value)
        if not re.fullmatch(r"(?:\d{4}\.\d{4,5}|[a-zA-Z][a-zA-Z.\-]+/\d{7})(?:v[1-9]\d*)?", value):
            raise ValueError("Invalid exact arXiv identifier")
        return value
    if kind == "url":
        value = urlsplit(identifier)
        if value.scheme not in {"https", "http"} or not value.hostname or value.username or value.password:
            raise ValueError("A public HTTP(S) metadata URL without credentials is required")
        secret = {"api_key", "apikey", "key", "token", "access_token", "secret", "signature", "mailto"}
        if any(key.lower() in secret for key, _ in parse_qsl(value.query, keep_blank_values=True)):
            raise ValueError("Public metadata URL lookup must not contain credential/contact query fields")
        return urlunsplit((value.scheme.lower(), value.netloc.lower(), value.path, value.query, ""))
    raise ValueError("Lookup kind must be doi, arxiv or url")


def record_id(record):
    """Stable identity across pages; metadata changes do not invent a new paper."""
    ids = record.get("identifiers") or {}
    if ids.get("doi"):
        identity = {"doi": canonical_identifier("doi", ids["doi"])}
    elif ids.get("arxiv"):
        identity = {"arxiv": re.sub(r"v\d+$", "", canonical_identifier("arxiv", ids["arxiv"]))}
    elif record.get("paper_id"):
        identity = {"paper_id": str(record["paper_id"])}
    else:
        identity = {"urls": sorted(str(x) for x in record.get("urls", [])), "title": record.get("title", "")}
    return digest(identity)


class _Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.values, self.title, self.in_title = {}, [], False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            name = (attrs.get("name") or attrs.get("property") or "").lower()
            if name in {"citation_title", "citation_doi", "citation_arxiv_id", "citation_publication_date",
                        "citation_online_date", "dc.date", "dc.title", "article:published_time", "article:modified_time"}:
                self.values.setdefault(name, []).append(attrs.get("content", "")[:3000])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and sum(map(len, self.title)) < 3000:
            self.title.append(data[:3000])


def lookup_metadata(kind, identifier, *, bibliography, client, known_versions=None):
    """No title-search fallback. Network and cache admission belong to the host."""
    identifier = canonical_identifier(kind, identifier)
    if kind == "doi":
        captured = []
        prior = getattr(bibliography, "client", None)
        if prior is not None:
            class Capture:
                def get(self, url, **kwargs):
                    response = prior.get(url, **kwargs)
                    captured.append(response)
                    return response
            bibliography.client = Capture()
        try:
            record = bibliography.lookup_doi(identifier)
        finally:
            if prior is not None:
                bibliography.client = prior
        actual = canonical_identifier("doi", record.get("identifiers", {}).get("doi", ""))
        if actual != identifier:
            raise ValueError("DOI lookup returned a different exact identity")
        notices, alerts, provenance = {}, [], {}
        if captured:
            response = captured[-1]
            payload = json.loads(response.body).get("message", {})
            if not isinstance(payload, dict):
                raise ValueError("Exact DOI update metadata has an invalid structure")
            notices = {key: value for key, value in payload.items()
                       if key in {"update-to", "relation", "update-policy"} or key.startswith("is-")}
            for key, value in notices.items():
                if key == "update-policy":
                    continue
                material = key in {"update-to", "relation"} or bool(re.search(r"retract|correct|update|withdraw|version", key, re.I))
                if material and value and value is not False:
                    alerts.append({"kind": "doi_update_or_relation", "field": key,
                                   "metadata_value_sha256": digest(value),
                                   "reason": "Official DOI metadata reports an update/relation/flag requiring applicability assessment"})
            provenance = {"metadata_response_sha256": hashlib.sha256(response.body).hexdigest(),
                          "metadata_url": response.url, "metadata_fetched_at": response.fetched_at}
        encoded = json.dumps(notices, ensure_ascii=False, sort_keys=True)
        if len(encoded) > 6000:
            notices = {"truncated": True, "sha256": digest(notices), "metadata_preview": encoded[:4000]}
            alerts.append({"kind": "doi_update_metadata_truncated", "reason": "Bounded identity lookup did not fully expose update metadata"})
        return {"record": record, "identity": {"doi": actual}, "version_history_complete": False,
                "official_update_metadata": notices, "correction_status": "not_established_by_lookup",
                "material_alerts": alerts, **provenance}
    if kind == "arxiv":
        response = client.get("https://export.arxiv.org/api/query?" + urlencode({"id_list": identifier, "max_results": 1}))
        root = ET.fromstring(response.body)
        ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
        entries = root.findall("a:entry", ns)
        if len(entries) != 1:
            raise ValueError("Exact arXiv lookup did not return one record")
        entry = entries[0]
        actual = canonical_identifier("arxiv", entry.findtext("a:id", "", ns))
        base = re.sub(r"v\d+$", "", actual)
        if base != re.sub(r"v\d+$", "", identifier) or (re.search(r"v\d+$", identifier) and actual != identifier):
            raise ValueError("arXiv lookup returned a different exact version")
        if not re.search(r"v[1-9]\d*$", actual):
            raise ValueError("arXiv lookup omitted its exact returned version")
        published, updated = entry.findtext("a:published", "", ns), entry.findtext("a:updated", "", ns)
        record = {"paper_id": "arxiv:" + base, "title": " ".join(entry.findtext("a:title", "", ns).split()),
            "identifiers": {"arxiv": base}, "urls": [x.get("href") for x in entry.findall("a:link", ns) if x.get("href")],
            "abstract": " ".join(entry.findtext("a:summary", "", ns).split())[:1500],
            "publication_events": [{"kind": "preprint", "date": published, "version_id": base + "v1"},
                                   {"kind": "revision", "date": updated, "version_id": actual}],
            "versions": [{"version_id": actual, "date": updated, "url": "https://arxiv.org/abs/" + actual}],
            "metadata_status": "exact_api_identity", "read_status": "unread"}
        known = sorted({str(v) for v in known_versions or [] if re.fullmatch(re.escape(base) + r"v[1-9]\d*", str(v))},
                       key=lambda v: int(v.rsplit("v", 1)[1]))
        alerts = []
        if known and actual not in known:
            alerts.append({"kind": "arxiv_version_differs_from_baseline", "returned_version": actual,
                           "known_baseline_versions": known, "reason": "This exact returned revision is absent from the frozen baseline version references"})
        return {"record": record, "identity": {"arxiv": base, "returned_version": actual},
            "latest_version_verified": not bool(re.search(r"v\d+$", identifier)),
            "requested_version": identifier if re.search(r"v\d+$", identifier) else None,
            "version_history_complete": False, "metadata_response_sha256": hashlib.sha256(response.body).hexdigest(),
            "metadata_url": response.url, "metadata_fetched_at": response.fetched_at,
            "known_baseline_versions": known, "material_alerts": alerts,
            "correction_status": "not_established_by_lookup"}
    response = client.get(identifier)
    content_type = response.headers.get("content-type", "").lower()
    if "html" not in content_type and not response.body.lstrip().lower().startswith((b"<!doctype html", b"<html")):
        raise ValueError("URL metadata fallback requires bounded HTML; use source_fetch for paper bodies")
    parser = _Metadata()
    parser.feed(response.body.decode("utf-8", errors="replace"))
    values = parser.values
    title = (values.get("citation_title") or values.get("dc.title") or [" ".join(parser.title)])[0]
    ids = {}
    for key, name in (("citation_doi", "doi"), ("citation_arxiv_id", "arxiv")):
        if values.get(key):
            ids[name] = canonical_identifier(name, values[key][0])
    record = {"paper_id": "url:" + hashlib.sha256(identifier.encode()).hexdigest(), "title": title,
        "identifiers": ids, "urls": [identifier, response.url], "publication_events": [], "versions": [],
        "metadata_fields": values, "metadata_status": "publisher_page_metadata_unverified", "read_status": "unread"}
    return {"record": record, "identity": {"url": identifier}, "version_history_complete": False,
        "metadata_response_sha256": hashlib.sha256(response.body).hexdigest(), "metadata_url": response.url,
        "metadata_fetched_at": response.fetched_at,
        "limitations": ["HTML identity/date metadata is unverified; primary-source status and theorem applicability are not certified."]}
