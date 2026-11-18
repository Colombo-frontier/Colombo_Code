# Nonstationary bandits: known variance budget and unknown variation budget.

**Setting ID.** `ONX_NS_VAR_QKNOWN_VUNKNOWN`

Online learning and bandits

A fixed sequence of bounded reward distributions may vary over time, and the learner observes only the selected arm's reward. One algorithm must adapt to every undisclosed budget; performance is evaluated using the actual environment's variance and mean variation. Different levels of budget knowledge cannot be interchanged.

**Status.** Other quantified gap present

**TASK tags.** formulation: Onx ns var qknown vunknown; task family: Online bandit

**MODEL tags.** stochastic model: Nonstationary; structure: Finite actions

**ORACLE tags.** interface family: Selected reward; operation: Selected reward; public information: Hidden objects explicitly declared; public information: Known q unknown v; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

A fixed sequence of bounded reward distributions may vary over time, and the learner observes only the selected arm's reward. One algorithm must adapt to every undisclosed budget; performance is evaluated using the actual environment's variance and mean variation. Different levels of budget knowledge cannot be interchanged.

### Admissible model

There are $K\ge2$ arms. All arm reward distributions $\nu_{t,i}$ are fixed before interaction, supported on $[0,1]$, and sampled independently across rounds. Write the means as $\mu_{t,i}=\mathbb{E} X_{t,i}$ and mean vectors as $\mu_t$.

$$
V_\mu=\sum_{t=2}^{T}\|\mu_t-\mu_{t-1}\|_\infty,\qquad Q_{\mathrm{env}}=\sum_{t=1}^{T}\max_{1\le i\le K}\operatorname{Var}(X_{t,i})\le\frac T4.
$$

The quantity $Q_{\mathrm{env}}$ sums the largest arm variance in each round. It is neither the sum of selected-arm variances nor the sum over all arms.

### Oracle interface

The algorithm chooses arm $I_t$ before receiving one reward $X_{t,I_t}$. Noise may be heteroscedastic or zero. Reward distributions may change across rounds even when their means remain constant.

The arm count $K$, horizon $T$, and variance-budget upper bound $Q$ are public, with $Q_{\mathrm{env}}\le Q$.

Arm-by-round variances, means, and change locations are hidden, as is the drift budget $V$.

The algorithm must be causal and cannot depend on unavailable budgets. One policy must work simultaneously across all such unknown-budget classes.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\mathbb{E}\!\left[\sum_{t=1}^{T}\left(\max_{1\le i\le K}\mu_{t,i}-\mu_{t,I_t}\right)\right].
$$

### Resource accounting

$$
N=T\quad\text{\text{selected-arm rewards}}.
$$

The sharp general frontier for this combination of information permissions remains unresolved. Formulas assuming both budgets known cannot be transferred directly.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

The algorithm must be causal and cannot depend on unavailable budgets. One policy must work simultaneously across all such unknown-budget classes.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

The criterion is expected dynamic pseudo-regret, averaging over rewards and algorithm randomness. Adaptation to an unknown budget uses one algorithm evaluated after the run at the realized budget; it cannot be replaced retrospectively by a budget-aware policy.

## 2. Notation and parameters

$K$: The finite number of arms. **Domain:** $K\in\mathbb N,\ K\ge2$.

The arm set is $[K]=\{1,\ldots,K\}$.

$Q$: Budget for the sum of per-round maximum arm-reward variances **Domain:** $0\le Q\le T/4$.

$Q_{\mathrm{env}}=\sum_{t=1}^T\max_i\operatorname{Var}(X_{t,i})\le Q$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$V$: The total mean-variation budget. **Domain:** $0\le V\le T-1$.

$V_\mu=\sum_{t=2}^T\|\mu_t-\mu_{t-1}\|_\infty\le V$.

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

$Q_{\mathrm{env}}$: The sum over rounds of the actual maximum arm variance. **Domain:** $0\le Q_{\mathrm{env}}\le T/4$.

$Q_{\mathrm{env}}=\sum_t\max_i\operatorname{Var}(X_{t,i})$.

$\Xi(K,T;Q,V)$: The known-budget lower-bound scale on a budget slice. **Domain:** A nonnegative real.

$\Xi=\min\{T,K+\sqrt{KQ}+(KQVT)^{1/3}+\sqrt{KT}\min\{V,\sqrt V\}\}$. The source denotes the variation budget here called $V$ by $B$.

