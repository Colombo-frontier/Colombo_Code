# Nonconvex second-order stationarity under joint gradient and Hessian regularity

**Setting ID.** `SO_HO_HON06_S`

Single-objective optimization

Find an approximate second-order stationary point of the full objective:

**Status.** Bounds missing

**TASK tags.** formulation: Second order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz gradient; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Exact jet 2; operation: Exact jet 2; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

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

Fix $k=2$. The gradient is $\beta$-Lipschitz and the Hessian is $M_2$-Lipschitz throughout the ambient space, in Euclidean induced norms.

Admissible parameter domain:

$$d\ge1,\quad k\ge2;\quad\text{all other parameters satisfy their tabulated ranges}.$$

### Oracle interface

Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $\Delta$, $\beta$, $M_k$, $\varepsilon_g$, $\varepsilon_H$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

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

$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,2\}$ and $D^0f=f$.

$\|T\|_{\mathrm{op}},\ \|T\|_{\mathrm{op},2}$: Induced operator norm of a Euclidean multilinear tensor; the spectral norm for matrices.

$$\|T\|_{\mathrm{op}}=\|T\|_{\mathrm{op},2}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|.$$

$\mathcal{E}$: Base error defined in the metric specification; expectation or probability aggregation is imposed by the guarantee.

$N$: Total number of original oracle calls; the unit cost is specified in the resource convention. **Domain:** $N\in\mathbb{Z}_{\ge0}$.

$T^*$: Minimum worst-case budget for one algorithm to meet the requirement on the full instance class, within the specified regime, guarantee and resource projection. Expected-resource specifications instead minimize the per-instance expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching bounds up to constants, and upper bounds omitting the declared logarithmic factors. **Domain:** Hidden constants, fixed parameters, and omitted logarithmic variables are specified for each bound.

$\inf,\sup,\min,\max$: Infimum, supremum, attained minimum and attained maximum.

$c,C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<c,C<\infty$.

$J_{2}f(x)$: Function value and the complete tuple of derivatives from order one through the specified maximum order.

$$J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x)).$$

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$\lambda_{\min}(A),[z]_+$: The smallest eigenvalue of a symmetric matrix and the positive part of a scalar.

$$[z]_+=\max\{z,0\}.$$

$I_d$: The identity matrix in dimension $d$.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k=2$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta\ge0$.

$\beta$: Gradient Lipschitz upper bound **Domain:** $\beta>0$.

$M_k$: Global Lipschitz upper bound for the order-$k$ derivative in the tensor operator norm. **Domain:** $M_k\ge0$.

$\varepsilon_g$: Gradient-norm tolerance **Domain:** $\varepsilon_g>0$.

$\varepsilon_H$: Tolerance for negative Hessian curvature **Domain:** $\varepsilon_H>0$.

$C_k$: A sufficiently large positive constant depending only on the fixed order $k$, without a numerical value specified. **Domain:** $C_k>0$.

$c_k$: A sufficiently small positive constant depending only on the fixed order $k$, without a numerical value specified. **Domain:** $c_k>0$.

$A$: Gradient work at order k=2 **Domain:** $A\ge0$.

$$A=\Delta\,(\min\{\beta\,((\varepsilon_g)^{-2}),\sqrt{M_k}\,((\varepsilon_g)^{\frac{-3}{2}})\}).$$

$B$: Negative-curvature work at order k=2 **Domain:** $B\ge0$.

$$B=\Delta\,(M_k)^{2}\,((\varepsilon_H)^{-3}).$$

$H_{\mathrm{auto}}$: Absolute bound on negative curvature over the initial sublevel set **Domain:** $H_{\mathrm{auto}}\ge0$.

$$H_{\mathrm{auto}}=\min\{\beta,(\frac{3}{2}\,\Delta\,(M_k)^{2})^{\frac{1}{3}}\}.$$

$M_2$: This specification fixes order two, so the highest-order modulus is the Hessian modulus.

$$M_2=M_k\quad(k=2).$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$C_\theta$: A sufficiently large positive constant depending only on the fixed parameter group $\theta$. **Domain:** $C_\theta>0$.

$c_\theta$: A sufficiently small positive accuracy threshold depending only on the fixed parameter group $\theta$. **Domain:** $c_\theta>0$.

$\theta$: Model parameters held fixed in the corresponding accuracy bound.

$$\theta=(k,\beta,M_k,\Delta).$$

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

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter window 1

**Region.** $\varepsilon_H\le c\beta,\max{A,B}\ge C,d\ge C(1+A+B)$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B3

$$
\Omega(A+B)
$$

**Upper bound.** B1, B2

$$
O(1+A+B)
$$

**Gap or comparison.** $\Theta(1)$

**Comparison argument.** Nontrivial deterministic regime over the stated parameter domain, excluding zero-query and automatic-curvature regimes. Dimension, probability and parameter constants are governed by the corresponding atomic bounds and conversions.

### R2 - Parameter window 2

**Region.** $\varepsilon_g\ge \sqrt(2\beta\Delta), \varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B7, B14

$$
0
$$

**Upper bound.** B6, B13

$$
0
$$

### R3 - Parameter window 3

**Region.** $k=2,d\ge 1,\beta,M_2,\Delta>0$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1, B2

$$
O(1+A+B)
$$

### R4 - Parameter window 4

**Region.** $\varepsilon_H\ge \beta$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B4

$$
C[1+\Delta \min{\beta\varepsilon_g^{-2},\sqrt{M_2}\varepsilon_g^{-3/2}}]
$$

### R5 - Parameter window 5

**Region.** $\varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B5

$$
C[1+\Delta \min{\beta\varepsilon_g^{-2},\sqrt{M_2}\varepsilon_g^{-3/2}}]
$$

### R6 - Parameter window 1

**Region.** $\theta=(\beta,M_2,\Delta)>0 fixed;0<\varepsilon_g\le c_\theta;0<\varepsilon_H\le c_\theta;d\ge C_\theta[1+\varepsilon_g^{-3}\log(2+\varepsilon_g^{-1})+\varepsilon_H^{-4}\log(2+\varepsilon_H^{-1})+\varepsilon_H^{-3}]$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B10

$$
\Omega_\theta(\varepsilon_g^{-3/2}+\varepsilon_H^{-3})
$$

**Upper bound.** B8

$$
O_\theta(1+\varepsilon_g^{-3/2}+\varepsilon_H^{-3})
$$

**Gap or comparison.** $\Theta_\theta(1)$

### R7 - Parameter window 2

**Region.** $k=2,d\ge 1,\beta,M_2,\Delta>0$

**Views.** Randomized

**Quantity.** Q3

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B8, B9

$$
O(1+A+B)
$$

### R8 - Parameter window 4

**Region.** $\varepsilon_H\ge \beta$

**Views.** Randomized

**Quantity.** Q3

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B11

$$
C[1+\Delta \min{\beta\varepsilon_g^{-2},\sqrt{M_2}\varepsilon_g^{-3/2}}]
$$

### R9 - Parameter window 5

**Region.** $\varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Views.** Randomized

**Quantity.** Q3

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B12

$$
C[1+\Delta \min{\beta\varepsilon_g^{-2},\sqrt{M_2}\varepsilon_g^{-3/2}}]
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Cubic regularization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\Delta M_2^{1/2}\varepsilon_g^{-3/2}+\Delta M_2^2\varepsilon_H^{-3}]
$$

