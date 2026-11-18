# Finite-sum minimization with convex components: queries within the ball; selected component gradients

**Setting ID.** `SO_FO_F01_bounded_G`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; convexity: Convex components; geometry: Euclidean ball; geometry: Full space; smoothness: Individual smoothness; smoothness: Lipschitz gradient; structure: Finite sum

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Component gradient; operation: Component gradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; budget: Worst-instance expected cost; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}F(x)$$

The complete objective is the finite sum $F(x)=n^{-1}\sum_{i=1}^n f_i(x)$. Component information is available only through the declared component oracle.

### Admissible model

There are $n$ fixed unknown convex $\beta$-smooth components, with $F=n^{-1}\sum_i f_i$, on the public ball $Q=RB_2^d$. A minimizer may lie on the boundary.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Individual smoothness means $\|\nabla f_i(u)-\nabla f_i(v)\|_2\le\beta\|u-v\|_2$ simultaneously for every $i\in\{1,\ldots,n\}$ and every pair $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad n \ge 1,\quad \varepsilon \le c\,\beta\,{R}^{2}\\\beta > 0,\quad R > 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ n,\ \varepsilon$.

Public upper bounds: $\beta,\ R$.

The unknown objects are the component functions $f_1,\ldots,f_n$.

For each query, the algorithm chooses $i\in\{1,\ldots,n\}$ and $x\in Q$ and receives the following information about that component.

$$\nabla f_i(x)$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

Exact Euclidean projection onto the public domain; its internal computation is free

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=F(\widehat{x})-F^\star$$

$F^\star=\inf_{x\in Q}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One component query at an algorithm-selected pair $(i,x)$ costs one unit; a full gradient costs $n$. Component proximal maps are not free.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Deterministic / Pointwise guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

**Resource qualification.** Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

**Resource qualification.** Cost is bounded in expectation for every instance: $\sup_{I,\mathcal O}\mathbb E N_A\le T$. This contract is not replaced by a fixed bound on every execution path.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f_i,F$: Unknown components and finite-sum objective **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\frac1n\sum_{i=1}^n f_i(x)$$

$\nabla f_i$: Full gradient of differentiable component $i$

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in Q}F(x)$$

$Q$: Feasible set of the task

$$Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$n$: Public number of components in the finite sum or finite maximum. **Domain:** $n\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta>0$.

$L$: Public upper bound on the Lipschitz constant of the objective or components. **Domain:** $L>0$.

$R$: Radius of the public feasible ball **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$T$: Total budget for the declared resource projection; for a risk curve, the budget is fixed in advance **Domain:** $T\in\mathbb{N}_{\ge0}$.

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$\log$: Natural logarithm; changing to another fixed base affects only a constant

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One component query at an algorithm-selected pair $(i,x)$ costs one unit; a full gradient costs $n$. Component proximal maps are not free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One component query at an algorithm-selected pair $(i,x)$ costs one unit; a full gradient costs $n$. Component proximal maps are not free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Sufficiently high-dimensional deterministic convex regime

**Region.** $d\ge Cn\sqrt{\beta R^2/\varepsilon}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One component query at an algorithm-selected pair $(i,x)$ costs one unit; a full gradient costs $n$. Component proximal maps are not free.

**Status.** Optimal

**Lower bound.** B2

$$
cn\sqrt{\beta R^2/\varepsilon}
$$

**Upper bound.** B1

$$
Cn\sqrt{\beta R^2/\varepsilon}
$$

**Gap or comparison.** $O(1)$

### R2 - Sufficiently high-dimensional randomized convex regime

**Region.** $d\ge C\beta^2R^4\varepsilon^{-2}\log(2+n\beta R^2/\varepsilon)$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** One component query at an algorithm-selected pair $(i,x)$ costs one unit; a full gradient costs $n$. Component proximal maps are not free.

**Status.** Logarithmic gap

**Lower bound.** B5

$$
c[n+\sqrt{n\beta R^2/\varepsilon}]
$$

**Upper bound.** B4, B3

$$
C\min\{n\sqrt{\beta R^2/\varepsilon},n\log\log(e^e+n)+\sqrt{n\beta R^2/\varepsilon}\}
$$

**Gap or comparison.** $O(\log\log(e^e+n))$

**Comparison argument.** Compare on the intersection of F01.bounded-R-G.parameter-domain and F01.cv-R-hd. The randomized expected-budget contract leaves a log-logarithmic factor in $n$. Constant-factor optimality holds when the accuracy term dominates $n\log\log n$.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Full accelerated gradient

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
Cn\sqrt{\beta R^2/\varepsilon}
$$

**Sources.** [2](https://arxiv.org/pdf/1405.4980)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [2](https://arxiv.org/pdf/1405.4980) theorem: Thm3.19 plus n component full-gradient simulation

### B2 - Deterministic lower bound for bounded queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
cn\sqrt{\beta R^2/\varepsilon}
$$

**Sources.** [1](https://arxiv.org/pdf/1605.08003v3)

**Conditions.** $$d\ge Cn\sqrt{\beta R^2/\varepsilon}$$

**Dimension conditions.** $d\ge Cn\sqrt{\beta R^2/\varepsilon}$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/1605.08003v3) theorem: Theorems3,4,7,8; AppendicesB.3,B.4,C.3,C.4; PDF pp.6,8

### B3 - Full accelerated gradient

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
Cn\sqrt{\beta R^2/\varepsilon}
$$

**Sources.** [2](https://arxiv.org/pdf/1405.4980)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [2](https://arxiv.org/pdf/1405.4980) theorem: Thm3.19 plus n component full-gradient simulation

### B4 - RECAPP

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C[n\log\log(e^e+n)+\sqrt{n\beta R^2/\varepsilon}]
$$

**Sources.** [3](https://proceedings.mlr.press/v162/carmon22a/carmon22a.pdf)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [3](https://proceedings.mlr.press/v162/carmon22a/carmon22a.pdf) theorem: Theorem4.3; AppendixB.4; PDF p.7

### B5 - WS16 randomized lower bound with bounded queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[n+\sqrt{n\beta R^2/\varepsilon}]
$$

**Sources.** [1](https://arxiv.org/pdf/1605.08003v3)

**Conditions.** $$d\ge C\beta^2R^4\varepsilon^{-2}\log(2+n\beta R^2/\varepsilon)$$

**Dimension conditions.** $d\ge C\beta^2R^4\varepsilon^{-2}\log(2+n\beta R^2/\varepsilon)$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound. Converting the source hard event to an expected-error statement retains the constant tolerance rescaling. Expected running costs additionally require a stopping-time truncation with its constant loss.

**Source location.** [1](https://arxiv.org/pdf/1605.08003v3) theorem: Theorems3,4,7,8; AppendicesB.3,B.4,C.3,C.4; PDF pp.6,8

## References

[1] Blake Woodworth and Nathan Srebro. Tight Complexity Bounds for Optimizing Composite Objectives. 2016; arXiv v3 2019; Theorems 3, 4, 7, 8; Appendices B.3/B.4/C.3/C.4.

https://arxiv.org/pdf/1605.08003v3

[2] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015; Theorems 2.1, 3.2, 3.9, 3.18, and 3.19: centroid, subgradient, and accelerated upper bounds..

https://arxiv.org/pdf/1405.4980

[3] Yair Carmon, Arun Jambulapati, Yujia Jin and Aaron Sidford. RECAPP: Crafting a More Efficient Catalyst for Convex Optimization. 2022; Theorem 4.3, PDF p.7 and Appendix B.4.

https://proceedings.mlr.press/v162/carmon22a/carmon22a.pdf
