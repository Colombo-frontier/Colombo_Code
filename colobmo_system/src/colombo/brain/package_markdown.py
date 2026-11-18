"""Explicit math syntax and reviewed literal formatting for package Markdown.

Bare CommonMark links are deliberately left ambiguous: mathematical-looking
destinations are not a reason to skip dependency checks. Legacy text can only
be made literal through exact, reviewed spans in a source-hash-bound repair.
"""
from __future__ import annotations

from markdown_it import MarkdownIt


def _escaped(text: str, position: int) -> bool:
    backslashes = 0
    while position > 0 and text[position - 1] == "\\":
        position -= 1
        backslashes += 1
    return backslashes % 2 == 1


def _math_inline(state, silent: bool) -> bool:
    start, maximum, text = state.pos, state.posMax, state.src
    if text.startswith(r"\(", start):
        opener, closer = r"\(", r"\)"
    elif text.startswith(r"\[", start):
        opener, closer = r"\[", r"\]"
    elif text[start] == "$":
        if start and text[start - 1] == "$":
            return False
        opener = "$$" if text.startswith("$$", start) else "$"
        closer = opener
        if text.startswith(opener + "$", start):
            return False
    else:
        return False
    content_start = start + len(opener)
    if content_start >= maximum:
        return False
    # Single-dollar math is inline, with conventional whitespace/currency
    # boundaries. Display delimiters may span lines inside one paragraph.
    if opener == "$" and text[content_start].isspace():
        return False
    cursor = content_start
    while True:
        end = text.find(closer, cursor, maximum)
        if end < 0:
            return False  # Unclosed delimiters never hide later links.
        after = end + len(closer)
        cursor = after
        if _escaped(text, end):
            continue
        if opener.startswith("$"):
            if (end > content_start and text[end - 1] == "$") or (
                    after < maximum and text[after] == "$"):
                continue
        if opener == "$":
            if "\n" in text[content_start:end]:
                return False
            if end == content_start or text[end - 1].isspace():
                continue
            if after < maximum and text[after].isdigit():
                continue
        if end == content_start:
            return False
        if not silent:
            token = state.push("math_inline", "math", 0)
            token.content = text[content_start:end]
            token.markup = opener
        state.pos = after
        return True


def _math_block(state, start_line: int, end_line: int, silent: bool) -> bool:
    """Recognize closed display blocks with delimiters on their own lines."""
    if state.is_code_block(start_line):
        return False
    start = state.bMarks[start_line] + state.tShift[start_line]
    opening = state.src[start:state.eMarks[start_line]].strip()
    if opening not in {"$$", r"\["}:
        return False
    closing = "$$" if opening == "$$" else r"\]"
    for line in range(start_line + 1, end_line):
        position = state.bMarks[line] + state.tShift[line]
        maximum = state.eMarks[line]
        if position < maximum and state.sCount[line] < state.blkIndent:
            return False
        if state.is_code_block(line):
            continue
        if state.src[position:maximum].strip() != closing:
            continue
        if not silent:
            token = state.push("math_block", "math", 0)
            token.content = state.getLines(start_line + 1, line,
                                           state.sCount[start_line], True)
            token.markup = opening
            token.map = [start_line, line + 1]
            token.block = True
            state.line = line + 1
        return True
    return False


def create_markdown_parser() -> MarkdownIt:
    """Return a dependency parser with explicit TeX math as opaque tokens.

    This parser discovers links; it does not render or rewrite the source.
    Code blocks/spans retain CommonMark handling. File links must be discovered
    so that the caller can apply its own authorization policy.
    """
    parser = MarkdownIt("commonmark")
    parser.validateLink = lambda value: True
    parser.inline.ruler.before("escape", "package_math", _math_inline)
    parser.block.ruler.before("reference", "package_math", _math_block,
                              {"alt": ["paragraph", "reference", "blockquote", "list"]})
    return parser


def apply_literal_spans(body: str, entry: dict) -> tuple[str, list[dict]]:
    """Format reviewed legacy spans literally in a derived package copy.

    The caller must validate ``source_sha256`` against original file bytes
    before calling this helper. Offsets address the original decoded
    UTF-8-with-optional-BOM body, not a previously transformed copy.
    """
    if not isinstance(body, str) or not isinstance(entry, dict):
        raise ValueError("Literal repair requires text and an object entry")
    reason = entry.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("Literal repair requires a nonempty review reason")
    spans = entry.get("literal_spans")
    if not isinstance(spans, list) or not spans:
        raise ValueError("Literal repair requires nonempty literal_spans")
    checked = []
    for span in spans:
        if not isinstance(span, dict):
            raise ValueError("Literal span must be an object")
        start, end, expected = span.get("start"), span.get("end"), span.get("expected")
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(body):
            raise ValueError("Literal span offsets are invalid")
        if not isinstance(expected, str) or body[start:end] != expected:
            raise ValueError("Literal span does not match the reviewed source text")
        if any(character in expected for character in ("\n", "\r", "`")):
            raise ValueError("Literal span must be one line without backticks")
        # Markdown normalizes surrounding spaces in code spans. Require an
        # exact literal representation instead of silently changing content.
        if expected != expected.strip():
            raise ValueError("Literal span cannot have surrounding whitespace")
        if (start and body[start - 1] == "`") or (end < len(body) and body[end] == "`"):
            raise ValueError("Literal span cannot touch an existing backtick")
        span_reason = span.get("reason", reason)
        if not isinstance(span_reason, str) or not span_reason.strip():
            raise ValueError("Literal span requires a nonempty review reason")
        checked.append({"start": start, "end": end, "expected": expected, "reason": span_reason})
    checked.sort(key=lambda span: span["start"])
    if any(left["end"] >= right["start"] for left, right in zip(checked, checked[1:])):
        raise ValueError("Literal spans must be disjoint and separated")
    audit = [{**span, "replacement": "`" + span["expected"] + "`"}
             for span in checked]
    for span in reversed(audit):
        body = body[:span["start"]] + span["replacement"] + body[span["end"]:]
    return body, audit
