#!/usr/bin/env python3
"""Independent global taxonomy and view-compatibility regression checks."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'data'
taxonomy=json.loads((DATA/'vocabulary/taxonomy.json').read_text())
catalog=json.loads((DATA/'derived/catalog.json').read_text())
axes=['TASK','MODEL','ORACLE','ALGORITHMS','OUTPUT','METRIC','GUARANTEE','RESOURCE']
errors=[]
if [a['id'] for a in taxonomy['axes']]!=axes:errors.append('Eight global axes are missing or reordered')
vocab={t['id']:t for t in taxonomy['tags']}
if len(vocab)!=len(taxonomy['tags']):errors.append('Duplicate vocabulary IDs')
for a in taxonomy['axes']:
    for group in a['groups']:
        for value in group['values']:
            tag=vocab.get(value['tag_id'])
            if not tag or (tag['axis'],tag['group'],tag['value'])!=(a['id'],group['id'],value['value']):
                errors.append('A global value is under the wrong axis/group: '+value['tag_id'])
conflicts=[('ALGORITHMS:randomization:deterministic','ALGORITHMS:randomization:private_randomness_allowed'),
           ('ALGORITHMS:restriction:zero_respecting','ALGORITHMS:restriction:no_zero_respecting_restriction'),
           ('ALGORITHMS:restriction:zero_respecting','ALGORITHMS:restriction:no_additional_restrictions_declared')]
quantitative={'tangent_residual','saddle_gap','reduced_gradient','reduced_gradient_rms'}
view_count=0
for record in catalog['profiles']:
    sid=record['id'];path=DATA/'settings'/sid/'profile.json'
    p=json.loads(path.read_text());c=json.loads(path.with_name('classification.json').read_text())
    if c['profile_sha256']!=hashlib.sha256(path.read_bytes()).hexdigest():errors.append(sid+': stale profile revision')
    actual_ids=list(dict.fromkeys(t['id'] for t in c['tags']))
    if actual_ids!=record['tags']:errors.append(sid+': stale catalog tags')
    for tag in c['tags']:
        if tag['id'] not in vocab:errors.append(sid+': vocabulary ID missing '+tag['id'])
        if tag['axis']=='TASK' and tag['group']=='solution_concept' and tag['value'] in quantitative:
            errors.append(sid+': a quantitative criterion was duplicated in TASK')
        if tag['axis']=='MODEL' and tag['group']=='structure' and tag['value'] in {'high_order','higher_order'}:
            errors.append(sid+': oracle access order was put in model structure')
    for view in p['views']:
        view_count+=1;vid=view['view_id']
        tags={t['id'] for t in c['tags'] if vid in t['view_ids']}
        if tags!=set(record['viewTagSets'][vid]):errors.append(sid+'/'+vid+': catalog view scope differs')
        for a,b in conflicts:
            if {a,b}<=tags:errors.append(sid+'/'+vid+': incompatible permissions '+a+' and '+b)
        required={comp['status']['code'] for comp in p['comparisons'] if comp['view_id']==vid}
        if not required<=set(record['viewStatusCodes'][vid]):errors.append(sid+'/'+vid+': comparison status omitted')
report={'passed':not errors,'profiles':len(catalog['profiles']),'views':view_count,'axes':axes,
        'vocabulary_values':len(vocab),'tag_assignments':sum(len(r['tags']) for r in catalog['profiles']),
        'errors':errors,'rules':['Shared global hierarchy','Exact catalog/classification membership',
        'Same-view permission compatibility','Quantitative criteria are indexed under METRIC',
        'Higher-order access is not model structure','Comparison statuses stay view-scoped']}
print(json.dumps(report,ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
