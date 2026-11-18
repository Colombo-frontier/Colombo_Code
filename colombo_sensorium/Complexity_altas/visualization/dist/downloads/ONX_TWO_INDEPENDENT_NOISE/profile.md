# Stochastic convex bandits: independent noise at two points and loss at the center.

**Setting ID.** `ONX_TWO_INDEPENDENT_NOISE`

Online learning and bandits

A fixed unknown convex Lipschitz objective is defined on a Euclidean ball. Each round permits two simultaneous probes, each returning an independently Gaussian-noised value. Only the center incurs the true objective loss; independent noise does not cancel in finite differences.

**Status.** Bounds missing

**TASK tags.** formulation: Onx two independent noise; task family: Online bandit

**MODEL tags.** convexity: Convex

**ORACLE tags.** interface family: Two point independent noise; operation: Two point independent noise; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

A fixed unknown convex Lipschitz objective is defined on a Euclidean ball. Each round permits two simultaneous probes, each returning an independently Gaussian-noised value. Only the center incurs the true objective loss; independent noise does not cancel in finite differences.

### Admissible model

The action center and both probes lie in the Euclidean ball $B_2^d(R)$. The fixed unknown objective $f$ is convex and $L$-Lipschitz on that ball, with normalization $f(0)=0$. Smoothness is not assumed.

### Oracle interface

$$
Y_t^+=f(z_t^+)+\varepsilon_t^+,\qquad Y_t^-=f(z_t^-)+\varepsilon_t^-,\qquad \varepsilon_t^\pm\overset{\mathrm{i.i.d.}}\sim\mathcal{N}(0,\sigma^2).
$$

The center $x_t$ and both probes $z_t^+,z_t^-$ must be submitted together before any response is received. Noise is independent across every query, with no shared random seed.

Only the center loss $f(x_t)$ is incurred each round. The two probes provide information, and their values are not added to the round loss.

Causal policies may submit two simultaneous probes per round. The quantities $d,T,R,L,\sigma$ are public; $f$ is hidden. Both probes and their center must lie in the same ball.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_T=\sum_{t=1}^T\bigl(f(x_t)-\min_{x\in B_2^d(R)}f(x)\bigr).
$$

Only the center $x_t$ incurs true function loss each round. Probe-noise realizations do not enter regret.

### Resource accounting

$$N=2T\quad\text{independent scalar function evaluations}.$$

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

$$
\inf_{\mathcal{A}}\ \sup_{\substack{f\ \text{\text{convex and} }L\text{-Lipschitz}\\f(0)=0}}\ \mathbb{E}\!\left[\sum_{t=1}^{T}\left(f(x_t)-\min_{x\in B_2^d(R)}f(x)\right)\right].
$$

Expectation covers policy randomness and all independent observation noise.

## 2. Notation and parameters

$L$: A Euclidean Lipschitz or gradient-norm bound on losses. **Domain:** $L>0$.

$|f(x)-f(y)|\le L\|x-y\|_2$. Function and point domains follow the declared model.

$R$: Euclidean-ball radius of the center-action set **Domain:** $R>0$.

$B_2^d(R)=\{x\in\mathbb R^d:\|x\|_2\le R\}$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\sigma$: Common standard deviation of two independent Gaussian observation-noise terms **Domain:** $\sigma\ge0$.

$\varepsilon_t^+,\varepsilon_t^-\sim\mathcal N(0,\sigma^2)$, independently across probes and rounds and independently of the past.

$f$: Fixed hidden normalized convex function **Domain:** $f:B_2^d(R)\to\mathbb R$.

Since $f(0)=0$, one has $|f(z)|\le LR$.

$x_t,z_t^+,z_t^-$: The loss-incurring center and two observation-only probes. **Domain:** $x_t,z_t^+,z_t^-\in B_2^d(R)$.

After both points are submitted, two independently noisy observations arrive. The center receives no third free observation.

$\varepsilon_t^+,\varepsilon_t^-$: The separate Gaussian noises at the two probes. **Domain:** Independent zero-mean real random variables.

Each variance is $\sigma^2$; these are neither accuracy nor privacy parameters.

$a,u$: The contraction ratio and random spherical direction in the conservative one-point upper bound. **Domain:** $0<a\le1/2,\ u\in\mathbb S^{d-1}$.

Probe radius is aR. The second observation may be discarded; the upper bound does not use same-sample cancellation.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

