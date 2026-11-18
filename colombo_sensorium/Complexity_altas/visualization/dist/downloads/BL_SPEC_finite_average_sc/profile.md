# Finite-sum bilevel optimization with strong convexity only in the average lower level.

**Setting ID.** `BL_SPEC_finite_average_sc`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the stated error criterion and guarantee. Assumptions on $f$, $g$, and $\Phi$ are specified separately. Here $f=n_f^{-1}\sum_i f_i$ and $g=n_g^{-1}\sum_jg_j$.

**Status.** Bounds missing

**TASK tags.** task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Bounded initial inner distance; structure: Finite sum

**ORACLE tags.** interface family: Exact gradient; query domain: Full space

**ALGORITHMS tags.** restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the stated error criterion and guarantee. Assumptions on $f$, $g$, and $\Phi$ are specified separately. Here $f=n_f^{-1}\sum_i f_i$ and $g=n_g^{-1}\sum_jg_j$.

### Admissible model

Each component gradient is $L$-Lipschitz in the joint Euclidean space. The $xy,yy$ Hessian block of every $g_j$ is $\rho$-Lipschitz. Only the average $g(x,\cdot)$ must be $\mu_y$-strongly convex; individual $g_j$ may be nonconvex.

Only the average upper-level function must satisfy $\|\nabla_yf\|\le B_f$. The function $\Phi$ is bounded below, and $\Phi(x_0)-\inf\Phi\le\Delta$ and $\|y_0-y^*(x_0)\|\le R_y$ hold.

### Oracle interface

Component counts, dimensions, budgets, and initial points are public. The algorithm chooses $(i,x,y)$ to obtain exact $\nabla f_i(x,y)$, or chooses $(j,x,y)$ to obtain exact $\nabla g_j(x,y)$. Any component may be queried repeatedly throughout the full space. There is no sample noise or additional hidden-solution interface.

### Output

Return any measurable $\widehat{x}\in\mathbb{R}^{d_x}$; unqueried outputs are allowed, with no inner point or certificate required.

### Loss or accuracy criterion

$\|\nabla\Phi(\widehat{x})\|_2^2$.

### Resource accounting

The resource is $N=N_{\nabla f}+N_{\nabla g}$, with one unit per full component gradient. A complete scan costs $n_f+n_g$. The budget is fixed on every execution path.

### Algorithm views and success guarantees

Arbitrary randomized adaptive algorithms are allowed, with measurable queries, stopping, and postprocessing. Outputs may be unqueried, randomly selected historical points, or admissible averages. No span or zero-respecting restriction applies. Queries are sequential; each response in a batch is charged. Internal arithmetic, linear algebra, and storage are free, with no separate work, memory, or communication budget.

For each instance, require $\mathbb{E}\|\nabla\Phi(\widehat{x})\|_2^2\le\varepsilon^2$. Expectation is over algorithmic randomness only.

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

$L$: Common joint-variable Lipschitz upper bound for the complete gradients at both levels **Domain:** $L\ge\mu_y>0$.

$B_f$: A uniform norm bound on the population upper function’s lower-variable gradient block. **Domain:** $B_f\ge0$.

$\|\nabla_yf(x,y)\|\le B_f$

$\mu_y$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu_y>0$.

$\rho$: Common joint Lipschitz upper bound for the lower function's cross-Hessian block and lower-variable Hessian block **Domain:** $\rho\ge0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_y$: Public initial lower-level distance bound **Domain:** $R_y\ge0$.

$\|y_0-y^*(x_0)\|\le R_y$

$n_f$: Number of upper-level finite-sum components **Domain:** Positive integer.

$n_g$: Number of lower-level finite-sum components **Domain:** Positive integer.

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$f_i,g_j$: Upper- and lower-level component functions in the finite sums **Domain:** $1\le i\le n_f,\ 1\le j\le n_g$.

$i,j$: Upper- and lower-level component indices queried by the algorithm

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Minimum charged resource attaining the stated success guarantee

**Scope.** The full documented parameter domain; no upper or lower bound is admitted for this comparison.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - The declared parameter domain.

**Region.** All admissible parameters in the eight-part specification; subregions with two-sided evidence have not yet been separated.

**Quantity.** Q1

**Resource.** The primary charged resource specified in the common resource contract.

**Status.** Both bounds missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** No admitted bound for this comparison

### R2 - Component-gradient lower bound in the normalized high-accuracy regime

**Region.** $n_f\ge1024$, $n_g\ge1$, $L=B_f=\rho=\Delta=R_y=1$, $\kappa=L/\mu_y\ge2$ and $0<\varepsilon\le\varepsilon_L$. The hard-instance dimensions can grow.

**Quantity.** Q1

**Resource.** The primary charged resource specified in the common resource contract.

**Status.** Upper bound missing

**Lower bound.** B1

$$
\Omega\!\left(n_f+n_g+\sqrt{n_f}\,\kappa^2\varepsilon^{-2}\right)
$$

**Upper bound.** No admitted bound for this comparison

**Comparison argument.** The lower envelope follows from an admissible hard subclass. No general upper envelope has been established in this comparison.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $n_f\ge1024$, $n_g\ge1$, $L=B_f=\rho=\Delta=R_y=1$, $\kappa=L/\mu_y\ge2$ and $0<\varepsilon\le\varepsilon_L$. The hard-instance dimensions can grow.

**Dimension conditions.** The source uses sufficiently large finite dimensions that can grow with the query budget.

**Oracle mapping.** Both contracts reveal the exact full gradient of a chosen component at an arbitrary query point, at unit cost. Restricting instances to the source's hard subclasses preserves all algorithm permissions.

**Guarantee mapping.** The source lower bound uses the same per-instance mean-square target $\mathbb E\|\nabla\Phi(\widehat{x})\|_2^2\le\varepsilon^2$ and covers the target fixed cap.

**Output mapping.** One arbitrary measurable upper-level point, which need not have been queried.

**Resource mapping.** Sum of calls to the two selectable component-gradient interfaces. The source fixed worst-case budget applies directly.

### B1 - Subclass transfer of the amplified-chain and component-needle lower bounds

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(n_f+n_g+\sqrt{n_f}\,\kappa^2\varepsilon^{-2}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.24538v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.**

$$
\Omega\!\left(n_f+n_g+\sqrt{n_f}\,\kappa^2\varepsilon^{-2}\right)
$$

**Constants.** Only universal constants are suppressed.

**Derivation.** Restrict the target instance class to the three source hard families. Their starting lower-level solutions are zero or plus/minus one and their lower Hessians are constant.

**Source location.** [1](https://arxiv.org/pdf/2610.24538v1) theorem: Proposition F.1 and its hard-family constructions; pdf pages: 21; 22; printed pages: 21; 22

The source lower bound covers randomized adaptive algorithms with arbitrary measurable outputs, using selectable exact full component gradients at both levels and a fixed worst-case budget.

Each lower component is strongly convex in all three hard families, so the lower population average is strongly convex as required here. The lower Hessians are constant and satisfy the target block regularity.

Choose the public starting points to be zero. The lower optimum at the starting point is zero in the amplified-chain and upper-needle families, and at distance one in the lower-needle family.

The componentwise strongly convex upper bound in the source has a stronger assumption than this profile. A matching upper bound for this profile remains unrecorded.

## References

[1] Qihao Zhou; Shanshui Niu. Accelerating Finite-Sum Bilevel Optimization with Fully First-Order Oracles. 2026. arXiv:2610.24538v1, 2026-10-17.

https://arxiv.org/pdf/2610.24538v1
