# Adversarial convex bandits with exact one-point value feedback

**Setting ID.** `ON_BCO1_ADV_S`

Online learning and bandits

The environment precommits to a sequence of bounded convex losses. Each round, the learner acts in the unit ball and observes only the exact loss at its action. There is no observation noise; difficulty comes from the changing functions and one-point feedback.

**Status.** Polynomial gap present

**TASK tags.** formulation: Adversarial one point bandit convex external regret; solution concept: Minimize expected cumulative regret; task family: Online bandit

**MODEL tags.** convexity: Convex; convexity: Convex in action

**ORACLE tags.** derivative order: Order 0; feedback quality: Exact function value; interface family: One point value; operation: Evaluate loss at action; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** measure: Internal computation; measure: Native feedback; measure: Rounds

## 1. Setting specification

### Task

The environment precommits to a sequence of bounded convex losses. Each round, the learner acts in the unit ball and observes only the exact loss at its action. There is no observation noise; difficulty comes from the changing functions and one-point feedback.

### Admissible model

The unknown current convex function $f_t$ takes values in $[0,1]$ at all feasible points. No Lipschitz bound or continuity at the boundary of the closed domain is assumed. Define the comparator using the infimum and do not add an attainment assumption.

The action and sole value-query point is $x_t$. The same point incurs and returns the loss.

Require $d,T\ge1$; actual actions and query points lie in the Euclidean unit ball.

### Oracle interface

Exact function value at the action point:

$$
t,\ x_t\in B_2^d(1)\ \longmapsto\ Y_t=f_t(x_t)
$$

Choose $x_t$ first, then receive one exact function value at that point.

No gradient, second point, extra noise, or full-function feedback is supplied.

Consecutive-round functions may differ completely. A difference of values across rounds is not a finite difference of one function.

Public inputs are $d,T$, the unit-ball domain, the value range $[0,1]$, and convexity.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_T=\sum_t f_t(x_t)-\inf_{u\in B_2^d(1)}\sum_t f_t(u),\qquad f_t:B_2^d(1)\to[0,1]\ \mathrm{convex}
$$

### Resource accounting

One function value per round, for a total of $T$ scalar observations.

Any measurable causal policy is allowed.

The 2020 upper bound is an information-theoretic existence result; its feedback count does not establish an executable polynomial-time algorithm.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}}\sup_{f_{1:T}}\mathbb{E}_{\mathcal{A}}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$f_t$: Hidden convex loss in round t **Domain:** $f_t:B_2^d(1)\to[0,1]$.

Boundary continuity and Lipschitz continuity are not additionally required. The comparator uses an infimum.

$x_t,u$: The actual action and fixed comparison point. **Domain:** $x_t,u\in B_2^d(1)$.

$Y_t$: Exact current function value **Domain:** $Y_t=f_t(x_t)\in[0,1]$.

$\varepsilon_t$: Independent uniform signs in the hard linear subclass **Domain:** $\varepsilon_t\in\{-1,1\}$.

The hard loss is $f_t(x)=(1+\varepsilon_tx_1)/2$.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_tf_t(x_t)-\inf_{u\in B_2^d(1)}\sum_tf_t(u)$.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{f_{1:T}\in\mathcal I}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T f_t(x_t)-\inf_{u\in B_2^d(1)}\sum_{t=1}^T f_t(u).\end{aligned}
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

The quantity $N=T$ counts cumulative native scalar feedback under a one-point or one-arm protocol.

$\mathcal I$: The complete environment class in the current minimax objective. **Domain:** Collection of function classes or reward-distribution classes.

The convex-function sequence $f_t:B_2^d(1)\to[0,1]$ is fixed before interaction, with no additional smoothness, Lipschitz, or continuity promise.

## 3. Complexity bracket

### Compared quantities

#### Q1 - cumulative regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{f_{1:T}\in\mathcal I}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T f_t(x_t)-\inf_{u\in B_2^d(1)}\sum_{t=1}^T f_t(u).\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - MAIN

**Region.** $d\ge 1,T\ge 2$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Polynomial gap

**Lower bound.** B2

$$
c sqrtT
$$

**Upper bound.** B1, B3

$$
\min{T,C d^{5/2}sqrtT ln(2T)}
$$

**Gap or comparison.** The recorded ratio differs by at most order d^(5/2) log T; the current lower bound is only a compatible weaker baseline.

**Comparison argument.** Only individually audited compatible claims enter. Stochastic additive-Gaussian hidden-curvature lower cannot be transferred to this noiseless adversarial oracle.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require $d\ge1$ and $T\ge2$. Convex losses take values in $[0,1]$; the actual action incurs loss and returns one exact function value each round.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - Information-theoretic adversarial BCO algorithm

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le C d^{5/2}\sqrt T\log(2T)
$$

**Sources.** [1](https://tor-lattimore.com/downloads/papers/2020-cvx.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**internal computation.** unrestricted; efficient runtime not claimed

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** ln(2T)

**Source location.** [1](https://tor-lattimore.com/downloads/papers/2020-cvx.pdf) theorem: Theorem 1; pdf pages: 1

For adversarial convex losses on the unit ball, exact one-point feedback, and value range $[0,1]$, the source gives $Cd^{5/2}\sqrt T\log(2T)$. This is an information-theoretic upper bound without an efficient-internal-computation guarantee.

### B2 - Rademacher linear losses f_t(x)=(1+eps_t x_1)/2

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge c\sqrt T
$$

**Sources.** [2](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Use $f_t(x)=(1+\varepsilon_t x_1)/2$ with independent uniform signs $\varepsilon_t$. The functions are convex and take values in $[0,1]$. The learner's centered loss has zero expectation, while the hindsight action gains $\mathbb E|\sum_t\varepsilon_t|/2$. The lower bound holds even with full-gradient feedback, so it also applies to one-value feedback.

**Source location.** [2](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf) theorem: Theorem 2; pdf pages: 5

The source lower bound is $\Omega(L\sqrt{T(D^2+DP)})$, with path budget in $[0,TD]$. An independent one-dimensional block construction on the Euclidean ball also checks the correspondence between geometry and path length.

### B3 - Any feasible action sequence

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\mathcal{R}_T^*\le T
$$

**Sources.** [1](https://tor-lattimore.com/downloads/papers/2020-cvx.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Each realized loss lies in $[0,1]$, and comparator cumulative loss is nonnegative. Thus $R_T\le T$ pathwise, achieved by any fixed feasible action.

**Source location.** [1](https://tor-lattimore.com/downloads/papers/2020-cvx.pdf) theorem: Theorem 1; pdf pages: 1

For adversarial convex losses on the unit ball, exact one-point feedback, and value range $[0,1]$, the source gives $Cd^{5/2}\sqrt T\log(2T)$. This is an information-theoretic upper bound without an efficient-internal-computation guarantee.

## References

[1] Tor Lattimore. Improved Regret for Zeroth-Order Adversarial Bandit Convex Optimisation. 2020. Mathematical Statistics and Learning 2(3/4):311–334; author PDF.

https://tor-lattimore.com/downloads/papers/2020-cvx.pdf

[2] Lijun Zhang; Shiyin Lu; Zhi-Hua Zhou. Adaptive Online Learning in Dynamic Environments. 2018. NeurIPS 2018 main paper.

https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf
