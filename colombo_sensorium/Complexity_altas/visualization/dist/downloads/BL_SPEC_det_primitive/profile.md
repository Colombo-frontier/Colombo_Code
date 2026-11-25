# Strongly convex lower level: exact primitive gradients and reduced-objective stationarity

**Setting ID.** `BL_SPEC_det_primitive`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Logarithmic gap present; Bounds missing

**TASK tags.** formulation: Bilevel unique reduced; task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Initial distance; smoothness: Bounded partial gradient; smoothness: Full hessian lipschitz; smoothness: Lipschitz gradient; smoothness: Twice continuously differentiable

**ORACLE tags.** feedback quality: Exact; interface family: Exact gradient; operation: Primitive gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N grad f; measure: N grad g; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

### Admissible model

For every fixed upper-level point $x$, $g(x,\cdot)$ is $\mu$-strongly convex on all of $\mathbb{R}^{d_y}$. Convexity in $x$ or joint convexity in $(x,y)$ is not required.

The population full gradient $\nabla f=(\nabla_x f,\nabla_y f)$ is globally $L$-Lipschitz in $(x,y)$. Convexity of $f$ is not required.

The population full gradient $\nabla g=(\nabla_x g,\nabla_y g)$ is globally $L$-Lipschitz in $(x,y)$.

For every $(x,y)$, $\|\nabla_y f(x,y)\|\le C_f$. Equivalently, for fixed $x$ the function $f(x,\cdot)$ is $C_f$-Lipschitz. This does not assert that $f$ is globally Lipschitz in value with respect to $x$.

The objective $\Phi$ has a finite lower bound. A point $x_0$ is given and satisfies $\Phi(x_0)-\inf_x\Phi(x)\le\Delta$. Convexity or existence of a global minimizer of $\Phi$ is not required.

The initial point $(x_0,y_0)$ and bound $\|y_0-y^*(x_0)\|\le R_0$ are given. This is an initialization budget, not a requirement that the oracle return $y^*$.

The function $g$ is twice continuously differentiable, and the full joint Hessian $\nabla^2g$ is globally $\rho$-Lipschitz. This is stronger than constraining only $g_{xy},g_{yy}$.

The function $f$ is twice continuously differentiable. No additional Hessian Lipschitz assumption is imposed.

### Oracle interface

Public inputs are dimension, target accuracy, the model's budgets, and the initial point. The original functions, their lower-level solutions, and the reduced objective are hidden. Queries are restricted to the stated interfaces; inner optima and undeclared derivatives are not available for free.

The map $(x,y)\mapsto\nabla f(x,y)$ is returned exactly, with no additional random noise.

The response is $(x,y)\longmapsto \nabla g(x,y)$, returned exactly with no additional stochastic noise.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2$, with $\varepsilon$ always specified on the gradient-norm scale. Gradient norm and squared gradient norm remain distinct.

In this unconstrained model with a strongly convex lower level, $\nabla\Phi(x)=\nabla_x f(x,y^*)-g_{xy}(x,y^*)g_{yy}(x,y^*)^{-1}\nabla_y f(x,y^*)$, where $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$, and $y^*$ denotes $y^*(x)$. The identity defines the hypergradient without granting additional query access.

### Resource accounting

Each primitive response costs one unit. Separate queries for the two gradients cost two calls. A joint response counts as one call only where explicitly permitted.

Initialization oracle calls count toward the total. A finite initialization bound is an instance-class assumption, not free access to an inner solver.

The budget is a fixed worst-case cap on every execution path; every actual response within a batch is counted.

Internal processing of available information is free. Comparisons use the explicitly specified scalarization or resource vector. Different resources without given weights cannot be assembled coordinatewise from separate algorithms.

### Algorithm views and success guarantees

Algorithms are deterministic and may use arbitrary measurable adaptive queries, stopping, and postprocessing. Outputs may be unqueried, deterministically selected historical points, or admissible averages. No span or zero-respecting restriction applies. Queries are sequential; each response in a batch is charged. Internal arithmetic, linear algebra, and storage are free, with no separate work, memory, or communication budget.

