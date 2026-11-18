"""Read completed public exports and freeze one self-contained downstream input.

This adapter never opens SQLite, calls Brain tools, or modifies the source run.
Agents see only the resulting package, not the Brain's internal run directory.
"""
import hashlib
import json
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                   separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def ident(ref):
    return ref['id'] if isinstance(ref, dict) else ref


def validate_package(package):
    if package.get('schema_version') != 1:
        raise ValueError('Unsupported handoff package')
    proof = package['proof']
    if package['proof_sha256'] != digest(proof):
        raise ValueError('ProofDraft hash mismatch')
    steps = [s for s in proof['steps'] if s['status'] != 'retired']
    if not steps or proof['open_questions'] or any(s['status'] != 'checked' or s['gaps'] for s in steps):
        raise ValueError('Downstream input requires a complete checked ProofDraft')
    required = [package['main_claim_id'], *[s['id'] for s in steps]]
    if len(set(required)) != len(required) or package['required_claim_ids'] != required:
        raise ValueError('Required Claim coverage is inconsistent')
    check = package['brain_check']
    if check.get('verdict') != 'pass' or check.get('proof_sha256') != package['proof_sha256']:
        raise ValueError('Brain Check is absent or belongs to another proof')
    for material in package.get('source_materials', []):
        if hashlib.sha256(material['text'].encode()).hexdigest() != material['sha256']:
            raise ValueError('Source material hash mismatch')
    return package


def from_brain_run(run_dir, materials=()):
    root = Path(run_dir).resolve()
    paths = [root/'research.json', root/'proof_draft.json', root/'output/final.md']
    raw = [p.read_bytes() for p in paths]
    research, exported = [json.loads(data) for data in raw[:2]]
    if (research.get('storage_version') != 4 or exported.get('storage_version') != 4
            or research.get('generation') is None or research['generation'] != exported.get('generation')):
        raise ValueError('Brain exports are inconsistent; wait for completed export')
    conclusions = list(research.get('conclusion', {}).values())
    if len(conclusions) != 1 or conclusions[0].get('status') != 'completed':
        raise ValueError('Brain research has not completed; downstream is not started')
    proof_ref = exported['current_ref']
    entry = exported['versions'][ident(proof_ref)]
    review_ref = entry.get('review_ref')
    review = entry.get('reviews', {}).get(ident(review_ref)) if review_ref else None
    progress = research['goal_progress']['versions'][ident(research['goal_progress']['current_ref'])]
    if (not review or review.get('verdict') != 'pass' or review.get('findings')
            or review.get('review_kind') != 'proof' or ident(proof_ref) not in review.get('checked_refs', [])
            or ident(progress.get('proof_ref')) != ident(proof_ref)
            or progress['progress']['status'] != 'completed'):
        raise ValueError('Final review/progress does not certify the adopted ProofDraft')
    proof = entry['proof_draft']
    main = '$main' if any(s['id'] == 'main' for s in proof['steps']) else 'main'
    sources = []
    for name, text in [('final.md', raw[2].decode('utf-8-sig')),
                       *[(Path(p).name, Path(p).read_text(encoding='utf-8-sig')) for p in materials]]:
        sources.append({'name': name, 'text': text, 'sha256': hashlib.sha256(text.encode()).hexdigest()})
    package = {'schema_version': 1, 'proof': proof, 'proof_sha256': digest(proof),
        'setting': research['goal']['setting_specification'],
        'goal': research['goal']['definition'], 'main_claim_id': main,
        'required_claim_ids': [main, *[s['id'] for s in proof['steps'] if s['status'] != 'retired']],
        'brain_check': {'verdict': 'pass', 'proof_sha256': digest(proof), 'proof_ref': proof_ref,
                        'review_ref': review_ref, 'review': review},
        'source_materials': sources,
        'source_exports': {p.relative_to(root).as_posix(): hashlib.sha256(data).hexdigest()
                           for p, data in zip(paths, raw)}}
    if any(p.read_bytes() != data for p, data in zip(paths, raw)):
        raise ValueError('Brain exports changed during handoff; retry after completion')
    return validate_package(package)
