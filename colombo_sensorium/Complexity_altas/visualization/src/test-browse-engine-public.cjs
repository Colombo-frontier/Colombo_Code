#!/usr/bin/env node
'use strict';
// End-to-end checks against the built local HTML, current browse evidence,
// and independent negative/scope fixtures. No browser or network is needed.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {performance} = require('node:perf_hooks');
const root = path.resolve(__dirname, '../..');
const reportPath = process.argv[2] ? path.resolve(process.argv[2]) : null;
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const page = read('visualization/dist/index.html');
const embedded = id => JSON.parse(page.match(new RegExp(`<script id="${id}" type="application/json">([\\s\\S]*?)</script>`))[1]);
const records = embedded('atlas-search-data');
const metadata = embedded('atlas-browse-meta');
const toolkitDictionary = JSON.parse(read('data/vocabulary/human_tags.json'));
const crypto = require('node:crypto');
const projection = JSON.parse(read('visualization/dist/navigation-projection.json')).settings;
const toolkitTags = new Map(records.map(record => {
  const native = JSON.parse(read(`data/settings/${record.id}/human_tags.json`));
  const projected = projection[record.id];
  if (!projected) return [record.id, native];
  for (const name of ['profile.json', 'classification.json', 'human_tags.json']) {
    const actual = crypto.createHash('sha256').update(read(`data/settings/${record.id}/${name}`)).digest('hex');
    assert.equal(actual, projected.input_files[name]);
  }
  assert.equal(crypto.createHash('sha256').update(read('data/vocabulary/human_tags.json')).digest('hex'), projected.dictionary_sha256);
  assert.deepEqual(projected.tags.details, native.details);
  assert.equal(projected.native_files_changed, false);
  return [record.id, projected.tags];
}));
const navigationAdditions = JSON.parse(read('data/derived/toolkit_navigation_additions.json')).settings;
const effectiveFacetIds = (tags, view) => [...new Set([
  ...view.facet_ids,
  ...(navigationAdditions[tags.setting_id]?.facets || [])
    .filter(facet => facet.view_ids.includes(view.view_id)).map(facet => facet.concept_id),
])];
const dataAudit = {semantic_fixtures: {checks: JSON.parse(read('visualization/src/browse-fixtures.json'))}};
vm.runInThisContext(read('visualization/src/browse-engine.js'), {filename: 'browse-engine.js'});
const engine = globalThis.AtlasBrowseEngine.createEngine(records, metadata);
const checks = [];
const run = (name, fn) => {
  try { const detail = fn(); checks.push({name, passed: true, ...(detail || {})}); }
  catch (error) { checks.push({name, passed: false, error: error.message}); }
};
const state = (common = [], query = '', advanced = [], statuses = []) => engine.makeState({common, advanced, statuses}, engine.parseQuery(query));
const ids = s => engine.results(s).map(record => record.id).sort();
const exampleFacetIds = ['ORACLE:access:zero', 'ORACLE:quality:exact', 'MODEL:objective_convexity:convex'];
const example = state(exampleFacetIds);
const exampleIds = ids(example);
const commonId = (axis, group, value) => [...engine.options.values()].find(option => option.axis === axis && option.group === group && option.value === value).id;
const convex = commonId('MODEL', 'objective_convexity', 'convex');
const strong = commonId('MODEL', 'objective_convexity', 'strongly_convex');
const notAssumed = commonId('MODEL', 'objective_convexity', 'not_assumed');
const exact = commonId('ORACLE', 'quality', 'exact');

