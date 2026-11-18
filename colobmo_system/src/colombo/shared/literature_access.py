"""Public mathematical literature search and source-text retrieval.

Search results are discovery material, never audited mathematical statements.
Serper search and Jina Reader share this entry point with optional arXiv,
direct-download and compatible theorem-search backends. Secrets are loaded
only when the selected provider needs them, outside saved task settings.
"""

from __future__ import annotations

import builtins
from contextvars import ContextVar
import json
import os
from colombo.shared.file_io import Path
from datetime import datetime
from datetime import timezone
from html.parser import HTMLParser
from io import BytesIO
import re
import threading
import time
from urllib.parse import urljoin
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

import requests
from colombo.cell.settings import CONFIG_PATH
from colombo.cell.settings import get_search_enabled
from colombo.cell.settings import get_settings


ARXIV_API = "https://export.arxiv.org/api/query"
SERPER_API = "https://google.serper.dev/search"
JINA_READER_API = "https://r.jina.ai/"
_context = ContextVar("lookup_context", default=None)
_ATOM = "{http://www.w3.org/2005/Atom}"
_ARXIV = "{http://arxiv.org/schemas/atom}"
_OPEN_SEARCH = "{http://a9.com/-/spec/opensearch/1.1/}"
_ARXIV_ID = re.compile(r"(?:\d{4}\.\d{4,5}|[A-Za-z.-]+/\d{7})(?:v\d+)?$")
_request_lock = threading.Lock()
_last_arxiv_request = 0.0


class LookupError(ValueError):
    def __init__(self, kind: str, message: str):
        super().__init__(message)
        self.kind = kind


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _settings() -> dict:
    context = _context.get()
    return context[0] if context is not None else get_settings()


def lookup_with_context(query: str = "", url: str = "", limit: int | None = None,
                        *, settings: dict, search_enabled: bool) -> dict:
    """Internal shared client: isolate Brain settings/policy from Cell state."""
    if type(search_enabled) is not bool:
        raise ValueError("search_enabled must be boolean")
    token = _context.set((settings, search_enabled))
    try:
        return lookup(query=query, url=url, limit=limit)
    finally:
        _context.reset(token)


def _check_search(settings: dict | None = None) -> None:
    """Recheck the current task at each tool call and before each HTTP request."""
    context = _context.get()
    if context is not None:
        if not context[1]:
            raise LookupError("search_disabled", "Brain lookup is disabled by brain.search_enabled in this run's configuration.")
        return
    role = os.environ.get("CELL_ROLE", "prover")
    run_dir = Path(os.environ["CELL_RUN_DIR"]) if os.environ.get("CELL_RUN_DIR") else None
    if not get_search_enabled(role, settings or get_settings(), run_dir):
        raise LookupError("search_disabled", "Search is disabled for this task. Use configure(search_enabled=True, reason=...) to enable lookup; native web search changes require a new model process.")


def _api_key(provider: str) -> str:
    """Read credentials without putting their contents in errors or results."""
    env_name = {"serper": "SERPER_API_KEY", "jina": "JINA_API_KEY"}[provider]
    key = os.environ.get(env_name, "").strip()
    if not key:
        configured = _settings()["network"].get("api_key_file", "")
        keys = {}
        if configured:
            path = Path(configured).expanduser()
            if not path.is_absolute():
                path = CONFIG_PATH.parent / path
            try:
                if path.stat().st_size > 65536:
                    raise LookupError("invalid_credentials_file", "The API key file exceeds 64 KiB.")
                content = path.read_text(encoding="utf-8-sig")
            except FileNotFoundError:
                content = ""
            except (OSError, UnicodeError) as exc:
                raise LookupError("invalid_credentials_file", "The API key file could not be read as UTF-8.") from exc
            pending = None
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = re.split(r"[=:：]", line, maxsplit=1)
                label = re.sub(r"[^a-z]", "", parts[0].lower())
                name = next((p for p in ("serper", "jina")
                             if label in {p, p + "api", p + "key", p + "apikey"}), None)
                if name is not None:
                    # A new label never becomes the previous provider's secret.
                    pending = None
                    value = parts[1].strip() if len(parts) == 2 else ""
                    if not value:
                        pending = name
                        continue
                elif pending is not None:
                    name, value = pending, line
                    pending = None
                else:
                    continue
                if name in keys:
                    raise LookupError("invalid_credentials_file", "Duplicate provider entries in the API key file.")
                keys[name] = value.strip().strip("\"'")
            key = keys.get(provider, "")
    if not key:
        raise LookupError("missing_api_key", f"Set {env_name} or its entry in the configured API key file.")
    if any(ch.isspace() for ch in key) or not key.isascii():
        raise LookupError("invalid_api_key", f"The configured {provider} API key has invalid characters.")
    return key


