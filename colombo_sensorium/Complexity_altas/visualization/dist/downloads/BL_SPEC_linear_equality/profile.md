# Equality-constrained lower level: primitive gradients and the outer gradient mapping

**Setting ID.** `BL_SPEC_linear_equality`

Bilevel optimization

Let $h(x,y)=Ax-By-b$, $y^*(x)=\operatorname*{argmin}_{y:\,h(x,y)=0}g(x,y)$, and $\Phi(x)=f(x,y^*(x))$. Seek the following approximate stationarity criterion for $\min_{x\in X}\Phi(x)$.

**Status.** Bounds missing

**TASK tags.** task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Initial distance; initialization: Initial gap

**ORACLE tags.** interface family: Exact gradient

**ALGORITHMS tags.** restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Gradient mapping

**GUARANTEE tags.** mode: Deterministic

**RESOURCE tags.** accounting: Joint coordinates retained; measure: N grad f; measure: N grad g; measure: N proj x

## 1. Setting specification

### Task

Let $h(x,y)=Ax-By-b$, $y^*(x)=\operatorname*{argmin}_{y:\,h(x,y)=0}g(x,y)$, and $\Phi(x)=f(x,y^*(x))$. Seek the following approximate stationarity criterion for $\min_{x\in X}\Phi(x)$.

### Admissible model

The function $f$ has $C_f$-Lipschitz joint gradient and is $L_f$-Lipschitz in value. The function $g$ has $C_g$-Lipschitz joint gradient and is $\mu_y$-strongly convex in $y$. All norms are Euclidean or their induced operator norms.

Inputs $A\in\mathbb{R}^{d_h\times d_x}$, $B\in\mathbb{R}^{d_h\times d_y}$, and $b\in\mathbb{R}^{d_h}$ are public. The matrix $B$ has full row rank and smallest singular value at least the public $\beta_B>0$. The initial point has upper-level gap at most $\Delta$ and lower-level initial distance at most $R_y$.

The set $X$ is nonempty, compact, and convex with diameter at most $D_X$. The full Hessian of $g$ is $S_g$-Lipschitz on $X\times\mathbb{R}^{d_y}$. Along the solution graph, the inverse lower-level KKT matrix has the public uniform bound $C_H$.

### Oracle interface

Choose $f$ or $g$ and obtain its exact full gradient at an admissible pair $(x,y)$, where $x\in X$ and $y\in\mathbb R^{d_y}$.

Operations with the known linear constraints and their projections are free. The interface $\Pi_X$ is also available, with its count recorded separately. Lower-level solutions, active sets, and hypergradients are not supplied by default.

### Output

Return an outer point $\widehat{x}\in X$, possibly unqueried. Neither an inner point nor a certificate is required.

### Loss or accuracy criterion

Define $\mathcal{G}_\tau(x)=\tau^{-1}[x-\Pi_X(x-\tau\nabla\Phi(x))]$ and error $\|\mathcal{G}_\tau(\widehat{x})\|$. The step size $0<\tau\le1/L_\Phi$ is public and fixed; $L_\Phi$ bounds reduced-gradient Lipschitz continuity.

### Resource accounting

Retain the primitive call counts at both levels and the outer projection count. The scalar gradient cost is $N=N_{\nabla f}+N_{\nabla g}$, with projections recorded separately. Every call in an approximate inner solve counts toward the fixed budget.

### Algorithm views and success guarantees

Algorithms are deterministic and may use arbitrary measurable adaptive queries, stopping, and postprocessing. Outputs may be unqueried, deterministically selected historical points, or admissible averages. No span or zero-respecting restriction applies. Queries are sequential; each response in a batch is charged. Internal arithmetic, linear algebra, and storage are free, with no separate work, memory, or communication budget.

The condition $\|\mathcal{G}_\tau(\widehat{x})\|\le\varepsilon$ holds deterministically on each instance.

## 2. Notation and parameters

$x,y$: The upper- and lower-level variables. **Domain:** $x\in X,y\in\mathbb R^{d_y}$.

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

$S_g$: Lipschitz upper bound for the complete lower-level Hessian on the declared query domain **Domain:** $S_g\ge0$.

$C_H$: Uniform operator-norm bound on the inverse lower-level KKT matrix along the solution graph. **Domain:** $C_H<\infty$.

$D_X$: Euclidean diameter bound for the public outer feasible set **Domain:** $D_X<\infty$.

$\tau$: The public fixed step size in the gradient mapping. **Domain:** $0<\tau\le1/L_\Phi$.

$\kappa_g$: Lower-level condition number **Domain:** $\kappa_g\ge1$.

$\kappa_g=C_g/\mu_y$

$C_J$: Effective operator-norm bound for the Jacobian of the lower-level solution map **Domain:** $C_J\ge0$.

$C_J=C_H(C_g+\|A\|)$

$L_\Phi$: An effective Lipschitz bound on the reduced gradient. **Domain:** $L_\Phi>0$.

Use $L_\Phi=(C_f+L_fC_HS_g)(1+C_J)^2$ or any larger valid upper bound.

$A,B,b$: The public lower-level linear-constraint coefficients. **Domain:** $A\in\mathbb R^{d_h\times d_x},B\in\mathbb R^{d_h\times d_y},b\in\mathbb R^{d_h}$.

$h$: Residual of the public linear constraints

$h(x,y)=Ax-By-b$

$X,\Pi_X$: Public outer feasible set and its Euclidean projection

$\mathcal G_\tau$: Gradient mapping of the reduced objective

$\mathcal G_\tau(x)=\tau^{-1}[x-\Pi_X(x-\tau\nabla\Phi(x))]$

$\mathcal K$: Lower-level KKT matrix along the solution graph

$\mathcal K=\begin{bmatrix}g_{yy}&-B^\top\\-B&0\end{bmatrix}$, $\|\mathcal K^{-1}\|\le C_H$

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

$N_{\Pi_X}$: Number of public outer projection calls, recorded separately from gradient calls **Domain:** Nonnegative integer.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
Q^*(\varepsilon)=\inf_A\sup_{I,\mathcal O}N(A,I,\mathcal O)
$$

### R1 - A fixed step size and nondegenerate model budgets.

**Region.** Assume $\tau=1/L_\Phi$ and sufficiently small $\varepsilon$, with $L_\Phi=(C_f+L_fC_HS_g)(1+C_J)^2>0$, $C_J=C_H(C_g+\|A\|)$, and $\kappa_g=C_g/\mu_y$. Constraint conditioning, compact-set diameter, and initialization budgets are fixed.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

**Gap or comparison.** An upper bound is available in this window. No matching-specification lower bound is registered.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The scalar count includes only original gradients at the two levels; outer projections are separately counted as $O(1+L_\Phi\Delta\varepsilon^{-2})$.

**Dimension conditions.** The upper bound holds for every finite-dimensional instance in the declared model. Any dimension or fixed-budget dependence not displayed explicitly follows the accompanying evidence qualification.

### B1 - Finite-difference hypergradients, accelerated inner solves, and projected descent.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\widetilde{\mathcal{O}}\!\left(\sqrt{\kappa_g}\,[1+L_\Phi\Delta\varepsilon^{-2}]\right)
$$

**Sources.** [1](https://proceedings.neurips.cc/paper_files/paper/2024/file/ffd86e56e6403d63dd6face033060e5a-Paper-Conference.pdf)

**Constants.** Unshown regularity, initialization, and noise budgets are fixed. Their joint parameter dependence is not certified as closed.

**Derivation.** Implicit KKT differentiation gives an effective $L_\Phi$. Projected descent needs $O(1+L_\Phi\Delta/\varepsilon^2)$ surrogate evaluations, each implemented using $\widetilde O(\sqrt{\kappa_g})$ exact primitive-gradient calls.

**Source location.** [1](https://proceedings.neurips.cc/paper_files/paper/2024/file/ffd86e56e6403d63dd6face033060e5a-Paper-Conference.pdf) theorem: Theorem 3.1; Appendix B, Algorithm 5

Combine $\|D_xy^*\|\le C_J$ and $\operatorname{Lip}(D_xy^*)\le C_HS_g(1+C_J)^2$ to obtain $L_\Phi$. This retains the $C_f$ term when $S_g=0$, avoiding degeneration of the source displayed formula at that endpoint.

Compute each hypergradient proxy to uniform error $O(\varepsilon)$ and select the smallest computable approximate gradient mapping. This provides a deterministic output for each instance. Accelerated gradient descent solves the strongly convex inner problems to the required accuracy.

## References

[1] Guy Kornowski; Swati Padmanabhan; Kai Wang; Jimmy Zhang; Suvrit Sra. First-Order Methods for Linearly Constrained Bilevel Optimization. 2024. NeurIPS2024 proceedings PDF.

https://proceedings.neurips.cc/paper_files/paper/2024/file/ffd86e56e6403d63dd6face033060e5a-Paper-Conference.pdf
