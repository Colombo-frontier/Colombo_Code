#!/usr/bin/env python3
"""Rebuild public indexes from native records and registered display rules.

Writes only toolkit_browser.json and toolkit_tag_graph.json. Membership is not
a reduction, and a source-declared relation is not a new accepted theorem.
"""
from copy import deepcopy
from collections import defaultdict
from pathlib import Path
import argparse
import base64
import gzip
import hashlib
import importlib.util
import json
import os
import tempfile

ROOT = Path(__file__).resolve().parents[2]
NATIVE = ('profile.json', 'identity.json', 'classification.json', 'human_tags.json', 'machine_tags.json')
OUTPUTS = ('data/derived/toolkit_browser.json', 'data/derived/toolkit_tag_graph.json')


def require(value, message):
    if not value:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(root, name):
    path = root / name
    require(path.is_file() and not path.is_symlink(), 'Expected a regular index input: ' + name)
    return json.loads(path.read_bytes())


def unique(rows, key, label):
    result = {row[key]: row for row in rows}
    require(len(result) == len(rows), 'Duplicate native identity: ' + label)
    return result


def at(value, pointer):
    require(isinstance(pointer, str) and pointer.startswith('/'), 'Invalid native pointer')
    for part in pointer[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def load_module(root, relative, name):
    spec = importlib.util.spec_from_file_location(name, root / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def browser_record(profile, human, machine):
    """Same native/display record shape as the original Toolkit projection."""
    facets = [{key: facet[key] for key in ('concept_id', 'axis', 'group', 'label', 'view_ids')}
              for facet in human['facets']]
    search = [profile['setting_id'], profile['title'], profile.get('summary', '')]
    search += [item['label'] for item in facets + human['details']]
    search += [item['concept_id'] for item in machine['features']]
    return {'id': profile['setting_id'], 'title': profile['title'], 'primary_domain': profile['primary_domain'],
            'summary': profile.get('summary', ''), 'views': human['views'], 'facets': facets,
            'details': human['details'], 'interface_notes': human['interface_notes'],
            'status': deepcopy(profile['summary_status']), 'search_text': ' '.join(item for item in search if item),
            'machine_gzip_base64': base64.b64encode(gzip.compress(canonical(machine), mtime=0)).decode(),
            'contract_sections': {axis: [facet['label'] for facet in facets if facet['axis'] == axis]
                                  for axis in machine['axis_coverage']}}


def hierarchy(human, machine):
    groups = defaultdict(lambda: {'human_concept_ids': [], 'machine_concept_ids': []})
    for layer, vocabulary in [('human', human), ('machine', machine)]:
        for concept in vocabulary['concepts']:
            groups[concept['axis'], concept['group']][layer + '_concept_ids'].append(concept['concept_id'])
    axes = []
    for axis in human['axes']:
        children = []
        for (owner, key), members in sorted(groups.items()):
            if owner == axis['id']:
                group_id = owner + ':' + key
                children.append({'id': group_id, 'key': key,
                                 'label': human['group_labels'].get(group_id, key.replace('_', ' ').capitalize()),
                                 **members})
        axes.append({'id': axis['id'], 'label': axis['label'], 'groups': children})
    return {'axes': axes, 'concept_identity': ['layer', 'concept_id']}


def declared_relations(profiles, input_hashes):
    declarations, grouped, notes = [], defaultdict(list), []
    for sid, profile in profiles.items():
        for index, relation in enumerate(profile.get('relations', [])):
            pointer = '/relations/' + str(index)
            require(isinstance(relation, dict), 'A native relation declaration must be an object')
            if 'id' in relation:
                require(isinstance(relation['id'], str) and relation['id'], 'An explicit native relation ID must be nonempty')
            row = {'declared_in_setting': sid, 'source_pointer': pointer, 'relation': deepcopy(relation),
                   'source_profile_sha256': input_hashes['data/settings/' + sid + '/profile.json'],
                   'source_value_sha256': digest(relation)}
            declarations.append({**row, 'target_in_pilot': relation.get('target_ref', relation.get('target_setting_id')) in profiles})
            if 'id' in relation:
                grouped[relation['id']].append(row)
            else:
                # Keep source notes by their real pointer, without inventing a
                # global relation ID or promoting them to mathematical claims.
                notes.append({**row, 'review_state': 'unreviewed_native_relation_note'})
    groups = []
    for identity, rows in sorted(grouped.items()):
        endpoints = {(row['relation'].get('source_ref'), row['relation'].get('target_ref'),
                      row['relation'].get('relation_kind')) for row in rows}
        groups.append({'relation_id': identity, 'declarations': rows,
                       'endpoint_conflict': len(endpoints) != 1,
                       'payload_variants': len({digest(row['relation']) for row in rows}),
                       'review_state': 'requires_relation_review',
                       'note': 'Native declarations are reproduced exactly; no acceptance, equivalence or contradiction is inferred from wording variation.'})
    return declarations, groups, notes


def classification_graph(profiles, machines, vocabulary, groups, notes):
    concepts = unique(vocabulary['concepts'], 'concept_id', 'machine vocabulary')
    axes = unique(vocabulary['axes'], 'id', 'machine axes')
    nodes = [{'id': 'setting:' + sid, 'kind': 'setting', 'setting_id': sid, 'label': profile['title']}
             for sid, profile in profiles.items()]
    nodes += [{'id': 'axis:' + key, 'kind': 'axis', 'label': value['label']} for key, value in axes.items()]
    group_ids = sorted({(item['axis'], item['group']) for item in concepts.values()})
    nodes += [{'id': 'group:' + axis + ':' + key, 'kind': 'group', 'axis': axis, 'label': key}
              for axis, key in group_ids]
    nodes += [{'id': 'concept:' + cid, 'kind': 'concept', 'concept_id': cid,
               'axis': item['axis'], 'group': item['group'], 'label': item['label']}
              for cid, item in concepts.items()]
    edges = [{'source': 'group:' + axis + ':' + key, 'target': 'axis:' + axis,
              'kind': 'in_group', 'layer': 'classification', 'mathematical_relation': False}
             for axis, key in group_ids]
    edges += [{'source': 'concept:' + cid, 'target': 'group:' + item['axis'] + ':' + item['group'],
               'kind': 'in_group', 'layer': 'classification', 'mathematical_relation': False}
              for cid, item in concepts.items()]
    for sid, machine in machines.items():
        for index, feature in enumerate(machine['features']):
            cid = feature['concept_id']
            require(cid in concepts, 'Unregistered precise concept: ' + cid)
            edges.append({'source': 'setting:' + sid, 'target': 'concept:' + cid,
                          'kind': 'has_concept', 'layer': 'classification', 'mathematical_relation': False,
                          'feature_id': feature['feature_id'], 'view_ids': deepcopy(feature['view_ids']),
                          'source_file': 'data/settings/' + sid + '/machine_tags.json',
                          'source_pointer': '/features/' + str(index), 'source_value_sha256': digest(feature)})
    node_ids = unique(nodes, 'id', 'graph nodes')
    require(all(edge['source'] in node_ids and edge['target'] in node_ids for edge in edges), 'Dangling graph edge')
    return {'schema_version': '1.0.0', 'nodes': nodes, 'edges': edges,
            'declared_mathematical_relations': groups, 'native_relation_notes_without_ids': notes, 'proposals': [],
            'semantics': {'classification': 'Shared labels and group membership do not establish reductions or equivalence.',
                          'mathematical': 'All native declarations remain requires_relation_review; this rebuild grants no relation-review credit.',
                          'projection': 'Only exact native feature incidences and registered hierarchy edges are emitted; no all-pairs similarity edges.'}}


def build(root):
    root = Path(root).resolve()
    ids = sorted(path.parent.name for path in (root / 'data/settings').glob('*/profile.json'))
    require(ids and len(ids) == len(set(ids)), 'Empty or duplicate native setting inventory')
    paths = ['data/settings/' + sid + '/' + name for sid in ids for name in NATIVE]
    dependencies = ['data/vocabulary/human_tags.json', 'data/vocabulary/machine_tags.json',
                    'data/derived/navigation_family_retention.json', 'data/tools/build_browse_index.py',
                    'data/tools/build_public_indexes.py',
                    'visualization/src/public_navigation_bridge.py', 'visualization/src/navigation_additions.py']
    if (root / 'data/derived/toolkit_navigation_additions.json').is_file():
        dependencies.append('data/derived/toolkit_navigation_additions.json')
    input_hashes = {name: sha(root / name) for name in paths + dependencies}
    human_vocab = read(root, 'data/vocabulary/human_tags.json')
    machine_vocab = read(root, 'data/vocabulary/machine_tags.json')
    registered = unique(human_vocab['concepts'], 'concept_id', 'registered navigation concepts')
    machine_ids = unique(machine_vocab['concepts'], 'concept_id', 'registered precise concepts')
    bridge = load_module(root, 'visualization/src/public_navigation_bridge.py', 'public_index_navigation_bridge')
    additions = load_module(root, 'visualization/src/navigation_additions.py', 'public_index_navigation_additions')
    rules, registry = bridge.load_bridge(root)
    extra = additions.load_navigation_additions(root)
    profiles, machines, shown, projection_rows = {}, {}, {}, {}
    for sid in ids:
        base = 'data/settings/' + sid + '/'
        profile = profiles[sid] = read(root, base + 'profile.json')
        native_human = read(root, base + 'human_tags.json')
        machine = machines[sid] = read(root, base + 'machine_tags.json')
        classification = read(root, base + 'classification.json')
        require(all(read(root, base + name)['setting_id'] == sid for name in NATIVE), 'Native five-file identity mismatch')
        require(classification['profile_sha256'] == input_hashes[base + 'profile.json'], 'Stale classification: ' + sid)
        for tags in (native_human, machine):
            require(tags['profile_sha256'] == digest(profile), 'Stale native tags: ' + sid)
        views = unique(profile['views'], 'view_id', sid + ' views')
        require(machine['view_ids'] == list(views) == native_human['view_ids'], 'Native view identity/order mismatch')
        unique(machine['features'], 'feature_id', sid + ' machine features')
        for feature in machine['features']:
            require(feature['concept_id'] in machine_ids and set(feature['view_ids']) <= set(views), 'Unregistered feature or wrong view')
            for binding in feature.get('bindings', []):
                if binding.get('pointer_state') == 'resolved':
                    source_value = at(profile, binding['source_pointer'])
                    if 'source_value' in binding:
                        require(source_value == binding['source_value'], 'Stale exact feature binding')
                    if 'source_value_sha256' in binding:
                        require(digest(source_value) == binding['source_value_sha256'], 'Stale hashed feature binding')
        display, audit = bridge.project(profile, classification, deepcopy(native_human), human_vocab, root, rules, registry)
        display = additions.apply_navigation_additions(display, extra)
        require(display['details'] == native_human['details'], 'Display projection changed native precise details')
        require({v['view_id'] for v in display['views']} == set(views), 'Display projection changed native views')
        require(all(set(v['facet_ids']) <= set(registered) for v in display['views']), 'Display projection invented a navigation concept')
        require(all(f['concept_id'] in registered for f in display['facets']), 'Display facet is not registered')
        shown[sid] = browser_record(profile, display, machine)
        projection_rows[sid] = {'input_files': {name: input_hashes[base + name] for name in NATIVE},
                                'native_human_tags_sha256': input_hashes[base + 'human_tags.json'],
                                'projected_display_tags_canonical_sha256': digest(display),
                                'bridge_applied': audit is not None, 'native_files_changed': False,
                                'raw_proposed_ids_registered': False, 'scientific_credit': False}
        shown[sid]['source'] = projection_rows[sid]
    declarations, groups, notes = declared_relations(profiles, input_hashes)
    graph = classification_graph(profiles, machines, machine_vocab, groups, notes)
    revision = 'public-native-projection-' + digest(input_hashes)[:24]
    graph.update(release_id=revision, provenance={'kind': 'native_feature_and_declared_relation_projection',
                 'input_hashes': input_hashes, 'scientific_credit': False})
    stats = {'settings': len(ids), 'views': sum(len(p['views']) for p in profiles.values()),
             'navigation_concepts': len(registered), 'precise_concepts': len(machine_ids),
             'machine_feature_assertions': sum(len(m['features']) for m in machines.values())}
    browser = {'version': '1.0.0', 'revision': revision, 'dictionary': deepcopy(human_vocab),
               'settings': [shown[sid] for sid in ids], 'relations': declarations,
               'taxonomy_hierarchy': hierarchy(human_vocab, machine_vocab), 'stats': stats,
               'provenance': {'kind': 'registered_display_projection', 'graph_path': OUTPUTS[1],
                              'input_hashes': input_hashes, 'native_files_changed': False,
                              'no_new_global_navigation_ids': True, 'scientific_credit': False}}
    # Counts describe this display projection, without changing vocabulary definitions/IDs.
    for concept in browser['dictionary']['concepts']:
        cid = concept['concept_id']
        members = [r for r in shown.values() if any(f['concept_id'] == cid for f in r['facets'])]
        concept['setting_count'] = len(members)
        concept['view_count'] = sum(len({vid for f in r['facets'] if f['concept_id'] == cid for vid in f['view_ids']}) for r in members)
    for detail in browser['dictionary'].get('detail_concepts', []):
        cid = detail['machine_concept_id']
        detail['setting_count'] = sum(any(f['concept_id'] == cid for f in m['features']) for m in machines.values())
    require(all(sha(root / name) == expected for name, expected in input_hashes.items()), 'Index inputs changed during projection')
    return {OUTPUTS[0]: browser, OUTPUTS[1]: graph}, input_hashes


def output_path(root, name):
    """A fixed derived output may not traverse an alias below its Atlas root."""
    destination = root / name
    current = root
    for part in Path(name).parts[:-1]:
        current = current / part
        require(not current.is_symlink(), 'Index output ancestor must not be a symlink')
        require(not current.exists() or current.is_dir(), 'Index output ancestor must be a directory')
        require(current.resolve().is_relative_to(root), 'Index output ancestor escapes its Atlas root')
    require(not destination.is_symlink(), 'Index output must not be a symlink')
    require(destination.resolve().is_relative_to(root), 'Index output escapes its Atlas root')
    return destination


def write_indexes(root, payloads, input_hashes):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'Atlas output root must be a regular directory, not a symlink')
    root = root.resolve()
    require(set(payloads) == set(OUTPUTS), 'Only the two public indexes can be written')
    require(all(sha(root / name) == expected for name, expected in input_hashes.items()), 'Native/dependency drift before index write')
    # Check both complete paths before creating any directory or temporary file.
    for name in OUTPUTS:
        output_path(root, name)
    for name in reversed(OUTPUTS):
        destination = output_path(root, name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        output_path(root, name)
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.public-index-', delete=False) as stream:
            temporary = Path(stream.name)
            try:
                stream.write(canonical(payloads[name]) + b'\n');stream.flush();os.fsync(stream.fileno())
                temporary.replace(destination)
            finally:
                temporary.unlink(missing_ok=True)
    require(all(sha(root / name) == expected for name, expected in input_hashes.items()), 'Native/dependency drift during index write')
    return {'settings': payloads[OUTPUTS[0]]['stats']['settings'], 'revision': payloads[OUTPUTS[0]]['revision'],
            'indexes': {name: sha(root / name) for name in OUTPUTS}, 'canonical_native_files_changed': False,
            'scientific_credit': False, 'relation_declarations': len(payloads[OUTPUTS[0]]['relations'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--check', action='store_true', help='Validate/project without writing either index')
    args = parser.parse_args()
    payloads, inputs = build(args.root)
    if args.check:
        print(json.dumps({'settings': payloads[OUTPUTS[0]]['stats']['settings'], 'write_performed': False}))
    else:
        print(json.dumps(write_indexes(args.root, payloads, inputs), ensure_ascii=False))


if __name__ == '__main__':
    main()
