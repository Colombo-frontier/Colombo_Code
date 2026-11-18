"""Bounded, reproducible discovery neighborhoods; never an identity classifier.

The catalog is a retrieval projection. Missing tags remain eligible for review,
and the selected neighborhood does not limit later Atlas-wide identity search.
"""
from __future__ import annotations

from collections import Counter
from typing import Any

from ..atlas.tags import expand_concepts


def _strings(value: Any) -> list[str]:
    return list(dict.fromkeys(x for x in value if isinstance(x, str) and x)) if isinstance(value, list) else []


def _positive_limit(request: dict, name: str, default: int) -> int:
    value = request.get(name, default)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _known_concepts(row: dict) -> set[str]:
    return {
        fact["concept_id"] for fact in row.get("tag_facts", [])
        if isinstance(fact, dict) and fact.get("status") == "known"
        and isinstance(fact.get("concept_id"), str)
    }


def _tasks(row: dict) -> tuple[set[str], bool]:
    """Use declared family IDs, without guessing categories from titles."""
    values: set[str] = set()
    family_declared = False
    for fact in row.get("tag_facts", []):
        if not isinstance(fact, dict) or fact.get("status") != "known":
            continue
        cid = fact.get("concept_id", "")
        if not isinstance(cid, str):
            continue
        parts = cid.split(":")
        if len(parts) == 3 and parts[0] == "TASK" and parts[1] in {"family", "task_family"}:
            values.add(parts[2])
            family_declared = True
    domain = row.get("primary_domain")
    if isinstance(domain, str) and domain:
        values.add(domain)
    values.update(_strings(row.get("task_ids", [])))
    uncertain = bool(row.get("diagnostics")) or "TASK" in row.get("unknown_axes", []) or not family_declared
    return values, uncertain


def _historical_use(history: list[dict] | None) -> Counter:
    """Count prior selections once per round; histories contain no model notes."""
    use: Counter = Counter()
    for record in history or []:
        if not isinstance(record, dict):
            continue
        ids = set(_strings(record.get("seed_setting_ids", [])))
        for seed in record.get("seeds", []):
            if isinstance(seed, str):
                ids.add(seed)
            elif isinstance(seed, dict) and isinstance(seed.get("setting_id"), str):
                ids.add(seed["setting_id"])
        for opportunity in record.get("opportunities", []):
            if isinstance(opportunity, dict):
                ids.update(_strings(opportunity.get("seed_setting_ids", [])))
        use.update(ids)
    return use


def _concept_summary(concepts: set[str], limit: int) -> list[str]:
    # Task/model/oracle give the planner structural context. Complete declarations
    # remain available through atlas_read; truncation never means absence.
    axis_rank = {"TASK": 0, "ORACLE": 1, "MODEL": 2}
    return sorted(concepts, key=lambda c: (axis_rank.get(c.split(":", 1)[0], 3), c))[:limit]


def _brief(row: dict, *, seed: bool = False) -> dict:
    concepts = _known_concepts(row)
    tasks, uncertain = _tasks(row)
    shown = _concept_summary(concepts, 20 if seed else 10)
    output = {
        "setting_id": row["setting_id"],
        "title": str(row.get("title", row["setting_id"]))[:300],
        "version": row.get("profile_version", row.get("version")),
        "task_ids": sorted(tasks),
        "task_scope_uncertain": uncertain,
        "concepts": shown,
        "concept_count": len(concepts),
        "concepts_truncated": len(shown) < len(concepts),
        "unknown_axes": list(dict.fromkeys(_strings(row.get("unknown_axes", [])))),
    }
    if seed:
        output["task_summary"] = str(row.get("task_text", ""))[:700]
        output["view_ids"] = _strings(row.get("view_ids", []))
    return output


