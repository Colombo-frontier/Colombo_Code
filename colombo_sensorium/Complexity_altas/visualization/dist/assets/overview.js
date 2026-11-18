/* The homepage overview is an incidence projection of the Atlas navigation labels. */
(() => {
  'use strict';
  const source = document.getElementById('atlas-overview-data');
  if (!source) return;
  const data = JSON.parse(source.textContent);
  const axes = [...document.querySelectorAll('[data-overview-axis]')];
  const groupControl = document.getElementById('overview-group-control');
  const select = document.getElementById('overview-group');
  const chart = document.getElementById('overview-chart');
  const plot = document.getElementById('overview-plot');
  const inspector = document.getElementById('overview-inspector');
  const clear = document.getElementById('overview-clear');
  const svgNS = 'http://www.w3.org/2000/svg';
  const byId = new Map(data.points.map(p => [p.id, p]));
  const status = new Map(data.status_legend.map(s => [s.id, s]));
  const nodes = new Map();
  const positions = new Map();
  let axis = 'TASK', group = 'TASK:family', chosen = null, filters = null;
  let tabStop = data.points[0]?.id, lines, dotOrder = [], related = new Map();
  let frame, lastWidth = 0;
  const svg = (name, attributes = {}) => {
    const e = document.createElementNS(svgNS, name);
    for (const [k, v] of Object.entries(attributes)) e.setAttribute(k, v);
    return e;
  };
  const html = (name, text, cls) => {
    const e = document.createElement(name);
    if (text) e.textContent = text;
    if (cls) e.className = cls;
    return e;
  };
  const activeLabels = point => Object.keys(point.memberships).filter(id => data.concepts[id].group === group);
  const pointStatus = p => status.get(p.status);

  function cluster(point) {
    if (axis === 'TASK') return ['task:' + point.task, data.tasks[point.task], true];
    const labels = activeLabels(point);
    if (labels.length === 0) return ['unknown', 'No recorded label', false];
    if (labels.length === 1) return [labels[0], data.concepts[labels[0]].label, true];
    // The convex label includes the stronger label in the same view; place
    // these settings with Strongly convex if every convex membership has it.
    const cv = 'MODEL:objective_convexity:convex';
    const strong = 'MODEL:objective_convexity:strongly_convex';
    if (labels.length === 2 && labels.includes(cv) && labels.includes(strong) &&
        point.memberships[cv].every(v => point.memberships[strong].includes(v))) {
      return [strong, data.concepts[strong].label, true];
    }
    return ['multiple', 'Multiple recorded labels', false];
  }

  function draw() {
    const width = Math.floor(chart.clientWidth);
    if (width < 200) return;
    lastWidth = width;
    const hasFocus = plot.contains(document.activeElement);
    positions.clear(); nodes.clear(); dotOrder = [];
    plot.replaceChildren();
    const backgrounds = svg('g', {'aria-hidden': 'true'});
    const guides = svg('g', {class: 'overview-guides', 'aria-hidden': 'true'});
    lines = svg('g', {class: 'overview-edges', 'aria-hidden': 'true'});
    const dots = svg('g');
    plot.append(backgrounds, guides, lines, dots);
    const cohorts = new Map();
    for (const point of data.points) {
      const [key, label, shared] = cluster(point);
      if (!cohorts.has(key)) cohorts.set(key, {key, label, shared, points: []});
      cohorts.get(key).points.push(point);
    }
    const ordered = [...cohorts.values()].sort((a, b) =>
      Number(a.key === 'unknown') - Number(b.key === 'unknown') ||
      b.points.length - a.points.length || a.label.localeCompare(b.label));
    const pad = 11, gap = 9, step = width < 620 ? 13 : 15;
    const available = width - 2 * pad;
    const tileWidth = cohort => Math.min(available, Math.max(width < 530 ? 144 : 164,
      Math.ceil(Math.sqrt(cohort.points.length * 3.5)) * step + 22,
      Math.ceil(cohort.label.length * 5.6 + 20)));
    let x = pad, y = pad, rowHeight = 0;
    for (const [index, cohort] of ordered.entries()) {
      const n = cohort.points.length;
      let w = tileWidth(cohort);
      if (x > pad && x + w > width - pad) {
        x = pad; y += rowHeight + gap; rowHeight = 0;
      }
      const next = ordered[index + 1];
      if (x === pad && n >= 100 && (!next || w + gap + tileWidth(next) > available)) w = available;
      const perRow = Math.max(1, Math.floor((w - 22) / step));
      const h = 45 + Math.ceil(n / perRow) * step;
      rowHeight = Math.max(rowHeight, h);
      backgrounds.append(svg('rect', {x, y, width: w, height: h, rx: 7,
                                      class: 'overview-tile' + (cohort.shared ? '' : ' is-unclassified')}));
      const title = svg('text', {x: x + 10, y: y + 17, class: 'overview-tile-label'});
      title.textContent = cohort.label;
      const sub = svg('text', {x: x + 10, y: y + 32, class: 'overview-tile-count'});
      sub.textContent = `${n} ${n === 1 ? 'setting' : 'settings'}`;
      backgrounds.append(title, sub);
      cohort.points.forEach((p, i) => {
        const col = i % perRow, row = Math.floor(i / perRow);
        const cx = x + 11 + step / 2 + col * step, cy = y + 44 + row * step;
        positions.set(p.id, {cx, cy});
        if (cohort.shared && col > 0) {
          guides.append(svg('line', {x1: cx - step, y1: cy, x2: cx, y2: cy}));
        }
        const dot = svg('circle', {cx, cy, r: width < 620 ? 4.6 : 5.1, fill: pointStatus(p).color,
          class: 'overview-dot', role: 'button', tabindex: p.id === tabStop ? '0' : '-1',
          'aria-label': `${p.title} · ${p.id} · ${pointStatus(p).label}`,
          'data-overview-id': p.id});
        const tooltip = svg('title');
        tooltip.textContent = `${p.title} · ${pointStatus(p).label}`;
        dot.append(tooltip); dots.append(dot);
        nodes.set(p.id, dot); dotOrder.push(p.id);
      });
      x += w + gap;
    }
    const height = y + rowHeight + pad;
    plot.setAttribute('viewBox', `0 0 ${width} ${height}`);
    plot.style.height = height + 'px';
    updateLinks();
    if (hasFocus) nodes.get(tabStop)?.focus({preventScroll: true});
  }

  function updateInspector() {
    inspector.replaceChildren();
    inspector.hidden = !chosen; clear.hidden = !chosen;
    if (!chosen) return;
    const p = byId.get(chosen), summary = pointStatus(p);
    const intro = html('div', '', 'overview-selection');
    intro.append(html('code', p.id), html('h3', p.title));
    const label = html('span', summary.label, 'overview-selected-status');
    label.style.setProperty('--swatch', summary.color);
    label.title = summary.description;
    intro.append(label);
    const info = html('div', '', 'overview-detail');
    const statusList = Object.entries(p.comparisons).map(([code, n]) => `${n} ${data.comparison_labels[code]}`);
    info.append(html('p', `Documented comparisons · ${statusList.join(' · ')}`, 'overview-breakdown'));
    const groupLabel = axis === 'TASK' ? 'Task family' : data.groups.find(g => g.id === group).label;
    const names = activeLabels(p).map(id => data.concepts[id].label);
    info.append(html('p', names.length
      ? `${related.size} connected · ${groupLabel}: ${names.join(', ')}`
      : `No recorded label for ${groupLabel.toLowerCase()}.`, 'overview-connection-count'));
    const links = html('div', '', 'overview-profile-links');
    const profile = html('a', 'Open profile ↗');
    profile.href = `settings/${encodeURIComponent(p.id)}.html`;
    const graph = html('a', 'Relationship graph ↗');
    graph.href = `graph.html?setting=${encodeURIComponent(p.id)}`;
    links.append(profile, graph);
    info.append(links);
    inspector.append(intro, info);
  }

  function updateLinks() {
    if (!lines) return;
    lines.replaceChildren(); related = new Map();
    if (chosen && positions.has(chosen)) {
      const root = positions.get(chosen);
      const labels = activeLabels(byId.get(chosen));
      for (const p of data.points) {
        if (p.id === chosen) continue;
        const common = labels.filter(cid => p.memberships[cid]);
        if (!common.length) continue;
        related.set(p.id, common);
        const target = positions.get(p.id);
        const line = svg('line', {x1: root.cx, y1: root.cy, x2: target.cx, y2: target.cy,
          class: filters && !filters.has(p.id) ? 'is-filtered' : '',
          'data-overview-link': p.id});
        lines.append(line);
      }
    }
    for (const [id, node] of nodes) {
      node.classList.toggle('is-filtered', !!filters && !filters.has(id) && id !== chosen);
      node.classList.toggle('is-unrelated', !!chosen && id !== chosen && !related.has(id));
      node.classList.toggle('is-selected', id === chosen);
      node.setAttribute('aria-pressed', String(id === chosen));
      const p = byId.get(id);
      const shared = related.get(id)?.map(cid => data.concepts[cid].label).join(', ');
      const name = `${p.title} · ${p.id} · ${pointStatus(p).label}` + (shared ? ` · Shared: ${shared}` : '');
      node.setAttribute('aria-label', name);
      node.firstElementChild.textContent = name;
    }
    if (chosen) {
      // Bring the selected node above neighboring points.
      const node = nodes.get(chosen);
      if (node && node !== document.activeElement) node.parentNode.append(node);
    }
    updateInspector();
  }

  function focusPoint(id) {
    if (nodes.has(tabStop)) nodes.get(tabStop).setAttribute('tabindex', '-1');
    tabStop = id;
    nodes.get(id).setAttribute('tabindex', '0');
  }
  function pin(id) {
    chosen = id;
    focusPoint(id);
    updateLinks();
  }
  function setAxis(newAxis) {
    axis = newAxis;
    const groups = data.groups.filter(g => g.axis === axis);
    group = groups[0].id;
    select.replaceChildren(...groups.map(g => {
      const option = html('option', g.label); option.value = g.id; return option;
    }));
    groupControl.hidden = groups.length < 2;
    axes.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.overviewAxis === axis)));
    plot.dataset.axis = axis;
    draw();
  }
  axes.forEach(button => button.addEventListener('click', () => setAxis(button.dataset.overviewAxis)));
  select.addEventListener('change', () => { group = select.value; draw(); });
  clear.addEventListener('click', () => {
    chosen = null; updateLinks(); nodes.get(tabStop)?.focus({preventScroll: true});
  });
  plot.addEventListener('click', event => {
    const node = event.target.closest('[data-overview-id]');
    if (node) pin(node.dataset.overviewId);
  });
  plot.addEventListener('keydown', event => {
    const node = event.target.closest('[data-overview-id]');
    if (!node) return;
    const id = node.dataset.overviewId;
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault(); pin(id);
    } else if (event.key === 'Escape' && chosen) {
      chosen = null; updateLinks();
    } else if (['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End'].includes(event.key)) {
      event.preventDefault();
      const i = dotOrder.indexOf(id);
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? dotOrder.length - 1 :
        Math.max(0, Math.min(dotOrder.length - 1, i + (['ArrowLeft','ArrowUp'].includes(event.key) ? -1 : 1)));
      focusPoint(dotOrder[next]); nodes.get(tabStop).focus();
    }
  });
  document.addEventListener('atlas:results', event => {
    const ids = event.detail.ids;
    filters = ids.length === data.points.length ? null : new Set(ids);
    updateLinks();
  });
  function scheduleDraw() {
    if (Math.floor(chart.clientWidth) === lastWidth) return;
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(draw);
  }
  if (typeof ResizeObserver !== 'undefined') new ResizeObserver(scheduleDraw).observe(chart);
  else window.addEventListener('resize', scheduleDraw);
  setAxis('TASK');
})();
