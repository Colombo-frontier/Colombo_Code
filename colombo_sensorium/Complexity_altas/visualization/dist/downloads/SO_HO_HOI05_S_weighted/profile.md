# Convex minimization with delayed or weighted Hessian queries: known resource prices

**Setting ID.** `SO_HO_HOI05_S_weighted`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Weighted gradient hessian; operation: Weighted gradient hessian; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** budget: Fixed worst-case budget; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is convex and $C^2$.

$$\|D^{2}f(x)-D^{2}f(y)\|_{\mathrm{op},2}\le M_2\|x-y\|_{2}.$$

There exists a global minimizer $x^*$ satisfying $\|x^*-x_0\|_2\le R$.

No uniform gradient smoothness budget is supplied.

Admissible parameter domain:

$$d\ge1,\quad R,M_2,\varepsilon_f>0,\quad c_g>0,\quad w\ge1$$

### Oracle interface

At any time, the algorithm may choose $x\in\mathbb{R}^d$ and request the exact gradient $\nabla f(x)$ or full exact Hessian $\nabla^2f(x)$. These operations are charged separately; there is no function-value channel.

The public inputs are $x_0$, the target accuracy, and $d$, $\varepsilon_f$, $R$, $M_2$, $c_g$, $w$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=f(\widehat{x})-f^*.$$

Here $f^*=\inf_{x\in \mathbb{R}^d}f(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

### Resource accounting

The native cost is $(N_g,N_H)$. The known gradient price is $c_g>0$ and relative Hessian price is $w\ge1$, giving the specified scalar cost

$$W=c_gN_g+c_gwN_H.$$

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

$c,C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<c,C<\infty$.

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$N_g,N_H,W$: Gradient-call count, full-Hessian-call count, and the specified weighted cost.

$$W=c_gN_g+c_gwN_H.$$

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\varepsilon_f$: Target accuracy **Domain:** $\varepsilon_f>0$.

$R$: Upper bound on the distance from the known initial point to at least one global minimizer. **Domain:** $R>0$.

$M_2$: Hessian Lipschitz bound **Domain:** $M_2>0$.

$c_g$: Unit price of a gradient call **Domain:** $c_g>0$.

$w$: Hessian-to-gradient price ratio **Domain:** $w\ge1$.

$Q$: Ratio of regularity, localization radius, and accuracy defined below. **Domain:** $Q=M_2R^3/\varepsilon_f$.

$$Q=\frac{M_2\,(R)^{3}}{\varepsilon_f}.$$

$C$: Sufficient dimension constant for the lower-bound construction; it depends only on the fixed parameters specified by that bound and is not numerically given. **Domain:** $C>0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Total cost W=c_gN_g+c_g w N_H. Gradient calls are charged as well as Hessian calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Weighted regime in sufficiently high dimension

**Region.** $d\ge C[w+w^{1/7}Q^{2/7}]$

**Quantity.** Q1

**Resource.** Total cost W=c_gN_g+c_g w N_H. Gradient calls are charged as well as Hessian calls.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(c_g(w+w^{1/7}Q^{2/7}))
$$

**Upper bound.** B1

$$
O(c_g(w+w^{1/7}Q^{2/7})[\log(ew)]^{11/3})
$$

**Gap or comparison.** $O([\log(ew)]^{11/3})$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** At any time, the algorithm may choose $x\in\mathbb{R}^d$ and request the exact gradient $\nabla f(x)$ or full exact Hessian $\nabla^2f(x)$. These operations are charged separately; there is no function-value channel.

**Guarantee mapping.** Deterministic-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** The native cost is $(N_g,N_H)$. The known gradient price is $c_g>0$ and relative Hessian price is $w\ge1$, giving the specified scalar cost

### B1 - Delayed-Hessian method with its refresh period chosen from known prices

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
c_g(w+w^{1/7}Q^{2/7})[\log(ew)]^{11/3}
$$

**Sources.** [1](https://arxiv.org/abs/2610.03222v1)

**Conditions.** $d\ge1,\quad R,M_2,\varepsilon_f>0,\quad c_g>0,\quad w\ge1$

**Dimension conditions.** $d\ge1,\ b\ge1,\ w\ge1,\ R,M_2,c_g,\varepsilon_f>0$

**Local argument.** A1

### B2 - Cost-preserving simulation from the weighted interface to the periodic interface

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c_g(w+w^{1/7}Q^{2/7})
$$

**Sources.** [1](https://arxiv.org/abs/2610.03222v1)

**Conditions.** $d\ge C[w+w^{1/7}Q^{2/7}]$

**Dimension conditions.** $d\ge C[w+w^{1/7}Q^{2/7}]$

**Local argument.** A1

## 5. Local arguments

### A1 - Periodic Hessian access and weighted on-demand access

**Scope.** Only the stated periodic and on-demand interfaces, with total weighted cost including gradients. Does not identify separate resource-coordinate bounds with one jointly attainable budget.

**Algorithm scope.** Only the stated periodic and on-demand interfaces, with total weighted cost including gradients. Does not identify separate resource-coordinate bounds with one jointly attainable budget.

With weight $w\ge1$ and period $b\asymp w$, simulations preserve information and relate total cost to periodic call count up to explicit constant and initialization terms.

The periodic interface returns a gradient on every call and a Hessian additionally on calls b,2b,...; the first Hessian is not prepaid. The on-demand interface charges $W=c_gN_g+c_gwN_H$.

To simulate an on-demand algorithm using the periodic interface, answer a gradient request at the next call. For a Hessian request, repeat the desired point until the next Hessian slot and discard unwanted responses. Each Hessian request costs at most b calls, so $T\le N_g+bN_H$. With $b=\lceil w\rceil$, $T\le2W/c_g$. A periodic lower bound therefore yields a weighted lower bound.

Conversely, simulate a periodic algorithm by purchasing a gradient each step and a Hessian at its scheduled slots. Then $N_g+wN_H\le T+w(T/b+1)$. With b comparable to w this is $O(T+b)$, and the initialization term must remain explicit. Both simulations preserve adaptivity and output requirements; no operation is free merely because it is discarded or used while waiting. In the primary definition, use the semantics of the action types when their numeric labels conflict with nearby notation.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [1](https://arxiv.org/abs/2610.03222v1)

## References

[1] Xinliang Zhang, Lesi Chen, Chengchang Liu, Jingzhao Zhang. Near-Optimal Convex Optimization with Lazy Second-Order Oracles. arXiv:2610.03222v1, 2026-10-02.

https://arxiv.org/abs/2610.03222v1
