# Strongly convex-strongly concave saddle problems: fresh gradients and mean-square distance.

**Setting ID.** `CV_S_SCSC_FRESH`

Minimax optimization

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$, with $z=(x,y)$.

**Status.** Bounds missing

**TASK tags.** solution concept: Distance to unique saddle; task family: Minimax

**MODEL tags.** convexity: Strong concavity; convexity: Strongly convex strongly concave; geometry: Closed geometry; initialization: Initial distance; initialization: Initialization

**ORACLE tags.** feedback quality: Exact; feedback quality: Stochastic unbiased bounded variance; interface family: Fresh joint gradient; operation: Projection; operation: Stochastic joint gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point pair

**METRIC tags.** criterion: Distance

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N grad; measure: N projection; setup: Initialization included

## 1. Setting specification

### Task

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$, with $z=(x,y)$.

### Admissible model

$X,Y$ are known, nonempty, closed, and convex.

The function $f$ is jointly $\beta$-smooth, uniformly $\mu_x$-strongly convex in $x$, and uniformly $\mu_y$-strongly concave in $y$; $\beta\ge\max\{\mu_x,\mu_y\}>0$.

A unique saddle point $z^\star$ exists, and the public initial point satisfies $\|z_0-z^\star\|_2\le R_0$.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $R_0$, $\beta$, $\varepsilon$, $\mu_x$, $\mu_y$, and $\sigma$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
z\in X\times Y\longmapsto G_f(z;\xi)
$$

Let $\mathcal H_t$ denote the full history before query t. Conditional on $\mathcal H_t,z_t$, the response $G_t\in\mathbb R^{d_x+d_y}$ satisfies $\mathbb E[G_t\mid\mathcal H_t,z_t]=\nabla f(z_t)$ and $\mathbb E[\|G_t-\nabla f(z_t)\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$. Each call uses an independent fresh sample.

No reusable sample identifier or cross-point sample reuse is available. No mean-square smoothness of sample gradients or operators is additionally assumed. Blocks within a full vector may be correlated.

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

### Output

Return a feasible pair $\widehat{z}=(\widehat{x},\widehat{y})\in X\times Y$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|\widehat{z}-z^\star\|_2
$$

Do not use a global gap that may be infinite on an unbounded domain.

### Resource accounting

Each joint-gradient sample counts once in $N_{\rm grad}$.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\left(\|\widehat{z}-z^\star\|_2\right)^2\right]\le\varepsilon^2.
$$

Expectation is over private algorithmic randomness and the random samples actually used.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$R_0$: Euclidean distance bound from the public initial point to the same solution promised by the model; not the entire domain diameter **Domain:** A nonnegative real.

$\|z_0-z^\star\|_2\le R_0$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: Euclidean distance tolerance to the unique solution; the mean-square contract targets squared distance $\varepsilon^2$. **Domain:** Positive real number.

$\mu$: Strong-monotonicity constant inherited from the saddle operator **Domain:** Positive real number.

$\mu=\min\{\mu_x,\mu_y\}$

$\mu_x$: Uniform strong-convexity lower bound for $f(\cdot,y)$ at every fixed $y$ **Domain:** $0<\mu_x\le\beta$.

$f(u,y)\ge f(x,y)+\langle\nabla_xf(x,y),u-x\rangle+\frac{\mu_x}{2}\|u-x\|_2^2$

$\mu_y$: A uniform strong-convexity lower bound for −f(x,·) at every fixed x; equivalently, the dual strong-concavity modulus of f. **Domain:** $0<\mu_y\le\beta$.

$f(x,v)\le f(x,y)+\langle\nabla_yf(x,y),v-y\rangle-\frac{\mu_y}{2}\|v-y\|_2^2$

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

$X,Y$: Known nonempty closed convex primal and dual domains, possibly unbounded **Domain:** $X\subset\mathbb R^{d_x},\ Y\subset\mathbb R^{d_y}$.