**Sources.** [3](https://arxiv.org/abs/1708.04044)

**Conditions.** $k=2,d\ge 1,\beta,M_2,\Delta>0$

**Dimension conditions.** $k=2,d\ge 1,\beta,M_2,\Delta>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [3](https://arxiv.org/abs/1708.04044) theorem: Theorem3.6 at k=2; pdf pages: 8

### B2 - Gradient descent or descent along the most negative eigenvector

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\Delta\beta\varepsilon_g^{-2}+\Delta M_2^2\varepsilon_H^{-3}]
$$

**Sources.** [5](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf) [3](https://arxiv.org/abs/1708.04044)

**Conditions.** $k=2,d\ge 1,\beta,M_2,\Delta>0$

**Dimension conditions.** $k=2,d\ge 1,\beta,M_2,\Delta>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A2

### B3 - Separate scaling of the first-order chain with joint smoothness and the curvature chain

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c(A+B)
$$

**Sources.** [2](https://arxiv.org/abs/1710.11606) [1](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) [6](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) [4](https://arxiv.org/abs/2610.16832) [7](https://arxiv.org/abs/1710.11606v3) [5](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

**Conditions.** $\varepsilon_H\le c\beta,\max{A,B}\ge C,d\ge C(1+A+B)$

**Dimension conditions.** $\varepsilon_H\le c\beta,\max{A,B}\ge C,d\ge C(1+A+B)$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3, A4, A1

**Source location.** [2](https://arxiv.org/abs/1710.11606) theorem: Theorem1, simultaneous β and M2 scaling; pdf pages: 14

**Source location.** [1](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) theorem: Appendix H.2 noiseless specialization, exact deterministic rotation conversion; pdf pages: 58

### B4 - Algorithm for first-order stationarity

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\Delta \min{\beta\varepsilon_g^{-2},\sqrt{M_2}\varepsilon_g^{-3/2}}]
$$

**Conditions.** $\varepsilon_H\ge \beta$

**Dimension conditions.** $\varepsilon_H\ge \beta$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A5

### B5 - Descent algorithm for first-order stationarity

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\Delta \min{\beta\varepsilon_g^{-2},\sqrt{M_2}\varepsilon_g^{-3/2}}]
$$

**Conditions.** $\varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Dimension conditions.** $\varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A5

### B6 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_g\ge \sqrt(2\beta\Delta), \varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Dimension conditions.** $\varepsilon_g\ge \sqrt(2\beta\Delta), \varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A5, A6

### B7 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon_g\ge \sqrt(2\beta\Delta), \varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Dimension conditions.** $\varepsilon_g\ge \sqrt(2\beta\Delta), \varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A6

### B8 - Cubic regularization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\Delta M_2^{1/2}\varepsilon_g^{-3/2}+\Delta M_2^2\varepsilon_H^{-3}]
$$

**Sources.** [3](https://arxiv.org/abs/1708.04044)

**Conditions.** $k=2,d\ge 1,\beta,M_2,\Delta>0$

**Dimension conditions.** $k=2,d\ge 1,\beta,M_2,\Delta>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [3](https://arxiv.org/abs/1708.04044) theorem: Theorem3.6 at k=2; pdf pages: 8

### B9 - Gradient descent or descent along the most negative eigenvector

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\Delta\beta\varepsilon_g^{-2}+\Delta M_2^2\varepsilon_H^{-3}]
$$

**Sources.** [5](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf) [3](https://arxiv.org/abs/1708.04044)

**Conditions.** $k=2,d\ge 1,\beta,M_2,\Delta>0$

**Dimension conditions.** $k=2,d\ge 1,\beta,M_2,\Delta>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1, A2

### B10 - Randomly rotated gated negative-curvature chain with an exact deterministic loss

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\theta[\varepsilon_g^{-3/2}+\varepsilon_H^{-3}]
$$

**Sources.** [4](https://arxiv.org/abs/2610.16832) [2](https://arxiv.org/abs/1710.11606)

**Conditions.** $\theta=(\beta,M_2,\Delta)>0 fixed;0<\varepsilon_g\le c_\theta;0<\varepsilon_H\le c_\theta;d\ge C_\theta[1+\varepsilon_g^{-3}\log(2+\varepsilon_g^{-1})+\varepsilon_H^{-4}\log(2+\varepsilon_H^{-1})+\varepsilon_H^{-3}]$

**Dimension conditions.** $\theta=(\beta,M_2,\Delta)>0 fixed;0<\varepsilon_g\le c_\theta;0<\varepsilon_H\le c_\theta;d\ge C_\theta[1+\varepsilon_g^{-3}\log(2+\varepsilon_g^{-1})+\varepsilon_H^{-4}\log(2+\varepsilon_H^{-1})+\varepsilon_H^{-3}]$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [4](https://arxiv.org/abs/2610.16832) theorem: Section6.1 pp14–16; Section6.3 p23; AppendixA.2 p25; pdf pages: 14

**Source location.** [2](https://arxiv.org/abs/1710.11606) theorem: Theorem2, fixed positive β/M2 gradient slice; pdf pages: 19

### B11 - Algorithm for first-order stationarity

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\Delta \min{\beta\varepsilon_g^{-2},\sqrt{M_2}\varepsilon_g^{-3/2}}]
$$

**Conditions.** $\varepsilon_H\ge \beta$

**Dimension conditions.** $\varepsilon_H\ge \beta$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A5

### B12 - Descent algorithm for first-order stationarity

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\Delta \min{\beta\varepsilon_g^{-2},\sqrt{M_2}\varepsilon_g^{-3/2}}]
$$

**Conditions.** $\varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Dimension conditions.** $\varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A5

### B13 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_g\ge \sqrt(2\beta\Delta), \varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Dimension conditions.** $\varepsilon_g\ge \sqrt(2\beta\Delta), \varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A5, A6

### B14 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon_g\ge \sqrt(2\beta\Delta), \varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Dimension conditions.** $\varepsilon_g\ge \sqrt(2\beta\Delta), \varepsilon_H\ge \min{\beta,(3\Delta M_2^2/2)^{1/3}}$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A6

## 5. Local arguments

### A1 - High-order regularized descent with full parameter dependence

**Scope.** Fixed derivative order, complete exact jets, full-space queries, bounded initial gap, and free global known-model solution. Zero modulus is treated by polynomial recovery.

**Algorithm scope.** Fixed derivative order, complete exact jets, full-space queries, bounded initial gap, and free global known-model solution. Zero modulus is treated by polynomial recovery.

With a Lipschitz kth derivative and fixed $k\ge2$, first-order stationarity uses $O_k(1+\Delta M_k^{1/k}\varepsilon_g^{-(k+1)/k})$ complete jets.

At x, form $m_x(s)=T_k(f;x,s)+a_kM_k\|s\|^{k+1}$, choosing $a_k$ sufficiently large, depending only on k, to dominate the Taylor remainder with slack. For $M_k>0$ the model is coercive, so it has a global minimizer, available under the declared free internal computation. Comparing the model at s and zero and applying the value remainder gives
$$f(x)-f(x+s)\ge c_kM_k\|s\|^{k+1}.$$
Model first-order optimality and the gradient remainder give
$$\|\nabla f(x+s)\|\le C_kM_k\|s\|^k.$$
If the next point is not $\varepsilon_g$-stationary, the decrease is at least $c_kM_k^{-1/k}\varepsilon_g^{(k+1)/k}$. The total decrease is at most $\Delta$, so after the displayed number of calls, including initialization and final verification, stationarity is reached.

This is the parameter restoration of the regularized-model argument in BGMST17, Lemmas 2.1–2.3 and Theorem 2.5. Its normalization is $(k-1)!L=M_k$. Separate function and derivative evaluations in the source cost only a fixed multiple when complete jets are charged as one. The argument is about information calls and does not assert an inexpensive arithmetic implementation of global nonconvex model minimization.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [5](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

### A2 - Independent gradient and curvature tolerances

**Scope.** Independent tolerances and all explicitly supplied regularity budgets are retained. This is a deterministic complete-jet upper bound and is also usable in randomized views.

**Algorithm scope.** Independent tolerances and all explicitly supplied regularity budgets are retained. This is a deterministic complete-jet upper bound and is also usable in randomized views.

High-order regularization attains independent $(\varepsilon_g,\varepsilon_H)$ tolerances in $O_k(1+\Delta M_k^{1/k}\varepsilon_g^{-(k+1)/k}+\Delta M_k^{2/(k-1)}\varepsilon_H^{-(k+1)/(k-1)})$ calls.

At a global minimizer s of the regularized Taylor model, its Hessian is positive semidefinite. The Hessian Taylor remainder and regularizer Hessian imply
$$[-\lambda_{\min}(\nabla^2f(x+s))]_+\le C_kM_k\|s\|^{k-1}.$$
Combined with the gradient estimate and decrease inequality, failure of either stationarity target forces a decrease at least
$$c_k\min\{M_k^{-1/k}\varepsilon_g^{(k+1)/k},M_k^{-2/(k-1)}\varepsilon_H^{(k+1)/(k-1)}\}.$$
Summing decreases up to $\Delta$ proves the stated bound; the sum and maximum of these two terms differ by at most two. This restores parameters in CGTSOSP, Theorem 3.6 and Lemmas 3.2–3.4.

When $k=2$ and $\beta$-smoothness is also public, use an alternative complete algorithm: take a $1/\beta$ gradient step if the gradient exceeds $\varepsilon_g$; otherwise, if the smallest Hessian eigenvalue is $-h<-\varepsilon_H$, choose its eigenvector sign for nonpositive linear term and step by $2h/M_2$. Decreases are at least $\varepsilon_g^2/(2\beta)$ and $2\varepsilon_H^3/(3M_2^2)$, respectively. Its budget is $O(1+\Delta\beta\varepsilon_g^{-2}+\Delta M_2^2\varepsilon_H^{-3})$. Selecting the better of this and cubic regularization gives the linked upper envelope with the minimum of the two gradient costs.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [3](https://arxiv.org/abs/1708.04044)

### A3 - Curvature lower bounds and their algorithm scope

**Scope.** The deterministic rotation extension and arbitrary-randomized second-order primary result are distinct. Preserve restricted algorithm classes, fixed-parameter qualifiers, tolerance windows, preprint status, and sufficient dimensions.

**Algorithm scope.** The deterministic rotation extension and arbitrary-randomized second-order primary result are distinct. Preserve restricted algorithm classes, fixed-parameter qualifiers, tolerance windows, preprint status, and sufficient dimensions.

Deterministic curvature lower bounds use a resisting-rotation reduction; the arbitrary-randomized exact-second-order result is separately tied to a primary fixed-parameter theorem.

The noiseless specialization in ACDFSS20, Appendix H.2, gives a zero-respecting curvature lower bound
$$\Omega_k\left(\frac\Delta{\varepsilon_H}\min_{2\le j\le k}(M_j/\varepsilon_H)^{2/(j-1)}\right),$$
within the nonautomatic window $\varepsilon_H\le c_kM_1$. For deterministic algorithms, adaptively rotate the smooth gated chain. Unactivated gates have every derivative zero, so each complete jet reveals at most the next direction, including its value response. Choose later directions orthogonal to prior queries and, at the end, to the unqueried output. A sufficient dimension $C_k(1+N)$ accommodates all constraints. Determinism ensures that the final single rotated instance produces the constructed transcript. This seed-dependent adversary argument does not prove an arbitrary-randomized lower bound.

With only $M_k$ controlled, choose width $b\asymp(\varepsilon_H/M_k)^{1/(k-1)}$ and amplitude $a\asymp\varepsilon_Hb^2$. Then
$$N\asymp_k\Delta M_k^{2/(k-1)}\varepsilon_H^{-(k+1)/(k-1)}.$$
Additional $\beta$-smoothness requires $\varepsilon_H\le c\beta$. Combine this hard family with the separate gradient hard family by taking their maximum, which is equivalent up to a factor two to the sum; no one instance is claimed to realize both difficulties simultaneously.

For arbitrary randomized exact second-order algorithms, REUSE26v2's deterministic-loss subclass supplies the separate curvature result. Its gated chain has $O(N)$ value range and dimension-independent Hessian and third-derivative operator bounds. With $\gamma=\varepsilon_H$, spatial scale of order $\gamma$, and amplitude of order $\gamma^3$, take N of order $\gamma^{-3}$. A radial cutoff and wall at radius of order $\gamma^{-1}$ prevent unrestricted distant queries or outputs from bypassing the chain: outside the hard region the gradient is too large, while the transition region retains negative curvature. Conditional exposure of hidden rotation directions and concentration over every query and the final output give the sufficient dimension
$$d\ge C_\theta[1+\gamma^{-4}\log(2+\gamma^{-1})+\gamma^{-3}],\qquad\theta=(\beta,M_2,\Delta).$$
Thus, for fixed positive $\theta$ and sufficiently small independent tolerances, the primary result yields $\Omega_{\theta}(\varepsilon_H^{-3})$. Combining it with the randomized gradient lower bound gives the linked exact-J2 bracket. Constants may depend on fixed $\theta$; this is not a joint-parameter lower bound with universal constants, nor a higher-order randomized theorem.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [6](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) [4](https://arxiv.org/abs/2610.16832)

### A4 - Simultaneous regularity budgets and common lower-bound scaling

**Scope.** Jointly declared positive regularity budgets. Deterministic and randomized lower bounds retain their distinct sufficient dimensions and source scope.

**Algorithm scope.** Jointly declared positive regularity budgets. Deterministic and randomized lower bounds retain their distinct sufficient dimensions and source scope.

For jointly bounded derivative Lipschitz moduli, the first-order scale is $A=\Delta\min_{1\le j\le k}M_j^{1/j}\varepsilon_g^{-(j+1)/j}$, with $M_1=\beta$.

For each fixed j, use the jth-order regularized method, reading only the relevant part of the complete k-jet. Its budget is $C_j[1+\Delta M_j^{1/j}\varepsilon_g^{-(j+1)/j}]$. All parameters are public, so an algorithm may select the smallest proved budget. This minimum is an envelope of complete algorithms.

For the lower bound, use the robust CDHS smooth chain $h_N$, whose initial gap is at most $C_kN$, whose gradient stays bounded away from zero before completion, and whose jth-derivative Lipschitz modulus is at most a constant $\ell_j$ depending only on j. Set $f(x)=a h_N(x/b)$ with
$$a/b=K_k\varepsilon_g,\qquad
b=\max_{1\le j\le k}(K_k\ell_j\varepsilon_g/M_j)^{1/j}.$$
Then $\operatorname{Lip}(D^jf)=a\ell_j/b^{j+1}\le M_j$ for every j simultaneously. Choosing N proportional to $\Delta/a$ gives N of order A. For A above a fixed k-dependent threshold, deterministic resisting rotations fit in $d\ge C_k(1+A)$; the classical randomized radial construction fits in $d\ge C_k(1+A)^2\log(3+A)$. These are sufficient dimensions.

If the primary result is stated as time to query a successful point, append one complete-jet query at the algorithm's final output. A lower bound of N then gives an original-budget lower bound N-1, of the same order in the nontrivial A region. This handles arbitrary unqueried outputs without changing the success quantifier.

For $k=2$, the common scaling gives $A=\Delta\min\{\beta\varepsilon_g^{-2},\sqrt{M_2}\varepsilon_g^{-3/2}\}$. Keep the zero-query region $\varepsilon_g^2\ge2\beta\Delta$ separate; the whole domain is not uniformly Theta(1+A). Dimension improvements proved for a highest-order-only model do not automatically preserve all lower-order budgets.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [7](https://arxiv.org/abs/1710.11606v3)

### A5 - Regions where the curvature requirement is automatic

**Scope.** Uses the explicit gradient or Hessian regularity stated in each bound. Maintained-sublevel arguments apply only to algorithms that preserve that condition. Zero-modulus cases are handled separately.

**Algorithm scope.** Uses the explicit gradient or Hessian regularity stated in each bound. Maintained-sublevel arguments apply only to algorithms that preserve that condition. Zero-modulus cases are handled separately.

Curvature can be bounded from smoothness and the current objective gap; these bounds yield sufficient simplifications and zero-query regions.

If the gradient is $\beta$-Lipschitz, every Hessian has operator norm at most $\beta$; $\varepsilon_H\ge\beta$ makes the curvature requirement automatic everywhere.

If the Hessian is $M_2$-Lipschitz and $f(x)-f^*\le\Delta$, let h be the positive part of minus its smallest eigenvalue. Choose a unit eigenvector with nonpositive gradient inner product. A step of length $2h/M_2$ gives
$$f(x+tv)\le f(x)-2h^3/(3M_2^2),$$
so $h\le(3\Delta M_2^2/2)^{1/3}$. On an algorithm's maintained initial sublevel set, either this bound or $\beta$, whichever is smaller when both are available, makes curvature automatic above that threshold. Combine it with the public initial gradient bound to obtain the stated sufficient spectral-SOSP zero-query region.

If only the third derivative is $M_3$-Lipschitz, average the Taylor bounds at $x\pm tv$. Odd terms cancel:
$$[f(x+tv)+f(x-tv)]/2\le f(x)-ht^2/2+M_3t^4/24.$$
Choosing $t^2=6h/M_3$ implies $h\le\sqrt{2\Delta M_3/3}$. This special order-three relation does not extend to highest-order-only $k\ge4$: bounded-below quartic polynomials can have arbitrarily large local negative curvature while the kth-derivative Lipschitz modulus is zero.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

### A6 - Zero-query and polynomial-recovery endpoints

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

[1] Yossi Arjevani; Yair Carmon; John C. Duchi; Dylan J. Foster; Ayush Sekhari; Karthik Sridharan. Second-Order Information in Non-Convex Stochastic Optimization: Power and Limitations. COLT 2020, PMLR 125, 242–299.

https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf

[2] Yair Carmon; John C. Duchi; Oliver Hinder; Aaron Sidford. Lower Bounds for Finding Stationary Points I. arXiv:1710.11606v3, 2019-08-15; Mathematical Programming 184 (2020), 71–120.

https://arxiv.org/abs/1710.11606

[3] Coralia Cartis; Nicholas I. M. Gould; Philippe L. Toint. A concise second-order complexity analysis for unconstrained optimization using high-order regularized models. arXiv:1708.04044v1, 2017-08-14; Optimization Methods and Software 35(2) (2020), 243–256.

https://arxiv.org/abs/1708.04044

[4] Qian Chen; Wendao Wu; Haihan Zhang; Chenheng Zhang; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Complexity for Second-Order Stationary Point with Sample Reuse. arXiv:2610.16832v2, 2026-10-19, preprint.

https://arxiv.org/abs/2610.16832

[5] E. G. Birgin; J. L. Gardenghi; J. M. Martínez; S. A. Santos; Ph. L. Toint. Worst-case evaluation complexity for unconstrained nonlinear optimization using high-order regularized models. NAXYS-05-2015, 2015-07-10; Mathematical Programming 163 (2017), 359–368.

https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf

[6] Yossi Arjevani; Yair Carmon; John C. Duchi; Dylan J. Foster; Ayush Sekhari; Karthik Sridharan. Second-Order Information in Non-Convex Stochastic Optimization: Power and Limitations. COLT 2020, PMLR 125:242-299, proceedings PDF.

https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf

[7] Yair Carmon, John C. Duchi, Oliver Hinder, Aaron Sidford. Lower Bounds for Finding Stationary Points I. arXiv:1710.11606v3; Mathematical Programming 184 (2020).

https://arxiv.org/abs/1710.11606v3
