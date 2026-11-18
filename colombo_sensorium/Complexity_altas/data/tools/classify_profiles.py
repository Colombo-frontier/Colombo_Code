#!/usr/bin/env python3
"""Build the global eight-axis, source-traceable setting classification.

This classifier reads the active profile bytes, never edits a profile, and
never infers mathematical equivalence. Typed source facts and narrowly
specified explicit-text rules generate tags. Unsupported material is audited.
Operation bindings retain the query/response/object/block/coupling contract.
"""
from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
import pathlib
import re
from datetime import datetime, timezone

DATA = pathlib.Path(__file__).resolve().parents[1]
VERSION = '1.0.0'

# Groups are global definitions, not profile-dependent headings.
GROUPS = {
    'TASK': ('Task', {
        'task_family': ('Task family', 'Navigation family declared by the task; it does not specify the mathematical formulation.'),
        'formulation': ('Mathematical formulation', 'Explicit task formulation codes. Similar titles do not imply identical formulations.'),
        'solution_concept': ('Requested solution concept', 'A goal explicitly declared in the task specification, independently of its performance metric.'),
    }),
    'MODEL': ('Admissible model', {
        'convexity': ('Convexity and concavity', 'Convexity promises on the declared object or variable block; a block promise is not a joint-objective promise.'),
        'monotonicity': ('Monotonicity', 'Monotonicity, strong monotonicity, and Minty-type promises on the declared operator.'),
        'smoothness': ('Smoothness and regularity', 'Function or derivative regularity, including population, component, samplewise, and higher-order distinctions. This does not grant derivative access.'),
        'growth': ('Growth and error bounds', 'PL, uniform convexity, and other explicitly declared growth conditions.'),
        'geometry': ('Geometry and domains', 'Shape and role of model domains, norms, and localization geometry, without granting an oracle interface.'),
        'initialization': ('Initialization and localization', 'Initial gaps, distances, residuals, potentials, or explicit absence of localization.'),
        'structure': ('Objective and instance structure', 'Finite sums, composites, separability, bilinear structure, and other declared instance structures.'),
        'spectral_structure': ('Matrix and spectral structure', 'Explicit matrix class, rank, symmetry, positive definiteness, and spectral restrictions.'),
        'stochastic_model': ('Stochastic and temporal assumptions', 'Instance distribution, moment, variance, drift, and dependence promises; oracle reuse permissions are recorded separately.'),
        'existence': ('Existence promises', 'Explicit existence or nonexistence promises; an omitted promise remains unknown.'),
    }),
    'ORACLE': ('Oracle interface', {
        'operation': ('Primitive operation', 'The explicitly declared operation or response kind; derivative actions and full tensors are distinct.'),
        'access_order': ('Access class', 'Explicit zero-, first-, or higher-order interface declaration; model smoothness is classified separately.'),
        'scalar_derivative_order': ('Scalar-function derivative order', 'Derivative order relative to the explicitly named scalar function, including a reduced objective only when named.'),
        'operator_derivative_order': ('Operator derivative order', 'Derivative order relative to an operator. A complete operator (p−1)-jet is not a scalar p-jet.'),
        'derivative_order': ('Other declared derivative order', 'An explicit derivative order whose reference object type cannot be safely normalized; exact binding is retained.'),
        'feedback_quality': ('Feedback quality', 'The source quality code. Exact feedback of a random reward is not relabeled as a noiseless population response.'),
        'sample_coupling': ('Sample coupling and reuse', 'Only explicitly supported fresh, shared-batch, persistent-handle, or independent-sample permissions.'),
        'index_control': ('Index control', 'Who selects a component, coordinate, arm, or other query index.'),
        'query_domain': ('Query domain', 'Only domains explicitly declared by the oracle, independently of function and output domains.'),
        'auxiliary_interface': ('Auxiliary interface', 'Explicitly supplied proximal, projection, resolvent, linear-minimization, or mirror access.'),
        'public_information': ('Public information contract', 'Declared public/hidden inputs and whether a parameter is an exact known value, an upper bound, or a lower bound.'),
        'interface_family': ('Declared interface family', 'An informative native interface code retained without deriving unspecified response details.'),
    }),
    'ALGORITHMS': ('Algorithm class', {
        'randomization': ('Randomization', 'Private randomness allowed or deterministic algorithms explicitly required.'),
        'adaptivity': ('Adaptivity and timing', 'Explicit sequential, adaptive, nonadaptive, online, or batch interaction permissions.'),
        'restriction': ('Algorithm restrictions', 'Explicit span, support, privacy, pass, and method restrictions. Missing or empty fields do not mean unrestricted.'),
        'computation': ('Internal computation', 'Only explicit arithmetic or computational restrictions and permissions.'),
        'communication': ('Communication', 'Declared synchronization or communication restrictions.'),
        'memory': ('Memory', 'Declared memory limits or explicit absence of an additional memory restriction.'),
        'named_method': ('Fixed method', 'A named method explicitly fixed by the specification, rather than an example upper-bound algorithm.'),
    }),
    'OUTPUT': ('Output contract', {
        'object': ('Output object', 'Required returned object type, independent of its approximation criterion.'),
        'feasibility': ('Feasibility', 'Explicit feasibility requirements and their pathwise or almost-sure interpretation.'),
        'postprocessing': ('Postprocessing', 'Explicit permission for unqueried points, measurable postprocessing, averages, or convex combinations.'),
        'certificate': ('Certificate requirement', 'Whether an additional certificate, graph element, or positive radius must be returned.'),
        'support': ('Output support', 'Explicit output support, atomic-hull, or zero-respecting requirements.'),
    }),
    'METRIC': ('Loss or accuracy criterion', {
        'criterion': ('Performance criterion', 'The mathematical error, residual, gap, regret, or approximation criterion; this is not an oracle or an output type.'),
        'normalization': ('Metric form and normalization', 'Explicit norm, square, relative, additive, or normalized form, without interchanging them.'),
    }),
    'GUARANTEE': ('Success guarantee', {
        'mode': ('Error / correctness guarantee', 'Deterministic, expectation, probability, almost-sure, or exact guarantees for the performance error only. Expected stopping cost is classified under RESOURCE.budget.'),
        'aggregation': ('Aggregation order', 'Explicit first/second-moment or RMS aggregation and per-instance rather than distribution-average requirements.'),
        'quantifier': ('Quantifier order', 'The algorithm is selected from public input before the admissible hidden instance is universally quantified.'),
        'randomness': ('Randomness sources', 'The explicitly named randomness over which expectation or probability is taken.'),
        'confidence': ('Confidence contract', 'Fixed success probability, tunable confidence, uniform delta-correctness, or time-indexed confidence.'),
        'time_uniformity': ('Time uniformity', 'Fixed-time, anytime, or per-time guarantees only where explicitly stated.'),
    }),
    'RESOURCE': ('Resource accounting', {
        'measure': ('Declared resource coordinate', 'A declared resource coordinate or native measure. Some coordinates are recorded separately or uncharged; the cited contract determines cost, and distinct coordinates are never added implicitly.'),
        'budget': ('Budget semantics', 'Fixed worst-case cap, worst-instance expected cost, or another explicit budget mode.'),
        'accounting': ('Accounting rules', 'Joint, weighted, summed, per-response, and per-instance accounting only when explicit.'),
        'precision': ('Arithmetic and bit accounting', 'Whether bit precision or internal arithmetic is counted; this does not imply oracle accuracy.'),
        'setup': ('Initialization cost', 'Explicit inclusion or treatment of setup and initialization calls.'),
    }),
}

IGNORE_CODES = {'other_declared', 'model_declared', 'task_declared', 'oracle_declared',
                'output_declared', 'metric_declared', 'resource_declared', 'performance_measure',
                'algorithms_declared', 'guarantee_declared', 'explicit_model_clause', 'none_declared'}
ALIASES = {
    'strong_convexity': 'strongly_convex', 'general': 'not_assumed',
    'gradient_lipschitz': 'lipschitz_gradient', 'smooth': 'lipschitz_gradient',
    'function_lipschitz': 'lipschitz_function', 'lipschitz_continuous': 'lipschitz_function',
    'hessian_lipschitz': 'lipschitz_hessian',
    'BL.UNIQUE_REDUCED': 'bilevel_unique_reduced', 'BL.OPTIMISTIC': 'bilevel_optimistic',
    'expected_loss': 'expectation', 'expected_error': 'expectation',
    'randomized_allowed': 'private_randomness_allowed', 'forbidden': 'deterministic',
    'root_mean_square': 'rms', 'tan': 'tangent_residual', 'gap': 'saddle_gap',
    'compact_saddle_gap': 'saddle_gap', 'expected_saddle_gap': 'saddle_gap',
    'full saddle gap': 'saddle_gap', 'expected_weak_gap': 'weak_gap', 'Minty weak gap': 'weak_gap',
    'reduced_gradient_norm': 'reduced_gradient', 'reduced_stationarity': 'reduced_gradient',
    'reduced stationarity': 'reduced_gradient', 'stationary_reduced_gradient': 'reduced_gradient',
    'reduced first-order stationarity': 'reduced_gradient',
    'moreau_gradient': 'moreau_envelope_gradient', 'moreau_envelope_stationarity': 'moreau_envelope_gradient',
    'moreau_envelope_gradient': 'moreau_envelope_gradient',
    'certified_graph_residual': 'graph_residual', 'rms_inclusion_residual': 'graph_residual',
    'expected_resolvent_displacement': 'resolvent_displacement',
    'function_gap': 'objective_gap', 'first_order_stationarity': 'first_order_stationarity',
    'gradient_norm': 'gradient_norm', 'goldstein': 'goldstein_stationarity',
    'fixed_success_probability': 'fixed_probability',
    'SO.global_minimization': 'global_minimization', 'SO.first_order_stationarity': 'first_order_stationarity',
    'SO.second_order_stationarity': 'second_order_stationarity',
    'lower_strong_convexity': 'lower_strongly_convex',
    'joint_gradient_lipschitz': 'lipschitz_gradient',
    'joint_hessian_lipschitz': 'lipschitz_hessian',
}
LABELS = {
    'not_assumed': 'Convexity not assumed', 'lipschitz_gradient': 'Lipschitz gradient',
    'lipschitz_hessian': 'Lipschitz Hessian', 'lipschitz_function': 'Lipschitz function',
    'higher': 'Higher-order interface', 'zero': 'Zeroth-order interface', 'first': 'First-order interface',
    'scalar_order_0': 'Scalar function value (order 0)', 'scalar_order_1': 'Scalar-function first derivative',
    'scalar_order_2': 'Scalar-function second derivative',
    'operator_order_0': 'Operator value (order 0)', 'operator_order_1': 'Operator first derivative',
    'operator_order_2': 'Operator second derivative',
    'parameterized': 'Parameterized order (see exact operation binding)',
    'parameterized_minus_one': 'Parameterized order p−1 (see exact operation binding)',
    'parameterized_zero_offset': 'Parameterized order p (see exact operation binding)',
    'no_additional_restrictions_declared': 'Explicitly no additional algorithm restrictions',
    'no_span_restriction': 'No additional span restriction explicitly imposed',
    'no_zero_respecting_restriction': 'No additional zero-respecting restriction explicitly imposed',
    'known_value': 'Known exact value', 'known_upper_bound': 'Known upper bound',
    'known_lower_bound': 'Known lower bound', 'known_interval': 'Known interval',
    'exact_feedback': 'Source-declared exact feedback (may be a random reward)',
    'fixed_worst_case': 'Fixed worst-case budget', 'worst_instance_expected': 'Worst-instance expected cost',
    'private_randomness_allowed': 'Private randomness allowed',
    'public_inputs_declared': 'Public inputs explicitly declared', 'hidden_objects_declared': 'Hidden objects explicitly declared',
    'strongly_convex_in_block': 'Strong convexity in the declared block',
    'strongly_concave_in_block': 'Strong concavity in the declared block',
    'convex_in_block': 'Convexity in the declared block', 'concave_in_block': 'Concavity in the declared block',
    'lower_strongly_convex': 'Lower objective strongly convex in its lower variable',
    'reduced_strongly_convex': 'Reduced objective strongly convex',
    'reduced_convex': 'Reduced objective convex', 'lower_quadratic': 'Quadratic lower objective',
    'lower_pl': 'Lower-level PL condition', 'reduced_gradient': 'Reduced-objective gradient norm',
    'tangent_residual': 'Tangential residual', 'saddle_gap': 'Saddle-point gap',
    'squared_norm': 'Squared-norm error (no square-root conversion)',
    'rms': 'Root-mean-square / second-moment guarantee',
    'second_moment': 'Second moment of the complete error',
    'unqueried_allowed': 'Unqueried output explicitly allowed',
    'unqueried_forbidden': 'Output must satisfy an explicit queried-point restriction',
    'none_required': 'No additional output certificate required',
    'graph_element_required': 'Graph-element certificate required',
    'fresh_calls': 'Fresh independent sampling across calls',
    'persistent_sample_handle': 'Persistent sample handle with permitted reuse',
    'shared_current_batch_only': 'Shared sample within the current batch only',
    'same_sample_pair': 'Same-sample paired observations',
    'declared_confidence_parameter': 'Confidence parameter explicitly declared',
    'parameterized_failure_probability': 'Failure probability parameter explicitly declared',
    'fixed_probability': 'Fixed numerical success / failure probability',
    'fixed_confidence_identification': 'Uniform fixed-confidence identification correctness',
    'instancewise_expected_stopping_cost': 'Instancewise expected stopping cost (not a worst-instance supremum)',
    'finite_bit_state': 'Finite-bit retained state',
    'real_register_state': 'Exact-real register state',
    'synchronization_protocol': 'Local-information protocol between synchronizations',
}


def read(path):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(value):
    value = ALIASES.get(str(value), str(value))
    return re.sub(r'[^a-z0-9]+', '_', value.lower()).strip('_')


def label(value):
    value = str(value)
    return LABELS.get(value, value.replace('_', ' ').replace('.', ' · ').capitalize())


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


def text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return ' '.join(text(v) for v in value.values())
    if isinstance(value, list):
        return ' '.join(text(v) for v in value)
    return str(value) if value is not None else ''


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


def model_group(code):
    """Group native typed properties by their scientific meaning, never misc."""
    code = str(code).lower().removeprefix('regularity:')
    if code in ['strongly_convex_set', 'known_convex_feasible_set']:
        return 'geometry'
    if code in ['explicit_field_matrices', 'square_matrices', 'fixed_rectangular_shape']:
        return 'spectral_structure'
    if any(word in code for word in ['initial', 'localization', 'root_localization', 'dual_initial', 'optimizer_localization']):
        return 'initialization'
    if any(word in code for word in ['monotone', 'monotonicity', 'minty']):
        return 'monotonicity'
    if any(word in code for word in ['convex', 'concav']):
        return 'convexity'
    if any(word in code for word in ['polyak', 'pl_condition', 'uniform_pl', 'dual_pl', 'uniform_perturbed_pl', 'error_bound']):
        return 'growth'
    if any(word in code for word in ['variance', 'moment', 'deviation', 'noise', 'iid', 'gaussian', 'bernoulli',
                                      'drift', 'variation', 'nonstationary', 'reward_range', 'loss_range',
                                      'bounded_loss', 'independent_reward', 'stochastic_model', 'mean_variation',
                                      'comparator_path', 'bounded_gradient_heterogeneity']):
        return 'stochastic_model'
    if any(word in code for word in ['lipschitz', 'smooth', 'holder', 'regularity', 'derivative', 'differentiab',
                                      'continuous', 'self_concord', 'bounded_gradient', 'bounded_partial_gradient',
                                      'gradient_bound', 'rkhs', 'hessian_bound']):
        return 'smoothness'
    if any(word in code for word in ['positive_definite', 'positive_semidefinite', 'real_spd', 'real_psd', 'psd_',
                                      'symmetric', 'spectral', 'matrix', 'rank', 'stieltjes', 'hodlr',
                                      's_regular_public_pattern', 'hierarchical_partition', 'hermitian']):
        return 'spectral_structure'
    if any(word in code for word in ['geometry', 'diameter', 'ball', 'simplex', 'closed', 'domain', 'norm_',
                                      'norm_mismatch', 'geodesic', 'hyperbolic', 'compact', 'parameter_ball',
                                      'coordinate_range', 'one_dimensional', 'feasible_set']):
        return 'geometry'
    if any(word in code for word in ['existence', 'exist', 'unique_inner_solution', 'unique_lower', 'uniform_bounded_solution']):
        return 'existence'
    structures = ['finite', 'composite', 'component', 'quadratic', 'bilinear', 'linear', 'separable', 'distributed',
                  'network', 'local_objective', 'partial_monitoring', 'submodular', 'public_signal', 'binary_outcome',
                  'known_', 'strict_coupling', 'normalized_common', 'constant_cardinality', 'balanced_context',
                  'expert_probabilities', 'unique_best', 'row_stream', 'public_complexity', 'bounded_below',
                  'compressible', 'trace_budget', 'expectation_', 'no_additional_structure', 'sample_loss_gradient_realizable',
                  'single_use_sample', 'fresh_samples', 'stochastic_observation', 'function_class']
    if any(word in code for word in structures):
        return 'structure'
    return None


class Classifier:
    def __init__(self, profile, path):
        self.p, self.path = profile, path
        self.all_views = [view['view_id'] for view in profile['views']]
        self.tags, self.unparsed, self.bindings = {}, [], []
        self.inspected = set()

    def note(self, axis, pointer, reason, value=None, views=None):
        key = (axis, pointer, reason, tuple(views or self.all_views))
        if key in self.inspected:
            return
        self.inspected.add(key)
        self.unparsed.append({'axis': axis, 'source_pointer': pointer, 'reason': reason,
                              'view_ids': views or self.all_views,
                              'source_excerpt': text(value)[:400] if value is not None else None})

    def add(self, axis, group, value, pointer, views=None, state='structured', display=None, context=None):
        if value is None or str(value) in IGNORE_CODES or not str(value).strip():
            return
        value = slug(value)
        if not value or value in IGNORE_CODES:
            return
        # These name quantitative accuracy targets, not additional task families.
        # Keep the source task.solution_goal intact and index their criterion in
        # METRIC only, so global navigation does not duplicate the same label.
        if axis == 'TASK' and group == 'solution_concept' and value in {
                'tangent_residual', 'saddle_gap', 'reduced_gradient', 'reduced_gradient_rms'}:
            return
        if group not in GROUPS[axis][1]:
            raise ValueError('Unknown global group ' + axis + ':' + group)
        source_value = resolve(self.p, pointer)  # Never cite an invented path.
        # A source paragraph can mention a capability solely to deny it. Rather
        # than attempt unrestricted prose entailment, withhold positive tags
        # from negated/qualified prose and record the exact clause for review.
        negative_fact = (value.startswith(('no_', 'not_')) or '_not_' in value
                         or value in ['none_required', 'unqueried_forbidden'])
        asserted_clause = (context or {}).get('asserted_clause')
        if asserted_clause is not None and asserted_clause not in text(source_value):
            raise ValueError('A reviewed clause must be a literal source substring: ' + pointer)
        entailment_text = asserted_clause if asserted_clause is not None else text(source_value)
        if state == 'explicit_text' and not negative_fact and re.search(
                r'\b(?:no|not|never|without|cannot|except)\b', entailment_text.lower()):
            self.note(axis, pointer, 'Negated or qualified prose is not automatically a positive classification fact', source_value, views)
            return
        vids = list(views if views is not None else self.all_views)
        if not vids:
            return
        tag_id = ':'.join([axis, group, value])
        tag = self.tags.setdefault(tag_id, {
            'id': tag_id, 'axis': axis, 'group': group, 'value': value,
            'label': display or label(value), 'source_pointers': [], 'view_ids': [],
            'evidence_state': state, 'evidence': [],
        })
        if pointer not in tag['source_pointers']:
            tag['source_pointers'].append(pointer)
        for vid in vids:
            if vid not in tag['view_ids']:
                tag['view_ids'].append(vid)
        evidence = {'source_pointer': pointer, 'view_ids': vids, 'state': state}
        if context:
            evidence['context'] = context
        if evidence not in tag['evidence']:
            tag['evidence'].append(evidence)
        order = {'structured': 0, 'explicit_text': 1, 'legacy_facet': 2}
        if order[state] < order[tag['evidence_state']]:
            tag['evidence_state'] = state

    def typed(self, axis, group, obj, key, ptr, views, aliases=None):
        if isinstance(obj, dict) and obj.get(key) is not None:
            value = obj[key]
            if isinstance(value, (str, int, float, bool)):
                self.add(axis, group, (aliases or {}).get(value, value), ptr + '/' + token(key), views)

    def process(self):
        # Only explicit task family data is global; no family is deduced from a title.
        self.add('TASK', 'task_family', self.p['primary_domain'], '/primary_domain')
        for index, view in enumerate(self.p['views']):
            vp = '/views/' + str(index)
            effective, origins = merge(self.p['common_specification'], view.get('specification_overrides', {}),
                                       '/common_specification', vp + '/specification_overrides')
            src = lambda suffix: origins[suffix]
            vids = [view['view_id']]
            self.task(effective.get('task', {}), src, vids)
            self.model(effective.get('model', {}), src, vids)
            self.oracle(effective.get('oracle', {}), src, vids)
            self.output(effective.get('output', {}), src, vids)
            self.metric(effective.get('metric', {}), src, vids)
            self.resource(effective.get('resource', {}), src, vids)
            self.algorithms(view.get('algorithms', {}), vp + '/algorithms', vids)
            for gi, guarantee in enumerate(view['guarantees']):
                self.guarantee(guarantee, vp + '/guarantees/' + str(gi), vids)
            for qi, qualification in enumerate(view.get('display_qualifications', [])):
                pointer = vp + '/display_qualifications/' + str(qi)
                self.output_text(qualification, pointer, vids)
                self.budget_text(qualification, pointer, vids)
            budget = view.get('budget', {})
            for field in ['budget_semantics', 'budget']:
                if budget.get(field):
                    self.budget_text(budget[field], vp + '/budget/' + field, vids)
        self.facets()
        tags = sorted(self.tags.values(), key=lambda item: (list(GROUPS).index(item['axis']), item['group'], item['value']))
        for tag in tags:
            tag['scope'] = 'all_declared_views' if set(tag['view_ids']) == set(self.all_views) else 'selected_views'
        axes = {axis: [tag['id'] for tag in tags if tag['axis'] == axis] for axis in GROUPS}
        return {
            'schema_version': VERSION, 'taxonomy_version': VERSION, 'classifier_version': VERSION,
            'record_type': 'setting_classification', 'setting_id': self.p['setting_id'],
            'profile_schema_version': self.p['schema_version'], 'profile_sha256': sha(self.path),
            'classification_policy': 'explicit_source_facts_only; missing_is_unknown; no_equivalence_claim',
            'contract_separation': 'GUARANTEE.mode describes performance error or correctness; RESOURCE.budget describes runtime/query cost. An expectation of stopping time is not an expected-error guarantee.',
            'axes': axes, 'tags': tags, 'operation_bindings': self.bindings,
            'unparsed_count': len(self.unparsed),
            'unclassified_axes': [axis for axis, ids in axes.items() if not ids],
        }

    def task(self, obj, src, vids):
        for index, family in enumerate(obj.get('navigation_domains', [])):
            self.add('TASK', 'task_family', family, src('/task/navigation_domains/' + str(index)), vids)
        code = obj.get('formulation_code')
        if code and code not in IGNORE_CODES and not code.endswith('.other_declared'):
            self.add('TASK', 'formulation', code, src('/task/formulation_code'), vids)
        elif code:
            self.note('TASK', src('/task/formulation_code'), 'Generic formulation code; inspect explicit mathematical statement', code, vids)
        goal = obj.get('solution_goal')
        if goal:
            if re.fullmatch(r'[A-Za-z0-9_.-]+', str(goal)):
                self.add('TASK', 'solution_concept', goal, src('/task/solution_goal'), vids)
            else:
                known = {
                    'Moreau envelope first-order stationarity': 'moreau_envelope_stationarity',
                    'full saddle gap': 'saddle_gap', 'Minty weak gap': 'weak_gap',
                    'solution distance': 'solution_distance', 'root residual': 'root_residual',
                    'constrained game stationarity': 'constrained_game_stationarity',
                    'reduced first-order stationarity': 'reduced_gradient', 'reduced stationarity': 'reduced_gradient',
                    'Moreau stationarity': 'moreau_envelope_stationarity', 'weighted stationarity': 'weighted_stationarity',
                    'distance to unique saddle': 'distance_to_unique_saddle',
                }
                if goal in known:
                    self.add('TASK', 'solution_concept', known[goal], src('/task/solution_goal'), vids)
                else:
                    self.note('TASK', src('/task/solution_goal'), 'Free-text solution goal retained for review', goal, vids)

    def model(self, obj, src, vids):
        cv = obj.get('convexity')
        if isinstance(cv, dict) and cv.get('code'):
            self.add('MODEL', 'convexity', cv['code'], src('/model/convexity/code'), vids)
        elif isinstance(cv, str):
            self.add('MODEL', 'convexity', cv, src('/model/convexity'), vids)
        props = obj.get('properties', {})
        if isinstance(props, dict):
            for group, values in props.items():
                values = values if isinstance(values, list) else [values]
                for index, value in enumerate(values):
                    suffix = '/model/properties/' + token(group) + ('/' + str(index) if isinstance(props[group], list) else '')
                    if not isinstance(value, str):
                        continue
                    canonical_group = 'convexity' if group == 'convexity' else model_group(value)
                    if canonical_group:
                        self.add('MODEL', canonical_group, value, src(suffix), vids)
                    else:
                        self.note('MODEL', src(suffix), 'Unmapped model property', value, vids)
        for index, assumption in enumerate(obj.get('assumptions', [])):
            suffix = '/model/assumptions/' + str(index)
            if not isinstance(assumption, dict):
                self.note('MODEL', src(suffix), 'Unparsed assumption', assumption, vids)
                continue
            code = assumption.get('property_code')
            group = model_group(code) if code not in IGNORE_CODES else None
            negated = re.search(r'not (?:assumed|required|promised|imposed)|need not|does not assume|no .{0,35}promise',
                                str(assumption.get('description', '')).lower())
            if group and negated and not str(code).startswith(('no_', 'not_')):
                self.note('MODEL', src(suffix + '/property_code'),
                          'Property code occurs in a negated or mixed-qualified assumption; no positive tag inferred', assumption, vids)
                continue
            if group:
                self.add('MODEL', group, code, src(suffix + '/property_code'), vids,
                         context={key: assumption[key] for key in ['subject_id', 'variable_blocks', 'scope', 'norm_ref'] if key in assumption})
            elif code == 'explicit_model_clause':
                self.model_text(assumption.get('description', ''), src(suffix + '/description'), vids)
            elif code:
                self.note('MODEL', src(suffix + '/property_code'), 'Unmapped typed model assumption', code, vids)
        for field in ['regularity', 'structure', 'geometry']:
            values = obj.get(field, [])
            values = values if isinstance(values, list) else [values]
            for index, item in enumerate(values):
                suffix = '/model/' + field + ('/' + str(index) if isinstance(obj.get(field), list) else '')
                if isinstance(item, dict):
                    code = item.get('code') or (item.get('kind') if field == 'geometry' else None)
                    key = 'code' if item.get('code') else 'kind'
                    if code and code not in IGNORE_CODES:
                        group = 'geometry' if field == 'geometry' else model_group(code)
                        if group:
                            self.add('MODEL', group, code, src(suffix + '/' + key), vids,
                                     context={k: item[k] for k in ['roles', 'norm', 'domain_ref'] if k in item})
                    elif item:
                        self.note('MODEL', src(suffix), 'Model object needs explicit property normalization', item, vids)
                elif isinstance(item, str) and re.fullmatch(r'[A-Za-z0-9_:.]+', item):
                    group = model_group(item)
                    if group:
                        self.add('MODEL', group, item.removeprefix('regularity:'), src(suffix), vids)
                    else:
                        self.note('MODEL', src(suffix), 'Unmapped structured model code', item, vids)
                elif item:
                    self.model_text(item, src(suffix), vids)
        for field in ['lower_geometry', 'reduced_geometry', 'outer_geometry', 'initialization', 'existence']:
            if obj.get(field):
                self.model_text(obj[field], src('/model/' + field), vids, role=field)
        # Narrative is allowed only through explicit, conservative rules, not keyword guessing.
        for index, paragraph in enumerate(obj.get('description_paragraphs', [])):
            self.model_text(paragraph, src('/model/description_paragraphs/' + str(index)), vids)

    def model_text(self, value, pointer, vids, role=None):
        value = text(value)
        low = value.lower()
        # Role-specific bilevel promises prevent primitive/reduced convexity conflation.
        if role == 'lower_geometry' and re.search(r'strongly[ -]convex', low):
            self.add('MODEL', 'convexity', 'lower_strongly_convex', pointer, vids, 'explicit_text')
        if role in ['reduced_geometry', 'outer_geometry']:
            if re.search(r'strongly[ -]convex', low):
                self.add('MODEL', 'convexity', 'reduced_strongly_convex', pointer, vids, 'explicit_text')
            elif re.search(r'(?:is |objective (?:is )?)convex', low) and not re.search(r'not.*convex|nonconvex|non-convex', low):
                self.add('MODEL', 'convexity', 'reduced_convex', pointer, vids, 'explicit_text')
        if role == 'initialization':
            if re.search(r'\|\|.*y.*y\*|\\\|.*y.*y\^', value):
                self.add('MODEL', 'initialization', 'bounded_initial_inner_distance', pointer, vids, 'explicit_text')
            if re.search(r'x0-x\*|x_0-x|initial.*distance', low):
                self.add('MODEL', 'initialization', 'initial_distance', pointer, vids, 'explicit_text')
            if re.search(r'initial.*gap|phi\(.*\).*phi|objective.gap', low):
                self.add('MODEL', 'initialization', 'initial_gap', pointer, vids, 'explicit_text')
        if role == 'existence':
            if re.search(r'not (?:assumed|promised)|no .*existence|need not (?:exist|attain)', low):
                self.add('MODEL', 'existence', 'not_promised', pointer, vids, 'explicit_text')
            elif re.search(r'(?:exists|existence|attain|nonempty|non-empty)', low):
                self.add('MODEL', 'existence', 'explicit_existence_promise', pointer, vids, 'explicit_text')
        if re.search(r'initial dual (?:error|residual).*unrestricted|no (?:bound|control).*dual.*initial|without.*dual.*localization', low):
            self.add('MODEL', 'initialization', 'no_dual_localization', pointer, vids, 'explicit_text')
        # Smoothness is deliberately not inferred by scanning arbitrary prose:
        # qualifications and negations frequently concern only a sample/object.
        # Typed regularity records and explicit source facets supply these tags.

    def oracle(self, obj, src, vids):
        code = obj.get('code')
        if code not in IGNORE_CODES and code is not None:
            if code in ['first_order', 'higher_order']:
                self.add('ORACLE', 'access_order', 'first' if code == 'first_order' else 'higher', src('/oracle/code'), vids)
            else:
                self.add('ORACLE', 'interface_family', code, src('/oracle/code'), vids)
        feedback = obj.get('feedback')
        if isinstance(feedback, dict):
            for field, group in [('kind', 'operation'), ('accuracy', 'feedback_quality')]:
                if feedback.get(field):
                    self.add('ORACLE', group, feedback[field], src('/oracle/feedback/' + field), vids)
        query_type = obj.get('query_type')
        if query_type and query_type not in ['point', 'point_query', 'point_coordinate', 'point_vector_query', 'time_indexed_point_query', 'typed_derivative_query']:
            self.add('ORACLE', 'interface_family', query_type, src('/oracle/query_type'), vids)
        objects = {item.get('id'): item for item in self.p.get('registry', {}).get('objects', [])}
        for index, operation in enumerate(obj.get('operations', [])):
            suffix = '/oracle/operations/' + str(index)
            pointer = src(suffix)
            if not isinstance(operation, dict):
                self.bindings.append({'view_ids': vids, 'source_pointer': pointer, 'state': 'unparsed',
                                      'raw': operation, 'object_binding': 'unknown', 'block_binding': 'unknown'})
                self.note('ORACLE', pointer, 'Natural-language operation; do not infer object, block, derivative or sample bindings', operation, vids)
                continue
            binding = {'view_ids': vids, 'source_pointer': pointer, 'state': 'structured',
                       'source_fields': copy.deepcopy(operation)}
            for field in ['target_object', 'derivative_reference_object']:
                ids = operation.get(field)
                ids = ids if isinstance(ids, list) else [ids]
                binding[field + '_registry'] = [copy.deepcopy(objects[oid]) for oid in ids if oid in objects]
            self.bindings.append(binding)
            if operation.get('operation_code'):
                self.add('ORACLE', 'operation', operation['operation_code'], src(suffix + '/operation_code'), vids,
                         context={key: operation[key] for key in ['target_object', 'derivative_reference_object', 'variable_blocks'] if key in operation})
            quality = operation.get('feedback_quality', {})
            if isinstance(quality, dict) and quality.get('code'):
                self.add('ORACLE', 'feedback_quality', quality['code'], src(suffix + '/feedback_quality/code'), vids)
            order = operation.get('derivative_order')
            if order is not None and order != 'not_applicable':
                op_code = operation.get('operation_code', '')
                target = operation.get('derivative_reference_object') or operation.get('target_object')
                ref = objects.get(target, {}) if isinstance(target, str) else {}
                operator = 'operator' in op_code and not any(word in op_code for word in ['hessian', 'gradient'])
                scalar = ref.get('type') in ['function', 'reduced_objective', 'scalar_function'] or any(word in op_code for word in ['gradient', 'hessian', 'derivative_vector', 'payoff_', 'function_value', 'sample_function'])
                group = 'operator_derivative_order' if operator else 'scalar_derivative_order' if scalar else 'derivative_order'
                if isinstance(order, int):
                    value = ('operator_order_' if operator else 'scalar_order_' if scalar else 'order_') + str(order)
                elif isinstance(order, dict):
                    value = 'parameterized_minus_one' if order.get('offset') == -1 else 'parameterized_zero_offset' if order.get('offset') == 0 else 'parameterized'
                else:
                    self.note('ORACLE', src(suffix + '/derivative_order'), 'Unparsed derivative order', order, vids)
                    value = None
                if value:
                    self.add('ORACLE', group, value, src(suffix + '/derivative_order'), vids,
                             context={key: operation[key] for key in ['target_object', 'derivative_reference_object', 'variable_blocks', 'order_convention'] if key in operation})
            for field in ['coupling', 'index_control', 'access_schedule']:
                if operation.get(field):
                    self.oracle_text(operation[field], src(suffix + '/' + field), vids, field)
        for field in ['coupling', 'query_domain_description', 'query_domain', 'domain', 'variant']:
            if obj.get(field):
                self.oracle_text(obj[field], src('/oracle/' + field), vids, field)
        for key in ['public_inputs', 'hidden_objects']:
            if obj.get(key):
                self.add('ORACLE', 'public_information', key + '_declared', src('/oracle/' + key), vids)
        for index, item in enumerate(obj.get('public_inputs', [])):
            if isinstance(item, dict) and item.get('knowledge'):
                self.add('ORACLE', 'public_information', item['knowledge'], src('/oracle/public_inputs/' + str(index) + '/knowledge'), vids)
        auxiliary = obj.get('auxiliary_interfaces', [])
        auxiliary_items = list(auxiliary.items()) if isinstance(auxiliary, dict) else list(enumerate(auxiliary))
        for index, item in auxiliary_items:
            pointer = src('/oracle/auxiliary_interfaces/' + token(index))
            if isinstance(auxiliary, dict) and index == 'coupling':
                self.oracle_text(item, pointer, vids, 'coupling')
            code = item.get('operation_code') or item.get('code') if isinstance(item, dict) else None
            if code:
                self.add('ORACLE', 'auxiliary_interface', code, pointer, vids)
            elif isinstance(item, str) and item:
                self.note('ORACLE', pointer,
                          'Free-text auxiliary contract may be negated, conditional, or describe scalar projection; capability is not inferred by keywords', item, vids)

    def oracle_text(self, value, pointer, vids, field):
        low = text(value).lower()
        if field == 'index_control':
            if low in ['none', 'not_applicable']:
                return
            if re.search(r'cannot select|sampling mechanism determines|not.*select.*sample|sample outcomes', low):
                self.note('ORACLE', pointer, 'Query choices do not imply control of random sample indices; exact clause retained in operation binding', value, vids)
            elif re.search(r'algorithm.selects?(?: (?:component|coordinate|arm))?(?: index|indices)?$|algorithm selects (?:component|coordinate|arm) index|algorithm chooses (?:indices|the component index)|chosen by the algorithm', low):
                self.add('ORACLE', 'index_control', 'algorithm_selects', pointer, vids, 'explicit_text')
            elif re.fullmatch(r'[a-z_]+', low):
                self.add('ORACLE', 'index_control', low, pointer, vids)
            else:
                self.note('ORACLE', pointer, 'Index-control wording retained for review', value, vids)
        elif field in ['query_domain_description', 'query_domain', 'domain']:
            if re.fullmatch(r'\$?\\mathbb\{?r\}?\^d\$?\.?|r\^d|full.space[.;]?(?: arbitrary v)?', low.strip()):
                self.add('ORACLE', 'query_domain', 'full_space', pointer, vids, 'explicit_text')
            elif re.search(r'full (?:euclidean )?space', low) and not re.search(r'not|outside|except|separately', low):
                self.add('ORACLE', 'query_domain', 'full_space', pointer, vids, 'explicit_text')
        elif field in ['coupling', 'variant']:
            if low == 'paid_unlimited_same_sample_reuse':
                self.add('ORACLE', 'sample_coupling', 'persistent_sample_handle', pointer, vids, 'explicit_text')
            elif low not in ['none', 'not_applicable']:
                self.note('ORACLE', pointer,
                          'Sampling/reuse prose requires exact contract review; fresh drawing does not imply fresh evaluation calls and a mentioned handle may be negated', value, vids)

    def algorithms(self, obj, pointer, vids):
        rv = obj.get('randomization')
        if rv:
            low = str(rv).lower()
            if low in ['deterministic', 'forbidden', 'deterministic only'] or re.search(r'randomization is forbidden|fixed deterministic|deterministic exact arithmetic', low):
                clause = str(rv).split(';', 1)[0]
                self.add('ALGORITHMS', 'randomization', 'deterministic', pointer + '/randomization', vids,
                         'structured' if low in ['deterministic', 'forbidden'] else 'explicit_text',
                         context={'asserted_clause': clause})
            elif re.search(r'allow|private random|arbitrary private random', low):
                self.add('ALGORITHMS', 'randomization', 'private_randomness_allowed', pointer + '/randomization', vids, 'structured' if low in ['allowed', 'randomized_allowed'] else 'explicit_text')
            else:
                self.note('ALGORITHMS', pointer + '/randomization', 'Unparsed randomization clause', rv, vids)
        av = obj.get('adaptivity')
        if av:
            low = str(av).lower()
            if low in ['adaptive', 'sequential_adaptive'] or re.search(r'arbitrary.*adaptiv|measurable.*past responses', low):
                self.add('ALGORITHMS', 'adaptivity', 'adaptive', pointer + '/adaptivity', vids,
                         'structured' if low in ['adaptive', 'sequential_adaptive'] else 'explicit_text')
            elif re.search(r'fixed before any response|nonadaptive', low):
                self.add('ALGORITHMS', 'adaptivity', 'nonadaptive', pointer + '/adaptivity', vids, 'explicit_text')
            elif re.search(r'previous.round|per.round|online|causal', low):
                self.add('ALGORITHMS', 'adaptivity', 'causal_protocol', pointer + '/adaptivity', vids, 'explicit_text')
            elif low == 'restricted':
                self.add('ALGORITHMS', 'adaptivity', 'explicit_restriction', pointer + '/adaptivity', vids)
        restrictions = obj.get('restrictions')
        if restrictions == ['none']:
            self.add('ALGORITHMS', 'restriction', 'no_additional_restrictions_declared', pointer + '/restrictions/0', vids)
        elif restrictions == [] or restrictions is None:
            self.note('ALGORITHMS', pointer + ('/restrictions' if 'restrictions' in obj else ''),
                      'Absent or empty restrictions do not establish an unrestricted algorithm class', restrictions, vids)
        for field in ['restrictions', 'description_paragraphs', 'internal_computation', 'internal_computation_restrictions']:
            values = obj.get(field, [])
            values = values if isinstance(values, list) else [values]
            for index, item in enumerate(values):
                if not item:
                    continue
                ip = pointer + '/' + field + ('/' + str(index) if isinstance(obj.get(field), list) else '')
                low = text(item).lower()
                if re.search(r'no (?:additional )?(?:linear.)?span|without (?:additional )?span|no linear.span', low):
                    self.add('ALGORITHMS', 'restriction', 'no_span_restriction', ip, vids, 'explicit_text')
                if re.search(r'no (?:additional )?(?:linear.span,? )?zero.respecting|without (?:additional )?(?:span, )?zero.respecting|no linear.span, zero.support', low):
                    self.add('ALGORITHMS', 'restriction', 'no_zero_respecting_restriction', ip, vids, 'explicit_text')
                if re.search(r'zero.respecting|zero.support', low) and not re.search(r'no .*zero|without .*zero|not .*zero', low):
                    self.add('ALGORITHMS', 'restriction', 'zero_respecting', ip, vids, 'explicit_text')
                if re.search(r'linear.span (?:queries|restriction)|block.memory linear.span|restricted.*linear.span', low) and not re.search(r'no .*span|without .*span|not .*span', low):
                    self.add('ALGORITHMS', 'restriction', 'linear_span', ip, vids, 'explicit_text')
                if 'one_pass' in low or 'one-pass' in low:
                    self.add('ALGORITHMS', 'restriction', 'one_pass', ip, vids, 'explicit_text')
                if 'no_past_requery' in low:
                    self.add('ALGORITHMS', 'restriction', 'no_past_requery', ip, vids, 'structured')
                if re.search(r'joint differential privacy', low):
                    self.add('ALGORITHMS', 'restriction', 'joint_differential_privacy', ip, vids, 'explicit_text')
                if re.search(r'concentrated differential privacy', low):
                    self.add('ALGORITHMS', 'restriction', 'concentrated_differential_privacy', ip, vids, 'explicit_text')
                if re.search(r'fixed_algorithm:', low):
                    self.add('ALGORITHMS', 'named_method', low.split('fixed_algorithm:', 1)[1], ip, vids)
                if item == 'exact_field_arithmetic':
                    self.add('ALGORITHMS', 'computation', 'exact_field_arithmetic', ip, vids)
                if 'history-span restrictions must hold' in low:
                    self.add('ALGORITHMS', 'restriction', 'linear_span', ip, vids, 'explicit_text')
                raw = text(item)
                for pattern, group, value in [
                    (r'The state between rows is a finite bit string', 'memory', 'finite_bit_state'),
                    (r'State consists of exact-real registers updated by ordinary arithmetic and comparisons', 'memory', 'real_register_state'),
                    (r'Between synchronizations, (?:each client uses only its|clients use only) new local observations and (?:history|information) shared at the (?:previous|preceding) synchronization', 'communication', 'synchronization_protocol'),
                ]:
                    match = re.search(pattern, raw, re.IGNORECASE)
                    if match:
                        self.add('ALGORITHMS', group, value, ip, vids, 'explicit_text',
                                 context={'asserted_clause': match.group(0), 'reviewed_rule': value})
                if (not re.search(r'count all field|every field operation.*charged|count.*arithmetic preprocessing', low)
                        and re.search(r'(?:internal (?:exact )?(?:real )?arithmetic|arithmetic[, ]+[^.;]{0,60}(?:storage|linear algebra))[^.;]{0,100}(?:uncharged|(?:is|are) free)', low)):
                    self.add('ALGORITHMS', 'computation', 'internal_arithmetic_uncharged', ip, vids, 'explicit_text')

    def output(self, obj, src, vids):
        if obj.get('object_type'):
            self.add('OUTPUT', 'object', obj['object_type'], src('/output/object_type'), vids)
        for field in ['feasible_required', 'may_be_unqueried']:
            if field in obj and isinstance(obj[field], bool):
                group = 'feasibility' if field == 'feasible_required' else 'postprocessing'
                value = 'required' if field == 'feasible_required' and obj[field] else 'not_required' if field == 'feasible_required' else 'unqueried_allowed' if obj[field] else 'unqueried_forbidden'
                self.add('OUTPUT', group, value, src('/output/' + field), vids)
        for field in ['description_paragraphs', 'allowed_postprocessing', 'postprocessing', 'certificate_requirement', 'certificate', 'feasibility']:
            values = obj.get(field, [])
            values = values if isinstance(values, list) else [values]
            for index, item in enumerate(values):
                if item:
                    suffix = '/output/' + field + ('/' + str(index) if isinstance(obj.get(field), list) else '')
                    self.output_text(item, src(suffix), vids)

    def output_text(self, item, pointer, vids):
        low = text(item).lower()
        if re.search(r'unqueried.*(?:allow|permi)|may be (?:an? )?unqueried|including an unqueried|possibly an unqueried', low):
            self.add('OUTPUT', 'postprocessing', 'unqueried_allowed', pointer, vids, 'explicit_text')
        clause = re.search(r'Return an outer point from the restricted iteration sequence', text(item))
        if clause:
            self.add('OUTPUT', 'object', 'outer_point', pointer, vids, 'explicit_text', context={'asserted_clause': clause.group(0)})
            self.add('OUTPUT', 'support', 'restricted_iteration_sequence', pointer, vids, 'explicit_text', context={'asserted_clause': clause.group(0)})
        if re.search(r'arbitrary measurable postprocessing|any measurable postprocessing', low):
            self.add('OUTPUT', 'postprocessing', 'measurable_postprocessing', pointer, vids, 'explicit_text')
        if re.search(r'(?:no|not required|need not).*certificate|certificate.*(?:not required|none)', low) or low in ['none', 'none beyond true-error guarantee']:
            self.add('OUTPUT', 'certificate', 'none_required', pointer, vids, 'explicit_text')
        if re.search(r'graph.element certificate|return.*\\(?:widehat|hat).*\\in a\(', low):
            self.add('OUTPUT', 'certificate', 'graph_element_required', pointer, vids, 'explicit_text')
        if re.search(r'output.*zero.respecting|must obey.*zero.respecting|output support.*(?:contained|lies)', low):
            self.add('OUTPUT', 'support', 'zero_respecting', pointer, vids, 'explicit_text')
        if re.search(r'convex hull of (?:the )?returned atoms|returned.atom hull', low):
            self.add('OUTPUT', 'support', 'returned_atom_hull', pointer, vids, 'explicit_text')

    def metric(self, obj, src, vids):
        kind = obj.get('kind')
        if kind and kind not in IGNORE_CODES:
            self.add('METRIC', 'criterion', kind, src('/metric/kind'), vids)
        for field in ['base_expression', 'base_expression_latex', 'formula_latex']:
            expression = obj.get(field)
            if not isinstance(expression, str):
                continue
            if re.search(r'\\(?:dist|operatorname\{dist\})\(0,.*N_', expression):
                self.add('METRIC', 'criterion', 'tangent_residual', src('/metric/' + field), vids, 'explicit_text')
            # Do not scan a compound definition for a squared norm: a square can
            # belong to a Moreau regularizer rather than the actual base loss.
            if re.fullmatch(r'(?:f|F|H|\\Phi)\(\\widehat\{?x\}?\)-\\inf_[\s\S]+', expression.strip()):
                self.add('METRIC', 'criterion', 'objective_gap', src('/metric/' + field), vids, 'explicit_text')
            if expression.strip() == r'\tfrac12(\widehat{x}-x_*)^\top A(\widehat{x}-x_*)':
                self.add('METRIC', 'criterion', 'quadratic_energy_loss', src('/metric/' + field), vids, 'explicit_text')

    def guarantee(self, obj, pointer, vids):
        mode = obj.get('mode')
        if mode:
            self.add('GUARANTEE', 'mode', mode, pointer + '/mode', vids)
        code = obj.get('code')
        if code and code not in IGNORE_CODES and code != 'accuracy_guarantee':
            groups = {'fixed_success_probability': ('mode', 'probability'), 'expected_loss': ('mode', 'expectation'),
                      'deterministic': ('mode', 'deterministic'), 'high_probability': ('mode', 'probability'),
                      'almost_sure_per_instance': ('mode', 'almost_sure'), 'exact_per_instance': ('mode', 'exact'),
                      'uniform_delta_correct': ('confidence', 'uniform_delta_correct')}
            if code in groups:
                self.add('GUARANTEE', *groups[code], pointer + '/code', vids)
            if code == 'uniform_delta_correct':
                self.add('GUARANTEE', 'mode', 'probability', pointer + '/code', vids)
        for field in ['complete_expression', 'formula_latex']:
            formula = obj.get(field)
            if not isinstance(formula, str):
                continue
            # Complete-expression fields can combine P(error) with E[cost].
            # Such mixed functionals are not classified by an arbitrary E/P.
            if re.search(r'\\tau|stopping|(?:query|call|work|cost|budget)\b|N_[A-Za-z]', formula, re.IGNORECASE):
                self.note('GUARANTEE', pointer + '/' + field,
                          'Complete functional contains cost/time terms; do not confuse their expectation with error aggregation', formula, vids)
                continue
            if re.search(r'\\(?:mathbb\s*\{?E\}?|operatorname\{E\})', formula):
                self.add('GUARANTEE', 'mode', 'expectation', pointer + '/' + field, vids, 'explicit_text')
                if re.search(r'\\\|(?:_\{?[A-Za-z0-9\\]+\}?)?\^\{?2|\)\^\{?2', formula):
                    self.add('GUARANTEE', 'aggregation', 'second_moment', pointer + '/' + field, vids, 'explicit_text')
            if re.search(r'\\(?:Pr|mathbb\s*\{?P\}?)', formula):
                self.add('GUARANTEE', 'mode', 'probability', pointer + '/' + field, vids, 'explicit_text')
        for index, paragraph in enumerate(obj.get('description_paragraphs', [])):
            low = str(paragraph).lower()
            pp = pointer + '/description_paragraphs/' + str(index)
            if re.search(r'deterministic (?:and instancewise|error|guarantee)|guarantee is deterministic', low):
                self.add('GUARANTEE', 'mode', 'deterministic', pp, vids, 'explicit_text')
            if re.search(r'for every (?:fixed )?admissible instance|every fixed admissible instance|every instance', low):
                self.add('GUARANTEE', 'aggregation', 'per_instance', pp, vids, 'explicit_text')
            if re.search(r'private (?:algorithmic )?(?:seed|random)', low) and re.search(r'probability|expectation|over', low):
                self.add('GUARANTEE', 'randomness', 'algorithm_private_seed', pp, vids, 'explicit_text')
            for pattern, mode in [
                (r'The output is exact for every input', 'exact_per_instance'),
                (r'holds deterministically (?:for every admissible fixed input|on each instance)', 'deterministic'),
            ]:
                match = re.search(pattern, str(paragraph), re.IGNORECASE)
                if match:
                    self.add('GUARANTEE', 'mode', mode, pp, vids, 'explicit_text', context={'asserted_clause': match.group(0)})
            for formula in re.findall(r'\$([^$]+)\$', str(paragraph)):
                if re.search(r'\\mathbb\s*\{?E\}?', formula) and r'\nabla' in formula and not re.search(r'\\tau|call|cost|work|budget', formula):
                    self.add('GUARANTEE', 'mode', 'expectation', pp, vids, 'explicit_text', context={'asserted_clause': formula})
        for index, parameter in enumerate(obj.get('confidence_parameters', [])):
            cp = pointer + '/confidence_parameters/' + str(index)
            value = str(parameter)
            if re.fullmatch(r'δ|\\delta|[A-Za-z0-9_]+_p_[a-f0-9]+', value):
                self.add('GUARANTEE', 'confidence', 'declared_confidence_parameter', cp, vids)
            elif re.search(r'fixed (?:success probability|to)|probability fixed', value.lower()):
                self.add('GUARANTEE', 'confidence', 'fixed_probability', cp, vids, 'explicit_text')
        if isinstance(obj.get('failure_probability'), dict) and obj['failure_probability'].get('parameter_ref'):
            self.add('GUARANTEE', 'confidence', 'parameterized_failure_probability', pointer + '/failure_probability/parameter_ref', vids)
        # Fixed-confidence identification has an error-probability contract and
        # a separate expected stopping-cost objective. The quantifier clause is
        # inspected independently of the mixed complete functional.
        quantifier = str(obj.get('quantifier_order', ''))
        if re.search(r'(?:δ|delta).correct.*(?:all|every).*(?:μ|mu)', quantifier, re.IGNORECASE):
            self.add('GUARANTEE', 'mode', 'fixed_confidence_identification', pointer + '/quantifier_order', vids, 'explicit_text')
        if obj.get('quantifier_order'):
            low = str(obj['quantifier_order']).lower()
            if re.search(r'exists_algorithm_forall_instance|choose a single algorithm|algorithm.*public.*then.*(?:all|every|instance)', low):
                self.add('GUARANTEE', 'quantifier', 'algorithm_before_instance', pointer + '/quantifier_order', vids, 'explicit_text')
        for index, item in enumerate(obj.get('randomness_sources', [])):
            low = str(item).lower()
            value = 'algorithm_private_seed' if re.search(r'private|algorithm', low) else 'oracle_samples' if re.search(r'oracle|sample', low) else None
            if value:
                self.add('GUARANTEE', 'randomness', value, pointer + '/randomness_sources/' + str(index), vids, 'explicit_text')
            elif item:
                self.note('GUARANTEE', pointer + '/randomness_sources/' + str(index), 'Unnormalized explicit randomness source', item, vids)
        for field in ['time_uniformity', 'uniformity']:
            if obj.get(field):
                low = str(obj[field]).lower()
                if re.search(r'fixed (?:output |target |accuracy |time)|not an anytime', low):
                    self.add('GUARANTEE', 'time_uniformity', 'fixed_time_or_accuracy', pointer + '/' + field, vids, 'explicit_text')
                elif re.search(r'anytime|simultaneously for all', low) and not re.search(r'not|no ', low):
                    self.add('GUARANTEE', 'time_uniformity', 'anytime', pointer + '/' + field, vids, 'explicit_text')

    def resource(self, obj, src, vids):
        for field in ['kind', 'primary']:
            values = obj.get(field, [])
            values = values if isinstance(values, list) else [values]
            for index, value in enumerate(values):
                if isinstance(value, str) and value and value not in IGNORE_CODES:
                    suffix = '/resource/' + field + ('/' + str(index) if isinstance(obj.get(field), list) else '')
                    self.add('RESOURCE', 'measure', value, src(suffix), vids)
        for index, component in enumerate(obj.get('components', [])):
            if isinstance(component, dict) and component.get('code'):
                self.add('RESOURCE', 'measure', component['code'], src('/resource/components/' + str(index) + '/code'), vids)
        if isinstance(obj.get('vector'), list):
            for index, coordinate in enumerate(obj['vector']):
                if isinstance(coordinate, str) and re.fullmatch(r'[A-Za-z0-9_]+', coordinate):
                    self.add('RESOURCE', 'measure', coordinate, src('/resource/vector/' + str(index)), vids)
            if obj['vector']:
                self.add('RESOURCE', 'accounting', 'joint_coordinates_retained', src('/resource/vector'), vids)
        for field in ['budget_mode', 'budget_semantics', 'budget', 'description_paragraphs']:
            values = obj.get(field, [])
            values = values if isinstance(values, list) else [values]
            for index, item in enumerate(values):
                if item:
                    suffix = '/resource/' + field + ('/' + str(index) if isinstance(obj.get(field), list) else '')
                    self.budget_text(item, src(suffix), vids)
        for field in ['bit_precision_counted', 'free_operations']:
            if field == 'bit_precision_counted' and isinstance(obj.get(field), bool):
                self.add('RESOURCE', 'precision', 'bit_precision_counted' if obj[field] else 'bit_precision_not_counted', src('/resource/' + field), vids)
        if obj.get('setup_cost') and re.search(r'all.*initialization.*included|count.*initialization|including initialization', str(obj['setup_cost']).lower()):
            self.add('RESOURCE', 'setup', 'initialization_included', src('/resource/setup_cost'), vids, 'explicit_text')
        if obj.get('scalarization'):
            low = str(obj['scalarization']).lower()
            if re.search(r'joint|vector|remain separate|no.*sum', low):
                self.add('RESOURCE', 'accounting', 'joint_coordinates_retained', src('/resource/scalarization'), vids, 'explicit_text')
        if obj.get('precision_model') and re.search(r'bit costs? (?:uncharged|excluded)|bit length is free|bit complexity.*not', str(obj['precision_model']).lower()):
            self.add('RESOURCE', 'precision', 'bit_precision_not_counted', src('/resource/precision_model'), vids, 'explicit_text')

    def budget_text(self, item, pointer, vids):
        low = text(item).lower()
        negated = re.search(r'(?:no|not|does not).{0,35}(?:fixed worst.case|pathwise cap)', low)
        if not negated and (low in ['worst_case', 'fixed_worst_case', 'fixed_worst_case_cap'] or re.search(r'fixed worst.case|fixed.*pathwise.*cap|fixed.*budget.*every.*path|calls never exceed|budget is fixed on every execution path', low)):
            self.add('RESOURCE', 'budget', 'fixed_worst_case', pointer, vids, 'structured' if low in ['worst_case', 'fixed_worst_case', 'fixed_worst_case_cap'] else 'explicit_text')
        if low in ['expected', 'expected_budget', 'worst_instance_expected_calls'] or re.search(r'worst.(?:case|instance) expected (?:total )?(?:component )?(?:calls|cost|work|stopping time)|expected work on the worst instance', low):
            self.add('RESOURCE', 'budget', 'worst_instance_expected', pointer, vids, 'structured' if low in ['expected', 'expected_budget', 'worst_instance_expected_calls'] else 'explicit_text')
        raw = text(item)
        match = re.search(r'The sample count[^.]+primary cost[^.]+', raw)
        if match and re.search(r'\\mathbb\s*E_.*\\tau', match.group(0)):
            self.add('RESOURCE', 'budget', 'instancewise_expected_stopping_cost', pointer, vids, 'explicit_text',
                     context={'asserted_clause': match.group(0), 'reviewed_rule': 'native_instancewise_stopping_cost'})

    def facets(self):
        # Legacy facets supplement factual gaps; they never override a view contract.
        for index, facet in enumerate(self.p.get('facets', [])):
            key, value = facet.get('facet'), facet.get('value')
            pointer = '/facets/' + str(index) + '/value'
            if key == 'domain':
                self.add('TASK', 'task_family', value, pointer, state='legacy_facet')
            elif key == 'goal' and value not in ['global_minimization', 'other_declared']:
                self.add('METRIC', 'criterion', value, pointer, state='legacy_facet')
            elif key == 'oracle_order':
                self.add('ORACLE', 'access_order', value, pointer, state='legacy_facet')
            elif key == 'feedback':
                self.add('ORACLE', 'interface_family', value, pointer, state='legacy_facet')
            elif key in ['initialization', 'smoothness', 'geometry']:
                self.add('MODEL', key, value, pointer, state='legacy_facet')
            elif key == 'structure' and value != 'high_order':
                group = model_group(value)
                if group:
                    self.add('MODEL', group, value, pointer, state='legacy_facet')
                else:
                    self.note('MODEL', pointer, 'Unmapped legacy structural facet', value)
            elif key == 'structure' and value == 'high_order':
                self.note('MODEL', pointer, 'Ambiguous high_order facet is not used for smoothness or access; inspect explicit model and oracle fields', value)
            elif key in ['algorithm', 'guarantee', 'resource']:
                # These old facets may describe only one of several views.
                self.note({'algorithm': 'ALGORITHMS', 'guarantee': 'GUARANTEE', 'resource': 'RESOURCE'}[key], pointer,
                          'Profile-level legacy facet does not establish a contract for every view; typed per-view fields take precedence', value)
            elif key == 'output' and value == 'returned_atom_hull':
                self.add('OUTPUT', 'support', value, pointer, state='legacy_facet')
            elif key == 'information':
                self.add('ORACLE', 'public_information', value, pointer, state='legacy_facet')
            elif key == 'solvability':
                self.add('MODEL', 'existence', value, pointer, state='legacy_facet')


def build_taxonomy(classifications):
    tags = {}
    for classification in classifications:
        for item in classification['tags']:
            record = tags.setdefault(item['id'], {key: item[key] for key in ['id', 'axis', 'group', 'value', 'label']}
                                     | {'setting_count': 0, 'view_count': 0})
            record['setting_count'] += 1
            record['view_count'] += len(item['view_ids'])
    axes = []
    for axis_id, (axis_label, definitions) in GROUPS.items():
        groups = []
        for group_id, (group_label, description) in definitions.items():
            values = [{key: item[key] for key in ['id', 'value', 'label', 'setting_count', 'view_count']}
                      | {'tag_id': item['id']} for item in tags.values()
                      if item['axis'] == axis_id and item['group'] == group_id]
            values.sort(key=lambda item: item['label'].lower())
            groups.append({'id': group_id, 'label': group_label, 'description': description, 'values': values})
        axes.append({'id': axis_id, 'label': axis_label, 'description': axis_label + ' facts from the explicit setting specification.',
                     'groups': groups})
    return {'schema_version': VERSION, 'taxonomy_version': VERSION,
            'classification_policy': 'global_axes_and_groups; source_backed_values; missing_is_unknown; view_scoped',
            'axes': axes, 'tags': sorted(tags.values(), key=lambda item: item['id']),
            'semantics': {'tags_are': 'Faceted source facts, not a complete mathematical identity or equivalence proof.',
                          'cross_view_filtering': 'Tags may belong to different views. Read tag.view_ids and exact operation bindings before comparing contracts.',
                          'object_scope': 'Convexity, regularity and derivative order apply only to the declared object/block in their cited source.',
                          'unparsed_material': 'Retained in the classification audit and never converted into unrestricted or generic misc tags.'}}


