# Smooth convex composite minimization: strong convexity of the complete objective; function values, gradients, and an exact proximal map

**Setting ID.** `SO_FO_C06_SC_FG`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Full space; smoothness: Lipschitz gradient; structure: Composite

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Fg plus exact prox; interface family: Mixed; operation: Value gradient prox; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \operatorname{dom}h}F(x)$$

The complete objective is $F=f+h$. The properties and Oracle interfaces of the two terms are specified separately.

### Admissible model

$F=f+h$, where $f$ is globally convex and $\beta$-smooth, and $h$ is a proper closed convex extended-real-valued function. The complete objective $F$ is $\mu$-strongly convex and satisfies $F(x_0)-F^\star\le\Delta$. Values $\mu>\beta$ are allowed because strong convexity may come from $h$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Strong convexity applies to the complete objective: $F(v)\ge F(u)+\langle g,v-u\rangle+\frac\mu2\|v-u\|_2^2$ for $u,v\in\operatorname{dom}h$ and $g\in\partial F(u)$.

Admissible parameter domain:

$$\beta>0,\quad d\in\mathbb{N}_{\ge1},\quad \varepsilon>0,\quad \Delta>0,\quad \mu>0$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ \Delta$.

Public lower bounds: $\mu$.

The unknown object is the objective $f$. Access to the composite term $h$, including public information and proximal operations, is specified by the interface below.

Query points lie in $\mathbb{R}^d$; feedback consists of function values, gradients, and exact proximal access:

$$(f(x),\nabla f(x));\ \operatorname{prox}_{\eta h}(v),\ \eta>0$$

All responses are consistent with one fixed function instance. Exact values and derivatives agree across repeated queries at the same point.

Independent queries to $\operatorname{prox}_{\eta h}(v)$ are allowed for $v\in\mathbb R^d$ and $\eta>0$. Their cost is specified separately by the resource convention.

### Output

Return a point $\widehat x\in\operatorname{dom}h$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$F(\widehat{x})-F^\star=(f+h)(\widehat{x})-\inf(f+h)$$

$F^\star=\inf_{x\in \operatorname{dom}h}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

First retain the joint budget $(N_G,N_P)$ achieved by one algorithm. A primitive first-order response for $f$ and an exact proximal response for $h$ each increment the corresponding coordinate by one. The scalar comparison explicitly uses $T=N_G+N_P$.

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

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \operatorname{dom}h$.

$f,h,F$: Smooth or Lipschitz term, convex proximal term, and complete objective

$$F=f+h$$

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in \operatorname{dom}h}F(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial F(x)$: Ambient subdifferential of the corresponding convex function

$$\partial F(x)=\{g:F(u)\ge F(x)+\langle g,u-x\rangle\ \forall u\in\operatorname{dom}F\}$$

$\operatorname{prox}_{\eta h}$: Proximal map of $h$, either public or obtained through the declared interface **Domain:** $\eta>0,\ v\in\mathbb{R}^d$.

$$\operatorname{prox}_{\eta h}(v)=\arg\min_u\{h(u)+\|u-v\|_2^2/(2\eta)\}$$

$\operatorname{dom}h$: Effective domain of $h$

$$\operatorname{dom}h=\{x:h(x)<+\infty\}$$

$d$: Dimension; a public positive integer whose dependence is tracked jointly **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient Lipschitz or smoothness constant **Domain:** $\beta>0$.

$\mu$: Lower bound on the strong-convexity modulus of the objective specified by the model **Domain:** $\mu>0$.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\Delta$: Public upper bound on initial suboptimality, rather than its exact value **Domain:** $\Delta>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $0<c<1$.

$C$: Sufficiently large universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $C>1$.

$\kappa$: Smooth-part constant divided by the strong-convexity modulus of the complete objective; the ratio may be less than one

$$\kappa=\frac{\beta}{\mu}$$

$H_\varepsilon$: Query scale for strongly convex objectives with a large condition number

$$H_\varepsilon=\sqrt{\kappa}\,\log(\frac{\Delta}{\varepsilon})$$

$T$: Total budget for the declared resource projection; for a risk curve, the budget is fixed in advance **Domain:** $T\in\mathbb{N}_{\ge0}$.

$N_G,N_P$: Primitive first-order calls for $f$ and exact proximal calls for $h$ **Domain:** $N_G,N_P\in\mathbb{N}_{\ge0}$.

$$T=N_G+N_P$$

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

**Definition.** Each gradient/value-gradient call for $f$ and each proximal call for $h$ costs one; $T=N_G+N_P$.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each gradient/value-gradient call for $f$ and each proximal call for $h$ costs one; $T=N_G+N_P$.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Strong convexity with $\kappa\ge4$

**Region.** $\kappa\ge4,\quad\varepsilon\le c\Delta$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each gradient/value-gradient call for $f$ and each proximal call for $h$ costs one; $T=N_G+N_P$.

**Status.** Other quantified gap

**Lower bound.** B4, B6

$$
c\max\{\min\{d,H_\varepsilon\},\log(\Delta/\varepsilon)\}
$$

**Upper bound.** B1, B2

$$
C\min\{H_\varepsilon,1+d\log(2+\kappa\Delta/\varepsilon)\}
$$

**Gap or comparison.** $\frac{C\min\{H_\varepsilon,1+d\log(2+\kappa\Delta/\varepsilon)\}}{c\max\{\min\{d,H_\varepsilon\},\log(\Delta/\varepsilon)\}}$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $\frac{C\min\{H_\varepsilon,1+d\log(2+\kappa\Delta/\varepsilon)\}}{c\max\{\min\{d,H_\varepsilon\},\log(\Delta/\varepsilon)\}}$

### R2 - Sufficient dimension for the randomized strongly convex lower bound

**Region.** $\kappa\ge4,\quad d\ge C\kappa\log^2(\Delta/\varepsilon),\quad\varepsilon\le c\Delta$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** Each gradient/value-gradient call for $f$ and each proximal call for $h$ costs one; $T=N_G+N_P$.

**Status.** Optimal

**Lower bound.** B5, B12

$$
cH_\varepsilon
$$

**Upper bound.** B1, B9

$$
CH_\varepsilon
$$

**Gap or comparison.** $C$

### R3 - Sufficient dimension for the deterministic strongly convex lower bound

**Region.** $\kappa\ge4,\quad d\ge C\sqrt\kappa\log(\Delta/\varepsilon),\quad\varepsilon\le c\Delta$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each gradient/value-gradient call for $f$ and each proximal call for $h$ costs one; $T=N_G+N_P$.

**Status.** Optimal

**Lower bound.** B4

$$
cH_\varepsilon
$$

**Upper bound.** B1

$$
CH_\varepsilon
$$

**Gap or comparison.** $C$

### R4 - Strong convexity with $1\le\kappa\le4$

**Region.** $1\le\kappa\le4,\quad\varepsilon\le c\Delta$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** Each gradient/value-gradient call for $f$ and each proximal call for $h$ costs one; $T=N_G+N_P$.

**Status.** Optimal

**Lower bound.** B6, B13

$$
c\log(\Delta/\varepsilon)
$$

**Upper bound.** B1, B9

$$
C\log(\Delta/\varepsilon)
$$

**Gap or comparison.** $C$

### R5 - Complete-objective curvature at least the smooth-part constant

**Region.** $\mu\ge\beta>0,\quad\varepsilon\le c\Delta$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** Each gradient/value-gradient call for $f$ and each proximal call for $h$ costs one; $T=N_G+N_P$.

**Status.** Optimal

**Lower bound.** B7, B14

$$
c[1+\log(\Delta/\varepsilon)/\log(1+\mu/\beta)]
$$

**Upper bound.** B3, B11

$$
C[1+\log(\Delta/\varepsilon)/\log(1+\mu/\beta)]
$$

**Gap or comparison.** $C$

### R6 - Zero-query strongly convex regime

**Region.** $\varepsilon\ge\Delta$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** Each gradient/value-gradient call for $f$ and each proximal call for $h$ costs one; $T=N_G+N_P$.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B8, B15

$$
0
$$

### R7 - Strong convexity with $\kappa\ge4$

**Region.** $\kappa\ge4,\quad\varepsilon\le c\Delta$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** Each gradient/value-gradient call for $f$ and each proximal call for $h$ costs one; $T=N_G+N_P$.

**Status.** Other quantified gap

**Lower bound.** B12, B13

$$
c\max\{\min\{\sqrt d,H_\varepsilon\},\log(\Delta/\varepsilon)\}
$$

**Upper bound.** B9, B10

$$
C\min\{H_\varepsilon,1+d\log(2+\kappa\Delta/\varepsilon)\}
$$

**Gap or comparison.** $\frac{C\min\{H_\varepsilon,1+d\log(2+\kappa\Delta/\varepsilon)\}}{c\max\{\min\{\sqrt d,H_\varepsilon\},\log(\Delta/\varepsilon)\}}$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $\frac{C\min\{H_\varepsilon,1+d\log(2+\kappa\Delta/\varepsilon)\}}{c\max\{\min\{\sqrt d,H_\varepsilon\},\log(\Delta/\varepsilon)\}}$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Restarted accelerated gradient / proximal gradient

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\sqrt\kappa\log(\Delta/\varepsilon)
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [6](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\kappa\ge1,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge1,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

**Source location.** [1](https://www.tau.ac.il/~becka/FISTA.pdf) theorem: Theorem 4.4, printed p. 195, and Lemma 2.3

### B2 - Strong-convexity localization and cutting planes

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+d\log(2+\kappa\Delta/\varepsilon)]
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [6](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$0<\varepsilon\le c\Delta,\quad\mu,\beta>0$$

**Dimension conditions.** $0<\varepsilon\le c\Delta,\quad\mu,\beta>0$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

### B3 - Proximal contraction at small condition numbers

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\log(\Delta/\varepsilon)/\log(1+\mu/\beta)]
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [6](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\mu\ge\beta>0,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\mu\ge\beta>0,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

### B4 - Deterministic quadratic-chain reduction under strong convexity

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{d,H_\varepsilon\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.33360v2)

**Conditions.** $$\kappa\ge4,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge4,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/2609.33360v2) theorem: Theorem 2.3 and Appendix B.2, applied to the subclass $h=0$

### B5 - Random-matrix hard-instance reduction under strong convexity

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,H_\varepsilon\}
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$\kappa\ge4,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge4,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1 and equation (7), with $h=0$ so that the proximal map returns its input

### B6 - One-dimensional strongly convex localization hard instances

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(\Delta/\varepsilon)
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf)

