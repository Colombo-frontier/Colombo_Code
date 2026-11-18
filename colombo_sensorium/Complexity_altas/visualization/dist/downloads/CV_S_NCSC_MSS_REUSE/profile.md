# Nonconvex–strongly concave optimization with reusable samples and mean-square smoothness.

**Setting ID.** `CV_S_NCSC_MSS_REUSE`

Minimax optimization

Solve $\min_x\Phi(x)$, where $\Phi(x)=\max_y f(x,y)$ and $f=\mathbb E_\xi f_\xi$.

**Status.** Bounds missing

**TASK tags.** task family: Minimax

**MODEL tags.** convexity: Nonconvex strongly concave; convexity: Strong concavity; initialization: Initialization; smoothness: Sample mean square

**ORACLE tags.** feedback quality: Exact; feedback quality: Stochastic unbiased bounded variance; interface family: Reusable sample gradient; operation: Sample draw; operation: Sample gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N independent sample; measure: N sample gradient; setup: Initialization included

## 1. Setting specification

### Task

Solve $\min_x\Phi(x)$, where $\Phi(x)=\max_y f(x,y)$ and $f=\mathbb E_\xi f_\xi$.

### Admissible model

$f:\mathbb{R}^{d_x}\times\mathbb{R}^{d_y}\to\mathbb{R}$, with both blocks unconstrained and Euclidean norms throughout. The joint gradient satisfies $\|\nabla f(z)-\nabla f(w)\|_2\le \beta\|z-w\|_2$.

For every $x$, $f(x,\cdot)$ is uniformly $\mu_y$-strongly concave. Thus $y^\star(x)=\arg\max_y f(x,y)$ is unique and $\Phi(x)=f(x,y^\star(x))$ is differentiable. Neither $f(\cdot,y)$ nor $\Phi$ is assumed convex.

Assume $\inf_x\Phi(x)>-\infty$, with an initial point satisfying $\Phi(x_0)-\inf_x\Phi(x)\le\Delta$.

The initial point additionally satisfies $\|\nabla_yf(x_0,y_0)\|_2\le G_0$. Every sample function is differentiable. For any fixed points $z,w$:

$$
\mathbb{E}\nabla f_\xi(z)=\nabla f(z),\qquad\mathbb{E}\|\nabla f_\xi(z)-\nabla f(z)\|_2^2\le\sigma^2,
$$

$$
\mathbb{E}\|\nabla f_\xi(z)-\nabla f_\xi(w)\|_2^2\le\beta_{\rm ms}^2\|z-w\|_2^2.
$$

### Oracle interface

Public inputs include the block dimensions $d_x,d_y$ and $\Delta$, $G_0$, $\beta$, $\beta_{\rm ms}$, $\varepsilon$, $\mu_y$, and $\sigma$. The stated initial points and feasible-set information are also supplied. An analytic representation of the hidden function, operator, or matrix is not revealed.

Sample identifiers $\xi$ are drawn independently from an unknown distribution fixed before interaction. Identifiers may be stored and used to evaluate $\nabla f_\xi$ at several points in the full space. Every sample–point evaluation is charged.

A paired-sample difference at two points requires two evaluations. Values and Hessians are unavailable. Adaptive points chosen after obtaining a reusable sample identifier need not be unbiased conditional on the entire history; fixed-point unbiasedness and persistent sample coupling retain their model definitions.

### Output

Return $\widehat x\in\mathbb R^{d_x}$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|\nabla\Phi(\widehat{x})\|_2
$$

### Resource accounting

The primary cost is $N_{\rm sample\text{-}gradient}$, with independent sample count recorded separately. Reusing one sample identity at several points does not turn those evaluations into one gradient call.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\left(\|\nabla\Phi(\widehat{x})\|_2\right)^2\right]\le\varepsilon^2.
$$

Expectation is over private algorithmic randomness and the random samples actually used.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$G_0$: Euclidean norm bound on the dual gradient at the public initial point **Domain:** A nonnegative real.

$\|\nabla_yf(x_0,y_0)\|_2\le G_0$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$\beta_{\rm ms}$: Mean-square Lipschitz upper bound for a same-sample gradient difference between two points. **Domain:** Positive real number.

$d_x$: Primal-space dimension **Domain:** Positive integer.

$d_y$: The dimension of the dual-variable space. **Domain:** Positive integer.

$\varepsilon$: Euclidean norm tolerance for the true reduced gradient; the mean-square contract targets its square $\varepsilon^2$. **Domain:** Positive real number.

$\kappa$: Ratio of the population smoothness upper bound, or mean-square average smoothness for finite sums, to the dual strong-concavity lower bound **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu_y$

$\mu_y$: A uniform strong-convexity lower bound for −f(x,·) at every fixed x; equivalently, the dual strong-concavity modulus of f. **Domain:** $0<\mu_y\le\beta$.

$f(x,v)\le f(x,y)+\langle\nabla_yf(x,y),v-y\rangle-\frac{\mu_y}{2}\|v-y\|_2^2$

$\sigma$: Standard-deviation upper bound for noise in the full stochastic response, controlling the joint squared norm rather than summing independent block budgets. **Domain:** A nonnegative real.

$\mathbb E_\xi\|\nabla f_\xi(z)-\nabla f(z)\|_2^2\le\sigma^2\quad\text{for every fixed }z$.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$\Phi$: Reduced objective after global dual maximization; neither its value nor gradient is an additional free interface **Domain:** Real-valued function on the primal-variable space.

$\Phi(x)=\max_{y\in \mathbb R^{d_y}}f(x,y)$

$y^\star(x)$: The unique global dual maximizer at fixed primal x. **Domain:** $y^\star(x)\in\mathbb R^{d_y}$.

$y^\star(x)=\arg\max_{y\in\mathbb R^{d_y}}f(x,y)$

$x_0,y_0$: The public initial primal and dual variables. **Domain:** The respective feasible domains. Both equal zero when the origins are explicitly fixed.

$\widehat x$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** A feasible primal point in $\mathbb R^{d_x}$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$\xi,f_\xi$: A retained sample identifier and its fixed differentiable sample function, drawn independently at creation. **Domain:** $f_\xi:\mathbb R^{d_x+d_y}\to\mathbb R$.

$f(z)=\mathbb E_\xi f_\xi(z)$

$N_{\rm independent}$: Number of independent sample identifiers drawn **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm sample\text{-}gradient}$: Gradient evaluations of one sample identifier at one point. **Domain:** Nonnegative integer count; expected work is its expectation.

$\mathcal A,I$: An algorithm selected from public inputs, a hidden admissible object fixed before interaction, and an oracle law satisfying the declared conditional means, variances, and independence protocol. **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$B_{\rm independent},B_{\rm sample\text{-}gradient}$: One algorithm simultaneously satisfies the separate caps on independent sample draws and sample-gradient evaluations. **Domain:** A pair of nonnegative integers. Sample identifiers may be stored persistently and reused.

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

## 4. Bounds and supporting evidence
