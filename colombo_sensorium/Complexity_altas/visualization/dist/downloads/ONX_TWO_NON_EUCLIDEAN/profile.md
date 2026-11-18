# Two-point convex bandits in a general norm with Euclidean-Lipschitz losses

**Setting ID.** `ONX_TWO_NON_EUCLIDEAN`

Online learning and bandits

Action centers lie in a convex set with public mirror geometry, and losses are globally Euclidean Lipschitz. Each round reveals exact values of the same function on opposite sides of the center; only the center incurs loss. Dual-norm moments of spherical directions control the gradient-estimator variance.

**Status.** Bounds missing

**TASK tags.** formulation: Onx two non euclidean; task family: Online bandit

**MODEL tags.** convexity: Convex

**ORACLE tags.** interface family: Two point exact; operation: Two point exact; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

Action centers lie in a convex set with public mirror geometry, and losses are globally Euclidean Lipschitz. Each round reveals exact values of the same function on opposite sides of the center; only the center incurs loss. Dual-norm moments of spherical directions control the gradient-estimator variance.

### Admissible model

The compact convex center-action set $W\subset\mathbb{R}^d$, norm $\|\cdot\|$, and its dual norm are public. A regularizer $\psi$ is supplied that is $1$-strongly convex in that norm and satisfies:

$$
0\le\psi(x)\le R_\psi^2\quad(x\in W),\qquad p_*\ge\left(\mathbb{E}_{u\sim\operatorname{Unif}(\mathbb{S}^{d-1})}\|u\|_*^4\right)^{1/4}.
$$

All losses are fixed before interaction and are globally convex and $G_2$-Lipschitz in Euclidean norm.

### Oracle interface

$$
f_t(x_t+\rho_tu_t),\qquad f_t(x_t-\rho_tu_t).
$$

The two evaluations in a round use the same current function without measurement noise. Feedback arrives after probe submission.

The center must satisfy $x_t\in W$. Probes may lie outside $W$ because losses are defined on the full space.

Only the center $x_t$ incurs loss. Probes supply information only.

Causal learners with centers inside the domain are allowed. The quantities $W,\psi,\|\cdot\|,G_2,R_\psi,p_*,T$ are public. One mirror or proximal update is permitted per round.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_T=\sum_{t=1}^T f_t(w_t)-\min_{w\in W}\sum_{t=1}^T f_t(w).
$$

Only the feasible center incurs loss. Losses at the two exact-value probes are not added.

### Resource accounting

Two simultaneous exact function evaluations per round, totaling $N=2T$. Mirror-proximal updates, direction sampling, and internal arithmetic are counted separately.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

Expectation includes the learner's internal randomness. Queries count exact function values; proximal operations are counted separately.

## 2. Notation and parameters

$G_2$: Global Euclidean Lipschitz bound for each round's loss **Domain:** $G_2\ge0$.

For all $x,y\in\mathbb R^d$, $|f_t(x)-f_t(y)|\le G_2\|x-y\|_2$.

$R_\psi$: Square-root scale of the regularizer's value range **Domain:** $R_\psi\ge0$.

The condition $0\le\psi(x)\le R_\psi^2$ holds for every $x\in W$. It is not an initial-point Bregman-divergence parameter.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$p_*$: Fourth-moment bound for the dual norm of a spherical direction **Domain:** $p_*>0$.

$p_*\ge(\mathbb E_{u\sim\operatorname{Unif}(\mathbb S^{d-1})}\|u\|_*^4)^{1/4}$.

$W,w_t,w$: The public center-action set, actual center, and fixed comparator. **Domain:** $w_t,w\in W\subset\mathbb R^d$.

Loss is charged at the center; both probes may lie anywhere in $\mathbb R^d$.

$\psi$: The public strongly convex regularizer. **Domain:** A finite real-valued function on W.

The function is 1-strongly convex in the stated primal norm and satisfies $0\le\psi(w)\le R_\psi^2$.

$\|\cdot\|,\|\cdot\|_*$: The public primal norm and its dual norm. **Domain:** Norm on $\mathbb R^d$.

The dual norm is $\|g\|_*=\sup_{\|x\|\le1}\langle g,x\rangle$. The loss Lipschitz condition still uses Euclidean norm.

$\mathbb S^{d-1},u_t$: Euclidean unit sphere and a uniformly random direction **Domain:** Sphere and a random element of that sphere.

$\mathbb S^{d-1}=\{u:\|u\|_2=1\}$.

$\rho_t,z_t^\pm$: Current probe radius and symmetric probe points **Domain:** $\rho_t>0,\ z_t^\pm\in\mathbb R^d$.

The probes are $z_t^\pm=w_t\pm\rho_tu_t$. Exact evaluations of the same $f_t$ are returned after both points are submitted.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_tf_t(w_t)-\min_{w\in W}\sum_tf_t(w)$.

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

The count $N=2T$ measures scalar value evaluations in the two-point protocol. Loss remains charged at the center.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
R_T=\sum_{t=1}^T f_t(w_t)-\min_{w\in W}\sum_{t=1}^T f_t(w).
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Two exact values from the same function; every sample is globally Euclidean-Lipschitz; only the center incurs loss.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
O(p_*G_2R_\psi\sqrt{dT})
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Choose step size $\eta_{\mathrm{step}}=R_\psi/(p_*G_2\sqrt{dT})$ and probe radius satisfying $0<\rho_t\le p_*R_\psi\sqrt{d/T}$.; The quantity $p_*$ bounds the fourth moment of the dual norm of a spherical direction; $G_2$ is the Euclidean Lipschitz constant, and $R_\psi$ comes from the regularizer-range bound $0\le\psi\le R_\psi^2$.; Both points are submitted simultaneously and return exact values of the same function. Only the center incurs loss. The symbol $\eta_{\mathrm{step}}$ denotes the update step size and is unrelated to the exponential-concavity coefficient.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - Spherical symmetric two-point gradient estimator with online mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(p_*G_2R_\psi\sqrt{dT}\right)
$$

**Sources.** [1](https://jmlr.org/papers/volume18/16-632/16-632.pdf)

**Source location.** [1](https://jmlr.org/papers/volume18/16-632/16-632.pdf) Theorem 1, PDF p.4

## References

[1] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. 2017. JMLR 18(52):1–11.

https://jmlr.org/papers/volume18/16-632/16-632.pdf
