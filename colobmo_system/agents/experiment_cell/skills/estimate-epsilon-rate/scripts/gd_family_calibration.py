"""Counted GD rollouts and separately labelled analytic references; stdlib only.

Hosted use: runpy.run_path(INPUT_FILES[path])["run"](PARAMETERS, OUTPUT_DIR).
Local development: python script.py --parameters '{...}' --output-dir directory
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def _positive(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite positive number")
    try:
        number = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite positive number") from exc
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{name} must be a finite positive number")
    return number


def _config(parameters):
    if not isinstance(parameters, dict):
        raise ValueError("parameters must be an object")
    allowed = {"mode", "L", "R", "a", "budgets", "epsilons", "max_steps"}
    if set(parameters) - allowed:
        raise ValueError(f"Unknown parameters: {sorted(set(parameters) - allowed)}")
    mode = parameters.get("mode", "all")
    if mode not in ("all", "fixed", "budget_matched", "epsilon_matched"):
        raise ValueError("mode must be all, fixed, budget_matched or epsilon_matched")
    L, R = _positive(parameters.get("L", 1), "L"), _positive(parameters.get("R", 1), "R")
    scale = L * R * R
    if not math.isfinite(scale) or scale <= 0 or not math.isfinite(R * R) or R * R == 0:
        raise ValueError("L*R^2 and R^2 must be representable positive finite numbers")
    if not math.isfinite(1 / L):
        raise ValueError("The GD step size 1/L must be representable")
    a = _positive(parameters.get("a", L / 4), "a")
    if a > L or a / L == 0:
        raise ValueError("a must satisfy 0 < a <= L with representable a/L")
    max_steps = parameters.get("max_steps", 10000)
    if type(max_steps) is not int or not 1 <= max_steps <= 100000:
        raise ValueError("max_steps must be an integer in [1, 100000] for this example")
    budgets = parameters.get("budgets", [n for n in [0, 1, 2, 4, 16, 64] if n <= max_steps])
    if (not isinstance(budgets, list) or not budgets or len(budgets) > 64
            or any(type(n) is not int or n < 0 or n > max_steps for n in budgets)
            or budgets != sorted(set(budgets))):
        raise ValueError("budgets must be 1..64 distinct increasing integers in [0, max_steps]")
    epsilons = parameters.get("epsilons", [scale / 10, scale / 20, scale / 40])
    if not isinstance(epsilons, list) or not epsilons or len(epsilons) > 64:
        raise ValueError("epsilons must be a nonempty list of at most 64 numbers")
    epsilons = [_positive(e, "epsilon") for e in epsilons]
    if len(set(epsilons)) != len(epsilons):
        raise ValueError("epsilons must be distinct")
    if mode in ("all", "epsilon_matched"):
        for epsilon in epsilons:
            matched_a = 4 * (epsilon / (R * R))
            if not 0 < matched_a < L or matched_a / L == 0:
                raise ValueError("epsilon matching requires representable 0 < 4*epsilon/R^2 < L")
    return {"mode": mode, "L": L, "R": R, "a": a, "budgets": budgets,
            "epsilons": epsilons, "max_steps": max_steps}


class CountedGradient:
    """Only the gradient callable is passed to the GD iteration."""

    def __init__(self, a, L):
        self._a, self._L, self.calls = a, L, 0

    def __call__(self, point):
        self.calls += 1
        return self._a * point[0], self._L * point[1]


def gd_iterates(gradient, initial_point, step_size, budget):
    """Fixed-budget GD; no optimum, gap, epsilon or evaluator is accessible."""
    point = tuple(initial_point)
    yield point
    for _ in range(budget):
        grad = gradient(point)
        point = tuple(x - step_size * g for x, g in zip(point, grad))
        yield point


def _reference(a, L, R, budget):
    initial_gap = (a / 2) * R * R
    if budget == 0:
        return initial_gap
    if a == L:
        return 0.0
    return initial_gap * math.exp(2 * budget * math.log1p(-a / L))


def _case(case_id, mode, a, config, budget, epsilon=None, predicted_crossing=None):
    L, R = config["L"], config["R"]
    oracle = CountedGradient(a, L)
    actual, analytic = [], []
    first_crossing = None
    for n, point in enumerate(gd_iterates(oracle, (R, 0), 1 / L, budget)):
        error = (a / 2) * point[0] ** 2 + (L / 2) * point[1] ** 2
        if not math.isfinite(error) or any(not math.isfinite(x) for x in point):
            raise ValueError("Numerical overflow in rollout; choose representable scales")
        actual.append({"N": n, "oracle_calls": oracle.calls, "point": list(point),
                       "error": error, "status": "measured"})
        analytic.append({"N": n, "error": _reference(a, L, R, n), "source": "analytic_formula"})
        if epsilon is not None and first_crossing is None and error <= epsilon:
            first_crossing = n
    parameters = {"L": L, "mu": a, "R": R, "dimension": 2,
                  "initial_gap": (a / 2) * R * R, "step_size": 1 / L}
    status = "completed" if epsilon is None or first_crossing is not None else "target_not_reached"
    measured = {"case_id": case_id, "mode": mode, "source": "actual_gd_rollout",
                "parameters": parameters, "budget": budget, "epsilon": epsilon,
                "status": status, "gradient_calls": oracle.calls,
                "evaluator_calls": len(actual), "first_crossing": first_crossing,
                "measurements": actual}
    reference = {"case_id": case_id, "mode": mode, "source": "analytic_formula",
                 "parameters": parameters, "predicted_crossing": predicted_crossing,
                 "values": analytic}
    return measured, reference


def run(parameters, output_dir):
    """Execute validated small examples; outputs never label formulas as rollouts."""
    config = _config(parameters)
    L, R, mode = config["L"], config["R"], config["mode"]
    measured, references = [], []
    jobs = []
    if mode in ("all", "fixed"):
        jobs.append(("fixed-0", "fixed", config["a"], max(config["budgets"]), None, None))
    if mode in ("all", "budget_matched"):
        for n in config["budgets"]:
            jobs.append((f"budget-{n}", "budget_matched", L / (2 * n + 1), n, None, None))
    if mode in ("all", "epsilon_matched"):
        for index, epsilon in enumerate(config["epsilons"]):
            a = 4 * (epsilon / (R * R))
            crossing_value = math.log(0.5) / (2 * math.log1p(-a / L))
            if not math.isfinite(crossing_value):
                raise ValueError("Analytic crossing exceeds this example's numerical range")
            crossing = math.ceil(crossing_value)
            # This analytic pilot chooses experiment budgets, never Algorithm feedback.
            jobs.append((f"epsilon-{index}", "epsilon_matched", a,
                         min(crossing + 2, config["max_steps"]), epsilon, crossing))
    for case_id, case_mode, a, budget, epsilon, crossing in jobs:
        actual, reference = _case(case_id, case_mode, a, config, budget, epsilon, crossing)
        measured.append(actual)
        references.append(reference)
    summary = {"schema_version": 1, "example": "gd_family_calibration", "configuration": config,
        "scientific_status": "calibration_observations", "case_count": len(measured),
        "gradient_calls": sum(case["gradient_calls"] for case in measured),
        "evaluator_calls": sum(case["evaluator_calls"] for case in measured),
        "target_not_reached": [case["case_id"] for case in measured if case["status"] == "target_not_reached"],
        "measurement_rule": "Fixed-budget GD outputs; deterministic crossing extracted after execution.",
        "limitations": ["Specific GD rule only; all instances share the minimizer zero.",
                        "Matched paths vary actual mu and initial gap; not a fixed-positive-mu experiment.",
                        "Float arithmetic and finite scales do not certify a minimax bound."],
        "artifacts": ["measurements.json", "analytic_reference.json", "summary.json"]}
    outputs = {"measurements.json": {"source": "actual_gd_rollout", "cases": measured},
               "analytic_reference.json": {"source": "analytic_formula", "cases": references},
               "summary.json": summary}
    encoded = {name: json.dumps(value, indent=2, allow_nan=False) + "\n" for name, value in outputs.items()}
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    for name, text in encoded.items():
        (target / name).write_text(text, encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parameters", default="{}", help="JSON object")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(run(json.loads(args.parameters), args.output_dir), indent=2))
    except (ValueError, TypeError) as exc:
        parser.error(str(exc))
