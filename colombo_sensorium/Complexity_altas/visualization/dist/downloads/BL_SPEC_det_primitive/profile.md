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

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O}C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \|\nabla\Phi_I(\hat x_{\mathcal A})\|\le\varepsilon\}.\\C=N_{\nabla f}+N_{\nabla g}.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - high-accuracy source window

**Region.** The tolerance $\varepsilon$ is sufficiently small, and $\Delta$ and the initial-distance budgets are finite. Penalties follow an admissible schedule from Chen et al., Theorem 4.1. The comparison concerns accuracy dependence at fixed positive structural budgets, with all initialization calls charged.

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

### R2 - High-accuracy regime with fixed structural budgets

**Region.** Fix all positive regularity and initialization budgets, with $\varepsilon\downarrow0$ and $\Delta>0$, and impose the accuracy conditions of the source upper-bound theorem. The lower bound uses sufficiently large finite dimension.

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

**Local argument.** A1

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

## 5. Local arguments

### A1 - F2BA

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

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

**Sources.** [2](https://jmlr.org/papers/volume26/23-1104/23-1104.pdf)

## References

[1] Yair Carmon; John C. Duchi; Oliver Hinder; Aaron Sidford. Lower Bounds for Finding Stationary Points I. 2020. arXiv:1710.11606v3; Mathematical Programming 184 (2020).

https://arxiv.org/abs/1710.11606

[2] Lesi Chen; Yaohua Ma; Jingzhao Zhang. Near-Optimal Nonconvex-Strongly-Convex Bilevel Optimization with Fully First-Order Oracles. 2025. JMLR 26(109), 2025.

https://jmlr.org/papers/volume26/23-1104/23-1104.pdf