def _valid_url(url: str) -> str:
    try:
        parsed = urlparse(url)
    except ValueError as exc:
        raise LookupError("invalid_url", "The source URL is malformed.") from exc
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise LookupError("invalid_url", "Only absolute HTTP or HTTPS URLs are supported.")
    if parsed.username or parsed.password:
        raise LookupError("invalid_url", "Do not embed credentials in a source URL.")
    return url


def _request(url: str, *, params=None, payload=None, headers=None) -> dict:
    _check_search()
    _valid_url(url)
    network = _settings()["network"]
    kwargs = {
        "timeout": (network["connect_timeout_seconds"], network["read_timeout_seconds"]), "stream": True,
        "headers": {"User-Agent": "ResearchCell/1.0 (mathematical literature lookup)",
                    "Accept": "application/atom+xml, application/pdf, text/html, text/plain, application/json;q=0.8, */*;q=0.1"},
    }
    if headers:
        kwargs["headers"].update(headers)
        kwargs["allow_redirects"] = False
    method = requests.get if payload is None else requests.post
    if payload is None:
        kwargs["params"] = params
    else:
        kwargs["json"] = payload
    with method(url, **kwargs) as response:
        if headers and 300 <= response.status_code < 400:
            raise LookupError("provider_redirect", "The API provider redirected the request; credentials were not forwarded.")
        response.raise_for_status()
        _valid_url(response.url)
        data = bytearray()
        truncated = False
        for chunk in response.iter_content(chunk_size=network["chunk_bytes"]):
            if not chunk:
                continue
            remaining = network["max_download_bytes"] - len(data)
            if len(chunk) > remaining:
                data.extend(chunk[:remaining])
                truncated = True
                break
            data.extend(chunk)
        return {
            "data": bytes(data), "url": response.url,
            "content_type": response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower(),
            "encoding": response.encoding,
            "last_modified": response.headers.get("Last-Modified"),
            "etag": response.headers.get("ETag"),
            "download_truncated": truncated, "retrieved_at": _now(),
        }


def _pace_arxiv() -> None:
    # Pacing is shared by requests in this MCP process.
    global _last_arxiv_request
    with _request_lock:
        wait = _settings()["network"]["arxiv_interval_seconds"] - (time.monotonic() - _last_arxiv_request)
        if wait > 0:
            time.sleep(wait)
        _last_arxiv_request = time.monotonic()


def _text(element, tag: str) -> str:
    return " ".join((element.findtext(tag) or "").split())


def _https_arxiv(url: str) -> str:
    parsed = urlparse(url)
    return "https:" + url[5:] if parsed.scheme == "http" and parsed.hostname in {"arxiv.org", "export.arxiv.org"} else url


def _arxiv_search(query: str, limit: int) -> dict:
    _pace_arxiv()
    response = _request(ARXIV_API, params={
        "search_query": query, "start": 0, "max_results": limit,
        "sortBy": "relevance", "sortOrder": "descending",
    })
    if response["download_truncated"]:
        raise LookupError("response_too_large", "The arXiv feed exceeded the download limit and was not parsed.")
    try:
        feed = ET.fromstring(response["data"])
    except ET.ParseError as exc:
        raise LookupError("invalid_response", "arXiv returned invalid Atom XML.") from exc
    if feed.tag != _ATOM + "feed":
        raise LookupError("invalid_response", "arXiv did not return an Atom feed.")
    results = []
    for entry in feed.findall(_ATOM + "entry"):
        entry_id = _text(entry, _ATOM + "id")
        if "/api/errors" in entry_id or _text(entry, _ATOM + "title").lower() == "error":
            raise LookupError("arxiv_query_error", _text(entry, _ATOM + "summary") or "arXiv rejected the query.")
        identifier = entry_id.split("/abs/", 1)[-1]
        if not _ARXIV_ID.fullmatch(identifier):
            continue
        url = f"https://arxiv.org/abs/{identifier}"
        pdf_url = next((link.get("href", "") for link in entry.findall(_ATOM + "link")
                        if link.get("type") == "application/pdf" or link.get("title") == "pdf"), "")
        abstract = _text(entry, _ATOM + "summary")
        results.append({
            "title": _text(entry, _ATOM + "title"), "url": url,
            "arxiv_id": identifier, "pdf_url": _https_arxiv(pdf_url),
            "authors": [_text(author, _ATOM + "name") for author in entry.findall(_ATOM + "author")],
            "published": _text(entry, _ATOM + "published"), "updated": _text(entry, _ATOM + "updated"),
            "doi": _text(entry, _ARXIV + "doi"),
            "categories": [node.get("term", "") for node in entry.findall(_ATOM + "category")],
            "abstract": abstract, "truncated": False,
            "content_kind": "abstract", "theorem": "", "theorem_text_verified": False,
        })
    total_text = feed.findtext(_OPEN_SEARCH + "totalResults")
    total = int(total_text) if total_text and total_text.isdigit() else None
    return {
        "provider": "arxiv", "results": results[:limit], "total_results": total,
        "has_more": total > len(results[:limit]) if total is not None else None,
        "source_url": response["url"], "retrieved_at": response["retrieved_at"],
        "warnings": ["These are paper metadata and abstracts, not theorem text. Read the original paper and check definitions and hypotheses before using a result."],
    }


def _provider_json(response: dict, provider: str) -> dict:
    if response["download_truncated"]:
        raise LookupError("response_too_large", f"The {provider} response exceeded the download limit.")
    try:
        value = json.loads(response["data"])
    except (ValueError, UnicodeError) as exc:
        raise LookupError("invalid_response", f"{provider} returned invalid JSON.") from exc
    if not isinstance(value, dict):
        raise LookupError("invalid_response", f"{provider} did not return a JSON object.")
    return value


def _serper_search(query: str, limit: int) -> dict:
    response = _request(SERPER_API, payload={"q": query, "num": limit},
                        headers={"X-API-KEY": _api_key("serper"), "Accept": "application/json"})
    value = _provider_json(response, "Serper")
    items = value.get("organic")
    if not isinstance(items, list):
        raise LookupError("invalid_response", "Serper did not return an organic results list.")
    results = []
    for item in items[:limit]:
        if not isinstance(item, dict) or not isinstance(item.get("link"), str):
            raise LookupError("invalid_response", "Serper returned an invalid result entry.")
        source_url = _valid_url(item["link"])
        title, snippet = item.get("title", ""), item.get("snippet", "")
        if not isinstance(title, str) or not isinstance(snippet, str):
            raise LookupError("invalid_response", "Serper returned invalid result text.")
        results.append({"title": title, "url": source_url, "snippet": snippet,
                        "content_kind": "search_snippet", "truncated": False,
                        "theorem": "", "theorem_text_verified": False,
                        "source_checked": False})
    return {"provider": "serper", "results": results, "source_url": SERPER_API,
            "retrieved_at": response["retrieved_at"],
            "warnings": ["Search snippets are discovery material. Read the original source and check its assumptions before using a result."]}


def _jina_read(url: str) -> dict:
    _valid_url(url)
    response = _request(JINA_READER_API, payload={"url": url}, headers={
        "Authorization": "Bearer " + _api_key("jina"),
        "Accept": "application/json", "X-Respond-With": "markdown"})
    value = _provider_json(response, "Jina Reader")
    data = value.get("data")
    if not isinstance(data, dict) or value.get("code", 200) != 200:
        raise LookupError("invalid_response", "Jina Reader did not return a successful source response.")
    content, title = data.get("content"), data.get("title", "")
    source_url = data.get("url", url)
    if not isinstance(content, str) or not isinstance(title, str) or not isinstance(source_url, str):
        raise LookupError("invalid_response", "Jina Reader returned invalid source fields.")
    _valid_url(source_url)
    if not content.strip():
        raise LookupError("no_extractable_text", "Jina Reader returned no usable source text.")
    parsed = urlparse(source_url)
    kind = "abstract_page" if parsed.hostname in {"arxiv.org", "export.arxiv.org"} and parsed.path.startswith("/abs/") else "reader_markdown"
    item = {"title": title, "url": source_url, "requested_url": url,
            "text": content, "content_type": "text/markdown", "content_kind": kind,
            "returned_characters": len(content), "downloaded_bytes": len(response["data"]),
            "truncated": False, "truncation_reasons": [],
            "retrieved_at": response["retrieved_at"], "theorem": "",
            "theorem_text_verified": False,
            "read_coverage": "provider_extracted_text"}
    return {"provider": "jina_reader", "results": [item],
            "retrieved_at": response["retrieved_at"],
            "warnings": ["Reader output is extracted source text, not an audited theorem. Check assumptions, notation and the original source; extraction does not certify full-document coverage."]}


def _configured_search(endpoint: str, query: str, limit: int) -> dict:
    import json

    response = _request(endpoint, payload={
        "query": query, "num_results": limit,
        "task": "Retrieve relevant mathematical theorems, lemmas, and definitions with original paper identifiers and locations.",
    })
    if response["download_truncated"]:
        raise LookupError("response_too_large", "The configured search response exceeded the download limit.")
    try:
        items = json.loads(response["data"])
    except (ValueError, UnicodeError) as exc:
        raise LookupError("invalid_response", "The configured theorem search returned invalid JSON.") from exc
    if not isinstance(items, list):
        raise LookupError("invalid_response", "The configured theorem search must return a JSON list.")
    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        identifier = item.get("arxiv_id", "")
        identifier = identifier if isinstance(identifier, str) else ""
        if "/abs/" in identifier:
            identifier = identifier.split("/abs/", 1)[1]
        theorem = item.get("theorem", "")
        theorem = theorem if isinstance(theorem, str) else ""
        source = f"https://arxiv.org/abs/{identifier}" if _ARXIV_ID.fullmatch(identifier) else ""
        if not source and isinstance(item.get("url"), str):
            try:
                source = _valid_url(item["url"])
            except LookupError:
                pass
        results.append({
            "title": str(item.get("title", "")), "arxiv_id": identifier,
            "url": source, "theorem_id": str(item.get("theorem_id", "")),
            "theorem": theorem, "truncated": False,
            "content_kind": "unverified_theorem_excerpt" if theorem else "search_metadata",
            "theorem_text_verified": False, "source_checked": False,
        })
    return {
        "provider": "configured_theorem_search", "results": results[:limit],
        "source_url": response["url"], "retrieved_at": response["retrieved_at"],
        "warnings": ["Theorem excerpts are supplied by the configured search service. They have not been compared with the original paper or audited for applicability."],
    }


