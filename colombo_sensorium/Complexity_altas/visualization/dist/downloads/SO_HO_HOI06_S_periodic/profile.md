# Nonconvex first-order stationarity with delayed or weighted Hessian queries: periodic interface

**Setting ID.** `SO_HO_HOI06_S_periodic`

Single-objective optimization

Find an approximate first-order stationary point of the full objective, namely $\|\nabla f(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Other quantified gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Lazy hessian; operation: Lazy hessian; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate first-order stationary point of the full objective, namely $\|\nabla f(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is $C^2$ and bounded below; nonconvexity is allowed.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

$$\|D^{2}f(x)-D^{2}f(y)\|_{\mathrm{op},2}\le M_2\|x-y\|_{2}.$$

Admissible parameter domain:

$$d\ge1,\quad\Delta,M_2,\varepsilon_g>0,\quad A\ge1,\quad b\in\mathbb{N}_{\ge1}$$

### Oracle interface

Query $t$ chooses any point $x_t\in\mathbb{R}^d$ and always returns $\nabla f(x_t)$; the complete $\nabla^2f(x_t)$ is additionally returned exactly when $t\in\{b,2b,3b,\ldots\}$. The first Hessian appears on call $b$; no function-value channel is provided.

The public inputs are $x_0$, the target accuracy, and $d$, $\varepsilon_g$, $\Delta$, $M_2$, $b$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\|\nabla f(\widehat{x})\|_2.$$

The criterion uses the gradient norm itself. Squared norms, expectations, and probability guarantees are recorded separately and are not substituted automatically.

### Resource accounting

Each periodic-interface reply costs one unit. Gradient queries made while waiting for the next Hessian slot also count toward the total.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive deterministic algorithms are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\|\nabla f(\widehat{x})\|_2\le \varepsilon_g.$$

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

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\varepsilon_g$: Target accuracy **Domain:** $\varepsilon_g>0$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$M_2$: Hessian Lipschitz bound **Domain:** $M_2>0$.

$b$: Hessian refresh period **Domain:** $b\in\mathbb{N},\ b\ge1$.

$A$: Leading first-order stationarity term with complete second-order feedback **Domain:** $A=\Delta\sqrt{M_2}\varepsilon_g^{-3/2}$.

$$A=\Delta\,\sqrt{M_2}\,((\varepsilon_g)^{\frac{-3}{2}}).$$

$C$: Sufficient dimension constant for the lower-bound construction; it depends only on the fixed parameters specified by that bound and is not numerically given. **Domain:** $C>0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Total number of primitive queries, including gradient queries made before a scheduled Hessian call and those used to select the output.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Common high-dimensional window for the periodic interface

**Region.** $d\ge C(b+A)$

**Quantity.** Q1

**Resource.** Total number of primitive queries, including gradient queries made before a scheduled Hessian call and those used to select the output.

**Status.** Other quantified gap

**Lower bound.** B2

$$
\Omega(b+A)
$$

**Upper bound.** B1

$$
O(b+b^{1/3}A)
$$

**Gap or comparison.** $O((b+b^{1/3}A)/(b+A))$

### R2 - Complete second-order refresh period

**Region.** $\Theta_H\cap\{b=1\}$

**Quantity.** Q1

**Resource.** Total number of primitive queries, including gradient queries made before a scheduled Hessian call and those used to select the output.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(1+A)
$$

**Upper bound.** B1

$$
O(1+A)
$$

**Gap or comparison.** $O(1)$

### R3 - Initialization-dominated regime

**Region.** $\Theta_H\cap\{b\ge A^{3/2}\}$

**Quantity.** Q1

**Resource.** Total number of primitive queries, including gradient queries made before a scheduled Hessian call and those used to select the output.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(b)
$$

**Upper bound.** B1

$$
O(b)
$$

**Gap or comparison.** $O(1)$

### R4 - Interior refresh-period regime

**Region.** $\Theta_H\cap\{1<b<A^{3/2}\}$

**Quantity.** Q1

**Resource.** Total number of primitive queries, including gradient queries made before a scheduled Hessian call and those used to select the output.

**Status.** Polynomial gap

**Lower bound.** B2

$$
\Omega(b+A)
$$

**Upper bound.** B1

$$
O(b+b^{1/3}A)
$$

**Gap or comparison.** $O((b+b^{1/3}A)/(b+A))\le O(b^{1/3})$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Query $t$ chooses any point $x_t\in\mathbb{R}^d$ and always returns $\nabla f(x_t)$; the complete $\nabla^2f(x_t)$ is additionally returned exactly when $t\in\{b,2b,3b,\ldots\}$. The first Hessian appears on call $b$; no function-value channel is provided.

**Guarantee mapping.** Deterministic-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each periodic-interface reply costs one unit. Gradient queries made while waiting for the next Hessian slot also count toward the total.

### B1 - NALEN, without an accuracy logarithm

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
b+b^{1/3}A
$$

**Sources.** [1](https://arxiv.org/abs/2501.17488v3)

**Conditions.** $d\ge1,\quad\Delta,M_2,\varepsilon_g>0,\quad A\ge1,\quad b\in\mathbb{N}_{\ge1}$

**Dimension conditions.** $\Delta,M_2,c_g,\varepsilon_g>0,\quad A\ge1,\ b,w\ge1$

**Source location.** [1](https://arxiv.org/abs/2501.17488v3) theorem: Theorem 4.1; Algorithm 1; eq. (10); pdf pages: 9

### B2 - Combine the highest-order second-order FOSP lower bound Omega(A) with the high-curvature quadratic gradient resisting-chain lower bound Omega(b).

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
b+A
$$

**Sources.** [2](https://arxiv.org/abs/1710.11606v3) [1](https://arxiv.org/abs/2501.17488v3) [3](https://arxiv.org/abs/2610.03222v1)

**Conditions.** $d\ge C(b+A)$

**Dimension conditions.** $d\ge C(b+A)$

**Local argument.** A1, A2

## 5. Local arguments

### A1 - Initialization cost before the first Hessian

**Scope.** Arbitrary deterministic algorithms and sufficiently large dimension. No global $\beta$ bound is assumed; adding one can invalidate the high-curvature quadratic construction.

**Algorithm scope.** Arbitrary deterministic algorithms and sufficiently large dimension. No global $\beta$ bound is assumed; adding one can invalidate the high-curvature quadratic construction.

In a highest-order-only nonconvex model, deterministic periodic access requires $\Omega(b)$ calls in addition to the complete-second-order stationarity difficulty.

Let $T=b-1$ and $N=T+1$, and choose resisting orthonormal directions $v_1,\ldots,v_N$. For $z_i=\langle v_i,x-x_0\rangle$, define
$$q(x)=\frac\lambda2[(z_1-a)^2+\sum_{i=1}^{N-1}(z_i-z_{i+1})^2].$$
Before the first Hessian slot, each gradient exposes at most one new direction. After the output is fixed, choose the final hidden direction orthogonal to it. A safe sufficient dimension is $d\ge2T+2$, and the output has $z_N=0$. With $S=\sum_{i=1}^Ni^2$, direct differentiation gives
$$\sum_{i=1}^N i\langle v_i,\nabla q(\widehat x)\rangle=-\lambda a,\qquad
\|\nabla q(\widehat x)\|\ge\lambda a/\sqrt S.$$
Choose $\lambda=2\varepsilon_g^2S/\Delta$ and $a=\sqrt{2\Delta/\lambda}$. Then the initial gap is exactly $\Delta$ and the output gradient is at least $2\varepsilon_g$. The Hessian is constant, hence its Lipschitz modulus is zero and every positive $M_2$ budget is met. This proves $\Omega(b)$. For weighted access, any cost below $c_gw$ buys no Hessian; take $T=\lceil w\rceil-1$ to obtain the corresponding initialization term.

The separate deterministic complete-second-order hard family gives $\Omega(A)$, with $A=\Delta\sqrt{M_2}\varepsilon_g^{-3/2}$. Taking worst cases yields $\Omega(b+A)$ when dimension accommodates both constructions. NALEN26, Theorem 4.1 supplies $O(b+b^{1/3}A)$. Bounds match for $b=1$ and in the sufficient initialization-dominated region $b\ge A^{3/2}$. In the middle region, retain the explicit ratio; necessity of $b^{1/3}$ has not been proved here.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [2](https://arxiv.org/abs/1710.11606v3) [1](https://arxiv.org/abs/2501.17488v3)

### A2 - Periodic Hessian access and weighted on-demand access

**Scope.** Only the stated periodic and on-demand interfaces, with total weighted cost including gradients. Does not identify separate resource-coordinate bounds with one jointly attainable budget.

**Algorithm scope.** Only the stated periodic and on-demand interfaces, with total weighted cost including gradients. Does not identify separate resource-coordinate bounds with one jointly attainable budget.

With weight $w\ge1$ and period $b\asymp w$, simulations preserve information and relate total cost to periodic call count up to explicit constant and initialization terms.

The periodic interface returns a gradient on every call and a Hessian additionally on calls b,2b,...; the first Hessian is not prepaid. The on-demand interface charges $W=c_gN_g+c_gwN_H$.

To simulate an on-demand algorithm using the periodic interface, answer a gradient request at the next call. For a Hessian request, repeat the desired point until the next Hessian slot and discard unwanted responses. Each Hessian request costs at most b calls, so $T\le N_g+bN_H$. With $b=\lceil w\rceil$, $T\le2W/c_g$. A periodic lower bound therefore yields a weighted lower bound.

Conversely, simulate a periodic algorithm by purchasing a gradient each step and a Hessian at its scheduled slots. Then $N_g+wN_H\le T+w(T/b+1)$. With b comparable to w this is $O(T+b)$, and the initialization term must remain explicit. Both simulations preserve adaptivity and output requirements; no operation is free merely because it is discarded or used while waiting. In the primary definition, use the semantics of the action types when their numeric labels conflict with nearby notation.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [3](https://arxiv.org/abs/2610.03222v1)

## References

[1] Lesi Chen, Chengchang Liu, Luo Luo, Jingzhao Zhang. Faster Newton Methods for Convex and Nonconvex Optimization in Gradient Complexity. arXiv:2501.17488v3, 2026-07-13; COLT 2026.

https://arxiv.org/abs/2501.17488v3

[2] Yair Carmon, John C. Duchi, Oliver Hinder, Aaron Sidford. Lower Bounds for Finding Stationary Points I. arXiv:1710.11606v3; Mathematical Programming 184 (2020).

https://arxiv.org/abs/1710.11606v3

[3] Xinliang Zhang, Lesi Chen, Chengchang Liu, Jingzhao Zhang. Near-Optimal Convex Optimization with Lazy Second-Order Oracles. arXiv:2610.03222v1, 2026-10-02.

https://arxiv.org/abs/2610.03222v1
