"""Regressions for bibliographic event handoffs, source archiving, and reference fidelity. All external HTTP uses fixed fixtures."""
from __future__ import annotations

from datetime import date, datetime, timezone
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from oracle_atlas.discovery import Bibliography, merge_records, qualifies_year, verify_publication, fetch_source
from oracle_atlas.discovery.bibliography import deduplicate_records
from oracle_atlas.discovery.http import HTTPResult, DiscoveryError, public_url


PUBLICATION_YEAR = date.today().year - 1
REVISION_YEAR = PUBLICATION_YEAR + 1
CREATED_YEAR = PUBLICATION_YEAR - 1
PUBLICATION_DATE = date(PUBLICATION_YEAR, 12, 3).isoformat()
REVISION_DATE = date(REVISION_YEAR, 1, 1).isoformat()


class FakeHTTP:
    def __init__(self, body, content_type="application/json"):
        self.body = body.encode() if isinstance(body, str) else body
        self.content_type = content_type
        self.urls = []
    def get(self, url, *, refresh=False):
        self.urls.append(url)
        return HTTPResult(url, self.body, {"content-type": self.content_type}, datetime.now(timezone.utc).isoformat())


CROSSREF = {"DOI": "10.1234/example", "title": ["Oracle paper"], "container-title": ["Fixture Journal"],
            "type": "journal-article", "published-online": {"date-parts": [[PUBLICATION_YEAR, 12, 3]]},
            "published-print": {"date-parts": [[REVISION_YEAR, 2]]}, "created": {"date-parts": [[CREATED_YEAR, 1, 1]]},
            "URL": "https://doi.org/10.1234/example", "author": [{"given": "A", "family": "Researcher"}]}


