# Strongly convex quadratic objective accuracy: Hessian–vector product interface

**Setting ID.** `SO_HO_HOI03_S_hvp`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Full space; smoothness: Lipschitz gradient; structure: Quadratic

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Gradient hvp; operation: Gradient hvp; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective is $f(x)=x^\top A x/2-b^\top x+c$, where $A\in\mathbb{R}^{d\times d}$ is symmetric, with $\mu I_d\preceq A\preceq\beta I_d$ and $0<\mu\le\beta$.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

Admissible parameter domain:

$$d\ge1,\ 0<\mu\le\beta,\ 0<\varepsilon_f<\Delta$$

### Oracle interface

Two separately charged queries are available: at $x$, obtain exact $(f(x),\nabla f(x))$; at a point and direction $(x,v)$, obtain exact $\nabla^2f(x)v$, with $v\in\mathbb{R}^d$. A directional query returns one vector.

The public inputs are $x_0$, the target accuracy, and $d$, $\varepsilon_f$, $\beta$, $\mu$, $\Delta$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=f(\widehat{x})-f^*.$$

Here $f^*=\inf_{x\in \mathbb{R}^d}f(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

### Resource accounting

Each joint exact value-and-gradient response or single-direction Hessian–vector product costs one unit. Recovering a matrix using $d$ basis vectors requires $d$ directional queries.

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

$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,2\}$ and $D^0f=f$.

$\|T\|_{\mathrm{op}},\ \|T\|_{\mathrm{op},2}$: Induced operator norm of a Euclidean multilinear tensor; the spectral norm for matrices.

$$\|T\|_{\mathrm{op}}=\|T\|_{\mathrm{op},2}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|.$$

$\mathcal{E}$: Base error defined in the metric specification; expectation or probability aggregation is imposed by the guarantee.

$N$: Total number of original oracle calls; the unit cost is specified in the resource convention. **Domain:** $N\in\mathbb{Z}_{\ge0}$.

$T^*$: Minimum worst-case budget for one algorithm to meet the requirement on the full instance class, within the specified regime, guarantee and resource projection. Expected-resource specifications instead minimize the per-instance expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching bounds up to constants, and upper bounds omitting the declared logarithmic factors. **Domain:** Hidden constants, fixed parameters, and omitted logarithmic variables are specified for each bound.

$\inf,\sup,\min,\max$: Infimum, supremum, attained minimum and attained maximum.

$J_{2}f(x)$: Function value and the complete tuple of derivatives from order one through the specified maximum order.

$$J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x)).$$

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$A,b,c$: Unknown symmetric positive-definite quadratic matrix, linear coefficient vector and constant term. **Domain:** $A\in\mathbb{R}^{d\times d}$, $b\in\mathbb{R}^d$, $c\in\mathbb{R}$.

$I_d$: The identity matrix in dimension $d$.

$A\preceq B$: Loewner order: the symmetric matrix $B-A$ is positive semidefinite.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\varepsilon_f$: Target accuracy **Domain:** $\varepsilon_f>0$.

$\beta$: Spectral upper bound **Domain:** $\beta>0$.

$\mu$: Positive spectral lower bound **Domain:** $\mu>0$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<C<\infty$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each value/gradient point query and each HVP costs one call. Querying d coordinate directions at the same point still costs d calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Nontrivial quadratic accuracy

**Region.** $d\ge1,\ 0<\mu\le\beta,\ 0<\varepsilon_f<\Delta$

**Quantity.** Q1

**Resource.** Each value/gradient point query and each HVP costs one call. Querying d coordinate directions at the same point still costs d calls.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(1+\min\{d,\sqrt\kappa\log(2\Delta/\varepsilon_f)\})
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $d\ge1,\ 0<\mu\le\beta,\ 0<\varepsilon_f<\Delta$

**Dimension conditions.** $d\ge1,\ 0<\mu\le\beta,\ 0<\varepsilon_f<\Delta$

**Oracle mapping.** Two separately charged queries are available: at $x$, obtain exact $(f(x),\nabla f(x))$; at a point and direction $(x,v)$, obtain exact $\nabla^2f(x)v$, with $v\in\mathbb{R}^d$. A directional query returns one vector.

**Guarantee mapping.** Deterministic-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each joint exact value-and-gradient response or single-direction Hessian–vector product costs one unit. Recovering a matrix using $d$ basis vectors requires $d$ directional queries.

### B1 - Conjugate gradients or full matrix reconstruction

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
1+\min\{d,\sqrt\kappa\log(2\Delta/\varepsilon_f)\}
$$

**Sources.** [1](https://nvlpubs.nist.gov/nistpubs/jres/049/jresv49n6p409_a1b.pdf)

**Local argument.** A1

**Source location.** [1](https://nvlpubs.nist.gov/nistpubs/jres/049/jresv49n6p409_a1b.pdf) theorem: Sections 3–6: exact-arithmetic conjugate gradients and finite termination. The Chebyshev error conversion is derived in the local argument “Quadratics: complete Hessians versus directional products”.; pdf pages: 1

## 5. Local arguments

### A1 - Quadratics: complete Hessians versus directional products

**Scope.** Full-Hessian and HVP interfaces remain separate settings or oracle views as defined. The lower statement here concerns one-call impossibility for the full interface, not general HVP optimality.

**Algorithm scope.** Full-Hessian and HVP interfaces remain separate settings or oracle views as defined. The lower statement here concerns one-call impossibility for the full interface, not general HVP optimality.

One complete second-order response solves a known quadratic model exactly; HVP access has a distinct recovery and iterative cost.

For $f(x)=x^TAx/2-b^Tx+c$ with $\mu I\preceq A\preceq\beta I$, a complete second-order response at $x_0$ gives A and $b=Ax_0-\nabla f(x_0)$. Free internal linear algebra returns $A^{-1}b$. When $0<\varepsilon_f<\Delta$, choose $A=\mu I$ and centers $x_0\pm\sqrt{2\Delta/\mu}\,e_1$. Their acceptable balls have radius $\sqrt{2\varepsilon_f/\mu}$, are disjoint, and give the zero-query lower bound. Thus the nontrivial complete-jet cost is exactly one.

An HVP returns only $Av$. Querying d basis vectors recovers A, while a set of fewer than d query directions has an orthogonal vector u such that a perturbation $\tau uu^{\mathsf T}$ leaves their responses unchanged. This is a matrix-recovery observation, not by itself a d-call lower bound for optimization.

Conjugate gradients uses an initial residual and one matrix product per iteration, terminating exactly within d iterations in exact arithmetic. Its Chebyshev estimate is
$$f(x_t)-f^*\le4\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^{2t}(f(x_0)-f^*),\qquad\kappa=\beta/\mu.$$
Combine this with finite termination to obtain the linked upper bound. At $\kappa=1$, $A=\mu I$ is already determined by the public budgets and one gradient suffices. Polynomial-approximation lower bounds for Krylov methods cannot be promoted to arbitrary adaptive randomized HVP lower bounds after dropping their algorithm restrictions.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [1](https://nvlpubs.nist.gov/nistpubs/jres/049/jresv49n6p409_a1b.pdf)

## References

[1] Magnus R. Hestenes, Eduard Stiefel. Methods of Conjugate Gradients for Solving Linear Systems. J. Res. NBS 49(6), 1952, 409–436.

https://nvlpubs.nist.gov/nistpubs/jres/049/jresv49n6p409_a1b.pdf
