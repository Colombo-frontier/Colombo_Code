"""Native budget continuation must retain the actual draft and the terminal material request."""
import hashlib
import json
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.store import Workspace, dumps
from oracle_atlas.providers.base import Reply
from oracle_atlas.runtime.native_budget import BUDGET_REASON, CHECKPOINT_RESERVE, LEGACY_ERROR, exhausted_limit, reserve_call
from oracle_atlas.workflow.engine import Engine


def test_atomic_ceiling_and_bounded_checkpoint_reserve(tmp_path):
    ws = Workspace(tmp_path)
    jid = ws.create_job("extractor", {})
    assert reserve_call(ws, jid, "first", "source_read", {}, 1)
    assert not reserve_call(ws, jid, "denied", "source_fetch", {}, 1)
    assert not reserve_call(ws, jid, "wrong-kind", "artifact_put", {"kind": "result"}, 1)
    assert reserve_call(ws, jid, "checkpoint", "artifact_put", {"kind": "checkpoint"}, 1)
    for i in range(CHECKPOINT_RESERVE - 1):
        assert reserve_call(ws, jid, f"memory-{i}", "memory_save", {}, 1)
    assert not reserve_call(ws, jid, "overflow", "memory_save", {}, 1)
    assert len(ws.query("SELECT * FROM tool_calls")) == 1 + CHECKPOINT_RESERVE
    assert len(ws.query("SELECT * FROM events WHERE event='native_tool_budget_exhausted'")) == 1
    ws.close()


def test_only_evidenced_budget_handoff_can_advance_on_new_limit(tmp_path):
    responses = []
    class Backend:
        def complete(self, **request):
            responses.append(request)
            text = BUDGET_REASON + ": fixed host ceiling" if len(responses)==1 else "Missing original theorem."
            return Reply(text=dumps({"status":"needs_materials","summary":text,"artifact_refs":[],"checkpoint_ref":None}))

    config={"backend":"codex","model":{},"atlas":str(tmp_path/"atlas"),"workspace":str(tmp_path/"work"),
            "budgets":{**DEFAULTS,"max_turns":1}}
    e=Engine(config, Backend())
    jid=e.ws.create_job("extractor",{})
    for i in range(8):
        assert reserve_call(e.ws,jid,str(i),"schema_read",{},8)
    assert not reserve_call(e.ws,jid,"excess","schema_read",{},8)
    draft=e.ws.draft_create(jid,"candidate",{"unreviewed":"same draft"},"keep")["draft_id"]
    assert e.runner.run(jid)["status"]=="needs_materials"
    assert e.runner.run(jid,continue_budget=True)["status"]=="needs_materials" and len(responses)==1
    config["budgets"]["max_turns"]=2
    assert e.runner.run(jid)["status"]=="needs_materials" and len(responses)==1
    result=e.runner.run(jid,continue_budget=True)
    assert result["status"]=="needs_materials" and len(responses)==2
    assert result["output"]["summary"]=="Missing original theorem."
    assert e.runner.run(jid,continue_budget=True)["output"]==result["output"] and len(responses)==2
    event=json.loads(e.ws.query("SELECT payload FROM events WHERE event='native_budget_continued'")[0]["payload"])
    assert event["drafts"][0]["id"]==draft and event["previous_handoff"]["summary"].startswith(BUDGET_REASON)
    assert len(e.ws.query("SELECT DISTINCT request_hash FROM calls"))==2
    assert len(e.ws.query("SELECT * FROM events WHERE event='transport_retry_authorized'"))==0
    e.ws.close()


def test_legacy_exact_native_receipt_required(tmp_path):
    ws=Workspace(tmp_path)
    jid=ws.create_job("extractor",{})
    out={"status":"needs_materials","summary":"The tool budget is exhausted.","artifact_refs":[],"checkpoint_ref":None}
    ws.save_job(jid,"needs_materials",{},out)
    with ws.transaction() as db:
        db.execute("INSERT INTO calls VALUES(?,?,?,?,?,?,?,?)",("call",jid,"h","response","{}",dumps({"response_id":"thread","text":dumps(out)}),None,1))
    for i in range(8):
        assert reserve_call(ws,jid,str(i),"schema_read",{},8)
    group=hashlib.sha256(jid.encode()).hexdigest()[:20]
    p=tmp_path/"transport"/"codex"/group/"request"/"g0000";p.mkdir(parents=True)
    (p/"receipt.json").write_text(dumps({"status":"completed","request_hash":"request"}))
    (p/"transport-metadata.json").write_text(dumps({"job_id":jid,"request_hash":"request"}))
    (p/"final.json").write_text(dumps(out))
    def write(server,thread):
        rows=[{"type":"thread.started","thread_id":thread},{"type":"item.completed","item":{"type":"mcp_tool_call",
            "server":server,"status":"completed","result":{"content":[{"type":"text","text":dumps({"error":LEGACY_ERROR})}]}}}]
        (p/"events.jsonl").write_text("\n".join(map(dumps,rows)))
    write("other","thread");assert exhausted_limit(ws,ws.job(jid)) is None
    write("oracle_atlas","other-thread");assert exhausted_limit(ws,ws.job(jid)) is None
    write("oracle_atlas","thread");assert exhausted_limit(ws,ws.job(jid))==8
    ws.close()
