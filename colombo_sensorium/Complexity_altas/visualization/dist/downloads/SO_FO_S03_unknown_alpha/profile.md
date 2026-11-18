# Stochastic nonconvex stationarity: unknown tail exponent and a common budget-indexed algorithm; stochastic full gradients

**Setting ID.** `SO_FO_S03_unknown_alpha`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Polynomial gap present

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz gradient; stochastic model: Centered alpha moment noise; structure: Unknown tail index

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic gradient; operation: Stochastic gradient; public information: Hidden objects explicitly declared; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Samples; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

The unknown function $f:\mathbb R^d\to\mathbb R$ is globally $\beta$-smooth and satisfies $f(x_0)-\inf f\le\Delta$. Convexity and a bounded query radius are not assumed. The centered noise has $\alpha$th moment at most $\sigma^\alpha$, but none of $\alpha,\beta,\Delta,\sigma$ is an algorithm input. The same budget-indexed algorithm $A_N$ must work for every fixed $\alpha$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad N\in\mathbb{N}_{\ge2},\quad r_0>0,\quad\beta>0,\quad\Delta>0,\quad\sigma\ge0,\quad1<\alpha\le2$$

### Oracle interface

Public numerical inputs: $d,\ N,\ r_0,\ x_0$.

The algorithm receives only $d,N,r_0,x_0$. The quantities $\alpha,\beta,\Delta,\sigma$ are hidden, and a common algorithm family cannot depend on them.

Query points lie in $\mathbb{R}^d$; feedback consists of stochastic full gradients:

$$\mathbb{E}_tG_t=\nabla f(x_t),\quad\mathbb{E}_t\|G_t-\nabla f(x_t)\|^\alpha\le\sigma^\alpha$$

Every observation is fresh. Same-point batches are conditionally independent, and the conditional moment bounds hold uniformly over histories. Samples cannot be reused across points.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=\|\nabla f(\widehat{x})\|_2$$

The comparison concerns the specified gradient-norm risk. Expected norm and expected squared norm are distinct performance requirements.

### Resource accounting

Prespecified integer $N$ bounds the total number of gradient samples on every execution path. Samples used for validation, grid evaluation, and candidate selection all count toward $N$.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Choose a common algorithm family $(A_N)_{N\ge2}$, where $A_N$ depends only on the public inputs $d,N,r_0,x_0$. For each fixed $1<\alpha\le2$ and each admissible choice of hidden scales, compare its worst-case expected residual over the corresponding instance class:

$$\mathcal{R}_N(A;\alpha,\beta,\Delta,\sigma)=\sup_{I,\mathcal{O}}\mathbb{E}\|\nabla f(A_N^{\mathcal{O}})\|_2$$

Fix the instance and response law, then take expectation over observations and private randomization, and finally the supremum over instances. The bounds compare budget-dependent risk directly; they do not presume that the algorithm can invert hidden parameters to choose a stopping budget.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f$: Unknown objective, with domain and structure specified by the model

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$G_t$: $t$th full stochastic gradient or subgradient observation

$\mathbb{E}_t$: Conditional expectation given the previous history and current query; the query is selected before the fresh observation is drawn

$A_N$: Common algorithm with budget $N$; the hidden tail exponent and scales are not inputs

$\mathcal{R}_N$: Worst expected gradient-norm risk over the class with fixed hidden parameters, as defined by the success contract

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Hidden upper bound on population-gradient Lipschitz continuity, used for classwise evaluation **Domain:** $\beta>0$.

$\Delta$: Hidden upper bound on initial suboptimality, used for classwise evaluation **Domain:** $\Delta>0$.

$\sigma$: Hidden centered-noise moment scale, used for classwise evaluation **Domain:** $\sigma\ge0$.

$\alpha$: Hidden centered-noise moment exponent; not an input to the common algorithm **Domain:** $1<\alpha\le2$.

$N$: Prespecified integer query budget for the budget-to-risk curve. **Domain:** $N\in\mathbb{N}_{\ge2}$.

$r_0$: Public length unit selected in advance; it is not a bound on distance to a minimizer. **Domain:** $r_0>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$c_\alpha$: Positive multiplicative constant depending only on the fixed $\alpha$; uniform boundedness as $\alpha\downarrow1$ is not asserted. **Domain:** $0<c_\alpha<\infty$.

$C_\alpha$: Positive multiplicative constant depending only on the fixed $\alpha$; uniform boundedness as $\alpha\downarrow1$ is not asserted. **Domain:** $0<C_\alpha<\infty$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

## 3. Complexity bracket

### Compared quantities

#### Q1 - fixed budget risk

$$
R^\star_{v,\pi}(B;\theta)=\inf_{\mathcal A\in\mathfrak A_v:\ C_\pi(\mathcal A,I)\le B\ \forall I}\sup_I\mathbb E[\ell(I,\mathcal A)]
$$

**Definition.** Error risk under the prescribed fixed budget

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Finite-variance slice $\alpha=2$ of the unknown-parameter model

**Region.** $\alpha=2,\quad\theta\in\Theta_{\rm normalized}$

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Optimal

**Lower bound.** B2

$$
cN^{-1/4}
$$

**Upper bound.** B1

$$
C N^{-1/4}
$$

**Gap or comparison.** $O(1)$

### R2 - Heavy-tailed slice of the unknown-parameter model

**Region.** $1<\alpha<2,\quad\theta\in\Theta_{\rm normalized}$

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Polynomial gap

**Lower bound.** B2

$$
c_\alpha N^{-(\alpha-1)/(3\alpha-2)}
$$

**Upper bound.** B1

$$
C_\alpha N^{-(\alpha-1)/(2\alpha)}
$$

**Gap or comparison.** $O_\alpha(N^{(\alpha-1)(2-\alpha)/(2\alpha(3\alpha-2))})$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Guarantee mapping.** Compare worst expected gradient-norm risk within the common-budget algorithm class. The tail index and hidden scales are not algorithm inputs. A class-dependent risk rate does not itself give an executable stopping rule.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Risk under a common budget for batched NSGDM

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_N\le C[(\Delta/r_0+\beta r_0)N^{-1/4}+\sigma N^{-(\alpha-1)/(2\alpha)}]
$$

**Sources.** [2](https://arxiv.org/pdf/2412.19529)

**Conditions.** $$N\ge2,\quad1<\alpha\le2,\quad r_0>0$$

**Dimension conditions.** $N\ge2,\quad1<\alpha\le2,\quad r_0>0$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Source location.** [2](https://arxiv.org/pdf/2412.19529) theorem: Theorem3.6; §3.2, PDF pp.5–6; arXivv4; rescale h(z)=f(r₀z)

### B2 - Classwise risk lower bound that also applies when $\alpha$ is known

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_N\ge c_\alpha N^{-(\alpha-1)/(3\alpha-2)}
$$

**Sources.** [1](https://proceedings.mlr.press/v313/liu26a.html)

**Conditions.** $$\beta=\Delta=\sigma=r_0=1,\quad N\ge2,\ d\ge d_{\rm ALT}(N,\alpha)$$

**Dimension conditions.** $\beta=\Delta=\sigma=r_0=1,\quad N\ge2,\ d\ge d_{\rm ALT}(N,\alpha)$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Source location.** [1](https://proceedings.mlr.press/v313/liu26a.html) theorem: Final ALT2026 Theorem 10 and Remark 13; PDF pp.44–46

## References

[1] Zijian Liu. Online Convex Optimization with Heavy Tails: Old Algorithms, New Regrets, and Applications. 2026; ALT 2026, PMLR 313:1–47; final published PDF Theorem 10 and Remark 13, pp.44–46. PDF: https://raw.githubusercontent.com/mlresearch/v313/main/assets/liu26a/liu26a.pdf; earlier author version Theorem 11 and Remark 10, pp.35–36.

https://proceedings.mlr.press/v313/liu26a.html

[2] Zijian Liu and Zhengyuan Zhou. Nonconvex Stochastic Optimization under Heavy-Tailed Noises: Optimal Convergence without Gradient Clipping. 2025; ICLR 2025; arXiv v4, 29 May 2025; Theorems 3.2–3.3.

https://arxiv.org/pdf/2412.19529
