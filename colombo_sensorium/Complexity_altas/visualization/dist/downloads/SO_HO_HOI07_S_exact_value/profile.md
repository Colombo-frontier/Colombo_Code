# Nonconvex first-order stationarity with biased gradients and approximate Hessians: exact function values included

**Setting ID.** `SO_HO_HOI07_S_exact_value`

Single-objective optimization

Find an approximate first-order stationary point of the full objective, namely $\|\nabla f(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

**Status.** Bounds missing

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz gradient; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: Higher-order interface; feedback quality: Biased; interface family: Value with biased derivatives; operation: Value with biased derivatives; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate first-order stationary point of the full objective, namely $\|\nabla f(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is $C^2$ and bounded below; nonconvexity is allowed.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

$$\|D^{2}f(x)-D^{2}f(y)\|_{\mathrm{op},2}\le M_2\|x-y\|_{2}.$$

The gradient satisfies $\|\nabla f(x)-\nabla f(y)\|_2\le\beta\|x-y\|_2$.

Admissible parameter domain:

$$d\ge1,\ \beta,M_2,\Delta,\eta_1,\eta_2,\varepsilon_g>0$$

### Oracle interface

A query at $x\in\mathbb{R}^d$ returns a vector $g(x)$ and symmetric matrix $H(x)$ satisfying

$$\|g(x)-\nabla f(x)\|_2\le\eta_1,\qquad\|H(x)-\nabla^2f(x)\|_{\mathrm{op}}\le\eta_2.$$

Replies may depend on the history, and performance must be guaranteed for every admissible reply rule. Each reply additionally includes the exact $f(x)$.

The public inputs are $x_0$, the target accuracy, and $d$, $\varepsilon_g$, $\beta$, $M_2$, $\Delta$, $\eta_1$, $\eta_2$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\|\nabla f(\widehat{x})\|_2.$$

The criterion uses the gradient norm itself. Squared norms, expectations, and probability guarantees are recorded separately and are not substituted automatically.

### Resource accounting

Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[\|\nabla f(\widehat{x})\|_2\le \varepsilon_g\right]\ge\frac23.$$

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

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$g(x),H(x)$: Gradient vector and symmetric Hessian approximation supplied by the oracle; exactness and error bounds are specified separately for each channel.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\varepsilon_g$: Target accuracy **Domain:** $\varepsilon_g>0$.

$\beta$: Gradient Lipschitz budget **Domain:** $\beta>0$.

$M_2$: Hessian Lipschitz bound **Domain:** $M_2>0$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$\eta_1$: Absolute gradient-deviation bound **Domain:** $\eta_1>0$.

$\eta_2$: Spectral-norm error bound on the Hessian estimate **Domain:** $\eta_2>0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive response costs one call; all additional gradient queries at other points are also charged.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Positive-parameter range

**Region.** $d\ge1,\ \beta,M_2,\Delta,\eta_1,\eta_2,\varepsilon_g>0$

**Quantity.** Q1

**Resource.** Each primitive response costs one call; all additional gradient queries at other points are also charged.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(d(1+\beta\Delta\varepsilon_g^{-2}))
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $d\ge1,\ \beta,M_2,\Delta,\eta_1,\eta_2,\varepsilon_g>0$

**Dimension conditions.** $d\ge1,\ \beta,M_2,\Delta,\eta_1,\eta_2,\varepsilon_g>0$

**Oracle mapping.** A query at $x\in\mathbb{R}^d$ returns a vector $g(x)$ and symmetric matrix $H(x)$ satisfying

**Guarantee mapping.** Success probability at least 2/3 for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Exact-value finite differences with fixed-step descent

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
d(1+\beta\Delta\varepsilon_g^{-2})
$$

**Local argument.** A1

## 5. Local arguments

### A1 - A finite-difference baseline with exact values

**Scope.** Exact values, globally $\beta$-Lipschitz gradients, full-space query access, and a public initial-gap bound.

**Algorithm scope.** Exact values, globally $\beta$-Lipschitz gradients, full-space query access, and a public initial-gap bound.

An exact value channel gives a reliable $O(d(1+\beta\Delta/\varepsilon_g^2))$ stationarity upper bound even when accompanying derivative estimates are biased.

For a globally $\beta$-smooth function, set $\widetilde g_i(x)=[f(x+he_i)-f(x)]/h$. Then $|\widetilde g_i-g_i|\le\beta h/2$. The finite positive step $h=\varepsilon_g/(8\beta\sqrt d)$ ensures $\|\widetilde g-g\|\le\varepsilon_g/16$. Computing the estimate costs d+1 exact values; ignore accompanying biased derivatives.

If $\|\widetilde g\|\le\varepsilon_g/2$, the true gradient is below $\varepsilon_g$. Otherwise update $x_+=x-\widetilde g/\beta$. Smoothness yields
$$f(x_+)\le f(x)-\|g(x)\|^2/(2\beta)+\|\widetilde g-g\|^2/(2\beta).$$
Before stopping, $\|g(x)\|\ge7\varepsilon_g/16$, so every step decreases the objective by a universal positive multiple of $\varepsilon_g^2/\beta$. The initial gap budget $\Delta$ limits the number of steps to $O(1+\beta\Delta/\varepsilon_g^2)$, proving the displayed call count.

No limit derivative is treated as a free oracle response; all steps are finite and positive. This is a verified information-interface baseline, not a claim to be the strongest known upper bound for the richer interface.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.
