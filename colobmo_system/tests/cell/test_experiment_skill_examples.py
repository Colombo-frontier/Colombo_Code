"""Execute the shipped Skill examples against independent mathematical references."""
from fractions import Fraction
import json
import math
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch


PROJECT = Path(__file__).resolve().parents[2]
SKILLS = PROJECT / "agents" / "experiment_cell" / "skills"
GD_SCRIPT = SKILLS / "estimate-epsilon-rate" / "scripts" / "gd_family_calibration.py"
QUADRATIC_SCRIPT = SKILLS / "probe-mechanism" / "scripts" / "quadratic_inequality_probe.py"


class ExperimentSkillExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gd = runpy.run_path(str(GD_SCRIPT))
        cls.quadratic = runpy.run_path(str(QUADRATIC_SCRIPT))

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".test-skill-example-", dir=PROJECT)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def read(self, directory, name):
        return json.loads((directory / name).read_text(encoding="utf-8"))

    def assert_close(self, actual, expected, scale=1):
        self.assertTrue(math.isclose(actual, float(expected), rel_tol=1e-10, abs_tol=1e-13 * scale),
                        (actual, expected))

    def test_gd_actual_and_analytic_outputs_match_independent_rational_reference(self):
        for index, (L, R, a) in enumerate([(Fraction(1), Fraction(1), Fraction(1, 4)),
                (Fraction(2), Fraction(3, 2), Fraction(3, 4)),
                (Fraction(5), Fraction(2), Fraction(5))]):
            directory = self.root / str(index)
            self.gd["run"]({"mode": "fixed", "L": float(L), "R": float(R),
                            "a": float(a), "budgets": [0, 1, 4, 16]}, directory)
            actual = self.read(directory, "measurements.json")["cases"][0]
            reference = self.read(directory, "analytic_reference.json")["cases"][0]
            self.assertEqual(actual["source"], "actual_gd_rollout")
            self.assertEqual(reference["source"], "analytic_formula")
            for row, analytic in zip(actual["measurements"], reference["values"]):
                n = row["N"]
                expected_x = R * (1 - a / L) ** n
                expected_error = a * expected_x ** 2 / 2
                self.assert_close(row["point"][0], expected_x, float(L * R ** 2))
                self.assertEqual(row["point"][1], 0)
                self.assert_close(row["error"], expected_error, float(L * R ** 2))
                self.assert_close(analytic["error"], expected_error, float(L * R ** 2))

    def test_gd_counts_actual_oracle_invocations_and_evaluator_separately(self):
        oracle = self.gd["CountedGradient"]
        original = oracle.__call__
        calls = []
        def counted(instance, point):
            calls.append(tuple(point))
            return original(instance, point)
        with patch.object(oracle, "__call__", counted):
            summary = self.gd["run"]({"budgets": [0, 1, 4], "epsilons": [0.1]}, self.root)
        cases = self.read(self.root, "measurements.json")["cases"]
        self.assertEqual(len(calls), summary["gradient_calls"])
        self.assertEqual(sum(c["budget"] for c in cases), len(calls))
        self.assertEqual(summary["evaluator_calls"], len(calls) + len(cases))
        for case in cases:
            self.assertEqual(case["gradient_calls"], case["budget"])
            self.assertEqual([r["oracle_calls"] for r in case["measurements"]], list(range(case["budget"] + 1)))

    def test_gd_iteration_uses_only_fixed_budget_and_gradient_callable(self):
        calls = []
        def gradient(point):
            calls.append(point)
            return (2 * point[0], 3 * point[1])
        points = list(self.gd["gd_iterates"](gradient, (1, 1), 0.25, 2))
        self.assertEqual(points, [(1, 1), (0.5, 0.25), (0.25, 0.0625)])
        self.assertEqual(calls, points[:-1])

    def test_budget_matched_paths_and_envelope_endpoints(self):
        budgets = [0, 1, 2, 10]
        self.gd["run"]({"mode": "budget_matched", "L": 2, "R": 3, "budgets": budgets}, self.root)
        cases = self.read(self.root, "measurements.json")["cases"]
        self.assertEqual(len(cases), len(budgets))
        for n, case in zip(budgets, cases):
            a = Fraction(2, 2 * n + 1)
            self.assert_close(case["parameters"]["mu"], a)
            self.assert_close(case["parameters"]["initial_gap"], a * 9 / 2)
            expected_error = a * 9 / 2 * (1 - a / 2) ** (2 * n)
            self.assert_close(case["measurements"][-1]["error"], expected_error, 18)
            self.assertEqual(case["budget"], n)

    def test_epsilon_crossings_from_rollouts_match_independent_exact_iteration(self):
        epsilons = [Fraction(1, 16), Fraction(1, 32), Fraction(1, 64)]
        self.gd["run"]({"mode": "epsilon_matched", "epsilons": [float(e) for e in epsilons]}, self.root)
        actual = self.read(self.root, "measurements.json")["cases"]
        references = self.read(self.root, "analytic_reference.json")["cases"]
        for epsilon, case, reference in zip(epsilons, actual, references):
            a = 4 * epsilon
            x, crossing = Fraction(1), 0
            while a * x * x / 2 > epsilon:
                x *= 1 - a
                crossing += 1
            self.assertEqual(case["first_crossing"], crossing)
            self.assertEqual(reference["predicted_crossing"], crossing)
            self.assertEqual(case["status"], "completed")
            self.assert_close(case["parameters"]["initial_gap"], 2 * epsilon)
            self.assertGreater(case["measurements"][crossing - 1]["error"], float(epsilon))
            self.assertLessEqual(case["measurements"][crossing]["error"], float(epsilon))

    def test_unreached_epsilon_retains_data_without_fabricating_a_crossing(self):
        summary = self.gd["run"]({"mode": "epsilon_matched", "epsilons": [1e-6], "max_steps": 3}, self.root)
        case = self.read(self.root, "measurements.json")["cases"][0]
        self.assertEqual(case["status"], "target_not_reached")
        self.assertIsNone(case["first_crossing"])
        self.assertEqual(case["gradient_calls"], 3)
        self.assertEqual(len(case["measurements"]), 4)
        self.assertEqual(summary["target_not_reached"], [case["case_id"]])

    def test_gd_invalid_inputs_do_not_create_artifacts(self):
        bad = [{"L": True}, {"L": float("nan")}, {"L": -1}, {"R": 0}, {"a": 2},
               {"budgets": [2, 1]}, {"budgets": [1, 1]}, {"budgets": [False]},
               {"epsilons": [0.25]}, {"epsilons": [0]}, {"epsilons": [0.1, 0.1]},
               {"mode": "unknown"}, {"max_steps": True}, {"L": 1e-320}, {"unknown": 1}]
        for index, parameters in enumerate(bad):
            directory = self.root / str(index)
            with self.subTest(parameters=parameters), self.assertRaises(ValueError):
                self.gd["run"](parameters, directory)
            self.assertFalse(directory.exists())

    def check_exact_witness(self, certificate):
        config, witness = certificate["configuration"], certificate["witness"]
        h = list(map(Fraction, config["diagonal"]))
        b = list(map(Fraction, config["b"]))
        x = list(map(Fraction, witness["point"]))
        c, L, C = map(Fraction, (config["c"], config["L"], config["C"]))
        optimum = [bj / hj for bj, hj in zip(b, h)]
        expected_star = c - sum(bj * bj / (2 * hj) for bj, hj in zip(b, h))
        expected_gap = sum(hj * (xj - zj) ** 2 / 2 for hj, xj, zj in zip(h, x, optimum))
        gradient = [hj * xj - bj for hj, xj, bj in zip(h, x, b)]
        squared = sum(g * g for g in gradient)
        residual = squared - C * L * expected_gap
        self.assertTrue(all(0 < hj <= L for hj in h))
        self.assertEqual(list(map(Fraction, witness["optimum"])), optimum)
        self.assertEqual(Fraction(witness["f_star"]), expected_star)
        self.assertEqual(Fraction(witness["gap"]), expected_gap)
        self.assertEqual(Fraction(witness["f_value"]), expected_gap + expected_star)
        self.assertEqual(list(map(Fraction, witness["gradient"])), gradient)
        self.assertEqual(Fraction(witness["gradient_norm_squared"]), squared)
        self.assertEqual(Fraction(witness["residual_lhs_minus_rhs"]), residual)
        self.assertEqual(witness["violation"], residual > 0)
        return residual

    def test_quadratic_default_finds_exact_rational_violation(self):
        summary = self.quadratic["run"]({}, self.root)
        certificate = self.read(self.root, "exact_witness.json")
        residual = self.check_exact_witness(certificate)
        self.assertGreater(residual, 0)
        self.assertEqual(Fraction(certificate["witness"]["ratio"]), 2)
        self.assertEqual(summary["scientific_status"], "counterexample_candidate")
        self.assertEqual(summary["search_points"], 25)
        self.assertEqual(self.read(self.root, "search_measurements.json")["source"], "float_grid_search")
        self.assertEqual(certificate["source"], "exact_rational_computation")

    def test_quadratic_positive_control_does_not_claim_violation_or_universal_proof(self):
        summary = self.quadratic["run"]({"C": "2"}, self.root)
        certificate = self.read(self.root, "exact_witness.json")
        self.assertEqual(self.check_exact_witness(certificate), 0)
        self.assertFalse(summary["exact_violation"])
        self.assertEqual(summary["scientific_status"], "no_violation_at_candidate")

    def test_quadratic_fractional_linear_term_and_additive_shift(self):
        self.quadratic["run"]({"diagonal": ["2/3", "5/4"], "b": ["1/7", "-2/3"],
                              "c": "-5/9", "L": "3/2", "shift": "17/11"}, self.root)
        certificate = self.read(self.root, "exact_witness.json")
        self.check_exact_witness(certificate)
        original, shifted = certificate["witness"], certificate["shifted_witness"]
        self.assertEqual(Fraction(shifted["f_star"]) - Fraction(original["f_star"]), Fraction(17, 11))
        self.assertEqual(shifted["gap"], original["gap"])
        self.assertEqual(shifted["gradient"], original["gradient"])
        self.assertEqual(shifted["residual_lhs_minus_rhs"], original["residual_lhs_minus_rhs"])

    def test_quadratic_invalid_or_unrepresentable_parameters_leave_no_artifacts(self):
        bad = [{"diagonal": ["0"]}, {"diagonal": ["-1"]}, {"diagonal": ["1"] * 4},
               {"b": ["0"]}, {"L": "1"}, {"C": "NaN"}, {"C": True},
               {"grid": ["0", "0"]}, {"grid": ["0"]}, {"c": "1/0"},
               {"diagonal": ["1e-400"]}, {"diagonal": ["1e-200"], "L": "1e-200"},
               {"unknown": "field"}]
        for index, parameters in enumerate(bad):
            directory = self.root / str(index)
            with self.subTest(parameters=parameters), self.assertRaises(ValueError):
                self.quadratic["run"](parameters, directory)
            self.assertFalse(directory.exists())

    def test_self_contained_scripts_work_under_an_uploaded_bin_filename(self):
        for index, script in enumerate((GD_SCRIPT, QUADRATIC_SCRIPT)):
            uploaded = self.root / f"file-{index}.bin"
            uploaded.write_bytes(script.read_bytes())
            directory = self.root / f"outputs-{index}"
            summary = runpy.run_path(str(uploaded))["run"]({}, directory)
            self.assertEqual(summary, self.read(directory, "summary.json"))
            self.assertEqual({p.name for p in directory.iterdir()}, set(summary["artifacts"]))


if __name__ == "__main__":
    unittest.main()
