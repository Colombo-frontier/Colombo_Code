# Exp-concave online optimization with one-gradient feedback and Euclidean projection

**Setting ID.** `ONX_OCO_EXP`

Online learning and bandits

Each round's loss is exp-concave with bounded gradient. After acting in the feasible domain, the learner receives one exact gradient. Public Euclidean projection supports LightONS. Regret, projection costs, and matrix-computation costs are recorded separately.

**Status.** Bounds missing

**TASK tags.** formulation: Onx oco exp; task family: Online bandit

**MODEL tags.** convexity: Exp concavity

**ORACLE tags.** interface family: Action gradient; operation: Action gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

Each round's loss is exp-concave with bounded gradient. After acting in the feasible domain, the learner receives one exact gradient. Public Euclidean projection supports LightONS. Regret, projection costs, and matrix-computation costs are recorded separately.

### Admissible model

The action set $X\subset\mathbb{R}^d$ is compact and convex and lies in a Euclidean ball of radius $D/2$. Differentiable losses satisfy:

$$
e^{-\alpha f_t(\cdot)}\ \text{\text{on} }X\text{ \text{is concave}},\qquad \|\nabla f_t(x)\|_2\le G\quad(x\in X).
$$

The environment may depend on past history but cannot anticipate current private randomness. The guarantee holds for every admissible realized loss sequence.

Precisely, exponential concavity requires that in each round $t$, the map $x\mapsto\exp(-\alpha f_t(x))$ be concave on the stated feasible domain. This property concerns the complete action variable; the norm and gradient bound are specified by this axis.

### Oracle interface

In each round, first choose $x_t\in X$, then receive one exact gradient at that point.

The quantity $X,T,D,G,\alpha$ is public, and Euclidean projection onto $X$ is available at arithmetic cost $\mathsf{EP}_X$ per projection. Causal learners respecting this timing are allowed.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\operatorname{Reg}_T(u)=\sum_{t=1}^{T}\bigl(f_t(x_t)-f_t(u)\bigr),\qquad u\in X.
$$

### Resource accounting

$$N=T,\qquad \text{LightONS total arithmetic cost}=O\!\left((\mathsf{EP}_X+d^2)T+d^{\omega}\sqrt T\log T\right).$$

The quantity $\omega$ is the exponent of the chosen matrix-multiplication algorithm. Cost follows the source's numerical-primitive model and does not establish general bit-complexity optimality.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

The upper bound holds pathwise, simultaneously for every fixed comparator and every admissible loss sequence.

## 2. Notation and parameters

$D$: Diameter of a public Euclidean ball containing the action set **Domain:** $D>0$.

A public ball center exists such that $X\subseteq B_2^d(D/2)$ after translation. This specifies more than a diameter bound alone.

$G$: Uniform Euclidean bound on the full loss gradient in each round **Domain:** $G>0$.

The condition $\|\nabla f_t(x)\|_2\le G$ holds for all t and x specified by the model.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$\alpha$: Exponential-concavity coefficient of the loss **Domain:** $\alpha>0$.

The function $x\mapsto\exp(-\alpha f_t(x))$ is concave on the action set. This parameter is not an algorithmic step size.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$X,x_t,u$: The public action domain, actual action, and fixed comparator. **Domain:** $x_t,u\in X\subset\mathbb R^d$.

$f_t$: Current differentiable exponentially concave loss **Domain:** Real-valued function on $X$.

The function $\exp(-\alpha f_t)$ is concave on $X$.

$\gamma_0$: Curvature step-size scale in the LightONS upper bound. **Domain:** Positive real number.

$\gamma_0=\frac12\min\{1/(DG),\alpha\}$.

$h_{\mathrm{reg}}$: Regularization scale in LightONS **Domain:** Positive real number.

$h_{\mathrm{reg}}=1+d\log T$.

$\operatorname{Reg}_T(u)$: Static regret against fixed u. **Domain:** Real number.

$\operatorname{Reg}_T(u)=\sum_t[f_t(x_t)-f_t(u)]$.

$\mathsf{EP}_X,\omega$: Arithmetic cost of one exact Euclidean projection and the matrix-multiplication exponent. **Domain:** Computational work and complexity exponent.

The projection is $\arg\min_{x\in X}\|x-y\|_2^2$. The quantity $\omega$ describes arithmetic work for order-d matrix multiplication.

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
\operatorname{Reg}_T(u)=\sum_{t=1}^{T}\bigl(f_t(x_t)-f_t(u)\bigr),\qquad u\in X.
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Assume $\alpha,D,G>0$, a nonempty instance class, and exact Euclidean projection.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
\begin{gathered}\frac d{2\gamma_0}\log\!\left(1+\frac{G^2T}{dh_{\mathrm{reg}}}\right)+\frac{\gamma_0h_{\mathrm{reg}}D^2}{8},\\ \gamma_0=\frac12\min\!\left\{\frac1{DG},\alpha\right\},\qquad h_{\mathrm{reg}}=1+d\log T.\end{gathered}
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The quantity $\gamma_0$ is the exponential-concavity surrogate coefficient, and $h_{\mathrm{reg}}$ is the regularization parameter. Accuracy-like notation in the source has been renamed; neither is an error tolerance or privacy parameter.; The shorthand $O(d\log T)$ assumes fixed $D,G,\alpha$. Source equation (11b) gives running time; this interface does not automatically supply a free Mahalanobis projection each round.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - LightONS with one gradient and one Euclidean projection

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\begin{gathered}\frac d{2\gamma_0}\log\!\left(1+\frac{G^2T}{dh_{\mathrm{reg}}}\right)+\frac{\gamma_0h_{\mathrm{reg}}D^2}{8},\\ \gamma_0=\frac12\min\!\left\{\frac1{DG},\alpha\right\},\qquad h_{\mathrm{reg}}=1+d\log T.\end{gathered}
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v336/main/assets/wang26b/wang26b.pdf)

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v336/main/assets/wang26b/wang26b.pdf) Corollary 1 p.9 Eq.(11a)

## References

[1] Yi-Han Wang; Peng Zhao; Zhi-Hua Zhou. A Simple, Optimal and Efficient Algorithm for Online Exp-Concave Optimization. 2026. COLT 2026, PMLR 336.

https://raw.githubusercontent.com/mlresearch/v336/main/assets/wang26b/wang26b.pdf
