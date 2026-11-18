"""Offline expansion acceptance using the actual engine, tools, reviews, and writer.

All scientific judgments are scripted synthetic fixtures. No model or network is
called. The example checks software integration, not the scientific performance
of an LLM, literature coverage, or novel research. Never use its Atlas in production.

Run: python examples/offline_expansion_demo.py --output /tmp/atlas-expansion-demo
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT / "src"))

_SPEC = importlib.util.spec_from_file_location("expansion_demo_shared", Path(__file__).with_name("offline_demo.py"))
BASE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(BASE)

from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.store import dumps
from oracle_atlas.expansion.engine import ExpansionEngine
from oracle_atlas.workflow.coverage import CHECKS


NOTICE = ("Offline synthetic expansion acceptance: no real model or network was called. "
          "Scripted decisions exercise actual tools and independent jobs; receipts establish software integration only.")
SEED_ID = "DEMO_QUADRATIC_VALUE_SEED"
SOURCE_VERSION = "synthetic-expansion-seed-v1"
SOURCE_TEXT = """SYNTHETIC DEFINITION, NOT A PAPER.
Let a be an unknown bit in {0,1}. Minimize f_a(x)=(x-a)^2 over R.
An exact value query at x returns f_a(x) and costs one unit. The family is public;
only a is hidden. One value at zero identifies a. A zero-query deterministic
output cannot equal both minimizers 0 and 1. The initial Atlas contains this
value-only setting with a deterministic view. Additional oracle contracts in
the expansion example are designed definitions, not claims extracted from this text.
"""


def case_definition(kind):
    case = deepcopy(BASE.CASES["new_setting"])
    if kind == "gradient":
        case.update(setting_id="DEMO_EXPANDED_GRADIENT", title="[SYNTHETIC] Two-shift quadratics with gradient-only queries")
    elif kind == "value_gradient":
        case.update(setting_id="DEMO_EXPANDED_VALUE_GRADIENT", title="[SYNTHETIC] Two-shift quadratics with value-and-gradient queries",
                    oracle="value_gradient", returns=["value", "gradient"])
    else:
        case.update(setting_id=SEED_ID, title="[SYNTHETIC] Two-shift quadratics with value-only queries",
                    oracle="function_value", returns=["value"], view="randomized" if kind == "existing_view" else "deterministic")
    return case


def profile_for(case, source_ref):
    profile = BASE.base_profile("new_setting", source_ref)
    profile.update(setting_id=case["setting_id"], title=case["title"],
                   common_specification=BASE.specification(case, source_ref), views=[BASE.view(case["view"])],
                   aliases=[{"legacy_id": case["setting_id"] + "_det", "view_id": "deterministic"}],
                   provenance={"synthetic": True, "source_snapshot": SOURCE_VERSION})
    return profile


def opportunities():
    definitions = [
        ("gradient", "oracle_substitution", ["ORACLE"], 100,
         "Replace exact value replies by an exact gradient-only reply while keeping the quadratic family fixed.",
         "Exercise a native interface change with a short independently reviewable one-query bracket."),
        ("value_gradient", "oracle_substitution", ["ORACLE"], 90,
         "Replace value-only replies by value-and-gradient replies from the same query.",
         "Check that equal toy rates do not merge different native information interfaces."),
        ("existing_view", "algorithm_permission", ["ALGORITHMS", "GUARANTEE"], 80,
         "Allow randomization with per-instance success at least two thirds under the original exact value oracle.",
         "Exercise redirection into an existing profile's new view rather than creating a duplicate setting."),
        ("duplicate_gradient", "oracle_substitution", ["ORACLE"], 70,
         "Reach the same gradient-only candidate through another planning description.",
         "Exercise independent comparison against pending batch candidates before spending research budget."),
    ]
    return [{"opportunity_id": oid, "title": case_definition("gradient" if oid == "duplicate_gradient" else oid)["title"],
             "seed_setting_ids": [SEED_ID], "neighbor_setting_ids": [], "operators": [operator],
             "changed_axes": axes, "target_task_ids": ["single_objective"], "mutation_steps": 1,
             "transformation": transformation, "selection_reason": reason,
             "expected_value": "Synthetic protocol verification; no literature novelty claim.",
             "transfer_leads": ["Use the two distinct exact minimizers to check the zero-query boundary."],
             "risks": ["A shared one-query rate is not native-interface identity."], "priority_score": score}
            for oid, operator, axes, score, transformation, reason in definitions]


def designed_candidate(oid, inputs, *, incomplete=False):
    kind = "gradient" if oid == "duplicate_gradient" else oid
    case = case_definition(kind)
    source_ref = inputs["seed_refs"][0]
    specification = BASE.specification(case, source_ref)
    if kind in {"gradient", "value_gradient"}:
        # The new interface is a designed contract, not a claim from the old seed.
        specification["oracle"]["statements"][0]["evidence_refs"] = []
    if incomplete:
        text = "Output a minimizer; permission to output an unqueried point is not yet specified."
        specification["output"]["summary"] = text
        specification["output"]["statements"][0].update(text=text, status="unknown")
    return {"candidate_id": "expansion_fixture_" + oid, "title": case["title"], "paper_refs": [],
            "common_specification": specification, "views": [BASE.view(case["view"])],
            "tag_facts": BASE.tag_facts(case, case["view"]), "issues": [], "synthetic_kind": kind,
            "origin": {"kind": "atlas_expansion", "request_ref": inputs["request_ref"], "plan_ref": inputs["plan_ref"],
                       "opportunity_id": oid, "seed_refs": inputs["seed_refs"], "designed_contract": True}}


class OfflineExpansionBackend(BASE.ScriptedBackend):
    """Fixed test choices, confined to examples; the production agents contain none of them."""

    def __init__(self, *, revise_first=False):
        super().__init__()
        self.revise_first = revise_first

    def _program(self, job):
        role, inputs = job["role"], job["inputs"]
        if role in {"identity_reviewer", "profile_reviewer"}:
            return (yield from super()._program(job))
        main = {"expansion_planner": "expansion_plan", "setting_expander": "expansion",
                "expansion_reviewer": "expansion_review", "matcher": "identity", "profile_researcher": "research"}[role]
        yield from self._call("schema_read", kind=main)
        if role == "expansion_planner":
            yield from self._read(inputs["request_ref"])
            yield from self._read(inputs["neighborhood_ref"])
            yield from self._read(inputs["history_ref"])
            plan = {"request_ref": inputs["request_ref"], "neighborhood_ref": inputs["neighborhood_ref"],
                    "opportunities": opportunities(), "not_pursued": [], "coverage_note": NOTICE}
            return self._finish((yield from self._put("expansion_plan", plan)))
        if role == "setting_expander":
            plan = yield from self._read(inputs["plan_ref"])
            yield from self._read(inputs["request_ref"])
            for ref in inputs["seed_refs"]:
                yield from self._call("source_read", ref=ref, offset=0, limit=10000)
            if inputs.get("repair_feedback_ref"):
                yield from self._read(inputs["repair_feedback_ref"])
                yield from self._read(inputs["previous_candidate_ref"])
            oid = inputs["opportunity_id"]
            op = next(item for item in plan["opportunities"] if item["opportunity_id"] == oid)
            candidate = designed_candidate(oid, inputs, incomplete=self.revise_first and oid == "gradient" and not inputs.get("revision"))
            cref = yield from self._put("candidate", candidate)
            expansion = {"request_ref": inputs["request_ref"], "plan_ref": inputs["plan_ref"],
                         "opportunity_id": oid, "candidate_ref": cref,
                         "changes": [{"axis": axis, "object_ref": "f", "before": "The seed's declared contract.",
                                      "after": op["transformation"], "reason": op["selection_reason"]} for axis in op["changed_axes"]],
                         "well_posedness": {"nonempty": "supported", "objective_defined": "supported",
                                             "oracle_implementable": "supported", "not_trivial": "supported",
                                             "checks": ["Both quadratic instances exist; their exact minimizers differ; the chosen oracle is an explicit algebraic map."],
                                             "unknowns": []}, "selection_reason": op["selection_reason"], "issues": []}
            yield from self._call("memory_save", text="PRIVATE_SYNTHETIC_PRODUCER: designed candidate, not adopted evidence.", refs=[cref])
            return self._finish((yield from self._put("expansion", expansion)))
        if role == "expansion_reviewer":
            expansion = yield from self._read(inputs["subject_ref"])
            candidate = yield from self._read(inputs["candidate_ref"])
            peers, duplicate = [], None
            for ref in inputs["peer_candidate_refs"]:
                peer = yield from self._read(ref)
                same = peer["common_specification"] == candidate["common_specification"] and peer["views"] == candidate["views"]
                peers.append({"candidate_ref": ref, "relation": "equivalent" if same else "distinct",
                              "reason": "Synthetic comparison of the fully declared contracts and views."})
                if same:
                    duplicate = ref
            revise = self.revise_first and expansion["opportunity_id"] == "gradient" and not inputs.get("revision")
            memory = yield from self._call("memory_search", query="PRIVATE_SYNTHETIC_PRODUCER", limit=5)
            self.review_memory.append(memory)
            review = {"subject_ref": inputs["subject_ref"], "candidate_ref": inputs["candidate_ref"],
                      "verdict": "exclude" if duplicate else "revise" if revise else "approve",
                      "reason": NOTICE, "scope_assessment": "The synthetic candidate stays within the finite request.",
                      "well_posedness_assessment": "The two specified quadratic instances have distinct exact minimizers and explicit oracle maps.",
                      "value_assessment": "Software acceptance only; scientific research value is not evaluated.",
                      "pending_comparisons": peers, "duplicate_of_ref": duplicate, "issues": [],
                      "required_changes": ["Explicitly state whether unqueried output points are allowed."] if revise else []}
            return self._finish((yield from self._put("expansion_review", review)))
        if role == "matcher":
            candidate = yield from self._read(inputs["candidate_ref"])
            yield from self._read(inputs["candidate_review_ref"])
            yield from self._call("atlas_search", candidate_ref=inputs["candidate_ref"], limit=30, offset=0, broaden=False)
            found = yield from self._call("atlas_search", candidate_ref=inputs["candidate_ref"], limit=30, offset=0, broaden=True)
            kind = candidate["synthetic_kind"]
            target = case_definition(kind)["setting_id"]
            comparisons = []
            for entry in found["candidates"]:
                native = yield from self._call("atlas_read", setting_id=entry["setting_id"], filename="profile.json",
                                               pointer="/common_specification", offset=0, limit=10000)
                comparisons.append({"setting_id": entry["setting_id"], "relation": "same" if entry["setting_id"] == target else "different",
                                    "reason": "Synthetic native-interface comparison: the objective family is fixed; value, gradient, and combined replies remain distinct. Randomization changes a view.",
                                    "evidence_refs": [native["ref"]]})
            existing = any(item["setting_id"] == target for item in found["candidates"])
            identity = {"candidate_ref": inputs["candidate_ref"], "decision": "existing" if existing else "new",
                        "setting_id": target if existing else None,
                        "view_mapping": [{"candidate_view_id": candidate["views"][0]["view_id"], "atlas_view_id": None,
                                          "reason": "A new fixture view is proposed only within the exact matching common contract."}],
                        "normalization": "No transformation or capability simulation is assumed.", "comparisons": comparisons,
                        "retrieval_ref": found["retrieval_ref"], "recall_audit": {
                            "strategies": ["task_oracle_concepts", "title_formulation", "unknown_retained"], "unresolved_ids": [],
                            "reason": "All entries in the small synthetic inventory were read. No literature novelty claim.",
                            "inventory_version": found["inventory_version"]}, "issues": []}
            return self._finish((yield from self._put("identity", identity)))
        if role == "profile_researcher":
            return (yield from self._research_expansion(inputs))
        raise RuntimeError(f"Unsupported offline expansion role {role}")

    def _research_expansion(self, inputs):
        yield from self._call("schema_read", kind="joint_analysis")
        candidate = yield from self._read(inputs["candidate_ref"])
        yield from self._read(inputs["identity_ref"])
        source_ref = candidate["origin"]["seed_refs"][0]
        source = yield from self._read(source_ref)
        case = case_definition(candidate["synthetic_kind"])
        p = profile_for(case, source_ref)
        p["common_specification"] = deepcopy(candidate["common_specification"])
        p["relations"] = [{"setting_id": SEED_ID, "relation": "oracle_substitution", "description": "Same two-shift family, different native replies."}]
        p["provenance"].update(designed_contract=True, origin_ref=inputs["origin_ref"])
        proof = {"proof_id": "one_query_" + candidate["synthetic_kind"], "origin": "analyst_derivation",
                 "proposition": "Exactly one query solves the declared two-shift quadratic toy model.",
                 "premises": [case["formulation"], "Only the declared exact native query is allowed; all public internal computation is free."],
                 "argument": "A gradient query at zero returns -2a. The combined oracle also returns this gradient. Output -gradient/2. Without queries a deterministic output is identical on both inputs, but the exact minimizers are respectively 0 and 1, so it fails on one instance.",
                 "boundary_cases": "The family has exactly the two specified distinct inputs; the zero-query case is included.",
                 "quantifiers": "A single deterministic algorithm must succeed on every one of the two fixed instances.",
                 "resource_accounting": "One charged primitive reply, followed by free arithmetic on the reply.",
                 "dependencies": [inputs["candidate_ref"], source_ref], "issues": []}
        proof_ref = yield from self._put("proof", proof)
        result_refs = []
        for direction in ("upper", "lower"):
            result = {"result_id": candidate["synthetic_kind"] + "_" + direction,
                      "comparison_key": {"setting_id": p["setting_id"], "view_id": "deterministic", "guarantee_id": "g_deterministic",
                                         "quantity_id": "q", "resource_projection_id": "rp", "regime_id": "r"},
                      "direction": direction, "statement": "One query is sufficient." if direction == "upper" else "At least one query is necessary.",
                      "formula_latex": "1", "conditions": [case["model"], "Exact minimization with the declared native oracle."],
                      "parameter_region": "The complete two-instance toy family.", "algorithm_scope": "All deterministic sequential adaptive algorithms; no span restriction.",
                      "witness_type": "deterministic" if direction == "upper" else None,
                      "guarantee": "Exact minimization separately for each fixed instance.", "resource_accounting": "Fixed worst-case primitive queries.",
                      "origin": "analyst_derivation", "source_refs": [source_ref],
                      "source_locators": [{"source_ref": source_ref, "version": source["version"], "locator": "Seed snapshot: common_specification.model; the changed oracle is defined in candidate_ref."}],
                      "proof_refs": [proof_ref], "status": "proposed", "issues": []}
            result_ref = yield from self._put("result", result)
            result_refs.append(result_ref)
            p["bounds"].append(BASE.bound(direction, "deterministic", [result_ref], [proof_ref]))
        p["comparisons"] = [BASE.comparison(p["setting_id"], "deterministic")]
        p["bracket_rows"] = [{"row_id": "toy_closed", "comparison_ids": ["comparison_deterministic"], "view_ids": ["deterministic"]}]
        p["summary_status"] = {"label": "All optimal", "coverage": "Synthetic two-instance domain only; not a literature survey."}
        p["proofs"] = [{"proof_id": proof["proof_id"], "artifact_ref": proof_ref, "origin": "analyst_derivation"}]
        p["evidence"] = [{"id": "e_" + str(i), "artifact_ref": ref} for i, ref in enumerate(result_refs)]
        p = BASE.SYNTHETIC.complete_synthetic_profile(p, proof_argument=proof["argument"])
        profile_ref = yield from self._draft_profile(p)
        yield from self._call("memory_save", text="PRIVATE_SYNTHETIC_PRODUCER: one-query derivation awaits independent review.", refs=[profile_ref, proof_ref, *result_refs])
        research = {"candidate_ref": inputs["candidate_ref"], "identity_ref": inputs["identity_ref"], "action": "new",
                    "setting_id": p["setting_id"], "base_version": None, "profile_ref": profile_ref,
                    "result_refs": result_refs, "proof_refs": [proof_ref], "issues": [], "change_summary": NOTICE,
                    "coverage_ledger": {"scope": NOTICE, "checks": [{"check_id": key, "scope": "Synthetic toy contract only.",
                        "status": "not_applicable", "reason": NOTICE, "result_refs": [], "proof_refs": []} for key in CHECKS], "issue_resolutions": []}}
        research["research_scope"] = BASE.SYNTHETIC.synthetic_research_scope()
        return self._finish((yield from self._put("research", research)))


class NoNetworkBibliography:
    def search(self, *args, **kwargs):
        raise AssertionError("The offline expansion demo must not search the network")


def setup_demo(output: Path, *, revise_first=False):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    backend = OfflineExpansionBackend(revise_first=revise_first)
    cfg = {"workspace": str(output / "work"), "atlas": str(output / "atlas"), "model": {"model": "synthetic-scripted-backend"},
           "budgets": {**DEFAULTS, "max_turns": 90, "max_segments": 16, "max_total_calls": 300, "max_jobs": 80},
           "expansion": {"max_batch_model_calls": 1600, "max_batch_external_calls": 600, "max_batch_jobs": 240},
           "tasks": [{"task_id": "single_objective", "label": "Single objective", "queries": [], "approved": True}]}
    engine = ExpansionEngine(cfg, backend, bibliography=NoNetworkBibliography())
    source_ref = engine.put("source", {"url": "urn:oracle-atlas:synthetic:expansion-seed", "version": SOURCE_VERSION,
        "content_hash": hashlib.sha256(SOURCE_TEXT.encode()).hexdigest(), "text": SOURCE_TEXT, "metadata": {"synthetic": True, "notice": NOTICE}})
    seed_case = case_definition("seed")
    p = profile_for(seed_case, source_ref)
    p["bounds"] = [BASE.bound(direction, "deterministic", []) for direction in ("upper", "lower")]
    p["comparisons"] = [BASE.comparison(SEED_ID, "deterministic")]
    p["summary_status"] = {"label": "All optimal", "coverage": "Synthetic initial seed only."}
    p = BASE.SYNTHETIC.complete_synthetic_profile(p)
    if engine.atlas.version(SEED_ID) is None:
        prepared = engine.atlas.prepare(p, BASE.tag_facts(seed_case, "deterministic"), None)
        engine.atlas.commit(prepared, {"verdict": "approve", "prepared_hash": prepared["bundle_hash"],
            "approved_bound_ids": [b["id"] for b in p["bounds"]], "issues": [], "synthetic_seed": True,
            "joint_review": BASE.SYNTHETIC.synthetic_joint_review(prepared)}, "synthetic-expansion-seed")
    request = {"seed_setting_ids": [SEED_ID], "source_task_ids": ["single_objective"], "target_task_ids": ["single_objective"],
               "allowed_operators": ["oracle_substitution", "algorithm_permission"], "allowed_axes": ["ORACLE", "ALGORITHMS", "GUARANTEE"],
               "scope_description": NOTICE, "fixed_constraints": ["Keep the exact two-shift quadratic family and exact minimization target."],
               "max_seeds": 1, "max_neighbors_per_seed": 2, "max_opportunities": 4,
               "max_candidates": 4, "max_profiles": 2, "max_mutation_steps": 1, "max_per_seed": 4, "max_per_operator": 4,
               "allow_existing_updates": False, "run_label": "synthetic-expansion-v1"}
    return engine, backend, request


def run_demo(output: Path):
    engine, backend, request = setup_demo(output)
    try:
        before = engine.expand(request)
        research_calls = backend.calls_by_role["profile_researcher"]
        published = engine.publish(before["batch_id"])
        publish_research_calls = backend.calls_by_role["profile_researcher"] - research_calls
        calls_before_repeat = backend.calls
        versions = {row["setting_id"]: row["profile_version"] for row in engine.atlas.catalog()}
        repeated = engine.expand(request)
        cases = [engine.ws.case(row["case_id"]) for row in published["cases"]]
        report = {"notice": NOTICE, "synthetic": True, "real_model_calls": 0, "network_calls": 0,
                  "before_publication": before, "after_publication": published, "repeat": repeated,
                  "scripted_backend_calls": backend.calls, "calls_by_role": dict(backend.calls_by_role),
                  "repeat_added_calls": backend.calls - calls_before_repeat,
                  "publication_added_research_calls": publish_research_calls,
                  "receipt_refs": [c["receipt_ref"] for c in cases if c.get("receipt_ref")],
                  "identity_refresh_cases": [c["case_id"] for c in cases if c.get("rebase_context_ref")],
                  "versions_unchanged_on_repeat": versions == {row["setting_id"]: row["profile_version"] for row in engine.atlas.catalog()},
                  "tool_errors": backend.observed_tool_errors, "reviewer_private_memory_hits": backend.review_memory,
                  "paper_artifact_count": engine.ws.query("SELECT COUNT(*) AS n FROM artifacts WHERE kind='paper'")[0]["n"]}
        report["synthetic_budget_note"] = "This fixed scripted fixture explicitly allows 16 segments and 90 turns per job for the current science contracts. The 60000-character input cap and finite call/job limits remain enforced; production defaults are unchanged."
        Path(output, "offline_expansion_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        lines = ["# Offline expansion acceptance", "", NOTICE, "", "| Candidate | Result | Selection reason |", "| --- | --- | --- |"]
        for row in published["cases"]:
            lines.append(f"| {row['title']} | {row['state']} | {row['selection_reason']} |")
        lines += ["", f"New transaction receipts: {len(report['receipt_refs'])}.",
                  f"Additional research calls during publication refresh: {publish_research_calls}.",
                  f"Additional scripted calls on repeat: {report['repeat_added_calls']}.",
                  "", "The seed and final profiles are synthetic. No findings from real literature were added.",
                  "", report["synthetic_budget_note"]]
        Path(output, "offline_expansion_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        return report
    finally:
        engine.ws.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = run_demo(args.output)
    print(NOTICE)
    print(json.dumps({"states": report["after_publication"]["state_counts"], "receipts": len(report["receipt_refs"]),
                      "repeat_added_calls": report["repeat_added_calls"], "report": str(args.output / "offline_expansion_report.json")}, indent=2))
    if len(report["receipt_refs"]) != 2 or report["repeat_added_calls"] or report["tool_errors"] or report["publication_added_research_calls"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
