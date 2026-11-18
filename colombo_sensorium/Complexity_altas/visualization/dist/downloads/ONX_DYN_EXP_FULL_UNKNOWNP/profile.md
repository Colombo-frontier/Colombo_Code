# Exp-concave dynamic online optimization: unknown Euclidean path budget and full information.

**Setting ID.** `ONX_DYN_EXP_FULL_UNKNOWNP`

Online learning and bandits

One learner must adapt to all comparator paths without knowing path length in advance. Losses are exponentially concave, path length is Euclidean, and the complete current function is revealed after acting.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Onx dyn exp full unknownp; task family: Online bandit

**MODEL tags.** convexity: Exp concavity; stochastic model: Comparator path

**ORACLE tags.** interface family: Full current function; operation: Full current function; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; public information: Unknown path

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

One learner must adapt to all comparator paths without knowing path length in advance. Losses are exponentially concave, path length is Euclidean, and the complete current function is revealed after acting.

### Admissible model

The learner acts in the same nonempty compact convex set $W\subset\mathbb{R}^d$ each round and competes simultaneously with every comparator path $u_{1:T}\in W^T$. Losses are differentiable and exp-concave on $W$:

$$
\operatorname{diam}_2(W)\le D,\qquad e^{-\eta f_t(\cdot)}\ \text{\text{on} }W\text{ \text{is concave}},\qquad \|\nabla f_t(w)\|_2\le G\quad(\forall t,\ w\in W).
$$

The upper bound holds for every admissible realized loss sequence; the recorded lower bound uses losses fixed before interaction. For dimension-optimality comparisons, $D,G,\eta$ are fixed independently of $d,T$.

Precisely, exponential concavity requires that in each round $t$, the map $x\mapsto\exp(-\eta f_t(x))$ be concave on the stated feasible domain. This property concerns the complete action variable; the norm and gradient bound are specified by this axis.

### Oracle interface

Submit $w_t\in W$, incur $f_t(w_t)$, then receive the complete function $f_t$. The function and its gradient may subsequently be evaluated at other points; feedback is noiseless.

The public projection interface supports exact Mahalanobis projection in any positive-definite metric $A\succ0$. The arithmetic cost of one such projection is $C_{\mathrm{proj}}(d)$.

$$
\Pi_W^A(z)\in\operatorname*{arg\,min}_{w\in W}(w-z)^{\mathsf T}A(w-z).
$$

Public inputs are $d,T,D,G,\eta$, the set $W$, and its projection interface.

Neither the comparator path $u_{1:T}$ nor its total path length $P_T^{(2)}$ is supplied to the algorithm.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
P_T^{(2)}(u)=\sum_{t=2}^{T}\|u_t-u_{t-1}\|_2,\qquad \operatorname{Reg}_T(u)=\sum_{t=1}^{T}\bigl(f_t(w_t)-f_t(u_t)\bigr).
$$

### Resource accounting

The quantity $T$ counts online rounds. The algorithm attaining the full frontier uses $O(\log T)$ loss evaluations, gradient evaluations, and Euclidean projections per round, including the internal computation of the exponentially concave branch.

The following formulas separately give total arithmetic work for dense spectral calculations and projections, and storage in real registers. Storage is not measured in bits.

$$\text{Arithmetic cost}=O\!\left(T\bigl(d^3+C_{\rm proj}(d)\bigr)\log^2(2T)\right),\qquad \text{Storage}=O\!\left(d^2\log^2(2T)\right).$$

This contract provides full-function feedback. A one-action-gradient version is a separate specification; the complete frontier here cannot be presented as requiring only one gradient per round.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

Any causal algorithm respecting information timing is allowed. Each realized action must belong to $W$.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

The upper bound is pathwise and deterministic: one algorithm satisfies it for every admissible loss sequence and comparator path simultaneously. In the lower-bound criterion below, expectation is only over learner randomness. The quantity $P$ is an analysis budget for the comparator class, not a known algorithm input.

$$
\inf_{\mathcal{A}}\ \sup_{\substack{f_{1:T}\ \text{\text{admissible}},\ u_{1:T}\in W^T\\ P_T^{(2)}(u)\le P}}\ \mathbb{E}_{\mathcal{A}}\!\left[\operatorname{Reg}_T(u)\right].
$$

## 2. Notation and parameters

$D$: A Euclidean-diameter bound on the action set. **Domain:** $D\ge0$.

The condition is $\sup_{x,y\in X}\|x-y\|_2\le D$; replace X by W when W denotes the action set.

$G$: Uniform Euclidean bound on the full loss gradient in each round **Domain:** $G>0$.

The condition $\|\nabla f_t(x)\|_2\le G$ holds for all t and x specified by the model.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\eta$: Exponential-concavity coefficient of the loss **Domain:** $\eta>0$.

The function $x\mapsto\exp(-\eta f_t(x))$ is concave on the action set. This parameter is not an algorithmic step size.

$P$: Euclidean comparator-path budget used only for stratified evaluation **Domain:** $0\le P\le D(T-1)$.

The comparator satisfies $P_T^{(2)}(u)=\sum_{t=2}^T\|u_t-u_{t-1}\|_2\le P$. A common algorithm may not tune to $P$.

