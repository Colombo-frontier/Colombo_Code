# Strongly convex reduced objective: derivative-vector products and function-value gap

**Setting ID.** `BL_SPEC_sc_gap_derivative`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Bounds missing

**TASK tags.** task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; convexity: Reduced objective strongly convex; initialization: Bounded initial inner distance; initialization: Initial distance

**ORACLE tags.** interface family: Derivative vector; query domain: Full space

**ALGORITHMS tags.** restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** mode: Deterministic

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

### Admissible model

The function $g(x,\cdot)$ is $\mu_y$-strongly convex on all of $\mathbb{R}^{d_y}$, uniformly for $x$. The quantities $\nabla f,\nabla g$ are jointly $L_f,L_g$-Lipschitz, and $g_{xy},g_{yy}$ are respectively $\rho_{xy},\rho_{yy}$-Lipschitz, in Euclidean induced operator norms.

The condition $\|\nabla_y f(x,y)\|\le B_f$ holds everywhere. The public initial point satisfies $\|y_0-y^*(x_0)\|\le R_y$, and there exists $x^*\in\arg\min\Phi$ satisfying $\|x_0-x^*\|\le R_x$. Joint convexity of the primitive $f$ is not assumed.

The reduced objective $\Phi$ is $\mu_x$-strongly convex, with $\mu_x>0$.

### Oracle interface

All dimensions, model budgets, and initial points are public. At any $(x,y)\in\mathbb{R}^{d_x+d_y}$, the algorithm selects $h\in\{f,g\}$ and receives exact full gradient $\nabla h(x,y)$. One call returns only the selected function's gradient. The functions and lower-level optimum remain hidden.

The additional operations $(x,y,v)\mapsto g_{xy}(x,y)v$ and $(x,y,v)\mapsto g_{yy}(x,y)v$ are permitted, with $v\in\mathbb{R}^{d_y}$. They return exact vectors rather than full matrices.

No direct reduced-gradient, lower-level optimum, or inverse-Hessian interface is supplied. Arithmetic based on public data is free.

### Output

Return $\widehat{x}\in\mathbb{R}^{d_x}$, which may be an unqueried point or any admissible postprocessing of the transcript. An inner optimizer or certificate is not required.

### Loss or accuracy criterion

The base error is $\Phi(\widehat{x})-\Phi^*$, where $\Phi^*=\min_x\Phi(x)$.

### Resource accounting

The native resource is $(N_{\nabla f},N_{\nabla g},N_J,N_H)$. Each operation costs one unit in its coordinate. Keep the joint budget unless weights are specified; use $N=N_{\nabla f}+N_{\nabla g}+N_J+N_H$ only for an explicitly declared unit-total-cost projection. The budget is a fixed worst-case cap.

### Algorithm views and success guarantees

Algorithms are deterministic and adaptive. Queries, stopping, and postprocessing may be arbitrary measurable functions of the transcript. The output may be unqueried, a deterministic selection of a past point, or an admissible average. No linear-span or zero-respecting restriction is imposed. Queries are sequential; each actual response in a parallel batch is charged separately. Arithmetic, linear algebra, and storage using received data are uncharged. Internal operations, memory, and communication are not tracked by this quantity.

There exists an algorithm determined by the public inputs such that $\Phi(\widehat{x})-\Phi^*\le\varepsilon$ holds on every admissible instance. The guarantee is deterministic and instancewise.

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

$B_f$: A uniform norm bound on the population upper function’s lower-variable gradient block. **Domain:** $B_f\ge0$.

$\|\nabla_yf(x,y)\|\le B_f$

$\mu_y$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu_y>0$.

$\mu_x$: The reduced objective’s strong-convexity modulus. **Domain:** $\mu_x>0$.

$\rho_{xy}$: Joint-variable Lipschitz upper bound for the lower cross-Hessian block. **Domain:** $\rho_{xy}\ge0$.

$\rho_{yy}$: Joint-variable Lipschitz upper bound for the lower-level lower-Hessian block **Domain:** $\rho_{yy}\ge0$.

$R_x$: Public distance bound from the outer initial point to some global minimizer **Domain:** $R_x\ge0$.

$\|x_0-x^*\|\le R_x$

$R_y$: Public initial lower-level distance bound **Domain:** $R_y\ge0$.

$\|y_0-y^*(x_0)\|\le R_y$

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$v$: The algorithm-selected direction for a derivative–vector query. **Domain:** $v\in\mathbb R^{d_y}$.

$\Phi^*,x^*$: Global minimum of the reduced objective and an optimizer satisfying the initial-distance budget.

$L_\Phi$: Effective reduced-gradient Lipschitz upper bound derived from the declared budgets.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
Q^*(\varepsilon)=\inf_A\sup_{I,\mathcal O}N(A,I,\mathcal O)
$$

### R1 - The objective-gap region at fixed structural budgets.

**Region.** All positive regularity, initial-distance, and dimension budgets are fixed, with $\varepsilon\downarrow0$ and fixed $\mu_x>0$. The comparison concerns accuracy dependence only; joint dependence on condition numbers is not certified as optimal.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

**Gap or comparison.** An upper bound is available at fixed structural budgets. No lower bound for arbitrary deterministic algorithms under this same specification is currently registered. The Ji–Liang lower bound applies only to the algorithm class in their Definition 2 and therefore does not certify unrestricted optimality.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Soft-O notation allows logarithmic factors in $1/\varepsilon$, with all structural budgets fixed. Each coordinate of the joint resource vector is bounded by the total-operation bound. This comparison assigns unit cost to every operation.

**Dimension conditions.** The upper bound holds for every finite-dimensional instance in the declared model. Any dimension or fixed-budget dependence not displayed explicitly follows the accompanying evidence qualification.

### B1 - AccBiO-BG with exact derivative–vector products.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\widetilde{\mathcal{O}}_{\rm fixed}(1)
$$

**Sources.** [1](https://www.jmlr.org/papers/volume24/21-0949/21-0949.pdf)

**Constants.** Unshown regularity, initialization, and noise budgets are fixed. Their joint parameter dependence is not certified as closed.

**Source location.** [1](https://www.jmlr.org/papers/volume24/21-0949/21-0949.pdf) theorem: Theorem 13; section: 5; Assumption 3

The source permits blockwise smoothness constants. The joint constant $L_f,L_g$ bounds the relevant block constants, and $\|\nabla_yf\|\le B_f$ holds here. The displayed accuracy order fixes the other budgets; its leading parameter term is not asserted to remain uniform at zero endpoints.

## References

[1] Kaiyi Ji; Yingbin Liang. Lower Bounds and Accelerated Algorithms for Bilevel Optimization. 2023. JMLR 24 (2023), 21-0949.

https://www.jmlr.org/papers/volume24/21-0949/21-0949.pdf