$z_0,z^\star$: Public initial point and the same solution appearing in the model assumption **Domain:** Feasible domain of this profile; the distance bound refers to the same solution.

$\widehat x,\widehat y$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** Feasible variable pairs in $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$\widehat z$: Joint output consisting of the two variable blocks **Domain:** $\mathbb R^{d_x+d_y}$.

$\widehat z=(\widehat x,\widehat y)$

$G_f(z;\xi),G_t$: Random sample of the full joint gradient and the response from sample $t$ **Domain:** $\mathbb R^{d_x+d_y}$. The two blocks may be internally correlated.

$G_f=(G_x,G_y)$

$G_x,G_y$: The primal and dual blocks in one complete joint-gradient sample. **Domain:** $G_x\in\mathbb R^{d_x},\ G_y\in\mathbb R^{d_y}$.

$\xi,\mathcal H_t,z_t$: Current fresh-sample seed, complete pre-query history, and query point. **Domain:** The seed space, history-generated $\sigma$-algebra, and declared query domain.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm grad}$: Number of full joint-gradient queries using fresh samples **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Projection count, uncharged in the primary query-cost projection **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs, a hidden admissible object fixed before interaction, and an oracle law satisfying the declared conditional means, variances, and independence protocol. **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\log,\ln,\log_+$: Natural logarithm and its nonnegative truncation **Domain:** Arguments of log and ln are positive; the argument of $\log_+$ may be zero.

$\log_+(t)=\log(\max\{1,t\})$

$F$: Saddle operator induced by the payoff function **Domain:** $X\times Y\to\mathbb R^{d_x+d_y}$.

$F(x,y)=(\nabla_xf(x,y),-\nabla_yf(x,y))$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm grad}(\mathcal A,I,\omega)
$$

**Scope.** The instancewise guarantee uses the same contract; dimension obeys the specification and theorem region.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - The nontrivial accuracy region.

**Region.** $0<\varepsilon<R_0$.

**Quantity.** Q1

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O\!\left(\frac{\beta}{\mu}\left[1+\log\frac{R_0}{\varepsilon}\right]+\frac{\sigma^2}{\mu^2\varepsilon^2}\right)
$$

**Comparison argument.** A matching lower bound for arbitrary randomized or deterministic algorithms is not recorded on this full parameter range. Noise-dominated subregions are listed separately.

### R2 - Zero-query regime

**Region.** $\varepsilon\ge R_0$.

**Quantity.** Q1

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B2

$$
0
$$

**Comparison argument.** Cost is nonnegative.

### R3 - Noise-dominated regime

**Region.** $0<\varepsilon\le R_0/4$, $\sigma^2/(\mu^2\varepsilon^2)\ge1+(\beta/\mu)[1+\log(R_0/\varepsilon)]$.

**Quantity.** Q1

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B3

$$
\Omega(\sigma^2/(\mu^2\varepsilon^2))
$$

**Upper bound.** B1

$$
O(\sigma^2/(\mu^2\varepsilon^2))
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** Matching is certified only in this noise-dominated subregion. The statistical lower bound is not a deterministic condition-number lower bound.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle mapping.** All primitive information operations are charged; see the specification and method description.

**Guarantee mapping.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource mapping.** Complete query budget of a single algorithm

### B1 - Geometrically restarted extragradient method (Corollary 1)

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The restarted method for strongly monotone stochastic operators uses fresh samples; randomness comes from the oracle.

$$
O\!\left(\frac{\beta}{\mu}\left[1+\log\frac{R_0}{\varepsilon}\right]+\frac{\sigma^2}{\mu^2\varepsilon^2}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.04188v2)

