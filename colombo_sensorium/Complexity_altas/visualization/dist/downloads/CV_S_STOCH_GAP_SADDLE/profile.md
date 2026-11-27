# Stochastic convex-concave saddle-point problems: expected global gap

**Setting ID.** `CV_S_STOCH_GAP_SADDLE`

Minimax optimization

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$.

**Status.** Fully optimal

**TASK tags.** formulation: Convex concave saddle; task family: Minimax

**MODEL tags.** convexity: Convex concave; geometry: Diameter bound; geometry: Known compact

**ORACLE tags.** feedback quality: Exact; feedback quality: Unbiased conditional on query history conditional squared noise norm sigma; interface family: Fresh joint gradient; operation: Projection; operation: Stochastic joint gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal dual pair; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Saddle-point gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N projection; measure: N sample; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$.

### Admissible model

The set $K\subset\mathbb{R}^d$ is known, nonempty, compact, and convex, with $\operatorname{diam}(K)\le D_K$. The conditions $K=X\times Y$ and $d=d_x+d_y$ also hold.

The function $f$ is convex in $x$, concave in $y$, and has a jointly $\beta$-Lipschitz gradient.

These assumptions ensure the relevant solutions exist; all vector norms are Euclidean.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $D_K$, $\beta$, $\varepsilon$, and $\sigma$, together with the stated initial-point and feasible-domain information. Analytic representations of hidden functions, operators, or matrices are not revealed.

$$
z\in K\longmapsto G_f(z;\xi)=(G_x,G_y)
$$

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

Let $\mathcal H_t$ denote the full history before query t. Conditional on $\mathcal H_t,z_t$, the response $G_t\in\mathbb R^{d_x+d_y}$ satisfies $\mathbb E[G_t\mid\mathcal H_t,z_t]=\nabla f(z_t)$ and $\mathbb E[\|G_t-\nabla f(z_t)\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$. Each call uses an independent fresh sample.

No reusable sample identifier or cross-point sample reuse is available. No mean-square smoothness of sample gradients or operators is additionally assumed. Blocks within a full vector may be correlated.

### Output

Return $(\widehat{x},\widehat{y})\in X\times Y$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\max_{v\in Y}f(\widehat{x},v)-\min_{u\in X}f(u,\widehat{y})
$$

This gap is finite and nonnegative on the compact domain.

### Resource accounting

Each fresh sample vector costs one $N_{\rm sample}$ call. Projection costs are recorded separately.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\max_{v\in Y}f(\widehat{x},v)-\min_{u\in X}f(u,\widehat{y})\right]\le\varepsilon.
$$

Expectation is outside the complete error expression; internal maxima or suprema are not moved outside it.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$D_K$: A Euclidean-diameter bound on the entire feasible product domain. **Domain:** Positive real number.

$\operatorname{diam}(K)=\sup_{u,v\in K}\|u-v\|_2\le D_K$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: Target tolerance for the complete weak-VI gap or global saddle gap, in the units of that gap. **Domain:** Positive real number.

$\sigma$: Standard-deviation upper bound for noise in the full stochastic response, controlling the joint squared norm rather than summing independent block budgets. **Domain:** Positive real number.

$\mathbb E[\|G_t-\mathbb E[G_t\mid\mathcal H_t,z_t]\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$d_x,d_y$: Positive integer primal and dual block dimensions; joint dimension $d=d_x+d_y$ **Domain:** Positive integer.

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$K$: A known nonempty compact convex feasible set. **Domain:** A subset of Euclidean space.

$K=X\times Y\subset\mathbb R^{d_x+d_y}$

$X,Y$: Both primal and dual domains are known, nonempty, compact, and convex. Their product has diameter at most $D_K$. **Domain:** $X\subset\mathbb R^{d_x},\ Y\subset\mathbb R^{d_y}$.

$\widehat x,\widehat y$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** Feasible variable pairs in $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$G_f(z;\xi),G_t$: Random sample of the full joint gradient and the response from sample $t$ **Domain:** $\mathbb R^{d_x+d_y}$. The two blocks may be internally correlated.

$G_f=(G_x,G_y)$

$G_x,G_y$: The primal and dual blocks in one complete joint-gradient sample. **Domain:** $G_x\in\mathbb R^{d_x},\ G_y\in\mathbb R^{d_y}$.

$\xi,\mathcal H_t,z_t$: Current fresh-sample seed, complete pre-query history, and query point. **Domain:** The seed space, history-generated $\sigma$-algebra, and declared query domain.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm sample}$: Number of full joint-gradient queries using fresh samples **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Number of exact Euclidean projections onto the known feasible domain, recorded separately from primary information queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs, a hidden admissible object fixed before interaction, and an oracle law satisfying the declared conditional means, variances, and independence protocol. **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

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

### R1 - Noise-dominated regime

**Region.** $0<\varepsilon\le\min\{\sigma^2/\beta,\sigma D_K/16\}$

**Quantity.** Q1

**Resource.** The number of actual sampled responses.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(\sigma^2D_K^2/\varepsilon^2)
$$

**Upper bound.** B1

$$
O(\sigma^2D_K^2/\varepsilon^2)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** noise window makes beta $D_K$²/eps and1 bounded by sigma²$D_K$²/eps²; all-region upper includes this subregion.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - Stochastic Mirror-Prox with fresh two-call iterations

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** Stochastic Mirror-Prox uses fresh oracle samples. Updates can be deterministic given the responses, while the execution remains random.

$$
O(1+\beta D_K^2/\varepsilon+\sigma^2D_K^2/\varepsilon^2)
$$

**Sources.** [1](https://www.isye.gatech.edu/~nemirovs/SMP.pdf)

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N sample.**

$$
O(1+\beta D_K^2/\varepsilon+\sigma^2D_K^2/\varepsilon^2)
$$

**N projection.**

$$
O(1+\beta D_K^2/\varepsilon+\sigma^2D_K^2/\varepsilon^2)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://www.isye.gatech.edu/~nemirovs/SMP.pdf) theorem: Theorem3.3 and Corollary3.4, (3.12); section: Section3; pdf pages: 8

Set the source model's additional linear-growth constant $M$ and feedback bias to zero, and use the Euclidean distance-generating function. The expected saddle-gap guarantee uses the source's separate Nash–VI result.

### B2 - two Gaussian mean hypotheses on an interval

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Two-point testing, zero-query indistinguishability, and nonexistence counterexamples cover arbitrary privately randomized policies. These are not linear-span lower bounds.

$$
\Omega(\sigma^2D_K^2/\varepsilon^2)
$$

**Dimension conditions.** One dimension suffices; the saddle-point variant may use a singleton dual domain.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega(\sigma^2D_K^2/\varepsilon^2)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** Use the primal interval $[-D_K/2,D_K/2]$, a singleton dual domain, and linear payoffs $f_\pm(x,y)=\pm ax$ with $a=8\varepsilon/D_K$. Fresh primal-gradient samples are Gaussian with mean $\pm a$ and variance $\sigma^2$. A wrong-half-axis output has saddle gap at least $4\varepsilon$, so the expected-gap guarantee implies a sign test with error at most $1/4$. The per-sample KL divergence $2a^2/\sigma^2$ yields the query lower bound $\Omega(\sigma^2D_K^2/\varepsilon^2)$.

**Local argument.** SIX_PROOF_02349a853ced

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 31ca0480309050e6b404c732ebc829d7a90278a936b4915170d17ba0b36123f8

### Native proof: SIX_PROOF_02349a853ced

Native pointer: /proofs/0; canonical SHA-256: dfdb6c63ff2e1353858acbad32a5d753a26dfafd78c3e22e5984a5d0a05dfb53

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: b1c0b2fd2b167defdb5312da42df9fa6ecf09aff97f1945820693b5d6da48a59

two Gaussian mean hypotheses on an interval

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 27c0383e314700790d706698d4658be84d6f8ead98ae92e1089d88d6172985e2

Use the primal interval $[-D_K/2,D_K/2]$, a singleton dual domain, and linear payoffs $f_\pm(x,y)=\pm ax$ with $a=8\varepsilon/D_K$. Fresh primal-gradient samples are Gaussian with mean $\pm a$ and variance $\sigma^2$. A wrong-half-axis output has saddle gap at least $4\varepsilon$, so the expected-gap guarantee implies a sign test with error at most $1/4$. The per-sample KL divergence $2a^2/\sigma^2$ yields the query lower bound $\Omega(\sigma^2D_K^2/\varepsilon^2)$.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

## References

[1] Anatoli Juditsky; Arkadi Nemirovski; Claire Tauvel. Solving Variational Inequalities with Stochastic Mirror-Prox Algorithm. 2011. author PDF, Stochastic Systems 1(1).

https://www.isye.gatech.edu/~nemirovs/SMP.pdf