Choose an algorithm using the public parameters, then require $\|\nabla\Phi(\widehat{x})\|_2\le\varepsilon$ for every admissible instance and oracle law. The guarantee is deterministic and applies instance by instance.

**Budget convention.** fixed worst-case total number of calls on every execution

## 2. Notation and parameters

$x,y$: The upper- and lower-level variables. **Domain:** $x\in\mathbb R^{d_x},y\in\mathbb R^{d_y}$.

$f,g$: The original upper- and lower-level real-valued functions. **Domain:** $f,g:\mathbb R^{d_x}\times\mathbb R^{d_y}\to\mathbb R$.

$\widehat x,x_0,y_0$: Output outer point, public outer initial point, and public lower-level initial point **Domain:** Each lies in its corresponding variable space.

$\Phi$: The reduced objective. **Domain:** Defined in the task specification.

$y^*$: Mapping to the unique lower-level global minimizer **Domain:** Constraints specified under TASK.

$\nabla,\|\cdot\|$: Euclidean gradient and vector norm; matrix and higher-derivative norms are the induced Euclidean operator norms

$\mathbb E,\Pr,\inf,\sup$: Expectation, probability, infimum, and supremum, with aggregation order and randomness specified by the guarantee.

$\mathcal O,\Omega,\Theta,\widetilde{\mathcal O}$: Asymptotic upper, lower, matching-order, and declared-logarithm upper bounds; fixed parameters are specified in each evidence record

$c,C$: Positive absolute constants or functions of fixed budgets, with dependencies specified by the corresponding result **Domain:** $0<c,C<\infty$.

$\varepsilon$: Target accuracy. Whether error is squared is determined by the metric and guarantee formulas. **Domain:** $\varepsilon>0$.

$d_x$: Upper-level dimension **Domain:** Positive integer.

$d_y$: Lower-level dimension **Domain:** Positive integer.

$L$: Common joint-variable Lipschitz upper bound for the complete gradients at both levels **Domain:** $L\ge\mu>0$.

$C_f$: A uniform norm bound on the population upper function’s lower-variable gradient block. **Domain:** $C_f\ge0$.

$\|\nabla_yf(x,y)\|\le C_f$

$\mu$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu>0$.

$\rho$: A Lipschitz bound on the complete joint Hessian of the lower-level objective. **Domain:** $\rho\ge0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_0$: Public initial lower-level distance bound **Domain:** $R_0\ge0$.

$\|y_0-y^*(x_0)\|\le R_0$

$\ell$: Common regularity scale for the original-gradient algorithm **Domain:** $\ell>0$.

$\ell=\max\{C_f,L,\rho\}$

$\kappa$: Ratio of the algorithm's common regularity scale to the lower-level curvature **Domain:** $\kappa\ge1$.

$\kappa=\ell/\mu$

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$v_t,\bar\delta_t,C_t$: Computed hypergradient surrogate, recursively maintainable tracking-error upper bound, and gradient-norm certificate. **Domain:** The recurrence and bound are given in the point-selection argument.

$a,c,B,\eta,T,t_*$: Tracking-error coefficient, recurrence coefficient, bias budget, step size, outer iteration count, and selected historical index **Domain:** Used only for the deterministic point-selection argument in the evidence.

$L_\Phi$: An effective Lipschitz bound on the reduced gradient, controlled by the stated regularity budgets.

$N_{\nabla f}$: Upper-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_{\nabla g}$: Lower-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

$\kappa_g$: The public complete-gradient smoothness budget divided by the lower strong-convexity budget; distinct from the existing aggregate ratio kappa. **Domain:** $\kappa_g\ge1$.

$\kappa_g=L/\mu$

$\theta$: Variation-to-curvature ratio for the new joint-parameter comparison. **Domain:** $\theta\ge0$.

$\theta=\rho/\mu$

$\chi$: The amplification factor for the original mean-function class. **Domain:** $\chi\ge1$.

$\chi=1+\theta$

$c_0$: A sufficiently small positive universal accuracy constant common to Corollary 8.3 and its construction; no numerical value is asserted. **Domain:** $c_0>0$.

$p_{\log}$: The fixed nonnegative numerical logarithmic-loss exponent in Corollary 8.3 and Theorem E.7. **Domain:** $0\le p_{\log}<\infty$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O}C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \|\nabla\Phi_I(\hat x_{\mathcal A})\|\le\varepsilon\}.\\C=N_{\nabla f}+N_{\nabla g}.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - Joint conditioning and Hessian-variation comparison for deterministic primitive gradients

**Region.** Common public upper budgets $C_f=L>0$, $\mu>0$, $\kappa_g=L/\mu\ge2$, $1\le\theta=\rho/\mu\le\kappa_g^2$, $\chi=1+\theta$, $\Delta>0$, $0\le R_0<\infty$, and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$. All other native model and parameter constraints remain in force. The budgets are upper bounds and need not be attained by an instance. The minimax supremum is over arbitrary finite dimensions chosen before execution, with dimensions known to the algorithm. The source constants $c_0$ and $p_{\log}$ are universal.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
\Omega\!\left(\frac{L\chi\kappa_g^{5/2}\Delta\varepsilon^{-2}}{[\log(2+\theta)]^{p_{\log}}}\right)
$$

**Upper bound.** B3

$$
\widetilde{\mathcal O}\!\left(L\chi\kappa_g^{5/2}\Delta\varepsilon^{-2}\right)
$$

**Gap or comparison.** Only declared logarithmic factors separate the joint bounds: the explicit lower loss $[\log(2+\theta)]^{p_{\log}}$ and the upper algorithm logs, including initialization logs in $R_0$. At $\rho=L$, the polynomial factor is $L\kappa_g^{7/2}\Delta\varepsilon^{-2}$. No matching $R_0$ or fixed-dimension dependence is asserted.

**Comparison argument.** Corollary 8.3 plus the native-interface transfer argument; the regularity witness certificate is Lemma E.8.

### R2 - high-accuracy source window: outside the new joint window

**Region.** The tolerance $\varepsilon$ is sufficiently small, and $\Delta$ and the initial-distance budgets are finite. Penalties follow an admissible schedule from Chen et al., Theorem 4.1. The comparison concerns accuracy dependence at fixed positive structural budgets, with all initialization calls charged. This comparison is restricted to the complement of the complete joint window defined above.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(\ell  \kappa ^4 \varepsilon ^{-2} \log(\ell \kappa /\varepsilon ))
$$

**Gap or comparison.** The broad parameter window has no verified matching lower bound under the same specification. The separate high-accuracy window at fixed structural budgets has a single-level embedding lower bound.

**Comparison argument.** Each included claim has verified statement and applicability; mathematics review is separately labeled. No numerical threshold inferred from asymptotics.

### R3 - High-accuracy regime with fixed structural budgets: outside the new joint window

**Region.** Fix all positive regularity and initialization budgets, with $\varepsilon\downarrow0$ and $\Delta>0$, and impose the accuracy conditions of the source upper-bound theorem. The lower bound uses sufficiently large finite dimension. This comparison is restricted to the complement of the complete joint window defined above.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Logarithmic gap

**Lower bound.** B2

**Upper bound.** B1

**Gap or comparison.** Only accuracy exponents are compared. The det_primitive upper bound still contains logarithmic factors, and optimal condition-number dependence is not asserted.

## 4. Bounds and supporting evidence

### B1 - F2BA

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\mathcal{O}\!\left(\ell\kappa^4\varepsilon^{-2}\log\frac{\ell\kappa}{\varepsilon}\right)
$$

**Sources.** [2](https://jmlr.org/papers/volume26/23-1104/23-1104.pdf)

**Dimension conditions.** Valid in every finite dimension of the declared model. No additional dimension dependence is introduced beyond the formula.

**Oracle correspondence.** Only exact full f and g gradients are available, with each call charged separately. Gradients used by inner iterations are included in the total.

**Guarantee conversion.** For every instance, the deterministic guarantee is $\|\nabla\Phi(\widehat x)\|\le\varepsilon$.

**Output rule.** Return the historical point with smallest computable certificate $C_t$, breaking ties deterministically by the smallest index. The derivation follows below.

**Resource conversion.** Charged resources are $N_{\nabla f}$ and $N_{\nabla g}$. Each execution has a fixed worst-case budget, rather than an expected call budget.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad f+N grad g.**

$$
O(\ell \kappa ^4\varepsilon ^{-2} \log(\ell \kappa /\varepsilon ))
$$

**N JVP.** 0

**N HVP.** 0

**N inner solve.** 0

**Constants.** The displayed expression fixes initial gap $\Delta$ and a finite public initialization-certificate budget. These dependencies are not claimed jointly optimal.

**Logarithmic factors.** Use $\log(\ell\kappa/\varepsilon)$ in the source theorem’s positive-parameter, high-accuracy window.

**Derivation.** Let $v_t$ be the computed hypergradient surrogate, $\eta>0$ the step size, and $\bar\delta_t\ge0$ a publicly computable tracking-error bound. Choose public constants $a,c\ge0$ and bias budget $B\ge0$ satisfying
$$
\begin{aligned}
\|v_t-\nabla\Phi(x_t)\|&\le\sqrt{a\bar\delta_t}+B,\\
\bar\delta_{t+1}&=\tfrac12\bar\delta_t+c\eta^2\|v_t\|^2,\\
C_t&=\|v_t\|+\sqrt{a\bar\delta_t}+B.
\end{aligned}
$$
Then $C_t$ is a computable upper bound on the true gradient norm. Define $t_* = \min\operatorname*{arg\,min}_{0\le t<T} C_t$, break ties by the smallest index, and return $x_{t_*}$. Under $\eta\le(2L_\Phi)^{-1}$, $ac\eta^2\le1/16$, and $a\le1/\eta$, summing the descent inequalities and the tracking recurrence gives
$$
\min_{t<T}C_t^2\le\frac{27\Delta/\eta+60a\bar\delta_0}{T}+30B^2.
$$
The choices $B\le\varepsilon/\sqrt{60}$ and $T\ge(54\Delta/\eta+120a\bar\delta_0)/\varepsilon^2$ therefore ensure $\|\nabla\Phi(x_{t_*})\|\le\varepsilon$ deterministically. The public initialization budget determines $\bar\delta_0$. Increasing the constants in the inner iteration counts and the existing logarithmic factors enforces these conditions without changing the stated query order. Selection uses only the surrogate and scalar recurrence, with no query to the true hypergradient.

**Local argument.** SIX_PROOF_aff52e4d8a61

**Source location.** [2](https://jmlr.org/papers/volume26/23-1104/23-1104.pdf) theorem: Theorem 4.1; section: 3–4; pdf pages: 6; 7; 9; 10

### B2 - Carmon–Duchi–Hinder–Sidford randomized hard family embedded with an independent quadratic lower level

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(L\Delta\varepsilon^{-2})
$$

**Sources.** [1](https://arxiv.org/abs/1710.11606)

**Conditions.** The initial lower-level distance may be zero. The quantity $\nabla_yf=0$ satisfies every nonnegative upper bound.

**Dimension conditions.** The upper bound holds in all finite dimensions. The cited unconstrained lower bound allows dimension to grow with accuracy and is not claimed for every fixed dimension.

**Constants.** Unshown regularity, initialization, and noise budgets are fixed. Their joint parameter dependence is not certified as closed.

**Derivation.** Embed any single-level hard function into $f(x,y)=h(x),g(x,y)=\mu\|y\|^2/2$; the original-gradient interface is no stronger than the single-level full-derivative interface.

**Source location.** [1](https://arxiv.org/abs/1710.11606) theorem: Theorems 1–2, p=1; section: Sections 4–5

Set $f(x,y)=h(x)$ and $g(x,y)=\mu\|y\|^2/2$. Then $y^*=0$ and $\Phi=h$; lower-level queries contain no information about $h$, while $\nabla_yf=0$ and $\nabla^2g$ are constant. An arbitrary unqueried terminal point can be checked with one extra query. Adjusting accuracy constants does not change the asymptotic order.

### B3 - Deterministic accelerated lower solves, frozen tilts and full-upper-gradient numerical reuse

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\widetilde{\mathcal O}\!\left(L\chi\kappa_g^{5/2}\Delta\varepsilon^{-2}\right)
$$

**Sources.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** Common public upper budgets $C_f=L>0$, $\mu>0$, $\kappa_g=L/\mu\ge2$, $1\le\theta=\rho/\mu\le\kappa_g^2$, $\chi=1+\theta$, $\Delta>0$, $0\le R_0<\infty$, and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$. All other native model and parameter constraints remain in force. The budgets are upper bounds and need not be attained by an instance. The minimax supremum is over arbitrary finite dimensions chosen before execution, with dimensions known to the algorithm. The source constants $c_0$ and $p_{\log}$ are universal.; At $C_f=L$, the complete-gradient bounds at the two levels coincide with the source common budget. The source parameter is $\kappa_g=L/\mu$; the pre-existing $\ell=\max\{C_f,L,\rho\}$ and $\kappa=\ell/\mu$ keep their original meanings. Only the total primitive cost $N_{\nabla f}+N_{\nabla g}$ is compared. This is not a coordinatewise resource-vector lower bound.

**Dimension conditions.** The upper bound holds in every finite dimension. The lower bound is a worst-case-over-finite-dimensions statement; the deterministic transport witness may require dimension exponential in its prescribed query horizon. No fixed-dimensional or polynomial-dimension matching statement is recorded.

**Oracle correspondence.** Exact complete gradients are requested separately; values, HVPs and lower solutions are not supplied. The source lower bound permits the stronger exact value-and-gradient oracle; its upper ignores values.

**Guarantee conversion.** For every admissible instance the deterministic returned point satisfies the native true reduced-gradient norm guarantee.

**Output rule.** An arbitrary unqueried outer point is allowed; the upper algorithm selects a historical point by a deterministic computable surrogate certificate.

**Resource conversion.** Fixed worst-case total number N_grad_f+N_grad_g; joint-pair simulation changes only a universal factor of at most two.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad f+N grad g.**

$$
\widetilde{\mathcal O}\!\left(L\chi\kappa_g^{5/2}\Delta\varepsilon^{-2}\right)
$$

**N value.** 0

**N HVP.** 0

**N inner solve.** 0

**Constants.** Only universal numerical constants are suppressed. The bounds do not claim matching R0 dependence.

**Logarithmic factors.** Logarithms in the charged upper algorithm, including initialization-radius logarithms from arbitrary finite R0.

**Local argument.** BL_SPEC_det_primitive__sfo_20261126__p_contract_transfer

**Source location.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) theorem: Corollary 8.3 and Corollary 4.6; section: Sections 4, 8.2 and Appendix E.2--E.5; pdf pages: 35; 36; printed pages: 35; 36; equations: (8.5)

The proof of Corollary 8.3 explicitly uses deterministic error certificates, deterministic tie-breaking and no function values. Initialization and lower-solve costs are charged; R0-dependent logarithms remain.

At $C_f=L$, the complete-gradient bounds at the two levels coincide with the source common budget. The source parameter is $\kappa_g=L/\mu$; the pre-existing $\ell=\max\{C_f,L,\rho\}$ and $\kappa=\ell/\mu$ keep their original meanings. Only the total primitive cost $N_{\nabla f}+N_{\nabla g}$ is compared. This is not a coordinatewise resource-vector lower bound.

### B4 - Recursive selected-carrier partial-Legendre lift with serial endpoint transport

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Deterministic witness

$$
\Omega\!\left(\frac{L\chi\kappa_g^{5/2}\Delta\varepsilon^{-2}}{[\log(2+\theta)]^{p_{\log}}}\right)
$$

**Sources.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** Common public upper budgets $C_f=L>0$, $\mu>0$, $\kappa_g=L/\mu\ge2$, $1\le\theta=\rho/\mu\le\kappa_g^2$, $\chi=1+\theta$, $\Delta>0$, $0\le R_0<\infty$, and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$. All other native model and parameter constraints remain in force. The budgets are upper bounds and need not be attained by an instance. The minimax supremum is over arbitrary finite dimensions chosen before execution, with dimensions known to the algorithm. The source constants $c_0$ and $p_{\log}$ are universal.; At $C_f=L$, the complete-gradient bounds at the two levels coincide with the source common budget. The source parameter is $\kappa_g=L/\mu$; the pre-existing $\ell=\max\{C_f,L,\rho\}$ and $\kappa=\ell/\mu$ keep their original meanings. Only the total primitive cost $N_{\nabla f}+N_{\nabla g}$ is compared. This is not a coordinatewise resource-vector lower bound.

**Dimension conditions.** The upper bound holds in every finite dimension. The lower bound is a worst-case-over-finite-dimensions statement; the deterministic transport witness may require dimension exponential in its prescribed query horizon. No fixed-dimensional or polynomial-dimension matching statement is recorded.

**Oracle correspondence.** Exact complete gradients are requested separately; values, HVPs and lower solutions are not supplied. The source lower bound permits the stronger exact value-and-gradient oracle; its upper ignores values.

**Guarantee conversion.** For every admissible instance the deterministic returned point satisfies the native true reduced-gradient norm guarantee.

**Output rule.** An arbitrary unqueried outer point is allowed; the upper algorithm selects a historical point by a deterministic computable surrogate certificate.

**Resource conversion.** Fixed worst-case total number N_grad_f+N_grad_g; joint-pair simulation changes only a universal factor of at most two.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad f+N grad g.**

$$
\Omega\!\left(\frac{L\chi\kappa_g^{5/2}\Delta\varepsilon^{-2}}{[\log(2+\theta)]^{p_{\log}}}\right)
$$

**N value.** 0

**N HVP.** 0

**N inner solve.** 0

**Constants.** Only universal numerical constants are suppressed. The bounds do not claim matching R0 dependence.

**Logarithmic factors.** The explicit fixed power [log(2+theta)]^p_log appears in the denominator.

**Local argument.** BL_SPEC_det_primitive__sfo_20261126__p_contract_transfer

**Source location.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) theorem: Corollary 8.3; Theorem E.7; Lemma E.8; section: Sections 4, 8.2 and Appendix E.2--E.5; pdf pages: 35; 36; 77; 78; 80; 81; printed pages: 35; 36; 77; 78; 80; 81; equations: (8.5); (E.18); (E.19)

The exact witnesses have the stronger joint-Hessian variation bound and smooth upper primitive required by the native model. The value-and-gradient lower bound transfers to the weaker gradient-only interface; finite hard dimension is not bounded polynomially.

At $C_f=L$, the complete-gradient bounds at the two levels coincide with the source common budget. The source parameter is $\kappa_g=L/\mu$; the pre-existing $\ell=\max\{C_f,L,\rho\}$ and $\kappa=\ell/\mu$ keep their original meanings. Only the total primitive cost $N_{\nabla f}+N_{\nabla g}$ is compared. This is not a coordinatewise resource-vector lower bound.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 2d0460ccf4f59c5eefed36e234e863e824fda3cda7bfa2208fc9c25c3af9fe59

### Native proof: SIX_PROOF_aff52e4d8a61

Native pointer: /proofs/0; canonical SHA-256: a8e17ac0fabe09c967a47a22d9308b0fa6b238b914b3b35d114923ce0a9758c4

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: f200bfb309302d7faa5c18bd8b58ab0054f0f1a93373fdb86ffc664dfa9bdfe2

F2BA

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 0e3827e0f6419e6b81ee2e02d423645008a1254a7878fb894c758f7f2bca291a

Let $v_t$ be the computed hypergradient surrogate, $\eta>0$ the step size, and $\bar\delta_t\ge0$ a publicly computable tracking-error bound. Choose public constants $a,c\ge0$ and bias budget $B\ge0$ satisfying
$$
\begin{aligned}
\|v_t-\nabla\Phi(x_t)\|&\le\sqrt{a\bar\delta_t}+B,\\
\bar\delta_{t+1}&=\tfrac12\bar\delta_t+c\eta^2\|v_t\|^2,\\
C_t&=\|v_t\|+\sqrt{a\bar\delta_t}+B.
\end{aligned}
$$
Then $C_t$ is a computable upper bound on the true gradient norm. Define $t_* = \min\operatorname*{arg\,min}_{0\le t<T} C_t$, break ties by the smallest index, and return $x_{t_*}$. Under $\eta\le(2L_\Phi)^{-1}$, $ac\eta^2\le1/16$, and $a\le1/\eta$, summing the descent inequalities and the tracking recurrence gives
$$
\min_{t<T}C_t^2\le\frac{27\Delta/\eta+60a\bar\delta_0}{T}+30B^2.
$$
The choices $B\le\varepsilon/\sqrt{60}$ and $T\ge(54\Delta/\eta+120a\bar\delta_0)/\varepsilon^2$ therefore ensure $\|\nabla\Phi(x_{t_*})\|\le\varepsilon$ deterministically. The public initialization budget determines $\bar\delta_0$. Increasing the constants in the inner iteration counts and the existing logarithmic factors enforces these conditions without changing the stated query order. Selection uses only the surrogate and scalar recurrence, with no query to the true hypergradient.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 1154a989f0afe11f0415dafc99eb6e5b32812553f9c93dcabb36f2f18951cdbf

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 23620c756ab92dc27b56258a85c71fdc9842cbe45651fe90658a34fab5601cc5

BL_SRC_chen2025

### Native proof: BL_SPEC_det_primitive__sfo_20261126__p_contract_transfer

Native pointer: /proofs/1; canonical SHA-256: 9e056e730885ff882be58f1e60768dc107e760b6244f4f015e179b1c0d4ab829

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 7f52a83b0cf6419431b9b503bcc12c33f1e91372df5b21f654d4b0ed5d72102b

Transfer from deterministic joint gradients to separately charged primitive gradients

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: f5610a2fc1ab1d4adb4d81dbea9d205e92e37657377104dae7d068ac843fd612

The common model and deterministic guarantee are unchanged. In the source's notation, $F=\Phi$ and $\kappa_g=L/\mu$; the equality $C_f=L$ is an equality of public upper budgets, not a claim that every instance attains the bounds. A global Lipschitz bound on the whole joint Hessian of $g$ implies the source's separate $g_{xy}$ and $g_{yy}$ bounds. Thus the local model is a subclass of the source's mean-function class, and its upper bound transfers to this model.

Corollary 8.3 gives a deterministic, value-free upper algorithm directly. Its proof sets both noise budgets to zero in the fully charged algorithm, uses deterministic tie-breaking, and returns the smallest-index minimizer of the estimated gradient norm. The source derives $\|\nabla\Phi(x_{\hat t})\|\le(\sqrt5+2)\varepsilon/8<\varepsilon$ on every instance, rather than inferring a pointwise deterministic guarantee from an expected-loss statement. Every lower solve and initialization call remains charged.

The lower witness satisfies the stronger local regularity. Lemma E.8 certifies $\operatorname{Lip}(\nabla^2g)\le\rho$ on the whole joint space. The upper primitive in (E.14) is built from the smooth chains, cutoffs and radial profiles of Appendices A and E.2; the joint second-derivative certificate in the proof of Lemma E.3 applies to this primitive. The partial conjugate has the global $C^{2,1}$ regularity of Lemma B.5. These facts yield the required $C^2$ primitives without imposing a full-upper-gradient cap on the local class. The additional witness estimate $\sup\|\nabla f\|\le C(L+\sqrt{L\Delta})$ is compatible with arbitrary $\Delta>0$ and is not replaced here by $O(L)$.

Corollary 8.3 proves that the same fixed witnesses remain hard even if exact values $f,g$ accompany both full gradients. The observer can evaluate the scalar potentials from the disclosed projections, radial norms and restricted inverse on every virtual history; the source supplies the measurability and actual--virtual coupling argument. Removing the value responses therefore cannot invalidate the lower bound for the local gradient-only interface.

For total cost, one exact joint full-gradient reply can simulate either requested primitive gradient, discarding unused components. Hence an $N$-call separate-gradient algorithm can be simulated with at most $N$ joint gradient-pair calls. Conversely, a gradient-pair-only algorithm is simulated by at most two separately charged gradients at each joint query point. Thus $N_{\rm pair}^*\le N_{\rm separate}^*\le2N_{\rm pair}^*$ when $N_{\rm pair}^*$ denotes the gradient-pair-only interface. The source lower oracle additionally supplies values and is stronger, so its lower bound applies to $N_{\rm pair}^*$ as well. Its upper algorithm explicitly ignores values and therefore supplies the stated separate-cost upper bound. This does not equate the value-and-gradient and gradient-pair-only oracle optima, or separate coordinatewise budget frontiers.

The source's fixed-horizon hard observer includes the terminal output, so unqueried outputs remain covered. The dimensions are finite and fixed before the execution, but may grow exponentially with the prescribed query horizon. The lower loss $[\log(2+\theta)]^{p_{\log}}$ and the upper initialization logarithms are retained. In particular, no matching dependence on $R_0$ is claimed, and its logarithm cannot be treated as independent of accuracy when $R_0$ grows exponentially with $1/\varepsilon$. The scalar joint comparison has only a logarithmic gap. On the slice $\rho=L$ it has the polynomial factor $L\kappa_g^{7/2}\Delta\varepsilon^{-2}$, subject to the same guards.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: e7b7fe1181c27730f958cdcb49ae471a48889bbbea2b6085766340eaf4574b7f

Common public upper budgets $C_f=L>0$, $\mu>0$, $\kappa_g=L/\mu\ge2$, $1\le\theta=\rho/\mu\le\kappa_g^2$, $\chi=1+\theta$, $\Delta>0$, $0\le R_0<\infty$, and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$. All other native model and parameter constraints remain in force. The budgets are upper bounds and need not be attained by an instance. The minimax supremum is over arbitrary finite dimensions chosen before execution, with dimensions known to the algorithm. The source constants $c_0$ and $p_{\log}$ are universal.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: premises

Native pointer: /proofs/1/premises; canonical SHA-256: 7d37ccbebdd0f066dbb2f16aee093fd4de03e2c234245163be1edf642c83b06a

#### Native item 1

Native pointer: /proofs/1/premises/0; canonical SHA-256: 4121ffa2b9b6715804800036abe2685bf18b443e98a8bdb588e204d73831abaf

#### Native field: pointer

Native pointer: /proofs/1/premises/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/1/premises/0/sha256; canonical SHA-256: d3dc6536fc2824ae4259e8c5c9d4c719233b2350c77632566f24c07ec44a8b60

bbcf6231bb68a2f8ab68728054a5189f8bb845a9c5ce017e279c8420be80a3f8

#### Native item 2

Native pointer: /proofs/1/premises/1; canonical SHA-256: 987349f50092ade4bc05439a6b1cb19eb2da69c3eb84de438ab45eb91e420e20

#### Native field: pointer

Native pointer: /proofs/1/premises/1/pointer; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native field: sha256

Native pointer: /proofs/1/premises/1/sha256; canonical SHA-256: ba5f9751449ae622a49440b32029684024dfb5d567b2dee351bda5046164a72d

677b66f4e7dddbfa5c1e430933b4a23229e5dad6babaffc9ce1d13ef6114f420

## References

[1] Yair Carmon; John C. Duchi; Oliver Hinder; Aaron Sidford. Lower Bounds for Finding Stationary Points I. 2020. arXiv:1710.11606v3; Mathematical Programming 184 (2020).

https://arxiv.org/abs/1710.11606

[2] Lesi Chen; Yaohua Ma; Jingzhao Zhang. Near-Optimal Nonconvex-Strongly-Convex Bilevel Optimization with Fully First-Order Oracles. 2025. JMLR 26(109), 2025.

https://jmlr.org/papers/volume26/23-1104/23-1104.pdf

[3] Colombo Team. Near-Optimal Joint Complexity of Stochastic Bilevel Optimization: Conditioning, Hessian Variation, and Separate Noise Budgets. User-supplied PDF, uploaded 2026-11-26; 81 pages; SHA-256 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf

**Contribution.** Joint conditioning, variation and noise-budget bounds

**Contribution scope.** The manuscript reports joint parameter bounds for fresh stochastic first-order bilevel optimization in the stated common-budget and reduced-curvature regions, using recursive lower-bound constructions and upper-gradient reuse. The bounds distinguish conditioning, Hessian variation and separate noise budgets. Fixed-parameter sixth-power accuracy dependence has prior work.
