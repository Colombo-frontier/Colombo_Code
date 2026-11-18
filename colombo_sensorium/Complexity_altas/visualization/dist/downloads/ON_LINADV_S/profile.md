# Adversarial linear bandits on a Euclidean ball: bounded loss vectors and exact projection feedback.

**Setting ID.** `ON_LINADV_S`

Online learning and bandits

The learner chooses an action in the unit ball and incurs and observes its exact inner product with the current bounded loss vector. The vectors are fixed in advance, and each round supplies one scalar; there is no additional independent additive noise.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Adversarial linear bandit; solution concept: Minimize expected cumulative regret; task family: Online bandit

**MODEL tags.** stochastic model: Bounded loss vector; structure: Linear; structure: Linear loss

**ORACLE tags.** derivative order: Order 0; feedback quality: Exact scalar projection; interface family: One point value; operation: Observe scalar linear loss; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds

## 1. Setting specification

### Task

The learner chooses an action in the unit ball and incurs and observes its exact inner product with the current bounded loss vector. The vectors are fixed in advance, and each round supplies one scalar; there is no additional independent additive noise.

### Admissible model

The hidden linear loss vectors obey $\|\ell_t\|_2\le1$ in every round.

The sole loss-incurring point is $x_t$. Feedback is one projection value, not the complete loss vector.

The comparator is the best fixed point $u$ in the ball after observing the sequence, with minimum cumulative loss $-\|\sum_t\ell_t\|_2$.

Require $d,T\ge1$; the action domain is the Euclidean unit ball.

The adversary cannot replace per-round norm constraints with unbounded Gaussian losses.

### Oracle interface

Exact linear-loss projection:

$$
t,\ x_t\in B_2^d(1)\ \longmapsto\ Y_t=\langle x_t,\ell_t\rangle
$$

The current loss vector $\ell_t$ is fixed before $x_t$ is selected.

One exact scalar is returned per round, with no independent observation noise.

No second direction may be queried for the same $\ell_t$.

Public inputs are d, T, the action domain B₂ᵈ(1), and the unit norm bound on each loss vector.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_T=\sum_t\langle x_t,\ell_t\rangle-\min_{u\in B_2^d(1)}\sum_t\langle u,\ell_t\rangle,\qquad \|x_t\|_2,\|\ell_t\|_2\le1
$$

### Resource accounting

One exact scalar per round, for $T$ bandit observations in total.

Any causal randomized algorithm is allowed. The available OSMD upper bound uses internal random exploration and regularized updates.

Internal linear algebra and domain optimization are separate from the native scalar-feedback count. Computational efficiency is not claimed for the entire admissible class.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}}\sup_{\ell_{1:T}\in(B_2^d(1))^T}\mathbb{E}_{\mathcal{A}}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\ell_t$: Linear loss vectors fixed in advance **Domain:** $\ell_t\in B_2^d(1)$.

$x_t,u$: The action and fixed comparator. **Domain:** $x_t,u\in B_2^d(1)$.

$Y_t$: Exact scalar linear loss **Domain:** $Y_t\in[-1,1]$.

The response is $Y_t=\langle x_t,\ell_t\rangle$, with no additional independent noise.

$\eta,\gamma$: The step size and exploration parameter in the OSMD branch. **Domain:** Public algorithm tuning.

Require $\eta=\sqrt{\log T/(2dT)}$ and $\gamma=T^{-1/2}$. This window ensures $\eta d\le1/2$.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_t\langle x_t,\ell_t\rangle-\min_{u\in B_2^d(1)}\sum_t\langle u,\ell_t\rangle$.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\ell_{1:T}\in(B_2^d(1))^T}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T\langle x_t,\ell_t\rangle-\min_{u\in B_2^d(1)}\sum_{t=1}^T\langle u,\ell_t\rangle.\end{aligned}
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

## 3. Complexity bracket

### Compared quantities

#### Q1 - cumulative regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\ell_{1:T}\in(B_2^d(1))^T}\mathbb E_{\mathcal A}[R_T],\\ R_T&=\sum_{t=1}^T\langle x_t,\ell_t\rangle-\min_{u\in B_2^d(1)}\sum_{t=1}^T\langle u,\ell_t\rangle.\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - MAIN

**Region.**

$$
T\ge d^3; T\ge 4d; lnT\le d; T\ge 2d lnT
$$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
c \sqrt{dT}
$$

**Upper bound.** B1

$$
3\sqrt{dTlnT}
$$

**Gap or comparison.** O(sqrt lnT)

**Comparison argument.** Only individually audited compatible claims enter. Outside this window retain the full lower formula; no unconditional Ω(sqrt(dT)) declaration from this source.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Retain all four window conditions: $T\ge d^3$, $T\ge4d$, $\log T\le d$, and $T\ge2d\log T$. Actions lie in the unit Euclidean ball, and loss vectors have a pointwise dual-norm bound.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - OSMD on Euclidean ball with barrier and randomized action

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le3\sqrt{dT\log T}
$$

**Sources.** [1](https://proceedings.mlr.press/v23/bubeck12a/bubeck12a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [1](https://proceedings.mlr.press/v23/bubeck12a/bubeck12a.pdf) theorem: Theorem 6; pdf pages: 11; printed pages: 41.11

For actions in the Euclidean unit ball and pointwise dual-norm-bounded losses, the source upper bound is $3\sqrt{dT\log T}$. Set $\eta=\sqrt{\log T/(2dT)}$ and $\gamma=T^{-1/2}$ and retain $\eta d\le1/2$.

### B2 - Truncated parameter-noise construction, Theorem5.2(2)

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge c\min\{\sqrt{dT},T/d\}\sqrt{\frac{d}{\max\{d,\log T\}}}
$$

**Sources.** [2](https://arxiv.org/pdf/2603.28201v3)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [2](https://arxiv.org/pdf/2603.28201v3) theorem: Theorem 5.2, part 2; Appendix F; pdf pages: 8; 38; 39; 40

Use the complete bounded-loss lower bound $c\min\{\sqrt{dT},T/d\}\sqrt{d/(d\vee\log T)}$, requiring $T\ge4d$. The abbreviated order in the abstract is valid only within its corresponding parameter window.

## References

[1] Sébastien Bubeck; Nicolò Cesa-Bianchi; Sham M. Kakade. Towards Minimax Policies for Online Linear Optimization with Bandit Feedback. 2012. COLT / PMLR 23:41.1–41.14.

https://proceedings.mlr.press/v23/bubeck12a/bubeck12a.pdf

[2] Andrew Jacobsen; Dorian Baudry; Shinji Ito; Nicolò Cesa-Bianchi. A Perturbation Approach to Unconstrained Linear Bandits. 2026. 2603.28201v3.

https://arxiv.org/pdf/2603.28201v3
