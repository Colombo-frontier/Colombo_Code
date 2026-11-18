"""Source-bound navigation assertions and derived indices for the five native files."""
from copy import deepcopy

from .tags import (EXACT_CONCEPTS, TagError, at, digest, effective_specification,
                   expand_concepts, human_vocabulary_index, match_interface)


def regime_index(profile):
    rows = []
    for index, region in enumerate(profile.get("regimes", [])):
        pointer = "/regimes/" + str(index)
        rid = region.get("id", region.get("regime_id", region.get("region_id")))
        field = next((key for key in ("predicate", "predicate_text") if region.get(key) is not None), None)
        rows.append({"regime_id": rid, "source_pointer": pointer,
                     "predicate_pointer": pointer + "/" + field if field else None,
                     "evaluation_state": "unparsed"})
    return rows


def _used_projection(profile, view, pointer):
    if not pointer.startswith("/resource_projections/"):
        return True
    projection = at(profile, "/".join(pointer.split("/")[:3]))
    pid = projection.get("resource_projection_id", projection.get("id"))
    return any(c.get("comparison_key", c).get("resource_projection_id") == pid
               and c.get("comparison_key", c).get("view_id") == view for c in profile.get("comparisons", []))


def retained_navigation(old, profile, machine, vocabulary):
    """Replay previously source-reviewed coarse assertions only in their original view.

    The previous profile hash and vocabulary version bind the evidence. Recheck precise feature
    support and resolved source values against the new profile, including referenced cost projections.
    """
    human = old.get("human_tags.json", {})
    previous = old.get("profile.json", {})
    registered = human_vocabulary_index(vocabulary)
    if (not previous or not registered or human.get("profile_sha256") != digest(previous)
            or old.get("machine_tags.json", {}).get("profile_sha256") != human["profile_sha256"]
            or human.get("vocabulary_version") != (vocabulary or {}).get("human", {}).get("version")):
        return {}
    before = {v["view_id"]: v for v in previous["views"]}
    after = {v["view_id"]: v for v in profile["views"]}
    old_fids = {f["feature_id"]: f for f in old["machine_tags.json"].get("features", [])}
    exact = {r["view_id"] for r in match_interface(profile, {"precision":"exact"})["views"] if r["state"] == "matched"}
    old_specs, new_specs, result = {}, {}, {}
    for facet in human.get("facets", []):
        cid = facet.get("concept_id")
        if cid not in registered or facet.get("status", "known") != "known":
            continue
        for evidence in facet.get("evidence", []):
            vid = evidence.get("view_id")
            if vid not in before or vid not in after or vid not in facet.get("view_ids", []):
                continue
            if cid in EXACT_CONCEPTS and vid not in exact:
                continue
            if vid not in old_specs:
                old_specs[vid] = effective_specification(previous, vid)[0]
                new_specs[vid] = effective_specification(profile, vid)[0]
            axis = cid.split(":")[0].lower()
            view_field = "guarantees" if axis == "guarantee" else axis
            if before[vid].get(view_field) != after[vid].get(view_field) or old_specs[vid].get(axis) != new_specs[vid].get(axis):
                continue
            for assertion in evidence.get("assertions", []):
                pointers = assertion.get("source_pointers", [])
                refs = assertion.get("precise_tag_refs", [])
                if not pointers or not isinstance(refs, list) or not set(pointers).issubset(facet.get("source_pointers", [])):
                    continue
                try:
                    if any(at(previous, p) != at(profile, p) or not _used_projection(profile, vid, p)
                           or (p.startswith("/views/") and not _native_assertion_source(p, vid, profile)) for p in pointers):
                        continue
                except (TagError, TypeError, KeyError, IndexError):
                    continue
                # A per-view withdrawal supersedes a legacy assertion. A stale resolved source hash
                # or a feature missing from the current projection never re-establishes its known status.
                candidates = [f for f in machine["features"] if vid in f.get("view_ids", [])
                              and set(pointers).intersection(f.get("source_pointers", []))]
                if any(f.get("status") != "known" and f["concept_id"] in [cid, *refs] for f in candidates):
                    continue
                active = [f for f in candidates if f.get("status") == "known" and f["concept_id"] in refs]
                if set(refs) != {f["concept_id"] for f in active}:
                    continue
                old_active = {old_fids[fid]["concept_id"] for fid in facet.get("source_feature_ids", [])
                              if fid in old_fids and vid in old_fids[fid].get("view_ids", [])
                              and old_fids[fid].get("status", "known") == "known"}
                if not set(refs).issubset(old_active):
                    continue
                if not refs and not all(_native_assertion_source(p, vid, profile) for p in pointers):
                    continue
                key = (cid, vid)
                item = result.setdefault(key, {"source_pointers":set(), "source_feature_ids":set(), "assertions":[]})
                item["source_pointers"].update(pointers)
                item["source_feature_ids"].update(f["feature_id"] for f in active)
                item["assertions"].append(deepcopy(assertion))
    return result


def _native_assertion_source(pointer, vid, profile):
    # Rules derived directly from an effective native contract may have no precise feature.
    if pointer.startswith("/resource_projections/"):
        return _used_projection(profile, vid, pointer)
    if pointer.startswith("/views/"):
        return at(profile, "/".join(pointer.split("/")[:3])).get("view_id") == vid
    return pointer in {"/primary_domain"} or pointer.startswith(("/common_specification/", "/quantities/", "/parameters/"))


def rebuild_indexes(profile, projected, old, vocabulary):
    machine, human = projected["machine_tags"], projected["human_tags"]
    projected["identity"]["regime_predicates"] = regime_index(profile)
    definitions = human_vocabulary_index(vocabulary)
    scoped = retained_navigation(old, profile, machine, vocabulary)
    facets = {f["concept_id"]: f for f in human["facets"]}
    for (cid, vid), support in scoped.items():
        definition = definitions[cid]
        axis, group, value = cid.split(":")
        facet = facets.setdefault(cid, {"concept_id":cid, "axis":axis, "group":group, "value":value,
                                    "label":definition.get("label", value), "parent_id":definition.get("parent_id"),
                                    "status":"known", "normalization_state":"controlled", "display_level":"navigation",
                                    "source_pointers":[], "source_feature_ids":[], "view_ids":[]})
        facet["view_ids"] = sorted(set(facet["view_ids"]) | {vid})
        for field in ("source_pointers", "source_feature_ids"):
            facet[field] = sorted(set(facet[field]) | support[field])
        facet.setdefault("evidence", []).append({"view_id":vid, "assertions":support["assertions"]})
    human["facets"] = list(facets.values())
    for row in human["views"]:
        row["facet_ids"] = sorted(f["concept_id"] for f in facets.values() if row["view_id"] in f["view_ids"])
    machine["navigation_by_view"] = {r["view_id"]: r["facet_ids"] for r in human["views"]}
    known = {f["concept_id"] for f in machine["features"] if f["status"] == "known"}
    machine["retrieval_concept_ids"] = sorted(expand_concepts(known, vocabulary) | set(facets))
    return scoped
