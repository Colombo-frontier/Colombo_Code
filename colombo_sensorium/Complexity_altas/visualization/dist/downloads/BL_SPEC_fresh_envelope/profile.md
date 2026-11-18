# Fresh stochastic gradients with derivative budgets uniform in order.

**Setting ID.** `BL_SPEC_fresh_envelope`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Fully optimal

**TASK tags.** formulation: Bilevel unique reduced; task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Initial distance; smoothness: Bounded partial gradient; smoothness: Hessian or cross derivative lipschitz; smoothness: Higher lower variable derivatives; smoothness: Lipschitz gradient; smoothness: Order uniform smoothness; smoothness: Quantitative derivative envelope

**ORACLE tags.** feedback quality: Fresh; interface family: Fresh gradient; operation: Primitive gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N grad f; measure: N grad g; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

### Admissible model

For every fixed upper-level point $x$, $g(x,\cdot)$ is $\mu$-strongly convex on all of $\mathbb{R}^{d_y}$. Convexity in $x$ or joint convexity in $(x,y)$ is not required.

The population full gradient $\nabla f=(\nabla_x f,\nabla_y f)$ is globally $L$-Lipschitz in $(x,y)$. Convexity of $f$ is not required.

The population full gradient $\nabla g=(\nabla_x g,\nabla_y g)$ is globally $L$-Lipschitz in $(x,y)$.

For every $(x,y)$, $\|\nabla_y f(x,y)\|\le C_f$. Equivalently, for fixed $x$ the function $f(x,\cdot)$ is $C_f$-Lipschitz. This does not assert that $f$ is globally Lipschitz in value with respect to $x$.

The derivatives $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$ exist and are each $\rho$-Lipschitz jointly in $(x,y)$. No Lipschitz budget for $g_{xx}$ is assumed.

The objective $\Phi$ has a finite lower bound. A point $x_0$ is given and satisfies $\Phi(x_0)-\inf_x\Phi(x)\le\Delta$. Convexity or existence of a global minimizer of $\Phi$ is not required.

The initial point $(x_0,y_0)$ and bound $\|y_0-y^*(x_0)\|\le R_0$ are given. This is an initialization budget, not a requirement that the oracle return $y^*$.

For every integer $1\le q\le p-1$, $D_y^q\nabla f$ exists and is $L_{q+1}$-Lipschitz in $y$, uniformly in $x$. Arbitrarily high-order x derivatives are not required.

For each integer $1\le q\le p-1$, $D_y^{q+1}\nabla g$ exists and is $L_{q+2}$-Lipschitz in $y$, uniformly over $x$. If $p=1$, this additional derivative list is empty, but the preceding two Hessian-block Lipschitz conditions remain.

Use the uniform budget $L_j=M\Lambda^j(j!)^\beta$ for $j\ge3$, for derivatives of both $f$ and $g$. The constant $M,\Lambda,\beta$ is independent of $p$ and $\varepsilon$, while $L_2=\rho$ is fixed separately. When $p=\infty$, all positive integers $q$ are included.

### Oracle interface

Public inputs are dimension, target accuracy, the model's budgets, and the initial point. The original functions, their lower-level solutions, and the reduced objective are hidden. Queries are restricted to the stated interfaces; inner optima and undeclared derivatives are not available for free.

A query $(x,y)$ returns the full stochastic gradient $G_f=(G_{f,x},G_{f,y})$. Let $\mathcal{H}$ denote the pre-query history. Every history-measurable query satisfies $$
\mathbb{E}[G_f\mid\mathcal{H}]=\nabla f(x,y),\qquad
\mathbb{E}[\|G_f-\nabla f(x,y)\|^2\mid\mathcal{H}]\le\sigma^2.
$$ almost surely, uniformly over the declared query domain.

A query $(x,y)$ returns the full stochastic gradient $G_g=(G_{g,x},G_{g,y})$. Let $\mathcal{H}$ denote the pre-query history. Every history-measurable query satisfies $$
\mathbb{E}[G_g\mid\mathcal{H}]=\nabla g(x,y),\qquad
\mathbb{E}[\|G_g-\nabla g(x,y)\|^2\mid\mathcal{H}]\le\sigma^2.
$$ almost surely, uniformly over the declared query domain.

Each call draws an independent fresh sample, used once at one point. Paired-sample differences across points are unavailable.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2$, with $\varepsilon$ always specified on the gradient-norm scale. Gradient norm and squared gradient norm remain distinct.

In this unconstrained model with a strongly convex lower level, $\nabla\Phi(x)=\nabla_x f(x,y^*)-g_{xy}(x,y^*)g_{yy}(x,y^*)^{-1}\nabla_y f(x,y^*)$, where $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$, and $y^*$ denotes $y^*(x)$. The identity defines the hypergradient without granting additional query access.

### Resource accounting

The compared resource is $Q=N_{\nabla f}+N_{\nabla g}$. A full gradient of either function costs one unit; obtaining both at the same point costs two.

Initialization oracle calls count toward the total. A finite initialization bound is an instance-class assumption, not free access to an inner solver.

The budget is a fixed worst-case cap on every execution path; every actual response within a batch is counted.

Internal processing of available information is free. Comparisons use the explicitly specified scalarization or resource vector. Different resources without given weights cannot be assembled coordinatewise from separate algorithms.

### Algorithm views and success guarantees

Algorithms may use private randomness. Queries, stopping, and postprocessing may be arbitrary measurable functions of the transcript. The output may be unqueried, a random selection of a past point, or an admissible average. No linear-span or zero-respecting restriction is imposed. Queries are sequential; each actual response in a parallel batch is charged separately. Arithmetic, linear algebra, and storage using received data are uncharged. Internal operations, memory, and communication are not tracked by this quantity.

Choose an algorithm from public parameters, then require $\mathbb{E}\|\nabla\Phi(\widehat{x})\|_2\le\varepsilon$ for every admissible instance and legal oracle law. Expectation covers all algorithmic and feedback randomness after fixing the instance.

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

$C_f$: A uniform norm bound on the population upper function’s lower-variable gradient block. **Domain:** $C_f\ge0$.

$\|\nabla_yf(x,y)\|\le C_f$

$\mu$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu>0$.

$\rho$: Common joint Lipschitz upper bound for the lower function's cross-Hessian block and lower-variable Hessian block **Domain:** $\rho\ge0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_0$: Public initial lower-level distance bound **Domain:** $R_0\ge0$.

$\|y_0-y^*(x_0)\|\le R_0$

$p$: Available order of lower-direction regularity **Domain:** Positive integer or infinity; infinity means the envelope holds at every finite order.

$\Lambda$: Exponential scale of the uniform derivative-budget envelope **Domain:** $\Lambda>0$.

$M$: The amplitude of the uniform derivative-budget envelope. **Domain:** $M>0$.

$\beta$: Factorial exponent in the uniform derivative-budget envelope **Domain:** $\beta\ge0$.

$\sigma$: Conditional standard-deviation upper bound for a stochastic full gradient; ORACLE specifies which gradient is constrained **Domain:** $\sigma\ge0$.

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$\mathrm D_y^q$: The qth Fréchet derivative in the lower-level variable. **Domain:** Fix $x$ and use the induced multilinear operator norm.

$q,j,r$: Derivative order, derivative-budget index, and effective order selected by the algorithm. **Domain:** The range is specified by the model or the subscript of the bound.

$G_f,G_g,\mathcal H$: Upper- and lower-level stochastic full-gradient responses and the pre-draw history. **Domain:** $G_f,G_g\in\mathbb R^{d_x+d_y}$.

$G_{f,x},G_{f,y},G_{g,x},G_{g,y}$: Outer and lower blocks of the corresponding full stochastic gradient **Domain:** Outer-block dimension d_x and lower-block dimension d_y.

$L_j$: The derivative Lipschitz budget at order j. **Domain:** $j\ge2$.

$L_2=\rho,\quad L_j=M\Lambda^j(j!)^\beta\ (j\ge3)$

$N_{\nabla f}$: Upper-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_{\nabla g}$: Lower-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O,\omega}C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \mathbb E\|\nabla\Phi_I(\hat x_{\mathcal A})\|\le\varepsilon\}.\\C=N_{\nabla f}+N_{\nabla g}.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - strictly coupled uniform-envelope window

**Region.** Assume $L_1>\mu$, $\Delta,L_0,\sigma>0$, and $0<\varepsilon\le\varepsilon_0$. The common derivative-envelope budget is fixed. The accuracy threshold is independent of $p$, covering finite and infinite orders in that envelope.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega (\varepsilon ^{-4} [inf_{r\in N,1\le r\le p} r^\beta  \varepsilon ^{-1/r}]^2)
$$

