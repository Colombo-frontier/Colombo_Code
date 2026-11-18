# Convex optimization with a DGN inexact first-order oracle: DGN inexact model pair

**Setting ID.** `SO_FO_I01_DGN`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present; Infinite complexity

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball

**ORACLE tags.** access order: First-order interface; feedback quality: Inexact; interface family: Inexact model pair; operation: Inexact model pair; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}f(x)$$

### Admissible model

The public feasible set is $Q=RB_2^d$. An instance comprises an unknown closed convex function $f:Q\to\mathbb R$ and a legal response rule. The function admits a $(\beta,\varepsilon_{\rm orc})$ DGN quadratic model. Differentiability is not required; $\beta$ is a model coefficient, not an established Lipschitz constant of the true gradient.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

An instance includes the objective and a response rule satisfying the oracle's quadratic model inequality. The budget $\varepsilon_{\rm orc}$ is an absolute model error, not an unbiased noise variance.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad R>0,\quad \varepsilon>0,\quad \varepsilon_{\rm orc}\ge0$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon$.

Public upper bounds: $\beta,\ R,\ \varepsilon_{\rm orc}$.

The unknown object is the objective $f$.

Query points lie in $Q$; the response is a DGN inexact-model pair:

$$(v_x,g_x):0\le f(y)-v_x-\langle g_x,y-x\rangle\le\tfrac\beta2\|y-x\|^2+\varepsilon_{\rm orc}\quad\forall y\in Q$$

All responses must be consistent with one fixed objective. Subject to the displayed model inequalities, the oracle may choose its response adaptively from the history.

Exact Euclidean projection onto the public ball is an allowed auxiliary operation.

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$f(\widehat{x})-\min_Q f$$

$f^\star=\inf_{x\in Q}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

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

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f$: Unknown objective, with domain and structure specified by the model

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in Q}f(x)$$

$Q$: Feasible set of the task

$$Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$v_x,g_x$: The scalar model value and vector slope returned by the DGN interface; they need not equal the true function value and gradient **Domain:** $v_x\in\mathbb{R},\ g_x\in\mathbb{R}^d$.

$d$: Dimension; a public positive integer **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Curvature coefficient in the DGN quadratic upper model; it does not assert smoothness of the true gradient **Domain:** $\beta>0$.

$R$: Radius of the public feasible ball **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$\varepsilon_{\rm orc}$: DGN model error that the algorithm cannot request to reduce **Domain:** $\varepsilon_{\rm orc}\ge0$.

$c$: Sufficiently small absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $0<c<1$.

$C$: Sufficiently large absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $C>1$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

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

### R1 - Exact-interface slice

**Region.** $\varepsilon_{\rm orc}=0,\quad d\ge C\max\{1,\beta R^2/\varepsilon\}$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B2, B3, B7, B8

$$
c(1+\sqrt{\beta R^2/\varepsilon})
$$

**Upper bound.** B1, B6

$$
C(1+\sqrt{\beta R^2/\varepsilon})
$$

**Gap or comparison.** $C/c$

### R2 - High-dimensional window with positive model error

**Region.** $\Theta_{\rm hd},\quad\varepsilon_{\rm orc}>0$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B2, B3, B4, B7, B8, B9

$$
c\max\{1,\sqrt{\beta R^2/\varepsilon},\beta\varepsilon_{\rm orc}R^2/\varepsilon^2\}
$$

**Upper bound.** B1, B6

$$
C(1+\sqrt{\beta R^2/\varepsilon}+\beta\varepsilon_{\rm orc}R^2/\varepsilon^2)
$$

**Gap or comparison.** $3C/c$

### R3 - Below the nonidentifiability floor

**Region.** $0<\varepsilon<\varepsilon_{\rm orc}/2$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Infinite complexity

**Lower bound.** B5

$$
\infty
$$

### R4 - Certifiable accuracy regime

**Region.** $\varepsilon\ge C\varepsilon_{\rm orc}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Other quantified gap

**Lower bound.** B2

$$
c
$$

**Upper bound.** B1

$$
C(1+\sqrt{\beta R^2/\varepsilon}+\beta\varepsilon_{\rm orc}R^2/\varepsilon^2)
$$

**Gap or comparison.** $C(1+\sqrt{\beta R^2/\varepsilon}+\beta\varepsilon_{\rm orc}R^2/\varepsilon^2)$

### R5 - Below the nonidentifiability floor

**Region.** $0<\varepsilon<\varepsilon_{\rm orc}/2$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Infinite complexity

**Lower bound.** B10

$$
\infty
$$

### R6 - Certifiable accuracy regime

**Region.** $\varepsilon\ge C\varepsilon_{\rm orc}$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Other quantified gap

**Lower bound.** B7

$$
c
$$

**Upper bound.** B6

$$
C(1+\sqrt{\beta R^2/\varepsilon}+\beta\varepsilon_{\rm orc}R^2/\varepsilon^2)
$$

**Gap or comparison.** $C(1+\sqrt{\beta R^2/\varepsilon}+\beta\varepsilon_{\rm orc}R^2/\varepsilon^2)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Intermediate Gradient Method tuned to the target accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C(1+\sqrt{\beta R^2/\varepsilon}+\beta\varepsilon_{\rm orc}R^2/\varepsilon^2)
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2014/03/4279.pdf)

**Conditions.** $$\varepsilon\ge C\varepsilon_{\rm orc}$$

**Dimension conditions.** $\varepsilon\ge C\varepsilon_{\rm orc}$

**Oracle correspondence.** Applicable interfaces: DGN inexact model pair. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2014/03/4279.pdf) theorem: Definition 1, (1.3); §7.1–7.2, PDF pp.38–42

### B2 - Unbounded affine slopes rule out zero queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874) [3](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad R>0,\quad \varepsilon>0,\quad \varepsilon_{\rm orc}\ge0$$

**Dimension conditions.** $d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad R>0,\quad \varepsilon>0,\quad \varepsilon_{\rm orc}\ge0$

**Oracle correspondence.** Applicable interfaces: DGN inexact model pair. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B3 - Exact smooth value-gradient subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\sqrt{\beta R^2/\varepsilon}
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874) [3](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$d\ge C\max\{1,\beta R^2/\varepsilon\}$$

**Dimension conditions.** $d\ge C\max\{1,\beta R^2/\varepsilon\}$

**Oracle correspondence.** Applicable interfaces: DGN inexact model pair. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

**Source location.** [2](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1, the strongly convex quadratic reduction on PDF p. 3, and equation (7); explicit rescaling to the stated contract

### B4 - Exact Lipschitz value-subgradient subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\beta\varepsilon_{\rm orc}R^2/\varepsilon^2
$$

**Sources.** [3](https://arxiv.org/pdf/1407.5144) [2](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$\varepsilon_{\rm orc}>0,\quad d\ge C\max\{1,\beta\varepsilon_{\rm orc}R^2/\varepsilon^2\}$$

**Dimension conditions.** $\varepsilon_{\rm orc}>0,\quad d\ge C\max\{1,\beta\varepsilon_{\rm orc}R^2/\varepsilon^2\}$

**Oracle correspondence.** Applicable interfaces: DGN inexact model pair. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

**Source location.** [3](https://arxiv.org/pdf/1407.5144) theorem: Theorem V.1 for Euclidean value-subgradient access, with $L=\sqrt{\beta\varepsilon_{\rm orc}/2}$

### B5 - Two affine instances with identical oracle responses

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\infty
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874) [3](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$0<\varepsilon<\varepsilon_{\rm orc}/2$$

**Dimension conditions.** $0<\varepsilon<\varepsilon_{\rm orc}/2$

**Oracle correspondence.** Applicable interfaces: DGN inexact model pair. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B6 - Intermediate Gradient Method tuned to the target accuracy

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C(1+\sqrt{\beta R^2/\varepsilon}+\beta\varepsilon_{\rm orc}R^2/\varepsilon^2)
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2014/03/4279.pdf)

**Conditions.** $$\varepsilon\ge C\varepsilon_{\rm orc}$$

**Dimension conditions.** $\varepsilon\ge C\varepsilon_{\rm orc}$

**Oracle correspondence.** Applicable interfaces: DGN inexact model pair. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2014/03/4279.pdf) theorem: Definition 1, (1.3); §7.1–7.2, PDF pp.38–42

### B7 - Unbounded affine slopes rule out zero queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874) [3](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad R>0,\quad \varepsilon>0,\quad \varepsilon_{\rm orc}\ge0$$

**Dimension conditions.** $d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad R>0,\quad \varepsilon>0,\quad \varepsilon_{\rm orc}\ge0$

**Oracle correspondence.** Applicable interfaces: DGN inexact model pair. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B8 - Exact smooth value-gradient subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\sqrt{\beta R^2/\varepsilon}
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874) [3](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$d\ge C\max\{1,\beta R^2/\varepsilon\}$$

**Dimension conditions.** $d\ge C\max\{1,\beta R^2/\varepsilon\}$

**Oracle correspondence.** Applicable interfaces: DGN inexact model pair. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

**Source location.** [2](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1, the strongly convex quadratic reduction on PDF p. 3, and equation (7); explicit rescaling to the stated contract

### B9 - Exact Lipschitz value-subgradient subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\beta\varepsilon_{\rm orc}R^2/\varepsilon^2
$$

**Sources.** [3](https://arxiv.org/pdf/1407.5144) [2](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$\varepsilon_{\rm orc}>0,\quad d\ge C\max\{1,\beta\varepsilon_{\rm orc}R^2/\varepsilon^2\}$$

**Dimension conditions.** $\varepsilon_{\rm orc}>0,\quad d\ge C\max\{1,\beta\varepsilon_{\rm orc}R^2/\varepsilon^2\}$

**Oracle correspondence.** Applicable interfaces: DGN inexact model pair. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

**Source location.** [3](https://arxiv.org/pdf/1407.5144) theorem: Theorem V.1 for Euclidean value-subgradient access, with $L=\sqrt{\beta\varepsilon_{\rm orc}/2}$

### B10 - Two affine instances with identical oracle responses

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\infty
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874) [3](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$0<\varepsilon<\varepsilon_{\rm orc}/2$$

**Dimension conditions.** $0<\varepsilon<\varepsilon_{\rm orc}/2$

**Oracle correspondence.** Applicable interfaces: DGN inexact model pair. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

## 5. Local arguments

### A1 - DGN subclasses and the model-error floor

**Scope.** DGN value-model pairs on the public ball.

**Algorithm scope.** Randomized lower bounds and an all-budget indistinguishability impossibility.

Every exact smooth value-gradient oracle satisfies the DGN model. The cited randomized smooth hard subclass supplies the smooth lower term in its original dimension window.

For positive error allowance $\epsilon_{\rm orc}$, take
$L=\sqrt{\beta\epsilon_{\rm orc}/2}$.
An exact convex $L$-Lipschitz value-subgradient response obeys
$$
0\le f(y)-f(x)-\langle g_x,y-x\rangle
\le2L\|y-x\|
\le\beta\|y-x\|^2/2+\epsilon_{\rm orc}.
$$
It is therefore a legal DGN instance. The nonsmooth randomized lower theorem gives
$\Omega(\beta\epsilon_{\rm orc}R^2/\epsilon^2)$
with its own dimension requirement. The maximum of the two subclass terms is equivalent to their sum up to a factor of two. Arbitrarily large affine slopes exclude zero queries and supply the constant baseline.

For the impossibility floor, use
$$
f_\pm(x)=(\epsilon_{\rm orc}/2)(1\pm x_1/R)
\quad(x\in RB_2^d).
$$
Both functions lie in $[0,\epsilon_{\rm orc}]$, have minimum zero, and admit identical responses $(v_x,g_x)=(0,0)$ at every query. Every common randomized output satisfies
$\mathbb E[f_+(\widehat x)-f_+^\star]+\mathbb E[f_-(\widehat x)-f_-^\star]=\epsilon_{\rm orc}$.
Thus error below $\epsilon_{\rm orc}/2$ is impossible with any finite budget. This is impossibility in a nonempty model, distinct from infeasible parameters.

**Limits of the argument.** Each imported subclass retains its own sufficient dimension; model infeasibility is separate from the information-theoretic error floor.

**Sources.** [2](https://arxiv.org/pdf/2609.10874) [3](https://arxiv.org/pdf/1407.5144)

## References

[1] Olivier Devolder; François Glineur; Yurii Nesterov. Intermediate Gradient Methods for Smooth Convex Problems with Inexact Oracle. 2013; CORE Discussion Paper 2013/17; published online in 2014.

https://optimization-online.org/wp-content/uploads/2014/03/4279.pdf

[2] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 2026-09-09; preprintv1.

https://arxiv.org/pdf/2609.10874

[3] Gábor Braun; Cristóbal Guzmán; Sebastian Pokutta. Lower Bounds on the Oracle Complexity of Nonsmooth Convex Optimization via Information Theory. 2017; arXiv v3 2023.

https://arxiv.org/pdf/1407.5144
