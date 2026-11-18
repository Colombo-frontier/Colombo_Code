---
name: probe-mechanism
description: Investigate optimization proof bottlenecks through intermediate quantities, inequality violations, candidate constructions or Oracle-information probes, producing scoped evidence and a concrete next Proof question.
---

# Probe a mechanism

Use the [protocol](../../protocol.md) for execution and submission. Start from the mathematical bottleneck rather than forcing a rate fit. Define the object, variable domain, assumptions, quantifiers, measured quantity and the decision the result should affect. A single useful question suffices; competing hypotheses need not be invented.

## Simplify before computing

Check additive shifts, scaling, homogeneity, symmetry and degeneracies. Absolute f* has no intrinsic scale without an additive anchor such as f(x_ref)=0; an optimality gap may be the meaningful target. Do not silently add the anchor to the Setting.

Choose an appropriate analytic reduction, symbolic calculation, finite enumeration, numerical search or exact/interval check. A local solver's output is not automatically the true optimum. Feasible primal values and valid lower bounds can bracket f*; propagate the bracket to gap uncertainty. When evaluator uncertainty obscures the effect, improve it before collecting more misleading measurements.

## Search for informative structure

For an inequality, write a violation objective such as F-C*G, or a ratio only where its denominator is valid. Preserve the original constraints and inspect boundaries, degeneracy, dimension changes and small parameters. Remove irrelevant homogeneous scale. Failure to find a violation only describes the searched region and method.

Reduce an informative candidate to low dimension/rank, sparse structure or rational parameters. Check all assumptions and whether cancellation, rounding, solver status or proximity to a boundary explains the observation. Higher precision can diagnose a problem but alone is not a rigorous error certificate.

Read [quadratic inequality](references/quadratic-inequality.md) for a small numerical-search-to-exact-check example; its [script](scripts/quadratic_inequality_probe.py) provides a reusable starting point. This example is optional and does not limit constructions or require every Task to use quadratics.

## Probe Oracle information carefully

Define the hidden object, prior/adversarial class, transcript, allowed query and information quantity. For a next-query question, distinguish unconditional average increments from increments conditional on the observed history. One query strategy or estimator's failure does not establish a bound for every allowed strategy/estimator.

Posterior risk, recoverable energy, unresolved subspace or candidate-set changes can be useful proxies; explain their relationship to the actual task. Continuous exact observations can have infinite Shannon mutual information. Binning, noise, tolerance or finite arithmetic changes the model; a finite-precision decoding failure does not establish exact-Oracle hardness.

## Certify the candidate and hand off

Exact arithmetic, valid intervals or complete finite coverage may certify a particular calculation. Preserve the object, assumptions, residual/certificate and coverage. Symbolic simplification also requires correct domains, branches and nonzero denominators. Numeric or symbolic output does not automatically certify a universal statement.

Deliver the concrete candidate statement or mechanism, supporting and opposing evidence, actual scope and remaining gap. If a counterexample can be certified, provide the exact witness for the existing Proof review. If generalization remains open, formulate the next precise lemma, recurrence, construction or intervention worth pursuing. Stop when computation has located the useful structure or further work will not improve the decision; inconclusive is allowed.
