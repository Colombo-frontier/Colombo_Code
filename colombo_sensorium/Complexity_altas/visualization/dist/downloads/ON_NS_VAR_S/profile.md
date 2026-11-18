# Nonstationary finite-armed bandits: known variance and variation budgets.

**Setting ID.** `ON_NS_VAR_S`

Online learning and bandits

The learner knows the environment-wide variance and mean-variation budgets and receives one bounded reward from the selected arm each round. The target is dynamic pseudo-regret, allowing zero noise and zero variation. The variance budget sums, over time, the maximum variance among all arms in each round.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Variance aware nonstationary dynamic bandit regret; solution concept: Minimize expected dynamic regret; task family: Online bandit

**MODEL tags.** stochastic model: Mean variation; stochastic model: Nonstationary; stochastic model: Variance budget; structure: Finite actions

**ORACLE tags.** feedback quality: Bounded nonstationary reward; interface family: Selected reward; operation: Sample selected arm; public information: Hidden objects explicitly declared; public information: Known q known v; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** measure: Native feedback; measure: Rounds

## 1. Setting specification

### Task

The learner knows the environment-wide variance and mean-variation budgets and receives one bounded reward from the selected arm each round. The target is dynamic pseudo-regret, allowing zero noise and zero variation. The variance budget sums, over time, the maximum variance among all arms in each round.

### Admissible model

Nonstationary reward distributions $\nu_{t,i}$ are fixed in advance, supported on $[0,1]$, and independent across rounds. Potential rewards of unselected arms within a round need not be independent.

The public environment-variance budget $Q$ constrains $\sum_t\max_i\operatorname{Var}(X_{t,i})$, rather than summing variances only for arms actually selected by the learner.

The public total mean-variation budget $B$ excludes the initial mean vector. It is distinct from a variance budget or the number of best-arm switches.

Require $K\ge2$, $0\le Q\le T/4$, and $0\le B\le T-1$.

The problem is defined at $T=1$, but the source model and theorem start at $T\ge2$. Its conclusion therefore does not cover the one-round endpoint.

Assume $K,T\ge2$, $0\le Q\le T/4$, and $0\le B\le T-1$. The source all-budget theorem is stated only on these ranges. The case $T=1$ can be treated separately as a direct finite problem.

### Oracle interface

The currently selected arm’s bounded random reward:

$$
t,\ a_t\in[K]\ \longmapsto\ Y_t\sim\nu_{t,a_t},\quad\mathbb{E}[Y_t\mid\mathcal{H}_{t-1},a_t]=\mu_{t,a_t},\quad\operatorname{Var}(Y_t\mid\mathcal{H}_{t-1},a_t)=\sigma_{t,a_t}^2
$$

The action is randomized before the current reward is revealed, making the choice and conditional variance predictable in the refined filtration.

Only one selected-arm sample is returned. Arm means and variances are hidden.

Only the budgets $Q,B$ are public; future mean and variance schedules are hidden.

Public inputs: K, T, variance-envelope budget Q, and mean-variation budget B.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\sum_t\max_i\sigma_{t,i}^2\le Q,\quad\sum_{t=2}^T\|\mu_t-\mu_{t-1}\|_\infty\le B,\quad R_T=\sum_t(\max_i\mu_{t,i}-\mu_{t,a_t})
$$

### Resource accounting

T rounds give T bounded reward samples. Q and B are model assumptions, not additional free oracles.

The algorithm knows Q and B. Automatic adaptation to unknown-budget variants is not asserted.

The 2026 upper-bound algorithm uses calibration, screening, clipping, and restarting. Every actual arm pull counts toward T; internal processing does not add native feedback.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}(K,T,Q,B)}\sup_{(\nu_{t,i})\ \mathrm{obeying}\ Q,B}\mathbb{E}_{\mathcal{A},\nu}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$B$: Public budget on total mean variation **Domain:** $0\le B\le T-1$.

$\sum_{t=2}^T\|\mu_t-\mu_{t-1}\|_\infty\le B$.

$K$: The finite number of arms. **Domain:** $K\in\mathbb N,\ K\ge2$.

The arm set is $[K]=\{1,\ldots,K\}$.

$Q$: Public budget on the sum of the maximum arm-reward variance in each round **Domain:** $0\le Q\le T/4$.

Assume $\sum_{t=1}^T\max_i\operatorname{Var}(X_{t,i})\le Q$. The adversary's distributions are fixed in advance, so the variance is the marginal reward variance in each round.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$\nu_{t,i},X_{t,i},\mu_{t,i}$: Reward distributions, latent rewards, and their means. **Domain:** $X_{t,i}\in[0,1],\ \mu_{t,i}\in[0,1]$.

Assume $X_{t,i}\sim\nu_{t,i}$ and $\mu_{t,i}=\mathbb E X_{t,i}$; the distribution schedule is fixed in advance, with independence across rounds.

$\mu_t$: The arm-mean vector in round t. **Domain:** $\mu_t\in[0,1]^K$.

$\mu_t=(\mu_{t,1},\ldots,\mu_{t,K})$.

$a_t$: Arm actually selected in the current round **Domain:** $a_t\in[K]$.

Observe only $X_{t,a_t}$.

$\sigma_{t,i}^2$: The variance of arm i’s reward in round t. **Domain:** $0\le\sigma_{t,i}^2\le1/4$.

$\sigma_{t,i}^2=\operatorname{Var}(X_{t,i})$.

$\Xi(K,T;Q,B)$: Full-budget comparison scale for the known two-budget model **Domain:** A nonnegative real.

$\Xi=\min\{T,K+\sqrt{KQ}+(KQBT)^{1/3}+\sqrt{KT}\min\{B,\sqrt B\}\}$.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

The loss is $R_T=\sum_t(\max_i\mu_{t,i}-\mu_{t,a_t})$. Realized observation noise is excluded from this difference of means. The guarantee separately specifies probability or expectation.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A(K,T,Q,B)}\sup_{\nu\in\mathcal I_{Q,B}}\mathbb E_{\mathcal A,\nu}[R_T],\\ R_T&=\sum_{t=1}^T(\max_{i\in[K]}\mu_{t,i}-\mu_{t,a_t}),\\ \mathcal I_{Q,B}&=\left\{\nu\in\mathcal I:\sum_{t=1}^T\max_i\sigma_{t,i}^2\le Q,\ \sum_{t=2}^T\|\mu_t-\mu_{t-1}\|_\infty\le B\right\}.\end{aligned}
$$

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

$\mathcal I$: The complete environment class in the current minimax objective. **Domain:** Collection of function classes or reward-distribution classes.

The sequence of $[0,1]^K$ reward-vector distributions is fixed before interaction and independent across rounds; different arms within one round may be dependent. The subclass $\mathcal I_{Q,B}$ additionally constrains the sum of the largest per-round arm variances and total mean variation as displayed.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax cumulative dynamic regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A(K,T,Q,B)}\sup_{\nu\in\mathcal I_{Q,B}}\mathbb E_{\mathcal A,\nu}[R_T],\\ R_T&=\sum_{t=1}^T(\max_{i\in[K]}\mu_{t,i}-\mu_{t,a_t}),\\ \mathcal I_{Q,B}&=\left\{\nu\in\mathcal I:\sum_{t=1}^T\max_i\sigma_{t,i}^2\le Q,\ \sum_{t=2}^T\|\mu_t-\mu_{t-1}\|_\infty\le B\right\}.\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - ALL

**Region.** $K,T\ge 2; 0\le Q\le T/4; 0\le B\le T-1$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(\Xi)
$$

**Upper bound.** B1

$$
O(\log(KT)\Xi)
$$

**Gap or comparison.** The ratio is $O(\log(KT))$ for general $Q$ and constant when $Q=0$.

**Comparison argument.** Only individually audited compatible claims enter. New October 2026 extension: statement and applicability reviewed; proof audit pending. Candidates are excluded.

### R2 - ZERO

**Region.** $K,T\ge 2$; $0\le B\le T-1$; $Q=0$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(\Xi(K,T;Q,B))
$$

**Upper bound.** B3

$$
O(\Xi(K,T;0,B))
$$

