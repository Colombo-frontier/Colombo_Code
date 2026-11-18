# Smooth convex global minimization with an initial-distance bound: exact function values and gradients

**Setting ID.** `SO_FO_C03_FG`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present

**Gap classes present.** Other quantified gap; Logarithmic gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz gradient

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Fg; operation: Value gradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

$f:\mathbb R^d\to\mathbb R$ is convex and $\beta$-smooth, with a global minimizer satisfying $\|x^\star-x_0\|_2\le R$. The radius $R$ localizes a minimizer; it does not restrict queries.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$R>0,\quad \beta>0,\quad d\in\mathbb{N}_{\ge1},\quad \varepsilon>0$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ R$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of exact function values and gradients:

$$(f(x),\nabla f(x))$$

All responses are consistent with one fixed function instance. Exact values and derivatives agree across repeated queries at the same point.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(f,x)=f(x)-f^\star$$

$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One declared full first-order response costs one call; its vector coordinates are not charged separately.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Deterministic / Pointwise guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\exists A\ \forall I,\mathcal{O}:\ \ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\exists A\ \forall I,\mathcal{O}:\ \mathbb{E}_A[\ell(I,\widehat{x})]\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f$: Unknown objective, with domain and structure specified by the model

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$x^\star$: A global minimizer whose existence is promised by the model; unique under strong convexity

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$d$: Dimension; a public positive integer whose dependence is tracked jointly **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient Lipschitz or smoothness constant **Domain:** $\beta>0$.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $0<c<1$.

$C$: Sufficiently large universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $C>1$.

$K_\varepsilon$: Accelerated query scale; neither a norm exponent nor an independent variable

$$K_\varepsilon=\sqrt{\frac{\beta\,{R}^{2}}{\varepsilon}}$$

$a$: Fix a positive $a$ independently of $d,\beta,R,\varepsilon$ to select a window away from the transition. Constants may depend on $a$. **Domain:** $a>0$.

$c_{a}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $a$. **Domain:** $c_{a}>0$.

$C_{a}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $a$. **Domain:** $C_{a}>0$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

$[a]_+$: Positive part of a real number

$$[a]_+=\max\{a,0\}$$

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Nontrivial function accuracy

**Region.** $0<\varepsilon\le c\beta R^2$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B3, B5, B6

$$
c\max\{\min\{d,\sqrt{\beta R^2/\varepsilon}\},\log(2+\beta R^2/\varepsilon),\frac d{\log(2+d)}[\log\frac{\beta R^2}{Cd^4\varepsilon}]_+\}
$$

**Upper bound.** B1, B2

$$
C\min\{\sqrt{\beta R^2/\varepsilon},d\log(2+\beta R^2/\varepsilon)\}
$$

**Gap or comparison.** $C\log(2+\beta R^2/\varepsilon)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: The accepted deterministic envelopes have at most a logarithmic gap throughout the nontrivial parameter domain, including the stated constant-factor optimal subregions. Ratio: $C\log(2+\beta R^2/\varepsilon)$

### R2 - Sufficiently high dimension for randomized algorithms

**Region.** $0<\varepsilon\le c\beta R^2,\quad d\ge C\beta R^2/\varepsilon$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** B4, B10

$$
c K_\varepsilon
$$

**Upper bound.** B1, B8

$$
C K_\varepsilon
$$

**Gap or comparison.** $C$

### R3 - Sufficiently high dimension for deterministic algorithms

**Region.** $0<\varepsilon\le c\beta R^2,\quad d\ge C\sqrt{\beta R^2/\varepsilon}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** B3

$$
c K_\varepsilon
$$

**Upper bound.** B1

$$
C K_\varepsilon
$$

**Gap or comparison.** $C$

### R4 - One-dimensional nontrivial-accuracy regime

**Region.** $d=1,\quad0<\varepsilon\le c\beta R^2$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** B5, B11

$$
c\log(2+\beta R^2/\varepsilon)
$$

**Upper bound.** B2, B9

$$
C\log(2+\beta R^2/\varepsilon)
$$

**Gap or comparison.** $C$

### R5 - Sufficient high-accuracy window for the deterministic bound

**Region.** $d\ge2,\quad0<\varepsilon\le c\beta R^2/d^{4+a},\quad a>0\text{ \text{fixed in advance}}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B6

$$
c_a\frac d{\log(2+d)}\log(2+\beta R^2/\varepsilon)
$$

**Upper bound.** B2

$$
C d\log(2+\beta R^2/\varepsilon)
$$

**Gap or comparison.** $C_a\log(2+d)$

### R6 - Zero-query regime

**Region.** $\varepsilon\ge\beta R^2/2$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B7, B12

$$
0
$$

### R7 - Nontrivial function accuracy

**Region.** $0<\varepsilon\le c\beta R^2$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Other quantified gap

**Lower bound.** B10, B11

$$
c\max\{\min\{\sqrt d,\sqrt{\beta R^2/\varepsilon}\},\log(2+\beta R^2/\varepsilon)\}
$$

**Upper bound.** B8, B9

$$
C\min\{\sqrt{\beta R^2/\varepsilon},d\log(2+\beta R^2/\varepsilon)\}
$$

**Gap or comparison.** $\frac{\min\{K_\varepsilon,d\log(2+K_\varepsilon^2)\}}{\max\{\min(\sqrt d,K_\varepsilon),\log(2+K_\varepsilon^2)\}}$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: The ratio is retained explicitly. Some joint parameter paths have a polynomial dimension gap; one common exponent is not assigned to the entire region. Ratio: $\frac{\min\{K_\varepsilon,d\log(2+K_\varepsilon^2)\}}{\max\{\min(\sqrt d,K_\varepsilon),\log(2+K_\varepsilon^2)\}}$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Accelerated gradient method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\sqrt{\beta R^2/\varepsilon}
$$

