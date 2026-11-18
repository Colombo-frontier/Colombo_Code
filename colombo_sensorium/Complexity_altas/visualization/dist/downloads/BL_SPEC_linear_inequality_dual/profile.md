# Inequality-constrained lower level with an additional exact multiplier interface

**Setting ID.** `BL_SPEC_linear_inequality_dual`

Bilevel optimization

Let $h(x,y)=Ax-By-b$, $y^*(x)=\operatorname*{argmin}_{y:\,h(x,y)\le0}g(x,y)$, and $\Phi(x)=f(x,y^*(x))$. Seek the following approximate stationarity criterion for $\min_{x\in \mathbb{R}^{d_x}}\Phi(x)$.

**Status.** Bounds missing; Joint budget unresolved

**TASK tags.** task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Initial distance; initialization: Initial gap

**ORACLE tags.** interface family: Primitive and exact dual

**ALGORITHMS tags.** restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Goldstein stationarity

**GUARANTEE tags.** aggregation: Per instance

**RESOURCE tags.** accounting: Joint coordinates retained; measure: N dual exact; measure: N fo f; measure: N fo g

## 1. Setting specification

### Task

Let $h(x,y)=Ax-By-b$, $y^*(x)=\operatorname*{argmin}_{y:\,h(x,y)\le0}g(x,y)$, and $\Phi(x)=f(x,y^*(x))$. Seek the following approximate stationarity criterion for $\min_{x\in \mathbb{R}^{d_x}}\Phi(x)$.

### Admissible model

The function $f$ has $C_f$-Lipschitz joint gradient and is $L_f$-Lipschitz in value. The function $g$ has $C_g$-Lipschitz joint gradient and is $\mu_y$-strongly convex in $y$. All norms are Euclidean or their induced operator norms.

Inputs $A\in\mathbb{R}^{d_h\times d_x}$, $B\in\mathbb{R}^{d_h\times d_y}$, and $b\in\mathbb{R}^{d_h}$ are public. The matrix $B$ has full row rank and smallest singular value at least the public $\beta_B>0$. The initial point has upper-level gap at most $\Delta$ and lower-level initial distance at most $R_y$.

$x\in\mathbb{R}^{d_x}$. The solution map $y^*(\cdot)$ is $L_y$-Lipschitz. The reduced objective is finite and globally Lipschitz, but changes in the active constraints may make it nondifferentiable.

For each $x$, the KKT multiplier $\lambda^*(x)$ is unique or selected by a prescribed rule and has norm at most the public bound $R_\lambda$. The selection rule is a fixed part of the instance definition.

### Oracle interface

Choose function $f$ or $g$ and obtain its exact value and full gradient jointly at an admissible $(x,y)$. Queries may use the full Euclidean space.

Public linear-constraint operations and corresponding projections are free. Inner solutions, active sets, and hypergradients are not supplied implicitly.

An additional interface returns exact multipliers $x\mapsto\lambda^*(x)$. Reading their positive support is arithmetic on available data. Unknown multipliers cannot be obtained for free from the original gradient interface.

### Output

Return an outer point $\widehat{x}\in \mathbb{R}^{d_x}$, which may be unqueried. No inner point or certificate is required.

### Loss or accuracy criterion

The error is $\operatorname{dist}(0,\partial_{r_G}\Phi(\widehat{x}))$, where $\partial_{r_G}\Phi(x)=\operatorname{conv}\bigcup_{\|z-x\|\le r_G}\partial_C\Phi(z)$; $\partial_C$ denotes the Clarke subdifferential and $r_G>0$ is the public neighborhood radius.

### Resource accounting

Retain the joint resource vector $(N_{\mathrm{FO},f},N_{\mathrm{FO},g},N_{\mathrm{dual}})$. The primitive first-order result also assumes exact multiplier access. Without specified weights, this vector is not a single primitive-gradient complexity.

### Algorithm views and success guarantees

Arbitrary randomized adaptive algorithms are allowed, with measurable queries, stopping, and postprocessing. Outputs may be unqueried, randomly selected historical points, or admissible averages. No span or zero-respecting restriction applies. Queries are sequential; each response in a batch is charged. Internal arithmetic, linear algebra, and storage are free, with no separate work, memory, or communication budget.

For every instance, $\mathbb{E}\operatorname{dist}(0,\partial_{r_G}\Phi(\widehat{x}))\le\varepsilon$. Expectation is over algorithmic randomness.

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

$d_h$: Number of lower-level linear constraints **Domain:** The quantity $0\le d_h\le d_y$ is an integer; zero denotes no constraints.

$L_f$: A joint-variable Lipschitz bound on upper-level function values. **Domain:** $L_f\ge0$.

$C_f$: Joint Lipschitz bound for the full upper-level gradient **Domain:** $C_f\ge0$.

$C_g$: Joint Lipschitz bound for the full lower-level gradient **Domain:** $C_g\ge\mu_y>0$.

$\mu_y$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu_y>0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_y$: Public initial lower-level distance bound **Domain:** $R_y\ge0$.

$\|y_0-y^*(x_0)\|\le R_y$

$\beta_B$: A lower bound on the smallest singular value of the public constraint matrix B. **Domain:** $\beta_B>0$.

$L_y$: A global Lipschitz bound on the lower-level solution map. **Domain:** $L_y\ge0$.

$\|y^*(x)-y^*(x\prime)\|\le L_y\|x-x\prime\|$

$r_G$: The neighborhood radius in the Goldstein subdifferential definition. **Domain:** $r_G>0$.

$R_\lambda$: A uniform norm bound on the selected optimal lower-level multiplier. **Domain:** $R_\lambda\ge0$.

$A,B,b$: The public lower-level linear-constraint coefficients. **Domain:** $A\in\mathbb R^{d_h\times d_x},B\in\mathbb R^{d_h\times d_y},b\in\mathbb R^{d_h}$.

$h$: Residual of the public linear constraints

$h(x,y)=Ax-By-b$

$\partial_C,\partial_{r_G},\operatorname{conv},\operatorname{dist}$: Clarke subdifferential, Goldstein subdifferential, convex hull, and Euclidean point-to-set distance; full definitions appear under METRIC

$L_0$: A Lipschitz bound for reduced-objective values derived from the original-function and solution-map budgets.

$L_0=L_f\sqrt{1+L_y^2}$

$\lambda^*$: Optimal lower-level KKT multiplier determined by the instance's fixed selection rule **Domain:** $\lambda^*(x)\in\mathbb R_+^{d_h},\ \|\lambda^*(x)\|\le R_\lambda$.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

$N_{\rm FO,f},N_{\rm FO,g}$: Counts of joint value and full-gradient responses for separately selected upper- or lower-level functions. **Domain:** Nonnegative integer.

$N_{\rm dual}$: Number of calls to the additional exact-multiplier interface **Domain:** Nonnegative integer.

## 3. Complexity bracket

### Compared quantities

#### Q1 - achievable resource region

$$
\mathcal B_v(\varepsilon;\theta)=\{b\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_j(\mathcal A,I)\le b_j\ \forall j,I,\quad G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Jointly attainable budgets under the stated success guarantee

**Scope.** The full documented parameter domain; no upper or lower bound is admitted for this comparison.

**Optimization direction.** pareto_minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - The declared parameter domain.

**Region.** All admissible parameters in the eight-part specification; subregions with two-sided evidence have not yet been separated.

**Quantity.** Q1

**Resource.** Identity projection on the declared joint resource vector; no scalar weights are supplied.

**Status.** Joint budget unresolved

**Achievable budgets.** No admitted claim in this comparison

**Necessary constraints.** No admitted claim in this comparison

## 4. Bounds and supporting evidence

## References

[1] Guy Kornowski; Swati Padmanabhan; Kai Wang; Jimmy Zhang; Suvrit Sra. First-Order Methods for Linearly Constrained Bilevel Optimization. 2024. NeurIPS2024 proceedings PDF.

https://proceedings.neurips.cc/paper_files/paper/2024/file/ffd86e56e6403d63dd6face033060e5a-Paper-Conference.pdf
