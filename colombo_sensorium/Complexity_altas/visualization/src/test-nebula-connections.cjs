/* Task memberships define clouds, never connection rails or bundle hits. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const sandbox = {window: {}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, 'nebula_bundles.js'), 'utf8'), sandbox);
const {create} = sandbox.window.AtlasNebulaBundles;
const concepts = {
  task: {id: 'task', label: 'Optimization', group: 'TASK:problem'},
  oracle: {id: 'oracle', label: 'Exact gradients', group: 'ORACLE:access'},
  model: {id: 'model', label: 'Convex', group: 'MODEL:convexity'},
};
const points = [
  {id: 'a', task: 'first', labels: ['task', 'oracle', 'model'], xyz: [0, 0, 0]},
  {id: 'b', task: 'first', labels: ['task', 'oracle'], xyz: [1, 0, 0]},
  {id: 'c', task: 'second', labels: ['task', 'oracle', 'model'], xyz: [0, 1, 0]},
  {id: 'd', task: 'first', labels: ['task'], xyz: [0, 0, 1]},
];
const traces = {ORACLE: {color: '#f277c6', dash: [5, 3]}, MODEL: {color: '#b3e35c', dash: [2, 3]}};
const bundles = create({concepts}, points, traces);
const ids = values => Array.from(values).sort();

assert.equal(bundles.get('task'), undefined);
assert.deepEqual(ids(bundles.visibleLabels(['TASK'])), []);
assert.equal(bundles.summary(['TASK']).memberships, 0);
assert.deepEqual(ids(bundles.visibleLabels(['TASK', 'ORACLE', 'MODEL']).map(label => label.id)), ['model', 'oracle']);
assert.deepEqual(ids(bundles.members('oracle')), ['a', 'b', 'c']);
assert.deepEqual(ids(bundles.members('oracle', 'first')), ['a', 'b']);
assert.deepEqual(ids(bundles.members('oracle', 'second')), ['c']);
assert.deepEqual(ids(bundles.members('model')), ['a', 'c']);
assert.equal(bundles.summary(['ORACLE', 'MODEL']).memberships, 5);
assert.equal(bundles.summary(['ORACLE', 'MODEL']).bundles, 4);
assert.equal(bundles.frameAnchors.length, 4);

// A stale caller that still asks for TASK must create neither a rail nor a hit.
const labels = [];
const ctx = new Proxy({measureText: text => ({width: text.length * 6}),
  fillText: text => labels.push(text)}, {get: (target, key) => target[key] || (() => {})});
const project = xyz => ({x: 400 + xyz[0] * 60, y: 250 + xyz[1] * 60, z: xyz[2], depth: 1});
const projected = new Map(points.map(point => [point.id, project(point.xyz)]));
const boxes = bundles.paint(ctx, {w: 800, h: 500, project, projected,
  axes: ['TASK', 'ORACLE', 'MODEL'], focus: null, hover: null, matching: null});
assert.deepEqual(labels.sort(), ['Model', 'Oracle']);
assert.equal(boxes.length, 2);

// Every retained real-data membership is still represented exactly once.
const root = path.resolve(__dirname, '../..');
const overview = JSON.parse(fs.readFileSync(path.join(root, 'data/derived/atlas_overview.json'), 'utf8'));
const layout = JSON.parse(fs.readFileSync(path.join(root, 'data/derived/atlas_nebula.json'), 'utf8'));
const actual = overview.points.map(point => ({...point, labels: Object.keys(point.memberships), xyz: layout.positions[point.id]}));
const real = create(overview, actual, traces);
let memberships = 0, expectedBundles = 0, sameTaskGroups = 0;
const primaryTasks = [...new Set(actual.map(point => point.task))];
for (const concept of Object.values(overview.concepts)) {
  const axis = concept.group.split(':')[0];
  const expected = actual.filter(point => point.labels.includes(concept.id)).map(point => point.id);
  if (axis === 'TASK') {
    assert.equal(real.get(concept.id), undefined);
  } else if (axis === 'ORACLE' || axis === 'MODEL') {
    assert.deepEqual(ids(real.members(concept.id)), ids(expected));
    memberships += expected.length;
    // Regrouping settings must retain their actual Oracle/Model connections
    // inside each primary task, rather than dropping all same-task peers.
    for (const task of primaryTasks) {
      const taskMembers = actual.filter(point => point.task === task && point.labels.includes(concept.id))
        .map(point => point.id);
      assert.deepEqual(ids(real.members(concept.id, task)), ids(taskMembers), concept.id + ' / ' + task);
      if (taskMembers.length) expectedBundles++;
      if (taskMembers.length > 1) sameTaskGroups++;
    }
  }
}
assert.equal(real.summary(['TASK', 'ORACLE', 'MODEL']).memberships, memberships);
assert.equal(real.summary(['ORACLE', 'MODEL']).bundles, expectedBundles);
assert(sameTaskGroups > 0, 'The real Atlas must exercise retained same-task Oracle/Model groups.');
console.log(JSON.stringify({passed: true, connected_axes: ['ORACLE', 'MODEL'], retained_memberships: memberships,
  task_grouped_bundles: expectedBundles, same_task_connected_groups: sameTaskGroups}));
