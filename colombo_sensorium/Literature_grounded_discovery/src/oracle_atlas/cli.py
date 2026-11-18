"""Command-line entry point. Agents generate all scientific text."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import sys
from pathlib import Path

from .core.config import load_config, resources_root
from .core.contracts import MAIN_KINDS, ProtocolError
from .core.store import Workspace, atomic_json
from .workflow.engine import Engine


class LazyBackend:
    def __init__(self,config): self.config=config;self.inner=None;self.job=None
    def bind_job(self,job,config):
        self.job=job
        self._resolve()
        if hasattr(self.inner,"bind_job"):self.inner.bind_job(self.job,self.config)
    def _resolve(self):
        if self.inner is None:
            if self.config.get("backend","responses")=="codex":
                from .providers.codex import CodexBackend
                self.inner=CodexBackend(self.config.get("model",{}))
            else:
                from .providers.responses import ResponsesBackend
                self.inner=ResponsesBackend(self.config.get("model",{}))
    def complete(self,**kwargs):
        self._resolve()
        return self.inner.complete(**kwargs)
    def close(self):
        if self.inner and hasattr(self.inner,"close"):self.inner.close()


def print_json(value): print(json.dumps(value,ensure_ascii=False,indent=2))


def import_source(engine,path, *, material_role=None):
    p=Path(path).resolve(); raw=p.read_bytes()
    if p.suffix.lower()==".pdf":
        try:from pypdf import PdfReader
        except ImportError as exc:raise ProtocolError('PDF import requires pip install ".[pdf]"') from exc
        text="\n\n".join(f"[Page {i+1}]\n{page.extract_text() or ''}" for i,page in enumerate(PdfReader(p).pages))
    else:text=raw.decode("utf-8")
    sha=hashlib.sha256(raw).hexdigest()
    metadata={"filename":p.name,"imported_by_user":True}
    if material_role:metadata.update(material_role=material_role,approval_status="unreviewed")
    return engine.put("source",{"url":p.as_uri(),"version":sha,"content_hash":sha,"text":text,"metadata":metadata})


def seed_paper(url,title):
    return {"title":title or url,"doi":None,"arxiv_id":None,"urls":[url],"publication_events":[],"provenance":[{"url":url,"method":"user_supplied_trigger"}],"read_status":"unread"}


def build_parser():
    p=argparse.ArgumentParser(prog="oracle-atlas",description="Agent system for paper discovery, setting research, independent review, and Atlas ingestion")
    sub=p.add_subparsers(dest="command",required=True)
    init=sub.add_parser("init",help="Generate a configuration template")
    init.add_argument("--config",default="config.local.toml");init.add_argument("--atlas",required=True);init.add_argument("--workspace",default="./work")
    init.add_argument("--backend",choices=["responses","codex"],default="responses");init.add_argument("--model",default="")
    for name,helptext in [("doctor","Check resources and configuration without calling a model"),("scan","Scan approved tasks and years"),("run-paper","Process a supplied trigger paper"),("scout-tasks","Discover task types and prepare proposals for review"),("approve-task","Manually approve a new task"),("reprepare","Reproject changed sidecars of an uncommitted, reviewed proposal and submit the new bundle for independent review"),("assess-transfer","Assess a paper result against an independently reviewed related target"),("status","Inspect actual stages and receipts"),("resume","Resume an unfinished job or revise a selected candidate"),("export","Export research and receipts for a fixed case"),("import-source","Import additional material"),("mcp","Internal stdio MCP service")]:
        q=sub.add_parser(name,help=helptext);q.add_argument("--config",required=True)
        if name=="scan":
            q.add_argument("--task",action="append",required=True);q.add_argument("--year",type=int,action="append",required=True)
            q.add_argument("--source",action="append");q.add_argument("--query-budget",type=int,default=12);q.add_argument("--paper-limit",type=int,default=10)
            q.add_argument("--event-kind",choices=["publication","preprint","any"],default="publication");q.add_argument("--notes",default="");q.add_argument("--run-label",default="",help="Resume the same run label; a new label starts a new literature scan")
        elif name=="run-paper":
            g=q.add_mutually_exclusive_group(required=True);g.add_argument("--url");g.add_argument("--paper-json");g.add_argument("--paper-ref")
            q.add_argument("--title",default="")
            q.add_argument("--research-material-ref",action="append",default=[],help="Supply unapproved reference material only to research and final review; it is not an extraction or identity answer")
            q.add_argument("--research-material-file",action="append",default=[],help="Import unapproved research references; every claim must be independently reverified")
        elif name=="scout-tasks":q.add_argument("--notes",default="");q.add_argument("--material-ref",action="append",default=[])
        elif name=="approve-task":q.add_argument("--proposal-ref",required=True);q.add_argument("--task-id",required=True)
        elif name=="reprepare":q.add_argument("--case-id",required=True)
        elif name=="assess-transfer":
            q.add_argument("--case-id",required=True)
            q.add_argument("--setting-id",required=True)
            q.add_argument("--material-ref",action="append",default=[])
        elif name=="resume":
            g=q.add_mutually_exclusive_group(required=True);g.add_argument("--case-id");g.add_argument("--job-id")
            q.add_argument("--stage",choices=["extraction","identity","research"]);q.add_argument("--material-ref",action="append",default=[]);q.add_argument("--material-file",action="append",default=[])
            q.add_argument("--approve",action="store_true");q.add_argument("--retry-transport",action="store_true");q.add_argument("--repair-protocol",action="store_true");q.add_argument("--continue-budget",action="store_true")
        elif name=="export":q.add_argument("--case-id",required=True);q.add_argument("--out",required=True)
        elif name=="import-source":q.add_argument("--file",required=True)
        elif name=="mcp":q.add_argument("--job",required=True)
    return p


def doctor(config):
    from .runtime.instructions import load_instructions
    from .core.contracts import schema
    results=[]
    for role in MAIN_KINDS:
        text,manifest=load_instructions(role)
        results.append({"role":role,"instructions_chars":len(text),"loaded_files":len(manifest["loaded"]),"skills":len(manifest["skills"])})
    return {"resources_root":str(resources_root()),"agents":results,"schema_files":len(list((resources_root()/"schemas").glob("*.json"))),"backend":config.get("backend","responses"),"model":config.get("model",{}).get("model"),"api_key_present":bool(os.getenv(config.get("model",{}).get("api_key_env","OPENAI_API_KEY"))),"live_model_test":False}


def export_case(engine,case_id,out):
    from .exports import render_profile
    case=engine.ws.case(case_id); target=Path(out).resolve();target.mkdir(parents=True,exist_ok=True)
    atomic_json(target/"case.json",case)
    refs=set()
    if case.get("proposal_ref"):
        proposal=engine.artifacts.get(case["proposal_ref"])["data"]
        prepared=engine.artifacts.get(proposal["prepared_ref"])["data"]
        for name,data in prepared["files"].items():atomic_json(target/name,data)
        (target/"profile.md").write_text(render_profile(prepared["files"]["profile.json"]),encoding="utf-8")
        refs.add(case["proposal_ref"])
    for key in ["candidate_ref","identity_ref","extraction_review_ref","identity_review_ref","research_ref","profile_review_ref","receipt_ref"]:
        if case.get(key):refs.add(case[key])
    # Portable evidence package: export the complete archive without making it a single model input.
    pending=list(refs);seen=set()
    while pending:
        ref=pending.pop()
        if ref in seen:continue
        seen.add(ref);obj=engine.artifacts.get(ref)
        atomic_json(target/"evidence"/(ref[7:]+".json"),obj)
        pending.extend(obj["dependencies"])
    note=("This directory is a portable archive, not a model input package.\n"
          f"Case status: {case['state']}.\n"
          "Ingestion is complete only when receipt_ref exists and the state is committed; other files may still be proposals.\n")
    (target/"REPORT.md").write_text(note,encoding="utf-8")
    return {"directory":str(target),"state":case["state"],"receipt_ref":case.get("receipt_ref"),"artifact_count":len(seen)}


def main(argv=None):
    args=build_parser().parse_args(argv)
    try:
        if args.command=="init":
            dest=Path(args.config).resolve()
            if dest.exists():raise ProtocolError("The configuration file already exists; edit it or choose another path")
            template=(resources_root()/"config"/"example.toml").read_text(encoding="utf-8")
            template=template.replace('atlas = "./atlas"','atlas = '+json.dumps(str(Path(args.atlas).resolve())))
            template=template.replace('workspace = "./work"','workspace = '+json.dumps(str(Path(args.workspace).resolve())))
            template=template.replace('backend = "responses"','backend = '+json.dumps(args.backend))
            template=template.replace('model = ""','model = '+json.dumps(args.model))
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(template,encoding="utf-8")
            print_json({"config":str(dest),"message":"Check the approved task catalog and model ID before running doctor/scan"});return
        config=load_config(args.config)
        if args.command=="doctor":print_json(doctor(config));return
        if args.command=="mcp":
            from .tools.server import serve
            asyncio.run(serve(config,args.job));return
        backend=LazyBackend(config);bridge=None
        if config.get("mcp") and config.get("backend","responses")=="responses" and args.command not in {"status","export","approve-task","import-source"}:
            from .providers.mcp import MCPBridge
            bridge=MCPBridge(config["mcp"])
        engine=Engine(config,backend,bridge=bridge)
        try:
            if args.command=="scan":out=engine.scan({"task_ids":args.task,"years":args.year,"sources":args.source or ["arxiv","crossref","openalex"],"query_budget":args.query_budget,"paper_limit":args.paper_limit,"event_kind":args.event_kind,"notes":args.notes},run_label=args.run_label)
            elif args.command=="run-paper":
                ref=args.paper_ref or engine.put("paper",json.loads(Path(args.paper_json).read_text()) if args.paper_json else seed_paper(args.url,args.title))
                materials=args.research_material_ref+[import_source(engine,p,material_role="unreviewed_research") for p in args.research_material_file]
                out=engine.process_paper(ref,research_material_refs=materials)
            elif args.command=="scout-tasks":out=engine.task_scout(args.notes,args.material_ref)
            elif args.command=="approve-task":out=engine.approve_task(args.proposal_ref,args.task_id)
            elif args.command=="status":out={"counts":engine.counts(),"cases":engine.ws.query("SELECT id,paper_ref,candidate_ref,state FROM cases"),"jobs":engine.ws.query("SELECT id,role,status FROM jobs ORDER BY created")}
            elif args.command=="reprepare":out=engine.reprepare_case(args.case_id)
            elif args.command=="assess-transfer":
                out=engine.assess_transfer(args.case_id,args.setting_id,material_refs=args.material_ref)
            elif args.command=="resume":
                if args.job_id:
                    job=engine.runner.run(args.job_id,validate_output=engine._validate_stage,retry_transport=args.retry_transport,repair_protocol=args.repair_protocol,continue_budget=args.continue_budget)
                    out={"job_id":job["id"],"status":job["status"],"output":job["output"],"next":"Continue the related case with resume --case-id"}
                else:
                    refs=args.material_ref+[import_source(engine,p) for p in args.material_file]
                    out=engine.resume_case(args.case_id,stage=args.stage,material_refs=refs,approve=args.approve)
            elif args.command=="export":out=export_case(engine,args.case_id,args.out)
            elif args.command=="import-source":out={"source_ref":import_source(engine,args.file)}
            else:raise ProtocolError("Unknown command")
            print_json(out)
        finally:
            backend.close()
            if bridge:bridge.close()
            engine.ws.close()
    except (ProtocolError,ValueError,RuntimeError,OSError) as exc:
        print(json.dumps({"error_type":type(exc).__name__,"message":str(exc)},ensure_ascii=False),file=sys.stderr)
        raise SystemExit(2)
