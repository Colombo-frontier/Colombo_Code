# Stochastic nonconvex second-order stationarity with fresh samples of a common loss: Hessian–vector products

**Setting ID.** `SO_HO_HOS05_S_hvp`

Single-objective optimization

Find an approximate second-order stationary point of the full objective:

**Status.** Logarithmic gap present

**TASK tags.** formulation: Second order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Holder hessian; smoothness: Lipschitz gradient; structure: Expectation common loss

**ORACLE tags.** access order: Higher-order interface; feedback quality: Stochastic; interface family: Fresh common loss gradient or hvp; operation: Fresh common loss gradient or hvp; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Second order stationarity; criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Probability; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate second-order stationary point of the full objective:

$$\|\nabla f(\widehat{x})\|_2\le\varepsilon_g,\qquad\nabla^2f(\widehat{x})\succeq-\varepsilon_H I_d.$$

### Admissible model

The population objective $f(x)=\mathbb{E}_Z[\ell(x;Z)]$ is bounded below and has an $\beta$-Lipschitz gradient.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

$$\|D^{2}f(x)-D^{2}f(y)\|_{\mathrm{op},2}\le M_{2,\nu}\|x-y\|_{2}^{\nu}.$$

Each sample loss $\ell(\cdot;Z)$ belongs to $C^{2,1}(\mathbb{R}^d)$ almost surely, and differentiation commutes with expectation. Sample-Hessian Lipschitz constants need not have a uniform upper bound.

### Oracle interface

Choose a point $x$ and, when needed, a direction $v$, then draw a fresh sample $Z$ and return $\nabla\ell(x;Z)$ or $\nabla^2\ell(x;Z)v$. Function values are not supplied.

$$\mathbb{E}\|\nabla\ell(x;Z)-\nabla f(x)\|_2^2\le\sigma_1^2,\quad\mathbb{E}\|(\nabla^2\ell(x;Z)-\nabla^2f(x))v\|_2^2\le\sigma_2^2\|v\|_2^2.$$

Every derivative estimate is unbiased. On a common probability-one event, $\|\nabla^2\ell(x;Z)-\nabla^2f(x)\|_{\mathrm{op}}\le\bar\sigma_2$ holds for all $x$. Different calls use independent fresh samples; sample identities are hidden and samples cannot be reused.

The public inputs are $x_0$, the target accuracy, and $d$, $\Delta$, $\beta$, $M_{2,\nu}$, $\nu$, $\sigma_1$, $\sigma_2$, $\bar\sigma_2$, $\varepsilon_g$, $\varepsilon_H$, $a$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\max\left\{\frac{\|\nabla f(\widehat{x})\|_2}{\varepsilon_g},\frac{[-\lambda_{\min}(\nabla^2f(\widehat{x}))]_+}{\varepsilon_H}\right\}.$$

$[a]_+=\max\{a,0\}$, and $\lambda_{\min}$ denotes the smallest eigenvalue of a symmetric matrix. The target is $\mathcal{E}(\widehat{x})\le1$, where $\varepsilon_g$ and $\varepsilon_H$ are independent positive tolerances.

### Resource accounting

Each stochastic gradient response or single-direction stochastic Hessian–vector product costs one unit; no function-value channel is included. If multiple directions are submitted together, each actual directional response is charged separately.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[\max\left\{\frac{\|\nabla f(\widehat{x})\|_2}{\varepsilon_g},\frac{[-\lambda_{\min}(\nabla^2f(\widehat{x}))]_+}{\varepsilon_H}\right\}\le 1\right]\ge\frac23.$$

Expectation or probability is evaluated after fixing the instance; randomness comes from the algorithm's private seed and oracle sampling.

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

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$Z,\ell(x;Z)$: Sample random variable and the associated scalar sample loss.

$$f(x)=\mathbb{E}_Z\ell(x;Z).$$

$\lambda_{\min}(A),[z]_+$: The smallest eigenvalue of a symmetric matrix and the positive part of a scalar.

$$[z]_+=\max\{z,0\}.$$

$I_d$: The identity matrix in dimension $d$.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge 1}$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$\beta$: Population-gradient smoothness **Domain:** $\beta>0$.

$M_{2,\nu}$: Hölder constant of the population Hessian **Domain:** $M_{2,\nu}>0$.

$\nu$: Hölder exponent **Domain:** $0<\nu\le1$.

$\sigma_1$: Root-mean-square gradient error **Domain:** $\sigma_1>0$.

$\sigma_2$: Root-mean-square error of a directional Hessian observation **Domain:** $\sigma_2>0$.

$\bar\sigma_2$: Uniform almost-sure Hessian-error bound **Domain:** $\bar\sigma_2>0$.

$\varepsilon_g$: Gradient tolerance **Domain:** $\varepsilon_g>0$.

$\varepsilon_H$: Curvature tolerance **Domain:** $\varepsilon_H>0$.

$a$: Dimension-envelope exponent **Domain:** $a>1+2/\nu$.

$C_M(\nu)$: Sufficiently large constant in the total-step envelope; it may depend on fixed nu and has not been assigned a numerical value. **Domain:** $C_M(\nu)\ge1$.

$C_{\log}(\nu)$: Sufficiently large constant in the explicit logarithmic envelope; not assigned a numerical value. **Domain:** $C_{\log}(\nu)\ge1$.

$C_H(\nu)$: Sufficiently large constant inside the logarithm in the negative-curvature hard-block dimension; not assigned a numerical value. **Domain:** $C_H(\nu)\ge1$.

$C_g$: Sufficiently large constant inside the logarithm in the gradient hard-block dimension; not assigned a numerical value. **Domain:** $C_g\ge1$.

$V_0$: Variance bound for fresh-sample line-integral HVP estimates **Domain:** $V_0>0$.

$$V_0=(\sigma_2)^{2}+(\beta)^{2}.$$

$\sigma_{\min}$: Noise scale in the gradient lower bound for the HVP model **Domain:** $\sigma_{\min}>0$.

$$\sigma_{\min}=\min\{\sigma_1,\sigma_2,\bar\sigma_2\}.$$

$\sigma_H$: Noise scale in the negative-curvature lower bound **Domain:** $\sigma_H>0$.

$$\sigma_H=\min\{\sigma_2,\bar\sigma_2\}.$$

$M_{\mathrm{steps}}$: Step-count envelope used to allocate the failure budget **Domain:** $M_{\mathrm{steps}}>0$.

$$M_{\mathrm{steps}}=C_M(\nu)\,(1+\frac{\Delta\,\beta}{(\varepsilon_g)^{2}}+\frac{\Delta\,(M_{2,\nu})^{\frac{2}{\nu}}}{(\varepsilon_H)^{1+\frac{2}{\nu}}}).$$

$\Lambda$: Explicit conservative logarithmic envelope, including log d **Domain:** $\Lambda\ge1$.

$$\Lambda=1+\log(C_{\log}(\nu)\,(d+1)\,(M_{\mathrm{steps}}+1)).$$

$D_H$: A logarithmic envelope within constant factors of the even block dimension in source Eq. (G.4) **Domain:** $D_H>0$.

$$D_H=C_H(\nu)\,(\log(2+\frac{\Delta\,(M_{2,\nu})^{\frac{2}{\nu}}}{(\varepsilon_H)^{1+\frac{2}{\nu}}}+\frac{\Delta\,(\sigma_H)^{2}\,(M_{2,\nu})^{\frac{2}{\nu}}}{(\varepsilon_H)^{3+\frac{2}{\nu}}})).$$

$D_g$: Derived scale specified by the following formula. **Domain:** $D_g>0$.

$$D_g=C_g\,(\log(2+\frac{\Delta}{\varepsilon_g}+\frac{\Delta\,(\sigma_{\min})^{2}}{(\varepsilon_g)^{3}})).$$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each gradient or HVP response costs one call, subject to a deterministic worst-case total cap. A batch of b samples costs b calls; internal real arithmetic is free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - High-dimensional, fixed-scale window with two tolerances

**Region.** $\theta>0\ {\rm fixed},\quad0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge\max\{C D_g\Delta/\varepsilon_g,C_\nu\Delta M_{2,\nu}^{2/\nu}\varepsilon_H^{-(1+2/\nu)}\}$

**Quantity.** Q1

**Resource.** Each gradient or HVP response costs one call, subject to a deterministic worst-case total cap. A batch of b samples costs b calls; internal real arithmetic is free.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
c_\nu\max\{\Delta\sigma_{\min}^2/\varepsilon_g^3,\ \Delta\sigma_H^2M_{2,\nu}^{2/\nu}/(D_H^2\varepsilon_H^{3+2/\nu})\}
$$

**Upper bound.** B1

$$
C(\theta)\Lambda^4(\varepsilon_g^{-3}+\varepsilon_H^{-(3+2/\nu)})
$$

**Gap or comparison.** $O_\theta(\Lambda^4D_H^2)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Choose a point $x$ and, when needed, a direction $v$, then draw a fresh sample $Z$ and return $\nabla\ell(x;Z)$ or $\nabla^2\ell(x;Z)v$. Function values are not supplied.

**Guarantee mapping.** Success probability at least 2/3 for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each stochastic gradient response or single-direction stochastic Hessian–vector product costs one unit; no function-value channel is included. If multiple directions are submitted together, each actual directional response is charged separately.

### B1 - Fresh-sample HVP line integration, chord tracking across scales, and randomized negative-curvature steps

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C_\nu\Lambda^4 B_{\rm fresh}
$$

**Sources.** [1](https://arxiv.org/pdf/2609.28238v2)

**Conditions.** $0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0,\quad0<\nu\le1$

**Dimension conditions.** $0<\varepsilon_g,\varepsilon_H\le1,\quad\theta>0,\quad0<\nu\le1$

**Source location.** [1](https://arxiv.org/pdf/2609.28238v2) theorem: Theorem A.11, eq.(A.9); Lemmas A.3-A.6 and Proposition A.10; pdf pages: 17

### B2 - Conservative noise localization and information lower bound for a common loss

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\nu\max\{\Delta\sigma_{\min}^2/\varepsilon_g^3,\ \Delta\sigma_H^2M_{2,\nu}^{2/\nu}/(D_H^2\varepsilon_H^{3+2/\nu})\}
$$

**Sources.** [1](https://arxiv.org/pdf/2609.28238v2)

**Conditions.** $\theta>0\ {\rm fixed},\quad0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge\max\{C D_g\Delta/\varepsilon_g,C_\nu\Delta M_{2,\nu}^{2/\nu}\varepsilon_H^{-(1+2/\nu)}\}$

**Dimension conditions.** $\theta>0\ {\rm fixed},\quad0<\varepsilon_g,\varepsilon_H\le c(\theta),\quad d\ge\max\{C D_g\Delta/\varepsilon_g,C_\nu\Delta M_{2,\nu}^{2/\nu}\varepsilon_H^{-(1+2/\nu)}\}$

**Source location.** [1](https://arxiv.org/pdf/2609.28238v2) theorem: Appendix G, (G.5)-(G.6); Theorem 3.5; pdf pages: 38

## References

[1] Wendao Wu; Haihan Zhang; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Second-Order Stationarity with Common Random Losses: Matching Tolerance Bounds. arXiv:2609.28238v2 (2026-10-19); latest history checked 2026-10-29.

https://arxiv.org/pdf/2609.28238v2
