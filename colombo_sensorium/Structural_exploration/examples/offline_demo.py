"""Offline synthetic acceptance: one fixture exercises three actual orchestration branches: adding bounds, a new view, and a new setting.

No models or network are called. In this example only, ScriptedBackend supplies predetermined scientific judgments to drive the actual
ToolHost, schemas, independent jobs, drafts, Atlas retrieval, and five-file transactions. This verifies software integration;
it is not scientific acceptance of real papers or a real LLM, and the example Atlas must not be used as a production Atlas.

Run: python examples/offline_demo.py --output /tmp/oracle-atlas-offline-demo
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT / "src"))

from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.store import dumps
from oracle_atlas.providers.base import Reply, ToolCall
from oracle_atlas.workflow.engine import Engine

_SYNTHETIC_SPEC = importlib.util.spec_from_file_location("offline_synthetic_contracts", Path(__file__).with_name("synthetic_contracts.py"))
SYNTHETIC = importlib.util.module_from_spec(_SYNTHETIC_SPEC)
_SYNTHETIC_SPEC.loader.exec_module(SYNTHETIC)

NOTICE = "Offline synthetic acceptance: no real LLM or network was called; receipts verify only software integration and add no findings from real literature."
SOURCE_VERSION = "synthetic-three-branches-v1"
SOURCE_TEXT = """SYNTHETIC FIXTURE — NOT A PUBLISHED PAPER.
Case A: Let a be an unknown bit. Minimize f_a(x)=1{x!=a} over {0,1}; one exact value query is charged.
One query determines a. No zero-query deterministic output is correct on both a=0 and a=1.
Case B: Let a be in {-1,+1}. Minimize f_a(x)=a*x over [0,1]; one exact value query is charged.
One query at x=1 determines a. The minimizers are 0 and 1 for the two signs.
For a randomized zero-query algorithm the two disjoint success events cannot both have probability at least 2/3.
Case C: Let a be an unknown bit. Minimize f_a(x)=(x-a)^2 over R using a gradient-only exact oracle.
One query at 0 returns -2a and recovers the minimizer. Zero-query deterministic recovery fails on one of the two inputs.
These toy examples exist solely to test orchestration, references, review separation, and transaction receipts.
"""

CASES = {
    "fill_bound": {"setting_id": "DEMO_BINARY_VALUE", "title": "[SYNTHETIC] Binary-domain minimization with exact values", "formulation": "Minimize f_a(x)=1{x!=a} over x in {0,1}, with hidden a in {0,1}.", "model": "The two explicitly declared functions on the two-point domain; no extension is promised.", "domain": "{0,1}", "oracle": "function_value", "returns": ["value"], "view": "deterministic", "model_tag": "two_point_domain", "source_case": "Case A"},
    "add_view": {"setting_id": "DEMO_SIGNED_LINEAR", "title": "[SYNTHETIC] Signed-linear minimization with exact values", "formulation": "Minimize f_a(x)=a*x over [0,1], with hidden a in {-1,+1}.", "model": "Two linear objectives on the known interval [0,1]; the coefficient is hidden.", "domain": "[0,1]", "oracle": "function_value", "returns": ["value"], "view": "randomized", "model_tag": "interval", "source_case": "Case B"},
    "new_setting": {"setting_id": "DEMO_QUADRATIC_GRADIENT", "title": "[SYNTHETIC] Two-shift quadratic minimization with gradients only", "formulation": "Minimize f_a(x)=(x-a)^2 over R, with hidden a in {0,1}.", "model": "The two specified quadratic objectives on the real line; only the shift is hidden.", "domain": "R", "oracle": "gradient_only", "returns": ["gradient"], "view": "deterministic", "model_tag": "euclidean", "source_case": "Case C"},
}


def view(vid):
    random = vid == "randomized"
    return {"view_id": vid, "label": "Randomized" if random else "Deterministic",
            "algorithms": {"randomization": "randomized_allowed" if random else "deterministic", "adaptivity": "sequential_adaptive", "restrictions": []},
            "guarantees": [{"guarantee_id": "g_" + vid, "quantifiers": "one_algorithm_for_every_instance", "error": "P(gap=0)>=2/3" if random else "gap=0 for every instance", "cost": "One fixed worst-case query budget on every path."}],
            "specification_overrides": {}, "alias_ids": []}


def specification(case, source_ref):
    statements = {
        "task": case["formulation"], "model": case["model"],
        "oracle": "A query at any point of the declared domain returns " + ", ".join(case["returns"]) + " exactly; no other unknown-instance access is allowed.",
        "algorithms": "Sequential adaptive algorithms; the permitted randomization is specified by the view. Internal computation is unrestricted and uncharged.",
        "output": "Output a minimizer in " + case["domain"] + ". It may be an unqueried point. No auxiliary value or certificate is required.",
        "metric": "The base loss is ell(a,x)=f_a(x)-min_u f_a(u), with exact target ell(a,x)=0.",
        "guarantee": "A single algorithm must meet the view's error guarantee separately for every hidden a; cost uses a deterministic worst-case cap.",
        "resource": "One primitive reply costs one query. Computation on public information and past replies is free; no additional hidden-instance operation is free.",
    }
    result = {}
    for axis, text in statements.items():
        result[axis] = {"summary": text, "statements": [{"id": axis + "_statement", "text": text, "status": "known", "object_ref": "f", "variable_block_ref": "x", "norm_ref": None, "domain_ref": "declared_domain", "view_ref": None, "operation_ref": "query" if axis == "oracle" else None, "evidence_refs": [source_ref]}]}
    result["task"]["navigation_domains"] = ["single_objective"]
    result["oracle"].update({"public_inputs": ["the two-function family", "the domain"], "hidden_objects": ["f"], "operations": [{"id": "query", "operation_code": case["oracle"], "target_object": "f", "returns": case["returns"], "query_signature": "x in " + case["domain"], "feedback_quality": {"code": "exact"}, "role": "unknown_object_primitive", "cost_rule_ref": "one_query"}]})
    return result


def tag_facts(case, vid):
    values = {"TASK": ("task_family", "single_objective"), "MODEL": ("geometry", case["model_tag"]), "ORACLE": ("operation", case["oracle"]), "ALGORITHMS": ("randomization", "private_randomness_allowed" if vid == "randomized" else "deterministic"), "OUTPUT": ("object", "minimizer"), "METRIC": ("criterion", "objective_gap"), "GUARANTEE": ("mode", "probability" if vid == "randomized" else "deterministic"), "RESOURCE": ("measure", "oracle_calls")}
    facts = []
    for axis, (group, value) in values.items():
        facts.append({"concept_id": f"{axis}:{group}:{value}", "axis": axis, "value": value, "object_ref": "f" if axis == "ORACLE" else None, "view_ref": vid if axis in {"ORACLE", "ALGORITHMS", "GUARANTEE"} else None, "operation_ref": "query" if axis == "ORACLE" else None, "source_pointer": "/common_specification/oracle/operations/0" if axis == "ORACLE" else f"/common_specification/{axis.lower()}/summary", "status": "known"})
    return facts


def candidate(branch, paper_ref, source_ref):
    case = CASES[branch]
    return {"candidate_id": "demo_" + branch, "title": case["title"], "paper_refs": [paper_ref], "common_specification": specification(case, source_ref), "views": [view(case["view"])], "tag_facts": tag_facts(case, case["view"]), "issues": [], "synthetic_branch": branch}


def base_profile(branch, source_ref, *, initial=False):
    case = CASES[branch]
    vid = "deterministic" if initial else case["view"]
    sid = case["setting_id"]
    p = {"schema_version": "1.0.0", "setting_id": sid, "title": case["title"], "primary_domain": "single_objective", "summary": "Synthetic software fixture. This profile is not a literature survey.", "common_specification": specification(case, source_ref), "views": [view(vid)], "parameters": [], "symbols": [], "quantities": [{"id": "q", "description": "Worst-case charged primitive queries for the declared guarantee."}], "resource_projections": [{"id": "rp", "expression": "N"}], "regimes": [{"id": "r", "description": "The complete two-instance toy family."}], "bounds": [], "comparisons": [], "bracket_rows": [], "summary_status": {"label": "Missing bounds", "coverage": "Synthetic fixture only."}, "proofs": [], "evidence": [], "references": [{"id": "synthetic_fixture", "source_ref": source_ref, "label": "Synthetic fixture, not a paper."}], "facets": [], "relations": [], "aliases": [{"legacy_id": sid + "_det", "view_id": "deterministic"}], "provenance": {"synthetic": True, "source_snapshot": SOURCE_VERSION}}
    if initial:
        p["bounds"].append(bound("upper", vid, []))
        if branch == "add_view":
            p["bounds"].append(bound("lower", vid, []))
        p["comparisons"] = [comparison(sid, vid, lower=branch == "add_view")]
        p["summary_status"]["label"] = "All optimal" if branch == "add_view" else "Missing bounds"
    return SYNTHETIC.complete_synthetic_profile(p) if initial else p


def bound(direction, vid, evidence_refs, proof_refs=()):
    return {"id": f"{vid}_{direction}", "direction": direction, "view_id": vid, "guarantee_id": "g_" + vid, "quantity_ref": "q", "region_refs": ["r"], "formula_latex": "1", "witness_type": "deterministic" if direction == "upper" else None, "algorithm_scope": "All declared algorithms in this view, with the stated per-instance guarantee.", "eligible_for_bracket": True, "included_in_bracket": True, "origin": "analyst_derivation", "evidence_refs": list(evidence_refs), "proof_refs": list(proof_refs), "synthetic": True}


def comparison(sid, vid, *, lower=True):
    return {"comparison_id": "comparison_" + vid, "comparison_key": {"setting_id": sid, "view_id": vid, "guarantee_id": "g_" + vid, "quantity_id": "q", "resource_projection_id": "rp", "regime_id": "r"}, "bracket": {"upper_refs": [vid + "_upper"], "lower_refs": [vid + "_lower"] if lower else []}, "status": {"code": "optimal" if lower else "missing_lower", "label": "Optimal" if lower else "Lower bound missing", "missing_sides": [] if lower else ["lower"]}}


class SyntheticBibliography:
    """Inject local fixtures only, without network operations."""
    def __init__(self, record):
        self.record = deepcopy(record)
        self.calls = 0

    def search(self, provider, query, year=None, limit=20, cursor=None):
        self.calls += 1
        return {"provider": "synthetic_fixture", "query": query, "year": year, "records": [deepcopy(self.record)], "next_cursor": None, "coverage": "One explicitly synthetic local fixture; no literature coverage claim."}


class ScriptedBackend:
    """Local protocol simulator; predetermined answers remain in examples and never enter production prompts."""
    def __init__(self):
        self.sessions = {}
        self.current_job = None
        self.calls = 0
        self.calls_by_role = Counter()
        self.observed_tool_errors = []
        self.review_memory = []

    def bind_job(self, job, config):
        self.current_job = deepcopy(job)
        self.workspace_path = Path(config["workspace"])
        if job["id"] not in self.sessions:
            self.sessions[job["id"]] = {"program": self._program(deepcopy(job)), "pending": None, "started": False, "sequence": 0}

    def complete(self, instructions, input_items, tools, output_schema):
        job = self.current_job
        session = self.sessions[job["id"]]
        self.calls += 1
        self.calls_by_role[job["role"]] += 1
        delivered = {item["call_id"]: json.loads(item["output"]) for item in input_items if item.get("type") == "function_call_output"}
        try:
            if not session["started"]:
                action = next(session["program"])
                session["started"] = True
            else:
                if session["pending"] not in delivered:
                    # The longer protocol triggers bounded continuation; a real model resumes using work_list/drafts.
                    # The fixed generator cannot replan; it consumes only the same persisted, completed tool receipt for this job.
                    # This is an offline fixture adaptation, without reading other jobs or supplying scientific conclusions for real research.
                    rotated = any('"resume_segment"' in str(item.get("content", "")) for item in input_items)
                    if not rotated:
                        raise RuntimeError("Synthetic tool response missing without a recorded context rotation")
                    import sqlite3
                    with sqlite3.connect(self.workspace_path / "state.sqlite3") as db:
                        row=db.execute("SELECT result FROM tool_calls WHERE id=? AND job=? AND status='done'",(job["id"]+":"+session["pending"],job["id"])).fetchone()
                    if not row:raise RuntimeError("Synthetic continuation has no persisted tool receipt")
                    response=json.loads(row[0])
                else:
                    response = delivered[session["pending"]]
                if "error_type" in response:
                    self.observed_tool_errors.append({"role": job["role"], "result": response})
                    raise RuntimeError(f"Synthetic driver exposed a tool error: {response}")
                action = session["program"].send(response)
        except StopIteration as done:
            text = dumps(done.value)
            return Reply(output_items=[{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": text}]}], text=text, response_id=f"synthetic:{job['id']}:final")
        name, arguments = action
        if name not in {t["name"] for t in tools}:
            raise RuntimeError(f"Synthetic driver requested unavailable tool {name}")
        session["sequence"] += 1
        call_id = f"synthetic_{session['sequence']}"
        session["pending"] = call_id
        return Reply(output_items=[{"type": "function_call", "name": name, "arguments": dumps(arguments), "call_id": call_id}], calls=[ToolCall(name, arguments, call_id)], response_id=f"synthetic:{job['id']}:{session['sequence']}")

    def _call(self, name, **args):
        response = yield name, args
        return response

    def _read(self, ref, pointer=""):
        offset, chunks = 0, []
        while True:
            result = yield from self._call("artifact_get", ref=ref, pointer=pointer, offset=offset, limit=10000)
            if "data" in result:
                return result["data"]
            chunks.append(result["text"])
            if result["next_offset"] is None:
                text = "".join(chunks)
                try:
                    return json.loads(text)
                except ValueError:
                    return text
            offset = result["next_offset"]

    def _put(self, kind, data, dependencies=()):
        response = yield from self._call("artifact_put", kind=kind, json_text=dumps(data), dependencies=list(dependencies))
        return response["ref"]

    def _draft_profile(self, p, clone_source=None, baseline=None):
        if clone_source:
            draft = yield from self._call("draft_clone", **clone_source)
            patches=[]
            for key,value in p.items():
                if key in baseline and baseline[key]==value:
                    continue
                path="/"+key.replace("~","~0").replace("/","~1")
                old=baseline.get(key)
                if isinstance(old,list) and isinstance(value,list) and value[:len(old)]==old:
                    patches.extend({"op":"add","path":path+"/-","value":item} for item in value[len(old):])
                else:
                    patches.append({"op":"replace" if key in baseline else "add","path":path,"value":value})
            if patches:
                yield from self._call("draft_patch",draft_id=draft["draft_id"],revision=draft["revision"],patches_json=dumps(patches))
            yield from self._call("draft_validate",draft_id=draft["draft_id"],tag_facts_json="")
            frozen=yield from self._call("draft_freeze",draft_id=draft["draft_id"])
            return frozen["ref"]
        # Write the profile in specification and scientific-result chunks; freeze performs full schema validation.
        arrays = {key: p[key] for key in ("bounds", "comparisons", "bracket_rows", "proofs", "evidence", "references")}
        initial = {key: value for key, value in p.items() if key not in arrays}
        draft = yield from self._call("draft_create", kind="profile", initial_json=dumps(initial))
        patched = yield from self._call("draft_patch", draft_id=draft["draft_id"], revision=draft["revision"], patches_json=dumps([{"op": "add", "path": "/" + key, "value": value} for key, value in arrays.items()]))
        yield from self._call("draft_read", draft_id=draft["draft_id"], pointer="/summary_status", offset=0, limit=1000)
        if patched["revision"] != draft["revision"] + 1:
            raise RuntimeError("Draft revision did not advance")
        frozen = yield from self._call("draft_freeze", draft_id=draft["draft_id"])
        return frozen["ref"]

    def _finish(self, ref):
        return {"status": "complete", "artifact_refs": [ref], "summary": NOTICE, "checkpoint_ref": None}

    def _program(self, job):
        role, inputs = job["role"], job["inputs"]
        main = {"coordinator": "plan", "paper_scanner": "paper_batch", "extractor": "extraction", "matcher": "identity", "bound_updater": "research", "profile_researcher": "research"}.get(role, "review")
        yield from self._call("schema_read", kind=main)
        if role == "coordinator":
            request = yield from self._read(inputs["request_ref"])
            yield from self._read(inputs["catalog_ref"])
            plan = {key: request[key] for key in ("task_ids", "years", "sources", "query_budget", "paper_limit", "notes")}
            return self._finish((yield from self._put("plan", plan)))
        if role == "paper_scanner":
            plan = yield from self._read(inputs["plan_ref"])
            found = yield from self._call("bibliography_search", provider="synthetic_fixture", query="synthetic two-instance oracle minimization", year=plan["years"][0], limit=10, cursor=None)
            batch = {"paper_refs": [x["paper_ref"] for x in found["papers"]], "coverage": {"synthetic": True, "leads": 1, "verified_year_records": 1, "message": NOTICE}, "search_refs": [found["search_ref"]]}
            return self._finish((yield from self._put("paper_batch", batch)))
        if role == "extractor":
            paper = yield from self._read(inputs["paper_ref"])
            source_ref = paper["source_refs"][0]
            yield from self._call("source_read", ref=source_ref, offset=0, limit=10000)
            candidate_refs = []
            for branch in CASES:
                candidate_refs.append((yield from self._put("candidate", candidate(branch, inputs["paper_ref"], source_ref))))
            yield from self._call("memory_save", text="PRIVATE_SYNTHETIC_PRODUCER: extraction finished; this is not a review.", refs=candidate_refs)
            return self._finish((yield from self._put("extraction", {"paper_ref": inputs["paper_ref"], "candidate_refs": candidate_refs})))
        if role == "extraction_reviewer":
            extracted = yield from self._read(inputs["subject_ref"])
            assessments = []
            for ref in extracted["candidate_refs"]:
                item = yield from self._read(ref)
                source_ref = item["common_specification"]["task"]["statements"][0]["evidence_refs"][0]
                yield from self._call("source_read", ref=source_ref, offset=0, limit=10000)
                assessments.append({"subject_id": ref, "verdict": "approve", "reason": "Synthetic script: the fixture's declared specification is copied completely; this is not a live LLM judgment."})
            memory = yield from self._call("memory_search", query="PRIVATE_SYNTHETIC_PRODUCER", limit=5)
            self.review_memory.append(memory)
            review = {"subject_ref": inputs["subject_ref"], "review_type": "extraction", "verdict": "approve", "assessments": assessments, "issues": [], "approved_bound_ids": [], "summary": NOTICE}
            return self._finish((yield from self._put("review", review)))
        if role == "matcher":
            c = yield from self._read(inputs["candidate_ref"])
            yield from self._read(inputs["extraction_review_ref"])
            yield from self._call("atlas_search", candidate_ref=inputs["candidate_ref"], limit=12, offset=0, broaden=False)
            found = yield from self._call("atlas_search", candidate_ref=inputs["candidate_ref"], limit=12, offset=0, broaden=True)
            branch = c["synthetic_branch"]
            sid = CASES[branch]["setting_id"]
            comparisons = []
            for entry in found["candidates"]:
                native = yield from self._call("atlas_read", setting_id=entry["setting_id"], filename="profile.json", pointer="/common_specification", offset=0, limit=10000)
                same = entry["setting_id"] == sid
                comparisons.append({"setting_id": entry["setting_id"], "relation": "same" if same else "different", "reason": "Synthetic fixture: compare the explicit objective family, domain, output, and exact native feedback; randomized permission is a view difference.", "evidence_refs": [native["ref"]]})
            identity = {"candidate_ref": inputs["candidate_ref"], "decision": "new" if branch == "new_setting" else "existing", "setting_id": None if branch == "new_setting" else sid, "view_mapping": [{"candidate_view_id": CASES[branch]["view"], "atlas_view_id": None if branch in {"new_setting", "add_view"} else "deterministic", "reason": "Synthetic fixture: introduce a view only when absent; common task/oracle/model stays fixed."}], "normalization": "No mathematical normalization is assumed; this synthetic test compares exact fixture definitions.", "comparisons": comparisons, "retrieval_ref": found["retrieval_ref"], "recall_audit": {"strategies": ["task_oracle_concepts", "title_formulation", "unknown_retained"], "unresolved_ids": [], "reason": "All two synthetic initial profiles were read; this is not a full literature novelty claim.", "inventory_version": found["inventory_version"]}, "issues": []}
            return self._finish((yield from self._put("identity", identity)))
        if role == "identity_reviewer":
            identity = yield from self._read(inputs["subject_ref"])
            yield from self._read(inputs["candidate_ref"])
            for row in identity["comparisons"]:
                for ref in row["evidence_refs"]:
                    yield from self._read(ref, "/content/common_specification")
            review = {"subject_ref": inputs["subject_ref"], "review_type": "identity", "verdict": "approve", "assessments": [{"subject_id": inputs["subject_ref"], "verdict": "approve", "reason": "Synthetic scripted identity review of separately frozen material."}], "issues": [], "approved_bound_ids": [], "summary": NOTICE}
            return self._finish((yield from self._put("review", review)))
        if role in {"bound_updater", "profile_researcher"}:
            return (yield from self._research(inputs))
        if role == "profile_reviewer":
            yield from self._call("schema_read", kind="joint_analysis")
            proposal = yield from self._read(inputs["subject_ref"])
            p = yield from self._read(proposal["profile_ref"])
            prepared = yield from self._read(proposal["prepared_ref"])
            research = yield from self._read(proposal["research_ref"])
            for ref in research["result_refs"] + research["proof_refs"]:
                yield from self._read(ref)
            memory = yield from self._call("memory_search", query="PRIVATE_SYNTHETIC_PRODUCER", limit=5)
            self.review_memory.append(memory)
            approved = [b["id"] for b in p["bounds"] if b.get("eligible_for_bracket")]
            review = {"subject_ref": inputs["subject_ref"], "review_type": "profile", "verdict": "approve", "assessments": [{"subject_id": bid, "verdict": "approve", "reason": "Synthetic software acceptance only; no live reviewer was queried."} for bid in approved], "issues": [], "approved_bound_ids": approved, "summary": NOTICE}
            review["joint_review"] = SYNTHETIC.synthetic_joint_review(prepared)
            from oracle_atlas.workflow.coverage import CHECKS
            review["coverage_audit"]={"scope":NOTICE,"checks":[{"check_id":k,"scope":"synthetic toy domain only","status":"not_applicable","reason":NOTICE,"result_refs":[],"proof_refs":[]} for k in CHECKS],"resolved_issue_ids":[],"carried_issue_ids":[],"new_blocker_justifications":[],"followups":[],"reuse_context_ref":inputs.get("review_context_ref"),"reused_bound_ids":[]}
            review.update(proof_approvals=[],proof_issue_scopes=[],proof_reuse_context_ref=None,reused_proof_refs=[])
            return self._finish((yield from self._put("review", review)))
        raise RuntimeError(f"Unsupported synthetic role {role}")

    def _research(self, inputs):
        yield from self._call("schema_read", kind="joint_analysis")
        c = yield from self._read(inputs["candidate_ref"])
        yield from self._read(inputs["identity_ref"])
        branch = c["synthetic_branch"]
        case = CASES[branch]
        source_ref = c["common_specification"]["task"]["statements"][0]["evidence_refs"][0]
        yield from self._call("source_read", ref=source_ref, offset=0, limit=10000)
        if inputs.get("base_profile_ref"):
            native = yield from self._read(inputs["base_profile_ref"])
            p = native["content"]
        else:
            p = base_profile(branch, source_ref)
        baseline=json.loads(dumps(p))
        vid = case["view"]
        if branch == "add_view":
            p["views"].append(view(vid))
            p["aliases"].append({"legacy_id": p["setting_id"] + "_rand", "view_id": vid})
        proof = {"proof_id": "proof_" + branch, "origin": "analyst_derivation", "proposition": "In this explicitly synthetic two-instance model, exactly one oracle call is necessary and sufficient.", "premises": [case["formulation"], "The native oracle and fixed worst-case cost are exactly those of the candidate."], "argument": "For A, one value at 0 identifies the hidden bit. For B, one value at 1 identifies the sign. For C, one gradient at 0 equals -2a and identifies the shift. Without queries the transcript is identical on the two inputs, whose sets of exact minimizers are disjoint. A deterministic output cannot solve both; under a fixed randomized seed distribution the two disjoint success events have probabilities summing to at most one, so they cannot both reach 2/3.", "boundary_cases": "Only the two declared distinct inputs are in scope. The zero-query case is handled explicitly; no asymptotic claim is made.", "quantifiers": "One algorithm works separately on each fixed input. Randomness, when allowed, is independent of the input. The lower bound uses a fixed worst-case query budget.", "resource_accounting": "The upper algorithm makes one charged primitive query; postprocessing uses only public information and that reply.", "dependencies": [source_ref], "issues": []}
        proof_ref = yield from self._put("proof", proof)
        result_refs = []
        directions = ["lower"] if branch == "fill_bound" else ["upper", "lower"]
        for direction in directions:
            card = {"result_id": f"result_{branch}_{direction}", "comparison_key": {"setting_id": case["setting_id"], "view_id": vid, "guarantee_id": "g_" + vid, "quantity_id": "q", "resource_projection_id": "rp", "regime_id": "r"}, "direction": direction, "statement": "Synthetic fixture: one call is " + ("sufficient." if direction == "upper" else "necessary."), "formula_latex": "1", "conditions": [case["model"], "Exact minimization and the declared native oracle."], "parameter_region": "The full two-input fixture.", "algorithm_scope": "All declared algorithms in the selected view; no span restriction.", "witness_type": "deterministic" if direction == "upper" else None, "guarantee": "Per-instance success at least 2/3." if vid == "randomized" else "Exact minimization on every input.", "resource_accounting": "One charged primitive call; fixed worst-case budget.", "origin": "analyst_derivation", "source_refs": [source_ref], "source_locators": [{"source_ref": source_ref, "version": SOURCE_VERSION, "locator": case["source_case"]}], "proof_refs": [proof_ref], "status": "proposed", "issues": []}
            result_ref = yield from self._put("result", card)
            result_refs.append(result_ref)
            p["bounds"].append(bound(direction, vid, [result_ref], [proof_ref]))
        if branch == "fill_bound":
            p["comparisons"] = [comparison(p["setting_id"], vid)]
        else:
            p["comparisons"].append(comparison(p["setting_id"], vid))
        p["bracket_rows"] = [{"row_id": "closed", "comparison_ids": [x["comparison_id"] for x in p["comparisons"]], "view_ids": [v["view_id"] for v in p["views"]]}]
        p["summary_status"] = {"label": "All optimal", "coverage": "Synthetic toy fixture only; no literature coverage claim."}
        p["proofs"].append({"proof_id": proof["proof_id"], "artifact_ref": proof_ref, "origin": "analyst_derivation"})
        p["evidence"].extend({"id": "evidence_" + str(i), "artifact_ref": ref} for i, ref in enumerate(result_refs))
        p = SYNTHETIC.complete_synthetic_profile(p, baseline=baseline if inputs.get("base_profile_ref") else None,
                                               proof_argument=proof["argument"])
        profile_ref = yield from self._draft_profile(p,inputs.get("profile_clone_source"),baseline)
        yield from self._call("memory_save", text="PRIVATE_SYNTHETIC_PRODUCER: result cards and formal toy proof saved. They are not adopted until fresh review.", refs=[profile_ref, proof_ref, *result_refs])
        research = {"candidate_ref": inputs["candidate_ref"], "identity_ref": inputs["identity_ref"], "action": "new" if branch == "new_setting" else "update", "setting_id": p["setting_id"], "base_version": inputs.get("base_version"), "profile_ref": profile_ref, "result_refs": result_refs, "proof_refs": [proof_ref], "issues": [], "change_summary": {"fill_bound": "Synthetic fixture: add the missing lower bound to the existing deterministic bracket.", "add_view": "Synthetic fixture: add a randomized view to the existing profile; deterministic witnesses remain recorded as deterministic.", "new_setting": "Synthetic fixture: create the distinct gradient-only two-shift problem."}[branch]}
        from oracle_atlas.workflow.coverage import CHECKS
        research["coverage_ledger"]={"scope":NOTICE,"checks":[{"check_id":k,"scope":"synthetic toy domain only","status":"not_applicable","reason":NOTICE,"result_refs":[],"proof_refs":[]} for k in CHECKS],"issue_resolutions":[]}
        research["research_scope"] = SYNTHETIC.synthetic_research_scope()
        return self._finish((yield from self._put("research", research)))


def setup_demo(output: Path):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    backend = ScriptedBackend()
    cfg = {"workspace": str(output / "work"), "atlas": str(output / "atlas"), "model": {"model": "synthetic-scripted-backend"}, "budgets": {**DEFAULTS, "max_total_calls": 300, "max_turns": 90, "max_segments": 16, "max_jobs": 40}, "publication": {"require_human_approval": False}, "tasks": [{"task_id": "synthetic_minimization", "label": "Synthetic oracle minimization fixture", "queries": ["synthetic two-instance oracle minimization"], "approved": True}]}
    engine = Engine(cfg, backend)
    source_ref = engine.put("source", {"url": "urn:oracle-atlas:synthetic:three-branches-v1", "version": SOURCE_VERSION, "content_hash": hashlib.sha256(SOURCE_TEXT.encode()).hexdigest(), "text": SOURCE_TEXT, "metadata": {"synthetic": True, "notice": NOTICE}})
    for branch in ("fill_bound", "add_view"):
        p = base_profile(branch, source_ref, initial=True)
        if engine.atlas.version(p["setting_id"]) is None:
            prepared = engine.atlas.prepare(p, tag_facts(CASES[branch], "deterministic"), None)
            engine.atlas.commit(prepared, {"verdict": "approve", "prepared_hash": prepared["bundle_hash"], "approved_bound_ids": [b["id"] for b in p["bounds"]], "issues": [], "synthetic_seed": True, "joint_review": SYNTHETIC.synthetic_joint_review(prepared)}, "synthetic-seed:" + p["setting_id"])
    record = {"title": "[SYNTHETIC] Three two-instance oracle cases for workflow verification", "doi": None, "arxiv_id": None, "urls": ["urn:oracle-atlas:synthetic:three-branches-v1"], "source_refs": [source_ref], "publication_events": [{"event_id": "synthetic-publication-event", "kind": "publication", "year": 2026, "date": "2026-01-01", "verified": True, "verification_sources": ["synthetic-fixture-provenance"], "source_refs": ["synthetic-fixture-provenance"], "synthetic": True}], "provenance": [{"source_id": "synthetic-fixture-provenance", "provider": "offline_fixture", "url": "urn:oracle-atlas:synthetic:three-branches-v1", "synthetic": True}], "synthetic": True}
    bibliography = SyntheticBibliography(record)
    engine.runner.bibliography = bibliography
    request = {"task_ids": ["synthetic_minimization"], "years": [2026], "sources": ["synthetic_fixture"], "query_budget": 1, "paper_limit": 1, "event_kind": "publication", "notes": NOTICE}
    return engine, backend, bibliography, request


def run_demo(output: Path) -> dict:
    engine, backend, bibliography, request = setup_demo(output)
    first = engine.scan(request)
    calls_before = backend.calls
    versions_before = {row["setting_id"]: row["profile_version"] for row in engine.atlas.catalog()}
    second = engine.scan(request)
    cases = [engine.ws.case(cid) for cid in first["cases"]]
    report = {"notice": NOTICE, "synthetic": True, "real_model_calls": 0, "network_calls": 0, "run_id": first["run_id"], "first_run": first, "second_run_counts": second.get("counts"), "scripted_backend_calls": backend.calls, "repeat_added_calls": backend.calls - calls_before, "bibliography_fixture_calls": bibliography.calls, "calls_by_role": dict(backend.calls_by_role), "cases": cases, "receipt_refs": [case["receipt_ref"] for case in cases if case.get("receipt_ref")], "versions_unchanged_on_repeat": versions_before == {row["setting_id"]: row["profile_version"] for row in engine.atlas.catalog()}, "tool_errors": backend.observed_tool_errors, "reviewer_private_memory_hits": backend.review_memory}
    report["synthetic_budget_note"] = "This fixed scripted fixture explicitly allows 16 segments and 90 turns per job to traverse the current science contracts. The 60000-character input cap and finite call/job limits remain enforced; production defaults are unchanged."
    (Path(output) / "offline_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    engine.ws.db.close()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Output directory for synthetic acceptance only; do not point to a production Atlas")
    args = parser.parse_args()
    report = run_demo(args.output)
    print(NOTICE)
    print(json.dumps({"counts": report["first_run"].get("counts"), "receipt_count": len(report["receipt_refs"]), "repeat_added_calls": report["repeat_added_calls"], "report": str((args.output / "offline_report.json").resolve())}, ensure_ascii=False, indent=2))
    if len(report["receipt_refs"]) != 3 or report["repeat_added_calls"] or report["tool_errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
