"""Literal text identifiers must render without changing mathematical subscripts."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'visualization/src'))
from build_site_public import normalize_math_text, ProfileRenderer


class MathTextRenderingTests(unittest.TestCase):
    def test_literal_identifier_and_math_subscripts_have_distinct_treatment(self):
        source = r'\text{view_name; $x_i$; \(y_j\); \ensuremath{z_k}; escaped\_name}\quad f(x_*)'
        expected = r'\text{view\_name; $x_i$; \(y_j\); \ensuremath{z_k}; escaped\_name}\quad f(x_*)'
        self.assertEqual(normalize_math_text(source), expected)
        self.assertEqual(normalize_math_text(expected), expected)

    def test_nested_text_keeps_the_existing_normalization(self):
        source = r'\text{outer_name \text{inner_name}}+x_i'
        expected = r'\text{outer\_name inner\_name}+x_i'
        self.assertEqual(normalize_math_text(source), expected)
        self.assertEqual(normalize_math_text(expected), expected)

    def test_e03_q5_uses_display_escaping_without_mutating_the_source(self):
        profile = json.loads((ROOT / 'data/settings/SO_ZO_E03/profile.json').read_text())
        before = deepcopy(profile)
        quantity = next(q for q in profile['quantities']
                        if q['id'] == 'SO_ZO_E03__bounded_query_deterministic__q1')
        renderer = ProfileRenderer(profile)
        rendered = renderer.math(quantity['expression_latex'])
        self.assertIn(r'\text{ admissible in bounded\_query\_deterministic}', rendered)
        self.assertIn(r'f(x_*)', rendered)
        self.assertEqual(profile, before)


if __name__ == '__main__':
    unittest.main()
