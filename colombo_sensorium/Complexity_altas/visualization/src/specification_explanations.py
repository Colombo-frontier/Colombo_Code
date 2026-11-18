"""Bind optional web explanations to the exact profile revision they explain."""
import json
from pathlib import Path
import re

RELATIVE = 'data/editorial/specification_explanations.json'
AXES = ('task', 'metric')


def load_explanations(root):
    path = Path(root) / RELATIVE
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding='utf-8'))
    if payload['schema_version'] != '1.0.0':
        raise ValueError('Unsupported specification explanation format.')
    return payload['settings']


def source_value(profile, pointer):
    if not pointer.startswith('/'):
        raise ValueError(f'Expected a JSON pointer: {pointer!r}')
    value = profile
    for part in pointer[1:].split('/'):
        key = part.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def bind_explanations(profile, profile_sha256, explanations):
    setting = profile['setting_id']
    row = explanations.get(setting)
    if row is None:
        return {}
    if row['profile_sha256'] != profile_sha256:
        raise ValueError(f'Specification explanation is stale: {setting}')
    sections = row['sections']
    if not sections or set(sections) - set(AXES):
        raise ValueError(f'Unsupported explanation section: {setting}')
    for axis, entry in sections.items():
        paragraphs = entry['paragraphs']
        pointers = entry['source_pointers']
        if not paragraphs or not pointers or not all(isinstance(p, str) and p.strip() for p in paragraphs):
            raise ValueError(f'Explanation lacks prose or sources: {setting}/{axis}')
        action = entry['action']
        if action not in {'prepend', 'replace'}:
            raise ValueError(f'Unsupported explanation action: {setting}/{axis}/{action}')
        if action == 'replace':
            container = 'display_specification' if profile.get('display_specification') else 'common_specification'
            replace = entry.get('replace_pointer', '')
            if not re.fullmatch(rf'/{container}/{axis}/description_paragraphs/(0|[1-9][0-9]*)', replace):
                raise ValueError(f'Explanation cannot replace this field: {setting}/{axis}{replace}')
            original = source_value(profile, replace)
            # Preserve any literal formulas in the line. Broad rewrites of the
            # mathematical specification belong to the canonical review flow.
            formulas = re.findall(r'\$\$[\s\S]*?\$\$|\$(?:\\.|[^$])*\$', original)
            omitted = [formula for formula in formulas if formula not in '\n'.join(paragraphs)]
            if omitted and (not entry.get('corrects_inline_notation') or any(f.startswith('$$') for f in omitted)):
                raise ValueError(f'Explanation would remove an original formula: {setting}/{axis}')
        for pointer in pointers:
            try:
                source_value(profile, pointer)
            except (ValueError, KeyError, TypeError, IndexError) as exc:
                raise ValueError(f'Unresolved explanation source: {setting}/{axis}{pointer}') from exc
    return sections
