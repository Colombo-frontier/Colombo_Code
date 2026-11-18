# Finite-sum second-order stationarity with independent tolerances: additional gradient smoothness and component-deviation bounds

**Setting ID.** `SO_HO_HOF04_S_smooth_components`

Single-objective optimization

Find an approximate second-order stationary point of the full objective:

**Status.** Bounds missing

**TASK tags.** formulation: Second order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Individual hessian lipschitz; smoothness: Individual smooth; stochastic model: Bounded component gradient deviation; structure: Finite sum

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Incremental full second order; operation: Incremental full second order; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Second order stationarity; criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate second-order stationary point of the full objective:

$$\|\nabla F(\widehat{x})\|_2\le\varepsilon_g,\qquad\nabla^2F(\widehat{x})\succeq-\varepsilon_H I_d.$$

### Admissible model

The full objective is $F=n^{-1}\sum_{i=1}^n f_i$, with components that are $C^2$ on the full space.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $F(x_0)-\inf_{x\in \mathbb{R}^d}F(x)\le\Delta$.

Every component Hessian satisfies $\|\nabla^2f_i(x)-\nabla^2f_i(y)\|_{\mathrm{op}}\le M_2\|x-y\|_2$ on the full space.

Additionally assume each component gradient is $\beta$-Lipschitz and $\sup_{i,x}\|\nabla f_i(x)-\nabla F(x)\|_2\le\sigma_g$. The value $\sigma_g=+\infty$ is allowed, in which case the deviation condition imposes no finite restriction.

### Oracle interface

Submit $(i,x)$, where $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$, and receive the complete exact component tuple $(f_i(x),Df_i(x),\ldots,D^{2}f_i(x))$. Components may be queried repeatedly. Permissions for selecting component indices are specified under ALGORITHMS.

The public inputs are $x_0$, the target accuracy, and $d$, $n$, $\Delta$, $M_2$, $\beta$, $\sigma_g$, $\varepsilon_g$, $\varepsilon_H$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\max\left\{\frac{\|\nabla F(\widehat{x})\|_2}{\varepsilon_g},\frac{[-\lambda_{\min}(\nabla^2F(\widehat{x}))]_+}{\varepsilon_H}\right\}.$$

$[a]_+=\max\{a,0\}$, and $\lambda_{\min}$ denotes the smallest eigenvalue of a symmetric matrix. The target is $\mathcal{E}(\widehat{x})\le1$, where $\varepsilon_g$ and $\varepsilon_H$ are independent positive tolerances.

### Resource accounting

Each complete component response through order $2$ costs one unit. A complete population response requires $n$ component queries.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[\max\left\{\frac{\|\nabla F(\widehat{x})\|_2}{\varepsilon_g},\frac{[-\lambda_{\min}(\nabla^2F(\widehat{x}))]_+}{\varepsilon_H}\right\}\le 1\right]\ge\frac23.$$

Expectation or probability is evaluated after fixing the instance; component sampling is part of the algorithm's private randomness.

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

$f_i,F,F^*$: Unknown component functions, mean objective, and population optimal value. **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\frac1n\sum_{i=1}^nf_i(x),\qquad F^*=\inf_{x\in\mathbb{R}^d}F(x).$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$\lambda_{\min}(A),[z]_+$: The smallest eigenvalue of a symmetric matrix and the positive part of a scalar.

$$[z]_+=\max\{z,0\}.$$

$I_d$: The identity matrix in dimension $d$.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge 1}$.

$n$: Number of components **Domain:** $n\in\mathbb{N}_{\ge 1}$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$M_2$: Componentwise or average Hessian Lipschitz bound **Domain:** $M_2>0$.

$\beta$: Gradient Lipschitz budget under the stronger specification **Domain:** $\beta>0$.

$\sigma_g$: Global component-gradient deviation bound under the stronger specification **Domain:** $\sigma_g\in(0,+\infty]$.

$\varepsilon_g$: Independent gradient tolerance **Domain:** $\varepsilon_g>0$.

$\varepsilon_H$: Independent negative-curvature tolerance **Domain:** $\varepsilon_H>0$.

$\eta$: Auxiliary accuracy sufficient to satisfy both independent stationarity tolerances. **Domain:** $\eta>0$.

$$\eta=\min\{\varepsilon_g,\frac{(\varepsilon_H)^{2}}{M_2}\}.$$

$\Lambda$: Logarithmic amplification factor in SRVRC.

$$\Lambda=\log\!\left(6C(d+1)(1+\Delta\sqrt{M_2}\,\eta^{-3/2})\right).$$

$U_{\mathrm{SVRC}}$: The recorded envelope for the algorithm's total number of component accesses.

$$U_{\mathrm{SVRC}}=C\log(2+d)[n+\Delta\sqrt{M_2}\,n^{4/5}\eta^{-3/2}].$$

$U_{\mathrm{SRVRC}}$: The recorded envelope for the algorithm's total number of component accesses.

$$U_{\mathrm{SRVRC}}=C_\theta\Lambda^2\{\min(n,\eta^{-2})+\min(n\eta^{-3/2},\sqrt n\eta^{-2},\eta^{-3})+\min(n,\eta^{-1})+\min(\sqrt n\eta^{-3/2},\eta^{-2})\}.$$

$\theta$: Model parameters held fixed in the corresponding accuracy bound.

$$\theta=(n,\Delta,M_2,\beta,\sigma_g).$$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Count all component-gradient and component-Hessian evaluations. Treating a joint response as one call changes only a fixed factor; global solution of the model is free. A Hessian-only subresource bound is not a total-complexity bound.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Fixed positive-scale window in ZG20

**Region.** $\theta=(\Delta,\beta,M_2,\sigma_g)>0\text{ fixed},\quad0<\eta\le c(\theta),\quad\sigma_g<\infty$

**Quantity.** Q1

**Resource.** Count all component-gradient and component-Hessian evaluations. Treating a joint response as one call changes only a fixed factor; global solution of the model is free. A Hessian-only subresource bound is not a total-complexity bound.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1, B2

$$
\min\{U_{SVRC},U_{SRVRC}\}
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Submit $(i,x)$, where $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$, and receive the complete exact component tuple $(f_i(x),Df_i(x),\ldots,D^{2}f_i(x))$. Components may be queried repeatedly. Permissions for selecting component indices are specified under ALGORITHMS.

**Guarantee mapping.** Success probability at least 2/3 for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each complete component response through order $2$ costs one unit. A complete population response requires $n$ component queries.

### B1 - Stochastic variance-reduced cubic regularization (SVRC)

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C\log(2+d)[n+\Delta\sqrt{M_2}\,n^{4/5}\eta^{-3/2}],\quad\eta=\min\{\varepsilon_g,\varepsilon_H^2/M_2\}
$$

**Sources.** [2](https://jmlr.org/papers/volume20/19-055/19-055.pdf)

**Conditions.** $n\ge1,\quad\Delta,M_2,\varepsilon_g,\varepsilon_H>0$

**Dimension conditions.** $n\ge1,\quad\Delta,M_2,\varepsilon_g,\varepsilon_H>0$

**Source location.** [2](https://jmlr.org/papers/volume20/19-055/19-055.pdf) theorem: Theorem 6; Corollary 9; Appendix A.2; pdf pages: 8

### B2 - Stochastic recursive variance-reduced cubic regularization (SRVRC)

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C_\theta\Lambda^2\{\min(n,\eta^{-2})+\min(n\eta^{-3/2},\sqrt n\eta^{-2},\eta^{-3})+\min(n,\eta^{-1})+\min(\sqrt n\eta^{-3/2},\eta^{-2})\}
$$

**Sources.** [1](https://proceedings.mlr.press/v108/zhou20a/zhou20a.pdf)

**Conditions.** $\theta=(\Delta,\beta,M_2,\sigma_g)>0\text{ fixed},\quad0<\eta\le c(\theta),\quad\sigma_g<\infty$

**Dimension conditions.** $\theta=(\Delta,\beta,M_2,\sigma_g)>0\text{ fixed},\quad0<\eta\le c(\theta),\quad\sigma_g<\infty$

**Source location.** [1](https://proceedings.mlr.press/v108/zhou20a/zhou20a.pdf) theorem: Theorem 4.2; Corollary 4.3; Remark 4.5; pdf pages: 6

## References

[1] Dongruo Zhou; Quanquan Gu. Stochastic Recursive Variance-Reduced Cubic Regularization Methods. AISTATS 2020, PMLR 108:3980-3990.

https://proceedings.mlr.press/v108/zhou20a/zhou20a.pdf

[2] Dongruo Zhou; Pan Xu; Quanquan Gu. Stochastic Variance-Reduced Cubic Regularization Methods. JMLR 20(134):1-47, 2019.

https://jmlr.org/papers/volume20/19-055/19-055.pdf
