# Strongly convex online optimization with action-point gradients and static regret

**Setting ID.** `ONX_OCO_STRONG`

Online learning and bandits

Each round's loss is strongly convex with bounded gradient on a public compact convex set. After incurring the loss, the learner receives only its action-point gradient. The criterion is static regret. Only compatible regularity and geometry parameters defining a nonempty class are included.

**Status.** Fully optimal

**TASK tags.** formulation: Onx oco strong; task family: Online bandit

**MODEL tags.** convexity: Strongly convex

**ORACLE tags.** interface family: Action gradient; operation: Action gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

Each round's loss is strongly convex with bounded gradient on a public compact convex set. After incurring the loss, the learner receives only its action-point gradient. The criterion is static regret. Only compatible regularity and geometry parameters defining a nonempty class are included.

### Admissible model

The public set $X\subset\mathbb{R}^d$ is nonempty, compact, and convex, with Euclidean diameter at most $D$. The environment fixes a differentiable loss sequence before interaction. Each loss is $\mu$-strongly convex on $X$ and satisfies:

$$
\|\nabla f_t(x)\|_2\le G,\qquad f_t(y)\ge f_t(x)+\langle\nabla f_t(x),y-x\rangle+\frac{\mu}{2}\|y-x\|_2^2\quad(x,y\in X).
$$

Public geometry and regularity parameters must make the loss class nonempty. No minimax conclusion is asserted when strong convexity and gradient bounds are incompatible.

### Oracle interface

The algorithm is causal: choose $x_t\in X$ each round, then receive the sole exact gradient $\nabla f_t(x_t)$ at that point. Feedback is noiseless.

Public inputs are $X,T,D,G,\mu$. Projection computation and gradient queries are accounted for separately.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

Use the cumulative quantity in the task formula, without dividing by online rounds.

### Resource accounting

$$
N=T\quad\text{\text{exact gradient queries}}.
$$

Projection counts and the cost of each projection are recorded separately.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

$$R_T=\sum_{t=1}^{T}f_t(x_t)-\min_{u\in X}\sum_{t=1}^{T}f_t(u),\qquad \inf_{\mathcal A}\sup_{f_{1:T}\ \text{admissible}}\mathbb E_{\mathcal A}[R_T].$$

The comparator remains fixed throughout. The environment supremum ranges only over fixed loss sequences satisfying the model; expectation covers only the learner's randomness.

## 2. Notation and parameters

$D$: A Euclidean-diameter bound on the action set. **Domain:** $D\ge0$.

The condition is $\sup_{x,y\in X}\|x-y\|_2\le D$; replace X by W when W denotes the action set.

$G$: Uniform Euclidean bound on the full loss gradient in each round **Domain:** $G>0$.

The condition $\|\nabla f_t(x)\|_2\le G$ holds for all t and x specified by the model.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\mu$: The Euclidean strong-convexity modulus of losses. **Domain:** $\mu>0$.

$f_t(y)\ge f_t(x)+\langle\nabla f_t(x),y-x\rangle+\mu\|y-x\|_2^2/2$.

$X,x_t,u$: Public action domain, actual action, and fixed comparator point **Domain:** $x_t,u\in X\subset\mathbb R^d$.

The admitted matching lower bound applies only to the stated one-dimensional interval slice.

$f_t,g_t$: Strongly convex loss and its full gradient at the action point **Domain:** $g_t=\nabla f_t(x_t)\in\mathbb R^d$.

This gradient is queried once after each round's action.

$\eta_t$: Step size of strongly convex projected gradient descent **Domain:** Positive real number.

$\eta_t=1/(\mu t)$.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_tf_t(x_t)-\min_{u\in X}\sum_tf_t(u)$.

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
R_T=\sum_{t=1}^{T}f_t(x_t)-\min_{u\in X}\sum_{t=1}^{T}f_t(u),\qquad \inf_{\mathcal A}\sup_{f_{1:T}\ \text{admissible}}\mathbb E_{\mathcal A}[R_T].
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

The comparator is fixed throughout the horizon. The environment supremum ranges over admissible fixed loss sequences; expectation covers only learner randomness.

### R1 - SUPPORTED

**Region.** Assume $T\ge 2$, one-dimensional interval $X=[0,G/\mu]$, and $D\ge G/\mu$; the lower bound concerns this domain slice.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega((G^2/\mu)\log T)
$$

**Upper bound.** B1

$$
O((G^2/\mu)\log T)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee mapping.** The accompanying argument states the native guarantee and necessary conversion.

### B1 - Deterministic projected gradient descent with step_t = 1/(mu t).

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\frac{G^2}{2\mu}(1+\log T)
$$

**Sources.** [1](https://jmlr.org/papers/v15/hazan14a.html)

**Conditions.** Require $\mu,G>0$ and a public compact convex domain $X$. Each round returns the full gradient at the action. Strong convexity and the gradient-norm bound must be compatible.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**gradients.** T

**euclidean projections.** T

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** For any fixed comparator $u$, strong convexity gives $f_t(x_t)-f_t(u)\le\langle g_t,x_t-u\rangle-\mu\|x_t-u\|_2^2/2$. Combine the one-step projected squared-distance inequality with step size $\eta_t=1/(\mu t)$ and sum. Distance terms telescope, leaving $(G^2/(2\mu))\sum_{t=1}^T1/t$.

**Source location.** [1](https://jmlr.org/papers/v15/hazan14a.html) theorem: Standard strongly convex OGD inequality; the cited paper's introduction and Theorem 2 discuss the corresponding online lower bound

For any fixed comparator $u$, strong convexity gives $f_t(x_t)-f_t(u)\le\langle g_t,x_t-u\rangle-\mu\|x_t-u\|_2^2/2$. Combine the one-step projected squared-distance inequality with step size $\eta_t=1/(\mu t)$ and sum. Distance terms telescope, leaving $(G^2/(2\mu))\sum_{t=1}^T1/t$.

### B2 - Stochastic quadratic-loss or mean-estimation hard instances.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{G^2}{\mu}\log T\right)
$$

**Sources.** [1](https://jmlr.org/papers/v15/hazan14a.html)

**Conditions.** Assume $T\ge2$ and use the interval $X=[0,G/\mu]$ with $D\ge G/\mu$, or an instance class into which this interval embeds.; A worst-case lower bound over the allowed domain class, not a claim for every fixed compact convex set.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** Scale the one-dimensional hard construction in source Theorem 2 by $x=(G/\mu)z$ and multiply losses by $G^2/\mu$. A lower bound with full-function feedback also applies to the weaker single-gradient interface. The geometries admitting this embedding are stated explicitly in the applicability conditions.

**Source location.** [1](https://jmlr.org/papers/v15/hazan14a.html) theorem: Theorem 2, using a proportionally scaled one-dimensional subclass.

Scale the one-dimensional hard construction in source Theorem 2 by $x=(G/\mu)z$ and multiply losses by $G^2/\mu$. A lower bound with full-function feedback also applies to the weaker single-gradient interface. The geometries admitting this embedding are stated explicitly in the applicability conditions.

## References

[1] Elad Hazan; Satyen Kale. Beyond the Regret Minimization Barrier: Optimal Algorithms for Stochastic Strongly-Convex Optimization. 2014. JMLR15:2489–2512.

https://jmlr.org/papers/v15/hazan14a.html
