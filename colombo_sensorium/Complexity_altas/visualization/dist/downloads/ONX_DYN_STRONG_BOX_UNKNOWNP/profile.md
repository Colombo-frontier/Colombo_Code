# Strongly convex dynamic online optimization on a box with unknown ℓ₁ path length.

**Setting ID.** `ONX_DYN_STRONG_BOX_UNKNOWNP`

Online learning and bandits

One learner must adapt to all comparator paths without knowing path length in advance. Losses are strongly convex, the domain is a box, and path length uses the one-norm. Each round reveals only the gradient at the chosen action.

**Status.** Bounds missing

**TASK tags.** formulation: Onx dyn strong box unknownp; task family: Online bandit

**MODEL tags.** convexity: Strongly convex; stochastic model: Comparator path

**ORACLE tags.** interface family: Action gradient; operation: Action gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; public information: Unknown path

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

One learner must adapt to all comparator paths without knowing path length in advance. Losses are strongly convex, the domain is a box, and path length uses the one-norm. Each round reveals only the gradient at the chosen action.

### Admissible model

$$
X=[-B,B]^d,\qquad P_T^{(1)}(u)=\sum_{t=2}^{T}\|u_t-u_{t-1}\|_1.
$$

Every loss is $\mu$-strongly convex in the Euclidean norm and satisfies the coordinate-gradient bound $\|\nabla f_t(x)\|_\infty\le G_\infty$. Any admissible loss sequence is allowed; the current loss is revealed after the action.

### Oracle interface

The source protocol supplies the complete current loss. A coordinate-surrogate implementation may use only the gradient at the final main action.

The algorithm is a causal learner acting within the domain and internally uses FLH–OGD with coordinatewise projections.

The quantity $T,d,B,\mu,G_\infty$ is public; $P_T^{(1)}$ is not supplied.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\operatorname{Reg}_T(u)=\sum_{t=1}^{T}\bigl(f_t(x_t)-f_t(u_t)\bigr),\qquad u_{1:T}\in X^T.
$$

### Resource accounting

The coordinate-surrogate implementation needs only $N=T$ action-point gradients. Internal expert states and histories are accounted for separately. Converting an $\ell_1$ path length to Euclidean path length can introduce dimension factors.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

The source upper bound holds pathwise and simultaneously for all comparator trajectories.

## 2. Notation and parameters

$B$: Half side length of the box action domain **Domain:** $B>0$.

$X=[-B,B]^d$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\mu$: The Euclidean strong-convexity modulus of losses. **Domain:** $\mu>0$.

$f_t(y)\ge f_t(x)+\langle\nabla f_t(x),y-x\rangle+\mu\|y-x\|_2^2/2$.

$G_\infty$: A uniform bound on absolute gradient coordinates. **Domain:** $G_\infty>0$.

The gradient bound is $\|\nabla f_t(x)\|_\infty\le G_\infty$. Strong convexity still uses Euclidean norm.

$X,x_t,u_t$: The public box action domain, actual action, and comparator location. **Domain:** $X=[-B,B]^d,\ x_t,u_t\in X$.

$P_T^{(1)}(u)$: Actual comparator path length in the one-norm **Domain:** $0\le P_T^{(1)}\le2Bd(T-1)$.

The quantity $P_T^{(1)}(u)=\sum_{t=2}^T\|u_t-u_{t-1}\|_1$ is not supplied to the algorithm.

$\operatorname{Reg}_T(u)$: Dynamic regret against the complete comparator path within the box. **Domain:** Real number.

Assume $\operatorname{Reg}_T(u)=\sum_t[f_t(x_t)-f_t(u_t)]$; upper-bound constants may depend on fixed B, mu, and G_infinity.

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
\operatorname{Reg}_T(u)=\sum_{t=1}^{T}\bigl(f_t(x_t)-f_t(u_t)\bigr),\qquad u_{1:T}\in X^T.
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Box constraints and an $\ell_1$ path budget; fixed $B,\mu,G_\infty$; proper algorithms.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
\widetilde{O}\!\left(\max\!\left\{d^{1/3}T^{1/3}\bigl(P_T^{(1)}\bigr)^{2/3},d\right\}\right)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $P_T^{(1)}=\sum_{t=2}^T\|u_t-u_{t-1}\|_1$. The displayed dimension rate fixes $B,\mu,G_\infty$. The shorthand suppresses $\log T$ and dependence on these fixed parameters.; Comparison with Euclidean path and gradient normalization may introduce dimension factors through norm conversion.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - Strongly convex FLH or constrained dynamic online learner

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\widetilde{O}\!\left(\max\!\left\{d^{1/3}T^{1/3}\bigl(P_T^{(1)}\bigr)^{2/3},d\right\}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v151/baby22a/baby22a.pdf)

**Source location.** [1](https://proceedings.mlr.press/v151/baby22a/baby22a.pdf) Corollary 5, PDF p.6

## References

[1] Dheeraj Baby; Yu-Xiang Wang. Optimal Dynamic Regret in Proper Online Learning with Strongly Convex Losses and Beyond. 2022. AISTATS 2022, PMLR 151.

https://proceedings.mlr.press/v151/baby22a/baby22a.pdf
