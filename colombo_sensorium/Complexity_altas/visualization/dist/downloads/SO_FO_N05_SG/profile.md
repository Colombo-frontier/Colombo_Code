# Moreau-envelope stationarity for weakly convex Lipschitz functions: one full subgradient

**Setting ID.** `SO_FO_N05_SG`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Polynomial gap present; Bounds missing

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; convexity: Weakly convex; geometry: Full space; initialization: Initial gap; smoothness: Lipschitz function

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Subgradient; operation: Subgradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

The unknown function $f:\mathbb R^d\to\mathbb R$ is globally $L$-Lipschitz, $\rho$-weakly convex, and bounded below, with $f(x_0)-\inf f\le\Delta$. Weak convexity means that $f(x)+\rho\|x\|_2^2/2$ is convex. The full subdifferential is the nonempty compact convex set $\partial f(x)=\partial(f+\rho\|\cdot\|_2^2/2)(x)-\rho x$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad L>0,\quad \rho>0,\quad \Delta>0,\quad \varepsilon>0$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $L,\ \rho,\ \Delta$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of one full subgradient:

$$g\in\partial f(x)$$

All responses are consistent with one fixed function instance. If several subgradients are admissible, the oracle selects one; the algorithm receives only that vector.

No proximal or Moreau-gradient queries for the objective $f$ are provided.

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

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f$: Unknown objective, with domain and structure specified by the model

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial f(x)$: Subdifferential of a weakly convex function, obtained by subtracting the quadratic gradient from the convex subdifferential of its quadratic regularization

$$\partial f(x)=\partial(f+\rho\|\cdot\|_2^2/2)(x)-\rho x$$

$g$: One subgradient vector selected and returned by the oracle, rather than the entire subdifferential

$f_\lambda$: Moreau envelope **Domain:** $\lambda=1/(2\rho)$.

$$f_\lambda(x)=\min_y\{f(y)+\|y-x\|_2^2/(2\lambda)\}$$

$\operatorname{prox}_{\lambda f}$: Unique proximal minimizer in the definition of the Moreau envelope; it defines the error criterion and is not an available primitive oracle

$d$: Dimension; a public positive integer **Domain:** $d\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the objective Lipschitz constant **Domain:** $L>0$.

$\rho$: Public upper bound on the weak-convexity parameter **Domain:** $\rho>0$.

$\Delta$: Public upper bound on the initial objective gap; the optimal value itself is unknown **Domain:** $\Delta>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $0<c<1$.

$C$: Sufficiently large absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $C>1$.

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

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - No queries required

**Region.** $\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B2, B7

$$
0
$$

**Upper bound.** B1, B6

$$
0
$$

### R2 - Small initial suboptimality in sufficiently high dimension

**Region.** $\rho\Delta\le L^2,\quad\varepsilon^2\le c\min\{L^2,\rho\Delta\},\quad d\ge C\rho\Delta L^2/\varepsilon^4$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B5

$$
c\rho\Delta L^2/\varepsilon^4
$$

**Upper bound.** B3, B4

$$
C\rho\Delta L^2/\varepsilon^4
$$

**Gap or comparison.** $C/c$

**Comparison argument.** Intersect this comparison region with N05-domain. The bounds match in sufficiently high dimension when $\rho\Delta\le L^2$. A lower bound for the strongest FSD interface matches an upper bound for the weakest SG interface.

### R3 - Large initial suboptimality in sufficiently high dimension

**Region.** $\rho\Delta>L^2,\quad\varepsilon^2\le cL^2,\quad d\ge CL^4/\varepsilon^4$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Polynomial gap

**Lower bound.** B5

$$
cL^4/\varepsilon^4
$$

**Upper bound.** B3, B4

$$
C\rho\Delta L^2/\varepsilon^4
$$

**Gap or comparison.** $C\rho\Delta/L^2$

**Comparison argument.** Intersect this comparison region with N05-domain. The accepted envelopes have a linear gap in the joint parameter $\rho\Delta/L^2$. When that ratio is fixed and only accuracy varies, the bounds match up to constants.

### R4 - High accuracy in arbitrary dimension

**Region.** $\varepsilon^2\le c\min\{L^2,\rho\Delta\}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3, B4

$$
\frac{C\rho\Delta}{\varepsilon^2}\min\{L^2/\varepsilon^2,d\log(2+L/\varepsilon)\}
$$

**Comparison argument.** Intersect this comparison region with N05-domain. The upper envelope applies in every dimension; a high-dimensional lower bound that fails to cover this full region is not inserted. The fixed-dimensional $\varepsilon^{-2}\log(1/\varepsilon)$ accuracy upper bound remains valid, but no matching lower bound is included.

### R5 - High accuracy in arbitrary dimension

**Region.** $\varepsilon^2\le c\min\{L^2,\rho\Delta\}$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B8, B9

$$
\frac{C\rho\Delta}{\varepsilon^2}\min\{L^2/\varepsilon^2,d\log(2+L/\varepsilon)\}
$$

**Comparison argument.** Intersect this comparison region with N05-domain. The upper envelope applies in every dimension; a high-dimensional lower bound that fails to cover this full region is not inserted. The fixed-dimensional $\varepsilon^{-2}\log(1/\varepsilon)$ accuracy upper bound remains valid, but no matching lower bound is included.

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

**Conditions.** $$\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$$

**Dimension conditions.** $\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential, the entire subdifferential, stochastic full subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Local argument.** A1

### B2 - Nonnegative resource budgets

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $$\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$$

**Dimension conditions.** $\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential, the entire subdifferential, stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B3 - Deterministic inexact proximal method with a strongly convex subgradient inner solver

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\rho\Delta L^2/\varepsilon^4
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980) [1](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [4](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon^2\le c\min\{L^2,\rho\Delta\}$$

**Dimension conditions.** $\varepsilon^2\le c\min\{L^2,\rho\Delta\}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential, the entire subdifferential. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A2, A3, A4

### B4 - Deterministic finite-dimensional subgradient-certificate inner solver

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\rho\Delta d\log(2+L/\varepsilon)/\varepsilon^2
$$

**Sources.** [1](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/1405.4980) [4](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon^2\le c\min\{L^2,\rho\Delta\}$$

**Dimension conditions.** $\varepsilon^2\le c\min\{L^2,\rho\Delta\}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential, the entire subdifferential. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A2, A3, A4

**Source location.** [1](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) theorem: Proposition 2.1(ii), combined with the finite-dimensional subgradient certificate

### B5 - Deterministic rotational lower bound with full-subdifferential access

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
cL^2\min\{\rho\Delta,L^2\}/\varepsilon^4
$$

**Sources.** [2](https://arxiv.org/pdf/2608.03246)

**Conditions.** $$\varepsilon^2\le c\min\{L^2,\rho\Delta\},\quad d\ge C L^2\min\{\rho\Delta,L^2\}/\varepsilon^4$$

**Dimension conditions.** $\varepsilon^2\le c\min\{L^2,\rho\Delta\},\quad d\ge C L^2\min\{\rho\Delta,L^2\}/\varepsilon^4$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential, the entire subdifferential. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2608.03246) theorem: Definition 2.3; Theorem 3.2 and Remark 3.1; the rotational extension in Section 6; Closing Remark in Section 7

### B6 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $$\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$$

**Dimension conditions.** $\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential, the entire subdifferential, stochastic full subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Local argument.** A1

### B7 - Nonnegative resource budgets

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $$\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$$

**Dimension conditions.** $\varepsilon\ge\min\{L,2\sqrt{\rho\Delta}\}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential, the entire subdifferential, stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B8 - Deterministic inexact proximal method with a strongly convex subgradient inner solver

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\rho\Delta L^2/\varepsilon^4
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980) [1](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [4](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon^2\le c\min\{L^2,\rho\Delta\}$$

**Dimension conditions.** $\varepsilon^2\le c\min\{L^2,\rho\Delta\}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential, the entire subdifferential. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A2, A3, A4

### B9 - Deterministic finite-dimensional subgradient-certificate inner solver

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\rho\Delta d\log(2+L/\varepsilon)/\varepsilon^2
$$

**Sources.** [1](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/1405.4980) [4](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon^2\le c\min\{L^2,\rho\Delta\}$$

**Dimension conditions.** $\varepsilon^2\le c\min\{L^2,\rho\Delta\}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient, function value and the entire subdifferential, the entire subdifferential. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A2, A3, A4

**Source location.** [1](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) theorem: Proposition 2.1(ii), combined with the finite-dimensional subgradient certificate

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

### A2 - A charged inexact proximal-point algorithm

**Scope.** One complete subgradient of a globally Lipschitz weakly convex function.

**Algorithm scope.** Deterministic upper witness.

At $x_t$, solve $h_t(y)=f(y)+\rho\|y-x_t\|^2$ to gap
$\epsilon_{\rm in}=c\epsilon^2/\rho$.
This objective is $\rho$-strongly convex and its minimizer lies within $L/(2\rho)$ of $x_t$. On the public ball of radius $L/\rho$, an observed subgradient plus $2\rho(y-x_t)$ is an inner subgradient of norm at most $3L$.

The weighted strongly convex solver costs $O(L^2/\epsilon^2)$ true calls per outer step. The centroid certificate alternatively costs $O(d\log(2+L/\epsilon))$. Both use only one returned subgradient; neither grants a free proximal map for the unknown function.

For inner output $x_{t+1}$ and exact proximal point $p_t$,
$$
f(x_{t+1})\le f(x_t)-\rho\|x_{t+1}-x_t\|^2+\epsilon_{\rm in},
\quad
\|x_{t+1}-p_t\|^2\le2\epsilon_{\rm in}/\rho.
$$
After $K=\lceil C\rho\Delta/\epsilon^2\rceil$ steps,
$\min_t\|x_{t+1}-x_t\|^2\le\Delta/(\rho K)+\epsilon_{\rm in}/\rho$.
Return the $x_t$ with smallest observed step. Since
$\nabla f_{1/(2\rho)}(x_t)=2\rho(x_t-p_t)$, suitable constants give norm at most $\epsilon$. Multiplying outer and inner budgets gives both recorded bounds. Selection needs no function values.

**Limits of the argument.** Every inner call is charged. The argument does not supply the unknown objective proximal map for free.

### A3 - Projected and weighted subgradient bounds

**Scope.** Public Euclidean projection; unbiased conditional subgradient mean and a total second-moment bound, or exact subgradients.

**Algorithm scope.** Deterministic policies and deterministic averages; randomness may come from observations.

Projection onto a public closed convex set gives
$$
\|x_{t+1}-x^\star\|^2\le\|x_t-x^\star\|^2
-2\eta_t\langle g_t,x_t-x^\star\rangle+\eta_t^2\|g_t\|^2.
$$
For convex $f$, initial distance at most $R$, and conditional second moment at most $V$, the constant step $R/\sqrt{VK}$ and averaged output have expected gap at most $R\sqrt{V/K}$. Exact subgradients correspond to $V=L^2$.

Under $\mu$-strong convexity, use $\eta_t=2/[\mu(t+1)]$. With $a_t=\mathbb E\|x_t-x^\star\|^2$,
$$
\mathbb E[f(x_t)-f^\star]\le{\mu(t-1)\over4}a_t
-{\mu(t+1)\over4}a_{t+1}+{V\over\mu(t+1)}.
$$
Multiply by $t$, sum, and use convexity. The weighted output
$\sum_{t=1}^K2t\,x_t/[K(K+1)]$ has expected gap at most $2V/[\mu(K+1)]$. Neither output rule requires private randomness. Apply norm conversion before these inequalities, preserving all dimension factors.

**Limits of the argument.** Norm-conversion factors must be applied explicitly. No noisy cutting-plane result follows from this recursion.

### A4 - Subgradient certificates and centroid cuts

**Scope.** One full subgradient is sufficient. Public compact convex geometry and exact internal geometric computation are available.

**Algorithm scope.** Deterministic upper-bound witness; valid as an upper bound for randomized views.

Let $Q\subset\mathbb R^d$ be public, compact, convex, and full dimensional, with diameter at most $D$ in the stated norm. Suppose all returned subgradients have dual norm at most $L$. Query $g_i\in\partial f(x_i)$ at the centroid of the current body and retain $\langle g_i,x_i-x\rangle\ge0$. The centroid halfspace theorem bounds the retained volume by $(1-e^{-1})^T\operatorname{vol}(Q)$.

The computable certificate is
$$
\Gamma_T=\min_{\lambda\in\Delta_T}\max_{x\in Q}\sum_i\lambda_i\langle g_i,x_i-x\rangle
=\max_{x\in Q}\min_i\langle g_i,x_i-x\rangle.
$$
The equality is convex minimax. Subgradient inequalities and convexity imply
$f(\sum_i\lambda_ix_i)-\min_Qf\le\Gamma_T$.
If $\Gamma_T>\epsilon$, choose $z\in Q$ with all cut margins greater than $\epsilon$. The copy $(1-a)z+aQ$, where $a=\epsilon/[2(\epsilon+LD)]$, survives every cut. Its volume is $a^d\operatorname{vol}(Q)$, contradicting centroid shrinkage once $T>C d\log(2+LD/\epsilon)$. If the body loses volume earlier, the same positive-volume argument already certifies the error. No function values or inscribed-ball estimate are required.

For $Q=RB_p^d$ and $\ell_q$-Lipschitz objectives, use $D=2Rd^{(1/q-1/p)_+}$. Returning the center has error at most $LRd^{(1/q-1/p)_+}$, giving the coarse zero-query regime. Exact centroid, minimax, and public geometric calculations are uncharged internal operations.

For a deterministic selector with total movement at most $W(T)$ on nested convex sets, instead impose deep cuts of margin $2LW(T)/T$. If all $T$ sets are nonempty, every move has length at least $2W(T)/T$, contradicting the movement bound. At the first empty intersection, minimax gives error at most $2LW(T)/T$. Substitution of the cited stable-movement theorem yields the recorded nondual upper bound. Its deterministic information scope is distinct from the scope of randomized implementations.

**Limits of the argument.** The stable-selector branch imports its movement theorem and does not claim efficient deterministic arithmetic time.

**Sources.** [3](https://arxiv.org/pdf/1405.4980) [1](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [4](https://arxiv.org/pdf/2609.20701)

## References

[1] Arkadi Nemirovski; Shmuel Onn; Uriel G. Rothblum. Accuracy Certificates for Computational Problems with Convex Structure. 2010.

https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf

[2] Jiajin Li; Siyu Pan. Optimal Deterministic Oracle Complexity for Weakly Convex Optimization. 2026-08-04; preprintv1.

https://arxiv.org/pdf/2608.03246

[3] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015.

https://arxiv.org/pdf/1405.4980

[4] David Martínez-Rubio; Cristóbal Guzmán. Stable Movement for Nondual Lipschitz Convex Optimization: Efficiency and Nearly Optimal Oracle Rates. 2026-09-17; preprintv1.

https://arxiv.org/pdf/2609.20701