$W$: Public nonempty compact convex action set **Domain:** $W\subset\mathbb R^d$.

$\operatorname{diam}_2(W)\le D$.

$w_t,u_t$: Learner action and current comparator location **Domain:** $w_t,u_t\in W$.

$f_t$: Current differentiable loss **Domain:** A real-valued function on W.

The function $\exp(-\eta f_t(\cdot))$ is concave, with Euclidean gradient norm at most G.

$P_T^{(2)}(u)$: Realized total Euclidean path length of the comparator **Domain:** $0\le P_T^{(2)}\le D(T-1)$.

$P_T^{(2)}(u)=\sum_{t=2}^T\|u_t-u_{t-1}\|_2$.

$\operatorname{Reg}_T(u)$: Dynamic regret relative to the complete comparator path **Domain:** Real number.

$\operatorname{Reg}_T(u)=\sum_t[f_t(w_t)-f_t(u_t)]$. One algorithm satisfies the upper bound simultaneously for all comparator paths.

$\Lambda_T$: Logarithmic factor appearing in the source upper bound **Domain:** Positive real number.

$\Lambda_T=1+\log(2T)$.

$c_0$: A positive universal constant in the source lower-bound horizon window. **Domain:** A fixed positive constant.

Require $T\ge c_0d^2$; the source gives no numerical value here, so none is assigned arbitrarily.

$A,C_{\mathrm{proj}}(d)$: The positive-definite metric for Mahalanobis projection and the cost of one exact projection. **Domain:** Positive definite matrix and arithmetic-operation count.

Metric projection minimizes $(x-y)^{\mathsf T}A(x-y)$; computational cost and loss-feedback count are measured separately.

$X$: Action-set notation in the ball-domain lower-bound slice **Domain:** Synonymous with $W$ in this parameter slice.

$X=W=B_2^d(1/2)$.

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

$N_{\mathrm{loss}},N_{\mathrm{grad}},N_{\mathrm{proj}}$: Function evaluations, gradient evaluations, and projections are counted separately. **Domain:** Nonnegative integer.

Each call type totals $O(T\log T)$ in the complete-frontier algorithm. This is not one gradient per round.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
P_T^{(2)}(u)=\sum_{t=2}^{T}\|u_t-u_{t-1}\|_2,\qquad \operatorname{Reg}_T(u)=\sum_{t=1}^{T}\bigl(f_t(w_t)-f_t(u_t)\bigr).
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Fix $X=B_2^d(1/2),D=1,G\ge 3/2,0<\eta\le 4/9$, with $T\ge c_0d^{2}$ and $0\le P\le T-1$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(d+\min\{d^{1/3}T^{1/3}P^{2/3},\sqrt{TP},T\})
$$

**Upper bound.** B1

$$
\widetilde{O}(d+\min\{d^{1/3}T^{1/3}P^{2/3},\sqrt{TP},T\})
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - Deterministic combination of the curvature learner and the full-information dynamic-gradient branch.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(d\Lambda_T^2+\min\!\left\{d^{1/3}\Lambda_T^{4/3}T^{1/3}\bigl(P_T^{(2)}\bigr)^{2/3},\ \sqrt{T\bigl(1+P_T^{(2)}\bigr)},\ T\right\}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.20187v1)

**Conditions.** The expression is $\Lambda_T=1+\log(2T)$, where $\log$ is the natural logarithm; $P_T^{(2)}=\sum_{t=2}^T\|u_t-u_{t-1}\|_2$.; The quantities $D,G,\eta$ are fixed independently of $d,T$. The complete frontier permits $O(\log T)$ additional evaluations per round; it is not a one-gradient-per-round result.

**Source location.** [1](https://arxiv.org/pdf/2610.20187v1) Corollary 4.2, PDF p.8, Eq.(6)

### B2 - Block construction with squared losses; lower bound for arbitrary randomized learners

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(d+\min\!\left\{d^{1/3}T^{1/3}P^{2/3},\ \sqrt{TP},\ T\right\}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.20187v1)

**Conditions.** The quantity $P\ge0$ is an analytical upper bound on the comparator's total Euclidean path length and need not be supplied to the learner. Assume $T\ge c_0d^2$, with dimension-independent $c_0>0$.; Use action set $W=B_2^d(1/2)$ and normalizations $D=1$, $G\le3/2$, and $\eta=4/9$, which also satisfy the weaker requirement $0<\eta\le4/9$. Construct losses $f_{j,y}(w)=(w_j-y)^2/2$, where $1\le j\le d$ and $y\in\{-1,1\}$.; This is a worst-case lower bound on the specified normalized domain. It does not apply uniformly to every fixed compact convex set.

**Source location.** [1](https://arxiv.org/pdf/2610.20187v1) Theorem 5.1, PDF pp.8–9, Eq.(8)

## References

[1] Yanyi Li; Wendao Wu; Haihan Zhang; Qinshi Wang; Chenheng Zhang; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Dimension-Optimal Dynamic Regret in Exp-Concave Online Learning. 2026. 2610.20187v1.

https://arxiv.org/pdf/2610.20187v1
