# Bandits with expert advice: pre-action advice and post-action single-arm feedback.

**Setting ID.** `ON_CTX_ADVICE_S`

Online learning and bandits

Each round reveals all experts' distributions over arms before the learner selects an arm and observes only its loss. The target is the best fixed advice expert, whose cumulative benchmark is expected loss under its advice distributions.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Bandit expert advice regret; solution concept: Minimize expected cumulative expert advice regret; task family: Online bandit

**MODEL tags.** stochastic model: Loss range; structure: Expert probabilities; structure: Finite actions

**ORACLE tags.** feedback quality: Source-declared exact feedback (may be a random reward); interface family: Selected reward; operation: Observe expert advice then selected arm; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** measure: Advice entries; measure: Native feedback; measure: Rounds

## 1. Setting specification

### Task

Each round reveals all experts' distributions over arms before the learner selects an arm and observes only its loss. The target is the best fixed advice expert, whose cumulative benchmark is expected loss under its advice distributions.

### Admissible model

Expert i’s current advice distribution $q_{t,i}$ lies in the K-dimensional probability simplex. All M advice distributions are visible before the arm is selected.

The hidden loss vector $\ell_t$ lies in [0,1]^K and is not visible before acting.

The comparator is the best fixed expert in hindsight, $i$, whose cumulative loss is the expected loss of its advice distribution, $\sum_t\langle q_{t,i},\ell_t\rangle$. Experts do not receive separately sampled reward trajectories.

This specification requires $K\ge2$, $M\ge K$, and $T\ge1$, with actions in $[K]$.

Advice is supplied through a dense M-by-K numerical interface; future advice remains hidden.

### Oracle interface

Full advice is revealed first, followed by the selected-arm loss.

$$
(q_{t,1},\ldots,q_{t,M})\ \longrightarrow\ a_t\in[K]\ \longmapsto\ Y_t=\ell_t(a_t)
$$

All current advice is visible before selecting an arm. Selection of an expert before advice is not required.

After acting, only the selected arm's loss is returned, not the full $\ell$_t or the true loss of every expert.

Expert advice and losses are fixed in advance; there is no additional observation noise.

Public inputs are $K,T,M$. All $M$ current recommendation vectors are revealed before arm selection; future recommendations are not supplied.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
q_{t,i}\in\Delta_K,\quad R_T=\sum_t\ell_t(a_t)-\min_{i\in[M]}\sum_t\langle q_{t,i},\ell_t\rangle
$$

### Resource accounting

Each round reveals M × K advice values and one loss scalar, for T selected-arm feedback observations.

Any policy acting after recommendations are revealed is allowed. q-FTRL may maintain expert weights and sample an arm from their mixture.

Dense advice itself contains MK numbers per round. Mixing, importance weighting, and FTRL subproblems are internal computation and are not hidden inside the bandit sample count.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}}\sup_{(q_{t,i}),\ell_{1:T}}\mathbb{E}_{\mathcal{A}}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$K$: The finite number of arms. **Domain:** $K\in\mathbb N,\ K\ge2$.

The arm set is $[K]=\{1,\ldots,K\}$.

$M$: Number of advice experts **Domain:** $M\in\mathbb N,\ M\ge K$.

Before acting each round, observe M experts' advice distributions over K arms.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$\ell_t$: Hidden loss vector at round t **Domain:** $\ell_t\in[0,1]^K$.

The entire sequence is fixed before interaction; only coordinates allowed by the protocol become visible after acting.

$a_t$: Arm or expert that actually incurs loss in round $t$ **Domain:** $a_t\in[K]$.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$q_{t,i}$: Expert i’s current advice distribution. **Domain:** $q_{t,i}\in\Delta_K$.

Coordinate a is the probability of recommending arm a. All current advice is visible before acting.

$\Delta_K$: Probability simplex over $K$ arms **Domain:** $\Delta_K\subset\mathbb R^K$.

$\{q\in[0,1]^K:\sum_aq_a=1\}$.

$i,[M]$: Index and index set of the fixed advice experts **Domain:** $i\in[M]=\{1,\ldots,M\}$.

The comparator loss is $\sum_t\langle q_{t,i},\ell_t\rangle$.

$e$: Base of the natural logarithm in the explicit upper-bound constant **Domain:** Constant.

$e=\exp(1)$.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_t\ell_t(a_t)-\min_{i\in[M]}\sum_t\langle q_{t,i},\ell_t\rangle$.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{(q,\ell)\in\mathcal I}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T\ell_t(a_t)-\min_{i\in[M]}\sum_{t=1}^T\langle q_{t,i},\ell_t\rangle,\\ q_{t,i}&\in\Delta_K,\qquad\ell_t\in[0,1]^K.\end{aligned}
$$

$\mathcal A$: Learning policies satisfying the specified information, computation, and privacy restrictions **Domain:** A measurable causal policy.

Actions may depend only on revealed information and the private seed. Additional restrictions are governed by the algorithm protocol in this profile.

$t$: Interaction-time index **Domain:** $t\in\{1,\ldots,T\}$.

$\mathbb E$: Mean operator **Domain:** Expectation over the specified random variables.

Expectation includes the learner's private randomness and, when allowed, the environment strategy's randomness. A fixed loss sequence introduces no additional observation noise.

$\log,\log_2$: Natural and binary logarithms **Domain:** Function on the positive real axis.

$\log x=\ln x$, $\log_2x=\log x/\log2$.

$c,C$: Positive constant in the bound without an assigned numerical value **Domain:** Positive real number.

Constants apply only under the associated bound’s conditions and fixed-parameter convention. Unspecified theorem constants are not treated as additional algorithm inputs.

$O,\Omega,\widetilde O,\widetilde\Omega$: Asymptotic upper and lower bounds, including explicitly permitted logarithmic suppression. **Domain:** Asymptotic comparison notation.

The result applies only in the regime declared for that bound. Tilde notation hides only its stated logarithms and fixed-parameter dependencies, never additional polynomial parameter factors.

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The quantity $N=T$ counts cumulative native scalar feedback under a one-point or one-arm protocol.

$\mathcal I$: The complete environment class in the current minimax objective. **Domain:** Collection of function classes or reward-distribution classes.

The loss and advice arrays $(\ell_{1:T},q_{1:T,1:M})$ are fixed before interaction, with $\ell_t\in[0,1]^K$ and $q_{t,i}\in\Delta_K$. All current advice is revealed before the action in each round.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax cumulative expert advice regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{(q,\ell)\in\mathcal I}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T\ell_t(a_t)-\min_{i\in[M]}\sum_{t=1}^T\langle q_{t,i},\ell_t\rangle,\\ q_{t,i}&\in\Delta_K,\qquad\ell_t\in[0,1]^K.\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - MAIN

**Region.** $M\ge K\ge 2; T\ge K$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
0.04\sqrt{KT}
$$

**Upper bound.** B1

$$
2sqrt[eKT(2+ln(M/K))]
$$

**Gap or comparison.** O(sqrt[1+ln(M/K)])

**Comparison argument.** Only individually audited compatible claims enter. Certified baseline polylog bracket, not exact expert-count dependence. Restricted feedback Th5.1 is expressly excluded.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Assume $M\ge K\ge2$ and $T\ge K$. Every expert's current recommendation is public before arm selection. After selecting an arm, only that arm's loss is observed.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - Tsallis regularization tuned to K,M

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le2\sqrt{eKT\bigl(2+\log(M/K)\bigr)}
$$

**Sources.** [1](https://arxiv.org/pdf/2406.16802v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T selected losses

**advice entries.** MKT

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2406.16802v1) theorem: Theorem 3.1; pdf pages: 4

The source upper bound is $2\sqrt{e(K\wedge M)T(2+\log(M/(K\wedge M)))}$. This setting reveals all expert advice before the action, so it can simulate the feedback required by the proved algorithm.

### B2 - K constant deterministic arm experts plus duplicate experts

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge0.04\sqrt{KT}
$$

**Sources.** [2](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Let the first $K$ experts always recommend distinct fixed arms, and let all remaining experts duplicate those recommendations. Revealed advice carries no loss information, and the best-expert comparator becomes the best fixed arm. The finite-armed bandit lower bound therefore applies directly.

**Source location.** [2](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf) theorem: Theorem 30 and proof; section: Appendix B; pdf pages: 28; 29; 30; printed pages: 2812; 2813; 2814

Use only the K-armed bandit branch with source sampling budget $m_{\mathrm{src}}=T$. In context-block reductions each block uses its own length. Bernoulli hard instances and Yao's principle give the randomized-learner lower bound.

## References

[1] Nicolò Cesa-Bianchi; Khaled Eldowa; Emmanuel Esposito; Julia Olkhovskaya. Improved Regret Bounds for Bandits with Expert Advice. 2024. arXiv:2406.16802v1, 2024-06-24; subsequent JAIR 83 article 6, July 2025.

https://arxiv.org/pdf/2406.16802v1

[2] Jean-Yves Audibert; Sébastien Bubeck. Regret Bounds and Minimax Policies under Partial Monitoring. 2010. JMLR 11:2785–2836.

https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf
