#!/usr/bin/env python3
"""Import the Toolkit's two existing tag projections into this Atlas.

The Toolkit files are input data. The import uses their published JSON and
checks it against the local profiles before writing the additive tag files.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import os
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = 'data/audit/toolkit_tags.json'
HUMAN = 'data/vocabulary/human_tags.json'
MACHINE = 'data/vocabulary/machine_tags.json'
GRAPH = 'data/derived/toolkit_tag_graph.json'
BROWSER = 'data/derived/toolkit_browser.json'


def read(root, path):
    return json.loads((root / path).read_bytes())


def digest(content):
    return hashlib.sha256(content).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def pointer(value, path):
    if path and not path.startswith('/'):
        raise ValueError(f'Invalid JSON pointer: {path!r}')
    for part in path[1:].split('/') if path else []:
        key = part.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_bytes() == content:
        return
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.toolkit-tags-', delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def indexed(rows, field, label):
    result = {row[field]: row for row in rows}
    require(len(result) == len(rows), f'Duplicate {field} in {label}')
    return result


def validate_setting(sid, profile, classification, human, machine, human_vocab, machine_vocab):
    """Validate exact provenance, membership scope and source evidence."""
    views = indexed(profile['views'], 'view_id', sid)
    hviews = indexed(human['views'], 'view_id', f'{sid} human views')
    canonical_sha = digest(canonical(profile))
    for tags in [human, machine]:
        require(tags['setting_id'] == sid and tags['profile_sha256'] == canonical_sha, f'Stale tag record: {sid}')
        require(tags['view_ids'] == list(views), f'Tag view order mismatch: {sid}')
    require(list(hviews) == list(views), f'Human view order mismatch: {sid}')
    require(human['title'] == profile['title'], f'Human title mismatch: {sid}')
    require(machine['source_classification_profile_sha256'] == classification['profile_sha256'], f'Classification hash mismatch: {sid}')
    require(machine['registry'] == profile['registry'], f'Machine registry mismatch: {sid}')
    require(machine['operation_bindings'] == classification['operation_bindings'], f'Operation bindings mismatch: {sid}')

    original = indexed(classification['tags'], 'id', f'{sid} source tags')
    features = indexed(machine['features'], 'feature_id', f'{sid} machine features')
    concepts = indexed(machine['features'], 'concept_id', f'{sid} machine concepts')
    require(concepts.keys() == original.keys(), f'Missing or extra precise concepts: {sid}')
    for cid, feature in concepts.items():
        source = original[cid]
        require(cid in machine_vocab, f'Unknown machine concept: {sid} {cid}')
        require(feature['feature_id'] == 'feat_' + digest(canonical([sid, cid]))[:20], f'Feature ID mismatch: {sid} {cid}')
        for key in ['axis', 'group', 'value', 'label', 'view_ids', 'source_pointers', 'evidence_state']:
            require(feature[key] == source[key], f'Machine feature {key} mismatch: {sid} {cid}')
        require(feature['source_evidence'] == source['evidence'], f'Machine evidence mismatch: {sid} {cid}')
        for binding in feature['bindings']:
            require(set(binding['view_ids']) <= set(feature['view_ids']), f'Machine binding outside its view: {sid} {cid}')
            if binding['pointer_state'] == 'resolved':
                require(pointer(profile, binding['source_pointer']) == binding['source_value'], f'Machine source value mismatch: {sid} {cid}')

    facets = indexed(human['facets'], 'concept_id', f'{sid} human facets')
    for cid, facet in facets.items():
        require(cid in human_vocab, f'Unknown navigation concept: {sid} {cid}')
        require(set(facet['view_ids']) <= views.keys() and facet['view_ids'], f'Invalid facet view scope: {sid} {cid}')
        require(set(facet['source_feature_ids']) <= features.keys(), f'Missing facet source feature: {sid} {cid}')
        for path in facet['source_pointers']:
            pointer(profile, path)
        require({entry['view_id'] for entry in facet['evidence']} == set(facet['view_ids']), f'Facet evidence scope mismatch: {sid} {cid}')
        for entry in facet['evidence']:
            for assertion in entry['assertions']:
                for path in assertion.get('source_pointers', []):
                    pointer(profile, path)
                for precise in assertion.get('precise_tag_refs', []):
                    require(precise in concepts and entry['view_id'] in concepts[precise]['view_ids'], f'Facet assertion crosses views: {sid} {cid} {precise}')
    for vid, view in hviews.items():
        expected = {cid for cid, facet in facets.items() if vid in facet['view_ids']}
        require(len(set(view['facet_ids'])) == len(view['facet_ids']) and set(view['facet_ids']) == expected, f'Human membership mismatch: {sid} {vid}')
    details = indexed(human['details'], 'machine_concept_id', f'{sid} human details')
    require(details.keys() == concepts.keys(), f'Detail concepts mismatch: {sid}')
    for cid, detail in details.items():
        feature = concepts[cid]
        require(detail['concept_id'] == 'detail:' + cid and detail['view_ids'] == feature['view_ids']
                and detail['source_feature_ids'] == [feature['feature_id']], f'Detail scope or feature mismatch: {sid} {cid}')
    for note in human['interface_notes']:
        require(set(note['view_ids']) <= views.keys(), f'Invalid native interface note scope: {sid}')
        for path in note.get('source_pointers', []):
            pointer(profile, path)


def hierarchy(human, machine):
    groups = defaultdict(lambda: {'human_concept_ids': [], 'machine_concept_ids': []})
    for layer, vocabulary in [('human', human), ('machine', machine)]:
        for concept in vocabulary['concepts']:
            group = groups[(concept['axis'], concept['group'])]
            group[layer + '_concept_ids'].append(concept['concept_id'])
    axes = []
    for axis in human['axes']:
        axis_id = axis['id']
        children = []
        for (owner, key), members in sorted(groups.items()):
            if owner == axis_id:
                group_id = owner + ':' + key
                children.append({'id': group_id, 'key': key,
                                 'label': human['group_labels'].get(group_id, key.replace('_', ' ').capitalize()),
                                 **members})
        axes.append({'id': axis_id, 'label': axis['label'], 'groups': children})
    return {'axes': axes, 'concept_identity': ['layer', 'concept_id']}


def browser_record(profile, human, machine):
    facets = [{key: facet[key] for key in ['concept_id', 'axis', 'group', 'label', 'view_ids']} for facet in human['facets']]
    search = [profile['setting_id'], profile['title'], profile.get('summary', '')]
    search += [item['label'] for item in facets + human['details']]
    search += [item['concept_id'] for item in machine['features']]
    return {'id': profile['setting_id'], 'title': profile['title'], 'primary_domain': profile['primary_domain'],
            'summary': profile.get('summary', ''), 'views': human['views'], 'facets': facets,
            'details': human['details'], 'interface_notes': human['interface_notes'],
            'status': profile['summary_status'], 'search_text': ' '.join(item for item in search if item),
            'machine_gzip_base64': base64.b64encode(gzip.compress(canonical(machine), mtime=0)).decode(),
            'contract_sections': {axis: [facet['label'] for facet in facets if facet['axis'] == axis]
                                  for axis in machine['axis_coverage']}}


def validate_graph(graph, profiles, machine_rows):
    nodes = indexed(graph['nodes'], 'id', 'Toolkit graph')
    actual_incidence = set()
    expected_incidence = {(f'setting:{sid}', f'concept:{item["concept_id"]}', item['feature_id'], tuple(item['view_ids']))
                          for sid, machine in machine_rows.items() for item in machine['features']}
    for edge in graph['edges']:
        require(edge['source'] in nodes and edge['target'] in nodes, f'Dangling Toolkit graph edge: {edge}')
        if edge['kind'] == 'has_concept':
            require(edge.get('mathematical_relation') is False, f'Graph membership improperly asserts a relation: {edge}')
            record = (edge['source'], edge['target'], edge['feature_id'], tuple(edge['view_ids']))
            require(record not in actual_incidence, f'Duplicate Toolkit incidence: {record}')
            actual_incidence.add(record)
    require(actual_incidence == expected_incidence, 'Toolkit graph incidence differs from machine memberships')
    actual_relations = set()
    for group in graph['declared_mathematical_relations']:
        for entry in group['declarations']:
            sid, path = entry['declared_in_setting'], entry['source_pointer']
            require(pointer(profiles[sid], path) == entry['relation'], f'Graph relation differs from local profile: {sid} {path}')
            actual_relations.add((sid, path))
    expected_relations = {(sid, f'/relations/{index}') for sid, profile in profiles.items()
                          for index, _ in enumerate(profile.get('relations', []))}
    require(actual_relations == expected_relations, 'Toolkit graph omitted source relation declarations')
    return {'nodes': len(nodes), 'edges': len(graph['edges']), 'machine_incidence_edges': len(actual_incidence),
            'declared_relation_groups': len(graph['declared_mathematical_relations']), 'relation_declarations': len(actual_relations)}


def import_tags(root, source):
    catalog = read(root, 'data/derived/catalog.json')
    ids = [item['id'] for item in catalog['profiles']]
    local_ids = {p.parent.name for p in (root / 'data/settings').glob('*/profile.json')}
    source_ids = {p.parent.name for p in (source / 'data/settings').glob('*/profile.json')}
    require(len(ids) == len(set(ids)) and set(ids) == local_ids == source_ids, 'Catalog, local profiles and Toolkit have different setting IDs')
    human = read(source, HUMAN)
    machine = read(source, MACHINE)
    human_vocab = indexed(human['concepts'], 'concept_id', 'Toolkit human vocabulary')
    machine_vocab = indexed(machine['concepts'], 'concept_id', 'Toolkit machine vocabulary')
    detail_vocab = indexed(human['detail_concepts'], 'machine_concept_id', 'Toolkit detail vocabulary')
    require(detail_vocab.keys() == machine_vocab.keys(), 'Toolkit human details do not cover the machine vocabulary')
    summary = read(source, 'data/derived/tag_summary.json')
    revision = read(source, 'data/state/active.json')['release_id']
    graph = read(source, 'data/derived/graph.json')
    require(graph['release_id'] == revision, 'Toolkit graph and active release IDs differ')
    profiles, hrows, mrows, profile_audit = {}, {}, {}, []
    imported = {HUMAN: HUMAN, MACHINE: MACHINE, GRAPH: 'data/derived/graph.json'}
    graph_edges, tag_counts = {}, {}
    for sid in ids:
        base = f'data/settings/{sid}/'
        local_hashes, source_hashes = {}, {}
        for filename in ['profile.json', 'classification.json', 'identity.json']:
            local_bytes = (root / (base + filename)).read_bytes()
            source_bytes = (source / (base + filename)).read_bytes()
            require(json.loads(local_bytes) == json.loads(source_bytes), f'Toolkit differs from canonical {filename}: {sid}')
            local_hashes[filename] = digest(local_bytes)
            source_hashes[filename] = digest(source_bytes)
        profile = profiles[sid] = read(root, base + 'profile.json')
        classification = read(root, base + 'classification.json')
        require(classification['profile_sha256'] == local_hashes['profile.json'], f'Local classification has a stale byte hash: {sid}')
        hrow = hrows[sid] = read(source, base + 'human_tags.json')
        mrow = mrows[sid] = read(source, base + 'machine_tags.json')
        validate_setting(sid, profile, classification, hrow, mrow, human_vocab, machine_vocab)
        profile_audit.append({'setting_id': sid, 'canonical_profile_sha256': hrow['profile_sha256'],
                              'local_input_sha256': local_hashes, 'upstream_input_sha256': source_hashes})
        for filename in ['human_tags.json', 'machine_tags.json']:
            imported[base + filename] = base + filename

    for definitions, rows, field in [(human_vocab, hrows, 'facets'), (machine_vocab, mrows, 'features')]:
        members, view_members = defaultdict(set), defaultdict(set)
        for sid, record in rows.items():
            for item in record[field]:
                members[item['concept_id']].add(sid)
                view_members[item['concept_id']].update((sid, vid) for vid in item['view_ids'])
        for cid, concept in definitions.items():
            require(concept['setting_count'] == len(members[cid]) and concept['view_count'] == len(view_members[cid]), f'Toolkit membership count mismatch: {cid}')
    graph_edges = validate_graph(graph, profiles, mrows)
    projection_hash = digest(canonical({'human_vocabulary': human, 'machine_vocabulary': machine,
                                        'human_records': [hrows[sid] for sid in sorted(ids)],
                                        'machine_records': [mrows[sid] for sid in sorted(ids)]}))
    require(projection_hash == summary['projection_hash'], 'Toolkit projection digest differs from tag_summary.json')
    tag_counts = {'settings': len(ids), 'views': sum(len(profile['views']) for profile in profiles.values()),
                  'navigation_concepts': len(human_vocab), 'precise_concepts': len(machine_vocab),
                  'machine_feature_assertions': sum(len(row['features']) for row in mrows.values())}
    for key, count in tag_counts.items():
        require(summary[key] == count, f'Toolkit tag summary count mismatch: {key}')

    # All checks precede writes. Publish the hash receipt last so verification
    # can detect a partially interrupted import.
    files = {}
    for destination, original in imported.items():
        content = (source / original).read_bytes()
        write(root / destination, content)
        files[destination] = {'source_path': original, 'sha256': digest(content), 'bytes': len(content)}
    payload = {'version': '1.0.0', 'revision': revision, 'dictionary': human,
               'settings': [browser_record(profiles[sid], hrows[sid], mrows[sid]) for sid in ids],
               'relations': read(source, 'data/registry/relations.json')['relations'],
               'taxonomy_hierarchy': hierarchy(human, machine), 'stats': tag_counts,
               'provenance': {'toolkit_projection_sha256': projection_hash, 'graph_path': GRAPH}}
    payload_bytes = canonical(payload) + b'\n'
    write(root / BROWSER, payload_bytes)
    files[BROWSER] = {'sha256': digest(payload_bytes), 'bytes': len(payload_bytes), 'derived': True}
    report = {'schema_version': '1.0.0', 'passed': True, 'toolkit_root': str(source), 'toolkit_release_id': revision,
              'created_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'vocabulary_version': human['version'],
              'counts': tag_counts, 'graph': graph_edges, 'toolkit_projection_sha256': projection_hash,
              'source_manifest_sha256': digest((source / 'MANIFEST.json').read_bytes()),
              'profile_hash_method': 'SHA-256 of sorted compact UTF-8 JSON for the Toolkit projection; byte hashes for file provenance.',
              'profiles': profile_audit, 'files': files}
    write(root / AUDIT, (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode())
    return {'passed': True, **tag_counts, 'audit': AUDIT}


def verify(root):
    from build_public_indexes import build
    payloads, _ = build(root)
    return {'passed': True, **payloads[BROWSER]['stats']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, help='Explicit Toolkit input directory')
    parser.add_argument('--verify', action='store_true', help='Check the current native scientific bindings')
    args = parser.parse_args()
    if not args.verify and args.source is None:
        parser.error('--source is required unless --verify is used')
    print(json.dumps(verify(ROOT) if args.verify else import_tags(ROOT, args.source.resolve())))


if __name__ == '__main__':
    main()
