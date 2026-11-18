"""Executed evidence provenance and exact arithmetic, not a theorem checker."""
from copy import deepcopy
import json

import pytest

from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.core.store import dumps
from oracle_atlas.tools.exact_checks import execute, validate_execution_check
from test_draft_clone import context, host


def program(right="5/6"):
    return {"steps":[{"name":"answer", "expr":["if", ["lt", "1/3", "1/2"], ["add", "1/3", "1/2"], ["div", 1, 0]]}],
            "assertions":[{"id":"independent_value", "left":{"var":"answer"}, "relation":"eq", "right":right}]}


def proof_value(pid):
    return {"proof_id":pid, "origin":"analyst_derivation", "proposition":"Synthetic fixture only.",
            "premises":[], "argument":"No scientific claim.", "boundary_cases":"fixture",
            "quantifiers":"fixture", "resource_accounting":"fixture", "dependencies":[], "issues":[]}


def test_exact_arithmetic_and_executed_failure_are_both_retained(context):
    _, ws, _ = context
    proof = ws.artifacts.put("proof", proof_value("arithmetic_fixture"), "fixture-author")
    h = host(context, {"subject_ref":"fixture-subject", "proof_refs":[proof]}, "profile_reviewer")
    good = h.call("exact_check", {"label":"Exact sum", "program_json":dumps(program()), "evidence_refs":[proof]}, "check-good")
    bad = h.call("exact_check", {"label":"Deliberately false expected value", "program_json":dumps(program("1")), "evidence_refs":[proof]}, "check-bad")
    assert good["all_passed"] is True and bad["all_passed"] is False
    assert bad["failed_assertion_ids"] == ["independent_value"]
    assert ws.artifacts.get(good["check_ref"])["data"]["result"]["values"] == {"answer":"5/6"}
    assert len(ws.query("SELECT * FROM events WHERE event='exact_check_executed'")) == 2
    check = {"required":True,"reason":"Tests the specified fixture calculation only.","check_refs":[good["check_ref"]]}
    assert validate_execution_check(check, proof, ws.artifacts, subject_ref="fixture-subject") == []
    check["check_refs"] = [bad["check_ref"]]
    assert validate_execution_check(check, proof, ws.artifacts, subject_ref="fixture-subject")


def test_cannot_substitute_self_written_receipt_or_unrelated_proof(context):
    _, ws, _ = context
    proof = ws.artifacts.put("proof", proof_value("fixture"), "author")
    other = ws.artifacts.put("proof", proof_value("other"), "author")
    h = host(context, {"subject_ref":"s", "proof_refs":[proof,other]}, "profile_reviewer")
    out = h.call("exact_check", {"label":"Test", "program_json":dumps(program()), "evidence_refs":[proof]}, "actual")
    check = {"required":True,"reason":"fixture", "check_refs":[out["check_ref"]]}
    assert validate_execution_check(check, other, ws.artifacts, subject_ref="s")
    body = deepcopy(ws.artifacts.get(out["check_ref"])["data"]); body["label"] = "Fake execution"
    fake = ws.artifacts.put("external_result", body, h.job["id"], [proof])
    check["check_refs"] = [fake]
    assert any("actual tool execution" in e for e in validate_execution_check(check, proof, ws.artifacts, subject_ref="s"))
    with pytest.raises(ProtocolError, match="authorized"):
        h.call("exact_check", {"label":"Foreign", "program_json":dumps(program()), "evidence_refs":[ws.artifacts.put("proof", proof_value("private"), "foreign")]}, "foreign")


def test_author_experiments_are_not_independent_review_credentials(context):
    _, ws, _ = context
    proof = ws.artifacts.put("proof", proof_value("fixture"), "author")
    h = host(context, {"proof_refs":[proof]}, "profile_researcher")
    out = h.call("exact_check", {"label":"Author test", "program_json":dumps(program()), "evidence_refs":[proof]}, "author-test")
    errors = validate_execution_check({"required":True,"reason":"fixture","check_refs":[out["check_ref"]]}, proof, ws.artifacts, subject_ref="s")
    assert any("reviewer's" in e for e in errors)


def test_historical_execution_needs_a_completed_independent_credential(context):
    _, ws, _ = context
    proof = ws.artifacts.put("proof", proof_value("fixture"), "author")
    h = host(context, {"subject_ref":"old", "proof_refs":[proof]}, "profile_reviewer")
    out = h.call("exact_check", {"label":"Prior test", "program_json":dumps(program()), "evidence_refs":[proof]}, "test")
    check = {"required":True,"reason":"Fixture only", "check_refs":[out["check_ref"]]}
    assert validate_execution_check(check, proof, ws.artifacts, subject_ref="new")
    subject = ws.artifacts.put("external_result", {"fixture":"prior subject"}, "controller")
    with ws.transaction() as db:
        inputs = {**h.job["inputs"], "subject_ref":subject}
        db.execute("UPDATE jobs SET inputs=? WHERE id=?", (dumps(inputs),h.job["id"]))
    review = ws.artifacts.put("review", {"subject_ref":subject,"review_type":"profile","verdict":"revise", "assessments":[],
        "issues":[],"approved_bound_ids":[],"summary":"Synthetic fixture.","proof_approvals":[{
            "proof_ref":proof,"scope":"standalone_proposition","assumptions_complete":True,
            "context_pointers":["/common_specification"],"reason":"Fixture only.","execution_check":check}]}, h.job["id"])
    with ws.transaction() as db:
        db.execute("UPDATE jobs SET status='complete' WHERE id=?", (h.job["id"],))
    assert validate_execution_check(check, proof, ws.artifacts, subject_ref="new")
    ws.event(h.job["id"], "validated_handoff", {"status":"complete", "refs":[review]})
    assert validate_execution_check(check, proof, ws.artifacts, subject_ref="new") == []


@pytest.mark.parametrize("bad", [
    {"steps":[],"assertions":[]},
    {"steps":[{"name":"x","expr":{"var":"later"}}],"assertions":program()["assertions"]},
    {"steps":[{"name":"x","expr":["pow",2,100000]}],"assertions":program()["assertions"]},
    {"steps":[{"name":"x","expr":["add",True,1]}],"assertions":program()["assertions"]},
    {"steps":[{"name":"x","expr":["open","/etc/passwd"]}],"assertions":program()["assertions"]},
    {"steps":[{"name":"x","expr":["div",1,0]}],"assertions":program()["assertions"]},
    {"steps":[{"name":"x","expr":"1/0"}],"assertions":program()["assertions"]},
])
def test_bounded_language_rejects_unsupported_or_invalid_programs(bad):
    with pytest.raises(ProtocolError): execute(bad)


def test_not_applicable_is_a_scientific_declaration_not_a_fabricated_pass(context):
    _, ws, _ = context
    assert validate_execution_check({"required":False,"reason":"Nonconstructive argument; full symbolic verification still required.","check_refs":[]}, "unused", ws.artifacts, subject_ref="s") == []
    assert validate_execution_check({"required":True,"reason":"Required","check_refs":[]}, "unused", ws.artifacts, subject_ref="s")


def test_tool_is_not_available_to_extraction_jobs(context):
    h = host(context, {}, "extractor")
    with pytest.raises(ProtocolError, match="does not have tool"):
        h.call("exact_check", {"label":"no", "program_json":dumps(program()), "evidence_refs":[]}, "not-granted")
