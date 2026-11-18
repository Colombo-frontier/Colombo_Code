# Strongly convex objective accuracy under joint gradient and Hessian regularity

**Setting ID.** `SO_HO_HOC04_S`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Logarithmic gap present; Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz gradient; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Full jet; operation: Exact jet 2; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is $C^2$ and satisfies $\mu I_d\preceq\nabla^2f(x)\preceq\beta I_d$ at every point, where $0<\mu\le\beta$.

$$\|D^{2}f(x)-D^{2}f(y)\|_{\mathrm{op},2}\le M_2\|x-y\|_{2}.$$

There exists a global minimizer $x^*$ satisfying $\|x^*-x_0\|_2\le R$.

### Oracle interface

Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The public inputs are $x_0$, the target accuracy, and $d$, $M_2$, $R$, $\varepsilon_f$, $\mu$, $\beta$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

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

$J_{2}f(x)$: Function value and the complete tuple of derivatives from order one through the specified maximum order.

$$J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x)).$$

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$I_d$: The identity matrix in dimension $d$.

$A\preceq B$: Loewner order: the symmetric matrix $B-A$ is positive semidefinite.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{+}$.

$M_2$: Global upper bound on the Hessian Lipschitz constant. **Domain:** $M_2\ge0$.

$R$: Upper bound on the distance from the known initial point to at least one global minimizer. **Domain:** $R\ge0$.

$\varepsilon_f$: Objective-gap tolerance **Domain:** $\varepsilon_f>0$.

$\mu$: Admissible positive lower bound on the strong-convexity modulus **Domain:** $\mu>0$.

$\beta$: Upper bound on the gradient Lipschitz modulus **Domain:** $\beta>0$.

$C$: Sufficient window constants depending only on the fixed orders or exponents in their subscripts; existence is asserted without numerical values. **Domain:** $C>1$.

$c$: Sufficient window constants depending only on the fixed orders or exponents in their subscripts; existence is asserted without numerical values. **Domain:** $0<c<1$.

$\kappa$: Ratio of the gradient smoothness upper bound to the strong-convexity lower bound: the condition number. **Domain:** $\kappa>0$.

$$\kappa=\frac{\beta}{\mu}.$$

$Q_\star$: Dimensionless ratio of highest-order regularity to the strong-convexity scale. **Domain:** $Q_\star\ge0$.

$$Q_\star=\frac{M_2\,R}{\mu}.$$

$E_\star$: Objective-value scale at entry to the local fast-convergence phase; used only where the highest-order regularity budget is positive. **Domain:** $E_\star>0\quad(M_2>0)$.

$$E_\star=\frac{(\mu)^{3}}{(M_2)^{2}}.$$

$d_{\rm ASS}$: Sufficient construction dimension in ASS17, Theorem 1 **Domain:** $d_{\rm ASS}>0$.

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

**View.** Randomized

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

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Second-order dominated branch

**Region.** $Q_\star^{2/7}\le\sqrt\kappa$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B3

$$
\Omega(1+\min\{Q_\star^{2/7},\sqrt\kappa\}+\log(1+\log(1+E_\star/\varepsilon_f)))
$$

**Upper bound.** B1, B2

$$
O(1+\min\{Q_\star^{2/7},\sqrt\kappa\log(2+\beta R^2/E_\star)\}+\log(1+\log(1+E_\star/\varepsilon_f)))
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** Compare within the same complete specification and common validity domain. Hidden constants may depend only on the declared fixed exponents.

### R2 - Gradient-dominated branch of the current envelope

**Region.** $Q_\star^{2/7}>\sqrt\kappa$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Logarithmic gap

**Lower bound.** B3

$$
\Omega(1+\min\{Q_\star^{2/7},\sqrt\kappa\}+\log(1+\log(1+E_\star/\varepsilon_f)))
$$

**Upper bound.** B1, B2

$$
O(1+\min\{Q_\star^{2/7},\sqrt\kappa\log(2+\beta R^2/E_\star)\}+\log(1+\log(1+E_\star/\varepsilon_f)))
$$

