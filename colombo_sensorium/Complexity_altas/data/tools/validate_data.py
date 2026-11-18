#!/usr/bin/env python3
"""Validate pilot provenance, exact content preservation, and bracket scopes.

Uses only Python's standard library. This is data-integrity validation, not
an independent mathematical reproof or a complete JSON Schema engine.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone

DATA = pathlib.Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))


def hash_file(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def escape(value):
    return str(value).replace('~', '~0').replace('/', '~1')


def walk(value, pointer=''):
    yield pointer, value
    if isinstance(value, dict):
        for key, item in value.items():
            yield from walk(item, pointer + '/' + escape(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk(item, pointer + '/' + str(index))


def resolve(value, pointer):
    if pointer == '':
        return value
    for token in pointer.removeprefix('/').split('/'):
        key = token.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def replace_pointer(value, pointer, replacement):
    parent, token = pointer.rsplit('/', 1)
    obj = resolve(value, parent)
    key = token.replace('~1', '/').replace('~0', '~')
    obj[int(key) if isinstance(obj, list) else key] = replacement


def without_removed_fields(value):
    if isinstance(value, list):
        return [without_removed_fields(item) for item in value]
    if isinstance(value, dict):
        return {key: without_removed_fields(item) for key, item in value.items()
                if key.lower() not in {'coverage', 'coverage_note'}}
    return value


def schema_subset_errors(value, schema, pointer=''):
    """Validate only keywords used in our schemas; report unsupported ones."""
    errors = []
    kind = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'integer': int,
             'number': (int, float), 'boolean': bool, 'null': type(None)}
    if kind and not isinstance(value, types[kind]):
        return [pointer + ': expected ' + kind]
    if 'const' in schema and value != schema['const']:
        errors.append(pointer + ': const mismatch')
    if 'enum' in schema and value not in schema['enum']:
        errors.append(pointer + ': value outside enum')
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0):
            errors.append(pointer + ': string too short')
        if 'pattern' in schema:
            import re
            if not re.search(schema['pattern'], value):
                errors.append(pointer + ': pattern mismatch')
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value:
                errors.append(pointer + ': missing required property ' + key)
        for key, child_schema in schema.get('properties', {}).items():
            if key in value:
                errors.extend(schema_subset_errors(value[key], child_schema, pointer + '/' + escape(key)))
        if schema.get('additionalProperties') is False:
            for key in value.keys() - schema.get('properties', {}).keys():
                errors.append(pointer + ': unexpected property ' + key)
        forbidden = schema.get('propertyNames', {}).get('not', {}).get('enum', [])
        for key in value:
            if key in forbidden:
                errors.append(pointer + ': forbidden property ' + key)
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            errors.append(pointer + ': array too short')
        if 'items' in schema:
            for index, item in enumerate(value):
                errors.extend(schema_subset_errors(item, schema['items'], pointer + '/' + str(index)))
    return errors


def validate():
    catalog = load(DATA / 'derived' / 'catalog.json')
    source_ids = [record['id'] for record in catalog['profiles']]
    source_by_id = {sid: load(DATA / 'settings' / sid / 'profile.json') for sid in source_ids}
    profile_schema = load(DATA / 'schemas' / 'profile.schema.json')
    identity_schema = load(DATA / 'schemas' / 'identity.schema.json')
    comparison_schema = load(DATA / 'schemas' / 'comparison-key.schema.json')
    errors, checks, reports, warnings = [], {}, [], []

    def check(kind, okay, message):
        checks[kind] = checks.get(kind, 0) + 1
        if not okay:
            errors.append({'check': kind, 'message': message})

    def unique_index(items, key, label):
        result = {}
        for item in items:
            value = item.get(key, item.get('id') if key == 'proof_id' else None)
            check('unique_ids', value is not None and value not in result, label + ': duplicate/missing ' + str(value))
            result[value] = item
        return result

    check('library_membership', catalog['profile_count'] == len(source_ids), 'Catalog count differs from inventory')
    check('library_membership', len(source_ids) == len(set(source_ids)), 'Duplicate catalog setting')
    check('library_membership', sorted(p.parent.name for p in (DATA / 'settings').glob('*/profile.json')) == sorted(source_ids),
          'Active settings differ from catalog membership')
    catalog_by_id = {record['id']: record for record in catalog['profiles']}
    for order, sid in enumerate(source_ids, 1):
        path = DATA / 'settings' / sid / 'profile.json'
        identity_path = path.with_name('identity.json')
        active = load(path)
        identity = load(identity_path)
        original = active
        record = catalog_by_id[sid]
        for value, schema, label in ((active, profile_schema, 'profile'), (identity, identity_schema, 'identity')):
            failures = schema_subset_errors(value, schema)
            check('schema', not failures, sid + ': ' + label + ': ' + '; '.join(failures))
        check('record_identity', active['setting_id'] == sid == identity['setting_id'], sid + ': identity mismatch')
        forbidden = [pointer for pointer, value in walk(active)
                     if pointer.rsplit('/', 1)[-1].lower() in {'coverage', 'coverage_note'}]
        check('excluded_metadata', not forbidden, sid + ': excluded presentation fields remain')
        counts = {key: len(active[key]) for key in ('views', 'comparisons', 'regimes', 'bounds', 'evidence', 'references', 'proofs')}
        math_keys = [(pointer, value) for pointer, value in walk(active)
                     if isinstance(value, str) and 'latex' in pointer.rsplit('/', 1)[-1].lower()]
        removed = []
        views = unique_index(active['views'], 'view_id', sid + '/views')
        quantities = unique_index(active['quantities'], 'id', sid + '/quantities')
        regimes = unique_index(active['regimes'], 'id', sid + '/regimes')
        resources = unique_index(active['resource_projections'], 'resource_projection_id', sid + '/resources')
        bounds = unique_index(active['bounds'], 'id', sid + '/bounds')
        evidence = unique_index(active['evidence'], 'id', sid + '/evidence')
        references = unique_index(active['references'], 'id', sid + '/references')
        proofs = unique_index(active['proofs'], 'proof_id', sid + '/proofs')
        comparisons = unique_index(active['comparisons'], 'comparison_id', sid + '/comparisons')
        guarantees = {view_id: {guarantee['guarantee_id'] for guarantee in view['guarantees']}
                      for view_id, view in views.items()}
        comparison_keys = set()
        for cid, comparison in comparisons.items():
            scope = sid + '/' + cid
            key = comparison['comparison_key']
            key_errors = schema_subset_errors(key, comparison_schema)
            check('comparison_scope', not key_errors, scope + ': comparison-key schema mismatch')
            check('comparison_scope', key['setting_id'] == sid, scope + ': wrong setting in key')
            for name in ['view_id', 'guarantee_id', 'quantity_id', 'resource_projection_id', 'regime_id']:
                check('comparison_scope', comparison[name] == key[name], scope + ': key disagrees at ' + name)
            key_tuple = tuple(key[name] for name in comparison_schema['required'])
            if key_tuple in comparison_keys:
                warnings.append({'kind':'inherited_comparison_scope_collision','setting_id':sid,
                                 'comparison_id':cid,'comparison_key':key,
                                 'disposition':'Source contains both a weaker and a stronger upper-envelope record on the same scope; retain separate original comparison IDs without claiming that the scope key is unique.'})
            check('comparison_scope', True, '')
            comparison_keys.add(key_tuple)
            view_id, guarantee_id = key['view_id'], key['guarantee_id']
            check('comparison_links', view_id in views and guarantee_id in guarantees.get(view_id, set()),
                  scope + ': missing view or guarantee')
            check('comparison_links', key['quantity_id'] in quantities, scope + ': missing quantity')
            check('comparison_links', key['resource_projection_id'] in resources, scope + ': missing resource projection')
            check('comparison_links', key['regime_id'] in regimes, scope + ': missing regime')
            quantity = quantities.get(key['quantity_id'], {})
            check('comparison_scope', quantity.get('view_id') == view_id and quantity.get('guarantee_id') == guarantee_id,
                  scope + ': quantity contract differs from comparison')
            for field, direction in [('upper_refs', 'upper'), ('lower_refs', 'lower')]:
                for bid in comparison['bracket'].get(field, []):
                    bound = bounds.get(bid)
                    check('bracket_links', bound is not None, scope + ': missing bound ' + bid)
                    if bound:
                        check('bracket_direction', bound['direction'] == direction, scope + ': bound direction mismatch ' + bid)
                        check('bracket_contract', bound['view_id'] == view_id and bound['guarantee_id'] == guarantee_id,
                              scope + ': bound belongs to another view/guarantee ' + bid)
                        check('bracket_contract', key['quantity_id'] in set(bound.get('quantity_refs',[])) | {bound.get('quantity_ref'), bound.get('quantity_id')},
                              scope + ': bound uses another quantity ' + bid)
        for bid, bound in bounds.items():
            quantity_refs = (set(bound.get('quantity_refs', [])) | {bound.get('quantity_ref'), bound.get('quantity_id')}) - {None}
            check('bound_links', bool(quantity_refs) and quantity_refs <= quantities.keys(), sid + ': missing bound quantity ' + bid)
            for rid in bound.get('region_refs', []):
                check('bound_links', rid in regimes, sid + ': missing bound regime ' + rid)
            for eid in bound.get('evidence_refs', []):
                check('evidence_links', eid in evidence, sid + ': missing evidence ' + eid)
            for source in list(bound.get('source_refs', [])) + list(bound.get('reference_refs', [])):
                check('citation_links', source in references, sid + ': missing bound reference ' + source)
            for proof in bound.get('proof_refs', []):
                check('proof_links', proof in proofs, sid + ': missing proof ' + proof)
        for eid, item in evidence.items():
            source_refs = item.get('source_refs', [])
            if item.get('source_ref'):
                source_refs = list(source_refs) + [item['source_ref']]
            for source in source_refs:
                check('citation_links', source in references, sid + ': missing evidence reference ' + source)
        for reference_id, reference in references.items():
            url = reference.get('url')
            check('citation_urls', isinstance(url, str) and url.startswith(('https://', 'http://')),
                  sid + ': missing public source URL ' + reference_id)

        check('catalog_fidelity', record['order'] == order and record['title'] == original['title']
              and record['domain'] == original['primary_domain'], sid + ': catalog identity/order differs')
        classification_path=path.with_name('classification.json')
        if classification_path.exists():
            classification=load(classification_path)
            expected_tags=list(dict.fromkeys(t['id'] for t in classification['tags']))
            check('classification_provenance', classification['profile_sha256']==hash_file(path),sid+': classification is stale')
            for tag in classification['tags']:
                check('classification_axis',tag['axis'] in ['TASK','MODEL','ORACLE','ALGORITHMS','OUTPUT','METRIC','GUARANTEE','RESOURCE'],sid+': invalid axis')
                for source_pointer in tag['source_pointers']:
                    try: resolve(active,source_pointer)
                    except (KeyError,IndexError,TypeError,ValueError):
                        check('classification_pointer',False,sid+': bad tag source '+source_pointer)
                    else: check('classification_pointer',True,'')
        else:
            expected_tags = list(dict.fromkeys(str(item['facet']) + ':' + str(item['value'])
                                             for item in original['facets'] if 'facet' in item and 'value' in item))
        check('catalog_fidelity', record['tags'] == expected_tags, sid + ': catalog tags differ from the audited global classification')
        status_codes = {item['code'] for item in original['summary_status']['badges']
                        + original['summary_status']['special_statuses']}
        status_codes.update(original['summary_status']['gap_classes'])
        status_codes.update(item['status']['code'] for item in original['comparisons'])
        check('catalog_fidelity', set(record['statusCodes']) == status_codes, sid + ': catalog status set differs')
        check('catalog_fidelity', len(record['statusCodes']) == len(record['statusLabels'])
              and len(record['tags']) == len(record['tagLabels']), sid + ': catalog labels are unaligned')
        for name in ['views', 'comparisons', 'regimes', 'bounds']:
            check('catalog_fidelity', record[name] == len(original[name]), sid + ': catalog count differs for ' + name)

        check('identity_provenance', identity['profile_sha256'] == hash_file(path), sid + ': identity points to another profile version')
        for pointer, node in walk(identity):
            if isinstance(node, dict) and 'source_pointer' in node:
                source_pointer = node['source_pointer']
                try:
                    resolved = resolve(active, source_pointer)
                except (KeyError, IndexError, ValueError, TypeError, AttributeError):
                    resolved = None
                    check('identity_pointers', node.get('state') == 'unknown', sid + ': bad identity pointer ' + str(source_pointer))
                else:
                    check('identity_pointers', True, '')
                if 'source_fields' in node:
                    for key, value in (node['source_fields'] or {}).items():
                        check('identity_value_fidelity', isinstance(resolved, dict) and resolved.get(key) == value,
                              sid + ': identity source field changed at ' + source_pointer + '/' + key)
        for view in identity['views']:
            for effective_pointer, source_pointer in view.get('effective_leaf_sources', {}).items():
                check('identity_merge_provenance', resolve(view['effective_specification'], effective_pointer)
                      == resolve(active, source_pointer), sid + ': effective view lost source mapping at ' + effective_pointer)
        reports.append({'setting_id': sid, 'source_order': order, 'source_counts': counts,
                        'removed_field_count': len(removed), 'formula_fields_checked': len(math_keys),
                        'identity_state': identity.get('matching_state', 'unreviewed')})

    aliases = load(DATA / 'registry' / 'aliases.json')
    for entries in aliases.values():
        for entry in entries:
            check('alias_links', entry['setting_id'] in source_by_id, 'Alias points outside pilot: ' + repr(entry))
    relations = load(DATA / 'registry' / 'relations.json')['relations']
    for record in relations:
        original = source_by_id[record['declared_in_setting']]
        check('relation_fidelity', record['relation'] == without_removed_fields(resolve(original, record['source_pointer'])),
              'Relation changed: ' + record['declared_in_setting'] + record['source_pointer'])
    warnings.append('No cited research theorem has been independently re-proved; source-fidelity checks do not certify scientific correctness.')
    warnings.append('Identity normalization is source extraction only. Unknown and unparsed information requires review before equivalence decisions.')
    return {
        'schema_version': '1.0.0',
        'passed': not errors, 'profile_count': len(source_ids),
        'checks_run': sum(checks.values()), 'checks_by_category': checks,
        'errors': errors, 'limitations': warnings, 'profiles': reports,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=pathlib.Path, help='Optional local report destination')
    args = parser.parse_args()
    result = validate()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': result['passed'], 'profiles': result['profile_count'],
                      'checks_run': result['checks_run'], 'errors': result['errors'],
                      'report': str(args.report)}, ensure_ascii=False))
    sys.exit(0 if result['passed'] else 1)
