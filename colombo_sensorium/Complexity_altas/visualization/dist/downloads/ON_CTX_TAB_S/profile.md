# Balanced finite-context bandits compared with all lookup-table policies

**Setting ID.** `ON_CTX_TAB_S`

Online learning and bandits

Each round first reveals a discrete context. The learner then selects an arm and observes its loss. The comparator is any fixed mapping from contexts to arms. Context occurrence counts are balanced as required by the model.

**Status.** Fully optimal

**TASK tags.** formulation: Contextual policy regret; solution concept: Minimize expected cumulative policy regret; task family: Online bandit

**MODEL tags.** stochastic model: Bounded loss; structure: Balanced context schedule; structure: Finite actions

**ORACLE tags.** feedback quality: Source-declared exact feedback (may be a random reward); interface family: Selected reward; operation: Observe context then selected arm; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds

## 1. Setting specification

### Task

Each round first reveals a discrete context. The learner then selects an arm and observes its loss. The comparator is any fixed mapping from contexts to arms. Context occurrence counts are balanced as required by the model.

### Admissible model

The context schedule $c_{1:T}$ is public and balanced, with each context appearing $T/S$ times. Contexts are neither random nor adversarially selected during the run.

The current hidden loss vector $\ell_t$ lies in [0,1]^K and is fixed in advance.

The comparator is the best fixed policy $\pi:[S]\to[K]$ in hindsight, assigning one arm to each context, possibly different arms across contexts.

Require $K\ge2$, $S,T\ge1$, and $S\mid T$, with actual action $a_t\in[K]$.

### Oracle interface

Context before the action; selected-arm loss after the action:

$$
c_t\ \longrightarrow\ a_t\in[K]\ \longmapsto\ Y_t=\ell_t(a_t)
$$

The current context is public before action $a_t$. The full cyclic schedule is also a public input.

Losses are hidden before selection; only one scalar for the selected arm is returned afterward.

There is no counterfactual loss feedback for other contexts or second-arm feedback within a round.

Public inputs: K, T, S, and the complete balanced cyclic context schedule, with S dividing T.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
c_t=1+((t-1)\bmod S),\quad R_T=\sum_t\ell_t(a_t)-\min_{\pi:[S]\to[K]}\sum_t\ell_t(\pi(c_t))
$$

### Resource accounting

Each round reveals one context identifier and one selected-arm loss, for T arm-feedback observations in total.

Run a separate bandit algorithm for each of S contexts and update only the current context's state each round.

The upper bound can be implemented with $O(SK)$ arm statistics, without enumerating all $K^S$ comparator policies. This witness's memory use is distinct from the unrestricted algorithm class.

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

$S$: Number of discrete contexts **Domain:** $S\in\mathbb N,\ S\ge1,\ S\mid T$.

$c_t=1+((t-1)\bmod S)$. Each context appears exactly $T/S$ times.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$\ell_t$: Hidden loss vector at round t **Domain:** $\ell_t\in[0,1]^K$.

The entire sequence is fixed before interaction; only coordinates allowed by the protocol become visible after acting.

$a_t$: Arm or expert that actually incurs loss in round $t$ **Domain:** $a_t\in[K]$.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$c_t$: The context revealed before the action in round t. **Domain:** $c_t\in[S]$.

$c_t=1+((t-1)\bmod S)$. The sequence is deterministic and balanced.

$[S],\pi$: Context space and fixed lookup-table policy **Domain:** $[S]=\{1,\ldots,S\},\ \pi:[S]\to[K]$.

The comparator is selected in hindsight from all $K^S$ mappings.

$n$: The effective subhorizon for each context. **Domain:** Positive integer.

Require $n=T/S$. The direct-sum lower bound additionally requires $n\ge K$.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_t\ell_t(a_t)-\min_{\pi:[S]\to[K]}\sum_t\ell_t(\pi(c_t))$.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\ell_{1:T}\in([0,1]^K)^T}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T\ell_t(a_t)-\min_{\pi:[S]\to[K]}\sum_{t=1}^T\ell_t(\pi(c_t)),\\ c_t&=1+((t-1)\bmod S),\qquad S\mid T.\end{aligned}
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

#### Q1 - minimax cumulative policy regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\ell_{1:T}\in([0,1]^K)^T}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T\ell_t(a_t)-\min_{\pi:[S]\to[K]}\sum_{t=1}^T\ell_t(\pi(c_t)),\\ c_t&=1+((t-1)\bmod S),\qquad S\mid T.\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - MAIN

**Region.** S divides T, T≥KS

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2

$$
0.04\sqrt{KST}
$$

**Upper bound.** B1

$$
4\sqrt{KST}+S
$$

**Gap or comparison.** Controlled by universal constants, using $S\le\sqrt{KST}$.

**Comparison argument.** Admit only individually checked claims compatible with this contract.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The $S$ contexts occur equally often; require $S\mid T$ and $T\ge KS$. The comparator is one fixed mapping from all contexts to arms.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - One Tsallis-INF learner per context

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le4\sqrt{KST}+S
$$

**Sources.** [1](https://jmlr.org/papers/volume22/19-753/19-753.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Each context occurs $T/S$ times. Running Tsallis-INF separately for each context gives the bound $4\sqrt{KT/S}+1$ per context. The best context-to-arm mapping decomposes by context, so the regrets of the $S$ independent algorithm states can be summed.

**Source location.** [1](https://jmlr.org/papers/volume22/19-753/19-753.pdf) theorem: Theorem 1, IW case; pdf pages: 9

Tsallis-INF has adversarial bandit pseudo-regret at most $4\sqrt{KT}+1$. For a deterministic loss sequence fixed before interaction, this equals expected realized external regret.

### B2 - S independent finite-bandit Bernoulli hard instances

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge0.04\sqrt{KST}
$$

**Sources.** [2](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Each context appears $n=T/S\ge K$ times. Choose hard optimal arms independently across contexts so other-context observations reveal no information about that identity. Summing block lower bounds gives $0.04S\sqrt{Kn}$. Averaging over the loss table sampled in advance yields an oblivious sequence lower bound.

**Source location.** [2](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf) theorem: Theorem 30 and proof; section: Appendix B; pdf pages: 28; 29; 30; printed pages: 2812; 2813; 2814

Use only the K-armed bandit branch with source sampling budget $m_{\mathrm{src}}=T$. In context-block reductions each block uses its own length. Bernoulli hard instances and Yao's principle give the randomized-learner lower bound.

## References

[1] Julian Zimmert; Yevgeny Seldin. Tsallis-INF: An Optimal Algorithm for Stochastic and Adversarial Bandits. 2021. JMLR 22(28):1–49.

https://jmlr.org/papers/volume22/19-753/19-753.pdf

[2] Jean-Yves Audibert; Sébastien Bubeck. Regret Bounds and Minimax Policies under Partial Monitoring. 2010. JMLR 11:2785–2836.

https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf
