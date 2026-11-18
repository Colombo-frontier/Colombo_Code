#!/usr/bin/env python3
"""Pin selected records into a research workspace. This never changes memory or proves applicability."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from _memory_bootstrap import DEFAULT_MEMORY_ROOT, SYSTEM_ROOT
from colombo.memory.store import Store,atomic_json,read_json,now
from colombo.memory.retrieval import Reader
from colombo.memory.contracts import ContractError,digest,dependencies
USES={'direct','needs_transfer','inspiration_only','incompatible','insufficient_information'}

def freeze(root:Path,refs:list[dict],out:Path,obligation:str,use:str='inspiration_only')->dict:
    if use not in USES:raise ContractError('Unknown use classification')
    if not isinstance(refs,list) or not refs:raise ContractError('Expected a nonempty array of exact tool-returned refs')
    store=Store(root);out=out.expanduser().resolve()
    if any(out==base or out.is_relative_to(base) for base in (store.root,store.state_root)):raise ContractError('Application packages belong in research workspace, outside memory')
    if out.exists():raise ContractError('Never overwrite an existing fixed application package')
    reader=Reader(store);records=[]
    for ref in refs:
        r=reader._record(ref)
        if r['kind']!=ref.get('kind') or digest(r)!=ref.get('content_hash'):raise ContractError('Reference identity/hash mismatch')
        if use=='direct' and (ref.get('tier')!='published' or r['evidence']['readiness']!='reference'):
            raise ContractError('Unreviewed candidates can be frozen for inspiration/transfer, not direct citation as accepted knowledge')
        records.append(r)
    selected={(r['id'],r['revision']) for r in records}
    missing=[{'from':r['id'],'id':dep,'revision':rev} for r in records for dep,rev in dependencies(r) if (dep,rev) not in selected]
    out.mkdir(parents=True)
    for r in records:atomic_json(out/'records'/(r['id']+'.json'),r)
    application={'schema':'colombo-memory-application/1','created_at':now(),'target_obligation':obligation,
        'memory_refs':refs,'use':use,'application_status':'not_assessed','variable_mapping':None,
        'assumption_checks':[],'conversion_obligations':[], 'unfrozen_dependency_refs':missing,
        'retained_material':[{'path':'records/'+r['id']+'.json','content_hash':digest(r)} for r in records],
        'note':'Byte-pinned selected records only. Complete variable/assumption checks and freeze missing dependencies; not a proof certificate.'}
    atomic_json(out/'application.json',application)
    return {'status':'frozen_not_certified','path':str(out),'records':len(records),'unfrozen_dependencies':len(missing)}

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--root',type=Path,default=DEFAULT_MEMORY_ROOT)
    a.add_argument('--refs',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    a.add_argument('--obligation',required=True);a.add_argument('--use',choices=sorted(USES),default='inspiration_only');q=a.parse_args()
    print(json.dumps(freeze(q.root,read_json(q.refs),q.out,q.obligation,q.use),ensure_ascii=False,indent=2))
if __name__=='__main__':
    try:main()
    except (ContractError,ValueError,OSError,KeyError) as e:print(str(e),file=sys.stderr);raise SystemExit(2)
