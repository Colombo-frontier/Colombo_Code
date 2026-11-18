/* Local incidence explorer. A path is a classification link, never an identity claim. */
(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('setting-graph-data').textContent);
  const $ = id => document.getElementById(id);
  const clean = value => String(value ?? '').replace(/information interface/gi, 'Oracle interface').replace(/\bcoverage\b/gi, 'applicability');
  const make = (tag, cls, text) => {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (text !== undefined) el.textContent = clean(text);
    return el;
  };
  const byId = new Map(data.settings.map((s, i) => [s.id, i]));
  const axisById = new Map(data.axes.map(a => [a.id, a]));
  const groupMaps = {}, axisMaps = {}, conceptMaps = {};
  const merge = (dst, src) => {
    for (const [i, views] of src) {
      if (!dst.has(i)) dst.set(i, new Set());
      for (const v of views) dst.get(i).add(v);
    }
  };
  for (const [mode, groups] of Object.entries(data.layers)) {
    groupMaps[mode] = new Map(); axisMaps[mode] = new Map(); conceptMaps[mode] = new Map();
    for (const group of groups) {
      const members = new Map();
      groupMaps[mode].set(group.id, {...group, members});
      if (!axisMaps[mode].has(group.axis)) axisMaps[mode].set(group.axis, new Map());
      for (const concept of group.concepts) {
        const entries = new Map(concept.members);
        conceptMaps[mode].set(concept.id, {...concept, group: group.id, members: entries});
        merge(members, entries);
      }
      merge(axisMaps[mode].get(group.axis), members);
    }
  }
  const hash = new URLSearchParams(location.hash.slice(1));
  const seedParam = hash.has('s') ? hash.get('s') : new URLSearchParams(location.search).get('setting');
  const state = {mode: hash.get('layer') === 'machine' ? 'machine' : 'human',
    axis: axisById.has(hash.get('axis')) ? hash.get('axis') : 'TASK', group: hash.get('group') || (hash.size === 0 ? 'TASK:family' : ''),
    concept: hash.get('tag') || '', seed: byId.has(seedParam) ? byId.get(seedParam) : null,
    labelPage: 0, settingPage: 0};
  if (hash.size === 0 && state.seed !== null) {
    const group = groupMaps.human.get(state.group);
    const related = (group?.concepts || []).map(c => conceptMaps.human.get(c.id))
      .filter(c => c.members.has(state.seed)).sort((a, b) => a.members.size - b.members.size);
    state.concept = related[0]?.id || '';
  }
  const L = {axes: $('graph-axes'), crumb: $('graph-breadcrumb'), axis: $('graph-axis-node'),
    groups: $('graph-group-nodes'), concepts: $('graph-concept-nodes'), settings: $('graph-setting-nodes'),
    labelFind: $('graph-label-search'), settingFind: $('graph-setting-search'), seed: $('graph-seed')};
  for (const [i, s] of data.settings.entries()) {
    const option = make('option', '', `${s.id} · ${s.title}`);
    option.value = String(i);
    L.seed.append(option);
  }
  const profileURL = i => `settings/${encodeURIComponent(data.settings[i].id)}.html`;
  const size = map => map.size - (state.seed !== null && map.has(state.seed) ? 1 : 0);
  const nText = (n, noun = 'setting') => `${n} ${noun}${n === 1 ? '' : 's'}`;
  const includesSeed = members => state.seed === null || members.has(state.seed);
  const norm = s => String(s).normalize('NFKC').toLowerCase().trim();
  const button = (label, action, value, pressed, extra = '') => {
    const el = make('button', extra, label);
    el.type = 'button'; el.dataset.action = action; el.dataset.value = value;
    if (pressed !== undefined) el.setAttribute('aria-pressed', String(pressed));
    return el;
  };
  const node = (label, note, action, value, selected) => {
    const el = button(undefined, action, value, selected, 'graph-node' + (selected ? ' is-current' : ''));
    el.append(make('strong', '', label), make('small', '', note));
    return el;
  };
  function persist() {
    const params = new URLSearchParams({layer: state.mode, axis: state.axis, s: state.seed === null ? '' : data.settings[state.seed].id});
    if (state.group) params.set('group', state.group);
    if (state.concept) params.set('tag', state.concept);
    try { history.replaceState(null, '', `#${params}`); } catch (_) { /* file browser may restrict history updates */ }
  }
  function pager(el, action, page, total, step, noun) {
    el.replaceChildren();
    if (total <= step) return;
    const previous = button('←', action, page - 1, undefined, 'graph-plain');
    const next = button('→', action, page + 1, undefined, 'graph-plain');
    previous.setAttribute('aria-label', `Previous ${noun}`); next.setAttribute('aria-label', `Next ${noun}`);
    previous.disabled = page === 0; next.disabled = (page + 1) * step >= total;
    el.append(previous, make('span', '', `${page * step + 1}–${Math.min((page + 1) * step, total)} / ${total}`), next);
  }
  function renderDeclarations() {
    const panel = $('graph-declarations');
    const selected = state.seed === null ? null : data.settings[state.seed].id;
    const entries = data.declared_mathematical_relations.filter(r => !selected || r.declarations.some(d =>
      [d.setting_id, d.relation.source_ref, d.relation.target_ref].includes(selected)));
    $('graph-declaration-count').textContent = `${entries.length} ${entries.length === 1 ? 'declaration group' : 'declaration groups'}`;
    const list = $('graph-declaration-list'); list.replaceChildren();
    if (!panel.open) return;
    if (!entries.length) list.append(make('p', 'graph-placeholder', 'No source declaration refers to the selected setting.'));
    for (const r of entries) {
      const disclosure = make('details', 'graph-declaration');
      disclosure.append(make('summary', '', `${r.id} · ${nText(r.declarations.length, 'source declaration')}`));
      for (const d of r.declarations) {
        const article = make('article', 'graph-declaration-card');
        const rel = d.relation;
        article.append(make('h3', '', `${rel.source_ref || 'Unspecified source'} → ${rel.target_ref || 'Unspecified target'}`));
        article.append(make('p', '', `${String(rel.relation_kind || 'Relation').replace(/_/g, ' ')} · requires review`));
        const conditions = make('ul', 'graph-conditions');
        const rawConditions = rel.conditions || [];
        for (const c of Array.isArray(rawConditions) ? rawConditions : [rawConditions]) conditions.append(make('li', '', c));
        if (conditions.children.length) article.append(conditions);
        const source = make('a', '', `Source: ${d.setting_id} · ${d.source_pointer}`);
        source.href = profileURL(byId.get(d.setting_id)); article.append(source);
        disclosure.append(article);
      }
      list.append(disclosure);
    }
  }
  const svg = $('graph-edges'), network = svg.parentElement;
  let frame = 0;
  function drawLater() {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => {
      svg.replaceChildren();
      const box = network.getBoundingClientRect();
      svg.setAttribute('viewBox', `0 0 ${box.width} ${box.height}`);
      const edge = (from, to, strong) => {
        if (!from || !to) return;
        const a = from.getBoundingClientRect(), b = to.getBoundingClientRect();
        if (b.left <= a.right + 1) return;
        const x1 = a.right - box.left, x2 = b.left - box.left;
        const y1 = a.top + a.height / 2 - box.top, y2 = b.top + Math.min(b.height / 2, 28) - box.top;
        const mid = x1 + (x2 - x1) * .52;
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', `M ${x1},${y1} C ${mid},${y1} ${mid},${y2} ${x2},${y2}`);
        if (strong) path.classList.add('is-selected');
        svg.append(path);
      };
      const axis = L.axis.firstElementChild, group = L.groups.querySelector('.is-current');
      const concept = L.concepts.querySelector('.is-current');
      for (const n of L.groups.querySelectorAll('.graph-node')) edge(axis, n, n === group);
      for (const n of L.concepts.querySelectorAll('.graph-node')) edge(group, n, n === concept);
      // A broad selection connects settings by the current group or axis.
      // Do not draw long edges over unopened lanes.
      for (const n of L.settings.querySelectorAll('.graph-setting-node')) edge(concept, n, true);
    });
  }
  function render() {
    const active = document.activeElement;
    const activeAction = active?.dataset.action, activeValue = active?.dataset.value;
    const axisMap = axisMaps[state.mode], groupsMap = groupMaps[state.mode], conceptsMap = conceptMaps[state.mode];
    if (!axisMap.get(state.axis) || !includesSeed(axisMap.get(state.axis))) {
      state.axis = data.axes.find(a => axisMap.get(a.id) && includesSeed(axisMap.get(a.id)))?.id || 'TASK';
      state.group = ''; state.concept = '';
    }
    const groups = [...groupsMap.values()].filter(g => g.axis === state.axis && includesSeed(g.members));
    let group = groups.find(g => g.id === state.group);
    if (!group) { state.group = ''; state.concept = ''; }
    let concept = conceptsMap.get(state.concept);
    if (!concept || concept.group !== state.group || !includesSeed(concept.members)) { concept = null; state.concept = ''; }
    const axis = axisById.get(state.axis), axisMembers = axisMap.get(state.axis) || new Map();
    const members = concept?.members || group?.members || axisMembers;
    const scopeName = concept?.label || group?.label || axis.label;
    document.querySelector(`input[name="graph-layer"][value="${state.mode}"]`).checked = true;
    L.seed.value = state.seed === null ? '' : String(state.seed);
    L.axes.replaceChildren(...data.axes.map(a => {
      const map = axisMap.get(a.id) || new Map();
      const control = button(a.label, 'axis', a.id, a.id === state.axis, 'graph-axis-tab');
      control.disabled = !includesSeed(map); return control;
    }));
    L.crumb.replaceChildren();
    const crumbs = [[axis.label, 'axis', axis.id], ...(group ? [[group.label, 'group', group.id]] : []), ...(concept ? [[concept.label, 'concept', concept.id]] : [])];
    crumbs.forEach(([label, action, value], index) => {
      if (index) L.crumb.append(make('span', 'graph-chevron', '›'));
      const b = button(label, action, value, undefined, 'graph-crumb');
      if (index === crumbs.length - 1) b.setAttribute('aria-current', 'location');
      L.crumb.append(b);
    });
    $('graph-context').textContent = clean(state.seed === null
      ? `${nText(size(members))} in ${scopeName}. Select a node to narrow the graph.`
      : `${nText(size(members))} share this ${concept ? 'label' : group ? 'property group' : 'axis'} with ${data.settings[state.seed].id}.`);
    L.axis.replaceChildren(node(axis.label, `${nText(groups.length, 'group')} · ${nText(size(axisMembers))}`, 'axis', axis.id, true));
    L.groups.replaceChildren(...groups.map(g => {
      const labelCount = g.concepts.filter(c => includesSeed(conceptsMap.get(c.id).members)).length;
      return node(g.label, `${nText(labelCount, 'label')} · ${nText(size(g.members))}`, 'group', g.id, g === group);
    }));
    if (!groups.length) L.groups.append(make('p', 'graph-placeholder', 'No recorded group in this layer.'));
    L.concepts.replaceChildren();
    $('graph-concept-find').hidden = !group;
    const terms = norm(L.labelFind.value);
    const labelOptions = group ? group.concepts.filter(c => includesSeed(conceptsMap.get(c.id).members) && norm(`${c.label} ${c.id}`).includes(terms)) : [];
    const labelStep = 8;
    state.labelPage = Math.max(0, Math.min(state.labelPage, Math.ceil(labelOptions.length / labelStep) - 1));
    for (const row of labelOptions.slice(state.labelPage * labelStep, (state.labelPage + 1) * labelStep)) {
      const c = conceptsMap.get(row.id);
      L.concepts.append(node(c.label, nText(size(c.members)), 'concept', c.id, c === concept));
    }
    if (!labelOptions.length) L.concepts.append(make('p', 'graph-placeholder', group ? 'No label matches this filter.' : 'Select a property group to see its labels.'));
    pager($('graph-concept-pages'), 'label-page', state.labelPage, labelOptions.length, labelStep, 'labels');
    const q = norm(L.settingFind.value);
    const settingRows = [...members].filter(([i]) => i !== state.seed && norm(`${data.settings[i].title} ${data.settings[i].id}`).includes(q)).sort(([a], [b]) => a - b);
    const step = 7;
    state.settingPage = Math.max(0, Math.min(state.settingPage, Math.ceil(settingRows.length / step) - 1));
    L.settings.replaceChildren();
    for (const [i, viewIds] of settingRows.slice(state.settingPage * step, (state.settingPage + 1) * step)) {
      const s = data.settings[i];
      const row = make('article', 'graph-setting-node');
      const link = make('a', 'graph-setting-title', s.title); link.href = profileURL(i);
      const labels = [...viewIds].sort((a, b) => a - b).map(v => s.views[v].label || s.views[v].id);
      const viewText = labels.length === 1 && labels[0].toLowerCase() === 'main' ? '1 matching view' : `Views: ${labels.join(', ')}`;
      const views = make('span', 'graph-setting-views', viewText);
      const related = button('Explore neighbors ↗', 'seed', String(i), undefined, 'graph-neighbor');
      row.append(make('code', 'graph-setting-id', s.id), link, views, related); L.settings.append(row);
    }
    if (!settingRows.length) L.settings.append(make('p', 'graph-placeholder', 'No settings match this path and text filter.'));
    pager($('graph-setting-pages'), 'setting-page', state.settingPage, settingRows.length, step, 'settings');
    renderDeclarations(); persist(); drawLater();
    if (activeAction && !active.isConnected) {
      const next = [...document.querySelectorAll('[data-action]')].find(el => el.dataset.action === activeAction && el.dataset.value === activeValue && !el.disabled);
      next?.focus({preventScroll: true});
    }
  }
  function resetPages() { state.labelPage = 0; state.settingPage = 0; L.labelFind.value = ''; L.settingFind.value = ''; }
  document.querySelector('.graph-main').addEventListener('click', event => {
    const control = event.target.closest('button[data-action]');
    if (!control) return;
    const {action, value} = control.dataset;
    if (action === 'axis') { state.axis = value; state.group = ''; state.concept = ''; resetPages(); }
    if (action === 'group') { state.group = value; state.concept = ''; resetPages(); }
    if (action === 'concept') { state.concept = value; state.settingPage = 0; L.settingFind.value = ''; }
    if (action === 'seed') { state.seed = Number(value); resetPages(); }
    if (action === 'label-page') state.labelPage = Number(value);
    if (action === 'setting-page') state.settingPage = Number(value);
    render();
  });
  document.querySelector('.graph-layer').addEventListener('change', event => {
    state.mode = event.target.value; state.group = ''; state.concept = ''; resetPages(); render();
  });
  L.seed.addEventListener('change', () => { state.seed = L.seed.value === '' ? null : Number(L.seed.value); resetPages(); render(); });
  L.labelFind.addEventListener('input', () => { state.labelPage = 0; render(); });
  L.settingFind.addEventListener('input', () => { state.settingPage = 0; render(); });
  $('graph-reset').addEventListener('click', () => {
    Object.assign(state, {mode: 'human', axis: 'TASK', group: 'TASK:family', concept: '', seed: null}); resetPages(); render();
  });
  $('graph-declarations').addEventListener('toggle', renderDeclarations);
  if (typeof ResizeObserver !== 'undefined') new ResizeObserver(drawLater).observe(network);
  window.addEventListener('resize', drawLater);
  render();
})();
