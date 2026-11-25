#!/usr/bin/env python3
"""Regression checks for the 2026-11-26 SFO source integration.

These tests exercise routing and frozen provenance, not the source theorems.
Synthetic values for universal constants test the declared scope boundaries;
they do not assign numerical constants to the manuscript.
"""
import importlib.util
import itertools
import json
import math
import operator
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
DATA = HERE.parent
spec = importlib.util.spec_from_file_location('comparison_scope_reader', DATA / 'tools/test_comparison_scope_repair.py')
repair = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repair)
canonical_sha, indexed = repair.canonical_sha, repair.indexed
DET = 'BL_SPEC_det_primitive'
DP = DET + '__sfo_20261126__'
SOURCE = 'COLOMBO_SFO_JOINT_20261126'

# Frozen identities observed in the supplied baseline, commit b2001c3.
# Keep these constants independent of newly generated candidate records.
DET_COMMON_SHA = 'bbcf6231bb68a2f8ab68728054a5189f8bb845a9c5ce017e279c8420be80a3f8'
DET_VIEWS_SHA = 'e3e85ce26a5d380d614a0b58c9a47bd9493b2d7e69a41f4aac0a6147a99ab1bf'
DET_PARAMETER_SHAS = {
    DET + '_p_71bfc2660c': '6e75b58f855ac7381de7bd42732966614417701a3acc5fb7dc70120ab04c9cf7',
    DET + '_p_44fae62c5c': '05c720bae25e5004e1ac5c1765c505324453e09b606dcaec1e1ee578de374f21',
}
DET_COMPARISON_SHAS = {
    DET + '__main__c1': '0af6b125b82cc4c9e4ffa0f4fa0788da1e48482e84ba2dfcb8d1550d58a06f79',
    DET + '__main__c2': '0498dd0cb820eedefb8d8a2db5ae3e065abecdaca86fa488b5ef6c849321dda9',
}
DET_BOUND_SHAS = {
    DET + '__main__b1': 'a09c3dc1d8bd902f97329a82eed58f8478429cb3573f940b875b3c8c3436a428',
    DET + '__main__b2': '5067c8140f17f0b4bdd2765875978fa702653352260275495d9b4f7b5aa397bb',
}
PRIMARY = 'BL_SPEC_joint_expected_cost'
PP = PRIMARY + '__main__'
PRIMARY_COMMON_SHA = 'd49ecb90a17193bca3c8acdedb4f3d47d2254bc49fed453999c873289d16f987'
PRIMARY_VIEWS_SHA = '5c4baa574ea8f517d0da8494fb4f7c057f363398301cc8d02a8e2b2f8e381cbc'
PRIMARY_Q_SHA = '4d8fd29b92a3bf0092ebb4fecb0fd15deb2ca05a0dbe355fff32934843c8e0c2'
PRIMARY_COMPARISON_SHAS = {
    PP + 'c_effective_zero_20261122': 'ef9c3e423b7c164c0ba70134b5dc91662269af92f584ec375efdbcff4fbc9e98',
    PP + 'c_source_remaining_20261122': '2235d4b97417f17f389da7e2d2df2571c710f0b22e2104d078573bc6dfae645d',
    PP + 'c_matching_noise_20261122': '81922a43e1d0b88318d5be81b03f3288afda5360e2628e1bc311c459fd37f0ea',
    PP + 'c_residual_20261122': 'a73ebd1ec55a409daa637ed0f1e374dbba5d0364613502c4cb7a9c44eb90bb34',
}


