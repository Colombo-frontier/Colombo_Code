# Nonconvex-concave minimax optimization: randomized zero-respecting algorithms and Moreau stationarity

**Setting ID.** `CV_S_NCC_STOCH_LOWER`

Minimax optimization

Solve $\min_{x\in X}\Phi(x)$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

**Status.** Bounds missing

**TASK tags.** formulation: Nonconvex concave minimize value; solution concept: Moreau envelope gradient; task family: Minimax

**MODEL tags.** convexity: Concavity in the declared block; convexity: No convexity promise in block; convexity: Nonconvex concave; geometry: Bounded dual; geometry: Dual diameter; initialization: Value initial gap; smoothness: Lipschitz gradient

**ORACLE tags.** feedback quality: Exact; feedback quality: Exact value plus gradient variance sigma; interface family: Value fresh gradient; operation: Projection; operation: Stochastic value joint gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Zero respecting

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal point; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Moreau envelope gradient

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N bundle; measure: N projection; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in X}\Phi(x)$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

### Admissible model

The set $X$ is known, nonempty, closed, and convex. The set $Y$ is known, nonempty, compact, and convex, with $\operatorname{diam}(Y)\le D_y$.

The function $f$ is jointly $\beta$-smooth on $X\times Y$. For every $x$, $f(x,\cdot)$ is concave. Convexity in the $x$ direction and a positive strong-concavity modulus are not required.

The public feasible initial point $(x_0,y_0)$ satisfies $\Phi(x_0)-\inf_{x\in X}\Phi(x)\le\Delta<\infty$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $\Delta$, $D_y$, $\beta$, $\varepsilon$, and $\sigma$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
(x,y)\longmapsto(f(x,y),G_x,G_y)
$$

Queries satisfy $(x,y)\in X\times Y$. Function values are exact; gradients use fresh samples.

Let $\mathcal H_t$ denote the full history before query t. Conditional on $\mathcal H_t,z_t$, the response $G_t\in\mathbb R^{d_x+d_y}$ satisfies $\mathbb E[G_t\mid\mathcal H_t,z_t]=\nabla f(z_t)$ and $\mathbb E[\|G_t-\nabla f(z_t)\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$. Each call uses an independent fresh sample.

No reusable sample identifier or cross-point sample reuse is available. No mean-square smoothness of sample gradients or operators is additionally assumed. Blocks within a full vector may be correlated.

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

### Output

Return one primal point $\widehat x\in X$. No dual point is required.

Unqueried outputs are allowed, subject to the stated support rule.

### Loss or accuracy criterion

$$
\|\nabla\phi_{1/(2\beta)}(\widehat{x})\|_2
$$

Let $\phi(x)=\Phi(x)+\iota_X(x)$, where $\iota_X$ equals $0$ on $X$ and $+\infty$ elsewhere; define $\phi_{1/(2\beta)}(c)=\min_u\{\phi(u)+\beta\|u-c\|_2^2\}$. The envelope is differentiable. Its gradient is the evaluation criterion, not a free oracle.

### Resource accounting

Each bundled value-and-joint-gradient call counts once in $N_{\rm first}$. Projection counts are recorded separately.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Randomized adaptive zero-respecting algorithms are allowed. Feasible queries and outputs may use only coordinates previously exposed by the corresponding gradient blocks. Projection may not bypass the support restriction in Definition 2.6 of the source.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\|\nabla\phi_{1/(2\beta)}(\widehat{x})\|_2\right]\le\varepsilon.
$$

Expectation is outside the complete error expression; internal maxima or suprema are not moved outside it.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$D_y$: Euclidean diameter bound for the dual feasible domain **Domain:** Positive real number.

$\operatorname{diam}(Y)=\sup_{u,v\in Y}\|u-v\|_2\le D_y$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: The Euclidean-norm tolerance for the reduced objective’s Moreau-envelope gradient. **Domain:** Positive real number.

$\sigma$: Standard-deviation upper bound for noise in the full stochastic response, controlling the joint squared norm rather than summing independent block budgets. **Domain:** A nonnegative real.