def schema():
    return {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': 'urn:complexity-atlas:classification:1.0.0', 'type': 'object',
        'required': ['schema_version', 'taxonomy_version', 'record_type', 'setting_id', 'profile_sha256',
                     'axes', 'tags', 'operation_bindings', 'unparsed_count', 'unclassified_axes'],
        'properties': {
            'schema_version': {'const': VERSION}, 'record_type': {'const': 'setting_classification'},
            'setting_id': {'type': 'string', 'minLength': 1},
            'profile_sha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'},
            'axes': {'type': 'object', 'required': list(GROUPS), 'additionalProperties': False,
                     'properties': {axis: {'type': 'array', 'items': {'type': 'string'}} for axis in GROUPS}},
            'tags': {'type': 'array', 'items': {'type': 'object',
                     'required': ['id', 'axis', 'group', 'value', 'label', 'source_pointers', 'view_ids', 'evidence_state', 'evidence'],
                     'properties': {'id': {'type': 'string', 'pattern': '^(TASK|MODEL|ORACLE|ALGORITHMS|OUTPUT|METRIC|GUARANTEE|RESOURCE):[a-z_]+:[a-z0-9_]+$'},
                                    'axis': {'enum': list(GROUPS)}, 'group': {'type': 'string'},
                                    'value': {'type': 'string', 'minLength': 1}, 'label': {'type': 'string'},
                                    'source_pointers': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'pattern': '^/'}},
                                    'view_ids': {'type': 'array', 'minItems': 1, 'items': {'type': 'string'}},
                                    'evidence_state': {'enum': ['structured', 'explicit_text', 'legacy_facet']}}}},
            'operation_bindings': {'type': 'array'}, 'unparsed_count': {'type': 'integer', 'minimum': 0},
        },
        '$comment': 'classify_profiles.py additionally validates every pointer, view scope, operation binding, source hash, global group and tag ID.'}


def validate_outputs(profiles, classifications, taxonomy):
    errors, checks = [], 0
    global_tags = {tag['id']: tag for tag in taxonomy['tags']}
    for (path, profile), classification in zip(profiles, classifications):
        def check(okay, detail):
            nonlocal checks
            checks += 1
            if not okay:
                errors.append({'setting_id': profile['setting_id'], 'detail': detail})
        vids = {view['view_id'] for view in profile['views']}
        check(classification['profile_sha256'] == sha(path), 'Profile hash mismatch')
        check(list(classification['axes']) == list(GROUPS), 'Eight axes differ')
        for tag in classification['tags']:
            check(tag['id'] == ':'.join([tag['axis'], tag['group'], tag['value']]), 'Tag identity mismatch')
            check(tag['group'] in GROUPS[tag['axis']][1], 'Unknown axis/group')
            check(tag['id'] in global_tags, 'Tag absent from taxonomy')
            check(bool(tag['source_pointers']) and bool(tag['view_ids']), 'Tag lacks source or view scope')
            check(set(tag['view_ids']) <= vids, 'Tag names nonexistent view')
            check(tag['value'] not in IGNORE_CODES, 'Generic misc tag leaked')
            for pointer in tag['source_pointers']:
                try:
                    resolve(profile, pointer)
                except (KeyError, ValueError, IndexError, TypeError):
                    check(False, 'Unresolvable source pointer ' + pointer)
                else:
                    check(True, '')
        for binding in classification['operation_bindings']:
            source = resolve(profile, binding['source_pointer'])
            check(source == binding.get('source_fields', binding.get('raw')), 'Operation binding differs from exact source')
            check(set(binding['view_ids']) <= vids, 'Operation binding names nonexistent view')
        for axis, tag_ids in classification['axes'].items():
            check(tag_ids == [tag['id'] for tag in classification['tags'] if tag['axis'] == axis], 'Axis tag list mismatch')
    return {'passed': not errors, 'checks_run': checks, 'errors': errors}


def semantic_fixtures(profiles, classifications):
    """Regression fixtures from independently identified, real source clauses.

    These are scientific non-entailment checks, not snapshots of the rule code.
    Each case states a concrete capability or cost interpretation that its
    source does not permit. No synthetic profile text is substituted.
    """
    by_id = {item['setting_id']: item for item in classifications}
    source = {profile['setting_id']: profile for _, profile in profiles}
    cases = [
        ('SO_FO_N05_SD', ['ORACLE:auxiliary_interface:proximal', 'METRIC:normalization:squared_norm'],
         'No proximal objective oracle is provided, and a Moreau regularizer square is not the base gradient-norm error.'),
        ('CV_S_FS_NCSC_AS', ['ORACLE:auxiliary_interface:projection'],
         'The conditional boilerplate "Projection uses the stated interface" supplies no additional projection operation.'),
        ('SO_HO_HON09_S_convexQh', ['ORACLE:auxiliary_interface:proximal'],
         'A known outer composite function does not grant an additional proximal oracle.'),
        ('SO_HO_HOC08_S', ['ORACLE:auxiliary_interface:proximal'],
         'Solving a known higher-order model is not an ordinary proximal interface.'),
        ('SO_HO_HOC09_S', ['ORACLE:auxiliary_interface:proximal'],
         'Solving a known higher-order model is not an ordinary proximal interface.'),
        ('ONX_PARAMNOISE_LP_KNOWNCOV', ['ORACLE:auxiliary_interface:projection'],
         'A scalar projection reward is not geometric projection access.'),
        ('ONX_PARAMNOISE_LP_UNKNOWNCOV', ['ORACLE:auxiliary_interface:projection'],
         'A scalar projection reward is not geometric projection access.'),
        ('BL_SPEC_two_point_coupled', ['ORACLE:sample_coupling:persistent_sample_handle'],
         'Sharing within the current simultaneous batch explicitly excludes a reusable persistent handle.'),
        ('BL_SPEC_zo_common_sample', ['ORACLE:sample_coupling:fresh_calls'],
         'Fresh sample drawing does not make every evaluation fresh when identifiers may be reused.'),
        ('BL_SPEC_stoch_derivative', ['ORACLE:index_control:algorithm_selects'],
         'Choosing points, derivative blocks and batch sizes does not grant control of random sample outcomes.'),
        ('ON_BCO1_STO_S', ['MODEL:smoothness:lipschitz_gradient'],
         'Differentiability and Lipschitz gradients are explicitly not required.'),
        ('CV_S_WEAK_MINTY_ROOT_FRESH', ['MODEL:monotonicity:monotonicity', 'MODEL:smoothness:mean_square_average'],
         'The assumption topic code names monotonicity, but its description explicitly does not assume it or sample mean-square smoothness.'),
        ('SO_FO_O02_hidden_curve', ['RESOURCE:budget:worst_instance_expected'],
         'Expected suboptimality risk is an error aggregation, while the call cap is uniform on every path.'),
        ('MX_S_matmul_square', ['ALGORITHMS:computation:internal_arithmetic_uncharged'],
         'All field arithmetic and preprocessing are charged; "not a free oracle" cannot imply free arithmetic.'),
        ('MX_S_matmul_rect', ['ALGORITHMS:computation:internal_arithmetic_uncharged'],
         'All field arithmetic and preprocessing are charged.'),
        ('ON_FC_S', ['GUARANTEE:mode:expectation'],
         'Expected stopping time is a resource objective; the error contract is uniformly delta-correct.'),
    ]
    results = []
    for sid, forbidden, reason in cases:
        if sid not in by_id:
            results.append({'setting_id': sid, 'state': 'not_in_selected_dataset', 'reason': reason})
            continue
        actual = {tag['id'] for tag in by_id[sid]['tags']}
        leaked = sorted(set(forbidden) & actual)
        results.append({'setting_id': sid, 'state': 'passed' if not leaked else 'failed',
                        'forbidden_tag_ids': forbidden, 'leaked_tag_ids': leaked, 'reason': reason,
                        'profile_sha256': by_id[sid]['profile_sha256']})
    fs = by_id.get('CV_S_FS_NCSC_AS')
    if fs:
        tags = {tag['id']: tag for tag in fs['tags']}
        expected = {
            'ALGORITHMS:restriction:zero_respecting': {'randomized_zero_respecting_expected_rms'},
            'RESOURCE:budget:worst_instance_expected': {'randomized_zero_respecting_expected_rms', 'randomized_unrestricted_expected_rms'},
            'RESOURCE:budget:fixed_worst_case': {'randomized_unrestricted_fixed_probability'},
        }
        for tid, required_views in expected.items():
            actual_views = set(tags.get(tid, {}).get('view_ids', []))
            results.append({'setting_id': fs['setting_id'], 'tag_id': tid,
                            'state': 'passed' if actual_views == required_views else 'failed',
                            'required_view_ids': sorted(required_views), 'actual_view_ids': sorted(actual_views),
                            'reason': 'Error and resource contracts must stay scoped to the exact source view.'})
    for sid, tid, reason in [
        ('ON_FC_S', 'GUARANTEE:mode:fixed_confidence_identification', 'The correctness contract is delta-correct identification, separately from its cost.'),
        ('ON_FC_S', 'GUARANTEE:confidence:declared_confidence_parameter', 'Delta is explicitly listed as a confidence parameter.'),
        ('ON_FC_S', 'RESOURCE:budget:instancewise_expected_stopping_cost', 'The native cost fixes the target instance before taking the stopping-time expectation.'),
        ('MX_S_stream_bits', 'ALGORITHMS:memory:finite_bit_state', 'The retained streaming state is a finite bit string.'),
        ('MX_S_stream_real', 'ALGORITHMS:memory:real_register_state', 'The retained streaming state consists of exact-real registers.'),
        ('ONX_FED_TWO_LINEAR', 'ALGORITHMS:communication:synchronization_protocol', 'Clients use local observations between explicitly scheduled synchronizations.'),
        ('ONX_FED_TWO_LIPSCHITZ', 'ALGORITHMS:communication:synchronization_protocol', 'Clients use local observations between explicitly scheduled synchronizations.'),
    ]:
        if sid in by_id:
            actual = {tag['id'] for tag in by_id[sid]['tags']}
            results.append({'setting_id': sid, 'tag_id': tid, 'state': 'passed' if tid in actual else 'failed', 'reason': reason})
    return {'schema_version': VERSION, 'passed': not any(item['state'] == 'failed' for item in results),
            'fixture_count': len(results), 'fixtures': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--settings', type=pathlib.Path, default=DATA / 'settings')
    args = parser.parse_args()
    paths = list(args.settings.glob('*/profile.json'))
    profiles = [(path, read(path)) for path in paths]
    profiles.sort(key=lambda item: item[1].get('provenance', {}).get('source_order', item[1]['setting_id']))
    classifications, unparsed = [], []
    before_hashes = {str(path): sha(path) for path, _ in profiles}
    for path, profile in profiles:
        classifier = Classifier(profile, path)
        classification = classifier.process()
        classifications.append(classification)
        unparsed.extend({'setting_id': profile['setting_id']} | entry for entry in classifier.unparsed)
        write(path.with_name('classification.json'), classification)
    taxonomy = build_taxonomy(classifications)
    write(DATA / 'vocabulary' / 'taxonomy.json', taxonomy)
    write(DATA / 'vocabulary' / 'tags.json', {
        'schema_version': VERSION, 'taxonomy_version': VERSION, 'tag_format': 'AXIS:group:value',
        'tags': taxonomy['tags'], 'filter_semantics': 'AND across selected tags; per-view scope is retained in classification records',
    })
    write(DATA / 'schemas' / 'classification.schema.json', schema())
    validation = validate_outputs(profiles, classifications, taxonomy)
    fixtures = semantic_fixtures(profiles, classifications)
    write(DATA / 'audit' / 'classification_semantic_fixtures.json', fixtures)
    if not fixtures['passed']:
        validation['passed'] = False
        validation['errors'].extend({'setting_id': item['setting_id'], 'detail': 'Semantic fixture failed',
                                     'fixture': item} for item in fixtures['fixtures'] if item['state'] == 'failed')
    unchanged = all(sha(pathlib.Path(path)) == value for path, value in before_hashes.items())
    validation['checks_run'] += len(before_hashes)
    if not unchanged:
        validation['passed'] = False
        validation['errors'].append({'detail': 'Active profile bytes changed during classification'})
    report = {'schema_version': VERSION, 'generated_at_utc': datetime.now(timezone.utc).isoformat(),
              'classifier_version': VERSION, 'profile_count': len(classifications),
              'tag_count': len(taxonomy['tags']), 'tag_assignments': sum(len(item['tags']) for item in classifications),
              'counts_by_axis': {axis: sum(len(item['axes'][axis]) for item in classifications) for axis in GROUPS},
              'profiles_with_empty_axis': {axis: [item['setting_id'] for item in classifications if not item['axes'][axis]] for axis in GROUPS},
              'unparsed_count': len(unparsed), 'profile_bytes_preserved': unchanged,
              'validation': validation,
              'limitations': ['Source-backed classification does not certify mathematical equivalence.',
                              'Unsupported free text remains in classification_unparsed.json.',
                              'Legacy facets never establish algorithm, guarantee or resource contracts across all views.']}
    write(DATA / 'audit' / 'classification.json', report)
    write(DATA / 'audit' / 'classification_unparsed.json', {'schema_version': VERSION, 'records': unparsed})
    print(json.dumps({'profiles': len(classifications), 'tags': len(taxonomy['tags']),
                      'assignments': report['tag_assignments'], 'passed': validation['passed'],
                      'checks': validation['checks_run'], 'unparsed': len(unparsed)}, ensure_ascii=False))
    return 0 if validation['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
