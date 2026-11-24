# Short-lived high-volume Bernoulli bandits with bounded-density priors

**Setting ID.** `ONX_SHORT_LIVED_HIGH_VOLUME_BERNOULLI`

Online learning and bandits

Long-run Bayesian average loss with random arriving arms, finite lifetimes, and entire-round batched feedback.

**Status.** Logarithmic gap

**TASK tags.** solution concept: Short lived bayesian bandit; task family: Online bandit

**ORACLE tags.** feedback quality: Stochastic bernoulli; operation: Batched bernoulli rewards; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**GUARANTEE tags.** quantifier: Algorithm before instance

**RESOURCE tags.** measure: Arrivals per round; measure: Lifetime; measure: Plays per round

## 1. Setting specification

### Task

Minimize long-run Bayesian average loss relative to the best currently alive arm in a streaming short-lived high-volume bandit.

### Admissible model

At the start of every calendar round t, a new disjoint cohort A_t of k arms arrives. An arm born at t remains available through t+w inclusive. Thus there are w+1 alive cohorts after initialization and w useful feedback opportunities before its last allocation.

Each arm mean is drawn independently from a distribution D on [0,1]. Conditional on all means, rewards are independent Bernoulli draws across arms and plays. The prior density satisfies $c_1\le f(u)\le c_2$ almost everywhere, where $0<c_1\le1\le c_2<\infty$. Arrival identities and times contain no mean information. The parameters w,c_1,c_2 are fixed for the rate statements.

### Oracle interface

At each round the policy chooses nonnegative integer allocations $\pi_t(a)$ to alive arms, with $\sum_{a\in\mathcal A_t}\pi_t(a)=n$. The entire allocation is measurable before any reward from that round is revealed. All rewards from these n plays are revealed together afterward; no within-round adaptation or stopping is permitted.

The values n,k,w,c_1,c_2 are public. The policy may be given D; the upper policy uses only its density bounds, and the lower bound holds even when D is the known uniform prior. The arm means are hidden.

### Output

The output is the executed sequence of batch allocations. Exactly n plays must be assigned each round, always to arms that are alive.

### Loss or accuracy criterion

Let $\mu_t^*=\max_{a\in\mathcal A_t}\mu_a$. For a finite evaluation horizon T, $\mathcal L_{n,T}(\pi;D)=(nT)^{-1}\mathbb E_D\sum_{t=1}^T\sum_{a\in\mathcal A_t}\pi_t(a)(\mu_t^*-\mu_a)$. The expectation includes the prior, rewards, and policy randomness.

The long-run risk uses $\overline{\mathcal L}_n(\pi;D)=\limsup_{T\to\infty}\mathcal L_{n,T}(\pi;D)$. Define $\mathcal L_n^*(c_1,c_2)=\inf_\pi\sup_{D\in\mathfrak D(c_1,c_2)}\overline{\mathcal L}_n(\pi;D)$, allowing a policy to take D as input. The expectation precedes the limit superior; this is not an expectation-of-limsup criterion.

### Resource accounting

The resource parameters are n plays per calendar round, k arriving arms per round, and lifetime w+1 rounds. There are nT rewards over a finite T-round evaluation. The asymptotic rate sends n to infinity at fixed w,c_1,c_2, with k possibly depending on n; T is sent to infinity inside the long-run performance criterion.

### Algorithm views and success guarantees

All randomized policies with allocations measurable before current-round feedback are allowed. Arms may be sampled multiple times in a round, but allocations cannot adapt within that round. The prior may be known.

$$
\sup_{D\in\mathfrak D(c_1,c_2)}\limsup_{T\to\infty}\mathcal L_{n,T}(\pi;D)\le\ell
$$

One upper policy depending only on n,k,w,c_1,c_2 handles every density in the class. The lower bound holds for every policy under the fixed known uniform prior and even for liminf of the finite-horizon expected losses.

**Budget convention.** fixed_per_round_play_count

## 2. Notation and parameters

$n$: Number of plays allocated in every round **Domain:** $n\ge1$ integer.

$k$: Number of newly arriving arms each round **Domain:** $k\ge1$ integer.

$w$: Number of feedback opportunities before an arm final-age allocation **Domain:** $w\ge1$ integer; lifespan is w+1 rounds.

$c_1,c_2$: Prior density lower and upper bounds **Domain:** $0<c_1\le1\le c_2<\infty$.

$D$: Prior distribution of independent arm means **Domain:** Density between c_1 and c_2 on [0,1].

$T$: Finite evaluation horizon before the long-run limit **Domain:** $T\ge1$ integer.

$\alpha_w$: Optimal finite-lifetime exponent **Domain:** $0<\alpha_w<1/2$.

$\alpha_w=(2^w-1)/(2^{w+1}-1)$

$\rho$: Fixed polynomial arrival exponent **Domain:** $\rho>0$.

$k=\lfloor n^\rho\rfloor$ in the polynomial-arrival regime

$n_0$: Source asymptotic threshold **Domain:** $n_0=n_0(w,c_1,c_2)$ finite.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
\mathcal L_n^*(c_1,c_2)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $(n,k,w)$; description: Exactly n plays per round, k arrivals per round, and a fixed finite lifetime.

### R1 - Finite lifetime with arbitrary arrival count

