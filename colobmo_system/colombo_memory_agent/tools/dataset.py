"""Dataset integrity checks, not mathematical certification. Stdlib only."""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
from _agent_bootstrap import AGENT_ROOT,CORE_ROOT,DATASET_ROOT
from colombo.memory.contracts import ContractError,LIBRARIES,AXES,digest,validate_record

def load_dataset(dataset_root: Path=DATASET_ROOT) -> list[dict]:
    """Validate current four-library records or an explicitly supplied legacy snapshot."""
    dataset_root=Path(dataset_root).expanduser().resolve()
    if all((dataset_root/name).is_dir() for name in set(LIBRARIES.values())):
        from colombo.memory.store import Store
        from colombo.memory.integration import _validate_store
        store = Store(dataset_root)
        _validate_store(store)
        records = store.current_records(include_leads=True)
        for record in records: validate_record(record)
        return records
    records=json.loads((dataset_root/'data/records.candidates.json').read_text(encoding='utf-8'))
    manifest=json.loads((dataset_root/'manifest.json').read_text(encoding='utf-8'))
    if digest(records)!=manifest['data_digest']:
        raise ContractError('Candidate dataset digest mismatch')
    by_id={r['id']:r for r in records}
    if len(by_id)!=len(records): raise ContractError('Duplicate record ID')
    lines=[json.loads(s) for s in (dataset_root/'data/records.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
    if lines!=records: raise ContractError('JSON and JSONL snapshots disagree')
    for r in records:
        validate_record(r)
        if r['revision'] is not None or r['evidence']['readiness']!='lead':
            raise ContractError('This delivery must remain unreviewed candidates')
        if digest(r)!=manifest['record_hashes'].get(r['id']):
            raise ContractError('Record hash mismatch: '+r['id'])
        standalone=json.loads((dataset_root/'data'/({'algorithm':'algorithm_library','source':'sources'}.get(r['kind'],LIBRARIES[r['kind']]))/(r['id']+'.json')).read_text(encoding='utf-8'))
        if standalone!=r: raise ContractError('Standalone record disagrees: '+r['id'])
        for s in r['source_refs']:
            if s['source_id'] not in by_id or by_id[s['source_id']]['kind']!='source':
                raise ContractError('Missing Source: '+s['source_id'])
        for l in r['links']:
            if l['target_id'] not in by_id: raise ContractError('Dangling link: '+l['target_id'])
        if r['kind']!='source' and {f['axis'] for f in r['navigation']['facets']}!=AXES:
            raise ContractError('Eight context axes not present: '+r['id'])
    ledger=[json.loads(s) for s in (dataset_root/'review/ledger.jsonl').read_text(encoding='utf-8').splitlines()]
    if {x['record_id'] for x in ledger}!=set(by_id) or len(ledger)!=len(records):
        raise ContractError('Ledger does not cover exact dataset')
    for x in ledger:
        if x['candidate_sha256']!=digest(by_id[x['record_id']]): raise ContractError('Stale ledger hash')
        if x['independent_review_performed'] or x['publication_disposition']!='defer':
            raise ContractError('Unexecuted review cannot authorize publication')
    return records

def report(records: list[dict]) -> dict:
    kinds=Counter(x['kind'] for x in records)
    return {'structure_and_hashes':'passed','records':len(records),'kinds':dict(kinds),
            'independent_scientific_review':False,'canonical_publication':False,
            'meaning':'JSON, pointers, record hashes, Source IDs and link integrity only; not correctness of mathematics.'}
