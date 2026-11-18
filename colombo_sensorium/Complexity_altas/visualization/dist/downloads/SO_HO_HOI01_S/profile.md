# Convex minimization with exact gradients and approximate Hessians

**Setting ID.** `SO_HO_HOI01_S`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: Higher-order interface; feedback quality: Inexact; interface family: Inexact hessian; operation: Inexact hessian; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is convex and $C^2$.

$$\|D^{2}f(x)-D^{2}f(y)\|_{\mathrm{op},2}\le M_2\|x-y\|_{2}.$$

There exists a global minimizer $x^*$ satisfying $\|x^*-x_0\|_2\le R$.

No uniform gradient smoothness budget is supplied.

Admissible parameter domain:

$$d\ge1,\ R,M_2,\varepsilon_f>0,\ \eta_2\ge0$$

### Oracle interface

A query at any $x\in\mathbb{R}^d$ returns $(f(x),\nabla f(x),H(x))$. The first two entries are exact, and $H(x)$ is symmetric with $\|H(x)-\nabla^2f(x)\|_{\mathrm{op}}\le\eta_2$. The approximation error may depend on previous queries and responses; neither unbiasedness nor independence is assumed.

The public inputs are $x_0$, the target accuracy, and $d$, $\varepsilon_f$, $R$, $M_2$, $\eta_2$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=f(\widehat{x})-f^*.$$

Here $f^*=\inf_{x\in \mathbb{R}^d}f(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

### Resource accounting

Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

#### Deterministic

Arbitrary measurable adaptive deterministic algorithms are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$f(\widehat{x})-f^*\le \varepsilon_f.$$

The running-cost guarantee is specified separately under RESOURCE.

#### Randomized

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[f(\widehat{x})-f^*\le \varepsilon_f\right]\ge\frac23.$$

Expectation or probability is evaluated after fixing the instance; randomness comes from the algorithm's private random seed.

The running-cost guarantee is specified separately under RESOURCE.

## 2. Notation and parameters

$x,\widehat{x},x_0$: Query or decision point, algorithm output, and public initial point. **Domain:** $\mathbb{R}^d$.

$\mathbb{R}^d$: Real coordinate space; vectors use the Euclidean norm unless otherwise stated. **Domain:** $d$ is a positive integer.

$\langle u,v\rangle,\ \|u\|_2$: Euclidean inner product and norm.

$$\langle u,v\rangle=u^\top v,\qquad\|u\|_2=\sqrt{\langle u,u\rangle}.$$

$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,2\}$ and $D^0f=f$.

$\|T\|_{\mathrm{op}},\ \|T\|_{\mathrm{op},2}$: Induced operator norm of a Euclidean multilinear tensor; the spectral norm for matrices.

$$\|T\|_{\mathrm{op}}=\|T\|_{\mathrm{op},2}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|.$$

$\mathcal{E}$: Base error defined in the metric specification; expectation or probability aggregation is imposed by the guarantee.

$N$: Total number of original oracle calls; the unit cost is specified in the resource convention. **Domain:** $N\in\mathbb{Z}_{\ge0}$.

$T^*$: Minimum worst-case budget for one algorithm to meet the requirement on the full instance class, within the specified regime, guarantee and resource projection. Expected-resource specifications instead minimize the per-instance expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching bounds up to constants, and upper bounds omitting the declared logarithmic factors. **Domain:** Hidden constants, fixed parameters, and omitted logarithmic variables are specified for each bound.

$\inf,\sup,\min,\max$: Infimum, supremum, attained minimum and attained maximum.

$c,C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<c,C<\infty$.

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$g(x),H(x)$: Gradient vector and symmetric Hessian approximation supplied by the oracle; exactness and error bounds are specified separately for each channel.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\varepsilon_f$: Target accuracy **Domain:** $\varepsilon_f>0$.

$R$: Upper bound on the distance from the known initial point to at least one global minimizer. **Domain:** $R>0$.

$M_2$: Hessian Lipschitz bound **Domain:** $M_2>0$.

$\eta_2$: Spectral-norm error bound for the symmetric Hessian approximation **Domain:** $\eta_2\ge0$.

$A$: Approximation-error term **Domain:** $A=(\eta_2R^2/\varepsilon_f)^{1/2}$.

$$A=\sqrt{\frac{\eta_2\,(R)^{2}}{\varepsilon_f}}.$$

$B$: Exact second-order term **Domain:** $B=(M_2R^3/\varepsilon_f)^{2/7}$.

$$B=(\frac{M_2\,(R)^{3}}{\varepsilon_f})^{\frac{2}{7}}.$$

$C_{\rm dim}$: Sufficient dimension constant for the lower-bound construction; it depends only on the fixed parameters specified by that bound and is not numerically given. **Domain:** $C_{\rm dim}>0$.

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive response costs one call; all additional gradient queries at other points are also charged.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive response costs one call; all additional gradient queries at other points are also charged.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Principal regime in sufficiently high dimension

**Region.** $d\ge C_{\rm dim}(1+A+B)$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each primitive response costs one call; all additional gradient queries at other points are also charged.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(1+A+B)
$$

**Upper bound.** B1

$$
O(1+A+B)
$$

**Gap or comparison.** $O(1)$

### R2 - The approximation-error term dominates

**Region.** $\Theta_H\cap\{A\ge B\}$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each primitive response costs one call; all additional gradient queries at other points are also charged.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(1+A)
$$

**Upper bound.** B1

$$
O(1+A)
$$

**Gap or comparison.** $O(1)$

### R3 - The exact second-order term dominates

**Region.** $\Theta_H\cap\{B>A\}$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each primitive response costs one call; all additional gradient queries at other points are also charged.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(1+B)
$$

**Upper bound.** B1

$$
O(1+B)
$$

**Gap or comparison.** $O(1)$

### R4 - Main domain of regularity budgets

**Region.** $d\ge1,\ R,M_2,\varepsilon_f>0,\ \eta_2\ge0$

**Views.** Randomized

**Quantity.** Q2

**Resource.** Each primitive response costs one call; all additional gradient queries at other points are also charged.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

$$
O(1+A+B)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** A query at any $x\in\mathbb{R}^d$ returns $(f(x),\nabla f(x),H(x))$. The first two entries are exact, and $H(x)$ is symmetric with $\|H(x)-\nabla^2f(x)\|_{\mathrm{op}}\le\eta_2$. The approximation error may depend on previous queries and responses; neither unbiasedness nor independence is assumed.

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Approximate cubic models and acceleration without search

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
1+A+B
$$

**Sources.** [1](https://arxiv.org/abs/2607.24520v3)

**Conditions.** $d\ge1,\ R,M_2,\varepsilon_f>0,\ \eta_2\ge0$

**Dimension conditions.** $d\ge1,\ R,M_2,\varepsilon_f>0,\ \eta_2\ge0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1

**Source location.** [1](https://arxiv.org/abs/2607.24520v3) theorem: Corollary 3.1; Theorem 3.1 and Lemma 3.1; pdf pages: 7

### B2 - Exact high-order hard family and hidden-Hessian quadratic family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
1+A+B
$$

**Sources.** [1](https://arxiv.org/abs/2607.24520v3)

**Conditions.** $d\ge C_{\rm dim}(1+A+B)$

**Dimension conditions.** $d\ge C_{\rm dim}(1+A+B)$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1

**Source location.** [1](https://arxiv.org/abs/2607.24520v3) theorem: Definition 5.1; Proposition 5.1; Appendix J; pdf pages: 11

### B3 - Approximate cubic models and acceleration without search

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
1+A+B
$$

**Sources.** [1](https://arxiv.org/abs/2607.24520v3)

**Conditions.** $d\ge1,\ R,M_2,\varepsilon_f>0,\ \eta_2\ge0$

**Dimension conditions.** $d\ge1,\ R,M_2,\varepsilon_f>0,\ \eta_2\ge0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1

**Source location.** [1](https://arxiv.org/abs/2607.24520v3) theorem: Corollary 3.1; Theorem 3.1 and Lemma 3.1; pdf pages: 7

## 5. Local arguments

### A1 - Two hard families for an approximate-Hessian interface

**Scope.** Exact function values and gradients, symmetric bounded-error Hessians, and the source lower-bound algorithm/dimension scope. Does not equate approximate-Hessian and exact-Hessian recovery.

**Algorithm scope.** Exact function values and gradients, symmetric bounded-error Hessians, and the source lower-bound algorithm/dimension scope. Does not equate approximate-Hessian and exact-Hessian recovery.

Convex objective accuracy with exact values and gradients but Hessian error $\eta_2$ has separate high-order and first-order lower contributions.

Chen et al., arXiv:2607.24520v3, Proposition 5.1 and Appendix J, use two admissible families. Exact-second-order hard instances give $cM_2R^3/T^{7/2}$. A quadratic family with gradient Lipschitz constant $\eta_2$ permits every approximate Hessian response to be zero, since the true Hessian has operator norm at most $\eta_2$. The remaining information is first order, yielding $c\eta_2R^2/T^2$. Worst-case risk is at least the maximum of these two quantities and hence at least half their sum. The sum does not require one instance to attain both terms simultaneously.

No quadratic-curvature upper bound is imposed by highest-order regularity alone. Therefore $M_2R^3$ is not an initial-gap upper bound. For $R>0$, two quadratics centered at $x_0\pm R e_1$ with sufficiently large common curvature have disjoint $\varepsilon_f$-success sets. Their zero-query transcripts coincide, excluding probability at least 2/3 on both and giving a one-call lower endpoint. If $R=0$, return $x_0$. If $M_2=\eta_2=0$, one complete response recovers the quadratic exactly. When $M_2=0$ but $\eta_2>0$, the true Hessian is not recovered by that response.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [1](https://arxiv.org/abs/2607.24520v3)

## References

[1] Lesi Chen, Chengchang Liu, Luo Luo, John C. S. Lui, Jingzhao Zhang. Optimal Convex Optimization with Inexact Second-Order Oracles. arXiv:2607.24520v3, 2026-07-31.

https://arxiv.org/abs/2607.24520v3
