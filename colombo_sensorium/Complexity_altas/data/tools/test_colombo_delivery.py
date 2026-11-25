"""Check that generated attribution stays scoped and distinct from math status."""
from html.parser import HTMLParser
from collections import Counter
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class Delivery(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.rows, self.regimes, self.badges, self.panels = {}, {}, [], 0
        self.text = []
        self.feed(path.read_text())

    def handle_data(self, text):
        self.text.append(text)

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
        cls.editorial = json.loads((ROOT/'data/editorial/colombo_results.json').read_text())
        cls.registry = json.loads((ROOT/'data/derived/colombo_contributions.json').read_text())
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

    def test_card_and_point_labels_agree_with_adopted_contributions(self):
        for sid, point in self.points.items():
            entry = self.registry['settings'].get(sid)
            classes = self.home.rows[sid]
            if not entry or entry['state'] != 'adopted':
                self.assertNotIn('colombo', point)
                self.assertNotIn('is-colombo', classes)
                self.assertNotIn('is-colombo-pending', classes)
                continue
            state = entry['state']
            self.assertEqual(point['colombo']['state'], state)
            self.assertIn('is-colombo' if state == 'adopted' else 'is-colombo-pending', classes)
            expected = set(entry['comparison_ids'])
            self.assertEqual(set(point['colombo']['comparison_ids']), expected)

    def test_profile_row_marks_cover_exactly_the_reviewed_comparisons(self):
        for sid, entry in self.registry['settings'].items():
            page = Delivery(ROOT/'visualization/dist/settings'/f'{sid}.html')
            expected = set(entry['comparison_ids']) if entry['state'] == 'adopted' else set()
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
        self.assertEqual(len(self.editorial['papers']), 22)
        ids = {p['id'] for p in self.editorial['papers']}
        self.assertEqual(ids, {
            '2610.22208', '2610.20187', '2610.17074', '2610.16991', '2610.16832',
            '2610.16771', '2610.12184', '2610.03638', '2610.03633', '2610.02095',
            '2609.35840', '2610.00276', '2610.00275', '2610.00260', '2609.28246',
            '2609.28238', '2610.00245', '2609.28202', '2610.00229', '2609.18728',
            '2609.18230', '2609.13462'})
        mapped = {sid for sid, e in self.registry['settings'].items()
                  if any(c['paper_id'] == '2610.00260' for c in e['contributions'])}
        self.assertEqual(mapped, {'SO_FO_S01_direction_HP'})

    def test_historical_near_optimal_subset_keeps_its_exact_scope(self):
        selected = {sid: e['highlight'] for sid, e in self.registry['settings'].items() if e.get('highlight')}
        self.assertEqual(len(selected), 39)
        self.assertEqual(sum(len(e['comparison_ids']) for e in selected.values()), 66)
        self.assertEqual(Counter(e['state'] for e in self.editorial['settings'].values()),
                         {'adopted': 49, 'pending': 2})
        statuses, paper_ids = Counter(), set()
        for sid, entry in selected.items():
            profile = json.loads((ROOT/'data/settings'/sid/'profile.json').read_text())
            comparisons = {c['comparison_id']: c for c in profile['comparisons']}
            for cid in entry['comparison_ids']:
                code = comparisons[cid]['status']['code']
                self.assertIn(code, ('optimal', 'logarithmic_gap'))
                statuses[code] += 1
            for contribution in self.registry['settings'][sid]['contributions']:
                if set(contribution['comparison_ids']) & set(entry['comparison_ids']):
                    paper_ids.add(contribution['paper_id'])
        self.assertEqual(statuses, {'optimal': 41, 'logarithmic_gap': 25})
        self.assertEqual(len(paper_ids), 20)
        hp = 'SO_FO_S01_direction_HP'
        saturation = hp + '__randomized__probability__c_saturation_20261122'
        profile = json.loads((ROOT/'data/settings'/hp/'profile.json').read_text())
        self.assertIn(saturation, {c['comparison_id'] for c in profile['comparisons']})
        self.assertEqual(len(selected[hp]['comparison_ids']), 5)
        self.assertNotIn(saturation, selected[hp]['comparison_ids'])

    def test_added_papers_credit_only_the_six_located_comparisons(self):
        expected = {
            'CV_S_HIGH_SADDLE_tan': ('2609.28246', 'CV_SRC_saddle_higher_2609_28246',
                {'main': ('b2', 'c1', 'e1')}),
            'CV_S_HIGH_SADDLE_gap': ('2609.28246', 'CV_SRC_saddle_higher_2609_28246',
                {'main': ('b2', 'c1', 'e1')}),
            'SO_ZO_E04': ('2609.18728', 'SO_SRC_aafbdd36039133ac',
                {'deterministic': ('b1', 'c3', 'e1'), 'randomized': ('b1', 'c3', 'e1')}),
            'SO_ZO_E09b': ('2609.18728', 'SO_SRC_aafbdd36039133ac',
                {'deterministic': ('b11', 'c6', 'e20'), 'randomized': ('b13', 'c7', 'e27')})}
        mapped = {sid for sid, entry in self.registry['settings'].items()
                  if any(c['paper_id'] in {'2609.28246', '2609.18728'} for c in entry['contributions'])}
        self.assertEqual(mapped, set(expected))
        for sid, (paper_id, reference_id, views) in expected.items():
            with self.subTest(setting=sid):
                entry = self.registry['settings'][sid]
                contributions = [c for c in entry['contributions'] if c['paper_id'] == paper_id]
                self.assertEqual(len(contributions), 1)
                contribution = contributions[0]
                prefix = lambda view, key: sid + '__' + view + '__' + key
                bids = {prefix(view, row[0]) for view, row in views.items()}
                cids = {prefix(view, row[1]) for view, row in views.items()}
                self.assertEqual(set(contribution['reference_ids']), {reference_id})
                self.assertEqual(set(contribution['view_ids']), set(views))
                self.assertEqual(set(contribution['bound_refs']), bids)
                self.assertEqual(set(contribution['comparison_ids']), cids)
                self.assertEqual(set(entry['highlight']['comparison_ids']), cids)
                profile = json.loads((ROOT/'data/settings'/sid/'profile.json').read_text())
                bounds = {b['id']: b for b in profile['bounds']}
                evidence = {e['id']: e for e in profile['evidence']}
                for view, (bid, cid, eid) in views.items():
                    self.assertIn(prefix(view, eid), bounds[prefix(view, bid)]['evidence_refs'])
                    located = evidence[prefix(view, eid)]
                    self.assertEqual(located['source_ref'], reference_id)
                    self.assertTrue(located['locator']['pdf_pages'])
                    self.assertNotIn('remains to be verified', located['locator']['theorem'])
                if sid == 'SO_ZO_E09b':
                    self.assertIn('n=1', entry['highlight']['scope_note'])
                    for c in profile['comparisons']:
                        if c['comparison_id'] in cids:
                            self.assertIn('n=1', c['predicate_text'])

    def test_summary_stays_outside_atlas_files_and_pages(self):
        self.assertEqual(self.home.panels, 0)
        for name in ('Colombo_settings_summary_20261122.html',
                     'Colombo_settings_summary_20261122.json', 'START_HERE.txt',
                     'PACKAGE_MANIFEST.json'):
            self.assertFalse((ROOT/name).exists(), name)

    def test_local_source_inventory_matches_catalog_and_native_references(self):
        sources = json.loads((ROOT/'data/sources/colombo/catalog.json').read_text())
        registered = {row['id'] for row in sources}
        self.assertEqual(registered, {row['id'] for row in self.registry['papers']
                                      if row['id'].startswith('COLOMBO_')})
        for path in (ROOT/'data/settings').glob('*/profile.json'):
            profile = json.loads(path.read_text())
            local_refs = {ref['id'] for ref in profile['references']
                          if ref['id'].startswith('COLOMBO_')}
            self.assertTrue(local_refs <= registered, path.parent.name)

    def test_retained_manuscripts_show_explicit_contribution_scope(self):
        sources = {row['id']: row for row in json.loads(
            (ROOT/'data/sources/colombo/catalog.json').read_text())}
        expected = {'COLOMBO_N01': 'SO_FO_N05_FSD',
                    'COLOMBO_A4': 'SO_HO_HOI10_S_weighted_jet_L1L2',
                    'COLOMBO_U10': 'SO_ZO_E02'}
        for pid, sid in expected.items():
            source = sources[pid]
            entry = self.registry['settings'][sid]
            self.assertEqual(entry['state'], 'adopted')
            self.assertIn(pid, entry['paper_ids'])
            page = Delivery(ROOT/'visualization/dist/settings'/f'{sid}.html')
            text = ' '.join(page.text)
            self.assertIn(source['contribution_label_en'], text)
            self.assertIn(source['contribution_note_en'], text)


if __name__ == '__main__':
    unittest.main()
