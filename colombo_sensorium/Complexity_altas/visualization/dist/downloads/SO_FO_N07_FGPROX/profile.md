# Gradient-mapping stationarity for smooth nonconvex composite objectives: function values, gradients, and an exact proximal map

**Setting ID.** `SO_FO_N07_FGPROX`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Other quantified gap present

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Convex body; geometry: Full space; initialization: Initial gap; smoothness: Lipschitz gradient; structure: Composite

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Mixed; interface family: Value gradient prox; operation: Value gradient prox; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in \operatorname{dom}h}F(x)$$

The complete objective is $F=f+h$. The properties and Oracle interfaces of the two terms are specified separately.

### Admissible model

The unknown function $f:\mathbb R^d\to\mathbb R$ may be nonconvex and has a $\beta$-Lipschitz gradient. The function $h$ is public, proper, closed, and convex, and its exact proximal map is available. The objective is $F=f+h$, and the public point $x_0\in\operatorname{dom}h$ satisfies $F(x_0)-\inf F\le\Delta$.

Feasible geometry: $\operatorname{dom}h\subseteq\mathbb{R}^d$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ \Delta$.

The unknown object is the objective $f$. Access to the composite term $h$, including public information and proximal operations, is specified by the interface below.

Query points lie in $\mathbb{R}^d$; feedback consists of function values, gradients, and exact proximal access:

$$(f(x),\nabla f(x));\quad\operatorname{prox}_{\lambda h}(v)$$

All responses are consistent with one fixed function instance. Exact values and derivatives agree across repeated queries at the same point.

The exact proximal map of the public function $h$ is computable. Whether its calls are charged is specified by the resource convention.

$h$ and its exact proximal map are public. No proximal oracle for the unknown function $f$ is provided.

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\|\mathcal{G}_{1/\beta}(x)\|_2,\quad\mathcal{G}_\lambda(x)=\lambda^{-1}[x-\operatorname{prox}_{\lambda h}(x-\lambda\nabla F(x))]$$

### Resource accounting

The scalar resource counts gradient or value-gradient calls for the unknown function $f$. Proximal operations are available but excluded from this scalar $T$. Each upper bound also retains its joint vector of gradient and proximal costs.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Deterministic / Pointwise guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I,\forall\text{admissible oracle responses},\quad\ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I,\forall\text{admissible oracle responses},\quad\mathbb{E}[\ell(I,\widehat{x})]\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f,h,F$: Smooth or Lipschitz term, convex proximal term, and complete objective

$$F=f+h$$

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$\nabla F$: Full gradient of the differentiable complete objective with respect to the decision variable

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in Q}F(x)$$

$Q$: Feasible set of the task

$$\operatorname{dom}h\subseteq\mathbb{R}^d$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\operatorname{prox}_{\eta h}$: Proximal map of $h$, either public or obtained through the declared interface **Domain:** $\eta>0,\ v\in\mathbb{R}^d$.

$$\operatorname{prox}_{\eta h}(v)=\arg\min_u\{h(u)+\|u-v\|_2^2/(2\eta)\}$$

$\operatorname{dom}h$: Effective domain of $h$

$$\operatorname{dom}h=\{x:h(x)<+\infty\}$$

$\mathcal{G}_\lambda$: Composite gradient mapping **Domain:** $\lambda=1/\beta$.

$$\mathcal{G}_\lambda(x)=\lambda^{-1}[x-\operatorname{prox}_{\lambda h}(x-\lambda\nabla f(x))]$$

$d$: Dimension; a public positive integer **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant **Domain:** $\beta>0$.

$\Delta$: Public upper bound on the initial objective gap; the optimal value itself is unknown **Domain:** $\Delta>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $0<c<1$.

$C$: Sufficiently large absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $C>1$.

$T$: Total budget for the declared resource projection; for a risk curve, the budget is fixed in advance **Domain:** $T\in\mathbb{N}_{\ge0}$.

$N_G,N_{\mathrm{prox}}$: Unknown-function gradient calls and public-function proximal operations **Domain:** All are nonnegative integers.

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

**Definition.** Projection onto unknown-function gradient calls; proximal operations are counted separately

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Projection onto unknown-function gradient calls; proximal operations are counted separately

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - The initial gradient mapping already meets the tolerance

**Region.** $\varepsilon^2\ge2\beta\Delta$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** Projection onto unknown-function gradient calls; proximal operations are counted separately

**Status.** Optimal

**Lower bound.** B2, B7

$$
0
$$

**Upper bound.** B1, B6

$$
0
$$

### R2 - Sufficient dimension for an arbitrary randomized value-gradient lower bound

**Region.** $\varepsilon^2\le c\beta\Delta,\quad d\ge C(\beta\Delta/\varepsilon^2)^2\log(2+\beta\Delta/\varepsilon^2)$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** Projection onto unknown-function gradient calls; proximal operations are counted separately

**Status.** Optimal

**Lower bound.** B4, B9

$$
c\beta\Delta/\varepsilon^2
$$

**Upper bound.** B3, B8

$$
C\beta\Delta/\varepsilon^2
$$

**Gap or comparison.** $C/c$

