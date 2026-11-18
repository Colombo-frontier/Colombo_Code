"""Vendor a pinned MathJax distribution for offline profile rendering."""
from pathlib import Path
import hashlib
import json
import urllib.request

out = Path(__file__).resolve().parent / "assets" / "mathjax"
out.mkdir(parents=True, exist_ok=True)
files = {
    "tex-svg.js": "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg-full.js",
    "LICENSE": "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/LICENSE",
}
manifest = {}
for name, url in files.items():
    with urllib.request.urlopen(url, timeout=45) as response:
        blob = response.read()
    (out / name).write_bytes(blob)
    manifest[name] = {"url": url, "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)}
(out / "source.json").write_text(json.dumps({"package": "mathjax", "version": "3.2.2", "files": manifest}, indent=2) + "\n")
print(json.dumps(manifest, indent=2))
