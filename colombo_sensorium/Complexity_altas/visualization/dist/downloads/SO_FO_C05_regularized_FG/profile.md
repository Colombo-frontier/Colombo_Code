# Global minimization of Hölder-smooth convex functions: a public quadratic regularizer; exact function values and gradients

**Setting ID.** `SO_FO_C05_regularized_FG`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Full space; smoothness: Holder smooth; structure: Public quadratic regularizer

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Fg; operation: Value gradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \mathbb{R}^d}F(x)$$

The complete objective is $F(x)=h(x)+\frac\mu2\|x-x_0\|_2^2$, with a public quadratic regularizer.

### Admissible model

$F(x)=h(x)+\mu\|x-x_0\|_2^2/2$, where $h$ is globally convex and has a $\nu$-Hölder continuous Euclidean gradient, with $0<\nu<1$. Assume $F(x_0)-F^\star\le\Delta$. Gradient access to the unknown function $h$ is equivalent to gradient access to $F$. The complete objective $F$ need not have a globally $\nu$-Hölder continuous gradient.

Admissible parameter domain:

$$\beta_\nu>0,\quad d\in\mathbb{N}_{\ge1},\quad \varepsilon>0,\quad \nu>0,\quad \nu\le1,\quad \Delta>0,\quad \mu>0,\quad \nu<1$$

### Oracle interface

Public numerical inputs: $d,\ \nu,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta_\nu,\ \Delta$.

Public lower bounds: $\mu$.

The unknown object is $h$.

Query points lie in $\mathbb{R}^d$; feedback consists of exact function values and gradients:

$$(h(x),\nabla h(x)),\qquad\nabla F(x)=\nabla h(x)+\mu(x-x_0)$$

All responses are consistent with one fixed function instance. Exact values and derivatives agree across repeated queries at the same point.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$F(\widehat{x})-F^\star$$

$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One declared full first-order response costs one call; its vector coordinates are not charged separately.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\exists A\ \forall I,\mathcal{O}:\ \mathbb{E}_A[\ell(I,\widehat{x})]\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$h,F$: Unknown Hölder-smooth term and regularized objective

$$F(x)=h(x)+\frac\mu2\|x-x_0\|_2^2$$

$\nabla F$: Full gradient of the differentiable complete objective with respect to the decision variable

$\nabla h$: Full gradient of the differentiable kernel or the unknown Hölder-smooth term

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$d$: Dimension; a public positive integer whose dependence is tracked jointly **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta_\nu$: Public upper bound on the gradient Hölder constant **Domain:** $\beta_\nu>0$.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$\nu$: Hölder exponent; public, with fixed or varying status stated in each comparison **Domain:** $0<\nu\le1$.

$\mu$: Lower bound on the strong-convexity modulus of the objective specified by the model **Domain:** $\mu>0$.

$\Delta$: Public upper bound on initial suboptimality, rather than its exact value **Domain:** $\Delta>0$.

$c$: Sufficiently small universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $0<c<1$.

$C$: Sufficiently large universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $C>1$.

$\beta$: When $\nu=1$, write $\beta=\beta_1$; this does not introduce another independent constant. **Domain:** $\beta=\beta_1\quad\text{when }\nu=1$.

$$\beta=\beta_\nu$$

$T$: Query budget used only in the exact finite-budget result; it is not another model scale. **Domain:** $T\in\mathbb{N}_{\ge1}$.

$B_\varepsilon$: Leading query scale for regularized Hölder-smooth minimization

$$B_\varepsilon={\frac{{\beta_\nu}^{2}}{({\mu}^{1+\nu})\,({\varepsilon}^{(1-\nu)})}}^{\frac{1}{1+3\,\nu}}$$

$c_{\nu}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $\nu$. **Domain:** $c_{\nu}>0$.

$C_{\nu}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $\nu$. **Domain:** $C_{\nu}>0$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Randomized lower-bound window with a public quadratic regularizer

**Region.** $\Delta\ge C_\nu\beta_\nu(\varepsilon/\mu)^{(1+\nu)/2},\quad d\ge C_\nu B_\varepsilon^4\log(2+B_\varepsilon),\quad0<\nu<1$

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Other quantified gap

**Lower bound.** B2

$$
c_\nu B_\varepsilon
$$

**Upper bound.** B1

$$
C_\nu[\log(2+\Delta/\varepsilon)+B_\varepsilon]
$$

**Gap or comparison.** $C_\nu[1+\log(2+\Delta/\varepsilon)/B_\varepsilon]$

### R2 - Power-law term dominates the initialization logarithm

**Region.** $\Theta_{\rm regularized,high},\quad B_\varepsilon\ge\log(2+\Delta/\varepsilon)$

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** B2

$$
c_\nu B_\varepsilon
$$

**Upper bound.** B1

$$
C_\nu B_\varepsilon
$$

**Gap or comparison.** $C_\nu$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Hölder acceleration and strong-convexity restart

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
C_\nu[\log(2+\Delta/\varepsilon)+B_\varepsilon]
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2010/12/2865.pdf) [2](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf)

**Conditions.** $$0<\nu<1,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $0<\nu<1,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2010/12/2865.pdf) theorem: Section 5.1, Theorem 5, and equation (42); the fixed schedule reads gradients only

### B2 - Regularization reduction for randomized Hölder hard instances

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\nu B_\varepsilon
$$

**Sources.** [2](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) [1](https://optimization-online.org/wp-content/uploads/2010/12/2865.pdf)

**Conditions.** $$\Delta\ge C_\nu\beta_\nu(\varepsilon/\mu)^{(1+\nu)/2},\quad d\ge C_\nu B_\varepsilon^4\log(2+B_\varepsilon),\quad0<\nu<1$$

**Dimension conditions.** $\Delta\ge C_\nu\beta_\nu(\varepsilon/\mu)^{(1+\nu)/2},\quad d\ge C_\nu B_\varepsilon^4\log(2+B_\varepsilon),\quad0<\nu<1$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

**Source location.** [2](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) theorem: Theorem 12 with $p=2$, $K=1$; full-space shielding in equation (3); the stated radius rescaling

## 5. Local arguments

### A1 - Public regularization of Hölder-smooth objectives

**Scope.** Global Hölder regularity of the unknown convex term; known quadratic regularization.

**Algorithm scope.** Deterministic upper witness and imported arbitrary-randomized lower construction.

Let $F=h+\mu\|x-x_0\|^2/2$, with unknown convex $h$ whose global gradient is $\nu$-Hölder, $0<\nu<1$. At error scale $u$, strong convexity provides radius $O(\sqrt{u/\mu})$. The cited Hölder accelerated bound reduces error by a constant factor in
$$
C_\nu[\beta_\nu^2/(\mu^{1+\nu}u^{1-\nu})]^{1/(1+3\nu)}
$$
calls, plus constant initialization. Restarting over geometric scales gives the final-stage power term plus $O(\log(2+\Delta/\epsilon))$. The public quadratic changes no oracle count.

For the randomized lower bound, scale the cited global Hölder hard family to minimizer radius $r=c\sqrt{\epsilon/\mu}$. An $\epsilon$-solution of $F$ is a $2\epsilon$-solution of $h$: compare with that minimizer, whose added quadratic is $O(\epsilon)$. One response still uses one $h$ query. Substituting $r$ gives
$$
c_\nu[\beta_\nu^2/(\mu^{1+\nu}\epsilon^{1-\nu})]^{1/(1+3\nu)}.
$$
Retain the initial-gap requirement
$\Delta\ge C_\nu\beta_\nu(\epsilon/\mu)^{(1+\nu)/2}$
and the original sufficient dimension. The random lower bound uses the globally shielded construction; a deterministic resisting oracle is not a substitute. Constants may depend on fixed $\nu$.

**Limits of the argument.** Fixed exponent, initial-gap admissibility, and sufficient dimension are retained. The total objective is not globally Hölder of exponent less than one.

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2010/12/2865.pdf) [2](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf)

## References

[1] Olivier Devolder; François Glineur; Yurii Nesterov. First-order methods of smooth convex optimization with inexact oracle. 2014; public preprint in 2011.

https://optimization-online.org/wp-content/uploads/2010/12/2865.pdf

[2] Jelena Diakonikolas; Cristóbal Guzmán. Lower Bounds for Parallel and Randomized Convex Optimization. 2019.

https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf
