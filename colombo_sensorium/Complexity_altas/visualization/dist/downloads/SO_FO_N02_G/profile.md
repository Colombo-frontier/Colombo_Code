# Approximate second-order stationarity using first-order information: exact gradients

**Setting ID.** `SO_FO_N02_G`

Single-objective optimization

Find a point with a sufficiently small gradient and no substantial negative curvature.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Second order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; initialization: Initial gap; smoothness: Lipschitz gradient; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Gradient; operation: Gradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Second order stationarity

**GUARANTEE tags.** aggregation: Per instance; confidence: Failure probability parameter explicitly declared; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point with a sufficiently small gradient and no substantial negative curvature.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

$f\in C^2(\mathbb R^d)$ has a globally $\beta$-Lipschitz gradient and a globally $\beta_2$-Lipschitz Hessian. It is bounded below and satisfies $f(x_0)-\inf f\le\Delta$. The oracle does not return the Hessian or Hessian-vector products.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Hessian regularity means $\|\nabla^2 f(u)-\nabla^2 f(v)\|_{\mathrm{op}}\le\beta_2\|u-v\|_2$ for all $u,v\in\mathbb R^d$.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \beta_2>0,\quad \Delta>0,\quad \varepsilon>0,\quad \varepsilon_{\mathrm{H}}>0$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ \varepsilon_{\mathrm{H}},\ x_0$.

Public upper bounds: $\beta,\ \beta_2,\ \Delta$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of exact gradients:

$$\nabla f(x)$$

All responses are consistent with one fixed function instance. Exact values and derivatives agree across repeated queries at the same point.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$(\|\nabla f(x)\|_2,\;[-\lambda_{\min}(\nabla^2 f(x))]_+)$$

$[a]_+=\max\{a,0\}$. The two tolerances are the gradient-norm tolerance $\varepsilon$ and the negative-curvature tolerance $\varepsilon_{\mathrm H}$.

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

$$\forall f:\ \|\nabla f(\widehat{x})\|\le\varepsilon,\quad\lambda_{\min}(\nabla^2 f(\widehat{x}))\ge-\varepsilon_{\mathrm{H}}$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

#### Randomized / Probability guarantee

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall f:\ \Pr(\|\nabla f(\widehat{x})\|\le\varepsilon,\ \lambda_{\min}(\nabla^2 f(\widehat{x}))\ge-\varepsilon_{\mathrm{H}})\ge1-\delta$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

**Oracle qualification.** This view additionally takes the public confidence parameter $\delta$, with $0<\delta\le1/3$.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f$: Unknown objective, with domain and structure specified by the model

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$\nabla^2f$: Hessian matrix of the objective **Domain:** $\nabla^2f(x)\in\mathbb{R}^{d\times d}$.

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\|\cdot\|_{\mathrm{op}}$: Matrix or multilinear operator norm induced by the stated vector norm

$\lambda_{\min}$: Smallest eigenvalue of a real symmetric Hessian matrix

$[a]_+$: Positive part of a real number $a$

$$[a]_+=\max\{a,0\}$$

$d$: Dimension; a public positive integer **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant **Domain:** $\beta>0$.

$\beta_2$: Public upper bound on the Hessian Lipschitz constant; the oracle need not supply Hessians **Domain:** $\beta_2>0$.

$\Delta$: Public upper bound on the initial objective gap; the optimal value itself is unknown **Domain:** $\Delta>0$.

$\varepsilon$: Gradient-norm tolerance; negative curvature is controlled separately by $\varepsilon_{\mathrm H}$ **Domain:** $\varepsilon>0$.

$\varepsilon_{\mathrm{H}}$: Allowed magnitude of negative curvature in the smallest Hessian eigenvalue **Domain:** $\varepsilon_{\mathrm{H}}>0$.

$c$: Sufficiently small absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $0<c<1$.

$C$: Sufficiently large absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $C>1$.

$d_{\rm hd}$: Finite dimension sufficient for the lower-bound construction against arbitrary randomized algorithms with Lipschitz Hessians. The theorem certifies sufficiently large $d$, not an optimal dimension threshold. **Domain:** $d_{\rm hd}\in\mathbb{N}$.

$C_d$: Positive constant depending only on the subscripted parameters fixed in advance. It does not support uniform optimality when those parameters grow jointly. **Domain:** $C_d>0$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\delta$: Failure probability, distinct from the Goldstein neighborhood radius **Domain:** $0<\delta\le1/3$.

$\Lambda_{\rm prob}$: Logarithmic scale in LL23; its sixth power is retained exactly as in the theorem, without assigning an unsupported numerical value. **Domain:** $\Lambda_{\rm prob}=\operatorname{polylog}(d,\beta,\beta_2,\Delta,1/\varepsilon,1/\delta)$.

$$\Lambda_{\rm prob}=LL23 Theorem 5 logarithmic scale$$

$\Pr,\mathbb{P}$: Event probability after the instance and admissible response law are fixed

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

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized / Probability guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Both coarse-accuracy conditions hold automatically

**Region.** $\varepsilon^2\ge2\beta\Delta,\quad\varepsilon_H\ge\beta$

**Views.** Deterministic / Pointwise guarantee

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

### R2 - Normalized fixed-dimensional accuracy branch

**Region.** $\beta=\beta_2=\Delta=1,\quad\varepsilon_H=\sqrt\varepsilon,\quad\varepsilon\le c$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B6

$$
c\varepsilon^{-3/2}
$$

**Upper bound.** B4

$$
C_d\varepsilon^{-3/2}
$$

**Gap or comparison.** $C_d/c$

### R3 - Both coarse-accuracy conditions hold automatically

**Region.** $\varepsilon^2\ge2\beta\Delta,\quad\varepsilon_H\ge\beta$

**Views.** Randomized / Probability guarantee

**Quantity.** Q4

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B9

$$
0
$$

**Upper bound.** B8

$$
0
$$

### R4 - Balanced tolerances in sufficiently high dimension

**Region.** $\Theta_{\rm balanced},\quad d\ge d_{\rm hd}$

**Views.** Randomized / Probability guarantee

**Quantity.** Q4

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Logarithmic gap

**Lower bound.** B11

$$
c\Delta\sqrt\beta\beta_2^{1/4}\varepsilon^{-7/4}
$$

**Upper bound.** B10, B12

$$
C\Delta\sqrt\beta\beta_2^{1/4}\varepsilon^{-7/4}\Lambda_{\rm prob}^6
$$

**Gap or comparison.** $C\Lambda_{\rm prob}^6$

**Comparison argument.** Intersect this comparison region with N02-parameters-R. The high-dimensional balanced-accuracy rate for randomized algorithms is near-optimal; optimal dependence on the failure probability $\delta$ is not claimed.

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

**Conditions.** $$\varepsilon^2\ge2\beta\Delta,\quad\varepsilon_H\ge\beta$$

**Dimension conditions.** $\varepsilon^2\ge2\beta\Delta,\quad\varepsilon_H\ge\beta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

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

**Conditions.** $$\varepsilon^2\ge2\beta\Delta,\quad\varepsilon_H\ge\beta$$

**Dimension conditions.** $\varepsilon^2\ge2\beta\Delta,\quad\varepsilon_H\ge\beta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B3 - First-order stationarity lower bound under Lipschitz Hessians

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\Delta\sqrt\beta\,\beta_2^{1/4}\varepsilon^{-7/4}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.00245v2)

**Conditions.** $$\Theta_{\rm balanced},\quad d\ge d_{\rm hd}$$

**Dimension conditions.** $\Theta_{\rm balanced},\quad d\ge d_{\rm hd}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2610.00245v2) theorem: Theorem 3.1, PDF p.4; 2026-10-19 v2

### B4 - Cubic regularization with a finite-difference Hessian

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
Cd(1+\Delta\sqrt{\beta_2}/\varepsilon^{3/2})
$$

**Conditions.** $$\varepsilon_H=\sqrt{\beta_2\varepsilon},\quad\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$$

**Dimension conditions.** $\varepsilon_H=\sqrt{\beta_2\varepsilon},\quad\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A2

### B5 - Hidden direction of negative curvature

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
d-1
$$

**Conditions.** $$d\ge2,\quad\varepsilon_H<c\min\{\beta,\beta_2^{2/3}\Delta^{1/3}\}$$

**Dimension conditions.** $d\ge2,\quad\varepsilon_H<c\min\{\beta,\beta_2^{2/3}\Delta^{1/3}\}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A2

### B6 - One-dimensional stationarity hard instances with Lipschitz Hessians

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\varepsilon^{-3/2}
$$

**Sources.** [2](https://arxiv.org/abs/2610.16295)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad\varepsilon_H=\sqrt\varepsilon,\quad\varepsilon\le c$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad\varepsilon_H=\sqrt\varepsilon,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/abs/2610.16295) theorem: Theorem 4.1 with $s=2$: one-dimensional gradient-only lower bound; second-order stationarity implies first-order stationarity

### B7 - Two-dimensional deterministic lower bound for a strong local oracle

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\varepsilon^{-1}
$$

**Sources.** [3](https://proceedings.mlr.press/v235/kontogiannis24a.html)

**Conditions.** $$d=2,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon_H=\sqrt\varepsilon,\quad\varepsilon\le c$$

**Dimension conditions.** $d=2,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon_H=\sqrt\varepsilon,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://proceedings.mlr.press/v235/kontogiannis24a.html) theorem: Corollary 2; Definition 1; Appendix F, PDF p.33

### B8 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $$\varepsilon^2\ge2\beta\Delta,\quad\varepsilon_H\ge\beta$$

**Dimension conditions.** $\varepsilon^2\ge2\beta\Delta,\quad\varepsilon_H\ge\beta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B9 - Nonnegative resource budgets

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $$\varepsilon^2\ge2\beta\Delta,\quad\varepsilon_H\ge\beta$$

**Dimension conditions.** $\varepsilon^2\ge2\beta\Delta,\quad\varepsilon_H\ge\beta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B10 - Accelerated gradient method with random perturbations

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Randomized witness

$$
C\Delta\sqrt\beta\,\beta_2^{1/4}\varepsilon^{-7/4}\Lambda_{\rm prob}^6
$$

**Sources.** [4](https://jmlr.org/papers/volume24/22-0522/22-0522.pdf)

**Conditions.** $$\varepsilon_H=\sqrt{\beta_2\varepsilon},\quad\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$$

**Dimension conditions.** $\varepsilon_H=\sqrt{\beta_2\varepsilon},\quad\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region.

**Source location.** [4](https://jmlr.org/papers/volume24/22-0522/22-0522.pdf) theorem: Theorem 5, PDF p. 9; retain the source logarithmic scale raised to the sixth power and the tolerance $1.011\sqrt{\beta_2\varepsilon}$

### B11 - First-order stationarity lower bound under Lipschitz Hessians

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\Delta\sqrt\beta\,\beta_2^{1/4}\varepsilon^{-7/4}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.00245v2)

**Conditions.** $$\Theta_{\rm balanced},\quad d\ge d_{\rm hd}$$

**Dimension conditions.** $\Theta_{\rm balanced},\quad d\ge d_{\rm hd}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2610.00245v2) theorem: Theorem 3.1, PDF p.4; 2026-10-19 v2

### B12 - Cubic regularization with a finite-difference Hessian

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
Cd(1+\Delta\sqrt{\beta_2}/\varepsilon^{3/2})
$$

**Conditions.** $$\varepsilon_H=\sqrt{\beta_2\varepsilon},\quad\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$$

**Dimension conditions.** $\varepsilon_H=\sqrt{\beta_2\varepsilon},\quad\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A2

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

### A2 - Second-order stationarity from first-order information

**Scope.** Gradient-only upper access; value-gradient lower access; global gradient and Hessian Lipschitz constants.

**Algorithm scope.** Deterministic upper witness and deterministic dimension lower bound.

For the deterministic dimension lower bound, use
$$
f_v(x)=-A(1-\cos(b\langle v,x-x_0\rangle)),\qquad\|v\|=1,
$$
where $2A\le\Delta$, $Ab^2\le\beta$, and $Ab^3\le\beta_2$. On the zero transcript of an algorithm with $T\le d-2$, choose $v$ orthogonal to all query displacements and the final output displacement. Every observed value and gradient is zero, but the output Hessian has eigenvalue $-Ab^2$. The curvature magnitude can be a constant multiple of $\min\{\beta,\beta_2^{2/3}\Delta^{1/3}\}$. Below that tolerance, $d-1$ calls are necessary. Choosing $v$ from the deterministic transcript does not establish an arbitrary-randomized lower bound.

For the gradient-only upper bound, assume $\beta_2>0$ and balanced tolerance $\epsilon_H=\sqrt{\beta_2\epsilon}$. Use $d+1$ gradients and coordinate finite differences, followed by symmetrization, to obtain
$\|B-\nabla^2f(x)\|_{\rm op}\le\eta=c\sqrt{\beta_2\epsilon}$.
A step $c\eta/(\beta_2d)$ suffices. Set $H_+=B+\eta I$ and minimize the known model
$$
m(s)=\langle\nabla f(x),s\rangle+\langle s,H_+s\rangle/2
+\beta_2\|s\|^3/6.
$$
Its global minimizer obeys the stationarity equation and
$H_++(\beta_2\|s\|/2)I\succeq0$.
Taylor bounds give
$$
f(x+s)\le f(x)-\beta_2\|s\|^3/12,\qquad
\|\nabla f(x+s)\|\le2\eta\|s\|+\beta_2\|s\|^2,
$$
$$
\lambda_{\min}(\nabla^2f(x+s))\ge-2\eta-\tfrac32\beta_2\|s\|.
$$
A step norm at most $c\sqrt{\epsilon/\beta_2}$ certifies both tolerances. Otherwise the decrease is at least $c\epsilon^{3/2}/\sqrt{\beta_2}$. The total is $O(d[1+\Delta\sqrt{\beta_2}/\epsilon^{3/2}])$ gradient calls. All reconstruction calls are charged; solving the known cubic model is internal computation.

**Limits of the argument.** The linear dimension obstruction does not cover arbitrary randomized algorithms. The upper formula uses the balanced tolerance window.

## References

[1] Haihan Zhang; Wendao Wu; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Lower Bounds for Randomized First-Order Methods in Hessian-Lipschitz Nonconvex Optimization. 2026-10-19; preprintv2.

https://arxiv.org/pdf/2610.00245v2

[2] Huanjian Zhou; Taiji Suzuki. On the Complexity of Finding Stationary Points of p-th Order Hölder Smooth Functions in One Dimension. 2026-10-12; preprintv1.

https://arxiv.org/abs/2610.16295

[3] Andreas Kontogiannis; Vasilis Pollatos; Sotiris Kanellopoulos; Panayotis Mertikopoulos; Aris Pagourtzis; Ioannis Panageas. The Computational Complexity of Finding Second-Order Stationary Points. 2024; ICML, PMLR 235:25191–25225.

https://proceedings.mlr.press/v235/kontogiannis24a.html

[4] Huan Li; Zhouchen Lin. Restarted Nonconvex Accelerated Gradient Descent: No More Polylogarithmic Factor in the O(epsilon^(-7/4)) Complexity. 2023.

https://jmlr.org/papers/volume24/22-0522/22-0522.pdf
