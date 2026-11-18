"""Directed, independently reviewed application of a source result to a related target."""
import json

from ..atlas.store import _active_bounds
from ..core.contracts import ProtocolError, check_review
from ..core.store import digest

CHECKS = ("direction", "assumptions", "queries", "outputs", "guarantees", "cost", "guards_and_proofs")
SOURCE_REFS = ("candidate_ref", "extraction_ref", "extraction_review_ref", "identity_ref", "identity_review_ref")
PRODUCER_TASK = (
    "Assess a directional source result for the PINNED RELATED TARGET. Preserve the source identity decision and target "
    "common specification and existing views. Clone base_profile_ref. Read transfer_scope_ref and original paper. "
    "Check upper and lower directions separately, including hard instances, model, queries, output, guarantee, cost "
    "and parameter guards. For an update, attach a target-keyed result and a self-contained mapping proof, link the "
    "proof to the result and the transferred native claim (native proofs use artifact_ref, joint provenance uses the native proof ID). Retain original target tags; omit tag_facts to inherit. "
    "A finite no_change or an explicit defer is allowed. Never publish the broader source as this target."
)
REVIEW_TASK = (
    "Independently assess the source-to-target transfer on the frozen target. Verify the source theorem, mapping and "
    "adjusted guards for every proposed adoption. In review.assessments write a distinct scoped reason and verdict "
    "for each subject ID: " + ", ".join("transfer:" + key for key in CHECKS) +
    ". Include individual bound approvals and all normal joint checks. A related identity is not applicability approval."
)


def _checked_review(engine, case, kind, subject_ref):
    ref = case.get(kind + "_review_ref")
    if not ref:
        raise ProtocolError("A completed independent " + kind + " review is required before assessing a transfer")
    item = engine.artifacts.get(ref)
    if item["kind"] != "review":
        raise ProtocolError("Transfer source review has the wrong artifact kind")
    review = item["data"]
    check_review(review, subject_ref, kind)
    role = kind + "_reviewer"
    owners = engine.ws.query("SELECT j.id,j.inputs,j.output FROM jobs j JOIN ownership o ON o.job=j.id "
                             "WHERE o.ref=? AND j.role=? AND j.status='complete'", (ref, role))
    for owner in owners:
        job = owner["id"]
        inputs = json.loads(owner["inputs"])
        if (inputs.get("subject_ref") != subject_ref or
                (kind == "identity" and any(inputs.get(k) != case[k] for k in ("candidate_ref", "extraction_review_ref"))) or
                (kind == "profile" and case.get("transfer_scope_ref") != inputs.get("transfer_scope_ref")) or
                ref not in (json.loads(owner["output"]) or {}).get("artifact_refs", []) or
                engine.artifacts.owned(subject_ref, job)):
            continue
        events = engine.ws.query("SELECT payload FROM events WHERE job=? AND event='validated_handoff'", (job,))
        if any((entry := json.loads(e["payload"])).get("status") == "complete" and ref in entry.get("refs", []) for e in events):
            return review
    raise ProtocolError("Transfer source lacks an independent, completed and validated " + kind + " review")


def check_profile_handoff(engine, case, subject_ref):
    review = _checked_review(engine, case, "profile", subject_ref)
    check_transfer_review(review)


def source_is_current(engine, scope):
    source = engine.ws.case(scope["source_case_id"])
    return (source.get("paper_ref") == scope["source_paper_ref"] and
            all(source.get(k) == scope[k] for k in SOURCE_REFS))


def pin_files(engine, setting_id):
    pinned = engine.atlas.snapshot(setting_id)
    files = {name: engine.put("native_record", {"setting_id": setting_id, "filename": name,
             "version": pinned["version"], "content": value}) for name, value in pinned["files"].items()}
    return pinned["version"], files


