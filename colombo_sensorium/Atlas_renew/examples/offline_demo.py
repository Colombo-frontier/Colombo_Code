"""Offline engineering demonstration with synthetic science and the real native writer.

Run from the component directory after installation:
    python examples/offline_demo.py --output /tmp/oracle-maintenance-demo

No papers, network requests, or model calls occur. The two theorem expressions are
deliberately synthetic and establish transaction behavior only.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

PROJECT = Path(__file__).resolve().parents[1]
if importlib.util.find_spec("oracle_atlas_maintenance") is None and str(PROJECT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT / "src"))

from oracle_atlas.atlas.store import Atlas, FILES
from oracle_atlas.atlas.tags import AXES
from oracle_atlas_maintenance.engine import Maintenance
from oracle_atlas_maintenance.state import digest, write_json
from oracle_atlas_maintenance.joint import analysis_template, synthesis_template
from oracle_atlas_maintenance.tools import MaintenanceTools
from oracle_atlas_maintenance.taxonomy import canonical_summary

SOURCE_TEXT = "Explicitly synthetic offline source text. No real theorem or scientific result is asserted."
SOURCE_HASH = hashlib.sha256(SOURCE_TEXT.encode("utf-8")).hexdigest()


def synthetic_profile(sid, order=0):
    common = {axis.lower(): {"summary": f"Synthetic explicit {axis.lower()} contract.", "statements": []} for axis in AXES}
    common["task"]["navigation_domains"] = ["matrix_computation"]
    common["oracle"]["operations"] = [{"id": "right", "operation_code": "right_matvec", "target_object": "A",
        "feedback_quality": {"code": "exact"}, "returns": ["matrix_product"]}]
    return {
        "schema_version": "1.0.0", "setting_id": sid, "title": f"Synthetic existing contract {sid}",
        "primary_domain": "matrix_computation", "common_specification": common,
        "views": [{"view_id": "randomized", "label": "Randomized", "algorithms": {"randomization": "randomized_allowed"},
                   "guarantees": [{"guarantee_id": "g", "summary": "Synthetic per-instance success."}],
                   "specification_overrides": {}, "alias_ids": []}],
        "parameters": [{"id": "n", "symbol": "n"}], "symbols": [], "quantities": [{"id": "q"}], "resource_projections": [{"id": "rp"}],
        "regimes": [{"id": "r", "predicate_text": "Synthetic regime only"}],
        "bounds": [{"id": "u", "direction": "upper", "view_id": "randomized", "guarantee_id": "g",
                    "quantity_ref": "q", "region_refs": ["r"], "eligible_for_bracket": True,
                    "witness_type": "deterministic", "formula_latex": "SYNTHETIC_OLD_RATE"}],
        "comparisons": [{"comparison_id": "c", "comparison_key": {"setting_id": sid, "view_id": "randomized",
            "guarantee_id": "g", "quantity_id": "q", "resource_projection_id": "rp", "regime_id": "r"},
            "status": {"code": "missing_lower", "label": "Lower bound missing", "missing_sides": ["lower"]},
            "bracket": {"upper_refs": ["u"], "lower_refs": []}}],
        "bracket_rows": [], "summary_status": {"scope": "documented_comparison_domain",
            "comparison_count": 1, "status_counts": {"missing_lower": 1}, "gap_classes": [],
            "missing_sides": ["lower"], "badges": [{"code": "bounds_missing", "label": "Bounds missing"}],
            "special_statuses": []},
        "proofs": [], "evidence": [], "references": [{"id": "synthetic_source", "title": "Explicit synthetic fixture, not a real theorem"}], "relations": [], "facets": [], "aliases": [],
        "provenance": {"source_order": order, "synthetic_fixture": True},
    }


def synthetic_facts():
    values = {"TASK": ("task_family", "matrix_computation"), "MODEL": ("structure", "arbitrary_real_matrix"),
              "ORACLE": ("operation", "right_matvec"), "ALGORITHMS": ("randomization", "private_randomness_allowed"),
              "OUTPUT": ("object", "matrix"), "METRIC": ("criterion", "exact_recovery"),
              "GUARANTEE": ("mode", "probability"), "RESOURCE": ("measure", "oracle_calls")}
    return [{"concept_id": f"{axis}:{group}:{value}", "axis": axis, "value": value,
             "object_ref": None, "view_ref": None, "operation_ref": None,
             "source_pointer": f"/common_specification/{axis.lower()}/summary", "status": "known"}
            for axis, (group, value) in values.items()]


def seed_atlas(root, ids=("SYNTHETIC_UNCHANGED", "SYNTHETIC_UPDATED")):
    atlas = Atlas(root)
    for order, sid in enumerate(ids):
        profile = synthetic_profile(sid, order)
        prepared = atlas.prepare(profile, synthetic_facts(), None)
        review = {"verdict": "approve", "prepared_hash": prepared["bundle_hash"],
                  "approved_bound_ids": ["u"], "issues": []}
        atlas.commit(prepared, review, "synthetic-seed:" + sid)
    return atlas


class SyntheticBibliography:
    """A local provider fixture; the real metadata tool still audits each call."""
    def search(self, provider, query, *, year, limit, cursor):
        return {"provider": provider, "records": [], "total": 0, "next_cursor": None}


class SyntheticTools(MaintenanceTools):
    """Real bounded tools over local synthetic bytes; never real literature evidence."""
    def __init__(self, atlas_root, cache_dir, context, config):
        fixture_context = deepcopy(context)
        fixture_context["allowed_source_hashes"] = sorted(set(context.get("allowed_source_hashes", [])) | {SOURCE_HASH})
        super().__init__(atlas_root, cache_dir, fixture_context, config)
        self._bibliography = SyntheticBibliography()
        source_root = Path(cache_dir) / "sources"
        for directory in ("text", "original"):
            path = source_root / directory / (SOURCE_HASH + ".txt")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(SOURCE_TEXT, encoding="utf-8")
        write_json(source_root / "metadata" / (SOURCE_HASH + ".json"), {
            "content_hash": SOURCE_HASH, "text_sha256": SOURCE_HASH,
            "url": "synthetic:offline-fixture", "synthetic_fixture": True, "locators": []})


def fixture_call(host, name, arguments):
    result = host.call(name, arguments)
    if result.get("error"):
        raise AssertionError("Synthetic tool fixture failed: " + result["error"])
    return result


def fixture_read_prepared_analysis(host):
    offset = 0
    while True:
        result = fixture_call(host, "artifact_read", {
            "name": "prepared", "pointer": "/joint_analysis", "offset": offset, "limit": 10000})
        offset = result["next_offset"]
        if offset is None:
            return


class ScriptedRunner:
    """Explicit fake runner. Its outputs test orchestration, never mathematical truth."""
    def __init__(self, behaviors=None, verdicts=None):
        self.behaviors = dict(behaviors or {})
        self.verdicts = dict(verdicts or {})
        self.calls = []
        self.last_metrics = {"synthetic_fixture": True, "model_calls": 0, "network_calls": 0}

    def run(self, role, context, host, task_key):
        sid = context["setting_id"]
        self.calls.append({"role": role, "setting_id": sid, "task_key": task_key})
        if role not in {"scout", "reviewer"}:
            raise AssertionError("Existing-setting maintenance must not invoke extraction or matching")
        if role == "reviewer":
            fixture_call(host, "source_read", {"source_hash": SOURCE_HASH, "offset": 0, "limit": 10000})
            fixture_read_prepared_analysis(host)
            return {"setting_id": sid, "base_version": context["base_version"],
                    "prepared_hash": context["prepared_hash"], "verdict": self.verdicts.get(sid, "approve"),
                    "approved_bound_ids": ["u"], "reviewed_comparison_ids": ["c"], "issues": [],
                    "joint_analysis_hash": context.get("joint_analysis_hash"),
                    "joint_checks": {key: True for key in ("parameter_roles", "guarded_envelopes", "domain_accounting", "improvement_regions", "provenance", "display_consistency")},
                    "rationale": "Synthetic independent reviewer fixture; no scientific acceptance claimed"}
        behavior = self.behaviors.get(sid, "no_change")
        fixture_call(host, "bibliography_search", {"provider": "crossref", "query": "Synthetic finite local fixture",
            "year": None, "cursor": None, "limit": 1})
        scope = {"queries_complete": behavior != "incomplete", "examined_comparison_ids": ["c"],
                 "unresolved_leads": ["Synthetic unread lead"] if behavior == "incomplete" else [],
                 "note": "Synthetic finite test scope, not a literature claim"}
        result = {"setting_id": sid, "base_version": context["base_version"], "cutoff": context["cutoff"],
                  "outcome": behavior, "scope": scope, "findings": [], "patch": [], "summary_status_json": None,
                  "joint_analysis_reuse": None,
                  "rationale": "Synthetic offline orchestration fixture"}
        if behavior in {"candidate_change", "partial_change"}:
            result["outcome"] = "candidate_change"
            if behavior == "partial_change":
                scope.update(queries_complete=False, unresolved_leads=["Synthetic independent pending lead"])
            before = context["artifacts"]["baseline"]["bounds"][0]
            updated = {**before, "formula_latex": "SYNTHETIC_NEW_RATE"}
            result["patch"] = [{"collection": "bounds", "id_field": "id", "id": "u",
                                "before_hash": digest(before), "value_json": json.dumps(updated)}]
            result["findings"] = [{"candidate_id": "synthetic-result", "impact": "improve_upper",
                                   "comparison_ids": ["c"], "source_hashes": [SOURCE_HASH],
                                   "reason": "Synthetic fixture changes the expression while keeping summary status"}]
        elif behavior == "no_change":
            result["findings"] = [{"candidate_id": "synthetic-no-effect", "impact": "no_effect",
                "comparison_ids": ["c"], "source_hashes": [SOURCE_HASH],
                "reason": "The explicitly fake source does not change this synthetic baseline"}]
        if result["findings"]:
            fixture_call(host, "source_read", {"source_hash": SOURCE_HASH, "offset": 0, "limit": 10000})
        if behavior != "incomplete":
            proposed = deepcopy(context["artifacts"]["baseline"])
            if result["patch"]:
                proposed["bounds"][0] = json.loads(result["patch"][0]["value_json"])
            result["joint_analysis_json"] = json.dumps(synthetic_analysis(proposed, result, baseline=context["artifacts"]["baseline"]))
        else:
            result["joint_analysis_json"] = None
        result["quantity_metadata_normalizations"] = []
        return result


def synthetic_analysis(profile, report, *, baseline=None):
    """Fully explicit fake synthesis used only to test the actual controller gates."""
    analysis = analysis_template(profile, version=2)
    analysis["target"].update(joint_variables=["n"], uniform_in=["n"],
                              full_domain="Synthetic n >= 1", resolution="resolved")
    analysis["normalization_requests"] = []
    analysis["pending_obligations"] = list(report["scope"]["unresolved_leads"])
    analysis["domain_map"].update(status="accounted", residual_domain="empty inside the synthetic domain",
                                  partition_argument="One synthetic comparison covers the declared fixture domain")
    analysis["synthesis_coverage"] = synthesis_template(profile if baseline is None else baseline, profile)
    coverage = analysis["synthesis_coverage"]
    coverage["status"] = "partial" if analysis["pending_obligations"] else "complete"
    coverage["literature"] = {
        "status": "finite_scope_complete" if report["scope"].get("queries_complete", True) and not report["scope"]["unresolved_leads"] else "partial",
        "scope": "One explicitly fake local bibliography query; no real literature conclusion."}
    for obligation in coverage["obligations"]:
        obligation.update(state="not_applicable" if obligation["kind"] == "resource_projection" else "resolved",
                          argument="Distinct synthetic quantities are not transferred; the remaining fake candidate ledger is explicit and no real theorem is certified.")
    for index, lead in enumerate(analysis["pending_obligations"]):
        coverage["obligations"].append({"id": "synthetic-pending-" + str(index), "kind": "material_lead",
            "comparison_ids": list(report["scope"]["examined_comparison_ids"]), "bound_refs": [], "cell_ids": [],
            "state": "pending", "affects_gap": False, "lead": lead,
            "argument": "An explicitly independent synthetic pending lead remains unassessed.", "proof_refs": []})
    for row in analysis["comparisons"]:
        row["upper_envelope"] = profile["bounds"][0]["formula_latex"]
        row["lower_envelope"] = "missing"
        row["gap"] = "missing lower"
        row["boundary_checks"] = ["Synthetic fixture has no additional boundary"]
    if report["outcome"] == "candidate_change":
        for row in analysis["provenance"]:
            row.update(origin="source_theorem", source_refs=["synthetic_source"],
                       source_locator="Synthetic fixture text", source_domain="Synthetic n >= 1",
                       mapping="Synthetic exact contract")
    analysis["impact"] = [{"finding_id": f["candidate_id"], "comparison_ids": f["comparison_ids"],
        "kind": "no_effect" if f["impact"] in {"no_effect", "incomparable"} else "bound_improvement",
        "old_envelope": "SYNTHETIC_OLD_RATE", "new_envelope": "SYNTHETIC_NEW_RATE" if report["outcome"] == "candidate_change" else "SYNTHETIC_OLD_RATE",
        "validity_region": "Synthetic n >= 1", "improvement_region": "Synthetic n >= 1",
        "unchanged_region": "empty", "witness": "Synthetic test witness only",
        "boundary_type": "not_applicable", "argument": "Synthetic fixture, not a mathematical proof", "extension_witness": None}
        for f in report["findings"]]
    return analysis


def demo_config(output):
    output = Path(output)
    return {"atlas": str(output / "atlas"), "workspace": str(output / "work"), "timezone": "UTC",
            "backend": "synthetic-test-only", "model": {},
            "maintenance": {"min_recheck_days": 14, "overlap_days": 30},
            "budgets": {"compact_profile_chars": 14000}}


def run_demo(output):
    output = Path(output).resolve()
    config = demo_config(output)
    if (output / "atlas").exists() or (output / "work").exists():
        raise ValueError("Choose a fresh output directory; the demo never overwrites an existing Atlas or workspace")
    native = seed_atlas(config["atlas"])
    runner = ScriptedRunner({"SYNTHETIC_UPDATED": "candidate_change"})
    maintenance = Maintenance(config, runner=runner, tools_factory=SyntheticTools)
    plan = maintenance.plan()
    staged = maintenance.run(plan["run_id"])
    committed = maintenance.apply(plan["run_id"])
    replay = maintenance.apply(plan["run_id"])
    assert staged["counts"] == {"no_change": 1, "staged": 1}
    assert committed["counts"] == replay["counts"] == {"no_change": 1, "committed": 1}
    assert len(runner.calls) == 3
    assert native.read("SYNTHETIC_UPDATED")["bounds"][0]["formula_latex"] == "SYNTHETIC_NEW_RATE"
    for name in FILES:
        assert native.read("SYNTHETIC_UPDATED", name)["setting_id"] == "SYNTHETIC_UPDATED"
    report = {"acceptance": "offline engineering only; synthetic mathematics",
              "real_model_acceptance": False, "network_acceptance": False, "production_atlas_modified": False,
              "native_five_file_commit": True, "ordered_ids": maintenance.state.plan(plan["run_id"])["setting_ids"],
              "calls": runner.calls, "staged": staged, "committed": committed, "idempotent_reapply": replay}
    write_json(output / "demo-report.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    output = arguments.output or Path(tempfile.mkdtemp(prefix="oracle-maintenance-demo-"))
    report = run_demo(output)
    print(json.dumps({"report": str(output.resolve() / "demo-report.json"),
                      "counts": report["committed"]["counts"], "native_five_file_commit": True,
                      "acceptance": report["acceptance"]}, indent=2))


if __name__ == "__main__":
    main()
