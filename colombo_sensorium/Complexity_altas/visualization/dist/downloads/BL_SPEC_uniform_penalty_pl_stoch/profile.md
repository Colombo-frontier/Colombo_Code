# Bilevel optimization with multiple lower solutions: uniform perturbed PL and stochastic gradients.

**Setting ID.** `BL_SPEC_uniform_penalty_pl_stoch`

Bilevel optimization

Consider the optimistic bilevel problem $Y^*(x)=\operatorname*{argmin}_{y\in\mathbb{R}^{d_y}}g(x,y)$, $\Phi(x)=\min_{y\in Y^*(x)}f(x,y)$, and seek stationarity of $\min_x\Phi(x)$. Multiple global lower-level solutions are allowed; the defining minima must be attained. Among lower-level minimizers, select one minimizing the upper-level objective.

**Status.** Bounds missing

**TASK tags.** task family: Bilevel

**MODEL tags.** growth: Uniform perturbed pl; initialization: Initial gap

**ORACLE tags.** interface family: Fresh gradient

**ALGORITHMS tags.** restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N grad f; measure: N grad g

## 1. Setting specification

### Task

Consider the optimistic bilevel problem $Y^*(x)=\operatorname*{argmin}_{y\in\mathbb{R}^{d_y}}g(x,y)$, $\Phi(x)=\min_{y\in Y^*(x)}f(x,y)$, and seek stationarity of $\min_x\Phi(x)$. Multiple global lower-level solutions are allowed; the defining minima must be attained. Among lower-level minimizers, select one minimizing the upper-level objective.

### Admissible model

For every $x$ and $t\in[0,\bar t]$, the perturbed lower-level objective $h_t(x,y)=g(x,y)+t f(x,y)$ attains its minimum and satisfies $\|\nabla_yh_t\|^2\ge2\mu_{\mathrm{PL}}(h_t-\min_yh_t)$ with the same constant $\mu_{\mathrm{PL}}>0$.

The joint gradient and Hessian of $f,g$ have finite Lipschitz budgets $L_f,L_g,\rho_f,\rho_g$; $f(x,\cdot)$ is $C_f$-Lipschitz. Also $\Phi(x_0)-\inf\Phi\le\Delta$ and $\operatorname{dist}(y_0,Y^*(x_0))\le R_y$. These are population assumptions, not samplewise assumptions.

### Oracle interface

At any $(x,y)$, choose $h=f$ or $g$ and receive the fresh full-gradient sample $G_h$. Conditional on history $\mathcal{H}$ and the query, $\mathbb{E}[G_h\mid\mathcal{H}]=\nabla h$ and $\mathbb{E}[\|G_h-\nabla h\|^2\mid\mathcal{H}]\le\sigma_h^2$ hold. Calls use independent fresh samples with no cross-point reuse.

Dimensions, budget, and initial point are public. No direct inner-solution, branch-selection, hypergradient, or second-order interface is supplied.

### Output

Return a single outer point $\widehat{x}\in\mathbb{R}^{d_x}$, possibly a randomized historical point or an unqueried point. No certificate is required.

### Loss or accuracy criterion

The criterion is $\|\nabla\Phi(\widehat x)\|$. Differentiability follows from the uniform perturbed-PL model, not from a PL condition on $g$ alone.

### Resource accounting

The budget is $N=N_{\nabla f}+N_{\nabla g}$. Each sample costs one unit, under a fixed worst-case budget including all initialization and inner-loop calls.

### Algorithm views and success guarantees

Arbitrary randomized adaptive algorithms are allowed, with measurable queries, stopping, and postprocessing. Outputs may be unqueried, randomly selected historical points, or admissible averages. No span or zero-respecting restriction applies. Queries are sequential; each response in a batch is charged. Internal arithmetic, linear algebra, and storage are free, with no separate work, memory, or communication budget.

For every instance, $\mathbb E\|\nabla\Phi(\widehat x)\|\le\varepsilon$, with expectation over observation and algorithm randomness.

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

$L_f$: Joint-variable Lipschitz upper bound for the complete population upper-level gradient **Domain:** $L_f\ge0$.

$L_g$: A joint-variable Lipschitz bound on the population lower-level full gradient. **Domain:** $L_g\ge\mu>0$.

$C_f$: A uniform norm bound on the population upper function’s lower-variable gradient block. **Domain:** $C_f\ge0$.

$\|\nabla_yf(x,y)\|\le C_f$

$\rho_f$: Joint-variable Lipschitz upper bound for the full upper Hessian. **Domain:** $\rho_f\ge0$.

$\rho_g$: Joint-variable Lipschitz upper bound for the full lower Hessian. **Domain:** $\rho_g\ge0$.

$\mu_{\rm PL}$: The common PL constant of all perturbed lower-level objectives. **Domain:** $\mu_{\rm PL}>0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_y$: A public bound on distance from the initial point to the lower solution set. **Domain:** $R_y\ge0$.

$\operatorname{dist}(y_0,Y^*(x_0))\le R_y$

$\bar t$: Upper endpoint of the parameter interval in the uniform perturbed PL condition **Domain:** $\bar t>0$.

$\ell$: Common regularity scale used by the uniformly perturbed PL algorithm **Domain:** $\ell>0$.

$\ell=\max\{C_f,L_f,L_g,\rho_g\}$

$\kappa$: The ratio of the common regularity scale to the uniform PL constant. **Domain:** $\kappa>0$.

$\kappa=\ell/\mu_{\rm PL}$

$\sigma_f$: Conditional standard-deviation bound for the full stochastic upper-level gradient **Domain:** $\sigma_f\ge0$.

$\sigma_g$: Conditional standard-deviation bound for the full stochastic lower-level gradient **Domain:** $\sigma_g\ge0$.

$G_f,G_g,\mathcal H$: Upper- and lower-level stochastic full-gradient responses and the pre-draw history. **Domain:** $G_f,G_g\in\mathbb R^{d_x+d_y}$.

$G_{f,x},G_{f,y},G_{g,x},G_{g,y}$: Outer and lower blocks of the corresponding full stochastic gradient **Domain:** Outer-block dimension d_x and lower-block dimension d_y.

$h_t,t$: The perturbed lower-level objective and perturbation parameter. **Domain:** $0\le t\le\bar t$.

$h_t(x,y)=g(x,y)+tf(x,y)$

$\operatorname{dist}$: Euclidean point-to-set distance

$\operatorname{dist}(u,S)=\inf_{s\in S}\|u-s\|$

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - source scoped metric resource statement

**Metric contract.** E||grad Phi(x_hat)|| <= epsilon; a uniform random outer iterate implements the source average guarantee.

**Resource contract.** vector: N_grad_f; N_grad_g; projection: Q=N_grad_f+N_grad_g; every sample in each batch is charged.; budget: Fixed planned horizon and batch schedule.

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

#### Q2 - source scoped metric resource statement

**Metric contract.** E||grad Phi(x_hat)|| <= epsilon; a uniform random outer iterate implements the source average guarantee.

**Resource contract.** vector: N_grad_f; N_grad_g; projection: Q=N_grad_f+N_grad_g; every sample in each batch is charged.; budget: Fixed planned horizon and batch schedule.

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

#### Q3 - source scoped metric resource statement

**Metric contract.** E||grad Phi(x_hat)|| <= epsilon; a uniform random outer iterate implements the source average guarantee.

**Resource contract.** vector: N_grad_f; N_grad_g; projection: Q=N_grad_f+N_grad_g; every sample in each batch is charged.; budget: Fixed planned horizon and batch schedule.

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

### R1 - BM_BOUND_pl_stoch_det source window

**Region.** Assume $\sigma_f=\sigma_g=0$ and take $\varepsilon$ sufficiently small that the source perturbation satisfies $t_{\rm pen}\le\bar t$. Regularity, variance, initial gap, and distance budgets are fixed. The quantity $\ell$ is the maximum normalized source regularity budget, with $\kappa=\ell/\mu_{\rm PL}$. The displayed logarithm requires $\rho_f>0$ and $\rho_f\ell\kappa/\varepsilon\ge e$; a positive public upper bound may be declared even when the actual variation is zero.

**Quantity.** Q2

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

### R2 - BM_BOUND_pl_stoch_upper_noise source window

**Region.** Assume $\sigma_f>0,\sigma_g=0$ and take $\varepsilon$ sufficiently small that the source perturbation satisfies $t_{\rm pen}\le\bar t$. Regularity, variance, initial gap, and distance budgets are fixed. The quantity $\ell$ is the maximum normalized source regularity budget, with $\kappa=\ell/\mu_{\rm PL}$. The displayed logarithm requires $\rho_f>0$ and $\rho_f\ell\kappa/\varepsilon\ge e$; a positive public upper bound may be declared even when the actual variation is zero.

**Quantity.** Q3

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B2

### R3 - BM_BOUND_pl_stoch_both_noise source window

**Region.** Assume $\sigma_f>0,\sigma_g>0$ and take $\varepsilon$ sufficiently small that the source perturbation satisfies $t_{\rm pen}\le\bar t$. Regularity, variance, initial gap, and distance budgets are fixed. The quantity $\ell$ is the maximum normalized source regularity budget, with $\kappa=\ell/\mu_{\rm PL}$. The displayed logarithm requires $\rho_f>0$ and $\rho_f\ell\kappa/\varepsilon\ge e$; a positive public upper bound may be declared even when the actual variation is zero.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Selected upper- and lower-level stochastic gradients use fresh samples; same-sample finite differences are unavailable.

**Resource mapping.** Every gradient response in every batch is charged.

### B1 - F2BSA

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{O}\!\left(\ell\kappa^4\varepsilon^{-2}\log\frac{\rho_f\ell\kappa}{\varepsilon}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v247/chen24a/chen24a.pdf)

**Constants.** Hold the stated regularity and initialization budgets fixed. Joint optimality is not claimed for parameters whose dependence is untracked.

**Source location.** [1](https://proceedings.mlr.press/v247/chen24a/chen24a.pdf) pdf pages: 8; 10; 11; 12; theorem or section: Assumption 4.1; Theorems 4.1–4.2; Assumption 4.2; theorem: Assumption 4.1; Theorems 4.1–4.2; Assumption 4.2

### B2 - F2BSA

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{O}\!\left(\ell\kappa^5\varepsilon^{-4}\log\frac{\rho_f\ell\kappa}{\varepsilon}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v247/chen24a/chen24a.pdf)

**Constants.** Hold the stated regularity and initialization budgets fixed. Joint optimality is not claimed for parameters whose dependence is untracked.

**Source location.** [1](https://proceedings.mlr.press/v247/chen24a/chen24a.pdf) pdf pages: 8; 10; 11; 12; theorem or section: Assumption 4.1; Theorems 4.1–4.2; Assumption 4.2; theorem: Assumption 4.1; Theorems 4.1–4.2; Assumption 4.2

### B3 - F2BSA

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{O}\!\left(\ell^3\kappa^{11}\varepsilon^{-6}\log\frac{\rho_f\ell\kappa}{\varepsilon}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v247/chen24a/chen24a.pdf)

**Constants.** Hold the stated regularity and initialization budgets fixed. Joint optimality is not claimed for parameters whose dependence is untracked.

**Source location.** [1](https://proceedings.mlr.press/v247/chen24a/chen24a.pdf) pdf pages: 8; 10; 11; 12; theorem or section: Assumption 4.1; Theorems 4.1–4.2; Assumption 4.2; theorem: Assumption 4.1; Theorems 4.1–4.2; Assumption 4.2

## References

[1] Lesi Chen; Jing Xu; Jingzhao Zhang. On Finding Small Hyper-Gradients in Bilevel Optimization: Hardness Results and Improved Analysis. 2024. COLT 2024, PMLR 247, pp.947–980.

https://proceedings.mlr.press/v247/chen24a/chen24a.pdf
