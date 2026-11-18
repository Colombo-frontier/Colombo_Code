"""Display-only projection of native proposed tags into registered UI tags."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def at(value, pointer):
    if not pointer.startswith('/'):
        raise ValueError('Expected source pointer')
    for part in pointer[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def load_bridge(root):
    root = Path(root)
    source = root / 'data/tools/build_browse_index.py'
    spec = importlib.util.spec_from_file_location('registered_navigation_rules', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    registry = json.loads((root / 'data/derived/navigation_family_retention.json').read_text())
    return module, registry


def project(profile, classification, native, dictionary, root, rules, registry):
    known = {row['id']: row for row in dictionary['concepts']}
    proposed = {identity for view in native['views'] for identity in view['facet_ids']} - set(known)
    if not proposed:
        return native, None
    sid = profile['setting_id']
    views = [rules.BrowseView(profile, classification, view, index).build() for index, view in enumerate(profile['views'])]
    facets = {}
    def add(identity, vid, pointers, assertions, feature_ids=()):
        definition = known[identity]
        row = facets.setdefault(identity, {key: deepcopy(definition[key]) for key in ('axis', 'group', 'value', 'label')}
            | {'concept_id': identity, 'parent_id': definition.get('parent_id', definition['axis'] + ':' + definition['group']),
               'view_ids': [], 'source_pointers': [], 'source_feature_ids': [], 'evidence': [], 'display_level': 'navigation'})
        if vid not in row['view_ids']:
            row['view_ids'].append(vid)
        row['source_pointers'] = list(dict.fromkeys(row['source_pointers'] + list(pointers)))
        row['source_feature_ids'] = list(dict.fromkeys(row['source_feature_ids'] + list(feature_ids)))
        row['evidence'].append({'view_id': vid, 'assertions': deepcopy(assertions)})
    for view in views:
        for fact in view['facets']:
            if fact['id'] not in known:
                raise ValueError('Unregistered normalized navigation concept: ' + fact['id'])
            add(fact['id'], view['view_id'], fact['source_pointers'], fact['evidence'])
    retained = []
    for entry in registry['entries']:
        if entry['setting_id'] != sid:
            continue
        identity, old = entry['concept_id'], entry['facet']
        if identity in rules.OPTIONS or identity not in known:
            raise ValueError('Retention is restricted to already registered additional families')
        if any(old.get(key) != known[identity].get(key) for key in ('axis', 'group', 'value', 'label')):
            raise ValueError('Registered family identity/label mismatch')
        for premise in entry['source_values']:
            if digest(at(profile, premise['pointer'])) != premise['baseline_sha256']:
                raise ValueError('Changed retained navigation source: ' + sid + premise['pointer'])
        for vid in old['view_ids']:
            support = [row for row in entry['current_support'] if row['view_id'] == vid]
            if not support:
                raise ValueError('Retained family lacks same-view source support')
            for item in support:
                matches = [tag for tag in classification['tags'] if tag['id'] == item['precise_tag_id']
                           and vid in tag['view_ids'] and item['tag_source_pointer'] in tag['source_pointers']]
                if not matches:
                    raise ValueError('Retained family precise source support changed')
            pointers = [row['pointer'] for row in entry['source_values']]
            add(identity, vid, pointers, [{'rule_id': 'display.exact_unchanged_registered_family',
                'source_pointers': pointers, 'precise_tag_refs': sorted({row['precise_tag_id'] for row in support}),
                'explanation': 'Existing registered family retained only on exact canonical source values and current same-view precise support.', 'derived': False}])
            next(view for view in views if view['view_id'] == vid)['facet_ids'].append(identity)
        retained.append(identity)
    result = deepcopy(native)
    result['facets'] = list(facets.values())
    result['views'] = [{key: deepcopy(view[key]) for key in ('view_id', 'label', 'unknown_groups')}
                       | {'facet_ids': sorted(set(view['facet_ids']))} for view in views]
    for view in result['views']:
        for identity in view['facet_ids']:
            view['unknown_groups'].pop(known[identity].get('parent_id', known[identity]['axis'] + ':' + known[identity]['group']), None)
    if result['details'] != native['details']:
        raise ValueError('Display bridge changed native advanced tags')
    root = Path(root)
    files = {name: sha(root / 'data/settings' / sid / name) for name in ('profile.json', 'classification.json', 'human_tags.json')}
    audit = {'input_files': files, 'dictionary_sha256': sha(root / 'data/vocabulary/human_tags.json'),
             'raw_proposed_ids_not_registered_as_global_common': sorted(proposed), 'retained_registered_family_ids': retained,
             'tags': result, 'native_files_changed': False, 'scientific_credit': False}
    return result, audit
