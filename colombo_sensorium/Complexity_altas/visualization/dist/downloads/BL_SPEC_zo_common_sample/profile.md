# Stochastic bilevel function values with reuse of the same sample at multiple points

**Setting ID.** `BL_SPEC_zo_common_sample`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Bounds missing

**TASK tags.** formulation: Bilevel unique reduced; task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; existence: Uniform bounded solution; initialization: Bounded initial potential; initialization: Initial distance; smoothness: Full hessian lipschitz; smoothness: Lipschitz gradient; smoothness: Value lipschitz; stochastic model: Fourth moment

**ORACLE tags.** feedback quality: Value sample; interface family: Zeroth common sample; operation: Sample function value; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar function value (order 0)

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N value f; measure: N value g; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

### Admissible model

For every fixed upper-level point $x$, $g(x,\cdot)$ is $\mu$-strongly convex on all of $\mathbb{R}^{d_y}$. Convexity in $x$ or joint convexity in $(x,y)$ is not required.

The population full gradient $\nabla f=(\nabla_x f,\nabla_y f)$ is globally $L$-Lipschitz in $(x,y)$. Convexity of $f$ is not required.

The population full gradient $\nabla g=(\nabla_x g,\nabla_y g)$ is globally $L$-Lipschitz in $(x,y)$.

The objective $\Phi$ has a finite lower bound. A point $x_0$ is given and satisfies $\Phi(x_0)-\inf_x\Phi(x)\le\Delta$. Convexity or existence of a global minimizer of $\Phi$ is not required.

The initial point $(x_0,y_0)$ and bound $\|y_0-y^*(x_0)\|\le R_0$ are given. This is an initialization budget, not a requirement that the oracle return $y^*$.

The population function $f$ is jointly $C_f$-Lipschitz in $(x,y)$, not merely in $y$.

The function $g$ is twice differentiable, and its full joint Hessian is $\rho$-Lipschitz. Samplewise conditions and additional promises are as follows.

Every upper-level sample function $F$ is differentiable; its value and full gradient are jointly Lipschitz with sample-uniform budgets. The latent partial gradients $F_x,F_y$ are unbiased for their population counterparts and have uniformly bounded variance. The interface itself returns only function values.

Each lower-level sample function $G$ is twice differentiable, with jointly Lipschitz full gradient and Hessian, and strongly convex in $y$ for every fixed $x$. Sample budgets are uniform. Latent derivatives $G_y,G_{xy},G_{yy}$ are unbiased with bounded variance. The source Assumption 2 does not separately impose bounded variance on $G_x$; no such condition is added here.

Assumption 3 requires $\sup_{x\in\mathbb{R}^{d_x}}\|y^*(x)\|\le B_y<\infty$. Theorem 3 explicitly invokes Assumptions 1-4, so this stronger condition is retained.

Source Assumption 4 requires $\sup_{x,y}\mathbb{E}\|F_y(x,y;\xi)\|^4\le M_4<\infty$.

The initialization potential $V_0^U$ in source Theorem 3 has a public upper bound independent of epsilon. If an algorithm first constructs this initialization, all of its value calls count toward total cost.

### Oracle interface

Public inputs are dimension, target accuracy, the model's budgets, and the initial point. The original functions, their lower-level solutions, and the reduced objective are hidden. Queries are restricted to the stated interfaces; inner optima and undeclared derivatives are not available for free.

$(sample_id,x,y)\longmapsto F(x,y;sample_id)$. Return the exact scalar value of the selected sampled function at the query point. Responses at different points are jointly determined by that sample, rather than corrupted by independent pointwise noise. Finite differences are generally unbiased for a smoothed objective and have controlled bias for the original objective.

$(sample_id,x,y)\longmapsto G(x,y;sample_id)$ Return the exact scalar value of the selected sampled function at the point. This is not independent additive noise at each point: a shared sample determines all joint responses. Gradient differences are generally unbiased for a smoothed objective and have controlled bias for the original objective.

After drawing an i.i.d. sample identifier, the algorithm may reuse it at the points required by the finite-difference template. The same G sample and Gaussian direction also couple the differences at y and z. Fresh samples and internal Gaussian directions are independently drawn as prescribed by the source algorithm.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2^2$. The tolerance $\varepsilon$ is always expressed on the gradient-norm scale. The mean-square requirement is equivalent to the RMS gradient being at most this tolerance.

In this unconstrained model with a strongly convex lower level, $\nabla\Phi(x)=\nabla_x f(x,y^*)-g_{xy}(x,y^*)g_{yy}(x,y^*)^{-1}\nabla_y f(x,y^*)$, where $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$, and $y^*$ denotes $y^*(x)$. The identity defines the hypergradient without granting additional query access.

### Resource accounting

Each scalar evaluation of one selected sample function at one selected point costs one call. Reusing a sample across points is charged separately at every point. Total cost sums all sample and stencil evaluations at both levels.

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

$L$: Common joint-variable Lipschitz upper bound for the complete gradients at both levels **Domain:** $L\ge\mu>0$.

$C_f$: Lipschitz upper bound for the population upper function over all joint variables. **Domain:** $C_f\ge0$.

$\|\nabla f(x,y)\|\le C_f$

$\mu$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu>0$.

$\rho$: A Lipschitz bound on the complete joint Hessian of the lower-level objective. **Domain:** $\rho\ge0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_0$: Public initial lower-level distance bound **Domain:** $R_0\ge0$.

