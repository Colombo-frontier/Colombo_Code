# Adversarial finite-armed bandits: selected-arm feedback and external regret

**Setting ID.** `ON_ADV_S`

Online learning and bandits

The environment fixes all arms' losses before interaction, and each round reveals only the chosen arm's loss. The target is worst-case expected external regret over all causal randomized strategies.

**Status.** Fully optimal

**TASK tags.** formulation: Online bandit external regret; solution concept: Minimize expected cumulative regret; task family: Online bandit

**MODEL tags.** stochastic model: Loss range; structure: Finite actions

**ORACLE tags.** feedback quality: Exact selected loss; interface family: Selected reward; operation: Sample selected arm; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds

## 1. Setting specification

### Task

The environment fixes all arms' losses before interaction, and each round reveals only the chosen arm's loss. The target is worst-case expected external regret over all causal randomized strategies.

### Admissible model

The hidden loss sequence $\ell_{1:T}$ is fixed before interaction, with every coordinate in $[0,1]$.

The current arm is $a_t$, chosen without knowing $\ell$_t.

The hindsight fixed-arm comparator is $i$, not the best arm chosen separately each round.

Require $K\ge2$ and $T\ge1$, with actual action $a_t\in[K]$.

### Oracle interface

The selected arm’s exact loss:

$$
t,\ a_t\in[K]\ \longmapsto\ Y_t=\ell_t(a_t)
$$

Only one scalar is returned; rewards of unselected arms are not observed.

The response is the exact selected entry of a loss table fixed in advance, not a fresh random reward from a fixed arm distribution.

Only one loss-incurring arm may be selected per round; no additional free probes are available.

Public inputs are K, T, and the loss-coordinate range [0,1].

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_T=\sum_{t=1}^T\ell_t(a_t)-\min_{i\in[K]}\sum_{t=1}^T\ell_t(i),\qquad \ell_t\in[0,1]^K
$$

### Resource accounting

One selected-arm response per round, for $T$ scalar observations.

Arbitrary causal randomized policies; Tsallis-INF supplies an available upper bound.

Importance weighting, weight updates, and probability sampling are internal computation. Solving a regularized subproblem is not treated as a single feedback operation.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}}\sup_{\ell_{1:T}}\mathbb{E}_{\mathcal{A}}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$K$: The finite number of arms. **Domain:** $K\in\mathbb N,\ K\ge2$.

The arm set is $[K]=\{1,\ldots,K\}$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$\ell_t$: Hidden loss vector at round t **Domain:** $\ell_t\in[0,1]^K$.

The entire sequence is fixed before interaction; only coordinates allowed by the protocol become visible after acting.

$a_t$: Arm or expert that actually incurs loss in round $t$ **Domain:** $a_t\in[K]$.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$i$: Comparator arm fixed over the entire horizon **Domain:** $i\in[K]$.

$Y_t$: Exact loss observed in the current round **Domain:** $Y_t\in[0,1]$.

$Y_t=\ell_t(a_t)$.

$\alpha,\eta_t$: The Tsallis-INF regularization exponent and round-t learning rate. **Domain:** Algorithm-tuning parameter.

The quantities $\alpha=1/2$ and $\eta_t=2/\sqrt t$ are not curvature or statistical-confidence parameters.

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

The quantity $N=T$ counts cumulative native scalar feedback under a one-point or one-arm protocol.

## 3. Complexity bracket

### Compared quantities

#### Q1 - cumulative regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\ell_{1:T}\in([0,1]^K)^T}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T\ell_t(a_t)-\min_{i\in[K]}\sum_{t=1}^T\ell_t(i).\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - MAIN

**Region.** $T\ge K\ge 2$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2

$$
0.04\sqrt{KT}
$$

**Upper bound.** B1

$$
4\sqrt{KT}+1
$$

**Gap or comparison.** Controlled by universal constants for $T\ge K\ge2$

**Comparison argument.** Admit only individually checked claims compatible with this contract.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require $T\ge K\ge2$. The loss sequence is precommitted, and each round reveals only the selected arm’s loss.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - Tsallis-INF, IW estimators

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le4\sqrt{KT}+1
$$

**Sources.** [1](https://jmlr.org/papers/volume22/19-753/19-753.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [1](https://jmlr.org/papers/volume22/19-753/19-753.pdf) theorem: Theorem 1, IW case; pdf pages: 9

Tsallis-INF has adversarial bandit pseudo-regret at most $4\sqrt{KT}+1$. For a deterministic loss sequence fixed before interaction, this equals expected realized external regret.

### B2 - i.i.d. Bernoulli hard distribution implies an oblivious deterministic-sequence witness

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

**Source location.** [2](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf) theorem: Theorem 30 and proof; section: Appendix B; pdf pages: 28; 29; 30; printed pages: 2812; 2813; 2814

Use only the K-armed bandit branch with source sampling budget $m_{\mathrm{src}}=T$. In context-block reductions each block uses its own length. Bernoulli hard instances and Yao's principle give the randomized-learner lower bound.

## References

[1] Julian Zimmert; Yevgeny Seldin. Tsallis-INF: An Optimal Algorithm for Stochastic and Adversarial Bandits. 2021. JMLR 22(28):1–49.

https://jmlr.org/papers/volume22/19-753/19-753.pdf

[2] Jean-Yves Audibert; Sébastien Bubeck. Regret Bounds and Minimax Policies under Partial Monitoring. 2010. JMLR 11:2785–2836.

https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf
