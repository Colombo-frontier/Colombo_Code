# Exact coordinate subgradients: convex Lipschitz minimization

**Setting ID.** `SO_FO_CS01_csg`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Other quantified gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Convex body; geometry: Full space; smoothness: Lipschitz function

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Coordinate subgradient; operation: Coordinate subgradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Scalar oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}f(x)$$

### Admissible model

The unknown function $f:\mathbb R^d\to\mathbb R$ is globally convex and satisfies $|f(u)-f(v)|\le L\|u-v\|_2$. Both the feasible and query domains are the public box $Q=[-R/\sqrt d,R/\sqrt d]^d$. An instance also contains a measurable selector $s_f(x)\in\partial f(x)$ fixed before the run.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\ L,R,\varepsilon>0$$

### Oracle interface

Public numerical inputs: $d,\ R,\ \varepsilon$.

Public upper bounds: $L$.

The unknown object is the objective $f$.

For each query, the algorithm chooses $x\in Q$ and $j\in\{1,\ldots,d\}$ and receives one scalar coordinate response.

$$[s_f(x)]_j,\quad s_f(x)\in\partial f(x)$$

All coordinate responses at the same point come from the selector $s_f$ fixed before the run. The oracle cannot choose a different full subgradient after observing $j$.

Projection onto the public box and exact internal arithmetic are free. No coordinate line-minimization oracle is supplied.

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(f,\widehat{x})=f(\widehat{x})-\min_{x\in Q}f(x)$$

$f^\star=\inf_{x\in Q}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Deterministic / Pointwise guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\exists A\ \forall I,\ \ell(I,A^\mathcal{O}(I))\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\exists A\ \forall I,\ \mathbb{E}\ell(I,A^\mathcal{O}(I))\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f$: Unknown objective, with domain and structure specified by the model

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in Q}f(x)$$

$Q$: Feasible set of the task

$$Q(d,R)=[-R/\sqrt d,R/\sqrt d]^d$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial f(x)$: Ambient subdifferential of the corresponding convex function

$$\partial f(x)=\{g:f(u)\ge f(x)+\langle g,u-x\rangle\ \forall u\in\operatorname{dom}f\}$$

$s_f$: Measurable full-subgradient selector fixed before the run

$$s_f(x)\in\partial f(x)$$

$j$: Coordinate index selected by the algorithm **Domain:** $j\in\{1,\ldots,d\}$.

$d$: Dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the global Euclidean Lipschitz constant. **Domain:** $L>0$.

$R$: Euclidean circumradius of the public box or ball **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small absolute constant. A smaller common value may be chosen across theorems; no executable numerical threshold is supplied. **Domain:** $0<c<1$.

$C$: Sufficiently large absolute multiplicative constant, which may differ between formulas; not a numerical control parameter. **Domain:** $C>0$.

$\theta_0$: Universal accuracy threshold fixed in advance for the hidden-coordinate-sign hard family **Domain:** $0<\theta_0\le c$.

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

**Definition.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q5 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q6 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Nontrivial accuracy

**Region.** $0<\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Status.** Other quantified gap

**Lower bound.** B3

$$
cd\log(2+LR/\varepsilon)
$$

**Upper bound.** B1, B2

