# Finite-sum bilevel optimization: a lower bound under linear-iteration restrictions.

**Setting ID.** `BL_SPEC_finite_derivative_linear`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the stated error criterion and guarantee. Assumptions on $f$, $g$, and $\Phi$ are specified separately. Here $f=n_f^{-1}\sum_if_i$ and $g=n_g^{-1}\sum_jg_j$.

**Status.** Bounds missing

**TASK tags.** task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; structure: Finite sum

**ORACLE tags.** interface family: Derivative vector

**ALGORITHMS tags.** restriction: Linear span

**OUTPUT tags.** object: Outer point; support: Restricted iteration sequence

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the stated error criterion and guarantee. Assumptions on $f$, $g$, and $\Phi$ are specified separately. Here $f=n_f^{-1}\sum_if_i$ and $g=n_g^{-1}\sum_jg_j$.

### Admissible model

Each $f_i$ has $L_F$-Lipschitz joint gradient. Each $g_j$ is twice continuously differentiable and $\mu_y$-strongly convex in $y$. This lower-bound class imposes no additional uniform Lipschitz budgets on function values, Hessians, or third derivatives.

The points $x_0,y_0,v_0$ are public and $\Phi(x_0)-\inf\Phi\le\Delta$. No additional bound is imposed on the initial inner or adjoint distance.

### Oracle interface

A query selects $i,j,x,y,v$ and returns the exact joint response $(\nabla f_i,\nabla g_j,g_{j,yy}v,g_{j,xy}v)$, with every component evaluated at $(x,y)$. Components may be queried repeatedly.

### Output

Return an outer point from the restricted iteration sequence. An arbitrary terminal output outside the permitted span cannot enlarge the algorithm class.

### Loss or accuracy criterion

$\|\nabla\Phi(\widehat{x})\|_2^2$.

### Resource accounting

The quantity $N_{\mathrm{tuple}}$ counts joint responses, each costing one unit under a fixed worst-case budget. Four primitive calls can simulate one joint response, but this simulation does not remove the algorithm’s linear-iteration restriction.

### Algorithm views and success guarantees

Restrict to the linear bilevel iteration class in Dagréou et al., Definition 4.2. Component indices may be randomized, but the following history-span restrictions must hold:

$y_{t+1}\in y_0+\operatorname{span}\{\nabla_yg_{j_s}(x_s,y_s):s\le t\}$; $v_{t+1}\in v_0+\operatorname{span}\{g_{j_s,yy}(x_s,y_s)v_s+\nabla_yf_{i_s}(x_s,y_s):s\le t\}$; $x_{t+1}\in x_0+\operatorname{span}\{g_{j_s,xy}(x_s,y_s)v_s+\nabla_xf_{i_s}(x_s,y_s):s\le t\}$.

For every instance, $\mathbb{E}\|\nabla\Phi(\widehat{x})\|_2^2\le\varepsilon^2$.

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

$L_F$: A joint Lipschitz bound on each upper-level component’s full gradient. **Domain:** $L_F>0$.

$\mu_y$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu_y>0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$n_f$: Number of upper-level finite-sum components **Domain:** Positive integer.

$n_g$: Number of lower-level finite-sum components **Domain:** Positive integer.

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$f_i,g_j$: Upper- and lower-level component functions in the finite sums **Domain:** $1\le i\le n_f,\ 1\le j\le n_g$.

$i,j$: Upper- and lower-level component indices queried by the algorithm

$v_0,v_t$: Public initial adjoint vector and the algorithm's adjoint iterates. **Domain:** $v_0,v_t\in\mathbb R^{d_y}$.

$g_{j,xy},g_{j,yy}$: Cross-Hessian and lower-variable Hessian blocks of lower component $j$.

$t,s,\operatorname{span}$: These denote the current iteration, a historical iteration, and a linear span. Enforce the three algorithm-restriction formulas separately.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

$N_{\rm tuple}$: Calls returning the joint tuple of two-level gradients and derivative–vector products. **Domain:** Nonnegative integer.

## 3. Complexity bracket

### Compared quantities

#### Q1 - source scoped metric resource statement

**Metric contract.** E||grad Phi(x_hat)||^2 <= epsilon^2.

**Resource contract.** metric: Q_tuple, the number of calls to the joint tuple in source Eq.(11).; budget: Fixed worst-case call budget.; mapping: One tuple can be simulated by four separate declared component operations, but arbitrary separate-operation algorithms need not satisfy Definition 4.2.

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

### R1 - BM_BOUND_finite_linear_native_lower source window

**Region.** $\varepsilon^2\le\Delta L_F/(1000n_f)$. Retain the source smoothness class and the linear-iteration restriction in Definition 4.2. The hard-instance dimension may grow as specified in Theorem 2.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Upper bound missing

**Lower bound.** B1

**Upper bound.** No admitted bound for this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** The lower-bound hard-instance dimension may grow with $\Delta,L_F,n_f,1/\varepsilon$. Here $L_F$ is the smoothness budget of the upper-level component gradients. The embedded reduced objective inherits that scale; this does not add a reduced-smoothness assumption to the full model class.

**Resource mapping.** Charge the joint tuple calls of source equation (11), retaining that restricted model.

### B1 - Finite-sum zero-chain embedded through g(y,x)=||y-x||^2/2

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** The stated restricted randomized class

$$
\Omega(\sqrt{n_f}\,\varepsilon^{-2})
$$

**Sources.** [1](https://proceedings.mlr.press/v238/dagreou24a/dagreou24a.pdf)

**Constants.** Hold the stated regularity and initialization budgets fixed. Joint optimality is not claimed for parameters whose dependence is untracked.

**Source location.** [1](https://proceedings.mlr.press/v238/dagreou24a/dagreou24a.pdf) pdf pages: 3; 4; 5; 6; 7; theorem or section: Assumptions 2.1–2.2; Eq.(11); Definitions 4.1–4.2; Theorems 1–2; theorem: Assumptions 2.1–2.2; Eq.(11); Definitions 4.1–4.2; Theorems 1–2

## References

[1] Mathieu Dagréou; Thomas Moreau; Samuel Vaiter; Pierre Ablin. A Lower Bound and a Near-Optimal Algorithm for Bilevel Empirical Risk Minimization. 2024. AISTATS 2024, PMLR 238.

https://proceedings.mlr.press/v238/dagreou24a/dagreou24a.pdf