The loss is $R_T=\sum_t[f(x_t)-\min_{u\in B_2^d(R)}f(u)]$. Realized observation noise is excluded from the loss difference; probability or expectation aggregation is specified separately by the guarantee.

$\mathcal A$: Learning policies satisfying the specified information, computation, and privacy restrictions **Domain:** A measurable causal policy.

Actions may depend only on revealed information and the private seed. Additional restrictions are governed by the algorithm protocol in this profile.

$t$: Interaction-time index **Domain:** $t\in\{1,\ldots,T\}$.

$\mathbb E$: Mean operator **Domain:** Expectation over the specified random variables.

Expectation includes learner randomness and the explicitly specified reward or sample randomness. Conditional expectations retain their stated history conditioning.

$\log,\log_2$: Natural and binary logarithms **Domain:** Function on the positive real axis.

$\log x=\ln x$, $\log_2x=\log x/\log2$.

$c,C$: Positive constant in the bound without an assigned numerical value **Domain:** Positive real number.

Constants apply only under the associated bound’s conditions and fixed-parameter convention. Unspecified theorem constants are not treated as additional algorithm inputs.

$O,\Omega,\widetilde O,\widetilde\Omega$: Asymptotic upper and lower bounds, including explicitly permitted logarithmic suppression. **Domain:** Asymptotic comparison notation.

The result applies only in the regime declared for that bound. Tilde notation hides only its stated logarithms and fixed-parameter dependencies, never additional polynomial parameter factors.

$B_2^d(r)$: Closed Euclidean ball of radius r **Domain:** $r\ge0$.

$B_2^d(r)=\{x\in\mathbb R^d:\|x\|_2\le r\}$. The symbol r is a placeholder radius, instantiated as R or 1 in the relevant specification.

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The count $N=2T$ measures scalar value evaluations in the two-point protocol. Loss remains charged at the center.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
R_T=\sum_{t=1}^T\bigl(f(x_t)-\min_{x\in B_2^d(R)}f(x)\bigr).
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** The center lies in the ball; two independent Gaussian probes are used; $f(0)=0$. This is a supported conservative baseline, with no optimality claim.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
O(\sqrt{dLR\sqrt{L^2R^2+\sigma^2}}\;T^{3/4})\wedge(2LRT)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The bound requires $d,T\ge 1$, $f(0)=0$, $L,R>0$, and $\sigma\ge 0$, with both probes and the center inside the ball.

**Oracle mapping.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee mapping.** The accompanying argument states the native guarantee and necessary conversion.

### B1 - Gaussian one-point smoothing with gradient descent, ignoring the second probe

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\sqrt{dLR\sqrt{L^2R^2+\sigma^2}}\;T^{3/4}\right)\wedge(2LRT)
$$

**Sources.** [1](https://arxiv.org/pdf/2607.18652v3)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** Contract the ball by proportion $a\in(0,1/2]$ and query the contracted center plus $aRu$, where $u$ is a random unit direction. The assumption $f(0)=0$ and Lipschitz continuity imply $|f(z)|\le LR$, and the gradient estimator has second moment at most $d^2(L^2R^2+\sigma^2)/(a^2R^2)$. Online gradient analysis gives $O(d\sqrt{L^2R^2+\sigma^2}\sqrt T/a+LRTa)$. Balance these terms and compare with the fixed-point strategy bound $2LRT$. Only one noisy value per round is needed; the second may be discarded. This argument does not use common-sample noise cancellation.

**Source location.** [1](https://arxiv.org/pdf/2607.18652v3) theorem: Classical one-point spherical-smoothing analysis and the source's corrected Gaussian-FKM discussion.

Contract the ball by proportion $a\in(0,1/2]$ and query the contracted center plus $aRu$, where $u$ is a random unit direction. The assumption $f(0)=0$ and Lipschitz continuity imply $|f(z)|\le LR$, and the gradient estimator has second moment at most $d^2(L^2R^2+\sigma^2)/(a^2R^2)$. Online gradient analysis gives $O(d\sqrt{L^2R^2+\sigma^2}\sqrt T/a+LRTa)$. Balance these terms and compare with the fixed-point strategy bound $2LRT$. Only one noisy value per round is needed; the second may be discarded. This argument does not use common-sample noise cancellation.

## References

[1] Nived Rajaraman; Yanjun Han. The Price of Hidden Curvature: Improved Lower Bounds for Bandit Convex Optimization. 2026. 2607.18652v3.

https://arxiv.org/pdf/2607.18652v3
