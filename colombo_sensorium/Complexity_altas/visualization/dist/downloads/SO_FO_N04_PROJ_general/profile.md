# Goldstein stationarity for Lipschitz nonconvex functions: normal-cone residual and projection; stochastic full subgradients

**Setting ID.** `SO_FO_N04_PROJ_general`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Bounds missing

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Convex body; geometry: Full space; smoothness: Differentiable samples; structure: Stochastic observation

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic subgradient; operation: Stochastic subgradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in Q}f(x)$$

### Admissible model

The public set $Q$ is nonempty, closed, and convex. Let $f=\mathbb E_\xi F(\cdot;\xi)$, with differentiable sample functions whose gradients need not be Lipschitz. The public point $x_0\in Q$ satisfies $f(x_0)-\inf_{x\in Q}f(x)\le\Delta$. At each $x\in Q$, fresh sample gradients are conditionally unbiased and have total second moment at most $\Gamma^2$. The Goldstein criterion is defined using the full-space function $f$.

Feasible geometry: $Q\subseteq\mathbb{R}^d\ \text{\text{public, closed, and convex};\quad \text{when using} LMO \text{compactness is additionally required}}$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

The sample functions and their distribution are part of the instance. The oracle specifies the observation protocol, unbiasedness, and moment budgets. Full-space local subdifferentials define the error measure but do not permit queries outside $Q$.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad \Delta>0,\quad \tau\ge0,\quad \varepsilon>0,\quad \Gamma>0,\quad \tau>0$$

### Oracle interface

Public numerical inputs: $d,\ \tau,\ \varepsilon,\ x_0$.

Public upper bounds: $\Delta,\ \Gamma$.

The unknown object is the objective $f$.

Query points lie in $Q$; feedback consists of stochastic full subgradients:

$$G_t:\ \mathbb{E}[G_t\mid\mathcal{F}_{t-1},x_t]\in\partial f(x_t),\quad\mathbb{E}[\|G_t\|_2^2\mid\mathcal{F}_{t-1},x_t]\le\Gamma^2$$

Each call produces a fresh stochastic observation satisfying the stated moment bounds conditional on the history and current query. Same-point batch samples are conditionally independent. Reusing a sample across distinct points is not permitted.

The exact Euclidean projection $\Pi_Q(v)=\arg\min_{u\in Q}\|u-v\|_2$ is available.

The primitive stochastic response is $G_t=\nabla_x F(x_t;\xi_t)$. Here $F(\cdot;\xi)$ is a sample function and $f=\mathbb E_\xi F(\cdot;\xi)$ is the population objective.

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\mathcal{R}_\tau^{f,Q}(x)=\min_{g\in\partial_\tau f(x)}\operatorname{dist}(-g,N_Q(x))$$

$\partial_C f$ is the Clarke subdifferential, and $\partial_\tau f(x)=\operatorname{conv}\bigcup_{\|y-x\|_2\le\tau}\partial_C f(y)$. Here $\operatorname{dist}(z,S)=\inf_{u\in S}\|z-u\|_2$ and $\tau$ is the neighborhood radius.

The normal cone is $N_Q(x)=\{v:\langle v,y-x\rangle\le0\ \forall y\in Q\}$. Projection-based normal-cone residuals and Frank–Wolfe gaps retain their separate definitions and are not substituted for each other.

### Resource accounting

The scalar resource $T$ counts fresh gradient observations only. Projection and sampling costs are retained jointly; no matching projection lower bound is asserted.

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

$c$: Sufficiently small absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $0<c<1$.

$C$: Sufficiently large absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $C>1$.

$T$: Total budget for the declared resource projection; for a risk curve, the budget is fixed in advance **Domain:** $T\in\mathbb{N}_{\ge0}$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

$\lceil a\rceil$: Smallest integer greater than or equal to $a$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** The scalar resource $T$ counts fresh gradient observations only. Projection and sampling costs are retained jointly; no matching projection lower bound is asserted.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Upper-bound regime for the constrained residual

**Region.** $\tau>0,\quad0<\varepsilon<\Gamma$

**Quantity.** Q1

**Resource.** The scalar resource $T$ counts fresh gradient observations only. Projection and sampling costs are retained jointly; no matching projection lower bound is asserted.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
\left\lceil C\log(C\Gamma/\varepsilon)\right\rceil\left\lceil C\Delta/(\tau\varepsilon)\right\rceil\left\lceil C\Gamma^2/\varepsilon^2\right\rceil
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $$\tau>0,\quad0<\varepsilon<\Gamma$$

**Dimension conditions.** $\tau>0,\quad0<\varepsilon<\Gamma$

**Oracle mapping.** Applicable interfaces: stochastic full subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee mapping.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Output mapping.** The projected output $p_{n^\star}$ of Algorithm 3 is returned, where $n^\star$ is the first successful wrapper trial, or the last trial if none succeeds. Each trial invokes the randomized Algorithm 1.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Gradient budget for the projected-residual algorithm

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\left\lceil C\log(C\Gamma/\varepsilon)\right\rceil\left\lceil C\Delta/(\tau\varepsilon)\right\rceil\left\lceil C\Gamma^2/\varepsilon^2\right\rceil
$$

**Sources.** [1](https://arxiv.org/pdf/2610.13787v1)

**Source location.** [1](https://arxiv.org/pdf/2610.13787v1) theorem: Theorem 4.1; Algorithm 3, lines 2–9; Algorithm 1, lines 5, 10–12; pdf pages: 4; 5; 6; printed pages: 4; 5; 6

Theorem 4.1 invokes Algorithm 3, whose line 4 calls Algorithm 1. Algorithm 1 uses private uniform draws for the query location (line 5), epoch transition (line 10), and output epoch (line 11), separately from gradient-sample randomness.

## References

[1] Gon Buzaglo and Guy Kornowski. Optimal Algorithms for Nonsmooth Nonconvex Stochastic Optimization with Constraints. 2026, arXiv v1 preprint.

https://arxiv.org/pdf/2610.13787v1