class NativePredicateReader(repair.PredicateReader):
    """Reuse the scope reader and support both historical native AST forms.

Opaque older theorem windows have no numeric AST. Tests supply their Boolean
truth values explicitly, checking every possibility without guessing their
unrecorded source constants or interpreting mathematical prose as code.
"""
    def __init__(self, profile, values, opaque_regions=None):
        super().__init__(profile, values)
        self.opaque_regions = opaque_regions or {}

    def region(self, regime_id):
        if regime_id in self.opaque_regions:
            return self.opaque_regions[regime_id]
        return super().region(regime_id)

    def eval(self, expression):
        if isinstance(expression, dict):
            if 'parameter' in expression:
                return self.values[expression['parameter']]
            if isinstance(expression.get('cmp'), dict):
                e = expression['cmp']
                compare = {'eq': operator.eq, 'ne': operator.ne, 'lt': operator.lt,
                           'le': operator.le, 'gt': operator.gt, 'ge': operator.ge}
                return compare[e['op']](self.eval(e['left']), self.eval(e['right']))
        return super().eval(expression)


def read_det():
    path = DATA / 'settings' / DET / 'profile.json'
    return json.loads(path.read_text())


def read_primary():
    path = DATA / 'settings' / PRIMARY / 'profile.json'
    return json.loads(path.read_text())


def det_values(**overrides):
    v = {'L': 4.0, r'\mu': 1.0, r'\rho': 4.0, 'C_f': 4.0,
         r'\Delta': 4.0, 'R_0': 0.0, r'\varepsilon': 0.125,
         'c_0': 0.125, r'p_{\log}': 2.0, 'd_x': 8, 'd_y': 8}
    v.update(overrides)
    v[r'\ell'] = max(v['C_f'], v['L'], v[r'\rho'])
    v[r'\kappa'] = v[r'\ell'] / v[r'\mu'] if v[r'\mu'] else math.inf
    v[r'\kappa_g'] = v['L'] / v[r'\mu'] if v[r'\mu'] else math.inf
    v[r'\theta'] = v[r'\rho'] / v[r'\mu'] if v[r'\mu'] else math.inf
    v[r'\chi'] = 1 + v[r'\theta']
    return v


def primary_values(**overrides):
    v = {'L': 4.0, 'L_f': 4.0, 'L_g': 4.0, 'C_f': 4.0,
         r'\mu': 1.0, r'\rho': 4.0, r'\Delta': 4.0,
         r'\sigma_f': 1.0, r'\sigma_g': 1.0, 'R_0': 0.0,
         r'\varepsilon': 0.125, r'\Lambda_\Phi': 512.0,
         'c_0': 0.125, 'C_F': 8.0, 'C_*': 2.0,
         r'p_{\log}': 2.0, r'\varepsilon_P': 0.2}
    v.update(overrides)
    v[r'\kappa'] = v['L'] / v[r'\mu']
    v[r'\theta'] = v[r'\rho'] / v[r'\mu']
    v[r'\chi'] = 1 + v[r'\theta']
    return v


def source_s0(values):
    kappa = values[r'\kappa']
    q = (kappa ** 2 - 1) ** 0.5
    g = (2 * values['L'] * values[r'\Delta']) ** 0.5
    t = min(q * g / kappa, 2 * values['L'])
    return (g ** 2 - t ** 2) ** 0.5 + q * t


class DeterministicSfoIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = read_det()
        cls.comparisons = indexed(cls.p, 'comparisons', 'comparison_id')
        cls.bounds = indexed(cls.p, 'bounds')
        cls.joint = DP + 'c_joint'
        cls.residuals = [DP + 'c_legacy_1_remaining', DP + 'c_legacy_2_remaining']
        cls.old_regions = [DET + '__main__r1', DET + '__main__r3']

    def reader(self, values, legacy=(True, True)):
        return NativePredicateReader(self.p, values, dict(zip(self.old_regions, legacy)))

    def test_joint_window_includes_declared_closed_boundaries(self):
        # c0 is synthetic. L=Delta keeps the accuracy boundary exactly binary.
        for rho, radius in itertools.product((1.0, 4.0, 16.0), (0.0, 1e100)):
            values = det_values(**{r'\rho': rho, 'R_0': radius, r'\varepsilon': 0.5})
            with self.subTest(rho=rho, R0=radius):
                self.assertTrue(self.reader(values).region(DP + 'r_joint'))
                above = dict(values, **{r'\varepsilon': math.nextafter(0.5, math.inf)})
                self.assertFalse(self.reader(above).region(DP + 'r_joint'))
        self.assertTrue(self.reader(det_values(L=2.0, C_f=2.0, **{r'\Delta': 2.0, r'\rho': 1.0})).region(DP + 'r_joint'))

    def test_joint_guard_rejects_unproved_parameter_slices(self):
        rejected = [{'C_f': 3.0}, {'C_f': 5.0}, {r'\mu': 3.0},
                    {r'\rho': 0.0}, {r'\rho': 0.5}, {r'\rho': 16.01},
                    {r'\Delta': 0.0}, {'R_0': -1.0}, {r'\varepsilon': 0.0},
                    {r'\varepsilon': 0.5001}]
        for overrides in rejected:
            with self.subTest(overrides=overrides):
                self.assertFalse(self.reader(det_values(**overrides)).region(DP + 'r_joint'))

    def test_legacy_complements_retain_off_normalized_and_outside_accuracy_points(self):
        samples = [det_values(), det_values(C_f=3.0), det_values(C_f=5.0),
                   det_values(**{r'\rho': 0.0}), det_values(**{r'\rho': 20.0}),
                   det_values(**{r'\varepsilon': 0.5001})]
        for values, legacy in itertools.product(samples, itertools.product((False, True), repeat=2)):
            reader = self.reader(values, legacy)
            inside = reader.region(DP + 'r_joint')
            actual = {cid for cid in [self.joint, *self.residuals]
                      if reader.eval(self.comparisons[cid]['predicate'])}
            expected = ({self.joint} if inside else
                        {cid for cid, holds in zip(self.residuals, legacy) if holds})
            with self.subTest(Cf=values['C_f'], rho=values[r'\rho'], eps=values[r'\varepsilon'], legacy=legacy):
                self.assertEqual(actual, expected)
                self.assertEqual(bool(actual), inside or any(legacy))
                if inside:
                    self.assertTrue(actual.isdisjoint(self.residuals))

    def test_ell_and_kappa_keep_their_original_identity(self):
        parameters = indexed(self.p, 'parameters')
        for pid, frozen in DET_PARAMETER_SHAS.items():
            self.assertEqual(canonical_sha(parameters[pid]), frozen)
        by_symbol = {p['symbol']: p for p in self.p['parameters']}
        self.assertEqual(by_symbol[r'\kappa_g']['definition'], r'$\kappa_g=L/\mu$')
        values = det_values(**{r'\rho': 16.0})
        self.assertEqual(values[r'\kappa'], 16.0)
        self.assertEqual(values[r'\kappa_g'], 4.0)
        self.assertTrue(self.reader(values).region(DP + 'r_joint'))
        tracked = set(self.p['quantities'][0]['tracked_parameters'])
        required = {by_symbol[s]['id'] for s in ['L', 'C_f', r'\mu', r'\rho', r'\Delta', 'R_0', r'\kappa_g', r'\theta', r'\chi']}
        self.assertTrue(required.issubset(tracked))

    def test_native_model_and_guarantee_signatures_stay_frozen(self):
        self.assertEqual(canonical_sha(self.p['common_specification']), DET_COMMON_SHA)
        self.assertEqual(canonical_sha(self.p['views']), DET_VIEWS_SHA)
        proof = indexed(self.p, 'proofs', 'proof_id')[DP + 'p_contract_transfer']
        bindings = {item['pointer']: item['sha256'] for item in proof['premises']}
        self.assertEqual(bindings['/common_specification'], DET_COMMON_SHA)
        self.assertEqual(bindings['/views/0'], canonical_sha(self.p['views'][0]))

    def test_legacy_comparison_hashes_and_source_bounds_are_retained(self):
        history = {entry['comparison']['comparison_id']: entry
                   for entry in self.p['provenance']['comparison_history']}
        for cid, frozen in DET_COMPARISON_SHAS.items():
            entry = history[cid]
            self.assertEqual(canonical_sha(entry['comparison']), frozen)
            self.assertEqual(entry['comparison_sha256'], frozen)
            self.assertNotIn(cid, self.comparisons)
            self.assertTrue(set(entry['superseded_by']).issubset(self.comparisons))
        for bid, frozen in DET_BOUND_SHAS.items():
            scientific = {k: v for k, v in self.bounds[bid].items() if k != 'selected_in_regimes'}
            self.assertEqual(canonical_sha(scientific), frozen)
            self.assertTrue(set(self.bounds[bid]['selected_in_regimes']).issubset(self.residuals))

    def test_new_bound_dispatch_cannot_escape_joint_guard(self):
        row = self.comparisons[self.joint]
        self.assertEqual(row['status']['code'], 'logarithmic_gap')
        for side in ['upper', 'lower']:
            refs = row['bracket'][side + '_refs']
            self.assertEqual(refs, [DP + 'b_joint_' + side])
            bound = self.bounds[refs[0]]
            self.assertEqual(bound['region_refs'], [DP + 'r_joint'])
            self.assertEqual(bound['selected_in_regimes'], [self.joint])
            self.assertEqual(bound['source_refs'], [SOURCE])
            guards = row['bracket']['claim_guards'][refs[0]]
            self.assertEqual({g['region_ref'] for g in guards}, {DP + 'r_joint'})
        self.assertEqual(self.bounds[DP + 'b_joint_lower']['lower_scope_type'], 'unrestricted_deterministic')


class PrimarySfoIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = read_primary()
        cls.comparisons = indexed(cls.p, 'comparisons', 'comparison_id')
        cls.regions = cls.p['joint_analysis']['source_regions_20261126']
        cls.guards = cls.regions['guard_region_refs']
        cls.historical = cls.regions['historical_region_refs']

    def reader(self, values, E=False, S=False, N=False):
        return NativePredicateReader(self.p, values, {
            self.historical['E']: E, self.historical['S']: S,
            self.historical['N']: N})

    def test_joint_and_curvature_guards_preserve_independent_curvature_and_accuracy(self):
        # Exact closed accuracy and variation boundaries, at source-normalized
        # public budgets. The curvature multiplier is a synthetic fixed number.
        for theta in (1.0, 4.0, 16.0):
            v = primary_values(**{r'\rho': theta, r'\varepsilon': 0.5,
                                  r'\Lambda_\Phi': 25 * 4 * (1 + theta)})
            reader = self.reader(v)
            self.assertTrue(reader.region(self.guards['J']))
            too_tight = dict(v, **{r'\Lambda_\Phi': math.nextafter(v[r'\Lambda_\Phi'], -math.inf)})
            self.assertFalse(self.reader(too_tight).region(self.guards['J']))
            above = dict(v, **{r'\varepsilon': math.nextafter(0.5, math.inf)})
            self.assertFalse(self.reader(above).region(self.guards['J']))
        both = primary_values()
        self.assertTrue(self.reader(both).region(self.guards['C']))
        self.assertTrue(self.reader(both).region(self.guards['J']))
        for overrides in [{'L_f': 3.0}, {'L_g': 3.0}, {'C_f': 3.0},
                          {r'\Lambda_\Phi': 1.0}, {r'\rho': 0.0},
                          {r'\rho': 17.0}, {r'\varepsilon': 0.5001}]:
            with self.subTest(overrides=overrides):
                reader = self.reader(primary_values(**overrides))
                self.assertFalse(reader.region(self.guards['J']))
                self.assertFalse(reader.region(self.guards['C']))
        self.assertFalse(self.reader(primary_values(C_F=1.0, **{r'\Lambda_\Phi': 64.0})).region(self.guards['C']))
        self.assertFalse(self.reader(primary_values(**{r'\rho': 5.0, r'\Lambda_\Phi': 512.0})).region(self.guards['C']))

    def test_constant_blocks_require_exact_initialization_and_affine_zero_is_closed(self):
        v = primary_values(**{r'\rho': 0.0, r'\Lambda_\Phi': 64.0})
        self.assertTrue(self.reader(v).region(self.guards['K']))
        self.assertFalse(self.reader(primary_values(R_0=1.0, **{r'\rho': 0.0, r'\Lambda_\Phi': 64.0})).region(self.guards['K']))
        threshold = source_s0(v)
        at = dict(v, **{r'\varepsilon': threshold})
        below = dict(v, **{r'\varepsilon': math.nextafter(threshold, -math.inf)})
        self.assertTrue(self.reader(at).region(self.guards['Z']))
        self.assertFalse(self.reader(at).region(self.guards['A']))
        self.assertFalse(self.reader(below).region(self.guards['Z']))
        self.assertTrue(self.reader(below).region(self.guards['A']))
        # Perfect conditioning permits positive rho and a tighter curvature
        # subclass for the sufficient zero statement, including equality.
        perfect = primary_values(L=2.0, L_f=2.0, L_g=2.0, C_f=2.0,
            **{r'\mu': 2.0, r'\rho': 4.0, r'\Delta': 1.0,
               r'\Lambda_\Phi': 0.5, r'\varepsilon': 2.0})
        self.assertTrue(self.reader(perfect).region(self.guards['Z']))
        perfect[r'\varepsilon'] = math.nextafter(2.0, -math.inf)
        self.assertFalse(self.reader(perfect).region(self.guards['Z']))

    def test_active_q1_cells_route_precedence_and_old_complements_once(self):
        samples = [
            (primary_values(), 'curvature'),
            (primary_values(**{r'\rho': 8.0, r'\Lambda_\Phi': 900.0}), 'joint'),
            (primary_values(**{r'\rho': 0.0, r'\Lambda_\Phi': 64.0}), 'constant_blocks'),
            (primary_values(R_0=1.0, **{r'\rho': 0.0, r'\Lambda_\Phi': 64.0, r'\varepsilon': 1.0}), 'affine_activation'),
            (primary_values(**{r'\Lambda_\Phi': 1.0}), 'remainder'),
            (primary_values(C_f=3.0), 'remainder'),
            (primary_values(**{r'\varepsilon': 0.5001}), 'remainder'),
        ]
        zero = primary_values(**{r'\rho': 0.0, r'\Lambda_\Phi': 64.0})
        zero[r'\varepsilon'] = source_s0(zero)
        samples.append((zero, 'source_zero'))
        q1 = self.p['quantities'][0]['id']
        current = [c for c in self.p['comparisons'] if c['quantity_id'] == q1]
        seen = set()
        for (values, family), E, (S,N) in itertools.product(samples, (False,True), ((False,False),(True,False),(True,True))):
            reader = self.reader(values, E, S, N)
            matches = [c['comparison_id'] for c in current if reader.region(c['regime_id'])]
            if E:
                expected = PP + 'c_effective_zero_20261122'
            elif family in ('curvature','joint'):
                cell = 'old_n' if N else 'old_s_remaining' if S else 'outside_old_s'
                expected = PP + 'c_' + family + '_' + cell + '_20261126'
            elif family == 'remainder':
                cell = 'old_noise_remainder' if N else 'old_source_remainder' if S else 'independent_budget_remainder'
                expected = PP + 'c_' + cell + '_20261126'
            else:
                expected = PP + 'c_' + family + '_20261126'
            with self.subTest(family=family, E=E, S=S, N=N):
                self.assertEqual(matches, [expected])
                seen.update(matches)
        self.assertEqual(seen, {c['comparison_id'] for c in current})

    def test_native_model_guarantee_and_joint_quantity_stay_frozen(self):
        self.assertEqual(canonical_sha(self.p['common_specification']), PRIMARY_COMMON_SHA)
        self.assertEqual(canonical_sha(self.p['views']), PRIMARY_VIEWS_SHA)
        self.assertEqual(canonical_sha(self.p['quantities'][0]), PRIMARY_Q_SHA)
        fixed = next(q for q in self.p['quantities'] if q['id'] == PP + 'q_fixed_structural_accuracy_20261126')
        by_symbol = {p['symbol']: p['id'] for p in self.p['parameters']}
        self.assertEqual(fixed['tracked_parameters'], [by_symbol[r'\varepsilon']])
        self.assertTrue({by_symbol[s] for s in ['L_f','L_g','C_f',r'\Lambda_\Phi',r'\sigma_g',r'\rho']}.issubset(fixed['fixed_parameters']))
        self.assertNotEqual(fixed['id'], self.p['quantities'][0]['id'])

    def test_accuracy_only_comparison_keeps_strict_fixed_tuple_cutoff(self):
        row = self.comparisons[PP + 'c_fixed_structural_accuracy_20261126']
        self.assertNotEqual(row['quantity_id'], self.p['quantities'][0]['id'])
        self.assertTrue(self.reader(primary_values()).region(row['regime_id']))
        self.assertFalse(self.reader(primary_values(**{r'\varepsilon': 0.2})).region(row['regime_id']))
        self.assertFalse(self.reader(primary_values(**{r'\sigma_g': 0.0})).region(row['regime_id']))
        self.assertFalse(self.reader(primary_values(**{r'\Lambda_\Phi': 1.0})).region(row['regime_id']))

    def test_old_eligible_lower_bounds_are_not_dropped_or_routed_outside_their_windows(self):
        old_l = PP + 'b_guarded_source_lower_20261122'
        old_n = PP + 'b_matching_noise_lower_20261122'
        old_u = PP + 'b_effective_upper_20261122'
        for family, cell in itertools.product(('curvature','joint'), ('old_n','old_s_remaining','outside_old_s')):
            row = self.comparisons[PP + 'c_' + family + '_' + cell + '_20261126']
            with self.subTest(family=family, cell=cell):
                self.assertIn(old_u, row['bracket']['upper_refs'])
                lower = set(row['bracket']['lower_refs'])
                self.assertEqual(old_l in lower, cell != 'outside_old_s')
                self.assertEqual(old_n in lower, cell == 'old_n')
                for side in ('upper','lower'):
                    self.assertEqual(set(row['bracket'][side + '_refs']),
                        set(row['bracket']['envelopes'][side]['claim_refs']))
                    for bid in row['bracket'][side + '_refs']:
                        guards = row['bracket']['claim_guards'][bid]
                        self.assertEqual(guards, [{'region_ref': row['regime_id'],
                                                   'predicate_text': row['predicate_text']}])

    def test_old_zero_cell_and_historical_nonzero_cells_keep_frozen_hashes(self):
        zero = PP + 'c_effective_zero_20261122'
        self.assertEqual(canonical_sha(self.comparisons[zero]), PRIMARY_COMPARISON_SHAS[zero])
        history = {entry['comparison']['comparison_id']: entry
                   for entry in self.p['provenance']['comparison_history']}
        for cid, frozen in PRIMARY_COMPARISON_SHAS.items():
            if cid == zero:
                continue
            with self.subTest(comparison=cid):
                self.assertNotIn(cid, self.comparisons)
                self.assertEqual(canonical_sha(history[cid]['comparison']), frozen)
                self.assertEqual(history[cid]['comparison_sha256'], frozen)
                self.assertTrue(set(history[cid]['superseded_by']).issubset(self.comparisons))

    def test_uniform_noise_supremum_is_not_an_infinite_fixed_budget_bracket(self):
        findings = self.p['joint_analysis']['structural_findings_20261126']
        finding = next(x for x in findings if x['kind'] == 'uniform_noise_finiteness_classification')
        self.assertIs(finding['quantity']['ordinary_fixed_sigma_comparison'], False)
        self.assertNotIn(finding['quantity']['id'], {c['quantity_id'] for c in self.p['comparisons']})
        # Equality belongs to the small-gap finite side and is excluded on the
        # large-gap finite side; neither branch is a per-finite-sigma infinity.
        self.assertIn(r'\ge', finding['branches'][0]['finite_iff'])
        self.assertIn('>A', finding['branches'][1]['finite_iff'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
