# Convex minimization with higher-order Hölder regularity: queries in an infinity-norm ball

**Setting ID.** `SO_HO_HOC07_S_inf`

Single-objective optimization

Solve $\min_{x\in Q}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Full space; geometry: Norm ball; smoothness: Kth derivative holder

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Full jet; operation: Exact jet k; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in Q}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f$ is convex and $C^k$ on an open convex neighborhood of the closed ball $Q=\{x\in\mathbb{R}^d:\|x-x_0\|_{\infty}\le R\}$. The optimization domain is $Q$.

$$\|D^{k}f(x)-D^{k}f(y)\|_{\mathrm{op},\infty}\le M_{k,\nu}\|x-y\|_{\infty}^{\nu}.$$

Fix $k\ge2$ and $0<\nu\le1$; the tensor norm is induced by the stated vector norm.

### Oracle interface

Each query selects $x$ in $Q$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

A description of the feasible set, feasibility tests and global minimization of known models formed from existing replies are supplied as public auxiliary operations.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $M_{k,\nu}$, $\nu$, $R$, $\varepsilon_f$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in Q$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=f(\widehat{x})-f^*.$$

Here $f^*=\inf_{x\in Q}f(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

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

$$f^*=\inf_{x\in Q}f(x).$$

$Q$: The feasible set specified by the model, also used as the query and output domain. Convexity or ball geometry is assumed only when stated in the model.

$\|x\|_p,\ \|x\|_\infty$: Finite-exponent vector norms and the maximum-coordinate norm.

$$\|x\|_p=\left(\sum_{i=1}^d|x_i|^p\right)^{1/p},\qquad\|x\|_\infty=\max_i|x_i|.$$

$\|T\|_{\mathrm{op},p}$: Replace every Euclidean unit ball in the tensor operator-norm definition by the $\ell_p$ unit ball; define $p=\infty$ analogously.

$p$: This specification uses the maximum norm. **Domain:** $p=\infty$.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{+}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}, k\ge2$.

$M_{k,\nu}$: Global $\nu$-Hölder upper bound for the order-$k$ derivative in the specified tensor norm. **Domain:** $M_{k,\nu}\ge0$.

$\nu$: Hölder exponent of the highest derivative **Domain:** $0<\nu\le1$.

$s$: Sum of the highest derivative order and its Hölder exponent. **Domain:** $s>2$.

$$s=k+\nu.$$

$R$: Radius of the known ball. **Domain:** $R\ge0$.

$\varepsilon_f$: Objective-gap tolerance **Domain:** $\varepsilon_f>0$.

$a$: Complexity exponent associated with the highest-order regularity. **Domain:** $a>0$.

$$a=\frac{2}{3\,s-(2)}.$$

$C_{k,\nu,p}$: Sufficient window constant depending only on $k,\nu$ after fixing the maximum-norm geometry $p=\infty$; not assigned a numerical value. **Domain:** $C_{k,\nu,p}>1$.

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

### R1 - Sufficient dimension for deterministic queries in an infinity-norm ball

**Region.** $p=\infty\ \text{(separate specification)},\ \mathcal{Q}\ge C,\ d\ge C(1+\mathcal{Q}^{1/(s-1)})$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega_{k,\nu}(\mathcal{Q}^{1/(s-1)}/\log(ed))
$$

**Upper bound.** B1

$$
O_{k,\nu}(1+\mathcal{Q}^{1/(s-1)})
$$

**Gap or comparison.** $O_{k,\nu}(\log(ed))$

### R2 - The localization or feasible ball degenerates to the initial point

**Region.** $R=0$

**Views.** Deterministic; Randomized

**Quantity.** Q2; Q4

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B4, B10

$$
0
$$

**Upper bound.** B3, B9

$$
0
$$

### R3 - Zero highest-order regularity modulus

**Region.** $M_{k,\nu}=0,\ R>0$

**Views.** Deterministic; Randomized

**Quantity.** Q2; Q4

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B6, B12

$$
1
$$

**Upper bound.** B5, B11

$$
1
$$

**Gap or comparison.** $1$

### R4 - Sufficient dimension for randomized queries in an infinity-norm ball

**Region.** $p=\infty\ \text{(separate specification)},\ \mathcal{Q}\ge C,\ d\ge C(1+\mathcal{Q}^{3/(s-1)})\log(2+\mathcal{Q})$

**Views.** Randomized

**Quantity.** Q3

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Logarithmic gap

**Lower bound.** B8

$$
\Omega_{k,\nu}(\mathcal{Q}^{1/(s-1)}/\log(ed))
$$

**Upper bound.** B7

$$
O_{k,\nu}(1+\mathcal{Q}^{1/(s-1)})
$$

**Gap or comparison.** $O_{k,\nu}(\log(ed))$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $Q$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Output mapping.** Return $\widehat{x}\in Q$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Nonaccelerated regularized Taylor method on a bounded ball

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu}(1+\mathcal{Q}^{1/(s-1)})
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $M_{k,\nu},R,\varepsilon_f>0,\ 0<\nu\le1$

**Dimension conditions.** $M_{k,\nu},R,\varepsilon_f>0,\ 0<\nu\le1$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [1](https://arxiv.org/pdf/2411.08987v2) theorem: Appendix D, Theorem 23; pdf pages: 32

### B2 - Orthogonal-coordinate hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
\Omega_{k,\nu}(\mathcal{Q}^{1/(s-1)}/\log(ed))
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $p=\infty\ \text{(separate specification)},\ \mathcal{Q}\ge C,\ d\ge C(1+\mathcal{Q}^{1/(s-1)})$

**Dimension conditions.** $p=\infty\ \text{(separate specification)},\ \mathcal{Q}\ge C,\ d\ge C(1+\mathcal{Q}^{1/(s-1)})$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [1](https://arxiv.org/pdf/2411.08987v2) theorem: Theorem 16 and Appendix E.1, p=∞; pdf pages: 41

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

**Local argument.** A1

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

**Local argument.** A1

### B5 - Recover a polynomial from one complete derivative reply

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

**Local argument.** A1

### B6 - Two admissible instances indistinguishable without queries

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

**Local argument.** A1

### B7 - Nonaccelerated regularized Taylor method on a bounded ball

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu}(1+\mathcal{Q}^{1/(s-1)})
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $M_{k,\nu},R,\varepsilon_f>0,\ 0<\nu\le1$

**Dimension conditions.** $M_{k,\nu},R,\varepsilon_f>0,\ 0<\nu\le1$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [1](https://arxiv.org/pdf/2411.08987v2) theorem: Appendix D, Theorem 23; pdf pages: 32

### B8 - Randomized hard family based on Rademacher blocks

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_{k,\nu}(\mathcal{Q}^{1/(s-1)}/\log(ed))
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $p=\infty\ \text{(separate specification)},\ \mathcal{Q}\ge C,\ d\ge C(1+\mathcal{Q}^{3/(s-1)})\log(2+\mathcal{Q})$

**Dimension conditions.** $p=\infty\ \text{(separate specification)},\ \mathcal{Q}\ge C,\ d\ge C(1+\mathcal{Q}^{3/(s-1)})\log(2+\mathcal{Q})$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [1](https://arxiv.org/pdf/2411.08987v2) theorem: Theorem 26 and Appendix E.2, p=∞; pdf pages: 42

### B9 - Return the public initial point

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

**Local argument.** A1

### B10 - Nonnegativity of oracle cost

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

**Local argument.** A1

### B11 - Recover a polynomial from one complete derivative reply

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

**Local argument.** A1

### B12 - Two admissible instances indistinguishable without queries

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

**Local argument.** A1

## 5. Local arguments

### A1 - Zero-query and polynomial-recovery endpoints

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

[1] Juan Pablo Contreras; Cristóbal Guzmán; David Martínez-Rubio. Non-Euclidean High-Order Smooth Convex Optimization. arXiv:2411.08987v2 (2025-02-06); COLT 2025 extended abstract.

https://arxiv.org/pdf/2411.08987v2
