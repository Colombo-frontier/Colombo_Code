# Monotone Lipschitz variational inequalities: deterministic tangential residual

**Setting ID.** `CV_S_VI_RESIDUAL_DET`

Variational inequalities

Solve $0\in F(z)+N_K(z)$.

**Status.** Fully optimal

**TASK tags.** formulation: Stampacchia vi; task family: Variational inequality

**MODEL tags.** geometry: Known closed; initialization: Root localization; monotonicity: Monotone; monotonicity: Monotone lipschitz

**ORACLE tags.** feedback quality: Exact; interface family: Exact operator; operation: Operator value; operation: Projection; operator derivative order: Operator value (order 0); public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Tangential residual

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N operator; measure: N projection; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $0\in F(z)+N_K(z)$.

### Admissible model

The set $K\subset\mathbb R^d$ is public, nonempty, closed, and convex, and may be unbounded. The operator $F$ is monotone and $\beta$-Lipschitz on $K$.

The initial point $z_0\in K$ is public, and a solution $z^\star$ satisfies $\|z_0-z^\star\|_2\le R$. The condition $\operatorname{diam}(K)\le R$ is not required.

### Oracle interface

Public inputs include dimension $d$ and $R$, $\beta$, and $\varepsilon$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
z\in K\longmapsto F(z)
$$

Return the complete exact operator value, not one coordinate or a scalar function value.

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

Each complete operator-value call counts once in $N_{\rm operator}$; projection counts are recorded separately.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Any measurable sequential adaptive deterministic algorithm is allowed. Queries and outputs may use the complete history, with no additional span, zero-support, communication, or memory restriction.

The same deterministic algorithm must satisfy the guarantee for every admissible instance.

$$
\operatorname{dist}(0,F(\widehat{z})+N_K(\widehat{z}))\le\varepsilon.
$$

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$R$: Euclidean distance bound from the public initial point to the same solution promised by the model; not the entire domain diameter **Domain:** Positive real number.

$\|z_0-z^\star\|_2\le R$

$\beta$: Euclidean Lipschitz upper bound for the population operator on the declared query domain **Domain:** Positive real number.

$\|F(z)-F(w)\|_2\le\beta\|z-w\|_2$

$d$: Finite Euclidean dimension of the operator domain; regime quantifiers specify whether complexity is uniform in dimension **Domain:** Positive integer.

$\varepsilon$: This is the tangent-residual tolerance. The mean-square guarantee uses its square $\varepsilon^2$. **Domain:** Positive real number.

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

$N_{\rm operator}$: The number of complete exact operator-value calls. **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Number of exact Euclidean projections onto the known feasible domain, recorded separately from primary information queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I N_{\rm operator}(\mathcal A,I)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - The nontrivial accuracy region.

**Region.** $0<\varepsilon\le\beta R$

**Quantity.** Q1

**Resource.** The number of operator-value responses.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(\beta R/\varepsilon)
$$

**Upper bound.** B1

$$
O(\beta R/\varepsilon)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** dimension-free worst-case quantity; deterministic class fixed before comparison.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - accumulative regularization with operator-extrapolation subsolvers

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The exact-operator AR–OE branch in source Section 2.2 and Theorem 1 uses deterministic subroutines.

$$
O(\beta R/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/2609.04188v2)

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N operator.**

$$
O(\beta R/\varepsilon)
$$

**N projection.** same-order iteration count; mini-batches only raise sampling cost

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [2](https://arxiv.org/pdf/2609.04188v2) theorem: Theorem1; section: Section2; pdf pages: 9

Identify the source Lipschitz constant $L$ and distance bound $D_0$ with $\beta$ and $R$, respectively. The deterministic output criterion in source Section 2.2 is the tangent residual.

### B2 - rotated affine monotone chain on a compact hard subclass

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

**Algorithm-scope qualification.** The source theorem covers arbitrary adaptive deterministic queries, beyond linear-span iterations. It does not thereby give an arbitrary-randomized lower bound.

$$
\Omega(\beta R/\varepsilon)
$$

**Sources.** [1](https://proceedings.mlr.press/v125/diakonikolas20a/diakonikolas20a.pdf)

**Dimension conditions.** Dimension $d\ge C\beta R/\varepsilon$ suffices. Complexity takes the worst case over all admissible finite dimensions.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega(\beta R/\varepsilon)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** The source hard domain can have diameter $R$, so any feasible public initial point is within $R$ of a solution. For every $v\in N_K(z)$, the local strong gap satisfies $\sup_{u\in K\cap B(z,1)}\langle F(z),z-u\rangle\le\|F(z)+v\|_2$, where $B(z,1)$ is the unit Euclidean ball centered at $z$. Taking the infimum over normal vectors converts the local-gap lower bound to a tangent-residual lower bound, preserving the quantifier over arbitrary deterministic algorithms.

**Source location.** [1](https://proceedings.mlr.press/v125/diakonikolas20a/diakonikolas20a.pdf) theorem: Lemma16(b), AppendixA oracle model; section: Section3 / AppendixA; pdf pages: 12; 23

The local strong gap on $K\cap B(z,1)$ is bounded above by the tangent residual; $B(z,1)$ is the unit Euclidean ball. The source lower bound covers arbitrary deterministic operator-query algorithms and does not establish a randomized lower bound.

## References

[1] Jelena Diakonikolas. Halpern Iteration for Near-Optimal and Parameter-Free Monotone Inclusion and Strong Solutions to Variational Inequalities. 2020. COLT, PMLR125:1428--1451.

https://proceedings.mlr.press/v125/diakonikolas20a/diakonikolas20a.pdf

[2] Yao Ji; Guanghui Lan; Jason Zhu. Computation of Strong Solutions to Stochastic Variational Inequalities. 2026. arXiv:2609.04188v2, 2026-09-17.

https://arxiv.org/pdf/2609.04188v2
