#!/usr/bin/env python3
"""Export complete profile PDFs without a browser, TeX installation, or network.

Uses the existing maintenance_nodes / vendor_renderer publication content,
MathJax 3.2.2 from an already installed local mathjax-full npm package, and
PyMuPDF's local HTML/CSS paginator. No dependency is downloaded or installed.
The MathJax version must match visualization/assets/mathjax/source.json.
Native proof/analysis appendices remain literal, as in export_profiles.py.

Example (repeat --setting-id for a batch):
  python data/tools/offline_profile_pdf.py --setting-id SO_ZO_O01 \
    --mathjax-root /local/node_modules/mathjax-full --output /local/exports

Generate the companion Markdown and TeX with export_profiles.py as usual.
This tool writes only profile.pdf plus an offline_pdf_report.json per batch;
--keep-html also keeps the local HTML and SVG images for visual inspection.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from xml.etree import ElementTree

import fitz

import export_profiles
import vendor_renderer
from public_display_rules import legacy_title_errors, validate_content_ledger
from public_render_adapter import maintenance_nodes


ROOT = Path(__file__).resolve().parents[2]
PAGE = fitz.paper_rect("a4")
MARGIN = 20 * 72 / 25.4
BODY_SIZE = 10.2
BODY_WIDTH = PAGE.width - 2 * MARGIN

# The offline Node process has no browser or remote loader. Disable network
# entry points before importing the installed MathJax modules as an additional
# guard; all input and output travel over stdin/stdout and local files.
NODE_RENDERER = r"""
const fs = require('fs');
const path = require('path');
const deny = () => { throw new Error('Network disabled in offline PDF exporter'); };
global.fetch = deny;
global.WebSocket = class { constructor() { deny(); } };
for (const name of ['http', 'https', 'http2', 'net', 'tls', 'dns', 'dgram']) {
  const mod = require(name);
  for (const key of Object.keys(mod)) {
    if (typeof mod[key] === 'function') mod[key] = deny;
  }
  if (mod.promises) {
    for (const key of Object.keys(mod.promises)) {
      if (typeof mod.promises[key] === 'function') mod.promises[key] = deny;
    }
  }
}
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const local = suffix => require(path.join(input.root, 'js', suffix));
const {mathjax} = local('mathjax.js');
const {TeX} = local('input/tex.js');
const {SVG} = local('output/svg.js');
const {liteAdaptor} = local('adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = local('handlers/html.js');
const {AllPackages} = local('input/tex/AllPackages.js');
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const errors = [];
const tex = new TeX({
  packages: AllPackages.filter(x => !['noerrors', 'noundefined'].includes(x)),
  macros: input.macros,
  formatError: (jax, error) => { errors.push(error.message); return jax.formatError(error); }
});
const svg = new SVG({fontCache: 'none'});
const mathDocument = mathjax.document('', {InputJax: tex, OutputJax: svg});
const result = input.formulas.map((formula, index) => {
  errors.length = 0;
  const node = mathDocument.convert(formula.tex, {display: formula.display, em: 10.2, ex: 5.1,
                                            containerWidth: input.width});
  return {index, html: adaptor.outerHTML(node), errors: errors.slice()};
});
fs.writeSync(1, JSON.stringify(result));
"""

MACROS = {
    key: r"\operatorname{" + key + "}"
    for key in ("polylog", "dist", "diam", "rank", "tr", "diag", "prox", "KL", "Var")
}
MACROS.update({"eps": r"\varepsilon", "R": r"\mathbb{R}", "E": r"\mathbb{E}",
               "mathbbm": [r"\mathbf{#1}", 1], "mathds": [r"\mathbf{#1}", 1],
               "llbracket": r"[\![", "rrbracket": r"]\!]"})

CSS = """
body { font-family: serif; font-size: 10.2pt; line-height: 1.36; color: #20313d; }
h1, h2, h3, h4 { font-family: sans-serif; color: #18334c; page-break-after: avoid; }
h1 { font-size: 21pt; margin: 0 0 13pt; }
h2 { font-size: 15pt; margin: 17pt 0 7pt; }
h3 { font-size: 11.8pt; color: #116d73; margin: 12pt 0 5pt; }
h4 { font-size: 10.2pt; margin: 9pt 0 4pt; }
p { margin: 0 0 6pt; orphans: 2; widows: 2; }
a { color: #116d73; text-decoration: underline; }
code { font-family: monospace; font-size: 8.8pt; }
.native { font-family: monospace; font-size: 8.5pt; line-height: 1.35; }
.source { font-size: 8pt; color: #52616d; }
.formula { text-align: center; margin: 9pt 0; page-break-inside: avoid; }
.keep { page-break-inside: avoid; }
.links { font-size: 8.5pt; margin-bottom: 12pt; }
"""


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def soft_breaks(text):
    """Wrap long source identifiers; the underlying source text is unchanged."""
    return re.sub(r"\S{36,}", lambda match: "\u200b".join(
        match.group()[i:i + 24] for i in range(0, len(match.group()), 24)), text)


def normalized_tex(text, display):
    # Reuse the website's narrowly scoped escaping of underscores inside
    # literal TeX text groups. Mathematical subscripts stay mathematical.
    renderer_path = str(ROOT / "visualization" / "src")
    if renderer_path not in sys.path:
        sys.path.insert(0, renderer_path)
    from build_site_public import normalize_math_text
    value = vendor_renderer.display_math(text) if display else vendor_renderer.mathclean(text)
    return normalize_math_text(value)


class HTMLNodes:
    def __init__(self):
        self.formulas = []
        self.links = []

    def math(self, text, display=False):
        index = len(self.formulas)
        self.formulas.append({"tex": normalized_tex(text, display), "display": display,
                              "original": text})
        return "@@ATLAS_MATH_%d@@" % index

    def anchor(self, target, label):
        self.links.append(target)
        return '<a href="' + html.escape(target, quote=True) + '">' + label + '</a>'

    def rich(self, text):
        text = str(text).replace(r"\[", "$$").replace(r"\]", "$$")
        text = text.replace(r"\(", "$").replace(r"\)", "$")
        chunks = re.split(
            r"(\[[^\]\n]+\]\([^\s)]+\)|https?://[^\s<>]+|\*\*[\s\S]*?\*\*|"
            r"`[^`]+`|\$\$[\s\S]*?\$\$|\$(?:\\.|[^$])*?\$)", text)
        output = []
        for chunk in chunks:
            if not chunk:
                continue
            link = re.fullmatch(r"\[([^\]\n]+)\]\(([^\s)]+)\)", chunk)
            if link:
                label = '[' + link[1] + ']' if link[1].isdigit() else link[1]
                output.append(self.anchor(link[2], self.rich(label)))
            elif chunk.startswith(("https://", "http://")):
                output.append(self.anchor(chunk, html.escape(soft_breaks(chunk))))
            elif chunk.startswith("**") and chunk.endswith("**"):
                output.append("<b>" + self.rich(chunk[2:-2]) + "</b>")
            elif chunk.startswith("`") and chunk.endswith("`"):
                output.append("<code>" + html.escape(soft_breaks(chunk[1:-1])) + "</code>")
            elif chunk.startswith("$$") and chunk.endswith("$$"):
                output.append(self.math(chunk[2:-2], True))
            elif chunk.startswith("$") and chunk.endswith("$"):
                output.append(self.math(chunk[1:-1]))
            else:
                output.append(html.escape(soft_breaks(chunk)).replace("\n", "<br/>"))
        return "".join(output)

    def document(self, nodes, setting_id):
        output = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>',
                  '<title>' + html.escape(nodes[0][1]) + '</title></head><body>']
        close_group = -1
        for index, (kind, text) in enumerate(nodes):
            if close_group < index and kind in {"h2", "h3", "h4"}:
                following = index + 1
                while following < len(nodes) and nodes[following][0].startswith("h"):
                    following += 1
                if following < len(nodes) and len(nodes[following][1]) < 1400:
                    output.append('<div class="keep">')
                    close_group = following
            if kind == "literal":
                # Same content policy as the canonical TeX/Markdown exporter:
                # no heuristic math parsing of free-form proof records.
                value = html.escape(soft_breaks(text)).replace("\n", "<br/>")
                output.append('<p class="native" id="node-%d">%s</p>' % (index, value))
            elif kind == "math":
                output.append('<div class="formula" id="node-%d">%s</div>' %
                              (index, self.math(text, True)))
            else:
                tag = kind if re.fullmatch(r"h[1-4]", kind) else "p"
                style = ' class="source"' if text.startswith("Native pointer:") else ""
                output.append('<%s id="node-%d"%s>%s</%s>' %
                              (tag, index, style, self.rich(text), tag))
                if index == 0:
                    output.append('<p class="links">' + ' · '.join([
                        self.anchor('../../settings/' + setting_id + '.html', 'Atlas profile'),
                        self.anchor('profile.tex', 'LaTeX source'),
                        self.anchor('profile.md', 'Markdown source')]) + '</p>')
            if index == close_group:
                output.append('</div>')
        output.append('</body></html>')
        return '\n'.join(output)


def load_profile(path):
    profile = json.loads(path.read_text(encoding="utf-8"))
    classification_path = path.with_name("classification.json")
    classification = json.loads(classification_path.read_text(encoding="utf-8"))
    if classification["profile_sha256"] != sha256(path):
        raise ValueError(str(path) + ": stale classification source revision")
    profile["_classification"] = classification
    if export_profiles.control_characters(profile):
        raise ValueError(str(path) + ": unexpected source control characters")
    nodes, ledger = maintenance_nodes(profile)
    validate_content_ledger(profile, ledger)
    if legacy_title_errors(nodes):
        raise ValueError(str(path) + ": excluded legacy field headings")
    if nodes[0] != ("h1", profile["title"]):
        raise ValueError(str(path) + ": full source title was not retained")
    return profile, nodes, ledger


def render_math(formulas, module_root, node):
    result = subprocess.run([node, "--eval", NODE_RENDERER], input=json.dumps({
        "root": str(module_root), "macros": MACROS, "formulas": formulas,
        "width": BODY_WIDTH}, ensure_ascii=False), capture_output=True, text=True,
        check=False, timeout=180, env={**os.environ, "NODE_OPTIONS": ""})
    if result.returncode:
        raise RuntimeError("Offline MathJax failed: " + result.stderr[-3000:])
    rendered = json.loads(result.stdout)
    errors = [{"index": row["index"], "errors": row["errors"],
               "tex": formulas[row["index"]]["tex"]} for row in rendered if row["errors"]]
    if errors:
        raise ValueError("MathJax rejected formulas: " + json.dumps(errors, ensure_ascii=False))
    return rendered


def replace_formulas(document, formulas, rendered, directory):
    scales = []
    for row in rendered:
        index = row["index"]
        svg = row["html"][row["html"].index("<svg"):row["html"].rindex("</svg>") + 6]
        element = ElementTree.fromstring(svg)
        box = [float(x) for x in element.attrib["viewBox"].split()]
        width, height = box[2] * BODY_SIZE / 1000, box[3] * BODY_SIZE / 1000
        scale = min(1, BODY_WIDTH / max(width, 1))
        scales.append(scale)
        width, height = width * scale, height * scale
        element.set("width", str(width) + "pt")
        element.set("height", str(height) + "pt")
        element.attrib.pop("style", None)
        name = "math-%05d.svg" % index
        # Keep the original SVG namespace prefix-free for local HTML loaders.
        ElementTree.register_namespace("", "http://www.w3.org/2000/svg")
        ElementTree.register_namespace("xlink", "http://www.w3.org/1999/xlink")
        (directory / name).write_bytes(ElementTree.tostring(element, encoding="utf-8"))
        depth = -(box[1] + box[3]) * BODY_SIZE * scale / 1000
        image = ('<img src="%s" width="%.4f" height="%.4f" '
                 'style="width:%.4fpt;height:%.4fpt;vertical-align:%.4fpt" alt="%s"/>') % (
                     name, width, height, width, height, depth,
                     html.escape(formulas[index]["original"], quote=True))
        if formulas[index]["display"]:
            image = '<span style="display:block;text-align:center">' + image + '</span>'
        document = document.replace("@@ATLAS_MATH_%d@@" % index, image)
    if "@@ATLAS_MATH_" in document:
        raise ValueError("Unrendered formula placeholder")
    return document, scales


def vector_math(pdf, assets, formula_count):
    """Replace the paginator's raster SVG previews with the original vectors.

    The only HTML images are the ordered MathJax formulas. MuPDF reports each
    occurrence in document paint order, including repeated formulas. Validate
    the complete count before replacing any resource; use the actual painted
    rectangles so the layout and inline baselines remain exactly unchanged.
    """
    occurrences = [(number, image) for number, page in enumerate(pdf)
                   for image in page.get_image_info(xrefs=True)]
    if len(occurrences) != formula_count:
        raise ValueError("PDF formula image count differs from the source formula count")
    resources = {}
    for number, image in occurrences:
        if not image["xref"]:
            raise ValueError("Cannot safely identify a formula image resource")
        resources.setdefault(image["xref"], number)
    for xref, number in resources.items():
        pdf[number].delete_image(xref)
    for index, (number, image) in enumerate(occurrences):
        with fitz.open(assets / ("math-%05d.svg" % index)) as source:
            with fitz.open("pdf", source.convert_to_pdf()) as vector:
                pdf[number].show_pdf_page(fitz.Rect(image["bbox"]), vector, 0,
                                         keep_proportion=False, overlay=True)
    return len(occurrences)


def write_pdf(document, assets, target, title, setting_id, nodes, expected_links, formula_count):
    frame = fitz.Rect(MARGIN, MARGIN, PAGE.width - MARGIN, PAGE.height - MARGIN)

    def rectangle(index, filled):
        if index > 5000:
            raise ValueError("PDF pagination exceeded its limit")
        return PAGE, frame, None

    moved_headings = set()
    for attempt in range(8):
        positions = []
        story = fitz.Story(document, user_css=CSS, archive=fitz.Archive(str(assets)))
        pdf = story.write_with_links(rectangle, positionfn=positions.append)
        first_positions = {}
        for position in positions:
            if position.open_close & 1 and re.fullmatch(r"node-\d+", position.id or ""):
                first_positions.setdefault(int(position.id[5:]), position)
        orphan_headings = []
        ordered = sorted(first_positions.items())
        for (index, position), (_, following) in zip(ordered, ordered[1:]):
            if position.heading >= 2 and following.page_num > position.page_num:
                orphan_headings.append(index)
        new_breaks = set(orphan_headings) - moved_headings
        if not new_breaks or attempt == 7:
            break
        pdf.close()
        for index in new_breaks:
            document = re.sub(r'(<h[2-4] id="node-' + str(index) + r'")',
                              r'\1 style="page-break-before:always"', document)
        moved_headings.update(new_breaks)
    toc = []
    for position in positions:
        if position.open_close & 1 and position.heading and position.id:
            level = min(position.heading, 3)
            if not toc:
                level = 1
            elif level > toc[-1][0] + 1:
                level = toc[-1][0] + 1
            node_index = int(position.id[5:])
            toc.append([level, nodes[node_index][1], position.page_num])
    if toc:
        pdf.set_toc(toc)
    vector_count = vector_math(pdf, assets, formula_count)
    pdf.set_metadata({"title": title, "subject": setting_id + " complete profile",
                      "author": "Complexity Atlas", "creator": "Complexity Atlas offline exporter",
                      "producer": "MathJax 3.2.2 and PyMuPDF " + fitz.VersionBind})
    for number, page in enumerate(pdf, 1):
        page.insert_text((MARGIN, 30), "COMPLEXITY ATLAS", fontsize=8,
                         fontname="helv", color=(.32, .38, .43))
        page.insert_textbox(fitz.Rect(MARGIN, PAGE.height - 38, PAGE.width - MARGIN,
                                     PAGE.height - 19), str(number), fontsize=8,
                            fontname="helv", align=1, color=(.32, .38, .43))
    pdf.save(target, garbage=4, deflate=True)
    pages = len(pdf)
    pdf.close()
    with fitz.open(target) as checked:
        links = [link for page in checked for link in page.get_links()]
        actual_links = {link.get("uri") or link.get("file") for link in links}
        if set(expected_links) - actual_links:
            raise ValueError("PDF hyperlinks missing: " + repr(set(expected_links) - actual_links))
        empty = [i + 1 for i, page in enumerate(checked) if not page.get_text().strip()]
        if empty:
            raise ValueError("Unexpected empty PDF pages: " + str(empty))
        def normalized(value):
            return re.sub(r"\s+", "", unicodedata.normalize("NFKC", value).replace("\u200b", ""))
        text = normalized(''.join(page.get_text(clip=fitz.Rect(
            25, 40, PAGE.width - 25, PAGE.height - 45)) for page in checked))
        native = [(index, value) for index, (kind, value) in enumerate(nodes) if kind == "literal"]
        missing = [index for index, value in native if normalized(value) not in text]
        if missing:
            raise ValueError("Native source text not found in PDF extraction at nodes: " + repr(missing))
    return {"pages": pages, "pdf_links": len(links),
            "external_citation_links": sum(str(x.get("uri", "")).startswith(("http://", "https://"))
                                            for x in links), "empty_pages": empty,
            "native_literals_verified_in_pdf": len(native),
            "vector_formulas_verified_in_pdf": vector_count,
            "all_source_link_targets_verified_in_pdf": True,
            "remaining_orphan_headings": orphan_headings}


def export_one(path, destination, module_root, node, keep_html=False):
    profile, nodes, ledger = load_profile(path)
    setting_id = profile["setting_id"]
    if not re.fullmatch(r"[A-Za-z0-9_-]+", setting_id):
        raise ValueError("Unsafe setting ID")
    folder = destination / setting_id
    folder.mkdir(parents=True, exist_ok=True)
    builder = HTMLNodes()
    document = builder.document(nodes, setting_id)
    rendered = render_math(builder.formulas, module_root, node)
    with tempfile.TemporaryDirectory(prefix="atlas-offline-") as temporary:
        assets = Path(temporary)
        document, scales = replace_formulas(document, builder.formulas, rendered, assets)
        (assets / "profile.html").write_text(document.replace('</head>', '<style>' + CSS + '</style></head>'),
                                            encoding="utf-8")
        target = folder / "profile.pdf"
        stats = write_pdf(document, assets, target, profile["title"], setting_id, nodes,
                          builder.links, len(rendered))
        if keep_html:
            preview = folder / "offline-preview"
            if preview.exists():
                shutil.rmtree(preview)
            shutil.copytree(assets, preview)
    return {"setting_id": setting_id, "source_sha256": sha256(path),
            "classification_sha256": sha256(path.with_name("classification.json")),
            "pdf": str(target), "pdf_sha256": sha256(target),
            "nodes": len(nodes), "nodes_canonical_sha256": canonical_hash(nodes),
            "native_content_ledger_validated": True,
            "native_appendix_literal_content_retained": True,
            "native_content_roots": ledger["canonical_sections"],
            "formulas": len(rendered), "math_errors": 0,
            "minimum_formula_scale": min(scales, default=1),
            "source_hyperlinks": len(builder.links), **stats}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, default=ROOT / "data" / "settings")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--setting-id", action="append", help="Repeat for a selected batch")
    parser.add_argument("--mathjax-root", type=Path,
                        default=os.environ.get("MATHJAX_NODE_MODULE_ROOT"),
                        help="Already installed local mathjax-full package directory")
    parser.add_argument("--node", default=shutil.which("node"))
    parser.add_argument("--keep-html", action="store_true")
    args = parser.parse_args()
    if not args.node:
        parser.error("Node.js must already be installed; no downloads are performed")
    if not args.mathjax_root:
        parser.error("--mathjax-root must name an already installed local mathjax-full package")
    module_root = args.mathjax_root.resolve()
    package = json.loads((module_root / "package.json").read_text(encoding="utf-8"))
    if package.get("name") != "mathjax-full" or package.get("version") != "3.2.2":
        parser.error("The local mathjax-full package must be version 3.2.2, matching bundled MathJax")
    bundled_mathjax = ROOT / "visualization/assets/mathjax/tex-svg.js"
    if sha256(module_root / "es5/tex-svg-full.js") != sha256(bundled_mathjax):
        parser.error("The local MathJax bundle does not match the repository's vendored bundle")
    selected = set(args.setting_id or [])
    paths = sorted(args.settings.glob("*/profile.json"))
    if selected:
        paths = [path for path in paths if path.parent.name in selected]
        missing = selected - {path.parent.name for path in paths}
        if missing:
            parser.error("Unknown setting IDs: " + ", ".join(sorted(missing)))
    if not paths:
        parser.error("No profile.json files selected")
    args.output.mkdir(parents=True, exist_ok=True)
    report = {"created_utc": datetime.now(timezone.utc).isoformat(),
              "renderer": "offline MathJax SVG + PyMuPDF HTML",
              "network": "disabled; no remote resource loaders or dependency installation",
              "mathjax_version": package["version"], "pymupdf_version": fitz.VersionBind,
              "bundled_mathjax_sha256": sha256(ROOT / "visualization/assets/mathjax/tex-svg.js"),
              "profiles": []}
    for path in paths:
        record = export_one(path, args.output, module_root, args.node, args.keep_html)
        report["profiles"].append(record)
        (args.output / "offline_pdf_report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({key: record[key] for key in
                          ("setting_id", "pages", "formulas", "math_errors", "pdf_links")}), flush=True)


if __name__ == "__main__":
    main()
