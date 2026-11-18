# Adversarial finite-armed bandits with fixed feedback delay and limited tracking capacity

**Setting ID.** `ON_ADV_FIXED_DELAY_CAPACITY`

Online learning and bandits

Play one arm each round against a fixed loss sequence. Only tracked rounds deliver their selected-arm losses after a public fixed delay, and at most C outstanding rounds can be tracked.

**Status.** Fully optimal

**TASK tags.** formulation: Online bandit external regret

**MODEL tags.** stochastic model: Loss range

**ORACLE tags.** feedback quality: Exact selected loss; public information: Hidden objects explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** object: Action trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation

**RESOURCE tags.** measure: Time rounds

## 1. Setting specification

### Task

Minimize the worst-case expected external regret against the best single fixed arm. The learner must act in every round; delayed feedback is conditional on tracking, not on whether an action was played.

### Admissible model

Loss vectors are in $[0,1]^K$, fixed before play and independent of the learner seed. There is no sampling noise. The delay is fixed and known.

### Oracle interface

Before play, an oblivious adversary fixes $(\ell_1,\ldots,\ell_T)$, with $\ell_t\in[0,1]^K$. The common delay $d$ is public.

At round $t$, choose and incur the loss of one arm $a_t\in[K]$, and decide whether to start tracking that round. These choices use earlier delivered feedback and private randomness.

At the end of round $t$, return $(s,\ell_s(a_s))$ for each still-tracked $s$ with $s+d=t$; release delivered slots. A round never tracked gives no feedback. No preemption is needed for the upper bound; this profile uses non-preemptive tracking.

At most $C$ rounds can be tracked at once, including a newly tracked round before that round's deliveries.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_T=\sum_{t=1}^T\ell_t(a_t)-\min_{i\in[K]}\sum_{t=1}^T\ell_t(i),\qquad \ell_t\in[0,1]^K
$$

### Resource accounting

The profile measures regret at a fixed horizon and a fixed simultaneous tracking capacity. It does not bound internal arithmetic or total internal memory.

### Algorithm views and success guarantees

All causal randomized learners and non-preemptive tracking policies satisfying the capacity cap are allowed. The lower bound also holds with preemption.

For each fixed admissible loss table, the upper bound controls $\mathbb E[R_T]$ over learner and tracking randomness. The lower bound concerns the worst fixed table for each allowed policy.

## 2. Notation and parameters

$K$: The finite number of arms. **Domain:** $K\in\mathbb N,\ K\ge2$.

The arm set is $[K]=\{1,\ldots,K\}$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The fixed number of loss-incurring rounds. Fewer than T losses may be observed.

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

$N$: Number of delivered selected-arm feedback values **Domain:** An integer between zero and T.

Let $N$ be the number of tracked feedback values delivered by the end of round $T$. In general $N\le T$, and equality is not required.

$d$: Common delay, public before the game. **Domain:** $d\in\mathbb N,\ 1\le d<T$.

Feedback for round $s$ is delivered at the end of round $s+d$ if still tracked.

$C$: Maximum number of rounds simultaneously tracked. **Domain:** $C\in\mathbb N,\ 2\le C\le d+1$.

The cap counts outstanding tracked rounds, including the newly accepted round before deliveries.

## 3. Complexity bracket

### Compared quantities

#### Q1 - cumulative regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\ell_{1:T}\in([0,1]^K)^T}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T\ell_t(a_t)-\min_{i\in[K]}\sum_{t=1}^T\ell_t(i).\end{aligned}
$$

**Scope.** All causal randomized policies with non-preemptive tracking and the given public parameters; supremum over obliviously fixed loss tables.

**Optimization direction.** minimize

### R1 - Fixed delay with matching capacity bounds

**Region.** $K\ge2$, $d\ge1$, $2\le C\le d+1$, $T\ge2(d+1)$, $K(d+1)\le CT$, and $d\log K\le T$. All inputs are integers; $\log$ is natural.

**Quantity.** Q1

**Resource.** Compare minimax expected regret with horizon T and hard capacity C fixed.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega\!\left(\sqrt{TK(1+d/C)}+\sqrt{Td\log K}\right)
$$

**Upper bound.** B1

$$
O\!\left(\sqrt{TK(1+d/C)}+\sqrt{Td\log K}\right)
$$

**Gap or comparison.** $\Theta\!\left(\sqrt{TK(1+d/C)}+\sqrt{Td\log K}\right)$

**Comparison argument.** Matching up to universal constants for the displayed fixed-delay bandit window.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $K\ge2$, $d\ge1$, $2\le C\le d+1$, $T\ge2(d+1)$, $K(d+1)\le CT$, and $d\log K\le T$. All inputs are integers; $\log$ is natural.

**Oracle mapping.** Exact delayed selected-arm loss conditional on tracking; same fixed table.

**Guarantee mapping.** Worst-case expected external regret; expectation over learner and scheduler randomness.

**Resource mapping.** T rounds and hard capacity C; not a memory lower bound.

### B1 - Delayed FTRL with batch partitioning

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\sqrt{TK(1+d/C)}+\sqrt{Td\log K}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v291/ryabchenko25a.html)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**tracking capacity.** C

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [1](https://proceedings.mlr.press/v291/ryabchenko25a.html) theorem: Theorems 3.1–3.2; Appendix D.1; version: https://arxiv.org/abs/2503.19856v1

### B2 - Label-efficient and fixed-delay reductions

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** all_admissible_algorithms

$$
\Omega\!\left(\sqrt{TK(1+d/C)}+\sqrt{Td\log K}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v291/ryabchenko25a.html)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**tracking capacity.** C

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [1](https://proceedings.mlr.press/v291/ryabchenko25a.html) theorem: Theorem D.5, proof of Theorem 3.2; version: https://arxiv.org/abs/2503.19856v1

## References

[1] Alexander Ryabchenko; Idan Attias; Daniel M. Roy. Capacity-Constrained Online Learning with Delays: Scheduling Frameworks and Regret Trade-offs. 2025.

https://proceedings.mlr.press/v291/ryabchenko25a.html
