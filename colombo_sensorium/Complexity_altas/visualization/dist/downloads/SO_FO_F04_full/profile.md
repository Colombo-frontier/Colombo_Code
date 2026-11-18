# Minimization of a finite maximum of convex functions: initial distance in the full space; selected component values and gradients

**Setting ID.** `SO_FO_F04_full`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; convexity: Convex components; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz function; structure: Finite max

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Component value gradient; operation: Component value gradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \mathbb{R}^d}F(x)$$

The complete objective is $F(x)=\max_{1\le i\le n}f_i(x)$. It may be nonsmooth even when all components are smooth.

### Admissible model

The $n$ components are globally convex, $L$-Lipschitz, and $\beta$-smooth. The maximum $F=\max_i f_i$ has a global minimizer within distance $R$ of $x_0$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Individual smoothness means $\|\nabla f_i(u)-\nabla f_i(v)\|_2\le\beta\|u-v\|_2$ simultaneously for every $i\in\{1,\ldots,n\}$ and every pair $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad n \ge 1,\quad L > 0\\R > 0,\quad \beta \ge 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ n,\ \varepsilon,\ x_0$.

Public upper bounds: $L,\ \beta,\ R$.

The unknown objects are the component functions $f_1,\ldots,f_n$.

For each query, the algorithm chooses $i\in\{1,\ldots,n\}$ and $x\in\mathbb R^d$ and receives the following information about that component.

$$(f_i(x),\nabla f_i(x))$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=F(\widehat{x})-F^\star$$

$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One component value-gradient query costs one call; queries may lie anywhere in the full space.

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

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f_i,F$: Unknown components and finite-maximum objective **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\max_{1\le i\le n}f_i(x)$$

$\nabla f_i$: Full gradient of differentiable component $i$

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$n$: Public number of components in the finite sum or finite maximum. **Domain:** $n\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the Lipschitz constant of the objective or components. **Domain:** $L>0$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta\ge0$.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$A_\varepsilon$: Dimensionless quantity $LR/\epsilon$, used only to shorten formulas.

$$A_\varepsilon=\frac{L\,R}{\varepsilon}$$

$B_\varepsilon$: Dimensionless quantity $\beta R^2/\epsilon$; not an independent parameter.

$$B_\varepsilon=\frac{\beta\,{R}^{2}}{\varepsilon}$$

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One component value-gradient query costs one call; queries may lie anywhere in the full space.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Nontrivial suboptimality

**Region.** $0<\varepsilon\le cLR$

**Quantity.** Q1

**Resource.** One component value-gradient query costs one call; queries may lie anywhere in the full space.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
\widetilde{O}(nA_\varepsilon^{2/3}+\sqrt n[A_\varepsilon+\sqrt{B_\varepsilon}])
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $$0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\varepsilon\le cLR$

**Oracle mapping.** Applicable interfaces: selected component values and gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee mapping.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - 2021 full-space ball acceleration

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}(nA_\varepsilon^{2/3}+\sqrt n[A_\varepsilon+\sqrt{B_\varepsilon}])
$$

**Sources.** [1](https://arxiv.org/pdf/2105.01778)

**Source location.** [1](https://arxiv.org/pdf/2105.01778) theorem: Theorem2 Eq.(9); PDF p.9

## References

[1] Yair Carmon, Arun Jambulapati, Yujia Jin and Aaron Sidford. Thinking Inside the Ball: Near-Optimal Minimization of the Maximal Loss. COLT 2021, full arXiv version; Theorem 2 and Eq.(9), p.9; Theorem 3 and Eq.(13), p.12; Appendices A.3 and D.3.

https://arxiv.org/pdf/2105.01778
