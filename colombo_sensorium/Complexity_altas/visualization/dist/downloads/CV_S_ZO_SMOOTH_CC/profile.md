# Smooth convex-concave saddle-point problems: exact scalar values on the full space

**Setting ID.** `CV_S_ZO_SMOOTH_CC`

Minimax optimization

$$
\min_{x\in R_xB_2^{d_x}}\max_{y\in R_yB_2^{d_y}}f(x,y).
$$

**Status.** Bounds missing

**TASK tags.** task family: Minimax

**MODEL tags.** convexity: Convex concave; geometry: Compact geometry; geometry: Two balls

**ORACLE tags.** feedback quality: Exact; interface family: Exact payoff value; operation: Payoff value; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Saddle-point gap

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N value; setup: Initialization included

## 1. Setting specification

### Task

$$
\min_{x\in R_xB_2^{d_x}}\max_{y\in R_yB_2^{d_y}}f(x,y).
$$

### Admissible model

The function $f:\mathbb{R}^{d_x+d_y}\to\mathbb{R}$ is continuously differentiable, convex on $x$, and concave on $y$, with globally $\beta$-Lipschitz joint gradient. Bilinearity and a separate gradient-norm bound are not assumed.

The ball radius $R_x,R_y>0$ and dimension are public. Compact convex output domains ensure a saddle point and finite global gap.

### Oracle interface

Public inputs comprise the block dimensions $d_x,d_y$ and parameters $R_x$, $R_y$, $\beta$, and $\varepsilon$, together with the stated initial point and feasible-set information. Analytic descriptions of hidden functions, operators, and matrices are not supplied.

$$
z\in\mathbb{R}^{d_x+d_y}\longmapsto f(z)\in\mathbb{R}.
$$

Scalar values are exact and noiseless. Queries may lie outside the output ball, with arbitrarily small separations and no charge for real precision. Projection onto the known ball is internal computation.

### Output

Return $(\widehat{x},\widehat{y})\in R_xB_2^{d_x}\times R_yB_2^{d_y}$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\operatorname{Gap}(\widehat{x},\widehat{y})=\max_{v\in R_yB_2^{d_y}}f(\widehat{x},v)-\min_{u\in R_xB_2^{d_x}}f(u,\widehat{y}).
$$

### Resource accounting

Each scalar evaluation costs one $N_{\rm value}$ call. Several evaluation points in an iteration cannot be bundled into one call.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\operatorname{Gap}(\widehat{x},\widehat{y})\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$R_x$: Radius of the primal Euclidean ball **Domain:** Positive real number.

$X=R_xB_2^{d_x}$

$R_y$: The Euclidean-ball radius for the dual variable. **Domain:** Positive real number.

$Y=R_yB_2^{d_y}$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d_x$: Primal-space dimension **Domain:** Positive integer.

$d_y$: The dimension of the dual-variable space. **Domain:** Positive integer.

$\varepsilon$: Target tolerance for the complete weak-VI gap or global saddle gap, in the units of that gap. **Domain:** Positive real number.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\widehat x,\widehat y$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** Feasible variable pairs in $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm value}$: The number of exact scalar-value calls. **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$B_2^k$: Closed k-dimensional Euclidean unit ball **Domain:** $k\ge1$.

$B_2^k=\{u\in\mathbb R^k:\|u\|_2\le1\}$

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

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []
