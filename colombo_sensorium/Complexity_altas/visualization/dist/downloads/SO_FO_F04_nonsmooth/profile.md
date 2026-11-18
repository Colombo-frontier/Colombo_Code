# Minimization of a finite maximum of convex functions: nonsmooth components; selected component values and subgradients

**Setting ID.** `SO_FO_F04_nonsmooth`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Logarithmic gap present; Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; convexity: Convex components; geometry: Euclidean ball; geometry: Full space; smoothness: Component nonsmooth allowed; smoothness: Lipschitz function; structure: Finite max

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Component value subgradient; operation: Component value subgradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}F(x)$$

The complete objective is $F(x)=\max_{1\le i\le n}f_i(x)$. It may be nonsmooth even when all components are smooth.

### Admissible model

There are $n$ unknown convex $L$-Lipschitz components on a public ball. Differentiability and component smoothness are not assumed.

Feasible geometry: $Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad n \ge 1,\quad L > 0\\R > 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ n,\ \varepsilon$.

Public upper bounds: $L,\ R$.

The unknown objects are the component functions $f_1,\ldots,f_n$.

For each query, the algorithm chooses $i\in\{1,\ldots,n\}$ and $x\in Q$ and receives the following information about that component.

$$(f_i(x),g_i),\quad g_i\in\partial f_i(x)$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

Exact Euclidean projection onto the public domain; its internal computation is free

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=F(\widehat{x})-F^\star$$

$F^\star=\inf_{x\in Q}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One component value together with one subgradient costs one call.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f_i,F$: Unknown components and finite-maximum objective **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\max_{1\le i\le n}f_i(x)$$

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in Q}F(x)$$

$Q$: Feasible set of the task

$$Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial f_i(x)$: Ambient subdifferential of the corresponding convex function

$$\partial f_i(x)=\{g:f_i(u)\ge f_i(x)+\langle g,u-x\rangle\ \forall u\in\operatorname{dom}f_i\}$$

$g$: One subgradient vector selected and returned by the oracle, rather than the entire subdifferential

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$n$: Public number of components in the finite sum or finite maximum. **Domain:** $n\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the Lipschitz constant of the objective or components. **Domain:** $L>0$.

$R$: Radius of the public feasible ball **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$A_\varepsilon$: Dimensionless quantity $LR/\epsilon$, used only to shorten formulas.

$$A_\varepsilon=\frac{L\,R}{\varepsilon}$$

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

**Definition.** One component value together with one subgradient costs one call.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Nontrivial suboptimality

**Region.** $0<\varepsilon\le cLR$

**Quantity.** Q1

**Resource.** One component value together with one subgradient costs one call.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
\widetilde{O}(nA_\varepsilon^{2/3}+A_\varepsilon^2)
$$

### R2 - nonsmooth componentssufficiently high dimension

**Region.** $0<\varepsilon\le cLR,\quad d\ge C A_\varepsilon^2\log(2+nA_\varepsilon)$

**Quantity.** Q1

**Resource.** One component value together with one subgradient costs one call.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
c(nA_\varepsilon^{2/3}+A_\varepsilon^2)
$$

**Upper bound.** B1

$$
\widetilde{O}(nA_\varepsilon^{2/3}+A_\varepsilon^2)
$$

**Gap or comparison.** $\operatorname{polylog}(n,LR/\varepsilon)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Randomized bias-reduced gradient method

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}(nA_\varepsilon^{2/3}+A_\varepsilon^2)
$$

**Sources.** [2](https://arxiv.org/pdf/2106.09481)

**Conditions.** $$0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: selected component values and subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [2](https://arxiv.org/pdf/2106.09481) theorem: Theorem4; §4.2; AppendixA.3

### B2 - 2021 lower bound for a finite maximum of nonsmooth functions

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c(nA_\varepsilon^{2/3}+A_\varepsilon^2)
$$

**Sources.** [1](https://arxiv.org/pdf/2105.01778)

**Conditions.** $$0<\varepsilon\le cLR,\quad d\ge C A_\varepsilon^2\log(2+nA_\varepsilon)$$

**Dimension conditions.** $0<\varepsilon\le cLR,\quad d\ge C A_\varepsilon^2\log(2+nA_\varepsilon)$

**Oracle correspondence.** Applicable interfaces: selected component values and subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2105.01778) theorem: Theorem3 nonsmooth branch; AppendixD.3

## References

[1] Yair Carmon, Arun Jambulapati, Yujia Jin and Aaron Sidford. Thinking Inside the Ball: Near-Optimal Minimization of the Maximal Loss. COLT 2021, full arXiv version; Theorem 2 and Eq.(9), p.9; Theorem 3 and Eq.(13), p.12; Appendices A.3 and D.3.

https://arxiv.org/pdf/2105.01778

[2] Hilal Asi, Yair Carmon, Arun Jambulapati, Yujia Jin and Aaron Sidford. Stochastic Bias-Reduced Gradient Methods. NeurIPS 2021; arXiv v2; Theorem 4 and Section 4.2; Appendix A.3 on deterministic query budgets.

https://arxiv.org/pdf/2106.09481
