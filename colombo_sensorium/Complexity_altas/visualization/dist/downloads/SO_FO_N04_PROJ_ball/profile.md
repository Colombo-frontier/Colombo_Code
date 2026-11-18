# Goldstein stationarity for Lipschitz nonconvex functions: normal-cone residual and projection; zero-respecting; stochastic full subgradients

**Setting ID.** `SO_FO_N04_PROJ_ball`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Bounds missing

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Convex body; geometry: Full space; smoothness: Differentiable samples; structure: Stochastic observation

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic subgradient; operation: Stochastic subgradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Explicit restriction; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: Zero respecting

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in Q}f(x)$$

### Admissible model

The public set $Q$ is nonempty, closed, and convex. Let $f=\mathbb E_\xi F(\cdot;\xi)$, with differentiable sample functions whose gradients need not be Lipschitz. The public point $x_0\in Q$ satisfies $f(x_0)-\inf_{x\in Q}f(x)\le\Delta$. At each $x\in Q$, fresh sample gradients are conditionally unbiased and have total second moment at most $\Gamma^2$. The Goldstein criterion is defined using the full-space function $f$. Here the feasible set is specifically $Q=B_2(0,D/2)$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

The sample functions and their distribution are part of the instance. The oracle specifies the observation protocol, unbiasedness, and moment budgets. Full-space local subdifferentials define the error measure but do not permit queries outside $Q$.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad \Delta>0,\quad \tau\ge0,\quad \varepsilon>0,\quad \Gamma>0,\quad D>0,\quad \tau>0$$

### Oracle interface

Public numerical inputs: $d,\ \tau,\ \varepsilon,\ x_0$.

Public upper bounds: $\Delta,\ \Gamma,\ D$.

The unknown object is the objective $f$.

Query points lie in $Q$; feedback consists of stochastic full subgradients:

$$G_t:\ \mathbb{E}[G_t\mid\mathcal{F}_{t-1},x_t]\in\partial f(x_t),\quad\mathbb{E}[\|G_t\|_2^2\mid\mathcal{F}_{t-1},x_t]\le\Gamma^2$$

Each call produces a fresh stochastic observation satisfying the stated moment bounds conditional on the history and current query. Same-point batch samples are conditionally independent. Reusing a sample across distinct points is not permitted.

The exact Euclidean projection $\Pi_Q(v)=\arg\min_{u\in Q}\|u-v\|_2$ is available.

The primitive stochastic response is $G_t=\nabla_x F(x_t;\xi_t)$. Here $F(\cdot;\xi)$ is a sample function and $f=\mathbb E_\xi F(\cdot;\xi)$ is the population objective.

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

The output must also satisfy the support, atomic-hull, or historical-span restriction of its algorithm view. An unqueried output remains subject to these restrictions.

### Loss or accuracy criterion

$$\mathcal{R}_\tau^{f,Q}(x)=\min_{g\in\partial_\tau f(x)}\operatorname{dist}(-g,N_Q(x))$$

$\partial_C f$ is the Clarke subdifferential, and $\partial_\tau f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\tau}\partial_C f(y)$. Here $\operatorname{dist}(z,S)=\inf_{u\in S}\|z-u\|_2$ and $\tau$ is the neighborhood radius.

The normal cone is $N_Q(x)=\{v:\langle v,y-x\rangle\le0\ \forall y\in Q\}$. Projection-based normal-cone residuals and Frank–Wolfe gaps retain their separate definitions and are not substituted for each other.

### Resource accounting

Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

Queries are zero-respecting: in the public standard coordinates, a coordinate must remain zero in every subsequent query until it has appeared with a nonzero value in an admissible feedback vector.

The nonzero support of the output must lie in the union of supports of previously returned gradients.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I,\forall\text{admissible oracle responses},\quad\mathbb{E}[\ell(I,\widehat{x})]\le\varepsilon$$

The probability space includes observation noise and the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f$: Unknown objective, with domain and structure specified by the model

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in Q}f(x)$$

$Q$: Feasible set of the task

$$Q\subseteq\mathbb{R}^d\ \text{\text{public, closed, and convex};\quad \text{when using} LMO \text{compactness is additionally required}}$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial_C f(x)$: Clarke subdifferential: the closed convex hull of limits of gradients at nearby differentiability points. Global Lipschitz continuity ensures that it is nonempty, compact, and convex.

$\partial_\tau f(x)$: Goldstein subdifferential with radius $\tau$

$$\partial_\tau f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\tau}\partial_C f(y)$$

$\operatorname{conv}$: Convex hull of a set

$\operatorname{dist}(z,S)$: Euclidean distance from a point to a set

$$\operatorname{dist}(z,S)=\inf_{u\in S}\|z-u\|_2$$

$N_Q(x)$: Outer normal cone of a closed convex set at $x$

$$N_Q(x)=\{v:\langle v,y-x\rangle\le0\ \forall y\in Q\}$$

$\mathcal{R}_\tau^{f,Q}$: Constrained Goldstein stationarity residual used in this profile

$$\mathcal{R}_\tau^{f,Q}(x)=\min_{g\in\partial_\tau f(x)}\operatorname{dist}(-g,N_Q(x))$$

$G_t$: $t$th full stochastic gradient or subgradient observation

$\xi$: Random observation sample; the oracle's interaction protocol determines sample-reuse permissions

$d$: Dimension; a public positive integer **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\Delta$: Public upper bound on the initial objective gap; the optimal value itself is unknown **Domain:** $\Delta>0$.

$\tau$: Goldstein neighborhood radius; it is not a failure probability **Domain:** $\tau\ge0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$\Gamma$: Public upper bound on the square root of the total second moment of the stochastic response; not the standard deviation of centered noise **Domain:** $\Gamma>0$.

$D$: Diameter upper bound for the public convex feasible set **Domain:** $D>0$.

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

### R1 - Zero-respecting lower-bound regime for the constrained residual

**Region.** $\tau>0,\quad C\varepsilon\tau\le\Delta\le c\varepsilon D^2/\tau,\quad\Gamma^2\ge C\varepsilon\Delta/\tau,\quad d\ge C\Delta/(\tau\varepsilon)$

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Upper bound missing

**Lower bound.** B1

$$
c\Delta\Gamma^2/(\tau\varepsilon^3)
$$

**Upper bound.** No admitted bound for this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $$\tau>0,\quad C\varepsilon\tau\le\Delta\le c\varepsilon D^2/\tau,\quad\Gamma^2\ge C\varepsilon\Delta/\tau,\quad d\ge C\Delta/(\tau\varepsilon)$$

**Dimension conditions.** $\tau>0,\quad C\varepsilon\tau\le\Delta\le c\varepsilon D^2/\tau,\quad\Gamma^2\ge C\varepsilon\Delta/\tau,\quad d\ge C\Delta/(\tau\varepsilon)$

**Oracle mapping.** Applicable interfaces: stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee mapping.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Gradient lower bound for the constrained residual under zero-respecting queries

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** The stated restricted randomized class

$$
c\Delta\Gamma^2/(\tau\varepsilon^3)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.13787v1)

**Source location.** [1](https://arxiv.org/pdf/2610.13787v1) theorem: Definition 8.13; Theorem 8.20; Corollaries 8.22–8.23, PDF pp.16, 18–20

## References

[1] Gon Buzaglo and Guy Kornowski. Optimal Algorithms for Nonsmooth Nonconvex Stochastic Optimization with Constraints. 2026, arXiv v1 preprint.

https://arxiv.org/pdf/2610.13787v1
