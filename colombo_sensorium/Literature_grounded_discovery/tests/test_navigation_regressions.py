"""Regression cases for the reviewed matrix proposal and the new profile's predicate_text format."""
from copy import deepcopy
import json

from oracle_atlas.atlas.retrieval import scope_search
from oracle_atlas.atlas.sidecars import validate_sidecars
from oracle_atlas.atlas.store import Atlas
from oracle_atlas.atlas.tags import project_tags
from test_sidecar_validation import profile, vocabulary


MATRIX = "TASK:family:matrix_computation"
EXACT = "ORACLE:quality:exact"
PRIVATE = "ALGORITHMS:randomization:private_randomness_allowed"
RANDOM = "ALGORITHMS:randomization:randomized"
POINTER = "/views/0/algorithms/randomization"


def library():
    v = vocabulary()
    for part in v:
        v[part]["version"] = "navigation-profile"
    for cid in (MATRIX, RANDOM):
        axis, group, value = cid.split(":")
        v["human"]["concepts"].append({"id":cid, "axis":axis, "group":group, "value":value,
                                      "label":value, "parent_id":axis + ":" + group})
    return v


def bundle(p, facts, v, old=None):
    return {"profile.json":p, **{key+".json":val for key,val in project_tags(p, facts, v, baseline_files=old).items()}}


def prior():
    p = profile()
    v = library()
    fact = {"concept_id":PRIVATE, "axis":"ALGORITHMS", "status":"known", "source_pointer":POINTER,
            "object_ref":None, "operation_ref":None, "view_ref":"adaptive", "value":"private_randomness_allowed"}
    b = bundle(p, [fact], v)
    feature = next(f for f in b["machine_tags.json"]["features"] if f["concept_id"] == PRIVATE)
    b["human_tags.json"]["facets"].append({"concept_id":RANDOM,"view_ids":["adaptive"],
        "source_feature_ids":[feature["feature_id"]],"source_pointers":[POINTER],"evidence":[{"view_id":"adaptive",
            "assertions":[{"source_pointers":[POINTER],"precise_tag_refs":[PRIVATE],"rule_id":"browse.scoped_contract_normalization"}]}]})
    return p, v, fact, b


def test_native_regime_index_reorders_missing_and_new_predicates_without_stale_rows():
    p, v = profile(), library()
    p["regimes"] = [{"id":"r0", "predicate":"old"}, {"id":"r1", "predicate_text":"scoped text"}]
    initial = bundle(p, [], v)
    fresh = deepcopy(p)
    fresh["regimes"] = [{"id":"r1", "predicate_text":"scoped text"}, {"id":"r2", "description":"still open"}]
    updated = bundle(fresh, [], v, initial)
    assert updated["identity.json"]["regime_predicates"] == [
        {"regime_id":"r1", "source_pointer":"/regimes/0", "predicate_pointer":"/regimes/0/predicate_text", "evaluation_state":"unparsed"},
        {"regime_id":"r2", "source_pointer":"/regimes/1", "predicate_pointer":None, "evaluation_state":"unparsed"}]
    updated["identity.json"]["regime_predicates"] = initial["identity.json"]["regime_predicates"]
    assert "regime_index" in {e["code"] for e in validate_sidecars(updated, v, baseline_files=initial)}


def test_old_sourced_navigation_survives_two_reprojections_and_removal_fails_validation():
    p, v, fact, old = prior()
    fresh = bundle(p, [fact], v, old)
    repeat = bundle(p, [fact], v, fresh)
    assert not validate_sidecars(repeat, v, baseline_files=fresh)
    assert RANDOM in repeat["machine_tags.json"]["navigation_by_view"]["adaptive"]
    assert RANDOM in repeat["machine_tags.json"]["retrieval_concept_ids"]
    repeat["human_tags.json"]["facets"] = [r for r in repeat["human_tags.json"]["facets"] if r["concept_id"] != RANDOM]
    codes = {r["code"] for r in validate_sidecars(repeat, v, baseline_files=fresh)}
    assert {"lost_source_navigation", "machine_navigation", "view_facet_coverage"}.issubset(codes)


def test_stale_evidence_unknown_fact_semantic_change_and_new_view_do_not_inherit_navigation():
    p, v, fact, old = prior()
    stale = deepcopy(old)
    stale["human_tags.json"]["profile_sha256"] = "stale"
    edited = deepcopy(p); edited["views"][0]["algorithms"]["randomization"] = "none"
    removed_vocab = deepcopy(v); removed_vocab["human"]["version"] = "alternate-navigation-profile"
    for current, supplied, vocab, previous in ((p, [{**fact,"status":"unknown"}], v, old), (p, [], v, old),
            (edited, [fact], v, old), (p, [fact], v, stale), (p, [fact], removed_vocab, old)):
        assert RANDOM not in bundle(current, supplied, vocab, previous)["machine_tags.json"]["retrieval_concept_ids"]
    extra = deepcopy(p); extra["views"].append({**deepcopy(p["views"][0]), "view_id":"another"})
    nav = bundle(extra, [fact], v, old)["machine_tags.json"]["navigation_by_view"]
    assert RANDOM in nav["adaptive"] and RANDOM not in nav["another"]


def test_matrix_exact_and_restored_navigation_reach_the_actual_scoped_atlas_search(tmp_path):
    p, v, fact, old = prior()
    atlas = Atlas(tmp_path)
    (atlas.data / "vocabulary").mkdir()
    for kind, value in v.items():
        (atlas.data / "vocabulary" / (kind+"_tags.json")).write_text(json.dumps(value))
    dest = atlas.settings / p["setting_id"]; dest.mkdir()
    for state in (bundle(p, [fact], v), bundle(p, [fact], v, old)):
        for k, value in state.items():
            (dest / k).write_text(json.dumps(value))
        assert {MATRIX,EXACT} <= set(state["machine_tags.json"]["navigation_by_view"]["adaptive"])
        labels = [MATRIX, EXACT] + ([RANDOM] if RANDOM in state["machine_tags.json"]["retrieval_concept_ids"] else [])
        answer = scope_search(atlas, [{"concept_id":cid} for cid in labels])
        assert answer["matched_count"] == 1
        assert [r["view_id"] for r in answer["items"][0]["views"] if r["state"] == "matched"] == ["adaptive"]
    state["machine_tags.json"]["retrieval_concept_ids"].remove(EXACT)
    assert "machine_retrieval" in {e["code"] for e in validate_sidecars(state, v, baseline_files=old)}
