# First-order stationarity for smooth nonconvex functions: Lipschitz gradient; exact function values and gradients

**Setting ID.** `SO_FO_N01_L1_FG`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Other quantified gap present

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; initialization: Initial gap; smoothness: Lipschitz gradient

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

$f\in C^1(\mathbb R^d)$ has a globally $\beta$-Lipschitz gradient, is bounded below, and satisfies $f(x_0)-\inf f\le\Delta$. Convexity is not assumed.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \Delta>0,\quad \varepsilon>0$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ \Delta$.

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

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$d$: Dimension; a public positive integer **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant **Domain:** $\beta>0$.

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

### R2 - One dimension, smoothness only

**Region.** $d=1,\quad\varepsilon^2\le c\beta\Delta$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q4

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B5, B16

$$
c\log(2+\sqrt{\beta\Delta}/\varepsilon)
$$

**Upper bound.** B4, B15

$$
C\log(2+\sqrt{\beta\Delta}/\varepsilon)
$$

**Gap or comparison.** $C/c$

### R3 - Normalized two-dimensional regime

**Region.** $d=2,\quad\beta=\Delta=1,\quad\varepsilon\le c$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B7

$$
c\varepsilon^{-1}
$$

**Upper bound.** B6

$$
C\varepsilon^{-1}
$$

**Gap or comparison.** $C/c$

### R4 - Sufficient dimension for deterministic value-gradient algorithms

**Region.** $\beta=\Delta=1,\quad\varepsilon\le c,\quad d\ge C\varepsilon^{-2}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B8

$$
c\varepsilon^{-2}
$$

**Upper bound.** B3

$$
C\varepsilon^{-2}
$$

**Gap or comparison.** $C/c$

### R5 - Normalized regime with $d\ge3$

**Region.** $d\ge3,\quad\beta=\Delta=1,\quad\varepsilon\le c$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Other quantified gap

**Lower bound.** B7, B10

$$
c\max\{\varepsilon^{-1},\min\{\varepsilon^{-2},d\}\}
$$

**Upper bound.** B3

$$
C\varepsilon^{-2}
$$

**Gap or comparison.** $\text{displayed upper / displayed lower}$

### R6 - Normalized two-dimensional regime

**Region.** $d=2,\quad\beta=\Delta=1,\quad\varepsilon\le c$

**Views.** Randomized / Expected loss

**Quantity.** Q5

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Other quantified gap

**Lower bound.** B16

$$
c\log(2/\varepsilon)
$$

**Upper bound.** B17

$$
C\varepsilon^{-1}
$$

**Gap or comparison.** $C/[\varepsilon\log(2/\varepsilon)]$

### R7 - Sufficient dimension for randomized value-gradient algorithms

**Region.** $\beta=\Delta=1,\quad\varepsilon\le c,\quad d\ge C\varepsilon^{-4}\log(2+1/\varepsilon)$

**Views.** Randomized / Expected loss

**Quantity.** Q4

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B18

$$
c\varepsilon^{-2}
$$

**Upper bound.** B14

$$
C\varepsilon^{-2}
$$

**Gap or comparison.** $C/c$

### R8 - Normalized regime with $d\ge3$

**Region.** $d\ge3,\quad\beta=\Delta=1,\quad\varepsilon\le c$

**Views.** Randomized / Expected loss

**Quantity.** Q4

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Other quantified gap

**Lower bound.** B16, B19

$$
c\max\{\log(2/\varepsilon),\min\{\varepsilon^{-2},\sqrt{d/\log(2+d)}\}\}
$$

**Upper bound.** B14

$$
C\varepsilon^{-2}
$$

**Gap or comparison.** $\text{displayed upper / displayed lower}$

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

### B4 - One-dimensional value-gradient bisection

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\log(2+\sqrt{\beta\Delta}/\varepsilon)
$$

**Sources.** [1](https://arxiv.org/pdf/2209.07513)

**Conditions.** $$d=1,\quad\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $d=1,\quad\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/2209.07513) theorem: Lemma 1 and Theorems 2–6. The native success probability is $1/2$; an explicit multiscale conversion yields the expected-error guarantee.

### B5 - One-dimensional arbitrary randomized FG lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\sqrt{\beta\Delta}/\varepsilon)
$$

**Sources.** [1](https://arxiv.org/pdf/2209.07513)

**Conditions.** $$\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2209.07513) theorem: Lemma 1 and Theorems 2–6. The native success probability is $1/2$; an explicit multiscale conversion yields the expected-error guarantee.

### B6 - Two-dimensional deterministic GFPT

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\varepsilon^{-1}
$$

**Sources.** [2](https://arxiv.org/pdf/2310.09157)

**Conditions.** $$d=2,\quad\beta=\Delta=1,\quad\varepsilon\le c$$

**Dimension conditions.** $d=2,\quad\beta=\Delta=1,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [2](https://arxiv.org/pdf/2310.09157) theorem: Theorems 3.2 and 4.1 and Appendix D; the task is two-dimensional and unconstrained

### B7 - Two-dimensional deterministic hard path

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\varepsilon^{-1}
$$

**Sources.** [2](https://arxiv.org/pdf/2310.09157)

**Conditions.** $$d\ge2,\quad\beta=\Delta=1,\quad\varepsilon\le c$$

**Dimension conditions.** $d\ge2,\quad\beta=\Delta=1,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2310.09157) theorem: Theorems 3.2 and 4.1 and Appendix D; the task is two-dimensional and unconstrained

### B8 - Rotated chain for arbitrary deterministic value-gradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\varepsilon^{-2}
$$

**Sources.** [3](https://arxiv.org/pdf/1710.11606)

**Conditions.** $$\beta=\Delta=1,\quad\varepsilon\le c,\quad d\ge C\varepsilon^{-2}$$

**Dimension conditions.** $\beta=\Delta=1,\quad\varepsilon\le c,\quad d\ge C\varepsilon^{-2}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/1710.11606) theorem: Theorems 1–2; Proposition 2; §5.3, PDF pp.19–20

### B9 - Local-information lower bound for arbitrary randomized value-gradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\varepsilon^{-2}
$$

**Sources.** [3](https://arxiv.org/pdf/1710.11606)

**Conditions.** $$\beta=\Delta=1,\quad\varepsilon\le c,\quad d\ge C\varepsilon^{-4}\log(2+1/\varepsilon)$$

**Dimension conditions.** $\beta=\Delta=1,\quad\varepsilon\le c,\quad d\ge C\varepsilon^{-4}\log(2+1/\varepsilon)$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/1710.11606) theorem: Theorems 1–2; Proposition 2; §5.3, PDF pp.19–20

### B10 - Truncated deterministic chain

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\min\{\varepsilon^{-2},d\}
$$

**Sources.** [3](https://arxiv.org/pdf/1710.11606)

**Conditions.** $$\beta=\Delta=1,\quad0<\varepsilon\le c$$

**Dimension conditions.** $\beta=\Delta=1,\quad0<\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/1710.11606) theorem: Theorems 1–2; Proposition 2; §5.3, PDF pp.19–20

### B11 - Truncated randomized value-gradient chain

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\varepsilon^{-2},\sqrt{d/\log(2+d)}\}
$$

**Sources.** [3](https://arxiv.org/pdf/1710.11606)

**Conditions.** $$\beta=\Delta=1,\quad0<\varepsilon\le c$$

**Dimension conditions.** $\beta=\Delta=1,\quad0<\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/1710.11606) theorem: Theorems 1–2; Proposition 2; §5.3, PDF pp.19–20

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

### B15 - One-dimensional value-gradient bisection

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\log(2+\sqrt{\beta\Delta}/\varepsilon)
$$

**Sources.** [1](https://arxiv.org/pdf/2209.07513)

**Conditions.** $$d=1,\quad\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $d=1,\quad\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/2209.07513) theorem: Lemma 1 and Theorems 2–6. The native success probability is $1/2$; an explicit multiscale conversion yields the expected-error guarantee.

### B16 - One-dimensional arbitrary randomized FG lower bound

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\sqrt{\beta\Delta}/\varepsilon)
$$

**Sources.** [1](https://arxiv.org/pdf/2209.07513)

**Conditions.** $$\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2209.07513) theorem: Lemma 1 and Theorems 2–6. The native success probability is $1/2$; an explicit multiscale conversion yields the expected-error guarantee.

### B17 - Two-dimensional deterministic GFPT

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\varepsilon^{-1}
$$

**Sources.** [2](https://arxiv.org/pdf/2310.09157)

**Conditions.** $$d=2,\quad\beta=\Delta=1,\quad\varepsilon\le c$$

**Dimension conditions.** $d=2,\quad\beta=\Delta=1,\quad\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [2](https://arxiv.org/pdf/2310.09157) theorem: Theorems 3.2 and 4.1 and Appendix D; the task is two-dimensional and unconstrained

### B18 - Local-information lower bound for arbitrary randomized value-gradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\varepsilon^{-2}
$$

**Sources.** [3](https://arxiv.org/pdf/1710.11606)

**Conditions.** $$\beta=\Delta=1,\quad\varepsilon\le c,\quad d\ge C\varepsilon^{-4}\log(2+1/\varepsilon)$$

**Dimension conditions.** $\beta=\Delta=1,\quad\varepsilon\le c,\quad d\ge C\varepsilon^{-4}\log(2+1/\varepsilon)$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/1710.11606) theorem: Theorems 1–2; Proposition 2; §5.3, PDF pp.19–20

### B19 - Truncated randomized value-gradient chain

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\varepsilon^{-2},\sqrt{d/\log(2+d)}\}
$$

**Sources.** [3](https://arxiv.org/pdf/1710.11606)

**Conditions.** $$\beta=\Delta=1,\quad0<\varepsilon\le c$$

**Dimension conditions.** $\beta=\Delta=1,\quad0<\varepsilon\le c$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/1710.11606) theorem: Theorems 1–2; Proposition 2; §5.3, PDF pp.19–20

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

[1] Sinho Chewi; Sébastien Bubeck; Adil Salim. On the complexity of finding stationary points of smooth functions in one dimension. 2023.

https://arxiv.org/pdf/2209.07513

[2] Alexandros Hollender; Manolis Zampetakis. The Computational Complexity of Finding Stationary Points in Non-Convex Optimization. 2025; COLT 2023.

https://arxiv.org/pdf/2310.09157

[3] Yair Carmon; John C. Duchi; Oliver Hinder; Aaron Sidford. Lower Bounds for Finding Stationary Points I. 2020; arXiv v3 2019.

https://arxiv.org/pdf/1710.11606
