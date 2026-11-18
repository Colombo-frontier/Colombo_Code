"""Adversarial writer/controller acceptance; all science here is synthetic."""
from copy import deepcopy
from pathlib import Path
import shutil

import pytest

from oracle_atlas.atlas.store import Atlas, AtlasValidationError
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.core.store import Workspace, digest
from oracle_atlas.science.gates import research_context, ScienceContractError
from oracle_atlas.workflow.engine import Engine
from test_atlas import profile, facts, approve


@pytest.fixture
def atlas(tmp_path):
    root=tmp_path/"atlas"
    shutil.copytree(Path(__file__).parent/"fixtures/native_atlas/data/schemas",root/"data/schemas")
    return Atlas(root)


@pytest.mark.parametrize("mutation",["unknown_status","missing_status","false_summary","no_joint","old_joint","hidden_status"])
def test_new_write_fails_closed_even_without_target_schemas(tmp_path,mutation):
    a=Atlas(tmp_path/"atlas")
    p=profile()
    if mutation=="unknown_status":p["comparisons"][0]["status"]["code"]="custom_optimal"
    elif mutation=="missing_status":del p["comparisons"][0]["status"]
    elif mutation=="false_summary":p["summary_status"]["badges"].append({"code":"fully_optimal","label":"Fully optimal"})
    elif mutation=="no_joint":del p["joint_analysis"]
    elif mutation=="old_joint":p["joint_analysis"]["version"]=1
    else:p["regimes"][0]["status"]={"code":"custom_optimal"}
    with pytest.raises(AtlasValidationError):a.prepare(p,facts(p))
    assert not list(a.settings.glob("*/profile.json"))


@pytest.mark.parametrize("mutation",["missing","bundle","analysis","context","omitted_check","repeated_check","bad_verdict","empty_reason","partial_approval"])
def test_writer_requires_exact_independent_science_checks(atlas,mutation):
    p=profile(); prepared=atlas.prepare(p,facts(p)); review=approve(prepared)
    value=review["joint_review"]
    if mutation=="missing":del review["joint_review"]
    elif mutation in {"bundle","analysis","context"}:
        key={"bundle":"prepared_hash","analysis":"analysis_hash","context":"science_context_hash"}[mutation]
        value[key]="0"*64
    elif mutation=="omitted_check":value["checks"].pop()
    elif mutation=="repeated_check":value["checks"][1]=deepcopy(value["checks"][0])
    elif mutation=="bad_verdict":value["checks"][0]["verdict"]=True
    elif mutation=="empty_reason":value["checks"][0]["reason"]="   "
    else:value["checks"][0]["verdict"]="defer"
    with pytest.raises(AtlasValidationError):atlas.commit(prepared,review,"invalid-"+mutation)
    assert atlas.version(p["setting_id"]) is None
    assert not list((atlas.state/"receipts").glob("*.json"))


def test_rehashed_context_still_requires_fresh_review(atlas):
    p=profile(); prepared=atlas.prepare(p,facts(p)); review=approve(prepared)
    prepared["science"]["research_context"]={"scope":{"scope":"Changed finite synthetic query scope.","queries_complete":False,"unresolved_leads":[]}}
    prepared["science"]["research_context_hash"]=digest(prepared["science"]["research_context"])
    prepared["science_hash"]=digest(prepared["science"])
    with pytest.raises(AtlasValidationError,match="science_context_hash"):
        atlas.commit(prepared,review,"changed-context")


def test_current_rule_bytes_are_part_of_reviewed_context(atlas):
    p=profile(); prepared=atlas.prepare(p,facts(p)); review=approve(prepared)
    prepared["science"]["contract"]["files"]["standards/status_taxonomy.json"]="0"*64
    prepared["science_hash"]=digest(prepared["science"])
    review["joint_review"]["science_context_hash"]=prepared["science_hash"]
    with pytest.raises(AtlasValidationError,match="rules changed"):
        atlas.commit(prepared,review,"stale-contract")


def test_finite_scope_requires_actual_declaration_and_controller_log_binding(atlas,tmp_path):
    ws=Workspace(tmp_path/"work")
    job=ws.create_job("profile_researcher",{})
    p=profile(); scope={"scope":"The explicit finite synthetic bibliography fixture.","queries_complete":True,"unresolved_leads":[]}
    p["research_scope"]=scope
    p["joint_analysis"]["synthesis_coverage"]["literature"]={"status":"finite_scope_complete","scope":scope["scope"]}
    with pytest.raises(AtlasValidationError):atlas.prepare(p,facts(p))
    context=research_context(ws,job,{"research_scope":scope})
    prepared=atlas.prepare(p,facts(p),research_context=context)
    assert prepared["science"]["research_context"]["observations"]["tool_trace_hash"]==digest([])
    with ws.transaction() as db:
        db.execute("INSERT INTO tool_calls VALUES(?,?,?,?,?,?)",("pending",job,"source_fetch","{}",None,"pending"))
    with pytest.raises(ScienceContractError,match="unconfirmed"):
        research_context(ws,job,{"research_scope":scope})
    changed=deepcopy(context);changed["scope"]["scope"]="Another query scope."
    with pytest.raises(AtlasValidationError,match="same actual research scope"):
        atlas.prepare(p,facts(p),research_context=changed)
    ws.close()


def test_no_change_cannot_grandfather_legacy_profile_or_neighbor(tmp_path):
    e=Engine({"workspace":str(tmp_path/"work"),"atlas":str(tmp_path/"atlas"),"budgets":dict(DEFAULTS),"model":{}},object())
    p=profile();del p["joint_analysis"]
    ref=e.put("native_record",{"setting_id":p["setting_id"],"version":"old-version","content":p})
    data={"setting_id":p["setting_id"],"base_version":"old-version"}
    ctx={"scope":{"scope":"Synthetic finite query scope.","queries_complete":True,"unresolved_leads":[]}}
    with pytest.raises(ValueError):e._no_change_snapshot(data,ctx,{"base_profile_ref":ref})
    with pytest.raises(ProtocolError,match="pinned"):
        e._no_change_snapshot(data,ctx,{"neighbor_refs":[ref]})
    e.ws.close()


def test_valid_new_profile_commits_once_and_snapshot_is_read_only(atlas,tmp_path):
    p=profile();ctx={"scope":{"scope":"Explicit synthetic finite fixture.","queries_complete":True,"unresolved_leads":[]}}
    p["joint_analysis"]["synthesis_coverage"]["literature"]={"status":"finite_scope_complete","scope":ctx["scope"]["scope"]}
    prepared=atlas.prepare(p,facts(p),research_context=ctx); review=approve(prepared)
    first=atlas.commit(prepared,review,"synthetic-valid")
    assert atlas.commit(prepared,review,"synthetic-valid")==first
    version=atlas.version(p["setting_id"])
    snap=atlas.review_snapshot(p["setting_id"],version,research_context=ctx)
    atlas.validate_review(snap,approve(snap))
    assert snap["read_only"] is True
    with pytest.raises(AtlasValidationError,match="read-only"):
        atlas.commit(snap,approve(snap),"cannot-publish-no-change")
    assert atlas.version(p["setting_id"])==version
    assert len(list((atlas.state/"receipts").glob("*.json")))==1
