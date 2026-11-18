# Finite-sum monotone inclusions: component values and an exact resolvent.

**Setting ID.** `CV_S_FINITE_VI_GENERAL_INCLUSION`

Variational inequalities

$$
0\in F(z)+G(z),\quad F=\frac1n\sum_iF_i.
$$

**Status.** Bounds missing

**TASK tags.** formulation: Finite sum monotone inclusion; solution concept: Graph residual; task family: Variational inequality

**MODEL tags.** initialization: Root localization; monotonicity: Maximal monotone; smoothness: Mean square average; smoothness: Mean square component lipschitz; structure: Finite sum

**ORACLE tags.** feedback quality: Exact; index control: Algorithm selects; interface family: Component plus resolvent; operation: Component operator value; operation: Known resolvent; operator derivative order: Operator value (order 0); public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point operator certificate; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Graph residual

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Worst-instance expected cost; measure: N component; measure: N resolvent; precision: Bit precision not counted

## 1. Setting specification

### Task

$$
0\in F(z)+G(z),\quad F=\frac1n\sum_iF_i.
$$

### Admissible model

The condition $F=n^{-1}\sum_{i=1}^nF_i:\mathbb{R}^d\to\mathbb{R}^d$ holds. The average $F$ is monotone; individual components need not be monotone.

$$
\frac1n\sum_i\|F_i(u)-F_i(v)\|_2^2\le\beta^2\|u-v\|_2^2\quad(\forall u,v\in\mathbb{R}^d).
$$

The public initial point is $0$. There exists $z^\star$ satisfying $0\in F(z^\star)+G(z^\star)$ and $\|z^\star\|_2\le R$.

The operator $G$ is maximally monotone and set-valued; its exact resolvent is a separate available interface.

### Oracle interface

Public inputs include dimension $d$ and $R$, $\beta$, $\varepsilon$, and $n$, together with the stated initial-point and feasible-domain information. Analytic representations of hidden functions, operators, or matrices are not revealed.

$$
(i,z)\longmapsto F_i(z),\quad i\in\{1,\ldots,n\},\ z\in\mathbb{R}^d.
$$

The algorithm selects component indices. Components are fixed and responses exact. Repeated evaluations of the same component are charged separately.

$$
(\eta,u)\longmapsto J_{\eta G}(u)=(\operatorname{Id}+\eta G)^{-1}u,\quad\eta>0.
$$

This resolvent applies only to $G$, not the full unknown $F+G$.

### Output

Return $(\widehat{z},\widehat{g})\in\mathbb{R}^d\times\mathbb{R}^d$ with guarantee $\widehat{g}\in G(\widehat{z})$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|F(\widehat{z})+\widehat{g}\|_2
$$

The returned $\widehat{g}$ is a valid graph element. An uncomputable optimal selection is not substituted for the actual output.

### Resource accounting

Each $F_i(z)$ increments $N_{\rm component}$ by one; a full average costs $n$ calls. Calls to $J_{\eta G}$ are recorded separately as $N_{\rm resolvent}$. The primary scalar comparison projects onto component calls only.

Use expected work on the worst instance. The algorithm stops almost surely, with call count $\tau$ satisfying $\sup_I\mathbb{E}[\tau]\le N$. This does not require every execution path to finish within $N$ calls.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\left(\|F(\widehat{z})+\widehat{g}\|_2\right)^2\right]\le\varepsilon^2.
$$

Expectation is only over the algorithm's private seed. Exact responses from fixed components contain no oracle noise.

**Budget convention.** worst-case expected total calls, random stopping allowed

## 2. Notation and parameters

$R$: Euclidean distance bound from the public initial point to the same solution promised by the model; not the entire domain diameter **Domain:** Positive real number.

$\|z_0-z^\star\|_2\le R$

$\beta$: A mean-square average Lipschitz bound on component-operator differences. **Domain:** Positive real number.

$\frac1n\sum_{i=1}^n\|F_i(z)-F_i(w)\|_2^2\le\beta^2\|z-w\|_2^2$

$d$: Finite Euclidean dimension of the operator domain; regime quantifiers specify whether complexity is uniform in dimension **Domain:** Positive integer.

