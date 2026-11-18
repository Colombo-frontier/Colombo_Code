# Global minimization of Hölder-smooth convex functions: queries within the ball; exact function values and gradients

**Setting ID.** `SO_FO_C05_ball_FG`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present; Bounds missing

**Gap classes present.** Other quantified gap; Logarithmic gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Full space; geometry: Norm ball; geometry: Norm mismatch allowed; smoothness: Holder smooth

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Fg; operation: Value gradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Feasible point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}f(x)$$

### Admissible model

Minimize a convex differentiable function $f$ over the public set $Q=RB_p^d$. The condition $\|\nabla f(x)-\nabla f(y)\|_{q^\star}\le\beta_\nu\|x-y\|_q^\nu$ is imposed only in a neighborhood of $Q$. Both queries and outputs lie in $Q$. An arbitrarily large affine term is allowed.

Admissible parameter domain:

$$\beta_\nu>0,\quad d\in\mathbb{N}_{\ge1},\quad \varepsilon>0,\quad \nu>0,\quad \nu\le1,\quad R>0,\quad p\ge1,\quad q\ge1$$

### Oracle interface

Public numerical inputs: $d,\ p,\ q,\ \nu,\ \varepsilon$.

Public upper bounds: $\beta_\nu,\ R$.

The unknown object is the objective $f$.

Query points lie in $Q$; feedback consists of exact function values and gradients:

$$(f(x),\nabla f(x))$$

All responses are consistent with one fixed function instance. Exact values and derivatives agree across repeated queries at the same point.

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(f,x)=f(x)-f^\star$$

$f^\star=\inf_{x\in Q}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

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

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f$: Unknown objective, with domain and structure specified by the model

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in Q}f(x)$$

$Q$: Feasible set of the task

$$Q=RB_p^d$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\|\cdot\|_p,\|\cdot\|_q$: Standard finite-dimensional norm with the indicated exponent **Domain:** Endpoint norm $\|x\|_\infty=\max_{1\le j\le d}|x_j|$.

$$\|x\|_a=(\sum_{j=1}^d|x_j|^a)^{1/a},\quad1\le a<\infty$$

$B_p^d$: Unit ball of the $p$ norm

$$B_p^d=\{x\in\mathbb{R}^d:\|x\|_p\le1\}$$

$d$: Dimension; a public positive integer whose dependence is tracked jointly **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta_\nu$: Public upper bound on the gradient Hölder constant **Domain:** $\beta_\nu>0$.

$R$: Radius of the public feasible ball **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$p$: Public norm exponent specifying the feasible-set or localization geometry **Domain:** $1\le p\le\infty$.

$q$: Public norm exponent specifying the Lipschitz or gradient-regularity geometry **Domain:** $1\le q\le\infty$.

$\nu$: Hölder exponent; public, with fixed or varying status stated in each comparison **Domain:** $0<\nu\le1$.

$c$: Sufficiently small universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $0<c<1$.

$C$: Sufficiently large universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $C>1$.

$\beta$: When $\nu=1$, write $\beta=\beta_1$; this does not introduce another independent constant. **Domain:** $\beta=\beta_1\quad\text{when }\nu=1$.

$$\beta=\beta_\nu$$

$A_\varepsilon$: Dimensionless accuracy scale for Hölder smoothness

$$A_\varepsilon=\frac{\beta_\nu\,({R}^{1+\nu})}{\varepsilon}$$

$q^\star$: Hölder conjugate exponent of $q$ **Domain:** $q^\star\in[1,\infty]$.

$$1/q+1/q^\star=1,\quad1^\star=\infty,\quad\infty^\star=1$$

$T$: Query budget used only in the exact finite-budget result; it is not another model scale. **Domain:** $T\in\mathbb{N}_{\ge1}$.

$S_+$: Error scale after converting the domain and smoothness geometry to Euclidean norms

$$S_+=\beta\,{R}^{2}\,({d}^{2\,(\max\{0,(\frac{1}{q}-0.5)\}+\max\{0,(0.5-\frac{1}{p})\})})$$

$c_{\nu}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $\nu$. **Domain:** $c_{\nu}>0$.

