# Finite-arm lexicographic bandits with a known objective-tradeoff bound.

**Setting ID.** `ONX_LEX_FINITE_KNOWN`

Online learning and bandits

The learner faces multiple reward objectives ordered by priority. Each round selects one arm and observes its complete reward vector. The comparator is the lexicographically optimal arm. Known tradeoff coefficients control improvements in lower-priority objectives relative to losses in higher-priority ones; performance is retained as signed regret for each objective.

**Status.** Logarithmic gap; Bounds missing

**TASK tags.** formulation: Onx lex finite known; task family: Online bandit

**MODEL tags.** structure: Finite actions

**ORACLE tags.** interface family: Selected reward vector; operation: Selected reward vector; public information: Hidden objects explicitly declared; public information: Known tradeoff; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Signed vector regret

**GUARANTEE tags.** mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

The learner faces multiple reward objectives ordered by priority. Each round selects one arm and observes its complete reward vector. The comparator is the lexicographically optimal arm. Known tradeoff coefficients control improvements in lower-priority objectives relative to losses in higher-priority ones; performance is retained as signed regret for each objective.

### Admissible model

The action set contains $K$ arms and carries a discrete metric of diameter at most $1$. Each arm has $m$ fixed mean rewards $\mu_1,\ldots,\mu_m$ ordered by priority, and each mean function is $1$-Lipschitz in this metric. The range of each objective is at most $1$; an irrelevant common additive shift is unrestricted.

A lexicographically optimal arm $x^\star$ exists. The highest-priority objective may have several optimal arms. Each subsequent objective is compared only among arms optimal for all higher-priority objectives. Only instances with the following finite tradeoff coefficients are included:

$$
\lambda_\star=\inf\!\left\{\lambda\ge0:\ \mu_i(x)-\mu_i(x^\star)\le\lambda\max_{j<i}\bigl(\mu_j(x^\star)-\mu_j(x)\bigr),\ \forall x\in\mathcal{X},\ 2\le i\le m\right\}<\infty.
$$

### Oracle interface

Select arm $x_t$ first, then observe all $m$ coordinates of its reward vector.

Given the past and the current arm, each reward coordinate is conditionally $1$-sub-Gaussian around its fixed mean. Independence between objective coordinates is not required.

$$
\mathbb{E}\!\left[e^{s(Y_{t,i}-\mu_i(x_t))}\mid\mathcal{H}_{t-1},x_t\right]\le e^{s^2/2}\qquad(s\in\mathbb{R},\ 1\le i\le m).
$$

Causal randomized policies are permitted. The information $K,m,T,\delta_{\mathrm{conf}}$ and a tradeoff upper bound satisfying $\lambda\ge\lambda_\star$ are public.

Neither the mean vector nor the set of primary-objective optimal arms is public.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_i(T)=T\mu_i(x^\star)-\sum_{t=1}^{T}\mu_i(x_t),\qquad i=1,\ldots,m.
$$

### Resource accounting

Pull one arm per round: $N=T$ pulls yield $mT$ reward coordinates in total.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

#### Main

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

These are signed cumulative regrets for individual objectives. No primary-objective tie indicator or positive part is applied. The stated tradeoff controls all objectives simultaneously with probability at least $1-\delta_{\mathrm{conf}}$, uniformly over the specified instance class. This vector guarantee is not automatically a scalarized regret bound.

#### Two objectives: simultaneous expected signed regret

All measurable randomized causal policies may use K,T and the supplied tradeoff bound lambda. No mean reward or optimal arm is known.

$$
\forall\nu:\quad\max_{i\le2}\mathbb E_\nu R_i(T)\le r
$$

Expected signed coordinate regret is controlled simultaneously; The expected signed-regret criterion is distinct from the high-probability criterion.

Task: Minimize the worst-instance simultaneous expected signed coordinate regret $\max_{i\in\{1,2\}}\mathbb E_\nu R_i(T)$ for two lexicographic objectives with a supplied tradeoff upper bound.

Model: The public action set is $\mathcal X=[K]$ with $K\ge2$ and the discrete metric $D(x,y)=\mathbf1\{x\ne y\}$.

Model: There are exactly two fixed mean functions $\mu^1,\mu^2$, each 1-Lipschitz in D and each with oscillation at most one. Common additive offsets may differ between the two coordinates and are unrestricted; the gaps, local tradeoff, and regret are invariant under these offsets.

Model: The primary optimum set is $\mathcal X_1^*=\operatorname{argmax}_{x\in\mathcal X}\mu^1(x)$, and a lexicographic optimum $x^*\in\operatorname{argmax}_{x\in\mathcal X_1^*}\mu^2(x)$ exists. Primary ties are permitted.

Model: The finite local tradeoff is $\lambda_*=\inf\{b\ge0:\mu^2(x)-\mu^2(x^*)\le b[\mu^1(x^*)-\mu^1(x)]\ \forall x\in\mathcal X\}$. A finite upper bound $\lambda\ge\lambda_*\ge0$ is supplied to the policy.

Oracle: At round t, choose one arm $X_t\in\mathcal X$ using past observations and independent internal randomness, then receive both coordinates $(Y_t^1,Y_t^2)$. Conditional on the past and current arm, $\mathbb E[\exp(\theta(Y_t^i-\mu^i(X_t)))\mid\mathcal H_{t-1},X_t]\le\exp(\theta^2/2)$ for all real theta and i=1,2. Cross-coordinate independence is not required. No unselected-arm feedback, same-round second pull, or historical requery is provided.

Oracle: Public inputs are K,T, the fact m=2, and the finite supplied upper bound lambda. No external confidence parameter is required by this expected-regret view.

Oracle: Mean functions, the primary-optimal arm set, and the lexicographic optimum are hidden.

Output: Output the executed causal arm trajectory; each round contributes to both signed coordinate regrets against the same lexicographic optimum.

Metric: Define $R_i(T)=\sum_t[\mu^i(x^*)-\mu^i(X_t)]$ for i=1,2. The comparison uses $\ell(\pi,\nu)=\max_{i\in\{1,2\}}\mathbb E_\nu R_i(T)$.

Metric: Take the expectation of each signed coordinate regret first and then the maximum over the two coordinates. This is not $\mathbb E\max_iR_i(T)$, a positive-part regret, a weighted sum, or a high-probability threshold. Secondary signed regret may be negative; primary regret is nonnegative.

Resource: One selected-arm pull is made per round. The fixed horizon T is the reward-query budget N=T, and exactly 2T scalar reward coordinates are observed. All exploration and initialization pulls are included.

Resource: Internal arithmetic and storage are unrestricted and are not reward observations.

**Budget convention.** fixed_horizon

## 2. Notation and parameters

$K$: Number of arms in the finite action set **Domain:** $K\in\mathbb N,\ K\ge1$.

$|\mathcal X|=K$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$\delta_{\mathrm{conf}}$: The allowed statistical failure probability. **Domain:** $0<\delta_{\mathrm{conf}}<1$.

Used only for statistical correctness or high-probability performance, and distinct from the privacy relaxation parameter.

$\lambda$: Public upper bound on lexicographic objective tradeoffs **Domain:** $\lambda\ge\lambda_\star\ge0$.

The quantity $\lambda_\star$ is defined by the model’s cross-objective reward-gap inequality. It is not a regularization strength.

$m$: The number of reward objectives, ordered by priority. **Domain:** $m\in\mathbb N,\ m\ge1$.

Objective index $i\in[m]$. Smaller indices have higher priority.

$\mathcal X,D$: The public action set and its metric. **Domain:** Metric space of diameter at most $1$.

The quantity $D(x,y)$ is the distance between two arms, not the Euclidean diameter parameter.

$\mu_i$: The fixed unknown mean-reward function for objective i. **Domain:** $\mu_i:\mathcal X\to\mathbb R,\ i\in[m]$.

