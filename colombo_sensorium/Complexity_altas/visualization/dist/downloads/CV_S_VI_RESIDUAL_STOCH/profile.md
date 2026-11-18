# Monotone Lipschitz variational inequalities: stochastic tangential residual

**Setting ID.** `CV_S_VI_RESIDUAL_STOCH`

Variational inequalities

Solve $0\in F(z)+N_K(z)$.

**Status.** Logarithmic gap present; Bounds missing

**TASK tags.** formulation: Stampacchia vi; task family: Variational inequality

**MODEL tags.** geometry: Known closed; initialization: Root localization; monotonicity: Monotone; monotonicity: Monotone lipschitz

**ORACLE tags.** feedback quality: Conditional variance sigma; feedback quality: Exact; interface family: Fresh operator; operation: Projection; operation: Stochastic operator value; operator derivative order: Operator value (order 0); public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Tangential residual

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N projection; measure: N sample; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $0\in F(z)+N_K(z)$.

### Admissible model

The set $K\subset\mathbb R^d$ is public, nonempty, closed, and convex, and may be unbounded. The operator $F$ is monotone and $\beta$-Lipschitz on $K$.

The initial point $z_0\in K$ is public, and a solution $z^\star$ satisfies $\|z_0-z^\star\|_2\le R$. The condition $\operatorname{diam}(K)\le R$ is not required.

### Oracle interface

Public inputs include dimension $d$ and $R$, $\beta$, $\varepsilon$, and $\sigma$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
z\in K\longmapsto G_F(z;\xi)
$$

Let $\mathcal H_t$ denote the full history before query t. Conditional on $\mathcal H_t,z_t$, the response $G_t\in\mathbb R^d$ satisfies $\mathbb E[G_t\mid\mathcal H_t,z_t]=F(z_t)$ and $\mathbb E[\|G_t-F(z_t)\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$. Each call uses an independent fresh sample.

No reusable sample identifier or cross-point sample reuse is available. No mean-square smoothness of sample gradients or operators is additionally assumed. Blocks within a full vector may be correlated.

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

### Output

Return a feasible point $\widehat z\in K$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\operatorname{dist}(0,F(\widehat{z})+N_K(\widehat{z}))
$$

For a closed convex set $K$, define $N_K(z)=\{v:\langle v,u-z\rangle\le0,\ \forall u\in K\}$ for $z\in K$, and $\operatorname{dist}(0,S)=\inf_{v\in S}\|v\|_2$.

The tangent residual is finite at feasible points because $0\in N_K(z)$. This metric is not equal to $\|F(z)\|_2$.

### Resource accounting

Each complete operator sample costs one $N_{\rm sample}$ call. Projection counts are separate.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\left(\operatorname{dist}(0,F(\widehat{z})+N_K(\widehat{z}))\right)^2\right]\le\varepsilon^2.
$$

Expectation is over private algorithmic randomness and the random samples actually used.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$R$: Euclidean distance bound from the public initial point to the same solution promised by the model; not the entire domain diameter **Domain:** Positive real number.

$\|z_0-z^\star\|_2\le R$

$\beta$: Euclidean Lipschitz upper bound for the population operator on the declared query domain **Domain:** Positive real number.

$\|F(z)-F(w)\|_2\le\beta\|z-w\|_2$

$d$: Finite Euclidean dimension of the operator domain; regime quantifiers specify whether complexity is uniform in dimension **Domain:** Positive integer.

$\varepsilon$: This is the tangent-residual tolerance. The mean-square guarantee uses its square $\varepsilon^2$. **Domain:** Positive real number.

$\sigma$: Standard-deviation upper bound for noise in the full stochastic response, controlling the joint squared norm rather than summing independent block budgets. **Domain:** A nonnegative real.

$\mathbb E[\|G_t-\mathbb E[G_t\mid\mathcal H_t,z_t]\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$F$: The unknown operator is single-valued. Monotonicity, strong monotonicity, or weak Minty properties use the specification’s explicit inequalities. **Domain:** A vector map from the declared query domain into $\mathbb R^d$.

$z,u,v$: The operator argument and comparison point in the inequality. **Domain:** The ambient space is $\mathbb R^d$. Formulas constrained by $K$ require the corresponding point to lie in $K$.

$K$: A known nonempty closed convex feasible set, possibly unbounded. **Domain:** A subset of Euclidean space.

$K\subset\mathbb R^d$

$N_K(z)$: Use the Euclidean normal cone of the closed convex feasible set K at the feasible point z. The same definition applies blockwise to $N_X$ and $N_Y$. **Domain:** $z\in K,\quad N_K(z)\subset\mathbb R^d$.

$N_K(z)=\{v:\langle v,u-z\rangle\le0\ \forall u\in K\}$

$\operatorname{dist}(0,S)$: Infimum of the Euclidean distances from vectors in $S$ to the origin **Domain:** Nonnegative extended real value.

$\operatorname{dist}(0,S)=\inf_{v\in S}\|v\|_2$

$z_0,z^\star$: Public initial point and the same solution appearing in the model assumption **Domain:** Feasible domain of this profile; the distance bound refers to the same solution.

$\widehat z$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** $K\subset\mathbb R^d$.

$G_F(z;\xi),G_t$: Random vector sample of population operator $F$ and its response at time $t$. **Domain:** $\mathbb R^d$.

$\xi,\mathcal H_t,z_t$: Current fresh-sample seed, complete pre-query history, and query point. **Domain:** The seed space, history-generated $\sigma$-algebra, and declared query domain.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm sample}$: Number of fresh-sample complete-operator-vector calls **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Number of exact Euclidean projections onto the known feasible domain, recorded separately from primary information queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs, a hidden admissible object fixed before interaction, and an oracle law satisfying the declared conditional means, variances, and independence protocol. **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\log,\ln,\log_+$: Natural logarithm and its nonnegative truncation **Domain:** Arguments of log and ln are positive; the argument of $\log_+$ may be zero.

$\log_+(t)=\log(\max\{1,t\})$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm sample}(\mathcal A,I,\omega)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - The nontrivial accuracy region.

**Region.** $0<\varepsilon\le\beta R$

**Quantity.** Q1

**Resource.** The number of actual sampled responses.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
\widetilde{O}(\beta R/\varepsilon+(\sigma^2/\varepsilon^2)\log^3(2+\beta R/\varepsilon))
$$

**Comparison argument.** The randomized residual lower bound and logarithmic terms have not been fully checked. The source abstract's phrase “nearly optimal” is not sufficient certification.

### R2 - Noise-dominated regime

**Region.** $0<\varepsilon\le\beta R$, $\sigma^2/\varepsilon^2\ge1+\beta R/\varepsilon$.

**Quantity.** Q1

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(\sigma^2/\varepsilon^2)
$$

**Upper bound.** B1

$$
\widetilde{O}\!\left(\frac{\sigma^2}{\varepsilon^2}\log^3(2+\beta R/\varepsilon)\right)
$$

**Gap or comparison.** $\log^3(2+\beta R/\varepsilon)\operatorname{polyloglog}(2+\beta R/\varepsilon)$

**Comparison argument.** The upper-bound tilde hides only the additional log-log factors declared in the source. Not all low-noise regimes are closed.

## 4. Bounds and supporting evidence

### B1 - accumulative regularization with operator-extrapolation subsolvers

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The AR subroutine in source Theorem 2 uses stochastic operator samples.

$$
\widetilde{O}(\beta R/\varepsilon+(\sigma^2/\varepsilon^2)\log^3(2+\beta R/\varepsilon))
$$

**Sources.** [1](https://arxiv.org/pdf/2609.04188v2)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle correspondence.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee conversion.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output rule.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource conversion.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N sample.**

$$
\widetilde O(\beta R/\varepsilon+(\sigma^2/\varepsilon^2)\log^3(2+\beta R/\varepsilon))
$$

**N projection.** same-order iteration count; mini-batches only raise sampling cost

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** Only polynomial factors in $\log\log(2+\beta R/\varepsilon)$ are hidden. The outer cubed logarithm is explicit.

**Source location.** [1](https://arxiv.org/pdf/2609.04188v2) theorem: Theorem2; section: Section2; pdf pages: 11; 12

Identify the source constants $L,D_0$ with $\beta,R$. The complete stochastic theorem gives a mean-square tangent-residual guarantee and specifies each stage's batch size in advance.

### B2 - Gaussian two-point testing and endpoint solutions.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Two-point testing, zero-query indistinguishability, and nonexistence counterexamples cover arbitrary privately randomized policies. These are not linear-span lower bounds.

$$
\Omega(\sigma^2/\varepsilon^2)
$$

**Conditions.** Take $K=[-R,R]$, $z_0=0$, constant operators $F_\pm=\pm4\varepsilon$, and noise $N(0,\sigma^2)$. Their tangent residual vanishes only at the left and right endpoints, respectively; elsewhere it equals $4\varepsilon$. Mean-square residual $\le\varepsilon^2$ forces endpoint-identification success $\ge15/16$. Two-point testing requires $\Omega(\sigma^2/\varepsilon^2)$ samples. Constant operators satisfy any positive Lipschitz upper bound $\beta$.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Local argument.** A1

## 5. Local arguments

### A1 - Gaussian two-point testing and endpoint solutions.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Take $K=[-R,R]$, $z_0=0$, constant operators $F_\pm=\pm4\varepsilon$, and noise $N(0,\sigma^2)$. Their tangent residual vanishes only at the left and right endpoints, respectively; elsewhere it equals $4\varepsilon$. Mean-square residual $\le\varepsilon^2$ forces endpoint-identification success $\ge15/16$. Two-point testing requires $\Omega(\sigma^2/\varepsilon^2)$ samples. Constant operators satisfy any positive Lipschitz upper bound $\beta$.

## References

[1] Yao Ji; Guanghui Lan; Jason Zhu. Computation of Strong Solutions to Stochastic Variational Inequalities. 2026. arXiv:2609.04188v2, 2026-09-17.

https://arxiv.org/pdf/2609.04188v2