**Conditions.** Set squared-distance tolerance in Corollary 1 to $\delta=\varepsilon^2$, with $D_0=R_0$ and $L=\beta$. Equations (2.43)-(2.46) give the mean-square distance bound with fixed stage count and batch sizes.

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [1](https://arxiv.org/pdf/2609.04188v2) theorem: Corollary 1; section: Section 2.3; pdf pages: 13; 14; equations: (2.43); (2.44); (2.45); (2.46)

$$
O\!\left(\frac{\beta}{\mu}\left[1+\log\frac{R_0}{\varepsilon}\right]+\frac{\sigma^2}{\mu^2\varepsilon^2}\right)
$$

Set squared-distance tolerance in Corollary 1 to $\delta=\varepsilon^2$, with $D_0=R_0$ and $L=\beta$. Equations (2.43)-(2.46) give the mean-square distance bound with fixed stage count and batch sizes.

### B2 - Return the public initial point.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** In this region, the witness returns the public initial point or known root, deterministically and without querying.

$$
0
$$

**Conditions.** This follows directly from the initial-distance assumption.

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Local argument.** SIX_PROOF_84a11f0b7cf2

### B3 - Two-point Gaussian test

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Two-point testing, zero-query indistinguishability, and nonexistence counterexamples cover arbitrary privately randomized policies. These are not linear-span lower bounds.

$$
\Omega(\sigma^2/(\mu^2\varepsilon^2))
$$

**Conditions.** In one dimension use $F_a(z)=\mu(z-a)$, $a\in\{-4\varepsilon,4\varepsilon\}$, and additive $N(0,\sigma^2)$ noise. Subtracting the known $\mu z$ leaves observations with mean $-\mu a$. Mean-square distance $\le\varepsilon^2$ forces sign-testing error $\le1/16$. The per-sample KL divergence is $32\mu^2\varepsilon^2/\sigma^2$, yielding the stated query lower bound. For saddle problems, embed this quadratic in the block with smaller curvature and use an independent known strongly convex or strongly concave quadratic in the other block.

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Local argument.** SIX_PROOF_35fff769a08c

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 22180e55d8edc8eebfcf60ce22f5554eaecf361c6d5f11db54a0f81e3848ba80

### Native proof: SIX_PROOF_84a11f0b7cf2

Native pointer: /proofs/0; canonical SHA-256: 1c2089eb30962bc28d14d72d504439dcf1d929bdbc83460ed2a255b870bc31b0

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 8953a390e1a74ba4192dbd71560f477ddada31a889b8d02ed4e96d05fb997f3f

Return the public initial point.

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 1104ab2b77a966ad7c37dcc25a63eff52c51b079eea5f4e6892f9ced11f1c53b

The public initialization promise gives $\|z_0-z^\star\|\le R_0$. When $\varepsilon\ge R_0$, returning $z_0$ without querying satisfies both the distance target and its mean-square version, deterministically. Query costs are nonnegative, so the minimum is exactly zero.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

### Native proof: SIX_PROOF_35fff769a08c

Native pointer: /proofs/1; canonical SHA-256: fa725d54b58ca3ddf274617c43aaebede9d1f2d7249b4c85596217ada71bae7c

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 6e66b7ba62031ce1ee7d217bb8b7332958277e17126fdcc7b616fffa51807a54

Gaussian two-point testing

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: e289d3a95c4d1329c88fb94ceea0c8e8efdce5fceffa0ee9fd75145d0a493026

In one dimension use $F_a(z)=\mu(z-a)$, $a\in\{-4\varepsilon,4\varepsilon\}$, and additive $N(0,\sigma^2)$ noise. Subtracting the known $\mu z$ leaves observations with mean $-\mu a$. Mean-square distance $\le\varepsilon^2$ forces sign-testing error $\le1/16$. The per-sample KL divergence is $32\mu^2\varepsilon^2/\sigma^2$, yielding the stated query lower bound. For saddle problems, embed this quadratic in the block with smaller curvature and use an independent known strongly convex or strongly concave quadratic in the other block.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

## References

[1] Yao Ji; Guanghui Lan; Jason Zhu. Computation of Strong Solutions to Stochastic Variational Inequalities. 2026. arXiv:2609.04188v2, 2026-09-17.

https://arxiv.org/pdf/2609.04188v2
