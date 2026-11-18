# Goldstein stationarity for Lipschitz nonconvex functions: zero-respecting; function value and the entire subdifferential

**Setting ID.** `SO_FO_N04_FSD`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Bounds missing

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; initialization: Initial gap; smoothness: Lipschitz function

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Value subdifferential set; operation: Value subdifferential set; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Explicit restriction; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: Zero respecting

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

The unknown function $f:\mathbb R^d\to\mathbb R$ is globally $L$-Lipschitz and bounded below, with $f(x_0)-\inf f\le\Delta$. No convexity, weak convexity, or smoothness is assumed; the model uses the Clarke subdifferential. Fix $x_0=0$, and define support in the public standard coordinates.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad \Delta>0,\quad \tau\ge0,\quad \varepsilon>0,\quad L>0$$

### Oracle interface

Public numerical inputs: $d,\ \tau,\ \varepsilon,\ x_0$.

Public upper bounds: $L,\ \Delta$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of function value and the entire subdifferential:

$$(f(x),\partial_C f(x))$$

All responses are consistent with one fixed function instance. A set-valued response provides the entire specified subdifferential, which the algorithm may process measurably.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

The output must also satisfy the support, atomic-hull, or historical-span restriction of its algorithm view. An unqueried output remains subject to these restrictions.

### Loss or accuracy criterion

$$\operatorname{dist}(0,\partial_\tau f(x)),\quad\partial_\tau f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\tau}\partial_C f(y)$$

$\partial_C f$ is the Clarke subdifferential, and $\partial_\tau f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\tau}\partial_C f(y)$. Here $\operatorname{dist}(z,S)=\inf_{u\in S}\|z-u\|_2$ and $\tau$ is the neighborhood radius.

### Resource accounting

Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

Queries are zero-respecting: in the public standard coordinates, a coordinate must remain zero in every subsequent query until it has appeared with a nonzero value in an admissible feedback vector.

The nonzero support of the output must lie in the union of supports of all vectors in the observed subdifferential sets.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I,\forall\text{admissible oracle responses},\quad\mathbb{E}[\ell(I,\widehat{x})]\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f$: Unknown objective, with domain and structure specified by the model

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial_C f(x)$: Clarke subdifferential: the closed convex hull of limits of gradients at nearby differentiability points. Global Lipschitz continuity ensures that it is nonempty, compact, and convex.

$\partial_\tau f(x)$: Goldstein subdifferential with radius $\tau$

$$\partial_\tau f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\tau}\partial_C f(y)$$

$\operatorname{conv}$: Convex hull of a set

$\operatorname{dist}(z,S)$: Euclidean distance from a point to a set

$$\operatorname{dist}(z,S)=\inf_{u\in S}\|z-u\|_2$$

$d$: Dimension; a public positive integer **Domain:** $d\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the objective Lipschitz constant **Domain:** $L>0$.

$\Delta$: Public upper bound on the initial objective gap; the optimal value itself is unknown **Domain:** $\Delta>0$.

$\tau$: Goldstein neighborhood radius; it is not a failure probability **Domain:** $\tau\ge0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $0<c<1$.

$C$: Sufficiently large absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $C>1$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - No queries required at coarse accuracy

**Region.** $\varepsilon\ge L$

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B2

$$
0
$$

**Upper bound.** B1

$$
0
$$

### R2 - Exact-oracle zero-respecting lower-bound regime

**Region.** $\varepsilon\le c\min\{L,\tau L^2/\Delta,\Delta/\tau\},\quad d\ge C\Delta L^2/(\tau\varepsilon^3)$

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Upper bound missing

**Lower bound.** B3

$$
c\Delta L^2/(\tau\varepsilon^3)
$$

**Upper bound.** No admitted bound for this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $$\varepsilon\ge L$$

**Dimension conditions.** $\varepsilon\ge L$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B2 - Nonnegative resource budgets

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $$\varepsilon\ge L$$

**Dimension conditions.** $\varepsilon\ge L$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B3 - Randomized zero-respecting hard chain with access to the entire Clarke subdifferential

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** The stated restricted randomized class

$$
c\Delta L^2/(\tau\varepsilon^3)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.17780)

**Conditions.** $$\varepsilon\le c\min\{L,\tau L^2/\Delta,\Delta/\tau\},\quad d\ge C\Delta L^2/(\tau\varepsilon^3)$$

