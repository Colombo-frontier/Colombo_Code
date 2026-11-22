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
import re
import sys
from datetime import datetime, timezone

DATA = pathlib.Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))


def hash_file(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def canonical_hash(value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':'), allow_nan=False).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def pointer_tokens(pointer):
    if not isinstance(pointer, str) or (pointer and not pointer.startswith('/')):
        raise ValueError('Expected a JSON pointer')
    if re.search(r'~(?![01])', pointer):
        raise ValueError('Invalid JSON pointer escape')
    return [token.replace('~1', '/').replace('~0', '~')
            for token in pointer[1:].split('/')] if pointer else []


def resolve_premise(value, pointer):
    for token in pointer_tokens(pointer):
        if isinstance(value, list):
            if not re.fullmatch(r'0|[1-9][0-9]*', token):
                raise ValueError('Invalid JSON array index')
            value = value[int(token)]
        else:
            value = value[token]
    return value


def valid_digest(value, length=64):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{' + str(length) + '}', value) is not None


def validate_profile_integrity(profile, key_fields, check, warnings):
    """Check active scopes and preserved history without recertifying old proofs."""
    sid = profile['setting_id']
    comparisons = {row['comparison_id']: row for row in profile.get('comparisons', [])}
    seen_keys = set()
    for cid, comparison in comparisons.items():
        key = comparison.get('comparison_key', {})
        if not isinstance(key, dict) or not all(field in key for field in key_fields):
            continue  # The comparison schema reports incomplete keys separately.
        signature = canonical_hash({field: key[field] for field in key_fields})
        check('comparison_scope_unique', signature not in seen_keys,
              sid + '/' + cid + ': duplicate active comparison scope')
        seen_keys.add(signature)

    history_ids = set()
    history = profile.get('provenance', {}).get('comparison_history', [])
    check('comparison_history', isinstance(history, list), sid + ': comparison history must be an array')
    for entry in history if isinstance(history, list) else []:
        original = entry.get('comparison') if isinstance(entry, dict) else None
        if not isinstance(original, dict):
            check('comparison_history', False, sid + ': missing historical comparison object')
            continue
        cid = original.get('comparison_id')
        check('comparison_history', isinstance(cid, str) and bool(cid)
              and cid not in comparisons and cid not in history_ids,
              sid + ': historical comparison ID is missing, duplicated or still active: ' + str(cid))
        if isinstance(cid, str):
            history_ids.add(cid)
        check('comparison_history_hash', entry.get('comparison_sha256') == canonical_hash(original),
              sid + '/' + str(cid) + ': historical comparison hash mismatch')
        replacements = entry.get('superseded_by')
        check('comparison_history', isinstance(replacements, list) and bool(replacements)
              and all(isinstance(target, str) and target in comparisons for target in replacements),
              sid + '/' + str(cid) + ': historical comparison must name active successors')
        check('comparison_history', isinstance(entry.get('relation'), str) and bool(entry['relation'].strip()),
              sid + '/' + str(cid) + ': historical comparison needs a replacement relation')

    proofs = {row.get('proof_id', row.get('id')): row for row in profile.get('proofs', [])}
    historical_ids = {pid for pid, proof in proofs.items()
                      if isinstance(proof.get('lifecycle'), dict)
                      and proof['lifecycle'].get('state') == 'historical'}
    for pid, proof in proofs.items():
        scope = sid + '/' + str(pid)
        lifecycle = proof.get('lifecycle', {})
        if not isinstance(lifecycle, dict):
            check('proof_lifecycle', False, scope + ': lifecycle must be an object')
            lifecycle = {}
        state = lifecycle.get('state', 'current')
        check('proof_lifecycle', state in ('current', 'historical'), scope + ': unknown proof lifecycle state')
        historical = state == 'historical'
        if historical:
            binding = lifecycle.get('premise_binding', {})
            observed = binding.get('first_observed', {}) if isinstance(binding, dict) else {}
            check('proof_lifecycle', lifecycle.get('eligible_for_current_bounds') is False,
                  scope + ': historical proof must be ineligible for current bounds')
            binding_ok = (isinstance(binding, dict)
                          and binding.get('mode') == 'historical_unresolved'
                          and binding.get('verification_status') == 'unresolved_snapshot'
                          and isinstance(observed, dict)
                          and valid_digest(observed.get('git_commit'), 40)
                          and valid_digest(observed.get('profile_sha256'))
                          and isinstance(binding.get('note'), str) and bool(binding['note'].strip()))
            check('proof_historical_binding', binding_ok,
                  scope + ': unresolved history requires an explicit first observation and uncertainty note')
            successors = lifecycle.get('superseded_by')
            check('proof_lifecycle', isinstance(successors, list) and bool(successors)
                  and all(isinstance(target, str) and target in proofs and target not in historical_ids
                          and target != pid for target in successors),
                  scope + ': historical proof must name current successor proofs')
            check('proof_lifecycle', isinstance(lifecycle.get('reason'), str) and bool(lifecycle['reason'].strip()),
                  scope + ': historical proof needs a retention reason')
            if binding_ok:
                warnings.append({'kind': 'unresolved_historical_proof_premises', 'setting_id': sid,
                                 'proof_id': pid, 'first_observed': observed,
                                 'disposition': 'Original premise hashes are preserved, not rebound to the current profile. '
                                                'First observation identifies a retained record, not its missing premise snapshot. '
                                                'This proof cannot support current bounds.'})
        premises = proof.get('premises', [])
        check('proof_premises', isinstance(premises, list), scope + ': premises must be an array')
        for index, premise in enumerate(premises if isinstance(premises, list) else []):
            if not isinstance(premise, dict) or 'sha256' not in premise:
                continue  # Unhashed prose premises make no integrity-binding claim.
            label = scope + '/premises/' + str(index)
            pointer = premise.get('pointer')
            try:
                pointer_tokens(pointer)
                well_formed = valid_digest(premise['sha256'])
            except ValueError:
                well_formed = False
            check('proof_premise_binding', well_formed, label + ': invalid pointer or SHA-256')
            if not well_formed or historical:
                continue
            try:
                value = resolve_premise(profile, pointer)
            except (KeyError, IndexError, TypeError, ValueError):
                check('proof_premise_binding', False, label + ': current premise pointer does not resolve')
            else:
                check('proof_premise_binding', canonical_hash(value) == premise['sha256'],
                      label + ': current premise hash mismatch at ' + pointer)

    evidence = {row['id']: row for row in profile.get('evidence', [])}
    for bound in profile.get('bounds', []):
        if not (bound.get('included_in_bracket', True) or bound.get('eligible_for_bracket', True)):
            continue
        pending = list(bound.get('proof_refs', []))
        for eid in bound.get('evidence_refs', []):
            pending.extend(evidence.get(eid, {}).get('proof_refs', []))
        visited = set()
        while pending:
            pid = pending.pop()
            if pid in visited:
                continue
            visited.add(pid)
            check('current_bound_proof', pid not in historical_ids,
                  sid + '/' + bound['id'] + ': current bound depends on historical proof ' + pid)
            proof = proofs.get(pid, {})
            pending.extend(proof.get('proof_refs', []))
            pending.extend(proof.get('premise_proof_refs', []))
    validate_research_targets(profile, key_fields, check)


def validate_research_targets(profile, key_fields, check):
    """Validate declared remaining regions, without deciding symbolic inclusion."""
    sid = profile['setting_id']
    comparisons = {row['comparison_id']: row for row in profile.get('comparisons', [])}
    regimes = {row['id']: row for row in profile.get('regimes', [])}
    parameters = {row['id'] for row in profile.get('parameters', [])}
    scope_fields = [field for field in key_fields if field != 'regime_id']
    for cid, comparison in comparisons.items():
        if 'research_target' not in comparison:
            continue
        label = sid + '/' + cid
        target = comparison['research_target']
        check('research_target', isinstance(target, dict), label + ': research target must be an object')
        if not isinstance(target, dict):
            continue
        outer, remaining = target.get('target_regime_ref'), target.get('remaining_regime_ref')
        check('research_target_links', isinstance(outer, str) and outer in regimes,
              label + ': target regime does not exist')
        remaining_exists = isinstance(remaining, str) and remaining in regimes
        check('research_target_links', remaining_exists and remaining == comparison.get('regime_id'),
              label + ': remaining regime must be this comparison\'s active regime')
        check('research_target', target.get('set_operation') == 'difference',
              label + ': unsupported research-target set operation')
        predicate = target.get('predicate')
        check('research_target_predicate', isinstance(predicate, dict)
              and predicate == comparison.get('predicate')
              and remaining_exists and predicate == regimes[remaining].get('predicate'),
              label + ': research target, comparison and remaining regime predicates differ')
        excluded = target.get('excluded_closed_comparison_refs')
        check('research_target_links', isinstance(excluded, list) and bool(excluded),
              label + ': difference must name closed comparisons')
        for excluded_id in excluded if isinstance(excluded, list) else []:
            closed = comparisons.get(excluded_id) if isinstance(excluded_id, str) else None
            check('research_target_links', closed is not None,
                  label + ': excluded comparison does not exist: ' + str(excluded_id))
            if closed is None:
                continue
            check('research_target_scope', all(comparison.get('comparison_key', {}).get(field)
                                              == closed.get('comparison_key', {}).get(field)
                                              for field in scope_fields),
                  label + ': excluded comparison has another view/guarantee/quantity/resource scope: ' + excluded_id)
            check('research_target_closed', closed.get('status', {}).get('code') == 'optimal',
                  label + ': excluded comparison is not certified closed: ' + excluded_id)
        for _, node in walk(predicate):
            if not isinstance(node, dict):
                continue
            for field, available in (('region_ref', regimes), ('ref', parameters)):
                if field in node:
                    value = node[field]
                    check('research_target_links', isinstance(value, str) and value in available,
                          label + ': unknown predicate ' + field + ': ' + str(value))


