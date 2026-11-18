"""Apply audited navigation additions to in-memory Toolkit records."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path


def load_navigation_additions(root):
    data = Path(root) / 'data'
    path = data / 'derived/toolkit_navigation_additions.json'
    if not path.is_file():
        return {}
    settings = json.loads(path.read_text(encoding='utf-8'))['settings']
    for setting_id, addition in settings.items():
        folder = data / 'settings' / setting_id
        for name, key in [('profile.json', 'profile_file_sha256'),
                          ('human_tags.json', 'human_tags_file_sha256')]:
            actual = hashlib.sha256((folder / name).read_bytes()).hexdigest()
            if actual != addition[key]:
                raise ValueError(f'Stale navigation addition for {setting_id}: {name}')
    return settings


def apply_navigation_additions(human_tags, additions):
    setting_id = human_tags['setting_id']
    addition = additions.get(setting_id)
    if not addition:
        return human_tags
    if addition['profile_sha256'] != human_tags['profile_sha256']:
        raise ValueError(f'Navigation addition refers to a different profile: {setting_id}')

    effective = deepcopy(human_tags)
    views = {view['view_id']: view for view in effective['views']}
    facets = {facet['concept_id']: facet for facet in effective['facets']}
    for new_facet in addition['facets']:
        concept_id = new_facet['concept_id']
        new_view_ids = []
        for view_id in new_facet['view_ids']:
            if view_id not in views:
                raise ValueError(f'Unknown navigation view {view_id} for {setting_id}')
            view = views[view_id]
            if concept_id not in view['facet_ids']:
                view['facet_ids'].append(concept_id)
                view.get('unknown_groups', {}).pop(new_facet['parent_id'], None)
                new_view_ids.append(view_id)
        if not new_view_ids:
            continue

        evidence = [deepcopy(row) for row in new_facet['evidence'] if row['view_id'] in new_view_ids]
        facet = facets.get(concept_id)
        if facet is None:
            facet = deepcopy(new_facet)
            facet['view_ids'] = new_view_ids
            facet['evidence'] = evidence
            effective['facets'].append(facet)
            facets[concept_id] = facet
        else:
            membership = set(facet['view_ids']) | set(new_view_ids)
            facet['view_ids'] = [view_id for view_id in views if view_id in membership]
            facet['source_pointers'] = list(dict.fromkeys(facet['source_pointers'] + new_facet['source_pointers']))
            facet['evidence'].extend(evidence)
        facet.setdefault('local_navigation_evidence', []).extend(evidence)
    return effective
