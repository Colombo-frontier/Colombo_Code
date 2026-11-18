import json
import time
from pathlib import Path
from jsonschema import Draft202012Validator
from colombo.downstream.handoff import digest, validate_package
from colombo.shared.file_io import atomic_write, json_bytes

TEXT = {'type': 'string', 'minLength': 1}
SCHEMA = {'type': 'object', 'additionalProperties': False, 'properties': {
    'proof_sha256': TEXT, 'manuscript_md': TEXT, 'manuscript_tex': TEXT,
    'bibliography_bib': {'type': 'string'},
    'claim_map': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False,
        'properties': {'claim_id': TEXT, 'location': TEXT}, 'required': ['claim_id','location']}},
    'editorial_gaps': {'type': 'array', 'items': TEXT}},
    'required': ['proof_sha256','manuscript_md','manuscript_tex','bibliography_bib','claim_map','editorial_gaps']}


def run(package, lean_result, work_dir, config, model):
    package, lean_result = json.loads(json.dumps([package,lean_result]))
    validate_package(package)
    if (lean_result.get('status') != 'passed' or lean_result.get('proof_sha256') != package['proof_sha256']):
        raise ValueError('Writing requires a passing Lean result for this exact ProofDraft')
    review = lean_result.get('semantic_review') or {}
    checked = review.get('checked_claim_ids', [])
    if ((lean_result.get('compiler') or {}).get('status') != 'passed' or review.get('verdict') != 'pass'
            or review.get('proof_sha256') != package['proof_sha256'] or review.get('findings')
            or len(checked) != len(set(checked)) or set(checked) != set(package['required_claim_ids'])):
        raise ValueError('Writing requires compiler evidence and complete semantic review')
    work = Path(work_dir).resolve(); work.mkdir(parents=True, exist_ok=True)
    lock = work/'.agent.lock'
    with lock.open('x') as f:
        f.write('Writing Agent active; inspect previous process before clearing stale lock.\n')
    try:
        return _run(package,lean_result,work,config,model)
    finally:
        lock.unlink(missing_ok=True)


def _run(package,lean_result,work,config,model):
    context = {**package, 'lean_result': lean_result}
    identity = digest({'input':context,'config':config})
    binding = work/'binding.json'
    if binding.exists():
        state = json.loads(binding.read_text())
        if state['sha256'] != identity:
            raise ValueError('Writing workspace is bound to different input')
    else:
        if any(p.name != '.agent.lock' for p in work.iterdir()):
            raise ValueError('Writing workspace has orphaned artifacts without an input binding')
        if type(config.get('timeout_seconds')) is not int or config['timeout_seconds'] <= 0:
            raise ValueError('Writing timeout_seconds must be positive integer')
        state = {'sha256':identity,'deadline_unix':time.time()+config['timeout_seconds']}
        atomic_write(binding,json_bytes(state))
    saved = work/'result.json'
    if saved.exists() and state.get('result_sha256'):
        report = json.loads(saved.read_text(encoding='utf-8'))
        if digest(report) != state['result_sha256']:
            raise ValueError('Saved writing result changed')
        payload = report['manuscript']
    else:
        remaining = state['deadline_unix']-time.time()
        if remaining <= 0: raise TimeoutError('Writing Agent time allowance exhausted')
        payload = model.invoke('manuscript-writing', work/'call',
            'Integrate the supplied checked research into a rigorous English research article. '
            'Use the writing Skill; preserve all assumptions, Claims and scope. Return the complete article '
            'in Markdown and LaTeX, verified bibliography, Claim locations and editorial gaps.',
            context, SCHEMA, remaining)
        if time.time() >= state['deadline_unix']: raise TimeoutError('Writing Agent time allowance exhausted')
        report = {'status':'draft_with_gaps' if payload.get('editorial_gaps') else 'draft',
            'proof_sha256':package['proof_sha256'], 'manuscript':payload,
            'latex_compilation':'not_run', 'mathematical_review':'writer_self_check_only'}
    Draft202012Validator(SCHEMA).validate(payload)
    if payload['proof_sha256'] != package['proof_sha256']:
        raise ValueError('Writer changed the proof binding')
    ids = [x['claim_id'] for x in payload['claim_map']]
    if len(ids) != len(set(ids)) or set(ids) != set(package['required_claim_ids']):
        raise ValueError('Manuscript Claim map must cover exactly the checked Claims')
    for field, name in [('manuscript_md','manuscript.md'),('manuscript_tex','manuscript.tex'),('bibliography_bib','references.bib')]:
        atomic_write(work/name,payload[field].encode())
    atomic_write(work/'claim-map.json',json_bytes({'claim_map':payload['claim_map'],
        'editorial_gaps':payload['editorial_gaps'],'proof_sha256':package['proof_sha256'],
        'latex_compilation':'not_run','mathematical_review':'writer_self_check_only'}))
    atomic_write(saved,json_bytes(report))
    atomic_write(binding,json_bytes({**state,'result_sha256':digest(report)}))
    return report
