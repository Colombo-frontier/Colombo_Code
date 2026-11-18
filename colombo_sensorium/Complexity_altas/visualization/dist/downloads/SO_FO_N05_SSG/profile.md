# Moreau-envelope stationarity for weakly convex Lipschitz functions: stochastic full subgradients

**Setting ID.** `SO_FO_N05_SSG`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Bounds missing

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; convexity: Weakly convex; geometry: Full space; initialization: Initial gap; smoothness: Lipschitz function; structure: Stochastic observation

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

The unknown function $f:\mathbb R^d\to\mathbb R$ is globally $L$-Lipschitz, $\rho$-weakly convex, and bounded below, with $f(x_0)-\inf f\le\Delta$. Weak convexity means that $f(x)+\rho\|x\|_2^2/2$ is convex. The full subdifferential is the nonempty compact convex set $\partial f(x)=\partial(f+\rho\|\cdot\|_2^2/2)(x)-\rho x$. Stochastic observations have conditional mean in this subdifferential and total second moment at most $\Gamma^2$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad L>0,\quad \rho>0,\quad \Delta>0,\quad \varepsilon>0,\quad \Gamma>0$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $L,\ \rho,\ \Delta,\ \Gamma$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of stochastic full subgradients:

$$G_t:\ \mathbb{E}[G_t\mid\mathcal{F}_{t-1},x_t]\in\partial f(x_t),\quad\mathbb{E}[\|G_t\|_2^2\mid\mathcal{F}_{t-1},x_t]\le\Gamma^2$$

Each call produces a fresh stochastic observation satisfying the stated moment bounds conditional on the history and current query. Same-point batch samples are conditionally independent. Reusing a sample across distinct points is not permitted.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(f,x)=\|\nabla f_{1/(2\rho)}(x)\|_2,\quad f_\lambda(x)=\min_y\{f(y)+\|y-x\|_2^2/(2\lambda)\}$$

Fix $\lambda=1/(2\rho)$. Weak convexity makes the Moreau envelope differentiable, with $\nabla f_\lambda(x)=\lambda^{-1}(x-\operatorname{prox}_{\lambda f}(x))$. This identity defines the error criterion; it does not grant proximal queries.

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

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial f(x)$: Subdifferential of a weakly convex function, obtained by subtracting the quadratic gradient from the convex subdifferential of its quadratic regularization

$$\partial f(x)=\partial(f+\rho\|\cdot\|_2^2/2)(x)-\rho x$$

$f_\lambda$: Moreau envelope **Domain:** $\lambda=1/(2\rho)$.

$$f_\lambda(x)=\min_y\{f(y)+\|y-x\|_2^2/(2\lambda)\}$$

$\operatorname{prox}_{\lambda f}$: Unique proximal minimizer in the definition of the Moreau envelope; it defines the error criterion and is not an available primitive oracle

$G_t$: $t$th full stochastic gradient or subgradient observation

$d$: Dimension; a public positive integer **Domain:** $d\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the objective Lipschitz constant **Domain:** $L>0$.

$\rho$: Public upper bound on the weak-convexity parameter **Domain:** $\rho>0$.

$\Delta$: Public upper bound on the initial objective gap; the optimal value itself is unknown **Domain:** $\Delta>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$\Gamma$: Public upper bound on the square root of the total second moment of the stochastic response; not the standard deviation of centered noise **Domain:** $\Gamma>0$.

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

### R1 - No queries required

**Region.** $\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$

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

### R2 - Parameter conditions shared by this family

**Region.** $d\in\mathbb{N}_{\ge1},\quad L>0,\quad \rho>0,\quad \Delta>0,\quad \varepsilon>0$

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

$$
C(1+\rho\Delta\Gamma^2/\varepsilon^4)
$$

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

**Conditions.** $$\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$$

**Dimension conditions.** $\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential, the entire subdifferential, stochastic full subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Local argument.** A1

### B2 - Nonnegative resource budgets

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $$\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$$

**Dimension conditions.** $\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential, the entire subdifferential, stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B3 - Stochastic model-based subgradient method

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C(1+\rho\Delta\Gamma^2/\varepsilon^4)
$$

**Sources.** [1](https://sites.math.washington.edu/~ddrusv/combined_model_based.pdf)

**Conditions.** $$d\in\mathbb{N}_{\ge1},\quad L>0,\quad \rho>0,\quad \Delta>0,\quad \varepsilon>0$$

**Dimension conditions.** $d\in\mathbb{N}_{\ge1},\quad L>0,\quad \rho>0,\quad \Delta>0,\quad \varepsilon>0$

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://sites.math.washington.edu/~ddrusv/combined_model_based.pdf) theorem: Assumptions A1–A3; Algorithm 3.1; Theorem 3.1; (3.4)–(3.5), PDF pp.12–13

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

[1] Damek Davis and Dmitriy Drusvyatskiy. Stochastic Model-Based Minimization of Weakly Convex Functions. 2019.

https://sites.math.washington.edu/~ddrusv/combined_model_based.pdf
