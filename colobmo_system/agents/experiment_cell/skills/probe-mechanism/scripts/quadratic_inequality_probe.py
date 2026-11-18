"""Numerical search and exact rational witness for a quadratic gap inequality.

Diagonal positive-definite H, dimension 1..3; stdlib only. Hosted entrypoint:
runpy.run_path(INPUT_FILES[path])["run"](PARAMETERS, OUTPUT_DIR).
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path


def _rational(value, name):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError(f"{name} must be a finite rational number or rational string")
    try:
        result = Fraction(str(value))
        numeric = float(result)
        finite = math.isfinite(numeric) and (result == 0 or numeric != 0)
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite representable rational") from exc
    if not finite:
        raise ValueError(f"{name} must be finite and nonzero values must not underflow")
    return result


def _config(parameters):
    if not isinstance(parameters, dict):
        raise ValueError("parameters must be an object")
    allowed = {"diagonal", "b", "c", "L", "C", "grid", "shift"}
    if set(parameters) - allowed:
        raise ValueError(f"Unknown parameters: {sorted(set(parameters) - allowed)}")
    diagonal = parameters.get("diagonal", ["1", "2"])
    if not isinstance(diagonal, list) or not 1 <= len(diagonal) <= 3:
        raise ValueError("diagonal must have dimension 1..3")
    diagonal = [_rational(x, "diagonal") for x in diagonal]
    if any(x <= 0 for x in diagonal):
        raise ValueError("H must be positive definite: all diagonal entries > 0")
    b = parameters.get("b", ["0"] * len(diagonal))
    if not isinstance(b, list) or len(b) != len(diagonal):
        raise ValueError("b must have the same dimension as diagonal")
    b = [_rational(x, "b") for x in b]
    L = _rational(parameters.get("L", str(max(diagonal))), "L")
    if L < max(diagonal):
        raise ValueError("L must bound every eigenvalue of H")
    grid = parameters.get("grid", ["-2", "-1", "0", "1", "2"])
    if not isinstance(grid, list) or not 2 <= len(grid) <= 33:
        raise ValueError("grid must contain 2..33 distinct rational values")
    grid = [_rational(x, "grid") for x in grid]
    if len(set(grid)) != len(grid):
        raise ValueError("grid values must be distinct")
    return {"diagonal": diagonal, "b": b, "L": L, "grid": grid,
            "c": _rational(parameters.get("c", "0"), "c"),
            "C": _rational(parameters.get("C", "1"), "C"),
            "shift": _rational(parameters.get("shift", "7"), "shift")}


def _exact(config, point, c=None):
    h, b = config["diagonal"], config["b"]
    c = config["c"] if c is None else c
    optimum = [bj / hj for hj, bj in zip(h, b)]
    f_star = c - sum((bj * bj / (2 * hj) for hj, bj in zip(h, b)), Fraction(0))
    f_value = sum((hj * x * x / 2 - bj * x for hj, bj, x in zip(h, b, point)), c)
    gradient = [hj * x - bj for hj, bj, x in zip(h, b, point)]
    gap = f_value - f_star
    norm_squared = sum((g * g for g in gradient), Fraction(0))
    residual = norm_squared - config["C"] * config["L"] * gap
    return {"point": [str(x) for x in point], "optimum": [str(x) for x in optimum],
            "f_value": str(f_value), "f_star": str(f_star), "gap": str(gap),
            "gradient": [str(x) for x in gradient], "gradient_norm_squared": str(norm_squared),
            "residual_lhs_minus_rhs": str(residual), "violation": residual > 0,
            "ratio": str(norm_squared / (config["L"] * gap)) if gap > 0 else None}


def run(parameters, output_dir):
    """Search a finite numerical grid, simplify its direction, then certify a point."""
    config = _config(parameters)
    h, b = config["diagonal"], config["b"]
    optimum = [bj / hj for hj, bj in zip(h, b)]
    measurements, candidates = [], []
    for point in itertools.product(config["grid"], repeat=len(h)):
        # The centered gap avoids cancellation; this is still a float search.
        delta = [float(x - z) for x, z in zip(point, optimum)]
        try:
            gap = sum(float(hj) * dx * dx / 2 for hj, dx in zip(h, delta))
            norm_squared = sum((float(hj) * dx) ** 2 for hj, dx in zip(h, delta))
        except OverflowError as exc:
            raise ValueError("Numerical search overflow; choose representable scales") from exc
        if not math.isfinite(gap) or not math.isfinite(norm_squared):
            raise ValueError("Numerical search overflow; choose representable scales")
        if gap == 0 and any(x != z for x, z in zip(point, optimum)):
            raise ValueError("Numerical gap underflow; choose representable scales")
        denominator = float(config["L"]) * gap
        if gap > 0 and (denominator == 0 or not math.isfinite(denominator)):
            raise ValueError("Numerical ratio denominator is not representable")
        ratio = norm_squared / denominator if gap > 0 else None
        if ratio is not None and not math.isfinite(ratio):
            raise ValueError("Nonfinite numerical ratio; choose representable scales")
        measurements.append({"point": [str(x) for x in point], "source": "float_grid_search",
                             "gap": gap, "gradient_norm_squared": norm_squared, "ratio": ratio})
        if ratio is not None:
            candidates.append((ratio, -sum(x != z for x, z in zip(point, optimum)), point))
    if not candidates:
        raise ValueError("No numerically resolved nonoptimal grid point")
    _, _, candidate = max(candidates)
    active = [index for index, (x, z) in enumerate(zip(candidate, optimum)) if x != z]
    direction = max(active, key=lambda index: h[index])
    simplified = list(optimum)
    simplified[direction] += 1 if candidate[direction] > optimum[direction] else -1
    witness = _exact(config, simplified)
    shifted = _exact(config, simplified, config["c"] + config["shift"])
    encoded_config = {name: [str(x) for x in value] if isinstance(value, list) else str(value)
                      for name, value in config.items()}
    certificate = {"schema_version": 1, "source": "exact_rational_computation",
        "configuration": encoded_config, "search_candidate": _exact(config, candidate),
        "simplification": "Retain a strongest active diagonal direction and set its displacement to +/-1.",
        "assumptions": {"positive_definite": all(x > 0 for x in h),
                        "smoothness_at_most_L": max(h) <= config["L"], "domain": "R^d"},
        "witness": witness, "shifted_witness": shifted,
        "additive_shift_check": {"shift": str(config["shift"]),
            "f_star_change": str(Fraction(shifted["f_star"]) - Fraction(witness["f_star"])),
            "gap_unchanged": shifted["gap"] == witness["gap"],
            "residual_unchanged": shifted["residual_lhs_minus_rhs"] == witness["residual_lhs_minus_rhs"]},
        "scope": "Exact arithmetic checks this explicit candidate, not every admissible function.",
        "proof_handoff": "Verify the stated assumptions and exact residual for this witness; any universal statement requires its own argument."}
    summary = {"schema_version": 1, "example": "quadratic_inequality_probe",
        "scientific_status": "counterexample_candidate" if witness["violation"] else "no_violation_at_candidate",
        "search_points": len(measurements), "exact_violation": witness["violation"],
        "exact_residual": witness["residual_lhs_minus_rhs"],
        "accounting": "Research search/evaluator computation; no Algorithm Oracle-complexity claim.",
        "limitations": ["Finite diagonal-quadratic search; not a universal inequality proof.",
                        "Mathematical adoption requires the existing Proof review flow."],
        "artifacts": ["search_measurements.json", "exact_witness.json", "summary.json"]}
    outputs = {"search_measurements.json": {"source": "float_grid_search", "measurements": measurements},
               "exact_witness.json": certificate, "summary.json": summary}
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
    except (ValueError, TypeError, OverflowError) as exc:
        parser.error(str(exc))
