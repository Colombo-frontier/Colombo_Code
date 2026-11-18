# GD family calibration

Use this example to distinguish fixed-instance convergence from a family whose hard instance changes with budget or target accuracy. It is an optional calibration for [rate estimation](../SKILL.md), not a required stage of every Experiment.

## Model and analytic reference

For positive L,R and 0<a<=L, use

\[
f_a(x)=\tfrac a2x_1^2+\tfrac L2x_2^2,
\quad x_0=(R,0),\quad \eta=1/L.
\]

The actual smoothness is L, strong-convexity parameter is a, distance is R, initial gap is aR²/2, dimension is 2 and minimizer is zero. After N gradient queries,

\[
e_N(a)=\frac{aR^2}{2}(1-a/L)^{2N}.
\]

| Mode | Parameter path | Interpretation |
|---|---|---|
| fixed | Fixed a,L,R; vary N. | For 0<a<L, exponential error decay and logarithmic accuracy complexity. At a=L, GD reaches zero in one query. |
| budget_matched | Fixed L,R; a=L/(2N+1). | The maximum of this family's e_N(a) has leading order LR²/(4eN). A different instance is measured at each N. |
| epsilon_matched | Fixed L,R; a=4epsilon/R², with 0<a<L. | Initial gap is 2epsilon. The deterministic crossing is ceil(log(1/2)/(2 log(1-4epsilon/(LR²)))); its leading order is log(2)LR²/(8epsilon). |

Matched paths vary actual mu and initial gap. They are not experiments with a fixed positive strong-convexity parameter. All instances share the known minimizer zero, so this construction cannot establish a general Algorithm Class minimax Lower Bound. It calibrates the specified GD rule.

## Execute the example

The [script](../scripts/gd_family_calibration.py) uses only the Python standard library. Upload its installed path as an input file using the [protocol](../../../protocol.md):

```python
import runpy
path = "skills/estimate-epsilon-rate/scripts/gd_family_calibration.py"
module = runpy.run_path(INPUT_FILES[path])
module["run"](PARAMETERS, OUTPUT_DIR)
```

Supply PARAMETERS as a JSON object. Defaults are a small three-mode run:

```json
{"mode":"all","L":1,"R":1,"a":0.25,
 "budgets":[0,1,2,4,16,64],"epsilons":[0.1,0.05,0.025],"max_steps":10000}
```

mode can be all, fixed, budget_matched or epsilon_matched. budgets must be distinct increasing integers in [0,max_steps]; epsilons must be distinct positive numbers. Explicit invalid inputs raise an error, without silently changing the Setting. This small example limits max_steps to 100000 and each input list to 64 entries; adapt a copied script deliberately for larger work.

The fixed case runs to the largest requested budget and records all intervening iterates. Each budget-matched case runs its own instance for that budget. Each epsilon-matched case runs a predetermined budget chosen using the analytic pilot, capped by max_steps. The Algorithm receives only a gradient callable, initial point, step size and fixed budget. Offline evaluation then extracts the deterministic crossing; evaluator truth does not stop or tune the Algorithm.

## Read and interpret artifacts

- measurements.json contains actual GD iterates, errors and measured query counts, with realized parameters and case status. gradient_calls counts exactly one Oracle call per GD update; evaluator_calls is separate.
- analytic_reference.json contains formula values and predicted crossings, labelled analytic_formula. These values were not obtained by running GD.
- summary.json records configuration, total accounting, unmet targets and limitations. These statuses describe the example; the enclosing execution status still comes from the service receipt.

target_not_reached retains all measured outputs and an absent crossing; it does not replace the crossing with the cap. This deterministic known family permits analytic investigation of monotonicity, but floating-point failure or stagnation should not be advertised as general Oracle hardness.

Compare actual errors against the separate formula on safe finite scales. Local slopes are diagnostics; no tolerance or fit certifies an asymptotic theorem. If producing a plot, identify each mode and data source and use these preserved values. Do not relabel a long analytic curve as an actual rollout.

Reuse calibration only when code, measurement/Oracle rules and the numerical regime remain applicable. A changed implementation, evaluator or problematic scale needs a targeted check. Subsequent research may use different families and Algorithms; preserve their own admissibility and normalization evidence.
