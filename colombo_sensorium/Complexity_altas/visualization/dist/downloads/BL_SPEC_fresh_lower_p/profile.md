# Higher-order smoothness only at the lower level: joint gradients and a mean-square target

**Setting ID.** `BL_SPEC_fresh_lower_p`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Fully optimal

**TASK tags.** formulation: Bilevel unique reduced; task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Normalized initial distance; initialization: Normalized initial gap; smoothness: Bounded partial gradient; smoothness: Fixed order smoothness; smoothness: Hessian or cross derivative lipschitz; smoothness: Higher lower variable derivatives; smoothness: Lipschitz gradient; structure: Normalized common budgets

**ORACLE tags.** feedback quality: Fresh; interface family: Fresh gradient; operation: Joint primitive gradient response; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N joint sample; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

### Admissible model

For every fixed upper-level point $x$, $g(x,\cdot)$ is $\mu$-strongly convex on all of $\mathbb{R}^{d_y}$. Convexity in $x$ or joint convexity in $(x,y)$ is not required.

The population full gradient $\nabla f=(\nabla_x f,\nabla_y f)$ is globally $L$-Lipschitz in $(x,y)$. Convexity of $f$ is not required.

The population full gradient $\nabla g=(\nabla_x g,\nabla_y g)$ is globally $L$-Lipschitz in $(x,y)$.

For every $(x,y)$, $\|\nabla_y f(x,y)\|\le C_f$. Equivalently, for fixed $x$ the function $f(x,\cdot)$ is $C_f$-Lipschitz. This does not assert that $f$ is globally Lipschitz in value with respect to $x$.

The derivatives $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$ exist and are each $\rho$-Lipschitz jointly in $(x,y)$. No Lipschitz budget for $g_{xx}$ is assumed.

For every $\ell\in\{x,y\}$, $D_y^p\nabla_\ell g$ exists and is $L_p$-Lipschitz in $y$ for all $x$. No additional intermediate-order bounds or high-order assumptions on $f$ are imposed. The case $p=1$ follows from the basic Hessian-block budgets.

Initialization is $x_0=0$ with $\Phi(0)-\inf\Phi\le1$. Use the source normalized lower-bound class $\mathcal{P}_p(M)$, with budgets stated below. Thus $\Delta$ is not an independently varying parameter.

Choose $y_0=0$ and $\|y^*(0)\|\le1$. Initialize the algorithm's adjoint variable at zero; no free linear-system solution is required.

The source requires $\max\{\ell_f,\ell_g,\rho_1,L_p,B_f,\sigma,\mu^{-1}\}\le M$. Here $\ell_f,\ell_g$ bounds both levels' gradient Lipschitz constants, $B_f$ bounds the lower-variable block of the upper-level gradient, and $\rho_1$ bounds the relevant lower-level Hessian blocks. Use the public bound $L$ for $\ell_f,\ell_g$ and write $C_f=B_f$ and $\rho=\rho_1$. These budgets and $L_p$ are all at most $M$.

### Oracle interface

Public inputs are dimension, target accuracy, the model's budgets, and the initial point. The original functions, their lower-level solutions, and the reduced objective are hidden. Queries are restricted to the stated interfaces; inner optima and undeclared derivatives are not available for free.

$(x,y)\longmapsto (G_{f,x},G_{f,y},G_{g,x},G_{g,y})$. Conditional on the pre-query history, each block has the corresponding population partial gradient as its mean. The sum of the four conditional mean-square errors is at most $\sigma^2\le M^2$.

The four blocks within a response may be arbitrarily correlated. Distinct calls use fresh randomness and are conditionally independent given the common history and query. Samples cannot be retained for cross-point reuse.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2^2$. The tolerance $\varepsilon$ is always expressed on the gradient-norm scale. The mean-square requirement is equivalent to the RMS gradient being at most this tolerance.

In this unconstrained model with a strongly convex lower level, $\nabla\Phi(x)=\nabla_x f(x,y^*)-g_{xy}(x,y^*)g_{yy}(x,y^*)^{-1}\nabla_y f(x,y^*)$, where $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$, and $y^*$ denotes $y^*(x)$. The identity defines the hypergradient without granting additional query access.

### Resource accounting

Compare $Q=N_{\rm joint}$. A joint response containing the four gradient estimates $(f_x,f_y,g_x,g_y)$ at one point costs one call; a batch of size $m$ costs $m$ calls.

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

$C_f$: A uniform norm bound on the population upper function’s lower-variable gradient block. **Domain:** $C_f\ge0$.

$\|\nabla_yf(x,y)\|\le C_f$

$\mu$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu>0$.

$\rho$: Common joint Lipschitz upper bound for the lower function's cross-Hessian block and lower-variable Hessian block **Domain:** $\rho\ge0$.

$\Delta$: Normalized budget on the initial reduced-objective gap **Domain:** $\Delta=1$.

$R_0$: The normalized initial lower-level distance budget. **Domain:** $R_0=1$.

$p$: Order of the specified lower-direction regularity; it does not increase the oracle's derivative order **Domain:** Positive integer.

$L_p$: Lipschitz upper bound, in the lower-level variable, for the pth lower-direction derivative of the complete lower-level gradient **Domain:** $L_p\ge0$.

$M$: The total budget of the normalized instance class. **Domain:** $M>0$.

$\max\{L,\rho,L_p,C_f,\sigma,\mu^{-1}\}\le M$

$\sigma$: Conditional standard-deviation upper bound for a stochastic full gradient; ORACLE specifies which gradient is constrained **Domain:** $\sigma\ge0$.

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$\mathrm D_y^q$: The qth Fréchet derivative in the lower-level variable. **Domain:** Fix $x$ and use the induced multilinear operator norm.

$q,j,r$: Derivative order, derivative-budget index, and effective order selected by the algorithm. **Domain:** The range is specified by the model or the subscript of the bound.

$G_f,G_g,\mathcal H$: Upper- and lower-level stochastic full-gradient responses and the pre-draw history. **Domain:** $G_f,G_g\in\mathbb R^{d_x+d_y}$.

$G_{f,x},G_{f,y},G_{g,x},G_{g,y}$: Outer and lower blocks of the corresponding full stochastic gradient **Domain:** Outer-block dimension d_x and lower-block dimension d_y.

$\ell_f,\ell_g,\rho_1,B_f$: Source budgets for upper-level smoothness, lower-level smoothness, Hessian-block variation, and the lower-variable block of the upper gradient.

$\ell_f,\ell_g\le L,\ \rho_1=\rho,\ B_f=C_f$

$\mathcal P_p(M)$: Normalized instance class whose total model budget is at most $M$

$K,m,\tau,\Delta_0$: Outer iteration count, batch size, perturbation scale, and initial potential difference in this upper-bound derivation **Domain:** Used only in the stated derivation; here $\tau$ is the algorithm's perturbation scale.

$N_{\rm joint}$: The number of joint full-gradient sample responses for both levels. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O,\omega}C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \mathbb E\|\nabla\Phi_I(\hat x_{\mathcal A})\|^2\le\varepsilon^2\}.\\C=N_{\mathrm{joint}}.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - The normalized instance class at fixed order.

**Region.** The order $p$ is fixed and finite. Assume normalized public budget $M\ge M_0$ and $0<\varepsilon\le\varepsilon_0$. The quantity $M_0$ is the universal source threshold. All baseline and lower-level-only higher-order conditions in the model hold.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega (\varepsilon ^{-4-2/p})
$$

**Upper bound.** B1

$$
O_p(\varepsilon ^{-4-2/p})
$$

**Gap or comparison.** For fixed $p$, the accuracy rate is $\Theta_p(\varepsilon^{-4-2/p})$.

**Comparison argument.** Each included claim has verified statement and applicability; mathematics review is separately labeled. No numerical threshold inferred from asymptotics.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** One fresh joint call returns the four gradient blocks $f,g$ and costs one call. The additional smoothness of order $p$ constrains only the stated lower-level derivative blocks of $g$. The initial function gap and lower-level distance satisfy the normalization $\mathcal P_p(M)$.

**Guarantee mapping.** The native target is $\mathbb E\|\nabla\Phi(\widehat x)\|^2\le\varepsilon^2$, a root-mean-square tolerance, rather than $\mathbb E\|\nabla\Phi(\widehat x)\|\le\varepsilon^2$.

**Output mapping.** Return one outer point $\widehat x$. Expectation uses the oracle and algorithm randomness stated in the contract.

**Resource mapping.** The charged resources are $N_{\rm joint}$. Cost is a fixed worst-case budget for every execution, not expected calls.

### B1 - p-point lower-gradient extrapolation

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{O}_p(\varepsilon^{-4-2/p})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.01843v1)

**Dimension conditions.** Valid in every finite dimension of the declared model. No additional dimension dependence is introduced beyond the formula.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N joint sample.**

$$
(2p+5)mK=O_p(\varepsilon ^{-4-2/p})
$$

**N HVP.** 0

**N JVP.** 0

**N inner solve.** 0

**Constants.** Upper-bound constants may depend on $p$ and the instance-class budgets.

**Derivation.** The source Theorem 3.1 bounds mean-square error by $C(\Delta_0/K+\tau^{2p}+1/(m\tau^2))$. Here $K$ is the outer iteration count, $m$ the batch size, $\tau$ the perturbation scale, and $\Delta_0$ the initial potential gap. Choose $\tau\asymp\varepsilon^{1/p}$, $m\asymp\varepsilon^{-2}\tau^{-2}$, and $K\asymp\Delta_0\varepsilon^{-2}$ so that each term has the target squared-error order.

**Source location.** [1](https://arxiv.org/pdf/2610.01843v1) theorem: Theorem 3.1; section: 2–3; pdf pages: 4; 5; 7; equations: (18)

### B2 - unrestricted randomized hard family

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\varepsilon^{-4-2/p})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.01843v1)

**Dimension conditions.** The lower-level dimension may be $d_y=1$, and the hard upper-level dimension is $d_x=O(\varepsilon^{-6-2/p}\log(1/\varepsilon))$. Dimensions may grow with the requested accuracy.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.**

$$
\Omega (\varepsilon ^{-4-2/p})
$$

**Constants.** The lower-bound constant and threshold $M_0$ in Theorem 4.3 are universal; the corresponding upper-bound constant may still depend on $p$.

**Source location.** [1](https://arxiv.org/pdf/2610.01843v1) theorem: Theorem 4.3; section: 4; pdf pages: 11; equations: (29); (30); (31)

## References

[1] Linxuan Pan; Junchi Yang. Optimal Stochastic Bilevel Optimization with First-Order Oracles. 2026. arXiv:2610.01843v1, 2026-10-01.

https://arxiv.org/pdf/2610.01843v1
