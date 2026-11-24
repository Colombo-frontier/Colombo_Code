# Metric Lipschitz lexicographic bandits with known objective-tradeoff upper bounds

**Setting ID.** `ONX_LEX_LIPSCHITZ_KNOWN`

Online learning and bandits

The learner faces multiple reward objectives ordered by priority. Each round selects one arm and observes its complete reward vector. The comparator is the lexicographically optimal arm. Known tradeoff coefficients control improvements in lower-priority objectives relative to losses in higher-priority ones; performance is retained as signed regret for each objective.

**Status.** Logarithmic gap; Bounds missing

**TASK tags.** formulation: Onx lex lipschitz known; task family: Online bandit

**MODEL tags.** smoothness: Metric lipschitz

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

The public metric action space $(\mathcal{X},D)$ has diameter at most $1$ and may contain infinitely many arms. Required covering and activation interfaces are available. Every arm has $m$ fixed mean rewards $\mu_1,\ldots,\mu_m$, ordered by priority; each mean function is $1$-Lipschitz and has oscillation at most $1$. Irrelevant common additive shifts are unrestricted.

A lexicographically optimal arm $x^\star$ exists. The highest-priority objective may have several optimal arms. Each subsequent objective is compared only among arms optimal for all higher-priority objectives. Only instances with the following finite tradeoff coefficients are included:

$$
\lambda_\star=\inf\!\left\{\lambda\ge0:\ \mu_i(x)-\mu_i(x^\star)\le\lambda\max_{j<i}\bigl(\mu_j(x^\star)-\mu_j(x)\bigr),\ \forall x\in\mathcal{X},\ 2\le i\le m\right\}<\infty.
$$

$$
N_c(r)=\min\!\left\{n:\ \mathcal{X}\subseteq\bigcup_{j=1}^{n}B_D(x_j,r),\ x_j\in\mathcal{X}\right\}.
$$

The quantity $N_c(r)$ is the covering number at radius $r$. Objective-specific scaled covering indices $N_z^{(i)}(r)$ are defined on the source near-optimal sets; they cannot be replaced by ambient dimension $d$ without justification.

### Oracle interface

Select arm $x_t$ first, then observe all $m$ coordinates of its reward vector.

Given the past and the current arm, each reward coordinate is conditionally $1$-sub-Gaussian around its fixed mean. Independence between objective coordinates is not required.

$$
\mathbb{E}\!\left[e^{s(Y_{t,i}-\mu_i(x_t))}\mid\mathcal{H}_{t-1},x_t\right]\le e^{s^2/2}\qquad(s\in\mathbb{R},\ 1\le i\le m).
$$

Causal strategies may use the public metric-covering or activation interface. The metric space, $m,T,\delta_{\mathrm{conf}}$, and $\lambda\ge\lambda_\star$ are public.

Mean functions and the lexicographically optimal arm $x^\star$ are hidden.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_i(T)=T\mu_i(x^\star)-\sum_{t=1}^{T}\mu_i(x_t),\qquad i=1,\ldots,m.
$$

### Resource accounting

There are $N=T$ arm pulls. Metric covering and new-arm activation have separate computational or interface costs; they are not free reward observations.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

#### Main

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

These are signed cumulative regrets for individual objectives. No primary-objective tie indicator or positive part is applied. The stated tradeoff controls all objectives simultaneously with probability at least $1-\delta_{\mathrm{conf}}$, uniformly over the specified instance class. This vector guarantee is not automatically a scalarized regret bound.

#### Two-objective expected regret with known tradeoff

All measurable randomized causal policies with the metric-net interface and supplied tradeoff envelope are allowed.

$$
\forall\nu:\quad\max_{i\le2}\mathbb E_\nu R_i(T)\le r
$$

The policy receives the envelope but does not require the entropy sequence.

Task: Minimize the worst-instance simultaneous expected signed coordinate regret $\max_{i\in\{1,2\}}\mathbb E_\nu R_i(T)$ for two lexicographic objectives with a supplied tradeoff upper bound.

Model: The public arm space is $\mathcal X=\{a\}\cup S$, where S is nonempty compact, $D(a,z)=1$ for every z in S, and $\operatorname{diam}(S)\le1/4$.

Model: There are exactly two fixed mean functions $\mu^1,\mu^2$, each 1-Lipschitz in D and each with oscillation at most one. Common additive offsets may differ between the two coordinates and are unrestricted; the gaps, local tradeoff, and regret are invariant under these offsets.

Model: The primary optimum set is $\mathcal X_1^*=\operatorname{argmax}_{x\in\mathcal X}\mu^1(x)$, and a lexicographic optimum $x^*\in\operatorname{argmax}_{x\in\mathcal X_1^*}\mu^2(x)$ exists. Primary ties are permitted.

Model: The finite local tradeoff is $\lambda_*=\inf\{b\ge0:\mu^2(x)-\mu^2(x^*)\le b[\mu^1(x^*)-\mu^1(x)]\ \forall x\in\mathcal X\}$. A finite upper bound $\lambda\ge\lambda_*\ge0$ is supplied to the policy.

Oracle: At round t, choose one arm $X_t\in\mathcal X$ using past observations and independent internal randomness, then receive both coordinates $(Y_t^1,Y_t^2)$. Conditional on the past and current arm, $\mathbb E[\exp(\theta(Y_t^i-\mu^i(X_t)))\mid\mathcal H_{t-1},X_t]\le\exp(\theta^2/2)$ for all real theta and i=1,2. Cross-coordinate independence is not required. No unselected-arm feedback, same-round second pull, or historical requery is provided.

Oracle: Public inputs are T, the fact m=2, the compact metric and its anchor-plus-tie geometry, and the finite supplied upper bound lambda. No external confidence parameter is required by this expected-regret view.

Oracle: Mean functions, the primary-optimal arm set, and the lexicographic optimum are hidden.

Oracle: A measurable maximal-net oracle is available: given a nonempty compact subset U of the public metric space and a radius r>0, it returns a finite inclusion-maximal r-separated subset of U. Such a set covers U by closed radius-r balls. This geometric computation does not supply reward information and is not charged as an arm pull.

Output: Output the executed causal arm trajectory; each round contributes to both signed coordinate regrets against the same lexicographic optimum.

Metric: Define $R_i(T)=\sum_t[\mu^i(x^*)-\mu^i(X_t)]$ for i=1,2. The comparison uses $\ell(\pi,\nu)=\max_{i\in\{1,2\}}\mathbb E_\nu R_i(T)$.

Metric: Take the expectation of each signed coordinate regret first and then the maximum over the two coordinates. This is not $\mathbb E\max_iR_i(T)$, a positive-part regret, a weighted sum, or a high-probability threshold. Secondary signed regret may be negative; primary regret is nonnegative.

Resource: One selected-arm pull is made per round. The fixed horizon T is the reward-query budget N=T, and exactly 2T scalar reward coordinates are observed. All exploration and initialization pulls are included.

Resource: Internal arithmetic and storage are unrestricted and are not reward observations.

Resource: The maximal-net interface has a separate geometric computation cost, which is uncharged in the reward-count comparison. It does not reveal rewards of newly generated arms.

**Budget convention.** fixed_horizon

## 2. Notation and parameters

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

$r,r_0$: Covering radius and truncation radius in the multiscale decomposition **Domain:** $0<r\le1,\ 0<r_0<1$.

These are auxiliary scales in algorithms or bounds, not environment dimension or rank.

$B_D(x,r)$: Closed metric ball **Domain:** An action subset.

$B_D(x,r)=\{y\in\mathcal X:D(x,y)\le r\}$.

$N_c(r)$: Minimum number of radius-$r$ balls needed to cover the action space **Domain:** A positive integer or infinity.

The quantity is $N_c(r)=\min\{n:\mathcal X\subseteq\cup_{j=1}^nB_D(x_j,r),\ x_j\in\mathcal X\}$; it must be finite when invoking the covering algorithm.

$\mathcal X^{(i)}(r)$: The scaled near-optimal gap level for objective i. **Domain:** An action subset.

$\{x:\Lambda_i(\lambda)r/2<\mu_i(x^\star)-\mu_i(x)\le\Lambda_i(\lambda)r\}$.

$N_z^{(i)}(r)$: Local covering number at a scaled gap level **Domain:** Nonnegative integer.

This is the minimum number of metric balls of radius $r/96$ needed to cover $\mathcal X^{(i)}(r)$. It is an analytical quantity and is not supplied to the algorithm.

$\alpha_T$: The confidence parameter of the fixed-covering method. **Domain:** Positive real number.

$\alpha_T=4\log(mN_c(r)T/\delta_{\mathrm{conf}})$.

$\widetilde\alpha_T$: The confidence parameter of the adaptive scaling algorithm. **Domain:** Positive real number.

