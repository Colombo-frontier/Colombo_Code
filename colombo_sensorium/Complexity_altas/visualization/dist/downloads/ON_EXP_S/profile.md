# Finite experts: full loss-vector feedback and external regret

**Setting ID.** `ON_EXP_S`

Online learning and bandits

In each round the learner chooses one of finitely many experts, incurs its loss, and then observes every expert's current loss. The objective is comparison with the best fixed expert in hindsight. The loss sequence is fixed before interaction, and the learner may randomize.

**Status.** Fully optimal

**TASK tags.** formulation: Online external regret; solution concept: Minimize expected cumulative regret; task family: Online bandit

**MODEL tags.** geometry: Coordinate range; structure: Finite actions

**ORACLE tags.** feedback quality: Exact loss vector; interface family: Full loss vector; operation: Reveal loss vector; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Revealed coordinates; measure: Rounds

## 1. Setting specification

### Task

In each round the learner chooses one of finitely many experts, incurs its loss, and then observes every expert's current loss. The objective is comparison with the best fixed expert in hindsight. The loss sequence is fixed before interaction, and the learner may randomize.

### Admissible model

The hidden loss-vector sequence is $\ell_{1:T}$, with every coordinate in [0,1]. There is no observation noise, and the fixed sequence is independent of the learner's randomness.

The loss-bearing expert $a_t$ is selected before the current loss vector is observed.

The hindsight fixed comparator $i$ uses the same expert throughout all T rounds.

Require $K\ge2$ and $T\ge1$.

Actual actions lie in $[K]$. The learner may select a distribution from the simplex $\Delta_K$ and randomize, but the sampled expert $a_t$ incurs the loss.

### Oracle interface

Full loss-vector feedback:

$$
t,\ a_t\in[K]\ \longmapsto\ (\ell_t(1),\ldots,\ell_t(K))
$$

Choose an action and incur $\ell_t(a_t)$, then receive the complete current loss vector.

All K coordinates are returned, including unselected experts; this is not K independent arm samples.

There is no second hidden loss vector in the round and no access to future rounds.

Public inputs are K, T, and the loss-coordinate range [0,1].

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\ell_t\in[0,1]^K,\quad a_t\in[K],\qquad R_T=\sum_{t=1}^T\ell_t(a_t)-\min_{i\in[K]}\sum_{t=1}^T\ell_t(i)
$$

### Resource accounting

Each round has one feedback event containing $K$ scalars: $KT$ loss coordinates over $T$ rounds.

Any causal randomized policy is allowed. Hedge is a valid upper-bound policy.

Hedge stores $K$ weights. Reading the vector and standard updates require $O(K)$ real operations per round. Arithmetic cost and feedback volume are recorded separately.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}}\sup_{\ell_{1:T}\in([0,1]^K)^T}\mathbb{E}_{\mathcal{A}}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$K$: Number of experts **Domain:** $K\in\mathbb N,\ K\ge2$.

The expert set is $[K]$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$\ell_t$: Hidden loss vector at round t **Domain:** $\ell_t\in[0,1]^K$.

The entire sequence is fixed before interaction; only coordinates allowed by the protocol become visible after acting.

$a_t$: Arm or expert that actually incurs loss in round $t$ **Domain:** $a_t\in[K]$.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$i$: The fixed comparator expert’s index. **Domain:** $i\in[K]$.

A single expert is used throughout the $T$ rounds and chosen in hindsight to minimize cumulative loss.

$\Delta_K$: Probability simplex used for randomized expert selection **Domain:** $\Delta_K\subset\mathbb R^K$.

$\Delta_K=\{p\in[0,1]^K:\sum_i p_i=1\}$.

$\eta$: Learning rate used in the Hedge upper bound **Domain:** Positive real number.

The quantity $\eta=\sqrt{8\log K/T}$ is used only for algorithm tuning.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_t\ell_t(a_t)-\min_{i\in[K]}\sum_t\ell_t(i)$.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\ell_{1:T}\in([0,1]^K)^T}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T\ell_t(a_t)-\min_{i\in[K]}\sum_{t=1}^T\ell_t(i).\end{aligned}
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

The quantity $N=T$ counts complete loss-vector feedback events; the corresponding scalar-coordinate count is KT.

## 3. Complexity bracket

### Compared quantities

#### Q1 - cumulative regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\ell_{1:T}\in([0,1]^K)^T}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T\ell_t(a_t)-\min_{i\in[K]}\sum_{t=1}^T\ell_t(i).\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - MAIN

**Region.** $K\ge 2, T\ge K$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2

$$
0.03 \sqrt{T lnK}
$$

**Upper bound.** B1

$$
\sqrt{T lnK/2}
$$

**Gap or comparison.** ≤1/(0.03sqrt2)

**Comparison argument.** Admit only individually checked claims compatible with this contract.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require $K\ge2$ and $T\ge K$. Select an expert before acting, then observe every current loss afterward.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - Hedge / full-information specialization of Theorem 7

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le\sqrt{T\log K/2}
$$

**Sources.** [1](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T vector reveals

**revealed coordinates.** KT

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [1](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf) theorem: Theorem 7; pdf pages: 12; printed pages: 2796

Set the observation budget $m=T$ in the source's label-efficient full-information theorem. Losses are fixed in advance; expectation is over the learner's private randomness only.

### B2 - Bernoulli expert construction, Yao principle

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge0.03\sqrt{T\log K}
$$

**Sources.** [1](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [1](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf) theorem: Theorem 30 and proof; section: Appendix B; pdf pages: 28; 29; 30; printed pages: 2812; 2813; 2814

Only the full-information experts branch is used, with source sampling budget $m_{\mathrm{src}}=T$. This source parameter is not an objective count, coordinate count, or memory length here. Independent Bernoulli hard instances extend to randomized learners by Yao's principle.

## References

[1] Jean-Yves Audibert; Sébastien Bubeck. Regret Bounds and Minimax Policies under Partial Monitoring. 2010. JMLR 11:2785–2836.

https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf
