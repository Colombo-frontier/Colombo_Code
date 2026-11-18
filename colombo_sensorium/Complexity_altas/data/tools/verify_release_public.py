#!/usr/bin/env python3
"""Check the actual static delivery, PDF links, scope bindings and file hashes."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote, urlsplit

from public_display_rules import html_title_errors, profile_title_errors, display_rule_manifest

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "visualization/dist"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.links = []
        self.comparisons = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append((tag, attrs[name]))
        if attrs.get("data-comparison-ids"):
            self.comparisons.append(attrs["data-comparison-ids"].split(","))

    def handle_data(self, data):
        self.text.append(data)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    import sys
    sys.path.insert(0, str(ROOT / "visualization/src"))
    from public_build_root import checked_root
    checked_root(ROOT, ROOT)
    from pypdf import PdfReader
    errors, records = [], []
    catalog = json.loads((ROOT / "data/derived/catalog.json").read_text())
    sources = json.loads((ROOT / 'data/derived/catalog_sources.json').read_text())
    if sources['catalog_sha256'] != digest(ROOT / 'data/derived/catalog.json'):
        errors.append('Catalog integrity binding is stale')
    if set(sources['settings']) != {row['id'] for row in catalog['profiles']}:
        errors.append('Native integrity inventory differs from the catalog')
    for sid, source in sources['settings'].items():
        for name, expected_hash in source['files'].items():
            if digest(ROOT / 'data/settings' / sid / name) != expected_hash:
                errors.append(f'Native integrity binding is stale: {sid}/{name}')
    local_links_checked = 0
    top_level = [DIST / "index.html"]
    if (DIST / "graph.html").is_file():
        top_level.append(DIST / "graph.html")
    for path in [*top_level, *sorted((DIST / "settings").glob("*.html"))]:
        source = path.read_text()
        if html_title_errors(source):
            errors.append(f"Excluded display label in {path.name}")
        page = Page(source)
        for tag, href in page.links:
            target = urlsplit(href)
            if target.scheme in ("file", "javascript") or target.hostname in ("localhost", "127.0.0.1", "::1"):
                errors.append(f"Non-public link scheme/host in {path.name}")
            if target.scheme in ("http", "https"):
                if tag in ("script", "link"):
                    errors.append(f"Remote runtime dependency in {path.name}: {href}")
                continue
            if target.scheme or not target.path:
                continue
            resolved = (path.parent / unquote(target.path)).resolve()
            if not resolved.is_relative_to(ROOT):
                errors.append(f"Local target escapes this Atlas in {path.name}")
            local_links_checked += 1
            if not resolved.is_file():
                errors.append(f"Broken local target {path.name}: {href}")

    for item in catalog["profiles"]:
        sid = item["id"]
        profile_path = ROOT / "data/settings" / sid / "profile.json"
        profile = json.loads(profile_path.read_text())
        if profile_title_errors(profile):
            errors.append(f"Excluded legacy section/field title in adapter nodes: {sid}")
        page = Page((DIST / "settings" / (sid + ".html")).read_text())
        visible_source = " ".join(" ".join(page.text).split())
        if " ".join(profile["title"].split()) not in visible_source:
            errors.append(f"Changed or missing full title: {sid}")
        expected = [r["comparison_ids"] for r in profile["bracket_rows"]]
        if page.comparisons != expected:
            errors.append(f"Changed or missing regional comparison bindings: {sid}")
        positions = [visible_source.find(x) for x in (
            "Setting specification", "Notation and parameters", "Complexity bracket", "Evidence")]
        if min(positions) < 0 or positions != sorted(positions):
            errors.append(f"Incorrect section order: {sid}")
        for reference in profile["references"]:
            if reference["url"] not in [url for _, url in page.links]:
                errors.append(f"Missing article hyperlink: {sid}/{reference['id']}")
        pdf = DIST / "downloads" / sid / "profile.pdf"
        tex = pdf.with_suffix(".tex")
        if not tex.is_file() or not pdf.with_suffix('.md').is_file():
            errors.append(f'Missing scientific text export: {sid}')
        reader = PdfReader(str(pdf), strict=True)
        uris = []
        for p in reader.pages:
            for annotation in p.get("/Annots", []):
                action = annotation.get_object().get("/A", {})
                if action.get("/URI"):
                    uris.append(str(action["/URI"]))
        for reference in profile["references"]:
            if reference["url"] not in uris:
                errors.append(f"Missing actual PDF hyperlink: {sid}/{reference['id']}")
        text_tool = shutil.which("pdftotext")
        if not text_tool:
            raise RuntimeError("pdftotext is required for PDF text QA")
        pdf_text = subprocess.check_output([text_tool, "-layout", str(pdf), "-"], text=True)
        if re.search(r"\ufffd", pdf_text, re.I):
            errors.append(f"Excluded label or replacement glyph in PDF: {sid}")
        if "Oracle interface" not in pdf_text:
            errors.append(f"Oracle interface absent from PDF: {sid}")
        records.append({"id": sid, "pdf_pages": len(reader.pages), "pdf_uri_annotations": len(uris),
                        "displayed_regimes": len(expected),
                        "comparisons": sum(map(len, expected)),
                        "pdf_sha256": digest(pdf), "tex_sha256": digest(tex)})
    report = {"passed": not errors, "profile_count": len(records),
              "pdf_pages": sum(r["pdf_pages"] for r in records),
              "local_links_checked": local_links_checked,
              "displayed_regimes": sum(r["displayed_regimes"] for r in records),
              "comparisons": sum(r["comparisons"] for r in records),
              "profiles": records, "errors": errors}
    report["display_rule"] = display_rule_manifest()
    print(json.dumps({k: v for k, v in report.items() if k != "profiles"}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