run('colombo_search_and_badges_cover_all_adopted_contributions', () => {
  const registry = JSON.parse(read('data/derived/colombo_contributions.json')).settings;
  const highlighted = Object.keys(registry).filter(id => registry[id].state === 'adopted').sort();
  assert.deepEqual(embedded('atlas-overview-data').points.filter(point => point.colombo).map(point => point.id).sort(), highlighted);
  const manuscriptIds = new Set(JSON.parse(read('data/sources/colombo/catalog.json')).map(source => source.id));
  assert.equal(manuscriptIds.size, 30);
  const coveredManuscripts = new Set();
  const attributed = records.filter(record => {
    const profile = JSON.parse(read(`data/settings/${record.id}/profile.json`));
    const refs = profile.references.filter(reference => manuscriptIds.has(reference.id));
    refs.forEach(reference => coveredManuscripts.add(reference.id));
    return refs.length > 0;
  }).map(record => record.id).sort();
  assert.equal(attributed.length, 36);
  assert.deepEqual([...coveredManuscripts].sort(), [...manuscriptIds].sort());
  // Attribution includes non-closed results; rate status is a separate filter.
  const expected = [...new Set([...highlighted, ...attributed])].sort();
  assert.equal(expected.length, 84);
  assert.deepEqual(ids(state([], '★ Colombo')), expected);
  assert.deepEqual(ids(state([], 'Colombo')), expected);
  return {adopted_contributions: highlighted.length, attributed_profiles: attributed.length,
    manuscript_sources: coveredManuscripts.size, matching_settings: expected.length};
});

