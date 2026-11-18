# Convex minimization with second-order feedback and third-order regularity

**Setting ID.** `SO_HO_HOI02_S_det`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space

**ORACLE tags.** access order: Higher-order interface; feedback quality: Inexact; interface family: Inexact hessian; operation: Inexact hessian; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is convex and $C^3$.

$$\|D^{3}f(x)-D^{3}f(y)\|_{\mathrm{op},2}\le M_3\|x-y\|_{2}.$$

There exists a global minimizer $x^*$ satisfying $\|x^*-x_0\|_2\le R$.

Every point in the initial sublevel set lies within distance $R_{\mathrm{lev}}$ of some minimizer. Initial derivatives satisfy $\|D^jf(x_0)\|_{\mathrm{op}}\le B_j$ and $j=1,2,3$.

Admissible parameter domain:

$$d\ge1,\ R,M_3,\eta_2,R_{\rm lev},B_1,B_2,B_3,\varepsilon_f>0$$

### Oracle interface

A query at any $x\in\mathbb{R}^d$ returns $(f(x),\nabla f(x),H(x))$. The first two entries are exact, and $H(x)$ is symmetric with $\|H(x)-\nabla^2f(x)\|_{\mathrm{op}}\le\eta_2$. The approximation error may depend on previous queries and responses; neither unbiasedness nor independence is assumed.

The public inputs are $x_0$, the target accuracy, and $d$, $\varepsilon_f$, $R$, $M_3$, $\eta_2$, $R_{\rm lev}$, $B_1$, $B_2$, $B_3$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

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

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$g(x),H(x)$: Gradient vector and symmetric Hessian approximation supplied by the oracle; exactness and error bounds are specified separately for each channel.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\varepsilon_f$: Target accuracy **Domain:** $\varepsilon_f>0$.

$R$: Upper bound on the distance from the known initial point to at least one global minimizer. **Domain:** $R>0$.

$M_3$: Lipschitz bound on the third derivative **Domain:** $M_3>0$.

$\eta_2$: Declared positive Hessian-error bound **Domain:** $\eta_2>0$.

$R_{\rm lev}$: Uniform radius bound from the initial sublevel set to a minimizer **Domain:** $R_{\rm lev}>0$.

$B_1$: Upper bound on the initial gradient norm **Domain:** $B_1>0$.

$B_2$: Upper bound on the initial Hessian norm **Domain:** $B_2>0$.

$B_3$: Upper bound on the initial third-derivative norm **Domain:** $B_3>0$.

$A$: Error term **Domain:** $A=(\eta_2R^2/\varepsilon_f)^{1/2}$.

$$A=\sqrt{\frac{\eta_2\,(R)^{2}}{\varepsilon_f}}.$$

$B$: Leading term from third-order regularity **Domain:** $B=(M_3R^4/\varepsilon_f)^{1/5}$.

$$B=(\frac{M_3\,(R)^{4}}{\varepsilon_f})^{\frac{1}{5}}.$$

$\mathcal{L}_{\mathrm{BDGM}}$: Query factor from the inner bidirectional-gradient method; polylogarithmic in the listed variables and equal to $O_\theta(1+\log(2+\varepsilon_f^{-1}))$ when the other positive scales are fixed.

$$\mathcal{L}_{\mathrm{BDGM}}=\operatorname{polylog}(\eta_2^{-1},\varepsilon_f^{-1},M_3,R_{\mathrm{lev}},B_1,B_2,B_3).$$

$\theta$: Model parameters held fixed in the corresponding accuracy bound.

$$\theta=(R,M_3,\eta_2,R_{\rm lev},B_1,B_2,B_3).$$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each original f/g/H reply costs one unit. Every new internal gradient query is charged; BDGM is not treated as free model computation.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Complete model including inner-solve scales

**Region.** $d\ge1,\ R,M_3,\eta_2,R_{\rm lev},B_1,B_2,B_3,\varepsilon_f>0$

**Quantity.** Q1

**Resource.** Each original f/g/H reply costs one unit. Every new internal gradient query is charged; BDGM is not treated as free model computation.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O((1+A+B)\mathcal{L}_{\rm BDGM})
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $d\ge1,\ R,M_3,\eta_2,R_{\rm lev},B_1,B_2,B_3,\varepsilon_f>0$

**Dimension conditions.** $d\ge1,\ R,M_3,\eta_2,R_{\rm lev},B_1,B_2,B_3,\varepsilon_f>0$

**Oracle mapping.** A query at any $x\in\mathbb{R}^d$ returns $(f(x),\nabla f(x),H(x))$. The first two entries are exact, and $H(x)$ is symmetric with $\|H(x)-\nabla^2f(x)\|_{\mathrm{op}}\le\eta_2$. The approximation error may depend on previous queries and responses; neither unbiasedness nor independence is assumed.

**Guarantee mapping.** Deterministic-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Third-order regularization implemented through second-order feedback and BDGM inner solves

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
(1+A+B)\mathcal{L}_{\rm BDGM}
$$

**Sources.** [1](https://arxiv.org/abs/2607.24520v3)

**Source location.** [1](https://arxiv.org/abs/2607.24520v3) theorem: Theorem 4.1, Corollary 4.1, eq. (17); Appendix I; pdf pages: 10

## References

[1] Lesi Chen, Chengchang Liu, Luo Luo, John C. S. Lui, Jingzhao Zhang. Optimal Convex Optimization with Inexact Second-Order Oracles. arXiv:2607.24520v3, 2026-07-31.

https://arxiv.org/abs/2607.24520v3
