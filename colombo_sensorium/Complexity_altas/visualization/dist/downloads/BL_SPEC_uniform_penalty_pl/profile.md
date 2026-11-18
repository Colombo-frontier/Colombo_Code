# Bilevel optimization with nonunique lower minimizers: uniform perturbed PL conditions and exact gradients.

**Setting ID.** `BL_SPEC_uniform_penalty_pl`

Bilevel optimization

Consider the optimistic bilevel problem $Y^*(x)=\operatorname*{argmin}_{y\in\mathbb{R}^{d_y}}g(x,y)$, $\Phi(x)=\min_{y\in Y^*(x)}f(x,y)$, and seek stationarity of $\min_x\Phi(x)$. Multiple global lower-level solutions are allowed; the defining minima must be attained. Among lower-level minimizers, select one minimizing the upper-level objective.

**Status.** Bounds missing

**TASK tags.** formulation: Bilevel optimistic; task family: Bilevel

**MODEL tags.** growth: Uniform perturbed pl; initialization: Finite initial gap; initialization: Initial solution set distance; smoothness: Gradient and hessian lipschitz

**ORACLE tags.** feedback quality: Exact; interface family: Exact gradient; operation: Primitive gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N grad f; measure: N grad g; precision: Bit precision not counted

## 1. Setting specification

### Task

Consider the optimistic bilevel problem $Y^*(x)=\operatorname*{argmin}_{y\in\mathbb{R}^{d_y}}g(x,y)$, $\Phi(x)=\min_{y\in Y^*(x)}f(x,y)$, and seek stationarity of $\min_x\Phi(x)$. Multiple global lower-level solutions are allowed; the defining minima must be attained. Among lower-level minimizers, select one minimizing the upper-level objective.

### Admissible model

For every $x$ and $t\in[0,\bar t]$, the lower-level minimum of $h_t=g+tf$ is finite and attained, and $\|\nabla_yh_t\|^2\ge2\mu(h_t-\min_yh_t)$ holds globally with the same $\mu$ for all $x,t$. This includes $t=0$, but the PL property of $g$ alone is insufficient. Lower-level strong convexity and uniqueness are not required.

The function $f$ is $C_f$-Lipschitz in the lower-level variable $y$, uniformly over $x$. The function $f$ need not be convex in $x$ or globally Lipschitz in value.

The full gradient of $f$ is jointly $L_f$-Lipschitz in $(x,y)$, and its full Hessian is jointly $\rho_f$-Lipschitz. The quantity $L$ is a public upper bound on $L_f,L_g$.

The full gradient of $g$ is jointly $L_g$-Lipschitz in $(x,y)$, and its full Hessian is jointly $\rho_g=\rho$-Lipschitz. Strong convexity of g is not additionally assumed.

The optimistic objective satisfies $\Phi(x_0)-\inf_x\Phi(x)\le\Delta$, with Delta a public fixed finite initialization budget.

The initial point satisfies $\operatorname{dist}(y_0,Y^*(x_0))\le R_0$, and initialize $z_0=y_0$; $z_0$ starts the second inner tracking sequence. The source perturbation bound for solution sets gives a computable initial tracking budget. Distances are measured to the solution set; no undeclared unique $y^*$ is selected.

### Oracle interface

Public inputs are dimension, target accuracy, the model's budgets, and the initial point. The original functions, their lower-level solutions, and the reduced objective are hidden. Queries are restricted to the stated interfaces; inner optima and undeclared derivatives are not available for free.

The map $(x,y)\mapsto\nabla f(x,y)$ is returned exactly, with no additional random noise.

The response is $(x,y)\longmapsto \nabla g(x,y)$, returned exactly with no additional stochastic noise.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2$, with $\varepsilon$ always specified on the gradient-norm scale. Gradient norm and squared gradient norm remain distinct.

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

$Y^*$: Set of lower-level global minimizers **Domain:** Constraints specified under TASK.

$\nabla,\|\cdot\|$: Euclidean gradient and vector norm; matrix and higher-derivative norms are the induced Euclidean operator norms

$\mathbb E,\Pr,\inf,\sup$: Expectation, probability, infimum, and supremum, with aggregation order and randomness specified by the guarantee.

$\mathcal O,\Omega,\Theta,\widetilde{\mathcal O}$: Asymptotic upper, lower, matching-order, and declared-logarithm upper bounds; fixed parameters are specified in each evidence record

$c,C$: Positive absolute constants or functions of fixed budgets, with dependencies specified by the corresponding result **Domain:** $0<c,C<\infty$.

$\varepsilon$: Target accuracy. Whether error is squared is determined by the metric and guarantee formulas. **Domain:** $\varepsilon>0$.

$d_x$: Upper-level dimension **Domain:** Positive integer.

$d_y$: Lower-level dimension **Domain:** Positive integer.

$C_f$: A uniform norm bound on the population upper function’s lower-variable gradient block. **Domain:** $C_f\ge0$.

$\|\nabla_yf(x,y)\|\le C_f$

$L$: Common joint-variable Lipschitz upper bound for the complete gradients at both levels **Domain:** $L\ge\mu>0$.

$L_f$: Joint-variable Lipschitz upper bound for the complete population upper-level gradient **Domain:** $L_f\ge0$.

$L_g$: A joint-variable Lipschitz bound on the population lower-level full gradient. **Domain:** $L_g\ge\mu>0$.

$\rho$: Joint Lipschitz bound for the full lower Hessian, equal to $\rho_g$. **Domain:** $\rho=\rho_g\ge0$.

$\rho_f$: Joint-variable Lipschitz upper bound for the full upper Hessian. **Domain:** $\rho_f\ge0$.

$\rho_g$: Joint-variable Lipschitz upper bound for the full lower Hessian. **Domain:** $\rho_g\ge0$.

$\mu$: The common PL constant of the entire perturbed lower-level family. It does not imply strong convexity. **Domain:** $\mu>0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_0$: A public bound on distance from the initial point to the lower solution set. **Domain:** $R_0\ge0$.

$\operatorname{dist}(y_0,Y^*(x_0))\le R_0$

$\ell$: Common regularity scale used by the uniformly perturbed PL algorithm **Domain:** $\ell>0$.

$\ell=\max\{C_f,L_f,L_g,\rho_g\}$

$\kappa$: The ratio of the common regularity scale to the uniform PL constant. **Domain:** $\kappa>0$.

$\kappa=\ell/\mu$

$\bar t$: Upper endpoint of the parameter interval in the uniform perturbed PL condition **Domain:** $\bar t>0$.

$h_t,t$: The perturbed lower-level objective and perturbation parameter. **Domain:** $0\le t\le\bar t$.

$h_t(x,y)=g(x,y)+tf(x,y)$

$\operatorname{dist}$: Euclidean point-to-set distance

$\operatorname{dist}(u,S)=\inf_{s\in S}\|u-s\|$

$v_t,\bar\delta_t,C_t$: Computed hypergradient surrogate, recursively maintainable tracking-error upper bound, and gradient-norm certificate. **Domain:** The recurrence and bound are given in the point-selection argument.

$a,c,B,\eta,T,t_*$: Tracking-error coefficient, recurrence coefficient, bias budget, step size, outer iteration count, and selected historical index **Domain:** Used only for the deterministic point-selection argument in the evidence.

$L_\Phi$: An effective Lipschitz bound on the reduced gradient, controlled by the stated regularity budgets.

$z_0$: Initial point of the second inner tracking sequence

$z_0=y_0$

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

### R1 - High-accuracy regime for uniformly perturbed PL problems

**Region.** The quantity $\varepsilon$ is small enough that the source algorithm's perturbation $t=O(\varepsilon)$ belongs to $[0,\bar t]$. Initial-gap and inner-distance certificates are finite.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(\ell  \kappa ^4 \varepsilon ^{-2} \log(\rho _f \ell \kappa /\varepsilon ))
$$

**Gap or comparison.** No lower bound covering the full allowed algorithm class has been registered for the same uniform perturbed-PL model.

**Comparison argument.** Each included claim has verified statement and applicability; mathematics review is separately labeled. No numerical threshold inferred from asymptotics.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** Valid in every finite dimension of the declared model. No additional dimension dependence is introduced beyond the formula.

**Oracle mapping.** Only exact full f/g gradients are available, each charged separately. The uniform PL property holds for every h_t = g + t f in the declared t interval. It does not provide free inner solves or higher derivatives.

**Guarantee mapping.** For every instance, the deterministic guarantee is $\|\nabla\Phi(\widehat x)\|\le\varepsilon$.

**Output mapping.** Return the historical point with smallest computable certificate $C_t$, breaking ties deterministically by the smallest index. The derivation follows below.

**Resource mapping.** Charged resources are $N_{\nabla f}$ and $N_{\nabla g}$. Each execution has a fixed worst-case budget, rather than an expected call budget.

### B1 - F2BA on the uniformly PL penalized family

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\mathcal{O}\!\left(\ell\kappa^4\varepsilon^{-2}\log\frac{\rho_f\ell\kappa}{\varepsilon}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v247/chen24a/chen24a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.**

$$
O(\ell  \kappa ^4 \varepsilon ^{-2} \log(\rho _f \ell \kappa /\varepsilon ))
$$

**Constants.** Finite initial objective gap, initial distance to the solution set, and perturbation-interval budgets are fixed. Source logarithms are interpreted within the stated positive-parameter window.

**Logarithmic factors.** Logarithms in Hessian regularity and accuracy.

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

**Source location.** [1](https://proceedings.mlr.press/v247/chen24a/chen24a.pdf) theorem: Assumption 4.1; Theorem 4.1; section: 4.1–4.3; pdf pages: 8; 10

## 5. Local arguments

### A1 - F2BA on the uniformly PL penalized family

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

**Sources.** [1](https://proceedings.mlr.press/v247/chen24a/chen24a.pdf)

## References

[1] Lesi Chen; Jing Xu; Jingzhao Zhang. On Finding Small Hyper-Gradients in Bilevel Optimization: Hardness Results and Improved Analysis. 2024. COLT 2024, PMLR 247, pp.947–980.

https://proceedings.mlr.press/v247/chen24a/chen24a.pdf
