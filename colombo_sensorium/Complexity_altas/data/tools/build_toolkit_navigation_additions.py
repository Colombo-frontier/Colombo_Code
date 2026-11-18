#!/usr/bin/env python3
"""Add audited navigation memberships for literal optimization-ball domains."""
from __future__ import annotations

import json
from datetime import datetime, timezone

from import_toolkit_tags import HUMAN, ROOT, digest, pointer, read, require, write

OUTPUT = 'data/derived/toolkit_navigation_additions.json'
REPORT = 'data/audit/toolkit_navigation_additions.json'
BALL = 'MODEL:geometry_family:ball'
RULE = 'local.explicit_optimization_ball'
ROLE_PATH = '/model/domain_roles/optimization'
LITERAL_BALLS = {'B_2(0,R)', 'B_2(0,1)', 'B_p(0,R)'}
TRIPLE = {'ORACLE:access:zero', 'ORACLE:quality:exact', 'MODEL:objective_convexity:convex'}


def optimization_domain(profile, index):
    """Resolve the one field under the Toolkit's recursive override policy."""
    override = profile['views'][index].get('specification_overrides', {})
    if 'model' in override:
        model_override = override['model']
        if not isinstance(model_override, dict):
            return None, None
        if 'domain_roles' in model_override:
            role_override = model_override['domain_roles']
            if not isinstance(role_override, dict):
                return None, None
            if 'optimization' in role_override:
                return f'/views/{index}/specification_overrides{ROLE_PATH}', role_override['optimization']
    roles = profile['common_specification']['model'].get('domain_roles')
    if isinstance(roles, dict) and 'optimization' in roles:
        return '/common_specification' + ROLE_PATH, roles['optimization']
    return None, None


def literal_ball(domain):
    if not isinstance(domain, str):
        return False
    value = ''.join(domain.split())
    if len(value) >= 2 and value[0] == value[-1] == '$':
        value = value[1:-1]
    return value in LITERAL_BALLS


def view_assertion(profile, index):
    source_pointer, value = optimization_domain(profile, index)
    if not literal_ball(value):
        return None
    require(pointer(profile, source_pointer) == value, f'Invalid overlay source pointer: {source_pointer}')
    return {'view_id': profile['views'][index]['view_id'], 'assertions': [{
        'source_pointer': source_pointer, 'source_pointers': [source_pointer], 'source_value': value,
        'rule_id': RULE, 'derived': True,
        'explanation': 'This view explicitly names a ball as its optimization domain.',
    }]}


def fixtures(settings, before, after):
    positives = ['SO_ZO_E01', 'SO_ZO_E02', 'SO_ZO_E06b', 'SO_ZO_E06e',
                 'SO_ZO_E07_neighborhood', 'SO_ZO_E09c', 'SO_ZO_E09c_sc']
    excluded = ['SO_ZO_E03', 'SO_ZO_E06d', 'SO_ZO_N04a_gaussian', 'SO_ZO_C15a_rand_native']
    checks = [{'setting_id': sid, 'check': 'literal ball and same-view Exact/Zero/Convex',
               'passed': sid in settings and sid in after} for sid in positives]
    checks.extend({'setting_id': sid, 'check': 'localization, query or trust radius grants no optimization-ball membership',
                   'passed': sid not in settings and sid not in after} for sid in excluded)
    checks.append({'setting_id': 'SO_ZO_N01_main', 'check': 'explicit ball with noisy feedback stays outside Exact',
                   'passed': 'SO_ZO_N01_main' in settings and 'SO_ZO_N01_main' not in after})
    # These exercise the override branch even though the current literal-ball
    # profiles inherit their optimization domain from the common specification.
    profile = {'common_specification': {'model': {'domain_roles': {'optimization': 'B_2(0,R)'}}},
               'views': [{'view_id': 'test', 'specification_overrides': {}}]}
    view = profile['views'][0]
    view['specification_overrides'] = {'model': {'domain_roles': {'optimization': 'R^d'}}}
    checks.append({'check': 'view-level full space replaces the common ball', 'passed': view_assertion(profile, 0) is None})
    view['specification_overrides'] = {'model': {'domain_roles': {'query': 'B_2(0,1)'}}}
    assertion = view_assertion(profile, 0)
    checks.append({'check': 'view-level query change retains the common optimization domain',
                   'passed': assertion['assertions'][0]['source_pointer'] == '/common_specification' + ROLE_PATH})
    view['specification_overrides'] = {'model': {'domain_roles': {'optimization': 'B_2(0,1)'}}}
    assertion = view_assertion(profile, 0)
    checks.append({'check': 'explicit view optimization ball points to the override value',
                   'passed': assertion['assertions'][0]['source_pointer'] == '/views/0/specification_overrides' + ROLE_PATH})
    return {'passed': all(item['passed'] for item in checks), 'checks': checks,
            'combination_before': before, 'combination_after': after}