def build_neighborhood(atlas, request: dict, history: list[dict] | None = None) -> dict:
    """Return a compact discovery portfolio, preserving unknown scope candidates.

    Explicit seeds restrict the seed pool. Source task IDs constrain seeds only;
    target-task settings can still appear as analogues. ``fixed_constraints``
    and free-text scope are scientific instructions for the planner/reviewer,
    not interpreted as keyword filters here. Priority modes likewise remain
    LLM instructions rather than assertions derived from stored gap labels.
    """
    max_seeds = _positive_limit(request, "max_seeds", 8)
    max_neighbors = _positive_limit(request, "max_neighbors_per_seed", 6)
    start_version = atlas.version()
    catalog = atlas.catalog()
    vocabulary = atlas.vocabulary()
    rows = {row["setting_id"]: row for row in catalog if isinstance(row, dict) and isinstance(row.get("setting_id"), str)}
    explicit = _strings(request.get("seed_setting_ids", []))
    missing = [sid for sid in explicit if sid not in rows]
    if missing:
        raise ValueError("Requested seed settings are absent from the current Atlas: " + ", ".join(missing))
    source_tasks = set(_strings(request.get("source_task_ids", [])))
    target_tasks = set(_strings(request.get("target_task_ids", [])))
    use = _historical_use(history)
    tasks = {sid: _tasks(row) for sid, row in rows.items()}
    concepts = {sid: _known_concepts(row) for sid, row in rows.items()}
    expanded = {sid: expand_concepts(values, vocabulary) for sid, values in concepts.items()}
    eligible: list[str] = []
    matched: list[str] = []
    unknown: list[str] = []
    outside: list[str] = []
    for sid in explicit or sorted(rows):
        declared, uncertain = tasks[sid]
        if not source_tasks or declared & source_tasks:
            eligible.append(sid)
            matched.append(sid)
        elif uncertain:
            eligible.append(sid)
            unknown.append(sid)
        else:
            outside.append(sid)

    # Rotate previously explored seeds, then spread choices over declared task
    # and oracle categories. This is scheduling, not scientific value scoring.
    selected: list[str] = []
    task_use: Counter = Counter()
    oracle_use: Counter = Counter()
    explicit_order = {sid: i for i, sid in enumerate(explicit)}
    remaining = list(eligible)
    while remaining and len(selected) < max_seeds:
        def key(sid):
            task_keys = tasks[sid][0] or {"__unknown__"}
            oracle_keys = {c for c in concepts[sid] if c.startswith("ORACLE:")} or {"__unknown__"}
            return (
                use[sid], min(task_use[t] for t in task_keys),
                min(oracle_use[o] for o in oracle_keys),
                explicit_order.get(sid, len(explicit)), sid,
            )
        chosen = min(remaining, key=key)
        remaining.remove(chosen)
        selected.append(chosen)
        task_use.update(tasks[chosen][0] or {"__unknown__"})
        oracle_use.update({c for c in concepts[chosen] if c.startswith("ORACLE:")} or {"__unknown__"})

    seeds = []
    for sid in selected:
        scores = []
        for other in rows:
            if other == sid:
                continue
            overlap = concepts[sid] & concepts[other]
            parents = (expanded[sid] & expanded[other]) - overlap
            task_overlap = tasks[sid][0] & tasks[other][0]
            target_overlap = target_tasks & tasks[other][0]
            value = sum(3 if c.startswith(("TASK:", "ORACLE:", "MODEL:")) else 1 for c in overlap)
            value += min(len(parents), 6) + 2 * bool(task_overlap) + 3 * bool(target_overlap)
            # Unknowns are retained in the ranked pool, without claiming a
            # positive mathematical relationship from absent information.
            scores.append((other, value, overlap, parents, target_overlap))
        scores.sort(key=lambda item: (-item[1], use[item[0]], item[0]))
        neighbor_rows = []
        for other, value, overlap, parents, target_overlap in scores[:max_neighbors]:
            brief = _brief(rows[other])
            brief.update({
                "retrieval_score": value,
                "signals": {
                    "shared_declared_concepts": sorted(overlap)[:10],
                    "shared_declared_parents": sorted(parents)[:6],
                    "target_task_analogue": bool(target_overlap),
                    "unknown_retained": tasks[other][1] or bool(rows[other].get("unknown_axes")),
                },
                "relation_status": "unverified_navigation_only",
            })
            neighbor_rows.append(brief)
        brief = _brief(rows[sid], seed=True)
        brief.update({
            "seed_scope": "unknown_requires_review" if sid in unknown else "declared_match",
            "prior_round_count": use[sid],
            "neighbors": neighbor_rows,
        })
        seeds.append(brief)
    if atlas.version() != start_version:
        raise ValueError("Atlas changed while the discovery neighborhood was being assembled; rebuild the snapshot")
    return {
        "inventory_version": start_version,
        "seeds": seeds,
        "available_task_ids": sorted(set().union(*(t[0] for t in tasks.values())) if tasks else set()),
        "coverage": {
            "catalog_count": len(rows), "eligible_seed_count": len(eligible),
            "declared_scope_matches": len(matched), "unknown_scope_retained": len(unknown),
            "known_outside_source_scope": len(outside),
            "selected_seed_count": len(seeds), "deferred_seed_count": len(remaining),
            "explicit_seed_scope_conflicts": outside if explicit else [],
            "unknown_scope_selected": sum(sid in unknown for sid in selected),
            "selection_policy": "Prior-round rotation, task/oracle diversity, then stable ID; LLM judges research value.",
            "scope_interpretation": "Task tags and declared source IDs screen seeds only; fixed constraints and free-text scope require Agent review.",
            "identity_search_scope": "entire_current_atlas",
            "seed_pool_fully_selected": not remaining,
            "discovery_complete": False,
            "notice": "A bounded discovery sample is not an exhaustive mathematical neighborhood. Navigation overlap does not establish equivalence, containment, or transferable bounds.",
        },
    }
