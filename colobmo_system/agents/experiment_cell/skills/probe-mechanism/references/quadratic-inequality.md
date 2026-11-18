# Quadratic inequality probe

Use this small [mechanism](../SKILL.md) example to connect numerical search, a simpler candidate and an exact check. It does not require inequality probes to use quadratics or every Experiment to perform a search.

## Question and scope

For a diagonal positive-definite H with eigenvalues at most L, investigate

\[
f(x)=\tfrac12x^\top Hx-b^\top x+c,
\qquad \|\nabla f(x)\|^2\le C L\,[f(x)-f^\star].
\]

Use rational coefficients in dimension 1..3. The exact evaluator has x*=H⁻¹b and f*=c-bᵀH⁻¹b/2. Search and evaluator computation here are research costs; the example makes no Algorithm Oracle-complexity claim.

The [script](../scripts/quadratic_inequality_probe.py) enumerates a finite grid using float arithmetic and maximizes the ratio where gap>0. It retains a strongest active diagonal direction and normalizes its displacement to +/-1, then recomputes the resulting candidate with Fraction arithmetic. It also checks an additive shift of c.

For C=1, H=LI and a nonoptimal point give ratio 2 and an exact violation. C=2 is a useful control: the same candidate need not violate the inequality. Neither numerical search nor one exact nonviolating point establishes a universal statement. A general C=2 argument requires mathematical reasoning and the existing Proof review.

## Execute and adapt

Use only the actual uploaded file mapping, as in the [protocol](../../../protocol.md):

```python
import runpy
path = "skills/probe-mechanism/scripts/quadratic_inequality_probe.py"
module = runpy.run_path(INPUT_FILES[path])
module["run"](PARAMETERS, OUTPUT_DIR)
```

The standard-library-only script exports run(parameters, output_dir). Default parameters are:

```json
{"diagonal":["1","2"],"b":["0","0"],"c":"0","L":"2",
 "C":"1","grid":["-2","-1","0","1","2"],"shift":"7"}
```

Rational strings such as "1/3" preserve exact intended inputs. Decimal numbers are interpreted from their string representation, so use explicit fractions when that distinction matters. b must match the diagonal dimension; omitted b is zero and omitted L is the maximum diagonal entry. H must be positive definite and L must bound its eigenvalues. grid has 2..33 distinct rational values. Nonfinite or unrepresentable numerical scales and invalid inputs raise an error before output artifacts are written.

Changing c does not change the gradient or optimality gap, but shifts the absolute optimum. An unanchored f* scale question therefore cannot be answered by silently choosing c=0. Declare an anchor or explicitly reformulate the target as a gap with the appropriate Task scope.

## Evidence and handoff

- search_measurements.json contains float grid measurements, labelled float_grid_search. The candidate search has finite coverage.
- exact_witness.json records rational coefficients, the original search candidate, simplification, positive-definiteness/smoothness checks, exact point, optimum, gradient, gap and lhs-minus-rhs residual. A positive exact residual certifies this candidate's arithmetic violation.
- The same file records the shifted candidate and exact invariance checks. summary.json reports counterexample_candidate or no_violation_at_candidate, with the exact residual and evidence scope.

Independently reconstruct the assumptions and residual when adopting the witness. The service's execution receipt establishes execution provenance; the certificate supplies explicit arithmetic to review. Mathematical acceptance still belongs to the existing Proof flow.

The useful handoff is the explicit construction, checked assumptions, exact violation or remaining gap, and the precise statement to prove/refute. Higher precision, a favorable solver status or a finite sample without violation is not a universal proof.
