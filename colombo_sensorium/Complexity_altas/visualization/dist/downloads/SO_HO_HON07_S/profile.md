# Weak high-order Taylor stationarity with a positive output radius

**Setting ID.** `SO_HO_HON07_S`

Single-objective optimization

Find a weak Taylor stationary point of order $m$ in the prescribed domain: output a feasible point and positive radius such that the normalized Taylor decrease in the metric definition is at most $\varepsilon$.

**Status.** Bounds missing

**TASK tags.** task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Holder smooth; smoothness: Kth derivative holder; structure: Inexpensive known constraints

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Exact jet k; operation: Exact jet k; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point with positive radius; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a weak Taylor stationary point of order $m$ in the prescribed domain: output a feasible point and positive radius such that the normalized Taylor decrease in the metric definition is at most $\varepsilon$.

### Admissible model

The feasible set $Q\subset\mathbb{R}^d$ is nonempty and closed, with $x_0\in Q$. The function $f$ is $C^k$ on an open convex neighborhood of $Q$.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in Q}f(x)\le\Delta$.

$$\|D^{k}f(x)-D^{k}f(y)\|_{\mathrm{op},2}\le M_{k,\nu}\|x-y\|_{2}^{\nu}.$$

Admissible parameter domain:

$$d\ge1,\quad k\ge2;\quad\text{all other parameters satisfy their tabulated ranges}.$$

### Oracle interface

Each query selects $x$ in $Q$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

A description of the feasible set, feasibility tests and global minimization of known models formed from existing replies are supplied as public auxiliary operations.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $m$, $\Delta$, $M_{k,\nu}$, $\nu$, $\varepsilon$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $(\widehat{x},\rho)$ with $\widehat{x}\in Q$ and $0<\rho\le1$; the radius is part of the output.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\frac{\phi_{f,m}^{\rho}(\widehat{x})}{\chi_m(\rho)}.$$

$$T_{f,m}(x,u)=\sum_{j=0}^m\frac1{j!}D^jf(x)[u^j],\quad\chi_m(\rho)=\sum_{j=1}^m\frac{\rho^j}{j!},$$

$$\phi_{f,m}^{\rho}(x)=f(x)-\min_{x+u\in Q,\ \|u\|_2\le\rho}T_{f,m}(x,u).$$

Here $1\le m\le k$. The radius must be strictly positive, so the denominator is positive. The local constraint set is nonempty and compact, and the Taylor minimum is finite and attained.

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

$$\frac{\phi_{f,m}^{\rho}(\widehat{x})}{\chi_m(\rho)}\le \varepsilon.$$

The running-cost guarantee is specified separately under RESOURCE.

#### Randomized

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[\frac{\phi_{f,m}^{\rho}(\widehat{x})}{\chi_m(\rho)}\le \varepsilon\right]\ge\frac23.$$

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

$$f^*=\inf_{x\in Q}f(x).$$

$Q$: The feasible set specified by the model, also used as the query and output domain. Convexity or ball geometry is assumed only when stated in the model.

$T_{f,j}(x,u)$: The Taylor polynomial of order $j$ centered at $x$ with step $u$; the exact expression is given in the metric definition.

$D^jf(x)[u^j]$: The order-$j$ derivative applied to $j$ copies of the same step direction.

$$D^jf(x)[u^j]=D^jf(x)[u,\ldots,u].$$

$\phi_{f,j}^{\rho}(x)$: Maximum feasible Taylor-model decrease within radius $\rho$, defined by the minimization formula in the metric specification.

$\rho,\rho_j$: Positive radius returned by the algorithm. **Domain:** $0<\rho,\rho_j\le1$.

$\chi_m(\rho)$: Normalization for weak Taylor stationarity.

$$\chi_m(\rho)=\sum_{j=1}^m\rho^j/j!.$$

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}_{\ge2}$.

$m$: Order of Taylor stationarity **Domain:** $m\in\{1,\ldots,k\}$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta\ge0$.

$M_{k,\nu}$: Global $\nu$-Hölder upper bound for the order-$k$ derivative in the specified tensor norm. **Domain:** $M_{k,\nu}\ge0$.

$\nu$: Hölder exponent of the highest derivative **Domain:** $0<\nu\le1$.

$\varepsilon$: Weak Taylor-stationarity tolerance **Domain:** $0<\varepsilon\le1$.

$\theta$: Model parameters held fixed in the corresponding accuracy bound.

$$\theta=(k,m,\Delta,M_{k,\nu},\nu).$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter window 1

**Region.** $1\le m\le k,0<\nu\le 1,0<\varepsilon\le 1;\theta=(k,m,\nu,M_{k,\nu},\Delta) fixed$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O_\theta(1+\varepsilon^{-(k+\nu)/(k-m+\nu)})
$$

### R2 - Parameter window 1

**Region.** $1\le m\le k,0<\nu\le 1,0<\varepsilon\le 1;\theta=(k,m,\nu,M_{k,\nu},\Delta) fixed$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B2

$$
O_\theta(1+\varepsilon^{-(k+\nu)/(k-m+\nu)})
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $1\le m\le k,0<\nu\le 1,0<\varepsilon\le 1;\theta=(k,m,\nu,M_{k,\nu},\Delta) fixed$

**Dimension conditions.** $1\le m\le k,0<\nu\le 1,0<\varepsilon\le 1;\theta=(k,m,\nu,M_{k,\nu},\Delta) fixed$

**Oracle mapping.** Each query selects $x$ in $Q$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Output mapping.** Return $(\widehat{x},\rho)$ with $\widehat{x}\in Q$ and $0<\rho\le1$; the radius is part of the output.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Adaptive high-order regularization and selection of the output radius

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C_\theta[1+\varepsilon^{-(k+\nu)/(k-m+\nu)}]
$$

**Sources.** [1](https://arxiv.org/abs/1811.01220)

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [1](https://arxiv.org/abs/1811.01220) theorem: Theorem3.4; pdf pages: 14

### B2 - Adaptive high-order regularization and selection of the output radius

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C_\theta[1+\varepsilon^{-(k+\nu)/(k-m+\nu)}]
$$

**Sources.** [1](https://arxiv.org/abs/1811.01220)

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [1](https://arxiv.org/abs/1811.01220) theorem: Theorem3.4; pdf pages: 14

## References

[1] Coralia Cartis; Nicholas I. M. Gould; Philippe L. Toint. Sharp worst-case evaluation complexity bounds for arbitrary-order nonconvex optimization with inexpensive constraints. arXiv:1811.01220v1, 2018-11-03; SIAM Journal on Optimization 30(1) (2020), 513–541.

https://arxiv.org/abs/1811.01220
