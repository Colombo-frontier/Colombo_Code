# Convex online optimization: known comparator-path budget and dynamic regret.

**Setting ID.** `ON_DYN_S`

Online learning and bandits

The learner acts in a Euclidean ball and receives action-point gradients, competing with comparator paths whose total movement obeys a public budget. The path restriction applies to the comparator, not to the learner's movement.

**Status.** Fully optimal

**TASK tags.** formulation: Online convex dynamic regret; solution concept: Minimize expected dynamic regret; task family: Online bandit

**MODEL tags.** convexity: Convex; convexity: Convex in action; stochastic model: Comparator path; stochastic model: Comparator path budget

**ORACLE tags.** feedback quality: Exact gradient; interface family: Action gradient; operation: Query gradient at action; public information: Hidden objects explicitly declared; public information: Known path; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** measure: Native feedback; measure: Projections; measure: Rounds

## 1. Setting specification

### Task

The learner acts in a Euclidean ball and receives action-point gradients, competing with comparator paths whose total movement obeys a public budget. The path restriction applies to the comparator, not to the learner's movement.

### Admissible model

The current loss is $f_t$; both convexity and the L gradient bound concern the function argument x.

The action and gradient-query point is $x_t$, chosen anywhere in the ball each round. The learner's own path is not restricted by $P$.

The comparator trajectory is $u_{1:T}$. Every $u_t$ lies in the ball, and total consecutive Euclidean displacement is at most $P$.

The public comparator budget $P$ is not a loss-function variation budget, reward-mean variation, or environment-noise parameter.

Assume $d,T\ge1$, $L,R>0$, and $0\le P\le2R(T-1)$.

The learner acts in B2^d(R); the comparator domain is the complete constrained trajectory class $\mathcal{U}$(P).

### Oracle interface

Exact gradient at the action point:

$$
t,\ x_t\in B_2^d(R)\ \longmapsto\ g_t=\nabla f_t(x_t)
$$

Choose $x_t$ and incur $f_t(x_t)$ before observing its gradient.

The interface does not supply the optimal comparator $u_t$, complete function, or gradients at other points in the same round.

Feedback has no observation noise and does not additionally return the function value $f_t(x_t)$.

Public inputs are $d,T,L,R$ and comparator path-length budget $P$.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\mathcal{U}(P)=\{u_{1:T}\in(B_2^d(R))^T:\sum_{t=2}^T\|u_t-u_{t-1}\|_2\le P\},\quad R_T(P)=\sum_t f_t(x_t)-\min_{u_{1:T}\in\mathcal{U}(P)}\sum_t f_t(u_t)
$$

### Resource accounting

One d-dimensional gradient per round, totaling T calls. The upper-bound algorithm additionally uses T ball projections.

Projected OGD knowing P may tune its step size to P; the algorithm class also allows other causal strategies.

Each iteration uses O(d) vector work and one projection onto the public ball. The reported quantity is regret, not optimal projection complexity.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}(d,T,L,R,P)}\sup_{f_{1:T}}\mathbb{E}_{\mathcal{A}}[R_T(P)]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$L$: A Euclidean Lipschitz or gradient-norm bound on losses. **Domain:** $L>0$.

The condition $\|\nabla f_t(x)\|_2\le L$ holds throughout the action domain.

$P$: Public budget for comparator path length in the Euclidean norm **Domain:** $0\le P\le2R(T-1)$.

The comparator obeys $\sum_{t=2}^T\|u_t-u_{t-1}\|_2\le P$. This restricts neither the learner's path nor changes in environmental functions.

$R$: Euclidean-ball radius of the center-action set **Domain:** $R>0$.

$B_2^d(R)=\{x\in\mathbb R^d:\|x\|_2\le R\}$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$f_t$: Obliviously chosen differentiable convex loss in round $t$ **Domain:** Real-valued function defined on a neighborhood of the action ball.

$x_t$: Actual action and gradient-query point **Domain:** $x_t\in B_2^d(R)$.

$u_{1:T},\mathcal U(P)$: The comparator trajectory and allowed trajectory class. **Domain:** $u_t\in B_2^d(R)$.

$\mathcal U(P)=\{u_{1:T}:\sum_{t=2}^T\|u_t-u_{t-1}\|_2\le P\}$.

$D$: Action-domain diameter in the source dynamic-regret theorem **Domain:** Used only to map the source formula.

$D=2R$.

$\eta$: Projected-gradient step size chosen using the public budget $P$ **Domain:** Positive real number.

$\eta=\sqrt{(14R^2+4RP)/(TL^2)}$.

$m,\varepsilon_t$: The number of lower-bound blocks and independent uniform signs. **Domain:** Used only to construct hard instances.

$m=\min\{T,1+\lfloor P/(2R)\rfloor\}$; $\varepsilon_t\in\{-1,1\}$.

$R_T(P)$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_tf_t(x_t)-\min_{u_{1:T}\in\mathcal U(P)}\sum_tf_t(u_t)$.

$\mathcal R_T^*(P)$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*(P)&=\inf_{\mathcal A(P)}\sup_{f_{1:T}\in\mathcal I}\mathbb E_{\mathcal A}[R_T(P)],\\ R_T(P)&=\sum_{t=1}^T f_t(x_t)-\inf_{u_{1:T}\in\mathcal U(P)}\sum_{t=1}^T f_t(u_t),\\ \mathcal U(P)&=\left\{u_{1:T}\in(B_2^d(R))^T:\sum_{t=2}^T\|u_t-u_{t-1}\|_2\le P\right\}.\end{aligned}
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

$B_2^d(r)$: Closed Euclidean ball of radius r **Domain:** $r\ge0$.

$B_2^d(r)=\{x\in\mathbb R^d:\|x\|_2\le r\}$. The symbol r is a placeholder radius, instantiated as R or 1 in the relevant specification.

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The quantity $N=T$ counts full-gradient or subgradient responses. Projection, proximal, and matrix operations are counted separately.

$\mathcal I$: The complete environment class in the current minimax objective. **Domain:** Collection of function classes or reward-distribution classes.

A convex loss sequence is fixed before interaction. Each function is differentiable on a neighborhood of $B_2^d(R)$ and has gradient norm at most L inside the ball. Comparator paths are separately constrained by $\mathcal U(P)$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax cumulative dynamic regret

$$
\begin{aligned}\mathcal R_T^*(P)&=\inf_{\mathcal A(P)}\sup_{f_{1:T}\in\mathcal I}\mathbb E_{\mathcal A}[R_T(P)],\\ R_T(P)&=\sum_{t=1}^T f_t(x_t)-\inf_{u_{1:T}\in\mathcal U(P)}\sum_{t=1}^T f_t(u_t),\\ \mathcal U(P)&=\left\{u_{1:T}\in(B_2^d(R))^T:\sum_{t=2}^T\|u_t-u_{t-1}\|_2\le P\right\}.\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - ALL

**Region.** $d,T\ge 1; L,R>0; 0\le P\le 2R(T-1)$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2

$$
c Lsqrt[T(R^2+RP)]
$$

**Upper bound.** B1

$$
C Lsqrt[T(R^2+RP)]
$$

**Gap or comparison.** Universal constants.

**Comparison argument.** Admit only individually checked claims compatible with this contract.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require $d,T\ge1$, $L,R>0$, and $0\le P\le2R(T-1)$. The comparator path lies in a Euclidean ball of radius $R$ and has total Euclidean length at most $P$.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - Projected OGD tuned to supplied P

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\mathcal{R}_T^*(P)\le C L\sqrt{T(R^2+RP)}
$$

**Sources.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T gradients

**projections.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Set the source diameter parameter to $D=2R$. Projected online gradient descent has dynamic regret bound $(7D^2/4+DP)/\eta+\eta TL^2/2$.

Choose $\eta=\sqrt{(7D^2/2+2DP)/(TL^2)}$. The inequality holds simultaneously for every feasible comparator path, so the best path may be selected in hindsight inside the expectation.

**Source location.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf) theorem: Theorem 1; pdf pages: 4

Projected online gradient descent has dynamic regret at most $7D^2/(4\eta)+DP/\eta+\eta TL^2/2$, with its step size tuned using the public path budget.

### B2 - Rademacher linear losses in independently signed blocks

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*(P)\ge c L\sqrt{T(R^2+RP)}
$$

**Sources.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Split the horizon into $m=\min\{T,1+\lfloor P/(2R)\rfloor\}$ approximately equal blocks and use independent Rademacher linear losses in the first coordinate. In each block the comparator is the radius endpoint opposite to that block's cumulative sign; its path length is at most $2R(m-1)\le P$. Expected regret is at least $cLR\sqrt{mT}$. Under $P\le2R(T-1)$, the number of blocks has order $1+P/R$, giving $cL\sqrt{T(R^2+RP)}$. The loss sequence is sampled before interaction, and averaging yields an oblivious deterministic witness against each randomized learner.

**Source location.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf) theorem: Theorem 2; pdf pages: 5

The source lower bound is $\Omega(L\sqrt{T(D^2+DP)})$, with path budget in $[0,TD]$. An independent one-dimensional block construction on the Euclidean ball also checks the correspondence between geometry and path length.

## References

[1] Lijun Zhang; Shiyin Lu; Zhi-Hua Zhou. Adaptive Online Learning in Dynamic Environments. 2018. NeurIPS 2018 main paper.

https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf
