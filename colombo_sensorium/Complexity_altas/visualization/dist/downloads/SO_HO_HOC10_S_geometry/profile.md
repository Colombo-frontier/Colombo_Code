# Self-concordant convex objectives: exact second derivatives with additional local geometry control

**Setting ID.** `SO_HO_HOC10_S_geometry`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Full space; smoothness: Self concordant

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Full jet; operation: Exact jet 2; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is convex and $C^3$, with an everywhere positive definite Hessian and an attained minimum. For every $x,h$,

$$|D^3f(x)[h,h,h]|\le2M_{\mathrm{sc}}\bigl(D^2f(x)[h,h]\bigr)^{3/2}.$$

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

An additional diameter bound is given for the initial sublevel set $\mathcal{S}_0=\{x:f(x)\le f(x_0)\}$ in the local norm at $x_0$:

$$\sup_{x,y\in\mathcal{S}_0}\sqrt{(x-y)^\top\nabla^2f(x_0)(x-y)}\le D_{\mathrm{sc}}.$$

### Oracle interface

Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The public inputs are $x_0$, the target accuracy, and $d$, $M_{\rm sc}$, $\Delta$, $\varepsilon_f$, $D_{\rm sc}$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

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

Arbitrary measurable adaptive deterministic algorithms are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$f(\widehat{x})-f^*\le \varepsilon_f.$$

The running-cost guarantee is specified separately under RESOURCE.

## 2. Notation and parameters

$x,\widehat{x},x_0$: Query or decision point, algorithm output, and public initial point. **Domain:** $\mathbb{R}^d$.

$\mathbb{R}^d$: Real coordinate space; vectors use the Euclidean norm unless otherwise stated. **Domain:** $d$ is a positive integer.

$\langle u,v\rangle,\ \|u\|_2$: Euclidean inner product and norm.

$$\langle u,v\rangle=u^\top v,\qquad\|u\|_2=\sqrt{\langle u,u\rangle}.$$

$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,3\}$ and $D^0f=f$.

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

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{+}$.

$M_{\rm sc}$: Self-concordance constant, with a factor of two in its definition **Domain:** $M_{\rm sc}\ge0$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta\ge0$.

$\varepsilon_f$: Objective-gap tolerance **Domain:** $\varepsilon_f>0$.

$D_{\rm sc}$: Upper bound on the diameter of the initial sublevel set in the local Hessian norm at $x_0$. **Domain:** $D_{\rm sc}<\infty$.

$\theta_{\rm sc}$: Initial objective gap normalized by the self-concordance constant. **Domain:** $\theta_{\rm sc}\ge0$.

$$\theta_{\rm sc}=(M_{\rm sc})^{2}\,\Delta.$$

$\omega,\omega^{-1}$: Self-concordant objective-value scale and its inverse on the nonnegative half-line.

$$\omega(t)=t-\log(1+t),\quad t\ge0.$$

$\theta$: Model parameters held fixed in the corresponding accuracy bound.

$$\theta=(M_{\rm sc},\Delta,D_{\rm sc}).$$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Bounded local level-set diameter

**Region.** $D_{\rm sc}<\infty$

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1, B2

$$
O(1+\min\{\theta_{\rm sc},\sqrt{\theta_{\rm sc}\log(e+M_{\rm sc}D_{\rm sc}\omega^{-1}(\theta_{\rm sc}))}\}+\log(1+\log(1+(M_{\rm sc}^2\varepsilon_f)^{-1})))
$$

### R2 - The known initial-gap bound already satisfies the target accuracy

**Region.** $\varepsilon_f\ge\Delta$

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B4

$$
0
$$

**Upper bound.** B3

$$
0
$$

### R3 - Nontrivial quadratic endpoint with a local geometry budget

**Region.** $M_{\rm sc}=0,\ 0<\varepsilon_f<\min\{\Delta,D_{\rm sc}^2/8\}$

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B6

$$
1
$$

**Upper bound.** B5

$$
1
$$

**Gap or comparison.** $1$

### R4 - Quadratic zero-query region determined jointly by local geometry and the initial gap

**Region.** $M_{\rm sc}=0,\ \varepsilon_f\ge\min\{\Delta,D_{\rm sc}^2/8\}$

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B8

$$
0
$$

**Upper bound.** B7

$$
0
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee mapping.** Deterministic-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Global damped-Newton phase followed by local quadratic convergence

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O(1+\theta_{\rm sc}+\log(1+\log(1+(M_{\rm sc}^2\varepsilon_f)^{-1})))
$$

**Sources.** [1](https://arxiv.org/pdf/2408.11022v1)

**Conditions.** $M_{\rm sc}>0,\ 0<\varepsilon_f<\Delta$

**Dimension conditions.** $M_{\rm sc}>0,\ 0<\varepsilon_f<\Delta$

**Source location.** [1](https://arxiv.org/pdf/2408.11022v1) theorem: §2, Eqs. (21)–(23), local quadratic Newton analysis; pdf pages: 7

### B2 - Path following and predictor–corrector Newton methods

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O(1+\sqrt{\theta_{\rm sc}\log(e+M_{\rm sc}D_{\rm sc}\omega^{-1}(\theta_{\rm sc}))}+\log(1+\log(1+(M_{\rm sc}^2\varepsilon_f)^{-1})))
$$

**Sources.** [1](https://arxiv.org/pdf/2408.11022v1)

**Conditions.** $D_{\rm sc}<\infty$

**Dimension conditions.** $D_{\rm sc}<\infty$

**Source location.** [1](https://arxiv.org/pdf/2408.11022v1) theorem: Theorem 6 Eq.(41); Theorem 10 Eq.(81); pdf pages: 13

### B3 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://arxiv.org/pdf/2408.11022v1)

**Conditions.** $\varepsilon_f\ge\Delta$

**Dimension conditions.** $\varepsilon_f\ge\Delta$

**Local argument.** A1, A2

### B4 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Sources.** [1](https://arxiv.org/pdf/2408.11022v1)

**Conditions.** $\varepsilon_f\ge\Delta$

**Dimension conditions.** $\varepsilon_f\ge\Delta$

**Local argument.** A1, A2

### B5 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Sources.** [1](https://arxiv.org/pdf/2408.11022v1)

**Conditions.** $M_{\rm sc}=0,\ 0<\varepsilon_f<\min\{\Delta,D_{\rm sc}^2/8\}$

**Dimension conditions.** $M_{\rm sc}=0,\ 0<\varepsilon_f<\min\{\Delta,D_{\rm sc}^2/8\}$

**Local argument.** A1, A2

### B6 - Two admissible instances indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Sources.** [1](https://arxiv.org/pdf/2408.11022v1)

**Conditions.** $M_{\rm sc}=0,\ 0<\varepsilon_f<\min\{\Delta,D_{\rm sc}^2/8\}$

**Dimension conditions.** $M_{\rm sc}=0,\ 0<\varepsilon_f<\min\{\Delta,D_{\rm sc}^2/8\}$

**Local argument.** A1, A2

### B7 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://arxiv.org/pdf/2408.11022v1)

**Conditions.** $M_{\rm sc}=0,\ \varepsilon_f\ge\min\{\Delta,D_{\rm sc}^2/8\}$

**Dimension conditions.** $M_{\rm sc}=0,\ \varepsilon_f\ge\min\{\Delta,D_{\rm sc}^2/8\}$

**Local argument.** A1, A2

### B8 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Sources.** [1](https://arxiv.org/pdf/2408.11022v1)

**Conditions.** $M_{\rm sc}=0,\ \varepsilon_f\ge\min\{\Delta,D_{\rm sc}^2/8\}$

**Dimension conditions.** $M_{\rm sc}=0,\ \varepsilon_f\ge\min\{\Delta,D_{\rm sc}^2/8\}$

**Local argument.** A1, A2

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

### A2 - Exact quadratic endpoint under local geometry control

**Scope.** Self-concordant full-space objectives with positive definite Hessian. The Hessian-norm base point and the linked zero-modulus region are essential.

**Algorithm scope.** Self-concordant full-space objectives with positive definite Hessian. The Hessian-norm base point and the linked zero-modulus region are essential.

At zero self-concordance constant, the exact zero/one-query threshold is $B_{\rm sc}=\min\{\Delta,D_{\rm sc}^2/8\}$ when the initial level-set diameter is supplied.

The geometry budget measures diameter in the Hessian norm at $x_0$, not at an unknown optimizer. If $M_{\rm sc}=0$, the third derivative vanishes and the objective is $f(x)=f^*+(x-x^*)^TH(x-x^*)/2$ with constant positive definite H. Write $\delta=f(x_0)-f^*$. Its initial sublevel set is an H-norm ball of radius $\sqrt{2\delta}$, with diameter $2\sqrt{2\delta}$. Therefore $\delta\le B_{\rm sc}=\min\{\Delta,D_{\rm sc}^2/8\}$.

If $\varepsilon_f\ge B_{\rm sc}$, return $x_0$ without a query. If $0<\varepsilon_f<B_{\rm sc}$, one complete second-order jet recovers H and the linear term, so the minimizer is known. To show one call is necessary, set $x_0=0$, $\delta=B_{\mathrm{sc}}$, and $f_\pm(x)=\delta\|x\mp e_1\|^2$. Both instances have the same public budgets and level-set H-diameter $2\sqrt{2\delta}$. Their acceptable sets are disjoint balls of radius $\sqrt{\varepsilon_f/\delta}<1$. One zero-query output distribution cannot assign probability at least 2/3 to both.

Without a geometry budget, use $B_{\mathrm{sc}}=\Delta$. In the geometry model, the weaker condition $\varepsilon_f<\Delta$ is insufficient for a one-call lower bound because the geometry budget may already force zero calls.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [1](https://arxiv.org/pdf/2408.11022v1)

## References

[1] Pavel Dvurechensky; Yurii Nesterov. Improved global performance guarantees of second-order methods in convex minimization. arXiv:2408.11022v1; FoCM online 2025, volume26 (2026), DOI10.1007/s10208-025-09726-6.

https://arxiv.org/pdf/2408.11022v1
