# Smooth minimization with coordinate gradients: initial-distance bound for a convex objective; one coordinate of the gradient

**Setting ID.** `SO_FO_O01_cv`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Coordinate smoothness

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Coordinate gradient; operation: Coordinate gradient; public information: Hidden objects explicitly declared; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic algorithms; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Scalar oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

The unknown differentiable convex function $f$ satisfies $|\partial_jf(x+te_j)-\partial_jf(x)|\le b_j|t|$ for every coordinate. A minimizer exists with $\|x_0-x^\star\|_2\le R$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Each coordinate-smoothness constant controls derivative variation along its own coordinate line. An individual $b_j$ is not a Lipschitz constant for the full gradient.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad b_j>0\quad(1\le j\le d),\quad R > 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ (b_j)_{j=1}^d,\ R,\ \varepsilon,\ x_0$.

The unknown object is the objective $f$.

For each query, the algorithm chooses $x\in\mathbb R^d$ and $j\in\{1,\ldots,d\}$ and receives one scalar coordinate response.

$$\partial_j f(x)$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=f(\widehat{x})-f^\star$$

$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One scalar partial derivative at an algorithm-selected pair $(x,j)$ costs one unit. A full gradient at one point costs $d$. No coordinate-update or span restriction is imposed.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Deterministic / Pointwise guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f$: Unknown objective, with domain and structure specified by the model

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$x^\star$: A global minimizer whose existence is promised by the model; unique under strong convexity

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$e_j$: $j$th standard basis vector **Domain:** $j\in\{1,\ldots,d\}$.

$\partial_j f$: The $j$th coordinate derivative of a differentiable function, returned as a scalar

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$(b_j)_{j=1}^d$: Public vector of positive coordinate-smoothness constants; numerical evaluation must support vector parameters. **Domain:** $b_j>0$.

$b$: Common coordinate smoothness constant on the equal-constants slice. **Domain:** $b>0$.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$\beta_{\rm sum}$: Sum of the coordinate smoothness constants; convexity makes this a valid full-gradient smoothness constant.

$$\beta_{\rm sum}=\sum_{j=1}^d b_j$$

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

$S_b$: The sum of square roots $\sum_j\sqrt{b_j}$ is a derived quantity only.

$$S_b=\sum_{j=1}^d\sqrt{b_j}$$

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar partial derivative at an algorithm-selected pair $(x,j)$ costs one unit. A full gradient at one point costs $d$. No coordinate-update or span restriction is imposed.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar partial derivative at an algorithm-selected pair $(x,j)$ costs one unit. A full gradient at one point costs $d$. No coordinate-update or span restriction is imposed.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar partial derivative at an algorithm-selected pair $(x,j)$ costs one unit. A full gradient at one point costs $d$. No coordinate-update or span restriction is imposed.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Convex initial-distance contract

**Region.** $b_j>0,\quad R>0,\quad\varepsilon>0$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One scalar partial derivative at an algorithm-selected pair $(x,j)$ costs one unit. A full gradient at one point costs $d$. No coordinate-update or span restriction is imposed.

**Status.** Other quantified gap

**Lower bound.** B11, B14

$$
\begin{cases}0,&\varepsilon\ge\beta_{\rm sum}R^2/2,\\\max\{1,3d/4\},&b_j=b\ (\forall j),\ 0<\varepsilon\le bR^2/8,\\1,&\text{otherwise}.\end{cases}
$$

**Upper bound.** B1, B2, B10

$$
\begin{cases}0,&\varepsilon\ge\beta_{\rm sum}R^2/2,\\\min\{Cd^2\log(2+\beta_{\rm sum}R^2/\varepsilon),CdR\sqrt{\beta_{\rm sum}/\varepsilon}\},&0<\varepsilon<\beta_{\rm sum}R^2/2.\end{cases}
$$

**Gap or comparison.** Exact C*=0 for epsilon>=beta_sum R^2/2, with ratio inapplicable. Below it, divide the unchanged upper minimum by max{1,3d/4} on r7 and by 1 elsewhere. The dimension-dependent improvement is strict for d>=2 on r7; positive-cost gaps remain.

**Comparison argument.** Retain the original upper and zero-query branches conditionally. FO_COORDINATE_DIAGONAL_DET_Q1 applies the retained diagonal-information inequality to deterministic pointwise algorithms and yields 3d/4 scalar calls on r7, including epsilon=bR^2/8. Since beta_sum=db there, r7 is disjoint from epsilon>=beta_sum R^2/2. The resulting lower is max{1,3d/4} on r7 and one elsewhere below the zero-query threshold. The stored b3 and b4 retain quantity q2 and are excluded from this q1 bracket; no identity merger is used.

### R2 - Full-gradient transfer window with equal coordinate constants

**Region.** $d\ge CbR^2/\varepsilon$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One scalar partial derivative at an algorithm-selected pair $(x,j)$ costs one unit. A full gradient at one point costs $d$. No coordinate-update or span restriction is imposed.

**Status.** Other quantified gap

**Lower bound.** B8, B9, B13

$$
\max\{cd,cR\sqrt{b/\varepsilon},1\}
$$

**Upper bound.** B5, B6, B7

$$
\min\{C(1+RS_b/\sqrt\varepsilon),Cd^2\log(2+\beta_{\rm sum}R^2/\varepsilon),CdR\sqrt{\beta_{\rm sum}/\varepsilon}\}
$$

**Gap or comparison.** $\frac{\min\{C(1+RS_b/\sqrt\varepsilon),Cd^2\log(2+\beta_{\rm sum}R^2/\varepsilon),CdR\sqrt{\beta_{\rm sum}/\varepsilon}\}}{\max\{cd,cR\sqrt{b/\varepsilon},1\}}$

**Comparison argument.** Compare on the intersection of O01.cv-R.parameter-domain and O01.cv-uniform-hd. The all-dimensional $\Omega(d)$ coordinate-information lower bound strengthens the bound obtained by full-gradient simulation alone. A matching full-parameter lower bound for arbitrary queries is still unavailable. FO_COORDINATE_ZERO_QUERY adds the compatible one-call lower bound. Since this regime has b_j=b and epsilon<=c bR^2 with the baseline universal c chosen <=1/8 as permitted by FO_COORDINATE_SMOOTH, epsilon<beta_sum R^2/2. Hence the zero-query upper branch is disjoint from this comparison.

### R3 - Convex initial-distance contract

**Region.** $b_j>0,\quad R>0,\quad\varepsilon>0$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One scalar partial derivative at an algorithm-selected pair $(x,j)$ costs one unit. A full gradient at one point costs $d$. No coordinate-update or span restriction is imposed.

**Status.** Other quantified gap

**Lower bound.** B13, B8, B9

$$
\begin{cases}0,&\varepsilon\ge\beta_{\rm sum}R^2/2,\\\max\{1,cd,cR\sqrt{b/\varepsilon}\},&r4,\\\max\{1,cd\},&r3\setminus r4,\\1,&\text{otherwise}.\end{cases}
$$

**Upper bound.** B5, B6, B7, B12

$$
\begin{cases}0,&\varepsilon\ge\beta_{\rm sum}R^2/2,\\\min\{C(1+RS_b/\sqrt\varepsilon),Cd^2\log(2+\beta_{\rm sum}R^2/\varepsilon),CdR\sqrt{\beta_{\rm sum}/\varepsilon}\},&0<\varepsilon<\beta_{\rm sum}R^2/2.\end{cases}
$$

**Gap or comparison.** Exact C*=0 for epsilon>=beta_sum R^2/2; no 0/0 ratio. Strictly below the threshold, the multiplicative gap is the displayed positive upper envelope divided by the displayed positive lower envelope.

**Comparison argument.** FO_COORDINATE_ZERO_QUERY proves exact cost zero when epsilon>=beta_sum R^2/2, including equality, and a one-call lower bound strictly below it. The original upper minimum applies below the threshold. Positive-accuracy rates remain unmatched. Here r3 and r4 denote SO_FO_O01_cv__randomized__expected_loss__r3 and SO_FO_O01_cv__randomized__expected_loss__r4. Existing lower bounds contribute only on those guarded slices; outside them the one-call lower applies below the threshold. The baseline's sufficiently small universal c can be chosen <=1/8 as in FO_COORDINATE_SMOOTH; thus the equal-constants slices do not overlap the zero-query branch. Different theorem constants retain their baseline convention.

### R4 - Exact zero-query coordinate-smooth endpoint

**Region.** $\varepsilon\ge\beta_{\rm sum}R^2/2$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One scalar partial derivative at an algorithm-selected pair $(x,j)$ costs one unit. A full gradient at one point costs $d$. No coordinate-update or span restriction is imposed.

**Status.** Optimal

**Lower bound.** B11

$$
0
$$

**Upper bound.** B10

$$
0
$$

**Gap or comparison.** Exact minimized scalar-call cost0 on the entire declared r6, including equality; multiplicative ratio inapplicable.

**Comparison argument.** FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

### R5 - Exact zero-query coordinate-smooth endpoint

**Region.** $\varepsilon\ge\beta_{\rm sum}R^2/2$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One scalar partial derivative at an algorithm-selected pair $(x,j)$ costs one unit. A full gradient at one point costs $d$. No coordinate-update or span restriction is imposed.

**Status.** Optimal

**Lower bound.** B13

$$
0
$$

**Upper bound.** B12

$$
0
$$

**Gap or comparison.** Exact minimized scalar-call cost0 on the entire declared r6, including equality; multiplicative ratio inapplicable.

**Comparison argument.** FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

## 4. Bounds and supporting evidence

### B1 - Finite-dimensional cutting planes with $d$ coordinate calls per full gradient

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
Cd^2\log(2+\beta_{\rm sum}R^2/\varepsilon)
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980) [4](https://arxiv.org/pdf/2101.09740v2) [5](https://arxiv.org/pdf/2609.33360v2) [6](https://arxiv.org/pdf/2609.10874) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [8](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$b_j>0,\quad R>0,\quad\varepsilon>0$$

**Dimension conditions.** $b_j>0,\quad R>0,\quad\varepsilon>0$

**Oracle correspondence.** Applicable interfaces: one coordinate of the gradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_COORDINATE_SMOOTH, FO_SMOOTH_LOCALIZATION, FO_CERTIFICATE

### B2 - Accelerated full-gradient simulation with $d$ coordinate calls per gradient

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
CdR\sqrt{\beta_{\rm sum}/\varepsilon}
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980) [4](https://arxiv.org/pdf/2101.09740v2) [5](https://arxiv.org/pdf/2609.33360v2) [6](https://arxiv.org/pdf/2609.10874) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [8](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$b_j>0,\quad R>0,\quad\varepsilon>0$$

**Dimension conditions.** $b_j>0,\quad R>0,\quad\varepsilon>0$

**Oracle correspondence.** Applicable interfaces: one coordinate of the gradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_COORDINATE_SMOOTH, FO_SMOOTH_LOCALIZATION, FO_CERTIFICATE

### B3 - Hidden independent coordinate signs

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cd
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980) [4](https://arxiv.org/pdf/2101.09740v2) [5](https://arxiv.org/pdf/2609.33360v2) [6](https://arxiv.org/pdf/2609.10874) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [8](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$b_j=b\ (\forall j),\quad\varepsilon\le cbR^2$$

**Dimension conditions.** $b_j=b\ (\forall j),\quad\varepsilon\le cbR^2$

**Oracle correspondence.** Applicable interfaces: one coordinate of the gradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_COORDINATE_SMOOTH, FO_SMOOTH_LOCALIZATION, FO_CERTIFICATE

### B4 - Transfer from a stronger full-gradient interface

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cR\sqrt{b/\varepsilon}
$$

**Sources.** [1](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$d\ge CbR^2/\varepsilon$$

**Dimension conditions.** $d\ge CbR^2/\varepsilon$

**Oracle correspondence.** Applicable interfaces: one coordinate of the gradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [1](https://arxiv.org/pdf/2609.10874) theorem: Theorem1, quadratic reduction p.3, Eq.(7) dimension O(T²)

### B5 - NU-ACDM

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C(1+RS_b/\sqrt\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/1512.09103)

**Conditions.** $$b_j>0,\quad R>0,\quad\varepsilon>0$$

**Dimension conditions.** $b_j>0,\quad R>0,\quad\varepsilon>0$

**Oracle correspondence.** Applicable interfaces: one coordinate of the gradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [2](https://arxiv.org/pdf/1512.09103) theorem: Theorems5.1,6.1; full PDF pp.9,13

### B6 - Finite-dimensional cutting planes with $d$ coordinate calls per full gradient

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
Cd^2\log(2+\beta_{\rm sum}R^2/\varepsilon)
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980) [4](https://arxiv.org/pdf/2101.09740v2) [5](https://arxiv.org/pdf/2609.33360v2) [6](https://arxiv.org/pdf/2609.10874) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [8](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$b_j>0,\quad R>0,\quad\varepsilon>0$$

**Dimension conditions.** $b_j>0,\quad R>0,\quad\varepsilon>0$

**Oracle correspondence.** Applicable interfaces: one coordinate of the gradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_COORDINATE_SMOOTH, FO_SMOOTH_LOCALIZATION, FO_CERTIFICATE

### B7 - Accelerated full-gradient simulation with $d$ coordinate calls per gradient

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
CdR\sqrt{\beta_{\rm sum}/\varepsilon}
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980) [4](https://arxiv.org/pdf/2101.09740v2) [5](https://arxiv.org/pdf/2609.33360v2) [6](https://arxiv.org/pdf/2609.10874) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [8](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$b_j>0,\quad R>0,\quad\varepsilon>0$$

**Dimension conditions.** $b_j>0,\quad R>0,\quad\varepsilon>0$

**Oracle correspondence.** Applicable interfaces: one coordinate of the gradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_COORDINATE_SMOOTH, FO_SMOOTH_LOCALIZATION, FO_CERTIFICATE

### B8 - Hidden independent coordinate signs

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cd
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980) [4](https://arxiv.org/pdf/2101.09740v2) [5](https://arxiv.org/pdf/2609.33360v2) [6](https://arxiv.org/pdf/2609.10874) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [8](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$b_j=b\ (\forall j),\quad\varepsilon\le cbR^2$$

**Dimension conditions.** $b_j=b\ (\forall j),\quad\varepsilon\le cbR^2$

**Oracle correspondence.** Applicable interfaces: one coordinate of the gradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_COORDINATE_SMOOTH, FO_SMOOTH_LOCALIZATION, FO_CERTIFICATE

### B9 - Transfer from a stronger full-gradient interface

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cR\sqrt{b/\varepsilon}
$$

**Sources.** [1](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$d\ge CbR^2/\varepsilon$$

**Dimension conditions.** $d\ge CbR^2/\varepsilon$

**Oracle correspondence.** Applicable interfaces: one coordinate of the gradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [1](https://arxiv.org/pdf/2609.10874) theorem: Theorem1, quadratic reduction p.3, Eq.(7) dimension O(T²)

### B10 - Return the public initial point x0

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980)

**Conditions.** $b_j>0,\ R>0,\ d\ge1,\ \varepsilon\ge\beta_{\rm sum}R^2/2$

**Dimension conditions.**

$$
All d>=1.
$$

**Oracle correspondence.** No oracle response or additional capability is used.

**Guarantee conversion.** Objective gap <=epsilon on every admissible instance; consequently expected gap <=epsilon.

**Output rule.** Return the public x0 in R^d; unqueried output is permitted.

**Resource conversion.** Exactly zero scalar coordinate-derivative calls on every path.

**Local argument.** FO_COORDINATE_ZERO_QUERY

### B11 - Opposite rank-one quadratic translations and integer query counting

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathbf{1}_{\{\varepsilon<\beta_{\rm sum}R^2/2\}}
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980)

**Conditions.** $b_j>0,\ R>0,\ d\ge1,\ \varepsilon>0$

**Dimension conditions.** All d>=1; one strictly below beta_sum R^2/2, zero at and above it.

**Oracle correspondence.** The no-query transcript cannot distinguish two fixed admissible quadratics. Arbitrary adaptive queries remain allowed.

**Guarantee conversion.** The two fixed-instance expected gaps average to at least beta_sum R^2/2. This covers randomized expected loss and deterministic pointwise guarantees.

**Output rule.** Any unqueried output in R^d, including a privately randomized output.

**Resource conversion.** A worst-path budget below one permits no call on any path. No expected-work conversion is used.

**Local argument.** FO_COORDINATE_ZERO_QUERY

### B12 - Return the public initial point x0

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980)

**Conditions.** $b_j>0,\ R>0,\ d\ge1,\ \varepsilon\ge\beta_{\rm sum}R^2/2$

**Dimension conditions.**

$$
All d>=1.
$$

**Oracle correspondence.** No oracle response or additional capability is used.

**Guarantee conversion.** Objective gap <=epsilon on every admissible instance; consequently expected gap <=epsilon.

**Output rule.** Return the public x0 in R^d; unqueried output is permitted.

**Resource conversion.** Exactly zero scalar coordinate-derivative calls on every path.

**Local argument.** FO_COORDINATE_ZERO_QUERY

### B13 - Opposite rank-one quadratic translations and integer query counting

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathbf{1}_{\{\varepsilon<\beta_{\rm sum}R^2/2\}}
$$

**Sources.** [3](https://arxiv.org/pdf/1405.4980)

**Conditions.** $b_j>0,\ R>0,\ d\ge1,\ \varepsilon>0$

**Dimension conditions.** All d>=1; one strictly below beta_sum R^2/2, zero at and above it.

**Oracle correspondence.** The no-query transcript cannot distinguish two fixed admissible quadratics. Arbitrary adaptive queries remain allowed.

**Guarantee conversion.** The two fixed-instance expected gaps average to at least beta_sum R^2/2. This covers randomized expected loss and deterministic pointwise guarantees.

**Output rule.** Any unqueried output in R^d, including a privately randomized output.

**Resource conversion.** A worst-path budget below one permits no call on any path. No expected-work conversion is used.

**Local argument.** FO_COORDINATE_ZERO_QUERY

### B14 - Explicit diagonal-information derivation for the deterministic q1 target

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\frac{3d}{4}
$$

**Conditions.** $d\ge1,\ R>0,\ b_j=b>0\ (\forall j),\ 0<\varepsilon\le bR^2/8$

**Dimension conditions.** Every integer d>=1; no high-dimensional restriction.

**Oracle correspondence.** Only partial_j f(x) at arbitrary adaptive (x,j); the hard family preserves precisely this oracle.

**Guarantee conversion.** The retained randomized Bayes-risk inequality implies the bound for every deterministic algorithm satisfying the pointwise g1 guarantee, as proved explicitly.

**Output rule.** Any returned point in R^d, queried or unqueried, is covered.

**Resource conversion.** Worst-path number of scalar coordinate responses, including repetitions and initialization; no expected-work conversion.

**Local argument.** FO_COORDINATE_DIAGONAL_DET_Q1, FO_COORDINATE_SMOOTH

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: e6aa59989e04603ada47f5c510b7dab12b8d730d7fe862f24c51a09f66bd7ac1

### Native proof: FO_COORDINATE_SMOOTH

Native pointer: /proofs/0; canonical SHA-256: 908b109d57b75d57bc2f95589983adf234dfba1d4abcf2751dbf47d27f8f8b61

#### Native field: algorithm_scope

Native pointer: /proofs/0/algorithm_scope; canonical SHA-256: 6b84baa0e326be71ea8dc859c58d9040e2d7783923cd51c8904564a2559372aa

Deterministic simulated-gradient upper witnesses; arbitrary randomized diagonal-information lower bound.

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: f9b14c6e6e9f102e1fc5f2358784da026820d2b9cdefb190d2fab84e537938be

Convex differentiability and coordinate smoothness constants $b_j$ imply full-gradient smoothness at most $\beta_{\rm sum}=\sum_jb_j$. For $C^2$ functions the positive semidefinite Hessian has diagonal at most $b_j$, and largest eigenvalue at most its trace. Convex smoothing and a limit give the differentiable case. A full gradient costs $d$ coordinate calls, so full-gradient acceleration and certificates acquire a factor $d$.

For equal constants, let independent signs define $v_j=\pm R/\sqrt d$, and put $f_v(x)=b\|x-v\|^2/2$. A scalar coordinate derivative reveals only that coordinate's sign. Conditional on any adaptive history, unqueried signs remain uniform. The Bayes expected gap after $T$ calls is at least
$$
(bR^2/2)(1-T/d).
$$
Error at most $bR^2/8$ requires $T\ge3d/4$. For initial gap $\Delta$, use
$v_j=\pm\sqrt{2\Delta/(bd)}$, obtaining residual
$\Delta(1-T/d)$. At $\epsilon\le\Delta/4$, the cost is $\Omega(d)$. The construction is $\mu$-strongly convex if $\mu\le b$.

This permits arbitrary randomized adaptive query points and outputs. It is specific to scalar coordinate derivatives; exact function values can encode additional information.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: a6fca0ac8fd987b56435636d370c6030ac649832762ca7eeb124883b0f1f0be2

The diagonal lower bound is on the equal-constants slice and does not extend automatically to value-augmented feedback.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 41f841bd94e9da7ce8b93c34c415f2bad0dee707b467c419def56f75dcc6aa39

One scalar partial derivative per query for a convex differentiable function.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: b473b9c587a11c7390e7c462836a57d9929d635333d351440fe501c3f5087ab2

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 9044dab56717e0435b18f3d52502c841bf45fbe4cbf91b1f95aee818f75cfcea

Coordinate smoothness and diagonal-quadratic information

### Native proof: FO_SMOOTH_LOCALIZATION

Native pointer: /proofs/1; canonical SHA-256: d51e14f76ae353f6d19ce8eac55c09c21cbd9eeee4bde8c3512c390a396b37e6

#### Native field: algorithm_scope

Native pointer: /proofs/1/algorithm_scope; canonical SHA-256: 7d91225f61bb29b37b94da2479bd65ed049edd57456242e4b2feaba37b16801c

Deterministic upper witnesses; imported lower theorems retain their own deterministic or randomized scopes.

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 8d4b35132c83602585f4977b5887a155d8f4ccd965bf6b5d2a12f65821daa109

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

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: d8794705c35ea24420b14f01cb7ff119c9c7926bf6951f1e120b77780dc03ef9

An arbitrary constrained minimizer may be on the boundary and need not have zero gradient. Fixed-dimensional lower transfers retain theorem dimension windows.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 3091ece9e2f7dce20041b0906cf893c2f7d027b16d3bad6d85399aa55c7a8419

Gradient access and a public ball localizing a global minimizer; public regularization when only initial gap is given.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 036d6bc31f87b5cca6c3679c2830d0b97c8176e2e9c43ff6000cdb083679bd61

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: 559a56b1b57844e3c568387a9ebb4d7cbcaf1e98ec7a31a094efd65fa367c08c

SO_SRC_3db9732ed66f3b8c

#### Native item 2

Native pointer: /proofs/1/source_refs/1; canonical SHA-256: a2cd77f7d9b231a6aa4b43e047274fe80a546f2eda06c8b43f4f125d862ff120

SO_SRC_c729895b420a5000

#### Native item 3

Native pointer: /proofs/1/source_refs/2; canonical SHA-256: 9aa4cfa7d9a55fe74b6acccc9d4369f9379589cff2486fc75a9d717fcb9aa355

SO_SRC_da45f3a56f11d157

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 3aae5cd443abef7955dd04a6655608cb10b6395f3b12c8a62a5f8214e01daa22

Smooth localization and gradient-norm conversion

### Native proof: FO_CERTIFICATE

Native pointer: /proofs/2; canonical SHA-256: 21979664af3d9c988ec0425d315ce0b043b36ff9d545026ed3322eb72c59ff61

#### Native field: algorithm_scope

Native pointer: /proofs/2/algorithm_scope; canonical SHA-256: 42d065ebafc108a64e9cee964510776065fd1792b4344749b3f72a002ccd46aa

Deterministic upper-bound witness; valid as an upper bound for randomized views.

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: 72d8341a17456c969432c1e806fc1bc7998d07720b92420071af653c600ce2eb

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

#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: 3c41670d63fc68cbd9a2b20c5bdffe5abdf747751c9b855a1dcef06421a036cd

The stable-selector branch imports its movement theorem and does not claim efficient deterministic arithmetic time.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 92d674be8fd361e7686d71fa4f979260ea491c9b015664334a0ec353e8059b63

One full subgradient is sufficient. Public compact convex geometry and exact internal geometric computation are available.

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: 6920d63b36e4e336e449c0c507724c9a8e022e16823935878f5a8459ea8654b1

#### Native item 1

Native pointer: /proofs/2/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native item 2

Native pointer: /proofs/2/source_refs/1; canonical SHA-256: 9daedb2ac95e8088053c7f30d00e8b484004c953b15791fc665f3978350e6bba

SO_SRC_c314bae252a3b929

#### Native item 3

Native pointer: /proofs/2/source_refs/2; canonical SHA-256: f49cfd2461dd4b0132f4f0fa2a90e3f29883781b5ad0bff19390f24edc0bff0c

SO_SRC_88e665bbd463b203

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: a3ebc976e1b51b6b06145bd0666cc8cefdf1c282c07da23238d9b82f3a05b3cb

Subgradient certificates and centroid cuts

### Native proof: FO_COORDINATE_ZERO_QUERY

Native pointer: /proofs/3; canonical SHA-256: 7afc74d71b21bec486d4fb9b009ba565ebc0728ba84760f5870a24bb2fefeea8

#### Native field: algorithm_scope

Native pointer: /proofs/3/algorithm_scope; canonical SHA-256: 130319f07f7b06df972cfb7b04d807d870d1bb7064f3237c3ece6a73610728f8

Arbitrary deterministic algorithms and privately randomized algorithms with expected objective gap and worst-path scalar-query budgets.

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: 854f072dba3ac2c6d24258fac2f06ed5e9c28cfb3f41b21c769e72ba8881e90b

Let B=beta_sum=sum_j b_j. Integrating coordinate Lipschitz derivatives gives f(x+t e_j)<=f(x)+t partial_j f(x)+b_j t^2/2. For nonzero h define S_h=sum_j sqrt(b_j)|h_j| and theta_j=sqrt(b_j)|h_j|/S_h on its nonzero coordinates. Convexity applied to x+h=sum_j theta_j(x+(h_j/theta_j)e_j) gives f(x+h)<=f(x)+<grad f(x),h>+S_h^2/2<=f(x)+<grad f(x),h>+B||h||_2^2/2. At a global minimizer grad f(x*)=0, so f(x0)-f*<=BR^2/2. Returning x0 uses zero queries and meets both guarantees for epsilon>=BR^2/2. No Hessian, function value, or auxiliary oracle is used. This direct coordinate argument recovers the smooth descent inequality in Bubeck, arXiv:1405.4980v2 (2015), Lemma 3.4 and Eq.(3.4), PDF pp.40-41, characters [56200,60900), source hash 4d5cd5428a8e627fa2b7ee80791259c2f17e6ae5bf68cf7c78aee1fcefdc05f2. For sharpness, a separate local proof uses a_j=sqrt(b_j) and f_+(x)=0.5(a^T(x-x0)-R sqrt(B))^2, f_-(x)=0.5(a^T(x-x0)+R sqrt(B))^2. Both are admissible convex quadratics with coordinate constants exactly b_j, minimum zero, and minimizers x0 +/- R a/sqrt(B) at distance R. A no-query output X has the same distribution on both fixed instances. Their average expected gap equals 0.5 E[(a^T(X-x0))^2]+BR^2/2>=BR^2/2, so one fixed instance violates every epsilon<BR^2/2. Deterministic outputs are included. A worst-path budget below one permits zero calls on every path; thus C*>=1 strictly below the threshold, and globally C*>=1_{epsilon<BR^2/2}. At equality and above, nonnegative query counts and the zero-call upper give C*=0. A multiplicative ratio is asserted only strictly below the threshold; no 0/0 ratio is formed.

#### Native field: limitations

Native pointer: /proofs/3/limitations; canonical SHA-256: 7f464cff5c9c86bc5dfe42e7dafcdd37cbcb27ba53277ef94a02f46406e4edce

The one-call lower bound leaves the positive-accuracy dependence on dimension and heterogeneous constants unresolved.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: 269b4c5eae11f154d7e76c4747a82b57d37f438ec5269fe259636bf3137b6bab

Both fixed views, all d>=1, b_j>0, R>0 and epsilon>0.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: b473b9c587a11c7390e7c462836a57d9929d635333d351440fe501c3f5087ab2

#### Native item 1

Native pointer: /proofs/3/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: b3292ef722b871963bc625f19d7f56af1eb0130a2198b256e81b1dfd3af8d5f0

Sharp zero-query threshold for coordinate-smooth initial-distance minimization

### Native proof: FO_COORDINATE_DIAGONAL_DET_Q1

Native pointer: /proofs/4; canonical SHA-256: 0587037eab35ede5667fd2fdf7d8d2fbaa038bcb0fabbd25e1dd02159513e63d

#### Native field: algorithm_scope

Native pointer: /proofs/4/algorithm_scope; canonical SHA-256: ab2b46afea4f6511bb83e8e4fce9e47242da532fc6273daaa6bf62938b38b3be

The retained inequality covers unrestricted randomized expected loss with worst-path budgets; deterministic pointwise algorithms form a subclass.

#### Native field: body

Native pointer: /proofs/4/body; canonical SHA-256: 0779b1e01d97f1bb79222b7668402e0b18258417ce62ca0f2a060fcfd1bdf93a

Retained premise: frozen /proofs/0, canonical hash 908b109d57b75d57bc2f95589983adf234dfba1d4abcf2751dbf47d27f8f8b61, states Bayes gap >=(bR^2/2)(1-T/d) for the independent-sign diagonal quadratics. Translate the family to public x0: v_j=+/-R/sqrt(d) independently and f_v(x)=b||x-x0-v||_2^2/2. Every instance is differentiable convex, has every coordinate constant b, and has minimizer x0+v at distance R. Its scalar response is partial_j f_v(x)=b(x_j-x0_j-v_j), revealing only sign j even for an arbitrary adaptive query point. Conditional on the transcript and private randomness, unqueried signs remain independent uniform. For any output X, each unqueried coordinate has conditional expected squared error at least R^2/d. If the worst-path number of calls is at most T<d, at least d-T coordinates are unqueried, so average objective gap >=(bR^2/2)(1-T/d). A deterministic q1 algorithm with gap<=epsilon on every fixed instance also has average gap<=epsilon on this finite family. For epsilon<=bR^2/8, this forces T>=3d/4. If T>=d the conclusion is immediate. A real budget B permits an integer number of calls at most floor(B), hence B>=3d/4 as well. The average argument identifies a violating fixed instance for each failing algorithm; the target guarantee is unchanged. Oracle, arbitrary outputs and scalar cost are preserved, no q2 identity is assumed, and no external theorem is introduced. Here beta_sum=db, so epsilon<=bR^2/8<dbR^2/2 for every d>=1. The old lower is 1 on this branch; max{1,3d/4} improves it exactly for integer d>=2 and is unchanged for d=1.

#### Native field: limitations

Native pointer: /proofs/4/limitations; canonical SHA-256: 8219f0dd2f151244d30918025a74f1cbde73b364a1d650055029721d2ff54ddd

This is a sufficient diagonal-information branch. Its accuracy threshold is not an intrinsic phase boundary. Recovering the diagonal quadratic subclass in d calls does not give a target upper bound of d for the full objective class.

#### Native field: scope

Native pointer: /proofs/4/scope; canonical SHA-256: 7acf5b854bb33cbc4dfa370e6a0307e8b73168407d6b185ae6e9638c4ba3c23d

Deterministic q1, equal b_j=b>0, d>=1, R>0, 0<epsilon<=bR^2/8; arbitrary adaptive scalar-coordinate queries and arbitrary outputs.

#### Native field: source_refs

Native pointer: /proofs/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: 46ea5e638853afdfff078c7c0dee7833017a24c89724ebc1e2aadf603dc4585d

Quantitative diagonal-information lower bound for the deterministic q1 target

### Native proof: FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

Native pointer: /proofs/5; canonical SHA-256: 42eed6079319621c3779a502717559da38f2f44150b2215aff2a7dc375e4387c

#### Native field: baseline_refs

Native pointer: /proofs/5/baseline_refs; canonical SHA-256: d3a36e12356e6d1ab6716083eff4c2834b5cc34f9b46f829a928a42dbafc4638

#### Native item 1

Native pointer: /proofs/5/baseline_refs/0; canonical SHA-256: 71213f1cf0413a265b380ec500f102141ff2e9e4795549b47f6daef4af37c6cf

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/0/sha256; canonical SHA-256: 75b58334c389a5b20108b96201ba1c6dea2f96abc72165e6ad1ab083e4920fcf

85e94548c3ff1d47561173bada8e66c881dcbe6e2cfac2b602bc9cb06a79b936

#### Native item 2

Native pointer: /proofs/5/baseline_refs/1; canonical SHA-256: 55248b031e3179eb633dd0a97274e42675fb18582216b1fb59e3f6d54eaef354

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/1/sha256; canonical SHA-256: 55b11f863d32f5125b532814b047c81537788b44068c21d9515bb84ec5cc81aa

2edeb8a5c53890724904c68986cfef199a612ff79a8f04409aba10b5765124b6

#### Native item 3

Native pointer: /proofs/5/baseline_refs/2; canonical SHA-256: ad92de054e345cd0f72e65ab656ee7f0b27d16286f58fbf2ee4e67ba6cbb0492

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/2/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/2/sha256; canonical SHA-256: d304f3607fa559c8cf888ae58ec5fb6251a74e0f162a458cb23b20b6f26c651d

2fcc98fefe8a7afaf438ffe481e65d63686ba02fe5e60a20a82c567cdc1d9eb3

#### Native item 4

Native pointer: /proofs/5/baseline_refs/3; canonical SHA-256: 4395ddf3c703cc16b34dcb4a7cae3733941e1f6cb79aa6a24a1ed94f5aa59fa8

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/3/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/3/sha256; canonical SHA-256: 3a527bb61731b3eb89aaab95df934835cd3e855aa3cfc740406f227ae501ca32

707fed817e55a12a1a90ccf39ca10ea2448ded3a3be33a3d2cc235becd42545c

#### Native item 5

Native pointer: /proofs/5/baseline_refs/4; canonical SHA-256: 54a578f42724c772deb9ceb5ae3b4f5ab4e0d801e6077f8a06ad8054fccbb7c7

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/4/pointer; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/4/sha256; canonical SHA-256: bf48fa1efb69155ef5c73d723d40d55cdc4fd7674321ac1a23d52e935cce229f

7c3fa256abaaa149b3adea8f79f7d15cb557bb284e85317d6068f959502beab8

#### Native item 6

Native pointer: /proofs/5/baseline_refs/5; canonical SHA-256: 9bc3f34da565c41ca0e78386ceeb478bcf666041c8fb23bb941837267e517049

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/5/pointer; canonical SHA-256: 75e7040ee9b7f6bb53623ed289617ff0705a4d81718776cbba42cdc3e6039b04

/bounds

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/5/sha256; canonical SHA-256: f6653bed9408da726916ca93773a0bc49d9cd4acc3098cbf0a4b44b463eaf196

bcac382bcc4d6e2ef080866abea20500049f77d8f22ea0f25a37d32d89001e80

#### Native item 7

Native pointer: /proofs/5/baseline_refs/6; canonical SHA-256: 9b5007cc7ea5e8afc934208f21ff10733d2a963eef48f6ac30e29441c4f45ed3

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/6/pointer; canonical SHA-256: b5a3c8e5a69ebbfa3a635cdb498215b14ffa316a5c88100937281d883417d1bf

/proofs

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/6/sha256; canonical SHA-256: 2f6009570b24bbe40bdb7855de010737627f28603e269d67091c95ec4d1390c9

f1d3b922861fdcbb57d1e937f66050b9b7ecfbcaf3803e1ac64c3ab942f65b52

#### Native item 8

Native pointer: /proofs/5/baseline_refs/7; canonical SHA-256: 6b993a7425b5fae9a010bf2824d52013a749107b45a669500ab62985648337ef

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/7/pointer; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/7/sha256; canonical SHA-256: 602f6f9c39b631020aa6fa242834de9daf3b8bf0e1f0dc8ab2cbd88b1dcd82bf

cd60c244e1e3cb4a60e5d47d2c9c26c346655eeae47d2827ee2f1ea530098ea8

#### Native field: body

Native pointer: /proofs/5/body; canonical SHA-256: 63f308ac815b3fbe3d529e7c24e7c405fe711cbe222b84a884b7b57f667a9bbb

Retain the exact unchanged native global differentiable convex full-space model, positive coordinate budgetsbj, publicx0 and a global minimizerx* at Euclidean distance<=R, both separateq1 quantities/views and the scalar coordinate-response cost. The accepted FO_COORDINATE_ZERO_QUERY proves directly from coordinate Lipschitzness and convexity: for h!=0, set S=sumj sqrt(bj)|hj| and thetaj=sqrt(bj)|hj|/S on its support. Coordinate integration and convexity at x+h=sumj thetaj(x+(hj/thetaj)ej) give f(x+h)<=f(x)+<gradf(x),h>+S²/2<=f(x)+<gradf(x),h>+(sumj bj)||h||²/2. At the GLOBAL unconstrained minimizer gradf(x*)=0, so f(x0)-f*<=beta_sum R²/2. This argument uses the declared global objective domain, not a constrained-boundary minimizer premise or a grant of a full-gradient query. On each exact native r6 including equality epsilon>=beta_sum R²/2, the SAME deterministic algorithm returningpublicx0 without any calls therefore meets pointwise gap<=epsilon on everyinstance. It also meets the randomized expected-loss criterion by embedding a deterministic algorithm in that view. All initialization calls are zero and each path's scalar-query cap is0. The existing matching lower indicator is1{epsilon<beta_sumR²/2}; onr6 it is0, agreeing with nonnegative counts and the exact minimized cost0. Thus publish a separate optimalq1 comparison for each view, without merging their IDs or attributing a scalar-positive ratio. No0/0 ratio is formed. The existing lower proof's opposite rank-one quadratic hypotheses shows strict-below-threshold impossibility but no new positive-cost main rate is needed here. Native r6 already includes its positive-parameter r2 universe. No b_j=0,R=0,constraineddomain or newaccuracy extension is asserted. The existing positive/full comparisons keep other_quantified_gap, and equal-constant/source-dimension guards remain exactly as before. This is publication of a previously accepted endpoint proof, not a new external theorem or blind discovery.

#### Native field: proof_refs

Native pointer: /proofs/5/proof_refs; canonical SHA-256: 36027080a5b45ff82a84f8d3f7a27254330c4b7a894f32c3ecfd5db565905340

#### Native item 1

Native pointer: /proofs/5/proof_refs/0; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: scope

Native pointer: /proofs/5/scope; canonical SHA-256: 5a3e694890f09938ce941801e664f231a69e20e6a3603e2b89dfd0e6fe600331

Each existing native r6 and its own q1/view/g1/scalar-query contract.

#### Native field: source_refs

Native pointer: /proofs/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/5/title; canonical SHA-256: 032c2f10545000796da855da5f080977d7a9f1cc356be5bff4dd41b33adf35fd

Publish the already-proved exact zero q1 endpoint separately for both views

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: ecb5ff3937bd3399a8f343fd577fac1edb85b39a632066b059316e571bf252b6

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 0f5b89d6dfa3f12c8dba5e3d71a812f0892ca241edfbd624a534e4ce217799aa

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: f9e13020a3b988e234fdf1ad18cb6435d0b7e3108df4fbefbb90737f5a5a747e

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: a736633dd02ce90e33926e33da07d9e63773d3341e1248485608fdc4b82fff60

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: c7092f32e9578c4e102be99afab921b17b0c5c3aeaa0ba9a356a04d861e36511

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 237d10346b66fb2eac266554939864a25e354d8c4aa242fde45a0d578a89930a

0<epsilon<beta_sum R^2/2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: eba896c6b8d3c69d6ddca1b001750cfae3d9108487154b23af784b37110fba47

SO_FO_O01_cv__deterministic__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 11b2def882f9b2e454039f751df9a86923521cebd6c44b8b0a581f3af2b37bbf

Conditional baseline retention; native guard retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 34e803993898bc48a222e4846af951a4e8ccb431cb51f815a09c8000b7c71797

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 237d10346b66fb2eac266554939864a25e354d8c4aa242fde45a0d578a89930a

0<epsilon<beta_sum R^2/2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 8c10521d2c0fd49da6c80fe65f9630181757724ae1446a35c8b872d4e376752b

SO_FO_O01_cv__deterministic__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 11b2def882f9b2e454039f751df9a86923521cebd6c44b8b0a581f3af2b37bbf

Conditional baseline retention; native guard retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: e48f91478f5015a01f9ac7b12ad43da9fef945a09c0169a02c8c1cd6d515f830

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: a2f2bfd0b9fc764391a04eac20011af9708ccdceeef455501c95002eac1e2b27

epsilon>=beta_sum R^2/2 within the target domain

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 825f6831d9371d7760b8ce7b87a830b3a01ea2805a83fe019346c27291673f3d

SO_FO_O01_cv__deterministic__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: dedf9102ea1071bef137e3c94f5ade5f6621f3db365e28c3c482f9f4b78dd03a

Conditional retention of the exact zero-query branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: a2f2bfd0b9fc764391a04eac20011af9708ccdceeef455501c95002eac1e2b27

epsilon>=beta_sum R^2/2 within the target domain

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: 63ca30f446de466cf7804918b8932e48eea8ad6ff855e6dab16d66d914e15e81

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: 0277b902d37cfe5e44dc459f068d9fafcec4786b0d18ae8548a4c10e815058d4

Full target domain, with its displayed indicator

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: c03dca2ca53c1d5fb6a64bf851bc8b9fd3eaae818cf4c4e444ae160ab71ed033

SO_FO_O01_cv__deterministic__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 581fdd810db3f63b327fd7a3d3b39e61909d3de3ca0fec122a5919bc79dcbc11

Conditional retention of one below the zero-query threshold and zero otherwise.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 0277b902d37cfe5e44dc459f068d9fafcec4786b0d18ae8548a4c10e815058d4

Full target domain, with its displayed indicator

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: ecfd58872e23ded7bb114d0bd4432f0927ff65976bcbf47dc52e0fe98ebaed76

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: 799afd02f309fe8f884a390b44f7a3f64a8561e240d4e10b25e51b787c7cee7d

b_j=b>0 for every j and 0<epsilon<=bR^2/8

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: 5706b96400d4fe05a6da50688db973968f5b42fb1a8c87b547e1bf00d462c4b2

SO_FO_O01_cv__deterministic__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: a99edcd2c6ccf116aa9c835e607af90cb719ab8a9938ad24ffc5cd4afaedcc39

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: f57567364bf52f50da0f2cd9800ff70c9f9eb9cd2ef52ce941880f03e8fdb879

FO_COORDINATE_DIAGONAL_DET_Q1

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs/1; canonical SHA-256: d44957cd082e2cec70b37225acc2e73e28272e57eba5ce04693207a9f3a97ec5

FO_COORDINATE_SMOOTH

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: f4bf0c9d50cb8ba7421d9ab691451fac330d1d1f49d3e36d4315ed218c702986

New deterministic q1 lower 3d/4 from the retained diagonal-information inequality; take its maximum with the one-call lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: 799afd02f309fe8f884a390b44f7a3f64a8561e240d4e10b25e51b787c7cee7d

b_j=b>0 for every j and 0<epsilon<=bR^2/8

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/bound_uses/5; canonical SHA-256: 8b4767af59953853650b8bfb47695f54f59c5c7ced97a446ce641228160a1156

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/adopted_region; canonical SHA-256: 29d4add62c4e13b949aa33dc54597007d847900520ad0cd2c171b94405e3eaf4

Empty for deterministic q1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/bound_id; canonical SHA-256: d3c74594111c5ff65bb7ff2801a76e79eaa89b0ea99c0f41936a7446ea2aff06

SO_FO_O01_cv__deterministic__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/reason; canonical SHA-256: 0a1c4cf3f7b3b3bfdf982904abc337c1b5b378578d628ecfd92ac2293c50fb91

Distinct native quantity q2. Matching labels do not establish a q1 transfer; the new q1 derivation is separately recorded.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/validity_region; canonical SHA-256: e85eaf6869024c9689fdce594bf5ac1e80daaf68858b8589c1228d0860f86bd8

b_j=b>0 for every j and 0<epsilon<=c bR^2

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/bound_uses/6; canonical SHA-256: 5ae338b7c55832cddbabdf08fe2d4c6a40bd27da68b5fb3ba10b57c8bfa41ee9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/adopted_region; canonical SHA-256: 29d4add62c4e13b949aa33dc54597007d847900520ad0cd2c171b94405e3eaf4

Empty for deterministic q1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/bound_id; canonical SHA-256: faef1860e81bdbc44ab3ca15d0c9b55c9f51b656f9d75983fa5645c6c32ae512

SO_FO_O01_cv__deterministic__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/reason; canonical SHA-256: e2fe233a801b7b19f60497f3dd4679db9d2ccaa5b3b108063457b08e2cfd8fba

Distinct native quantity q2; no identity merger or active q1 transfer is assumed.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/validity_region; canonical SHA-256: e436734b23eab008f39d302c76c0abecdb07ecf540d3533481107a0125b7aa21

b_j=b>0 for every j and 0<epsilon<=c bR^2 and d>=C bR^2/epsilon

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: e5d7bc2f87b0b0c8d4ae54908f20ebfc17e314b85689971bb3a0745dd3397151

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 6cc2a152d49e5da56df8d24fd71d141eed2d22c6ace64470ce140219af5ea8c5

At epsilon=beta_sum R^2/2, both retained envelopes are zero; the ratio is inapplicable.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 4aaaf89ca6286e09a72c447946f4d47d4442a58b6d7929a5ca585bce1dfa62d7

On r7, beta_sum=db and epsilon<=bR^2/8<dbR^2/2, so the new lower is disjoint from the zero-query branch.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 6da07d8bb58b0fcd6e21afc36661bbbde425db082bc884bc2790f55362df316d

Equality epsilon=bR^2/8 is included by the explicit Bayes-risk inequality.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: 6e7e2522be460ac61d7f484071bcb3f51d293f8c8e3b43ef02262160e75ea5cc

For d=1 the old lower 1 dominates 3d/4; for every integer d>=2 the new lower is strictly stronger.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/boundary_checks/4; canonical SHA-256: 40572e553847ba72bf54cd02d70fa16cef3396b738a70702b69e01ea04d32c75

The upper crossover compares d log(2+beta_sum R^2/epsilon) with R sqrt(beta_sum/epsilon); universal hidden constants permit only an asymptotic crossover statement.

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/boundary_checks/5; canonical SHA-256: 9f1cbae710eb6dd677dd33591c81ebb46709f8b94c32ba5ba94c682920c19397

At d=1 the retained high-precision upper is logarithmic. A matching one-dimensional lower remains unassessed. Recovery of the diagonal quadratic subclass in d calls does not give an upper bound for the full objective class.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 91f5aece8539d823eb6b1a925cb30db7bb79236ff63aa2436ac8fab83d89d5cb

Ratio inapplicable on the zero-cost branch; otherwise displayed upper/lower. On r7 the lower is max{1,3d/4}.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 20885ca1d31d66efec0d7adf21562511e920385846727c7a6d16bc0f68291c40

0 when epsilon>=beta_sum R^2/2; max{1,3d/4} on deterministic r7; 1 otherwise.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: e5716a295f950ecb5089a5f6ee85d9f9c1b1314f39284efe42264fbc0b716947

Positive-cost gaps remain. The new lower improves dimension dependence on r7 for d>=2; the complement retains the one-call lower without a claim of optimality.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 1eb8d09fef751c6820adb0bfc3a2390fac358ceeb1d16be0247731fa690cbfc7

0 when epsilon>=beta_sum R^2/2; otherwise min{C d^2 log(2+beta_sum R^2/epsilon), C d R sqrt(beta_sum/epsilon)}.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 6c50bfbe180ebeaf18d7a2bcdba3af5efcc2bef936848103b80c38a39c644ced

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 2407a5ea988d0ea973210c9fc3b6b44e9f716345371e5db92e98a40d29c36ef7

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 0d1858f9e1a58e0743dc2ebc23f05a26d782dd19e0fef44e73b535286a34b4e7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 052743db904c7402e3792a517f3c0b7c0e2c77728f323876ec55a8e381e67a58

randomized r4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: da76177ea1614b700983092662ce01fb8258e217f41010b5a789d1607a753483

SO_FO_O01_cv__randomized__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 49554e2b96432793aa70d81e4c9ac7fac8f381db22612dbae063e636e7c0c1d7

Conditional baseline retention with the native guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 6f398310f55bc97521d74af2e692638bbee2f404de21f51bad7fe76f602dccc4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 052743db904c7402e3792a517f3c0b7c0e2c77728f323876ec55a8e381e67a58

randomized r4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: b51819312d23200e6daa313beac4ed522102f19e2feb8a6a0b7aad1d22dbe63c

SO_FO_O01_cv__randomized__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 49554e2b96432793aa70d81e4c9ac7fac8f381db22612dbae063e636e7c0c1d7

Conditional baseline retention with the native guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 056a9d7b4af40900939daff2a49d150dfa618ea32685b0cccd333344c8f46d78

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 052743db904c7402e3792a517f3c0b7c0e2c77728f323876ec55a8e381e67a58

randomized r4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 1b007c71f61af05d4157b583e66541cd067126142b2aa5bfabfde58d1f7c0f6d

SO_FO_O01_cv__randomized__expected_loss__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: dc77397c50229259df718f316d63ebd483d0800d657bdbb200562b2b7a687a54

Retained in the native minimum. S_b<=sqrt(d beta_sum)<=d sqrt(beta_sum), and the additive one is absorbed below the zero threshold, so NU-ACDM dominates this term up to universal constants.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: a6dc523e5f5aab7253f55c7e8d54d9650dc00a800b2585a14ad3328a6763ac4b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: 052743db904c7402e3792a517f3c0b7c0e2c77728f323876ec55a8e381e67a58

randomized r4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: b3153a06df0e5fed6430330b5540fab189e709cb63d7bd70bdc7b55e7153ca77

SO_FO_O01_cv__randomized__expected_loss__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 50cd914be0960c0dbbbfc46c5a912b4706c737f517e854efd53667df66a7fa28

Conditional baseline retention; r4 is contained in r3.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: e85eaf6869024c9689fdce594bf5ac1e80daaf68858b8589c1228d0860f86bd8

b_j=b>0 for every j and 0<epsilon<=c bR^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: 72a9efe794e9bd7c4de5c86272cbb10611ecfa18f9693b21658c38381816028f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: 052743db904c7402e3792a517f3c0b7c0e2c77728f323876ec55a8e381e67a58

randomized r4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: 752732da4061f2b7d93a4016da15d44cc38174d3fcd5c04bb51604452d746f57

SO_FO_O01_cv__randomized__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 4e200b05dbc319150b9e9f5e80c80144a4b12878bd6713c23e4442e509de1dbd

Conditional retention in the guarded maximum. Its sqrt(bR^2/epsilon) rate is asymptotically redundant beside d on r4; no deletion or new adoption is asserted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: e436734b23eab008f39d302c76c0abecdb07ecf540d3533481107a0125b7aa21

b_j=b>0 for every j and 0<epsilon<=c bR^2 and d>=C bR^2/epsilon

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/bound_uses/5; canonical SHA-256: 4ec112b1a183a42757e0106f19ed86a2913e36b81c57829d1f6f004342288f40

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/adopted_region; canonical SHA-256: 65b1cbba3b92c5b2597926a0d5dcf1fe03cdb5fa8f518dbfc1c66a523473bc7a

Empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/bound_id; canonical SHA-256: 1c798694907312bd28fdc500ae3fb79b6098f6f3fec378670c1b100a0c041196

SO_FO_O01_cv__randomized__expected_loss__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/reason; canonical SHA-256: fb4ecf55662844bfff98eda3f1383c873bd2c0a4d90dc735c979b56ed6494004

On r4, epsilon<=c bR^2<=bR^2/8<dbR^2/2. The zero-query candidate is disjoint and remains outside native active references.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/validity_region; canonical SHA-256: a2f2bfd0b9fc764391a04eac20011af9708ccdceeef455501c95002eac1e2b27

epsilon>=beta_sum R^2/2 within the target domain

#### Native item 7

Native pointer: /joint_analysis/comparisons/1/bound_uses/6; canonical SHA-256: c7f9e04abd31b3ab9c0b90fd2e965fdc43e0db0290dae5fb42a14ac74026157e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/adopted_region; canonical SHA-256: 052743db904c7402e3792a517f3c0b7c0e2c77728f323876ec55a8e381e67a58

randomized r4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/bound_id; canonical SHA-256: 9103521008b15c9f17feb9f646c05fb9a833e303d76a68c50e7fe2ab1b2fca76

SO_FO_O01_cv__randomized__expected_loss__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/reason; canonical SHA-256: 0e1190d02967e782516fb75dfc3315052f40c81cc563109fb32b3acc9d6725d7

Conditional baseline retention of the one-call lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/validity_region; canonical SHA-256: 601a27dd8d2726891727b4597763be0eead93d04d87d5d4062c656ee47d33494

Full target domain, with its indicator

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: e1b8f787f54abb93c0923ca4ac6cc608ca8da56022afa2ba6009b664e334f3db

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 632172daca6b7aa5fd2f0bcec4e30b56283af07b77cafc17b675b3b4d4defc1d

The retained small-c choice places r3 and r4 strictly below the zero-query threshold, including their accuracy endpoints.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 6e8779dec0fdbb933a4217767dfc3eedd648bd0baf0833b7eae4f50aaea8f195

The dimension guard d>=C bR^2/epsilon is a sufficient source-activation restriction, not an intrinsic phase transition.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 021e26fb3d8aa92da2859e60ee43a6c1fbf901a57cd331079d05a4a283296916

The guarded minimum retains the localization branch at extreme precision; no fixed-dimension asymptotic substitution is made.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: 839ea1aad58596e217862a93076ce9a2a7d9eb990a175d5ac0d908f4ab4c3c24

The disjoint zero-query upper b6 is absent from this comparison's native active references.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: b5d058532d6b25e2c699738c9dc6bf3e7582d5d72305b685dc3290f016ae776e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/0; canonical SHA-256: 879923da020d1533f4d8e921ea7bac61e8ba41d3c89d17a4d14e3a89c6780d5d

c

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/1; canonical SHA-256: c2e8c0cc2e73b9bd1ba9ef1979e73169b471e25b0e9909efe98fde462c0bf55f

C

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: d65621b96756174b00d4cf4f44752edee7955c4adaa78676dd5affc12e31047c

Displayed upper divided by displayed positive lower on r4.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 0ab3ac8d2615e3abf15c808ab288c27165c4373448ace44817de96403b61582b

max{c d,c R sqrt(b/epsilon),1} on randomized r4.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 7499e9ec4365e8444c0be5fc576efcae474d98ad6c40ef52ed138929e4e219df

The frozen quantified gap is retained conditionally; the annotation does not recertify every old premise or establish literature-wide optimality.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: e436734b23eab008f39d302c76c0abecdb07ecf540d3533481107a0125b7aa21

b_j=b>0 for every j and 0<epsilon<=c bR^2 and d>=C bR^2/epsilon

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 17d5f906a73bfe67dfb96f03c4fa09d654573643dfd3824df7d71dbe128b6e40

min{C(1+R S_b/sqrt(epsilon)), C d^2 log(2+beta_sum R^2/epsilon), C d R sqrt(beta_sum/epsilon)} on randomized r4.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: a55f4e730c69a76fe931743c8f6b9cf0f5d2abd39ccc37e99ae7af7bd284d33f

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 2a7548c4b869116033d636c76452374d4beebabea008c9df94f4197cd9786839

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: e77284e0d145f70096bfc862bfc93c78901fc2da36f237f941789f23caab48d3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 237d10346b66fb2eac266554939864a25e354d8c4aa242fde45a0d578a89930a

0<epsilon<beta_sum R^2/2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: da76177ea1614b700983092662ce01fb8258e217f41010b5a789d1607a753483

SO_FO_O01_cv__randomized__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 81a8c30659242452e1245df877f9048023a8b36caf8ed6a60f3f7150a33d31b8

Conditional baseline retention with native guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 9a52ac46501670c1ccb08ed3e6bb55b290c462f962fd6f6e5f7f3936726bdfea

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: 237d10346b66fb2eac266554939864a25e354d8c4aa242fde45a0d578a89930a

0<epsilon<beta_sum R^2/2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: b51819312d23200e6daa313beac4ed522102f19e2feb8a6a0b7aad1d22dbe63c

SO_FO_O01_cv__randomized__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: 81a8c30659242452e1245df877f9048023a8b36caf8ed6a60f3f7150a33d31b8

Conditional baseline retention with native guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: 8559b6a145272fe302c5d2491d2ce75d6dc022bd3436161ca87d4abb13f35f4d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: 237d10346b66fb2eac266554939864a25e354d8c4aa242fde45a0d578a89930a

0<epsilon<beta_sum R^2/2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: 1b007c71f61af05d4157b583e66541cd067126142b2aa5bfabfde58d1f7c0f6d

SO_FO_O01_cv__randomized__expected_loss__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: ad1cd7443eaff7249b42d040731c97f72936c0b42883bcd527b6cbabad704746

Retained in the minimum. S_b<=sqrt(d beta_sum)<=d sqrt(beta_sum), so NU-ACDM dominates this simulated-gradient term up to universal constants below the zero threshold.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: 0ce160da64fa7c877446a06d10ee2f3032a006e17100042993f6c15628e23dc9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: b9e1ad2cb7c587672d398a563f19b460ceb3d9a1b513ba32a2e18fe94d7c362f

randomized r3

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: b3153a06df0e5fed6430330b5540fab189e709cb63d7bd70bdc7b55e7153ca77

SO_FO_O01_cv__randomized__expected_loss__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: f31bc61367786370a55da8fd8113d3f5de7ac309ee20a97e3f61dc621e70f73f

Conditional baseline retention with its equal-constants and accuracy guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: e85eaf6869024c9689fdce594bf5ac1e80daaf68858b8589c1228d0860f86bd8

b_j=b>0 for every j and 0<epsilon<=c bR^2

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: efc0a6f9ccd9f0d7c56272776f5bce0edb543f5aefef4ce03db0660bca127223

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: 052743db904c7402e3792a517f3c0b7c0e2c77728f323876ec55a8e381e67a58

randomized r4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: 752732da4061f2b7d93a4016da15d44cc38174d3fcd5c04bb51604452d746f57

SO_FO_O01_cv__randomized__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: 8f294e5923a7933d4e40cdd112ace7f63ab846502bfbc77e28f78dde2730b487

Conditional retention in the guarded maximum; asymptotically redundant beside d on r4.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: e436734b23eab008f39d302c76c0abecdb07ecf540d3533481107a0125b7aa21

b_j=b>0 for every j and 0<epsilon<=c bR^2 and d>=C bR^2/epsilon

#### Native item 6

Native pointer: /joint_analysis/comparisons/2/bound_uses/5; canonical SHA-256: 9f754a50378079b4f77546cebef61139c80a945e41b8e4c7130ecdbb2e6c4db6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/adopted_region; canonical SHA-256: a2f2bfd0b9fc764391a04eac20011af9708ccdceeef455501c95002eac1e2b27

epsilon>=beta_sum R^2/2 within the target domain

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/bound_id; canonical SHA-256: 1c798694907312bd28fdc500ae3fb79b6098f6f3fec378670c1b100a0c041196

SO_FO_O01_cv__randomized__expected_loss__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/reason; canonical SHA-256: dedf9102ea1071bef137e3c94f5ade5f6621f3db365e28c3c482f9f4b78dd03a

Conditional retention of the exact zero-query branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/validity_region; canonical SHA-256: a2f2bfd0b9fc764391a04eac20011af9708ccdceeef455501c95002eac1e2b27

epsilon>=beta_sum R^2/2 within the target domain

#### Native item 7

Native pointer: /joint_analysis/comparisons/2/bound_uses/6; canonical SHA-256: 686a8fe4f5076a6f7ebff39214b637c90cac06fde0a30059513cfaf34cc1fcbe

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/adopted_region; canonical SHA-256: 601a27dd8d2726891727b4597763be0eead93d04d87d5d4062c656ee47d33494

Full target domain, with its indicator

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/bound_id; canonical SHA-256: 9103521008b15c9f17feb9f646c05fb9a833e303d76a68c50e7fe2ab1b2fca76

SO_FO_O01_cv__randomized__expected_loss__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/reason; canonical SHA-256: 581fdd810db3f63b327fd7a3d3b39e61909d3de3ca0fec122a5919bc79dcbc11

Conditional retention of one below the zero-query threshold and zero otherwise.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/validity_region; canonical SHA-256: 601a27dd8d2726891727b4597763be0eead93d04d87d5d4062c656ee47d33494

Full target domain, with its indicator

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 18309ef72b541bdf8b5723dd64f8961bd43ab1f13ccf01ae110b4dfe658c1bc3

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: c5f706d7956e70631752748eb53b7a0ab40357e39bf9bcb0c61e308033c201fa

At and above epsilon=beta_sum R^2/2 the exact cost is zero, with no 0/0 ratio.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: 4c3b093b541b298aebb11e42f16160843f6cd31b1b7b4d91712571e4278f9e87

The retained c<=1/8 choice makes r3 and r4 disjoint from the zero-query branch.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/boundary_checks/2; canonical SHA-256: fb74a8fed7383821f9aedea5ec24fef5b07ef887b1161924ae3a5e207b8b2106

Outside r3 and r4 the positive-cost lower remains one.

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/boundary_checks/3; canonical SHA-256: 90235d63d8e43a9af87ef88c4aa991b4f152543b0e0889cbcd37da584ffddef9

The sufficient dimension restriction is a theorem-activation guard; the finite-dimensional upper branch remains in the guarded minimum.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: 71ddc089addf96acf7b1b56e5e3169dedcf0e74fd276feab450a8170488cc8c0

Ratio inapplicable on the zero-cost branch; otherwise displayed upper/lower with every guard retained.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 002c5f5e2629a45202559efd74f25c5730235b4e99f5fd410ac2c2b25ab4b2b8

0 when epsilon>=beta_sum R^2/2; max{1,c d,c R sqrt(b/epsilon)} on randomized r4; max{1,c d} on randomized r3 minus r4; 1 otherwise.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 5639f5fc6e389977cf522814cff4c09455d9b10526242c3e911a6441560bfa70

The frozen quantified gap is retained conditionally. Sharper heterogeneous and low-dimensional lower bounds remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: 6e84dcd983502c46486497fdd98029f042b0e8f211c3c1c8b6332db7af992660

0 when epsilon>=beta_sum R^2/2; otherwise min{C(1+R S_b/sqrt(epsilon)), C d^2 log(2+beta_sum R^2/epsilon), C d R sqrt(beta_sum/epsilon)}.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: a5df2637284a3615a4857ac0949f934e12d2b06169387e75ded005389d5e7b74

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 78fb4b3e770f3a56687bb520f8f7281ed8fca450d92a4d4c0f07c4fd13a60bf8

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: 1054ded3518af67e622e5d5916a10f07bfe1685d30ac2dba5703ec1248ccbaa9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 4c5a0504d86b4226555043d12ecf5e7bc428f1bb8c6b07bb82c9382d178faf9d

Not selected onr6.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: eba896c6b8d3c69d6ddca1b001750cfae3d9108487154b23af784b37110fba47

SO_FO_O01_cv__deterministic__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 8ce443bd23d2ea24e1ccc4fc1f9c413f1388b309a7f1fbf7525cdb6aaa62851c

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 936ebdba719c665b8c36cbc9b3e8fb494e256a6b14a080aca88a9bf0a485b970

The already-proved0-call witness dominates this positive sufficient cap on its source-valid overlap. Original validity is unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 5107c4f67836b49faabcd4af2ebc6d13e6eb92e8af914ab720664e6e949c9227

Referenced regions: ($b_j>0,\quad R>0,\quad\varepsilon>0$) AND ($$b_j>0,\quad R>0,\quad\varepsilon>0$$)

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: fdafb256a372dbccdb35402d7054708d0a4fe266a8e14837303e5254b18b6c4d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: 4c5a0504d86b4226555043d12ecf5e7bc428f1bb8c6b07bb82c9382d178faf9d

Not selected onr6.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 8c10521d2c0fd49da6c80fe65f9630181757724ae1446a35c8b872d4e376752b

SO_FO_O01_cv__deterministic__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8ce443bd23d2ea24e1ccc4fc1f9c413f1388b309a7f1fbf7525cdb6aaa62851c

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: 936ebdba719c665b8c36cbc9b3e8fb494e256a6b14a080aca88a9bf0a485b970

The already-proved0-call witness dominates this positive sufficient cap on its source-valid overlap. Original validity is unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 5107c4f67836b49faabcd4af2ebc6d13e6eb92e8af914ab720664e6e949c9227

Referenced regions: ($b_j>0,\quad R>0,\quad\varepsilon>0$) AND ($$b_j>0,\quad R>0,\quad\varepsilon>0$$)

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: f195e3ee0e02d92f6fff4f524ab39ce65812ca4b86a8e30007435163520f55aa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 0fa9796874d27b0fcf46110e50a41d253d693cf4191338076850f7c62c516096

Comparison region: ($\varepsilon\ge\beta_{\rm sum}R^2/2$) AND Bound validity: (Referenced regions: ($\varepsilon\ge\beta_{\rm sum}R^2/2$) AND ($b_j>0,\ R>0,\ d\ge1,\ \varepsilon\ge\beta_{\rm sum}R^2/2$)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "The exact native r6 within its positive-parameter r2; no source guard extension.", "region_ref": "SO_FO_O01_cv__deterministic__deterministic__r6"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: 825f6831d9371d7760b8ce7b87a830b3a01ea2805a83fe019346c27291673f3d

SO_FO_O01_cv__deterministic__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: a32bcc821894584b743becc4e0801195d57b182f4df0fc381f53b908e266f3b7

The same native q1/view resource, specialized on exactr6 and completely combined in FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: c2b5ac62ae411687ece225b27222811f65d2fd06540e7cebf847c221e7bb73d2

Referenced regions: ($\varepsilon\ge\beta_{\rm sum}R^2/2$) AND ($b_j>0,\ R>0,\ d\ge1,\ \varepsilon\ge\beta_{\rm sum}R^2/2$)

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: 4b2985ba1d45fae9e8d45ce8465db8432207b88970ace69cf48810658ec0b314

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: f6bb5983a677bcf279d7102b5c6dd80de59430cbbfd117ad35c10306048a0a86

Comparison region: ($\varepsilon\ge\beta_{\rm sum}R^2/2$) AND Bound validity: (Referenced regions: ($b_j>0,\quad R>0,\quad\varepsilon>0$) AND ($b_j>0,\ R>0,\ d\ge1,\ \varepsilon>0$)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "The exact native r6 within its positive-parameter r2; no source guard extension.", "region_ref": "SO_FO_O01_cv__deterministic__deterministic__r6"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: c03dca2ca53c1d5fb6a64bf851bc8b9fd3eaae818cf4c4e444ae160ab71ed033

SO_FO_O01_cv__deterministic__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: a32bcc821894584b743becc4e0801195d57b182f4df0fc381f53b908e266f3b7

The same native q1/view resource, specialized on exactr6 and completely combined in FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 3fac14b3e797c33ced10af12f2be7d6ca34795ac03acfc8bde3cc7827981cf5d

Referenced regions: ($b_j>0,\quad R>0,\quad\varepsilon>0$) AND ($b_j>0,\ R>0,\ d\ge1,\ \varepsilon>0$)

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: 96ce6920a32b587cd5c198579e2c07834aac8d9ae208afa7a121275515ec21a3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: 12322a38008ca46ea21c2482934efdf581bbcb6564d460e77eb5012722d91346

No adoption outside the original positive-accuracy source guard.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: 5706b96400d4fe05a6da50688db973968f5b42fb1a8c87b547e1bf00d462c4b2

SO_FO_O01_cv__deterministic__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: f5894652376e048e34bd080f5f7d4c21f41339aee9735f16d054f6edf61ff158

The original positive lower guard remains binding. Its small-accuracy/equal-constant domain (including native parent-region constraints) is disjoint from this r6 zero endpoint; do not extend a positive lower to it.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: 5c04e027212e67d62a80da2eeeb06eab6b52fa3c86aae006c84694f1ad40a23b

Referenced regions: ($b_j=b>0\ (\forall j),\quad 0<\varepsilon\le bR^2/8$) AND ($d\ge1,\ R>0,\ b_j=b>0\ (\forall j),\ 0<\varepsilon\le bR^2/8$)

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/bound_uses/5; canonical SHA-256: f7aef65741ee8f4b021defc52aab87269b763250ad442f6fe61b3be017516a4b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/adopted_region; canonical SHA-256: 249bc322638b991c0bfa19f77fcb4956a0d68185e745cbdd9d4345a0a03d9133

No direct distinct-quantity adoption.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/bound_id; canonical SHA-256: d3c74594111c5ff65bb7ff2801a76e79eaa89b0ea99c0f41936a7446ea2aff06

SO_FO_O01_cv__deterministic__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/reason; canonical SHA-256: 2b1b30461aa96ab16de5ffa2825d16ce7fec2171b4f99772b799e5f025ec0377

The deterministic q2-to-q1 positive-cost route remains an explicitly typed pending obligation, not an identity merge or a lower used in the zero comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/validity_region; canonical SHA-256: 0cb2eac390ad4ad7857bc0c6eab6b910f65acdc2098fab8b6738a03ca2525716

Referenced regions: ($b_j=b\ (\forall j),\quad\varepsilon\le cbR^2$) AND ($$b_j=b\ (\forall j),\quad\varepsilon\le cbR^2$$)

#### Native item 7

Native pointer: /joint_analysis/comparisons/3/bound_uses/6; canonical SHA-256: 60de59f546d785bb890e8ee04fea946e8b7686590c2ca736b12926c91b8430c5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/adopted_region; canonical SHA-256: 249bc322638b991c0bfa19f77fcb4956a0d68185e745cbdd9d4345a0a03d9133

No direct distinct-quantity adoption.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/bound_id; canonical SHA-256: faef1860e81bdbc44ab3ca15d0c9b55c9f51b656f9d75983fa5645c6c32ae512

SO_FO_O01_cv__deterministic__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/reason; canonical SHA-256: 2b1b30461aa96ab16de5ffa2825d16ce7fec2171b4f99772b799e5f025ec0377

The deterministic q2-to-q1 positive-cost route remains an explicitly typed pending obligation, not an identity merge or a lower used in the zero comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/validity_region; canonical SHA-256: 529283b40e437355a55817c86dfc2b4c47f909352a93f92c61242f09cb379b1a

Referenced regions: ($d\ge CbR^2/\varepsilon$) AND ($$d\ge CbR^2/\varepsilon$$)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: 67f50827b34fdce13848979dd7472f4afdcf54e83764c05fb14b7e43f0ba3dc0

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: 7b0814c618a8474fd3f15bb64fc9a2372b7816533fdbede3e83cfa03077bdb1a

epsilon=beta_sumR²/2 included; positivebj,R,d and the exactnative r6 universe retained.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: 6e125f55eb901752ab76e032c4d273e7231378f66a9d9d4feb5517e81f5f4cfe

Same deterministic0-call witness meets this view; no q1/q2 or deterministic/randomized identity merge.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: 560e6cf0fd1a149e96b768ce70c855af7171d3d63eb12d09f4fa6bef47ee88a2

SO_FO_O01_cv__deterministic__deterministic__c_zero

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: aa4a2fb3f7c4257f2d662788d887f44e196aa1c10db760450e7ad25a41cb9177

Exactcost0, multiplicative ratio inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 2cc26299d4bff46c9254904259bc6c40ec56b1d9597f941bbbae3e6523eb8deb

0: existing indicatorlower specializes to0 onr6 and counts are nonnegative.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 70647f839453454d256ebc24ece2a6b5c30765556835ae91f5079b1a65737cbc

No rate gap on this exact zero endpoint only. Positive-cost rates and heterogeneous-coordinate refinements remain unassessed as before.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: f9c1a480cef8f51d16daf028be885c86e02c4427f561e26ffe9cd5003d21daa2

0 scalar coordinate calls; returnpublicx0.

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: 238239ae22f54c1f7c7c78f266590b07a03319a4abba1bb2c8f16a1f7b542c3d

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: 7209227a16c0864750fe4d901ba9ed861357c968786cdbfb22a5d97e1a45ad56

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: 0b8f9bc064e26e095fa508477c0a1e1e86584258055477b231cdc1045fd504bf

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: 4c5a0504d86b4226555043d12ecf5e7bc428f1bb8c6b07bb82c9382d178faf9d

Not selected onr6.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: da76177ea1614b700983092662ce01fb8258e217f41010b5a789d1607a753483

SO_FO_O01_cv__randomized__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 8ce443bd23d2ea24e1ccc4fc1f9c413f1388b309a7f1fbf7525cdb6aaa62851c

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: 936ebdba719c665b8c36cbc9b3e8fb494e256a6b14a080aca88a9bf0a485b970

The already-proved0-call witness dominates this positive sufficient cap on its source-valid overlap. Original validity is unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 5107c4f67836b49faabcd4af2ebc6d13e6eb92e8af914ab720664e6e949c9227

Referenced regions: ($b_j>0,\quad R>0,\quad\varepsilon>0$) AND ($$b_j>0,\quad R>0,\quad\varepsilon>0$$)

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: a2d3cfb6c528d08cd3fa6647646c44f9a471a0765d64749dba550043bb26db6a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: 4c5a0504d86b4226555043d12ecf5e7bc428f1bb8c6b07bb82c9382d178faf9d

Not selected onr6.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: b51819312d23200e6daa313beac4ed522102f19e2feb8a6a0b7aad1d22dbe63c

SO_FO_O01_cv__randomized__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8ce443bd23d2ea24e1ccc4fc1f9c413f1388b309a7f1fbf7525cdb6aaa62851c

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: 936ebdba719c665b8c36cbc9b3e8fb494e256a6b14a080aca88a9bf0a485b970

The already-proved0-call witness dominates this positive sufficient cap on its source-valid overlap. Original validity is unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: 5107c4f67836b49faabcd4af2ebc6d13e6eb92e8af914ab720664e6e949c9227

Referenced regions: ($b_j>0,\quad R>0,\quad\varepsilon>0$) AND ($$b_j>0,\quad R>0,\quad\varepsilon>0$$)

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/bound_uses/2; canonical SHA-256: 25842c9da2f9890bc855645b6c05ef1a2806d962f1151a13b23b6b3b1058055b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/adopted_region; canonical SHA-256: 4c5a0504d86b4226555043d12ecf5e7bc428f1bb8c6b07bb82c9382d178faf9d

Not selected onr6.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/bound_id; canonical SHA-256: 1b007c71f61af05d4157b583e66541cd067126142b2aa5bfabfde58d1f7c0f6d

SO_FO_O01_cv__randomized__expected_loss__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8ce443bd23d2ea24e1ccc4fc1f9c413f1388b309a7f1fbf7525cdb6aaa62851c

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/reason; canonical SHA-256: 936ebdba719c665b8c36cbc9b3e8fb494e256a6b14a080aca88a9bf0a485b970

The already-proved0-call witness dominates this positive sufficient cap on its source-valid overlap. Original validity is unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/validity_region; canonical SHA-256: 5107c4f67836b49faabcd4af2ebc6d13e6eb92e8af914ab720664e6e949c9227

Referenced regions: ($b_j>0,\quad R>0,\quad\varepsilon>0$) AND ($$b_j>0,\quad R>0,\quad\varepsilon>0$$)

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/bound_uses/3; canonical SHA-256: ac020c0879d09edb102b458c6fa6f7b1e4f549eebf0aff97a5f9218615133edf

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/adopted_region; canonical SHA-256: 12322a38008ca46ea21c2482934efdf581bbcb6564d460e77eb5012722d91346

No adoption outside the original positive-accuracy source guard.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/bound_id; canonical SHA-256: b3153a06df0e5fed6430330b5540fab189e709cb63d7bd70bdc7b55e7153ca77

SO_FO_O01_cv__randomized__expected_loss__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/reason; canonical SHA-256: f5894652376e048e34bd080f5f7d4c21f41339aee9735f16d054f6edf61ff158

The original positive lower guard remains binding. Its small-accuracy/equal-constant domain (including native parent-region constraints) is disjoint from this r6 zero endpoint; do not extend a positive lower to it.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/validity_region; canonical SHA-256: 0cb2eac390ad4ad7857bc0c6eab6b910f65acdc2098fab8b6738a03ca2525716

Referenced regions: ($b_j=b\ (\forall j),\quad\varepsilon\le cbR^2$) AND ($$b_j=b\ (\forall j),\quad\varepsilon\le cbR^2$$)

#### Native item 5

Native pointer: /joint_analysis/comparisons/4/bound_uses/4; canonical SHA-256: 129b7a6f9a6ffce8721ca848806154e9e306261c1c46b5defd93c799038b3b00

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/adopted_region; canonical SHA-256: 12322a38008ca46ea21c2482934efdf581bbcb6564d460e77eb5012722d91346

No adoption outside the original positive-accuracy source guard.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/bound_id; canonical SHA-256: 752732da4061f2b7d93a4016da15d44cc38174d3fcd5c04bb51604452d746f57

SO_FO_O01_cv__randomized__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/reason; canonical SHA-256: f5894652376e048e34bd080f5f7d4c21f41339aee9735f16d054f6edf61ff158

The original positive lower guard remains binding. Its small-accuracy/equal-constant domain (including native parent-region constraints) is disjoint from this r6 zero endpoint; do not extend a positive lower to it.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/validity_region; canonical SHA-256: 529283b40e437355a55817c86dfc2b4c47f909352a93f92c61242f09cb379b1a

Referenced regions: ($d\ge CbR^2/\varepsilon$) AND ($$d\ge CbR^2/\varepsilon$$)

#### Native item 6

Native pointer: /joint_analysis/comparisons/4/bound_uses/5; canonical SHA-256: 4818a6dc7c6fa07333708bf0bc1b28d1ddcba2401f7af677f4d8482b198dcb97

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/adopted_region; canonical SHA-256: a4a0be3d27f4c2b40f19dd3ec5d2b8b9359495e04ecd108f4c41a1acb5ff762b

Comparison region: ($\varepsilon\ge\beta_{\rm sum}R^2/2$) AND Bound validity: (Referenced regions: ($\varepsilon\ge\beta_{\rm sum}R^2/2$) AND ($b_j>0,\ R>0,\ d\ge1,\ \varepsilon\ge\beta_{\rm sum}R^2/2$)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "The exact native r6 within its positive-parameter r2; no source guard extension.", "region_ref": "SO_FO_O01_cv__randomized__expected_loss__r6"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/bound_id; canonical SHA-256: 1c798694907312bd28fdc500ae3fb79b6098f6f3fec378670c1b100a0c041196

SO_FO_O01_cv__randomized__expected_loss__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/mapping_proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/mapping_proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/reason; canonical SHA-256: a32bcc821894584b743becc4e0801195d57b182f4df0fc381f53b908e266f3b7

The same native q1/view resource, specialized on exactr6 and completely combined in FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/validity_region; canonical SHA-256: c2b5ac62ae411687ece225b27222811f65d2fd06540e7cebf847c221e7bb73d2

Referenced regions: ($\varepsilon\ge\beta_{\rm sum}R^2/2$) AND ($b_j>0,\ R>0,\ d\ge1,\ \varepsilon\ge\beta_{\rm sum}R^2/2$)

#### Native item 7

Native pointer: /joint_analysis/comparisons/4/bound_uses/6; canonical SHA-256: 0ec02dd0fa28d4703e8899e8521bbdafb63dabf653f8539c6ba546213d44bd72

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/adopted_region; canonical SHA-256: 0332b9ff0c2b1b417344d6f8d5b84ebde9a0971292c83f9cb85ca1cd6ecdd39a

Comparison region: ($\varepsilon\ge\beta_{\rm sum}R^2/2$) AND Bound validity: (Referenced regions: ($b_j>0,\quad R>0,\quad\varepsilon>0$) AND ($b_j>0,\ R>0,\ d\ge1,\ \varepsilon>0$)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "The exact native r6 within its positive-parameter r2; no source guard extension.", "region_ref": "SO_FO_O01_cv__randomized__expected_loss__r6"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/bound_id; canonical SHA-256: 9103521008b15c9f17feb9f646c05fb9a833e303d76a68c50e7fe2ab1b2fca76

SO_FO_O01_cv__randomized__expected_loss__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/mapping_proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/mapping_proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/reason; canonical SHA-256: a32bcc821894584b743becc4e0801195d57b182f4df0fc381f53b908e266f3b7

The same native q1/view resource, specialized on exactr6 and completely combined in FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/validity_region; canonical SHA-256: 3fac14b3e797c33ced10af12f2be7d6ca34795ac03acfc8bde3cc7827981cf5d

Referenced regions: ($b_j>0,\quad R>0,\quad\varepsilon>0$) AND ($b_j>0,\ R>0,\ d\ge1,\ \varepsilon>0$)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: 67f50827b34fdce13848979dd7472f4afdcf54e83764c05fb14b7e43f0ba3dc0

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: 7b0814c618a8474fd3f15bb64fc9a2372b7816533fdbede3e83cfa03077bdb1a

epsilon=beta_sumR²/2 included; positivebj,R,d and the exactnative r6 universe retained.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/boundary_checks/1; canonical SHA-256: 6e125f55eb901752ab76e032c4d273e7231378f66a9d9d4feb5517e81f5f4cfe

Same deterministic0-call witness meets this view; no q1/q2 or deterministic/randomized identity merge.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: 504cc054d68beda454fec328ceae164cdffef5ff47aa37a8cec054935facb5e0

SO_FO_O01_cv__randomized__expected_loss__c_zero

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: aa4a2fb3f7c4257f2d662788d887f44e196aa1c10db760450e7ad25a41cb9177

Exactcost0, multiplicative ratio inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: 2cc26299d4bff46c9254904259bc6c40ec56b1d9597f941bbbae3e6523eb8deb

0: existing indicatorlower specializes to0 onr6 and counts are nonnegative.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: 70647f839453454d256ebc24ece2a6b5c30765556835ae91f5079b1a65737cbc

No rate gap on this exact zero endpoint only. Positive-cost rates and heterogeneous-coordinate refinements remain unassessed as before.

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: f9c1a480cef8f51d16daf028be885c86e02c4427f561e26ffe9cd5003d21daa2

0 scalar coordinate calls; returnpublicx0.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 02b34314a5686977dc97601ebbc4608909311b8ffc0351563c09ad95a8923f59

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 66dd3989bf56c8f4bf8c201245ce15ec7699824faf3b4e49f626a0089c3159c6

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: dc19da5994c6a4094299e329bb4e93e6e67d816273109462252c8c8d252d99dd

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: b7ce3f814d0e14e74eb1dc742ad4a2c7a798413fb9771560f107cad87ef46402

zero

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 13184086e9629ad57277f9c8ad7a471b5f02d8e4c259c1ac87bc379773ccf6da

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 560e6cf0fd1a149e96b768ce70c855af7171d3d63eb12d09f4fa6bef47ee88a2

SO_FO_O01_cv__deterministic__deterministic__c_zero

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/1; canonical SHA-256: 504cc054d68beda454fec328ceae164cdffef5ff47aa37a8cec054935facb5e0

SO_FO_O01_cv__randomized__expected_loss__c_zero

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: b38de0ec1a6fe91cff479d785da82ec7f9820eb30edc9e3f0ca2ae37674611b7

Both separate q1 native optimal comparisons publish the exact0 endpoint; original positive-cost comparisons remain unclosed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: a2f2bfd0b9fc764391a04eac20011af9708ccdceeef455501c95002eac1e2b27

epsilon>=beta_sum R^2/2 within the target domain

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: e0aac8fa6354d5546392e97cada79ab41d46d400fcb851fa68fc03ae580d72f8

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: b52807322b26a1676463a92c8a0aa839d60dd3b11eae1a04d8700722fbb060e0

equal-high-dimension

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 1669791fc8db9fee3cb3dd73b0d631e3b8c54188856756181ccd69d88c176596

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/2; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 84fed6c7b821b5bae2a221c1f464f5b7df8cc9c54f6fe2bbe2b409b53e789e7d

The frozen r4 is contained in r3. With the retained small-c choice this cell lies inside the new deterministic r7. The dimension guard activates a retained theorem; it is not an established intrinsic phase boundary.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: e436734b23eab008f39d302c76c0abecdb07ecf540d3533481107a0125b7aa21

b_j=b>0 for every j and 0<epsilon<=c bR^2 and d>=C bR^2/epsilon

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 40995664ee358774ea3b30c5a908a66d02cb62915b04d2a0c7fbbf7f27874031

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 62a3ef5bc5c7cb659b8a4a76935e6a3cd38c8647d21698291001ff52c899cea0

equal-small-accuracy-other-dimension

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 8973a3840a6f6dfdc1e68332dc9e162c5028718e7d226493d7f443f6033eb99a

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/1; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: ff9e5c9a5a29754a0f5cb0b1b5a94ed15ff7f8974bb26ab336f1f20259fcb0b0

Includes d=1. The new deterministic lower is max{1,3d/4}; randomized science remains conditional baseline data.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: ead9105b9153831946cfce7f97ba9f4fcd1f4adfcf3c0a069a97af4a28dbdf55

b_j=b>0 for every j and 0<epsilon<=c bR^2 and d<C bR^2/epsilon

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: f51523e1d2a3224aee6d65655333cfaa6f67697071b85afcbf949bb6639e03d0

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: f40dc35d0575d7a2bac2f19bd348f91963de6148af4bf641890491ce60d92a97

equal-explicit-extension

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 8973a3840a6f6dfdc1e68332dc9e162c5028718e7d226493d7f443f6033eb99a

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/1; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: bd52ff57043d3ca3911167321b6bd46ee4cd984c93091a28bc7fd61a144f1c56

May be empty when the retained c is 1/8. The new deterministic lower applies with an explicit constant; no new randomized row is adopted.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 7769ff46a906018646e3ce04e9f54fa371866fdd74c66b6f5e130a3dd4cbec3d

b_j=b>0 for every j and c bR^2<epsilon<=bR^2/8

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 5

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: 43b1054b6bab44c190ff1d93167dc3753d71902c922ce81ea0a38c58858f18e4

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: 9e65972a8fddbbe946abd07cb5fd391f937a20e6af28ce1fb1d033330863c53b

positive-residual

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: 8973a3840a6f6dfdc1e68332dc9e162c5028718e7d226493d7f443f6033eb99a

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/1; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: df2b0ea02389d88594f14028693c738f80ed57e282bfbcc0e474c18df8a32b21

Frozen upper bounds and the one-call lower are recorded. Sharper main-rate and heterogeneous-parameter assessment remains unassessed; this is not a proved open region.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: 12a592998dcb7affbf331b3641de09f947f71d6dd144e52a6f628e80ec3d71b4

0<epsilon<beta_sum R^2/2 and NOT (b_j=b>0 for every j and 0<epsilon<=bR^2/8)

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: d1ca66b36f281849fbef984c39c1740a75293ba677ae42cf589f9b3cbb42092d

Split first at epsilon=beta_sum R^2/2. The equal-constant branch epsilon<=bR^2/8 is strictly below that threshold because beta_sum=db and d>=1. Within that branch, choose the retained sufficient universal c<=1/8, split at epsilon=c bR^2, and on r3 split at d=C bR^2/epsilon. Remaining positive-cost points form positive-residual. Strict complementary inequalities ensure disjointness; equalities belong to the displayed <= or >= branch.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 365134b52b1869a18703b6ffb5440d0481bbd2f6ef7048fd52a132105f85ac40

No target points lie outside these cells. Stronger-rate assessment remains unassessed on positive-residual; sharper bounds on the other cells also remain possible.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 9e363812cc7dc00cec2ae58f8cbbf852f79da9d603de5af12315c8c5d1e9044d

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: aeb2e06b5e4ed0133fd9f7e3a49d00390dc19ed2db5624c279a50384f21193ea

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 120ab9d7d3e8845b2077542e856bebb04fc409f421bb198f9f0fcdc1632ac029

The retained inequality (bR^2/2)(1-T/d)<=epsilon and epsilon<=bR^2/8 imply T>=3d/4. Comparing with 1 is strict exactly for integer d>=2. The accuracy boundary is an exact sufficient activation threshold for this stated lower, not an intrinsic phase boundary.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 10f57901a31b4ab7c52dcc5e1aaa49270849a0d4aac8dfc0e65e0693d1a8f0a4

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 3ef7cf214e7472368b3209dca0497a7eb4b53a943682ad7a014af84e41fadf52

det-q1-diagonal-main-lower

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: e661ca59b5c4445ad182bc5908b3aa8b922b5ebcc3de81aefca0b7b6ae943b72

b_j=b>0 for every j, 0<epsilon<=bR^2/8, and integer d>=2

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: c89d44acd29d128abfc4e61f77f2de09b0ca7b60010b4cbb8689f693b21f82a7

Same upper; lower=max{1,3d/4} on r7, 1 elsewhere below beta_sum R^2/2, and 0 at/above it.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: e3846f167564791e390e3d3541c563a8d1629ddf1fbcd2a8bc82a4c574c9d655

Lower=1 below beta_sum R^2/2 and 0 at/above it; upper is the retained deterministic guarded minimum.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: eb9ec30b3e3fa2028ba8f77b9805d23979b742ac20841195afcd07e7e8a86b67

d=1 on r7 and the target outside r7; all upper bounds and both randomized native comparisons.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 799afd02f309fe8f884a390b44f7a3f64a8561e240d4e10b25e51b787c7cee7d

b_j=b>0 for every j and 0<epsilon<=bR^2/8

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 0f7a8b09f3b00817f73cf5147b2f81ca5072411bd824d31f06383bca84d1f701

b=R=1, epsilon=1/8, integer d>=2: old lower 1, new lower 3d/4, an improvement proportional to d as d grows.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 4c6f72e3a08aa7978c5897b08ad7a5f4967d8163e329c21f303847e1c13cede3

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 791d8d91a86e9f6a78983a30e86b701a6148076f1f9f90ed4695b3ab243d5c19

Native joint-variable IDs and uniform constants are explicit. Both q1 quantities already track these parameters; b is used only on its equal-constants slice. No metadata normalization is needed, and unassessed sharper-rate work remains recorded.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 1669791fc8db9fee3cb3dd73b0d631e3b8c54188856756181ccd69d88c176596

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 8566dff460923c77201b1f86b0f3b5e891c4f28e952edb31c910d2266aaea96f

joint-target-guarded-annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: c478df81a3a771d6a0d420c077eb4983194b1018d048c3a5f608f38bb6f0da50

Empty for this presentation finding

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 37cec0db32b3646d837087ebff48fda30c6432d27d4273d42d7cbc295beb898a

The same scientific content except the independently justified deterministic delta; this finding resolves parameter roles, participation and domain accounting.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: a94bf3404a60f5356b440439ed581f5b0aa70f4b205b30b8155e8c7960fee52c

The three frozen guarded native brackets with an unresolved joint annotation.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: e0f04d2c7885b79044837d947c988f172a9dce874d15be5a212e9d1ec919a51b

All scientific inequalities, guards and statuses except the separately justified deterministic delta.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: ba6624c380add766b7b38248770c405705f6738e94a440a522d994f224fe0d37

The zero-query equality is retained; randomized c1 excludes disjoint b6, and q2 rows are not active in deterministic q1.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 80d13f275418ee3e649d4998f1c2d904e36536b025d036d01a84af5b55b9034b

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 0fc3f15cf544e6e697cdbac84fec49fd27b77bbe367201b3b163fdaeda5612ed

Read arXiv:1512.09103v3, source f22fe112e65b231732047a12008e97876e17b466b80704abd3b3f5bae1ea3d0e, Algorithm 2 and Theorem 6.1, PDF p.13, characters [30843,32542). Set source beta=0, L_j=b_j and n=d. Each iteration reuses one partial derivative for both updates, and fixed T preserves worst-path scalar cost and expected objective loss.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 91c7099501fc6d74f9f5a3b350f881464c837b83facd0e91a464dfe828b8a701

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 615bba8fdca77df0a2d81672d7a626870fd5369e80eff221209f6387c030d16c

nu-acdm-v3-screen

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 65b1cbba3b92c5b2597926a0d5dcf1fe03cdb5fa8f518dbfc1c66a523473bc7a

Empty

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 6bf944f966212bfcbf491aacc256ad47af3e3449e5521f6d46bd94c3b7cd9f27

Unchanged randomized upper.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 330b40eea0b7500f57c01bcfb17d90baf05e4fd8490a9b34ec64e72fd4aff541

Randomized upper already contains C(1+R S_b/sqrt(epsilon)).

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: fa5916a3d2801be276916f7e00cbc63b59f93387de99368b7b236bdf675fe419

All adopted bounds and target parameters.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 0e2080133bcadf15d7721bdee1771588429547599dc20784d9f2b383788c42e0

Full target domain for the source beta=0 specialization.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 188cf933d08bcf3d99b01a370e5e36c102c0ce30fcc73003d39122e5f3f62bed

Theorem 6.1 gives expected gap<=2R^2 S_b^2/(T+1)^2, reproducing the stored order.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: ea76681495d8ac7c7b67e833a81d547200f754ff9dfa62d2856c15b219b1316b

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 295cf0d99c473adec31ec5d18fc3e77182ea37fd92749ffa5034b2441908f99a

Read arXiv:2609.10874v1, source 4cdec5889a00b9e7b2a81c80304f12e0d22bb3ef409eb46ce5d08112989e68a7, Theorem 1 PDF p.2 and reduction p.3, characters [3550,6701). The direct contracts differ. Existing converted bounds remain conditional baseline premises; a stronger new conversion remains unassessed.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 1669791fc8db9fee3cb3dd73b0d631e3b8c54188856756181ccd69d88c176596

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 4279db7cd31247d95e22b9e3467222c6da6a1bbda971f11ee236ad372a797fda

matrix-lower-direct-scope

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 0a1a8bb37e11ab08a6914dba569f8eafd31430b5037fe481d434a9a78b0c2d3a

Empty for the directly stated theorem

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 052536e2cf13aa804f3f0666ba0446ae2ecca0eb968abc7fd21e57bb93e6b87a

Unchanged; the direct matrix theorem is not adopted as a new coordinate bound.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: 6dd451f27cdcbe01ddb244ed213728fe9b07c912519cb2e0524db1d9d1a5a3e3

Frozen coordinate-oracle envelopes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 24e600226c8b5f7a52f0145c247048f8ddab1b4a87324b532827b919ea7df379

Every adopted coordinate bracket.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: d54f1b5af0f83a6c2a334ebfd259a9f1b43fbdf5d90ae56bd1d5ac018f27cfef

Source theorem: matrix-vector oracle, kappa>=C, small relative residual tolerance, sufficient dimension of order T^2, success probability 2/3.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 30959a692381eccfcce022aebe67e8208721c22f4179d4cc64303a36a156ab28

Theorem 1 and its adjacent reduction state matrix-product and strongly convex relative-error results rather than the target initial-distance coordinate quantity.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: ddf34da15e105b82b47a2cac50f8653a501d7417e0371fad346818cc6324d532

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 63f308ac815b3fbe3d529e7c24e7c405fe711cbe222b84a884b7b57f667a9bbb

Retain the exact unchanged native global differentiable convex full-space model, positive coordinate budgetsbj, publicx0 and a global minimizerx* at Euclidean distance<=R, both separateq1 quantities/views and the scalar coordinate-response cost. The accepted FO_COORDINATE_ZERO_QUERY proves directly from coordinate Lipschitzness and convexity: for h!=0, set S=sumj sqrt(bj)|hj| and thetaj=sqrt(bj)|hj|/S on its support. Coordinate integration and convexity at x+h=sumj thetaj(x+(hj/thetaj)ej) give f(x+h)<=f(x)+<gradf(x),h>+S²/2<=f(x)+<gradf(x),h>+(sumj bj)||h||²/2. At the GLOBAL unconstrained minimizer gradf(x*)=0, so f(x0)-f*<=beta_sum R²/2. This argument uses the declared global objective domain, not a constrained-boundary minimizer premise or a grant of a full-gradient query. On each exact native r6 including equality epsilon>=beta_sum R²/2, the SAME deterministic algorithm returningpublicx0 without any calls therefore meets pointwise gap<=epsilon on everyinstance. It also meets the randomized expected-loss criterion by embedding a deterministic algorithm in that view. All initialization calls are zero and each path's scalar-query cap is0. The existing matching lower indicator is1{epsilon<beta_sumR²/2}; onr6 it is0, agreeing with nonnegative counts and the exact minimized cost0. Thus publish a separate optimalq1 comparison for each view, without merging their IDs or attributing a scalar-positive ratio. No0/0 ratio is formed. The existing lower proof's opposite rank-one quadratic hypotheses shows strict-below-threshold impossibility but no new positive-cost main rate is needed here. Native r6 already includes its positive-parameter r2 universe. No b_j=0,R=0,constraineddomain or newaccuracy extension is asserted. The existing positive/full comparisons keep other_quantified_gap, and equal-constant/source-dimension guards remain exactly as before. This is publication of a previously accepted endpoint proof, not a new external theorem or blind discovery.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 13184086e9629ad57277f9c8ad7a471b5f02d8e4c259c1ac87bc379773ccf6da

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 560e6cf0fd1a149e96b768ce70c855af7171d3d63eb12d09f4fa6bef47ee88a2

SO_FO_O01_cv__deterministic__deterministic__c_zero

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: 504cc054d68beda454fec328ceae164cdffef5ff47aa37a8cec054935facb5e0

SO_FO_O01_cv__randomized__expected_loss__c_zero

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: 3dd8bbeff98508164edf8d1d3aa5a7ee7cf517770b6169572bbc15e70407001f

coordinate_zero_native_publication_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 2406ffa59683bd2969f971c2bd4f5055f04453d02d0e49437cc4a74d5e971c99

Native publication only; no new inequality, positive main-rate gain or strict extension of the old certified domain.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: 7249f099445029410a160bddb6fd935004aff56d921f462672a9f41815a78001

explicit_region_registration

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 2e6ea1cfd8dc45cbc2b8df1dc7d8cc7ec7413df51d1097db09394330b2080c81

Two separate native optimalq1 entries now publish exact0 with inapplicable multiplicative ratio.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: 417dfd1642809fff88c14c74cf69c8835c693dd68aa145e2e3c6f5fe9e890a20

The accepted proof and broad comparison envelopes already contained exact0 on each native r6 but had no separately optimal native regional comparison.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 2715a81b88fdfe98d94a2a517d36891a5cb324463cad487908e68bff0bf08de9

All original comparison objects, q2 identities, positive-accuracy/source-dimension guards and unassessed complements.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: aa08371dd8cb008ff6d9f86655f143ac1810fe22b9294442e936ac518bd60487

Exact existing r6 for each fixedview:positivebj,R,d and epsilon>=beta_sumR²/2.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: fd03f1d34aa2b3987d34eac1cb3a58bc33cd1f68e5fecaac75906d1061fdc4c2

Return the existingpublicx0 with0scalar responses on everypath.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: dc78db3b374577276f8d5bc967580cea70035bd40e3ec9fbeac66c68009c9966

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: 56d9e66e2b9e81d38efa09f7945f6b7dcc51e209c7f0ffd714ef558bc9d54771

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration. This revision addresses the preserved actual independent-review issues. Publication and typed projection obligations are explicit; every mathematical formula and adoption guard is verified against the exact native candidate, and historical effects are not reported as new frontier gains.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: d4fda4eb5936951c267eb09c135080a021ae47fd07c67766d0669d82ebd2bd7c

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/5/comparison_ids/1; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native item 3

Native pointer: /joint_analysis/impact/5/comparison_ids/2; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native item 4

Native pointer: /joint_analysis/impact/5/comparison_ids/3; canonical SHA-256: 560e6cf0fd1a149e96b768ce70c855af7171d3d63eb12d09f4fa6bef47ee88a2

SO_FO_O01_cv__deterministic__deterministic__c_zero

#### Native item 5

Native pointer: /joint_analysis/impact/5/comparison_ids/4; canonical SHA-256: 504cc054d68beda454fec328ceae164cdffef5ff47aa37a8cec054935facb5e0

SO_FO_O01_cv__randomized__expected_loss__c_zero

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: 65646d83c01b6ace4db606ad6d1ca4f140221d67dd9d0176dd64cf298e954bbd

curated_feedback_SO_FO_O01_cv_20261116_2a144b4edf

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/5/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/5/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/5/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/5/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/5/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: 8389b9e48793584de1f92f12ccc61e9c6b9faacb1f4b390d4a31c4bc93cb7ebb

d is an integer >=1, every b_j>0, R>0 and epsilon>0. The target is the minimax number of scalar coordinate-derivative calls with a uniform worst-path budget, separately for deterministic pointwise g1 (deterministic q1) and randomized expected-loss g1 (randomized q1). The common b is used only where b_j=b for every j; it is not an additional unconstrained input. beta_sum=sum_j b_j and S_b=sum_j sqrt(b_j) retain their native definitions.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 68fbf282fae07471b407ae4cd65a1dbd5dde54f1efce5a3370f570662154a24b

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 7b6d2f7862642df194415efe912c950a8a27dc53efc8770585b4deff53554e79

Independent review of the exact retained premises, new native proof, guarded deterministic patch and prepared joint analysis.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 3860d4113d33c3bb1b4ed016eb5ac7f8f7911f2500aafded123c8f5db8ee2adc

Broader literature queries and sharper heterogeneous-coordinate lower bounds remain unassessed; the terminal exact-ID page is not a literature-exhaustion certificate.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 21fdf4a985abd6d5e12957cd392ed16c538dd38812a35719d7257c1b69c05466

Any stronger finite-dimensional initial-distance expected-loss reduction from arXiv:2609.10874v1 is outside this local delta.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 5039088c29d0c120e7ec98e299592fc3c8108dd045418cc2caa406d46bcd0c7a

Sharp one-dimensional lower bounds and extensions of the diagonal risk inequality beyond the selected sufficient branch remain unassessed.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 38dd335d035d41fe29a0e84de9fa359b119cee71167c378a4873a58da6f78f50

Assess the guarded directional transfer of deterministic q2 bounds b3/b4 to q1 comparison c1; preserve both quantity IDs and all equal-constant, accuracy and source-dimension guards before any adoption.

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: f183a94dae7e07427ea16437043a5d9184c0bd07bbd3b2db41d44ad19a40e978

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 36283b35e55f77df43780debd234a9193bb55e1f3e5ee2593d7fffbcf9bfe44f

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: eba896c6b8d3c69d6ddca1b001750cfae3d9108487154b23af784b37110fba47

SO_FO_O01_cv__deterministic__deterministic__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 317a5bdb6c2ad967c103f9d1beb0bc9e5a9b58b1fe1a2084c7bb0b45389b4bd7

Conditional retention with identical scientific contract and guard.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 431abe2d716f21bab798860b7264c315ccabbcfcbdae844e174434b7adb0840f

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: d44957cd082e2cec70b37225acc2e73e28272e57eba5ce04693207a9f3a97ec5

FO_COORDINATE_SMOOTH

#### Native item 2

Native pointer: /joint_analysis/provenance/0/proof_refs/1; canonical SHA-256: 735f5d57c9e45cc1d5f6066a9a38bba20fa288fadcc1ad315ae708ee5b59119d

FO_SMOOTH_LOCALIZATION

#### Native item 3

Native pointer: /joint_analysis/provenance/0/proof_refs/2; canonical SHA-256: eb9c08cbdcaf3ce27cd3966b384038e6e91bf05a0d67f6d3ecad83aa6d0e5a1e

FO_CERTIFICATE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 6c6d4dc151373031765087da530598a8a59b517f9bd70d9253fa7693e22011c2

Frozen applicability; external premises not recertified.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 6d470765fe28b13be7722e4fdf9ed2efc910c392f1a244d012c6630929c978f4

Frozen /bounds/0; canonical parent hash is recorded in the annotation finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: e91f6c813ef56cb76e091ee7a4e5afd475a988040ea51613cce07350bbad3f4b

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native item 2

Native pointer: /joint_analysis/provenance/0/source_refs/1; canonical SHA-256: 559a56b1b57844e3c568387a9ebb4d7cbcaf1e98ec7a31a094efd65fa367c08c

SO_SRC_3db9732ed66f3b8c

#### Native item 3

Native pointer: /joint_analysis/provenance/0/source_refs/2; canonical SHA-256: a2cd77f7d9b231a6aa4b43e047274fe80a546f2eda06c8b43f4f125d862ff120

SO_SRC_c729895b420a5000

#### Native item 4

Native pointer: /joint_analysis/provenance/0/source_refs/3; canonical SHA-256: 9aa4cfa7d9a55fe74b6acccc9d4369f9379589cff2486fc75a9d717fcb9aa355

SO_SRC_da45f3a56f11d157

#### Native item 5

Native pointer: /joint_analysis/provenance/0/source_refs/4; canonical SHA-256: 9daedb2ac95e8088053c7f30d00e8b484004c953b15791fc665f3978350e6bba

SO_SRC_c314bae252a3b929

#### Native item 6

Native pointer: /joint_analysis/provenance/0/source_refs/5; canonical SHA-256: f49cfd2461dd4b0132f4f0fa2a90e3f29883781b5ad0bff19390f24edc0bff0c

SO_SRC_88e665bbd463b203

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: c13e78f53cca703a047362f3aac70473444a5013a506abb0983ccf13406587a1

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 8c10521d2c0fd49da6c80fe65f9630181757724ae1446a35c8b872d4e376752b

SO_FO_O01_cv__deterministic__deterministic__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 317a5bdb6c2ad967c103f9d1beb0bc9e5a9b58b1fe1a2084c7bb0b45389b4bd7

Conditional retention with identical scientific contract and guard.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 431abe2d716f21bab798860b7264c315ccabbcfcbdae844e174434b7adb0840f

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: d44957cd082e2cec70b37225acc2e73e28272e57eba5ce04693207a9f3a97ec5

FO_COORDINATE_SMOOTH

#### Native item 2

Native pointer: /joint_analysis/provenance/1/proof_refs/1; canonical SHA-256: 735f5d57c9e45cc1d5f6066a9a38bba20fa288fadcc1ad315ae708ee5b59119d

FO_SMOOTH_LOCALIZATION

#### Native item 3

Native pointer: /joint_analysis/provenance/1/proof_refs/2; canonical SHA-256: eb9c08cbdcaf3ce27cd3966b384038e6e91bf05a0d67f6d3ecad83aa6d0e5a1e

FO_CERTIFICATE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 6c6d4dc151373031765087da530598a8a59b517f9bd70d9253fa7693e22011c2

Frozen applicability; external premises not recertified.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 1615e831c4657064ae701e8ce9b4f573358b974c75e49323939fd28aad73d7dd

Frozen /bounds/1; canonical parent hash is recorded in the annotation finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: e91f6c813ef56cb76e091ee7a4e5afd475a988040ea51613cce07350bbad3f4b

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native item 2

Native pointer: /joint_analysis/provenance/1/source_refs/1; canonical SHA-256: 559a56b1b57844e3c568387a9ebb4d7cbcaf1e98ec7a31a094efd65fa367c08c

SO_SRC_3db9732ed66f3b8c

#### Native item 3

Native pointer: /joint_analysis/provenance/1/source_refs/2; canonical SHA-256: a2cd77f7d9b231a6aa4b43e047274fe80a546f2eda06c8b43f4f125d862ff120

SO_SRC_c729895b420a5000

#### Native item 4

Native pointer: /joint_analysis/provenance/1/source_refs/3; canonical SHA-256: 9aa4cfa7d9a55fe74b6acccc9d4369f9379589cff2486fc75a9d717fcb9aa355

SO_SRC_da45f3a56f11d157

#### Native item 5

Native pointer: /joint_analysis/provenance/1/source_refs/4; canonical SHA-256: 9daedb2ac95e8088053c7f30d00e8b484004c953b15791fc665f3978350e6bba

SO_SRC_c314bae252a3b929

#### Native item 6

Native pointer: /joint_analysis/provenance/1/source_refs/5; canonical SHA-256: f49cfd2461dd4b0132f4f0fa2a90e3f29883781b5ad0bff19390f24edc0bff0c

SO_SRC_88e665bbd463b203

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: b69dded11ee49c37525163b31cd9485eb474c4f74a480d767cdfed8a0e7db0ad

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 825f6831d9371d7760b8ce7b87a830b3a01ea2805a83fe019346c27291673f3d

SO_FO_O01_cv__deterministic__deterministic__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 374aaecf198d0ab7a7f97051999d53572c0b0f1e55a1f66f4eb847a1105539e5

Conditional retention of the zero-query output x0.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 36027080a5b45ff82a84f8d3f7a27254330c4b7a894f32c3ecfd5db565905340

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 2da9d98d1f9bc9a8bb3694b64ad72383805d2734df4ac67effea3c4e4bd95037

Retained coordinate-smooth initial-distance argument.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: d6cefdd0f414ce9d31a41fbae5ef2bb58d6b1ee78039953e79013d232bdeea68

Frozen /bounds/9 and /proofs/3; canonical hashes are recorded in the annotation finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: b473b9c587a11c7390e7c462836a57d9929d635333d351440fe501c3f5087ab2

#### Native item 1

Native pointer: /joint_analysis/provenance/2/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: def4f579abf55efa3a0d28110a44c976076cac3eb1d4b0e1b4a46c07ce01a315

epsilon>=beta_sum R^2/2

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 94b3e79b6f69886a9f49f551fd5319f22f3d5e238630f83f804b24cbcb559e59

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: c03dca2ca53c1d5fb6a64bf851bc8b9fd3eaae818cf4c4e444ae160ab71ed033

SO_FO_O01_cv__deterministic__deterministic__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 56ff10e7a898e020cf9c300057a991f5e177d29770ca086c4f0304549c3e3396

Conditional retention; one-call necessity strictly below the zero-query threshold.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 36027080a5b45ff82a84f8d3f7a27254330c4b7a894f32c3ecfd5db565905340

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 63b095bd3e6cf210325c5267b652a587aebe493c7ea8a8dfdaa6a85d365cca64

Retained opposite rank-one quadratic argument.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 79a668ec0bf76a7508af78f75cfbee3770aa1421ba09ea3e4d15d168afa3fb80

Frozen /bounds/10 and /proofs/3; canonical hashes are recorded in the annotation finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: b473b9c587a11c7390e7c462836a57d9929d635333d351440fe501c3f5087ab2

#### Native item 1

Native pointer: /joint_analysis/provenance/3/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 4dc128a795c514013cae06bc8e89bf12f7eb9f956854fb4cf8f445e951642f28

Full target domain with the native indicator

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: 9099f0f828c20983fe83da27a7f685991e79ee1b341b453160456a6b6c1a6883

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: da76177ea1614b700983092662ce01fb8258e217f41010b5a789d1607a753483

SO_FO_O01_cv__randomized__expected_loss__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: 19ce6bd5b24039ffa02440f3194df3ff9d8c37f58667184855b496794357a41f

Conditional retention with identical expected-loss and worst-path scalar-cost contract.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 844205e397351249a309bcce62d81f418cc0960001710d85e69f31e1f6dc82c7

Frozen applicability; unchanged source theorem additionally screened in nu-acdm-v3-screen.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: dbfb129fbfbc18a4efec80f4f7aa6706e8d65a4cf923f57d0fab8b3c3aad1b3a

Frozen /bounds/4; canonical parent hash is recorded in the annotation finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: c59b5b5d11792dc4aa4c5b90992f25de2704246134b50b92c9ae4cc714542e98

#### Native item 1

Native pointer: /joint_analysis/provenance/4/source_refs/0; canonical SHA-256: 1c4468ae370e0f86cbcbd8574540983aa81008ca2682cef1330c9a1165377169

SO_SRC_c372bbbf5326fa91

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: 4289adb35b85bcbdaca3e20f20aaab5ce4bb26fcbb9919d22c792ef800497b0d

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: b51819312d23200e6daa313beac4ed522102f19e2feb8a6a0b7aad1d22dbe63c

SO_FO_O01_cv__randomized__expected_loss__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 317a5bdb6c2ad967c103f9d1beb0bc9e5a9b58b1fe1a2084c7bb0b45389b4bd7

Conditional retention with identical scientific contract and guard.

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 431abe2d716f21bab798860b7264c315ccabbcfcbdae844e174434b7adb0840f

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: d44957cd082e2cec70b37225acc2e73e28272e57eba5ce04693207a9f3a97ec5

FO_COORDINATE_SMOOTH

#### Native item 2

Native pointer: /joint_analysis/provenance/5/proof_refs/1; canonical SHA-256: 735f5d57c9e45cc1d5f6066a9a38bba20fa288fadcc1ad315ae708ee5b59119d

FO_SMOOTH_LOCALIZATION

#### Native item 3

Native pointer: /joint_analysis/provenance/5/proof_refs/2; canonical SHA-256: eb9c08cbdcaf3ce27cd3966b384038e6e91bf05a0d67f6d3ecad83aa6d0e5a1e

FO_CERTIFICATE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: 6c6d4dc151373031765087da530598a8a59b517f9bd70d9253fa7693e22011c2

Frozen applicability; external premises not recertified.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: 2ee56779d750cfa6029bed647f0a4e626698cf7c140df854781ddacd57d84cba

Frozen /bounds/5; canonical parent hash is recorded in the annotation finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: e91f6c813ef56cb76e091ee7a4e5afd475a988040ea51613cce07350bbad3f4b

#### Native item 1

Native pointer: /joint_analysis/provenance/5/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native item 2

Native pointer: /joint_analysis/provenance/5/source_refs/1; canonical SHA-256: 559a56b1b57844e3c568387a9ebb4d7cbcaf1e98ec7a31a094efd65fa367c08c

SO_SRC_3db9732ed66f3b8c

#### Native item 3

Native pointer: /joint_analysis/provenance/5/source_refs/2; canonical SHA-256: a2cd77f7d9b231a6aa4b43e047274fe80a546f2eda06c8b43f4f125d862ff120

SO_SRC_c729895b420a5000

#### Native item 4

Native pointer: /joint_analysis/provenance/5/source_refs/3; canonical SHA-256: 9aa4cfa7d9a55fe74b6acccc9d4369f9379589cff2486fc75a9d717fcb9aa355

SO_SRC_da45f3a56f11d157

#### Native item 5

Native pointer: /joint_analysis/provenance/5/source_refs/4; canonical SHA-256: 9daedb2ac95e8088053c7f30d00e8b484004c953b15791fc665f3978350e6bba

SO_SRC_c314bae252a3b929

#### Native item 6

Native pointer: /joint_analysis/provenance/5/source_refs/5; canonical SHA-256: f49cfd2461dd4b0132f4f0fa2a90e3f29883781b5ad0bff19390f24edc0bff0c

SO_SRC_88e665bbd463b203

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: 8ee00b5f14091814bde7739c1ff67f2ff9ad973f1748ec1c74eaf66ea15a2544

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: 1b007c71f61af05d4157b583e66541cd067126142b2aa5bfabfde58d1f7c0f6d

SO_FO_O01_cv__randomized__expected_loss__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: 317a5bdb6c2ad967c103f9d1beb0bc9e5a9b58b1fe1a2084c7bb0b45389b4bd7

Conditional retention with identical scientific contract and guard.

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: 431abe2d716f21bab798860b7264c315ccabbcfcbdae844e174434b7adb0840f

#### Native item 1

Native pointer: /joint_analysis/provenance/6/proof_refs/0; canonical SHA-256: d44957cd082e2cec70b37225acc2e73e28272e57eba5ce04693207a9f3a97ec5

FO_COORDINATE_SMOOTH

#### Native item 2

Native pointer: /joint_analysis/provenance/6/proof_refs/1; canonical SHA-256: 735f5d57c9e45cc1d5f6066a9a38bba20fa288fadcc1ad315ae708ee5b59119d

FO_SMOOTH_LOCALIZATION

#### Native item 3

Native pointer: /joint_analysis/provenance/6/proof_refs/2; canonical SHA-256: eb9c08cbdcaf3ce27cd3966b384038e6e91bf05a0d67f6d3ecad83aa6d0e5a1e

FO_CERTIFICATE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: 6c6d4dc151373031765087da530598a8a59b517f9bd70d9253fa7693e22011c2

Frozen applicability; external premises not recertified.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: 1a2f46056eceb2e6c026d0d51fbe518509966bd72658c48ccf6c299906862fb1

Frozen /bounds/6; canonical parent hash is recorded in the annotation finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: e91f6c813ef56cb76e091ee7a4e5afd475a988040ea51613cce07350bbad3f4b

#### Native item 1

Native pointer: /joint_analysis/provenance/6/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native item 2

Native pointer: /joint_analysis/provenance/6/source_refs/1; canonical SHA-256: 559a56b1b57844e3c568387a9ebb4d7cbcaf1e98ec7a31a094efd65fa367c08c

SO_SRC_3db9732ed66f3b8c

#### Native item 3

Native pointer: /joint_analysis/provenance/6/source_refs/2; canonical SHA-256: a2cd77f7d9b231a6aa4b43e047274fe80a546f2eda06c8b43f4f125d862ff120

SO_SRC_c729895b420a5000

#### Native item 4

Native pointer: /joint_analysis/provenance/6/source_refs/3; canonical SHA-256: 9aa4cfa7d9a55fe74b6acccc9d4369f9379589cff2486fc75a9d717fcb9aa355

SO_SRC_da45f3a56f11d157

#### Native item 5

Native pointer: /joint_analysis/provenance/6/source_refs/4; canonical SHA-256: 9daedb2ac95e8088053c7f30d00e8b484004c953b15791fc665f3978350e6bba

SO_SRC_c314bae252a3b929

#### Native item 6

Native pointer: /joint_analysis/provenance/6/source_refs/5; canonical SHA-256: f49cfd2461dd4b0132f4f0fa2a90e3f29883781b5ad0bff19390f24edc0bff0c

SO_SRC_88e665bbd463b203

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: dd135dbae3d714e68aedeac234c256e65acbdc5f560a6bca5025fb1639bd6841

Full target domain

#### Native item 8

Native pointer: /joint_analysis/provenance/7; canonical SHA-256: 7d756fef731cc2ae27efb528f0eb4d6edf007e77a512fd275059a03cc4368fdc

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/7/bound_id; canonical SHA-256: b3153a06df0e5fed6430330b5540fab189e709cb63d7bd70bdc7b55e7153ca77

SO_FO_O01_cv__randomized__expected_loss__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/7/mapping; canonical SHA-256: 3f03fe4a7414f79f36b1ddfa38c998997130eedeee2e248b108e1725b54733b8

Conditional retention of the existing randomized q1 lower.

#### Native field: origin

Native pointer: /joint_analysis/provenance/7/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/7/proof_refs; canonical SHA-256: 431abe2d716f21bab798860b7264c315ccabbcfcbdae844e174434b7adb0840f

#### Native item 1

Native pointer: /joint_analysis/provenance/7/proof_refs/0; canonical SHA-256: d44957cd082e2cec70b37225acc2e73e28272e57eba5ce04693207a9f3a97ec5

FO_COORDINATE_SMOOTH

#### Native item 2

Native pointer: /joint_analysis/provenance/7/proof_refs/1; canonical SHA-256: 735f5d57c9e45cc1d5f6066a9a38bba20fa288fadcc1ad315ae708ee5b59119d

FO_SMOOTH_LOCALIZATION

#### Native item 3

Native pointer: /joint_analysis/provenance/7/proof_refs/2; canonical SHA-256: eb9c08cbdcaf3ce27cd3966b384038e6e91bf05a0d67f6d3ecad83aa6d0e5a1e

FO_CERTIFICATE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/7/source_domain; canonical SHA-256: 880fe8a8a3c90cd491d11a6e2b13e45eb9b5b004585d8321434f5e4674d229d9

Frozen equal-constant diagonal-information branch.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/7/source_locator; canonical SHA-256: cdeced144d65526b9673d78e866d16c9eb8c1564c9a9a00c229ed08274c93929

Frozen /bounds/7; canonical parent hash is recorded in the annotation finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/7/source_refs; canonical SHA-256: e91f6c813ef56cb76e091ee7a4e5afd475a988040ea51613cce07350bbad3f4b

#### Native item 1

Native pointer: /joint_analysis/provenance/7/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native item 2

Native pointer: /joint_analysis/provenance/7/source_refs/1; canonical SHA-256: 559a56b1b57844e3c568387a9ebb4d7cbcaf1e98ec7a31a094efd65fa367c08c

SO_SRC_3db9732ed66f3b8c

#### Native item 3

Native pointer: /joint_analysis/provenance/7/source_refs/2; canonical SHA-256: a2cd77f7d9b231a6aa4b43e047274fe80a546f2eda06c8b43f4f125d862ff120

SO_SRC_c729895b420a5000

#### Native item 4

Native pointer: /joint_analysis/provenance/7/source_refs/3; canonical SHA-256: 9aa4cfa7d9a55fe74b6acccc9d4369f9379589cff2486fc75a9d717fcb9aa355

SO_SRC_da45f3a56f11d157

#### Native item 5

Native pointer: /joint_analysis/provenance/7/source_refs/4; canonical SHA-256: 9daedb2ac95e8088053c7f30d00e8b484004c953b15791fc665f3978350e6bba

SO_SRC_c314bae252a3b929

#### Native item 6

Native pointer: /joint_analysis/provenance/7/source_refs/5; canonical SHA-256: f49cfd2461dd4b0132f4f0fa2a90e3f29883781b5ad0bff19390f24edc0bff0c

SO_SRC_88e665bbd463b203

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/7/target_domain; canonical SHA-256: e85eaf6869024c9689fdce594bf5ac1e80daaf68858b8589c1228d0860f86bd8

b_j=b>0 for every j and 0<epsilon<=c bR^2

#### Native item 9

Native pointer: /joint_analysis/provenance/8; canonical SHA-256: f2ef1a01442f08d5f1da6461b9ae3e643a0450544ff7e716f03ff5eed4326350

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/8/bound_id; canonical SHA-256: 752732da4061f2b7d93a4016da15d44cc38174d3fcd5c04bb51604452d746f57

SO_FO_O01_cv__randomized__expected_loss__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/8/mapping; canonical SHA-256: 17b3176811bda565dab94657e550713c742782f99cc46b22a408aec2b6d060a9

Conditional retention with native source, dimension, guarantee and cost guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/8/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/8/source_domain; canonical SHA-256: 11e6abdf2bf6be86cbe940bbc239baa4a43985d3d2295d3309707facd71eea87

Frozen converted full-gradient lower; complete historical conversion not freshly recertified.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/8/source_locator; canonical SHA-256: 8c35c1d7e4db86e3c17c84bcf71a38ef318342d9fa58d9a4e533a7206cda32ce

Frozen /bounds/8; canonical parent hash is recorded in the annotation finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/8/source_refs; canonical SHA-256: 64598e5f5ac8dd470410dac4dc6be6680cf855f3dd59a38e2c84c0e545ed063c

#### Native item 1

Native pointer: /joint_analysis/provenance/8/source_refs/0; canonical SHA-256: b16d20412234a21b7d751ad148856511c79c81bf7535570d39faedcbd0ba1d21

SO_SRC_cdf1550d10cb341b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/8/target_domain; canonical SHA-256: e436734b23eab008f39d302c76c0abecdb07ecf540d3533481107a0125b7aa21

b_j=b>0 for every j and 0<epsilon<=c bR^2 and d>=C bR^2/epsilon

#### Native item 10

Native pointer: /joint_analysis/provenance/9; canonical SHA-256: a114e1f314ec666b917451ea436c5ee17aaa5fc5d791ac59c9bdb1c23ea690ae

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/9/bound_id; canonical SHA-256: 1c798694907312bd28fdc500ae3fb79b6098f6f3fec378670c1b100a0c041196

SO_FO_O01_cv__randomized__expected_loss__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/9/mapping; canonical SHA-256: a6980bb1cc37b10e69c4eaac4dc8c056ea20661bc98475d310a702b0b875c2b9

Conditional retention of the zero-query output x0; excluded from disjoint randomized c1.

#### Native field: origin

Native pointer: /joint_analysis/provenance/9/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/9/proof_refs; canonical SHA-256: 36027080a5b45ff82a84f8d3f7a27254330c4b7a894f32c3ecfd5db565905340

#### Native item 1

Native pointer: /joint_analysis/provenance/9/proof_refs/0; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/9/source_domain; canonical SHA-256: 2da9d98d1f9bc9a8bb3694b64ad72383805d2734df4ac67effea3c4e4bd95037

Retained coordinate-smooth initial-distance argument.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/9/source_locator; canonical SHA-256: bfa40a3939a5f8272820ea4b46a74d821ceeddbf2cec5f9b16a31aa18ba2d0cd

Frozen /bounds/11 and /proofs/3; canonical hashes are recorded in the annotation finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/9/source_refs; canonical SHA-256: b473b9c587a11c7390e7c462836a57d9929d635333d351440fe501c3f5087ab2

#### Native item 1

Native pointer: /joint_analysis/provenance/9/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/9/target_domain; canonical SHA-256: def4f579abf55efa3a0d28110a44c976076cac3eb1d4b0e1b4a46c07ce01a315

epsilon>=beta_sum R^2/2

#### Native item 11

Native pointer: /joint_analysis/provenance/10; canonical SHA-256: fc31cc671f1e624f8fbf48665b5fe745eb6b56c01e2d35aacb6a055ce146f7a6

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/10/bound_id; canonical SHA-256: 9103521008b15c9f17feb9f646c05fb9a833e303d76a68c50e7fe2ab1b2fca76

SO_FO_O01_cv__randomized__expected_loss__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/10/mapping; canonical SHA-256: 1f98157805073f7c4b76ca465d60913f4537bc142b0cd9809888524152646e17

Conditional retention of the one-call expected-loss lower with worst-path budgets.

#### Native field: origin

Native pointer: /joint_analysis/provenance/10/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/10/proof_refs; canonical SHA-256: 36027080a5b45ff82a84f8d3f7a27254330c4b7a894f32c3ecfd5db565905340

#### Native item 1

Native pointer: /joint_analysis/provenance/10/proof_refs/0; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/10/source_domain; canonical SHA-256: 63b095bd3e6cf210325c5267b652a587aebe493c7ea8a8dfdaa6a85d365cca64

Retained opposite rank-one quadratic argument.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/10/source_locator; canonical SHA-256: b57f8a4d1435e802cc9f465cb08d44b53ca70d14b7bb50f6742bae8100794a1e

Frozen /bounds/12 and /proofs/3; canonical hashes are recorded in the annotation finding.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/10/source_refs; canonical SHA-256: b473b9c587a11c7390e7c462836a57d9929d635333d351440fe501c3f5087ab2

#### Native item 1

Native pointer: /joint_analysis/provenance/10/source_refs/0; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/10/target_domain; canonical SHA-256: 4dc128a795c514013cae06bc8e89bf12f7eb9f956854fb4cf8f445e951642f28

Full target domain with the native indicator

#### Native item 12

Native pointer: /joint_analysis/provenance/11; canonical SHA-256: 45db5c1d876f3a003e492a6b0a5aa405d467854c9f85b3a424cafc34d3f1609f

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/11/bound_id; canonical SHA-256: 5706b96400d4fe05a6da50688db973968f5b42fb1a8c87b547e1bf00d462c4b2

SO_FO_O01_cv__deterministic__deterministic__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/11/mapping; canonical SHA-256: 7406a0b0f0f9df8a4d7ecbc262a801416badab8ce98e92ee86e606897084c404

Every hard instance belongs to the immutable class. A deterministic pointwise algorithm is an expected-loss algorithm with degenerate randomness; the retained risk inequality forces T>=3d/4. Queries, outputs and worst-path scalar costs are preserved. No q2 identity merger is used.

#### Native field: origin

Native pointer: /joint_analysis/provenance/11/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/11/proof_refs; canonical SHA-256: a99edcd2c6ccf116aa9c835e607af90cb719ab8a9938ad24ffc5cd4afaedcc39

#### Native item 1

Native pointer: /joint_analysis/provenance/11/proof_refs/0; canonical SHA-256: f57567364bf52f50da0f2cd9800ff70c9f9eb9cd2ef52ce941880f03e8fdb879

FO_COORDINATE_DIAGONAL_DET_Q1

#### Native item 2

Native pointer: /joint_analysis/provenance/11/proof_refs/1; canonical SHA-256: d44957cd082e2cec70b37225acc2e73e28272e57eba5ce04693207a9f3a97ec5

FO_COORDINATE_SMOOTH

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/11/source_domain; canonical SHA-256: 869f1673bf79330f26e263b701954e946f01cce60e01a6e0bc1d60b2ae31b7ec

Independent-sign diagonal quadratics with equal b, optimizer distance R and arbitrary adaptive coordinate queries.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/11/source_locator; canonical SHA-256: c83eb4254ddaed85a293e8b2eae8936a35f1ef3a0c2a6c51efd76b988ae0f694

Frozen /proofs/0, canonical hash 908b109d57b75d57bc2f95589983adf234dfba1d4abcf2751dbf47d27f8f8b61; full new native proof FO_COORDINATE_DIAGONAL_DET_Q1.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/11/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/11/target_domain; canonical SHA-256: 799afd02f309fe8f884a390b44f7a3f64a8561e240d4e10b25e51b787c7cee7d

b_j=b>0 for every j and 0<epsilon<=bR^2/8

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 1e12c754de36a75eccf3861ba74cc09d741efdf2817246e2a67e6b6d36b46e9a

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: d9ce4bf9b1c9a468e42b5e85cb8436134a8c5b10448fd5b68c6c04b352bcb088

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 560e6cf0fd1a149e96b768ce70c855af7171d3d63eb12d09f4fa6bef47ee88a2

SO_FO_O01_cv__deterministic__deterministic__c_zero

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: 504cc054d68beda454fec328ceae164cdffef5ff47aa37a8cec054935facb5e0

SO_FO_O01_cv__randomized__expected_loss__c_zero

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: d4d3066227543deefb2bd165a10a4f8922532486377109007e37e62d29936c86

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: f44902418633a6a927c42d0e451b78fdca596b9167d496f6305c3031528c835c

No new blind literature search in this migration. Conditional retention of the exact preceding accepted analysis and its finite historical scope; all stated pending work remains pending.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 3689135faa53a95dfc1eda78a546042bb93255ef822eeabbd29ea1d958d6a229

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 4b0f8c6cfe05edf9205b8b27c82eca33de12b39d446a41398454fb1f9e585f99

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: 4d92409f540159006d2cac33b21e868515ab7c92994dfcbf9f9c9a8a42d403a3

The complete compatible candidate dispositions are recorded in the corresponding bound-use ledger. The newly published zero regions are supported by FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116 and acceptedFO_COORDINATE_ZERO_QUERY; original positive comparisons retain their guarded min/max/status unchanged. No distinctq2 row is adopted by this declaration.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 290138d9251907ccd3e74379306dcf256c68a56cd05f08bb89010bafdfd39b5c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: eba896c6b8d3c69d6ddca1b001750cfae3d9108487154b23af784b37110fba47

SO_FO_O01_cv__deterministic__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 8c10521d2c0fd49da6c80fe65f9630181757724ae1446a35c8b872d4e376752b

SO_FO_O01_cv__deterministic__deterministic__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 825f6831d9371d7760b8ce7b87a830b3a01ea2805a83fe019346c27291673f3d

SO_FO_O01_cv__deterministic__deterministic__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: c03dca2ca53c1d5fb6a64bf851bc8b9fd3eaae818cf4c4e444ae160ab71ed033

SO_FO_O01_cv__deterministic__deterministic__b6

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/4; canonical SHA-256: 5706b96400d4fe05a6da50688db973968f5b42fb1a8c87b547e1bf00d462c4b2

SO_FO_O01_cv__deterministic__deterministic__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 10f57901a31b4ab7c52dcc5e1aaa49270849a0d4aac8dfc0e65e0693d1a8f0a4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/id; canonical SHA-256: cbd717faae83a18dcd0984f69326879d0fe1418a4573e90441638e7d8eb23ec6

synthesis-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 105d56c89d95f7a582da04cd847a34c5fc3001d82d2c6e3ead9d9b82a16c15f9

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: 4d92409f540159006d2cac33b21e868515ab7c92994dfcbf9f9c9a8a42d403a3

The complete compatible candidate dispositions are recorded in the corresponding bound-use ledger. The newly published zero regions are supported by FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116 and acceptedFO_COORDINATE_ZERO_QUERY; original positive comparisons retain their guarded min/max/status unchanged. No distinctq2 row is adopted by this declaration.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 290138d9251907ccd3e74379306dcf256c68a56cd05f08bb89010bafdfd39b5c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: eba896c6b8d3c69d6ddca1b001750cfae3d9108487154b23af784b37110fba47

SO_FO_O01_cv__deterministic__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 8c10521d2c0fd49da6c80fe65f9630181757724ae1446a35c8b872d4e376752b

SO_FO_O01_cv__deterministic__deterministic__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 825f6831d9371d7760b8ce7b87a830b3a01ea2805a83fe019346c27291673f3d

SO_FO_O01_cv__deterministic__deterministic__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: c03dca2ca53c1d5fb6a64bf851bc8b9fd3eaae818cf4c4e444ae160ab71ed033

SO_FO_O01_cv__deterministic__deterministic__b6

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/4; canonical SHA-256: 5706b96400d4fe05a6da50688db973968f5b42fb1a8c87b547e1bf00d462c4b2

SO_FO_O01_cv__deterministic__deterministic__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: caa2db72d179220c784d8040d38ab11342ef512e8387cb47bf1b5f5515fda65d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 560e6cf0fd1a149e96b768ce70c855af7171d3d63eb12d09f4fa6bef47ee88a2

SO_FO_O01_cv__deterministic__deterministic__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: ebcba919e62a1ab3932a5511960ae541204ef3e4e612a3e2b58eaa7aea342c2d

synthesis-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: ad2fad369d0bbfb40cdd7b8120accb5533d9cbc7d7b4a328c081f83d79896e04

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: 4d92409f540159006d2cac33b21e868515ab7c92994dfcbf9f9c9a8a42d403a3

The complete compatible candidate dispositions are recorded in the corresponding bound-use ledger. The newly published zero regions are supported by FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116 and acceptedFO_COORDINATE_ZERO_QUERY; original positive comparisons retain their guarded min/max/status unchanged. No distinctq2 row is adopted by this declaration.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 9c32cb14113550e74de9b474e601176681034ea00bf1a52383710f80ed100151

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: da76177ea1614b700983092662ce01fb8258e217f41010b5a789d1607a753483

SO_FO_O01_cv__randomized__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: b51819312d23200e6daa313beac4ed522102f19e2feb8a6a0b7aad1d22dbe63c

SO_FO_O01_cv__randomized__expected_loss__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: 1b007c71f61af05d4157b583e66541cd067126142b2aa5bfabfde58d1f7c0f6d

SO_FO_O01_cv__randomized__expected_loss__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: b3153a06df0e5fed6430330b5540fab189e709cb63d7bd70bdc7b55e7153ca77

SO_FO_O01_cv__randomized__expected_loss__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/4; canonical SHA-256: 752732da4061f2b7d93a4016da15d44cc38174d3fcd5c04bb51604452d746f57

SO_FO_O01_cv__randomized__expected_loss__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/5; canonical SHA-256: 1c798694907312bd28fdc500ae3fb79b6098f6f3fec378670c1b100a0c041196

SO_FO_O01_cv__randomized__expected_loss__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/6; canonical SHA-256: 9103521008b15c9f17feb9f646c05fb9a833e303d76a68c50e7fe2ab1b2fca76

SO_FO_O01_cv__randomized__expected_loss__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: acbc9994beb945925cd2a25c2d714e6b4c1fd4f6c363d2a4f1ca4b1c0d090130

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 94ebdcb021bcbc6fc94fa708c1e7a7f9d1afd6248b96e70935fa7df176e425ff

synthesis-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: bb4bcd099616e813795ac57ac03c009e62e1599c5b6dd7433d43979d96662b20

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: 4d92409f540159006d2cac33b21e868515ab7c92994dfcbf9f9c9a8a42d403a3

The complete compatible candidate dispositions are recorded in the corresponding bound-use ledger. The newly published zero regions are supported by FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116 and acceptedFO_COORDINATE_ZERO_QUERY; original positive comparisons retain their guarded min/max/status unchanged. No distinctq2 row is adopted by this declaration.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 9c32cb14113550e74de9b474e601176681034ea00bf1a52383710f80ed100151

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: da76177ea1614b700983092662ce01fb8258e217f41010b5a789d1607a753483

SO_FO_O01_cv__randomized__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: b51819312d23200e6daa313beac4ed522102f19e2feb8a6a0b7aad1d22dbe63c

SO_FO_O01_cv__randomized__expected_loss__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: 1b007c71f61af05d4157b583e66541cd067126142b2aa5bfabfde58d1f7c0f6d

SO_FO_O01_cv__randomized__expected_loss__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/3; canonical SHA-256: b3153a06df0e5fed6430330b5540fab189e709cb63d7bd70bdc7b55e7153ca77

SO_FO_O01_cv__randomized__expected_loss__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/4; canonical SHA-256: 752732da4061f2b7d93a4016da15d44cc38174d3fcd5c04bb51604452d746f57

SO_FO_O01_cv__randomized__expected_loss__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/5; canonical SHA-256: 1c798694907312bd28fdc500ae3fb79b6098f6f3fec378670c1b100a0c041196

SO_FO_O01_cv__randomized__expected_loss__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/6; canonical SHA-256: 9103521008b15c9f17feb9f646c05fb9a833e303d76a68c50e7fe2ab1b2fca76

SO_FO_O01_cv__randomized__expected_loss__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 32a77b5b28fac0ad9e1fbb1df7797211eb35172f72da09a358be36a1b4a92d46

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: 7f1a6540bd14dbb3bcfdfdfac9a64bfde09607556bb3c904bfc43adedf6ede22

synthesis-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 4b300dcb742140d568d3f6d9292217311e21d09e19b952b37cfbe5518ac2db18

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: 4d92409f540159006d2cac33b21e868515ab7c92994dfcbf9f9c9a8a42d403a3

The complete compatible candidate dispositions are recorded in the corresponding bound-use ledger. The newly published zero regions are supported by FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116 and acceptedFO_COORDINATE_ZERO_QUERY; original positive comparisons retain their guarded min/max/status unchanged. No distinctq2 row is adopted by this declaration.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 9c32cb14113550e74de9b474e601176681034ea00bf1a52383710f80ed100151

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/0; canonical SHA-256: da76177ea1614b700983092662ce01fb8258e217f41010b5a789d1607a753483

SO_FO_O01_cv__randomized__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/1; canonical SHA-256: b51819312d23200e6daa313beac4ed522102f19e2feb8a6a0b7aad1d22dbe63c

SO_FO_O01_cv__randomized__expected_loss__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/2; canonical SHA-256: 1b007c71f61af05d4157b583e66541cd067126142b2aa5bfabfde58d1f7c0f6d

SO_FO_O01_cv__randomized__expected_loss__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/3; canonical SHA-256: b3153a06df0e5fed6430330b5540fab189e709cb63d7bd70bdc7b55e7153ca77

SO_FO_O01_cv__randomized__expected_loss__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/4; canonical SHA-256: 752732da4061f2b7d93a4016da15d44cc38174d3fcd5c04bb51604452d746f57

SO_FO_O01_cv__randomized__expected_loss__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/5; canonical SHA-256: 1c798694907312bd28fdc500ae3fb79b6098f6f3fec378670c1b100a0c041196

SO_FO_O01_cv__randomized__expected_loss__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/6; canonical SHA-256: 9103521008b15c9f17feb9f646c05fb9a833e303d76a68c50e7fe2ab1b2fca76

SO_FO_O01_cv__randomized__expected_loss__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 908c23cf4388d1b348319ee55f23756edeb09d4de01fc4e7d6b997c3b1bcda90

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 504cc054d68beda454fec328ceae164cdffef5ff47aa37a8cec054935facb5e0

SO_FO_O01_cv__randomized__expected_loss__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: ca0bbdf769e92b6ee0fc04da5960cb413f34af9e8cc0d5eca08f2ac29f71ac8f

synthesis-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: e7fc0a14e711f0607c823f8632288e4a53e041c75ed64f1276be939c2f2631c5

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs/0; canonical SHA-256: 69f30cd2486f3fcffd61cca105bfb5e22a0f56435fd843f7b0eb4046c9aac6b3

FO_COORDINATE_ZERO_NATIVE_PUBLICATION_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs/1; canonical SHA-256: f648aed2dac44dec5ef99a70fa12fae52d906f19c9166f8d72ef9664a30c7b7f

FO_COORDINATE_ZERO_QUERY

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 682414682e0c2d553291e0bc12062018d8ce449eb835ee14b4cee32224853986

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: f2357fe5fb0182b6a7a6ac18a791b3110d3fe9127b0c028fa1873c076b264e73

This retained lead is not resolved by publication of the existingzero endpoint.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: d4fda4eb5936951c267eb09c135080a021ae47fd07c67766d0669d82ebd2bd7c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/2; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/3; canonical SHA-256: 560e6cf0fd1a149e96b768ce70c855af7171d3d63eb12d09f4fa6bef47ee88a2

SO_FO_O01_cv__deterministic__deterministic__c_zero

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/4; canonical SHA-256: 504cc054d68beda454fec328ceae164cdffef5ff47aa37a8cec054935facb5e0

SO_FO_O01_cv__randomized__expected_loss__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 7b6d2f7862642df194415efe912c950a8a27dc53efc8770585b4deff53554e79

Independent review of the exact retained premises, new native proof, guarded deterministic patch and prepared joint analysis.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: c9e1eefa9fa04be3408d3a1774fbbba5e02a0ee658e0d617ee2552759ff9bb74

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: f2357fe5fb0182b6a7a6ac18a791b3110d3fe9127b0c028fa1873c076b264e73

This retained lead is not resolved by publication of the existingzero endpoint.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: d4fda4eb5936951c267eb09c135080a021ae47fd07c67766d0669d82ebd2bd7c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/2; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/3; canonical SHA-256: 560e6cf0fd1a149e96b768ce70c855af7171d3d63eb12d09f4fa6bef47ee88a2

SO_FO_O01_cv__deterministic__deterministic__c_zero

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/4; canonical SHA-256: 504cc054d68beda454fec328ceae164cdffef5ff47aa37a8cec054935facb5e0

SO_FO_O01_cv__randomized__expected_loss__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 3860d4113d33c3bb1b4ed016eb5ac7f8f7911f2500aafded123c8f5db8ee2adc

Broader literature queries and sharper heterogeneous-coordinate lower bounds remain unassessed; the terminal exact-ID page is not a literature-exhaustion certificate.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 18ea2708ce44395c45877997ce995aadab76c9dc4e16500c0ce8a84c9dbea967

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: f2357fe5fb0182b6a7a6ac18a791b3110d3fe9127b0c028fa1873c076b264e73

This retained lead is not resolved by publication of the existingzero endpoint.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: d4fda4eb5936951c267eb09c135080a021ae47fd07c67766d0669d82ebd2bd7c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/2; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/3; canonical SHA-256: 560e6cf0fd1a149e96b768ce70c855af7171d3d63eb12d09f4fa6bef47ee88a2

SO_FO_O01_cv__deterministic__deterministic__c_zero

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/4; canonical SHA-256: 504cc054d68beda454fec328ceae164cdffef5ff47aa37a8cec054935facb5e0

SO_FO_O01_cv__randomized__expected_loss__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 21fdf4a985abd6d5e12957cd392ed16c538dd38812a35719d7257c1b69c05466

Any stronger finite-dimensional initial-distance expected-loss reduction from arXiv:2609.10874v1 is outside this local delta.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: 57ede18474e4a3fbba74586ceeacafc34df396efd390b950e521045c60f194af

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: f2357fe5fb0182b6a7a6ac18a791b3110d3fe9127b0c028fa1873c076b264e73

This retained lead is not resolved by publication of the existingzero endpoint.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: d4fda4eb5936951c267eb09c135080a021ae47fd07c67766d0669d82ebd2bd7c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/2; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/3; canonical SHA-256: 560e6cf0fd1a149e96b768ce70c855af7171d3d63eb12d09f4fa6bef47ee88a2

SO_FO_O01_cv__deterministic__deterministic__c_zero

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/4; canonical SHA-256: 504cc054d68beda454fec328ceae164cdffef5ff47aa37a8cec054935facb5e0

SO_FO_O01_cv__randomized__expected_loss__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 5039088c29d0c120e7ec98e299592fc3c8108dd045418cc2caa406d46bcd0c7a

Sharp one-dimensional lower bounds and extensions of the diagonal risk inequality beyond the selected sufficient branch remain unassessed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 9451b11d58ec5b39118cc90867a285466663726a536b4d720534869cafb57012

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: 800385358df10f7b21848374691fe4d01d82077ecd63688c9aaff2afc370b1a3

Native SO_FO_O01_cv__deterministic__deterministic__b3 andb4 use a distinctq2 quantity. Matching scalar-call labels do not certify an identity. Review exact source/target minimax convention, algorithm/guarantee and resource maps on their originalr3/r4 guards; any legal consequence must then be compared with the already adoptedq1 max{indicator,3d/4 onr7}. The displayeddimension floor may already be order-dominated on its overlap, whereas the accuracy-dependent branch needs a guarded assessment. Neither is inserted intoq1 by this correction; no newpaper is claimed. The unresolved route affects only positive-cost synthesis, never the independently proved r6 zero closure.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: c1e2a21b3d4abb9e81a2f8470f60af47ce3cae6e03c476c4be9fa609611732f0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/0; canonical SHA-256: d3c74594111c5ff65bb7ff2801a76e79eaa89b0ea99c0f41936a7446ea2aff06

SO_FO_O01_cv__deterministic__deterministic__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/1; canonical SHA-256: faef1860e81bdbc44ab3ca15d0c9b55c9f51b656f9d75983fa5645c6c32ae512

SO_FO_O01_cv__deterministic__deterministic__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 61bf14ddac0e7bc5f66bd7c2693931e0392f590e34803aa91615b5754998b1b2

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids/0; canonical SHA-256: b52807322b26a1676463a92c8a0aa839d60dd3b11eae1a04d8700722fbb060e0

equal-high-dimension

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids/1; canonical SHA-256: 62a3ef5bc5c7cb659b8a4a76935e6a3cd38c8647d21698291001ff52c899cea0

equal-small-accuracy-other-dimension

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 10f57901a31b4ab7c52dcc5e1aaa49270849a0d4aac8dfc0e65e0693d1a8f0a4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: ed02ce53c84d15709d48cecf3a3352656b2f343c68e5c1709d79abc1f5457f76

deterministic-q2-to-q1-positive-route

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 38dd335d035d41fe29a0e84de9fa359b119cee71167c378a4873a58da6f78f50

Assess the guarded directional transfer of deterministic q2 bounds b3/b4 to q1 comparison c1; preserve both quantity IDs and all equal-constant, accuracy and source-dimension guards before any adoption.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: fd8c66cea99f64ff8060dc6f8f9a9c0f4c5192a39c3e4085ba7a88b421a378c0

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/argument; canonical SHA-256: 800385358df10f7b21848374691fe4d01d82077ecd63688c9aaff2afc370b1a3

Native SO_FO_O01_cv__deterministic__deterministic__b3 andb4 use a distinctq2 quantity. Matching scalar-call labels do not certify an identity. Review exact source/target minimax convention, algorithm/guarantee and resource maps on their originalr3/r4 guards; any legal consequence must then be compared with the already adoptedq1 max{indicator,3d/4 onr7}. The displayeddimension floor may already be order-dominated on its overlap, whereas the accuracy-dependent branch needs a guarded assessment. Neither is inserted intoq1 by this correction; no newpaper is claimed. The unresolved route affects only positive-cost synthesis, never the independently proved r6 zero closure.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs; canonical SHA-256: c1e2a21b3d4abb9e81a2f8470f60af47ce3cae6e03c476c4be9fa609611732f0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/0; canonical SHA-256: d3c74594111c5ff65bb7ff2801a76e79eaa89b0ea99c0f41936a7446ea2aff06

SO_FO_O01_cv__deterministic__deterministic__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/1; canonical SHA-256: faef1860e81bdbc44ab3ca15d0c9b55c9f51b656f9d75983fa5645c6c32ae512

SO_FO_O01_cv__deterministic__deterministic__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids; canonical SHA-256: 61bf14ddac0e7bc5f66bd7c2693931e0392f590e34803aa91615b5754998b1b2

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids/0; canonical SHA-256: b52807322b26a1676463a92c8a0aa839d60dd3b11eae1a04d8700722fbb060e0

equal-high-dimension

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids/1; canonical SHA-256: 62a3ef5bc5c7cb659b8a4a76935e6a3cd38c8647d21698291001ff52c899cea0

equal-small-accuracy-other-dimension

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: 10f57901a31b4ab7c52dcc5e1aaa49270849a0d4aac8dfc0e65e0693d1a8f0a4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 8f7461301073f5983cd51083043470e29020a83f045679b44ec5d450b3a88bc2

deterministic-q2-to-q1-positive-route-material-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 38dd335d035d41fe29a0e84de9fa359b119cee71167c378a4873a58da6f78f50

Assess the guarded directional transfer of deterministic q2 bounds b3/b4 to q1 comparison c1; preserve both quantity IDs and all equal-constant, accuracy and source-dimension guards before any adoption.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: 6a88d909b389d682066b28fee794148d14d5cc14ea4ab659baee1012df4e4bbd

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: d4fda4eb5936951c267eb09c135080a021ae47fd07c67766d0669d82ebd2bd7c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: ed1cccee674a7bdb7f2f7623e57647f280b85ed4f0863efb7f7cee099ba5209c

SO_FO_O01_cv__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/1; canonical SHA-256: d7c86a40c4af9165aec8ed6a6605d24185cfa53640bb099e61de69fcd3a4157e

SO_FO_O01_cv__randomized__expected_loss__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/2; canonical SHA-256: 8b6ab0405a86ab727dce54c68b5ec4b47689626804c1e7da0082546aab39ba19

SO_FO_O01_cv__randomized__expected_loss__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/3; canonical SHA-256: 560e6cf0fd1a149e96b768ce70c855af7171d3d63eb12d09f4fa6bef47ee88a2

SO_FO_O01_cv__deterministic__deterministic__c_zero

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/4; canonical SHA-256: 504cc054d68beda454fec328ceae164cdffef5ff47aa37a8cec054935facb5e0

SO_FO_O01_cv__randomized__expected_loss__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: 7b66618750ce506ccf40819cef50f764846b4ebf660cc36789c8ef551ca05dfe

curated-scope-limit-2a144b4edf

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 3def15dd525c170c41308d206cfb035a0a05c1a97a4f112e578be83625069ced

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 8e1c31ce2035615e38fefca4469565bf063b9b3b43a5bfb33c3c489d7780ad6e

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 4b81cab280b1e31c2ea7afa9a416577b7c9c22795698d5d642e0394c36a90edd

/quantities/2

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native item 7

Native pointer: /joint_analysis/target/contract_refs/6; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 186ed335e1402e2425ecd40c6839c0006bc1338f6afd136df6de45ea09b764fd

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 50450be9de3eed05dc8cd0b3f62b1411730f417846d41d7be6c950da8ad210fc

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: 16790c9ac362633c11194d5bbb36a2ac535b6a0d71bdc030a058c6330a8eabec

Sufficiently small universal proof constant; the retained diagonal certificates permit c<=1/8. Values may differ between theorems.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: ecd2856c19924845d1fb827b3f4ec2886a1a3f4e8c8321ec1cba9249e9fe9ce9

SO_FO_O01_cv_p_b48b2597a7

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 879923da020d1533f4d8e921ea7bac61e8ba41d3c89d17a4d14e3a89c6780d5d

c

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: b69d673d093ef769600fb02515037086235a92dd328ff6c00824d1a9873d6b62

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: d2bb86df93e6668bcc6fcf9602c2ae3ef156fee57e220dfa5840dd3addc85391

Sufficiently large universal proof constant, independent of all joint variables; values may differ between theorems.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: 281891ab5f9dfb8a41155ad2425c76ce5f429536c0a74d57e083122d3cafffb4

SO_FO_O01_cv_p_5eeb762d76

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: c2e8c0cc2e73b9bd1ba9ef1979e73169b471e25b0e9909efe98fde462c0bf55f

C

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 8389b9e48793584de1f92f12ccc61e9c6b9faacb1f4b390d4a31c4bc93cb7ebb

d is an integer >=1, every b_j>0, R>0 and epsilon>0. The target is the minimax number of scalar coordinate-derivative calls with a uniform worst-path budget, separately for deterministic pointwise g1 (deterministic q1) and randomized expected-loss g1 (randomized q1). The common b is used only where b_j=b for every j; it is not an additional unconstrained input. beta_sum=sum_j b_j and S_b=sum_j sqrt(b_j) retain their native definitions.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: ced141c0bbb4c2da3399f0d1bbc904e3e0f2b5c8c25024d0dcca6cd13d8ca1db

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: a6c76b3ace6af2eaaea597799d63d8cc0a5c128c2ed7fe68aab74fa70fea0723

SO_FO_O01_cv_p_b4e942dc3f

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 373c10fb79091778180db18ab0b080c7b3b16c4928e75801662007d980b62fef

SO_FO_O01_cv_p_172ae36314

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 3ef60e056923dcb763914843d7edf040657fbeda83e3c13746e369bb19bdeccd

SO_FO_O01_cv_p_6c03ab1cb0

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: 3e26d892c370e612a74e31fc4ac10e92434cc3193e25e4b2a7ce956a9c7a5a07

SO_FO_O01_cv_p_4497cc9e5d

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 72535fabb77d1a7750f0ac5921f572c51dafe93b23d5fe1b4ad2b10831f4ff90

SO_FO_O01_cv_p_95775a4b65

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: ced141c0bbb4c2da3399f0d1bbc904e3e0f2b5c8c25024d0dcca6cd13d8ca1db

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: a6c76b3ace6af2eaaea597799d63d8cc0a5c128c2ed7fe68aab74fa70fea0723

SO_FO_O01_cv_p_b4e942dc3f

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 373c10fb79091778180db18ab0b080c7b3b16c4928e75801662007d980b62fef

SO_FO_O01_cv_p_172ae36314

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 3ef60e056923dcb763914843d7edf040657fbeda83e3c13746e369bb19bdeccd

SO_FO_O01_cv_p_6c03ab1cb0

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 3e26d892c370e612a74e31fc4ac10e92434cc3193e25e4b2a7ce956a9c7a5a07

SO_FO_O01_cv_p_4497cc9e5d

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 72535fabb77d1a7750f0ac5921f572c51dafe93b23d5fe1b4ad2b10831f4ff90

SO_FO_O01_cv_p_95775a4b65

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 9 September 2026; preprint v1. Theorem 1 (PDF p. 2); strongly convex quadratic reduction (p. 3); the dimension $O(T^2)$ in equation (7) (p. 7)..

https://arxiv.org/pdf/2609.10874

[2] Zeyuan Allen-Zhu, Zheng Qu, Peter Richtarik and Yang Yuan. Even Faster Accelerated Coordinate Descent Using Non-Uniform Sampling. 2016; Definition 4.2; Theorems 5.1 and 6.1, full version PDF pp.9 and 13.

https://arxiv.org/pdf/1512.09103

[3] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015.

https://arxiv.org/pdf/1405.4980

[4] Yoel Drori; Adrien Taylor. On the oracle complexity of smooth strongly convex minimization. 2021; arXiv:2101.09740v2.

https://arxiv.org/pdf/2101.09740v2

[5] Yoel Drori. Exact oracle complexity for function-value suboptimality under weighted initial conditions. 2026-10-16; preprintv2.

https://arxiv.org/pdf/2609.33360v2

[6] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 2026-09-09; preprintv1.

https://arxiv.org/pdf/2609.10874

[7] Arkadi Nemirovski; Shmuel Onn; Uriel G. Rothblum. Accuracy Certificates for Computational Problems with Convex Structure. 2010.

https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf

[8] David Martínez-Rubio; Cristóbal Guzmán. Stable Movement for Nondual Lipschitz Convex Optimization: Efficiency and Nearly Optimal Oracle Rates. 2026-09-17; preprintv1.

https://arxiv.org/pdf/2609.20701