**Upper bound.** B1

$$
O(\varepsilon ^{-4} [inf_{r\in N,1\le r\le p} r^\beta  \varepsilon ^{-1/r}]^2)
$$

**Gap or comparison.** The upper and lower bounds match the following expression up to universal constants; finite order and accuracy must be compared jointly: $$
\Theta\!\left(\varepsilon^{-4}\left[\inf_{r\in\mathbb{N},\,1\le r\le p}r^\beta\varepsilon^{-1/r}\right]^2\right).
$$ If $\beta>0$, the transition scale is $p\asymp\log(1/\varepsilon)/\beta$; $p=\infty$ corresponds to $\Theta(\varepsilon^{-4}\log^{2\beta}(1/\varepsilon))$. If $\beta=0$ and arbitrary order is allowed, the result is $\Theta(\varepsilon^{-4})$.

**Comparison argument.** Each included claim has verified statement and applicability; mathematics review is separately labeled. No numerical threshold inferred from asymptotics.

### R2 - zero initial gap

**Region.** Under $\Delta=0$, the supplied initial point already globally minimizes the reduced objective and is therefore stationary.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B3

$$
0
$$

**Gap or comparison.** If the initial function value is globally minimal and the reduced objective is differentiable, its gradient at the initial point is zero. No query is needed.

**Comparison argument.** Each included claim has verified statement and applicability; mathematics review is separately labeled. No numerical threshold inferred from asymptotics.

### R3 - Degenerate model at the maximum-curvature endpoint

**Region.** Assume $L_1=\mu$, $\Delta,\sigma>0$, and sufficiently small $\varepsilon$. Upper-level gradient noise is allowed. Keep this degenerate boundary separate from the coupled regime.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Optimal

**Lower bound.** B5

$$
\Omega (\varepsilon ^{-4})
$$

**Upper bound.** B4

$$
O(\varepsilon ^{-4})
$$

**Gap or comparison.** When upper-level noise is permitted, the accuracy rate is $\Theta(\varepsilon^{-4})$. This lower bound does not apply to the subclass requiring exact upper-level gradients.

**Comparison argument.** Each included claim has verified statement and applicability; mathematics review is separately labeled. No numerical threshold inferred from asymptotics.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Fresh-sample full gradients of f and g are charged separately; the same sample cannot be reused across points. The uniform high-order budget envelope constrains the instance class without adding derivative-query access. At p=1, the Lipschitz assumptions on $g_{xy}$ and $g_{yy}$ already apply.

**Guarantee mapping.** The native objective is $\mathbb E\|\nabla\Phi(\widehat x)\|\le\varepsilon$; an expected norm is not strengthened to a root-mean-square criterion.

### B1 - uniform-order Chebyshev extrapolation

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{O}\!\left(\varepsilon^{-4}\left[\inf_{\substack{r\in\mathbb{N}\\1\le r\le p}}r^\beta\varepsilon^{-1/r}\right]^2\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03638v2)

**Dimension conditions.** Valid in every finite dimension of the declared model. No additional dimension dependence is introduced beyond the formula.

**Output rule.** Return one outer point $\widehat x$. Expectation uses the oracle and algorithm randomness stated in the contract.

**Resource conversion.** Charged resources are $N_{\nabla f}$ and $N_{\nabla g}$. Each execution has a fixed worst-case budget, rather than an expected call budget.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.**

$$
O(\varepsilon ^{-4} [inf_{r\in N,1\le r\le p} r^\beta  \varepsilon ^{-1/r}]^2)
$$

**Constants.** Constants may depend on fixed budgets including $\beta,M,\Lambda$, but not on $p$ or $\varepsilon$.

**Source location.** [1](https://arxiv.org/pdf/2610.03638v2) theorem: Theorem 3.1; Corollary 3.3; section: 2–3; pdf pages: 5; 6; 7; equations: (9); (11); (12)

### B2 - uniform envelope hard family

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\varepsilon^{-4}\left[\inf_{\substack{r\in\mathbb{N}\\1\le r\le p}}r^\beta\varepsilon^{-1/r}\right]^2\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03638v2)

**Dimension conditions.** The lower dimension may be $d_y=1$, while the upper dimension grows as $d_x=O(\varepsilon^{-2}\log(1/\varepsilon))$.

