"""Archive original sources and extract paginated text. Webpages, abstracts, and search results are not automatically promoted to a higher evidential status."""
from __future__ import annotations

import hashlib
import io
import json
import re
from html.parser import HTMLParser
from pathlib import Path

from .http import DiscoveryError, HTTPClient, atomic_write, display_url


class ArticleText(HTMLParser):
    """Preserve arXiv/LaTeXML math alttext; retain the original for verification when formulas are incomplete."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0
        self.math_skip = 0
        self.math_count = 0
        self.math_alt_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style", "nav", "head", "footer"):
            self.skip += 1
        if self.skip:
            return
        if self.math_skip:
            if tag == "math":
                self.math_skip += 1
            return
        if tag == "math":
            self.math_count += 1
            latex = attrs.get("alttext") or attrs.get("data-tex")
            if latex:
                self.parts.append(" $" + latex.strip() + "$ ")
                self.math_alt_count += 1
                self.math_skip = 1
        if tag in ("p", "div", "section", "h1", "h2", "h3", "h4", "li", "br", "tr"):
            self.parts.append("\n")
        if tag == "img" and attrs.get("alt"):
            self.parts.append(" [image: " + attrs["alt"] + "] ")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav", "head", "footer"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if self.math_skip:
            if tag == "math":
                self.math_skip -= 1
            return
        if tag in ("p", "div", "section", "h1", "h2", "h3", "h4", "li", "tr"):
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip and not self.math_skip:
            self.parts.append(data)

    def get_text(self):
        lines = [re.sub(r"[ \t\r\f]+", " ", line).strip() for line in "".join(self.parts).split("\n")]
        return "\n".join(line for line in lines if line)


def html_text(content: str) -> str:
    parser = ArticleText()
    parser.feed(content)
    return parser.get_text()


def fetch_source(url, cache_dir, timeout=30, max_bytes=20_000_000, *, refresh=False, client=None):
    """Return the archive path, text, and minimal locators; the caller stores the text in the object store and passes only its ref.

    client is used only for offline testing or HTTP transport substitution. Missing PDF dependencies or text extraction failures are reported explicitly;
    a successful download never establishes that mathematical facts have been verified, and site authentication is never bypassed.
    """
    cache_dir = Path(cache_dir).resolve()
    client = client or HTTPClient(cache_dir=cache_dir / "http", timeout=timeout,
                                  max_bytes=max_bytes, cache_ttl=None)
    response = client.get(url, refresh=refresh)
    raw = response.body
    if len(raw) > max_bytes:
        raise DiscoveryError("The source exceeds max_bytes.")
    digest = hashlib.sha256(raw).hexdigest()
    content_type = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
    metadata = {"fetched_at": response.fetched_at, "cached": response.cached,
                "final_url": display_url(response.url), "read_status": "fetched_unread",
                "source_version": digest, "locators": []}
    is_pdf = raw.startswith(b"%PDF-") or content_type == "application/pdf"
    if is_pdf:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise DiscoveryError('PDF extraction requires pip install ".[pdf]"; the original has not yet been read as text.') from exc
        try:
            reader = PdfReader(io.BytesIO(raw))
            pages, position = [], 0
            for number, page in enumerate(reader.pages, 1):
                text = page.extract_text() or ""
                pages.append(text)
                metadata["locators"].append({"page": number, "start": position, "end": position + len(text)})
                position += len(text) + 2
            text = "\n\n".join(pages)
        except Exception as exc:
            raise DiscoveryError(f"PDF text extraction failed: {type(exc).__name__}; obtain HTML or the original for verification.") from exc
        extension, content_type = ".pdf", "application/pdf"
        metadata.update({"extraction": "pdf_text", "page_count": len(pages), "needs_ocr": not text.strip(),
                         "limitations": ["PDF text extraction may lose subscripts, superscripts, layout, and formulas; verify critical formulas against the original."]})
    elif content_type in ("text/html", "application/xhtml+xml") or raw.lstrip()[:100].lower().startswith((b"<!doctype html", b"<html")):
        parser = ArticleText()
        parser.feed(response.text)
        text, extension = parser.get_text(), ".html"
        metadata.update({"extraction": "html_text", "math_elements": parser.math_count,
                         "math_alttext_preserved": parser.math_alt_count,
                         "limitations": ["Existing math alttext is preserved; verify other formulas or images against the archived webpage."]})
    elif content_type.startswith("text/") or content_type in ("application/xml", "application/atom+xml", ""):
        text, extension = response.text, ".txt"
        metadata["extraction"] = "text"
    else:
        raise DiscoveryError(f"Source type {content_type!r} is not currently supported; provide HTML/PDF/text.")
    original = cache_dir / "originals" / (digest + extension)
    text_path = cache_dir / "text" / (digest + ".txt")
    atomic_write(original, raw)
    atomic_write(text_path, text.encode("utf-8"))
    metadata.update({"text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                     "text_path": str(text_path), "characters": len(text)})
    atomic_write(cache_dir / "metadata" / (digest + ".json"), json.dumps(metadata, ensure_ascii=False).encode())
    return {"url": display_url(url), "content_hash": digest, "content_type": content_type,
            "text": text, "path": str(original), "metadata": metadata}
