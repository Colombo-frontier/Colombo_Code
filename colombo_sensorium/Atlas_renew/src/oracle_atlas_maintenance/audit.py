"""Read-only preflight and reviewable drafts. No models, network or Atlas writes."""
from collections import Counter, defaultdict
from copy import deepcopy
import json
from pathlib import Path

from .joint import analysis_template, synthesis_catalog, validate_joint_analysis, render_analysis
from .state import digest, write_json


def _id(row):
    return row.get("id", row.get("quantity_id"))


def profile_preflight(profile):
    issues = []
    analysis = profile.get("joint_analysis")
    if analysis is None:
        issues.append({"code": "joint_analysis_missing", "severity": "needs_review",
                       "detail": "Legacy comparisons do not encode the complete joint target/domain/impact contract."})
    else:
        try:
            result = validate_joint_analysis(analysis, profile, profile)
            if not result["joint_scope_complete"]:
                issues.append({"code": "joint_accounting_incomplete", "severity": "needs_review",
                               "detail": "Joint-domain, candidate participation or normalization obligations remain."})
        except ValueError as exc:
            issues.append({"code": "joint_analysis_invalid", "severity": "structural_error", "detail": str(exc)})
    groups = defaultdict(list)
    for quantity in profile.get("quantities", []):
        expression = quantity.get("expression_latex", quantity.get("expression", quantity.get("symbol")))
        if expression:
            key = digest({"expression": expression, "view": quantity.get("view_id"),
                          "guarantee": quantity.get("guarantee_id"), "units": quantity.get("units")})
            groups[key].append(_id(quantity))
    for ids in groups.values():
        if len(ids) > 1:
            issues.append({"code": "quantity_equivalence_candidate", "severity": "needs_review", "quantity_ids": ids,
                           "detail": "Similar expressions are a review lead, not mathematical equivalence or automatic permission to merge."})
    return {"setting_id": profile["setting_id"], "profile_sha256": digest(profile),
            "comparison_count": len(profile.get("comparisons", [])), "bound_count": len(profile.get("bounds", [])),
            "issues": issues}


def audit_inventory(inventory, ids=None):
    ids = inventory.ordered_ids() if ids is None else ids
    if not isinstance(ids, list) or not ids or any(not isinstance(s, str) for s in ids) or len(set(ids)) != len(ids):
        raise ValueError("Audit needs a nonempty unique list of setting IDs")
    rows = [profile_preflight(inventory.read(sid)) for sid in ids]
    counts = Counter(issue["code"] for row in rows for issue in row["issues"])
    return {"mode": "read_only_structural_preflight", "settings": len(rows), "issue_counts": dict(counts),
            "mathematics_recertified": False, "literature_searched": False,
            "note": "Flags identify work to examine. They do not establish incorrect rates or prove that a literature gap is open.",
            "profiles": rows}


def outside_atlas(path, inventory):
    path = Path(path).resolve()
    if path.is_relative_to(inventory.root):
        raise ValueError("Write drafts and audit output outside the Atlas; native adoption uses stage/apply")
    return path


def create_draft(inventory, sid, output):
    requested = Path(output).absolute()
    if any(path.is_symlink() for path in (requested, *requested.parents)):
        raise ValueError("Draft output cannot use symbolic links")
    output = outside_atlas(output, inventory)
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Choose an empty draft output directory")
    version = inventory.version(sid)
    profile = inventory.read(sid)
    if inventory.version(sid) != version:
        raise ValueError("Atlas changed while drafting; retry from the current frozen version")
    existing = profile.get("joint_analysis")
    legacy = None
    if "joint_analysis" not in profile:
        mode = "first_analysis_v2"
        analysis = analysis_template(profile, version=2)
    elif not isinstance(existing, dict) or type(existing.get("version")) is not int:
        raise ValueError("Existing joint_analysis must be an explicit version 1 or 2 object")
    elif existing["version"] == 2:
        mode = "existing_v2_preserved"
        analysis = deepcopy(existing)
    elif existing["version"] == 1:
        mode = "legacy_v1_reassessment"
        legacy = deepcopy(existing)
        analysis = analysis_template(profile, version=2)
    else:
        raise ValueError("Unsupported existing joint_analysis version")
    proposed = deepcopy(profile)
    proposed["joint_analysis"] = analysis
    structural = validate_joint_analysis(analysis, profile, proposed, require_current=True)
    markdown = render_analysis(analysis)
    catalog = synthesis_catalog(profile)
    if inventory.version(sid) != version:
        raise ValueError("Atlas changed while drafting; retry from the current frozen version")
    if any(path.is_symlink() for path in (output, *output.parents)):
        raise ValueError("Draft output cannot use symbolic links")
    output = outside_atlas(output, inventory)
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Choose an empty draft output directory")
    source_analysis = None if existing is None else {
        "version": existing["version"], "source_pointer": "/joint_analysis",
        "canonical_sha256": digest(existing), "base_version": version}
    if legacy is not None:
        archive = output / "legacy_joint_analysis.json"
        write_json(archive, legacy)
        archive.chmod(0o444)
        source_analysis["archived_object"] = archive.name
    write_json(output / "profile.draft.json", proposed)
    write_json(output / "joint_analysis.draft.json", analysis)
    write_json(output / "synthesis_catalog.json", catalog)
    write_json(output / "manifest.json", {"setting_id": sid, "base_version": version,
        "baseline_sha256": digest(profile), "proposal_sha256": digest(proposed),
        "draft_mode": mode, "joint_analysis_version": 2, "source_joint_analysis": source_analysis,
        "structural_validation": structural, "approval_inherited": False, "new_approval": False,
        "adoption_state": "unreviewed_draft", "scientific_baseline_changed": False,
        "warning": "Do not copy profile.draft.json over native files. Submit a fresh scout proposal and independent review."})
    (output / "joint_analysis.draft.md").write_text(markdown, encoding="utf-8")
    return {"draft_directory": str(output), "setting_id": sid, "adoption_state": "unreviewed_draft"}


def validate_files(profile_path, analysis_path=None, baseline_path=None):
    proposed = json.loads(Path(profile_path).read_text("utf-8"))
    baseline = json.loads(Path(baseline_path).read_text("utf-8")) if baseline_path else proposed
    analysis = json.loads(Path(analysis_path).read_text("utf-8")) if analysis_path else proposed.get("joint_analysis")
    if analysis is None:
        raise ValueError("Profile has no joint_analysis; provide --analysis")
    return validate_joint_analysis(analysis, baseline, proposed)
