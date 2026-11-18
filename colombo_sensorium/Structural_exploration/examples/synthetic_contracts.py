"""Explicit contracts for synthetic fixtures only; never imported by production.

The declarations below are scripted test judgments, not model research. They
make fixed finite toy domains readable without inventing varying d/epsilon
parameters or claiming that any real literature has been surveyed.
"""
from copy import deepcopy

from oracle_atlas.core.store import digest
from oracle_atlas.science.joint import JOINT_CHECKS, build_joint_draft, synthesis_template
from oracle_atlas.science.status import canonical_summary


NOTICE = "Synthetic software fixture only; no real model, literature survey or scientific adoption."
DOMAIN = "The complete fixed finite synthetic family explicitly declared by this fixture; no varying continuous parameters."
PROOF = ("Synthetic structural test assertion, not a theorem from real literature. "
         "The fixture's recorded bound is an assumed scripted premise for exercising "
         "review and transaction plumbing. Its whole fixed test domain is declared explicitly.")


def _id(row, *names):
    return next(row[name] for name in names if name in row)


def complete_synthetic_profile(profile, *, baseline=None, proof_argument=PROOF):
    """Explicitly finish a test profile's metadata, leaving its status codes intact.

    Call this only while constructing a synthetic fixture. It does not infer a
    scientific code from a rate or bracket and is not a production repair hook.
    The complete declaration is returned in a new object for review by tests.
    """
    p = deepcopy(profile)
    p.setdefault("parameters", [])
    p.setdefault("symbols", [])
    p.setdefault("proofs", [])
    p.setdefault("evidence", [])
    p.setdefault("references", [])
    p.setdefault("regimes", [])
    p.setdefault("bounds", [])
    p.setdefault("comparisons", [])
    p.setdefault("bracket_rows", [])
    proof_map = {row["artifact_ref"]: _id(row, "id", "proof_id")
                 for row in p["proofs"] if row.get("artifact_ref")}
    evidence_map = {row["artifact_ref"]: _id(row, "id", "evidence_id")
                    for row in p["evidence"] if row.get("artifact_ref")}
    source_map = {row["source_ref"]: _id(row, "id", "source_id", "reference_id")
                  for row in p["references"] if row.get("source_ref")}
    known_proofs = {_id(row, "id", "proof_id") for row in p["proofs"]}
    for row in p["regimes"]:
        row.setdefault("predicate_text", DOMAIN)
    for row in p["proofs"]:
        row.setdefault("body", proof_argument)
    bound_proofs = {}
    for bound in p["bounds"]:
        bid = _id(bound, "id", "bound_id")
        native = [proof_map.get(ref, ref) for ref in bound.get("proof_refs", [])]
        if not native:
            pid = "synthetic-proof-" + bid
            if pid not in known_proofs:
                p["proofs"].append({"proof_id": pid, "body": proof_argument,
                                     "origin": "analyst_derivation", "synthetic": True})
                known_proofs.add(pid)
            native = [pid]
        bound["proof_refs"] = native
        if "evidence_refs" in bound:
            bound["evidence_refs"] = [evidence_map.get(ref, ref) for ref in bound["evidence_refs"]]
        if "source_refs" in bound:
            bound["source_refs"] = [source_map.get(ref, ref) for ref in bound["source_refs"]]
        bound_proofs[bid] = native
    p["summary_status"] = canonical_summary(p)
    analysis = build_joint_draft(p)
    analysis["target"].update(joint_variables=[], normalized_variables=[], fixed_parameters=[],
        uniform_in=[], allowed_constant_dependencies=[], full_domain=DOMAIN, resolution="resolved")
    analysis["normalization_requests"] = []
    analysis["pending_obligations"] = []
    analysis["domain_map"].update(status="accounted", residual_domain="Empty outside the declared finite toy family.",
        partition_argument="Synthetic enumeration: the registered fixture rows account for the whole fixed toy family.")
    comparison_codes = {row["comparison_id"]: row["status"]["code"] for row in p["comparisons"]}
    all_proofs = sorted({ref for refs in bound_proofs.values() for ref in refs})
    for row in analysis["comparisons"]:
        row.update(upper_envelope="Synthetic recorded upper envelope on the fixed fixture domain.",
                   lower_envelope="Synthetic recorded lower envelope on the fixed fixture domain.",
                   gap="Synthetic status is explicitly specified by its native comparison.",
                   boundary_checks=["Fixed finite family only; no invented asymptotic parameter endpoints."],
                   remaining_gap=NOTICE)
        for use in row["bound_uses"]:
            if use["disposition"] == "unresolved":
                use["disposition"] = "dominated"
            use["reason"] = "Explicit scripted synthetic participation judgment; no real theorem inferred."
    for cell in analysis["domain_map"]["cells"]:
        cell["note"] = NOTICE
        if all(comparison_codes[cid] == "optimal" for cid in cell["comparison_ids"]):
            cell.update(closure="established", publication="native_comparison", closure_proof_refs=all_proofs)
    sources = [_id(row, "id", "source_id", "reference_id") for row in p["references"]]
    analysis["provenance"] = [{"bound_id": _id(bound, "id", "bound_id"), "origin": "analyst_derivation",
        "source_refs": sources, "proof_refs": bound_proofs[_id(bound, "id", "bound_id")],
        "source_locator": "Explicit self-contained synthetic test proof record.", "source_domain": DOMAIN,
        "target_domain": DOMAIN, "mapping": "Identity on the fixed synthetic fixture only; no real literature claim."}
        for bound in p["bounds"]]
    frozen = baseline
    if frozen is None:
        frozen = deepcopy(p)
        for name in ("bounds", "comparisons", "regimes", "proofs", "evidence", "references"):
            frozen[name] = []
    coverage = synthesis_template(frozen, p)
    coverage["status"] = "complete"
    coverage["literature"] = {"status": "not_assessed", "scope": NOTICE}
    for obligation in coverage["obligations"]:
        obligation.update(state="resolved", argument="Explicit synthetic test judgment of this finite fixture obligation.",
                          proof_refs=all_proofs)
    analysis["synthesis_coverage"] = coverage
    p["joint_analysis"] = analysis
    return p


def synthetic_joint_review(prepared):
    """Bind a scripted test review to the actual five-file bundle and analysis."""
    return {"prepared_hash": prepared["bundle_hash"],
            "analysis_hash": digest(prepared["files"]["profile.json"]["joint_analysis"]),
            "science_context_hash": prepared["science_hash"],
            "checks": [{"check_id": name, "verdict": "approve", "reason": NOTICE} for name in JOINT_CHECKS]}


def synthetic_research_scope():
    return {"scope": NOTICE, "queries_complete": False, "unresolved_leads": []}