$U(K,T;V)$: Leading adaptive upper-bound term that ignores small-variance structure **Domain:** Positive real number.

$U=\min\{T,\sqrt{KT}+(KV)^{1/3}T^{2/3}\}$. The source polylogarithmic factors are listed separately.

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

### R1 - ALL

**Region.** Assume $K,T\ge2$, $0\le Q\le T/4$, and $0\le V\le T-1$. Hidden budgets stratify evaluation while the algorithm remains fixed.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Other quantified gap

**Lower bound.** B2

$$
\Omega(\Xi(K,T;Q,V))
$$

**Upper bound.** B1

$$
\widetilde{O}(\min\{T,\sqrt{KT}+(KB)^{1/3}T^{2/3}\})
$$

**Gap or comparison.** $\widetilde O\!\left(\frac{\min\{T,\sqrt{KT}+(KV)^{1/3}T^{2/3}\}}{\Xi(K,T;Q,V)}\right)$, on the same budget slice $V_\mu\le V, Q_{\mathrm{env}}\le Q$. Only the polylogarithmic factors in the source upper bound are suppressed.

## 4. Bounds and supporting evidence

### B1 - MASTER + UCB1

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}\!\left(\min\{T,\sqrt{KT}+(KV_\mu)^{1/3}T^{2/3}\}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v134/wei21b.html)

**Conditions.** Require $K\ge2$ and $T\ge1$, with rewards in $[0,1]$. The algorithm uses only $K,T$ and is therefore admissible whether the current budget is public or hidden. Evaluate the displayed bound on the stated budget region.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** Only the logarithms in $\widetilde O$ are suppressed; see the evidence record.

**Derivation.** MASTER uses neither the variance budget $Q$ nor the variation budget $V$, so it also applies when only some of these parameters are public. This bound does not exploit the additional small-noise structure described by the variance budget.

**Source location.** [1](https://proceedings.mlr.press/v134/wei21b.html) theorem: Theorem 2 and Appendix I.1

Insert UCB1 coefficients $c_1\asymp\sqrt K$ and $c_2\asymp K$ into MASTER Theorem 2. Choose failure probability $T^{-2}$ and use $0\le R_T\le T$ for the expectation bound; cap endpoints by $T$. The same policy handles all realized variations $V_\mu$ without taking variation as input.

### B2 - Fixed oblivious variance/variation constrained hard arrays

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\begin{aligned}[c]\mathcal{R}_T^*&\ge c\,\Xi(K,T;Q,V),\\ \Xi(K,T;Q,V)&=\min\left\{T,\ K+\sqrt{KQ}+(KQVT)^{1/3}\right.\\ &\hspace{7em}\left.+\sqrt{KT}\min\{V,\sqrt V\}\right\}.\end{aligned}
$$

**Sources.** [2](https://arxiv.org/pdf/2610.26116)

**Conditions.** The environment satisfies $K,T\ge2$, $0\le Q\le T/4$, and $0\le V\le T-1$. Each selected arm returns one independent fresh bounded sample per round.; The source lower bound holds even with $Q,V$ all public. Hiding some budgets only reduces the information available to the present algorithm class, so the bound remains valid.

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

**Derivation.** The source lower bound holds even when $Q,V$ are all public, so it also constrains the present algorithm class with only partial budget knowledge. Environment budgets and independent per-round observations remain unchanged.

**Source location.** [2](https://arxiv.org/pdf/2610.26116) theorem: Theorem 4.1; Theorem 3.1; pdf pages: 5; 7; printed pages: 4; 6

The source statements and budget conventions have been checked. This profile uses only the explicitly compatible portions of the linked atomic bounds. Lower bounds may transfer by restricting public information; upper bounds with two known budgets do not transfer automatically when less information is available. Full proofs have not been independently reconstructed line by line; this does not alter the recorded status of the source theorems.

## References

[1] Chen-Yu Wei; Haipeng Luo. Non-stationary Reinforcement Learning without Prior Knowledge: an Optimal Black-box Approach. 2021. COLT2021, PMLR134:4300–4354.

https://proceedings.mlr.press/v134/wei21b.html

[2] Xiaojin Zhang. Variance-Aware Non-Stationary Bandits: All-Budget Regret Bounds and Adaptation Costs. 2026. 2610.26116v1.

https://arxiv.org/pdf/2610.26116
