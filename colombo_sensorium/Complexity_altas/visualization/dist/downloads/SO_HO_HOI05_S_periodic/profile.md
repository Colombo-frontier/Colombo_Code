# Convex minimization with delayed or weighted Hessian queries: a fixed refresh-period interface

**Setting ID.** `SO_HO_HOI05_S_periodic`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Lazy hessian; operation: Lazy hessian; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

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

$$d\ge1,\quad R,M_2,\varepsilon_f>0,\quad b\in\mathbb{N}_{\ge1}$$

### Oracle interface

Query $t$ chooses any point $x_t\in\mathbb{R}^d$ and always returns $\nabla f(x_t)$; the complete $\nabla^2f(x_t)$ is additionally returned exactly when $t\in\{b,2b,3b,\ldots\}$. The first Hessian appears on call $b$; no function-value channel is provided.

The public inputs are $x_0$, the target accuracy, and $d$, $\varepsilon_f$, $R$, $M_2$, $b$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=f(\widehat{x})-f^*.$$

Here $f^*=\inf_{x\in \mathbb{R}^d}f(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

### Resource accounting

Each periodic-interface reply costs one unit. Gradient queries made while waiting for the next Hessian slot also count toward the total.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive deterministic algorithms are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$f(\widehat{x})-f^*\le \varepsilon_f.$$

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

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\varepsilon_f$: Target accuracy **Domain:** $\varepsilon_f>0$.

$R$: Upper bound on the distance from the known initial point to at least one global minimizer. **Domain:** $R>0$.

$M_2$: Hessian Lipschitz bound **Domain:** $M_2>0$.

$b$: Refresh period; the first Hessian is delayed until call b **Domain:** $b\in\mathbb{N},\ b\ge1$.

$Q$: Ratio of regularity, localization radius, and accuracy defined below. **Domain:** $Q=M_2R^3/\varepsilon_f$.

$$Q=\frac{M_2\,(R)^{3}}{\varepsilon_f}.$$

$C$: Sufficient dimension constant for the lower-bound construction; it depends only on the fixed parameters specified by that bound and is not numerically given. **Domain:** $C>0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each response of the periodic interface costs one call; gradient queries used while waiting for a Hessian slot are also charged.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Periodic-interface regime in sufficiently high dimension

**Region.** $d\ge C[b+b^{1/7}Q^{2/7}]$

**Quantity.** Q1

**Resource.** Each response of the periodic interface costs one call; gradient queries used while waiting for a Hessian slot are also charged.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(b+b^{1/7}Q^{2/7})
$$

**Upper bound.** B1

$$
O((b+b^{1/7}Q^{2/7})[\log(eb)]^{11/3})
$$

**Gap or comparison.** $O([\log(eb)]^{11/3})$

### R2 - The initialization term dominates

**Region.** $\Theta_H\cap\{Q\le b^3\}$

**Quantity.** Q1

**Resource.** Each response of the periodic interface costs one call; gradient queries used while waiting for a Hessian slot are also charged.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(b)
$$

**Upper bound.** B1

$$
O(b[\log(eb)]^{11/3})
$$

**Gap or comparison.** $O([\log(eb)]^{11/3})$

### R3 - The accuracy term dominates

**Region.** $\Theta_H\cap\{Q>b^3\}$

**Quantity.** Q1

**Resource.** Each response of the periodic interface costs one call; gradient queries used while waiting for a Hessian slot are also charged.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(b^{1/7}Q^{2/7})
$$

**Upper bound.** B1

$$
O(b^{1/7}Q^{2/7}[\log(eb)]^{11/3})
$$

**Gap or comparison.** $O([\log(eb)]^{11/3})$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Query $t$ chooses any point $x_t\in\mathbb{R}^d$ and always returns $\nabla f(x_t)$; the complete $\nabla^2f(x_t)$ is additionally returned exactly when $t\in\{b,2b,3b,\ldots\}$. The first Hessian appears on call $b$; no function-value channel is provided.

**Guarantee mapping.** Deterministic-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each periodic-interface reply costs one unit. Gradient queries made while waiting for the next Hessian slot also count toward the total.

### B1 - Accelerated upper bound for the periodic interface

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
(b+b^{1/7}Q^{2/7})[\log(eb)]^{11/3}
$$

**Sources.** [1](https://arxiv.org/abs/2610.03222v1)

**Conditions.** $d\ge1,\quad R,M_2,\varepsilon_f>0,\quad b\in\mathbb{N}_{\ge1}$

**Dimension conditions.** $d\ge1,\ b\ge1,\ w\ge1,\ R,M_2,c_g,\varepsilon_f>0$

**Source location.** [1](https://arxiv.org/abs/2610.03222v1) theorem: Theorem 4.1; eq. (10); proof pp. 13–14; pdf pages: 5

### B2 - Block zero-chain and quadratic initialization

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
b+b^{1/7}Q^{2/7}
$$

**Sources.** [1](https://arxiv.org/abs/2610.03222v1)

**Conditions.** $d\ge C[b+b^{1/7}Q^{2/7}]$

**Dimension conditions.** $d\ge C[b+b^{1/7}Q^{2/7}]$

**Source location.** [1](https://arxiv.org/abs/2610.03222v1) theorem: Definition 3.1; Lemmas 3.1–3.2; Theorem 3.1 and following quadratic argument; pdf pages: 4

## References

[1] Xinliang Zhang, Lesi Chen, Chengchang Liu, Jingzhao Zhang. Near-Optimal Convex Optimization with Lazy Second-Order Oracles. arXiv:2610.03222v1, 2026-10-02.

https://arxiv.org/abs/2610.03222v1
