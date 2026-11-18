# Nonstationary finite-armed bandits with a known mean-variation budget

**Setting ID.** `ON_NS_S`

Online learning and bandits

Arm reward distributions may change over time, but total mean variation has a known upper bound. The learner samples one arm per round and competes with that round's best mean arm. The variation budget constrains the environment and is not a comparator-path-length bound.

**Status.** Fully optimal

**TASK tags.** formulation: Nonstationary dynamic bandit regret; solution concept: Minimize expected dynamic regret; task family: Online bandit

**MODEL tags.** stochastic model: Bounded independent rewards; stochastic model: Mean variation; stochastic model: Nonstationary; structure: Finite actions

**ORACLE tags.** feedback quality: Independent nonstationary bounded reward; interface family: Selected reward; operation: Sample selected arm; public information: Hidden objects explicitly declared; public information: Known variation; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** measure: Native feedback; measure: Rounds

## 1. Setting specification

### Task

Arm reward distributions may change over time, but total mean variation has a known upper bound. The learner samples one arm per round and competes with that round's best mean arm. The variation budget constrains the environment and is not a comparator-path-length bound.

### Admissible model

Reward distributions $\nu_{t,i}$ depend on time and are fixed before interaction. They are supported on $[0,1]$ and need not be identically distributed over time.

For the arm means $\mu_t$, total variation sums infinity-norm differences of successive mean vectors from $t=2$. The initial mean vector is not charged.

The public total mean-variation budget $V$ is neither the variation of a realized observation path nor the number of best-arm switches.

Require $K\ge2$, $T\ge1$, and $0\le V\le T-1$, with actions in $[K]$.

The classical matching region has additional restrictions. The endpoint V = 0 and other boundaries have separate applicability records.

### Oracle interface

Fresh reward from the currently selected arm:

$$
t,\ a_t\in[K]\ \longmapsto\ Y_t\mid\mathcal{H}_{t-1},a_t\sim\nu_{t,a_t}
$$

Only one $[0,1]$-valued sample from the currently selected arm is observed.

An arm's distribution may change in the next round and cannot be treated as repeated sampling from a fixed distribution $\nu_i$.

The native model fixes the mean schedule. This specification does not extend to environments adapting to learner history.

Public inputs: $K$, $T$, and the total mean-variation bound $V$.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\sum_{t=2}^T\|\mu_t-\mu_{t-1}\|_\infty\le V,\qquad R_T=\sum_t(\max_i\mu_{t,i}-\mu_{t,a_t})
$$

### Resource accounting

A fixed number $T$ of arm pulls, with one reward sample per round.

The public V may be used to restart a base bandit policy. Restarts do not create additional reward queries.

Restart length, arm-weight maintenance, and sampling are internal computation. Adaptation to unknown V requires a different information specification.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}(K,T,V)}\sup_{(\nu_{t,i}):\ \mathrm{VarPath}(\mu)\le V}\mathbb{E}_{\mathcal{A},\nu}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$K$: The finite number of arms. **Domain:** $K\in\mathbb N,\ K\ge2$.

The arm set is $[K]=\{1,\ldots,K\}$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$V$: Public budget on total mean variation **Domain:** $0\le V\le T-1$.

$\sum_{t=2}^T\|\mu_t-\mu_{t-1}\|_\infty\le V$. The initial mean is excluded; this is not sample-path variation.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$\nu_{t,i},X_{t,i},\mu_{t,i}$: Reward distributions, latent rewards, and their means. **Domain:** $X_{t,i}\in[0,1],\ \mu_{t,i}\in[0,1]$.

Assume $X_{t,i}\sim\nu_{t,i}$ and $\mu_{t,i}=\mathbb E X_{t,i}$; the distribution schedule is fixed in advance, with independence across rounds.

$\mu_t$: The arm-mean vector in round t. **Domain:** $\mu_t\in[0,1]^K$.

$\mu_t=(\mu_{t,1},\ldots,\mu_{t,K})$.

$a_t$: Arm actually selected in the current round **Domain:** $a_t\in[K]$.

Observe only $X_{t,a_t}$.

$\operatorname{VarPath}(\mu)$: Total variation of the actual consecutive mean vectors. **Domain:** A nonnegative real.

$\sum_{t=2}^T\|\mu_t-\mu_{t-1}\|_\infty$.

$H,I,V_I$: Restart-block length, a contiguous block of rounds, and mean variation within that block **Domain:** Used only in the upper-bound derivation.

Use $H\asymp K^{1/3}(T/V)^{2/3}$, rounded and clipped to [1,T]; $V_I=\sum_{t,t-1\in I}\|\mu_t-\mu_{t-1}\|_\infty$.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

