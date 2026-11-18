# Goldstein stationarity for Lipschitz nonconvex functions: stochastic full subgradients

**Setting ID.** `SO_FO_N04_SSG`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Fully optimal

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; initialization: Initial gap; smoothness: Lipschitz function; structure: Stochastic observation

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic subgradient; operation: Stochastic subgradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

The unknown function $f$ is globally $\Gamma$-Lipschitz and bounded below, with initial suboptimality at most $\Delta$. Every fresh observation has conditional mean in the Clarke subdifferential and total second moment at most $\Gamma^2$. The same bound $\Gamma$ controls both quantities; there is no independent Lipschitz parameter $L$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad \Delta>0,\quad \tau\ge0,\quad \varepsilon>0,\quad \Gamma>0,\quad \tau>0$$

### Oracle interface

Public numerical inputs: $d,\ \tau,\ \varepsilon$.

Public upper bounds: $\Delta,\ \Gamma$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of stochastic full subgradients:

$$G_t:\ \mathbb{E}[G_t\mid\mathcal{F}_{t-1},x_t]\in\partial f(x_t),\quad\mathbb{E}[\|G_t\|_2^2\mid\mathcal{F}_{t-1},x_t]\le\Gamma^2$$

Each call produces a fresh stochastic observation satisfying the stated moment bounds conditional on the history and current query. Same-point batch samples are conditionally independent. Reusing a sample across distinct points is not permitted.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\operatorname{dist}(0,\partial_\tau f(x)),\quad\partial_\tau f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\tau}\partial_C f(y)$$

$\partial_C f$ is the Clarke subdifferential, and $\partial_\tau f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\tau}\partial_C f(y)$. Here $\operatorname{dist}(z,S)=\inf_{u\in S}\|z-u\|_2$ and $\tau$ is the neighborhood radius.

### Resource accounting

Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I,\forall\text{admissible oracle responses},\quad\mathbb{E}[\ell(I,\widehat{x})]\le\varepsilon$$

The probability space includes observation noise and the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f$: Unknown objective, with domain and structure specified by the model

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

$G_t$: $t$th full stochastic gradient or subgradient observation

$d$: Dimension; a public positive integer **Domain:** $d\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the objective Lipschitz constant **Domain:** $L>0$.

$\Delta$: Public upper bound on the initial objective gap; the optimal value itself is unknown **Domain:** $\Delta>0$.

$\tau$: Goldstein neighborhood radius; it is not a failure probability **Domain:** $\tau\ge0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$\Gamma$: Public upper bound on the square root of the total second moment of the stochastic response; not the standard deviation of centered noise **Domain:** $\Gamma>0$.

$c$: Sufficiently small absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $0<c<1$.

$C$: Sufficiently large absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $C>1$.

$d_{\rm hd}$: Sufficient dimension for the randomized CMO hard construction; not specified numerically **Domain:** $d_{\rm hd}\in\mathbb{N}$.

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

### R1 - Matching high-dimensional regime with nonzero noise

**Region.** $\varepsilon\le c\Gamma,\quad\tau\varepsilon\le c\Delta,\quad\Gamma\ge11\sqrt{2\varepsilon\Delta/\tau},\quad d\ge d_{\rm hd}$

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B2

$$
c\Delta\Gamma^2/(\tau\varepsilon^3)
$$

**Upper bound.** B1

$$
C\Delta\Gamma^2/(\tau\varepsilon^3)
$$

**Gap or comparison.** $C/c$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Online-to-nonconvex conversion with stochastic observations

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C[1+\Gamma^2/\varepsilon^2+\Delta/(\tau\varepsilon)+\Delta\Gamma^2/(\tau\varepsilon^3)]
$$

**Sources.** [1](https://arxiv.org/pdf/2302.03775)

**Conditions.** $$\Gamma>0,\quad\tau>0;\quad\text{\text{function Lipschitz bound and total second-moment bound both use} }\Gamma$$

**Dimension conditions.** $\Gamma>0,\quad\tau>0;\quad\text{\text{function Lipschitz bound and total second-moment bound both use} }\Gamma$

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://arxiv.org/pdf/2302.03775) theorem: Corollary 9; Proposition 2 and Corollary 6. General Lipschitz functions use full-dimensional local smoothing.

### B2 - Hard instances with nonzero observation noise

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\Delta\Gamma^2/(\tau\varepsilon^3)
$$

**Sources.** [1](https://arxiv.org/pdf/2302.03775)

**Conditions.** $$\varepsilon\le c\Gamma,\quad\tau\varepsilon\le c\Delta,\quad\Gamma\ge11\sqrt{2\varepsilon\Delta/\tau},\quad d\ge d_{\rm hd}$$

**Dimension conditions.** $\varepsilon\le c\Gamma,\quad\tau\varepsilon\le c\Delta,\quad\Gamma\ge11\sqrt{2\varepsilon\Delta/\tau},\quad d\ge d_{\rm hd}$

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2302.03775) theorem: Theorem 28 and Appendix F, PDF p. 32; rescaling the source hard instance to Goldstein stationarity

## References

[1] Ashok Cutkosky; Harsh Mehta; Francesco Orabona. Optimal Stochastic Non-smooth Non-convex Optimization through Online-to-Non-convex Conversion. 2023; arXiv v3 2025.

https://arxiv.org/pdf/2302.03775
