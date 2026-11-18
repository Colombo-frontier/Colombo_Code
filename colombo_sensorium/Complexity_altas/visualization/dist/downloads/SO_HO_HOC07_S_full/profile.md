# Convex minimization with higher-order Hölder regularity in normed geometry: full-space queries

**Setting ID.** `SO_HO_HOC07_S_full`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Polynomial gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Full space; geometry: Norm ball; smoothness: Kth derivative holder

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Full jet; operation: Exact jet k; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic algorithms; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is convex and $C^k$.

There exists a global minimizer $x^*$ satisfying $\|x^*-x_0\|_p\le R$.

$$\|D^{k}f(x)-D^{k}f(y)\|_{\mathrm{op},p}\le M_{k,\nu}\|x-y\|_{p}^{\nu}.$$

Fix $k\ge2$ and $0<\nu\le1$; the tensor norm is induced by the stated vector norm. Finite norm exponents satisfy $1\le p<\infty$.

### Oracle interface

Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $M_{k,\nu}$, $\nu$, $R$, $\varepsilon_f$, $p$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

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

$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,k\}$ and $D^0f=f$.

$\|T\|_{\mathrm{op}},\ \|T\|_{\mathrm{op},2}$: Induced operator norm of a Euclidean multilinear tensor; the spectral norm for matrices.

$$\|T\|_{\mathrm{op}}=\|T\|_{\mathrm{op},2}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|.$$

$\mathcal{E}$: Base error defined in the metric specification; expectation or probability aggregation is imposed by the guarantee.

$N$: Total number of original oracle calls; the unit cost is specified in the resource convention. **Domain:** $N\in\mathbb{Z}_{\ge0}$.

$T^*$: Minimum worst-case budget for one algorithm to meet the requirement on the full instance class, within the specified regime, guarantee and resource projection. Expected-resource specifications instead minimize the per-instance expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching bounds up to constants, and upper bounds omitting the declared logarithmic factors. **Domain:** Hidden constants, fixed parameters, and omitted logarithmic variables are specified for each bound.

$\inf,\sup,\min,\max$: Infimum, supremum, attained minimum and attained maximum.

$c,C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<c,C<\infty$.

$J_{k}f(x)$: Function value and the complete tuple of derivatives from order one through the specified maximum order.

$$J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x)).$$

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$\|x\|_p,\ \|x\|_\infty$: Finite-exponent vector norms and the maximum-coordinate norm.

$$\|x\|_p=\left(\sum_{i=1}^d|x_i|^p\right)^{1/p},\qquad\|x\|_\infty=\max_i|x_i|.$$

$\|T\|_{\mathrm{op},p}$: Replace every Euclidean unit ball in the tensor operator-norm definition by the $\ell_p$ unit ball; define $p=\infty$ analogously.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{+}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}, k\ge2$.

$M_{k,\nu}$: Global $\nu$-Hölder upper bound for the order-$k$ derivative in the specified tensor norm. **Domain:** $M_{k,\nu}\ge0$.

$\nu$: Hölder exponent of the highest derivative **Domain:** $0<\nu\le1$.

$s$: Sum of the highest derivative order and its Hölder exponent. **Domain:** $s>2$.

$$s=k+\nu.$$

$R$: Upper bound on the distance from the known initial point to at least one global minimizer. **Domain:** $R\ge0$.

$\varepsilon_f$: Objective-gap tolerance **Domain:** $\varepsilon_f>0$.

$p$: Finite norm exponent of the vector space. **Domain:** $1\le p<\infty$.

$p^*$: Conjugate norm exponent.

$$p^*=\frac{p}{p-1}\ (p>1),\qquad p^*=\infty\ (p=1).$$

$m_p$: Auxiliary exponent determined by the norm geometry. **Domain:** $m_p\ge2$.

$$m_p=\max\{2,p\}.$$

$a_p$: High-order complexity exponent for the corresponding norm geometry. **Domain:** $a_p>0$.

$$a_p=\frac{m_p}{(m_p+1)\,s-(m_p)}.$$

$a$: Complexity exponent associated with the highest-order regularity. **Domain:** $a>0$.

$$a=\frac{2}{3\,s-(2)}.$$

$C_{k,\nu,p}$: Sufficient window constants depending only on the fixed orders or exponents in their subscripts; existence is asserted without numerical values. **Domain:** $C_{k,\nu,p}>1$.

$\mathcal{Q}$: Dimensionless ratio formed from the highest-order regularity, radius, and target accuracy; distinct from the feasible set $Q$. **Domain:** $\mathcal{Q}\ge0$.

$$\mathcal{Q}=\frac{M_{k,\nu}\,(R)^{s}}{\varepsilon_f}.$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q5 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q6 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Sufficiently high dimension for deterministic Euclidean bounds

**Region.** $p=2,\ d\ge C_{k,\nu}(1+\mathcal{Q}^{2/(3s-2)})$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B3

$$
\Omega_{k,\nu}(1+\mathcal{Q}^{2/(3s-2)})
$$

**Upper bound.** B1

$$
O_{k,\nu}(1+\mathcal{Q}^{2/(3s-2)})
$$

**Gap or comparison.** $O_{k,\nu}(1)$

### R2 - The localization or feasible ball degenerates to the initial point

**Region.** $R=0$

**Views.** Deterministic; Randomized

**Quantity.** Q2; Q5

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B5, B11

$$
0
$$

**Upper bound.** B4, B10

$$
0
$$

### R3 - Zero highest-order regularity modulus

**Region.** $M_{k,\nu}=0,\ R>0$

**Views.** Deterministic; Randomized

**Quantity.** Q2; Q5

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B7, B13

$$
1
$$

**Upper bound.** B6, B12

$$
1
$$

**Gap or comparison.** $1$

### R4 - Interior regime for finite p

**Region.** $1<p<\infty$

**Views.** Randomized

**Quantity.** Q4

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Polynomial gap

**Lower bound.** B14

$$
1
$$

**Upper bound.** B8, B15

$$
\min\!\left\{O_{k,\nu,p}(1+\mathcal{Q}^{a_p}),\ \left[1+\left\lceil\frac{\log_2(\max\{1,\mathcal{Q}\})}{s}\right\rceil\right]_{\mathcal{Q}\le1\ \mathrm{or}\ d=1}\right\}
$$

**Gap or comparison.** $1$ for $0<\mathcal{Q}\le1$; $O_{k,\nu}(1+\log\mathcal{Q})$ for $d=1,\mathcal{Q}>1$; $O_{k,\nu,p}(1+\mathcal{Q}^{a_p})$ otherwise.

### R5 - Exact one-call Taylor saturation

**Region.** $M_{k,\nu}>0,\ R>0,\ 1<p<\infty,\ 0<\mathcal{Q}\le1$

**Views.** Randomized

**Quantity.** Q4

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B14

$$
1
$$

**Upper bound.** B15

$$
1
$$

**Gap or comparison.** Exactly one complete-jet query; ratio one on the stated sufficient saturation region.

**Comparison argument.** The SATURATION and LOWER parts of HO_FULL_TAYLOR_BISECTION_20261115 give upper=lower=1 on this exact region. This registers their existing consequence; the one-query threshold is sufficient, not proved maximal.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Non-Euclidean adaptive accelerated proximal and Taylor models

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu,p}(1+\mathcal{Q}^{a_p})
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $1<p<\infty$

**Dimension conditions.** $1<p<\infty$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [1](https://arxiv.org/pdf/2411.08987v2) pdf pages: 8; theorem: Theorem 10; proof pp.29–31

### B2 - Norm replacement with $\widehat p=1+1/\log(ed)$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu}(1+\mathcal{Q}^{2/(3s-2)}[\log(ed)]^{s/(3s-2)})
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $p=1$

**Dimension conditions.** $p=1$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [1](https://arxiv.org/pdf/2411.08987v2) pdf pages: 10; theorem: Fact 7, Remark 15, proof of Theorem 10 pp.29–31

### B3 - Euclidean Hölder resisting chain

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega_{k,\nu}(1+\mathcal{Q}^{2/(3s-2)})
$$

**Conditions.** $p=2,\ d\ge C_{k,\nu}(1+\mathcal{Q}^{2/(3s-2)})$

**Dimension conditions.** $p=2,\ d\ge C_{k,\nu}(1+\mathcal{Q}^{2/(3s-2)})$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** HO_CONVEX_CHAIN

### B4 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $R=0$

**Dimension conditions.** $R=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** HO_ENDPOINTS

### B5 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $R=0$

**Dimension conditions.** $R=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** HO_ENDPOINTS

### B6 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_{k,\nu}=0,\ R>0$

**Dimension conditions.** $M_{k,\nu}=0,\ R>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** HO_ENDPOINTS

### B7 - Two admissible instances indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $M_{k,\nu}=0,\ R>0$

**Dimension conditions.** $M_{k,\nu}=0,\ R>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** HO_ENDPOINTS

### B8 - Non-Euclidean adaptive accelerated proximal and Taylor models

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu,p}(1+\mathcal{Q}^{a_p})
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $1<p<\infty$

**Dimension conditions.** $1<p<\infty$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [1](https://arxiv.org/pdf/2411.08987v2) pdf pages: 8; theorem: Theorem 10; proof pp.29–31

### B9 - Norm replacement with $\widehat p=1+1/\log(ed)$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu}(1+\mathcal{Q}^{2/(3s-2)}[\log(ed)]^{s/(3s-2)})
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $p=1$

**Dimension conditions.** $p=1$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [1](https://arxiv.org/pdf/2411.08987v2) pdf pages: 10; theorem: Fact 7, Remark 15, proof of Theorem 10 pp.29–31

### B10 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $R=0$

**Dimension conditions.** $R=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** HO_ENDPOINTS

### B11 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $R=0$

**Dimension conditions.** $R=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** HO_ENDPOINTS

### B12 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_{k,\nu}=0,\ R>0$

**Dimension conditions.** $M_{k,\nu}=0,\ R>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** HO_ENDPOINTS

### B13 - Two admissible instances indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $M_{k,\nu}=0,\ R>0$

**Dimension conditions.** $M_{k,\nu}=0,\ R>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** HO_ENDPOINTS

### B14 - Two translated quadratics exclude zero queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $1<p<\infty$

**Dimension conditions.** $1<p<\infty$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** HO_FULL_TAYLOR_BISECTION_20261115

### B15 - Taylor minimization; in d=1, derivative bisection before the final Taylor query

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
1+\left\lceil\frac{\log_2(\max\{1,\mathcal{Q}\})}{s}\right\rceil
$$

**Conditions.** $M_{k,\nu},R>0,\ 1<p<\infty,\ (\mathcal{Q}\le1\ \mathrm{or}\ d=1)$

**Dimension conditions.** $d\ge1$ when $\mathcal{Q}\le1$; otherwise $d=1$.

**Guarantee conversion.** Deterministic objective-gap success on every instance, hence probability one and in particular at least 2/3.

**Local argument.** HO_FULL_TAYLOR_BISECTION_20261115

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: ac121ca867f94f19c0f73e498afa0edb22bc0413fcf46f4ad0de9c6f797646f5

### Native proof: HO_CONVEX_CHAIN

Native pointer: /proofs/0; canonical SHA-256: 153eef0b9ac7cde06c81b4242660b274b8ba58b6c2903f6506928823d37c2df1

#### Native field: algorithm_scope

Native pointer: /proofs/0/algorithm_scope; canonical SHA-256: 8ea022d2b48a8ed7971c590b21b0417d67ccd1463d2129f8dfb751fc5169f238

Arbitrary deterministic complete-jet algorithms, including unqueried outputs. No randomized lower bound follows from the resisting-rotation argument. Constants depend only on fixed derivative order and Hölder exponent.

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 276683a605d4e1bf1aee0878268c133488f9de3b735f68c54e98407ef178f9d1

For $N\ge2$, define
$$h_N(z)=\frac1s\left(\sum_{i=1}^{N-1}|z_i-z_{i+1}|^s+|z_N|^s\right)-z_1.$$
Let $A$ be the forward-difference matrix with a terminal row. Its Euclidean operator norm is at most two. The first $k$ derivatives of $|u|^s/s$ vanish at zero, and its kth derivative has a $\nu$-Hölder modulus depending only on $k,\nu$. Applying Hölder's inequality with exponents $s/\nu,s,\ldots,s$ gives
$$|[D^kh_N(z)-D^kh_N(w)][u_1,\ldots,u_k]|
\le H_{k,\nu}\|z-w\|_2^\nu\prod_j\|u_j\|_2,$$
with $H_{k,\nu}$ independent of $N$.

The minimizer is $z^*=(N,N-1,\ldots,1)$, with
$$h_N(0)-h_N(z^*)=(s-1)N/s,\qquad
\|z^*\|^2=N(N+1)(2N+1)/6.$$
If $z_{t+1}=\cdots=z_N=0$, then the remaining chain gives
$$h_N(z)-h_N(z^*)\ge(s-1)(N-t)/s,\qquad
\|\nabla h_N(z)\|\ge1/\sqrt{t+1}.$$
For the gradient inequality, the first $t+1$ gradient coordinates sum to $-1$, and Cauchy–Schwarz applies.

For any deterministic adaptive algorithm making $T$ queries, select orthonormal chain directions successively, orthogonal to previous directions and the query displacements seen so far. Vanishing derivatives of unrevealed terms ensure that each complete jet exposes at most the next direction. After the output is determined, choose the remaining hidden directions orthogonal to that output too. The sufficient dimension $d\ge N+T+1$ leaves room for these choices. The final function
$$f(x)=\alpha h_N(V^\top(x-x_0)/b)$$
is one fixed admissible instance consistent with the entire transcript. This construction does not select a separate instance after seeing a randomized algorithm's private seed.

For a radius promise, take $b=R/\|z^*\|$ and $\alpha=M_{k,\nu}b^s/H_{k,\nu}$. Choosing $N=2T+2$ for objective gap or $N=T+2$ for gradient norm gives
$$\operatorname{gap}(T)\ge\frac{c_{k,\nu}M_{k,\nu}R^s}{(T+1)^{(3s-2)/2}},\qquad
\operatorname{grad}_R(T)\ge\frac{c_{k,\nu}M_{k,\nu}R^{s-1}}{(T+1)^{(3s-2)/2}}.$$
For an initial-gap promise, set $\alpha=\Delta s/((s-1)N)$ and $b=(\alpha H_{k,\nu}/M_{k,\nu})^{1/s}$. Then
$$\operatorname{grad}_\Delta(T)\ge\frac{c_{k,\nu}M_{k,\nu}^{1/s}\Delta^{(s-1)/s}}{(T+1)^{(3s-2)/(2s)}}.$$
Inverting these inequalities yields the linked bounds with a sufficient dimension proportional to one plus the complexity scale. The minimizer lies in the localization ball, so the same hard subclass is admissible for ball-restricted optimization.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: 918705965626e3df518889587e400c0256e29c0f4de1cd53ae94b6c6343683b9

The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 8ea022d2b48a8ed7971c590b21b0417d67ccd1463d2129f8dfb751fc5169f238

Arbitrary deterministic complete-jet algorithms, including unqueried outputs. No randomized lower bound follows from the resisting-rotation argument. Constants depend only on fixed derivative order and Hölder exponent.

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: 15230f4be795cb5d810a6b257f8c7cd4cf2984b68e63b00bf4ea2756b6af7d8e

For fixed $s=k+\nu>2$, the construction gives deterministic lower bounds for objective accuracy and gradient norm, including arbitrary unqueried outputs.

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: c5f31b12c8e70584272c0fad3a05ecf09d31fa8727efc8eb5f1aea881ad138f4

A dimension-controlled convex high-order resisting chain

### Native proof: HO_ENDPOINTS

Native pointer: /proofs/1; canonical SHA-256: b4cae642401d5d94cdce40203762dbe2dcc36171225cbeaa38b31ba59414bf25

#### Native field: algorithm_scope

Native pointer: /proofs/1/algorithm_scope; canonical SHA-256: 27db664d8739f6b71895cf9307c2fa51fca46dfdb4289ac2f8415d525f164282

Applies only to the indicated objective-gap, first-order, or spectral second-order criteria. A true minimizer need not satisfy a finite-radius high-order Taylor-decrease criterion; those criteria require their own argument. Public-domain, curvature, and accuracy conditions remain those of the linked bound.

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: b8837d30d87467eb5722fd001e1a97c4b20caf0f43e28cf131ec6217446632ed

For a full-space differentiable objective with $f(x_0)-\inf f\le\Delta$, the condition $\Delta=0$ makes $x_0$ a global minimizer. Its gradient is zero, and its Hessian is positive semidefinite whenever it exists. Thus first-order and spectral second-order stationarity require no query. An objective-gap target also requires no query when $\varepsilon_f\ge\Delta$. Nonnegative query cost proves exact optimality of these zero bounds.

If a public gradient-Lipschitz bound $\beta$ is part of the specification, the descent lemma gives $\|\nabla f(x_0)\|^2\le2\beta\Delta$. For convex full-space objectives with a minimizer within distance $R$, it also gives $f(x_0)-f^*\le\beta R^2/2$ and $\|\nabla f(x_0)\|\le\beta R$. These sufficient zero-query regions require that explicit first-order regularity assumption. If only the highest derivative is controlled, positive quadratics can have arbitrary curvature and arbitrarily large initial gap despite zero highest-order modulus.

On a connected Euclidean domain, $M_k=0$ or $M_{k,\nu}=0$ makes $D^kf$ constant, so $f$ is a polynomial of degree at most $k$. One complete jet determines all coefficients. Under the specified free internal computation, a known polynomial can then be optimized on a compact public domain, or combined with a public regularizer and solved through the declared known-model interface.

A bounded-below polynomial on the full space need not attain its infimum. For approximate spectral stationarity, shift $x_0$ to zero and minimize $f(x)+\eta\|x\|^2/2$. This function is coercive, and its minimizer $x_\eta$ satisfies $\eta\|x_\eta\|^2/2\le\Delta$, $\|\nabla f(x_\eta)\|\le\sqrt{2\eta\Delta}$, and $\nabla^2f(x_\eta)\succeq-\eta I$. Choosing $\eta\le\min\{\varepsilon_H,\varepsilon_g^2/(2\Delta)\}$ meets both targets. For global objective accuracy, exact polynomial coefficients permit arbitrary-accuracy internal global optimization; no additional unknown-function query is needed.

To exclude zero queries in a nontrivial region, choose two positive quadratics centered on opposite sides of $x_0$, with the same public budgets and disjoint acceptable-output sets. A zero-query algorithm has the same output distribution on both instances, so their success probabilities sum to at most one. It cannot succeed with probability at least $2/3$ on each. With only highest-order regularity, curvature can be increased until the acceptable sets are disjoint at any prescribed positive accuracy and positive localization radius. In an initial-gap model with additional curvature restrictions, retain the bound's explicit accuracy and compatibility window.

If both a global PL constant $\mu$ and a gradient-Lipschitz upper bound $\beta$ are supplied, then $2\mu(f-f_*)\le\|\nabla f\|^2\le2\beta(f-f_*)$. When $\mu>\beta>0$, every gap is zero and the class contains only constant objectives. This degeneracy does not apply without the extra $\beta$ assumption.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: 918705965626e3df518889587e400c0256e29c0f4de1cd53ae94b6c6343683b9

The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 27db664d8739f6b71895cf9307c2fa51fca46dfdb4289ac2f8415d525f164282

Applies only to the indicated objective-gap, first-order, or spectral second-order criteria. A true minimizer need not satisfy a finite-radius high-order Taylor-decrease criterion; those criteria require their own argument. Public-domain, curvature, and accuracy conditions remain those of the linked bound.

#### Native field: statement

Native pointer: /proofs/1/statement; canonical SHA-256: d4c17587463f6cf74fa2d09f365b89376efcf35723b4f888b5f6d669473ecfbc

Zero-query guarantees follow from a public initial-error bound. A zero highest-order regularity modulus permits exact polynomial recovery from one complete jet.

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 4e8cc661512a877d5023d683fef209a064798f2e93b413a01bdea7d1779a245f

Zero-query and polynomial-recovery endpoints

### Native proof: HO_FULL_TAYLOR_BISECTION_20261115

Native pointer: /proofs/2; canonical SHA-256: 2c47273f081e54495074c38b5c6c76fa0c0ce5bbab30d56ddd654a02cc02cebd

#### Native field: algorithm_scope

Native pointer: /proofs/2/algorithm_scope; canonical SHA-256: c104992e08b3945984f28483b70ebe1f98f51c84fc8e462a0373d9d1b0ee6b00

Arbitrary measurable randomized adaptive algorithms for the lower bound; a deterministic full-jet algorithm witnesses both upper bounds. The target is randomized q1, g1, resource_23a9ec40f1. No quantity-ID equivalence is used.

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: 3fc0c8045ef25674ce70cbff4176084ed656ca581c841bf624549c5561fa9e73

Retained premises: /common_specification (59c0726f7ecbd97a7790da4a305ad361206a8f196e5c2054ec025b5f48ba19da), /views/1 (873400a618391c5f34909dcf88fc74ed8a4171d0eb99793f280fd666407a1bbd), /quantities/3 (e98d41b2d6b04dc44923b7282c5370210ad87a839c73cc1b7593686549b8f74a), and /proofs/1 (b4cae642401d5d94cdce40203762dbe2dcc36171225cbeaa38b31ba59414bf25). No external theorem is introduced.
LOWER: Fix public parameters with R>0. Let a_plus=x0+R e1 and a_minus=x0-R e1, and f_plus/minus(x)=A||x-a_plus/minus||_2^2, where A>epsilon_f/R^2. Both objectives are convex C^infinity, have a minimizer at lp-distance R, and have constant kth derivative for k=2 or zero kth derivative for k>2. Thus their kth-derivative Holder modulus is zero and is admissible under any public upper bound M. Their epsilon_f-optimal sets are disjoint Euclidean balls of radius sqrt(epsilon_f/A)<R. Without a query the output distribution is identical for both objectives, so its probabilities of belonging to these disjoint sets sum to at most one. It cannot succeed with probability at least 2/3 for each fixed instance. Oracle counts are integers, so every worst-path budget B<1 permits zero queries and fails; C*>=1.
TAYLOR: At a queried point c let T_c(x)=sum_{j=0}^k D^j f(c)[x-c]^j/j!. For h=x-c, repeated integration along c+t h gives f(c+h)-T_c(c+h)=1/(k-1)! integral_0^1 (1-t)^(k-1) (D^k f(c+t h)-D^k f(c))[h,...,h] dt. Consequently |f(c+h)-T_c(c+h)| <= M||h||_p^(k+nu)/k! <= M||h||_p^s/2, because t^nu<=1 and k>=2. If a known compact set K contains a global minimizer and is contained in B_p(c,r), select a global minimizer y of the known polynomial T_c on K. Existence follows from continuity and compactness; the declared free internal operations permit its selection without another unknown-function response. The two remainder inequalities and T_c(y)<=T_c(x*) give f(y)-f*<=M r^s. All lower-order derivatives, even when arbitrarily large, are included exactly in T_c.
SATURATION: Query at x0 and use K=B_p(x0,R). The localization promise puts x* in K, hence error<=M R^s. Thus Q=M R^s/epsilon_f<=1 suffices for one query in every dimension. Together with LOWER, C*=1. Q=1 is included by a non-strict inequality. This is a sufficient threshold, not a claimed maximal one-query domain.
ONE DIMENSION: Every finite lp norm equals absolute value. Set n=1+ceil(log2(max{1,Q})/s). Begin with I=[x0-R,x0+R], which contains a global minimizer. For the first n-1 queries, query the midpoint c. If f'(c)=0, convexity makes c globally optimal and return it. If f'(c)>0 keep the left closed half; if f'(c)<0 keep the right closed half. Convexity preserves a global minimizer in the retained interval, including possible endpoint minimizers. Unless already terminated, the nth query is the midpoint of the current pre-cut interval, whose radius is r=R*2^(-(n-1)). Minimize that query's known Taylor polynomial on that interval and return its minimizer without an extra oracle query. Its error is at most M r^s<=epsilon_f because Q*2^(-s(n-1))<=1. Total responses on every path are at most n. All query choices and a fixed measurable minimizer selection depend only on public inputs and received jets. The deterministic success guarantee implies success probability one in the randomized view, with the identical fixed-path cost.
BOUNDARIES: R=0 remains the separate zero-query q2 endpoint, and M=0,R>0 remains the separate polynomial-recovery q2 endpoint. This proof neither transfers q2/q3 bounds to q1 nor uses a randomized resisting rotation.

#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: 97ed44645b1db850c2519c82d1c015cd3d3c4214f4313191b568d7f307c67b85

No logarithmic lower bound, no d>=2 main-rate improvement when Q>1, and no sharp one-query activation boundary are asserted. The p=1 quantity and deterministic-view adoption are outside this local patch.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 3fffacfda1727703ba2363a74d11b3c9a7409d050a850dddcb1fd418a558b6cb

M>0, R>0, epsilon_f>0, d>=1, k>=2, 0<nu<=1, 1<p<infinity. The upper bound is adopted only when Q<=1 or d=1.

#### Native field: statement

Native pointer: /proofs/2/statement; canonical SHA-256: 7b65e7ec8d5be4647bd9821609826959193c7ea62321e2666c74a91d6de09f7c

For randomized q1 on its positive finite-p domain, C* >= 1. It equals 1 when 0<Q<=1. On d=1 it is at most 1+ceil(log2(max{1,Q})/(k+nu)).

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: cc57aef6701852330c97b662094b7033a4ab4df8cffc3a657c8c834bdd0307ee

Taylor saturation and one-dimensional bisection under a full-jet budget

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 3d45b31c5ac758468b72a340d0a331322eb6a49b22dde445927c7391e6e50c80

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: f7b927a270f7920e1130bbbf22a3a9cc4fc610f7092593894f35f59fc1ee7cdb

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 88b6d6357fd4df76fa66d1b1b57f67bca9b7964830c5b5b8b9f3b707a264eb2f

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 5c2e463adaaac86c50026be048f43643e302cae626fe743929ec80386deb9f1a

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: a80a04aa7e1abe1fffdba6156936c8e60aaccbafec5196c487ec2454f3a46913

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 3c3c9b834357f77e2cdb89e0221cfd7d27232622d3e10fc7681143928ded53b9

SO_HO_HOC07_S_full__deterministic__r4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 205d8d1c2f10c9c5187e2076b6fc93dc02270a6285523e8988f3ffe7ef169eff

SO_HO_HOC07_S_full__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 2e2aac1f68c2cc0c4da000b77f15fa6fca47f4a1391b675505a094ece495652f

Retain frozen scientific contract and guard conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 3e6885d1d8eefdfe1eb64684dce44f9099c0314dfb25a580a7430d6b81d53543

SO_HO_HOC07_S_full__deterministic__r3

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: b1568761f0d07dc3054d0cab48cdcb7c3c244032ecdb5595536adc36dcf6db5c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 3c3c9b834357f77e2cdb89e0221cfd7d27232622d3e10fc7681143928ded53b9

SO_HO_HOC07_S_full__deterministic__r4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 308f3613ad2a3ecf57ca46b14d3c5fb444515f3f1bf17a2d83573fc09c3b038e

SO_HO_HOC07_S_full__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: bd7914634dd18e5dcbe1fe1c2d55031e67e2450758b989e880cbc4cda8f57ba6

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 92b1a6147b4e3c4f1a5e9e1c539f5f042480db00db87fbd4358a20c2b533549c

HO_CONVEX_CHAIN

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 2e2aac1f68c2cc0c4da000b77f15fa6fca47f4a1391b675505a094ece495652f

Retain frozen scientific contract and guard conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 3c3c9b834357f77e2cdb89e0221cfd7d27232622d3e10fc7681143928ded53b9

SO_HO_HOC07_S_full__deterministic__r4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: aab444377797724dbdd58a2d38b7d57b1d28ffd1a385b0bc58e47045ac7ce991

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: b4998bdac686b99c7dbddc69d6df19ac3d6772897c063cde8ab0bd07d73faf22

All main-rate statements exclude M=0 and R=0.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 3a8e410335be5c246802994e25fa3c8ac13983ecf2d056de0873660351c443fa

Dimension restrictions are sufficient source/proof applicability conditions, not intrinsic phase transitions.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 53714398fa37266ae95f8746edbbaef47409835f21441c980b70f9509e991db7

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/0; canonical SHA-256: 71ef2135560b4492a70fc1492c2fa2ee883f07c90849ee5398cf6cc815ac3ca1

SO_HO_HOC07_S_full_p_5ca4632155

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/1; canonical SHA-256: a63eb8589904175a9afbd68d8954c257780392fb9bc988236c076bc9829cdf65

SO_HO_HOC07_S_full_p_573ff14ac8

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 3d90c82354370fd2c3d6eddea92616d228bc6965cd23589f0f0095167d0859e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/0; canonical SHA-256: 71ef2135560b4492a70fc1492c2fa2ee883f07c90849ee5398cf6cc815ac3ca1

SO_HO_HOC07_S_full_p_5ca4632155

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/1; canonical SHA-256: a63eb8589904175a9afbd68d8954c257780392fb9bc988236c076bc9829cdf65

SO_HO_HOC07_S_full_p_573ff14ac8

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/2; canonical SHA-256: d3cbe48ec13be2b9294ee718ca8f1707da2f655e1ac7817b88fa717dbe790473

SO_HO_HOC07_S_full_p_07b6ef0c28

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: b44408cf0ab36ed88bdd4d889dcb1c3423e13372db6429814b18f611b505f12e

$O_{k,\nu}(1)$

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 656a80f24248426d149ca3efc9a5f553bbd36901e8968fc6f588214c2c956402

\Omega_{k,\nu}(1+\mathcal{Q}^{2/(3s-2)})

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 533007337a62c38e29a9f246409b3d838b52cfd43ed7070cb5b397819317d86d

None in this comparison, conditional on the frozen baseline; outside its guard is unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 12b7dc0c08caee3722d4b6d0d61108f0b17040b2c6e6bda08d27f668d4f21da0

O_{k,\nu}(1+\mathcal{Q}^{2/(3s-2)})

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 7ea1aa6dad065be14c984691016c993c6ed643b4a1f756641a0c89d401106e82

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 5855339dac87ba0461d4239e8dbaf231a62e7d0c7da2ae7d8d86e19bc0ec2920

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 40dfe32ec2889acdc6e1f8724615415fe97bedffb8e045daf401313c93bafaa4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 01580d95458dd03ab78590c3eb03f81f51dd5f28edd437df349e44a28a48f02e

SO_HO_HOC07_S_full__deterministic__r7

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 83f0ac1f500c7fe9c385b748c18bd4e867f70d4bc3c9086dca567625ab1df4d5

SO_HO_HOC07_S_full__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 2e2aac1f68c2cc0c4da000b77f15fa6fca47f4a1391b675505a094ece495652f

Retain frozen scientific contract and guard conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 01580d95458dd03ab78590c3eb03f81f51dd5f28edd437df349e44a28a48f02e

SO_HO_HOC07_S_full__deterministic__r7

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 5dcafec79b2c49c2f64500f8e8b33c14662c84ce222b7f25adc4135cf57a724d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 01580d95458dd03ab78590c3eb03f81f51dd5f28edd437df349e44a28a48f02e

SO_HO_HOC07_S_full__deterministic__r7

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 8702620a814f0ed501c17dc0d415138a972ab99a2b96c9b4198f06e4c1d47167

SO_HO_HOC07_S_full__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 2e2aac1f68c2cc0c4da000b77f15fa6fca47f4a1391b675505a094ece495652f

Retain frozen scientific contract and guard conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 01580d95458dd03ab78590c3eb03f81f51dd5f28edd437df349e44a28a48f02e

SO_HO_HOC07_S_full__deterministic__r7

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 8e0b512151b8ff0b7e8348ec011e3ee63cecab487942197a4fa34461566cb4b9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: f67057f2bb9b9bced72783cfb69752670d10f042b6deb3ba05b661e7a5d92cc4

SO_HO_HOC07_S_full__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 668fbb7c895003717efa71d263d36e570058649178204d8d52e411b1616b87fc

Disjoint endpoint guard; not active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: db5deb6ccd0e11aa1451d0cb8920e233ea31e84d786f925c73b2f18e89c7e7e8

SO_HO_HOC07_S_full__deterministic__r8

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: 2812636f49c16c00514912d084f9a4c8d4d20b0a9e5badcf4c3a55ca5f176e0c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: fb327adae86fbfbf634e6bed1126e770466fc5deaa9ca0e5c236a9b50e9fdb1e

SO_HO_HOC07_S_full__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 668fbb7c895003717efa71d263d36e570058649178204d8d52e411b1616b87fc

Disjoint endpoint guard; not active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: db5deb6ccd0e11aa1451d0cb8920e233ea31e84d786f925c73b2f18e89c7e7e8

SO_HO_HOC07_S_full__deterministic__r8

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 6e388fd864d306c922220a32481471051ad06d4262a2dc5b36e7e3d121d68629

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 8482e9dc2f997447c3ec121a1bd039fae770dd0a7ac3261a85da3a32856616f4

R=0 includes M=0: x0 is a promised global minimizer, so exact cost is zero. Q=0 alone cannot distinguish this branch from M=0,R>0.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: fac92a0584cf87af91b5ad8cbd3c7936075a2529d83858b6110abe04be35eb9b

Ratio inapplicable: both costs are exactly zero.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 533007337a62c38e29a9f246409b3d838b52cfd43ed7070cb5b397819317d86d

None in this comparison, conditional on the frozen baseline; outside its guard is unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 67d3bf8fa88bc221599fa862542cbb10a91bd9b2376d64545a6a96f4ae85056d

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 2d9347fb5a0c5fdb9a937148b98a8a3b95d9bc73cd3dece1205bc8ecc88d2f75

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 8deb2d18913af688b86d15f64c608c01cb2909ab361740d19bfa22414ed92d77

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: 83f0ac1f500c7fe9c385b748c18bd4e867f70d4bc3c9086dca567625ab1df4d5

SO_HO_HOC07_S_full__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 668fbb7c895003717efa71d263d36e570058649178204d8d52e411b1616b87fc

Disjoint endpoint guard; not active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 01580d95458dd03ab78590c3eb03f81f51dd5f28edd437df349e44a28a48f02e

SO_HO_HOC07_S_full__deterministic__r7

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: abc5cd80da9818b6e4de0975c8e3287c847896f469cd4b2e796ad8db689bc929

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 8702620a814f0ed501c17dc0d415138a972ab99a2b96c9b4198f06e4c1d47167

SO_HO_HOC07_S_full__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: 668fbb7c895003717efa71d263d36e570058649178204d8d52e411b1616b87fc

Disjoint endpoint guard; not active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 01580d95458dd03ab78590c3eb03f81f51dd5f28edd437df349e44a28a48f02e

SO_HO_HOC07_S_full__deterministic__r7

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: fdb040147b248a65c66381a3c9282cf70b4e6b01a0a8943cab3d3cd37e3a89f1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: db5deb6ccd0e11aa1451d0cb8920e233ea31e84d786f925c73b2f18e89c7e7e8

SO_HO_HOC07_S_full__deterministic__r8

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: f67057f2bb9b9bced72783cfb69752670d10f042b6deb3ba05b661e7a5d92cc4

SO_HO_HOC07_S_full__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 2e2aac1f68c2cc0c4da000b77f15fa6fca47f4a1391b675505a094ece495652f

Retain frozen scientific contract and guard conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: db5deb6ccd0e11aa1451d0cb8920e233ea31e84d786f925c73b2f18e89c7e7e8

SO_HO_HOC07_S_full__deterministic__r8

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: d3b97adbadb4d5b2b2d6474971bedc53a7fad76b71c54195abc8ce9eb9759e28

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: db5deb6ccd0e11aa1451d0cb8920e233ea31e84d786f925c73b2f18e89c7e7e8

SO_HO_HOC07_S_full__deterministic__r8

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: fb327adae86fbfbf634e6bed1126e770466fc5deaa9ca0e5c236a9b50e9fdb1e

SO_HO_HOC07_S_full__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 2e2aac1f68c2cc0c4da000b77f15fa6fca47f4a1391b675505a094ece495652f

Retain frozen scientific contract and guard conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: db5deb6ccd0e11aa1451d0cb8920e233ea31e84d786f925c73b2f18e89c7e7e8

SO_HO_HOC07_S_full__deterministic__r8

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 017f0cd5542cbaff5d208b707175eda2a8a1830eb5c5a30fe912cfb2c09445c0

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: f6f0e07dde474131cd88311b07d9d341ec98a3c5d14b6eaf446448fde2a0c046

M=0,R>0 is disjoint from R=0; retain exact polynomial-recovery cost one for every positive finite accuracy.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: 9e8a28708309c8e3e08e5432c793bc8be701e3fa5c6570533407e44aff13c94d

$1$

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 533007337a62c38e29a9f246409b3d838b52cfd43ed7070cb5b397819317d86d

None in this comparison, conditional on the frozen baseline; outside its guard is unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 8ca6133225a4d2eb159c43b0e113087e94ec7d89280db65953d06dd151e150de

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 6605b72ddfdfd8cb99f3248a28f0a8b23c9ed7d2d8fe3cf50051e1b1ca92f557

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: 7a5897397781060666a0a10e2fe0671c8264c64b70ea3b316c6e3bade35c3c96

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 96eb3f7f3153b2b727b623c23f2e78f2721eaeee15590af19affaac2bc908029

SO_HO_HOC07_S_full__randomized__r3

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 38a392dbb7d2397b1a36071dd564f84337c8ccffae62771c6dab786a9e54900e

SO_HO_HOC07_S_full__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 2e2aac1f68c2cc0c4da000b77f15fa6fca47f4a1391b675505a094ece495652f

Retain frozen scientific contract and guard conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 96eb3f7f3153b2b727b623c23f2e78f2721eaeee15590af19affaac2bc908029

SO_HO_HOC07_S_full__randomized__r3

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: c87a7271b22d49ff9222d3489f47189f07f80014efedc16167d43b47a1435d76

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: 96eb3f7f3153b2b727b623c23f2e78f2721eaeee15590af19affaac2bc908029

SO_HO_HOC07_S_full__randomized__r3

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 3bdd35ef64238633064d8f2cbabf8a570e4d8f825bb6cc1ea551d1ef6502b42b

SO_HO_HOC07_S_full__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 42490e050279d9daa0999bdc9534a290621f9b77f8b2835259d3bc7a74e01af5

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 271da148b6b5c2a2c5eb00e4aac5b37cef587289dba548ffba093165dc02ebb9

HO_FULL_TAYLOR_BISECTION_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: 57309ebbba24e2573b3be9064eced35ee1509b3e67a8643fe02d674868bdf48a

A new direct quadratic-subclass argument preserves the full-space model, output, per-instance 2/3 guarantee and integer fixed-path query count.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 96eb3f7f3153b2b727b623c23f2e78f2721eaeee15590af19affaac2bc908029

SO_HO_HOC07_S_full__randomized__r3

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 9478a54a317bea7e540908623f7370bece5ce564eed3bf677d021843248d431b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 92b5021f9fdbaeb0c9f87d2b30070730ee0f8237cdb692796d3660364a1f2a21

SO_HO_HOC07_S_full__randomized__r8

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: b472c8df2d4011b84b6db9e404b56da843dd4dcaa3b80a2001009d37cb6c0107

SO_HO_HOC07_S_full__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 42490e050279d9daa0999bdc9534a290621f9b77f8b2835259d3bc7a74e01af5

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 271da148b6b5c2a2c5eb00e4aac5b37cef587289dba548ffba093165dc02ebb9

HO_FULL_TAYLOR_BISECTION_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: e57bc9d8104d0b782e30bbc1131166cd8280deec9d0e1dcd13f4aa90652f1247

Deterministic Taylor witness, admitted to the randomized view with probability one. Keep its guard inside the minimum; on d=1 compare both upper witnesses.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 92b5021f9fdbaeb0c9f87d2b30070730ee0f8237cdb692796d3660364a1f2a21

SO_HO_HOC07_S_full__randomized__r8

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: 08e61c76813454c61d6efaa82c842414c862b76343c03fbaf734aff0b8e4f7d0

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: 308f3613ad2a3ecf57ca46b14d3c5fb444515f3f1bf17a2d83573fc09c3b038e

SO_HO_HOC07_S_full__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: ee7f407b4de059c949ecd79972124957656694252e4e8ad4896e3dd9e5252b30

The deterministic resisting chain is not a lower bound for arbitrary private-randomness algorithms; no distributional transfer is supplied.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 3c3c9b834357f77e2cdb89e0221cfd7d27232622d3e10fc7681143928ded53b9

SO_HO_HOC07_S_full__deterministic__r4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: b93b61946076ba72a68db482c765097bc021b335c84407ab27a02025f0a828b4

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: cbce03c9e94f83e14b8fb4ba53b6b7b68589ed5ab0a8c040dd1c4dabeb77e758

Q=1 is included in the proved one-query region because f(y)-f*<=M R^s<=epsilon_f. The sufficient threshold is not asserted to be sharp.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: bcbc37cd38cb03d944a69cc111948dcd984daf794440a1a579d1e4a45c05fc4f

For d=1 choose n=1+ceil(log2(max{1,Q})/s); at Q=2^(s m), m integer>=0, n=m+1 suffices, including equality.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/boundary_checks/2; canonical SHA-256: 9111b3cbcd3057263bb8349eb39fc4356db58d6aae57d1a03bfb324c5a0a996c

The final Taylor model and its output use no further unknown-function response; a derivative zero permits earlier termination.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/boundary_checks/3; canonical SHA-256: 6cd63967d3f172cf7301aa70e3d1f4abdc0790de186a1607684cf518d2add1ae

Large lower derivatives are queried exactly, not hidden in constants; the Holder remainder is the only approximation error.

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/boundary_checks/4; canonical SHA-256: d135d223b5dca72ac40488e8d0677bb0ee7af91fe124b1866543e215889cdd1f

R=0 and M=0 remain separate q2 endpoints; neither q2 nor q3 is merged into q1.

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/boundary_checks/5; canonical SHA-256: d27d832a33dbb10b19d250a34467e734cf5d0a1410bea8bda9b9e4947962db71

The d=1 logarithmic branch improves the old polynomial rate as Q tends to infinity at fixed k,nu,p. No exact finite crossover with an O-constant is claimed.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 3d90c82354370fd2c3d6eddea92616d228bc6965cd23589f0f0095167d0859e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/0; canonical SHA-256: 71ef2135560b4492a70fc1492c2fa2ee883f07c90849ee5398cf6cc815ac3ca1

SO_HO_HOC07_S_full_p_5ca4632155

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/1; canonical SHA-256: a63eb8589904175a9afbd68d8954c257780392fb9bc988236c076bc9829cdf65

SO_HO_HOC07_S_full_p_573ff14ac8

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/2; canonical SHA-256: d3cbe48ec13be2b9294ee718ca8f1707da2f655e1ac7817b88fa717dbe790473

SO_HO_HOC07_S_full_p_07b6ef0c28

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 3d90c82354370fd2c3d6eddea92616d228bc6965cd23589f0f0095167d0859e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/0; canonical SHA-256: 71ef2135560b4492a70fc1492c2fa2ee883f07c90849ee5398cf6cc815ac3ca1

SO_HO_HOC07_S_full_p_5ca4632155

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/1; canonical SHA-256: a63eb8589904175a9afbd68d8954c257780392fb9bc988236c076bc9829cdf65

SO_HO_HOC07_S_full_p_573ff14ac8

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/2; canonical SHA-256: d3cbe48ec13be2b9294ee718ca8f1707da2f655e1ac7817b88fa717dbe790473

SO_HO_HOC07_S_full_p_07b6ef0c28

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 05b132733821c4db8ab1d7f4a3b3692a5eec239993c0e19f004fb3a74ffc97ea

Exactly 1 for 0<Q<=1; at most min{O_{k,nu,p}(1+Q^a_p),1+ceil(log2 Q/s)} for d=1,Q>1; at most O_{k,nu,p}(1+Q^a_p) for d>=2,Q>1. The denominator is the lower bound 1, not a logarithmic lower bound.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 02ceed316035887b843e20a3305378a04e1a18e5ef136176a36e4647b10b6230

1 on the entire positive-parameter p>1 comparison.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 6a267e56d3599fee586fd0006ef7b40ab464de96788c58189d63b9aaad912c6b

For d=1,Q>1 the recorded lower bound is only 1, leaving a logarithmic upper/lower gap; for d>=2,Q>1 it leaves a polynomial gap. A randomized full-space main-rate lower theorem remains unestablished in this finite check.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: e46dc08d9339f20cb15eb1b467050fab606d83b910547fd1264d98c41bae6a3b

\min\!\left\{O_{k,\nu,p}(1+\mathcal{Q}^{a_p}),\ \left[1+\left\lceil\frac{\log_2(\max\{1,\mathcal{Q}\})}{s}\right\rceil\right]_{\mathcal{Q}\le1\ \mathrm{or}\ d=1}\right\}

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: 1a833324031d7ea24b8335ffb46eca7fd4c7af96db3e4e44fce58c1f3a806b50

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: 07349e7ff1c7a19f1d5a06609bb2e0d0359d8c697c1fef0dc0f441c29b63dd3f

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: c75c0d36938b04b76929c6c8e806e1dfb58389d292522ad786ef3a8c35600b60

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: b2bb30ab2423a2bed4c2b54c1ec6eefeeedb67a2495a81195256ed617b9faf4f

SO_HO_HOC07_S_full__randomized__r6

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: 95140400d37033b7b0f792030b856b83fcb8b01f9afac2dfc3cb2d732ce83b71

SO_HO_HOC07_S_full__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: 2e2aac1f68c2cc0c4da000b77f15fa6fca47f4a1391b675505a094ece495652f

Retain frozen scientific contract and guard conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: b2bb30ab2423a2bed4c2b54c1ec6eefeeedb67a2495a81195256ed617b9faf4f

SO_HO_HOC07_S_full__randomized__r6

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: 0c60bf4cdebc103abba7823f4d1a85ea94a33b3392cdea17e45d94cd1ae4fb01

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: b2bb30ab2423a2bed4c2b54c1ec6eefeeedb67a2495a81195256ed617b9faf4f

SO_HO_HOC07_S_full__randomized__r6

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: f4c639bcf2b99f164924f9ea9f8d3840800311987a57d4c8644082324b442861

SO_HO_HOC07_S_full__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: 2e2aac1f68c2cc0c4da000b77f15fa6fca47f4a1391b675505a094ece495652f

Retain frozen scientific contract and guard conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: b2bb30ab2423a2bed4c2b54c1ec6eefeeedb67a2495a81195256ed617b9faf4f

SO_HO_HOC07_S_full__randomized__r6

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/bound_uses/2; canonical SHA-256: 97d052043cc6f8c28034cc6b4e40fdf26f5bc2bc8289608a0b35a5699cfa110c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/bound_id; canonical SHA-256: af3bcc03396457984950437ba8194b3bb5aa39d311fc302b9df8f8f6d263ad42

SO_HO_HOC07_S_full__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/reason; canonical SHA-256: 668fbb7c895003717efa71d263d36e570058649178204d8d52e411b1616b87fc

Disjoint endpoint guard; not active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/validity_region; canonical SHA-256: 54ac90c154f651442ca4735c05a2ce5828835db96f8f9947196c751cae1bc1f8

SO_HO_HOC07_S_full__randomized__r7

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/bound_uses/3; canonical SHA-256: b41e23d9a00a90b36f928e115a28871dee6cd03f851a98ffa51cd5655e457de6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/bound_id; canonical SHA-256: 193f99499a7b6cbdd91c2524e116c017eaf87924ecde93693184a4dcb474124f

SO_HO_HOC07_S_full__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/reason; canonical SHA-256: 668fbb7c895003717efa71d263d36e570058649178204d8d52e411b1616b87fc

Disjoint endpoint guard; not active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/validity_region; canonical SHA-256: 54ac90c154f651442ca4735c05a2ce5828835db96f8f9947196c751cae1bc1f8

SO_HO_HOC07_S_full__randomized__r7

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: 6e388fd864d306c922220a32481471051ad06d4262a2dc5b36e7e3d121d68629

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: 8482e9dc2f997447c3ec121a1bd039fae770dd0a7ac3261a85da3a32856616f4

R=0 includes M=0: x0 is a promised global minimizer, so exact cost is zero. Q=0 alone cannot distinguish this branch from M=0,R>0.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: fac92a0584cf87af91b5ad8cbd3c7936075a2529d83858b6110abe04be35eb9b

Ratio inapplicable: both costs are exactly zero.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: 533007337a62c38e29a9f246409b3d838b52cfd43ed7070cb5b397819317d86d

None in this comparison, conditional on the frozen baseline; outside its guard is unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native item 6

Native pointer: /joint_analysis/comparisons/5; canonical SHA-256: 95ab02476c0a8a48db28b981d1337a1a88030db9c057556eda675ad3138753db

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/5/bound_uses; canonical SHA-256: 7a7fec29d615ae163335e223ac552e9b9de7de2c4ffd2f67faff747ef8934637

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0; canonical SHA-256: 032a586a6bce0dbb6288a709d74b1cf9ee879efae5a5921241f8e59a91ac7809

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/bound_id; canonical SHA-256: 95140400d37033b7b0f792030b856b83fcb8b01f9afac2dfc3cb2d732ce83b71

SO_HO_HOC07_S_full__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/reason; canonical SHA-256: 668fbb7c895003717efa71d263d36e570058649178204d8d52e411b1616b87fc

Disjoint endpoint guard; not active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/validity_region; canonical SHA-256: b2bb30ab2423a2bed4c2b54c1ec6eefeeedb67a2495a81195256ed617b9faf4f

SO_HO_HOC07_S_full__randomized__r6

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1; canonical SHA-256: 4f7e71177e953771acce67d6346c4fbc5516aca703e6d3e042b6a561adcd5561

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/bound_id; canonical SHA-256: f4c639bcf2b99f164924f9ea9f8d3840800311987a57d4c8644082324b442861

SO_HO_HOC07_S_full__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/reason; canonical SHA-256: 668fbb7c895003717efa71d263d36e570058649178204d8d52e411b1616b87fc

Disjoint endpoint guard; not active.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/validity_region; canonical SHA-256: b2bb30ab2423a2bed4c2b54c1ec6eefeeedb67a2495a81195256ed617b9faf4f

SO_HO_HOC07_S_full__randomized__r6

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/bound_uses/2; canonical SHA-256: f5c7eee4ccb660ec89e1be5e24d47e97bec01fe53d08bd747eae600cf16f9a20

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/adopted_region; canonical SHA-256: 54ac90c154f651442ca4735c05a2ce5828835db96f8f9947196c751cae1bc1f8

SO_HO_HOC07_S_full__randomized__r7

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/bound_id; canonical SHA-256: af3bcc03396457984950437ba8194b3bb5aa39d311fc302b9df8f8f6d263ad42

SO_HO_HOC07_S_full__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/reason; canonical SHA-256: 2e2aac1f68c2cc0c4da000b77f15fa6fca47f4a1391b675505a094ece495652f

Retain frozen scientific contract and guard conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/validity_region; canonical SHA-256: 54ac90c154f651442ca4735c05a2ce5828835db96f8f9947196c751cae1bc1f8

SO_HO_HOC07_S_full__randomized__r7

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/bound_uses/3; canonical SHA-256: 0ffe8a71cf7228a905f5e1a0b273f4f3aac9a51dada8fd6d105237380d6a4634

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/adopted_region; canonical SHA-256: 54ac90c154f651442ca4735c05a2ce5828835db96f8f9947196c751cae1bc1f8

SO_HO_HOC07_S_full__randomized__r7

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/bound_id; canonical SHA-256: 193f99499a7b6cbdd91c2524e116c017eaf87924ecde93693184a4dcb474124f

SO_HO_HOC07_S_full__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/reason; canonical SHA-256: 2e2aac1f68c2cc0c4da000b77f15fa6fca47f4a1391b675505a094ece495652f

Retain frozen scientific contract and guard conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/validity_region; canonical SHA-256: 54ac90c154f651442ca4735c05a2ce5828835db96f8f9947196c751cae1bc1f8

SO_HO_HOC07_S_full__randomized__r7

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/5/boundary_checks; canonical SHA-256: 017f0cd5542cbaff5d208b707175eda2a8a1830eb5c5a30fe912cfb2c09445c0

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/boundary_checks/0; canonical SHA-256: f6f0e07dde474131cd88311b07d9d341ec98a3c5d14b6eaf446448fde2a0c046

M=0,R>0 is disjoint from R=0; retain exact polynomial-recovery cost one for every positive finite accuracy.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/5/comparison_id; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/5/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/5/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/5/gap; canonical SHA-256: 9e8a28708309c8e3e08e5432c793bc8be701e3fa5c6570533407e44aff13c94d

$1$

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/5/lower_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/5/remaining_gap; canonical SHA-256: 533007337a62c38e29a9f246409b3d838b52cfd43ed7070cb5b397819317d86d

None in this comparison, conditional on the frozen baseline; outside its guard is unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/5/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/5/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/5/upper_envelope; canonical SHA-256: 391552c099c101b131feaf24c5795a6a15bc8ec82015424e0d2b4274a369a0bf

1

#### Native item 7

Native pointer: /joint_analysis/comparisons/6; canonical SHA-256: f9c6ca746cb8d4edaf1acf3dc44ab7ab12c3f0c59a590e4b11fb3981a12e76aa

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/6/bound_uses; canonical SHA-256: c286d53a2cc52e41a89ad72ccc65edc5db22f65d85d26360ffe9961530e238ad

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0; canonical SHA-256: 7faadf8cd438d639593bda94f69c5ce7e9edd115be62d6efb141105ed167c2d2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/adopted_region; canonical SHA-256: cc322124fdd592e1e34325730f2b6b75b9e627303337ef71e6a0f24ea2f22708

Not selected in the exact-one comparison.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/bound_id; canonical SHA-256: 38a392dbb7d2397b1a36071dd564f84337c8ccffae62771c6dab786a9e54900e

SO_HO_HOC07_S_full__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/reason; canonical SHA-256: 6e8ed117af4e87224717e787c26deed5b572c9e74c9e99a617ae83ed481df82b

The explicit one-call witness attains the independent positive integer lower bound; the retained asymptotic upper is unnecessary here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/validity_region; canonical SHA-256: 96eb3f7f3153b2b727b623c23f2e78f2721eaeee15590af19affaac2bc908029

SO_HO_HOC07_S_full__randomized__r3

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/bound_uses/1; canonical SHA-256: 58cc5b9892e3198b4fddcc41720758a0f044baff799416044c7075ce5f82c1fa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/adopted_region; canonical SHA-256: a148726d6c1888a655e5301f834ce75e500024e57d6e9438441a705dcc569748

SO_HO_HOC07_S_full__randomized__r_one_call_20261116

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/bound_id; canonical SHA-256: 3bdd35ef64238633064d8f2cbabf8a570e4d8f825bb6cc1ea551d1ef6502b42b

SO_HO_HOC07_S_full__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs; canonical SHA-256: 42490e050279d9daa0999bdc9534a290621f9b77f8b2835259d3bc7a74e01af5

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 271da148b6b5c2a2c5eb00e4aac5b37cef587289dba548ffba093165dc02ebb9

HO_FULL_TAYLOR_BISECTION_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/reason; canonical SHA-256: 57309ebbba24e2573b3be9064eced35ee1509b3e67a8643fe02d674868bdf48a

A new direct quadratic-subclass argument preserves the full-space model, output, per-instance 2/3 guarantee and integer fixed-path query count.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/validity_region; canonical SHA-256: 96eb3f7f3153b2b727b623c23f2e78f2721eaeee15590af19affaac2bc908029

SO_HO_HOC07_S_full__randomized__r3

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/bound_uses/2; canonical SHA-256: a58343ed0366aa56fb2909eac407af2d85d04603230edb7304fd7774fe07b11d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/adopted_region; canonical SHA-256: a148726d6c1888a655e5301f834ce75e500024e57d6e9438441a705dcc569748

SO_HO_HOC07_S_full__randomized__r_one_call_20261116

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/bound_id; canonical SHA-256: b472c8df2d4011b84b6db9e404b56da843dd4dcaa3b80a2001009d37cb6c0107

SO_HO_HOC07_S_full__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs; canonical SHA-256: 42490e050279d9daa0999bdc9534a290621f9b77f8b2835259d3bc7a74e01af5

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 271da148b6b5c2a2c5eb00e4aac5b37cef587289dba548ffba093165dc02ebb9

HO_FULL_TAYLOR_BISECTION_20261115

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/reason; canonical SHA-256: e57bc9d8104d0b782e30bbc1131166cd8280deec9d0e1dcd13f4aa90652f1247

Deterministic Taylor witness, admitted to the randomized view with probability one. Keep its guard inside the minimum; on d=1 compare both upper witnesses.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/validity_region; canonical SHA-256: 92b5021f9fdbaeb0c9f87d2b30070730ee0f8237cdb692796d3660364a1f2a21

SO_HO_HOC07_S_full__randomized__r8

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/bound_uses/3; canonical SHA-256: 08e61c76813454c61d6efaa82c842414c862b76343c03fbaf734aff0b8e4f7d0

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/bound_id; canonical SHA-256: 308f3613ad2a3ecf57ca46b14d3c5fb444515f3f1bf17a2d83573fc09c3b038e

SO_HO_HOC07_S_full__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/reason; canonical SHA-256: ee7f407b4de059c949ecd79972124957656694252e4e8ad4896e3dd9e5252b30

The deterministic resisting chain is not a lower bound for arbitrary private-randomness algorithms; no distributional transfer is supplied.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/validity_region; canonical SHA-256: 3c3c9b834357f77e2cdb89e0221cfd7d27232622d3e10fc7681143928ded53b9

SO_HO_HOC07_S_full__deterministic__r4

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/6/boundary_checks; canonical SHA-256: b93b61946076ba72a68db482c765097bc021b335c84407ab27a02025f0a828b4

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/boundary_checks/0; canonical SHA-256: cbce03c9e94f83e14b8fb4ba53b6b7b68589ed5ab0a8c040dd1c4dabeb77e758

Q=1 is included in the proved one-query region because f(y)-f*<=M R^s<=epsilon_f. The sufficient threshold is not asserted to be sharp.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/boundary_checks/1; canonical SHA-256: bcbc37cd38cb03d944a69cc111948dcd984daf794440a1a579d1e4a45c05fc4f

For d=1 choose n=1+ceil(log2(max{1,Q})/s); at Q=2^(s m), m integer>=0, n=m+1 suffices, including equality.

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/boundary_checks/2; canonical SHA-256: 9111b3cbcd3057263bb8349eb39fc4356db58d6aae57d1a03bfb324c5a0a996c

The final Taylor model and its output use no further unknown-function response; a derivative zero permits earlier termination.

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/boundary_checks/3; canonical SHA-256: 6cd63967d3f172cf7301aa70e3d1f4abdc0790de186a1607684cf518d2add1ae

Large lower derivatives are queried exactly, not hidden in constants; the Holder remainder is the only approximation error.

#### Native item 5

Native pointer: /joint_analysis/comparisons/6/boundary_checks/4; canonical SHA-256: d135d223b5dca72ac40488e8d0677bb0ee7af91fe124b1866543e215889cdd1f

R=0 and M=0 remain separate q2 endpoints; neither q2 nor q3 is merged into q1.

#### Native item 6

Native pointer: /joint_analysis/comparisons/6/boundary_checks/5; canonical SHA-256: d27d832a33dbb10b19d250a34467e734cf5d0a1410bea8bda9b9e4947962db71

The d=1 logarithmic branch improves the old polynomial rate as Q tends to infinity at fixed k,nu,p. No exact finite crossover with an O-constant is claimed.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/6/comparison_id; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/6/constant_dependencies; canonical SHA-256: 3d90c82354370fd2c3d6eddea92616d228bc6965cd23589f0f0095167d0859e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/constant_dependencies/0; canonical SHA-256: 71ef2135560b4492a70fc1492c2fa2ee883f07c90849ee5398cf6cc815ac3ca1

SO_HO_HOC07_S_full_p_5ca4632155

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/constant_dependencies/1; canonical SHA-256: a63eb8589904175a9afbd68d8954c257780392fb9bc988236c076bc9829cdf65

SO_HO_HOC07_S_full_p_573ff14ac8

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/constant_dependencies/2; canonical SHA-256: d3cbe48ec13be2b9294ee718ca8f1707da2f655e1ac7817b88fa717dbe790473

SO_HO_HOC07_S_full_p_07b6ef0c28

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/6/fixed_parameters; canonical SHA-256: 3d90c82354370fd2c3d6eddea92616d228bc6965cd23589f0f0095167d0859e3

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/fixed_parameters/0; canonical SHA-256: 71ef2135560b4492a70fc1492c2fa2ee883f07c90849ee5398cf6cc815ac3ca1

SO_HO_HOC07_S_full_p_5ca4632155

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/fixed_parameters/1; canonical SHA-256: a63eb8589904175a9afbd68d8954c257780392fb9bc988236c076bc9829cdf65

SO_HO_HOC07_S_full_p_573ff14ac8

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/fixed_parameters/2; canonical SHA-256: d3cbe48ec13be2b9294ee718ca8f1707da2f655e1ac7817b88fa717dbe790473

SO_HO_HOC07_S_full_p_07b6ef0c28

#### Native field: gap

Native pointer: /joint_analysis/comparisons/6/gap; canonical SHA-256: ad94b30d01e095f626d08d40ad741dc1522f5091d85e4f286933777573c705c9

1; exact minimax jet cost one.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/6/lower_envelope; canonical SHA-256: 9e7d183991c48b8aaed0a35c440a0843fa59b3aa5aebf5aa521933d832bb6c61

1 on SO_HO_HOC07_S_full__randomized__r_one_call_20261116

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/6/remaining_gap; canonical SHA-256: d6fcd1556767e6b206a9eabcde8d674b7d86fc85a79579158e9d2fe65d22fc7c

No registered gap on this sufficient one-call region. No maximal threshold or new source theorem is asserted.

#### Native field: role

Native pointer: /joint_analysis/comparisons/6/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/6/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/6/upper_envelope; canonical SHA-256: 9e7d183991c48b8aaed0a35c440a0843fa59b3aa5aebf5aa521933d832bb6c61

1 on SO_HO_HOC07_S_full__randomized__r_one_call_20261116

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 8b7253919689be46e504991d6d10c69f5902383d4f152b720897fff9166c61c0

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 4cff65ad0b7b3a5ad56d31ae7152df9c4db120a549f352275aba039c2c9e4231

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 47d447a43afa7de64260f90dce1cefff3f2994a56e7ae9a4e4064e597140482c

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 19e1851e6e2852abf38b77b707e8ed4885187d70e9652cd45e08df131ff40017

zero_radius

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: e2d17951e5a5dd8a6b2bfb6328ecd9b8f7bac23ed00d5b1cdee9e0d595528cbb

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/1; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: b5badeacd7ac67aee519f072a61ef6d8f006963c41dbc70c085c08a5fcc2d0e6

Conditional frozen exact cost zero; a ratio of two zero costs is inapplicable.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: cff93ff388b9b0a224e4ecea8380125690c8c5e3dd25d2725195c7a11c7d0a7b

Both views: R=0, all other admissible parameters.

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: ca7b9c202cb402a42802e25c05e6c2b793b04030276c869538e217aff81c0874

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: aac31b84b10b445dda9c696227665c28d216968f4f5d0b106bf9a1d10ca54c71

zero_modulus

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 2655ee7ad9d1ed66c38c448605a84ce3adc816bfec0d06bcb5601be781975603

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 3ef05c1b7b2fa081c5add0ccea4b316b828faef5b46249762dbbc8364ae9780a

Conditional frozen exact cost one; this shares Q=0 with zero_radius but has a different cost.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 3924f3cbc01ff90457fb5dbc7dcc98f1156ec394a9873fccdc2dfe09feb75e1a

Both views: R>0,M=0, all other admissible parameters.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 2cd1d2440fe50861bb672de43830b1eb2cf3996cb6cb4d00c20bcc094f04406d

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 481e44011ce6cf3e0f6cda7e63fe8abf3fcdc9f60acde46eb1a40b1efec1df0c

randomized_saturation

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 42490e050279d9daa0999bdc9534a290621f9b77f8b2835259d3bc7a74e01af5

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs/0; canonical SHA-256: 271da148b6b5c2a2c5eb00e4aac5b37cef587289dba548ffba093165dc02ebb9

HO_FULL_TAYLOR_BISECTION_20261115

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 72a966443254de468f713d8571d2ae34880b4985b24f1471c610ce5dc99673c5

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 0f823840b42739fd837226ca4e42c4e068ab8d5cd8149440047908f771619aee

New exact cost one. This is a proved sufficient saturation region, not a maximal activation domain. The previously proved closure now has its own native optimal randomized-q1 comparison; broad c1 retains its distinct joint polynomial-gap record.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 0e7b89e4d79b36f7409820e638b325d4847ce075ebb24e716f8199498a43bee6

Randomized view: M,R>0,p>1,0<Q<=1, any d>=1.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: 67f823c58b16399fb9450ecf356cf6884067ec408da31d805d26b684d481083e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: ce58db861ab34478f83108a64668d860efaad6464a16e98065f2ffa81bb80533

randomized_line

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 2c3d8bd9c0ddaebc8f3a2f2a7487a1fa2c558cc00f9a36f6c5e6656f52c4fc29

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: 9db88fcf3c69941419a3bff815621cc644e4f2cb542fc5f178cd774bf840a0b2

New logarithmic upper; lower one. No logarithmic optimality claim.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: dcd758c8d125c7c5078060da677d264a861338244cf840d60d804f5735989307

Randomized view: M,R>0,p>1,Q>1,d=1.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 5

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: 82019e15cb8b0d0c58e796f7603a96ab9b6d2292a7fe9859665742a3ccc6bb50

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: 0bdeeb03c0da33bf7f7cda48d16773e11dbac3e5121aae8e1b2cb54541c1e8fd

randomized_remaining

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: 2c3d8bd9c0ddaebc8f3a2f2a7487a1fa2c558cc00f9a36f6c5e6656f52c4fc29

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/0; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: 1301bb5f52f387dd391ab1b8f282a819bce2a9c863b8f6cf245995ee1e11f562

Retained polynomial upper and new constant lower. The main-rate lower gap remains.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: 4b66ba2072c8d8a8d11848710169abdc86411866cf23782b85ae33b0ce141c5d

Randomized view: M,R>0,p>1,Q>1,d>=2.

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

Native pointer: /joint_analysis/domain_map/cells/5; canonical SHA-256: 02f8b77eb1fd449d65f90782d00f4ac75d7b3c892f253b6dde5258db59e2c12d

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/5/cell_id; canonical SHA-256: 3b50aad1fd6b61ae0044744fa7f02c51bb5e3dd6f4eb540d80c75d06033fb2fc

deterministic_high_dimension

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/5/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs; canonical SHA-256: bd7914634dd18e5dcbe1fe1c2d55031e67e2450758b989e880cbc4cda8f57ba6

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs/0; canonical SHA-256: 92b1a6147b4e3c4f1a5e9e1c539f5f042480db00db87fbd4358a20c2b533549c

HO_CONVEX_CHAIN

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids; canonical SHA-256: 7b53375b84db926d9e3d5b1a08ee32361b50b0239d11e6617b2ed38dd851db5e

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/5/note; canonical SHA-256: ebf23063d1901d656715c808772d688d03c158849a30bcbe019bf66807d56008

Conditionally retained matching Euclidean rates. The dimension guard is only sufficient applicability.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/5/predicate; canonical SHA-256: 47a6c7e1166b83a3f4926483964bd497e0f1cd7f852049da8fc5af7bbc8862bc

Deterministic view: M,R>0,p=2,d>=C_{k,nu}(1+Q^(2/(3s-2))).

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/5/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/5/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/5/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 7

Native pointer: /joint_analysis/domain_map/cells/6; canonical SHA-256: 79faf814d0dce43cba3728f1c997f9e5caca6280b1a626b835f2e4890c843911

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/6/cell_id; canonical SHA-256: 9be04d36df4b8fe0998013cd260f86f8022dea059a548e3ba5413840783c9b54

deterministic_other_positive

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/6/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/6/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/6/note; canonical SHA-256: f055afc33c4c114b559589bd984cd8819ea8b8f6eb4d09262aa93cac82c13d20

No registered comparison assembles this complement. A stored upper exists; no fresh envelope or deterministic adoption of the new local witness is proposed here.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/6/predicate; canonical SHA-256: 09b0b49c69068c08ef21f55b97b3ae304376caf1d31a3705a92be991bacc4b6f

Deterministic view: M,R>0,p>1 and NOT[p=2 and d>=C_{k,nu}(1+Q^(2/(3s-2)))].

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/6/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/6/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/6/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native item 8

Native pointer: /joint_analysis/domain_map/cells/7; canonical SHA-256: fe13cf4f4dae00758724d6d9c8000bdc4d6ea2a5486065b11af73536508dfbc8

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/7/cell_id; canonical SHA-256: d0317333ff99be2656c35f3b5e9231690bb3c49163704bfccbef327d26338850

p_one

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/7/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/7/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/7/note; canonical SHA-256: a2d408e046a27147e508fbf00c50162a87fe0113de26e1d3c74161c030d8fc1d

Unused b2 bounds refer to separate q3 quantities, whose tracked/fixed arrays are empty and analysis_scope is absent. These records are not merged or adopted; a future role audit and explicit comparison/transfer are needed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/7/predicate; canonical SHA-256: cdadc273fedbc1c05c6c1d2d7f74328cbf1f8241d18bdf5872058d64f69a267e

Both views: M,R>0,p=1.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/7/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/7/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/7/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: f1a854d53c07913b1fbcb29aa24922b47903266668f72a20bca46a2abe397245

Split first by R=0 versus R>0; then M=0 versus M>0. On the positive branch split p=1 versus p>1 and the two algorithm views. Randomized p>1 splits by Q<=1 versus Q>1, then d=1 versus d>=2. Deterministic p>1 splits by the exact retained high-dimensional Euclidean predicate and its negation. These cases are disjoint and exhaust the fixed admissible domain.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 0d1e2f1530e35d82c164588e3bd9fc9b07e75cf983b5681662ee7a5b982f4512

No unallocated target parameters. Scientifically unassessed cells are deterministic_other_positive and p_one; bounds_recorded does not certify globally strongest rates in the other cells.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 968ae20af4d79d7d0238043bb4fc3e32cdfac16654284a070c4d35b3385ab236

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 1840e9e25b9300e95426d22f55279fe4dbdcdea59f24edd2cb245e151f76b9ba

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 6ed8ef145affa6bbb684893b63ec80c5fbc2ebedc257a89f2d3b87576fc3fe2d

The quadratic subclass is admissible at every public M>=0. This is a nontriviality bound, not a diverging main-rate lower theorem.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 2c3d8bd9c0ddaebc8f3a2f2a7487a1fa2c558cc00f9a36f6c5e6656f52c4fc29

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 2a6577ee53c0458acb81c28cdd9d1dba9a3c5e7c7c623a33b294edd0602c25dd

quadratic-nontriviality-20261115

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: f7ae6168991f4c3b5391afe0c066b0bc08a8b36056c7d9309de02915fe9f0cca

Entire registered positive-parameter p>1 comparison, as a missing-side fill.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: db3e3a5f5e632773be25071832b4ead55ce7887470644e9a9e8167fdf1e0bcd3

nontriviality_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: b048edfa75f9d0dab30215818944860cf6d8999ca1570353c86b7bad3bab465e

Lower side 1.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: b8a21069ea3ed2ecee43630ae4229964a8ff4bed8e714e32cb7caf797bc4cd70

Lower side absent.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 665dd2bced4c6f26a034f6e31ca92b6812d9a5b783c66dd77fdbabc753ece516

Existing upper witnesses and all other native comparisons are unchanged by this lower finding.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 96eb3f7f3153b2b727b623c23f2e78f2721eaeee15590af19affaac2bc908029

SO_HO_HOC07_S_full__randomized__r3

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: e1b84d399aaf47e32e027be411de6a513f4740422bc3d9774e5f1d92fb36d923

f_plus/minus=A||x-(x0 plus/minus R e1)||_2^2 with A>epsilon_f/R^2.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 4175650b488ac8c16fda98c8f8e20c51d913193ae9c69276e0ea717eb52f7bd0

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: e1faf34680139df636676659c57c27a03fe1c53e9ee09f6ec1a83f4b7aa6cd40

The integral remainder bound and free compact known-model minimization use exactly one complete jet. The boundary Q=1 is proved sufficient and is not claimed sharp.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 86fd2b48e62dc77d0b98ee32890f9fb5c453e2a1a1b00fe420c08ff8edc4d86b

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 4d8f4a76e42a552ad58c4f0b538f90137ce697524a54fee61cea69d01ac9835c

taylor-saturation-20261115

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 98711988648c5d67d770f270bd040c5066c1085663b6b91d66bb9aaff47c1f17

Exact finite-count closure throughout this sufficient saturation region; no asymptotic order improvement over the previous O(1).

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 7c5a91d3e0e35b1d11a1891b9a37077123dd3c6612c5a3df5c4579a1b3c375e4

Upper 1 and, using the separate lower finding, exact minimax cost 1.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 3b3232ad81a8f333a379dce13c8c38f6b6b2bf7a1dbc329e7cf132e683eb5bf2

O_{k,nu,p}(1+Q^a_p), with no exact finite call count.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 82d29f72e469b9ea33db84f20da56337c7862695a890c8abd5b362f506356122

Q>1 is not improved by this saturation argument; other comparisons retain their native rows.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 426adc02d300d7d8ecec8a56ec9a958dbbfcabf5e1567ca2424a51de7cd7b340

M,R>0,p>1,0<Q<=1, any d>=1.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: db355c7e3e1967acd4b6435faf095feca0bc2c1d64b0ece1667d7d0d2f7cb6b9

At Q=1, two Taylor remainders sum to at most M R^s=epsilon_f.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 6ddcb2bdfa96bf188eab4f5c058b76d0b8ee0e94ca9d944b1e1a2fa4f6c563ff

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 6d2e89b04e73e3c800bce4cdfeb1f3e3d96fed727d1e2a2881f3a81592d2a7d1

The exact n-query witness is valid for every Q>0 in d=1. The rate crossover against an O-constant is asymptotic; the guarded minimum retains both witnesses.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 2c3d8bd9c0ddaebc8f3a2f2a7487a1fa2c558cc00f9a36f6c5e6656f52c4fc29

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 5d6917bfe98ac1fe4b02af4787c7bd75b636d3ba53779c975c2e95e31e9ad036

one-dimensional-upper-20261115

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 940fb28452f51cf2b473752bb166822109c6b91efb589d8166215b0c79d0fd9b

For each fixed k,nu,p, d=1 and Q tending to infinity: O(1+log Q) improves the recorded polynomial upper rate.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: e46dc08d9339f20cb15eb1b467050fab606d83b910547fd1264d98c41bae6a3b

\min\!\left\{O_{k,\nu,p}(1+\mathcal{Q}^{a_p}),\ \left[1+\left\lceil\frac{\log_2(\max\{1,\mathcal{Q}\})}{s}\right\rceil\right]_{\mathcal{Q}\le1\ \mathrm{or}\ d=1}\right\}

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 3c8ddc09d66a4ba7e67570ba623770dc0fea8ee637463a8dd91af108f33ee455

O_{k,nu,p}(1+Q^a_p).

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 41e4d605b95abe1612548a6c41641090659ec0af0ee8eaa10048a24395989fed

For d>=2,Q>1 the original upper remains; for bounded Q both statements are O(1), with exact saturation handled separately.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: c377ff37a73041633a5a171a3db2e10fe39896f24ebb16306e69b5d506624214

M,R>0,p>1,d=1; the new witness is also valid on the saturation region.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 8596985720b9056c6bcdad9f33a376b626b55d5a2f3df5c886fdf48566a4dfd1

d=1,Q=2^(s m), m->infinity: new count m+1 versus old rate 1+2^(s a_p m).

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: b2ce8464b43379f0749e889ce3adfe6b752bb8028e99cff7e801665afad73e44

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 6bc1c7b8b856e1efea0a108dde26ab2d1d26e9442e9d612b5048df5bf8a4e14c

First annotation records parameter roles, conditional provenance, candidate dispositions and the residual domain. It does not independently certify old theorems.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 87a35e09c7f085dc424f1a4528556e38fbc7d0647f4d59e7d6fb881defcb7a5f

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/impact/3/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/impact/3/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/impact/3/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 5f4197239c7422ff2429bd020d845c23cc3967eda324228f5f585010ea807c47

initial-joint-synthesis-20261115

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 84df6bc1fee6fab24ccf521fd5a77223e53784251eb3cfb3de1284a58ca73cba

No scientific improvement is attributed to presentation.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 1b9f1a7daad76f77242917f9ebb228b3d8e1521842ac69ade8f7acec470d7ac4

The five unchanged comparison envelopes are preserved; c1 randomized scientific changes are justified only by the three separate derivation findings.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: fd879311f3bec5ea8558c5183dc6f764005f4a5b57b9d4aa8644feb976cd34a0

Six frozen comparison envelopes and no joint analysis.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: a33020761aad420260ef8381cdb63784bdf6aed9707523639c2442a639f532fe

All unaffected scientific rows, endpoints, guards and status labels.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: c7f100629f42d3c024268737f307aad57fb07f3e72a49304238079fbdb130049

Full fixed target domain.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 277ed9883df8ff98adc05b6d59b7edaedeee23899f8183e6563d4a5b8e515e82

Disjoint domain partition separates Q=0 endpoints and explicit unassessed complements.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: 5630fb2eae5a72943f0144b63eb643bd1672bf9d171d6b9908bcab58ffd6ce2a

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 1d3f148e58727a5c6e1e6aa7f67e40ba3da531a11bf0a5c755a8b641dd9fc9d0

The bounded-ball specialization does not establish the required full-space concentration or an attained global minimizer within R. No source-to-target transfer is asserted.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 2c3d8bd9c0ddaebc8f3a2f2a7487a1fa2c558cc00f9a36f6c5e6656f52c4fc29

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: 25cfe61f59db087d421c4add5f36bac7e258185eceae5997665a3495b238ce88

cgm-theorem26-fullspace-screen

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 65fccc62082037c59840e2998863f9f68d9cea33897b675f5ef57f0568684fd7

No lower theorem from Theorem 26 is adopted.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: 65fccc62082037c59840e2998863f9f68d9cea33897b675f5ef57f0568684fd7

No lower theorem from Theorem 26 is adopted.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 6781cdb345743d11ed9b6b187b625b0384aae646ca30c7b7ad39a877ad845e15

Entire target domain.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: 577443933b83d0250cc5f092230cf56f1a57b0220655bd883831e6d48ac0a8c6

Source Theorem 26, arXiv:2411.08987v2, pp.42-45, chars 98829-105001.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: e5a9a5ffd90ee9a2695893c9f54ba207b0a4ea3975181bbb98bf05646b486f0f

Condition (iii) requires concentration for every x in X. For X=R^d scaling x contradicts that bound for any nonzero random vector.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: 6c56d78e147faf48051a02a46ccb078cb826fef42944debb041321b6fd952fc8

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: 36eab91212175d66eb99b6364c656c95744048cbf0a7eaba26db197eb4875d9e

Curated continuation of the original held research, not fresh blind recall. Scientific formulas, guards and native proofs are preserved. The v2 ledger explicitly retains pending synthesis/projection work. Register the already-proved randomized-q1 exact-one saturation cell in a native comparison and explicitly classify the broad joint registered gap as polynomial; no claim of literature completeness.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/5/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/5/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/impact/5/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/impact/5/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/impact/5/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/impact/5/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: c5abf2a07f881a337c679a1e518b210e960742fe3fa86639145c2f586e1a957c

curated_feedback_SO_HO_HOC07_S_full_20261116

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

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: a8b2116d8f43cd09d072eb84519e2bf00263fd3ee34b3ad754e3f9ec30a03f2b

For each fixed k>=2, 0<nu<=1 and finite 1<=p<infinity: d in positive integers, M>=0, R>=0, epsilon_f>0; convex C^k objectives on R^d with the stated global Holder bound and a minimizer within lp-distance R of x0. Separate deterministic error and randomized per-instance probability>=2/3 views; fixed worst-path complete-jet count. The six existing comparisons use distinct q1/q2 identities; q3 is not transferred.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 7

Native pointer: /joint_analysis/impact/6; canonical SHA-256: 8e5672f4fb2806b9ca7f63035255c61b3d980c9d7428b888456d64b9711eb53a

#### Native field: argument

Native pointer: /joint_analysis/impact/6/argument; canonical SHA-256: 27f13269515265b1342c5f746170f0138e34ac988e3697d1c69e363782cc4706

The exact previously adopted science is conditionally retained. Correct only open-cell closure-publication metadata to the current explicit unassessed convention; no bound, guard, comparison, scientific contract or summary changes. Grouped cross-ID opportunities remain unassessed pending work, without any adopted reduction. This is presentation restructuring, not a new theorem or blind research.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/6/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/6/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/impact/6/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/6/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/6/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/impact/6/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/impact/6/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/impact/6/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/impact/6/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/6/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/6/finding_id; canonical SHA-256: a0d61353775a6451d19668f927dbcb71ef8694846bd8521a9f1674be83855965

curated_feedback_SO_HO_HOC07_S_full_20261116_42b1a1bbfb

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/6/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/6/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/6/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/6/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/6/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/6/validity_region; canonical SHA-256: a8b2116d8f43cd09d072eb84519e2bf00263fd3ee34b3ad754e3f9ec30a03f2b

For each fixed k>=2, 0<nu<=1 and finite 1<=p<infinity: d in positive integers, M>=0, R>=0, epsilon_f>0; convex C^k objectives on R^d with the stated global Holder bound and a minimizer within lp-distance R of x0. Separate deterministic error and randomized per-instance probability>=2/3 views; fixed worst-path complete-jet count. The six existing comparisons use distinct q1/q2 identities; q3 is not transferred.

#### Native field: witness

Native pointer: /joint_analysis/impact/6/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 4236fff6c8bb78361d5db51ca9f0ea1142db94c2654c0feec44a17dfa40e4af7

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 889d319695513c370490f90465f5d1a19e2dca2f6ebdc254ee5a9b65d2aa114f

Obtain and independently verify a randomized full-space hard distribution with the optimizer-localization promise before claiming any main-rate lower bound. The cited Theorem 26 does not satisfy its own concentration premise on unrestricted R^d.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 20c79c8092eb398b3b6614af8a243779d2d3c299acdf335b2344c313a2eda631

Assess deterministic positive-parameter regions outside c1 and the separate p=1/q3 quantities before a broader joint envelope. Empty q3 role metadata must be audited before adoption.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 1dc417c812f0e9d3b613f33a5999e966aa74bba82c78ef6018dd0ce9c80afedd

No exhaustive literature search, sharp one-query threshold, logarithmic lower bound, or d>=2 finite-dimensional saturation theorem has been established. These broader questions do not support or obstruct the present local derivation.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 8bedc1894445b2f4a1e9e190dc8b794505627b2cae32e42759a556db48d61080

Assess a separately proved deterministic-q1 adoption of the local Taylor/two-point witness, without merging the randomized quantity/resource IDs; this candidate registers only the originally proved randomized-q1 target.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: b43ca9a66d7d4bc7605218821bca65cda5d008ccf401b161edbd56d26739f392

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c2 and SO_HO_HOC07_S_full__randomized__b7

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: f6f350b5e5c81ad2ced73d8ab870ee45578300637075043c942992dcab3aa9ca

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c3 and SO_HO_HOC07_S_full__randomized__b7

#### Native item 7

Native pointer: /joint_analysis/pending_obligations/6; canonical SHA-256: f6c504f296693e0be0925f1b94a6567f6db204fdd2b0a817cdf845255387fb2f

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c2 and SO_HO_HOC07_S_full__randomized__b8

#### Native item 8

Native pointer: /joint_analysis/pending_obligations/7; canonical SHA-256: 61b5a3f3e3c50d60defec919909bc62941fa896c2a61a341cea695f8742969b8

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c3 and SO_HO_HOC07_S_full__randomized__b8

#### Native item 9

Native pointer: /joint_analysis/pending_obligations/8; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native item 10

Native pointer: /joint_analysis/pending_obligations/9; canonical SHA-256: d98988f1825c51146e242a9547595513fe08ba9532e68391654e2edaee4596a0

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b1, SO_HO_HOC07_S_full__deterministic__b3 to SO_HO_HOC07_S_full__deterministic__c2, SO_HO_HOC07_S_full__deterministic__c3; no transfer is adopted by this metadata inventory.

#### Native item 11

Native pointer: /joint_analysis/pending_obligations/10; canonical SHA-256: dd60242ef2211d49db3c0ffd6850aa46b962a48864e6941052437a72f30c68cd

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b2 to SO_HO_HOC07_S_full__deterministic__c1; no transfer is adopted by this metadata inventory.

#### Native item 12

Native pointer: /joint_analysis/pending_obligations/11; canonical SHA-256: 892a3a4ad482a70c5fc668020e49204a3f7fca117e740d316794561b7f90b7f1

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b2 to SO_HO_HOC07_S_full__deterministic__c2, SO_HO_HOC07_S_full__deterministic__c3; no transfer is adopted by this metadata inventory.

#### Native item 13

Native pointer: /joint_analysis/pending_obligations/12; canonical SHA-256: d2e3167926005e3bb8cec229eec29568dca824d2e8d3fd9868bb705b7d96021a

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b4, SO_HO_HOC07_S_full__deterministic__b5, SO_HO_HOC07_S_full__deterministic__b6, SO_HO_HOC07_S_full__deterministic__b7 to SO_HO_HOC07_S_full__deterministic__c1; no transfer is adopted by this metadata inventory.

#### Native item 14

Native pointer: /joint_analysis/pending_obligations/13; canonical SHA-256: 6733f875bfab938b49ccceb0426684b43157b4804cca4b71ef8be813b9aa4cf8

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b1 to SO_HO_HOC07_S_full__randomized__c2, SO_HO_HOC07_S_full__randomized__c3; no transfer is adopted by this metadata inventory.

#### Native item 15

Native pointer: /joint_analysis/pending_obligations/14; canonical SHA-256: befa36f08164b5ee892f2dbfdefc103b29151354db6b69c5652f612361358dce

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b2 to SO_HO_HOC07_S_full__randomized__c1, SO_HO_HOC07_S_full__randomized__c_one_call; no transfer is adopted by this metadata inventory.

#### Native item 16

Native pointer: /joint_analysis/pending_obligations/15; canonical SHA-256: 12c70b5f9aef614b54e04a7c6bf3ac107ed4a735cdb5d2e8c83d4db9028bfc56

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b2 to SO_HO_HOC07_S_full__randomized__c2, SO_HO_HOC07_S_full__randomized__c3; no transfer is adopted by this metadata inventory.

#### Native item 17

Native pointer: /joint_analysis/pending_obligations/16; canonical SHA-256: 6fa367dd7976c990c318d9263529d236364821ea8064019697bdebcd544f859d

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b3, SO_HO_HOC07_S_full__randomized__b4, SO_HO_HOC07_S_full__randomized__b5, SO_HO_HOC07_S_full__randomized__b6 to SO_HO_HOC07_S_full__randomized__c1, SO_HO_HOC07_S_full__randomized__c_one_call; no transfer is adopted by this metadata inventory.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 7116a3a3026c0a5c13369444d9443200da78bec6ca446fcf0f295263959c5fee

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: a3a339ca686dfd7a7828f13836e10dbabd4045c7507cec9004310df4e4ad5fb5

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 3bdd35ef64238633064d8f2cbabf8a570e4d8f825bb6cc1ea551d1ef6502b42b

SO_HO_HOC07_S_full__randomized__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: db535cb5987ca1c994ce89b8d91ca15632e7327d3b129a8998e3be2a20f4402d

Two fixed admissible quadratics with disjoint acceptable outputs exclude zero queries under the native per-instance randomized guarantee.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 42490e050279d9daa0999bdc9534a290621f9b77f8b2835259d3bc7a74e01af5

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: 271da148b6b5c2a2c5eb00e4aac5b37cef587289dba548ffba093165dc02ebb9

HO_FULL_TAYLOR_BISECTION_20261115

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 96eb3f7f3153b2b727b623c23f2e78f2721eaeee15590af19affaac2bc908029

SO_HO_HOC07_S_full__randomized__r3

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 7211923cc4096d4ed9cb606b42589d2c3e43bf14f42da5272d96611802634d35

HO_FULL_TAYLOR_BISECTION_20261115; complete LOWER, TAYLOR, SATURATION and ONE DIMENSION steps.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 96eb3f7f3153b2b727b623c23f2e78f2721eaeee15590af19affaac2bc908029

SO_HO_HOC07_S_full__randomized__r3

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 40c9ac87321ba5ae689759a80e9da9ad8bfd13135ad1764a877b32c3aa8ad912

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: b472c8df2d4011b84b6db9e404b56da843dd4dcaa3b80a2001009d37cb6c0107

SO_HO_HOC07_S_full__randomized__b8

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: ee020795006eccf2644ce1a79f53189b34b26b9e28bd8f1818cf7e4884e61b7c

One exact jet per queried point; polynomial-model optimization and the unqueried output are free. The deterministic witness meets randomized g1 with probability one. No native quantity or resource identity is changed.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 42490e050279d9daa0999bdc9534a290621f9b77f8b2835259d3bc7a74e01af5

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 271da148b6b5c2a2c5eb00e4aac5b37cef587289dba548ffba093165dc02ebb9

HO_FULL_TAYLOR_BISECTION_20261115

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 92b5021f9fdbaeb0c9f87d2b30070730ee0f8237cdb692796d3660364a1f2a21

SO_HO_HOC07_S_full__randomized__r8

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 7211923cc4096d4ed9cb606b42589d2c3e43bf14f42da5272d96611802634d35

HO_FULL_TAYLOR_BISECTION_20261115; complete LOWER, TAYLOR, SATURATION and ONE DIMENSION steps.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 92b5021f9fdbaeb0c9f87d2b30070730ee0f8237cdb692796d3660364a1f2a21

SO_HO_HOC07_S_full__randomized__r8

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: e0f2442c56203ad699cdc96f2780637dc48ceb42a95b28eb4bc9f1bd64ef5004

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: bf855a2053d460a825b181298451642412142c4cdc63816e225b3b930c9975d3

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: 5329623590805a744dd40547f43c85fcb2906a25f05369682e7db3a5e466d1e9

No new literature search. This is a curated continuation of the original held, unadopted proposal and its historical finite screens; no prior source-reading credit or approval is inherited. Fresh independent review must verify all changed science and the proposed ledger.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: a656dfe42458d290d6210797fbe6f99b7275aaa480e7aee3cbe5773b3e2c3e7a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: d200cd6e47f4b9edf1a5d60aac4dba456770b21723b625fe6dcf35bca8f3afdc

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 8d55dc738ea9eb38b8c1fa04f16bf252c6bec9b09770b08e24789563dc498061

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 205d8d1c2f10c9c5187e2076b6fc93dc02270a6285523e8988f3ffe7ef169eff

SO_HO_HOC07_S_full__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 308f3613ad2a3ecf57ca46b14d3c5fb444515f3f1bf17a2d83573fc09c3b038e

SO_HO_HOC07_S_full__deterministic__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 7b53375b84db926d9e3d5b1a08ee32361b50b0239d11e6617b2ed38dd851db5e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 7475f5c28d6e11aed1e0488576316565370bec26989c73e41336d34999b4a066

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 29ec46dbdee6ade598da2a7b863907306b4533ec1cd9bc92506548db76ed70ec

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 83f0ac1f500c7fe9c385b748c18bd4e867f70d4bc3c9086dca567625ab1df4d5

SO_HO_HOC07_S_full__deterministic__b4

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 8702620a814f0ed501c17dc0d415138a972ab99a2b96c9b4198f06e4c1d47167

SO_HO_HOC07_S_full__deterministic__b5

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: f67057f2bb9b9bced72783cfb69752670d10f042b6deb3ba05b661e7a5d92cc4

SO_HO_HOC07_S_full__deterministic__b6

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: fb327adae86fbfbf634e6bed1126e770466fc5deaa9ca0e5c236a9b50e9fdb1e

SO_HO_HOC07_S_full__deterministic__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: f732add385947966be16f263422d0849ce5916d2d6ac95baa960438353a08a12

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 0d163c37ff0d6e8ba57a619761b977731cd0123e168b93d6595d1f7c390611dd

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 29ec46dbdee6ade598da2a7b863907306b4533ec1cd9bc92506548db76ed70ec

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: 83f0ac1f500c7fe9c385b748c18bd4e867f70d4bc3c9086dca567625ab1df4d5

SO_HO_HOC07_S_full__deterministic__b4

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 8702620a814f0ed501c17dc0d415138a972ab99a2b96c9b4198f06e4c1d47167

SO_HO_HOC07_S_full__deterministic__b5

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: f67057f2bb9b9bced72783cfb69752670d10f042b6deb3ba05b661e7a5d92cc4

SO_HO_HOC07_S_full__deterministic__b6

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: fb327adae86fbfbf634e6bed1126e770466fc5deaa9ca0e5c236a9b50e9fdb1e

SO_HO_HOC07_S_full__deterministic__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: af29487142059fb54c8030c2980849930d78402f2af4c1ef4df30b4e9aa2a94e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 0dbba30c6187f135314b526fba00b5ac985f99c1deca631d451ca1696b065099

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: fb22af52dbc46639b76c9fb5ecc5ff9bbf4a6bf32376ce461bf792d3d3cf8a55

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: 38a392dbb7d2397b1a36071dd564f84337c8ccffae62771c6dab786a9e54900e

SO_HO_HOC07_S_full__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: 3bdd35ef64238633064d8f2cbabf8a570e4d8f825bb6cc1ea551d1ef6502b42b

SO_HO_HOC07_S_full__randomized__b7

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: b472c8df2d4011b84b6db9e404b56da843dd4dcaa3b80a2001009d37cb6c0107

SO_HO_HOC07_S_full__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 2c3d8bd9c0ddaebc8f3a2f2a7487a1fa2c558cc00f9a36f6c5e6656f52c4fc29

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: f664c42239cd85c0e474d249a8ac9809e2957b305119c8c0d86d4f0112ae7c5c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 037fa7a1efe2d0918a573af62bf0a07481c0afbae37dfa524cd7411fe0bcf318

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/0; canonical SHA-256: 95140400d37033b7b0f792030b856b83fcb8b01f9afac2dfc3cb2d732ce83b71

SO_HO_HOC07_S_full__randomized__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/1; canonical SHA-256: f4c639bcf2b99f164924f9ea9f8d3840800311987a57d4c8644082324b442861

SO_HO_HOC07_S_full__randomized__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/2; canonical SHA-256: af3bcc03396457984950437ba8194b3bb5aa39d311fc302b9df8f8f6d263ad42

SO_HO_HOC07_S_full__randomized__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/3; canonical SHA-256: 193f99499a7b6cbdd91c2524e116c017eaf87924ecde93693184a4dcb474124f

SO_HO_HOC07_S_full__randomized__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 8f4bbd6b5a79b5c7ecd67057cf734277208879c6dbe294fcc22f1d958eef157f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 911831b4a1de84e739d6adee4c9c63c3cbab4207a19aa20ce616f1ece72cb93e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 037fa7a1efe2d0918a573af62bf0a07481c0afbae37dfa524cd7411fe0bcf318

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/0; canonical SHA-256: 95140400d37033b7b0f792030b856b83fcb8b01f9afac2dfc3cb2d732ce83b71

SO_HO_HOC07_S_full__randomized__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/1; canonical SHA-256: f4c639bcf2b99f164924f9ea9f8d3840800311987a57d4c8644082324b442861

SO_HO_HOC07_S_full__randomized__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/2; canonical SHA-256: af3bcc03396457984950437ba8194b3bb5aa39d311fc302b9df8f8f6d263ad42

SO_HO_HOC07_S_full__randomized__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/3; canonical SHA-256: 193f99499a7b6cbdd91c2524e116c017eaf87924ecde93693184a4dcb474124f

SO_HO_HOC07_S_full__randomized__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 591026b80e22ce49e8d316b91d5a0aaac6c1d87fb0cdff76b979a18b18f13fd4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 36dbcb9de69a967c80f978a060522264a0c29aaaa17dc37d79fb5a48201e39e9

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: fb22af52dbc46639b76c9fb5ecc5ff9bbf4a6bf32376ce461bf792d3d3cf8a55

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/0; canonical SHA-256: 38a392dbb7d2397b1a36071dd564f84337c8ccffae62771c6dab786a9e54900e

SO_HO_HOC07_S_full__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/1; canonical SHA-256: 3bdd35ef64238633064d8f2cbabf8a570e4d8f825bb6cc1ea551d1ef6502b42b

SO_HO_HOC07_S_full__randomized__b7

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/2; canonical SHA-256: b472c8df2d4011b84b6db9e404b56da843dd4dcaa3b80a2001009d37cb6c0107

SO_HO_HOC07_S_full__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 72a966443254de468f713d8571d2ae34880b4985b24f1471c610ce5dc99673c5

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 5fa33983f32a4c1027a92106c478a51fb23e76f63df8884a2a111e3319f68669

synthesis-6

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: af354acec1b0870e001d65c4377ed643debd5d261cdd6ccfe89162d5d34f058c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: 54a66eab467db3d40ca6c45ae750e0e0576d631e4d5d8010be0ccc1904086c2b

This directed projection/replacement opportunity needs a separate applicability/cost judgment. Distinct IDs are not merged, and no opposite-direction inference is made.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 6e66527efe840c8421133cf11eb30d60251dc5c4770152093de123b511391640

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/0; canonical SHA-256: 3bdd35ef64238633064d8f2cbabf8a570e4d8f825bb6cc1ea551d1ef6502b42b

SO_HO_HOC07_S_full__randomized__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 8f4bbd6b5a79b5c7ecd67057cf734277208879c6dbe294fcc22f1d958eef157f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: f1d7c1b829959acf5fd8b22ab6c75fdbf1b3810e2c3ef78a394693a9a0260546

synthesis-7

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: b43ca9a66d7d4bc7605218821bca65cda5d008ccf401b161edbd56d26739f392

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c2 and SO_HO_HOC07_S_full__randomized__b7

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: a1ea53449f01ab3e74ae66c370b97b7fdfb4fa0af8227e8d532edb75a014745c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: 54a66eab467db3d40ca6c45ae750e0e0576d631e4d5d8010be0ccc1904086c2b

This directed projection/replacement opportunity needs a separate applicability/cost judgment. Distinct IDs are not merged, and no opposite-direction inference is made.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 6e66527efe840c8421133cf11eb30d60251dc5c4770152093de123b511391640

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/0; canonical SHA-256: 3bdd35ef64238633064d8f2cbabf8a570e4d8f825bb6cc1ea551d1ef6502b42b

SO_HO_HOC07_S_full__randomized__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 591026b80e22ce49e8d316b91d5a0aaac6c1d87fb0cdff76b979a18b18f13fd4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 705e1af290021b0ee8b6cac71ead9597d036f83961af1c252c90f4ed8047130f

synthesis-8

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: f6f350b5e5c81ad2ced73d8ab870ee45578300637075043c942992dcab3aa9ca

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c3 and SO_HO_HOC07_S_full__randomized__b7

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: c7d1fc7878e875f8eeef6b311249c03bc33dfad5f6b628495253138d26af3815

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: 54a66eab467db3d40ca6c45ae750e0e0576d631e4d5d8010be0ccc1904086c2b

This directed projection/replacement opportunity needs a separate applicability/cost judgment. Distinct IDs are not merged, and no opposite-direction inference is made.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 79a88979d1d914179dde1264ef8a13ed871cd17d51aa71f3fc40f71d0dd9896f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/0; canonical SHA-256: b472c8df2d4011b84b6db9e404b56da843dd4dcaa3b80a2001009d37cb6c0107

SO_HO_HOC07_S_full__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 8f4bbd6b5a79b5c7ecd67057cf734277208879c6dbe294fcc22f1d958eef157f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: cefa876d80b27bbc26ecd952c430927d231047df60d2c399f9959d4307ecfd70

synthesis-9

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: f6c504f296693e0be0925f1b94a6567f6db204fdd2b0a817cdf845255387fb2f

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c2 and SO_HO_HOC07_S_full__randomized__b8

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: 0d77535f174a76679c09783ae1bd9013c18a9d3d0dfafaae8299585237e4e815

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/argument; canonical SHA-256: 54a66eab467db3d40ca6c45ae750e0e0576d631e4d5d8010be0ccc1904086c2b

This directed projection/replacement opportunity needs a separate applicability/cost judgment. Distinct IDs are not merged, and no opposite-direction inference is made.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs; canonical SHA-256: 79a88979d1d914179dde1264ef8a13ed871cd17d51aa71f3fc40f71d0dd9896f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/0; canonical SHA-256: b472c8df2d4011b84b6db9e404b56da843dd4dcaa3b80a2001009d37cb6c0107

SO_HO_HOC07_S_full__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: 591026b80e22ce49e8d316b91d5a0aaac6c1d87fb0cdff76b979a18b18f13fd4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 9cab9589f3334662db7e0a597e42e682e82fc47dc9b49b5f48ad62e4069ce795

synthesis-10

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 61b5a3f3e3c50d60defec919909bc62941fa896c2a61a341cea695f8742969b8

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c3 and SO_HO_HOC07_S_full__randomized__b8

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: b367fc141b0a96bc30602d9689d2d18eaa48be01a0ed7650a65bfa2e1db14cb7

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/argument; canonical SHA-256: 15bb622aa888859bd83552fa3033677233d47f11da4e5b25275518c041f30870

Unapproved working memory is preserved as explicitly pending. This curation neither resolves the lead nor claims a proved literature-open problem or previous scientific approval.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: 889d319695513c370490f90465f5d1a19e2dca2f6ebdc254ee5a9b65d2aa114f

Obtain and independently verify a randomized full-space hard distribution with the optimizer-localization promise before claiming any main-rate lower bound. The cited Theorem 26 does not satisfy its own concentration premise on unrestricted R^d.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/obligations/12; canonical SHA-256: e2c74b584dc5e85e175c19cbed0c20770b008a495fca4c74b32c8412727de6fc

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/argument; canonical SHA-256: 15bb622aa888859bd83552fa3033677233d47f11da4e5b25275518c041f30870

Unapproved working memory is preserved as explicitly pending. This curation neither resolves the lead nor claims a proved literature-open problem or previous scientific approval.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/lead; canonical SHA-256: 20c79c8092eb398b3b6614af8a243779d2d3c299acdf335b2344c313a2eda631

Assess deterministic positive-parameter regions outside c1 and the separate p=1/q3 quantities before a broader joint envelope. Empty q3 role metadata must be audited before adoption.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 14

Native pointer: /joint_analysis/synthesis_coverage/obligations/13; canonical SHA-256: 9b0ae8ed91f66862bc466104a94fbcb6df0cb55454de1aeb35d04069a632650b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/argument; canonical SHA-256: 15bb622aa888859bd83552fa3033677233d47f11da4e5b25275518c041f30870

Unapproved working memory is preserved as explicitly pending. This curation neither resolves the lead nor claims a proved literature-open problem or previous scientific approval.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/lead; canonical SHA-256: 1dc417c812f0e9d3b613f33a5999e966aa74bba82c78ef6018dd0ce9c80afedd

No exhaustive literature search, sharp one-query threshold, logarithmic lower bound, or d>=2 finite-dimensional saturation theorem has been established. These broader questions do not support or obstruct the present local derivation.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 15

Native pointer: /joint_analysis/synthesis_coverage/obligations/14; canonical SHA-256: 7508d21fc12d3c1d0f9baa66966005d7c67e4d134b7639e57cc42648d1e04396

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/argument; canonical SHA-256: 15bb622aa888859bd83552fa3033677233d47f11da4e5b25275518c041f30870

Unapproved working memory is preserved as explicitly pending. This curation neither resolves the lead nor claims a proved literature-open problem or previous scientific approval.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/lead; canonical SHA-256: 8bedc1894445b2f4a1e9e190dc8b794505627b2cae32e42759a556db48d61080

Assess a separately proved deterministic-q1 adoption of the local Taylor/two-point witness, without merging the randomized quantity/resource IDs; this candidate registers only the originally proved randomized-q1 target.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 16

Native pointer: /joint_analysis/synthesis_coverage/obligations/15; canonical SHA-256: 04030e4bd3181afe1e90ea7ea5202715f4ba1c3f6aed01d2a83273a26ee84659

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/argument; canonical SHA-256: 15bb622aa888859bd83552fa3033677233d47f11da4e5b25275518c041f30870

Unapproved working memory is preserved as explicitly pending. This curation neither resolves the lead nor claims a proved literature-open problem or previous scientific approval.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/id; canonical SHA-256: a0050dd45f09b8c1454f66ddc34c7e3533ab3f980a23fb9c8576d4ecdca8fe45

retained-material-lead-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/lead; canonical SHA-256: b43ca9a66d7d4bc7605218821bca65cda5d008ccf401b161edbd56d26739f392

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c2 and SO_HO_HOC07_S_full__randomized__b7

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 17

Native pointer: /joint_analysis/synthesis_coverage/obligations/16; canonical SHA-256: 73d1237d21b02b1c81ee7a2e8389d238890ff69e362e766996b03ad5346d3672

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/argument; canonical SHA-256: 15bb622aa888859bd83552fa3033677233d47f11da4e5b25275518c041f30870

Unapproved working memory is preserved as explicitly pending. This curation neither resolves the lead nor claims a proved literature-open problem or previous scientific approval.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/id; canonical SHA-256: 816e64d45ab01655b0cdb3174cc88338b9552319d4504b2ed46ed2504883fbc8

retained-material-lead-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/lead; canonical SHA-256: f6f350b5e5c81ad2ced73d8ab870ee45578300637075043c942992dcab3aa9ca

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c3 and SO_HO_HOC07_S_full__randomized__b7

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 18

Native pointer: /joint_analysis/synthesis_coverage/obligations/17; canonical SHA-256: 690cf9bb2ab18052ca4320a8aed3848772c299bfafa7477762efe23a127df459

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/argument; canonical SHA-256: 15bb622aa888859bd83552fa3033677233d47f11da4e5b25275518c041f30870

Unapproved working memory is preserved as explicitly pending. This curation neither resolves the lead nor claims a proved literature-open problem or previous scientific approval.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/id; canonical SHA-256: 5f5ef600bbb2ac5a387c0c18974eca304cd2a13b61d69abb61fe40a3138ea1c9

retained-material-lead-6

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/lead; canonical SHA-256: f6c504f296693e0be0925f1b94a6567f6db204fdd2b0a817cdf845255387fb2f

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c2 and SO_HO_HOC07_S_full__randomized__b8

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 19

Native pointer: /joint_analysis/synthesis_coverage/obligations/18; canonical SHA-256: 0d01b6b5b6d6c33bd056ca4641fc449bbbc07eb1e29b0c279e03d16e9d072f25

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/argument; canonical SHA-256: 15bb622aa888859bd83552fa3033677233d47f11da4e5b25275518c041f30870

Unapproved working memory is preserved as explicitly pending. This curation neither resolves the lead nor claims a proved literature-open problem or previous scientific approval.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/id; canonical SHA-256: 20ad6c87c364725f99c5c808f9434c0ceddcc5b3563d71c5f7a0ff6148b9be6d

retained-material-lead-7

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/lead; canonical SHA-256: 61b5a3f3e3c50d60defec919909bc62941fa896c2a61a341cea695f8742969b8

Assess resource_projection for SO_HO_HOC07_S_full__randomized__c3 and SO_HO_HOC07_S_full__randomized__b8

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 20

Native pointer: /joint_analysis/synthesis_coverage/obligations/19; canonical SHA-256: 5151feb87e1626a02c11ea1ffe195c71f7dd999d0d066cb18b825aa998e7f142

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids; canonical SHA-256: 8d50958568c0f223902c32342f32e837e6e9add00c29547e8106363bfe3d95f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/1; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/2; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/3; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/4; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/5; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/6; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/id; canonical SHA-256: 8f3893b390dbf1c98368d6b451c613dd05f798a42d5bd62383775de81d03258c

curated-scope-limit

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 21

Native pointer: /joint_analysis/synthesis_coverage/obligations/20; canonical SHA-256: 3b464baa2ced8e244a97936440d09038bc845ef35e16d258395796b3cf0e6f19

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/bound_refs; canonical SHA-256: 8d55dc738ea9eb38b8c1fa04f16bf252c6bec9b09770b08e24789563dc498061

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/bound_refs/0; canonical SHA-256: 205d8d1c2f10c9c5187e2076b6fc93dc02270a6285523e8988f3ffe7ef169eff

SO_HO_HOC07_S_full__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/bound_refs/1; canonical SHA-256: 308f3613ad2a3ecf57ca46b14d3c5fb444515f3f1bf17a2d83573fc09c3b038e

SO_HO_HOC07_S_full__deterministic__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids; canonical SHA-256: 43dcf397d5f39f06f288690dfd2ca09beb9a5c7a4621b371eb7c7e4351b157d8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/0; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/1; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/id; canonical SHA-256: 63757bbeb852486506119309822316f014d83ae0b2e1e99ea16080aa227f7d81

possible-projection-37669a81858c

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/lead; canonical SHA-256: d98988f1825c51146e242a9547595513fe08ba9532e68391654e2edaee4596a0

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b1, SO_HO_HOC07_S_full__deterministic__b3 to SO_HO_HOC07_S_full__deterministic__c2, SO_HO_HOC07_S_full__deterministic__c3; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 22

Native pointer: /joint_analysis/synthesis_coverage/obligations/21; canonical SHA-256: fefe3afa703e04264b737033d74b6d7769394d30569631462f88977713a2b666

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/bound_refs; canonical SHA-256: 8d55dc738ea9eb38b8c1fa04f16bf252c6bec9b09770b08e24789563dc498061

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/bound_refs/0; canonical SHA-256: 205d8d1c2f10c9c5187e2076b6fc93dc02270a6285523e8988f3ffe7ef169eff

SO_HO_HOC07_S_full__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/bound_refs/1; canonical SHA-256: 308f3613ad2a3ecf57ca46b14d3c5fb444515f3f1bf17a2d83573fc09c3b038e

SO_HO_HOC07_S_full__deterministic__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids; canonical SHA-256: 43dcf397d5f39f06f288690dfd2ca09beb9a5c7a4621b371eb7c7e4351b157d8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/0; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/1; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/id; canonical SHA-256: 760dabf99864d761a967181aa9ce9f422bcceca2697b61bd07c4a11372c17185

possible-projection-37669a81858c-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/lead; canonical SHA-256: d98988f1825c51146e242a9547595513fe08ba9532e68391654e2edaee4596a0

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b1, SO_HO_HOC07_S_full__deterministic__b3 to SO_HO_HOC07_S_full__deterministic__c2, SO_HO_HOC07_S_full__deterministic__c3; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 23

Native pointer: /joint_analysis/synthesis_coverage/obligations/22; canonical SHA-256: b7021e4a2c009ce463317a327873d88ca8ce32865bf84dee498c1d790200e9dc

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/bound_refs; canonical SHA-256: ef00caca5b1c4671e51be35af5c13965d31a73351e5623a0e03be762decc63f0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/bound_refs/0; canonical SHA-256: dc7c4614f598df7e3b081c1e7c5ebbe390ce232a4e647baf2799a261e32001bc

SO_HO_HOC07_S_full__deterministic__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids; canonical SHA-256: 7b53375b84db926d9e3d5b1a08ee32361b50b0239d11e6617b2ed38dd851db5e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/id; canonical SHA-256: 08291d2c9ce1a5f358d02509dfd021849d0d84f45eafae23aef4d50f44d94ebd

possible-projection-72b90daf8054

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/lead; canonical SHA-256: dd60242ef2211d49db3c0ffd6850aa46b962a48864e6941052437a72f30c68cd

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b2 to SO_HO_HOC07_S_full__deterministic__c1; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 24

Native pointer: /joint_analysis/synthesis_coverage/obligations/23; canonical SHA-256: 3bbef20f7d1234c7ea47c27a13b0809aa443e79704d802bf799257f74ddd6813

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/bound_refs; canonical SHA-256: ef00caca5b1c4671e51be35af5c13965d31a73351e5623a0e03be762decc63f0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/bound_refs/0; canonical SHA-256: dc7c4614f598df7e3b081c1e7c5ebbe390ce232a4e647baf2799a261e32001bc

SO_HO_HOC07_S_full__deterministic__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/comparison_ids; canonical SHA-256: 7b53375b84db926d9e3d5b1a08ee32361b50b0239d11e6617b2ed38dd851db5e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/id; canonical SHA-256: c994f8332d6fd7283f76affa99236a36218b53559e85bad1005534c791a5c796

possible-projection-72b90daf8054-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/lead; canonical SHA-256: dd60242ef2211d49db3c0ffd6850aa46b962a48864e6941052437a72f30c68cd

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b2 to SO_HO_HOC07_S_full__deterministic__c1; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/23/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 25

Native pointer: /joint_analysis/synthesis_coverage/obligations/24; canonical SHA-256: fe8f31e149245b5847d9f02b64068c81c23292e9b5663667c95ab02a6202a21e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/bound_refs; canonical SHA-256: ef00caca5b1c4671e51be35af5c13965d31a73351e5623a0e03be762decc63f0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/bound_refs/0; canonical SHA-256: dc7c4614f598df7e3b081c1e7c5ebbe390ce232a4e647baf2799a261e32001bc

SO_HO_HOC07_S_full__deterministic__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/comparison_ids; canonical SHA-256: 43dcf397d5f39f06f288690dfd2ca09beb9a5c7a4621b371eb7c7e4351b157d8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/comparison_ids/0; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/comparison_ids/1; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/id; canonical SHA-256: 19986dde69921bf1c33d4289292a9ac002aa914b78ac9db606bee328f7abff38

possible-projection-a7df2cee0a29

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/lead; canonical SHA-256: 892a3a4ad482a70c5fc668020e49204a3f7fca117e740d316794561b7f90b7f1

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b2 to SO_HO_HOC07_S_full__deterministic__c2, SO_HO_HOC07_S_full__deterministic__c3; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/24/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 26

Native pointer: /joint_analysis/synthesis_coverage/obligations/25; canonical SHA-256: de5c444521101404b621b77b250065f45d3e20b65050895718b8694ffa4071ce

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/bound_refs; canonical SHA-256: ef00caca5b1c4671e51be35af5c13965d31a73351e5623a0e03be762decc63f0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/bound_refs/0; canonical SHA-256: dc7c4614f598df7e3b081c1e7c5ebbe390ce232a4e647baf2799a261e32001bc

SO_HO_HOC07_S_full__deterministic__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/comparison_ids; canonical SHA-256: 43dcf397d5f39f06f288690dfd2ca09beb9a5c7a4621b371eb7c7e4351b157d8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/comparison_ids/0; canonical SHA-256: 6cb93489b2d692aba795976a02c2d41fbe37901f56c7114bc458e93df066bc26

SO_HO_HOC07_S_full__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/comparison_ids/1; canonical SHA-256: e91b4638d1277aab9ea395d1030edd9e3a552e75c04c618ddc9d36dcef039fb4

SO_HO_HOC07_S_full__deterministic__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/id; canonical SHA-256: bf6805c6813c9e8a70c1cc2bbb296fd558ac7bf9c80ffe8800b6feab31331971

possible-projection-a7df2cee0a29-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/lead; canonical SHA-256: 892a3a4ad482a70c5fc668020e49204a3f7fca117e740d316794561b7f90b7f1

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b2 to SO_HO_HOC07_S_full__deterministic__c2, SO_HO_HOC07_S_full__deterministic__c3; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/25/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 27

Native pointer: /joint_analysis/synthesis_coverage/obligations/26; canonical SHA-256: 3264181c38ad6ca9400d8d597e26c3c16f9c5b664b0abcc1f97bf261aae1d579

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/bound_refs; canonical SHA-256: 29ec46dbdee6ade598da2a7b863907306b4533ec1cd9bc92506548db76ed70ec

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/bound_refs/0; canonical SHA-256: 83f0ac1f500c7fe9c385b748c18bd4e867f70d4bc3c9086dca567625ab1df4d5

SO_HO_HOC07_S_full__deterministic__b4

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/bound_refs/1; canonical SHA-256: 8702620a814f0ed501c17dc0d415138a972ab99a2b96c9b4198f06e4c1d47167

SO_HO_HOC07_S_full__deterministic__b5

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/bound_refs/2; canonical SHA-256: f67057f2bb9b9bced72783cfb69752670d10f042b6deb3ba05b661e7a5d92cc4

SO_HO_HOC07_S_full__deterministic__b6

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/bound_refs/3; canonical SHA-256: fb327adae86fbfbf634e6bed1126e770466fc5deaa9ca0e5c236a9b50e9fdb1e

SO_HO_HOC07_S_full__deterministic__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/comparison_ids; canonical SHA-256: 7b53375b84db926d9e3d5b1a08ee32361b50b0239d11e6617b2ed38dd851db5e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/id; canonical SHA-256: 39f8303473a4174cdce3809732e978dd3904540eb691b96639d489c27fbf5fdc

possible-projection-baa653c0b708

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/lead; canonical SHA-256: d2e3167926005e3bb8cec229eec29568dca824d2e8d3fd9868bb705b7d96021a

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b4, SO_HO_HOC07_S_full__deterministic__b5, SO_HO_HOC07_S_full__deterministic__b6, SO_HO_HOC07_S_full__deterministic__b7 to SO_HO_HOC07_S_full__deterministic__c1; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/26/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 28

Native pointer: /joint_analysis/synthesis_coverage/obligations/27; canonical SHA-256: d724a16a8d828ca37de86b3a3d96e065d7568b6c4cb75c1f4b1314dc4e06eac0

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/bound_refs; canonical SHA-256: 29ec46dbdee6ade598da2a7b863907306b4533ec1cd9bc92506548db76ed70ec

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/bound_refs/0; canonical SHA-256: 83f0ac1f500c7fe9c385b748c18bd4e867f70d4bc3c9086dca567625ab1df4d5

SO_HO_HOC07_S_full__deterministic__b4

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/bound_refs/1; canonical SHA-256: 8702620a814f0ed501c17dc0d415138a972ab99a2b96c9b4198f06e4c1d47167

SO_HO_HOC07_S_full__deterministic__b5

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/bound_refs/2; canonical SHA-256: f67057f2bb9b9bced72783cfb69752670d10f042b6deb3ba05b661e7a5d92cc4

SO_HO_HOC07_S_full__deterministic__b6

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/bound_refs/3; canonical SHA-256: fb327adae86fbfbf634e6bed1126e770466fc5deaa9ca0e5c236a9b50e9fdb1e

SO_HO_HOC07_S_full__deterministic__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/comparison_ids; canonical SHA-256: 7b53375b84db926d9e3d5b1a08ee32361b50b0239d11e6617b2ed38dd851db5e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/comparison_ids/0; canonical SHA-256: 7aa06662b9325e2cc382b2aec7a1865452bb550ac758258315cca90741f5cbb0

SO_HO_HOC07_S_full__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/id; canonical SHA-256: d37e513852120ac3e60c8c4b38d015d598b11d9be46c2f4dbfd76c05380bc9f3

possible-projection-baa653c0b708-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/lead; canonical SHA-256: d2e3167926005e3bb8cec229eec29568dca824d2e8d3fd9868bb705b7d96021a

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__deterministic__b4, SO_HO_HOC07_S_full__deterministic__b5, SO_HO_HOC07_S_full__deterministic__b6, SO_HO_HOC07_S_full__deterministic__b7 to SO_HO_HOC07_S_full__deterministic__c1; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/27/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 29

Native pointer: /joint_analysis/synthesis_coverage/obligations/28; canonical SHA-256: 404e5a44ab5161f175c98abf978c8cee7cfcfb5070316098a65f67e822dcbf21

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/bound_refs; canonical SHA-256: 1c6228e1728d6fc5e3ca526b85451c24b2cf6a4f916f0a348165fd7789f248ca

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/bound_refs/0; canonical SHA-256: 38a392dbb7d2397b1a36071dd564f84337c8ccffae62771c6dab786a9e54900e

SO_HO_HOC07_S_full__randomized__b1

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/comparison_ids; canonical SHA-256: 2cd8dc0d9c0579c168c659ff8a1b02f1ad4f5e4cb9257a855bb081c531f2ba8b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/comparison_ids/0; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/comparison_ids/1; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/id; canonical SHA-256: 2fa4e485e58d0cc5067fa8da1f1b8044bb5ffa0bbe4da573026e6dcd4d37187e

possible-projection-0d825a836c13

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/lead; canonical SHA-256: 6733f875bfab938b49ccceb0426684b43157b4804cca4b71ef8be813b9aa4cf8

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b1 to SO_HO_HOC07_S_full__randomized__c2, SO_HO_HOC07_S_full__randomized__c3; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/28/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 30

Native pointer: /joint_analysis/synthesis_coverage/obligations/29; canonical SHA-256: 36c020e408907a06f9f0a2ca8d239f2f5ce62614244e52b7920ce2eaf4f17d4d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/bound_refs; canonical SHA-256: 1c6228e1728d6fc5e3ca526b85451c24b2cf6a4f916f0a348165fd7789f248ca

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/bound_refs/0; canonical SHA-256: 38a392dbb7d2397b1a36071dd564f84337c8ccffae62771c6dab786a9e54900e

SO_HO_HOC07_S_full__randomized__b1

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/comparison_ids; canonical SHA-256: 2cd8dc0d9c0579c168c659ff8a1b02f1ad4f5e4cb9257a855bb081c531f2ba8b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/comparison_ids/0; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/comparison_ids/1; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/id; canonical SHA-256: df390711ae227e8f2e3a173f5b43d21de74009f3fd2ba701ede7f49333a6ab8f

possible-projection-0d825a836c13-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/lead; canonical SHA-256: 6733f875bfab938b49ccceb0426684b43157b4804cca4b71ef8be813b9aa4cf8

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b1 to SO_HO_HOC07_S_full__randomized__c2, SO_HO_HOC07_S_full__randomized__c3; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/29/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 31

Native pointer: /joint_analysis/synthesis_coverage/obligations/30; canonical SHA-256: b6808bf9b5bfba561a0b19e7ee2e294d7136d0cb1bbbfdfbd114f63ca076ae75

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/bound_refs; canonical SHA-256: b5be6e6955ff5c57ac69c3077552c44669ac63defe5bcd4e13b928acb92cc6a4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/bound_refs/0; canonical SHA-256: f595fcd9f06cc95774f1aa5df808fa469848bbfae779caf9b1deb1527842020a

SO_HO_HOC07_S_full__randomized__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/comparison_ids; canonical SHA-256: 86fd2b48e62dc77d0b98ee32890f9fb5c453e2a1a1b00fe420c08ff8edc4d86b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/comparison_ids/0; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/comparison_ids/1; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/id; canonical SHA-256: c1a7c35389ae82ab47b0a5421fe0a3fe08f73a0487f5d3c714c65846bf9f9e89

possible-projection-c2998b9a679d

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/lead; canonical SHA-256: befa36f08164b5ee892f2dbfdefc103b29151354db6b69c5652f612361358dce

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b2 to SO_HO_HOC07_S_full__randomized__c1, SO_HO_HOC07_S_full__randomized__c_one_call; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/30/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 32

Native pointer: /joint_analysis/synthesis_coverage/obligations/31; canonical SHA-256: fe89a2650546b8e6bc94b54b98fe3c9376e66bddc45715c0e5708d1ee547d78b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/bound_refs; canonical SHA-256: b5be6e6955ff5c57ac69c3077552c44669ac63defe5bcd4e13b928acb92cc6a4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/bound_refs/0; canonical SHA-256: f595fcd9f06cc95774f1aa5df808fa469848bbfae779caf9b1deb1527842020a

SO_HO_HOC07_S_full__randomized__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/comparison_ids; canonical SHA-256: 86fd2b48e62dc77d0b98ee32890f9fb5c453e2a1a1b00fe420c08ff8edc4d86b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/comparison_ids/0; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/comparison_ids/1; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/id; canonical SHA-256: b656f8a581daf0ece84392b78250c5e9e2884991aa057a8bc2557789685d868b

possible-projection-c2998b9a679d-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/lead; canonical SHA-256: befa36f08164b5ee892f2dbfdefc103b29151354db6b69c5652f612361358dce

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b2 to SO_HO_HOC07_S_full__randomized__c1, SO_HO_HOC07_S_full__randomized__c_one_call; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/31/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 33

Native pointer: /joint_analysis/synthesis_coverage/obligations/32; canonical SHA-256: 4727bdd6ba615bca09e0057ee9e81fd94c048a3292c7d700cd39d95915fef10f

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/bound_refs; canonical SHA-256: b5be6e6955ff5c57ac69c3077552c44669ac63defe5bcd4e13b928acb92cc6a4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/bound_refs/0; canonical SHA-256: f595fcd9f06cc95774f1aa5df808fa469848bbfae779caf9b1deb1527842020a

SO_HO_HOC07_S_full__randomized__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/comparison_ids; canonical SHA-256: 2cd8dc0d9c0579c168c659ff8a1b02f1ad4f5e4cb9257a855bb081c531f2ba8b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/comparison_ids/0; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/comparison_ids/1; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/id; canonical SHA-256: 1c0e860ef9e276e34ebc9d2bd6537212b8395afd94233dbf07fa7ef2e4b0af6c

possible-projection-9d8fd2fa43a5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/lead; canonical SHA-256: 12c70b5f9aef614b54e04a7c6bf3ac107ed4a735cdb5d2e8c83d4db9028bfc56

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b2 to SO_HO_HOC07_S_full__randomized__c2, SO_HO_HOC07_S_full__randomized__c3; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/32/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 34

Native pointer: /joint_analysis/synthesis_coverage/obligations/33; canonical SHA-256: 4c3ba2e4852dbdb8359aa98d98bb8632051c008aefa7211974c41f1d667a283e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/bound_refs; canonical SHA-256: b5be6e6955ff5c57ac69c3077552c44669ac63defe5bcd4e13b928acb92cc6a4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/bound_refs/0; canonical SHA-256: f595fcd9f06cc95774f1aa5df808fa469848bbfae779caf9b1deb1527842020a

SO_HO_HOC07_S_full__randomized__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/comparison_ids; canonical SHA-256: 2cd8dc0d9c0579c168c659ff8a1b02f1ad4f5e4cb9257a855bb081c531f2ba8b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/comparison_ids/0; canonical SHA-256: c519fc173d753b692736bdcb722acd8eff575f33ff12c52cc456b8104315fead

SO_HO_HOC07_S_full__randomized__c2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/comparison_ids/1; canonical SHA-256: db4b501ee3d1a9358d06b5a3b09228298629933e8bf4c18631495b8a94f81f60

SO_HO_HOC07_S_full__randomized__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/id; canonical SHA-256: 761f934bd5361bd397fb55b5a23ecf305efc7a0cba99fc1c8041c6de2706d905

possible-projection-9d8fd2fa43a5-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/lead; canonical SHA-256: 12c70b5f9aef614b54e04a7c6bf3ac107ed4a735cdb5d2e8c83d4db9028bfc56

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b2 to SO_HO_HOC07_S_full__randomized__c2, SO_HO_HOC07_S_full__randomized__c3; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/33/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 35

Native pointer: /joint_analysis/synthesis_coverage/obligations/34; canonical SHA-256: 895e0527adb7845c69f82fbf1e63f708202cde60d5111bf6af8bd8a1dce5682b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/bound_refs; canonical SHA-256: 037fa7a1efe2d0918a573af62bf0a07481c0afbae37dfa524cd7411fe0bcf318

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/bound_refs/0; canonical SHA-256: 95140400d37033b7b0f792030b856b83fcb8b01f9afac2dfc3cb2d732ce83b71

SO_HO_HOC07_S_full__randomized__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/bound_refs/1; canonical SHA-256: f4c639bcf2b99f164924f9ea9f8d3840800311987a57d4c8644082324b442861

SO_HO_HOC07_S_full__randomized__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/bound_refs/2; canonical SHA-256: af3bcc03396457984950437ba8194b3bb5aa39d311fc302b9df8f8f6d263ad42

SO_HO_HOC07_S_full__randomized__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/bound_refs/3; canonical SHA-256: 193f99499a7b6cbdd91c2524e116c017eaf87924ecde93693184a4dcb474124f

SO_HO_HOC07_S_full__randomized__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/comparison_ids; canonical SHA-256: 86fd2b48e62dc77d0b98ee32890f9fb5c453e2a1a1b00fe420c08ff8edc4d86b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/comparison_ids/0; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/comparison_ids/1; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/id; canonical SHA-256: 4e1716efb4b09320d269c469ac8650e091e7d36166d03bf5b89acd205eac5ee1

possible-projection-f31cd56dab38

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/lead; canonical SHA-256: 6fa367dd7976c990c318d9263529d236364821ea8064019697bdebcd544f859d

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b3, SO_HO_HOC07_S_full__randomized__b4, SO_HO_HOC07_S_full__randomized__b5, SO_HO_HOC07_S_full__randomized__b6 to SO_HO_HOC07_S_full__randomized__c1, SO_HO_HOC07_S_full__randomized__c_one_call; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/34/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 36

Native pointer: /joint_analysis/synthesis_coverage/obligations/35; canonical SHA-256: 168a1c50bd2e032a6c3b46c62f9ecde0bf4a7db9421eb4c9cb17707d120b9895

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/bound_refs; canonical SHA-256: 037fa7a1efe2d0918a573af62bf0a07481c0afbae37dfa524cd7411fe0bcf318

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/bound_refs/0; canonical SHA-256: 95140400d37033b7b0f792030b856b83fcb8b01f9afac2dfc3cb2d732ce83b71

SO_HO_HOC07_S_full__randomized__b3

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/bound_refs/1; canonical SHA-256: f4c639bcf2b99f164924f9ea9f8d3840800311987a57d4c8644082324b442861

SO_HO_HOC07_S_full__randomized__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/bound_refs/2; canonical SHA-256: af3bcc03396457984950437ba8194b3bb5aa39d311fc302b9df8f8f6d263ad42

SO_HO_HOC07_S_full__randomized__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/bound_refs/3; canonical SHA-256: 193f99499a7b6cbdd91c2524e116c017eaf87924ecde93693184a4dcb474124f

SO_HO_HOC07_S_full__randomized__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/comparison_ids; canonical SHA-256: 86fd2b48e62dc77d0b98ee32890f9fb5c453e2a1a1b00fe420c08ff8edc4d86b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/comparison_ids/0; canonical SHA-256: 9dc3dd2047add603820b5ab261b1915d6346545c775dcc256af809551e12c2af

SO_HO_HOC07_S_full__randomized__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/comparison_ids/1; canonical SHA-256: 22f9db69df100e9cf459e2ce12177a75bf9d88a674d5bb010a92a27b05e04439

SO_HO_HOC07_S_full__randomized__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/id; canonical SHA-256: 058d71e0a4344d280897a489d756f790d6a2af90e89a85038e6fd0e86a6b07c0

possible-projection-f31cd56dab38-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/lead; canonical SHA-256: 6fa367dd7976c990c318d9263529d236364821ea8064019697bdebcd544f859d

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_HO_HOC07_S_full__randomized__b3, SO_HO_HOC07_S_full__randomized__b4, SO_HO_HOC07_S_full__randomized__b5, SO_HO_HOC07_S_full__randomized__b6 to SO_HO_HOC07_S_full__randomized__c1, SO_HO_HOC07_S_full__randomized__c_one_call; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/35/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: a22067cc65903dde10f928ccb12e5f4f6b2c6c6ba05ac2555ee623b3e778eaaa

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 3d90c82354370fd2c3d6eddea92616d228bc6965cd23589f0f0095167d0859e3

#### Native item 1

Native pointer: /joint_analysis/target/allowed_constant_dependencies/0; canonical SHA-256: 71ef2135560b4492a70fc1492c2fa2ee883f07c90849ee5398cf6cc815ac3ca1

SO_HO_HOC07_S_full_p_5ca4632155

#### Native item 2

Native pointer: /joint_analysis/target/allowed_constant_dependencies/1; canonical SHA-256: a63eb8589904175a9afbd68d8954c257780392fb9bc988236c076bc9829cdf65

SO_HO_HOC07_S_full_p_573ff14ac8

#### Native item 3

Native pointer: /joint_analysis/target/allowed_constant_dependencies/2; canonical SHA-256: d3cbe48ec13be2b9294ee718ca8f1707da2f655e1ac7817b88fa717dbe790473

SO_HO_HOC07_S_full_p_07b6ef0c28

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: fe48ac04e0258375bf6f87aaadd7df1d23ed3ed2cc9d6f690ab606673e32b94c

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

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

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 2a20eb96e92a2d5b8fc4e065625df2e88412b97edc6ba37072bbd49a51019e3e

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 712574624fd0f588ab5194fb3166fec56f2510371014bfe78a5890bb2ae3cebe

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: 23a9ca027a9a55fba891321150ef8c75648c4e6e69a0ab8d8bcecd65dc7d3a38

integer k>=2

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: 71ef2135560b4492a70fc1492c2fa2ee883f07c90849ee5398cf6cc815ac3ca1

SO_HO_HOC07_S_full_p_5ca4632155

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 71ef2135560b4492a70fc1492c2fa2ee883f07c90849ee5398cf6cc815ac3ca1

SO_HO_HOC07_S_full_p_5ca4632155

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: f7fa965b80d5a2e4de0db00814ec83661801c0834268259fa7b28129da9e057b

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: 5a21dc4cace1bab3d9a4e6f7021f6c1890e5d602e16187f29c4e2266c12d441c

0<nu<=1

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: a63eb8589904175a9afbd68d8954c257780392fb9bc988236c076bc9829cdf65

SO_HO_HOC07_S_full_p_573ff14ac8

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: a63eb8589904175a9afbd68d8954c257780392fb9bc988236c076bc9829cdf65

SO_HO_HOC07_S_full_p_573ff14ac8

#### Native item 3

Native pointer: /joint_analysis/target/fixed_parameters/2; canonical SHA-256: d9c819c088518ae722c2623a203c416e4ffbbf6316f0e06e4c61941d369abfab

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/2/domain; canonical SHA-256: 8ba62d9744a872bd88fd68c730030f76d87b814f5128e2473f9f5525d0d9fd3d

1<=p<infinity; rate comparison q1 uses fixed p>1, and deterministic c1 has p=2

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/2/parameter_ref; canonical SHA-256: d3cbe48ec13be2b9294ee718ca8f1707da2f655e1ac7817b88fa717dbe790473

SO_HO_HOC07_S_full_p_07b6ef0c28

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/2/symbol; canonical SHA-256: d3cbe48ec13be2b9294ee718ca8f1707da2f655e1ac7817b88fa717dbe790473

SO_HO_HOC07_S_full_p_07b6ef0c28

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: a8b2116d8f43cd09d072eb84519e2bf00263fd3ee34b3ad754e3f9ec30a03f2b

For each fixed k>=2, 0<nu<=1 and finite 1<=p<infinity: d in positive integers, M>=0, R>=0, epsilon_f>0; convex C^k objectives on R^d with the stated global Holder bound and a minimizer within lp-distance R of x0. Separate deterministic error and randomized per-instance probability>=2/3 views; fixed worst-path complete-jet count. The six existing comparisons use distinct q1/q2 identities; q3 is not transferred.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 22619ef082abb04b662dbf665b8b44fe632b4dd7d327f2aaead864ad7ee28cde

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: c8635dcca240c3523f84e388e45dc849452453b79a115ebd4b23a8ad34e7b3e8

SO_HO_HOC07_S_full_p_08ec3403a6

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: b028de3040ab997152532a0eb475037c9d424a1a41ac5a1d5997429645f9616f

SO_HO_HOC07_S_full_p_9c38bb74d9

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: da774ae242a77bed2e90c3ed4b283dcb2e5fdd409ee260aa1f333fea54ca4d8c

SO_HO_HOC07_S_full_p_225446ffa5

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: fe5132617e26f922bc543e7131b5e3595afe54ee09500f09528c35a0edc08205

SO_HO_HOC07_S_full_p_e11cc1020a

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 0386c36c59f8ff9fe4fd6c5e8e20779ed39e38c95de0bd61aed50b54f1424754

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: c94d1f26dc2e9f5ae74a11b0e5ec19a2f9e44958c178eaf22db1889ad55fd878

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: e0ecfaa0434407a049241d704e0733fbc949d5286940e8167b657122832c6fbc

Q=M_{k,nu} R^(k+nu)/epsilon_f, the existing native dimensionless parameter. For M,R>0, x=x0+R y and g(y)=f(x0+R y)/(M R^(k+nu)) make the kth-derivative Holder bound at most one and the target error 1/Q, preserving one complete jet per point. The zero-scale endpoints are kept separate.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: 8692520d5d411ea9c5fbea98da128245bed27c69e17a42380528351bbcd2e96e

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: b028de3040ab997152532a0eb475037c9d424a1a41ac5a1d5997429645f9616f

SO_HO_HOC07_S_full_p_9c38bb74d9

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: da774ae242a77bed2e90c3ed4b283dcb2e5fdd409ee260aa1f333fea54ca4d8c

SO_HO_HOC07_S_full_p_225446ffa5

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/2; canonical SHA-256: 71ef2135560b4492a70fc1492c2fa2ee883f07c90849ee5398cf6cc815ac3ca1

SO_HO_HOC07_S_full_p_5ca4632155

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/3; canonical SHA-256: a63eb8589904175a9afbd68d8954c257780392fb9bc988236c076bc9829cdf65

SO_HO_HOC07_S_full_p_573ff14ac8

#### Native item 5

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/4; canonical SHA-256: fe5132617e26f922bc543e7131b5e3595afe54ee09500f09528c35a0edc08205

SO_HO_HOC07_S_full_p_e11cc1020a

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: 0f771f5a6850d5abf42bfa8f4622f09da84f72eba826c870eb9349bb47e406c2

SO_HO_HOC07_S_full_p_ed70f4e4e5

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: a8e33c82820699fbfac12467e959658d826a5f280c2c28274b8dfa2a0c1fbee8

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: c8635dcca240c3523f84e388e45dc849452453b79a115ebd4b23a8ad34e7b3e8

SO_HO_HOC07_S_full_p_08ec3403a6

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: b028de3040ab997152532a0eb475037c9d424a1a41ac5a1d5997429645f9616f

SO_HO_HOC07_S_full_p_9c38bb74d9

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: da774ae242a77bed2e90c3ed4b283dcb2e5fdd409ee260aa1f333fea54ca4d8c

SO_HO_HOC07_S_full_p_225446ffa5

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: fe5132617e26f922bc543e7131b5e3595afe54ee09500f09528c35a0edc08205

SO_HO_HOC07_S_full_p_e11cc1020a

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 0f771f5a6850d5abf42bfa8f4622f09da84f72eba826c870eb9349bb47e406c2

SO_HO_HOC07_S_full_p_ed70f4e4e5

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Juan Pablo Contreras; Cristóbal Guzmán; David Martínez-Rubio. Non-Euclidean High-Order Smooth Convex Optimization. arXiv:2411.08987v2 (2025-02-06); COLT 2025 extended abstract.

https://arxiv.org/pdf/2411.08987v2
