# Nonconvex-concave problems: probability guarantee with an initial-distance bound

**Setting ID.** `CV_S_NCC_PROB_UPPER`

Minimax optimization

Solve $\min_{x\in X}\Phi(x)$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

**Status.** Bounds missing

**TASK tags.** formulation: Nonconvex concave minimize value; solution concept: Moreau envelope gradient; task family: Minimax

**MODEL tags.** convexity: Concavity in the declared block; convexity: No convexity promise in block; convexity: Nonconvex concave; geometry: Dual diameter; initialization: Extra inner distance; initialization: Initial regularized distance; initialization: Value initial gap; smoothness: Lipschitz gradient

**ORACLE tags.** feedback quality: Exact; interface family: Value joint gradient; operation: Payoff value joint gradient; operation: Projection; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal point; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Moreau envelope gradient

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N bundle; measure: N projection; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in X}\Phi(x)$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

### Admissible model

The set $X$ is known, nonempty, closed, and convex. The set $Y$ is known, nonempty, compact, and convex, with $\operatorname{diam}(Y)\le D_y$. This setting uses $X=\mathbb{R}^{d_x}$.

The function $f$ is jointly $\beta$-smooth on $X\times Y$. For every $x$, $f(x,\cdot)$ is concave. Convexity in the $x$ direction and a positive strong-concavity modulus are not required.

The public feasible initial point $(x_0,y_0)$ satisfies $\Phi(x_0)-\inf_{x\in X}\Phi(x)\le\Delta<\infty$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

Define $x_{\rm aux}=\arg\min_{u\in\mathbb R^{d_x}}\{f(u,y_0)+\beta\|u-x_0\|_2^2\}$. The subproblem is strongly convex and has a unique minimizer. The public bound $\|x_0-x_{\rm aux}\|_2\le\widetilde D_x$ is a separate initialization promise, independent of the primal gap.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $\Delta$, $\widetilde{D}_x$, $D_y$, $\beta$, and $\varepsilon$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
(x,y)\longmapsto(f(x,y),\nabla_xf(x,y),\nabla_yf(x,y))
$$

Queries satisfy $(x,y)\in X\times Y$. The exact value and both gradient blocks form one bundled response.

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

### Output

Return one primal point $\widehat x\in X$. No dual point is required.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

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

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\|\nabla\phi_{1/(2\beta)}(\widehat{x})\|_2\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$\widetilde{D}_x$: A public bound on distance from the initial point to the unique auxiliary minimizer $x_{\rm aux}$. **Domain:** A nonnegative real.

$\|x_0-x_{\rm aux}\|_2\le\widetilde D_x,\quad x_{\rm aux}=\arg\min_u\{f(u,y_0)+\beta\|u-x_0\|_2^2\}$

$D_y$: Euclidean diameter bound for the dual feasible domain **Domain:** Positive real number.

$\operatorname{diam}(Y)=\sup_{u,v\in Y}\|u-v\|_2\le D_y$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: The Euclidean-norm tolerance for the reduced objective’s Moreau-envelope gradient. **Domain:** Positive real number.

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

$X=\mathbb R^{d_x}$

$x_0,y_0$: The public initial primal and dual variables. **Domain:** The respective feasible domains. Both equal zero when the origins are explicitly fixed.

$\widehat x$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** A feasible primal point in $\mathbb R^{d_x}$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm first}$: Number of bundled function-value and full joint-gradient queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Number of exact Euclidean projections onto the known feasible domain, recorded separately from primary information queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\log,\ln,\log_+$: Natural logarithm and its nonnegative truncation **Domain:** Arguments of log and ln are positive; the argument of $\log_+$ may be zero.

$\log_+(t)=\log(\max\{1,t\})$

$c_1$: A small universal constant in the source accuracy window, with no numerical value specified. **Domain:** Fixed positive constant in the source theorem; its numerical value is unspecified and it is not a new instance parameter.

$\phi,\iota_X$: Reduced objective with primal feasibility constraints and the set indicator function. **Domain:** An extended-real-valued function.

$\phi=\Phi+\iota_X,\quad\iota_X(x)=0\ (x\in X),\ +\infty\ (x\notin X)$

$\phi_{1/(2\beta)}$: The Moreau envelope of the constrained reduced objective; error measures its true gradient. **Domain:** A differentiable real-valued function on $\mathbb R^{d_x}$.

$\phi_{1/(2\beta)}(c)=\min_u\{\phi(u)+\beta\|u-c\|_2^2\}$

$x_{\rm aux}$: Unique minimizer of the first regularized primal subproblem **Domain:** $\mathbb R^{d_x}$.

$x_{\rm aux}=\arg\min_u\{f(u,y_0)+\beta\|u-x_0\|_2^2\}$

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

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(\beta^2D_y\Delta\varepsilon^{-3}\log^2(\beta(\widetilde{D}_x^2+D_y^2)/\varepsilon))
$$

**Comparison argument.** No applicable unrestricted probability lower audited here.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Retain the source full-space primal domain and additional initial-distance bound. The guarantee still has fixed success probability.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - dual regularization plus Minimax-PPA

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** Line 7 of Lin–Jin–Jordan Algorithm 5 samples the output index uniformly from the outer history. This upper-bound witness is randomized despite using exact gradients.

$$
O(\beta^2D_y\Delta\varepsilon^{-3}\log^2(\beta(\widetilde{D}_x^2+D_y^2)/\varepsilon))
$$

**Sources.** [1](https://arxiv.org/pdf/2002.02417v6)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
O(\beta^2D_y\Delta\varepsilon^{-3}\log^2(\beta(\widetilde D_x^2+D_y^2)/\varepsilon))
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** The display retains the source squared logarithm. Boundary extensions use a positive saturated logarithm and retain a term accounting for at least one iteration.

**Source location.** [1](https://arxiv.org/pdf/2002.02417v6) theorem: CorollaryA.8; section: AppendixA; pdf pages: 22

Map source smoothness, dual diameter, and initial primal gap to $\beta,D_y,\Delta$, retaining initialization scale $\widetilde D_x$. The source randomized output gives success probability at least $2/3$. The algorithm does not use the exact value included in the oracle bundle.

## References

[1] Tianyi Lin; Chi Jin; Michael I. Jordan. Near-Optimal Algorithms for Minimax Optimization. 2021. arXiv:2002.02417v6, 2021-07-26.

https://arxiv.org/pdf/2002.02417v6
