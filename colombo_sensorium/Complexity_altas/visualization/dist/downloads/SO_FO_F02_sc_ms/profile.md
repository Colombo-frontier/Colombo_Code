# Finite-sum minimization with possibly nonconvex components: strongly convex average and mean-square component smoothness; selected component gradients

**Setting ID.** `SO_FO_F02_sc_ms`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Possibly nonconvex components; convexity: Strongly convex; geometry: Full space; smoothness: Lipschitz gradient; smoothness: Mean square smooth components; structure: Finite sum

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Component gradient; operation: Component gradient; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; adaptivity: Explicit restriction; computation: Internal arithmetic uncharged; randomization: Deterministic algorithms; randomization: Private randomness allowed; restriction: Linear span; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; budget: Worst-instance expected cost; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \mathbb{R}^d}F(x)$$

The complete objective is the finite sum $F(x)=n^{-1}\sum_{i=1}^n f_i(x)$. Component information is available only through the declared component oracle.

### Admissible model

$F=\frac1n\sum_{i=1}^n f_i$, where the components may be nonconvex. The average $F$ is globally $\mu$-strongly convex and has initial suboptimality at most $\Delta$. The components are mean-square smooth: $\frac1n\sum_{i=1}^n\|\nabla f_i(x)-\nabla f_i(y)\|_2^2\le\beta^2\|x-y\|_2^2$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad n \ge 1,\quad \mu > 0\\\kappa \ge 1,\quad \varepsilon \le c\,\Delta,\quad \beta > 0,\quad \Delta > 0\\\mu \le \beta\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ n,\ \varepsilon$.

Public upper bounds: $\beta,\ \Delta$.

Public lower bounds: $\mu$.

The unknown objects are the component functions $f_1,\ldots,f_n$.

For each query, the algorithm chooses $i\in\{1,\ldots,n\}$ and $x\in\mathbb R^d$ and receives the following information about that component.

$$\nabla f_i(x)$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=F(\widehat{x})-F^\star$$

$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One selected-component gradient costs one call; a two-point difference costs two, and a full gradient costs $n$.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

**Resource qualification.** Cost is bounded in expectation for every instance: $\sup_{I,\mathcal O}\mathbb E N_A\le T$. This contract is not replaced by a fixed bound on every execution path.

#### Randomized / Linear span / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

Queries and outputs belong to the permitted span of historical gradients. Randomized index selection is allowed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

**Output qualification.** The output must also satisfy the support, atomic-hull, or historical-span restriction of its algorithm view. An unqueried output remains subject to these restrictions.

**Resource qualification.** Cost is bounded in expectation for every instance: $\sup_{I,\mathcal O}\mathbb E N_A\le T$. This contract is not replaced by a fixed bound on every execution path.

#### Deterministic / Pointwise guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

**Resource qualification.** Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f_i,F$: Unknown components and finite-sum objective **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\frac1n\sum_{i=1}^n f_i(x)$$

$\nabla f_i$: Full gradient of differentiable component $i$

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$n$: Public number of components in the finite sum or finite maximum. **Domain:** $n\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta>0$.

$\mu$: Lower bound on the strong-convexity modulus of the objective specified by the model **Domain:** $\mu>0$.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\Delta$: Public upper bound on initial suboptimality. **Domain:** $\Delta>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$\kappa$: $\beta/\mu$.

$$\kappa=\frac{\beta}{\mu}$$

$d_{\rm dense}$: Sufficient finite dimension for Dense Weak Hiding v3. The theorem takes the worst case over finite dimensions; it does not hold for every prescribed $d$. **Domain:** $d_{\rm dense}(n,\kappa,\Delta/\varepsilon)$.

$T$: Total budget for the declared resource projection; for a risk curve, the budget is fixed in advance **Domain:** $T\in\mathbb{N}_{\ge0}$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

$d_{\rm ZG}$: Sufficient dimension for the Zhou–Gu (2019), Theorem 4.1/4.2, lower-bound construction, chosen for the specified accuracy and parameters. This is not a fixed-low-dimensional conclusion. **Domain:** $d_{\rm ZG}=d_{\rm ZG}(n,\beta,\mu,R,\Delta,\varepsilon)$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One selected-component gradient costs one call; a two-point difference costs two, and a full gradient costs $n$.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Linear span / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One selected-component gradient costs one call; a two-point difference costs two, and a full gradient costs $n$.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One selected-component gradient costs one call; a two-point difference costs two, and a full gradient costs $n$.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - strongly convex average

**Region.** $\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$

**Views.** Randomized / Expected loss

**Quantity.** Q1

**Resource.** One selected-component gradient costs one call; a two-point difference costs two, and a full gradient costs $n$.

**Status.** Lower bound missing

**Lower bound.** B5

$$
\left.c[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]\right|_{n\ge1024,\ 3\le\kappa\le\sqrt n,\ d\ge d_{\rm dense}}
$$

**Upper bound.** B1, B2, B3, B10, B11

$$
\min\{C(n+n^{3/4}\sqrt\kappa)\log(C\Delta/\varepsilon),Cn\sqrt\kappa\log(C\Delta/\varepsilon),Cnd\log(2+\kappa\Delta/\varepsilon),\left.C[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]\right|_{1\le\kappa\le\sqrt n},\left.n\right|_{\kappa=1}\}
$$

**Comparison argument.** Each guarded term is usable only on its recorded region. The lower side is recorded only on r3; it remains missing on r2 minus r3, so missing_lower status is retained. b4 is covered at the same rate by b6 on r3 and is retained actively in c2. The kappa=1 n-call upper endpoint and the PAGE extension do not assert matching lower bounds outside r3. See F02_MS_PAGE_GRADIENT_TRANSFER and F02_MS_UNIT_CONDITION_AND_GUARDS.

### R2 - Small-condition-number strongly convex average: arbitrary randomized algorithms

**Region.** $n\ge1024,\quad3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad0<\varepsilon\le c\Delta$

**Views.** Randomized / Expected loss

**Quantity.** Q1

**Resource.** One selected-component gradient costs one call; a two-point difference costs two, and a full gradient costs $n$.

**Status.** Optimal

**Lower bound.** B5

$$
c[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Upper bound.** B4

$$
C[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Gap or comparison.** $O(1)$

### R3 - High-accuracy regime for strongly convex averages under a span restriction

**Region.** $\kappa\ge4\sqrt n,\quad\varepsilon\le c\Delta\min\{1,n^{7/2}/\kappa^3\},\quad d\ge d_{\rm ZG}$

**Views.** Randomized / Linear span / Expected loss

**Quantity.** Q2

**Resource.** One selected-component gradient costs one call; a two-point difference costs two, and a full gradient costs $n$.

**Status.** Optimal

**Lower bound.** B7

$$
c[(n+n^{3/4}\sqrt\kappa)\log(\Delta/\varepsilon)]
$$

**Upper bound.** B6

$$
C[(n+n^{3/4}\sqrt\kappa)\log(C\Delta/\varepsilon)]
$$

**Gap or comparison.** $O(1)$

### R4 - strongly convex average

**Region.** $\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q3

**Resource.** One selected-component gradient costs one call; a two-point difference costs two, and a full gradient costs $n$.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B8, B9, B12

$$
\min\{Cn\sqrt\kappa\log(C\Delta/\varepsilon),Cnd\log(2+\kappa\Delta/\varepsilon),\left.n\right|_{\kappa=1}\}
$$

**Comparison argument.** The two retained general upper bounds and the new exact n-call endpoint are compared with their guards. The endpoint witness meets the deterministic guarantee and pathwise cost directly, without a randomized-to-deterministic conversion. No lower bound is adopted in this comparison.

## 4. Bounds and supporting evidence

### B1 - Katyusha X

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C[(n+n^{3/4}\sqrt\kappa)\log(C\Delta/\varepsilon)]
$$

**Sources.** [1](https://arxiv.org/pdf/1802.03866) [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf)

**Conditions.** $$\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [1](https://arxiv.org/pdf/1802.03866) theorem: Corollaries4.4 and4.7; PDF pp.13–14

**Source location.** [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) theorem: Definition3.3; Thm4.1/4.2; §4.3 Proposition4.9

### B2 - Full-gradient acceleration

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
Cn\sqrt\kappa\log(C\Delta/\varepsilon)
$$

**Sources.** [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://arxiv.org/pdf/2101.09740v2) [6](https://arxiv.org/pdf/2609.33360v2) [7](https://arxiv.org/pdf/2609.10874) [8](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [9](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_FINITE_SUM_SIMULATION, FO_SMOOTH_LOCALIZATION, FO_CERTIFICATE

### B3 - Gradient-only cutting planes valid in every dimension

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
Cnd\log(2+\kappa\Delta/\varepsilon)
$$

**Sources.** [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://arxiv.org/pdf/2101.09740v2) [6](https://arxiv.org/pdf/2609.33360v2) [7](https://arxiv.org/pdf/2609.10874) [8](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [9](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_FINITE_SUM_SIMULATION, FO_SMOOTH_LOCALIZATION, FO_CERTIFICATE

### B4 - restarted PAGE

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Sources.** [3](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** $$n\ge1024,\quad3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $n\ge1024,\quad3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [3](https://arxiv.org/pdf/2609.00045v3) theorem: Thm3.3 small-κ hard instance; PropE.2; AppendicesF,G.1

### B5 - Dense hiding under individual smoothness and strong convexity of the average

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Sources.** [3](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** $$n\ge1024,\quad3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $n\ge1024,\quad3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: selected component gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [3](https://arxiv.org/pdf/2609.00045v3) theorem: Thm3.3 small-κ hard instance; PropE.2; AppendicesF,G.1

### B6 - Katyusha X

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Linear span / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C[(n+n^{3/4}\sqrt\kappa)\log(C\Delta/\varepsilon)]
$$

**Sources.** [1](https://arxiv.org/pdf/1802.03866) [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf)

**Conditions.** $$\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [1](https://arxiv.org/pdf/1802.03866) theorem: Corollaries4.4 and4.7; PDF pp.13–14

**Source location.** [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) theorem: Definition3.3; Thm4.1/4.2; §4.3 Proposition4.9

### B7 - Span-restricted lower bound under mean-square smoothness

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Linear span / Expected loss

**Witness or lower-bound scope.** The stated restricted randomized class

$$
c[(n+n^{3/4}\sqrt\kappa)\log(\Delta/\varepsilon)]
$$

**Sources.** [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf)

**Conditions.** $$\kappa\ge4\sqrt n,\quad\varepsilon\le c\Delta\min\{1,n^{7/2}/\kappa^3\},\quad d\ge d_{\rm ZG}$$

**Dimension conditions.** $\kappa\ge4\sqrt n,\quad\varepsilon\le c\Delta\min\{1,n^{7/2}/\kappa^3\},\quad d\ge d_{\rm ZG}$

**Oracle correspondence.** Applicable interfaces: selected component gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) theorem: Definition3.3; Thm4.1/4.2; §4.3 Proposition4.9

### B8 - Full-gradient acceleration

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
Cn\sqrt\kappa\log(C\Delta/\varepsilon)
$$

**Sources.** [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://arxiv.org/pdf/2101.09740v2) [6](https://arxiv.org/pdf/2609.33360v2) [7](https://arxiv.org/pdf/2609.10874) [8](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [9](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_FINITE_SUM_SIMULATION, FO_SMOOTH_LOCALIZATION, FO_CERTIFICATE

### B9 - Gradient-only cutting planes valid in every dimension

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
Cnd\log(2+\kappa\Delta/\varepsilon)
$$

**Sources.** [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://arxiv.org/pdf/2101.09740v2) [6](https://arxiv.org/pdf/2609.33360v2) [7](https://arxiv.org/pdf/2609.10874) [8](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [9](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\mu>0,\kappa\ge1,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_FINITE_SUM_SIMULATION, FO_SMOOTH_LOCALIZATION, FO_CERTIFICATE

### B10 - Restarted PAGE with optimized epoch length; all dimensions

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Sources.** [3](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** $1\le\kappa\le\sqrt n,\quad d,n\ge1,\quad0<\varepsilon\le c\Delta$

**Dimension conditions.** Every prescribed integer d>=1; no dense dimension threshold.

**Oracle correspondence.** Algorithm 1 uses only selected-component gradients; refresh n calls, sampled two-point difference two calls.

**Guarantee conversion.** Expected objective gap and expected total component calls as in the target view; no fixed-path conversion.

**Output rule.** Unrestricted feasible point in R^d; the random epoch iterate is allowed.

**Resource conversion.** Include every full-gradient initialization and every refresh/difference; expected epoch cost <=n+3T.

**Local argument.** F02_MS_PAGE_GRADIENT_TRANSFER

**Source location.** [3](https://arxiv.org/pdf/2609.00045v3) pdf pages: 9; 47; 48; 49; printed pages: 9; 47; 48; 49; theorem: arXiv:2609.00045v3, revised 2026-10-10; Algorithm 1; Lemma E.1; Proposition E.2, equations (287)-(301); source characters 26000-30500 and 111000-119000

Version date independently read at arXiv abstract-page hash d88373783cb5c75296e816a8273ec11eefd02187ce7561ef55440fc45f5db74d, characters 0-5012; before cutoff 2026-11-15.

### B11 - Exact full-gradient solution of the known-curvature average

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
n
$$

**Conditions.** $\kappa=1,\quad d,n\ge1,\quad0<\varepsilon\le c\Delta$

**Dimension conditions.** Every prescribed d>=1 and n>=1.

**Oracle correspondence.** Query all n component gradients at x0; use their average and the public mu.

**Guarantee conversion.** Loss is exactly zero on every instance; deterministic n-call cost implies the required expected loss and expected cost.

**Output rule.** Return x0-grad F(x0)/mu, a feasible unqueried point.

**Resource conversion.** Exactly n component calls; arithmetic is uncharged.

**Local argument.** F02_MS_UNIT_CONDITION_AND_GUARDS

### B12 - Exact full-gradient solution of the known-curvature average

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
n
$$

**Conditions.** $\kappa=1,\quad d,n\ge1,\quad0<\varepsilon\le c\Delta$

**Dimension conditions.** Every prescribed d>=1 and n>=1.

**Oracle correspondence.** Query all n component gradients at x0; use their average and the public mu.

**Guarantee conversion.** Loss is zero for every instance and cost is exactly n on every execution; this meets the deterministic view.

**Output rule.** Return x0-grad F(x0)/mu, a feasible unqueried point.

**Resource conversion.** Exactly n component calls; arithmetic is uncharged.

**Local argument.** F02_MS_UNIT_CONDITION_AND_GUARDS

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 33fee5326748f66b7dbe42a9e198e7437b608d9044c7e06046a431d12f60cd5d

### Native proof: FO_FINITE_SUM_SIMULATION

Native pointer: /proofs/0; canonical SHA-256: e0e52a7a0b52fa5ea926c6ff98ff378655f40506a1700d6de84ee934a3e0d72d

#### Native field: algorithm_scope

Native pointer: /proofs/0/algorithm_scope; canonical SHA-256: 54b22f9df96b3af77f502f428142dafbd52c9d5944316dc0773d7d3cca042157

Deterministic full-gradient upper witnesses; lower constructions preserve their source algorithm scopes.

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: eedbf388be57d4b9f5311b551148d991409660b948f1ff7c60644f5630f9f21d

A full gradient of $F=n^{-1}\sum_i f_i$ costs $n$ component calls. Mean-square smoothness implies
$$
\|\nabla F(x)-\nabla F(y)\|
\le(n^{-1}\sum_i\|\nabla f_i(x)-\nabla f_i(y)\|^2)^{1/2}
\le\beta\|x-y\|.
$$
Individual smoothness also implies this. Full-gradient convex, strongly convex, PL, stationarity, and certificate algorithms therefore transfer with an $n$ multiplier. A zero-query endpoint remains zero. Convexity or PL of the average must be stated separately.

For an unrestricted smooth finite-sum $\Omega(n)$ baseline, hide an index $J$. All components have public quadratic curvature $\beta$; only component $J$ has an unknown linear term $\mp n\beta R x_1$. Their average is
$\beta\|x\|^2/2\mp\beta Rx_1$, with minimizer distance $R$. Until $J$ is queried, its sign is hidden. A budget much smaller than $n$ misses it with constant probability, giving loss of order $\beta R^2$. This construction requires a model allowing the component linear offsets.

For an expected-budget lower-bound conversion, truncate after a sufficiently large constant multiple of the expected budget. Markov's inequality makes truncation unlikely enough to preserve a constant-probability hard-instance lower bound. This does not convert an expected-budget upper bound to a pathwise budget.

Replicating the same hard function in every component preserves its one-function lower bound without multiplying by $n$. This covers nonsmooth strongly convex and one-dimensional logarithmic subclasses.

In the cited span-restricted construction, individual smoothness is $\sqrt n$ times the native mean-square parameter. Substitute native parameter $\beta/\sqrt n$ to obtain the recorded individual-smoothness lower bound. Keep the original span, dimension, and accuracy restrictions. Rescaling does not expand the lower algorithm class.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: 7c83750816f39269726e96b627ac9a4b969b056051086340b78b2fbaa1fb2e53

Replication gives no extra factor n. The rescaled lower theorem remains span-restricted.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 57c28cd8c12418c1ded62146ad8b357d232bc0b4a97c9de169f7364a267c91ba

Exact component gradients; the declared average objective and component regularity.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 37a6d8ea889bdf26ae17da513902ea4efb82e84aa5dc5664db745dca61d4ab00

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 7c5c331dc2ff680b93cc77ba12a6361537df349221fd57f9e03efd62652269a1

SO_SRC_b8b05e6e898a4e32

#### Native item 2

Native pointer: /proofs/0/source_refs/1; canonical SHA-256: f636ed5cb2c3078753fe74a8d5e61f525482a9f5b53b6ac34ca8401dd49dc086

SO_SRC_a6e5b4d495f30052

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 3de444ffcd774c5bafc3f72220ec1cfb12fbcc30f2647bcfb800178cb2f44246

Finite-sum simulation and hidden components

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

### Native proof: F02_MS_PAGE_GRADIENT_TRANSFER

Native pointer: /proofs/3; canonical SHA-256: 54eea92c61366e70c68ee63689cc77ff8edb50b661df832e68e526008586146d

#### Native field: algorithm_scope

Native pointer: /proofs/3/algorithm_scope; canonical SHA-256: 16b0488a1b6b045a2c3652a55eef4695956d4e2f6f7f9b8d6f5d603c9f9c2945

Unrestricted randomized; no assertion of a deterministic algorithm.

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: ee3ef722a8986aca3d9ee8d4fc2d610e40307739475d5b47accdf624521c6697

Dense Weak Hiding arXiv:2609.00045v3 (2026-10-10), Algorithm 1, p.9, and Lemma E.1/Proposition E.2, pp.47-49; read characters 26000-30500 and 111000-119000. Strong convexity gives F(y)>=F(x)+<grad F(x),y-x>+mu||y-x||^2/2. Taking the infimum in y yields ||grad F(x)||^2>=2mu(F(x)-F*), so the source PL assumption follows without any assumption on component convexity. Set L_ms=beta and kappa_ms=beta/mu. Algorithm 1 computes only gradients: an initial/refresh mean costs n calls; a sampled difference costs two calls. With p_refresh=1/(n+1), its expected update cost is p_refresh*n+2(1-p_refresh)<=3. Put A=kappa(1+sqrt(n)), T=ceil(4(n+A)), q=A/T<=1/4, and s=ceil(log(Delta/epsilon)/log(1/q)). Lemma E.1 bounds conditional expected epoch gap by q times the input gap, and cost by n+3T. Tower expectation gives expected output gap <=q^s Delta<=epsilon and expected calls <=s(n+3T). For 1<=kappa<=sqrt(n), T=Theta(n), log(1/q)=Theta(1+log(sqrt(n)/kappa)), uniformly also at n=1. Thus cost is O(n+n log(Delta/epsilon)/(1+log(sqrt(n)/kappa))). No source function values, unknown F*, extra certificate, distance bound or prescribed high dimension are used.

#### Native field: limitations

Native pointer: /proofs/3/limitations; canonical SHA-256: 161b7dce92cf174886994dc66a7c6e33058c8046b540f843b595d07c63a57a48

An expected cost upper bound is not promoted to a deterministic or pathwise guarantee. The source PL lower bound for large kappa is not transferred to strongly convex objectives.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: 89771bed20409546ff2b6da7489cdc11194d6f2a9e7d1e56e5e43c40ffdc5364

Arbitrary randomized expected-gap, expected-component-call view; d,n>=1 and 1<=kappa<=sqrt(n).

#### Native field: source_hashes

Native pointer: /proofs/3/source_hashes; canonical SHA-256: f63bef320f078321764bebc2b58c8f3aa1805b3de7123b2f61bf863f29a200e5

#### Native item 1

Native pointer: /proofs/3/source_hashes/0; canonical SHA-256: 0b800da789a72cd0c44c24db5645e41fd5d54da2ecf419947366995cc9394882

7b3ac948c46c7981dd56a0e49c09250d3e2dfa53bf70cae9fe199a360deff9ee

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: dedb2e4ca1fbb13c60f876530ffb6a509064d82fd568a36cba94bf14c69649c6

#### Native item 1

Native pointer: /proofs/3/source_refs/0; canonical SHA-256: e5dda0cd5237cf61fe20c407dfbca09aedf6bf2436ab18d75eb19d9d2a637fae

SO_SRC_b44bad59cad582d9

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: f70c82647314742cb121dbc51fa23ad6fb649586ab412c5f46db4edbab30a0a7

Gradient-only transfer of restarted PAGE to a strongly convex average

### Native proof: F02_MS_UNIT_CONDITION_AND_GUARDS

Native pointer: /proofs/4; canonical SHA-256: ffa22db478fea562dddc760aeddf02067cc6ce986564e83f70c4cda1d666252d

#### Native field: algorithm_scope

Native pointer: /proofs/4/algorithm_scope; canonical SHA-256: 1d3f5e18e835e91b49162c8433489c626f373bd653cf5d81cb1c183d347a1a45

The endpoint witness is deterministic and hence admissible in the randomized view.

#### Native field: baseline_dependencies

Native pointer: /proofs/4/baseline_dependencies; canonical SHA-256: 7439d3d8d1d197c376065be9d658e3d7a479797ad40012411ab84f35541dd661

#### Native item 1

Native pointer: /proofs/4/baseline_dependencies/0; canonical SHA-256: 541a3ad36dd48b5221aff0b8aa810e2068a926234d93e871e78be8ddcdaa3442

#### Native field: pointer

Native pointer: /proofs/4/baseline_dependencies/0/pointer; canonical SHA-256: b5a3c8e5a69ebbfa3a635cdb498215b14ffa316a5c88100937281d883417d1bf

/proofs

#### Native field: sha256

Native pointer: /proofs/4/baseline_dependencies/0/sha256; canonical SHA-256: c07ac8a96c743d96e8281871bfb2f72cc2d3b3ad0e21b98a67c2c74469070bb2

09c14b74cc1de361ffe7c0244e9e4a71aaf24f0db6de442b56bb57e21eef9314

#### Native item 2

Native pointer: /proofs/4/baseline_dependencies/1; canonical SHA-256: 59c4fb19d637eb9b7984897c3abd07ed2bdf9c4ee30cb75d717f4d3818649ad3

#### Native field: pointer

Native pointer: /proofs/4/baseline_dependencies/1/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/4/baseline_dependencies/1/sha256; canonical SHA-256: 8e09baa828d09849901dc9ed86e8483c31186b871f3e199e500f8151de302b29

025da431bd57e492aeb3b539722067455bdf8389289a0a65894925e3eebf94a3

#### Native item 3

Native pointer: /proofs/4/baseline_dependencies/2; canonical SHA-256: 062c7df44e0a10c30ea34e167975b86eb18158d7698b33505230b6dc017c484e

#### Native field: pointer

Native pointer: /proofs/4/baseline_dependencies/2/pointer; canonical SHA-256: 75e7040ee9b7f6bb53623ed289617ff0705a4d81718776cbba42cdc3e6039b04

/bounds

#### Native field: sha256

Native pointer: /proofs/4/baseline_dependencies/2/sha256; canonical SHA-256: 5dae73e0dfab6ac0f52810e88ea41a0bfd77d79b2d8b7cfd3c2dd9d08b9533c1

7f23cf4be39eb5b5349089af4303a66a11501feb5e15a330bc1ac7c68cfa87ef

#### Native item 4

Native pointer: /proofs/4/baseline_dependencies/3; canonical SHA-256: 4ae307219fee96f992f45c2ae9e77a150c76b534682c1ad538e1a7d3a9f83681

#### Native field: pointer

Native pointer: /proofs/4/baseline_dependencies/3/pointer; canonical SHA-256: 710d9e6bcc130379a8bad365103ceedd68708a0b078f97fda36e184171d24280

/comparisons

#### Native field: sha256

Native pointer: /proofs/4/baseline_dependencies/3/sha256; canonical SHA-256: 8ec75603dc02d3a71727be5ceb8584c4f55839ed66126a74bdf0041f76595679

88539b93308c49415a6f6c911ec32cee0018ce9163ebef53dbc3b75a2a414291

#### Native item 5

Native pointer: /proofs/4/baseline_dependencies/4; canonical SHA-256: 5c03eb2add1c6409e3a38aef59716d6057bce89b665d44c91e804822721dcc9d

#### Native field: pointer

Native pointer: /proofs/4/baseline_dependencies/4/pointer; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: sha256

Native pointer: /proofs/4/baseline_dependencies/4/sha256; canonical SHA-256: ce0d20cfedd6ce950bae984e4dafa94fd01b7a4355b0f4668d961f978ad2ae80

0f3c3363c29242d8a6354a20350eb63567e0694c1b6f2880e841aad91707e2a7

#### Native field: body

Native pointer: /proofs/4/body; canonical SHA-256: a724ce12b1ba28123a65737c8789c0aa8d2308ae14b9333b608d7bce2466b047

Retain the frozen FO_FINITE_SUM_SIMULATION and FO_SMOOTH_LOCALIZATION premises, not their unrelated external theorems. Mean-square component smoothness implies ||grad F(x)-grad F(y)||<=beta||x-y|| by Jensen. At beta=mu, for v=x-y, strong monotonicity and Cauchy-Schwarz give mu||v||^2<=<grad F(x)-grad F(y),v><=||grad F(x)-grad F(y)|| ||v||<=mu||v||^2. Equality forces grad F(x)-grad F(y)=mu(x-y). Query all n components at the public initial point x0, form g=grad F(x0), and return x0-g/mu. Its gradient is zero, so its loss is exactly zero; total component cost is exactly n for every d and epsilon in the unchanged contract. This is an upper cost, not an assertion that expected-cost minimax complexity equals n. No R promise is used. Zero cost cannot meet epsilon<Delta uniformly: at x0=0 take all components equal to mu||x-s a e1||^2/2 with s in {+1,-1} and a=sqrt(2Delta/mu). These instances meet mean-square beta-smoothness for every beta>=mu and have initial gap Delta. The average loss of any zero-information output X over the two signs is Delta+mu E||X||^2/2>=Delta. Separately retain bound b5 at its exact frozen statement: its native view, g1, q1 and resource projection equal those of randomized comparison c1, and region r3 is a subset of r2 by its predicate. Hence b5 can be referenced in c1 only with guard r3. This does not extend b5 to any new parameters or certify its old source again. The same n-call algorithm satisfies the deterministic view pointwise on every path; record it separately as deterministic b3 with its own q1 and unit-condition region. No scientific quantity IDs are merged.

#### Native field: limitations

Native pointer: /proofs/4/limitations; canonical SHA-256: c04097454d13db7bde532d4fad50edbd91a5743439962bdb100dd1113989ac74

No main-rate lower bound is derived outside the original dense guard; no span-view transfer is adopted.

#### Native field: scope

Native pointer: /proofs/4/scope; canonical SHA-256: 90d507a520fb22feaaa486cfa971f80ab51d4d691988f9770cf7163c50d02dd7

Unit-condition upper witnesses in the unrestricted randomized and deterministic views; conditional reuse of dense lower premise only on its original guard.

#### Native field: source_refs

Native pointer: /proofs/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: 7759c2c40af4f6ba5f8099e646faabc1fc21122a957df446ef06d1f697b07e93

Unit-condition full-gradient endpoint and guarded inclusion of an existing lower bound

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: f98c3ba0195c8a660d3a4e4c4a5d0dd585913531775cd27ee88bec8b3ce8a78f

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 1d3fc94d80e1bd1a5072799ed647eea86b02e2f9de15cbd8fc374a4d85f28c8c

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 3373ebacf83f56c6e58873d84036e17f5a9d3edaa980a544092e62198fcc650b

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: feeb80c1a05d51390f76a13eb0b624a036b306a8fb243fe67a072d5a1e10ec88

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 8c4d4dcd8bf255cc0d385d96e0ff3521f342109d9b1da92c901f8e8bef43a702

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 3f38a0693a4a833a28b56ad746c41939249130cc15a1d34ca6ce2b615f3def57

Where it minimizes the guarded upper

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 8e73e1078a395593b9af485eb5b3d67102246479315dce4a0e2b12bdea5da790

SO_FO_F02_sc_ms__randomized__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 8d0c36cd6d4ac68d68ed507d53603b6569e4a30265f029dec4446b1251b3b7cc

Retained Katyusha X.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 9a82de25b278219fcd71585a3613e6c8363eb010645eaf272afd8d6c36c80b97

Full randomized target T

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 9c26a44ef59353c416cb5e7169d98b478485f563226819f24f3df79fd36d349a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 3f38a0693a4a833a28b56ad746c41939249130cc15a1d34ca6ce2b615f3def57

Where it minimizes the guarded upper

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 66b8130c6d61e0d96ed814c9a86d1b9d1af11d48d2b932fccb7ff58bf8b2bc27

SO_FO_F02_sc_ms__randomized__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 6815d5f5dd60f199e4b0d1e022519de5074bfb4d87a409820a8480a9533f9185

Retained compatible upper.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 9a82de25b278219fcd71585a3613e6c8363eb010645eaf272afd8d6c36c80b97

Full randomized target T

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: df596da5fef27f066c2b2325f327093b8591b888c384c3cb26d55805aab0c20f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 3f38a0693a4a833a28b56ad746c41939249130cc15a1d34ca6ce2b615f3def57

Where it minimizes the guarded upper

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 419b36cc2ac88cee094fbc6bf9bb280dc920720773754a3f4249e2bed2432a93

SO_FO_F02_sc_ms__randomized__expected_loss__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 6815d5f5dd60f199e4b0d1e022519de5074bfb4d87a409820a8480a9533f9185

Retained compatible upper.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 9a82de25b278219fcd71585a3613e6c8363eb010645eaf272afd8d6c36c80b97

Full randomized target T

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: b0d9ec0261f17f29b7b6cc223e08c118001e27e6f8adc93071bad7b752bb21a6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: ccc180f1792f4152895b02dba137f5b59a2acf9c2f5a1c5f2b9e7c4062cf0cf0

empty in c1; remains active in c2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: b790bb86d54a91734ce8623dbc23ac042e4155331da3955fcddd44b4cede7f64

SO_FO_F02_sc_ms__randomized__expected_loss__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 63e51e13799fede18787b5accee6c0d3674217865d2c7d4e63cfe33c3fea1a3b

New b6 has the identical upper rate and a containing validity domain; do not put b4 among c1 active upper references.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: e1f173ad4ab092a64e4cb5ce7d2fb4f0fb31ba679dec1791c96da1174f69adf5

D_dense

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: 4fe4ec2f533ad372fcb3e4f78d51a59ec67da384e7b90a90414465775a0969b9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: 182af37b7e902020a5746b06bc15fb029219556fafc5815578519500e35ecbd3

D_dense only

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: aede0918330648d722e4b851f2f55b2f4c613893e6d5fac3183f0da4cb1917b3

SO_FO_F02_sc_ms__randomized__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: c972700fbd458fda0fee1014c9d989bfebcb734b92cdc7e33e443d8ffb37fb20

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: d075bab0272472417b7b76027253659b233c1732af4edf2d1c9ec8e1aece3ece

F02_MS_UNIT_CONDITION_AND_GUARDS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: 575008a0f9ff458cc57d7f6e186b180e7ce3f448cbc213a669ec6f354f1687ec

Same frozen view, guarantee, quantity and resource as c1; integrate only under its original guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: e1f173ad4ab092a64e4cb5ce7d2fb4f0fb31ba679dec1791c96da1174f69adf5

D_dense

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/bound_uses/5; canonical SHA-256: c75053f10fe0357cf99ea6988d66e1610d98423fdfbfc68ab41bdd5f1565df4c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/adopted_region; canonical SHA-256: 388267f6a20369db5a7f75d3a8467276482ef043c846ac58ed63e0f1addca1e3

1<kappa<=sqrt(n); its kappa=1 branch is dominated by b7

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/bound_id; canonical SHA-256: c2a681b30dd6ef796ef66691bd86e413de337a79a747b1c1bae84e2440c8a429

SO_FO_F02_sc_ms__randomized__expected_loss__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs; canonical SHA-256: 5c651c341e8582e9b0b20cf6b790bfc9bda6d7bbfdcbadd262c4d4962ce578b3

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: 83cebb71f79cf1985a667ef0b86fc3fff7eae6b7bdda264a92f9b897626b8b9d

F02_MS_PAGE_GRADIENT_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/reason; canonical SHA-256: 34e0cddee8753395de6214e775e33dfdf2d9180e38a05e4726d794bc0e79b3b2

The source upper has no n>=1024, kappa>=3 or high-dimension requirement. Expected-cost convention matches.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/validity_region; canonical SHA-256: bbe42b731cb9a824ab884fe2970e0b3c8f1cb1f58ec8a638c1c9751d98cbb08c

1<=kappa<=sqrt(n), d,n>=1, in T

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/bound_uses/6; canonical SHA-256: 7485572c282a91cecc4e71f21eb47778b852c04747b9e51ab5b25270884c5ede

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/adopted_region; canonical SHA-256: a49a27ab5089ef7205d46b3cabfc0e2abe23ce876056b288833bf9a30e371170

kappa=1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/bound_id; canonical SHA-256: 03785648550f6477360e9443d1fa43e09eb3217abb550725c628f9b309fede1d

SO_FO_F02_sc_ms__randomized__expected_loss__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/mapping_proof_refs; canonical SHA-256: c972700fbd458fda0fee1014c9d989bfebcb734b92cdc7e33e443d8ffb37fb20

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: d075bab0272472417b7b76027253659b233c1732af4edf2d1c9ec8e1aece3ece

F02_MS_UNIT_CONDITION_AND_GUARDS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/reason; canonical SHA-256: afc7e9219a5abd5050fee8246496fad6859067eeeccd4f700e20a0c366fd2069

Exact zero loss with n calls; this is an upper witness, not an exact expected-cost minimax value.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/validity_region; canonical SHA-256: 4b6e5b456ecdf4d767a32a810e6c157297157f6828bf4b7935c41b41003fd90e

kappa=1 in T

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 80b26c88bbcd5eff8529aa1185bb298cac1f1bb19f68ff4cb8bc097cbd91977d

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 7afb1b7935caa54ac5157c3cfc1b5470b6d3f786315f36cae415a18566a789b5

kappa=sqrt(n): H=1 and PAGE=Theta(nL), so no order gain.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 2c0e0ed29bff2c8fd368fcbb0828c1e79c31c336c5fed469bb6f7a244a368da9

n=1 small branch has only kappa=1; the n-call endpoint applies.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: c5fa9daa69217838c9f164084d8269b0a92e227b10d3b53e28392f462784309a

On 1<=kappa<=sqrt(n), U0=Theta(nL) uniformly: Katyusha is at most O(nL), and each old upper expression is at least that rate.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: 859f393f587ae32f425d265978f9d3bb84db0a7eb8f529360af896e9d4a1659d

L~H is an asymptotic crossover: PAGE=O(n) for L<=H and O(nL/H) for L>=H.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/boundary_checks/4; canonical SHA-256: 7e26d3ac070a0dedc5e90e4b9d180931d8da223c7998bc3573e55cadbd53a856

epsilon>=Delta is outside the contract; opposite translations exclude zero cost for epsilon<Delta.

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/boundary_checks/5; canonical SHA-256: a35d49a0f84bb93a873135a3a428ccac6f7574155f7f27cc64100f9141957649

kappa=1 gives zero loss after n calls, without extending this precision-independent branch to kappa>1.

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/boundary_checks/6; canonical SHA-256: 4c378ce7e828ff3a2a2b1e6cc1211c4f573a95f7823ad0fb69d73c37ae6e06c4

d_dense is sufficient source applicability, not an intrinsic transition; no low-dimensional or large-PL lower transfer.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: c0b5ebf179781cc3796d0a54e71a3b5cda090badd9b308a9e9eaecff70f032e8

O(1) on D_dense from retained c2; no certified multiplicative gap outside D_dense. At kappa=1 the new upper cost is n, not zero.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: f6b81012b005bc785b63976d3b7d2bf5b3259c3c68811120d6ad788be88cd25d

c P on D_dense only; no adopted quantitative lower bound on its complement.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: d3b4e3686f1c8b0898f753653c765d845403331dc73362c079f84067646768ec

Quantitative lower missing outside D_dense; sharper near-unit and hidden-component rates are deferred.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: d4a3f0c4faeb71fbe80044484b380571ee957e03c3d4c03d9ac2e84f7ca54d2c

min{C(n+n^(3/4)sqrt(kappa))log(C/tau), C n sqrt(kappa)log(C/tau), C n d log(2+kappa/tau), [C P if 1<=kappa<=sqrt(n)], [n if kappa=1]}.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 23e8cada3591c3646d6bce2961e532fdf7aa3e334bf3d467879e526910db4aa8

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: bcf57ed16107f45bfff88922238d3e39e01a9e96be5c94499e3f11cee7cc2347

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 2e207b7ff4ba12788cae49e6918e90ab065c3516d945f70677f7bde39e374fdd

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 8e73e1078a395593b9af485eb5b3d67102246479315dce4a0e2b12bdea5da790

SO_FO_F02_sc_ms__randomized__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 55606982039cdc541618a64d2f5e15f3caef1b0eab305005e33130a1bbd3d05e

On D_dense, retained b5 lower and b4 upper already match P.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 9a82de25b278219fcd71585a3613e6c8363eb010645eaf272afd8d6c36c80b97

Full randomized target T

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: e84ef098a17d56f8da9ccb5fd5fcb64f7bcb21947e862041a3c5930985ed959e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 66b8130c6d61e0d96ed814c9a86d1b9d1af11d48d2b932fccb7ff58bf8b2bc27

SO_FO_F02_sc_ms__randomized__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 55606982039cdc541618a64d2f5e15f3caef1b0eab305005e33130a1bbd3d05e

On D_dense, retained b5 lower and b4 upper already match P.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 9a82de25b278219fcd71585a3613e6c8363eb010645eaf272afd8d6c36c80b97

Full randomized target T

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 77970a7b4943c3c8b42c3486e61f59e7f073985c9a3ae059f11c754cd7da4c54

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 419b36cc2ac88cee094fbc6bf9bb280dc920720773754a3f4249e2bed2432a93

SO_FO_F02_sc_ms__randomized__expected_loss__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 55606982039cdc541618a64d2f5e15f3caef1b0eab305005e33130a1bbd3d05e

On D_dense, retained b5 lower and b4 upper already match P.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 9a82de25b278219fcd71585a3613e6c8363eb010645eaf272afd8d6c36c80b97

Full randomized target T

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: 92aac02fbcddb4a43e68232b7d5ce323886a6e5bea1b3143d23070be55ea5423

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: e1f173ad4ab092a64e4cb5ce7d2fb4f0fb31ba679dec1791c96da1174f69adf5

D_dense

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: b790bb86d54a91734ce8623dbc23ac042e4155331da3955fcddd44b4cede7f64

SO_FO_F02_sc_ms__randomized__expected_loss__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 9c992d9a6f95050aafefd68ff1e9d83349b44e6968f2ac51f1ed287352105382

Retain the native active upper bound and its guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: e1f173ad4ab092a64e4cb5ce7d2fb4f0fb31ba679dec1791c96da1174f69adf5

D_dense

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: f74794614aa722df0d720bbbc8abd5905ee67b3f7c7614b8525f971a82f6c0ab

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: e1f173ad4ab092a64e4cb5ce7d2fb4f0fb31ba679dec1791c96da1174f69adf5

D_dense

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: aede0918330648d722e4b851f2f55b2f4c613893e6d5fac3183f0da4cb1917b3

SO_FO_F02_sc_ms__randomized__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 80a042bfbbce657e111d367097ea1a43818622a30e30c98d7bccfe69af9e8d12

Retain the native lower premise conditionally; no recertification of the old lower construction.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: e1f173ad4ab092a64e4cb5ce7d2fb4f0fb31ba679dec1791c96da1174f69adf5

D_dense

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/bound_uses/5; canonical SHA-256: a12240194ca900435020afb9beee27ba89c55569b6336c814ba917cd260b2958

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/adopted_region; canonical SHA-256: 7d13c076156a7ca921736f76ee5ef878a2e37c487e7de8785cb550974c1d91d4

empty in c2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/bound_id; canonical SHA-256: c2a681b30dd6ef796ef66691bd86e413de337a79a747b1c1bae84e2440c8a429

SO_FO_F02_sc_ms__randomized__expected_loss__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs; canonical SHA-256: 5c651c341e8582e9b0b20cf6b790bfc9bda6d7bbfdcbadd262c4d4962ce578b3

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: 83cebb71f79cf1985a667ef0b86fc3fff7eae6b7bdda264a92f9b897626b8b9d

F02_MS_PAGE_GRADIENT_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/reason; canonical SHA-256: 56bceff398d2065ae5909380e4643eaa49e0aff2d5e7453d18692bab8bfa6de0

Equal O(P) rate to b4 on D_dense; broader applicability is used in c1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/validity_region; canonical SHA-256: ba1b392e8b2aaf547170a4b6ed4f16a3e4b82c16c267d9b2dbffb4873f81b6bd

1<=kappa<=sqrt(n)

#### Native item 7

Native pointer: /joint_analysis/comparisons/1/bound_uses/6; canonical SHA-256: d24259a8d7f88869cb32e7a2cbdbc052ff11ed52b85d2f7d537e73916efbe4cc

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/bound_id; canonical SHA-256: 03785648550f6477360e9443d1fa43e09eb3217abb550725c628f9b309fede1d

SO_FO_F02_sc_ms__randomized__expected_loss__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/reason; canonical SHA-256: 1256e647b4f3f00bc652477cd325d870cbec1555e6780a65a9980546bc70e494

D_dense requires kappa>=3.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/validity_region; canonical SHA-256: a49a27ab5089ef7205d46b3cabfc0e2abe23ce876056b288833bf9a30e371170

kappa=1

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 6255cd01008ec0a7ae7fdaa11d150977a772444bccdc9c49e66844dc65f3005a

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 5c469fe130a1f3ed7aaf72fc24e596cc8e55a7fbc1bba8cd7a82d6b68be651c7

Retain n>=1024, 3<=kappa<=sqrt(n), d>=d_dense and native accuracy guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 33299ff76cba7bc9c14d5cd699768f0278106cbf04bb8c884b1c86791e51a7c4

At kappa=sqrt(n), H=1.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: b072d16ea9a05f8fee8abfa622a3d323101d62d672c462d4aeb248fc3000bac0

These lower/source guards do not restrict the new PAGE upper.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 606a62dbfb43693613b22c59bb614ff2f59fc0800e67d96bb996cbbd3e4fac93

SO_FO_F02_sc_ms__randomized__expected_loss__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: b2e470b32021ca03236f93a688f040980d20b3541cf789ef9eb9408466a16920

O(1), conditionally retained from the accepted baseline.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 739d3742b40eaa45c58e3ab1996c31a83656c3fd152b452e78bb9e42ca1b2fce

c P on D_dense, retaining b5.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 4d893673023f3c1d9eef11fb78d0ab821da6f35867e2890b2f807200f03fe39e

Conditional matching bracket only on D_dense; no fresh source recertification.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 94e13cd105cb983086cf9e860e04b33dcf51a22d53f62d72d2c0aa4e0532dc71

C P on D_dense, retaining b4.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: f4354c7486061e43e88112eeb49890fba77e921a34cbf24cfacb02ae290c8d7e

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 47e67b73c361c34d3858671f7b011fa075195441cf6c5d315b95c268779f71cb

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 761712c391c4de54eb6101ca71bea01e091a9e91cbdc6b20b4a54a1e9f420228

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: b51bed53fac6542c523852678ea221c8e437a82481f507c2c2b65ae97d6fdeb1

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: edcbb214c5c554676e6844b97cc5f0a045df43d3a125266db0b3a3bef9a9ec05

Retain the compatible span upper and its original guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 11d5f2a2e8a48f927bda56ba5765c2982a0543bb52fd875c4b440dffd1f0744d

Full native span target

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 7a0575043c3450ff667293970de2263099b021c9ee2dbecbc19650d47ed02b9c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 09ecd540fee2c569ac3f92d9c03a17f9a62f98ee6cf48a0e4e06014d11ddedcb

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: bb6391f904d0b55f86ee578491df9e7355b3b42c7573d7e20333c1be0d6d434e

Retain span, high-accuracy and sufficient-dimension restrictions; do not promote to arbitrary algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: c974befbe2f51240cea99378fb171c69b1e3c0ee65b006f9806e6bcbacd4a6f5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: 0f38de94af0b693399d4dcf0839eaedee78886f989e4810277d8093222126274

None on existing Z; source D_dense is disjoint. The typed pending route targets the separate span_complement cell.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: aede0918330648d722e4b851f2f55b2f4c613893e6d5fac3183f0da4cb1917b3

SO_FO_F02_sc_ms__randomized__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 8f793a8ed32ff153519e600a458ea065b03019e052a8f1edf9ee4cbaef8cd64e

Span randomized expected-loss/expected-cost algorithms are a restricted subclass of the same unrestricted randomized contract, giving a concrete lower-transfer route on source D_dense after exact contract verification. Existing span c1 uses Z with kappa>=4sqrt(n), whereas D_dense has kappa<=sqrt(n), so they are disjoint for n>=1024. The existing c1 is listed only as the native target quantity/algorithm-contract anchor: no change to its optimal Z envelope is asserted. The actual opportunity lies in domaincell span_complement, with no native comparison there yet. A complete native mapping and new quantity-matched bound/comparison are required before publication. It may add a lower in that unassessed complement; it is not a proof of a matching whole-complement rate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 71449cb0d51f754f8de2e252aaa85fbf8ca2574a23b423ccc8a68ef3275c7176

Referenced regions: ($n\ge1024,\quad3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad0<\varepsilon\le c\Delta$) AND ($$n\ge1024,\quad3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad0<\varepsilon\le c\Delta$$)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 1d97d32c825b24d22e1f3de92018588220f8f5a998d01ef41d5240f3d2dc5409

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: 3897982213d8fca3ae40d80e4f52582081b80f5b40a841a6f81358a2a2c54e69

Retain tau<=c min(1,n^(7/2)/kappa^3) and d>=d_ZG.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: 3b17f4bb2982af61f1813b47dc7a36f9459726a275c9b3d80fde456f11e58675

Z and the PAGE small branch are disjoint since Z requires kappa>=4sqrt(n).

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 399f59f0cccdbcff28414ab8f751ae13f20033b8f39fcfb5dbdaa0680acac2b8

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: 87aca3ee5aeba9760327eac01d99eb80c6fee5c6cc5b5b1da5d68f75ab6a6f1e

O(1) on Z, conditionally retained.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: f2ce50f351a12ac627c14fc7640afabfa5b539231934feb3ffd4a973ce238e9a

c(n+n^(3/4)sqrt(kappa))log(1/tau) on Z.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: dff05767a1631025e246e3f97eb9a960dc503d7e51c9fdbbdf3340912f609360

Span target outside Z remains unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: b3f6b0ecf6cb3d3ca1a39a9d113f0aa508ab66b44c7c846b3f166b06505705d9

C(n+n^(3/4)sqrt(kappa))log(C/tau) on Z.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 3666ab534207ad335de17470f4bce6c6f193b1bbcb9e9a79f98ff8e7cf84922f

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 247711d1725cd15aec1dfc6398fa9c0a3c1c56e96060ce9211ac3deeeebb5dff

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: d2efaa2c2f4e640d2a9e98392a5e35ac1f91339e49b0ebdd0b23fbf6e217a245

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 85e885c6bd9f6662373c5df9c19d6375f3a6c5bbe0d28a903f3e3e730f37cf31

Where acceleration minimizes the upper envelope outside the unit endpoint

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 323860be03d6df2ae08d2a78ed9cbd58067a2df456d3511550e33682bf574cf8

SO_FO_F02_sc_ms__deterministic__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: ac841221f827928efb9b36533ef71cb5880544510fa2d98566a2156e013eaddd

Conditionally retain its pointwise guarantee and pathwise cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 2ef4c4d6ea8ebcc6afcb72e9405d6579a4940e322041f3cb7fe06b5f387606af

Full deterministic target T

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: a7dac5cb0fc83049bbf51ef3459f40f8aa8b505241ea3af648b369f3d9c62645

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: bc28de75b247a7f718e78896c4b2426bc095e984e76c0695baf7f3ddf478bc18

Where cutting planes minimize the upper envelope outside the unit endpoint

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 549ead76064af804003339d8839121d593d87c1c4b14291c31287afbb0f95ce4

SO_FO_F02_sc_ms__deterministic__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: dd8012e5be11b3b15106a56a56f05558480bdf7016d768383512228172273af6

Retain the dimension-dependent gradient-only witness.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 2ef4c4d6ea8ebcc6afcb72e9405d6579a4940e322041f3cb7fe06b5f387606af

Full deterministic target T

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 0a3eb3f759d947c5c7b3fb542e6a99513ff0d916d29d91df835edd92fc3fdd9a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: a49a27ab5089ef7205d46b3cabfc0e2abe23ce876056b288833bf9a30e371170

kappa=1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: 085b5237ee06324a35745a9192dd9a7f9984d77a59806b8216f614d865126916

SO_FO_F02_sc_ms__deterministic__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: c972700fbd458fda0fee1014c9d989bfebcb734b92cdc7e33e443d8ffb37fb20

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: d075bab0272472417b7b76027253659b233c1732af4edf2d1c9ec8e1aece3ece

F02_MS_UNIT_CONDITION_AND_GUARDS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 12196deb4866498ff1892fe27c4033b507b0d86594df9fc0049b2343129e295d

Same exact algorithm as the randomized endpoint, recorded with a distinct native view and quantity ID.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: d784bbc478cffb10bdcd98e0045c6ea0e68d2a82236e3c4093dff49a7f7e3f9e

kappa=1 within the deterministic target

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: 027e98aa084dd0974695198640b7a0a0f991e1a85c6e98cc631dec0481a904bd

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: 736b6cf8f1ad5ba550c260439bdf7db4f4975fa327b23c5e46d0b3870135b720

None: distinct native quantity/view and a pending guarded transfer.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: aede0918330648d722e4b851f2f55b2f4c613893e6d5fac3183f0da4cb1917b3

SO_FO_F02_sc_ms__randomized__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: e3db67692bcffe55218a65c50e3686a0f7a7940960adfc734ffd88bf8b695e9a

unresolved

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: 0f800d9d56822ce5710f83f87cbe81003530fdab872d2dcd627e9f51f9a01c27

Source SO_FO_F02_sc_ms__randomized__expected_loss__b5 has D_dense: n>=1024,3<=kappa<=sqrt(n),d>=d_dense,0<epsilon<=cDelta. A deterministic all-instance pointwise-loss algorithm with pathwise capB is an unrestricted randomized algorithm with expectedgap<=epsilon and expectedcost<=B. This identifies a directional subclass/stronger-guarantee route, not a permission to copy a distinct quantity ID. Verify complete source/target oracle/instance/initialization and cost conventions, write a full native transfer proof and quantity-matched bound before any adoption. Potential effect: fill/improve the deterministic missing lower on D_dense only; not at kappa1, lowerdimension or outside this guard. No transferred bound is adopted in this metadata correction.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 71449cb0d51f754f8de2e252aaa85fbf8ca2574a23b423ccc8a68ef3275c7176

Referenced regions: ($n\ge1024,\quad3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad0<\varepsilon\le c\Delta$) AND ($$n\ge1024,\quad3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad0<\varepsilon\le c\Delta$$)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: 09367a5b29c4b089253c5c5513448d68e983d7ef746576d0d75bb4be75cef0db

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: 7fae59c819ff7a71a1aa2e0a3c3b21be187fa5b25957a28ab4b53fbda990f97f

At kappa=1 cost is exactly n on every path and loss is zero.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: 051a52e5a80a4dfb05cca0b09a2aea3995e33a03d01135f7b9e4e11e0a2482e3

No expected-work PAGE-to-deterministic conversion.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/boundary_checks/2; canonical SHA-256: a23ef87ab549a23f2158b0b19e29203a45207050ea6c36820df94ba5bea41f46

epsilon>=Delta is outside T.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 8d34cf95c1d6b4ec28d04455189f042929ae3ce0ae95d3f201cdd0d70fbdd35f

Unquantified; native missing_lower status retained.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 686d1fff0316f9e0ea0491db11261d835fe73d54030b4c8a47b92bcad725e905

No quantitative lower side adopted.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 3c212c92f1bfc1d7ccb9787322ee94218c25e5629686350ed17ed7465f72e9c7

Quantitative lower and sharper kappa>1 rates are deferred.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: e3b708aba3fb36b70d35aa575a31e9354e2a3216f1d7380584bc2168e2a1c67b

min{C n sqrt(kappa)log(C/tau), C n d log(2+kappa/tau), [n when kappa=1]}.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: a88d986db9fa1ac08fcffc23314cb2c44744a8aa6c7772f9f510fb3f4aebed43

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 7a71489b714c3def5979806412afcc42e1fd9686978ef166c47c3e8f90fee3db

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 09386d7b622efa63951ff0debc46401337d28610e03a446df35a3257dc799718

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 3702da2c6d1cf553a59600c30f566abe7a0f7b89bf8776334d29277e295f54d1

randomized_unit

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: b71bcc1526e5c27cbf8d7b5011bc89019ff1db00baaf8c7aff43edeeeb501b87

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 4c85d25893da720c219f335689d1f834de7d01719f58b79b6d76946b99096cf1

n-call exact upper; quantitative lower missing.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 194ce06398bc941dfb581833a3b832970fddf7e7f1b24fa5fe7705269e183783

Randomized unrestricted target, kappa=1

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: d8e25242861c9cc11bf5545f8ee0affe1c8509825cd23aa667035c9e6d586ce2

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 715a489ad519f6d51b7cd756091d2ed5fdcc53811bfdd1e2944cbee84595755b

randomized_dense

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 5e407ec088c0e2cb665cfa5e003948e2e2b0af625d59ac8c625b982821f09648

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: 606a62dbfb43693613b22c59bb614ff2f59fc0800e67d96bb996cbbd3e4fac93

SO_FO_F02_sc_ms__randomized__expected_loss__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: edfaad61c85c2f408d12e6bc7780558eb13b02588ed931f4f936726bacf97bf3

Retained Theta(P); sufficient-dimension guard remains binding.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 171856d45eb569bf6dc7ec1a121ef3081844e97302dd0d4e6e116bafda900c32

Randomized unrestricted target intersect D_dense

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: eac1a3c54d9e24ecec08c4186878157f914bf1746dd808ba538ebf8629b2a0cd

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: bde03b5284aa8b549c80c7f095a72e67050c152eb1ffed822a91a8d889f04ea5

randomized_small_remaining

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: b71bcc1526e5c27cbf8d7b5011bc89019ff1db00baaf8c7aff43edeeeb501b87

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 393a3ec409e7cc29cf3930ca982a15929f2c0331105ec9f62e0bebb426a1afdc

New PAGE upper, quantitative lower missing; not a literature-absence claim.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: c0bdd4108253b425ddb1a72008bcaa9e3588ee5d2dcd15e02fc17f31cbb93919

Randomized unrestricted target, 1<kappa<=sqrt(n), outside D_dense

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: 692a4f1febc8f559adfb9973f72298807668472ce75158bec7d24dd9bab52d77

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: cc44dfec8c92cb021fd9acd119dd217e1bc380275be2121f88dece7cfef1cce1

randomized_large

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: b71bcc1526e5c27cbf8d7b5011bc89019ff1db00baaf8c7aff43edeeeb501b87

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: f4af3e50eb44d4cc9a2bc6ed16346418b8cd241fd8f58d7ce465b3860bc534e3

Retained U0; PL hard instances are not transferred.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: abbef8ec5d369f9fad65abd7d0ddcf4619b97d952148039830bc070c9f18eaae

Randomized unrestricted target, kappa>sqrt(n)

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 5

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: fb850c3e02fce4e410bab5770dd644976d7af707dcf9f348399c8e45408ace06

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: e0c9441b6c0ab9595b31ca9238449af9cd8f7a9dc642b38741a99de7142067eb

span_Z

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: 851b52e8fe3e3494c2ab4132ebb676cfa78efa4cc26e16470dc0b451f84f01d6

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/0; canonical SHA-256: 399f59f0cccdbcff28414ab8f751ae13f20033b8f39fcfb5dbdaa0680acac2b8

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: 55334f2fa081c325fdd9bce8974f8665c9899a110cae9a24042158317a1811ec

Retained matching span bracket with accuracy/dimension guards. Existing optimal comparison states are conditionally retained; this metadata migration issues no new native-proof closure certificate for historical source-only records.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: cb502c42ba7bad757d505b4dfcbcd0608c0101e37a2c4fb7482ace7db4a98dbd

Span randomized target intersect Z

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 6

Native pointer: /joint_analysis/domain_map/cells/5; canonical SHA-256: 30c139880967d28be1a8d8019c2e55cdb17f8b76e754e7bb997001216e5f16a5

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/5/cell_id; canonical SHA-256: 8d3c8d93e94f0039ff326ae17fd4c4c85dbccd79f2b448b482a519c0ad958e3e

span_complement

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/5/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/5/note; canonical SHA-256: a1c9f1ff56e9f4cf3c49f092d42bd5f94b1851a0dbb33f9c20f423c3a0d98949

Stored upper exists; complete joint comparison outside Z is unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/5/predicate; canonical SHA-256: 08a0a78cde6dc7e5be58efcd1cc4632d7d0c3ae0b739e723cd2beaf02de125de

Span randomized target outside Z

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/5/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/5/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/5/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native item 7

Native pointer: /joint_analysis/domain_map/cells/6; canonical SHA-256: d75867c1caa71c94decb28acc4c46f057fc72c773758b6d2d9429174e5c1c5c3

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/6/cell_id; canonical SHA-256: bd9a25a86c8eb77a8d7ee66dae5e2ef6c8d13f9765c6e0768bd57dba62a3f1ab

deterministic_unit

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/6/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/6/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids; canonical SHA-256: e3dbc77abea392b3687684e4f6c6fa2b68d8d5a273552a091160d1911c82fb1c

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids/0; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/6/note; canonical SHA-256: b5bb3d6d040dd7c5b92b589bf38512e94ca8faf3300fc2bbbf60c7f176679b96

Separate deterministic n-call exact upper.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/6/predicate; canonical SHA-256: 8c69a5ec89a646a76b8e272632eb1da74688a74a0805ac0ab09151e40a44caca

Deterministic target, kappa=1

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/6/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/6/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/6/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 8

Native pointer: /joint_analysis/domain_map/cells/7; canonical SHA-256: 4c399827eef63f38a800414c512cf380126c30bd1e5c8aab6b8aeab7c7d749b1

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/7/cell_id; canonical SHA-256: c929ec151d3d22026a833b2c674731372012cbd16fe1c493210d42546b1fe9ae

deterministic_other

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/7/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/7/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids; canonical SHA-256: e3dbc77abea392b3687684e4f6c6fa2b68d8d5a273552a091160d1911c82fb1c

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids/0; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/7/note; canonical SHA-256: 42d294c00f3e3b76a627c7b2dbfa0f313fc9ef2af66fda7ef38f25b1e67f274f

Retained upper envelope; quantitative lower missing.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/7/predicate; canonical SHA-256: d0666833ccc51527f01d0933e120b41617e954e9b5c5453999be9073182b51fc

Deterministic target, kappa>1

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/7/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/7/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/7/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 3e9a7ac86f171f10c5ef6c52bb9e8be3edd9cafb3f2c1566506c5aa755f74f50

Partition the disjoint union of view domains: randomized into kappa=1, D_dense, (1<kappa<=sqrt(n)) minus D_dense, and kappa>sqrt(n); span into Z and its complement; deterministic into kappa=1 and kappa>1. D_dense implies kappa>=3. These disjoint cases cover the native target.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: c80f22f9b5c38629bbcf23b20f91881df0397e1f04f9784431241b1dac109be0

None unlisted; the span complement is explicitly unassessed, not proved open.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 2401f7caa86213a146c76bd001a338c514a8a917ff2885b46f103f64698e799d

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 2d4dab513c22d5e5dc89fed7cd8a770158ea4bb9ae21655de2258c223c7172b2

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: b9e56f704b48f3b1a7ad79d770a97f8d1f22377a0fcc289b9fddf5d774266a6d

U0=Theta(nL), PAGE=n(1+L/H); L~H is an asymptotic crossover. Source validity, adopted region and actual gain differ.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: b71bcc1526e5c27cbf8d7b5011bc89019ff1db00baaf8c7aff43edeeeb501b87

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: d73f9eb2bc309ec674c82d09e7f86c5677c362bd969b23d9307eb043bb7eb970

page_upper_extension

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 7aefbc132a91d898940aa155fb1b8a12e891db8ca7965ff84b342df845808c30

Outside D_dense, 1<kappa<sqrt(n), along families with L,H both divergent; gain Theta(L/(1+L/H))=Theta(min(L,H)).

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: f6980229df03421e3cf23418c2763d224fc813df3ebe64dca1c1ab4dd934a27c

min(U0,C P) on kappa<=sqrt(n), intersected with n at kappa=1.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 0e9678efea30fcb9b7f075805f8e64658ba79afd9b653a60266c8015f432ee41

U0=min{C(n+n^(3/4)sqrt(kappa))log(C/tau),Cn sqrt(kappa)log(C/tau),Cnd log(2+kappa/tau)}; old full profile also has O(P) on D_dense.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: c3312a991a8222c1c8fc16e89bd3becbb9d5248c586ee479c81bcc5df7e4e264

D_dense already had P; no order gain when min(L,H) stays bounded or kappa=sqrt(n); kappa>sqrt(n) retains U0; kappa=1 has its separate endpoint.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: a37bcec985508b3b11bd78141ad82bc1bd378a241876718efdb81818f5f12248

T intersect 1<=kappa<=sqrt(n), every d,n>=1.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 23645ca49af4e39d308a415dfe7b01b8eb2a2e7639cc53104fca7dcf8628c34c

d=1,kappa=2,mu=1,beta=2,Delta=1,tau=1/n: old Theta(n log n), new O(n), outside D_dense.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 039f71ded0d66542a0d38139af500535abd5b130d75e2e5565dc67e9399d750c

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: a9c8786510934914d4cdc9b93ad6f05ec3853172734885ff197640388bbc23e6

Equality of strong monotonicity and Lipschitz bounds yields an affine gradient. Exact upper cost, not exact expected-cost minimax complexity.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 3560be38006ca0ee0f8864465a8fbb51345044adf6dac3b0e8d53cc685e5fff2

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: f3ab2a4581dfc2be9e4ba69a4c8dcd0ffa000d7f878bcc1e2432419476d394d9

unit_condition_endpoint

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 5de519fecefc2e0e6c9fa54392dae676571484832b31dd80a89331d95884cc3b

As tau->0, removes the accuracy logarithm. Also improves PAGE when L/(1+log(sqrt(n))) grows.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 53286f764966c17bd09beb25a678ecb8ff9bbf0162bbc325e1bd07b8f93f9a1f

Zero loss with exactly n algorithm calls.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 03293ce3e9f18275ac0ddf185f04d434d972eb158ddcddc6a77a862c1edfa4a9

Theta(n log(1/tau)) at kappa=1 in both unrestricted views.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 559e2e2cbfdaa20213992c00716d73ed819556aecf76fc5aff5cb5fa37a7f3c9

kappa>1; fixed tau gives at most constant-factor change.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 86d676996981b09d88f27341f22cde9b6cec7d1c187edd95b93031c582f03ae3

T intersect kappa=1, all d,n.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 613a064f42dde4b9afd1dbfed2d6442a0c1fd016aac2d3a45d51003be8a3dc75

n=d=beta=mu=Delta=1, epsilon->0: one gradient instead of the old logarithmic upper.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 9628153ee7229430af459c0f95a74a321d2c1f637633110e1d55be7f8e961b07

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 10f13527ba013a022b5a69ca7ca83959d820ac85e2218919fec6ce27fc68b94a

Complete retained-premise subset derivation; only adoption bookkeeping and partial-coverage display change. Status remains missing_lower.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 5e407ec088c0e2cb665cfa5e003948e2e2b0af625d59ac8c625b982821f09648

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: 606a62dbfb43693613b22c59bb614ff2f59fc0800e67d96bb996cbbd3e4fac93

SO_FO_F02_sc_ms__randomized__expected_loss__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 38fadc95e31c1b924b49d7c37d6ca839309642bf6143741a258d65b036a44a64

guarded_dense_lower_integration

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 101635f5f5dc4bedb408aa15c2632d2216c4c95e86f98916acc1d586a8536d04

Empty for the full-profile scientific envelope.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 8137959c0505fa73977aedc49469cfbbd8e4c5d899b4d60959041f88f405d78f

Same c P also active in c1 with the same D_dense guard.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 328ecdf8d72cd481408959372d8f14b42ff6ec42f7a49f9d50756cb00aea6034

c P active only in c2.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 74a4a40916181bbc444eb080870519e842770aa3ea8016c0e104cf0a9e9041f6

Entire target globally; lower still missing outside D_dense.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 40e60ae3ff7bd4b84f924741a24b06d72ac15a0bbfecad2ca778e575efe03128

D_dense only.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: c7402860d4e4cbb241a7595582ee5b1669e5e8aa287a4b14c0524680c8ad1d0e

c1 and c2 share view/g1/q1/resource, and r3 implies r2.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 2a1beedca625dac20a104ba6708037224ef12f5db4ae1f2314fb2bb17f7fecde

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: b5b99832dff3b53056491bed2d3148a2a2eba939e12374bce4378814ed7d3bb9

Presentation alone supports no inequality edit; the other scientific findings cover every change.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 79e8ecadc0249b0931d625bbe430b934f64189fb1894d810552aaafcfb12eac4

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 606a62dbfb43693613b22c59bb614ff2f59fc0800e67d96bb996cbbd3e4fac93

SO_FO_F02_sc_ms__randomized__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: 399f59f0cccdbcff28414ab8f751ae13f20033b8f39fcfb5dbdaa0680acac2b8

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__c1

#### Native item 4

Native pointer: /joint_analysis/impact/3/comparison_ids/3; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: fcdd6190343c888ccea6f4d6f5a5f625d1457b21baf2334f1792d2ec063b793b

first_joint_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 6be07067b236d59a6d4e70e3b54884189414595fe3090ba0b689b09aa830de35

None beyond separately supported deltas.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: a94c1064657d0494bf231480894ab389518823bcef511ccbe3b4d2536fbe90ed

View-separated domain accounting and guarded synthesis.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: 7ddc4ee8f94ec552e72beb3c16f301efcc859a2e301e30cec99f22ce4709f56f

Frozen comparisons without joint analysis.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 02a8354de5ab56fba7b34eb18fcb5aad8b18f51530fbf38109bef08c1dfc3c20

All retained inequalities and statuses; c2 and span c1 science unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: ed0e7dbfd7b6e5625296d821d53da2f5719f38b344cb37c58f95045a7e1a99d8

All four registered comparisons under conditional baseline retention.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: af7a3f0dd31299eb9877d7b689778e89ba3900fd0e58b0b79d9f76731bf8ea51

All nine old bounds and four comparisons completely read and dispositioned.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: 3abf96d23d34013576227ede021e4a81ac5baf4c26e4dee4a1bd4e0b32d31f12

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 93b205677f0cd8fa6c8505ec811ba82067e21924a3304cd09a95323d86f46308

A lower bound for a larger class does not imply one for this subclass. Large-kappa PAGE upper is dominated by Katyusha.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: b71bcc1526e5c27cbf8d7b5011bc89019ff1db00baaf8c7aff43edeeeb501b87

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: aff39f3efe22ee209f3938e3cb68faa4a4d003c1ef2773cc4075694fedd75b29

large_PL_route_not_transferred

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 3bc472ac9d1996a3c56f6b71040d755923fdb418e20481428989143fa40e0f6d

Empty.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 66917362f433c05b839593b0aab1a53c300932655736cc7f3985d91aa17dbcf1

Unchanged U0.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: d891c03b6784eecb7843671e5445f6ff0663689f7c4e5f464f1e13314e9ce9dc

U0 at kappa>sqrt(n).

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 354e186d2836fa13067ee855c46ab5f7f6f17d2345d3cc63e6ef3cf077dc19bc

Entire target.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: 502645f73170e1c965ea8faf7ca4a85d3c1a03513042c562a3a9c30d206da274

Larger source PL class; strong-convexity inclusion unestablished.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 0b767929a9766378ec41616a52cf240dad6ae6fd3a114ee131db7a2555947ffc

Theorem 3.3 singles out strong convexity only for its small-kappa hard instances.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: c3748816d3295231a58bdc1314cd4a91687f6b72b0917a8d2fc3bec3bc9407b6

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: 56d9e66e2b9e81d38efa09f7945f6b7dcc51e209c7f0ffd714ef558bc9d54771

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration. This revision addresses the preserved actual independent-review issues. Publication and typed projection obligations are explicit; every mathematical formula and adoption guard is verified against the exact native candidate, and historical effects are not reported as new frontier gains.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: 79e8ecadc0249b0931d625bbe430b934f64189fb1894d810552aaafcfb12eac4

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/impact/5/comparison_ids/1; canonical SHA-256: 606a62dbfb43693613b22c59bb614ff2f59fc0800e67d96bb996cbbd3e4fac93

SO_FO_F02_sc_ms__randomized__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/impact/5/comparison_ids/2; canonical SHA-256: 399f59f0cccdbcff28414ab8f751ae13f20033b8f39fcfb5dbdaa0680acac2b8

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__c1

#### Native item 4

Native pointer: /joint_analysis/impact/5/comparison_ids/3; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: f8e7fd7383e718ca5435183cb076f9142bfe16f1c50613431ec9cf08e9db1616

curated_feedback_SO_FO_F02_sc_ms_20261116_2a144b4edf

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/5/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/5/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

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

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: c33b3e5c793b71361e1394e59f19f333e063a581816f5ca3771acf288836791e

Separate native minimax component-call quantities for unrestricted randomized/expected gap and cost, span randomized/expected gap and cost, and deterministic/pointwise gap and pathwise cost. In every view: d,n positive integers, beta,mu,Delta>0, mu<=beta, kappa=beta/mu, 0<epsilon<=c Delta. R is an inert inherited coordinate, with no added distance promise; constants are independent of it. Write tau=epsilon/Delta, L=log(1/tau), H=1+log(sqrt(n)/kappa), P=n+nL/H on kappa<=sqrt(n). D_dense is native randomized r3: n>=1024, 3<=kappa<=sqrt(n), d>=d_dense. Z is native span r3: kappa>=4sqrt(n), tau<=c min(1,n^(7/2)/kappa^3), d>=d_ZG. Dimension thresholds are sufficient source conditions, not intrinsic transitions.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 3c8f7194f268771e7dc9298ee35c31e20920d88711275be080deb5e8f5c38c92

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: cce3fe6fe250c4cbd72965ec22d3ad149c0175f60421896746bb2ddf9db62d15

Finish discovery: two arXiv HTTP-429 failures and noisy Crossref search 6cf8c8212bb0cd952623f110c8ca868fca55d014de59cb5f7207340173d4927a with unprocessed cursor MTcxMDQxMDk5ODAwMCwxMC4xMDM3JTJGbWV0MDAwMDY0OQ==. All five returned records were exposed; no terminal replacement or complete-search claim.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 630e6bcfcde7fbfea8192378e18070fb346a2c2e8c3fee11aba313674e83664d

Sharper near-unit-condition rates, quantitative hidden-component lower bounds and span-complement synthesis are deferred; no proposed bound depends on them.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 23e383273bba673ba3b6e5e6022bc1fba392f6efb16a1eb808251b44a06babd5

Assess and natively prove the D_dense transfer of unrestricted randomized expected-loss/expected-cost b5 to deterministic pointwise-loss/pathwise-cost q1; preserve every source dimension/accuracy guard and distinct quantity IDs before any adoption.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 5f5df550ff80b63bafbed7ddd22bdf1fc4a6801fd53e5994aa87e5804ee654e5

Assess and natively prove the D_dense transfer of unrestricted randomized expected-loss/expected-cost b5 to the randomized linear-span q1 in its unassessed span complement; a new guarded comparison/bound may be needed. Preserve IDs and do not relabel the existing disjoint Z comparison.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: b45a13c46afbc0aab239e5823ead1e1ae199e6c8b32985d5415e1e7abcb09b3c

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: dbceda45b21a0ffe45277578d6046a1e49e7730c94f41fa771f5a841d96d3d57

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: c2a681b30dd6ef796ef66691bd86e413de337a79a747b1c1bae84e2440c8a429

SO_FO_F02_sc_ms__randomized__expected_loss__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 739f6c98c2e80c0b5e3a362dceca1e1dee7ff7429c2b75d0046f20ed795a63bf

Strong convexity implies mu-PL; Algorithm 1 uses only gradients and exactly the target expected-cost accounting. See the complete native proof.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: ddae27b67763f9c9e97b1642e696a251d27b99db3a39ead8f5cc37d45be99181

source_theorem

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 5c651c341e8582e9b0b20cf6b790bfc9bda6d7bbfdcbadd262c4d4962ce578b3

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: 83cebb71f79cf1985a667ef0b86fc3fff7eae6b7bdda264a92f9b897626b8b9d

F02_MS_PAGE_GRADIENT_TRANSFER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 929e7cc72de00a2a8e3560b3621a0233fc758762b75b98e23d3e81800155fc04

mu-PL finite sums, beta mean-square smoothness, gap Delta; arbitrary d,n>=1, 1<=kappa<=sqrt(n).

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 2533b8a870020307c281f0deb69d64bf51f8ef5fe996df6d6a8985bc0e08c441

arXiv:2609.00045v3, 2026-10-10; Algorithm 1 p.9, Lemma E.1 and Proposition E.2 pp.47-49; read characters 26000-30500 and 111000-119000; dates at abstract-page characters 0-5012.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: dedb2e4ca1fbb13c60f876530ffb6a509064d82fd568a36cba94bf14c69649c6

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: e5dda0cd5237cf61fe20c407dfbca09aedf6bf2436ab18d75eb19d9d2a637fae

SO_SRC_b44bad59cad582d9

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 18a0a4c41261e6830793faeb4b02b1cf0426fc78ab0627dfab1d73a4979a83db

The unchanged strongly convex-average target intersect 1<=kappa<=sqrt(n).

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: abb089920a47a735f51a0cbb535edc307607a71e4788c938c121f797e8ba7295

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 03785648550f6477360e9443d1fa43e09eb3217abb550725c628f9b309fede1d

SO_FO_F02_sc_ms__randomized__expected_loss__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 7a9f932610858ef30a3f42a37411f6e4bb693ffb5aac8a6dd978d23262386d04

Equality at beta=mu identifies the minimizer from a full gradient; n-call pointwise witness meets the expected contract.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: c972700fbd458fda0fee1014c9d989bfebcb734b92cdc7e33e443d8ffb37fb20

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: d075bab0272472417b7b76027253659b233c1732af4edf2d1c9ec8e1aece3ece

F02_MS_UNIT_CONDITION_AND_GUARDS

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 1b347ae6cc7b266ab45d2e92644a3724ae418efde6ed827b0fc2c7f7ea09ed0a

Frozen smoothness and strong-monotonicity premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 25e63e7fa2e68258dd1dc11251a9742b46228ab241733b48542942addda76144

Frozen /proofs and /common_specification, exact hashes in finding/proof F02_MS_UNIT_CONDITION_AND_GUARDS.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 7cd282a8e62f98cdcb0196ff34418afd4a592c7c4072a06e7ec5e2fbfe56c010

Randomized unrestricted target, kappa=1, every d,n>=1.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 2916752d6c7f1ab10871fc4701d8103788f4c22389e693f25578202ddf2a9dc0

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 085b5237ee06324a35745a9192dd9a7f9984d77a59806b8216f614d865126916

SO_FO_F02_sc_ms__deterministic__deterministic__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 598a0cb0428dd06f199ec6e088b8a67ecbe5a45466afcdf124c38135b356b198

The witness is deterministic, with n calls on each path and zero loss; no quantity-ID merge.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: c972700fbd458fda0fee1014c9d989bfebcb734b92cdc7e33e443d8ffb37fb20

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: d075bab0272472417b7b76027253659b233c1732af4edf2d1c9ec8e1aece3ece

F02_MS_UNIT_CONDITION_AND_GUARDS

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: ccfa4bed406b7cf2a90100c5c8dfecf901b22b7b59112cd08b7371010199ef4e

Same fixed instance class at beta=mu.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 36b327fc6a939804951b3234d435b7563915b7e4ad2d3c79050821467c33b341

Same complete equality proof, separately recorded for deterministic q1.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 52678af32d5377f46fe3f626e39906f6b6fd0b5c353d2954152540cf7ae48f51

Deterministic target, kappa=1, every d,n>=1.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 06a1378b4343b2a75eac32bec4f342c409dfd4e5beb96549d4f01ba46bc07ead

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: aede0918330648d722e4b851f2f55b2f4c613893e6d5fac3183f0da4cb1917b3

SO_FO_F02_sc_ms__randomized__expected_loss__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 21ab9fbb37047f048ee42fe77f3568fed5042288c3c81a98056a097d2f6f6325

Identical view/g1/q1/resource; r3 subset r2 permits only guarded adoption. Conditional old premise, no validity extension.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: c972700fbd458fda0fee1014c9d989bfebcb734b92cdc7e33e443d8ffb37fb20

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: d075bab0272472417b7b76027253659b233c1732af4edf2d1c9ec8e1aece3ece

F02_MS_UNIT_CONDITION_AND_GUARDS

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 3e822548e70b357d7d7317f4f0e855568ededad9252671b37f1c72e40be4651c

Exactly native D_dense and native expected-budget/expected-gap lower scope.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: a15fdb3e8c4319f89526448e3e8353cf53b0fda8932e395916e91119dbe6de14

Frozen /bounds/4, /comparisons/1, /regimes/2, completely read via their parent arrays.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: dedb2e4ca1fbb13c60f876530ffb6a509064d82fd568a36cba94bf14c69649c6

#### Native item 1

Native pointer: /joint_analysis/provenance/3/source_refs/0; canonical SHA-256: e5dda0cd5237cf61fe20c407dfbca09aedf6bf2436ab18d75eb19d9d2a637fae

SO_SRC_b44bad59cad582d9

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 905bb216a06c8dc32dfed3a2573aae8119f06c0d4feb3b229e64e8483729702d

The same D_dense within c1 and c2, with no guard extension.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: e90c1356ebc29d909688bb82f0815249a6f6035a15c9c5400027db598e1d4ee7

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: b0be5a13c204e06c5d35d148ddb23ea29a914f227f6d94847f5cff8a9df004fc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 606a62dbfb43693613b22c59bb614ff2f59fc0800e67d96bb996cbbd3e4fac93

SO_FO_F02_sc_ms__randomized__expected_loss__c2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 399f59f0cccdbcff28414ab8f751ae13f20033b8f39fcfb5dbdaa0680acac2b8

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: d1443a3f5433e32941e2d354263d2f5dafa7e4270aff7e50fb39ad2fba17340a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: e222f70d2fbc76f959ba5d014d8ce326c148c5f74224014d184df38a8251c06e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 52a7fe7e3a26e8630cd48a0021ee2d2ed788a675485c4f8ebd3b17815764fda8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 323860be03d6df2ae08d2a78ed9cbd58067a2df456d3511550e33682bf574cf8

SO_FO_F02_sc_ms__deterministic__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 549ead76064af804003339d8839121d593d87c1c4b14291c31287afbb0f95ce4

SO_FO_F02_sc_ms__deterministic__deterministic__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 085b5237ee06324a35745a9192dd9a7f9984d77a59806b8216f614d865126916

SO_FO_F02_sc_ms__deterministic__deterministic__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: e3dbc77abea392b3687684e4f6c6fa2b68d8d5a273552a091160d1911c82fb1c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: f9620c59304373b5e65cf07b96ce3c29aefb5ef338fa8506c3ee9292bf42eb29

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 68057e7e12a707344ff3c754e0598c9712dec6130e5c371a1091109e3a5fa21d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 8e73e1078a395593b9af485eb5b3d67102246479315dce4a0e2b12bdea5da790

SO_FO_F02_sc_ms__randomized__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 66b8130c6d61e0d96ed814c9a86d1b9d1af11d48d2b932fccb7ff58bf8b2bc27

SO_FO_F02_sc_ms__randomized__expected_loss__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 419b36cc2ac88cee094fbc6bf9bb280dc920720773754a3f4249e2bed2432a93

SO_FO_F02_sc_ms__randomized__expected_loss__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: b790bb86d54a91734ce8623dbc23ac042e4155331da3955fcddd44b4cede7f64

SO_FO_F02_sc_ms__randomized__expected_loss__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/4; canonical SHA-256: aede0918330648d722e4b851f2f55b2f4c613893e6d5fac3183f0da4cb1917b3

SO_FO_F02_sc_ms__randomized__expected_loss__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/5; canonical SHA-256: c2a681b30dd6ef796ef66691bd86e413de337a79a747b1c1bae84e2440c8a429

SO_FO_F02_sc_ms__randomized__expected_loss__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/6; canonical SHA-256: 03785648550f6477360e9443d1fa43e09eb3217abb550725c628f9b309fede1d

SO_FO_F02_sc_ms__randomized__expected_loss__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: b71bcc1526e5c27cbf8d7b5011bc89019ff1db00baaf8c7aff43edeeeb501b87

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 8292c6a932e9ceb0aab8e0e6ac18215b9847794d46840b22c2709d2a79d751f5

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 68057e7e12a707344ff3c754e0598c9712dec6130e5c371a1091109e3a5fa21d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: 8e73e1078a395593b9af485eb5b3d67102246479315dce4a0e2b12bdea5da790

SO_FO_F02_sc_ms__randomized__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 66b8130c6d61e0d96ed814c9a86d1b9d1af11d48d2b932fccb7ff58bf8b2bc27

SO_FO_F02_sc_ms__randomized__expected_loss__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: 419b36cc2ac88cee094fbc6bf9bb280dc920720773754a3f4249e2bed2432a93

SO_FO_F02_sc_ms__randomized__expected_loss__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: b790bb86d54a91734ce8623dbc23ac042e4155331da3955fcddd44b4cede7f64

SO_FO_F02_sc_ms__randomized__expected_loss__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/4; canonical SHA-256: aede0918330648d722e4b851f2f55b2f4c613893e6d5fac3183f0da4cb1917b3

SO_FO_F02_sc_ms__randomized__expected_loss__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/5; canonical SHA-256: c2a681b30dd6ef796ef66691bd86e413de337a79a747b1c1bae84e2440c8a429

SO_FO_F02_sc_ms__randomized__expected_loss__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/6; canonical SHA-256: 03785648550f6477360e9443d1fa43e09eb3217abb550725c628f9b309fede1d

SO_FO_F02_sc_ms__randomized__expected_loss__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 418eefc15dce23eb339c992a799ab202b7be2e4eaf38aeca6630b692c8ad5a00

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 606a62dbfb43693613b22c59bb614ff2f59fc0800e67d96bb996cbbd3e4fac93

SO_FO_F02_sc_ms__randomized__expected_loss__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 8cd647717cfa7f33958abbd9c638693d3106f55553cc49fd0b2967fdd30dcb73

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 240084a1fb4325bae8ffee3313602dca98b661ad362f66990eab22aa33791fe6

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: b51bed53fac6542c523852678ea221c8e437a82481f507c2c2b65ae97d6fdeb1

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: 09ecd540fee2c569ac3f92d9c03a17f9a62f98ee6cf48a0e4e06014d11ddedcb

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 851b52e8fe3e3494c2ab4132ebb676cfa78efa4cc26e16470dc0b451f84f01d6

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 399f59f0cccdbcff28414ab8f751ae13f20033b8f39fcfb5dbdaa0680acac2b8

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 66815948a4b83841cb60f445babe49e8063535e7b4bcede451c90dfd0f321a0c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 79e8ecadc0249b0931d625bbe430b934f64189fb1894d810552aaafcfb12eac4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: 606a62dbfb43693613b22c59bb614ff2f59fc0800e67d96bb996cbbd3e4fac93

SO_FO_F02_sc_ms__randomized__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/2; canonical SHA-256: 399f59f0cccdbcff28414ab8f751ae13f20033b8f39fcfb5dbdaa0680acac2b8

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/3; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: cce3fe6fe250c4cbd72965ec22d3ad149c0175f60421896746bb2ddf9db62d15

Finish discovery: two arXiv HTTP-429 failures and noisy Crossref search 6cf8c8212bb0cd952623f110c8ca868fca55d014de59cb5f7207340173d4927a with unprocessed cursor MTcxMDQxMDk5ODAwMCwxMC4xMDM3JTJGbWV0MDAwMDY0OQ==. All five returned records were exposed; no terminal replacement or complete-search claim.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 59a11c1b6f669313d3c7fad4876b0ac43ca69351114787872a3016f9b31587f7

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 79e8ecadc0249b0931d625bbe430b934f64189fb1894d810552aaafcfb12eac4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: 606a62dbfb43693613b22c59bb614ff2f59fc0800e67d96bb996cbbd3e4fac93

SO_FO_F02_sc_ms__randomized__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/2; canonical SHA-256: 399f59f0cccdbcff28414ab8f751ae13f20033b8f39fcfb5dbdaa0680acac2b8

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/3; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 630e6bcfcde7fbfea8192378e18070fb346a2c2e8c3fee11aba313674e83664d

Sharper near-unit-condition rates, quantitative hidden-component lower bounds and span-complement synthesis are deferred; no proposed bound depends on them.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 2efd000396d002a09ab2a8feab31c56728c3ea6f873e0490bc66b9f9f2c7bc6a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: 0f800d9d56822ce5710f83f87cbe81003530fdab872d2dcd627e9f51f9a01c27

Source SO_FO_F02_sc_ms__randomized__expected_loss__b5 has D_dense: n>=1024,3<=kappa<=sqrt(n),d>=d_dense,0<epsilon<=cDelta. A deterministic all-instance pointwise-loss algorithm with pathwise capB is an unrestricted randomized algorithm with expectedgap<=epsilon and expectedcost<=B. This identifies a directional subclass/stronger-guarantee route, not a permission to copy a distinct quantity ID. Verify complete source/target oracle/instance/initialization and cost conventions, write a full native transfer proof and quantity-matched bound before any adoption. Potential effect: fill/improve the deterministic missing lower on D_dense only; not at kappa1, lowerdimension or outside this guard. No transferred bound is adopted in this metadata correction.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 7602903e0513248a1c3b512450913dfdae747fc5d4841ea307b0b86d08e76890

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/0; canonical SHA-256: aede0918330648d722e4b851f2f55b2f4c613893e6d5fac3183f0da4cb1917b3

SO_FO_F02_sc_ms__randomized__expected_loss__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 0dd0f165c054d8017d087fdbd4515a475fdf7c9a3c95e6682a0874f31c204473

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids/0; canonical SHA-256: c929ec151d3d22026a833b2c674731372012cbd16fe1c493210d42546b1fe9ae

deterministic_other

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: e3dbc77abea392b3687684e4f6c6fa2b68d8d5a273552a091160d1911c82fb1c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 366c2d939ad8723022ccfa9406972b8f203eac0c98fd25639b6d220bf08a7da4

dense-unrestricted-to-deterministic

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 23e383273bba673ba3b6e5e6022bc1fba392f6efb16a1eb808251b44a06babd5

Assess and natively prove the D_dense transfer of unrestricted randomized expected-loss/expected-cost b5 to deterministic pointwise-loss/pathwise-cost q1; preserve every source dimension/accuracy guard and distinct quantity IDs before any adoption.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: f2e384f0de6fbc0ed69e7216fb72975792e4f18f40387d8e99756c9fb0103abb

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: 0f800d9d56822ce5710f83f87cbe81003530fdab872d2dcd627e9f51f9a01c27

Source SO_FO_F02_sc_ms__randomized__expected_loss__b5 has D_dense: n>=1024,3<=kappa<=sqrt(n),d>=d_dense,0<epsilon<=cDelta. A deterministic all-instance pointwise-loss algorithm with pathwise capB is an unrestricted randomized algorithm with expectedgap<=epsilon and expectedcost<=B. This identifies a directional subclass/stronger-guarantee route, not a permission to copy a distinct quantity ID. Verify complete source/target oracle/instance/initialization and cost conventions, write a full native transfer proof and quantity-matched bound before any adoption. Potential effect: fill/improve the deterministic missing lower on D_dense only; not at kappa1, lowerdimension or outside this guard. No transferred bound is adopted in this metadata correction.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 7602903e0513248a1c3b512450913dfdae747fc5d4841ea307b0b86d08e76890

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/0; canonical SHA-256: aede0918330648d722e4b851f2f55b2f4c613893e6d5fac3183f0da4cb1917b3

SO_FO_F02_sc_ms__randomized__expected_loss__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 0dd0f165c054d8017d087fdbd4515a475fdf7c9a3c95e6682a0874f31c204473

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids/0; canonical SHA-256: c929ec151d3d22026a833b2c674731372012cbd16fe1c493210d42546b1fe9ae

deterministic_other

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: e3dbc77abea392b3687684e4f6c6fa2b68d8d5a273552a091160d1911c82fb1c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: d27feb5a8b8ab8f081557c95058c61d3dd6491badd4b3c73c96b880d48cf5af3

dense-unrestricted-to-deterministic-material-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 23e383273bba673ba3b6e5e6022bc1fba392f6efb16a1eb808251b44a06babd5

Assess and natively prove the D_dense transfer of unrestricted randomized expected-loss/expected-cost b5 to deterministic pointwise-loss/pathwise-cost q1; preserve every source dimension/accuracy guard and distinct quantity IDs before any adoption.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: 4af7ea49fb3fa8fcd7a3263fd7f2436aeb8ef2878600bb68749188feb3ec2309

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: 8f793a8ed32ff153519e600a458ea065b03019e052a8f1edf9ee4cbaef8cd64e

Span randomized expected-loss/expected-cost algorithms are a restricted subclass of the same unrestricted randomized contract, giving a concrete lower-transfer route on source D_dense after exact contract verification. Existing span c1 uses Z with kappa>=4sqrt(n), whereas D_dense has kappa<=sqrt(n), so they are disjoint for n>=1024. The existing c1 is listed only as the native target quantity/algorithm-contract anchor: no change to its optimal Z envelope is asserted. The actual opportunity lies in domaincell span_complement, with no native comparison there yet. A complete native mapping and new quantity-matched bound/comparison are required before publication. It may add a lower in that unassessed complement; it is not a proof of a matching whole-complement rate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 7602903e0513248a1c3b512450913dfdae747fc5d4841ea307b0b86d08e76890

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/0; canonical SHA-256: aede0918330648d722e4b851f2f55b2f4c613893e6d5fac3183f0da4cb1917b3

SO_FO_F02_sc_ms__randomized__expected_loss__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: f69d65463b4ec4053f8708494cb82ad075041cf89bf94428410a2851ca76161e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids/0; canonical SHA-256: 8d3c8d93e94f0039ff326ae17fd4c4c85dbccd79f2b448b482a519c0ad958e3e

span_complement

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 851b52e8fe3e3494c2ab4132ebb676cfa78efa4cc26e16470dc0b451f84f01d6

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 399f59f0cccdbcff28414ab8f751ae13f20033b8f39fcfb5dbdaa0680acac2b8

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 2779aa317dfba935d154b1e733edcae82acb22048ba5e838d370dd6af642f4d6

dense-unrestricted-to-span-complement

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 5f5df550ff80b63bafbed7ddd22bdf1fc4a6801fd53e5994aa87e5804ee654e5

Assess and natively prove the D_dense transfer of unrestricted randomized expected-loss/expected-cost b5 to the randomized linear-span q1 in its unassessed span complement; a new guarded comparison/bound may be needed. Preserve IDs and do not relabel the existing disjoint Z comparison.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 648471d085a26f0ea928a916f6fd942b954355c41310ac63e116583ddbf7c5ab

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: 8f793a8ed32ff153519e600a458ea065b03019e052a8f1edf9ee4cbaef8cd64e

Span randomized expected-loss/expected-cost algorithms are a restricted subclass of the same unrestricted randomized contract, giving a concrete lower-transfer route on source D_dense after exact contract verification. Existing span c1 uses Z with kappa>=4sqrt(n), whereas D_dense has kappa<=sqrt(n), so they are disjoint for n>=1024. The existing c1 is listed only as the native target quantity/algorithm-contract anchor: no change to its optimal Z envelope is asserted. The actual opportunity lies in domaincell span_complement, with no native comparison there yet. A complete native mapping and new quantity-matched bound/comparison are required before publication. It may add a lower in that unassessed complement; it is not a proof of a matching whole-complement rate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 7602903e0513248a1c3b512450913dfdae747fc5d4841ea307b0b86d08e76890

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/0; canonical SHA-256: aede0918330648d722e4b851f2f55b2f4c613893e6d5fac3183f0da4cb1917b3

SO_FO_F02_sc_ms__randomized__expected_loss__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: f69d65463b4ec4053f8708494cb82ad075041cf89bf94428410a2851ca76161e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids/0; canonical SHA-256: 8d3c8d93e94f0039ff326ae17fd4c4c85dbccd79f2b448b482a519c0ad958e3e

span_complement

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 851b52e8fe3e3494c2ab4132ebb676cfa78efa4cc26e16470dc0b451f84f01d6

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 399f59f0cccdbcff28414ab8f751ae13f20033b8f39fcfb5dbdaa0680acac2b8

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: d74af488ce930bc1844695d82152c5061d6e19947913b51beda1d021087ab4a0

dense-unrestricted-to-span-complement-material-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 5f5df550ff80b63bafbed7ddd22bdf1fc4a6801fd53e5994aa87e5804ee654e5

Assess and natively prove the D_dense transfer of unrestricted randomized expected-loss/expected-cost b5 to the randomized linear-span q1 in its unassessed span complement; a new guarded comparison/bound may be needed. Preserve IDs and do not relabel the existing disjoint Z comparison.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: ac199033fcb13ad604229382d81d264b38cff9ed87157b84bb020b0899c968cd

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: 79e8ecadc0249b0931d625bbe430b934f64189fb1894d810552aaafcfb12eac4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: 239a688e3b1d25694305020cee7037ab29f0ab9a919db6a86ee7e8513d9e4184

SO_FO_F02_sc_ms__randomized__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/1; canonical SHA-256: 606a62dbfb43693613b22c59bb614ff2f59fc0800e67d96bb996cbbd3e4fac93

SO_FO_F02_sc_ms__randomized__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/2; canonical SHA-256: 399f59f0cccdbcff28414ab8f751ae13f20033b8f39fcfb5dbdaa0680acac2b8

SO_FO_F02_sc_ms__randomized__linear_span__expected_loss__c1

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/3; canonical SHA-256: d0831708e5cac7aa998e0411893263c42c533a2bdcc178357bf0e73776752880

SO_FO_F02_sc_ms__deterministic__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 7b66618750ce506ccf40819cef50f764846b4ebf660cc36789c8ef551ca05dfe

curated-scope-limit-2a144b4edf

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 6a48c1be38739b36dde9c00da63c01083b54999ae787aed3b23dbee15dea1f46

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: a00fa4176bb7aefe6c8f87b275a4e9cdf2273435cb1db0bf14830a550f446110

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 8d65311f8a785198e53a1915bb5908b3c4abf1e26623fde6d8d4f09ed2c903fc

/views/1

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: 2498f2d25116b918966965c7d103716acf03b57a449fc0f6519db9fdf2357be3

/views/2

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 7

Native pointer: /joint_analysis/target/contract_refs/6; canonical SHA-256: f1096cde15a520562dc4693c6e0b624bdb9b388f32263d6c4947dbf7a56c363a

/quantities/1

#### Native item 8

Native pointer: /joint_analysis/target/contract_refs/7; canonical SHA-256: 4b81cab280b1e31c2ea7afa9a416577b7c9c22795698d5d642e0394c36a90edd

/quantities/2

#### Native item 9

Native pointer: /joint_analysis/target/contract_refs/8; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native item 10

Native pointer: /joint_analysis/target/contract_refs/9; canonical SHA-256: 7bb9459dcac5b77a99df0d6dbaa2fe9f7fd0b02dfef9f93123a32f8fe3041262

/regimes/3

#### Native item 11

Native pointer: /joint_analysis/target/contract_refs/10; canonical SHA-256: f1bcac22d3bd2dc168a105bfbea334e0e43f5794256ea11f9b6af12fec35896e

/regimes/7

#### Native item 12

Native pointer: /joint_analysis/target/contract_refs/11; canonical SHA-256: b172ac3a49bac5042090cb45d060b07164d7e0acb899134d6686e3bcd66f63e3

/regimes/10

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: cc525b820edc1518ebdeee8346e2bdb56b8323f1d90f88e63cb7686a5141df10

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 1d1a3505b50fc3327652d3a0852ee8b0c5c2ef93d6e4856c5cb780b27fcbce33

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: 5a5d428e98f33ec83f04266dad8e0c00d58dd070a116f1fe7667f872b362c001

Native theorem-dependent sufficiently small universal constant, 0<c<1; not a numerical transition.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: 45c6f59909413113c16bd798dea368d2e906421b9acab31513b8c96bd077d326

SO_FO_F02_sc_ms_p_b48b2597a7

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 879923da020d1533f4d8e921ea7bac61e8ba41d3c89d17a4d14e3a89c6780d5d

c

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: dd3eef0d2320835e2365164178ccccdd576d5e206a6184672956b735acd9b93e

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: c100fe0dab4d6dfea88b7028e87ccc1388390abe679a04acc5834dc0c6e75f15

Native sufficiently large universal bound constant, C>1.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: 78e928076612ccc73eb6d020e23e448238f80c73faf57f0e121a588a32b0e841

SO_FO_F02_sc_ms_p_5eeb762d76

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: c2e8c0cc2e73b9bd1ba9ef1979e73169b471e25b0e9909efe98fde462c0bf55f

C

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: c33b3e5c793b71361e1394e59f19f333e063a581816f5ca3771acf288836791e

Separate native minimax component-call quantities for unrestricted randomized/expected gap and cost, span randomized/expected gap and cost, and deterministic/pointwise gap and pathwise cost. In every view: d,n positive integers, beta,mu,Delta>0, mu<=beta, kappa=beta/mu, 0<epsilon<=c Delta. R is an inert inherited coordinate, with no added distance promise; constants are independent of it. Write tau=epsilon/Delta, L=log(1/tau), H=1+log(sqrt(n)/kappa), P=n+nL/H on kappa<=sqrt(n). D_dense is native randomized r3: n>=1024, 3<=kappa<=sqrt(n), d>=d_dense. Z is native span r3: kappa>=4sqrt(n), tau<=c min(1,n^(7/2)/kappa^3), d>=d_ZG. Dimension thresholds are sufficient source conditions, not intrinsic transitions.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 7f4d12b69c7f8d1179c76a74452bc89ae5e4fba2537e9ec1438a57b350cdc3f6

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 8149384cfad8f7fe9820e7c5ba1ca12946055ec864d7744a84d1dc304e440fd2

SO_FO_F02_sc_ms_p_b4e942dc3f

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: f691c2274fea62b581e2e7234f7d13c36d902335c2050f742da379588f637e25

SO_FO_F02_sc_ms_p_a2fb90437f

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 2d23a3f7df0453ed36e1a247e9ca65f18ddb7cb5bf5562c97cb2c75577d94655

SO_FO_F02_sc_ms_p_d360d55977

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: 461ddd250f01e3bdba59ae95d56061bcd87f7f12904f0622bb36710c71bbaebf

SO_FO_F02_sc_ms_p_daf3a45a8f

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 17649022a760f1814970ee01dc39727a1370e433f28e4138f95738d1afdfbc09

SO_FO_F02_sc_ms_p_e65970dd2a

#### Native item 6

Native pointer: /joint_analysis/target/joint_variables/5; canonical SHA-256: 809cf7f3f8b688bb44f72dab856be38c4997fc34f13582b6b9db634f2d646fcd

SO_FO_F02_sc_ms_p_1bb94fe04b

#### Native item 7

Native pointer: /joint_analysis/target/joint_variables/6; canonical SHA-256: 896d6a2c0db67aa798ce57c4e9dcb0fd65c709c71eaacc0751b891d14e875206

SO_FO_F02_sc_ms_p_95775a4b65

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 48fac6562cb0fa4938d16a6c34597ad78e8cdf4c1648d4df88b961f9f6520aec

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: 88c56f2973676aa174b520b5c0637ef8af45c8f934565cb133349e67b99bb1ee

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: d4f6d273d6f84c9d21f04b326bdec09d8af9dfd090a4d9dd089e5468f8b26516

tau=epsilon/Delta. Multiplying all component objectives and beta,mu,Delta,epsilon by the same positive factor preserves algorithms by scaling gradient replies and preserves query counts. Thus tau is dimensionless; native parameters keep their identities.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: f5579508d32d49b0fc416d2f0d840524171904d08c641e7a9fbb840ed2b1da43

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: 896d6a2c0db67aa798ce57c4e9dcb0fd65c709c71eaacc0751b891d14e875206

SO_FO_F02_sc_ms_p_95775a4b65

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: 809cf7f3f8b688bb44f72dab856be38c4997fc34f13582b6b9db634f2d646fcd

SO_FO_F02_sc_ms_p_1bb94fe04b

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: 679c97609fb336420cb339dd72db6965df4d5c2e6133cf2dd498cf3f674f4440

tau

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 7f4d12b69c7f8d1179c76a74452bc89ae5e4fba2537e9ec1438a57b350cdc3f6

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 8149384cfad8f7fe9820e7c5ba1ca12946055ec864d7744a84d1dc304e440fd2

SO_FO_F02_sc_ms_p_b4e942dc3f

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: f691c2274fea62b581e2e7234f7d13c36d902335c2050f742da379588f637e25

SO_FO_F02_sc_ms_p_a2fb90437f

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 2d23a3f7df0453ed36e1a247e9ca65f18ddb7cb5bf5562c97cb2c75577d94655

SO_FO_F02_sc_ms_p_d360d55977

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 461ddd250f01e3bdba59ae95d56061bcd87f7f12904f0622bb36710c71bbaebf

SO_FO_F02_sc_ms_p_daf3a45a8f

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 17649022a760f1814970ee01dc39727a1370e433f28e4138f95738d1afdfbc09

SO_FO_F02_sc_ms_p_e65970dd2a

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: 809cf7f3f8b688bb44f72dab856be38c4997fc34f13582b6b9db634f2d646fcd

SO_FO_F02_sc_ms_p_1bb94fe04b

#### Native item 7

Native pointer: /joint_analysis/target/uniform_in/6; canonical SHA-256: 896d6a2c0db67aa798ce57c4e9dcb0fd65c709c71eaacc0751b891d14e875206

SO_FO_F02_sc_ms_p_95775a4b65

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Zeyuan Allen-Zhu. Katyusha X: Practical Momentum Method for Stochastic Sum-of-Nonconvex Optimization. 2018; Corollaries 4.4 and 4.7, PDF pp.13-14.

https://arxiv.org/pdf/1802.03866

[2] Dongruo Zhou and Quanquan Gu. Lower Bounds for Smooth Nonconvex Finite-Sum Optimization. 2019; Definition 3.3; Theorem 4.2; Section 4.3 and Proposition 4.9.

https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf

[3] Yuxing Peng, Zhiqing Tang and Weijia Jia. Dense Weak Hiding: Closing Complexity Gaps in Nonconvex and PL Finite-Sum Optimization under Individual Smoothness. 2026, arXiv v3 preprint; Theorems 3.1 and 3.3; Corollary 3.2; Proposition E.2; Appendices F and G.1.

https://arxiv.org/pdf/2609.00045v3

[4] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015.

https://arxiv.org/pdf/1405.4980

[5] Yoel Drori; Adrien Taylor. On the oracle complexity of smooth strongly convex minimization. 2021; arXiv:2101.09740v2.

https://arxiv.org/pdf/2101.09740v2

[6] Yoel Drori. Exact oracle complexity for function-value suboptimality under weighted initial conditions. 2026-10-16; preprintv2.

https://arxiv.org/pdf/2609.33360v2

[7] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 2026-09-09; preprintv1.

https://arxiv.org/pdf/2609.10874

[8] Arkadi Nemirovski; Shmuel Onn; Uriel G. Rothblum. Accuracy Certificates for Computational Problems with Convex Structure. 2010.

https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf

[9] David Martínez-Rubio; Cristóbal Guzmán. Stable Movement for Nondual Lipschitz Convex Optimization: Efficiency and Nearly Optimal Oracle Rates. 2026-09-17; preprintv1.

https://arxiv.org/pdf/2609.20701
