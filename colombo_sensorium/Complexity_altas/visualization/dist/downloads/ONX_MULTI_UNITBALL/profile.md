# Multitask linear bandits with unit-ball actions and unit-norm parameters

**Setting ID.** `ONX_MULTI_UNITBALL`

Online learning and bandits

Multiple linear bandit tasks share an unknown low-dimensional representation. All task actions must be submitted together before the batch of scalar rewards is revealed. Performance is the sum of cumulative pseudo-regret across tasks. Each task has the unit ball as its action set and a unit-norm parameter.

**Status.** Bounds missing

**TASK tags.** formulation: Onx multi unitball; task family: Online bandit

**MODEL tags.** spectral structure: Shared low rank

**ORACLE tags.** interface family: Batched task rewards; operation: Batched task rewards; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

Multiple linear bandit tasks share an unknown low-dimensional representation. All task actions must be submitted together before the batch of scalar rewards is revealed. Performance is the sum of cumulative pseudo-regret across tasks. Each task has the unit ball as its action set and a unit-norm parameter.

### Admissible model

There are $M$ parallel tasks, each lasting $T$ rounds, with one action per task per round. The parameter matrix and shared representation satisfy:

$$
\Theta=[\theta_1,\ldots,\theta_M],\quad \operatorname{rank}(\Theta)=r,\quad \theta_m=Bw_m,\quad B^{\mathsf T}B=I_r,\quad \|\theta_m\|_2=1.
$$

Each task has action set $\mathcal{A}_m=B_2^d(1)$. This profile imposes no task-diversity assumption; applicability of the separately listed representation-based upper bound remains pending.

### Oracle interface

Submit all $M$ actions simultaneously, then receive all rewards simultaneously. Later actions in a batch cannot use earlier rewards from that batch.

$$
Y_{t,m}=\langle x_{t,m},\theta_m\rangle+\eta_{t,m}.
$$

The variables $\eta_{t,m}$ are IID $\mathcal N(0,1)$ across tasks and rounds.

Centralized causal policies are allowed, with $d,r,M,T$ public. The shared basis $B$ and coefficient matrix $W=[w_1,\ldots,w_M]$ are hidden.

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

The source three-stage explore-then-commit algorithm uses the following two exploration lengths:

$$
T_1=\left\lceil d\sqrt{\frac{rT}{M}}\right\rceil,\qquad T_2=\left\lceil r\sqrt T\right\rceil.
$$

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

The algorithm may centrally use all previously observed task data. No sequential feedback is available within a batch.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

The objective minimizes expected total pseudo-regret $\mathbb{E}[R_T]$, with $\mathcal{A}_{t,m}=B_2^d(1)$.

## 2. Notation and parameters

$M$: Number of parallel tasks **Domain:** $M\in\mathbb N,\ M\ge1$.

Submit one action per task each round. Rewards for the batch arrive together after all actions are submitted.

$T$: Interaction rounds per task. **Domain:** $T\in\mathbb N,\ T\ge1$.

The total scalar reward count across tasks is $N=MT$. Regret is summed across tasks and is not divided by M.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$r$: Rank of the shared parameter matrix **Domain:** $r\in\mathbb N,\ 1\le r\le\min\{d,M\}$.

$\operatorname{rank}(\Theta)=r$.

$\Theta$: Fixed unknown task-parameter matrix **Domain:** $\Theta=[\theta_1,\ldots,\theta_M]\in\mathbb R^{d\times M}$.

$B,W$: The hidden shared representation basis and task-coefficient matrix. **Domain:** $B\in\mathbb R^{d\times r},\ W=[w_1,\ldots,w_M]\in\mathbb R^{r\times M}$.

$\Theta=BW$. One may choose $B^{\mathsf T}B=I_r$. The quantity B is not a public scalar radius.

$\theta_m,w_m$: Task m’s reward parameter and coefficients in the low-dimensional representation. **Domain:** $\theta_m=Bw_m$.

$\|\theta_m\|_2=1$.

$\mathcal A_{t,m}$: Action set for task $m$, revealed before the current action **Domain:** $\mathcal A_{t,m}\subseteq B_2^d(1)$.

For every t and m, use the fixed unit ball $B_2^d(1)$.

$x_{t,m},Y_{t,m}$: Task action in the current round and the scalar reward subsequently observed **Domain:** $x_{t,m}\in\mathcal A_{t,m},\ Y_{t,m}\in\mathbb R$.

$Y_{t,m}=\langle x_{t,m},\theta_m\rangle+\eta_{t,m}$.

$\eta_{t,m}$: Observation noise in task rewards. **Domain:** Real random variable.

Samples are i.i.d. $\mathcal N(0,1)$ across tasks and rounds.

$m$: Task index **Domain:** $m\in[M]$.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

$R_T=\sum_{t=1}^T\sum_{m=1}^M[1-\langle x_{t,m},\theta_m\rangle]$. Realized observation noise is excluded from loss differences. Probability and expectation are specified by the success guarantee.

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

**Region.** $\|\theta_m\|=1,\operatorname{rank}(\Theta)=r$. No task-diversity assumption is imposed.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B2

$$
O(M\min\{T,d\sqrt T\})
$$

## 4. Bounds and supporting evidence

### B1 - Three-stage representation estimation, task exploration, and commitment; applicability review pending.

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** upper

**Witness or lower-bound scope.** Witness type not certified

$$
\widetilde{O}\!\left(d\sqrt{rMT}+rM\sqrt T\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2203.15664)

**Conditions.** The total exploration phase must fit within the $T$ rounds.; The source-bound mapping involves $\sigma_r(\Theta)$, the $r$th largest singular value of the task-parameter matrix. Its applicability to the model without task diversity remains pending.; The source claim remains pending applicability review and is not promoted to a certified frontier result for this specification.

**Oracle correspondence.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

**Source location.** [1](https://arxiv.org/pdf/2203.15664) Theorem 4.1, PDF p.6; proof Eq.(18) p.8

### B2 - Run E2TC independently for each task

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(M\min\{T,d\sqrt T\}\right)
$$

**Sources.** [2](https://proceedings.mlr.press/v291/zhang25b.html)

**Conditions.** Each task parameter satisfies $\|\theta_m\|_2=1$. Actions lie in the unit Euclidean ball, and observations have independent standard Gaussian noise.; Any shared rank $r$ allowed by the specification is permitted, without task diversity. All tasks submit their actions simultaneously each round.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** Each task runs E2TC using only its own past rewards, so actions for all tasks can be submitted simultaneously within a batch. Sum the taskwise expected regrets and retain total sample count $N=MT$. This upper bound does not exploit a shared low-rank representation.

**Source location.** [2](https://proceedings.mlr.press/v291/zhang25b.html) theorem: Corollary8, independent application to each task

Each task runs E2TC using only its own past rewards, so actions for all tasks can be submitted simultaneously within a batch. Sum the taskwise expected regrets and retain total sample count $N=MT$. This upper bound does not exploit a shared low-rank representation.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Jiaqi Yang; Jason D. Lee; Qi Lei; Simon S. Du. Nearly Minimax Algorithms for Linear Bandits with Shared Representation. 2022. 2203.15664v1.

https://arxiv.org/pdf/2203.15664

[2] Raymond Zhang; Hédi Hadiji; Richard Combes. Linear Bandits on Ellipsoids: Minimax Optimal Algorithms. 2025. COLT2025, PMLR291:6016–6040.

https://proceedings.mlr.press/v291/zhang25b.html
