"""Role-scoped MCP operations. Only the controller promotes reviewed progress."""
from __future__ import annotations
import json
import math
import re
import sys
import uuid
from typing import Annotated, Literal

from pydantic import Strict, WithJsonSchema

from colombo.brain.submission_validation import ContractError, validate_semantics
from colombo.brain.record_formats import PLAN, OBSERVATION, INTEGRATION, REVIEW
from colombo.brain.cell_evidence import RECORD_REF_SCHEMA

from colombo.shared.file_io import Path, atomic_write, freeze_json
from colombo.brain.research_store import Store

CellRecordRef = Annotated[dict, WithJsonSchema(RECORD_REF_SCHEMA)]


# Publish the existing paging contract without adding coercion or validators.
ReadOffset = Annotated[int, WithJsonSchema({"type": "integer", "minimum": 0})]
ResearchLimit = Annotated[int, WithJsonSchema({"type": "integer", "minimum": 1, "maximum": 50})]
MaterialLimit = Annotated[int, WithJsonSchema({"type": "integer", "minimum": 1, "maximum": 32000})]
ReviewOffset = Annotated[ReadOffset, Strict()]
ReviewLimit = Annotated[ResearchLimit, Strict()]
LookupLimit = Annotated[int, Strict(), WithJsonSchema({"type": "integer", "minimum": 1})]


def _lookup_sources(query, url, limit, *, settings, search_enabled):
    """Use the same provider client as Cell without modifying task environment."""
    from colombo.shared.literature_access import lookup_with_context
    return lookup_with_context(query=query, url=url, limit=limit,
                               settings=settings, search_enabled=search_enabled)




class AgentService:
    def __init__(self, run_root, role, stage, call_id):
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}", call_id):
            raise ValueError("Invalid call ID")
        self.store = Store(Path(run_root))
        self.version = self.store.get_meta("config").get("workflow", {}).get("version", 1)
        if self.version != 3:
            raise ValueError("Unsupported workflow version; current Brain requires workflow version 3")
        allowed_stages = {"brain": {"plan", "process_results", "integrate"}, "verifier": {"verify-progress"}}
        if role not in allowed_stages or stage not in allowed_stages[role]:
            raise ValueError("Invalid role/stage for this run's workflow version")
        self.role, self.stage, self.call_id = role, stage, call_id
        self.work = self.store.root / "brain/calls" / call_id
        self.context = json.loads((self.work / "context.json").read_text(encoding="utf-8"))
        manifest = json.loads((self.work / "call.json").read_text(encoding="utf-8"))
        if any(manifest.get(k) != v for k, v in {"role": role, "stage": stage, "call_id": call_id}.items()):
            raise ValueError("Call identity does not match frozen manifest")
        self.manifest = manifest
        self.allowed = None
        if role == "verifier":
            package_ref = self.context["review_package_ref"]
            package = self.store.read_record(package_ref)
            self.allowed = set(package["allowed_refs"]) | {package_ref["id"] if isinstance(package_ref, dict) else package_ref}

    def _active(self):
        pending = self.store.get_meta("pending_call")
        if not pending or pending.get("call_id") != self.call_id:
            raise ValueError("This call is no longer active")

    def _readable(self, ref):
        record = self.store.record_ref(ref)
        if self.allowed is not None and record["id"] not in self.allowed:
            raise ValueError("Reference is outside the frozen review package")
        return record

    def read_research(self, section="overview", id=None, ref=None, offset=0, limit=20):
        """Navigate domain objects or read one exact authorized version."""
        if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 50:
            raise ValueError("offset must be nonnegative and limit must be an integer from 1 to 50")
        if ref is not None:
            if section != "overview" or id is not None or offset:
                raise ValueError("ref and section/id navigation are mutually exclusive")
            record = self._readable(ref)
            return {"ref": record, "payload": self.store.public_read(record)}
        if self.role != "brain":
            raise ValueError("Verifier must read a fixed ref from its review package")
        from colombo.brain.research_records import research_page
        return research_page(self.store, section, id, offset, limit)

    def read_material(self, ref, path=None, offset=0, limit=12000, record_ref=None):
        record = self._readable(ref)
        limit = min(max(limit, 1), 32000)
        if record_ref is not None:
            from colombo.brain.cell_evidence import read_record_evidence
            return read_record_evidence(self.store, record, path, record_ref, offset, limit)
        material = self.store.read_artifact(record, path, offset, limit)
        return material

    def lookup(self, query="", url="", limit=None):
        """Discover sources or preserve a fetched original as a fixed material."""
        if self.role != "brain":
            raise ValueError("Lookup is available to Brain only")
        self._active()
        config = self.store.get_meta("config")
        enabled = config["brain"].get("search_enabled", False)
        if type(enabled) is not bool:
            raise ValueError("brain.search_enabled must be boolean")
        if not enabled:
            return {"ok": False, "mode": "read" if url else "search", "results": [], "count": 0,
                    "warnings": [], "error": {"kind": "search_disabled",
                    "message": "Lookup is disabled by this run's frozen brain.search_enabled setting."}}
        result = _lookup_sources(query, url, limit, settings=config["cell"]["settings"],
                                 search_enabled=enabled)
        self._active()  # A call can expire while a provider request is in flight.
        if not result.get("ok") or result.get("mode") != "read":
            return result
        sources = result.get("results", [])
        if (len(sources) != 1 or not isinstance(sources[0], dict)
                or not isinstance(sources[0].get("text"), str) or not sources[0]["text"].strip()):
            raise ValueError("A successful source read must contain one nonempty text")
        source = sources[0]
        data = source["text"].encode("utf-8")
        relative = f"input/materials/lookup-{uuid.uuid4().hex}.txt"
        artifact = {"path": relative, "kind": "source_text", "name": "source.txt", "size": len(data)}
        path = self.store.safe_path(relative)
        atomic_write(path, data)
        fields = ("title", "url", "requested_url", "content_type", "content_kind", "metadata", "links",
                  "returned_characters", "downloaded_bytes", "truncated", "truncation_reasons",
                  "last_modified", "retrieved_at", "page_count", "pages_read", "pages_truncated", "read_coverage")
        payload = {"source": source.get("url") or url, "name": source.get("title") or "Retrieved source",
                   "summary": source.get("title") or "Retrieved source text", "provider": result.get("provider"),
                   "call_id": self.call_id, "artifacts": [artifact],
                   "source_info": {key: source[key] for key in fields if key in source},
                   "warnings": result.get("warnings", []), "theorem_text_verified": False}
        try:
            ref = self.store.write_lookup_material(self.call_id, payload)
        except Exception:
            path.unlink(missing_ok=True)
            raise
        return {**result, "material_ref": ref, "artifact": artifact}

    def read_review_package(self, offset=0, limit=20):
        if self.role != "verifier":
            raise ValueError("Only verifier may use this operation")
        return self.store.review_package_view(self.context["review_package_ref"], offset, limit)

    def audit_preflight(self, goal, inputs, record_refs=None, materials=None, request_id=None):
        """Reject invalid input before creating a long-tool worker or reservation."""
        self._active()
        if self.role != "brain":
            raise ValueError("Audit is available to Brain only")
        from colombo.brain.evidence_audit import _input
        binding = None
        if isinstance(inputs, dict) and "prune_relations" in inputs:
            if self.stage != "process_results":
                raise ValueError("Bound pruning audits are available during process_results only")
            from colombo.brain.pruning import prepare_relation_audit
            goal, inputs, binding = prepare_relation_audit(self.store, self.context, goal, inputs)
        _input(self.store, goal, inputs, [] if record_refs is None else record_refs,
               [] if materials is None else materials, binding)
        if request_id is not None and (not isinstance(request_id, str)
                                      or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}", request_id)):
            raise ValueError("Invalid audit request_id")
        return goal, inputs, binding, self._audit_call_budget()

    def audit(self, goal, inputs, record_refs=None, materials=None, request_id=None):
        goal, inputs, binding, call_budget = self.audit_preflight(goal, inputs, record_refs, materials, request_id)
        from colombo.brain.evidence_audit import audit
        return audit(self.store, self.call_id, goal, inputs, record_refs, materials, request_id,
                     _binding=binding, _call_budget=call_budget)

    def _audit_call_budget(self):
        """Use the frozen invocation deadline, never an MCP caller-supplied value."""
        budget = self.context.get("call_budget")
        if "call_budget" in self.manifest:
            if not isinstance(budget, dict):
                raise ValueError("Missing managed call_budget")
            if budget != self.manifest["call_budget"]:
                raise ValueError("call_budget differs from its immutable process manifest")
            deadline = self.manifest.get("deadline_unix")
            if budget.get("deadline_unix") != deadline:
                raise ValueError("call_budget differs from the frozen invocation deadline")
            if deadline is None:
                return None
            if type(deadline) not in (int, float) or not math.isfinite(deadline):
                raise ValueError("Invalid managed deadline")
            from colombo.shared.runtime_budget import context as shared_context
            shared = shared_context(self.store.root)
            if shared and shared.get("work_deadline_unix") is not None:
                deadline = min(deadline, shared["work_deadline_unix"])
            return {"deadline_unix": deadline,
                    "submission_reserve_seconds": budget.get("submission_reserve_seconds", 0)}
        frozen = self.manifest.get("input", {}).get("context", {}).get("call_budget")
        if budget is None and frozen is None:
            return None  # Historical fixtures/contexts retain their original behavior.
        required = {"started_at_unix", "deadline_unix", "timeout_seconds", "audit_timeout_seconds", "submission_reserve_seconds"}
        optional = {"recommended_audit_start_by_unix", "audit_wait_counts_toward_call"}
        numeric = {"started_at_unix", "audit_timeout_seconds", "submission_reserve_seconds"}
        if (not isinstance(budget, dict) or not required <= set(budget) or set(budget) - required - optional
                or any(type(budget[key]) not in (int, float) or not math.isfinite(budget[key]) for key in numeric)):
            raise ValueError("Invalid frozen call_budget")
        if "audit_wait_counts_toward_call" in budget and budget["audit_wait_counts_toward_call"] is not True:
            raise ValueError("Invalid call_budget audit wait accounting")
        from colombo.shared.file_io import json_equal
        if frozen is not None and not json_equal(frozen, budget):
            raise ValueError("call_budget differs from the frozen invocation input")
        started, timeout = self.manifest.get("started_at"), self.manifest.get("timeout_seconds")
        config = self.store.get_meta("config")
        if (type(started) not in (int, float) or not math.isfinite(started)
                or budget["started_at_unix"] != started
                or budget["audit_timeout_seconds"] != config["audit"]["timeout_seconds"]):
            raise ValueError("call_budget is not bound to the parent invocation deadline and audit configuration")
        if timeout == "unlimited":
            if (self.role != "brain" or config["brain"]["timeout_seconds"] != "unlimited"
                    or budget["timeout_seconds"] != "unlimited"
                    or budget["deadline_unix"] is not None
                    or budget["submission_reserve_seconds"] != 0
                    or budget.get("recommended_audit_start_by_unix") is not None):
                raise ValueError("Invalid unlimited call_budget for the parent invocation")
            # The audit keeps its own finite timeout; there is no parent deadline.
            return None
        if any(type(budget[key]) not in (int, float) or not math.isfinite(budget[key])
               for key in ("deadline_unix", "timeout_seconds")):
            raise ValueError("Invalid frozen call_budget")
        if "recommended_audit_start_by_unix" in budget:
            recommended = budget["recommended_audit_start_by_unix"]
            if (type(recommended) not in (int, float) or not math.isfinite(recommended)
                    or recommended != budget["deadline_unix"] - budget["audit_timeout_seconds"] - budget["submission_reserve_seconds"]):
                raise ValueError("Invalid call_budget recommended audit start")
        if (type(timeout) not in (int, float) or not math.isfinite(timeout) or timeout <= 0
                or budget["timeout_seconds"] != timeout
                or budget["deadline_unix"] != started + timeout
                or budget["submission_reserve_seconds"] != min(45, timeout * 0.15)):
            raise ValueError("call_budget is not bound to the parent invocation deadline and audit configuration")
        return {"deadline_unix": budget["deadline_unix"],
                "submission_reserve_seconds": budget["submission_reserve_seconds"]}

    def submit(self, expected_stage, payload):
        self._active()
        if self.role == "brain":
            from colombo.shared.tool_jobs import pending_jobs
            if pending_jobs(self.store.root, owner=self.call_id):
                raise ValueError("Audit jobs are still pending; use job_status before submitting")
        if self.stage != expected_stage:
            raise ValueError("Submission is not valid for this call's stage")
        value = validate_semantics(self.stage, payload, self.store, self.context)
        kind = {"plan": "plan", "process_results": "assessment", "integrate": "assessment", "verify-progress": "review"}[self.stage]
        ref = self.store.write_record(kind, value, request_id="submission:" + self.call_id)
        receipt = {"call_id": self.call_id, "role": self.role, "stage": self.stage, "ref": ref}
        freeze_json(self.work / "submission.json", receipt)
        return {"ref": ref, "status": "submitted", "message": "Saved. End this conversation with this receipt."}

    def format_package_literal(self, ref, path, literal_text, reason):
        self._active()
        if self.role != "brain" or self.stage != "plan":
            raise ValueError("Package formatting is available only to Brain during plan")
        from colombo.brain.cell_package import register_literal_formatting
        return register_literal_formatting(self.store, self._readable(ref), path,
            literal_text, reason, actor={"role": self.role, "call_id": self.call_id})

    def save_note(self, text, related_refs=None, status="open", supersedes=None):
        self._active()
        if (self.role != "brain" or not isinstance(text, str) or not text.strip()
                or not isinstance(status, str) or status not in {"open", "resolved", "abandoned"}):
            raise ValueError("Invalid working note")
        refs = [] if related_refs is None else related_refs
        if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref for ref in refs):
            raise ValueError("related_refs must contain fixed reference IDs")
        for ref in refs:
            self.store.read_record(ref)
        if supersedes is not None:
            if not isinstance(supersedes, str) or not supersedes:
                raise ValueError("supersedes must be a note reference ID")
            if self.store.record_kind(supersedes) != "note":
                raise ValueError("Only a note can be superseded")
        return self.store.write_record("note", {"text": text, "related_refs": refs,
            "status": status, "supersedes": supersedes, "call_id": self.call_id})


def create_server(run_root, role, stage, call_id):
    """Expose just the tools this independent invocation can use."""
    from mcp.server.fastmcp import FastMCP
    service = AgentService(run_root, role, stage, call_id)
    mcp = FastMCP("colombo")

    @mcp.tool()
    def read_research(section: str = "overview", id: str | None = None, ref: str | None = None,
                      offset: ReadOffset = 0, limit: ResearchLimit = 20) -> dict:
        """Read the research overview and the task/wave, proof draft, note, material, and audit catalogs, or use ref to read a pinned version.
        The notes catalog lists each note's current version, brief summary, and links with pagination; read full text and earlier versions using a pinned ref.
        section/id navigation and ref are mutually exclusive; use next to continue reading catalogs and history. The Verifier may supply only refs authorized by the review package.
        """
        return service.read_research(section, id, ref, offset, limit)

    @mcp.tool()
    def read_material(ref: str, path: str | None = None, offset: ReadOffset = 0, limit: MaterialLimit = 12000,
                      record_ref: CellRecordRef | None = None) -> dict:
        """Read the original attachment text authorized by a pinned reference; continue by offset until truncated=false.
        To read a historical Cell record, provide path and record_ref={kind,id,revision}; the latest version is not substituted automatically.
        """
        return service.read_material(ref, path, offset, limit, record_ref)

    if role == "brain":
        from colombo.memory.integration import register_builtin_memory
        register_builtin_memory(mcp, research_mode="oracle_complexity")

        @mcp.tool()
        def lookup(query: str = "", url: str = "", limit: LookupLimit | None = None) -> dict:
            """Search public sources or read one URL; URL takes precedence, limit only controls search count.
            Successful URL reads return text plus material_ref and artifact: select material_ref.id in
            a Cell package or link it in a note. Text is preserved outside research.json; a source is
            not an audited theorem. Search availability comes from this run's brain.search_enabled.
            """
            return service.lookup(query, url, limit)

        @mcp.tool()
        def audit(goal: str, inputs: dict, record_refs: list[str] | None = None,
                  materials: list[dict] | None = None, request_id: str | None = None) -> dict:
            """Start an independent lightweight audit of the supplied inputs only; it does not update progress or stop tasks.
            Use inputs.prune_relations for pruning relations, available only in process_results; do not restart requests whose outcomes are unknown.
            """
            service.audit_preflight(goal, inputs, record_refs, materials, request_id)
            from colombo.shared.tool_jobs import submit_or_poll
            return submit_or_poll(service.store.root, "brain_audit",
                {"role": role, "stage": stage, "call_id": call_id, "goal": goal,
                 "inputs": inputs, "record_refs": record_refs, "materials": materials,
                 "request_id": request_id}, request_id=request_id)

        @mcp.tool()
        def job_status(job_id: str) -> dict:
            """Continue polling the audit job for this call; do not restart it after a disconnection. Return the original audit receipt when complete."""
            service._active()
            from colombo.shared.tool_jobs import poll_job
            return poll_job(service.store.root, job_id, owner=call_id)

        @mcp.tool()
        def save_note(text: str, related_refs: list[str] | None = None,
                      status: Literal["open", "resolved", "abandoned"] = "open", supersedes: str | None = None) -> dict:
            """Save research ideas, questions, conjectures, or lessons worth retaining at any time; text is free-form content, may use Markdown, and has no fixed template.
            Write only new ideas; link existing tasks, results, proofs, or extended reviews through pinned IDs in related_refs, and include any necessary locators in the body.
            status defaults to open; ordinary notes need not be closed. Use resolved/abandoned only when applicable. supersedes revises an earlier note while retaining its history.
            Subsequent Brain calls may select full notes from their summaries; notes do not alter formal progress or replace evidence and review. Notes are not required at every step.
            """
            return service.save_note(text, related_refs, status, supersedes)

        if stage == "plan":
            @mcp.tool()
            def format_package_literal(ref: str, path: str, literal_text: str, reason: str) -> dict:
                """Resolve an explicitly inspected formula/Markdown ambiguity in future package copies.
                Read the fixed source first. Give one unique exact single-line literal expression and
                explain why it is mathematical/literal text, not a real file dependency. The service
                only adds code-span delimiters, binds source hash, and records the transformation.
                Never use to hide a genuine dependency. Original Results/reviews and published
                packages remain unchanged. Resubmit the plan after correcting preflight feedback.
                """
                return service.format_package_literal(ref, path, literal_text, reason)

            def submit_plan(payload: dict) -> dict:
                """Submit the tasks, responsibilities, and material list for this batch; the submission receipt references the same saved content."""
                return service.submit("plan", payload)
            submit_plan.__annotations__["payload"] = Annotated[dict, WithJsonSchema(PLAN)]
            mcp.tool()(submit_plan)
        elif stage in {"process_results", "integrate"}:
            def record_results(payload: dict) -> dict:
                """process_results uses already verified Result Claims to submit admissions, GoalProgress and audited Pruning.
                integrate submits the complete self-contained ProofDraft and candidate GoalProgress, with no Pruning.
                A new comparison in integrate may leave comparison review refs null until final Verifier passes.
                Proof body_source={result_ref,path} may select a complete frozen manuscript for final review.
                """
                return service.submit(stage, payload)
            record_results.__annotations__["payload"] = Annotated[dict, WithJsonSchema(INTEGRATION if stage == "integrate" else OBSERVATION)]
            mcp.tool()(record_results)
    else:
        @mcp.tool()
        def read_review_package(offset: ReviewOffset = 0, limit: ReviewLimit = 20) -> dict:
            """Retrieve the pinned review package and the full text of required records; each pinned version is supplied only once. Use next for subsequent pages.
            required_records does not automatically expand attachments or allowed history; populate checked_refs only after actually checking the records.
            """
            return service.read_review_package(offset, limit)

        def write_review(payload: dict) -> dict:
            """Submit an independent review and the references actually checked, without directly changing formal progress or execution status."""
            return service.submit("verify-progress", payload)
        write_review.__annotations__["payload"] = Annotated[dict, WithJsonSchema(REVIEW)]
        mcp.tool()(write_review)
    return mcp


def serve(run_root, role, stage, call_id):
    create_server(run_root, role, stage, call_id).run(transport="stdio")
