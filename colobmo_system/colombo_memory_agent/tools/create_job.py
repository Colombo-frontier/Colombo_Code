#!/usr/bin/env python3
"""Create a small explicit extraction job. Never treats seed records as original sources."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from _agent_bootstrap import DATASET_ROOT
from dataset import load_dataset,ContractError
from colombo.memory.contracts import dependencies,safe_id
from colombo.memory.store import atomic_json

def create_job(*,out:Path,job_id:str,sources:list[Path],papers:list[str],focus:list[str],
               objective:str,policy='stage_only',max_rounds=3,dataset_root:Path=DATASET_ROOT)->dict:
    safe_id(job_id)
    if policy not in {'stage_only','publish_reviewed'}:raise ContractError('Unknown publication policy')
    if not 1<=max_rounds<=6:raise ContractError('max_rounds must be 1..6')
    if not sources:raise ContractError('At least one actual local original is required')
    paths=[]
    for p in sources:
        p=p.expanduser().resolve()
        if not p.is_file() or p.stat().st_size==0:raise ContractError('Missing/empty original: '+str(p))
        if str(p) not in paths:paths.append(str(p))
    out=out.expanduser().resolve()
    inputs=out.parent/(job_id+'.inputs')
    if out.exists() or inputs.exists():raise ContractError('Job path/input directory already exists; never overwrite a resumed job')
    selected=set();by_id={}
    if papers:
        # Jobs without --paper do not read corpus seeds. Explicit paper seeds
        # come from the current four libraries (or a supplied legacy snapshot).
        all_records=load_dataset(dataset_root);by_id={r['id']:r for r in all_records}
        known={r['id'].split('.')[1] for r in all_records}
        if not set(papers)<=known:raise ContractError('Unknown seed paper IDs')
        selected={r['id'] for r in all_records if r['id'].split('.')[1] in papers}
    changed=True
    while changed:
        changed=False
        for ident in list(selected):
            for dep,_ in dependencies(by_id[ident]):
                if dep in by_id and dep not in selected:selected.add(dep);changed=True
    seed_files=[]
    if selected:
        inputs.mkdir(parents=True)
        seed=inputs/'seed_records.json';atomic_json(seed,[by_id[i] for i in sorted(selected)])
        seed_files=[str(seed)]
    job={'job_id':job_id,'objective':objective,'source_files':paths,'seed_files':seed_files,
         'focus_anchors':focus,'publication_policy':policy,'max_rounds':max_rounds,
         'seed_paper_ids':papers,'source_handling':'Originals are evidence; seeds are unreviewed repair targets, not evidence.'}
    atomic_json(out,job)
    return {'job_path':str(out),'seed_records':len(selected),'source_files':len(paths),
            'publication_policy':policy,'model_calls':0,'job':job}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--out',type=Path,required=True);a.add_argument('--job-id',required=True)
    a.add_argument('--source',type=Path,action='append',required=True)
    a.add_argument('--paper',action='append',default=[]);a.add_argument('--focus',action='append',default=[])
    a.add_argument('--dataset-root',type=Path,default=DATASET_ROOT,
                   help='Current four-library seeds or an explicit legacy snapshot; not read without --paper')
    a.add_argument('--objective',required=True);a.add_argument('--publication-policy',choices=['stage_only','publish_reviewed'],default='stage_only')
    a.add_argument('--max-rounds',type=int,default=3);q=a.parse_args()
    print(json.dumps(create_job(out=q.out,job_id=q.job_id,sources=q.source,papers=q.paper,focus=q.focus,
        objective=q.objective,policy=q.publication_policy,max_rounds=q.max_rounds,dataset_root=q.dataset_root),ensure_ascii=False,indent=2))
if __name__=='__main__':
    try:main()
    except (ContractError,ValueError,OSError) as e:print(str(e),file=sys.stderr);raise SystemExit(2)
