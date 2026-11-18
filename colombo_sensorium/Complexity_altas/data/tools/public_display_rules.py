"""Public title verification; native scientific prose remains unchanged."""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re

import public_render_adapter as adapter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DISPLAY_RULE = "native-appendices-original-text; legacy-heading-field-title-ban"


def legacy_title_errors(nodes):
    errors, native = [], False
    for index, (kind, text) in enumerate(nodes):
        if kind == "h2" and text in {"Maintenance appendix: Native proof extensions", "Maintenance appendix: Complete native joint analysis"}:
            native = True
        elif kind == "h2" and text == "References":
            native = False
        if native:
            continue
        heading = kind in {"h2", "h3", "h4"} and re.fullmatch(r"(?:[0-9]+[.]\s*)?(?:Coverage(?: of the full domain)?|Information interface)", text.strip(), re.I)
        field = kind == "p" and re.match(r"^\*\*(?:Coverage|Information interface)[.]?\*\*(?:\s|$)", text, re.I)
        if heading or field:
            errors.append({"node_index": index, "kind": kind, "title": text})
    return errors


def validate_content_ledger(profile, ledger):
    """Exact native leaf/root validation, independent of PDF/font availability."""
    expected = {record["pointer"]: record for key in ("proofs", "joint_analysis") if key in profile
                for record in adapter.leaf_records(profile[key], "/" + key)}
    leaves = ledger.get("leaves", [])
    actual = {item["pointer"]: {key: value for key, value in item.items() if key != "route"} for item in leaves}
    if len(actual) != len(leaves) or actual != expected:
        raise ValueError("Native content coverage does not match the original canonical leaves")
    roots = [{"pointer": "/" + key, "canonical_sha256": adapter.canonical_hash(profile[key])}
             for key in ("proofs", "joint_analysis") if key in profile]
    if ledger.get("canonical_sections") != roots:
        raise ValueError("Native content coverage root identity changed")



_TITLE = re.compile(r"(?:[0-9]+[.]\s*)?(?:Coverage(?: of the full domain)?|Information interface)[.:]?", re.I)
_VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class _TitleParser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.stack, self.labels, self.errors = [], [], []
        self.feed(source)
        self.close()
        if any(native for _, native in self.stack):
            self.errors.append({"kind": "unclosed_native_appendix", "title": "Native appendix section is not closed"})
        if self.labels:
            self.errors.append({"kind": "unclosed_legacy_title", "title": "A legacy heading/field label is not closed"})

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        parent_native = bool(self.stack and self.stack[-1][1])
        native = parent_native or (tag == "section" and any(
            values.get(key) == "true" for key in ("data-native-proof-appendix", "data-native-analysis-appendix")))
        depth = len(self.stack)
        if not native and (tag in {"h2", "h3", "h4"} or "field-label" in values.get("class", "").split()):
            self.labels.append({"depth": depth, "kind": tag, "text": []})
        if tag not in _VOID:
            self.stack.append((tag, native))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in _VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        index = next((i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i][0] == tag), None)
        if index is None:
            return
        active = []
        for label in self.labels:
            if label["depth"] >= index:
                text = " ".join("".join(label["text"]).split())
                if _TITLE.fullmatch(text):
                    self.errors.append({"kind": label["kind"], "title": text})
            else:
                active.append(label)
        self.labels = active
        del self.stack[index:]

    def handle_data(self, data):
        for label in self.labels:
            label["text"].append(data)


def html_title_errors(source):
    """Inspect only legacy h2/h3/h4 or .field-label text, not body prose.

    Only a closed section with the explicit native appendix marker exempts its
    contents. Character references are decoded before matching title text.
    """
    return _TitleParser(source).errors


def profile_title_errors(profile):
    """Independently regenerate current adapter nodes from canonical input.

    The integrity ledger is checked against every original proof/joint leaf;
    this grants no source-read, review, approval or compiled-PDF credit.
    """
    nodes, ledger = adapter.maintenance_nodes(profile)
    validate_content_ledger(profile, ledger)
    return legacy_title_errors(nodes)


def display_rule_manifest():
    names = ("public_display_rules.py", "public_render_adapter.py", "export_profiles.py", "vendor_renderer.py", "verify_release_public.py")
    return {"display_rule": DISPLAY_RULE,
            "change": "Global Coverage/Information interface word ban replaced by legacy section/field-title verification.",
            "scope": "Verification policy and current source identities only; no assertion that historical exports used the adapter or received visual review.",
            "native_appendix_original_prose_retained": True, "entity_encoding_bypass": False,
            "pdf_title_basis": "Canonical profile regenerated through current adapter nodes and exact native-content ledger.",
            "pdf_text_checks": "Replacement-glyph and positive Oracle interface checks remain; other PDF machine checks are unchanged.",
            "scientific_validation_credit": False, "tool_read_credit": False, "approval_credit": False,
            "sources": {name: {"path": str((HERE / name).relative_to(ROOT)),
                               "sha256": hashlib.sha256((HERE / name).read_bytes()).hexdigest()} for name in names}}
