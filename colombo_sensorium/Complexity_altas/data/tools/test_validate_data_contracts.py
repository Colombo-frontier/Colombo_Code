"""Regression tests for active envelopes and historical proof integrity."""
from copy import deepcopy
import unittest

from validate_data import canonical_hash, validate_comparison_aliases, validate_profile_integrity


KEY_FIELDS = ('setting_id', 'view_id', 'guarantee_id', 'quantity_id',
              'resource_projection_id', 'regime_id')


def comparison(cid, regime='positive'):
    key = dict(zip(KEY_FIELDS, ('example', 'randomized', 'g1', 'q1', 'calls', regime)))
    return {**key, 'comparison_id': cid, 'comparison_key': key,
            'bracket': {'envelopes': {'upper': {'expression_latex': 'O(T)'}}}}


def profile():
    model = {'budget': 2, 'label': 'curvature'}
    return {'setting_id': 'example', 'common_specification': model,
            'comparisons': [comparison('current')], 'provenance': {},
            'proofs': [{'id': 'current_proof', 'premises': [
                {'pointer': '/common_specification', 'sha256': canonical_hash(model)}]}],
            'bounds': [{'id': 'upper', 'included_in_bracket': True,
                        'eligible_for_bracket': True, 'proof_refs': ['current_proof']}],
            'evidence': []}


def retain_history(value):
    old = comparison('old')
    value['provenance']['comparison_history'] = [
        {'comparison': old, 'comparison_sha256': canonical_hash(old),
         'superseded_by': ['current'], 'relation': 'stronger_upper_envelope'}]
    return old


def retain_historical_proof(value):
    # These bytes predate the current model. First observation is explicitly
    # not claimed to be the unavailable original premise snapshot.
    old = {'id': 'old_proof', 'statement': 'Original retained derivation.',
           'premises': [{'pointer': '/common_specification', 'sha256': 'a' * 64}],
           'lifecycle': {'state': 'historical', 'eligible_for_current_bounds': False,
                         'premise_binding': {'mode': 'historical_unresolved',
                                             'verification_status': 'unresolved_snapshot',
                                             'first_observed': {'git_commit': 'b' * 40,
                                                                'profile_sha256': 'c' * 64},
                                             'note': 'The premise snapshot is unavailable.'},
                         'superseded_by': ['current_proof'],
                         'reason': 'Retained for audit, replaced by a current derivation.'}}
    value['proofs'].append(old)
    return old


def research_profile():
    value = profile()
    remaining = comparison('gap', 'remaining')
    predicate = {'all': [{'region_ref': 'positive'}, {'not': {'region_ref': 'closed'}}]}
    remaining.update(predicate=predicate, status={'code': 'polynomial_gap'},
                     research_target={'target_regime_ref': 'positive', 'set_operation': 'difference',
                                      'excluded_closed_comparison_refs': ['closed'],
                                      'remaining_regime_ref': 'remaining', 'predicate': deepcopy(predicate)})
    closed = comparison('closed', 'closed')
    closed['status'] = {'code': 'optimal'}
    value['comparisons'] = [remaining, closed]
    value['regimes'] = [{'id': 'positive', 'predicate': {'cmp': 'gt', 'left': {'ref': 'epsilon'}, 'right': 0}},
                        {'id': 'closed', 'predicate': {'cmp': 'ge', 'left': {'ref': 'epsilon'}, 'right': 1}},
                        {'id': 'remaining', 'predicate': deepcopy(predicate)}]
    value['parameters'] = [{'id': 'epsilon'}]
    return value


def inspect(value, aliases=None):
    errors, warnings = [], []

    def check(kind, okay, message):
        if not okay:
            errors.append((kind, message))

    validate_profile_integrity(value, KEY_FIELDS, check, warnings)
    if aliases is not None:
        validate_comparison_aliases(aliases, {'example': value}, check)
    return errors, warnings


