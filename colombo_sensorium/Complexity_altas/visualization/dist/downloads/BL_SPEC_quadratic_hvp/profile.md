# Quadratic lower levels: exact values, gradients, and vector products.

**Setting ID.** `BL_SPEC_quadratic_hvp`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Bounds missing

**TASK tags.** formulation: Bilevel unique reduced; task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Initial gap; smoothness: Lipschitz gradient; structure: Quadratic lower

**ORACLE tags.** feedback quality: Exact; interface family: Derivative vector; operation: Cross derivative vector product; operation: Function value; operation: Hessian vector product; operation: Primitive gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar function value (order 0); scalar derivative order: Scalar-function first derivative; scalar derivative order: Scalar-function second derivative

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N grad f; measure: N grad g; measure: N hvp; measure: N jvp; measure: N source bundle; measure: N value f; measure: N value g; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

### Admissible model

Assume $g(x,y)=\tfrac12y^\top Hy+x^\top Jy+b^\top y$, $H=H^\top$, $\mu I\preceq H\preceq LI$, and $\|J\|\le L$, with fixed unknown coefficients. The function $g$ is strongly convex in $y$ but need not be jointly convex.

The class inclusion in Definition 2.3 still requires $\nabla g$ to be $L$-Lipschitz jointly in $(x,y)$. Equivalently, its constant joint Hessian $\bigl[\begin{smallmatrix}0&J\\J^\top&H\end{smallmatrix}\bigr]$ has operator norm at most $L$. Separate bounds on H and J alone do not ensure the same L.

The full gradient of $f$ is jointly $L$-Lipschitz. Nonconvexity is allowed. No finite global Lipschitz or norm bound is imposed on the values of $f$ or on $f_y$.

$\Phi(0)-\inf_x\Phi(x)\le\Delta$, with upper-level initial point zero. The lower-level initial point may also be zero, but no additional uniform distance bound is imposed.

### Oracle interface

Public inputs are dimension, target accuracy, the model's budgets, and the initial point. The original functions, their lower-level solutions, and the reduced objective are hidden. Queries are restricted to the stated interfaces; inner optima and undeclared derivatives are not available for free.

The map $(x,y)\mapsto f(x,y)$ is returned exactly, with no additional random noise.

The map $(x,y)\mapsto\nabla f(x,y)$ is returned exactly, with no additional random noise.

The map $(x,y)\mapsto g(x,y)$ is returned exactly, with no additional random noise.

The response is $(x,y)\longmapsto \nabla g(x,y)$, returned exactly with no additional stochastic noise.

The map $(x,y,v)\mapsto g_{xy}(x,y)v$ is returned exactly, with no additional random noise.

$(x,y,v)\longmapsto g_{yy}(x,y)v$. The stated response is exact, with no additional random noise.

The bundled interface $O_{\rm fo}$ in Definition 2.4 returns $f,g,\nabla f,\nabla g$ in one call. Here it is split into four charged primitive operations, so one source call costs four. Definition 2.6 adds cross-derivative action $Jv$ and lower-Hessian action $Hv$ to interface $O_{\rm hvp}$; at most six primitive calls simulate it.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2$, with $\varepsilon$ always specified on the gradient-norm scale. Gradient norm and squared gradient norm remain distinct.

In this unconstrained model with a strongly convex lower level, $\nabla\Phi(x)=\nabla_x f(x,y^*)-g_{xy}(x,y^*)g_{yy}(x,y^*)^{-1}\nabla_y f(x,y^*)$, where $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$, and $y^*$ denotes $y^*(x)$. The identity defines the hypergradient without granting additional query access.

### Resource accounting

Q is the unit-weight sum of all available operations. Simulation in both directions with the source's joint oracle differs only by a fixed constant; the source's native accounting is retained in the explanation.

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

$\mu$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu>0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$\kappa_y$: Condition number of the quadratic lower level **Domain:** $\kappa_y\ge1$.

$\kappa_y=L/\mu$

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$v$: The algorithm-selected direction for a derivative–vector query. **Domain:** $v\in\mathbb R^{d_y}$.

$H,J,b$: The coefficient matrix and linear term of the hidden quadratic lower level. **Domain:** $H\in\mathbb R^{d_y\times d_y},\ J\in\mathbb R^{d_x\times d_y},\ b\in\mathbb R^{d_y}$.

$I$: Identity matrix of the corresponding dimension

$\preceq$: The positive-semidefinite order on symmetric matrices.

$L_1$: The source notation for the joint-gradient Lipschitz budget. **Domain:** $L_1=L$.

$O_{\rm fo},O_{\rm hvp}$: The source joint first-order interface and additional derivative-vector-product interfaces, charged per primitive response.

$N_{\nabla f}$: Upper-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_{\nabla g}$: Lower-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_J$: The number of lower cross-derivative–vector responses. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_H$: Number of lower-level Hessian-vector product responses **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_{f,\rm val}$: The number of upper-level scalar-value responses. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_{g,\rm val}$: Number of lower-level scalar-value responses **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O}C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \|\nabla\Phi_I(\hat x_{\mathcal A})\|\le\varepsilon\}.\\C=N_{\nabla f}+N_{\nabla g}+N_J+N_H+N_{f^0}+N_{g^0}.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - The source theorem’s applicability window.

**Region.** The parameter $\kappa_y$ is at least the source's universal constant, and accuracy is small enough for a nontrivial hard-chain length. The hard dimension may grow with $\kappa_y$ and $\varepsilon$. Verification issues remain concerning the source quantifiers and the output correction.

**Quantity.** Q1

**Resource.** Charge the declared primitive operations. Source joint responses are simulated with four or six calls, as applicable, retaining the resource vector and fixed conversion constants.

**Status.** Both bounds missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** No admitted bound for this comparison

**Gap or comparison.** No upper or lower bound has yet passed an applicability check for this complete specification. The source is used only as the direct basis for the quadratic model and interface definition.

**Comparison argument.** Each included claim has verified statement and applicability; mathematics review is separately labeled. No numerical threshold inferred from asymptotics.

## 4. Bounds and supporting evidence

## References

[1] Lesi Chen; Kaiyi Ji; Jingzhao Zhang. On the Condition Number Dependency in Bilevel Optimization. 2026. arXiv:2511.22331v4, 2026-08-11.

https://arxiv.org/pdf/2511.22331v4