run('example_matches_current_source_view_intersection', () => {
  const expected = [...toolkitTags.values()].filter(tags => tags.views.some(view => exampleFacetIds.every(id => effectiveFacetIds(tags, view).includes(id)))).map(tags => tags.setting_id).sort();
  assert.deepEqual(exampleIds, expected);
  assert(exampleIds.length > 0);
  return {matching_settings: exampleIds.length, setting_ids: exampleIds};
});
run('toolkit_and_local_navigation_and_exact_tags_are_bound_to_their_own_views', () => {
  assert.equal(metadata.toolkitVocabularyVersion, toolkitDictionary.version);
  assert.deepEqual([...engine.options.keys()].sort(), toolkitDictionary.concepts.map(concept => concept.id).sort());
  assert.deepEqual([...engine.precise.keys()].sort(), toolkitDictionary.detail_concepts.map(concept => concept.machine_concept_id).sort());
  for (const record of records) {
    const tags = toolkitTags.get(record.id);
    for (const view of tags.views) {
      assert.deepEqual([...record.commonViewFacets[view.view_id]].sort(), effectiveFacetIds(tags, view).sort());
      const exact = tags.details.filter(detail => detail.view_ids.includes(view.view_id)).map(detail => detail.machine_concept_id);
      assert.deepEqual([...record.viewTagSets[view.view_id]].sort(), [...new Set(exact)].sort());
    }
  }
  const smooth = commonId('MODEL', 'smoothness', 'function_lipschitz');
  assert(ids(state([smooth])).includes('SO_ZO_E01'));
  assert([...engine.options.values()].some(option => option.axis === 'MODEL' && option.group === 'geometry'));
});
run('ball_geometry_recovers_explicit_feasible_domains', () => {
  const ball = commonId('MODEL', 'geometry', 'ball');
  const query = [...exampleFacetIds, ball];
  const matching = ids(state(query));
  const positives = ['SO_ZO_E01', 'SO_ZO_E02', 'SO_ZO_E03', 'SO_ZO_E06b', 'SO_ZO_E06e', 'SO_ZO_E07_neighborhood', 'SO_ZO_E09c', 'SO_ZO_E09c_sc'];
  const localizationOnly = ['SO_ZO_E04', 'SO_ZO_E05', 'SO_ZO_E06a', 'SO_ZO_E06d', 'SO_ZO_E06f_rand', 'SO_ZO_E09a', 'SO_ZO_E09b', 'SO_ZO_O01'];
  for (const id of positives) {
    assert(matching.includes(id), `Missing explicit feasible ball: ${id}`);
    const source = read(`visualization/dist/settings/${id}.html`);
    assert(source.includes(id === 'SO_ZO_E03' ? 'queries and output in the ball' : 'Explicit feasible domain'));
  }
  for (const id of localizationOnly) assert(!matching.includes(id), `Localization ball became a feasible ball: ${id}`);
  const e03 = toolkitTags.get('SO_ZO_E03');
  const e03ByView = new Map(e03.views.map(view => [view.view_id, effectiveFacetIds(e03, view)]));
  assert(e03ByView.get('bounded_query_deterministic').includes(ball), 'Bounded-query regime must expose its feasible ball');
  assert(!e03ByView.get('deterministic').includes(ball), 'Unrestricted deterministic view must remain unrestricted');
  assert(!e03ByView.get('randomized').includes(ball), 'Unrestricted randomized view must remain unrestricted');
  assert.deepEqual(ids(state([], 'zeroth-order exact convex ball geometry')), matching);
  const group = globalThis.AtlasBrowseEngine.groupKey('common', 'MODEL', 'geometry');
  assert.equal(engine.facetCounts(example, new Set([group])).get(group).get(ball), matching.length);
  assert.equal(engine.options.get(ball).count_settings, ids(state([ball])).length);
  return {matching_settings: matching.length, setting_ids: matching};
});
run('graph_entry_points_from_index_and_profile', () => {
  assert(page.includes('href="graph.html"'));
  assert(read('visualization/dist/settings/SO_ZO_E01.html').includes('href="../graph.html?setting=SO_ZO_E01"'));
  assert(fs.existsSync(path.join(root, 'visualization/dist/graph.html')));
});
run('single_objective_ordinals_agree_across_atlas_views', () => {
  const catalog = JSON.parse(read('data/derived/catalog.json')).profiles;
  const settingIds = catalog.map(entry => entry.id);
  const singleCount = catalog.filter(entry => entry.domain === 'single_objective').length;
  assert.deepEqual(records.map(record => record.id), settingIds);
  assert.deepEqual(embedded('atlas-overview-data').points.map(point => point.id), settingIds);
  assert.deepEqual(Object.keys(embedded('atlas-nebula-data').positions), settingIds);
  const graph = JSON.parse(read('data/derived/setting_graph.json'));
  assert.deepEqual(graph.settings.map(setting => setting.id), settingIds);
  const cards = [...page.matchAll(/class="setting-row(?: [^"]+)?" data-setting="([^"]+)" data-setting-id="[^"]+"><div class="setting-order">(\d+)<\/div>/g)];
  assert.deepEqual(cards.map(card => card[1]), settingIds);
  for (const [index, entry] of catalog.entries()) {
    const number = String(index + 1).padStart(2, '0');
    assert.equal(entry.order, index + 1, entry.id);
    assert.equal(entry.domain === 'single_objective', index < singleCount, entry.id);
    assert.equal(cards[index][2], number, entry.id);
    const profile = read(`visualization/dist/settings/${entry.id}.html`);
    assert(profile.includes(`All settings <span>${number} / ${String(catalog.length).padStart(2, '0')}</span>`), entry.id);
    const adjacent = [...profile.match(/<nav class="profile-pagination"[^>]*>(.*?)<\/nav>/s)[1].matchAll(/href="([^"]+)"/g)].map(link => link[1]);
    const previous = index ? [`${settingIds[index - 1]}.html`] : [];
    const next = index + 1 < catalog.length ? `${settingIds[index + 1]}.html` : '../index.html';
    assert.deepEqual(adjacent, [...previous, next], entry.id);
  }
  return {single_objective_settings: singleCount, profile_links_checked: catalog.length};
});
run('homepage_keeps_search_and_count_without_retired_controls', () => {
  const markup = page.split('<script id="atlas-search-data"')[0];
  const script = read('visualization/dist/assets/atlas.js');
  assert(markup.includes('<h2>Explore the atlas</h2>'));
  assert(markup.includes('id="search"'));
  assert(markup.includes('id="results-label"'));
  for (const id of ['search-mode', 'search-mode-note', 'search-interpretation', 'example-convex-zeroth', 'example-count', 'result-count']) {
    assert(!markup.includes(`id="${id}"`), id);
    assert(!script.includes(`getElementById('${id}')`), id);
  }
  assert(!metadata.exampleFacetIds);
  for (const text of ['Explore settings through their mathematical specification', 'SETTING LIBRARY', 'Original source order', 'ORDERED AS IN THE SOURCE ATLAS']) {
    assert(!markup.includes(text), text);
  }
});
for (const fixture of dataAudit.semantic_fixtures.checks) {
  if (fixture.setting_id && fixture.query && typeof fixture.expected_match === 'boolean') {
    run(`evidence_fixture:${fixture.setting_id}`, () => {
      assert.equal(ids(state(fixture.query)).includes(fixture.setting_id), fixture.expected_match);
    });
  } else if (fixture.alias_query && fixture.expected_option_ids) {
    run(`semantic_alias:${fixture.alias_query}`, () => {
      assert.deepEqual(engine.parseQuery(fixture.alias_query).concepts.sort(), [...fixture.expected_option_ids].sort());
    });
  }
}
for (const query of ['Zeroth-order Exact Convex', 'Zeroth-order · Exact · Convex', '"zeroth-order" "exact" "convex"']) {
  run(`three_concepts:${query}`, () => { assert.deepEqual(ids(state([], query)), exampleIds); });
}
run('manual_same_group_OR', () => {
  assert.deepEqual(ids(state([convex, notAssumed])), [...new Set([...ids(state([convex])), ...ids(state([notAssumed]))])].sort());
});
run('query_AND_manual_strong_convexity', () => {
  assert.deepEqual(ids(state([strong], 'convex')), ids(state([strong])));
});
run('longest_phrase_and_negation_boundaries', () => {
  assert.deepEqual(engine.parseQuery('strongly convex').concepts, [strong]);
  for (const query of ['nonconvex', 'non-convex', 'not strongly convex']) assert(!engine.parseQuery(query).concepts.includes(convex));
  for (const query of ['inexact', 'not exact']) assert(!engine.parseQuery(query).concepts.includes(exact));
});
run('counts_use_other_groups_and_distinct_settings', () => {
  const key = globalThis.AtlasBrowseEngine.groupKey('common', 'MODEL', 'objective_convexity');
  const started = performance.now();
  const counts = engine.facetCounts(state(exampleFacetIds.filter(id => id !== convex)), new Set([key]));
  assert.equal(counts.get(key).get(convex), exampleIds.length);
  return {matching_settings: counts.get(key).get(convex), duration_ms: Number((performance.now() - started).toFixed(2))};
});
run('common_parent_UI_entries_are_not_duplicated_in_advanced', () => {
  for (const id of metadata.presentationPolicy.coarseAdvancedChoicesHidden) {
    assert(!page.includes(`name="tag" value="${id}"`), id);
  }
  assert(!page.includes('taxonomy-value-count'));
  assert(!/<details[^>]*id="advanced-filters"[^>]*\bopen\b/.test(page));
  assert(!/<details[^>]*id="more-filters"[^>]*\bopen\b/.test(page));
});
run('full_text_mode_does_not_assert_concepts', () => {
  assert.deepEqual(engine.parseQuery('convex exact', 'fulltext').concepts, []);
});

// A synthetic profile with incompatible views checks the semantics that a
// union of all tags on a profile cannot check, without relying on any title.
const fixtureMetadata = {commonAxes: [
  {id: 'MODEL', groups: [{label: 'Model', options: [
    {id: 'm:c', axis: 'MODEL', group: 'convexity', label: 'Convex', aliases: ['convex']},
    {id: 'm:n', axis: 'MODEL', group: 'convexity', label: 'Nonconvex', aliases: ['nonconvex']},
  ]}]},
  {id: 'ORACLE', groups: [{label: 'Order', options: [
    {id: 'o:z', axis: 'ORACLE', group: 'order', label: 'Zeroth-order', aliases: ['zeroth order']},
    {id: 'o:f', axis: 'ORACLE', group: 'order', label: 'First-order', aliases: ['first order']},
  ]}]},
], preciseTags: [
  {id: 'A:r:zero', axis: 'A', group: 'restriction', label: 'Zero respecting'},
  {id: 'A:r:free', axis: 'A', group: 'restriction', label: 'Unrestricted'},
], statuses: [{id: 'optimal', label: 'Optimal'}, {id: 'polynomial_gap', label: 'Polynomial gap'}]};
const fixtureEngine = globalThis.AtlasBrowseEngine.createEngine([{
  id: 'scope_fixture', search: 'sample text',
  viewTagSets: {restricted: ['A:r:zero'], free: ['A:r:free']},
  viewStatusCodes: {restricted: ['polynomial_gap'], free: ['optimal']},
  commonViewFacets: {restricted: ['m:c', 'o:z'], free: ['m:n', 'o:f']},
}], fixtureMetadata);
const fixtureState = (common = [], advanced = [], query = '', statuses = []) => fixtureEngine.makeState({common, advanced, statuses}, fixtureEngine.parseQuery(query));
run('all_common_advanced_and_status_conditions_share_one_view', () => {
  assert.equal(fixtureEngine.results(fixtureState(['m:n', 'o:z'])).length, 0);
  assert.equal(fixtureEngine.results(fixtureState(['o:z'], ['A:r:free'])).length, 0);
  assert.equal(fixtureEngine.results(fixtureState(['o:z'], [], '', ['optimal'])).length, 0);
  assert.equal(fixtureEngine.results(fixtureState([], ['A:r:zero', 'A:r:free'])).length, 1);
  const restriction = fixtureState(['o:z']);
  assert.deepEqual(fixtureEngine.matchingViews(fixtureEngine.results(restriction)[0], restriction), ['restricted']);
});
run('minimum_removals_and_restored_counts_are_actionable', () => {
  for (const s of [fixtureState(['m:n', 'o:z']), fixtureState([], [], 'unfindable!')]) {
    const diagnostic = fixtureEngine.diagnose(s);
    assert.equal(diagnostic.minimum, 1);
    assert(diagnostic.suggestions.length > 0);
    for (const suggestion of diagnostic.suggestions) {
      assert.equal(suggestion.keys.length, 1);
      assert.equal(suggestion.restored, 1);
      assert.equal(fixtureEngine.results(fixtureEngine.stateAfterRemoval(s, new Set(suggestion.keys))).length, suggestion.restored);
    }
  }
});
run('minimum_two_removals_are_distinguished_from_one', () => {
  const oneView = globalThis.AtlasBrowseEngine.createEngine([{
    id: 'two_removals', search: 'sample', viewTagSets: {main: []}, viewStatusCodes: {main: []},
    commonViewFacets: {main: ['m:c', 'o:z']},
  }], fixtureMetadata);
  const s = oneView.makeState({common: ['m:n', 'o:f']}, oneView.parseQuery(''));
  const diagnostic = oneView.diagnose(s);
  assert.equal(diagnostic.minimum, 2);
  assert.equal(diagnostic.suggestions[0].keys.length, 2);
  assert.equal(diagnostic.suggestions[0].restored, 1);
});
const report = {passed: checks.every(check => check.passed), source: 'built local HTML + Toolkit human tag sidecars + audited navigation additions + evidence fixtures + independent scope fixtures',
  profile_count: records.length, view_count: engine.records.reduce((n, record) => n + record.views.length, 0),
  common_option_count: engine.options.size, example_match_count: exampleIds.length, checks};
if (reportPath) fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({passed: report.passed, checks: checks.length, example_match_count: exampleIds.length, report: reportPath}));
if (!report.passed) { console.error(JSON.stringify(checks.filter(check => !check.passed), null, 2)); process.exitCode = 1; }
