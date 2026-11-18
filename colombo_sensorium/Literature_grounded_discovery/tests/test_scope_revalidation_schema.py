"""Schema-only controls; runtime eligibility and mathematics are validated separately."""
from copy import deepcopy

from jsonschema import Draft202012Validator
import pytest

from oracle_atlas.core.contracts import schema


REF = "sha256:" + "a" * 64


def review():
    return {
        "subject_ref": REF, "review_type": "profile", "verdict": "revise",
        "assessments": [], "issues": [], "approved_bound_ids": [],
        "summary": "Schema fixture only; no scientific approval.",
        "issue_scope_version": "occurrence-bound-scope",
    }


def revalidation():
    return {"proof_ref": REF, "candidate_id": "controller-candidate", "changes_reviewed": True,
            "reason": "Fixture reviewer examines changed context; not a proof result."}


def errors(value):
    return list(Draft202012Validator(schema("review")).iter_errors(value))


@pytest.mark.parametrize("scope", ["standalone_proposition", "standalone_proposition_explicit_context"])
def test_legacy_and_explicit_context_credentials_remain_valid_shapes(scope):
    data = review()
    data["proof_approvals"] = [{"proof_ref": REF, "scope": scope, "assumptions_complete": True,
        "context_pointers": ["/common_specification", "/parameters/0"], "reason": "Fixture only."}]
    assert errors(data) == []


def test_current_scope_revalidation_shape_is_optional_and_compatible():
    data = review()
    assert errors(data) == []
    data["proof_scope_revalidations"] = [revalidation()]
    assert errors(data) == []
    assert schema("review")["properties"]["issue_scope_version"]["enum"] == ["snapshot-bound-scope", "occurrence-bound-scope"]


@pytest.mark.parametrize("field,value", [("proof_ref", "old-proof"), ("candidate_id", ""),
    ("changes_reviewed", False), ("reason", ""), ("automatic_reuse", True)])
def test_scope_revalidation_rejects_incomplete_or_invented_declarations(field, value):
    data = review()
    row = revalidation()
    row[field] = value
    data["proof_scope_revalidations"] = [row]
    assert errors(data)


@pytest.mark.parametrize("field", ["proof_ref", "candidate_id", "changes_reviewed", "reason"])
def test_scope_revalidation_requires_each_field(field):
    data = review()
    row = revalidation()
    del row[field]
    data["proof_scope_revalidations"] = [row]
    assert errors(data)


def test_identical_revalidation_rows_are_rejected():
    data = review()
    row = revalidation()
    data["proof_scope_revalidations"] = [row, deepcopy(row)]
    assert errors(data)
