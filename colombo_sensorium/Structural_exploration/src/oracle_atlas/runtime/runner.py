"""Bounded tool loop. Paid responses, protocol rejections, and validated handoffs are recorded separately."""
from __future__ import annotations

import json
import time
from dataclasses import asdict

from jsonschema import Draft202012Validator

from ..core.contracts import MAIN_KINDS, ProtocolError, references, schema, validate, tool_error
from ..core.store import Workspace, digest, dumps
from ..providers.base import Reply, ToolCall, ProviderProtocolError, ProviderRefusal
from ..tools.host import ToolHost
from .instructions import load_instructions


class AgentRunner:
    def __init__(self, workspace: Workspace, atlas, backend, config: dict, *, bridge=None, bibliography=None):
        self.ws=workspace; self.atlas=atlas; self.backend=backend; self.config=config
        self.bridge=bridge; self.bibliography=bibliography

    def run(self, job_id: str, *, validate_output=None, retry_transport=False, repair_protocol=False, continue_budget=False) -> dict:
        job=self.ws.job(job_id)
        if job["status"] in {"complete","needs_materials","blocked"}:
            return job
        if job["status"] == "transport_uncertain" and not retry_transport:
            return job
        if job["status"] == "protocol_error" and not repair_protocol:
            return job
        if job["status"] == "budget_exhausted" and not continue_budget:
            return job
        instructions, manifest=load_instructions(job["role"])
        state=job["state"] or {}
        if retry_transport and job["status"]=="transport_uncertain":
            state["transport_retry_generation"]=state.get("transport_retry_generation",0)+1
            self.ws.event(job_id,"transport_retry_authorized",{"generation":state["transport_retry_generation"],"previous_attempt_retained":True})
        job["state"]=state
        if state.get("manifest_hash") and state["manifest_hash"] != digest(manifest):
            raise ProtocolError("Instructions changed during execution; continue as a new revision, not as recovery of the same request")
        initial={"role":"user","content":dumps({"job_id":job_id,"inputs":job["inputs"]})}
        state.setdefault("history",[initial]); state.setdefault("turn",0)
        state.setdefault("segment",0); state.setdefault("repairs",0)
        state["manifest_hash"]=digest(manifest)
        self.ws.event(job_id,"instruction_manifest",manifest)
        if hasattr(self.backend,"bind_job"):
            self.backend.bind_job(job,self.config)
        host=ToolHost(self.ws,self.atlas,job,self.config,bridge=self.bridge,bibliography=self.bibliography)
        tools=host.definitions(); cap=self.config["budgets"]["max_input_chars"]
        budgets=self.config["budgets"]
        fixed_chars=len(instructions)+len(dumps(tools))+len(dumps(schema("handoff")))
        if fixed_chars+len(dumps(initial)) > cap:
            raise ProtocolError("The fixed role/tool input exceeds the configured budget; specifications or schemas must not be truncated to run")
        self.ws.save_job(job_id,"running",state)
        while state["turn"] < budgets["max_turns"]:
            size=fixed_chars+len(dumps(state["history"]))
            if size > cap:
                if state["segment"]+1 >= budgets["max_segments"]:
                    return self._stop(job_id,"budget_exhausted",state,"The session segment budget is exhausted; formal intermediate results have been saved")
                state["segment"]+=1
                notes=self.ws.memory_search(job_id,"",limit=2)
                state["history"]=[initial,{"role":"user","content":dumps({"resume_segment":state["segment"],"notes":notes,"instruction":"The previous bounded context has ended. Use work_list / memory_search to retrieve saved drafts and formal results, then fetch source text as needed. Do not inherit unrecorded conjectures."})}]
                self.ws.event(job_id,"context_rotated",{"segment":state["segment"],"previous_chars":size})
                self.ws.save_job(job_id,"running",state)
                size=fixed_chars+len(dumps(state["history"]))
            if size > cap:
                return self._stop(job_id,"budget_exhausted",state,"The continuation catalog exceeds the input budget")
            request={"instructions":instructions,"input_items":state["history"],"tools":tools,"output_schema":schema("handoff")}
            call_id=f"{job_id}:{state['segment']}:{state['turn']}:g{state.get('transport_retry_generation',0)}"
            rows=self.ws.query("SELECT * FROM calls WHERE id=?",(call_id,))
            existing=rows[0] if rows else None
            if existing and existing["request_hash"] != digest(request):
                raise ProtocolError("Request content changed under the same call ID")
            if existing and existing["status"] == "pending" and not retry_transport:
                return self._stop(job_id,"transport_uncertain",state,"The call was issued but no recoverable response exists; no automatic repeat payment")
            if existing and existing["response"] and existing["status"] == "response":
                raw=json.loads(existing["response"])
                reply=Reply(output_items=raw["output_items"],calls=[ToolCall(**x) for x in raw["calls"]],text=raw["text"],usage=raw.get("usage"),response_id=raw.get("response_id"))
            else:
                scope=job["inputs"].get("budget_scope",job_id)
                count=self.ws.query("SELECT COUNT(*) AS n FROM calls c JOIN jobs j ON c.job=j.id WHERE COALESCE(json_extract(j.inputs,'$.budget_scope'),j.id)=?",(scope,))[0]["n"]
                if not existing and count >= budgets["max_total_calls"]:
                    return self._stop(job_id,"budget_exhausted",state,"The model-call budget for this run is exhausted")
                batch_scope=job["inputs"].get("batch_scope")
                if batch_scope and not existing:
                    batch_count=self.ws.query("SELECT COUNT(*) AS n FROM calls c JOIN jobs j ON c.job=j.id WHERE json_extract(j.inputs,'$.batch_scope')=?",(batch_scope,))[0]["n"]
                    batch_limit=self.config.get("expansion",{}).get("max_batch_model_calls",1600)
                    if batch_count >= batch_limit:
                        return self._stop(job_id,"budget_exhausted",state,"The expansion batch provider-call budget is exhausted; saved responses remain recoverable. Native Codex calls count client session boundaries, not internal model calls.")
                with self.ws.transaction() as db:
                    db.execute("INSERT OR IGNORE INTO calls VALUES(?,?,?,?,?,?,?,?)",(call_id,job_id,digest(request),"pending",dumps(request),None,None,time.time()))
                self.ws.event(job_id,"model_request",{"call_id":call_id,"input_chars":size,"segment":state["segment"],"measure":"serialized client input; not hidden server context"})
                try:
                    reply=self.backend.complete(**request)
                except ProviderRefusal as exc:
                    self._archive_exception(call_id,exc,"refusal")
                    return self._stop(job_id,"blocked",state,"The model refusal has been archived; do not enter formatting resampling")
                except ProviderProtocolError as exc:
                    self._archive_exception(call_id,exc,"rejected")
                    if not self._repair(job_id,state,str(exc),getattr(exc,"raw_response",None)):
                        return self._stop(job_id,"protocol_error",state,str(exc))
                    continue
                except Exception as exc:
                    # Preserve requests for configuration, HTTP, and connection failures. Do not claim that a retry is free when the response is uncertain.
                    self.ws.event(job_id,"transport_uncertain",{"call_id":call_id,"error_type":type(exc).__name__,"message":str(exc)[:1500]})
                    return self._stop(job_id,"transport_uncertain",state,str(exc)[:1500])
                with self.ws.transaction() as db:
                    db.execute("UPDATE calls SET status='response',response=? WHERE id=?",(dumps(asdict(reply)),call_id))
                self.ws.event(job_id,"model_response",{"call_id":call_id,"response_id":reply.response_id,"usage":reply.usage,"usage_known":reply.usage is not None})
            retry_transport=False
            state["history"].extend(reply.output_items)
            if reply.calls:
                defs={t["name"]:t for t in tools}
                for call in reply.calls:
                    token=f"{job_id}:{call.call_id}"
                    cached=self.ws.query("SELECT * FROM tool_calls WHERE id=?",(token,))
                    if cached and (cached[0]["name"] != call.name or cached[0]["args"] != dumps(call.arguments)):
                        raise ProtocolError("tool call_id was reused for a different operation")
                    if cached and cached[0]["status"] == "done":
                        result=json.loads(cached[0]["result"])
                        host.grants.update(references(result))
                    else:
                        with self.ws.transaction() as db:
                            db.execute("INSERT OR IGNORE INTO tool_calls VALUES(?,?,?,?,?,?)",(token,job_id,call.name,dumps(call.arguments),None,"pending"))
                        try:
                            if call.name not in defs: raise ProtocolError("Tool is not authorized")
                            errors=list(Draft202012Validator(defs[call.name]["parameters"]).iter_errors(call.arguments))
                            if errors: raise ProtocolError("; ".join(e.message for e in errors[:8]))
                            result=host.call(call.name,call.arguments,call.call_id)
                            # Limit the entire tool response, not only its body while allowing metadata to grow unchecked.
                            if len(dumps(result)) > budgets["max_tool_chars"]+2000:
                                ref=self.ws.artifacts.put("external_result",{"tool":call.name,"result":result},job_id)
                                host.grants.add(ref)
                                result={"archived_result_ref":ref,"message":"The result exceeds the response limit; use artifact_get /result with pagination","chars":len(dumps(result))}
                        except Exception as exc:
                            result=tool_error(exc)
                        with self.ws.transaction() as db:
                            db.execute("UPDATE tool_calls SET result=?,status='done' WHERE id=?",(dumps(result),token))
                    state["history"].append({"type":"function_call_output","call_id":call.call_id,"output":dumps(result)})
                state["turn"]+=1
                if fixed_chars+len(dumps(state["history"])) > .8*cap:
                    state["history"].append({"role":"user","content":"The current context is near its budget. Save specific unresolved issues, formal result references, and next steps with memory_save; keep large manuscripts in drafts rather than concatenating their full text."})
                self.ws.save_job(job_id,"running",state)
                continue
            try:
                output=json.loads(reply.text)
                validate("handoff",output)
                for ref in output["artifact_refs"]:
                    if not self.ws.artifacts.owned(ref,job_id):
                        raise ProtocolError("handoff must reference artifacts produced by the current job; another job's approval cannot be reused")
                main=[r for r in output["artifact_refs"] if self.ws.artifacts.get(r)["kind"]==MAIN_KINDS[job["role"]]]
                if output["status"]=="complete" and len(main)!=1:
                    raise ProtocolError(f"complete must include one main artifact of kind {MAIN_KINDS[job['role']]}")
                if output["checkpoint_ref"]:
                    chk=self.ws.artifacts.get(output["checkpoint_ref"])
                    if chk["kind"]!="checkpoint" or not self.ws.artifacts.owned(chk["ref"],job_id):
                        raise ProtocolError("checkpoint must be a formally saved checkpoint of this job")
                if validate_output: validate_output(job,output)
            except (ProtocolError,ValueError,KeyError,TypeError) as exc:
                with self.ws.transaction() as db:
                    db.execute("UPDATE calls SET status='rejected',diagnostic=? WHERE id=?",(str(exc),call_id))
                if not self._repair(job_id,state,str(exc),reply.text):
                    return self._stop(job_id,"protocol_error",state,str(exc))
                continue
            state["turn"]+=1
            self.ws.save_job(job_id,output["status"],state,output)
            self.ws.event(job_id,"validated_handoff",{"refs":output["artifact_refs"],"status":output["status"]})
            return self.ws.job(job_id)
        return self._stop(job_id,"budget_exhausted",state,"The tool/model turn budget for this job is exhausted")

    def _repair(self,job_id,state,diagnostic,raw) -> bool:
        # Consume and persist the invalid response before the next request; do not repeatedly read the same pending response indefinitely.
        state["turn"]+=1; state["repairs"]+=1
        self.ws.event(job_id,"protocol_rejected",{"diagnostic":diagnostic,"repair_number":state["repairs"]})
        ref=self.ws.artifacts.put("external_result",{"diagnostic":diagnostic,"invalid_output_json":dumps(raw)},job_id)
        state["history"].append({"role":"user","content":dumps({"protocol_repair":diagnostic,"rejected_output_ref":ref,"instructions":"Repair formatting/bindings; retrieve the original invalid output with artifact_get and obtain the complete artifact schema with schema_read first. Do not remove genuine issues or alter a scientific rejection to satisfy validation.","handoff_schema":schema("handoff")})})
        self.ws.save_job(job_id,"running",state)
        return state["repairs"] <= self.config["budgets"]["max_protocol_repairs"]

    def _archive_exception(self,call_id,exc,status):
        with self.ws.transaction() as db:
            db.execute("UPDATE calls SET status=?,response=?,diagnostic=? WHERE id=?",(status,dumps(getattr(exc,"raw_response",None)),str(exc)[:5000],call_id))

    def _stop(self,job_id,status,state,message):
        state["last_error"]=message
        self.ws.save_job(job_id,status,state)
        return self.ws.job(job_id)
