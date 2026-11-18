# Lipschitz geodesically convex minimization in hyperbolic space: one full subgradient

**Setting ID.** `SO_FO_G01_SG`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Geodesically convex; convexity: Convexity not assumed; geometry: Hyperbolic geometry; smoothness: Global lipschitz; smoothness: Lipschitz function

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Riemannian subgradient; operation: Subgradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in\mathbb{H}_K^d}f(x)$$

### Admissible model

The public hyperbolic space $\mathbb H_K^d$ has constant sectional curvature $-K$, where $K\ge0$ and $K=0$ denotes the Euclidean limit. The function $f$ is geodesically convex and $L$-Lipschitz throughout the space, and it has a global minimizer with $\operatorname{dist}(x^\star,x_0)\le R$. The localization ball does not restrict queries or outputs. The dimension satisfies $d\ge2$.

Admissible parameter domain:

$$K\ge0,\quad L>0,\quad R>0,\quad d\in\mathbb{N}_{\ge1},\quad \varepsilon>0,\quad d\ge2$$

### Oracle interface

Public numerical inputs: $d,\ K,\ \varepsilon,\ x_0$.

Public upper bounds: $L,\ R$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{H}_K^d$; feedback consists of one full subgradient:

$$g\in\partial f(x)\subset T_x\mathbb{H}_K^d;\ f(y)\ge f(x)+\langle g,\log_x y\rangle_x$$

The function and its admissible subgradient selector are fixed before execution; every response comes from that same instance.

The exponential map of the public manifold is computable.

The logarithmic map of the public manifold is computable.

Geodesic projection onto the public localization ball is computable.

### Output

Return a point $\widehat x\in\mathbb H_K^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(f,x)=f(x)-f^\star$$

$f^\star=\inf_{x\in \mathbb{H}_K^d}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One declared full first-order response costs one call; its vector coordinates are not charged separately.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Deterministic / Pointwise guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\exists A\ \forall I,\mathcal{O}:\ \ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\exists A\ \forall I,\mathcal{O}:\ \mathbb{E}_A[\ell(I,\widehat{x})]\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{H}_K^d$.

$f$: Unknown objective, with domain and structure specified by the model

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{H}_K^d}f(x)$$

$x^\star$: A global minimizer whose existence is promised by the model; unique under strong convexity

$\mathbb{H}_K^d$: $d$-dimensional hyperbolic space of sectional curvature $-K$; $K=0$ is the Euclidean limit **Domain:** $K\ge0,\ d\ge2$.

$T_x\mathbb{H}_K^d$: Tangent space at $x$

$\langle\cdot,\cdot\rangle_x$: Riemannian metric inner product at $x$

$\log_x y$: Riemannian logarithm mapping $y$ to the tangent space at $x$

$\operatorname{dist}$: Geodesic distance in hyperbolic space

$\partial f(x)$: Ambient subdifferential of the corresponding convex function

$$\partial f(x)=\{g:f(u)\ge f(x)+\langle g,u-x\rangle\ \forall u\in\operatorname{dom}f\}$$

$g$: One subgradient vector selected and returned by the oracle, rather than the entire subdifferential

$d$: Dimension; a public positive integer whose dependence is tracked jointly **Domain:** $d\in\mathbb{N}_{\ge2}$.

$K$: Magnitude of the negative sectional curvature; $K=0$ is the Euclidean limit **Domain:** $K\ge0$.

$L$: Public upper bound on the function Lipschitz constant **Domain:** $L>0$.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $0<c<1$.

$C$: Sufficiently large universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $C>1$.

$\zeta$: Curvature-localization factor, with continuous limit $1$ at $K=0$; its dependence cannot be absorbed into a constant

$$\zeta=\sqrt K R/\tanh(\sqrt K R),\quad\zeta(0)=1$$

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Sufficiently high dimension for deterministic algorithms

**Region.** $K>0,\quad d\ge C\zeta(LR/\varepsilon)^2,\quad\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** B2

$$
c\zeta(LR/\varepsilon)^2
$$

**Upper bound.** B1

$$
C\zeta(LR/\varepsilon)^2
$$

**Gap or comparison.** $C$

### R2 - Nontrivial accuracy

**Region.** $d\ge2,\quad0<\varepsilon\le cLR,\quad K\ge0$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
C\zeta(LR/\varepsilon)^2
$$

### R3 - Zero queries

**Region.** $\varepsilon\ge LR,\quad d\ge2,\quad K\ge0$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B3, B5

$$
0
$$

### R4 - Nontrivial accuracy

**Region.** $d\ge2,\quad0<\varepsilon\le cLR,\quad K\ge0$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B4

$$
C\zeta(LR/\varepsilon)^2
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Geodesic projected subgradient method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\zeta(LR/\varepsilon)^2
$$

