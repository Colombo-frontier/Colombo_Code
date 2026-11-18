#!/usr/bin/env python3
"""Build global search records from profiles and their sourced classifications."""
from pathlib import Path
import json
import hashlib
import sys
from import_profiles import catalog_record

DATA=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DATA.parent / 'visualization/src'))
from catalog_order import order_catalog, write_catalog

catalog_path=DATA/'derived/catalog.json'
previous=json.loads(catalog_path.read_text()) if catalog_path.is_file() else {}
active_ids={path.parent.name for path in (DATA/'settings').glob('*/profile.json')}
prior_ids=[record['id'] for record in previous.get('profiles', [])]
setting_ids=dict.fromkeys(prior_ids + sorted(active_ids))
records=[]
for order,sid in enumerate((sid for sid in setting_ids if sid in active_ids),1):
    path=DATA/'settings'/sid/'profile.json'
    p=json.loads(path.read_text())
    classification=json.loads(path.with_name('classification.json').read_text())
    if classification['profile_sha256']!=hashlib.sha256(path.read_bytes()).hexdigest():
        raise ValueError('Stale classification: '+sid)
    r=catalog_record(p,order)
    unique_tags=list({tag['id']: tag for tag in classification['tags']}.values())
    r['tags']=[t['id'] for t in unique_tags]
    r['tagLabels']=[t['axis']+' / '+t['group'].replace('_',' ')+': '+t['label'] for t in unique_tags]
    r['classification_path']='settings/'+sid+'/classification.json'
    r['viewTagSets']={v['view_id']:[t['id'] for t in classification['tags'] if v['view_id'] in t['view_ids']] for v in p['views']}
    r['viewStatusCodes']={}
    global_badges={b['code'] for b in p['summary_status'].get('badges',[])}
    for v in p['views']:
        comparisons=[c for c in p['comparisons'] if c['view_id']==v['view_id']]
        codes=list(dict.fromkeys(c['status']['code'] for c in comparisons))
        if 'fully_optimal' in global_badges:
            codes.append('fully_optimal')
        if any(c['status'].get('missing_sides') or c['status']['code'].startswith('missing_') or c['status']['code']=='joint_budget_unclosed' for c in comparisons):
            codes.append('bounds_missing')
        r['viewStatusCodes'][v['view_id']]=list(dict.fromkeys(codes))
    records.append(r)
catalog=order_catalog({'schema_version':'2.0.0','profile_schema_version':'6.1.0','taxonomy_version':'1.0.0',
         **({'release_date':previous['release_date']} if 'release_date' in previous else {}),
         'profile_count':len(records),
         'filter_semantics':'All selected tags must coexist in one effective view; selected statuses are OR within that same view.',
         'profiles':records})
write_catalog(catalog_path, catalog)
sources = {'settings': {sid: {'files': {name: hashlib.sha256((DATA / 'settings' / sid / name).read_bytes()).hexdigest()
                                    for name in ('profile.json', 'identity.json', 'classification.json', 'human_tags.json', 'machine_tags.json')}}
                        for sid in sorted(active_ids)},
           'catalog_sha256': hashlib.sha256(catalog_path.read_bytes()).hexdigest()}
(DATA / 'derived/catalog_sources.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'profiles':len(records),'tag_assignments':sum(len(r['tags']) for r in records)},ensure_ascii=False))