class IntegrityRegressionTests(unittest.TestCase):
    def assertFailure(self, value, category, aliases=None):
        errors, _ = inspect(value, aliases)
        self.assertIn(category, [kind for kind, _ in errors], errors)

    def test_current_binding_uses_canonical_unicode_object(self):
        value = profile()
        value['common_specification'] = {'label': 'curvature', 'budget': 2}
        self.assertEqual(inspect(value), ([], []))

    def test_changing_a_current_premise_is_fatal(self):
        value = profile()
        value['common_specification']['budget'] = 3
        self.assertFailure(value, 'proof_premise_binding')

    def test_missing_and_malformed_pointers_are_fatal(self):
        for pointer in ('/missing', 'common_specification', '/bad~2escape', '/items/-1'):
            with self.subTest(pointer=pointer):
                value = profile()
                value['items'] = [2]
                value['proofs'][0]['premises'][0] = {'pointer': pointer, 'sha256': canonical_hash(2)}
                self.assertFailure(value, 'proof_premise_binding')

    def test_json_pointer_escapes_and_array_indices_resolve(self):
        value = profile()
        value['a/b'] = {'~key': [7]}
        value['proofs'][0]['premises'][0] = {'pointer': '/a~1b/~0key/0', 'sha256': canonical_hash(7)}
        self.assertEqual(inspect(value), ([], []))

    def test_distinct_ids_and_upper_formulas_do_not_avoid_scope_collision(self):
        value = profile()
        duplicate = comparison('weaker')
        duplicate['bracket']['envelopes']['upper']['expression_latex'] = 'O(T squared)'
        value['comparisons'].append(duplicate)
        self.assertFailure(value, 'comparison_scope_unique')

    def test_different_regimes_can_have_independent_active_envelopes(self):
        value = profile()
        value['comparisons'].append(comparison('zero', 'zero'))
        self.assertEqual(inspect(value), ([], []))

    def test_history_retains_old_envelope_without_active_collision(self):
        value = profile()
        retain_history(value)
        before = deepcopy(value)
        self.assertEqual(inspect(value), ([], []))
        self.assertEqual(value, before)

    def test_mutating_archived_comparison_is_fatal(self):
        value = profile()
        old = retain_history(value)
        old['bracket']['envelopes']['upper']['expression_latex'] = 'changed'
        self.assertFailure(value, 'comparison_history_hash')

    def test_history_cannot_reactivate_old_id_or_lose_successor(self):
        for mutation in ('reactivate', 'missing_successor', 'duplicate_history'):
            with self.subTest(mutation=mutation):
                value = profile()
                old = retain_history(value)
                if mutation == 'reactivate':
                    value['comparisons'].append(deepcopy(old))
                elif mutation == 'missing_successor':
                    value['provenance']['comparison_history'][0]['superseded_by'] = ['missing']
                else:
                    value['provenance']['comparison_history'].append(
                        deepcopy(value['provenance']['comparison_history'][0]))
                self.assertFailure(value, 'comparison_history')

    def test_navigation_alias_cannot_target_archived_or_missing_comparison(self):
        value = profile()
        retain_history(value)
        for target in ('old', 'missing'):
            with self.subTest(target=target):
                aliases = {'comparison_aliases': [
                    {'legacy_id': 'legacy', 'setting_id': 'example', 'comparison_id': target}]}
                self.assertFailure(value, 'alias_comparison_links', aliases)

    def test_migrated_alias_can_preserve_old_name_and_route_to_current(self):
        value = profile()
        retain_history(value)
        aliases = {'comparison_aliases': [
            {'legacy_id': 'old', 'setting_id': 'example', 'previous_comparison_id': 'old',
             'comparison_id': 'current'}],
            'comparison_migrations': [
                {'setting_id': 'example', 'old_comparison_id': 'old',
                 'new_comparison_ids': ['current'], 'navigation_default_comparison_id': 'current'}]}
        self.assertEqual(inspect(value, aliases), ([], []))

    def test_unresolved_historical_hash_is_preserved_with_explicit_warning(self):
        value = profile()
        old = retain_historical_proof(value)
        before = deepcopy(old)
        errors, warnings = inspect(value)
        self.assertEqual(errors, [])
        self.assertEqual(old, before)
        self.assertEqual([x['kind'] for x in warnings], ['unresolved_historical_proof_premises'])

    def test_current_or_eligible_bound_cannot_use_historical_proof(self):
        for included, eligible in ((True, False), (False, True), (True, True)):
            with self.subTest(included=included, eligible=eligible):
                value = profile()
                retain_historical_proof(value)
                value['bounds'][0].update(included_in_bracket=included, eligible_for_bracket=eligible,
                                          proof_refs=['old_proof'])
                self.assertFailure(value, 'current_bound_proof')

    def test_inactive_bound_may_keep_historical_support(self):
        value = profile()
        retain_historical_proof(value)
        value['bounds'][0].update(included_in_bracket=False, eligible_for_bracket=False,
                                  proof_refs=['old_proof'])
        self.assertEqual(inspect(value)[0], [])

    def test_evidence_and_transitive_proof_links_cannot_hide_historical_support(self):
        for route in ('evidence', 'proof'):
            with self.subTest(route=route):
                value = profile()
                retain_historical_proof(value)
                if route == 'evidence':
                    value['bounds'][0]['evidence_refs'] = ['e1']
                    value['evidence'] = [{'id': 'e1', 'proof_refs': ['old_proof']}]
                else:
                    value['proofs'][0]['proof_refs'] = ['old_proof']
                self.assertFailure(value, 'current_bound_proof')

    def test_historical_label_requires_honest_unresolved_binding_and_current_successor(self):
        for mutation in ('eligible', 'binding', 'successor'):
            with self.subTest(mutation=mutation):
                value = profile()
                old = retain_historical_proof(value)
                if mutation == 'eligible':
                    old['lifecycle']['eligible_for_current_bounds'] = True
                elif mutation == 'binding':
                    old['lifecycle']['premise_binding']['verification_status'] = 'verified'
                else:
                    old['lifecycle']['superseded_by'] = ['missing']
                category = 'proof_historical_binding' if mutation == 'binding' else 'proof_lifecycle'
                self.assertFailure(value, category)

    def test_malformed_lifecycle_state_fails_without_crashing_validator(self):
        value = profile()
        value['proofs'][0]['lifecycle'] = {'state': {'unsupported': 'historical'}}
        self.assertFailure(value, 'proof_lifecycle')

    def test_remaining_research_region_has_static_difference_contract(self):
        self.assertEqual(inspect(research_profile()), ([], []))

    def test_research_target_and_remaining_predicate_cannot_diverge(self):
        for mutation in ('comparison', 'regime'):
            with self.subTest(mutation=mutation):
                value = research_profile()
                if mutation == 'comparison':
                    value['comparisons'][0]['predicate'] = {'region_ref': 'positive'}
                else:
                    value['regimes'][-1]['predicate'] = {'region_ref': 'positive'}
                self.assertFailure(value, 'research_target_predicate')

    def test_research_target_foreign_keys_must_resolve(self):
        for field in ('target_regime_ref', 'remaining_regime_ref', 'excluded_closed_comparison_refs'):
            with self.subTest(field=field):
                value = research_profile()
                value['comparisons'][0]['research_target'][field] = ['missing'] if field.startswith('excluded') else 'missing'
                self.assertFailure(value, 'research_target_links')

    def test_research_target_cannot_subtract_an_open_or_different_scope_comparison(self):
        for mutation in ('open', 'other_quantity'):
            with self.subTest(mutation=mutation):
                value = research_profile()
                closed = value['comparisons'][1]
                if mutation == 'open':
                    closed['status']['code'] = 'missing_lower'
                else:
                    closed['comparison_key']['quantity_id'] = 'another_quantity'
                category = 'research_target_closed' if mutation == 'open' else 'research_target_scope'
                self.assertFailure(value, category)

    def test_research_target_predicate_foreign_keys_are_checked(self):
        value = research_profile()
        predicate = {'not': {'region_ref': 'missing'}}
        value['comparisons'][0]['predicate'] = deepcopy(predicate)
        value['comparisons'][0]['research_target']['predicate'] = deepcopy(predicate)
        value['regimes'][-1]['predicate'] = deepcopy(predicate)
        self.assertFailure(value, 'research_target_links')


if __name__ == '__main__':
    unittest.main()
