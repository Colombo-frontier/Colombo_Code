# First-order stationarity for smooth nonconvex functions: normalized higher-order smoothness; exact function values and gradients

**Setting ID.** `SO_FO_N01_HS_FG`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Logarithmic gap present

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; initialization: Initial gap; smoothness: Lipschitz gradient; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Value gradient; operation: Value gradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

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

Fix a finite integer $s\ge3$. The function $f\in C^s(\mathbb R^d)$ has derivatives of orders $j=1,\ldots,s$ with operator-norm Lipschitz constants at most $1$, and $f(x_0)-\inf f\le1$. This variant records only the normalized scale $\beta=\beta_2=\Delta=1$. Higher-order regularity does not increase the order of information supplied by the oracle.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0,\quad \beta_2>0,\quad s\in\mathbb{N}_{\ge3},\quad \beta=\beta_2=\Delta=1$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ s,\ x_0$.

Public upper bounds: $\beta,\ \beta_2,\ \Delta$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of exact function values and gradients:

$$(f(x),\nabla f(x))$$

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

$D^j f$: $j$th Fréchet derivative, viewed as a $j$-linear form **Domain:** $j\in\{1,\ldots,s\}$.

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

$C_s$: Positive constant depending only on the fixed regularity order $s$; it gives no control when $s$ grows with $d$ or $1/\varepsilon$. **Domain:** $C_s>0$.

$c_s$: Positive constant depending only on the subscripted parameters fixed in advance. It does not support uniform optimality when those parameters grow jointly. **Domain:** $c_s>0$.

$C_d$: Positive constant depending only on the subscripted parameters fixed in advance. It does not support uniform optimality when those parameters grow jointly. **Domain:** $C_d>0$.

$C_{d,s}$: Positive constant depending only on the subscripted parameters fixed in advance. It does not support uniform optimality when those parameters grow jointly. **Domain:** $C_{d,s}>0$.

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

### R1 - Normalized higher-order regime with $d=1$

**Region.** $d=1,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q4

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B6, B15

$$
c_s\log(2/\varepsilon)
$$

**Upper bound.** B5, B14

$$
C_s\log(2/\varepsilon)
$$

**Gap or comparison.** $C_s/c_s$

### R2 - Sufficient dimension for the higher-order lower bound

**Region.** $\beta=\beta_2=\Delta=1,\quad\varepsilon\le c,\quad d\ge C_s\varepsilon^{-47/3},\quad s\ge3\text{ \text{fixed}}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Logarithmic gap

**Lower bound.** B9

$$
c_s\varepsilon^{-5/3}
$$

**Upper bound.** B8, B4

$$
C_s\varepsilon^{-5/3}\log(2/\varepsilon)
$$

**Gap or comparison.** $C_s\log(2/\varepsilon)$

**Comparison argument.** Intersect this comparison region with N01-parameters-HS. In the high-dimensional value-gradient regime with fixed finite $s\ge3$, the principal accuracy order differs by only a logarithmic factor.

### R3 - Sufficient dimension for the higher-order lower bound

**Region.** $\beta=\beta_2=\Delta=1,\quad\varepsilon\le c,\quad d\ge C_s\varepsilon^{-47/3},\quad s\ge3\text{ \text{fixed}}$

**Views.** Randomized / Expected loss

**Quantity.** Q5

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Logarithmic gap

**Lower bound.** B18

$$
c_s\varepsilon^{-5/3}
$$

**Upper bound.** B17, B13

$$
C_s\varepsilon^{-5/3}\log(2/\varepsilon)
$$

**Gap or comparison.** $C_s\log(2/\varepsilon)$

**Comparison argument.** Intersect this comparison region with N01-parameters-HS. In the high-dimensional value-gradient regime with fixed finite $s\ge3$, the principal accuracy order differs by only a logarithmic factor.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Ordinary gradient descent

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

### B2 - Restarted accelerated gradient method for nonconvex optimization

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

### B3 - Reconstruction of an order-$s$ local model from gradient queries alone

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_s d^{s-1}(1+\varepsilon^{-(s+1)/s})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.02791)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/2610.02791) theorem: Theorem 4.1 (PDF pp.19–20) ; Theorems 5.1–5.2; §3, §6

### B4 - Improved dimension factor for the local model

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_s[d^{s-1}+d^{s-2+1/s}\varepsilon^{-(s+1)/s}]
$$

**Sources.** [1](https://arxiv.org/pdf/2610.02791)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/2610.02791) theorem: Theorem 4.1 (PDF pp.19–20) ; Theorems 5.1–5.2; §3, §6

### B5 - One-dimensional order-$s$ D/FG upper bound

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_s\log(2/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/abs/2610.16295)

**Conditions.** $$d=1,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$$

**Dimension conditions.** $d=1,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [2](https://arxiv.org/abs/2610.16295) theorem: Theorems 3.1, 4.1, 5.1, 6.1, 7.1; §8 Conclusion

### B6 - One-dimensional order-$s$ $R$/FG lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_s\log(2/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/abs/2610.16295)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/abs/2610.16295) theorem: Theorems 3.1, 4.1, 5.1, 6.1, 7.1; §8 Conclusion

### B7 - Fixed-dimensional value trapping under order-$s$ smoothness

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_{d,s}\varepsilon^{-(d-1)}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.02791)

**Conditions.** $$d\ge2,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$$

**Dimension conditions.** $d\ge2,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/2610.02791) theorem: Theorem 4.1 (PDF pp.19–20) ; Theorems 5.1–5.2; §3, §6