$C_{\nu}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $\nu$. **Domain:** $C_{\nu}>0$.

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

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Smooth minimization on a ball

**Region.** $\nu=1,\quad\beta=\beta_1,\quad\varepsilon>0$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1, B2

$$
C[1+\min\{\sqrt{S_+/\varepsilon},d\log(2+S_+/\varepsilon)\}]
$$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: The constrained gradient-only upper bound applies in every dimension. Specialized mismatched geometries may admit faster rates, as stated in their regimes. Ratio: None

### R2 - High-dimensional randomized l1/l2 regime

**Region.** $p=1,q=2,\nu=1,\quad d\ge C(\beta R^2/\varepsilon)^{1/3},\quad\varepsilon\le c\beta R^2$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q2

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
c(\beta R^2/\varepsilon)^{1/3}
$$

**Upper bound.** B3, B1, B2

$$
C(\beta R^2/\varepsilon)^{1/3}[\log(2+d)\log(2+\beta R^2\log(2+d)/\varepsilon)]^{1/3}
$$

**Gap or comparison.** $C[\log(2+d)\log(2+\beta R^2\log(2+d)/\varepsilon)]^{1/3}$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: The logarithm in the implicit budget T is inverted explicitly, retaining the contribution of log log d. The expression is valid when dimension and accuracy vary jointly. Ratio: $C[\log(2+d)\log(2+\beta R^2\log(2+d)/\varepsilon)]^{1/3}$

### R3 - l1 domain with Euclidean smoothness

**Region.** $p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q2

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Other quantified gap

**Lower bound.** B4, B5

$$
c\max\{\min(d,(\beta R^2/\varepsilon)^{1/3}),\log(2+\beta R^2/\varepsilon)\}
$$

**Upper bound.** B3, B1, B2

$$
C\min\{\min\{T:\beta R^2\log(2T)\log(2d)/T^3\le c\varepsilon\},1+d\log(2+\beta R^2/\varepsilon)\}
$$

**Gap or comparison.** $\frac{C\min\{\min\{T:\beta R^2\log(2T)\log(2d)/T^3\le c\varepsilon\},1+d\log(2+\beta R^2/\varepsilon)\}}{c\max\{\min(d,(\beta R^2/\varepsilon)^{1/3}),\log(2+\beta R^2/\varepsilon)\}}$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds are logarithmic in inverse accuracy at fixed d, but their joint dimension dependence may differ polynomially. Ratio: $\frac{C\min\{\min\{T:\beta R^2\log(2T)\log(2d)/T^3\le c\varepsilon\},1+d\log(2+\beta R^2/\varepsilon)\}}{c\max\{\min(d,(\beta R^2/\varepsilon)^{1/3}),\log(2+\beta R^2/\varepsilon)\}}$

### R4 - High-dimensional randomized Hölder regime with l1/l2 geometry

**Region.** $p=1,q=2,\quad0<\nu<1,\quad d\ge C_\nu A_\varepsilon^{1/(1+2\nu)}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q2

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B7

$$
c_\nu A_\varepsilon^{1/(1+2\nu)}
$$

**Upper bound.** B6

$$
C_\nu A_\varepsilon^{1/(1+2\nu)}[\log(2+d)\log(2+A_\varepsilon\log(2+d))]^{(1+\nu)/(2+4\nu)}
$$

**Gap or comparison.** $C_\nu[\log(2+d)\log(2+A_\varepsilon\log(2+d))]^{(1+\nu)/(2+4\nu)}$

### R5 - High-dimensional randomized matching infinity-norm endpoint

**Region.** $p=q=\infty,\quad d\ge C_\nu A_\varepsilon^{3/\nu}\log(2+A_\varepsilon),\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q2

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B9

$$
c_\nu A_\varepsilon^{1/\nu}/\log(2+d)
$$

**Upper bound.** B8

$$
C_\nu A_\varepsilon^{1/\nu}
$$

**Gap or comparison.** $C_\nu\log(2+d)$

### R6 - Smooth minimization on a ball

**Region.** $\nu=1,\quad\beta=\beta_1,\quad\varepsilon>0$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B10, B11

$$
C[1+\min\{\sqrt{S_+/\varepsilon},d\log(2+S_+/\varepsilon)\}]
$$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: The constrained gradient-only upper bound applies in every dimension. Specialized mismatched geometries may admit faster rates, as stated in their regimes. Ratio: None

### R7 - High-dimensional randomized l1/l2 regime

**Region.** $p=1,q=2,\nu=1,\quad d\ge C(\beta R^2/\varepsilon)^{1/3},\quad\varepsilon\le c\beta R^2$

**Views.** Randomized / Expected loss

**Quantity.** Q4

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B13

$$
c(\beta R^2/\varepsilon)^{1/3}
$$

**Upper bound.** B12, B10, B11

$$
C(\beta R^2/\varepsilon)^{1/3}[\log(2+d)\log(2+\beta R^2\log(2+d)/\varepsilon)]^{1/3}
$$

**Gap or comparison.** $C[\log(2+d)\log(2+\beta R^2\log(2+d)/\varepsilon)]^{1/3}$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: The logarithm in the implicit budget T is inverted explicitly, retaining the contribution of log log d. The expression is valid when dimension and accuracy vary jointly. Ratio: $C[\log(2+d)\log(2+\beta R^2\log(2+d)/\varepsilon)]^{1/3}$

### R8 - l1 domain with Euclidean smoothness

**Region.** $p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$

**Views.** Randomized / Expected loss

**Quantity.** Q4

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Other quantified gap

**Lower bound.** B13, B14

$$
c\max\{\min(d,(\beta R^2/\varepsilon)^{1/3}),\log(2+\beta R^2/\varepsilon)\}
$$

**Upper bound.** B12, B10, B11

$$
C\min\{\min\{T:\beta R^2\log(2T)\log(2d)/T^3\le c\varepsilon\},1+d\log(2+\beta R^2/\varepsilon)\}
$$

**Gap or comparison.** $\frac{C\min\{\min\{T:\beta R^2\log(2T)\log(2d)/T^3\le c\varepsilon\},1+d\log(2+\beta R^2/\varepsilon)\}}{c\max\{\min(d,(\beta R^2/\varepsilon)^{1/3}),\log(2+\beta R^2/\varepsilon)\}}$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds are logarithmic in inverse accuracy at fixed d, but their joint dimension dependence may differ polynomially. Ratio: $\frac{C\min\{\min\{T:\beta R^2\log(2T)\log(2d)/T^3\le c\varepsilon\},1+d\log(2+\beta R^2/\varepsilon)\}}{c\max\{\min(d,(\beta R^2/\varepsilon)^{1/3}),\log(2+\beta R^2/\varepsilon)\}}$

### R9 - High-dimensional randomized Hölder regime with l1/l2 geometry

**Region.** $p=1,q=2,\quad0<\nu<1,\quad d\ge C_\nu A_\varepsilon^{1/(1+2\nu)}$

**Views.** Randomized / Expected loss

**Quantity.** Q4

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B16

$$
c_\nu A_\varepsilon^{1/(1+2\nu)}
$$

**Upper bound.** B15

$$
C_\nu A_\varepsilon^{1/(1+2\nu)}[\log(2+d)\log(2+A_\varepsilon\log(2+d))]^{(1+\nu)/(2+4\nu)}
$$

**Gap or comparison.** $C_\nu[\log(2+d)\log(2+A_\varepsilon\log(2+d))]^{(1+\nu)/(2+4\nu)}$

### R10 - High-dimensional randomized matching infinity-norm endpoint

**Region.** $p=q=\infty,\quad d\ge C_\nu A_\varepsilon^{3/\nu}\log(2+A_\varepsilon),\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$

**Views.** Randomized / Expected loss

**Quantity.** Q4

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B18

$$
c_\nu A_\varepsilon^{1/\nu}/\log(2+d)
$$

**Upper bound.** B17

$$
C_\nu A_\varepsilon^{1/\nu}
$$

**Gap or comparison.** $C_\nu\log(2+d)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Accelerated gradient method on a ball

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\sqrt{S_+/\varepsilon}]
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2010/12/2865.pdf)

**Conditions.** $$\nu=1,\quad\beta=\beta_1,\quad\varepsilon>0$$

**Dimension conditions.** $\nu=1,\quad\beta=\beta_1,\quad\varepsilon>0$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2010/12/2865.pdf) theorem: Section 5.1, Theorem 5, and equation (42); the fixed schedule reads gradients only

### B2 - Cutting-plane localization for smooth functions

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+d\log(2+S_+/\varepsilon)]
$$

**Sources.** [4](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$\nu=1,\quad\beta=\beta_1,\quad\varepsilon>0$$

**Dimension conditions.** $\nu=1,\quad\beta=\beta_1,\quad\varepsilon>0$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

**Source location.** [4](https://arxiv.org/pdf/2609.32910) theorem: Proposition E.12, PDF pp. 51–52, extended to a general public $p$-norm ball

### B3 - Value-gradient algorithm for mismatched geometry

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
\min\{T\ge1:C\beta R^2\log(2T)\log(2d)/T^3\le\varepsilon\}
$$

**Sources.** [4](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$$

**Dimension conditions.** $p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [4](https://arxiv.org/pdf/2609.32910) theorem: PropositionsE.1–E.3, PDFpp.41–43

### B4 - Randomized hard instances for mismatched geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{d,(\beta R^2/\varepsilon)^{1/3}\}
$$

**Sources.** [4](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$$

**Dimension conditions.** $p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [4](https://arxiv.org/pdf/2609.32910) theorem: Theorem 1 and Proposition D.7, PDF pp. 4 and 36; randomized construction with $d\ge32T+1$

### B5 - One-dimensional smooth localization hard instances

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\beta R^2/\varepsilon)
$$

**Sources.** [5](https://arxiv.org/pdf/2101.09740v2) [6](https://arxiv.org/pdf/2609.33360v2) [7](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$$

**Dimension conditions.** $p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A2, A3

### B6 - Non-Euclidean acceleration for Hölder-smooth functions

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
\min\{T\ge1:C_\nu\beta_\nu R^{1+\nu}[\log(2T)\log(2d)]^{(1+\nu)/2}/T^{1+2\nu}\le\varepsilon\}
$$

**Sources.** [4](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,q=2,\quad0<\nu<1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$$

**Dimension conditions.** $p=1,q=2,\quad0<\nu<1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [4](https://arxiv.org/pdf/2609.32910) theorem: Propositions D.8 and E.3, specialized to first-order access; PDF pp. 36 and 43

### B7 - Hölder-smooth hard instances with mismatched geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\nu\min\{d,A_\varepsilon^{1/(1+2\nu)}\}
$$

**Sources.** [4](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,q=2,\quad0<\nu<1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$$

**Dimension conditions.** $p=1,q=2,\quad0<\nu<1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [4](https://arxiv.org/pdf/2609.32910) theorem: Propositions D.8 and E.3, specialized to first-order access; PDF pp. 36 and 43

### B8 - Conditional gradient method on a box

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_\nu A_\varepsilon^{1/\nu}
$$

**Sources.** [3](https://arxiv.org/pdf/1307.5001)

**Conditions.** $$p=q=\infty,\quad0<\nu\le1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$$

**Dimension conditions.** $p=q=\infty,\quad0<\nu\le1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [3](https://arxiv.org/pdf/1307.5001) theorem: Section 4.1A: Frank–Wolfe on the matching infinity-norm ball with Hölder exponent $\nu$

### B9 - Hard instances for box geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\nu A_\varepsilon^{1/\nu}/\log(2+d)
$$

**Sources.** [2](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf)

**Conditions.** $$p=q=\infty,\quad d\ge C_\nu A_\varepsilon^{3/\nu}\log(2+A_\varepsilon),\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$$

**Dimension conditions.** $p=q=\infty,\quad d\ge C_\nu A_\varepsilon^{3/\nu}\log(2+A_\varepsilon),\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) theorem: Second bullet following Theorem 12, PDF p. 11; $p\to\infty$, $K=1$, and constant failure probability

### B10 - Accelerated gradient method on a ball

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\sqrt{S_+/\varepsilon}]
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2010/12/2865.pdf)

**Conditions.** $$\nu=1,\quad\beta=\beta_1,\quad\varepsilon>0$$

**Dimension conditions.** $\nu=1,\quad\beta=\beta_1,\quad\varepsilon>0$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2010/12/2865.pdf) theorem: Section 5.1, Theorem 5, and equation (42); the fixed schedule reads gradients only

### B11 - Cutting-plane localization for smooth functions

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+d\log(2+S_+/\varepsilon)]
$$

**Sources.** [4](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$\nu=1,\quad\beta=\beta_1,\quad\varepsilon>0$$

**Dimension conditions.** $\nu=1,\quad\beta=\beta_1,\quad\varepsilon>0$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

**Source location.** [4](https://arxiv.org/pdf/2609.32910) theorem: Proposition E.12, PDF pp. 51–52, extended to a general public $p$-norm ball

### B12 - Value-gradient algorithm for mismatched geometry

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
\min\{T\ge1:C\beta R^2\log(2T)\log(2d)/T^3\le\varepsilon\}
$$

**Sources.** [4](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$$

**Dimension conditions.** $p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [4](https://arxiv.org/pdf/2609.32910) theorem: PropositionsE.1–E.3, PDFpp.41–43

### B13 - Randomized hard instances for mismatched geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{d,(\beta R^2/\varepsilon)^{1/3}\}
$$

**Sources.** [4](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$$

**Dimension conditions.** $p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [4](https://arxiv.org/pdf/2609.32910) theorem: Theorem 1 and Proposition D.7, PDF pp. 4 and 36; randomized construction with $d\ge32T+1$

### B14 - One-dimensional smooth localization hard instances

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(2+\beta R^2/\varepsilon)
$$

**Sources.** [5](https://arxiv.org/pdf/2101.09740v2) [6](https://arxiv.org/pdf/2609.33360v2) [7](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$$

**Dimension conditions.** $p=1,q=2,\nu=1,\quad\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A2, A3

### B15 - Non-Euclidean acceleration for Hölder-smooth functions

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
\min\{T\ge1:C_\nu\beta_\nu R^{1+\nu}[\log(2T)\log(2d)]^{(1+\nu)/2}/T^{1+2\nu}\le\varepsilon\}
$$

**Sources.** [4](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,q=2,\quad0<\nu<1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$$

**Dimension conditions.** $p=1,q=2,\quad0<\nu<1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [4](https://arxiv.org/pdf/2609.32910) theorem: Propositions D.8 and E.3, specialized to first-order access; PDF pp. 36 and 43

### B16 - Hölder-smooth hard instances with mismatched geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\nu\min\{d,A_\varepsilon^{1/(1+2\nu)}\}
$$

**Sources.** [4](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,q=2,\quad0<\nu<1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$$

**Dimension conditions.** $p=1,q=2,\quad0<\nu<1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [4](https://arxiv.org/pdf/2609.32910) theorem: Propositions D.8 and E.3, specialized to first-order access; PDF pp. 36 and 43

### B17 - Conditional gradient method on a box

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_\nu A_\varepsilon^{1/\nu}
$$

**Sources.** [3](https://arxiv.org/pdf/1307.5001)

**Conditions.** $$p=q=\infty,\quad0<\nu\le1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$$

**Dimension conditions.** $p=q=\infty,\quad0<\nu\le1,\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [3](https://arxiv.org/pdf/1307.5001) theorem: Section 4.1A: Frank–Wolfe on the matching infinity-norm ball with Hölder exponent $\nu$

### B18 - Hard instances for box geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\nu A_\varepsilon^{1/\nu}/\log(2+d)
$$

**Sources.** [2](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf)

**Conditions.** $$p=q=\infty,\quad d\ge C_\nu A_\varepsilon^{3/\nu}\log(2+A_\varepsilon),\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$$

**Dimension conditions.** $p=q=\infty,\quad d\ge C_\nu A_\varepsilon^{3/\nu}\log(2+A_\varepsilon),\quad\varepsilon\le c_\nu\beta_\nu R^{1+\nu}$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf) theorem: Second bullet following Theorem 12, PDF p. 11; $p\to\infty$, $K=1$, and constant failure probability

## 5. Local arguments

### A1 - Smooth constrained cuts with unrestricted affine slope

**Scope.** Gradient-only queries inside the public convex ball; no bound on affine slope.

**Algorithm scope.** Deterministic upper witness.

Suppose $Q\subset B(0,R)$ is public, compact, convex, and contains zero, and $f$ is convex and $\beta$-smooth near $Q$. Query $b=\nabla f(0)$, choose $y\in\arg\min_Q\langle b,u\rangle$, and query $\nabla f(y)$. Every point satisfying $\langle\nabla f(y),y-u\rangle\ge\epsilon$ lies in
$$
C_b=\{u\in Q:\langle b,u-y\rangle\le2\beta R^2\},
$$
because replacing $\nabla f(y)$ by $b$ costs at most $2\beta R^2$. For $w,v\in C_b$, the affine functional varies by at most $2\beta R^2$, and gradient variation contributes at most another $2\beta R^2$. Hence $\langle\nabla f(w),w-v\rangle\ge-4\beta R^2$.

At each centroid $w_i$ of the retained part of $C_b$, retain the shallow cut of margin $\epsilon/2$. It removes at least a constant fraction of volume. If all deep cuts of margin $\epsilon$, including the cut at $y$, share a point $z$, then
$(1-a)z+aC_b$, $a=\epsilon/[2(\epsilon+4\beta R^2)]$, survives all shallow cuts. Volume shrinkage contradicts this after $O(d\log(2+\beta R^2/\epsilon))$ iterations. Empty deep intersection gives a minimax subgradient certificate and a feasible convex combination of queried points with the desired error. Degenerate bodies are handled in their affine hull, or by the positive-volume limiting argument.

The initialization costs two calls, and all queries lie in $Q$. No bound on $\|\nabla f(0)\|$ is assumed. For $RB_p^d$ and $\ell_q$-smoothness, insert the declared Euclidean norm conversions.

**Limits of the argument.** Smoothness is required near the domain. Exact geometric operations are internal; no efficient arithmetic bound is claimed.

### A2 - A one-dimensional lower bound with exact values and gradients

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

### A3 - Smooth localization and gradient-norm conversion

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

**Sources.** [5](https://arxiv.org/pdf/2101.09740v2) [6](https://arxiv.org/pdf/2609.33360v2) [7](https://arxiv.org/pdf/2609.10874)

## References

[1] Olivier Devolder; François Glineur; Yurii Nesterov. First-order methods of smooth convex optimization with inexact oracle. 2014; public preprint in 2011.

https://optimization-online.org/wp-content/uploads/2010/12/2865.pdf

[2] Jelena Diakonikolas; Cristóbal Guzmán. Lower Bounds for Parallel and Randomized Convex Optimization. 2019.

https://proceedings.mlr.press/v99/diakonikolas19c/diakonikolas19c.pdf

[3] Cristóbal Guzmán; Arkadi Nemirovski. On Lower Complexity Bounds for Large-Scale Smooth Convex Optimization. 2015; arXiv2013.

https://arxiv.org/pdf/1307.5001

[4] Timofei Loginov, Alexander Gasnikov, Yuriy Dorn, Aleksandr Shestakov, Nazarii Tupitsa, Osman Osmanov and Darina Dvinskikh. The Complexity of Convex Optimization with Mismatched Geometry. 2026-09-26, arXiv v1 preprint.

https://arxiv.org/pdf/2609.32910

[5] Yoel Drori; Adrien Taylor. On the oracle complexity of smooth strongly convex minimization. 2021; arXiv:2101.09740v2.

https://arxiv.org/pdf/2101.09740v2

[6] Yoel Drori. Exact oracle complexity for function-value suboptimality under weighted initial conditions. 2026-10-16; preprintv2.

https://arxiv.org/pdf/2609.33360v2

[7] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 2026-09-09; preprintv1.

https://arxiv.org/pdf/2609.10874