**Dimension conditions.** $\varepsilon\le c\min\{L,\tau L^2/\Delta,\Delta/\tau\},\quad d\ge C\Delta L^2/(\tau\varepsilon^3)$

**Oracle correspondence.** Applicable interfaces: function value and the entire subdifferential. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.17780) theorem: §2 Algorithms; Theorem 3.1; §5 Discussion

### B4 - Local-information impossibility at zero neighborhood radius

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\infty
$$

**Sources.** [2](https://www.jmlr.org/papers/volume23/21-1507/21-1507.pdf)

**Conditions.** $$\tau=0,\quad\varepsilon\le cL$$

**Dimension conditions.** $\tau=0,\quad\varepsilon\le cL$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** Proposition 11 in the published version supplies a hard instance for every arbitrary randomized local-information algorithm and every finite budget. At every nonminimizer, the Clarke residual is bounded below by a universal positive multiple of $L$. Hence, for $\tau=0$ and $\varepsilon\le cL$, no uniform finite expected-residual guarantee exists.

**Source location.** [2](https://www.jmlr.org/papers/volume23/21-1507/21-1507.pdf) theorem: Proposition 11 and Section 5.1; final JMLR PDF p. 12; Appendix C, pp. 34–38

## 5. Local arguments

### A1 - Descent, PL contraction, and zero-query endpoints

**Scope.** The exact smooth, PL, Clarke, Moreau, or composite residual specified in the associated bound.

**Algorithm scope.** Deterministic upper witnesses and elementary indistinguishability lower bounds.

Global $\beta$-smoothness and boundedness below imply
$$
f(x-\nabla f(x)/\beta)\le f(x)-\|\nabla f(x)\|^2/(2\beta).
$$
Thus $\|\nabla f(x_0)\|^2\le2\beta\Delta$. Summing the decrease and returning the queried point with least gradient norm gives $O(1+\beta\Delta/\epsilon^2)$ calls; values are unnecessary. If the initial gradient bound already meets the tolerance, output $x_0$ without querying.

A globally $\beta$-Lipschitz gradient gives Hessian norm at most $\beta$, so the second-order zero-query regime additionally requires permitted negative curvature at least $\beta$.

For a global $\mu$-PL objective,
$\mathrm{gap}_{t+1}\le(1-1/\kappa)\mathrm{gap}_t$.
This proves the exact ceiling formula for $1<\kappa$. At $\kappa=1$, one step is exact, and opposite translated quadratics exclude zero calls at nontrivial accuracy. At $\epsilon\ge\Delta$, the initial point suffices.

In one dimension, PL excludes nonoptimal stationary points. The minimizer set is an interval. Integrating
$|f'|\ge\sqrt{2\mu(f-f^\star)}$
along the decreasing side shows that a minimizer lies within $\sqrt{2\Delta/\mu}$ of $x_0$. Derivative-sign bisection and smoothness therefore give $O(\log(2+\kappa\Delta/\epsilon))$ calls.

Clarke subgradients of a globally $L$-Lipschitz function have norm at most $L$, so Goldstein residuals are at most $L$, also at radius zero. For a $\rho$-weakly convex function, proximal optimality gives
$\|\nabla f_{1/(2\rho)}(x_0)\|\le L$; the proximal objective inequality gives its square at most $4\rho\Delta$.
For a smooth composite objective, proximal-gradient descent gives
$F(y)\le F(x)-\|\mathcal G_\beta(x)\|^2/(2\beta)$,
so $\|\mathcal G_\beta(x_0)\|^2\le2\beta\Delta$.
These bounds certify the corresponding zero-query outputs; the output contract does not require computing the residual.

**Limits of the argument.** Each endpoint uses its own residual and model; the metrics are not interchangeable.

## References

[1] Guy Kornowski. The Complexity of Finding Stationary Points in Nonsmooth Nonconvex Optimization. 2026-09; preprint.

https://arxiv.org/pdf/2609.17780

[2] Guy Kornowski; Ohad Shamir. Oracle Complexity in Nonsmooth Nonconvex Optimization. JMLR 23(314), 2022; Proposition 11.

https://www.jmlr.org/papers/volume23/21-1507/21-1507.pdf
