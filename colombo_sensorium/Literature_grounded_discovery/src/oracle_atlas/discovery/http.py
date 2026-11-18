"""HTTP access to public literature with size, timeout, and cache limits; no arbitrary shell access."""
from __future__ import annotations

import gzip
import hashlib
import io
import ipaddress
import json
import os
import re
import socket
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class DiscoveryError(RuntimeError):
    pass


def public_url(url: str, *, allow_private: bool = False) -> str:
    """Reject local files, userinfo, and private network addresses; apply the same checks to redirects."""
    if not isinstance(url, str) or len(url) > 20000:
        raise DiscoveryError("Invalid URL type or length.")
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
        raise DiscoveryError("Only http(s) literature URLs without userinfo are permitted.")
    if not allow_private:
        try:
            addresses = socket.getaddrinfo(parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80),
                                           type=socket.SOCK_STREAM)
        except OSError as exc:
            raise DiscoveryError("Unable to resolve the literature server address.") from exc
        if not addresses or any(not ipaddress.ip_address(addr[4][0].split("%")[0]).is_global for addr in addresses):
            raise DiscoveryError("Public literature downloads may not access private, loopback, or reserved addresses.")
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))


def display_url(url: str) -> str:
    """Omit known credential parameters from logs/evidence without modifying the network request itself."""
    parsed = urlsplit(url)
    secret = {"api_key", "apikey", "key", "token", "access_token", "secret", "signature", "mailto"}
    query = [(k, "[redacted]" if k.lower() in secret else v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)]
    return urlunsplit((parsed.scheme, parsed.netloc.split("@")[-1], parsed.path, urlencode(query), ""))


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@dataclass(frozen=True)
class HTTPResult:
    url: str
    body: bytes
    headers: dict[str, str]
    fetched_at: str
    cached: bool = False

    @property
    def text(self) -> str:
        match = re.search(r"charset\s*=\s*['\"]?([\w-]+)", self.headers.get("content-type", ""), re.I)
        encoding = match.group(1) if match else "utf-8"
        try:
            return self.body.decode(encoding, errors="replace")
        except LookupError:
            return self.body.decode("utf-8", errors="replace")

    def json(self):
        try:
            return json.loads(self.text)
        except (ValueError, TypeError) as exc:
            raise DiscoveryError("The literature service returned invalid JSON.") from exc


class _Redirects(HTTPRedirectHandler):
    def __init__(self, allow_private):
        self.allow_private = allow_private

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        public_url(newurl, allow_private=self.allow_private)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class HTTPClient:
    def __init__(self, *, cache_dir=None, timeout=30, max_bytes=20_000_000,
                 cache_ttl=3600, user_agent="LiteratureGroundedDiscovery (research metadata)", allow_private=False):
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.timeout = float(timeout)
        self.max_bytes = int(max_bytes)
        self.cache_ttl = cache_ttl
        self.user_agent = user_agent
        self.allow_private = allow_private

    def get(self, url: str, *, refresh=False) -> HTTPResult:
        if self.timeout <= 0 or self.max_bytes <= 0:
            raise DiscoveryError("HTTP timeout and max_bytes must be positive.")
        # Validate URL structure even for cache hits; omit DNS resolution to allow offline review of archived material.
        parsed = urlsplit(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username:
            raise DiscoveryError("Invalid literature URL.")
        key = hashlib.sha256(url.encode()).hexdigest()
        meta_path = self.cache_dir / (key + ".json") if self.cache_dir else None
        raw_path = self.cache_dir / (key + ".bin") if self.cache_dir else None
        if not refresh and meta_path and meta_path.exists() and raw_path.exists():
            try:
                info = json.loads(meta_path.read_text("utf-8"))
                young = self.cache_ttl is None or time.time() - info["fetched_epoch"] <= self.cache_ttl
                if young and raw_path.stat().st_size <= self.max_bytes:
                    body = raw_path.read_bytes()
                    if hashlib.sha256(body).hexdigest() == info["sha256"]:
                        return HTTPResult(info["url"], body, info["headers"], info["fetched_at"], True)
            except (OSError, ValueError, KeyError, TypeError):
                pass  # A corrupted cache cannot serve as evidence; download again without reporting a cache hit.
        checked = public_url(url, allow_private=self.allow_private)
        request = Request(checked, headers={"User-Agent": self.user_agent, "Accept-Encoding": "identity"})
        try:
            with build_opener(_Redirects(self.allow_private)).open(request, timeout=self.timeout) as response:
                headers = {k.lower(): v for k, v in response.headers.items()}
                declared = headers.get("content-length")
                if declared and declared.isdecimal() and int(declared) > self.max_bytes:
                    raise DiscoveryError("The download exceeds max_bytes; increase the file budget if needed.")
                body = response.read(self.max_bytes + 1)
                if len(body) > self.max_bytes:
                    raise DiscoveryError("The download exceeds max_bytes; the source has not been truncated and presented as complete.")
                if headers.get("content-encoding", "").lower() == "gzip":
                    with gzip.GzipFile(fileobj=io.BytesIO(body)) as compressed:
                        body = compressed.read(self.max_bytes + 1)
                    if len(body) > self.max_bytes:
                        raise DiscoveryError("The decompressed literature exceeds max_bytes.")
                final_url = display_url(response.geturl())
        except HTTPError as exc:
            status = exc.code
            exc.close()
            if status == 429:
                raise DiscoveryError("The literature service is rate limiting requests (HTTP 429); preserve the task for later resumption without automatic rapid retries.") from exc
            raise DiscoveryError(f"The literature service returned HTTP {status}.") from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise DiscoveryError(f"Literature download failed: {type(exc).__name__}.") from exc
        now = time.time()
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
        result = HTTPResult(final_url, body, headers, stamp, False)
        if meta_path:
            info = {"url": final_url, "headers": headers, "fetched_at": stamp, "fetched_epoch": now,
                    "sha256": hashlib.sha256(body).hexdigest()}
            atomic_write(raw_path, body)
            atomic_write(meta_path, json.dumps(info, ensure_ascii=False).encode())
        return result