**Gap or comparison.** $O(\log(2+\beta R^2/E_\star))$

**Comparison argument.** Compare within the same complete specification and common validity domain. Hidden constants may depend only on the declared fixed exponents.

### R3 - The localization or feasible ball degenerates to the initial point

**Region.** $R=0$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B5, B15

$$
0
$$

**Upper bound.** B4, B14

$$
0
$$

### R4 - Zero-query regime at coarse accuracy for smooth convex objectives

**Region.** $\varepsilon_f\ge\beta R^2/2$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B7, B17

$$
0
$$

**Upper bound.** B6, B16

$$
0
$$

### R5 - Zero Hessian regularity modulus and nontrivial accuracy

**Region.** $M_2=0,\ 0<\varepsilon_f<\beta R^2/2$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B9, B19

$$
1
$$

**Upper bound.** B8, B18

$$
1
$$

**Gap or comparison.** $1$

### R6 - Equal strong-convexity and smoothness budgets

**Region.** $\beta=\mu,\ 0<\varepsilon_f<\beta R^2/2$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B11, B21

$$
1
$$

**Upper bound.** B10, B20

$$
1
$$

**Gap or comparison.** $1$

### R7 - Nondegenerate positive-parameter domain

**Region.** $0<\mu\le\beta,\ M_2,R,\varepsilon_f>0$

**Views.** Randomized

**Quantity.** Q2

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B12

$$
O(1+Q_\star^{2/7}+\log(1+\log(1+E_\star/\varepsilon_f)))
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Restarted second-order acceleration and local regularized models

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(1+Q_\star^{2/7}+\log(1+\log(1+E_\star/\varepsilon_f)))
$$

**Sources.** [2](https://arxiv.org/pdf/2205.09647v1) [3](https://arxiv.org/pdf/2010.06642v2) [1](https://arxiv.org/pdf/1705.07260v2)

**Conditions.** $0<\mu\le\beta,\ M_2,R,\varepsilon_f>0$

**Dimension conditions.** $0<\mu\le\beta,\ M_2,R,\varepsilon_f>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A2

### B2 - Accelerated gradients enter the local region, followed by regularized Newton steps

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(1+\sqrt\kappa\log(2+\beta R^2/E_\star)+\log(1+\log(1+E_\star/\varepsilon_f)))
$$

**Sources.** [2](https://arxiv.org/pdf/2205.09647v1) [3](https://arxiv.org/pdf/2010.06642v2) [1](https://arxiv.org/pdf/1705.07260v2)

**Conditions.** $\kappa,Q_\star\ge C,\ \varepsilon_f\le cE_\star,\ d\ge d_{\rm ASS}$

**Dimension conditions.** $\kappa,Q_\star\ge C,\ \varepsilon_f\le cE_\star,\ d\ge d_{\rm ASS}$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A2

### B3 - Truncated strongly convex chain

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega(1+\min\{\sqrt\kappa,Q_\star^{2/7}\}+\log(1+\log(1+E_\star/\varepsilon_f)))
$$

**Sources.** [1](https://arxiv.org/pdf/1705.07260v2)

**Conditions.** $\kappa,Q_\star\ge C,\ \varepsilon_f\le cE_\star,\ d\ge d_{\rm ASS}$

**Dimension conditions.** $\kappa,Q_\star\ge C,\ \varepsilon_f\le cE_\star,\ d\ge d_{\rm ASS}$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [1](https://arxiv.org/pdf/1705.07260v2) theorem: Theorem 1; pdf pages: 6

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

**Local argument.** A3

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

**Local argument.** A3

### B6 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_f\ge\beta R^2/2$

**Dimension conditions.** $\varepsilon_f\ge\beta R^2/2$

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

**Conditions.** $\varepsilon_f\ge\beta R^2/2$

**Dimension conditions.** $\varepsilon_f\ge\beta R^2/2$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3

### B8 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_2=0,\ 0<\varepsilon_f<\beta R^2/2$

**Dimension conditions.** $M_2=0,\ 0<\varepsilon_f<\beta R^2/2$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3

### B9 - Two admissible instances indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $M_2=0,\ 0<\varepsilon_f<\beta R^2/2$

**Dimension conditions.** $M_2=0,\ 0<\varepsilon_f<\beta R^2/2$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3

### B10 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $\beta=\mu,\ 0<\varepsilon_f<\beta R^2/2$

**Dimension conditions.** $\beta=\mu,\ 0<\varepsilon_f<\beta R^2/2$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3

### B11 - Two admissible instances indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $\beta=\mu,\ 0<\varepsilon_f<\beta R^2/2$

**Dimension conditions.** $\beta=\mu,\ 0<\varepsilon_f<\beta R^2/2$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3

### B12 - Restarted second-order acceleration and local regularized models

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(1+Q_\star^{2/7}+\log(1+\log(1+E_\star/\varepsilon_f)))
$$

**Sources.** [2](https://arxiv.org/pdf/2205.09647v1) [3](https://arxiv.org/pdf/2010.06642v2) [1](https://arxiv.org/pdf/1705.07260v2)

**Conditions.** $0<\mu\le\beta,\ M_2,R,\varepsilon_f>0$

**Dimension conditions.** $0<\mu\le\beta,\ M_2,R,\varepsilon_f>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1, A2

### B13 - Accelerated gradients enter the local region, followed by regularized Newton steps

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(1+\sqrt\kappa\log(2+\beta R^2/E_\star)+\log(1+\log(1+E_\star/\varepsilon_f)))
$$

**Sources.** [2](https://arxiv.org/pdf/2205.09647v1) [3](https://arxiv.org/pdf/2010.06642v2) [1](https://arxiv.org/pdf/1705.07260v2)

**Conditions.** $\kappa,Q_\star\ge C,\ \varepsilon_f\le cE_\star,\ d\ge d_{\rm ASS}$

**Dimension conditions.** $\kappa,Q_\star\ge C,\ \varepsilon_f\le cE_\star,\ d\ge d_{\rm ASS}$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1, A2

### B14 - Return the public initial point

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

**Local argument.** A3

### B15 - Nonnegativity of oracle cost

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

**Local argument.** A3

### B16 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_f\ge\beta R^2/2$

**Dimension conditions.** $\varepsilon_f\ge\beta R^2/2$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

### B17 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon_f\ge\beta R^2/2$

**Dimension conditions.** $\varepsilon_f\ge\beta R^2/2$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

### B18 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_2=0,\ 0<\varepsilon_f<\beta R^2/2$

**Dimension conditions.** $M_2=0,\ 0<\varepsilon_f<\beta R^2/2$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

### B19 - Two admissible instances indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $M_2=0,\ 0<\varepsilon_f<\beta R^2/2$

**Dimension conditions.** $M_2=0,\ 0<\varepsilon_f<\beta R^2/2$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

### B20 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $\beta=\mu,\ 0<\varepsilon_f<\beta R^2/2$

**Dimension conditions.** $\beta=\mu,\ 0<\varepsilon_f<\beta R^2/2$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

### B21 - Two admissible instances indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $\beta=\mu,\ 0<\varepsilon_f<\beta R^2/2$

**Dimension conditions.** $\beta=\mu,\ 0<\varepsilon_f<\beta R^2/2$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

## 5. Local arguments

### A1 - A dimension-controlled convex high-order resisting chain

**Scope.** Arbitrary deterministic complete-jet algorithms, including unqueried outputs. No randomized lower bound follows from the resisting-rotation argument. Constants depend only on fixed derivative order and Hölder exponent.

**Algorithm scope.** Arbitrary deterministic complete-jet algorithms, including unqueried outputs. No randomized lower bound follows from the resisting-rotation argument. Constants depend only on fixed derivative order and Hölder exponent.

For fixed $s=k+\nu>2$, the construction gives deterministic lower bounds for objective accuracy and gradient norm, including arbitrary unqueried outputs.

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

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

### A2 - Strongly convex high-order restarting and local refinement

**Scope.** Complete-jet oracle complexity with free global solution of known regularized models. Deterministic upper bounds remain available in randomized views. Lower bounds retain their own algorithm and dimension scopes.

**Algorithm scope.** Complete-jet oracle complexity with free global solution of known regularized models. Deterministic upper bounds remain available in randomized views. Lower bounds retain their own algorithm and dimension scopes.

For fixed $k\ge2$, geometric radius reduction gives a global cost of order $1+(M_kR^{k-1}/\mu)^{2/(3k+1)}$, followed by a double-logarithmic local phase.

The primary input is the convex complete-jet bound $C_k[1+(M_kr^{k+1}/\eta)^{2/(3k+1)}]$ when a minimizer lies within radius $r$ (Kovalev–Gasnikov, Theorem 5). Write $M=M_k$, $a=2/(3k+1)$, $r_*=(\mu/M)^{1/(k-1)}$, $E_* =\mu r_*^2$, and $Q_*=MR^{k-1}/\mu$.

At radius $r_j=2^{-j}R$, solve to gap $\eta_j=\mu r_j^2/8$. Strong convexity reduces the next distance to at most $r_j/2$. Until $r_j$ reaches a sufficiently small fixed multiple of $r_*$, the total cost is
$$\sum_j C_k[1+(Q_*2^{-j(k-1)})^a]\le C_k(1+Q_*^a).$$
The number of stages is absorbed by this geometric-series bound, so no extra global logarithm is introduced.

At a current point $x$, globally minimize the known upper model
$$U_x(y)=T_k(f;x,y)+\frac{kM}{(k+1)!}\|y-x\|^{k+1}.$$
Taylor's remainder ensures $U_x\ge f$ and, for a model minimizer $y$,
$$f(y)-f^*\le U_x(x^*)-f(x^*)\le\frac M{k!}\|x-x^*\|^{k+1}.$$
Once within the local radius, this gives a small constant multiple of $E_*$. Subsequent gaps obey
$$e_+\le\frac M{k!}(2e/\mu)^{(k+1)/2}.$$
The normalized exponent exceeds one, yielding $O_k(1+\log(1+\log(1+E_*/\varepsilon_f)))$ further calls. No absolute bound on lower-order derivatives at the optimum is used, and every restart length can be fixed from public parameters.

For the deterministic global lower bound, add $\mu\|x-x_0\|^2/2$ to the convex chain. Its new minimizer remains within radius $R$, and the output gap is at least
$$\frac{c_kMR^{k+1}}{(T+1)^{(3k+1)/2}}-\frac{\mu R^2}{2}.$$
This excludes success when $T+1$ is a sufficiently small constant times the minimum of $(MR^{k+1}/\varepsilon_f)^a$ and $Q_*^a$. The local double-logarithmic lower bound is a separate primary result, Kornowski–Shamir, Theorem 1; it is not derived from this subtraction argument.

When an explicit gradient-smoothness budget $\beta$ is also given, accelerated-gradient entry is an alternative. Geometric restarts cost at most $O(\sqrt{\beta/\mu}\log(2+R/r_*))$ before the same local model phase. For $k=2$, this is the alternative entry branch recorded in the linked bounds; use its full stated logarithm and parameter window.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [2](https://arxiv.org/pdf/2205.09647v1) [3](https://arxiv.org/pdf/2010.06642v2) [1](https://arxiv.org/pdf/1705.07260v2)

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

[1] Yossi Arjevani; Ohad Shamir; Ron Shiff. Oracle Complexity of Second-Order Methods for Smooth Convex Optimization. arXiv:1705.07260v2 (2017-08-17); Mathematical Programming 178 (2019).

https://arxiv.org/pdf/1705.07260v2

[2] Dmitry Kovalev; Alexander Gasnikov. The First Optimal Acceleration of High-Order Methods in Smooth Convex Optimization. arXiv:2205.09647v1; NeurIPS 2022.

https://arxiv.org/pdf/2205.09647v1

[3] Guy Kornowski; Ohad Shamir. High-Order Oracle Complexity of Smooth and Strongly Convex Optimization. arXiv:2010.06642v2 (2021-04-28).

https://arxiv.org/pdf/2010.06642v2
