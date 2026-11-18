# Nonconvex first-order stationarity under joint multilevel regularity

**Setting ID.** `SO_HO_HON02_S`

Single-objective optimization

Find an approximate first-order stationary point of the full objective, namely $\|\nabla f(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

**Status.** Bounds missing

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz gradient; smoothness: Simultaneous derivative lipschitz

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

Each $1\le j\le k$ satisfies $\|D^jf(x)-D^jf(y)\|_{\mathrm{op}}\le M_j\|x-y\|_2$, where $M_1=\beta$.

Admissible parameter domain:

$$d\ge1,\quad k\ge2;\quad\text{all other parameters satisfy their tabulated ranges}.$$

### Oracle interface

Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $\Delta$, $(M_j)_{j=1}^k$, $\beta$, $\varepsilon_g$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

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

$(M_j)_{j=1}^k$: Derivative Lipschitz bounds, with $M_1=\beta$ **Domain:** $(M_j)_{j=1}^k\in\mathbb{R}_{>0}^k$.

$\beta$: Gradient Lipschitz upper bound **Domain:** $\beta>0$.

$\varepsilon_g$: Gradient-norm tolerance **Domain:** $\varepsilon_g>0$.

$C_k$: A sufficiently large positive constant depending only on the fixed order $k$, without a numerical value specified. **Domain:** $C_k>0$.

$c_k$: A sufficiently small positive constant depending only on the fixed order $k$, without a numerical value specified. **Domain:** $c_k>0$.

$A$: First-order stationarity work for the intersection of multiple regularity classes **Domain:** $A\ge0$.

$S$: Most favorable natural regularity scale in one dimension **Domain:** $S\ge0$.

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

### R1 - Parameter window 1

**Region.** $A\ge C_k, d\ge C_k(1+A)$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega_k(A)
$$

**Upper bound.** B1

$$
O_k(1+A)
$$

**Gap or comparison.** $\Theta_k(1)$

### R2 - Parameter window 2

**Region.** $d=1,0<\varepsilon_g\le c_k S$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B4, B11

$$
\Omega_k(1+\log(S/\varepsilon_g))
$$

**Upper bound.** B3, B10

$$
O_k(1+\log(S/\varepsilon_g))
$$

**Gap or comparison.** $\Theta_k(1)$

### R3 - Parameter window 3

**Region.** $\varepsilon_g^2\ge 2\beta\Delta$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

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

### R4 - Parameter window 4

**Region.** $d=2, \varepsilon_g^2<2\beta\Delta$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1, B5

$$
O_k(1+\min{A,\sqrt{\beta\Delta}/\varepsilon_g})
$$

### R5 - Parameter window 5

**Region.** $d\ge 1, \Delta>0, M_j>0$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
C_j(1+\Delta M_j^{1/j}\varepsilon_g^{-(j+1)/j}),\qquad j\in\{1,\ldots,k\}
$$

### R6 - Parameter window 1

**Region.** $A\ge C_k, d\ge C_k(1+A)^2 \log(3+A)$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B9

$$
\Omega_k(A)
$$

**Upper bound.** B8

$$
O_k(1+A)
$$

**Gap or comparison.** $\Theta_k(1)$

### R7 - Parameter window 3

**Region.** $d=2, \varepsilon_g^2<2\beta\Delta$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B8, B12

$$
O_k(1+\min{A,\sqrt{\beta\Delta}/\varepsilon_g})
$$

### R8 - Parameter window 5

**Region.** $d\ge 1, \Delta>0, M_j>0$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B8

$$
C_j(1+\Delta M_j^{1/j}\varepsilon_g^{-(j+1)/j}),\qquad j\in\{1,\ldots,k\}
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Regularized model with the order j selected optimally from public parameters

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C_j(1+\Delta M_j^{1/j}\varepsilon_g^{-(j+1)/j}),\qquad j\in\{1,\ldots,k\}
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf) [5](https://arxiv.org/abs/1710.11606v3)

**Conditions.** $d\ge 1, \Delta>0, M_j>0$

**Dimension conditions.** $d\ge 1, \Delta>0, M_j>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A2

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf) theorem: Theorem2.5 (each j≥2); j=1 follows smooth descent; pdf pages: 7

### B2 - A single smooth robust chain controls every $M_j$ simultaneously

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c_k A
$$

**Sources.** [2](https://arxiv.org/abs/1710.11606) [5](https://arxiv.org/abs/1710.11606v3) [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

**Conditions.** $A\ge C_k, d\ge C_k(1+A)$

**Dimension conditions.** $A\ge C_k, d\ge C_k(1+A)$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A2

**Source location.** [2](https://arxiv.org/abs/1710.11606) theorem: Theorem1; common smooth-chain regularity; pdf pages: 14

### B3 - One-dimensional bisection using function values

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C_k[1+\log_+(S/\varepsilon_g)]
$$

**Sources.** [4](https://arxiv.org/abs/2610.16295)

**Conditions.** $d=1,0<\varepsilon_g\le c_k S$

**Dimension conditions.** $d=1,0<\varepsilon_g\le c_k S$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [4](https://arxiv.org/abs/2610.16295) theorem: Theorem7.1; pdf pages: 11

### B4 - Ordered hidden intervals for complete jets

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_k[1+\log(S/\varepsilon_g)]
$$

**Sources.** [4](https://arxiv.org/abs/2610.16295)

**Conditions.** $d=1,0<\varepsilon_g\le c_k S$

**Dimension conditions.** $d=1,0<\varepsilon_g\le c_k S$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [4](https://arxiv.org/abs/2610.16295) theorem: Theorem6.1; pdf pages: 9

### B5 - Two-dimensional GFPT

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\sqrt{\beta\Delta}/\varepsilon_g]
$$

**Sources.** [3](https://arxiv.org/abs/2310.09157)

**Conditions.** $d=2, \varepsilon_g^2<2\beta\Delta$

**Dimension conditions.** $d=2, \varepsilon_g^2<2\beta\Delta$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [3](https://arxiv.org/abs/2310.09157) theorem: Theorem4.1; pdf pages: 9

### B6 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_g^2\ge 2\beta\Delta$

**Dimension conditions.** $\varepsilon_g^2\ge 2\beta\Delta$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3

### B7 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon_g^2\ge 2\beta\Delta$

**Dimension conditions.** $\varepsilon_g^2\ge 2\beta\Delta$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3

### B8 - Regularized model with the order j selected optimally from public parameters

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C_j(1+\Delta M_j^{1/j}\varepsilon_g^{-(j+1)/j}),\qquad j\in\{1,\ldots,k\}
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf) [5](https://arxiv.org/abs/1710.11606v3)

**Conditions.** $d\ge 1, \Delta>0, M_j>0$

**Dimension conditions.** $d\ge 1, \Delta>0, M_j>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1, A2

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf) theorem: Theorem2.5 (each j≥2); j=1 follows smooth descent; pdf pages: 7

### B9 - Common multilevel scaling of a randomized robust chain

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_k A
$$

**Sources.** [2](https://arxiv.org/abs/1710.11606) [5](https://arxiv.org/abs/1710.11606v3) [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

**Conditions.** $A\ge C_k, d\ge C_k(1+A)^2 \log(3+A)$

**Dimension conditions.** $A\ge C_k, d\ge C_k(1+A)^2 \log(3+A)$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1, A2

**Source location.** [2](https://arxiv.org/abs/1710.11606) theorem: Theorem2; Lemma6; simultaneous regularity scaling; pdf pages: 19

### B10 - One-dimensional bisection using function values

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C_k[1+\log_+(S/\varepsilon_g)]
$$

**Sources.** [4](https://arxiv.org/abs/2610.16295)

**Conditions.** $d=1,0<\varepsilon_g\le c_k S$

**Dimension conditions.** $d=1,0<\varepsilon_g\le c_k S$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [4](https://arxiv.org/abs/2610.16295) theorem: Theorem7.1; pdf pages: 11

### B11 - Ordered hidden intervals for complete jets

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_k[1+\log(S/\varepsilon_g)]
$$

**Sources.** [4](https://arxiv.org/abs/2610.16295)

**Conditions.** $d=1,0<\varepsilon_g\le c_k S$

**Dimension conditions.** $d=1,0<\varepsilon_g\le c_k S$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [4](https://arxiv.org/abs/2610.16295) theorem: Theorem6.1; pdf pages: 9

### B12 - Two-dimensional GFPT

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C[1+\sqrt{\beta\Delta}/\varepsilon_g]
$$

**Sources.** [3](https://arxiv.org/abs/2310.09157)

**Conditions.** $d=2, \varepsilon_g^2<2\beta\Delta$

**Dimension conditions.** $d=2, \varepsilon_g^2<2\beta\Delta$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [3](https://arxiv.org/abs/2310.09157) theorem: Theorem4.1; pdf pages: 9

### B13 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_g^2\ge 2\beta\Delta$

**Dimension conditions.** $\varepsilon_g^2\ge 2\beta\Delta$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

### B14 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon_g^2\ge 2\beta\Delta$

**Dimension conditions.** $\varepsilon_g^2\ge 2\beta\Delta$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

## 5. Local arguments

### A1 - Simultaneous regularity budgets and common lower-bound scaling

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

**Sources.** [5](https://arxiv.org/abs/1710.11606v3)

### A2 - High-order regularized descent with full parameter dependence

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

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

### A3 - Zero-query and polynomial-recovery endpoints

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

[3] Alexandros Hollender; Manolis Zampetakis. The Computational Complexity of Finding Stationary Points in Non-Convex Optimization. arXiv:2310.09157v2, 2024-09-11; extended abstract COLT 2023.

https://arxiv.org/abs/2310.09157

[4] Huanjian Zhou; Taiji Suzuki. On the Complexity of Finding Stationary Points of p-th Order Hölder Smooth Functions in One Dimension. arXiv:2610.16295v1, 2026-10-12, preprint.

https://arxiv.org/abs/2610.16295

[5] Yair Carmon, John C. Duchi, Oliver Hinder, Aaron Sidford. Lower Bounds for Finding Stationary Points I. arXiv:1710.11606v3; Mathematical Programming 184 (2020).

https://arxiv.org/abs/1710.11606v3