The loss is $R_T=\sum_t(\max_i\mu_{t,i}-\mu_{t,a_t})$. Realized observation noise is excluded from this difference of means. The guarantee separately specifies probability or expectation.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A(K,T,V)}\sup_{\nu\in\mathcal I_V}\mathbb E_{\mathcal A,\nu}[R_T],\\ R_T&=\sum_{t=1}^T(\max_{i\in[K]}\mu_{t,i}-\mu_{t,a_t}),\\ \mathcal I_V&=\left\{\nu\in\mathcal I:\sum_{t=2}^T\|\mu_t-\mu_{t-1}\|_\infty\le V\right\}.\end{aligned}
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

Before interaction, the environment fixes a sequence of bounded reward distributions. Every arm’s rewards lie in [0,1], with independent fresh samples across rounds. The subclass $\mathcal I_V$ additionally bounds total mean variation by V.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax cumulative dynamic regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A(K,T,V)}\sup_{\nu\in\mathcal I_V}\mathbb E_{\mathcal A,\nu}[R_T],\\ R_T&=\sum_{t=1}^T(\max_{i\in[K]}\mu_{t,i}-\mu_{t,a_t}),\\ \mathcal I_V&=\left\{\nu\in\mathcal I:\sum_{t=2}^T\|\mu_t-\mu_{t-1}\|_\infty\le V\right\}.\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - MAIN

**Region.** $T\ge K\ge 2; \max{1/K,\sqrt{K/T}}\le V\le T/K$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2

$$
c(KV)^{1/3}T^{2/3}
$$

**Upper bound.** B1

$$
C(KV)^{1/3}T^{2/3}
$$

**Gap or comparison.** Controlled by universal constants within the stated range of $V$

**Comparison argument.** Admit only individually checked claims compatible with this contract.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require $T\ge K\ge2$ and $\max\{1/K,\sqrt{K/T}\}\le V\le T/K$. Total mean variation excludes the initial mean vector. The comparator is the best current arm in each round.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - Restart Tsallis-INF in blocks of length H

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le C(KV)^{1/3}T^{2/3}
$$

**Sources.** [1](https://jmlr.org/papers/volume22/19-753/19-753.pdf) [2](https://arxiv.org/pdf/1405.3316v2)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** For each interval $I$ of length approximately $H$, dynamic regret is bounded by static regret plus $2|I|V_I$, where $V_I$ is within-interval mean variation. Restarting Tsallis-INF gives total static contribution $O(T\sqrt{K/H}+\sqrt{KH})$ and drift contribution at most $2HV$. Choose $H\asymp K^{1/3}(T/V)^{2/3}$ and clip it to $[1,T]$. In this region, $V\ge\sqrt{K/T}$ makes the target term dominate the stationary term, while $V\le T/K$ ensures $H\ge K$. The result is $O((KV)^{1/3}T^{2/3})$.

**Source location.** [2](https://arxiv.org/pdf/1405.3316v2) theorem: Theorem 2 and Remark 1; pdf pages: 11

Rexp3 gives $C(K\log K\,V)^{1/3}T^{2/3}$ on the window $V\in[1/K,T/K]$. Replacing its base learner by INF removes $\log K$. A direct restarted Tsallis-INF regret decomposition is included separately.

**Source location.** [1](https://jmlr.org/papers/volume22/19-753/19-753.pdf) theorem: Theorem 1, IW case; pdf pages: 9

Tsallis-INF has adversarial bandit pseudo-regret at most $4\sqrt{KT}+1$. For a deterministic loss sequence fixed before interaction, this equals expected realized external regret.

### B2 - Independent Bernoulli block environments

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge c(KV)^{1/3}T^{2/3}
$$

**Sources.** [2](https://arxiv.org/pdf/1405.3316v2)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [2](https://arxiv.org/pdf/1405.3316v2) theorem: Theorem 1; pdf pages: 9

Bernoulli hard rewards yield $c(KV)^{1/3}T^{2/3}$ on window $V\in[1/K,T/K]$. Variation excludes the initial mean vector, and the comparator is the best arm in each round.

## References

[1] Julian Zimmert; Yevgeny Seldin. Tsallis-INF: An Optimal Algorithm for Stochastic and Adversarial Bandits. 2021. JMLR 22(28):1–49.

https://jmlr.org/papers/volume22/19-753/19-753.pdf

[2] Omar Besbes; Yonatan Gur; Assaf Zeevi. Optimal Exploration–Exploitation in a Multi-Armed-Bandit Problem with Non-Stationary Rewards. 2019. arXiv:1405.3316v2, 2019-06-06; manuscript dated 2019-04-04; Stochastic Systems 2019.

https://arxiv.org/pdf/1405.3316v2
