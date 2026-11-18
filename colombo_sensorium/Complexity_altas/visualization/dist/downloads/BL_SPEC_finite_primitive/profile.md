# Finite-sum bilevel optimization with selectable original component gradients

**Setting ID.** `BL_SPEC_finite_primitive`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Other quantified gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Bilevel unique reduced; task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Initial gap; initialization: Initial solution distance; smoothness: Componentwise sc and derivative lipschitz; structure: Finite sum; structure: Finite sum componentwise sc

**ORACLE tags.** feedback quality: Exact; interface family: Exact gradient; operation: Component gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N grad f; measure: N grad g; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

### Admissible model

Assume $f=(1/n_f)\sum_i f_i$. Each upper component's full gradient is jointly 1-Lipschitz in $(x,y)$. Only the average satisfies $\|\nabla_y f\|\le1$; individual $f_i$ partial gradients need not be bounded.

Assume $g=(1/n_g)\sum_j g_j$. Each lower-level component $g_j$ is twice continuously differentiable. Its full gradient and Hessian are jointly 1-Lipschitz in $(x,y)$, and it is $\mu$-strongly convex in y for fixed x.

The optimized upper-level objective $\Phi$ is bounded below. The supplied x0 satisfies $\Phi(x_0)-\inf_x\Phi(x)\le1$, a public fixed bound.

Given $\|y_0-y^*(x_0)\|\le R_{init}=1$, the algorithm sets $z_{init}=y_0,v_{init}=0$. The full scan used to compute the source initialization residual remains charged. This uniform certificate controls the initialization logarithm in the fixed-budget class.

### Oracle interface

Public inputs are dimension, target accuracy, the model's budgets, and the initial point. The original functions, their lower-level solutions, and the reduced objective are hidden. Queries are restricted to the stated interfaces; inner optima and undeclared derivatives are not available for free.

$(i,x,y), i\in\{1,\ldots,n_f\}\longmapsto \nabla f_i(x,y)=(\nabla _x f_i,\nabla _y f_i)$. The oracle returns the exact full gradient of the selected component, with no additional oracle noise. Unbiasedness for the population mean holds only when the algorithm samples components uniformly.

$(j,x,y), j\in\{1,\ldots,n_g\}\longmapsto \nabla g_j(x,y)=(\nabla _x g_j,\nabla _y g_j)$ The full gradient of the chosen component is exact, with no additional oracle noise. It is unbiased for the population average only when the algorithm samples components uniformly.

A selected component may be evaluated at arbitrarily many points, with each gradient evaluation charged separately.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2^2$. The tolerance $\varepsilon$ is always expressed on the gradient-norm scale. The mean-square requirement is equivalent to the RMS gradient being at most this tolerance.

In this unconstrained model with a strongly convex lower level, $\nabla\Phi(x)=\nabla_x f(x,y^*)-g_{xy}(x,y^*)g_{yy}(x,y^*)^{-1}\nabla_y f(x,y^*)$, where $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$, and $y^*$ denotes $y^*(x)$. The identity defines the hypergradient without granting additional query access.

### Resource accounting

Compare $Q=N_{\nabla f}+N_{\nabla g}$. Each complete gradient of a selected component costs one call; evaluations at different points are charged separately. A complete scan of both layers costs $n_{\rm tot}=n_f+n_g$ calls.

Initialization oracle calls count toward the total. A finite initialization bound is an instance-class assumption, not free access to an inner solver.

The budget is a fixed worst-case cap on every execution path; every actual response within a batch is counted.

Internal processing of available information is free. Comparisons use the explicitly specified scalarization or resource vector. Different resources without given weights cannot be assembled coordinatewise from separate algorithms.

### Algorithm views and success guarantees

Algorithms may use private randomness. Queries, stopping, and postprocessing may be arbitrary measurable functions of the transcript. The output may be unqueried, a random selection of a past point, or an admissible average. No linear-span or zero-respecting restriction is imposed. Queries are sequential; each actual response in a parallel batch is charged separately. Arithmetic, linear algebra, and storage using received data are uncharged. Internal operations, memory, and communication are not tracked by this quantity.

Choose one algorithm from the public parameters, then require $\mathbb{E}\|\nabla\Phi(\widehat{x})\|_2^2\le\varepsilon^2$ for every admissible instance and legal oracle law. Expectation includes all algorithmic and feedback randomness, with the instance fixed first.

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

$L$: A common Lipschitz bound for both full gradients in the joint variables, normalized here to one. **Domain:** $L=1$.

$C_f$: Uniform norm upper bound for the lower-variable block of the population upper-level gradient; normalized to one in this profile **Domain:** $C_f=1$.

$\mu$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu>0$.

$\rho$: Joint Lipschitz upper bound for the lower-level cross-Hessian and lower-Hessian blocks; normalized to one in this profile **Domain:** $\rho=1$.

$\Delta$: A public initial reduced-objective gap bound, normalized here to one. **Domain:** $\Delta=1$.

$\kappa$: The lower-level condition number under unit smoothness normalization. **Domain:** $\kappa\ge1$.

$\kappa=1/\mu$

$n_f$: Number of upper-level finite-sum components **Domain:** Positive integer.

$n_g$: Number of lower-level finite-sum components **Domain:** Positive integer.

$n_{\mathrm{tot}}$: The sum of upper- and lower-level component counts. **Domain:** Positive integer.

$n_{\mathrm{tot}}=n_f+n_g$

$R_{\rm init}$: Normalized initial lower-level distance budget in the finite-sum primitive-gradient model. **Domain:** $R_{\rm init}=1$.

$\varepsilon_*$: Small-accuracy threshold for validity of the source lower bound **Domain:** Fixed positive number.

Define $\varepsilon_*=\min\{1,\varepsilon_L\}$, where $\varepsilon_L$ is the source theorem's threshold.

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$f_i,g_j$: Upper- and lower-level component functions in the finite sums **Domain:** $1\le i\le n_f,\ 1\le j\le n_g$.

$i,j$: Upper- and lower-level component indices queried by the algorithm

$z_{\rm init},v_{\rm init}$: Auxiliary initialization used by the source algorithm

$z_{\rm init}=y_0,\ v_{\rm init}=0$

$N_{\nabla f}$: Upper-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_{\nabla g}$: Lower-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O,\omega}C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \mathbb E\|\nabla\Phi_I(\hat x_{\mathcal A})\|^2\le\varepsilon^2\}.\\C=N_{\nabla f}+N_{\nabla g}.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - The joint window in component count and condition number.

**Region.** Assume $n_f\ge1024$, $n_g\ge1$, $\kappa\ge2$, and $0<\varepsilon\le\min\{1,\varepsilon_L\}$. Initial gap and lower-level distance use public unit budgets; other structure follows the source normalization. Hard-instance dimension may grow.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Other quantified gap

**Lower bound.** B2

$$
\Omega (n_f+n_g+\sqrt{n_f} \kappa ^2 \varepsilon ^{-2})
$$

**Upper bound.** B1

$$
\widetilde O(n_{\mathrm{tot}}+\sqrt{n_{\mathrm{tot}}} \kappa ^{7/2} \varepsilon ^{-2})
$$

**Gap or comparison.** Let $n_{\rm tot}=n_f+n_g$. The current upper-to-lower ratio is at most $$
\widetilde{O}\!\left(\frac{n_{\rm tot}+\sqrt{n_{\rm tot}}\kappa^{7/2}\varepsilon^{-2}}{n_{\rm tot}+\sqrt{n_f}\kappa^2\varepsilon^{-2}}\right).
$$. The lower bound does not yet establish a leading $\sqrt{n_g}$ term for every component split.

**Comparison argument.** The joint regime implies every numerical condition in the source upper and lower bounds. The upper bound covers both $n_{\mathrm{tot}}>\kappa$ and $n_{\mathrm{tot}}\le\kappa$. The three hard families in Appendix F have initial lower-level minimizers $y^\star(0)=0$, $0$, and $\pm1$, respectively, and satisfy $R_{\rm init}=1$, retaining both component-count lower terms. The condition $\Delta=1$ is an upper budget, not an exact gap.

### R2 - Balanced regime for the upper- and lower-level component counts

**Region.** The stated joint finite-sum parameter window holds, with $n_g\le n_f$. Public initialization and structural normalization budgets are fixed.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Polynomial gap

**Lower bound.** B2

$$
\Omega (n_f+n_g+\sqrt{n_f} \kappa ^2 \varepsilon ^{-2})
$$

**Upper bound.** B1

$$
\widetilde O(n_{\mathrm{tot}}+\sqrt{n_{\mathrm{tot}}} \kappa ^{7/2} \varepsilon ^{-2})
$$

**Gap or comparison.** On the $n_g\le n_f$ window, the ratio is at most $\widetilde{O}(\kappa^{3/2})$. For fixed $\kappa$, dependence on $n_{\rm tot}$ and $\varepsilon$ matches up to logarithms. This does not cover the split $n_g\gg n_f$.

**Comparison argument.** The balanced regime is the joint regime intersected with $n_g\le n_f$. Hence $n_f\le n_{\mathrm{tot}}\le2n_f$, and $$n_{\mathrm{tot}}+\sqrt{n_{\mathrm{tot}}}\kappa^{7/2}\varepsilon^{-2}\le\sqrt2\kappa^{3/2}(n_{\mathrm{tot}}+\sqrt{n_f}\kappa^2\varepsilon^{-2}).$$ Both the upper construction and every Appendix F lower family obey $R_{\rm init}=1$. No assertion is made for $n_g\gg n_f$.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Fix public $R_{\rm init}=1$ and unit $L,C_f,\rho,\Delta$ budgets, and take $\varepsilon\le\varepsilon_*$. Initialization conditions are checked against Theorem 5.1, Appendix E, and Proposition F.1 of the source.

**Oracle mapping.** The algorithm chooses an $f_i$ or $g_j$ component index and receives that component’s exact full gradient. Each selected component costs one call. Full gradients and scans are not free, and the interface provides no JVP or HVP.

**Guarantee mapping.** The native target is $\mathbb E\|\nabla\Phi(\widehat x)\|^2\le\varepsilon^2$, a root-mean-square tolerance, rather than $\mathbb E\|\nabla\Phi(\widehat x)\|\le\varepsilon^2$.

**Output mapping.** Return one outer point $\widehat x$. Expectation uses the oracle and algorithm randomness stated in the contract.

**Resource mapping.** Charged resources are $N_{\nabla f}$ and $N_{\nabla g}$. Each execution has a fixed worst-case budget, rather than an expected call budget.

### B1 - SICBO

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{\mathcal{O}}\!\left(n_{\mathrm{tot}}+\sqrt{n_{\mathrm{tot}}}\,\kappa^{7/2}\varepsilon^{-2}\right),\qquad n_{\mathrm{tot}}=n_f+n_g
$$

**Sources.** [1](https://arxiv.org/pdf/2610.24538v1)

**Dimension conditions.** Valid in every finite dimension of the declared model. No additional dimension dependence is introduced beyond the formula.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad f+N grad g.**

$$
\widetilde O(n_{\mathrm{tot}}+\sqrt n_{\mathrm{tot}}\kappa ^{7/2}\varepsilon ^{-2})
$$

**N HVP.** 0

**N JVP.** 0

**N inner solve.** 0

**Constants.** Component smoothness and the average $\|\nabla_yf\|$ budget are normalized to one. The quantity $\Delta$ is fixed, and polynomial dependence on $n_{\rm tot},\kappa,\varepsilon$ is explicit.

**Logarithmic factors.** Logarithmic factors in dimension, accuracy, solver confidence, and initial distance.

**Derivation.** Fixing the public initialization budget $R_{\rm init}=1$ makes the logarithmic initialization terms in the source upper bound uniform over the declared instance class. The hard lower-bound instances have initial lower-level solutions $y^*(0)=0$ or $\pm1$, both within that budget.

**Source location.** [1](https://arxiv.org/pdf/2610.24538v1) theorem: Theorem 5.1; section: 2,5; pdf pages: 2; 6; equations: (13); (14)

### B2 - bounded-gradient hidden chain plus two finite-sum needles

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(n_f+n_g+\sqrt{n_f}\,\kappa^2\varepsilon^{-2}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.24538v1)

**Dimension conditions.** Dimension may grow with $n_f,n_g,\kappa,\varepsilon$ and the query budget.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.**

$$
\Omega (n_f+n_g+\sqrt{n_f} \kappa ^2 \varepsilon ^{-2})
$$

**Constants.** Only universal constants are suppressed.

**Derivation.** Fixing the public initialization budget $R_{\rm init}=1$ makes the logarithmic initialization terms in the source upper bound uniform over the declared instance class. The hard lower-bound instances have initial lower-level solutions $y^*(0)=0$ or $\pm1$, both within that budget.

**Source location.** [1](https://arxiv.org/pdf/2610.24538v1) theorem: Proposition F.1; section: Appendix F.2; pdf pages: 21; 22; 23; equations: (F.1); (F.4); (F.6)

The affine lower-level solution $y^*(x)=(\kappa-1)x$ embeds a finite-sum bounded-gradient chain into bilevel stationarity, with amplification $\kappa-1$. Linear terms in upper- and lower-level component counts come from different hard families. The information lemma of Peng et al. has not been independently reproved. The source $\sqrt n$ is the upper-level component count and cannot be replaced by $\sqrt{n_f+n_g}$ for arbitrary splits.

## References

[1] Qihao Zhou; Shanshui Niu. Accelerating Finite-Sum Bilevel Optimization with Fully First-Order Oracles. 2026. arXiv:2610.24538v1, 2026-10-17.

https://arxiv.org/pdf/2610.24538v1
