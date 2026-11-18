/* Offline 3D atlas, projected into a Canvas2D scene with a real orbit camera. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const canvas = $('nebula-canvas');
  if (!canvas) return;
  const stage = $('nebula-stage'), ctx = canvas.getContext('2d');
  if (!ctx) {
    stage.textContent = 'This browser cannot render the 3D atlas. Use the 2D map below.';
    return;
  }
  const overview = JSON.parse($('atlas-overview-data').textContent);
  const layout = JSON.parse($('atlas-nebula-data').textContent);
  const palette = new Map(overview.status_legend.map(s => [s.id, s]));
  const style = getComputedStyle($('atlas-nebula'));
  const colors = new Map(overview.status_legend.map(s => [s.id, style.getPropertyValue('--star-' + s.id).trim() || s.color]));
  const traces = {
    TASK: {color: style.getPropertyValue('--trace-task').trim(), dash: []},
    ORACLE: {color: style.getPropertyValue('--trace-oracle').trim(), dash: [5, 3]},
    MODEL: {color: style.getPropertyValue('--trace-model').trim(), dash: [2, 3]},
  };
  const traceInputs = [...$('nebula-links').querySelectorAll('input')];
  const inspector = $('nebula-inspector'), lookup = $('nebula-find'), tip = $('nebula-tooltip');
  const points = overview.points.map(p => ({...p, xyz: layout.positions[p.id], labels: Object.keys(p.memberships)}));
  const byId = new Map(points.map(p => [p.id, p]));
  const bundles = AtlasNebulaBundles.create(overview, points, traces);
  const modeButtons = [...document.querySelectorAll('[data-nebula-mode]')];
  const labelSelect = $('nebula-bundle-label'), taskSelect = $('nebula-bundle-task');
  const options = document.createDocumentFragment();
  for (const p of points) {
    const option = document.createElement('option');
    option.value = p.id; option.label = p.title; options.append(option);
  }
  $('nebula-options').append(options);
  const initial = {yaw: -.21, pitch: .16, zoom: 1};
  const camera = {...initial};
  const pointers = new Map();
  let selected = null, hovered = null, matching = null, edges = new Map();
  let projected = [], projectedById = new Map(), frame = 0, lastFrame = 0;
  let spinning = false, visible = true, clickCandidate = null;
  let mode = 'star', bundleFocus = null, bundleHover = null;
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const enabled = () => traceInputs.filter(input => input.checked).map(input => input.value);
  const make = (tag, text, cls) => {
    const el = document.createElement(tag);
    if (text) el.textContent = text;
    if (cls) el.className = cls;
    return el;
  };

  for (const [axis, name] of [['TASK', 'Task'], ['ORACLE', 'Oracle'], ['MODEL', 'Model']]) {
    const group = make('optgroup'); group.label = name; group.dataset.axis = axis;
    for (const label of bundles.visibleLabels([axis])) {
      const option = make('option', label.label + ' · ' + label.members.length); option.value = label.id; group.append(option);
    }
    labelSelect.append(group);
  }
  function updateRelations() {
    const all = mode === 'all', axes = enabled();
    canvas.dataset.connectionMode = mode;
    $('nebula-links').hidden = !all && !selected;
    $('nebula-bundle-tools').hidden = !all;
    for (const input of traceInputs) {
      const axis = input.value;
      const count = all ? bundles.summary([axis]).bundles : (edges.get(axis)?.length || 0);
      $('nebula-links').querySelector('[data-nebula-count="' + axis + '"]').textContent =
        count + (all ? (count === 1 ? ' bundle' : ' bundles') : (count === 1 ? ' neighbor' : ' neighbors'));
    }
    if (!all) return;
    for (const group of labelSelect.querySelectorAll('optgroup')) group.disabled = !axes.includes(group.dataset.axis);
    if (bundleFocus && !axes.includes(bundles.get(bundleFocus.id).axis)) bundleFocus = null;
    const label = bundleFocus && bundles.get(bundleFocus.id);
    labelSelect.value = label ? label.id : '';
    $('nebula-bundle-task-label').hidden = !label || label.tasks.size < 2;
    $('nebula-bundle-clear').hidden = !label;
    if (taskSelect.dataset.label !== (label?.id || '')) {
      taskSelect.replaceChildren();
      const option = make('option', 'All task clusters'); option.value = ''; taskSelect.append(option);
      if (label) for (const [task, b] of label.tasks) {
        const option = make('option', overview.tasks[task] + ' · ' + b.members.length); option.value = task; taskSelect.append(option);
      }
      taskSelect.dataset.label = label?.id || '';
    }
    taskSelect.value = bundleFocus?.task || '';
    if (label) {
      const ids = bundles.members(label.id, bundleFocus.task);
      const name = label.label + (bundleFocus.task ? ' · ' + overview.tasks[bundleFocus.task] : '');
      $('nebula-bundle-status').textContent = name + ' · ' + ids.length + (ids.length === 1 ? ' setting' : ' settings') +
        (matching ? ' · ' + ids.filter(id => matching.has(id)).length + ' match the search' : '');
    } else {
      const totals = bundles.summary(axes);
      $('nebula-bundle-status').textContent = totals.labels + ' labels · ' + totals.bundles + ' bundles · ' + totals.memberships.toLocaleString('en-US') + ' label memberships';
    }
  }
  function setBundle(id, task = null) {
    const label = bundles.get(id);
    bundleFocus = label && enabled().includes(label.axis) ? {id, task: label.tasks.has(task) ? task : null} : null;
    hideTip(); setSpin(false); updateRelations();
  }
  function setMode(next) {
    mode = next; hideTip();
    modeButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.nebulaMode === mode)));
    updateRelations(); request();
  }

  function request() {
    if (!frame) frame = requestAnimationFrame(paint);
  }
  function setSpin(value) {
    spinning = value; lastFrame = 0;
    $('nebula-orbit').setAttribute('aria-pressed', String(value));
    request();
  }
  function reset() {
    Object.assign(camera, initial);
    hideTip();
    setSpin(false);
  }
  function zoom(factor) {
    camera.zoom = clamp(camera.zoom * factor, .69, 2.65);
    hideTip(); request();
  }
  function rotate(dx, dy) {
    camera.yaw += dx;
    camera.pitch = clamp(camera.pitch + dy, -1.48, 1.48);
    hideTip(); request();
  }
  function paint(time) {
    frame = 0;
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (w < 10 || h < 10) return;
    if (spinning && visible) {
      if (lastFrame) camera.yaw += Math.min(time - lastFrame, 38) * .00020;
      lastFrame = time;
    }
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const pw = Math.round(w * dpr), ph = Math.round(h * dpr);
    if (canvas.width !== pw || canvas.height !== ph) { canvas.width = pw; canvas.height = ph; }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.globalAlpha = 1;
    const sky = ctx.createLinearGradient(0, 0, w, h);
    sky.addColorStop(0, '#08121e'); sky.addColorStop(.57, '#122431'); sky.addColorStop(1, '#111a2b');
    ctx.fillStyle = sky; ctx.fillRect(0, 0, w, h);
    const sy = Math.sin(camera.yaw), cy = Math.cos(camera.yaw);
    const sp = Math.sin(camera.pitch), cp = Math.cos(camera.pitch);
    const all = mode === 'all';
    const cx = w * .5, cyScreen = h * (all ? .493 : .55);
    let fit = Math.min(w / (all ? 6.74 : 5.72), h / (all ? 4.32 : 3.75));
    function view([x, y, z]) {
      const x1 = x * cy - z * sy, z1 = x * sy + z * cy;
      const y2 = y * cp - z1 * sp, z2 = y * sp + z1 * cp;
      const depth = 6.9 / (6.9 - z2);
      return {x: x1 * depth, y: -y2 * depth, z: z2, depth};
    }
    const inView = points.map(p => ({p, v: view(p.xyz)}));
    if (all) {
      // At the default zoom keep the stars and all rail endpoints framed,
      // even while orbiting or changing the visibility of a rail.
      const frame = [...inView.map(({v}) => v), ...bundles.frameAnchors.map(view)];
      for (const v of frame) {
        if (v.x) fit = Math.min(fit, (cx - 20) / Math.abs(v.x));
        if (v.y < 0) fit = Math.min(fit, (cyScreen - 50) / -v.y);
        if (v.y > 0) fit = Math.min(fit, (h - cyScreen - 23) / v.y);
      }
    }
    const scale = fit * camera.zoom;
    const screen = v => ({...v, x: cx + v.x * scale, y: cyScreen + v.y * scale});
    const project = xyz => screen(view(xyz));
    const clusters = layout.clusters.map(c => ({...c, p: project(c.center)})).sort((a, b) => a.p.z - b.p.z);
    // Smooth colored clouds only. Every discrete luminous point comes from a setting.
    for (const c of clusters) {
      const r = Math.max(8, c.radius * scale * c.p.depth * 1.65);
      ctx.save();
      ctx.translate(c.p.x, c.p.y);
      ctx.rotate((c.p.z + camera.yaw * .4) * .24);
      ctx.scale(1.23, .80);
      const haze = ctx.createRadialGradient(0, 0, 0, 0, 0, r);
      haze.addColorStop(0, c.haze + 'a1');
      haze.addColorStop(.42, c.haze + '5f');
      haze.addColorStop(1, c.haze + '00');
      ctx.fillStyle = haze; ctx.fillRect(-r, -r, 2*r, 2*r);
      ctx.restore();
    }
    projected = inView.map(({p, v}) => {
      const pos = screen(v);
      const radius = clamp((w < 480 ? 2.35 : 2.85) * pos.depth * Math.sqrt(camera.zoom), 1.65, 5.5);
      return {...pos, p, radius};
    }).sort((a, b) => a.z - b.z);
    projectedById = new Map(projected.map(item => [item.p.id, item]));
    const root = projectedById.get(selected);
    const linked = new Set(all && bundleFocus ? bundles.members(bundleFocus.id, bundleFocus.task) : []);
    let axisLabelBoxes = [];
    if (all) {
      axisLabelBoxes = bundles.paint(ctx, {w, h, project, projected: projectedById, axes: enabled(), focus: bundleFocus, hover: bundleHover, matching});
    } else if (root) {
      const activeAxes = enabled();
      const lanes = new Map();
      for (const axis of activeAxes) {
        for (const sid of edges.get(axis) || []) {
          if (!lanes.has(sid)) lanes.set(sid, []);
          lanes.get(sid).push(axis);
        }
      }
      for (const axis of activeAxes) {
        const peers = edges.get(axis) || [];
        peers.forEach(sid => linked.add(sid));
        const {color, dash} = traces[axis];
        ctx.strokeStyle = color; ctx.lineWidth = 1.12; ctx.setLineDash(dash);
        for (const muted of [true, false]) {
          ctx.beginPath();
          ctx.globalAlpha = muted ? .10 : .56;
          for (const sid of peers) {
            if (muted !== (!!matching && !matching.has(sid))) continue;
            const p = projectedById.get(sid);
            const dx = p.x - root.x, dy = p.y - root.y;
            const distance = Math.hypot(dx, dy);
            const pairLanes = lanes.get(sid);
            const offset = (pairLanes.indexOf(axis) - (pairLanes.length - 1) / 2) * Math.min(23, distance * .24);
            ctx.moveTo(root.x, root.y);
            if (offset && distance > 0) {
              ctx.quadraticCurveTo(root.x + dx / 2 - dy / distance * offset,
                                   root.y + dy / 2 + dx / distance * offset, p.x, p.y);
            } else ctx.lineTo(p.x, p.y);
          }
          ctx.stroke();
        }
      }
      ctx.setLineDash([]);
    }
    for (const item of projected) {
      const id = item.p.id, active = id === selected || id === hovered;
      const filtered = matching && !matching.has(id) && id !== selected;
      const distant = (all ? bundleFocus : root) && !linked.has(id) && id !== selected;
      const color = colors.get(item.p.status), r = item.radius;
      const opacity = active ? 1 : clamp(.68 + item.z * .12, .43, .94) * (filtered ? .23 : distant ? .52 : 1);
      ctx.globalAlpha = opacity * (active ? .29 : .12);
      ctx.fillStyle = color;
      ctx.beginPath(); ctx.arc(item.x, item.y, r * (active ? 2.5 : 1.75), 0, Math.PI * 2); ctx.fill();
      ctx.globalAlpha = opacity;
      ctx.beginPath(); ctx.arc(item.x, item.y, r * (active ? 1.21 : 1), 0, Math.PI * 2); ctx.fill();
    }
    if (root) {
      ctx.strokeStyle = '#f3f9f7'; ctx.lineWidth = 1.3; ctx.globalAlpha = .9;
      ctx.beginPath(); ctx.arc(root.x, root.y, root.radius + 3.3, 0, Math.PI * 2); ctx.stroke();
    }
    // Label task anchors in the screen plane so labels remain upright in orbit.
    ctx.globalAlpha = 1; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.font = '600 ' + (w < 520 ? '10px' : '12px') + ' system-ui, sans-serif';
    const labelBoxes = axisLabelBoxes;
    for (const c of clusters.slice().sort((a, b) => b.count - a.count)) {
      const label = c.label;
      const tw = ctx.measureText(label).width;
      const x = c.p.x, y = c.p.y - Math.max(11, c.radius * scale * c.p.depth * .92);
      const rect = {l: x - tw/2 - 4, r: x + tw/2 + 4, t: y - 7, b: y + 7};
      if (rect.l < 3 || rect.r > w - 3 || rect.t < 43 || rect.b > (all ? h * .862 : h - 4) ||
          labelBoxes.some(q => rect.l < q.r && rect.r > q.l && rect.t < q.b && rect.b > q.t)) continue;
      labelBoxes.push(rect);
      ctx.strokeStyle = '#0b1723dd'; ctx.lineWidth = 3.5; ctx.strokeText(label, x, y);
      ctx.fillStyle = '#cbdde3'; ctx.fillText(label, x, y);
    }
    canvas.dataset.points = String(projected.length);
    canvas.dataset.yaw = camera.yaw.toFixed(4);
    canvas.dataset.pitch = camera.pitch.toFixed(4);
    canvas.dataset.zoom = camera.zoom.toFixed(3);
    $('nebula-minus').disabled = camera.zoom <= .69;
    $('nebula-plus').disabled = camera.zoom >= 2.65;
    if (spinning && visible && !document.hidden) request();
  }
  function location(event) {
    const rect = canvas.getBoundingClientRect();
    return {x: event.clientX - rect.left, y: event.clientY - rect.top};
  }
  function pick(pos) {
    let hit = null, distance = Infinity;
    for (let i = projected.length - 1; i >= 0; i--) {
      const item = projected[i];
      const d = Math.hypot(pos.x - item.x, pos.y - item.y);
      if (d <= Math.max(6, item.radius + 3.5) && d < distance - .35) { hit = item; distance = d; }
    }
    return hit;
  }
  function hideTip() {
    hovered = null; bundleHover = null; tip.hidden = true;
  }
  function showTip(item) {
    const id = item?.p.id || null;
    if (id !== hovered || bundleHover) request();
    bundleHover = null;
    hovered = id;
    if (!item) { tip.hidden = true; return; }
    const p = item.p;
    tip.replaceChildren(make('strong', p.title), make('span', p.id + ' · ' + palette.get(p.status).label));
    positionTip(item.x, item.y);
  }
  function positionTip(x, y) {
    tip.hidden = false;
    const w = stage.clientWidth, h = stage.clientHeight;
    tip.style.left = clamp(x + 9, 5, Math.max(5, w - tip.offsetWidth - 5)) + 'px';
    tip.style.top = clamp(y - tip.offsetHeight - 7, 38, Math.max(38, h - tip.offsetHeight - 4)) + 'px';
  }
  function showBundleTip(item) {
    if (hovered || !bundleHover || bundles.key(bundleHover.id, bundleHover.task) !== bundles.key(item.id, item.task)) request();
    hovered = null; bundleHover = item;
    const label = bundles.get(item.id);
    tip.replaceChildren(make('strong', label.label + (item.task ? ' · ' + overview.tasks[item.task] : '')),
      make('span', item.count + (item.count === 1 ? ' setting' : ' settings') + ' · Click to expand'));
    positionTip(item.point.x, item.point.y);
  }
  function setSelection(id) {
    selected = id; hideTip();
    edges = new Map(Object.keys(traces).map(axis => [axis, []]));
    inspector.hidden = !id;
    const summary = $('nebula-selected');
    summary.replaceChildren();
    if (id) {
      const p = byId.get(id);
      const byAxis = {};
      for (const axis of Object.keys(traces)) byAxis[axis] = p.labels.filter(cid => overview.concepts[cid].group.startsWith(axis + ':'));
      for (const other of points) {
        if (other.id === id) continue;
        for (const axis of Object.keys(traces)) {
          if (byAxis[axis].some(cid => other.memberships[cid])) edges.get(axis).push(other.id);
        }
      }
      const breakdown = Object.entries(p.comparisons).map(([code, n]) => n + ' ' + overview.comparison_labels[code]).join(' · ');
      summary.append(make('code', id), make('h3', p.title), make('p', palette.get(p.status).label + ' · ' + breakdown));
      const links = make('div', '', 'nebula-destinations');
      const profile = make('a', 'Open profile ↗'); profile.href = 'settings/' + encodeURIComponent(id) + '.html';
      const graph = make('a', 'Relationship graph ↗'); graph.href = 'graph.html?setting=' + encodeURIComponent(id);
      links.append(profile, graph); summary.append(links);
    }
    inspector.dataset.selected = id || '';
    updateRelations(); request();
  }
  function matchLookup(query, partial) {
    const q = query.trim().toLowerCase();
    if (!q) return null;
    const full = points.find(p => p.id.toLowerCase() === q || p.title.toLowerCase() === q);
    if (full || !partial) return full;
    const matches = points.filter(p => (p.id + ' ' + p.title).toLowerCase().includes(q));
    return matches.length === 1 ? matches[0] : null;
  }
  function chooseLookup(partial) {
    const point = matchLookup(lookup.value, partial);
    const message = $('nebula-lookup-status');
    if (point) { lookup.value = point.id; message.hidden = true; setSpin(false); setSelection(point.id); }
    else if (partial && lookup.value.trim()) { message.textContent = 'Choose a setting from the list or enter its full ID.'; message.hidden = false; }
    else message.hidden = true;
  }

  canvas.addEventListener('pointerdown', event => {
    if (event.button > 0) return;
    const pos = location(event);
    pointers.set(event.pointerId, pos);
    canvas.setPointerCapture(event.pointerId);
    clickCandidate = pointers.size === 1 ? pos : null;
    canvas.classList.add('is-dragging');
    hideTip(); request();
  });
  canvas.addEventListener('pointermove', event => {
    const pos = location(event);
    const old = pointers.get(event.pointerId);
    if (!old) {
      if (!pointers.size && !spinning) {
        const star = pick(pos);
        const bundle = mode === 'all' && !star && bundles.pick(pos);
        if (bundle) showBundleTip(bundle); else showTip(star);
      }
      return;
    }
    pointers.set(event.pointerId, pos);
    if (pointers.size > 1) {
      const other = [...pointers.entries()].find(([id]) => id !== event.pointerId)[1];
      const before = Math.hypot(old.x - other.x, old.y - other.y);
      const after = Math.hypot(pos.x - other.x, pos.y - other.y);
      if (before > 4 && after > 4) zoom(after / before);
      clickCandidate = null;
    } else {
      if (clickCandidate && Math.hypot(pos.x - clickCandidate.x, pos.y - clickCandidate.y) <= 4) return;
      if (spinning) setSpin(false);
      rotate((pos.x - old.x) * .007, (pos.y - old.y) * .007);
      clickCandidate = null;
    }
  });
  const endPointer = event => {
    if (!pointers.has(event.pointerId)) return;
    const pos = location(event);
    if (event.type === 'pointerup' && clickCandidate && Math.hypot(pos.x - clickCandidate.x, pos.y - clickCandidate.y) <= 5) {
      const item = pick(pos);
      if (item) { setSpin(false); setSelection(item.p.id); lookup.value = item.p.id; }
      else if (mode === 'all') {
        const bundle = bundles.pick(pos);
        if (bundle) setBundle(bundle.id, bundle.task);
      }
    }
    pointers.delete(event.pointerId); clickCandidate = null;
    if (!pointers.size) canvas.classList.remove('is-dragging');
  };
  canvas.addEventListener('pointerup', endPointer);
  canvas.addEventListener('pointercancel', endPointer);
  canvas.addEventListener('lostpointercapture', endPointer);
  canvas.addEventListener('pointerleave', () => { hideTip(); request(); });
  canvas.addEventListener('wheel', event => {
    if (!event.ctrlKey && !event.metaKey) return;
    event.preventDefault(); zoom(Math.exp(-event.deltaY * .007));
  }, {passive: false});
  canvas.addEventListener('keydown', event => {
    const turn = {ArrowLeft: [-.13, 0], ArrowRight: [.13, 0], ArrowUp: [0, -.13], ArrowDown: [0, .13]};
    if (turn[event.key]) { event.preventDefault(); setSpin(false); rotate(...turn[event.key]); }
    else if (event.key === '+' || event.key === '=') { event.preventDefault(); zoom(1.18); }
    else if (event.key === '-') { event.preventDefault(); zoom(1 / 1.18); }
    else if (event.key === '0') { event.preventDefault(); reset(); }
    else if (event.key === 'Escape') {
      if (mode === 'all' && bundleFocus) setBundle('');
      else { setSelection(null); lookup.value = ''; }
    }
  });
  $('nebula-orbit').addEventListener('click', () => { hideTip(); setSpin(!spinning); });
  $('nebula-reset').addEventListener('click', reset);
  $('nebula-minus').addEventListener('click', () => zoom(1 / 1.18));
  $('nebula-plus').addEventListener('click', () => zoom(1.18));
  $('nebula-clear').addEventListener('click', () => { setSelection(null); lookup.value = ''; lookup.focus(); });
  modeButtons.forEach(button => button.addEventListener('click', () => setMode(button.dataset.nebulaMode)));
  traceInputs.forEach(input => input.addEventListener('change', () => { hideTip(); updateRelations(); request(); }));
  labelSelect.addEventListener('change', () => setBundle(labelSelect.value));
  taskSelect.addEventListener('change', () => setBundle(labelSelect.value, taskSelect.value));
  $('nebula-bundle-clear').addEventListener('click', () => { setBundle(''); labelSelect.focus(); });
  lookup.addEventListener('input', () => chooseLookup(false));
  lookup.addEventListener('change', () => chooseLookup(false));
  lookup.addEventListener('keydown', event => {
    if (event.key === 'Enter') { event.preventDefault(); chooseLookup(true); }
  });
  document.addEventListener('atlas:results', event => {
    const ids = event.detail.ids;
    matching = ids.length === points.length ? null : new Set(ids);
    $('nebula-count').textContent = matching ? ids.length + ' / ' + points.length + ' match' : points.length + ' settings';
    canvas.dataset.matches = String(ids.length);
    if (mode === 'all') updateRelations();
    request();
  });
  if (typeof ResizeObserver !== 'undefined') new ResizeObserver(request).observe(stage);
  else window.addEventListener('resize', request);
  if (typeof IntersectionObserver !== 'undefined') {
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      lastFrame = 0;
      if (visible) request();
    }).observe(stage);
  }
  document.addEventListener('visibilitychange', () => {
    lastFrame = 0;
    if (!document.hidden) request();
  });
  updateRelations(); request();
})();
