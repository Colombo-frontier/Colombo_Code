"""Offline homepage map: effective navigation memberships and comparison status."""
from collections import Counter
from html import escape
import hashlib
import json
from pathlib import Path

# A setting may have several comparison statuses. Show the first applicable
# class here and retain the entire breakdown on its dot.
STATUS = [
    ('optimal', 'Optimal', '#25664b', 'All documented comparisons are optimal.'),
    ('near', 'Near optimal (log gap)', '#a9c479', 'The documented comparisons are optimal or have logarithmic gaps, with at least one logarithmic gap.'),
    ('gap', 'Quantified gap', '#e9bf4d', 'A polynomial or other quantified gap is documented.'),
    ('one', 'One bound missing', '#e68b4c', 'At least one documented comparison lacks an upper or a lower bound.'),
    ('both', 'Both bounds missing', '#fffdf7', 'A single documented comparison lacks both bounds. This is an open bracket.'),
    ('joint', 'Joint budget unresolved', '#a18bbd', 'A joint resource budget remains unresolved.'),
    ('special', 'Infinite or infeasible', '#596370', 'At least one comparison is marked as infinite complexity or an infeasible task.'),
]

AXES = {
    'TASK': [('family', 'Primary task')],
    'ORACLE': [('access', 'Oracle access'), ('quality', 'Feedback quality')],
    'MODEL': [('objective_convexity', 'Objective convexity'), ('smoothness', 'Smoothness and regularity'),
              ('geometry', 'Geometry'), ('structure', 'Problem structure'), ('monotonicity', 'Operator monotonicity')],
}
TASKS = {
    'single_objective': 'Single objective', 'online_bandit': 'Online learning / bandits',
    'minimax': 'Minimax', 'bilevel': 'Bilevel', 'matrix_computation': 'Matrix computation',
    'variational_inequality': 'Variational inequality', 'saddle_point': 'Saddle point',
}
COMPARISON_LABELS = {
    'optimal': 'Optimal', 'logarithmic_gap': 'Logarithmic gap', 'polynomial_gap': 'Polynomial gap',
    'other_quantified_gap': 'Other quantified gap', 'missing_upper': 'Upper bound missing',
    'missing_lower': 'Lower bound missing', 'missing_both': 'Both bounds missing',
    'joint_budget_unclosed': 'Joint budget unresolved', 'infinite_complexity': 'Infinite complexity',
    'infeasible_task': 'Infeasible task',
}


def category(counts):
    if not counts or set(counts) - set(COMPARISON_LABELS):
        raise ValueError(f'Map cannot classify comparison statuses: {counts}')
    for group, codes in (
        ('special', ('infeasible_task', 'infinite_complexity')),
        ('both', ('missing_both',)),
        ('joint', ('joint_budget_unclosed',)),
        ('one', ('missing_upper', 'missing_lower')),
        ('gap', ('polynomial_gap', 'other_quantified_gap')),
        ('near', ('logarithmic_gap',)),
    ):
        if any(counts.get(code, 0) for code in codes):
            return group
    return 'optimal'


def build_overview(profiles, human_tags, dictionary, root):
    groups = [{'id': f'{axis}:{key}', 'axis': axis, 'label': label}
              for axis, group_rows in AXES.items() for key, label in group_rows]
    group_ids = {g['id'] for g in groups}
    concepts = {c['id']: {'id': c['id'], 'group': f'{c["axis"]}:{c["group"]}', 'label': c['label']}
                for c in dictionary['concepts'] if f'{c["axis"]}:{c["group"]}' in group_ids}
    points, totals, comparison_totals = [], Counter(), Counter()
    for p in profiles:
        sid = p['setting_id']
        counts = Counter(c['status']['code'] for c in p['comparisons'])
        if dict(counts) != p['summary_status']['status_counts']:
            raise ValueError(f'Stale comparison status summary in {sid}')
        tone = category(counts)
        totals[tone] += 1
        comparison_totals.update(counts)
        view_membership = {}
        for view in human_tags[sid]['views']:
            for cid in view['facet_ids']:
                if cid in concepts:
                    view_membership.setdefault(cid, []).append(view['view_id'])
        domain = p['primary_domain']
        if domain not in TASKS:
            raise ValueError(f'Unregistered primary task {domain} in {sid}')
        points.append({'id': sid, 'title': p['title'], 'task': domain, 'status': tone,
                       'comparisons': dict(counts), 'memberships': view_membership})
    status_rows = [{'id': cid, 'label': label, 'color': color, 'description': description, 'count': totals[cid]}
                   for cid, label, color, description in STATUS]
    data = {'schema_version': '1.0.0', 'groups': groups, 'concepts': concepts, 'tasks': TASKS,
            'status_legend': status_rows, 'comparison_labels': COMPARISON_LABELS, 'points': points}
    encoded = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    data_path = Path(root) / 'data/derived/atlas_overview.json'
    data_path.write_text(encoded + '\n', encoding='utf-8')
    audit = {'passed': True, 'settings': len(points), 'comparison_count': sum(comparison_totals.values()),
             'status_counts': dict(totals), 'comparison_status_counts': dict(comparison_totals),
             'navigation_concepts': len(concepts), 'setting_concept_incidences': sum(len(p['memberships']) for p in points),
             'category_priority': ['special', 'both', 'joint', 'one', 'gap', 'near', 'optimal'],
             'sha256': hashlib.sha256(data_path.read_bytes()).hexdigest()}
    return data


def overview_markup(data):
    count = len(data['points'])
    legend = ''.join(
        f'<li title="{escape(row["description"], quote=True)}"><i style="--swatch:{row["color"]}" aria-hidden="true"></i>'
        f'{escape(row["label"])} <span>{row["count"]}</span></li>' for row in data['status_legend']
    )
    markup = f"""
<section class="overview" id="setting-map" aria-labelledby="overview-heading">
  <header class="overview-head">
    <div><h2 id="overview-heading">Setting map</h2><p>{count} settings · Select a dot to see its connections.</p></div>
    <a href="#setting-library">Search settings ↓</a>
  </header>
  <div class="overview-controls">
    <div class="overview-axes" role="group" aria-label="Map axis">
      <button type="button" data-overview-axis="TASK" aria-pressed="true">Task</button>
      <button type="button" data-overview-axis="ORACLE" aria-pressed="false">Oracle</button>
      <button type="button" data-overview-axis="MODEL" aria-pressed="false">Model</button>
    </div>
    <label id="overview-group-control" hidden>Group by <select id="overview-group"></select></label>
    <button type="button" id="overview-clear" hidden>Clear selection</button>
  </div>
  <div class="overview-chart" id="overview-chart">
    <svg id="overview-plot" role="group" aria-label="Map of {count} settings"></svg>
  </div>
  <div class="overview-inspector" id="overview-inspector" aria-live="polite" hidden></div>
  <ul class="overview-legend" aria-label="Status colors">{legend}</ul>
  <p class="overview-note">Colors summarize documented comparisons. Links show shared labels, not mathematical reductions.</p>
</section>"""
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    return markup + f'<script id="atlas-overview-data" type="application/json">{payload}</script>'
