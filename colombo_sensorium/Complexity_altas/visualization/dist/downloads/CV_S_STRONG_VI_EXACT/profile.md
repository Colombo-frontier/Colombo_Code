# Strongly monotone variational inequalities: exact operator values and distance to the solution

**Setting ID.** `CV_S_STRONG_VI_EXACT`

Variational inequalities

Solve $0\in F(z)+N_K(z)$.

**Status.** Bounds missing

**TASK tags.** solution concept: Solution distance; task family: Variational inequality

**MODEL tags.** initialization: Initial distance; initialization: Initialization; monotonicity: Strong monotonicity; monotonicity: Strongly monotone

**ORACLE tags.** feedback quality: Exact; interface family: Exact operator; operation: Operator value; operation: Projection; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Distance

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N operator value; measure: N projection; setup: Initialization included

## 1. Setting specification

### Task

Solve $0\in F(z)+N_K(z)$.

### Admissible model

The set $K\subset\mathbb{R}^d$ is known, nonempty, closed, and convex. The operator $F$ is $\beta$-Lipschitz and $\mu$-strongly monotone: $\langle F(u)-F(v),u-v\rangle\ge\mu\|u-v\|_2^2$ and $\beta\ge\mu>0$.

A unique solution $z^\star$ exists, and the public initial point $z_0\in K$ satisfies $\|z_0-z^\star\|_2\le R_0$.

### Oracle interface

Public inputs include dimension $d$ and $R_0$, $\beta$, $\varepsilon$, and $\mu$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
z\in K\longmapsto F(z)
$$

An exact full-vector response, not a derivative-order label for a scalar objective.

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

### Output

Return $\widehat{z}\in K$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|\widehat{z}-z^\star\|_2
$$

### Resource accounting

Each operator-value call counts once in $N_{\rm operator}$; projection counts are recorded separately.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Any measurable sequential adaptive deterministic algorithm is allowed. Queries and outputs may use the complete history, with no additional span, zero-support, communication, or memory restriction.

The same deterministic algorithm must satisfy the guarantee for every admissible instance.

$$
\|\widehat{z}-z^\star\|_2\le\varepsilon.
$$

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$R_0$: Euclidean distance bound from the public initial point to the same solution promised by the model; not the entire domain diameter **Domain:** A nonnegative real.

$\|z_0-z^\star\|_2\le R_0$

$\beta$: Euclidean Lipschitz upper bound for the population operator on the declared query domain **Domain:** Positive real number.

$\|F(z)-F(w)\|_2\le\beta\|z-w\|_2$

$d$: Finite Euclidean dimension of the operator domain; regime quantifiers specify whether complexity is uniform in dimension **Domain:** Positive integer.

$\varepsilon$: Euclidean distance tolerance to the unique solution; the mean-square contract targets squared distance $\varepsilon^2$. **Domain:** Positive real number.

$\mu$: A strong-monotonicity lower bound for the full operator. **Domain:** Positive real number.

$\langle F(u)-F(v),u-v\rangle\ge\mu\|u-v\|_2^2$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$F$: The unknown operator is single-valued. Monotonicity, strong monotonicity, or weak Minty properties use the specification’s explicit inequalities. **Domain:** A vector map from the declared query domain into $\mathbb R^d$.

$z,u,v$: The operator argument and comparison point in the inequality. **Domain:** The ambient space is $\mathbb R^d$. Formulas constrained by $K$ require the corresponding point to lie in $K$.

$K$: A known nonempty closed convex feasible set, possibly unbounded. **Domain:** A subset of Euclidean space.

$K\subset\mathbb R^d$

$z_0,z^\star$: Public initial point and the same solution appearing in the model assumption **Domain:** Feasible domain of this profile; the distance bound refers to the same solution.

$\widehat z$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** $K\subset\mathbb R^d$.

$N_{\rm operator}$: The number of complete exact operator-value calls. **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Projection count, uncharged in the primary query-cost projection **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\log,\ln,\log_+$: Natural logarithm and its nonnegative truncation **Domain:** Arguments of log and ln are positive; the argument of $\log_+$ may be zero.

$\log_+(t)=\log(\max\{1,t\})$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I N_{\rm operator}(\mathcal A,I)
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
O\!\left(\frac{\beta}{\mu}\left[1+\log\frac{R_0}{\varepsilon}\right]\right)
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

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle mapping.** All primitive information operations are charged; see the specification and method description.

**Guarantee mapping.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource mapping.** Complete query budget of a single algorithm

### B1 - Geometrically restarted extragradient method (Corollary 1)

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Apply geometric restarting to a deterministic exact-operator residual method. Public parameters determine every restart threshold.

$$
O\!\left(\frac{\beta}{\mu}\left[1+\log\frac{R_0}{\varepsilon}\right]\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.04188v2)

**Conditions.** Set squared-distance tolerance in Corollary 1 to $\delta=\varepsilon^2$, with $D_0=R_0$ and $L=\beta$. Equations (2.43)-(2.46) give the mean-square distance bound with fixed stage count and batch sizes.; With zero noise and deterministic subsolvers, the source's mean-square expression becomes a deterministic squared-distance bound for each instance. The cited result is the explicit noiseless branch.

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [1](https://arxiv.org/pdf/2609.04188v2) theorem: Corollary 1; section: Section 2.3; pdf pages: 13; 14; equations: (2.43); (2.44); (2.45); (2.46)

$$
O\!\left(\frac{\beta}{\mu}\left[1+\log\frac{R_0}{\varepsilon}\right]\right)
$$

In Corollary 1, set the squared-distance tolerance to $\delta=\varepsilon^2$ and identify $D_0=R_0$ and $L=\beta$. Equations (2.43)-(2.46) give a mean-square distance bound with fixed stage and batch counts. With zero noise and deterministic subsolvers, this becomes an instancewise deterministic squared-distance guarantee. Only that noiseless branch is used here.

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

**Local argument.** A1

## 5. Local arguments

### A1 - Return the public initial point.

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

The public initialization promise gives $\|z_0-z^\star\|\le R_0$. When $\varepsilon\ge R_0$, returning $z_0$ without querying satisfies both the distance target and its mean-square version, deterministically. Query costs are nonnegative, so the minimum is exactly zero.

## References

[1] Yao Ji; Guanghui Lan; Jason Zhu. Computation of Strong Solutions to Stochastic Variational Inequalities. 2026. arXiv:2609.04188v2, 2026-09-17.

https://arxiv.org/pdf/2609.04188v2
