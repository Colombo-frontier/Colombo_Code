#!/usr/bin/env python3
"""Import candidates into four libraries; workflow artifacts remain outside them."""
from __future__ import annotations
import argparse,json,os,shutil,tempfile
from pathlib import Path
from _agent_bootstrap import AGENT_ROOT,DEFAULT_MEMORY_ROOT,DATASET_ROOT
from dataset import load_dataset,ContractError,digest
from colombo_memory_agent.store import WriterStore as Store
from colombo.memory.store import atomic_json,read_json,now
RECEIPT='IMPORT_RECORDS.json'


def verify_existing(root:Path,receipt:dict,records:list[dict],signature:str)->dict:
    if receipt.get('dataset_digest')!=signature:
        raise ContractError('A different import exists; use explicit reconciliation, not overwrite')
    store=Store(root)
    if store.manifest()['entries']:
        raise ContractError('Published state changed; refusing to replay a candidate import')
    if {r['id']:digest(r) for r in records}!={r['id']:digest(r) for r in store.lead_records()}:
        raise ContractError('Current record snapshot changed')
    for x in receipt['proposals']:
        p=store.load_proposal(x['proposal_id'])
        if p['digest']!=x['digest'] or {r['id']:digest(r) for r in p['records']}!=x['prepared_record_hashes']:
            raise ContractError('Prepared proposal changed')
    return {'status':'already_imported_verified','records':len(records),'proposals':len(receipt['proposals']),
            'receipt':str(store.state_root/RECEIPT),'canonical_published':0,'independent_reviews':0}


def import_dataset(root:Path=DEFAULT_MEMORY_ROOT,papers:list[str]|None=None,*,dataset_root:Path=DATASET_ROOT)->dict:
    dataset_root=Path(dataset_root).expanduser().resolve()
    records=sorted(load_dataset(dataset_root),key=lambda r:r['id'])
    allowed={r['id'].split('.')[1] for r in records}
    wanted=set(papers or allowed)
    if not wanted or not wanted<=allowed:raise ContractError('Unknown paper IDs')
    selected=[r for r in records if r['id'].split('.')[1] in wanted]
    if any(r['evidence']['readiness']!='lead' for r in selected):
        raise ContractError('Import cannot turn reviewed references into unreviewed copies; use prepare/review/publish')
    signature=digest({'records':selected,'papers':sorted(wanted)})
    root=root.expanduser().resolve();state=Store(root).state_root
    if root==AGENT_ROOT or root.is_relative_to(AGENT_ROOT):raise ContractError('Use a separate scientific memory directory')
    root.parent.mkdir(parents=True,exist_ok=True)
    lock=root.parent/('.'+root.name+'.import.lock')
    try:lock.mkdir()
    except FileExistsError as exc:raise ContractError('Import lock exists; inspect its owner') from exc
    build=None;root_committed=False;state_committed=False
    try:
        atomic_json(lock/'owner.json',{'pid':os.getpid(),'created_at':now()})
        if (state/RECEIPT).exists():return verify_existing(root,read_json(state/RECEIPT),selected,signature)
        if root.exists() and (not root.is_dir() or any(root.iterdir())):
            raise ContractError('Refusing to overwrite nonempty memory; use the existing records or explicit migration')
        if state.exists():raise ContractError('State already exists; explicit reconciliation required')
        build=Path(tempfile.mkdtemp(prefix='.'+root.name+'.import-',dir=root.parent))
        temporary=build/'memory';store=Store(temporary);store.initialize()
        discovery=store.install_leads(selected);proposals=[]
        for pid in sorted(wanted):
            batch=[r for r in selected if r['id'].split('.')[1]==pid]
            p=store.prepare(batch,curator_run_id='record-import-no-new-review',job_id='import-'+pid)
            proposals.append({'paper_id':pid,'proposal_id':p['proposal_id'],'digest':p['digest'],
                'relative_path':'staging/'+p['proposal_id']+'/proposal.json',
                'prepared_record_hashes':{r['id']:digest(r) for r in p['records']},'review_state':'not_executed'})
        receipt={'schema':'colombo-record-import/1','dataset_digest':signature,'paper_ids':sorted(wanted),
                 'created_at':now(),'discovery':discovery,'proposals':proposals,
                 'canonical_records_published_by_this_import':0,'independent_reviews_run_by_this_import':0,
                 'note':'One current record per scientific object. No duplicate dataset tree is installed.'}
        atomic_json(store.state_root/RECEIPT,receipt)
        if root.exists():root.rmdir()
        try:
            os.rename(store.state_root,state);state_committed=True
            os.rename(temporary,root);root_committed=True
        except BaseException:
            if root_committed:os.rename(root,temporary)
            if state_committed:os.rename(state,store.state_root)
            raise
        return {'status':'imported_unreviewed','records':len(selected),'papers':len(wanted),
                'proposals':len(proposals),'receipt':str(state/RECEIPT),'canonical_published':0,'independent_reviews':0}
    finally:
        if build is not None and build.exists():shutil.rmtree(build)
        shutil.rmtree(lock,ignore_errors=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--memory-root',type=Path,default=DEFAULT_MEMORY_ROOT)
    p.add_argument('--dataset-root',type=Path,default=DATASET_ROOT)
    p.add_argument('--paper',action='append');a=p.parse_args()
    print(json.dumps(import_dataset(a.memory_root,a.paper,dataset_root=a.dataset_root),ensure_ascii=False,indent=2))
if __name__=='__main__':
    try:main()
    except (ContractError,OSError,ValueError,KeyError) as e:
        print(json.dumps({'error':str(e)},ensure_ascii=False));raise SystemExit(2)