def build():
    catalog = read(ROOT, 'data/derived/catalog.json')
    dictionary = read(ROOT, HUMAN)
    definition = next(item for item in dictionary['concepts'] if item['concept_id'] == BALL)
    settings, before, after = {}, {}, {}
    imported_ball_views = 0
    imported_ball_settings = 0
    for record in catalog['profiles']:
        sid = record['id']
        base = ROOT / 'data/settings' / sid
        profile_bytes = (base / 'profile.json').read_bytes()
        human_bytes = (base / 'human_tags.json').read_bytes()
        profile, human = json.loads(profile_bytes), json.loads(human_bytes)
        evidence = []
        existing = 0
        for index, view in enumerate(human['views']):
            vid, facets = view['view_id'], set(view['facet_ids'])
            require(profile['views'][index]['view_id'] == vid, f'View alignment failed: {sid}')
            if BALL in facets:
                existing += 1
                if TRIPLE <= facets:
                    before.setdefault(sid, []).append(vid)
            else:
                assertion = view_assertion(profile, index)
                if assertion:
                    evidence.append(assertion)
                    facets.add(BALL)
            if TRIPLE | {BALL} <= facets:
                after.setdefault(sid, []).append(vid)
        imported_ball_views += existing
        imported_ball_settings += bool(existing)
        if evidence:
            facet = {key: definition[key] for key in ['concept_id', 'axis', 'group', 'parent_id', 'value', 'label', 'display_level']}
            facet.update({'view_ids': [item['view_id'] for item in evidence],
                          'source_pointers': list(dict.fromkeys(item['assertions'][0]['source_pointer'] for item in evidence)),
                          'source_feature_ids': [], 'evidence': evidence})
            settings[sid] = {'profile_sha256': human['profile_sha256'], 'profile_file_sha256': digest(profile_bytes),
                             'human_tags_file_sha256': digest(human_bytes), 'facets': [facet]}

    checks = fixtures(settings, before, after)
    require(checks['passed'], f'Optimization-ball regression failed: {checks}')
    added_views = sum(len(record['facets'][0]['view_ids']) for record in settings.values())
    counts = {'added_settings': len(settings), 'added_views': added_views, 'original_ball_settings': imported_ball_settings,
              'original_ball_views': imported_ball_views, 'combination_before_settings': len(before),
              'combination_after_settings': len(after), 'combination_after_views': sum(map(len, after.values()))}
    payload = {'schema_version': '1.0.0', 'rule_id': RULE, 'concept_id': BALL, 'counts': counts, 'settings': settings}
    encoded = (json.dumps(payload, ensure_ascii=False, indent=2) + '\n').encode()
    report = {'schema_version': '1.0.0', 'passed': True, 'rule_id': RULE,
              'created_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
              'rule_scope': 'Exact literal values in the effective model.domain_roles.optimization field.',
              'supported_literals': sorted(LITERAL_BALLS),
              'overlay_sha256': digest(encoded), 'counts': counts, 'regression': checks}
    write(ROOT / OUTPUT, encoded)
    return counts


if __name__ == '__main__':
    print(json.dumps(build()))
