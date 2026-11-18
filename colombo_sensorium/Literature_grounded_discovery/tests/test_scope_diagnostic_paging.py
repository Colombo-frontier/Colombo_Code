"""Large review-scope diagnostics stay fully archived and immediately navigable."""
import json

import pytest

from oracle_atlas.core.contracts import ValidationDiagnostics, tool_error
from test_preflight_pipeline import context, host, call
from test_atlas import profile


@pytest.mark.parametrize("method", ["draft_validate", "artifact_put"])
def test_large_scope_error_is_a_short_report_pointer_with_full_paged_content(context, monkeypatch, method):
    h = host(context)
    catalog = {"expected_issue_scopes": [{"issue_id": "fixture", "occurrence_ids": [f"occurrence:{i}" for i in range(80)]}],
               "current_review_occurrences": [{"occurrence_id": f"occurrence:{i}", "issue": {"message": "Full immutable diagnostic. " * 70}} for i in range(80)],
               "hard_dependency_blockers": []}
    errors = [{"code": "proof_approval_contract", "path": "/proof_approvals",
               "message": "Missing exact occurrence scopes", "scope_diagnostic": catalog}]
    monkeypatch.setattr(h, "_validate_artifact", lambda kind, data, *a, **kw: (data, errors, []))
    p = profile("PAGED_DIAGNOSTIC")
    if method == "draft_validate":
        draft = call(h, "draft_create", kind="profile", initial_json=json.dumps(p))
        result = call(h, method, draft_id=draft["draft_id"], tag_facts_json="")
        preview = result["errors"][0]
    else:
        with pytest.raises(ValidationDiagnostics) as failure:
            call(h, method, kind="profile", json_text=json.dumps(p), dependencies=[])
        assert failure.value.diagnostics[0]["scope_diagnostic"] == catalog
        result = tool_error(failure.value)
        preview = result["diagnostics"][0]
    assert len(json.dumps(result)) < 2000 < h.cap
    assert "scope_diagnostic" not in preview
    assert preview["scope_diagnostic_counts"]["current_review_occurrences"] == 80
    pointer = preview["scope_diagnostic_pointer"]
    assert pointer == "/errors/0/scope_diagnostic"
    assert h._allowed(result["report_ref"])["data"]["errors"][0]["scope_diagnostic"] == catalog
    offset, chunks = 0, []
    while True:
        page = call(h, "artifact_get", ref=result["report_ref"], pointer=pointer, offset=offset, limit=5000)
        if "data" in page:
            recovered = page["data"]
            break
        chunks.append(page["text"])
        if page["next_offset"] is None:
            recovered = json.loads("".join(chunks))
            break
        offset = page["next_offset"]
    assert recovered == catalog
