#!/usr/bin/env python3
"""Repack the uploaded unreviewed Store into four visible scientific libraries.

Default is audit only. --apply needs stopped research/curation processes.
The original directory is archived byte-for-byte before any replacement.
This command does not review, edit, merge, or promote scientific records.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import uuid
import zipfile
from _agent_bootstrap import DEFAULT_MEMORY_ROOT
from colombo.memory.contracts import ContractError, LIBRARIES, digest, validate_record
from colombo.memory.store import Store, read_json, atomic_json, now
from colombo.memory.integration import _validate_store
from colombo_memory_agent.store import WriterStore


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()


def inside(root: Path, rel: str) -> Path:
    if not isinstance(rel, str) or Path(rel).is_absolute(): raise ContractError('Unsafe legacy path')
    p = (root / rel).resolve()
    if not p.is_relative_to(root): raise ContractError('Legacy pointer escapes memory')
    return p


def inspect(root: Path) -> tuple[dict, list[tuple[Path, dict]]]:
    root = root.resolve()
    state = Store(root).state_root
    if set(p.name for p in root.iterdir()) == set(LIBRARIES.values()) and (state/'CURRENT.json').exists():
        _validate_store(Store(root))
        records = Store(root).current_records()
        return {'status': 'already_four_libraries', 'records': len(records),
                'counts': dict(Counter(LIBRARIES[r['kind']] for r in records)),
                'memory_root': str(root), 'state_root': str(state)}, []
    if state.exists(): raise ContractError('State directory already exists; reconcile explicitly')
    if (root/'.writer.lock').exists(): raise ContractError('Existing writer lock; stop processes and inspect its owner')
    if any(p.is_symlink() for p in root.rglob('*')): raise ContractError('Symlinks need explicit operator handling')
    pointer = read_json(root/'CURRENT.json')
    m = read_json(inside(root, '.generations/'+pointer['generation'])/'manifest.json')
    if digest(m) != pointer['manifest_hash']: raise ContractError('Legacy manifest hash mismatch')
    if m['entries'] or m['receipts'] or m['sequence'] != 0:
        raise ContractError('This migration targets the uploaded zero-publication snapshot; published history needs explicit mapping')
    lead = read_json(root/'LEADS.json')
    folder = inside(root, lead['path'])/'records'
    entries = []
    for p in sorted(folder.glob('*.json')):
        r = read_json(p); validate_record(r)
        if r['evidence']['readiness'] != 'lead' or r['revision'] is not None:
            raise ContractError('Unexpected published/reference state in lead snapshot')
        if p.name != r['id']+'.json': raise ContractError('Record filename/identity mismatch')
        entries.append((p,r))
    if len(entries)!=lead['count'] or len({r['id'] for _,r in entries})!=len(entries):
        raise ContractError('Lead count or identity conflict')
    by_id={r['id']:r for _,r in entries}
    for _,r in entries:
        for s in r['source_refs']:
            if s['source_id'] not in by_id or by_id[s['source_id']]['kind']!='source':
                raise ContractError('Source dependency missing')
        for link in r['links']:
            if link['target_id'] not in by_id: raise ContractError('Link target missing')
    proposals = sorted((root/'staging').glob('proposal-*/proposal.json'))
    for p in proposals:
        v=read_json(p)
        if digest({k:x for k,x in v.items() if k!='digest'})!=v['digest']:
            raise ContractError('Prepared proposal hash mismatch: '+str(p))
    return {'status':'plan_only','memory_root':str(root),'state_root':str(state),
            'old_file_count':sum(p.is_file() for p in root.rglob('*')),
            'records':len(entries),'counts':dict(Counter(LIBRARIES[r['kind']] for _,r in entries)),
            'proposal_count':len(proposals),'scientific_edits':0,'independent_reviews':0,
            'canonical_publications':0}, entries


def migrate(root: Path, *, apply: bool=False) -> dict:
    root=root.expanduser().resolve()
    plan,entries=inspect(root)
    if not apply or plan['status']=='already_four_libraries': return plan
    lock=root.parent/('.'+root.name+'.layout.lock')
    try: lock.mkdir()
    except FileExistsError as exc: raise ContractError('Layout lock exists; inspect rather than deleting it') from exc
    build=None;retired=None;state=Store(root).state_root;newroot=None;newstate=None;state_committed=False;root_committed=False
    try:
        atomic_json(lock/'owner.json',{'pid':os.getpid(),'created_at':now()})
        # Recheck after obtaining the layout lock; users must stop other processes.
        plan,entries=inspect(root)
        build=Path(tempfile.mkdtemp(prefix='.'+root.name+'.layout-build-',dir=root.parent))
        newroot=build/'memory';store=WriterStore(newroot);store.initialize();newstate=store.state_root
        archive=newstate/'archive'/'previous_layout.zip';archive.parent.mkdir(parents=True)
        inventory={p.relative_to(root).as_posix():sha(p) for p in sorted(root.rglob('*')) if p.is_file()}
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for rel in inventory: z.write(root/rel,rel)
        # Verify all archived bytes, not merely zip container integrity.
        with zipfile.ZipFile(archive) as z:
            if set(z.namelist())!=set(inventory): raise ContractError('Backup inventory mismatch')
            for rel,h in inventory.items():
                if hashlib.sha256(z.read(rel)).hexdigest()!=h: raise ContractError('Backup hash mismatch')
        record_checks={}
        for p,r in entries:
            target=store.current_path(r['id'],r['kind']);target.write_bytes(p.read_bytes())
            record_checks[r['id']]={'before_sha256':sha(p),'after_sha256':sha(target),
                                    'record_digest':digest(r),'path':target.relative_to(newroot).as_posix()}
        with store.writer(): store._save_lead_catalog([r for _,r in entries])
        for directory in sorted((root/'staging').glob('proposal-*')):
            if directory.is_dir(): shutil.copytree(directory,newstate/'staging'/directory.name)
        _validate_store(Store(newroot))
        # Verify that inputs have not changed during archive/copy.
        after={p.relative_to(root).as_posix():sha(p) for p in sorted(root.rglob('*')) if p.is_file()}
        if inventory!=after: raise ContractError('Memory changed while migrating; no replacement made')
        report={**plan,'status':'migrated','completed_at':now(),'archive_sha256':sha(archive),
                'archive':'archive/previous_layout.zip','old_inventory':inventory,'records_verified':record_checks,
                'meaning':'Storage layout only. Record bytes, IDs, reference hashes and scientific status unchanged.'}
        atomic_json(newstate/'LAYOUT_MIGRATION.json',report)
        retired=root.parent/('.'+root.name+'.retired-'+uuid.uuid4().hex)
        os.rename(root,retired)
        try:
            os.rename(newstate,state);state_committed=True
            os.rename(newroot,root);root_committed=True
            _validate_store(Store(root))
        except BaseException:
            if root_committed: os.rename(root,newroot);root_committed=False
            if state_committed: os.rename(state,newstate);state_committed=False
            os.rename(retired,root);retired=None
            raise
        # A hash-verified archive preserves every original file, including duplicates.
        shutil.rmtree(retired);retired=None
        return {k:v for k,v in report.items() if k not in {'old_inventory','records_verified'}}
    finally:
        if build is not None and build.exists(): shutil.rmtree(build)
        shutil.rmtree(lock,ignore_errors=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--memory-root',type=Path,default=DEFAULT_MEMORY_ROOT)
    p.add_argument('--apply',action='store_true')
    a=p.parse_args();print(json.dumps(migrate(a.memory_root,apply=a.apply),ensure_ascii=False,indent=2))

if __name__=='__main__':
    try: main()
    except (ContractError,OSError,ValueError,KeyError) as exc:
        print(json.dumps({'error':str(exc),'scientific_review':False},ensure_ascii=False));raise SystemExit(2)
