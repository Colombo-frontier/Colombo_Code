"""Regressions for native shapes from real SLQ candidates; do not infer mathematical interfaces from return prose."""
from copy import deepcopy

import pytest

from oracle_atlas.atlas.bindings import normalize_tag_facts
from oracle_atlas.atlas.sidecars import validate_sidecars
from oracle_atlas.atlas.tags import effective_native_operations, match_interface, project_tags
from test_bindings import operation_fact, slq_shape


def actual_shape():
    p = slq_shape()
    p["common_specification"]["oracle"]["operations"] = [{
        "operation_id": "right_matvec", "object_ref": "matrix_A", "query": "Algorithm chooses v.",
        "precision": {"model": "exact", "status": "known", "text": "Explanation is not parsed."},
        "noise": {"status": "not_applicable", "text": "Explanation is not parsed."},
        "returns": "Av∈R^n",
    }]
    return p


def fact(**updates):
    return operation_fact(object_ref="matrix_A", view_ref=None, **updates)


def files(p):
    return {"profile.json": p, **{name + ".json": value for name, value in project_tags(p, []).items()}}


def test_actual_slq_returns_scalar_and_model_precision_are_valid_without_mutating_source():
    p = actual_shape(); before = deepcopy(p)
    normalized = effective_native_operations(p, "slq-exact-randomized")
    row = normalized["operations"][0]
    assert normalized["complete"] and row["valid"]
    assert row["precision"] == "exact" and row["returns"] == ["Av∈R^n"]
    assert row["operation_code"] is None  # opaque label is not guessed into matrix_right_matvec
    assert row["precision_pointer"] == "/common_specification/oracle/operations/0/precision"
    assert normalize_tag_facts(p, [fact()])["errors"] == []
    assert match_interface(p, {"precision": "exact"})["state"] == "matched"
    assert validate_sidecars(files(p)) == []
    assert p == before and isinstance(p["common_specification"]["oracle"]["operations"][0]["returns"], str)


def test_consistent_precision_code_kind_model_aliases_and_returns_aliases_are_supported():
    p = actual_shape(); raw = p["common_specification"]["oracle"]["operations"][0]
    raw["precision"] = {"code": "exact", "kind": "noiseless", "model": "exact", "status": "known"}
    raw["return_components"] = ["Av∈R^n"]
    assert normalize_tag_facts(p, [fact()])["errors"] == []
    assert match_interface(p, {"precision": "exact"})["state"] == "matched"


@pytest.mark.parametrize("precision", [None, "unknown", {"model": "exact", "status": "unknown"},
    {"status": "unknown", "text": "exact in some unverified claim"}, {"model": None, "status": "known"}])
def test_explicit_unknown_precision_never_becomes_known_exact(precision):
    p = actual_shape(); p["common_specification"]["oracle"]["operations"][0]["precision"] = precision
    row = effective_native_operations(p, "slq-exact-randomized")["operations"][0]
    assert row["valid"] and row["precision"] is None
    assert match_interface(p, {"precision": "exact"})["state"] == "unknown"
    assert not any(x["concept_id"] == "ORACLE:quality:exact" for x in files(p)["human_tags.json"]["facets"])


@pytest.mark.parametrize("precision", [
    {"code": "exact", "model": "stochastic"}, {"code": None, "model": "exact"},
    {"code": "exact", "model": "inexact", "status": "unknown"},
    {"model": {"code": "exact"}}, {"text": "Exact matrix-vector multiplication"}, {"feedback": "Exact matrix-vector multiplication"},
    ["exact"], 1,
])
def test_conflicting_or_unsupported_precision_reports_actual_native_field(precision):
    p = actual_shape(); p["common_specification"]["oracle"]["operations"][0]["precision"] = precision
    result = normalize_tag_facts(p, [fact()])
    error = next(e for e in result["errors"] if e["code"] == "invalid_native_operation")
    assert error["source_pointer"] == "/common_specification/oracle/operations/0"
    assert any(d["path"] == "/common_specification/oracle/operations/0/precision" for d in error["native_diagnostics"])
    assert not any(e["code"] == "unknown_operation" for e in result["errors"])
    assert not effective_native_operations(p, "slq-exact-randomized")["complete"]
    assert validate_sidecars(files(p))


@pytest.mark.parametrize("returns,path", [(3, "/returns"), ({"code": "vector"}, "/returns"),
    (["vector", 4], "/returns/1"), ([{"component": "vector"}], "/returns/0")])
def test_bad_returns_is_an_invalid_native_operation_not_an_unknown_id(returns, path):
    p = actual_shape(); p["common_specification"]["oracle"]["operations"][0]["returns"] = returns
    result = normalize_tag_facts(p, [fact()])
    error = next(e for e in result["errors"] if e["code"] == "invalid_native_operation")
    assert error["operation_ref"] == "right_matvec"
    assert any(d["code"] == "invalid_returns" and d["path"] == "/common_specification/oracle/operations/0" + path for d in error["native_diagnostics"])
    assert not any(e["code"] == "unknown_operation" for e in result["errors"])
    assert any(e["path"] == "/common_specification/oracle/operations/0" + path for e in validate_sidecars(files(p)))


def test_nonexistent_id_remains_unknown_and_conflicting_declared_id_is_invalid():
    p = actual_shape()
    assert any(e["code"] == "unknown_operation" for e in normalize_tag_facts(p, [fact(operation_ref="not_declared")])["errors"])
    p["common_specification"]["oracle"]["operations"][0]["id"] = "a_different_declared_alias"
    errors = normalize_tag_facts(p, [fact()])["errors"]
    assert any(e["code"] == "invalid_native_operation" for e in errors)
    assert not any(e["code"] == "unknown_operation" for e in errors)


def test_invalid_view_override_points_to_the_actual_override_returns_field():
    p = actual_shape(); operation = deepcopy(p["common_specification"]["oracle"]["operations"][0]);operation["returns"] = {"vector": True}
    p["views"][0]["specification_overrides"] = {"oracle": {"operations": [operation]}}
    error = next(e for e in normalize_tag_facts(p, [fact()])["errors"] if e["code"] == "invalid_native_operation")
    assert error["source_pointer"] == "/views/0/specification_overrides/oracle/operations/0"
    assert any(d["path"] == "/views/0/specification_overrides/oracle/operations/0/returns" for d in error["native_diagnostics"])


def test_scalar_returns_remains_an_opaque_exact_label_for_interface_matching():
    p = actual_shape()
    assert match_interface(p, {"operation_ref": "right_matvec", "returns": ["Av∈R^n"]})["state"] == "matched"
    assert match_interface(p, {"operation_ref": "right_matvec", "returns": ["matrix_product"]})["state"] == "conflict"


def test_legacy_feedback_descriptor_is_preserved_as_unknown_without_reading_its_prose():
    p = actual_shape(); raw = p["common_specification"]["oracle"]["operations"][0]
    raw.pop("precision")
    raw["feedback_quality"] = {"feedback": "The prose happens to say exact; it is not a precision code.", "noise": "Legacy descriptive feedback."}
    row = effective_native_operations(p, "slq-exact-randomized")["operations"][0]
    assert row["valid"] and row["precision"] is None
    assert match_interface(p, {"precision": "exact"})["state"] == "unknown"
    assert validate_sidecars(files(p)) == []
