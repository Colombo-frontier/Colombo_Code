# Relatively smooth convex minimization: primal first-order and mirror-map access

**Setting ID.** `SO_FO_C08`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Other quantified gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Convex body; smoothness: Relative smoothness

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Bregman first order and mirror; interface family: Mixed; operation: Values gradients and mirror; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; adaptivity: Explicit restriction; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}f(x)$$

### Admissible model

The unknown pair $(f,h)$ consists of a proper closed kernel $h$ that is strictly convex and differentiable in the interior, and a differentiable convex function $f$. The function $\beta_hh-f$ is convex, and $D_h(x^\star,x_0)\le R^2$. Every linearly perturbed kernel subproblem has a unique interior solution. The complete formula for $h$ is not additionally disclosed.

Feasible geometry: $Q=\operatorname{dom}h\subseteq\mathbb{R}^d$.

Admissible parameter domain:

$$R>0,\quad \beta_h>0,\quad d\in\mathbb{N}_{\ge1},\quad \varepsilon>0$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta_h,\ R$.

The unknown object is the function pair $(f,h)$.

Query points lie in $Q$; feedback consists of primal first-order information and mirror-map access:

$$(f(x),\nabla f(x),h(x),\nabla h(x));\quad\nabla h^*(y)=\arg\min_{z\in Q}\{h(z)-\langle y,z\rangle\}$$

All responses are consistent with one fixed function instance. Exact values and derivatives agree across repeated queries at the same point.

The mirror-map interface accepts a dual vector $y\in\mathbb R^d$ and returns $\nabla h^*(y)$.

Primal first-order queries lie in $\operatorname{int}(\operatorname{dom}h)$; mirror queries lie in the dual space. The initial primal query is also charged.

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(f,x)=f(x)-f^\star$$

$f^\star=\inf_{x\in Q}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

Retain the primal and mirror query counts $(N_{\rm primal},N_{\rm mirror})$. Each call increments its own coordinate by one. The scalar cost is $T=N_{\rm primal}+N_{\rm mirror}$.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Deterministic / Linear span / Pointwise guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

Let $X_t$ and $Y_t$ denote the primal and dual histories. Initially $X_0=\{x_0\}$; after the primal response at $x_0$, add $\nabla f(x_0)$ and $\nabla h(x_0)$ to $Y_0$. Primal queries lie in $\operatorname{span}X_{t-1}\cap\operatorname{dom}\nabla h$ and their responses enlarge only $Y_t$. Mirror queries lie in $\operatorname{span}Y_{t-1}$ and their responses enlarge only $X_t$. The output lies in $\operatorname{span}X_T\cap Q$.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\exists A\ \forall I,\mathcal{O}:\ \ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

**Output qualification.** The output must also satisfy the support, atomic-hull, or historical-span restriction of its algorithm view. An unqueried output remains subject to these restrictions.

#### Randomized / Linear span / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

Let $X_t$ and $Y_t$ denote the primal and dual histories. Initially $X_0=\{x_0\}$; after the primal response at $x_0$, add $\nabla f(x_0)$ and $\nabla h(x_0)$ to $Y_0$. Primal queries lie in $\operatorname{span}X_{t-1}\cap\operatorname{dom}\nabla h$ and their responses enlarge only $Y_t$. Mirror queries lie in $\operatorname{span}Y_{t-1}$ and their responses enlarge only $X_t$. The output lies in $\operatorname{span}X_T\cap Q$.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\exists A\ \forall I,\mathcal{O}:\ \mathbb{E}_A[\ell(I,\widehat{x})]\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

**Output qualification.** The output must also satisfy the support, atomic-hull, or historical-span restriction of its algorithm view. An unqueried output remains subject to these restrictions.

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

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f$: Unknown objective, with domain and structure specified by the model

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$\nabla h$: Full gradient of the differentiable kernel or the unknown Hölder-smooth term

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in Q}f(x)$$

$x^\star$: A global minimizer whose existence is promised by the model; unique under strong convexity

$Q$: Feasible set of the task

$$Q=\operatorname{dom}h\subseteq\mathbb{R}^d$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$h,h^*$: Kernel function and its Fenchel conjugate

$$h^*(y)=\sup_{x\in Q}\{\langle y,x\rangle-h(x)\}$$

$D_h$: Bregman divergence induced by the kernel

$$D_h(u,v)=h(u)-h(v)-\langle\nabla h(v),u-v\rangle$$

$X_t,Y_t$: Primal history of points and dual history of vectors; their update rules are specified by the algorithm view **Domain:** $t\in\mathbb{N}_{\ge0}$.

$\operatorname{span}$: Linear space of all finite real linear combinations of vectors in the set

$d$: Dimension; a public positive integer whose dependence is tracked jointly **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta_h$: Public upper bound on the relative smoothness constant **Domain:** $\beta_h>0$.

$R$: Public upper bound on the square root of the initial Bregman divergence **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $0<c<1$.

$C$: Sufficiently large universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $C>1$.

$T$: Total budget for the declared resource projection; for a risk curve, the budget is fixed in advance **Domain:** $T\in\mathbb{N}_{\ge0}$.

$N_{\mathrm{primal}},N_{\mathrm{mirror}}$: Numbers of primal first-order and mirror-map calls **Domain:** All are nonnegative integers.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic / Linear span / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primal first-order query and each mirror-map query costs one call; one NoLips iteration uses one of each.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Linear span / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primal first-order query and each mirror-map query costs one call; one NoLips iteration uses one of each.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primal first-order query and each mirror-map query costs one call; one NoLips iteration uses one of each.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primal first-order query and each mirror-map query costs one call; one NoLips iteration uses one of each.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Nontrivial accuracy under relative smoothness

**Region.** $0<\varepsilon\le c\beta_hR^2$

**Views.** Deterministic / Linear span / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primal first-order query and each mirror-map query costs one call; one NoLips iteration uses one of each.

**Status.** Other quantified gap

**Lower bound.** B2, B3, B4

$$
c\max\{\min(d,\beta_hR^2/\varepsilon),\log(2+\beta_hR^2/\varepsilon)\}
$$

**Upper bound.** B1

$$
C\beta_hR^2/\varepsilon
$$

**Gap or comparison.** $\frac{\beta_hR^2/\varepsilon}{\max\{\min(d,\beta_hR^2/\varepsilon),\log(2+\beta_hR^2/\varepsilon)\}}$

### R2 - Sufficiently high dimension for the span-restricted class

**Region.** $d\ge C\beta_hR^2/\varepsilon,\quad\varepsilon\le c\beta_hR^2$

**Views.** Deterministic / Linear span / Pointwise guarantee; Randomized / Linear span / Expected loss

**Quantity.** Q1; Q2

**Resource.** Each primal first-order query and each mirror-map query costs one call; one NoLips iteration uses one of each.

**Status.** Optimal

**Lower bound.** B2, B6

$$
c\beta_hR^2/\varepsilon
$$

**Upper bound.** B1, B5

$$
C\beta_hR^2/\varepsilon
$$

**Gap or comparison.** $C$

### R3 - Nontrivial accuracy under relative smoothness

**Region.** $0<\varepsilon\le c\beta_hR^2$

**Views.** Randomized / Linear span / Expected loss

**Quantity.** Q2

**Resource.** Each primal first-order query and each mirror-map query costs one call; one NoLips iteration uses one of each.

**Status.** Other quantified gap

**Lower bound.** B6, B7, B8

$$
c\max\{\min(d,\beta_hR^2/\varepsilon),\log(2+\beta_hR^2/\varepsilon)\}
$$

**Upper bound.** B5

$$
C\beta_hR^2/\varepsilon
$$

**Gap or comparison.** $\frac{\beta_hR^2/\varepsilon}{\max\{\min(d,\beta_hR^2/\varepsilon),\log(2+\beta_hR^2/\varepsilon)\}}$

### R4 - Nontrivial accuracy under relative smoothness

**Region.** $0<\varepsilon\le c\beta_hR^2$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q3

**Resource.** Each primal first-order query and each mirror-map query costs one call; one NoLips iteration uses one of each.

**Status.** Other quantified gap

**Lower bound.** B10, B11

$$
c\max\{\min(\sqrt d,\sqrt{\beta_hR^2/\varepsilon}),\log(2+\beta_hR^2/\varepsilon)\}
$$

**Upper bound.** B9

$$
C\beta_hR^2/\varepsilon
$$

**Gap or comparison.** $\frac{\beta_hR^2/\varepsilon}{\max\{\min(\sqrt d,\sqrt{\beta_hR^2/\varepsilon}),\log(2+\beta_hR^2/\varepsilon)\}}$

### R5 - Sufficiently high dimension for the span-restricted class

**Region.** $d\ge C\beta_hR^2/\varepsilon,\quad\varepsilon\le c\beta_hR^2$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q3

**Resource.** Each primal first-order query and each mirror-map query costs one call; one NoLips iteration uses one of each.

**Status.** Polynomial gap

**Lower bound.** B10

$$
c\sqrt{\beta_hR^2/\varepsilon}
$$

**Upper bound.** B9

$$
C\beta_hR^2/\varepsilon
$$

**Gap or comparison.** $C\sqrt{\beta_hR^2/\varepsilon}$

### R6 - Nontrivial accuracy under relative smoothness

**Region.** $0<\varepsilon\le c\beta_hR^2$

**Views.** Randomized / Expected loss

**Quantity.** Q4

**Resource.** Each primal first-order query and each mirror-map query costs one call; one NoLips iteration uses one of each.

**Status.** Other quantified gap

**Lower bound.** B13, B14

$$
c\max\{\min(\sqrt d,\sqrt{\beta_hR^2/\varepsilon}),\log(2+\beta_hR^2/\varepsilon)\}
$$

**Upper bound.** B12

$$
C\beta_hR^2/\varepsilon
$$

**Gap or comparison.** $\frac{\beta_hR^2/\varepsilon}{\max\{\min(\sqrt d,\sqrt{\beta_hR^2/\varepsilon}),\log(2+\beta_hR^2/\varepsilon)\}}$

### R7 - Sufficiently high dimension for the span-restricted class

**Region.** $d\ge C\beta_hR^2/\varepsilon,\quad\varepsilon\le c\beta_hR^2$

**Views.** Randomized / Expected loss

**Quantity.** Q4

**Resource.** Each primal first-order query and each mirror-map query costs one call; one NoLips iteration uses one of each.

**Status.** Polynomial gap

**Lower bound.** B13

$$
c\sqrt{\beta_hR^2/\varepsilon}
$$

**Upper bound.** B12

$$
C\beta_hR^2/\varepsilon
$$

**Gap or comparison.** $C\sqrt{\beta_hR^2/\varepsilon}$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $$0<\varepsilon\le c\beta_hR^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta_hR^2$

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - NoLips / Bregman gradient method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Linear span / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\beta_hR^2/\varepsilon
$$

**Sources.** [1](https://arxiv.org/pdf/1911.08510v3)

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1911.08510v3) theorem: Theorem 1, PDF p. 7: native NoLips error bound $\beta_hD_h(x^\star,x_0)/T$

### B2 - Pathwise support expansion for a fixed Bregman hard pair

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Linear span / Pointwise guarantee

**Witness or lower-bound scope.** The stated restricted randomized class

$$
c\min\{d,\beta_hR^2/\varepsilon\}
$$

**Sources.** [1](https://arxiv.org/pdf/1911.08510v3)

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/1911.08510v3) theorem: Definition4, Proposition2, Theorem2, PDFpp.7,13; d≥2T+1

### B3 - Randomized quadratic hard instances in the public Euclidean-kernel subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Linear span / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,\sqrt{\beta_hR^2/\varepsilon}\}
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874)

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1 and the dimension-truncated smooth-convex lower bound, embedded in the subclass with a fixed public Euclidean kernel

### B4 - One-dimensional localization hard instances in the public Euclidean-kernel subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Linear span / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\beta_hR^2/\varepsilon)
$$

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B5 - NoLips / Bregman gradient method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Linear span / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\beta_hR^2/\varepsilon
$$

**Sources.** [1](https://arxiv.org/pdf/1911.08510v3)

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1911.08510v3) theorem: Theorem 1, PDF p. 7: native NoLips error bound $\beta_hD_h(x^\star,x_0)/T$

### B6 - Pathwise support expansion for a fixed Bregman hard pair

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Linear span / Expected loss

**Witness or lower-bound scope.** The stated restricted randomized class

$$
c\min\{d,\beta_hR^2/\varepsilon\}
$$

**Sources.** [1](https://arxiv.org/pdf/1911.08510v3)

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/1911.08510v3) theorem: Definition4, Proposition2, Theorem2, PDFpp.7,13; d≥2T+1

### B7 - Randomized quadratic hard instances in the public Euclidean-kernel subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Linear span / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,\sqrt{\beta_hR^2/\varepsilon}\}
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874)

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1 and the dimension-truncated smooth-convex lower bound, embedded in the subclass with a fixed public Euclidean kernel

### B8 - One-dimensional localization hard instances in the public Euclidean-kernel subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Linear span / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\beta_hR^2/\varepsilon)
$$

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B9 - NoLips / Bregman gradient method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\beta_hR^2/\varepsilon
$$

**Sources.** [1](https://arxiv.org/pdf/1911.08510v3)

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1911.08510v3) theorem: Theorem 1, PDF p. 7: native NoLips error bound $\beta_hD_h(x^\star,x_0)/T$

### B10 - Randomized quadratic hard instances in the public Euclidean-kernel subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,\sqrt{\beta_hR^2/\varepsilon}\}
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874)

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1 and the dimension-truncated smooth-convex lower bound, embedded in the subclass with a fixed public Euclidean kernel

### B11 - One-dimensional localization hard instances in the public Euclidean-kernel subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\beta_hR^2/\varepsilon)
$$

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B12 - NoLips / Bregman gradient method

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\beta_hR^2/\varepsilon
$$

**Sources.** [1](https://arxiv.org/pdf/1911.08510v3)

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1911.08510v3) theorem: Theorem 1, PDF p. 7: native NoLips error bound $\beta_hD_h(x^\star,x_0)/T$

### B13 - Randomized quadratic hard instances in the public Euclidean-kernel subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,\sqrt{\beta_hR^2/\varepsilon}\}
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874)

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1 and the dimension-truncated smooth-convex lower bound, embedded in the subclass with a fixed public Euclidean kernel

### B14 - One-dimensional localization hard instances in the public Euclidean-kernel subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\beta_hR^2/\varepsilon)
$$

**Oracle correspondence.** Applicable interfaces: primal first-order information and a mirror map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

## 5. Local arguments

### A1 - A one-dimensional lower bound with exact values and gradients

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

[1] Radu-Alexandru Dragomir; Adrien Taylor; Alexandre d’Aspremont; Jérôme Bolte. Optimal Complexity and Certification of Bregman First-Order Methods. 2021; arXiv1911.08510v3.

https://arxiv.org/pdf/1911.08510v3

[2] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 2026-09-09; preprintv1.

https://arxiv.org/pdf/2609.10874
