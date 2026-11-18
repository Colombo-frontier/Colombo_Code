#!/usr/bin/env python3
"""Exercise all five read operations and check that no memory bytes changed."""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
from _memory_bootstrap import DEFAULT_MEMORY_ROOT, SYSTEM_ROOT
from colombo.memory.store import Store,atomic_json
from colombo.memory.retrieval import Reader
from colombo.memory.contracts import ContractError

def tree(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def smoke(root:Path,out:Path):
    root=root.resolve();out=out.resolve()
    state=Store(root).state_root
    if out.is_relative_to(root) or out.is_relative_to(state):raise ContractError('Keep smoke outputs outside memory and state')
    before=(tree(root),tree(state));r=Reader(Store(root));results={}
    results['overview']=r.overview(include_leads=True,limit=12)
    results['search']=r.search('SPIDER',include_leads=True,limit=10)
    if not results['search']['items']:raise ContractError('SPIDER scientific-memory fixture not found')
    card=next((x for x in results['search']['items'] if x['ref']['kind']!='source'),results['search']['items'][0])
    concept=card['research_use'][0]['concept_id'];results['browse']=r.browse(concept,include_leads=True,limit=10)
    results['read']=r.read(card['ref'],pointer='#/content',limit=20000)
    results['expand']=r.expand(card['ref'],include_leads=True)
    if (tree(root),tree(state))!=before:raise ContractError('Read-only smoke changed memory bytes')
    for k,v in results.items():atomic_json(out/(k+'.json'),v)
    atomic_json(out/'selected_refs.json',[card['ref']])
    summary={'five_operations':'passed','memory_bytes_unchanged':True,'model_calls':0,
             'selected_ref':card['ref'],'source':'Bundled scientific store; read-only validation grants no review'}
    atomic_json(out/'SMOKE.json',summary);return summary
if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--root',type=Path,default=DEFAULT_MEMORY_ROOT);a.add_argument('--out',type=Path,required=True);q=a.parse_args()
    print(json.dumps(smoke(q.root,q.out),ensure_ascii=False,indent=2))