$\|y_0-y^*(x_0)\|\le R_0$

$V_0^U$: Public upper bound on the zeroth-order method's initial Lyapunov gap, using the source theorem's potential. **Domain:** Finite and nonnegative; fixed as accuracy varies.

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$F,G$: Upper- and lower-level stochastic sample functions

$f(x,y)=\mathbb E_\xi F(x,y;\xi),\quad g(x,y)=\mathbb E_\zeta G(x,y;\zeta)$

$\xi,\zeta,\mathcal H$: The upper-level seed, lower-level seed, and pre-sampling history.

$B_y$: A uniform norm bound on lower-level solutions over all outer points. **Domain:** $B_y<\infty$.

$\sup_x\|y^*(x)\|\le B_y$

$M_4$: A uniform fourth-moment bound on the latent upper sample’s lower-variable gradient block. **Domain:** $M_4<\infty$.

$\sup_{x,y}\mathbb E\|F_y(x,y;\xi)\|^4\le M_4$

$L_{0,F},L_{1,F},L_{1,G},L_{2,G},\mu_G$: Budgets comprise the Lipschitz constants of sample F values and gradients, the Lipschitz constants of sample G gradients and Hessians, and the strong-convexity modulus of each lower-level sample. **Domain:** All budgets are fixed and finite, and $\mu_G>0$.

$\sigma_{Fx}^2,\sigma_{Fy}^2,\sigma_{Gy}^2,\sigma_{Gxy}^2,\sigma_{Gyy}^2$: Second-moment bounds on latent sampled derivative errors. The interface itself permits values only. **Domain:** Every budget is fixed, finite, and nonnegative.

$F_x,F_y,G_y,G_{xy},G_{yy}$: Potential sample partial derivatives and Hessian blocks used to define regularity and moment conditions.

$\mathrm{id}$: Identifier of a drawn sample, reusable at the multiple query points permitted by the interface

$N_{f,\rm val}$: The number of upper-level scalar-value responses. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_{g,\rm val}$: Number of lower-level scalar-value responses **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O,\omega}C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \mathbb E\|\nabla\Phi_I(\hat x_{\mathcal A})\|^2\le\varepsilon^2\}.\\C=N_{f^0}+N_{g^0}.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - Penalty-function regime with function-value access

**Region.** The quantity $\eta=\varepsilon^2$ is sufficiently small. Per-sample regularity, fourth moments, and public initialization-potential budgets satisfy MODEL. Values of each retained sample are returned exactly, with each evaluation point charged separately.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O((d_x+d_y) \varepsilon ^{-4})
$$

**Gap or comparison.** No value-oracle lower bound under the same specification has been verified that matches both dimension and accuracy.

**Comparison argument.** Each included claim has verified statement and applicability; mathematics review is separately labeled. No numerical threshold inferred from asymptotics.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** A simplified query rate requires a uniform bound on initial potential. Charge the calls actually used to obtain that initialization.

**Dimension conditions.** Track the supplied dimensions $d_x,d_y$ separately; the formula retains the linear factor $d_x+d_y$ explicitly.

**Oracle mapping.** The oracle returns only sampled scalar function values. A sample identifier may be reused at the points specified by the finite-difference template, with every actual scalar evaluation charged separately. This differs from independent additive noise at each point.

**Guarantee mapping.** The native target is $\mathbb E\|\nabla\Phi(\widehat x)\|^2\le\varepsilon^2$, a root-mean-square tolerance, rather than $\mathbb E\|\nabla\Phi(\widehat x)\|\le\varepsilon^2$. If the source denotes squared-gradient tolerance by $\eta$, the exact substitution is $\eta=\varepsilon^2$.

**Output mapping.** Return one outer point $\widehat x$. Expectation uses the oracle and algorithm randomness stated in the contract.

**Resource mapping.** Charged resources are $N_{f,\mathrm{val}}$ and $N_{g,\mathrm{val}}$. Cost uses a fixed worst-case budget on each execution, rather than expected call count.

### B1 - Algorithm3 zeroth-order penalty double loop

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{O}\!\left((d_x+d_y)\varepsilon^{-4}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2510.03646v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N value f+N value g.**

$$
O((d_x+d_y)\varepsilon ^{-4})
$$

**N grad f.** 0

**N grad g.** 0

**N HVP.** 0

**N JVP.** 0

**N inner solve.** 0

**Constants.** Regularity, noise, and initial potential $V_0^U$ are fixed. Each finite-difference stencil contains a constant number of actual function-value evaluations.

**Derivation.** Substitute squared-gradient tolerance $\eta=\varepsilon^2$. There are $O(\eta^{-1})$ outer steps, upper-level batch size $O(d_x/\eta)$ per step, and inner iteration length $O(d_y/\eta)$. Every function evaluation is charged under the stated interface.

**Source location.** [1](https://arxiv.org/pdf/2510.03646v1) theorem: Theorem 3; Algorithm 3; section: 1.1,3; pdf pages: 4; 15; 21; 22; equations: (3.39); (3.40)

The theorem explicitly depends on the initial potential $V_0^U$. A simplified rate needs a uniform potential bound or must charge the initialization achieving it. The paper does not supply a matching lower bound for the same value interface.

## References

[1] Alireza Aghasi; Jeongyeol Kwon; Saeed Ghadimi. Optimal Zeroth-Order Bilevel Optimization. 2025. arXiv:2510.03646v1, 2025-10-04.

https://arxiv.org/pdf/2510.03646v1