**Conditions.** $$\kappa\ge1,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge1,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A4, A1

### B7 - Indistinguishability at small proximal condition numbers

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[1+\log(\Delta/\varepsilon)/\log(1+\mu/\beta)]
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf)

**Conditions.** $$\mu\ge\beta>0,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\mu\ge\beta>0,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A4, A1

### B8 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [6](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon\ge\Delta$$

**Dimension conditions.** $\varepsilon\ge\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

### B9 - Restarted accelerated gradient / proximal gradient

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\sqrt\kappa\log(\Delta/\varepsilon)
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [6](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\kappa\ge1,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge1,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

**Source location.** [1](https://www.tau.ac.il/~becka/FISTA.pdf) theorem: Theorem 4.4, printed p. 195, and Lemma 2.3

### B10 - Strong-convexity localization and cutting planes

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+d\log(2+\kappa\Delta/\varepsilon)]
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [6](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$0<\varepsilon\le c\Delta,\quad\mu,\beta>0$$

**Dimension conditions.** $0<\varepsilon\le c\Delta,\quad\mu,\beta>0$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

### B11 - Proximal contraction at small condition numbers

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\log(\Delta/\varepsilon)/\log(1+\mu/\beta)]
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [6](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\mu\ge\beta>0,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\mu\ge\beta>0,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

### B12 - Random-matrix hard-instance reduction under strong convexity

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,H_\varepsilon\}
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$\kappa\ge4,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge4,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1 and equation (7), with $h=0$ so that the proximal map returns its input

### B13 - One-dimensional strongly convex localization hard instances

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\log(\Delta/\varepsilon)
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf)

**Conditions.** $$\kappa\ge1,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa\ge1,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A4, A1

### B14 - Indistinguishability at small proximal condition numbers

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[1+\log(\Delta/\varepsilon)/\log(1+\mu/\beta)]
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf)

**Conditions.** $$\mu\ge\beta>0,\quad\varepsilon\le c\Delta$$

**Dimension conditions.** $\mu\ge\beta>0,\quad\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A4, A1

### B15 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [6](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon\ge\Delta$$

**Dimension conditions.** $\varepsilon\ge\Delta$

**Oracle correspondence.** Applicable interfaces: function values, gradients, and an exact proximal map, gradients and an exact proximal map. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

## 5. Local arguments

### A1 - Gradient-plus-proximal certificates

**Scope.** Unknown smooth gradient and exact proximal map of the specified convex term.

**Algorithm scope.** Deterministic upper witness; separate randomized gradient lower transfer.

Let $F=f+h$, with convex $\beta$-smooth $f$ and proper closed convex $h$. Define
$y=\operatorname{prox}_{h/\beta}(x-\nabla f(x)/\beta)$, $g=\beta(x-y)$.
Proximal optimality gives $g-\nabla f(x)\in\partial h(y)$. Adding its subgradient inequality to the convex smooth bound for $f$ yields
$$
F(y)-F(z)\le\langle g,x-z\rangle-\|g\|^2/(2\beta)
\quad(z\in\operatorname{dom}h).
$$
For $x,x^\star\in B(x_0,R)$, this gives $\|g\|\le4\beta R$ and a valid separating halfspace. Apply the centroid certificate and output the weighted combination of proximal points $y_i$, rather than the centers $x_i$. One gradient and one proximal call are used per round. Values of $f$ and $h$ are unnecessary.

For complete-objective strong convexity and initial gap $\Delta$, use radius $\sqrt{2\Delta/\mu}$. FISTA's convex error theorem plus this radius halves the gap in $O(\max\{1,\sqrt{\beta/\mu}\})$ iterations, giving the restarted bound.

Completing the square in the displayed inequality also gives
$$
F(y)-F^\star\le(\beta/2)\|x-x^\star\|^2
\le(\beta/\mu)(F(x)-F^\star).
$$
For $\mu\ge2\beta$, one step therefore contracts by $\beta/\mu$; for $\beta\le\mu\le2\beta$, use a constant-length accelerated restart. Together the budget is
$O(1+\log(\Delta/\epsilon)/\log(1+\mu/\beta))$.
The nested value-gradient construction with public quadratic $h$ gives the matching unknown-gradient lower bound. It does not imply a proximal-call lower bound.

**Limits of the argument.** The convex combination uses proximal points. No lower bound on proximal-call count is inferred.

**Sources.** [1](https://www.tau.ac.il/~becka/FISTA.pdf)

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

**Sources.** [4](https://arxiv.org/pdf/1405.4980) [5](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [6](https://arxiv.org/pdf/2609.20701)

### A3 - Descent, PL contraction, and zero-query endpoints

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

### A4 - A one-dimensional lower bound with exact values and gradients

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

[1] Amir Beck; Marc Teboulle. A Fast Iterative Shrinkage-Thresholding Algorithm for Linear Inverse Problems. 2009.

https://www.tau.ac.il/~becka/FISTA.pdf

[2] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 2026-09-09; preprintv1.

https://arxiv.org/pdf/2609.10874

[3] Yoel Drori. Exact oracle complexity for function-value suboptimality under weighted initial conditions. 2026-10-16; preprintv2.

https://arxiv.org/pdf/2609.33360v2

[4] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015.

https://arxiv.org/pdf/1405.4980

[5] Arkadi Nemirovski; Shmuel Onn; Uriel G. Rothblum. Accuracy Certificates for Computational Problems with Convex Structure. 2010.

https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf

[6] David Martínez-Rubio; Cristóbal Guzmán. Stable Movement for Nondual Lipschitz Convex Optimization: Efficiency and Nearly Optimal Oracle Rates. 2026-09-17; preprintv1.

https://arxiv.org/pdf/2609.20701