class BibliographyTests(unittest.TestCase):
    def test_verified_record_reaches_annual_queue_after_merge(self):
        lead = {"paper_id": "lead-1", "identifiers": {"doi": "10.1234/example"}, "year": PUBLICATION_YEAR, "verified": True,
                "publication_events": [{"kind": "publication", "date": PUBLICATION_DATE, "year": PUBLICATION_YEAR,
                                        "medium": "online", "venue": "Fixture Journal", "version_id": "10.1234/example",
                                        "verified": False, "source_refs": ["old"], "verification_sources": []}],
                "provenance": [{"source_id": "old", "url": "https://example.org/lead"}]}
        self.assertFalse(qualifies_year(lead, [PUBLICATION_YEAR]))
        bibliography = Bibliography(FakeHTTP(json.dumps({"message": CROSSREF})))
        verified = bibliography.lookup_doi("https://doi.org/10.1234/example")
        merged = merge_records(lead, verified)
        self.assertTrue(qualifies_year(merged, [PUBLICATION_YEAR]))
        self.assertTrue(qualifies_year(merged, [REVISION_YEAR]))
        self.assertFalse(qualifies_year(merged, [CREATED_YEAR]))  # created is not a publication year
        self.assertEqual(merged["paper_id"], "lead-1")
        self.assertIn("doi:10.1234/example", merged["aliases"])
        source_ids = {x["source_id"] for x in merged["provenance"]}
        self.assertIn("old", source_ids)
        event = next(e for e in merged["publication_events"] if e["medium"] == "online")
        self.assertTrue(set(event["verification_sources"]).issubset(source_ids))
        self.assertEqual(len([e for e in merged["publication_events"] if e["medium"] == "online"]), 1)

    def test_manual_verification_creates_event_and_preserves_source(self):
        record = {"paper_id": "p", "publication_events": [], "provenance": []}
        updated = verify_publication(record, date=f"{REVISION_YEAR}-06", source={"artifact_ref": "sha256:fixed"}, venue="Journal")
        self.assertTrue(qualifies_year(updated, REVISION_YEAR))
        self.assertEqual(record["publication_events"], [])
        self.assertEqual(updated["provenance"][0]["artifact_ref"], "sha256:fixed")
        with self.assertRaises(ValueError):
            verify_publication(record, date=str(REVISION_YEAR), source={})

    def test_unverified_new_hit_does_not_erase_verified_events_or_read_state(self):
        verified = verify_publication({"paper_id": "p", "title": "Verified title", "read_status": "read"},
                                      date=str(REVISION_YEAR), source={"url": "https://example.org/publisher"})
        merged = merge_records(verified, {"paper_id": "p", "title": "Fuzzy title", "metadata_status": "lead", "read_status": "unread"})
        self.assertEqual(merged["title"], "Verified title")
        self.assertEqual(merged["read_status"], "read")
        self.assertTrue(qualifies_year(merged, REVISION_YEAR))

    def test_doi_conflict_cannot_silently_merge(self):
        with self.assertRaises(ValueError):
            merge_records({"identifiers": {"doi": "10.a/a"}}, {"identifiers": {"doi": "10.a/b"}})

    def test_crossref_cursor_and_date_filter(self):
        client = FakeHTTP(json.dumps({"message": {"items": [CROSSREF], "total-results": 7, "next-cursor": "next:cursor"}}))
        result = Bibliography(client).search("crossref", "oracle complexity", year=REVISION_YEAR, limit=1)
        self.assertEqual(result["next_cursor"], "next:cursor")
        self.assertIn(f"from-pub-date%3A{REVISION_DATE}", client.urls[0])
        self.assertEqual(result["coverage"]["read_papers"], 0)
        self.assertFalse(result["coverage"]["exhaustive"])

    def test_arxiv_preprint_and_revision_are_not_journal_publication(self):
        atom = f'''<feed xmlns="http://www.w3.org/2005/Atom" xmlns:o="http://a9.com/-/spec/opensearch/1.1/">
          <o:totalResults>21</o:totalResults><entry><id>http://arxiv.org/abs/2512.00001v2</id>
          <title>Oracle paper</title><published>{PUBLICATION_DATE}T00:00:00Z</published><updated>{REVISION_DATE}T00:00:00Z</updated>
          <author><name>A Researcher</name></author><summary>Abstract</summary>
          <link href="https://arxiv.org/pdf/2512.00001v2" /></entry></feed>'''
        client = FakeHTTP(atom, "application/atom+xml")
        result = Bibliography(client, arxiv_interval=0).search("arxiv", "oracle complexity", year=PUBLICATION_YEAR, limit=1)
        record = result["records"][0]
        self.assertEqual(result["next_cursor"], "1")
        self.assertTrue(qualifies_year(record, PUBLICATION_YEAR, "preprint"))
        self.assertTrue(qualifies_year(record, REVISION_YEAR, "revision"))
        self.assertFalse(qualifies_year(record, [PUBLICATION_YEAR, REVISION_YEAR]))
        self.assertIn("submittedDate", client.urls[0])
        self.assertNotIn("abstract", record["versions"][0])

    def test_openalex_is_lead_and_api_key_not_in_provenance(self):
        data = {"meta": {"count": 1, "next_cursor": "next"}, "results": [{"id": "https://openalex.org/W1",
                "title": "Paper", "publication_date": date(REVISION_YEAR, 3, 2).isoformat(), "doi": "https://doi.org/10.a/b",
                "abstract_inverted_index": {"two": [1], "one": [0]}, "locations": []}]}
        client = FakeHTTP(json.dumps(data))
        with patch.dict(os.environ, {"OPENALEX_API_KEY": "private-test-key"}):
            result = Bibliography(client).search("openalex", "task", REVISION_YEAR)
        self.assertIn("private-test-key", client.urls[0])
        self.assertNotIn("private-test-key", json.dumps(result))
        self.assertFalse(qualifies_year(result["records"][0], REVISION_YEAR))
        self.assertEqual(result["records"][0]["abstract"], "one two")

    def test_dedup_retains_unknown_title_duplicates(self):
        records = [{"title": "same", "identifiers": {}}, {"title": "same", "identifiers": {}}]
        self.assertEqual(len(deduplicate_records(records)), 2)


class SourceTests(unittest.TestCase):
    def test_html_archived_and_latex_alttext_retained(self):
        content = '<html><head><title>Header</title></head><body><p>Theorem 1</p><math alttext="x^2"><mi>x</mi></math><p>Done</p></body></html>'
        with tempfile.TemporaryDirectory() as tmp:
            source = fetch_source("https://example.org/paper", tmp, client=FakeHTTP(content, "text/html"))
            self.assertIn("$x^2$", source["text"])
            self.assertNotIn("Header", source["text"])
            self.assertEqual(source["metadata"]["read_status"], "fetched_unread")
            self.assertEqual(Path(source["path"]).read_text(), content)
            self.assertEqual(source["content_hash"], hashlib.sha256(content.encode()).hexdigest())
            self.assertEqual(source["metadata"]["math_alttext_preserved"], 1)

    def test_oversized_source_not_truncated_and_private_url_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(DiscoveryError):
                fetch_source("https://example.org/x", tmp, max_bytes=3, client=FakeHTTP("1234", "text/plain"))
        for url in ("file:///etc/passwd", "http://user:pass@example.org/x"):
            with self.assertRaises(DiscoveryError):
                public_url(url)
        with patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("127.0.0.1", 80))]):
            with self.assertRaises(DiscoveryError):
                public_url("http://example.org/x")


if __name__ == "__main__":
    unittest.main()
