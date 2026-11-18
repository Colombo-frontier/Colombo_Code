(() => {
  'use strict';
  const records = JSON.parse(document.getElementById('atlas-search-data').textContent);
  const metadata = JSON.parse(document.getElementById('atlas-browse-meta').textContent);
  const engine = AtlasBrowseEngine.createEngine(records, metadata);
  const search = document.getElementById('search');
  const inputs = [...document.querySelectorAll('input[name="common"], input[name="status"], input[name="tag"]')];
  const rows = [...document.querySelectorAll('[data-setting]')];
  const active = document.getElementById('active-filters');
  const advanced = document.getElementById('advanced-filters');
  const filterShell = document.getElementById('filter-shell');
  const filterToggle = document.getElementById('toggle-filters');
  const tagSearch = document.getElementById('tag-search');
  const taxonomyAxes = [...document.querySelectorAll('.taxonomy-axis')];
  const previousAxisState = new Map();
  let currentState;
  let currentResults = [];
  let timer;

  function findTags() {
    const query = tagSearch.value.trim().toLowerCase();
    if (query && !previousAxisState.size) taxonomyAxes.forEach(axis => previousAxisState.set(axis, axis.open));
    let totalVisible = 0;
    taxonomyAxes.forEach(axis => {
      let visibleInAxis = 0;
      [...axis.querySelectorAll('.taxonomy-subgroup')].forEach(group => {
        let visibleInGroup = 0;
        [...group.querySelectorAll('.filter-option')].forEach(option => {
          const matches = !query || `${axis.dataset.axis} ${group.querySelector('h4').textContent} ${option.querySelector('span').textContent}`.toLowerCase().includes(query);
          option.hidden = !matches;
          if (matches) visibleInGroup += 1;
        });
        group.hidden = visibleInGroup === 0;
        visibleInAxis += visibleInGroup;
      });
      axis.hidden = visibleInAxis === 0;
      if (query) axis.open = visibleInAxis > 0;
      else if (previousAxisState.has(axis)) axis.open = previousAxisState.get(axis);
      totalVisible += visibleInAxis;
    });
    if (!query) previousAxisState.clear();
    document.getElementById('tag-search-empty').hidden = totalVisible !== 0;
  }

  function readState() {
    const selected = name => inputs.filter(input => input.name === name && input.checked).map(input => input.value);
    const parsed = engine.parseQuery(search.value);
    return engine.makeState({common: selected('common'), advanced: selected('tag'), statuses: selected('status')}, parsed);
  }

  function updateCounts(state) {
    // Counts are computed once per group across compatible views, then each
    // setting is counted once per option. Closed advanced vocabularies are
    // deferred until opened; selected advanced groups are always current.
    const relevantInputs = inputs.filter(input => input.name !== 'tag' || advanced.open || input.checked);
    const requestedGroups = new Set(relevantInputs.map(input => input.dataset.groupKey));
    const counts = engine.facetCounts(state, requestedGroups);
    relevantInputs.forEach(input => {
      const n = counts.get(input.dataset.groupKey)?.get(input.value) || 0;
      const label = input.closest('label');
      label.querySelector('.facet-count').textContent = `${n} ${n === 1 ? 'setting' : 'settings'}`;
      label.classList.toggle('is-unavailable', n === 0);
      input.disabled = n === 0 && !input.checked;
      label.setAttribute('aria-disabled', String(input.disabled));
      if (n === 0) {
        label.title = 'No settings match this option with your other groups.';
      } else if (input.name === 'common') {
        label.title = engine.options.get(input.value)?.description || '';
      } else {
        label.title = `${n} ${n === 1 ? 'setting matches' : 'settings match'} this option with your other groups.`;
      }
    });
  }

  function removeUnits(keys) {
    const removed = new Set(keys);
    inputs.forEach(input => {
      const kind = input.name === 'tag' ? 'advanced' : input.name;
      if (removed.has(`${kind}:${input.value}`)) input.checked = false;
    });
    search.value = engine.removeFromQuery(currentState.parsed, removed);
    applyFilters();
  }

  function showChips(state) {
    active.replaceChildren();
    state.units.forEach(unit => {
      const button = document.createElement('button');
      button.className = `active-filter${unit.kind === 'search' ? ' semantic-filter' : ''}`;
      button.type = 'button';
      button.textContent = `${unit.label} ×`;
      button.setAttribute('aria-label', `Remove ${unit.label}`);
      button.addEventListener('click', () => removeUnits([unit.key]));
      active.append(button);
    });
  }

  function showConflict(state) {
    const diagnostic = engine.diagnose(state);
    const explanation = document.getElementById('conflict-explanation');
    explanation.textContent = Number.isFinite(diagnostic.minimum) && diagnostic.minimum > 0
      ? `No setting currently satisfies these conditions in one view. Remove at least ${diagnostic.minimum} selected ${diagnostic.minimum === 1 ? 'condition' : 'conditions'} to restore a documented match.`
      : 'No documented setting currently matches this combination in one view.';
    const container = document.getElementById('relaxation-options');
    container.replaceChildren();
    diagnostic.suggestions.forEach(suggestion => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'relaxation-button';
      const label = document.createElement('span');
      label.textContent = `Remove ${suggestion.labels.join(' + ')}`;
      const count = document.createElement('strong');
      count.textContent = `Show ${suggestion.restored} ${suggestion.restored === 1 ? 'setting' : 'settings'} →`;
      button.append(label, count);
      button.addEventListener('click', () => removeUnits(suggestion.keys));
      container.append(button);
    });
  }

  function applyFilters() {
    const start = performance.now();
    currentState = readState();
    currentResults = engine.results(currentState);
    const visibleRecords = new Map(currentResults.map(record => [record.id, record]));
    rows.forEach(row => {
      const record = visibleRecords.get(row.dataset.setting);
      row.hidden = !record;
      if (!record) return;
      const scope = row.querySelector('.matching-views');
      const views = currentState.groups.size && record.views.length > 1
        ? engine.matchingViews(record, currentState) : [];
      scope.hidden = !views.length || views.length === record.views.length;
      if (!scope.hidden) {
        scope.textContent = `Matching ${views.length === 1 ? 'view' : 'views'} · ${views.map(id => record.viewLabels[id]).join(', ')}`;
      }
    });
    const visible = currentResults.length;
    document.getElementById('results-label').textContent = `${visible} ${visible === 1 ? 'setting' : 'settings'}`;
    document.getElementById('filter-toggle-count').textContent = currentState.units.size ? `${currentState.units.size} conditions` : '';
    document.getElementById('empty-state').hidden = visible !== 0;
    showChips(currentState);
    if (visible === 0) showConflict(currentState);
    updateCounts(currentState);
    document.dispatchEvent(new CustomEvent('atlas:results', {detail: {ids: [...visibleRecords.keys()]}}));
    window.AtlasBrowseApp.lastDurationMs = performance.now() - start;
  }

  function reset() {
    inputs.forEach(input => { input.checked = false; });
    search.value = '';
    tagSearch.value = '';
    findTags();
    applyFilters();
  }

  window.AtlasBrowseApp = {
    engine, applyFilters, reset,
    snapshot: () => ({ids: currentResults.map(record => record.id), conditions: [...currentState.units.values()],
      concepts: currentState.parsed.concepts, words: currentState.parsed.words}),
  };
  filterToggle.addEventListener('click', () => {
    const expanded = !filterShell.classList.contains('is-open');
    filterShell.classList.toggle('is-open', expanded);
    filterToggle.setAttribute('aria-expanded', String(expanded));
  });
  advanced.addEventListener('toggle', event => {
    if (event.target === advanced && advanced.open && currentState) updateCounts(currentState);
  });
  tagSearch.addEventListener('input', findTags);
  search.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(applyFilters, 120); });
  inputs.forEach(input => input.addEventListener('change', applyFilters));
  document.getElementById('reset-filters').addEventListener('click', reset);
  document.getElementById('clear-empty').addEventListener('click', reset);
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
      event.preventDefault();
      search.focus();
    }
    if (event.key === 'Escape' && document.activeElement === search) {
      search.value = '';
      applyFilters();
      search.blur();
    }
  });
  applyFilters();
})();