**Sources.** [1](https://proceedings.mlr.press/v49/zhang16b.pdf)

**Conditions.** $$d\ge2,\quad0<\varepsilon\le cLR,\quad K\ge0$$

**Dimension conditions.** $d\ge2,\quad0<\varepsilon\le cLR,\quad K\ge0$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://proceedings.mlr.press/v49/zhang16b.pdf) theorem: Theorem 9, PDF p. 9; substitute diameter $2R$ and use $\zeta(2\sqrt K R)\le2\zeta(\sqrt K R)$

### B2 - Deterministic hard instances in hyperbolic geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\zeta(LR/\varepsilon)^2
$$

**Sources.** [2](https://arxiv.org/pdf/2610.12184v3) [3](https://arxiv.org/pdf/2610.26815v1)

**Conditions.** $$K>0,\quad d\ge C\zeta(LR/\varepsilon)^2,\quad\varepsilon\le cLR$$

**Dimension conditions.** $K>0,\quad d\ge C\zeta(LR/\varepsilon)^2,\quad\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2610.12184v3) theorem: §3.1, Theorem3.1, §7.1; PDFpp.5–6,15–19; d=T+2

**Source location.** [3](https://arxiv.org/pdf/2610.26815v1) theorem: Theorem 1.1, PDF p. 4; Section 5 removes the geodesic-span restriction

### B3 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [4](https://arxiv.org/pdf/2605.17540v4) [5](https://arxiv.org/pdf/1405.4980)

**Conditions.** $$\varepsilon\ge LR,\quad d\ge2,\quad K\ge0$$

**Dimension conditions.** $\varepsilon\ge LR,\quad d\ge2,\quad K\ge0$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B4 - Geodesic projected subgradient method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\zeta(LR/\varepsilon)^2
$$

**Sources.** [1](https://proceedings.mlr.press/v49/zhang16b.pdf)

**Conditions.** $$d\ge2,\quad0<\varepsilon\le cLR,\quad K\ge0$$

**Dimension conditions.** $d\ge2,\quad0<\varepsilon\le cLR,\quad K\ge0$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://proceedings.mlr.press/v49/zhang16b.pdf) theorem: Theorem 9, PDF p. 9; substitute diameter $2R$ and use $\zeta(2\sqrt K R)\le2\zeta(\sqrt K R)$

### B5 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [4](https://arxiv.org/pdf/2605.17540v4) [5](https://arxiv.org/pdf/1405.4980)

**Conditions.** $$\varepsilon\ge LR,\quad d\ge2,\quad K\ge0$$

**Dimension conditions.** $\varepsilon\ge LR,\quad d\ge2,\quad K\ge0$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

## 5. Local arguments

### A1 - Klein-coordinate centroid reduction

**Scope.** Hyperbolic geodesic convexity and value-subgradient access; public Klein geometry.

**Algorithm scope.** Deterministic upper witness.

Returning $x_0$ has gap at most $LR$. For value-subgradient access, the cited Klein-coordinate construction transforms subgradient inequalities into Euclidean cuts preserving the lower level set. Its geometric lemmas give an inscribed ball of radius
$r=\epsilon\sqrt K/[8L\cosh^2(\sqrt KR)]$
inside an initial ball of radius $\tanh(\sqrt KR)$. Replacing the ellipsoid center by an exact centroid makes every unsuccessful cut shrink volume by a constant fraction.

The log volume ratio is
$$
d\log\!\left({8L\sinh(\sqrt KR)\cosh(\sqrt KR)\over\epsilon\sqrt K}\right)
=O(d[\sqrt KR+\log(eLR/\epsilon)]).
$$
Use the continuous limit at $K=0$. Function values choose the best queried point. This proves the deterministic value-subgradient information bound, also valid in the randomized view. It does not give a subgradient-only algorithm or a polynomial arithmetic-time guarantee.

**Limits of the argument.** Imported Klein geometric lemmas are required; this is not a subgradient-only or arithmetic-time result.

**Sources.** [4](https://arxiv.org/pdf/2605.17540v4) [5](https://arxiv.org/pdf/1405.4980)

## References

[1] Hongyi Zhang and Suvrit Sra. First-order Methods for Geodesically Convex Optimization. 2016.

https://proceedings.mlr.press/v49/zhang16b.pdf

[2] Wendao Wu; Haihan Zhang; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Geodesically Convex Optimization in Hyperbolic Space: Matching Lower Bounds. 2026-10-21; arXiv v3 preprint.

https://arxiv.org/pdf/2610.12184v3

[3] Christopher Criscitiello. Tight lower bounds for Lipschitz geodesically convex optimization on hyperbolic space. 2026-10-19; arXiv v1 preprint.

https://arxiv.org/pdf/2610.26815v1

[4] Yutong Zhang; Yaoran Yang; Yifan Zhu; Wentao Zhang. One-Shot Klein Cutting Planes for Lipschitz Geodesically Convex Optimization in Hyperbolic Space. 2026-05-28; arXiv v4 preprint.

https://arxiv.org/pdf/2605.17540v4

[5] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015.

https://arxiv.org/pdf/1405.4980
