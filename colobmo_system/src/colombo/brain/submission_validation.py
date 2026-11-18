"""Validate submitted candidates and fixed evidence; adoption requires Verifier."""
import copy
import json
from jsonschema import Draft202012Validator
from colombo.brain.record_formats import PROOF, BOUND_DESCRIPTION, SCHEMAS


class ContractError(ValueError):
    pass


def _shape(schema, value):
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: str(list(e.path)))
    if errors:
        raise ContractError("; ".join(f"{'.'.join(map(str, e.path)) or '$'}: {e.message}" for e in errors[:6]))
    return copy.deepcopy(value)


def validate_proof_shape(payload):
    return _shape(PROOF, payload)


def proof_complete(proof):
    active = [s for s in proof.get("steps", []) if s["status"] != "retired"]
    return (bool(active) and not proof.get("open_questions") and
            all(s["status"] == "checked" and not s["gaps"] for s in active))


def integration_structure_issues(proof):
    """Explain structural completion requirements without judging the mathematics."""
    active = [step for step in proof.get("steps", []) if step["status"] != "retired"]
    issues = []
    if not active:
        issues.append("ProofDraft has no active proof steps.")
    for step in active:
        if step["status"] != "checked":
            issues.append(f"Proof step {step['id']} has status={step['status']}; completed integration requires checked.")
        if step.get("gaps"):
            issues.append(f"Proof step {step['id']} still lists unresolved gaps.")
    if proof.get("open_questions"):
        issues.append("ProofDraft still lists open_questions.")
    return issues

def result_review(store, rid):
    ref = store.get_meta("result_reviews", {}).get(rid)
    if not ref:
        raise ContractError("Result has not returned through Verifier")
    report = store.read_record(ref)
    if report.get("review_kind") != "result" or report.get("result_ref") != rid:
        raise ContractError("Result review identity mismatch")
    return ref, report

def confirmed_claim(store, review_ref, claim_id):
    if not review_ref or not claim_id:
        raise ContractError("Claim needs a fixed review and Claim identity")
    if store.record_kind(review_ref) != "review":
        raise ContractError("Claim needs a Verifier review")
    report = store.read_record(review_ref)
    rid = report.get("result_ref")
    actual, _ = result_review(store, rid)
    if actual["id"] != review_ref:
        raise ContractError("Claim review is not the registered Result review")
    matches = [c for c in report["confirmed_claims"] if c["id"] == claim_id]
    if len(matches) != 1:
        raise ContractError("Unknown confirmed Claim")
    return rid, matches[0]


def _bound_descriptions(bounds):
    return sorted(json.dumps({key: bound[key] for key in BOUND_DESCRIPTION["properties"]},
                             sort_keys=True, ensure_ascii=False) for bound in bounds)

def _adopted_final_progress(store, progress):
    """Source-only goals require the exact independently adopted final version."""
    pref, review_ref = store.get_meta("progress_ref"), store.get_meta("final_review_ref")
    if not pref or not review_ref:
        return False
    record = store.read_record(pref)
    report = store.read_record(review_ref)
    if (record.get("progress") != progress or record.get("review_ref") != review_ref or
            record.get("proof_ref") != store.get_meta("proof_ref") or
            report.get("review_kind") != "proof" or report.get("verdict") != "pass"):
        return False
    refs = [store.get_meta("goal_ref"), store.get_meta("setting_ref"), record.get("assessment_ref"),
            record.get("proof_ref"), *store.get_meta("material_refs", [])]
    return all(ref and ref["id"] in report.get("checked_refs", []) for ref in refs)


def validate_progress(store, progress, *, final_candidate=False):
    goals = {g["id"] for g in store.read_record(store.get_meta("goal_ref"))["targets"]}
    if len(progress["items"]) != len(goals) or {i["goal_id"] for i in progress["items"]} != goals:
        raise ContractError("Progress must cover each Goal exactly once")
    bounds = {b["id"]: b for b in progress["bracket"]["bounds"]}
    if len(bounds) != len(progress["bracket"]["bounds"]):
        raise ContractError("Duplicate Bound IDs")
    regimes = progress["bracket"]["regimes"]
    if len({r["id"] for r in regimes}) != len(regimes):
        raise ContractError("Duplicate regime IDs")
    for b in bounds.values():
        if b["evidence_state"] == "certified":
            rid, claim = confirmed_claim(store, b["review_ref"], b["claim_id"])
            if rid != b["result_ref"] or any(claim[k] != b[k] for k in ("expression", "scope", "assumptions")) or claim["kind"] != b["direction"]:
                raise ContractError("Certified Bound differs from its verified Claim")
    for regime in progress["bracket"]["regimes"]:
        for side, direction in (("lower_bound_ids", "lower_bound"), ("upper_bound_ids", "upper_bound")):
            if any(b not in bounds or bounds[b]["direction"] != direction for b in regime[side]):
                raise ContractError("Regime references an unknown or wrong-direction Bound")
        if regime["status"] == "near_optimal":
            comparison = regime["comparison_review_ref"]
            if final_candidate and comparison is None:
                pass  # This new composition is checked by the final Proof Verifier.
            elif comparison and store.read_record(comparison).get("review_kind") == "proof":
                report = store.read_record(comparison)
                final_ref = store.get_meta("final_review_ref")
                if not final_ref or final_ref["id"] != comparison or report["verdict"] != "pass":
                    raise ContractError("Comparison does not belong to adopted final review")
                matches = []
                for rid in report["checked_refs"]:
                    if store.record_kind(rid) == "assessment":
                        bracket = store.read_record(rid).get("update", {}).get("progress", {}).get("bracket", {})
                        old_bounds = {b["id"]: b for b in bracket.get("bounds", [])}
                        matches += [(r, old_bounds) for r in bracket.get("regimes", [])]
                bound_ids = [*regime["lower_bound_ids"], *regime["upper_bound_ids"]]
                if not any(all(r.get(k) == regime[k] for k in regime if k not in {"comparison_review_ref", "comparison_claim_id"})
                           and all(bid in old_bounds for bid in bound_ids)
                           and _bound_descriptions([bounds[bid] for bid in bound_ids]) == _bound_descriptions([old_bounds[bid] for bid in bound_ids])
                           for r, old_bounds in matches):
                    raise ContractError("Comparison changed after final review")
            else:
                _, claim = confirmed_claim(store, comparison, regime["comparison_claim_id"])
                if (claim["kind"] != "comparison" or claim["scope"] != regime["scope"]
                        or claim["expression"] != regime["gap"]
                        or claim["assumptions"] != regime.get("assumptions", [])):
                    raise ContractError("Near-optimal comparison needs verified matching scope, assumptions and gap")
                used = [bounds[bid] for bid in (*regime["lower_bound_ids"], *regime["upper_bound_ids"])]
                if _bound_descriptions(used) != _bound_descriptions(claim.get("comparison_bounds", [])):
                    raise ContractError("Near-optimal comparison differs from its verified Bounds")
            if not regime["lower_bound_ids"] or not regime["upper_bound_ids"] or regime["remaining"]:
                raise ContractError("Near-optimal regime has missing Bounds or remaining work")
    for item in progress["items"]:
        for rid in item["result_refs"]:
            result_review(store, rid)
        if item["status"] in {"supported", "refuted"}:
            if not item["result_refs"] and (final_candidate or _adopted_final_progress(store, progress)):
                # Independent final review checks the complete source-based
                # Proof; this exception cannot promote an ordinary update.
                continue
            if not item["result_refs"] or not any(
                    any(c["kind"] != "empirical" for c in result_review(store, rid)[1]["confirmed_claims"])
                    for rid in item["result_refs"]):
                raise ContractError("Completed mathematical Goal item needs confirmed mathematical Claims")
    if progress["status"] == "completed":
        setting_ref = store.get_meta("setting_ref")
        if setting_ref:
            declared = store.read_record(setting_ref).get("specification", {}).get("regimes", [])
            declared_ids = (set(declared) if isinstance(declared, dict) else
                            {r["id"] for r in declared if isinstance(r, dict) and isinstance(r.get("id"), str)})
            if not declared_ids.issubset({r["id"] for r in regimes}):
                raise ContractError("Completed Goal omitted regimes from its fixed Setting Specification")
        if (progress["remaining"] or not progress["bracket"]["regimes"] or
            any(r["status"] != "near_optimal" for r in progress["bracket"]["regimes"]) or
            any(i["remaining"] or i["status"] not in {"supported", "refuted"} for i in progress["items"])):
            raise ContractError("Completed Goal cannot contain unresolved regimes or items")

def validate_semantics(stage, payload, store, context):
    if store.get_meta("config", {}).get("workflow", {}).get("version") != 3:
        raise ContractError("Current Brain submissions require workflow version 3")
    if stage not in SCHEMAS:
        raise ContractError(f"Unsupported Brain stage: {stage}")
    value = _shape(SCHEMAS[stage], payload)
    if stage == "plan":
        remaining = context.get("dispatch_remaining", store.get_meta("config")["limits"]["max_dispatches_per_wave"])
        if len(value["tasks"]) > remaining:
            raise ContractError("Plan exceeds current Wave dispatch allocation")
        setting = store.get_meta("setting_ref")
        if not setting and "setting_specification" not in value:
            raise ContractError("First plan must complete Setting Specification")
        if setting and "setting_specification" in value and value["setting_specification"] != store.read_record(setting):
            raise ContractError("Setting Specification is fixed")
        resumed = set()
        for task in value["tasks"]:
            for item in task["package"]["items"]:
                store.read_record(item["ref"])
                store.artifact_entries(item["ref"])
            goals = {g["id"] for g in store.read_record(store.get_meta("goal_ref"))["targets"]}
            if not set(task["responsibility"]["goal_ids"]).issubset(goals):
                raise ContractError("Unknown Goal responsibility")
            if task["mode"] == "new" and task["resume_task_id"] is not None:
                raise ContractError("New Task needs null resume_task_id")
            if task["mode"] == "new":
                from colombo.brain.cell_package import preflight_package
                from colombo.brain.research_store import StoreError
                try:
                    preflight_package(store, task)
                except StoreError as exc:
                    details = getattr(exc, "details", {"kind": "package_preflight", "reason": str(exc)})
                    raise ContractError(f"Package preflight failed for {task['title']}: "
                        + json.dumps(details, ensure_ascii=False)
                        + ". No plan or dispatch was committed. Read the exact source; for a literal "
                        "formula use format_package_literal, otherwise supply the required dependency.") from exc
            if task["mode"] in {"resume", "restart"}:
                tid = task["resume_task_id"]
                old = store.get_task(tid) if tid else None
                if tid in resumed or not old or old.get("state") not in {"returned", "failed", "cancelled"}:
                    raise ContractError("Resume/restart requires a reconciled Task")
                resumed.add(tid)
                original = store.read_record(old["assignment_ref"])["spec"]
                if original.get("specialization") == "experiment" and old.get("latest_result_ref"):
                    returned = store.read_record(old["latest_result_ref"])
                    if returned.get("evidence_kind") == "empirical" and returned.get("empirical_report"):
                        raise ContractError("Completed Experiment report is fixed; create a new repair Task with Verifier feedback")
                if any(task.get(k, "general" if k == "specialization" else None) != original.get(k, "general" if k == "specialization" else None)
                       for k in (set(task) | set(original)) - {"mode", "resume_task_id"}):
                    raise ContractError("Resume/restart cannot change the fixed Task or package")
                from colombo.brain.resume_eligibility import task_resume_eligibility
                eligibility = task_resume_eligibility(store, old)
                status = eligibility["restart_status"] if task["mode"] == "restart" else eligibility["status"]
                if status != "allowed":
                    raise ContractError(f"{task['mode']} is not eligible for {tid}: "
                        + json.dumps(eligibility, ensure_ascii=False)
                        + ". No plan or dispatch was committed.")
    elif stage == "verify-progress":
        package = store.read_record(context["review_package_ref"])
        if value["review_kind"] != package["review_kind"] or value["result_ref"] != package.get("result_ref"):
            raise ContractError("Review target mismatch")
        if not set(package["required_checked_refs"]).issubset(value["checked_refs"]) or not set(value["checked_refs"]).issubset(package["allowed_refs"]):
            raise ContractError("Review must cover exactly authorized evidence")
        if value["verdict"] == "pass" and (value["findings"] or value["repair_kind"] != "none"):
            raise ContractError("Passing review cannot leave unresolved findings")
        if len({c["id"] for c in value["confirmed_claims"]}) != len(value["confirmed_claims"]):
            raise ContractError("Duplicate confirmed Claim IDs")
        if value["review_kind"] == "result":
            result = store.read_record(value["result_ref"])
            paths = {a["path"] for a in result.get("artifacts", [])}
            for claim in value["confirmed_claims"]:
                if result.get("evidence_kind") == "empirical" and claim["kind"] != "empirical":
                    raise ContractError("Empirical Result cannot certify mathematics")
                if not claim["evidence_paths"] or not set(claim["evidence_paths"]).issubset(paths):
                    raise ContractError("Confirmed Claim needs frozen evidence paths")
                if claim["kind"] == "comparison":
                    compared = claim.get("comparison_bounds", [])
                    if {b["direction"] for b in compared} != {"upper_bound", "lower_bound"}:
                        raise ContractError("Comparison Claim must identify its exact Lower and Upper Bounds")
                    descriptions = _bound_descriptions(compared)
                    if len(set(descriptions)) != len(descriptions):
                        raise ContractError("Comparison Claim repeats a Bound")
    else:
        for rid in value["result_refs"]:
            result_review(store, rid)
        for admission in value["update"]["admissions"]:
            _, report = result_review(store, admission["result_ref"])
            if admission["verdict"] in {"accepted", "partial"} and not report["confirmed_claims"]:
                raise ContractError("Admission requires confirmed Claims")
            if admission["completion_status"] == "completed" and report["completion_status"] != "completed":
                raise ContractError("Partial Result does not complete Task")
        validate_progress(store, value["update"]["progress"], final_candidate=stage == "integrate")
        if stage == "integrate" and value["prunes"]:
            raise ContractError("integrate cannot prune")
        if stage == "integrate":
            proof = value["update"]["proof_draft"]
            if value["update"]["progress"]["status"] == "completed" and not proof_complete(proof):
                raise ContractError("Completed integration has incomplete ProofDraft structure: "
                    + " ".join(integration_structure_issues(proof))
                    + " Recheck and correct the candidate step declarations, or retain in_progress for unresolved work. "
                    "This structural check does not certify the proof; the revised version still requires final Verifier.")
            steps = {s["id"]: s for s in proof["steps"]}
            if len(steps) != len(proof["steps"]):
                raise ContractError("Proof step IDs must be unique")
            visiting, done = set(), set()
            def visit(sid):
                if sid not in steps or sid in visiting:
                    raise ContractError("Proof has missing or cyclic dependencies")
                if sid in done:
                    return
                visiting.add(sid)
                step = steps[sid]
                for dep in step["depends_on"]:
                    visit(dep)
                    if step["status"] == "checked" and steps[dep]["status"] != "checked":
                        raise ContractError("Checked Proof step depends on unchecked work")
                if step["status"] == "checked" and step["gaps"]:
                    raise ContractError("Checked Proof step has unresolved gaps")
                for evidence in step["evidence"]:
                    result_review(store, evidence["result_ref"])
                    if (step["status"] == "checked" and
                            store.read_record(evidence["result_ref"]).get("evidence_kind") == "empirical"):
                        raise ContractError("Empirical Result cannot certify a checked Proof step; keep it as motivation or draft evidence")
                    if evidence["path"] not in {a["path"] for a in store.artifact_entries(evidence["result_ref"])}:
                        raise ContractError("Proof evidence is outside the fixed returned artifacts")
                    if evidence.get("record_ref"):
                        from colombo.brain.cell_evidence import resolve_record
                        resolve_record(store, evidence["result_ref"], evidence["path"], evidence["record_ref"])
                visiting.remove(sid)
                done.add(sid)
            for sid in steps:
                visit(sid)
        for prune in value["prunes"]:
            from colombo.brain.pruning import validate_prune_audit
            validate_prune_audit(store, prune, store.get_task(prune["task_id"]))
    return value
