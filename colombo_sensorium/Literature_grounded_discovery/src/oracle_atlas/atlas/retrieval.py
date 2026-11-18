"""High-recall preliminary screening: rank only, without declaring setting novelty from tags or top-k results."""
from __future__ import annotations

import math
import re
from typing import Any

from .tags import AXES, EXACT_CONCEPTS, HUMAN_GROUP_ALIASES, expand_concepts, match_interface, vocabulary_index

STOP_WORDS = {"the", "and", "for", "with", "from", "setting", "optimization", "problem", "of", "a", "an", "in", "to", "or", "on", "is", "by", "using", "this", "that"}


def _tokens(value: Any) -> set[str]:
    if isinstance(value, list):
        value = " ".join(str(x) for x in value)
    return {word for word in re.findall(r"[a-z0-9_]+|[\u3400-\u9fff]{2,}", str(value).casefold()) if len(word) > 1 and word not in STOP_WORDS}


def _canonical_concept(concept: str) -> str:
    """Map registered human group aliases back to machine groups; do not infer parent relationships."""
    for machine, human in HUMAN_GROUP_ALIASES.items():
        if concept.startswith(human + ":") and concept.count(":") == 2:
            return machine + concept[len(human):]
    return concept


def retrieve(atlas, candidate: dict, limit: int = 12, offset: int = 0, broaden: bool = False) -> dict:
    """Rank the multichannel union; pagination ultimately includes every catalog entry.

    Even known differing tags only lower ranking; Agents must judge equivalence transformations across formulations.
    ``broaden`` further promotes candidates with unknown/legacy indexes so the matcher can inspect blind spots in initial retrieval.
    """
    if not isinstance(limit, int) or not 1 <= limit <= 100 or not isinstance(offset, int) or offset < 0:
        raise ValueError("limit must be 1-100 and offset must be a nonnegative integer")
    catalog, vocabulary = atlas.catalog(), atlas.vocabulary()
    facts = candidate.get("tag_facts", [])
    wanted = {_canonical_concept(row["concept_id"]) for row in facts if isinstance(row, dict) and isinstance(row.get("concept_id"), str) and row.get("status") == "known"}
    expanded = expand_concepts(wanted, vocabulary)
    text = " ".join(str(candidate.get(key, "")) for key in ("title", "candidate_id", "setting_id", "formulation", "keywords"))
    task = candidate.get("common_specification", {}).get("task", {})
    if isinstance(task, dict):
        text += " " + " ".join(str(task.get(key, "")) for key in ("summary", "formulation", "formulation_code", "solution_goal"))
    terms = _tokens(text)
    ids = {value for value in (candidate.get("setting_id"), candidate.get("candidate_id")) if isinstance(value, str)}
    ids.update(x for x in candidate.get("aliases", []) if isinstance(x, str))
    documents = [_tokens(" ".join((entry["setting_id"], entry.get("title", ""), entry.get("task_text", ""), " ".join(entry.get("aliases", []))))) for entry in catalog]
    document_frequency = {term: sum(term in words for words in documents) for term in terms}
    ranked = []
    unknown_count = 0
    for entry, words in zip(catalog, documents):
        signals = []
        score = 0.0
        search_facts = entry["tag_facts"] + entry.get("navigation_facts", [])
        direct = {_canonical_concept(f["concept_id"]) for f in search_facts if f.get("status") == "known"}
        weak = {_canonical_concept(f["concept_id"]) for f in entry["tag_facts"] if isinstance(f.get("concept_id"), str)}
        direct_overlap = sorted(wanted & direct)
        parent_overlap = sorted((expanded & expand_concepts(direct, vocabulary)) - set(direct_overlap))
        weak_overlap = sorted(wanted & (weak - direct))
        if direct_overlap:
            score += sum(6.0 if cid.startswith(("TASK:", "ORACLE:")) else 3.0 for cid in direct_overlap)
            signals.append({"channel": "scoped_concepts", "concept_ids": direct_overlap[:16]})
        if parent_overlap:
            score += min(8, len(parent_overlap)) * 1.5
            signals.append({"channel": "declared_parents", "concept_ids": parent_overlap[:12]})
        if weak_overlap:
            score += min(6, len(weak_overlap))
            signals.append({"channel": "legacy_or_unknown", "concept_ids": weak_overlap[:8]})
        matched_terms = sorted(terms & words)
        if matched_terms:
            score += sum(1 + math.log((len(catalog) + 1) / (document_frequency[t] + 1)) for t in matched_terms)
            signals.append({"channel": "title_formulation", "terms": matched_terms[:12]})
        if ids & ({entry["setting_id"]} | set(entry.get("aliases", []))):
            score += 100
            signals.append({"channel": "stable_id_or_alias"})
        unknown = bool(entry.get("unknown_axes")) or not direct or bool(entry.get("diagnostics"))
        if unknown:
            unknown_count += 1
            if broaden:
                score += 3
            signals.append({"channel": "unknown_retained", "axes": entry.get("unknown_axes", [])})
        ranked.append({"setting_id": entry["setting_id"], "title": entry["title"], "profile_version": entry["profile_version"], "score": round(score, 5), "signals": signals, "unknown_axes": entry.get("unknown_axes", []), "view_ids": entry.get("view_ids", []), "diagnostics": entry.get("diagnostics", []), "identity_state": "unexamined"})
    ranked.sort(key=lambda row: (-row["score"], row["setting_id"]))
    return {"candidates": ranked[offset:offset + limit], "has_more": offset + limit < len(ranked), "total": len(ranked), "offset": offset, "next_offset": offset + limit if offset + limit < len(ranked) else None, "unknown_count": unknown_count, "query": {"concept_ids": sorted(wanted), "terms": sorted(terms), "broaden": broaden, "hard_exclusions": 0, "channels": ["stable_id_or_alias", "scoped_concepts", "declared_parents", "title_formulation", "legacy_or_unknown", "unknown_retained"]}, "inventory_version": atlas.version(), "notice": "Ranking is candidate screening. No top-k cutoff, score, or empty tag match proves a new setting."}