### B8 - Convex-until-proven-guilty with value-gradient access

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_s\varepsilon^{-5/3}\log(2/\varepsilon)
$$

**Sources.** [4](https://proceedings.mlr.press/v70/carmon17a/carmon17a.pdf)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [4](https://proceedings.mlr.press/v70/carmon17a/carmon17a.pdf) theorem: Theorem 2: dimension-independent value-gradient upper bound under third-order smoothness

### B9 - Higher-order lower bound against arbitrary randomized value-gradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_s\varepsilon^{-5/3}
$$

**Sources.** [5](https://arxiv.org/pdf/2610.17074v2)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad\varepsilon\le c,\quad d\ge C_s\varepsilon^{-47/3},\quad s\ge3\text{ \text{fixed}}$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad\varepsilon\le c,\quad d\ge C_s\varepsilon^{-47/3},\quad s\ge3\text{ \text{fixed}}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [5](https://arxiv.org/pdf/2610.17074v2) theorem: Theorem 2.1, PDF p. 3, and Appendix B; v2 dated 19 October 2026; sufficient dimension $C_s\varepsilon^{-47/3}$

### B10 - Ordinary gradient descent

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

### B11 - Restarted accelerated gradient method for nonconvex optimization

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

### B12 - Reconstruction of an order-$s$ local model from gradient queries alone

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_s d^{s-1}(1+\varepsilon^{-(s+1)/s})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.02791)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/2610.02791) theorem: Theorem 4.1 (PDF pp.19–20) ; Theorems 5.1–5.2; §3, §6

### B13 - Improved dimension factor for the local model

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_s[d^{s-1}+d^{s-2+1/s}\varepsilon^{-(s+1)/s}]
$$

**Sources.** [1](https://arxiv.org/pdf/2610.02791)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/2610.02791) theorem: Theorem 4.1 (PDF pp.19–20) ; Theorems 5.1–5.2; §3, §6

### B14 - One-dimensional order-$s$ D/FG upper bound

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_s\log(2/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/abs/2610.16295)

**Conditions.** $$d=1,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$$

**Dimension conditions.** $d=1,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [2](https://arxiv.org/abs/2610.16295) theorem: Theorems 3.1, 4.1, 5.1, 6.1, 7.1; §8 Conclusion

### B15 - One-dimensional order-$s$ $R$/FG lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_s\log(2/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/abs/2610.16295)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/abs/2610.16295) theorem: Theorems 3.1, 4.1, 5.1, 6.1, 7.1; §8 Conclusion

### B16 - Fixed-dimensional value trapping under order-$s$ smoothness

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_{d,s}\varepsilon^{-(d-1)}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.02791)

**Conditions.** $$d\ge2,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$$

**Dimension conditions.** $d\ge2,\quad\beta=\beta_2=\Delta=1,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/2610.02791) theorem: Theorem 4.1 (PDF pp.19–20) ; Theorems 5.1–5.2; §3, §6

### B17 - Convex-until-proven-guilty with value-gradient access

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_s\varepsilon^{-5/3}\log(2/\varepsilon)
$$

**Sources.** [4](https://proceedings.mlr.press/v70/carmon17a/carmon17a.pdf)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad0<\varepsilon\le c,\quad\varepsilon^{-3/2}\ge C$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [4](https://proceedings.mlr.press/v70/carmon17a/carmon17a.pdf) theorem: Theorem 2: dimension-independent value-gradient upper bound under third-order smoothness

### B18 - Higher-order lower bound against arbitrary randomized value-gradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_s\varepsilon^{-5/3}
$$

**Sources.** [5](https://arxiv.org/pdf/2610.17074v2)

**Conditions.** $$\beta=\beta_2=\Delta=1,\quad\varepsilon\le c,\quad d\ge C_s\varepsilon^{-47/3},\quad s\ge3\text{ \text{fixed}}$$

**Dimension conditions.** $\beta=\beta_2=\Delta=1,\quad\varepsilon\le c,\quad d\ge C_s\varepsilon^{-47/3},\quad s\ge3\text{ \text{fixed}}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [5](https://arxiv.org/pdf/2610.17074v2) theorem: Theorem 2.1, PDF p. 3, and Appendix B; v2 dated 19 October 2026; sufficient dimension $C_s\varepsilon^{-47/3}$

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

[4] Yair Carmon; John C. Duchi; Oliver Hinder; Aaron Sidford. “Convex Until Proven Guilty”: Dimension-Free Acceleration of Gradient Descent on Non-Convex Functions. 2017.

https://proceedings.mlr.press/v70/carmon17a/carmon17a.pdf

[5] Haihan Zhang; Wendao Wu; Fangqing Zhang; Chenheng Zhang; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Randomized First-Order Bounds for Higher-Order Smooth Nonconvex Optimization. 2026-10-19; preprintv2.

https://arxiv.org/pdf/2610.17074v2
