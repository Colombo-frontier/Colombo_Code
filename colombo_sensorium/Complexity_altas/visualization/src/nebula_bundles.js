/* Represent Oracle and Model memberships, grouped by label and primary task. */
(() => {
  'use strict';
  const key = (label, task) => label + '|' + (task || '');
  // Offset rails run in two perpendicular world directions. The offsets
  // keep label nodes outside the main cloud in the initial camera view.
  const rails = {
    ORACLE: {from: [2.63, .17, -2.32], to: [2.63, .17, 2.12], inward: [-1, -.08, 0]},
    MODEL: {from: [-2.46, -1.54, .84], to: [2.19, -1.54, .84], inward: [0, 1, -.12]},
  };
  const frameAnchors = Object.values(rails).flatMap(({from, to}) => [from, to]);
  const mix = (a, b, t) => a.map((x, i) => x + (b[i] - x) * t);
  const bounds = points => ({
    left: Math.min(...points.map(p => p.x)), right: Math.max(...points.map(p => p.x)),
    top: Math.min(...points.map(p => p.y)), bottom: Math.max(...points.map(p => p.y)),
  });
  const opacityAt = depth => Math.max(.58, Math.min(1.16, .87 + .14 * depth));
  function create(overview, points, traces) {
    const all = new Map(Object.values(overview.concepts).filter(c => c.group.split(':')[0] in rails).map(c => [c.id, {
      id: c.id, label: c.label, axis: c.group.split(':')[0], tasks: new Map(), members: [],
    }]));
    for (const p of points) {
      for (const id of p.labels) {
        const label = all.get(id);
        if (!label) continue;
        if (!label.tasks.has(p.task)) label.tasks.set(p.task, {task: p.task, members: [], center: [0, 0, 0]});
        const b = label.tasks.get(p.task);
        b.members.push(p.id); label.members.push(p.id);
        p.xyz.forEach((x, i) => { b.center[i] += x; });
      }
    }
    for (const [id, label] of all) {
      if (!label.members.length) { all.delete(id); continue; }
      for (const b of label.tasks.values()) b.center = b.center.map(x => x / b.members.length);
    }
    const ordered = [...all.values()].sort((a, b) => a.label.localeCompare(b.label) || a.id.localeCompare(b.id));
    const visibleLabels = axes => ordered.filter(label => axes.includes(label.axis));
    const summary = axes => visibleLabels(axes).reduce((s, label) => ({
      labels: s.labels + 1, bundles: s.bundles + label.tasks.size, memberships: s.memberships + label.members.length,
    }), {labels: 0, bundles: 0, memberships: 0});
    const members = (id, task) => task ? all.get(id)?.tasks.get(task)?.members || [] : all.get(id)?.members || [];
    let hits = [];

    function spatialPath(a, b, axis, project) {
      const push = Math.min(1.42, Math.hypot(...b.map((v, i) => v - a[i])) * .49);
      const c1 = a.map((v, i) => v + rails[axis].inward[i] * push);
      const c2 = mix(b, a, .27);
      return Array.from({length: 19}, (_, i) => {
        const t = i / 18, s = 1 - t;
        return project(a.map((v, k) => s*s*s*v + 3*s*s*t*c1[k] + 3*s*t*t*c2[k] + t*t*t*b[k]));
      });
    }
    function tracePath(ctx, path) {
      ctx.beginPath(); ctx.moveTo(path[0].x, path[0].y);
      for (let i = 1; i < path.length; i++) ctx.lineTo(path[i].x, path[i].y);
    }
    function railLabels(ctx, lines, w, h) {
      const boxes = [];
      ctx.font = '700 10px system-ui, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      for (const line of lines) {
        const {axis, a, b} = line;
        const text = axis[0] + axis.slice(1).toLowerCase();
        const half = ctx.measureText(text).width / 2 + 6;
        const middle = {x: (a.x + b.x) / 2, y: (a.y + b.y) / 2};
        const dx = b.x - a.x, dy = b.y - a.y, length = Math.hypot(dx, dy);
        let nx = length > 5 ? -dy / length : 0, ny = length > 5 ? dx / length : -1;
        if (nx * (middle.x - w / 2) + ny * (middle.y - h / 2) < 0) { nx = -nx; ny = -ny; }
        // Place the upright label alongside its projected rail, choosing the
        // outer side first, then the other side if it would overlap a label.
        for (const side of [1, -1]) {
          const x = Math.max(half + 3, Math.min(w - half - 3, middle.x + nx * 15 * side));
          const y = Math.max(42, Math.min(h - 10, middle.y + ny * 15 * side));
          const box = {l: x - half, r: x + half, t: y - 8, b: y + 8};
          if (boxes.some(q => box.l < q.r && box.r > q.l && box.t < q.b && box.b > q.t)) continue;
          boxes.push(box);
          ctx.globalAlpha = .94; ctx.fillStyle = '#101c28';
          ctx.fillRect(box.l, box.t, 2 * half, 16);
          ctx.strokeStyle = traces[axis].color; ctx.globalAlpha = .63; ctx.lineWidth = .7;
          ctx.strokeRect(box.l + .5, box.t + .5, 2 * half - 1, 15);
          ctx.globalAlpha = 1; ctx.fillStyle = traces[axis].color; ctx.fillText(text, x, y);
          break;
        }
      }
      return boxes;
    }
    function paint(ctx, {w, h, project, projected, axes, focus, hover, matching, selected = null}) {
      hits = [];
      const star = projected.get(selected);
      const selectedLabels = new Set(star ? visibleLabels(axes).filter(label => label.members.includes(selected)).map(label => label.id) : []);
      if (star) { focus = null; hover = null; }
      const hubs = [], routes = [], railLines = [];
      ctx.save();
      ctx.lineCap = 'round';
      for (const axis of axes.filter(axis => axis in rails)) {
        const labels = visibleLabels([axis]);
        const rail = rails[axis], {color} = traces[axis];
        const a = project(rail.from), b = project(rail.to);
        railLines.push({axis, a, b});
        for (const [i, label] of labels.entries()) {
          const t = labels.length === 1 ? .5 : i / (labels.length - 1);
          const xyz = mix(rail.from, rail.to, .05 + .90 * t), at = project(xyz);
          const activeLabel = focus?.id === label.id;
          const hoverLabel = hover?.id === label.id;
          const radius = (2.1 + Math.min(2.4, Math.sqrt(label.members.length) * .14)) * Math.sqrt(at.depth);
          hubs.push({id: label.id, at, radius, color, bright: selectedLabels.has(label.id) || activeLabel || hoverLabel,
            muted: star ? !selectedLabels.has(label.id) : !!focus && !activeLabel});
          hits.push({id: label.id, point: at, count: label.members.length, radius, hub: true});
          for (const b of label.tasks.values()) {
            const expands = activeLabel && (!focus.task || b.task === focus.task);
            if (expands) continue;
            const count = b.members.length;
            const path = spatialPath(xyz, b.center, axis, project);
            const depth = path[Math.floor(path.length / 2)].z;
            const width = (.58 + Math.min(3.9, Math.sqrt(count) * .28)) * Math.sqrt(path[Math.floor(path.length / 2)].depth);
            const highlight = hoverLabel && (!hover.task || b.task === hover.task);
            const filtered = matching && !focus && !star ? b.members.filter(id => matching.has(id)).length : 0;
            routes.push({axis, path, depth, width, highlight, filtered, count});
            hits.push({id: label.id, task: b.task, count, path, width, bounds: bounds(path), depth});
          }
        }
      }
      for (const route of routes.sort((a, b) => a.depth - b.depth)) {
        const {color, dash} = traces[route.axis];
        const depthOpacity = opacityAt(route.depth);
        ctx.strokeStyle = color; ctx.setLineDash(dash); ctx.lineWidth = route.width;
        ctx.globalAlpha = (focus || star ? .07 : route.highlight ? .66 : matching ? .075 : .29) * depthOpacity;
        tracePath(ctx, route.path); ctx.stroke();
        if (route.filtered) {
          ctx.globalAlpha = route.highlight ? .76 : .42;
          ctx.lineWidth = route.width * Math.max(.3, Math.sqrt(route.filtered / route.count)); ctx.stroke();
        }
      }
      ctx.setLineDash([]);
      for (const {axis, a, b} of railLines) {
        ctx.strokeStyle = traces[axis].color; ctx.globalAlpha = .51; ctx.lineWidth = 1;
        tracePath(ctx, [a, b]); ctx.stroke();
      }
      if (focus) {
        const hub = hubs.find(hub => hub.id === focus.id);
        if (hub) {
          const {dash} = traces[all.get(focus.id).axis];
          ctx.strokeStyle = hub.color; ctx.lineWidth = .95; ctx.setLineDash(dash);
          const ids = members(focus.id, focus.task);
          for (const dimmed of [true, false]) {
            ctx.globalAlpha = dimmed ? .10 : .55;
            ctx.beginPath();
            for (const id of ids) {
              if (dimmed !== (!!matching && !matching.has(id))) continue;
              const star = projected.get(id);
              ctx.moveTo(hub.at.x, hub.at.y); ctx.lineTo(star.x, star.y);
            }
            ctx.stroke();
          }
        }
      }
      if (star) {
        for (const hub of hubs.filter(hub => selectedLabels.has(hub.id))) {
          const {dash} = traces[all.get(hub.id).axis];
          ctx.strokeStyle = hub.color; ctx.lineWidth = 1.8; ctx.globalAlpha = .94; ctx.setLineDash(dash);
          ctx.beginPath(); ctx.moveTo(hub.at.x, hub.at.y); ctx.lineTo(star.x, star.y); ctx.stroke();
        }
      }
      ctx.setLineDash([]);
      for (const hub of hubs.sort((a, b) => a.at.z - b.at.z)) {
        ctx.globalAlpha = hub.muted ? .40 : hub.bright ? 1 : .86 * opacityAt(hub.at.z);
        ctx.fillStyle = hub.color;
        const r = hub.radius + (hub.bright ? 1.6 : 0);
        ctx.beginPath(); ctx.moveTo(hub.at.x, hub.at.y - r);
        ctx.lineTo(hub.at.x + r, hub.at.y); ctx.lineTo(hub.at.x, hub.at.y + r);
        ctx.lineTo(hub.at.x - r, hub.at.y); ctx.closePath(); ctx.fill();
        if (hub.bright) {
          ctx.strokeStyle = '#eef8fc'; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.arc(hub.at.x, hub.at.y, hub.radius + 3.5, 0, Math.PI * 2); ctx.stroke();
        }
      }
      const labelBoxes = railLabels(ctx, railLines, w, h);
      ctx.restore();
      return labelBoxes;
    }
    const dist = (p, q) => Math.hypot(p.x - q.x, p.y - q.y);
    function segmentDistance(p, a, b) {
      const dx = b.x - a.x, dy = b.y - a.y;
      const d = dx*dx + dy*dy;
      const t = d ? Math.max(0, Math.min(1, ((p.x - a.x)*dx + (p.y - a.y)*dy)/d)) : 0;
      return Math.hypot(p.x - a.x - t*dx, p.y - a.y - t*dy);
    }
    function pick(pos) {
      let best = null, nearest = Infinity;
      for (const item of hits) {
        if (!item.hub) continue;
        const d = dist(pos, item.point);
        if (d <= Math.max(6, item.radius + 3) && (d < nearest || (d === nearest && item.point.z > best.point.z))) {
          nearest = d; best = item;
        }
      }
      if (best) return best;
      nearest = 5;
      for (const item of hits) {
        if (!item.path) continue;
        const {left, right, top, bottom} = item.bounds;
        if (pos.x < left - 5 || pos.x > right + 5 || pos.y < top - 5 || pos.y > bottom + 5) continue;
        for (let i = 1; i < item.path.length; i++) {
          const distance = segmentDistance(pos, item.path[i - 1], item.path[i]);
          if (distance < nearest || (distance === nearest && best && item.depth > best.depth)) {
            nearest = distance; best = {...item, point: pos};
          }
        }
      }
      return best;
    }
    return {visibleLabels, summary, get: id => all.get(id), members, paint, pick, key, frameAnchors};
  }
  window.AtlasNebulaBundles = {create};
})();
