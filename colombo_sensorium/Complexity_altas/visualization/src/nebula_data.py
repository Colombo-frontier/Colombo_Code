"""Deterministic three-dimensional layout for the homepage Atlas nebula."""
from collections import Counter, defaultdict
from html import escape
import hashlib
import json
import math
from pathlib import Path

# Keep the seven task families legible from the initial view. Anchor distances
# are layout choices. The local offsets use only recorded navigation labels.
ANCHORS = {
    'single_objective': ((-.27, .06, .02), 1.03, '#255d51'),
    'online_bandit': ((-2.02, .70, .48), .55, '#385a76'),
    'bilevel': ((-1.27, -1.03, -.51), .45, '#57617f'),
    'minimax': ((1.29, .89, .45), .48, '#5c4275'),
    'matrix_computation': ((2.00, -.41, -.43), .47, '#305771'),
    'variational_inequality': ((.86, -1.08, .61), .38, '#427360'),
    'saddle_point': ((.28, 1.36, -.83), .22, '#6b526f'),
}


def unit(key):
    raw = hashlib.sha256(key.encode('utf-8')).digest()
    z = 2 * int.from_bytes(raw[:8], 'big') / (2**64) - 1
    theta = math.tau * int.from_bytes(raw[8:16], 'big') / (2**64)
    r = math.sqrt(max(0, 1 - z*z))
    return (r * math.cos(theta), r * math.sin(theta), z)


def mean(vectors):
    return tuple(sum(v[i] for v in vectors) / len(vectors) for i in range(3)) if vectors else (0, 0, 0)


def label_offset(point, concepts, label_vectors):
    by_group = defaultdict(list)
    for cid in sorted(point['memberships']):
        group = concepts[cid]['group']
        if group.startswith(('ORACLE:', 'MODEL:')):
            by_group[group].append(label_vectors[cid])
    axes = {axis: mean([mean(vectors) for g, vectors in by_group.items() if g.startswith(axis + ':')])
            for axis in ('ORACLE', 'MODEL')}
    return tuple(.54 * axes['ORACLE'][i] + .44 * axes['MODEL'][i] for i in range(3))


