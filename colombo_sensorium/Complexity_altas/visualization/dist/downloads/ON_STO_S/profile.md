# Stationary stochastic finite-armed bandits: expected pseudo-regret.

**Setting ID.** `ON_STO_S`

Online learning and bandits

Each arm has a fixed unknown bounded reward distribution and supplies a fresh sample whenever pulled. Performance uses the true means and compares with the best fixed arm. Observation noise is excluded from the comparator definition.

**Status.** Fully optimal

**TASK tags.** formulation: Stochastic bandit pseudo regret; solution concept: Minimize expected cumulative pseudo regret; task family: Online bandit

**MODEL tags.** stochastic model: Iid per arm; stochastic model: Reward range; structure: Finite actions

**ORACLE tags.** feedback quality: Iid bounded reward; interface family: Selected reward; operation: Sample selected arm; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds

## 1. Setting specification

### Task

Each arm has a fixed unknown bounded reward distribution and supplies a fresh sample whenever pulled. Performance uses the true means and compares with the best fixed arm. Observation noise is excluded from the comparator definition.

### Admissible model

Unknown arm distributions $\nu_i$ generate i.i.d. sample streams for each arm, taken mutually independent in this model. The distributions do not change during interaction.

Distribution mean $\mu_i$, which cannot be queried directly

The sampled arm is $a_t$. Repeating an arm still yields a fresh sample.

Assume $K\ge2$ and $T\ge1$. Rewards lie in $[0,1]$ and actions in $[K]$.

This regret model does not require a unique best arm, and gaps are hidden.

### Oracle interface

Fresh reward sample from the selected arm:

$$
t,\ a_t\in[K]\ \longmapsto\ Y_t\mid\mathcal{H}_{t-1},a_t\sim\nu_{a_t}
$$

Select an arm before drawing its fresh reward sample.

The learner cannot observe means $\mu_i$, other arms' same-round rewards, or future samples.

No extra resampling is available within a round; the same arm may be selected and charged again in a later round.

Public inputs are $K,T$ and reward support $[0,1]$. Distributions and means are hidden.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
Y_t\sim\nu_{a_t},\quad \mu_i=\mathbb{E}_{\nu_i}Y,\quad R_T=\sum_{t=1}^T(\mu_* -\mu_{a_t}),\quad \mu_* =\max_i\mu_i
$$

### Resource accounting

One arm pull and one scalar sample per round, under fixed budget T.

Arbitrary causal randomized policies are allowed; MOSS is the admitted upper-bound algorithm.

Maintain arm sample means, counts, and selection indices. These internal operations are charged separately from the T reward samples.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}}\sup_{\nu_1,\ldots,\nu_K\,\mathrm{on}\,[0,1]}\mathbb{E}_{\mathcal{A},\nu}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$K$: The finite number of arms. **Domain:** $K\in\mathbb N,\ K\ge2$.

The arm set is $[K]=\{1,\ldots,K\}$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$\nu_i$: Fixed unknown reward distribution of arm $i$ **Domain:** A probability distribution supported on [0,1].

Each arm pull returns an independent fresh sample from its reward distribution.

$\mu_i,\mu_*$: Arm means and their maximum **Domain:** $\mu_i,\mu_*\in[0,1]$.

$\mu_i=\mathbb E_{Y\sim\nu_i}Y$, $\mu_*=\max_i\mu_i$.

$a_t,Y_t$: The current selected arm and its fresh reward. **Domain:** $a_t\in[K],\ Y_t\in[0,1]$.

Conditionally on the selected arm, $Y_t\sim\nu_{a_t}$.

$X_{t,i}$: Latent arm rewards used to transfer a realized-regret bound to pseudo-regret. **Domain:** $X_{t,i}\in[0,1]$.

The complete latent reward table is used only in the proof. The protocol observes the selected arm only, with no additional feedback.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

The loss is $R_T=\sum_t(\mu_*-\mu_{a_t})$. Realized observation noise is excluded from the loss difference; probability or expectation aggregation is specified separately by the guarantee.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\nu\in\mathcal I}\mathbb E_{\mathcal A,\nu}[R_T],\\ R_T&=\sum_{t=1}^T(\mu_*-\mu_{a_t}),\\ \mu_i&=\mathbb E_{Y\sim\nu_i}Y,\qquad\mu_*=\max_{i\in[K]}\mu_i.\end{aligned}
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

The K reward distributions $\nu=(\nu_1,\ldots,\nu_K)$ are supported on [0,1]. Each pull returns a fresh independent draw from the selected distribution.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax cumulative pseudo regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\nu\in\mathcal I}\mathbb E_{\mathcal A,\nu}[R_T],\\ R_T&=\sum_{t=1}^T(\mu_*-\mu_{a_t}),\\ \mu_i&=\mathbb E_{Y\sim\nu_i}Y,\qquad\mu_*=\max_{i\in[K]}\mu_i.\end{aligned}
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
25\sqrt{KT}
$$

**Gap or comparison.** $\le 625$

**Comparison argument.** Admit only individually checked claims compatible with this contract.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Assume $T\ge K\ge2$. Each arm has a fixed reward distribution on $[0,1]$, and a pull returns an independent fresh sample.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - MOSS

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\mathcal{R}_T^*\le25\sqrt{KT}
$$

**Sources.** [1](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** The source bounds expected realized regret. If $X_{t,i}$ is arm $i$'s reward, then $\mathbb E\max_i\sum_tX_{t,i}\ge\max_i\mathbb E\sum_tX_{t,i}$. Its expected-realized-regret upper bound therefore controls this pseudo-regret. Only this direction of transfer is used.

**Source location.** [1](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf) theorem: Theorem 24, equation (23); pdf pages: 22; printed pages: 2806; equations: (23)

For fixed arm distributions supported on $[0,1]$, the source gives expected realized regret at most $25\sqrt{KT}$. The inequality between expectation and maximization implies the same upper bound for pseudo-regret.

### B2 - Theorem 30 Bernoulli family is itself stationary stochastic

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge0.04\sqrt{KT}
$$

**Sources.** [1](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [1](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf) theorem: Theorem 30 and proof; section: Appendix B; pdf pages: 28; 29; 30; printed pages: 2812; 2813; 2814

Use only the K-armed bandit branch with source sampling budget $m_{\mathrm{src}}=T$. In context-block reductions each block uses its own length. Bernoulli hard instances and Yao's principle give the randomized-learner lower bound.

## References

[1] Jean-Yves Audibert; Sébastien Bubeck. Regret Bounds and Minimax Policies under Partial Monitoring. 2010. JMLR 11:2785–2836.

https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf
