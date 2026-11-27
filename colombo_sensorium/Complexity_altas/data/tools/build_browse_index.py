#!/usr/bin/env python3
"""Build a small, audited semantic browse layer without editing source data.

Fine-grained source classifications remain the advanced index. This layer
normalizes common concepts and records each normalization/inheritance rule.
Missing facts remain unknown. Filtering is OR within a group, AND across
groups, and must be satisfied by one and the same algorithm view.
"""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
import pathlib
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone

DATA = pathlib.Path(__file__).resolve().parents[1]
VERSION = '1.0.0'
AXES = [
    ('TASK', 'Task', True, 'Mathematical task family; not a loss, success probability, or oracle capability.'),
    ('MODEL', 'Model', True, 'Promises on the objective, payoff, or operator. Convex feasible sets and convex lower-level objectives are not automatically convex target objectives.'),
    ('ORACLE', 'Oracle', True, 'Declared primitive oracle interface. Public geometric auxiliaries do not determine the quality of the unknown-object feedback.'),
    ('ALGORITHMS', 'Algorithms', False, 'The algorithm class in this specific view; absence of a restriction is not a permission.'),
    ('OUTPUT', 'Output', False, 'The returned object, independently of its error criterion.'),
    ('METRIC', 'Metric', False, 'Broad performance-criterion families. Exact formulas and distinctions remain in the profile and advanced source tags.'),
    ('GUARANTEE', 'Guarantee', False, 'Correctness or performance-error guarantee, independently of expected runtime or query cost.'),
    ('RESOURCE', 'Resource', False, 'Principal charged resource and budget interpretation; auxiliary recorded coordinates do not automatically become the principal cost.'),
]

# Each definition is global. The browser displays these concepts, not hundreds
# of literal property codes. Aliases are whole phrases, never substrings.
GROUPS = {
    ('TASK', 'family'): ('Task family', 'The task navigation families explicitly declared by the source.'),
    ('MODEL', 'objective_convexity'): ('Objective convexity', 'Convexity of the same objective being minimized (or per-round loss). Strong convexity implies convexity on that same domain. This excludes only-convex feasible sets and only-convex lower-level g in a bilevel problem.'),
    ('MODEL', 'structure'): ('Problem structure', 'Declared payoff, finite-sum or composite structure, without asserting a different objective or oracle.'),
    ('MODEL', 'monotonicity'): ('Operator monotonicity', 'Monotonicity of the declared target operator. Strong monotonicity implies monotonicity for that same operator.'),
    ('ORACLE', 'access'): ('Oracle access', 'For scalar primitives, the highest declared derivative-access family: zeroth order includes derivative-free value, component-value and comparison replies, not only full values. Operator/matrix and online protocols are named separately when no scalar order is normalized. Vector-operator order zero is not scalar-objective zeroth order. Exact parameterized orders remain in advanced detail.'),
    ('ORACLE', 'quality'): ('Primitive feedback quality', 'Quality of the unknown-object primitive feedback. Exact means deterministic exact replies from the fixed hidden function/operator/loss. Exact evaluation of a sampled function is still sampled feedback. Mixed means explicitly different qualities among primitive replies; exact public projection/prox auxiliaries are excluded.'),
    ('ALGORITHMS', 'randomization'): ('Randomization', 'Private randomization allowed or a deterministic class explicitly required in this same view.'),
    ('OUTPUT', 'object'): ('Returned object', 'Broad returned-object types only; feasibility, certificates, positive radii and support restrictions remain in advanced detail.'),
    ('METRIC', 'goal'): ('Performance criterion', 'Broad mathematical error families. Selecting a family does not equate its different norms, residuals, probability aggregations or accuracy parameters.'),
    ('GUARANTEE', 'error_mode'): ('Error guarantee', 'How correctness or performance error is controlled. Expected query/stopping cost is not an expected-error guarantee; exact and almost-sure special contracts remain in advanced detail.'),
    ('RESOURCE', 'measure'): ('Cost / budget family', 'The main compared cost or native budget family. Scalar/component/matrix-vector calls, time rounds and joint coordinates remain distinct in the profile; recorded uncharged auxiliaries never determine this option.'),
}
OPTIONS = {}


def option(axis, group, value, name, aliases, description):
    tid = ':'.join([axis, group, value])
    OPTIONS[tid] = {'id': tid, 'axis': axis, 'group': group, 'group_id': axis + ':' + group,
                    'value': value, 'label': name, 'aliases': aliases, 'description': description}


for value, name, aliases in [
    ('single_objective', 'Single objective', ['single objective', 'single-objective']),
    ('bilevel', 'Bilevel', ['bilevel', 'bi-level']),
    ('minimax', 'Minimax', ['minimax', 'min-max']),
    ('variational_inequality', 'Variational inequality', ['variational inequality', 'vi']),
    ('matrix_computation', 'Matrix computation', ['matrix computation']),
    ('online_bandit', 'Online learning / bandits', ['online learning', 'bandit', 'bandits']),
]:
    option('TASK', 'family', value, name, aliases, 'Source-declared task family: ' + name + '.')
for value, name, aliases, desc in [
    ('convex', 'Convex objective', ['convex', 'convex objective'], 'Same-target convexity, including certified same-target strong convexity; not merely convex geometry or a convex lower problem.'),
    ('strongly_convex', 'Strongly convex objective', ['strongly convex', 'strongly-convex', 'strongly convex objective'], 'Strong convexity of the target objective on its declared domain.'),
    ('weakly_convex', 'Weakly convex objective', ['weakly convex', 'weakly-convex'], 'Explicit weak-convexity promise on the target objective.'),
    ('not_assumed', 'Convexity not assumed', ['nonconvex', 'non-convex', 'convexity not assumed'], 'Convexity is explicitly not promised; this does not assert that every individual function is nonconvex.'),
]:
    option('MODEL', 'objective_convexity', value, name, aliases, desc)
for value, name, aliases in [
    ('convex_concave', 'Convex–concave payoff', ['convex concave', 'convex-concave'],),
    ('nonconvex_strongly_concave', 'Nonconvex–strongly concave class', ['nonconvex strongly concave', 'nonconvex-strongly-concave']),
    ('finite_sum', 'Finite sum', ['finite sum', 'finite-sum']),
    ('composite', 'Composite objective', ['composite objective', 'composite']),
]:
    option('MODEL', 'structure', value, name, aliases, 'Explicit source-declared structure: ' + name + '.')
for value, name, aliases in [
    ('monotone', 'Monotone operator', ['monotone operator', 'monotone']),
    ('strongly_monotone', 'Strongly monotone operator', ['strongly monotone', 'strongly-monotone']),
]:
    option('MODEL', 'monotonicity', value, name, aliases, 'Applies to the declared target operator; no scalar-potential assumption is inferred.')
for value, name, aliases in [
    ('zero', 'Zeroth-order interface', ['zeroth order', 'zeroth-order', 'zero order', 'zeroth-order interface']),
    ('first', 'First-order interface', ['first order', 'first-order', 'first-order interface']),
    ('higher', 'Higher-order interface', ['higher order', 'higher-order', 'high order', 'higher-order interface']),
    ('operator_matrix', 'Operator / matrix interface', ['operator interface', 'matrix interface']),
    ('online_feedback', 'Online feedback protocol', ['online feedback']),
]:
    option('ORACLE', 'access', value, name, aliases, GROUPS[('ORACLE', 'access')][1])
for value, name, aliases in [
    ('exact', 'Exact', ['exact', 'noiseless feedback']),
    ('stochastic', 'Stochastic / sampled', ['stochastic', 'sampled', 'stochastic feedback', 'sampled feedback']),
    ('inexact', 'Inexact / biased', ['inexact', 'biased feedback']),
    ('mixed', 'Mixed primitive qualities', ['mixed primitive qualities', 'mixed feedback']),
]:
    option('ORACLE', 'quality', value, name, aliases, GROUPS[('ORACLE', 'quality')][1])
for value, name, aliases in [
    ('deterministic', 'Deterministic algorithms', ['deterministic algorithms', 'deterministic algorithm']),
    ('randomized', 'Randomization allowed', ['randomized algorithms', 'randomized']),
]:
    option('ALGORITHMS', 'randomization', value, name, aliases, GROUPS[('ALGORITHMS', 'randomization')][1])
for value, name, aliases in [
    ('point_vector', 'Point / vector / point pair', ['point output', 'vector output']),
    ('matrix_subspace', 'Matrix / subspace', ['matrix output', 'subspace output']),
    ('trajectory', 'Action trajectory', ['action trajectory', 'online trajectory']),
]:
    option('OUTPUT', 'object', value, name, aliases, GROUPS[('OUTPUT', 'object')][1])
for value, name, aliases in [
    ('objective_gap', 'Objective gap', ['objective gap', 'function gap']),
    ('first_order_stationarity', 'First-order stationarity', ['first-order stationarity', 'first order stationarity', 'reduced gradient']),
    ('higher_order_stationarity', 'Higher-order stationarity', ['second-order stationarity', 'higher-order stationarity']),
    ('saddle_gap', 'Saddle-point gap', ['saddle gap', 'saddle-point gap']),
    ('variational_gap_residual', 'Variational gap / residual', ['tangent residual', 'operator residual', 'variational gap']),
    ('distance', 'Solution distance', ['solution distance', 'distance error']),
    ('regret', 'Regret', ['regret']),
    ('matrix_accuracy', 'Matrix / linear-system accuracy', ['matrix accuracy', 'linear-system error']),
    ('identification', 'Identification / decision error', ['identification error', 'decision error']),
]:
    option('METRIC', 'goal', value, name, aliases, GROUPS[('METRIC', 'goal')][1])
for value, name, aliases in [
    ('deterministic', 'Deterministic error guarantee', ['deterministic guarantee']),
    ('expectation', 'Expected-error guarantee', ['expected error', 'expectation guarantee']),
    ('probability', 'Probability guarantee', ['probability guarantee', 'high probability', 'fixed confidence']),
]:
    option('GUARANTEE', 'error_mode', value, name, aliases, GROUPS[('GUARANTEE', 'error_mode')][1])
for value, name, aliases in [
    ('oracle_calls', 'Oracle calls', ['oracle calls', 'query calls']),
    ('samples', 'Samples', ['sample complexity', 'samples']),
    ('rounds', 'Time rounds', ['time rounds', 'horizon']),
    ('arithmetic', 'Arithmetic work', ['arithmetic work', 'arithmetic complexity']),
    ('memory', 'Memory', ['memory complexity', 'memory']),
    ('joint', 'Joint resource budget', ['joint budget', 'joint resources']),
]:
    option('RESOURCE', 'measure', value, name, aliases, GROUPS[('RESOURCE', 'measure')][1])

EXACT_CODES = {'exact', 'exact_function_value', 'exact_function_values', 'exact_gradient', 'exact_loss_vector',
               'exact_selected_loss', 'exact_scalar_projection'}
STOCHASTIC_CODES = {'fresh', 'sample', 'value_sample', 'iid_bounded_reward', 'gaussian_additive_noise',
                    'bounded_nonstationary_reward', 'independent_nonstationary_bounded_reward',
                    'conditional_variance_sigma', 'stochastic_unbiased_bounded_variance',
                    'noisy_function_value', 'exact_values_of_same_random_function',
                    'conditionally_unbiased_e_noise_2_past_query_sigma_2',
                    'unbiased_conditional_on_query_history_conditional_squared_noise_norm_sigma',
                    'e_sample_f_z_b_z_z0_sigma'}
INEXACT_CODES = {'biased', 'inexact', 'bounded_adversarial', 'deterministic_roundoff', 'relative_roundoff'}
AUXILIARY_OPERATIONS = {'projection', 'known_prox', 'known_resolvent', 'linear_minimization', 'public_scalar_function_evaluation'}
ZERO_NATIVE = {'exact_value', 'selected_component_value', 'independent_noisy_value', 'same_sample_paired_value',
               'reusable_sample_value', 'exact_comparison', 'noisy_comparison', 'biased_adversarial_noisy_value',
               'markov_single_value', 'markov_same_state_paired_value'}
SCALAR_ZERO_OPERATIONS = {'function_value', 'sample_function_value', 'payoff_value', 'evaluate_same_sample_pair',
                          'evaluate_loss_at_action', 'two_point_exact', 'two_point_independent_noise'}
SCALAR_FIRST_OPERATIONS = {'primitive_gradient', 'partial_gradient', 'block_gradient', 'joint_primitive_gradient_response',
                           'reduced_objective_gradient', 'stochastic_joint_gradient', 'payoff_joint_gradient',
                           'payoff_value_joint_gradient', 'stochastic_value_joint_gradient', 'component_gradient',
                           'component_joint_gradient', 'component_value_joint_gradient', 'sample_gradient',
                           'query_gradient_at_action', 'action_gradient', 'complete_subgradient'}
