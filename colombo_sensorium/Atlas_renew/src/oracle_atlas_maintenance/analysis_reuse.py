"""Read-only qualification of an unchanged, actually adopted joint analysis.

These certificates authorize no publication and supply no source-reading credit.
Native writer construction, recovery, model execution and inspection of native
reasoning content are deliberately absent. Missing evidence disables the shortcut.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat

from jsonschema import Draft202012Validator

from oracle_atlas.atlas.store import FILES, json_bytes

from .state import digest
from .tools import MaintenanceTools
from .joint import joint_scope_complete, synthesis_scope_complete, validate_joint_analysis
from .evidence_basis import fully_read_frozen_value


_HEX = re.compile(r"[0-9a-f]{64}\Z")
_ATTEMPT = re.compile(r"[0-9a-f]{24}/[0-9]{6}/attempt-[0-9]{3,}\Z")
# Published pre-reference strict handoff, not an arbitrary caller schema.
# Current reports use the current schema; archived reports are never rewritten.
_LEGACY_SCOUT_SCHEMAS = frozenset({"16325c93208d9e7484dfa9ccf12cc833272ea55cbe9061034738be5fa73ffa1c"})


class StageIndex:
    """Incremental lookup hints only; every relevant native stage is revalidated."""
    def __init__(self, workspace):
        self.workspace = Path(workspace).resolve()
        self._seen, self._tasks, self._invalid = {}, {}, set()
        self._integrity = self._checksum()

    def _checksum(self):
        return digest({"seen": {str(p): value for p, value in self._seen.items()},
                       "tasks": {key: sorted(map(str, paths)) for key, paths in self._tasks.items()},
                       "invalid": sorted(map(str, self._invalid))})

    def refresh(self):
        # An in-memory hint is never authority. Rebuild corrupted lookup state.
        if self._integrity != self._checksum():
            self._seen, self._tasks, self._invalid = {}, {}, set()
        model = self.workspace / "model"
        paths = {p for p in model.iterdir() if p.is_dir() and _HEX.fullmatch(p.name)} if model.is_dir() else set()
        for path in set(self._seen) - paths:
            _, old_task = self._seen.pop(path)
            if old_task in self._tasks:
                self._tasks[old_task].discard(path)
            self._invalid.discard(path)
        for path in paths:
            request = path / "request.json"
            try:
                info = request.lstat()
                fingerprint = (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)
            except OSError:
                fingerprint = None
            if path in self._seen and self._seen[path][0] == fingerprint:
                continue
            previous = self._seen.get(path, (None, None))[1]
            if previous in self._tasks:
                self._tasks[previous].discard(path)
            task = None
            try:
                value = _load(request, self.workspace, {})
                _require(digest(value) == path.name and isinstance(value.get("task_key"), str), "Invalid native stage lookup entry")
                task = value["task_key"]
                self._tasks.setdefault(task, set()).add(path)
                self._invalid.discard(path)
            except (ValueError, TypeError, KeyError, OSError):
                self._invalid.add(path)
            self._seen[path] = (fingerprint, task)
        self._integrity = self._checksum()

    def candidates(self, task_key):
        _require(self._integrity == self._checksum(), "Corrupt native lookup cache cannot qualify a role")
        _require(not self._invalid, "Native stage index contains unreadable or invalid entries; no reuse offer")
        return set(self._tasks.get(task_key, set()))


def stage_index_for(state):
    index = getattr(state, "_analysis_stage_index", None)
    if not isinstance(index, StageIndex) or index.workspace != state.root.resolve():
        index = state._analysis_stage_index = StageIndex(state.root)
    return index


def _no_pending(inventory):
    for name in ("oracle_atlas_agents", "oracle_scout"):
        path = inventory.data / "intake" / name / "pending.json"
        _require(not path.exists() and not path.is_symlink(), "A native transaction is pending; no analysis reuse")


def _require(ok, message):
    if not ok:
        raise ValueError(message)


def _read(path, root, pins):
    path, root = Path(os.path.abspath(path)), Path(root).resolve()
    _require(path.is_relative_to(root), "Analysis-reuse evidence escapes its bound root")
    for part in (path, *path.parents):
        if part.exists() or part.is_symlink():
            _require(not stat.S_ISLNK(part.lstat().st_mode), "Analysis-reuse evidence cannot use symbolic links")
    _require(path.is_file(), "Missing analysis-reuse evidence: " + str(path))
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)), "rb") as stream:
        raw = stream.read()
    pins[str(path)] = hashlib.sha256(raw).hexdigest()
    return raw


def _load(path, root, pins):
    value = json.loads(_read(path, root, pins))
    # Reject nonfinite numbers even in ancillary, supposedly frozen records.
    digest(value)
    return value


def _instructions(request, agents, schema, metrics):
    manifest = request["instructions"]
    taxonomy = ("status_taxonomy.md", "status_taxonomy.json")
    present = {name for name in taxonomy if name in manifest}
    _require(not present or present == set(taxonomy), "Native taxonomy instruction manifest is incomplete")
    # Published four-part stages retain their original strict path. New stages
    # bind both taxonomy resources in the exact order actually sent by runtime.
    names = (("protocol.md",) + (("finite_research_standard.md",) if "finite_research_standard.md" in manifest else ())
             + ("joint_parameter_standard.md", "joint_analysis.schema.json")
             + (taxonomy if present else ()) + (request["role"] + ".md",))
    _require(set(manifest) == set(names) | {request["role"] + ".schema.json"},
             "Unsupported native instruction manifest resources")
    resources = Path(__file__).parent / "resources"
    for name in ("joint_parameter_standard.md", "joint_analysis.schema.json"):
        _require(manifest.get(name) == hashlib.sha256((resources / name).read_bytes()).hexdigest(),
                 "Accepted analysis uses a different joint standard or schema")
    for name in taxonomy if present else ():
        _require(manifest[name] == hashlib.sha256((resources / name).read_bytes()).hexdigest(),
                 "Accepted analysis uses a different status taxonomy")
    if "finite_research_standard.md" in manifest:
        _require(manifest["finite_research_standard.md"] == hashlib.sha256((resources / "finite_research_standard.md").read_bytes()).hexdigest(),
                 "Accepted analysis uses a different finite research standard")
    text, start = agents.decode("utf-8"), 0
    for i, name in enumerate(names):
        expected = manifest[name]
        if i == len(names) - 1:
            _require(hashlib.sha256(text[start:].encode()).hexdigest() == expected,
                     "Native role instructions do not match their manifest")
            break
        stop, matched = text.find("\n\n", start), False
        while stop != -1:
            if hashlib.sha256(text[start:stop].encode()).hexdigest() == expected:
                start, matched = stop + 2, True
                break
            stop = text.find("\n\n", stop + 1)
        _require(matched, "Native instruction segment does not match its manifest")
    _require(digest(schema) == manifest[request["role"] + ".schema.json"], "Native output schema differs from its manifest")
    _require(metrics.get("instructions_utf8_bytes") == len(agents)
             and metrics.get("project_doc_max_bytes", 0) >= len(agents), "Native instructions were not fully available")


def _known_role_schema(role, schema, report):
    current = json.loads((Path(__file__).parent / "resources" / (role + ".schema.json")).read_text("utf-8"))
    def strict(value):
        if isinstance(value, dict):
            if value.get("type") == "object" and "properties" in value:
                value["required"] = list(value["properties"])
            for child in value.values():
                strict(child)
        elif isinstance(value, list):
            for child in value:
                strict(child)
    strict(current)
    allowed = {digest(current)} | (_LEGACY_SCOUT_SCHEMAS if role == "scout" else set())
    _require(digest(schema) in allowed, "Unsupported historical native role schema")
    _require(not list(Draft202012Validator(schema).iter_errors(report)), "Original native report fails its actual archived schema")
    from .contracts import validate
    validate(role, report)


def _task_stage(workspace, task_key, index):
    _require(isinstance(index, StageIndex) and index.workspace == workspace.resolve(), "Invalid native stage lookup cache")
    candidates = sorted(index.candidates(task_key))
    _require(len(candidates) == 1, "Accepted role needs exactly one original actual native task")
    request = _load(candidates[0] / "request.json", workspace, {})
    _require(request.get("task_key") == task_key and digest(request) == candidates[0].name,
             "Stale or corrupt native lookup cannot identify the requested stage")
    return candidates[0]


def _native_stage(workspace, stage, role, report, pins, *, context=None, expected_host=None,
                  allow_partial_scout=False):
    """Verify one exact completed native request and every sealed public tool state."""
    workspace, stage = Path(workspace).resolve(), Path(stage)
    _require(stage.parent == workspace / "model" and _HEX.fullmatch(stage.name), "Invalid native evidence stage")
    load = lambda name: _load(stage / name, workspace, pins)
    request, metrics = load("request.json"), load("metrics.json")
    _require(digest(request) == stage.name and request.get("role") == role
             and request.get("backend") == "codex", "Native request identity/backend mismatch")
    _require(load("codex-receipt.json").get("status") == "completed"
             and metrics.get("native_sessions") == 1 and metrics.get("status") == "complete"
             and not metrics.get("replayed") and not metrics.get("reconciled"), "A completed original native session is required")
    result, final = load("result.json"), load("final.json")
    if request.get("compact_handoff", False):
        # Representation adapter only: all original native-role, source, read,
        # journal and adoption checks below still apply to the complete report.
        # Pin every additional raw dependency so warm reuse rechecks the exact
        # transport/artifact chain, including its public completion marker.
        _require(request.get("compact_handoff") is True, "Unsupported compact transport mode")
        try:
            from .runtime import validated_transport_report, validated_transport_dependencies
            dependencies = validated_transport_dependencies(stage)
            for path, expected in dependencies.items():
                _require(hashlib.sha256(_read(Path(path), workspace, pins)).hexdigest() == expected,
                         "Compact transport dependency changed while qualifying reuse")
            resolved = validated_transport_report(stage, role=role)
        except Exception as exc:
            raise ValueError("Completed compact native transport could not be verified") from exc
        _require(result == resolved == report, "Compact native result differs from the complete frozen report")
    else:
        _require(result == final == report, "Native result/final differs from the frozen report")
    _require(load("input.json") == request["context"], "Native input differs from request")
    mcp = load("mcp-input.json")
    frozen = mcp["context"]
    prompt = {k: v for k, v in frozen.items() if k != "artifacts"}
    prompt["frozen_artifact_hashes"] = {k: digest(v) for k, v in frozen.get("artifacts", {}).items()}
    _require(request["context"] == prompt and (context is None or frozen == context), "Native frozen context mismatch")
    _require(Path(mcp["cache_dir"]) == workspace / "cache" and Path(mcp["log_path"]) == stage / "tools.json"
             and request["model"] == mcp["config"].get("model", {})
             and mcp["config"].get("backend") == "codex"
             and Path(mcp["config"]["atlas"]).resolve() == Path(mcp["atlas_root"]).resolve()
             and Path(mcp["config"]["workspace"]).resolve() == workspace, "Native model/root/cache/log binding mismatch")
    host = MaintenanceTools(mcp["atlas_root"], mcp["cache_dir"], frozen, mcp["config"])
    _require(request["tools"] == host.specs(), "Native tool contract changed")
    schema = load("output.schema.json")
    _instructions(request, _read(stage / "AGENTS.md", workspace, pins), schema, metrics)
    if isinstance(frozen.get("runtime_budget"), dict):
        allocation = load("budget-allocation.json")
        _require(digest(allocation) == frozen["runtime_budget"].get("full_audit_sha256"),
                 "Native adaptive-budget audit differs from its pinned request")
        _require(allocation.get("scientific_approval") is False and allocation.get("source_read_credit") is False
                 and allocation.get("baseline_read_credit") is False, "Budget planning cannot grant scientific or reading credit")
    _known_role_schema(role, schema, report)
    records = [json.loads(line) for line in _read(stage / "tools-events.jsonl", workspace, pins).decode().splitlines()]
    _require(records, "Native evidence requires an actual tool journal")
    previous, events = None, []
    for sequence, record in enumerate(records):
        material = {k: v for k, v in record.items() if k != "record_hash"}
        _require(record.get("sequence") == sequence and record.get("previous_hash") == previous
                 and record.get("record_hash") == digest(material), "Native tool journal chain mismatch")
        event = record["event"]
        event_id = digest({"setting_id": frozen["setting_id"], "base_version": frozen["base_version"],
                           "prepared_hash": frozen.get("prepared_hash"), "sequence": sequence,
                           "tool": event["tool"], "arguments": event["arguments"]})
        _require(event["result"].get("event_id") == event_id, "Native tool event belongs to a different stage context")
        if isinstance(event["result"].get("audit"), dict):
            _require(event["result"]["audit"].get("event_id") == event_id, "Native tool audit identity mismatch")
        events.append(event)
        host.import_state({"events": events, **record["state_flags"]})
        _require(digest(host.state()) == record["state_sha256"], "Native tool journal state does not replay")
        previous = record["record_hash"]
    closed = {"audit_closed": True, "journal_records": len(records), "journal_head": previous,
              "state_sha256": digest(host.state())}
    _require(load("tools-closed.json") == closed and load("tools.json") == host.state()
             and load("tools-controller.json") == host.state(), "Native journal closure/state mismatch")
    from .contracts import current_finite_research_audit
    finite = current_finite_research_audit(host, frozen, report)
    operationally_clean = not host.failed or finite is not None and finite.get("failure_scope_clean") is True
    partial_scout = False
    if allow_partial_scout:
        _require(role == "scout" and report.get("outcome") == "candidate_change"
                 and report.get("joint_analysis_reuse") is None
                 and isinstance(report.get("joint_analysis_json"), str)
                 and finite is not None,
                 "Partial review import requires an auditable finite candidate scout, never another role or completed check")
        if not operationally_clean:
            _require(not finite.get("finite_scope_complete") and not getattr(host, "_orphan_failure_ids", set())
                     and not getattr(host, "_persistent_failed", False),
                     "A partial candidate cannot conceal completed or uncertain original evidence")
            partial_scout = True
    _require(all(metrics.get(k) == v for k, v in closed.items())
             and (operationally_clean or partial_scout) and not host.budget_exhausted,
             "Native stage was incomplete or failed")
    if expected_host is not None:
        _require(expected_host.state() == host.state(), "Current native journal does not describe this scout's own tools")
    return request, frozen, host, closed


def _native_semantics(inventory, pins):
    files = []
    for folder in ("schemas", "registry", "vocabulary"):
        paths = (inventory.data / folder).rglob("*.json") if folder == "schemas" else (inventory.data / folder).glob("*.json")
        from oracle_atlas.atlas.store import DERIVED_VOCABULARY
        files += [p for p in sorted(paths) if not (folder == "vocabulary" and p.name in DERIVED_VOCABULARY)]
    files += sorted(inventory.data.glob("aliases*.json"))
    return digest({p.relative_to(inventory.root).as_posix(): hashlib.sha256(_read(p, inventory.root, pins)).hexdigest()
                   for p in files})


def _unallocated_role_context(workspace, stage, role, frozen, pins):
    """Undo only a fully regenerated controller budget representation.

    The returned value is for cross-role comparison, never reading credit. All
    actual scientific checks continue to use the original allocated host.
    """
    from .budgeting import PREVIEW_ARTIFACT, PREVIEW_KEYS, _at, _parts, _replace, prepare_role_budget
    marker = frozen.get("runtime_budget")
    if marker is None:
        configured = _load(stage / "mcp-input.json", workspace, pins)["config"].get("budgets", {})
        _require(not configured.get("adaptive_input_budget") and not configured.get("adaptive_tool_budget")
                 and PREVIEW_ARTIFACT not in frozen.get("artifacts", {}),
                 "An unaudited budgeting artifact cannot qualify reuse")
        return copy.deepcopy(frozen)
    _require(isinstance(marker, dict), "Invalid adaptive role-budget marker")
    audit = _load(stage / "budget-allocation.json", workspace, pins)
    _require(digest(audit) == marker.get("full_audit_sha256") and audit.get("role") == role
             and audit.get("version") == 1 and audit.get("enabled") is True,
             "Adaptive role budget is not bound to its exact generated audit")
    restored = copy.deepcopy(frozen)
    def restore_field(parent, key, record):
        _require(isinstance(record, dict) and set(record) == {"present", "value"}
                 and type(record["present"]) is bool, "Missing exact preallocation budget-field provenance")
        if record["present"]:
            parent[key] = copy.deepcopy(record["value"])
        else:
            _require(record["value"] is None, "Absent preallocation field has an invented value")
            parent.pop(key, None)
    for projection in reversed(audit["projections"]):
        path = _parts(projection["context_pointer"])
        catalog_version = audit.get("catalog_projection_version")
        if catalog_version is not None:
            from .budgeting import CATALOG_PREVIEW_KEYS, CATALOG_PROJECTION_VERSION
            _require(type(catalog_version) is int and catalog_version == CATALOG_PROJECTION_VERSION,
                     "Unsupported whole catalog budgeting projection")
        allowed_roots = set(PREVIEW_KEYS) | (set(CATALOG_PREVIEW_KEYS) if catalog_version is not None else set())
        _require(path and path[0] in allowed_roots and projection["provided_complete"] is False
                 and projection["artifact"] in {"baseline", "prepared", PREVIEW_ARTIFACT},
                 "Adaptive audit attempted a non-preview representation change")
        original = _at(frozen["artifacts"][projection["artifact"]], _parts(projection["pointer"]))
        _require(digest(original) == projection["original_sha256"], "Adaptive preview original value changed")
        _replace(restored, path, copy.deepcopy(original))
        for metadata in reversed(projection["metadata_before"]):
            field_path = _parts(metadata["context_pointer"])
            _require(field_path and field_path[0] == path[0]
                     and field_path[-1] in {"provided_complete", "incomplete", "fixed_scope_incomplete"},
                     "Adaptive audit attempted to restore non-preview metadata")
            restore_field(_at(restored, field_path[:-1]), field_path[-1],
                          {key: metadata[key] for key in ("present", "value")})
    artifacts = restored.get("artifacts", {})
    additions = audit["preview_artifact_added_keys"]
    _require(isinstance(additions, list) and len(set(additions)) == len(additions),
             "Adaptive preview extension key inventory is invalid")
    if PREVIEW_ARTIFACT in artifacts:
        bucket = artifacts[PREVIEW_ARTIFACT]
        _require(isinstance(bucket, dict) and isinstance(bucket.get("values"), dict), "Invalid adaptive preview container")
        for key in additions:
            _require(key in bucket["values"], "Missing frozen adaptive preview extension")
            del bucket["values"][key]
        if audit["original_preview_artifact_sha256"] is None:
            _require(digest(bucket) == digest({"kind": "controller_budgeting_previews", "version": 1, "values": {}}),
                     "Adaptive preview container contains unaudited entries or metadata")
            del artifacts[PREVIEW_ARTIFACT]
        else:
            _require(digest(bucket) == audit["original_preview_artifact_sha256"],
                     "Adaptive allocation changed an existing frozen preview container")
    else:
        _require(not additions and audit["original_preview_artifact_sha256"] is None,
                 "Adaptive preview container provenance is missing")
    fields = audit["original_context_fields"]
    _require(set(fields) == {"budgets", "runtime_budget"}, "Unsupported preallocation context-field provenance")
    for key, record in fields.items():
        restore_field(restored, key, record)
    _require(digest(restored) == audit["original_context_sha256"]
             and {key: digest(restored[key]) for key in PREVIEW_KEYS if key in restored} == audit["original_preview_hashes"],
             "Adaptive restoration changed the original semantic context or preview identity")
    config = copy.deepcopy(_load(stage / "mcp-input.json", workspace, pins)["config"])
    effective_config = copy.deepcopy(config)
    restore_field(config, "budgets", audit["original_config_budgets"])
    _require(digest(config) == audit["original_config_sha256"], "Adaptive original configuration binding changed")
    instructions = _read(stage / "AGENTS.md", workspace, pins).decode("utf-8")
    generated = prepare_role_budget(role, instructions, restored, config,
        max_tool_calls=audit["tool_estimate"]["remaining_tool_limit"])
    _require(digest(generated["context"]) == digest(frozen)
             and digest(generated["config"]) == digest(effective_config) and digest(generated["audit"]) == digest(audit),
             "Adaptive role context does not equal its exact deterministic allocation")
    return restored


def _qualify_attempt(inventory, state, directory, sid, version, semantics, index):
    pins, workspace = {}, state.root.resolve()
    load = lambda name: _load(directory / name, workspace, pins)
    baseline, scout, prepared, review = (load(n) for n in ("baseline.json", "scout.json", "prepared.json", "reviewer.json"))
    approved, receipt, context = (load(n) for n in ("approved.json", "receipt.json", "context.json"))
    run_id, position, attempt = directory.relative_to(workspace / "runs").parts
    plan = _load(workspace / "runs" / run_id / "plan.json", workspace, pins)
    _require(plan == state.plan(run_id) and plan["setting_ids"][int(position)] == sid
             and Path(plan["atlas_root"]).resolve() == inventory.root
             and plan["versions"][sid] == context["base_version"] and plan["cutoff"] == context["cutoff"] == approved["cutoff"]
             and context["setting_id"] == baseline["setting_id"] == sid, "Accepted origin does not bind its original plan")
    _require(context["semantics"] == approved["semantics"] == plan["semantics"] == semantics
             and context["policy"] == approved["policy"] == plan["policy"], "Accepted origin semantics/policy mismatch")
    _require(approved.get("scope_complete") is True and scout["outcome"] == "candidate_change"
             and scout["scope"]["queries_complete"] is True and not scout["scope"]["unresolved_leads"], "Partial or pending acceptance cannot be reused")
    files = prepared["files"]
    _require(set(files) == set(FILES), "Accepted prepared snapshot must contain the native five files")
    hashes = {name: hashlib.sha256(json_bytes(files[name])).hexdigest() for name in FILES}
    bundle = digest(files)
    _require(prepared["setting_id"] == receipt["setting_id"] == sid and prepared["version"] == receipt["version"] == version
             and prepared["hashes"] == receipt["files"] == hashes and version == "target-" + digest(hashes)
             and prepared["bundle_hash"] == receipt["bundle_hash"] == bundle
             and prepared["base_version"] == receipt["base_version"] == context["base_version"], "Accepted native snapshot binding mismatch")
    for name in FILES:
        _require(hashlib.sha256(_read(inventory.path(sid, name), inventory.root, pins)).hexdigest() == hashes[name],
                 "Current native files differ from the accepted five-file snapshot")
    _require(prepared["semantics_version"] == _native_semantics(inventory, pins), "Native schema semantics changed")
    _require(approved["prepared"] == prepared and approved["review"] == review and approved["report"] == scout,
             "Accepted execution records disagree")
    task_prefix = run_id + ":" + str(int(position)) + ":" + str(int(attempt.removeprefix("attempt-")))
    scout_stage = _task_stage(workspace, task_prefix + ":scout", index)
    _, scout_frozen, scout_host, scout_closed = _native_stage(workspace, scout_stage, "scout", scout, pins)
    scout_unallocated = _unallocated_role_context(workspace, scout_stage, "scout", scout_frozen, pins)
    _require({k: v for k, v in scout_frozen.items() if k != "artifacts"} == context
             and scout_frozen["artifacts"].get("baseline") == baseline
             and set(scout_unallocated["artifacts"]).issubset({"baseline", "joint_template"})
             and ("joint_template" not in scout_unallocated["artifacts"]
                  or scout_unallocated["artifacts"]["joint_template"] == baseline.get("joint_analysis")),
             "Accepted scout did not read the exact original frozen context")
    _require(Path(_load(scout_stage / "mcp-input.json", workspace, pins)["atlas_root"]).resolve() == inventory.root
             and load("scout-tools.json") == scout_host.state()
             and load("scout-metrics.json") == _load(scout_stage / "metrics.json", workspace, pins),
             "Accepted scout controller/native evidence mismatch")
    from .contracts import check_scope, reviewer_context_view, row_id, current_finite_research_audit, finite_review_context
    from .engine import search_complete, _review_source_grants
    check_scope(scout, scout_frozen, scout_host)
    finite = current_finite_research_audit(scout_host, scout_frozen, scout)
    discovery_complete = finite.get("finite_scope_complete") if finite is not None else bool(scout_host.search_log) and search_complete(scout_host.search_log)
    _require(set(scout["scope"]["examined_comparison_ids"]) == {row_id(row, "comparisons") for row in baseline.get("comparisons", [])}
             and discovery_complete,
             "Accepted scout did not complete its actual finite comparison/search scope")
    joint = files["profile.json"].get("joint_analysis")
    _require(isinstance(joint, dict) and joint_scope_complete(joint) and synthesis_scope_complete(joint),
             "Accepted joint analysis needs current complete synthesis, without draft or pending work")
    _require(json.loads(scout["joint_analysis_json"]) == joint, "Accepted joint analysis differs from its actual scout handoff")
    validate_joint_analysis(joint, files["profile.json"], files["profile.json"], expected_comparison_ids=None,
                            require_current=True)
    _require(review.get("joint_analysis_hash") == digest(joint) and review.get("verdict") == "approve"
             and not review.get("issues"), "Accepted review does not bind the exact joint analysis")
    checks = {"parameter_roles", "guarded_envelopes", "domain_accounting", "improvement_regions", "provenance", "display_consistency"}
    _require(set(review.get("joint_checks", {})) == checks and all(review["joint_checks"][k] is True for k in checks), "Accepted review lacks the six independent checks")
    request_hash = digest({"bundle_hash": bundle, "review": review, "base_version": prepared["base_version"]})
    _require(receipt.get("status") == "committed" and receipt.get("request_hash") == request_hash
             and receipt.get("receipt_id") == "atlas-" + request_hash[:24], "Invalid actual native receipt")
    key = approved["idempotency_key"]
    _require(isinstance(key, str) and bool(key), "Missing native idempotency key")
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    native = inventory.data / "intake/oracle_atlas_agents"
    _require(not (native / "pending.json").exists(), "A native transaction is still pending")
    _require(_load(native / "receipts" / (key_hash + ".json"), inventory.root, pins) == receipt,
             "Accepted receipt is absent from native storage")
    transaction = native / "transactions" / request_hash
    journal = _load(transaction / "journal.json", inventory.root, pins)
    for key, value in {"transaction_id": request_hash, "request_hash": request_hash, "key_hash": key_hash,
                       "setting_id": sid, "bundle_hash": bundle, "base_version": prepared["base_version"],
                       "version": version, "state": "committed"}.items():
        _require(journal.get(key) == value, "Accepted native committed journal mismatch")
    _require(set(journal["files"]) == set(FILES) and journal.get("approved_bound_ids") == receipt.get("approved_bound_ids")
             and set(receipt.get("approved_bound_ids", [])).issubset(review.get("approved_bound_ids", [])), "Native adopted bound identities mismatch")
    old_hashes = {name: journal["files"][name]["old_sha256"] for name in FILES}
    _require(prepared["base_version"] == "target-" + digest(old_hashes), "Native journal does not bind the old five-file version")
    for name in FILES:
        _require(journal["files"][name]["new_sha256"] == hashes[name]
                 and hashlib.sha256(_read(transaction / "new" / name, inventory.root, pins)).hexdigest() == hashes[name], "Native staged file differs from the accepted snapshot")
    # Bound by exact original task keys, never a caller-supplied stage path.
    review_stage = _task_stage(workspace, task_prefix + ":reviewer", index)
    request, frozen, host, closed = _native_stage(workspace, review_stage, "reviewer", review, pins)
    comparison_frozen = _unallocated_role_context(workspace, review_stage, "reviewer", frozen, pins)
    # Historical stages without a marker must match their exact original view.
    # A marked stage must match the complete same pure projection, including
    # every pending field, compact descriptor and marker member. No field is
    # exempted merely because it is old working context.
    inherited_context = context
    if "reviewer_input_view" in comparison_frozen:
        inherited_context = {k: v for k, v in reviewer_context_view(scout_frozen, scout["findings"]).items()
                             if k != "artifacts"}
    projected_fields = {"compact_profile", "pending_work", "reviewer_input_view"}
    _require({k: comparison_frozen[k] for k in projected_fields if k in comparison_frozen}
             == {k: inherited_context[k] for k in projected_fields if k in inherited_context},
             "Accepted reviewer input view differs from its exact original or projected scout context")
    expected_artifacts = {**scout_frozen["artifacts"], "prepared": files["profile.json"]}
    if finite is not None:
        expected_artifacts["scout_research_scope"] = finite
        inherited_context = {**inherited_context, **finite_review_context(finite, _review_source_grants(scout, scout_host))}
    _require(Path(_load(review_stage / "mcp-input.json", workspace, pins)["atlas_root"]).resolve() == inventory.root
             and frozen["artifacts"]["baseline"] == baseline and frozen["artifacts"]["prepared"] == files["profile.json"]
             and frozen["prepared_hash"] == bundle and frozen.get("findings") == scout["findings"]
             and frozen.get("research_scope") == scout["scope"]
             and frozen.get("allowed_source_hashes") == _review_source_grants(scout, scout_host)
             and comparison_frozen["artifacts"] == expected_artifacts
             and all(comparison_frozen.get(k) == v for k, v in inherited_context.items() if k not in {"synthesis_catalog", "allowed_source_hashes"}),
             "Accepted reviewer read different frozen objects/findings/research scope/source grants")
    from .contracts import check_review
    check_review(review, frozen, prepared, scout, host)
    resources = Path(__file__).parent / "resources"
    return {"kind": "verified_complete_native_joint_acceptance", "setting_id": sid, "base_version": version,
            "joint_analysis_hash": digest(joint), "semantics": semantics, "analysis": copy.deepcopy(joint),
            "workspace": str(workspace), "atlas_root": str(inventory.root), "origin_attempt": str(directory),
            "origin_scout_stage": str(scout_stage), "origin_scout_closed_receipt": scout_closed,
            "origin_review_stage": str(review_stage), "origin_closed_receipt": closed,
            "origin_role_tasks": {task_prefix + ":scout": str(scout_stage), task_prefix + ":reviewer": str(review_stage)},
            "joint_policy_hashes": {name: hashlib.sha256((resources / name).read_bytes()).hexdigest()
                for name in ("joint_parameter_standard.md", "joint_analysis.schema.json")},
            "evidence_pins": pins, "publication_authorized": False,
            "source_read_credit": False}


def qualify_accepted_analysis(inventory, state, sid, version, semantics):
    """Return an internal exact certificate, or no offer when proof is unavailable."""
    profile = inventory.read(sid)
    if (not isinstance(profile.get("joint_analysis"), dict)
            or not joint_scope_complete(profile["joint_analysis"])
            or not synthesis_scope_complete(profile["joint_analysis"])):
        return None
    try:
        _no_pending(inventory)
        index = stage_index_for(state)
        index.refresh()
    except (ValueError, OSError):
        return None
    rows = state.db.execute("SELECT result FROM items WHERE setting_id=? AND status='committed' AND result IS NOT NULL ORDER BY rowid DESC LIMIT 32", (sid,)).fetchall()
    for row in rows:
        try:
            result = json.loads(row[0])
            if result.get("receipt", {}).get("version") != version:
                continue
            path = Path(result["artifact_path"])
            _require(path.is_absolute() and path.is_relative_to(state.root / "runs")
                     and _ATTEMPT.fullmatch(path.relative_to(state.root / "runs").as_posix()), "Invalid accepted attempt location")
            certificate = _qualify_attempt(inventory, state, path, sid, version, semantics, index)
            _require(result["receipt"] == _load(path / "receipt.json", state.root, {}), "Queue receipt differs from its actual transaction")
            return certificate
        except (ValueError, KeyError, TypeError, IndexError, OSError):
            continue
    return None


def recheck_accepted_analysis(certificate, inventory, *, stage_index=None):
    _require(certificate is not None and certificate.get("kind") == "verified_complete_native_joint_acceptance",
             "No verified complete native analysis is available for reuse")
    _require(str(inventory.root) == certificate["atlas_root"] and inventory.version(certificate["setting_id"]) == certificate["base_version"]
             and inventory.semantics() == certificate["semantics"], "Accepted analysis baseline or semantics changed")
    _no_pending(inventory)
    index = stage_index if stage_index is not None else StageIndex(certificate["workspace"])
    index.refresh()
    for task_key, expected_stage in certificate["origin_role_tasks"].items():
        _require(str(_task_stage(Path(certificate["workspace"]), task_key, index)) == expected_stage,
                 "Accepted native role became ambiguous or changed during maintenance")
    resources = Path(__file__).parent / "resources"
    _require(certificate["joint_policy_hashes"] == {name: hashlib.sha256((resources / name).read_bytes()).hexdigest()
        for name in ("joint_parameter_standard.md", "joint_analysis.schema.json")}, "Joint standard or schema changed during maintenance")
    for path, expected in certificate["evidence_pins"].items():
        root = inventory.root if Path(path).is_relative_to(inventory.root) else Path(certificate["workspace"])
        _require(hashlib.sha256(_read(path, root, {})).hexdigest() == expected, "Accepted-analysis evidence changed during maintenance")
    _require(digest(inventory.read(certificate["setting_id"]).get("joint_analysis")) == certificate["joint_analysis_hash"], "Accepted joint analysis changed")


def recheck_evidence_pins(pins, root):
    for path, expected in pins.items():
        _require(hashlib.sha256(_read(path, root, {})).hexdigest() == expected, "Finite-empty discovery evidence changed during maintenance")


def require_own_analysis_read(baseline, host):
    joint = baseline.get("joint_analysis")
    _require(isinstance(joint, dict) and (fully_read_frozen_value(host, "baseline", "/joint_analysis", joint)
             or fully_read_frozen_value(host, "baseline", "", baseline)), "No-change reuse requires the scout's complete own frozen baseline joint-analysis read")


def finite_empty_search_certificate(inventory, state, config, context, host, task_key, report, analysis, accepted):
    """Attest zero actual metadata, never turn an omitted preview into no results."""
    _require(not context.get("pending_work"), "Pending working notes cannot be resolved by a different empty-query snapshot")
    recheck_accepted_analysis(accepted, inventory, stage_index=stage_index_for(state))
    _require(report.get("findings") == [] and digest(analysis) == accepted["joint_analysis_hash"], "Finite-empty reuse cannot change the accepted analysis")
    require_own_analysis_read(context["artifacts"]["baseline"], host)
    from .runtime import _instructions, build_stage_request
    _, _, instructions = _instructions("scout")
    prompt = {k: copy.deepcopy(v) for k, v in context.items() if k != "artifacts"}
    prompt["frozen_artifact_hashes"] = {k: digest(v) for k, v in context.get("artifacts", {}).items()}
    request = build_stage_request("scout", prompt, instructions, host.specs(), config, task_key)
    stage = state.root / "model" / digest(request)
    pins = {}
    actual, _, replayed, closed = _native_stage(state.root, stage, "scout", report, pins, context=context, expected_host=host)
    _require(actual == request, "Finite-empty native request differs from the current task")
    searches = [e for e in replayed.events if e["tool"] == "bibliography_search"]
    _require(searches and not any(e["result"].get("error") for e in replayed.events), "Finite-empty discovery requires successful actual current calls")
    _require(not any(e["tool"] in {"source_fetch", "source_read", "source_find"} for e in replayed.events),
             "Finite-empty discovery cannot leave a directly accessed source unclassified; use source-backed findings or incomplete")
    snapshots = []
    for event in replayed.events:
        if event["tool"] not in {"bibliography_search", "bibliography_read"}:
            continue
        result = event["result"]
        _require(type(result.get("page_records_total")) is int and result["page_records_total"] == 0
                 and result.get("records") == [] and result.get("record_indices") == []
                 and result.get("next_record_offset") is None and result.get("next_cursor") is None
                 and result.get("output_truncated") is False
                 and type(result.get("total")) in {int, float} and result["total"] == 0,
                 "Finite-empty discovery encountered positive, unknown or unfinished metadata")
    for event in searches:
        args, result = event["arguments"], event["result"]
        audit = result["audit"]
        _require(audit.get("success") is True and audit.get("fresh") is True
                 and type(audit.get("records_returned")) is int and audit["records_returned"] == 0
                 and type(audit.get("records_exposed")) is int and audit["records_exposed"] == 0
                 and audit.get("output_truncated") is False and audit.get("next_cursor") is None
                 and type(audit.get("total")) in {int, float} and audit["total"] == 0
                 and args.get("cursor") is None and isinstance(audit.get("cached"), bool)
                 and type(audit.get("fetched_epoch")) in {int, float} and math.isfinite(audit["fetched_epoch"]) and audit["fetched_epoch"] > 0,
                 "Finite-empty query lacks an exact terminal zero-result audit")
        page = _load(state.root / "cache/search_pages" / (result["search_id"] + ".json"), state.root, pins)
        _require(digest(page["result"]) == page["sha256"] and digest({"query": page["query"], "page_sha256": page["sha256"]}) == result["search_id"]
                 and page["result"].get("records") == [] and type(page["result"].get("total")) in {int, float}
                 and page["result"]["total"] == 0 and page["result"].get("next_cursor") is None,
                 "Finite-empty cached metadata snapshot differs from the observed page")
        query = {**args, "query": args["query"].strip(), "window_start": context.get("window_start"), "cutoff": context["cutoff"], "version": 1}
        _require(page["query"] == query, "Finite-empty snapshot belongs to a different query/window")
        snapshots.append({"search_id": result["search_id"], "provider": args["provider"], "query": args["query"],
                          "cached": audit["cached"], "fetched_epoch": audit["fetched_epoch"], "total": 0})
    return {"kind": "verified_finite_empty_native_search", "setting_id": context["setting_id"], "base_version": context["base_version"],
            "report_sha256": digest(report), "tool_state_sha256": digest(host.state()), "native_stage": str(stage),
            "closed_receipt": closed, "snapshots": snapshots, "evidence_pins": pins,
            "interpretation": "These literal metadata-query snapshots returned zero records. Cached snapshots retain their fetched time; this is finite scope, not global literature exhaustiveness or a source-theorem read."}
