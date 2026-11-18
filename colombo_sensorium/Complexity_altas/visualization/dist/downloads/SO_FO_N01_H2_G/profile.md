# First-order stationarity for smooth nonconvex functions: Hessian Lipschitz; exact gradients

**Setting ID.** `SO_FO_N01_H2_G`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Other quantified gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; initialization: Initial gap; smoothness: Lipschitz gradient; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Gradient; operation: Gradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

$f\in C^2(\mathbb R^d)$ has a globally $\beta$-Lipschitz gradient and a globally $\beta_2$-Lipschitz Hessian. It is bounded below and satisfies $f(x_0)-\inf f\le\Delta$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Hessian regularity means $\|\nabla^2 f(u)-\nabla^2 f(v)\|_{\mathrm{op}}\le\beta_2\|u-v\|_2$ for all $u,v\in\mathbb R^d$.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0,\quad \beta_2>0$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ \beta_2,\ \Delta$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of exact gradients:

$$\nabla f(x)$$

All responses are consistent with one fixed function instance. Exact values and derivatives agree across repeated queries at the same point.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\|\nabla f(\widehat{x})\|_2$$

$\varepsilon$ is a gradient-norm tolerance. Expected norm and expected squared norm are different performance requirements.

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

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$\nabla^2f$: Hessian matrix of the objective **Domain:** $\nabla^2f(x)\in\mathbb{R}^{d\times d}$.

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\|\cdot\|_{\mathrm{op}}$: Matrix or multilinear operator norm induced by the stated vector norm

$d$: Dimension; a public positive integer **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant **Domain:** $\beta>0$.

$\beta_2$: Public upper bound on the Hessian Lipschitz constant; the oracle need not supply Hessians **Domain:** $\beta_2>0$.

$\Delta$: Public upper bound on the initial objective gap; the optimal value itself is unknown **Domain:** $\Delta>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$s$: Fixed finite regularity order; it restricts the model without increasing the oracle order **Domain:** $s\in\mathbb{N},\ s\ge3$.

$c$: Sufficiently small absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $0<c<1$.

$C$: Sufficiently large absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $C>1$.

$d_{\rm hd,H2}$: Sufficient dimension function for the randomized Hessian-Lipschitz lower bound; no constants enabling numerical evaluation are supplied **Domain:** $d_{\rm hd,H2}\in\mathbb{N}$.

$C_d$: Positive constant depending only on the subscripted parameters fixed in advance. It does not support uniform optimality when those parameters grow jointly. **Domain:** $C_d>0$.

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

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q5 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q6 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Coarse-accuracy initial-point regime

**Region.** $\varepsilon\ge\sqrt{2\beta\Delta}$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q4

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B2, B13

$$
0
$$

**Upper bound.** B1, B12

$$
0
$$

### R2 - Construction window for the randomized Hessian-Lipschitz lower bound

**Region.** $\Theta_{\rm H2,main},\quad d\ge d_{\rm hd,H2}$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q4

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B7, B18

$$
c\Delta\sqrt\beta\beta_2^{1/4}/\varepsilon^{7/4}
$$

**Upper bound.** B4, B6, B5, B3, B15, B17, B16, B14

$$
C\Delta\sqrt\beta\beta_2^{1/4}/\varepsilon^{7/4}
$$

**Gap or comparison.** $C/c$

**Comparison argument.** Intersect this comparison region with N01-parameters-H2. A lower bound for arbitrary randomized value-gradient algorithms is compared with a deterministic gradient-only upper bound. A sufficient dimension exists; an optimal dimension threshold is not claimed.

### R3 - Normalized higher-order regime in arbitrary fixed dimension

**Region.** $\beta=\beta_2=\Delta=1,\quad\varepsilon\le c;\quad d\text{ \text{held fixed in this comparison}}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B8

$$
c\varepsilon^{-3/2}
$$

**Upper bound.** B6, B3

$$
C_d\varepsilon^{-3/2}
$$

**Gap or comparison.** $C_d/c$

**Comparison argument.** Intersect this comparison region with N01-parameters-H2. The accuracy order matches at fixed dimension; the joint dependence on dimension remains unmatched.

### R4 - Normalized higher-order regime with $d=1$

**Region.** $d=1,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$

**Views.** Randomized / Expected loss

**Quantity.** Q5

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B20

$$
c\varepsilon^{-1}
$$

**Upper bound.** B19

$$
C\varepsilon^{-1}
$$

**Gap or comparison.** $C/c$

### R5 - Normalized higher-order regime with $d=2$

**Region.** $d=2,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$

**Views.** Randomized / Expected loss

**Quantity.** Q5

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Polynomial gap

**Lower bound.** B20

$$
c\varepsilon^{-1}
$$

**Upper bound.** B22, B17

$$
\widetilde{O}(\varepsilon^{-6/5})
$$

**Gap or comparison.** $\widetilde{O}(\varepsilon^{-1/5})$

**Comparison argument.** Intersect this comparison region with N01-parameters-H2. The accuracy exponent for two-dimensional randomized gradient-only algorithms with Lipschitz Hessians remains unmatched.

### R6 - Normalized higher-order regime with $d\ge3$

**Region.** $d\ge3,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$

**Views.** Randomized / Expected loss

**Quantity.** Q5

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Other quantified gap

**Lower bound.** B20

$$
c\varepsilon^{-1}
$$

**Upper bound.** B17

$$
C_d\varepsilon^{-3/2}
$$

**Gap or comparison.** $C_d\varepsilon^{-3/2}/(c\varepsilon^{-1})$

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

**Conditions.** $$\varepsilon\ge\sqrt{2\beta\Delta}$$

**Dimension conditions.** $\varepsilon\ge\sqrt{2\beta\Delta}$

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

**Conditions.** $$\varepsilon\ge\sqrt{2\beta\Delta}$$

**Dimension conditions.** $\varepsilon\ge\sqrt{2\beta\Delta}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B3 - Ordinary gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C(1+\beta\Delta/\varepsilon^2)
$$

**Conditions.** $$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0$$

**Dimension conditions.** $d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B4 - Restarted accelerated gradient method for nonconvex optimization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\Delta\sqrt\beta\,\beta_2^{1/4}/\varepsilon^{7/4}
$$

**Sources.** [3](https://jmlr.org/papers/volume24/22-0522/22-0522.pdf)

**Conditions.** $$\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$$

**Dimension conditions.** $\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [3](https://jmlr.org/papers/volume24/22-0522/22-0522.pdf) theorem: Algorithm 1; Theorem 1, PDF p.6

### B5 - Finite differences after balancing the gradient and Hessian tolerances

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
\widetilde{O}(d+d^{1/3}\Delta\sqrt{\beta_2}/\varepsilon^{3/2})
$$

**Sources.** [4](https://arxiv.org/pdf/2510.20786)

**Conditions.** $$\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$$

**Dimension conditions.** $\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [4](https://arxiv.org/pdf/2510.20786) theorem: Corollary 1 and the preceding finite-difference reduction, PDF p. 3

### B6 - Gradient reconstruction from fresh local quadratic-model observations

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
Cd(1+\Delta\sqrt{\beta_2}/\varepsilon^{3/2})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.02791)

**Conditions.** $$\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$$

**Dimension conditions.** $\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/2610.02791) theorem: Theorem 4.1 (PDF pp.19–20) ; Theorems 5.1–5.2; §3, §6

### B7 - Arbitrary randomized value-gradient algorithms under Lipschitz Hessians

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\Delta\sqrt\beta\,\beta_2^{1/4}/\varepsilon^{7/4}
$$

**Sources.** [5](https://arxiv.org/pdf/2610.00245v2)

**Conditions.** $$\Theta_{\rm H2,main},\quad d\ge d_{\rm hd,H2}$$

**Dimension conditions.** $\Theta_{\rm H2,main},\quad d\ge d_{\rm hd,H2}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound. Converting the source hard event to an expected-error statement retains the constant tolerance rescaling. Expected running costs additionally require a stopping-time truncation with its constant loss.

**Source location.** [5](https://arxiv.org/pdf/2610.00245v2) theorem: Theorem 3.1, PDF p. 4; v2 dated 19 October 2026; oracle and algorithm quantifiers from Section 2

### B8 - One dimension Hessian-Lipschitz D/$G$

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\varepsilon^{-3/2}
$$

**Sources.** [2](https://arxiv.org/abs/2610.16295)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/abs/2610.16295) theorem: Theorems 3.1, 4.1, 5.1, 6.1, 7.1; §8 Conclusion

### B9 - One-dimensional higher-order randomized $G$ lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\varepsilon^{-1}
$$

**Sources.** [2](https://arxiv.org/abs/2610.16295)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/abs/2610.16295) theorem: Theorems 3.1, 4.1, 5.1, 6.1, 7.1; §8 Conclusion

### B10 - One-dimensional higher-order randomized FG lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/abs/2610.16295)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/abs/2610.16295) theorem: Theorems 3.1, 4.1, 5.1, 6.1, 7.1; §8 Conclusion

### B11 - Two-dimensional deterministic lower bound with Lipschitz Hessians

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\varepsilon^{-1}
$$

**Sources.** [6](https://proceedings.mlr.press/v235/kontogiannis24a.html)

**Conditions.** $$d\ge2,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$$

**Dimension conditions.** $d\ge2,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [6](https://proceedings.mlr.press/v235/kontogiannis24a.html) theorem: Corollary 2 and Appendix F, PDF p. 33; the hard class has Lipschitz Hessians

### B12 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $$\varepsilon\ge\sqrt{2\beta\Delta}$$

**Dimension conditions.** $\varepsilon\ge\sqrt{2\beta\Delta}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B13 - Nonnegative resource budgets

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $$\varepsilon\ge\sqrt{2\beta\Delta}$$

**Dimension conditions.** $\varepsilon\ge\sqrt{2\beta\Delta}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B14 - Ordinary gradient descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C(1+\beta\Delta/\varepsilon^2)
$$

**Conditions.** $$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0$$

**Dimension conditions.** $d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B15 - Restarted accelerated gradient method for nonconvex optimization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\Delta\sqrt\beta\,\beta_2^{1/4}/\varepsilon^{7/4}
$$

**Sources.** [3](https://jmlr.org/papers/volume24/22-0522/22-0522.pdf)

**Conditions.** $$\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$$

**Dimension conditions.** $\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [3](https://jmlr.org/papers/volume24/22-0522/22-0522.pdf) theorem: Algorithm 1; Theorem 1, PDF p.6

### B16 - Finite differences after balancing the gradient and Hessian tolerances

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
\widetilde{O}(d+d^{1/3}\Delta\sqrt{\beta_2}/\varepsilon^{3/2})
$$

**Sources.** [4](https://arxiv.org/pdf/2510.20786)

**Conditions.** $$\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$$

**Dimension conditions.** $\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [4](https://arxiv.org/pdf/2510.20786) theorem: Corollary 1 and the preceding finite-difference reduction, PDF p. 3

### B17 - Gradient reconstruction from fresh local quadratic-model observations

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
Cd(1+\Delta\sqrt{\beta_2}/\varepsilon^{3/2})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.02791)

**Conditions.** $$\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$$

**Dimension conditions.** $\varepsilon\le c\beta^2/\beta_2,\quad\Delta\sqrt{\beta_2}/\varepsilon^{3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/2610.02791) theorem: Theorem 4.1 (PDF pp.19–20) ; Theorems 5.1–5.2; §3, §6

### B18 - Arbitrary randomized value-gradient algorithms under Lipschitz Hessians

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\Delta\sqrt\beta\,\beta_2^{1/4}/\varepsilon^{7/4}
$$

**Sources.** [5](https://arxiv.org/pdf/2610.00245v2)

**Conditions.** $$\Theta_{\rm H2,main},\quad d\ge d_{\rm hd,H2}$$

**Dimension conditions.** $\Theta_{\rm H2,main},\quad d\ge d_{\rm hd,H2}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound. Converting the source hard event to an expected-error statement retains the constant tolerance rescaling. Expected running costs additionally require a stopping-time truncation with its constant loss.

**Source location.** [5](https://arxiv.org/pdf/2610.00245v2) theorem: Theorem 3.1, PDF p. 4; v2 dated 19 October 2026; oracle and algorithm quantifiers from Section 2

### B19 - One-dimensional randomized higher-order gradient method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C\varepsilon^{-1}
$$

**Sources.** [2](https://arxiv.org/abs/2610.16295)

**Conditions.** $$d=1,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$$

**Dimension conditions.** $d=1,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [2](https://arxiv.org/abs/2610.16295) theorem: Theorems 3.1, 4.1, 5.1, 6.1, 7.1; §8 Conclusion

### B20 - One-dimensional higher-order randomized $G$ lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\varepsilon^{-1}
$$

**Sources.** [2](https://arxiv.org/abs/2610.16295)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/abs/2610.16295) theorem: Theorems 3.1, 4.1, 5.1, 6.1, 7.1; §8 Conclusion

### B21 - One-dimensional higher-order randomized FG lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/abs/2610.16295)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/abs/2610.16295) theorem: Theorems 3.1, 4.1, 5.1, 6.1, 7.1; §8 Conclusion

### B22 - Two-dimensional randomized trapping with Lipschitz Hessians

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}(\varepsilon^{-6/5})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.02791)

**Conditions.** $$d=2,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$$

**Dimension conditions.** $d=2,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://arxiv.org/pdf/2610.02791) theorem: Theorem 4.1 (PDF pp.19–20) ; Theorems 5.1–5.2; §3, §6

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

[1] Huanjian Zhou; Masashi Sugiyama; Taiji Suzuki. Finding Stationary Points under Higher-Order Smoothness: Trapping Algorithms and First-Order Lower Bounds. 2026-10-02; preprintv1.

https://arxiv.org/pdf/2610.02791

[2] Huanjian Zhou; Taiji Suzuki. On the Complexity of Finding Stationary Points of p-th Order Hölder Smooth Functions in One Dimension. 2026-10-12; preprintv1.

https://arxiv.org/abs/2610.16295

[3] Huan Li; Zhouchen Lin. Restarted Nonconvex Accelerated Gradient Descent: No More Polylogarithmic Factor in the O(epsilon^(-7/4)) Complexity. 2023.

https://jmlr.org/papers/volume24/22-0522/22-0522.pdf

[4] Deeksha Adil; Brian Bullins; Aaron Sidford; Chenyi Zhang. Balancing Gradient and Hessian Queries in Non-Convex Optimization. 2025; NeurIPS 2025.

https://arxiv.org/pdf/2510.20786

[5] Haihan Zhang; Wendao Wu; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Lower Bounds for Randomized First-Order Methods in Hessian-Lipschitz Nonconvex Optimization. 2026-10-19; preprintv2.

https://arxiv.org/pdf/2610.00245v2

[6] Andreas Kontogiannis; Vasilis Pollatos; Sotiris Kanellopoulos; Panayotis Mertikopoulos; Aris Pagourtzis; Ioannis Panageas. The Computational Complexity of Finding Second-Order Stationary Points. 2024; ICML, PMLR 235:25191–25225.

https://proceedings.mlr.press/v235/kontogiannis24a.html