SCALAR_HIGHER_OPERATIONS = {'cross_derivative_vector_product', 'hessian_vector_product',
                            'payoff_value_gradient_full_hessian', 'payoff_complete_jet'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(value):
    return re.sub(r'[^a-z0-9]+', '_', str(value).lower()).strip('_')


def token(value):
    return str(value).replace('~', '~0').replace('/', '~1')


def walk(value, pointer=''):
    yield pointer, value
    if isinstance(value, dict):
        for key, item in value.items():
            yield from walk(item, pointer + '/' + token(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk(item, pointer + '/' + str(index))


def resolve(value, pointer):
    for key in pointer.lstrip('/').split('/') if pointer else []:
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def merge(base, patch, bp, pp):
    if isinstance(base, dict) and isinstance(patch, dict):
        result, pointers = {}, {'': bp}
        for key in dict.fromkeys(list(base) + list(patch)):
            suffix = '/' + token(key)
            if key in base and key in patch:
                item, children = merge(base[key], patch[key], bp + suffix, pp + suffix)
            else:
                item = copy.deepcopy(patch[key] if key in patch else base[key])
                source = pp + suffix if key in patch else bp + suffix
                children = {pointer: source + pointer for pointer, _ in walk(item)}
            result[key] = item
            pointers.update({suffix + pointer: source for pointer, source in children.items()})
        return result, pointers
    result = copy.deepcopy(patch)
    return result, {pointer: pp + pointer for pointer, _ in walk(result)}


class BrowseView:
    def __init__(self, profile, classification, view, index):
        self.p, self.c, self.view = profile, classification, view
        self.vid = view['view_id']
        self.effective, self.origins = merge(profile['common_specification'], view.get('specification_overrides', {}),
                                              '/common_specification', '/views/' + str(index) + '/specification_overrides')
        self.facts, self.unknown = {}, {}
        self.precise = [tag for tag in classification['tags'] if self.vid in tag['view_ids']]

    def src(self, suffix):
        return self.origins[suffix]

    def emit(self, tid, pointers, rule_id, explanation, derived=False, context=None):
        definition = OPTIONS[tid]
        pointers = list(dict.fromkeys(pointers))
        for pointer in pointers:
            resolve(self.p, pointer)
        refs = [tag['id'] for tag in self.precise
                if any(pointer in tag['source_pointers'] for pointer in pointers)]
        evidence = {'source_pointers': pointers, 'precise_tag_refs': refs, 'rule_id': rule_id,
                    'explanation': explanation, 'derived': derived}
        if context:
            evidence['scope'] = context
        fact = self.facts.setdefault(tid, {key: definition[key] for key in ['id', 'axis', 'group', 'group_id', 'value', 'label']}
                                     | {'source_pointers': [], 'precise_tag_refs': [], 'rule_id': rule_id,
                                        'explanation': explanation, 'evidence': []})
        for key, values in [('source_pointers', pointers), ('precise_tag_refs', refs)]:
            fact[key] = list(dict.fromkeys(fact[key] + values))
        if evidence not in fact['evidence']:
            fact['evidence'].append(evidence)
        self.unknown.pop(definition['group_id'], None)

    def source_tag(self, tid, target, rule, explanation, derived=False):
        for tag in self.precise:
            if tag['id'] == tid:
                evidence = [entry for entry in tag['evidence'] if self.vid in entry['view_ids']]
                pointers = [entry['source_pointer'] for entry in evidence]
                scopes = [entry['context'] for entry in evidence if entry.get('context')]
                self.emit(target, pointers, rule, explanation, derived,
                          {'source_scopes': scopes} if scopes else None)

    def build(self):
        self.emit('TASK:family:' + self.p['primary_domain'], ['/primary_domain'], 'task.primary_family',
                  'Task family is explicitly recorded in primary_domain.')
        task = self.effective.get('task', {})
        for index, family in enumerate(task.get('navigation_domains', [])):
            if 'TASK:family:' + family in OPTIONS:
                self.emit('TASK:family:' + family, [self.src('/task/navigation_domains/' + str(index))],
                          'task.navigation_family', 'The task explicitly declares this navigation family.')
        self.model()
        self.access()
        self.quality()
        self.more_filters()
        facets = sorted(self.facts.values(), key=lambda item: item['id'])
        for axis, group in GROUPS:
            if not any(fact['group_id'] == axis + ':' + group for fact in facets):
                self.unknown.setdefault(axis + ':' + group, 'No safely normalized fact; consult source/advanced detail.')
        return {'view_id': self.vid, 'label': self.view['label'], 'facet_ids': [item['id'] for item in facets],
                'facets': facets, 'unknown_groups': self.unknown}

    def model(self):
        obj = self.effective.get('model', {})
        family = self.p['primary_domain']
        convex_records = []
        if family == 'single_objective':
            cv = obj.get('convexity')
            if isinstance(cv, dict) and cv.get('code'):
                convex_records.append((cv['code'], self.src('/model/convexity/code')))
            if isinstance(obj.get('properties'), dict) and obj['properties'].get('convexity'):
                convex_records.append((obj['properties']['convexity'], self.src('/model/properties/convexity')))
        if family == 'bilevel':
            # The explicitly named reduced objective is the target, not g(x,y).
            for field in ['outer_geometry', 'reduced_geometry']:
                value = str(obj.get(field, ''))
                if value in ['The reduced objective is strongly convex.', 'Phi is mu_x-strongly convex']:
                    convex_records.append(('strongly_convex', self.src('/model/' + field)))
                elif value in ['The reduced objective is convex.', r'Convex $\Phi$']:
                    convex_records.append(('convex', self.src('/model/' + field)))
                elif value.startswith('The reduced objective may be nonconvex.'):
                    convex_records.append(('not_assumed', self.src('/model/' + field)))
        if family == 'online_bandit':
            for index, assumption in enumerate(obj.get('assumptions', [])):
                if (isinstance(assumption, dict) and assumption.get('property_code') == 'convex_in_action'
                        and not re.search(r'not assumed|not required|need not', str(assumption.get('description', '')).lower())):
                    convex_records.append(('convex', self.src('/model/assumptions/' + str(index) + '/property_code')))
        positive = {'convex', 'strongly_convex', 'weakly_convex', 'not_assumed', 'general',
                    'strongly_convex_average_with_convex_components', 'strongly_convex_on_feasible_ball',
                    'strongly_convex_composite_with_convex_components'}
        for value, pointer in convex_records:
            if value not in positive:
                self.unknown['MODEL:objective_convexity'] = 'Structured convexity is scoped to components or requires a reviewed composition rule: ' + value
                continue
            normalized = 'not_assumed' if value == 'general' else 'strongly_convex' if value.startswith('strongly_convex') else value
            context = {'target': 'reduced_objective' if family == 'bilevel' else 'current_per_round_loss' if family == 'online_bandit' else 'minimized_objective',
                       'domain': obj.get('domain_roles', {}).get('optimization', 'as declared by the model')}
            self.emit('MODEL:objective_convexity:' + normalized, [pointer], 'model.target_convexity',
                      'The source promise applies to the actual target objective on the stated domain.', context=context)
            if normalized == 'strongly_convex':
                self.emit('MODEL:objective_convexity:convex', [pointer], 'model.strong_convexity_implies_convexity',
                          'Strong convexity implies convexity for this same target objective and domain; no promise is transferred from lower g or from a convex feasible set.', True, context)
        if family == 'single_objective':
            self.source_tag('MODEL:convexity:weakly_convex', 'MODEL:objective_convexity:weakly_convex',
                            'model.declared_target_weak_convexity', 'The single-objective source explicitly declares weak convexity; this does not grant ordinary convexity.')
            properties = obj.get('properties', {})
            if properties.get('convexity') == 'convex_components' and 'finite_sum' in properties.get('structure', []):
                for index, paragraph in enumerate(obj.get('description_paragraphs', [])):
                    if paragraph.startswith(r'$F(x)=n^{-1}\sum_{i=1}^n f_i(x)$'):
                        self.emit('MODEL:objective_convexity:convex',
                                  [self.src('/model/properties/convexity'), self.src('/model/properties/structure'),
                                   self.src('/model/description_paragraphs/' + str(index))],
                                  'model.convex_component_average_implies_convex_target',
                                  'The source explicitly defines the minimized F as the positive average of convex f_i. A positive average is convex on the same optimization domain; this is not an inference from convex geometry or lower-level g.',
                                  True, {'target': 'F_positive_component_average', 'domain': obj.get('domain_roles', {}).get('optimization', 'declared domain')})
        for tag, target in [
            ('MODEL:structure:finite_sum', 'MODEL:structure:finite_sum'),
            ('MODEL:structure:composite', 'MODEL:structure:composite'),
            ('MODEL:structure:structured_composite', 'MODEL:structure:composite'),
            ('MODEL:convexity:convex_composite', 'MODEL:structure:composite'),
            ('MODEL:convexity:known_convex_regularizer', 'MODEL:structure:composite'),
            ('MODEL:convexity:convex_concave', 'MODEL:structure:convex_concave'),
            ('MODEL:convexity:nonconvex_strongly_concave', 'MODEL:structure:nonconvex_strongly_concave'),
        ]:
            self.source_tag(tag, target, 'model.declared_structure', 'This broad structure is explicitly supported by the scoped source classification.')
        self.source_tag('MODEL:convexity:strongly_convex_strongly_concave', 'MODEL:structure:convex_concave',
                        'model.strong_saddle_implies_convex_concave', 'The same payoff is strongly convex in its primal block and strongly concave in its dual block, hence convex–concave.', True)
        for tag in ['MODEL:monotonicity:monotone', 'MODEL:monotonicity:average_monotone']:
            self.source_tag(tag, 'MODEL:monotonicity:monotone', 'model.declared_monotone', 'The target operator or explicitly declared average operator is monotone.')
        for tag in ['MODEL:monotonicity:strong_monotonicity', 'MODEL:monotonicity:strongly_monotone']:
            self.source_tag(tag, 'MODEL:monotonicity:strongly_monotone', 'model.declared_strong_monotone', 'Strong monotonicity is explicitly promised for the declared target operator.')
            self.source_tag(tag, 'MODEL:monotonicity:monotone', 'model.strong_monotonicity_implies_monotonicity', 'Strong monotonicity implies monotonicity for that same declared operator.', True)

    def access(self):
        oracle = self.effective.get('oracle', {})
        code = oracle.get('code')
        if code in ZERO_NATIVE:
            self.emit('ORACLE:access:zero', [self.src('/oracle/code')], 'oracle.native_scalar_value_or_comparison',
                      'The native interface explicitly supplies scalar function-value or comparison observations, without a derivative response.')
            return
        if code in ['first_order', 'higher_order']:
            self.emit('ORACLE:access:' + ('first' if code == 'first_order' else 'higher'), [self.src('/oracle/code')],
                      'oracle.declared_access_family', 'The source explicitly declares this scalar derivative-access family; exact order and primitive objects remain in advanced detail.')
            return
        kinds = []
        for index, operation in enumerate(oracle.get('operations', [])):
            if not isinstance(operation, dict) or operation.get('operation_code') in AUXILIARY_OPERATIONS:
                continue
            name = operation.get('operation_code')
            pointer = self.src('/oracle/operations/' + str(index) + '/operation_code')
            if name in SCALAR_HIGHER_OPERATIONS:
                kinds.append((2, pointer))
            elif name in SCALAR_FIRST_OPERATIONS:
                kinds.append((1, pointer))
            elif name in SCALAR_ZERO_OPERATIONS:
                kinds.append((0, pointer))
        if kinds:
            highest = max(value for value, _ in kinds)
            self.emit('ORACLE:access:' + ['zero', 'first', 'higher'][highest], [pointer for value, pointer in kinds if value == highest],
                      'oracle.scalar_primitive_access', 'This is the highest explicitly named scalar primitive access family. Vector-operator values and matrix products are excluded, and the named primitive is not silently replaced by a reduced objective.')
        else:
            operator_pointers = [self.src('/oracle/operations/' + str(index) + '/operation_code')
                                 for index, operation in enumerate(oracle.get('operations', []))
                                 if isinstance(operation, dict) and operation.get('operation_code') not in AUXILIARY_OPERATIONS
                                 and re.search(r'operator|matrix|matvec|resolvent|explicit_matrix|stream', operation.get('operation_code', ''))]
            online_pointers = [self.src('/oracle/operations/' + str(index) + '/operation_code')
                               for index, operation in enumerate(oracle.get('operations', []))
                               if self.p['primary_domain'] == 'online_bandit' and isinstance(operation, dict)
                               and operation.get('operation_code') not in AUXILIARY_OPERATIONS]
            if operator_pointers:
                self.emit('ORACLE:access:operator_matrix', operator_pointers, 'oracle.nonscalar_operator_matrix_interface',
                          'The declared primitive returns or acts on a vector operator/matrix. An operator value of order zero is not converted into a scalar-function zeroth-order oracle.')
            elif online_pointers:
                self.emit('ORACLE:access:online_feedback', online_pointers, 'oracle.declared_online_feedback',
                          'The explicitly named operation follows an online action/feedback protocol; no scalar derivative order is inferred from task family alone.')
            else:
                self.unknown['ORACLE:access'] = 'No normalized scalar-derivative family or reviewed operator/matrix/online operation; exact native operations remain in advanced detail.'

    def quality(self):
        oracle = self.effective.get('oracle', {})
        code = oracle.get('code')
        code_quality = {'exact_value': 'exact', 'selected_component_value': 'exact', 'exact_comparison': 'exact',
                        'independent_noisy_value': 'stochastic', 'same_sample_paired_value': 'stochastic',
                        'reusable_sample_value': 'stochastic', 'noisy_comparison': 'stochastic',
                        'markov_single_value': 'stochastic', 'markov_same_state_paired_value': 'stochastic',
                        'biased_adversarial_noisy_value': 'inexact'}
        if code in code_quality:
            self.emit('ORACLE:quality:' + code_quality[code], [self.src('/oracle/code')], 'oracle.native_quality',
                      'The reviewed native interface code explicitly fixes population feedback quality. Exact sampled-function evaluations are kept stochastic rather than treated as noiseless population values.')
            return
        feedback = oracle.get('feedback', {})
        if isinstance(feedback, dict) and feedback.get('accuracy') in ['exact', 'stochastic', 'inexact', 'biased']:
            accuracy, kind = feedback['accuracy'], feedback.get('kind')
            value = {'exact': 'exact', 'stochastic': 'stochastic', 'inexact': 'inexact', 'biased': 'inexact'}[accuracy]
            pointers = [self.src('/oracle/feedback/accuracy')]
            if kind in ['inexact_hessian', 'value_with_biased_derivatives']:
                paragraph_hits = [(index, paragraph) for index, paragraph in enumerate(oracle.get('description_paragraphs', []))
                                  if 'The first two entries are exact' in paragraph or 'Each reply additionally includes the exact' in paragraph]
                if paragraph_hits:
                    value = 'mixed'
                    pointers += [self.src('/oracle/feedback/kind')] + [self.src('/oracle/description_paragraphs/' + str(index)) for index, _ in paragraph_hits]
            self.emit('ORACLE:quality:' + value, pointers, 'oracle.structured_primary_accuracy',
                      'This accuracy field describes the primary unknown-object response. A separate exact projection/prox does not alter it; a mixed bundle is declared only when exact and inexact components are both explicitly stated.')
            return
        qualities, pointers, unknown = [], [], []
        for index, operation in enumerate(oracle.get('operations', [])):
            if not isinstance(operation, dict):
                unknown.append('natural_language_operation')
                continue
            name = operation.get('operation_code')
            if name in AUXILIARY_OPERATIONS:
                continue
            quality = operation.get('feedback_quality', {})
            qcode = norm(quality.get('code'))
            pointer = self.src('/oracle/operations/' + str(index) + '/feedback_quality/code') if quality.get('code') is not None else None
            value = None
            if qcode in EXACT_CODES:
                value = 'stochastic' if name in ['sample_function_value', 'sample_gradient'] else 'exact'
            elif qcode in STOCHASTIC_CODES:
                value = 'stochastic'
            elif qcode in INEXACT_CODES:
                value = 'inexact'
            elif qcode == 'exact_value_plus_gradient_variance_sigma':
                value = 'mixed'
            elif qcode == 'exact_feedback':
                response = str(operation.get('response_signature', ''))
                if re.search(r'Y_t=\\ell_t\(a_t\)', response):
                    value = 'exact'
                elif r'\mathbb P' in response or r'\sim\mathcal N' in response or r'\sim\mathcal N' in response.replace(' ', ''):
                    value = 'stochastic'
                if value:
                    pointers.append(self.src('/oracle/operations/' + str(index) + '/response_signature'))
            if value:
                qualities.append(value)
                if pointer:
                    pointers.append(pointer)
            else:
                unknown.append(str(name) + ':' + qcode)
        if qualities and not unknown:
            value = qualities[0] if len(set(qualities)) == 1 else 'mixed'
            self.emit('ORACLE:quality:' + value, pointers, 'oracle.primitive_quality_aggregation',
                      'Quality is normalized over all supported non-geometric primitive replies. Fixed current-loss observations may be exact, while sampled values/rewards remain stochastic; exact public auxiliaries are excluded.')
        else:
            self.unknown['ORACLE:quality'] = 'Primitive quality is not fully normalized; no Exact inference is made from a geometric auxiliary or from ambiguous exact_feedback. ' + '; '.join(unknown)

    def more_filters(self):
        for source, target in [
            ('ALGORITHMS:randomization:deterministic', 'ALGORITHMS:randomization:deterministic'),
            ('ALGORITHMS:randomization:private_randomness_allowed', 'ALGORITHMS:randomization:randomized'),
            ('GUARANTEE:mode:deterministic', 'GUARANTEE:error_mode:deterministic'),
            ('GUARANTEE:mode:expectation', 'GUARANTEE:error_mode:expectation'),
            ('GUARANTEE:mode:probability', 'GUARANTEE:error_mode:probability'),
            ('GUARANTEE:mode:fixed_confidence_identification', 'GUARANTEE:error_mode:probability'),
        ]:
            self.source_tag(source, target, 'browse.scoped_contract_normalization',
                            'The coarse option is a normalization of this same view’s explicit source contract; no cost expectation is treated as expected performance error.')
        objects = {
            'point': 'point_vector', 'vector': 'point_vector', 'primal_point': 'point_vector',
            'primal_dual_pair': 'point_vector', 'point_pair': 'point_vector', 'outer_point': 'point_vector',
            'outer_point_x_hat': 'point_vector', 'feasible_point': 'point_vector', 'unit_vector': 'point_vector',
            'node_points': 'point_vector', 'point_with_positive_radius': 'point_vector',
            'point_with_orderwise_positive_radii': 'point_vector', 'point_operator_certificate': 'point_vector',
            'matrix': 'matrix_subspace', 'structured_matrix': 'matrix_subspace',
            'orthogonal_projector': 'matrix_subspace', 'orthogonal_projector_or_basis': 'matrix_subspace',
            'matrix_in_finite_family': 'matrix_subspace', 'matrix_in_linear_space': 'matrix_subspace',
            'orthonormal_block': 'matrix_subspace', 'action_trajectory': 'trajectory',
            'online_trajectory': 'trajectory', 'online_scalar_sequence': 'trajectory',
        }
        first_stationarity = {'gradient_norm', 'first_order_stationarity', 'reduced_gradient',
                              'reduced_stationarity', 'moreau_envelope_gradient', 'gradient_mapping', 'goldstein_stationarity',
                              'prox_goldstein_stationarity', 'prox_gradient_stationarity', 'goldstein_normal_cone_stationarity',
                              'goldstein_frank_wolfe_stationarity', 'weighted_joint_gradient', 'game_stationarity'}
        variational = {'tangent_residual', 'weak_gap', 'root_residual', 'graph_residual', 'resolvent_displacement'}
        distances = {'distance', 'squared_distance', 'weighted_squared_distance', 'principal_angle_error', 'subspace_containment_error'}
        for tag in self.precise:
            value = tag['value']
            if tag['axis'] == 'OUTPUT' and tag['group'] == 'object' and value in objects:
                self.source_tag(tag['id'], 'OUTPUT:object:' + objects[value], 'browse.output_object_family',
                                'Only the returned-object family is grouped; the exact output and certificate restrictions remain in the source.')
            if tag['axis'] != 'METRIC' or tag['group'] != 'criterion':
                continue
            target = ('objective_gap' if value in {'objective_gap', 'function_gap', 'quadratic_energy_loss', 'fixed_budget_gap_risk'}
                      else 'first_order_stationarity' if value in first_stationarity
                      else 'higher_order_stationarity' if value == 'second_order_stationarity'
                      else 'saddle_gap' if value == 'saddle_gap'
                      else 'variational_gap_residual' if value in variational
                      else 'distance' if value in distances
                      else 'regret' if 'regret' in value
                      else 'identification' if value in {'fixed_confidence_identification', 'fixed_budget_error', 'exact_rank_decision', 'exact_symmetry_decision', 'relative_error_exponent'}
                      else 'matrix_accuracy' if self.p['primary_domain'] == 'matrix_computation' and value != 'arithmetic_exponent'
                      else None)
            if target:
                self.source_tag(tag['id'], 'METRIC:goal:' + target, 'browse.metric_goal_family',
                                'This is a broad criterion family only. The native error formula, norm, scale, order, and guarantee remain distinct in the profile and advanced tags.')
        resource = self.effective.get('resource', {})
        kind = resource.get('kind')
        kind_map = {'oracle_calls': 'oracle_calls', 'scalar_oracle_calls': 'oracle_calls',
                    'component_calls': 'oracle_calls', 'samples': 'samples', 'joint': 'joint'}
        if kind in kind_map:
            self.emit('RESOURCE:measure:' + kind_map[kind], [self.src('/resource/kind')], 'resource.declared_principal_kind',
                      'The source explicitly names the main resource kind; a component call is a declared primitive call, with its exact unit retained in the profile.')
        elif isinstance(resource.get('primary'), str):
            primary = resource['primary']
            value = ('memory' if 'memory' in primary.lower() else 'arithmetic' if 'arithmetic' in primary.lower()
                     else 'samples' if 'sample' in primary.lower() else 'rounds' if primary.lower() in ['t', 'rounds', 'stopping_time']
                     else 'oracle_calls' if re.fullmatch(r'N_[A-Za-z0-9_]+', primary) else None)
            if value:
                self.emit('RESOURCE:measure:' + value, [self.src('/resource/primary')], 'resource.declared_primary_coordinate',
                          'The explicitly designated primary coordinate determines the cost family; other recorded coordinates are not assumed charged.')
        if isinstance(resource.get('vector'), list) and resource['vector']:
            self.emit('RESOURCE:measure:joint', [self.src('/resource/vector')], 'resource.declared_joint_vector',
                      'The source retains a joint resource vector. No arbitrary scalar sum of its differently charged coordinates is introduced.')
        # Projection expressions belong to the exact compared resource in this
        # view. This avoids treating every auxiliary component as the main cost.
        projection_ids = {comparison['resource_projection_id'] for comparison in self.p['comparisons']
                          if comparison['view_id'] == self.vid}
        for index, projection in enumerate(self.p.get('resource_projections', [])):
            if projection['resource_projection_id'] not in projection_ids:
                continue
            if projection.get('mode') in ['pareto', 'multi_resource_feasibility']:
                self.emit('RESOURCE:measure:joint', ['/resource_projections/' + str(index) + '/mode'],
                          'resource.compared_joint_feasibility', 'This view explicitly compares a Pareto/joint feasible resource budget rather than an arbitrary scalar sum.')
            expression = projection.get('expression')
            if not isinstance(expression, str):
                continue
            normalized = expression.strip()
            value = ('memory' if re.fullmatch(r'memory_(?:bits|registers)', normalized)
                     else 'arithmetic' if normalized in ['arithmetic_ops', 'arithmetic', 'field_ops', 'asymptotic arithmetic exponent']
                     else 'rounds' if normalized in ['T', 'rounds', 'time_rounds']
                     else 'samples' if re.fullmatch(r'(?:E )?N_(?:sample|joint_sample|independent_sample|operator_sample|source_bundle)', normalized)
                     else 'oracle_calls' if re.fullmatch(r'(?:E )?N_[A-Za-z0-9_]+(?:\s*\+\s*N_[A-Za-z0-9_]+)*', normalized)
                     else None)
            if value:
                self.emit('RESOURCE:measure:' + value, ['/resource_projections/' + str(index) + '/expression'],
                          'resource.compared_projection_family',
                          'This exact resource projection is used by a documented comparison in this view. Only its broad cost family is grouped; units, weights and joint constraints are not equated.')
        parameters = {parameter['id']: parameter for parameter in self.p['parameters']}
        round_components = [index for index, component in enumerate(resource.get('components', []))
                            if isinstance(component, dict) and component.get('code') == 'rounds']
        for index, quantity in enumerate(self.p['quantities']):
            if quantity['view_id'] != self.vid:
                continue
            if quantity.get('units') == 'joint resource vector':
                self.emit('RESOURCE:measure:joint', ['/quantities/' + str(index) + '/units'], 'resource.joint_quantity_units',
                          'The native compared quantity explicitly has joint-resource-vector units; weights and simultaneous constraints remain unchanged.')
            if quantity.get('units') == 'arithmetic exponent':
                self.emit('RESOURCE:measure:arithmetic', ['/quantities/' + str(index) + '/units'], 'resource.arithmetic_exponent_units',
                          'The native compared exponent measures field arithmetic work, not oracle calls or memory.')
            if quantity.get('kind') == 'asymptotic_expected_sample_constant' or quantity.get('units') == 'samples per nat of confidence':
                self.emit('RESOURCE:measure:samples', ['/quantities/' + str(index) + '/units'], 'resource.expected_sample_constant_units',
                          'The native objective explicitly measures expected sample cost per logarithmic confidence scale; this is a resource expectation, not expected performance error.')
            if self.p['primary_domain'] == 'online_bandit' and round_components:
                for bi, parameter_id in enumerate(quantity.get('budget_variables', [])):
                    if parameters.get(parameter_id, {}).get('symbol') == 'T':
                        self.emit('RESOURCE:measure:rounds', [self.src('/resource/components/' + str(round_components[0]) + '/code'),
                                                           '/quantities/' + str(index) + '/budget_variables/' + str(bi)],
                                  'resource.declared_online_horizon', 'The source declares rounds as a resource and this view explicitly uses horizon T as a budget variable; rounds are not equated with scalar observations or communication rounds.')


def matches(view, selected_ids):
    groups = defaultdict(set)
    for tid in selected_ids:
        groups[OPTIONS[tid]['group_id']].add(tid)
    actual = set(view['facet_ids'])
    return all(actual & options for options in groups.values())


def resolve_alias_phrases(query):
    """Reference semantics for precise aliases; UI may implement the same rule.

    English aliases require whole token boundaries. All aliases compete by
    longest phrase, and an accepted span cannot also trigger a shorter alias.
    Thus nonconvex/inexact never trigger convex/exact, and first-order
    stationarity does not silently select a first-order oracle.
    """
    query = unicodedata.normalize('NFKC', query).lower()
    candidates = []
    for tid, definition in OPTIONS.items():
        for alias in definition['aliases']:
            alias = unicodedata.normalize('NFKC', alias).lower()
            boundary = bool(re.search(r'[a-z0-9]', alias))
            pattern = (r'(?<![a-z0-9_])' if boundary else '') + re.escape(alias) + (r'(?![a-z0-9_])' if boundary else '')
            for match in re.finditer(pattern, query):
                candidates.append((len(alias), match.start(), match.end(), tid))
    occupied, accepted = set(), set()
    for length, start, end, tid in sorted(candidates, key=lambda item: (-item[0], item[1], item[3])):
        span = set(range(start, end))
        if not span & occupied:
            occupied.update(span)
            accepted.add(tid)
    return sorted(accepted)


def fixtures(profiles):
    by_id = {item['id']: item for item in profiles}
    combo = ['ORACLE:access:zero', 'ORACLE:quality:exact', 'MODEL:objective_convexity:convex']
    expected = ['SO_ZO_E01', 'SO_ZO_E02', 'SO_ZO_E03', 'SO_ZO_E04', 'SO_ZO_E05', 'SO_ZO_E06a', 'SO_ZO_E06b',
                'SO_ZO_E06cL', 'SO_ZO_E06cS', 'SO_ZO_E06d', 'SO_ZO_E06e', 'SO_ZO_E06f_rand', 'SO_ZO_E07_neighborhood', 'SO_ZO_B03_rand_expected',
                'ON_BCO1_ADV_S', 'ON_BCO2_ADV_S', 'SO_ZO_E09a', 'SO_ZO_E09c']
    excluded = ['SO_ZO_N06_main', 'SO_ZO_B01_operator_expected', 'SO_ZO_C01_smooth_only', 'BL_SPEC_zo_common_sample',
                'CV_S_VI_RESIDUAL_DET', 'SO_FO_N04_PROJ_ball']
    checks = []
    for sid in expected + excluded:
        hit = any(matches(view, combo) for view in by_id[sid]['views'])
        checks.append({'setting_id': sid, 'query': combo, 'expected_match': sid in expected,
                       'actual_match': hit, 'passed': hit == (sid in expected)})
    for sid, required, forbidden in [
        ('SO_FO_N04_PROJ_ball', 'ORACLE:quality:stochastic', 'ORACLE:quality:exact'),
        ('CV_S_NCC_STOCH_LOWER', 'ORACLE:quality:mixed', 'ORACLE:quality:exact'),
        ('ON_FC_S', 'ORACLE:quality:stochastic', 'ORACLE:quality:exact'),
        ('ON_ADV_S', 'ORACLE:quality:exact', 'ORACLE:quality:stochastic'),
        ('BL_SPEC_det_primitive', None, 'MODEL:objective_convexity:convex'),
        ('SO_HO_HON09_S_convexQh', None, 'METRIC:goal:first_order_stationarity'),
        ('MX_S_matmul_square', 'RESOURCE:measure:arithmetic', 'RESOURCE:measure:oracle_calls'),
    ]:
        actual = {tid for view in by_id[sid]['views'] for tid in view['facet_ids']}
        checks.append({'setting_id': sid, 'required': required, 'forbidden': forbidden,
                       'passed': (required is None or required in actual) and forbidden not in actual})
    for profile in profiles:
        for view in profile['views']:
            if 'MODEL:monotonicity:strongly_monotone' in view['facet_ids']:
                checks.append({'setting_id': profile['id'], 'view_id': view['view_id'],
                               'rule': 'strong_monotonicity_same_operator_closure',
                               'passed': 'MODEL:monotonicity:monotone' in view['facet_ids']})
    actual_hits = [profile['id'] for profile in profiles if any(matches(view, combo) for view in profile['views'])]
    alias_cases = [
        ('zeroth order exact convex', combo),
        ('zeroth-order exact convex', combo),
        ('inexact nonconvex', ['ORACLE:quality:inexact', 'MODEL:objective_convexity:not_assumed']),
        ('strongly convex', ['MODEL:objective_convexity:strongly_convex']),
        ('first-order stationarity', ['METRIC:goal:first_order_stationarity']),
        ('second-order stationarity', ['METRIC:goal:higher_order_stationarity']),
        ('convex-concave', ['MODEL:structure:convex_concave']),
    ]
    for phrase, expected_ids in alias_cases:
        actual = resolve_alias_phrases(phrase)
        checks.append({'alias_query': phrase, 'expected_option_ids': sorted(expected_ids),
                       'actual_option_ids': actual, 'passed': actual == sorted(expected_ids)})
    return {'passed': all(item['passed'] for item in checks), 'checks': checks,
            'primary_query': combo, 'primary_query_setting_ids': actual_hits, 'primary_query_count': len(actual_hits)}


def main():
    paths = list((DATA / 'settings').glob('*/profile.json'))
    inputs = [(path, read(path)) for path in paths]
    inputs.sort(key=lambda item: item[1]['provenance']['source_order'])
    preserved = {str(path): sha(path) for path, _ in inputs}
    preserved.update({str(path.with_name('classification.json')): sha(path.with_name('classification.json')) for path, _ in inputs})
    profiles, validation_errors, group_views = [], [], defaultdict(list)
    old_query = ['ORACLE:access_order:zero', 'ORACLE:feedback_quality:exact', 'MODEL:convexity:convex']
    old_sets = {tid: set() for tid in old_query}
    option_settings, option_views = defaultdict(set), Counter()
    for path, profile in inputs:
        classification_path = path.with_name('classification.json')
        classification = read(classification_path)
        if classification['profile_sha256'] != sha(path):
            raise ValueError('Stale source classification: ' + profile['setting_id'])
        for tag in classification['tags']:
            if tag['id'] in old_sets:
                old_sets[tag['id']].update((profile['setting_id'], vid) for vid in tag['view_ids'])
        views = [BrowseView(profile, classification, view, index).build() for index, view in enumerate(profile['views'])]
        record = {'id': profile['setting_id'], 'title': profile['title'], 'order': profile['provenance']['source_order'],
                  'profile_sha256': sha(path), 'classification_sha256': sha(classification_path), 'views': views}
        profiles.append(record)
        for view in views:
            for fact in view['facets']:
                option_settings[fact['id']].add(profile['setting_id'])
                option_views[fact['id']] += 1
                for pointer in fact['source_pointers']:
                    resolve(profile, pointer)
            for group in view['unknown_groups']:
                group_views[group].append({'setting_id': profile['setting_id'], 'view_id': view['view_id'], 'reason': view['unknown_groups'][group]})
    semantics = {'within_group': 'OR', 'across_groups': 'AND', 'compatibility': 'same_view',
                 'unknown': 'Unnormalized source facts do not match a positive option; unknown is audited, not fabricated as a default option.',
                 'aliases': 'Exact natural phrases with longest-phrase matching; never substring-match convex inside nonconvex, exact inside inexact, or access order inside first-order stationarity.'}
    vocabulary_axes = []
    for axis, name, default_open, description in AXES:
        groups = []
        for (ga, group), (group_name, desc) in GROUPS.items():
            if ga != axis:
                continue
            options = [{**definition, 'count_settings': len(option_settings[tid]), 'count_views': option_views[tid]}
                       for tid, definition in OPTIONS.items() if definition['axis'] == axis and definition['group'] == group]
            groups.append({'id': axis + ':' + group, 'key': group, 'axis': axis, 'label': group_name,
                           'description': desc, 'options': options})
        vocabulary_axes.append({'id': axis, 'label': name, 'default_open': default_open,
                                'description': description, 'groups': groups})
    vocabulary = {'version': VERSION, 'schema_version': VERSION, 'axes': vocabulary_axes,
                   'options': list(OPTIONS.values()), 'filter_semantics': semantics,
                   'advanced_source_tags': 'taxonomy.json', 'option_count': len(OPTIONS)}
    browse = {'version': VERSION, 'schema_version': VERSION, 'facets_version': VERSION,
              'profile_count': len(profiles), 'view_count': sum(len(item['views']) for item in profiles),
              'filter_semantics': semantics, 'profiles': profiles}
    tests = fixtures(profiles)
    aliases = defaultdict(list)
    for tid, definition in OPTIONS.items():
        for alias in definition['aliases']:
            aliases[unicodedata.normalize('NFKC', alias).strip().lower()].append(tid)
    collisions = {alias: ids for alias, ids in aliases.items() if len(set(ids)) > 1}
    if collisions:
        validation_errors.append({'alias_collisions': collisions})
    unchanged = all(sha(pathlib.Path(path)) == fingerprint for path, fingerprint in preserved.items())
    if not unchanged:
        validation_errors.append({'input_bytes_changed': True})
    report = {'schema_version': VERSION, 'generated_at_utc': datetime.now(timezone.utc).isoformat(),
              'profile_count': len(profiles), 'view_count': browse['view_count'], 'common_option_count': len(OPTIONS),
              'profile_and_classification_bytes_preserved': unchanged, 'validation_errors': validation_errors,
              'unknown_groups': dict(group_views), 'semantic_fixtures': tests,
              'passed': not validation_errors and tests['passed'],
              'advanced_tags_unchanged': True, 'pdfs_not_read_or_modified': True}
    report['original_zero_result_diagnosis'] = {
        'semantics': 'All intersections require the same setting AND same view.',
        'original_source_tag_ids': old_query,
        'intersections': [{'tag_ids': list(combo), 'views': len(set.intersection(*(old_sets[tid] for tid in combo))),
                           'settings': len({sid for sid, _ in set.intersection(*(old_sets[tid] for tid in combo))})}
                          for count in [1, 2, 3] for combo in itertools.combinations(old_query, count)],
        'cause': 'exact_value native codes were stored only as interface_family, never as feedback_quality exact; the old literal-code Exact and Zero view sets were disjoint. Strong convexity also lacked a same-target Convex browse closure.',
        'minimal_counterexample': {'setting_id': 'SO_ZO_E01', 'source_pointers': ['/common_specification/oracle/code', '/common_specification/model/properties/convexity'],
                                   'native_code': 'exact_value', 'target_convexity': 'convex'},
    }
    write(DATA / 'derived/browse.json', browse)
    write(DATA / 'vocabulary/browse_facets.json', vocabulary)
    write(DATA / 'audit/browse.json', report)
    print(json.dumps({'profiles': len(profiles), 'views': browse['view_count'], 'options': len(OPTIONS),
                      'zero_exact_convex_matches': tests['primary_query_count'], 'passed': report['passed']}))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
