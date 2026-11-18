# Maximally monotone inclusion with an exact resolvent and selectable step size

**Setting ID.** `CV_S_EXACT_RESOLVENT`

Variational inequalities

$$
0\in A(z).
$$

**Status.** Fully optimal

**TASK tags.** formulation: Maximal monotone inclusion; solution concept: Graph residual; task family: Variational inequality

**MODEL tags.** monotonicity: Maximal monotone

**ORACLE tags.** feedback quality: Exact; interface family: Full resolvent free step; operation: Unknown operator exact resolvent; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: Graph-element certificate required; object: Point operator certificate; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Graph residual

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N resolvent; precision: Bit precision not counted

## 1. Setting specification

### Task

$$
0\in A(z).
$$

### Admissible model

The operator $A:\mathbb{R}^d\rightrightarrows\mathbb{R}^d$ is maximally monotone. A zero $z^\star$ satisfies $\|z_0-z^\star\|_2\le R$, and $R\ge0$ is public.

### Oracle interface

Public inputs comprise the dimension $d$ and parameters $R$ and $\varepsilon$, together with the stated initial point and feasible-set information. Analytic descriptions of hidden functions, operators, and matrices are not supplied.

$$
(\eta,u)\longmapsto J_{\eta A}(u)=(\operatorname{Id}+\eta A)^{-1}u,\quad\eta>0.
$$

The algorithm may choose any positive real step size. The full resolvent is exact, and step-size bit length is free.

### Output

Return $(\widehat{z},\widehat{v})$ with $\widehat{v}\in A(\widehat{z})$ almost surely. The response $\widehat{z}=J_{\eta A}(z_0)$ determines $\widehat{v}=(z_0-\widehat{z})/\eta$.

### Loss or accuracy criterion

$$
\|\widehat{v}\|_2,\quad\widehat{v}\in A(\widehat{z}).
$$

### Resource accounting

Each full-resolvent query costs one call. If $R=0$, output $(z_0,0)$ without querying. If $R>0$, a single query at $\eta\ge R/\varepsilon$ suffices.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\|\widehat{v}\|_2\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$R$: Euclidean distance bound from the public initial point to the same solution promised by the model; not the entire domain diameter **Domain:** A nonnegative real.

$\|z_0-z^\star\|_2\le R$

$d$: Finite Euclidean dimension of the operator domain; regime quantifiers specify whether complexity is uniform in dimension **Domain:** Positive integer.

$\varepsilon$: Tolerance for the true root residual or Euclidean norm of an admissible graph element. **Domain:** Positive real number.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$z_0,z^\star$: Public initial point and the same solution appearing in the model assumption **Domain:** Feasible domain of this profile; the distance bound refers to the same solution.

$\widehat z$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** $\mathbb R^d$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm resolvent}$: The number of exact resolvent calls for the complete unknown operator A. **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$A,\widehat v$: Unknown maximally monotone set-valued operator and an admissible output element of its graph **Domain:** $A:\mathbb R^d\rightrightarrows\mathbb R^d,\quad\widehat v\in A(\widehat z)$.

$J_{\eta A}$: Exact resolvent of the full unknown operator $A$. **Domain:** $\mathbb R^d\to\mathbb R^d$.

$J_{\eta A}=(\operatorname{Id}+\eta A)^{-1}$

$\eta$: Any positive real step size selected by the algorithm, without a bit-precision charge. **Domain:** Positive real number.

$$
\text{For }R>0,\text{ one may choose }\eta=R/\varepsilon
$$

$\operatorname{Id}$: The identity map on $\mathbb R^d$. **Domain:** Linear map.

$\operatorname{Id}(u)=u$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm resolvent}(\mathcal A,I,\omega)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - Positive initialization-radius regime

**Region.** $R>0,\ \varepsilon>0$

**Quantity.** Q1

**Resource.** The number of resolvent responses under this specification.

**Status.** Optimal

**Lower bound.** B2

$$
1
$$

**Upper bound.** B1

$$
1
$$

**Gap or comparison.** $1$

**Comparison argument.** Exact integer complexity1; eta can be chosen arbitrarily and its bit representation is free.

### R2 - Zero-radius regime

**Region.** $R=0$

**Quantity.** Q1

**Resource.** The number of resolvent responses under this specification.

**Status.** Optimal

**Lower bound.** B4

$$
0
$$

**Upper bound.** B3

$$
0
$$

**Comparison argument.** Initial root promise certifies exact solution without access.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - single exact resolvent with eta=R/eps

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The witnesses return either the public initial point or one exact resolvent query at a fixed step size. Neither uses private or oracle randomness.

$$
1
$$

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N resolvent.** 1

**arithmetic.** uncharged exact real arithmetic

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** Query $z=J_{\eta A}(z_0)$ and set $v=(z_0-z)/\eta$, giving $v\in A(z)$. Firm nonexpansiveness relative to a zero yields $\|z_0-z\|_2\le\|z_0-z^\star\|_2\le R$. The public step size $\eta=R/\varepsilon$ ensures $\|v\|_2\le\varepsilon$ using one exact resolvent call.

**Local argument.** A1

### B2 - two affine maximal monotone operators on the line

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Two-point testing, zero-query indistinguishability, and nonexistence counterexamples cover arbitrary privately randomized policies. These are not linear-span lower bounds.

$$
1
$$

**Dimension conditions.** Dimension $d=1$ already suffices.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.** 1

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** On the real line take $A_\pm(z)=(2\varepsilon/R)(z\mp R)$ and $z_0=0$. The roots are $\pm R$. Residual at most $\varepsilon$ requires the output to lie within radius $R/2$ of the respective root. These success sets are disjoint, so one zero-query output distribution cannot attain probability $2/3$ on both instances.

**Local argument.** A2

### B3 - return (z0,0)

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The witnesses return either the public initial point or one exact resolvent query at a fixed step size. Neither uses private or oracle randomness.

$$
0
$$

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.** 0

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** If the initialization radius is $R=0$, the promise directly gives $0\in A(z_0)$. Return $(z_0,0)$ without querying.

**Local argument.** A3

### B4 - nonnegative cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Two-point testing, zero-query indistinguishability, and nonexistence counterexamples cover arbitrary privately randomized policies. These are not linear-span lower bounds.

$$
0
$$

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.** 0

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** Query cost is nonnegative. Combined with a zero-query witness, this proves exact zero cost.

**Local argument.** A4

## 5. Local arguments

### A1 - single exact resolvent with eta=R/eps

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Query $z=J_{\eta A}(z_0)$ and set $v=(z_0-z)/\eta$, giving $v\in A(z)$. Firm nonexpansiveness relative to a zero yields $\|z_0-z\|_2\le\|z_0-z^\star\|_2\le R$. The public step size $\eta=R/\varepsilon$ ensures $\|v\|_2\le\varepsilon$ using one exact resolvent call.

### A2 - two affine maximal monotone operators on the line

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

On the real line take $A_\pm(z)=(2\varepsilon/R)(z\mp R)$ and $z_0=0$. The roots are $\pm R$. Residual at most $\varepsilon$ requires the output to lie within radius $R/2$ of the respective root. These success sets are disjoint, so one zero-query output distribution cannot attain probability $2/3$ on both instances.

### A3 - return (z0,0)

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

When the initialization radius is $R=0$, the promise gives $0\in A(z_0)$. Return the graph pair $(z_0,0)$ without a query. It has zero residual and satisfies the output requirement exactly.

### A4 - nonnegative cost

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

Query cost is nonnegative. Combined with a zero-query witness, this proves exact zero cost.
