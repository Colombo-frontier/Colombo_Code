# Bandits with increasing mean trajectories and a known variation budget

**Setting ID.** `ONX_RISING_MONOTONE_KNOWNV`

Online learning and bandits

All arms evolve in calendar time, including unselected arms. Their fixed unknown means increase, without a concavity requirement. The learner observes only the selected arm's fresh reward and compares with the largest current mean; the variation budget is known.

**Status.** Polynomial gap present

**TASK tags.** formulation: Onx rising monotone knownv; task family: Online bandit

**MODEL tags.** stochastic model: Nonstationary

**ORACLE tags.** interface family: Selected reward; operation: Selected reward; public information: Hidden objects explicitly declared; public information: Known variation; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

All arms evolve in calendar time, including unselected arms. Their fixed unknown means increase, without a concavity requirement. The learner observes only the selected arm's fresh reward and compares with the largest current mean; the variation budget is known.

### Admissible model

There are $K\ge2$ arms with reward distributions $\nu_i(t)$ fixed before interaction and evolving in absolute time. Every arm evolves, including unpulled arms. The means satisfy:

$$
\mu_i(t)=\mathbb{E}_{X\sim\nu_i(t)}X\in[0,1],\qquad \gamma_i(t)=\mu_i(t+1)-\mu_i(t)\ge0.
$$

Decreasing increments are not required, so temporal concavity is not assumed.

$$
V_\mu=\sum_{t=1}^{T-1}\max_{i\in[K]}\gamma_i(t)\le V,\qquad 0\le V\le K.
$$

### Oracle interface

Choose $I_t\in[K]$ using past observations, then observe only $X_{I_t,t}$. Rewards of other arms in the same round are hidden.

Each $X_{i,t}$ is $\sigma$-sub-Gaussian around $\mu_i(t)$ and is independent of the entire reward table before round $t$. Within-round dependence across arms does not affect the single-arm feedback model.

Only reward means are restricted to $[0,1]$; realized rewards need not lie in that interval.

Causal bandit policies are allowed. Public inputs are $K,T,\sigma,V$.

The mean function is not revealed.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\mathbb{E}_{\mathcal{A},\nu}\!\left[\sum_{t=1}^{T}\left(\max_{i\in[K]}\mu_i(t)-\mu_{I_t}(t)\right)\right].
$$

### Resource accounting

The horizon $T$ counts calendar-time rounds, and $N=T$ counts observed selected-arm rewards. Each bound retains its source noise, horizon, and exploration windows.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

The target is expected dynamic pseudo-regret. Take the infimum over admissible causal strategies before the supremum over fixed distribution schedules satisfying the structural and variation constraints. Expectation includes algorithm and reward randomness.

## 2. Notation and parameters

$K$: The finite number of arms. **Domain:** $K\in\mathbb N,\ K\ge2$.

The arm set is $[K]=\{1,\ldots,K\}$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$V$: A budget on cumulative maximum mean increments. **Domain:** $0\le V\le K$.

Assume $V_\mu=\sum_{t=1}^{T-1}\max_i[\mu_i(t+1)-\mu_i(t)]\le V$; every arm evolves in calendar time.

$\sigma$: Conditional sub-Gaussian scale of the reward noise **Domain:** Require $\sigma\ge0$. The registered theorem window additionally requires $\sigma\ge1$.

The condition $\mathbb E[e^{s(X_t-\mu_{I_t}(t))}\mid\mathcal H_{t-1},I_t]\le e^{s^2\sigma^2/2}$ holds for every real s.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$\nu_i(t),\mu_i(t)$: Reward distribution and mean of arm $i$ at absolute time $t$. **Domain:** Probability distributions and their means in [0,1].

$\mu_i(t)=\mathbb E_{X\sim\nu_i(t)}X$. Unpulled arms also evolve with calendar time.

$\gamma_i(t)$: Mean increments between consecutive calendar times. **Domain:** $\gamma_i(t)\ge0$.

The quantity is $\gamma_i(t)=\mu_i(t+1)-\mu_i(t)$; it need not be nonincreasing in t.

$V_\mu$: Actual cumulative maximum arm-mean increment **Domain:** $0\le V_\mu\le\min\{K,T-1\}$.

$V_\mu=\sum_{t=1}^{T-1}\max_i\gamma_i(t)$.

$I_t$: The currently selected arm. **Domain:** $I_t\in[K]$.

$h$: The restart block length for MOSS. **Domain:** $1\le h\le T$.

Use public V to balance $Vh$ and $\sigma T\sqrt{K/h}$; when $V=0$, choose $h=T$.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

The loss is $R_T=\sum_t[\max_i\mu_i(t)-\mu_{I_t}(t)]$. Realized observation noise is excluded from the loss difference; probability or expectation aggregation is specified separately by the guarantee.

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

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The quantity $N=T$ counts cumulative native scalar feedback under a one-point or one-arm protocol.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
\mathbb E_{\mathcal A,\nu}\!\left[\sum_{t=1}^{T}\left(\max_{i\in[K]}\mu_i(t)-\mu_{I_t}(t)\right)\right].
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SMALL_VARIATION

**Region.** Assume $\sigma\ge1$, $0<V\le1$, and $T\ge4\sigma^2K/V^2$. Both bounds track every parameter explicitly.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Optimal

**Lower bound.** B1

$$
\Omega((\sigma^2KV)^{1/3}T^{2/3})
$$

**Upper bound.** B2

$$
O((\sigma^2KV)^{1/3}T^{2/3})
$$

**Gap or comparison.** Bounds match up to constants. The increasing-mean constraint does not reduce hardness on this slice.

### R2 - SUPPORTED

**Region.** $\sigma\ge 1$; $0<V\le K$; $T\ge 4\sigma^{2}K \min{1,V}^{-2}$. Under $V>1$, the gap is at most $V^{1/3}$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Polynomial gap

**Lower bound.** B1

$$
\Omega(\sigma^{2/3}K^{1/3}\min\{1,V\}^{1/3}T^{2/3})
$$

**Upper bound.** B2

$$
O((\sigma^2KV)^{1/3}T^{2/3})
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee mapping.** The accompanying argument states the native guarantee and necessary conversion.

### B1 - A fixed hard prior with independent optimal arms across windows.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
2^{-6}\sigma^{2/3}K^{1/3}\min\{1,V\}^{1/3}T^{2/3}
$$

**Sources.** [1](https://proceedings.nips.cc/paper_files/paper/2025/file/1aa670dafbd4b32ebf483f8372e612c5-Paper-Conference.pdf)

**Conditions.** Require $\sigma\ge1$, $0<V\le K$, and $T\ge\sigma^2K\min\{1,V\}^{-2}$, together with the increasing-mean model.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** The appendix uses a fixed hard prior independent of the algorithm. Conditioning on the private seed and then integrating preserves the prior and lower-bound constant, so the result covers randomized strategies.

**Source location.** [1](https://proceedings.nips.cc/paper_files/paper/2025/file/1aa670dafbd4b32ebf483f8372e612c5-Paper-Conference.pdf) theorem: Theorem 3.2; Appendix B Lemma 3.1

The appendix uses a fixed hard prior independent of the algorithm. Conditioning on the private seed and then integrating preserves the prior and lower-bound constant, so the result covers randomized strategies.

### B2 - Deterministic R-MOSS with restart length chosen from known $V$.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\min\{T,\sigma\sqrt{KT}+(\sigma^2KV)^{1/3}T^{2/3}\}\right)
$$

**Sources.** [2](https://arxiv.org/abs/2101.08980)

**Conditions.** Require $\sigma\ge1$, $K\ge2$, $T\ge K$, and $0\le V\le K$. Means lie in $[0,1]$, while realized rewards may be unbounded.; All arms evolve with calendar time. Only the selected arm yields a fresh independent sample each round.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** Divide rewards by $2\sigma$, yielding the source sub-Gaussian parameter $1/2$ and variation $V/(2\sigma)$. With restart length $h$, the original-scale upper bound is $O(Vh+\sigma T\sqrt{K/h}+\sigma\sqrt{Kh})$. Restrict $h$ to $[1,T]$ and balance the terms; if $V=0$, choose $h=T$. Mean gaps per round are at most one, giving the additional cap $T$. The algorithm needs no monotonicity and therefore applies to the increasing subclass.

**Source location.** [2](https://arxiv.org/abs/2101.08980) theorem: Assumption1; Theorem3 and its arbitrary-reset-length proof

Divide rewards by $2\sigma$, yielding the source sub-Gaussian parameter $1/2$ and variation $V/(2\sigma)$. With restart length $h$, the original-scale upper bound is $O(Vh+\sigma T\sqrt{K/h}+\sigma\sqrt{Kh})$. Restrict $h$ to $[1,T]$ and balance the terms; if $V=0$, choose $h=T$. Mean gaps per round are at most one, giving the additional cap $T$. The algorithm needs no monotonicity and therefore applies to the increasing subclass.

## References

[1] Cristiano Migali; Marco Mussi; Gianmarco Genalti; Alberto Maria Metelli. Tightening Regret Lower and Upper Bounds in Restless Rising Bandits. 2025. NeurIPS 2025 publisher PDF.

https://proceedings.nips.cc/paper_files/paper/2025/file/1aa670dafbd4b32ebf483f8372e612c5-Paper-Conference.pdf

[2] Lai Wei; Vaibhav Srivastava. Nonstationary Stochastic Multiarmed Bandits: UCB Policies and Minimax Regret. 2021. arXiv2101.08980v1.

https://arxiv.org/abs/2101.08980
