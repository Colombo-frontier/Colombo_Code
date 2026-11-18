"""Publication checks shared by the research, review, and Atlas write paths."""
from .joint import _index, _selected, validate_joint_analysis
from .taxonomy import validate_status_taxonomy


def validate_profile_science(profile, baseline=None, *, no_change=False):
    """Validate a complete candidate against its actual previous scientific record.

    A new setting has no previous scientific claims. Raw legacy Atlas records
    remain readable. An assessment declaring no change supplies the current
    profile with a newly researched joint_analysis and the real native baseline.
    """
    try:
        return _validate(profile, baseline, no_change)
    except (KeyError, TypeError, AttributeError, IndexError) as exc:
        raise ValueError(f"Invalid native scientific record: {exc}") from exc


def _validate(profile, baseline, no_change):
    from .store import _active_bounds

    validate_status_taxonomy(profile)
    if baseline is not None and baseline.get("setting_id") != profile.get("setting_id"):
        raise ValueError("Scientific assessment must bind its exact setting baseline")
    if no_change and baseline is None:
        raise ValueError("No-change requires a registered baseline")
    if no_change and any(profile.get(k) != baseline.get(k) for k in profile.keys() | baseline.keys() if k != "joint_analysis"):
        raise ValueError("No-change cannot replace native scientific content")
    previous = baseline if baseline is not None else {"setting_id": profile["setting_id"]}
    analysis = profile.get("joint_analysis")
    if not isinstance(analysis, dict) or analysis.get("version") != "complete":
        raise ValueError("A published profile requires complete joint_analysis")
    result = validate_joint_analysis(analysis, previous, profile, require_current=True)
    unresolved = analysis["target"]["resolution"] == "normalization_required"
    refinement = profile.get("refinement_pending")
    if unresolved:
        if (not analysis["normalization_requests"] or not analysis["pending_obligations"]
                or analysis["synthesis_coverage"]["status"] == "complete"):
            raise ValueError("An unresolved target needs normalization requests, pending obligations and unfinished synthesis")
        if not isinstance(refinement, dict) or any(not isinstance(refinement.get(k), str) or not refinement[k].strip()
                                                   for k in ("reason", "next_evidence")):
            raise ValueError("refinement_pending must explain the unresolved formulation and next evidence")
        native_sources = _index(profile, "references")
        refs = refinement.get("source_refs")
        if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or ref not in native_sources for ref in refs):
            raise ValueError("refinement_pending requires existing source_refs")
    elif refinement is not None:
        raise ValueError("Remove refinement_pending once the joint target has been resolved")
    if not profile["comparisons"] and (not unresolved or profile.get("bounds") or profile.get("bracket_rows")):
        raise ValueError("A comparison-free open formulation cannot adopt bounds or assert a native bracket")
    if no_change and (not result["joint_scope_complete"] or result["synthesis_coverage"]["literature_status"] != "finite_scope_complete"):
        raise ValueError("No-change requires completed joint-parameter synthesis and an explicitly completed finite literature scope")
    old_bounds, bounds = _index(previous, "bounds"), _index(profile, "bounds")
    old_rows, rows = _index(previous, "comparisons"), _index(profile, "comparisons")
    old_active = _active_bounds(previous)
    fresh = {bid for bid in _active_bounds(profile) if bid not in old_bounds
             or bounds[bid] != old_bounds[bid] or bid not in old_active}
    provenance = {row["bound_id"]: row for row in analysis["provenance"]}
    if any(bid not in provenance or provenance[bid]["origin"] == "retained_baseline" for bid in fresh):
        raise ValueError("New, changed or newly adopted bounds require explicit non-baseline provenance")
    if baseline is None:
        if any(item["origin"] == "retained_baseline" for item in provenance.values()):
            raise ValueError("A new setting has no retained-baseline provenance")
        if any(impact["kind"] in {"domain_extension", "bound_improvement"} for impact in analysis["impact"]):
            raise ValueError("A new setting cannot claim an improvement or extension of a prior Atlas bracket")
    else:
        if old_rows.keys() - rows.keys():
            raise ValueError("An update cannot silently remove a registered comparison; retain and document the correction")
        changed = {cid for cid, row in rows.items()
                   if cid not in old_rows or row != old_rows[cid]
                   or _selected(profile, row) != _selected(previous, old_rows[cid])
                   or bool(_selected(profile, row) & fresh)}
        covered = {cid for impact in analysis["impact"] if impact["kind"] != "no_effect" for cid in impact["comparison_ids"]}
        if changed - covered:
            raise ValueError("Changed comparisons require a scoped material impact: " + ", ".join(sorted(changed - covered)))
    return result
