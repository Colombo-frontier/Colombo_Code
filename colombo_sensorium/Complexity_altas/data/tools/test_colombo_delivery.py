"""Check that generated attribution stays scoped and distinct from math status."""
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class Delivery(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.rows, self.regimes, self.badges, self.panels = {}, {}, [], 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = a.get('class', '').split()
        if tag == 'article' and 'setting-row' in classes:
            self.rows[a['data-setting']] = classes
        if tag == 'article' and 'regime-card' in classes:
            for cid in a['data-comparison-ids'].split(','):
                self.regimes[cid] = set(filter(None, a.get('data-colombo-comparisons', '').split(',')))
        if 'colombo-badge' in classes:
            self.badges.append(a['data-colombo-state'])
        if a.get('id') in ('colombo-results', 'colombo-paper-map'):
            self.panels += 1


class ColomboDeliveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT/'data/editorial/colombo_results.json').read_text())
        cls.overview = json.loads((ROOT/'data/derived/atlas_overview.json').read_text())
        cls.points = {p['id']: p for p in cls.overview['points']}
        cls.home = Delivery(ROOT/'visualization/dist/index.html')

    def test_all_settings_remain_present_with_their_original_statuses(self):
        profiles = list((ROOT/'data/settings').glob('*/profile.json'))
        self.assertEqual(set(self.home.rows), {p.parent.name for p in profiles})
        self.assertEqual(set(self.points), set(self.home.rows))
        for path in profiles:
            p = json.loads(path.read_text())
            self.assertEqual(self.points[p['setting_id']]['comparisons'], p['summary_status']['status_counts'])

    def test_card_and_point_labels_agree_with_reviewed_registry_only(self):
        for sid, point in self.points.items():
            entry = self.registry['settings'].get(sid)
            classes = self.home.rows[sid]
            if not entry or not entry.get('highlight'):
                self.assertNotIn('colombo', point)
                self.assertNotIn('is-colombo', classes)
                self.assertNotIn('is-colombo-pending', classes)
                continue
            state = entry['state']
            self.assertEqual(point['colombo']['state'], state)
            self.assertIn('is-colombo' if state == 'adopted' else 'is-colombo-pending', classes)
            expected = set(entry['highlight']['comparison_ids'])
            self.assertEqual(set(point['colombo']['comparison_ids']), expected)

    def test_profile_row_marks_cover_exactly_the_reviewed_comparisons(self):
        for sid, entry in self.registry['settings'].items():
            page = Delivery(ROOT/'visualization/dist/settings'/f'{sid}.html')
            expected = set(entry.get('highlight', {}).get('comparison_ids', []))
            actual = set().union(*page.regimes.values())
            self.assertEqual(actual, expected, sid)
            self.assertEqual(page.panels, 0, sid)
            if expected:
                self.assertIn('adopted', page.badges, sid)
            else:
                self.assertFalse(page.badges, sid)

    def test_e03_full_space_and_matrix_quarantine_do_not_gain_solved_rows(self):
        sid = 'SO_ZO_E03'
        page = Delivery(ROOT/'visualization/dist/settings'/f'{sid}.html')
        for cid, marks in page.regimes.items():
            if '__bounded_query_deterministic__' not in cid:
                self.assertFalse(marks, cid)
        for sid in ('CV_S_MG_RANDOM_BALL', 'CV_S_SIMPLEX_MATRIX_GAME'):
            self.assertNotIn('colombo', self.points[sid])
            self.assertEqual(self.registry['settings'][sid]['state'], 'pending')

    def test_heavy_tail_paper_uses_the_existing_profile(self):
        self.assertEqual(len(self.registry['papers']), 20)
        ids = {p['id'] for p in self.registry['papers']}
        self.assertIn('2610.00260', ids)
        mapped = {sid for sid, e in self.registry['settings'].items()
                  if any(c['paper_id'] == '2610.00260' for c in e['contributions'])}
        self.assertEqual(mapped, {'SO_FO_S01_direction_HP'})

    def test_only_reviewed_nontrivial_near_optimal_regions_are_highlighted(self):
        selected = {sid: e['highlight'] for sid, e in self.registry['settings'].items() if e.get('highlight')}
        self.assertEqual(len(selected), 35)
        self.assertEqual(sum(len(e['comparison_ids']) for e in selected.values()), 60)
        for sid, entry in selected.items():
            profile = json.loads((ROOT/'data/settings'/sid/'profile.json').read_text())
            comparisons = {c['comparison_id']: c for c in profile['comparisons']}
            for cid in entry['comparison_ids']:
                self.assertIn(comparisons[cid]['status']['code'], ('optimal', 'logarithmic_gap'))
        hp = 'SO_FO_S01_direction_HP'
        saturation = hp + '__randomized__probability__c_saturation_20261122'
        profile = json.loads((ROOT/'data/settings'/hp/'profile.json').read_text())
        self.assertIn(saturation, {c['comparison_id'] for c in profile['comparisons']})
        self.assertEqual(len(selected[hp]['comparison_ids']), 5)
        self.assertNotIn(saturation, selected[hp]['comparison_ids'])

    def test_summary_stays_outside_atlas_files_and_pages(self):
        self.assertEqual(self.home.panels, 0)
        for name in ('Colombo_settings_summary_20261122.html',
                     'Colombo_settings_summary_20261122.json', 'START_HERE.txt',
                     'PACKAGE_MANIFEST.json'):
            self.assertFalse((ROOT/name).exists(), name)


if __name__ == '__main__':
    unittest.main()