$\widetilde\alpha_T=4\log(4mT^2/\delta_{\mathrm{conf}})$.

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

$(\mathcal X,D)$: Public compact metric arm space **Domain:** $\operatorname{diam}(\mathcal X)\le1$.

$\lambda_*$: Unknown local tradeoff **Domain:** $\lambda_*\in[0,\infty]$.

$S$: Compact tie component in the anchor-plus-tie regimes **Domain:** $S\ne\varnothing$, $\operatorname{diam}(S)\le1/4$.

$a$: Anchor arm **Domain:** $\mathcal X=\{a\}\cup S$, $D(a,z)=1$ for z in S.

$d_p$: Packing-growth exponent **Domain:** $d_p\ge0$.

$Z$: Packing-profile size coefficient **Domain:** $Z\ge1$.

$c_-,c_+$: Regular metric packing and covering constants **Domain:** $c_-,c_+>0$.

$r_0$: Maximum radius in regular metric growth assumptions **Domain:** $0<r_0\le1/16$.

$r_s$: Dyadic radius for the entropy frontier **Domain:** $s\ge0$ integer, $r_s>0$.

$r_s=2^{-s-4}$

$s_T$: Final dyadic entropy scale **Domain:** $s_T\in\mathbb N$.

$s_T=\lceil\log_2(16T)\rceil+2$

$M_s$: Tie-space packing number **Domain:** $M_s\ge1$.

$M_s=\operatorname{Pack}(S,r_s)$

$\Psi_T^\infty(S)$: Critical entropy regret scale **Domain:** $\Psi_T^\infty(S)>0$.

$\Psi_T^\infty(S)=T\max_{0\le s\le s_T}\min\{r_s,(M_s/T)^{1/3}\}$

$B_\lambda$: Effective envelope **Domain:** $B_\lambda\ge1$.

$B_\lambda=1\vee\lambda$

$\Psi_T^{B_\lambda}(S)$: Known-envelope critical entropy regret scale **Domain:** $\Psi_T^{B_\lambda}(S)>0$.

$\Psi_T^{B_\lambda}(S)=T\max_{0\le s\le s_T}\min\{r_s,\sqrt{B_\lambda M_s/T},(M_s/T)^{1/3}\}$

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

**View.** Two-objective expected regret with known tradeoff

$$
\mathfrak M_T(\mathcal X;\lambda)=\inf_{\pi(\lambda)}\sup_{\nu:\lambda_*\le\lambda}\max_i\mathbb E_\nu R_i(T)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $T$; description: Each played round and its prescribed feedback are charged.

### R1 - SUPPORTED

**Region.** The required finite covering and activation interfaces are available, and $\lambda\ge\lambda_\star$. No ambient dimension is fixed in advance.

**Views.** Main

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1, B2

$$
\min\left\{2\Lambda_i(\lambda)\left[rT+8\sqrt{\alpha_TN_c(r)T}\right],\ \inf_{0<r_0<1}\Lambda_i(\lambda)\left[r_0T+1152\widetilde\alpha_T\sum_{j\ge0:2^{-j}\ge r_0}N_z^{(i)}(2^{-j})2^j\right]\right\}
$$

### R2 - Two-objective supplied-envelope tie entropy

**Region.** $T\ge2$, two objectives, public $\lambda\ge\lambda_*\ge0$, and the stated compact anchor-plus-tie metric geometry. Arbitrary compact tie component S; all metric dependence enters M_s.

**Views.** Two-objective expected regret with known tradeoff

**Quantity.** Q2

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
\Omega(\Psi_T^{B_\lambda}(S))
$$

**Upper bound.** B3

$$
O(\log(eT)\Psi_T^{B_\lambda}(S))
$$

**Gap or comparison.** Ratio at most $O(\log(eT))$.

## 4. Bounds and supporting evidence

### B1 - SDLO with a fixed covering net.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Main

**Witness or lower-bound scope.** Deterministic witness

$$
R_i(T)\le2\Lambda_i(\lambda)\left[rT+8\sqrt{\alpha_TN_c(r)T}\right]\quad(i\in[m])
$$

**Sources.** [1](https://jmlr.org/papers/volume26/24-1047/24-1047.pdf)

**Conditions.** Require $\lambda\ge\lambda_\star$, $0<r\le1$, and $N_c(r)<\infty$. A single event controls all objectives simultaneously with probability at least $1-\delta_{\mathrm{conf}}$.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** Let $\alpha_T=4\log(mN_c(r)T/\delta_{\mathrm{conf}})$, where $N_c(r)$ is the covering number at radius $r$. Choose the radius from public geometry and the horizon. One success event controls all objectives simultaneously; the vector bound is not implicitly scalarized.

**Source location.** [1](https://jmlr.org/papers/volume26/24-1047/24-1047.pdf) theorem: Theorem 1

Let $\alpha_T=4\log(mN_c(r)T/\delta_{\mathrm{conf}})$, where $N_c(r)$ is the covering number at radius $r$. Choose the radius from public geometry and the horizon. One success event controls all objectives simultaneously; the vector bound is not implicitly scalarized.

### B2 - ADLO: adaptive activation and lexicographic filtering

**Admission.** Included in the bracket

**Direction.** upper

**View.** Main

**Witness or lower-bound scope.** Deterministic witness

$$
R_i(T)\le\inf_{0<r_0<1}\!\left[\Lambda_i(\lambda)r_0T+1152\Lambda_i(\lambda)\widetilde\alpha_T\sum_{j\ge0:\,2^{-j}\ge r_0}N_z^{(i)}(2^{-j})2^j\right]
$$

**Sources.** [1](https://jmlr.org/papers/volume26/24-1047/24-1047.pdf)

**Conditions.** Require $\lambda\ge\lambda_\star$ and supply the specified covering/activation interface. The joint success probability for all objectives is at least $1-\delta_{\mathrm{conf}}$.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** Only the logarithms in $\widetilde O$ are suppressed; see the evidence record.

**Derivation.** The quantity $N_z^{(i)}(r)$ is the $r/96$-covering number of the gap layer for objective $i$, defined by $\Lambda_i(\lambda)r/2<\mu_i(x^\star)-\mu_i(x)\le\Lambda_i(\lambda)r$. It is used only in analysis, not supplied to the algorithm. The confidence parameter is $\widetilde\alpha=4\log(4mT^2/\delta_{\mathrm{conf}})$.

**Source location.** [1](https://jmlr.org/papers/volume26/24-1047/24-1047.pdf) theorem: Theorem 2

The quantity $N_z^{(i)}(r)$ is the $r/96$-covering number of the gap layer for objective $i$, defined by $\Lambda_i(\lambda)r/2<\mu_i(x^\star)-\mu_i(x)\le\Lambda_i(\lambda)r$. It is used only in analysis, not supplied to the algorithm. The confidence parameter is $\widetilde\alpha=4\log(4mT^2/\delta_{\mathrm{conf}})$.

### B3 - Metric filtering with a supplied envelope and entropy crossing.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Two-objective expected regret with known tradeoff

**Witness or lower-bound scope.** Randomized witness

$$
O(\log(eT)\Psi_T^{B_\lambda}(S))
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $T\ge2$, two objectives, public $\lambda\ge\lambda_*\ge0$, and the stated compact anchor-plus-tie metric geometry.

**Dimension conditions.** Arbitrary compact tie component S; all metric dependence enters M_s.

**Constants.** Universal constants.

**Logarithmic factors.** Only the displayed horizon logarithm.

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:entropy; Appendix app:entropy

Metric filtering with a supplied envelope and entropy crossing.. Causal policies given the envelope and net access.

### B4 - One-scale primary-tie lower bounds obeying the supplied envelope.

**Admission.** Included in the bracket

**Direction.** lower

**View.** Two-objective expected regret with known tradeoff

**Witness or lower-bound scope.** Randomized witness

$$
\Omega(\Psi_T^{B_\lambda}(S))
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $T\ge2$, two objectives, public $\lambda\ge\lambda_*\ge0$, and the stated compact anchor-plus-tie metric geometry.

**Dimension conditions.** Arbitrary compact tie component S; all metric dependence enters M_s.

**Constants.** Universal constants.

**Logarithmic factors.** Only the displayed horizon logarithm.

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:entropy; Appendix app:entropy

One-scale primary-tie lower bounds obeying the supplied envelope.. Every randomized causal policy with the same envelope.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Bo Xue; Ji Cheng; Fei Liu; Yimu Wang; Lijun Zhang; Qingfu Zhang. Lexicographic Lipschitz Bandits: New Algorithms and a Lower Bound. 2025. JMLR 26 (2025), published September 2025.

https://jmlr.org/papers/volume26/24-1047/24-1047.pdf

[2] Colombo_U07. Primary Ties and the Price of Unknown Trade-offs in Lexicographic Bandits. primary_ties_unknown_tradeoffs.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf
