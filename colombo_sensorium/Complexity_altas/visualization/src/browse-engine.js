/* Pure, local search logic shared by the browser UI and release checks. */
(() => {
  'use strict';
  const normalize = value => String(value).normalize('NFKC').toLowerCase()
    .replace(/[‐‑‒–—−-]/g, ' ').replace(/\s+/g, ' ').trim();
  const groupKey = (kind, axis, group) => `${kind}|${axis}|${group}`;
  const escapeRegExp = value => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  function createEngine(records, metadata) {
    const options = new Map();
    metadata.commonAxes.forEach(axis => axis.groups.forEach(group => group.options.forEach(option => {
      options.set(option.id, {...option, groupKey: groupKey('common', option.axis, option.group), groupLabel: group.label});
    })));
    const precise = new Map(metadata.preciseTags.map(tag => [tag.id, {
      ...tag, groupKey: groupKey('advanced', tag.axis, tag.group), groupLabel: tag.groupLabel || tag.group,
    }]));
    const statusLabels = new Map(metadata.statuses.map(status => [status.id, status.label]));
    const aliasMap = new Map();
    options.forEach(option => {
      [...(option.aliases || []), option.label].forEach(alias => {
        const key = normalize(alias);
        if (!key) return;
        if (!aliasMap.has(key)) aliasMap.set(key, []);
        if (!aliasMap.get(key).some(item => item.id === option.id)) aliasMap.get(key).push(option);
      });
    });
    const aliases = [...aliasMap].map(([alias, choices]) => {
      // The generic terms have one explicit semantic dimension. Other
      // genuinely ambiguous aliases remain literal text.
      if (choices.length > 1 && ['exact', '精确', 'exact oracle'].includes(alias)) {
        choices = choices.filter(option => option.axis === 'ORACLE' && /quality/.test(option.group));
      }
      if (choices.length > 1 && ['convex', '凸'].includes(alias)) {
        choices = choices.filter(option => option.axis === 'MODEL' && /convexity/.test(option.group));
      }
      return {alias, choices};
    }).sort((a, b) => b.alias.length - a.alias.length || a.alias.localeCompare(b.alias));
    const sourceRecords = records.map(record => ({
      ...record,
      views: Object.entries(record.viewTagSets).map(([viewId, tagIds]) => {
        const groups = new Map();
        const add = (key, value) => {
          if (!groups.has(key)) groups.set(key, new Set());
          groups.get(key).add(value);
        };
        (record.commonViewFacets[viewId] || []).forEach(id => {
          const option = options.get(id);
          if (option) add(option.groupKey, id);
        });
        tagIds.forEach(id => {
          const tag = precise.get(id);
          if (tag) add(tag.groupKey, id);
        });
        (record.viewStatusCodes[viewId] || []).forEach(id => add('status', id));
        return {id: viewId, groups};
      }),
    }));

    function parseQuery(query, mode = 'smart') {
      const normalized = normalize(query);
      const occupied = Array(normalized.length).fill(false);
      const blocked = Array(normalized.length).fill(false);
      const matches = [];
      const ambiguous = [];
      if (mode === 'smart') aliases.forEach(({alias, choices}) => {
        const latin = /[a-z0-9]/.test(alias);
        const expression = new RegExp(latin ? `(^|[^a-z0-9_])(${escapeRegExp(alias)})(?=$|[^a-z0-9_])` : `(${escapeRegExp(alias)})`, 'g');
        let match;
        while ((match = expression.exec(normalized))) {
          const start = match.index + (latin ? match[1].length : 0);
          const end = start + alias.length;
          if (occupied.slice(start, end).some(Boolean) || blocked.slice(start, end).some(Boolean)) continue;
          // Without a longer recognized negative phrase, a positive suffix
          // must not be extracted from "non convex", "not exact" or the Chinese term for "nonconvex".
          const prefix = normalized.slice(0, start);
          if (/(?:\b(?:non|not|in)\s+|[非不])$/.test(prefix)) {
            for (let i = start; i < end; i += 1) blocked[i] = true;
            continue;
          }
          if (choices.length !== 1) {
            if (!ambiguous.includes(alias)) ambiguous.push(alias);
            continue;
          }
          for (let i = start; i < end; i += 1) occupied[i] = true;
          matches.push({start, end, id: choices[0].id, text: normalized.slice(start, end)});
        }
      });
      const remaining = normalized.split('').map((char, i) => occupied[i] ? ' ' : char).join('');
      const wordRanges = [];
      const tokenExpression = /\S+/g;
      let token;
      while ((token = tokenExpression.exec(remaining))) {
        const leading = token[0].match(/^[,;·/:"'“”‘’()[\]{}.!?]+/)?.[0].length || 0;
        const word = token[0].replace(/^[,;·/:"'“”‘’()[\]{}.!?]+|[,;·/:"'“”‘’()[\]{}.!?]+$/g, '');
        if (/[\p{L}\p{N}_\\]/u.test(word)) wordRanges.push({word, start: token.index + leading, end: token.index + leading + word.length});
      }
      const words = [...new Set(wordRanges.map(item => item.word))];
      return {normalized, concepts: [...new Set(matches.map(match => match.id))], matches, words, wordRanges, ambiguous, mode};
    }

    function textMatches(record, word) {
      if (record.id.toLowerCase().includes(word)) return true;
      if (/^[a-z0-9]+$/.test(word)) {
        return new RegExp(`(^|[^a-z0-9_])${escapeRegExp(word)}(?=$|[^a-z0-9_])`, 'i').test(record.search);
      }
      return record.search.includes(word);
    }

    function makeState(selection, parsed) {
      const groups = new Map();
      const sources = new Map();
      const units = new Map();
      const add = (key, id, unit) => {
        if (!groups.has(key)) groups.set(key, new Set());
        groups.get(key).add(id);
        units.set(unit.key, unit);
      };
      [...new Set(selection.common || [])].forEach(id => {
        const option = options.get(id);
        if (option) add(option.groupKey, id, {key: `common:${id}`, kind: 'common', id,
          groupKey: option.groupKey, label: `${option.groupLabel}: ${option.label}`});
      });
      parsed.concepts.forEach(id => {
        const option = options.get(id);
        if (!option) return;
        const key = `search|${id}`;
        sources.set(key, option.groupKey);
        add(key, id, {key: `search:${id}`, kind: 'search', id, groupKey: key,
          label: `Search: ${option.groupLabel} / ${option.label}`});
      });
      (selection.advanced || []).forEach(id => {
        const tag = precise.get(id);
        if (tag) add(tag.groupKey, id, {key: `advanced:${id}`, kind: 'advanced', id,
          groupKey: tag.groupKey, label: `${tag.axis} / ${tag.groupLabel}: ${tag.label}`});
      });
      (selection.statuses || []).forEach(id => add('status', id, {key: `status:${id}`, kind: 'status', id,
        groupKey: 'status', label: `Status: ${statusLabels.get(id) || id}`}));
      const words = parsed.words.map(word => ({word, key: `text:${word}`}));
      words.forEach(({word, key}) => units.set(key, {key, kind: 'text', id: word, label: `Text: ${word}`}));
      return {groups, sources, units, words, parsed};
    }

    function viewMatches(view, state, ignoredGroups = new Set()) {
      for (const [key, choices] of state.groups) {
        if (ignoredGroups.has(key)) continue;
        const available = view.groups.get(state.sources.get(key) || key);
        if (!available || ![...choices].some(id => available.has(id))) return false;
      }
      return true;
    }

    function recordMatches(record, state, ignoredGroups = new Set()) {
      if (!ignoredGroups.has('text') && !state.words.every(({word}) => textMatches(record, word))) return false;
      return record.views.some(view => viewMatches(view, state, ignoredGroups));
    }

    function results(state) {
      return sourceRecords.filter(record => recordMatches(record, state));
    }

    function matchingViews(record, state) {
      return record.views.filter(view => viewMatches(view, state)).map(view => view.id);
    }

    function facetCounts(state, requestedGroups) {
      const counts = new Map();
      const textEligible = sourceRecords.filter(record => state.words.every(({word}) => textMatches(record, word)));
      requestedGroups.forEach(key => {
        const values = new Map();
        const ignored = new Set([key]);
        textEligible.forEach(record => {
          const present = new Set();
          record.views.forEach(view => {
            if (viewMatches(view, state, ignored)) (view.groups.get(key) || []).forEach(id => present.add(id));
          });
          present.forEach(id => values.set(id, (values.get(id) || 0) + 1));
        });
        counts.set(key, values);
      });
      return counts;
    }

    function withoutUnits(state, removed) {
      const groups = new Map();
      state.groups.forEach((choices, key) => {
        const kept = new Set([...choices].filter(id => {
          const prefix = key === 'status' ? 'status:' : key.startsWith('search|') ? 'search:' : key.startsWith('common|') ? 'common:' : 'advanced:';
          return !removed.has(prefix + id);
        }));
        if (kept.size) groups.set(key, kept);
      });
      return {...state, groups, words: state.words.filter(({key}) => !removed.has(key))};
    }

    function diagnose(state, limit = 4) {
      let minimum = Infinity;
      const candidates = new Map();
      sourceRecords.forEach(record => record.views.forEach(view => {
        const failed = [];
        state.words.forEach(({word, key}) => { if (!textMatches(record, word)) failed.push(key); });
        state.groups.forEach((choices, key) => {
          const available = view.groups.get(state.sources.get(key) || key);
          if (available && [...choices].some(id => available.has(id))) return;
          const prefix = key === 'status' ? 'status:' : key.startsWith('search|') ? 'search:' : key.startsWith('common|') ? 'common:' : 'advanced:';
          choices.forEach(id => failed.push(prefix + id));
        });
        if (failed.length < minimum) { minimum = failed.length; candidates.clear(); }
        if (failed.length === minimum) candidates.set([...failed].sort().join('\n'), [...new Set(failed)]);
      }));
      const suggestions = [...candidates.values()].map(keys => {
        const restored = results(stateAfterRemoval(state, new Set(keys))).length;
        return {keys, labels: keys.map(key => state.units.get(key)?.label || key), restored};
      }).filter(item => item.restored > 0).sort((a, b) => b.restored - a.restored).slice(0, limit);
      return {minimum, suggestions};
    }

    function removeFromQuery(parsed, removed) {
      const ranges = parsed.matches.filter(match => removed.has(`search:${match.id}`)).map(match => [match.start, match.end]);
      (parsed.wordRanges || []).filter(item => removed.has(`text:${item.word}`)).forEach(item => ranges.push([item.start, item.end]));
      const text = parsed.normalized.split('').map((char, i) => ranges.some(([start, end]) => i >= start && i < end) ? ' ' : char).join('');
      return text.replace(/\s+/g, ' ').trim();
    }

    function stateAfterRemoval(state, removed) {
      const selection = {common: [], advanced: [], statuses: []};
      state.units.forEach(unit => {
        if (removed.has(unit.key)) return;
        if (unit.kind === 'common') selection.common.push(unit.id);
        else if (unit.kind === 'advanced') selection.advanced.push(unit.id);
        else if (unit.kind === 'status') selection.statuses.push(unit.id);
      });
      const parsed = parseQuery(removeFromQuery(state.parsed, removed), state.parsed.mode);
      return makeState(selection, parsed);
    }

    return {options, precise, statusLabels, parseQuery, makeState, results, matchingViews, facetCounts, diagnose,
      removeFromQuery, withoutUnits, stateAfterRemoval, records: sourceRecords};
  }
  globalThis.AtlasBrowseEngine = {createEngine, groupKey, normalize};
})();
