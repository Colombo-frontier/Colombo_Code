"""Tools support reference-based reads, incremental drafting, and role isolation rather than single-pass JSON assembly."""
from __future__ import annotations

import json
import re
from pathlib import Path

from ..core.config import resources_root
from ..core.contracts import ROLE_KINDS, ProtocolError, ValidationDiagnostics, references, resolve_pointer, schema, validate
from ..core.store import Workspace, bounded, digest, dumps


def function(name: str, description: str, props: dict) -> dict:
    return {"type": "function", "name": name, "description": description,
            "strict": True, "parameters": {"type": "object", "properties": props,
            "required": list(props), "additionalProperties": False}}


S = {"type": "string"}; I = {"type": "integer"}; B = {"type": "boolean"}
N = {"type": ["string", "null"]}; STRINGS = {"type": "array", "items": S}


class ToolHost:
    def __init__(self, workspace: Workspace, atlas, job: dict, config: dict, *, bridge=None, bibliography=None):
        self.ws = workspace; self.artifacts = workspace.artifacts; self.atlas = atlas
        self.job = job; self.role = job["role"]; self.config = config
        self.grants = set(references(job["inputs"]))
        self.bridge = bridge; self.bibliography = bibliography
        self.call_id = ""
        self.cap = config["budgets"]["max_tool_chars"]
        # A job may have multiple native MCP connections; ownership is the shared live source of permissions.
        self._refresh_owned()
        for row in self.ws.query("SELECT result FROM tool_calls WHERE job=? AND status='done'", (job["id"],)):
            self.grants.update(references(json.loads(row["result"])))

    def _refresh_owned(self):
        """Synchronize formal objects newly produced by this job without expanding permissions from other jobs or arbitrary diagnostics."""
        self.grants.update(r["ref"] for r in self.ws.query(
            "SELECT ref FROM ownership WHERE job=?", (self.job["id"],)))

    def definitions(self) -> list[dict]:
        defs = [
            function("work_list", "List this job's formal artifacts and drafts in pages for recovery after context continuation.", dict(offset=I,limit=I)),
            function("vocabulary_lookup", "Look up current controlled concepts, explicit parent edges, and missing IDs in batches. With empty ids, navigate using query/axis pagination; do not infer containment relationships.", dict(ids=STRINGS,query=S,axis=S,offset=I,limit=I)),
            function("vocabulary_lookup_batch", "Find alternatives for 1-16 source terms or exact IDs at once. Each result identifies human and machine registrations and its continuation offset. Use an empty axis to search all axes. Matches are retrieval suggestions; verify source scope before selecting any tag.", dict(queries={"type":"array","minItems":1,"maxItems":16,"items":{"type":"object","properties":{"term":S,"axis":S,"offset":I},"required":["term","axis","offset"],"additionalProperties":False}},limit=I)),
            function("resource_read", "Read role skills, shared standards, or schema files on demand; supports character pagination.", dict(path=S,offset=I,limit=I)),
            function("schema_read", "Get a component schema; profile also provides a target Atlas schema summary and access to the full schema.", dict(kind=S)),
            function("target_schema_read", "Read local schemas for the current Atlas. Empty name lists the manifest; paginate full schemas with pointer/offset without resolving references over the network.", dict(name=S,pointer=S,offset=I,limit=I)),
            function("artifact_get", "Read an authorized immutable artifact; narrow scope with a JSON Pointer and paginate with offset.", dict(ref=S,pointer=S,offset=I,limit=I)),
            function("artifact_put", "Validate and save a formal artifact for this role; json_text is complete JSON. Check source/proof references and source.version before freezing a result, and recheck all results for research; failures return diagnostics with specific paths.", dict(kind=S,json_text=S,dependencies=STRINGS)),
            function("draft_create", "Create a resumable draft for this job; initial_json may be an empty object.", dict(kind=S,initial_json=S)),
            function("draft_read", "Read this job's own draft and revision.", dict(draft_id=S,pointer=S,offset=I,limit=I)),
            function("draft_outline", "List immediate fields or array items of your own draft, with exact JSON Pointers, types, counts, and existing ID fields. No scientific text or dependency graph is expanded. offset/limit paginate entries; use the returned revision for draft_read_batch.", dict(draft_id=S,pointer=S,offset=I,limit=I)),
            function("draft_read_batch", "Read 1 to 8 selected subtrees from one snapshot of your own draft at a pinned revision. The response budget is shared and each page has next_offset; a stale revision rejects the entire batch. Use draft_outline first to locate exact paths.", dict(draft_id=S,revision=I,requests={"type":"array","minItems":1,"maxItems":8,"items":{"type":"object","properties":{"pointer":S,"offset":I,"limit":I},"required":["pointer","offset","limit"],"additionalProperties":False}})),
            function("draft_patch", "Apply JSON Patch add/replace/remove/test at a pinned revision; parent paths cannot be created implicitly.", dict(draft_id=S,revision=I,patches_json=S)),
            function("draft_validate", "Aggregate checks of the draft, source versions, target schema, and final tags in the current session; profile may supply final tag_facts_json, while an empty string uses draft or candidate facts. Does not write to Atlas or constitute scientific approval.", dict(draft_id=S,tag_facts_json=S)),
            function("draft_freeze", "Preflight bindings and target schema for the complete draft; freeze after mechanical adaptation. Return errors in the current session and issue a formal reference only on success.", dict(draft_id=S)),
            function("memory_save", "Save up to 5000 characters of working memory and formal result references for this job; this is not a review conclusion.", dict(text=S,refs=STRINGS)),
            function("memory_search", "Search this job's own working memory and reviewed shared result summaries; other producers' private memory is inaccessible.", dict(query=S,limit=I)),
            function("source_read", "Read a pinned version and character range of the original source.", dict(ref=S,offset=I,limit=I)),
            function("source_search", "Find text in an archived original source and return bounded context and character locations.", dict(ref=S,query=S,limit=I)),
        ]
        if self.role != "coordinator":
            defs += [
                function("bibliography_search", "Search arxiv, crossref, and openalex by task/topic; results are unread paper leads and cannot be treated as full text.", dict(provider=S,query=S,year={"type":["integer","null"]},limit=I,cursor=N)),
                function("source_fetch", "Fetch and archive original papers/clarification material. Pinned versions may use the cache; new material at the same URL requires refresh=true.", dict(url=S,version=S,refresh=B)),
            ]
        if self.role == "paper_scanner":
            defs += [function("paper_verify", "Register verified dates and pinned sources as publication events and retain verification provenance, rather than changing only top-level year.", dict(paper_ref=S,date=S,source_ref=S,venue=S,medium=S,event_kind=S,version_id=N))]
        if self.role in {"coordinator","task_scout","matcher","identity_reviewer","bound_updater","profile_researcher","profile_reviewer"}:
            defs += [function("atlas_catalog", "Browse the compact Atlas catalog in pages without loading full profiles or exclusion audits.", dict(offset=I,limit=I)),
                     function("atlas_search", "Broad-recall preliminary screening. Retain unknown entries; paginate/expand retrieval. Scores do not establish identity.", dict(candidate_ref=S,limit=I,offset=I,broaden=B)),
                     function("atlas_read", "Read a scientific file for the specified Atlas setting and pin its version; supports Pointer/pagination.", dict(setting_id=S,filename=S,pointer=S,offset=I,limit=I))]
        if self.role in {"bound_updater", "profile_researcher"}:
            defs.append(function("draft_synthesis_plan", "List mechanically identified synthesis obligations for your current profile draft against its assigned baseline. Read pages by offset. The listed opportunities await mathematical assessment.", dict(draft_id=S,offset=I,limit=I)))
            defs += [function("draft_clone", "Mechanically clone an authorized pinned profile into a draft for this job without returning its full text or inheriting scientific approval. Use an empty pointer for a profile source; native_record baselines allow only /content and check the job and current Atlas version/content. expected_digest is the bare hex digest of the pointer value's canonical JSON payload, available directly from the controller descriptor or artifact_get.value_digest. Submit only incremental changes through draft_patch afterward; final validation remains complete.", dict(source_ref=S,source_pointer=S,expected_digest=S))]
        if self.role in {"bound_updater", "profile_researcher", "profile_reviewer"}:
            defs.append(function("exact_check", "Execute a bounded exact-rational experiment and save a verifiable receipt. Read standards/exact_checks.md for the steps/assertions expression format. Bind tested proof/source refs. Failed assertions refute only the specified calculation; passing is never proof of a theorem or source fidelity.", dict(label=S,program_json=S,evidence_refs=STRINGS)))
        read_schemas = [definition["parameters"] for definition in defs
                        if definition["name"] in {"artifact_get", "source_read", "atlas_read"}]
        defs += [function("read_batch", "Execute up to 8 bounded read-only pages at once: artifact_get/source_read/atlas_read available to this role. Share the max_tool_chars budget and archive long responses for pagination; batch writes, network access, and recursive calls are not permitted.", {
            "requests": {"type": "array", "minItems": 1, "maxItems": 8, "items": {
                "type": "object", "properties": {
                    "tool": {"type": "string", "enum": ["artifact_get", "source_read", "atlas_read"]},
                    "arguments": {"anyOf": read_schemas}},
                "required": ["tool", "arguments"], "additionalProperties": False}}})]
        if self.bridge and self.role != "coordinator":
            defs += self.bridge.tools()
        return defs

    def _allowed(self, ref: str) -> dict:
        self._refresh_owned()
        if ref not in self.grants and not self.artifacts.owned(ref,self.job["id"]):
            raise ProtocolError("Reference is unauthorized; obtain it first from task input or an authorized formal artifact")
        item = self.artifacts.get(ref)
        self.grants.add(ref)
        self.grants.update(references(item["data"]))
        return item

    def _put(self, kind, data, deps=()):
        if kind not in ROLE_KINDS[self.role] | {"checkpoint"}:
            raise ProtocolError(f"{self.role} is not authorized to write {kind}")
        self._refresh_owned()
        # Check input references first and reject unauthorized material; normalization must not expand adapter permissions.
        refs = references(data) | set(deps)
        if not refs.issubset(self.grants):
            raise ProtocolError(f"Unauthorized artifact references: {sorted(refs-self.grants)[:3]}")
        projection = {}
        data, errors, changes = self._validate_artifact(kind, data, projection=projection)
        # Adapting legacy metadata must not implicitly introduce dependencies from other workspaces/producers.
        # Do not use reports containing original reference values here, to prevent the report itself from becoming an authorization bypass.
        self._refresh_owned()
        if not references(data).issubset(self.grants):
            raise ProtocolError("Adaptation introduced unauthorized artifact references; explicitly provide an authorized formal baseline/source first. Dependencies from other tasks cannot be copied automatically.")
        errors, changes = self._diagnostic_safe(errors), self._diagnostic_safe(changes)
        if errors:
            report = self._validation_report(kind, errors, changes)
            raise ValidationDiagnostics(errors, report, changes)
        ref = self.artifacts.put(kind, data, self.job["id"], deps)
        self.grants.add(ref)
        result = {"ref": ref, "kind": kind}
        result.update(self._projection_preview(projection))
        if changes:
            result["normalization_changes"] = changes
        return result

    def _validation_report(self, kind, errors, changes):
        ref = self.artifacts.put("external_result", {"validation_kind": kind, "errors": self._diagnostic_safe(errors),
                                  "normalization_changes": self._diagnostic_safe(changes)}, self.job["id"])
        self.grants.add(ref)
        return ref

    def _diagnostic_safe(self, value):
        """Unauthorized hashes in diagnostics are text only; they cannot be registered as artifact dependencies or grant permissions during recovery."""
        if isinstance(value, str):
            if references(value) and value not in self.grants:
                return "unavailable-artifact-reference:" + value
            return value
        if isinstance(value, dict):
            return {k: self._diagnostic_safe(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._diagnostic_safe(v) for v in value]
        return value

    def _profile_facts(self, profile, explicit=None):
        if self.job["inputs"].get("transfer_scope_ref"):
            from ..workflow.transfer import target_facts
            return target_facts(explicit)
        if explicit is not None:
            return explicit
        if "tag_facts" in profile:
            return profile["tag_facts"]
        inputs = self.job["inputs"]
        if inputs.get("candidate_ref") and inputs.get("identity_ref"):
            # Delay imports to avoid an Engine→Runner→Host initialization cycle; share mappings with the actual handoff.
            from ..workflow.engine import profile_facts
            candidate = self._allowed(inputs["candidate_ref"])["data"]
            identity = self._allowed(inputs["identity_ref"])["data"]
            return profile_facts(candidate, identity, profile)
        return []

    def _validation_reference(self, ref, expected_kind, path, errors, cache):
        """Preflight reads only authorized pinned objects; error responses cannot register unauthorized refs."""
        try:
            if ref not in cache:
                cache[ref] = self._allowed(ref)
            item = cache[ref]
        except (ProtocolError, KeyError, FileNotFoundError, ValueError, TypeError) as exc:
            errors.append({"code": "artifact_reference_unavailable", "path": path,
                           "expected_kind": expected_kind,
                           "message": "The reference is unauthorized, nonexistent, or unavailable in the archive; provide an authorized formal object first.",
                           "error_type": type(exc).__name__})
            return None
        if item["kind"] != expected_kind:
            errors.append({"code": "artifact_reference_kind", "path": path,
                           "expected_kind": expected_kind, "actual_kind": item["kind"],
                           "message": f"This reference must point to a {expected_kind} object; actual kind: {item['kind']}."})
            return None
        return item

    def _result_reference_errors(self, data, prefix="", cache=None):
        """Check source versions and proof references before freezing atomic results; do not judge theorem validity."""
        errors = []
        cache = {} if cache is None else cache
        for name, expected in (("source_refs", "source"), ("proof_refs", "proof")):
            for index, ref in enumerate(data.get(name, []) or []):
                self._validation_reference(ref, expected, f"{prefix}/{name}/{index}", errors, cache)
        if data.get("origin") != "published_theorem" and not data.get("proof_refs"):
            errors.append({"code": "analyst_proof_required", "path": prefix + "/proof_refs",
                           "message": "Analyst derivations/transformations must bind self-contained proof objects; a conclusion alone is insufficient."})
        for index, locator in enumerate(data.get("source_locators", []) or []):
            path = f"{prefix}/source_locators/{index}"
            if not isinstance(locator, dict):
                errors.append({"code": "source_locator_shape", "path": path,
                               "message": "A source locator must be an object."})
                continue
            source = self._validation_reference(locator.get("source_ref"), "source", path + "/source_ref", errors, cache)
            if source is None:
                continue
            version = source["data"].get("version")
            if not isinstance(version, str) or not version:
                errors.append({"code": "source_version_missing", "path": path + "/version",
                               "message": "The source object lacks a valid version, so its locator cannot be verified."})
            elif locator.get("version") != version:
                errors.append({"code": "source_version_mismatch", "path": path + "/version",
                               "expected_version": version, "actual_version": locator.get("version"),
                               "message": "The source locator version must equal the bound source.version value by value; use the version returned by the source read unchanged, rather than substituting a paper version name."})
        return errors

    def _research_reference_errors(self, data):
        errors, cache = [], {}
        for index, ref in enumerate(data["result_refs"]):
            path = f"/result_refs/{index}"
            result = self._validation_reference(ref, "result", path, errors, cache)
            if result is not None:
                errors.extend(self._result_reference_errors(result["data"], path + "/data", cache))
        for index, ref in enumerate(data["proof_refs"]):
            self._validation_reference(ref, "proof", f"/proof_refs/{index}", errors, cache)
        return errors

    def _projection_preview(self, projection):
        if not projection or self.role not in {"profile_researcher", "bound_updater"}:
            return {}
        # Only publish a program-produced snapshot whose existing artifact dependencies
        # the current author can already read. Do not import other cases' permissions.
        if not references(projection).issubset(self.grants):
            return {"preview_status": "unavailable: projection includes ungranted dependencies"}
        from ..atlas.projection_report import projection_report
        report = projection_report(projection)
        preview = self.artifacts.put("external_result", {"kind": "native_projection_preview",
            "files": projection["files"], "hashes": projection["hashes"],
            "bundle_hash": projection["bundle_hash"], "projection_report": report}, self.job["id"])
        self.grants.add(preview)
        return {"projection_preview_ref": preview, "bundle_hash": projection["bundle_hash"],
                "projection_report_pointer": "/projection_report", "validation": report["validation"],
                "regime_index_pointer": "/files/identity.json/regime_predicates",
                "regime_index_count": report["counts"]["regime_predicates"]}

    def _validate_artifact(self, kind, data, explicit_facts=None, *, projection=None):
        from copy import deepcopy
        from ..atlas.bindings import normalize_tag_facts
        from ..atlas.target_schema import adapt_profile, validate_profile_target
        from ..atlas.store import AtlasValidationError, comparison_binding_errors, _validate_profile_bindings
        from jsonschema import Draft202012Validator
        value = deepcopy(data)
        errors = [{"code": "component_schema", "path": "/" + "/".join(map(str, e.absolute_path)),
                   "message": ("comparisons require complete comparison keys; place relationship descriptions in relations" if kind == "profile" and list(e.absolute_path)[:1] == ["comparisons"] else e.message)}
                  for e in Draft202012Validator(schema(kind)).iter_errors(value)]
        changes = []
        if errors:
            shaped_profile = (kind == "profile" and isinstance(value, dict)
                and isinstance(value.get("setting_id"), str) and isinstance(value.get("schema_version"), str)
                and isinstance(value.get("common_specification"), dict) and isinstance(value.get("provenance"), dict)
                and all(isinstance(value.get(k), list) for k in ("views", "quantities", "resource_projections", "regimes", "bounds", "comparisons"))
                and all(isinstance(v, dict) for v in value["views"]))
            if not shaped_profile:
                return value, errors, changes
        scope_ref = self.job["inputs"].get("transfer_scope_ref")
        if scope_ref and kind in {"research", "review", "profile"}:
            from ..workflow import transfer
            scope = self._allowed(scope_ref)["data"]
            try:
                if self.atlas.version(scope["setting_id"]) != scope["base_version"]:
                    raise ProtocolError("The pinned transfer target changed during assessment")
                if kind == "profile":
                    original = self._allowed(scope["target_files"]["profile.json"])["data"]["content"]
                    transfer.check_transfer_profile(value, original)
                elif kind == "research":
                    transfer.check_transfer_research(scope, value, self._allowed)
                else:
                    transfer.check_transfer_review(value)
            except (KeyError, TypeError, ValueError) as exc:
                errors.append({"code": "transfer_contract", "path":"", "message":str(exc)})
                return value, errors, changes
        if kind == "review" and self.role == "profile_reviewer" and value.get("verdict") == "approve":
            from ..workflow.joint_review import require_frozen_analysis_read, require_joint_checks, validate_no_change
            try:
                require_joint_checks(value)
                subject = self._allowed(self.job["inputs"]["subject_ref"])
                if value["subject_ref"] != self.job["inputs"]["subject_ref"]:
                    raise ProtocolError("Review must bind the assigned subject.")
                if subject["kind"] == "proposal":
                    prepared = self._allowed(subject["data"]["prepared_ref"])["data"]
                    self.atlas.validate_review(prepared, value)
                elif subject["kind"] == "research" and subject["data"]["action"] == "no_change":
                    validate_no_change(self.atlas, subject["data"])
                require_frozen_analysis_read(self.ws, self.job["id"], subject)
            except (KeyError, ValueError) as exc:
                errors.append({"code": "joint_review", "path": "/joint_checks", "message": str(exc)})
        if kind in {"research", "review"} and self.job["inputs"].get("coverage_scope_ref"):
            # Also validate versioned research boundaries and review ledgers before freezing in the current session.
            from ..workflow.coverage import coverage_errors
            errors.extend(coverage_errors(value, self.job["inputs"], self.role, self.artifacts, resolve=self._allowed))
        if kind == "review" and self.role == "profile_reviewer" and (self.job["inputs"].get("proof_context_ref") or self.job["inputs"].get("issue_scope_contract_version") == "occurrence-bound-scope"):
            from ..workflow.proof_reuse import proof_approval_errors
            if self.job["inputs"].get("issue_scope_contract_version") == "occurrence-bound-scope" and not self.job["inputs"].get("proof_context_ref"):
                errors.append({"code": "proof_context_missing", "path": "/", "message": "A occurrence-bound-scope profile review requires its controller-generated proof context; missing catalogs cannot disable validation."})
            errors.extend(proof_approval_errors(value, self.job["inputs"], self.artifacts, resolve=self._allowed))
        if kind == "review" and self.role == "profile_reviewer":
            from ..atlas.projection_report import mechanical_repair_request
            try:
                mechanical_repair_request(value)
            except ProtocolError as exc:
                errors.append({"code": "projection_repair_scope", "path": "/projection_repairs", "message": str(exc)})
        if kind == "review" and self.role == "profile_reviewer" and (self.job["inputs"].get("review_context_ref") or value.get("bound_approvals") or self.job["inputs"].get("issue_scope_contract_version") == "occurrence-bound-scope"):
            from ..workflow.review_context import bound_approval_errors
            if self.job["inputs"].get("issue_scope_contract_version") == "occurrence-bound-scope" and not self.job["inputs"].get("review_context_ref"):
                errors.append({"code": "bound_context_missing", "path": "/", "message": "A occurrence-bound-scope profile review requires its controller-generated bound context; missing catalogs cannot disable validation."})
            errors.extend(bound_approval_errors(value, self.job["inputs"], self.artifacts, resolve=self._allowed))
        if kind == "result":
            errors.extend(self._result_reference_errors(value))
        elif kind == "candidate":
            result = normalize_tag_facts(value, value["tag_facts"])
            errors.extend(result["errors"]); changes.extend(result["changes"])
            value["tag_facts"] = result["facts"]
            if changes:
                value["reference_normalization"] = changes
        elif kind == "profile":
            sid = value["setting_id"]
            previous = self.atlas.read(sid) if self.atlas.version(sid) is not None else None
            result = adapt_profile(value, self.atlas.data, previous=previous)
            value = result["profile"]; changes.extend(result["changes"])
            errors.extend(validate_profile_target(value, self.atlas.data))
            from ..atlas.scientific import validate_profile_science
            try:
                validate_profile_science(value, previous)
            except ValueError as exc:
                errors.append({"code": "scientific_contract", "path": "/joint_analysis", "message": str(exc)})
            structural = comparison_binding_errors(value)
            errors.extend(structural)
            if not structural:
                try:
                    _validate_profile_bindings(value)
                except (AtlasValidationError, KeyError, TypeError, IndexError) as exc:
                    errors.extend(getattr(exc, "diagnostics", [{"code": "profile_shape", "message": str(exc)}]))
            if "tag_facts" in value:
                normalized = normalize_tag_facts(value, value["tag_facts"])
                value["tag_facts"] = normalized["facts"]
                changes.extend(normalized["changes"]); errors.extend(normalized["errors"])
            # Complete final facts belong to the research contract; profile freezing itself does not infer legacy format mappings.
            # Explicit draft_validate can run the same five-file preflight as the actual handoff in advance.
            if explicit_facts is not None:
                checked = self.atlas.preflight(value, explicit_facts, self.job["inputs"].get("base_version"))
                errors.extend(checked["errors"])
                if projection is not None and checked.get("valid"):
                    projection.update(checked["prepared"])
        elif kind == "research":
            errors.extend(self._research_reference_errors(value))
            if value["action"] == "no_change":
                from ..workflow.joint_review import validate_no_change
                try:
                    validate_no_change(self.atlas, value)
                except ValueError as exc:
                    errors.append({"code": "no_change_scope", "path": "/joint_analysis", "message": str(exc)})
            if value["action"] != "no_change":
                profile = self._allowed(value["profile_ref"])
                candidate = self._allowed(value["candidate_ref"])
                identity = self._allowed(value["identity_ref"])
                if profile["kind"] != "profile" or candidate["kind"] != "candidate" or identity["kind"] != "identity":
                    errors.append({"code": "research_reference_kind", "message": "The profile/candidate/identity reference kinds in research do not match"})
                else:
                    from ..workflow.engine import profile_facts
                    try:
                        facts = (transfer.target_facts(value.get("tag_facts")) if scope_ref else
                                 profile_facts(candidate["data"], identity["data"], profile["data"], value.get("tag_facts")))
                        normalized = normalize_tag_facts(profile["data"], facts)
                        errors.extend(normalized["errors"]); changes.extend(normalized["changes"])
                        value["tag_facts"] = normalized["facts"]
                        checked = self.atlas.preflight(profile["data"], normalized["facts"], value["base_version"])
                        errors.extend(checked["errors"])
                        if projection is not None and checked.get("valid"):
                            projection.update(checked["prepared"])
                    except (ProtocolError, AtlasValidationError) as exc:
                        errors.extend(getattr(exc, "diagnostics", [{"code": "profile_facts", "message": str(exc)}]))
            if not errors:
                from ..workflow.joint_review import require_finite_literature
                try:
                    require_finite_literature(self.ws, self.job["id"], value)
                except ValueError as exc:
                    errors.append({"code": "literature_scope", "path": "/literature_scope", "message": str(exc)})
        # Retain one copy when both binding validation and full prepare produce the same diagnostic.
        unique = {dumps(e): e for e in errors}
        return value, list(unique.values()), changes

    def _draft(self, draft_id):
        draft = self.ws.draft(draft_id, self.job["id"])
        origin = draft.get("clone_source")
        if origin is not None:
            # New connections/continuations restore refs only from existing authorized sources; draft patches cannot arbitrarily expand permissions.
            source = self._allowed(origin["source_ref"])
            if source["kind"] != origin["source_kind"] or digest(resolve_pointer(source["data"], origin["source_pointer"])) != origin["source_digest"]:
                raise ProtocolError("The cloned draft's pinned-source audit binding is invalid")
        return draft

    def _authorized_clone_source(self, args, item):
        """A material continuation may clone only its verified partial or the established fallback."""
        inputs = self.job["inputs"]
        if not inputs.get("resume_producer_job_id"):
            return
        selected = inputs.get("profile_clone_source")
        requested = {key: args[key] for key in ("source_ref", "source_pointer", "expected_digest")}
        if selected != requested:
            raise ProtocolError("Use the controller's pinned clone source for this material continuation.")
        from ..workflow.partial_clone import partial_clone_source
        partial = partial_clone_source(self.ws, self.role, inputs)
        if partial is not None:
            if selected != partial:
                raise ProtocolError("The partial clone descriptor does not match the interrupted producer's unique handoff.")
            return
        if item["kind"] == "native_record" and args["source_ref"] == inputs.get("base_profile_ref"):
            return
        previous = inputs.get("previous_artifact_ref")
        if previous:
            origin = self._allowed(previous)
            research = origin["data"]
            if (origin["kind"] == "research" and item["kind"] == "profile" and research.get("profile_ref") == args["source_ref"]
                    and all(research.get(k) == inputs.get(k) for k in ("candidate_ref", "identity_ref"))):
                return
        raise ProtocolError("The partial profile has no unique authorized producer handoff or fixed fallback.")

    def _clone_profile(self, args, call_id):
        """Clone an authorized immutable snapshot; bind CAS, payload, and the live Atlas version separately."""
        if not isinstance(args.get("expected_digest"), str) or not re.fullmatch(r"[a-f0-9]{64}", args["expected_digest"]):
            raise ProtocolError("expected_digest must be the 64-character bare hex digest of the canonical JSON payload; artifact_get.value_digest may be used")
        item = self._allowed(args["source_ref"])
        self._authorized_clone_source(args, item)
        pointer = args["source_pointer"]
        if item["kind"] == "profile":
            if pointer != "":
                raise ProtocolError("Cloning a profile supports only an empty source_pointer; subobjects cannot be converted into profiles")
            payload, version = item["data"], None
        elif item["kind"] == "native_record":
            if pointer != "/content" or item["data"].get("filename") not in {None, "profile.json"}:
                raise ProtocolError("Cloning a native_record supports only /content of profile.json")
            payload, version = item["data"].get("content"), item["data"].get("version")
        else:
            raise ProtocolError("draft_clone accepts only a profile or a pinned native profile baseline; other artifact kinds cannot be converted")
        if not isinstance(payload, dict):
            raise ProtocolError("The clone source must be a complete profile object")
        validate("profile", payload)
        text = dumps(payload)
        if len(text.encode("utf-8")) > 4_000_000:
            raise ProtocolError("The cloned profile exceeds the 4 MB limit; oversized objects must not be implicitly read or reconstructed")
        source_digest = digest(payload)
        if source_digest != args["expected_digest"]:
            raise ProtocolError("The clone source payload digest does not match; reread the pinned-source descriptor rather than guessing the version")
        setting_id = payload.get("setting_id")
        target_id = self.job["inputs"].get("setting_id")
        if target_id is not None and setting_id != target_id:
            raise ProtocolError("The cloned profile setting_id does not match the current research target")
        if item["kind"] == "native_record":
            inputs = self.job["inputs"]
            if not target_id or item["data"].get("setting_id") != target_id or not inputs.get("base_version") or version != inputs["base_version"]:
                raise ProtocolError("The native clone baseline must bind the current job's setting_id and base_version; self-reported versions are not accepted")
        source = {"source_ref": args["source_ref"], "source_pointer": pointer, "source_kind": item["kind"],
                  "source_digest": source_digest, "source_version": version}
        token = self.job["id"] + ":" + call_id
        prior = self.ws.draft_clone_receipt(self.job["id"], source, token)
        if prior is not None:
            # A successful clone receipt remains recoverable after subsequent Atlas changes; do not create or rewrite the draft.
            return prior
        if item["kind"] == "native_record":
            if self.atlas.version(target_id) != version:
                raise ProtocolError("The native clone baseline is stale: the current Atlas version differs from the pinned base_version")
            if digest(self.atlas.read(target_id, "profile.json")) != source_digest:
                raise ProtocolError("The native record content does not match the current pinned Atlas version; a self-reported version cannot impersonate a baseline")
        return self.ws.draft_clone(self.job["id"], payload, source, token)

    def _external_budget(self):
        scope = self.job["inputs"].get("budget_scope", self.job["id"])
        rows = self.ws.query("SELECT COUNT(*) AS n FROM tool_calls t JOIN jobs j ON t.job=j.id WHERE COALESCE(json_extract(j.inputs,'$.budget_scope'),j.id)=? AND (t.name IN ('source_fetch','bibliography_search') OR t.name LIKE 'mcp_%')", (scope,))
        if rows[0]["n"] > self.config["budgets"]["max_external_calls"]:
            raise ProtocolError("The external-call budget for this round is exhausted; save verified material and the unfinished scope")
        if getattr(self,"_active_tool",None)=="bibliography_search" and self.role=="paper_scanner" and self.job["inputs"].get("plan_ref"):
            plan=self.artifacts.get(self.job["inputs"]["plan_ref"])["data"]
            n=self.ws.query("SELECT COUNT(*) AS n FROM tool_calls WHERE job=? AND name='bibliography_search'",(self.job["id"],))[0]["n"]
            if n>plan["query_budget"]:raise ProtocolError("The bibliographic-query budget for this round is exhausted; retain the unread queue and coverage report")

    def _read_batch(self, requests, call_id):
        """Combine at most 8 existing paginated reads; recheck role, arguments, and reference permissions for each item."""
        from jsonschema import Draft202012Validator
        definitions = {definition["name"]: definition for definition in self.definitions()}
        wrapper_errors = list(Draft202012Validator(definitions["read_batch"]["parameters"]).iter_errors({"requests": requests}))
        if wrapper_errors:
            raise ProtocolError("read_batch accepts 1 to 8 artifact_get/source_read/atlas_read operations, each with tool and arguments.")
        if self.cap < 512:
            raise ProtocolError("max_tool_chars cannot accommodate the minimum batch-read response.")
        # Reserve space for each item's version/pinned-ref/pagination metadata and the batch header; do not allocate the full total budget to each of the 8 reads.
        page_limit = max(1, (self.cap - 512) // len(requests) - 512)
        items = []
        for index, request in enumerate(requests):
            name, arguments = request["tool"], request["arguments"]
            row = {"index": index, "tool": name}
            try:
                if name not in definitions:
                    raise ProtocolError("This role has not been granted this read tool.")
                parameter_errors = list(Draft202012Validator(definitions[name]["parameters"]).iter_errors(arguments))
                if parameter_errors:
                    raise ProtocolError("Arguments do not conform to the read tool's public schema.")
                if arguments["limit"] < 1 or arguments["offset"] < 0:
                    raise ProtocolError("offset/limit is out of range.")
                limited = dict(arguments, limit=min(arguments["limit"], page_limit))
                row["result"] = self.call(name, limited, f"{call_id}:batch:{index}")
            except Exception as exc:
                # Do not echo original arguments/refs or exception bodies, to prevent error responses from becoming an authorization bypass.
                row["error"] = {"error_type": type(exc).__name__, "recoverable": True,
                                "message": "This read failed; check role permissions, object kind, JSON Pointer, and pagination settings."}
            items.append(row)
        result = {"items": items, "count": len(items), "per_item_limit": page_limit,
                  "notice": "The response budget is shared; next_offset indicates unread content. Dependencies and subsequent pages are not expanded automatically."}
        if len(dumps(result)) > self.cap:
            # Archive only the bounded pages already requested; never read the full text or dependency graph in the background.
            ref = self.artifacts.put("external_result", {"tool": "read_batch", "result": result}, self.job["id"])
            self.grants.add(ref)
            return {"archived_result_ref": ref, "count": len(items),
                    "message": "Batch pages and metadata exceed max_tool_chars; paginate individual items with artifact_get /result/items."}
        return result

    def call(self, name: str, args: dict, call_id: str) -> object:
        self._refresh_owned()
        self.call_id = call_id
        self._active_tool = name
        allowed = {d["name"] for d in self.definitions()}
        if name not in allowed:
            raise ProtocolError(f"This role does not have tool: {name}")
        if name == "read_batch":
            return self._read_batch(args["requests"], call_id)
        if name == "work_list":
            rows=self.ws.query("SELECT a.ref,a.kind FROM artifacts a JOIN ownership o ON a.ref=o.ref WHERE o.job=? ORDER BY a.created",(self.job["id"],))
            drafts=self.ws.query("SELECT id AS draft_id,kind,revision FROM drafts WHERE job=?",(self.job["id"],))
            origins={r["draft_id"]:json.loads(r["source"]) for r in self.ws.query("SELECT draft_id,source FROM draft_origins WHERE job=?",(self.job["id"],))}
            for draft in drafts:
                if draft["draft_id"] in origins:
                    draft["clone_source"] = origins[draft["draft_id"]]
            entries=rows+drafts; off=max(args["offset"],0); lim=min(max(args["limit"],1),30)
            return {"items":entries[off:off+lim],"total":len(entries),"next_offset":off+lim if off+lim<len(entries) else None}
        if name == "vocabulary_lookup":
            from ..atlas.tags import vocabulary_index
            vocab=self.atlas.vocabulary();index=vocabulary_index(vocab)
            if len(args["ids"])>24:raise ProtocolError("Look up at most 24 exact concept IDs per batch")
            requested=args["ids"]
            if requested:
                rows=[index[k] for k in requested if k in index]; missing=[k for k in requested if k not in index]
            else:
                query=args["query"].casefold();axis=args["axis"].upper()
                rows=[v for k,v in sorted(index.items()) if (not axis or v.get("axis")==axis or k.startswith(axis+":")) and (not query or query in dumps(v).casefold())];missing=[]
            off=max(args["offset"],0);lim=min(max(args["limit"],1),24)
            selected=rows[off:off+lim];parents=set()
            for r in selected:
                for p in r.get("retrieval_parent_ids",r.get("parent_ids",[])) or []:
                    if isinstance(p,str):parents.add(p)
                if isinstance(r.get("parent_id"),str):parents.add(r["parent_id"])
            return {"vocabulary_version":{k:v.get("version") for k,v in vocab.items() if isinstance(v,dict)},"vocabulary_hash":digest(vocab),"concepts":selected,"registered_parents":[index[p] for p in sorted(parents) if p in index],"missing_ids":missing,"total":len(rows),"next_offset":off+lim if off+lim<len(rows) else None,"new_concept_policy":"Unregistered concepts remain proposed; they do not automatically imply a conflict or a mathematically new setting"}
        if name == "vocabulary_lookup_batch":
            from .vocabulary import lookup_batch
            return lookup_batch(self.atlas.vocabulary(), args["queries"], args["limit"], self.cap)
        if name == "atlas_catalog":
            entries=self.atlas.catalog();off=max(args["offset"],0);lim=min(max(args["limit"],1),30)
            return {"settings":[{k:r.get(k) for k in ["setting_id","title","primary_domain","view_ids","unknown_axes","profile_version"]} for r in entries[off:off+lim]],"inventory_version":self.atlas.version(),"total":len(entries),"next_offset":off+lim if off+lim<len(entries) else None}
        if name == "resource_read":
            root = resources_root().resolve(); path = (root / args["path"]).resolve()
            if not path.is_relative_to(root) or path.suffix not in {".md", ".json"} or not path.is_file():
                raise ProtocolError("Only project roles/protocols/skills/standards/schemas may be read")
            if path.relative_to(root).parts[0] not in {"agents", "skills", "standards", "schemas", "protocol.md"}:
                raise ProtocolError("Not an Agent resource directory")
            return bounded(path.read_text(encoding="utf-8"), args["offset"], min(args["limit"], self.cap))
        if name == "schema_read":
            result = {"path": f"schemas/{args['kind']}.schema.json", **bounded(schema(args["kind"]), 0, self.cap)}
            if args["kind"] in {"candidate","profile"}:
                result["native_operation_schema"]={"kind":"native_operation","path":"schemas/native_operation.schema.json",
                    "notice":"The target schema permits free-form objects; read schema_read(native_operation) separately for native operation structures this component can mechanically project. ID, returns, and precision/response fields follow that contract; invalid structure does not mean the ID is absent."}
            if args["kind"] == "profile":
                from ..atlas.target_schema import schema_manifest
                result["target_atlas"] = schema_manifest(self.atlas.data)
                result["target_schema_tool"] = "target_schema_read(name='profile',pointer='',offset=0,limit=...)"
            return result
        if name == "target_schema_read":
            from ..atlas.target_schema import schema_manifest, read_target_schema
            if not args["name"]:
                return schema_manifest(self.atlas.data, offset=max(args["offset"], 0), limit=min(max(args["limit"], 1), 20))
            return read_target_schema(self.atlas.data, args["name"], args["pointer"], args["offset"], min(args["limit"], self.cap))
        if name in {"artifact_get", "source_read", "source_search"}:
            item = self._allowed(args["ref"])
            if name == "artifact_get":
                return {"value_digest": digest(resolve_pointer(item["data"], args["pointer"])),
                        **self.artifacts.read(args["ref"], args["pointer"], args["offset"], min(args["limit"], self.cap))}
            if item["kind"] != "source":
                raise ProtocolError("source tools require kind=source")
            if name == "source_read":
                return {"ref": args["ref"], "url": item["data"]["url"], "version": item["data"]["version"], **bounded(item["data"]["text"], args["offset"], min(args["limit"], self.cap))}
            query = args["query"]
            if not query:
                raise ProtocolError("query must not be empty")
            text = item["data"]["text"]; hits = []; pos = 0
            for _ in range(min(max(args["limit"], 1), 10)):
                i = text.lower().find(query.lower(), pos)
                if i < 0: break
                start=max(0,i-400); end=min(len(text),i+len(query)+700)
                hits.append({"offset":start,"end":end,"text":text[start:end]}); pos=i+len(query)
            return {"ref":args["ref"],"version":item["data"]["version"],"hits":hits}
        if name == "artifact_put":
            return self._put(args["kind"], json.loads(args["json_text"]), args["dependencies"])
        if name == "draft_create":
            if args["kind"] not in ROLE_KINDS[self.role] | {"checkpoint"}: raise ProtocolError("No permission for this draft kind")
            return self.ws.draft_create(self.job["id"],args["kind"],json.loads(args["initial_json"]),call_id)
        if name == "draft_clone":
            return self._clone_profile(args, call_id)
        if name == "draft_read":
            d=self._draft(args["draft_id"])
            origin={"clone_source":d["clone_source"]} if "clone_source" in d else {}
            return {"draft_id":d["id"],"revision":d["revision"],"kind":d["kind"],**origin,**bounded(resolve_pointer(d["data"],args["pointer"]),args["offset"],min(args["limit"],self.cap))}
        if name in {"draft_outline", "draft_read_batch"}:
            from .drafts import outline, read_batch
            draft = self._draft(args["draft_id"])
            if name == "draft_outline":
                return outline(draft, args["pointer"], args["offset"], args["limit"], self.cap)
            return read_batch(draft, args["revision"], args["requests"], self.cap)
        if name == "draft_patch":
            self._draft(args["draft_id"])
            return self.ws.draft_patch(args["draft_id"],self.job["id"],args["revision"],json.loads(args["patches_json"]),self.job["id"]+":"+call_id)
        if name == "draft_freeze":
            d=self._draft(args["draft_id"])
            result=self._put(d["kind"],d["data"])
            if "clone_source" in d:
                audit={"draft_id":d["id"],"revision":d["revision"],"profile_ref":result["ref"],
                       "clone_source":d["clone_source"],"payload_digest":digest(d["data"])}
                self.ws.event(self.job["id"],"draft_clone_frozen",audit)
            return result
        if name == "draft_synthesis_plan":
            from ..atlas.joint import synthesis_requirements
            draft = self._draft(args["draft_id"])
            if self.role not in {"bound_updater", "profile_researcher"} or draft["kind"] != "profile":
                raise ProtocolError("A producer's profile draft is required.")
            baseline = {}
            ref = self.job["inputs"].get("base_profile_ref")
            if ref:
                baseline = self._allowed(ref)["data"]["content"]
            profile = draft["data"]
            scope = [c.get("comparison_id", c.get("id")) for c in profile.get("comparisons", [])]
            return {"draft_revision": draft["revision"], **bounded(
                synthesis_requirements(baseline, profile, scope), args["offset"], min(args["limit"], self.cap))}
        if name == "exact_check":
            from .exact_checks import run_check
            return run_check(self, args["label"], args["program_json"], args["evidence_refs"], call_id)
        if name == "draft_validate":
            d = self._draft(args["draft_id"])
            if args["tag_facts_json"]:
                facts = json.loads(args["tag_facts_json"])
                if not isinstance(facts, list):
                    raise ProtocolError("tag_facts_json must be a JSON array or an empty string")
            else:
                try:
                    facts = self._profile_facts(d["data"]) if d["kind"] == "profile" else None
                except (ProtocolError, KeyError, ValueError) as exc:
                    errors = [{"code": "profile_facts", "message": str(exc)}]
                    ref = self._validation_report(d["kind"], errors, [])
                    return {"valid": False, "report_ref": ref, "errors": errors, "error_count": len(errors)}
            projection = {}
            value, errors, changes = self._validate_artifact(d["kind"], d["data"], facts, projection=projection)
            self._refresh_owned()
            if not references(value).issubset(self.grants):
                errors.append({"code": "adaptation_ungranted_reference", "message": "The draft or adaptation metadata contains unauthorized artifact dependencies; provide an authorized formal baseline/source first."})
            errors, changes = self._diagnostic_safe(errors), self._diagnostic_safe(changes)
            ref = self._validation_report(d["kind"], errors, changes)
            from ..core.contracts import diagnostic_preview
            return {"valid": not errors, "report_ref": ref, "errors": diagnostic_preview(errors),
                    **(self._projection_preview(projection) if not errors else {}),
                    "error_count": len(errors), "normalization_changes": changes[:8],
                    "notice": "Preflight checks only format, source bindings, and the target five files; it does not establish independent scientific approval or ingestion."}
        if name == "memory_save":
            if not set(args["refs"]).issubset(self.grants): raise ProtocolError("Memory references are unauthorized")
            mid=self.ws.memory_save(self.job["id"],self.role,args["text"],args["refs"])
            return {"memory_id":mid}
        if name == "memory_search":
            out=self.ws.memory_search(self.job["id"],args["query"],args["limit"])
            self.grants.update(references(out)); return {"notes":out}
        if name == "atlas_search":
            from ..atlas.retrieval import retrieve
            item=self._allowed(args["candidate_ref"])
            if item["kind"]!="candidate": raise ProtocolError("Retrieval requires a candidate reference")
            out=retrieve(self.atlas,item["data"],limit=min(max(args["limit"],1),30),offset=max(args["offset"],0),broaden=args["broaden"])
            out["broaden"]=args["broaden"]
            out["candidate_ref"]=args["candidate_ref"]
            ref=self.artifacts.put("retrieval",out,self.job["id"])
            self.grants.add(ref)
            return {"retrieval_ref":ref,**out}
        if name == "atlas_read":
            content=self.atlas.read(args["setting_id"],args["filename"])
            native={"setting_id":args["setting_id"],"filename":args["filename"],"version":self.atlas.version(args["setting_id"]),"content":content}
            ref=self.artifacts.put("native_record",native,self.job["id"])
            self.grants.add(ref)
            return {"ref":ref,"version":native["version"],**bounded(resolve_pointer(content,args["pointer"]),args["offset"],min(args["limit"],self.cap))}
        if name == "source_fetch":
            from ..discovery.sources import fetch_source
            self._external_budget()
            result=fetch_source(args["url"],self.ws.root/"sources",refresh=args["refresh"])
            data={"url":result["url"],"version":args["version"] or result["content_hash"],"content_hash":result["content_hash"],"text":result["text"],"metadata":result.get("metadata",{})}
            ref=self.artifacts.put("source",data,self.job["id"])
            self.grants.add(ref)
            return {"source_ref":ref,"url":data["url"],"version":data["version"],"chars":len(data["text"]),"metadata":data["metadata"]}
        if name == "bibliography_search":
            from ..discovery.bibliography import Bibliography
            self._external_budget()
            if self.bibliography is None:
                self.bibliography=Bibliography()
            client=self.bibliography
            out=client.search(args["provider"],args["query"],year=args["year"],limit=min(max(args["limit"],1),50),cursor=args["cursor"])
            refs=[]; brief=[]
            for p in out.get("records",[]):
                identifiers=p.get("identifiers",{})
                p={**p,"doi":p.get("doi") or identifiers.get("doi"),"arxiv_id":p.get("arxiv_id") or identifiers.get("arxiv"),"urls":p.get("urls",[]),"publication_events":p.get("publication_events",[]),"provenance":p.get("provenance",[])}
                ref=self.artifacts.put("paper",p,self.job["id"]); self.grants.add(ref); refs.append(ref)
                brief.append({"paper_ref":ref,"title":p["title"],"doi":p["doi"],"events":p["publication_events"]})
            meta={k:v for k,v in out.items() if k!="records"}; meta["paper_refs"]=refs
            search_ref=self.artifacts.put("search",meta,self.job["id"]); self.grants.add(search_ref)
            return {"search_ref":search_ref,"papers":brief,**{k:v for k,v in meta.items() if k!="paper_refs"}}
        if name == "paper_verify":
            from ..discovery.bibliography import verify_publication
            paper=self._allowed(args["paper_ref"]);source=self._allowed(args["source_ref"])
            if paper["kind"]!="paper" or source["kind"]!="source":raise ProtocolError("Verification requires a paper and a source that has been read")
            data=verify_publication(paper["data"],date=args["date"],source={"artifact_ref":source["ref"],"url":source["data"]["url"],"version":source["data"]["version"]},venue=args["venue"],medium=args["medium"],event_kind=args["event_kind"],version_id=args["version_id"])
            ref=self.artifacts.put("paper",data,self.job["id"],[paper["ref"],source["ref"]]);self.grants.add(ref)
            return {"paper_ref":ref,"publication_events":data["publication_events"]}
        if self.bridge:
            self._external_budget()
            out=self.bridge.call(name,args)
            # Archive long MCP results and paginate them so third-party tools cannot bypass context limits.
            ref=self.artifacts.put("external_result",{"tool":name,"result":out},self.job["id"])
            self.grants.add(ref)
            return {"ref":ref,**bounded(out,0,self.cap)}
        raise ProtocolError(f"Unknown tool {name}")