$\varepsilon$: Tolerance for the true root residual or Euclidean norm of an admissible graph element. **Domain:** Positive real number.

$n$: Fixed number of finite-sum components; the full function or operator is their 1/n average **Domain:** Positive integer.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$F$: The unknown operator is single-valued. Monotonicity, strong monotonicity, or weak Minty properties use the specification’s explicit inequalities. **Domain:** A vector map from the declared query domain into $\mathbb R^d$.

$z,u,v$: The operator argument and comparison point in the inequality. **Domain:** The ambient space is $\mathbb R^d$. Formulas constrained by $K$ require the corresponding point to lie in $K$.

$F_i,i$: Fixed component operators and algorithm-selected indices **Domain:** $i\in\{1,\ldots,n\},\ F_i:\text{query domain}\to\mathbb R^d$.

$F=\frac1n\sum_{i=1}^n F_i$

$\widehat z$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** $\mathbb R^d$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm component}$: Number of full operator-value queries to a specified component **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm resolvent}$: Only exact resolvent calls for the stated set-valued operator G are counted **Domain:** Nonnegative integer count; expected work is its expectation.

$\tau$: Cumulative primary information calls at termination of one run; almost surely finite, with random stopping allowed. **Domain:** A nonnegative integer-valued random variable.

$\sup_I\mathbb E[\tau]\le N$

$N$: A worst-instance upper bound on expected total information calls at termination. **Domain:** A nonnegative real.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$G,\widehat g$: A set-valued monotone operator and the admissible graph element actually returned. **Domain:** $G:\mathbb R^d\rightrightarrows\mathbb R^d,\quad\widehat g\in G(\widehat z)$.

$J_{\eta G}$: Only the exact resolvent of G is supplied; it does not include the unknown mean operator F. **Domain:** $\eta>0,\quad J_{\eta G}:\mathbb R^d\to\mathbb R^d$.

$J_{\eta G}(u)=(\operatorname{Id}+\eta G)^{-1}(u)$

$\eta,\operatorname{Id}$: An algorithm-selected positive step size and the identity map. **Domain:** Positive real number; identity linear map on $\mathbb R^d$.

$z_0,z^\star$: The public initial point and the same solution satisfying $0\in F(z^\star)+G(z^\star)$ **Domain:** $z_0=0,\quad\|z^\star\|_2\le R$.

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \mathbb E_\omega[N_{\rm component}(\mathcal A,I,\omega)]
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

Each call counts the complete response package specified by this interface. The algorithm class retains the stated randomization, adaptivity, and output conditions and must satisfy the full error guarantee for every fixed admissible instance. Expectations include the algorithm's seed and sampled observations; the stated random stopping rules are allowed.

### R1 - Main theorem's applicability region

**Region.** $n\ge1,\ 0<\varepsilon\le\beta R/2$

**Quantity.** Q1

**Resource.** Expected total number of component queries.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(n+\sqrt n\,\beta R/\varepsilon)
$$

**Comparison argument.** restricted lower is stored under a different specification and is not transferred to arbitrary algorithms.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - recursive regularization and centered variance reduction

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** Finite-sum recursive regularization and centered variance reduction genuinely sample components at random.

$$
O(n+\sqrt n\,\beta R/\varepsilon)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.05038v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**E N component.**

$$
O(n+\sqrt n\,\beta R/\varepsilon)
$$

**E N resolvent.**

$$
O(n+\sqrt n\,\beta R/\varepsilon)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2610.05038v1) theorem: Theorem1 / Theorem2; Section4; section: Sections3--4; pdf pages: 6; 7

A full averaged-operator evaluation costs $n$ component calls, and a two-point difference costs two evaluations. The exact resolvent of the splitting term $G$ is a separately registered operation. A source linear-span lower bound does not automatically apply to the unrestricted-algorithm inclusion problem here.

## References

[1] Qihao Zhou. Optimal Oracle Complexity for Finite-Sum Monotone Inclusions. 2026. arXiv:2610.05038v1, 2026-10-04.

https://arxiv.org/pdf/2610.05038v1
