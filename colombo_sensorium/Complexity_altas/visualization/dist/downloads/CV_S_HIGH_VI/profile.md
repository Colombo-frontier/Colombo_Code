# Higher-order monotone variational inequalities: complete operator jets and tangential residual

**Setting ID.** `CV_S_HIGH_VI`

Variational inequalities

Solve the monotone VI $0\in F(z)+N_K(z)$ by returning a feasible point with small tangent residual.

**Status.** Fully optimal

**TASK tags.** formulation: Stampacchia vi; task family: Variational inequality

**MODEL tags.** geometry: Diameter bound; monotonicity: Monotone; smoothness: Highest derivative lipschitz

**ORACLE tags.** feedback quality: Exact; interface family: Complete operator jet; operation: Operator complete jet; operation: Projection; operator derivative order: Parameterized order p−1 (see exact operation binding); public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Tangential residual

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N jet; measure: N model solve; measure: N projection; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve the monotone VI $0\in F(z)+N_K(z)$ by returning a feasible point with small tangent residual.

### Admissible model

The set $K\subset\mathbb{R}^d$ is known, nonempty, compact, and convex, with $\operatorname{diam}(K)\le D_K$. Queries and outputs lie in $K$. Differentiability conditions hold on a neighborhood of $K$.

Fix an integer $p\ge2$. The operator $F$ is monotone, meaning $\langle F(u)-F(v),u-v\rangle\ge0$; moreover, $F\in C^{p-1}$ and $\|\mathrm{D}^{p-1}F(u)-\mathrm{D}^{p-1}F(v)\|_{\rm op}\le L_p\|u-v\|_2$.

These conditions ensure existence of a solution. Derivative tensors use the multilinear operator norm induced by the Euclidean norm.

### Oracle interface

Public inputs comprise the dimension $d$ and parameters $D_K$, $L_p$, $\varepsilon$, and $p$, together with the stated initial point and feasible-set information. Analytic descriptions of hidden functions, operators, and matrices are not supplied.

$$
z\in K\longmapsto(F(z),\mathrm{D}F(z),\ldots,\mathrm{D}^{p-1}F(z))
$$

One exact query returns the entire derivative bundle, not just tensor actions along a selected direction. Repeated queries at the same point are allowed.

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

### Output

Return $\widehat{z}\in K$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\operatorname{dist}(0,F(\widehat{z})+N_K(\widehat{z}))
$$

This nonnegative error uses the declared Euclidean geometry.

For a closed convex set $K$, define $N_K(z)=\{v:\langle v,u-z\rangle\le0,\ \forall u\in K\}$ for $z\in K$, and $\operatorname{dist}(0,S)=\inf_{v\in S}\|v\|_2$.

### Resource accounting

Each complete jet call counts once in $N_{\rm jet}$. Projection and known Taylor-model solution counts are recorded separately; the main comparison counts only $N_{\rm jet}$.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\operatorname{dist}(0,F(\widehat{z})+N_K(\widehat{z}))\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$D_K$: A Euclidean-diameter bound on the feasible domain. **Domain:** Positive real number.

$\operatorname{diam}(K)=\sup_{u,v\in K}\|u-v\|_2\le D_K$

$L_p$: Lipschitz upper bound for the operator's order-(p-1) Fréchet derivative in the Euclidean induced tensor norm **Domain:** Positive real number.

$\|\mathrm D^{p-1}F(z)-\mathrm D^{p-1}F(w)\|_{\rm op}\le L_p\|z-w\|_2$

$\chi$: Dimensionless accuracy ratio expressed in the units of the specified metric **Domain:** Positive real number.

$\chi=L_pD_K^p/\varepsilon$

$d$: Finite Euclidean dimension of the operator domain; regime quantifiers specify whether complexity is uniform in dimension **Domain:** Positive integer.

$\varepsilon$: This is the tangent-residual tolerance. The mean-square guarantee uses its square $\varepsilon^2$. **Domain:** Positive real number.

$p$: Fix the operator order parameter. One jet query returns the complete bundle from F through $\mathrm D^{p-1}F$. **Domain:** Integer at least $2$.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$F$: The unknown operator is single-valued. Monotonicity, strong monotonicity, or weak Minty properties use the specification’s explicit inequalities. **Domain:** A vector map from the declared query domain into $\mathbb R^d$.

$z,u,v$: The operator argument and comparison point in the inequality. **Domain:** The ambient space is $\mathbb R^d$. Formulas constrained by $K$ require the corresponding point to lie in $K$.

$\mathrm D^jF$: The jth Fréchet derivative of operator F. One interface call returns every tensor in the bundle. **Domain:** For $0\le j\le p-1$, the interface takes $j$ vectors in $\mathbb R^d$ and returns one vector in $\mathbb R^d$.

$\mathrm D^0F=F$

$\|\cdot\|_{\rm op}$: Matrix or multilinear tensor norm induced by the Euclidean norm **Domain:** Matrix and derivative tensors used in this profile.

$\|T\|_{\rm op}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}\|T[u_1,\ldots,u_j]\|_2$

$K$: A known nonempty compact convex feasible set. **Domain:** A subset of Euclidean space.

$K\subset\mathbb R^d$

$N_K(z)$: Use the Euclidean normal cone of the closed convex feasible set K at the feasible point z. The same definition applies blockwise to $N_X$ and $N_Y$. **Domain:** $z\in K,\quad N_K(z)\subset\mathbb R^d$.