**Sources.** [1](https://arxiv.org/pdf/1405.4980)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1405.4980) theorem: Theorem 3.19, with the source notation $L$ replaced by $\beta$

### B2 - Centroid cutting planes and subgradient certificates

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C d\log(2+\beta R^2/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/2101.09740v2) [5](https://arxiv.org/pdf/2609.33360v2) [3](https://arxiv.org/pdf/2609.10874) [1](https://arxiv.org/pdf/1405.4980) [6](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [7](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2

### B3 - Deterministic resisting-oracle quadratic chain

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\min\{d,\sqrt{\beta R^2/\varepsilon}\}
$$

**Sources.** [2](https://arxiv.org/pdf/2101.09740v2)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2101.09740v2) theorem: Corollary 2; Theorem 2, d≥2T+1

### B4 - Reduction from randomized matrix-vector hard instances to first-order optimization

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,\sqrt{\beta R^2/\varepsilon}\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1, PDF pp.2–3; Eq. (7), p.7

### B5 - One-dimensional nested-interval hard instances

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\beta R^2/\varepsilon)
$$

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A3

### B6 - Fixed-dimensional deterministic information-complexity hard instances

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\frac d{\log(2+d)}\left[\log\frac{\beta R^2}{C d^4\varepsilon}\right]_+
$$

**Sources.** [4](https://www2.isye.gatech.edu/~nemirovs/LecEMCO.pdf)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [4](https://www2.isye.gatech.edu/~nemirovs/LecEMCO.pdf) theorem: Theorem 11.4.1, printed p. 179; conversion from relative error to absolute error under an initial-distance bound

### B7 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [2](https://arxiv.org/pdf/2101.09740v2) [5](https://arxiv.org/pdf/2609.33360v2) [3](https://arxiv.org/pdf/2609.10874) [1](https://arxiv.org/pdf/1405.4980) [6](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [7](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon\ge\beta R^2/2$$

**Dimension conditions.** $\varepsilon\ge\beta R^2/2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2

### B8 - Accelerated gradient method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\sqrt{\beta R^2/\varepsilon}
$$

**Sources.** [1](https://arxiv.org/pdf/1405.4980)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1405.4980) theorem: Theorem 3.19, with the source notation $L$ replaced by $\beta$

### B9 - Centroid cutting planes and subgradient certificates

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C d\log(2+\beta R^2/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/2101.09740v2) [5](https://arxiv.org/pdf/2609.33360v2) [3](https://arxiv.org/pdf/2609.10874) [1](https://arxiv.org/pdf/1405.4980) [6](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [7](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2

### B10 - Reduction from randomized matrix-vector hard instances to first-order optimization

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,\sqrt{\beta R^2/\varepsilon}\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1, PDF pp.2–3; Eq. (7), p.7

### B11 - One-dimensional nested-interval hard instances

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\beta R^2/\varepsilon)
$$

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A3

### B12 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [2](https://arxiv.org/pdf/2101.09740v2) [5](https://arxiv.org/pdf/2609.33360v2) [3](https://arxiv.org/pdf/2609.10874) [1](https://arxiv.org/pdf/1405.4980) [6](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [7](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon\ge\beta R^2/2$$

**Dimension conditions.** $\varepsilon\ge\beta R^2/2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2

## 5. Local arguments

### A1 - Smooth localization and gradient-norm conversion

**Scope.** Gradient access and a public ball localizing a global minimizer; public regularization when only initial gap is given.

**Algorithm scope.** Deterministic upper witnesses; imported lower theorems retain their own deterministic or randomized scopes.

If a global minimizer lies within distance $R$ of $x_0$, query on $B(x_0,R)$. Since $\nabla f(x^\star)=0$, gradients there have norm at most $2\beta R$. The centroid certificate gives $O(d\log(2+\beta R^2/\epsilon))$ gradient calls. Smoothness gives $f(x_0)-f^\star\le\beta R^2/2$, including the zero-query endpoint.

With global $\mu$-strong convexity and initial gap $\Delta$, use radius $\sqrt{2\Delta/\mu}$, obtaining $O(d\log(2+\kappa\Delta/\epsilon))$. At $\mu=\beta$, equality in strong monotonicity and Lipschitz continuity forces $\nabla f(x)-\nabla f(y)=\beta(x-y)$. One gradient identifies the minimizer of this known-curvature quadratic plus unknown affine term. Opposite translations exclude zero calls at nontrivial accuracy.

Under global Hölder smoothness in $\ell_q$, convert to Euclidean quantities
$\beta_E=\beta_\nu d^{(1+\nu)(1/q-1/2)_+}$ and
$R_E=Rd^{(1/2-1/p)_+}$. Gradients on the localization ball are at most $\beta_E(2R_E)^\nu$, giving
$C_\nu d\log(2+\beta_E R_E^{1+\nu}/\epsilon)$.
A boundary minimizer of an arbitrary constrained problem does not justify the zero-gradient premise. With two public norm-distance bounds, their intersection lies in the Euclidean ball of radius $R_{2,+}$, while the Euclidean ball of radius $R_{2,-}$ satisfies both promises. The former gives a certificate upper bound; embedding the one-dimensional hard family in the latter gives the logarithmic lower bound.

For gradient-norm accuracy, use $\|\nabla f(x)\|^2\le2\beta(f(x)-f^\star)$. Under initial distance, target gap $\epsilon^2/(2\beta)$. Under initial gap alone, instead set
$$
F_\lambda=f+\lambda\|x-x_0\|^2/2,\qquad\lambda=\epsilon^2/(32\Delta).
$$
Its minimizer lies within $8\Delta/\epsilon$. A certificate at gap $\epsilon^2/(128\beta)$ gives $\|\nabla F_\lambda(\widehat x)\|\le\epsilon/4$, while the public regularizer contributes at most $\epsilon/4$. Each regularized gradient costs one original gradient, and the budget is $O(d\log(2+\beta\Delta/\epsilon^2))$.

For lower transfers, strong convexity gives $f-f^\star\le\|\nabla f\|^2/(2\mu)$. Choose the hard subclass modulus proportional to $\epsilon/R$, or $\epsilon^2/\Delta$, for the two respective initializations. Gradient accuracy forces constant relative gap reduction. Apply the cited deterministic chain or randomized matrix-query theorem in its original dimension window; truncate only to constructions that fit. This preserves initialization, guarantee, and algorithm scope.

For an already strongly convex model, the gap threshold required for the lower transfer is $\epsilon^2/(2\mu)$, whereas the sufficient gap for the upper transfer is $\epsilon^2/(2\beta)$. Retain these different logarithm arguments rather than silently canceling their condition-number shift. For $1<\kappa\le4$, gradient descent and the nested one-dimensional construction yield the stated comparable near-unit denominators. At $\kappa=1$, the known-curvature quadratic is solved in one call.

For matching $\ell_p$ Hölder geometry, the descent model along a dual steepest-descent direction gives
$f(x)-f^\star\ge c_\nu\beta_\nu^{-1/\nu}\|\nabla f(x)\|_{p^\star}^{(1+\nu)/\nu}$.
Targeting gap $c_\nu\beta_\nu^{-1/\nu}\epsilon^{(1+\nu)/\nu}$ in the localization certificate therefore gives
$C_\nu d\log(2+\beta_\nu R^\nu/\epsilon)$.

**Limits of the argument.** An arbitrary constrained minimizer may be on the boundary and need not have zero gradient. Fixed-dimensional lower transfers retain theorem dimension windows.

**Sources.** [2](https://arxiv.org/pdf/2101.09740v2) [5](https://arxiv.org/pdf/2609.33360v2) [3](https://arxiv.org/pdf/2609.10874)

### A2 - Subgradient certificates and centroid cuts

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

**Sources.** [1](https://arxiv.org/pdf/1405.4980) [6](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [7](https://arxiv.org/pdf/2609.20701)

### A3 - A one-dimensional lower bound with exact values and gradients

**Scope.** Exact values and gradients; unbounded real-line queries, with higher-dimensional embeddings.

**Algorithm scope.** Lower bounds against arbitrary randomized adaptive algorithms, including unqueried output.

Fix $1<\kappa=\beta/\mu$. Choose a fixed smooth $\psi$, equal to $-x$ on $[-1/2,1/2]$ and zero outside $[-1,1]$, and let $C_\psi=\max\{1,\|\psi''\|_\infty\}$. Set
$$
\beta_0=(\beta+\mu)/2,\quad a={\kappa-1\over8C_\psi(\kappa+1)},\quad
\eta=a/4,\quad \rho_0={(1-\eta)\over a}\sqrt{\Delta/\beta}.
$$
For independent uniform signs $b_i$, define $u_0=0$,
$u_i=u_{i-1}+b_i a\rho_{i-1}$, $\rho_i=\eta\rho_{i-1}$, and
$$
f_b(x)=\beta_0x^2/2+
\beta_0\sum_{i=1}^N b_i a\rho_{i-1}^2
\psi((x-u_{i-1})/\rho_{i-1}).
$$
The two child intervals $I_i=[u_i-\rho_i,u_i+\rho_i]$ are disjoint and lie inside the central half of the parent. Second derivatives of successive bumps have disjoint shell supports. Thus $\mu\le f_b''\le\beta$, and $f_b''\ge7\beta/16$. Within $I_i$, the partial sum through level $i$ is a quadratic centered at $u_i$. The final minimizer is $u_N$, with $|u_N|\le\sqrt{\Delta/\beta}$ and initial gap at most $\Delta/2$.

A stronger oracle reveals the next bit when the query lies in the current unresolved interval, continuing only while it lies in the selected child. Unrevealed bumps vanish near the query, so the revealed prefix computes the exact value and derivative. Conditional on history, a fixed point belongs to at most one child; one query reveals at most $\sum_{j\ge1}2^{-(j-1)}=2$ new bits in expectation.

Treat the final output as one more such query. If $|\widehat x-u_N|<\rho_N$, all $N$ bits are revealed. Its probability is at most $2(T+1)/N$. Otherwise the loss is at least
$c\beta\rho_N^2=c'\Delta\eta^{2(N-1)}$.
Choose $N$ at the accuracy scale and use opposite translations to exclude zero calls. For expected error and constant-probability accuracy,
$$
T\ge c\left[1+{\log(\Delta/\epsilon)\over
\log(C\kappa/(\kappa-1))}\right].
$$
Queries may be arbitrary, randomized, adaptive, and unbounded.

Fixing $\kappa=2$, $\Delta=c\beta R^2$, gives the initial-distance logarithmic bound. The gradient version uses
$|f_b'(x)|\ge(7\beta/16)|x-u_N|$.
Add a public quadratic to embed in higher dimension. For composite minimization, apply the construction on total curvature interval $[\mu,\mu+\beta]$, with public $h(x)=\mu x^2/2$; the unknown remainder is convex and $\beta$-smooth, and every proximal response for $h$ is independent of the hidden bits.

**Limits of the argument.** Curvature, initialization, and nontrivial-accuracy restrictions remain explicit; the composite transfer lower-bounds unknown-gradient calls.

## References

[1] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015.

https://arxiv.org/pdf/1405.4980

[2] Yoel Drori; Adrien Taylor. On the oracle complexity of smooth strongly convex minimization. 2021; arXiv:2101.09740v2.

https://arxiv.org/pdf/2101.09740v2

[3] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 2026-09-09; preprintv1.

https://arxiv.org/pdf/2609.10874

[4] Arkadi Nemirovski. Information-Based Complexity of Convex Programming. Lecture notes, Fall 1994/95.

https://www2.isye.gatech.edu/~nemirovs/LecEMCO.pdf

[5] Yoel Drori. Exact oracle complexity for function-value suboptimality under weighted initial conditions. 2026-10-16; preprintv2.

https://arxiv.org/pdf/2609.33360v2

[6] Arkadi Nemirovski; Shmuel Onn; Uriel G. Rothblum. Accuracy Certificates for Computational Problems with Convex Structure. 2010.

https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf

[7] David Martínez-Rubio; Cristóbal Guzmán. Stable Movement for Nondual Lipschitz Convex Optimization: Efficiency and Nearly Optimal Oracle Rates. 2026-09-17; preprintv1.

https://arxiv.org/pdf/2609.20701
