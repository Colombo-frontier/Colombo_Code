# Bandits with increasing concave mean trajectories and an unknown variation budget

**Setting ID.** `ONX_RISING_CONCAVE_UNKNOWNV`

Online learning and bandits

All arms evolve in calendar time, including unselected arms. Their fixed unknown means increase concavely in time. The learner observes only the selected arm's fresh reward and compares with the largest current mean; the variation budget is unknown.

**Status.** Logarithmic gap

**TASK tags.** formulation: Onx rising concave unknownv; task family: Online bandit

**MODEL tags.** convexity: Rising concave; stochastic model: Nonstationary

**ORACLE tags.** interface family: Selected reward; operation: Selected reward; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; public information: Unknown variation

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

All arms evolve in calendar time, including unselected arms. Their fixed unknown means increase concavely in time. The learner observes only the selected arm's fresh reward and compares with the largest current mean; the variation budget is unknown.

### Admissible model

There are $K\ge2$ arms with reward distributions $\nu_i(t)$ fixed before interaction and evolving in absolute time. Every arm evolves, including unpulled arms. The means satisfy:

$$
\mu_i(t)=\mathbb{E}_{X\sim\nu_i(t)}X\in[0,1],\qquad \gamma_i(t)=\mu_i(t+1)-\mu_i(t)\ge0.
$$

Each arm’s mean is also discretely concave in time:

$$
\gamma_i(t+1)\le\gamma_i(t).
$$

$$
V_\mu=\sum_{t=1}^{T-1}\max_{i\in[K]}\gamma_i(t)\le V,\qquad 0\le V\le K.
$$

### Oracle interface

Choose $I_t\in[K]$ using past observations, then observe only $X_{I_t,t}$. Rewards of other arms in the same round are hidden.

Each $X_{i,t}$ is $\sigma$-sub-Gaussian around $\mu_i(t)$ and is independent of the entire reward table before round $t$. Within-round dependence across arms does not affect the single-arm feedback model.

Only reward means are restricted to $[0,1]$; realized rewards need not lie in that interval.

Causal bandit policies are allowed. The data $K,T,\sigma$ are public. The algorithm receives neither $V$ nor any variation bound beyond structural feasibility.

Mean functions are hidden. The concavity variant also hides change times.

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

The target is expected dynamic pseudo-regret: take the infimum over causal policies, then the supremum over fixed distribution schedules satisfying the structural and variation constraints. Expectation covers policy and reward randomness. Unknown-budget variants require one policy independent of $V$ to handle different actual variations, rather than a separately tuned known-budget algorithm for each $V$.

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

The increments are $\gamma_i(t)=\mu_i(t+1)-\mu_i(t)$. In the concave variant they are nonincreasing in $t$.

$V_\mu$: Actual cumulative maximum arm-mean increment **Domain:** $0\le V_\mu\le\min\{K,T-1\}$.

$V_\mu=\sum_{t=1}^{T-1}\max_i\gamma_i(t)$.

$I_t$: The currently selected arm. **Domain:** $I_t\in[K]$.

$\alpha_R$: The growth exponent of budget-independent RC-BE. **Domain:** Fixed algorithm tuning.

The quantity $\alpha_R=8/3$ is independent of V.

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

$v$: Clipped variation **Domain:** $0\le v\le1$.

$v=\min\{1,V\}$

$S$: Stationary regret scale **Domain:** $S>0$.

$S=\sigma\sqrt{KT}$

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
\mathbb E_{\mathcal A,\nu}\!\left[\sum_{t=1}^{T}\left(\max_{i\in[K]}\mu_i(t)-\mu_{I_t}(t)\right)\right].
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - Concave rising means: all expected-regret regimes

**Region.** $K,T\ge2$ integers, $\sigma\ge1$, and $0\le V\le K$; let $v=\min\{1,V\}$. Finite K arms; no Euclidean action dimension. The saturated regime is $T\le\sigma^2K$. When $T>\sigma^2K$, the stationary term dominates for $v\le\sigma\sqrt{K/T}$ and the concave nonstationary term dominates above that threshold. No theorem here claims a sharp minimax rate for sigma<1.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
\Omega\!\left(\min\{T,\sigma\sqrt{KT}+\sigma^{4/5}K^{2/5}v^{1/5}T^{3/5}\}\right)
$$

**Upper bound.** B3

$$
O\!\left(\min\{T,[\log(2KT)]^{3/2}(\sigma\sqrt{KT}+\sigma^{4/5}K^{2/5}v^{1/5}T^{3/5})\}\right)
$$

**Gap or comparison.** An $O([\log(2KT)]^{3/2})$ factor remains, uniformly in K,T,V,sigma in the stated domain.

## 4. Bounds and supporting evidence

### B1 - RC-BE with fixed parameter $8/3$, without access to $V$ or $T$.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\widetilde{O}\!\left(\sigma K^3T^{6/11}+K^3V_\mu T^{7/11}+\sigma KT^{7/11}\right)
$$

**Sources.** [1](https://proceedings.nips.cc/paper_files/paper/2025/file/1aa670dafbd4b32ebf483f8372e612c5-Paper-Conference.pdf)

**Conditions.** Require $\sigma\ge1$ and $T\ge2^{24}$. RC–BE uses the fixed exploration parameter $\alpha_R=8/3$.; The quantity $V_\mu$ is actual total mean variation. This fixed-parameter algorithm needs neither $V$ nor advance knowledge of $T$; $T$ appears only in its evaluation.; The notation $\widetilde O$ hides only the source's logarithmic factors. This entry adopts the displayed RC-BE rate for unknown variation. The separate $T^{3/5}$ rate is not adopted from this source.

**Oracle correspondence.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

**Source location.** [1](https://proceedings.nips.cc/paper_files/paper/2025/file/1aa670dafbd4b32ebf483f8372e612c5-Paper-Conference.pdf) Theorem 4.4, alpha=8/3, PDF p.9

### B2 - Fixed hard prior for the baseline or corrected trend within a window

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
2^{-14}\sigma^{4/5}K^{2/5}\min\{1,V\}^{1/5}T^{3/5}
$$

**Sources.** [1](https://proceedings.nips.cc/paper_files/paper/2025/file/1aa670dafbd4b32ebf483f8372e612c5-Paper-Conference.pdf)

**Conditions.** Require $\sigma\ge1$, $0<V\le K$, and $T\ge2^{10}\sigma^2K\min\{1,V\}^{-2}$. The variation budget is not supplied to the algorithm.

**Oracle correspondence.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

**Derivation.** The randomized lower bound under a fixed hard prior also applies to policies lacking the variation budget. Each $V$ slice has its own worst-case instance; one instance is not asserted to realize all slices simultaneously.

**Source location.** [1](https://proceedings.nips.cc/paper_files/paper/2025/file/1aa670dafbd4b32ebf483f8372e612c5-Paper-Conference.pdf) Theorem 3.3, PDF p.6

### B3 - Suffix-OLS-UCB with confidence level delta=T^(-2), all observation suffixes, and an adaptive piecewise-affine approximation inequality.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\min\{T,[\log(2KT)]^{3/2}(\sigma\sqrt{KT}+\sigma^{4/5}K^{2/5}v^{1/5}T^{3/5})\}\right)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U12/manuscript.pdf)

**Conditions.** $K,T\ge2$ integers, $\sigma\ge1$, and $0\le V\le K$; let $v=\min\{1,V\}$.; The original upper theorem permits conditional sub-Gaussian noise, so it applies to this independent-noise subclass.; The saturated regime is $T\le\sigma^2K$. When $T>\sigma^2K$, the stationary term dominates for $v\le\sigma\sqrt{K/T}$ and the concave nonstationary term dominates above that threshold.; No theorem here claims a sharp minimax rate for sigma<1.

**Dimension conditions.** Finite K arms; no Euclidean action dimension.

**Constants.** Universal constants.

**Logarithmic factors.** Only the explicitly displayed logarithm in K,T.

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U12/manuscript.pdf) Corollary cor:expected-main; Theorem cor:minimax-main; equations eq:expected-rate and eq:minimax-main

Suffix-OLS-UCB with confidence level delta=T^(-2), all observation suffixes, and an adaptive piecewise-affine approximation inequality.. A causal policy using K,T,sigma but no variation budget or slope-change information.

The original upper theorem permits conditional sub-Gaussian noise, so it applies to this independent-noise subclass.

### B4 - Stationary Gaussian lower bound combined with the cited concave nonstationary hard prior in its valid horizon window.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\Omega\!\left(\min\{T,\sigma\sqrt{KT}+\sigma^{4/5}K^{2/5}v^{1/5}T^{3/5}\}\right)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U12/manuscript.pdf)

**Conditions.** $K,T\ge2$ integers, $\sigma\ge1$, and $0\le V\le K$; let $v=\min\{1,V\}$.; Independent Gaussian rewards witness the lower bound. The stationary term covers the parameter region outside the nonstationary source lower-bound window.; The saturated regime is $T\le\sigma^2K$. When $T>\sigma^2K$, the stationary term dominates for $v\le\sigma\sqrt{K/T}$ and the concave nonstationary term dominates above that threshold.; No theorem here claims a sharp minimax rate for sigma<1.

**Dimension conditions.** Finite K arms; no Euclidean action dimension.

**Constants.** Universal constants.

**Logarithmic factors.** Only the explicitly displayed logarithm in K,T.

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U12/manuscript.pdf) Theorem cor:minimax-main; stationary lower bound eq:stationary-lower; Appendix app:main-proof

Stationary Gaussian lower bound combined with the cited concave nonstationary hard prior in its valid horizon window.. Every causal randomized policy, even if V is supplied.

Independent Gaussian rewards witness the lower bound. The stationary term covers the parameter region outside the nonstationary source lower-bound window.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Cristiano Migali; Marco Mussi; Gianmarco Genalti; Alberto Maria Metelli. Tightening Regret Lower and Upper Bounds in Restless Rising Bandits. 2025. NeurIPS 2025 publisher PDF.

https://proceedings.nips.cc/paper_files/paper/2025/file/1aa670dafbd4b32ebf483f8372e612c5-Paper-Conference.pdf

[2] Colombo_U12. Minimax Regret for Restless Rising Concave Bandits via Suffix Least-Squares Optimism. Suffix_OLS_UCB_Colombo_Team.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U12/manuscript.pdf