$N_K(z)=\{v:\langle v,u-z\rangle\le0\ \forall u\in K\}$

$\operatorname{dist}(0,S)$: Infimum of the Euclidean distances from vectors in $S$ to the origin **Domain:** Nonnegative extended real value.

$\operatorname{dist}(0,S)=\inf_{v\in S}\|v\|_2$

$\widehat z$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** $K\subset\mathbb R^d$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm jet}$: Number of complete operator-jet calls through the stated derivative order. **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Number of exact Euclidean projections onto the known feasible domain, recorded separately from primary information queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm model_solve}$: exact regularized Taylor-model VI solves use known returned coefficients; uncharged information cost, arithmetic/bit complexity not certified **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm jet}(\mathcal A,I,\omega)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - Main higher-order theorem regime

**Region.** Fix the integer $p\ge2$ and impose $\chi=L_pD_K^p/\varepsilon\ge2$. The worst case ranges over all admissible finite dimensions.

**Quantity.** Q1

**Resource.** The number of complete jet responses.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega_p(\chi^{2/(3p-1)})
$$

**Upper bound.** B1

$$
O_p(1+\chi^{2/(3p-1)})
$$

**Gap or comparison.** $O_p(1)$

**Comparison argument.** The two bounds are not a native two-sided theorem from one paper. Domain diameter, complete-jet access, fixed budget, and instancewise success probability have been aligned explicitly.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - Inexact accelerated Halpern with adaptive tensor subsolver

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Accelerated Halpern and known-model subroutines with complete jets use no random selection. Scalar-jet simulation preserves this determinism.

$$
O_p(1+\chi^{2/(3p-1)})
$$

**Sources.** [2](https://arxiv.org/pdf/2609.23557v1)

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N jet.**

$$
O_p(1+\chi^{2/(3p-1)})
$$

**N projection.** $O_p\!\left(1+\chi^{2/(3p-1)}\right)$. Use the objective-specific $\chi$ and retain the dependence on the fixed order $p$.

**N model solve.** The bound is $O_p\!\left(1+\chi^{2/(3p-1)}\right)$. Only models defined by returned coefficients are solved exactly; internal arithmetic does not count as queries.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** The source assumes initial distance to a solution bounded by $R_0\le D_K$, so this setting's diameter bound $D_K$ suffices. Deterministic success implies success probability at least $2/3$. The upper bound without an additional logarithm is from 2609.23557v1.

**Source location.** [2](https://arxiv.org/pdf/2609.23557v1) Assumptions2.1–2.4; Definition2.1/2.2; Theorems3.1,5.1; Lemma5.4

Log-free O_p((L_p R_0^p/epsilon)^{2/(3p-1)}) operator-jet upper.

Source R_0=||x0-x*|| <= $D_K$, not a new diameter assumption. Full operator jet through p-1; same-point tangent certificate. All nested F calls counted. Exact known Taylor-model solves are internal. Fixed p. Deterministic upper satisfies randomized success2/3. Source does not itself supply unrestricted randomized lower.

Let $T$ denote the outer iteration count. Lemma 5.4 and (22)-(23) sum all inner-solver calls to obtain total inner cost $O(T)$. The counted object is a full jet call, so outer iterations alone are insufficient. Bound the source initial distance to a solution by the domain diameter $D_K$.

### B2 - flat-gated monotone operator chains and adaptive transcripts

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** The verified source theorem allows arbitrary randomized adaptive algorithms. Domain, output, dimension, and fixed-budget conditions remain those of the specification and region.

$$
\Omega_p(\chi^{2/(3p-1)})
$$

**Sources.** [1](https://arxiv.org/pdf/2609.13462v2)

**Dimension conditions.** For $N$ calls, the deterministic hard construction requires $d\ge2N+2$; for randomized algorithms, dimension $d=O_p(N^3\log(N+2))$ suffices. Subscript $p$ permits constants to depend on the fixed order $p$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega_p(\chi^{2/(3p-1)})
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2609.13462v2) Definitions3.1–3.2; Theorems3.3,11.1,11.3

Unrestricted randomized feasible-query fixed-cap high-dimensional lower Omega_p(q_tan^{2/(3p-1)}).

q_tan=L_p $D_K$^p/epsilon>=2. No lower derivative norm bounds. Deterministic d>=2N+2, randomized sufficient d=O_p(N^3 log(N+2)). The paper's own upper has log^{6(p-1)}; do not attribute log-free bound to it.

The specification retains feasible-domain queries, complete derivative bundles, arbitrary outputs, and private randomness independent of the instance. It does not claim an independent line-by-line verification of the full proof.

## References

[1] Haihan Zhang; Wendao Wu; Chenheng Zhang; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Higher-Order Oracle Complexity for Smooth Monotone Variational Inequalities. 2026. arXiv:2609.13462v2, 2026-10-19.

https://arxiv.org/pdf/2609.13462v2

[2] Xinliang Zhang; Lesi Chen; Linxuan Pan; Chengchang Liu; Junchi Yang; Jingzhao Zhang. Optimal High-Order Methods for Solving Monotone Variational Inequalities. 2026. arXiv:2609.23557v1, 2026-09-20.

https://arxiv.org/pdf/2609.23557v1
