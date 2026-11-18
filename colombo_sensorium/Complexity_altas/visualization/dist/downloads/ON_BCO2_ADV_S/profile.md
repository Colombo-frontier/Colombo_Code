# Adversarial convex bandits with two values of the same function and center loss

**Setting ID.** `ON_BCO2_ADV_S`

Online learning and bandits

The loss sequence is fixed in advance, and every loss has the same global Lipschitz bound. Each round the algorithm submits a center and two probes and receives two exact values of the current function. Only the center incurs loss; probes may lie outside the center's feasible set.

**Status.** Polynomial gap present

**TASK tags.** formulation: Adversarial two point convex external regret; solution concept: Minimize expected cumulative regret; task family: Online bandit

**MODEL tags.** convexity: Convex; convexity: Convex in action; smoothness: Pointwise lipschitz

**ORACLE tags.** derivative order: Order 0; feedback quality: Exact function values; interface family: Two point exact; operation: Evaluate same sample pair; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** measure: Native feedback; measure: Rounds

## 1. Setting specification

### Task

The loss sequence is fixed in advance, and every loss has the same global Lipschitz bound. Each round the algorithm submits a center and two probes and receives two exact values of the current function. Only the center incurs loss; probes may lie outside the center's feasible set.

### Admissible model

The fixed current loss is $F_t$. Every loss is convex and globally L-Lipschitz. There are no random sample functions or observation noise.

The loss-bearing center satisfies $x_t\in B_2^d(R)$ and incurs $F_t(x_t)$.

Two probes $z_t^+,z_t^-$ of the same function are chosen together and return two exact values; they may lie outside the ball.

Require $d,T\ge1$ and $L,R>0$.

Centers lie in $B_2^d(R)$; both probes may lie in $\mathbb R^d$.

### Oracle interface

Two exact values of the same current function:

$$
x_t\in B_2^d(R),\quad z_t^+,z_t^-\in\mathbb{R}^d\ \longmapsto\ \big(F_t(z_t^+),F_t(z_t^-)\big)
$$

The function $F_t$ is fixed before the action in round $t$.

Both probes are chosen jointly before either response and access the same function $F_t$.

There is no third feedback value at the center and no independent Gaussian scalar error.

Probes incur no separate loss. The center incurs $F_t(x_t)$ once.

The quantity $d,T,L,R$ is public, and every function is $L$-Lipschitz throughout $\mathbb{R}^d$.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\mathrm{Lip}_2(F_t)\le L\quad\forall t,\qquad R_T=\sum_tF_t(x_t)-\min_{u\in B_2^d(R)}\sum_tF_t(u)
$$

### Resource accounting

There are T sequential rounds, each giving two exact function values, for 2T values in total.

A symmetric two-point estimator and mirror descent attain the stated upper bound. Euclidean-ball updates may use projection.

The two function calls, internal direction sampling, and projection costs are separate.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}}\sup_{F_{1:T}}\mathbb{E}_{\mathcal{A}}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$L$: A Euclidean Lipschitz or gradient-norm bound on losses. **Domain:** $L>0$.

$|f(x)-f(y)|\le L\|x-y\|_2$. Function and point domains follow the declared model.

$R$: Euclidean-ball radius of the center-action set **Domain:** $R>0$.

$B_2^d(R)=\{x\in\mathbb R^d:\|x\|_2\le R\}$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$F_t$: Current round's convex loss, fixed before interaction **Domain:** Real-valued $L$-Lipschitz function on the full space.

$F_t:\mathbb R^d\to\mathbb R$.

$x_t,u$: Loss-incurring center and fixed comparator point **Domain:** $x_t,u\in B_2^d(R)$.

$z_t^+,z_t^-$: Two probes of the same current function **Domain:** $z_t^+,z_t^-\in\mathbb R^d$.

After joint submission, return $F_t(z_t^+),F_t(z_t^-)$; the center's function value is not additionally provided.

$\delta_{\mathrm{sm}},u_t,g_t$: Smoothing radius, spherical direction, and two-point gradient estimate **Domain:** Upper-bound algorithm quantity.

$g_t=\frac d{2\delta_{\mathrm{sm}}}[F_t(x_t+\delta_{\mathrm{sm}}u_t)-F_t(x_t-\delta_{\mathrm{sm}}u_t)]u_t$ There is no statistical confidence parameter.

$\varepsilon_t$: Independent uniform signs drawn before interaction in the lower bound. **Domain:** $\varepsilon_t\in\{-1,1\}$.

$f_t(x)=L\varepsilon_tx_1$.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_tF_t(x_t)-\min_{u\in B_2^d(R)}\sum_tF_t(u)$.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{F_{1:T}\in\mathcal I}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T F_t(x_t)-\min_{u\in B_2^d(R)}\sum_{t=1}^T F_t(u).\end{aligned}
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

The count $N=2T$ measures scalar value evaluations in the two-point protocol. Loss remains charged at the center.

$\mathcal I$: The complete environment class in the current minimax objective. **Domain:** Collection of function classes or reward-distribution classes.

The function sequence $F_t:\mathbb R^d\to\mathbb R$ is fixed before interaction. Every function is convex and globally $L$-Lipschitz. The two-point responses come from the same current function.

## 3. Complexity bracket

### Compared quantities

#### Q1 - cumulative regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{F_{1:T}\in\mathcal I}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T F_t(x_t)-\min_{u\in B_2^d(R)}\sum_{t=1}^T F_t(u).\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - MAIN

**Region.** $T\ge d\ge 1; L,R>0$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Polynomial gap

**Lower bound.** B2

$$
(LR/sqrt2)sqrtT
$$

**Upper bound.** B1

$$
C LRsqrt(dT)
$$

**Gap or comparison.** O(sqrt d)

**Comparison argument.** Only individually audited compatible claims enter. Evidence gap, not a claim that the deterministic two-point rate is mathematically open. Need a pointwise bounded hard family before strengthening lower.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require $T\ge d\ge1$ and $L,R>0$. After committing the center, query two exact values of the same current convex function; only the center incurs loss.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - Shamir symmetric two-point algorithm

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le C L R\sqrt{dT}
$$

**Sources.** [2](https://jmlr.org/papers/volume18/16-632/16-632.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** 2T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** The source reports average regret. Multiplication by $T$ gives cumulative regret under this specification. The submitted center incurs loss, while the two probes provide feedback from the current function; the interaction protocol is unchanged.

**Source location.** [2](https://jmlr.org/papers/volume18/16-632/16-632.pdf) theorem: Corollary 2; Theorem 1 proof; pdf pages: 1; 4; 5; 6; 7

The center $w_t$ incurs loss; the two probes in the same round provide only feedback. Multiply the source's average regret by $T$. In the random-sample variant, replace the pointwise squared Lipschitz bound with the sample Lipschitz constant's second moment.

### B2 - Full-information Rademacher loss lower, valid even with two exact probes after action

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge\frac{LR}{\sqrt2}\sqrt T
$$

**Sources.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** 2T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Take $f_t(x)=L\varepsilon_t x_1$. Once a center is submitted, even full revelation of the current function cannot change incurred loss. The hindsight comparator gains $LR\mathbb E|\sum_t\varepsilon_t|$. This yields a dimension-free lower bound, distinct from stronger constructions under a stochastic sample second-moment model.

**Source location.** [1](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf) theorem: Theorem 2; pdf pages: 5

The source lower bound is $\Omega(L\sqrt{T(D^2+DP)})$, with path budget in $[0,TD]$. An independent one-dimensional block construction on the Euclidean ball also checks the correspondence between geometry and path length.

## References

[1] Lijun Zhang; Shiyin Lu; Zhi-Hua Zhou. Adaptive Online Learning in Dynamic Environments. 2018. NeurIPS 2018 main paper.

https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf

[2] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. 2017. JMLR 18(52):1–11.

https://jmlr.org/papers/volume18/16-632/16-632.pdf
