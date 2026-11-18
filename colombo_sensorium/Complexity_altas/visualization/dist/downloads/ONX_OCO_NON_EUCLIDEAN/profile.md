# Online convex optimization in general norms: full subgradients and Bregman geometry.

**Setting ID.** `ONX_OCO_NON_EUCLIDEAN`

Online learning and bandits

Losses are convex, with full subgradients bounded in the specified dual norm, and actions lie in a public convex set. A public strongly convex regularizer supplies the Bregman geometry and initial radius. The target is static regret; geometric operations and loss feedback are charged separately.

**Status.** Bounds missing

**TASK tags.** formulation: Onx oco non euclidean; task family: Online bandit

**MODEL tags.** convexity: Convex

**ORACLE tags.** interface family: Complete subgradient; operation: Complete subgradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

Losses are convex, with full subgradients bounded in the specified dual norm, and actions lie in a public convex set. A public strongly convex regularizer supplies the Bregman geometry and initial radius. The target is static regret; geometric operations and loss feedback are charged separately.

### Admissible model

The compact convex set $X\subset\mathbb{R}^d$, norm $\|\cdot\|$, and dual norm $\|\cdot\|_*$ are public. Losses $f_t$ are convex; returned valid subgradients satisfy $g_t\in\partial f_t(x_t)$ and $\|g_t\|_*\le G_*$.

The supplied regularizer $\psi$ is differentiable on a neighborhood of $X$ and $1$-strongly convex in the specified norm. The initial point $x_{\mathrm{init}}\in X$ is public, and require:

$$
D_\psi(u,v)=\psi(u)-\psi(v)-\langle\nabla\psi(v),u-v\rangle,\qquad \sup_{u\in X}D_\psi(u,x_{\mathrm{init}})\le R_\psi^2.
$$

The environment may precommit to losses or choose history-dependent losses consistent with the current subgradient feedback. It cannot anticipate current private randomness.

### Oracle interface

The learner is a causal policy acting in the domain. After each action, it receives a valid subgradient $g_t$.

A Bregman-projection or proximal-subproblem interface relative to $\psi$ is explicitly supplied.

Public inputs are $X,\|\cdot\|,\|\cdot\|_*,\psi,R_\psi,G_*,T,x_{\mathrm{init}}$.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_T=\sum_{t=1}^{T}f_t(x_t)-\min_{u\in X}\sum_{t=1}^{T}f_t(u).
$$

### Resource accounting

$$
N=T\quad\text{\text{subgradient observations}},\qquad T\quad\text{\text{proximal operations}}.
$$

The cost of a proximal operation depends on the supplied set and regularizer.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

Control worst-case static regret in the stated geometry and admissible loss class. Changing the norm changes both $G_*$ and $R_\psi$, so one cannot merely rename the norm while preserving their numerical values.

## 2. Notation and parameters

$G_*$: Dual-norm bound on valid subgradients **Domain:** $G_*\ge0$.

The feedback satisfies $g_t\in\partial f_t(x_t)$ and $\|g_t\|_*\le G_*$.

$R_\psi$: Bregman-radius parameter relative to the public initial point **Domain:** $R_\psi\ge0$.

$\sup_{u\in X}D_\psi(u,x_{\mathrm{init}})\le R_\psi^2$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$X,x_t,u$: Public compact convex action set, current action, and fixed comparator point **Domain:** $x_t,u\in X\subset\mathbb R^d$.

$\|\cdot\|,\|\cdot\|_*$: Public primal norm and its dual norm **Domain:** Norm on $\mathbb R^d$.

$\|g\|_* =\sup_{\|x\|\le1}\langle g,x\rangle$.

$\psi,D_\psi$: Differentiable strongly convex regularizer and its Bregman divergence. **Domain:** Real-valued function and nonnegative divergence.

$D_\psi(u,v)=\psi(u)-\psi(v)-\langle\nabla\psi(v),u-v\rangle$. The function ψ is 1-strongly convex in the original norm.

$x_{\mathrm{init}}$: Public initial point **Domain:** $x_{\mathrm{init}}\in X$.

$f_t,g_t$: Current convex loss and the returned admissible full subgradient **Domain:** $g_t\in\partial f_t(x_t)$.

The oracle may select any subgradient within the dual-norm bound, but returns only one complete vector.

$\eta$: Mirror-descent step size **Domain:** Algorithm tuning.

Use $\eta=\sqrt2R_\psi/(G_*\sqrt T)$ when $R_\psi G_*>0$. In zero-scale cases, a fixed action suffices.

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
R_T=\sum_{t=1}^{T}f_t(x_t)-\min_{u\in X}\sum_{t=1}^{T}f_t(u).
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** The Bregman geometry is public and full valid subgradients are returned. Matching lower bounds are not asserted for every fixed geometry.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
\sqrt2R_\psi G_*\sqrt T
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The function $\psi$ is 1-strongly convex in the stated norm and satisfies $\sup_uD_\psi(u,x_{\mathrm{init}})\le R_\psi^2$. Full subgradients satisfy $\|g_t\|_*\le G_*$.; An exact Bregman-proximal operation is publicly available; feedback is one complete valid subgradient.

**Oracle mapping.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee mapping.** The accompanying argument states the native guarantee and necessary conversion.

### B1 - Deterministic online mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\sqrt2 R_\psi G_*\sqrt T
$$

**Sources.** [1](https://jmlr.org/papers/volume18/16-632/16-632.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**subgradients.** T

**Bregman prox.** T

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** Choose step size $\eta=\sqrt2R_\psi/(G_*\sqrt T)$. The Bregman three-point inequality gives $\sum_t\langle g_t,x_t-u\rangle\le R_\psi^2/\eta+\eta G_*^2T/2$; convexity yields the regret bound. The proof holds pathwise, so random or adversarial selection of a valid full subgradient does not change it.

**Source location.** [1](https://jmlr.org/papers/volume18/16-632/16-632.pdf) theorem: The basic online mirror-descent inequality in Lemma 7.

Choose step size $\eta=\sqrt2R_\psi/(G_*\sqrt T)$. The Bregman three-point inequality gives $\sum_t\langle g_t,x_t-u\rangle\le R_\psi^2/\eta+\eta G_*^2T/2$; convexity yields the regret bound. The proof holds pathwise, so random or adversarial selection of a valid full subgradient does not change it.

## References

[1] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. 2017. JMLR 18(52):1–11.

https://jmlr.org/papers/volume18/16-632/16-632.pdf
