"""Frozen science-contract boundaries; these checks do not prove mathematics."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

from ..atlas.tags import digest
from ..core.config import resources_root
from .joint import JOINT_CHECKS, validate_joint_profile
from .status import validate_status_taxonomy

CONTRACT_VERSION = "atlas-science-1.2.0"


class ScienceContractError(ValueError):
    def __init__(self, message, path="/science"):
        self.path = path
        self.diagnostics = [{"code": "science_contract", "path": path, "message": message}]
        super().__init__(f"{path}: {message}")


def contract_fingerprint():
    """Pin actual rule bytes in source and installed wheels, without path identity."""
    root = resources_root()
    files = {"science/" + name: Path(__file__).with_name(name)
             for name in ("gates.py", "joint.py", "status.py")}
    files.update({name: root / name for name in (
        "standards/status_taxonomy.json", "standards/status_taxonomy.md",
        "standards/joint_parameter_standard.md", "schemas/joint_analysis.schema.json",
        "schemas/profile.schema.json", "schemas/research.schema.json", "schemas/review.schema.json")})
    hashes = {}
    for name, path in files.items():
        if not path.is_file():
            raise ScienceContractError(f"Required contract resource is missing: {name}", "/science/contract")
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"version": CONTRACT_VERSION, "files": hashes}


def validate_profile_contract(profile, *, baseline=None, research_context=None):
    _match_scope(profile, research_context, baseline)
    validate_status_taxonomy(profile)
    return validate_joint_profile(profile, baseline=baseline, research_context=research_context)


def profile_contract_errors(profile, *, baseline=None, research_context=None):
    """Return bounded path-specific diagnostics, without repairing the document."""
    errors = []
    for check in (lambda: _match_scope(profile, research_context, baseline),
                  lambda: validate_status_taxonomy(profile),
                  lambda: validate_joint_profile(profile, baseline=baseline, research_context=research_context)):
        try:
            check()
        except (ValueError, KeyError, TypeError) as exc:
            errors.extend(getattr(exc, "diagnostics", [{"code": "science_contract",
                "path": getattr(exc, "path", "/joint_analysis"), "message": str(exc)}]))
    return errors


def _match_scope(profile, context, baseline=None):
    # An unchanged native baseline records its previous round's scope. The new
    # round binds its own declaration in the frozen controller context instead.
    if baseline is not None and profile == baseline:
        return
    declared = profile.get("research_scope") if isinstance(profile, dict) else None
    if declared is not None and context is not None and declared != context.get("scope"):
        raise ScienceContractError("Profile and final research must declare the same actual research scope", "/research_scope")


def freeze_science_context(profile, *, baseline=None, research_context=None):
    checked = validate_profile_contract(profile, baseline=baseline, research_context=research_context)
    return {"contract": contract_fingerprint(), "analysis_hash": checked["analysis_hash"],
            "research_context": deepcopy(research_context),
            "research_context_hash": digest(research_context),
            "baseline_profile": deepcopy(baseline),
            "baseline_hash": digest(baseline) if baseline is not None else None}


def validate_prepared_science(prepared):
    if not isinstance(prepared, dict) or not isinstance(prepared.get("science"), dict):
        raise ScienceContractError("A current frozen science context is required; historical approval is not inherited")
    science = prepared["science"]
    if prepared.get("bundle_hash") != digest(prepared.get("files")):
        raise ScienceContractError("Frozen five-file bundle hash mismatch", "/bundle_hash")
    if prepared.get("science_hash") != digest(science):
        raise ScienceContractError("Frozen science context hash mismatch", "/science_hash")
    if science.get("contract") != contract_fingerprint():
        raise ScienceContractError("Science rules changed after preparation; prepare and independently review again", "/science/contract")
    baseline = science.get("baseline_profile")
    expected = digest(baseline) if baseline is not None else None
    if science.get("baseline_hash") != expected:
        raise ScienceContractError("Frozen baseline hash mismatch", "/science/baseline_hash")
    if (prepared.get("base_version") is None) != (baseline is None):
        raise ScienceContractError("The frozen scientific baseline disagrees with new/update scope", "/science/baseline_profile")
    context = science.get("research_context")
    if science.get("research_context_hash") != digest(context):
        raise ScienceContractError("Research context hash mismatch", "/science/research_context_hash")
    profile = prepared.get("files", {}).get("profile.json")
    checked = validate_profile_contract(profile, baseline=baseline, research_context=context)
    if science.get("analysis_hash") != checked["analysis_hash"]:
        raise ScienceContractError("Prepared joint analysis hash mismatch", "/science/analysis_hash")
    return checked


def validate_joint_review(review, prepared):
    """Require an independent explicit check of this exact snapshot and context."""
    validate_prepared_science(prepared)
    value = review.get("joint_review")
    if not isinstance(value, dict):
        raise ScienceContractError("A complete joint_review is required", "/joint_review")
    expected = {"prepared_hash": prepared.get("bundle_hash"),
                "analysis_hash": prepared["science"]["analysis_hash"],
                "science_context_hash": prepared.get("science_hash")}
    for key, digest_value in expected.items():
        if value.get(key) != digest_value:
            raise ScienceContractError(f"Review does not bind the current {key}", "/joint_review/" + key)
    checks = value.get("checks")
    if not isinstance(checks, list) or len(checks) != len(JOINT_CHECKS):
        raise ScienceContractError("Record all six independent joint checks once", "/joint_review/checks")
    seen = set()
    for index, check in enumerate(checks):
        path = f"/joint_review/checks/{index}"
        if not isinstance(check, dict) or check.get("check_id") not in JOINT_CHECKS or check["check_id"] in seen:
            raise ScienceContractError("Unknown or repeated joint check", path)
        seen.add(check["check_id"])
        if check.get("verdict") not in {"approve", "revise", "defer"} or not isinstance(check.get("reason"), str) or not check["reason"].strip():
            raise ScienceContractError("Every joint check needs its own verdict and substantive reason", path)
        if review.get("verdict") == "approve" and check["verdict"] != "approve":
            raise ScienceContractError("Document approval conflicts with an unapproved joint check", path)
    return {"valid": True, **expected}


def research_context(workspace, job_id, research):
    """Bind a producer's scope declaration to observations, never infer completeness."""
    scope = research.get("research_scope")
    if (not isinstance(scope, dict) or not isinstance(scope.get("scope"), str) or not scope["scope"].strip()
            or type(scope.get("queries_complete")) is not bool
            or not isinstance(scope.get("unresolved_leads"), list)
            or any(not isinstance(x, str) or not x.strip() for x in scope["unresolved_leads"])):
        raise ScienceContractError("Declare the actual finite research scope, completion and unresolved leads", "/research_scope")
    rows = workspace.query("SELECT id,name,args,result,status FROM tool_calls WHERE job=? ORDER BY id", (job_id,))
    observed = [row for row in rows if row["name"] in {"bibliography_search", "source_fetch", "source_read", "source_search", "paper_verify"}
                or row["name"].startswith("mcp__")]
    external = [row for row in observed if row["name"] in {"bibliography_search", "source_fetch", "paper_verify"} or row["name"].startswith("mcp__")]
    pending = sum(row["status"] != "done" for row in external)
    if scope["queries_complete"] and (scope["unresolved_leads"] or pending):
        raise ScienceContractError("A completed finite scope cannot contain unresolved leads or unconfirmed external calls", "/research_scope")
    return {"scope": deepcopy(scope), "authority": "producer_declaration_with_controller_log_binding",
            "producer_job": job_id, "observations": {"tool_call_count": len(observed),
            "completed_external_calls": sum(row["status"] == "done" for row in external),
            "pending_external_calls": pending, "tool_trace_hash": digest(observed),
            "activity": [{"call_id": row["id"], "name": row["name"],
                          "arguments": json.loads(row["args"]), "status": row["status"],
                          "result_hash": digest(row["result"])} for row in observed]}}
