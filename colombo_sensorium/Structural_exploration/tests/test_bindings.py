"""Engineering regressions for binding normalization; all specifications test field contracts only."""
from copy import deepcopy

from oracle_atlas.atlas.bindings import normalize_tag_facts
from oracle_atlas.atlas.tags import project_tags


def slq_shape():
    """Extract operation/ID shapes from the actually rejected profile 51766af..., without asserting scientific conclusions."""
    return {
        "setting_id": "MX_S_cesm_wasserstein", "title": "Binding regression only",
        "objects": [{"id": "A"}],
        "common_specification": {
            "oracle": {"operations": [{"id": "right_matvec", "operation_code": "matrix_right_matvec",
                                       "target_object": "A", "feedback_quality": {"code": "exact"},
                                       "response_signature": "Return the complete exact vector Av in R^n."}]},
            "algorithms": {"summary": "The view declares algorithm permissions."},
        },
        "views": [{"view_id": "slq-exact-randomized", "algorithms": {"randomization": "private"},
                   "guarantees": [], "specification_overrides": {}}],
    }


def operation_fact(**overrides):
    fact = {"axis": "ORACLE", "concept_id": "ORACLE:operation:matrix_right_matvec", "value": "matrix_right_matvec",
            "object_ref": "A", "operation_ref": "right_matvec", "view_ref": "slq-exact-randomized",
            "source_pointer": "/common_specification/oracle/operations/0", "status": "known"}
    fact.update(overrides)
    return fact


def test_real_rejection_pointer_shapes_normalize_without_mutating_input():
    p = slq_shape()
    facts = [operation_fact(view_ref="/views/0", operation_ref="/operations/0", source_pointer="/operations/0"),
             {"axis": "ALGORITHMS", "concept_id": "ALGORITHMS:randomization:randomized", "value": "randomized",
              "object_ref": None, "operation_ref": None, "view_ref": "/views/0",
              "source_pointer": "/common_specification/algorithms/summary", "status": "known"}]
    original = deepcopy((p, facts))
    result = normalize_tag_facts(p, facts)
    assert result["errors"] == []
    assert result["facts"][0]["view_ref"] == "slq-exact-randomized"
    assert result["facts"][0]["operation_ref"] == "right_matvec"
    assert result["facts"][0]["source_pointer"] == "/common_specification/oracle/operations/0"
    assert len(result["changes"]) == 4
    assert (p, facts) == original
    project_tags(p, result["facts"])
    assert normalize_tag_facts(p, result["facts"])["changes"] == []


def test_top_level_operation_without_canonical_interface_is_not_promoted():
    p = slq_shape()
    p["operations"] = [{"operation_id": "right_matvec", "object_ref": "/objects/0",
                         "reply": "full Av", "accuracy": {"type": "exact"}}]
    del p["common_specification"]["oracle"]["operations"]
    f = operation_fact(operation_ref="/operations/0", view_ref="/views/0", source_pointer="/operations/0")
    result = normalize_tag_facts(p, [f])
    assert result["facts"][0]["view_ref"] == "slq-exact-randomized"
    assert any(e["code"] == "operation_scope_missing" for e in result["errors"])
    assert "operations" not in p["common_specification"]["oracle"]


def test_common_operation_pointer_does_not_select_one_of_different_views():
    p = slq_shape()
    second = deepcopy(p["views"][0]); second["view_id"] = "left_only"
    second["specification_overrides"] = {"oracle": {"operations": [{"id": "left", "operation_code": "matrix_left_matvec",
                                                                            "target_object": "A", "feedback_quality": {"code": "exact"}}]}}
    p["views"].append(second)
    result = normalize_tag_facts(p, [operation_fact(operation_ref="/operations/0", source_pointer="/operations/0", view_ref=None)])
    assert any(e["code"] == "ambiguous_operation_pointer" for e in result["errors"])
    assert result["facts"][0]["operation_ref"] == "/operations/0"
    selected = normalize_tag_facts(p, [operation_fact(operation_ref="/operations/0", source_pointer="/operations/0", view_ref="/views/1")])
    assert selected["errors"] == []
    assert selected["facts"][0]["operation_ref"] == "left"
    assert selected["facts"][0]["source_pointer"] == "/views/1/specification_overrides/oracle/operations/0"


def test_overridden_common_operation_cannot_be_borrowed_even_if_id_is_same():
    p = slq_shape()
    p["views"][0]["specification_overrides"] = {"oracle": {"operations": [{"id": "right_matvec", "operation_code": "other",
                                                                            "target_object": "A", "feedback_quality": {"code": "inexact"}}]}}
    result = normalize_tag_facts(p, [operation_fact(operation_ref="/common_specification/oracle/operations/0")])
    assert any(e["code"] == "unknown_operation" for e in result["errors"])


def test_operation_source_and_view_errors_are_aggregated_across_facts():
    p = slq_shape()
    p["common_specification"]["oracle"]["operations"].append({"id": "left", "operation_code": "matrix_left_matvec", "target_object": "A"})
    facts = [operation_fact(operation_ref="does_not_exist"),
             operation_fact(source_pointer="/common_specification/task/statements/0"),
             operation_fact(operation_ref="left"),
             operation_fact(view_ref=None, operation_ref=None, source_pointer="/views/0/algorithms/randomization")]
    result = normalize_tag_facts(p, facts)
    assert {e["path"].split("/")[2] for e in result["errors"]} == {"0", "1", "2", "3"}
    assert any(e["code"] == "unresolved_source_pointer" for e in result["errors"])
    assert all(result["facts"][i] == facts[i] for i in range(len(facts)))


def test_statement_references_are_not_rewritten_or_reinterpreted():
    p = slq_shape()
    p["common_specification"]["oracle"]["statements"] = [{"operation_ref": "/operations/0", "text": "An explicitly scoped statement."}]
    result = normalize_tag_facts(p, [operation_fact(source_pointer="/common_specification/oracle/statements/0/text")])
    assert any(e["code"] == "binding_invalid" for e in result["errors"])
    assert p["common_specification"]["oracle"]["statements"][0]["operation_ref"] == "/operations/0"
    p["common_specification"]["oracle"]["statements"][0]["operation_ref"] = "right_matvec"
    assert normalize_tag_facts(p, [operation_fact(source_pointer="/common_specification/oracle/statements/0/text")])["errors"] == []


def test_explicit_unknown_does_not_require_guessed_native_interface():
    p = slq_shape()
    p.pop("setting_id")
    p["common_specification"]["oracle"] = {"summary": "The source leaves native feedback unknown."}
    result = normalize_tag_facts(p, [operation_fact(operation_ref=None, view_ref=None, object_ref=None,
                                                 source_pointer="/common_specification/oracle/summary", status="unknown")])
    assert result["errors"] == []
    assert result["facts"][0]["status"] == "unknown"
    assert "setting_id" not in p


def test_named_id_path_can_only_resolve_the_exact_effective_id():
    p = slq_shape()
    result = normalize_tag_facts(p, [operation_fact(operation_ref="/common_specification/oracle/operations/right_matvec",
                                                 source_pointer="/common_specification/oracle/operations/right_matvec")])
    assert result["errors"] == []
    assert result["facts"][0]["operation_ref"] == "right_matvec"
    assert normalize_tag_facts(p, [operation_fact(operation_ref="/common_specification/oracle/operations/right")])["errors"]


def test_object_pointer_repairs_only_to_the_explicit_same_operation_target():
    p = slq_shape()
    result = normalize_tag_facts(p, [operation_fact(object_ref="/objects/0")])
    assert result["errors"] == []
    assert result["facts"][0]["object_ref"] == "A"
    p["objects"].append({"id": "A"})
    assert any(e["code"] == "ambiguous_object_id" for e in normalize_tag_facts(p, [operation_fact(object_ref="/objects/0")])["errors"])


def test_invalid_pointer_and_duplicate_native_ids_are_rejected():
    p = slq_shape()
    for bad in ["/operations/-1", "/operations/01", "/operations/0/id", "/views/0", "/operations/" + "9" * 5000]:
        assert normalize_tag_facts(p, [operation_fact(operation_ref=bad)])["errors"]
    assert normalize_tag_facts(p, [operation_fact(view_ref="/views/" + "9" * 5000)])["errors"]
    p["common_specification"]["oracle"]["operations"].append(deepcopy(p["common_specification"]["oracle"]["operations"][0]))
    assert normalize_tag_facts(p, [operation_fact(operation_ref="/operations/0")])["errors"]
