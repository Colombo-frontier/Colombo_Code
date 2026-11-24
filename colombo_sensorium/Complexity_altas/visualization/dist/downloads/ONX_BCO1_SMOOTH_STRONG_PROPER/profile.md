# Proper one-point bandits with smooth strongly convex losses on known convex bodies

**Setting ID.** `ONX_BCO1_SMOOTH_STRONG_PROPER`

Online learning and bandits

Expected static regret with exact bounded one-point feedback, feasible actions, and explicit domain conditioning and curvature budgets.

**Status.** Logarithmic gap; Other quantified gap

**Gap classes present.** Logarithmic gap; Other quantified gap

**TASK tags.** solution concept: Online regret minimization; task family: Online bandit

**MODEL tags.** convexity: Strongly convex; smoothness: Lipschitz gradient

**ORACLE tags.** derivative order: Order 0; feedback quality: Exact; operation: Played point loss value; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**GUARANTEE tags.** mode: Expectation; quantifier: Algorithm before instance

**RESOURCE tags.** measure: T

## 1. Setting specification

### Task

Minimize expected static regret for proper one-point adversarial bandit convex optimization on a known compact convex body, allowing boundary comparators.

### Admissible model

The public domain belongs to $\mathcal K_d=\{K:(4d)^{-1}B_2^d\subseteq K\subseteq B_2^d,\ K\text{ compact and convex}\}$. Every loss is the restriction of a continuously differentiable function on a neighborhood of $K$, takes values in $[0,1]$ on $K$, is $\mu$-strongly convex, and is $\beta$-smooth in the Euclidean norm on $K$. No globally bounded strongly convex extension is assumed.

An oblivious adversary fixes the loss sequence before the learner seed is drawn. The domain is known, the losses are hidden, and $0<\mu\le\beta$. Only domains with a nonempty loss class are included. The family is nonempty exactly when $\mu\le32d^2$.

### Oracle interface

At round $t$, play $X_t\in K$, incur $f_t(X_t)$, and observe exactly this scalar. No gradient, extra value query, or query outside $K$ is available. The domain, horizon, and curvature budgets are public. Exact computations using the known domain are free; no additional loss information is included.

### Output

The executed actions must be feasible almost surely at every round. The static comparator is the minimizer of the cumulative loss over the same domain and can lie on its boundary.

### Loss or accuracy criterion

$R_T=\sum_{t=1}^T f_t(X_t)-\min_{u\in K}\sum_{t=1}^T f_t(u)$. The minimax risk is $\mathfrak R^*_{T,\mathrm{sc}}(d;\mu,\beta)=\sup_{K\in\mathcal K_d:\mathcal F(K;\mu,\beta)\ne\varnothing}\inf_A\sup_{f_{1:T}}\mathbb E_A R_T$. The algorithm may depend on the known domain before the losses are selected.

### Resource accounting

One exact scalar observation per round; the budget is the fixed horizon $T$. Geometric computation, internal arithmetic, and storage are not charged.

### Algorithm views and success guarantees

All measurable randomized causal proper one-point policies are allowed. Computation on the known domain is unrestricted.

$$
\sup_{f_{1:T}}\mathbb E_A R_T\le r
$$

The guarantee is uniform over admissible oblivious loss sequences for each public domain; the risk subsequently takes the worst admissible domain.

**Budget convention.** fixed_horizon

## 2. Notation and parameters

$d$: Euclidean dimension **Domain:** $d\in\mathbb N_{\ge1}$.

$T$: Horizon **Domain:** $T\in\mathbb N_{\ge1}$.

$\mu$: Strong-convexity lower bound **Domain:** $0<\mu\le32d^2$.

$\beta$: Gradient-Lipschitz upper bound **Domain:** $\beta\ge\mu$.

$\kappa$: Condition number **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu$

$K$: Known feasible convex body **Domain:** $(4d)^{-1}B_2^d\subseteq K\subseteq B_2^d$.

$R_b$: Radius used only to index the admissible ball lower-bound subclass **Domain:** $R_b\in[(4d)^{-1},1]$.

$M_b$: Curvature scale of the ball lower-bound subclass **Domain:** $0<M_b<2$.

$M_b=\mu R_b^2$

$\Delta_b$: Bounded-loss headroom on the lower-bound ball **Domain:** $\Delta_b>0$.

$\Delta_b=1-M_b/2$

$Q_b$: Lower-bound scale **Domain:** $Q_b>0$.

$Q_b=\min\{M_b,\Delta_b^2/M_b\}$

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
\mathfrak R^*_{T,\mathrm{sc}}(d;\mu,\beta)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $T$; description: Each played round and its prescribed feedback are charged.

### R1 - Fixed positive curvature: joint dimension–horizon rate

**Region.** Fix $0<\mu\le\beta<\infty$ independently of $d,T$. Require $d,T\ge1$ integers and $\mu<32d^2$. Every finite dimension satisfying the explicit nondegeneracy condition.

**Quantity.** Q1

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega_{\mu}\!\left(\min\{T,d\sqrt T\}\right)
$$

**Upper bound.** B1

$$
O_{\mu,\beta}\!\left(\min\{T,d\log(ed)\sqrt{T\log(edT)}\}\right)
$$

**Gap or comparison.** Only logarithmic factors in dimension and horizon remain.

### R2 - Varying curvature and a specified admissible ball witness

**Region.** $d,T\ge1$, $0<\mu\le\beta$, $\mu<32d^2$; choose $R_b\in[(4d)^{-1},1]$ with $M_b=\mu R_b^2<2$, $\Delta_b=1-M_b/2$, and $Q_b=\min\{M_b,\Delta_b^2/M_b\}$. Every finite d with an admissible witness radius. The lower bound holds for each admissible witness radius and hence for the worst-domain risk; it does not state a lower bound on every individual convex body.

**Quantity.** Q1

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Other quantified gap

**Lower bound.** B4

$$
\frac{1}{1024\pi}\min\{Q_bT,\Delta_bd\sqrt T\}
$$

**Upper bound.** B3

$$
O\!\left(\min\{T,d\sqrt{T[\log^2(ed)\log(edT\kappa)+\kappa\log(eT)]}\}\right)
$$

**Gap or comparison.** The upper bound contains sqrt(kappa) dependence; this lower bound does not establish matching joint dependence on varying curvature or loss headroom.

### R3 - Degenerate maximal-curvature endpoint

**Region.** $d,T\ge1$, $\mu=32d^2$, and $\beta\ge\mu$. Every finite d.

**Quantity.** Q1

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Optimal

**Lower bound.** B6

$$
0
$$

**Upper bound.** B5

$$
0
$$

**Gap or comparison.** The minimax regret equals zero.

## 4. Bounds and supporting evidence

### B1 - Feasible covariance-local exploration, compact smoothing, and quadratic exponential weights.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O_{\mu,\beta}\!\left(\min\{T,d\log(ed)\sqrt{T\log(edT)}\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf)

**Conditions.** Fix $0<\mu\le\beta<\infty$ independently of $d,T$. Require $d,T\ge1$ integers and $\mu<32d^2$.

**Dimension conditions.** Every finite dimension satisfying the explicit nondegeneracy condition.

**Constants.** The lower constant may depend on the fixed positive mu; the upper constant may depend on the fixed pair (mu,beta), but neither depends on d or T.

**Logarithmic factors.** Displayed logarithms in d and T; no polynomial dimension dependence is suppressed.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf) Corollary cor:fixed; equation eq:fixedmatching; Theorem thm:main

Feasible covariance-local exploration, compact smoothing, and quadratic exponential weights.. Proper randomized one-point policies.

### B2 - Bounded quadratic losses with compactly supported offsets and an adaptive Hellinger argument.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\Omega_{\mu}\!\left(\min\{T,d\sqrt T\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf)

**Conditions.** Fix $0<\mu\le\beta<\infty$ independently of $d,T$. Require $d,T\ge1$ integers and $\mu<32d^2$.

**Dimension conditions.** Every finite dimension satisfying the explicit nondegeneracy condition.

**Constants.** The lower constant may depend on the fixed positive mu; the upper constant may depend on the fixed pair (mu,beta), but neither depends on d or T.

**Logarithmic factors.** Displayed logarithms in d and T; no polynomial dimension dependence is suppressed.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf) Corollary cor:fixed; Theorem thm:lowergeneral; Appendix app:fixed

Bounded quadratic losses with compactly supported offsets and an adaptive Hellinger argument.. Every randomized causal proper one-point policy.

### B3 - Proper one-point exploration and quadratic exponential weights.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\min\{T,d\sqrt{T[\log^2(ed)\log(edT\kappa)+\kappa\log(eT)]}\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf)

**Conditions.** $d,T\ge1$, $0<\mu\le\beta$, $\mu<32d^2$; choose $R_b\in[(4d)^{-1},1]$ with $M_b=\mu R_b^2<2$, $\Delta_b=1-M_b/2$, and $Q_b=\min\{M_b,\Delta_b^2/M_b\}$.; The lower bound holds for each admissible witness radius and hence for the worst-domain risk; it does not state a lower bound on every individual convex body.

**Dimension conditions.** Every finite d with an admissible witness radius.

**Constants.** Universal constants.

**Logarithmic factors.** The upper logarithms are displayed explicitly.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf) Theorem thm:main; equation eq:generalupper

Proper one-point exploration and quadratic exponential weights.. Randomized proper policies; uniform over every admissible K.

### B4 - The admissible ball K=R_b B_2^d with Hessian exactly mu I.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\frac{1}{1024\pi}\min\{Q_bT,\Delta_bd\sqrt T\}
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf)

**Conditions.** $d,T\ge1$, $0<\mu\le\beta$, $\mu<32d^2$; choose $R_b\in[(4d)^{-1},1]$ with $M_b=\mu R_b^2<2$, $\Delta_b=1-M_b/2$, and $Q_b=\min\{M_b,\Delta_b^2/M_b\}$.; The lower bound holds for each admissible witness radius and hence for the worst-domain risk; it does not state a lower bound on every individual convex body.

**Dimension conditions.** Every finite d with an admissible witness radius.

**Constants.** Universal constants.

**Logarithmic factors.** The upper logarithms are displayed explicitly.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf) Theorem thm:lowergeneral; equation eq:lowergeneral

The admissible ball K=R_b B_2^d with Hessian exactly mu I.. Every proper randomized one-point policy on the ball subclass.

### B5 - Play the origin.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf)

**Conditions.** $d,T\ge1$, $\mu=32d^2$, and $\beta\ge\mu$.

**Dimension conditions.** Every finite d.

**Constants.** Universal constants.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf) Proposition prop:admissibility; equations eq:diamcurvature and subsequent proof

Play the origin.. Deterministic policy suffices.

### B6 - The unique admissible domain is K=(4d)^(-1)B_2^d and its unique admissible loss is mu||x||^2/2.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf)

**Conditions.** $d,T\ge1$, $\mu=32d^2$, and $\beta\ge\mu$.

**Dimension conditions.** Every finite d.

**Constants.** Universal constants.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf) Proposition prop:admissibility

The unique admissible domain is K=(4d)^(-1)B_2^d and its unique admissible loss is mu||x||^2/2.. All policies.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_U01. Near-Optimal Proper Bandit Optimization with Smooth Strongly Convex Losses. colombo_proper_bandit.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U01/manuscript.pdf
