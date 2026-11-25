"""Validate curated contribution provenance; never infer theorem correctness."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re


SUMMARY_FIELDS = ('state', 'label', 'paper_ids', 'comparison_ids', 'view_ids', 'scope_note')
SIDES = ('upper_refs', 'lower_refs', 'achievable_refs', 'necessary_refs')
SCOPE_NOTE = ('Attribution applies only to the documented regions and preserves the native mathematical status. '
              'Source-link validation does not independently certify external theorems.')


def require(condition, message):
    if not condition:
        raise ValueError('Colombo results: ' + message)


def string_list(value, label, allow_empty=False):
    require(isinstance(value, list) and all(isinstance(x, str) and x for x in value),
            label + ' must be an array of identifiers')
    require((allow_empty or bool(value)) and len(value) == len(set(value)),
            label + ' must contain distinct identifiers')
    return set(value)


def cited_refs(record):
    refs = set(record.get('source_refs', [])) | set(record.get('reference_refs', []))
    if record.get('source_ref'):
        refs.add(record['source_ref'])
    return refs


def support_path(bound, reference_ids, evidence, proofs, adopted):
    """Follow explicit native links only; a bibliography entry alone is insufficient."""
    pending, visited, supported = [bound], set(), False
    while pending:
        record = pending.pop()
        identity = id(record)
        if identity in visited:
            continue
        visited.add(identity)
        lifecycle = record.get('lifecycle', {})
        if adopted and (lifecycle.get('state') == 'historical'
                        or lifecycle.get('eligible_for_current_bounds') is False):
            return False
        supported = supported or bool(cited_refs(record) & reference_ids)
        pending.extend(evidence[x] for x in record.get('evidence_refs', []) if x in evidence)
        for field in ('proof_refs', 'premise_proof_refs', 'module_dependencies'):
            pending.extend(proofs[x] for x in record.get(field, []) if x in proofs)
    return supported


def selected_bounds(comparison):
    return {bid for side in SIDES for bid in comparison.get('bracket', {}).get(side, [])}


def public_summary(info):
    return None if info is None else {key: deepcopy(info[key]) for key in SUMMARY_FIELDS}


def display_registry(registry):
    """Display all adopted contributions; rate status remains a separate property."""
    result = {'papers': deepcopy(registry['papers']), 'settings': {}}
    for sid, original in registry['settings'].items():
        if original['state'] != 'adopted':
            continue
        result['settings'][sid] = deepcopy(original)
    return result


def local_manuscripts(root):
    """Read the explicit manuscript catalog, verifying its bundled file identities."""
    path = root / 'data/sources/colombo/catalog.json'
    if not path.is_file():
        return {}
    rows = json.loads(path.read_text(encoding='utf-8'))
    require(isinstance(rows, list), 'local manuscript catalog must be an array')
    papers = {}
    for row in rows:
        require(isinstance(row, dict), 'local manuscript record must be an object')
        pid = row.get('id')
        require(isinstance(pid, str) and re.fullmatch(r'COLOMBO_[A-Za-z0-9_]+', pid)
                and pid not in papers and row.get('source_ref') == pid,
                'invalid or duplicate local manuscript identity')
        require(row.get('publication_status') == 'unpublished_manuscript',
                pid + ': unsupported local publication status')
        if any(field in row for field in ('contribution_type', 'contribution_label_en', 'contribution_note_en')):
            require(all(isinstance(row.get(field), str) and row[field].strip()
                        for field in ('contribution_type', 'contribution_label_en', 'contribution_note_en')),
                    pid + ': incomplete contribution presentation')
        require(isinstance(row.get('local_path'), str) and row['local_path'].strip()
                and isinstance(row.get('source_pdf_sha256'), str)
                and re.fullmatch(r'[0-9a-f]{64}', row['source_pdf_sha256']),
                pid + ': missing bundled PDF identity')
        for field, hash_field in (('local_path', 'source_pdf_sha256'),
                                  ('source_tex_path', 'source_tex_sha256')):
            if field not in row:
                continue
            require(isinstance(row[field], str) and row[field].strip(),
                    pid + ': invalid bundled source path')
            target = (root / row[field]).resolve()
            require(target.is_relative_to(root.resolve()) and target.is_file(),
                    pid + ': missing bundled source file')
            require(hashlib.sha256(target.read_bytes()).hexdigest() == row.get(hash_field),
                    pid + ': bundled source hash mismatch')
        papers[pid] = deepcopy(row)
    return papers


def with_local_contributions(root, profiles, original, manuscripts):
    """Join local sources through selected native support paths, never bibliography alone."""
    registry = deepcopy(original)
    for paper in registry['papers']:
        if paper.get('id') in manuscripts:
            canonical = manuscripts[paper['id']]
            require(all(paper.get(key) == canonical[key]
                        for key in ('local_path', 'source_pdf_sha256')),
                    paper['id'] + ': editorial source conflicts with manuscript catalog')
    registered = {paper['id'] for paper in registry['papers']}
    registry['papers'].extend(deepcopy(paper) for pid, paper in manuscripts.items()
                              if pid not in registered)
    for sid, profile in profiles.items():
        references = {ref['id']: ref for ref in profile['references']}
        local_ids = set(references) & manuscripts.keys()
        if not local_ids:
            continue
        bounds = {bound['id']: bound for bound in profile['bounds']}
        evidence = {record['id']: record for record in profile.get('evidence', [])}
        proofs = {record.get('proof_id', record.get('id')): record
                  for record in profile.get('proofs', [])}
        for pid in sorted(local_ids):
            bids, cids, vids = set(), set(), set()
            for comparison in profile['comparisons']:
                for bid in selected_bounds(comparison):
                    bound = bounds.get(bid)
                    if not bound or not (bound.get('eligible_for_bracket', True)
                                         and bound.get('included_in_bracket', True)):
                        continue
                    if bound.get('lower_scope_type') == 'not_certified':
                        continue
                    if support_path(bound, {pid}, evidence, proofs, adopted=True):
                        bids.add(bid)
                        cids.add(comparison['comparison_id'])
                        vids.add(bound['view_id'])
            if not bids:
                continue
            if sid not in registry['settings']:
                raw = (root / 'data/settings' / sid / 'profile.json').read_bytes()
                registry['settings'][sid] = {
                    'state': 'adopted', 'source_profile_sha256': hashlib.sha256(raw).hexdigest(),
                    'note': 'Contribution attribution follows selected native bounds and explicit source links.',
                    'contributions': []}
            info = registry['settings'][sid]
            require(info['state'] == 'adopted', sid + ': mixed pending and adopted attribution needs review')
            if any(item['paper_id'] == pid for item in info['contributions']):
                continue
            source = manuscripts[pid]
            contribution = {
                'paper_id': pid, 'reference_ids': [pid], 'bound_refs': sorted(bids),
                'comparison_ids': sorted(cids), 'view_ids': sorted(vids),
                'binding': 'selected_native_manuscript_support',
                'note': source.get('contribution_note_en',
                        'The cited unpublished manuscript supports the selected bounds in the marked regions. '
                        'The contribution marker does not assert priority, peer review, or whole-setting optimality.')}
            if 'contribution_note_en' in source:
                contribution.update(contribution_type=source['contribution_type'],
                                    contribution_label=source['contribution_label_en'])
            info['contributions'].append(contribution)
    return registry


def reference_identifies_paper(reference, paper, manuscripts):
    pid = paper['id']
    if pid in manuscripts:
        canonical = manuscripts[pid]
        return (reference.get('id') == pid
                and reference.get('local_path') == canonical['local_path']
                and reference.get('source_pdf_sha256') == canonical['source_pdf_sha256'])
    return re.search(r'(?<![\d.])' + re.escape(pid) + r'(?!\d)',
                     json.dumps(reference, ensure_ascii=False)) is not None


def load_colombo_results(root, profiles):
    """Return a new registry, enriched for rendering, without changing canonical data."""
    root = Path(root)
    registry = json.loads((root / 'data/editorial/colombo_results.json').read_text(encoding='utf-8'))
    require(registry.get('schema_version') == '1.0.0', 'unsupported schema version')
    require(isinstance(registry.get('papers'), list), 'papers must be an array')
    manuscripts = local_manuscripts(root)
    registry = with_local_contributions(root, profiles, registry, manuscripts)
    papers = {}
    for paper in registry['papers']:
        pid = paper.get('id')
        require(isinstance(pid, str) and (re.fullmatch(r'\d{4}\.\d{4,5}', pid) or pid in manuscripts)
                and pid not in papers, 'invalid or duplicate paper ID: ' + str(pid))
        require(isinstance(paper.get('title'), str) and paper['title'].strip()
                and isinstance(paper.get('url'), str)
                and (pid in manuscripts or pid in paper['url']),
                pid + ': missing title or identity URL')
        papers[pid] = paper
    require(isinstance(registry.get('settings'), dict), 'settings must be an object')
    enriched = deepcopy(registry)
    for sid, info in enriched['settings'].items():
        require(sid in profiles, 'unknown setting: ' + sid)
        profile = profiles[sid]
        raw = (root / 'data/settings' / sid / 'profile.json').read_bytes()
        require(info.get('source_profile_sha256') == hashlib.sha256(raw).hexdigest(),
                sid + ': stale source_profile_sha256')
        require(json.loads(raw) == profile and profile.get('setting_id') == sid,
                sid + ': supplied canonical profile differs from disk')
        state = info.get('state')
        require(state in ('adopted', 'pending'), sid + ': unsupported contribution state')
        require(isinstance(info.get('note'), str) and info['note'].strip(), sid + ': missing curator note')
        require(isinstance(info.get('contributions'), list) and info['contributions'],
                sid + ': contributions must be a nonempty array')
        comparisons = {c['comparison_id']: c for c in profile['comparisons']}
        bounds = {b['id']: b for b in profile['bounds']}
        references = {r['id']: r for r in profile['references']}
        evidence = {e['id']: e for e in profile.get('evidence', [])}
        proofs = {p.get('proof_id', p.get('id')): p for p in profile.get('proofs', [])}
        views = {v['view_id'] for v in profile['views']}
        all_selected = set().union(*(selected_bounds(c) for c in comparisons.values()))
        paper_ids, comparison_ids, view_ids, notes = set(), set(), set(), []
        for contribution in info['contributions']:
            pid = contribution.get('paper_id')
            label = sid + '/' + str(pid)
            require(pid in papers, label + ': paper is not registered')
            for field in ('binding', 'note'):
                require(isinstance(contribution.get(field), str) and contribution[field].strip(),
                        label + ': missing ' + field)
            refs = string_list(contribution.get('reference_ids'), label + '/reference_ids')
            bids = string_list(contribution.get('bound_refs'), label + '/bound_refs')
            cids = string_list(contribution.get('comparison_ids'), label + '/comparison_ids', state == 'pending')
            vids = string_list(contribution.get('view_ids'), label + '/view_ids')
            require(refs <= references.keys(), label + ': unknown native reference')
            for ref in refs:
                require(reference_identifies_paper(references[ref], papers[pid], manuscripts),
                        label + ': native reference does not identify the paper: ' + ref)
            require(bids <= bounds.keys(), label + ': unknown bound: ' + repr(sorted(bids - bounds.keys())))
            require(vids <= views and cids <= comparisons.keys(), label + ': unknown view or comparison')
            require({bounds[bid].get('view_id') for bid in bids} == vids,
                    label + ': declared views do not match contribution bounds')
            if state == 'pending':
                require(not cids, label + ': pending claim cannot identify active comparisons')
            covered = set()
            for cid in cids:
                comparison = comparisons[cid]
                chosen = selected_bounds(comparison) & bids
                require(chosen and comparison['view_id'] in vids,
                        label + '/' + cid + ': no contribution bound selected in the declared view')
                for bid in chosen:
                    bound = bounds[bid]
                    quantities = set(bound.get('quantity_refs', [])) | {bound.get('quantity_ref'), bound.get('quantity_id')}
                    require(bound.get('view_id') == comparison['view_id']
                            and bound.get('guarantee_id') == comparison['guarantee_id']
                            and comparison['quantity_id'] in quantities,
                            label + '/' + bid + ': bound/comparison contract mismatch')
                covered.update(chosen)
            if state == 'adopted':
                require(covered == bids, label + ': contribution contains an unselected bound: '
                        + repr(sorted(bids - covered)))
            for bid in bids:
                bound = bounds[bid]
                admitted = (bound.get('included_in_bracket', True)
                            and bound.get('eligible_for_bracket', True)
                            and bound.get('lower_scope_type') != 'not_certified')
                require(bool(admitted) if state == 'adopted' else not admitted and bid not in all_selected,
                        label + '/' + bid + ': contribution state contradicts native admission/selection')
                require(support_path(bound, refs, evidence, proofs, state == 'adopted'),
                        label + '/' + bid + ': no eligible explicit paper support path')
            paper_ids.add(pid)
            comparison_ids.update(cids)
            view_ids.update(vids)
            notes.append(contribution['note'].strip())
        highlight = info.get('highlight')
        if highlight is not None:
            require(state == 'adopted', sid + ': pending attribution cannot be highlighted')
            selected = string_list(highlight.get('comparison_ids'), sid + '/highlight/comparison_ids')
            require(selected <= comparison_ids, sid + ': highlight is outside attributed comparisons')
            require(isinstance(highlight.get('scope_note'), str) and highlight['scope_note'].strip(),
                    sid + ': missing highlight scope')
            for cid in selected:
                comparison = comparisons[cid]
                bracket = comparison.get('bracket', {})
                require(comparison['status']['code'] in ('optimal', 'logarithmic_gap'),
                        sid + '/' + cid + ': highlighted comparison is not near-optimal')
                require(bool(bracket.get('upper_refs')) and bool(bracket.get('lower_refs')),
                        sid + '/' + cid + ': highlighted comparison lacks a two-sided bracket')
            highlight['view_ids'] = sorted({comparisons[cid]['view_id'] for cid in selected})
        info.update(label='★ Colombo',
                    paper_ids=sorted(paper_ids), comparison_ids=sorted(comparison_ids),
                    view_ids=sorted(view_ids), scope_note=' '.join([*dict.fromkeys(notes), SCOPE_NOTE]))
    return enriched