def validate_comparison_aliases(aliases, profiles, check):
    """Legacy identifiers may be historical; navigation targets must be active."""
    for group, entries in aliases.items():
        for entry in entries:
            sid = entry.get('setting_id')
            if sid not in profiles:
                continue  # The existing setting-level foreign-key check reports this.
            active_ids = {row['comparison_id'] for row in profiles[sid]['comparisons']}
            for field in ('comparison_id', 'comparison_ids', 'new_comparison_ids', 'navigation_default_comparison_id'):
                if field not in entry or entry[field] is None:
                    continue
                targets = entry[field] if isinstance(entry[field], list) else [entry[field]]
                for target in targets:
                    check('alias_comparison_links', isinstance(target, str) and target in active_ids,
                          group + '/' + str(entry.get('legacy_id', entry.get('old_comparison_id')))
                          + ': alias target is not an active comparison: ' + str(target))


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
        validate_profile_integrity(active, comparison_schema['required'], check, warnings)
        guarantees = {view_id: {guarantee['guarantee_id'] for guarantee in view['guarantees']}
                      for view_id, view in views.items()}
        for cid, comparison in comparisons.items():
            scope = sid + '/' + cid
            key = comparison['comparison_key']
            key_errors = schema_subset_errors(key, comparison_schema)
            check('comparison_scope', not key_errors, scope + ': comparison-key schema mismatch')
            check('comparison_scope', key['setting_id'] == sid, scope + ': wrong setting in key')
            for name in ['view_id', 'guarantee_id', 'quantity_id', 'resource_projection_id', 'regime_id']:
                check('comparison_scope', comparison[name] == key[name], scope + ': key disagrees at ' + name)
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
    validate_comparison_aliases(aliases, source_by_id, check)
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
