"""Create immutable, validated preview material requested by a paused research author."""
import argparse
import json
from pathlib import Path

from oracle_atlas.core.config import load_config
from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.core.store import atomic_json
from oracle_atlas.workflow.engine import Engine


def prepare_requested_material(config_path, case_id, checkpoint_ref):
    config=load_config(config_path)
    engine=Engine(config,None)
    case=engine.ws.case(case_id)
    status=case['state'].split(':')
    if len(status)!=2 or status[0] not in {'bound_updater','profile_researcher'} or status[1]!='needs_materials':
        raise ProtocolError('Expected a current bound_updater or profile_researcher needs_materials handoff.')
    role=status[0]
    job=engine.ws.job(case['jobs'][role])
    output=job.get('output') or {}
    if (job['status']!='needs_materials' or output.get('status')!='needs_materials'
            or output.get('checkpoint_ref')!=checkpoint_ref or not engine.artifacts.owned(checkpoint_ref,job['id'])):
        raise ProtocolError('The requested checkpoint is not the paused author’s current handoff.')
    checkpoint=engine.artifacts.get(checkpoint_ref)
    if checkpoint['kind']!='checkpoint' or not checkpoint['data'].get('remaining'):
        raise ProtocolError('The paused handoff must include an outstanding material request.')
    refs=[r for r in output['artifact_refs'] if engine.artifacts.get(r)['kind']=='research']
    if len(refs)!=1 or not engine.artifacts.owned(refs[0],job['id']):
        raise ProtocolError('The author must hand off exactly one frozen research record.')
    research_ref=refs[0]
    research=engine.artifacts.get(research_ref)['data']
    inputs=job['inputs']
    if any(research[k]!=case[k] or inputs[k]!=case[k] for k in ('candidate_ref','identity_ref')):
        raise ProtocolError('The current author, frozen research and case differ on candidate/identity.')
    if (inputs.get('transfer_scope_ref')!=case.get('transfer_scope_ref')
            or inputs.get('base_version')!=research['base_version']
            or research['action']!={'bound_updater':'update','profile_researcher':'new'}[role]):
        raise ProtocolError('The frozen record, job and pinned target must have the same scope/version.')
    sid=research['setting_id']
    if research['action']=='update' and (inputs.get('setting_id')!=sid or engine.atlas.version(sid)!=research['base_version']):
        raise ProtocolError('The target changed after drafting. Refresh the research baseline.')
    if research['action']=='new' and (research['base_version'] is not None or engine.atlas.version(sid) is not None):
        raise ProtocolError('The newly proposed setting already exists or has an unexpected baseline.')
    profile=engine.artifacts.get(research['profile_ref'])
    if profile['kind']!='profile' or profile['data'].get('setting_id')!=sid:
        raise ProtocolError('The frozen profile is not the author’s proposed target.')
    if not engine.artifacts.owned(research['profile_ref'],job['id']):
        raise ProtocolError('The paused research author does not own the frozen profile.')
    # The caller explicitly selected the current checkpoint after reading its outstanding request.
    # Normal controller projection validates the entire native bundle without changing the case.
    proposal_ref=engine._prepare_proposal({**case,'research_ref':research_ref})
    proposal=engine.artifacts.get(proposal_ref)['data']
    prepared_ref=proposal['prepared_ref']
    prepared=engine.artifacts.get(prepared_ref)['data']
    interpretation=('Native five-file projection completed against the pinned Atlas. Inspect this CURRENT preview, '
        'its semantic pointers, inherited human/machine navigation and bound hashes. A study requiring no further '
        'scientific changes may keep its frozen profile and evidence and record resolved technical issues in a new '
        'research handoff. Each remaining scientific or projection concern must still be reported. '
        'A separate independent review must assess the actual final proposal before any adoption.')
    descriptor={'kind':'requested_prepared_preview','case_id':case_id,'setting_id':sid,'author_job':job['id'],
        'checkpoint_ref':checkpoint_ref,'research_ref':research_ref,'profile_ref':research['profile_ref'],
        'prepared_ref':prepared_ref,'proposal_ref':proposal_ref,'base_version':research['base_version'],
        'bundle_hash':prepared['bundle_hash'],'five_file_hashes':prepared['hashes'],'meaning':interpretation}
    material_ref=engine.put('external_result',descriptor,[checkpoint_ref,research_ref,prepared_ref])
    if engine.ws.case(case_id)!=case:
        raise ProtocolError('The case changed during projection. Recheck the current handoff before resume.')
    return {**descriptor,'material_ref':material_ref}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--case-id',required=True)
    parser.add_argument('--requested-checkpoint-ref',required=True,help='Pass the exact current author checkpoint after confirming it asks for a five-file preview.')
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    report=prepare_requested_material(args.config,args.case_id,args.requested_checkpoint_ref)
    if args.report:
        atomic_json(args.report,report)
    print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__=='__main__':
    main()