Assume $|\mu_i(x)-\mu_i(y)|\le D(x,y)$; the range of each objective mean is at most one.

$x^\star,x_t$: Lexicographically first optimal arm and the arm selected at round $t$ **Domain:** $x^\star,x_t\in\mathcal X$.

Maximize the next objective among arms already optimal for all higher-priority objectives.

$\lambda_\star$: Smallest objective-tradeoff coefficient for the instance **Domain:** Finite nonnegative real number; a hidden analysis quantity.

The smallest coefficient satisfying the model's condition $\mu_i(x)-\mu_i(x^\star)\le\lambda_\star\max_{j<i}(\mu_j(x^\star)-\mu_j(x))$.

$R_i(T)$: Signed cumulative regret for objective $i$ **Domain:** Real number.

The criterion is $R_i(T)=T\mu_i(x^\star)-\sum_t\mu_i(x_t)$; do not take positive parts or replace it with a scalarized objective.

$\Lambda_i(\lambda)$: Error-amplification factor induced by the known tradeoff coefficient **Domain:** Positive real number.

$\Lambda_i(\lambda)=\sum_{j=0}^{i-1}\lambda^j$, with every zeroth power interpreted as one.

$i,j$: Target and summation index **Domain:** Nonnegative integer index.

$i\in\{1,\ldots,m\}$. Use $1\le j<i$ in the tradeoff expression and $0\le j<i$ in the geometric series.

$s$: Test parameter in the conditional sub-Gaussian moment-generating-function bound **Domain:** $s\in\mathbb R$.

A conditional moment-generating-function inequality for every s defines observation noise. Here s is not a budget.

$\alpha_T$: Parameter for simultaneous confidence bounds over finitely many arms **Domain:** Positive real number.

$\alpha_T=4\log(mKT/\delta_{\mathrm{conf}})$.

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

The quantity $N=T$ counts arm pulls. Each pull returns the current arm’s m objective rewards.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

**View.** Main

$$
R_i(T)=T\mu_i(x^\star)-\sum_{t=1}^{T}\mu_i(x_t),\qquad i=1,\ldots,m.
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

#### Q2 - minimax metric resource quantity

**View.** Two objectives: simultaneous expected signed regret

$$
\mathfrak M_{T,K}(\lambda)=\inf_{\pi(\lambda)}\sup_{\nu:\lambda_*\le\lambda}\max_{i\le2}\mathbb E_\nu R_i(T)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $T$; description: Each played round and its prescribed feedback are charged.

### R1 - SUPPORTED

**Region.** Finite $K$; known $\lambda\ge\lambda_\star$; arbitrary $\delta_{\mathrm{conf}}$; simultaneous guarantees for all vector coordinates.

**Views.** Main

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
\begin{gathered}R_i(T)\le16\Lambda_i(\lambda)\sqrt{\alpha_TKT},\\ \Lambda_i(\lambda)=\sum_{j=0}^{i-1}\lambda^j,\qquad \alpha_T=4\log\!\left(\frac{mKT}{\delta_{\mathrm{conf}}}\right).\end{gathered}
$$

### R2 - Two-objective supplied-envelope phase diagram

**Region.** $K,T\ge2$, exactly two objectives, and public $\lambda\ge0$ with $\lambda_*\le\lambda$. Finite arm count K. The upper strategy uses reward-coordinate differences, so common additive shifts allowed by the existing profile do not change its decisions or guarantee.

**Views.** Two objectives: simultaneous expected signed regret

**Quantity.** Q2

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Logarithmic gap

**Lower bound.** B3

$$
\Omega\!\left(\min\{T,\sqrt{(1\vee\lambda)(K-1)T},(K-1)^{1/3}T^{2/3}\}\right)
$$

**Upper bound.** B2

$$
\widetilde O\!\left(\min\{T,\sqrt{(1\vee\lambda)KT},K^{1/3}T^{2/3}\}\right)
$$