def refresh_target(engine, case):
    prior = engine.artifacts.get(case["transfer_scope_ref"])["data"]
    version, files = pin_files(engine, prior["setting_id"])
    baseline = engine.artifacts.get(prior["target_files"]["profile.json"])["data"]["content"]
    current = engine.artifacts.get(files["profile.json"])["data"]["content"]
    check_transfer_profile(current, baseline)
    case["transfer_scope_ref"] = engine.put("external_result", {**prior, "target_files":files, "base_version":version})
    case.pop("previous_artifact_ref", None)
    case.pop("resume_work_refs", None)
    case.pop("human_approved", None)


def transfer_case(engine, source_id, setting_id, materials):
    try:
        source = engine.ws.case(source_id)
    except KeyError as exc:
        raise ProtocolError("Unknown source case") from exc
    if source.get("transfer_scope_ref"):
        raise ProtocolError("Choose the original paper case as the transfer source")
    cref = source["candidate_ref"]
    extraction = engine.artifacts.get(source["extraction_ref"])["data"]
    if cref not in extraction["candidate_refs"] or extraction["paper_ref"] != source["paper_ref"]:
        raise ProtocolError("Transfer source is not the candidate of the reviewed extraction")
    ex_review = _checked_review(engine, source, "extraction", source["extraction_ref"])
    cid = engine.artifacts.get(cref)["data"]["candidate_id"]
    assessment = [r for r in ex_review["assessments"] if r["subject_id"] in {cid, cref}]
    if len(assessment) != 1 or engine._candidate_verdict(source["extraction_review_ref"], cref, cid) != "approve":
        raise ProtocolError("The extracted source candidate lacks individual approval")
    if not source.get("identity_ref"):
        raise ProtocolError("The source identity review is incomplete")
    iref = source["identity_ref"]
    identity = engine.artifacts.get(iref)["data"]
    review = _checked_review(engine, source, "identity", iref)
    if review["verdict"] != "approve" or identity["candidate_ref"] != cref or identity["decision"] == "unresolved":
        raise ProtocolError("An approved, resolved source identity is required")
    rows = [r for r in identity["comparisons"] if r["setting_id"] == setting_id]
    if len(rows) != 1 or rows[0]["relation"] != "related":
        raise ProtocolError("The reviewed identity must explicitly classify this target as related")
    source_refs = {k: source[k] for k in SOURCE_REFS}
    branch_id = digest({"source_case_id": source_id, "source_refs": source_refs, "transfer_to": setting_id})[:24]
    try:
        existing = engine.ws.case(branch_id)
    except KeyError:
        existing = None
    if existing:
        if set(materials) - set(existing.get("research_material_refs", []) + existing.get("material_refs", [])):
            return engine.resume_case(branch_id, stage="research", material_refs=materials)
        return engine.resume_case(branch_id)
    for ref in materials:
        engine.artifacts.get(ref)
    version, files = pin_files(engine, setting_id)
    scope = {"source_case_id": source_id, "source_paper_ref": source["paper_ref"], **source_refs, "relation": rows[0],
             "setting_id": setting_id, "base_version": version, "target_files": files}
    scope_ref = engine.put("external_result", scope)
    case = {"paper_ref": source["paper_ref"], **source_refs}
    case.update(case_id=branch_id, source_case_id=source_id, transfer_scope_ref=scope_ref,
                transfer_target_id=setting_id, budget_scope=branch_id, state="transfer_pending", history=[], jobs={},
                research_material_refs=list(dict.fromkeys([*source.get("research_material_refs", []), *materials])))
    engine.ws.create_case_once(case)
    return engine.resume_case(branch_id)


def target_facts(explicit):
    # Existing bound-only transfers can rely on Atlas.prepare's hash-checked
    # inheritance from the target. Source-candidate tags describe another setting.
    return [] if explicit is None else explicit


def check_transfer_profile(profile, baseline):
    if profile.get("setting_id") != baseline["setting_id"] or profile.get("common_specification") != baseline.get("common_specification"):
        raise ProtocolError("Transfer must preserve the pinned target ID and common specification")
    views = {v["view_id"]:v for v in profile["views"]}
    if any(views.get(v["view_id"]) != v for v in baseline["views"]):
        raise ProtocolError("Transfer must preserve each existing target view contract")


def check_transfer_research(scope, research, read):
    if (research["setting_id"] != scope["setting_id"] or research["base_version"] != scope["base_version"]
            or research["identity_ref"] != scope["identity_ref"] or research["candidate_ref"] != scope["candidate_ref"]
            or research["action"] not in {"update","no_change"}):
        raise ProtocolError("Transfer research must bind the reviewed source and pinned target; allowed actions are update and no_change")
    if research["action"] == "no_change":
        return
    if not research["profile_ref"]:
        raise ProtocolError("Transfer update requires a complete target profile")
    profile = read(research["profile_ref"])["data"]
    base = read(scope["target_files"]["profile.json"])["data"]["content"]
    check_transfer_profile(profile, base)
    new_views = {v["view_id"] for v in profile["views"]} - {v["view_id"] for v in base["views"]}
    if any(row.get("view_ref") not in new_views for row in research.get("tag_facts", [])):
        raise ProtocolError("Inherit existing target tags unchanged; explicit transfer tags are scoped to newly added target views")
    proofs = set(research["proof_refs"])
    for ref in proofs:
        if read(ref)["kind"] != "proof":
            raise ProtocolError("Transfer proof_refs must identify proof records")
    cards = [read(ref) for ref in research["result_refs"]]
    if not cards or any(card["kind"] != "result" or card["data"]["comparison_key"]["setting_id"] != scope["setting_id"] for card in cards):
        raise ProtocolError("An adopted transfer needs target-keyed scientific result cards")
    linked = {ref for card in cards for ref in card["data"]["proof_refs"] if ref in proofs}
    if not linked:
        raise ProtocolError("Transfer requires a result linked to a self-contained source-to-target proof")
    old_bounds = {b.get("id", b.get("bound_id")): b for b in base["bounds"]}
    new_bounds = {b.get("id", b.get("bound_id")): b for b in profile["bounds"]}
    old_active = _active_bounds(base)
    changed = {bid for bid in _active_bounds(profile) if bid not in old_active or new_bounds[bid] != old_bounds.get(bid)}
    native_proofs = {row.get("id", row.get("proof_id")): row.get("artifact_ref") for row in profile["proofs"]}
    for bid in changed:
        bound = new_bounds[bid]
        evidence = {native_proofs.get(pid) for row in profile["joint_analysis"]["provenance"]
                    if row["bound_id"] == bid for pid in row["proof_refs"]}
        def covers(card):
            result = card["data"]
            key = result["comparison_key"]
            return (bool(evidence.intersection(result["proof_refs"], linked)) and result["direction"] == bound["direction"]
                    and key["view_id"] == bound["view_id"] and key["guarantee_id"] == bound["guarantee_id"]
                    and key["quantity_id"] == bound["quantity_ref"] and key["regime_id"] in bound["region_refs"])
        if not any(covers(card) for card in cards):
            raise ProtocolError("Each changed adopted target bound needs a same-direction, same-contract target result and its mapping proof in joint_analysis.provenance; bind the native proof to the research proof using artifact_ref")


def check_transfer_review(review):
    if review["verdict"] != "approve":
        return
    for key in CHECKS:
        rows = [r for r in review["assessments"] if r["subject_id"] == "transfer:" + key]
        if len(rows) != 1 or rows[0]["verdict"] != "approve" or not rows[0]["reason"].strip():
            raise ProtocolError("An approving transfer review must individually assess transfer:" + key)


def stage_inputs(read, case, role):
    scope = read(case["transfer_scope_ref"])["data"]
    return {"transfer_scope_ref": case["transfer_scope_ref"], "setting_id":scope["setting_id"],
            "base_version":scope["base_version"], "base_profile_ref":scope["target_files"]["profile.json"],
            "transfer_task": REVIEW_TASK if role == "profile_reviewer" else PRODUCER_TASK}
