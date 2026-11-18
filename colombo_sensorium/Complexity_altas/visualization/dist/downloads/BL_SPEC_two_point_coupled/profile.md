# Stochastic bilevel gradients with two-point coupling within one fresh sample

**Setting ID.** `BL_SPEC_two_point_coupled`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Bounds missing

**TASK tags.** task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Bounded initial inner distance; initialization: Initial gap

**ORACLE tags.** interface family: Two point fresh

**ALGORITHMS tags.** restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N pair f; measure: N pair g

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

### Admissible model

The function $g(x,\cdot)$ is $\mu_y$-strongly convex. The functions $\nabla f,\nabla g$ are jointly $L_f,L_g$-Lipschitz; $\|\nabla_yf\|\le C_f$, and $g_{xy},g_{yy}$ is jointly $\rho$-Lipschitz. Also $\Phi(x_0)-\inf\Phi\le\Delta$ and $\|y_0-y^*(x_0)\|\le R_y$.

Population gradients are unbiased, with variances bounded by $\sigma_f^2,\sigma_g^2$. If $L_{\mathrm{ms}}<\infty$, additionally require the common-sample condition $\mathbb{E}\|G_g(x,y_1;\xi)-G_g(x,y_2;\xi)\|^2\le L_{\mathrm{ms}}^2\|y_1-y_2\|^2$; $L_{\mathrm{ms}}=\infty$ means this condition is absent. It applies only in the lower-variable direction at fixed $x$.

### Oracle interface

The algorithm specifies at most two points $z_1,z_2$ before sampling. Independent upper- and lower-level seeds $\zeta$ and $\xi$ are then drawn, and the oracle returns $(G_f(z_j;\zeta),G_g(z_j;\xi))$ at each requested point. The two points share the current batch seeds; different batches use fresh seeds. No persistent sample handle is provided.

Queries may use the full Euclidean space. Budgets, dimensions, and initial points are public. No additional localization information about $y^*(x)$ is supplied.

### Output

Return any measurable $\widehat{x}\in\mathbb{R}^{d_x}$, possibly an unqueried point.

### Loss or accuracy criterion

$\|\nabla\Phi(\widehat{x})\|^2$.

### Resource accounting

Each function-point-sample gradient evaluation costs one unit. Querying both levels at two points costs four units. The fixed worst-case budget includes all inner, outer, and initialization calls.

### Algorithm views and success guarantees

Arbitrary randomized adaptive algorithms are allowed, but both points in a batch must be fixed before its seed is drawn. Queries, stopping, and postprocessing may be arbitrary measurable functions; outputs may be unqueried, randomly selected historical points, or admissible averages. No span or zero-respecting restriction is imposed. Queries are sequential, and each response in a batch is charged. Internal arithmetic, linear algebra, and storage are free; internal work, memory, and communication are not budgeted.

For every instance, $\mathbb E\|\nabla\Phi(\widehat x)\|^2\le\varepsilon^2$, with expectation over all randomness.

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

$L_f$: Joint-variable Lipschitz upper bound for the complete population upper-level gradient **Domain:** $L_f\ge0$.

$L_g$: A joint-variable Lipschitz bound on the population lower-level full gradient. **Domain:** $L_g\ge\mu_y>0$.

$C_f$: A uniform norm bound on the population upper function’s lower-variable gradient block. **Domain:** $C_f\ge0$.

$\|\nabla_yf(x,y)\|\le C_f$

$\mu_y$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu_y>0$.

$\rho$: Common joint Lipschitz upper bound for the lower function's cross-Hessian block and lower-variable Hessian block **Domain:** $\rho\ge0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_y$: Public initial lower-level distance bound **Domain:** $R_y\ge0$.

$\|y_0-y^*(x_0)\|\le R_y$

$L_{\rm ms}$: A mean-square Lipschitz bound on gradient differences at two lower-level points using the same lower-level sample. **Domain:** The parameter satisfies $0\le L_{\mathrm{ms}}\le\infty$; infinity means that this condition is not imposed.

$\sigma_f$: Conditional standard-deviation bound for the full stochastic upper-level gradient **Domain:** $\sigma_f\ge0$.

$\sigma_g$: Conditional standard-deviation bound for the full stochastic lower-level gradient **Domain:** $\sigma_g\ge0$.

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$G_f,G_g,\mathcal H$: Upper- and lower-level stochastic full-gradient responses and the pre-draw history. **Domain:** $G_f,G_g\in\mathbb R^{d_x+d_y}$.

$G_{f,x},G_{f,y},G_{g,x},G_{g,y}$: Outer and lower blocks of the corresponding full stochastic gradient **Domain:** Outer-block dimension d_x and lower-block dimension d_y.

$z_1,z_2$: At most two joint query points specified simultaneously before one sample draw. **Domain:** $z_j=(x_j,y_j)$.

$\xi,\zeta$: Lower- and upper-level seeds, in the source order used here. They are independent.

$n,T,M$: The source algorithm’s predetermined batch and inner/outer iteration budgets. **Domain:** Role fixed by the evidence's call-accounting convention.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - source scoped metric resource statement

**Metric contract.** E||grad Phi(x_hat)||^2<=epsilon^2.

**Resource contract.** vector: N_pair_f; N_pair_g; projection: Q counts each actual point/sample gradient separately; two points and two functions cost four. Fixed batch size two makes this a constant-factor mapping of the source N-simultaneous interface.; budget: Fixed outer/inner horizons and batches; all initialization and inner calls included.

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

#### Q2 - source scoped metric resource statement

**Metric contract.** E||grad Phi(x_hat)||^2<=epsilon^2.

**Resource contract.** vector: N_pair_f; N_pair_g; projection: Q counts each actual point/sample gradient separately; two points and two functions cost four. Fixed batch size two makes this a constant-factor mapping of the source N-simultaneous interface.; budget: Fixed outer/inner horizons and batches; all initialization and inner calls included.

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

### R1 - BM_BOUND_coupled_variance_upper source window

**Region.** No finite mean-square smoothness budget is required; $L_{\mathrm{ms}}=\infty$ is allowed. Regularity, variance, initial-gap, and inner-distance budgets are fixed, and $\varepsilon$ is sufficiently small.

**Quantity.** Q2

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

### R2 - BM_BOUND_coupled_mss_upper source window

**Region.** $L_{\mathrm{ms}}<\infty$. Fix regularity, variance, initial-gap, and inner-distance budgets, with $\varepsilon$ sufficiently small.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B2

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** In the source branch $r=\infty$, each fresh coupled draw is evaluated at no more than two points.

**Resource mapping.** Each native joint batch is implemented by a constant number of separately charged point-and-function gradient responses.

### B1 - Penalty method with coupled lower iterates

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{O}(\varepsilon^{-6})
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v235/main/assets/kwon24b/kwon24b.pdf)

**Constants.** Hold the stated regularity and initialization budgets fixed. Joint optimality is not claimed for parameters whose dependence is untracked.

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v235/main/assets/kwon24b/kwon24b.pdf) pdf pages: 1; 2; 5; 6; 15; 16; 21; 22; theorem or section: Equations (2)–(4); Definition 1.1; Oracle Classes; Theorems 3.1–3.2; Eq.(86); theorem: Equations (2)–(4); Definition 1.1; Oracle Classes; Theorems 3.1–3.2; Eq.(86)

### B2 - Penalty method with coupled lower iterates

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{O}(\varepsilon^{-4})
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v235/main/assets/kwon24b/kwon24b.pdf)

**Constants.** Hold the stated regularity and initialization budgets fixed. Joint optimality is not claimed for parameters whose dependence is untracked.

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v235/main/assets/kwon24b/kwon24b.pdf) pdf pages: 1; 2; 5; 6; 15; 16; 21; 22; theorem or section: Equations (2)–(4); Definition 1.1; Oracle Classes; Theorems 3.1–3.2; Eq.(86); theorem: Equations (2)–(4); Definition 1.1; Oracle Classes; Theorems 3.1–3.2; Eq.(86)

## References

[1] Jeongyeol Kwon; Dohyun Kwon; Hanbaek Lyu. On The Complexity of First-Order Methods in Stochastic Bilevel Optimization. 2024. PMLR235 ICML2024 publisher PDF.

https://raw.githubusercontent.com/mlresearch/v235/main/assets/kwon24b/kwon24b.pdf