def build_nebula(overview, root):
    points = overview['points']
    counts = Counter(p['task'] for p in points)
    by_signature = defaultdict(list)
    by_task = defaultdict(list)
    label_vectors = {cid: unit('atlas-nebula-label:' + cid) for cid in overview['concepts']}
    offsets = {}
    for p in points:
        sid, task = p['id'], p['task']
        by_signature[(task, tuple(sorted(p['memberships'])))].append(sid)
        by_task[task].append(sid)
        offsets[sid] = label_offset(p, overview['concepts'], label_vectors)
    centroids = {task: mean([offsets[sid] for sid in ids]) for task, ids in by_task.items()}
    positions = {}
    golden_angle = math.pi * (3 - math.sqrt(5))
    for (task, signature), ids in sorted(by_signature.items()):
        center, radius, _ = ANCHORS[task]
        n = len(ids)
        phase = math.pi * unit('signature:' + task + '/'.join(signature))[2]
        for i, sid in enumerate(sorted(ids)):
            jitter = unit('atlas-nebula-point:' + sid)
            # Give repeated membership signatures a small three-dimensional
            # spread instead of collapsing them into an unselectable point.
            if n > 1:
                z = 2 * (i + .5) / n - 1
                angle = phase + i * golden_angle
                r = math.sqrt(1 - z*z)
                spiral = (r * math.cos(angle), r * math.sin(angle), z)
                jitter = tuple(.65 * spiral[k] + .35 * jitter[k] for k in range(3))
            # ID-based radial variation fills the cloud interior as well as its surface.
            density = .35 + .65 * (unit('density:' + sid)[2] + 1) / 2
            shape = (1.17, .88, .91) if task == 'single_objective' else (1.02, .92, 1)
            positions[sid] = [round(center[k] + radius * shape[k] * (
                offsets[sid][k] - centroids[task][k] + .82 * density * jitter[k]), 6) for k in range(3)]
    if len(positions) != len(points) or len(set(map(tuple, positions.values()))) != len(points):
        raise ValueError('The nebula must have a distinct 3D point for every setting.')
    data = {'schema_version': '1.0.0',
            'layout': 'primary task anchors; group-balanced oracle and model label offsets; deterministic overlap separation',
            'positions': {p['id']: positions[p['id']] for p in points},
            'clusters': [{'task': task, 'label': overview['tasks'][task], 'count': counts[task],
                          'center': center, 'radius': radius, 'haze': haze}
                         for task, (center, radius, haze) in ANCHORS.items() if counts[task]]}
    target = Path(root) / 'data/derived/atlas_nebula.json'
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    audit = {'passed': True, 'settings': len(points), 'unique_positions': len(positions),
             'task_clusters': dict(counts), 'distinct_membership_signatures': len(by_signature),
             'largest_signature_group': max(map(len, by_signature.values())),
             'semantics': 'Position is illustrative. Connections are only drawn from recorded shared labels.',
             'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
    return data


def nebula_markup(data, overview):
    count = len(data['positions'])
    colors = ''.join(
        f'<li title="{escape(s["description"], quote=True)}"><i data-nebula-status="{s["id"]}"></i>{escape(s["label"])}</li>'
        for s in overview['status_legend']
    )
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    return f"""
<section class="nebula" id="atlas-nebula" aria-labelledby="nebula-heading">
  <header class="nebula-heading">
    <div><h2 id="nebula-heading">Atlas nebula <span>3D</span></h2><p>{count} settings in {len(data['clusters'])} task constellations</p></div>
    <nav aria-label="Other ways to explore"><a href="#setting-map">2D map ↓</a><a href="#setting-library">Search ↓</a></nav>
  </header>
    <div class="nebula-relation-row">
      <div class="nebula-mode" role="group" aria-label="Connections view">
        <button type="button" data-nebula-mode="star" aria-pressed="true">Selected star</button>
        <button type="button" data-nebula-mode="all" aria-pressed="false">All connections</button>
      </div>
      <fieldset id="nebula-links" class="nebula-links" hidden><legend class="nebula-sr">Shared labels by axis</legend>
      <label class="nebula-task"><input type="checkbox" value="TASK" checked><i aria-hidden="true"></i> Task <span data-nebula-count="TASK"></span></label>
      <label class="nebula-oracle"><input type="checkbox" value="ORACLE" checked><i aria-hidden="true"></i> Oracle <span data-nebula-count="ORACLE"></span></label>
      <label class="nebula-model"><input type="checkbox" value="MODEL" checked><i aria-hidden="true"></i> Model <span data-nebula-count="MODEL"></span></label>
      </fieldset>
    </div>
  <div class="nebula-stage" id="nebula-stage">
    <canvas id="nebula-canvas" tabindex="0" aria-label="Interactive three-dimensional atlas of {count} settings" aria-describedby="nebula-instructions"></canvas>
    <div class="nebula-overlay">
      <span class="nebula-match-count" id="nebula-count">{count} settings</span>
      <div class="nebula-camera" role="group" aria-label="3D camera">
        <button type="button" id="nebula-orbit" aria-pressed="false">Orbit</button>
        <button type="button" id="nebula-minus" aria-label="Zoom out">−</button>
        <button type="button" id="nebula-plus" aria-label="Zoom in">+</button>
        <button type="button" id="nebula-reset">Reset view</button>
      </div>
    </div>
    <div id="nebula-tooltip" class="nebula-tooltip" aria-hidden="true" hidden></div>
  </div>
  <div class="nebula-actions">
    <p id="nebula-instructions">Drag to rotate · Pinch or use +/− to zoom · Select a star</p>
    <label class="nebula-lookup"><span>Find a star</span><input type="search" id="nebula-find" list="nebula-options" placeholder="Setting ID" autocomplete="off"><datalist id="nebula-options"></datalist></label>
  </div>
  <p id="nebula-lookup-status" class="nebula-lookup-status" role="status" hidden></p>
  <div class="nebula-relations">
    <div id="nebula-bundle-tools" class="nebula-bundle-tools" hidden>
      <div class="nebula-bundle-pickers">
        <label>Label <select id="nebula-bundle-label"><option value="">All labels</option></select></label>
        <label id="nebula-bundle-task-label" hidden>Task cluster <select id="nebula-bundle-task"></select></label>
        <button type="button" id="nebula-bundle-clear" hidden>Back to all bundles</button>
      </div>
      <p id="nebula-bundle-status" role="status"></p>
      <p>Each bundle connects a label to a task cluster. Thicker lines contain more settings. Select a bundle or label to see its member stars.</p>
    </div>
  </div>
  <div id="nebula-inspector" class="nebula-inspector" hidden>
    <div id="nebula-selected" aria-live="polite"></div>
    <button type="button" id="nebula-clear" class="nebula-clear">Clear selection</button>
  </div>
  <ul class="nebula-legend" aria-label="Setting status colors">{colors}</ul>
  <p class="nebula-note">Task defines the main clouds. Oracle and Model labels shape their interiors. Distances are illustrative; links show shared labels.</p>
</section><script id="atlas-nebula-data" type="application/json">{payload}</script>"""