def resolve_labels(labels: list[str], vocabulary: dict | None = None) -> dict:
    """Human tag entry point: report ambiguity explicitly rather than silently merging similar display text."""
    index = vocabulary_index(vocabulary)
    resolved, ambiguous, unknown = [], {}, []
    for label in labels:
        if label in index or re.fullmatch(r"[A-Z]+:[a-z_]+:[a-z0-9_]+", label):
            resolved.append(_canonical_concept(label))
            continue
        hits = set()
        for cid, row in index.items():
            names = [row.get("label", ""), *row.get("aliases", [])]
            if label.casefold() in {str(name).casefold() for name in names}:
                hits.add(_canonical_concept(cid))
        if len(hits) == 1:
            resolved.extend(hits)
        elif hits:
            ambiguous[label] = sorted(hits)
        else:
            unknown.append(label)
    return {"concept_ids": sorted(set(resolved)), "ambiguous": ambiguous, "unknown": unknown}


def match_tag_filters(profile: dict, facts: list[dict], filters: list[dict], vocabulary: dict | None = None) -> dict:
    """Combine constraints with AND within the same view, returning matched/conflict/unknown; this is not an identity decision.

    Express a single-operation constraint explicitly with ``{"interface": {...}, "mode": "native|supplies"}``
    to avoid combining Exact from one operation with feedback from another.
    """
    view_results = []
    for view in profile.get("views", []):
        vid = view["view_id"]
        outcomes = []
        for wanted in filters:
            if "interface" in wanted:
                query = dict(wanted["interface"], view_ref=vid)
                outcomes.append(match_interface(profile, query, wanted.get("mode", "native")))
                continue
            cid = _canonical_concept(wanted["concept_id"])
            if cid in EXACT_CONCEPTS and not wanted.get("operation_ref"):
                outcomes.append(match_interface(profile, {"view_ref": vid, "precision": "exact"}))
                continue
            if cid in EXACT_CONCEPTS and wanted.get("operation_ref"):
                outcomes.append(match_interface(profile, {"view_ref": vid, "operation_ref": wanted["operation_ref"], "object_ref": wanted.get("object_ref"), "precision": "exact"}))
                continue
            candidates = []
            for fact in facts:
                if fact.get("view_ref") not in (None, vid):
                    continue
                for key in ("operation_ref", "object_ref"):
                    if wanted.get(key) is not None and fact.get(key) != wanted[key]:
                        break
                else:
                    if cid in expand_concepts({_canonical_concept(fact["concept_id"])}, vocabulary):
                        candidates.append(fact)
            state = "matched" if any(x.get("status") == "known" for x in candidates) else "unknown"
            # A missing tag indicates only unknown; the set makes no closed-world commitment, so conflict cannot be concluded.
            outcomes.append({"state": state, "concept_id": cid})
        state = "conflict" if any(x["state"] == "conflict" for x in outcomes) else ("unknown" if any(x["state"] == "unknown" for x in outcomes) else "matched")
        view_results.append({"view_id": vid, "state": state, "conditions": outcomes})
    state = "matched" if any(x["state"] == "matched" for x in view_results) else ("unknown" if not view_results or any(x["state"] == "unknown" for x in view_results) else "conflict")
    return {"state": state, "views": view_results, "identity_decision": "requires_llm_reasoning"}


def scope_search(atlas, filters: list[dict], include_unknown: bool = True, limit: int = 50, offset: int = 0) -> dict:
    """Provide the same three-valued results for visualization/machine scopes; display unknown separately by default rather than discarding it."""
    if not 1 <= limit <= 100 or offset < 0:
        raise ValueError("Invalid pagination arguments")
    matches, unknown, excluded = [], [], 0
    vocabulary = atlas.vocabulary()
    for entry in atlas.catalog():
        if entry.get("diagnostics") and not entry.get("tag_facts"):
            verdict = {"state": "unknown", "views": [], "diagnostics": entry["diagnostics"]}
        else:
            verdict = match_tag_filters(atlas.read(entry["setting_id"]), entry["tag_facts"] + entry.get("navigation_facts", []), filters, vocabulary)
        row = {"setting_id": entry["setting_id"], "title": entry["title"], **verdict}
        if verdict["state"] == "matched":
            matches.append(row)
        elif verdict["state"] == "unknown":
            unknown.append(row)
        else:
            excluded += 1
    items = matches + (unknown if include_unknown else [])
    return {"items": items[offset:offset + limit], "matched_count": len(matches), "unknown_count": len(unknown), "conflict_count": excluded, "total": len(items), "has_more": offset + limit < len(items), "inventory_version": atlas.version()}
