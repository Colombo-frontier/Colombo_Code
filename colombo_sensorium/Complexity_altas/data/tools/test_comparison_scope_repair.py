#!/usr/bin/env python3
"""Regression checks for the 2026-11-22 comparison-scope repair.

These tests exercise the native predicates and support graph. Synthetic values
for proof constants test routing only; they do not assign constants to external
theorems or certify those theorems. Run with Python's standard unittest runner.
"""

import hashlib
import json
import math
import operator
from pathlib import Path
import unittest


ATLAS = Path(__file__).resolve().parents[2]
FO = "SO_FO_N01_L1_G"
FO_PREFIX = FO + "__randomized__expected_loss__"
HOC = "SO_HO_HOC01_S_full"
HOC_PREFIX = HOC + "__randomized__"
BL = "BL_SPEC_joint_expected_cost"
BL_PROOF = BL + "__main__p_zero_query"
BL_EVIDENCE = BL + "__main__e3"

# Frozen claims first observed in commit 996c941; these are audit identities,
# deliberately not recomputed from today's mathematical fields.
BL_ORIGINAL_PREMISES = (
    ("/common_specification", "ceca4e7c6ec43934abd8aad69c1dc4ce7a250f35e14a5835efc6ac1e1a04705f"),
    ("/parameters", "6bd2eebfbb8e22955d1cb7d4f8c0c254d7b6bf1d37babcd44050b9feb6762e3c"),
    ("/quantities/0", "4d8fd29b92a3bf0092ebb4fecb0fd15deb2ca05a0dbe355fff32934843c8e0c2"),
    ("/views", "369bfdfba279f845c0805be2ec40d8770d10503770c5399b0c2116dd86757a7d"),
    ("/resource_projections/0", "fd19c50dc5cbe6d31f7b8408a3fe9b0866f63f570e249a91326a5b72eb7b18ed"),
    ("/bounds/1", "40bba78e2aefee06fb788a9fa40c046a8af71108d2018f1d3f2425119cc96e88"),
    ("/comparisons/0", "3cc36dd53a1b28b7ec361c916a618d99b2a146810a43c242b9c0ca520e5d57dc"),
    ("/regimes", "08e51bb1f0fba5279523f61420bf98323829aa188915d03823a6b597a8834009"),
)


def read_profile(setting_id):
    return json.loads((ATLAS / "data/settings" / setting_id / "profile.json").read_text())


def canonical_sha(value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def indexed(profile, field, key="id"):
    return {record[key]: record for record in profile[field]}


class PredicateReader:
    """Small independent interpreter for the mathematical AST used in scopes."""

    def __init__(self, profile, values):
        self.regimes = indexed(profile, "regimes")
        self.values = {
            parameter["id"]: values[parameter["symbol"]]
            for parameter in profile["parameters"]
            if parameter["symbol"] in values
        }

    def region(self, regime_id):
        regime = self.regimes[regime_id]
        parent = regime.get("universe_ref")
        return (not parent or self.region(parent)) and bool(self.eval(regime["predicate"]))

    def eval(self, expression):
        if isinstance(expression, (int, float)):
            return expression
        if "all" in expression:
            return all(self.eval(item) for item in expression["all"])
        if "any" in expression:
            return any(self.eval(item) for item in expression["any"])
        if "not" in expression:
            return not self.eval(expression["not"])
        if "region_ref" in expression:
            return self.region(expression["region_ref"])
        if "ref" in expression:
            return self.values[expression["ref"]]
        if "cmp" in expression:
            compare = {"eq": operator.eq, "ne": operator.ne, "lt": operator.lt,
                       "le": operator.le, "gt": operator.gt, "ge": operator.ge}
            return compare[expression["cmp"]](self.eval(expression["left"]),
                                               self.eval(expression["right"]))
        if "op" in expression:
            args = [self.eval(item) for item in expression["args"]]
            operations = {"add": sum, "mul": math.prod, "min": min, "max": max,
                          "div": lambda xs: xs[0] / xs[1],
                          "pow": lambda xs: xs[0] ** xs[1],
                          "log": lambda xs: math.log(xs[0]),
                          "sub": lambda xs: xs[0] - xs[1]}
            return operations[expression["op"]](args)
        raise AssertionError("Unsupported native scope expression: %r" % expression)


class ComparisonScopeRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fo = read_profile(FO)
        cls.hoc = read_profile(HOC)
        cls.bl = read_profile(BL)
        cls.fo_comparisons = indexed(cls.fo, "comparisons", "comparison_id")
        cls.aliases = json.loads((ATLAS / "data/registry/aliases.json").read_text())
        cls.fo_rows = [FO_PREFIX + "c4", FO_PREFIX + "c_saturated_envelope_20261122",
                       FO_PREFIX + "c_remaining_gap_20261122"]

    def fo_membership(self, dimension, epsilon, constant=8, **overrides):
        values = {"d": dimension, "\\beta": 1, "\\Delta": 1,
                  "\\varepsilon": epsilon, "c": 0.25, "C": constant}
        values.update(overrides)
        reader = PredicateReader(self.fo, values)
        matches = [name for name in self.fo_rows
                   if reader.eval(self.fo_comparisons[name]["predicate"])]
        return reader, matches

    def test_fo_partition_routes_integer_dimensions_once(self):
        # Sample both sides of each precision/dimension crossover, including
        # dimensions far above the original source theorem's sufficient cap.
        reached = set()
        for epsilon in (0.25, 0.1, 0.03, 0.01):
            for constant in (2, 8, 100):
                high = constant * epsilon ** -2 * math.log(2 + 1 / epsilon)
                dimensions = {3, 4, 8, 32, 128, 512, 2048, 1000000,
                              max(3, math.floor(high)), max(3, math.ceil(high))}
                for dimension in dimensions:
                    with self.subTest(d=dimension, epsilon=epsilon, C=constant):
                        reader, matches = self.fo_membership(dimension, epsilon, constant)
                        self.assertTrue(reader.region(FO_PREFIX + "r7"))
                        self.assertEqual(len(matches), 1)
                        reached.update(matches)
                        research = self.fo_comparisons[self.fo_rows[2]]["research_target"]
                        self.assertEqual(reader.eval(research["predicate"]),
                                         matches == [self.fo_rows[2]])
        self.assertEqual(reached, set(self.fo_rows))

    def test_fo_closed_boundaries_are_not_research_targets(self):
        # An integer dimension exactly at the H boundary; C is synthetic.
        epsilon, dimension = 0.1, 1024
        constant = dimension / (epsilon ** -2 * math.log(2 + 1 / epsilon))
        self.assertEqual(constant * epsilon ** -2 * math.log(2 + 1 / epsilon), dimension)
        self.assertEqual(self.fo_membership(dimension, epsilon, constant)[1], [self.fo_rows[0]])
        self.assertNotIn(self.fo_rows[0], self.fo_membership(dimension - 1, epsilon, constant)[1])
        # Choose representable boundary cases so no comparison tolerance can
        # conceal an accidental strict/closed inequality in the native AST.
        exact_cases = 0
        for dimension in (32, 128, 512, 2048):
            q = dimension / math.log(2 + dimension)
            epsilon = math.sqrt(1 / q)
            if epsilon > 0.25 or epsilon ** -2 != q:
                continue
            exact_cases += 1
            with self.subTest(saturation_dimension=dimension):
                self.assertEqual(self.fo_membership(dimension, epsilon, 100)[1], [self.fo_rows[1]])
                self.assertEqual(self.fo_membership(dimension, epsilon * (1 - 1e-9), 100)[1],
                                 [self.fo_rows[2]])
                self.assertEqual(self.fo_membership(dimension, epsilon * (1 + 1e-9), 100)[1],
                                 [self.fo_rows[1]])
        self.assertGreater(exact_cases, 0)

    def test_fo_new_rows_preserve_normalized_source_window(self):
        for overrides in ({"\\beta": 2}, {"\\Delta": 2}, {"c": 0.01}):
            self.assertEqual(self.fo_membership(512, 0.1, **overrides)[1], [])
        self.assertEqual(self.fo_membership(2, 0.1, 100)[1], [])
        reader, _ = self.fo_membership(512, 0.1)
        self.assertTrue(reader.region(FO_PREFIX + "r4"))  # b5 guard is retained.
        ratio = self.fo_comparisons[self.fo_rows[2]]["bracket"]["ratio_or_gap"]
        self.assertNotIn("displayed upper", ratio)
        self.assertIn("\\frac", ratio)

    def test_fo_legacy_alias_routes_to_all_refined_rows(self):
        old_id = FO_PREFIX + "c5"
        self.assertNotIn(old_id, self.fo_comparisons)
        migration = next(item for item in self.aliases["comparison_migrations"]
                         if item["old_comparison_id"] == old_id)
        self.assertEqual(set(migration["new_comparison_ids"]), set(self.fo_rows))
        self.assertIsNone(migration["navigation_default_comparison_id"])
        legacy = "SO_FO_N01_L1_G_R_C_N01_cmp_mid_L1_G_R"
        alias = next(item for item in self.aliases["aliases"] if item["legacy_id"] == legacy)
        self.assertEqual(alias["kind"], "view")
        self.assertEqual(set(alias["comparison_ids"]), set(self.fo_rows))
        self.assertFalse(any(item["legacy_id"] == legacy
                             for item in self.aliases["comparison_aliases"]))

    def test_hoc_same_scope_has_one_current_stronger_envelope(self):
        current = indexed(self.hoc, "comparisons", "comparison_id")
        old_id, new_id = HOC_PREFIX + "c1", HOC_PREFIX + "c4"
        self.assertNotIn(old_id, current)
        history = next(item for item in self.hoc["provenance"]["comparison_history"]
                       if item["comparison"]["comparison_id"] == old_id)
        archived, updated = history["comparison"], current[new_id]
        self.assertEqual(archived["comparison_key"], updated["comparison_key"])
        self.assertEqual(archived["predicate"], updated["predicate"])
        self.assertEqual(sum(row["comparison_key"] == updated["comparison_key"]
                             for row in current.values()), 1)
        self.assertEqual(set(updated["bracket"]["upper_refs"]),
                         {HOC_PREFIX + "b1", HOC_PREFIX + "b6"})
        self.assertEqual(set(updated["bracket"]["envelopes"]["upper"]["claim_refs"]),
                         {HOC_PREFIX + "b1", HOC_PREFIX + "b6"})
        self.assertIn("\\min", updated["bracket"]["envelopes"]["upper"]["expression_latex"])
        self.assertEqual(updated["status"]["code"], "missing_lower")
        self.assertEqual(updated["bracket"]["lower_refs"], [])
        self.assertEqual(sum(row["status"]["code"] == "missing_lower" for row in current.values()), 1)
        self.assertEqual(self.hoc["summary_status"]["status_counts"]["missing_lower"], 1)

    def test_archived_comparisons_keep_their_identity_and_leave_active_rows(self):
        for profile in (self.fo, self.hoc):
            with self.subTest(profile=profile["setting_id"]):
                active = {row["comparison_id"] for row in profile["comparisons"]}
                for entry in profile["provenance"]["comparison_history"]:
                    record = entry["comparison"]
                    self.assertEqual(canonical_sha(record), entry["comparison_sha256"])
                    old_id = record["comparison_id"]
                    self.assertNotIn(old_id, active)
                    self.assertTrue(set(entry["superseded_by"]).issubset(active))
                    self.assertFalse(any(old_id in row["comparison_ids"] for row in profile["bracket_rows"]))
                    self.assertFalse(any(old_id in bound.get("selected_in_regimes", [])
                                         for bound in profile["bounds"]))

    def test_bl_preserves_eight_original_hashes_without_claiming_a_recovered_snapshot(self):
        proof = indexed(self.bl, "proofs")[BL_PROOF]
        self.assertEqual(tuple((item["pointer"], item["sha256"]) for item in proof["premises"]),
                         BL_ORIGINAL_PREMISES)
        lifecycle = proof["lifecycle"]
        self.assertEqual(lifecycle["state"], "historical")
        self.assertIs(lifecycle["eligible_for_current_bounds"], False)
        binding = lifecycle["premise_binding"]
        self.assertEqual(binding["mode"], "historical_unresolved")
        self.assertEqual(binding["verification_status"], "unresolved_snapshot")
        self.assertEqual(binding["first_observed"]["git_commit"],
                         "996c941748d9d2c998dfeadba41766d463357b1d")
        self.assertEqual(binding["first_observed"]["profile_sha256"],
                         "e7d304cc4e6f3035a9c31d64e8a4957d693bb7b502e107c35faf6f699f207d85")
        self.assertEqual(set(binding["unresolved_first_observed_pointers"]),
                         {"/common_specification", "/bounds/1", "/comparisons/0", "/regimes"})

    def test_historical_bl_support_cannot_certify_a_current_bound(self):
        evidence = indexed(self.bl, "evidence")
        proofs = indexed(self.bl, "proofs")
        self.assertEqual(evidence[BL_EVIDENCE]["proof_refs"], [BL_PROOF])
        active_bounds = [bound for bound in self.bl["bounds"]
                         if bound.get("included_in_bracket") or bound.get("eligible_for_bracket")]
        for bound in active_bounds:
            with self.subTest(bound=bound["id"]):
                evidence_ids = bound.get("evidence_refs", [])
                proof_ids = set(bound.get("proof_refs", []))
                proof_ids.update((bound.get("derivation") or {}).get("proof_refs", []))
                for evidence_id in evidence_ids:
                    proof_ids.update(evidence[evidence_id].get("proof_refs", []))
                self.assertNotIn(BL_EVIDENCE, evidence_ids)
                self.assertNotIn(BL_PROOF, proof_ids)
                for proof_id in proof_ids:
                    self.assertNotEqual(proofs[proof_id].get("lifecycle", {}).get("state"), "historical")


if __name__ == "__main__":
    unittest.main(verbosity=2)
