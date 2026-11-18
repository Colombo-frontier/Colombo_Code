"""Bounded concurrent fixed-ID maintenance; only reviewed deltas reach the native writer."""
from __future__ import annotations

from datetime import date, datetime, timedelta
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from zoneinfo import ZoneInfo
from types import SimpleNamespace

from oracle_atlas.atlas.store import Atlas, FILES, DERIVED_VOCABULARY

from .contracts import IMMUTABLE, affected_comparisons, apply_delta, baseline_catalog, check_review, check_scope, compact, maintenance_review_scope, retained_adoption_catalog, review_input_pack, reviewer_context_view, row_id, current_finite_research_audit, finite_review_context
from .runtime import ModelRunner
from .state import State, digest, write_json
from .tools import MaintenanceTools
from .joint import synthesis_catalog, validate_joint_analysis, joint_scope_complete, synthesis_scope_complete, render_analysis
from .taxonomy import validate_status_taxonomy
from .evidence_basis import check_evidence_basis, source_requirements
from .analysis_reuse import (qualify_accepted_analysis, recheck_accepted_analysis,
                             require_own_analysis_read, finite_empty_search_certificate, recheck_evidence_pins, stage_index_for)

TERMINAL = {"no_change", "skipped_recent", "staged", "committed", "committed_partial", "rejected"}
RETRYABLE = {"incomplete", "error", "conflict"}


class SettingBudgetError(RuntimeError):
    """Operational cumulative exhaustion; never a scientific no-change claim."""


def _review_source_grants(report, host):
    """Let the independent reviewer read cited scout evidence without refetching it.

    Grants are access to immutable cached text, never a reading or approval credit.
    Decisive source requirements remain unchanged; optional findings may additionally
    name sources that the scout actually read successfully in this attempt.
    """
    mentioned = {sha for finding in report.get("findings", [])
                 for sha in finding.get("source_hashes", [])}
    observed = {row.get("sha256", row.get("source_hash")) for row in host.source_log
                if row.get("tool") == "source_read" and row.get("success")
                and row.get("characters_read", 0) > 0}
    return sorted(source_requirements(report) | (mentioned & observed))


def _previous_validated_scout_draft(tools, context):
    """Extract only a pinned, mechanically checked scout draft as unapproved data."""
    from .runtime import _instructions
    from .tools import _parse_handoff_report
    schema = None
    for event in reversed(tools.get("events", [])):
        if not isinstance(event, dict) or event.get("tool") != "handoff_validate":
            continue
        arguments, result = event.get("arguments"), event.get("result")
        if not isinstance(arguments, dict) or not isinstance(result, dict) or arguments.get("role") != "scout" or \
                result.get("error") or result.get("mechanically_valid") is not True or \
                result.get("scientific_approval") is not False or result.get("prepared_or_review_gate_waived") is not False or \
                result.get("errors") != [] or not isinstance(arguments.get("report_json"), str) or \
                not isinstance(result.get("event_id"), str) or not re.fullmatch(r"[0-9a-f]{64}", result["event_id"]):
            continue
        try:
            if schema is None:
                _, schema, _ = _instructions("scout")
            report, errors = _parse_handoff_report(arguments["report_json"], schema)
            if errors or digest(report) != result.get("report_hash") or \
                    any(report.get(key) != context.get(key) for key in ("setting_id", "base_version", "cutoff")):
                continue
        except (ValueError, TypeError, RecursionError):
            continue
        return {"event_id": result["event_id"], "report_hash": result["report_hash"], "report": report,
                "unapproved": True, "mechanical_validation_only": True, "scientific_approval": False,
                "source_read_credit": False, "baseline_read_credit": False, "approval_inherited": False}
    return None


class Inventory:
    """Read-only inventory. Planning never constructs the native recovering writer."""
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.data = self.root / "data" if (self.root / "data" / "settings").is_dir() else self.root
        self.settings = self.data / "settings"
        if not self.settings.is_dir():
            raise ValueError("Atlas root must contain settings/ or data/settings/")

    def path(self, sid, name="profile.json"):
        if not isinstance(sid, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,199}", sid) or name not in FILES:
            raise ValueError("Invalid native setting ID or filename")
        path = self.settings / sid / name
        if not path.resolve().is_relative_to(self.settings):
            raise ValueError("Setting path escapes Atlas")
        return path

    def version(self, sid):
        hashes = {name: hashlib.sha256(self.path(sid, name).read_bytes()).hexdigest() if self.path(sid, name).is_file() else None for name in FILES}
        return "target-" + digest(hashes) if any(hashes.values()) else None

    def read(self, sid):
        profile = json.loads(self.path(sid).read_text("utf-8"))
        if profile.get("setting_id") != sid:
            raise ValueError("Directory and profile setting_id disagree")
        return profile

    def semantics(self):
        paths = []
        for folder in ("schemas", "registry", "vocabulary"):
            for path in sorted((self.data / folder).rglob("*.json")):
                if folder == "vocabulary" and path.name in DERIVED_VOCABULARY:
                    continue
                if not path.resolve().is_relative_to(self.root):
                    raise ValueError("Atlas semantics path escapes root")
                paths.append(path)
        paths += sorted(self.data.glob("aliases*.json"))
        return digest({str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})

    def ordered_ids(self, mode="current_catalog"):
        rows = []
        for path in self.settings.iterdir():
            if path.is_dir() and (path / "profile.json").is_file():
                profile = self.read(path.name)
                order = profile.get("provenance", {}).get("source_order")
                rows.append((order if isinstance(order, (int, float)) and not isinstance(order, bool) else float("inf"), path.name))
        ordered = [sid for _, sid in sorted(rows)]
        catalog = self.data / "derived" / "catalog.json"
        if mode == "current_catalog" and catalog.is_file():
            if not catalog.resolve().is_relative_to(self.root):
                raise ValueError("Catalog order path escapes Atlas")
            value = json.loads(catalog.read_text("utf-8"))
            available = set(ordered)
            preferred = [r.get("id", r.get("setting_id")) for r in value.get("profiles", []) if isinstance(r, dict)]
            preferred = list(dict.fromkeys(sid for sid in preferred if sid in available))
            return preferred + [sid for sid in ordered if sid not in set(preferred)]
        if mode not in {"current_catalog", "source_order"}:
            raise ValueError("maintenance.order must be current_catalog or source_order")
        return ordered


class Maintenance:
    def __init__(self, config, *, runner=None, runner_factory=None, tools_factory=MaintenanceTools, atlas_factory=Atlas):
        self.config = config
        self.inventory = Inventory(config["atlas"])
        self.state = State(config["workspace"])
        self.state.bind(self.inventory.root)
        self.runner = runner or ModelRunner(config, self.state.root)
        self._runner_factory = runner_factory
        self._injected_runner = runner is not None
        self.tools_factory, self.atlas_factory = tools_factory, atlas_factory
        self._inherited_model_config = self._inherited_model_config_hash()
        resources = Path(__file__).parent / "resources"
        self._resource_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(resources.iterdir()) if p.is_file()}
        self._implementation_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob("*.py"))}
        self.policy = digest({"version": 2, "resources": self._resource_hashes,
                              "implementation": self._implementation_hashes,
                              "backend": config.get("backend"), "model": config.get("model", {}),
                              "maintenance": config.get("maintenance", {}), "budgets": config.get("budgets", {}),
                              "cache": config.get("cache", {}), "literature": config.get("literature", {}),
                              "observability": config.get("observability", {}),
                              "execution": config.get("execution", {}),
                              "inherited_user_model_config_sha256": self._inherited_model_config})

    def _budget_limits(self):
        values = self.config.get("budgets", {})
        names = {"setting_max_seconds": 3600, "setting_max_tool_calls": 256, "setting_max_sessions": 4}
        if not any(name in values for name in names):
            return None
        result = {name: values.get(name, default) for name, default in names.items()}
        if any(isinstance(v, bool) or not isinstance(v, int) or v < 1 for v in result.values()):
            raise ValueError("Cumulative setting budgets must be positive integers")
        return result

    def _prepare_budget_plan(self, plan):
        limits = self._budget_limits()
        if limits is None:
            return plan
        keys = {}
        for sid in plan["setting_ids"]:
            identity = {"atlas_root": plan["atlas_root"], "setting_id": sid,
                        "base_version": plan["versions"][sid], "cutoff": plan["cutoff"], "semantics": plan["semantics"]}
            key = self.state.budget_lineage(identity)
            self.state.budget_snapshot(key, limits)
            keys[sid] = key
        plan.update(budget_keys=keys, budget_limits=limits)
        return plan

    def _begin_setting_budget(self, plan, sid, task_key):
        self._active_budget = None
        key = plan.get("budget_keys", {}).get(sid)
        if key is None:
            if self._budget_limits() is not None:
                raise SettingBudgetError("This plan has no cumulative ledger; create a new plan")
            return
        snapshot = self.state.budget_snapshot(key, plan["budget_limits"])
        if snapshot.get("outstanding"):
            raise SettingBudgetError("An earlier stage has an unsettled budget reservation; inspect its durable evidence before continuing")
        started = time.monotonic()
        self._active_budget = {"key": key, "limits": plan["budget_limits"], "task_key": task_key,
                               "tick": started, "deadline": started + snapshot["remaining_seconds"], "sequence": 0}

    def _account_controller(self):
        active = getattr(self, "_active_budget", None)
        if active is None:
            return None
        now = time.monotonic()
        elapsed = max(0.0, now - active["tick"])
        active["sequence"] += 1
        self.state.charge_controller(active["key"], active["task_key"] + f":controller:{active['sequence']}",
                                     elapsed, limits=active["limits"])
        active["tick"] = time.monotonic()
        return self.state.budget_snapshot(active["key"], active["limits"])

    def _run_role(self, plan, sid, role, context, host, task_key):
        self.runner.last_metrics = {"backend": self.config.get("backend", "responses"), "status": "not_started",
                                    "model_calls": 0, "native_sessions": 0, "tool_calls": 0, "task_key": task_key}
        self._assert_model_binding()
        active = getattr(self, "_active_budget", None)
        if active is None:
            return self.runner.run(role, context, host, task_key)
        snapshot = self._account_controller()
        remaining = min(snapshot["remaining_seconds"], max(0.0, active["deadline"] - time.monotonic()))
        minimum_seconds = self.config.get("budgets", {}).get("min_stage_seconds", 10)
        if remaining < minimum_seconds or snapshot["remaining_tool_calls"] < 1 or snapshot["remaining_sessions"] < 1:
            raise SettingBudgetError("Cumulative setting budget exhausted before another model session")
        # Allocation happens inside runtime before reserving actual paid execution.
        host.setting_budget = {"remaining_seconds": remaining,
            "remaining_tool_calls": snapshot["remaining_tool_calls"], "remaining_sessions": snapshot["remaining_sessions"],
            "lineage_key": active["key"]}
        reservation = None
        reserved_at = None
        paid_started = False
        def reserve(timeout, tool_limit):
            nonlocal reservation, reserved_at
            snapshot = self._account_controller()
            available = min(snapshot["remaining_seconds"], max(0.0, active["deadline"] - time.monotonic()))
            if available < minimum_seconds or snapshot["remaining_sessions"] < 1:
                raise SettingBudgetError("Cumulative setting budget exhausted during input preparation")
            timeout = min(float(timeout), available)
            tool_limit = min(int(tool_limit), snapshot["remaining_tool_calls"])
            if tool_limit < 1:
                raise SettingBudgetError("No cumulative tool-call budget remains")
            reservation = self.state.reserve_stage(active["key"], task_key, role, timeout, tool_limit,
                                                    limits=active["limits"])
            reserved_at = time.monotonic()
            return reservation
        host.reserve_setting_stage = reserve
        def require_admission():
            self._assert_model_binding()
            if reservation is None:
                raise SettingBudgetError("A model process requires a current cumulative budget reservation")
            snapshot = self.state.budget_snapshot(active["key"], active["limits"])
            if not any(row["reservation_id"] == reservation["reservation_id"] for row in snapshot["outstanding"]):
                raise SettingBudgetError("The cumulative reservation no longer authorizes this model process")
        host.require_setting_stage_admitted = require_admission
        def mark_started():
            nonlocal paid_started
            require_admission()
            if not paid_started:
                self.state.mark_stage_started(reservation)
                paid_started = True
        host.mark_setting_stage_started = mark_started
        try:
            return self.runner.run(role, context, host, task_key)
        finally:
            if reservation is not None:
                metrics = getattr(self.runner, "last_metrics", {})
                sessions = metrics.get("native_sessions", 1 if metrics.get("model_calls", 0) else 0)
                elapsed = max(0.0, time.monotonic() - reserved_at)
                receipt = self.state.settle_stage(reservation, elapsed, len(host.events),
                    sessions=int(bool(sessions)), uncertain=bool(metrics.get("paid_outcome_uncertain") or
                    sessions and metrics.get("status") == "failed" and not metrics.get("audit_closed", True)))
                if not receipt["paid_started"]:
                    self.state.charge_controller(active["key"], task_key + ":unstarted-preparation", elapsed,
                                                 limits=active["limits"])
                active["tick"] = time.monotonic()
            self._account_controller()

    def _inherited_model_config_hash(self):
        if self.config.get("backend") != "codex" or self.config.get("model", {}).get("model"):
            return None
        codex_home = Path(os.environ["CODEX_HOME"]).expanduser() if os.environ.get("CODEX_HOME") else Path.home() / ".codex"
        path = codex_home / "config.toml"
        # Hash only: credentials or other user configuration are never copied to
        # a prompt, continuation receipt, output log, or component workspace.
        return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "missing"

    def _assert_model_binding(self):
        if self._inherited_model_config_hash() != self._inherited_model_config:
            raise ValueError("Inherited Codex configuration changed; create a fresh controller and plan")
        root = Path(__file__).parent
        if {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob("*.py"))} != self._implementation_hashes or \
                {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root / "resources").iterdir()) if p.is_file()} != self._resource_hashes:
            raise ValueError("Maintenance implementation or role resources changed; create a fresh controller and plan")

    def plan(self, *, ids=None, cutoff=None, force=False):
        self._assert_model_binding()
        cutoff = cutoff or datetime.now(ZoneInfo(self.config.get("timezone", "UTC"))).date().isoformat()
        date.fromisoformat(cutoff)
        explicit_order = ids is not None
        mode = self.config.get("maintenance", {}).get("order", "current_catalog")
        ids = list(ids) if explicit_order else self.inventory.ordered_ids(mode)
        if not ids or len(set(ids)) != len(ids):
            raise ValueError("Choose a nonempty, duplicate-free list of existing setting IDs")
        versions = {}
        for sid in ids:
            self.inventory.read(sid)
            versions[sid] = self.inventory.version(sid)
        plan = {"atlas_root": str(self.inventory.root), "setting_ids": ids, "versions": versions,
                "semantics": self.inventory.semantics(), "policy": self.policy, "cutoff": cutoff, "force": force}
        with self.state.lock():
            self._prepare_budget_plan(plan)
            run_id = self.state.create(plan)
        return {"run_id": run_id, "settings": len(ids), "cutoff": cutoff,
                "order": "explicit input order" if explicit_order else mode + " (source_order then setting_id fallback)",
                "plan_path": str(self.state.root / "runs" / run_id / "plan.json")}

    def _scope_complete(self, report, context, host, analysis=None):
        analysis = json.loads(report["joint_analysis_json"]) if analysis is None else analysis
        finite = current_finite_research_audit(host, context, report, self.config)
        discovery_complete = bool(finite.get("finite_scope_complete")) if finite is not None else (
            bool(host.search_log) and not getattr(host, "failed", False) and search_complete(host.search_log))
        return report["scope"]["queries_complete"] and not report["scope"]["unresolved_leads"] and \
            set(report["scope"]["examined_comparison_ids"]) == set(context["compact_profile"]["comparison_ids"]) and \
            discovery_complete and not getattr(host, "budget_exhausted", False) and \
            joint_scope_complete(analysis) and synthesis_scope_complete(analysis) and \
            analysis.get("synthesis_coverage", {}).get("literature", {}).get("status") == "finite_scope_complete"

    def _review_committed_receipt(self, pending):
        """Read-only proof of this exact completed native transaction, never a local claim."""
        from oracle_atlas.atlas.store import json_bytes
        prepared, review = pending["prepared"], pending["review"]
        sid, files = prepared["setting_id"], prepared["files"]
        hashes = {name: hashlib.sha256(json_bytes(files[name])).hexdigest() for name in FILES}
        version, bundle = "target-" + digest(hashes), digest(files)
        request_hash = digest({"bundle_hash": bundle, "review": review, "base_version": prepared["base_version"]})
        key_hash = hashlib.sha256(pending["idempotency_key"].encode()).hexdigest()
        native = self.inventory.data / "intake/oracle_atlas_agents"
        def raw(path):
            relative = path.relative_to(self.inventory.root)
            current = self.inventory.root
            for part in relative.parts:
                current /= part
                if current.is_symlink():
                    raise ValueError("Native recovery evidence cannot follow symlinks")
            try:
                return path.read_bytes()
            except OSError as exc:
                raise ValueError("Review-only recovery requires existing persistent native evidence") from exc
        if (native / "pending.json").exists():
            raise ValueError("An unfinished native transaction must be recovered before review-only reconciliation")
        receipt = json.loads(raw(native / "receipts" / (key_hash + ".json")))
        transaction = native / "transactions" / request_hash
        journal = json.loads(raw(transaction / "journal.json"))
        if prepared.get("hashes") != hashes or prepared.get("version") != version or prepared.get("bundle_hash") != bundle or \
                receipt.get("receipt_id") != "atlas-" + request_hash[:24] or receipt.get("status") != "committed" or \
                receipt.get("request_hash") != request_hash or receipt.get("setting_id") != sid or receipt.get("version") != version or \
                receipt.get("base_version") != prepared["base_version"] or receipt.get("bundle_hash") != bundle or receipt.get("files") != hashes:
            raise ValueError("Review-only recovery requires its exact persistent native receipt")
        for key, value in {"transaction_id": request_hash, "request_hash": request_hash, "key_hash": key_hash,
            "setting_id": sid, "bundle_hash": bundle, "base_version": prepared["base_version"], "version": version, "state": "committed"}.items():
            if journal.get(key) != value:
                raise ValueError("Review-only recovery native transaction journal disagrees")
        if set(journal.get("files", {})) != set(FILES) or \
                prepared["base_version"] != "target-" + digest({name: journal["files"][name]["old_sha256"] for name in FILES}):
            raise ValueError("Review-only recovery does not bind the old native five files")
        for name in FILES:
            if journal["files"][name]["new_sha256"] != hashes[name] or \
                    hashlib.sha256(raw(transaction / "new" / name)).hexdigest() != hashes[name] or \
                    hashlib.sha256(raw(self.inventory.path(sid, name))).hexdigest() != hashes[name]:
                raise ValueError("Review-only recovery differs from its exact committed five-file snapshot")
        return receipt

    def _review_rejection_guard(self, origin):
        """A concrete rejection cannot be erased by importing the unchanged source again."""
        for row in self.state.db.execute("SELECT id,plan FROM runs"):
            plan = json.loads(row["plan"])
            prior = plan.get("origins", {}).get(origin["setting_id"]) if plan.get("mode") == "review_only" else None
            if not isinstance(prior, dict) or prior.get("source_task_key") != origin["source_task_key"] or \
                    prior.get("prepared_files_sha256") != origin["prepared_files_sha256"]:
                continue
            for item in self.state.items(row["id"]):
                if item["setting_id"] != origin["setting_id"]:
                    continue
                for index in range(item["attempt"] + 1):
                    path = self._continuation_path(self.state.root / "runs" / row["id"] / f"{item['position']:06d}" / f"attempt-{index:03d}" / "reviewer.json")
                    if path.is_file() and json.loads(path.read_text("utf-8")).get("verdict") == "reject":
                        raise ValueError("This exact candidate has a fresh reviewer rejection; revise it through normal scout research")

    def _review_origin(self, source_run, sid, expected_origin=None, *, recovery=None):
        """Qualify original actual scout evidence; never import reviewer authority."""
        from .analysis_reuse import _native_stage
        self._assert_model_binding()
        original_plan = self.state.plan(source_run)
        if original_plan.get("atlas_root") != str(self.inventory.root) or original_plan.get("semantics") != self.inventory.semantics():
            raise ValueError("Review source Atlas root or semantics changed")
        rows = [row for row in self.state.items(source_run) if row["setting_id"] == sid]
        if len(rows) != 1 or rows[0]["status"] not in {"error", "incomplete"}:
            raise ValueError("Review source must be one unapproved error/incomplete candidate")
        item = rows[0]
        source = self._continuation_path(self.state.root / "runs" / source_run / f"{item['position']:06d}" / f"attempt-{item['attempt']:03d}")
        if any(self._continuation_path(source / name).exists() for name in ("approved.json", "receipt.json")):
            raise ValueError("Approved or published review sources cannot be imported")
        pins = {}
        def load(path):
            path = self._continuation_path(path)
            raw = path.read_bytes()
            pins[str(path)] = hashlib.sha256(raw).hexdigest()
            return json.loads(raw)
        disk_plan = load(self.state.root / "runs" / source_run / "plan.json")
        if disk_plan != original_plan:
            raise ValueError("Review source plan file and queue disagree")
        baseline, context, report, tools, metrics, old_prepared = [load(source / name) for name in
            ("baseline.json", "context.json", "scout.json", "scout-tools.json", "scout-metrics.json", "prepared.json")]
        old_review_path = self._continuation_path(source / "reviewer.json")
        if old_review_path.is_file() and load(old_review_path).get("verdict") != "incomplete":
            raise ValueError("A rejected or approved reviewer verdict cannot be bypassed by review import")
        version = self.inventory.version(sid)
        recovered = False
        if recovery is not None and version != original_plan["versions"].get(sid):
            receipt = self._review_committed_receipt(recovery)
            recovered = receipt["version"] == version and receipt["base_version"] == original_plan["versions"].get(sid)
        source_version = original_plan["versions"].get(sid)
        if (not recovered and (version != source_version or baseline != self.inventory.read(sid))) or \
                context.get("base_version") != source_version or context.get("setting_id") != sid or \
                context.get("cutoff") != original_plan["cutoff"] or context.get("semantics") != original_plan["semantics"] or \
                context.get("policy") != original_plan["policy"] or old_prepared.get("base_version") != source_version:
            raise ValueError("Review source baseline/cutoff/policy identity changed")
        stage = self._continuation_stage(metrics.get("stage_path", ""))
        # Only this explicit review-import lane may carry a closed candidate's
        # unfinished operational scope. It imports no approval/read credit.
        request, frozen, host, closed = _native_stage(self.state.root, stage, "scout", report, pins,
                                                     allow_partial_scout=True if tools.get("failed") else False)
        if metrics != load(stage / "metrics.json"):
            raise ValueError("Original scout controller metrics differ from its actual native stage")
        if request.get("task_key") != f"{source_run}:{item['position']}:{item['attempt']}:scout" or \
                {key: value for key, value in frozen.items() if key != "artifacts"} != context or \
                frozen.get("artifacts", {}).get("baseline") != baseline or host.state() != tools or \
                Path(host.atlas_root).resolve() != self.inventory.root:
            raise ValueError("Review source does not bind its actual original scout task/context/audit")
        if self.config.get("backend") != "codex" or request.get("model") != self.config.get("model", {}) or \
                frozen.get("continuation_identity", {}).get("inherited_user_model_config_sha256") != self._inherited_model_config:
            raise ValueError("Review source model or inherited Codex configuration changed")
        if report.get("outcome") != "candidate_change" or report.get("joint_analysis_reuse") is not None:
            raise ValueError("Review-only requires an actual complete unapproved candidate handoff")
        check_scope(report, frozen, host)
        proposed, delta = apply_delta(baseline, report)
        affected = sorted(affected_comparisons(baseline, proposed, delta))
        analysis = json.loads(report["joint_analysis_json"])
        validate_status_taxonomy(proposed)
        validate_joint_analysis(analysis, baseline, proposed, report=report, expected_comparison_ids=affected, require_current=True)
        check_evidence_basis(report, baseline, proposed, host)
        old_profile = old_prepared.get("files", {}).get("profile.json")
        if not isinstance(old_profile, dict) or old_profile.get("joint_analysis") != analysis:
            raise ValueError("Review source prepared analysis differs from its actual handoff")
        validate_status_taxonomy(old_profile)
        validate_joint_analysis(old_profile["joint_analysis"], baseline, old_profile,
            report=report, expected_comparison_ids=affected, require_current=True)
        from .evidence_basis import check_retention_read_obligations
        check_retention_read_obligations(maintenance_review_scope(baseline, old_profile, report), baseline, old_profile, host, role="scout")
        partial_scope = None
        if host.failed:
            finite = current_finite_research_audit(host, frozen, report, self.config)
            if finite is None:
                raise ValueError("A partial scout import must retain its incomplete finite scope")
            if finite.get("failure_scope_clean") is not True:
                archived_finite = load(source / "finite-research-audit.json")
                if archived_finite != finite:
                    raise ValueError("Original partial scout finite audit changed")
                if report.get("scope", {}).get("queries_complete") is not False or \
                        not report.get("scope", {}).get("unresolved_leads") or \
                        self._scope_complete(report, frozen, host, analysis):
                    raise ValueError("A partial scout import must retain its incomplete finite scope")
                partial_scope = {"kind": "closed_partial_scout_candidate", "state_sha256": digest(host.state()),
                "finite_audit_sha256": digest(finite), "unresolved_failure_ids": list(host.state()["unresolved_failure_ids"]),
                "failed": host.failed, "budget_exhausted": host.budget_exhausted, "scope_complete": False,
                "new_scout_sessions": 0, "approval_inherited": False, "source_read_credit": False,
                "note": "Original closed candidate has unresolved operational work. All original findings/proofs are rechecked; only a new clean independent reviewer can authorize partial adoption."}
        origin = {"version": 1, "source_run": source_run, "setting_id": sid, "position": item["position"], "attempt": item["attempt"],
            "source_attempt": str(source.relative_to(self.state.root)), "source_task_key": request["task_key"],
            "source_stage": str(stage.relative_to(self.state.root)), "source_policy": original_plan["policy"],
            "source_cutoff": original_plan["cutoff"], "base_version": source_version, "semantics": original_plan["semantics"],
            "model_sha256": digest(request["model"]), "instructions": request["instructions"], "closed": closed,
            "prepared_files_sha256": {name: digest(old_prepared["files"][name]) for name in FILES},
            "source_file_sha256": {str(Path(path).relative_to(self.state.root)): sha for path, sha in sorted(pins.items())},
            "new_scout_sessions": 0, "original_scout_witness": True, "approval_inherited": False, "reviewer_read_credit": False}
        if partial_scope is not None:
            origin["partial_scout_scope"] = partial_scope
        if expected_origin is not None and origin != expected_origin:
            raise ValueError("Pinned original scout witness changed; no reviewer call was started")
        self._review_rejection_guard(origin)
        return origin, baseline, frozen, report, host

    def plan_review(self, *, source_run, ids, cutoff=None):
        """Explicitly plan a fresh reviewer using exact original scout witnesses."""
        if not isinstance(ids, (list, tuple)) or not ids or len(set(ids)) != len(ids):
            raise ValueError("Choose a nonempty, duplicate-free review-only ID list")
        with self.state.lock():
            origins = {sid: self._review_origin(source_run, sid)[0] for sid in ids}
            source_cutoff = self.state.plan(source_run)["cutoff"]
            if cutoff is not None and cutoff != source_cutoff:
                raise ValueError("Review-only cutoff must equal the original scout cutoff")
            plan = {"atlas_root": str(self.inventory.root), "setting_ids": list(ids),
                "versions": {sid: origins[sid]["base_version"] for sid in ids}, "semantics": self.inventory.semantics(),
                "policy": self.policy, "cutoff": source_cutoff, "force": True, "mode": "review_only",
                "source_run": source_run, "origins": origins}
            source_plan = self.state.plan(source_run)
            if self._budget_limits() is not None:
                if not source_plan.get("budget_keys"):
                    raise ValueError("Cumulative-budget review requires a budgeted source plan; legacy work cannot be silently imported at zero cost")
                if source_plan.get("budget_limits") != self._budget_limits():
                    raise ValueError("Review-only must retain the original cumulative setting caps")
                plan.update(budget_keys={sid: source_plan["budget_keys"][sid] for sid in ids},
                            budget_limits=source_plan["budget_limits"])
            run_id = self.state.create(plan)
        return {"run_id": run_id, "mode": "review_only", "settings": len(ids), "cutoff": source_cutoff,
                "new_scout_sessions": 0, "plan_path": str(self.state.root / "runs" / run_id / "plan.json")}

    def _step_review(self, plan, sid, directory, task_key, commit):
        origin, profile, context, report, host = self._review_origin(plan["source_run"], sid, plan["origins"][sid])
        if plan["cutoff"] != origin["source_cutoff"] or plan["versions"][sid] != origin["base_version"]:
            raise ValueError("Review-only plan changed its original cutoff or baseline")
        source = self._continuation_path(origin["source_attempt"])
        for name in ("baseline.json", "context.json", "scout.json", "scout-tools.json", "scout-metrics.json"):
            raw = (source / name).read_bytes()
            if hashlib.sha256(raw).hexdigest() != origin["source_file_sha256"][str((source / name).relative_to(self.state.root))]:
                raise ValueError("Original scout copy changed before review")
            (directory / name).write_bytes(raw)
        write_json(directory / "scout-origin.json", origin)
        write_json(directory / "review-origin.json", {"origin_hash": digest(origin), "original_scout_witness": True,
            "new_scout_sessions": 0, "approval_inherited": False, "reviewer_read_credit": False})
        return self._post_scout(plan, sid, directory, task_key, commit, profile, origin["base_version"], context, report, host, review_origin=origin)

    def _scope_record(self, report, host, analysis=None):
        """Save the actual finite search and its refinements with the successful watermark."""
        analysis = json.loads(report["joint_analysis_json"]) if analysis is None else analysis
        finite = current_finite_research_audit(host, getattr(host, "context", {}), report, self.config)
        return {**report["scope"], "query_audit": host.search_log,
                **({"finite_research": finite} if finite is not None else {}),
                "joint_analysis_hash": digest(analysis),
                "joint_domain_map": analysis["domain_map"],
                "joint_target": analysis["target"],
                "finite_search_complete": bool(report["scope"]["queries_complete"] and (finite.get("finite_scope_complete") if finite is not None else search_complete(host.search_log))),
                "joint_accounting_complete": joint_scope_complete(analysis),
                "synthesis_coverage": analysis.get("synthesis_coverage", {"status": "legacy_unknown", "gap_basis": "registered_envelope"}),
                "interpretation": "Completion is a finite scoped check with explicit parameter-domain accounting, not global literature exhaustiveness or closed optimality.",
                "decisive_source_reads": sorted({r.get("source_hash") for r in host.source_log
                    if r.get("tool") == "source_read" and r.get("success") and r.get("characters_read", 0) > 0})}

    def _prior_work(self, sid, version):
        """Carry short unresolved work forward; never load a previous conversation graph."""
        rows = self.state.db.execute("SELECT status,result FROM items WHERE setting_id=? AND result IS NOT NULL AND status IN ('error','incomplete','running','committed_partial') ORDER BY rowid DESC LIMIT 8", (sid,)).fetchall()
        for row in rows:
            status, raw_result = row
            result = json.loads(raw_result)
            path = Path(result.get("artifact_path", ""))
            if not path.is_absolute() or not path.resolve().is_relative_to(self.state.root):
                continue
            if not (path / "context.json").is_file() or not (path / "scout-tools.json").is_file():
                continue
            context = json.loads((path / "context.json").read_text())
            if context.get("semantics") != self.inventory.semantics():
                continue
            own_partial = status == "committed_partial"
            if own_partial:
                # Publication changes the baseline. Carry only the unfinished notes when
                # this exact transaction produced the still-current native five files.
                receipt = result.get("receipt", {})
                if receipt.get("setting_id") != sid or receipt.get("version") != version or not (path / "prepared.json").is_file():
                    continue
                prepared = json.loads((path / "prepared.json").read_text())
                if prepared.get("bundle_hash") != receipt.get("bundle_hash") or \
                        digest(prepared.get("files", {}).get("profile.json")) != digest(self.inventory.read(sid)):
                    continue
            elif context.get("base_version") != version:
                continue
            report = json.loads((path / "scout.json").read_text()) if (path / "scout.json").is_file() else {}
            tools = json.loads((path / "scout-tools.json").read_text()) if (path / "scout-tools.json").is_file() else {}
            if not report and not tools.get("events"):
                # A failed local startup contains no research progress or
                # scientific clue to carry into the next independent scout.
                continue
            try:
                previous_analysis = json.loads(report.get("joint_analysis_json") or "{}")
            except (ValueError, TypeError):
                previous_analysis = {}
            findings = [] if own_partial else [{**f, "reason": f["reason"][:1000]} for f in report.get("findings", [])[:10]]
            pending = {"note": "Unapproved working memory from the exact baseline and Atlas semantics. The prior policy is separately indicated; recheck pending evidence under current rules. Any last_mechanical_error is controller diagnostic metadata only, not scientific evidence, an expected result, or approval.",
                    "after_own_partial_commit": own_partial,
                    "prior_policy_matches": context.get("policy") == self.policy,
                    "policy_note": "A changed implementation/policy permits unapproved working notes only; no former approval or successful-check watermark is inherited.",
                    "prior_cutoff": context["cutoff"], "prior_window_start": context.get("window_start"),
                    "unresolved_leads": report.get("scope", {}).get("unresolved_leads", [])[:20], "findings": findings,
                    "joint_pending_obligations": previous_analysis.get("pending_obligations", [])[:20],
                    "normalization_requests": previous_analysis.get("normalization_requests", [])[:8],
                    "joint_pending_truncated": len(previous_analysis.get("pending_obligations", [])) > 20 or len(previous_analysis.get("normalization_requests", [])) > 8,
                    "queries": [{k: r.get(k) for k in ("provider", "query", "year", "cursor", "limit", "next_cursor", "fetched_epoch", "output_truncated")} for r in tools.get("search_log", [])[:12]],
                    "source_hashes": sorted({r["source_hash"] for r in tools.get("source_log", []) if r.get("success") and r.get("source_hash")})[:24]}
            # run() changes an error item to running while retaining its previous
            # result. Only that recorded controller-error receipt, matched to its
            # own error.json, may supply diagnostic feedback in either state.
            if not own_partial and status in {"error", "running"}:
                fields = ("error_type", "error", "artifact_path")
                if all(isinstance(result.get(k), str) and result[k] for k in fields):
                    error_path = path / "error.json"
                    if not error_path.is_symlink() and error_path.resolve().parent == path.resolve() and error_path.is_file():
                        try:
                            archived_error = json.loads(error_path.read_text("utf-8"))
                        except (OSError, ValueError):
                            archived_error = None
                        if isinstance(archived_error, dict) and all(archived_error.get(k) == result[k] for k in fields) and \
                                re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", result["error_type"]):
                            pending["last_mechanical_error"] = {"type": result["error_type"][:120],
                                                                "message": result["error"][:1000]}
            return pending
        return None

    def _continuation_identity(self, plan, sid):
        """Exact scientific and configured-model boundary, never an approval."""
        return {"schema_version": 1, "setting_id": sid, "base_version": plan["versions"][sid],
                "cutoff": plan["cutoff"], "semantics": plan["semantics"], "policy": self.policy,
                "backend": self.config.get("backend", "responses"),
                "inherited_user_model_config_sha256": self._inherited_model_config,
                "model_config_sha256": digest(self.config.get("model", {})),
                "configuration_sha256": digest({"backend": self.config.get("backend", "responses"),
                    "model": self.config.get("model", {}), "observability": self.config.get("observability", {})})}

    def _continuation_path(self, path):
        """Workspace evidence must be real files, including every parent component."""
        path = Path(path)
        if not path.is_absolute():
            path = self.state.root / path
        try:
            relative = path.relative_to(self.state.root)
        except ValueError as exc:
            raise ValueError("Continuation evidence escapes its workspace") from exc
        current = self.state.root
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError("Continuation evidence cannot follow symlinks")
        if not path.resolve().is_relative_to(self.state.root):
            raise ValueError("Continuation evidence resolves outside its workspace")
        return path

    def _continuation_file_hash(self, path):
        path = self._continuation_path(path)
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _continuation_stage(self, relative):
        stage = self._continuation_path(relative)
        if stage.parent != self.state.root / "model":
            raise ValueError("Continuation must name one native model stage in this workspace")
        for name in ("request.json", "tools.json", "tools-closed.json", "tools-terminal.json", "tools-events.jsonl",
                     "checkpoint.json", "controller-checkpoint.json", "continuation-terminal.json", "codex-receipt.json"):
            self._continuation_path(stage / name)
        return stage

    def _capture_continuation(self, plan, sid, directory, task_key):
        """Pin a stopped scout's unapproved work; failure never changes its outcome."""
        from .runtime import continuation_stage_snapshot
        identity = self._continuation_identity(plan, sid)
        binding = digest(identity)
        required = ("baseline.json", "context.json", "scout-tools.json", "scout-metrics.json")
        for name in required:
            self._continuation_path(directory / name)
        context = json.loads((directory / "context.json").read_text("utf-8"))
        if context.get("continuation_identity") != identity or context.get("resume_binding") != binding:
            raise ValueError("Stopped attempt has no exact current continuation identity; create a fresh plan")
        metrics = json.loads((directory / "scout-metrics.json").read_text("utf-8"))
        if not isinstance(metrics.get("stage_path"), str):
            raise ValueError("Stopped scout has no verifiable native stage; use an explicit fresh attempt")
        stage = self._continuation_stage(metrics["stage_path"])
        snapshot = continuation_stage_snapshot(stage, expected_task_key=task_key + ":scout",
                                                expected_resume_binding=binding)
        request = json.loads(self._continuation_path(stage / "request.json").read_text("utf-8"))
        request_context = request.get("context", {})
        baseline = json.loads((directory / "baseline.json").read_text("utf-8"))
        tools = json.loads((directory / "scout-tools.json").read_text("utf-8"))
        if request.get("role") != "scout" or request_context.get("continuation_identity") != identity or \
                {k: v for k, v in request_context.items() if k != "frozen_artifact_hashes"} != context or \
                request_context.get("frozen_artifact_hashes", {}).get("baseline") != digest(baseline) or \
                digest(tools) != digest(json.loads(self._continuation_path(stage / "tools.json").read_text("utf-8"))):
            raise ValueError("Continuation stage, frozen baseline and controller tool evidence disagree")
        pins = {name: self._continuation_file_hash(directory / name) for name in required}
        for name in ("scout.json", "error.json"):
            path = self._continuation_path(directory / name)
            if path.is_file():
                pins[name] = self._continuation_file_hash(path)
        return {"schema_version": 1, "eligible": True, "identity": identity, "resume_binding": binding,
                "source_attempt": str(directory.relative_to(self.state.root)), "source_task_key": task_key + ":scout",
                "stage_path": str(stage.relative_to(self.state.root)), "runtime_snapshot": snapshot,
                "runtime_snapshot_sha256": digest(snapshot), "attempt_file_sha256": pins,
                "source_read_credit": False, "baseline_read_credit": False, "approval_inherited": False,
                "note": "A continuation starts a new paid-capable attempt and independent review. Prior work is unapproved planning data only."}

    def _save_continuation(self, plan, sid, directory, task_key):
        try:
            value = self._capture_continuation(plan, sid, directory, task_key)
        except (ValueError, OSError, KeyError, TypeError, RuntimeError) as exc:
            value = {"schema_version": 1, "eligible": False, "reason": str(exc)[:1000]}
        path = self._continuation_path(directory / "continuation.json")
        if path.exists():
            if json.loads(path.read_text("utf-8")) != value:
                raise ValueError("An existing continuation receipt is immutable; use a new attempt")
        else:
            write_json(path, value)
        return {"eligible": value["eligible"], "path": str(path),
                **({"resume_binding": value["resume_binding"]} if value["eligible"] else {"reason": value["reason"]})}

    def _load_continuation(self, run_id, sid):
        self._assert_model_binding()
        plan = self.state.plan(run_id)
        if plan["policy"] != self.policy or plan["semantics"] != self.inventory.semantics():
            raise ValueError("Policy or Atlas semantics changed; create a fresh plan")
        if plan.get("atlas_root") != str(self.inventory.root):
            raise ValueError("Continuation plan belongs to another Atlas")
        matches = [item for item in self.state.items(run_id) if item["setting_id"] == sid]
        if len(matches) != 1:
            raise ValueError("Choose one setting in this frozen run")
        item = matches[0]
        if item["status"] not in {"error", "incomplete"}:
            raise ValueError("Continuation is available only for stopped error/incomplete items")
        if self.inventory.version(sid) != plan["versions"][sid]:
            raise ValueError("Baseline changed; create a fresh plan")
        directory = self._continuation_path(self.state.root / "runs" / run_id / f"{item['position']:06d}" / f"attempt-{item['attempt']:03d}")
        for name in ("approved.json", "receipt.json"):
            if self._continuation_path(directory / name).exists():
                raise ValueError("Approved or published bundles use apply, never checkpoint continuation")
        path = self._continuation_path(directory / "continuation.json")
        saved = json.loads(path.read_text("utf-8"))
        if saved.get("eligible") is not True:
            raise ValueError(saved.get("reason", "No verified continuation checkpoint is available"))
        task_key = f"{run_id}:{item['position']}:{item['attempt']}"
        current = self._capture_continuation(plan, sid, directory, task_key)
        if current != saved:
            raise ValueError("Pinned continuation evidence changed; no model call was started")
        self._continuation_mechanical_error(saved, directory)
        return plan, item, directory, saved

    def _continuation_mechanical_error(self, saved, source):
        """Bounded controller feedback, cross-bound to its task/queue/receipt."""
        expected_hash = saved.get("attempt_file_sha256", {}).get("error.json")
        if expected_hash is None:
            return None
        match = re.fullmatch(r"([0-9a-f]{24}):([0-9]+):([0-9]+):scout", str(saved.get("source_task_key", "")))
        if match is None:
            raise ValueError("Controller diagnostic has no exact source scout task")
        run_id, position, attempt = match.group(1), int(match.group(2)), int(match.group(3))
        if source.relative_to(self.state.root).parts != ("runs", run_id, f"{position:06d}", f"attempt-{attempt:03d}"):
            raise ValueError("Controller diagnostic source task and attempt path disagree")
        error_path = self._continuation_path(source / "error.json")
        if self._continuation_file_hash(error_path) != expected_hash:
            raise ValueError("Pinned controller diagnostic changed")
        receipt = json.loads(self._continuation_path(source / "continuation.json").read_text("utf-8"))
        if receipt != saved:
            raise ValueError("Controller diagnostic does not bind its exact continuation receipt")
        rows = [item for item in self.state.items(run_id) if item["position"] == position]
        if len(rows) != 1 or rows[0]["setting_id"] != saved["identity"]["setting_id"] or \
                rows[0]["status"] not in {"error", "running"} or rows[0]["attempt"] not in {attempt, attempt + 1}:
            raise ValueError("Controller diagnostic source queue state does not match")
        result = json.loads(rows[0]["result"]) if rows[0]["result"] else None
        error = json.loads(error_path.read_text("utf-8"))
        fields = ("error_type", "error", "artifact_path")
        if not isinstance(result, dict) or not isinstance(error, dict) or \
                any(not isinstance(error.get(key), str) or not error[key] or result.get(key) != error[key] for key in fields) or \
                error["artifact_path"] != str(source) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", error["error_type"]):
            raise ValueError("Controller diagnostic does not match its recorded source error")
        binding = result.get("continuation")
        if not isinstance(binding, dict) or binding.get("eligible") is not True or \
                binding.get("path") != str(source / "continuation.json") or binding.get("resume_binding") != saved["resume_binding"]:
            raise ValueError("Controller diagnostic queue result does not bind the continuation receipt")
        return {"type": error["error_type"][:120], "message": error["error"][:1000],
                "source_error_sha256": expected_hash,
                "note": "Controller diagnostic metadata only; not scientific evidence, an expected scientific result, proof, or approval."}

    def checkpoint(self, run_id, *, setting_id):
        """Inspect resumability without starting a backend or reusing an approval."""
        with self.state.lock():
            plan, item, directory, saved = self._load_continuation(run_id, setting_id)
            return {"run_id": run_id, "setting_id": setting_id, "attempt": item["attempt"],
                    "eligible": True, "cutoff": plan["cutoff"], "base_version": plan["versions"][setting_id],
                    "checkpoint_path": str(directory / "continuation.json"), "checkpoint_sha256": digest(saved),
                    "source_stage_path": saved["stage_path"], "new_attempt_requires_explicit_continue": True,
                    "new_model_calls_possible": True, "source_read_credit": False, "approval_inherited": False}

    def reconcile_startup(self, run_id, *, setting_id, evidence_snapshot=None, evidence_sha256=None):
        """Append a credit only for a narrowly proven pre-model local startup failure.

        Original plans, metrics, tool records and budget settlements are retained.
        This command never starts a model, qualifies a source or adopts a result.
        """
        from .runtime import known_native_startup_failure
        import math
        with self.state.lock():
            attestation = None
            if evidence_snapshot is not None or evidence_sha256 is not None:
                if evidence_snapshot is None or not isinstance(evidence_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", evidence_sha256):
                    raise ValueError("An operator evidence snapshot requires its explicit exact SHA256")
                evidence_path = self._continuation_path(evidence_snapshot)
                raw = evidence_path.read_bytes()
                if hashlib.sha256(raw).hexdigest() != evidence_sha256:
                    raise ValueError("Operator startup evidence snapshot changed")
                attestation = json.loads(raw)
                if attestation.get("kind") != "operator_verified_startup_snapshot" or \
                        attestation.get("run_id") != run_id or attestation.get("setting_id") != setting_id:
                    raise ValueError("Operator startup evidence snapshot belongs to another task")
            plan = self.state.plan(run_id)
            if plan.get("atlas_root") != str(self.inventory.root) or self.inventory.semantics() != plan["semantics"]:
                raise ValueError("Startup reconciliation requires the original Atlas and semantics")
            matches = [row for row in self.state.items(run_id) if row["setting_id"] == setting_id]
            if len(matches) != 1 or matches[0]["status"] not in {"error", "incomplete"}:
                raise ValueError("Choose one failed, unapproved setting attempt")
            item = matches[0]
            if self.inventory.version(setting_id) != plan["versions"][setting_id]:
                raise ValueError("Startup reconciliation baseline changed")
            directory = self._continuation_path(self.state.root / "runs" / run_id / f"{item['position']:06d}" / f"attempt-{item['attempt']:03d}")
            if any((directory / name).exists() for name in ("approved.json", "receipt.json")):
                raise ValueError("An approved or published attempt cannot be refunded as unstarted")
            reconciled = []
            for role in ("scout", "reviewer"):
                metrics_path = self._continuation_path(directory / (role + "-metrics.json"))
                if not metrics_path.is_file():
                    continue
                metrics = json.loads(metrics_path.read_text("utf-8"))
                if metrics.get("status") != "failed" or not isinstance(metrics.get("stage_path"), str):
                    continue
                stage = self._continuation_stage(metrics["stage_path"])
                request = json.loads((stage / "request.json").read_text("utf-8"))
                key = f"{run_id}:{item['position']}:{item['attempt']}:{role}"
                if digest(request) != stage.name or request.get("task_key") != key or request.get("role") != role or \
                        request.get("backend") != "codex" or request["context"].get("setting_id") != setting_id or \
                        request["context"].get("base_version") != plan["versions"][setting_id] or \
                        request["context"].get("policy") != plan["policy"] or request["context"].get("cutoff") != plan["cutoff"]:
                    raise ValueError("Startup proof does not bind the exact failed native task")
                if known_native_startup_failure(stage) != "local_state_initialization_denied":
                    continue
                current = json.loads((stage / "metrics.json").read_text("utf-8"))
                status = json.loads((stage / "live-status.json").read_text("utf-8"))
                reservation = json.loads((stage / "setting-budget-reservation.json").read_text("utf-8"))
                if current != metrics or status.get("process", {}).get("state") != "exited" or \
                        status["process"].get("returncode") != 1 or metrics.get("tool_calls") != 0 or \
                        reservation.get("task_key") != key or reservation.get("role") != role or \
                        reservation.get("budget_key") != plan.get("budget_keys", {}).get(setting_id):
                    raise ValueError("Startup proof contradicts its stopped process, metrics or cumulative reservation")
                observed = metrics.get("elapsed_seconds")
                if isinstance(observed, bool) or not isinstance(observed, (int, float)) or not math.isfinite(observed) or observed < 0:
                    raise ValueError("Startup proof has no valid observed elapsed time")
                # Reject replaced logs after the immutable settlement, even if a
                # caller resets their modification time. ctime is OS maintained.
                row = self.state.db.execute("SELECT settlement FROM budget_stages WHERE reservation_id=?", (reservation["reservation_id"],)).fetchone()
                if row is None or not row["settlement"]:
                    raise ValueError("Startup proof requires an existing immutable settlement")
                settled = json.loads(row["settlement"])
                cutoff_epoch = datetime.fromisoformat(settled["settled_at"]).timestamp()
                names = ("request.json", "stderr.log", "events.jsonl", "metrics.json", "live-status.json",
                         "codex-receipt.json", "setting-budget-reservation.json")
                pins = {}
                metadata_conflicts = {}
                for name in names:
                    path = self._continuation_path(stage / name)
                    relative = str(path.relative_to(self.state.root))
                    actual_hash = self._continuation_file_hash(path)
                    if attestation is not None and attestation.get("source_pins", {}).get(relative) != actual_hash:
                        raise ValueError("A startup file differs from the explicitly pinned operator snapshot")
                    if path.stat().st_ctime > cutoff_epoch + 0.001 and attestation is None:
                        raise ValueError("Native startup proof was replaced after budget settlement")
                    if path.stat().st_ctime > cutoff_epoch + 0.001:
                        metadata_conflicts[relative] = {"ctime_after_settlement_seconds": path.stat().st_ctime - cutoff_epoch,
                                                       "mtime_after_settlement_seconds": path.stat().st_mtime - cutoff_epoch}
                    pins[relative] = actual_hash
                proof = {"kind": "readonly_verified_native_startup_not_started", "reservation_id": reservation["reservation_id"],
                         "task_key": key, "role": role, "stage_path": str(stage.relative_to(self.state.root)),
                         "failure_kind": "local_state_initialization_denied", "source_pins": pins,
                         "model_events": 0, "tool_calls": 0, "scientific_approval": False}
                if attestation is not None:
                    if set(attestation.get("source_pins", {})) != set(pins):
                        raise ValueError("Operator startup snapshot must pin exactly this stage's evidence files")
                    proof.update(operator_evidence_sha256=evidence_sha256, metadata_conflicts=metadata_conflicts,
                                 operator_attestation_only=True, original_artifacts_or_settlements_rewritten=False)
                receipt = self.state.reconcile_not_started(reservation, observed, proof)
                path = directory / (role + "-startup-reconciliation.json")
                if path.exists() and json.loads(path.read_text("utf-8")) != receipt:
                    raise ValueError("A startup reconciliation receipt is immutable")
                if not path.exists():
                    write_json(path, receipt)
                reconciled.append(receipt)
            if not reconciled:
                raise ValueError("No narrowly verified unstarted native initialization failure is available")
            return {"run_id": run_id, "setting_id": setting_id, "model_calls_started": 0,
                    "original_records_preserved": True, "adjustments": reconciled,
                    "cumulative_budget": self.state.budget_snapshot(plan["budget_keys"][setting_id])}

    def _continuation_work(self, saved, context):
        """Expose a frozen draft as data; a fresh host owns every new read credit."""
        from .runtime import continuation_stage_snapshot
        if context["continuation_identity"] != saved.get("identity") or context["resume_binding"] != saved.get("resume_binding"):
            raise ValueError("Continuation identity no longer matches this attempt")
        source = self._continuation_path(saved["source_attempt"])
        for name, expected in saved["attempt_file_sha256"].items():
            if name not in {"baseline.json", "context.json", "scout-tools.json", "scout-metrics.json", "scout.json", "error.json"} or \
                    self._continuation_file_hash(source / name) != expected:
                raise ValueError("Continuation source pins changed before the new model call")
        stage = self._continuation_stage(saved["stage_path"])
        current = continuation_stage_snapshot(stage, expected_task_key=saved["source_task_key"],
                                              expected_resume_binding=saved["resume_binding"])
        if current != saved["runtime_snapshot"] or digest(current) != saved["runtime_snapshot_sha256"]:
            raise ValueError("Continuation terminal audit changed before the new model call")
        checkpoint_path = self._continuation_path(stage / "checkpoint.json")
        checkpoint = json.loads(checkpoint_path.read_text("utf-8")) if checkpoint_path.is_file() else None
        if checkpoint is not None and not isinstance(checkpoint, dict):
            raise ValueError("Continuation checkpoint must be an unapproved object")
        report_path = self._continuation_path(source / "scout.json")
        report = json.loads(report_path.read_text("utf-8")) if report_path.is_file() else None
        tools = json.loads((source / "scout-tools.json").read_text("utf-8"))
        source_hashes = sorted({row.get("source_hash") for row in tools.get("source_log", [])
                                if isinstance(row, dict) and row.get("success") and isinstance(row.get("source_hash"), str)})
        work = {"note": "UNAPPROVED previous scout work. Drafts, queries and source handles are planning data, not proof of completion, reads, or review. Recheck decisive premises and submit a complete new handoff under all current gates.",
                "checkpoint": checkpoint, "previous_scout_report": report,
                "previous_validated_draft": _previous_validated_scout_draft(tools, context),
                "query_history": copy.deepcopy(tools.get("search_log", [])), "source_handles": source_hashes,
                "previous_failed": bool(tools.get("failed")), "previous_budget_exhausted": bool(tools.get("budget_exhausted")),
                "previous_unresolved_failure_ids": copy.deepcopy(tools.get("unresolved_failure_ids", []))}
        diagnostic = self._continuation_mechanical_error(saved, source)
        if diagnostic is not None:
            work["last_mechanical_error"] = diagnostic
        context["artifacts"]["continuation_work"] = work
        context["continuation"] = {"source_attempt": saved["source_attempt"], "source_task_key": saved["source_task_key"],
            "runtime_snapshot_sha256": saved["runtime_snapshot_sha256"], "source_read_credit": False,
            "baseline_read_credit": False, "approval_inherited": False,
            "work": {"provided_complete": False, "artifact": "continuation_work", "pointer": "", "content_hash": digest(work)}}
        # Nonempty pending_work also disables the accepted-analysis shortcut. No
        # former events are imported into this fresh host's evidence or budgets.
        pending = {"note": work["note"], "explicit_checkpoint_continuation": True,
                "prior_policy_matches": True, "prior_cutoff": saved["identity"]["cutoff"],
                "source_hashes": source_hashes, "source_handles_are_read_credit": False,
                "work": copy.deepcopy(context["continuation"]["work"])}
        if diagnostic is not None:
            pending["last_mechanical_error"] = copy.deepcopy(diagnostic)
        return pending

    def continue_run(self, run_id, *, setting_id, commit=False):
        """Explicitly start exactly one new attempt from verified unapproved work."""
        with self.state.lock():
            plan, item, source, saved = self._load_continuation(run_id, setting_id)
            attempt = item["attempt"] + 1
            directory = self._continuation_path(source.parent / f"attempt-{attempt:03d}")
            if directory.exists():
                raise ValueError("Next attempt already exists; inspect it rather than silently rerunning")
            # Check all pins again immediately before marking a new attempt running.
            self._load_continuation(run_id, setting_id)
            directory.mkdir()
            write_json(directory / "continuation-source.json", saved)
            self.state.save(run_id, item["position"], "running", json.loads(item["result"]) if item["result"] else None, attempt=attempt)
            task_key = f"{run_id}:{item['position']}:{attempt}"
            continued_item = {**item, "attempt": attempt}
            status, result = self._execute_item(plan, continued_item, directory, task_key, commit, continuation=saved)
            self.state.save(run_id, item["position"], status, result)
            summary = self.state.summary(run_id)
            write_json(self.state.root / "runs" / run_id / "summary.json", summary)
            return summary

    def _worker(self):
        """Construct every mutable controller/SQLite/runner object in its owning thread."""
        runner = self._runner_factory() if self._runner_factory is not None else None
        return type(self)(self.config, runner=runner, runner_factory=self._runner_factory,
                          tools_factory=self.tools_factory, atlas_factory=self.atlas_factory)

    def _execute_item(self, plan, item, directory, task_key, commit, *, continuation=None, workers=1):
        from .scheduling import record_scheduler_event
        from .state import CumulativeBudgetError
        from .runtime import MaintenanceBudgetError
        sid = item["setting_id"]
        record_scheduler_event(self.state.root, task_key.split(":")[0], "item_started", setting_id=sid,
                               position=item["position"], attempt=item["attempt"], workers=workers)
        self._active_budget = None
        try:
            self._begin_setting_budget(plan, sid, task_key)
            status, result = self._step(plan, sid, directory, task_key, commit, continuation=continuation)
        except Exception as exc:
            exhausted = isinstance(exc, (SettingBudgetError, CumulativeBudgetError, MaintenanceBudgetError))
            status = "incomplete" if exhausted else "conflict" if "conflict" in type(exc).__name__.lower() else "error"
            result = {"error_type": type(exc).__name__, "error": str(exc)[:3000], "artifact_path": str(directory)}
            if exhausted:
                result["budget_exhausted"] = True
            write_json(directory / "error.json", result)
        finally:
            try:
                self._account_controller()
            finally:
                record_scheduler_event(self.state.root, task_key.split(":")[0], "item_finished", setting_id=sid,
                                       position=item["position"], attempt=item["attempt"], workers=workers)
        if status in {"incomplete", "error"}:
            result["continuation"] = self._save_continuation(plan, sid, directory, task_key)
        if plan.get("budget_keys", {}).get(sid):
            result["cumulative_budget"] = self.state.budget_snapshot(plan["budget_keys"][sid], plan["budget_limits"])
            write_json(directory / "cumulative-budget.json", result["cumulative_budget"])
        return status, result

    def _thread_item(self, plan, item, directory, task_key, commit, workers):
        worker = None
        try:
            worker = self._worker()
            if worker.policy != plan["policy"]:
                raise ValueError("Worker policy or inherited model configuration changed; create a fresh plan")
            return worker._execute_item(plan, item, directory, task_key, commit, workers=workers)
        except Exception as exc:
            result = {"error_type": type(exc).__name__, "error": str(exc)[:3000], "artifact_path": str(directory)}
            write_json(directory / "worker-error.json", result)
            return "error", result
        finally:
            if worker is not None:
                worker.state.db.close()

    def run(self, run_id, *, limit=None, retry_incomplete=False, commit=False, jobs=None):
        from .scheduling import record_scheduler_event
        self._assert_model_binding()
        if limit is not None and (isinstance(limit, bool) or not isinstance(limit, int) or limit < 1):
            raise ValueError("limit must be positive")
        maximum = self.config.get("execution", {}).get("max_workers", 1)
        jobs = maximum if jobs is None else jobs
        if isinstance(maximum, bool) or not isinstance(maximum, int) or not 1 <= maximum <= 64 or \
                isinstance(jobs, bool) or not isinstance(jobs, int) or not 1 <= jobs <= maximum:
            raise ValueError("jobs must be positive and at most the configured max_workers (maximum 64)")
        if jobs > 1 and self._injected_runner and self._runner_factory is None:
            raise ValueError("Parallel execution requires an independent runner_factory; a mutable runner cannot be shared")
        with self.state.lock():
            plan = self.state.plan(run_id)
            if plan["policy"] != self.policy or plan["semantics"] != self.inventory.semantics():
                raise ValueError("Policy or Atlas semantics changed; create a fresh plan")
            eligible = [item for item in self.state.items(run_id)
                        if item["status"] not in TERMINAL and (item["status"] not in RETRYABLE or retry_incomplete)]
            if limit is not None:
                eligible = eligible[:limit]
            workers = min(jobs, max(1, len(eligible)))
            record_scheduler_event(self.state.root, run_id, "batch_started", workers=workers)
            def prepare(item):
                item = dict(item)
                item["attempt"] += int(item["status"] in RETRYABLE)
                previous = json.loads(item["result"]) if item["result"] else None
                self.state.save(run_id, item["position"], "running", previous, attempt=item["attempt"])
                directory = self.state.root / "runs" / run_id / f"{item['position']:06d}" / f"attempt-{item['attempt']:03d}"
                directory.mkdir(parents=True, exist_ok=True)
                return item, directory, f"{run_id}:{item['position']}:{item['attempt']}"
            def finish(item, result):
                self.state.save(run_id, item["position"], *result)
                write_json(self.state.root / "runs" / run_id / "summary.json", self.state.summary(run_id))
            try:
                if workers == 1:
                    for item in eligible:
                        item, directory, key = prepare(item)
                        finish(item, self._execute_item(plan, item, directory, key, commit))
                else:
                    # Submit at most workers items: pending items remain pending, never an unbounded running queue.
                    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="atlas-setting") as pool:
                        iterator, futures = iter(eligible), {}
                        def submit_next():
                            item = next(iterator, None)
                            if item is None:
                                return
                            item, directory, key = prepare(item)
                            futures[pool.submit(self._thread_item, plan, item, directory, key, commit, workers)] = item
                        for _ in range(workers):
                            submit_next()
                        while futures:
                            completed, _ = wait(futures, return_when=FIRST_COMPLETED)
                            for future in completed:
                                item = futures.pop(future)
                                finish(item, future.result())
                                submit_next()
            finally:
                record_scheduler_event(self.state.root, run_id, "batch_finished", workers=workers)
            summary = self.state.summary(run_id)
            write_json(self.state.root / "runs" / run_id / "summary.json", summary)
            return summary

    def _step(self, plan, sid, directory, task_key, commit, *, continuation=None):
        if (directory / "approved.json").is_file():
            pending = json.loads((directory / "approved.json").read_text())
            if pending["policy"] != self.policy or pending["prepared"]["setting_id"] != sid:
                raise ValueError("Saved approved bundle does not bind the current task")
            if commit or (directory / "receipt.json").exists():
                return self._publish(pending, directory)
            return "staged", {"artifact_path": str(directory), "prepared_hash": pending["prepared"]["bundle_hash"], "scope_complete": pending["scope_complete"]}
        if plan.get("mode") == "review_only":
            return self._step_review(plan, sid, directory, task_key, commit)
        version = self.inventory.version(sid)
        if version != plan["versions"][sid]:
            return "conflict", {"reason": "Setting changed since the ordered queue was frozen; create a new plan"}
        days = int(self.config.get("maintenance", {}).get("min_recheck_days", 14))
        if not plan["force"] and not self.state.due(sid, version, plan["semantics"], self.policy, plan["cutoff"], days):
            return "skipped_recent", {"reason": "Successful scope is recent and baseline/policy are unchanged"}
        profile = self.inventory.read(sid)
        if self.inventory.version(sid) != version:
            return "conflict", {"reason": "Setting changed while reading baseline"}
        last = self.state.last(sid)
        overlap = int(self.config.get("maintenance", {}).get("overlap_days", 30))
        reusable = last and (last["version"], last["semantics"], last["policy"]) == (version, plan["semantics"], self.policy)
        since = (date.fromisoformat(last["cutoff"]) - timedelta(days=overlap)).isoformat() if reusable else None
        context = {"setting_id": sid, "base_version": version, "cutoff": plan["cutoff"], "window_start": since,
                   "policy": self.policy, "semantics": plan["semantics"],
                   "budgets": self.config.get("budgets", {}), "maintenance_premise": "conditional_existing_baseline",
                   "baseline_catalog": baseline_catalog(profile),
                   "compact_profile": compact(profile, int(self.config.get("budgets", {}).get("compact_profile_chars", 14000))),
                   "contract_hash": digest({k: profile.get(k) for k in IMMUTABLE}),
                   "artifacts": {"baseline": profile}}
        if self.config.get("budgets", {}).get("finite_research_scope"):
            context["maintenance_role"] = "scout"
            comparisons = profile.get("comparisons", [])
            closed_hint = bool(comparisons) and all(
                row.get("status", {}).get("code") == "optimal" and not row.get("status", {}).get("missing_sides")
                for row in comparisons)
            context["maintenance_lane"] = {
                "candidate": "closed_bracket_check" if closed_hint else "standard",
                "scientific_approval": False,
                "note": "A native status is only a screening hint. Light planning requires complete own frozen-contract/parameter/view/quantity/resource/bound/comparison/proof reads, exact hashes and an explicit matching-envelope proof check. Known source revisions/corrections and the finite novelty route remain required within the declared scope. No case answer or expected result is supplied."}
        context["continuation_identity"] = self._continuation_identity(plan, sid)
        context["resume_binding"] = digest(context["continuation_identity"])
        existing_analysis = "joint_analysis" in profile
        context["joint_analysis_input"] = {
            "mode": "existing_analysis" if existing_analysis else "first_annotation",
            "existing_analysis_present": existing_analysis,
            "generic_template_supplied": False,
            "note": "Preserve the existing frozen analysis and revise its affected records; it is not a fresh scientific approval."
                    if existing_analysis else
                    "No existing joint analysis or generic template is supplied. Construct the first analysis from the frozen baseline, catalogues and the complete supplied schema; do not request a joint_template artifact."}
        if existing_analysis:
            template = profile["joint_analysis"]
            if not isinstance(template, dict) or not template:
                raise ValueError("Existing joint_analysis must be a nonempty object; it cannot be silently replaced by a generic draft")
            context["artifacts"]["joint_template"] = template
            template_limit = int(self.config.get("budgets", {}).get("joint_template_chars", 8000))
            context["joint_analysis_template"] = template if len(json.dumps(template, ensure_ascii=False)) <= template_limit else {
                "provided_complete": False, "artifact": "baseline", "pointer": "/joint_analysis",
                "content_hash": digest(template), "note": "Read every page of baseline /joint_analysis by artifact_read; this canonical pointer also satisfies the own-analysis read check. No omitted fields are inferred complete."}
        context["synthesis_catalog"] = synthesis_catalog(profile,
            max_chars=int(self.config.get("budgets", {}).get("synthesis_catalog_chars", 10000)))
        context["analysis_policy"] = {
            "version": 2, "required": True,
            "first_annotation": "Adding or changing the joint target/domain requires findings and synthesis for all comparisons; use a separate synthesis_only finding for preserved rows.",
            "no_change": "Requires version-2 complete synthesis coverage, a complete finite search and explicit resolved joint-domain accounting. Legacy coverage is unknown. An unassessed domain cell is not a proved open problem.",
            "synthesis": "Record compatible-candidate, withdrawn-branch and possible resource-projection obligations in the affected scope. Resolve each or retain it as pending; a different resource or quantity ID is never an automatic transfer. Every remaining textual lead needs a pending material_lead obligation.",
            "publication": "Distinguish registered-envelope gap from literature coverage. Each new closed cell must link optimal native comparisons and proof records, or remain explicitly unpublished and partial. Strict domain_extension requires an old-domain-exterior nonempty witness/proof; explicit_region_registration makes no such extension claim.",
            "draft_is_not_approval": True}
        prior = self._prior_work(sid, version) if continuation is None else self._continuation_work(continuation, context)
        if prior:
            context["pending_work"] = prior
            context["allowed_source_hashes"] = prior["source_hashes"]
        # Acceptance evidence stays internal. The model receives only an exact
        # optional identity, never an earlier verdict, receipt or approval text.
        pending = bool(prior)
        accepted = None if pending else qualify_accepted_analysis(self.inventory, self.state, sid, version, plan["semantics"])
        if accepted is not None:
            context["accepted_analysis_reuse"] = {"base_version": version,
                                                  "joint_analysis_hash": accepted["joint_analysis_hash"]}
        write_json(directory / "baseline.json", profile)
        write_json(directory / "context.json", {k: v for k, v in context.items() if k != "artifacts"})
        host = self.tools_factory(self.inventory.root, self.state.root / "cache", context, self.config)
        try:
            report = self._run_role(plan, sid, "scout", context, host, task_key + ":scout")
        finally:
            write_json(directory / "context.json", {k: v for k, v in context.items() if k != "artifacts"})
            write_json(directory / "scout-tools.json", host.state())
            write_json(directory / "scout-metrics.json", getattr(self.runner, "last_metrics", {}))
        write_json(directory / "scout.json", report)
        return self._post_scout(plan, sid, directory, task_key, commit, profile, version, context, report, host, accepted=accepted)

    def _post_scout(self, plan, sid, directory, task_key, commit, profile, version, context, report, host, *, accepted=None, review_origin=None):
        finite = current_finite_research_audit(host, context, report, self.config)
        if finite is not None:
            write_json(directory / "scout-frozen-context.json", context)
            write_json(directory / "finite-research-audit.json", finite)
        check_scope(report, context, host)
        if report["outcome"] == "incomplete":
            return "incomplete", {"reason": report["rationale"], "artifact_path": str(directory)}
        reuse = report.get("joint_analysis_reuse")
        if reuse is not None:
            if context.get("pending_work"):
                raise ValueError("Pending working notes require a full current assessment; an analysis reference cannot resolve them")
            recheck_accepted_analysis(accepted, self.inventory, stage_index=stage_index_for(self.state))
            if reuse != context.get("accepted_analysis_reuse"):
                raise ValueError("No-change reuse must bind the exact controller-qualified baseline version and joint hash")
            require_own_analysis_read(profile, host)
            analysis = json.loads(json.dumps(profile["joint_analysis"], ensure_ascii=False))
        else:
            if not isinstance(report.get("joint_analysis_json"), str):
                raise ValueError("Live maintenance requires joint_analysis_json (complete body) or an eligible no-change reference")
            analysis = json.loads(report["joint_analysis_json"])
        proposed, delta = apply_delta(profile, report)
        expected = context["compact_profile"]["comparison_ids"] if report["outcome"] == "no_change" else sorted(affected_comparisons(profile, proposed, delta))
        assessment = validate_joint_analysis(analysis, profile, proposed, report=report, expected_comparison_ids=expected,
                                             require_current=reuse is None)
        write_json(directory / "joint-analysis.json", analysis)
        write_json(directory / "joint-validation.json", assessment)
        (directory / "joint-analysis.md").write_text(render_analysis(analysis), encoding="utf-8")
        complete = self._scope_complete(report, context, host, analysis)
        if review_origin is not None and review_origin.get("partial_scout_scope") is not None:
            if complete:
                raise ValueError("A partial scout witness cannot become a completed scope or successful watermark")
            complete = False
        if report["outcome"] == "no_change":
            from .evidence_basis import check_no_change_evidence
            empty = None
            if report["findings"] == []:
                empty = finite_empty_search_certificate(self.inventory, self.state, self.config, context,
                    host, task_key + ":scout", report, analysis, accepted)
            evidence = check_no_change_evidence(report, profile, host, empty_search_certificate=empty)
            if not complete:
                return "incomplete", {"reason": "Search failed, remained paginated/truncated, or scope was not finished", "artifact_path": str(directory)}
            if self.inventory.version(sid) != version or self.inventory.semantics() != plan["semantics"]:
                return "conflict", {"reason": "Baseline/semantics changed during check"}
            scope_record = self._scope_record(report, host, analysis)
            if reuse is not None or empty is not None:
                recheck_accepted_analysis(accepted, self.inventory, stage_index=stage_index_for(self.state))
                if empty is not None:
                    recheck_evidence_pins(empty["evidence_pins"], self.state.root)
                certificate = {"kind": "no_change_only_analysis_reuse", "base_version": version,
                    "joint_analysis_hash": digest(analysis), "acceptance": {k: v for k, v in accepted.items() if k != "analysis"},
                    "current_evidence": evidence, "finite_empty_search": empty,
                    "native_files_written": False, "approval_inherited_for_new_claims": False}
                write_json(directory / "joint-analysis-reuse.json", certificate)
                scope_record["joint_analysis_reuse_certificate_hash"] = digest(certificate)
            self.state.success(sid, version, plan["semantics"], self.policy, plan["cutoff"], scope_record)
            return "no_change", {"artifact_path": str(directory), "scope": report["scope"]}
        # Every material finding needs an observed immutable full-text source.
        check_evidence_basis(report, profile, proposed, host)
        writer = self.atlas_factory(self.inventory.root)
        prepared = writer.prepare(proposed, [], version)
        if review_origin is not None and {name: digest(prepared["files"][name]) for name in FILES} != review_origin["prepared_files_sha256"]:
            raise ValueError("Fresh native preparation differs from the pinned original five-file candidate")
        prepared_profile = prepared["files"]["profile.json"]
        validate_status_taxonomy(prepared_profile)
        validate_joint_analysis(prepared_profile["joint_analysis"], profile, prepared_profile,
                                report=report, expected_comparison_ids=expected, require_current=True)
        for change in delta:
            collection, rid = change["collection"], change["id"]
            for name, target in (("baseline", profile), ("prepared", prepared["files"]["profile.json"])):
                index = next((i for i, row in enumerate(target.get(collection, [])) if row_id(row, collection) == rid), None)
                change[name + "_pointer"] = f"/{collection}/{index}" if index is not None else None
        write_json(directory / "prepared.json", prepared)
        review_scope = maintenance_review_scope(profile, prepared["files"]["profile.json"], report)
        from .evidence_basis import check_retention_read_obligations
        check_retention_read_obligations(review_scope, profile, prepared_profile, host, role="scout")
        write_json(directory / "review-scope.json", review_scope)
        adoption_catalog = retained_adoption_catalog(prepared["files"]["profile.json"], review_scope,
            int(self.config.get("budgets", {}).get("retained_adoption_catalog_chars", 12000)))
        write_json(directory / "retained-adoption-catalog.json", adoption_catalog)
        input_pack = review_input_pack(profile, prepared["files"]["profile.json"], delta,
                                       int(self.config.get("budgets", {}).get("review_input_pack_chars", 18000)))
        write_json(directory / "review-input-pack.json", input_pack)
        review_base = context
        if review_origin is not None:
            review_base = copy.deepcopy(context)
            review_base.update(policy=self.policy, budgets=self.config.get("budgets", {}),
                               continuation_identity=self._continuation_identity(plan, sid))
            review_base["resume_binding"] = digest(review_base["continuation_identity"])
        review_context = {**reviewer_context_view(review_base, report["findings"]), "prepared_hash": prepared["bundle_hash"], "delta": delta,
                          "joint_analysis_hash": digest(prepared_profile["joint_analysis"]),
                          "joint_analysis": prepared_profile["joint_analysis"] if len(json.dumps(prepared_profile["joint_analysis"], ensure_ascii=False)) <= int(self.config.get("budgets", {}).get("joint_review_chars", 8000)) else {
                              "provided_complete": False, "artifact": "prepared", "pointer": "/joint_analysis",
                              "content_hash": digest(prepared_profile["joint_analysis"]),
                              "note": "Read the omitted complete synthesis by artifact_read; omission is not a completed check."},
                          "synthesis_catalog": synthesis_catalog(prepared_profile, expected,
                              max_chars=int(self.config.get("budgets", {}).get("synthesis_catalog_chars", 10000)), artifact="prepared"),
                          "review_input_pack": input_pack,
                          "retained_adoption_catalog": adoption_catalog,
                          "review_scope": review_scope,
                          "research_scope": report["scope"],
                          "affected_comparison_ids": sorted(affected_comparisons(profile, proposed, delta)),
                          "findings": report["findings"], "allowed_source_hashes": _review_source_grants(report, host),
                          "proposed_summary": prepared["files"]["profile.json"].get("summary_status"),
                          "artifacts": {**context["artifacts"], "prepared": prepared["files"]["profile.json"]}}
        if finite is not None:
            review_context["artifacts"]["scout_research_scope"] = finite
            review_context.update(finite_review_context(finite, review_context["allowed_source_hashes"]))
        if review_origin is not None:
            review_context["scout_origin"] = {"origin_hash": digest(review_origin), "source_task_key": review_origin["source_task_key"],
                "original_scout_witness": True, "new_scout_sessions": 0, "new_scout_read_credit": False,
                "reviewer_read_credit": False, "approval_inherited": False}
        reviewer = self.tools_factory(self.inventory.root, self.state.root / "cache", review_context, self.config)
        try:
            review = self._run_role(plan, sid, "reviewer", review_context, reviewer, task_key + ":reviewer")
        finally:
            write_json(directory / "reviewer-tools.json", reviewer.state())
            write_json(directory / "reviewer-metrics.json", getattr(self.runner, "last_metrics", {}))
            if finite is not None:
                write_json(directory / "reviewer-frozen-context.json", review_context)
        write_json(directory / "reviewer.json", review)
        if finite is not None:
            write_json(directory / "reviewer-finite-research-audit.json",
                       current_finite_research_audit(reviewer, review_context, report, self.config))
        if review_origin is not None and review_origin.get("partial_scout_scope") is not None and (
                reviewer.failed or reviewer.budget_exhausted):
            raise ValueError("A partial scout origin requires a new clean independent reviewer")
        check_review(review, review_context, prepared, report, reviewer)
        if review["verdict"] != "approve":
            return "rejected" if review["verdict"] == "reject" else "incomplete", {"artifact_path": str(directory), "reason": review["rationale"]}
        writer.validate_review(prepared, review)
        pending = {"prepared": prepared, "review": review, "report": report, "scope_complete": complete,
                   "review_scope": review_scope,
                   "scope_record": self._scope_record(report, host),
                   "semantics": plan["semantics"], "policy": self.policy, "cutoff": plan["cutoff"],
                   "idempotency_key": "maintenance:" + task_key + ":" + prepared["bundle_hash"]}
        if finite is not None:
            pending["finite_context_hashes"] = {"scout": digest(context), "reviewer": digest(review_context),
                                                "scout_audit": digest(finite)}
        if review_origin is not None:
            pending["review_origin"] = review_origin
        write_json(directory / "approved.json", pending)
        if not commit:
            return "staged", {"artifact_path": str(directory), "prepared_hash": prepared["bundle_hash"], "scope_complete": complete}
        return self._publish(pending, directory)

    def _publish(self, pending, directory):
        if pending.get("policy") != self.policy:
            raise ValueError("Policy changed since review; create a fresh plan")
        if pending.get("review_origin") is not None:
            origin = pending["review_origin"]
            self._review_origin(origin["source_run"], origin["setting_id"], origin, recovery=pending)
        profile = pending["prepared"]["files"]["profile.json"]
        validate_status_taxonomy(profile)
        analysis = profile.get("joint_analysis")
        if analysis is None or pending["review"].get("joint_analysis_hash") != digest(analysis):
            raise ValueError("Publication requires the exact independently reviewed joint analysis")
        baseline = json.loads((directory / "baseline.json").read_text("utf-8"))
        proposed, delta = apply_delta(baseline, pending["report"])
        affected = sorted(affected_comparisons(baseline, proposed, delta))
        validate_joint_analysis(analysis, baseline, profile, report=pending["report"], expected_comparison_ids=affected,
                                require_current=True)
        for name, value in (("prepared", pending["prepared"]), ("reviewer", pending["review"]), ("scout", pending["report"])):
            archived = json.loads((directory / f"{name}.json").read_text("utf-8"))
            if digest(archived) != digest(value):
                raise ValueError(f"Staged {name} no longer matches its frozen review record")
        scout_log = json.loads((directory / "scout-tools.json").read_text("utf-8"))
        scout_context = json.loads((directory / "context.json").read_text("utf-8"))
        finite = None
        if scout_context.get("budgets", {}).get("finite_research_scope") is True:
            bound_context = json.loads((directory / "scout-frozen-context.json").read_text("utf-8"))
            pins = pending.get("finite_context_hashes", {})
            if (digest(bound_context) != pins.get("scout")
                    or {k: v for k, v in bound_context.items() if k != "artifacts"} != scout_context
                    or bound_context.get("artifacts", {}).get("baseline") != baseline):
                raise ValueError("Staged finite scout context differs from its exact original frozen baseline and input")
            scout_context = bound_context
            finite = current_finite_research_audit(SimpleNamespace(**scout_log), scout_context, pending["report"], self.config)
            archived_finite = json.loads((directory / "finite-research-audit.json").read_text("utf-8"))
            if digest(finite) != pins.get("scout_audit") or finite != archived_finite:
                raise ValueError("Staged finite research audit no longer matches its actual immutable event replay")
        review_context = {"setting_id": profile["setting_id"], "base_version": pending["prepared"]["base_version"],
                          "joint_analysis_hash": digest(analysis),
                          "joint_analysis": analysis if len(json.dumps(analysis, ensure_ascii=False)) <= int(self.config.get("budgets", {}).get("joint_review_chars", 8000)) else {"provided_complete": False},
                          "affected_comparison_ids": affected,
                          "artifacts": {"baseline": baseline, "prepared": profile}}
        if finite is not None:
            bound_review = json.loads((directory / "reviewer-frozen-context.json").read_text("utf-8"))
            expected_fields = finite_review_context(finite, _review_source_grants(pending["report"], SimpleNamespace(**scout_log)))
            if (digest(bound_review) != pending["finite_context_hashes"].get("reviewer")
                    or any(bound_review.get(key) != value for key, value in expected_fields.items())
                    or bound_review.get("prepared_hash") != pending["prepared"]["bundle_hash"]
                    or bound_review.get("artifacts", {}).get("baseline") != baseline
                    or bound_review.get("artifacts", {}).get("prepared") != profile
                    or bound_review.get("artifacts", {}).get("scout_research_scope") != finite
                    or bound_review.get("allowed_source_hashes") != _review_source_grants(pending["report"], SimpleNamespace(**scout_log))):
                raise ValueError("Staged finite reviewer input/witness/source grants differ from their independent review")
            review_context = bound_review
        reviewer_log = json.loads((directory / "reviewer-tools.json").read_text("utf-8"))
        if pending.get("review_origin", {}).get("partial_scout_scope") is not None and (
                reviewer_log.get("failed") or reviewer_log.get("budget_exhausted")):
            raise ValueError("A partial scout origin requires its independently clean reviewer evidence")
        check_review(pending["review"], review_context, pending["prepared"], pending["report"], SimpleNamespace(**reviewer_log))
        review_scope = maintenance_review_scope(baseline, profile, pending["report"])
        if pending.get("review_scope") != review_scope:
            raise ValueError("Staged retention certificate no longer matches the exact frozen proposal")
        from .evidence_basis import check_retention_read_obligations
        check_retention_read_obligations(review_scope, baseline, profile, SimpleNamespace(**scout_log), role="scout")
        if pending["scope_complete"] != self._scope_complete(pending["report"], scout_context, SimpleNamespace(**scout_log)):
            raise ValueError("Staged completion flag no longer matches frozen search and joint-domain evidence")
        writer = self.atlas_factory(self.inventory.root)
        receipt = writer.commit(pending["prepared"], pending["review"], pending["idempotency_key"])
        write_json(directory / "receipt.json", receipt)
        if pending["scope_complete"]:
            self.state.success(pending["prepared"]["setting_id"], pending["prepared"]["version"], pending["semantics"], pending["policy"],
                               pending["cutoff"], pending.get("scope_record", pending["report"]["scope"]))
        return "committed" if pending["scope_complete"] else "committed_partial", {"artifact_path": str(directory), "receipt": receipt}

    def apply(self, run_id, *, setting_id=None):
        self._assert_model_binding()
        with self.state.lock():
            plan = self.state.plan(run_id)
            if plan["policy"] != self.policy:
                raise ValueError("Policy changed since review; create a fresh plan")
            for item in self.state.items(run_id):
                if item["status"] != "staged" or setting_id and item["setting_id"] != setting_id:
                    continue
                result = json.loads(item["result"])
                directory = Path(result["artifact_path"])
                pending = json.loads((directory / "approved.json").read_text())
                status, result = self._publish(pending, directory)
                self.state.save(run_id, item["position"], status, result)
            return self.state.summary(run_id)


def search_complete(log):
    """Every observed pagination edge must be consumed within its exact query scope."""
    log = [row for row in log if not row.get("resolved") and not row.get("retired")]
    if not log or any(not r.get("success") or not r.get("fresh") or r.get("output_truncated") for r in log):
        return False
    groups = {}
    for row in log:
        key = digest({k: row.get(k) for k in ("provider", "query", "year", "limit", "window_start", "cutoff")})
        groups.setdefault(key, []).append(row)
    for rows in groups.values():
        provider = rows[0].get("provider")
        def node(cursor):
            starts = (None, "", "0", 0) if provider == "arxiv" else (None, "", "*") if provider in {"crossref", "openalex"} else (None, "", "0", 0)
            return "__start__" if cursor in starts else str(cursor)
        edges = {}
        for row in rows:
            start = node(row.get("cursor"))
            target = node(row["next_cursor"]) if row.get("next_cursor") else None
            if start in edges and edges[start] != target:
                return False
            edges[start] = target
        seen, current = set(), "__start__"
        while current is not None:
            if current in seen or current not in edges:
                return False
            seen.add(current)
            current = edges[current]
        if seen != set(edges):
            return False
    return True
