# Minimization under a global PL inequality: exact gradients

**Setting ID.** `SO_FO_N03_G`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Other quantified gap; Logarithmic gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; growth: Pl condition; initialization: Initial gap; smoothness: Lipschitz gradient

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Gradient; operation: Gradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

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

$f\in C^1(\mathbb R^d)$ has a globally $\beta$-Lipschitz gradient, is bounded below, and satisfies $f(x_0)-\inf f\le\Delta$. For every $x\in\mathbb R^d$, $\|\nabla f(x)\|_2^2\ge2\mu(f(x)-\inf f)$. Nonconvex functions are allowed, and the optimal value is unknown.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad \beta>0,\quad \mu>0,\quad \Delta>0,\quad \varepsilon>0,\quad \mu\le\beta$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ \Delta$.

Public lower bounds: $\mu$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of exact gradients:

$$\nabla f(x)$$

All responses are consistent with one fixed function instance. Exact values and derivatives agree across repeated queries at the same point.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$f(\widehat{x})-f^\star$$

$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

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

$\mu$: Known lower bound on the global PL modulus **Domain:** $0<\mu\le\beta$.

$\Delta$: Public upper bound on the initial objective gap; the optimal value itself is unknown **Domain:** $\Delta>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $0<c<1$.

$C$: Sufficiently large absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $C>1$.

$\kappa$: Derived condition number $\kappa=\beta/\mu$, where $\mu$ is a PL constant, not a strong-convexity modulus. **Domain:** $\kappa=\beta/\mu\ge1$.

$$\kappa=\frac{\beta}{\mu}$$

$d_{\rm hd}$: Sufficient dimension function for the OW stochastic-gradient construction. It exists and has an upper bound up to logarithmic factors; the construction does not supply a uniform numerical threshold for automatic evaluation. **Domain:** $d_{\rm hd}\le\widetilde{O}(\kappa^2\Delta/\varepsilon)$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

$\lceil a\rceil$: Smallest integer greater than or equal to $a$

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

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - The initial point suffices

**Region.** $\varepsilon\ge\Delta$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q3

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B2, B14

$$
0
$$

**Upper bound.** B1, B13

$$
0
$$

### R2 - Equal PL and smoothness constants

**Region.** $\kappa=1,\quad0<\varepsilon<\Delta$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q3

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B4, B16

$$
1
$$

**Upper bound.** B3, B15

$$
1
$$

**Gap or comparison.** $1$

### R3 - Main fixed one-dimensional regime

**Region.** $d=1,\quad\kappa\ge6,\quad\varepsilon\le c\Delta$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Logarithmic gap

**Lower bound.** B7

$$
c\log(\Delta/\varepsilon)
$$

**Upper bound.** B6, B5

$$
C\min\{\log(2+\kappa\Delta/\varepsilon),\kappa\log(\Delta/\varepsilon)\}
$$

**Gap or comparison.** $C[1+\log\kappa/\log(\Delta/\varepsilon)]$

**Comparison argument.** Intersect this comparison region with N03-domain. The joint-parameter bounds differ by at most an additive $\log\kappa$ term. They match up to constants for fixed $\kappa$; necessity of the $\log\kappa$ term is not asserted.

### R4 - Main nondegenerate comparison region

**Region.** $\kappa\ge6,\quad0<\varepsilon\le c\Delta$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Other quantified gap

**Lower bound.** B7, B11

$$
c\max\{\log(\Delta/\varepsilon),\min\{d,\kappa\log(\Delta/\varepsilon)\}\}
$$

**Upper bound.** B5

$$
C\kappa\log(\Delta/\varepsilon)
$$

**Gap or comparison.** $\text{upper envelope / displayed lower envelope}$

### R5 - Sufficient dimension for the deterministic hard chain

**Region.** $\kappa\ge C,\quad d\ge C\kappa\log(\Delta/\varepsilon),\quad\varepsilon\le c\Delta$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B8

$$
c\kappa\log(\Delta/\varepsilon)
$$

**Upper bound.** B5

$$
C\kappa\log(\Delta/\varepsilon)
$$

**Gap or comparison.** $C/c$

### R6 - Main fixed two-dimensional regime

**Region.** $d=2,\quad\kappa\ge6,\quad\varepsilon\le c\Delta$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Polynomial gap

**Lower bound.** B7

$$
c\log(\Delta/\varepsilon)
$$

**Upper bound.** B5

$$
C\kappa\log(\Delta/\varepsilon)
$$

**Gap or comparison.** $C\kappa$

### R7 - Main fixed one-dimensional regime

**Region.** $d=1,\quad\kappa\ge6,\quad\varepsilon\le c\Delta$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Logarithmic gap

**Lower bound.** B19

$$
c\log(\Delta/\varepsilon)
$$

**Upper bound.** B18, B17

$$
C\min\{\log(2+\kappa\Delta/\varepsilon),\kappa\log(\Delta/\varepsilon)\}
$$

**Gap or comparison.** $C[1+\log\kappa/\log(\Delta/\varepsilon)]$

**Comparison argument.** Intersect this comparison region with N03-domain. The joint-parameter bounds differ by at most an additive $\log\kappa$ term. They match up to constants for fixed $\kappa$; necessity of the $\log\kappa$ term is not asserted.

### R8 - Main nondegenerate comparison region

**Region.** $\kappa\ge6,\quad0<\varepsilon\le c\Delta$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Other quantified gap

**Lower bound.** B19, B23

$$
c\max\{\log(\Delta/\varepsilon),\min\{\sqrt d,\sqrt\kappa\log(\Delta/\varepsilon)\}\}
$$

**Upper bound.** B17

$$
C\kappa\log(\Delta/\varepsilon)
$$

**Gap or comparison.** $\text{upper envelope / displayed lower envelope}$

### R9 - Sufficient dimension for arbitrary randomized gradient-only algorithms

**Region.** $\kappa\ge6,\quad\varepsilon\le c\Delta,\quad d\ge d_{\rm hd};\quad d_{\rm hd}\le\widetilde{O}(\kappa^2\Delta/\varepsilon)$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B21

$$
c\kappa\log(\Delta/\varepsilon)
$$

**Upper bound.** B17

$$
C\kappa\log(\Delta/\varepsilon)
$$

**Gap or comparison.** $C/c$

### R10 - Main fixed two-dimensional regime

**Region.** $d=2,\quad\kappa\ge6,\quad\varepsilon\le c\Delta$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Polynomial gap

**Lower bound.** B19

$$
c\log(\Delta/\varepsilon)
$$

**Upper bound.** B17, B20

$$
\widetilde{O}(\kappa^{2/3}\log(\Delta/\varepsilon))
$$

**Gap or comparison.** $\widetilde{O}(\kappa^{2/3})$

**Comparison argument.** Intersect this comparison region with N03-domain. Joint condition-number dependence in two dimensions remains unmatched. With $\kappa$ fixed, only the accuracy order $\log(\Delta/\varepsilon)$ is closed.

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

**Conditions.** $$\varepsilon\ge\Delta$$

**Dimension conditions.** $\varepsilon\ge\Delta$

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

**Conditions.** $$\varepsilon\ge\Delta$$

**Dimension conditions.** $\varepsilon\ge\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B3 - One exact gradient step attains the optimum when $\kappa=1$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $$\kappa=1,\quad0<\varepsilon<\Delta$$

**Dimension conditions.** $\kappa=1,\quad0<\varepsilon<\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B4 - Unknown translated quadratics rule out zero queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $$\kappa=1,\quad0<\varepsilon<\Delta$$

**Dimension conditions.** $\kappa=1,\quad0<\varepsilon<\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B5 - Exact gradient descent under the PL condition

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
\left\lceil\frac{\log(\Delta/\varepsilon)}{\log(\kappa/(\kappa-1))}\right\rceil
$$

**Conditions.** $$\kappa>1,\quad0<\varepsilon<\Delta$$

**Dimension conditions.** $\kappa>1,\quad0<\varepsilon<\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B6 - One-dimensional bisection using exact derivative signs

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\log(2+\kappa\Delta/\varepsilon)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$d=1,\quad\kappa\ge6,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $d=1,\quad\kappa\ge6,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Lemma D.4, PDF p. 55; noiseless derivative-sign bisection derived from Algorithm 2

### B7 - One-dimensional randomized FG lower-bound embedding

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(\Delta/\varepsilon)
$$

**Conditions.** $$\kappa\ge6,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge6,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A2

### B8 - Hard chain for arbitrary deterministic value-gradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\kappa\log(\Delta/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/2212.13551) [3](https://arxiv.org/pdf/1710.11606)

**Conditions.** $$\kappa\ge C,\quad d\ge C\kappa\log(\Delta/\varepsilon),\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge C,\quad d\ge C\kappa\log(\Delta/\varepsilon),\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2212.13551) theorem: Lemmas 1–2, Theorem 2, and Section 3.2, equation (5), combined with CDHS20, Proposition 2

**Source location.** [3](https://arxiv.org/pdf/1710.11606) theorem: The value-inclusive first-order interface in Section 2 and the deterministic rotation in Proposition 2

### B9 - High-dimensional lower bound for arbitrary randomized gradient-only algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\kappa\log(\Delta/\varepsilon)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$\kappa\ge6,\quad\varepsilon\le c\Delta,\quad d\ge d_{\rm hd};\quad d_{\rm hd}\le\widetilde{O}(\kappa^2\Delta/\varepsilon)$$

**Dimension conditions.** $\kappa\ge6,\quad\varepsilon\le c\Delta,\quad d\ge d_{\rm hd};\quad d_{\rm hd}\le\widetilde{O}(\kappa^2\Delta/\varepsilon)$

**Oracle correspondence.** Applicable interfaces: exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorem 3.1 sigma=0; Appendix B.4 (163), (168)

### B10 - Strongly convex subclass for arbitrary randomized value-gradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\sqrt\kappa\log(\Delta/\varepsilon)
$$

**Sources.** [4](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$\kappa\ge6,\quad\varepsilon\le c\Delta,\quad d\ge C\kappa\log^2(\Delta/\varepsilon)$$

**Dimension conditions.** $\kappa\ge6,\quad\varepsilon\le c\Delta,\quad d\ge C\kappa\log^2(\Delta/\varepsilon)$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [4](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1; strongly convex quadratic reduction on PDF p. 3; dimension specified in equation (7)

### B11 - Truncated deterministic hard chain

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c\min\{d,\kappa\log(\Delta/\varepsilon)\}
$$

**Sources.** [2](https://arxiv.org/pdf/2212.13551) [3](https://arxiv.org/pdf/1710.11606)

**Conditions.** $$\kappa\ge6,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge6,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2212.13551) theorem: Lemmas 1–2, Theorem 2, and Section 3.2, equation (5), combined with CDHS20, Proposition 2

**Source location.** [3](https://arxiv.org/pdf/1710.11606) theorem: The value-inclusive first-order interface in Section 2 and the deterministic rotation in Proposition 2

### B12 - Truncated randomized strongly convex subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,\sqrt\kappa\log(\Delta/\varepsilon)\}
$$

**Sources.** [4](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$\kappa\ge6,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge6,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [4](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1; strongly convex quadratic reduction on PDF p. 3; dimension specified in equation (7)

### B13 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $$\varepsilon\ge\Delta$$

**Dimension conditions.** $\varepsilon\ge\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B14 - Nonnegative resource budgets

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $$\varepsilon\ge\Delta$$

**Dimension conditions.** $\varepsilon\ge\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B15 - One exact gradient step attains the optimum when $\kappa=1$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $$\kappa=1,\quad0<\varepsilon<\Delta$$

**Dimension conditions.** $\kappa=1,\quad0<\varepsilon<\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B16 - Unknown translated quadratics rule out zero queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $$\kappa=1,\quad0<\varepsilon<\Delta$$

**Dimension conditions.** $\kappa=1,\quad0<\varepsilon<\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B17 - Exact gradient descent under the PL condition

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
\left\lceil\frac{\log(\Delta/\varepsilon)}{\log(\kappa/(\kappa-1))}\right\rceil
$$

**Conditions.** $$\kappa>1,\quad0<\varepsilon<\Delta$$

**Dimension conditions.** $\kappa>1,\quad0<\varepsilon<\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B18 - One-dimensional bisection using exact derivative signs

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\log(2+\kappa\Delta/\varepsilon)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$d=1,\quad\kappa\ge6,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $d=1,\quad\kappa\ge6,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Lemma D.4, PDF p. 55; noiseless derivative-sign bisection derived from Algorithm 2

### B19 - One-dimensional randomized FG lower-bound embedding

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(\Delta/\varepsilon)
$$

**Conditions.** $$\kappa\ge6,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge6,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A2

### B20 - Two-dimensional randomized gradient line-integration algorithm

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}(\kappa^{2/3}\log(\Delta/\varepsilon))
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$d=2,\quad\kappa\ge6,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $d=2,\quad\kappa\ge6,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorem 5.3, Theorem D.1(ii), sigma=0; Appendix D.4–D.5

### B21 - High-dimensional lower bound for arbitrary randomized gradient-only algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\kappa\log(\Delta/\varepsilon)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$\kappa\ge6,\quad\varepsilon\le c\Delta,\quad d\ge d_{\rm hd};\quad d_{\rm hd}\le\widetilde{O}(\kappa^2\Delta/\varepsilon)$$

**Dimension conditions.** $\kappa\ge6,\quad\varepsilon\le c\Delta,\quad d\ge d_{\rm hd};\quad d_{\rm hd}\le\widetilde{O}(\kappa^2\Delta/\varepsilon)$

**Oracle correspondence.** Applicable interfaces: exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorem 3.1 sigma=0; Appendix B.4 (163), (168)

### B22 - Strongly convex subclass for arbitrary randomized value-gradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\sqrt\kappa\log(\Delta/\varepsilon)
$$

**Sources.** [4](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$\kappa\ge6,\quad\varepsilon\le c\Delta,\quad d\ge C\kappa\log^2(\Delta/\varepsilon)$$

**Dimension conditions.** $\kappa\ge6,\quad\varepsilon\le c\Delta,\quad d\ge C\kappa\log^2(\Delta/\varepsilon)$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [4](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1; strongly convex quadratic reduction on PDF p. 3; dimension specified in equation (7)

### B23 - Truncated randomized strongly convex subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,\sqrt\kappa\log(\Delta/\varepsilon)\}
$$

**Sources.** [4](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$\kappa\ge6,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge6,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: exact function values and gradients, exact gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [4](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1; strongly convex quadratic reduction on PDF p. 3; dimension specified in equation (7)

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

## References

[1] Weiming Ou; Xiao Wang. Tight Heavy-Tailed Complexity Bounds for Optimizing Polyak–Łojasiewicz Objectives. 2026-09-26; preprintv2.

https://arxiv.org/pdf/2609.03990

[2] Pengyun Yue; Cong Fang; Zhouchen Lin. On the Lower Bound of Minimizing Polyak-Lojasiewicz Functions. 2023.

https://arxiv.org/pdf/2212.13551

[3] Yair Carmon; John C. Duchi; Oliver Hinder; Aaron Sidford. Lower Bounds for Finding Stationary Points I. 2020; arXiv v3 2019.

https://arxiv.org/pdf/1710.11606

[4] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 2026-09-09; preprintv1.

https://arxiv.org/pdf/2609.10874
