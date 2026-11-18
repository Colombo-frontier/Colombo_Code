#!/usr/bin/env python3
"""Rebuild human/machine navigation from installed records; output is disposable, never canonical."""
from __future__ import annotations
import argparse,json,sys
from collections import defaultdict
from pathlib import Path
from _memory_bootstrap import DEFAULT_MEMORY_ROOT, SYSTEM_ROOT
from colombo.memory.store import Store,read_json,atomic_json,now
from colombo.memory.retrieval import Reader,render_record
from colombo.memory.contracts import ContractError,digest

def export(root:Path,out:Path,include_leads:bool=False)->dict:
    store=Store(root);out=out.expanduser().resolve()
    if any(out==base or out.is_relative_to(base) for base in (store.root,store.state_root)):raise ContractError('Export navigation outside the memory root')
    if out.exists() and any(out.iterdir()):raise ContractError('Use an empty export directory; old exports are snapshots')
    out.mkdir(parents=True,exist_ok=True);reader=Reader(store);records={}
    records={r['id']:r for r in store.current_records(include_leads=include_leads)}
    # Keep every scope card, deduping an old lead only when the same published scope is visible.
    all_cards=reader._cards(include_leads);all_cards.sort(key=lambda item:item[0]['ref']['tier']!='published')
    unique={}
    for card,_ in all_cards:unique.setdefault((card['ref']['id'],card['scope_ref']),card)
    cards=list(unique.values());concepts=defaultdict(lambda:{'groups':set(),'entry_ids':set(),'reasons':set()})
    for r in records.values():
        for t in r['navigation']['research_use']:
            c=concepts[t['concept_id']];c['groups'].add(t['group']);c['entry_ids'].add(r['id']);c['reasons'].add(t['reason'])
    concepts={k:{a:sorted(b) for a,b in v.items()} for k,v in sorted(concepts.items())}
    (out/'cards.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in cards),encoding='utf-8')
    atomic_json(out/'concepts.json',concepts)
    entries=out/'records';entries.mkdir()
    for r in records.values():(entries/(r['id']+'.md')).write_text(render_record(r),encoding='utf-8')
    papers=out/'papers';papers.mkdir();source_count=0
    for src in records.values():
        if src['kind']!='source':continue
        source_count+=1;version=src['content']['bibliographic_identity']['version']
        children=[r for r in records.values() if any(s['source_id']==src['id'] and s['source_version']==version for s in r['source_refs'])]
        text=f"# {src['title']}\n\nSource: `{src['id']}`; version: `{version}`\n\n"
        text+='This page is generated from actual references; the existence of a record does not imply complete extraction or approval by an independent review.\n\n'
        text+='\n'.join(f"- [{r['title']}](../records/{r['id']}.md) · {r['kind']} · {r['evidence']['readiness']}" for r in children) or 'No scientific objects have been extracted yet.'
        (papers/(src['id']+'.md')).write_text(text+'\n',encoding='utf-8')
    text='# Memory navigation snapshot\n\nThe directory is derived data. Cards do not establish applicability; a lead remains an unreviewed candidate.\n\n'
    text+=f'Records: {len(records)}; source views: {source_count}; scopes: {len(cards)}.\n\n'
    for k,c in concepts.items():
        text+=f"## `{k}`\n\n"+'; '.join(c['reasons'][:2])+'\n\n'
        text+='\n'.join(f"- [{records[i]['title']}](records/{i}.md)" for i in c['entry_ids'])+'\n\n'
    (out/'overview.md').write_text(text,encoding='utf-8')
    receipt={'exported_at':now(),'include_leads':include_leads,'records':len(records),'scopes':len(cards),
             'concepts':len(concepts),'paper_views':source_count,'manifest_sequence':store.manifest()['sequence'],
             'record_hashes':{i:digest(r) for i,r in records.items()},'meaning':'Navigation export only, no review/publication'}
    atomic_json(out/'EXPORT.json',receipt);return receipt

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--root',type=Path,default=DEFAULT_MEMORY_ROOT)
    a.add_argument('--out',type=Path,required=True);a.add_argument('--include-leads',action='store_true');q=a.parse_args()
    r=export(q.root,q.out,q.include_leads);print(json.dumps({k:v for k,v in r.items() if k!='record_hashes'},ensure_ascii=False,indent=2))
if __name__=='__main__':
    try:main()
    except (ContractError,ValueError,OSError) as e:print(str(e),file=sys.stderr);raise SystemExit(2)