**Output rule.** Return one outer point $\widehat x$. Expectation uses the oracle and algorithm randomness stated in the contract.

**Resource conversion.** Charged resources are $N_{\nabla f}$ and $N_{\nabla g}$. Each execution has a fixed worst-case budget, rather than an expected call budget.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.**

$$
\Omega (\varepsilon ^{-4} [inf_{r\in N,1\le r\le p} r^\beta  \varepsilon ^{-1/r}]^2)
$$

**Constants.** Constants may depend on fixed budgets including $\beta,M,\Lambda$, but not on $p$ or $\varepsilon$.

**Source location.** [1](https://arxiv.org/pdf/2610.03638v2) theorem: Theorem 3.1; Corollary 3.3; section: 2–3; pdf pages: 5; 6; 7; equations: (9); (11); (12)

### B3 - return x0

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03638v2)

**Dimension conditions.** Valid in every finite dimension of the declared model. No additional dimension dependence is introduced beyond the formula.

**Output rule.** When $\Delta=0$, return the public point $x_0$. It already globally minimizes $\Phi$ and has zero gradient, requiring no oracle call.

**Resource conversion.** Every resource coordinate is zero. This conclusion applies only in the cited Delta=0 regime.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad f.** 0

**N grad g.** 0

**N JVP.** 0

**N HVP.** 0

**N inner solve.** 0

**N value f.** 0

**N value g.** 0

**N joint sample.** 0

**N reduced gradient.** 0

**Constants.** Exactly zero calls, with no hidden constant.

**Derivation.** Differentiability and $\Phi(x_0)=\inf_x\Phi(x)$ imply $\nabla\Phi(x_0)=0$. Return the initial point.

**Source location.** [1](https://arxiv.org/pdf/2610.03638v2) theorem: Propositions H.1–H.2; section: Appendix H; pdf pages: 30; 31

A lower bound with noisy upper-level gradients cannot directly apply to a subclass requiring exact upper-level gradients.

### B4 - estimate fixed y* then single-level stochastic optimization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{O}(\varepsilon^{-4})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03638v2)

**Dimension conditions.** Valid in every finite dimension of the declared model. No additional dimension dependence is introduced beyond the formula.

**Output rule.** Return one outer point $\widehat x$. Expectation uses the oracle and algorithm randomness stated in the contract.

**Resource conversion.** Charged resources are $N_{\nabla f}$ and $N_{\nabla g}$. Each execution has a fixed worst-case budget, rather than an expected call budget.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.**

$$
O(\varepsilon ^{-4})
$$

**Constants.** Hold the stated regularity and initialization budgets fixed. Joint optimality is not claimed for parameters whose dependence is untracked.

**Source location.** [1](https://arxiv.org/pdf/2610.03638v2) theorem: Propositions H.1–H.2; section: Appendix H; pdf pages: 30; 31

A lower bound with noisy upper-level gradients cannot directly apply to a subclass requiring exact upper-level gradients.

### B5 - upper-noise single-level hard embedding

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\varepsilon^{-4})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03638v2)

**Conditions.** This region permits upper-gradient noise. Its lower bound does not transfer to another interface requiring exact upper gradients.

**Dimension conditions.** Arbitrary finite dimensions; lower hard family may require dimensions growing with the budget.

**Output rule.** Return one outer point $\widehat x$. Expectation uses the oracle and algorithm randomness stated in the contract.

**Resource conversion.** Charged resources are $N_{\nabla f}$ and $N_{\nabla g}$. Each execution has a fixed worst-case budget, rather than an expected call budget.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.**

$$
\Omega (\varepsilon ^{-4})
$$

**Constants.** Hold the stated regularity and initialization budgets fixed. Joint optimality is not claimed for parameters whose dependence is untracked.

**Source location.** [1](https://arxiv.org/pdf/2610.03638v2) theorem: Propositions H.1–H.2; section: Appendix H; pdf pages: 30; 31

A lower bound with noisy upper-level gradients cannot directly apply to a subclass requiring exact upper-level gradients.

## References

[1] Wendao Wu; Haihan Zhang; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. The Minimax Cost of Smoothness in Fully First-Order Stochastic Bilevel Optimization. 2026. arXiv:2610.03638v2, 2026-10-19.

https://arxiv.org/pdf/2610.03638v2