**Region.** Fix integer $w\ge1$ and $0<c_1\le1\le c_2<\infty$; require $n\ge n_0(w,c_1,c_2)$ and any integer $k\ge1$. No ambient Euclidean dimension; the number of alive arms is at most k(w+1). The lower bound is for liminf of expected averages, hence also bounds the same limsup-risk used by the upper bound.

**Quantity.** Q1

**Resource.** Exactly n plays per round, k arrivals per round, and a fixed finite lifetime.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega_w(\max\{k^{-1},n^{-\alpha_w}\})
$$

**Upper bound.** B1

$$
O_{w,c_1,c_2}\!\left(\min\{1,(\log n)/k+((\log n)/n)^{\alpha_w}\}\right)
$$

**Gap or comparison.** At most logarithmic factors in n; max and sum of the two positive scales differ only by a factor of two.

### R2 - Optimal exponent for polynomial arm arrivals

**Region.** Fix $w,c_1,c_2$ as above and $\rho>0$; let $k=\lfloor n^\rho\rfloor$ and $n\ge n_0$ sufficiently large. Alive-arm count grows as (w+1)floor(n^rho); no Euclidean dimension.

**Quantity.** Q1

**Resource.** Per-round n, polynomial k, and fixed w; the performance is a long-run average.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
\widetilde\Omega_{w,\rho}(n^{-\min\{\rho,\alpha_w\}})
$$

**Upper bound.** B3

$$
\widetilde O_{w,c_1,c_2,\rho}(n^{-\min\{\rho,\alpha_w\}})
$$

**Gap or comparison.** The polynomial exponent is matched; only logarithmic factors remain.

## 4. Bounds and supporting evidence

### B1 - Capped all-success screening across increasing cohort sampling depths.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O_{w,c_1,c_2}\!\left(\min\{1,(\log n)/k+((\log n)/n)^{\alpha_w}\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U09/manuscript.pdf)

**Conditions.** Fix integer $w\ge1$ and $0<c_1\le1\le c_2<\infty$; require $n\ge n_0(w,c_1,c_2)$ and any integer $k\ge1$.; The lower bound is for liminf of expected averages, hence also bounds the same limsup-risk used by the upper bound.

**Dimension conditions.** No ambient Euclidean dimension; the number of alive arms is at most k(w+1).

**Constants.** Upper constants may depend on fixed w,c_1,c_2; lower constants may depend on w. No uniform-in-lifetime claim is made.

**Logarithmic factors.** Powers of log(n) only, not powers of n.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U09/manuscript.pdf) Theorem thm:main; equation eq:main-upper

Capped all-success screening across increasing cohort sampling depths.. One batching policy independent of the exact prior.

### B2 - A batched posterior-discovery inequality and the arrival floor under a uniform prior.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\Omega_w(\max\{k^{-1},n^{-\alpha_w}\})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U09/manuscript.pdf)

**Conditions.** Fix integer $w\ge1$ and $0<c_1\le1\le c_2<\infty$; require $n\ge n_0(w,c_1,c_2)$ and any integer $k\ge1$.; The lower bound is for liminf of expected averages, hence also bounds the same limsup-risk used by the upper bound.

**Dimension conditions.** No ambient Euclidean dimension; the number of alive arms is at most k(w+1).

**Constants.** Upper constants may depend on fixed w,c_1,c_2; lower constants may depend on w. No uniform-in-lifetime claim is made.

**Logarithmic factors.** Powers of log(n) only, not powers of n.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U09/manuscript.pdf) Theorem thm:main; equation eq:main-lower

A batched posterior-discovery inequality and the arrival floor under a uniform prior.. Every randomized admissible policy, including policies knowing the prior.

### B3 - The same prior-uniform capped screening policy.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O_{w,c_1,c_2,\rho}(n^{-\min\{\rho,\alpha_w\}})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U09/manuscript.pdf)

**Conditions.** Fix $w,c_1,c_2$ as above and $\rho>0$; let $k=\lfloor n^\rho\rfloor$ and $n\ge n_0$ sufficiently large.

**Dimension conditions.** Alive-arm count grows as (w+1)floor(n^rho); no Euclidean dimension.

**Constants.** Fixed w,c_1,c_2,rho may enter constants; no uniform growing-w rate is claimed.

**Logarithmic factors.** Powers of log(n) only.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U09/manuscript.pdf) Corollary cor:rho

The same prior-uniform capped screening policy.. Admissible batched policies.

### B4 - Uniform-prior posterior-discovery and arrival lower bounds.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde\Omega_{w,\rho}(n^{-\min\{\rho,\alpha_w\}})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U09/manuscript.pdf)

**Conditions.** Fix $w,c_1,c_2$ as above and $\rho>0$; let $k=\lfloor n^\rho\rfloor$ and $n\ge n_0$ sufficiently large.

**Dimension conditions.** Alive-arm count grows as (w+1)floor(n^rho); no Euclidean dimension.

**Constants.** Fixed w,c_1,c_2,rho may enter constants; no uniform growing-w rate is claimed.

**Logarithmic factors.** Powers of log(n) only.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U09/manuscript.pdf) Corollary cor:rho

Uniform-prior posterior-discovery and arrival lower bounds.. Every admissible policy, even with the uniform prior known.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_U09. Optimal Exponents for Short-Lived High-Volume Bandits. short_lived_high_volume_bandits.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U09/manuscript.pdf