### R3 - High-accuracy region below the sufficient-dimension threshold

**Region.** $\Theta_{\rm small}\setminus\Theta_{\rm hd}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Projection onto unknown-function gradient calls; proximal operations are counted separately

**Status.** Other quantified gap

**Lower bound.** B5

$$
c\log(2+\sqrt{\beta\Delta}/\varepsilon)
$$

**Upper bound.** B3

$$
C\beta\Delta/\varepsilon^2
$$

**Gap or comparison.** $C\beta\Delta/[\varepsilon^2\log(2+\sqrt{\beta\Delta}/\varepsilon)]$

### R4 - High-accuracy region below the sufficient-dimension threshold

**Region.** $\Theta_{\rm small}\setminus\Theta_{\rm hd}$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** Projection onto unknown-function gradient calls; proximal operations are counted separately

**Status.** Other quantified gap

**Lower bound.** B10

$$
c\log(2+\sqrt{\beta\Delta}/\varepsilon)
$$

**Upper bound.** B8

$$
C\beta\Delta/\varepsilon^2
$$

**Gap or comparison.** $C\beta\Delta/[\varepsilon^2\log(2+\sqrt{\beta\Delta}/\varepsilon)]$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $$\varepsilon^2\ge2\beta\Delta$$

**Dimension conditions.** $\varepsilon^2\ge2\beta\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B2 - Nonnegative resource budgets

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $$\varepsilon^2\ge2\beta\Delta$$

**Dimension conditions.** $\varepsilon^2\ge2\beta\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B3 - Proximal gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C(1+\beta\Delta/\varepsilon^2)
$$

**Sources.** [1](https://arxiv.org/pdf/1308.6594)

**Conditions.** $$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0$$

**Dimension conditions.** $d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1308.6594) theorem: Theorem 1; Corollary 1: exact proximal-gradient specialization

### B4 - Sufficiently high-dimensional subclass for arbitrary randomized value-gradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\beta\Delta/\varepsilon^2
$$

**Sources.** [3](https://arxiv.org/pdf/1710.11606)

**Conditions.** $$\varepsilon^2\le c\beta\Delta,\quad d\ge C(\beta\Delta/\varepsilon^2)^2\log(2+\beta\Delta/\varepsilon^2)$$

**Dimension conditions.** $\varepsilon^2\le c\beta\Delta,\quad d\ge C(\beta\Delta/\varepsilon^2)^2\log(2+\beta\Delta/\varepsilon^2)$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/1710.11606) theorem: Theorem 2, Section 5.3, with $h=0$; unrestricted query locations and value-gradient access are retained

### B5 - One-dimensional randomized FG subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\sqrt{\beta\Delta}/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/2209.07513)

**Conditions.** $$\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2209.07513) theorem: Theorems 2 and 5; one-dimensional subclasses give randomized gradient-only and value-gradient lower bounds

### B6 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $$\varepsilon^2\ge2\beta\Delta$$

**Dimension conditions.** $\varepsilon^2\ge2\beta\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B7 - Nonnegative resource budgets

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $$\varepsilon^2\ge2\beta\Delta$$

**Dimension conditions.** $\varepsilon^2\ge2\beta\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B8 - Proximal gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C(1+\beta\Delta/\varepsilon^2)
$$

**Sources.** [1](https://arxiv.org/pdf/1308.6594)

**Conditions.** $$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0$$

**Dimension conditions.** $d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1308.6594) theorem: Theorem 1; Corollary 1: exact proximal-gradient specialization

### B9 - Sufficiently high-dimensional subclass for arbitrary randomized value-gradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\beta\Delta/\varepsilon^2
$$

**Sources.** [3](https://arxiv.org/pdf/1710.11606)

**Conditions.** $$\varepsilon^2\le c\beta\Delta,\quad d\ge C(\beta\Delta/\varepsilon^2)^2\log(2+\beta\Delta/\varepsilon^2)$$

**Dimension conditions.** $\varepsilon^2\le c\beta\Delta,\quad d\ge C(\beta\Delta/\varepsilon^2)^2\log(2+\beta\Delta/\varepsilon^2)$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/1710.11606) theorem: Theorem 2, Section 5.3, with $h=0$; unrestricted query locations and value-gradient access are retained

### B10 - One-dimensional randomized FG subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\sqrt{\beta\Delta}/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/2209.07513)

**Conditions.** $$\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2209.07513) theorem: Theorems 2 and 5; one-dimensional subclasses give randomized gradient-only and value-gradient lower bounds

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

[1] Saeed Ghadimi; Guanghui Lan; Hongchao Zhang. Mini-batch Stochastic Approximation Methods for Nonconvex Stochastic Composite Optimization. 2016; arXiv v2 2013.

https://arxiv.org/pdf/1308.6594

[2] Sinho Chewi; Sébastien Bubeck; Adil Salim. On the complexity of finding stationary points of smooth functions in one dimension. 2023.

https://arxiv.org/pdf/2209.07513

[3] Yair Carmon; John C. Duchi; Oliver Hinder; Aaron Sidford. Lower Bounds for Finding Stationary Points I. 2020; arXiv v3 2019.

https://arxiv.org/pdf/1710.11606
