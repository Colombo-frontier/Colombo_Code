"""Contribution provenance must respect the native active scientific contracts."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'visualization/src'))
from colombo_results import load_colombo_results, public_summary, display_registry


class ColomboResultsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.profile = {
            'setting_id': 'example', 'views': [{'view_id': 'main'}, {'view_id': 'other'}],
            'references': [{'id': 'paper', 'url': 'https://arxiv.org/pdf/2610.03633v2'},
                           {'id': 'unrelated', 'url': 'https://arxiv.org/abs/1234.56789'}],
            'bounds': [{'id': 'upper', 'view_id': 'main', 'guarantee_id': 'g1', 'quantity_ref': 'q1',
                        'included_in_bracket': True, 'eligible_for_bracket': True,
                        'source_refs': ['paper']}],
            'comparisons': [{'comparison_id': 'c1', 'view_id': 'main', 'guarantee_id': 'g1',
                             'quantity_id': 'q1', 'status': {'code': 'missing_lower'},
                             'bracket': {'upper_refs': ['upper']}}],
            'evidence': [], 'proofs': []}
        self.registry = {'schema_version': '1.0.0', 'papers': [
            {'id': '2610.03633', 'title': 'A registered result', 'url': 'https://arxiv.org/abs/2610.03633'}],
            'settings': {'example': {'state': 'adopted', 'note': 'Manual source and scope review.',
                                     'contributions': [{'paper_id': '2610.03633', 'reference_ids': ['paper'],
                                                        'bound_refs': ['upper'], 'comparison_ids': ['c1'],
                                                        'view_ids': ['main'], 'binding': 'scoped_native_support',
                                                        'note': 'Only this upper bound, with lower still missing.'}]}}}

    @property
    def info(self):
        return self.registry['settings']['example']

    @property
    def contribution(self):
        return self.info['contributions'][0]

    def load(self, stale=False, supplied=None):
        path = self.root / 'data/settings/example/profile.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        raw = (json.dumps(self.profile, ensure_ascii=False, indent=2) + '\n').encode()
        path.write_bytes(raw)
        self.info['source_profile_sha256'] = '0' * 64 if stale else hashlib.sha256(raw).hexdigest()
        registry_path = self.root / 'data/editorial/colombo_results.json'
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_text(json.dumps(self.registry, ensure_ascii=False))
        return load_colombo_results(self.root, {'example': supplied or self.profile})

    def test_direct_selected_source_is_adopted_without_changing_scientific_status(self):
        before = deepcopy(self.profile)
        result = self.load()['settings']['example']
        self.assertEqual(result['label'], '★ Colombo')
        self.assertEqual(result['comparison_ids'], ['c1'])
        self.assertIn('only to the documented regions', result['scope_note'])
        self.assertIn('preserves the native mathematical status', result['scope_note'])
        self.assertEqual(self.profile, before)
        self.assertEqual(self.profile['comparisons'][0]['status']['code'], 'missing_lower')

    def test_located_evidence_or_explicit_local_transfer_supports_selected_bound(self):
        for route in ('evidence', 'proof'):
            with self.subTest(route=route):
                self.profile['bounds'][0]['source_refs'] = []
                self.profile['bounds'][0]['evidence_refs'] = ['e1']
                if route == 'evidence':
                    self.profile['evidence'] = [{'id': 'e1', 'source_ref': 'paper'}]
                else:
                    self.profile['evidence'] = [{'id': 'e1', 'proof_refs': ['p1']}]
                    self.profile['proofs'] = [{'id': 'p1', 'source_refs': ['paper']}]
                self.assertEqual(self.load()['settings']['example']['state'], 'adopted')

    def test_bibliography_alone_does_not_create_a_contribution(self):
        self.profile['bounds'][0]['source_refs'] = []
        with self.assertRaisesRegex(ValueError, 'upper.*explicit paper support path'):
            self.load()

    def test_stale_raw_profile_hash_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'stale source_profile_sha256'):
            self.load(stale=True)

    def highlight(self):
        self.profile['bounds'].append({'id': 'lower', 'view_id': 'main', 'guarantee_id': 'g1',
                                      'quantity_ref': 'q1', 'source_refs': ['paper']})
        self.profile['comparisons'][0]['status']['code'] = 'optimal'
        self.profile['comparisons'][0]['bracket']['lower_refs'] = ['lower']
        self.info['highlight'] = {'comparison_ids': ['c1'], 'scope_note': 'Only the native guarded region.'}

    def test_display_excludes_unclosed_contributions_without_altering_provenance(self):
        result = self.load()
        self.assertIn('example', result['settings'])
        self.assertEqual(display_registry(result)['settings'], {})

    def test_display_accepts_reviewed_near_optimal_selection(self):
        self.highlight()
        result = display_registry(self.load())['settings']['example']
        self.assertEqual(result['comparison_ids'], ['c1'])
        self.assertEqual(result['view_ids'], ['main'])
        self.assertEqual(result['label'], '★ Colombo')

    def test_highlight_rejects_unclosed_status_or_missing_side(self):
        self.highlight()
        self.profile['comparisons'][0]['status']['code'] = 'polynomial_gap'
        with self.assertRaisesRegex(ValueError, 'not near-optimal'):
            self.load()
        self.profile['comparisons'][0]['status']['code'] = 'optimal'
        self.profile['comparisons'][0]['bracket']['lower_refs'] = []
        with self.assertRaisesRegex(ValueError, 'two-sided bracket'):
            self.load()

    def test_highlight_rejects_pending_and_unattributed_comparisons(self):
        self.highlight()
        self.info['highlight']['comparison_ids'] = ['unattributed']
        with self.assertRaisesRegex(ValueError, 'outside attributed'):
            self.load()

    def test_callers_canonical_profile_must_match_disk(self):
        other = deepcopy(self.profile)
        other['comparisons'][0]['status']['code'] = 'optimal'
        with self.assertRaisesRegex(ValueError, 'supplied canonical profile differs'):
            self.load(supplied=other)

    def test_unregistered_paper_is_rejected(self):
        self.contribution['paper_id'] = '2610.00275'
        with self.assertRaisesRegex(ValueError, 'paper is not registered'):
            self.load()

    def test_reference_must_identify_the_registered_arxiv_paper(self):
        self.contribution['reference_ids'] = ['unrelated']
        with self.assertRaisesRegex(ValueError, 'native reference does not identify'):
            self.load()

    def test_arxiv_identity_cannot_match_a_numeric_prefix(self):
        self.profile['references'][0]['url'] = 'https://arxiv.org/abs/2610.036330'
        with self.assertRaisesRegex(ValueError, 'native reference does not identify'):
            self.load()

    def test_unknown_bound_view_and_comparison_are_rejected(self):
        for field in ('bound_refs', 'view_ids', 'comparison_ids'):
            with self.subTest(field=field):
                previous = self.contribution[field]
                self.contribution[field] = ['missing']
                with self.assertRaises(ValueError):
                    self.load()
                self.contribution[field] = previous

    def test_existing_wrong_view_and_wrong_comparison_do_not_pass_foreign_keys(self):
        self.contribution['view_ids'] = ['other']
        with self.assertRaisesRegex(ValueError, 'views do not match'):
            self.load()
        self.contribution['view_ids'] = ['main']
        self.profile['comparisons'].append({'comparison_id': 'c2', 'view_id': 'other', 'guarantee_id': 'g1',
                                            'quantity_id': 'q1', 'bracket': {'upper_refs': []}})
        self.contribution['comparison_ids'] = ['c2']
        with self.assertRaisesRegex(ValueError, 'no contribution bound selected'):
            self.load()

    def test_comparison_contract_cannot_reuse_bound_for_another_quantity(self):
        self.profile['comparisons'][0]['quantity_id'] = 'q2'
        with self.assertRaisesRegex(ValueError, 'contract mismatch'):
            self.load()

    def test_all_registered_bounds_need_actual_comparison_selection(self):
        unselected = deepcopy(self.profile['bounds'][0])
        unselected['id'] = 'unselected'
        self.profile['bounds'].append(unselected)
        self.contribution['bound_refs'].append('unselected')
        with self.assertRaisesRegex(ValueError, 'unselected bound'):
            self.load()

    def test_quarantined_lower_cannot_receive_adopted_label(self):
        for mutation in ('excluded', 'not_certified'):
            with self.subTest(mutation=mutation):
                self.profile['bounds'][0].update(included_in_bracket=True, eligible_for_bracket=True)
                if mutation == 'excluded':
                    self.profile['bounds'][0]['eligible_for_bracket'] = False
                else:
                    self.profile['bounds'][0]['lower_scope_type'] = 'not_certified'
                with self.assertRaisesRegex(ValueError, 'contradicts native admission'):
                    self.load()

    def test_pending_excluded_paper_is_retained_without_a_public_highlight(self):
        self.info['state'] = 'pending'
        self.contribution['comparison_ids'] = []
        self.profile['comparisons'] = []
        self.profile['bounds'][0].update(included_in_bracket=False, eligible_for_bracket=False,
                                          lower_scope_type='not_certified')
        registry = self.load()
        result = registry['settings']['example']
        self.assertEqual(result['state'], 'pending')
        self.assertEqual(result['comparison_ids'], [])
        self.assertEqual(display_registry(registry)['settings'], {})
        self.info['highlight'] = {'comparison_ids': ['c1'], 'scope_note': 'Invalid pending highlight.'}
        with self.assertRaisesRegex(ValueError, 'pending attribution cannot be highlighted'):
            self.load()

    def test_pending_cannot_hide_a_selected_or_admitted_bound(self):
        self.info['state'] = 'pending'
        self.contribution['comparison_ids'] = []
        with self.assertRaisesRegex(ValueError, 'contradicts native admission'):
            self.load()
        self.profile['bounds'][0].update(included_in_bracket=False, eligible_for_bracket=False)
        with self.assertRaisesRegex(ValueError, 'contradicts native admission'):
            self.load()

    def test_current_support_cannot_depend_on_a_historical_proof(self):
        self.profile['bounds'][0]['proof_refs'] = ['old']
        self.profile['proofs'] = [{'id': 'old', 'source_refs': ['paper'],
                                  'lifecycle': {'state': 'historical', 'eligible_for_current_bounds': False}}]
        with self.assertRaisesRegex(ValueError, 'no eligible explicit paper support path'):
            self.load()

    def test_public_summary_excludes_private_registry_and_copies_lists(self):
        info = self.load()['settings']['example']
        summary = public_summary(info)
        self.assertEqual(set(summary), {'state', 'label', 'paper_ids', 'comparison_ids', 'view_ids', 'scope_note'})
        summary['comparison_ids'].append('changed')
        self.assertEqual(info['comparison_ids'], ['c1'])
        self.assertIsNone(public_summary(None))


if __name__ == '__main__':
    unittest.main()
