# Multitask linear contextual bandits with a shared low-rank representation

**Setting ID.** `ONX_MULTI_CONTEXTUAL`

Online learning and bandits

Multiple linear bandit tasks share an unknown low-dimensional representation. All task actions must be submitted together before the batch of scalar rewards is revealed. Performance is the sum of cumulative pseudo-regret across tasks. Each task’s predictable action set may change over time.

**Status.** Bounds missing

**TASK tags.** formulation: Onx multi contextual; task family: Online bandit

**MODEL tags.** spectral structure: Shared low rank

**ORACLE tags.** interface family: Batched task rewards; operation: Batched task rewards; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

Multiple linear bandit tasks share an unknown low-dimensional representation. All task actions must be submitted together before the batch of scalar rewards is revealed. Performance is the sum of cumulative pseudo-regret across tasks. Each task’s predictable action set may change over time.

### Admissible model

There are $M$ parallel tasks, each lasting $T$ rounds, with one action per task per round. The parameter matrix and shared representation satisfy:

$$
\Theta=[\theta_1,\ldots,\theta_M],\qquad \operatorname{rank}(\Theta)\le r,\qquad \|\theta_m\|_2\le1.
$$

The current action set $\mathcal{A}_{t,m}\subseteq B_2^d(1)$ may depend on past history and is revealed before the action batch is chosen. No task-diversity or covariance-eigenvalue lower bound is imposed.

### Oracle interface

Submit all $M$ actions simultaneously, then receive all rewards simultaneously. Later actions in a batch cannot use earlier rewards from that batch.

$$
Y_{t,m}=\langle x_{t,m},\theta_m\rangle+\eta_{t,m}.
$$

Given past history and the current action, noise has conditional mean zero and is $1$-sub-Gaussian.

A centralized causal learner is permitted. The parameters $M,d,r,T,\delta_{\mathrm{conf}}$ and current action sets are public; the shared representation $B$ and individual $w_m$ are hidden.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_T=\sum_{t=1}^{T}\sum_{m=1}^{M}\left(\max_{x\in\mathcal{A}_{t,m}}\langle x,\theta_m\rangle-\langle x_{t,m},\theta_m\rangle\right).
$$

### Resource accounting

$$
N=MT.
$$

The quantity $T$ is rounds per task; $N$ is total scalar rewards across all tasks.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

The statistical upper bound permits exact solution of nonconvex low-rank least-squares and optimistic-maximization problems. A polynomial-time implementation is not thereby certified.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

The source guarantee controls $R_T$ with probability at least $1-\delta_{\mathrm{conf}}$, uniformly over the shared parameters and predictable action sets. This is a high-probability pseudo-regret guarantee, not regret computed from realized observation noise.

## 2. Notation and parameters

$M$: Number of parallel tasks **Domain:** $M\in\mathbb N,\ M\ge1$.

Submit one action per task each round. Rewards for the batch arrive together after all actions are submitted.

$T$: Interaction rounds per task. **Domain:** $T\in\mathbb N,\ T\ge1$.

The total scalar reward count across tasks is $N=MT$. Regret is summed across tasks and is not divided by M.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\delta_{\mathrm{conf}}$: The allowed statistical failure probability. **Domain:** $0<\delta_{\mathrm{conf}}<1$.

Used only for statistical correctness or high-probability performance, and distinct from the privacy relaxation parameter.

$r$: The shared-representation rank bound. **Domain:** $r\in\mathbb N,\ 1\le r\le\min\{d,M\}$.

$\operatorname{rank}(\Theta)\le r$.

$\Theta$: Fixed unknown task-parameter matrix **Domain:** $\Theta=[\theta_1,\ldots,\theta_M]\in\mathbb R^{d\times M}$.

$B,W$: The hidden shared representation basis and task-coefficient matrix. **Domain:** $B\in\mathbb R^{d\times r},\ W=[w_1,\ldots,w_M]\in\mathbb R^{r\times M}$.

$\Theta=BW$. One may choose $B^{\mathsf T}B=I_r$. The quantity B is not a public scalar radius.

$\theta_m,w_m$: Task m’s reward parameter and coefficients in the low-dimensional representation. **Domain:** $\theta_m=Bw_m$.

$\|\theta_m\|_2\le1$.

$\mathcal A_{t,m}$: Action set for task $m$, revealed before the current action **Domain:** $\mathcal A_{t,m}\subseteq B_2^d(1)$.

Actions may use prior batches, but not rewards still unavailable from the current batch.

$x_{t,m},Y_{t,m}$: Task action in the current round and the scalar reward subsequently observed **Domain:** $x_{t,m}\in\mathcal A_{t,m},\ Y_{t,m}\in\mathbb R$.

$Y_{t,m}=\langle x_{t,m},\theta_m\rangle+\eta_{t,m}$.

$\eta_{t,m}$: Observation noise in task rewards. **Domain:** Real random variable.

Conditionally on the history and the entire action batch, the noise has mean zero and is $1$-sub-Gaussian.

$m$: Task index **Domain:** $m\in[M]$.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

$R_T=\sum_{t=1}^T\sum_{m=1}^M[\max_{x\in\mathcal A_{t,m}}\langle x,\theta_m\rangle-\langle x_{t,m},\theta_m\rangle]$ Realized observation noise is excluded from the loss difference. Probability or expectation aggregation is specified separately by the guarantee.

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

$B_2^d(r)$: Closed Euclidean ball of radius r **Domain:** $r\ge0$.

$B_2^d(r)=\{x\in\mathbb R^d:\|x\|_2\le r\}$. The symbol r is a placeholder radius, instantiated as R or 1 in the relevant specification.

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The quantity $N=MT$ is the total number of scalar rewards across all tasks.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
R_T=\sum_{t=1}^{T}\sum_{m=1}^{M}\left(\max_{x\in\mathcal A_{t,m}}\langle x,\theta_m\rangle-\langle x_{t,m},\theta_m\rangle\right).
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Use source Assumptions 1–2 and the exact internal-optimization interfaces, with a high-probability guarantee.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
\widetilde{O}\!\left(M\sqrt{drT}+d\sqrt{rMT}\right)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The result assumes the source's Assumptions 1–2 and holds with probability at least $1-\delta_{\mathrm{conf}}$. Exact low-rank least squares and optimistic maximization are permitted; this does not certify a polynomial-time implementation.; The horizon $T$ is per task, $M$ is the number of tasks, and $r$ is the shared rank. A fixed-unit-ball result does not justify replacing the first term by $Mr\sqrt T$.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - Multitask optimistic confidence-set algorithm with a shared representation

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\widetilde{O}\!\left(M\sqrt{drT}+d\sqrt{rMT}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v139/hu21a/hu21a.pdf)

**Source location.** [1](https://proceedings.mlr.press/v139/hu21a/hu21a.pdf) Theorem 1, PDF p.5 Eq.(13)

## References

[1] Jiachen Hu; Xiaoyu Chen; Chi Jin; Lihong Li; Liwei Wang. Near-Optimal Representation Learning for Linear Bandits and Linear RL. 2021. ICML 2021, PMLR 139.

https://proceedings.mlr.press/v139/hu21a/hu21a.pdf