**Gap or comparison.** Constant ratio

### R3 - NOISY

**Region.** $K,T\ge 2$; $0\le B\le T-1$; $0<Q\le T/4$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(\Xi(K,T;Q,B))
$$

**Upper bound.** B1

$$
O(\log(KT)\Xi(K,T;Q,B))
$$

**Gap or comparison.** O(log(KT))

## 4. Bounds and supporting evidence

### B1 - Calibration, clipping, and hybrid base learner

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\begin{aligned}[c]\mathcal{R}_T^*&\le C\log(KT)\,\Xi(K,T;Q,B),\\ Q=0:\quad\mathcal{R}_T^*&\le C\Xi(K,T;0,B),\\ \Xi(K,T;Q,B)&=\min\left\{T,\ K+\sqrt{KQ}+(KQBT)^{1/3}\right.\\ &\hspace{7em}\left.+\sqrt{KT}\min\{B,\sqrt B\}\right\}.\end{aligned}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.26116)

**Conditions.** Require $K,T\ge2$, $0\le Q\le T/4$, and $0\le B\le T-1$. The algorithm knows $K,T,Q,B$. Each round observes one independent fresh bounded reward from the selected arm.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle correspondence.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee conversion.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output rule.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource conversion.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** one log(KT)

**Source location.** [1](https://arxiv.org/pdf/2610.26116) theorem: Theorem 4.1; Theorem 3.1; pdf pages: 5; 7; printed pages: 4; 6

The source statements and budget conventions have been checked. This profile uses only the explicitly compatible portions of the linked atomic bounds. Lower bounds may transfer by restricting public information; upper bounds with two known budgets do not transfer automatically when less information is available. Full proofs have not been independently reconstructed line by line; this does not alter the recorded status of the source theorems.

### B2 - Fixed oblivious variance/variation constrained hard arrays

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\begin{aligned}[c]\mathcal{R}_T^*&\ge c\,\Xi(K,T;Q,B),\\ \Xi(K,T;Q,B)&=\min\left\{T,\ K+\sqrt{KQ}+(KQBT)^{1/3}\right.\\ &\hspace{7em}\left.+\sqrt{KT}\min\{B,\sqrt B\}\right\}.\end{aligned}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.26116)

**Conditions.** Require $K,T\ge2$, $0\le Q\le T/4$, and $0\le B\le T-1$. The algorithm knows $K,T,Q,B$. Each round observes one independent fresh bounded reward from the selected arm.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle correspondence.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee conversion.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output rule.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource conversion.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2610.26116) theorem: Theorem 4.1; Theorem 3.1; pdf pages: 5; 7; printed pages: 4; 6

The source statements and budget conventions have been checked. This profile uses only the explicitly compatible portions of the linked atomic bounds. Lower bounds may transfer by restricting public information; upper bounds with two known budgets do not transfer automatically when less information is available. Full proofs have not been independently reconstructed line by line; this does not alter the recorded status of the source theorems.

### B3 - Deterministic probing and restarting in the zero-noise model

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
C\min\!\left\{T,K+\sqrt{KT}\min\{B,\sqrt B\}\right\}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.26116)

**Conditions.** Require $K,T\ge2$, $Q=0$, and $0\le B\le T-1$; $K,T,B$ is public before execution.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** The zero-noise upper bound in source Theorem 3.1 holds on every deterministic reward path. The condition $Q=0$ makes every per-round reward distribution degenerate. This deterministic upper bound is recorded separately, preserving its witness type relative to the noisy randomized bound.

**Source location.** [1](https://arxiv.org/pdf/2610.26116) theorem: Theorem3.1

The zero-noise upper bound in source Theorem 3.1 holds on every deterministic reward path. The condition $Q=0$ makes every per-round reward distribution degenerate. This deterministic upper bound is recorded separately, preserving its witness type relative to the noisy randomized bound.

## References

[1] Xiaojin Zhang. Variance-Aware Non-Stationary Bandits: All-Budget Regret Bounds and Adaptation Costs. 2026. 2610.26116v1.

https://arxiv.org/pdf/2610.26116
