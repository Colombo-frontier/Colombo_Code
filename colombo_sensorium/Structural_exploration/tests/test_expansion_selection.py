"""Discovery budgets and recall boundaries, without scripted mathematical judgments."""
from copy import deepcopy
import json
import unittest

from oracle_atlas.expansion.neighborhood import build_neighborhood
from oracle_atlas.expansion.selection import select_opportunities


def row(sid, task=None, oracle="value", unknown=False):
    facts = [{"axis": "ORACLE", "concept_id": f"ORACLE:operation:{oracle}", "status": "known"}]
    if task:
        facts.append({"axis": "TASK", "concept_id": f"TASK:task_family:{task}", "status": "known"})
    return {"setting_id": sid, "title": sid, "profile_version": f"v-{sid}", "tag_facts": facts,
            "unknown_axes": ["TASK"] if unknown or not task else [], "diagnostics": [], "task_text": "Compact task description"}


class AtlasStub:
    def __init__(self, rows):
        self.rows = rows
        self.read_count = 0

    def catalog(self):
        return deepcopy(self.rows)

    def version(self, setting_id=None):
        return "inventory-v1" if setting_id is None else "v-" + setting_id

    def vocabulary(self):
        return {}

    def read(self, *_args, **_kwargs):
        self.read_count += 1
        raise AssertionError("Neighborhood creation must not load all profile bodies")


def opportunity(oid, seed="A", operator="oracle_transfer", score=50, **changes):
    result = {"opportunity_id": oid, "title": oid, "seed_setting_ids": [seed], "neighbor_setting_ids": [],
              "operators": [operator], "changed_axes": ["ORACLE"], "target_task_ids": ["single_objective"],
              "mutation_steps": 1, "transformation": "Inspect an explicitly specified information change.",
              "selection_reason": "Planner supplied reason", "expected_value": "To be reviewed",
              "transfer_leads": [], "risks": [], "priority_score": score}
    result.update(changes)
    return result


class NeighborhoodTests(unittest.TestCase):
    def test_unknown_is_retained_and_identity_scope_is_global(self):
        atlas = AtlasStub([row("A", "single_objective"), row("B", "bilevel"), row("C", unknown=True)])
        out = build_neighborhood(atlas, {"source_task_ids": ["single_objective"], "max_seeds": 8, "max_neighbors_per_seed": 2})
        self.assertEqual({x["setting_id"] for x in out["seeds"]}, {"A", "C"})
        self.assertEqual(out["coverage"]["unknown_scope_retained"], 1)
        self.assertEqual(out["coverage"]["identity_search_scope"], "entire_current_atlas")
        self.assertEqual(atlas.read_count, 0)
        self.assertIn("B", [x["setting_id"] for x in out["seeds"][0]["neighbors"]])
        json.dumps(out)

    def test_rotates_seeds_and_keeps_bounded_navigation(self):
        atlas = AtlasStub([row("A", "single_objective"), row("B", "bilevel"), row("C", "single_objective", "gradient")])
        request = {"max_seeds": 2, "max_neighbors_per_seed": 1}
        first = build_neighborhood(atlas, request)
        second = build_neighborhood(atlas, request, [{"seeds": first["seeds"]}])
        fresh = {"A", "B", "C"} - {s["setting_id"] for s in first["seeds"]}
        self.assertIn(second["seeds"][0]["setting_id"], fresh)
        self.assertTrue(all(len(s["neighbors"]) == 1 for s in second["seeds"]))
        self.assertEqual(second["coverage"]["deferred_seed_count"], 1)
        self.assertFalse(second["coverage"]["discovery_complete"])

    def test_explicit_missing_and_conflicting_seeds_are_visible(self):
        atlas = AtlasStub([row("A", "single_objective"), row("B", "bilevel")])
        with self.assertRaisesRegex(ValueError, "absent"):
            build_neighborhood(atlas, {"seed_setting_ids": ["missing"]})
        out = build_neighborhood(atlas, {"seed_setting_ids": ["B"], "source_task_ids": ["single_objective"]})
        self.assertEqual(out["seeds"], [])
        self.assertEqual(out["coverage"]["explicit_seed_scope_conflicts"], ["B"])

    def test_navigation_does_not_claim_simulation_or_equivalence(self):
        out = build_neighborhood(AtlasStub([row("A", "single_objective"), row("B", "single_objective")]), {"max_seeds": 1})
        self.assertEqual(out["seeds"][0]["neighbors"][0]["relation_status"], "unverified_navigation_only")


class SelectionTests(unittest.TestCase):
    def test_bounded_diversity_uses_llm_scores_without_mutating_plan(self):
        plan = {"opportunities": [opportunity("a", score=90), opportunity("b", score=80),
                                   opportunity("c", seed="B", operator="model_transfer", score=70)]}
        before = deepcopy(plan)
        result = select_opportunities(plan, {"max_candidates": 2, "max_per_seed": 1, "max_per_operator": 1})
        self.assertEqual([x["opportunity_id"] for x in result["selected"]], ["a", "c"])
        self.assertEqual(result["deferred"][0]["opportunity_id"], "b")
        self.assertEqual(plan, before)
        result["selected"][0]["title"] = "Changed"
        self.assertEqual(plan, before)

    def test_scope_and_steps_are_enforced_before_research(self):
        ops = [opportunity("outside_axis", changed_axes=["MODEL"]),
               opportunity("outside_task", target_task_ids=["bilevel"]),
               opportunity("deep", mutation_steps=2), opportunity("valid")]
        result = select_opportunities({"opportunities": ops}, {"allowed_axes": ["ORACLE"],
            "allowed_operators": ["oracle_transfer"], "target_task_ids": ["single_objective"], "max_mutation_steps": 1})
        self.assertEqual([x["opportunity_id"] for x in result["selected"]], ["valid"])
        self.assertEqual(len(result["deferred"]), 3)

    def test_duplicate_and_oversized_plans_require_protocol_repair(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            select_opportunities({"opportunities": [opportunity("same"), opportunity("same")]}, {})
        with self.assertRaisesRegex(ValueError, "max_opportunities"):
            select_opportunities({"opportunities": [opportunity("one"), opportunity("two")]}, {"max_opportunities": 1})

    def test_all_participating_seeds_and_operators_consume_quota(self):
        ops = [opportunity("joint", seed_setting_ids=["A", "B"], operators=["oracle_transfer", "model_transfer"], score=99),
               opportunity("blocked_seed", seed="B", operator="other", score=90),
               opportunity("blocked_operator", seed="C", operator="model_transfer", score=80)]
        result = select_opportunities({"opportunities": ops}, {"max_per_seed": 1, "max_per_operator": 1})
        self.assertEqual([x["opportunity_id"] for x in result["selected"]], ["joint"])
        self.assertEqual(len(result["deferred"]), 2)


if __name__ == "__main__":
    unittest.main()
