# Finite-sum monotone root finding with randomized linear-span algorithms

**Setting ID.** `CV_S_FINITE_VI_SPAN_ROOT`

Variational inequalities

$$
0\in F(z)+G(z),\quad F=\frac1n\sum_iF_i.
$$

**Status.** Fully optimal

**TASK tags.** formulation: Finite sum root; solution concept: Graph residual; task family: Variational inequality

**MODEL tags.** initialization: Root localization; smoothness: Mean square average; smoothness: Mean square component lipschitz; structure: Finite sum

**ORACLE tags.** feedback quality: Exact; index control: Algorithm selects; interface family: Component operator; operation: Component operator value; operator derivative order: Operator value (order 0); public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Linear span

**OUTPUT tags.** object: Point operator certificate; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Root residual

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Worst-instance expected cost; measure: N component; precision: Bit precision not counted

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

The public initial point is $z_0=0$. A root $z^\star\in\mathbb R^d$ satisfies $F(z^\star)=0$ and $\|z^\star\|_2\le R$.

To match the output notation of the inclusion problem, fix the set-valued operator $G(z)=\{0\}$. The returned graph element must be $\widehat g=0$; there is no separate unknown $G$.

### Oracle interface

Public inputs include dimension $d$ and $R$, $\beta$, $\varepsilon$, and $n$, together with the stated initial-point and feasible-domain information. Analytic representations of hidden functions, operators, or matrices are not revealed.

$$
(i,z)\longmapsto F_i(z),\quad i\in\{1,\ldots,n\},\ z\in\mathbb{R}^d.
$$

The algorithm selects component indices. Components are fixed and responses exact. Repeated evaluations of the same component are charged separately.

### Output

Return $(\widehat{z},\widehat{g})\in\mathbb{R}^d\times\mathbb{R}^d$ and ensure $\widehat{g}\in G(\widehat{z})$. Here $G=0$, so $\widehat{g}=0$.

Unqueried outputs are permitted, but remain subject to the stated linear-span condition.

### Loss or accuracy criterion

$$
\|F(\widehat z)\|_2.
$$

Under the present condition $G(z)=\{0\}$, the source notation $\|F(\widehat z)+\widehat g\|_2$ is exactly the root residual used here.

### Resource accounting

One $F_i(z)$ call counts once in $N_{\rm component}$; a complete mean requires $n$ calls.

Use expected work on the worst instance. The algorithm stops almost surely, with call count $\tau$ satisfying $\sup_I\mathbb{E}[\tau]\le N$. This does not require every execution path to finish within $N$ calls.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Randomized adaptive algorithms are allowed, but every query and output must lie in the span of previously received component vectors, starting from $0$. Indices, scalar coefficients, and stopping times may be adaptive.

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

$z_0,z^\star$: Public initial point and the same solution appearing in the model assumption **Domain:** Feasible domain of this profile; the distance bound refers to the same solution.

$\widehat z$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** $\mathbb R^d$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm component}$: Number of full operator-value queries to a specified component **Domain:** Nonnegative integer count; expected work is its expectation.

$\tau$: Cumulative primary information calls at termination of one run; almost surely finite, with random stopping allowed. **Domain:** A nonnegative integer-valued random variable.

$\sup_I\mathbb E[\tau]\le N$

$N$: A worst-instance upper bound on expected total information calls at termination. **Domain:** A nonnegative real.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$G,\widehat g$: A set-valued monotone operator and the admissible graph element actually returned. **Domain:** $G:\mathbb R^d\rightrightarrows\mathbb R^d,\quad\widehat g\in G(\widehat z)$.

$G(z)=\{0\},\ \widehat g=0$

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

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(n+\sqrt n\,\beta R/\varepsilon)
$$

**Upper bound.** B1

$$
O(n+\sqrt n\,\beta R/\varepsilon)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** RMS guarantee implies E residual≤eps; no projection is added to the root lower model.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

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

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**E N component.**

$$
O(n+\sqrt n\,\beta R/\varepsilon)
$$

**E N resolvent.** $0$; this branch sets $G=0$.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** When $G=0$, every linear combination, translation, and regularization starting at the origin remains in the span of previously revealed component vectors.

**Source location.** [1](https://arxiv.org/pdf/2610.05038v1) theorem: Theorem1 / Theorem2; Section4; section: Sections3--4; pdf pages: 6; 7

A full averaged-operator evaluation costs $n$ component calls; a same-component two-point difference costs two. The source lower bound concerns expected residual and hence also constrains a root-mean-square requirement, but only for its declared linear-span class.

### B2 - independent component chains and hidden shifted index

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** The stated restricted randomized class

**Algorithm-scope qualification.** The source lower bound concerns randomized linear-span queries and outputs under its declared expected-work budget.

$$
(n+\sqrt n\,\beta R/\varepsilon)/64
$$

**Sources.** [1](https://arxiv.org/pdf/2610.05038v1)

**Dimension conditions.** Dimension may grow with the expected-work threshold. Hard components are affine operators, with $G=0$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
(n+\sqrt n\,\beta R/\varepsilon)/64
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2610.05038v1) theorem: Theorem1 / Theorem2; Section4; section: Sections3--4; pdf pages: 6; 7

A full averaged-operator evaluation costs $n$ component calls; a same-component two-point difference costs two. The source lower bound concerns expected residual and hence also constrains a root-mean-square requirement, but only for its declared linear-span class.

## References

[1] Qihao Zhou. Optimal Oracle Complexity for Finite-Sum Monotone Inclusions. 2026. arXiv:2610.05038v1, 2026-10-04.

https://arxiv.org/pdf/2610.05038v1