**Gap or comparison.** Only logarithmic factors in the displayed parameters remain.

## 4. Bounds and supporting evidence

### B1 - SDLO: lexicographic UCB with a known tradeoff coefficient.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Main

**Witness or lower-bound scope.** Deterministic witness

$$
\begin{gathered}R_i(T)\le16\Lambda_i(\lambda)\sqrt{\alpha_TKT},\\ \Lambda_i(\lambda)=\sum_{j=0}^{i-1}\lambda^j,\qquad \alpha_T=4\log\!\left(\frac{mKT}{\delta_{\mathrm{conf}}}\right).\end{gathered}
$$

**Sources.** [1](https://jmlr.org/papers/volume26/24-1047/24-1047.pdf)

**Conditions.** The quantity $K$ is finite, and $\lambda\ge\lambda_*$ is known. The stated guarantees hold simultaneously for $i=1,\ldots,m$ with probability at least $1-\delta_{\mathrm{conf}}$.; The quantity $R_i(T)=T\mu_i(x^\star)-\sum_{t=1}^T\mu_i(x_t)$ is signed regret for objective $i$. The factor $\Lambda_i$ is an explicit geometric sum, not a logarithm of the horizon.; Multiple arms may maximize the primary objective. This upper bound does not prove the catalog's proposed lower bound for unknown tradeoffs with exact ties.

**Oracle correspondence.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

**Source location.** [1](https://jmlr.org/papers/volume26/24-1047/24-1047.pdf) Theorem 1 with covering radius 0, Remark 1, PDF pp.10–11

### B2 - Robust-score multiscale elimination with secondary-objective commitment.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Two objectives: simultaneous expected signed regret

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O\!\left(\min\{T,\sqrt{(1\vee\lambda)KT},K^{1/3}T^{2/3}\}\right)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $K,T\ge2$, exactly two objectives, and public $\lambda\ge0$ with $\lambda_*\le\lambda$.; The upper strategy uses reward-coordinate differences, so common additive shifts allowed by the existing profile do not change its decisions or guarantee.

**Dimension conditions.** Finite arm count K.

**Constants.** Universal constants.

**Logarithmic factors.** Source tilde-O hides logarithms in K, T, and the supplied envelope, but no polynomial dependence.

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:finite-envelope; Section sec:envelope

Robust-score multiscale elimination with secondary-objective commitment.. Causal policies given the supplied envelope.

### B3 - Primary-only and hidden-candidate constructions across envelope sizes.

**Admission.** Included in the bracket

**Direction.** lower

**View.** Two objectives: simultaneous expected signed regret

**Witness or lower-bound scope.** Randomized witness

$$
\Omega\!\left(\min\{T,\sqrt{(1\vee\lambda)(K-1)T},(K-1)^{1/3}T^{2/3}\}\right)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $K,T\ge2$, exactly two objectives, and public $\lambda\ge0$ with $\lambda_*\le\lambda$.; The upper strategy uses reward-coordinate differences, so common additive shifts allowed by the existing profile do not change its decisions or guarantee.

**Dimension conditions.** Finite arm count K.

**Constants.** Universal constants.

**Logarithmic factors.** Source tilde-O hides logarithms in K, T, and the supplied envelope, but no polynomial dependence.

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:finite-envelope; Appendix app:envelope

Primary-only and hidden-candidate constructions across envelope sizes.. Every randomized causal policy given the same envelope.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Bo Xue; Ji Cheng; Fei Liu; Yimu Wang; Lijun Zhang; Qingfu Zhang. Lexicographic Lipschitz Bandits: New Algorithms and a Lower Bound. 2025. JMLR 26 (2025), published September 2025.

https://jmlr.org/papers/volume26/24-1047/24-1047.pdf

[2] Colombo_U07. Primary Ties and the Price of Unknown Trade-offs in Lexicographic Bandits. primary_ties_unknown_tradeoffs.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf
