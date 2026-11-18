"""Source reading and exact, actually-read baseline premises for local synthesis.

An inherited lemma is a conditional premise, not a new literature certificate.
Every source hash still needs an independent full-text read. Source-free changes
are limited to explicit baseline derivations or presentation restructuring.
"""
import json
import re

from .state import digest


def pointer_value(value, pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("Baseline evidence must identify a non-root JSON Pointer")
    for part in pointer[1:].split("/"):
        key = part.replace("~1", "/").replace("~0", "~")
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def material_findings(report):
    return [f for f in report.get("findings", []) if f["impact"] not in {"no_effect", "incomparable"}]


def source_requirements(report):
    return {sha for finding in material_findings(report) for sha in finding["source_hashes"]}


def fully_read_frozen_value(host, artifact, pointer, value):
    """Match complete observed pages to one exact frozen value, including its hash."""
    expected_hash = digest(value)
    expected_text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    intervals = []
    for event in getattr(host, "events", []):
        tool, args, result = event.get("tool"), event.get("arguments", {}), event.get("result", {})
        matches_artifact = (artifact == "baseline" and tool == "profile_read"
                            or tool == "artifact_read" and args.get("name") == artifact)
        if not matches_artifact or args.get("pointer") != pointer or result.get("error") or result.get("content_hash") != expected_hash:
            continue
        if result.get("total_characters") != len(expected_text):
            continue
        start = result.get("offset", args.get("offset", 0))
        text = result.get("text")
        if (not isinstance(start, int) or isinstance(start, bool) or start < 0
                or not isinstance(text, str) or not text
                or text != expected_text[start:start + len(text)]):
            continue
        intervals.append((start, start + len(text)))
    end = 0
    for start, stop in sorted(intervals):
        if start > end:
            break
        end = max(end, stop)
    return end >= len(expected_text)


def fully_read_frozen_value_or_ancestor(host, artifact, pointer, root):
    """Credit the same frozen object's complete exact value or ancestor.

    The referenced child must exist in this root.  Its separate reference hash
    is still checked by the caller; this changes the reading route, never the
    identity of a mathematical premise or another role's/source's read credit.
    """
    if not isinstance(pointer, str) or (pointer and not pointer.startswith("/")):
        return False
    try:
        pointer_value(root, pointer) if pointer else root
    except (KeyError, IndexError, TypeError, ValueError):
        return False
    parts = pointer[1:].split("/") if pointer else []
    for size in range(len(parts), -1, -1):
        parent = "/" + "/".join(parts[:size]) if size else ""
        try:
            value = pointer_value(root, parent) if parent else root
        except (KeyError, IndexError, TypeError, ValueError):
            continue
        if fully_read_frozen_value(host, artifact, parent, value):
            return True
    return False


def check_retention_read_obligations(scope, baseline, proposed, host, *, role):
    """Check each role's own reads; callers recompute scope from frozen objects."""
    if role not in {"scout", "reviewer"}:
        raise ValueError("Unknown retention-reading role")
    roots = {"baseline": baseline, "prepared": proposed}
    for item in scope.get("retention_read_obligations", []):
        artifact, pointer = item["artifact"], item["pointer"]
        if role == "scout" and artifact == "prepared":
            # The prepared object does not yet exist in the scout's session.
            continue
        if artifact not in roots:
            raise ValueError("Unknown frozen retention-premise artifact")
        value = pointer_value(roots[artifact], pointer)
        if digest(value) != item["sha256"]:
            raise ValueError("Retention reading obligation does not bind its frozen object")
        if not fully_read_frozen_value_or_ancestor(host, artifact, pointer, roots[artifact]):
            raise ValueError(f"Conditional quantity-metadata retention requires {role} to completely read {artifact}{pointer} or its complete exact ancestor")
    return {"role": role, "complete": True}


def _observed_source_reads(host):
    """Use this host's successful calls and their matching audit rows, never grants."""
    observed = set()
    for event in getattr(host, "events", []):
        arguments, result = event.get("arguments", {}), event.get("result", {})
        if event.get("tool") != "source_read" or result.get("error"):
            continue
        sha, text, audit = arguments.get("source_hash"), result.get("text"), result.get("audit")
        if (not isinstance(sha, str) or re.fullmatch(r"[0-9a-f]{64}", sha) is None
                or result.get("source_hash") != sha or not isinstance(text, str) or not text
                or not isinstance(audit, dict) or audit.get("tool") != "source_read"
                or audit.get("source_hash") != sha or audit.get("success") is not True
                or audit.get("characters_read") != len(text)
                or isinstance(audit.get("characters_read"), bool)
                or audit not in getattr(host, "source_log", [])):
            continue
        start = arguments.get("offset")
        if (not isinstance(start, int) or isinstance(start, bool) or start < 0
                or result.get("offset") != start or audit.get("offset") != start
                or audit.get("end") != start + len(text)):
            continue
        observed.add(sha)
    return observed


def check_no_change_evidence(report, baseline, host, *, empty_search_certificate=None):
    """Check evidence for a no-change outcome, including an adopted-analysis reference.

    The empty-result alternative is certified by the controller from a closed
    native journal and a fully read, qualified accepted analysis. It is not a
    model-supplied assertion and is bound again here to this report and host.
    """
    if report.get("outcome") != "no_change":
        raise ValueError("No-change evidence requires a no_change report")
    if getattr(host, "budget_exhausted", False):
        raise ValueError("No-change evidence cannot use a failed or budget-exhausted host")
    if getattr(host, "failed", False):
        from .contracts import current_finite_research_audit
        finite = current_finite_research_audit(host, getattr(host, "context", {}), report)
        if finite is None or not finite.get("no_change_eligible"):
            raise ValueError("No-change evidence cannot use a failed or budget-exhausted host")
    if report.get("patch") or report.get("summary_status_json") is not None or report.get("quantity_metadata_normalizations"):
        raise ValueError("No-change evidence cannot introduce profile edits or new proofs")
    findings = report.get("findings")
    if not isinstance(findings, list):
        raise ValueError("No-change findings must be an explicit array")
    if not findings:
        certificate = empty_search_certificate
        if not callable(getattr(host, "state", None)):
            raise ValueError("Empty no-change evidence requires actual tool state")
        expected = {"kind": "verified_finite_empty_native_search",
                    "setting_id": baseline.get("setting_id"), "base_version": report.get("base_version"),
                    "report_sha256": digest(report), "tool_state_sha256": digest(host.state())}
        if (not isinstance(certificate, dict) or not expected["setting_id"]
                or report.get("setting_id") != expected["setting_id"] or not expected["base_version"]
                or any(certificate.get(key) != value for key, value in expected.items())):
            raise ValueError("Empty no-change findings require a controller-verified finite empty native search certificate")
        return {"route": "verified_finite_empty_native_search", "source_hashes": [],
                "baseline_premises_are_conditional": True, "empty_search_certificate": dict(certificate)}

    comparisons = {row.get("comparison_id") for row in baseline.get("comparisons", [])}
    observed = _observed_source_reads(host)
    required, primary_findings = set(), 0
    for finding in findings:
        ids = finding.get("comparison_ids")
        if (finding.get("impact") not in {"no_effect", "incomparable"}
                or not isinstance(ids, list) or not ids
                or any(not isinstance(cid, str) or not cid or cid not in comparisons for cid in ids)):
            raise ValueError("Every no-change finding needs a no_effect/incomparable impact and nonempty existing comparison_ids")
        hashes = finding.get("source_hashes")
        if not isinstance(hashes, list) or any(not isinstance(sha, str) or re.fullmatch(r"[0-9a-f]{64}", sha) is None for sha in hashes):
            raise ValueError("Every cited no-change source must be a strict SHA-256 hash")
        if not set(hashes).issubset(observed):
            raise ValueError("Every cited no-change source must have a successful nonempty actual own source_read")
        required.update(hashes)
        basis = finding.get("evidence_basis", "primary_source")
        refs = finding.get("baseline_refs", [])
        if not isinstance(refs, list):
            raise ValueError("No-change baseline_refs must be an array")
        proof_premise = False
        for ref in refs:
            try:
                pointer = ref["pointer"]
                value = pointer_value(baseline, pointer)
                ref_hash = ref["sha256"]
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                raise ValueError("Unknown no-change baseline evidence pointer") from exc
            if not isinstance(ref_hash, str) or re.fullmatch(r"[0-9a-f]{64}", ref_hash) is None or digest(value) != ref_hash:
                raise ValueError("No-change baseline evidence hash does not bind its frozen premise")
            if not fully_read_frozen_value_or_ancestor(host, "baseline", pointer, baseline):
                raise ValueError("Every no-change baseline premise must be completely read by this host")
            rows = value if pointer == "/proofs" and isinstance(value, list) else [value] if re.fullmatch(r"/proofs/(0|[1-9][0-9]*)", pointer) else []
            if rows and all(isinstance(row, dict) and isinstance(row.get("id", row.get("proof_id")), str)
                            and row.get("id", row.get("proof_id")) for row in rows):
                proof_premise = True
        if basis == "primary_source":
            if not hashes:
                raise ValueError("Primary-source no-change findings require cited actual full-text reads")
            primary_findings += 1
        elif basis == "retained_baseline_derivation":
            if not proof_premise:
                raise ValueError("No-change baseline derivation requires an exact completely read existing proof row or proofs container")
        elif basis == "presentation_restructure":
            raise ValueError("Presentation restructuring cannot support a no-change evidence finding")
        else:
            raise ValueError("Unknown no-change evidence_basis")
    if not primary_findings:
        raise ValueError("Nonempty no-change findings require at least one cited primary-source actual read")
    return {"route": "primary_source_findings", "source_hashes": sorted(required),
            "primary_source_findings": primary_findings, "baseline_premises_are_conditional": True}


def check_evidence_basis(report, baseline, proposed, host):
    findings = material_findings(report)
    if any(f.get("evidence_basis") == "presentation_restructure" for f in findings):
        from .contracts import row_id
        from .delta_classification import classify_delta, scientific_support_comparisons
        scientific_delta = []
        for collection in ("bounds", "comparisons", "regimes", "evidence", "references", "proofs", "bracket_rows"):
            old = {row_id(r, collection): r for r in baseline.get(collection, [])}
            new = {row_id(r, collection): r for r in proposed.get(collection, [])}
            scientific_delta.extend({"collection": collection, "id": rid}
                                    for rid in set(old) | set(new) if old.get(rid) != new.get(rid))
        classification = classify_delta(baseline, proposed, report)
        adoption_only = set(classification["adoption_only_bound_ids"])
        scientific_delta = [change for change in scientific_delta
                            if not (change["collection"] == "bounds" and change["id"] in adoption_only)]
        summary_changed = (baseline.get("summary_status") != proposed.get("summary_status")
                           and not classification["summary_counts_only"] and not classification["summary_derived_only"])
        if scientific_delta or summary_changed:
            scientific_findings = [f for f in findings if f.get("evidence_basis", "primary_source") != "presentation_restructure"]
            if not scientific_findings:
                raise ValueError("Presentation restructuring cannot introduce or alter scientific claims, regimes, envelopes or statuses")
            # Mixed proposals may annotate unchanged rows while a different,
            # independently evidenced finding supports the scientific changes.
            affected = scientific_support_comparisons(baseline, proposed, scientific_delta, report)
            supported = {cid for f in scientific_findings for cid in f["comparison_ids"]}
            if not affected.issubset(supported):
                raise ValueError("Every scientific change in a mixed presentation proposal requires a separate source or derivation finding")
    required = source_requirements(report)
    read = {r.get("sha256", r.get("source_hash")) for r in host.source_log
            if (r.get("tool") == "source_read" and r.get("success") and r.get("characters_read", 0) > 0)
            or (r.get("action") in {"read", "source_read"} and r.get("characters_read", 1) > 0)}
    if not required.issubset(read):
        raise ValueError("Every decisive source hash must be independently read in full-text")
    for finding in material_findings(report):
        basis = finding.get("evidence_basis", "primary_source")
        if basis == "primary_source":
            if not finding["source_hashes"]:
                raise ValueError("Primary-source findings require source-backed full-text evidence")
            continue
        refs = finding.get("baseline_refs", [])
        if not refs:
            raise ValueError("Baseline derivation or presentation restructuring needs exact baseline_refs")
        for ref in refs:
            try:
                value = pointer_value(baseline, ref["pointer"])
            except (KeyError, IndexError, TypeError) as exc:
                raise ValueError("Unknown baseline evidence pointer") from exc
            if digest(value) != ref["sha256"]:
                raise ValueError("Baseline evidence hash does not bind the frozen premise")
            if not fully_read_frozen_value_or_ancestor(host, "baseline", ref["pointer"], baseline):
                raise ValueError("Each exact baseline premise must actually be read, including all its pages, in its frozen baseline directly or through its complete exact ancestor")
        if basis == "presentation_restructure":
            if finding["impact"] != "synthesis_only":
                raise ValueError("Presentation evidence may only support synthesis_only findings")
        elif basis == "retained_baseline_derivation":
            # New mathematical reasoning must be explicit, not merely asserted in a finding.
            before = {p.get("id", p.get("proof_id")): p for p in baseline.get("proofs", [])}
            changed = [p for p in proposed.get("proofs", []) if before.get(p.get("id", p.get("proof_id"))) != p]
            if not changed:
                raise ValueError("A retained-baseline derivation needs an explicit new or changed proof record")
        else:
            raise ValueError("Unknown evidence_basis")
    return {"source_hashes": sorted(required), "baseline_premises_are_conditional": True}
