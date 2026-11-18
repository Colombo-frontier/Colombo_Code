---
name: estimate-epsilon-rate
description: Estimate Oracle-complexity rates or parameter dependence in epsilon, budget, dimension, condition number or noise; compare fixed Algorithms, search Algorithms or investigate empirical minimax behavior under a fixed Setting.
---

# Rate and parameter dependence

Use the [protocol](../../protocol.md) for execution and evidence. Choose methods for the assigned question; the sections below are decision criteria, not compulsory stages.

## Define the estimand

Distinguish fixed Algorithm evaluation, Algorithm search on a specified Function Family, and empirical minimax competition. State Metric, risk, Output, Resource and normalization using the fixed Setting. Each Algorithm candidate includes its full public tuning rule; offline discovery may use evaluation truth, but the deployed rule cannot read a hidden instance, its optimum or future random seeds.

For fixed-budget expected error, first estimate E[error(A,f,N)] for a fixed instance, then aggregate in the specified sup_f / inf_A order. Choose a hard instance against the Algorithm rule/distribution before the private randomness is realized. Do not substitute worst seed, instance average or per-instance best hyperparameters. Restricting both pools generally produces neither a certified Upper nor a certified Lower Bound on the full minimax problem.

## Specify the parameter path

Separate public model budgets, realized instance parameters, internal construction parameters and Algorithm/numerical parameters. Identify fixed, scanned and linked quantities. Axes may be epsilon, N, dimension d, condition number kappa, noise sigma or a declared joint path. A joint exponent is not the independent exponent of one varying parameter.

Distinguish a fixed instance from a budget-matched or epsilon-matched family. The Function Family and its public constraints stay fixed; a different legal hard instance may be selected at each scale. Recheck smoothness, convexity, domain, initial gap/distance, noise and dimension requirements after matching. State whether evidence is analytic certification or a limited numerical check.

Normalize epsilon by a declared scale. For kappa, define kappa=L/mu and say whether L, mu, gap or distance stays fixed. For d, check norm, spectral scale and total noise normalization. Detect initial gap already below epsilon, finite-dimension saturation, invalid chain truncation and evaluator/numerical floors.

For a transparent calibration of these distinctions, read [GD family calibration](references/gd-family-calibration.md) and use its [self-contained script](scripts/gd_family_calibration.py) if relevant. It calibrates a particular GD rule, not general minimax hardness.

## Construct, calibrate and search as needed

Start small. Calibrate a new implementation, changed Oracle/evaluator/counting interface, anomalous output or a new numerical regime. Reuse applicable recorded calibration. Choose scales that distinguish the candidate explanations; no fixed grid or repetition count is required.

Keep the Algorithm interface separate from the evaluator. Count initialization, mini-batches, finite differences, line search and any Algorithm verification queries. Report a Resource vector when the Setting uses one. Evaluator and search compute are separate costs, not free Algorithm capabilities.

A fixed Algorithm Task can concentrate on Hard Instance search. An Algorithm search can use a fixed challenge pool. For empirical minimax competition, compare complete rules on a common pool, retain witnesses, and choose whether changing the Algorithm or construction is most informative. The hardest found instance is a witness, not a demonstrated supremum.

Freeze important searched/tuned candidates before proportionate independent checks. New instances, scales, independent calculations or fresh seeds may help; deterministic exact cases do not need artificial random repeats. If validation changes the candidate, acknowledge it as discovery data and obtain fresh evidence for the revised claim.

## Measure and invert the correct risk

Usually measure error-at-budget before inverting for T(epsilon). For expected error, take the arithmetic mean at the same budget on the same fixed instance, then take logs for analysis. Mean log error, mean first-hitting time, fixed-budget expected-error complexity and a high-probability success budget are different estimands.

Keep crossing data on both sides and the unresolved interval when uncertainty spans epsilon. Last-iterate risk can be nonmonotone. Evaluator-chosen best iterate or a monotone envelope needs a legal Output rule; failure at one budget does not exclude all smaller budgets. High-probability targets fix delta; expected-cost targets require the cost distribution and their own convention. Tail behavior limits what a small sample can say about an expectation.

Preserve unmet targets, censored observations, timeout, divergence, invalid instance and numerical failure separately. Never treat a cap as an exact crossing or fit only successful trajectories. Recover missing outcomes, use justified bounds, or mark the risk unresolved. Execution failure is not an Oracle-complexity Lower Bound. Evaluator error must be small enough to distinguish the proposed effect; improving a plot does not resolve an inaccurate reference optimum.

## Interpret and hand off

Compare plausible power laws, logarithmic dependence, log corrections, additive terms, crossovers and floors. Risk(N) ~ N^(-q) corresponds to T(epsilon) ~ epsilon^(-1/q) only for the same risk/regime; exponential error decay usually means logarithmic accuracy complexity.

Inspect local slopes, fitting-window sensitivity, residuals, normalized curves and predictions at scales not used for fitting. State the axis and uncertainty. Sampling intervals do not cover unsearched Algorithms or Hard Instances. An apparent conflict with a theorem first calls for checking scope, Oracle, Resource, normalization, dimensions and implementation.

Report the strongest scoped empirical finding, remaining explanations and one concrete next Proof or Experiment question. Include the actual parameter path, complete Algorithm rules, constructions, admissibility evidence, raw measurements and failure statuses. Reliable non-identifiability is a valid outcome; a stable exponent is not mandatory.
