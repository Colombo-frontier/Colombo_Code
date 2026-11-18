# Convex dynamic online optimization with an unknown path budget and one-gradient feedback

**Setting ID.** `ONX_DYN_CONVEX_UNKNOWNP`

Online learning and bandits

One learner must adapt to all comparator paths without knowing path length in advance. Losses are convex with bounded gradients, and path length is Euclidean. Each round reveals only the gradient at the chosen action.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Onx dyn convex unknownp; task family: Online bandit

**MODEL tags.** convexity: Convex; stochastic model: Comparator path

**ORACLE tags.** interface family: Action gradient; operation: Action gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; public information: Unknown path

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

One learner must adapt to all comparator paths without knowing path length in advance. Losses are convex with bounded gradients, and path length is Euclidean. Each round reveals only the gradient at the chosen action.

### Admissible model

The public compact convex set $X\subset\mathbb{R}^d$ contains the origin and has Euclidean diameter at most $D$. Losses are differentiable and convex and satisfy $\|\nabla f_t(x)\|_2\le G$. The environment may depend on past history but cannot anticipate current private randomness.

### Oracle interface

Each round submits the final principal action $x_t\in X$ before receiving its one exact gradient. Internal experts do not separately query gradients at their own actions.

Euclidean projection onto $X$ is available. The learner is causal and cannot depend on the comparator or its path budget.

The data $T,X,D,G$ are public. The comparator path $u_{1:T}$ and its total Euclidean length are hidden.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
P_T^{(2)}(u)=\sum_{t=2}^{T}\|u_t-u_{t-1}\|_2,\qquad \operatorname{Reg}_T(u)=\sum_{t=1}^{T}\bigl(f_t(x_t)-f_t(u_t)\bigr).
$$

### Resource accounting

$$N=T\quad\text{subgradient queries},\qquad O(T\log T)\quad\text{internal expert projections}.$$

Gradient calls and internal projections are accounted for separately.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

One algorithm satisfies the pathwise upper bound simultaneously for all $u_{1:T}\in X^T$. The quantity $P_T^{(2)}$ is used only in the analysis and is not a runtime input.

## 2. Notation and parameters

$D$: A Euclidean-diameter bound on the action set. **Domain:** $D\ge0$.

The condition is $\sup_{x,y\in X}\|x-y\|_2\le D$; replace X by W when W denotes the action set.

$G$: Uniform Euclidean bound on the full loss gradient in each round **Domain:** $G>0$.

The condition $\|\nabla f_t(x)\|_2\le G$ holds for all t and x specified by the model.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$P$: Euclidean comparator-path budget used only for stratified evaluation **Domain:** $0\le P\le D(T-1)$.

The comparator satisfies $P_T^{(2)}(u)=\sum_{t=2}^T\|u_t-u_{t-1}\|_2\le P$. A common algorithm may not tune to $P$.

$X,x_t,u_t$: Public action domain, primary action, and comparator location **Domain:** $x_t,u_t\in X\subset\mathbb R^d$.

The set X contains the origin and has Euclidean diameter at most D.

$P_T^{(2)}(u)$: Realized total Euclidean path length of the comparator **Domain:** $0\le P_T^{(2)}\le D(T-1)$.

The quantity $P_T^{(2)}(u)=\sum_{t=2}^T\|u_t-u_{t-1}\|_2$ is not supplied to the algorithm.

$\operatorname{Reg}_T(u)$: Dynamic regret relative to the entire comparator trajectory **Domain:** Real number.

$\sum_t[f_t(x_t)-f_t(u_t)]$.

$k_{\mathrm{index}}$: Index of the step-size expert matched to the path length in the analysis **Domain:** Positive integer.

Assume $k_{\mathrm{index}}=\lfloor\frac12\log_2(1+4P_T^{(2)}/(7D))\rfloor+1$; the singleton-domain case $D=0$ additionally has zero regret.

$R,L$: Radius and gradient-bound aliases used in the lower-bound argument **Domain:** Used only to explain the source coordinate transformation.

Require $R=D/2$ and $L=G$. The displayed lower bound is expressed in the local D and G notation.

$\mathcal R_T^*$: Worst-case expected-regret comparison under the same budget slice and information restrictions **Domain:** A nonnegative real.

The upper bound for an unknown budget must be attained by one policy that does not receive that budget. The lower bound applies to every such policy. Different algorithms cannot be chosen retrospectively for different hidden budgets.

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

The quantity $N=T$ counts full-gradient or subgradient responses. Projection, proximal, and matrix operations are counted separately.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
P_T^{(2)}(u)=\sum_{t=2}^{T}\|u_t-u_{t-1}\|_2,\qquad \operatorname{Reg}_T(u)=\sum_{t=1}^{T}\bigl(f_t(x_t)-f_t(u_t)\bigr).
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** The set X is a Euclidean ball, with $D=2R$ and $0\le P\le D(T-1)$. One algorithm must operate without P as input.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
cG\sqrt{T(D^2/4+DP/2)}
$$

**Upper bound.** B1

$$
O(G\sqrt{T(D^2+DP)}[1+\log\log(2+P/D)])
$$

## 4. Bounds and supporting evidence

### B1 - Improved Ader: expert aggregation sharing one gradient.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\begin{gathered}\frac{3G}{4}\sqrt{2T\bigl(7D^2+4DP_T^{(2)}\bigr)}+\frac{GD\sqrt{2T}}2\bigl[1+2\log(k_{\mathrm{index}}+1)\bigr],\\ k_{\mathrm{index}}=\left\lfloor\frac12\log_2\!\left(1+\frac{4P_T^{(2)}}{7D}\right)\right\rfloor+1.\end{gathered}
$$

**Sources.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf)

**Conditions.** The information $T,D,G$ is supplied, while $P_T^{(2)}$ is not. The quantity $k_{\mathrm{index}}$ is an analysis-scale index, not a representation rank or an unknown budget required as an algorithm input.; This implementation uses exactly one gradient at the principal action per round. Basic Ader with full-function feedback is a separate implementation.

**Oracle correspondence.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

**Source location.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf) Theorem 4, PDF p.7

### B2 - Rademacher linear losses in independently signed blocks

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal R_T^*(P)\ge cG\sqrt{T(D^2/4+DP/2)}
$$

**Sources.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf)

**Conditions.** Require $d,T\ge1$, $D,G>0$, and $0\le P\le D(T-1)$. The construction uses a Euclidean ball of radius $D/2$ and gradients of norm at most G.; The lower bound uses this ball-domain slice of the admissible domain class. The comparator-path budget is not given to the algorithm.

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

**Derivation.** A randomized lower bound that holds even when the path budget $P$ is public also applies to strategies not given $P$. The comparison uses a Euclidean-ball slice and preserves the normalization of $D=2R$ and $G=L$.

**Source location.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf) theorem: Theorem 2; pdf pages: 5

Use the independent-block construction on the Euclidean ball with radius $D/2$ and gradient bound G to obtain $cG\sqrt{T(D^2/4+DP/2)}$. Strategies unaware of P form a restricted class also covered by this lower bound.

## References

[1] Lijun Zhang; Shiyin Lu; Zhi-Hua Zhou. Adaptive Online Learning in Dynamic Environments. 2018. NeurIPS 2018 main paper.

https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf
