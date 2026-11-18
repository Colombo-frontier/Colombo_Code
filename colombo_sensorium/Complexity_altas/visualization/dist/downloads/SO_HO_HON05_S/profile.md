# Nonconvex second-order stationarity with complete high-order derivatives and independent tolerances

**Setting ID.** `SO_HO_HON05_S`

Single-objective optimization

Find an approximate second-order stationary point of the full objective:

**Status.** Bounds missing

**TASK tags.** formulation: Second order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Kth derivative lipschitz

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Exact jet k; operation: Exact jet k; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic algorithms; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Second order stationarity; criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate second-order stationary point of the full objective:

$$\|\nabla f(\widehat{x})\|_2\le\varepsilon_g,\qquad\nabla^2f(\widehat{x})\succeq-\varepsilon_H I_d.$$

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is $C^k$ and bounded below; nonconvexity is allowed.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

$$\|D^{k}f(x)-D^{k}f(y)\|_{\mathrm{op},2}\le M_k\|x-y\|_{2}.$$

Fix $k\ge2$; no additional lower-order regularity bound is imposed.

Admissible parameter domain:

$$d\ge1,\quad k\ge2;\quad\text{all other parameters satisfy their tabulated ranges}.$$

### Oracle interface

Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $\Delta$, $M_k$, $\varepsilon_g$, $\varepsilon_H$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\max\left\{\frac{\|\nabla f(\widehat{x})\|_2}{\varepsilon_g},\frac{[-\lambda_{\min}(\nabla^2f(\widehat{x}))]_+}{\varepsilon_H}\right\}.$$

$[a]_+=\max\{a,0\}$, and $\lambda_{\min}$ denotes the smallest eigenvalue of a symmetric matrix. The target is $\mathcal{E}(\widehat{x})\le1$, where $\varepsilon_g$ and $\varepsilon_H$ are independent positive tolerances.

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

$$\max\left\{\frac{\|\nabla f(\widehat{x})\|_2}{\varepsilon_g},\frac{[-\lambda_{\min}(\nabla^2f(\widehat{x}))]_+}{\varepsilon_H}\right\}\le 1.$$

The running-cost guarantee is specified separately under RESOURCE.

#### Randomized

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[\max\left\{\frac{\|\nabla f(\widehat{x})\|_2}{\varepsilon_g},\frac{[-\lambda_{\min}(\nabla^2f(\widehat{x}))]_+}{\varepsilon_H}\right\}\le 1\right]\ge\frac23.$$

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

$\lambda_{\min}(A),[z]_+$: The smallest eigenvalue of a symmetric matrix and the positive part of a scalar.

$$[z]_+=\max\{z,0\}.$$

$I_d$: The identity matrix in dimension $d$.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}_{\ge2}$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta\ge0$.

$M_k$: Global Lipschitz upper bound for the order-$k$ derivative in the tensor operator norm. **Domain:** $M_k\ge0$.

$\varepsilon_g$: Gradient-norm tolerance **Domain:** $\varepsilon_g>0$.

$\varepsilon_H$: Tolerance for negative Hessian curvature **Domain:** $\varepsilon_H>0$.

$C_k$: A sufficiently large positive constant depending only on the fixed order $k$, without a numerical value specified. **Domain:** $C_k>0$.

$A$: Gradient workload **Domain:** $A\ge0$.

$$A=\Delta\,(M_k)^{\frac{1}{k}}\,((\varepsilon_g)^{(-1)\,(\frac{k+1}{k})}).$$

$B$: Negative-curvature workload **Domain:** $B\ge0$.

$$B=\Delta\,((M_k)^{\frac{2}{k-(1)}})\,((\varepsilon_H)^{(-1)\,(\frac{k+1}{k-(1)})}).$$

$C_0$: Fixed gradient-dominance ratio in this regime, retained as a symbolic constant. **Domain:** $C_0>0$.

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

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter window 1

**Region.** $\max{A,B}\ge C_k,d\ge C_k(1+A+B)$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B6

$$
\Omega_k(\max{A,B})=\Omega_k(A+B)
$$

**Upper bound.** B1

$$
O_k(1+A+B)
$$

**Gap or comparison.** $\Theta_k(1)$

### R2 - Parameter window 2

**Region.** $\Delta=0$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q4

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B5, B10

$$
0
$$

**Upper bound.** B4, B9

$$
0
$$

### R3 - Parameter window 3

**Region.** $k\ge 3,B>C_0 A$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** B6

$$
\Omega_k(A+B)\quad\text{on r3 only}
$$

**Upper bound.** B1

$$
O_k(1+A+B)
$$

**Gap or comparison.**

$$
\Theta_k(1)\text{ on r3; lower bound missing outside r3}
$$

### R4 - Parameter window 4

**Region.** $d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** B6

$$
\Omega_k(A+B)\quad\text{on r3 only}
$$

**Upper bound.** B1

$$
C_k(1+A+B)
$$

**Gap or comparison.**

$$
\Theta_k(1)\text{ on r3; lower bound missing outside r3}
$$

### R5 - Parameter window 1

**Region.** $A\ge C_k,B\le C_0 A,d\ge C_k(1+A)\log(3+A)$

**Views.** Randomized

**Quantity.** Q3

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B8

$$
\Omega_k(1+A)
$$

**Upper bound.** B7

$$
O_k(1+A+B)
$$

**Gap or comparison.** $\Theta_{k,C0}(1)$

### R6 - Parameter window 2

**Region.** $k\ge 3,B>C_0 A$

**Views.** Randomized

**Quantity.** Q4

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** B11

$$
\Omega_k(1+A)\quad\text{on r7 only}
$$

**Upper bound.** B7

$$
O_k(1+A+B)
$$

**Gap or comparison.**

$$
O_k((1+A+B)/(1+A))\text{ on r7; lower bound missing outside r7}
$$

### R7 - Parameter window 4

**Region.** $d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$

**Views.** Randomized

**Quantity.** Q4

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** B11

$$
\Omega_k(1+A)\quad\text{on r7 only}
$$

**Upper bound.** B7

$$
C_k(1+A+B)
$$

**Gap or comparison.**

$$
O_k((1+A+B)/(1+A))\text{ on r7; lower bound missing outside r7}
$$

### R8 - Exact one-query polynomial branch

**Region.** $\Delta>0,M_k=0$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q4

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B13, B15

$$
1
$$

**Upper bound.** B12, B14

$$
1
$$

**Gap or comparison.** 1

### R9 - Randomized q2 matching first-order-dominated window

**Region.** $A\ge C_k,B\le C_0 A,d\ge C_k(1+A)\log(3+A)$

**Views.** Randomized

**Quantity.** Q4

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B11

$$
\Omega_k(1+A)
$$

**Upper bound.** B7

$$
O_{k,C_0}(1+A)
$$

**Gap or comparison.** Theta_{k,C0}(1), with fixedC0; no varyingB/A hidden in constants.

**Comparison argument.** HO_RANDOMIZED_Q2_J_NATIVE_CLOSURE_20261116

## 4. Bounds and supporting evidence

### B1 - High-order regularized models jointly control the next-point gradient and smallest eigenvalue

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C_k(1+A+B)
$$

**Sources.** [3](https://arxiv.org/abs/1708.04044)

**Conditions.** $d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$

**Dimension conditions.** $d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$

**Oracle correspondence.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

**Source location.** [3](https://arxiv.org/abs/1708.04044) pdf pages: 8; theorem: Theorem3.6 and Lemmas3.2–3.4

### B2 - Hard subclass for first-order stationarity

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c_k A
$$

**Sources.** [2](https://arxiv.org/abs/1710.11606)

**Conditions.** $A\ge C_k,d\ge C_k(1+A)$

**Dimension conditions.** $A\ge C_k,d\ge C_k(1+A)$

**Oracle correspondence.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

**Source location.** [2](https://arxiv.org/abs/1710.11606) pdf pages: 14; theorem: Theorem1

### B3 - Curvature-robust zero-chain with deterministic resisting rotations

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c_k B
$$

**Sources.** [1](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) [5](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) [6](https://arxiv.org/abs/2610.16832) [7](https://arxiv.org/abs/1710.11606v3) [8](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

**Conditions.** $B\ge C_k,d\ge C_k(1+B)$

**Dimension conditions.** $B\ge C_k,d\ge C_k(1+B)$

**Oracle correspondence.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

**Local argument.** HO_CURVATURE_LOWER, HO_MULTI_REGULARITY, HO_REGULARIZED_DESCENT

**Source location.** [1](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) pdf pages: 58; theorem: Appendix H.2, noiseless specialization

### B4 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Oracle correspondence.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

**Local argument.** HO_ENDPOINTS

### B5 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Oracle correspondence.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

**Local argument.** HO_ENDPOINTS

### B6 - Regime-wise combination of gradient and negative-curvature hard families

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c_k(A+B)
$$

**Sources.** [2](https://arxiv.org/abs/1710.11606) [1](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) [5](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) [6](https://arxiv.org/abs/2610.16832) [7](https://arxiv.org/abs/1710.11606v3) [8](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

**Conditions.** $\max{A,B}\ge C_k,d\ge C_k(1+A+B)$

**Dimension conditions.** $\max{A,B}\ge C_k,d\ge C_k(1+A+B)$

**Oracle correspondence.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

**Local argument.** HO_CURVATURE_LOWER, HO_MULTI_REGULARITY, HO_REGULARIZED_DESCENT

**Source location.** [2](https://arxiv.org/abs/1710.11606) pdf pages: 14; theorem: Theorem1

**Source location.** [1](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) pdf pages: 58; theorem: Appendix H.2, noiseless specialization

### B7 - High-order regularized models jointly control the next-point gradient and smallest eigenvalue

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C_k(1+A+B)
$$

**Sources.** [3](https://arxiv.org/abs/1708.04044)

**Conditions.** $d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$

**Dimension conditions.** $d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$

**Oracle correspondence.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

**Source location.** [3](https://arxiv.org/abs/1708.04044) pdf pages: 8; theorem: Theorem3.6 and Lemmas3.2–3.4

### B8 - Second-order stationarity includes the first-order requirement

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_k(1+A)
$$

**Sources.** [4](https://arxiv.org/abs/2609.28202)

**Conditions.** $A\ge C_k,B\le C_0 A,d\ge C_k(1+A)\log(3+A)$

**Dimension conditions.** $A\ge C_k,B\le C_0 A,d\ge C_k(1+A)\log(3+A)$

**Oracle correspondence.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

**Source location.** [4](https://arxiv.org/abs/2609.28202) pdf pages: 5; theorem: Theorems3.2/3.4 n=1

### B9 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Oracle correspondence.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

**Local argument.** HO_ENDPOINTS

### B10 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Oracle correspondence.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Output rule.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource conversion.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

**Local argument.** HO_ENDPOINTS

### B11 - n=1 full-jet source lower bound; simultaneous stationarity implies gradient stationarity

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_k(1+A)
$$

**Sources.** [4](https://arxiv.org/abs/2609.28202)

**Conditions.** Delta>0, M_k>0, A>=C_k, d>=C_k(1+A)log(3+A)

**Oracle correspondence.** Exact full k-jet at one point costs one call.

**Guarantee conversion.** Success probability at least 2/3 for every fixed admissible instance.

**Output rule.** Any point, including an unqueried point.

**Resource conversion.** Fixed worst-case cap on every execution path; all responses counted.

**Local argument.** HO_RANDOMIZED_GRADIENT_TRANSFER

**Source location.** [4](https://arxiv.org/abs/2609.28202) pdf pages: 5; 6; printed pages: 5; 6; theorem: Definition 3.1; Theorems 3.2 and 3.4; arXiv:2609.28202v2; archived characters 13323-16400

n=1, p=k; first-order necessity and flat dimension padding are proved in HO_RANDOMIZED_GRADIENT_TRANSFER.

### B12 - One jet reconstructs f; free regularized polynomial minimization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

**Oracle correspondence.** Exact full k-jet at one point costs one call.

**Guarantee conversion.** Deterministic success for every admissible instance.

**Output rule.** Any point, including an unqueried point.

**Resource conversion.** Fixed worst-case cap on every execution path; all responses counted.

**Local argument.** HO_POLYNOMIAL_ONE_CALL

### B13 - Two positive quadratics with disjoint acceptable-output balls exclude zero calls

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
1
$$

**Conditions.** Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

**Oracle correspondence.** Exact full k-jet at one point costs one call.

**Guarantee conversion.** Deterministic success for every admissible instance.

**Output rule.** Any point, including an unqueried point.

**Resource conversion.** Fixed worst-case cap on every execution path; all responses counted.

**Local argument.** HO_POLYNOMIAL_ONE_CALL

### B14 - One jet reconstructs f; free regularized polynomial minimization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

**Oracle correspondence.** Exact full k-jet at one point costs one call.

**Guarantee conversion.** Success probability at least 2/3 for every fixed admissible instance.

**Output rule.** Any point, including an unqueried point.

**Resource conversion.** Fixed worst-case cap on every execution path; all responses counted.

**Local argument.** HO_POLYNOMIAL_ONE_CALL

### B15 - Two positive quadratics with disjoint acceptable-output balls exclude zero calls

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

**Oracle correspondence.** Exact full k-jet at one point costs one call.

**Guarantee conversion.** Success probability at least 2/3 for every fixed admissible instance.

**Output rule.** Any point, including an unqueried point.

**Resource conversion.** Fixed worst-case cap on every execution path; all responses counted.

**Local argument.** HO_POLYNOMIAL_ONE_CALL

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: b2e9b6b70c4ea545c7767a79fa012a1d95643ba0d74a3c4dbaea0a9bdd580607

### Native proof: HO_CURVATURE_LOWER

Native pointer: /proofs/0; canonical SHA-256: ea6aec714e02700b0e628931da047d856e7a0ebd6a8c63a0c91876c60d84eeaf

#### Native field: algorithm_scope

Native pointer: /proofs/0/algorithm_scope; canonical SHA-256: e7631280608e65306a624bac6f81b095d63315e6ba226b83db7bfc04924dcd71

The deterministic rotation extension and arbitrary-randomized second-order primary result are distinct. Preserve restricted algorithm classes, fixed-parameter qualifiers, tolerance windows, preprint status, and sufficient dimensions.

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 8b2356c60fae01a303ef034de840ae671bb7c46284ad3aff7534fc86c1242ca8

The noiseless specialization in ACDFSS20, Appendix H.2, gives a zero-respecting curvature lower bound
$$\Omega_k\left(\frac\Delta{\varepsilon_H}\min_{2\le j\le k}(M_j/\varepsilon_H)^{2/(j-1)}\right),$$
within the nonautomatic window $\varepsilon_H\le c_kM_1$. For deterministic algorithms, adaptively rotate the smooth gated chain. Unactivated gates have every derivative zero, so each complete jet reveals at most the next direction, including its value response. Choose later directions orthogonal to prior queries and, at the end, to the unqueried output. A sufficient dimension $C_k(1+N)$ accommodates all constraints. Determinism ensures that the final single rotated instance produces the constructed transcript. This seed-dependent adversary argument does not prove an arbitrary-randomized lower bound.

With only $M_k$ controlled, choose width $b\asymp(\varepsilon_H/M_k)^{1/(k-1)}$ and amplitude $a\asymp\varepsilon_Hb^2$. Then
$$N\asymp_k\Delta M_k^{2/(k-1)}\varepsilon_H^{-(k+1)/(k-1)}.$$
Additional $\beta$-smoothness requires $\varepsilon_H\le c\beta$. Combine this hard family with the separate gradient hard family by taking their maximum, which is equivalent up to a factor two to the sum; no one instance is claimed to realize both difficulties simultaneously.

For arbitrary randomized exact second-order algorithms, REUSE26v2's deterministic-loss subclass supplies the separate curvature result. Its gated chain has $O(N)$ value range and dimension-independent Hessian and third-derivative operator bounds. With $\gamma=\varepsilon_H$, spatial scale of order $\gamma$, and amplitude of order $\gamma^3$, take N of order $\gamma^{-3}$. A radial cutoff and wall at radius of order $\gamma^{-1}$ prevent unrestricted distant queries or outputs from bypassing the chain: outside the hard region the gradient is too large, while the transition region retains negative curvature. Conditional exposure of hidden rotation directions and concentration over every query and the final output give the sufficient dimension
$$d\ge C_\theta[1+\gamma^{-4}\log(2+\gamma^{-1})+\gamma^{-3}],\qquad\theta=(\beta,M_2,\Delta).$$
Thus, for fixed positive $\theta$ and sufficiently small independent tolerances, the primary result yields $\Omega_{\theta}(\varepsilon_H^{-3})$. Combining it with the randomized gradient lower bound gives the linked exact-J2 bracket. Constants may depend on fixed $\theta$; this is not a joint-parameter lower bound with universal constants, nor a higher-order randomized theorem.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: 918705965626e3df518889587e400c0256e29c0f4de1cd53ae94b6c6343683b9

The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

#### Native field: module_dependencies

Native pointer: /proofs/0/module_dependencies; canonical SHA-256: 0ea7d779794e574b392cb0e5609cbc1d2f7e89ee158788ee998a1e6c7cd73f30

#### Native item 1

Native pointer: /proofs/0/module_dependencies/0; canonical SHA-256: 18d60db987286d34cea63943c53af3776cd00c08daea4dfe2ae38e36f8e9e7b8

HO_MULTI_REGULARITY

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: e7631280608e65306a624bac6f81b095d63315e6ba226b83db7bfc04924dcd71

The deterministic rotation extension and arbitrary-randomized second-order primary result are distinct. Preserve restricted algorithm classes, fixed-parameter qualifiers, tolerance windows, preprint status, and sufficient dimensions.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: a75a145f0238f9fc47e1cfe38e117a7d7a4b1a64506612ec7bf946b765f00042

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: b94d81bf8d0c218567bc0a6900a7fbcd503a6f25e62a5102d46c6a24052a07e5

SO_SRC_6948bf8f8c23676c

#### Native item 2

Native pointer: /proofs/0/source_refs/1; canonical SHA-256: 72f15b8b51b86b83c82b097c98a0a6c4aa505de1d08d26c605f0d9991df84f11

SO_SRC_b954002f48cd0141

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: d3f0fd938f20f073f58c2344bdddd5b9574f7a50804eb2cd5fc25f6c54eaebdc

Deterministic curvature lower bounds use a resisting-rotation reduction; the arbitrary-randomized exact-second-order result is separately tied to a primary fixed-parameter theorem.

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 167706646414198e6abce83e3ddcc09900cbfdc6d7349e6d1292635638457740

Curvature lower bounds and their algorithm scope

### Native proof: HO_MULTI_REGULARITY

Native pointer: /proofs/1; canonical SHA-256: 0d0ebd30b5d87ff7f3b4d1f5334e4f72fb8710bb3b0ac5b911a3a82fed4685cb

#### Native field: algorithm_scope

Native pointer: /proofs/1/algorithm_scope; canonical SHA-256: 748044c9eb4efa3c2e26c076542527e51222b1195eaa41ae98ed06bf2f8d0742

Jointly declared positive regularity budgets. Deterministic and randomized lower bounds retain their distinct sufficient dimensions and source scope.

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 1c686da3222c80218c67595c44cd00127d21854cd62def011f9cb155c68b8246

For each fixed j, use the jth-order regularized method, reading only the relevant part of the complete k-jet. Its budget is $C_j[1+\Delta M_j^{1/j}\varepsilon_g^{-(j+1)/j}]$. All parameters are public, so an algorithm may select the smallest proved budget. This minimum is an envelope of complete algorithms.

For the lower bound, use the robust CDHS smooth chain $h_N$, whose initial gap is at most $C_kN$, whose gradient stays bounded away from zero before completion, and whose jth-derivative Lipschitz modulus is at most a constant $\ell_j$ depending only on j. Set $f(x)=a h_N(x/b)$ with
$$a/b=K_k\varepsilon_g,\qquad
b=\max_{1\le j\le k}(K_k\ell_j\varepsilon_g/M_j)^{1/j}.$$
Then $\operatorname{Lip}(D^jf)=a\ell_j/b^{j+1}\le M_j$ for every j simultaneously. Choosing N proportional to $\Delta/a$ gives N of order A. For A above a fixed k-dependent threshold, deterministic resisting rotations fit in $d\ge C_k(1+A)$; the classical randomized radial construction fits in $d\ge C_k(1+A)^2\log(3+A)$. These are sufficient dimensions.

If the primary result is stated as time to query a successful point, append one complete-jet query at the algorithm's final output. A lower bound of N then gives an original-budget lower bound N-1, of the same order in the nontrivial A region. This handles arbitrary unqueried outputs without changing the success quantifier.

For $k=2$, the common scaling gives $A=\Delta\min\{\beta\varepsilon_g^{-2},\sqrt{M_2}\varepsilon_g^{-3/2}\}$. Keep the zero-query region $\varepsilon_g^2\ge2\beta\Delta$ separate; the whole domain is not uniformly Theta(1+A). Dimension improvements proved for a highest-order-only model do not automatically preserve all lower-order budgets.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: 918705965626e3df518889587e400c0256e29c0f4de1cd53ae94b6c6343683b9

The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

#### Native field: module_dependencies

Native pointer: /proofs/1/module_dependencies; canonical SHA-256: d5dcd732fb3969e08b9b1a961c61061337b5c38a2eed2076db6d15e0c728fc73

#### Native item 1

Native pointer: /proofs/1/module_dependencies/0; canonical SHA-256: f77592dbde85797058a609134cf6afa9d4f50a25d239219c1b47d5fb0ae1b70f

HO_REGULARIZED_DESCENT

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 748044c9eb4efa3c2e26c076542527e51222b1195eaa41ae98ed06bf2f8d0742

Jointly declared positive regularity budgets. Deterministic and randomized lower bounds retain their distinct sufficient dimensions and source scope.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: dc7f821958e3cc0989409026e7775e27772a4a25ff55341bec58a34b2cb218ea

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: f00c6d5c7d3d9705d8ad04d097f84e286c0b36be79f0bbe0a88cf04768e32dc9

SO_SRC_3400224028061741

#### Native field: statement

Native pointer: /proofs/1/statement; canonical SHA-256: 4f9277d4faa34b8843ff69afdb04cfe69cb052f957078773137acee8b3965553

For jointly bounded derivative Lipschitz moduli, the first-order scale is $A=\Delta\min_{1\le j\le k}M_j^{1/j}\varepsilon_g^{-(j+1)/j}$, with $M_1=\beta$.

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 83305bed0881c9c7b021021382ff01a4aedc0306ef031a2b9c70169d2d84f46b

Simultaneous regularity budgets and common lower-bound scaling

### Native proof: HO_REGULARIZED_DESCENT

Native pointer: /proofs/2; canonical SHA-256: f265478cd585f58aa3443d41fe70f46ffb456b517ba2a4977f1b3451f06021fe

#### Native field: algorithm_scope

Native pointer: /proofs/2/algorithm_scope; canonical SHA-256: c4d6434ac949e2b6b906923723d972935ac965572c321f94bebfcb374eb6945e

Fixed derivative order, complete exact jets, full-space queries, bounded initial gap, and free global known-model solution. Zero modulus is treated by polynomial recovery.

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: 5936b194a7c7301cb3c75257948fbde504be4f0a3e4484ce0992e45f43d47486

At x, form $m_x(s)=T_k(f;x,s)+a_kM_k\|s\|^{k+1}$, choosing $a_k$ sufficiently large, depending only on k, to dominate the Taylor remainder with slack. For $M_k>0$ the model is coercive, so it has a global minimizer, available under the declared free internal computation. Comparing the model at s and zero and applying the value remainder gives
$$f(x)-f(x+s)\ge c_kM_k\|s\|^{k+1}.$$
Model first-order optimality and the gradient remainder give
$$\|\nabla f(x+s)\|\le C_kM_k\|s\|^k.$$
If the next point is not $\varepsilon_g$-stationary, the decrease is at least $c_kM_k^{-1/k}\varepsilon_g^{(k+1)/k}$. The total decrease is at most $\Delta$, so after the displayed number of calls, including initialization and final verification, stationarity is reached.

This is the parameter restoration of the regularized-model argument in BGMST17, Lemmas 2.1–2.3 and Theorem 2.5. Its normalization is $(k-1)!L=M_k$. Separate function and derivative evaluations in the source cost only a fixed multiple when complete jets are charged as one. The argument is about information calls and does not assert an inexpensive arithmetic implementation of global nonconvex model minimization.

#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: 918705965626e3df518889587e400c0256e29c0f4de1cd53ae94b6c6343683b9

The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: c4d6434ac949e2b6b906923723d972935ac965572c321f94bebfcb374eb6945e

Fixed derivative order, complete exact jets, full-space queries, bounded initial gap, and free global known-model solution. Zero modulus is treated by polynomial recovery.

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: b8722949257a952fc946d69bd8c283a5753716e5a3e79453e2c125aac9f71e79

#### Native item 1

Native pointer: /proofs/2/source_refs/0; canonical SHA-256: 33f8e9246608380d16d457cc4ac626e35b03c98b4cf8bc3c5ae53c6a8e14dd47

SO_SRC_8b820eaa5c1d7163

#### Native field: statement

Native pointer: /proofs/2/statement; canonical SHA-256: 74205485655ec8cf14bfbd38471458e6fc6a9681646cfeef71ee8fefd662d856

With a Lipschitz kth derivative and fixed $k\ge2$, first-order stationarity uses $O_k(1+\Delta M_k^{1/k}\varepsilon_g^{-(k+1)/k})$ complete jets.

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: cc7360922d1d1e2994248e8345a3a6902b2359a9bd3bfa2c1c1893016b25446b

High-order regularized descent with full parameter dependence

### Native proof: HO_ENDPOINTS

Native pointer: /proofs/3; canonical SHA-256: b4cae642401d5d94cdce40203762dbe2dcc36171225cbeaa38b31ba59414bf25

#### Native field: algorithm_scope

Native pointer: /proofs/3/algorithm_scope; canonical SHA-256: 27db664d8739f6b71895cf9307c2fa51fca46dfdb4289ac2f8415d525f164282

Applies only to the indicated objective-gap, first-order, or spectral second-order criteria. A true minimizer need not satisfy a finite-radius high-order Taylor-decrease criterion; those criteria require their own argument. Public-domain, curvature, and accuracy conditions remain those of the linked bound.

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: b8837d30d87467eb5722fd001e1a97c4b20caf0f43e28cf131ec6217446632ed

For a full-space differentiable objective with $f(x_0)-\inf f\le\Delta$, the condition $\Delta=0$ makes $x_0$ a global minimizer. Its gradient is zero, and its Hessian is positive semidefinite whenever it exists. Thus first-order and spectral second-order stationarity require no query. An objective-gap target also requires no query when $\varepsilon_f\ge\Delta$. Nonnegative query cost proves exact optimality of these zero bounds.

If a public gradient-Lipschitz bound $\beta$ is part of the specification, the descent lemma gives $\|\nabla f(x_0)\|^2\le2\beta\Delta$. For convex full-space objectives with a minimizer within distance $R$, it also gives $f(x_0)-f^*\le\beta R^2/2$ and $\|\nabla f(x_0)\|\le\beta R$. These sufficient zero-query regions require that explicit first-order regularity assumption. If only the highest derivative is controlled, positive quadratics can have arbitrary curvature and arbitrarily large initial gap despite zero highest-order modulus.

On a connected Euclidean domain, $M_k=0$ or $M_{k,\nu}=0$ makes $D^kf$ constant, so $f$ is a polynomial of degree at most $k$. One complete jet determines all coefficients. Under the specified free internal computation, a known polynomial can then be optimized on a compact public domain, or combined with a public regularizer and solved through the declared known-model interface.

A bounded-below polynomial on the full space need not attain its infimum. For approximate spectral stationarity, shift $x_0$ to zero and minimize $f(x)+\eta\|x\|^2/2$. This function is coercive, and its minimizer $x_\eta$ satisfies $\eta\|x_\eta\|^2/2\le\Delta$, $\|\nabla f(x_\eta)\|\le\sqrt{2\eta\Delta}$, and $\nabla^2f(x_\eta)\succeq-\eta I$. Choosing $\eta\le\min\{\varepsilon_H,\varepsilon_g^2/(2\Delta)\}$ meets both targets. For global objective accuracy, exact polynomial coefficients permit arbitrary-accuracy internal global optimization; no additional unknown-function query is needed.

To exclude zero queries in a nontrivial region, choose two positive quadratics centered on opposite sides of $x_0$, with the same public budgets and disjoint acceptable-output sets. A zero-query algorithm has the same output distribution on both instances, so their success probabilities sum to at most one. It cannot succeed with probability at least $2/3$ on each. With only highest-order regularity, curvature can be increased until the acceptable sets are disjoint at any prescribed positive accuracy and positive localization radius. In an initial-gap model with additional curvature restrictions, retain the bound's explicit accuracy and compatibility window.

If both a global PL constant $\mu$ and a gradient-Lipschitz upper bound $\beta$ are supplied, then $2\mu(f-f_*)\le\|\nabla f\|^2\le2\beta(f-f_*)$. When $\mu>\beta>0$, every gap is zero and the class contains only constant objectives. This degeneracy does not apply without the extra $\beta$ assumption.

#### Native field: limitations

Native pointer: /proofs/3/limitations; canonical SHA-256: 918705965626e3df518889587e400c0256e29c0f4de1cd53ae94b6c6343683b9

The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: 27db664d8739f6b71895cf9307c2fa51fca46dfdb4289ac2f8415d525f164282

Applies only to the indicated objective-gap, first-order, or spectral second-order criteria. A true minimizer need not satisfy a finite-radius high-order Taylor-decrease criterion; those criteria require their own argument. Public-domain, curvature, and accuracy conditions remain those of the linked bound.

#### Native field: statement

Native pointer: /proofs/3/statement; canonical SHA-256: d4c17587463f6cf74fa2d09f365b89376efcf35723b4f888b5f6d669473ecfbc

Zero-query guarantees follow from a public initial-error bound. A zero highest-order regularity modulus permits exact polynomial recovery from one complete jet.

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: 4e8cc661512a877d5023d683fef209a064798f2e93b413a01bdea7d1779a245f

Zero-query and polynomial-recovery endpoints

### Native proof: HO_POLYNOMIAL_ONE_CALL

Native pointer: /proofs/4; canonical SHA-256: c1446b3727ae87e61d4a965286c7c536713ecf4f986bf738ecec8d27dcd5b9d4

#### Native field: algorithm_scope

Native pointer: /proofs/4/algorithm_scope; canonical SHA-256: 1baf875e61a3dbe3fb6e46ad648d9a5ae97ad82a0326ed0cb4ae91646b11a0c8

Unrestricted measurable adaptive deterministic or randomized algorithms; randomized success at least 2/3; fixed-path cap.

#### Native field: baseline_refs

Native pointer: /proofs/4/baseline_refs; canonical SHA-256: b0cfca23e61c4f54378ec4c5e9049e715994296a15165a9bcaf3f3e035ac084c

#### Native item 1

Native pointer: /proofs/4/baseline_refs/0; canonical SHA-256: 3bbc0ffe4e35b62e32eabf2963be0181ad39163f22126aca50bf059ba3ba4ce3

#### Native field: pointer

Native pointer: /proofs/4/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/4/baseline_refs/0/sha256; canonical SHA-256: 50a7ace1a76af1554f112805e05c23ed42246b057e5187a963f4bcfceecef8e7

c6cf8951aaa936a2621655d11aa144eff0be620532919f688a364a7125e98013

#### Native item 2

Native pointer: /proofs/4/baseline_refs/1; canonical SHA-256: 81c4c2d2fe46a20f37dd09770b2bb9fbd10a96f6c34800872357b938ec8fab0b

#### Native field: pointer

Native pointer: /proofs/4/baseline_refs/1/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/4/baseline_refs/1/sha256; canonical SHA-256: c32c979f8c7272f1a639c8f422c42ebefe915a092e9eccbc21bb71f855af1d21

cbc6033972fcce80bd2790880bc9123e4a6f7a7e84ddf5f48f17e2720bdd7bcf

#### Native item 3

Native pointer: /proofs/4/baseline_refs/2; canonical SHA-256: ec3e960e1632677edbbb973f26e67dca0703fd971fe84492486ddf5aafe20c54

#### Native field: pointer

Native pointer: /proofs/4/baseline_refs/2/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/4/baseline_refs/2/sha256; canonical SHA-256: 7cba023d2f38bc2921e331e18d9ee1427f5301e7609ece886adbee7e4ad21d67

787f517b00959c64e9f2b224b88803b8f6b26576bd53d050bfc65c112157e89b

#### Native item 4

Native pointer: /proofs/4/baseline_refs/3; canonical SHA-256: f174d5ca913d7cd11d5b01ec2dec4a9d11a72d342eb26420eea63381a0681a4c

#### Native field: pointer

Native pointer: /proofs/4/baseline_refs/3/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/4/baseline_refs/3/sha256; canonical SHA-256: 7a5a8dfd3fd4dae87664c36bb3fbd71eab64039323c869d1a8fa46a6199f4a8b

88682c58ad92dcce6485cfd9c88345d8fa6d5545531b1f58deaff9088a2796d6

#### Native item 5

Native pointer: /proofs/4/baseline_refs/4; canonical SHA-256: fc193189a4201ef373fe595ac73c98753eaa8033985efaf858e4855f2f806025

#### Native field: pointer

Native pointer: /proofs/4/baseline_refs/4/pointer; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: sha256

Native pointer: /proofs/4/baseline_refs/4/sha256; canonical SHA-256: f1536d6967c39040908819e7719f6a272fcf42ea54056e4c1cdc262cd0882d0a

b3ce4f66b7d99a49acc47a176beee150070235d368270fae67dfe6871c4f3829

#### Native item 6

Native pointer: /proofs/4/baseline_refs/5; canonical SHA-256: 178741841cef3e8956d3f3f60a6e10eaeb8693e68f61cfea54b42a5b5e792619

#### Native field: pointer

Native pointer: /proofs/4/baseline_refs/5/pointer; canonical SHA-256: 4730c807a4749b5c80e0e1ff5fe96de66e96934baf3d92654507d220f152751c

/proofs/3

#### Native field: sha256

Native pointer: /proofs/4/baseline_refs/5/sha256; canonical SHA-256: ab8d95c7d2c065980af13035e6550456210aff376ed24ebe37f6e3533fcdf820

b4cae642401d5d94cdce40203762dbe2dcc36171225cbeaa38b31ba59414bf25

#### Native field: body

Native pointer: /proofs/4/body; canonical SHA-256: c468f489d8a18730cc60d9ab76ba6e3989730b76851602ec483aef92c4068cc5

Retain the frozen full-space C^k, bounded-below objective, gap, jet, output and free-known-model contracts and HO_ENDPOINTS. M_k=0 makes D^k f constant, so the Taylor polynomial of degree at most k recovered from J_k f(x0) equals f everywhere. After this single query set eta=min(epsilon_H,epsilon_g^2/(2Delta))>0 and globally minimize the known coercive polynomial f(x)+eta||x-x0||^2/2 using the permitted free model solution. At a minimizer y, eta||y-x0||^2/2<=f(x0)-inf f<=Delta; therefore ||grad f(y)||=eta||y-x0||<=sqrt(2eta Delta)<=epsilon_g and Hess f(y)>=-eta I>=-epsilon_H I. No further oracle check is required and y may be unqueried. This does not assume that f attains its own infimum. For the lower bound fix lambda>epsilon_g^2/(2Delta), a=sqrt(2Delta/lambda), and f_+(x)=lambda||x-x0-a e1||^2/2, f_-(x)=lambda||x-x0+a e1||^2/2. Both have gap Delta and Lipschitz D^k modulus zero for every k>=2. Their Hessians are positive definite; their acceptable outputs are disjoint balls of radius epsilon_g/lambda because a>epsilon_g/lambda. A zero-query output law is the same on both instances, so its two success probabilities sum to at most one. It cannot give probability >=2/3 on each; the deterministic case follows as well. Integer query counts give cost>=1. Thus the upper and lower costs are exactly one, uniformly in dimension and both tolerances. At Delta=0 the retained zero-query branch applies instead.

#### Native field: limitations

Native pointer: /proofs/4/limitations; canonical SHA-256: 68e89a3fe8990bde7b861ab66b56bed884be2f3e2e21c40d8b9ab48d2b6507a4

Only M_k=0 and Delta>0. No inference to small positive M_k.

#### Native field: scope

Native pointer: /proofs/4/scope; canonical SHA-256: fb4de890e92bf9a6471ed92283e235879fd1c7ded036d213ef261a134dbc3efc

Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

#### Native field: source_refs

Native pointer: /proofs/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: statement

Native pointer: /proofs/4/statement; canonical SHA-256: 81dddeb7d46b6a06afc79105a92d4a4be8ea57cc12311e6753b994827ffb81fc

For Delta>0 and M_k=0, each registered algorithm view has exact minimax jet cost one.

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: 9b2101f8cb23ba68be10703c6e492d2a28a12ae669cdde06ead5a3b58a95a385

Exact one-jet polynomial branch

### Native proof: HO_RANDOMIZED_GRADIENT_TRANSFER

Native pointer: /proofs/5; canonical SHA-256: 166cce2c666bbd8247f1911b82d86ae07249c2d157d3700d5d3d0660070336e2

#### Native field: algorithm_scope

Native pointer: /proofs/5/algorithm_scope; canonical SHA-256: dcb31cfc8fb813e0a03dc0841d896a0f45aa84e7312dfb6662296e87aef9d8ab

Arbitrary randomized adaptive algorithms with private randomness, arbitrary query points and unqueried outputs.

#### Native field: body

Native pointer: /proofs/5/body; canonical SHA-256: bf06092984d730b5ba831094724d3e45d3cc70f1440f410c924483c91663ebae

Read arXiv:2609.28202v2, Definition 3.1 and Theorems 3.2 and 3.4, PDF pp.5-6, archived characters 13323-16400, source SHA256 5129c1f6b8ae94f321c0541890578a5ef396ec08583340160ed877699bae11f9. Set n=1, p=k, L_p=M_k, epsilon=epsilon_g. Then the complete component p-jet is precisely one target complete jet and S_p=1+A. The source class is bounded below with initial gap at most Delta and Lipschitz D^k bound M_k, with no lower-order regularity budget. Any algorithm meeting the target simultaneous gradient/Hessian condition with probability at least 2/3 also meets its gradient condition with that probability, for every positive epsilon_H. The source lower bound is therefore necessary for the target. Theorem 3.4 supplies hard dimension at most C_k(1+A)log(3+A); choose the k-only source constant sufficiently large. For an ambient dimension above this value, pad a hard function h(z) by f(z,w)=h(z). Projection of every query gives an exact equal-cost source query; all derivatives involving dummy coordinates vanish and the remaining complete jet agrees with h. Project the arbitrary output as well. Gap, lower boundedness, tensor operator Lipschitz bound, fixed-path cost and success probability are preserved. Hence an ambient target algorithm below c_k(1+A) would contradict the source theorem. We adopt the conservative A>=C_k subregion. No relation between B and A is used. This is a new q2 bound, not a relabeling or merger of the old q1 bound.

#### Native field: limitations

Native pointer: /proofs/5/limitations; canonical SHA-256: 648567ea591cbbeb4fbfb82abb3e8d26c610cfaae4473c9998b5d6e1dccf7c89

The dimension and workload thresholds are sufficient source applicability guards with unspecified k-only constants, not intrinsic transitions. No curvature-order lower bound is obtained.

#### Native field: scope

Native pointer: /proofs/5/scope; canonical SHA-256: bd6037b58d6164df5366bd8308c7f04bc5fbb84f9ffc5a475050fb5f5a93a081

Delta>0, M_k>0, A>=C_k, d>=C_k(1+A)log(3+A)

#### Native field: source_hashes

Native pointer: /proofs/5/source_hashes; canonical SHA-256: 1bfd46dccd094289d527666221c2700cf63dfa874989b0eea2a933c2346965a0

#### Native item 1

Native pointer: /proofs/5/source_hashes/0; canonical SHA-256: 5703803334d8c37d66cce664e9ae853392e8c79fa267a922897d67039f7d054e

5129c1f6b8ae94f321c0541890578a5ef396ec08583340160ed877699bae11f9

#### Native field: source_refs

Native pointer: /proofs/5/source_refs; canonical SHA-256: dc5d469fadf73e33fd68f2487cb4b113858021a2860465254054003c8ee1b39d

#### Native item 1

Native pointer: /proofs/5/source_refs/0; canonical SHA-256: 6a3493c431ca82e403f1a150922292adb3e5dcfbadc754d48d4009587db48498

SO_SRC_dbd0fbd46018f76e

#### Native field: statement

Native pointer: /proofs/5/statement; canonical SHA-256: 54d364f73055b5063b739ba594ff0146f6f00a756ee05f53d35bae957c5f4154

On Delta>0, M_k>0, A>=C_k, d>=C_k(1+A)log(3+A), randomized q2 costs at least c_k(1+A), independently of epsilon_H.

#### Native field: title

Native pointer: /proofs/5/title; canonical SHA-256: 385a7f16abe7d71de1b722f59da815844bc9572eee8e8ef7a9f3d26dcbd0133e

One-component gradient lower bound for the randomized second-order target

### Native proof: HO_GUARDED_ENVELOPE

Native pointer: /proofs/6; canonical SHA-256: 315bb1ccc5c284610a58deebbf63acafc566f2b42667909e2bcd27c10fd2c38c

#### Native field: algorithm_scope

Native pointer: /proofs/6/algorithm_scope; canonical SHA-256: 24c127ba9ba3bd163ab9d0f90a2697853179fdca0ec8e60dca7430cc8e73ef57

Exactly the frozen deterministic q1, g1 and resource contract.

#### Native field: baseline_refs

Native pointer: /proofs/6/baseline_refs; canonical SHA-256: c0b52098154ca9e41cfd9ce78a6b031cc51eae8920c5f8559653ce5420d8b9e1

#### Native item 1

Native pointer: /proofs/6/baseline_refs/0; canonical SHA-256: 23581e209f60a5c7631efc5061657170d32a69777d13ea424d009610efbb267d

#### Native field: pointer

Native pointer: /proofs/6/baseline_refs/0/pointer; canonical SHA-256: ec44798dd503dcc20291e10e4c07830bfbd41d1832a737884bbf882260330bf4

/bounds/5

#### Native field: sha256

Native pointer: /proofs/6/baseline_refs/0/sha256; canonical SHA-256: 3280fb87998235add4359606c60f33a54538672777fc1e1c5c48a226f89f9a8c

1044fb91b7779e63a7c57c7a6e236e771328f54c21def18a4c860757cdcd135f

#### Native item 2

Native pointer: /proofs/6/baseline_refs/1; canonical SHA-256: 21776a709b1b6d6133f07166acd637efb6be8168429686c6e38ea93920efd630

#### Native field: pointer

Native pointer: /proofs/6/baseline_refs/1/pointer; canonical SHA-256: 710d9e6bcc130379a8bad365103ceedd68708a0b078f97fda36e184171d24280

/comparisons

#### Native field: sha256

Native pointer: /proofs/6/baseline_refs/1/sha256; canonical SHA-256: 594b31d3ed54b22fc3ec3fee32ee0de9de63b3a0b581a55778dbc8624514adf0

0dc90dc974e3c5a6eda5e1b882c1b501432e46ccb624c9d115712bc4048fe280

#### Native field: body

Native pointer: /proofs/6/body; canonical SHA-256: 6babd0aef494ddb72d3be8e2495d3174c52b487c3cb95c5c0b0bb2010b7bc574

Condition on the unchanged frozen b6 claim at /bounds/5, hash 1044fb91b7779e63a7c57c7a6e236e771328f54c21def18a4c860757cdcd135f, and its retained dependencies; this is not fresh certification of those dependencies. If theta belongs to an existing comparison and to r3, the same target minimax quantity obeys b6 at theta. Thus the lower envelope for c4 includes c_k(A+B) guarded by r3, and the c3 lower envelope includes the same term guarded by r3 intersect r4. Upper b1 remains C_k(1+A+B). On r3, max(A,B)>=C_k>0, so 1+A+B=O_k(A+B), and the bracket is tight up to k-only constants. No lower inequality is extended outside r3. This adds explicit overlap bookkeeping; c1 already recorded this rate, so no new global rate improvement is claimed.

#### Native field: scope

Native pointer: /proofs/6/scope; canonical SHA-256: 8617ad41723577bf854b67a091cc988e0c2a4f20f9f7a266596f70fc2d73ad02

Delta>0, M_k>0, max(A,B)>=C_k, d>=C_k(1+A+B)

#### Native field: source_refs

Native pointer: /proofs/6/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: statement

Native pointer: /proofs/6/statement; canonical SHA-256: b09a34fe275bdee3757ebfe9ef6c6c43c8248648b811c2f88f2c38076d64d569

Retained deterministic b6 contributes on its intersection with c3 and c4.

#### Native field: title

Native pointer: /proofs/6/title; canonical SHA-256: ebde6841239183292bb57ce5b510eafb4dc56569be1e69f9f4549fe5927876d7

Guarded reuse of the retained deterministic bracket

### Native proof: HO_RANDOMIZED_Q2_J_NATIVE_CLOSURE_20261116

Native pointer: /proofs/7; canonical SHA-256: 947665f7ccffe3eebb2c1667f61b45da0244c499242581fa9073f5957d3c0de9

#### Native field: baseline_refs

Native pointer: /proofs/7/baseline_refs; canonical SHA-256: bdbb7104d053a201567ff9744d7b4c92877ff43ee669dcbd373cd7caf6edfca8

#### Native item 1

Native pointer: /proofs/7/baseline_refs/0; canonical SHA-256: 3bbc0ffe4e35b62e32eabf2963be0181ad39163f22126aca50bf059ba3ba4ce3

#### Native field: pointer

Native pointer: /proofs/7/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/7/baseline_refs/0/sha256; canonical SHA-256: 50a7ace1a76af1554f112805e05c23ed42246b057e5187a963f4bcfceecef8e7

c6cf8951aaa936a2621655d11aa144eff0be620532919f688a364a7125e98013

#### Native item 2

Native pointer: /proofs/7/baseline_refs/1; canonical SHA-256: ec3e960e1632677edbbb973f26e67dca0703fd971fe84492486ddf5aafe20c54

#### Native field: pointer

Native pointer: /proofs/7/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/7/baseline_refs/1/sha256; canonical SHA-256: 7cba023d2f38bc2921e331e18d9ee1427f5301e7609ece886adbee7e4ad21d67

787f517b00959c64e9f2b224b88803b8f6b26576bd53d050bfc65c112157e89b

#### Native item 3

Native pointer: /proofs/7/baseline_refs/2; canonical SHA-256: 81c4c2d2fe46a20f37dd09770b2bb9fbd10a96f6c34800872357b938ec8fab0b

#### Native field: pointer

Native pointer: /proofs/7/baseline_refs/2/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/7/baseline_refs/2/sha256; canonical SHA-256: c32c979f8c7272f1a639c8f422c42ebefe915a092e9eccbc21bb71f855af1d21

cbc6033972fcce80bd2790880bc9123e4a6f7a7e84ddf5f48f17e2720bdd7bcf

#### Native item 4

Native pointer: /proofs/7/baseline_refs/3; canonical SHA-256: f174d5ca913d7cd11d5b01ec2dec4a9d11a72d342eb26420eea63381a0681a4c

#### Native field: pointer

Native pointer: /proofs/7/baseline_refs/3/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/7/baseline_refs/3/sha256; canonical SHA-256: 7a5a8dfd3fd4dae87664c36bb3fbd71eab64039323c869d1a8fa46a6199f4a8b

88682c58ad92dcce6485cfd9c88345d8fa6d5545531b1f58deaff9088a2796d6

#### Native item 5

Native pointer: /proofs/7/baseline_refs/4; canonical SHA-256: 0f5bc81e3a3f536595e4d73a5240fc35e80e6bbe28285817ac106de2429eb171

#### Native field: pointer

Native pointer: /proofs/7/baseline_refs/4/pointer; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: sha256

Native pointer: /proofs/7/baseline_refs/4/sha256; canonical SHA-256: d0c06e1a7e06ab333717e84b46c79cf9fdbbdaf71e8b8733f8369793e7e02430

359e9b8333d4f602a2138a3091bcf33c82eb14d756c431b4b9f4d0166ab3d626

#### Native item 6

Native pointer: /proofs/7/baseline_refs/5; canonical SHA-256: 8014795c3533db2163036bb34e6a45ae5b2ee39696038d177642958d08664e0c

#### Native field: pointer

Native pointer: /proofs/7/baseline_refs/5/pointer; canonical SHA-256: 75e7040ee9b7f6bb53623ed289617ff0705a4d81718776cbba42cdc3e6039b04

/bounds

#### Native field: sha256

Native pointer: /proofs/7/baseline_refs/5/sha256; canonical SHA-256: 73820571080a805fec2272e7cedc94d071ca231e55366de35ad82de4698170db

56b7e0375a1bad90d245887bf327c96e503e1fd25f547cd379c8fdfbfbc21501

#### Native item 7

Native pointer: /proofs/7/baseline_refs/6; canonical SHA-256: 21776a709b1b6d6133f07166acd637efb6be8168429686c6e38ea93920efd630

#### Native field: pointer

Native pointer: /proofs/7/baseline_refs/6/pointer; canonical SHA-256: 710d9e6bcc130379a8bad365103ceedd68708a0b078f97fda36e184171d24280

/comparisons

#### Native field: sha256

Native pointer: /proofs/7/baseline_refs/6/sha256; canonical SHA-256: 594b31d3ed54b22fc3ec3fee32ee0de9de63b3a0b581a55778dbc8624514adf0

0dc90dc974e3c5a6eda5e1b882c1b501432e46ccb624c9d115712bc4048fe280

#### Native item 8

Native pointer: /proofs/7/baseline_refs/7; canonical SHA-256: 860579aa09985a08ba932fa6b7edd0931312248cb45a08670b09134bfa503378

#### Native field: pointer

Native pointer: /proofs/7/baseline_refs/7/pointer; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: sha256

Native pointer: /proofs/7/baseline_refs/7/sha256; canonical SHA-256: 40cfcb8c8ead6539601ba984e12a723d242126b681c1102fc41cec2724841619

aac46b80c92d8996e17bae2a83c298ae54be29ab8212efb23152d7a3d47d21db

#### Native item 9

Native pointer: /proofs/7/baseline_refs/8; canonical SHA-256: 77a0d4b7a029aaacec56995d61c885b8a54e18a27cb17325fba9b180df0d7648

#### Native field: pointer

Native pointer: /proofs/7/baseline_refs/8/pointer; canonical SHA-256: b5a3c8e5a69ebbfa3a635cdb498215b14ffa316a5c88100937281d883417d1bf

/proofs

#### Native field: sha256

Native pointer: /proofs/7/baseline_refs/8/sha256; canonical SHA-256: 9161b47c9c8ae8c42ac1862b4c141084eb16b90f2d4d29ef8a401ec7c3008503

f2828f1ec7fed912f704424ab685403cc8c0f165c70031c7f2bbebc51eede332

#### Native field: body

Native pointer: /proofs/7/body; canonical SHA-256: cd6be459c95a7cb052c0e6513e22d459259cb21cc81482807bce2577baff285e

This proof is specifically for the unchanged randomized q2/g1 complete-k-jet scalar-cost contract. Retain the exact existing b1 upper C_k(1+A+B): its quantity_refs explicitly include q2 and it was already adopted in q2 c2/c4. Thus it is an upper for one actual complete algorithm controlling BOTH gradient and Hessian at the SAME output, not an upper obtained by merging q1 and q2 labels or combining algorithms. All initialization, next-point checks and actual full-jet responses are included in its original fixed-path cap; global known-model computations remain free only as allowed by the unchanged model. The independent source-based b5 lower is already a native q2 statement. HO_RANDOMIZED_GRADIENT_TRANSFER uses source Definition3.1/Theorems3.2/3.4 with n1,p=k,Lp=M_k,epsilon=epsilon_g: an algorithm meeting simultaneous gradient/Hessian accuracy with probability>=2/3 necessarily meets gradient accuracy with that probability, for everyepsilon_H>0. The source hard class obeys the same bounded-below initialgap and Lipschitz D^k budget, without adding lower-order regularity. For its harddimension d0<=C_k(1+A)log(3+A), pad h by f(z,w)=h(z). Each arbitrary adaptive target query projects to exactly one source completejet query; dummy derivatives vanish, the remaining tensors agree, and their operator-norm Lipschitz bound and initialgap are unchanged. Project the final arbitrary/unqueried output; targetsuccess implies sourcegradient success. Private randomness, fixedpathcap and per-instance successquantifier are preserved, so every targetalgorithm has cap>=c_k(1+A) on G={Delta>0,M_k>0,A>=C_k,d>=C_k(1+A)log(3+A)}. This is the recorded conservative source guard, including all k-only workload/dimension constants; no lower beyond G is adopted. Now restrict to J=G intersect{B<=C0*A}, with fixed k>=2 and a fixed finite public window constant C0>0 chosen independently of the five native joint parameters. Since 1+A+B<=1+(1+C0)A<=(1+C0)(1+A), the exact q2 envelope obeys c_k(1+A)<=q2*<=C_k(1+C0)(1+A). Hence Theta_{k,C0}(1+A) on J, with a constant ratio independent of d,Delta,M_k,epsilon_g,epsilon_H. C0 is solely a comparison-window constant: it is not an objective smoothness budget, is not substituted by the varying valueB/A, and its dependence is explicitly declared at this comparison. q2's global quantity metadata remains unchanged; this regional result does not assert globally uniform C0-independent optimality. Both B=C0*A and A=C_k are included subject to the sufficiently-large sourceconstant. Positive Delta,M_k and sufficientdimension remain mandatory; zero-gap and polynomial branches are separate. Outside J, especially when B/A grows or outside G, the old q2 comparisons remain unclosed. The old optimal q1 c1 is a distinct registered quantity and is not the publication certificate for q2. This is native publication of the matching consequence already stated in F_RANDOMIZED_GRADIENT and the old boundary ledger, not a new paper lower bound, a new algorithm, or a new blind discovery. No fresh source verification or prior read/approval credit is claimed by this curator proof.

#### Native field: proof_refs

Native pointer: /proofs/7/proof_refs; canonical SHA-256: 8e47a3ee60869f18447621d8dccf7f5d793f180b25199fddd4f17f98d5168f03

#### Native item 1

Native pointer: /proofs/7/proof_refs/0; canonical SHA-256: 870e4304ff412f84a5969428876cde72a3db0d2b5cc7e6c090fbddd18d7e6899

HO_RANDOMIZED_GRADIENT_TRANSFER

#### Native field: scope

Native pointer: /proofs/7/scope; canonical SHA-256: 4103f36e21b1b8026e4b7ae141fbbe0ca2af6c316e946266c92208768946892d

Randomized q2/g1, fixed k>=2 and fixed0<C0<infinity; exact J=G intersect{B<=C0A}.

#### Native field: source_refs

Native pointer: /proofs/7/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/7/title; canonical SHA-256: 1e0cd4bea6d15ad0a3c3e0b3e50a3d6c562a0651e4ec2367acb942195cfd7060

Independent native randomized q2 closure on fixed-ratio window J

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: dfc7a8998a85f29c4059e725c47827ba430c9464650554d1a0c8b3c430a8e5f8

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: b2da0f5c6846e0079294a2b8fb78349da24c7f0194d57087bd68cb4cebda7a10

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 6e2de994f684b4bb1d6604689a19ffe7162901d2a773cd3f860cbb8fc3da561a

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 84dea4d699d3e7af852c43583724075f699ef1593cd29309bc2938d6572b6c62

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: f176c1a2304341c0d1e4da7bdd008ef9a49439b5177763da7193c33b38b96cc4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 61d6cc34a43b958ddf1fa9198bda41fd2e5da92991db3bb8e8c76f8f93f370b7

SO_HO_HON05_S__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 57487e702a5b9f463aad24c3d7be279c072c2c3f2264d48780b63c4c3b01902d

Conditional unchanged bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 92ef6d8f3c446da68342ff35f8a8b464a9f08c7f6ad21213b545d71ee2b99a7e

Delta>0,M_k>0

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 23e3814f756961fa25b2c5003198a61a54613a99a23bac41ad6496fed0e17332

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 2a2d9c487891eba39d70b19edc7e8d4c537efab3c2d5ea13dd918262cbf29dfe

SO_HO_HON05_S__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: a6b4d81ffeb8e294ee6b438d3ebbf682127a683cebcf1ec3d36448a856eee299

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: f7764d9594dd85e3608e7e028148634ddfb6cc925dd5bfec541d401df669b2cb

SO_HO_HON05_S__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: dda3ad7e6a03ec35d1b26e00cacdc7c42bd268a265b051ca4963360bebf22ea8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: e8d9ca523da3f6a06ce6e10fc38204ef187ffd3da8bbc9910b629c006169b7ca

comparison intersect H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: ff156402cf7bd52cad944cc034dc4666caa99ec0ed606016b2ecdd5f2454dc06

SO_HO_HON05_S__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 29d0d284a61b25c383f5e97312e3b0528a7774000cc626073f30600cf6fedec1

Retained lower, with its guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: f3fef0c598f9ab2c4000597d8967a68dca7b43fca735f06eb50c576b2d8af831

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: fe7c7024f45b198e26447fc97d7ba7895ce8f92b9706eaf81f35e93a2c05968b

SO_HO_HON05_S__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/bound_uses/5; canonical SHA-256: fd3b9bee1a9e9b880d87c2173f28b9115fd557eab9be33d27238338980148ab3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/bound_id; canonical SHA-256: e9f21132ad11087e56e3dea5c81bac0db9ed0c6b83d3dd4076fc7e5b59dcc658

SO_HO_HON05_S__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 545d141fb6210cca4db0b227396e24eccab589a5a4068c8922782c70935baa92

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 7a46c6e2d2d69f6377b7f5618acfc5aaae05aa6d6395329a9e99edf176ec90a4

H is source applicability, not an intrinsic dimension transition.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 3d71fa1e2e95f41b5cf97fac21fe2ce670ac2bfaf0b9af6a863458122e39af11

On H, 1+A+B=O_k(A+B).

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 8da9c6ee496e95be1af049c18aa626531b77fd32e7d6918ba1aba715c6b8d669

Zero-gap and zero-modulus endpoints handled separately.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: c2f5222d01fbf4b50bc53c71137107c76c3c7321cf350dbc2e4a0925f173568c

Theta_k(1) on H; unavailable outside H

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 69aad35933fa7542eb33c4c2212627ed3cc1e45f6feb60f3ead72724009f1d0d

Omega_k(A+B) throughout c1

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 568f4b044936b272b98aa15bd22290b82f6f4fcce1874eef7008b3df1eb83a42

No rate gap under conditional retention.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 6c55cb498eaace2dc5fc77f239ae0760578a98d5cdc229f35d76f5bb73281865

O_k(1+A+B)

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 2cdabc4fdb4f8d625187d2e6e5b24cbbf4ae8ef3b1d4cfd53b0aeeb1e13001e3

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 7e46b4994c0a8be7bbed5564a17ae6a15702894a0c7c86983206d2db7d8b637a

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: fcc880e8cae8fd95ed18bbdae1bb66006e8db1909e3e0b016832ab492bfc23d5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 61d6cc34a43b958ddf1fa9198bda41fd2e5da92991db3bb8e8c76f8f93f370b7

SO_HO_HON05_S__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 92ef6d8f3c446da68342ff35f8a8b464a9f08c7f6ad21213b545d71ee2b99a7e

Delta>0,M_k>0

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: c3f1434f11854f2238eb62c9f1e1bd6291711c88cdc376419813d38e16829e28

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 2a2d9c487891eba39d70b19edc7e8d4c537efab3c2d5ea13dd918262cbf29dfe

SO_HO_HON05_S__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 57487e702a5b9f463aad24c3d7be279c072c2c3f2264d48780b63c4c3b01902d

Conditional unchanged bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: a7ded34d7abdbdfa4fc0fcd02c8d3dbd9ef923a8bb37e1cec0eb339452c00359

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: f7764d9594dd85e3608e7e028148634ddfb6cc925dd5bfec541d401df669b2cb

SO_HO_HON05_S__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 57487e702a5b9f463aad24c3d7be279c072c2c3f2264d48780b63c4c3b01902d

Conditional unchanged bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: ddea295858a3eacb41372613f154754509a24dbbbd0b3b66ad3ceddf0e378a0a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: ff156402cf7bd52cad944cc034dc4666caa99ec0ed606016b2ecdd5f2454dc06

SO_HO_HON05_S__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: f3fef0c598f9ab2c4000597d8967a68dca7b43fca735f06eb50c576b2d8af831

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: fe7c7024f45b198e26447fc97d7ba7895ce8f92b9706eaf81f35e93a2c05968b

SO_HO_HON05_S__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/bound_uses/5; canonical SHA-256: fd3b9bee1a9e9b880d87c2173f28b9115fd557eab9be33d27238338980148ab3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/bound_id; canonical SHA-256: e9f21132ad11087e56e3dea5c81bac0db9ed0c6b83d3dd4076fc7e5b59dcc658

SO_HO_HON05_S__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: ac19e821af5c79eccd15ddd53970649e729a0bef6355342481efe4b7a9fa2b60

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 7743fb77b40085bcf3bcd2c4bb8c69fab247537515555f147ae8e319cacb599e

Delta=0 includes M_k=0.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 17bd2b03af8aaf409327ca267e43a321031d93862c071f4b23f121c2246bcf09

Inapplicable ratio: exact zero cost.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: efe12abd516569f289ea53fe9f2d0c8d7b9513a8249725b9dc831156383ae6a6

None within this branch.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 0f4bf6490ea6934b18cb5c37c5e0f4eced728b6a16bc1c7741165e777b20ebe2

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 59ed1132e2d9048e4105f90a1b7efe476a8f70435f714e4753ecda9f549a46c1

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: f176c1a2304341c0d1e4da7bdd008ef9a49439b5177763da7193c33b38b96cc4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: 61d6cc34a43b958ddf1fa9198bda41fd2e5da92991db3bb8e8c76f8f93f370b7

SO_HO_HON05_S__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 57487e702a5b9f463aad24c3d7be279c072c2c3f2264d48780b63c4c3b01902d

Conditional unchanged bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 92ef6d8f3c446da68342ff35f8a8b464a9f08c7f6ad21213b545d71ee2b99a7e

Delta>0,M_k>0

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 23e3814f756961fa25b2c5003198a61a54613a99a23bac41ad6496fed0e17332

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 2a2d9c487891eba39d70b19edc7e8d4c537efab3c2d5ea13dd918262cbf29dfe

SO_HO_HON05_S__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: a6b4d81ffeb8e294ee6b438d3ebbf682127a683cebcf1ec3d36448a856eee299

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: f7764d9594dd85e3608e7e028148634ddfb6cc925dd5bfec541d401df669b2cb

SO_HO_HON05_S__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: deaee5515e44f685a27cd67ba6b71cd59485a8222014a722c918bec2ab96ef78

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: e8d9ca523da3f6a06ce6e10fc38204ef187ffd3da8bbc9910b629c006169b7ca

comparison intersect H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: ff156402cf7bd52cad944cc034dc4666caa99ec0ed606016b2ecdd5f2454dc06

SO_HO_HON05_S__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 82a44e60460a701ca888c1881fe4c80c2dc2f6e671573137aecfba5da987ef47

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 73b4b43ffce5977ca7f83f6bbc55284b3cc3bc822ca8a821063dcc21f2ab0953

HO_GUARDED_ENVELOPE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 29d0d284a61b25c383f5e97312e3b0528a7774000cc626073f30600cf6fedec1

Retained lower, with its guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: f3fef0c598f9ab2c4000597d8967a68dca7b43fca735f06eb50c576b2d8af831

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: fe7c7024f45b198e26447fc97d7ba7895ce8f92b9706eaf81f35e93a2c05968b

SO_HO_HON05_S__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native item 6

Native pointer: /joint_analysis/comparisons/2/bound_uses/5; canonical SHA-256: fd3b9bee1a9e9b880d87c2173f28b9115fd557eab9be33d27238338980148ab3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/bound_id; canonical SHA-256: e9f21132ad11087e56e3dea5c81bac0db9ed0c6b83d3dd4076fc7e5b59dcc658

SO_HO_HON05_S__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 545d141fb6210cca4db0b227396e24eccab589a5a4068c8922782c70935baa92

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: 7a46c6e2d2d69f6377b7f5618acfc5aaae05aa6d6395329a9e99edf176ec90a4

H is source applicability, not an intrinsic dimension transition.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: 3d71fa1e2e95f41b5cf97fac21fe2ce670ac2bfaf0b9af6a863458122e39af11

On H, 1+A+B=O_k(A+B).

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/boundary_checks/2; canonical SHA-256: 8da9c6ee496e95be1af049c18aa626531b77fd32e7d6918ba1aba715c6b8d669

Zero-gap and zero-modulus endpoints handled separately.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 2f23be3f3509558fb70a62770f6637f34fbdd0cda81bad4943db8bac38d5d46e

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/fixed_parameters/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/fixed_parameters/1; canonical SHA-256: 1f5a58ab97d8a0942b61630f5fe9855dc2f63f8a71f21c1e113292284989a5fd

SO_HO_HON05_S_p_977bf3923c

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: c2f5222d01fbf4b50bc53c71137107c76c3c7321cf350dbc2e4a0925f173568c

Theta_k(1) on H; unavailable outside H

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 7bdc9b9149b215c5a0a4af6190f0e3c4ea20ad08a178624e9fccbd6ad96872d6

Omega_k(A+B) on H intersect this comparison; unassessed outside H

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 44852b1dbfb146ba5f62582c91168e9d294311f6ab75da27dd9fa8ff4115ecaf

Lower outside H unassessed; q2 bounds remain separate.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: 6c55cb498eaace2dc5fc77f239ae0760578a98d5cdc229f35d76f5bb73281865

O_k(1+A+B)

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 6209577a27e45fb58b17ca68ae529ee5067c5d604b02d39175db3468fa2ff118

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 7d794ea7490a9f218af99811d24f38514948477015b6dbd6eb7def032fa23b5d

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: f176c1a2304341c0d1e4da7bdd008ef9a49439b5177763da7193c33b38b96cc4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 61d6cc34a43b958ddf1fa9198bda41fd2e5da92991db3bb8e8c76f8f93f370b7

SO_HO_HON05_S__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 57487e702a5b9f463aad24c3d7be279c072c2c3f2264d48780b63c4c3b01902d

Conditional unchanged bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 92ef6d8f3c446da68342ff35f8a8b464a9f08c7f6ad21213b545d71ee2b99a7e

Delta>0,M_k>0

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: 23e3814f756961fa25b2c5003198a61a54613a99a23bac41ad6496fed0e17332

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 2a2d9c487891eba39d70b19edc7e8d4c537efab3c2d5ea13dd918262cbf29dfe

SO_HO_HON05_S__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: a6b4d81ffeb8e294ee6b438d3ebbf682127a683cebcf1ec3d36448a856eee299

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: f7764d9594dd85e3608e7e028148634ddfb6cc925dd5bfec541d401df669b2cb

SO_HO_HON05_S__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: deaee5515e44f685a27cd67ba6b71cd59485a8222014a722c918bec2ab96ef78

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: e8d9ca523da3f6a06ce6e10fc38204ef187ffd3da8bbc9910b629c006169b7ca

comparison intersect H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: ff156402cf7bd52cad944cc034dc4666caa99ec0ed606016b2ecdd5f2454dc06

SO_HO_HON05_S__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 82a44e60460a701ca888c1881fe4c80c2dc2f6e671573137aecfba5da987ef47

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 73b4b43ffce5977ca7f83f6bbc55284b3cc3bc822ca8a821063dcc21f2ab0953

HO_GUARDED_ENVELOPE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: 29d0d284a61b25c383f5e97312e3b0528a7774000cc626073f30600cf6fedec1

Retained lower, with its guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: f3fef0c598f9ab2c4000597d8967a68dca7b43fca735f06eb50c576b2d8af831

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: fe7c7024f45b198e26447fc97d7ba7895ce8f92b9706eaf81f35e93a2c05968b

SO_HO_HON05_S__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/bound_uses/5; canonical SHA-256: fd3b9bee1a9e9b880d87c2173f28b9115fd557eab9be33d27238338980148ab3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/bound_id; canonical SHA-256: e9f21132ad11087e56e3dea5c81bac0db9ed0c6b83d3dd4076fc7e5b59dcc658

SO_HO_HON05_S__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native item 7

Native pointer: /joint_analysis/comparisons/3/bound_uses/6; canonical SHA-256: cd1c8180d7ee59b32ec117f006581572543b0309b570d0b50d90c37a54e529fd

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/bound_id; canonical SHA-256: 377bbe00b8b580e09512ccb27a243b045d6fc58f954e29736cee4d36e25c30ce

SO_HO_HON05_S__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/reason; canonical SHA-256: e8f0c99d44b1117d92e9d04113c4af01cdf9ab29b95be00372b345a673f309c1

Different native q2; no transfer into q1 adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/validity_region; canonical SHA-256: 07ee519bfa51f165e1704239df829bacfdd5676be775bfcab77d8cf340ea6004

A>=C_k,d>=C_k(1+A)

#### Native item 8

Native pointer: /joint_analysis/comparisons/3/bound_uses/7; canonical SHA-256: 834415b0ffd3fa23c7c59509dd903ebeaa556071bdada0b0df1527e6d4bac13a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/bound_id; canonical SHA-256: 173587647257a61ba788a08e005f90ea95ca813081cc8d7424410c3ccc73a4fb

SO_HO_HON05_S__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/reason; canonical SHA-256: e8f0c99d44b1117d92e9d04113c4af01cdf9ab29b95be00372b345a673f309c1

Different native q2; no transfer into q1 adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/validity_region; canonical SHA-256: b7b66d13ad5e938a6402b2b129b054f395d210c8aeafdb03656035f3a4280230

B>=C_k,d>=C_k(1+B)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: 545d141fb6210cca4db0b227396e24eccab589a5a4068c8922782c70935baa92

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: 7a46c6e2d2d69f6377b7f5618acfc5aaae05aa6d6395329a9e99edf176ec90a4

H is source applicability, not an intrinsic dimension transition.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: 3d71fa1e2e95f41b5cf97fac21fe2ce670ac2bfaf0b9af6a863458122e39af11

On H, 1+A+B=O_k(A+B).

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/boundary_checks/2; canonical SHA-256: 8da9c6ee496e95be1af049c18aa626531b77fd32e7d6918ba1aba715c6b8d669

Zero-gap and zero-modulus endpoints handled separately.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: c2f5222d01fbf4b50bc53c71137107c76c3c7321cf350dbc2e4a0925f173568c

Theta_k(1) on H; unavailable outside H

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 7bdc9b9149b215c5a0a4af6190f0e3c4ea20ad08a178624e9fccbd6ad96872d6

Omega_k(A+B) on H intersect this comparison; unassessed outside H

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 44852b1dbfb146ba5f62582c91168e9d294311f6ab75da27dd9fa8ff4115ecaf

Lower outside H unassessed; q2 bounds remain separate.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: 6c55cb498eaace2dc5fc77f239ae0760578a98d5cdc229f35d76f5bb73281865

O_k(1+A+B)

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: c6d5a8692d25069fcbe00fc89630af80fd545922e1a631ab5b016f2a510b5b8d

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: d684a32e3353206333e895c409c89f23a6345a3c7db3473dbeb42c49445053f3

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: 1a2a089b8dfa3f38fa999f34c802e85db9147c1e947926e111cdac668e5a965d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: 57487e702a5b9f463aad24c3d7be279c072c2c3f2264d48780b63c4c3b01902d

Conditional unchanged bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 92ef6d8f3c446da68342ff35f8a8b464a9f08c7f6ad21213b545d71ee2b99a7e

Delta>0,M_k>0

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: 008227158dc9156af3ca6a884657e4d018a51790f7b86303c47922473de668ae

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: 9b53c78c06e9b16db6e5313a0b8410c6822f44c37d67cbfd441c0eef554c363e

SO_HO_HON05_S__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: 57487e702a5b9f463aad24c3d7be279c072c2c3f2264d48780b63c4c3b01902d

Conditional unchanged bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: cd045dd9c71bc81511b2fa015c942988122e9ac918912150ac19faa3a0058fc6

J

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: a718b6a92770b70f78e4738961e31cb6fce4b833539bfca21fd539e533beca73

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: 3a8b66baa39313f9a8f2e8d07ae352f24934166563c1648588e869cd38c7a7b5

C_0 is fixed; do not substitute a varying B/A into its hidden constants.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: 2f23be3f3509558fb70a62770f6637f34fbdd0cda81bad4943db8bac38d5d46e

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/constant_dependencies/1; canonical SHA-256: 1f5a58ab97d8a0942b61630f5fe9855dc2f63f8a71f21c1e113292284989a5fd

SO_HO_HON05_S_p_977bf3923c

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: 2f23be3f3509558fb70a62770f6637f34fbdd0cda81bad4943db8bac38d5d46e

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/fixed_parameters/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/fixed_parameters/1; canonical SHA-256: 1f5a58ab97d8a0942b61630f5fe9855dc2f63f8a71f21c1e113292284989a5fd

SO_HO_HON05_S_p_977bf3923c

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: 10cd043524e6b4c89c5a46d4a7014061cad63fc65e744a107fc0f52d7a8a9d52

Theta_{k,C_0}(1)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: 420fbf9992ef2dae9e07858149adcaa98e4528b4ff50d421e1e77c9c7080a9ca

Omega_k(1+A) on J

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: 870b5fc493b12612a66241740c20ac96cc115da75bd88e3c4dc98351927359dd

No rate gap on J under conditional retention; outside J unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: 6c55cb498eaace2dc5fc77f239ae0760578a98d5cdc229f35d76f5bb73281865

O_k(1+A+B)

#### Native item 6

Native pointer: /joint_analysis/comparisons/5; canonical SHA-256: 09f3ee95adc35c44cbdf548aef16a9470843aa48ec862823f22498c0b4519741

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/5/bound_uses; canonical SHA-256: 41ea58bf29785cc53ac722233edf55b6806aa91a70721a869b40e69001b5d452

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0; canonical SHA-256: 4e7027a1f03a858267e517d283009ca0739d4f8f6dfeadab5134176fa7816d93

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/adopted_region; canonical SHA-256: bd26ecb040b07c34df35c692e2e65c93b66473df14eba730592017572cd6cacb

Comparison region: ($k\ge 3,B>C_0 A$) AND Bound validity: (Referenced regions: ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$) AND ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "$d\\ge 1,\\Delta>0,M_k>0,\\varepsilon_g>0,\\varepsilon_H>0$", "region_ref": "SO_HO_HON05_S__randomized__r2"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/bound_id; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/reason; canonical SHA-256: 57487e702a5b9f463aad24c3d7be279c072c2c3f2264d48780b63c4c3b01902d

Conditional unchanged bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/validity_region; canonical SHA-256: 92ef6d8f3c446da68342ff35f8a8b464a9f08c7f6ad21213b545d71ee2b99a7e

Delta>0,M_k>0

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1; canonical SHA-256: ef830e81cd2dc6903be5b6dd145b40d52c5b6df749e3a41bee9b11677807597d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/bound_id; canonical SHA-256: 1d8be8836dfaefd01b9b7c2dac6ee8eff26b1d09206cab8c5a3167795d2f85fa

SO_HO_HON05_S__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/bound_uses/2; canonical SHA-256: bb27fc02ee151f6c60a4d5ce4cc7431f5500f73a5d529b25b536d19d9b574008

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/bound_id; canonical SHA-256: 3fe5491ee1e3a58e6cb01b8f7e813fe1eec87fd1b9a14d727ae0fe55524d78a2

SO_HO_HON05_S__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/bound_uses/3; canonical SHA-256: 79664b7b218d316f0cb53bb7824881599c75b2d916b06e8a7472fda09f44ac2e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/adopted_region; canonical SHA-256: 8449dff249b1e3516182b10f5dd8368cb9ba25ef578c1fa8ca9a3eaf18ad7b81

Comparison region: ($k\ge 3,B>C_0 A$) AND Bound validity: (Referenced regions: ($\Delta>0,M_k>0,A\ge C_k,d\ge C_k(1+A)\log(3+A)$) AND (Delta>0, M_k>0, A>=C_k, d>=C_k(1+A)log(3+A))) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "$\\Delta>0,M_k>0,A\\ge C_k,d\\ge C_k(1+A)\\log(3+A)$", "region_ref": "SO_HO_HON05_S__randomized__r7"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/bound_id; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs; canonical SHA-256: 8e47a3ee60869f18447621d8dccf7f5d793f180b25199fddd4f17f98d5168f03

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 870e4304ff412f84a5969428876cde72a3db0d2b5cc7e6c090fbddd18d7e6899

HO_RANDOMIZED_GRADIENT_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/reason; canonical SHA-256: 6192b0ea65ff03ab4d03eb9b060e913dc5e69716e0433c318ac9a34280965fef

Source-backed q2 lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/validity_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native item 5

Native pointer: /joint_analysis/comparisons/5/bound_uses/4; canonical SHA-256: fd1c64972811751a9eb40a09dce621cd7a7d4e05114e0f0782cc93373b3d5b5c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/bound_id; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native item 6

Native pointer: /joint_analysis/comparisons/5/bound_uses/5; canonical SHA-256: 38f1630359246826c45bbe2853fee5cc642f2b2e8bdc1b0b62301e49e2c6ce37

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/bound_id; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/5/boundary_checks; canonical SHA-256: 235925d9b912e6c3cad724610c6dad9ce93ab7952cec46e1d10a5a83296299c0

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/boundary_checks/0; canonical SHA-256: 8dba4d79da0fc8b19c69c75f96ac90da93971964b3a84ad8eab0580a5d92bc26

This curvature comparison has B>C0A, so its intersection with J is empty. q2 tightness on J is published only in new SO_HO_HON05_S__randomized__c6_q2_J.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/boundary_checks/1; canonical SHA-256: 57d4ab2f7fd52c16454be5efb5a1bd6e1e940d7d08661d76b0cc638b8652736e

The sourceb5 lower is adopted on G intersect this curvature comparison only; its quotient can grow withB/(1+A).

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/boundary_checks/2; canonical SHA-256: 1e5948170db101c706db1eb96232cff46c4b72270609781f0fa5a0e30e98c197

All source workload/dimension constants and separate zero/polynomial endpoints retained.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/5/comparison_id; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/5/constant_dependencies; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/5/fixed_parameters; canonical SHA-256: 2f23be3f3509558fb70a62770f6637f34fbdd0cda81bad4943db8bac38d5d46e

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/fixed_parameters/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/fixed_parameters/1; canonical SHA-256: 1f5a58ab97d8a0942b61630f5fe9855dc2f63f8a71f21c1e113292284989a5fd

SO_HO_HON05_S_p_977bf3923c

#### Native field: gap

Native pointer: /joint_analysis/comparisons/5/gap; canonical SHA-256: fdf6f75b2ce5404c7eec53a6e726cb51647a9f9ae961f18e75b178bf3f9325f4

O_k((1+A+B)/(1+A)) on G; unavailable outside G

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/5/lower_envelope; canonical SHA-256: 3419b7b852e15efd16c12a3de50eb01808b8c1a5de5500c739422a2c04911f08

Omega_k(1+A) on G intersect this comparison; unassessed outside G

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/5/remaining_gap; canonical SHA-256: 03c5243b8e95901e737b508dffd7c59a972e1e9a0a6c770dc5ed57f39d94c446

Curvature gap can grow when B/(1+A) grows; lower outside G unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/5/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/5/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/5/upper_envelope; canonical SHA-256: 6c55cb498eaace2dc5fc77f239ae0760578a98d5cdc229f35d76f5bb73281865

O_k(1+A+B)

#### Native item 7

Native pointer: /joint_analysis/comparisons/6; canonical SHA-256: d4ee5c3e8882a79e000c3821870f11c72db3a54dd4edbe516eed1ea61350039a

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/6/bound_uses; canonical SHA-256: dc2e3a2d5c39ea16cee414a39b529034cdcdf5d670da87a8e6c5ec4296143d35

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0; canonical SHA-256: 7b572a65c0d4a2d62ff055cdf589960a4620cb0d735b2ab186a4c092d70cae02

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/bound_id; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/validity_region; canonical SHA-256: 92ef6d8f3c446da68342ff35f8a8b464a9f08c7f6ad21213b545d71ee2b99a7e

Delta>0,M_k>0

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/bound_uses/1; canonical SHA-256: eec040b002de18c06ac3590a23df70d4ce78fe27ef4359709d7279a0329db507

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/bound_id; canonical SHA-256: 1d8be8836dfaefd01b9b7c2dac6ee8eff26b1d09206cab8c5a3167795d2f85fa

SO_HO_HON05_S__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/reason; canonical SHA-256: 57487e702a5b9f463aad24c3d7be279c072c2c3f2264d48780b63c4c3b01902d

Conditional unchanged bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/bound_uses/2; canonical SHA-256: 94384a79db13bc4dd6d1cb466d2f43f164ea3b7ff868fa6c46a2e76e97d6b8d6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/bound_id; canonical SHA-256: 3fe5491ee1e3a58e6cb01b8f7e813fe1eec87fd1b9a14d727ae0fe55524d78a2

SO_HO_HON05_S__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/reason; canonical SHA-256: 57487e702a5b9f463aad24c3d7be279c072c2c3f2264d48780b63c4c3b01902d

Conditional unchanged bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/bound_uses/3; canonical SHA-256: 283197d71c72f40840292d02437cb9a608107b023dc78843d77ea4e5c32cfb96

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/bound_id; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/validity_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native item 5

Native pointer: /joint_analysis/comparisons/6/bound_uses/4; canonical SHA-256: fd1c64972811751a9eb40a09dce621cd7a7d4e05114e0f0782cc93373b3d5b5c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/bound_id; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/4/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native item 6

Native pointer: /joint_analysis/comparisons/6/bound_uses/5; canonical SHA-256: 38f1630359246826c45bbe2853fee5cc642f2b2e8bdc1b0b62301e49e2c6ce37

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/bound_id; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/5/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/6/boundary_checks; canonical SHA-256: ac19e821af5c79eccd15ddd53970649e729a0bef6355342481efe4b7a9fa2b60

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/boundary_checks/0; canonical SHA-256: 7743fb77b40085bcf3bcd2c4bb8c69fab247537515555f147ae8e319cacb599e

Delta=0 includes M_k=0.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/6/comparison_id; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/6/constant_dependencies; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/6/fixed_parameters; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/fixed_parameters/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: gap

Native pointer: /joint_analysis/comparisons/6/gap; canonical SHA-256: 17bd2b03af8aaf409327ca267e43a321031d93862c071f4b23f121c2246bcf09

Inapplicable ratio: exact zero cost.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/6/lower_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/6/remaining_gap; canonical SHA-256: efe12abd516569f289ea53fe9f2d0c8d7b9513a8249725b9dc831156383ae6a6

None within this branch.

#### Native field: role

Native pointer: /joint_analysis/comparisons/6/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/6/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/6/upper_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native item 8

Native pointer: /joint_analysis/comparisons/7; canonical SHA-256: 7578a1b95dbd293666580828239b52a51fb45538fb49d98553d1e3b55f7d7cba

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/7/bound_uses; canonical SHA-256: 113c4d8c4e6592201b732a22d2bc1ee6f681e4e6fea0e27284f1f912544212d0

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/0; canonical SHA-256: 4c15c2d767db9a8150054e7bfa67cf6f3567c55a7bbfae1fcdf3acef7b3e5067

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/adopted_region; canonical SHA-256: e53b1d7ec8535999c6963e4cc9f391171bfa2e59d5b2cbbe82e38638cb20b070

Comparison region: ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$) AND Bound validity: (Referenced regions: ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$) AND ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$))

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/bound_id; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/reason; canonical SHA-256: 57487e702a5b9f463aad24c3d7be279c072c2c3f2264d48780b63c4c3b01902d

Conditional unchanged bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/validity_region; canonical SHA-256: 92ef6d8f3c446da68342ff35f8a8b464a9f08c7f6ad21213b545d71ee2b99a7e

Delta>0,M_k>0

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/bound_uses/1; canonical SHA-256: ef830e81cd2dc6903be5b6dd145b40d52c5b6df749e3a41bee9b11677807597d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/bound_id; canonical SHA-256: 1d8be8836dfaefd01b9b7c2dac6ee8eff26b1d09206cab8c5a3167795d2f85fa

SO_HO_HON05_S__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 3

Native pointer: /joint_analysis/comparisons/7/bound_uses/2; canonical SHA-256: bb27fc02ee151f6c60a4d5ce4cc7431f5500f73a5d529b25b536d19d9b574008

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/bound_id; canonical SHA-256: 3fe5491ee1e3a58e6cb01b8f7e813fe1eec87fd1b9a14d727ae0fe55524d78a2

SO_HO_HON05_S__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 4

Native pointer: /joint_analysis/comparisons/7/bound_uses/3; canonical SHA-256: 38877497043fcaacfecbe7f0072be59de48b18767c347ba1ac1956fadc9290f3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/adopted_region; canonical SHA-256: f031c9cce2828c38d621fddf2b22794d3b829df5b9c8bf0104d05e6d8e1c9990

Comparison region: ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$) AND Bound validity: (Referenced regions: ($\Delta>0,M_k>0,A\ge C_k,d\ge C_k(1+A)\log(3+A)$) AND (Delta>0, M_k>0, A>=C_k, d>=C_k(1+A)log(3+A))) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "$\\Delta>0,M_k>0,A\\ge C_k,d\\ge C_k(1+A)\\log(3+A)$", "region_ref": "SO_HO_HON05_S__randomized__r7"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/bound_id; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/mapping_proof_refs; canonical SHA-256: 8e47a3ee60869f18447621d8dccf7f5d793f180b25199fddd4f17f98d5168f03

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 870e4304ff412f84a5969428876cde72a3db0d2b5cc7e6c090fbddd18d7e6899

HO_RANDOMIZED_GRADIENT_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/reason; canonical SHA-256: 6192b0ea65ff03ab4d03eb9b060e913dc5e69716e0433c318ac9a34280965fef

Source-backed q2 lower.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/3/validity_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native item 5

Native pointer: /joint_analysis/comparisons/7/bound_uses/4; canonical SHA-256: fd1c64972811751a9eb40a09dce621cd7a7d4e05114e0f0782cc93373b3d5b5c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/bound_id; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/4/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native item 6

Native pointer: /joint_analysis/comparisons/7/bound_uses/5; canonical SHA-256: 38f1630359246826c45bbe2853fee5cc642f2b2e8bdc1b0b62301e49e2c6ce37

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/bound_id; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/5/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native item 7

Native pointer: /joint_analysis/comparisons/7/bound_uses/6; canonical SHA-256: fb92e4beeed2ca5ccae81d5bd0ffb44b4c121bf0c9a453b2f42caf3bff057cbc

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/bound_id; canonical SHA-256: 9b53c78c06e9b16db6e5313a0b8410c6822f44c37d67cbfd441c0eef554c363e

SO_HO_HON05_S__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/reason; canonical SHA-256: 6629a3530cf3b0f8615d32fcb64434e98044687ab24eca06e449539923368225

Old q1 bound is not merged into q2; new b5 has an independent mapping.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/6/validity_region; canonical SHA-256: cd045dd9c71bc81511b2fa015c942988122e9ac918912150ac19faa3a0058fc6

J

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/7/boundary_checks; canonical SHA-256: 71572f30f442c44b1843cdfe526a40162b1255ff70d100babea1ec5acfe2d1d6

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/boundary_checks/0; canonical SHA-256: 77f0e1d1be3957bdd1b4da10621d4b98e7ad846836b0ea08ee3650af24b54af1

Native q2 lower b5 has no B<=C0A condition: validity is exactG.

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/boundary_checks/1; canonical SHA-256: 378475cb446b8a66dbf2f43265d3a9ad973d9e17313fc187b8479079ecc5508b

Its matching fixed-ratio consequence on J now has separate optimal q2 comparison SO_HO_HON05_S__randomized__c6_q2_J.

#### Native item 3

Native pointer: /joint_analysis/comparisons/7/boundary_checks/2; canonical SHA-256: 9102683b132a319db31721b4f7741154425346a1be3ca80bfa76ec894a67b0f7

Outside J no q2 tightness is inferred; source thresholds have k-only unspecified constants.

#### Native item 4

Native pointer: /joint_analysis/comparisons/7/boundary_checks/3; canonical SHA-256: 7d71ca5a017c133f64d0ed503bb0d764f5eebf8f3a75c7b00e6d6bd8e877c690

Zero-gap and zero-modulus endpoints are separate.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/7/comparison_id; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/7/constant_dependencies; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/7/fixed_parameters; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/fixed_parameters/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: gap

Native pointer: /joint_analysis/comparisons/7/gap; canonical SHA-256: fdf6f75b2ce5404c7eec53a6e726cb51647a9f9ae961f18e75b178bf3f9325f4

O_k((1+A+B)/(1+A)) on G; unavailable outside G

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/7/lower_envelope; canonical SHA-256: 3419b7b852e15efd16c12a3de50eb01808b8c1a5de5500c739422a2c04911f08

Omega_k(1+A) on G intersect this comparison; unassessed outside G

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/7/remaining_gap; canonical SHA-256: 03c5243b8e95901e737b508dffd7c59a972e1e9a0a6c770dc5ed57f39d94c446

Curvature gap can grow when B/(1+A) grows; lower outside G unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/7/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/7/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/7/upper_envelope; canonical SHA-256: 6c55cb498eaace2dc5fc77f239ae0760578a98d5cdc229f35d76f5bb73281865

O_k(1+A+B)

#### Native item 9

Native pointer: /joint_analysis/comparisons/8; canonical SHA-256: a36118dfde8135ffad92251c647e051cbefd18677ab1fca043ade6b012f6e16b

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/8/bound_uses; canonical SHA-256: 278ed437a81465c08f95fe885e9beafa52f0ec8dc5135b1481f0f100903247a1

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/0; canonical SHA-256: fcc880e8cae8fd95ed18bbdae1bb66006e8db1909e3e0b016832ab492bfc23d5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/bound_id; canonical SHA-256: 61d6cc34a43b958ddf1fa9198bda41fd2e5da92991db3bb8e8c76f8f93f370b7

SO_HO_HON05_S__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/validity_region; canonical SHA-256: 92ef6d8f3c446da68342ff35f8a8b464a9f08c7f6ad21213b545d71ee2b99a7e

Delta>0,M_k>0

#### Native item 2

Native pointer: /joint_analysis/comparisons/8/bound_uses/1; canonical SHA-256: 23e3814f756961fa25b2c5003198a61a54613a99a23bac41ad6496fed0e17332

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/bound_id; canonical SHA-256: 2a2d9c487891eba39d70b19edc7e8d4c537efab3c2d5ea13dd918262cbf29dfe

SO_HO_HON05_S__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 3

Native pointer: /joint_analysis/comparisons/8/bound_uses/2; canonical SHA-256: a6b4d81ffeb8e294ee6b438d3ebbf682127a683cebcf1ec3d36448a856eee299

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/bound_id; canonical SHA-256: f7764d9594dd85e3608e7e028148634ddfb6cc925dd5bfec541d401df669b2cb

SO_HO_HON05_S__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 4

Native pointer: /joint_analysis/comparisons/8/bound_uses/3; canonical SHA-256: ddea295858a3eacb41372613f154754509a24dbbbd0b3b66ad3ceddf0e378a0a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/bound_id; canonical SHA-256: ff156402cf7bd52cad944cc034dc4666caa99ec0ed606016b2ecdd5f2454dc06

SO_HO_HON05_S__deterministic__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/validity_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 5

Native pointer: /joint_analysis/comparisons/8/bound_uses/4; canonical SHA-256: 1fc73bddef97afcb7d5bba171056b861064fd1c42fcb55baab355091a1abc723

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/bound_id; canonical SHA-256: fe7c7024f45b198e26447fc97d7ba7895ce8f92b9706eaf81f35e93a2c05968b

SO_HO_HON05_S__deterministic__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/mapping_proof_refs; canonical SHA-256: 546bf492c7b9c11ee35f16a724f801d7db6db5ded029f06e1ba4133311cba323

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 5b135968819c938cbd625b7cdc79942df0278dac868fc6a40d0104866c264c2b

HO_POLYNOMIAL_ONE_CALL

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/reason; canonical SHA-256: 58a30a2f84b1c5247cc0c56b471b35850ab3257bc06d88d83339df452661a74b

Exact polynomial branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native item 6

Native pointer: /joint_analysis/comparisons/8/bound_uses/5; canonical SHA-256: 152784c4b7c24a5da59622a6c6740e2cb345df61656f1fb5ea5afc5e3d9efaac

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/bound_id; canonical SHA-256: e9f21132ad11087e56e3dea5c81bac0db9ed0c6b83d3dd4076fc7e5b59dcc658

SO_HO_HON05_S__deterministic__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/mapping_proof_refs; canonical SHA-256: 546bf492c7b9c11ee35f16a724f801d7db6db5ded029f06e1ba4133311cba323

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: 5b135968819c938cbd625b7cdc79942df0278dac868fc6a40d0104866c264c2b

HO_POLYNOMIAL_ONE_CALL

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/reason; canonical SHA-256: 58a30a2f84b1c5247cc0c56b471b35850ab3257bc06d88d83339df452661a74b

Exact polynomial branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/5/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/8/boundary_checks; canonical SHA-256: 8fb74c3f6ccf7c4feac630b70d8769b108f0cc089aedc13556c8b9bb882d2a39

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/boundary_checks/0; canonical SHA-256: 93b6eeda8ccf97fc0126aef3c31a83bb6e5b2a3b85a90690754410cf7aee46d6

Delta=0 excluded; its cost is zero.

#### Native item 2

Native pointer: /joint_analysis/comparisons/8/boundary_checks/1; canonical SHA-256: 13b39bccb0a3658d3de2eb40274ecd61776535f23ba776be79395ac15b38170b

A=B=0 does not imply zero calls: quadratic curvature is uncontrolled.

#### Native item 3

Native pointer: /joint_analysis/comparisons/8/boundary_checks/2; canonical SHA-256: de7a1fe0650e9b0f0508c01a07212648195dbe3818dd396ae25c961608f8d5be

d=1 and k=2 included.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/8/comparison_id; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/8/constant_dependencies; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/8/fixed_parameters; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/fixed_parameters/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: gap

Native pointer: /joint_analysis/comparisons/8/gap; canonical SHA-256: 19e7b00f3706ee6ccd014a695afde439c3137e6507b75aec1b1954fda32ece1f

1 exactly

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/8/lower_envelope; canonical SHA-256: 19e7b00f3706ee6ccd014a695afde439c3137e6507b75aec1b1954fda32ece1f

1 exactly

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/8/remaining_gap; canonical SHA-256: efe12abd516569f289ea53fe9f2d0c8d7b9513a8249725b9dc831156383ae6a6

None within this branch.

#### Native field: role

Native pointer: /joint_analysis/comparisons/8/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/8/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/8/upper_envelope; canonical SHA-256: 19e7b00f3706ee6ccd014a695afde439c3137e6507b75aec1b1954fda32ece1f

1 exactly

#### Native item 10

Native pointer: /joint_analysis/comparisons/9; canonical SHA-256: f89d387eba576b59f9d307895eb0e7baa65d1b3e2332d42a190420111a1f54cc

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/9/bound_uses; canonical SHA-256: 999d239f087fde68bec3dc40fbca7330af08b3bdf51fe54df1880b30c126db79

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/0; canonical SHA-256: 7b572a65c0d4a2d62ff055cdf589960a4620cb0d735b2ab186a4c092d70cae02

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/bound_id; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/validity_region; canonical SHA-256: 92ef6d8f3c446da68342ff35f8a8b464a9f08c7f6ad21213b545d71ee2b99a7e

Delta>0,M_k>0

#### Native item 2

Native pointer: /joint_analysis/comparisons/9/bound_uses/1; canonical SHA-256: ef830e81cd2dc6903be5b6dd145b40d52c5b6df749e3a41bee9b11677807597d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/bound_id; canonical SHA-256: 1d8be8836dfaefd01b9b7c2dac6ee8eff26b1d09206cab8c5a3167795d2f85fa

SO_HO_HON05_S__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 3

Native pointer: /joint_analysis/comparisons/9/bound_uses/2; canonical SHA-256: bb27fc02ee151f6c60a4d5ce4cc7431f5500f73a5d529b25b536d19d9b574008

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/bound_id; canonical SHA-256: 3fe5491ee1e3a58e6cb01b8f7e813fe1eec87fd1b9a14d727ae0fe55524d78a2

SO_HO_HON05_S__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/validity_region; canonical SHA-256: bf7f0e141f886fe007dc650fe7afb918d9e2e5f606cd9b045b59f5f35bc6a062

Delta=0

#### Native item 4

Native pointer: /joint_analysis/comparisons/9/bound_uses/3; canonical SHA-256: 283197d71c72f40840292d02437cb9a608107b023dc78843d77ea4e5c32cfb96

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/bound_id; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/reason; canonical SHA-256: 58251751626334de877effc94e72c384c64821c20accd64819ddd45843ac6519

Disjoint parameter guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/validity_region; canonical SHA-256: aa61870c76b8f6f57889888fbf24c006487753f3139494f7790353cf5a998492

G

#### Native item 5

Native pointer: /joint_analysis/comparisons/9/bound_uses/4; canonical SHA-256: da85a5c9d7dcd9319ee72d28b8d70c0d1a58504d644b3bc874f2f90f1a6b3249

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/bound_id; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/mapping_proof_refs; canonical SHA-256: 546bf492c7b9c11ee35f16a724f801d7db6db5ded029f06e1ba4133311cba323

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 5b135968819c938cbd625b7cdc79942df0278dac868fc6a40d0104866c264c2b

HO_POLYNOMIAL_ONE_CALL

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/reason; canonical SHA-256: 58a30a2f84b1c5247cc0c56b471b35850ab3257bc06d88d83339df452661a74b

Exact polynomial branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native item 6

Native pointer: /joint_analysis/comparisons/9/bound_uses/5; canonical SHA-256: 6e20644cc00a812cec57de2f2a0fc778b44f540b5be131550383ace23b732a60

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/adopted_region; canonical SHA-256: 358cf98022aed946459208f6dd65db68d9c500f22521c0303faa3ab452a21f59

whole comparison

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/bound_id; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/mapping_proof_refs; canonical SHA-256: 546bf492c7b9c11ee35f16a724f801d7db6db5ded029f06e1ba4133311cba323

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: 5b135968819c938cbd625b7cdc79942df0278dac868fc6a40d0104866c264c2b

HO_POLYNOMIAL_ONE_CALL

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/reason; canonical SHA-256: 58a30a2f84b1c5247cc0c56b471b35850ab3257bc06d88d83339df452661a74b

Exact polynomial branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/5/validity_region; canonical SHA-256: a5d23a567371c76fb5f620fed5f71be0919ff6ebb558cf709765eebeb6254c4b

Delta>0,M_k=0

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/9/boundary_checks; canonical SHA-256: 8fb74c3f6ccf7c4feac630b70d8769b108f0cc089aedc13556c8b9bb882d2a39

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/boundary_checks/0; canonical SHA-256: 93b6eeda8ccf97fc0126aef3c31a83bb6e5b2a3b85a90690754410cf7aee46d6

Delta=0 excluded; its cost is zero.

#### Native item 2

Native pointer: /joint_analysis/comparisons/9/boundary_checks/1; canonical SHA-256: 13b39bccb0a3658d3de2eb40274ecd61776535f23ba776be79395ac15b38170b

A=B=0 does not imply zero calls: quadratic curvature is uncontrolled.

#### Native item 3

Native pointer: /joint_analysis/comparisons/9/boundary_checks/2; canonical SHA-256: de7a1fe0650e9b0f0508c01a07212648195dbe3818dd396ae25c961608f8d5be

d=1 and k=2 included.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/9/comparison_id; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/9/constant_dependencies; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/9/fixed_parameters; canonical SHA-256: cd6cfe5b144ac1ff76dd968d24d950dfb4a668bdba3cd21c51afd09b5778b663

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/fixed_parameters/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: gap

Native pointer: /joint_analysis/comparisons/9/gap; canonical SHA-256: 19e7b00f3706ee6ccd014a695afde439c3137e6507b75aec1b1954fda32ece1f

1 exactly

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/9/lower_envelope; canonical SHA-256: 19e7b00f3706ee6ccd014a695afde439c3137e6507b75aec1b1954fda32ece1f

1 exactly

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/9/remaining_gap; canonical SHA-256: efe12abd516569f289ea53fe9f2d0c8d7b9513a8249725b9dc831156383ae6a6

None within this branch.

#### Native field: role

Native pointer: /joint_analysis/comparisons/9/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/9/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/9/upper_envelope; canonical SHA-256: 19e7b00f3706ee6ccd014a695afde439c3137e6507b75aec1b1954fda32ece1f

1 exactly

#### Native item 11

Native pointer: /joint_analysis/comparisons/10; canonical SHA-256: bc6b9b5d40f18974098213040c68c116e5fedbc109515fd50cc3084ad2a1cf33

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/10/bound_uses; canonical SHA-256: b763cf9ef49762134845074c7725c7a6ceb26b8560ec19896848b1909bc8542b

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/0; canonical SHA-256: 59334716fdd3b27c4debb70c497e9fadca164e0ba7100941ce47f5641ded4af5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/adopted_region; canonical SHA-256: db23119119eeea525264de6318ad06eb882293ccbc5c12c5eab92395be0dd938

Comparison region: ($A\ge C_k,B\le C_0 A,d\ge C_k(1+A)\log(3+A)$) AND Bound validity: (Referenced regions: ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$) AND ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$)) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Full unchanged positive-domain upper restricted to exactJ.", "region_ref": "SO_HO_HON05_S__randomized__r3"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/bound_id; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/mapping_proof_refs; canonical SHA-256: da7b2749266c1abec3a82da6daac572c52cea8fb9a5704ae67622feef5df1509

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: fedeaf8a8b4c6dff330975f648fe542d9c163249c8576a514ade49cf95b7cd25

HO_RANDOMIZED_Q2_J_NATIVE_CLOSURE_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/reason; canonical SHA-256: 55f95f5991cf84411fca31c7091b01cfac5b685eb9f8458ba000c953757eb86f

Same native q2 contract and explicitly proved guarded matching envelope; complete new publication proof HO_RANDOMIZED_Q2_J_NATIVE_CLOSURE_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/validity_region; canonical SHA-256: 09269de6a0d5708234f2be9a6e93f3ef91f4daa3a4a8a7e67609bccbe2b043ba

Referenced regions: ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$) AND ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$)

#### Native item 2

Native pointer: /joint_analysis/comparisons/10/bound_uses/1; canonical SHA-256: 9be512a069f8932e094d4e3e135b5bcf54734aba6ce941614bd0fc3938918723

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/adopted_region; canonical SHA-256: 6125727f320f1cd56a50d7e411968e5463947acea9bb1e5778c2be323b166748

Not included in this newq2J bracket.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/bound_id; canonical SHA-256: 1d8be8836dfaefd01b9b7c2dac6ee8eff26b1d09206cab8c5a3167795d2f85fa

SO_HO_HON05_S__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/reason; canonical SHA-256: ba3c6eb5b873c15ea7937a47b91bd1af9caa9c541e996e1ed439948a7cf98160

Old q1 is not used to prove q2; zero-gap and polynomial branches are disjoint from positive-modulus J. All original guards/quantity IDs retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/validity_region; canonical SHA-256: 0a246c5cb81c0559c4bd31ec8e44b3c760b556d75c1cba5d791d9a2d96120156

Referenced regions: ($\Delta=0$) AND ($\Delta=0$)

#### Native item 3

Native pointer: /joint_analysis/comparisons/10/bound_uses/2; canonical SHA-256: 97b9d06ee3825d823db1d3e0951f2fe12f03a71ffafaf3bcd9f4ed8cf67b90bb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/adopted_region; canonical SHA-256: 6125727f320f1cd56a50d7e411968e5463947acea9bb1e5778c2be323b166748

Not included in this newq2J bracket.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/bound_id; canonical SHA-256: 3fe5491ee1e3a58e6cb01b8f7e813fe1eec87fd1b9a14d727ae0fe55524d78a2

SO_HO_HON05_S__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/reason; canonical SHA-256: ba3c6eb5b873c15ea7937a47b91bd1af9caa9c541e996e1ed439948a7cf98160

Old q1 is not used to prove q2; zero-gap and polynomial branches are disjoint from positive-modulus J. All original guards/quantity IDs retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/validity_region; canonical SHA-256: 0a246c5cb81c0559c4bd31ec8e44b3c760b556d75c1cba5d791d9a2d96120156

Referenced regions: ($\Delta=0$) AND ($\Delta=0$)

#### Native item 4

Native pointer: /joint_analysis/comparisons/10/bound_uses/3; canonical SHA-256: 3371007a1b4e52f737ee25cd6afd562224b3af564d981ee7c4d0604efbe0e239

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/adopted_region; canonical SHA-256: 903008ef3856ab56e8d589cb6e59f07dcd869acb1b9e3aa17cb0a1753726a5bc

Comparison region: ($A\ge C_k,B\le C_0 A,d\ge C_k(1+A)\log(3+A)$) AND Bound validity: (Referenced regions: ($\Delta>0,M_k>0,A\ge C_k,d\ge C_k(1+A)\log(3+A)$) AND (Delta>0, M_k>0, A>=C_k, d>=C_k(1+A)log(3+A))) AND Native claim-guard declaration (retain its branch semantics): [{"predicate_text": "Exact sourceG, intersected with comparisonJ; no guard extension.", "region_ref": "SO_HO_HON05_S__randomized__r7"}]

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/bound_id; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/mapping_proof_refs; canonical SHA-256: f44b4dd24c90a5184abe2b7bf6763d36378b7b0c8d6ae3c0f328a828fc89e8c1

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: fedeaf8a8b4c6dff330975f648fe542d9c163249c8576a514ade49cf95b7cd25

HO_RANDOMIZED_Q2_J_NATIVE_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/mapping_proof_refs/1; canonical SHA-256: 870e4304ff412f84a5969428876cde72a3db0d2b5cc7e6c090fbddd18d7e6899

HO_RANDOMIZED_GRADIENT_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/reason; canonical SHA-256: 55f95f5991cf84411fca31c7091b01cfac5b685eb9f8458ba000c953757eb86f

Same native q2 contract and explicitly proved guarded matching envelope; complete new publication proof HO_RANDOMIZED_Q2_J_NATIVE_CLOSURE_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/validity_region; canonical SHA-256: dcc55921c4b5bcb74d97563c74891288a01fc3413d3cc0b043aa34b8eb5875bc

Referenced regions: ($\Delta>0,M_k>0,A\ge C_k,d\ge C_k(1+A)\log(3+A)$) AND (Delta>0, M_k>0, A>=C_k, d>=C_k(1+A)log(3+A))

#### Native item 5

Native pointer: /joint_analysis/comparisons/10/bound_uses/4; canonical SHA-256: 2471e2318dad303456e15f7f162dcb42b6cd2f7fed5f7129a667ccf7c5219439

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/adopted_region; canonical SHA-256: 6125727f320f1cd56a50d7e411968e5463947acea9bb1e5778c2be323b166748

Not included in this newq2J bracket.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/bound_id; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/reason; canonical SHA-256: ba3c6eb5b873c15ea7937a47b91bd1af9caa9c541e996e1ed439948a7cf98160

Old q1 is not used to prove q2; zero-gap and polynomial branches are disjoint from positive-modulus J. All original guards/quantity IDs retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/validity_region; canonical SHA-256: 1a2a4111ab66bb847701b423136ea5bf96688708734595ef11491cfd2163adf7

Referenced regions: ($\Delta>0,M_k=0$) AND (Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0))

#### Native item 6

Native pointer: /joint_analysis/comparisons/10/bound_uses/5; canonical SHA-256: ece4ad4413690ccacd8d9db58c42f129e411664778ffd52947a9d9fda5a42c82

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/5/adopted_region; canonical SHA-256: 6125727f320f1cd56a50d7e411968e5463947acea9bb1e5778c2be323b166748

Not included in this newq2J bracket.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/5/bound_id; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/5/reason; canonical SHA-256: ba3c6eb5b873c15ea7937a47b91bd1af9caa9c541e996e1ed439948a7cf98160

Old q1 is not used to prove q2; zero-gap and polynomial branches are disjoint from positive-modulus J. All original guards/quantity IDs retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/5/validity_region; canonical SHA-256: 1a2a4111ab66bb847701b423136ea5bf96688708734595ef11491cfd2163adf7

Referenced regions: ($\Delta>0,M_k=0$) AND (Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0))

#### Native item 7

Native pointer: /joint_analysis/comparisons/10/bound_uses/6; canonical SHA-256: 4ee719fe9746d68c1037525a0d15423227df5e156d44f79f6244f9075ddf3f74

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/6/adopted_region; canonical SHA-256: 6125727f320f1cd56a50d7e411968e5463947acea9bb1e5778c2be323b166748

Not included in this newq2J bracket.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/6/bound_id; canonical SHA-256: 9b53c78c06e9b16db6e5313a0b8410c6822f44c37d67cbfd441c0eef554c363e

SO_HO_HON05_S__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/6/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/6/reason; canonical SHA-256: ba3c6eb5b873c15ea7937a47b91bd1af9caa9c541e996e1ed439948a7cf98160

Old q1 is not used to prove q2; zero-gap and polynomial branches are disjoint from positive-modulus J. All original guards/quantity IDs retained.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/6/validity_region; canonical SHA-256: 6c7b63b0d9b0a9495b583e60186b7527f487dc6b4d91ca9eb98f0c8cc6820c18

Referenced regions: ($A\ge C_k,B\le C_0 A,d\ge C_k(1+A)\log(3+A)$) AND ($A\ge C_k,B\le C_0 A,d\ge C_k(1+A)\log(3+A)$)

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/10/boundary_checks; canonical SHA-256: b30cc636c71ba737d10a5115fec7074df77b72f7de745171566d876afab632e1

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/boundary_checks/0; canonical SHA-256: faa97b5a2a55b45a7bda8e671c6f3fbc154fc76a7d1062759a13e55addfc5ed0

Exact original G sourceworkload/dimension constants retained; B=C0A included.

#### Native item 2

Native pointer: /joint_analysis/comparisons/10/boundary_checks/1; canonical SHA-256: 8d2c0971a2a2b9ada7d26397bb00370a2521fc9a922628e3dad713c5dc7266e6

C0 is fixed independent of allfivejointparameters; it is a window constant, never chosen asB/A.

#### Native item 3

Native pointer: /joint_analysis/comparisons/10/boundary_checks/2; canonical SHA-256: f5183651142bf1578937410861a020de82390d56a3e5d874ba13fc52a174096e

Complete jet count/initialization and probability2/3 are unchanged; no distinctquantity or optimum pairing.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/10/comparison_id; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/10/constant_dependencies; canonical SHA-256: 2f23be3f3509558fb70a62770f6637f34fbdd0cda81bad4943db8bac38d5d46e

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native item 2

Native pointer: /joint_analysis/comparisons/10/constant_dependencies/1; canonical SHA-256: 1f5a58ab97d8a0942b61630f5fe9855dc2f63f8a71f21c1e113292284989a5fd

SO_HO_HON05_S_p_977bf3923c

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/10/fixed_parameters; canonical SHA-256: 2f23be3f3509558fb70a62770f6637f34fbdd0cda81bad4943db8bac38d5d46e

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/fixed_parameters/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native item 2

Native pointer: /joint_analysis/comparisons/10/fixed_parameters/1; canonical SHA-256: 1f5a58ab97d8a0942b61630f5fe9855dc2f63f8a71f21c1e113292284989a5fd

SO_HO_HON05_S_p_977bf3923c

#### Native field: gap

Native pointer: /joint_analysis/comparisons/10/gap; canonical SHA-256: 0e3976e69da30e983ec4fdfe933483efc9f20ab2004660f6525cd8c7b7211cb6

Theta_{k,C0}(1); fixedC0, no joint parameter hidden.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/10/lower_envelope; canonical SHA-256: f0a4b2f1016d37d138035924c4b56716d55ba0be888bd92ecabbe5ebd37d191d

Omega_k(1+A) from nativeq2 b5 on G, restricted to J.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/10/remaining_gap; canonical SHA-256: f92e1f5ebea2b0b014fce4c004a13a15ed636bdcd50eceb5f3a5b5afcd279ca7

No rate gap only on J; q2 outside G or at growing B/A and q1 outside its registered window remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/10/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/10/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/10/upper_envelope; canonical SHA-256: ba1bfec4e14cc7896ae792e523d0cb2116b54c3e7a960229799c5ab11f0aec97

O_{k,C0}(1+A) from the SAME retained simultaneous full-jet algorithm.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 4bcc26feeacc07766b122c0c538a74c72d9a4d606ce490b776cbd84f54aede51

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: d5709c9350a5366ddd206d33923230caafc974935c615ecfb8d08327ca2f3bee

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 96b559dcd97f0ad64231a9d3b018748e85f8690a8433e958f5ba24d670f7aab3

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: b7ce3f814d0e14e74eb1dc742ad4a2c7a798413fb9771560f107cad87ef46402

zero

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 66eb6032eedbe2af4b8580e3158597786505211582bb885f6f70bec9fc6da207

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: 72863d52f6317cacc5bbcbb83f4e11d08a73c5c15d27a4d86e8d067003eb0be2

HO_ENDPOINTS

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 95ca79986adeb3b90316542be34249a210e9925925ffb7e652fd7ce0542081f8

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/1; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: a79c4aef2b67823be485ce4d298cb2c974efaff9f5e7ae1af280519050979277

Exact cost zero for the registered deterministic q1 and randomized q2.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: e213bbf478e3b55c2c76c79556cad30d32841eeec8408e9a1a12c77f14127825

Either view; Delta=0,M_k>=0

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 43df82f1ab1783bc1cdf37be2feff431233b2553a16f062cbd9611fe84353daf

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 2828b8a21e8cd71cd06db80f3835f39767299bf9d06f22f1f84ddef850de442d

polynomial

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 546bf492c7b9c11ee35f16a724f801d7db6db5ded029f06e1ba4133311cba323

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/0; canonical SHA-256: 5b135968819c938cbd625b7cdc79942df0278dac868fc6a40d0104866c264c2b

HO_POLYNOMIAL_ONE_CALL

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: ef02682616ea514f980153b8c63f1710025d6b2285fc65371f2a62ef9a33c69e

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 820adeccf03c450c8004ba457c1688ec1aa05162acf62d837ffb04ad897b2172

Exact cost one, including d=1,k=2 and all positive tolerances.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: cbe23ef3f611426f2d8b3079562de30b15b6f126954ce156585acac98c110944

Either view; Delta>0,M_k=0

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

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: e7e213048559b60668ddc1de5c6440df57350ac7fb42846d61d11a16cc30f6c4

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: e1f943b3fd592aa08179eae8262124a19c9c11301dcf27af70b0d26df0a4f5e7

det_H_C

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 25b46b44dc803532f9caa1a4d566e66e66fc1f834f463cb70e438d7f305a981d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/1; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 12378771cd8725508b9e5c1b8acc585f781fa203f17fd1b634ca4dc730eeec30

Retained tight bracket.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 99fa6a4ce3b6e48b966ebbf8a39919384347a93f60e17f1388e1f887fce422cc

deterministic q1; Delta>0,M_k>0; H and C

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

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: e705e2952accbcc9f96319f484320b3ac89f309fabf30af6ec2f5a1041c814dd

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: 809f99f351976ab2b71fd1bb01811444f3908b33e12d71f239519bcba543654e

det_H_notC

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 66156c2b0c468257af6d9f8effcde559d9fda0222922a92c3c41a06282def14b

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/1; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: 12378771cd8725508b9e5c1b8acc585f781fa203f17fd1b634ca4dc730eeec30

Retained tight bracket.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: a0d9faf6c846ba780e61747364a0171bd46969eef31b54aaa7e8fdfed0297228

deterministic q1; Delta>0,M_k>0; H and not C

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

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: d233f338b7f87911ca06001450b4784a45f0656b655f54e905b2b8bae44158d9

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: 7c7834511f3c31c26bdbe1e20bcab873203028f4fab6afeb2ae9a6347c3ac859

det_notH_C

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: 86f1e51624b741a3c4e6e934edec7bf55f1f3ff14013e1d57d76d8e40e14509c

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/0; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/1; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: 0290a77e2fccac31fe15e505a176ef189d7ca220d81c983fdbc04045b9eca73d

Lower unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: fb4706238c0c1de6f855aa7de6b13e60ad0495e335827ed70cd0933881a98d7d

deterministic q1; Delta>0,M_k>0; not H and C

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 6

Native pointer: /joint_analysis/domain_map/cells/5; canonical SHA-256: 61abd5143e62c12cbc013445c65a5f3377e1bc27e6b844e7e47900e61f37fd6b

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/5/cell_id; canonical SHA-256: 634563574ca92cc0c63fe057c7d51c44c0047313e5c7e643edcc87d34a0be8a9

det_notH_notC

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/5/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids; canonical SHA-256: a9285299c94468c04bf60e621691bbac290b133bf72d0bb74f7de5bb6c8d03fb

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids/0; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/5/note; canonical SHA-256: 0290a77e2fccac31fe15e505a176ef189d7ca220d81c983fdbc04045b9eca73d

Lower unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/5/predicate; canonical SHA-256: e20a8a1eab8c6cb65ca2ae308a876b41451d7f6e3b8694f6091ebaf44163abfe

deterministic q1; Delta>0,M_k>0; not H and not C

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/5/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/5/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/5/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 7

Native pointer: /joint_analysis/domain_map/cells/6; canonical SHA-256: 50a805207b1be039b93f428abd7f32e017f4910d272fffb9f548a6508dd10d9e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/6/cell_id; canonical SHA-256: 8f294f2ee1c507cff38b86595cd72701f8b1e1905b2a0db2ddd33b3bce4d3d40

rand_J

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/6/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/6/closure_proof_refs; canonical SHA-256: f44b4dd24c90a5184abe2b7bf6763d36378b7b0c8d6ae3c0f328a828fc89e8c1

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/6/closure_proof_refs/0; canonical SHA-256: fedeaf8a8b4c6dff330975f648fe542d9c163249c8576a514ade49cf95b7cd25

HO_RANDOMIZED_Q2_J_NATIVE_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/6/closure_proof_refs/1; canonical SHA-256: 870e4304ff412f84a5969428876cde72a3db0d2b5cc7e6c090fbddd18d7e6899

HO_RANDOMIZED_GRADIENT_TRANSFER

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids; canonical SHA-256: d457fad487720d395854f89f50e560a04be8612c5a34fe9044e38db7b14e0519

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids/0; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/6/note; canonical SHA-256: 1772f02ec1a7bd4481598d1240df449bed6898d900cc12a2fcf9954c5501b464

The native randomizedq2 comparison now publishes Theta_{k,C0}(1+A) on exactJ. A q1 comparison cannot certify q2 closure.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/6/predicate; canonical SHA-256: c79bd4a445850144112a72203280bd1e10b9af46027cfdfad97622e3e103ca02

randomized; Delta>0,M_k>0; J

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/6/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/6/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/6/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 8

Native pointer: /joint_analysis/domain_map/cells/7; canonical SHA-256: cf5b4f90264e402fe8bc348f84482eb2bf6b57393e72e3d54ca175f41fe563b0

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/7/cell_id; canonical SHA-256: 6771a30ea6f8e1354d2f3bf440f3b17ecc838c4f768c85db3472cffbe9638cb7

rand_G_C

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/7/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/7/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids; canonical SHA-256: 5d71692dc401ae12e982281e59dba58584b1416a9e3ba7a8e09cc2565e5d5c16

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids/0; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids/1; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/7/note; canonical SHA-256: cc01a3320d5f3545c67cafb6974c440b3598a61a515e51af3991d057150bf52a

q2 gap O_k(1+B/(1+A)); q1 only on J.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/7/predicate; canonical SHA-256: d4ccbec215da6cbe36d0e57c4e5fe1a7ff709e3e1c69fb71f1616b99738b16cf

randomized; Delta>0,M_k>0; G and C

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/7/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/7/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/7/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 9

Native pointer: /joint_analysis/domain_map/cells/8; canonical SHA-256: 0b15712a8ba8a1c8338c8bc8eca06e41930fb8de453967039fed1808317ca4dc

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/8/cell_id; canonical SHA-256: 6ce8d013964e366ae4769aeb7687717a6508718b9a32b414e4cf45d7d6247e35

rand_G_rest

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/8/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/8/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/8/comparison_ids; canonical SHA-256: 15eb274742572d5f35ce6ef90578fec1600898ce81d09b55f5136631e0c91184

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/8/comparison_ids/0; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/8/note; canonical SHA-256: cc01a3320d5f3545c67cafb6974c440b3598a61a515e51af3991d057150bf52a

q2 gap O_k(1+B/(1+A)); q1 only on J.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/8/predicate; canonical SHA-256: 29f0de0bf48c8934515f008e0c4804fa4e436f7bd0da70d86a1fbbd9be988cd2

randomized; Delta>0,M_k>0; G and not J and not C

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/8/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/8/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/8/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 10

Native pointer: /joint_analysis/domain_map/cells/9; canonical SHA-256: 0925106ea1074abf5d0f3dff0740cc697744e23e63422e6acf4da384093c0509

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/9/cell_id; canonical SHA-256: c40af3980cf0bce1f58158f2fcf0cc4bafaceb38f1eabdda409703aecba128ff

rand_notG_C

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/9/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/9/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/9/comparison_ids; canonical SHA-256: 5d71692dc401ae12e982281e59dba58584b1416a9e3ba7a8e09cc2565e5d5c16

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/9/comparison_ids/0; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/9/comparison_ids/1; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/9/note; canonical SHA-256: 1d33a0aef58282c50293c716c7f92aa5ad630d7bc475f1a46f4ff1f44a21f9dc

q2 lower unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/9/predicate; canonical SHA-256: aced41da99d89f488e01e555f3f1e3b336bfd111ca44affd4fd34b1457b5d6ff

randomized; Delta>0,M_k>0; not G and C

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/9/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/9/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/9/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 11

Native pointer: /joint_analysis/domain_map/cells/10; canonical SHA-256: 773e33a5c658758014c6c20092280f0b6275dbc5e2e02aa2a915454083216141

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/10/cell_id; canonical SHA-256: 6658968b9208768b4e0bd132f6e8ac0c75b67f27a23b94d068b179cd161a41e4

rand_notG_rest

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/10/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/10/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/10/comparison_ids; canonical SHA-256: 15eb274742572d5f35ce6ef90578fec1600898ce81d09b55f5136631e0c91184

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/10/comparison_ids/0; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/10/note; canonical SHA-256: 1d33a0aef58282c50293c716c7f92aa5ad630d7bc475f1a46f4ff1f44a21f9dc

q2 lower unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/10/predicate; canonical SHA-256: f8bec02741c401df3e4c55cf7a99dfba9eaef9facc058425b82a0963bca2bf68

randomized; Delta>0,M_k>0; not G and not C

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/10/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/10/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/10/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 12

Native pointer: /joint_analysis/domain_map/cells/11; canonical SHA-256: 26b89a9630962838c2d97010ca10f2c8fe7be4a80bc6fc5a586d0fcfa63d3974

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/11/cell_id; canonical SHA-256: e4199567daf88d9024d9fea029874cbf8e6c8c0552e5fd1e2cff32a6967fe2a1

rand_J_retained_q1

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/11/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/11/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/11/comparison_ids; canonical SHA-256: de0ec271d10a9ee0b879f424964cc7c492775702db9d9fda878dc0d4803a6da8

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/11/comparison_ids/0; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/11/note; canonical SHA-256: 18e47172aed834aa5e8fe01b40b66eadcf5571fcce0036636ea453590b049e78

Separate retained q1 layer on the same parameter region; its old optimal native bracket is conditionally retained, not inferred from q2. No new q1 source recertification is claimed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/11/predicate; canonical SHA-256: 204705ee4a635def61a5274b7d00100c188b7398b2171e2dcc30911ad88b1d85

Randomizedq1 only; Delta>0,M_k>0; exact nativeJ.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/11/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/11/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/11/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: b2a60e283e81e972301c07f4b716f3697377a8d9a15b940dcce7909680eb36a3

Delta=0, Delta>0 with M_k=0, and Delta>0 with M_k>0 partition the parameter domain. H/not H and C/not C partition the deterministic positive branch. Since J implies G and not C, the five randomized positive cells are disjoint and exhaustive. Comparison overlap does not combine distinct quantities or views. The additional rand_J_retained_q1 is an explicitly separate quantity layer on J, not a new parameter cell or a q1/q2 identity. rand_J now carries the independently published q2 closure.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 365c9288e414cfa96ca7476a684a36cd2ca4c6602647212e8ad1e05381608866

No parameter tuple for deterministic q1 or randomized q2 is omitted by these cells, but missing-lower cells remain scientifically unassessed. Randomized q1 outside J and dormant deterministic q2 remain unassessed; no quantity equivalence is asserted.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 64abd61109d0fe9a4c2e87631f1fcdaa30aa70946c2c1d6b6671a239dec2f971

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 5c3c40b9d0e145d684d66487881abbc9c25a3bced42fdeb14e55a2c06800b7e6

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: ade1df3f266d712b1111b3fa35ab092721fe71cb66c5c9a9f2bf8d3ed048fa0d

n=1 source lower, gradient necessity and flat padding. Gap O_k(1+B/(1+A)) can still diverge.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 5d71692dc401ae12e982281e59dba58584b1416a9e3ba7a8e09cc2565e5d5c16

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: e4a19f45efc5697b5cf0d5a35559ff8ea2838ce3a6c723119838c1088e755760

F_RANDOMIZED_GRADIENT

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 107e3cf50a36c5f8da0f6b4702d938312aca46424e9ab5d3f3cbe4c302b4e6ad

G in c4; G intersect C in c2; newly tight on fixed-ratio B<=C_0 A.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 1e0fdc883ae7dacc75525bd41365e31a49ad5a3c1a9affd2aa90e456dbf9a3b8

Same upper; lower Omega_k(1+A) on G.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: b0dc41bc430ec554ee7e6f616762fc10e14986b3cc9c665e91a01a318b31a3d5

q2 upper O_k(1+A+B); lower unrecorded.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: a0e01d1b0e4d9db140b76ba744ab970a61996218896279d4f0fa7a25e5bb6008

Outside G and all old q1 brackets.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: bd6037b58d6164df5366bd8308c7f04bc5fbb84f9ffc5a475050fb5f5a93a081

Delta>0, M_k>0, A>=C_k, d>=C_k(1+A)log(3+A)

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 0e956236e672bfecdc82c17b36da70c6a092dbb1e6a472144d4229b069bc862b

k=3,Delta=M_k=1,epsilon_g=t^(-3/4),epsilon_H=t^(-1): A=t,B=t^2, with d>=C_k(1+t)log(3+t), yields a growing q2 lower in the curvature branch.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: aab54456c55f9fdb4f53c7065b472ef655b8aa1c3ee95e62eb51da80cd6e76d8

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 78d76eda77b891426588425e33d44f321f41665bbf65e92424ac91b2ab4891f8

The explicit regularized polynomial solver costs one jet; indistinguishability excludes zero jets.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: ef02682616ea514f980153b8c63f1710025d6b2285fc65371f2a62ef9a33c69e

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: d116cf26231ca5cae965ceb2af43072595d07026b790e2e5c34701a3d532e4e0

#### Native field: new_domain

Native pointer: /joint_analysis/impact/1/extension_witness/new_domain; canonical SHA-256: 669290ef6f82d791668e4411f81bd7686141a93795da1d3e87e35243e8e86d83

Delta>0, M_k=0, d>=1, fixed k>=2, epsilon_g,epsilon_H>0, in deterministic q1 and randomized q2 separately.

#### Native field: old_domain

Native pointer: /joint_analysis/impact/1/extension_witness/old_domain; canonical SHA-256: 5b55667cf779b25e6435f79beeff624467291d27f875461fbe1547cd7a801559

Union of the eight preceding registered comparison predicates with their retained admissibility/source guards: Delta=0 endpoints, positive-modulus branches, large-workload/dimension branches, and B>C0*A curvature branches.

#### Native field: outside_old_argument

Native pointer: /joint_analysis/impact/1/extension_witness/outside_old_argument; canonical SHA-256: 4eb95c4d1ee17ce5ace6cdc43dad07d58fda83a62c3c11922eb4dd4392b08682

These quadratics have initialization gap 1, are bounded below, and have zero kth-derivative Lipschitz modulus, so the original HO_POLYNOMIAL_ONE_CALL construction places this tuple in both new exact-one branches. The old zero-gap predicates require Delta=0; the broad old positive branches require M_k>0; the old deterministic large-workload and randomized gradient-dominated windows require max(A,B)>=C_k or A>=C_k with C_k>0; and the residual curvature predicates require k>=3 and B>C0*A, both false here. Thus this legal tuple lies outside every preceding registered predicate even before any further source guard. This is a strict extension of the registered domain, not a claim of a new positive-modulus frontier or necessity of a saturation threshold.

#### Native field: outside_old_witness

Native pointer: /joint_analysis/impact/1/extension_witness/outside_old_witness; canonical SHA-256: 0b04674c027d26555cf7c1356ca5091b3a45d0a614b8f91c245ee02ac575480e

d=1, k=2, Delta=1, M_k=0, epsilon_g=epsilon_H=1; hence A=B=0. Take x0=0 and the original proof quadratics f_±(x)=(x∓sqrt(2))^2/2.

#### Native field: proof_refs

Native pointer: /joint_analysis/impact/1/extension_witness/proof_refs; canonical SHA-256: 546bf492c7b9c11ee35f16a724f801d7db6db5ded029f06e1ba4133311cba323

#### Native item 1

Native pointer: /joint_analysis/impact/1/extension_witness/proof_refs/0; canonical SHA-256: 5b135968819c938cbd625b7cdc79942df0278dac868fc6a40d0104866c264c2b

HO_POLYNOMIAL_ONE_CALL

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 58af990bebff89aca28ace7f8aa4692eab3dbabd481ef5958c9f02bb7a4697a2

F_POLYNOMIAL_ONE_CALL

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: fb4de890e92bf9a6471ed92283e235879fd1c7ded036d213ef261a134dbc3efc

Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: 6c09510eb937226bbc6ce35656f44dccd8607964af9f29cac4e5cd5bd9bdc3c4

domain_extension

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 25baa78187c0be75a537245e7373513ef5bd56391074b415eaa5c665aac76fd8

Exact upper=lower=1.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 4128385608b2b00add70be1c3e2ea57751880e42a3680dd096a0f4ecd1f66dcd

No registered positive-gap zero-modulus branch.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 79b799aa850bd3cc7e834522638266fc876b3d7fe2e33b7c55b1fbfde45f44fc

Delta=0 remains zero; all M_k>0 rates.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: fb4de890e92bf9a6471ed92283e235879fd1c7ded036d213ef261a134dbc3efc

Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 8466426cf44f3d0319ccad8cda52b7f4e0cf555ca10573784c3e26cdbba5637e

Two quadratics with lambda>epsilon_g^2/(2Delta) have disjoint success balls.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 335006acc856ee7afb265fbf88bd78f73485cd9f68b8dfdd713a3445f3460507

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 3fdbfe170de7b8381fc785cf13a6448bb3444b565ab72a22ae9ac1b8f4093e1d

Restrict the frozen b6 premise without enlarging its validity or recertifying dependencies.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: dce8a51ee099458d423546d9d720bac514748aa64e751a15c9cfddb03e3411ac

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 46a93a3afcfb0059fbb183d5d06c657429bab68b1b462dd72e04a1bf326ffd15

F_GUARDED_DETERMINISTIC

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 27b172663d1f0144402799d0519c09e195ff13b2ec0ce8f5e91583b55cabdbb8

No new global inequality; omitted overlap representation filled.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 842f9125967482b313c33b4d36aadd0cbeae62b2d1d3ced03067fb6166b4f785

Expose b6 in c3/c4 only on intersections with H.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 8f612903d6b1b6beb29c8c805719aa866f03206a2edbb6bddf7116e6a91dcfe7

c3/c4 lower unreferenced; c1 already records b6 on H.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 569f7bfe3038f1294e8a03cc3f85f13fd28b2afbce1f1ff897a5860922ef7536

Every retained bound and the complement of H.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 8617ad41723577bf854b67a091cc988e0c2a4f20f9f7a266596f70fc2d73ad02

Delta>0, M_k>0, max(A,B)>=C_k, d>=C_k(1+A+B)

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: d1bbfcf760b2f144b53c1ebff36410e4c0577c6c095715a56e266f7c0feea97d

Every point in c3 intersect H already belongs to c1.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 9cda0f4f5ce9669585409165339001a781890277c67e2c4dc757a71fa02af73a

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 0f89c38f8b4e8d7aa96778524fe08a6976bb02e95ec6165078dfdd81d4e92a5f

Presentation only; separate findings support all scientific edits.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: a67a3d924edc23e2c4790590b833585008a4a36774249f65d3602ecca66abc0c

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 4

Native pointer: /joint_analysis/impact/3/comparison_ids/3; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 9720753df3c4284d1ac4a3332fde7c84d239ccfef073443ac14c0f98e7bae8a9

F_FIRST_JOINT_ANNOTATION

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 45f1160f7272623c213cff5e47fa967191c639d6175a43417f9298408bb4eb84

None.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 180de809095bd90b7fa0d6f93b5c8fff354f055effa990fe75d43d272613e17d

Same inequalities with explicit joint-domain bookkeeping.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: fbe8b71bae6b7d359a9b622aa83e62553cdc7c56901435ca7323c449d3c74ad8

Frozen native brackets.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 717359d15ad29435e08f9ebee93d8f2fa324dd2101dfb8386fa3cb9392a7671a

All four preserved comparisons.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 09dabe532fbaded7413555622da7702318f7ca64f5a2e66dddc920d50c648b41

Original comparison guards.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: dabf40209c7d1782dd2a288d779534e622317d4d4eab38953a7a2d72c3f0d51c

Zero-gap costs remain zero and c1 rates keep their guards.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: fac09fa89a20659bd7ae529dd0577df93e1c33e87b9b3601c200529b98de2d48

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 5685228524fc62ef3e1f7a497d0520cda82c51e68597d194385620feac643735

No sharper term found in this source check; retain old conversions conditionally.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 01548117f8500884cd27f67a42364ae77986d17b1b0eb594a1d2883c7a291d96

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 3

Native pointer: /joint_analysis/impact/4/comparison_ids/2; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 4

Native pointer: /joint_analysis/impact/4/comparison_ids/3; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 5

Native pointer: /joint_analysis/impact/4/comparison_ids/4; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 6

Native pointer: /joint_analysis/impact/4/comparison_ids/5; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: 1dc4c29a123e590e07157f5af799cb07fdafd1ed1e252bf46dc1d61ae172461f

F_UPPER_SCREEN

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 45f1160f7272623c213cff5e47fa967191c639d6175a43417f9298408bb4eb84

None.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 708547349ce0f9a12c337fbb292b1315175f9c4e281340a370680fea68b1b5a5

Same.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: 106f218fc0c7e84139efd619c773d38f18c1a784167fa9b5899d6b2ddbbf07bc

O_k(1+A+B).

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 7bf57a435423dc4acc7f54345d148edfbea54e30c9db8d2fc109ec86b6f46af7

All old upper envelopes.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: a7d0e12c6acfa1211c5a3f637d12ac3be36bddd295b2387f9d45ae7d455a7b8d

Delta>0, M_k>0, d>=1, epsilon_g,epsilon_H>0

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 52809be50b02b3613ee612dd0a7b897861da7616590ca400aaa64a5d6f4b2f39

Theorem 3.6 has the same two tolerance exponents.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: a293dd4f99c8f766b17a15a5c32a407ad695975712752a05ba631f2f448005fa

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: 8f90166ee02b7f90a3f36e592e4a51751a97f6ae6770c1a933ed8ff756a86c32

The separate deterministic construction is not automatically excluded; it remains pending.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: 5d71692dc401ae12e982281e59dba58584b1416a9e3ba7a8e09cc2565e5d5c16

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 2

Native pointer: /joint_analysis/impact/5/comparison_ids/1; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: 596ac5442dfde61c855113dcb239a67c9a2e7182e6e54c38c99ab56e7a42ec64

F_STOCHASTIC_SCREEN

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/5/improvement_region; canonical SHA-256: 45f1160f7272623c213cff5e47fa967191c639d6175a43417f9298408bb4eb84

None.

#### Native field: kind

Native pointer: /joint_analysis/impact/5/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/5/new_envelope; canonical SHA-256: 2a522e3a4451eca87c23b8a77e83b1a879cd1c4e17303d55746fb34ae5878216

No stochastic theorem adopted.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/5/old_envelope; canonical SHA-256: bf8a11be2e48a796d2c3639a3ec35c06e187ec6d8605d92ea73f0e7bf5d1e5c2

Exact-jet target brackets.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/5/unchanged_region; canonical SHA-256: 7c083e897db84c08dabecdeb0cc24fbcb4552887158201cb7195a2c7753afc86

All native target bounds.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: f9ef97af3ffb4c154cf902f2913cd5003a675fc35f29245fc54897499027f520

Direct theorem is outside the target oracle contract.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: 1c473ecbf7ff11ccf795da630a429e27851c0ed31a65d98f5daa990cfdb7dcbe

The oracle includes reusable stochastic samples and stops at order two.

#### Native item 7

Native pointer: /joint_analysis/impact/6; canonical SHA-256: 06ea94b632723e28c54c175bfb5662b3456da1d1849eb8266eb0cc16ddc22229

#### Native field: argument

Native pointer: /joint_analysis/impact/6/argument; canonical SHA-256: cd6be459c95a7cb052c0e6513e22d459259cb21cc81482807bce2577baff285e

This proof is specifically for the unchanged randomized q2/g1 complete-k-jet scalar-cost contract. Retain the exact existing b1 upper C_k(1+A+B): its quantity_refs explicitly include q2 and it was already adopted in q2 c2/c4. Thus it is an upper for one actual complete algorithm controlling BOTH gradient and Hessian at the SAME output, not an upper obtained by merging q1 and q2 labels or combining algorithms. All initialization, next-point checks and actual full-jet responses are included in its original fixed-path cap; global known-model computations remain free only as allowed by the unchanged model. The independent source-based b5 lower is already a native q2 statement. HO_RANDOMIZED_GRADIENT_TRANSFER uses source Definition3.1/Theorems3.2/3.4 with n1,p=k,Lp=M_k,epsilon=epsilon_g: an algorithm meeting simultaneous gradient/Hessian accuracy with probability>=2/3 necessarily meets gradient accuracy with that probability, for everyepsilon_H>0. The source hard class obeys the same bounded-below initialgap and Lipschitz D^k budget, without adding lower-order regularity. For its harddimension d0<=C_k(1+A)log(3+A), pad h by f(z,w)=h(z). Each arbitrary adaptive target query projects to exactly one source completejet query; dummy derivatives vanish, the remaining tensors agree, and their operator-norm Lipschitz bound and initialgap are unchanged. Project the final arbitrary/unqueried output; targetsuccess implies sourcegradient success. Private randomness, fixedpathcap and per-instance successquantifier are preserved, so every targetalgorithm has cap>=c_k(1+A) on G={Delta>0,M_k>0,A>=C_k,d>=C_k(1+A)log(3+A)}. This is the recorded conservative source guard, including all k-only workload/dimension constants; no lower beyond G is adopted. Now restrict to J=G intersect{B<=C0*A}, with fixed k>=2 and a fixed finite public window constant C0>0 chosen independently of the five native joint parameters. Since 1+A+B<=1+(1+C0)A<=(1+C0)(1+A), the exact q2 envelope obeys c_k(1+A)<=q2*<=C_k(1+C0)(1+A). Hence Theta_{k,C0}(1+A) on J, with a constant ratio independent of d,Delta,M_k,epsilon_g,epsilon_H. C0 is solely a comparison-window constant: it is not an objective smoothness budget, is not substituted by the varying valueB/A, and its dependence is explicitly declared at this comparison. q2's global quantity metadata remains unchanged; this regional result does not assert globally uniform C0-independent optimality. Both B=C0*A and A=C_k are included subject to the sufficiently-large sourceconstant. Positive Delta,M_k and sufficientdimension remain mandatory; zero-gap and polynomial branches are separate. Outside J, especially when B/A grows or outside G, the old q2 comparisons remain unclosed. The old optimal q1 c1 is a distinct registered quantity and is not the publication certificate for q2. This is native publication of the matching consequence already stated in F_RANDOMIZED_GRADIENT and the old boundary ledger, not a new paper lower bound, a new algorithm, or a new blind discovery. No fresh source verification or prior read/approval credit is claimed by this curator proof.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/6/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/6/comparison_ids; canonical SHA-256: d457fad487720d395854f89f50e560a04be8612c5a34fe9044e38db7b14e0519

#### Native item 1

Native pointer: /joint_analysis/impact/6/comparison_ids/0; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/6/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/6/finding_id; canonical SHA-256: 0ac712d55e0da52c51f2f70597e5710b23fea55bef7e528a4df96d153095d763

HON_Q2_J_NATIVE_CLOSURE_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/6/improvement_region; canonical SHA-256: f2952dd9c729dd7b29fd68326010cbba327d8785878917ff3883edaf0f513c50

Native publication of an already-proved local envelope consequence; no new main-rate inequality or certified-domain expansion.

#### Native field: kind

Native pointer: /joint_analysis/impact/6/kind; canonical SHA-256: 7249f099445029410a160bddb6fd935004aff56d921f462672a9f41815a78001

explicit_region_registration

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/6/new_envelope; canonical SHA-256: e751cf2cac6587d5ee1965e66a4220ff0f78e4d9c5ab47ee0c431adaf618e4b8

Independent q2 optimal comparison on J with Theta_{k,C0}(1+A).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/6/old_envelope; canonical SHA-256: f79227c46eb0926f2ad0f78a55da9cae40a424da01422060fc47fe7b9e29af74

The q2 G lower and global upper already stated the matching J consequence, but only distinctq1 c1 was nativeoptimal there.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/6/unchanged_region; canonical SHA-256: 19c63e53558f424b1708a2c28fab9c99305a12251f16250e7b90d9c63af5b6e2

All ten old comparison objects/statuses, sourceG guards and positive/fine/complement pending limitations.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/6/validity_region; canonical SHA-256: c5ddf84c7d7d4477a8a84f43536bc273bcbaaf8569ccbb77fe43d65213ff5675

Exact positive-modulus G intersect{B<=C0A}, fixedk and fixedpositiveC0.

#### Native field: witness

Native pointer: /joint_analysis/impact/6/witness; canonical SHA-256: 3d52ef3c0b7a955062106063df5dac303981dcd70c254f63d9a5c4040eb23020

The retained full-jet simultaneous upper and nativeq2 gradient-necessity lower have constant ratio on J for each fixedC0.

#### Native item 8

Native pointer: /joint_analysis/impact/7; canonical SHA-256: 1e526b466f6cebce5bee23832aa9e7f8501c024730c963da5c1a5a8f5b42b01c

#### Native field: argument

Native pointer: /joint_analysis/impact/7/argument; canonical SHA-256: a4d801099771a0f2d76a3e663209b087b66e2f37111e4f8290c9840bd08c0f29

Publish a separately proved native randomized q2/J bracket using the retained actual q2 upper and q2 lower with their exact guards and a fixed preselected C0; preserve the old unclosed q2 comparison. The source paper is read afresh and the new combination is explicitly analyst derived. No literature completeness is claimed. Operational read priority after the preserved incomplete 40-tool review: finish the full prepared joint_analysis first, read exact decisive baseline parent objects completely where useful, and finish all evidence/resource/proof objects required by the review pack. Forty-eight tool calls allow completion of the same strict source, exact-reference, prepared-hash and six-check gates; no prior reading or approval is imported. Explicit prepared obligations include /evidence/11, /evidence/12, /resource_projections/0, /proofs/7 and /comparisons/10, with their current exact hashes in the review pack.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/7/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/7/comparison_ids; canonical SHA-256: 25f62ba9147f3ae6c831da33eeded1471abea5da855d3ee23692e4ea3cc43a28

#### Native item 1

Native pointer: /joint_analysis/impact/7/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/7/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/impact/7/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/impact/7/comparison_ids/3; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/impact/7/comparison_ids/4; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 6

Native pointer: /joint_analysis/impact/7/comparison_ids/5; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 7

Native pointer: /joint_analysis/impact/7/comparison_ids/6; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native item 8

Native pointer: /joint_analysis/impact/7/comparison_ids/7; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native item 9

Native pointer: /joint_analysis/impact/7/comparison_ids/8; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 10

Native pointer: /joint_analysis/impact/7/comparison_ids/9; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native item 11

Native pointer: /joint_analysis/impact/7/comparison_ids/10; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/7/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/7/finding_id; canonical SHA-256: 7389272f531e1b7cd8a6f92a820e778110d67bab20525d0e26e15f8071fbce1a

curated_feedback_SO_HO_HON05_S_20261116_7aeb3b9408

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/7/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/7/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/7/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/7/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/7/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/7/validity_region; canonical SHA-256: 7ba2eb95fcd0502d92ac06f4b8546b20c171f06bc8372091dc709644ad5b42be

d>=1 integer, Delta>=0,M_k>=0,epsilon_g>0,epsilon_H>0, fixed k>=2. Separate deterministic q1/g1 and randomized q1 or q2/g1 fixed-path full-jet minimax costs; no quantity IDs merged. On the positive branch define H={Delta>0, M_k>0, max(A,B)>=C_k, d>=C_k(1+A+B)}, G={Delta>0, M_k>0, A>=C_k, d>=C_k(1+A)log(3+A)}, C={k>=3 and B>C_0 A}, J=G intersect {B<=C_0 A}. C_k denotes a sufficiently large unspecified k-only proof constant. Randomized q1 is assessed on its registered J window; dormant deterministic q2 is excluded.

#### Native field: witness

Native pointer: /joint_analysis/impact/7/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 1bccfb1e541fb772cf4e3b164e70576d35659b7b3d53d0fdd8191f30ac9ffe33

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: da84e6401129bbd4a68d323cfe422a826809eab30c2b6cc9f0bd90c5fbb57aba

Reviewer must independently read prepared analysis, changed claims, decisive frozen premises and arXiv:2609.28202v2 Definition 3.1/Theorems 3.2 and 3.4.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 76b4feab956a6bdaedfb3989ef58b65a4a8b4947818a6ad8036f97d14b761566

arXiv:2610.16832v2 Section 6.1 deterministic curvature transfer: higher-order regularity, uniform scaling, dimension and complete-jet robustness remain unread/unproved; no adoption.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 21025226cc3a6925841a72b3d01807e61c8aff4eabad4e703f7b85709daf6119

Low-dimensional positive-modulus rates and possible saturation remain unassessed in the marked missing-lower regions.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 8a26a7bcda61a7d4d48e2ee27263a23763953c92c56a2a2de663a0f978b23edf

Dormant deterministic q2 has empty tracked/fixed metadata; its b2/b3 are not adopted into q1. Any future transfer or normalization needs separate exact-premise review.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 2487ee44afece63c92e4754a807a6ff4770d93d5db77e7445ba03d2a74798ca3

Randomized q1 outside its registered fixed-ratio window is unassessed; q2 results do not automatically relabel q1.

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: b56583d96053a6da59b461fdf3534635dea9cff8f4a11c97e8f4bcc62d181b83

Assess resource_projection for SO_HO_HON05_S__randomized__c1 and SO_HO_HON05_S__randomized__b5

#### Native item 7

Native pointer: /joint_analysis/pending_obligations/6; canonical SHA-256: 54a9474e45dd39ff8830deb83c3df639137374ba3f3433819a4c5c9b494ed193

Assess resource_projection for SO_HO_HON05_S__randomized__c1 and SO_HO_HON05_S__randomized__b6

#### Native item 8

Native pointer: /joint_analysis/pending_obligations/7; canonical SHA-256: b7f61692d68897762d151ac9302129477b8f366a0f0442d993efe79cd177fe40

Assess resource_projection for SO_HO_HON05_S__randomized__c1 and SO_HO_HON05_S__randomized__b7

#### Native item 9

Native pointer: /joint_analysis/pending_obligations/8; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: c7e2ed30b8a9d3ae7e2a53bb9e33c80e382f1507a2235f3904ba9814d6889f87

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 8d8d136ba3c6d5392ef87a9e8af0cec149f9ad17f2948e1958bec36692559d01

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: ff156402cf7bd52cad944cc034dc4666caa99ec0ed606016b2ecdd5f2454dc06

SO_HO_HON05_S__deterministic__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: bb533ecf6b28ad759f9a44d5bea9a8dac0a16e363bcfaf25c0f55ca12a287116

Same q1; restrict to comparison intersections with r3.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 04367c4dfeb7b660e5bbe6e930a4b60ef683f13602af782f9612aef3f004c24e

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: 5c838c9222ed7e14352894f930a52856809a507366388e4d79809ddc2757def8

HO_CURVATURE_LOWER

#### Native item 2

Native pointer: /joint_analysis/provenance/0/proof_refs/1; canonical SHA-256: 18d60db987286d34cea63943c53af3776cd00c08daea4dfe2ae38e36f8e9e7b8

HO_MULTI_REGULARITY

#### Native item 3

Native pointer: /joint_analysis/provenance/0/proof_refs/2; canonical SHA-256: f77592dbde85797058a609134cf6afa9d4f50a25d239219c1b47d5fb0ae1b70f

HO_REGULARIZED_DESCENT

#### Native item 4

Native pointer: /joint_analysis/provenance/0/proof_refs/3; canonical SHA-256: 73b4b43ffce5977ca7f83f6bbc55284b3cc3bc822ca8a821063dcc21f2ab0953

HO_GUARDED_ENVELOPE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 682770d0a3147e6323f6f0d0c037700715de55150d0a814cd10a0b282b5922e3

$\max{A,B}\ge C_k,d\ge C_k(1+A+B)$

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 140238e855a54af8db4e5b749a7c6caccd7be3583ae4215dbf95fb4c92558b2d

Frozen /bounds/5; conditional retention.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 869fff36721d2345cb52301e03aabe5754ba40f0de62c03cde98da722d649a9b

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: ac6dd1b02df088d679c11f24fd967e6bc3a6fefe41b8f97ad031240bf53ecf73

SO_SRC_2978ef8b062af3ec

#### Native item 2

Native pointer: /joint_analysis/provenance/0/source_refs/1; canonical SHA-256: 4357b5ed22937b6d7a411160f76ce347226d931b770445ee6f389ebec7160aff

SO_SRC_52acb46387420698

#### Native item 3

Native pointer: /joint_analysis/provenance/0/source_refs/2; canonical SHA-256: b94d81bf8d0c218567bc0a6900a7fbcd503a6f25e62a5102d46c6a24052a07e5

SO_SRC_6948bf8f8c23676c

#### Native item 4

Native pointer: /joint_analysis/provenance/0/source_refs/3; canonical SHA-256: 72f15b8b51b86b83c82b097c98a0a6c4aa505de1d08d26c605f0d9991df84f11

SO_SRC_b954002f48cd0141

#### Native item 5

Native pointer: /joint_analysis/provenance/0/source_refs/4; canonical SHA-256: f00c6d5c7d3d9705d8ad04d097f84e286c0b36be79f0bbe0a88cf04768e32dc9

SO_SRC_3400224028061741

#### Native item 6

Native pointer: /joint_analysis/provenance/0/source_refs/5; canonical SHA-256: 33f8e9246608380d16d457cc4ac626e35b03c98b4cf8bc3c5ae53c6a8e14dd47

SO_SRC_8b820eaa5c1d7163

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 682770d0a3147e6323f6f0d0c037700715de55150d0a814cd10a0b282b5922e3

$\max{A,B}\ge C_k,d\ge C_k(1+A+B)$

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: d8368b9e3982bf12f80c9fb6ee411d662bf00876dbbb31215a2184746a7883f0

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: dd1718af8c817825a52383772d81b22b7ba40c8ce744c8422cc3647f6aaa87fc

Gradient necessity; n=1,p=k,L_p=M_k,epsilon=epsilon_g; equal-cost flat padding.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: ede9164e34fb157c4f3376d7721f7e47b8b07e22a23dc384c0fd8f471be26298

subclass_transfer

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 8e47a3ee60869f18447621d8dccf7f5d793f180b25199fddd4f17f98d5168f03

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 870e4304ff412f84a5969428876cde72a3db0d2b5cc7e6c090fbddd18d7e6899

HO_RANDOMIZED_GRADIENT_TRANSFER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 62d8a034389f3d34b96347558dfcb09aa324e4984fd50e0462bb925b8c828cd8

n=1 first-order full-jet class, fixed p=k, positive Delta,L_p,epsilon.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 3c20c318b9f5e39a051058bed78d1de3ba96acc7dcb02647047d40fd567a49f2

arXiv:2609.28202v2, Def.3.1/Thms.3.2,3.4, pp.5-6, chars13323-16400; SHA256 5129c1f6b8ae94f321c0541890578a5ef396ec08583340160ed877699bae11f9

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: dc5d469fadf73e33fd68f2487cb4b113858021a2860465254054003c8ee1b39d

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: 6a3493c431ca82e403f1a150922292adb3e5dcfbadc754d48d4009587db48498

SO_SRC_dbd0fbd46018f76e

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: bd6037b58d6164df5366bd8308c7f04bc5fbb84f9ffc5a475050fb5f5a93a081

Delta>0, M_k>0, A>=C_k, d>=C_k(1+A)log(3+A)

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 1a64537efa67dc32e7a38e1c0e210947ca8d22e448d422207b0f0edcdd61e642

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: fe7c7024f45b198e26447fc97d7ba7895ce8f92b9706eaf81f35e93a2c05968b

SO_HO_HON05_S__deterministic__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: e03e4bc6bf931fe79621c45025e54405b00d5314fdb15208e341b8fdb9423c27

Exact polynomial recovery and regularized minimization; disjoint quadratic output sets.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 546bf492c7b9c11ee35f16a724f801d7db6db5ded029f06e1ba4133311cba323

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: 5b135968819c938cbd625b7cdc79942df0278dac868fc6a40d0104866c264c2b

HO_POLYNOMIAL_ONE_CALL

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: fb4de890e92bf9a6471ed92283e235879fd1c7ded036d213ef261a134dbc3efc

Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 00414c6ed2798ca4db256d4f05edadf9404fa59a6924ea153b2f29d98f202360

Frozen /proofs/3, HO_ENDPOINTS; new HO_POLYNOMIAL_ONE_CALL

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: fb4de890e92bf9a6471ed92283e235879fd1c7ded036d213ef261a134dbc3efc

Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: b013f851a90b911cf1176306e393b3ca2e7021c3aee684d7e6c045d6f12faee9

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: e9f21132ad11087e56e3dea5c81bac0db9ed0c6b83d3dd4076fc7e5b59dcc658

SO_HO_HON05_S__deterministic__b8

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: e03e4bc6bf931fe79621c45025e54405b00d5314fdb15208e341b8fdb9423c27

Exact polynomial recovery and regularized minimization; disjoint quadratic output sets.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 546bf492c7b9c11ee35f16a724f801d7db6db5ded029f06e1ba4133311cba323

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: 5b135968819c938cbd625b7cdc79942df0278dac868fc6a40d0104866c264c2b

HO_POLYNOMIAL_ONE_CALL

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: fb4de890e92bf9a6471ed92283e235879fd1c7ded036d213ef261a134dbc3efc

Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 00414c6ed2798ca4db256d4f05edadf9404fa59a6924ea153b2f29d98f202360

Frozen /proofs/3, HO_ENDPOINTS; new HO_POLYNOMIAL_ONE_CALL

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: fb4de890e92bf9a6471ed92283e235879fd1c7ded036d213ef261a134dbc3efc

Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: 8647cbd40a4b49ccd3a8d04f9069a4fc36aa217b643f1606a47eb94fe26e39c6

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: e03e4bc6bf931fe79621c45025e54405b00d5314fdb15208e341b8fdb9423c27

Exact polynomial recovery and regularized minimization; disjoint quadratic output sets.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: 546bf492c7b9c11ee35f16a724f801d7db6db5ded029f06e1ba4133311cba323

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: 5b135968819c938cbd625b7cdc79942df0278dac868fc6a40d0104866c264c2b

HO_POLYNOMIAL_ONE_CALL

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: fb4de890e92bf9a6471ed92283e235879fd1c7ded036d213ef261a134dbc3efc

Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: 00414c6ed2798ca4db256d4f05edadf9404fa59a6924ea153b2f29d98f202360

Frozen /proofs/3, HO_ENDPOINTS; new HO_POLYNOMIAL_ONE_CALL

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: fb4de890e92bf9a6471ed92283e235879fd1c7ded036d213ef261a134dbc3efc

Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: 815b905c8b0b83f6a8a8ee5786df8e9215d58bb5793388a9a602740aebeee400

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: e03e4bc6bf931fe79621c45025e54405b00d5314fdb15208e341b8fdb9423c27

Exact polynomial recovery and regularized minimization; disjoint quadratic output sets.

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 546bf492c7b9c11ee35f16a724f801d7db6db5ded029f06e1ba4133311cba323

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: 5b135968819c938cbd625b7cdc79942df0278dac868fc6a40d0104866c264c2b

HO_POLYNOMIAL_ONE_CALL

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: fb4de890e92bf9a6471ed92283e235879fd1c7ded036d213ef261a134dbc3efc

Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: 00414c6ed2798ca4db256d4f05edadf9404fa59a6924ea153b2f29d98f202360

Frozen /proofs/3, HO_ENDPOINTS; new HO_POLYNOMIAL_ONE_CALL

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: fb4de890e92bf9a6471ed92283e235879fd1c7ded036d213ef261a134dbc3efc

Delta>0, M_k=0 (d>=1, fixed k>=2, epsilon_g,epsilon_H>0)

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: f36beb190ad1d892f0aa2c8f4684888d1d1bc0580986715e2632544540fe75bb

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: 37d5c2bace2e935464d285f96cd520ad4b7d0be5197e7a7de858583a5ca96560

No new algorithm/source theorem: conditionally retain the same full-jet simultaneous upper, and restrict its new selection to J. Algebra with independently proved nativeq2 b5 yields O_{k,C0}(1+A). No q1/q2 identity merger or cross-algorithm coordinate pairing.

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: da7b2749266c1abec3a82da6daac572c52cea8fb9a5704ae67622feef5df1509

#### Native item 1

Native pointer: /joint_analysis/provenance/6/proof_refs/0; canonical SHA-256: fedeaf8a8b4c6dff330975f648fe542d9c163249c8576a514ade49cf95b7cd25

HO_RANDOMIZED_Q2_J_NATIVE_CLOSURE_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: 09269de6a0d5708234f2be9a6e93f3ef91f4daa3a4a8a7e67609bccbe2b043ba

Referenced regions: ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$) AND ($d\ge 1,\Delta>0,M_k>0,\varepsilon_g>0,\varepsilon_H>0$)

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: 25105c2f08122cb980e36931c3c0d7e175969a14a5dbc90a27505af9591a095f

Exact frozen native randomized b1 with explicit q2 quantity_refs and existing q2 c2/c4 adoption; original external source retained conditionally.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: 66d8a480c84ac2f36e0290e245ae5eeda1993cc869766a5d93998f1ccf1e7505

#### Native item 1

Native pointer: /joint_analysis/provenance/6/source_refs/0; canonical SHA-256: 171733dd139abd5b535ef1328a8568e48d23619546fbb8b8210432593281b0c3

SO_SRC_4e3927a01a1d23a9

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: 304cfc38bff46790312d89bb7921feae597eb7bbb44194273e7301694f0294c4

The exact J window and unchanged randomized q2/g1/resource; C0 fixed only as a regional constant.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: e5caee168627dada144c03fb3dd373467a0268705669253dfca287481d77a1b7

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 4042cb031b6647b71ba1ea79ef50623cd0da1aa442f46e319f885b77a6af854b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/5; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/6; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/7; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/8; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/9; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/10; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 591c492b298171ed0956c8b95f612f01e6f2d717b56034e40a2a5ce3fd7ef50a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 8f98a87d7e7e6840d0d9ba3f7f0791c0f4d194adc9456344e093722303359a9b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 8b1c99c7778fbf54038bc63ab4d198341a53188523381f4d798700e4a0918c17

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 61d6cc34a43b958ddf1fa9198bda41fd2e5da92991db3bb8e8c76f8f93f370b7

SO_HO_HON05_S__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 2a2d9c487891eba39d70b19edc7e8d4c537efab3c2d5ea13dd918262cbf29dfe

SO_HO_HON05_S__deterministic__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: f7764d9594dd85e3608e7e028148634ddfb6cc925dd5bfec541d401df669b2cb

SO_HO_HON05_S__deterministic__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: ff156402cf7bd52cad944cc034dc4666caa99ec0ed606016b2ecdd5f2454dc06

SO_HO_HON05_S__deterministic__b6

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/4; canonical SHA-256: fe7c7024f45b198e26447fc97d7ba7895ce8f92b9706eaf81f35e93a2c05968b

SO_HO_HON05_S__deterministic__b7

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/5; canonical SHA-256: e9f21132ad11087e56e3dea5c81bac0db9ed0c6b83d3dd4076fc7e5b59dcc658

SO_HO_HON05_S__deterministic__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 8f92fa835b0a6fb4daf5a8e4e6460bdfe7dbe7998229175f50058af1c2eb906f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: f711ba1b3fda5cbbc401c8a83c28f19a64273f9349a0f471e8fa7203c8cea6c4

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 8b1c99c7778fbf54038bc63ab4d198341a53188523381f4d798700e4a0918c17

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 61d6cc34a43b958ddf1fa9198bda41fd2e5da92991db3bb8e8c76f8f93f370b7

SO_HO_HON05_S__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 2a2d9c487891eba39d70b19edc7e8d4c537efab3c2d5ea13dd918262cbf29dfe

SO_HO_HON05_S__deterministic__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: f7764d9594dd85e3608e7e028148634ddfb6cc925dd5bfec541d401df669b2cb

SO_HO_HON05_S__deterministic__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: ff156402cf7bd52cad944cc034dc4666caa99ec0ed606016b2ecdd5f2454dc06

SO_HO_HON05_S__deterministic__b6

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/4; canonical SHA-256: fe7c7024f45b198e26447fc97d7ba7895ce8f92b9706eaf81f35e93a2c05968b

SO_HO_HON05_S__deterministic__b7

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/5; canonical SHA-256: e9f21132ad11087e56e3dea5c81bac0db9ed0c6b83d3dd4076fc7e5b59dcc658

SO_HO_HON05_S__deterministic__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: d5f7b7fa6d47c7a6718c595b89d1b8e53eb6c983792ac28cf2f7898d1a9c7ec1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 34b2e8d58f95ef48daea99c9821626dcb3f194db3949058fd391fb7e13655303

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 8b1c99c7778fbf54038bc63ab4d198341a53188523381f4d798700e4a0918c17

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: 61d6cc34a43b958ddf1fa9198bda41fd2e5da92991db3bb8e8c76f8f93f370b7

SO_HO_HON05_S__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 2a2d9c487891eba39d70b19edc7e8d4c537efab3c2d5ea13dd918262cbf29dfe

SO_HO_HON05_S__deterministic__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: f7764d9594dd85e3608e7e028148634ddfb6cc925dd5bfec541d401df669b2cb

SO_HO_HON05_S__deterministic__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: ff156402cf7bd52cad944cc034dc4666caa99ec0ed606016b2ecdd5f2454dc06

SO_HO_HON05_S__deterministic__b6

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/4; canonical SHA-256: fe7c7024f45b198e26447fc97d7ba7895ce8f92b9706eaf81f35e93a2c05968b

SO_HO_HON05_S__deterministic__b7

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/5; canonical SHA-256: e9f21132ad11087e56e3dea5c81bac0db9ed0c6b83d3dd4076fc7e5b59dcc658

SO_HO_HON05_S__deterministic__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: e9254c3830af107ea389eed850e9cb9cafbd2c65bfe48ef39035329c2964ed29

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 784d30078dee1929a5b71bf1e6e8e3ea5a0722912345a558dad390db06f5fae5

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 8b1c99c7778fbf54038bc63ab4d198341a53188523381f4d798700e4a0918c17

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: 61d6cc34a43b958ddf1fa9198bda41fd2e5da92991db3bb8e8c76f8f93f370b7

SO_HO_HON05_S__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: 2a2d9c487891eba39d70b19edc7e8d4c537efab3c2d5ea13dd918262cbf29dfe

SO_HO_HON05_S__deterministic__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: f7764d9594dd85e3608e7e028148634ddfb6cc925dd5bfec541d401df669b2cb

SO_HO_HON05_S__deterministic__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/3; canonical SHA-256: ff156402cf7bd52cad944cc034dc4666caa99ec0ed606016b2ecdd5f2454dc06

SO_HO_HON05_S__deterministic__b6

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/4; canonical SHA-256: fe7c7024f45b198e26447fc97d7ba7895ce8f92b9706eaf81f35e93a2c05968b

SO_HO_HON05_S__deterministic__b7

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/5; canonical SHA-256: e9f21132ad11087e56e3dea5c81bac0db9ed0c6b83d3dd4076fc7e5b59dcc658

SO_HO_HON05_S__deterministic__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: a9285299c94468c04bf60e621691bbac290b133bf72d0bb74f7de5bb6c8d03fb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: c82405e7112035e790b5a5793cb6b538ef61747f343a7eb827e0eda0c8c76870

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 8b1c99c7778fbf54038bc63ab4d198341a53188523381f4d798700e4a0918c17

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/0; canonical SHA-256: 61d6cc34a43b958ddf1fa9198bda41fd2e5da92991db3bb8e8c76f8f93f370b7

SO_HO_HON05_S__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/1; canonical SHA-256: 2a2d9c487891eba39d70b19edc7e8d4c537efab3c2d5ea13dd918262cbf29dfe

SO_HO_HON05_S__deterministic__b4

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/2; canonical SHA-256: f7764d9594dd85e3608e7e028148634ddfb6cc925dd5bfec541d401df669b2cb

SO_HO_HON05_S__deterministic__b5

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/3; canonical SHA-256: ff156402cf7bd52cad944cc034dc4666caa99ec0ed606016b2ecdd5f2454dc06

SO_HO_HON05_S__deterministic__b6

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/4; canonical SHA-256: fe7c7024f45b198e26447fc97d7ba7895ce8f92b9706eaf81f35e93a2c05968b

SO_HO_HON05_S__deterministic__b7

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/5; canonical SHA-256: e9f21132ad11087e56e3dea5c81bac0db9ed0c6b83d3dd4076fc7e5b59dcc658

SO_HO_HON05_S__deterministic__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: c2d205c1888a6169ed47bfaa7d0c52df58a233df6e659142a9ab534bc1c43e9c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: b6b7108d57ef22ff5b7f3d2116d4e0f4591716f3d2a8a74f36a23680b92fb9a5

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 0b70be63a1530e7d8e3993ab68c201a309828dc9a661713cb1a3ae860a232305

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/0; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/1; canonical SHA-256: 9b53c78c06e9b16db6e5313a0b8410c6822f44c37d67cbfd441c0eef554c363e

SO_HO_HON05_S__randomized__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: de0ec271d10a9ee0b879f424964cc7c492775702db9d9fda878dc0d4803a6da8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 2410182452f64a5b6f33fb01d2e7743652efde6bfe2aa5b1b886c1d088dcd8a9

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 1293f9b21222262de1167f66fb80a25ff2ddd42a6a975b042cecfd669241be28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/0; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/1; canonical SHA-256: 1d8be8836dfaefd01b9b7c2dac6ee8eff26b1d09206cab8c5a3167795d2f85fa

SO_HO_HON05_S__randomized__b3

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/2; canonical SHA-256: 3fe5491ee1e3a58e6cb01b8f7e813fe1eec87fd1b9a14d727ae0fe55524d78a2

SO_HO_HON05_S__randomized__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/3; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/4; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/5; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: d7ac4f44432065d013c3eddd09d22f25c2ed7114834d2c477c97079fee7324f3

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: b99a79db321ebf0eb8b218c7f1ee4c01d9db5571f5fcd7e273c4238b4f25e248

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 1293f9b21222262de1167f66fb80a25ff2ddd42a6a975b042cecfd669241be28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/0; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/1; canonical SHA-256: 1d8be8836dfaefd01b9b7c2dac6ee8eff26b1d09206cab8c5a3167795d2f85fa

SO_HO_HON05_S__randomized__b3

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/2; canonical SHA-256: 3fe5491ee1e3a58e6cb01b8f7e813fe1eec87fd1b9a14d727ae0fe55524d78a2

SO_HO_HON05_S__randomized__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/3; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/4; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/5; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 7af9d3f82555bfbab3f782f86f2b2d12f705e5492babff709008275ef00a22bd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: f1d7c1b829959acf5fd8b22ab6c75fdbf1b3810e2c3ef78a394693a9a0260546

synthesis-7

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: 7648e994d6aff107ee6f072a1baacb0bffe071b4667cfab21b99792234ceab44

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 1293f9b21222262de1167f66fb80a25ff2ddd42a6a975b042cecfd669241be28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/0; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/1; canonical SHA-256: 1d8be8836dfaefd01b9b7c2dac6ee8eff26b1d09206cab8c5a3167795d2f85fa

SO_HO_HON05_S__randomized__b3

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/2; canonical SHA-256: 3fe5491ee1e3a58e6cb01b8f7e813fe1eec87fd1b9a14d727ae0fe55524d78a2

SO_HO_HON05_S__randomized__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/3; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/4; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/5; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 15eb274742572d5f35ce6ef90578fec1600898ce81d09b55f5136631e0c91184

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 705e1af290021b0ee8b6cac71ead9597d036f83961af1c252c90f4ed8047130f

synthesis-8

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 6f3d90bef3ca1a72a4e3b681f887f3e54ca3df56a9b8ca1ea9b80601d03bb572

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: 1b88e9bb0ca9819b4bbd82cd814e777d50cb36e29e0a0b006bf4d2f476b3a687

The curator proposes the complete original bound-use ledger, including the stated dispositions and guards, plus the explicitly registered existing proof consequence. These are author assertions for fresh independent review, not inherited adoption or certification of the held candidate. Unchanged baseline claims retain only the declared conditional premise.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 1293f9b21222262de1167f66fb80a25ff2ddd42a6a975b042cecfd669241be28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/0; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/1; canonical SHA-256: 1d8be8836dfaefd01b9b7c2dac6ee8eff26b1d09206cab8c5a3167795d2f85fa

SO_HO_HON05_S__randomized__b3

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/2; canonical SHA-256: 3fe5491ee1e3a58e6cb01b8f7e813fe1eec87fd1b9a14d727ae0fe55524d78a2

SO_HO_HON05_S__randomized__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/3; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/4; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/5; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 7ee6bdd07feb3e4f2bd1a0a22b816df64f92074d4b69b841e656ffdd3efa8e2b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: cefa876d80b27bbc26ecd952c430927d231047df60d2c399f9959d4307ecfd70

synthesis-9

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: b6a63b7a172b107ac3993cc834edffc5e7cc2b9372b084c86aab7c455ee6971c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/argument; canonical SHA-256: 9c3e59f954dc5b9e12fede8fc0ff54e347a71f386cfd980adbab71ea601dd64c

Complete newq2J bound-use ledger includes native multi-quantity upperb1 and nativeq2 lowerb5 with exactadoptionguards. Any source/replacement/resource question not previously resolved remains an explicit materiallead. The regional scalarcap is one full algorithm; q1 IDs and independently optimal coordinates are not combined. Full matching proof HO_RANDOMIZED_Q2_J_NATIVE_CLOSURE_20261116

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs; canonical SHA-256: 1293f9b21222262de1167f66fb80a25ff2ddd42a6a975b042cecfd669241be28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/0; canonical SHA-256: d82061d1301c64f46342e36bcbb12cec80ec181beb23f48e41cbc6253068bc52

SO_HO_HON05_S__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/1; canonical SHA-256: 1d8be8836dfaefd01b9b7c2dac6ee8eff26b1d09206cab8c5a3167795d2f85fa

SO_HO_HON05_S__randomized__b3

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/2; canonical SHA-256: 3fe5491ee1e3a58e6cb01b8f7e813fe1eec87fd1b9a14d727ae0fe55524d78a2

SO_HO_HON05_S__randomized__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/3; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/4; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs/5; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: d457fad487720d395854f89f50e560a04be8612c5a34fe9044e38db7b14e0519

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 9cab9589f3334662db7e0a597e42e682e82fc47dc9b49b5f48ad62e4069ce795

synthesis-10

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: f44b4dd24c90a5184abe2b7bf6763d36378b7b0c8d6ae3c0f328a828fc89e8c1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs/0; canonical SHA-256: fedeaf8a8b4c6dff330975f648fe542d9c163249c8576a514ade49cf95b7cd25

HO_RANDOMIZED_Q2_J_NATIVE_CLOSURE_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs/1; canonical SHA-256: 870e4304ff412f84a5969428876cde72a3db0d2b5cc7e6c090fbddd18d7e6899

HO_RANDOMIZED_GRADIENT_TRANSFER

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: 6d06b50e9b35565e1ec1b80b75af8b720ba1df245cb3a99a84424d04a1766b79

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/argument; canonical SHA-256: 54a66eab467db3d40ca6c45ae750e0e0576d631e4d5d8010be0ccc1904086c2b

This directed projection/replacement opportunity needs a separate applicability/cost judgment. Distinct IDs are not merged, and no opposite-direction inference is made.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs; canonical SHA-256: 253bc734a6684a45e34822cd4f8708449e75641237730409055cb938d67e256f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs/0; canonical SHA-256: 59255e0ec759b8e56b49d7b6c288fe02193b2a4671c210059d4c14ea0d742d9c

SO_HO_HON05_S__randomized__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: de0ec271d10a9ee0b879f424964cc7c492775702db9d9fda878dc0d4803a6da8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: feb7b5e13e39ba9c3fd05c25add5ea4e2cecf0c49861217b1b978e57b06145f4

synthesis-11

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: b56583d96053a6da59b461fdf3534635dea9cff8f4a11c97e8f4bcc62d181b83

Assess resource_projection for SO_HO_HON05_S__randomized__c1 and SO_HO_HON05_S__randomized__b5

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/obligations/12; canonical SHA-256: 4c25d4e441b4a5ddc37d487aa68303ce45c2ecc0c3d8356fd256bc7f5746fbae

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/argument; canonical SHA-256: 54a66eab467db3d40ca6c45ae750e0e0576d631e4d5d8010be0ccc1904086c2b

This directed projection/replacement opportunity needs a separate applicability/cost judgment. Distinct IDs are not merged, and no opposite-direction inference is made.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs; canonical SHA-256: 4dc32143bfe6cdb10313fd781c29902a517aa07dc0c7cafbd5ebcd220600bd1e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs/0; canonical SHA-256: 340e40bac9514f3b354282eb127a91cad888f0434df8482a2f7c77e149b26897

SO_HO_HON05_S__randomized__b6

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids; canonical SHA-256: de0ec271d10a9ee0b879f424964cc7c492775702db9d9fda878dc0d4803a6da8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/0; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/id; canonical SHA-256: 2882ec2161c3f82fe99edd536675194d9cab7af971ea8f7b2000e93fc92f51a3

synthesis-12

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/lead; canonical SHA-256: 54a9474e45dd39ff8830deb83c3df639137374ba3f3433819a4c5c9b494ed193

Assess resource_projection for SO_HO_HON05_S__randomized__c1 and SO_HO_HON05_S__randomized__b6

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 14

Native pointer: /joint_analysis/synthesis_coverage/obligations/13; canonical SHA-256: cef8583747ba7a7365af5836946e10d4348c538d8039cbaf4c514fab18c25c9d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/argument; canonical SHA-256: 54a66eab467db3d40ca6c45ae750e0e0576d631e4d5d8010be0ccc1904086c2b

This directed projection/replacement opportunity needs a separate applicability/cost judgment. Distinct IDs are not merged, and no opposite-direction inference is made.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs; canonical SHA-256: 4f084142a68f217a9f091e04743d331b8f295137a37622905af8e5190f8578c6

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs/0; canonical SHA-256: de63c0e05edeeab75b5c89e5b340c5b6fbd523a38190e3834b021eec1f219cea

SO_HO_HON05_S__randomized__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids; canonical SHA-256: de0ec271d10a9ee0b879f424964cc7c492775702db9d9fda878dc0d4803a6da8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/0; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/id; canonical SHA-256: 6e1f748f3b3ba34e115027c6b98663cae9101a61cf4f66864ed75f96fa708e34

synthesis-13

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/lead; canonical SHA-256: b7f61692d68897762d151ac9302129477b8f366a0f0442d993efe79cd177fe40

Assess resource_projection for SO_HO_HON05_S__randomized__c1 and SO_HO_HON05_S__randomized__b7

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 15

Native pointer: /joint_analysis/synthesis_coverage/obligations/14; canonical SHA-256: 6ca9665dc048c8d8370adc131f21e2ccb0abc66153a53519eb0afd44b77eb6c1

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/argument; canonical SHA-256: 3e2bb1b2308c3b700170d5f9b92c02a770c5a364bd4f6789809f688f10b7927e

Unresolved historical/current review/source/projection work is not completed by this native regional publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids; canonical SHA-256: 25f62ba9147f3ae6c831da33eeded1471abea5da855d3ee23692e4ea3cc43a28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/3; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/4; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/5; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/6; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/7; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/8; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/9; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/10; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/lead; canonical SHA-256: da84e6401129bbd4a68d323cfe422a826809eab30c2b6cc9f0bd90c5fbb57aba

Reviewer must independently read prepared analysis, changed claims, decisive frozen premises and arXiv:2609.28202v2 Definition 3.1/Theorems 3.2 and 3.4.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 16

Native pointer: /joint_analysis/synthesis_coverage/obligations/15; canonical SHA-256: 3cf178715c136924974b97719baf3f696d817da10aa95ba1e53a56b615f4f191

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/argument; canonical SHA-256: 3e2bb1b2308c3b700170d5f9b92c02a770c5a364bd4f6789809f688f10b7927e

Unresolved historical/current review/source/projection work is not completed by this native regional publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids; canonical SHA-256: 25f62ba9147f3ae6c831da33eeded1471abea5da855d3ee23692e4ea3cc43a28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/3; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/4; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/5; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/6; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/7; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/8; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/9; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/10; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/lead; canonical SHA-256: 76b4feab956a6bdaedfb3989ef58b65a4a8b4947818a6ad8036f97d14b761566

arXiv:2610.16832v2 Section 6.1 deterministic curvature transfer: higher-order regularity, uniform scaling, dimension and complete-jet robustness remain unread/unproved; no adoption.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 17

Native pointer: /joint_analysis/synthesis_coverage/obligations/16; canonical SHA-256: d6aa16baef4d3a0598577571b661049b51a40c511c46b75812b0769dac55f42f

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/argument; canonical SHA-256: 3e2bb1b2308c3b700170d5f9b92c02a770c5a364bd4f6789809f688f10b7927e

Unresolved historical/current review/source/projection work is not completed by this native regional publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids; canonical SHA-256: 25f62ba9147f3ae6c831da33eeded1471abea5da855d3ee23692e4ea3cc43a28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/3; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/4; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/5; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/6; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/7; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/8; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/9; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/10; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/lead; canonical SHA-256: 21025226cc3a6925841a72b3d01807e61c8aff4eabad4e703f7b85709daf6119

Low-dimensional positive-modulus rates and possible saturation remain unassessed in the marked missing-lower regions.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 18

Native pointer: /joint_analysis/synthesis_coverage/obligations/17; canonical SHA-256: e535149582666fbb60788f5e523f391204b544a9c3f7ec97098ac8f8ca198f8f

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/argument; canonical SHA-256: 3e2bb1b2308c3b700170d5f9b92c02a770c5a364bd4f6789809f688f10b7927e

Unresolved historical/current review/source/projection work is not completed by this native regional publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids; canonical SHA-256: 25f62ba9147f3ae6c831da33eeded1471abea5da855d3ee23692e4ea3cc43a28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/3; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/4; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/5; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/6; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/7; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/8; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/9; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/10; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/lead; canonical SHA-256: 8a26a7bcda61a7d4d48e2ee27263a23763953c92c56a2a2de663a0f978b23edf

Dormant deterministic q2 has empty tracked/fixed metadata; its b2/b3 are not adopted into q1. Any future transfer or normalization needs separate exact-premise review.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 19

Native pointer: /joint_analysis/synthesis_coverage/obligations/18; canonical SHA-256: 3f81486d4301553cea676ca3b163ff133aee627ecdfb8a7c6b061da76938efff

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/argument; canonical SHA-256: 3e2bb1b2308c3b700170d5f9b92c02a770c5a364bd4f6789809f688f10b7927e

Unresolved historical/current review/source/projection work is not completed by this native regional publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids; canonical SHA-256: 25f62ba9147f3ae6c831da33eeded1471abea5da855d3ee23692e4ea3cc43a28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/3; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/4; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/5; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/6; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/7; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/8; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/9; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/10; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/id; canonical SHA-256: a0050dd45f09b8c1454f66ddc34c7e3533ab3f980a23fb9c8576d4ecdca8fe45

retained-material-lead-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/lead; canonical SHA-256: 2487ee44afece63c92e4754a807a6ff4770d93d5db77e7445ba03d2a74798ca3

Randomized q1 outside its registered fixed-ratio window is unassessed; q2 results do not automatically relabel q1.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 20

Native pointer: /joint_analysis/synthesis_coverage/obligations/19; canonical SHA-256: 914820ca7d5adda8d5df7736abd04d8193348ebb683cff6fb7eedda800ee9183

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/argument; canonical SHA-256: 3e2bb1b2308c3b700170d5f9b92c02a770c5a364bd4f6789809f688f10b7927e

Unresolved historical/current review/source/projection work is not completed by this native regional publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids; canonical SHA-256: 25f62ba9147f3ae6c831da33eeded1471abea5da855d3ee23692e4ea3cc43a28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/3; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/4; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/5; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/6; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/7; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/8; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/9; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/10; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/id; canonical SHA-256: 816e64d45ab01655b0cdb3174cc88338b9552319d4504b2ed46ed2504883fbc8

retained-material-lead-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/lead; canonical SHA-256: b56583d96053a6da59b461fdf3534635dea9cff8f4a11c97e8f4bcc62d181b83

Assess resource_projection for SO_HO_HON05_S__randomized__c1 and SO_HO_HON05_S__randomized__b5

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 21

Native pointer: /joint_analysis/synthesis_coverage/obligations/20; canonical SHA-256: ec89072c21a01fd242526c739b0ebf8192e595d133de6c05a4eca2fa4ecb9d9d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/argument; canonical SHA-256: 3e2bb1b2308c3b700170d5f9b92c02a770c5a364bd4f6789809f688f10b7927e

Unresolved historical/current review/source/projection work is not completed by this native regional publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids; canonical SHA-256: 25f62ba9147f3ae6c831da33eeded1471abea5da855d3ee23692e4ea3cc43a28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/3; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/4; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/5; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/6; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/7; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/8; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/9; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/comparison_ids/10; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/id; canonical SHA-256: 5f5ef600bbb2ac5a387c0c18974eca304cd2a13b61d69abb61fe40a3138ea1c9

retained-material-lead-6

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/lead; canonical SHA-256: 54a9474e45dd39ff8830deb83c3df639137374ba3f3433819a4c5c9b494ed193

Assess resource_projection for SO_HO_HON05_S__randomized__c1 and SO_HO_HON05_S__randomized__b6

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/20/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 22

Native pointer: /joint_analysis/synthesis_coverage/obligations/21; canonical SHA-256: 3566000ce89835b6b1ead40bade539b7cdecccc33dee0fa2cd3bb76fa2c01e2e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/argument; canonical SHA-256: 3e2bb1b2308c3b700170d5f9b92c02a770c5a364bd4f6789809f688f10b7927e

Unresolved historical/current review/source/projection work is not completed by this native regional publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids; canonical SHA-256: 25f62ba9147f3ae6c831da33eeded1471abea5da855d3ee23692e4ea3cc43a28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/3; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/4; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/5; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/6; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/7; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/8; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/9; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/comparison_ids/10; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/id; canonical SHA-256: 20ad6c87c364725f99c5c808f9434c0ceddcc5b3563d71c5f7a0ff6148b9be6d

retained-material-lead-7

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/lead; canonical SHA-256: b7f61692d68897762d151ac9302129477b8f366a0f0442d993efe79cd177fe40

Assess resource_projection for SO_HO_HON05_S__randomized__c1 and SO_HO_HON05_S__randomized__b7

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/21/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 23

Native pointer: /joint_analysis/synthesis_coverage/obligations/22; canonical SHA-256: a45f56f290f7873e71914492cc02309125813dd8082fd6afd7a7c697dd2b9f46

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids; canonical SHA-256: 25f62ba9147f3ae6c831da33eeded1471abea5da855d3ee23692e4ea3cc43a28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/0; canonical SHA-256: da352751ef8f6146665c81137303fdbd3068e160342c10fe8476878eb5ec2cec

SO_HO_HON05_S__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/1; canonical SHA-256: 0b5aa9ef5483f766b04f5adf2f27119423368cc8b1fe1b3cf74665b8c884f002

SO_HO_HON05_S__deterministic__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/2; canonical SHA-256: 7eca538a87f504eddb93d5c806abc697a5d01cef907891ddbc1073bb87464479

SO_HO_HON05_S__deterministic__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/3; canonical SHA-256: d7d1ffa9bd82e40759d59f6be8f173e06cec60463a97b03c6e2328f0a658c3cc

SO_HO_HON05_S__deterministic__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/4; canonical SHA-256: f5cc3bb7d1ccaf7fb7d8519467c39ed785646f0b7fbbb4d9e3a5e657eca26409

SO_HO_HON05_S__randomized__c1

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/5; canonical SHA-256: 7f54e849781cbcf28c7a6a613b709317ef56d7a6d9ae8e2a08e61dad69bba5bb

SO_HO_HON05_S__randomized__c2

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/6; canonical SHA-256: 09bcc5c5016878aa22d309e42e356436902626f614e9f3e7832622f72a73d791

SO_HO_HON05_S__randomized__c3

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/7; canonical SHA-256: 76c062927af5efcb9fc392db2ca185beb815af78ab28e9021ee6c73c3614c49a

SO_HO_HON05_S__randomized__c4

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/8; canonical SHA-256: 7e1530e38b7a8dd198c30bd8d4ee40326afc2048d85773c19ae79660ca270b22

SO_HO_HON05_S__deterministic__c5

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/9; canonical SHA-256: 377a8047246086275fe88983c91997742c53345b1b9099a62aaca6c4494c0287

SO_HO_HON05_S__randomized__c5

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/comparison_ids/10; canonical SHA-256: aef8e67e208c90deec903662cd6693211d228052909fbb8980caf1ce5b04218d

SO_HO_HON05_S__randomized__c6_q2_J

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/id; canonical SHA-256: a5c315aec3d2bd020dd2947eec97cfe5eefac6580ca15c86d6108989f6e8cb85

curated-scope-limit-7aeb3b9408

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/22/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 619d8ab729b6c20f8b1a3db421ca27a19c4368252bb60264fd3f2d534a4e7f0f

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 2f23be3f3509558fb70a62770f6637f34fbdd0cda81bad4943db8bac38d5d46e

#### Native item 1

Native pointer: /joint_analysis/target/allowed_constant_dependencies/0; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native item 2

Native pointer: /joint_analysis/target/allowed_constant_dependencies/1; canonical SHA-256: 1f5a58ab97d8a0942b61630f5fe9855dc2f63f8a71f21c1e113292284989a5fd

SO_HO_HON05_S_p_977bf3923c

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 17e9c1f175d8c8b46b7568ef355c1317dd255bce9b02e18a70d5e0f1600b22e1

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 8d65311f8a785198e53a1915bb5908b3c4abf1e26623fde6d8d4f09ed2c903fc

/views/1

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: 4b81cab280b1e31c2ea7afa9a416577b7c9c22795698d5d642e0394c36a90edd

/quantities/2

#### Native item 7

Native pointer: /joint_analysis/target/contract_refs/6; canonical SHA-256: 05d046233905e198d7a7ff8166fdfb957609dfac6a952d72e56884a938e4a37c

/quantities/3

#### Native item 8

Native pointer: /joint_analysis/target/contract_refs/7; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 9dfa229d1157617aeedbe2df97f0f94cab89ad42c77416a6eb96669760b598a4

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 4707e6d7f2d3b17f0833ab1ee1f2a0bf5c23a5b237951ba02f575d3ad603fc77

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: add7c50d2b91811dbf514b6a4537184a8ddb9a4ebd3facc78a7700b7e6c5c83e

Fixed integer k>=2.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 37664d5895f78758ec8e94e440b30c9a2cfc68873c28306301b40d6a2f3fefa3

k

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: d708d89005acb51d21218b979ca855bffdca74245c3114cd5e398d9c3ef1689f

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: c34bccf86607fb3b4639cfe53fb3fb3421b33082937c4f9c621be15e77ddaf6a

Fixed positive window constant, local to B<=C_0 A or B>C_0 A; not an objective assumption.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: 1f5a58ab97d8a0942b61630f5fe9855dc2f63f8a71f21c1e113292284989a5fd

SO_HO_HON05_S_p_977bf3923c

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: e2139ce8ac0004812b0693b1a06e2fd2ffac12e112d5130e9e0ed2bc54d984b3

C_0

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 7ba2eb95fcd0502d92ac06f4b8546b20c171f06bc8372091dc709644ad5b42be

d>=1 integer, Delta>=0,M_k>=0,epsilon_g>0,epsilon_H>0, fixed k>=2. Separate deterministic q1/g1 and randomized q1 or q2/g1 fixed-path full-jet minimax costs; no quantity IDs merged. On the positive branch define H={Delta>0, M_k>0, max(A,B)>=C_k, d>=C_k(1+A+B)}, G={Delta>0, M_k>0, A>=C_k, d>=C_k(1+A)log(3+A)}, C={k>=3 and B>C_0 A}, J=G intersect {B<=C_0 A}. C_k denotes a sufficiently large unspecified k-only proof constant. Randomized q1 is assessed on its registered J window; dormant deterministic q2 is excluded.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 72adc548d251383229a37c5f8a5056128958d94804283246ef1a5988f3921916

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 2a25d2c28c8db2f24f22ecea58f4b309c5a525e73766fdffc4c259b211058118

SO_HO_HON05_S_p_981b3c27ef

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 787e83f1611fe309121f71833458dd7e2f4bf79cf528865e7b6d64f68e27bcbd

SO_HO_HON05_S_p_1affd8ebbd

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 81a4acfb96fe2c2ae594ccbeb770233250ba966549631d46b230cbbd6fdb0a76

SO_HO_HON05_S_p_cf7461a27d

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: 2a449bc7bc857e8b02f3bca16f93f7d5dd385f37babb0285635dcea2ee59ad07

SO_HO_HON05_S_p_f1e4f0befe

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 9b7761a9e6367e59920ce2ceca78b5e685c3e6705d522b6325b1559d8a19a1a9

SO_HO_HON05_S_p_b4bfb5b0de

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 6ce51e07ac90088e08a04a51fe3eac5bc5829a6989f656ea4a2154cddd8d302a

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: 1e0a2047fa2d3b6974192b318658de322c48073137ebff0faf5f0c24fdfadc6b

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: ebd72388d400ece2eac4c38c383eecd2047fa48d6e3952a2f3b401054add213a

A=Delta*M_k^(1/k)*epsilon_g^(-(k+1)/k). Native dimensionless workload, invariant under f(x)->a*f(x/b), with (Delta,M_k,epsilon_g)->(a*Delta,a*b^(-(k+1))*M_k,a*epsilon_g/b).

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: 2efd69e4f68ced5a40d1bc25bc7d91edc30c493239d515d730ed1392c9acbef6

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: 787e83f1611fe309121f71833458dd7e2f4bf79cf528865e7b6d64f68e27bcbd

SO_HO_HON05_S_p_1affd8ebbd

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: 81a4acfb96fe2c2ae594ccbeb770233250ba966549631d46b230cbbd6fdb0a76

SO_HO_HON05_S_p_cf7461a27d

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/2; canonical SHA-256: 2a449bc7bc857e8b02f3bca16f93f7d5dd385f37babb0285635dcea2ee59ad07

SO_HO_HON05_S_p_f1e4f0befe

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/3; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: 798640599597df7a8daa32b1132f07850a68b5e71bd295650399a38074f52804

A

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1; canonical SHA-256: 7255c2c402c655af11799ca32e9de0ed07a2dcb4d3b4e96c3fa6b5023f76bc18

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/1/expression; canonical SHA-256: 6fb511d4fd13d98d0aeef570cbaebf1d64367a615d0c90f3df9c79103df45c1a

B=Delta*M_k^(2/(k-1))*epsilon_H^(-(k+1)/(k-1)). Native dimensionless workload; invariant under the same rescaling with epsilon_H->a*epsilon_H/b^2.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs; canonical SHA-256: ace6cfcdbe9ac94f1f92e2b34c3d1f72d68800150bd48ad723704671510a03a1

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/0; canonical SHA-256: 787e83f1611fe309121f71833458dd7e2f4bf79cf528865e7b6d64f68e27bcbd

SO_HO_HON05_S_p_1affd8ebbd

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/1; canonical SHA-256: 81a4acfb96fe2c2ae594ccbeb770233250ba966549631d46b230cbbd6fdb0a76

SO_HO_HON05_S_p_cf7461a27d

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/2; canonical SHA-256: 9b7761a9e6367e59920ce2ceca78b5e685c3e6705d522b6325b1559d8a19a1a9

SO_HO_HON05_S_p_b4bfb5b0de

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/3; canonical SHA-256: ba6c6206e41dfadf512194d24e3d5e157a165c696b5a53f13f04d931dd56b0a4

SO_HO_HON05_S_p_8e95fcb970

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/1/symbol; canonical SHA-256: 955cca1ceba45052d85984d3a2565f4ce25b7488602c60a165598bf80b26e472

B

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 72adc548d251383229a37c5f8a5056128958d94804283246ef1a5988f3921916

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 2a25d2c28c8db2f24f22ecea58f4b309c5a525e73766fdffc4c259b211058118

SO_HO_HON05_S_p_981b3c27ef

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 787e83f1611fe309121f71833458dd7e2f4bf79cf528865e7b6d64f68e27bcbd

SO_HO_HON05_S_p_1affd8ebbd

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 81a4acfb96fe2c2ae594ccbeb770233250ba966549631d46b230cbbd6fdb0a76

SO_HO_HON05_S_p_cf7461a27d

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 2a449bc7bc857e8b02f3bca16f93f7d5dd385f37babb0285635dcea2ee59ad07

SO_HO_HON05_S_p_f1e4f0befe

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 9b7761a9e6367e59920ce2ceca78b5e685c3e6705d522b6325b1559d8a19a1a9

SO_HO_HON05_S_p_b4bfb5b0de

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Yossi Arjevani; Yair Carmon; John C. Duchi; Dylan J. Foster; Ayush Sekhari; Karthik Sridharan. Second-Order Information in Non-Convex Stochastic Optimization: Power and Limitations. COLT 2020, PMLR 125, 242–299.

https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf

[2] Yair Carmon; John C. Duchi; Oliver Hinder; Aaron Sidford. Lower Bounds for Finding Stationary Points I. arXiv:1710.11606v3, 2019-08-15; Mathematical Programming 184 (2020), 71–120.

https://arxiv.org/abs/1710.11606

[3] Coralia Cartis; Nicholas I. M. Gould; Philippe L. Toint. A concise second-order complexity analysis for unconstrained optimization using high-order regularized models. arXiv:1708.04044v1, 2017-08-14; Optimization Methods and Software 35(2) (2020), 243–256.

https://arxiv.org/abs/1708.04044

[4] Wendao Wu; Haihan Zhang; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Upper and Lower Bounds for Higher-Order Nonconvex Finite-Sum Optimization. arXiv:2609.28202v2, 2026-10-19, preprint.

https://arxiv.org/abs/2609.28202

[5] Yossi Arjevani; Yair Carmon; John C. Duchi; Dylan J. Foster; Ayush Sekhari; Karthik Sridharan. Second-Order Information in Non-Convex Stochastic Optimization: Power and Limitations. COLT 2020, PMLR 125:242-299, proceedings PDF.

https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf

[6] Qian Chen; Wendao Wu; Haihan Zhang; Chenheng Zhang; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Complexity for Second-Order Stationary Point with Sample Reuse. arXiv:2610.16832v2, 2026-10-19, preprint.

https://arxiv.org/abs/2610.16832

[7] Yair Carmon, John C. Duchi, Oliver Hinder, Aaron Sidford. Lower Bounds for Finding Stationary Points I. arXiv:1710.11606v3; Mathematical Programming 184 (2020).

https://arxiv.org/abs/1710.11606v3

[8] E. G. Birgin; J. L. Gardenghi; J. M. Martínez; S. A. Santos; Ph. L. Toint. Worst-case evaluation complexity for unconstrained nonlinear optimization using high-order regularized models. NAXYS-05-2015, 2015-07-10; Mathematical Programming 163 (2017), 359–368.

https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf
