from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from colombo.brain.package_markdown import apply_literal_spans, create_markdown_parser


def links(body):
    parser, env = create_markdown_parser(), {}
    tokens = parser.parse(body, env)
    found = []

    def visit(rows):
        for token in rows:
            if token.type == "link_open":
                found.append(token.attrGet("href"))
            if token.type == "image":
                found.append(token.attrGet("src"))
            if token.children:
                visit(token.children)
    visit(tokens)
    found.extend(ref["href"] for ref in env.get("references", {}).values())
    return found


class PackageMarkdownTests(unittest.TestCase):
    def test_explicit_inline_math_is_opaque_and_outside_links_remain(self):
        for opening, closing in [("$", "$"), ("$$", "$$"), (r"\(", r"\)"), (r"\[", r"\]")]:
            with self.subTest(opening=opening):
                body = f"Before [first](first.md) {opening}[2(d+1)/d^2](t^2+t){closing} after [last](last.md)."
                self.assertEqual(links(body), ["first.md", "last.md"])

    def test_display_blocks_hide_reference_definitions_and_preserve_outside(self):
        for opening, closing in [("$$", "$$"), (r"\[", r"\]")]:
            with self.subTest(opening=opening):
                body = f"{opening}\n[x](math-only.md)\n\n[inside]: hidden.md\n{closing}\n\n[outside][p]\n\n[p]: real.md\n"
                self.assertEqual(links(body), ["real.md", "real.md"])

    def test_math_inside_code_does_not_open_a_math_region(self):
        body = "`$` [first](first.md) `$`\n\n```md\n$$\n[x](hidden.md)\n```\n\n[last](last.md)\n"
        self.assertEqual(links(body), ["first.md", "last.md"])

    def test_code_looking_text_inside_math_stays_opaque(self):
        self.assertEqual(links("$`[x](hidden.md)`$ [p](real.md)"), ["real.md"])

    def test_nested_display_math_and_indented_code_respect_container_boundaries(self):
        for body in ["> $$\n> [x](hidden.md)\n> $$\n\n[real](real.md)",
                     "- item\n\n  $$\n  [x](hidden.md)\n  $$\n\n[real](real.md)",
                     "    $$\n    [x](hidden.md)\n    $$\n\n[real](real.md)"]:
            with self.subTest(body=body):
                self.assertEqual(links(body), ["real.md"])

    def test_real_image_and_html_outside_math_remain_visible(self):
        body = '$$<a href="hidden.md">x</a>$$ <a href="real.md">x</a> ![figure](figure.png)'
        tokens = create_markdown_parser().parse(body)
        inline = next(token for token in tokens if token.type == "inline")
        html = [token.content for token in inline.children if token.type == "html_inline"]
        self.assertEqual(html, ['<a href="real.md">', '</a>'])
        self.assertEqual(links(body), ["figure.png"])

    def test_unclosed_and_escaped_math_never_hide_outside_links(self):
        for body in [r"\$ [x](real.md)", r"\\( [x](real.md)", "$x [x](real.md)",
                     "$$\n[x](real.md)\n", "\\[\n[x](real.md)\n", "$5 [x](real.md) and $6"]:
            with self.subTest(body=body):
                self.assertEqual(links(body), ["real.md"])

    def test_escaped_closer_and_newline_dollar_boundaries(self):
        self.assertEqual(links(r"$x\$ [x](hidden.md)$ [p](real.md)"), ["real.md"])
        self.assertEqual(links("$x\n[x](real.md)$"), ["real.md"])

    def test_inline_closing_display_delimiter_preserves_following_link(self):
        self.assertEqual(links("$$[x](hidden.md)$$ [p](real.md)"), ["real.md"])

    def test_bare_legacy_math_is_not_silently_exempted(self):
        self.assertEqual(links("=1+[2(d+1)/d^2](t^2+t)<=1."), ["t%5E2+t"])

    def test_math_in_link_label_keeps_outer_dependency(self):
        self.assertEqual(links("[$x$](proof.md)"), ["proof.md"])

    def test_literal_repair_preserves_original_and_records_exact_transform(self):
        formula = "=1+[2(d+1)/d^2](t^2+t)<=1."
        body = "Proof\n" + formula + "\n[real](proof.md)\n"
        start = body.index(formula)
        entry = {"source_sha256": "validated-by-caller", "reason": "Reviewed as literal arithmetic",
                 "literal_spans": [{"start": start, "end": start + len(formula), "expected": formula}]}
        rendered, audit = apply_literal_spans(body, entry)
        self.assertEqual(rendered, "Proof\n`" + formula + "`\n[real](proof.md)\n")
        self.assertEqual(links(rendered), ["proof.md"])
        self.assertEqual(body[start:start + len(formula)], formula)
        self.assertEqual(audit[0]["replacement"], "`" + formula + "`")
        self.assertEqual(audit[0]["reason"], entry["reason"])

    def test_literal_spans_apply_original_offsets_in_any_input_order(self):
        body = "a + b"
        rendered, audit = apply_literal_spans(body, {"reason": "Reviewed literals", "literal_spans": [
            {"start": 4, "end": 5, "expected": "b"}, {"start": 0, "end": 1, "expected": "a"}]})
        self.assertEqual(rendered, "`a` + `b`")
        self.assertEqual([item["start"] for item in audit], [0, 4])

    def test_invalid_or_stale_literal_spans_fail_closed(self):
        bad_entries = [
            {"reason": "", "literal_spans": [{"start": 0, "end": 1, "expected": "a"}]},
            {"reason": "review", "literal_spans": []},
            {"reason": "review", "literal_spans": [{"start": True, "end": 2, "expected": "b"}]},
            {"reason": "review", "literal_spans": [{"start": 0, "end": 1, "expected": "b"}]},
            {"reason": "review", "literal_spans": [{"start": 0, "end": 2, "expected": "ab"},
                                                    {"start": 1, "end": 3, "expected": "bc"}]},
            {"reason": "review", "literal_spans": [{"start": 0, "end": 1, "expected": "a"},
                                                    {"start": 1, "end": 2, "expected": "b"}]},
        ]
        for entry in bad_entries:
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                apply_literal_spans("abc", entry)
        for body in ["a\nb", "a`b", " a ", "a\rb"]:
            with self.subTest(body=body), self.assertRaises(ValueError):
                apply_literal_spans(body, {"reason": "review", "literal_spans": [
                    {"start": 0, "end": len(body), "expected": body}]})
        with self.assertRaises(ValueError):
            apply_literal_spans("`abc`", {"reason": "review", "literal_spans": [
                {"start": 1, "end": 4, "expected": "abc"}]})


if __name__ == "__main__":
    unittest.main()
