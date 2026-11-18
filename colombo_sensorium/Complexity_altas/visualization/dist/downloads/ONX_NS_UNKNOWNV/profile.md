# Nonstationary finite-armed bandits: unknown mean-variation budget.

**Setting ID.** `ONX_NS_UNKNOWNV`

Online learning and bandits

A fixed sequence of bounded reward distributions may vary over time, and the learner observes only the selected arm's reward. One algorithm must adapt to every undisclosed budget; performance is evaluated using the actual environment's variance and mean variation. Different levels of budget knowledge cannot be interchanged.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Onx ns unknownv; task family: Online bandit

**MODEL tags.** stochastic model: Nonstationary; structure: Finite actions

**ORACLE tags.** interface family: Selected reward; operation: Selected reward; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; public information: Unknown variation

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

A fixed sequence of bounded reward distributions may vary over time, and the learner observes only the selected arm's reward. One algorithm must adapt to every undisclosed budget; performance is evaluated using the actual environment's variance and mean variation. Different levels of budget knowledge cannot be interchanged.

### Admissible model

There are $K$ arms, with rewards in $[0,1]$, independent across rounds. All reward distributions and their unknown means $\mu_{t,i}$ are fixed before interaction. Total mean drift is defined by:

$$
V_\mu=\sum_{t=2}^{T}\|\mu_t-\mu_{t-1}\|_\infty,\qquad \mu_t=(\mu_{t,1},\ldots,\mu_{t,K}).
$$

### Oracle interface

Each round selects one arm $I_t$ and receives only that arm's reward.

The data $K,T$ are public. The quantity $V_\mu$, means, and change locations are hidden. No nontrivial upper bound on actual drift is supplied.

The common causal policy may use neither $V_\mu$ nor a nontrivial upper bound on it as input.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\mathbb{E}\!\left[\sum_{t=1}^{T}\left(\max_{1\le i\le K}\mu_{t,i}-\mu_{t,I_t}\right)\right].
$$

### Resource accounting

$$
N=T\quad\text{\text{reward observations}}.
$$

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

One policy must adapt to every possible realized total drift. When taking the worst case over environments at each drift level, the policy cannot be retuned to that level. Expectation includes rewards and algorithm randomness.

## 2. Notation and parameters

$K$: The finite number of arms. **Domain:** $K\in\mathbb N,\ K\ge2$.

The arm set is $[K]=\{1,\ldots,K\}$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$V$: The total mean-variation budget used for evaluation by budget slice. **Domain:** $0\le V\le T-1$.

The actual drift satisfies $V_\mu\le V$, but $V$ is hidden. One policy serves every budget slice.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$\nu_{t,i},X_{t,i},\mu_{t,i}$: Reward distributions, latent rewards, and their means. **Domain:** $X_{t,i}\in[0,1],\ \mu_{t,i}\in[0,1]$.

Assume $\mu_{t,i}=\mathbb E X_{t,i}$; per-round distributions are fixed in advance, with independent sampling across rounds.

$\mu_t,V_\mu$: Mean vector at round $t$ and its realized total variation **Domain:** Vector and nonnegative real number.

$\mu_t=(\mu_{t,i})_{i=1}^K$, $V_\mu=\sum_{t=2}^T\|\mu_t-\mu_{t-1}\|_\infty$.

$I_t$: Arm actually selected in the current round **Domain:** $I_t\in[K]$.

Only $X_{t,I_t}$ is observed; rewards of unselected arms remain hidden.

$\delta_{\mathrm{conf}}$: The internal failure probability used to convert the MASTER bound to expectation. **Domain:** Tuning parameter used in the proof.

Choose $T^{-2}$. The one-round endpoint is handled directly by regret at most T.

$c_1,c_2$: Coefficient of the UCB1 base learner in the MASTER reduction **Domain:** Used only in the derivation of this upper bound.

The quantities $c_1\asymp\sqrt K$ and $c_2\asymp K$ are not hidden environmental parameters.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

The loss is $R_T=\sum_t[\max_i\mu_{t,i}-\mu_{t,I_t}]$. Realized observation noise is excluded from this difference of means. The guarantee separately specifies probability or expectation.

$\mathcal R_T^*$: Worst-case expected-regret comparison under the same budget slice and information restrictions **Domain:** A nonnegative real.

The upper bound for an unknown budget must be attained by one policy that does not receive that budget. The lower bound applies to every such policy. Different algorithms cannot be chosen retrospectively for different hidden budgets.

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
\mathbb E\!\left[\sum_{t=1}^{T}\left(\max_{1\le i\le K}\mu_{t,i}-\mu_{t,I_t}\right)\right].
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - MAIN

**Region.** Assume $T\ge K\ge2$ and $\max\{1/K,\sqrt{K/T}\}\le V\le T/K$. Evaluate performance in strata indexed by $V_\mu\le V$; the algorithm does not know $V$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega((KV_\mu)^{1/3}T^{2/3})
$$

**Upper bound.** B1

$$
\widetilde{O}((KV_\mu)^{1/3}T^{2/3})
$$

**Gap or comparison.** Logarithmic factors; the same policy adapts to every $V$.

## 4. Bounds and supporting evidence

### B1 - MASTER + UCB1

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}\!\left(\min\{T,\sqrt{KT}+(KV_\mu)^{1/3}T^{2/3}\}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v134/wei21b.html)

**Conditions.** Require $K\ge2$ and $T\ge1$, with rewards in $[0,1]$. The strategy uses only the public $K,T$ and need not know the actual variation $V_\mu$.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** Only the logarithms in $\widetilde O$ are suppressed; see the evidence record.

**Derivation.** Insert UCB1 coefficients $c_1\asymp\sqrt K$ and $c_2\asymp K$ into MASTER Theorem 2. Choose failure probability $T^{-2}$ and use $0\le R_T\le T$ for the expectation bound; cap endpoints by $T$. The same policy handles all realized variations $V_\mu$ without taking variation as input.

**Source location.** [1](https://proceedings.mlr.press/v134/wei21b.html) theorem: Theorem 2 and Appendix I.1

Insert UCB1 coefficients $c_1\asymp\sqrt K$ and $c_2\asymp K$ into MASTER Theorem 2. Choose failure probability $T^{-2}$ and use $0\le R_T\le T$ for the expectation bound; cap endpoints by $T$. The same policy handles all realized variations $V_\mu$ without taking variation as input.

### B2 - Independent Bernoulli block environments

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge c(KV)^{1/3}T^{2/3}
$$

**Sources.** [2](https://arxiv.org/pdf/1405.3316v2)

**Conditions.** Require $T\ge K\ge2$ and $\max\{1/K,\sqrt{K/T}\}\le V\le T/K$. Total mean variation excludes the initial mean vector. The comparator is the best current arm in each round.; The lower bound does not require disclosure of the variation budget. Hard instances are still selected separately for each budget region.

**Dimension conditions.** Dimension and horizon must satisfy the stated regime. The source's large-dimension and asymptotic conditions are retained.

**Oracle correspondence.** Preserve the specified current-round feedback, sample coupling, and response timing.

**Guarantee conversion.** Retain the stated cumulative regret, error probability, stopping time, or error exponent. Any necessary transfer is explicit in the derivation.

**Output rule.** The output is the action trajectory or recommendation required by the objective.

**Resource conversion.** No free samples or additional queries to past rounds are introduced.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** A lower bound for all causal randomized policies in the stronger model with public variation budget $V$ also applies when the budget is hidden. The transfer preserves the original theorem's full parameter window.

**Source location.** [2](https://arxiv.org/pdf/1405.3316v2) theorem: Theorem 1; pdf pages: 9

Bernoulli hard rewards yield $c(KV)^{1/3}T^{2/3}$ on window $V\in[1/K,T/K]$. Variation excludes the initial mean vector, and the comparator is the best arm in each round.

## References

[1] Chen-Yu Wei; Haipeng Luo. Non-stationary Reinforcement Learning without Prior Knowledge: an Optimal Black-box Approach. 2021. COLT2021, PMLR134:4300–4354.

https://proceedings.mlr.press/v134/wei21b.html

[2] Omar Besbes; Yonatan Gur; Assaf Zeevi. Optimal Exploration–Exploitation in a Multi-Armed-Bandit Problem with Non-Stationary Rewards. 2019. arXiv:1405.3316v2, 2019-06-06; manuscript dated 2019-04-04; Stochastic Systems 2019.

https://arxiv.org/pdf/1405.3316v2
