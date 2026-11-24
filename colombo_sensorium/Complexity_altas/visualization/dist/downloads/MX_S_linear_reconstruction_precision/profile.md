# Linear-function reconstruction with causal bounded errors and paid precision

**Setting ID.** `MX_S_linear_reconstruction_precision`

Matrix computation

Adaptive bounded scalar measurements of a hidden Euclidean vector are priced by their requested tolerance. The objective is uniform reconstruction, allowing arbitrary prediction outputs.

**Status.** Fully optimal on the documented comparison domain

**TASK tags.** solution concept: Uniform linear reconstruction; task family: Matrix computation

**ORACLE tags.** feedback quality: Deterministic bounded error; operation: Approximate linear functional; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**GUARANTEE tags.** mode: Probability; quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Precision cost

## 1. Setting specification

### Task

Reconstruct the hidden linear function $f_\theta(x)=\langle\theta,x\rangle$ uniformly on $B_2^d$. This is an information-reconstruction task with a paid precision resource.

### Admissible model

The hidden target is one fixed vector $\theta\in B_2^d$. Its function is defined on the public Euclidean unit ball. The target remains unchanged throughout the interaction.

### Oracle interface

A query chooses $(x_t,\delta_t)$ with $x_t\in B_2^d$ and $0<\delta_t\le1$. It returns a real $Y_t$ satisfying $$|Y_t-\langle\theta,x_t\rangle|\le\delta_t,$$ at cost $\delta_t^{-a}$, where $a>0$ is public.

The error rule may depend causally on the target, the current query, and the public past transcript. It cannot depend on future queries or unrevealed private random bits. Repeated queries need not receive the same error. No stochastic centering, independence, or distributional assumption is imposed.

Public inputs are $d,a,\varepsilon,\eta$. The target and legal causal error rule are fixed before averaging over private algorithmic randomness.

### Output

Return any prediction function $\widehat f:B_2^d\to\mathbb R$ encoded measurably by the transcript and seed. The output is not required to be linear. All query, oracle, and output maps are measurable, and the uniform-error success event is jointly measurable.

### Loss or accuracy criterion

The loss is uniform prediction error $$\sup_{x\in B_2^d}|\widehat f(x)-\langle\theta,x\rangle|.$$

### Resource accounting

The paid resource is $B=\sum_{t=1}^N\delta_t^{-a}$. The budget must hold on every legal execution and every private seed. Each call costs at least one, so $N\le\lfloor B\rfloor$. Internal computation and storage are uncharged.

### Algorithm views and success guarantees

Queries, stopping decisions, and the output are measurable functions of the preceding transcript and an instance-independent private random seed. The unknown instance is fixed before the seed is realized. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage using public inputs and received information are uncharged. The stated budget must hold on every execution path.

$$
\inf_{\theta\in B_2^d}\inf_{\mathcal O\,\mathrm{legal\ causal}}\Pr\!\left(\sup_{x\in B_2^d}|\widehat f(x)-\langle\theta,x\rangle|\le\varepsilon\right)\ge1-\eta
$$

Only the independent private seed is randomized in the guarantee. The target and causal oracle are fixed first. The budget remains valid on every legal path.

**Budget convention.** fixed_worst_case

## 2. Notation and parameters

$d$: Dimension of the hidden vector **Domain:** $d\in\mathbb N_{\ge1}$.

$a$: Precision-cost exponent **Domain:** $a>0$.

$\varepsilon$: Uniform prediction tolerance **Domain:** $0<\varepsilon<1/4$.

$\eta$: Required failure probability **Domain:** $0\le\eta\le1/3$.

$\delta_t$: Requested tolerance of query t **Domain:** $0<\delta_t\le1$.

Chosen adaptively by the algorithm; not fixed by the instance.

$B$: Pathwise total precision-cost budget **Domain:** $B>=0$.

$\sum_t\delta_t^{-a}\le B$

$\theta$: Hidden target vector **Domain:** $\theta\in B_2^d$.

$N$: Number of actual oracle calls **Domain:** $N\in\mathbb N_0$.

$\widehat f$: Arbitrary returned prediction function **Domain:** $\widehat f:B_2^d\to\mathbb R$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
C^*(B_2^d,\varepsilon,a,\eta)=\inf\{B:\exists A\text{ with pathwise cost }B\text{ and the stated guarantee}\}
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $\sum_{t=1}^N\delta_t^{-a}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

### R1 - Optimal worst-case precision cost for the Euclidean ball

**Region.** Fix $a>0$; $d\ge1$, $0<\varepsilon<1/4$, and $0\le\eta\le1/3$. Every integer d>=1; no growing-dimension requirement. The ball geometry is essential: the rate is not asserted for every smaller fixed query domain.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B2

$$
c_a d^{1+a/2}\varepsilon^{-a}
$$

**Upper bound.** B1

$$
d^{1+a/2}\varepsilon^{-a}
$$

**Gap or comparison.**

$$
O_a(1)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** Every integer d>=1; no growing-dimension requirement.

### B1 - Query all coordinate vectors at tolerance epsilon/sqrt(d), and return the resulting linear predictor

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
d^{1+a/2}\varepsilon^{-a}
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H18/manuscript.pdf)

**Conditions.** Fix $a>0$; $d\ge1$, $0<\varepsilon<1/4$, and $0\le\eta\le1/3$.; The construction succeeds for every legal reply sequence and hence for every required confidence in the stated range.; The ball geometry is essential: the rate is not asserted for every smaller fixed query domain.

**Constants.** Only the lower multiplicative constant depends on fixed a. There is no confidence penalty.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H18/manuscript.pdf) Theorem thm:main, eq:main; Section sec:upper; Corollary cor:confidence

Query all coordinate vectors at tolerance epsilon/sqrt(d), and return the resulting linear predictor. Deterministic nonadaptive algorithms

The construction succeeds for every legal reply sequence and hence for every required confidence in the stated range.

### B2 - Truncated-Gaussian target prior, a fixed causal quantizer, and entropy cost versus small-ball information

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
c_a d^{1+a/2}\varepsilon^{-a}
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H18/manuscript.pdf)

**Conditions.** Fix $a>0$; $d\ge1$, $0<\varepsilon<1/4$, and $0\le\eta\le1/3$.; The lower bound permits adaptive directions, tolerances, stopping, and any measurable prediction function.; The ball geometry is essential: the rate is not asserted for every smaller fixed query domain.

**Constants.** Only the lower multiplicative constant depends on fixed a. There is no confidence penalty.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H18/manuscript.pdf) Theorem thm:main, eq:main; Corollary cor:confidence

Truncated-Gaussian target prior, a fixed causal quantizer, and entropy cost versus small-ball information. All adaptive randomized algorithms with arbitrary prediction outputs

The lower bound permits adaptive directions, tolerances, stopping, and any measurable prediction function.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_H18. Optimal Precision Cost for Randomized Linear Reconstruction. H18_randomized_linear_reconstruction.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H18/manuscript.pdf
