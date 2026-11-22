# Convex minimization with complete exact higher-order derivatives: full-space queries

**Setting ID.** `SO_HO_HOC01_S_full`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Logarithmic gap present; Bounds missing

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Kth derivative lipschitz

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Full jet; operation: Exact jet k; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is convex and $C^k$, with $k\ge2$.



$$
\|D^{k}f(x)-D^{k}f(y)\|_{\mathrm{op},2}\le M_k\|x-y\|_{2}.
$$



There exists a global minimizer $x^*$ satisfying $\|x^*-x_0\|_2\le R$.

The highest-order regularity condition does not include uniform bounds on lower derivatives or a gradient-smoothness bound.

### Oracle interface

Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $M_k$, $R$, $\varepsilon_f$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is



$$
\mathcal{E}(\widehat{x})=f(\widehat{x})-f^*.
$$



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



$$
f(\widehat{x})-f^*\le \varepsilon_f.
$$



The running-cost guarantee is specified separately under RESOURCE.

#### Randomized

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.



$$
\Pr\!\left[f(\widehat{x})-f^*\le \varepsilon_f\right]\ge\frac23.
$$



Expectation or probability is evaluated after fixing the instance; randomness comes from the algorithm's private random seed.

The running-cost guarantee is specified separately under RESOURCE.

The sole current positive-parameter bracket is randomized c4, with upper $O_k(1+\min\{Q_f^{a_k},d\log(2+Q_f)\})$. The weaker randomized c1 is retained in provenance.comparison_history, routes to c4, and is excluded from active comparisons, summary counts and research tasks. Its source bound b1 remains available and contributes to the minimum envelope; no lower bound has been added.

## 2. Notation and parameters

$x,\widehat{x},x_0$: Query or decision point, algorithm output, and public initial point. **Domain:** $\mathbb{R}^d$.

$\mathbb{R}^d$: Real coordinate space; vectors use the Euclidean norm unless otherwise stated. **Domain:** $d$ is a positive integer.

$\langle u,v\rangle,\ \|u\|_2$: Euclidean inner product and norm.



$$
\langle u,v\rangle=u^\top v,\qquad\|u\|_2=\sqrt{\langle u,u\rangle}.
$$



$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,k\}$ and $D^0f=f$.

$\|T\|_{\mathrm{op}},\ \|T\|_{\mathrm{op},2}$: Induced operator norm of a Euclidean multilinear tensor; the spectral norm for matrices.



$$
\|T\|_{\mathrm{op}}=\|T\|_{\mathrm{op},2}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|.
$$



$\mathcal{E}$: Base error defined in the metric specification; expectation or probability aggregation is imposed by the guarantee.

$N$: Total number of original oracle calls; the unit cost is specified in the resource convention. **Domain:** $N\in\mathbb{Z}_{\ge0}$.

$T^*$: Minimum worst-case budget for one algorithm to meet the requirement on the full instance class, within the specified regime, guarantee and resource projection. Expected-resource specifications instead minimize the per-instance expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching bounds up to constants, and upper bounds omitting the declared logarithmic factors. **Domain:** Hidden constants, fixed parameters, and omitted logarithmic variables are specified for each bound.

$\inf,\sup,\min,\max$: Infimum, supremum, attained minimum and attained maximum.

$c,C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<c,C<\infty$.

$J_{k}f(x)$: Function value and the complete tuple of derivatives from order one through the specified maximum order.



$$
J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x)).
$$



$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.



$$
f^*=\inf_{x\in \mathbb{R}^d}f(x).
$$



$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{+}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}, k\ge2$.

$M_k$: Global Lipschitz upper bound for the order-$k$ derivative in the tensor operator norm. **Domain:** $M_k\ge0$.

$R$: Upper bound on the distance from the known initial point to at least one global minimizer. **Domain:** $R\ge0$.

$\varepsilon_f$: Objective-gap tolerance **Domain:** $\varepsilon_f>0$.

$a_k$: Complexity exponent associated with the highest-order regularity. **Domain:** $a_k>0$.



$$
a_k=\frac{2}{3\,k+1}.
$$



$C_{k}$: Sufficient window constants depending only on the fixed orders or exponents in their subscripts; existence is asserted without numerical values. **Domain:** $C_{k}>1$.

$Q_f$: Dimensionless ratio formed from the highest-order regularity, localization radius, and objective-value accuracy. **Domain:** $Q_f\ge0$.



$$
Q_f=\frac{M_k\,((R)^{k+1})}{\varepsilon_f}.
$$



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

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Scope.** declared_joint_parameter_window

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

### R1 - Sufficient dimension for the deterministic chain

**Region.** $d\ge C_k(1+Q_f^{a_k})$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega_k(1+Q_f^{a_k})
$$

**Upper bound.** B1

$$
O_k(1+Q_f^{a_k})
$$

**Gap or comparison.** $O_k(1)$

### R2 - The localization or feasible ball degenerates to the initial point

**Region.** $R=0$

**Views.** Deterministic; Randomized

**Quantity.** Q2; Q4

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B4, B11

$$
0
$$

**Upper bound.** B3, B10

$$
0
$$

### R3 - Zero highest-order regularity modulus

**Region.** $M_k=0,\ R>0$

**Views.** Deterministic; Randomized

**Quantity.** Q2; Q4

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B6, B13

$$
1
$$

**Upper bound.** B5, B12

$$
1
$$

**Gap or comparison.** $1$

### R4 - Finite-dimensional truncation: the tensor power does not exceed the dimension

**Region.** $d\ge Q_f^{a_k}$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B8

$$
\Omega_k(1+\min\{d,Q_f^{a_k}\})
$$

**Upper bound.** B1, B7

$$
O_k(1+\min\{Q_f^{a_k},d\log(2+Q_f)\})
$$

**Gap or comparison.** $O_k(1)$

**Comparison argument.** The finite-dimensional argument treats legal queries, boundary minimizers, and arbitrary unqueried outputs separately for each domain. Compare the two verified envelopes according to the relative sizes of d and Q^a.

### R5 - Finite-dimensional high-accuracy regime

**Region.** $1\le d<Q_f^{a_k}$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Logarithmic gap

**Lower bound.** B8

$$
\Omega_k(1+\min\{d,Q_f^{a_k}\})
$$

**Upper bound.** B1, B7

$$
O_k(1+\min\{Q_f^{a_k},d\log(2+Q_f)\})
$$

**Gap or comparison.** $O_k(\min\{Q_f^{a_k}/d,\log(2+Q_f)\})$

**Comparison argument.** The finite-dimensional argument treats legal queries, boundary minimizers, and arbitrary unqueried outputs separately for each domain. Compare the two verified envelopes according to the relative sizes of d and Q^a.

### R6 - Positive-parameter domain

**Region.** $M_k,R,\varepsilon_f>0,\ d\ge1$

**Views.** Randomized

**Quantity.** Q3

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B9, B14

$$
O_k(1+\min\{Q_f^{a_k},d\log(2+Q_f)\})
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Higher-order tensor acceleration without bisection search

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O_k(1+Q_f^{a_k})
$$

**Sources.** [1](https://arxiv.org/pdf/2205.09647v1)

**Conditions.** $M_k,R,\varepsilon_f>0,\ d\ge1$

**Dimension conditions.** $M_k,R,\varepsilon_f>0,\ d\ge1$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [1](https://arxiv.org/pdf/2205.09647v1) theorem: Theorem 5, Eq. (32); actual oracle accounting; pdf pages: 9

### B2 - Resisting rotations of a high-order chain, including the unqueried output

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega_k(1+Q_f^{a_k})
$$

**Conditions.** $d\ge C_k(1+Q_f^{a_k})$

**Dimension conditions.** $d\ge C_k(1+Q_f^{a_k})$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1

### B3 - Return the public initial point

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

**Local argument.** A2

### B4 - Nonnegativity of oracle cost

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

**Local argument.** A2

### B5 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_k=0,\ R>0$

**Dimension conditions.** $M_k=0,\ R>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A2

### B6 - Two admissible instances indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $M_k=0,\ R>0$

**Dimension conditions.** $M_k=0,\ R>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A2

### B7 - Exact centroid cuts on $C_0=B\cap\{U\le\min_B U+2\delta_0\}$; internal model optimization, integration and global computation are free

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O_k(1+d\log(2+Q_f))
$$

**Sources.** [2](https://arxiv.org/pdf/2411.08987v2) [3](https://msp.org/pjm/1960/10-4/pjm-v10-n4-p18-s.pdf) [1](https://arxiv.org/pdf/2205.09647v1)

**Conditions.** $M_k,R,\varepsilon_f>0,\ d\ge1$

**Dimension conditions.** $M_k,R,\varepsilon_f>0,\ d\ge1$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3, A1, A4

### B8 - Dimension-truncated high-order resisting chain

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega_k(1+\min\{d,Q_f^{a_k}\})
$$

**Conditions.** $M_k,R,\varepsilon_f>0,\ d\ge1$

**Dimension conditions.** $M_k,R,\varepsilon_f>0,\ d\ge1$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A5, A2

### B9 - Higher-order tensor acceleration without bisection search

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O_k(1+Q_f^{a_k})
$$

**Sources.** [1](https://arxiv.org/pdf/2205.09647v1)

**Conditions.** $M_k,R,\varepsilon_f>0,\ d\ge1$

**Dimension conditions.** $M_k,R,\varepsilon_f>0,\ d\ge1$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [1](https://arxiv.org/pdf/2205.09647v1) theorem: Theorem 5, Eq. (32); actual oracle accounting; pdf pages: 9

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

**Local argument.** A2

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

**Local argument.** A2

### B12 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_k=0,\ R>0$

**Dimension conditions.** $M_k=0,\ R>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A2

### B13 - Two admissible instances indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $M_k=0,\ R>0$

**Dimension conditions.** $M_k=0,\ R>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A2

### B14 - Exact centroid cuts on $C_0=B\cap\{U\le\min_B U+2\delta_0\}$; internal model optimization, integration and global computation are free

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O_k(1+d\log(2+Q_f))
$$

**Sources.** [2](https://arxiv.org/pdf/2411.08987v2) [3](https://msp.org/pjm/1960/10-4/pjm-v10-n4-p18-s.pdf) [1](https://arxiv.org/pdf/2205.09647v1)

**Conditions.** $M_k,R,\varepsilon_f>0,\ d\ge1$

**Dimension conditions.** $M_k,R,\varepsilon_f>0,\ d\ge1$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3, A1, A4

## 5. Local arguments

### A1 - A dimension-controlled convex high-order resisting chain

**Scope.** Arbitrary deterministic complete-jet algorithms, including unqueried outputs. No randomized lower bound follows from the resisting-rotation argument. Constants depend only on fixed derivative order and Hölder exponent.

**Algorithm scope.** Arbitrary deterministic complete-jet algorithms, including unqueried outputs. No randomized lower bound follows from the resisting-rotation argument. Constants depend only on fixed derivative order and Hölder exponent.

For fixed $s=k+\nu>2$, the construction gives deterministic lower bounds for objective accuracy and gradient norm, including arbitrary unqueried outputs.

For $N\ge2$, define


$$
h_N(z)=\frac1s\left(\sum_{i=1}^{N-1}|z_i-z_{i+1}|^s+|z_N|^s\right)-z_1.
$$


Let $A$ be the forward-difference matrix with a terminal row. Its Euclidean operator norm is at most two. The first $k$ derivatives of $|u|^s/s$ vanish at zero, and its kth derivative has a $\nu$-Hölder modulus depending only on $k,\nu$. Applying Hölder's inequality with exponents $s/\nu,s,\ldots,s$ gives


$$
|[D^kh_N(z)-D^kh_N(w)][u_1,\ldots,u_k]|
\le H_{k,\nu}\|z-w\|_2^\nu\prod_j\|u_j\|_2,
$$


with $H_{k,\nu}$ independent of $N$.

The minimizer is $z^*=(N,N-1,\ldots,1)$, with


$$
h_N(0)-h_N(z^*)=(s-1)N/s,\qquad
\|z^*\|^2=N(N+1)(2N+1)/6.
$$


If $z_{t+1}=\cdots=z_N=0$, then the remaining chain gives


$$
h_N(z)-h_N(z^*)\ge(s-1)(N-t)/s,\qquad
\|\nabla h_N(z)\|\ge1/\sqrt{t+1}.
$$


For the gradient inequality, the first $t+1$ gradient coordinates sum to $-1$, and Cauchy–Schwarz applies.

For any deterministic adaptive algorithm making $T$ queries, select orthonormal chain directions successively, orthogonal to previous directions and the query displacements seen so far. Vanishing derivatives of unrevealed terms ensure that each complete jet exposes at most the next direction. After the output is determined, choose the remaining hidden directions orthogonal to that output too. The sufficient dimension $d\ge N+T+1$ leaves room for these choices. The final function


$$
f(x)=\alpha h_N(V^\top(x-x_0)/b)
$$


is one fixed admissible instance consistent with the entire transcript. This construction does not select a separate instance after seeing a randomized algorithm's private seed.

For a radius promise, take $b=R/\|z^*\|$ and $\alpha=M_{k,\nu}b^s/H_{k,\nu}$. Choosing $N=2T+2$ for objective gap or $N=T+2$ for gradient norm gives


$$
\begin{aligned}&\operatorname{gap}(T)\ge\frac{c_{k,\nu}M_{k,\nu}R^s}{(T+1)^{(3s-2)/2}},\\[3pt]&\operatorname{grad}_R(T)\ge\frac{c_{k,\nu}M_{k,\nu}R^{s-1}}{(T+1)^{(3s-2)/2}}.\end{aligned}
$$


For an initial-gap promise, set $\alpha=\Delta s/((s-1)N)$ and $b=(\alpha H_{k,\nu}/M_{k,\nu})^{1/s}$. Then


$$
\operatorname{grad}_\Delta(T)\ge\frac{c_{k,\nu}M_{k,\nu}^{1/s}\Delta^{(s-1)/s}}{(T+1)^{(3s-2)/(2s)}}.
$$


Inverting these inequalities yields the linked bounds with a sufficient dimension proportional to one plus the complexity scale. The minimizer lies in the localization ball, so the same hard subclass is admissible for ball-restricted optimization.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

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

### A3 - Public convex constraints and composite terms

**Scope.** Applies only where the auxiliary operations are explicitly permitted. Does not merge distinct oracle interfaces or impose a lower bound on a publicly known singleton feasible domain.

**Algorithm scope.** Applies only where the auxiliary operations are explicitly permitted. Does not merge distinct oracle interfaces or impose a lower bound on a publicly known singleton feasible domain.

The convex high-order proximal analysis transfers to a public proper closed convex term when the declared auxiliary interface solves known composite models globally.

For $F=f+\psi$, solve the known model


$$
T_k(f;x,y)+\psi(y)+CM\|y-x\|^s.
$$


At a global model minimizer y, model optimality supplies a compatible $v_\psi\in\partial\psi(y)$. Then $v=\nabla f(y)+v_\psi$ is a subgradient of F, and the residual relative to the model's regularization gradient is exactly the Taylor-gradient error of f. The subgradient support inequality and Bregman three-point identity used in the convex accelerated framework therefore remain valid. Mirror subproblems also stay in the effective domain of $\psi$, and queries are convex combinations of known feasible points, preserving ball-restricted access.

This transfer requires global solution of the known high-order composite model and mirror subproblems, including a compatible subgradient or normal-cone selection. An ordinary projection, ordinary proximal map, or linear-minimization oracle alone does not automatically supply that capability. Unknown objective values or gradients requested at candidate points cost additional complete jets; at most a constant number per iteration preserves the stated order. The primary theorem's phrase 'one highest-order call per iteration' does not make other unknown-function information free.

For lower bounds on the family of permitted public regularizers, choose the subclass $\psi=0$ and use the convex resisting chain. This is a family-level inclusion argument, not a lower bound for every individually fixed special regularizer or feasible set.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [2](https://arxiv.org/pdf/2411.08987v2)

### A4 - Finite-dimensional convex upper bound by centroid cuts

**Scope.** Deterministic complete-jet algorithms, also valid as upper-bound witnesses in randomized views. Internal centroid, convex-body, and known-model computations are free in oracle accounting; arithmetic complexity is not claimed.

**Algorithm scope.** Deterministic complete-jet algorithms, also valid as upper-bound witnesses in randomized views. Internal centroid, convex-body, and known-model computations are free in oracle accounting; arithmetic complexity is not claimed.

For fixed $k\ge2$, $R,M_k>0$, complete jets give $O_k(1+d\log(2+M_kR^{k+1}/\varepsilon_f))$ calls, both with unrestricted queries and with queries restricted to the public ball.

For unrestricted queries with a global minimizer within R of $x_0$, use the internal ball $B=B_2(x_0,2R)$. For ball-restricted optimization, use $B=B_2(x_0,R)$ itself. The second case permits a constrained boundary minimizer and never queries the larger ball. Let b be the radius of B.

Query one jet at $x_0$ and define


$$
U(y)=T_k(f;x_0,y)+\frac{kM_k}{(k+1)!}\|y-x_0\|^{k+1}.
$$


The value remainder gives $0\le U(y)-f(y)\le M_k\|y-x_0\|^{k+1}/k!$. The Hessian remainder gives


$$
\nabla^2T_k(y)\succeq-\frac{M_k}{(k-1)!}\|y-x_0\|^{k-1}I.
$$


The regularizer's Hessian contains the opposite scalar-matrix term plus a positive semidefinite rank-one term. Thus U is convex on B, including the continuous extension at $x_0$. This argument uses only segments within the legal ball.

Set $\delta_0=M_kb^{k+1}/k!$, $u=\min_B U$, and $C_0=B\cap\{U\le u+2\delta_0\}$. These are known after one jet and can be computed through free internal geometry. An optimum $x^*$ lies in $C_0$, and every z in $C_0$ satisfies $f(z)-f^*\le3\delta_0$. The body is full-dimensional even if $x^*$ lies on the boundary: move a small positive distance from $x^*$ toward any interior point of B. Continuity preserves the strict U-sublevel inequality, producing an interior ball in $C_0$. No quantitative inradius bound is needed.

For $0<\varepsilon_f<3\delta_0$, let $\lambda=\varepsilon_f/(3\delta_0)$ and $K_\varepsilon=\{y\in C_0:f(y)-f^*\le\varepsilon_f\}$. Convexity implies


$$
x^*+\lambda(C_0-x^*)\subseteq K_\varepsilon,\qquad
\operatorname{vol}(K_\varepsilon)\ge\lambda^d\operatorname{vol}(C_0).
$$


This affine volume formula holds equally for boundary $x^*$.

At the centroid $c_t$ of $C_t$, query a complete jet. A zero gradient certifies optimality. Otherwise retain the halfspace $\langle\nabla f(c_t),y-c_t\rangle\le0$. Grünbaum's centroid theorem ensures that each cut leaves at most $\rho=1-e^{-1}$ of the previous volume. Queries remain in B. If every queried centroid has gap greater than $\varepsilon_f$, convexity makes every cut retain all of $K_{\varepsilon}$. Consequently $\lambda^d\le\rho^N$, a contradiction once


$$
N>\frac{d\log(3\delta_0/\varepsilon_f)}{-\log\rho}.
$$


Run this public fixed number of iterations and return the queried point with smallest exact value. No knowledge of $f^*$ or free success test is needed. If $\varepsilon_f\ge\delta_0$, the minimizer of U already meets the target after the initial jet.

This proves the displayed finite-dimensional bound. Taking the minimum with the applicable accelerated tensor upper bound gives


$$
O_k\left(1+\min\{Q^{2/(3k+1)},d\log(2+Q)\}\right),\qquad Q=M_kR^{k+1}/\varepsilon_f.
$$


For ball-restricted tensor acceleration, the public-domain composite transfer must also be permitted. The centroid branch itself does not depend on that transfer.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [3](https://msp.org/pjm/1960/10-4/pjm-v10-n4-p18-s.pdf) [1](https://arxiv.org/pdf/2205.09647v1)

### A5 - Finite-dimensional deterministic truncation

**Scope.** Arbitrary deterministic complete-jet algorithms, all finite $d\ge1$, positive $M_k$ and R. The same one-query argument handles zero modulus separately.

**Algorithm scope.** Arbitrary deterministic complete-jet algorithms, all finite $d\ge1$, positive $M_k$ and R. The same one-query argument handles zero modulus separately.

The deterministic complete-jet lower bound is $\Omega_k(1+\min\{d,Q^{2/(3k+1)}\})$ for $Q=M_kR^{k+1}/\varepsilon_f$.

Use the convex chain with $s=k+1$ and $N=2T+2$. Its kth-derivative Lipschitz modulus is at most $H_k=2^{k+1}k!$, independent of N, and its minimizer has norm at most $N^{3/2}$. The adaptive orthogonal construction, including the final unqueried output, needs only $d\ge N+T+1=3T+3$.

Scale with $b=R/\|z^*\|$ and $\alpha=M_kb^{k+1}/H_k$. The final fixed instance has a global minimizer at distance exactly R, so it belongs both to the unrestricted localization class and to the ball-domain hard subclass. Its output gap is at least


$$
\gamma_k\frac{M_kR^{k+1}}{(T+1)^{(3k+1)/2}},\qquad
\gamma_k=\frac{k}{2(k+1)H_k2^{(3k+1)/2}}.
$$


Choose T as a sufficiently small k-dependent multiple of $\min\{d,Q^{2/(3k+1)}\}$, rounded down. Whenever that minimum is sufficiently large, both the dimension condition and failure inequality hold.

For $d=1,2$ or a bounded minimum, use two translated positive quadratics with minimizers at $x_0\pm R e_1$ and enough common curvature to make their acceptable sets disjoint. Their kth-derivative Lipschitz modulus is zero, so they satisfy every nonnegative $M_k$ budget. At least one query is necessary. This fills the small-dimension and small-budget endpoints and yields the full lower bound with its additive one-query term.

With the finite-dimensional upper bound, the ratio is at most a constant times


$$
\frac{1+\min\{Q^{2/(3k+1)},d\log(2+Q)\}}{1+\min\{Q^{2/(3k+1)},d\}}.
$$


It is constant in the sufficient region $d\ge Q^{2/(3k+1)}$ and at most logarithmic elsewhere. The proof does not show that the logarithm is necessary, nor does it supply the same truncation lower bound for randomized algorithms.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

## References

[1] Dmitry Kovalev; Alexander Gasnikov. The First Optimal Acceleration of High-Order Methods in Smooth Convex Optimization. arXiv:2205.09647v1; NeurIPS 2022.

https://arxiv.org/pdf/2205.09647v1

[2] Juan Pablo Contreras; Cristóbal Guzmán; David Martínez-Rubio. Non-Euclidean High-Order Smooth Convex Optimization. arXiv:2411.08987v2 (2025-02-06); COLT 2025 extended abstract.

https://arxiv.org/pdf/2411.08987v2

[3] Branko Grünbaum. Partitions of mass-distributions and of convex bodies by hyperplanes. Pacific Journal of Mathematics 10(4), 1257–1261 (1960).

https://msp.org/pjm/1960/10-4/pjm-v10-n4-p18-s.pdf
