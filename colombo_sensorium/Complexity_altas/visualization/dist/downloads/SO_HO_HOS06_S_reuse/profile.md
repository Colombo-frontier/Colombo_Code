# Stochastic nonconvex second-order stationarity with persistently reusable samples: joint derivative budgets

**Setting ID.** `SO_HO_HOS06_S_reuse`

Single-objective optimization

Find an approximate second-order stationary point of the full objective:

**Status.** Polynomial gap present; Bounds missing; Joint budget unresolved

**Gap classes present.** Polynomial gap; Logarithmic gap

**TASK tags.** formulation: Second order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Samplewise hessian lipschitz; smoothness: Samplewise smooth; structure: Expectation common loss

**ORACLE tags.** access order: Higher-order interface; feedback quality: Stochastic; interface family: Reusable gradient or full hessian; operation: Reusable gradient or full hessian; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Second order stationarity; criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Probability; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Joint resource budget; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate second-order stationary point of the full objective:

$$\|\nabla f(\widehat{x})\|_2\le\varepsilon_g,\qquad\nabla^2f(\widehat{x})\succeq-\varepsilon_H I_d.$$

### Admissible model

The population objective $f(x)=\mathbb{E}_Z[\ell(x;Z)]$ is bounded below.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

On a common probability-one event, all sample gradients are $\beta$-Lipschitz and all sample Hessians are $M_2$-Lipschitz at every point. Differentiation and expectation may be interchanged.

Sample errors satisfy $\|\nabla\ell(x;Z)-\nabla f(x)\|_2\le\sigma_1$ and $\|\nabla^2\ell(x;Z)-\nabla^2f(x)\|_{\mathrm{op}}\le\sigma_2$, with $\sup_x\|\nabla f(x)\|_2\le G$.

### Oracle interface

An opaque persistent handle $a$ can be requested for free without revealing sample data. Distinct new handles bind independent samples $Z_a$. At each call, choose an existing handle and any point $(a,x)$, then request the full $\nabla\ell(x;Z_a)$ or full $\nabla^2\ell(x;Z_a)$, charged separately. A handle may be reused at arbitrarily many points.

No sample value, internal sample data or third derivative is returned. An observed full matrix may be used freely in internal linear algebra.

The public inputs are $x_0$, the target accuracy, and $d$, $\Delta$, $\beta$, $M_2$, $\sigma_1$, $\sigma_2$, $G$, $\varepsilon_g$, $\varepsilon_H$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

The algorithm may output the failure symbol $\bot$; this event counts toward the failure probability.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\max\left\{\frac{\|\nabla f(\widehat{x})\|_2}{\varepsilon_g},\frac{[-\lambda_{\min}(\nabla^2f(\widehat{x}))]_+}{\varepsilon_H}\right\}.$$

$[a]_+=\max\{a,0\}$, and $\lambda_{\min}$ denotes the smallest eigenvalue of a symmetric matrix. The target is $\mathcal{E}(\widehat{x})\le1$, where $\varepsilon_g$ and $\varepsilon_H$ are independent positive tolerances.

### Resource accounting

The native cost is the joint resource vector $(N_g,N_H)$, counting full sample gradients and full sample Hessians separately. Requesting both derivatives at one point costs two calls, as does evaluating the same handle at two points for a difference.

The total-cost projection is explicitly $N_g+N_H$. Separate budgets for $N_g$ and $N_H$ may also be displayed, but displaying one coordinate does not make the other operation free. All coordinatewise upper bounds must be attained by the same algorithm.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[\max\left\{\frac{\|\nabla f(\widehat{x})\|_2}{\varepsilon_g},\frac{[-\lambda_{\min}(\nabla^2f(\widehat{x}))]_+}{\varepsilon_H}\right\}\le 1\right]\ge\frac23.$$

Expectation or probability is evaluated after fixing the instance; randomness comes from the algorithm's private seed and oracle sampling.

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

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$Z,\ell(x;Z)$: Sample random variable and the associated scalar sample loss.

$$f(x)=\mathbb{E}_Z\ell(x;Z).$$

$a,Z_a$: Opaque persistent handle and its associated hidden sample.

$N_g,N_H$: Numbers of full sample-gradient and full sample-Hessian evaluations. **Domain:** $N_g,N_H\in\mathbb{Z}_{\ge0}$.

$\bot$: Output symbol explicitly declaring algorithmic failure.

$u\preceq v$: Coordinatewise order for resource vectors; the same symbol for symmetric matrices denotes the positive semidefinite order.

$$u\preceq v\iff u_i\le v_i\quad\text{for every }i.$$

$\lambda_{\min}(A),[z]_+$: The smallest eigenvalue of a symmetric matrix and the positive part of a scalar.

$$[z]_+=\max\{z,0\}.$$

$I_d$: The identity matrix in dimension $d$.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge 1}$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$\beta$: Common Lipschitz upper bound for the gradients of all sample losses. **Domain:** $\beta>0$.

$M_2$: Common Lipschitz upper bound for the Hessians of all sample losses. **Domain:** $M_2>0$.

$\sigma_1$: Almost-sure bound on the sample gradient's deviation from the population gradient. **Domain:** $\sigma_1>0$.

$\sigma_2$: Almost-sure operator-norm bound on the sample Hessian's deviation from the population Hessian. **Domain:** $\sigma_2>0$.

$G$: Global upper bound on the population gradient norm **Domain:** $G>0$.

$\varepsilon_g$: Gradient tolerance **Domain:** $\varepsilon_g>0$.

$\varepsilon_H$: Curvature tolerance **Domain:** $\varepsilon_H>0$.

$\theta$: Fixed group of positive model bounds.

$$\theta=(\Delta,\beta,M_2,\sigma_1,\sigma_2,G).$$

$B_g$: Dimensionless leading term in one algorithm's gradient-evaluation budget.

$$B_g=1+\frac{\Delta\beta+\sigma_1^2}{\varepsilon_g^2}+\frac{\sigma_1\beta\Delta}{\varepsilon_g^3}+\frac{\beta^2\Delta}{\varepsilon_g^2\varepsilon_H}.$$

$B_H$: Dimensionless leading term in one algorithm's Hessian-evaluation budget.

$$B_H=1+\frac{\Delta\beta}{\varepsilon_g^2}+\frac{\sigma_2^2}{\varepsilon_H^2}+\frac{\sigma_2M_2\Delta}{\varepsilon_g\varepsilon_H^2}+\frac{2M_2^2\Delta}{\varepsilon_H^3}.$$

$T,\Lambda$: Iteration cap and shared logarithmic factor.

$$T=\left\lceil1+48\Delta\left(\frac{32\beta}{3\varepsilon_g^2}+\frac{12M_2^2}{\varepsilon_H^3}\right)\right\rceil,\quad\Lambda=1+\log[C(d+1)(T+1)].$$

$s_*$: Positive scale used in the lower-bound construction.

$$s_*=\min\{1,\sigma_1,\sigma_2,\beta,M_2,G\}.$$

$D_g$: Logarithmic dimension factor in the persistent-handle gradient hard construction.

$$D_g=C\log(2+\Delta/\varepsilon_g+\Delta s_*^2/\varepsilon_g^3).$$

$d_*$: Sufficient dimension threshold for the lower-bound construction; an existential constant function, not a supplied numerical value.

$$d_*\le C(\theta)\left[1+\frac{\Delta D_g^{3/4}}{\varepsilon_g}+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}\right].$$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Declared total number of calls $N_g+N_H$

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Number of gradient calls $N_g$

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Number of Hessian calls $N_H$

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - achievable resource region

$$
\mathcal B_v(\varepsilon;\theta)=\{b\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_j(\mathcal A,I)\le b_j\ \forall j,I,\quad G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Joint resource vector

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - High-dimensional fixed-scale window

**Region.** $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$

**Quantity.** Q1

**Resource.** Declared total number of calls $N_g+N_H$

**Status.** Logarithmic gap

**Lower bound.** B4, B7

$$
\max\{L_{old}\text{ on }r3,L_g\text{ on }r3\cap r7\}
$$

**Upper bound.** B3, B12

$$
\min\{C\Lambda^4(B_g+B_H),C_{gf}\}
$$

**Gap or comparison.**

$$
\min\{U_{old},C_{gf}\}/\max\{L_{old},L_g\text{ when }r7\}
$$

### R2 - Scope of the upper bound

**Region.** $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Quantity.** Q2

**Resource.** Number of gradient calls $N_g$

**Status.** Lower bound missing

**Lower bound.** B6

$$
\frac{\sigma_1^2}{288\varepsilon_g^2}\quad\text{on }r7;\quad\text{no registered lower bound outside }r7
$$

**Upper bound.** B1, B13

$$
\min\{C\Lambda^4B_g,C_{gf}\}
$$

**Gap or comparison.**

$$
\min\{C\Lambda^4B_g,C_{gf}\}/L_g\quad\text{only on }r7
$$

### R3 - Scope of the upper bound

**Region.** $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Quantity.** Q3

**Resource.** Number of Hessian calls $N_H$

**Status.** Optimal

**Lower bound.** B10

$$
0
$$

**Upper bound.** B9

$$
0
$$

**Gap or comparison.** Not applicable: the Hessian-call coordinate is exactly zero, with a finite positive gradient budget supplied by the same algorithm.

### R4 - Scope of the upper bound

**Region.** $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Quantity.** Q4

**Resource.** Joint resource vector

**Status.** Joint budget unresolved

**Achievable budgets.** B5, B11

**Necessary constraints.** B8, B14

### R5 - Total-cost necessary floor on the full r7 marginal-information window

**Region.** Native r7 (all positive structural budgets,d>=1,epsilon_H<=1,epsilon_g<=min{1,sigma1/8,beta/4,M2/12,G/6,Delta/(4-2sqrt(3))}).

**Quantity.** Q1

**Resource.** Declared total number of calls $N_g+N_H$

**Status.** Polynomial gap

**Lower bound.** B7, B4

$$
\max\{L_g,L_{old}\text{ when }r3\}
$$

**Upper bound.** B3, B12

$$
\min\{U_{old},C_{gf}\}
$$

**Gap or comparison.**

$$
\min\{U_{old},C_{gf}\}/\max\{L_g,L_{old}\text{ when }r3\};\text{ no sharp gap claim}
$$

## 4. Bounds and supporting evidence

### B1 - Curvature-first steps and binary-ancestor gradient estimation

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N_g\le C\Lambda^4 B_g
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16832v2)

**Conditions.** $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Dimension conditions.** $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Oracle correspondence.** An opaque persistent handle $a$ can be requested for free without revealing sample data. Distinct new handles bind independent samples $Z_a$. At each call, choose an existing handle and any point $(a,x)$, then request the full $\nabla\ell(x;Z_a)$ or full $\nabla^2\ell(x;Z_a)$, charged separately. A handle may be reused at arbitrarily many points.

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** The native cost is the joint resource vector $(N_g,N_H)$, counting full sample gradients and full sample Hessians separately. Requesting both derivatives at one point costs two calls, as does evaluating the same handle at two points for a difference.

**Source location.** [1](https://arxiv.org/pdf/2610.16832v2) pdf pages: 8; theorem: Theorem 4.1, eqs.(4.1),(4.3)

### B2 - Difference-tree estimation of same-sample Hessians

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N_H\le C\Lambda^4 B_H
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16832v2)

**Conditions.** $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Dimension conditions.** $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Oracle correspondence.** An opaque persistent handle $a$ can be requested for free without revealing sample data. Distinct new handles bind independent samples $Z_a$. At each call, choose an existing handle and any point $(a,x)$, then request the full $\nabla\ell(x;Z_a)$ or full $\nabla^2\ell(x;Z_a)$, charged separately. A handle may be reused at arbitrarily many points.

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** The native cost is the joint resource vector $(N_g,N_H)$, counting full sample gradients and full sample Hessians separately. Requesting both derivatives at one point costs two calls, as does evaluating the same handle at two points for a difference.

**Source location.** [1](https://arxiv.org/pdf/2610.16832v2) pdf pages: 8; theorem: Theorem 4.1, eqs.(4.2),(4.4)

### B3 - Sum projection of one algorithm's joint derivative budget

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N_g+N_H\le C\Lambda^4(B_g+B_H)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16832v2)

**Conditions.** $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Dimension conditions.** $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Oracle correspondence.** An opaque persistent handle $a$ can be requested for free without revealing sample data. Distinct new handles bind independent samples $Z_a$. At each call, choose an existing handle and any point $(a,x)$, then request the full $\nabla\ell(x;Z_a)$ or full $\nabla^2\ell(x;Z_a)$, charged separately. A handle may be reused at arbitrarily many points.

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** The native cost is the joint resource vector $(N_g,N_H)$, counting full sample gradients and full sample Hessians separately. Requesting both derivatives at one point costs two calls, as does evaluating the same handle at two points for a difference.

**Source location.** [1](https://arxiv.org/pdf/2610.16832v2) pdf pages: 8; theorem: Theorem 4.1; Corollary 1

### B4 - Persistent-handle relative-entropy lower bound and a deterministic negative-curvature chain

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c(\theta)\max\{\Delta s_*^2/(\varepsilon_g^3D_g^{1/4}),\varepsilon_H^{-3}\}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16832v2)

**Conditions.** $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$

**Dimension conditions.** $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$

**Oracle correspondence.** An opaque persistent handle $a$ can be requested for free without revealing sample data. Distinct new handles bind independent samples $Z_a$. At each call, choose an existing handle and any point $(a,x)$, then request the full $\nabla\ell(x;Z_a)$ or full $\nabla^2\ell(x;Z_a)$, charged separately. A handle may be reused at arbitrarily many points.

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** The native cost is the joint resource vector $(N_g,N_H)$, counting full sample gradients and full sample Hessians separately. Requesting both derivatives at one point costs two calls, as does evaluating the same handle at two points for a difference.

**Source location.** [1](https://arxiv.org/pdf/2610.16832v2) pdf pages: 9; theorem: Theorem 4.2, eq.(4.5); Sections 6.1-6.3

### B5 - Curvature-priority steps and binary-ancestor derivative estimation within one algorithm

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Randomized witness

$$
(N_g,N_H)\preceq(C\Lambda^4 B_g,C\Lambda^4 B_H)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16832v2)

**Conditions.** $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Dimension conditions.** $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Oracle correspondence.** An opaque persistent handle $a$ can be requested for free without revealing sample data. Distinct new handles bind independent samples $Z_a$. At each call, choose an existing handle and any point $(a,x)$, then request the full $\nabla\ell(x;Z_a)$ or full $\nabla^2\ell(x;Z_a)$, charged separately. A handle may be reused at arbitrarily many points.

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** The native cost is the joint resource vector $(N_g,N_H)$, counting full sample gradients and full sample Hessians separately. Requesting both derivatives at one point costs two calls, as does evaluating the same handle at two points for a difference.

**Source location.** [1](https://arxiv.org/pdf/2610.16832v2) pdf pages: 8; theorem: Theorem 4.1, eqs.(4.1),(4.3)

**Source location.** [1](https://arxiv.org/pdf/2610.16832v2) pdf pages: 8; theorem: Theorem 4.1, eqs.(4.2),(4.4)

**Source location.** [1](https://arxiv.org/pdf/2610.16832v2) pdf pages: 8; theorem: Theorem 4.1; Corollary 1

### B6 - Two-hypothesis marginal gradient information bound, robust to arbitrary persistent reuse and Hessian access

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N_g\ge\frac{\sigma_1^2}{288\varepsilon_g^2}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16832v2)

**Conditions.** r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive

**Dimension conditions.** Every integer d>=1, by flat-coordinate embedding.

**Oracle correspondence.** Exactly the fixed opaque persistent sample-handle interface. Each new informative handle contributes at most one Bernoulli observation; any Hessian query is hypothesis-independent.

**Guarantee conversion.** Per-instance success probability >=2/3 for simultaneous gradient and curvature tests; the hard populations are convex, so curvature is automatic.

**Output rule.** Arbitrary output points are allowed. Their first-coordinate sign must distinguish the hypotheses on successful executions.

**Resource conversion.** Lower bound on worst-case N_g with no restriction on how many Hessian calls an algorithm's finite joint cap permits. It does not make Hessian calls free in the native resource vector.

**Local argument.** SO_HO_HOS06_S_reuse__main__p1

**Source location.** [1](https://arxiv.org/pdf/2610.16832v2) pdf pages: 28; printed pages: 28; theorem: Appendix C, A Marginal Gradient Lower Bound; arXiv:2610.16832v2 (2026-10-19), extracted characters 66046-67739

Full Appendix C independently read through source_read. Explicit threshold, constant, initial-point translation and arbitrary-dimension embedding are proved in SO_HO_HOS06_S_reuse__main__p1.

### B7 - Guard-preserving directed sum-cost lower projection Ng+NH>=Ng>=Lg.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N_g+N_H\ge L_g:=\sigma_1^2/(288\varepsilon_g^2)
$$

**Conditions.** Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive

**Dimension conditions.** The same all-finite-integer-d>=1 scope already proved for b6 on r7 is retained. This algebra adds no dimension extension or new hard-family embedding.

**Oracle correspondence.** Keep precisely the same persistent gradient/Hessian calls of the same algorithm; no response is simulated, no new oracle is granted and no cost channel is renamed. The retained b6 information proof remains the premise, rather than a new source theorem.

**Guarantee conversion.** Retain b6 for every algorithm meeting the unchanged simultaneous population SOS guarantee with per-instance probability>=2/3. Arbitrary finite Hessian caps are permitted as in b6; this projection changes no algorithm/instance/guarantee class.

**Output rule.** The original output point and success tests are unchanged. No general-target sign-discrimination output requirement is added; any hard-family sign argument belongs only to the retained proof of b6.

**Resource conversion.** For each pathNg+NH>=Ng becauseNH>=0. A successful algorithm with a total worst-path cap would in particular have Ng at most that cap; b6 therefore forces totalcap>=Lg on r7.

**Local argument.** HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

### B8 - Guard-preserving directed joint-cap necessary projection Bg>=Lg from the robust marginal Ng lower.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal B\subseteq\{(B_g,B_H)\ge0:B_g\ge L_g\}
$$

**Conditions.** Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive

**Dimension conditions.** The same all-finite-integer-d>=1 scope already proved for b6 on r7 is retained. This algebra adds no dimension extension or new hard-family embedding.

**Oracle correspondence.** Keep precisely the same persistent gradient/Hessian calls of the same algorithm; no response is simulated, no new oracle is granted and no cost channel is renamed. The retained b6 information proof remains the premise, rather than a new source theorem.

**Guarantee conversion.** Retain b6 for every algorithm meeting the unchanged simultaneous population SOS guarantee with per-instance probability>=2/3. Arbitrary finite Hessian caps are permitted as in b6; this projection changes no algorithm/instance/guarantee class.

**Output rule.** The original output point and success tests are unchanged. No general-target sign-discrimination output requirement is added; any hard-family sign argument belongs only to the retained proof of b6.

**Resource conversion.** Any successful same-algorithm joint cap(Bg,BH) boundsNg byBg on everypath; robust b6 forcesBg>=Lg on r7, regardless of its finiteBH. This is necessary only, not a sufficient vector or marginal-minimum identity.

**Local argument.** HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

### B9 - Finite capped gradient means and same-handle central-gradient-difference matrices, proving zero Hessian-oracle cost.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N_H=0
$$

**Conditions.** Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.

**Dimension conditions.** Every fixed finite integer d>=1. The explicit Cgf=K(mg+2d*mH) is finite and displays its dimension dependence; no high-dimensional threshold or embedding argument is used.

**Oracle correspondence.** Only full sample-gradient calls are requested. At an iteration, mg independent fresh handles estimate the mean gradient; another mH fresh independent handles each supply all2d central-difference gradients at x+/-h*e_j using that same handle. No sample Hessian, value, comparison, hidden sample data or free validation oracle is used.

**Guarantee conversion.** The SAME explicitly capped algorithm returns a point satisfying BOTH population SOS conditions with probability>=2/3 for each instance, by conditional gradient/matrix estimation, a 2K union bound and descent; failed cap exhaustion returns bottom and counts as failure.

**Output rule.** Return the current arbitrary point x in R^d when the explicit gradient/curvature tests pass, or bottom on cap exhaustion; no first-coordinate sign restriction or external certificate is imposed.

**Resource conversion.** All gradient estimates,2d differences per sample matrix, initialization and stopping are included in worst-path Ng<=Cgf=K(mg+2d*mH),NH=0. Linear algebra/eigendecomposition is internal arithmetic allowed by the frozen model. No independently optimized marginal budgets are paired. This q3 bound concerns Hessian calls only; gradient calls are finite but not free.

**Local argument.** HOS06_GRADIENT_ONLY_SOSP_20261116

### B10 - Nonnegativity of the native Hessian-call count and cap; no hard instance or oracle response needed.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N_H>=0
$$

**Conditions.** Unchanged target r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$

**Dimension conditions.** Every legal finite integerd>=1 by resource-count definition, not by a hard-family embedding.

**Oracle correspondence.** The proof invokes no gradient, Hessian, comparison or sample-data response; it only uses the declared nonnegative call-count units of the unchanged interfaces.

**Guarantee conversion.** Every execution has NH>=0, including failed executions; hence every successful admissible algorithm and its Hessian cap satisfy the same lower0. No extra success or hypothesis-test premise is used.

**Output rule.** Any output or failure symbol allowed by the native contract is covered; no coordinate sign or constructed output restriction is needed.

**Resource conversion.** NH is a nonnegative integer on every path and every admissible worst-path cap is nonnegative. This is solely the q3 lower0; the separate finite gradient-only witness b9 supplies the matching upper, not this lower proof.

**Local argument.** HOS06_GRADIENT_ONLY_SOSP_20261116

### B11 - One explicit finite gradient-only algorithm with simultaneous worst-path vector(Cgf,0).

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Randomized witness

$$
(N_g,N_H)\preceq(C_{gf},0)
$$

**Conditions.** Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.

**Dimension conditions.** Every fixed finite integer d>=1. The explicit Cgf=K(mg+2d*mH) is finite and displays its dimension dependence; no high-dimensional threshold or embedding argument is used.

**Oracle correspondence.** Only full sample-gradient calls are requested. At an iteration, mg independent fresh handles estimate the mean gradient; another mH fresh independent handles each supply all2d central-difference gradients at x+/-h*e_j using that same handle. No sample Hessian, value, comparison, hidden sample data or free validation oracle is used.

**Guarantee conversion.** The SAME explicitly capped algorithm returns a point satisfying BOTH population SOS conditions with probability>=2/3 for each instance, by conditional gradient/matrix estimation, a 2K union bound and descent; failed cap exhaustion returns bottom and counts as failure.

**Output rule.** Return the current arbitrary point x in R^d when the explicit gradient/curvature tests pass, or bottom on cap exhaustion; no first-coordinate sign restriction or external certificate is imposed.

**Resource conversion.** All gradient estimates,2d differences per sample matrix, initialization and stopping are included in worst-path Ng<=Cgf=K(mg+2d*mH),NH=0. Linear algebra/eigendecomposition is internal arithmetic allowed by the frozen model. No independently optimized marginal budgets are paired. This is a joint achievable vector, not the two scalar coordinate minima.

**Local argument.** HOS06_GRADIENT_ONLY_SOSP_20261116

### B12 - Nonnegative sum upper projection of that SAME(Cgf,0) algorithm, giving total<=Cgf.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N_g+N_H<=C_{gf}
$$

**Conditions.** Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.

**Dimension conditions.** Every fixed finite integer d>=1. The explicit Cgf=K(mg+2d*mH) is finite and displays its dimension dependence; no high-dimensional threshold or embedding argument is used.

**Oracle correspondence.** Only full sample-gradient calls are requested. At an iteration, mg independent fresh handles estimate the mean gradient; another mH fresh independent handles each supply all2d central-difference gradients at x+/-h*e_j using that same handle. No sample Hessian, value, comparison, hidden sample data or free validation oracle is used.

**Guarantee conversion.** The SAME explicitly capped algorithm returns a point satisfying BOTH population SOS conditions with probability>=2/3 for each instance, by conditional gradient/matrix estimation, a 2K union bound and descent; failed cap exhaustion returns bottom and counts as failure.

**Output rule.** Return the current arbitrary point x in R^d when the explicit gradient/curvature tests pass, or bottom on cap exhaustion; no first-coordinate sign restriction or external certificate is imposed.

**Resource conversion.** All gradient estimates,2d differences per sample matrix, initialization and stopping are included in worst-path Ng<=Cgf=K(mg+2d*mH),NH=0. Linear algebra/eigendecomposition is internal arithmetic allowed by the frozen model. No independently optimized marginal budgets are paired. For this same witness totalNg+NH=Ng<=Cgf; it is not an optimal total-rate claim.

**Local argument.** HOS06_GRADIENT_ONLY_SOSP_20261116

### B13 - Gradient upper projection of that SAME(Cgf,0) algorithm, giving Ng<=Cgf.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N_g<=C_{gf}
$$

**Conditions.** Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.

**Dimension conditions.** Every fixed finite integer d>=1. The explicit Cgf=K(mg+2d*mH) is finite and displays its dimension dependence; no high-dimensional threshold or embedding argument is used.

**Oracle correspondence.** Only full sample-gradient calls are requested. At an iteration, mg independent fresh handles estimate the mean gradient; another mH fresh independent handles each supply all2d central-difference gradients at x+/-h*e_j using that same handle. No sample Hessian, value, comparison, hidden sample data or free validation oracle is used.

**Guarantee conversion.** The SAME explicitly capped algorithm returns a point satisfying BOTH population SOS conditions with probability>=2/3 for each instance, by conditional gradient/matrix estimation, a 2K union bound and descent; failed cap exhaustion returns bottom and counts as failure.

**Output rule.** Return the current arbitrary point x in R^d when the explicit gradient/curvature tests pass, or bottom on cap exhaustion; no first-coordinate sign restriction or external certificate is imposed.

**Resource conversion.** All gradient estimates,2d differences per sample matrix, initialization and stopping are included in worst-path Ng<=Cgf=K(mg+2d*mH),NH=0. Linear algebra/eigendecomposition is internal arithmetic allowed by the frozen model. No independently optimized marginal budgets are paired. The minimized q2 may be smaller; no Ng optimality is claimed.

**Local argument.** HOS06_GRADIENT_ONLY_SOSP_20261116

### B14 - Guard-preserving same-algorithm total-lower to joint necessary-sum halfspace.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal B\subseteq\{(B_g,B_H)\ge0:B_g+B_H\ge L_{old}\}\quad\text{on }r3
$$

**Conditions.** Exactly the unchanged old b4/r3 source guard, intersected with receiving native r2 where used: $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$

**Dimension conditions.** Retain the exact original b4 dimension/accuracy conditions: $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$ No all-dimension or flat-coordinate embedding transfer is asserted.

**Oracle correspondence.** Use the same original gradient/Hessian responses and opaque persistent-handle interface without simulation or new information. This is cap arithmetic applied to the accepted total lower, not a Bernoulli-discrimination theorem.

**Guarantee conversion.** Conditionally retain the original unrestricted-randomized q1 lower for the exact same simultaneous population SOS guarantee and instance class. A joint-cap algorithm is one of those same successful algorithms; no new probability conversion or source recertification occurs.

**Output rule.** The original admissible output point/failure convention and success event are preserved verbatim. No output sign test or new hard family is imposed by this projection.

**Resource conversion.** If an algorithm has pathwise caps(Bg,BH), its total count is at mostBg+BH. The retained lower total>=Lold therefore forcesBg+BH>=Lold on the unchanged r3 guard. Neither separate positive marginal lower nor any sufficient joint budget follows.

**Local argument.** HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: dc8738b5e39de804d0aa8afe73147b3c4a5803c367a60f88a7ed25a34fddbe82

### Native proof: SO_HO_HOS06_S_reuse__main__p1

Native pointer: /proofs/0; canonical SHA-256: 99185073d1a63b3919f46001b4f5ff8c8be8d45d25b7c343efa10f398b7e8e12

#### Native field: claim_refs

Native pointer: /proofs/0/claim_refs; canonical SHA-256: be4df3343a95756a18bf8aea1417fe6b0af1b814d67ef483f34641a76f7b2cf4

#### Native item 1

Native pointer: /proofs/0/claim_refs/0; canonical SHA-256: 40635d3e7f3b937894529c09a2781692b387308be6a7f1341b4681248b717abd

SO_HO_HOS06_S_reuse__main__b6

#### Native field: proof_steps

Native pointer: /proofs/0/proof_steps; canonical SHA-256: 3f1c43dadcfcd61597d7e055b709d7629390102c9601cbbdabf9bc90a8f48fc5

#### Native item 1

Native pointer: /proofs/0/proof_steps/0; canonical SHA-256: 6d3cbff27ca362928edf56273844ce8472bae3a8e6b8e56b784af47298d6ee37

Translate the public initial point to the origin. Set e=epsilon_g, b=sigma_1/2 and t=x_1-(x_0)_1. For hypotheses h=+2e and h=-2e, let independent handle variables Z take values +/-b with mean h. Define ell_h(x;Z)=4e*sqrt(1+t^2)+Z*t, independent of all other coordinates. Its population objective is 4e*sqrt(1+t^2)+h*t.

#### Native item 2

Native pointer: /proofs/0/proof_steps/1; canonical SHA-256: 575ac83107ad71ed2c1132086cfbf09a2c6daf7a8b993816824b20a0909fd8c1

These populations have finite minima 2*sqrt(3)*e and initial gap (4-2*sqrt(3))*e. Their gradient norm is at most 6e. Each sample Hessian has only entry 4e*(1+t^2)^(-3/2), so sample-gradient Lipschitz constant is at most 4e and sample-Hessian Lipschitz constant is at most 12e. Gradient noise is at most b+2e<=sigma_1; Hessian noise is zero. Differentiation commutes with expectation. The r7 inequalities therefore ensure every fixed-contract assumption. Only the population must be bounded below; individual sample losses need not be.

#### Native item 3

Native pointer: /proofs/0/proof_steps/2; canonical SHA-256: 2f1a1238c84c5c744144e44afc11eff165dd4111741b0c8285d9f23656681702

The population Hessian is positive semidefinite, so any positive epsilon_H is allowed. Under h=+2e, any successful output must have t<0; under h=-2e it must have t>0. Failure symbols count as failure. Thus success probability >=2/3 separately on both admissible instances yields a test with total variation at least 1/3.

#### Native item 4

Native pointer: /proofs/0/proof_steps/3; canonical SHA-256: 7c7f6249b118f08550a2dec5a6976bbdb87e4aa99b265cd41cc9101a580a7008

All Hessian responses are deterministic and identical under both hypotheses, even at arbitrary adaptive points. The first gradient query on a handle reveals its single Z; later gradient queries on that handle add no information. Handles first used for Hessians still reveal no Z until their first gradient. Opaque handle allocation supplies no side data. Padding by unused coordinates preserves these facts for every d>=1 and arbitrary outputs.

#### Native item 5

Native pointer: /proofs/0/proof_steps/4; canonical SHA-256: a381b5176a311bbf6679d497b00fdba81e552592b8aa7eaef379eec9cac541ad

Let a=2e/b<=1/2. The two Bernoulli laws have probabilities (1+a)/2 and (1-a)/2. Their KL divergence is a*log((1+a)/(1-a))<=4a^2=16e^2/b^2. Adaptive transcript chain-rule accounting bounds KL by (16e^2/b^2)*n when the worst-case gradient cap is n, regardless of the finite Hessian cap. Reuse contributes zero new conditional divergence.

#### Native item 6

Native pointer: /proofs/0/proof_steps/5; canonical SHA-256: 3f09206796656622408b8cefe25ebccdca4f8182938f350a292c27d97525f198

Pinsker's inequality as used in Appendix C gives KL>=2*(1/3)^2=2/9. Consequently n>=b^2/(72e^2)=sigma_1^2/(288e^2). This holds for every feasible algorithm, hence also for the q2 minimax infimum. The threshold and coefficient are explicit and uniform in all nine native parameters. The extension from the source's one-dimensional construction to arbitrary finite d is the flat-coordinate embedding above; no target subclass assumption is added.

#### Native field: source_hash

Native pointer: /proofs/0/source_hash; canonical SHA-256: 0029b121a20500e3cec6ddd441354fc02c1b6fa871e1beda53b851183b756684

823bfd622821d7a90d406041aa4fe994036503dd9b7385dcfd79161baa0b42b3

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 0c64ffe5a599a7a475cb7f5a3aa50c63ae37ce980304a1e9f330342ffff0d8d6

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 6672fb2f13aa3f49de2d795ece50fd9b7b8f470c9937d1c67e361451b6be25ae

SO_SRC_1e0f32cd5172fba2

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: 9c2a0f5a550827098534a27a503a80910b67500ecdfb2a7ba0d899d0c38c38dd

On r7, every algorithm meeting main/g1 has worst-case gradient cap at least sigma_1^2/(288*epsilon_g^2), even allowing arbitrary Hessian evaluations.

### Native proof: HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

Native pointer: /proofs/1; canonical SHA-256: f6fb26c870204c9d88e2a314233d8f1b9bf687ba7a6b94e5c7cba17d9c4cf748

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 35ef02782753222040f20776badc7d6824b5958da8ae628a7bcf24a599584955

The frozen b6/p1 establishes Ng>=L=sigma1^2/(288epsilon_g^2) on exact r7 for every successful algorithm, with arbitrary finite Hessian budget. For each same algorithm and each path,Ng+NH>=Ng becauseNH>=0. Thus any successful total-budget algorithm must have totalcap>=L. Likewise a successful jointcap(Bg,BH) must satisfy Bg>=L. Equivalently B subset{(Bg,BH)>=0:Bg>=L}. Infima over identical algorithm/instance/guarantee classes preserve these implications. This is not equality or identity of q1/q2/q4: new quantity-matched bounds carry explicit directions. No reverse implication, Hessianlower, sum-to-gradientlower or mixing of different algorithm minima is claimed. The oldr7 guard remains exact; onr3 intersectr7 maximize the old total lower and this newL, even if one is dominated. The proof also records that a single algorithm with jointcap(C,0) gives the three marginal upper witnesses, but not a pair formed from different optimizers. The retained older q1 lower Lold on exact r3 also implies, for the same algorithm class, the joint necessary sum halfspace Bg+BH>=Lold on r3. This implication is separately published as b14; it yields no positive Ng or NH marginal lower alone and is not asserted outside r3.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: d8326689898c168b9baa4840d579a3dcb722a6196ba9935b5f203d63b2b8658d

#### Native item 1

Native pointer: /proofs/1/limitations/0; canonical SHA-256: 169044e0d4c3cda8c1a6726155e3f4ec9331b45416bd1b52141e8dd567461ff3

user-feedback-guided curated analyst_derivation; not a prior blind scout result; no old approval/source-read credit transferred

#### Native item 2

Native pointer: /proofs/1/limitations/1; canonical SHA-256: f32fbff2e31d9fb69deace36ed7b339a1d0539d8f82ae462ab845a17c6c50355

External retained premises keep their original validity; this candidate has no native approval.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 3c4e46b6c6943b35ab0df8f2081cea712553bf241dd394a15aec9e1d85df8162

Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 56863128b732905ea80a67269544daaf7e3c27fa8b56990ea104989aa3611bd6

Directed implications between native derivative resource projections

### Native proof: HOS06_GRADIENT_ONLY_SOSP_20261116

Native pointer: /proofs/2; canonical SHA-256: 61b53984aac48e07cb679ac4c9bd9a9acff4207a81984663bff13a87a4abfcbb

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: dcbcd608b71c27f405399666b14d8c2af14585cb5728bf9619348ac03943332c

# HOS06: An explicit witness with finitely many gradient calls and zero Hessian calls (pending independent review)

This round is an analyst_derivation guided by user feedback, not an outcome of the earlier blind scout, and confers no additional credit for earlier native source_read or approvals. The argument establishes only the single-coordinate q3 claim and a joint-budget witness for the same algorithm; it does not combine the minimum gradient cost of another algorithm with zero Hessian cost.

Contract basis: in the new previous-baseline, on a single common probability-1 event, the sample losses have globally β-Lipschitz gradients and M2-Lipschitz Hessians; the population objective has initial gap≤Δ; distinct new handles are independent, and the same handle may be reused across points; the gradient error is ≤σ1 almost surely; all public structural parameters β,M2,Δ,σ1,σ2,G are strictly positive, with d≥1 and 0<εg,εH≤1. Thus this proof does not tacitly exclude β=0/M2=0: these cases were already outside the native structural domain. Queries range over the entire space. Population differentiation and expectation may be interchanged; the native resources Ng,NH are counted separately, the failure symbol ⊥ is permitted, and per-instance success≥2/3 together with a finite resource cap on every execution path is required.

## Public parameters and fixed caps

Let

\[
a=\min\{\varepsilon_g/8,\varepsilon_H^2/(48M_2)\},\quad b=\varepsilon_H/4,\quad
D=\min\{\varepsilon_g^2/(16\beta),\varepsilon_H^3/(16M_2^2)\},
\]
\[
K=\lfloor\Delta/D\rfloor+1,\quad
m_g=\max\{1,\lceil6K\sigma_1^2/a^2\rceil\},\quad
m_H=\max\{1,\lceil24Kd\beta^2/b^2\rceil\},\quad
h=b/(M_2\sqrt d).
\]

These quantities depend only on the public inputs and are all positive and finite. Let
\[
C_{\rm gf}=K(m_g+2dm_H).
\]
No attempt is made to optimize this highly conservative gradient cap; its purpose is to establish a single finite witness valid throughout the contract, rather than to claim optimal gradient complexity.

## Estimators: gradient oracle calls only

At the current point x:

1. Request one sample gradient from each of mg previously unused new handles and take their average \(\widetilde g\). Conditional on the past, independence, unbiasedness, and an error second moment ≤σ1² give
\[
\Pr(\|\widetilde g-\nabla f(x)\|>a\mid\text{past})\le\sigma_1^2/(m_ga^2)\le1/(6K).
\]
2. When a curvature check is needed, draw another mH independent new handles; for each handle a, request two gradients \(\nabla\ell(x\pm he_j;Z_a)\) along each coordinate axis at the same x. Use the central differences as matrix columns to obtain D_a, symmetrize to \(A_a=(D_a+D_a^T)/2\), and take \(\widetilde H=m_H^{-1}\sum A_a\). Neither a sample Hessian nor a sample value is requested.

Each column of D_a has norm ≤β, so \(\|A_a\|_F\le\sqrt d\beta\). The M2-Lipschitz property of the sample Hessian gives a central-difference error ≤M2 h/2 in each column; therefore
\[
\|\mathbb E A_a-\nabla^2f(x)\|_{op}\le\sqrt d M_2h/2=b/2.
\]
Symmetrization does not increase the error in the Frobenius/operator norms. The Hilbert-space variance of the independent sample matrices satisfies
\[
\mathbb E\|\widetilde H-\mathbb EA_a\|_F^2\le d\beta^2/m_H.
\]
Thus Chebyshev and op≤F give
\[
\Pr(\|\widetilde H-\nabla^2 f(x)\|_{op}>b\mid\text{current gradient and past})
\le4d\beta^2/(m_Hb^2)\le1/(6K).
\]

Reuse occurs only among the 2d finite-difference gradients for a single new handle. Handles within the matrix batch are independent; the gradient batch and the matrix batch are independent; and new batches are independent across iterations. The conditional bounds hold uniformly for adaptively selected x, without incorrectly treating reused noise as independent. The common probability-1 sample-smoothness event makes all adaptive locations simultaneously valid.

## Truncated algorithm

Starting from the public x0, execute at most K iterations:

- Form \(\widetilde g\). If \(\|\widetilde g\|>\varepsilon_g/2\), set \(x\gets x-\widetilde g/\beta\) and proceed to the next iteration.
- Otherwise, form \(\widetilde H\). If \(\lambda_{min}(\widetilde H)\ge-3\varepsilon_H/4\), return the current x.
- Otherwise, take a unit eigenvector v corresponding to the smallest eigenvalue of the known symmetric matrix, choose its sign so that \(\widetilde g^Tv\le0\), and set \(x\gets x+(\varepsilon_H/M_2)v\).

If K iterations are reached without returning, output ⊥. Eigendecomposition of a known matrix, inner products, and linear algebra are all free internal operations; sign selection and termination verification require no additional information/function-value calls. Use a fixed measurable eigenvector-selection rule; tied eigenvalues do not affect the inequalities. h and every step are finite, positive/known; all loops are truncated, so the per-path cap is retained even when the estimates are inaccurate.

## Joint good event, descent, and accuracy

There are at most K gradient estimates and K matrix estimates. A union bound using the conditional failure bounds gives a good-event probability ≥1−2K/(6K)=2/3. All conditions below hold on this same event.

If a gradient step is taken, a≤εg/8 and \(\|\widetilde g\|>\varepsilon_g/2\). β-smoothness gives
\[
f(x-\widetilde g/\beta)-f(x)
\le-\|\widetilde g\|^2/(2\beta)+a\|\widetilde g\|/\beta
\le-\varepsilon_g^2/(16\beta).
\]

If a negative-curvature step is taken, \(v^T\nabla^2 f(x)v<-\varepsilon_H/2\), while \(\nabla f(x)^Tv\le a\). The population Hessian is also M2-Lipschitz. Set s=εH/M2; the Taylor upper bound then gives
\[
f(x+sv)-f(x)\le as-\varepsilon_Hs^2/4+M_2s^3/6
\le-\varepsilon_H^3/(16M_2^2).
\]

Hence every nonterminating step decreases the objective by at least D. Since K D>Δ, all K steps cannot be nonterminating on the good event, as that would violate f(x0)−inf f≤Δ.

At termination (including a threshold attained with equality),
\[
\|\nabla f(x)\|\le\varepsilon_g/2+a\le5\varepsilon_g/8\le\varepsilon_g,
\qquad
\lambda_{min}(\nabla^2f(x))\ge-3\varepsilon_H/4-b=-\varepsilon_H.
\]

The algorithm therefore satisfies both SOS conditions at the same point with probability at least 2/3, and on every execution path
\[
N_g\le C_{\rm gf}<\infty,\qquad N_H=0.
\]
The nonnegativity of q3 gives the matching lower bound 0, so the Hessian single-coordinate optimum is exactly 0. This conclusion does not state Ng=0 or total=0; the jointly attainable budget of this same witness is \((C_{\rm gf},0)\) and its upward closure. It cannot be combined with the q2 optimum of a different algorithm to obtain a smaller joint budget.

## Online literature verification actually performed in this round and limits of adoption

The [original SPIDER paper arXiv:1807.01695v2](https://arxiv.org/pdf/1807.01695v2) was actually opened and read: §3.1 Assumptions1–3 (PDF pp9–10), §3.3 Algorithm2/Theorem6 (pp14–15), footnote 9 on success-probability amplification, and the beginning of Appendix B.4. The paper does construct an SOS algorithm using stochastic gradients; its sample conditions are compatible with this native contract. Direct adoption, however, would also require addressing internal accuracy, verification/restarts from 1/2 to 2/3, and per-path accounting. Accordingly, this candidate does not claim to have completed a transfer of the full SPIDER proof and does not adopt its optimized gradient rate; the zero-Hessian conclusion is supported by the independent explicit finite algorithm above. This report does not reprove the full appendix or the Neon2 proof.


#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: d8326689898c168b9baa4840d579a3dcb722a6196ba9935b5f203d63b2b8658d

#### Native item 1

Native pointer: /proofs/2/limitations/0; canonical SHA-256: 169044e0d4c3cda8c1a6726155e3f4ec9331b45416bd1b52141e8dd567461ff3

user-feedback-guided curated analyst_derivation; not a prior blind scout result; no old approval/source-read credit transferred

#### Native item 2

Native pointer: /proofs/2/limitations/1; canonical SHA-256: f32fbff2e31d9fb69deace36ed7b339a1d0539d8f82ae462ab845a17c6c50355

External retained premises keep their original validity; this candidate has no native approval.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 3c4e46b6c6943b35ab0df8f2081cea712553bf241dd394a15aec9e1d85df8162

Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: f35f181f38200d3af4721075e4c0bd780c085ba2fe416dfdc43f08a5277db865

Explicit capped stochastic-gradient-only second-order stationarity witness

### Native proof: HOS06_HESSIAN_UPPER_REPLACEMENT_20261116

Native pointer: /proofs/3; canonical SHA-256: 925aaa0437c5cadf0f3735fffb93005ecf68ffbc0ac5ba6bde5db506192d0dd9

#### Native field: baseline_refs

Native pointer: /proofs/3/baseline_refs; canonical SHA-256: 11f2b02cef74abc34fd7476cb1984f9547b7d859cf187b820b0cda9488346ae4

#### Native item 1

Native pointer: /proofs/3/baseline_refs/0; canonical SHA-256: a3c0420b155cd533ad468253bdf7700ac0260099ab1d118cdc42e4b1377a6a80

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/0/pointer; canonical SHA-256: d6039afddf27bddb8de5dba6560d032afc09d8a78c6a685d9519ce1cea90d703

/bounds/1

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/0/sha256; canonical SHA-256: 6c5261f443b5b3e82bf36e79faf542104a4b6b1d14908f1a94332f71ac71cb55

4963459cc9625c658ae0d13a1df0a8df5dc106084087e633dcde5e587dee97ab

#### Native item 2

Native pointer: /proofs/3/baseline_refs/1; canonical SHA-256: 9962056281fa30f0f8ced2ddd2679c90b0150c3eb9774d844353d294ea643038

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/1/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/1/sha256; canonical SHA-256: 73bc06ffc924b5734983eb8d4ac1479bfe613e92a10cb4738c17e0daabfcb818

da8090927621eb9794f7c260de6c4fd4d4eaafa0810afe0e45ff0c01d190c001

#### Native item 3

Native pointer: /proofs/3/baseline_refs/2; canonical SHA-256: c7302bfd3ce9c23d72df6687e66f197234c0604789c3ab0dd8eb2ac4297f7c53

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/2/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/2/sha256; canonical SHA-256: 32ab5cbda7da6c9fe6917348afb97d05418e489c92843bc9385d877997596d7e

344b32705a9c4fdabca29c577e1bab2a1af8b6114270daf8aac88b0fb81cb921

#### Native item 4

Native pointer: /proofs/3/baseline_refs/3; canonical SHA-256: ac0938878b255e9b167c83489c586900093f9a96a215e8485e73ddaa89e3636d

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/3/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/3/sha256; canonical SHA-256: 8fdb47c65624550d90f2821b8bdb1138f2d56c85b3be3517082b522bec52d76a

8c410c50d7e7da1df65eccb4d0ab1e01b931a832f9ae4913a77f8b8d4df73682

#### Native item 5

Native pointer: /proofs/3/baseline_refs/4; canonical SHA-256: 9859e745c43b83bd826371efd6840d139ad05034458a3370d9a2e859ff0ba2d8

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/4/pointer; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/4/sha256; canonical SHA-256: d4893cf9255d78c0645fc3adefd1502207da19183f4fb60b4ad0c3f1981f8bfc

7b8a34bcf946b03c901027f13305a4e167e2ad770be09209eb052350937e778b

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: 889968ff297f7e3f56ad293a9a758c980bba06aa1c10ecd35bf63d8c902a1f1b

Retain conditionally the exact frozen b2 upper for scalar Hessian-query optimum q3 on original r2 under main/g1, without recertifying its historical external source or changing its numeric formula/validity guard. The complete new finite capped proof HOS06_GRADIENT_ONLY_SOSP_20261116 explicitly certifies a SAME algorithm with Ng<=Cgf<infinity and NH=0 on every execution path, and simultaneous population SOS success>=2/3 on the entire same r2 target. It uses only stochastic gradient calls with same-handle finite differences and all original public/samplewise assumptions. Hence q3<=0; resource nonnegativity gives q3>=0, so q3=0 there. Zero is no larger than the old nonnegative sufficient upper cap, so that historical upper may remain a valid conditional statement while being dominated in c3's selected envelope. The publication change selected_in_regimes:[c3]->[] is a genuine replacement, not a strict append-only unchanged-baseline bookkeeping exception. It is supported by the new exact-zero witness and nonnegativity, never by a claim that the full published b2 object was unchanged. c3 uses new b9/b10 to certify exact0. No zero Ng, zero total, independently optimized joint pair, or source-guard extension follows. Outside the unchanged target no result is added.

#### Native field: proof_refs

Native pointer: /proofs/3/proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /proofs/3/proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: a7be04ef0ca5eb399d4e8a270eb30bcd4b6d0d38f130abfda9fdbc5159705b12

Unchanged main/g1/q3/c3 and b2 original r2 only.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: ad206b9f3a506d724377c28925880842e3b379c9950af531e6f659891c6b0cc5

Explicit replacement of the historical Hessian upper participant

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 7d70ead5e94c84ee155185a171148b2b03b99f7fe9947b0903536b3d20388a1f

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: b3708b6396fa2a398c8dc28270c8ae8deac540762f4bd985475b896abf977bfd

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: d6715648e3c1675cdfe35cc9c4270b30c24c43cdf8c4521dc60444520c1600d6

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: d0f1422a7275abae6e365e1d68109ac8e67be12384f7a7a5b1a483b9d6b9ba78

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 00283cdcaf79e8f6a0defce2be523e291da2bc114c51811e5af7e8964db8c1f4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 9ece930192e93e0a917db5e70cf7dba47c5f98424bda551efbf78f7bdbde2768

Comparison region: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND Bound validity: (Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "$d\\ge1,\\quad0<\\varepsilon_g,\\varepsilon_H\\le1,\\quad\\theta>0$", "region_ref": "SO_HO_HOS06_S_reuse__main__r2"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: ae5cbb2842c7a31a8ec929bf99894df67b7e8d6e1b063b5f3e17fcb29804a1ce

SO_HO_HOS06_S_reuse__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 98044d0c29085a2119f5fe6fe1ed1d71f41df72791b2e594dfe9930a9e03f778

Retained q1/sum upper bound; only its intersection with r3 is displayed here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 130cb7b3ee39d9973e25e175bf32b862b2f1905bc665923c017c0bda09e87aed

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: f74c502ba088407658467fe49a0b27889004a3320c0101c031fb2bb06dd6a62e

Comparison region: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND Bound validity: (Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$))

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 06ac0ae5be77b122c05ef886ae4257c063acf9b25cae6a5a65cd4809e03b946f

SO_HO_HOS06_S_reuse__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: b895eb376d411a04bf3f426969aa3f12566f28b7826357c2d7769617480e8296

Retained unrestricted randomized q1/sum lower bound; the dimension condition is source applicability.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 52028b293c8e8da683d8c2cdffb6709b3572c85c1eba99b4540e1b0007d53dd7

Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 5c1bff7a519ecf30a8d2e7b8d37d1b220e694f1c216f97e6833e6f5fe29c4def

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: e2bea876d5b01adf95355fcfa3d5a1eb1c0f18cb82989aef4da6c94606c19fe2

SO_HO_HOS06_S_reuse__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 160fb7615456457124de138e3345b72738dcc760541ebb78a9499518cc0d1d87

Distinct quantity/resource IDs; no transfer is adopted into this comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: c36d6be23d5dc06281ea7d65530e125726cc4383435ce0ca73fd523d403f07ee

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 160fb7615456457124de138e3345b72738dcc760541ebb78a9499518cc0d1d87

Distinct quantity/resource IDs; no transfer is adopted into this comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: fadc0971baa518f8515e895ab197289d02cc308413fd1a95f341cf280c13f3ab

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: 8b2bfb9ed10b34dcb679c9beed579713efc81b4ffcade8f4b512788295cdce68

SO_HO_HOS06_S_reuse__main__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: 160fb7615456457124de138e3345b72738dcc760541ebb78a9499518cc0d1d87

Distinct quantity/resource IDs; no transfer is adopted into this comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/bound_uses/5; canonical SHA-256: 2a83852286418afcffc417f616b417fb1ef001cdef1bd7432c702fbb84f34de2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/bound_id; canonical SHA-256: 40635d3e7f3b937894529c09a2781692b387308be6a7f1341b4681248b717abd

SO_HO_HOS06_S_reuse__main__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/reason; canonical SHA-256: 8bdff6bb0e57c3193ba36b45608a4a57884426bdcf8967c039ea02841ee8954b

The literalq2 scalar row is notmerged. Its directed implications are proved and adopted through quantity-matched b7(sum) andb8(joint necessaryhalfspace).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/validity_region; canonical SHA-256: 9ca5e8634604660045ef04b6cc2d40af30390e65c2e248ea0e0cc3f23513ff28

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/bound_uses/6; canonical SHA-256: 93dccb97e6d00dcc1698bf7e5a1a0ec9ede48dd69c07f394d003b3ff9f7a0708

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/adopted_region; canonical SHA-256: eb7e49653ce21388b85cc5a9bc52965a200b7bd09fcd006cd9faf21e88901cc6

Comparison region: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND Bound validity: (Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Unchangedr7, intersectr3 for this c1.", "region_ref": null}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/bound_id; canonical SHA-256: d27979fbb4ff540b828b9bcf3eb65ff7df3be3f55e99207f18815dd518826fd2

SO_HO_HOS06_S_reuse__main__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/reason; canonical SHA-256: 43870d598e6a3b973c97f795fb8d221911479aabc16a060d8da2c4d602879ef4

Quantity-matched total lower follows from original robust Ng>=Lg and Ng+NH>=Ng, only on r7 intersect this comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/validity_region; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 8

Native pointer: /joint_analysis/comparisons/0/bound_uses/7; canonical SHA-256: ac48554815517e826f99f9b09409663570b7822953c49763b76569de9ccdf987

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/bound_id; canonical SHA-256: 62c122f2bb12b92af4bfb00323b7590c0619e3e536669a423a6167881d359cc3

SO_HO_HOS06_S_reuse__main__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/7/validity_region; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 9

Native pointer: /joint_analysis/comparisons/0/bound_uses/8; canonical SHA-256: e0e8d6af0ef7aed25362f35742eecb9bff5b7ed3fc626b08df28916b679b57a6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/bound_id; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/8/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 10

Native pointer: /joint_analysis/comparisons/0/bound_uses/9; canonical SHA-256: 247942ab70058a0485cdd5cfb3ffa41f0fe6c6647569cee7be771211a08afa4b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/bound_id; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/9/validity_region; canonical SHA-256: 46f621275f85d7a8e0a6cc175d6eb0bbeeed84077a832b2c0dd532e0cc20c813

(Unchanged target r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 11

Native pointer: /joint_analysis/comparisons/0/bound_uses/10; canonical SHA-256: e60fa1950f0dbc25f3b71bbaf2536c0b85008f40919c403cb9a05f2f139bbed9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/10/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/10/bound_id; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/10/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/10/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/10/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/10/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/10/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/10/validity_region; canonical SHA-256: 3355a6bae6f9d2e2849259ec7981722027e22977effd417adce5cab45da08c9a

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND (Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 12

Native pointer: /joint_analysis/comparisons/0/bound_uses/11; canonical SHA-256: f67b99a162494018519db038adb99ce6058821f05a3eac5eafb9812d8ff0ffa2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/11/adopted_region; canonical SHA-256: 10ab86391222ede6798c9646b8623e55cc94668412339315e472f5d49fbe7469

Comparison region: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND Bound validity: ((Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.", "region_ref": null}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/11/bound_id; canonical SHA-256: 9625661fb8c53c6c9524b366b157ae48b6e2a0c3a09535bd0ef568a6f4b2f7e2

SO_HO_HOS06_S_reuse__main__b12

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/11/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/11/mapping_proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/11/mapping_proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/11/reason; canonical SHA-256: 6361a71f0c165725af0356bfff60fc72d604327be9843d10943250beed5919ce

Sum upper of the SAME finite gradient-only witness: Ng+NH=Ng<=Cgf on its proved native target.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/11/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 13

Native pointer: /joint_analysis/comparisons/0/bound_uses/12; canonical SHA-256: a02c1b895f9ed96963987a1982a6919a6eec80b2410927127b96ea505f9af5c1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/12/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/12/bound_id; canonical SHA-256: a5835deee3b5251752a48d50c4b66ff5e9c708cc235efb44900cb2a26a13e0a3

SO_HO_HOS06_S_reuse__main__b13

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/12/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/12/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/12/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/12/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/12/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/12/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 14

Native pointer: /joint_analysis/comparisons/0/bound_uses/13; canonical SHA-256: d858717865e266b9fd762134bd869fa7dcaab7f9e179fcc296aea6f46c6d05dd

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/13/adopted_region; canonical SHA-256: 530af9b10790ef7558742b3d3219945348d067b89dfbfec230b05f7697377e30

No literal quantity merge; its valid implications are explicitly represented.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/13/bound_id; canonical SHA-256: 9d49ad9e5587ad73868b47fb1678457a90d0aebac4d4c8f6a9337213c93b7130

SO_HO_HOS06_S_reuse__main__b14

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/13/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/13/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/13/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/13/reason; canonical SHA-256: 1444dcecd03c25f4a423369a1965d0a15074a1104c14442e880d4fb998022d5b

A same-algorithm joint necessary sum halfspace from the retained q1 lower; the literal joint quantity differs in scalar rows, whose original total lower remains active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/13/validity_region; canonical SHA-256: 569e71e6eb987fb6ffa0150dac91ee49ffba28e20fb382ed2551be6230a4d9d4

Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND (Exactly the unchanged old b4/r3 source guard, intersected with receiving native r2 where used: $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 3d35abec3c6772d0a577e3a98c09dcfdac3300e3ea2233aad205538f35d47043

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 9ad07e5c9f02d28c936bb0faed9c0e1a7f7164b8c1f7a503728b29e1726ff08e

r3 has an unspecified sufficient source dimension threshold, not a proved intrinsic phase transition.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 623b4272e014c88aa8e8542077b0149c02c747b5dc698153e5798a89371d9628

epsilon_g and epsilon_H remain independent; neither is replaced by a fixed-parameter slice.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: e4b7c975d4f73f9dd711530a8f084f73d9b78bc77328084d2fbebadd791ccdb9

The new marginal lower bound concerns q2 and does not replace or strengthen this retained q1 envelope.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: acdf0cab8b25fce346fa055070ac156dc0af82d92cfabc4b88b84f0db9018c37

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/0; canonical SHA-256: 92ffedc715a1d5ffe8f98e16298777d6cfe08037922a53723da4b7eaf98b67a2

SO_HO_HOS06_S_reuse_p_360c30de02

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/1; canonical SHA-256: 3b62aa9f90972f46cdb02143a98e47c210dd4e56a049b65462248b824d871162

SO_HO_HOS06_S_reuse_p_58c6dbfa8a

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/2; canonical SHA-256: 7033b07143ee6c8e8ab1cc4ee6945216f9f3f8948a64e7cfa71f84d6af3272be

SO_HO_HOS06_S_reuse_p_fb9a0c2872

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/3; canonical SHA-256: 6d3482225c13218e1267c0b2cfd93d4d7a0bc45ca10b2f4af37c1db25d199c1b

SO_HO_HOS06_S_reuse_p_26aa16ff5b

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/4; canonical SHA-256: d563822a02ff1cd27784f53df621d6ca99707d5b602115ff5a93bf409fe81d1f

SO_HO_HOS06_S_reuse_p_1bfb19894a

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/5; canonical SHA-256: ed68a704c652d42876f81a0d09952ff55da2e27943967e15748f7d748bfebc8d

SO_HO_HOS06_S_reuse_p_45d020550f

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: acdf0cab8b25fce346fa055070ac156dc0af82d92cfabc4b88b84f0db9018c37

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/0; canonical SHA-256: 92ffedc715a1d5ffe8f98e16298777d6cfe08037922a53723da4b7eaf98b67a2

SO_HO_HOS06_S_reuse_p_360c30de02

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/1; canonical SHA-256: 3b62aa9f90972f46cdb02143a98e47c210dd4e56a049b65462248b824d871162

SO_HO_HOS06_S_reuse_p_58c6dbfa8a

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/2; canonical SHA-256: 7033b07143ee6c8e8ab1cc4ee6945216f9f3f8948a64e7cfa71f84d6af3272be

SO_HO_HOS06_S_reuse_p_fb9a0c2872

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/3; canonical SHA-256: 6d3482225c13218e1267c0b2cfd93d4d7a0bc45ca10b2f4af37c1db25d199c1b

SO_HO_HOS06_S_reuse_p_26aa16ff5b

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/4; canonical SHA-256: d563822a02ff1cd27784f53df621d6ca99707d5b602115ff5a93bf409fe81d1f

SO_HO_HOS06_S_reuse_p_1bfb19894a

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/5; canonical SHA-256: ed68a704c652d42876f81a0d09952ff55da2e27943967e15748f7d748bfebc8d

SO_HO_HOS06_S_reuse_p_45d020550f

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: a20b92518cb493318b8d446ced72633362d764356f1c5e2df925da8527be0efb

The guarded quotient ofthe stated compatible envelopes; old asymptotic upper remains available.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: aba98b96375798ef6e953398b85271e269cd11e18137f314898b0ebfa72ee1f9

max{L_old,L_g whenr7}

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 1a8dc08ebb5228a1b40adaa210782b154de3cefdb67c199d44dd375bf7654c51

No sharp total frontier is claimed. L_g is valid in addition to oldlower even if dominated.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 0b69a915b1a2b80c315d2266c4a2e09d1fe14e4a40876a349b297043a59fcdfc

min{U_old,C_gf}

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 98b6555e36a21f9c078b44eec775ea2beacb42d1c4a35a1383adf2ef447b78b2

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 5869f5e968419b388f24d8032c805143c2fe1ee0b301c006696e8c0bf9c52c4f

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 04b6d519830ae94c09aecabf929913c4379c475feee911f5c1be0d4a9ca82a15

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 1e934f1f09936a6f084a5024a8b3cd5608e612b58ae62bcac1eb36695613de70

Comparison region: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND Bound validity: (Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$))

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: e2bea876d5b01adf95355fcfa3d5a1eb1c0f18cb82989aef4da6c94606c19fe2

SO_HO_HOS06_S_reuse__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 15fe1a89038f3fe5643ff856852ad54fe05da012c447ffdcccb7f691925c7ba7

Retained uniform explicit-parameter upper bound for q2.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 6bc9def00b360bf9158886931f776520e6d53c6a9f6ac2cb512f246bd05f97fb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: b2f297dad0a2388e53bbc9264987adf83b6fae0fe8697bfd2dcad60bd18e19d4

Comparison region: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND Bound validity: (Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive", "region_ref": "SO_HO_HOS06_S_reuse__main__r7"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 40635d3e7f3b937894529c09a2781692b387308be6a7f1341b4681248b717abd

SO_HO_HOS06_S_reuse__main__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 65f1f3b9952a378b816ed7da7d5def3470773a2084d80268452c63832a0584f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 8b9ff11578e738aa89cca94088565503bf71f5ed015e1429e1cae6c857760bd5

SO_HO_HOS06_S_reuse__main__p1

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: c1bc8327c76ab3a9d880c68417fb446f2cc528bdddbb706336c1ca497d17808d

Appendix C hard subclass with explicit activation threshold and constant; no restriction on Hessian access.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 9ca5e8634604660045ef04b6cc2d40af30390e65c2e248ea0e0cc3f23513ff28

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 27aac6ff8e1b77a1e71fd5ae73d9b77f5bd36dea9847e33d49454e08776abf75

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 9e1a17a45914047a700efa5855974b38caa1809b59b559d847c0ad6d091ac933

Distinct quantity/resource IDs; no transfer is adopted into this comparison. A total-call lower bound cannot be split into a gradient-call lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: 6ebcb1f7b11cce5c7b5a097bd4123f22e05d5bdf084fc3fbe7eb12f5fa37c364

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: ae5cbb2842c7a31a8ec929bf99894df67b7e8d6e1b063b5f3e17fcb29804a1ce

SO_HO_HOS06_S_reuse__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 9e1a17a45914047a700efa5855974b38caa1809b59b559d847c0ad6d091ac933

Distinct quantity/resource IDs; no transfer is adopted into this comparison. A total-call lower bound cannot be split into a gradient-call lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: 08a406563fe53a6f2785bea33dd59a91d6058acd5ceb2c6bdade3a30bd1d53ab

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: 06ac0ae5be77b122c05ef886ae4257c063acf9b25cae6a5a65cd4809e03b946f

SO_HO_HOS06_S_reuse__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 9e1a17a45914047a700efa5855974b38caa1809b59b559d847c0ad6d091ac933

Distinct quantity/resource IDs; no transfer is adopted into this comparison. A total-call lower bound cannot be split into a gradient-call lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: 52028b293c8e8da683d8c2cdffb6709b3572c85c1eba99b4540e1b0007d53dd7

Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/bound_uses/5; canonical SHA-256: 745d146402370a9d83e9714027f0a4310b7a21c5a24071ccfa4e3c47a8e2016d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/bound_id; canonical SHA-256: 8b2bfb9ed10b34dcb679c9beed579713efc81b4ffcade8f4b512788295cdce68

SO_HO_HOS06_S_reuse__main__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/reason; canonical SHA-256: 9e1a17a45914047a700efa5855974b38caa1809b59b559d847c0ad6d091ac933

Distinct quantity/resource IDs; no transfer is adopted into this comparison. A total-call lower bound cannot be split into a gradient-call lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 7

Native pointer: /joint_analysis/comparisons/1/bound_uses/6; canonical SHA-256: 6eb4bfa126c770f1e26e8ca1ee36a1b4b9f45d5aa82e6ff05da8aa294f5b0e3c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/bound_id; canonical SHA-256: d27979fbb4ff540b828b9bcf3eb65ff7df3be3f55e99207f18815dd518826fd2

SO_HO_HOS06_S_reuse__main__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/validity_region; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 8

Native pointer: /joint_analysis/comparisons/1/bound_uses/7; canonical SHA-256: ac48554815517e826f99f9b09409663570b7822953c49763b76569de9ccdf987

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/bound_id; canonical SHA-256: 62c122f2bb12b92af4bfb00323b7590c0619e3e536669a423a6167881d359cc3

SO_HO_HOS06_S_reuse__main__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/validity_region; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 9

Native pointer: /joint_analysis/comparisons/1/bound_uses/8; canonical SHA-256: e0e8d6af0ef7aed25362f35742eecb9bff5b7ed3fc626b08df28916b679b57a6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/bound_id; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/8/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 10

Native pointer: /joint_analysis/comparisons/1/bound_uses/9; canonical SHA-256: 247942ab70058a0485cdd5cfb3ffa41f0fe6c6647569cee7be771211a08afa4b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/bound_id; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/9/validity_region; canonical SHA-256: 46f621275f85d7a8e0a6cc175d6eb0bbeeed84077a832b2c0dd532e0cc20c813

(Unchanged target r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 11

Native pointer: /joint_analysis/comparisons/1/bound_uses/10; canonical SHA-256: e60fa1950f0dbc25f3b71bbaf2536c0b85008f40919c403cb9a05f2f139bbed9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/10/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/10/bound_id; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/10/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/10/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/10/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/10/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/10/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/10/validity_region; canonical SHA-256: 3355a6bae6f9d2e2849259ec7981722027e22977effd417adce5cab45da08c9a

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND (Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 12

Native pointer: /joint_analysis/comparisons/1/bound_uses/11; canonical SHA-256: 6bfd37e22e3718d15e00af10ffab77c88a3f937a1475ce518e2e0869d19de9fe

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/11/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/11/bound_id; canonical SHA-256: 9625661fb8c53c6c9524b366b157ae48b6e2a0c3a09535bd0ef568a6f4b2f7e2

SO_HO_HOS06_S_reuse__main__b12

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/11/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/11/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/11/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/11/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/11/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/11/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 13

Native pointer: /joint_analysis/comparisons/1/bound_uses/12; canonical SHA-256: 73405942db47d3e6a3e591a3670950e8275f97a503ea6aa311bacb7ffee415b2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/12/adopted_region; canonical SHA-256: 34d3d4da332a12d3d22d8cb38f3e57f46e4071907d313de39d3d2482e3a6a1ff

Comparison region: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND Bound validity: ((Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.", "region_ref": null}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/12/bound_id; canonical SHA-256: a5835deee3b5251752a48d50c4b66ff5e9c708cc235efb44900cb2a26a13e0a3

SO_HO_HOS06_S_reuse__main__b13

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/12/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/12/mapping_proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/12/mapping_proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/12/reason; canonical SHA-256: 91ea0e06968a60bf9e07e901a0aaa1425e68af9040a67566b1b41a21d25bc3b6

Gradient upper of the SAME finite gradient-only witness: Ng<=Cgf on its proved native target.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/12/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 14

Native pointer: /joint_analysis/comparisons/1/bound_uses/13; canonical SHA-256: d858717865e266b9fd762134bd869fa7dcaab7f9e179fcc296aea6f46c6d05dd

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/13/adopted_region; canonical SHA-256: 530af9b10790ef7558742b3d3219945348d067b89dfbfec230b05f7697377e30

No literal quantity merge; its valid implications are explicitly represented.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/13/bound_id; canonical SHA-256: 9d49ad9e5587ad73868b47fb1678457a90d0aebac4d4c8f6a9337213c93b7130

SO_HO_HOS06_S_reuse__main__b14

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/13/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/13/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/13/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/13/reason; canonical SHA-256: 1444dcecd03c25f4a423369a1965d0a15074a1104c14442e880d4fb998022d5b

A same-algorithm joint necessary sum halfspace from the retained q1 lower; the literal joint quantity differs in scalar rows, whose original total lower remains active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/13/validity_region; canonical SHA-256: 569e71e6eb987fb6ffa0150dac91ee49ffba28e20fb382ed2551be6230a4d9d4

Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND (Exactly the unchanged old b4/r3 source guard, intersected with receiving native r2 where used: $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 33f25e82321fb8a0a9e231a8456f34c6022d379eb906ad7961a054d8d7cf4cdd

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 54ed001bf2f941c7ffb2d7ffedfcbfb257b74d5814533c289f2812b1a7153d0a

At equality in every r7 threshold the non-strict regularity and KL estimates remain valid.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 938c8300d4d5e0501aacfe36948f6aee300281a6e6a0b1932d972e359dc4cb26

The hard Hessian is positive semidefinite, so epsilon_H=1 and arbitrarily small positive epsilon_H are both covered.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: e4f42ed94cc890fff0a5646fa448e6f07f1707d8eb7a264b2d820e9b40b09f2b

Every d>=1 is covered; there is no high-dimensional activation requirement.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: 12ed762e06b32dc0661898ecdf20c7043d13c8c739118bfc42359695d58572d2

The lower bound is strictly positive on r7, hence zero gradient calls are impossible there; no zero-cost ratio is formed.

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/boundary_checks/4; canonical SHA-256: 36d62c2c0594b77ef8555412dc8250353dac7bc472653bfeaa74a6e73af518a9

The threshold is a sufficient source activation guard, not an intrinsic complexity crossover. No subregion is shown rate-matched.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 0d7bca0b4d7525563a0d146ce6e58e75f3984ffdda3dab32d1d726022c1ae4eb

On r7: O(Lambda^4*B_g*epsilon_g^2/sigma_1^2). At fixed positive theta this is O_theta(Lambda^4*(1+epsilon_g^(-1)+epsilon_H^(-1))). Outside r7 the gap remains unassessed.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 577710d853139510630ce9f9bdba4f2f3006ffd714a341f49ef472c9060240b9

sigma_1^2/(288*epsilon_g^2) on r7 only; no registered nontrivial lower envelope outside r7.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 3531ec38de9261a018f9c78d140f3d69b43e36ec0c3ae27bbd3991de5bf9e089

Marginal gradient optimum remains unclosed; cannot pair its optimum withNH0 fromanotheralgorithm.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 299d34d9ac40143d5997115b815d0ce834b43a5a1e30692a1082e7f366a7c594

min{old gradient upper,C_gf}

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 38f44efc4d3cd9dbaaa8a0cdcabe6b821b7d5ce1bbea2df37eea8369688d99af

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: db60bc9f07fd7eafd6de37eab35fe4cb2d503de75ba55b8ebd459fc1f62de081

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: f81e0aba1f03a414d8665de826a98eac01ab3221d692a99069e9d854baa963fe

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: bae10f92c95cea4a5592af53c487d7c1aa01b4b3dbf0656f94e7eb63ed773f6e

The explicitgradient-only witness hasNH=0, so the oldpositiveHessian upper is valid history but dominated inthis scalar projection.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 5c1bff7a519ecf30a8d2e7b8d37d1b220e694f1c216f97e6833e6f5fe29c4def

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: e2bea876d5b01adf95355fcfa3d5a1eb1c0f18cb82989aef4da6c94606c19fe2

SO_HO_HOS06_S_reuse__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: 160fb7615456457124de138e3345b72738dcc760541ebb78a9499518cc0d1d87

Distinct quantity/resource IDs; no transfer is adopted into this comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: b9fc43144ac4235c3dec4cf32d361c709579c0c17300edc878edf8ea221daf14

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: ae5cbb2842c7a31a8ec929bf99894df67b7e8d6e1b063b5f3e17fcb29804a1ce

SO_HO_HOS06_S_reuse__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 160fb7615456457124de138e3345b72738dcc760541ebb78a9499518cc0d1d87

Distinct quantity/resource IDs; no transfer is adopted into this comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: 5d93292e46a17dca970fe2011636bf0c9dc2ed9e7b7448a943e37638e13aabed

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: 06ac0ae5be77b122c05ef886ae4257c063acf9b25cae6a5a65cd4809e03b946f

SO_HO_HOS06_S_reuse__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 160fb7615456457124de138e3345b72738dcc760541ebb78a9499518cc0d1d87

Distinct quantity/resource IDs; no transfer is adopted into this comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: 52028b293c8e8da683d8c2cdffb6709b3572c85c1eba99b4540e1b0007d53dd7

Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: fadc0971baa518f8515e895ab197289d02cc308413fd1a95f341cf280c13f3ab

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: 8b2bfb9ed10b34dcb679c9beed579713efc81b4ffcade8f4b512788295cdce68

SO_HO_HOS06_S_reuse__main__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: 160fb7615456457124de138e3345b72738dcc760541ebb78a9499518cc0d1d87

Distinct quantity/resource IDs; no transfer is adopted into this comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 6

Native pointer: /joint_analysis/comparisons/2/bound_uses/5; canonical SHA-256: 33a0212d98b6b7d2cbfa1e9d353e775ec271d925d9a6c73495839013d057a998

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/bound_id; canonical SHA-256: 40635d3e7f3b937894529c09a2781692b387308be6a7f1341b4681248b717abd

SO_HO_HOS06_S_reuse__main__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/reason; canonical SHA-256: 160fb7615456457124de138e3345b72738dcc760541ebb78a9499518cc0d1d87

Distinct quantity/resource IDs; no transfer is adopted into this comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/validity_region; canonical SHA-256: 9ca5e8634604660045ef04b6cc2d40af30390e65c2e248ea0e0cc3f23513ff28

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 7

Native pointer: /joint_analysis/comparisons/2/bound_uses/6; canonical SHA-256: 6eb4bfa126c770f1e26e8ca1ee36a1b4b9f45d5aa82e6ff05da8aa294f5b0e3c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/bound_id; canonical SHA-256: d27979fbb4ff540b828b9bcf3eb65ff7df3be3f55e99207f18815dd518826fd2

SO_HO_HOS06_S_reuse__main__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/validity_region; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 8

Native pointer: /joint_analysis/comparisons/2/bound_uses/7; canonical SHA-256: ac48554815517e826f99f9b09409663570b7822953c49763b76569de9ccdf987

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/bound_id; canonical SHA-256: 62c122f2bb12b92af4bfb00323b7590c0619e3e536669a423a6167881d359cc3

SO_HO_HOS06_S_reuse__main__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/validity_region; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 9

Native pointer: /joint_analysis/comparisons/2/bound_uses/8; canonical SHA-256: 209141009788d1201bf55c833ee0329a4bc2fce365ee9e5a50775c6383db622a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/adopted_region; canonical SHA-256: 34d3d4da332a12d3d22d8cb38f3e57f46e4071907d313de39d3d2482e3a6a1ff

Comparison region: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND Bound validity: ((Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.", "region_ref": null}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/bound_id; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/mapping_proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/mapping_proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/reason; canonical SHA-256: 39075facfaa30b48154191817c4d268bcf1b40e155c24e58e57896bb0adced1b

Exact NH=0 upper from the complete finite gradient-only SAME algorithm, Ng<=Cgf; no free gradient calls.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/8/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 10

Native pointer: /joint_analysis/comparisons/2/bound_uses/9; canonical SHA-256: 04488b17e312197ee4c63a727cf338483cfdc6d197d53527a0f635f5afa9e014

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/adopted_region; canonical SHA-256: 2655b3ac270311b5929c1e225dc41442bf730b7eca0ebfe25eefb4a9e34ba326

Comparison region: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND Bound validity: ((Unchanged target r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.", "region_ref": null}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/bound_id; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/mapping_proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/mapping_proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/reason; canonical SHA-256: af328847c08b08fe3c037cf947c44e9ab10012af1047efb5a1d6c622a4d4af69

Resource NH>=0 on every execution path; no hypothesis discrimination or output restriction is required.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/9/validity_region; canonical SHA-256: 46f621275f85d7a8e0a6cc175d6eb0bbeeed84077a832b2c0dd532e0cc20c813

(Unchanged target r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 11

Native pointer: /joint_analysis/comparisons/2/bound_uses/10; canonical SHA-256: e60fa1950f0dbc25f3b71bbaf2536c0b85008f40919c403cb9a05f2f139bbed9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/10/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/10/bound_id; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/10/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/10/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/10/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/10/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/10/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/10/validity_region; canonical SHA-256: 3355a6bae6f9d2e2849259ec7981722027e22977effd417adce5cab45da08c9a

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND (Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 12

Native pointer: /joint_analysis/comparisons/2/bound_uses/11; canonical SHA-256: 6bfd37e22e3718d15e00af10ffab77c88a3f937a1475ce518e2e0869d19de9fe

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/11/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/11/bound_id; canonical SHA-256: 9625661fb8c53c6c9524b366b157ae48b6e2a0c3a09535bd0ef568a6f4b2f7e2

SO_HO_HOS06_S_reuse__main__b12

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/11/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/11/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/11/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/11/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/11/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/11/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 13

Native pointer: /joint_analysis/comparisons/2/bound_uses/12; canonical SHA-256: a02c1b895f9ed96963987a1982a6919a6eec80b2410927127b96ea505f9af5c1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/12/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/12/bound_id; canonical SHA-256: a5835deee3b5251752a48d50c4b66ff5e9c708cc235efb44900cb2a26a13e0a3

SO_HO_HOS06_S_reuse__main__b13

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/12/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/12/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/12/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/12/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/12/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/12/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 14

Native pointer: /joint_analysis/comparisons/2/bound_uses/13; canonical SHA-256: d858717865e266b9fd762134bd869fa7dcaab7f9e179fcc296aea6f46c6d05dd

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/13/adopted_region; canonical SHA-256: 530af9b10790ef7558742b3d3219945348d067b89dfbfec230b05f7697377e30

No literal quantity merge; its valid implications are explicitly represented.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/13/bound_id; canonical SHA-256: 9d49ad9e5587ad73868b47fb1678457a90d0aebac4d4c8f6a9337213c93b7130

SO_HO_HOS06_S_reuse__main__b14

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/13/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/13/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/13/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/13/reason; canonical SHA-256: 1444dcecd03c25f4a423369a1965d0a15074a1104c14442e880d4fb998022d5b

A same-algorithm joint necessary sum halfspace from the retained q1 lower; the literal joint quantity differs in scalar rows, whose original total lower remains active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/13/validity_region; canonical SHA-256: 569e71e6eb987fb6ffa0150dac91ee49ffba28e20fb382ed2551be6230a4d9d4

Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND (Exactly the unchanged old b4/r3 source guard, intersected with receiving native r2 where used: $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 9d59b0de99e609bc807e65ba4424f4f2ac70a4c5ffcd058edbbb9735deb9df9a

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: 85eb4991d293c8fbfd6659221164dfdc555008ea60d463e5d88f2c580d574cba

All positive publicstructure with independentpositiveepsg,epsH in the unchangedtargetwindow.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: 7349f631714eeac95922e9179dfb88c87d9ed22140478995bdb15cb67919add4

Returning⊥ is allowedonly within the failurebudget; success>=2/3 and all paths have finiteNg cap.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: ab56c88c1d33fe48ab3eb01e9ac0ee6ef8a5404d10dad1208d586dfca54c5807

exact0; multiplicative ratio undefined

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 1015a7c148f9a8ed8839b971ccda86dc10927828d9733e9831804018d0bf6a31

0 by nonnegativity

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: b86a9396f9d319e6d7646535fe58877920a505bb48b2a087865f9c1120b61018

This closes onlythe Hessian coordinate. It does not make gradient queries free or solve the jointPareto frontier.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: 08c427cad3ff6a8de1d9c5fa8294158c8fe694d767dbb91b6b2481deedbfdfbc

0 Hessian oracle calls withNg<=C_gf

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 844c6ad7600ae493f3baf208f5d3d035c7e1268af927c80e054e1297e837fa4b

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 3968e1e5f1c6b6d64218ce4a0fcc2e79334a58e97c5734a693f4059944dc9d38

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: 2e0b0961bcb9588880af67a9e47bb7bbd028786437ad7670deabb4c190f358eb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 1e934f1f09936a6f084a5024a8b3cd5608e612b58ae62bcac1eb36695613de70

Comparison region: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND Bound validity: (Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$))

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 8b2bfb9ed10b34dcb679c9beed579713efc81b4ffcade8f4b512788295cdce68

SO_HO_HOS06_S_reuse__main__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 97a33366577c95c065d78cc360102143a5cea43f5e9692782dfdd71e5a369d4e

Retained one-algorithm achievable vector, with both coordinates charged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: 1c2e75e79b772518360b6c39ddf64f21394eda7de4c455fe1bf3e0747b82688d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: e612186e188a327317997c81733ff7842f8b69f700c881a702d263edfb498dcb

The literal q1 row is not directly included in q4; its guard-preserving consequence IS adopted through quantity-matched b14 on r2 intersect r3.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 06ac0ae5be77b122c05ef886ae4257c063acf9b25cae6a5a65cd4809e03b946f

SO_HO_HOS06_S_reuse__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: 3655b8d67967a521c24fbdff9622b95345f6585cac26c00929d8384e7d6fa086

The previous unresolved/no-transfer note is superseded: HOS06_RESOURCE_PROJECTION_CLOSURE_20261116 proves that this same-algorithm total lower gives the q4 necessary sum halfspace, and native c4 explicitly includes b14. The q1/q4 IDs are not identified and the original r3 source guard is retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 52028b293c8e8da683d8c2cdffb6709b3572c85c1eba99b4540e1b0007d53dd7

Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: f20fb82a3fe8ef14a70a1cedd1b99a4613b09512e40339629588c7489b57664b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 0a58feb45b19a7951494a9afc94f964801f2fa6fb3fa54c1d66724d397494a0c

No literal scalar-row merge. Original same-algorithm joint upper is separately b5; new gradient-only same-algorithm upper is b11.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: e2bea876d5b01adf95355fcfa3d5a1eb1c0f18cb82989aef4da6c94606c19fe2

SO_HO_HOS06_S_reuse__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 1028ceb3e15c0a9ebbb83bbb1fe3757cb1230224d9eabc409c17f3f33efdbdc0

Separate scalar minima are not combined. The existing b5 already represents its actual old simultaneous caps; the new witnessb11 is a different fully proved algorithm. Typed projection obligations retain their valid dominated consequences, without a claim that scalar budgets determine arbitrary Pareto vectors.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: 0ed3e725677249da1a49dfe6b9f1a5c333b873b617435088925c07e66cd08f0e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: 0a58feb45b19a7951494a9afc94f964801f2fa6fb3fa54c1d66724d397494a0c

No literal scalar-row merge. Original same-algorithm joint upper is separately b5; new gradient-only same-algorithm upper is b11.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: 1028ceb3e15c0a9ebbb83bbb1fe3757cb1230224d9eabc409c17f3f33efdbdc0

Separate scalar minima are not combined. The existing b5 already represents its actual old simultaneous caps; the new witnessb11 is a different fully proved algorithm. Typed projection obligations retain their valid dominated consequences, without a claim that scalar budgets determine arbitrary Pareto vectors.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: 9212f572ece3e35c69cf35b5cfb73b4d3c444355977a998ac87567ec7c50c47f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: 0a58feb45b19a7951494a9afc94f964801f2fa6fb3fa54c1d66724d397494a0c

No literal scalar-row merge. Original same-algorithm joint upper is separately b5; new gradient-only same-algorithm upper is b11.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: ae5cbb2842c7a31a8ec929bf99894df67b7e8d6e1b063b5f3e17fcb29804a1ce

SO_HO_HOS06_S_reuse__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: 1028ceb3e15c0a9ebbb83bbb1fe3757cb1230224d9eabc409c17f3f33efdbdc0

Separate scalar minima are not combined. The existing b5 already represents its actual old simultaneous caps; the new witnessb11 is a different fully proved algorithm. Typed projection obligations retain their valid dominated consequences, without a claim that scalar budgets determine arbitrary Pareto vectors.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/bound_uses/5; canonical SHA-256: 2a83852286418afcffc417f616b417fb1ef001cdef1bd7432c702fbb84f34de2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/bound_id; canonical SHA-256: 40635d3e7f3b937894529c09a2781692b387308be6a7f1341b4681248b717abd

SO_HO_HOS06_S_reuse__main__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/reason; canonical SHA-256: 8bdff6bb0e57c3193ba36b45608a4a57884426bdcf8967c039ea02841ee8954b

The literalq2 scalar row is notmerged. Its directed implications are proved and adopted through quantity-matched b7(sum) andb8(joint necessaryhalfspace).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/validity_region; canonical SHA-256: 9ca5e8634604660045ef04b6cc2d40af30390e65c2e248ea0e0cc3f23513ff28

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 7

Native pointer: /joint_analysis/comparisons/3/bound_uses/6; canonical SHA-256: 6eb4bfa126c770f1e26e8ca1ee36a1b4b9f45d5aa82e6ff05da8aa294f5b0e3c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/bound_id; canonical SHA-256: d27979fbb4ff540b828b9bcf3eb65ff7df3be3f55e99207f18815dd518826fd2

SO_HO_HOS06_S_reuse__main__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/validity_region; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 8

Native pointer: /joint_analysis/comparisons/3/bound_uses/7; canonical SHA-256: 7a3628ab7e74228c20f4cbc2699c2a205ede25143f0175d7e9ae29eb62762729

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/adopted_region; canonical SHA-256: fcc6f44b69fa03299f6adc857ed6422846464f6f87ded8291ce9b4d98b6ca350

Comparison region: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND Bound validity: (Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Exactlyr7; outside r7 this halfspace is not used.", "region_ref": null}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/bound_id; canonical SHA-256: 62c122f2bb12b92af4bfb00323b7590c0619e3e536669a423a6167881d359cc3

SO_HO_HOS06_S_reuse__main__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/reason; canonical SHA-256: 885d853401ec3ccbab4f8357e72503b67e69ff41fb4a7160773ebac653feb1ab

Quantity-matched joint necessary Bg>=Lg, only on r7 intersect this comparison, with arbitrary other finite budget.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/validity_region; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 9

Native pointer: /joint_analysis/comparisons/3/bound_uses/8; canonical SHA-256: e0e8d6af0ef7aed25362f35742eecb9bff5b7ed3fc626b08df28916b679b57a6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/bound_id; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/8/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 10

Native pointer: /joint_analysis/comparisons/3/bound_uses/9; canonical SHA-256: 247942ab70058a0485cdd5cfb3ffa41f0fe6c6647569cee7be771211a08afa4b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/bound_id; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/9/validity_region; canonical SHA-256: 46f621275f85d7a8e0a6cc175d6eb0bbeeed84077a832b2c0dd532e0cc20c813

(Unchanged target r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 11

Native pointer: /joint_analysis/comparisons/3/bound_uses/10; canonical SHA-256: 8525b9c30346f952482249603537da6540dba37b81ec994b63acadb0cea51106

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/adopted_region; canonical SHA-256: 1af7d154c2600aa75c38d5e92157d2e45771b6f8749644d03a4c4c2abccc3eea

Comparison region: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND Bound validity: (Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND (Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.", "region_ref": null}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/bound_id; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/mapping_proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/mapping_proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/reason; canonical SHA-256: 14b87591c2828132dea6275fdd8a8e42bdb585f749e743214fb64ddba79c6d28

One fully proved SAME algorithm attains joint(Cgf,0), never a pair of independently optimal marginal costs.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/10/validity_region; canonical SHA-256: 3355a6bae6f9d2e2849259ec7981722027e22977effd417adce5cab45da08c9a

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND (Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 12

Native pointer: /joint_analysis/comparisons/3/bound_uses/11; canonical SHA-256: 6bfd37e22e3718d15e00af10ffab77c88a3f937a1475ce518e2e0869d19de9fe

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/11/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/11/bound_id; canonical SHA-256: 9625661fb8c53c6c9524b366b157ae48b6e2a0c3a09535bd0ef568a6f4b2f7e2

SO_HO_HOS06_S_reuse__main__b12

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/11/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/11/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/11/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/11/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/11/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/11/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 13

Native pointer: /joint_analysis/comparisons/3/bound_uses/12; canonical SHA-256: a02c1b895f9ed96963987a1982a6919a6eec80b2410927127b96ea505f9af5c1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/12/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/12/bound_id; canonical SHA-256: a5835deee3b5251752a48d50c4b66ff5e9c708cc235efb44900cb2a26a13e0a3

SO_HO_HOS06_S_reuse__main__b13

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/12/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/12/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/12/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/12/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/12/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/12/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 14

Native pointer: /joint_analysis/comparisons/3/bound_uses/13; canonical SHA-256: 556265db41dd226114b39d726658d98da66d586d210f2192d1308e3c8f27ed06

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/13/adopted_region; canonical SHA-256: 89b0f94fef8dddf7da8f97ff56de6cf1f2f285435e53f90e206656a8350b46a9

Comparison region: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND Bound validity: (Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND (Exactly the unchanged old b4/r3 source guard, intersected with receiving native r2 where used: $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Exactly unchanged b4/r3, intersected with the native target.", "region_ref": "SO_HO_HOS06_S_reuse__main__r3"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/13/bound_id; canonical SHA-256: 9d49ad9e5587ad73868b47fb1678457a90d0aebac4d4c8f6a9337213c93b7130

SO_HO_HOS06_S_reuse__main__b14

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/13/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/13/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/13/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/13/reason; canonical SHA-256: 71841087abe13f367bed2db533cefcf7f97618ab21c49acb34052df0ef77d294

Quantity-matched necessary joint sum constraint from retained q1/b4 through HOS06_RESOURCE_PROJECTION_CLOSURE_20261116; only on r3 intersect this comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/13/validity_region; canonical SHA-256: 569e71e6eb987fb6ffa0150dac91ee49ffba28e20fb382ed2551be6230a4d9d4

Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND (Exactly the unchanged old b4/r3 source guard, intersected with receiving native r2 where used: $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: a15cb58d7f378de8151a26e170b60aa7a828001034d535d7d63cf3dd07026311

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: f3c3398ead85c1e041bcb5b475cdf97fc8f78a4431d83174af50d31e9a1b66ca

Each upper vector is one actual algorithm; separate scalar minima cannot be combined.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: b1f8a08bbb5b245e216d9851e8e7f40136e2dece1af8139c503e385453ba4cd6

b8 is adopted only on r2 intersectr7; b14 only on r2 intersectr3. Their native claim guards and source dimension windows are retained.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/boundary_checks/2; canonical SHA-256: 48686eaf01ef325378cdebe884493753da1d6cea049608ef59678c06d0336b50

The q1 b4 consequence is explicitly adopted through b14 and its native transferproof; it is not an unresolved absence of transfer.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: acdf0cab8b25fce346fa055070ac156dc0af82d92cfabc4b88b84f0db9018c37

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/0; canonical SHA-256: 92ffedc715a1d5ffe8f98e16298777d6cfe08037922a53723da4b7eaf98b67a2

SO_HO_HOS06_S_reuse_p_360c30de02

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/1; canonical SHA-256: 3b62aa9f90972f46cdb02143a98e47c210dd4e56a049b65462248b824d871162

SO_HO_HOS06_S_reuse_p_58c6dbfa8a

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/2; canonical SHA-256: 7033b07143ee6c8e8ab1cc4ee6945216f9f3f8948a64e7cfa71f84d6af3272be

SO_HO_HOS06_S_reuse_p_fb9a0c2872

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/3; canonical SHA-256: 6d3482225c13218e1267c0b2cfd93d4d7a0bc45ca10b2f4af37c1db25d199c1b

SO_HO_HOS06_S_reuse_p_26aa16ff5b

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/4; canonical SHA-256: d563822a02ff1cd27784f53df621d6ca99707d5b602115ff5a93bf409fe81d1f

SO_HO_HOS06_S_reuse_p_1bfb19894a

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/5; canonical SHA-256: ed68a704c652d42876f81a0d09952ff55da2e27943967e15748f7d748bfebc8d

SO_HO_HOS06_S_reuse_p_45d020550f

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: acdf0cab8b25fce346fa055070ac156dc0af82d92cfabc4b88b84f0db9018c37

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/0; canonical SHA-256: 92ffedc715a1d5ffe8f98e16298777d6cfe08037922a53723da4b7eaf98b67a2

SO_HO_HOS06_S_reuse_p_360c30de02

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/1; canonical SHA-256: 3b62aa9f90972f46cdb02143a98e47c210dd4e56a049b65462248b824d871162

SO_HO_HOS06_S_reuse_p_58c6dbfa8a

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/2; canonical SHA-256: 7033b07143ee6c8e8ab1cc4ee6945216f9f3f8948a64e7cfa71f84d6af3272be

SO_HO_HOS06_S_reuse_p_fb9a0c2872

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/3; canonical SHA-256: 6d3482225c13218e1267c0b2cfd93d4d7a0bc45ca10b2f4af37c1db25d199c1b

SO_HO_HOS06_S_reuse_p_26aa16ff5b

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/4; canonical SHA-256: d563822a02ff1cd27784f53df621d6ca99707d5b602115ff5a93bf409fe81d1f

SO_HO_HOS06_S_reuse_p_1bfb19894a

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/5; canonical SHA-256: ed68a704c652d42876f81a0d09952ff55da2e27943967e15748f7d748bfebc8d

SO_HO_HOS06_S_reuse_p_45d020550f

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 70880f75ab1f2dbf9e7c602963d070ce8698af0d92b1003d672fba08fd2358f7

Paretofrontier stillunclosed

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: d3bceab639ad757da81352d15e715de5d4049570c98e04c6dbb6c4e8964ce6f1

Intersection of necessary Bg>=Lg on r7 and Bg+BH>=Lold on r3; no constraint is extended outside its guard.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: cb53323b520146891c3731865de835443087dc6dd812c3d3f2afe3037a44af45

No matchinggradient optimum or completePareto surface; no mixingcoordinates ofdifferentwitnesses.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: c2c7d17a635854026a11b43130f568e40e2f78f0a6ccd90b53613803e1f76072

Upward closure of two separately proved same-algorithm budgetvectors: oldvector and(C_gf,0).

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: 7fed3811426704555b82aa4ee64a82283c7789bea63eb220ab1677db39d32f83

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: 6f805ef0e520107ef32b0995e1538e3d911b57944665ce6a37982ab2f5e761b6

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: 1168cd3c49b7ce4cf5988a82e248b8416e64ef3fb7b9d92d872bf94150229a6e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: e2bea876d5b01adf95355fcfa3d5a1eb1c0f18cb82989aef4da6c94606c19fe2

SO_HO_HOS06_S_reuse__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: cd3938507660d747f1491410fe84a5aae693a56cfd8e2f66344432d3fa2ded84

Direct row belongs to another quantity or unadopted statement; any proved transfer is represented by its own bound ID.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: 17f7975cf7c560a6a731402b313b489e7c7485021b165837839ab3b46e706257

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: cd3938507660d747f1491410fe84a5aae693a56cfd8e2f66344432d3fa2ded84

Direct row belongs to another quantity or unadopted statement; any proved transfer is represented by its own bound ID.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/bound_uses/2; canonical SHA-256: 89de590ff6f4879bd77a8b6c6da206dee684d68eda4b74a9c8083daeff542523

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/adopted_region; canonical SHA-256: 612effa8a25c39c0c843e829a4b7b20eb4c8d3683575b376fed874371bd3a722

Comparison region: (Native r7 (all positive structural budgets,d>=1,epsilon_H<=1,epsilon_g<=min{1,sigma1/8,beta/4,M2/12,G/6,Delta/(4-2sqrt(3))}).) AND Bound validity: (Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Unchanged originalr2, which containsr7.", "region_ref": null}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/bound_id; canonical SHA-256: ae5cbb2842c7a31a8ec929bf99894df67b7e8d6e1b063b5f3e17fcb29804a1ce

SO_HO_HOS06_S_reuse__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/reason; canonical SHA-256: a79d2f14db7a67252089ba2bee4146fbf4ee4056e36418eb9a9625df71ffd8f3

Included as an explicit quantity-matched native participant.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/bound_uses/3; canonical SHA-256: bc4a94ff4116a3fa8f604d833b7c232e96a183cacde0105bbe0878f9d17ee60b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/adopted_region; canonical SHA-256: 55c1ea9a91852716f4cb368fcf845ab04119a71f1e56c1c704a2652b827d26ab

Comparison region: (Native r7 (all positive structural budgets,d>=1,epsilon_H<=1,epsilon_g<=min{1,sigma1/8,beta/4,M2/12,G/6,Delta/(4-2sqrt(3))}).) AND Bound validity: (Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "The unchanged old r3 source guard, intersected with this comparison's exact r7. Never used on r7 minus r3.", "region_ref": "SO_HO_HOS06_S_reuse__main__r3"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/bound_id; canonical SHA-256: 06ac0ae5be77b122c05ef886ae4257c063acf9b25cae6a5a65cd4809e03b946f

SO_HO_HOS06_S_reuse__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/reason; canonical SHA-256: e44c2710e1a5ee6e03194dd30bf7925f8eb80f7df4a9205cc54d3385be579fe9

A compatible old total lower remains in the maximum on its exact source-valid overlap.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/validity_region; canonical SHA-256: 52028b293c8e8da683d8c2cdffb6709b3572c85c1eba99b4540e1b0007d53dd7

Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)

#### Native item 5

Native pointer: /joint_analysis/comparisons/4/bound_uses/4; canonical SHA-256: de66bc0939fb7d2bfbb44cc23b4eeb47957c456b73f780e06492490454982d1d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/bound_id; canonical SHA-256: 8b2bfb9ed10b34dcb679c9beed579713efc81b4ffcade8f4b512788295cdce68

SO_HO_HOS06_S_reuse__main__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/reason; canonical SHA-256: cd3938507660d747f1491410fe84a5aae693a56cfd8e2f66344432d3fa2ded84

Direct row belongs to another quantity or unadopted statement; any proved transfer is represented by its own bound ID.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/validity_region; canonical SHA-256: 86ced3f6b582728de0c37d3954b348d37e72e613b6166617a449c25932785e9b

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 6

Native pointer: /joint_analysis/comparisons/4/bound_uses/5; canonical SHA-256: 741c112f1a326013acb7f530ac970de82da6e33ed9d12c9297d6cf017740e33b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/bound_id; canonical SHA-256: 40635d3e7f3b937894529c09a2781692b387308be6a7f1341b4681248b717abd

SO_HO_HOS06_S_reuse__main__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/mapping_proof_refs; canonical SHA-256: 65f1f3b9952a378b816ed7da7d5def3470773a2084d80268452c63832a0584f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: 8b9ff11578e738aa89cca94088565503bf71f5ed015e1429e1cae6c857760bd5

SO_HO_HOS06_S_reuse__main__p1

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/reason; canonical SHA-256: cd3938507660d747f1491410fe84a5aae693a56cfd8e2f66344432d3fa2ded84

Direct row belongs to another quantity or unadopted statement; any proved transfer is represented by its own bound ID.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/5/validity_region; canonical SHA-256: 9ca5e8634604660045ef04b6cc2d40af30390e65c2e248ea0e0cc3f23513ff28

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 7

Native pointer: /joint_analysis/comparisons/4/bound_uses/6; canonical SHA-256: 92fb4406af490b536c8346beaba336d042377376a0f1a3f6d12175794424bd4c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/adopted_region; canonical SHA-256: 25c304843a80128fb2eede6c35be8ab2337029cdb654251c5891bea537538364

Comparison region: (Native r7 (all positive structural budgets,d>=1,epsilon_H<=1,epsilon_g<=min{1,sigma1/8,beta/4,M2/12,G/6,Delta/(4-2sqrt(3))}).) AND Bound validity: (Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Exactr7.", "region_ref": null}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/bound_id; canonical SHA-256: d27979fbb4ff540b828b9bcf3eb65ff7df3be3f55e99207f18815dd518826fd2

SO_HO_HOS06_S_reuse__main__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/reason; canonical SHA-256: 43870d598e6a3b973c97f795fb8d221911479aabc16a060d8da2c4d602879ef4

Quantity-matched total lower follows from original robust Ng>=Lg and Ng+NH>=Ng, only on r7 intersect this comparison.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/6/validity_region; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 8

Native pointer: /joint_analysis/comparisons/4/bound_uses/7; canonical SHA-256: ac48554815517e826f99f9b09409663570b7822953c49763b76569de9ccdf987

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/bound_id; canonical SHA-256: 62c122f2bb12b92af4bfb00323b7590c0619e3e536669a423a6167881d359cc3

SO_HO_HOS06_S_reuse__main__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/7/validity_region; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 9

Native pointer: /joint_analysis/comparisons/4/bound_uses/8; canonical SHA-256: e0e8d6af0ef7aed25362f35742eecb9bff5b7ed3fc626b08df28916b679b57a6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/bound_id; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/8/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 10

Native pointer: /joint_analysis/comparisons/4/bound_uses/9; canonical SHA-256: 247942ab70058a0485cdd5cfb3ffa41f0fe6c6647569cee7be771211a08afa4b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/bound_id; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/9/validity_region; canonical SHA-256: 46f621275f85d7a8e0a6cc175d6eb0bbeeed84077a832b2c0dd532e0cc20c813

(Unchanged target r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 11

Native pointer: /joint_analysis/comparisons/4/bound_uses/10; canonical SHA-256: e60fa1950f0dbc25f3b71bbaf2536c0b85008f40919c403cb9a05f2f139bbed9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/bound_id; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/10/validity_region; canonical SHA-256: 3355a6bae6f9d2e2849259ec7981722027e22977effd417adce5cab45da08c9a

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND (Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 12

Native pointer: /joint_analysis/comparisons/4/bound_uses/11; canonical SHA-256: 6427a39c213789a957dd2edce0fc33537959a5ad335ea05731ee7ec377ab1607

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/11/adopted_region; canonical SHA-256: 8571b9fa47e70cf9b0d17b7c7a3370cedb097026612d33d780bf67ba5824e90c

Comparison region: (Native r7 (all positive structural budgets,d>=1,epsilon_H<=1,epsilon_g<=min{1,sigma1/8,beta/4,M2/12,G/6,Delta/(4-2sqrt(3))}).) AND Bound validity: ((Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.", "region_ref": null}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/11/bound_id; canonical SHA-256: 9625661fb8c53c6c9524b366b157ae48b6e2a0c3a09535bd0ef568a6f4b2f7e2

SO_HO_HOS06_S_reuse__main__b12

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/11/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/11/mapping_proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/11/mapping_proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/11/reason; canonical SHA-256: 6361a71f0c165725af0356bfff60fc72d604327be9843d10943250beed5919ce

Sum upper of the SAME finite gradient-only witness: Ng+NH=Ng<=Cgf on its proved native target.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/11/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 13

Native pointer: /joint_analysis/comparisons/4/bound_uses/12; canonical SHA-256: a02c1b895f9ed96963987a1982a6919a6eec80b2410927127b96ea505f9af5c1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/12/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/12/bound_id; canonical SHA-256: a5835deee3b5251752a48d50c4b66ff5e9c708cc235efb44900cb2a26a13e0a3

SO_HO_HOS06_S_reuse__main__b13

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/12/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/12/mapping_proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/12/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/12/mapping_proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/12/reason; canonical SHA-256: d0d0645a2c0f18ee40435938a7eede717693488ed4235777ad4c49b802338f84

The literal native quantity IDs differ; the directed implications are explicitly judged in v2 resource_projection obligations and represented by quantity-matched b6/b7/b8/b9/b10/b11/b12/b13. Never identify their separate infima or combine different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/12/validity_region; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 14

Native pointer: /joint_analysis/comparisons/4/bound_uses/13; canonical SHA-256: d858717865e266b9fd762134bd869fa7dcaab7f9e179fcc296aea6f46c6d05dd

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/13/adopted_region; canonical SHA-256: 530af9b10790ef7558742b3d3219945348d067b89dfbfec230b05f7697377e30

No literal quantity merge; its valid implications are explicitly represented.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/13/bound_id; canonical SHA-256: 9d49ad9e5587ad73868b47fb1678457a90d0aebac4d4c8f6a9337213c93b7130

SO_HO_HOS06_S_reuse__main__b14

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/13/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/13/mapping_proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/13/mapping_proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/13/reason; canonical SHA-256: 1444dcecd03c25f4a423369a1965d0a15074a1104c14442e880d4fb998022d5b

A same-algorithm joint necessary sum halfspace from the retained q1 lower; the literal joint quantity differs in scalar rows, whose original total lower remains active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/13/validity_region; canonical SHA-256: 569e71e6eb987fb6ffa0150dac91ee49ffba28e20fb382ed2551be6230a4d9d4

Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND (Exactly the unchanged old b4/r3 source guard, intersected with receiving native r2 where used: $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: 07e082663d1b1e480be1467d670e3321bb84ec94a4b69cb6835510ecb2b673af

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: f84bba8ef5053c930d62b6a8df954b2cd5a964020ebf6b757a099d931393efc0

r7 isexact inheritedsourceguard; no dimension restrictionadded.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/boundary_checks/1; canonical SHA-256: 244772b4f35f0d4e4c49fe4f32315f0481d7cabf9da35f8397529f8a9cc1a6e7

Thisquantity-matchedtotal comparison extends registrationofthe provenprojection, not thegradientmodel.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: acdf0cab8b25fce346fa055070ac156dc0af82d92cfabc4b88b84f0db9018c37

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/constant_dependencies/0; canonical SHA-256: 92ffedc715a1d5ffe8f98e16298777d6cfe08037922a53723da4b7eaf98b67a2

SO_HO_HOS06_S_reuse_p_360c30de02

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/constant_dependencies/1; canonical SHA-256: 3b62aa9f90972f46cdb02143a98e47c210dd4e56a049b65462248b824d871162

SO_HO_HOS06_S_reuse_p_58c6dbfa8a

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/constant_dependencies/2; canonical SHA-256: 7033b07143ee6c8e8ab1cc4ee6945216f9f3f8948a64e7cfa71f84d6af3272be

SO_HO_HOS06_S_reuse_p_fb9a0c2872

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/constant_dependencies/3; canonical SHA-256: 6d3482225c13218e1267c0b2cfd93d4d7a0bc45ca10b2f4af37c1db25d199c1b

SO_HO_HOS06_S_reuse_p_26aa16ff5b

#### Native item 5

Native pointer: /joint_analysis/comparisons/4/constant_dependencies/4; canonical SHA-256: d563822a02ff1cd27784f53df621d6ca99707d5b602115ff5a93bf409fe81d1f

SO_HO_HOS06_S_reuse_p_1bfb19894a

#### Native item 6

Native pointer: /joint_analysis/comparisons/4/constant_dependencies/5; canonical SHA-256: ed68a704c652d42876f81a0d09952ff55da2e27943967e15748f7d748bfebc8d

SO_HO_HOS06_S_reuse_p_45d020550f

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: acdf0cab8b25fce346fa055070ac156dc0af82d92cfabc4b88b84f0db9018c37

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/fixed_parameters/0; canonical SHA-256: 92ffedc715a1d5ffe8f98e16298777d6cfe08037922a53723da4b7eaf98b67a2

SO_HO_HOS06_S_reuse_p_360c30de02

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/fixed_parameters/1; canonical SHA-256: 3b62aa9f90972f46cdb02143a98e47c210dd4e56a049b65462248b824d871162

SO_HO_HOS06_S_reuse_p_58c6dbfa8a

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/fixed_parameters/2; canonical SHA-256: 7033b07143ee6c8e8ab1cc4ee6945216f9f3f8948a64e7cfa71f84d6af3272be

SO_HO_HOS06_S_reuse_p_fb9a0c2872

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/fixed_parameters/3; canonical SHA-256: 6d3482225c13218e1267c0b2cfd93d4d7a0bc45ca10b2f4af37c1db25d199c1b

SO_HO_HOS06_S_reuse_p_26aa16ff5b

#### Native item 5

Native pointer: /joint_analysis/comparisons/4/fixed_parameters/4; canonical SHA-256: d563822a02ff1cd27784f53df621d6ca99707d5b602115ff5a93bf409fe81d1f

SO_HO_HOS06_S_reuse_p_1bfb19894a

#### Native item 6

Native pointer: /joint_analysis/comparisons/4/fixed_parameters/5; canonical SHA-256: ed68a704c652d42876f81a0d09952ff55da2e27943967e15748f7d748bfebc8d

SO_HO_HOS06_S_reuse_p_45d020550f

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: a7c91b02b6ca18da66e2c9171ad94e90974735435297f93a428075b4fe96c8de

Guarded quotient; no optimality claimed.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: 59ab67295da644d3024ead51e3e363d9b582b6ba48a3e8f48257ccf328acbaa8

max{Lg,Lold on the unchanged r3 overlap}; no old source-guard extension

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: 5253199183248b999f30eb32ed800c71bd4b9d8ff832c3a4b97b8125496f6126

The strongest registered compatible lower is retained on each valid overlap. Outside r3, only Lg is adopted; no complete total frontier is asserted.

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: 0b69a915b1a2b80c315d2266c4a2e09d1fe14e4a40876a349b297043a59fcdfc

min{U_old,C_gf}

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 76f29770b28294f0e6fdce3683eb8259d5095676716d4d57fff1137b8ad3fcea

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 9c471f8bd32cb9d0d4e1f7d1ad774aca53194bf9599824499c4001e1bd12ab49

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 9a5e7ae2f5fbd2e799e77e7fbbac9b26d3c797504725d5742491bb301c0d0f60

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 52d3370883aec631a42a0f7732c37470581fe39127691ac7dac24316b4ac0951

W_and_G

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 9c6cc761cbe0170e4c7a3d0b28485a89d61ebfd2abff78103538afbefd49b5c9

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/1; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/2; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/3; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: a44cee29c2ca3450829f3b9bf7ca19aad9df0c113271305443981003f2e2ed22

This layer tracks non-Hessian quantities. Lg in total and Bg>=Lg in joint budgets apply only on r7; the old total lower keeps r3. Hessian-coordinate exact zero is recorded separately. Gradient/total/Pareto sharpness and complements remain unclosed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 85774c720c539bc5f300c6e9ea465eb5b43d0543b0a18e292939a1a51bc4a235

r4 intersect r3 intersect r7

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 997ef396ab2d4d4f9dc3000dabae1619f0737ab43b0bd22ad618acb4f4ad4d30

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 6d3dc5105fc77c2d9b5a249ae49cfea4e013086989ffbd6233ff6e615f19ce92

W_not_G

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: af1f6c3e2462149d0ce4ca32c0470333e18c243567a6dada5fbd6adab1892b15

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/2; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: a44cee29c2ca3450829f3b9bf7ca19aad9df0c113271305443981003f2e2ed22

This layer tracks non-Hessian quantities. Lg in total and Bg>=Lg in joint budgets apply only on r7; the old total lower keeps r3. Hessian-coordinate exact zero is recorded separately. Gradient/total/Pareto sharpness and complements remain unclosed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 39d90a59384b121cfcdf5d7efc6a630e958aca1eb306a1582f998171d463c4ba

r4 intersect r3 minus r7

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 53248f3af95e7aa0e5708ab6b99f256d14340f727e3880f29b446d20b274fe67

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: ad735e00da351942c5f95ff25eca71fc1d4a15c88baf1f3fbb433a43009293ff

G_not_W

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 1ee6fb108625ae8511b0f40f0ada2c0d0a881511bfd3e20dcee5210163e89034

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/1; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/2; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: a44cee29c2ca3450829f3b9bf7ca19aad9df0c113271305443981003f2e2ed22

This layer tracks non-Hessian quantities. Lg in total and Bg>=Lg in joint budgets apply only on r7; the old total lower keeps r3. Hessian-coordinate exact zero is recorded separately. Gradient/total/Pareto sharpness and complements remain unclosed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: f83292b9d55a420b5537b112f39bed714f3b53bb6841c1138e21915eb8ee51b7

r4 intersect r7 minus r3

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: 36b920ea01d2111bdf4ed3381aba6cd232219a457b42325f4c7d67172916d2fc

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: b2063dbe4d29b0d8d43e79ff19360e21c0e6575651cd70e52503ddd638f6a92b

neither_W_nor_G

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 76bfeb0da1ef449cec0c5b747212fa5f213e16709d1f9ec3d8c3f4c97b6940e8

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/1; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: a44cee29c2ca3450829f3b9bf7ca19aad9df0c113271305443981003f2e2ed22

This layer tracks non-Hessian quantities. Lg in total and Bg>=Lg in joint budgets apply only on r7; the old total lower keeps r3. Hessian-coordinate exact zero is recorded separately. Gradient/total/Pareto sharpness and complements remain unclosed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 71cea1450dd0a7ec0aaaf6832ad0ac1b9d5f77976d54b912bc3157e1fef15c2e

r4 minus (r3 union r7)

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native item 5

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: b416db512a92bec99feccf0dd7fd043c9bf5574425769ffafa0aa618d23558bf

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: 22de28350907c906bc37f4c3af6427ef6df892c7d3c898d9f3b7cba78b93113a

hessian_coordinate_closed

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: 6a2ea4ebf6c3e625ed70d7927c0552676b2e94269a6d55f8ec14a4f500e21626

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: f5750685d50790e40f657d28021dd6af63f32e9ae58530330184ba51896d2cf4

The same finite gradient-only witness gives NH=0 and Ng<=Cgf. This resource-coordinate closure overlays, and does not close, the parameter partition for other quantities.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: 90a6416a050bc4df00317cfb718e43db00ce459cf0207b310c4afedd91cf9e29

Entire unchanged target r4: d>=1, positive public structure, 0<epsilon_g,epsilon_H<=1, quantity q3 only.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: a37f810e689615593e9d2dc2b09b816495459b45fb77b7ea61ca24b8cecfd0b2

Within the immutable r4 domain, the four Boolean combinations of membership in r3 and r7 are disjoint and exhaustive. Empty intersections are harmless. r3 retains its source's existential sufficient constants; this partition does not turn them into exact phase boundaries. Different quantities have separate missing-side assessments in each cell. The added hessian_coordinate_closed cell is an explicitly identified quantity-q3 overlay across that parameter partition; it asserts no closure for q1/q2/q4.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 85eb525bada88af8bc50786826a93cc1eeeea54355a54169d1ef60b7132be562

No part of r4 is omitted from bookkeeping. Scientific residual includes the lower sides stated above, endpoint/saturation refinements and sharp Pareto tradeoffs.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: ea4dd5a7887716ef34e62d9ec3a26d6b327b98def6f3207bc616a2f9e209292b

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: dc0abfb85069f3f36d68f7289b19f91bddb9c2a7f7d1a19a99cf67b60a4af829

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 67f6047c9e361b86818d265ceda7aa8581b4aa08cd27d05626b12a9096298b9f

Proof p1 verifies the sufficient guard and an explicit universal constant. This is a marginal rate lower bound, not merely an at-least-one-call statement. It does not improve the main total-query rate or close the gradient-coordinate gap.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: b16fe75c7652eb87e34bb8f99fd7c7e5bac7ebc007aa66f436d79a077708eb08

appendix_c_marginal_gradient

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: e8545da20e58a66626de24e5e32b6912ef8ab7332f596f2b64d1162680733a02

All of r7: fills a previously absent gradient-coordinate lower side.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 78752693101cdc44724a927640f2701e6a379698fa95a943fa2a6f3d081fe9c7

Same upper; lower sigma_1^2/(288*epsilon_g^2) on r7 only.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: f0bbacc8fee383ecee1cacba1757f707de8f3f87c1c570ffe9db19328f625b0c

q2: upper C*Lambda^4*B_g on r2; lower absent.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: bda27b2afb876172b0c0a5dd1ea838ce2e2ad37308063305b8729865ce8bf822

All q2 parameters outside r7, the q2 upper side, and q1/q3/q4 native brackets.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 7c55e7669d60c4afdf88ce72bdbc8f4bb3ba06dea338cd430e4fd554c85c59c0

r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 944e32b641cadc4ce035e21868580b4a2b4e0a4b61f319afa6da8e38355d3f46

Fix any positive theta, choose epsilon_g below all r7 thresholds, choose any epsilon_H in (0,1], and any integer d>=1. The two convex hypotheses force Omega(sigma_1^2/epsilon_g^2) gradient calls despite Hessian access.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 5a38b1db671a7c14e6756a8ceec21c2b10f0525ccaac264cf36fa6f5def5b44d

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: dbd8af335ee081837dee6133b5e86fd55f00ad4c9e572967bc7b128ab1a9dcbe

First annotation organizes existing records, explicit joint variables, guarded regions and unassessed complements. The scientific c2 lower edit is supported solely by appendix_c_marginal_gradient.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 0e79eafb61173a359b54a4d8eff8dd0b95ba8db286819d1d76472a50bd0d6d04

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native item 4

Native pointer: /joint_analysis/impact/1/comparison_ids/3; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: fcdd6190343c888ccea6f4d6f5a5f625d1457b21baf2334f1792d2ec063b793b

first_joint_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: bf37e3217d2448d19ab5ffeb99b50dfece92cdc6da3939e4c693b75a6547c252

None attributable to presentation.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 0734b380c23c53eaebadf0e85c24ac9b85dd85fbbe521886addb427d8f61321a

Those same scientific records are retained, with the separately justified b6 addition to c2.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 39a6d034dc4ba2c350a2287a0ba7456063a261c276f0321ecae46cbf67282b00

Frozen native envelopes and guards; no existing joint_analysis.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: da32b4a3b5f6a3b99f7bf09cba7abc34ee6c36957ee7c3a2225bb48257fe9db7

All unchanged scientific bounds, guards, statuses, resource identities and native parameter metadata.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 6cf7180ca395f59a4fd7562f6dd5c903713cb9a5a4df238ce5544bde34275311

r4 (the fixed reusable-handle contract): integer d>=1, positive Delta,beta,M_2,sigma_1,sigma_2,G, and independent 0<epsilon_g,epsilon_H<=1

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 2920c9250bae5274584b6c4ff4bcb2f11789788597188e3da1358971f1484f7a

c1 retains its source dimension guard; c3 and c4 retain their missing-side limitations.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 62115ce6955dc80a5ef2a25dad448b48f0b5fd9fe2d18b5e7a4af614dbe402b9

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 8a31fc6d6e086f99691052a1863b0ece18002eee64c14c55da86844c94784c3e

Completeprojectionproof plusindependentstochasticmean/samehandlecentraldifference/descent/unionboundproof. Allcosts andvalidationcounted.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: e2b3b307c0ed41f89da40cff113ce5f0b3a3b12b40a31186e3bcbaffa23ae2e1

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 3

Native pointer: /joint_analysis/impact/2/comparison_ids/2; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native item 4

Native pointer: /joint_analysis/impact/2/comparison_ids/3; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native item 5

Native pointer: /joint_analysis/impact/2/comparison_ids/4; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: ae22bc491d714c4553780b6f32a44aa0b524cae75a3c368c5bd52f99dc2b8ae6

HOS06_PROJECTION_AND_ZERO_HESSIAN_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: dd9fd4f251c7ceca279e46b6a955cce1d2b32b731950798562da8cd6cfd51c6b

q3positiveupperreplacedbyexact0; newregisteredtotal/jointlowercoverageonr7. NumericrateimprovementoftotalL_gmaybedominated.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 02e0dd3b088de72f9a1d1a024164267fe2f3dcb3b0e589fd561838838959b83f

DirectedtotalL_g/jointBg>=L_g onr7; exactq3=0 withsame-algorithmfiniteNgwitness; nofreecombinedmarginalminima.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 98389fd42830a206ff9bb37cd51481e5f5e0dc7d02a1b911013d826261eb3325

Ng flooronlyin q2; Hessianprojectionmissinglower; jointnecessarysideempty.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: ae88cd7a279cf69f0b2b4b906638216d5c38ec8c36bda350024a034a43b8717c

All immutable native contracts; all statements outside the explicit new guarded adoption remain unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 3c4e46b6c6943b35ab0df8f2081cea712553bf241dd394a15aec9e1d85df8162

Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 989fd6cb5cff13147f34d642d09447eb626e59a31812c1a05bd2abd491f6166e

Everyfinite successfulalgorithmhasNsum>=Ng; theexplicitcappedalgorithmhas(Ng,NH)<=(C_gf,0).

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: ca984cf51b4f38183a1ad1cb2b324543b7f90151c4110e893926f585d46ee5d9

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: e4f77f38555537082448312bca8e2618d950ced10eb13e11ebc95c0575dc2423

Publish separately proved directed resource projections: Ng>=Lg implies Ntotal>=Lg and Bg>=Lg, preserving r7; the old total lower also gives Bg+BH>=Lold only on its own r3. A complete same-algorithm finite gradient-estimation/central-difference/negative-curvature witness has NH=0 and public finite worst-path Ng, success at least 2/3. It closes only the Hessian coordinate and supplies its own joint vector; do not combine optimal coordinates from different algorithms. This revision addresses the preserved actual independent-review issues. Publication and typed projection obligations are explicit; every mathematical formula and adoption guard is verified against the exact native candidate, and historical effects are not reported as new frontier gains. Operational read priority after the preserved incomplete 40-tool review: finish the full prepared joint_analysis first, read exact decisive baseline parent objects completely where useful, and finish all evidence/resource/proof objects required by the review pack. Forty-eight tool calls allow completion of the same strict source, exact-reference, prepared-hash and six-check gates; no prior reading or approval is imported.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: e2b3b307c0ed41f89da40cff113ce5f0b3a3b12b40a31186e3bcbaffa23ae2e1

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native item 4

Native pointer: /joint_analysis/impact/3/comparison_ids/3; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native item 5

Native pointer: /joint_analysis/impact/3/comparison_ids/4; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 9970a0733458c88c93fdb33894f8f1605e70374f7aecf07bf7e16e2261a022fd

curated_feedback_SO_HO_HOS06_S_reuse_20261116_06ff2bdeb1

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 18cffcbcf2e22897c060a80d6c3f9f73795ea9a55cf85cea7ff1cbe6836abe22

r4 (the fixed reusable-handle contract): integer d>=1, positive Delta,beta,M_2,sigma_1,sigma_2,G, and independent 0<epsilon_g,epsilon_H<=1. Primary fixed-scale asymptotics vary d and both tolerances jointly. Native q1/q4 fix the six structural bounds; q2/q3 retain all nine tracked parameters and their explicit uniform formulas (their comparison constant_dependencies are empty). No quantity metadata is changed. The guarantee is main/g1, per-instance success >=2/3, with worst-case native vector (N_g,N_H), and exactly the declared q1 sum, q2 gradient, q3 Hessian and q4 vector projections.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 3327e74789a4ac22fc3fed09a7ee4457682ad6dce25392f59019847043e473bb

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 5f90876875623f265d6b6bed79bf7914614c3cb9e83d19b97c8f0a122afce369

Formalize the sufficient zero-query endpoint epsilon_g>=G and epsilon_H>=beta before changing native envelopes; it is disjoint from r7.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 373c006d98513160657a5d77a13c09e6819c6f5cb964fcfb0c2f19cf9bb3d15d

Sharper total-cost bounds at low dimension and coordinate bounds outside r7 remain unassessed; the targeted searches do not certify literature absence.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 3d49c4a1f0529de2629fb7df6775b58ae596113bcb2cc8cf7209bc29655b3e60

Optimize theexplicitC_gfgradientcost and comparePareto witness dominance;NH=0doesnotdetermine optimalNg. AnySPIDERrate transfer stillneedsitsown completeprecision/amplificationaccounting;thiscandidateadoptsnoSPIDERgradientrate.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: b8fb44566f5e0328d2c4d18a77a8f4887b4491216523e1fc049d3720f535a62d

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 1152a0f0397c2abbbd563796a574091bafff82cb84c1a13301728ae76b4b4d30

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: e2bea876d5b01adf95355fcfa3d5a1eb1c0f18cb82989aef4da6c94606c19fe2

SO_HO_HOS06_S_reuse__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: f019e8ad489c33a8fa334a2b00ae67259fcdc25af30e1f12c8d2c5f15e95267c

Conditionally retain the exact baseline quantity/resource/view/guarantee and guard; no recertification or scientific edit.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 74a0569e562da29e27c27d25c9904ce1bb0990885ff78bfce0d734b44346130b

SO_HO_HOS06_S_reuse__main__r2

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 3649d2614987e6ce0b159410be88b95e4b1de145cd9cd46005d797c2651903ca

Frozen baseline /bounds/0; unchanged historical source attribution, not fresh recertification.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 0c64ffe5a599a7a475cb7f5a3aa50c63ae37ce980304a1e9f330342ffff0d8d6

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 6672fb2f13aa3f49de2d795ece50fd9b7b8f470c9937d1c67e361451b6be25ae

SO_SRC_1e0f32cd5172fba2

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 74a0569e562da29e27c27d25c9904ce1bb0990885ff78bfce0d734b44346130b

SO_HO_HOS06_S_reuse__main__r2

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 8a5504dfea1fe243373b19bcbe94aef8a9ef852ab7728336ea3c312466451277

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 623595c59892a0850b8d1ef909b98f80d32f926574aa666fda1604e34592fd53

Old numeric upper/source attribution remains conditional history. Its selected_in_regimes removal is explicitly justified by the new same-algorithm finite Ng/NH0 proof and nonnegativity. This is an analyst-derived replacement judgment, not unchanged-baseline provenance or an append-only adoption exception.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: c788e0ee7ba6df972286dcfc11fcf0a51031b85d35da29d3030e5de110ad88dc

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 77d7a05099c0f628130f1ebbf732f9899046db3d4d7ffc5545e8a7ec141217ab

HOS06_HESSIAN_UPPER_REPLACEMENT_20261116

#### Native item 2

Native pointer: /joint_analysis/provenance/1/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: b8b16223304801095de577abefa3b9a80bbe44653c0a22e8f7308b1d10d152ed

Exact original b2/r2; no formula or validity guard change.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: c59f911cc6c62263e9d61b6a5bedc082323f49210ff4e8d32afa911dde38d0cb

Exact accepted /bounds/1 plus new full finite Hessian-free proof; old external source retained conditionally, not freshly verified.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 0c64ffe5a599a7a475cb7f5a3aa50c63ae37ce980304a1e9f330342ffff0d8d6

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: 6672fb2f13aa3f49de2d795ece50fd9b7b8f470c9937d1c67e361451b6be25ae

SO_SRC_1e0f32cd5172fba2

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: a716e1341e6b516c914799ac35ec052b9840b5c3d1fc596fa56138c59403256d

Same native q3/c3 on original r2; only best-envelope participation is replaced by exact zero.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 758faf406fe4761ecd341b6544272dc6bd1da2119fbc3faac22fe24f856c0b35

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: ae5cbb2842c7a31a8ec929bf99894df67b7e8d6e1b063b5f3e17fcb29804a1ce

SO_HO_HOS06_S_reuse__main__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: f019e8ad489c33a8fa334a2b00ae67259fcdc25af30e1f12c8d2c5f15e95267c

Conditionally retain the exact baseline quantity/resource/view/guarantee and guard; no recertification or scientific edit.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 74a0569e562da29e27c27d25c9904ce1bb0990885ff78bfce0d734b44346130b

SO_HO_HOS06_S_reuse__main__r2

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 09b0d6034fe025f714076e104a1074c76511d911aa8e8dcc63e8f2c120a0a1cc

Frozen baseline /bounds/2; unchanged historical source attribution, not fresh recertification.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 0c64ffe5a599a7a475cb7f5a3aa50c63ae37ce980304a1e9f330342ffff0d8d6

#### Native item 1

Native pointer: /joint_analysis/provenance/2/source_refs/0; canonical SHA-256: 6672fb2f13aa3f49de2d795ece50fd9b7b8f470c9937d1c67e361451b6be25ae

SO_SRC_1e0f32cd5172fba2

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 74a0569e562da29e27c27d25c9904ce1bb0990885ff78bfce0d734b44346130b

SO_HO_HOS06_S_reuse__main__r2

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 26e0a13e6b21ee4443d95d799dfb3ae596719abfc4adfb3f8625e3964163aeeb

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: 06ac0ae5be77b122c05ef886ae4257c063acf9b25cae6a5a65cd4809e03b946f

SO_HO_HOS06_S_reuse__main__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: f019e8ad489c33a8fa334a2b00ae67259fcdc25af30e1f12c8d2c5f15e95267c

Conditionally retain the exact baseline quantity/resource/view/guarantee and guard; no recertification or scientific edit.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: b8a21f30a1abe1b48a410d58ac6c43be361ac05b0392ab1bc3516cf5f64712c3

SO_HO_HOS06_S_reuse__main__r3

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 3a820b500a0df39b916a617a10aba0fee6453e1e236b40c8554eac80dffc2756

Frozen baseline /bounds/3; unchanged historical source attribution, not fresh recertification.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 0c64ffe5a599a7a475cb7f5a3aa50c63ae37ce980304a1e9f330342ffff0d8d6

#### Native item 1

Native pointer: /joint_analysis/provenance/3/source_refs/0; canonical SHA-256: 6672fb2f13aa3f49de2d795ece50fd9b7b8f470c9937d1c67e361451b6be25ae

SO_SRC_1e0f32cd5172fba2

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: b8a21f30a1abe1b48a410d58ac6c43be361ac05b0392ab1bc3516cf5f64712c3

SO_HO_HOS06_S_reuse__main__r3

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: 086b968927d216096d627b4ee3a3278c44a9cab7df190d62e4b7b6b01b7476b1

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: 8b2bfb9ed10b34dcb679c9beed579713efc81b4ffcade8f4b512788295cdce68

SO_HO_HOS06_S_reuse__main__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: f019e8ad489c33a8fa334a2b00ae67259fcdc25af30e1f12c8d2c5f15e95267c

Conditionally retain the exact baseline quantity/resource/view/guarantee and guard; no recertification or scientific edit.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 74a0569e562da29e27c27d25c9904ce1bb0990885ff78bfce0d734b44346130b

SO_HO_HOS06_S_reuse__main__r2

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: 67a2f473407f303ee26c9782e41a4d9d4a7ec60ba27c51904c82dd630b1d7e82

Frozen baseline /bounds/4; unchanged historical source attribution, not fresh recertification.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 0c64ffe5a599a7a475cb7f5a3aa50c63ae37ce980304a1e9f330342ffff0d8d6

#### Native item 1

Native pointer: /joint_analysis/provenance/4/source_refs/0; canonical SHA-256: 6672fb2f13aa3f49de2d795ece50fd9b7b8f470c9937d1c67e361451b6be25ae

SO_SRC_1e0f32cd5172fba2

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 74a0569e562da29e27c27d25c9904ce1bb0990885ff78bfce0d734b44346130b

SO_HO_HOS06_S_reuse__main__r2

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: ec4411d3e903b3c7321417a8cf1904c234a277feb8d808d7f824efe88944f670

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: 40635d3e7f3b937894529c09a2781692b387308be6a7f1341b4681248b717abd

SO_HO_HOS06_S_reuse__main__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 8cc1c985f0371509d0c4ff910e5cf5bb54d9711f7d3d4e4850139da8a23a6b42

Translate x0 and embed the source loss in one coordinate. Verify all model budgets with the explicit guard; preserve full gradient/Hessian responses, adaptive algorithms, arbitrary outputs, per-instance probability and worst-case gradient accounting. Quantify the source KL proof to obtain sigma_1^2/(288*epsilon_g^2).

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: ede9164e34fb157c4f3376d7721f7e47b8b07e22a23dc384c0fd8f471be26298

subclass_transfer

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 65f1f3b9952a378b816ed7da7d5def3470773a2084d80268452c63832a0584f0

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: 8b9ff11578e738aa89cca94088565503bf71f5ed015e1429e1cae6c857760bd5

SO_HO_HOS06_S_reuse__main__p1

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: 716e5ca7125356f6bd0ad839e65bf805c3d437584ccdeb7fe777b28d3a94a3e4

One-dimensional two-hypothesis construction for sufficiently small epsilon; arbitrary positive curvature tolerance; opaque sample reuse; unrestricted Hessian access.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: f59ed63849e68ab418e8308f4151db2dcca0ba6c1166a6cf8195c0633551d609

arXiv:2610.16832v2, 2026-10-19, Appendix C, PDF p.28, extracted characters 66046-67739.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 0c64ffe5a599a7a475cb7f5a3aa50c63ae37ce980304a1e9f330342ffff0d8d6

#### Native item 1

Native pointer: /joint_analysis/provenance/5/source_refs/0; canonical SHA-256: 6672fb2f13aa3f49de2d795ece50fd9b7b8f470c9937d1c67e361451b6be25ae

SO_SRC_1e0f32cd5172fba2

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 7c55e7669d60c4afdf88ce72bdbc8f4bb3ba06dea338cd430e4fd554c85c59c0

r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: a5e24ddbf8e8f3591d6aaeaf9aa2d6f0d310c8e3decf467f04960c61dd63c7d2

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: d27979fbb4ff540b828b9bcf3eb65ff7df3be3f55e99207f18815dd518826fd2

SO_HO_HOS06_S_reuse__main__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: c516b32f7a44cd6dc397e1c4751595b404a60ac705e95f7beba9415e6309a7eb

Ng+NH>=Ng for every same successful algorithm; same native class and exactr7.

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/provenance/6/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: a32d5a443def48e6d64c6f4be2c6d6b68110d27d53cd5bc1187981ade52741fb

r7

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: ce83030ca743eeb224e761d55031afafac364c9b559e2d7dbd973e194b771d1e

Complete new guided proof HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 8

Native pointer: /joint_analysis/provenance/7; canonical SHA-256: 6d57cfd73d74333897934429c930f415b9fb8a6dc365dc1c55293175b1c61bfe

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/7/bound_id; canonical SHA-256: 62c122f2bb12b92af4bfb00323b7590c0619e3e536669a423a6167881d359cc3

SO_HO_HOS06_S_reuse__main__b8

#### Native field: mapping

Native pointer: /joint_analysis/provenance/7/mapping; canonical SHA-256: 84a6421f03ad883e15d2de405d640c68e4d7a3f1974ad475b278e1b3ea4defaa

Every admissible jointcap hasBg>=L; no Hessian/resource tradeoff equality asserted.

#### Native field: origin

Native pointer: /joint_analysis/provenance/7/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/7/proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/provenance/7/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/7/source_domain; canonical SHA-256: a32d5a443def48e6d64c6f4be2c6d6b68110d27d53cd5bc1187981ade52741fb

r7

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/7/source_locator; canonical SHA-256: ce83030ca743eeb224e761d55031afafac364c9b559e2d7dbd973e194b771d1e

Complete new guided proof HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/7/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/7/target_domain; canonical SHA-256: 6d3226a38d1dac77494062b891624aed4cc1d7f85355ba059657d7a448ebfb65

Referenced regions: (r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive) AND (Exactly unchanged r7: r7: d>=1, 0<epsilon_H<=1 and 0<epsilon_g<=min{1,sigma_1/8,beta/4,M_2/12,G/6,Delta/(4-2sqrt(3))}, with all structural bounds positive)

#### Native item 9

Native pointer: /joint_analysis/provenance/8; canonical SHA-256: 573b0ce658391d53e77b3604f4fe25c3b1f5259b5a8521ba95079f48d82c884f

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/8/bound_id; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native field: mapping

Native pointer: /joint_analysis/provenance/8/mapping; canonical SHA-256: d5bc608bb19fd319804ca0b38ef2f949fbd857e9826c1c9ee7697615e2dbea03

Complete finite algorithm and 2/3 union-bound proof; m_g,m_H,K,h depend only on publicinputs, withzero Hessian oracle responses.

#### Native field: origin

Native pointer: /joint_analysis/provenance/8/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/8/proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/provenance/8/proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/8/source_domain; canonical SHA-256: 3c4e46b6c6943b35ab0df8f2081cea712553bf241dd394a15aec9e1d85df8162

Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/8/source_locator; canonical SHA-256: 78f27e6db9c6b0bd219d33f2889a478514c259d0845c0865b9418866adaf272b

Complete new guided proof HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/8/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/8/target_domain; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 10

Native pointer: /joint_analysis/provenance/9; canonical SHA-256: fc79fbfa896726d1c5baf5dc3a679f6a8992a2176e03522a45ee538af28f59cf

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/9/bound_id; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native field: mapping

Native pointer: /joint_analysis/provenance/9/mapping; canonical SHA-256: d5bc608bb19fd319804ca0b38ef2f949fbd857e9826c1c9ee7697615e2dbea03

Complete finite algorithm and 2/3 union-bound proof; m_g,m_H,K,h depend only on publicinputs, withzero Hessian oracle responses.

#### Native field: origin

Native pointer: /joint_analysis/provenance/9/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/9/proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/provenance/9/proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/9/source_domain; canonical SHA-256: 3c4e46b6c6943b35ab0df8f2081cea712553bf241dd394a15aec9e1d85df8162

Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/9/source_locator; canonical SHA-256: 78f27e6db9c6b0bd219d33f2889a478514c259d0845c0865b9418866adaf272b

Complete new guided proof HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/9/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/9/target_domain; canonical SHA-256: 46f621275f85d7a8e0a6cc175d6eb0bbeeed84077a832b2c0dd532e0cc20c813

(Unchanged target r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$)

#### Native item 11

Native pointer: /joint_analysis/provenance/10; canonical SHA-256: ccb384cc5c830a90a9f7755b3dd85c4400f7f92a5c7719729028e2aa759039ec

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/10/bound_id; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native field: mapping

Native pointer: /joint_analysis/provenance/10/mapping; canonical SHA-256: d5bc608bb19fd319804ca0b38ef2f949fbd857e9826c1c9ee7697615e2dbea03

Complete finite algorithm and 2/3 union-bound proof; m_g,m_H,K,h depend only on publicinputs, withzero Hessian oracle responses.

#### Native field: origin

Native pointer: /joint_analysis/provenance/10/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/10/proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/provenance/10/proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/10/source_domain; canonical SHA-256: 3c4e46b6c6943b35ab0df8f2081cea712553bf241dd394a15aec9e1d85df8162

Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/10/source_locator; canonical SHA-256: 78f27e6db9c6b0bd219d33f2889a478514c259d0845c0865b9418866adaf272b

Complete new guided proof HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/10/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/10/target_domain; canonical SHA-256: 3355a6bae6f9d2e2849259ec7981722027e22977effd417adce5cab45da08c9a

Referenced regions: ($d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$) AND (Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 12

Native pointer: /joint_analysis/provenance/11; canonical SHA-256: cda291b24c2eddf39c9ef22ac476fa9b37e993b5f55b4636485e020ce0101aad

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/11/bound_id; canonical SHA-256: 9625661fb8c53c6c9524b366b157ae48b6e2a0c3a09535bd0ef568a6f4b2f7e2

SO_HO_HOS06_S_reuse__main__b12

#### Native field: mapping

Native pointer: /joint_analysis/provenance/11/mapping; canonical SHA-256: 493cd9ef470ff6817c5c88b50bf7ba6c742b631d45720bf67743b1ef86e6b244

Directed upper projection of one established joint witness(C_gf,0); not an optimal Ngclaim.

#### Native field: origin

Native pointer: /joint_analysis/provenance/11/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/11/proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/provenance/11/proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/11/source_domain; canonical SHA-256: 3c4e46b6c6943b35ab0df8f2081cea712553bf241dd394a15aec9e1d85df8162

Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/11/source_locator; canonical SHA-256: 78f27e6db9c6b0bd219d33f2889a478514c259d0845c0865b9418866adaf272b

Complete new guided proof HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/11/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/11/target_domain; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 13

Native pointer: /joint_analysis/provenance/12; canonical SHA-256: 4cf87f6d878caa1b94e57eb948516e452ddc61f094737dc49f05f9ab95adb6fd

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/12/bound_id; canonical SHA-256: a5835deee3b5251752a48d50c4b66ff5e9c708cc235efb44900cb2a26a13e0a3

SO_HO_HOS06_S_reuse__main__b13

#### Native field: mapping

Native pointer: /joint_analysis/provenance/12/mapping; canonical SHA-256: 493cd9ef470ff6817c5c88b50bf7ba6c742b631d45720bf67743b1ef86e6b244

Directed upper projection of one established joint witness(C_gf,0); not an optimal Ngclaim.

#### Native field: origin

Native pointer: /joint_analysis/provenance/12/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/12/proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/provenance/12/proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/12/source_domain; canonical SHA-256: 3c4e46b6c6943b35ab0df8f2081cea712553bf241dd394a15aec9e1d85df8162

Native reusable sample contract: integerd>=1;Delta,beta,M2,sigma1,sigma2,G>0;0<epsilon_g,epsilon_H<=1;population SOS success>=2/3 and finite worst-path resource caps.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/12/source_locator; canonical SHA-256: 78f27e6db9c6b0bd219d33f2889a478514c259d0845c0865b9418866adaf272b

Complete new guided proof HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/12/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/12/target_domain; canonical SHA-256: 0af6bc7d4d72794642a23549c023933fe58ea20e41b5839481fe8e8c4af6b5af

(Unchanged native r2: $d\ge1,\quad0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0$; integerd>=1 and Delta,beta,M2,sigma1,sigma2,G>0; common-probability-one globally beta-smooth and M2-Hessian-Lipschitz samples, unbiased population derivatives, opaque independent fresh handles reusable across arbitrary points.)

#### Native item 14

Native pointer: /joint_analysis/provenance/13; canonical SHA-256: 97f9300c7a3f47cc97ca6385c2489b560426915fc7a607af49a875d67fc2b660

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/13/bound_id; canonical SHA-256: 9d49ad9e5587ad73868b47fb1678457a90d0aebac4d4c8f6a9337213c93b7130

SO_HO_HOS06_S_reuse__main__b14

#### Native field: mapping

Native pointer: /joint_analysis/provenance/13/mapping; canonical SHA-256: 9161ede56db3618126fdc07dafd603310c95cb182434ccd55cacd80b7b0580e6

If an algorithm has caps (Bg,BH), its total cap is Bg+BH. The retained q1 lower therefore requires Bg+BH>=Lold. This is necessary only, never a sufficient budget or a marginal lower.

#### Native field: origin

Native pointer: /joint_analysis/provenance/13/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/13/proof_refs; canonical SHA-256: 79d97d6e040bc5389a3a1475e286771387397d26dc69b1734e30c3750d9e79e3

#### Native item 1

Native pointer: /joint_analysis/provenance/13/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/13/source_domain; canonical SHA-256: 15ad7ea93b7d3552f51626dcb1786fd9a2844347d5d3d1d33da5c0a634228fb5

Unchanged b4/r3 only, conditionally retaining its recorded source chain.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/13/source_locator; canonical SHA-256: a2696bb60d9f75ad64cd6982d13c28375b2921a6f29c241a3b7af1b8700fa39b

Exact retained native b4 lower and the same-algorithm resource projection proof.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/13/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/13/target_domain; canonical SHA-256: 569e71e6eb987fb6ffa0150dac91ee49ffba28e20fb382ed2551be6230a4d9d4

Referenced regions: ($0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$) AND (Exactly the unchanged old b4/r3 source guard, intersected with receiving native r2 where used: $0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge d_*,\quad d_*\le C(\theta)[1+\Delta D_g^{3/4}/\varepsilon_g+\varepsilon_H^{-4}\log(2/\varepsilon_H)+\varepsilon_H^{-3}]$)

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 852774d4fd2fa97645c0dc9919ed95dd5f5a38fdb5bc66fbb3ce7cece3000684

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: e2b3b307c0ed41f89da40cff113ce5f0b3a3b12b40a31186e3bcbaffa23ae2e1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: fa5e390ece55c6b8e51ee91f48b354c5e9ac4ff51b7bb79b305cd73e7af0a2bc

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: 8c42041c3d721fd9a7c249e43a89935601f6430ba09523a58b00f260883449ec

User-feedback-guided curator synthesis plus the explicitly recorded new primary-source reads. Previous partial searches and retained-source recertification limits persist; neither a new exhaustive search nor a completed native approval is claimed.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 412b772cf449a5f7b12f122f31426f989c526278e81c3454049d2c3cb5f9f126

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 78ff37a020951ee446db01b53c7382dffea36122cc5346da633f9319473cccd4

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: f674d6e1e5dda6b19350ece9111e25d369b8073b60395d6c02bff348a4e45113

Concrete candidate dispositions: SO_HO_HOS06_S_reuse__main__b3: included; SO_HO_HOS06_S_reuse__main__b4: included; SO_HO_HOS06_S_reuse__main__b7: included; SO_HO_HOS06_S_reuse__main__b12: included. The complete validity/adoption intersections are explicitly recorded once in the corresponding comparison bound_uses, retaining comparison region AND exact native bound validity AND native claim_guards. In particular c1/b7 requires r3 intersectr7; c4/b8 requires r2 intersectr7; c5/b4 and c4/b14 keep r3. c4 adopts the old q1/b4 consequence through quantity-matched b14 and HOS06_RESOURCE_PROJECTION_CLOSURE_20261116, so it is not an unresolved absence of transfer. Full-target Hessian-free witnesses apply only as proved on r2; b10 is resource nonnegativity, not hypothesis discrimination. Guarded min/max/Pareto arguments and the remaining conditional-source limitations are unchanged.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 27f7d2fbf934e968d7e480ca6edbd6998bd81b131544ead63f83c027fc037000

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 9625661fb8c53c6c9524b366b157ae48b6e2a0c3a09535bd0ef568a6f4b2f7e2

SO_HO_HOS06_S_reuse__main__b12

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: ae5cbb2842c7a31a8ec929bf99894df67b7e8d6e1b063b5f3e17fcb29804a1ce

SO_HO_HOS06_S_reuse__main__b3

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 06ac0ae5be77b122c05ef886ae4257c063acf9b25cae6a5a65cd4809e03b946f

SO_HO_HOS06_S_reuse__main__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: d27979fbb4ff540b828b9bcf3eb65ff7df3be3f55e99207f18815dd518826fd2

SO_HO_HOS06_S_reuse__main__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: b2df57e17320857df268fb72a2a2a0c388fa2784df0f94354bf05b3d947e46ea

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: d140fa472d503ef97dd68b28d37b4dd52378752c60a0ab1d8f1d5bf58f4980fc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/2; canonical SHA-256: 8b9ff11578e738aa89cca94088565503bf71f5ed015e1429e1cae6c857760bd5

SO_HO_HOS06_S_reuse__main__p1

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: dd144d135db712b57c8121446a620e0c49025f2bdefb1e57050995d31516c679

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: c751cfcfb8acae996cfe1b91a1ca7d7e3611ae2f1895067ecb45d7a7a8dec79b

Concrete candidate dispositions: SO_HO_HOS06_S_reuse__main__b1: included; SO_HO_HOS06_S_reuse__main__b6: included; SO_HO_HOS06_S_reuse__main__b13: included. The complete validity/adoption intersections are explicitly recorded once in the corresponding comparison bound_uses, retaining comparison region AND exact native bound validity AND native claim_guards. In particular c1/b7 requires r3 intersectr7; c4/b8 requires r2 intersectr7; c5/b4 and c4/b14 keep r3. c4 adopts the old q1/b4 consequence through quantity-matched b14 and HOS06_RESOURCE_PROJECTION_CLOSURE_20261116, so it is not an unresolved absence of transfer. Full-target Hessian-free witnesses apply only as proved on r2; b10 is resource nonnegativity, not hypothesis discrimination. Guarded min/max/Pareto arguments and the remaining conditional-source limitations are unchanged.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: aaffd7e22d034243660b087daa5e08a40f1b1e84960c845593cf26d06a91beab

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: e2bea876d5b01adf95355fcfa3d5a1eb1c0f18cb82989aef4da6c94606c19fe2

SO_HO_HOS06_S_reuse__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: a5835deee3b5251752a48d50c4b66ff5e9c708cc235efb44900cb2a26a13e0a3

SO_HO_HOS06_S_reuse__main__b13

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 40635d3e7f3b937894529c09a2781692b387308be6a7f1341b4681248b717abd

SO_HO_HOS06_S_reuse__main__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: d140fa472d503ef97dd68b28d37b4dd52378752c60a0ab1d8f1d5bf58f4980fc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/2; canonical SHA-256: 8b9ff11578e738aa89cca94088565503bf71f5ed015e1429e1cae6c857760bd5

SO_HO_HOS06_S_reuse__main__p1

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: b04c3932d27f521b19eccf4ecc73e50ea02ce5f2272bfe78d34d4e8c25ac4198

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: cbe4a73d564b5ac835877354cc372a5b401bac0a37edd250227ccbf00d98553e

Concrete candidate dispositions: SO_HO_HOS06_S_reuse__main__b2: dominated; SO_HO_HOS06_S_reuse__main__b9: included; SO_HO_HOS06_S_reuse__main__b10: included. The complete validity/adoption intersections are explicitly recorded once in the corresponding comparison bound_uses, retaining comparison region AND exact native bound validity AND native claim_guards. In particular c1/b7 requires r3 intersectr7; c4/b8 requires r2 intersectr7; c5/b4 and c4/b14 keep r3. c4 adopts the old q1/b4 consequence through quantity-matched b14 and HOS06_RESOURCE_PROJECTION_CLOSURE_20261116, so it is not an unresolved absence of transfer. Full-target Hessian-free witnesses apply only as proved on r2; b10 is resource nonnegativity, not hypothesis discrimination. Guarded min/max/Pareto arguments and the remaining conditional-source limitations are unchanged.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 561cd077fc24908cdb7109fbe6e81b18c4fdfa659c244d96975c2049171a857e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 6a2ea4ebf6c3e625ed70d7927c0552676b2e94269a6d55f8ec14a4f500e21626

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: d140fa472d503ef97dd68b28d37b4dd52378752c60a0ab1d8f1d5bf58f4980fc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/2; canonical SHA-256: 8b9ff11578e738aa89cca94088565503bf71f5ed015e1429e1cae6c857760bd5

SO_HO_HOS06_S_reuse__main__p1

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 23c974923210f61bf00112c7b42fd36cdadca1165c8e7c9227ce861fa4390459

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: 854f9899486a1d8a87d7efeed402f762d1e378e8a5091ff7f028b0595475ffd3

The old positive Hessian upper is retained as valid history but not selected. Exact NH=0 dominates it on the entire same target through a finite capped gradient-only witness; no old upper was silently dropped without a proved replacement. Non-append removal from selected_in_regimes is explicitly supported by HOS06_HESSIAN_UPPER_REPLACEMENT_20261116; historical source not newly recertified.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: ec69e2d21529a66eedf21be0aabf239144aa602ef5ea7221edb26d872e412499

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 6a2ea4ebf6c3e625ed70d7927c0552676b2e94269a6d55f8ec14a4f500e21626

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: 7f1a6540bd14dbb3bcfdfdfac9a64bfde09607556bb3c904bfc43adedf6ede22

synthesis-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: 0ad6e47ac22eacc914c886e6ef31d7a4dac086af14d97d0c57709a2e37e020ed

replacement_branch

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 1fc73ef359228381cb07b713981cc619c6b233e7655cce647576f975d736b1e0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs/1; canonical SHA-256: 77d7a05099c0f628130f1ebbf732f9899046db3d4d7ffc5545e8a7ec141217ab

HOS06_HESSIAN_UPPER_REPLACEMENT_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 20cff7a4f145ab80857868543b1cec779c8c3b982cfb8472ca367e6410c8c1ef

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: 1dc6f400638c76a116e0a64efac00964aeefe945f00760f3545be066f303f561

Concrete candidate dispositions: SO_HO_HOS06_S_reuse__main__b5: included; SO_HO_HOS06_S_reuse__main__b8: included; SO_HO_HOS06_S_reuse__main__b11: included; SO_HO_HOS06_S_reuse__main__b14: included. The complete validity/adoption intersections are explicitly recorded once in the corresponding comparison bound_uses, retaining comparison region AND exact native bound validity AND native claim_guards. In particular c1/b7 requires r3 intersectr7; c4/b8 requires r2 intersectr7; c5/b4 and c4/b14 keep r3. c4 adopts the old q1/b4 consequence through quantity-matched b14 and HOS06_RESOURCE_PROJECTION_CLOSURE_20261116, so it is not an unresolved absence of transfer. Full-target Hessian-free witnesses apply only as proved on r2; b10 is resource nonnegativity, not hypothesis discrimination. Guarded min/max/Pareto arguments and the remaining conditional-source limitations are unchanged.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 61d38beefaf739dd35327a5de657747f771dcbeef4b8a862e4efbfe5fc898fc9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/0; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/1; canonical SHA-256: 9d49ad9e5587ad73868b47fb1678457a90d0aebac4d4c8f6a9337213c93b7130

SO_HO_HOS06_S_reuse__main__b14

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/2; canonical SHA-256: 8b2bfb9ed10b34dcb679c9beed579713efc81b4ffcade8f4b512788295cdce68

SO_HO_HOS06_S_reuse__main__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/3; canonical SHA-256: 62c122f2bb12b92af4bfb00323b7590c0619e3e536669a423a6167881d359cc3

SO_HO_HOS06_S_reuse__main__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 4128c09e9eff66f446cf0e59b5a8870f8cf221ea14210e3b4eab38a1e091affd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: d140fa472d503ef97dd68b28d37b4dd52378752c60a0ab1d8f1d5bf58f4980fc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs/2; canonical SHA-256: 8b9ff11578e738aa89cca94088565503bf71f5ed015e1429e1cae6c857760bd5

SO_HO_HOS06_S_reuse__main__p1

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: c57a478f0336ee46562c381f2ef8e8b918363e324bf2a9d8b9af4eb2968bad00

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: f674d6e1e5dda6b19350ece9111e25d369b8073b60395d6c02bff348a4e45113

Concrete candidate dispositions: SO_HO_HOS06_S_reuse__main__b3: included; SO_HO_HOS06_S_reuse__main__b4: included; SO_HO_HOS06_S_reuse__main__b7: included; SO_HO_HOS06_S_reuse__main__b12: included. The complete validity/adoption intersections are explicitly recorded once in the corresponding comparison bound_uses, retaining comparison region AND exact native bound validity AND native claim_guards. In particular c1/b7 requires r3 intersectr7; c4/b8 requires r2 intersectr7; c5/b4 and c4/b14 keep r3. c4 adopts the old q1/b4 consequence through quantity-matched b14 and HOS06_RESOURCE_PROJECTION_CLOSURE_20261116, so it is not an unresolved absence of transfer. Full-target Hessian-free witnesses apply only as proved on r2; b10 is resource nonnegativity, not hypothesis discrimination. Guarded min/max/Pareto arguments and the remaining conditional-source limitations are unchanged.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 27f7d2fbf934e968d7e480ca6edbd6998bd81b131544ead63f83c027fc037000

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/0; canonical SHA-256: 9625661fb8c53c6c9524b366b157ae48b6e2a0c3a09535bd0ef568a6f4b2f7e2

SO_HO_HOS06_S_reuse__main__b12

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/1; canonical SHA-256: ae5cbb2842c7a31a8ec929bf99894df67b7e8d6e1b063b5f3e17fcb29804a1ce

SO_HO_HOS06_S_reuse__main__b3

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/2; canonical SHA-256: 06ac0ae5be77b122c05ef886ae4257c063acf9b25cae6a5a65cd4809e03b946f

SO_HO_HOS06_S_reuse__main__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/3; canonical SHA-256: d27979fbb4ff540b828b9bcf3eb65ff7df3be3f55e99207f18815dd518826fd2

SO_HO_HOS06_S_reuse__main__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 28b46a8d26ba0142d4ca01374a376501e9fb3314d8d5c52d29755428731d1ce0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 8cedb7c54fb7a3ff1b2d98263a56263d1a8afbb4fdabf8cee435054dc16d1ea3

synthesis-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: d140fa472d503ef97dd68b28d37b4dd52378752c60a0ab1d8f1d5bf58f4980fc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs/2; canonical SHA-256: 8b9ff11578e738aa89cca94088565503bf71f5ed015e1429e1cae6c857760bd5

SO_HO_HOS06_S_reuse__main__p1

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 3168ae9f0807df7bf160c1bcd9f85a4995d36e7868209761845e1f5cb4ca78e0

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: 9514a49144f09becbf5e0c656d8302a9a40dc9215dcf650d3dd03883c9f39bfc

NH>=0 transfers at most the trivial nonnegative lower in the other scalar resources or joint orthant. It gives no positive Ng, total or tradeoff lower. Existing positive guarded lower rows dominate where present; no duplicate zero lower is needed there. Target comparison SO_HO_HOS06_S_reuse__main__c1; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 84ee1a0919af1ab708ab0e0f5981ef06e7befcd0a490cf7e535ef09ba5379189

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/0; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: b2df57e17320857df268fb72a2a2a0c388fa2784df0f94354bf05b3d947e46ea

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 5fa33983f32a4c1027a92106c478a51fb23e76f63df8884a2a111e3319f68669

synthesis-6

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: e045b3f07b262739ae2d70ee748b049527194fd5832145636600f409d041bf68

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: e298f66c5d2945eeee6c71abd378362fd80f4ebb0d139ea8c62fa502c63f65d4

NH>=0 transfers at most the trivial nonnegative lower in the other scalar resources or joint orthant. It gives no positive Ng, total or tradeoff lower. Existing positive guarded lower rows dominate where present; no duplicate zero lower is needed there. Target comparison SO_HO_HOS06_S_reuse__main__c2; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 84ee1a0919af1ab708ab0e0f5981ef06e7befcd0a490cf7e535ef09ba5379189

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/0; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: f1d7c1b829959acf5fd8b22ab6c75fdbf1b3810e2c3ef78a394693a9a0260546

synthesis-7

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: 2f422aba660cc7c731bddfbb7c34d8142b2d1f0152a9bba1f2dd751bd3a5efb2

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: f36327b4565daac5d13d9100e5bf7735233cd1309b61d2bff7d2463142d78b03

NH>=0 transfers at most the trivial nonnegative lower in the other scalar resources or joint orthant. It gives no positive Ng, total or tradeoff lower. Existing positive guarded lower rows dominate where present; no duplicate zero lower is needed there. Target comparison SO_HO_HOS06_S_reuse__main__c4; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 84ee1a0919af1ab708ab0e0f5981ef06e7befcd0a490cf7e535ef09ba5379189

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/0; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 4128c09e9eff66f446cf0e59b5a8870f8cf221ea14210e3b4eab38a1e091affd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 705e1af290021b0ee8b6cac71ead9597d036f83961af1c252c90f4ed8047130f

synthesis-8

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 45d17f4f3d6f4b92b93f1784cd430adc774f31b36622d649d477b13caacc1c3a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: 707a6773cee97982eba43ccc4b5ce6568c920fcf7b357a19a5a810a57e048b51

NH>=0 transfers at most the trivial nonnegative lower in the other scalar resources or joint orthant. It gives no positive Ng, total or tradeoff lower. Existing positive guarded lower rows dominate where present; no duplicate zero lower is needed there. Target comparison SO_HO_HOS06_S_reuse__main__c5; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 84ee1a0919af1ab708ab0e0f5981ef06e7befcd0a490cf7e535ef09ba5379189

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/0; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 28b46a8d26ba0142d4ca01374a376501e9fb3314d8d5c52d29755428731d1ce0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: cefa876d80b27bbc26ecd952c430927d231047df60d2c399f9959d4307ecfd70

synthesis-9

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: f40646f8d3bb93ce90bf46400bb52a2e49ae4b338d19236691f1b6d33551220b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/argument; canonical SHA-256: 0f56db0fa8ed088ff37d378a706e70c67e4674a58e9ab6e678eb46465f1432e3

This SAME algorithm has caps (Cgf,0), hence total<=Cgf (b12), Ng<=Cgf (b13), and NH=0 (b9), all on the full target. q4 adopts b11 directly. The explicit projections, not a pair of different scalar optimizers, are used. Target comparison SO_HO_HOS06_S_reuse__main__c1; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs; canonical SHA-256: 3f3b4b593156e4086a2fe0ecb7e163a4a4632dfd243b0e910f54428053ee4234

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/0; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: b2df57e17320857df268fb72a2a2a0c388fa2784df0f94354bf05b3d947e46ea

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 9cab9589f3334662db7e0a597e42e682e82fc47dc9b49b5f48ad62e4069ce795

synthesis-10

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: f94a2402ec4cf81e011115e292a45d9fad9f2f65c441ff623049439c0770b563

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/argument; canonical SHA-256: 17d4a1f371ef6724efcc038358ac9bbeaddd74088b98ac88b0ff1900eb212f09

This SAME algorithm has caps (Cgf,0), hence total<=Cgf (b12), Ng<=Cgf (b13), and NH=0 (b9), all on the full target. q4 adopts b11 directly. The explicit projections, not a pair of different scalar optimizers, are used. Target comparison SO_HO_HOS06_S_reuse__main__c2; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs; canonical SHA-256: 3f3b4b593156e4086a2fe0ecb7e163a4a4632dfd243b0e910f54428053ee4234

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs/0; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: feb7b5e13e39ba9c3fd05c25add5ea4e2cecf0c49861217b1b978e57b06145f4

synthesis-11

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/obligations/12; canonical SHA-256: 1f7ff6262edba4e9002c0e66022644b59191d153a67d2c14ef577ae343a13036

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/argument; canonical SHA-256: f48808c216cd3ab1af9655796566f02fb2cf6f29913b5787fb0bc9e094e1d999

This SAME algorithm has caps (Cgf,0), hence total<=Cgf (b12), Ng<=Cgf (b13), and NH=0 (b9), all on the full target. q4 adopts b11 directly. The explicit projections, not a pair of different scalar optimizers, are used. Target comparison SO_HO_HOS06_S_reuse__main__c3; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs; canonical SHA-256: 3f3b4b593156e4086a2fe0ecb7e163a4a4632dfd243b0e910f54428053ee4234

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs/0; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids; canonical SHA-256: 6a2ea4ebf6c3e625ed70d7927c0552676b2e94269a6d55f8ec14a4f500e21626

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/id; canonical SHA-256: 2882ec2161c3f82fe99edd536675194d9cab7af971ea8f7b2000e93fc92f51a3

synthesis-12

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 14

Native pointer: /joint_analysis/synthesis_coverage/obligations/13; canonical SHA-256: 92f7d5d92a94fb29bec20af794e1dcf0d6ff5cadff0b32ba9a4fd654e74d62c3

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/argument; canonical SHA-256: dd6038016cbc44136486176978ede47c31159ca0449190c802bdc339994cb0cf

This SAME algorithm has caps (Cgf,0), hence total<=Cgf (b12), Ng<=Cgf (b13), and NH=0 (b9), all on the full target. q4 adopts b11 directly. The explicit projections, not a pair of different scalar optimizers, are used. Target comparison SO_HO_HOS06_S_reuse__main__c5; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs; canonical SHA-256: 3f3b4b593156e4086a2fe0ecb7e163a4a4632dfd243b0e910f54428053ee4234

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs/0; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids; canonical SHA-256: 28b46a8d26ba0142d4ca01374a376501e9fb3314d8d5c52d29755428731d1ce0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/0; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/id; canonical SHA-256: 6e1f748f3b3ba34e115027c6b98663cae9101a61cf4f66864ed75f96fa708e34

synthesis-13

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 15

Native pointer: /joint_analysis/synthesis_coverage/obligations/14; canonical SHA-256: ba268e6b0439bd37587b036c6fb0a161c9b518c385f8f78dc16150ddc9627469

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/argument; canonical SHA-256: c9bf206104daea85c6c954d184248209a3c50d26dd4470ebe2d26cfc3f678644

The total upper Cgf by itself implies each marginal upper<=Cgf and a joint witness (Cgf,Cgf). The stronger same-algorithm b11 independently certifies (Cgf,0); its q2/q3 projections b13/b9 dominate these indirect consequences. No reverse lower implication is inferred. Target comparison SO_HO_HOS06_S_reuse__main__c2; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs; canonical SHA-256: 9cd6867b480e2eb0b1e39682961d8974fcc4149fba4b48ba446804f64a284b72

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs/0; canonical SHA-256: 9625661fb8c53c6c9524b366b157ae48b6e2a0c3a09535bd0ef568a6f4b2f7e2

SO_HO_HOS06_S_reuse__main__b12

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/id; canonical SHA-256: db10229057c9ce34edb92d41588fee1a97e45c7898ce6d2d78a4f94f79b29e53

synthesis-14

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 16

Native pointer: /joint_analysis/synthesis_coverage/obligations/15; canonical SHA-256: 445d209ea37049431ddfc86d2a524875ae9146ba090c6cb7934d398542841adb

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/argument; canonical SHA-256: e64e55fd35a0a217a552b65b95d38f120d31cb606310f288cc16e2d74b78be92

The total upper Cgf by itself implies each marginal upper<=Cgf and a joint witness (Cgf,Cgf). The stronger same-algorithm b11 independently certifies (Cgf,0); its q2/q3 projections b13/b9 dominate these indirect consequences. No reverse lower implication is inferred. Target comparison SO_HO_HOS06_S_reuse__main__c3; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs; canonical SHA-256: 9cd6867b480e2eb0b1e39682961d8974fcc4149fba4b48ba446804f64a284b72

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs/0; canonical SHA-256: 9625661fb8c53c6c9524b366b157ae48b6e2a0c3a09535bd0ef568a6f4b2f7e2

SO_HO_HOS06_S_reuse__main__b12

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids; canonical SHA-256: 6a2ea4ebf6c3e625ed70d7927c0552676b2e94269a6d55f8ec14a4f500e21626

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/id; canonical SHA-256: 9c70b32b9eaa3fa80c1eb45835c4241c6987b57973f48ac657397e759ab2e156

synthesis-15

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 17

Native pointer: /joint_analysis/synthesis_coverage/obligations/16; canonical SHA-256: c3f7baa9b2a5b7ab4288966aa58acb0395aec93c46ffa9edbdde94041097b114

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/argument; canonical SHA-256: db05f7a038f277dd3884d225d2a33434bfb93d76afa038be812a21f94e3ae7b2

The total upper Cgf by itself implies each marginal upper<=Cgf and a joint witness (Cgf,Cgf). The stronger same-algorithm b11 independently certifies (Cgf,0); its q2/q3 projections b13/b9 dominate these indirect consequences. No reverse lower implication is inferred. Target comparison SO_HO_HOS06_S_reuse__main__c4; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs; canonical SHA-256: 9cd6867b480e2eb0b1e39682961d8974fcc4149fba4b48ba446804f64a284b72

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/0; canonical SHA-256: 9625661fb8c53c6c9524b366b157ae48b6e2a0c3a09535bd0ef568a6f4b2f7e2

SO_HO_HOS06_S_reuse__main__b12

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids; canonical SHA-256: 4128c09e9eff66f446cf0e59b5a8870f8cf221ea14210e3b4eab38a1e091affd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/0; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/id; canonical SHA-256: ae0010ee9bed7c6c3f9e2522a3923d8c76200fd38262c11802a5f697be271b89

synthesis-16

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 18

Native pointer: /joint_analysis/synthesis_coverage/obligations/17; canonical SHA-256: fbd982e7dc2eebed299e1244d8bdb97e4636075a6bc9509c7f66db3bbb769aed

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/argument; canonical SHA-256: a9b3e34cc19889ca3090704cb88df4934f474cb933166939733f7d4da6e1aecf

A marginal Ng optimum alone bounds neither total nor NH nor a Pareto vector. Here the underlying complete proof separately certifies b11=(Cgf,0), whose explicit b12/b9 projections carry those consequences. No illicit combination of separate minima is used. Target comparison SO_HO_HOS06_S_reuse__main__c1; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs; canonical SHA-256: 8cc1d09e11f8000d4b2bfcaecd3fd36782703a3958f993b4b1be95f440ff2231

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs/0; canonical SHA-256: a5835deee3b5251752a48d50c4b66ff5e9c708cc235efb44900cb2a26a13e0a3

SO_HO_HOS06_S_reuse__main__b13

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids; canonical SHA-256: b2df57e17320857df268fb72a2a2a0c388fa2784df0f94354bf05b3d947e46ea

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/id; canonical SHA-256: 6bcbe0868e1d0319f0c8cce19387b1c345c263363f45ed33569ef2fe530668aa

synthesis-17

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 19

Native pointer: /joint_analysis/synthesis_coverage/obligations/18; canonical SHA-256: dd9f810c4b43743e782407a8dcedb39b7b21fab081458a6da47cfc81fcc53ee9

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/argument; canonical SHA-256: 56d5409f1d2ffeaebf90ef909456cfe6a58830c9c3941f4278a5d0fdc2458e74

A marginal Ng optimum alone bounds neither total nor NH nor a Pareto vector. Here the underlying complete proof separately certifies b11=(Cgf,0), whose explicit b12/b9 projections carry those consequences. No illicit combination of separate minima is used. Target comparison SO_HO_HOS06_S_reuse__main__c3; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/bound_refs; canonical SHA-256: 8cc1d09e11f8000d4b2bfcaecd3fd36782703a3958f993b4b1be95f440ff2231

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/bound_refs/0; canonical SHA-256: a5835deee3b5251752a48d50c4b66ff5e9c708cc235efb44900cb2a26a13e0a3

SO_HO_HOS06_S_reuse__main__b13

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids; canonical SHA-256: 6a2ea4ebf6c3e625ed70d7927c0552676b2e94269a6d55f8ec14a4f500e21626

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/id; canonical SHA-256: 0e1735155ad7d87ec6c3e991a68c8ca4cd526265e27027c4b60b559eb8fb9cf4

synthesis-18

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 20

Native pointer: /joint_analysis/synthesis_coverage/obligations/19; canonical SHA-256: 4f80f9cd127a5cf44357115da73de48a29e6a8858f30db88bd9c58aa34f9dd75

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/argument; canonical SHA-256: c62afeae9ff160e206e8e7d53b37f8d143582d8179a7533c6679481986f56489

A marginal Ng optimum alone bounds neither total nor NH nor a Pareto vector. Here the underlying complete proof separately certifies b11=(Cgf,0), whose explicit b12/b9 projections carry those consequences. No illicit combination of separate minima is used. Target comparison SO_HO_HOS06_S_reuse__main__c4; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/bound_refs; canonical SHA-256: 8cc1d09e11f8000d4b2bfcaecd3fd36782703a3958f993b4b1be95f440ff2231

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/bound_refs/0; canonical SHA-256: a5835deee3b5251752a48d50c4b66ff5e9c708cc235efb44900cb2a26a13e0a3

SO_HO_HOS06_S_reuse__main__b13

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids; canonical SHA-256: 4128c09e9eff66f446cf0e59b5a8870f8cf221ea14210e3b4eab38a1e091affd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/0; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/id; canonical SHA-256: 88002ec70b13de15a55f5b060f45df458e2721280ed7e0d983466a02c934ee63

synthesis-19

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 21

Native pointer: /joint_analysis/synthesis_coverage/obligations/20; canonical SHA-256: 2ce517bd5524de07f657a718a8048f4943bd771e982f89c0b65b72962163ed59

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/argument; canonical SHA-256: b85077e2b487166b76e0752313837557aff39cc39fb845f964d839fff1a18911

A marginal Ng optimum alone bounds neither total nor NH nor a Pareto vector. Here the underlying complete proof separately certifies b11=(Cgf,0), whose explicit b12/b9 projections carry those consequences. No illicit combination of separate minima is used. Target comparison SO_HO_HOS06_S_reuse__main__c5; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/bound_refs; canonical SHA-256: 8cc1d09e11f8000d4b2bfcaecd3fd36782703a3958f993b4b1be95f440ff2231

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/bound_refs/0; canonical SHA-256: a5835deee3b5251752a48d50c4b66ff5e9c708cc235efb44900cb2a26a13e0a3

SO_HO_HOS06_S_reuse__main__b13

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids; canonical SHA-256: 28b46a8d26ba0142d4ca01374a376501e9fb3314d8d5c52d29755428731d1ce0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/0; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/id; canonical SHA-256: 87561e678f922710b1763cf9f64990db955be24cd345b157bb3b55ab808fe35a

synthesis-20

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 22

Native pointer: /joint_analysis/synthesis_coverage/obligations/21; canonical SHA-256: c75b7151c4cf36a8441084dd5c02f265843ac431b99f6df1c076afe7512b03c6

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/argument; canonical SHA-256: 45afd410c0fd7beb67119dbeb629f0298a8bcc892db56b4ee5d6d57620895ed5

The joint necessary sum halfspace on exact r3 is precisely the retained q1 total lower b4, included in c1 and on the r3 overlap of c5. It implies no positive separate Ng or NH lower. The r7 marginal information lower b6 is independent and its stronger directional constraint b8 is separately adopted. Target comparison SO_HO_HOS06_S_reuse__main__c1; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/bound_refs; canonical SHA-256: 2f3e0e66d907ad6324f449f135d9ba8aaed307d55ea50f02faaceb1ba7270325

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/bound_refs/0; canonical SHA-256: 9d49ad9e5587ad73868b47fb1678457a90d0aebac4d4c8f6a9337213c93b7130

SO_HO_HOS06_S_reuse__main__b14

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids; canonical SHA-256: b2df57e17320857df268fb72a2a2a0c388fa2784df0f94354bf05b3d947e46ea

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/id; canonical SHA-256: e3b776230ced10698b7ccf9438d1a464ea126a47d9919261fba2c82989cecbc8

synthesis-21

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 23

Native pointer: /joint_analysis/synthesis_coverage/obligations/22; canonical SHA-256: 373e649ab4a06bb1c7b80bda41f0df71573a3e96dda3a84a6f33d2980af5c023

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/argument; canonical SHA-256: 7a540eeac79280dd54591296cac66bde7cfda5e37facb565d33eca7c0e61beba

The joint necessary sum halfspace on exact r3 is precisely the retained q1 total lower b4, included in c1 and on the r3 overlap of c5. It implies no positive separate Ng or NH lower. The r7 marginal information lower b6 is independent and its stronger directional constraint b8 is separately adopted. Target comparison SO_HO_HOS06_S_reuse__main__c2; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/bound_refs; canonical SHA-256: 2f3e0e66d907ad6324f449f135d9ba8aaed307d55ea50f02faaceb1ba7270325

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/bound_refs/0; canonical SHA-256: 9d49ad9e5587ad73868b47fb1678457a90d0aebac4d4c8f6a9337213c93b7130

SO_HO_HOS06_S_reuse__main__b14

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/id; canonical SHA-256: ddfa466fe7843ac39e72eb00dd37ae01a7c17a51e14b650f0958af2d470167c8

synthesis-22

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 24

Native pointer: /joint_analysis/synthesis_coverage/obligations/23; canonical SHA-256: 7ee93e02666ffd59a56147e5bce154d4459e0bbdd4ec406984b01a92d655c9d2

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/argument; canonical SHA-256: 48d8a9774bc5f168bb6408d408d04a1dbe0e260d47a80eea08779046608bfa9b

The joint necessary sum halfspace on exact r3 is precisely the retained q1 total lower b4, included in c1 and on the r3 overlap of c5. It implies no positive separate Ng or NH lower. The r7 marginal information lower b6 is independent and its stronger directional constraint b8 is separately adopted. Target comparison SO_HO_HOS06_S_reuse__main__c3; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/bound_refs; canonical SHA-256: 2f3e0e66d907ad6324f449f135d9ba8aaed307d55ea50f02faaceb1ba7270325

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/bound_refs/0; canonical SHA-256: 9d49ad9e5587ad73868b47fb1678457a90d0aebac4d4c8f6a9337213c93b7130

SO_HO_HOS06_S_reuse__main__b14

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/comparison_ids; canonical SHA-256: 6a2ea4ebf6c3e625ed70d7927c0552676b2e94269a6d55f8ec14a4f500e21626

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/id; canonical SHA-256: 47e9ed587655c1cf4fbbb69e06671f0c8ec580ecbf4cd84e05a9793c15b2280f

synthesis-23

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 25

Native pointer: /joint_analysis/synthesis_coverage/obligations/24; canonical SHA-256: 5b9a6593f316d496b2477f8e290702920da48f2a4117d0224641ea1862254bd6

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/argument; canonical SHA-256: 6d500793702f17864fead660e66c77650df27eea0a1a6a5d9dc760dfe98c08b9

The joint necessary sum halfspace on exact r3 is precisely the retained q1 total lower b4, included in c1 and on the r3 overlap of c5. It implies no positive separate Ng or NH lower. The r7 marginal information lower b6 is independent and its stronger directional constraint b8 is separately adopted. Target comparison SO_HO_HOS06_S_reuse__main__c5; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/bound_refs; canonical SHA-256: 2f3e0e66d907ad6324f449f135d9ba8aaed307d55ea50f02faaceb1ba7270325

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/bound_refs/0; canonical SHA-256: 9d49ad9e5587ad73868b47fb1678457a90d0aebac4d4c8f6a9337213c93b7130

SO_HO_HOS06_S_reuse__main__b14

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/comparison_ids; canonical SHA-256: 28b46a8d26ba0142d4ca01374a376501e9fb3314d8d5c52d29755428731d1ce0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/comparison_ids/0; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/id; canonical SHA-256: 13a3b319bde651e5e649c14614171087c9d5a2847aeb85bf882a42d16627ca40

synthesis-24

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 26

Native pointer: /joint_analysis/synthesis_coverage/obligations/25; canonical SHA-256: 444ef404aa680dd17f1fe5e3007821a602f51374464e3def2fdd16a781ef870b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/argument; canonical SHA-256: 9895f089326dc3e1a7eccf0d0768ef88e2d3ca011822a05ef354c270d3d14e90

A positive marginal NH upper alone imposes no cap on Ng or total and cannot supply an independently optimized joint pair. Its original same-algorithm joint witness b5 is separately retained, while new b11 has NH=0. No marginal-only inference is adopted. Target comparison SO_HO_HOS06_S_reuse__main__c1; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/bound_refs; canonical SHA-256: ec69e2d21529a66eedf21be0aabf239144aa602ef5ea7221edb26d872e412499

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/bound_refs/0; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/comparison_ids; canonical SHA-256: b2df57e17320857df268fb72a2a2a0c388fa2784df0f94354bf05b3d947e46ea

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/id; canonical SHA-256: 62e9c73ee815105cb0c7610b3557637da29e23c19b1c01ae624d760fab2bf957

synthesis-25

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 27

Native pointer: /joint_analysis/synthesis_coverage/obligations/26; canonical SHA-256: 3c7cfb33e467880e4c6f405edfac139af0cb11a12a0cdf2599291cc882048caf

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/argument; canonical SHA-256: 8a52e76ac412b4143173f9cd35edf6f0a54dc8036db79b506a4dc865c63fb416

A positive marginal NH upper alone imposes no cap on Ng or total and cannot supply an independently optimized joint pair. Its original same-algorithm joint witness b5 is separately retained, while new b11 has NH=0. No marginal-only inference is adopted. Target comparison SO_HO_HOS06_S_reuse__main__c2; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/bound_refs; canonical SHA-256: ec69e2d21529a66eedf21be0aabf239144aa602ef5ea7221edb26d872e412499

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/bound_refs/0; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/id; canonical SHA-256: be55e268a90a5296ead94117e2a2f151dcb28a229b6578cb01afa1e6a0510c69

synthesis-26

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 28

Native pointer: /joint_analysis/synthesis_coverage/obligations/27; canonical SHA-256: 38fee8193171d66f7a77795b7a5081f565114165068a2cbe6180d0fcc03e1b99

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/argument; canonical SHA-256: 7bb4e52d2d5861273e2b4c0a646025894c5d62c5309a6ebbe6f6a2ea64d19a67

A positive marginal NH upper alone imposes no cap on Ng or total and cannot supply an independently optimized joint pair. Its original same-algorithm joint witness b5 is separately retained, while new b11 has NH=0. No marginal-only inference is adopted. Target comparison SO_HO_HOS06_S_reuse__main__c4; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/bound_refs; canonical SHA-256: ec69e2d21529a66eedf21be0aabf239144aa602ef5ea7221edb26d872e412499

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/bound_refs/0; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/comparison_ids; canonical SHA-256: 4128c09e9eff66f446cf0e59b5a8870f8cf221ea14210e3b4eab38a1e091affd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/comparison_ids/0; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/id; canonical SHA-256: 8dda965246efc0241eb3de9a5ffe0b468393dfc7d711d6c784df3ce69595926c

synthesis-27

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 29

Native pointer: /joint_analysis/synthesis_coverage/obligations/28; canonical SHA-256: 0d19645740093f6882e7e4937076577f8cc4ab872c6715dc2ca765d06757fef2

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/argument; canonical SHA-256: a6b9a5dd527f985a9adbf0a2a6b8bfb09b542d832c458dcd902d07bb17c10d2d

A positive marginal NH upper alone imposes no cap on Ng or total and cannot supply an independently optimized joint pair. Its original same-algorithm joint witness b5 is separately retained, while new b11 has NH=0. No marginal-only inference is adopted. Target comparison SO_HO_HOS06_S_reuse__main__c5; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/bound_refs; canonical SHA-256: ec69e2d21529a66eedf21be0aabf239144aa602ef5ea7221edb26d872e412499

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/bound_refs/0; canonical SHA-256: deb62b0d093369cdf2495245981bba2cbd71fe1c869d52ae4b751b482ad26cb5

SO_HO_HOS06_S_reuse__main__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/comparison_ids; canonical SHA-256: 28b46a8d26ba0142d4ca01374a376501e9fb3314d8d5c52d29755428731d1ce0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/comparison_ids/0; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/id; canonical SHA-256: c8dbb883bebd53e0d3c6a074a46655e222802af53f2e1372a9c558c0d8550cd9

synthesis-28

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 30

Native pointer: /joint_analysis/synthesis_coverage/obligations/29; canonical SHA-256: 6bc04c2dcd66e327fd037983a0d349ab3831c6681ed4e5a77035093e0c6eafb0

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/argument; canonical SHA-256: cc815b3429d08129f0232e72d0e72eb2b713139c77bb7a45dea1db1d2ef42a9b

Old total upper Uold bounds each marginal by Uold and permits a joint witness (Uold,Uold). The retained same-algorithm b5 already gives the sharper separate old caps, and the new b11 gives NH=0. q2 keeps its old sharper b1; q3 uses exact zero; q4 keeps the two concrete vectors. Target comparison SO_HO_HOS06_S_reuse__main__c2; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/bound_refs; canonical SHA-256: 34a0df5cc010019fbf12b240fc95bc69df44986a75cdfc839840e5200594b9aa

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/bound_refs/0; canonical SHA-256: ae5cbb2842c7a31a8ec929bf99894df67b7e8d6e1b063b5f3e17fcb29804a1ce

SO_HO_HOS06_S_reuse__main__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/id; canonical SHA-256: d7eb22e083c731fa1974dc52d7dc3258ab5e053a7c706f3355f07ac9b042f4be

synthesis-29

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 31

Native pointer: /joint_analysis/synthesis_coverage/obligations/30; canonical SHA-256: 1018a496d1adcd6c4fb5987d132fdf56ab1f51d7a3240d59b8f5b066264ff1d5

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/argument; canonical SHA-256: 94e81e7f2ed5f1b3f6af020c0a1b4f3c9bd844d6d40f283bbb9b0fc0edd72f18

Old total upper Uold bounds each marginal by Uold and permits a joint witness (Uold,Uold). The retained same-algorithm b5 already gives the sharper separate old caps, and the new b11 gives NH=0. q2 keeps its old sharper b1; q3 uses exact zero; q4 keeps the two concrete vectors. Target comparison SO_HO_HOS06_S_reuse__main__c3; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/bound_refs; canonical SHA-256: 34a0df5cc010019fbf12b240fc95bc69df44986a75cdfc839840e5200594b9aa

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/bound_refs/0; canonical SHA-256: ae5cbb2842c7a31a8ec929bf99894df67b7e8d6e1b063b5f3e17fcb29804a1ce

SO_HO_HOS06_S_reuse__main__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/comparison_ids; canonical SHA-256: 6a2ea4ebf6c3e625ed70d7927c0552676b2e94269a6d55f8ec14a4f500e21626

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/id; canonical SHA-256: 5eacc02594e32f35e2b20254ccb9860ade19c3dfd1a705009165846e9a3d2c50

synthesis-30

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 32

Native pointer: /joint_analysis/synthesis_coverage/obligations/31; canonical SHA-256: e295180a7b28b7bfd2ead4655c273f40059f07ee034158a13ed2b59648e332ec

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/argument; canonical SHA-256: d1b3ffe83084778d763ab7104a8b9428a7996630696df067302eb51a9d5ecfed

Old total upper Uold bounds each marginal by Uold and permits a joint witness (Uold,Uold). The retained same-algorithm b5 already gives the sharper separate old caps, and the new b11 gives NH=0. q2 keeps its old sharper b1; q3 uses exact zero; q4 keeps the two concrete vectors. Target comparison SO_HO_HOS06_S_reuse__main__c4; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/bound_refs; canonical SHA-256: 34a0df5cc010019fbf12b240fc95bc69df44986a75cdfc839840e5200594b9aa

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/bound_refs/0; canonical SHA-256: ae5cbb2842c7a31a8ec929bf99894df67b7e8d6e1b063b5f3e17fcb29804a1ce

SO_HO_HOS06_S_reuse__main__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/comparison_ids; canonical SHA-256: 4128c09e9eff66f446cf0e59b5a8870f8cf221ea14210e3b4eab38a1e091affd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/comparison_ids/0; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/id; canonical SHA-256: fd25acd138f6df2960dfb9e3614cb93ae63a78554c31e95d35d5dcb22161f3e1

synthesis-31

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 33

Native pointer: /joint_analysis/synthesis_coverage/obligations/32; canonical SHA-256: a8d25fcbec7344c1648bb573099ae4e83c8434e08f4831f1b373637e0e07978e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/argument; canonical SHA-256: 20a578b15790f390a3c17f70a0a45f2a40d6043b511321e7e7ca54db88e249ca

The old total lower on exact r3 implies the joint necessary sum halfspace Bg+BH>=Lold, explicitly published as b14 in c4. It does not imply a positive Ng or NH marginal lower; no reverse implication or guard extension is adopted. Target comparison SO_HO_HOS06_S_reuse__main__c2; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/bound_refs; canonical SHA-256: bf8757416b23368facbf7cad4aa9f7ca5a588e56269be6bd92eb59e958a21159

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/bound_refs/0; canonical SHA-256: 06ac0ae5be77b122c05ef886ae4257c063acf9b25cae6a5a65cd4809e03b946f

SO_HO_HOS06_S_reuse__main__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/id; canonical SHA-256: e0b1883cc851c5eeef7aae67c0a2d2c70e81202af6c099d6f1a55e4f98cda88c

synthesis-32

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 34

Native pointer: /joint_analysis/synthesis_coverage/obligations/33; canonical SHA-256: 5a006b16eedcccbf92d938c3a98e58bc7795047339b7a29527b1f9216e135025

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/argument; canonical SHA-256: 8d0c1db63c3de6176002b31ba78abaae87e398316aede2a6d0385e570105122d

The old total lower on exact r3 implies the joint necessary sum halfspace Bg+BH>=Lold, explicitly published as b14 in c4. It does not imply a positive Ng or NH marginal lower; no reverse implication or guard extension is adopted. Target comparison SO_HO_HOS06_S_reuse__main__c3; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/bound_refs; canonical SHA-256: bf8757416b23368facbf7cad4aa9f7ca5a588e56269be6bd92eb59e958a21159

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/bound_refs/0; canonical SHA-256: 06ac0ae5be77b122c05ef886ae4257c063acf9b25cae6a5a65cd4809e03b946f

SO_HO_HOS06_S_reuse__main__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/comparison_ids; canonical SHA-256: 6a2ea4ebf6c3e625ed70d7927c0552676b2e94269a6d55f8ec14a4f500e21626

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/id; canonical SHA-256: 57c7567d6ab0e27eabdeed21cdbd34fd56b04408ed069248d566d64b21248ae8

synthesis-33

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 35

Native pointer: /joint_analysis/synthesis_coverage/obligations/34; canonical SHA-256: 549bdfb3551379ffc2d1c5593f9a3e9086e49693f2b6a4145a1b1924ff592db7

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/argument; canonical SHA-256: fa3ede7b371a19ef24ef4cb7c93435014d5f43234abc1bdc1803280f3d4f503e

The old total lower on exact r3 implies the joint necessary sum halfspace Bg+BH>=Lold, explicitly published as b14 in c4. It does not imply a positive Ng or NH marginal lower; no reverse implication or guard extension is adopted. Target comparison SO_HO_HOS06_S_reuse__main__c4; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/bound_refs; canonical SHA-256: bf8757416b23368facbf7cad4aa9f7ca5a588e56269be6bd92eb59e958a21159

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/bound_refs/0; canonical SHA-256: 06ac0ae5be77b122c05ef886ae4257c063acf9b25cae6a5a65cd4809e03b946f

SO_HO_HOS06_S_reuse__main__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/comparison_ids; canonical SHA-256: 4128c09e9eff66f446cf0e59b5a8870f8cf221ea14210e3b4eab38a1e091affd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/comparison_ids/0; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/id; canonical SHA-256: 77c00ec2db1f39dc2cd7c3a963fe3a565381f04154c003eb57deebecc4d2c448

synthesis-34

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 36

Native pointer: /joint_analysis/synthesis_coverage/obligations/35; canonical SHA-256: c5f45b5016b24eb09eb5e1cfbafd54af492d2e3a32a0ceb1d475110c84310c41

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/argument; canonical SHA-256: a139cdae6cf57ee5b5375365e6cbae61c807cb512be39ee97fe0cf75581ecdf7

A total lower alone does not imply either positive marginal lower. Its valid joint constraint Bg+BH>=Lg is already dominated by the stronger independently proved Bg>=Lg (b8) on the SAME r7. q2 retains original b6, not a reverse projection; no positive NH lower is inferred. Target comparison SO_HO_HOS06_S_reuse__main__c2; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/bound_refs; canonical SHA-256: 9a14c041604e2cba3d957ebfa0ef87ce8299079ff92f7068a26774758a5f67f3

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/bound_refs/0; canonical SHA-256: d27979fbb4ff540b828b9bcf3eb65ff7df3be3f55e99207f18815dd518826fd2

SO_HO_HOS06_S_reuse__main__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/id; canonical SHA-256: 998b57541e0a5fab7a0c09d6eb6ddb302e4dcbe635cd76744278de30dac7e4b5

synthesis-35

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 37

Native pointer: /joint_analysis/synthesis_coverage/obligations/36; canonical SHA-256: 5adf62de7df3d54456c041a3b0b1be7337843d74406d179013ca2c6af91ae399

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/argument; canonical SHA-256: 209efabda42aeacb7e3afc3278201cd9e138c884f4b1da0beed0214fc1bf26a1

A total lower alone does not imply either positive marginal lower. Its valid joint constraint Bg+BH>=Lg is already dominated by the stronger independently proved Bg>=Lg (b8) on the SAME r7. q2 retains original b6, not a reverse projection; no positive NH lower is inferred. Target comparison SO_HO_HOS06_S_reuse__main__c3; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/bound_refs; canonical SHA-256: 9a14c041604e2cba3d957ebfa0ef87ce8299079ff92f7068a26774758a5f67f3

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/bound_refs/0; canonical SHA-256: d27979fbb4ff540b828b9bcf3eb65ff7df3be3f55e99207f18815dd518826fd2

SO_HO_HOS06_S_reuse__main__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/comparison_ids; canonical SHA-256: 6a2ea4ebf6c3e625ed70d7927c0552676b2e94269a6d55f8ec14a4f500e21626

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/id; canonical SHA-256: 29856869b07f55999810ca12f94393e1da340a1b6836506377266c7879b04a94

synthesis-36

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/36/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 38

Native pointer: /joint_analysis/synthesis_coverage/obligations/37; canonical SHA-256: 2c43cd67b8343f869bba48d568ffc271b6f6be49fec3f447169cdf411b9c48d9

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/argument; canonical SHA-256: 754a1de8a22e25c22b1a49f1de722b995c1ec67c6b54899bfbd4c7d42e384f42

A total lower alone does not imply either positive marginal lower. Its valid joint constraint Bg+BH>=Lg is already dominated by the stronger independently proved Bg>=Lg (b8) on the SAME r7. q2 retains original b6, not a reverse projection; no positive NH lower is inferred. Target comparison SO_HO_HOS06_S_reuse__main__c4; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/bound_refs; canonical SHA-256: 9a14c041604e2cba3d957ebfa0ef87ce8299079ff92f7068a26774758a5f67f3

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/bound_refs/0; canonical SHA-256: d27979fbb4ff540b828b9bcf3eb65ff7df3be3f55e99207f18815dd518826fd2

SO_HO_HOS06_S_reuse__main__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/comparison_ids; canonical SHA-256: 4128c09e9eff66f446cf0e59b5a8870f8cf221ea14210e3b4eab38a1e091affd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/comparison_ids/0; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/id; canonical SHA-256: c8a199077537a863144d1046efd524d9af689b3ad627dc9d676fb2689f94f6c1

synthesis-37

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/37/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 39

Native pointer: /joint_analysis/synthesis_coverage/obligations/38; canonical SHA-256: 94c13268b0cffd84d522fc614412b1ee3581afb192b5e43e8f90efd08e7cf89e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/argument; canonical SHA-256: 408c01095c66688e6d647686efae77ecfd2d9c66d8bee05a8479daaa18fca7ea

The directed same-algorithm constraint Bg>=Lg implies marginal Ng>=Lg (original b6) and total>=Lg (b7), on exact r7; these matched rows are included in c2 and c1/c5 respectively. It imposes no positive NH lower; the explicit NH=0 witness is compatible. Target comparison SO_HO_HOS06_S_reuse__main__c1; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/bound_refs; canonical SHA-256: 3bd2970a3831fff6302e566801c32816d26a00a1ae65bc035b87681796168385

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/bound_refs/0; canonical SHA-256: 62c122f2bb12b92af4bfb00323b7590c0619e3e536669a423a6167881d359cc3

SO_HO_HOS06_S_reuse__main__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/comparison_ids; canonical SHA-256: b2df57e17320857df268fb72a2a2a0c388fa2784df0f94354bf05b3d947e46ea

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/id; canonical SHA-256: dd1a016143270dda6040eff45ed458cfd454b773356e735ef7258db202f4bae9

synthesis-38

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/38/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 40

Native pointer: /joint_analysis/synthesis_coverage/obligations/39; canonical SHA-256: b278ff93e7c81432437eaddaf9c529009156b4d65da2455eb10044344d0b4104

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/argument; canonical SHA-256: ab44741e03f457d52d319f5dbe6d58b4aa254e773e8776686ab5092e6e57f04f

The directed same-algorithm constraint Bg>=Lg implies marginal Ng>=Lg (original b6) and total>=Lg (b7), on exact r7; these matched rows are included in c2 and c1/c5 respectively. It imposes no positive NH lower; the explicit NH=0 witness is compatible. Target comparison SO_HO_HOS06_S_reuse__main__c2; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/bound_refs; canonical SHA-256: 3bd2970a3831fff6302e566801c32816d26a00a1ae65bc035b87681796168385

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/bound_refs/0; canonical SHA-256: 62c122f2bb12b92af4bfb00323b7590c0619e3e536669a423a6167881d359cc3

SO_HO_HOS06_S_reuse__main__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/id; canonical SHA-256: 6db609bfee29c1e4de5339af35211d93e116506ee6abc2649a427a70be6292cf

synthesis-39

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/39/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 41

Native pointer: /joint_analysis/synthesis_coverage/obligations/40; canonical SHA-256: d010a43cc681cc1dfb4f49d5c201664a7f20e291ece892d33be8b54cb0f9f45d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/argument; canonical SHA-256: 142bb34c109e907a13d58cd4ad5b8a2ce21ca30e389b29b30ccdb24866aca3cd

The directed same-algorithm constraint Bg>=Lg implies marginal Ng>=Lg (original b6) and total>=Lg (b7), on exact r7; these matched rows are included in c2 and c1/c5 respectively. It imposes no positive NH lower; the explicit NH=0 witness is compatible. Target comparison SO_HO_HOS06_S_reuse__main__c3; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/bound_refs; canonical SHA-256: 3bd2970a3831fff6302e566801c32816d26a00a1ae65bc035b87681796168385

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/bound_refs/0; canonical SHA-256: 62c122f2bb12b92af4bfb00323b7590c0619e3e536669a423a6167881d359cc3

SO_HO_HOS06_S_reuse__main__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/comparison_ids; canonical SHA-256: 6a2ea4ebf6c3e625ed70d7927c0552676b2e94269a6d55f8ec14a4f500e21626

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/id; canonical SHA-256: bb3523a4f7dae0ed82abeb0b557d71605a78975c9f7be90b787d1a626dca7293

synthesis-40

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/40/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 42

Native pointer: /joint_analysis/synthesis_coverage/obligations/41; canonical SHA-256: 71466faca0ccec8acfe34879975d077782a8ca2bf5807a59973bbc879966c8e0

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/argument; canonical SHA-256: 28e342eeb2b65a91cedabb2ba392ffbfe014f139651ca74a83a3d497bd2d8675

The directed same-algorithm constraint Bg>=Lg implies marginal Ng>=Lg (original b6) and total>=Lg (b7), on exact r7; these matched rows are included in c2 and c1/c5 respectively. It imposes no positive NH lower; the explicit NH=0 witness is compatible. Target comparison SO_HO_HOS06_S_reuse__main__c5; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/bound_refs; canonical SHA-256: 3bd2970a3831fff6302e566801c32816d26a00a1ae65bc035b87681796168385

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/bound_refs/0; canonical SHA-256: 62c122f2bb12b92af4bfb00323b7590c0619e3e536669a423a6167881d359cc3

SO_HO_HOS06_S_reuse__main__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/comparison_ids; canonical SHA-256: 28b46a8d26ba0142d4ca01374a376501e9fb3314d8d5c52d29755428731d1ce0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/comparison_ids/0; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/id; canonical SHA-256: c9cfcd1ca0043a91168cd5b92d11b49346d699323c658b7d1c1b950a1d7342db

synthesis-41

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/41/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 43

Native pointer: /joint_analysis/synthesis_coverage/obligations/42; canonical SHA-256: 89f2a32b3c2b6273bb762b29a04dbc0ecfa34f141ffa3689faf680652a1f1ece

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/argument; canonical SHA-256: b8ee3274c18ceb7ea2b3f9808502735faca1624d22e5171165f943cf290c458a

The scalar NH optimum zero alone fixes no Ng/total cost. The COMPLETE SAME algorithm used for this upper additionally has Ng<=Cgf and is explicitly b11; b12/b13 carry its sum/gradient projections. No marginal optimum from another algorithm is attached to zero NH. Target comparison SO_HO_HOS06_S_reuse__main__c1; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/bound_refs; canonical SHA-256: 9373ad2bbb9e8c2617ff35167a33b3e85a0ec6872dc40eb43852a7c1c34d4135

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/bound_refs/0; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/comparison_ids; canonical SHA-256: b2df57e17320857df268fb72a2a2a0c388fa2784df0f94354bf05b3d947e46ea

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/id; canonical SHA-256: 7497956f043095c26aab59155524f20fd061a7e8870457fb6ea601c106aa1a55

synthesis-42

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/42/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 44

Native pointer: /joint_analysis/synthesis_coverage/obligations/43; canonical SHA-256: c0ade10a5f9d77f1c2c62adf9fb0c34f1ead240dde9d2485e3b522eda54027f6

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/argument; canonical SHA-256: 4da431bac432622a05bdcdc9b728267b7fd166b565994b7ec2b3ff1a9b4118f7

The scalar NH optimum zero alone fixes no Ng/total cost. The COMPLETE SAME algorithm used for this upper additionally has Ng<=Cgf and is explicitly b11; b12/b13 carry its sum/gradient projections. No marginal optimum from another algorithm is attached to zero NH. Target comparison SO_HO_HOS06_S_reuse__main__c2; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/bound_refs; canonical SHA-256: 9373ad2bbb9e8c2617ff35167a33b3e85a0ec6872dc40eb43852a7c1c34d4135

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/bound_refs/0; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/comparison_ids; canonical SHA-256: eaa4f5b426a5922b5b998567802a7275470eb227885d3510a2e36c5bcf131c4a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/comparison_ids/0; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/id; canonical SHA-256: a3ec184a91c1b3aa95ec0c0bf76c5633d44bb30b8c56a59125a4bab52528ef85

synthesis-43

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/43/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 45

Native pointer: /joint_analysis/synthesis_coverage/obligations/44; canonical SHA-256: 84a92c805770e1bf9b923259f6213797cd3f76bfbb6e33b01d1aa91f71dc9eb8

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/argument; canonical SHA-256: 098c351f827c6b9ec5967da9e17823e7fea83fd3da1efe130c59b9214f29bb5e

The scalar NH optimum zero alone fixes no Ng/total cost. The COMPLETE SAME algorithm used for this upper additionally has Ng<=Cgf and is explicitly b11; b12/b13 carry its sum/gradient projections. No marginal optimum from another algorithm is attached to zero NH. Target comparison SO_HO_HOS06_S_reuse__main__c4; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/bound_refs; canonical SHA-256: 9373ad2bbb9e8c2617ff35167a33b3e85a0ec6872dc40eb43852a7c1c34d4135

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/bound_refs/0; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/comparison_ids; canonical SHA-256: 4128c09e9eff66f446cf0e59b5a8870f8cf221ea14210e3b4eab38a1e091affd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/comparison_ids/0; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/id; canonical SHA-256: 6563553bcbf1f0b32bbb3e04d54505250adc94844a3c8cdc1985485f144b290a

synthesis-44

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/44/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 46

Native pointer: /joint_analysis/synthesis_coverage/obligations/45; canonical SHA-256: f46977b256becff9044386cd8f6d9d4b4b8dfc6a0e3ff892c9b707f15c639197

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/argument; canonical SHA-256: 743710cc77802866fd251fc6600c05be2bb9d0b6d3cf68dfcaed9f4d82d5a124

The scalar NH optimum zero alone fixes no Ng/total cost. The COMPLETE SAME algorithm used for this upper additionally has Ng<=Cgf and is explicitly b11; b12/b13 carry its sum/gradient projections. No marginal optimum from another algorithm is attached to zero NH. Target comparison SO_HO_HOS06_S_reuse__main__c5; all original r3/r7 guards are retained.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/bound_refs; canonical SHA-256: 9373ad2bbb9e8c2617ff35167a33b3e85a0ec6872dc40eb43852a7c1c34d4135

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/bound_refs/0; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/comparison_ids; canonical SHA-256: 28b46a8d26ba0142d4ca01374a376501e9fb3314d8d5c52d29755428731d1ce0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/comparison_ids/0; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/id; canonical SHA-256: e19fb61cad6b23968a06ac633ac32e78b3fcb0fdcdc7713299f232021640c12c

synthesis-45

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/proof_refs; canonical SHA-256: 7ecf2c6576e5c05a2290c1e0f8c277e47bc05115c82ea825185704c5c7f4a303

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/proof_refs/0; canonical SHA-256: d35cbc3c7ae77c25bd2a505f6e95d0174dca944691136fad1a85718c794a8982

HOS06_RESOURCE_PROJECTION_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/proof_refs/1; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/45/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 47

Native pointer: /joint_analysis/synthesis_coverage/obligations/46; canonical SHA-256: 1da5c77460f30891693bf1b96aadebf63755fefac43b0af2b5239137c77bc1af

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/argument; canonical SHA-256: cf23295a9c03ead0cfc41f710d623bb42a9283be2d37991dba0d61839f3b3baf

The newly written self-contained finite capped stochastic gradient/difference algorithm resolves this exact prior lead. It does not certify SPIDER's optimized gradient rate or the full joint frontier.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/bound_refs; canonical SHA-256: e83710eda848f58c4e263ac9385ca3363e768864ecc1d3bc16f8769ce5af11b9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/bound_refs/0; canonical SHA-256: 38d5ecedaa154860c8314db54a2f6a42b13d28a0da59385aaad036121c72be54

SO_HO_HOS06_S_reuse__main__b9

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/bound_refs/1; canonical SHA-256: 5e8221be4450e504b0a562f04cd07b73b41d9633795bb192a3758f439a64b8da

SO_HO_HOS06_S_reuse__main__b10

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/bound_refs/2; canonical SHA-256: 241c8bf00b4a96f6d0cc44b37be4e286cc06414ad07e3f878a4d63a0efc5fd9d

SO_HO_HOS06_S_reuse__main__b11

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/cell_ids; canonical SHA-256: db36634ea02f193a64424fa9a7943392760002d8e27fc5bfef83840f5a772738

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/cell_ids/0; canonical SHA-256: 22de28350907c906bc37f4c3af6427ef6df892c7d3c898d9f3b7cba78b93113a

hessian_coordinate_closed

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/comparison_ids; canonical SHA-256: 89323569f313bf5fc1f6491cdca7d44cda5af2a41a975065d7da44d2eebdd861

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/comparison_ids/0; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/comparison_ids/1; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/id; canonical SHA-256: 0a4b8fb470adc9a6c4cfa3c2d7f4f64e9a37d63f82a0313f9096100e545a2853

resolved-prior-hessian-free-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/lead; canonical SHA-256: c7f96c4a16e0e30fea8c30e9fd28ce302ada99e766d04bb4b2df7db7957ff306

Investigate a rigorous zero-Hessian-call algorithm based on same-handle gradient differences before changing q3.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/proof_refs; canonical SHA-256: e1a100931de3c800c1e4255adfaf2e564bbd62f7cc0d21fa5f7d08c7913cbc64

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/proof_refs/0; canonical SHA-256: 42a2fd47da4d34dc0d28b852d8d5a002668dc4a9159ccaf1e59c85c444378af0

HOS06_GRADIENT_ONLY_SOSP_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/46/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 48

Native pointer: /joint_analysis/synthesis_coverage/obligations/47; canonical SHA-256: 9c45c2adec17086cb4d8f99689cbf1345ef6eaf327bf6f49111806888baddfdb

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/comparison_ids; canonical SHA-256: e2b3b307c0ed41f89da40cff113ce5f0b3a3b12b40a31186e3bcbaffa23ae2e1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/comparison_ids/1; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/comparison_ids/2; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/comparison_ids/3; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/comparison_ids/4; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/id; canonical SHA-256: d0167f548742ead3d895787ec442b4a84beeb280ebe70d01f9a7603611e9c56f

remaining-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/lead; canonical SHA-256: 5f90876875623f265d6b6bed79bf7914614c3cb9e83d19b97c8f0a122afce369

Formalize the sufficient zero-query endpoint epsilon_g>=G and epsilon_H>=beta before changing native envelopes; it is disjoint from r7.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/47/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 49

Native pointer: /joint_analysis/synthesis_coverage/obligations/48; canonical SHA-256: f857c9fdafafd4a3a15a8a8d32358369406412db1be152e11eb14b0ef665d929

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/comparison_ids; canonical SHA-256: e2b3b307c0ed41f89da40cff113ce5f0b3a3b12b40a31186e3bcbaffa23ae2e1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/comparison_ids/1; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/comparison_ids/2; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/comparison_ids/3; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/comparison_ids/4; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/id; canonical SHA-256: a4b3d9806c41184784f257b17680c859184105b903c13a4dc473b5d4a38646ea

remaining-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/lead; canonical SHA-256: 373c006d98513160657a5d77a13c09e6819c6f5cb964fcfb0c2f19cf9bb3d15d

Sharper total-cost bounds at low dimension and coordinate bounds outside r7 remain unassessed; the targeted searches do not certify literature absence.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/48/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 50

Native pointer: /joint_analysis/synthesis_coverage/obligations/49; canonical SHA-256: 0aac085bcc7492a009478621adb548993d5e9f23ca7581301b0fb5e3b5090cb1

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/comparison_ids; canonical SHA-256: e2b3b307c0ed41f89da40cff113ce5f0b3a3b12b40a31186e3bcbaffa23ae2e1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/comparison_ids/1; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/comparison_ids/2; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/comparison_ids/3; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/comparison_ids/4; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/id; canonical SHA-256: 3e14526e35b394fe370a6fc3dd84e97e336771629d764f97e1112f9be119d23a

remaining-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/lead; canonical SHA-256: 3d49c4a1f0529de2629fb7df6775b58ae596113bcb2cc8cf7209bc29655b3e60

Optimize theexplicitC_gfgradientcost and comparePareto witness dominance;NH=0doesnotdetermine optimalNg. AnySPIDERrate transfer stillneedsitsown completeprecision/amplificationaccounting;thiscandidateadoptsnoSPIDERgradientrate.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/49/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 51

Native pointer: /joint_analysis/synthesis_coverage/obligations/50; canonical SHA-256: cf7eafe195c56bbe19b8ce33b286aeee365086e2a67792ec8dca692ec7fe43b1

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/comparison_ids; canonical SHA-256: e2b3b307c0ed41f89da40cff113ce5f0b3a3b12b40a31186e3bcbaffa23ae2e1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/comparison_ids/0; canonical SHA-256: 7890f537a5fbb42d2f02f4e6d380f7220dfc8eab8c98d2c901e254d071aed8a4

SO_HO_HOS06_S_reuse__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/comparison_ids/1; canonical SHA-256: 9c4f6d3544d17fa403104049d9de5c10143df23cdb9a22160925687532cba65c

SO_HO_HOS06_S_reuse__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/comparison_ids/2; canonical SHA-256: f00c655c4b38f125f77a8ce20a6fddbaf7d204bc7b3ca386ea1cfe3f77e3969f

SO_HO_HOS06_S_reuse__main__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/comparison_ids/3; canonical SHA-256: 671017e396f97bdde15c4d8cbcd779763fda9727a4e0778f88bb72b53a2aa555

SO_HO_HOS06_S_reuse__main__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/comparison_ids/4; canonical SHA-256: 39d6d59294793e9d39344794f47bae96157ab152da5973a28e330e06b11ef3c9

SO_HO_HOS06_S_reuse__main__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/id; canonical SHA-256: 52f2f3bc992d47ca5e65400cef22478acd6fd6c80777b214e6c32b59fb652ce8

curated-scope-limit-06ff2bdeb1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/50/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 1b3afffc6fd6f1f90712e001044c7b349d4736d0ee573648f2ab09a63f62d13f

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: acdf0cab8b25fce346fa055070ac156dc0af82d92cfabc4b88b84f0db9018c37

#### Native item 1

Native pointer: /joint_analysis/target/allowed_constant_dependencies/0; canonical SHA-256: 92ffedc715a1d5ffe8f98e16298777d6cfe08037922a53723da4b7eaf98b67a2

SO_HO_HOS06_S_reuse_p_360c30de02

#### Native item 2

Native pointer: /joint_analysis/target/allowed_constant_dependencies/1; canonical SHA-256: 3b62aa9f90972f46cdb02143a98e47c210dd4e56a049b65462248b824d871162

SO_HO_HOS06_S_reuse_p_58c6dbfa8a

#### Native item 3

Native pointer: /joint_analysis/target/allowed_constant_dependencies/2; canonical SHA-256: 7033b07143ee6c8e8ab1cc4ee6945216f9f3f8948a64e7cfa71f84d6af3272be

SO_HO_HOS06_S_reuse_p_fb9a0c2872

#### Native item 4

Native pointer: /joint_analysis/target/allowed_constant_dependencies/3; canonical SHA-256: 6d3482225c13218e1267c0b2cfd93d4d7a0bc45ca10b2f4af37c1db25d199c1b

SO_HO_HOS06_S_reuse_p_26aa16ff5b

#### Native item 5

Native pointer: /joint_analysis/target/allowed_constant_dependencies/4; canonical SHA-256: d563822a02ff1cd27784f53df621d6ca99707d5b602115ff5a93bf409fe81d1f

SO_HO_HOS06_S_reuse_p_1bfb19894a

#### Native item 6

Native pointer: /joint_analysis/target/allowed_constant_dependencies/5; canonical SHA-256: ed68a704c652d42876f81a0d09952ff55da2e27943967e15748f7d748bfebc8d

SO_HO_HOS06_S_reuse_p_45d020550f

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 9788c8ca617a6755bca61ae99630eba2c809a7c6f4c5fdb4ebea456a47d52802

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: 7bb9459dcac5b77a99df0d6dbaa2fe9f7fd0b02dfef9f93123a32f8fe3041262

/regimes/3

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: ad1790018b9fd38c768a1d556052a4bdef80f90e0800c553add650756317baf3

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 07753f22f81d6ef82dd173abf8857ed0eb9a2cef965a95e571fde8fdd8552c84

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: 075ddd0032478c5f16981a07e120e5b0794f92458b97d204c3a70d1be622ff45

strictly positive admissible public bound

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: 92ffedc715a1d5ffe8f98e16298777d6cfe08037922a53723da4b7eaf98b67a2

SO_HO_HOS06_S_reuse_p_360c30de02

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 92ffedc715a1d5ffe8f98e16298777d6cfe08037922a53723da4b7eaf98b67a2

SO_HO_HOS06_S_reuse_p_360c30de02

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: d5d39f2225d07e7a0a3c7716313f6614ca4a2dd87b3f76b6d8ab08bcb3d1dd9f

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: 075ddd0032478c5f16981a07e120e5b0794f92458b97d204c3a70d1be622ff45

strictly positive admissible public bound

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: 3b62aa9f90972f46cdb02143a98e47c210dd4e56a049b65462248b824d871162

SO_HO_HOS06_S_reuse_p_58c6dbfa8a

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: 3b62aa9f90972f46cdb02143a98e47c210dd4e56a049b65462248b824d871162

SO_HO_HOS06_S_reuse_p_58c6dbfa8a

#### Native item 3

Native pointer: /joint_analysis/target/fixed_parameters/2; canonical SHA-256: 6d0707204457e1aade15213325762b7c075c4dd9091e7ea81de4d96eaecbe45b

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/2/domain; canonical SHA-256: 075ddd0032478c5f16981a07e120e5b0794f92458b97d204c3a70d1be622ff45

strictly positive admissible public bound

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/2/parameter_ref; canonical SHA-256: 7033b07143ee6c8e8ab1cc4ee6945216f9f3f8948a64e7cfa71f84d6af3272be

SO_HO_HOS06_S_reuse_p_fb9a0c2872

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/2/symbol; canonical SHA-256: 7033b07143ee6c8e8ab1cc4ee6945216f9f3f8948a64e7cfa71f84d6af3272be

SO_HO_HOS06_S_reuse_p_fb9a0c2872

#### Native item 4

Native pointer: /joint_analysis/target/fixed_parameters/3; canonical SHA-256: 276677cb18f8c6c66c78b36b79801f52a8c39075e905184e0233ca8b794548eb

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/3/domain; canonical SHA-256: 075ddd0032478c5f16981a07e120e5b0794f92458b97d204c3a70d1be622ff45

strictly positive admissible public bound

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/3/parameter_ref; canonical SHA-256: 6d3482225c13218e1267c0b2cfd93d4d7a0bc45ca10b2f4af37c1db25d199c1b

SO_HO_HOS06_S_reuse_p_26aa16ff5b

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/3/symbol; canonical SHA-256: 6d3482225c13218e1267c0b2cfd93d4d7a0bc45ca10b2f4af37c1db25d199c1b

SO_HO_HOS06_S_reuse_p_26aa16ff5b

#### Native item 5

Native pointer: /joint_analysis/target/fixed_parameters/4; canonical SHA-256: 1a6898a7a23daa4b07e91e0dc9054b40acdbef9d03f1fd5db901a3d7924ee123

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/4/domain; canonical SHA-256: 075ddd0032478c5f16981a07e120e5b0794f92458b97d204c3a70d1be622ff45

strictly positive admissible public bound

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/4/parameter_ref; canonical SHA-256: d563822a02ff1cd27784f53df621d6ca99707d5b602115ff5a93bf409fe81d1f

SO_HO_HOS06_S_reuse_p_1bfb19894a

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/4/symbol; canonical SHA-256: d563822a02ff1cd27784f53df621d6ca99707d5b602115ff5a93bf409fe81d1f

SO_HO_HOS06_S_reuse_p_1bfb19894a

#### Native item 6

Native pointer: /joint_analysis/target/fixed_parameters/5; canonical SHA-256: 081dbd5f848166aa1f3fa71c7ef12e2b3fd2ee1dc047202575fff2c4fa749ad7

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/5/domain; canonical SHA-256: 075ddd0032478c5f16981a07e120e5b0794f92458b97d204c3a70d1be622ff45

strictly positive admissible public bound

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/5/parameter_ref; canonical SHA-256: ed68a704c652d42876f81a0d09952ff55da2e27943967e15748f7d748bfebc8d

SO_HO_HOS06_S_reuse_p_45d020550f

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/5/symbol; canonical SHA-256: ed68a704c652d42876f81a0d09952ff55da2e27943967e15748f7d748bfebc8d

SO_HO_HOS06_S_reuse_p_45d020550f

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 18cffcbcf2e22897c060a80d6c3f9f73795ea9a55cf85cea7ff1cbe6836abe22

r4 (the fixed reusable-handle contract): integer d>=1, positive Delta,beta,M_2,sigma_1,sigma_2,G, and independent 0<epsilon_g,epsilon_H<=1. Primary fixed-scale asymptotics vary d and both tolerances jointly. Native q1/q4 fix the six structural bounds; q2/q3 retain all nine tracked parameters and their explicit uniform formulas (their comparison constant_dependencies are empty). No quantity metadata is changed. The guarantee is main/g1, per-instance success >=2/3, with worst-case native vector (N_g,N_H), and exactly the declared q1 sum, q2 gradient, q3 Hessian and q4 vector projections.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 6cddb69989809494de7f38260049eb2e474d6af19e8540e148add121dfc880c8

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 2ecb34469159a73a5807d6bbb38979eeae6bd9a36401165fdfd3de250e3f154b

SO_HO_HOS06_S_reuse_p_e96612ebbf

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: dee5fc2dfdf211a1cb08b119a0e75c6f1e7a6160ed75db9baffbe19f1f31a77a

SO_HO_HOS06_S_reuse_p_70bbfec331

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 112fcb7b9c4aa8c1ea4716ab8aff63157ea852ecbd0403a628c13f773735d2ec

SO_HO_HOS06_S_reuse_p_e4bfdcb515

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 6cddb69989809494de7f38260049eb2e474d6af19e8540e148add121dfc880c8

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 2ecb34469159a73a5807d6bbb38979eeae6bd9a36401165fdfd3de250e3f154b

SO_HO_HOS06_S_reuse_p_e96612ebbf

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: dee5fc2dfdf211a1cb08b119a0e75c6f1e7a6160ed75db9baffbe19f1f31a77a

SO_HO_HOS06_S_reuse_p_70bbfec331

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 112fcb7b9c4aa8c1ea4716ab8aff63157ea852ecbd0403a628c13f773735d2ec

SO_HO_HOS06_S_reuse_p_e4bfdcb515

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Qian Chen; Wendao Wu; Haihan Zhang; Chenheng Zhang; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Complexity for Second-Order Stationary Point with Sample Reuse. arXiv:2610.16832v2 (2026-10-19); latest history checked 2026-10-29.

https://arxiv.org/pdf/2610.16832v2