$$
Cd\min\{L^2R^2/\varepsilon^2,\ d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $O\!\left(\min\{(LR/\varepsilon)^2/\log(2+LR/\varepsilon),d\}\right)$

**Comparison argument.** The certified envelopes do not close uniformly in dimension and accuracy. Their ratio is not a proved separation between optimal algorithmic costs.

### R2 - One dimension

**Region.** $d=1,\quad0<\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q4

**Resource.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Status.** Optimal

**Lower bound.** B3, B7

$$
c\log(2+LR/\varepsilon)
$$

**Upper bound.** B2, B6

$$
C\log(2+LR/\varepsilon)
$$

**Gap or comparison.** $O(1)$

### R3 - Regime where cutting planes provide the smaller upper bound

**Region.** $(LR/\varepsilon)^2>d\log(2+LR/\varepsilon),\quad0<\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Status.** Polynomial gap

**Lower bound.** B3

$$
cd\log(2+LR/\varepsilon)
$$

**Upper bound.** B2

$$
Cd^2\log(2+LR/\varepsilon)
$$

**Gap or comparison.** $O(d)$

### R4 - Relative-accuracy slice fixed in advance

**Region.** $\varepsilon=\theta_0 LR,\quad0<\theta_0\le c\ \text{fixed in advance}$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q2; Q5

**Resource.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Status.** Optimal

**Lower bound.** B3, B7

$$
c d\log(2+\theta_0^{-1})
$$

**Upper bound.** B1, B5

$$
C\theta_0^{-2}d
$$

**Gap or comparison.** $O_{\theta_0}(1)$

### R5 - Accuracy asymptotics with dimension fixed in advance

**Region.** $d\ge2\ \text{fixed in advance},\quad0<\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q3; Q6

**Resource.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Status.** Optimal

**Lower bound.** B3, B7

$$
cd\log(2+LR/\varepsilon)
$$

**Upper bound.** B2, B6

$$
Cd^2\log(2+LR/\varepsilon)
$$

**Gap or comparison.** $O_d(1)$

### R6 - Zero-call center output

**Region.** $\varepsilon\ge LR$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q4

**Resource.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B4, B8

$$
0
$$

### R7 - Nontrivial accuracy

**Region.** $0<\varepsilon\le cLR$

**Views.** Randomized / Expected loss

**Quantity.** Q4

**Resource.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Status.** Other quantified gap

**Lower bound.** B7

$$
cd\log(2+LR/\varepsilon)
$$

**Upper bound.** B5, B6

$$
Cd\min\{L^2R^2/\varepsilon^2,\ d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $O\!\left(\min\{(LR/\varepsilon)^2/\log(2+LR/\varepsilon),d\}\right)$

**Comparison argument.** The certified envelopes do not close uniformly in dimension and accuracy. Their ratio is not a proved separation between optimal algorithmic costs.

### R8 - Regime where cutting planes provide the smaller upper bound

**Region.** $(LR/\varepsilon)^2>d\log(2+LR/\varepsilon),\quad0<\varepsilon\le cLR$

**Views.** Randomized / Expected loss

**Quantity.** Q4

**Resource.** One complete response to a query $(x,j)$ costs one call. The simultaneous function value in FCSG carries no additional charge.

**Status.** Polynomial gap

**Lower bound.** B7

$$
cd\log(2+LR/\varepsilon)
$$

**Upper bound.** B6

$$
Cd^2\log(2+LR/\varepsilon)
$$

**Gap or comparison.** $O(d)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Projected subgradient descent with complete coordinate scans

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
CdL^2R^2/\varepsilon^2
$$

**Sources.** [1](https://arxiv.org/pdf/1405.4980) [2](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: function value and one coordinate of a subgradient, one coordinate of a subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

**Source location.** [1](https://arxiv.org/pdf/1405.4980) theorem: Theorem 3.2; the complete-scan conversion is supplied in the local coordinate-simulation proof

### B2 - Centroid method with complete coordinate scans

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
Cd^2\log(2+LR/\varepsilon)
$$

**Sources.** [2](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [1](https://arxiv.org/pdf/1405.4980) [3](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: function value and one coordinate of a subgradient, one coordinate of a subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

**Source location.** [2](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) theorem: Proposition 2.1(ii), PDF p. 5; the volume argument is given in the local cutting-plane proof

### B3 - Lower bound against arbitrary randomized coordinate-subgradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cd\log(2+LR/\varepsilon)
$$

**Conditions.** $$0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one coordinate of a subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A4

### B4 - Return the center with zero queries

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://arxiv.org/pdf/1405.4980) [2](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon\ge LR$$

**Dimension conditions.** $\varepsilon\ge LR$

**Oracle correspondence.** Applicable interfaces: function value and one coordinate of a subgradient, one coordinate of a subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

### B5 - Projected subgradient descent with complete coordinate scans

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
CdL^2R^2/\varepsilon^2
$$

**Sources.** [1](https://arxiv.org/pdf/1405.4980) [2](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: function value and one coordinate of a subgradient, one coordinate of a subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

**Source location.** [1](https://arxiv.org/pdf/1405.4980) theorem: Theorem 3.2; the complete-scan conversion is supplied in the local coordinate-simulation proof

### B6 - Centroid method with complete coordinate scans

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
Cd^2\log(2+LR/\varepsilon)
$$

**Sources.** [2](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [1](https://arxiv.org/pdf/1405.4980) [3](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: function value and one coordinate of a subgradient, one coordinate of a subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

**Source location.** [2](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) theorem: Proposition 2.1(ii), PDF p. 5; the volume argument is given in the local cutting-plane proof

### B7 - Lower bound against arbitrary randomized coordinate-subgradient algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cd\log(2+LR/\varepsilon)
$$

**Conditions.** $$0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one coordinate of a subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A4

### B8 - Return the center with zero queries

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://arxiv.org/pdf/1405.4980) [2](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon\ge LR$$

**Dimension conditions.** $\varepsilon\ge LR$

**Oracle correspondence.** Applicable interfaces: function value and one coordinate of a subgradient, one coordinate of a subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2, A3

## 5. Local arguments

### A1 - Exact and noisy coordinate scans

**Scope.** A selector coherent across all coordinates at a point; fixed variance allocations in the noisy model.

**Algorithm scope.** Deterministic scan and averaging policies, including when observations are random.

At a fixed point, every coordinate response comes from the same measurable full-subgradient selector $s_f(x)$, fixed before the run. Scanning all $d$ coordinates therefore reconstructs a legal subgradient in $d$ calls. Projected, weighted strongly convex, and centroid-certificate methods transfer with that multiplier.

For noisy coordinates, conditional means are $s_f(x)_j$, with fixed variance budgets $\sigma_j^2$ satisfying $\sum_j\sigma_j^2\le\sigma^2$. Keep the point fixed through the scan. Iterated expectation gives
$$
\mathbb E\widehat g=s_f(x),\qquad
\mathbb E\|\widehat g-s_f(x)\|^2
=\sum_j\mathbb E|\widehat g_j-s_f(x)_j|^2\le\sigma^2.
$$
Cross-coordinate independence is unnecessary for this sum of squares. Total second moment is at most $L^2+\sigma^2$, so the projected bounds apply. Every scan costs $d$. A deterministic scan and weighted output remain deterministic policies despite observation noise.

At zero noise use the smallest applicable exact upper bound, including the certificate. At $\epsilon\ge LR$, the center suffices without sampling.

For public separability $f=\sum_j\phi_j(x_j)$, with coordinate Lipschitz constants at most $L/\sqrt d$, subgradient signs permit bisection. Shrink each interval to length $\epsilon/(L\sqrt d)$, giving component error at most $\epsilon/d$. Total cost is $O(d\log(2+LR/\epsilon))$. The algorithm remains valid under strong convexity but requires the declared separability assumption.

**Limits of the argument.** Coordinate-dependent replacement of the full selector invalidates the simulation. Separable bisection requires public separability.

### A2 - Projected and weighted subgradient bounds

**Scope.** Public Euclidean projection; unbiased conditional subgradient mean and a total second-moment bound, or exact subgradients.

**Algorithm scope.** Deterministic policies and deterministic averages; randomness may come from observations.

Projection onto a public closed convex set gives
$$
\|x_{t+1}-x^\star\|^2\le\|x_t-x^\star\|^2
-2\eta_t\langle g_t,x_t-x^\star\rangle+\eta_t^2\|g_t\|^2.
$$
For convex $f$, initial distance at most $R$, and conditional second moment at most $V$, the constant step $R/\sqrt{VK}$ and averaged output have expected gap at most $R\sqrt{V/K}$. Exact subgradients correspond to $V=L^2$.

Under $\mu$-strong convexity, use $\eta_t=2/[\mu(t+1)]$. With $a_t=\mathbb E\|x_t-x^\star\|^2$,
$$
\mathbb E[f(x_t)-f^\star]\le{\mu(t-1)\over4}a_t
-{\mu(t+1)\over4}a_{t+1}+{V\over\mu(t+1)}.
$$
Multiply by $t$, sum, and use convexity. The weighted output
$\sum_{t=1}^K2t\,x_t/[K(K+1)]$ has expected gap at most $2V/[\mu(K+1)]$. Neither output rule requires private randomness. Apply norm conversion before these inequalities, preserving all dimension factors.

**Limits of the argument.** Norm-conversion factors must be applied explicitly. No noisy cutting-plane result follows from this recursion.

### A3 - Subgradient certificates and centroid cuts

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

**Sources.** [1](https://arxiv.org/pdf/1405.4980) [2](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/2609.20701)

### A4 - Information trees for coordinate subgradients

**Scope.** Pure coordinate subgradient feedback from one fixed selector; box geometry.

**Algorithm scope.** Lower bounds against arbitrary randomized adaptive algorithms.

On $Q=[-R/\sqrt d,R/\sqrt d]^d$, choose $v$ uniformly in $Q$ and
$$
f_v(x)=(L/\sqrt d)\sum_j|x_j-v_j|.
$$
The fixed coordinate selector returns one sign bit, except at probability-zero ties. Conditional on a private seed, $T$ adaptive calls give at most $2^T$ leaves. An $\epsilon$-accurate output requires
$\|\widehat x-v\|_1\le\epsilon\sqrt d/L$.
The volume of this ball relative to the prior box is
$(d\epsilon/(LR))^d/d!\le(e\epsilon/(LR))^d$.
Thus success probability is at most
$2^T(e\epsilon/(LR))^d$.
A constant success probability needs $\Omega(d\log(LR/\epsilon))$ calls in the stated accuracy window. Averaging over private seeds preserves the bound; Markov converts expected error to constant-probability accuracy.

For strong convexity with $\mu R\le L/4$, let $r=R/\sqrt d$, choose $v$ uniformly in $[-r/2,r/2]^d$, and set
$$
f_v(x)=\mu\|x\|^2/2+(L/(2\sqrt d))\sum_j|x_j-v_j|
\quad(x\in Q).
$$
Its minimizer is $v$, and
$f_v(x)-f_v(v)\ge(3L/(8\sqrt d))\|x-v\|_1$.
Subtracting the known quadratic leaves a sign bit. Clipping the quadratic derivative outside each interval gives a globally convex Lipschitz extension with subgradient norm at most $\mu R+L/2\le3L/4$.

These instances are separable. They also belong to the noisy model at zero noise. Their bit-counting proof does not transfer to value-augmented coordinate access.

**Limits of the argument.** Exact function values can reveal additional information. The strong-convexity branch requires the stated slack.

## References

[1] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015.

https://arxiv.org/pdf/1405.4980

[2] Arkadi Nemirovski; Shmuel Onn; Uriel G. Rothblum. Accuracy Certificates for Computational Problems with Convex Structure. 2010.

https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf

[3] David Martínez-Rubio; Cristóbal Guzmán. Stable Movement for Nondual Lipschitz Convex Optimization: Efficiency and Nearly Optimal Oracle Rates. 2026-09-17; preprintv1.

https://arxiv.org/pdf/2609.20701
