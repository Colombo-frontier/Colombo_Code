#!/usr/bin/env python3
"""Import explicit scientific profiles without retaining workstation history.

The input directory is read only. No source code is executed.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import pathlib
import re
import shutil
from datetime import datetime, timezone

DATA = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_VERSION = '6.1.0'
NORMALIZER_VERSION = '0.2.0'
REMOVED_KEYS = frozenset({'coverage', 'coverage_note'})


def read_json(path):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))


def sha256(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def content_hash(value):
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def write_json(path, value):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def pointer_token(value):
    return str(value).replace('~', '~0').replace('/', '~1')


def clean_profile(value, pointer='', removed=None):
    """Remove only the two presentation fields; preserve every other value."""
    if removed is None:
        removed = []
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            item_pointer = pointer + '/' + pointer_token(key)
            if key.casefold() in REMOVED_KEYS:
                removed.append(item_pointer)
            else:
                result[key] = clean_profile(item, item_pointer, removed)
        return result
    if isinstance(value, list):
        return [clean_profile(item, pointer + '/' + str(index), removed)
                for index, item in enumerate(value)]
    return value


def verified_formula_repairs(profile):
    """Repair only evidenced JSON escape corruption; archive bytes stay intact."""
    sid = profile['setting_id']
    corrections = []
    def visit(value, pointer=''):
        if isinstance(value, dict):
            return {k: visit(v, pointer + '/' + pointer_token(k)) for k, v in value.items()}
        if isinstance(value, list):
            return [visit(v, pointer + '/' + str(i)) for i, v in enumerate(value)]
        if not isinstance(value, str):
            return value
        replacement, basis = value, None
        if sid == 'SO_HO_HOI01_S' and chr(13) + 'm dim' in value:
            replacement = value.replace(chr(13) + 'm dim', r'\rm dim')
            basis = 'The same bound applicability.conditions and original TeX Conditions preserve C_{\\rm dim}.'
        if sid in {'SO_HO_HOS04_S_hvp', 'SO_HO_HOS04_S_full'} and pointer == '/comparisons/0/bracket/ratio_or_gap' and chr(9) + 'heta' in value:
            replacement = value.replace(chr(9) + 'heta', r'\theta')
            basis = 'The original symbol table explicitly defines \\theta as the fixed model-parameter tuple; O_theta retains that dependence.'
        if replacement != value:
            corrections.append({'pointer': pointer, 'before': value, 'after': replacement,
                                'kind': 'verified_formula_escape_repair', 'basis': basis})
        return replacement
    result = visit(profile)
    return result, corrections


def all_leaf_sources(value, pointer):
    if isinstance(value, dict) and value:
        result = {}
        for key, item in value.items():
            child = '/' + pointer_token(key)
            for suffix, source in all_leaf_sources(item, pointer + child).items():
                result[child + suffix] = source
        return result
    if isinstance(value, list) and value:
        result = {}
        for index, item in enumerate(value):
            child = '/' + str(index)
            for suffix, source in all_leaf_sources(item, pointer + child).items():
                result[child + suffix] = source
        return result
    return {'': pointer}


def merge_with_sources(base, patch, base_pointer, patch_pointer):
    """Explicit mechanical merge: object recursion, scalar/array replacement."""
    if isinstance(base, dict) and isinstance(patch, dict):
        result, sources = {}, {}
        for key in list(base) + [key for key in patch if key not in base]:
            token = '/' + pointer_token(key)
            if key in patch and key in base:
                merged, child_sources = merge_with_sources(
                    base[key], patch[key], base_pointer + token, patch_pointer + token)
            elif key in patch:
                merged = copy.deepcopy(patch[key])
                child_sources = all_leaf_sources(merged, patch_pointer + token)
            else:
                merged = copy.deepcopy(base[key])
                child_sources = all_leaf_sources(merged, base_pointer + token)
            result[key] = merged
            sources.update({token + k: v for k, v in child_sources.items()})
        return result, sources
    return copy.deepcopy(patch), all_leaf_sources(patch, patch_pointer)


NARRATIVE_KEYS = {'description', 'description_zh', 'description_paragraphs',
                  'detail', 'description_en', 'notes'}
AXES = {'task': 'task', 'instance_model': 'model', 'oracle_interface': 'oracle',
        'output': 'output', 'metric': 'metric', 'resource_model': 'resource'}


def axis_record(value, pointer):
    if value is None or value == {}:
        state = 'unknown'
        fields = {}
    elif isinstance(value, dict):
        fields = {key: copy.deepcopy(item) for key, item in value.items()
                  if key not in NARRATIVE_KEYS}
        state = 'source_structured' if fields else 'unparsed'
    else:
        fields, state = {}, 'unparsed'
    return {
        'state': state,
        'source_pointer': pointer,
        'source_fields': fields,
        'narrative_pointers': [pointer + '/' + pointer_token(key)
                               for key in value if key in NARRATIVE_KEYS]
                              if isinstance(value, dict) else [],
        'equivalence_review': 'unreviewed',
        'semantic_validation': 'not_performed',
    }


def build_identity(profile, profile_hash):
    common = profile['common_specification']
    views = []
    for index, view in enumerate(profile['views']):
        vp = '/views/' + str(index)
        patch = view.get('specification_overrides', {})
        effective, sources = merge_with_sources(common, patch,
                                                '/common_specification',
                                                vp + '/specification_overrides')
        views.append({
            'view_id': view['view_id'],
            'source_pointer': vp,
            'algorithms': axis_record(view.get('algorithms'), vp + '/algorithms'),
            'guarantees': [axis_record(guarantee, vp + '/guarantees/' + str(gi))
                           | {'guarantee_id': guarantee['guarantee_id']}
                           for gi, guarantee in enumerate(view.get('guarantees', []))],
            'budget': axis_record(view.get('budget'), vp + '/budget'),
            'effective_specification': effective,
            'effective_leaf_sources': sources,
            'merge_review': 'mechanical_merge_only_not_mathematical_equivalence',
        })
    return {
        'schema_version': '1.0.0',
        'record_type': 'setting_identity',
        'setting_id': profile['setting_id'],
        'normalization_version': NORMALIZER_VERSION,
        'profile_version': SCHEMA_VERSION,
        'profile_sha256': profile_hash,
        'source_document': 'profile.json',
        'completeness': 'unreviewed',
        'normalization_scope': 'source_field_extraction_only',
        'matching_state': 'unreviewed',
        'missing_field_semantics': 'unknown_not_unrestricted',
        'axes': {axis: axis_record(common.get(key), '/common_specification/' + key)
                 for axis, key in AXES.items()},
        'parameters': {'source_pointer': '/parameters', 'cross_setting_alignment': 'unreviewed',
                       'parameter_ids': [item['id'] for item in profile.get('parameters', [])]},
        'regime_predicates': [{
            'regime_id': regime['id'], 'source_pointer': '/regimes/' + str(ri),
            'predicate_pointer': '/regimes/' + str(ri) + '/predicate',
            'evaluation_state': 'unparsed',
        } for ri, regime in enumerate(profile.get('regimes', []))],
        'view_override_policy': {
            'object_values': 'recursive_key_merge',
            'array_and_scalar_values': 'override_replaces_entire_value',
            'absent_override_keys': 'inherit_from_common_specification',
            'null': 'explicit_value_not_deletion',
            'limitations': 'Mechanical merge does not certify consistency or mathematical identity. '
                           'Narrative qualifications and source conditions remain authoritative.',
        },
        'views': views,
        'relations_source_pointer': '/relations',
        'matching_policy': {
            'candidate_retrieval': ['legacy_alias', 'declared_facets', 'text'],
            'accepted_relations': ['exact_match', 'same_setting_new_view', 'candidate_is_special_case',
                                   'candidate_is_generalization', 'partial_overlap', 'distinct',
                                   'undetermined'],
            'identity_decision': 'requires_explicit_axis_correspondences_and_review',
            'hash_semantics': 'file_integrity_only_not_mathematical_equivalence',
        },
    }


def human_label(value):
    return str(value).replace('_', ' ')


def catalog_record(profile, order):
    status = profile.get('summary_status', {})
    labels = {}
    for badge in status.get('badges', []) + status.get('special_statuses', []):
        labels[badge['code']] = badge.get('label', human_label(badge['code']))
    for code in status.get('gap_classes', []):
        labels.setdefault(code, human_label(code))
    for comparison in profile.get('comparisons', []):
        item = comparison.get('status', {})
        if item.get('code'):
            labels.setdefault(item['code'], item.get('label', human_label(item['code'])))
    facets = profile.get('facets', [])
    tags = list(dict.fromkeys(str(item['facet']) + ':' + str(item['value'])
                             for item in facets if 'facet' in item and 'value' in item))
    sid = profile['setting_id']
    return {
        'id': sid, 'title': profile['title'], 'domain': profile['primary_domain'],
        'statusCodes': list(labels), 'statusLabels': list(labels.values()),
        'tags': tags,
        'tagLabels': [human_label(tag.split(':', 1)[0]) + ': ' + human_label(tag.split(':', 1)[1])
                      for tag in tags],
        'views': len(profile['views']), 'comparisons': len(profile['comparisons']),
        'regimes': len(profile['regimes']), 'bounds': len(profile['bounds']),
        'order': order,
        'profile_path': 'settings/' + sid + '/profile.json',
        'identity_path': 'settings/' + sid + '/identity.json',
    }


def safe_id(sid):
    if not re.fullmatch(r'[A-Za-z0-9_\-]+', sid):
        raise ValueError('Unsafe source setting ID: ' + repr(sid))
    return sid


def run(source, count, snapshot=None):
    source = source.resolve()
    atlas = read_json(source / 'atlas.json')
    selected = atlas['settings'][:count]
    if count < 1 or count > len(atlas['settings']):
        raise ValueError('count must be positive and no greater than the source profile count')
    selected_ids = [safe_id(profile['setting_id']) for profile in selected]
    destinations = [DATA / 'settings' / sid for sid in selected_ids]
    if any(path.exists() for path in destinations):
        raise ValueError('Import refuses to overwrite an existing scientific setting')
    catalog = []
    for order, original in enumerate(selected, 1):
        sid = original['setting_id']
        active, _ = verified_formula_repairs(clean_profile(original))
        active['schema_version'] = SCHEMA_VERSION
        active['provenance'] = {'source_order': order}
        if snapshot:
            active['provenance']['source_snapshot'] = snapshot
        profile_path = DATA / 'settings' / sid / 'profile.json'
        write_json(profile_path, active)
        write_json(profile_path.with_name('identity.json'), build_identity(active, sha256(profile_path)))
        catalog.append(catalog_record(active, order))
    existing_path = DATA / 'derived' / 'catalog.json'
    existing = read_json(existing_path) if existing_path.exists() else {'profiles': []}
    existing['profiles'].extend(catalog)
    existing.update(profile_count=len(existing['profiles']), profile_schema_version=SCHEMA_VERSION)
    write_json(existing_path, existing)
    print(json.dumps({'imported': len(catalog), 'setting_ids': selected_ids}, ensure_ascii=False))


def build_vocabularies(selected, catalog):
    summary_codes, comparison_codes, tags = {}, {}, {}
    for profile in selected:
        summary = profile.get('summary_status', {})
        for kind in ['badges', 'special_statuses']:
            for item in summary.get(kind, []):
                summary_codes.setdefault(item['code'], {'code': item['code'], 'label': item['label'],
                                                        'source_scope': 'summary_status.' + kind})
        for comparison in profile.get('comparisons', []):
            item = comparison['status']
            comparison_codes.setdefault(item['code'], {'code': item['code'], 'label': item.get('label', human_label(item['code'])),
                                                        'source_scope': 'comparisons[].status'})
    for record in catalog:
        for tag, label in zip(record['tags'], record['tagLabels']):
            facet, value = tag.split(':', 1)
            tags.setdefault(tag, {'id': tag, 'facet': facet, 'value': value, 'label': label,
                                  'origin': 'source_facets', 'semantic_inference': False})
    write_json(DATA / 'vocabulary' / 'statuses.json', {
        'schema_version': '1.0.0', 'summary_statuses': list(summary_codes.values()),
        'comparison_statuses': list(comparison_codes.values()),
        'filter_semantics': 'OR within selected statuses; a setting matches any own summary or subregime status',
    })
    write_json(DATA / 'vocabulary' / 'tags.json', {
        'schema_version': '1.0.0', 'tags': list(tags.values()),
        'filter_semantics': 'AND across selected tags; only explicitly declared source facets are indexed',
    })


def build_schemas():
    obj = {'type': 'object'}
    arr = {'type': 'array'}
    profile = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': 'urn:complexity-atlas:profile:6.1.0',
        'title': 'Source-faithful active setting profile', 'type': 'object',
        'required': ['schema_version', 'setting_id', 'title', 'primary_domain', 'common_specification',
                     'views', 'parameters', 'symbols', 'quantities', 'resource_projections', 'regimes',
                     'bounds', 'comparisons', 'summary_status', 'proofs', 'evidence', 'references',
                     'facets', 'relations', 'aliases', 'provenance'],
        'properties': {
            'schema_version': {'const': SCHEMA_VERSION}, 'setting_id': {'type': 'string', 'minLength': 1},
            'title': {'type': 'string', 'minLength': 1}, 'primary_domain': {'type': 'string'},
            'common_specification': {'type': 'object', 'required': list(AXES.values())},
            'summary_status': obj,
            'provenance': {'type': 'object'},
            **{key: arr for key in ['views', 'parameters', 'symbols', 'quantities', 'resource_projections',
                                    'regimes', 'bounds', 'comparisons', 'proofs', 'evidence', 'references',
                                    'facets', 'relations', 'aliases']},
        },
        'propertyNames': {'not': {'enum': ['coverage', 'coverage_note']}},
        '$comment': 'Nested forbidden-field checks, source fidelity, foreign keys, and comparison scopes are enforced by validate_data.py.',
    }
    identity = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': 'urn:complexity-atlas:identity:1.0.0', 'type': 'object',
        'required': ['schema_version', 'record_type', 'setting_id', 'normalization_version',
                     'profile_sha256', 'axes', 'parameters', 'views', 'view_override_policy', 'matching_policy'],
        'properties': {'schema_version': {'const': '1.0.0'}, 'record_type': {'const': 'setting_identity'},
                       'setting_id': {'type': 'string'}, 'profile_sha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'},
                       'axes': {'type': 'object', 'required': list(AXES)}, 'views': arr},
    }
    comparison = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': 'urn:complexity-atlas:comparison-key:1.0.0', 'type': 'object',
        'required': ['setting_id', 'view_id', 'guarantee_id', 'quantity_id', 'resource_projection_id', 'regime_id'],
        'properties': {key: {'type': 'string', 'minLength': 1} for key in
                       ['setting_id', 'view_id', 'guarantee_id', 'quantity_id', 'resource_projection_id', 'regime_id']},
        'additionalProperties': False,
    }
    for filename, schema in [('profile.schema.json', profile), ('identity.schema.json', identity),
                             ('comparison-key.schema.json', comparison)]:
        write_json(DATA / 'schemas' / filename, schema)


def build_intake_template():
    write_json(DATA / 'intake' / 'candidate.template.json', {
        'schema_version': '1.0.0', 'record_type': 'setting_candidate', 'candidate_id': None,
        'workflow_status': 'candidate_unreviewed',
        'paper': {'title': None, 'authors': [], 'persistent_url': None, 'version': None, 'date': None},
        'declared_specification': {key: {'state': 'unknown', 'value': None, 'source_locator': None}
                                   for key in AXES},
        'theorem_records': [{'theorem_locator': None, 'direction': None, 'statement': None,
                              'formula_latex': None, 'parameter_region': None,
                              'actual_upper_witness_type': None, 'actual_lower_algorithm_scope': None}],
        'profile_resolution': {
            'action': 'unresolved', 'setting_id': None, 'view_id': None,
            'allowed_actions': ['update_existing_view', 'add_view_to_existing_profile', 'create_distinct_profile',
                                'needs_review', 'reject_as_incompatible'],
            'relation': 'undetermined', 'candidate_matches': [],
            'axis_correspondences': {key: {'result': 'unknown', 'source_locator': None, 'reason': None}
                                     for key in AXES},
            'legacy_alias_used': None, 'reason': None,
        },
        'required_correspondences': {key: None for key in ['instance_map', 'oracle_simulation', 'algorithm_class',
                                     'guarantee_conversion', 'quantity_alignment', 'resource_accounting', 'parameter_window']},
        'comparison_keys_affected': [],
        'admission': {'included_in_bracket': False, 'unresolved_conditions': [], 'reviewed_by': None, 'review_date': None},
    })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=pathlib.Path, required=True)
    parser.add_argument('--count', type=int, default=10)
    parser.add_argument('--snapshot', help='Optional source publication date or label')
    args = parser.parse_args()
    run(args.source, args.count, args.snapshot)
