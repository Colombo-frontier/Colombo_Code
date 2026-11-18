# Nonconvex first-order stationarity under highest-order Lipschitz regularity

**Setting ID.** `SO_HO_HON01_S`

Single-objective optimization

Find an approximate first-order stationary point of the full objective, namely $\|\nabla f(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

**Status.** Bounds missing

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Kth derivative lipschitz

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Exact jet k; operation: Exact jet k; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate first-order stationary point of the full objective, namely $\|\nabla f(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is $C^k$ and bounded below; nonconvexity is allowed.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

$$\|D^{k}f(x)-D^{k}f(y)\|_{\mathrm{op},2}\le M_k\|x-y\|_{2}.$$

Fix $k\ge2$; no additional lower-order regularity bound is imposed.

Admissible parameter domain:

$$d\ge1,\quad k\ge2;\quad\text{all other parameters satisfy their tabulated ranges}.$$

### Oracle interface

Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $\Delta$, $M_k$, $\varepsilon_g$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\|\nabla f(\widehat{x})\|_2.$$

The criterion uses the gradient norm itself. Squared norms, expectations, and probability guarantees are recorded separately and are not substituted automatically.

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

$$\|\nabla f(\widehat{x})\|_2\le \varepsilon_g.$$

The running-cost guarantee is specified separately under RESOURCE.

#### Randomized

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[\|\nabla f(\widehat{x})\|_2\le \varepsilon_g\right]\ge\frac23.$$

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

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}_{\ge2}$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta\ge0$.

$M_k$: Global Lipschitz upper bound for the order-$k$ derivative in the tensor operator norm. **Domain:** $M_k\ge0$.

$\varepsilon_g$: Gradient-norm tolerance **Domain:** $\varepsilon_g>0$.

$C_k$: A sufficiently large positive constant depending only on the fixed order $k$, without a numerical value specified. **Domain:** $C_k>0$.

$c_k$: A sufficiently small positive constant depending only on the fixed order $k$, without a numerical value specified. **Domain:** $c_k>0$.

$A_k$: Dimensionless high-dimensional first-order stationarity workload **Domain:** $A_k\ge0$.

$$A_k=\Delta\,(M_k)^{\frac{1}{k}}\,((\varepsilon_g)^{(-1)\,(\frac{k+1}{k})}).$$

$S_k$: Natural one-dimensional gradient scale **Domain:** $S_k\ge0$.

$$S_k=((M_k)^{\frac{1}{k+1}})\,((\Delta)^{\frac{k}{k+1}}).$$

$\log_+(t)$: Truncated logarithm. **Domain:** $t>0$.

$$\log_+(t)=\max\{0,\log t\}.$$

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

#### Q3 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter window 1

**Region.** $A_k\ge C_k, d\ge C_k(1+A_k)$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega_k(A_k)
$$

**Upper bound.** B1

$$
O_k(1+A_k)
$$

**Gap or comparison.** $\Theta_k(1)$

### R2 - Parameter window 2

**Region.** $d=1, 0<\varepsilon_g\le c_k S_k$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B4, B13

$$
\Omega_k(1+\log(S_k/\varepsilon_g))
$$

**Upper bound.** B3, B12

$$
O_k(1+\log(S_k/\varepsilon_g))
$$

**Gap or comparison.** $\Theta_k(1)$

### R3 - Parameter window 3

**Region.** $\Delta=0$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B7, B16

$$
0
$$

**Upper bound.** B5, B14

$$
0
$$

### R4 - Parameter window 4

**Region.** $d\ge 1, \Delta>0, M_k>0, \varepsilon_g>0$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O_k(1+A_k)
$$

### R5 - Parameter window 5

**Region.** $\Delta>0, M_k=0$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B8, B17

$$
1
$$

**Upper bound.** B6, B15

$$
1
$$

**Gap or comparison.** $1$

### R6 - Parameter window 1

**Region.** $A_k\ge C_k, d\ge C_k(1+A_k)\log(3+A_k)$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B11

$$
\Omega_k(1+A_k)
$$

**Upper bound.** B9

$$
O_k(1+A_k)
$$

**Gap or comparison.** $\Theta_k(1)$

### R7 - Parameter window 3

**Region.** $d\ge 1, \Delta>0, M_k>0, \varepsilon_g>0$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B9

$$
O_k(1+A_k)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Global minimization of the regularized Taylor model of order k

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C_k(1+\Delta M_k^{1/k}\varepsilon_g^{-(k+1)/k})
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

**Conditions.** $d\ge 1, \Delta>0, M_k>0, \varepsilon_g>0$

**Dimension conditions.** $d\ge 1, \Delta>0, M_k>0, \varepsilon_g>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf) theorem: Theorem 2.5; Lemmas 2.1–2.3; pdf pages: 7

### B2 - Robust zero-chain and resisting rotations

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c_k\Delta M_k^{1/k}\varepsilon_g^{-(k+1)/k}
$$

**Sources.** [2](https://arxiv.org/abs/1710.11606)

**Conditions.** $A_k\ge C_k, d\ge C_k(1+A_k)$

**Dimension conditions.** $A_k\ge C_k, d\ge C_k(1+A_k)$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [2](https://arxiv.org/abs/1710.11606) theorem: Theorem 1; pdf pages: 14

### B3 - Value-based bisection and local interpolation

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C_k[1+\log_+(S_k/\varepsilon_g)]
$$

**Sources.** [3](https://arxiv.org/abs/2610.16295)

**Conditions.** $d=1, 0<\varepsilon_g\le c_k S_k$

**Dimension conditions.** $d=1, 0<\varepsilon_g\le c_k S_k$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [3](https://arxiv.org/abs/2610.16295) theorem: Theorem 7.1; pdf pages: 11

### B4 - Ordered hidden intervals with at most three local responses

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_k[1+\log(S_k/\varepsilon_g)]
$$

**Sources.** [3](https://arxiv.org/abs/2610.16295) [5](https://arxiv.org/abs/1710.11606v3) [6](https://arxiv.org/abs/1811.01220)

**Conditions.** $d=1, 0<\varepsilon_g\le c_k S_k$

**Dimension conditions.** $d=1, 0<\varepsilon_g\le c_k S_k$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1

**Source location.** [3](https://arxiv.org/abs/2610.16295) theorem: Theorem 6.1; Appendix E.2; pdf pages: 9

### B5 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A2

### B6 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $\Delta>0, M_k=0$

**Dimension conditions.** $\Delta>0, M_k=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A2

### B7 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A2

### B8 - Zero-query indistinguishability of translated quadratics

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $\Delta>0, M_k=0$

**Dimension conditions.** $\Delta>0, M_k=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A2

### B9 - Global minimization of the regularized Taylor model of order k

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C_k(1+\Delta M_k^{1/k}\varepsilon_g^{-(k+1)/k})
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

**Conditions.** $d\ge 1, \Delta>0, M_k>0, \varepsilon_g>0$

**Dimension conditions.** $d\ge 1, \Delta>0, M_k>0, \varepsilon_g>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf) theorem: Theorem 2.5; Lemmas 2.1–2.3; pdf pages: 7

### B10 - Random rotation and radial modification

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_k\Delta M_k^{1/k}\varepsilon_g^{-(k+1)/k}
$$

**Sources.** [2](https://arxiv.org/abs/1710.11606)

**Conditions.** $A_k\ge C_k,\quad d\ge C_k(1+A_k)^2\log(3+A_k)$

**Dimension conditions.** $A_k\ge C_k,\quad d\ge C_k(1+A_k)^2\log(3+A_k)$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [2](https://arxiv.org/abs/1710.11606) theorem: Theorem 2; pdf pages: 19

### B11 - Single-component radial chain with a random hidden direction

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_k(1+\Delta M_k^{1/k}\varepsilon_g^{-(k+1)/k})
$$

**Sources.** [4](https://arxiv.org/abs/2609.28202)

**Conditions.** $A_k\ge C_k, d\ge C_k(1+A_k)\log(3+A_k)$

**Dimension conditions.** $A_k\ge C_k, d\ge C_k(1+A_k)\log(3+A_k)$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [4](https://arxiv.org/abs/2609.28202) theorem: Theorems 3.2,3.4; Appendix E.2; pdf pages: 5

### B12 - Value-based bisection and local interpolation

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C_k[1+\log_+(S_k/\varepsilon_g)]
$$

**Sources.** [3](https://arxiv.org/abs/2610.16295)

**Conditions.** $d=1, 0<\varepsilon_g\le c_k S_k$

**Dimension conditions.** $d=1, 0<\varepsilon_g\le c_k S_k$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [3](https://arxiv.org/abs/2610.16295) theorem: Theorem 7.1; pdf pages: 11

### B13 - Ordered hidden intervals with at most three local responses

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_k[1+\log(S_k/\varepsilon_g)]
$$

**Sources.** [3](https://arxiv.org/abs/2610.16295) [5](https://arxiv.org/abs/1710.11606v3) [6](https://arxiv.org/abs/1811.01220)

**Conditions.** $d=1, 0<\varepsilon_g\le c_k S_k$

**Dimension conditions.** $d=1, 0<\varepsilon_g\le c_k S_k$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1

**Source location.** [3](https://arxiv.org/abs/2610.16295) theorem: Theorem 6.1; Appendix E.2; pdf pages: 9

### B14 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A2

### B15 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $\Delta>0, M_k=0$

**Dimension conditions.** $\Delta>0, M_k=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A2

### B16 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A2

### B17 - Zero-query indistinguishability of translated quadratics

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $\Delta>0, M_k=0$

**Dimension conditions.** $\Delta>0, M_k=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A2

## 5. Local arguments

### A1 - Hölder scaling and one-dimensional information reductions

**Scope.** One-dimensional reductions preserve value versus derivative-only interfaces. Hölder interpolation uses global bounded and Lipschitz derivative properties of the chosen chain, not an unstated assumption on the entire target class.

**Algorithm scope.** One-dimensional reductions preserve value versus derivative-only interfaces. Hölder interpolation uses global bounded and Lipschitz derivative properties of the chosen chain, not an unstated assumption on the entire target class.

Highest-order Hölder lower bounds follow by interpolation and rescaling; one-dimensional value access and derivative-only access remain distinct.

If the normalized smooth hard chain satisfies $\sup_x\|D^kh(x)\|\le B_k$ and $\operatorname{Lip}(D^kh)\le L_k$, then
$$\|D^kh(x)-D^kh(y)\|\le(2B_k)^{1-\nu}L_k^\nu\|x-y\|^\nu.$$
This follows by bounding the difference by both $2B_k$ and $L_k\|x-y\|$ and interpolating the minimum. For $s=k+\nu$ and $f(x)=a h(x/b)$, the gradient scale is $a/b$ and the Hölder scale is $a/b^s$. Enforcing scales $\varepsilon_g$ and $M_{k,\nu}$ gives
$$b\asymp_{k,\nu}(\varepsilon_g/M_{k,\nu})^{1/(s-1)},\qquad
N\asymp_{k,\nu}\Delta M_{k,\nu}^{1/(s-1)}\varepsilon_g^{-s/(s-1)}.$$
Use the deterministic or randomized CDHS dimension condition matching the algorithm view. The Hölder upper bound uses CGTweak, Theorem 3.4, with the same parameter scaling.

In one dimension, let I be the promised derivative orders, $k\in I$, $s_j=j+\nu_j$, and $S=\min_{j\in I}M_{j,\nu_j}^{1/s_j}\Delta^{(s_j-1)/s_j}$. ZS26, Theorem 3.1 gives the derivative-only randomized lower bound $\Omega_k(S/\varepsilon_g)$; Theorem 4.1 gives the deterministic power lower bound, and Theorem 5.1's matching method reads only f'. For full local information including values, Theorems 6.1 and 7.1 give logarithmic lower and upper bounds in $S/\varepsilon_g$. These theorem statements, not a general simulation, support the change of information complexity.

The full-information lower theorem lists all derivative orders. For a highest-order-only target class, impose additional finite lower-order bounds solely on the hard subclass, choosing their natural scales at least the highest-order scale. The subclass is contained in the target class; those extra constants are not algorithm inputs.

To convert a source algorithm with success probability 1/2 and strict target $|f'|<\varepsilon$ to success at least 2/3 with nonstrict target $\varepsilon_g$, run two independent copies at $\varepsilon_g/2$. Query f' at both candidates, retain any verified success, and otherwise return within the fixed cap. Success is at least 3/4, and cost changes by a constant factor. Lower bounds for the weaker 1/2 guarantee also constrain the stronger 2/3 requirement, with a constant rescaling of strictness if needed.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [5](https://arxiv.org/abs/1710.11606v3) [6](https://arxiv.org/abs/1811.01220) [3](https://arxiv.org/abs/2610.16295)

### A2 - Zero-query and polynomial-recovery endpoints

**Scope.** Applies only to the indicated objective-gap, first-order, or spectral second-order criteria. A true minimizer need not satisfy a finite-radius high-order Taylor-decrease criterion; those criteria require their own argument. Public-domain, curvature, and accuracy conditions remain those of the linked bound.

**Algorithm scope.** Applies only to the indicated objective-gap, first-order, or spectral second-order criteria. A true minimizer need not satisfy a finite-radius high-order Taylor-decrease criterion; those criteria require their own argument. Public-domain, curvature, and accuracy conditions remain those of the linked bound.

Zero-query guarantees follow from a public initial-error bound. A zero highest-order regularity modulus permits exact polynomial recovery from one complete jet.

For a full-space differentiable objective with $f(x_0)-\inf f\le\Delta$, the condition $\Delta=0$ makes $x_0$ a global minimizer. Its gradient is zero, and its Hessian is positive semidefinite whenever it exists. Thus first-order and spectral second-order stationarity require no query. An objective-gap target also requires no query when $\varepsilon_f\ge\Delta$. Nonnegative query cost proves exact optimality of these zero bounds.

If a public gradient-Lipschitz bound $\beta$ is part of the specification, the descent lemma gives $\|\nabla f(x_0)\|^2\le2\beta\Delta$. For convex full-space objectives with a minimizer within distance $R$, it also gives $f(x_0)-f^*\le\beta R^2/2$ and $\|\nabla f(x_0)\|\le\beta R$. These sufficient zero-query regions require that explicit first-order regularity assumption. If only the highest derivative is controlled, positive quadratics can have arbitrary curvature and arbitrarily large initial gap despite zero highest-order modulus.

On a connected Euclidean domain, $M_k=0$ or $M_{k,\nu}=0$ makes $D^kf$ constant, so $f$ is a polynomial of degree at most $k$. One complete jet determines all coefficients. Under the specified free internal computation, a known polynomial can then be optimized on a compact public domain, or combined with a public regularizer and solved through the declared known-model interface.

A bounded-below polynomial on the full space need not attain its infimum. For approximate spectral stationarity, shift $x_0$ to zero and minimize $f(x)+\eta\|x\|^2/2$. This function is coercive, and its minimizer $x_\eta$ satisfies $\eta\|x_\eta\|^2/2\le\Delta$, $\|\nabla f(x_\eta)\|\le\sqrt{2\eta\Delta}$, and $\nabla^2f(x_\eta)\succeq-\eta I$. Choosing $\eta\le\min\{\varepsilon_H,\varepsilon_g^2/(2\Delta)\}$ meets both targets. For global objective accuracy, exact polynomial coefficients permit arbitrary-accuracy internal global optimization; no additional unknown-function query is needed.

To exclude zero queries in a nontrivial region, choose two positive quadratics centered on opposite sides of $x_0$, with the same public budgets and disjoint acceptable-output sets. A zero-query algorithm has the same output distribution on both instances, so their success probabilities sum to at most one. It cannot succeed with probability at least $2/3$ on each. With only highest-order regularity, curvature can be increased until the acceptable sets are disjoint at any prescribed positive accuracy and positive localization radius. In an initial-gap model with additional curvature restrictions, retain the bound's explicit accuracy and compatibility window.

If both a global PL constant $\mu$ and a gradient-Lipschitz upper bound $\beta$ are supplied, then $2\mu(f-f_*)\le\|\nabla f\|^2\le2\beta(f-f_*)$. When $\mu>\beta>0$, every gap is zero and the class contains only constant objectives. This degeneracy does not apply without the extra $\beta$ assumption.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

## References

[1] E. G. Birgin; J. L. Gardenghi; J. M. Martínez; S. A. Santos; Ph. L. Toint. Worst-case evaluation complexity for unconstrained nonlinear optimization using high-order regularized models. NAXYS-05-2015, 2015-07-10; Mathematical Programming 163 (2017), 359–368.

https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf

[2] Yair Carmon; John C. Duchi; Oliver Hinder; Aaron Sidford. Lower Bounds for Finding Stationary Points I. arXiv:1710.11606v3, 2019-08-15; Mathematical Programming 184 (2020), 71–120.

https://arxiv.org/abs/1710.11606

[3] Huanjian Zhou; Taiji Suzuki. On the Complexity of Finding Stationary Points of p-th Order Hölder Smooth Functions in One Dimension. arXiv:2610.16295v1, 2026-10-12, preprint.

https://arxiv.org/abs/2610.16295

[4] Wendao Wu; Haihan Zhang; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Upper and Lower Bounds for Higher-Order Nonconvex Finite-Sum Optimization. arXiv:2609.28202v2, 2026-10-19, preprint.

https://arxiv.org/abs/2609.28202

[5] Yair Carmon, John C. Duchi, Oliver Hinder, Aaron Sidford. Lower Bounds for Finding Stationary Points I. arXiv:1710.11606v3; Mathematical Programming 184 (2020).

https://arxiv.org/abs/1710.11606v3

[6] Coralia Cartis; Nicholas I. M. Gould; Philippe L. Toint. Sharp worst-case evaluation complexity bounds for arbitrary-order nonconvex optimization with inexpensive constraints. arXiv:1811.01220v1, 2018-11-03; SIAM Journal on Optimization 30(1) (2020), 513–541.

https://arxiv.org/abs/1811.01220
