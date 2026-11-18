# Convex online optimization on a Euclidean ball: action-point gradients and static regret

**Setting ID.** `ON_OCO_S`

Online learning and bandits

The learner acts in a public Euclidean ball and receives the full gradient at its action only after incurring the loss. Every loss is convex with bounded gradient. The comparator is the best single fixed point in the ball over the horizon.

**Status.** Fully optimal

**TASK tags.** formulation: Online convex external regret; solution concept: Minimize expected cumulative regret; task family: Online bandit

**MODEL tags.** convexity: Convex; convexity: Convex in action

**ORACLE tags.** feedback quality: Exact gradient; interface family: Action gradient; operation: Query gradient at action; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Projections; measure: Rounds

## 1. Setting specification

### Task

The learner acts in a public Euclidean ball and receives the full gradient at its action only after incurring the loss. Every loss is convex with bounded gradient. The comparator is the best single fixed point in the ball over the horizon.

### Admissible model

The current hidden convex loss is $f_t$. Convexity and the gradient bound apply to its x argument. Differentiability does not imply a Lipschitz gradient; smoothness and strong convexity are not added.

The feasible action and gradient query point is $x_t$. The same point incurs loss and returns a gradient.

The hindsight fixed comparator $u$ is one point in the ball used throughout the horizon.

Require $d,T\ge1$ and $L,R>0$.

Both the action and gradient-query domains are B₂ᵈ(R).

### Oracle interface

Exact gradient at the action point:

$$
t,\ x_t\in B_2^d(R)\ \longmapsto\ g_t=\nabla f_t(x_t)
$$

The current function $f_t$ is fixed before interaction but remains hidden. The learner first submits $x_t$, then receives one complete $d$-dimensional gradient.

The interface supplies no same-round gradients at other points, Hessians, or complete function $f_t$.

The value $f_t(x_t)$ is not additionally promised as feedback. Inclusion of a loss in the objective does not mean the learner observes it.

Public inputs: d, T, L, R, and the Euclidean ball domain.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
x_t\in B_2^d(R),\quad f_t\ \mathrm{convex},\quad \|\nabla f_t(x)\|_2\le L,\qquad R_T=\sum_t f_t(x_t)-\min_{u\in B_2^d(R)}\sum_t f_t(u)
$$

### Resource accounting

One $d$-dimensional gradient per round, for a total of $T$ gradient responses.

Any causal strategy is allowed; the projected-OGD upper bound uses only the current gradient.

Each OGD iteration uses one Euclidean-ball projection and O(d) vector operations. Projection onto the public domain is internal computation, not an additional loss query.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}}\sup_{f_{1:T}}\mathbb{E}_{\mathcal{A}}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$L$: A Euclidean Lipschitz or gradient-norm bound on losses. **Domain:** $L>0$.

The condition $\|\nabla f_t(x)\|_2\le L$ holds throughout the action domain.

$R$: Euclidean-ball radius of the center-action set **Domain:** $R>0$.

$B_2^d(R)=\{x\in\mathbb R^d:\|x\|_2\le R\}$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$f_t$: Obliviously fixed differentiable convex loss in round $t$ **Domain:** Real-valued function defined on a neighborhood of the action ball.

$x_t$: Actual action and sole gradient-query point **Domain:** $x_t\in B_2^d(R)$.

$u$: Best fixed comparator point in hindsight **Domain:** $u\in B_2^d(R)$.

$g_t$: The complete exact gradient at the action. **Domain:** $g_t\in\mathbb R^d$.

$g_t=\nabla f_t(x_t)$.

$\eta$: Step size of projected online gradient descent **Domain:** Positive real number.

$\eta=2R/(L\sqrt T)$.

$\varepsilon_t$: Independent uniform signs in the lower-bound construction **Domain:** $\Pr(\varepsilon_t=1)=\Pr(\varepsilon_t=-1)=1/2$.

Drawn before interaction and used only in the hard-instance proof.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_tf_t(x_t)-\min_{u\in B_2^d(R)}\sum_tf_t(u)$.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{f_{1:T}\in\mathcal I}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T f_t(x_t)-\min_{u\in B_2^d(R)}\sum_{t=1}^T f_t(u).\end{aligned}
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

A sequence of $T$ convex functions fixed before interaction. Each is differentiable near $B_2^d(R)$ and satisfies $\|\nabla f_t(x)\|_2\le L$ on the ball.

## 3. Complexity bracket

### Compared quantities

#### Q1 - cumulative regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{f_{1:T}\in\mathcal I}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T f_t(x_t)-\min_{u\in B_2^d(R)}\sum_{t=1}^T f_t(u).\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - ALL

**Region.** $d,T\ge 1; L,R>0$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2

$$
(LR/sqrt2)sqrtT
$$

**Upper bound.** B1

$$
2LRsqrtT
$$

**Gap or comparison.** ≤2sqrt2

**Comparison argument.** Admit only individually checked claims compatible with this contract.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require integers $d,T\ge1$ and $L,R>0$. The feasible domain is a Euclidean ball of radius $R$, and losses are convex and $L$-Lipschitz.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - Projected online gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\mathcal{R}_T^*\le2LR\sqrt T
$$

**Sources.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T gradients

**projections.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Fix any comparator $u$. Convexity and nonexpansiveness of projection bound regret by $\|x_1-u\|_2^2/(2\eta)+\eta L^2T/2$. The ball has diameter $2R$, giving $2R^2/\eta+\eta L^2T/2$. Choose step size $\eta=2R/(L\sqrt T)$. The inequality holds for every realized loss sequence and every $u$ simultaneously, including the hindsight optimizer.

**Source location.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf) theorem: Theorem 1; pdf pages: 4

Projected online gradient descent has dynamic regret at most $7D^2/(4\eta)+DP/\eta+\eta TL^2/2$, with its step size tuned using the public path budget.

### B2 - Independent Rademacher linear losses on first coordinate

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge cLR\sqrt T
$$

**Sources.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Use linear losses $f_t(x)=L\varepsilon_t x_1$ with independent uniform signs $\varepsilon_t$ sampled before interaction. Every causal learner has zero expected cumulative loss, whereas the best fixed action has cumulative loss $-LR|\sum_t\varepsilon_t|$. Khintchine's inequality gives $\mathbb E|\sum_t\varepsilon_t|\ge\sqrt{T/2}$. Averaging over the sampled sequence yields a deterministic oblivious sequence attaining the corresponding expected regret for the randomized learner.

**Source location.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf) theorem: Theorem 2; pdf pages: 5

The source lower bound is $\Omega(L\sqrt{T(D^2+DP)})$, with path budget in $[0,TD]$. An independent one-dimensional block construction on the Euclidean ball also checks the correspondence between geometry and path length.

## References

[1] Lijun Zhang; Shiyin Lu; Zhi-Hua Zhou. Adaptive Online Learning in Dynamic Environments. 2018. NeurIPS 2018 main paper.

https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf
