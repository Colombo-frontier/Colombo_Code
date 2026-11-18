# Finite-sum strongly convex objective accuracy with complete component second derivatives

**Setting ID.** `SO_HO_HOF03_S_as`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}F(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Full space; smoothness: Lipschitz gradient; structure: Finite sum

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Incremental full second order; operation: Incremental full second order; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Explicit restriction; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}F(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The full objective is $F=n^{-1}\sum_{i=1}^n f_i$. Each component is $C^2$, and every $i,x$ satisfies $\mu I_d\preceq\nabla^2f_i(x)\preceq\beta I_d$ and $0<\mu\le\beta$.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $F(x_0)-\inf_{x\in \mathbb{R}^d}F(x)\le\Delta$.

Admissible parameter domain:

$$d\ge1,\ n>1,\quad0<\mu<\beta,\quad\Delta>0,\quad0<\varepsilon_{rel}<1$$

### Oracle interface

Submit $(i,x)$, where $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$, and receive the complete exact component tuple $(f_i(x),Df_i(x),\ldots,D^{2}f_i(x))$. Components may be queried repeatedly. Permissions for selecting component indices are specified under ALGORITHMS.

The public inputs are $x_0$, the target accuracy, and $d$, $n$, $\beta$, $\mu$, $\Delta$, $\varepsilon_{rel}$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

Unqueried outputs are permitted but must still satisfy the spatial or support restrictions of the algorithm class.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=F(\widehat{x})-F^*.$$

The relative success guarantee scales this loss by the actual initial gap $F(x_0)-F^*$; the public bound $\Delta$ is an admissibility parameter.

### Resource accounting

Each complete component response through order $2$ costs one unit. A complete population response requires $n$ component queries.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Internal computation consistent with the algorithm-class restrictions is free; free computation does not remove the stated linear-algebra or index-selection restrictions.

### Algorithm views and success guarantees

#### Restricted oblivious

Private randomness is allowed. Queries and outputs must lie in the recursively generated spaces below, with coordinates centered at the known initial point. Let $\mathcal{W}_1=\{0\}$. The set $\mathcal{W}_{t+1}$ is the closure of vectors obtainable from $\mathcal{W}_t\cup\{\nabla f_{i_t}(x_t)\}$ by finitely many linear combinations and permitted matrix multiplications.

Multiplication by $u\mapsto Hu$ is allowed when $H$ has the block-diagonal structure of a matrix of the following form:

$$\sum_{\tau=\max\{1,t-\lfloor n/2\rfloor+1\}}^{t}\alpha_\tau\nabla^2f_{i_\tau}(x_\tau),\qquad\alpha_\tau\in\mathbb{R}.$$

Blocks may be subdivided further. Between oracle calls, the algorithm may perform any finite number of the permitted operations.

The index sequence is independent of the unknown component functions and may be generated randomly in advance.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\mathbb{E}\!\left[F(\widehat{x})-F^*\right]\le \varepsilon_{\mathrm{rel}}(F(x_0)-F^*).$$

Expectation or probability is evaluated after fixing the instance; component sampling is part of the algorithm's private randomness.

The running-cost guarantee is specified separately under RESOURCE.

#### Restricted adaptive

Private randomness is allowed. Queries and outputs must lie in the recursively generated spaces below, with coordinates centered at the known initial point. Let $\mathcal{W}_1=\{0\}$. The set $\mathcal{W}_{t+1}$ is the closure of vectors obtainable from $\mathcal{W}_t\cup\{\nabla f_{i_t}(x_t)\}$ by finitely many linear combinations and permitted matrix multiplications.

Multiplication by $u\mapsto Hu$ is allowed when $H$ has the block-diagonal structure of a matrix of the following form:

$$\sum_{\tau=\max\{1,t-\lfloor n/2\rfloor+1\}}^{t}\alpha_\tau\nabla^2f_{i_\tau}(x_\tau),\qquad\alpha_\tau\in\mathbb{R}.$$

Blocks may be subdivided further. Between oracle calls, the algorithm may perform any finite number of the permitted operations.

Indices may be selected adaptively from the history; the stated linear-algebra restrictions remain in force.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\mathbb{E}\!\left[F(\widehat{x})-F^*\right]\le \varepsilon_{\mathrm{rel}}(F(x_0)-F^*).$$

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

$I_d$: The identity matrix in dimension $d$.

$A\preceq B$: Loewner order: the symmetric matrix $B-A$ is positive semidefinite.

$\mathcal{W}_t,H,\alpha_\tau$: Admissible recursively generated vector spaces, internal matrices with the required block structure, and arbitrary real coefficients; the complete generation rule appears in the algorithm specification.

$i_t,x_t$: Component index and query point of query $t$.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge 1}$.

$n$: Number of components **Domain:** $n\in\mathbb{N}_{\ge 1}$.

$\beta$: Component-gradient Lipschitz bound **Domain:** $\beta>0$.

$\mu$: Per-component strong-convexity lower bound **Domain:** $\mu>0$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$\varepsilon_{rel}$: Relative objective-gap tolerance in AS17 **Domain:** $0<\varepsilon_{rel}<1$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Restricted oblivious

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete componentwise second-order reply costs one call; internal linear algebra is free. A first-order algorithm may discard the Hessian information.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Restricted adaptive

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete componentwise second-order reply costs one call; internal linear algebra is free. A first-order algorithm may discard the Hessian information.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Validity window for index-oblivious algorithms in AS17

**Region.** $\beta>\mu>0,\quad0<\varepsilon_{rel}\le c(\mu/\beta)^{3/2}\sqrt n,\quad d\ge\widetilde{O}(1+\sqrt{\beta/(n\mu)})$

**Views.** Restricted oblivious

**Quantity.** Q1

**Resource.** One complete componentwise second-order reply costs one call; internal linear algebra is free. A first-order algorithm may discard the Hessian information.

**Status.** Upper bound missing

**Lower bound.** B1

$$
c[n+\sqrt{n\beta/\mu}\log((\mu/\beta)^{3/2}\sqrt n/\varepsilon_{rel})]
$$

**Upper bound.** No admitted bound for this comparison

### R2 - Applicability window of an individual theorem

**Region.** $\Theta_{\rm AS}\text{ parameter conditions},\quad d\ge n^{\widetilde{O}(1+\sqrt{\beta/(n\mu)})}$

**Views.** Restricted adaptive

**Quantity.** Q2

**Resource.** One complete componentwise second-order reply costs one call; internal linear algebra is free. A first-order algorithm may discard the Hessian information.

**Status.** Upper bound missing

**Lower bound.** B2

**Upper bound.** No admitted bound for this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Submit $(i,x)$, where $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$, and receive the complete exact component tuple $(f_i(x),Df_i(x),\ldots,D^{2}f_i(x))$. Components may be queried repeatedly. Permissions for selecting component indices are specified under ALGORITHMS.

**Guarantee mapping.** Expected-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each complete component response through order $2$ costs one unit. A complete population response requires $n$ component queries.

### B1 - Information-propagation lower bound under matrix block-structure restrictions

**Admission.** Included in the bracket

**Direction.** lower

**View.** Restricted oblivious

**Witness or lower-bound scope.** The stated restricted randomized class

$$
c[n+\sqrt{n\beta/\mu}\log((\mu/\beta)^{3/2}\sqrt n/\varepsilon_{rel})]
$$

**Sources.** [1](https://proceedings.mlr.press/v70/arjevani17a/arjevani17a.pdf)

**Conditions.** $\beta>\mu>0,\quad0<\varepsilon_{rel}\le c(\mu/\beta)^{3/2}\sqrt n,\quad d\ge\widetilde{O}(1+\sqrt{\beta/(n\mu)})$

**Dimension conditions.** $\beta>\mu>0,\quad0<\varepsilon_{rel}\le c(\mu/\beta)^{3/2}\sqrt n,\quad d\ge\widetilde{O}(1+\sqrt{\beta/(n\mu)})$

**Source location.** [1](https://proceedings.mlr.press/v70/arjevani17a/arjevani17a.pdf) theorem: Assumptions 1–2; Theorem 2; pdf pages: 4

### B2 - Restricted matrix-information lower bound with adaptive indices

**Admission.** Included in the bracket

**Direction.** lower

**View.** Restricted adaptive

**Witness or lower-bound scope.** The stated restricted randomized class

$$
c[n+\sqrt{n\beta/\mu}\log((\mu/\beta)^{3/2}\sqrt n/\varepsilon_{rel})]
$$

**Sources.** [1](https://proceedings.mlr.press/v70/arjevani17a/arjevani17a.pdf)

**Conditions.** $\Theta_{\rm AS}\text{ parameter conditions},\quad d\ge n^{\widetilde{O}(1+\sqrt{\beta/(n\mu)})}$

**Dimension conditions.** $\Theta_{\rm AS}\text{ parameter conditions},\quad d\ge n^{\widetilde{O}(1+\sqrt{\beta/(n\mu)})}$

**Source location.** [1](https://proceedings.mlr.press/v70/arjevani17a/arjevani17a.pdf) theorem: Theorem 3; pdf pages: 5

## References

[1] Yossi Arjevani; Ohad Shamir. Oracle Complexity of Second-Order Methods for Finite-Sum Problems. ICML 2017, PMLR 70 proceedings PDF.

https://proceedings.mlr.press/v70/arjevani17a/arjevani17a.pdf