class _HTMLText(HTMLParser):
    """Extract inert HTML text and source metadata, preserving common math text."""
    _skip = {"script", "style", "noscript", "nav", "header", "footer", "svg"}
    _blocks = {"p", "div", "section", "article", "main", "br", "li", "h1", "h2", "h3", "h4", "tr"}
    _void = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, base: str):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.max_links = _settings()["network"]["html_max_links"]
        self.parts, self.title_parts, self.links = [], [], []
        self.metadata = {}
        self.skip_stack = []
        self.in_title = False
        self.in_math_script = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.skip_stack:
            if tag not in self._void:
                self.skip_stack.append(tag)
            return
        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key and attrs.get("content"):
                self.metadata.setdefault(key.lower(), []).append(attrs["content"])
        elif tag == "link" and attrs.get("rel") == "canonical":
            self.metadata["canonical_url"] = [urljoin(self.base, attrs.get("href", ""))]
        elif tag == "title":
            self.in_title = True
        elif tag == "a" and attrs.get("href") and len(self.links) < self.max_links:
            href = urljoin(self.base, attrs["href"])
            if urlparse(href).scheme in {"http", "https"} and href not in self.links:
                self.links.append(href)
        if tag == "script" and attrs.get("type", "").startswith("math/tex"):
            self.in_math_script = True
            self.parts.append(" ")
        elif tag in self._skip:
            self.skip_stack.append(tag)
        elif tag == "math" and (attrs.get("alttext") or attrs.get("aria-label")):
            self.parts.append(" " + (attrs.get("alttext") or attrs["aria-label"]) + " ")
            self.skip_stack.append(tag)
        elif tag == "img" and attrs.get("alt"):
            self.parts.append(" " + attrs["alt"] + " ")
        elif tag in self._blocks:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if self.skip_stack:
            if tag in self.skip_stack:
                index = len(self.skip_stack) - 1 - self.skip_stack[::-1].index(tag)
                del self.skip_stack[index:]
            return
        if tag == "title":
            self.in_title = False
        if tag == "script":
            self.in_math_script = False
            self.parts.append(" ")
        if tag in self._blocks:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_stack:
            return
        if self.in_title:
            self.title_parts.append(data)
        else:
            self.parts.append(data)

    def result(self) -> dict:
        text = re.sub(r"[ \t\r\f\v]+", " ", "".join(self.parts))
        text = re.sub(r"\n[ \t]*\n+", "\n\n", text).strip()
        return {
            "text": text, "title": " ".join("".join(self.title_parts).split()),
            "metadata": self.metadata, "links": self.links,
        }


def _pdf_text(data: bytes) -> dict:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise LookupError("missing_dependency", "Install pypdf to read PDF source text, or use the paper's HTML version.") from exc
    try:
        reader = PdfReader(BytesIO(data))
        if reader.is_encrypted and not reader.decrypt(""):
            raise LookupError("encrypted_pdf", "The source PDF requires a password.")
        page_count = len(reader.pages)
        parts = []
        pages_read = 0
        for page_number in range(page_count):
            parts.append(f"[Page {page_number + 1}]\n" + (reader.pages[page_number].extract_text() or ""))
            pages_read += 1
        text = "\n\n".join(parts)
        metadata = reader.metadata or {}
        return {"text": text, "title": str(metadata.get("/Title", "")),
                "metadata": {"author": str(metadata.get("/Author", ""))},
                "page_count": page_count, "pages_read": pages_read,
                "pages_truncated": pages_read < page_count,
                "text_available": any(part.split("\n", 1)[-1].strip() for part in parts)}
    except LookupError:
        raise
    except Exception as exc:
        raise LookupError("pdf_extraction_failed", f"Could not extract text from the source PDF ({type(exc).__name__}).") from exc


def _read_source(url: str) -> dict:
    response = _request(url)
    data = response["data"]
    content_type = response["content_type"]
    warnings = ["Retrieved source text is not an audited theorem. Check the original definitions, hypotheses, and surrounding argument."]
    if content_type == "application/pdf" or data.startswith(b"%PDF-"):
        if response["download_truncated"]:
            raise LookupError("response_too_large", "The PDF exceeded the download limit. A partial PDF cannot be reliably parsed; try its HTML version.")
        extracted = _pdf_text(data)
        if not extracted.pop("text_available"):
            raise LookupError("no_extractable_text", "The PDF has no extractable text in the inspected pages; OCR or manual reading is required.")
        kind = "pdf_text"
        warnings.append("PDF extraction can lose mathematical notation and layout; page labels are provided for checking.")
    else:
        encoding = response.get("encoding")
        # Requests defaults text/html without a charset to Latin-1, while modern
        # mathematics pages usually use UTF-8. Prefer an actual UTF-8 decode.
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            try:
                text = data.decode(encoding or "utf-8", errors="replace")
            except builtins.LookupError:
                text = data.decode("utf-8", errors="replace")
        if content_type in {"text/html", "application/xhtml+xml"} or text.lstrip().lower().startswith(("<!doctype html", "<html")):
            parser = _HTMLText(response["url"])
            parser.feed(text)
            extracted = parser.result()
            parsed_url = urlparse(response["url"])
            kind = "abstract_page" if parsed_url.hostname in {"arxiv.org", "export.arxiv.org"} and parsed_url.path.startswith("/abs/") else "html_text"
            warnings.append("HTML text extraction may omit rendered formulas or dynamic content; common MathML alternative text is retained.")
        elif content_type.startswith("text/") or content_type in {"application/json", "application/xml", "application/atom+xml", "application/x-tex", "application/x-latex"}:
            extracted = {"text": text, "title": "", "metadata": {}}
            kind = "source_text"
        else:
            raise LookupError("unsupported_content_type", f"Unsupported source content type: {content_type or 'unknown'}.")
    text = extracted.pop("text")
    reasons = []
    if response["download_truncated"]:
        reasons.append("download_byte_limit")
    if not text.strip():
        raise LookupError("no_extractable_text", "The source returned no usable text.")
    item = {
        **extracted, "url": response["url"], "requested_url": url,
        "content_type": content_type, "content_kind": kind,
        "text": text, "returned_characters": len(text),
        "downloaded_bytes": len(data), "truncated": bool(reasons), "truncation_reasons": reasons,
        "last_modified": response["last_modified"], "etag": response["etag"],
        "retrieved_at": response["retrieved_at"], "theorem": "", "theorem_text_verified": False,
    }
    return {"provider": "url", "results": [item], "retrieved_at": response["retrieved_at"], "warnings": warnings}


def lookup(query: str = "", url: str = "", limit: int | None = None) -> dict:
    """Search papers, or read one URL (URL takes precedence when both supplied).

    Return the selected reader's extracted source text, with actual provenance.
    limit controls search result count only; omission uses config.toml's search_results.
    It does not limit source text.
    Expected network/format failures return ok=False with a typed error, never
    an apparently successful empty theorem list. This function launches no LLM.
    """
    base = {"ok": False, "mode": "read" if url else "search", "query": query,
            "requested_url": url, "retrieved_at": _now(), "results": [], "count": 0, "warnings": []}
    settings = _settings()
    retrieval, network = settings["retrieval"], settings["network"]
    if limit is None:
        limit = retrieval["search_results"]
    try:
        _check_search(settings)
        if not isinstance(query, str) or not isinstance(url, str):
            raise LookupError("invalid_input", "query and url must be strings.")
        if type(limit) is not int or not 1 <= limit <= retrieval["max_search_results"]:
            raise LookupError("invalid_input", f"limit must be an integer between 1 and {retrieval['max_search_results']}.")
        query, url = query.strip(), url.strip()
        if url:
            result = _jina_read(url) if network["reader_provider"] == "jina" else _read_source(url)
        else:
            if not query or len(query) > network["query_max_chars"]:
                raise LookupError("invalid_input", f"Provide a non-empty query of at most {network['query_max_chars']} characters, or a source URL.")
            endpoint = network["theorem_search_url"].strip()
            if endpoint:
                try:
                    result = _configured_search(endpoint, query, limit)
                except (requests.RequestException, LookupError) as exc:
                    result = _arxiv_search(query, limit)
                    result["warnings"].insert(0, f"Configured theorem search failed ({type(exc).__name__}); returning arXiv metadata instead.")
            elif network["search_provider"] == "serper":
                result = _serper_search(query, limit)
            else:
                result = _arxiv_search(query, limit)
        return {**base, **result, "ok": True, "count": len(result["results"])}
    except LookupError as exc:
        return {**base, "error": {"kind": exc.kind, "message": str(exc)}}
    except requests.Timeout:
        return {**base, "error": {"kind": "network_timeout", "message": "The source request timed out; no mathematical conclusion can be drawn."}}
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else None
        return {**base, "error": {"kind": "http_error", "status_code": status, "message": "The source returned an HTTP error."}}
    except requests.RequestException as exc:
        return {**base, "error": {"kind": "network_error", "message": f"The source request failed ({type(exc).__name__}); check network access and the source URL."}}
