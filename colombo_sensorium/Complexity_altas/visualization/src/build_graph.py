#!/usr/bin/env python3
"""Generate the offline setting graph from the active atlas and Toolkit label sidecars."""
import hashlib
import json
import shutil
from collections import defaultdict
from pathlib import Path

from catalog_order import load_ordered_catalog
from navigation_additions import apply_navigation_additions, load_navigation_additions

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent

GROUP_LABELS = {
    'TASK:family': 'Task family',
    'MODEL:objective_convexity': 'Objective convexity',
    'MODEL:monotonicity': 'Monotonicity',
    'MODEL:structure': 'Structure',
    'ORACLE:access': 'Oracle access',
    'ORACLE:quality': 'Primitive feedback quality',
    'ALGORITHMS:randomization': 'Randomization',
    'OUTPUT:object': 'Returned object',
    'METRIC:goal': 'Error and loss',
    'GUARANTEE:error_mode': 'Error guarantee',
    'RESOURCE:measure': 'Resource measure',
}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def json_hash(item):
    return hashlib.sha256(json.dumps(item, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def build_graph(root=ROOT):
    data = Path(root) / 'data'
    dist = Path(root) / 'visualization/dist'
    additions = load_navigation_additions(root)
    catalog = load_ordered_catalog(data / 'derived/catalog.json')['profiles']
    human = read(data / 'vocabulary/human_tags.json')
    machine = read(data / 'vocabulary/machine_tags.json')
    axes = [{'id': a['id'], 'label': a['label']} for a in human['axes']]
    settings = []
    dictionaries = {'human': human, 'machine': machine}
    definitions = {
        mode: {c.get('concept_id', c.get('id')): c for c in vocabulary['concepts']}
        for mode, vocabulary in dictionaries.items()
    }
    incidence = {mode: defaultdict(lambda: defaultdict(set)) for mode in dictionaries}
    declared = defaultdict(list)

    def add(mode, concept, position, view_ids, view_positions):
        if concept not in definitions[mode] or not view_ids or not set(view_ids) <= view_positions.keys():
            raise ValueError(f'Invalid {mode} graph membership: {settings[position]["id"]}/{concept}/{view_ids}')
        incidence[mode][concept][position].update(view_positions[v] for v in view_ids)

    for position, entry in enumerate(catalog):
        sid = entry['id']
        folder = data / 'settings' / sid
        profile = read(folder / 'profile.json')
        if entry['domain'] != profile['primary_domain']:
            raise ValueError(f'Catalog task differs from the profile primary domain: {sid}')
        navigation = apply_navigation_additions(read(folder / 'human_tags.json'), additions)
        precise = read(folder / 'machine_tags.json')
        profile_hash = json_hash(profile)
        if any(r['setting_id'] != sid or r['profile_sha256'] != profile_hash for r in [navigation, precise]):
            raise ValueError(f'Stale graph sidecar: {sid}')
        views = [{'id': v['view_id'], 'label': v['label']} for v in navigation['views']]
        view_positions = {v['id']: i for i, v in enumerate(views)}
        if set(view_positions) != set(entry['viewTagSets']) or set(view_positions) != set(precise['view_ids']):
            raise ValueError(f'View mismatch in graph data: {sid}')
        settings.append({'id': sid, 'title': entry['title'], 'views': views})
        for view in navigation['views']:
            for concept in view['facet_ids']:
                add('human', concept, position, [view['view_id']], view_positions)
        for feature in precise['features']:
            add('machine', feature['concept_id'], position, feature['view_ids'], view_positions)
        for i, relation in enumerate(profile.get('relations', [])):
            declared[relation.get('id', f'{sid}:{i}')].append({'setting_id': sid, 'source_pointer': f'/relations/{i}', 'relation': relation})

    layers = {}
    for mode, vocabulary in dictionaries.items():
        groups = {}
        for concept, d in definitions[mode].items():
            axis, group = d['axis'], d['group']
            gid = f'{axis}:{group}'
            g = groups.setdefault(gid, {'id': gid, 'axis': axis, 'label': GROUP_LABELS.get(gid, human['group_labels'].get(group, group.replace('_', ' ').capitalize())), 'concepts': []})
            members = incidence[mode].get(concept, {})
            g['concepts'].append({'id': concept, 'label': d['label'],
                                  'members': [[pos, sorted(views)] for pos, views in sorted(members.items())]})
        for group in groups.values():
            group['concepts'].sort(key=lambda c: c['label'].casefold())
        layers[mode] = sorted(groups.values(), key=lambda g: g['label'].casefold())

    relations = [{'id': rid, 'review_state': 'requires_relation_review', 'declarations': rows}
                 for rid, rows in sorted(declared.items())]
    graph = {
        'schema_version': '1.0.0', 'taxonomy_versions': {mode: v['version'] for mode, v in dictionaries.items()},
        'axes': axes, 'settings': settings, 'layers': layers,
        'declared_mathematical_relations': relations,
        'semantics': {'membership': 'Shared labels, groups and axes are classification links.',
                      'members': '[zero-based setting position, zero-based matching view positions]',
                      'relations': 'Source declarations requiring independent mathematical review.'},
    }
    encoded = json.dumps(graph, ensure_ascii=False, separators=(',', ':'))
    graph_path = data / 'derived/setting_graph.json'
    graph_path.write_text(encoded + '\n', encoding='utf-8')
    # Escape script delimiters. Keep the data intact; apply display terminology in graph.js.
    payload = encoded.replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    dist.mkdir(parents=True, exist_ok=True)
    (dist / 'assets').mkdir(exist_ok=True)
    for name in ('graph.js', 'graph.css'):
        shutil.copyfile(SRC / name, dist / 'assets' / name)
    template = (SRC / 'graph.template.html').read_text(encoding='utf-8')
    (dist / 'graph.html').write_text(template.replace('__GRAPH_DATA__', payload), encoding='utf-8')
    report = {
        'passed': True, 'settings': len(settings), 'views': sum(len(s['views']) for s in settings),
        'axes': len(axes), 'concepts': {mode: len(ds) for mode, ds in definitions.items()},
        'groups': {mode: len(groups) for mode, groups in layers.items()},
        'view_memberships': {mode: sum(len(v) for setting_views in values.values() for v in setting_views.values())
                             for mode, values in incidence.items()},
        'declared_relation_groups': len(relations), 'relation_declarations': sum(map(len, declared.values())),
        'sha256': hashlib.sha256(graph_path.read_bytes()).hexdigest(),
    }
    return report


if __name__ == '__main__':
    print(json.dumps(build_graph(), ensure_ascii=False))