$\mathbb E[\|G_t-\mathbb E[G_t\mid\mathcal H_t,z_t]\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$d_x,d_y$: Positive integer primal and dual block dimensions; joint dimension $d=d_x+d_y$ **Domain:** Positive integer.

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$\Phi$: Reduced objective after global dual maximization; neither its value nor gradient is an additional free interface **Domain:** Real-valued function on the primal-variable space.

$\Phi(x)=\max_{y\in Y}f(x,y)$

$X,Y$: The primal domain is known, nonempty, closed, and convex; the dual domain is known, nonempty, compact, and convex, with $\operatorname{diam}(Y)\le D_y$. **Domain:** $X\subset\mathbb R^{d_x},\ Y\subset\mathbb R^{d_y}$.

$x_0,y_0$: The public initial primal and dual variables. **Domain:** The respective feasible domains. Both equal zero when the origins are explicitly fixed.

$\widehat x$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** A feasible primal point in $\mathbb R^{d_x}$.

$G_f(z;\xi),G_t$: Random sample of the full joint gradient and the response from sample $t$ **Domain:** $\mathbb R^{d_x+d_y}$. The two blocks may be internally correlated.

$G_f=(G_x,G_y)$

$G_x,G_y$: The primal and dual blocks in one complete joint-gradient sample. **Domain:** $G_x\in\mathbb R^{d_x},\ G_y\in\mathbb R^{d_y}$.

$\xi,\mathcal H_t,z_t$: Current fresh-sample seed, complete pre-query history, and query point. **Domain:** The seed space, history-generated $\sigma$-algebra, and declared query domain.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm first}$: Bundled calls returning an exact function value and a fresh joint-gradient sample. **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Number of exact Euclidean projections onto the known feasible domain, recorded separately from primary information queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs, a hidden admissible object fixed before interaction, and an oracle law satisfying the declared conditional means, variances, and independence protocol. **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$c_1$: A small universal constant in the source accuracy window, with no numerical value specified. **Domain:** Fixed positive constant in the source theorem; its numerical value is unspecified and it is not a new instance parameter.

$\phi,\iota_X$: Reduced objective with primal feasibility constraints and the set indicator function. **Domain:** An extended-real-valued function.

$\phi=\Phi+\iota_X,\quad\iota_X(x)=0\ (x\in X),\ +\infty\ (x\notin X)$

$\phi_{1/(2\beta)}$: The Moreau envelope of the constrained reduced objective; error measures its true gradient. **Domain:** A differentiable real-valued function on $\mathbb R^{d_x}$.

$\phi_{1/(2\beta)}(c)=\min_u\{\phi(u)+\beta\|u-c\|_2^2\}$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm first}(\mathcal A,I,\omega)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - The source theorem’s applicability window.

**Region.** $0<\varepsilon\le c_1\min\{\sqrt{\beta\Delta},\beta D_y\}$

**Quantity.** Q1

**Resource.** Number of joint responses explicitly allowed by this profile

**Status.** Upper bound missing

**Lower bound.** B1

$$
\Omega(\beta^2D_y\Delta\varepsilon^{-3}+\beta^3D_y^2\Delta\sigma^2\varepsilon^{-6})
$$

**Upper bound.** No admitted bound for this comparison

**Comparison argument.** The retained upper belongs to a different algorithm/guarantee/initialization specification.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - deterministic dual lattice plus masked stochastic chain

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** The stated restricted randomized class

**Algorithm-scope qualification.** The lower bound covers randomized methods satisfying the zero-respecting condition on every path. It does not extend to arbitrary randomized queries.

$$
\Omega(\beta^2D_y\Delta\varepsilon^{-3}+\beta^3D_y^2\Delta\sigma^2\varepsilon^{-6})
$$

**Sources.** [1](https://arxiv.org/pdf/2609.14233v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega(\beta^2D_y\Delta\varepsilon^{-3}+\beta^3D_y^2\Delta\sigma^2\varepsilon^{-6})
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2609.14233v1) theorem: Theorem5.5; section: Section5; pdf pages: 20

The support condition in source Definition 2.6 holds on every random execution path, including the output. Its randomized zero-respecting lower bound does not extend automatically to arbitrary randomized algorithms.

## References

[1] Qilong Wu; Zhihao Gu; Junchi Yang. Lower Bounds for Nonconvex-Concave Minimax Optimization. 2026. arXiv:2609.14233v1, 2026-09-13.

https://arxiv.org/pdf/2609.14233v1
